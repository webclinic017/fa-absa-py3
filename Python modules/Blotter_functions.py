"""--------------------------------------------------------------------------
MODULE
   Blotter_functions

DESCRIPTION
    This module houses the functions that are used in the ASUS Equity Blotter sql function

HISTORY
Date: 2020-11-09
Author: Snowy Mabilu
Jira : ARR-72 - Equity blotter for 15a6 US counterparties

-----------------------------------------------------------------------------"""
import acm, ael
import ASUSNewTradeConfirmationGeneral

context = acm.GetDefaultContext()
calc_space = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')


def get_commission(ael_trade, *rest):
    try:
        trade = acm.Ael.AelToFObject(ael_trade)
        return ASUSNewTradeConfirmationGeneral.get_commission_amount(trade)
    except:
        pass


def get_original_counterparty(ael_trade, *rest):
    trade = acm.Ael.AelToFObject(ael_trade)
    original_party = ASUSNewTradeConfirmationGeneral.get_counterparty_for_trade(trade)
    if original_party:
        return original_party.Name()
    return trade.Counterparty().Name()


def is_valid_asus_trade(ael_trade, *rest):
    trade = acm.Ael.AelToFObject(ael_trade)
    party_name = get_original_counterparty(ael_trade)
    counterparty = acm.FParty[party_name]
    isvalid = ASUSNewTradeConfirmationGeneral.has_been_processed(
        trade) and counterparty.LegalForm().Name() == "15a6 US client"
    return str(isvalid)


def consideration_amount(ael_trade, *rest):
    trade = acm.Ael.AelToFObject(ael_trade)
    commission = get_commission(ael_trade)
    consideration = abs(trade.Premium()) + commission if trade.Bought() else abs(trade.Premium()) - commission
    return consideration


def get_usd_consideration(ael_trade, *rest):
    trade = acm.Ael.AelToFObject(ael_trade)
    spot_price = ASUSNewTradeConfirmationGeneral.get_current_usd_pot_price(acm.FInstrument['USD'],
                                                                           trade.Currency())
    consideration = consideration_amount(ael_trade)
    usd_consideration = consideration / spot_price
    return usd_consideration


def get_usd_premium(ael_trade, *rest):
    trade = acm.Ael.AelToFObject(ael_trade)
    return calc_space.CalculateValue(trade, 'PremiumUSD').Number()



