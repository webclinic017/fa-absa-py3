'''----------------------------------------------------------------------------------------------------------
MODULE                  :       SAIT_MOneyFlow_SettlementLink
PROJECT                 :       Cross Border Foreign Exchange Transaction Reporting
PURPOSE                 :       This module retrives rhe settlement from a money flow object.
DEPARTMENT AND DESK     :       Operations
REQUASTER               :       CBFETR Project - BOPCUS 3 Upgrade
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       CHNG0001209844
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2013-08-17      CHNG0001209844  Heinrich Cronje                 Initial Implementation

-------------------------------------------------------------------------------------------------------------

'''

import acm
import FOperationsUtils as Utils

def get_top_level_settlement(settlement):
    if settlement.Parent():
        return get_top_level_settlement(settlement.Parent())
    elif settlement.SplitChildren():
        return get_top_level_settlement(settlement.SplitChildren()[0])
    else:
        return settlement
   
def get_settlement_from_money_flow(mf):
    sourceObject = mf.SourceObject()
    if sourceObject.RecordType() == 'Trade':
        settlements = acm.FSettlement.Select('type = %i and trade = %i and relationType = None' %(Utils.GetEnum('SettlementCashFlowType', mf.Type()), sourceObject.Oid()))
        for settlement in settlements:
            return get_top_level_settlement(settlement)
    elif sourceObject.RecordType() == 'Instrument':
        settlements = acm.FSettlement.Select('type = %i and trade = %i and relationType = None' %(Utils.GetEnum('SettlementCashFlowType', mf.Type()), mf.Trade().Oid()))
        for settlement in settlements:
            return get_top_level_settlement(settlement)
    elif sourceObject.RecordType() == 'CashFlow':
        settlements = acm.FSettlement.Select('cashFlow = %i and trade = %i and relationType = None' %(sourceObject.Oid(), mf.Trade().Oid()))
        for settlement in settlements:
            return get_top_level_settlement(settlement)
    elif sourceObject.RecordType() == 'Payment':
        settlements = acm.FSettlement.Select('payment = %i and relationType = None' %sourceObject.Oid())
        for settlement in settlements:
            return get_top_level_settlement(settlement)

def get_mf_settlement_from_trade_or_mf(acmObject):
    try:
        #Trade Processing
        list = acm.FArray()
        for mf in acmObject.MoneyFlows(None, None):
            mf_settlement = get_mf_settlement_from_trade_or_mf(mf)
            if mf_settlement:
                list.Add(mf_settlement)
        return list
    except:
        #Money Flow Processing
        return get_settlement_from_money_flow(acmObject)

'''
#Testing
trade = acm.FTrade[4892623]
print get_mf_settlement_from_trade_or_mf(trade)
'''
