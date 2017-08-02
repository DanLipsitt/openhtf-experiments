from openhtf.core.measurements import Outcome


def is_fail(test, name):
    """Return whether the given measurement validated with a FAIL outcome."""
    return test.measurements._measurements[name].outcome == Outcome.FAIL


def get_measurement(test, phase_name, measurement_name):
    """Look up a measurement from a previous phase by name.

    Args:
        phase_name(str): The requested phase.
        measurement_name(str): The requested measurement.

    Throws:
        LookupError: When the requested measurement or phase is not found or
        has not been set.

    Returns:
        The value of the requested measurement from the most-recent run of the
        requested phase from the current test. Phases can be run more than
        once in given test.

    """
    try:
        phase = [p for p in test.test_record.phases
                 if p.name == phase_name][-1]
    except IndexError:
        raise LookupError('Phase "{}" not found.'.format(phase_name))
    try:
        measurement = phase.measurements[measurement_name]
    except KeyError:
        raise LookupError('Measurement "{}" not found in phase "{}"'.format(
            measurement_name, phase_name))
    try:
        value = measurement.measured_value
    except AttributeError:
        raise LookupError('No value for measurement "{}" in phase "{}"'.format(
            measurement_name, phase_name))
    return value
