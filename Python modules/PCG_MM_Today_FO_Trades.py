"""
Business require an automated script to BO confirm specific MM trades (Non Derivative) in
certain portfolios with a few validations. Exclude allocate mirror trades. Pick only all trades
with an execution time for today, i.e booked today for any given value date.

Date            Change            Developer               Requester
==========      ===========       ==================      ======================
2012-12-07      ABITFA-1846       Pavel Saparov           Haroon Mansoor
2013-04-10      ABITFA-2250       Sanele Macanda          Michael Kelleher
2015-05-06      FAU-736           Pavel Saparov           Anwar Banoo
2015-09-07      ABITFA-3469       Mike Schaefer           Natasja McAllister
2016-09-06      CHNG0003914707    Willie van der Bank     Linda Breytenbach
"""
import acm
from time import mktime
from datetime import datetime, timedelta
from auto_confirm import AutoConfirmation as AC

ael_gui_parameters = {'windowCaption': 'PCG Autoconfirm FO MM Trades'}

ael_variables = [
    ['trade_filter', 'Trade Filter',
     'FTradeSelection', None, 'PCG_MM_Today_FO_Trades', 1, 0,
     'Select your trade filter with trade population', None, 1],
    ['trade_execution', 'Trade Time Execution',
     'string', None, '-2h', 1, 0,
     'Period after which trades will not be considered', None, 1],
]

valid_instypes = (
    'CD','CD Pre Payable', 'CL Pre Payable',
    'CD Roll-up', 'CL Roll-up', 'CL', 'FDC', 'FDE',
    'FDI','FRD Pre Payable',
    'FRD Pre Payable 13M',
    'FRD Pre Payable 1M',
    'FRD Pre Payable 3M',
    'FRD Pre Payable 6M', 'FRN','LBB',
    'FTL', 'FBB', 'NCC', 'NCD',
    'NCF', 'PN', 'PRN', 'SARB Debenture',
    'SRP', 'TB'
)

def ael_main(params):
    """ Main loop """

    print "Executing {0}".format(__name__)

    td = dict(list(zip(
        ('s', 'm', 'h', 'w', 'd'),
        ('seconds', 'minutes', 'hours', 'weeks', 'days')
    )))

    delta = timedelta(**{td[params['trade_execution'][-1]]:
                         int(params['trade_execution'][:-1])})

    past = mktime((datetime.now() + delta).timetuple())

    # convert and copy from FPersistentSet to Python list
    trades = list(params['trade_filter'].Trades())

    if len(trades) == 0:
        print "No trades found in {0} to automatically BO Confirm.".format(
            params['trade_filter'].Name())
    else:
        print "%s trade(s) selected." %len(trades)

    # iterate through trade list copy and remove
    # mirror trades from the original list
    mirror_trades = []

    for trade in list(trades):
        mirror = trade.GetMirrorTrade()
        if (mirror and mirror in trades and trade not in mirror_trades):
            mirror_trades.append(mirror)
            trades.remove(mirror)
    
    for trade in trades:
        # valid statement since ``MM_Instype`` is for Bill, FRN
        # and ``Funding Instype`` for CD, Deposit
        # trade's instrument cannot have both at the same time
        
        create_time = acm.Time.DateFromTime(trade.CreateTime())
        trade_time = acm.Time.DateFromTime(trade.TradeTime())
        
        if acm.Time.FirstDayOfMonth(trade_time) != acm.Time.FirstDayOfMonth(create_time):
            print "%s was booked and backdated to the previous " \
                    "month and has not been 'BO-Confirmed'." %trade.Name()
        else:
            add_info = (trade.AdditionalInfo().MM_Instype()
                        or trade.AdditionalInfo().Funding_Instype())
            trade_execution_time = datetime.strptime(trade.ExecutionTime(), '%Y-%m-%d %H:%M:%S')
            trade_execution_time = mktime(trade_execution_time.timetuple())
            if (trade_execution_time <= past and add_info in valid_instypes and
                    not (trade.Instrument().AdditionalInfo().Demat_Instrument() and trade.AdditionalInfo().Demat_Acq_BPID() != trade.AdditionalInfo().MM_DEMAT_CP_BPID())):
                mirror = trade.GetMirrorTrade()
                # if trade is valid and has its mirror trade in not Allocate portfolio
                # update both trades in one transaction, otherwise leave them be
                if mirror and (mirror.Portfolio().Name().startswith('Allocate')):
                    print "Skipping BO confirmation for trade {0} - mirror " \
                            "portfolio name starts with 'Allocate'.".format(trade.Oid())
                    continue
                elif mirror and (mirror.AdditionalInfo().Funding_Instype()
                    not in valid_instypes):
                    print "Skipping BO confirmation for trade {0} " \
                            "- the addinfo 'Funding Instype' is " \
                            "invalid ({1}).".format(trade.Oid(),
                            mirror.AdditionalInfo().Funding_Instype())
                    continue
                else:
                    try:
                        # FIXME FValidation does not prevent Voided/Simulated/Terminated
                        #       trades from being BO Confirmed.
                        if trade.Status() != "FO Confirmed":
                            print "Trade {0} has the status {1}. Nothing done.".format(trade.Oid(),
                                    trade.Status())
                        else:
                            # FIXME Remove once Prime >= 2015.4 is deployed
                            #In version 2014.4.8 there is a problem with BO Confirmation of mirror trades
                            #(the one with lower trade number), doing so it produces a Runtime exception.
                            #The function 'hotfix_confirm_trade' is automatically changing the status of a
                            #trade with higher trade number.
                            AC.hotfix_confirm_trade(trade, "BO Confirmed")
                            print "Trade {0} was automatically BO Confirmed".format(trade.Oid())
                    except Exception as e:
                        trade.Undo()
                        print "Unable to BO Confirm trade {0}".format(trade.Oid())
                        print " Reason: {0}".format(e)
            else:
                print "Skipping BO confirmation for trade %s." \
                      " Execution Time: %s." \
                      " Additional Info: %s." %(trade.Oid(), \
                        acm.Time.DateFromTime(trade.ExecutionTime()), add_info)

    print "Completed successfully"
