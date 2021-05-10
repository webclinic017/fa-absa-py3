"""-----------------------------------------------------------------------------
PURPOSE              :  SBL onto FA
                        Collateral trade upload/update script 
                        for project go-live
DESK                 :  PCG Collateral
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-06-11  CHG0105578     Libor Svoboda       Initial Implementation
"""
import csv
from math import copysign

import acm
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from sl_collateral_partial_returns import partial_return


LOGGER = getLogger(__name__)


def uncheck(ael_input, checkbox_var):
    checkbox = ael_variables.get(checkbox_var)
    if ael_input.value:
        checkbox.value = 0


ael_variables = AelVariableHandler()
ael_variables.add_input_file(
    'input_file_path',
    'Data File',
    file_filter='*.txt',
    default=r'C:\FA\coll_val_dates.txt',
)
ael_variables.add_bool(
    'update_value_day',
    label='Update Value Day',
    default=0,
    hook=lambda x: uncheck(x, 'book_returns'),
)
ael_variables.add_bool(
    'book_returns',
    label='Book Returns',
    default=0,
    hook=lambda x: uncheck(x, 'update_value_day'),
)


def get_trade_ref(coll_ref):
    return coll_ref.split(':')[0]


def get_trades(trade_ref):
    return acm.FTrade.Select('tradeCategory="Collateral" and acquirer="SECURITY LENDINGS DESK" and text1="" and text2="%s"' 
                             % trade_ref)


def run_value_day_update(file_path):
    LOGGER.info('Updating value dates using %s' % file_path)
    with open(file_path, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                trade_ref = get_trade_ref(row['Trade Ref'])
                fa_trades = get_trades(trade_ref)
                if not fa_trades:
                    LOGGER.warning('No collateral trades found for ref %s.' % trade_ref)
                    continue
                value_date = row['Sett Date']
                for trade in fa_trades:
                    trade_time = trade.TradeTime()
                    trade_image = trade.StorageImage()
                    trade_image.TradeTime(value_date + trade_time[10:])
                    trade_image.ValueDay(value_date)
                    trade_image.AcquireDay(value_date)
                    try:
                        trade_image.Commit()
                    except:
                        LOGGER.exception('Trade %s, ref %s: Failed to update value day to %s.' 
                                         % (trade.Oid(), trade_ref, value_date))
                    else:
                        LOGGER.info('Trade %s, ref %s: Value day updated to %s.' 
                                    % (trade.Oid(), trade_ref, value_date))
            except:
                LOGGER.info('Failed to process %s.' % row)


def run_return_booking(file_path):
    LOGGER.info('Booking returns using %s' % file_path)
    booked_returns = []
    with open(file_path, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                trade_ref = get_trade_ref(row['Trade Ref'])
                fa_trades = get_trades(trade_ref)
                if not fa_trades:
                    LOGGER.warning('No collateral trades found for ref %s.' 
                                   % trade_ref)
                    continue
                value_date = row['Sett Date']
                trade_date = row['Trade Date']
                trade_time = trade_date + acm.Time.TimeNow()[10:19]
                quantity = abs(int(row['Quantity']))
                swift_flag = 'SWIFT' if row['Mode'] == 'On-Market' else 'DOM'
                for trade in fa_trades[:]:
                    parent = trade.Contract()
                    if parent in booked_returns:
                        LOGGER.info('Trade %s, ref %s: Return already booked.' 
                                    % (trade.Oid(), trade_ref))
                        continue
                    return_quantity = copysign(quantity, -1 * parent.FaceValue())
                    parent_list = acm.FList()
                    parent_list.Add(parent)
                    try:
                        return_trade = partial_return(parent_list, value_date, 
                                                      return_quantity, trade_time, swift_flag)
                    except:
                        LOGGER.exception('Trade %s, ref %s: Failed to book return.' 
                                         % (trade.Oid(), trade_ref))
                        continue
                    LOGGER.info('Trade %s, ref %s: Return trade booked %s.' 
                                % (trade.Oid(), trade_ref, return_trade.Oid()))
                    booked_returns.append(parent)
            except:
                LOGGER.info('Failed to process %s.' % row)


def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    file_path = str(ael_params['input_file_path'])
    update_value_day = ael_params['update_value_day']
    book_returns = ael_params['book_returns']
    if update_value_day and book_returns:
        raise Exception("Please select only one option. Can't do both using the same input.")
    if update_value_day:
        run_value_day_update(file_path)
    if book_returns:
        run_return_booking(file_path)
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')
