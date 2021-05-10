"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    NetPaymentsforGrouper.

DESCRIPTION
    This module contains a functions that nets payments on a counterparty group level.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-01-28      FAOPS-905       Metse Moshobane         Gasant Thulsie          Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""
import acm

from logging import getLogger

LOGGER = getLogger(__name__)

def net_payments_for_grouper(eii):
    """
    Function used for netting payments according to the party selected from the
    'Net Payments' FMenuExtension.
    """
    if eii.ExtensionObject().ActiveSheet().Selection().SelectedCells()[0].RowObject().Settlements():
        settlements = list(
            eii.ExtensionObject().ActiveSheet().Selection().SelectedCells()[0].RowObject().Settlements())
    else:
        LOGGER.info("The grouper selected has no setlements")
        return

    qualifying_settlements = []
    net_amount = 0
    first_settlement = settlements[0]
    for settlement in settlements:
        if check_qualifying_settlements_for_netting(first_settlement, settlement):
            qualifying_settlements.append(settlement)

    for settlement in qualifying_settlements:
        net_amount = net_amount + settlement.Amount()

    if len(qualifying_settlements) > 1:
        settlement_attributes = get_settlement_attributes(qualifying_settlements)
        new_settlement = create_settlement(settlement_attributes, net_amount)
        set_parent_settlement(new_settlement, qualifying_settlements)
    else:
        LOGGER.info("There is either only one or no settlements to be netted")


def check_qualifying_settlements_for_netting(first_settlement, settlement):
    currency = first_settlement.Currency().Name()
    value_day = first_settlement.ValueDay()
    counter_party = first_settlement.Counterparty().Name()

    if settlement.Status() != 'Authorised':
        return False
    if settlement.Type() not in ['Loan Fee', 'Finder Fee', 'Payment Cash']:
        return False
    if settlement.Currency().Name() != currency:
        return False
    if settlement.ValueDay() != value_day:
        return False
    if settlement.Counterparty().Name() != counter_party:
        return False
    if settlement.AcquirerName() != 'SECURITY LENDINGS DESK':
        return False

    return True


def get_settlement_attributes(qualifying_settlements):
    """
    Getting attributes from one of the settlements in the "qualifying_settlements" list into a dictionary
    """
    settlement_dict = dict()
    settlement_dict['status'] = qualifying_settlements[0].Status()
    settlement_dict['aquirer'] = qualifying_settlements[0].AcquirerName()
    settlement_dict['acquirer_acc_name'] = qualifying_settlements[0].AcquirerAccName()
    settlement_dict['acquirer_account'] = qualifying_settlements[0].AcquirerAccount()
    settlement_dict['currency'] = qualifying_settlements[0].Currency().Name()
    settlement_dict['value_day'] = qualifying_settlements[0].ValueDay()
    settlement_dict['settlement_type'] = qualifying_settlements[0].Type()
    settlement_dict['counter_party'] = qualifying_settlements[0].Counterparty().Name()
    settlement_dict['counter_party_account_ref'] = qualifying_settlements[0].CounterpartyAccountRef()
    settlement_dict['acquirer_account_network_name'] = qualifying_settlements[0].AcquirerAccountNetworkName()

    return settlement_dict


def create_settlement(settlement_dict, net_amount):
    """
    Creating a new settlement and setting up certain attributes
    """
    try:
        new_settlement = acm.FSettlement()
        new_settlement.RegisterInStorage()
        new_settlement.Status = settlement_dict.get('status')
        new_settlement.AcquirerName = settlement_dict.get('aquirer')
        new_settlement.AcquirerAccName = settlement_dict.get('acquirer_acc_name')
        new_settlement.AcquirerAccount = settlement_dict.get('acquirer_account')
        new_settlement.Currency = settlement_dict.get('currency')
        new_settlement.ValueDay = settlement_dict.get('value_day')
        new_settlement.Type = settlement_dict.get('settlement_type')
        new_settlement.Counterparty = settlement_dict.get('counter_party')
        new_settlement.CounterpartyAccountRef = settlement_dict.get('counter_party_account_ref')
        new_settlement.AcquirerAccountNetworkName = settlement_dict.get('acquirer_account_network_name')
        new_settlement.Amount = net_amount
        new_settlement.RelationType('Ad Hoc Net')
        new_settlement.Trade(None)
        set_call_confirmation(new_settlement)
        new_settlement.Commit()
        return new_settlement
    except Exception as e:
        LOGGER.exception(e)


def set_parent_settlement(new_settlement, qualifying_settlements):
    """
    Setting up the parent settlement and changing the status of the children to void
    """
    acm.BeginTransaction()
    try:
        for settlement in qualifying_settlements:
            settlement_image = settlement.StorageImage()
            settlement_image.Parent(new_settlement)
            settlement_image.Status('Void')
            settlement_image.Commit()
        acm.CommitTransaction()
    except Exception as e:
        LOGGER.exception(e)
        acm.AbortTransaction()


def set_call_confirmation(settlement):

    additional_info_field = 'Call_Confirmation'
    additional_info_value = 'SBLManualRelease'
    settlement.AddInfoValue(additional_info_field, additional_info_value)
    LOGGER.info("Auto-setting Call_Confirmation for Settlement with id {settlement}".format(settlement=settlement.Oid()))
    settlement.Commit()
