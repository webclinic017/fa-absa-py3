""" Compiled: NONE NONE """

"""----------------------------------------------------------------------------
MODULE
    FSettlementMain - Module that subscribes to AMB messages.

    (c) Copyright 2008 by SunGard Front ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import acm
import amb
import time
import collections
import FOperationsAMBAMessage
from FOperationsAMBAMessage import AMBAMessageException
import ATSParameters as Params
import exceptions

try:
    import FOperationsUtils as Utils
except Exception, error:
    print "Failed to import FOperationsUtils, "  + str(error)

try:
    from ABSAFConfirmationXML import ABSAFConfirmationXML as FConfirmationXML
except Exception, error:
    print "Failed to import ABSAFConfirmationXML, "  + str(error)

try:
    import ABSADocumentStatusTransitions
except Exception, error:
    print "Failed to import ABSADocumentStatusTransitions, "  + str(error)

try:
    from ABSADataContainer import ABSADataContainer
except Exception, error:
    print "Failed to import ABSADataContainer, "  + str(error)



ambMsgNbr = 0
maxUpdateCollisions = 5
eventDeque = collections.deque()
nrOfTries  = 0
TRXNumber = 0
dbTables = ['CONFIRMATION',
            'OPERATIONSDOCUMENT']

class TridentMessage(object):
    def __init__(self, tridentDocumentStatus, confirmation, documentTridentID, documentOID):
        self.__documentStatus = tridentDocumentStatus
        self.__confirmation = confirmation
        self.__tridentID = documentTridentID
        self.__documentOID = documentOID
        self.__cpRef = None
        self.__XML = None

    def GetXML(self):
        return self.__XML

    def GetDocumentStatus(self):
        return self.__documentStatus

    def GetConfirmation(self):
        return self.__documentOID.Confirmation()
       
    def GetCPRef(self):
        return self.__cpRef

    def GetTridentID(self):
        return self.__tridentID

    def SetDocumentOID(self, documentOID):
        self.__documentOID = documentOID

    def SetDocumentStatus(self, documentStatus):
        self.__documentStatus = documentStatus

    def SetConfirmation(self, confirmation):
        self.__confirmation = confirmation

    def SetCPRef(self, cpRef):
        self.__cpRef = cpRef

    def SetTridentID(self, tridentID):
        self.__tridentID = tridentID

    def GetDocumentOID(self):
        return self.__documentOID


    def GetOperationsDocument(self):
        return self.__documentOID

    @staticmethod
    def CreateTridendMessageFromAMBA(ambaMsg):
        tables = ambaMsg.GetTableAndChildTables()
        OBTables = FOperationsAMBAMessage.AMBAMessage.GetTablesByName(tables, 'OperationsDocument')
        if len(OBTables) != 1:
            acm.Log("Failed to read amba message")
            return None

        OBTable = OBTables[0]
        try:
            tridentID = 0
            documentOID = None
            documentStatus = str(OBTable.GetAttribute('STATUS').GetCurrentValue())
            if OBTable.GetAttribute('DOCUMENT_ID'):
                if OBTable.GetAttribute('DOCUMENT_ID').GetCurrentValue() != 'None':
                    tridentID = OBTable.GetAttribute('DOCUMENT_ID').GetCurrentValue()

            if OBTable.GetAttribute('SEQNBR'):
                if OBTable.GetAttribute('SEQNBR').GetCurrentValue() != 'None':
                    documentOID = acm.FOperationsDocument[int(OBTable.GetAttribute('SEQNBR').GetCurrentValue())]

        except AMBAMessageException, ambaError:
            acm.Log("Failed to parse amba message:" + str(ambaError))
            return None
        if documentOID == None:
            acm.Log("Failed to get document OID")
            return None
        return TridentMessage(documentStatus, documentOID.Confirmation(), tridentID, documentOID)


class OperationsCommitter(object):

    def __init__(self):
        self.__objectsToCommit = list()

    def AddObject(self, newObject):
        self.__objectsToCommit.append(newObject)

    def Commit(self):
        try:
            acm.BeginTransaction()
            for i in self.__objectsToCommit:
                i.Commit()
            acm.CommitTransaction()
        except Exception, commitError:
            self.__RaiseCommitException(commitError)

    def __RaiseCommitException(self, errorString):
        if (str(errorString).find("Update collision") != -1):
            msg = 'Error while committing operations document or confirmation! An update collision occurred.'
            acm.Log(msg)
            raise UpdateCollisionException, errorString
        else:
            msg = 'Error while committing operations document or confirmation! Cause: %s.' %  errorString
            acm.Log(msg)
            raise Exception, errorString


class UpdateCollisionException(exceptions.Exception):
    def init(self, args = None):
        self.args = args


def HandleDocumentEvents(ambaMsg, message):
    tridentMessage = TridentMessage.CreateTridendMessageFromAMBA(ambaMsg)

    if tridentMessage == None:
        acm.Log("Failed to read amba message for OperationsDocument")
        return
    confirmation = tridentMessage.GetConfirmation()
    documentStatus = tridentMessage.GetDocumentStatus()
    document = tridentMessage.GetOperationsDocument()
    isUpdateCollision = False
    if not confirmation or not document:
        return isUpdateCollision

    ABSADataContainer.SetConfirmation(confirmation)
    acm.Log("Status of the Document = " + str(documentStatus))
    acm.Log("Document OID = " + str(document.Oid()))
    acm.Log("Status of the Confirmation = " + str(confirmation.Status()))
    acm.Log("Confirmation Oid = " + str(confirmation.Oid()))
    operationsCommitter = OperationsCommitter()

    if documentStatus == "Awaiting Dispatch":
        ABSADocumentStatusTransitions.Generated(confirmation, document, operationsCommitter)
    elif documentStatus == "Dispatched":
        ABSADocumentStatusTransitions.Sending(confirmation, document, operationsCommitter)
    elif documentStatus == "Counterparty To Produce":
        ABSADocumentStatusTransitions.CounterpartyToProduce(confirmation, document, operationsCommitter)
    elif documentStatus == "Document Not Required(Pre Release)":
        ABSADocumentStatusTransitions.DocumentNotRequired(confirmation, document, operationsCommitter)
    elif documentStatus == "Matched":
        ABSADocumentStatusTransitions.Matched(confirmation, document, operationsCommitter, tridentMessage.GetTridentID())
    elif documentStatus == "Document Not Required(Post Release)":
        ABSADocumentStatusTransitions.DocumentNotRequiredPostRelease(confirmation, document, operationsCommitter)
    elif documentStatus == "Mismatched":
        ABSADocumentStatusTransitions.MatchFailed(confirmation, document, operationsCommitter)
    elif documentStatus == "Acknowledged":
        ABSADocumentStatusTransitions.AffirmationAcknowledged(confirmation, document, operationsCommitter, tridentMessage.GetTridentID())
    elif documentStatus == "Financials Agreed":
        ABSADocumentStatusTransitions.AffirmationFinancialsAgreed(confirmation, document, operationsCommitter, tridentMessage.GetTridentID())
    elif documentStatus == "Counterparty Does Not Recognise Deal":
        ABSADocumentStatusTransitions.AffirmationCounterpartyDoesNotRecogniseDeal(confirmation, document, operationsCommitter, tridentMessage.GetTridentID())
    elif documentStatus == "Terms Disputed":
        ABSADocumentStatusTransitions.AffirmationTermsDisputed(confirmation, document, operationsCommitter, tridentMessage.GetTridentID())
    elif documentStatus == "CounterpartyReference":
        ABSADocumentStatusTransitions.UpdateCPRefAddInfo(confirmation, document, operationsCommitter, tridentMessage.GetTridentID())

    try:
        operationsCommitter.Commit()
    except UpdateCollisionException, exceptionString:
        isUpdateCollision = True
        acm.Log(exceptionString)
    except Exception, exceptionString:
        acm.Log('Failed to Commit:' + str(exceptionString) )

    return isUpdateCollision


def event_cb(channel, event, arg):
    ''' Main callback function for AMB messages. The events are placed in a
    queue that is then processed by work_cb. '''
    Utils.LogTrace()

    global ambMsgNbr

    eventString = amb.mb_event_type_to_string(event.event_type)
    if eventString == 'Status':
        try:
            ambMsgNbr = int(event.status.status)
        except ValueError:
            ambMsgNbr = 0
    elif eventString == 'Message':
        ambMsgNbr += 1
        eventDeque.append((amb.mb_copy_message(event.message), channel, ambMsgNbr))
        Utils.Log(False, 'Added event, %d in queue.' % len(eventDeque))
    else:
        Utils.Log(True, 'Unknown event %s' % eventString)


def RemoveOperationsDocument(settlementOrConfirmation):
    Utils.LogTrace()
    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    orNode = query.AddOpNode('OR')

    if settlementOrConfirmation.IsKindOf(acm.FSettlement):
        query.AddAttrNode('Settlement.Oid', 'EQUAL', settlementOrConfirmation.Oid())
    if settlementOrConfirmation.IsKindOf(acm.FConfirmation):
        query.AddAttrNode('Confirmation.Oid', 'EQUAL', settlementOrConfirmation.Oid())
    orNode.AddAttrNode('Status', 'EQUAL', 'Exception')
    orNode.AddAttrNode('Status', 'EQUAL', 'Send failed')
    orNode.AddAttrNode('Status', 'EQUAL', 'Generated')
    orNode.AddAttrNode('Status', 'EQUAL', 'Pending generation')

    for operationsDocument in query.Select():
        operationsDocument.Delete()


def ZlibAndHex(data):
    '''Converts input data to compressed zlib format and then hex.'''
    #return data.encode("zlib").encode("hex")
    import zlib
    return zlib.compress(data, 9).encode("hex")


def ZlibToXml(data):
    '''Converts zlib compressed data to xml string format. '''
    ret = data
    try:
        ret = data.decode("zlib")
    except Exception, e:
        acm.Log(e)
    return ret

def CreateOperationsDocument(documentStatus, documentId, \
                             statusExplanation, documentType, \
                             settlementOrConfirmation):
    Utils.LogTrace()
    try:
        document = acm.FOperationsDocument()
        document.Commit()
        ABSADataContainer.SetDocument(document)
        document.Status(documentStatus)
        document.DocumentId(documentId)
        document.StatusExplanation(statusExplanation)
        document.Type(documentType)

        if settlementOrConfirmation.IsKindOf(acm.FSettlement):
            document.Settlement(settlementOrConfirmation)
        elif settlementOrConfirmation.IsKindOf(acm.FConfirmation):
            document.Confirmation(settlementOrConfirmation)

        XML = FConfirmationXML(settlementOrConfirmation).GenerateXmlFromTemplate()
        if XML == "":
            document.Status('Exception')
            document.StatusExplanation('Failed to generate XML')
        elif XML == "InvalidEventException":
            document.Status('Exception')
            document.StatusExplanation('Invalid event')
        else:
            XMLCompressed = ZlibAndHex(XML)
            document.Data(XMLCompressed)
            document.Size(len(XMLCompressed))
            Utils.Log(True, "The size of the XML Compressed = " +str(len(XMLCompressed)))
        document.Commit()

    except Exception, exception:
        Utils.Log(True, "Failed to create FOperationsDocument: "  + str(exception))

def ChangeStatusOfDocumentsToReleased(confirmation):
    Utils.LogTrace()

    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    query.AddAttrNode('Confirmation.Oid', 'EQUAL', confirmation.Oid())

    for document in query.Select():
        document.Status('Sent successfully')
        document.Commit()

def CallTridentGenerateDocument():
    return "Pending Generation", ""

def IsSwiftConfirmation(confirmation):
    return confirmation.Transport == 'NetWork' and confirmation.Template == 'SWIFT'

def ConfirmationProcessing(message):
    Utils.LogTrace()
    messageAsString = message.mbf_object_to_string()
    isUpdateCollision = False
    obj = None

    try:
        obj = acm.AMBAMessage.CreateSimulatedObject(messageAsString)
    except Exception, error:
        Utils.Log(True, 'Error in acm.AMBAMessage.ConfirmationProcessing: %s. \nAMBA message:\n %s' % \
                 (error, messageAsString))

    if obj and obj.IsKindOf(acm.FConfirmation):
        confirmation = obj
    else:
        return False
    if not obj:
        Utils.Log(True, 'No object found in DocumentationProcess')
        # The object was deleted and was not found by CreateSimulatedObject
        return isUpdateCollision
    ABSADataContainer.SetConfirmation(confirmation)
    Utils.Log(True, 'Got ' + str(obj.Class().Name()) + ' with name ' + str(obj.Name() + \
              ' updated by user ' + obj.UpdateUser().Name()))

    if confirmation.Status() == 'Pending Document Generation':
        Utils.Log(False, 'Creating document for confirmation %d.' % confirmation.Oid())
        RemoveOperationsDocument(confirmation)
        documentStatus, statusExplanation = CallTridentGenerateDocument()

        if IsSwiftConfirmation(confirmation):
            documentType = 'SWIFT'
        else:
            documentType = 'LONGFORM'
        CreateOperationsDocument(documentStatus, confirmation.Oid(), statusExplanation, documentType, confirmation)
    elif  confirmation.Status() ==  'Released':
        ChangeStatusOfDocumentsToReleased(confirmation)

    try:
        acm.AMBAMessage.DestroySimulatedObject(obj)
    except Exception, error:
        Utils.Log(True, 'Error in acm.AMBAMessage.DestroySimulatedObject: %s. \nAMBA message:\n %s' % \
                 (error, messageAsString))

    return isUpdateCollision


def GetTRXNumberFromAmbaMessage(message):
    inner = message.mbf_first_object()
    field = ''
    ABSADataContainer.SetTRXNumber(0)
    while inner:
        field = inner.mbf_get_name()
        value = inner.mbf_get_value()
        if field == 'TXNBR':
            ABSADataContainer.SetTRXNumber(value)
        inner = message.mbf_next_object()


def DocumentationProcess(message):
    ''' Main function for the document process flow. '''
    Utils.LogTrace()

    isUpdateCollision = False
    ambaMessage = FOperationsAMBAMessage.AMBAMessage(message)
    GetTRXNumberFromAmbaMessage(message)
    if ambaMessage.GetNameOfUpdatedTable() == 'OPERATIONSDOCUMENT':
        isUpdateCollision = HandleDocumentEvents(ambaMessage, message)
    else:
        isUpdateCollision = ConfirmationProcessing(message)

    return isUpdateCollision


def work():
    ''' Process the event queue. '''
    if len(eventDeque) == 0:
        return

    Utils.LogTrace()
    global nrOfTries
    queueMember = eventDeque.popleft()
    (eventCopy, channel, msgNbr) = queueMember
    if (len(eventDeque) > 0):
        Utils.Log(True, '>>> Processing event, %d in queue.' % len(eventDeque))
    buf = amb.mbf_create_buffer_from_data(eventCopy.data_p)
    msg = buf.mbf_read()
    isUpdateCollision = DocumentationProcess(msg)
    if isUpdateCollision: #An update collision occurred
        nrOfTries = nrOfTries + 1
        eventDeque.appendleft(queueMember) # reprocess the message
        Utils.Log(True, '>>> Event re-entered in the queue (try #%d). %d members in the queue.' %
            (nrOfTries, len(eventDeque)))
    else:
        nrOfTries = 0
    amb.mb_queue_accept(channel, eventCopy, str(msgNbr))
    msg.mbf_destroy_object()
    buf.mbf_destroy_buffer()
    print('>>> Waiting for events...\n')


def start():
    try:
        ''' Set up AMB connection. '''
        Utils.LogTrace()
        Utils.Log(False, 'Document ATS start-up commenced at %s' % (time.ctime()))

        try:
            Utils.Log(False, 'Setting up AMB subscriptions...')
            amb.mb_init(Params.ambAddress)
            reader = amb.mb_queue_init_reader(Params.documentationReceiverMBName, event_cb, None)
            for dbTable in dbTables:
                subscriptionString = Params.receiverSource + '/' + dbTable
                amb.mb_queue_enable(reader, subscriptionString)
            Utils.Log(True, 'Documentation ATS start-up completed.')

        except RuntimeError, runtimeError:
            errStr = 'Documentation ATS start-up failed, %s' % runtimeError
            Utils.Log(True, errStr)

        print('>>> Waiting for events...\n')
        amb.mb_poll()
    except Exception, error:
        print "Failed to run start, "  + str(error)


def stop():
    ''' Stop. '''
    Utils.LogTrace()

    return


def status():
    ''' Status. '''
    Utils.LogTrace()

    return
