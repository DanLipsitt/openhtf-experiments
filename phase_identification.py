from __future__ import print_function
import openhtf as htf
from openhtf.output.callbacks import json_factory


def phase1(test):
    pass

def phase2(test):
    """Phase 2 has a docstring."""
    pass

if __name__ == '__main__':
    import sys

    htf.conf.load(capture_source=True)

    test = htf.Test(
        phase1,
        phase2,
        test_name='phase naming experiment'
    )

    test.add_output_callbacks(json_factory.OutputToJSON(sys.stdout, indent=4))

    test.execute(test_start=lambda: 'phases_demo')
