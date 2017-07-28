"""
Real-ish scenario:

- get the serial over ssh
- check it's blank
- burn a new serial pulled from a barcode
- validate the serial on the tool matches barcode

"""

from __future__ import print_function
import openhtf as htf
from openhtf.plugs import user_input
from openhtf.output.callbacks import json_factory
from util import is_fail


class PlatformSSH(htf.plugs.BasePlug):
    """Mockup of SSH command interface to a DUT."""

    def __init__(self):
        self.serial = ''

    def get_serial(self):
        return self.serial

    def set_serial(self, serial):
        self.serial = serial

@htf.plug(platform=PlatformSSH)
@htf.measures(htf.Measurement('old_serial').equals(''))
def assert_blank_serial(test, platform):
    """Check that the serial is currently blank."""
    test.measurements.old_serial = platform.get_serial()


@htf.plug(prompts=user_input.UserInput)
@htf.measures(htf.Measurement('scanned_serial').matches_regex(r'\d{4}'))
def scan_serial(test, prompts):
    """Scan in a new serial for the DUT."""
    test.measurements.scanned_serial = prompts.prompt(
        'Enter a serial (four digits):', text_input=True)
    if is_fail(test, 'scanned_serial'):
        test.logger.warning('Invalid serial. Try again.')
        return htf.PhaseResult.REPEAT


@htf.plug(platform=PlatformSSH)
@htf.measures(htf.Measurement('serial').matches_regex(r'\d{4}'))
def burn_serial(test, platform):
    """Burn the new serial onto the DUT and verify that it can be read."""
    scanned_serial = test.test_record.phases[-1].measurements['scanned_serial'].measured_value
    platform.set_serial(scanned_serial)
    serial = platform.get_serial()
    test.measurements.serial = serial
    # haven't a way to do this using validators yet...
    if serial != scanned_serial:
        test.logger.warning(
            'Fail: serial {} does not equal scanned serial {}'.format(serial, scanned_serial))
        return htf.PhaseResult.STOP


if __name__ == '__main__':
    import sys

    test = htf.Test(
        assert_blank_serial,
        scan_serial,
        burn_serial,
        test_name='simulated serial check'
    )

    test.add_output_callbacks(json_factory.OutputToJSON(sys.stdout, indent=4))

    test.execute(test_start=lambda: 'dut')
