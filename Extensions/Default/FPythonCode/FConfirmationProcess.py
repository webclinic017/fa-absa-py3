""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationProcess.py"

import acm

from FOperationsAMBAMessage import AMBAMessage
from FOperationsExceptions import AMBAMessageException, CommitException, InvalidHookException
from FOperationsEnums import SignOffStatus
from FConfirmationEnums import ConfirmationStatus, ConfirmationType
from FOperationsDocumentEnums import OperationsDocumentStatus
from FOperationsUtils import LogAlways, LogVerbose, GetEnum, SortByOid, IsCorrectedTrade, InitFromParameters

from FConfirmationCommitter import Committer
from FConfirmationUnderlyingObject import CreateUnderlyingObject
from FConfirmationSingletons import GetSingleton, ConfirmationPreventionRulesHandler
from FConfirmationCreator import FConfirmationCreator as ConfirmationCreator
from FConfirmationEngine import FConfirmationEngine as ConfirmationEngine
from FConfirmationEventFactory import FConfirmationEventFactory as ConfirmationEventFactory
from FConfirmationHookAdministrator import GetConfirmationHookAdministrator, ConfirmationHooks
from FConfirmationUpdate import ApplyConfirmation

from FConfirmationChecksum import CreateChecksum

try:
    import FConfirmationClientValidation as ClientValidation
except ImportError as ie:
    import FConfirmationClientValidationTemplate as ClientValidation

def ___AllDocumentsAreSentSuccessfully(dummyConfirmation):
    '''Confirmations have 1 document so True returned. '''
    return True

def UpdateStatusAfterOperationsDocument(status, confirmation):

    if confirmation and not confirmation.IsDeleted():
        if status == OperationsDocumentStatus.SENT_SUCCESSFULLY:
            if ___AllDocumentsAreSentSuccessfully(confirmation):
                confirmation.Status(ConfirmationStatus.PENDING_MATCHING)
                ConfirmationCreator.SetChaserCutoff(confirmation)

        elif status == OperationsDocumentStatus.SEND_FAILED:
            confirmation.Status(ConfirmationStatus.NOT_ACKNOWLEDGED)
            if confirmation.IsApplicableForSWIFT():
                confirmation.IsSwiftNAK(True)

        elif status == OperationsDocumentStatus.EXCEPTION:
            confirmation.Status(ConfirmationStatus.EXCEPTION)
            confirmation.IsInsufficientMessageData(True)

        elif status == OperationsDocumentStatus.GENERATED:
            if confirmation.Checksum() == "" and confirmation.Type() != ConfirmationType.CHASER:
                confirmationClone = acm.FConfirmation()
                confirmationClone.RegisterInStorage()
                ApplyConfirmation(confirmationClone, confirmation)
                confirmationClone.Owner(confirmation.Owner())
                confirmationClone.ConfirmationReference(None)
                confirmationClone.ChaserCutoff(0)
                confirmationClone.Type(ConfirmationType.DEFAULT)
                confirmation.Checksum(CreateChecksum(confirmationClone))

            confirmation.Status(ConfirmationStatus.PENDING_APPROVAL)
            if not confirmation.IsSignOffed():
                confirmation.SignOffStatus1(SignOffStatus.PENDING_APPROVAL)

        else:
            return

        confirmation.Status(GetNextConfirmationStatus(confirmation))
        try:
            Committer(confirmation).Commit()
        except CommitException as exceptionString:
            LogAlways('Commit failed in %s. %s' % (__OperationsDocumentUpdateProcessing.__name__, str(exceptionString)))


def __OperationsDocumentUpdateProcessing(ambaMessage):

    assert ambaMessage.GetNameOfUpdatedTable() == 'OPERATIONSDOCUMENT'
    tables = ambaMessage.GetTableAndChildTables()

    operationsDocumentTable = tables[0]

    try:
        confirmationId = int(operationsDocumentTable.GetAttribute('CONFIRMATION_SEQNBR').GetCurrentValue())
        status = operationsDocumentTable.GetAttribute('STATUS').GetCurrentValue()
    except AMBAMessageException as error:
        LogAlways('AMBAMessageException in %s: %s' % (__OperationsDocumentUpdateProcessing.__name__, str(error)))
        return
    confirmation = acm.FConfirmation[confirmationId]
    if confirmation:
        LogVerbose('Got a document with status %s for confirmation %s' % (status, confirmationId))
        UpdateStatusAfterOperationsDocument(status, confirmation.Clone())
    else:
        LogVerbose('Ignoring OperationsDocument for settlement')


def __GetConfirmationsAffectedByPartyUpdate(partyOid):
    baseQuery = acm.CreateFASQLQuery(acm.FConfirmation, 'or')
    baseQuery.AddAttrNode('Trade.Counterparty.Oid', 'EQUAL', int(partyOid))
    baseQuery.AddAttrNode('Trade.Acquirer.Oid', 'EQUAL', int(partyOid))

    query = acm.CreateFASQLQuery(acm.FConfirmation, 'AND')
    Today = acm.GetFunction('dateToday', 0)
    query.AddAttrNode('ExpiryDay', 'GREATER_EQUAL', Today())
    query.AddAttrNode('IsNewestInConfirmationChain', 'EQUAL', True)
    query.AddAttrNode('Type', 'NOT_EQUAL', GetEnum('ConfirmationType', ConfirmationType.CANCELLATION))

    orNode1 = query.AddOpNode('OR')
    orNode1.AddAttrNode('Status', 'EQUAL', GetEnum('ConfirmationStatus', ConfirmationStatus.NEW))
    orNode1.AddAttrNode('Status', 'EQUAL', GetEnum('ConfirmationStatus', ConfirmationStatus.AUTHORISED))
    orNode1.AddAttrNode('Status', 'EQUAL', GetEnum('ConfirmationStatus', ConfirmationStatus.EXCEPTION))
    orNode1.AddAttrNode('Status', 'EQUAL', GetEnum('ConfirmationStatus', ConfirmationStatus.MANUAL_MATCH))
    orNode1.AddAttrNode('Status', 'EQUAL', GetEnum('ConfirmationStatus', ConfirmationStatus.PENDING_DOCUMENT_GENERATION))
    orNode1.AddAttrNode('Status', 'EQUAL', GetEnum('ConfirmationStatus', ConfirmationStatus.PENDING_APPROVAL))

    confirmationsToUpdate = acm.FArray()
    for i in baseQuery.Select():
        if query.IsSatisfiedBy(i):
            confirmationsToUpdate.Add(i)
    return confirmationsToUpdate


def __PartyUpdateProcessing(ambaMessage):
    assert ambaMessage.GetNameOfUpdatedTable() == 'PARTY'
    assert ambaMessage.GetTypeOfUpdate() == 'UPDATE'

    tables = ambaMessage.GetTableAndChildTables()
    partyTables = AMBAMessage.GetTablesByName(tables, 'PARTY')
    assert len(partyTables) == 1
    partyTable = partyTables[0]
    ptyNbrAttribute = partyTable.GetAttribute('PTYNBR')

    confirmationResultSet = __GetConfirmationsAffectedByPartyUpdate(ptyNbrAttribute.GetCurrentValue())
    confirmationResultSet.SortByProperty('Trade.Oid', True)

    tempTrade = None
    confirmationEngine = ConfirmationEngine()
    for confirmation in confirmationResultSet:
        if (tempTrade       == None or
            tempTrade.Oid() != confirmation.Trade().Oid()):
            tempTrade = confirmation.Trade()
            try:
                confirmationEngine.Create(CreateUnderlyingObject(tempTrade), ConfirmationEventFactory.GetConfirmationEvents())
            except CommitException as err:
                LogAlways('%s: %s' % (__PartyUpdateProcessing.__name__, str(err)))
        else:
            continue

def RegenerateConfirmationsFromConfirmation(confirmation):
    import FConfirmationParameters as ConfirmationParameters

    InitFromParameters(ConfirmationParameters)
    confirmationEngine = ConfirmationEngine()
    trade = confirmation.Trade()
    confirmations = acm.FArray()

    if IsCorrectedTrade(trade):
        return confirmations
    confirmationTupleList = confirmationEngine.RegenerateCreate(CreateUnderlyingObject(trade), ConfirmationEventFactory.GetConfirmationEvents(), confirmation)

    for operationType, confirmation in confirmationTupleList:
        pair = acm.FPair()
        if operationType in ['Resended Confirmation', 'Amended Confirmation', 'Cancelled Confirmation']:
            pair.First('UPDATE')
        elif operationType in ['New', 'Cancellation', 'Amend', 'Resend']:
            pair.First('INSERT')
        elif operationType in ['Delete']:
            pair.First('DELETE')
        if confirmation:
            pair.Second(confirmation)
            confirmations.Add(pair)

    return confirmations

def GetTradesFromInstrument(instrument):
    for trade in instrument.Trades():
        yield trade

    for link in instrument.CombinationMaps():
        for trade in GetTradesFromInstrument(link.Combination()):
            yield trade

def GetConfirmationGeneratingObjects(fObject):
    objects = list()
    cprh = GetSingleton(ConfirmationPreventionRulesHandler)
    if fObject.IsKindOf(acm.FInstrument):
        for trade in GetTradesFromInstrument(fObject):
            cprh.FilterAndAddFObject(trade, objects)
    elif fObject.IsKindOf(acm.FTrade):
        cprh.FilterAndAddFObject(fObject, objects)
    elif fObject.IsKindOf(acm.FDealPackage):
        leadTrade = fObject.LeadTrade()
        if leadTrade != None:
            LogVerbose("Processing lead trade %d for deal package %d." % (leadTrade.Oid(), fObject.Oid()))
            cprh.FilterAndAddFObject(leadTrade, objects)
    hookAdmin = GetConfirmationHookAdministrator()
    tradesToBeProcessed = hookAdmin.HA_CallHook(ConfirmationHooks.GET_TRADES_TO_BE_PROCESSED, fObject)
    for aTrade in tradesToBeProcessed:
        cprh.FilterAndAddFObject(aTrade, objects)
    return objects

def __DefaultProcessing(obj):
    LogVerbose('Got ' + str(obj.Class().Name()) + ' with name ' + str(obj.Name() + \
              ' updated by user ' + obj.UpdateUser().Name()))

    fObjects = GetConfirmationGeneratingObjects(obj)
    fObjects.sort(SortByOid)
    numberObjects = len(fObjects)
    for obj in fObjects:
        LogVerbose("Processing %s %d, %d left in queue" % (obj.ClassName(), obj.Oid(), numberObjects - 1))
        numberObjects = numberObjects - 1
        try:
            ConfirmationEngine().Create(CreateUnderlyingObject(obj), ConfirmationEventFactory.GetConfirmationEvents())
        except CommitException as error:
            LogAlways('%s: %s' % (__DefaultProcessing.__name__, str(error)))

def ConfirmationProcess(msg, obj):
    ''' Main function for the confirmation process flow. '''
    try:
        if(obj):
            __DefaultProcessing(obj)
        else:
            ambaMessage = AMBAMessage(msg)

            if ambaMessage.GetNameOfUpdatedTable() == 'OPERATIONSDOCUMENT':
                if ambaMessage.GetTypeOfUpdate() == 'UPDATE' or ambaMessage.GetTypeOfUpdate() == 'INSERT':
                    __OperationsDocumentUpdateProcessing(ambaMessage)
            elif ambaMessage.GetNameOfUpdatedTable() == 'PARTY':
                if ambaMessage.GetTypeOfUpdate() == 'UPDATE':
                    __PartyUpdateProcessing(ambaMessage)
    except InvalidHookException as error:
        if obj:
            LogAlways("Failed to process {} object with id {}".format(obj.Class().Name(), obj.Oid()))
        else:
            LogAlways("Failed to process message: \n {}".format(msg.mbf_object_to_string()))
        LogAlways(error)

def GetNextConfirmationStatus(confirmation):
    status = confirmation.Status()
    if status == ConfirmationStatus.PENDING_APPROVAL:
        if confirmation.IsSignOffed():
            status = ConfirmationStatus.AUTHORISED
    if status == ConfirmationStatus.AUTHORISED:
        isSetToReleased = ClientValidation.IsSetToReleased(confirmation)
        if isSetToReleased == False:
            isSetToReleased = confirmation.Stp()
        if isSetToReleased == True:
            status = ConfirmationStatus.RELEASED
    return status
