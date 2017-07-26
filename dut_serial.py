from __future__ import print_function
import openhtf as htf
from openhtf.plugs.user_input import prompt_for_test_start
from openhtf.output.callbacks import json_factory

if __name__ == '__main__':
    import sys

    test = htf.Test(
        test_name='dut input'
    )

    test.add_output_callbacks(json_factory.OutputToJSON(sys.stdout, indent=4))

    test.execute(
        test_start=prompt_for_test_start(
            message="This prompt only accepts 'x' as an answer.",
            validator=lambda s: s if s == 'x' else False))
