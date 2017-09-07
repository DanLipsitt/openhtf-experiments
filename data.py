"""
"""

from __future__ import print_function

import datetime

import openhtf as htf
from openhtf.output.callbacks import console_summary, json_factory
from util import is_fail


@htf.measures(
    htf.Measurement('dict1'),
    htf.Measurement('list1'),
)
def phase1(test):
    """Store complex data without using dimensions."""
    test.measurements.dict1 = {'foo': 'a', 'bar': 1.0}
    test.measurements.list1 = [u'x', 10, datetime.datetime.now()]


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
