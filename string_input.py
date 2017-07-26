from __future__ import print_function
import openhtf as htf
from openhtf.plugs.user_input import UserInput
from openhtf.output.callbacks import json_factory


@htf.measures(htf.Measurement('input').in_range(0, 1))
@htf.plug(prompts=UserInput)
def int_from_prompt(test, prompts):
    test.measurements.input = prompts.prompt(
        'Enter an integer:', text_input=True)


@htf.measures(htf.Measurement('input').in_range(0, 1))
def int_from_string_error(test):
    test.measurements.input = '1'

if __name__ == '__main__':
    import sys

    htf.conf.load_from_dict({'capture_source': True})

    test = htf.Test(
        int_from_prompt,
#        int_from_string_error,
        test_name='string input'
    )

    test.add_output_callbacks(json_factory.OutputToJSON(sys.stdout, indent=4))

    test.execute(test_start=lambda: 'string input demo')
