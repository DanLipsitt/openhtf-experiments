from openhtf.core.measurements import Outcome


def is_fail(test, name):
    """Return whether the given measurement validated with a FAIL outcome."""
    return test.measurements._measurements[name].outcome == Outcome.FAIL
