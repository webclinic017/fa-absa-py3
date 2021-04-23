"""
This module contains functionality for saving down PnL values into TimeSeriesDv
as soon as a trade is FO Confirmed.

Date              JIRA               Developer               Requestor
==========        ====               ====================    ===================
2014-10-20        ABITFA-2382        Pavel Saparov           Nick Bance
"""

import acm
import ael
import math
import traceback
import at_timeSeriesDv

from Queue import Queue
from datetime import datetime, timedelta
from at_time import to_date, to_datetime, datetime_from_string
from at_calculation_space import prepare_calc_space

# Synchronized queue to hold requests for processing
REQUEST_QUEUE = Queue()


def log(message):
    """Log the message with current date and time."""
    print('{0}: {1}'.format(acm.Time.TimeNow(), message))


def log_exception():
    """Log the last raised exception."""
    log('Exception:')
    traceback.print_exc()


class Request(object):
    """Class representing request container"""


    def __init__(self, trade):
        """Initialize the object.

        Args:
            trade: a trade object (FTrade)
        """
        self.trade = trade

    def process(self):
        """Will save down relevant PnL calculation to Time Series Dv"""

        trade_oid = self.trade.Oid()
        instr_oid = self.trade.Instrument().Oid()

        today = acm.Time.DateToday()
        offset = datetime.now() - timedelta(minutes=15)

        # process only if execution time is equal to Today and as the part
        # of business decision is to permit re-saving of Deltas and PNL values
        # only 15 minutes after execution time
        if (datetime_from_string(self.trade.ExecutionTime()).date() == to_date(today)
                and datetime_from_string(self.trade.ExecutionTime()) > offset):

            # prepare calc space
            prepare_row = prepare_calc_space('FPortfolioSheet')
            get_column = prepare_row(self.trade)

            log("Saving specific values for trade {0}".format(trade_oid))

            # save TPL to Inception_TPL Time Series
            tpl = get_column('Portfolio Total Profit and Loss')
            if tpl and not math.isnan(tpl.Number()):
                at_timeSeriesDv.update_time_series_value(
                    'Inception_TPL', instr_oid, trade_oid, today, tpl)

            # save Delta to Inception_Delta Time Series
            delta = get_column('Portfolio Delta')
            if delta and not math.isnan(delta.Number()):
                at_timeSeriesDv.update_time_series_value(
                    'Inception_Delta', instr_oid, trade_oid, today, delta)

            # save Yield Delta to Inception_YDelta Time Series
            ydelta = get_column('Portfolio Delta Yield')
            if ydelta and not math.isnan(ydelta.Number()):
                at_timeSeriesDv.update_time_series_value(
                    'Inception_YDelta', instr_oid, trade_oid, today, ydelta)


class InceptionSaverHandler(object):
    """Reacts to changes on the trade table.

    Instances of this class move trades into the required states as requested.
    """

    handler = None

    @classmethod
    def register(cls):
        """Registers a handler"""

        if cls.handler is not None:
            log("Today's booked trades are already being monitored.")

        cls.handler = cls()

    @classmethod
    def unregister(cls):
        """Unregisters a handler"""

        if cls.handler is None:
            log("Unable to unregister the handler.")

        cls.handler.remove()
        cls.handler = None

    def __init__(self):
        """Initialize the handler and subscribe to collection"""

        # subscribe to the whole trade table
        log("Registering listener for today's booked trades.")
        ael.Trade.subscribe(InceptionSaverHandler.listener)

    @staticmethod
    def listener(obj, trade, arg, operation):
        """Picks up a trade and save related PnL details"""

        # Only pick on insert or update actions.
        if str(operation).lower() in ('insert', 'update'):
            # Put a request in the queue so that it can be safely processed.
            trade = acm.FTrade[trade.trdnbr]
            request = Request(trade)
            REQUEST_QUEUE.put(request)

    def remove(self):
        """Removes the subscription from the monitored table"""
        ael.Trade.unsubscribe(InceptionSaverHandler.listener)


def start():
    """Start ATS and subscribe to incoming trades"""

    log("Starting...")
    InceptionSaverHandler.register()

def stop():
    """Stop ATS and unsubscribe"""

    log("Stopping...")
    InceptionSaverHandler.unregister()

def work():
    """Process the queue and try to catch all exceptions"""

    try:
        while not REQUEST_QUEUE.empty():
            request = REQUEST_QUEUE.get()
            request.process()
    except Exception:
        log_exception()
