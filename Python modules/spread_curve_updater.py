"""
-------------------------------------------------------------------------------
MODULE
    spread_curve_updater

DESCRIPTION
    Date                : 2014-04-11
    Purpose             : This module contains an implementation of spread
                          curve updater.
    Department and Desk : Credit Desk
    Requester           : Neeran Govender
    Developer           : Jakub Tomaga
    CR Number           : CHNG0001887623

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
"""    

import os

import acm
from at_feed_processing import SimpleXLSFeedProcessor, notify_log


class SpreadCurveXLSFeedProcessor(SimpleXLSFeedProcessor):
    """Feed Processor used for spread curve update."""

    PERIOD_7D = '7d'
    PERIOD_14D = '14d'
    PERIOD_28D = '28d'
    PERIOD_56D = '56d'
    PERIOD_91D = '91d'
    PERIOD_182D = '182d'
    PERIOD_273D = '273d'
    PERIOD_364D = '364d'

    _required_columns = [PERIOD_7D, PERIOD_14D, PERIOD_28D, PERIOD_56D,
        PERIOD_91D, PERIOD_182D, PERIOD_273D, PERIOD_364D]

    def __init__(self, curve_name, file_path, sheet_name):
        super(SpreadCurveXLSFeedProcessor, self).__init__(
            file_path=file_path, sheet_index=None, sheet_name=sheet_name)
        self.curve_name = curve_name

    def _process_record(self, record, dry_run):
        """Handle curve record."""
        _, data = record

        # Get the yield curve
        yield_curve = acm.FYieldCurve[self.curve_name]
        if yield_curve is None:
            message = "Yield curve {0} does not exist."
            raise self.FeedProcessingException(message.format(self.curve_name))

        # Update all the curve's spreads with new values
        for spread in yield_curve.Attributes()[0].Spreads():
            spread_name = spread.Point().Name()
            old_spread_value = spread.Spread()
            new_spread_value = data[spread_name]

            self._log("Changing {0} spread value from {1} to {2}".format(
                spread_name, old_spread_value, new_spread_value))

            if not dry_run:
                spread.Spread = new_spread_value
                spread.Commit()


ael_variables = SpreadCurveXLSFeedProcessor.ael_variables(
    file_dir='F:/', file_name='input.xls')

ael_variables.add('sheet_name', label='Sheet name',
    default='Sheet1', alt='Sheet name value')

ael_variables.add('curve_name', label='Yield curve name',
    default='ZAR-GOV-TBILLS', alt='Yield curve name')


def ael_main(config):
    """The main entry point of the Run Script window."""    
    processor = SpreadCurveXLSFeedProcessor(curve_name=config['curve_name'],
        file_path=os.path.join(config['file_dir'], config['file_name']),
        sheet_name=config['sheet_name'])
    processor.add_error_notifier(notify_log)
    processor.process(config['dry_run'])

    if not processor.errors:
        print('Completed successfully')
