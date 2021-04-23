""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/upgrade/FAccountingUpgradeScript.py"
import acm
import FAccountingUpgradeUtils as UpgradeUtils
import FOperationsUtils as Utils



ael_variables = []

class AccountingUpgradeHandler(object):

    newTreatmentLinks               = acm.FArray()
    newTreatmentMappings            = acm.FArray()
    newAIMappings                   = acm.FArray()
    clonedOriginalTAccountMappings  = acm.FArray()


    def RunUpgradeScript(self):
        try:
            Utils.LogAlways("Upgrade to the new accounting solution has started.")
            Utils.LogAlways("Checking if environment has already been upgraded.")
            alreadyUpgraded = UpgradeUtils.CheckIfEnvironmentIsAlreadyUpgraded()
            if alreadyUpgraded:
                Utils.LogAlways("Found already upgraded mappings. The upgrade will be aborted.")
                return

            self.BackupClonesOfOriginalTAccountMappings()


            self.newTreatmentLinks.AddAll(UpgradeUtils.CreateNewTreatmentLinks())

            tradeTreatmentMappingsDict          = UpgradeUtils.GetTreatmentMappingsDictGroupedByBooks(UpgradeUtils.TreatmentType.TRADE)
            settlementTreatmentMappingsDict     = UpgradeUtils.GetTreatmentMappingsDictGroupedByBooks(UpgradeUtils.TreatmentType.SETTLEMENT)

            moneyflowAIMappingsDict             = UpgradeUtils.GetAIMappingsDictGroupedByBookLinks(UpgradeUtils.AIType.MONEYFLOW, self.newTreatmentLinks)
            legAIMappingsDict                   = UpgradeUtils.GetAIMappingsDictGroupedByBookLinks(UpgradeUtils.AIType.LEG, self.newTreatmentLinks)
            tradeAIMappingsDict                 = UpgradeUtils.GetAIMappingsDictGroupedByBookLinks(UpgradeUtils.AIType.TRADE, self.newTreatmentLinks)
            combinationAIMappingsDict           = UpgradeUtils.GetAIMappingsDictGroupedByBookLinks(UpgradeUtils.AIType.COMBINATION, self.newTreatmentLinks)
            settlementAIMappingsDict            = UpgradeUtils.GetAIMappingsDictGroupedByBookLinks(UpgradeUtils.AIType.SETTLEMENT, self.newTreatmentLinks)

            tradeTAccountMappingsDict           = UpgradeUtils.GetTAccountMappingsDictGroupedByTreatmentLinks(UpgradeUtils.TAccountType.TRADE, self.newTreatmentLinks)
            settlementTAccountMappingsDict      = UpgradeUtils.GetTAccountMappingsDictGroupedByTreatmentLinks(UpgradeUtils.TAccountType.SETTLEMENT, self.newTreatmentLinks)


            newTradeTreatmentMappingsDict       = UpgradeUtils.CreateNewTreatmentMappingsDictFromBranchDict(tradeTreatmentMappingsDict)
            newSettlTreatmentMappingsDict       = UpgradeUtils.CreateNewTreatmentMappingsDictFromBranchDict(settlementTreatmentMappingsDict)

            newMoneyflowAIMappingsDict          = UpgradeUtils.CreateNewAIMappingsFromBranchDict(moneyflowAIMappingsDict, self.newTreatmentLinks)
            newLegAIMappingsDict                = UpgradeUtils.CreateNewAIMappingsFromBranchDict(legAIMappingsDict, self.newTreatmentLinks)
            newTradeAIMappingsDict              = UpgradeUtils.CreateNewAIMappingsFromBranchDict(tradeAIMappingsDict, self.newTreatmentLinks)
            newCombinationAIMappingsDict        = UpgradeUtils.CreateNewAIMappingsFromBranchDict(combinationAIMappingsDict, self.newTreatmentLinks)
            newSettlementAIMappingsDict         = UpgradeUtils.CreateNewAIMappingsFromBranchDict(settlementAIMappingsDict, self.newTreatmentLinks)

            newTradeTAccountMappingsDict        = UpgradeUtils.UpdateFAccountMappingsFromBranchDict(tradeTAccountMappingsDict)
            newSettlementTAccountMappingsDict   = UpgradeUtils.UpdateFAccountMappingsFromBranchDict(settlementTAccountMappingsDict)


            tradeTreatmentMappingsTreeDict      = UpgradeUtils.CreateTreatmentMappingTreesDict(newTradeTreatmentMappingsDict)
            settlemenTreatmentMappingsTreeDict  = UpgradeUtils.CreateTreatmentMappingTreesDict(newSettlTreatmentMappingsDict)

            moneyflowAIMappingsTreeDict         = UpgradeUtils.CreateAIMappingTreesDict(newMoneyflowAIMappingsDict)
            legAIMappingsTreeDict               = UpgradeUtils.CreateAIMappingTreesDict(newLegAIMappingsDict)
            tradeAIMappingsTreeDict             = UpgradeUtils.CreateAIMappingTreesDict(newTradeAIMappingsDict)
            combinationAIMappingsTreeDict       = UpgradeUtils.CreateAIMappingTreesDict(newCombinationAIMappingsDict)
            settlementAIMappingsTreeDict        = UpgradeUtils.CreateAIMappingTreesDict(newSettlementAIMappingsDict)

            tradeTAccountMappingsTreeDict       = UpgradeUtils.CreateTAccountMappingTreesDict(newTradeTAccountMappingsDict)
            settlementTAccountMappingsTreeDict  = UpgradeUtils.CreateTAccountMappingTreesDict(newSettlementTAccountMappingsDict)


            #create new treatment links and new mappings
            try:
                acm.BeginTransaction()

                Utils.LogAlways("\nStep 1: Updating treatment links")
                self.CommitTreatmentLinks(self.newTreatmentLinks)
                Utils.LogAlways("Step 1: Done")


                Utils.LogAlways("\nStep 2: Creating new treatment mappings")
                self.CommitTreatmentMappingTrees(tradeTreatmentMappingsTreeDict)
                self.CommitTreatmentMappingTrees(settlemenTreatmentMappingsTreeDict)
                Utils.LogAlways("Step 2: Done")

                Utils.LogAlways("\nStep 3: Creating new accounting instruction mappings")
                self.CommitAIMappingTrees(moneyflowAIMappingsTreeDict)
                self.CommitAIMappingTrees(legAIMappingsTreeDict)
                self.CommitAIMappingTrees(tradeAIMappingsTreeDict)
                self.CommitAIMappingTrees(combinationAIMappingsTreeDict)
                self.CommitAIMappingTrees(settlementAIMappingsTreeDict)
                Utils.LogAlways("Step 3: Done")

                Utils.LogAlways("\nStep 4: Updating taccount mappings")
                self.CommitTAccountMappingTrees(tradeTAccountMappingsTreeDict)
                self.CommitTAccountMappingTrees(settlementTAccountMappingsTreeDict)
                Utils.LogAlways("Step 4: Done")

                acm.CommitTransaction()

            except Exception as e:
                acm.AbortTransaction()
                Utils.LogAlways("\nAn exception occurred while committing:\n%s" % str(e))
                Utils.LogAlways("\nReverting changes.")
                self.RevertChanges()
                Utils.LogAlways("\nReverting changes: Done.")
                Utils.LogAlways("\nUpgrade was aborted.")
                return

            #set mapping references
            try:
                Utils.LogAlways("\nStep 5: Setting references for new treatment mappings")
                self.CommitMappingTreeReferences(tradeTreatmentMappingsTreeDict)
                self.CommitMappingTreeReferences(settlemenTreatmentMappingsTreeDict)
                Utils.LogAlways("Step 5: Done")

                Utils.LogAlways("\nStep 6: Setting references for new accounting instruction mappings")
                self.CommitMappingTreeReferences(moneyflowAIMappingsTreeDict)
                self.CommitMappingTreeReferences(legAIMappingsTreeDict)
                self.CommitMappingTreeReferences(tradeAIMappingsTreeDict)
                self.CommitMappingTreeReferences(combinationAIMappingsTreeDict)
                self.CommitMappingTreeReferences(settlementAIMappingsTreeDict)
                Utils.LogAlways("Step 6: Done")

                Utils.LogAlways("\nStep 7: Setting references for updated taccount mappings")
                self.CommitMappingTreeReferences(tradeTAccountMappingsTreeDict)
                self.CommitMappingTreeReferences(settlementTAccountMappingsTreeDict)
                Utils.LogAlways("Step 7: Done")

            except Exception as e:
                Utils.LogAlways("\nAn exception occurred while committing:\n%s" % str(e))
                Utils.LogAlways("\nReverting changes.")
                self.RevertChanges()
                Utils.LogAlways("\nReverting changes: Done.")
                Utils.LogAlways("\nUpgrade was aborted.")
                return

            try:
                Utils.LogAlways("\nStep 8: Deleting old treatment links")
                self.DeleteOldTreatmentLinks()
                Utils.LogAlways("Step 8: Done")

                Utils.LogAlways("\nStep 9: Deleting old mappings")
                self.DeleteOldMappings()
                Utils.LogAlways("Step 9: Done")
            except Exception as e:
                Utils.LogAlways("\nAn exception occurred while deleting old links and mappings:\n%s" % str(e))
                Utils.LogAlways("\nUpgrade was aborted.")
                return

            Utils.LogAlways("\nThe environment has been successfully upggraded to the new accounting solution!")

        except Exception as e:
            Utils.LogAlways("\nAn exception occurred while performing the upgrade:\n%s" % str(e))
            Utils.LogAlways("\nUpgrade was aborted.")
            return



    def CommitTreatmentLinks(self, treatmentLinks):
        for treatmentLink in treatmentLinks:
            Utils.LogAlways(self.GetTreatmentLinkCommitMessage(treatmentLink))
            treatmentLink.Commit()

    def CommitTreatmentMappingTrees(self, mappingTreeDict):
        for treeList in list(mappingTreeDict.values()):
            for tree in treeList:
                node = tree.Root()
                self.CommitNodesRecursively(node, self.GetTreatmentMappingCommitMessage, self.newTreatmentMappings)

    def CommitAIMappingTrees(self, mappingTreeDict):
        for treeList in list(mappingTreeDict.values()):
            for tree in treeList:
                node = tree.Root()
                self.CommitNodesRecursively(node, self.GetAIMappingCommitMessage, self.newAIMappings)

    def CommitTAccountMappingTrees(self, mappingTreeDict):
        for treatmentLink, treeList in mappingTreeDict.items():
            for tree in treeList:
                node = tree.Root()
                self.CommitTAccountNodesRecursively(node, treatmentLink)

    def CommitNodesRecursively(self, node, commitMessageFunc, commitList):
        mapping = node.GetMapping()
        Utils.LogAlways(commitMessageFunc(mapping))
        mapping.Commit()
        commitList.Add(mapping)
        for child in node.Children():
            self.CommitNodesRecursively(child, commitMessageFunc, commitList)

    def CommitTAccountNodesRecursively(self, node, treatmentLink):
        mapping = node.GetMapping()
        mapping.TreatmentLink(treatmentLink)
        Utils.LogAlways("Updating taccount mapping '%s'" % mapping.Name())
        mapping.Commit()
        for child in node.Children():
            self.CommitTAccountNodesRecursively(child, treatmentLink)

    def CommitMappingTreeReferences(self, mappingsTreeDict):
        try:
            for treeList in list(mappingsTreeDict.values()):
                prevTopMapping = None
                for tree in treeList:
                    node = tree.Root()
                    mapping = node.GetMapping()
                    mapping.Next(None)
                    mapping.Previous(None)
                    mapping.Parent(None)
                    if prevTopMapping:
                        prevTopMapping.Next(mapping)
                        prevTopMapping.Commit()
                        mapping.Previous(prevTopMapping)
                    mapping.Commit()
                    self.CommitMappingNodeReferences(node)
                    prevTopMapping = mapping
        except Exception as e:
            raise Exception("An error occurred while committing references:\n%s" % str(e))

    def CommitMappingNodeReferences(self, parentMappingNode):
        prevMapping = None
        parentMapping = parentMappingNode.GetMapping()
        for childNode in parentMappingNode.Children():
            currentMapping = childNode.GetMapping()
            currentMapping.Parent(parentMapping)
            currentMapping.Next(None)
            if prevMapping:
                prevMapping.Next(currentMapping)
                prevMapping.Commit()
                currentMapping.Previous(prevMapping)
            currentMapping.Commit()
            prevMapping = currentMapping
            self.CommitMappingNodeReferences(childNode)

    def CommitReferencesForTreatmentMappings(self, mappingsDict):
        self.CommitPreviousAndNextReferences(mappingsDict, "treatment mappings")

    def CommitReferencesForAIMappings(self, mappingsDict):
        self.CommitPreviousAndNextReferences(mappingsDict, "accounting instruction mappings")

    def CommitReferencesForTAccountMappings(self, mappingsDict):
        self.CommitPreviousAndNextReferences(self, mappingsDict, "taccount mappings")

    def GetTreatmentLinkCommitMessage(self, treatmentLink):
        ai = treatmentLink.AccountingInstruction()
        book = treatmentLink.Book()
        treatment = treatmentLink.Treatment()
        commitMessage = "Creating new treatment link connecting accounting instruction %s and treatment %s in book %s" % (ai.Name(), treatment.Name(), book.Name())
        return commitMessage

    def GetTreatmentMappingCommitMessage(self, treatmentMapping):
        book = treatmentMapping.Book()
        oid = treatmentMapping.Oid()
        bookLink = treatmentMapping.BookLink()
        if bookLink:
            treatment = bookLink.Treatment()
            commitMessage = "Creating new treatment mapping '%d' in book '%s' for treatment '%s'" % (oid, book.Name(), treatment.Name())
        else:
            commitMessage = "Creating new treatment mapping '%d' in book '%s'" % (oid, book.Name())
        return commitMessage

    def GetAIMappingCommitMessage(self, aiMapping):
        oid = aiMapping.Oid()
        bookLink = aiMapping.BookLink()
        book = bookLink.Book()
        treatment = bookLink.Treatment()
        treatmentLink = aiMapping.TreatmentLink()

        if treatmentLink:
            ai = treatmentLink.AccountingInstruction()
            commitMessage = "Creating new accounting instruction mapping '%d' in book '%s' and treatment '%s' for accounting instruction '%s'" % (oid, book.Name(), treatment.Name(), ai.Name())
        else:
            commitMessage = "Creating new accounting instruction mapping '%d' in book '%s' and treatment '%s'" % (oid, book.Name(), treatment.Name())
        return commitMessage

    def DeleteOldTreatmentLinks(self, ):
        oldTreatmentLinks = acm.FTreatmentLink.Select("book = 0").AsArray()
        self.DeleteObjectsInList(oldTreatmentLinks)

    def DeleteObjectsInList(self, objList):
        pythonList = list()
        pythonList.extend(objList)
        for obj in pythonList:
            obj.Delete()

    def RevertChanges(self):
        self.DeleteNewTreatmentMappings()
        self.DeleteNewAIMappings()
        self.RestoreOldTAccountMappings()
        self.DeleteObjectsInList(self.newTreatmentLinks)

    def BackupClonesOfOriginalTAccountMappings(self):
        originalMappings = acm.FTAccountMapping.Select("").AsArray()
        for orgMapping in originalMappings:
            clone = orgMapping.Clone()
            self.clonedOriginalTAccountMappings.Add(clone)

    def RestoreOldTAccountMappings(self):
        for clonedMapping in self.clonedOriginalTAccountMappings:
            orgMapping = clonedMapping.Original()
            orgMapping.Apply(clonedMapping)
            orgMapping.Commit()

    def DeleteNewTreatmentMappings(self):
        self.RemoveMappingReferences(self.newTreatmentMappings)
        self.DeleteObjectsInList(self.newTreatmentMappings)

    def DeleteNewAIMappings(self):
        self.RemoveMappingReferences(self.newAIMappings)
        self.DeleteObjectsInList(self.newAIMappings)


    def DeleteOldMappings(self):
        oldTreatmentMappings = acm.FTreatmentMapping.Select("book = 0").AsArray()
        oldAIMappings = acm.FAccountingInstructionMapping.Select("bookLink = 0").AsArray()
        oldTAccountMappings = acm.FTAccountMapping.Select("treatmentLink = 0").AsArray()
        self.RemoveMappingReferences(oldTreatmentMappings)
        self.RemoveMappingReferences(oldAIMappings)
        self.RemoveMappingReferences(oldTAccountMappings)
        self.DeleteObjectsInList(oldTreatmentMappings)
        self.DeleteObjectsInList(oldAIMappings)
        self.DeleteObjectsInList(oldTAccountMappings)

    def RemoveMappingReferences(self, mappings):
        for mapping in mappings:
            mapping.Parent(None)
            mapping.Previous(None)
            mapping.Next(None)
            mapping.Commit()

def ael_main(dictionary):
    upgradeHandler = AccountingUpgradeHandler()
    upgradeHandler.RunUpgradeScript()
