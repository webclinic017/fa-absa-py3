'''
Created on 3 Jun 2014

@author: conicova
HISTORY
=================================================================================================================================
Date            Change no       Developer              Requester         Description
=================================================================================================================================
2014-06-05      CHNG0001963915  Andrei Conicov        Bruce Dell         New netting rule for the paying agent
2020-03-17      FAOPS-623       Ntokozo Skosana       Seven Khoza        Include 'Float-rate' in CashFlow type for
                                                                         'Coupon' settlements

=================================================================================================================================
'''
from demat_isin_mgmt_menex import current_ins_available_amount

def PayingAgentNetting(settlement, settlementCadidate):
    """ Returns true if both settlements have the same:
    1. first 6 chars in the External id1
    2. the same counterparty
    3. the same Trans Ref 
    """
    isPayingAgentNetting = False
    
    theSameExternalId1 = False
    if settlement.Trade() and settlementCadidate.Trade():
        externalId1 = settlement.Trade().Instrument().ExternalId1()
        externalId1Candidate = settlementCadidate.Trade().Instrument().ExternalId1()
        theSameExternalId1 = externalId1 and externalId1[0:6] == externalId1Candidate[0:6]
    
    theSameCounterparty = settlement.Counterparty() == settlementCadidate.Counterparty()
    
    theSameTransRef = False
    if settlement.Trade().TrxTrade() and settlementCadidate.Trade().TrxTrade():
        theSameTransRef = settlement.Trade().TrxTrade() == settlementCadidate.Trade().TrxTrade()
    
    if theSameCounterparty and theSameExternalId1 and theSameTransRef:
        isPayingAgentNetting = True
    
    return isPayingAgentNetting


def check_if_additional_payment_generated(settlement):
    cashflows = settlement.SecurityInstrument().MainLeg().CashFlows()
    
    for cashflow in cashflows:
        if cashflow.PayDate() == settlement.ValueDay():
            if settlement.Type() == 'Redemption':
                if cashflow.CashFlowType() == 'Fixed Amount':
                    print cashflow.Oid(), 'calc_appr', cashflow.AddInfoValue('Demat_Calc_Approvl')
                    if cashflow.AddInfoValue('Demat_Calc_Approvl'):
                        return True
                    else:
                        return False
            elif settlement.Type() == 'Coupon':
                if cashflow.CashFlowType() in ['Fixed Rate', 'Float Rate']:
                    print cashflow.Oid(), 'calc_appr', cashflow.AddInfoValue('Demat_Calc_Approvl')
                    if cashflow.AddInfoValue('Demat_Calc_Approvl'):
                        return True
                    else:
                        return False
                
    return False


def compare_DIS_settlements(settlement, settlementCadidate, type):
    if not settlement.Type() == type and settlementCadidate.Type() == type:
        return False
    if not settlement.SecurityInstrument() == settlementCadidate.SecurityInstrument():
        return False
    if not settlement.ValueDay() == settlementCadidate.ValueDay():
        return False
    if not settlement.CounterpartyAccount() == settlementCadidate.CounterpartyAccount():
        return False
    if not settlement.Currency() == settlementCadidate.Currency():
        return False
    if not settlement.AcquirerAccount() == settlementCadidate.AcquirerAccount():
        return False
        
    return True


def DISCouponNetting(settlement, settlementCadidate):
    if settlement.SecurityInstrument():
        if current_ins_available_amount(settlement.SecurityInstrument()) == 0:
            return compare_DIS_settlements(settlement, settlementCadidate, 'Coupon')
            

        elif check_if_additional_payment_generated(settlement):
            return compare_DIS_settlements(settlement, settlementCadidate, 'Coupon')
        else:
            return False
            
            
def DISRedemptionNetting(settlement, settlementCadidate):
    if settlement.SecurityInstrument():
        if current_ins_available_amount(settlement.SecurityInstrument()) == 0:
            return compare_DIS_settlements(settlement, settlementCadidate, 'Redemption')
            

        elif check_if_additional_payment_generated(settlement):
            return compare_DIS_settlements(settlement, settlementCadidate, 'Redemption')
        else:
            return False
