""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementCorrectTradeRecaller.py"
import FOperationsUtils as Utils
import FSettlementUtils
from FSettlementCorrectTradeHandler import CorrectTradeHandler
import FSettlementRecallHandlerSingleton as Singleton
from FSettlementEnums import SettlementStatus, RelationType, SettlementType

class FSettlementCorrectTradeRecaller(object):
    def __init__(self):
        self.__settlementsFromTheCreator = list()
        self.__recallHandler = Singleton.GetSettlementRecallHandler()


    def __FindEqualSettlementInList(self, settlement, settlementList):
        foundSettlement = None
        for aSettlement in settlementList:
            if aSettlement.Type() == settlement.Type():
                if aSettlement.IsSameReferenceOid(settlement):
                    foundSettlement = aSettlement
                    break
                if aSettlement.RefPayment() == settlement.Payment():
                    foundSettlement = aSettlement
                    break
                else:
                    if not settlement.HasDividendCashFlowPaymentReference():
                        foundSettlement = aSettlement
                        break
        return foundSettlement


    def AddSettlement(self, settlement):
        self.__settlementsFromTheCreator.append(settlement)


    def RecallSettlementIfApplicable(self, trade):
        settlementCommitterList = list()

        if Utils.IsCorrectingTrade(trade):
            if not Utils.IsCorrectedTrade(trade):
                for aTrade in CorrectTradeHandler.GetCorrectedTrades(trade):
                    for aSettlement in aTrade.Settlements():
                        if FSettlementUtils.IsWithinTimeWindow(aSettlement):
                            if aSettlement.RelationType() == RelationType.NONE:
                                if not aSettlement.IsRecalledData():
                                    if aSettlement.Type() != SettlementType.STAND_ALONE_PAYMENT:
                                        recallSettlement = False
                                        rootSettlement = FSettlementUtils.FindRootInHierarchyTree(aSettlement)
                                        if trade.Counterparty() != aTrade.Counterparty():
                                            recallSettlement = True
                                        elif self.__FindEqualSettlementInList(aSettlement, self.__settlementsFromTheCreator) == None:
                                            recallSettlement = True
                                        elif not FSettlementUtils.CorrectTradePayNet(rootSettlement):
                                            recallSettlement = True

                                        if rootSettlement.Status() == SettlementStatus.CLOSED:
                                            recallSettlement = False
                                        if recallSettlement:
                                            for sc in self.__recallHandler.ProcessRecall(aSettlement):
                                                settlementCommitterList.append(sc)
        return settlementCommitterList