'''----------------------------------------------------------------------------------------------------------
MODULE                  :       SettlementNettingHelperFunction
PURPOSE                 :       This module provides common functions needed for various settlement netting
                                rules.
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

    This module contains functions that will be used in different netting rule classes.
    
    The function executeNetting will be called from all netting rule classes and will do the netting
    based on the given parent settlement and settlements to net.
'''

import acm
import FOperationsUtils as Utils
from SettlementCommitter import SettlementCommitter

class SettlementNettingHelperFunction():

    @classmethod
    def IsPartOfNetting(self, obj):
        if obj.Parent():
            return True
        return False
    
    @classmethod
    def GetPortfolio(self, obj):
        if obj.FromPortfolio():
            return obj.FromPortfolio()
        return obj.ToPortfolio()
    
    @classmethod
    def SelectSettlements(self, obj, status, acquirer, relationType, valueDay):
        settlements = acm.FSettlement.Select('status=%i and currency=%i and acquirer=%i and relationType=%s and valueDay=%s ' \
                    %(Utils.GetEnum('SettlementStatus', status), obj.Currency().Oid(), acquirer, Utils.GetEnum('SettlementRelationType', relationType), valueDay))
        return settlements
    
    @classmethod
    def SelectSettlementsCPRestriction(self, obj, status, acquirer, relationType, valueDay):
        settlements = acm.FSettlement.Select('status=%i and currency=%i and acquirer=%i and relationType=%s  and counterparty=%i and valueDay=%s' \
                    %(Utils.GetEnum('SettlementStatus', status), obj.Currency().Oid(), acquirer, Utils.GetEnum('SettlementRelationType', relationType), obj.Counterparty().Oid(), valueDay))
        print settlements, obj.CounterpartyName()
        return settlements
         
    @classmethod
    def __GetNetAmount(self, parentSettlement, settlementsToNet):
        amount = parentSettlement.Amount()
        for s in settlementsToNet:
            amount = amount + s.Amount()
        return amount

    @classmethod
    def __CreateNewParentSettlement(self, settlements):
        settlement = settlements[0]
        new_S = acm.FSettlement()
        new_S.Status('New')
        new_S.RelationType('Ad Hoc Net')
        new_S.Type('None')
        new_S.ToPortfolio(None)
        new_S.FromPortfolio(None)
        new_S.Currency(settlement.Currency())
        new_S.Acquirer(settlement.Acquirer())
        new_S.AcquirerName(settlement.AcquirerName())
        new_S.AcquirerAccountRef(settlement.AcquirerAccountRef())
        new_S.Counterparty(settlement.Counterparty())
        new_S.CounterpartyName(settlement.CounterpartyName())
        new_S.CounterpartyAccountRef(settlement.CounterpartyAccountRef())
        new_S.NettingRule(None)
        new_S.Trade(None)
        new_S.Protection(settlement.Protection())
        new_S.Owner(settlement.Owner())
        new_S.ValueDay(settlement.ValueDay())
        amount = 0
        for s in settlements:
            amount = amount + s.Amount()
        new_S.Amount(amount)
        return new_S
        
    @classmethod
    def executeNetting(self, obj, settlementsToNet, parentSettlement, settlementAddInfoValue):
        settlementCommitter = SettlementCommitter()
        if parentSettlement:
            parentSettlement.Amount(self.__GetNetAmount(parentSettlement, settlementsToNet))
            settlementCommitter.AddParent(parentSettlement)
        else:
            if len(settlementsToNet) > 1:
                parentSettlement = self.__CreateNewParentSettlement(settlementsToNet)
                settlementCommitter.AddParent(parentSettlement)
                
        for s in settlementsToNet:
            s.Status('Void')
            if parentSettlement:
                if s.Oid() != parentSettlement.Oid():
                    settlementCommitter.AddChild(s)
            else:
                settlementCommitter.AddChild(s)

        if parentSettlement and settlementsToNet:
            settlementCommitter.SetSplitNetFlag('Net')
            settlementCommitter.SetAddInfoValue(settlementAddInfoValue)
            settlementCommitter.Commit()
        return False
