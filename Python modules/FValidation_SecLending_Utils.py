"""Utilities for security lending.

History
=======

2015-02-04 Vojtech Sidorin  Initial implementation. Move util functions from FValidation_SecLending.
2020-02-20 Bhavnisha Sarawan Added SBL collateral group as part of GlobalOne Decom
2020-03-18 Sihle Gaxa        Removed check_entity_amendments method and unused constants 
                             as new access no longer uses it as part of GlobalOne decom
2020-12-08 Qaqamba Ntshobane Added exception handling for sl_quantity in should_not_create_sasol_trade
2020-12-11 Sihle Gaxa        PCGDEV-622: Added Front office group to facilitate trade direction validation
2021-02-19 Sihle Gaxa        PCGDEV-663: Added collateral original trade ID in text2 logic
"""

import ael
import acm
from FValidation_core import AccessValidationError


def user_belongs_to_SBL_operations():
    """Returns True if the user belongs to
    user group OPS SecLend"""
    sbl_ops_grpid = 'OPS SecLend'
    current_user = ael.user()
    if current_user.grpnbr.grpid == sbl_ops_grpid:
        return True
        
def user_belongs_to_Collateral_operations():
    """Returns True if the user belongs to
    user group PCG Collateral"""
    sbl_ops_grpid = 'PCG Collateral'
    current_user = ael.user()
    if current_user.grpnbr.grpid == sbl_ops_grpid:
        return True

def user_belongs_to_SBL_front_office():
    """Returns True if the user belongs to
    user group FO PSSecLend Trader"""
    sbl_fo_grpid = 'FO PSSecLend Trader'
    current_user = ael.user()
    if current_user.grpnbr.grpid == sbl_fo_grpid:
        return True

def trade_lender_not_allowed(trade):
    """"Returns True if a trade is booked in
    ACS - Script Lending portfolio and its lender
    is not set to SLL ACS Lender"""
    if trade.prfnbr.prfid == 'ACS - Script Lending':
        lender = trade.add_info('SL_G1Counterparty2')
        if lender and lender != 'SLL ACS LENDER':
            return True
    return False


def is_return(trade):

    return acm.FTrade[trade.trdnbr].Text1() in ["PARTIAL_RETURN", "FULL_RETURN"]


def should_not_create_sasol_trade(trade):

    trade = acm.FTrade[trade.trdnbr]
    client_name = trade.Counterparty().Name()
    underlying_ins = trade.Instrument().Underlying().Name()
    instrument = "{}/SELO/{}/Avail_Holdings_Trade".format(underlying_ins[:3], underlying_ins[4:])
    instrument = acm.FInstrument[instrument]

    if 'SLL SASOL PENSION FUND' in [trade.add_info("SL_G1Counterparty2"), client_name]:
        available_quantity = acm.GetCalculatedValue(instrument, acm.GetDefaultContext(), 'slAvailableQuantity').Value()
        trade_position = acm.GetCalculatedValue(trade, acm.GetDefaultContext(), 'sl_quantity')

        if trade_position:
            trade_position = trade_position.Value()
        else:
            trade_position = trade.Quantity()

        return (available_quantity < 0 or trade_position > available_quantity)


def get_instrument(entity):
    modified_entity = entity
    if modified_entity.record_type in ["Trade", "Leg"]:
        modified_entity = entity.insaddr
    elif modified_entity.record_type == "CashFlow":
        modified_entity = entity.legnbr.insaddr
    return modified_entity


def get_counterparty_type(lender_name, borrower_name):
    lender = acm.FParty[lender_name]
    borrower = acm.FParty[borrower_name]
    counterparty_list =  acm.FChoiceList[6326].Choices() # SBL_Principal_Accounts
    excluded_counterparties = [counterparty.Name() for counterparty in counterparty_list]
    if borrower and lender_name in excluded_counterparties and \
            borrower.add_info("SL_CptyType").upper() == "BORROWER":
        return "Borrower"
    elif lender and borrower_name in excluded_counterparties and \
            lender.add_info("SL_CptyType").upper() == "LENDER":
        return "Lender"
    message = ("This is not a valid SBL loan, please check your counterparties")
    raise AccessValidationError(message)


def get_trade_counterparties(entity):
    """
    Retrieves the lender and borrower counterparty names from GlobalOne add infos on the trade
    """
    lender = None
    borrower = None
    lender_addinfo = ael.AdditionalInfoSpec['SL_G1Counterparty2']
    borrower_addinfo = ael.AdditionalInfoSpec['SL_G1Counterparty1']
    for add_info in entity.additional_infos():
        if add_info.addinf_specnbr.specnbr == lender_addinfo.specnbr:
            lender = add_info.value
        if add_info.addinf_specnbr.specnbr == borrower_addinfo.specnbr:
            borrower = add_info.value
    return lender, borrower


def check_if_trade_direction_correct(entity, operation):
    """Rule 120f: Security loan trades booked or amended in portfolio SBL Agency
    against a lender counterparty then the trade must be a buy.
    If the counterparty is a borrower then the trade direction must be a sell.
    Anything booked in any other portfolio must follow the inverse of the above rules."""
    if entity.record_type == "Trade":
        if entity.insaddr.instype != 'SecurityLoan':
            return
        lender, borrower = get_trade_counterparties(entity)
        if lender and borrower:
            is_incorrect_direction(entity, lender, borrower)
            return
    else:
        modified_entity = get_instrument(entity)
        if modified_entity.instype != 'SecurityLoan':
            return
        instrument_trades = modified_entity.trades().members()
        if instrument_trades:
            for instrument_trade in instrument_trades:
                lender, borrower = get_trade_counterparties(entity)
                if lender and borrower:
                    is_incorrect_direction(trade, lender, borrower)


def is_incorrect_direction(entity, lender, borrower):
    trade_portfolio = entity.prfnbr
    trade_acquirer = entity.acquirer_ptynbr.ptynbr
    message = "FV120f: Trade booked in wrong direction"
    trade_direction = "Sell" if entity.quantity < 0 else "Buy"
    if trade_portfolio.prfnbr == 2799 or trade_acquirer != 32668:  # SBL_Accrued_1, SECURITY LENDINGS DESK
        return
    counterparty_type = get_counterparty_type(lender, borrower)
    if trade_portfolio.prfnbr == 3186:  # SBL Agency
        if counterparty_type == "Borrower" and trade_direction == "Buy":
            raise AccessValidationError(message)
        elif counterparty_type == "Lender" and trade_direction == "Sell":
            raise AccessValidationError(message)
    else:
        if counterparty_type == "Borrower" and trade_direction == "Sell":
            raise AccessValidationError(message)
        elif counterparty_type == "Lender" and trade_direction == "Buy":
            raise AccessValidationError(message)
