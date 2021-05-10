"""Validation rules related to Security Loans.

History
=======

2014-01-22 Nada Jasikova        Rule 120 - SBL operations team can only create and update trades
                                if it is related to capturing a partial return
                                Apart from this, the SBL operations users' profile is non-trading
                                - i.e. the validation rule blocks other security loans to be created
                                and updated.
                                The operation has to comply with the following conditions:
                                    - the instrument type is SecurityLoan
                                    - if the trade is booked in portfolio ACS   Script Lending,
                                    the Fund/Lender has to be SLL ACS Lender
                                    - the new trade was created using the Partial Return functionality
                                    on the trade ticket
                                    - the trade being updated has been modified using the Partial Return
                                    functionality on the trade ticket
2015-02-04      Vojtech Sidorin         ABITFA-3354:    Move util functions to FValidation_SecLending_Utils.
2015-08-20      Vojtech Sidorin         ABITFA-3743:    Include rule numbers in messages.
2019-10-21      Bhavnisha Saraawan                      Global 1 decomm project: Remove restrictions for which fields can be updated.
2020-07-24      Sihle Gaxa              PCGDEV-539      Updated Insert function to prohibit SBL team from booking new loans
2020-08-11      Sihle Gaxa              PCGDEV-551      Update to allow SBL team to book simulated loans for lender holdings
2020-10-27      Faize Adams             FAOPS-878       Enable booking for non-cash collateral on all underlying instruments.
2020-12-11      Sihle Gaxa              PCGDEV-622      FV120f - Added trade direction validation rule
2020-12-17      Sihle Gaxa              PCGDEV-636      Added Namibian principal accounts to FV120f
2021-02-19      Sihle Gaxa              PCGDEV-663      Added collateral original trade ID in text2 logic to FV120g
"""
import acm
import ael
from FValidation_core import (validate_entity,
                              AccessValidationError)
from FValidation_SecLending_Utils import (user_belongs_to_SBL_operations,
                                          trade_lender_not_allowed,
                                          user_belongs_to_SBL_front_office,
                                          user_belongs_to_Collateral_operations,
                                          should_not_create_sasol_trade,
                                          is_return,
                                          get_instrument, check_if_trade_direction_correct)


@validate_entity("Trade", "Insert", caller="validate_transaction")
def check_if_sbl_trade_insert_allowed(entity, operation):
    """ Rule 120a: New trade can only be created by SBL Ops users
    if it is related to the partial return process

    (a): The function checks for the connected_trdnbr which cannot be
    modified in UI and is always entered for the SecLoans related
    to partial returns"""
    if entity.insaddr.instype != 'SecurityLoan':
        return
    if user_belongs_to_SBL_front_office() or user_belongs_to_SBL_operations():
        check_if_trade_direction_correct(entity, operation)
    if not user_belongs_to_SBL_operations():
        return
    # connected_trdnbr is not editable in UI and is always available with new
    # Security Loans created by the Partial Return script
    message = ('FV120a: New trade is not a part of the partial return '
               'process. Operation not allowed.')
    if not entity.contract_trdnbr and not (entity.text1 in ["PARTIAL_RETURN", "FULL_RETURN"]):
        raise AccessValidationError(message, popup=False)
    if entity.contract_trdnbr:
        if entity.contract_trdnbr == entity.trdnbr and not (entity.text1 in ["PARTIAL_RETURN", "FULL_RETURN"]):
            raise AccessValidationError(message, popup=False)


@validate_entity("Leg", "Update", caller="validate_transaction")
@validate_entity("Trade", "Update", caller="validate_transaction")
@validate_entity("CashFlow", "Insert", caller="validate_transaction")
@validate_entity("CashFlow", "Update", caller="validate_transaction")
@validate_entity("Instrument", "Update", caller="validate_transaction")
def check_if_trade_lender_allowed(entity, operation):
    """ Rule 120b: Trade booked in ACS Script Lending portfolio can
    only be updated by SBL OPS users if lender is SLL ACS LENDER

    (b): The function checks for the trade portfolio and returns True
    only if SLL ACS LENDER is set"""
    if user_belongs_to_SBL_front_office() or user_belongs_to_SBL_operations():
        check_if_trade_direction_correct(entity, operation)
    if not user_belongs_to_SBL_operations():
        return
    modified_entity = get_instrument(entity)
    if modified_entity.instype != 'SecurityLoan':
        return
    ins_trades = modified_entity.trades().members()
    if ins_trades:
        for trade in ins_trades:
            if trade_lender_not_allowed(trade):
                message = ('FV120b: Trade in portfolio ACS - Script Lending '
                           'does not have SLL ACS Lender. Operation not allowed.')
                raise AccessValidationError(message)


@validate_entity("Leg", "Update")
@validate_entity("Trade", "Update")
@validate_entity("Instrument", "Update")
def check_if_sbl_update_allowed(entity, operation):
    """ Rule 120c: Leg can only be updated by SBL Ops users
    if it is related to the partial return process

    (c): The function ensures the SBL team does not update anything on new loan
         legs for instruments that have trades that are in FO Confirmed status"""
    if not user_belongs_to_SBL_operations():
        return
    modified_entity = get_instrument(entity)
    if modified_entity.instype != "SecurityLoan":
        return
    ins_trades = modified_entity.trades().members()
    if ins_trades:
        for trade in ins_trades:
            if trade.status == "Simulated" and trade.prfnbr.prfid == "Lender_Availability":
                return
            if trade.connected_trdnbr:
                if trade.connected_trdnbr.trdnbr == trade.trdnbr and trade.status in ["FO Confirmed", "Simulated"]:
                    message = ("FV120c:Cannot amend a new security loan leg if it is in Simulated or FO Confirmed status.\
                                Operation not allowed.")
                    raise AccessValidationError(message, popup=False)


@validate_entity("Trade", "Insert")
@validate_entity("Trade", "Update")
def check_if_coll_trade_insert_allowed(entity, operation):
    """ Rule 120d: New trade can only be created by PCG Collateral users
    if it is a Colalteral trade and only mandated instrument types."""
    if user_belongs_to_Collateral_operations():
        if entity.category != "Collateral":
            message = ("FV120e: PTS/PCG Collateral team is only allowed to book Collaterals.")
            raise AccessValidationError(message)


@validate_entity("Trade", "Insert", caller="validate_transaction")
@validate_entity("Trade", "Update", caller="validate_transaction")
def check_if_sasol_trade_insert_allowed(entity, operation):
    """ 
    """
    if (entity.insaddr.instype != "SecurityLoan" or is_return(entity) or
      (operation == "Update" and entity.status in ["Void", "BO Confirmed", "BO-BO Confirmed"])):
        return
    if should_not_create_sasol_trade(entity):
        message = ("Available quantity exceeded. You cannot book this trade.")
        raise AccessValidationError(message)


@validate_entity("Trade", "Update", caller="validate_transaction")
def check_if_parent_id_populated(entity, operation):
    if user_belongs_to_Collateral_operations():
        if entity.category == "Collateral" and operation == "Insert" and entity.text2:
            if int(entity.text2.replace(",", "")) != entity.trdnbr:
                message = "FV120g: Please add original trade number in text2 field"
                raise AccessValidationError(message)
        else:
            original_entity = entity.original()
            if entity.text2 and original_entity and original_entity.text2:
                new_parent_id = int(entity.text2.replace(",", ""))
                original_parent_id = int(original_entity.text2.replace(",", ""))
                if new_parent_id != original_parent_id and original_parent_id > 0:
                    if entity.trdnbr == new_parent_id:
                        return
                    if not entity.text1 and entity.contract_trdnbr != entity.trdnbr and \
                        entity.contract_trdnbr == original_parent_id and \
                        (not entity.optkey1_chlnbr or entity.opt.key1_chlnbr.entry != "Collateral balance trade"):
                        return
                    message = "FV120g: You do not have permission to update original id in Text2"
                    raise AccessValidationError(message)
            elif not entity.text2 and original_entity.status == "Simulated":
                message = "FV120g: Please add original trade number in text2 field"
                raise AccessValidationError(message)
