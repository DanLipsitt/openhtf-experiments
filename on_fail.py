from __future__ import print_function
import openhtf as htf
from openhtf.output.callbacks import json_factory
from openhtf.core.measurements import Outcome
from contextlib import contextmanager
from util import is_fail

def phase1(test):
    print('phase1 (pass)')


@htf.measures(
    htf.Measurement('val1').equals(1),
    htf.Measurement('val2').equals(1),
)
def phase2(test):
    print('phase 2 (fail)')
    # Pass at first.
    test.measurements.val1 = 1
    if is_fail(test, 'val1'):
        return htf.PhaseResult.STOP
    # Same test as is_fail, run manually.
    # Fail this time.
    test.measurements.val2 = -1
    if test.measurements._measurements['val2'].outcome == Outcome.FAIL:
        return htf.PhaseResult.STOP


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
