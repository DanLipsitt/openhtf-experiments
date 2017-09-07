"""
"""

from __future__ import print_function
import openhtf as htf
from openhtf.plugs import user_input
from openhtf.output.callbacks import json_factory, console_summary
from util import is_fail


@htf.plug(prompts=user_input.UserInput)
@htf.measures(htf.Measurement('val1'))
def phase1(test, prompts):
    """Phase 1 description."""
    pass


if __name__ == '__main__':
    import os.path

    htf.conf.load(capture_source=True)

    test = htf.Test(
        phase1,
        test_name='example test'
    )

    name = os.path.splitext(os.path.basename(__file__))[0]
    test.add_output_callbacks(
        json_factory.OutputToJSON(name + '.json', indent=4),
        console_summary.ConsoleSummary())

    test.execute(test_start=lambda: 'dut')
