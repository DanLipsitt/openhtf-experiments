from __future__ import print_function

import openhtf as htf
from openhtf.output.callbacks import console_summary, json_factory
from openhtf.plugs import user_input
from openhtf.util.validators import matches_regex, register
from util import is_fail


@register
def valid_serial():
    return matches_regex(r'x')


@htf.PhaseOptions(repeat_limit=5)
@htf.plug(prompts=user_input.UserInput)
@htf.measures(htf.Measurement('serial').valid_serial())
def get_serial(test, prompts):
    serial = prompts.prompt(
        message="Enter a serial number (must be 'x')", text_input=True)
    test.measurements.serial = serial
    if is_fail(test, 'serial'):
        return htf.PhaseResult.REPEAT
    test.test_record.dut_id = serial


@htf.plug(prompts=user_input.UserInput)
@htf.measures(htf.Measurement('value').matches_regex('a'))
def get_value(test, prompts):
    test.measurements.value = prompts.prompt(
        message="Enter the letter 'a'", text_input=True)


if __name__ == '__main__':
    import os.path

    test = htf.Test(
        get_value,
        test_name='dut input'
    )

    name = os.path.splitext(os.path.basename(__file__))[0]
    test.add_output_callbacks(
        json_factory.OutputToJSON(name + '.json', indent=4),
        console_summary.ConsoleSummary())

    test.execute(test_start=get_serial)
