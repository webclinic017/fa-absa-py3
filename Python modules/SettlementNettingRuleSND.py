'''----------------------------------------------------------------------------------------------------------
MODULE                  :       SettlementNettingRuleSND
PURPOSE                 :       This module contains the SND Netting rule.
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
2012-12-07      653119          Tesslyn Pillay                  Change to allow netting to take place within
                                                                counterpiarties via trans ref
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    Settlements should be netted if the acquirer is STRUCT NOTES DESK or
    if the acquirer is CREDIT DERIVATIVES DESK and the portfolio in one the following compound portfolios:
    1574,1571,1573,2792,2793,2794,1572,3306,0057
'''

import ael, acm
from SettlementNettingHelperFunction import SettlementNettingHelperFunction as HelperUtils
from SAGEN_IT_Functions import get_Port_Struct_from_Port

class SettlementNettingRuleSND():
    def __init__(self, settlObj):
        self.settlObj = settlObj
        self.INVALID_SETTLEMENT_TYPES = ['Security Nominal']
        self.ACQUIRER = [30301] #30301 = STRUCT NOTES DESK
        self.ACQUIRER_FOR_VALID_PORTF = [6292]          #6292 = CREDIT DERIVATIVES DESK
        self.VALID_PORTF_FOR_ACQUIRER = [1512, 1518, 1631, 1644, 1742, 1746, 1827, 1884, 1098]         #1512 = 1574,   1518 = 1571,    1631 = 1573,    1644 = 2792,    1742 = 2793,    1746 = 2794,    1827 = 1572,    1884 = 3306,    1098 = 0057
        self.isUpdateCollision = ''
        self.executeSNDNetting()
        
    def IsValidPortfolio(self, portfolio):
        for p in self.VALID_PORTF_FOR_ACQUIRER:
            if get_Port_Struct_from_Port(ael.Portfolio[str(portfolio.Name())], str(ael.Portfolio[p].prfid)):
                return True
        return False
        
    def IsSNDSettlement(self,overrideSettlement = None, override = False):
        settlObj = self.settlObj
        if overrideSettlement:
            settlObj = overrideSettlement
        validSNDSettlement = 0
        if settlObj.RelationType() == 'None' and settlObj.Trade().TrxTrade() and (settlObj.Type() not in (self.INVALID_SETTLEMENT_TYPES)) and ((override) or (not override and not settlObj.Parent())):
            acquirerOid = settlObj.Acquirer().Oid()
            if acquirerOid in self.ACQUIRER:
                validSNDSettlement = 1
            elif acquirerOid in self.ACQUIRER_FOR_VALID_PORTF:
                portfolio = HelperUtils.GetPortfolio(settlObj)
                if portfolio:
                    if self.IsValidPortfolio(portfolio):
                        validSNDSettlement = 1

        return validSNDSettlement

    def TrxTradeCheck(self, s):
        trxTrade = s.Trade().TrxTrade()
        return s.RelationType() == 'None' and trxTrade and trxTrade.Oid() == self.settlObj.Trade().TrxTrade().Oid() and not s.Parent() and (self.settlObj.Type() not in (self.INVALID_SETTLEMENT_TYPES))

    def TrxTradeCheckOnly(self, s, obj):
        trxTrade = s.Trade().TrxTrade()
        return trxTrade and trxTrade.Oid() == obj.Trade().TrxTrade().Oid() and (obj.Type() not in (self.INVALID_SETTLEMENT_TYPES))

    def GetSNDSettlements(self):
        valid_settl = acm.FArray()
        if self.settlObj.Trade():
            if not HelperUtils.IsPartOfNetting(self.settlObj):
                settl_ACQUIRER_A = HelperUtils.SelectSettlementsCPRestriction(self.settlObj, 'Authorised', self.ACQUIRER[0], self.settlObj.RelationType(), self.settlObj.ValueDay())
                
                settlACQUIRER_FOR_VALID_PORTF_A = HelperUtils.SelectSettlementsCPRestriction(self.settlObj, 'Authorised', self.ACQUIRER_FOR_VALID_PORTF[0], self.settlObj.RelationType(), self.settlObj.ValueDay())

                for s in settl_ACQUIRER_A:
                    if self.TrxTradeCheck(s):
                        valid_settl.Add(s)
                
                for s in settlACQUIRER_FOR_VALID_PORTF_A:
                    if self.TrxTradeCheck(s):
                        if self.IsSNDSettlement(s):
                            valid_settl.Add(s)
        return valid_settl

    def GetParentSettlement(self, settlementsToNet):
        s = settlementsToNet[0]
        potentialParentsA = HelperUtils.SelectSettlementsCPRestriction(s, 'Authorised', self.ACQUIRER[0], 'Ad Hoc Net', s.ValueDay())

        potentialParentsB = HelperUtils.SelectSettlementsCPRestriction(s, 'Authorised', self.ACQUIRER_FOR_VALID_PORTF[0], 'Ad Hoc Net', s.ValueDay())
        
        potentialParents = acm.FArray()
        for p in potentialParentsA:
            potentialParents.Add(p)
        for p in potentialParentsB:
            potentialParents.Add(p)
        
        for parent in potentialParents:
            validParent = 1
            for child in parent.Children():
                if not self.IsSNDSettlement(child, True):        
                    validParent = 0
                elif not self.TrxTradeCheckOnly(child, s):
                    validParent = 0
            if validParent:
                return parent
        return None
        
    def executeSNDNetting(self):
        if not HelperUtils.IsPartOfNetting(self.settlObj):
            if self.IsSNDSettlement():
                settlementsToNet = self.GetSNDSettlements()
                parentSettlement = None
                if settlementsToNet:
                    parentSettlement = self.GetParentSettlement(settlementsToNet)
                    self.isUpdateCollision = HelperUtils.executeNetting(self.settlObj, settlementsToNet, parentSettlement, 'SND_Auto_Netting')
        self.isUpdateCollision =  False
