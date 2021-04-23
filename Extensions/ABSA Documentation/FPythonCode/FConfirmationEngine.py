"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FConfirmationEngine

DESCRIPTION
    This module is used to extend the behaviour of the core FConfirmationEngine
    module.

    The following customisations have been done:

    - Addition of GetConfirmationOwnerTradeStrategy method to determine the strategy
      that should be used to select the confirmation owner trade.  A confirmation
      owner trade is the trade against which a confirmation is created.  This role is
      distinguished from the role of the trade against which an event occurred and
      triggered confirmation processing (referred to as the event trade).  Currently
      the following three strategies are supported:
      - Event Trade:
        - This is default strategy used when no override is specified for an
          event in FConfirmationParameters.eventToConfirmationOwnerTradeStrategyMap.
        - Its behaviour is the same as the core FConfirmationEngine logic, i.e.
          any confirmation will be created against the event trade.
      - Trx Trade Or Event Trade:
        - This strategy will select the TrxTrade trade to which the event trade
          is related should one exist.  If the event trade is not related to a
          TrxTrade then the event trade will be selected.
      - Simulated Trade:
        - This strategy will select a simulated trade that is used for owning
          multi-trade confirmations related to the event trade acquirer and
          counterparty.
    - Addition of GetEventsByConfirmationOwnerTrade method to determine which trades
      are the confirmation owner trades for each event triggered against a specified
      event trade.
    - Addition of GetEventsByConfirmationOwnerUnderlyingObject method to translate
      the output of GetEventsByConfirmationOwnerTrade to a dictionary of events by
      underlying object for use within the Create method.
    - Modification of Create method to add support for confirmation owner trades
      being possibly distinct from event trades.
    - Modification of SelectConfirmations method to only select existing confirmations
      for specified events (those 'owned' by a particular trade).

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-10-29                      Stuart Wilson           Loan Ops                Loan Notice Automation
2019-06-14      FAOPS-439       Cuen Edwards            Letitia Carboni         Refactor of support for creating confirmations against
                                                                                trades other than the event trade.
2019-10-30      FAOPS-439       Tawanda Mukhalela       Letitia Carboni         Aligned with upgrade changes.
2021-01-27      FAOPS-899       Joshua Mvelase          Wandile Sithole         Create a custom unique id for Demat confirmations
                                                                                and commit values to the confirmation add info
-----------------------------------------------------------------------------------------------------------------------------------------
"""

""" Compiled: 2019-05-28 12:54:12 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationEngine.py"
import sys
import traceback

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
from FConfirmationUnderlyingObject import CreateUnderlyingObject
from MultiTradeConfirmationOwnerProvider import MultiTradeConfirmationOwnerProvider
import FConfirmationParameters as ConfirmationParameters

simulatedTradeConfirmationOwnerProvider = MultiTradeConfirmationOwnerProvider()


class FConfirmationEngine(object):
    def __init__(self):

        self.__cancelPreReleasedConfirmations = False
        try:
            self.__cancelPreReleasedConfirmations = ConfirmationParameters.cancelPreReleasedConfirmations
        except Exception as error:
            Utils.LogAlways("Exception Error: %s" % error)
            traceback.print_exc(file=sys.stdout)

    def SatisfiesEvents(self, underlying, confirmationEventList):
        listOfEvents = []
        for i in confirmationEventList:
            if i.baseRule.IsSatisfiedBy(underlying.GetObject()):
                listOfEvents.append(i)
        return listOfEvents

    def SelectConfirmations(self, underlyingObject, events):
        eventNames = [event.eventName for event in events]
        confirmations = list()
        if underlyingObject.IsTrade():
            trade = underlyingObject.GetObject()
            for confirmation in trade.Confirmations():
                if not confirmation.IsNewestInConfirmationChain():
                    continue
                if confirmation.Type() == ConfirmationType.CANCELLATION:
                    continue
                if confirmation.EventChlItem().Name() not in eventNames:
                    continue
                confirmations.append(confirmation)

            if len(confirmations) == 0 and Utils.IsTopmostCorrectingTrade(trade):
                self.GetConfirmationsFromCorrectTradeHierarchy(trade, confirmations, eventNames)

        return confirmations

    def GetConfirmationsFromCorrectTradeHierarchy(self, trade, confirmations, eventNames):
        while trade.CorrectionTrade():
            for confirmation in acm.FConfirmation.Select('trade = %d' % trade.CorrectionTrade().Oid()):
                if not confirmation.IsNewestInConfirmationChain():
                    continue
                if confirmation not in confirmations:
                    continue
                if confirmation.EventChlItem().Name() not in eventNames:
                    continue
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
                if FConfirmationEngine.IsValidDematConfirmation(newConfirmation):
                    self.UpdateDematConfirmationUniqueId(newConfirmation)
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

    def UpdateDematConfirmationUniqueId(self, confirmation):
        dematIdTextObject = acm.FCustomTextObject['Demat_Confirmation_ID']    
        self.UpdateConfirmationDematIdAddInfo(confirmation, dematIdTextObject)
        self.IncrementDematId(dematIdTextObject)

    def IncrementDematId(self, dematIdTextObject):
        try:
            currentDematId = int(dematIdTextObject.Text())
            dematIdTextObject.Text(currentDematId + 1)
            dematIdTextObject.Commit()
        except Exception as error:
            Utils.LogAlways('Failed to increment Demat ID on text object {}'.format(str(error)))

    def UpdateConfirmationDematIdAddInfo(self, confirmation, dematIdTextObject):
        dematIdIncrement = int(dematIdTextObject.Text()) + 1
        confirmation.AdditionalInfo().Demat_ID(dematIdIncrement)

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
            if (newConfirmation == None and oldConfirmation.Type() == ConfirmationType.CANCELLATION):
                continue
            if self.compareXML(newConfirmation, oldConfirmation):
                continue
            if oldConfirmation and HelperFunctions.IsPastExpiryDay(oldConfirmation):
                Utils.LogVerbose('Confirmation %d will not be processed.\nExpiry day %s has been passed.'
                                 % (oldConfirmation.Oid(), oldConfirmation.ExpiryDay()))
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

    def Create(self, eventUnderlyingObject, confirmationEventList):
        if Utils.IsCorrectedTrade(eventUnderlyingObject.GetObject()):
            return
        Utils.LogVerbose('Event Trade: {trade_oid}'.format(
            trade_oid=eventUnderlyingObject.GetTrade().Oid()
        ))
        eventsByConfirmationOwnerUnderlyingObject = FConfirmationEngine.GetEventsByConfirmationOwnerUnderlyingObject(
            eventUnderlyingObject, confirmationEventList)
        acm.BeginTransaction()
        newConfirmations = list()
        oldConfirmations = list()
        for confirmationOwnerUnderlyingObject, events in list(eventsByConfirmationOwnerUnderlyingObject.items()):
            satisfiedEvents = self.SatisfiesEvents(eventUnderlyingObject, events)
            Utils.LogVerbose('Confirmation Owner Trade: {trade_oid}, Satisfied Events: {events}'.format(
                trade_oid=confirmationOwnerUnderlyingObject.GetTrade().Oid(),
                events=[event.eventName for event in satisfiedEvents]
            ))

            newConfirmationsForSatisfiedEvents = ConfirmationCreator.CreateConfirmation(
                confirmationOwnerUnderlyingObject, satisfiedEvents)
            Utils.LogVerbose('Created Confirmations For Satisfied Confirmation Owner Trade Events: {confirmations}'.format(
                confirmations=[confirmation.EventChlItem().Name() for confirmation in newConfirmationsForSatisfiedEvents]
            ))
            newConfirmations += newConfirmationsForSatisfiedEvents
            oldConfirmationsForAllEvents = self.SelectConfirmations(confirmationOwnerUnderlyingObject, events)
            oldConfirmations += oldConfirmationsForAllEvents
            Utils.LogVerbose('Existing Confirmations For All Confirmation Owner Trade Events: {confirmations}'.format(
                confirmations=[confirmation.EventChlItem().Name() for confirmation in oldConfirmationsForAllEvents]
            ))
        Utils.LogVerbose('The creator returned %s confirmations' % (str(len(newConfirmations))))
        Utils.LogVerbose('The selector returned %s confirmations' % (str(len(oldConfirmations))))
        matchingConfirmations = ConfirmationMatcher(newConfirmations, oldConfirmations).GetMatchedConfirmations()
        Utils.LogVerbose('The matcher returned %s confirmations' % (str(len(matchingConfirmations))))
        matchingConfirmations = self.RemoveUnwantedConfirmations(matchingConfirmations)
        commiterList = self.CreateCommiterList(matchingConfirmations)
        Utils.LogAlways('Updating or Creating %s confirmations' % (str(len(commiterList))))
        commiterList = self.CommitCommiterList(commiterList)

        if len(commiterList) > 0:
            try:
                acm.CommitTransaction()
            except Exception as error:
                acm.AbortTransaction()
                Utils.RaiseCommitException(error)
        else:
            acm.AbortTransaction()

        return commiterList

    @staticmethod
    def GetEventsByConfirmationOwnerUnderlyingObject(eventUnderlyingObject, confirmationEventList):
        """
        Gets the confirmation owner underlying objects used for each
        event triggered against a specified event underlying object.

        This is returned as a dictionary with each confirmation owner
        underlying object as a key against which the list of corresponding
        events is related.
        """
        eventsByConfirmationOwnerTrade = FConfirmationEngine.GetEventsByConfirmationOwnerTrade(
            eventUnderlyingObject.GetTrade(), confirmationEventList)
        eventsByConfirmationOwnerUnderlyingObject = dict()
        for confirmationOwnerTrade, events in list(eventsByConfirmationOwnerTrade.items()):
            Utils.LogVerbose('Confirmation Owner Trade: {trade_oid}, Owner For Events: {events}'.format(
                trade_oid=confirmationOwnerTrade.Oid(),
                events=[event.eventName for event in events]
            ))
            confirmationOwnerUnderlyingObject = CreateUnderlyingObject(confirmationOwnerTrade)
            eventsByConfirmationOwnerUnderlyingObject[confirmationOwnerUnderlyingObject] = events
        return eventsByConfirmationOwnerUnderlyingObject

    @staticmethod
    def GetEventsByConfirmationOwnerTrade(eventTrade, confirmationEventList):
        """
        Gets the confirmation owner trades used for each event triggered
        against a specified event trade.

        This is returned as a dictionary with each confirmation owner
        trade as a key against which the list of corresponding events
        is related.
        """
        eventsByConfirmationOwnerTrade = dict()
        for event in confirmationEventList:
            confirmationOwnerTrade = None
            confirmationOwnerTradeStrategy = FConfirmationEngine.GetConfirmationOwnerTradeStrategy(event)
            if confirmationOwnerTradeStrategy == 'Event Trade':
                # Generate confirmations against the trade on which the event occurred.
                confirmationOwnerTrade = eventTrade
            elif confirmationOwnerTradeStrategy == 'Trx Trade Or Event Trade':
                # Generate confirmations against the transaction reference trade (if present)
                # else fallback on the trade on which the event occurred.
                if eventTrade.TrxTrade() is None:
                    confirmationOwnerTrade = eventTrade
                else:
                    confirmationOwnerTrade = eventTrade.TrxTrade()
            elif confirmationOwnerTradeStrategy == 'Simulated Trade':
                # Generate confirmations against a simulated trade.
                confirmationOwnerTrade = simulatedTradeConfirmationOwnerProvider.provide_owner_trade(
                    eventTrade.Acquirer(), eventTrade.Counterparty())
            else:
                error_message = "Unsupported confirmation owner trade strategy '{strategy}' "
                error_message += "specified for event '{event}'."
                raise ValueError(error_message.format(
                    strategy=confirmationOwnerTradeStrategy,
                    event=event.eventName
                ))
            if confirmationOwnerTrade not in list(eventsByConfirmationOwnerTrade.keys()):
                eventsByConfirmationOwnerTrade[confirmationOwnerTrade] = list()
            eventsByConfirmationOwnerTrade[confirmationOwnerTrade].append(event)
        return eventsByConfirmationOwnerTrade

    @staticmethod
    def GetConfirmationOwnerTradeStrategy(event):
        """
        Get the strategy that should be used to select the confirmation
        owner trade (the trade against which a confirmation is created)
        for a specified event.
        """
        defaultStrategy = 'Event Trade'
        if not hasattr(ConfirmationParameters, 'eventToConfirmationOwnerTradeStrategyMap'):
            return defaultStrategy
        eventToConfirmationOwnerTradeStrategyMap = dict(ConfirmationParameters.eventToConfirmationOwnerTradeStrategyMap)
        return eventToConfirmationOwnerTradeStrategyMap.get(event.eventName, defaultStrategy)

    @staticmethod
    def IsValidDematConfirmation(confirmation):
        if not confirmation.Trade().Instrument().AdditionalInfo().Demat_Instrument():
            return False
        if confirmation.EventType() != 'Demat Match Request':
            return False
        if confirmation.MTMessages() != '598':
            return False
        return True
