"""----------------------------------------------------------------------------
PURPOSE                 :  Done for Day / Block trade booking tool for ACS 
                           Cash Equities Agency client trades. 
                           Right-click on instrument in portfolio view -->
                           'Book DfD blocks'.
REQUESTER               :  Ray Phillips, ACS
DEVELOPER               :  Libor Svoboda
CR NUMBER               :  CHNG0005014337
-------------------------------------------------------------------------------

HISTORY
===============================================================================
Date        Change no         Developer           Description
-------------------------------------------------------------------------------
09/11/2017  CHNG0005064599    Libor Svoboda       Added multi row support.
"""
import acm
from collections import defaultdict
from t3_alloc_logic import get_process_class, TREES
from t3_alloc_eod import generate_trades, book_acs_block


DATE_TODAY = acm.Time().DateToday()
CALENDAR = acm.FCalendar['ZAR Johannesburg']
LAST_BUSINESS_DAY = CALENDAR.AdjustBankingDays(DATE_TODAY, -1)
PARENT_PRF = 'ACS Cash Equities Agency'


def show_message_box(shell, message, dialog_type):
    acm.UX().Dialogs().MessageBox(shell, dialog_type, message, 'OK', 
                                  None, None, 'Button1', 'Button1')


def process_trades(portfolio_name, ins_name, start_date):
    ProcessClass = get_process_class(portfolio_name)
    ProcessClass.closing_types = []
    process_object = ProcessClass(portfolio_name, start_date)
    trade_items = process_object.get_trade_items(ins_name)
    trade_container = process_object.get_alloc_container(trade_items)
    block_trades = generate_trades(trade_container, book_acs_block, False)
    return block_trades


def book_dfd(eii):
    ext_obj = eii.ExtensionObject()
    shell = ext_obj.Shell()
    row_objects = ext_obj.ActiveSheet().Selection().SelectedRowObjects()
    booked_dfds = defaultdict(dict)
    for row in row_objects:
        if (not row.IsKindOf(acm.FSingleInstrumentAndTrades) and not 
                (row.IsKindOf(acm.FDistributedRow) and row.IsSingleInstrument())):
            msg = 'Only applicable to instrument level rows (row %s).' % str(row)
            show_message_box(shell, msg, 'Error')
            continue
        trades = row.Trades().AsList()
        portfolios = {trade.Portfolio().Name() for trade in trades}
        if len(portfolios) != 1:
            msg = 'Only applicable to instruments under a single portfolio (row %s).' % str(row)
            show_message_box(shell, msg, 'Error')
            continue
        portfolio_name = trades[0].Portfolio().Name()
        ins_name = trades[0].Instrument().Name()
        if not (TREES[PARENT_PRF].has(portfolio_name) and 
                portfolio_name.endswith('-TRD')):
            msg = 'Only applicable to %s portfolios ending with "-TRD" (row %s).' % (PARENT_PRF, str(row))
            show_message_box(shell, msg, 'Error')
            continue
        block_trades = process_trades(portfolio_name, ins_name, LAST_BUSINESS_DAY)
        booked_dfds[portfolio_name][ins_name] = block_trades
    
    if booked_dfds:
        msg = 'Successfully created the folowing DfD block trades:'
        for prf_name, instruments in booked_dfds.iteritems():
            for ins_name, trades in instruments.iteritems():
                trades_list = ', '.join([trade.Name() for trade in trades])
                msg += '\n\t%s, %s: %s' % (prf_name, ins_name, trades_list)
    else:
        msg = 'No DfD block trades were created.'
    print msg
    show_message_box(shell, msg, 'Information')
