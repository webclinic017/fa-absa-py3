"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    OperationsSTPFunctions

DESCRIPTION
    This module contains general functionality related to operations STP (straight-
    through-processing).

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-04-08      FAOPS-448       Hugo Decloedt           Kgomotso Gumbo          Initial implementation.
                                Cuen Edwards
                                Stuart Wilson
2019-04-12      FAOPS-483       Cuen Edwards            Kgomotso Gumbo          Addition of confirmation matching.
2019-05-13      FAOPS-308       Joash Moodley           Kgomotso Gumbo          Addition of settlement netting.
2019-05-27      FAOPS-488       Tawanda Mukhalela       Kgomotso Gumbo          Addition of MT5xx Auto acknowledge
2020-02-06      PCGDEV-298      Tawanda Mukhalela       Gasant Thulsie          Addition of SBL Authorise Function
2020-10-06      PCGDEV-594      Qaqamba Ntshobane       Daveshin Chetty         Exposed addinfo update function for 
                                                                                use outside module
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger


LOGGER = getLogger(__name__)


def bo_confirm_trade(trade):
    """
    Change the status of a trade to BO Confirmed.
    """
    LOGGER.info('BO Confirming trade {trade_oid}.'.format(
        trade_oid=trade.Oid()
    ))
    trade = trade.StorageImage()
    trade.Status('BO Confirmed')
    trade.Commit()


def match_confirmation(confirmation):
    """
    Change the status of a confirmation to Matched.
    """
    LOGGER.info('Matching confirmation {confirmation_oid}.'.format(
        confirmation_oid=confirmation.Oid()
    ))
    confirmation = confirmation.StorageImage()
    confirmation.Status('Matched')
    confirmation.Commit()


def release_settlement(settlement):
    """
    Change the status of a settlement to released.
    """
    LOGGER.info('Releasing settlement {settlement_oid}.'.format(
        settlement_oid=settlement.Oid()
    ))
    settlement = settlement.StorageImage()
    # Set Call_Confirmation AddInfo.
    call_confirmation_value = _get_settlement_call_confirmation_value(settlement)
    set_additional_info_value(settlement, 'Call_Confirmation', call_confirmation_value)
    # Set Authorise Debit AddInfo.
    if is_incoming_settlement(settlement):
        set_additional_info_value(settlement, 'Authorise Debit', 'Yes')
    settlement.Status('Released')
    settlement.Commit()


def hold_settlement(settlement):
    """
    Change the status of a settlement to hold.
    """
    LOGGER.info('Holding settlement {settlement_oid}.'.format(
        settlement_oid=settlement.Oid()
    ))
    settlement = settlement.StorageImage()
    settlement.Status('Hold')
    settlement.Commit()


def authorise_settlement(settlement):
    """
    Change Settlement status to Authorised
    """
    LOGGER.info('Authorised settlement {settlement_oid}.'.format(
        settlement_oid=settlement.Oid()
    ))
    settlement = settlement.StorageImage()
    settlement.Status('Authorised')
    settlement.Commit()


def is_incoming_settlement(settlement):
    """
    Determines whether or not a specified settlement represents an
    incoming settlement.
    """
    return settlement.Amount() > 0


def is_outgoing_settlement(settlement):
    """
    Determines whether or not a specified settlement represents an
    outgoing settlement.
    """
    return settlement.Amount() < 0


def _get_settlement_call_confirmation_value(settlement):
    """
    Get the Call_Confirmation additional info value to populate
    for a settlement.
    """
    call_confirmation_value = 'AutoRelease'
    demat_sett = settlement.Trade().Instrument().AdditionalInfo().Demat_Instrument()
    if demat_sett and settlement.CashFlow():
        demat_ce_ref = settlement.CashFlow().AdditionalInfo().Demat_CE_Reference()
        if demat_ce_ref:
            call_confirmation_value = "{0}CEM{1}".format(demat_ce_ref[:4], demat_ce_ref[4:])
    return call_confirmation_value


def set_additional_info_value(entity, additional_info_field, additional_info_value):
    """
    Set an entity additional info value.
    """
    LOGGER.info("Setting additional info '{field}' to '{value}'.".format(
        field=additional_info_field,
        value=additional_info_value
    ))
    entity.AddInfoValue(additional_info_field, additional_info_value)


def acknowledge_settlement(settlement):
    """
    Change the status of a settlement to Acknowledged
    """
    LOGGER.info('Acknowledging settlement {settlement_oid}.'.format(
        settlement_oid=settlement.Oid()
    ))
    settlement = settlement.StorageImage()
    settlement.Status('Acknowledged')
    settlement.Commit()


def _create_net_parent_settlement(settlements):
    """
    Create new parent for netted settlement.
    """
    LOGGER.info('creating new parent settlement')
    settlement = settlements[0]
    new_settlement = acm.FSettlement()
    new_settlement.Status('New')
    new_settlement.RelationType('Ad Hoc Net')
    new_settlement.Type('None')
    new_settlement.ToPortfolio(settlement.ToPortfolio())
    new_settlement.FromPortfolio(settlement.FromPortfolio())
    new_settlement.Currency(settlement.Currency())
    new_settlement.Acquirer(settlement.Acquirer())
    new_settlement.AcquirerName(settlement.AcquirerName())
    new_settlement.AcquirerAccountRef(settlement.AcquirerAccountRef())
    new_settlement.Counterparty(settlement.Counterparty())
    new_settlement.CounterpartyName(settlement.CounterpartyName())
    new_settlement.CounterpartyAccountRef(settlement.CounterpartyAccountRef())
    new_settlement.Trade(settlement.Trade())
    new_settlement.Protection(settlement.Protection())
    new_settlement.Owner(settlement.Owner())
    new_settlement.ValueDay(settlement.ValueDay())
    new_settlement.Status(settlement.Status())
    amount = 0
    new_settlement.Amount(amount)
    new_settlement.Commit()
    return new_settlement


def net_settlements(settlements):
    """
    This function nets settlements and returns a 
    new parent with the netted settlements attached. 
    """
    parent = _create_net_parent_settlement(settlements)
    amount = parent.Amount()
    for settlement in settlements:
        LOGGER.info(
            'add settlement {sett_id} to be netted'.format(
            sett_id=settlement.Oid())
        )
        settlement = settlement.StorageImage()
        if settlement.Status() != 'Void':
            settlement.Status('Void')
        amount = amount + settlement.Amount()
        settlement.Parent(parent)
        settlement.Commit()
    parent.Amount(amount)
    parent.Commit()
    LOGGER.info(
        'new parent settlement {parent_id} created'.format(
        parent_id=parent.Oid())
    )
    return parent


def void_trade(trade):
    """
    Function to change trade status to Void
    """
    LOGGER.info('Voiding Trade {trade_oid}.'.format(
        trade_oid=trade.Oid()
    ))
    trade = trade.StorageImage()
    trade.Status('Void')
    trade.Commit()
