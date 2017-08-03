from __future__ import print_function

import openhtf as htf
from openhtf.output.callbacks import console_summary, json_factory
from openhtf.plugs import user_input
from openhtf.util.validators import matches_regex, register


@register
def valid_serial():
    return matches_regex(r'x')


@htf.plug(prompts=user_input.UserInput)
@htf.measures(htf.Measurement('serial').valid_serial())
def get_serial(test, prompts):
    serial = prompts.prompt(message="Enter a serial number", text_input=True)
    test.measurements.serial = serial
    test.test_record.dut_id = serial


if __name__ == '__main__':
    import os.path

    test = htf.Test(test_name='dut input')

    name = os.path.splitext(os.path.basename(__file__))[0]
    test.add_output_callbacks(
        json_factory.OutputToJSON(name + '.json', indent=4),
        console_summary.ConsoleSummary())

    test.execute(test_start=get_serial)
