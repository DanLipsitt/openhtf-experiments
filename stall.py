from __future__ import print_function
import openhtf as htf
from time import sleep
from openhtf.output.callbacks import json_factory


def stall(test):
    """Stall so we can test keyboard interrupt."""
    test.logger.info('sleeping...')
    sleep(5)
    test.logger.info('done sleeping')


if __name__ == '__main__':
    import sys
    import thread

    test = htf.Test(
        stall,
        test_name='stall'
    )

    test.add_output_callbacks(json_factory.OutputToJSON(sys.stdout, indent=4))

    test.execute(test_start=lambda: 'stall_demo')
