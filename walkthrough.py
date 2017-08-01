"""OpenHTF demonstrations."""

from __future__ import print_function
import openhtf as htf
from openhtf.plugs import user_input
from openhtf.output.callbacks import json_factory, console_summary
from util import is_fail


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
        fail_mid_phase,
        test_name='example test'
    )

    name = os.path.splitext(os.path.basename(__file__))[0]
    test.add_output_callbacks(
        json_factory.OutputToJSON(name + '.json', indent=4),
        console_summary.ConsoleSummary())

    test.execute(test_start=lambda: 'dut')
