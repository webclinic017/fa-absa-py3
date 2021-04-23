'''----------------------------------------------------------------------------------------------------------
MODULE                  :       SettlementNettingRuleGold
PURPOSE                 :       This module contains the Gold Netting rule.
DEPARTMENT AND DESK     :       OPS
REQUASTER               :       Nicolette Burger
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       335129
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2012-07-13      335129          Heinrich Cronje                 Initial Implementation

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    Settlements should be netted if the counterparty is BARCLAYS BANK PLC or BARCLAYS BNK PLC GERMISTON,
    the portfolio OTC GOLD, the instrument XAU and the currency USD.
'''

import acm
from SettlementNettingHelperFunction import SettlementNettingHelperFunction as HelperUtils

class SettlementNettingRuleGold():
    def __init__(self, obj):
        self.settlObj = obj
        self.trade = self.settlObj.Trade()
        self.VALID_CURR = 'USD'
        self.VALID_INSID = 'XAU'
        self.VALID_PARTIES = ['BARCLAYS BANK PLC', 'BARCLAYS BNK PLC GERMISTON']
        self.VALID_PORTFOLIO = 'OTC GOLD'
        self.isUpdateCollision = ''
        self.executeGoldNetting()

    def IsGoldSettlement(self, overrideSettlement = None, override = False):
        settlObj = self.settlObj
        if overrideSettlement:
            settlObj = overrideSettlement
            
        validGoldSettlement = 0
        currency = settlObj.Currency()
        counterparty = settlObj.Counterparty()
        portfolio = self.trade.Portfolio()
        if settlObj.RelationType() == 'None' and currency and currency.Name() == self.VALID_CURR \
                and self.trade.Instrument().Name() == self.VALID_INSID \
                and counterparty and counterparty.Name() in self.VALID_PARTIES \
                and portfolio and portfolio.Name() == self.VALID_PORTFOLIO \
                and ((override) or (not override and not settlObj.Parent())):
            validGoldSettlement = 1
            
        return validGoldSettlement
    
    def GetGoldSettlements(self):
        valid_settl = acm.FArray()
        if self.trade:
            if not HelperUtils.IsPartOfNetting(self.settlObj):
                settlements = HelperUtils.SelectSettlements(self.settlObj, 'Authorised', self.settlObj.Acquirer().Oid(), self.settlObj.RelationType(), self.settlObj.ValueDay())
                
                for s in settlements:
                    if self.IsGoldSettlement(s):
                        valid_settl.Add(s)
        return valid_settl
    
    def GetParentGoldSettlement(self, settlementsToNet):
        s = settlementsToNet[0]
        potentialParents = HelperUtils.SelectSettlements(s, 'Authorised', s.Acquirer().Oid(), 'Ad Hoc Net', s.ValueDay())
        
        for parent in potentialParents:
            validParent = 1
            for child in parent.Children():
                if not self.IsGoldSettlement(child, True):
                    validParent = 0
            if validParent:
                return parent
        return None
        
    def executeGoldNetting(self):
        if not HelperUtils.IsPartOfNetting(self.settlObj):
            if self.IsGoldSettlement():
                settlementsToNet = self.GetGoldSettlements()
                parentSettlement = None
                if settlementsToNet:
                    parentSettlement = self.GetParentGoldSettlement(settlementsToNet)
                    self.isUpdateCollision = HelperUtils.executeNetting(self.settlObj, settlementsToNet, parentSettlement, 'Gold_Auto_Netting')
        self.isUpdateCollision
