"""
This module contains functionality for trade BO-confirm/termination
requesting.

TimeSeriesUpdateHandler does the automatic confirmation/termination.

The global functions serve as gui callbacks for the saving down of
requests.

History
=======
(Previous history not recorded.)
2015-08-31 Andrei Conicov/Vojtech Sidorin ABITFA-3161: Output the user that has created the Time Series request.
2016-01-14 Vojtech Sidorin  ABITFA-4018: Use AEL instead of ACM when updating FX Swaps.
"""

import acm
import ael
from FTradeStatus import is_component_in_user_profile
import at_timeSeries
import traceback
import FValidation
from Queue import Queue
from auto_confirm import AutoConfirmation as AC

# Components required for the two request actions.
BO_CONFIRM_COMPONENT = 'RequestBOConfirm'
TERMINATE_COMPONENT = 'RequestTerminate'

# Names of the two time series used for requests.
TIME_SERIES_SPEC_BO_CONFIRM = 'TradeNumber'
TIME_SERIES_SPEC_TERMINATE = 'TerminateTrdnbr'

# Entry trade statuses for the requests.
ALLOWED_STATUSES_FOR_BO_CONFIRM = ('FO Confirmed',)
ALLOWED_STATUSES_FOR_TERMINATION = ('BO Confirmed', 'BO-BO Confirmed')

# Synchronized queue to hold the requests.
request_queue = Queue()


def log(message):
    """Log the message with current date and time."""
    print('{0}: {1}'.format(acm.Time.TimeNow(), message))


def log_exception():
    """Log the last raised exception."""
    log('Exception:')
    traceback.print_exc()


def start():
    """Subscribe to TimeSeries."""

    log("Starting...")
    TimeSeriesUpdateHandler.register_time_series(TIME_SERIES_SPEC_BO_CONFIRM)
    TimeSeriesUpdateHandler.register_time_series(TIME_SERIES_SPEC_TERMINATE)
    log('Started in main.')


def stop():
    """Unsusbscribe from TimeSeries."""

    log("Stopping...")
    TimeSeriesUpdateHandler.cancel_registrations()
    log('Process stopped')
    return


def work():
    while not request_queue.empty():
        request = request_queue.get()
        request.process()


class Request(object):
    """Holds and processes one request."""
    def __init__(self, time_series, allowed_statuses, target_status):
        self._time_series = time_series
        self._allowed_statuses = allowed_statuses
        self._target_status = target_status

    def process(self):
        """Process the given time series record and the referenced trade.

        This tries to move the trade to the target status. Any exceptions
        during the commit of the trade or the time series are logged.
        """

        try:
            trade = acm.FTrade[self._time_series.Recaddr()]
            user = self._time_series.CreateUser().Name()
            if trade.Status() == self._target_status:
                log('Trade {0} is already {1} ({2})'.format(
                    trade.Oid(), self._target_status, user))

                # The request is irrelevant, the trade is in the target state.
                # Delete the request.
                self._time_series.Delete()
            elif trade.Status() not in self._allowed_statuses:
                log('Trade {0} is not in one of the required states ({1}) ({2})'.format(
                    trade.Oid(), ','.join(self._allowed_statuses), user))

                # The request is not valid, the trade status got changed since the
                # request had been placed. Delete the request.
                self._time_series.Delete()
            else:
                try:
                    if trade.IsFxSwap():
                        # FX Swaps need to have both trades in the same status.
                        # This needs to be done in a transaction.

                        # ABITFA-4018: The code below uses ACM, which has
                        # issues when updating certain FX Swap trades, e.g.
                        # 57260936 or 57459076. AEL works and is used instead.

                        # ACM variant -- doesn't work with certain trades
                        #acm.BeginTransaction()
                        #try:
                        #    other_trade = None
                        #    if trade.IsFxSwapNearLeg():
                        #        other_trade = trade.FxSwapFarLeg()
                        #    else:
                        #        other_trade = trade.FxSwapNearLeg()

                        #    trade.Status(self._target_status)
                        #    other_trade.Status(self._target_status)
                        #    trade.Commit()
                        #    other_trade.Commit()

                        #    acm.CommitTransaction()
                        #except:
                        #    acm.AbortTransaction()
                        #    raise

                        # AEL variant
                        other = None
                        if trade.IsFxSwapNearLeg():
                            other = trade.FxSwapFarLeg()
                        else:
                            other = trade.FxSwapNearLeg()
                        ael_trade = ael.Trade[trade.Oid()]
                        ael_clone = ael_trade.clone()
                        ael_other = ael.Trade[other.Oid()]

                        ael_clone.status = self._target_status
                        ael_clone.commit_fx_swap(ael_other)
                    else:
                        # FIXME Remove once Prime >= 2015.3 is deployed
                        AC.hotfix_confirm_trade(trade, self._target_status)
                    log('Trade {0} committed ({1})'.format(trade.Oid(), user))
                except Exception:
                    log('Cannot commit trade {0} ({1})'.format(trade.Oid(), user))
                    raise

                # Once the trade is processed, flag the time series so that it
                # doesn't get processed again.
                self._time_series.RunNo(1)
                try:
                    self._time_series.Commit()
                except:
                    # This is a problem which needs to be dealt with manually.
                    log('Could not update time series {0} ({1}).'.format(self._time_series.Oid(), user))
                    raise

        except Exception as ex:
            log_exception()
            try:
                # Catch everything as this is a script that must not fail.
                self.notify_user(self._time_series, ex)

                # Delete the request as it needs to be able to be
                # placed again.
                self._time_series.Delete()
            except:
                log_exception()

    def notify_user(self, time_series, exception):
        """Notify user of an error which prevented the trade action."""
        user = time_series.CreateUser()
        subject = "Trade could not be {0}".format(self._target_status)
        body = []

        info_msg = "Trade {0} could not be {1} due to the following error:\n"
        body.append(info_msg.format(
                time_series.Recaddr(), self._target_status))
        body.append(str(exception) + "\n")

        if FValidation.last_exc_info:
            body.extend(traceback.format_exception(*FValidation.last_exc_info))

        trade = acm.FTrade[time_series.Recaddr()]
        acm.SendUserMessage([user], subject, ''.join(body), trade)


class TimeSeriesUpdateHandler(object):
    """Reacts to changes to the time series table.

    Instances of this class move trades into the required states as requested.

    """

    # Store all handlers here.
    _handlers = {}

    @classmethod
    def register_time_series(cls, time_series_name):
        """Registers a handler for the given time series.

        Supported time series: TradeNumber, TerminationTrdnbr.

        """
        if time_series_name in cls._handlers:
            raise ValueError('This Time Series is already monitored.')

        cls._handlers[time_series_name] = cls(time_series_name)

    @classmethod
    def cancel_registrations(cls):
        """Removes registration of all instances."""
        for time_series_name, handler in cls._handlers.items():
            handler.cancel_registration()
            del cls._handlers[time_series_name]

    def __init__(self, time_series_name):
        """Initialize the handler.

        This registers the handler as dependent on the time series which
        weren't processed yet. Any unprocessed time series get processed
        during the initialization, then all new records trigger the
        ServerUpdate method.

        """

        specification = acm.FTimeSeriesSpec[time_series_name]
        where = 'timeSeriesSpec = {0} and runNo = 0'.format(specification.Oid())
        self._selection = acm.FTimeSeries.Select(where)

        if time_series_name == TIME_SERIES_SPEC_BO_CONFIRM:
            self._target_status = 'BO Confirmed'
            self._allowed_statuses = ALLOWED_STATUSES_FOR_BO_CONFIRM
        elif time_series_name == TIME_SERIES_SPEC_TERMINATE:
            self._target_status = 'Terminated'
            self._allowed_statuses = ALLOWED_STATUSES_FOR_TERMINATION

        # Process unprocessed records.
        log('Processing queued requests for {0}.'.format(time_series_name))
        for time_series in self._selection.AsList():
            self._add_request(time_series)

        log('Registering listener for {0}.'.format(time_series_name))
        self._selection.AddDependent(self)

    def cancel_registration(self):
        """Removes the hook from dependent handlers."""
        self._selection.RemoveDependent(self)

    def ServerUpdate(self, time_series_selection, operation, time_series):
        """Picks up time series inserts and confirms/terminates trades."""

        # Only pick up insert actions. There are always 2 update actions
        # following immediately after which need to be ignored.
        if (str(operation) == 'insert' and time_series.RunNo() == 0):
            # Put a request in the queue so that it can be safely processed.
            self._add_request(time_series)

    def _add_request(self, time_series):
        request = Request(time_series, self._allowed_statuses, self._target_status)
        request_queue.put(request)


def _request_status_change(trade, time_series_name):
    """Request change to BO Confirmed or Terminated.

    time_series_name -- one of (TIME_SERIES_SPEC_BO_CONFIRM, TIME_SERIES_SPEC_TERMINATE)

    This creates a record in the time series specified by time_series_name.
    Raises ValueError if the trade is not in the correct entry status or
    if the time series has already been requested.

    """

    if time_series_name == TIME_SERIES_SPEC_BO_CONFIRM:
        allowed_statuses = ALLOWED_STATUSES_FOR_BO_CONFIRM
    elif time_series_name == TIME_SERIES_SPEC_TERMINATE:
        allowed_statuses = ALLOWED_STATUSES_FOR_TERMINATION

    date = acm.Time.DateToday()
    if trade.Status() in allowed_statuses:
        if _request_exists(trade, time_series_name):
            message = 'Request already sent.'
            raise ValueError(message)

        at_timeSeries.add_time_series_value(time_series_name, trade.Oid(), 0, date, 0)
    else:
        message = 'Trade must have status {0}.'.format(
            ', '.join(map(str, allowed_statuses)))
        raise ValueError(message)


def _request_exists(trade, time_series_name):
    """Check if the action was previously requested."""
    time_series_spec = acm.FTimeSeriesSpec[time_series_name]
    for time_series in time_series_spec.TimeSeries():
        if time_series.Recaddr() == trade.Oid() and time_series.RunNo() == 0:
            # If the trade is being requested correctly for the second time,
            # all the previous requests must already have run_no=1.
            return True

    return False


def _request_single_status_change(trade, time_series_name):
    """Request a status change of a single trade."""


def _confirm_action(time_series_name):
    """Check user profile and ask for confirmation of the action.

    Returns True if the action should be executed, False otherwise.

    """
    if time_series_name == TIME_SERIES_SPEC_BO_CONFIRM:
        warning_msg = 'Do you really want to BO Confirm the trade(s)?'
        required_component = BO_CONFIRM_COMPONENT
    elif time_series_name == TIME_SERIES_SPEC_TERMINATE:
        warning_msg = 'Do you really want to TERMINATE the trade(s)?'
        required_component = TERMINATE_COMPONENT

    dialog_func = acm.GetFunction('msgBox', 3)

    # Check for required profile component.
    if is_component_in_user_profile(required_component) != 1:
        message = 'Request not allowed. Please contact Front Arena support.'
        dialog_func('Warning', message, 0)
        return False

    buttonSelected = dialog_func('Warning', warning_msg, 1)

    # 1 == Ok button was pressed.
    if buttonSelected == 1:
        return True

    return False


def _menu_request_single_status_change(eii, time_series_name):
    """A menu extension code for single status change request.

    Retrieves the trade object from eii and checks for eligibility
    and confirmation from the user.

    """

    obj = eii.ExtensionObject()
    trade = obj.OriginalTrade()
    if _confirm_action(time_series_name):
        try:
            _request_status_change(trade, time_series_name)
        except (RuntimeError, ValueError):
            log_exception()
            dialog_func = acm.GetFunction('msgBox', 3)
            message = ('Error placing request, see log for details.')
            dialog_func('Warning', message, 0)


def _menu_request_bulk_status_change(eii, time_series_name):
    """A menu extension code for bulk status change.

    Processes all selected trades, checks user eligibility and
    confirmation and then executes the status change. If any trades are
    problematic, this writes the reasons in the log and pops up
    a message.

    """
    dialog_func = acm.GetFunction('msgBox', 3)

    rows = eii.ExtensionObject().ActiveSheet().Selection()
    trades = rows.SelectedTrades()
    if not trades:
        print('Warning: No trades selected.')
        return

    if not _confirm_action(time_series_name):
        return

    wrong_trades = False
    for trade in trades:
        try:
            _request_status_change(trade, time_series_name)
        except (RuntimeError, ValueError):
            wrong_trades = True
            print("Error on trade", trade.Oid(), ":")
            traceback.print_exc()

    if wrong_trades:
        message = ('Some trades were not changed due to errors.'
            ' Please see the log for details.')
        dialog_func('Warning', message, 0)


def menu_request_single_confirmation(eii):
    """Request single confirmation.

    If the trade cannot be confirmed for some reason, a dialog pops up.

    """
    _menu_request_single_status_change(eii, TIME_SERIES_SPEC_BO_CONFIRM)


def menu_request_single_termination(eii):
    """Request single termination.

    If the trade cannot be confirmed for some reason, a dialog pops up.

    """
    _menu_request_single_status_change(eii, TIME_SERIES_SPEC_TERMINATE)


def menu_request_bulk_confirmation(eii):
    """Request bulk confirmation from a Trading Manager.

    If some trades cannot be confirmed for some reason, they are skipped
    and the reasons are dumped in the log. A single informative dialog
    pops up after the whole set is processed.

    """
    _menu_request_bulk_status_change(eii, TIME_SERIES_SPEC_BO_CONFIRM)


def menu_request_bulk_termination(eii):
    """Request bulk termination from a Trading Manager.

    If some trades cannot be confirmed for some reason, they are skipped
    and the reasons are dumped in the log. A single informative dialog
    pops up after the whole set is processed.

    """
    _menu_request_bulk_status_change(eii, TIME_SERIES_SPEC_TERMINATE)
