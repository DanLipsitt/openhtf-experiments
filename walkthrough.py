"""OpenHTF demonstrations."""

from __future__ import print_function
import re
import openhtf as htf
from openhtf.plugs import user_input
from openhtf.output.callbacks import json_factory, console_summary
from openhtf.util.validators import register, RegexMatcher
from util import is_fail, get_measurement


class SerialValidator(RegexMatcher):
    def __init__(self):
        regex = r'\w{4}'
        super(SerialValidator, self).__init__(regex, re.compile(regex))

    def __str__(self):
        # Shown in output.
        return 'Value must consist of four characters.'

    def __deepcopy__(self, dummy_memo):
        # This method required by the validator spec. We can abstract this away
        # later.
        return type(self)()


register(SerialValidator, name='valid_serial')


class NumericSerialValidator(RegexMatcher):
    def __init__(self):
        regex = r'\d{4}'
        super(NumericSerialValidator, self).__init__(regex, re.compile(regex))

    def __str__(self):
        return 'Value must consist of four digits.'

    def __deepcopy__(self, dummy_memo):
        return type(self)()


register(NumericSerialValidator, name='valid_numeric_serial')


@htf.plug(prompts=user_input.UserInput)
@htf.measures(htf.Measurement('scanned_serial').valid_serial())
def scan_serial(test, prompts):
    """Scan in a new serial for the DUT."""
    test.measurements.scanned_serial = prompts.prompt(
        'Enter a serial (four digits):', text_input=True)
    if is_fail(test, 'scanned_serial'):
        test.logger.warning('Invalid serial. Try again.')
        return htf.PhaseResult.REPEAT


@htf.measures(htf.Measurement('original_serial').valid_numeric_serial())
def get_earlier_measurement(test):
    test.measurements.original_serial = get_measurement(
        test, 'scan_serial', 'scanned_serial')


@htf.measures(
    htf.Measurement('succeed').equals(True).doc('This test should succeed.'),
    htf.Measurement('fail_ok').equals(True).doc('Fail but keep going.'),
    htf.Measurement('fail_fatal').equals(True).doc('Fail and stop.'),
    htf.Measurement('skipped').equals(True).doc("This shouldn't run.")
)
def fail_mid_phase(test):
    """Fail before we get to the end of the phase."""
    test.measurements.succeed = True
    test.measurements.fail_ok = False
    test.measurements.fail_fatal = False
    if is_fail(test, 'fail_fatal'):
        return htf.PhaseResult.STOP
    test.measurements.skipped = False


if __name__ == '__main__':
    import os.path

    htf.conf.load(capture_source=True)

    test = htf.Test(
        scan_serial,
        get_earlier_measurement,
        fail_mid_phase,
        get_earlier_measurement,
        test_name='example test'
    )

    name = os.path.splitext(os.path.basename(__file__))[0]
    test.add_output_callbacks(
        json_factory.OutputToJSON(name + '.json', indent=4),
        console_summary.ConsoleSummary())

    test.execute(test_start=lambda: 'dut')
