from __future__ import print_function
import openhtf as htf
from openhtf.output.callbacks import json_factory


def phase1(test):
    pass


@htf.measures(htf.Measurement('x').in_range(0, 1))
def phase2(test):
    test.measurements.x = -1


def phase3(test):
    test.logger.warning("We don't want to make it here")


if __name__ == '__main__':
    import sys

    test = htf.Test(
        phase1,
        phase2,
        test_name='phase naming experiment'
    )

    test.add_output_callbacks(json_factory.OutputToJSON(sys.stdout, indent=4))

    test.execute(test_start=lambda: "example failed phase")
