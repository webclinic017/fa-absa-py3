""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsArchiveContainers.py"
"""----------------------------------------------------------------------------
MODULE
    FOperationsArchiveContainers - Archive container classes for operations
                                   related objects.

    (c) Copyright 2018 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import acm

#itertools
from itertools import groupby

#accounting
from FAccountingDRCRPairGenerator import GenerateDRCRPairs

#settlement
from FSettlementUtils import IsBeforeTimeWindow, FindRootInPartialHierarchyTree, FindRootInPairOffHierarchyTree, FindRootInHierarchyTree
from FSettlementEnums import RelationType

class OperationsArchiveContainer:

    def __init__(self, entities):
        self._entities = entities
        self._entityName = str(entities[0].ClassName())[1:]
        self._entitiesToArchive = dict()

    def GetEntities(self):
        return self._entities

    def GetEntityName(self):
        return self._entityName

    def GetAllEntitiesToArchive(self):
        return self._entitiesToArchive

    def AddSwiftMessagingObjects(self, entity, linkedObjects):
        externalObjects = entity.ExternalObjects()
        for eo in externalObjects:
            linkedObjects.append(eo)
            if eo.Data():
                linkedObjects.append(eo.Data())
            bprs = acm.FBusinessProcess.Select('subject_type = "ExternalObject" and subject_seqnbr = {}'.format(eo.Oid()))
            for bpr in bprs:
                linkedObjects.append(bpr)
                if bpr.Diary():
                    linkedObjects.append(bpr.Diary())

    def AddOperationsDocumentObjects(self, entity, linkedObjects):
        opsDocs = entity.Documents()
        for doc in opsDocs:
            linkedObjects.append(doc)
            linkedObjects.extend(doc.AddInfos())

class ConfirmationArchiveContainer(OperationsArchiveContainer):

    def __init__(self, entities):
        OperationsArchiveContainer.__init__(self, entities)
        self.SetLinkedObjects()

    def SetLinkedObjects(self):
        for e in self._entities:
            linkedObjects = list()
            linkedObjects.extend(e.AddInfos())
            self.AddOperationsDocumentObjects(e, linkedObjects)
            if e.Diary():
                linkedObjects.append(e.Diary())
            self.AddSwiftMessagingObjects(e, linkedObjects)

            self._entitiesToArchive[e] = linkedObjects

class AccountingArchiveContainer(OperationsArchiveContainer):

    def __init__(self, entities):
        OperationsArchiveContainer.__init__(self, entities)
        self.__journals = dict()
        self.__journalInformations = dict()
        self.__journalLinks = dict()
        self.__GenerateJournalPairs()

    def __GenerateJournalPairs(self):
        assert len(self._entities) != 0, "No journals found!"

        for journalPair in GenerateDRCRPairs(self._entities, True, False, None):
            self.__journalLinks[journalPair.JournalLink()] = None
            for j in journalPair.Journals():
                linkedObjects = list()
                linkedObjects.extend(j.AddInfos())
                self.__journals[j] = linkedObjects

            linkedObjects = list()
            linkedObjects.extend(journalPair.JournalInformation().AddInfos())
            self.__journalInformations[journalPair.JournalInformation()] = linkedObjects


    def GetJournals(self):
        return self.__journals

    def GetJournalLinks(self):
        return self.__journalLinks

    def GetJournalInformations(self):
        return self.__journalInformations

class SettlementArchiveContainer(OperationsArchiveContainer):

    def __init__(self, entities):
        OperationsArchiveContainer.__init__(self, entities)
        self.excludedSettlements = list()
        self.activeSettlements = list()
        self.__ExcludeIneligibleSettlements()

    def __ExcludeIneligibleSettlements(self):
        entitiesList = self._entities
        entitiesList = list(filter(IsBeforeTimeWindow, entitiesList))

        self.activeSettlements = list(set(self._entities) - set(entitiesList))

        self.__RetrieveAndFilterHierarchies(entitiesList)

        entitiesList = list(set(entitiesList) - set(self.excludedSettlements))
        self._entities = []
        self._entities.extend(entitiesList)
        for e in entitiesList:
            linkedObjects = list()
            linkedObjects.extend(e.AddInfos())
            self.AddOperationsDocumentObjects(e, linkedObjects)
            bpr = e.GetSettlementProcess()
            if bpr:
                linkedObjects.append(bpr)
            if e.Diary():
                linkedObjects.append(e.Diary())
            self.AddSwiftMessagingObjects(e, linkedObjects)

            self._entitiesToArchive[e] = linkedObjects

    def __RetrieveAndFilterHierarchies(self, inputList):
        allSettlementsInHierarchy = acm.FSet()
        commonSettlements = acm.FSet()
        visitedSettlements = acm.FSet()
        allSettlements = acm.FSet()
        allSettlements.AddAll(inputList)

        for settlement in inputList:
            if not visitedSettlements.Includes(settlement):
                allSettlementsInHierarchy.Clear()
                commonSettlements.Clear()
                visitedSettlements.Add(settlement)
                topPartialParent = None
                topPairOffParent = None
                topSettlement = None
                parent = settlement.Parent()

                if parent and parent.RelationType() != RelationType.CANCELLATION:
                    topPartialParent = FindRootInPartialHierarchyTree(parent)
                    topPairOffParent = FindRootInPairOffHierarchyTree(parent)
                else:
                    topPartialParent = FindRootInPartialHierarchyTree(settlement)
                    topPairOffParent = FindRootInPairOffHierarchyTree(settlement)

                if topPartialParent:
                    self.__TraverseTree(topPartialParent, allSettlementsInHierarchy)

                if topPairOffParent:
                    self.__TraverseTree(topPairOffParent, allSettlementsInHierarchy)

                topSettlement = FindRootInHierarchyTree(settlement)
                if topSettlement.SplitParent():
                    self.__TraverseTree(topSettlement.SplitParent(), allSettlementsInHierarchy)
                else:
                    self.__TraverseTree(topSettlement, allSettlementsInHierarchy)

                commonSettlements = allSettlements.Intersection(allSettlementsInHierarchy)
                visitedSettlements.AddAll(commonSettlements)

                if commonSettlements.Size() != allSettlementsInHierarchy.Size():
                    self.excludedSettlements.extend(commonSettlements)

    def __TraverseTree(self, settlement, settlementsInHierarchy):
        if settlement:
            settlementsInHierarchy.Add(settlement)

            if settlement.Parent():
                settlementsInHierarchy.Add(settlement.Parent())

                if settlement.Parent().PartialChildren():
                    for partialChild in settlement.Parent().PartialChildren():
                        self.__TraverseTree(partialChild, settlementsInHierarchy)

                if settlement.Parent().PairOffChildren():
                    for pairOffChild in settlement.Parent().PairOffChildren():
                        self.__TraverseTree(pairOffChild, settlementsInHierarchy)

            if settlement.Children():
                settlementsInHierarchy.AddAll(settlement.Children())
                for child in settlement.Children():
                    self.__TraverseTree(child, settlementsInHierarchy)

            if settlement.SplitChildren():
                settlementsInHierarchy.AddAll(settlement.SplitChildren())
                for splitChild in settlement.SplitChildren():
                    self.__TraverseTree(splitChild, settlementsInHierarchy)

            if settlement.PartialChildren():
                for partialChild in settlement.PartialChildren():
                    self.__TraverseTree(partialChild, settlementsInHierarchy)

            if settlement.PairOffChildren():
                for pairOffChild in settlement.PairOffChildren():
                    self.__TraverseTree(pairOffChild, settlementsInHierarchy)

            if settlement.CorrectionSettlement():
                self.__TraverseTree(settlement.CorrectionSettlement(), settlementsInHierarchy)

    def GetActiveSettlements(self):
        return self.activeSettlements

    def GetExcludedSettlements(self):
        return set(self.excludedSettlements)
