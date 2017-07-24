from __future__ import print_function
import openhtf as htf
from openhtf.output.callbacks import json_factory


def phase1_continue(test):
    """Continue by default."""
    pass


def phase2_continue(test):
    """Explicitly continue."""
    return htf.PhaseResult.CONTINUE


def phase3_abort(test):
    raise KeyboardInterrupt('simulated user cancellation')


def phase4_after_stop(test):
    """This one shouldn't run."""
    test.logger.error('After STOP. Shouldn\'t get here!')


if __name__ == '__main__':
    import sys

    test = htf.Test(
        phase1_continue,
        phase2_continue,
        phase3_abort,
        phase4_after_stop,
        test_name='abort demo'
    )

    test.add_output_callbacks(json_factory.OutputToJSON(sys.stdout, indent=4))

    test.execute(test_start=lambda: 'abort_demo')
