from __future__ import print_function
import openhtf as htf
from openhtf.output.callbacks import json_factory


def phase1(test):
    print('phase 1 (pass)')


@htf.measures(htf.Measurement('x').in_range(0, 1))
def phase2(test):
    test.measurements.x = -1
    print('phase 2 (fail)')


def phase3(test):
    print("phase 3 (we shouldn't get here!)")


if __name__ == '__main__':
    import sys

    test = htf.Test(
        phase1,
        phase2,
        phase3,
        test_name='phase failure demo'
    )

    test.add_output_callbacks(json_factory.OutputToJSON(sys.stdout, indent=4))

    test.execute(test_start=lambda: "dut")
