"""
    AMWI_ValGroup

    This is based on CSA_ValGroups but has been converted to use acm.
"""

import acm

from AMWICommon import log_error
from AMWICustomUtil import log_debug


def find_val_group(val_group_name):
    choice_list_item = acm.FChoiceList[val_group_name]
    if choice_list_item and choice_list_item.List() == "ValGroup":
        return choice_list_item

    return None


def has_parent_portfolio(portfolio, parent_name):
    if portfolio.Name() == parent_name:
        return True

    link = acm.FPortfolioLink.Select01("memberPortfolio=%i" % portfolio.Oid(),
                                       "More than one parent portfolio for portfolio: %s" % portfolio.Name())

    if link:
        parent = link.OwnerPortfolio()
        if parent:
            return has_parent_portfolio(parent, parent_name)

    return False


def get_csa_counterparty_val_group(trade):
    counterparty = trade.Counterparty()
    if not counterparty:
        log_error("[ValGroup] Counterparty not set.")
        return None

    csa = counterparty.AdditionalInfo().CSA()
    csa_ccy = counterparty.AdditionalInfo().CSA_Collateral_Curr()
    csa_type = counterparty.AdditionalInfo().CSA_Type()
    csa_switch_date = counterparty.AdditionalInfo().CSA_Switch_Date()

    if csa_switch_date:
        if csa_switch_date <= acm.Time().AsDate(trade.TradeTime()):
            csa_ccy = counterparty.AdditionalInfo().CSA_CollateralCurr2()

    if (csa != "Yes" and str(csa) != "True") or csa_type not in ["Gold", "Strong"]:
        if trade.Instrument().InsType() in ['Swap', 'FRA', 'IndexLinkedSwap']:
            return "AC_GLOBAL"
        elif trade.Instrument().InsType() == 'CurrSwap':
            return "AC_GLOBAL_Basis"
    elif csa_type in ["Gold", "Strong"]:
        if trade.Instrument().InsType() == "CurrSwap":
            return "AC_OIS_%s_XCCY" % csa_ccy
        else:
            return "AC_OIS_%s" % csa_ccy

    return None


def get_clearing_trade_val_group(trade):
    ccy = trade.Instrument().Currency().Name()
    if ccy == "EUR":
        return "AC_ESTR_LCH_EUR"
    elif ccy == "USD":
        return "AC_SOFR_LCH_USD"
    else:
        return "AC_OIS_%s" % ccy


def get_csa_val_group(trade, is_clearing):
    if is_clearing:
        return get_clearing_trade_val_group(trade)
    elif trade.Counterparty() and trade.Counterparty().Name() == "PRIME SERVICES DESK":
        log_debug("[ValGroup] Counterparty is 'PRIME SERVICES DESK'. No val group set.")
        return None
    else:
        return get_csa_counterparty_val_group(trade)
