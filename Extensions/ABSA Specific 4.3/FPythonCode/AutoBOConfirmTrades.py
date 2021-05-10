"""
Business require an automated script to BO confirm specific trades in
certain portfolios with a few validations. Exclude allocate mirror trades. Pick only all trades
with an execution time for today, i.e booked today for any given value date.

Date            Change            Developer               Requester
==========      ===========       ==================      ======================
2019-05-01      FAOPS-456         Hugo                    Imraan Hendrix

"""

# pylint: disable=import-error
import acm
import FLogger

from auto_confirm import AutoConfirmation as AC
from at_ael_variables import AelVariableHandler


TRADE_FILTER = 'EQ Trades To Auto BO Confirm'
VALID_INSTRUMENT_TYPES = ('Stock', 'ETF')
logger = FLogger.FLogger()


# RunScriptCMD parameters
ael_gui_parameters = {'windowCaption': 'Equity Desk Auto Confirm Trades'}

ael_variables = AelVariableHandler()
ael_variables.add(
    'trade_filter',
    label='Trade Filter',
    cls='FTradeSelection',
    default='EQ Trades To Auto BO Confirm',
    mandatory=True,
    multiple=False,
    alt='Select your trade filter with trade population'
)

# End of RunScriptCMD


def ael_main(params):
    """
    Main entry point for RunScriptCMD.
    :param params: FDictionary
    """
    mirror_trades = []

    logger.info("Executing {0}".format(__name__))

    # Convert and copy from FPersistentSet to Python list
    trades = list(params['trade_filter'].Trades())

    if trades:
        logger.info("{0} trade(s) selected.".format(trades))
    else:
        logger.info("No trades found in {0} to automatically BO Confirm.".format(params['trade_filter'].Name()))

    # Iterate through trade list copy and remove mirror trades from the original list
    for trade in list(trades):
        mirror = trade.GetMirrorTrade()
        if mirror and mirror in trades and trade not in mirror_trades:
            mirror_trades.append(mirror)
            trades.remove(mirror)

    for trade in trades:
        create_time = acm.Time.DateFromTime(trade.CreateTime())
        trade_time = acm.Time.DateFromTime(trade.TradeTime())

        if acm.Time.FirstDayOfMonth(trade_time) != acm.Time.FirstDayOfMonth(create_time):
            logger.info("{0} was booked and backdated to the previous month and has not been 'BO-Confirmed'.".format(
                        trade.Name()))
        elif trade.Instrument().InsType() in VALID_INSTRUMENT_TYPES:
            mirror = trade.GetMirrorTrade()
            # if trade is valid and has its mirror trade in not Allocate portfolio
            # update both trades in one transaction, otherwise leave them be
            if mirror and (mirror.Portfolio().Name().startswith('Allocate')):
                logger.info("Skipping BO confirmation for trade {0} - mirror "
                            "portfolio name starts with 'Allocate'.".format(trade.Oid()))
                continue
            else:
                _BoConfirm(trade)
        else:
            logger.info('Skipping BO confirmation for trade {0}. Execution Time: {1}.'.format(
                trade.Oid(), acm.Time.DateFromTime(trade.ExecutionTime())))

        logger.info("Completed successfully")


def _BoConfirm(trade):
    """
    BO Confirm trade.
    :param trade: FTrade
    """
    try:
        if trade.Status() != "FO Confirmed":
            logger.info("Trade {0} has the status {1}. Nothing done.".format(trade.Oid(), trade.Status()))
        else:
            AC.hotfix_confirm_trade(trade, "BO Confirmed")
            logger.info("Trade {0} was automatically BO Confirmed".format(trade.Oid()))
    except Exception as exception:  # pylint: disable=import-error
        trade.Undo()
        logger.info("Unable to BO Confirm trade {0}".format(trade.Oid()))
        logger.info("Reason: {0}".format(exception))
