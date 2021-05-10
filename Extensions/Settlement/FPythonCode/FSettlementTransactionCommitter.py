""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementTransactionCommitter.py"
"""
FSettlementTransactionCommitter
"""
import acm, math, FSettlementNetting
import FOperationsUtils as Utils
from   FSettlementCommitter import SettlementCommitter, CommitAction
from FSettlementEnums import SettlementStatus, RelationType
from FOperationsExceptions import CommitException
from FSettlementNettingEngine import SettlementNettingEngine

class TransactionCommitter:

    def __init__(self, settlementCommitterList, settlementProcessData, nettingRuleQueryCache, commitedSettlements = acm.FArray()):

        self.__settlementCommitterList = settlementCommitterList
        self.__spd = settlementProcessData
        self.__settlementCommitterMap = self.__GetSettlementCommitterMap()
        self.__commitedSettlements = commitedSettlements
        self.__nettingEngine = SettlementNettingEngine(nettingRuleQueryCache)

    def __Commit(self, commiter):
        commiter.Commit()
        self.__commitedSettlements.Add(commiter.GetSettlement())

    def __GetSettlementCommitterMap(self):
        settlementCommitterMap = dict()
        for sc in self.__settlementCommitterList:
            settlementCommitterMap[sc.GetSettlement().Oid()] = sc
        return settlementCommitterMap

    def CommitSettlements(self):
        acm.BeginTransaction()
        netParentCleanUpList = self.__CommitAndNet()
        try:
            acm.CommitTransaction()
        except Exception as error:
            acm.AbortTransaction()
            Utils.RaiseCommitException(error)

        if len(netParentCleanUpList):
            acm.BeginTransaction()
            self.__NetParentUpdateAndCleanUp(netParentCleanUpList)
            try:
                acm.CommitTransaction()
            except Exception as error:
                acm.AbortTransaction()
                del netParentCleanUpList
                Utils.RaiseCommitException(error)

        del self.__settlementCommitterList[:]

    def CommitSettlementsWithoutTransaction(self):
        netParentCleanUpList = self.__CommitAndNet()
        if len(netParentCleanUpList):
            self.__NetParentUpdateAndCleanUp(netParentCleanUpList)
        del self.__settlementCommitterList[:]

    def __CommitAndNet(self):
        self.__PrintSettlementCommitterList()

        netHierarchiesList, netParentCleanUpList = self.__nettingEngine.Net(self.__settlementCommitterList, self.__settlementCommitterMap)

        for (settlementCommitter, netHierarchyList) in netHierarchiesList:
            if len(netHierarchyList):
                self.__CommitNetHierarchy(settlementCommitter, netHierarchyList)
            else:
                self.__Commit(settlementCommitter)
        return netParentCleanUpList

    def __CommitNetHierarchy(self, settlementCommitter, netHierarchyList):

        netParentSettlementCommitter = netHierarchyList.pop()
        netParent = netParentSettlementCommitter.GetSettlement()
        settlement = settlementCommitter.GetSettlement()
        netParentParent = netParent.Parent()
        if settlement.IsValidForSTP():
            settlement.STP()
        if netParent.IsValidForSTP():
            netParent.STP()
        self.__Commit(netParentSettlementCommitter)
        settlement.Parent(netParent)
        self.__Commit(settlementCommitter)
        for netSettlementCommitter in netHierarchyList:
            netChild = netSettlementCommitter.GetSettlement()
            if netParentParent:
                if netParentParent.Oid() != netChild.Oid():
                    netChild.Parent(netParent)
            else:
                netChild.Parent(netParent)
            self.__Commit(netSettlementCommitter)

    def __NetParentUpdateAndCleanUp(self, netParentList):

        settlementCommitterList = list()

        for netParent in netParentList:
            netChildren = netParent.Children()
            numOfChildren = len(netChildren)
            if numOfChildren == 0:
                settlementCommitterList.append(SettlementCommitter(netParent, CommitAction.DELETE))
            elif numOfChildren == 1:
                netChild = netChildren.First()
                self.__UnNetNetChild(netChild, settlementCommitterList)
                settlementCommitterList.append(SettlementCommitter(netParent, CommitAction.DELETE))
            elif numOfChildren > 1:
                if netParent.RelationType() == RelationType.CLOSE_TRADE_NET:
                    self.__UpdateCloseTradeNetHierarchy(netParent, netChildren, settlementCommitterList)
                else:
                    updateProcess = self.__UpdateNetParent(netParent, netChildren)
                    settlementCommitterList.append(SettlementCommitter(netParent, CommitAction.UPDATE, updateProcess))

        for settlementCommitter in settlementCommitterList:
            self.__Commit(settlementCommitter)
        del settlementCommitterList
        del netParentList

    def __UpdateNetParent(self, netParent, netChildren):
        FSettlementNetting.SetNetParentTypes(netParent, netChildren)
        return FSettlementNetting.SetNetParentData(netParent, netChildren, netParent.NettingRule())

    def __UpdateCloseTradeNetHierarchy(self, netParent, netChildren, settlementCommitterList):

        if not FSettlementNetting.IsCloseTradeNetPart(netChildren[0]):
            for netChild in netChildren:
                self.__UnNetNetChild(netChild, settlementCommitterList)
            settlementCommitterList.append(SettlementCommitter(netParent, CommitAction.DELETE))
        else:
            self.__UpdateNetParent(netParent, netChildren)
            settlementCommitterList.append(SettlementCommitter(netParent, CommitAction.UPDATE))

    def __UnNetNetChild(self, netChild, settlementCommitterList):

        if netChild.Status() != SettlementStatus.PENDING_AMENDMENT:
            netChild.Status(SettlementStatus.EXCEPTION)
        netChild.Parent(None)
        netChild.IsChangeToSourceData(False)
        netChild.IsAmendmentProcess(False)
        if netChild.IsValidForSTP():
            netChild.STP()
        netChild.StateChart(acm.Operations.GetMappedSettlementProcessStateChart(netChild))
        settlementCommitterList.append(SettlementCommitter(netChild, CommitAction.UPDATE, True))

    def __IsSettlementIncludedInList(self, settlement, settlementList):

        isSettlementIncludedInList = False
        for s in settlementList:
            if s.Oid() == settlement.Oid():
                isSettlementIncludedInList = True
                break
        return isSettlementIncludedInList

    def __PrintSettlementCommitterList(self):

        printList = []
        for sc in self.__settlementCommitterList:
            printList.append(sc.GetSettlement().Oid())
        Utils.LogVerbose('Settlements in settlementCommitterList %s' % printList)


class PartyUpdateCommitter:

    TRANSACTION_SIZE = 50

    def __init__(self, settlementCommitterList, settlementProcessData, nettingRuleQueryCache):
        self.__settlementCommitterList = settlementCommitterList
        self.__spd = settlementProcessData
        self.__settlementsWithTradeReferences = []
        self.__settlementsWithoutTradeReferences = []
        self.__nettingRuleQueryCache = nettingRuleQueryCache
        self.SetSettlementCommiterLists(self.__settlementsWithTradeReferences, self.__settlementsWithoutTradeReferences)
        self.SortSettlementCommitterList()

    def SetSettlementCommiterLists(self, settlementsWithTradeReferences, settlementsWithoutTradeReferences):

        for sc in self.__settlementCommitterList:
            if sc.GetSettlement().Trade() == None:
                settlementsWithoutTradeReferences.append(sc)
            else:
                settlementsWithTradeReferences.append(sc)

    def SortSettlementCommitterList(self):

        self.__settlementsWithTradeReferences.sort(PartyUpdateCommitter.SortSettlementsByTradeOid)
        self.__settlementsWithTradeReferences.reverse()

    def CommitSettlements(self):

        commitList = self.GetTradeCommitList() + self.GetStandAloneCommitList()
        for scList in commitList:
            tc = TransactionCommitter(scList, self.__spd, self.__nettingRuleQueryCache)
            try:
                tc.CommitSettlements()
            except CommitException as error:
                self.__spd.ErrorLog(error)

    def GetTradeCommitList(self):

        scList = self.__settlementsWithTradeReferences
        tmpList = []
        commitList = []
        if len(scList):
            tmpList.append(scList.pop())
            while len(scList):
                sc = scList.pop()
                if sc.GetSettlement().Trade().Oid() == \
                   tmpList[0].GetSettlement().Trade().Oid():
                    tmpList.append(sc)
                else:
                    commitList.append(tmpList)
                    tmpList = [sc]
            commitList.append(tmpList)
        return commitList

    def GetStandAloneCommitList(self):

        aList = []
        length = len(self.__settlementsWithoutTradeReferences) / 1.0
        batchSize = math.ceil(length / PartyUpdateCommitter.TRANSACTION_SIZE)
        counter = 0
        index = 0
        while counter != batchSize:
            aList.append(self.__settlementsWithoutTradeReferences[index:PartyUpdateCommitter.TRANSACTION_SIZE * (counter + 1)])
            counter += 1
            index = PartyUpdateCommitter.TRANSACTION_SIZE * counter
        return aList

    @staticmethod
    def SortSettlementsByTradeOid(settlementCommitter1, settlementCommitter2):

        sortResult = 0
        oid1 = settlementCommitter1.GetSettlement().Trade().Oid()
        oid2 = settlementCommitter2.GetSettlement().Trade().Oid()
        if oid1 < oid2:
            sortResult = -1
        elif oid1 > oid2:
            sortResult = 1
        return sortResult
