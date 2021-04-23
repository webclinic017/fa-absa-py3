import acm
from logging import getLogger
from at_ael_variables import AelVariableHandler

"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    BO-BO_Confirm_trades
DESCRIPTION
    This module contains a script that changes DIS_Instruments from 'BO-Confirm' to 'BO-BO Confirm' status
-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2021-01-29      FAOPS-970       Robello Munzhedzi       Wandile Sithole         Auto BO-BO_Confirm 'DIS' trades
-----------------------------------------------------------------------------------------------------------------------------------------
"""


LOGGER = getLogger(__name__)


COUNTERPARTY_DICT = dict()
COUNTERPARTY_DICT[1940] = 'EXXARO COAL MPUMALANGA PTY LTD'
COUNTERPARTY_DICT[4590] = 'ZZZ DO NOT USE SUPER GROUP TRADING'
COUNTERPARTY_DICT[10244] = 'ZZZ DO NOT USE ARMSCOR'
COUNTERPARTY_DICT[14591] = 'ZZZ DO NOT TRADE STANDARD CHARTERED LON'
COUNTERPARTY_DICT[19434] = 'ZZZ DO NOT USE NBC FUTURE GUARD PTY LTD'
COUNTERPARTY_DICT[26442] = 'ZZZ DO NOT USE IAM ISMONM'
COUNTERPARTY_DICT[27617] = 'ZZZ DO NOT USE AUTUMN STORM INVESTMEMEN'
COUNTERPARTY_DICT[29004] = 'ZZZ DO NOT USE FIRST RAND BANK'
COUNTERPARTY_DICT[25935] = 'ZZZ DO NOT USE CORONATION AM FORRUT'


def set_not_trading_flag(client_list, not_trading_flag):
    for c_key in client_list.keys():
        try:
            party = acm.FParty[client_list[c_key]]
            if party:
                party.NotTrading = not_trading_flag
                party.Commit()
        except Exception:
            LOGGER.exception("Failed to commit {}".format(c_key.Id()))


def change_trade_status(acm_trade, status='BO-BO Confirmed'):
    trade_image = acm_trade.StorageImage()
    trade_image.Status(status)
    trade_image.Commit()
    LOGGER.info("Successfully updated trade status for trade {} to {}".format(acm_trade.Name(), status))


def bo_bo_confirm_trade(acm_trade, simulate_mode=True):
    if acm_trade.Status() == 'BO-BO Confirmed':
        return
    acm.BeginTransaction()
    try:
        change_trade_status(acm_trade)
        if acm_trade.GetMirrorTrade():
            mirror_trade = acm_trade.GetMirrorTrade()
            change_trade_status(mirror_trade)
            if mirror_trade.ConnectedTrade():
                connected_mirror_trade = acm_trade.ConnectedTrade()
                change_trade_status(connected_mirror_trade)
        if acm_trade.ConnectedTrade():
            connected_trade = acm_trade.ConnectedTrade()
            change_trade_status(connected_trade)
        if not simulate_mode:
            acm.CommitTransaction()
        else:
            acm.AbortTransaction()
    except Exception:
        acm.AbortTransaction()
        LOGGER.exception("Failed to change status for trade {}".format(acm_trade.Name()))


def _is_qualifying_trade(trade):
    check_approx_load = trade.AdditionalInfo()
    if trade.Status() != 'BO Confirmed':
        return False
    if trade.Aggregate() or trade.ArchiveStatus():
        return False
    if not trade.Instrument().AdditionalInfo().DIS_Instrument():
        return False
    if trade.Instrument().SettleCategoryChlItem().Name() != 'DIS':
        return False
    if check_approx_load.Approx_46_load() not in [None, True]:
        return False
    if trade.Counterparty().Oid() == 25935:
        return False
    return True


def _is_qualifying_general_trade(trade):
    if trade.Acquirer() == trade.Counterparty():
        return False
    if trade.YourRef() is None:
        return False
    return _is_qualifying_trade(trade)


def get_portfolio_trades(portfolios):
    trade_list = list()
    for portfolio in portfolios:
        trade_list.extend(list(filter(_is_qualifying_general_trade, portfolio.Trades())))
    return trade_list


def get_dis_trades():
    instrument_selection = acm.FInstrument.Select('settleCategoryChlItem = "DIS"')
    trade_list = list()
    for instrument in instrument_selection:
        if instrument.AdditionalInfo().DIS_Instrument():
            trade_list.extend(list(filter(_is_qualifying_trade, instrument.Trades())))
    return trade_list


ael_variables = AelVariableHandler()


ael_variables.add_bool(
    "dis_trades",
    label="Process DIS trades",
    default=True,
    cls="boolean",
    mandatory=True,
    alt="Include DIS trades to the list of trades to BO-BO Confirmed."
)
ael_variables.add(
    "portfolios",
    label="Portfolio(s)",
    default=",".join(('CFD', 'Equity Script Lending', '4440798', '4440806')),
    cls=acm.FPhysicalPortfolio,
    mandatory=True,
    multiple=True,
    alt="Include trades in the select Portfolios to the list of trades to BO-BO Confirmed."
)
ael_variables.add_bool(
    "simulate_mode",
    label="Simulate Mode",
    default=True,
    cls="boolean",
    mandatory=True,
    alt="Simulate BO-BO Confirming of Trades."
)


def ael_main(parameter_dict):
    set_not_trading_flag(COUNTERPARTY_DICT, 0)

    full_trade_list = list()
    if parameter_dict['portfolios']:
        full_trade_list.extend(get_portfolio_trades(parameter_dict['portfolios']))
    LOGGER.info("Processing {} Trades.".format(str(len(full_trade_list))))
    if parameter_dict['dis_trades'] is True:
        full_trade_list.extend(get_dis_trades())
    LOGGER.info("Processing {} Trades.".format(str(len(full_trade_list))))
    simulate_mode = parameter_dict['simulate_mode']
    if simulate_mode:
        LOGGER.info("Code Running is SIMULATE Mode.\n")
    for trade in full_trade_list:
        bo_bo_confirm_trade(trade, simulate_mode=simulate_mode)
    LOGGER.info("Finished Processing the All Trades\n")
    set_not_trading_flag(COUNTERPARTY_DICT, 1)
