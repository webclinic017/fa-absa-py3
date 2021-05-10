""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationEngine.py"
import acm
from FConfirmationHelperFunctions import FConfirmationHelperFunctions as HelperFunctions
from FConfirmationCreator import FConfirmationCreator as ConfirmationCreator
from FConfirmationMatcher import ConfirmationMatcher
import FOperationsUtils as Utils
from FConfirmationSingletons import GetSingleton, ConfirmationPreventionRulesHandler
from FConfirmationCommitter import Committer
from FOperationsDocumentEnums import OperationsDocumentStatus
from FConfirmationEnums import ConfirmationStatus, ConfirmationType
from FConfirmationUpdate import ApplyConfirmation
from FConfirmationHookAdministrator import ConfirmationHooks, GetConfirmationHookAdministrator

class FConfirmationEngine(object):
    def __init__(self):
        import FConfirmationParameters as ConfirmationParameters

        self.__cancelPreReleasedConfirmations = False
        try:
            self.__cancelPreReleasedConfirmations = ConfirmationParameters.cancelPreReleasedConfirmations
        except Exception:
            pass

    def SatisfiesEvents(self, underlying, confirmationEventList):
        listOfEvents = []
        for i in confirmationEventList:
            if i.baseRule.IsSatisfiedBy(underlying.GetObject()):
                listOfEvents.append(i)
        return listOfEvents

    def SelectConfirmations(self, underlyingObject):
        confirmations = list()
        if underlyingObject.IsTrade():
            trade = underlyingObject.GetObject()
            for confirmation in trade.Confirmations():
                if confirmation.IsNewestInConfirmationChain() and confirmation.Type() != ConfirmationType.CANCELLATION:
                    confirmations.append(confirmation.Clone())
            if len(confirmations) == 0 and Utils.IsTopmostCorrectingTrade(trade):
                self.GetConfirmationsFromCorrectTradeHierarchy(trade, confirmations)
        return confirmations

    def GetConfirmationsFromCorrectTradeHierarchy(self, trade, confirmations):
        while trade.CorrectionTrade():
            for confirmation in acm.FConfirmation.Select('trade = %d' % trade.CorrectionTrade().Oid()):
                if confirmation.IsNewestInConfirmationChain() and confirmation not in confirmations:
                    confirmations.append(confirmation.Clone())
            if trade.CorrectionTrade().Oid() == trade.Oid():
                break
            trade = trade.CorrectionTrade()

    def CreateCancellationConfirmation(self, cancelledConfirmation):
        cancellationConfirmation = acm.FConfirmation()
        cancellationConfirmation.RegisterInStorage()
        ApplyConfirmation(cancellationConfirmation, cancelledConfirmation)
        cancellationConfirmation.Owner(cancelledConfirmation.Owner())
        cancellationConfirmation.Status(ConfirmationStatus.NEW)
        cancellationConfirmation.ChaserCutoff(None)
        cancellationConfirmation.EventChlItem(cancelledConfirmation.EventChlItem())
        cancellationConfirmation.SetTypeAndUpdateDocumentData(ConfirmationType.CANCELLATION)
        cancellationConfirmation.ConfirmationReference(cancelledConfirmation)
        cancellationConfirmation.Validate()

        return cancellationConfirmation

    def CreateAmendmentConfirmation(self, newConfirmation, oldConfirmation, committerList):
        newConfirmation.CopyAndCommitDiary(oldConfirmation)

        if oldConfirmation.IsApplicableForSWIFT() and oldConfirmation.Status() == ConfirmationStatus.NOT_ACKNOWLEDGED:
            newConfirmation.SetTypeAndUpdateDocumentData(ConfirmationType.RESEND)
            newConfirmation.ConfirmationReference(oldConfirmation)
            newConfirmation.ExpiryDay(oldConfirmation.ExpiryDay())
            committerList.append(('Resend', newConfirmation))
            committerList.append(("Resended Confirmation", oldConfirmation))
        elif oldConfirmation.IsPreRelease():
            if oldConfirmation.ConfirmationReference():
                newConfirmation.ConfirmationReference(oldConfirmation.ConfirmationReference())
            expiryDay = oldConfirmation.ExpiryDay()
            newConfirmation.SetTypeAndUpdateDocumentData(oldConfirmation.Type())
            ApplyConfirmation(oldConfirmation, newConfirmation)
            oldConfirmation.Owner(newConfirmation.Owner())
            oldConfirmation.ExpiryDay(expiryDay)
            committerList.append(('Amended Confirmation', oldConfirmation))
        else:
            newConfirmation.SetTypeAndUpdateDocumentData("Amendment")
            newConfirmation.ConfirmationReference(oldConfirmation)
            newConfirmation.ExpiryDay(oldConfirmation.ExpiryDay())
            committerList.append(('Amend', newConfirmation))
            committerList.append(("Amended Confirmation", oldConfirmation))


    def IsCancellationAndNewInsteadOfAmendment(self, confirmation, newConfirmation):
        cancellationAndNewInsteadOfAmendment = False
 
        hookAdmin = GetConfirmationHookAdministrator()
        if hookAdmin.HA_IsCustomHook(ConfirmationHooks.CANCELLATION_AND_NEW_INSTEAD_OF_AMENDMENT):
            from FConfirmationXML import FConfirmationXML
            newXML = FConfirmationXML(newConfirmation).GenerateXmlFromTemplate()
            cancellationAndNewInsteadOfAmendment = hookAdmin.HA_CallHook(ConfirmationHooks.CANCELLATION_AND_NEW_INSTEAD_OF_AMENDMENT, confirmation, newConfirmation, newXML)

        else:
            import FConfirmationParameters as ConfirmationParameters

            try:
                if confirmation.IsApplicableForSWIFT():
                    cancellationAndNewInsteadOfAmendment = ConfirmationParameters.cancellationAndNewInsteadOfAmendmentSWIFT
                else:
                    cancellationAndNewInsteadOfAmendment = ConfirmationParameters.cancellationAndNewInsteadOfAmendmentFreeForm
            except AttributeError:
                Utils.LogAlways("Could not find the parameter called 'cancellationAndNewInsteadOfAmendment' in FConfirmationParameters")

        return cancellationAndNewInsteadOfAmendment

    def AddNewConfirmation(self, newConfirmation, confirmations):
        confirmations.append(("New", newConfirmation))

    def AddCancelOrDelete(self, oldConfirmation, confirmations):
        cprh = GetSingleton(ConfirmationPreventionRulesHandler)
        if cprh.IsPreventConfirmationCancellation(oldConfirmation) == False:
            if (oldConfirmation.Status() in HelperFunctions.postReleasedStatuses) or (oldConfirmation.ConfirmationReference()) or self.__cancelPreReleasedConfirmations:
                confirmations.append(("Cancellation", self.CreateCancellationConfirmation(oldConfirmation)))
                confirmations.append(("Cancelled Confirmation", oldConfirmation))
            else:
                confirmations.append(("Delete", oldConfirmation))

    def CreateCommiterList(self, confirmationList):
        confirmations = list()
        for newConfirmation, oldConfirmation in confirmationList:
            if oldConfirmation == None: #A new confirmation
                self.AddNewConfirmation(newConfirmation, confirmations)
            elif newConfirmation == None: #Create a Cancellation confirmation
                self.AddCancelOrDelete(oldConfirmation, confirmations)
            else:
                if HelperFunctions.IsPostReleasedConfirmation(oldConfirmation) and self.IsCancellationAndNewInsteadOfAmendment(oldConfirmation, newConfirmation):
                    self.AddNewConfirmation(newConfirmation, confirmations)
                    self.AddCancelOrDelete(oldConfirmation, confirmations)
                else:
                    rulesHandler = GetSingleton(ConfirmationPreventionRulesHandler)
                    if rulesHandler.IsPreventConfirmationAmendment(oldConfirmation) == False:
                        self.CreateAmendmentConfirmation(newConfirmation, oldConfirmation, confirmations)
        return confirmations

    def DeleteConfirmation(self, confirmation):
        if confirmation.IsPreRelease():
            operationsDocuments = confirmation.Documents()
            confirmations = confirmation.Confirmations()
            externalObjects = confirmation.ExternalObjects()

            if len(confirmations) == 0:
                for operationsDocument in operationsDocuments:
                    if operationsDocument.Status() != OperationsDocumentStatus.SENT_SUCCESSFULLY:
                        Committer(operationsDocument).Delete()
                for externalObject in externalObjects:
                    for child in externalObject.ChildrenDepthFirst():
                        Committer(child).Delete()
                    Committer(externalObject).Delete()
                Committer(confirmation).Delete()
            else:
                Utils.LogAlways('References to confirmation %d exist, confirmation could not be deleted, will be set to void instead.' % confirmation.Oid())
                confirmationClone = confirmation.Clone()
                confirmationClone.RegisterInStorage()
                confirmationClone.Status(ConfirmationStatus.VOID)
                Committer(confirmationClone).Commit()
        else:
            if confirmation.ConfirmationReference():
                if confirmation.IsPreRelease():
                    confirmationClone = confirmation.Clone()
                    confirmationClone.RegisterInStorage()
                    Committer(confirmationClone).Commit()


    def CommitCommiterList(self, commiterList):
        commitedConfirmations = list()
        for newConfirmation, oldConfirmation in commiterList:
            commitedConfirmations.append(oldConfirmation)
            if newConfirmation == 'Delete':
                self.DeleteConfirmation(oldConfirmation)
            else:
                Committer(oldConfirmation).Commit()
        return commitedConfirmations

    def compareXML(self, newConfirmation, originalConfirmation):
        if originalConfirmation == None:
            return False
        if newConfirmation == None:
            return False
        if originalConfirmation.Checksum() == '':
            return False

        if str(originalConfirmation.Checksum()) == str(newConfirmation.Checksum()):
            return True
        return False

    def RemoveUnwantedConfirmations(self, confirmationTupleList):
        newConfirmationTupleList = list()
        for newConfirmation, oldConfirmation in confirmationTupleList:
            if (newConfirmation == None and
                oldConfirmation.Type() == ConfirmationType.CANCELLATION):
                continue
            if self.compareXML(newConfirmation, oldConfirmation):
                continue
            if oldConfirmation and HelperFunctions.IsPastExpiryDay(oldConfirmation):
                Utils.LogVerbose('Confirmation %d will not be processed.\nExpiry day %s has been passed.' % (oldConfirmation.Oid(), oldConfirmation.ExpiryDay()))
                continue
            if (newConfirmation and oldConfirmation and
                oldConfirmation.Status() == ConfirmationStatus.HOLD):
                Utils.LogVerbose('Confirmation %d in status Hold. Will not be updated.' % oldConfirmation.Oid())
                continue
            newConfirmationTupleList.append((newConfirmation, oldConfirmation))
        return newConfirmationTupleList 

    def SameSourceConfirmation(self, newConfirmation, originalConfirmation):
        return newConfirmation.EventChlItem() == originalConfirmation.EventChlItem() and \
               newConfirmation.Receiver() == originalConfirmation.Receiver() and \
               newConfirmation.Subject() == originalConfirmation.Subject()

    def FilterOutOnlyConnected(self, confirmationTupleList, originalConfirmation):
        newConfirmationTupleList = list()
        for newConfirmation, oldConfirmation in confirmationTupleList:
            if (newConfirmation and self.SameSourceConfirmation(newConfirmation, originalConfirmation)) or \
             (oldConfirmation and self.SameSourceConfirmation(oldConfirmation, originalConfirmation)):
                newConfirmationTupleList.append((newConfirmation, oldConfirmation))
        return newConfirmationTupleList

    def RegenerateCreate(self, underlyingObject, confirmationEventList, confirmation):
        satisfiedEvents = self.SatisfiesEvents(underlyingObject, confirmationEventList)
        newConfirmations = ConfirmationCreator.CreateConfirmation(underlyingObject, satisfiedEvents)
        matchingConfirmations = ConfirmationMatcher(newConfirmations, [confirmation]).GetMatchedConfirmations()
        newOldPair = self.FilterOutOnlyConnected(matchingConfirmations, confirmation)
        committerList = self.CreateCommiterList(newOldPair)
        Utils.LogVerbose('Updating or Creating %s confirmations' % (str(len(committerList))))
        return committerList

    def Create(self, underlyingObject, confirmationEventList):

        if Utils.IsCorrectedTrade(underlyingObject.GetObject()):
            return
        SatisfiedEvents = self.SatisfiesEvents(underlyingObject, confirmationEventList)
        acm.BeginTransaction()
        try:
            newConfirmations = ConfirmationCreator.CreateConfirmation(underlyingObject, SatisfiedEvents)
            Utils.LogVerbose('The creator returned %s confirmations' % (str(len(newConfirmations))))
            oldConfirmations = self.SelectConfirmations(underlyingObject)
            Utils.LogVerbose('The selector returned %s confirmations' % (str(len(oldConfirmations))))
            matchingConfirmations = ConfirmationMatcher(newConfirmations, oldConfirmations).GetMatchedConfirmations()
            Utils.LogVerbose('The matcher returned %s confirmations' % (str(len(matchingConfirmations))))
            matchingConfirmations = self.RemoveUnwantedConfirmations(matchingConfirmations)
            commiterList = self.CreateCommiterList(matchingConfirmations)
            Utils.LogAlways('Updating or Creating %s confirmations' % (str(len(commiterList))))
            commiterList = self.CommitCommiterList(commiterList)
        except Exception as e:
            acm.AbortTransaction()
            raise e

        if len(commiterList) > 0:
            try:
                acm.CommitTransaction()
            except Exception as error:
                acm.AbortTransaction()
                Utils.RaiseCommitException(error)
        else:
            acm.AbortTransaction()
        return commiterList


