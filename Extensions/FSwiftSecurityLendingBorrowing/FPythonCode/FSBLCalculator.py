'''
FSBLCalculator.py

Module that calculate the message types for SBL trades.
-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
01-05-2020   SBL          Jaysen Naicker          Gasant Thulsie                Calculate the message type for SBL messages
-----------------------------------------------------------------------------------------------------------------------------------------
'''

from FSecurityLendingBorrowingOutUtils import (is_business_partner, get_client_from_settlement, get_additionalinfo_value_for)
from FSwiftServiceSelector import is_security_loan_settlement, is_collateral_settlement, is_off_market_security_loan_settlement, is_off_market_collateral_settlement
import acm
import FSwiftWriterAPIs
import FLogger

LOGGER = FLogger.FLogger('FSBLCalculator')
ACQUIRER_NAMES = ('SECURITY LENDINGS DESK')
PAYMENT_TYPES = ('Security Nominal', 'End Security')


def is_sl_swift(settlement):
    acquirer = settlement.Acquirer().Name() in ACQUIRER_NAMES
    add_inf_spec = get_additionalinfo_value_for(settlement.Trade(), 'SL_SWIFT') != None
    return add_inf_spec and acquirer


def get_custom_message_type(acm_obj, message_type_from_mt_calculator):
    if is_sl_swift(acm_obj):
        swift_addinfo = get_additionalinfo_value_for(acm_obj.Trade(), 'SL_SWIFT')
        if swift_addinfo == 'SWIFT'  and acm_obj.Type() in PAYMENT_TYPES:
           return get_custom_message_type_on_market(acm_obj, message_type_from_mt_calculator)
           
        elif swift_addinfo == 'DOM' and acm_obj.Type() in PAYMENT_TYPES:
            return get_custom_message_type_off_market(acm_obj, message_type_from_mt_calculator)
            
        else:
            return message_type_from_mt_calculator
            
    return message_type_from_mt_calculator


def get_custom_message_type_on_market(acm_obj, message_type_from_mt_calculator):
    # For Security Loans
    if is_security_loan_settlement(acm_obj, message_type_from_mt_calculator):
        if acm_obj.RelationType() == 'Cancellation':
            return '598_132'
        client = get_client_from_settlement(acm_obj)
        if is_business_partner(client):
            return '598_131'
        else:
            return '598_130'
    #For Collaterals
    elif is_collateral_settlement(acm_obj, message_type_from_mt_calculator):
        if acm_obj.RelationType() == 'Cancellation':
            return '598_132'
        counterparty = acm_obj.Trade().Counterparty()
        if is_business_partner(counterparty):
            return '598_131'
        else:
            return '598_130'
            
def get_custom_message_type_off_market(acm_obj, message_type_from_mt_calculator):           
    trade = acm_obj.Trade()
    counterparty = trade.Counterparty()
    
    # For Security Loans
    if is_off_market_security_loan_settlement(acm_obj, message_type_from_mt_calculator):
        if counterparty.Name() == 'ABSA SECURITIES LENDING' and trade.Portfolio().Name() == 'SBL Agency':
            if trade.Quantity() < 0 and trade.AdditionalInfo().SL_G1Counterparty1():
                if trade.Text1() in ['FULL_RETURN', 'PARTIAL_RETURN']:
                    return '540'
                else:
                    return '542'
            if trade.Quantity() > 0 and trade.AdditionalInfo().SL_G1Counterparty2():
                if trade.Text1() in ['FULL_RETURN', 'PARTIAL_RETURN']:
                    return '542'
                else:
                    return '540'
                
        if counterparty.Name() == 'SBL AGENCY I/DESK' and trade.Portfolio().Name() != 'SBL Agency':
            if trade.Quantity() > 0 and trade.AdditionalInfo().SL_G1Counterparty1():
                if trade.Text1() in ['FULL_RETURN', 'PARTIAL_RETURN']:
                    return '540'
                else:
                    return '542'
            if trade.Quantity() < 0 and trade.AdditionalInfo().SL_G1Counterparty2():
                if trade.Text1() in ['FULL_RETURN', 'PARTIAL_RETURN']:
                    return '542'
                else:
                    return '540'
                    
    # For Collaterals
    if is_off_market_collateral_settlement(acm_obj, message_type_from_mt_calculator):
        if trade.Portfolio().Name().startswith('SBL_NonCash_Collateral'):
            if trade.Quantity() > 0:
                return '540'
            if trade.Quantity() < 0:
                return '542'
    return message_type_from_mt_calculator
