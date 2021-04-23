"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FOperationsDocumentProcess

DESCRIPTION
    This module is used to extend the behaviour of the core FOperationsDocumentProcess
    module.

    The following customisations have been done:

    - Addition of ShouldProcessViaContingencyPlan function to determine whether or
      not an object should be processed via the payment contingency plan.
    - Addition of ContingencyPlanCreateDocuments function to create documents via
      the payment contingency plan.
    - Addition of CoreCreateDocuments function to extract default/core behaviour
      for creating documents out into a separate method.
    - Modification of CreateDocuments to replace default/core behaviour with logic
      to route creation of documents to either ContingencyPlanCreateDocuments (if
      enabled and the object is a qualifying settlement) or CoreCreateDocuments (in
      all other cases).
    - Addition of ContingencyPlanGetDocumentsToSend function to get documents to
      send via the payment contingency plan.
    - Addition of CoreGetDocumentsToSend function to extract default/core behaviour
      for getting documents to send out into a separate method.
    - Modification of GetDocumentsToSend to replace default/core behaviour with logic
      to route getting documents to send to either ContingencyPlanGetDocumentsToSend
      (if enabled and the object is a qualifying settlement) or CoreGetDocumentsToSend
      (in all other cases).
    - Addition of ContingencyPlanReleaseDocument function to release a document via
      the payment contingency plan.
    - Addition of CoreReleaseDocument function to extract default/core behaviour
      for releasing a document out into a separate method.
    - Modification of ReleaseDocument to replace default/core behaviour with logic
      to route releasing of a document to either ContingencyPlanReleaseDocument (if
      enabled and the object is a qualifying settlement) or CoreReleaseDocument (in
      all other cases).
    - Modification of DefaultProcessing to only check whether or not an object should
      be processed by SwiftWriter if it isn't eligible to be processed via the payment
      contingency plan.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-03-23      FAOPS-681       Cuen Edwards            Linda Breytenbach       Initial override for payment contingency plan.
2020-06-08      FAOPS-808       Cuen Edwards            Linda Breytenbach       Changes to allow payment contingency plan to work with
                                                                                SwiftWriter.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

""" Compiled: 2018-12-05 17:44:23 """

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentProcess.py"
import acm
import amb
import xml.dom.minidom
import FOperationsUtils as Utils
import FConfirmationDocXMLSpecifier as XmlConfDocSpecifier
import FConfirmationSwiftXMLSpecifier as XmlConfSwiftSpecifier
import FSettlementSwiftXMLSpecifier as XmlSettleSwiftSpecifier
import FOperationsDocumentService
import PaymentContingencyPlanGeneral
from FOperationsDocumentXSLTransformer import XSLTransformer, XSLTransformerException
from FOperationsDocumentHookAdministrator import OperationsDocumentHooks, GetHookAdministrator
from FSettlementEnums import SettlementStatus
from FOperationsDocumentEnums import OperationsDocumentStatus, OperationsDocumentType
from FConfirmationEnums import ConfirmationStatus
from FDocumentationCompression import ZlibAndHex
from FSwiftMessageTypeCalculator import Calculate
from FSwiftServiceSelector import UseSwiftWriterForMessage
from FSwiftExceptions import SwiftWriterAPIException


def ShouldDocumentsBeDeleted(fObject):
    if fObject.IsKindOf(acm.FSettlement):
        if (fObject.IsPreReleased() and IsMissingMTDocument(fObject)) or fObject.Status() in [SettlementStatus.VOID, SettlementStatus.RELEASED, SettlementStatus.PENDING_CANCELLATION]:
            return True
    if fObject.IsKindOf(acm.FConfirmation):
        if fObject.Status() in [ConfirmationStatus.MANUAL_MATCH, ConfirmationStatus.PENDING_DOCUMENT_GENERATION]:
            return True
    return False


def IsMissingMTDocument(fObject):
    isMissing = True
    mt = fObject.MTMessages()

    if fObject.Status() == SettlementStatus.PENDING_CANCELLATION and mt in ['292', '192']:
        return isMissing

    for document in fObject.Documents():
        if (mt == str(document.SwiftMessageType())):
            isMissing = False
    return isMissing


def InDocumentCreationStatus(fObject):
    if fObject.IsKindOf(acm.FSettlement):
        if fObject.Status() in [SettlementStatus.RELEASED, SettlementStatus.PENDING_CANCELLATION]:
            return True
    if fObject.IsKindOf(acm.FConfirmation):
        if fObject.Status() == ConfirmationStatus.PENDING_DOCUMENT_GENERATION:
            return True
    return False


def InSendDocumentStatus(fObject):
    if fObject.IsKindOf(acm.FSettlement):
        if fObject.Status() in [SettlementStatus.RELEASED, SettlementStatus.PENDING_CANCELLATION]:
            return True
    if fObject.IsKindOf(acm.FConfirmation):
        if fObject.Status() == ConfirmationStatus.RELEASED:
            return True
    return False


def InOperationsDocumentCreationStatus(fObject):
    if fObject.IsKindOf(acm.FSettlement):
        return fObject.IsPreReleased()
    return False


def GetDocumentsToSend(fObject, documents):
    """
    Get the documents to send for the specified object.
    """
    if ShouldProcessViaContingencyPlan(fObject):
        return ContingencyPlanGetDocumentsToSend(fObject, documents)
    else:
        return CoreGetDocumentsToSend(fObject, documents)


def ContingencyPlanGetDocumentsToSend(settlement, documents):
    """
    Get the documents to send for specified payment contingency plan
    settlement.

    This is accomplished by determining whether or not a contingency
    plan settlement is in a released status.
    """
    documentsToSend = list()
    if settlement.Status() in [SettlementStatus.RELEASED]:
        documentsToSend.extend(documents)
    return documentsToSend


def CoreGetDocumentsToSend(fObject, documents):
    """
    Default/Core behaviour for getting the documents to send for the
    specified object.
    """
    allPossibleDocuments = list()
    documentsToSend = list()
    opdocStatusToSend = [OperationsDocumentStatus.GENERATED, OperationsDocumentStatus.PENDING_GENERATION, OperationsDocumentStatus.SEND_FAILED]
    if fObject.IsKindOf(acm.FSettlement):
        if fObject.Status() in [SettlementStatus.RELEASED, SettlementStatus.PENDING_CANCELLATION]:
            allPossibleDocuments = documents
    if fObject.IsKindOf(acm.FConfirmation):
        query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
        query.AddAttrNode('Confirmation.Oid', 'EQUAL', fObject.Oid())
        allPossibleDocuments = query.Select()
    for opdoc in allPossibleDocuments:
        if opdoc.DocumentId() > 0:
            if opdoc.Status() in opdocStatusToSend:
                documentsToSend.append(opdoc)
            else:
                Utils.LogAlways("%s operations document %s will not be sent as the status is %s" % (str(GetClassName(fObject)), str(fObject.Oid()), opdoc.Status()))
    return documentsToSend


def DocumentInStatusSendFailed(settlementOrConfirmation, MTMessageType):
    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    if settlementOrConfirmation.IsKindOf(acm.FSettlement):
        query.AddAttrNode('Settlement.Oid', 'EQUAL', settlementOrConfirmation.Oid())
    if settlementOrConfirmation.IsKindOf(acm.FConfirmation):
        query.AddAttrNode('Confirmation.Oid', 'EQUAL', settlementOrConfirmation.Oid())

    if MTMessageType > 0:
        query.AddAttrNode('SwiftMessageType', 'EQUAL', MTMessageType)
    query.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SEND_FAILED)
    result = query.Select()

    if len(result) > 0:
        return result[0]
    return None


def CreateOperationsDocument(documentStatus, messageType, documentId, \
                             statusExplanation, xml, documentType, \
                             settlementOrConfirmation):
    import FDocumentationParameters as Params

    document = None
    try:
        if DocumentInStatusSendFailed(settlementOrConfirmation, messageType) != None:
            document = DocumentInStatusSendFailed(settlementOrConfirmation, messageType)
        else:
            document = acm.FOperationsDocument()

        document.Status(documentStatus)
        document.DocumentId(documentId)
        document.StatusExplanation(statusExplanation)
        document.SwiftMessageType(messageType)
        document.Type(documentType)
        document.Data("")
        document.Size(len(""))
        document.Protection(settlementOrConfirmation.Protection())
        document.Owner(settlementOrConfirmation.Owner())

        if settlementOrConfirmation.IsKindOf(acm.FSettlement):
            document.Settlement(settlementOrConfirmation)
        elif settlementOrConfirmation.IsKindOf(acm.FConfirmation):
            document.Confirmation(settlementOrConfirmation)

        if (Params.xmlStoredInOperationsDocument or
            (settlementOrConfirmation.IsKindOf(acm.FConfirmation) and settlementOrConfirmation.IsApplicableForSWIFT())):
            if xml != "":
                compressed_xml = ZlibAndHex(xml)
                document.Data(compressed_xml)
                document.Size(len(compressed_xml))
        if (not document.IsDeleted() and
            not settlementOrConfirmation.IsDeleted()):
            Utils.LogVerbose('FOperationsDocument created for %s %d.' % (settlementOrConfirmation.RecordType(), settlementOrConfirmation.Oid()))
    except Exception as exception:
        Utils.LogAlways("Failed to create FOperationsDocument: "  + str(exception))
    return document


def RemoveOperationsDocument(settlementOrConfirmation):

    if settlementOrConfirmation.Status() == "Pending Cancellation":
        return RemoveOperationsDocumentPendingCancellation()
    else:
        return RemoveOperationsDocumentDefault(settlementOrConfirmation)


def RemoveOperationsDocumentDefault(settlementOrConfirmation):
    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    orNode = query.AddOpNode('OR')

    if settlementOrConfirmation.IsKindOf(acm.FSettlement):
        query.AddAttrNode('Settlement.Oid', 'EQUAL', settlementOrConfirmation.Oid())
    if settlementOrConfirmation.IsKindOf(acm.FConfirmation):
        query.AddAttrNode('Confirmation.Oid', 'EQUAL', settlementOrConfirmation.Oid())
    orNode.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.EXCEPTION)
    orNode.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SEND_FAILED)
    orNode.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.GENERATED)
    orNode.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.NEW)
    AddCancellationNodeTree(orNode)
    return RemoveAckedOpdocsThatAreCancelled(query.Select(), settlementOrConfirmation)


def RemoveOperationsDocumentPendingCancellation():
    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    orNode = query.AddOpNode('OR')
    AddCancellationNodeTree(orNode)
    return query.Select()


def AddCancellationNodeTree(parentNode):
    '''Tree for finding operations documents belonging to n92 settlements no
    matter if they failed or were successful. This search is needed in order to
    clean opdocs before resending the settlement in status Release/Pending Cancellation.'''
    cancellationNode = parentNode.AddOpNode('AND')
    cancellationStatusNode = cancellationNode.AddOpNode('OR')
    cancellationStatusNode.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SEND_FAILED)
    cancellationStatusNode.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SENT_SUCCESSFULLY)
    cancellationMtsNode = cancellationNode.AddOpNode('OR')
    cancellationMtsNode.AddAttrNode('SwiftMessageType', 'EQUAL', 192)
    cancellationMtsNode.AddAttrNode('SwiftMessageType', 'EQUAL', 192199)
    cancellationMtsNode.AddAttrNode('SwiftMessageType', 'EQUAL', 292)
    cancellationMtsNode.AddAttrNode('SwiftMessageType', 'EQUAL', 292299)


def RemoveAckedOpdocsThatAreCancelled(selection, rec):
    '''Deployed selection-list will be extended with already cancelled opdocs.
    Applies only for settlements.'''
    if not rec.IsKindOf(acm.FSettlement):
        return selection
    ackedMTs = []
    cancellationMTs = []
    for opdoc in rec.Documents():
        if opdoc.Status() == OperationsDocumentStatus.SENT_SUCCESSFULLY:
            if str(opdoc.SwiftMessageType()).find("92") > -1:
                cancellationMTs.append(opdoc)
            else:
                ackedMTs.append(opdoc)

    if len(ackedMTs) <= len(cancellationMTs):
        # match so that already sent MT is cancelled, then it is ok to remove opdoc
        for mtOrig in ackedMTs:
            if mtOrig not in selection:
                selection.Add(mtOrig)

    return selection


def GetClassName(fObject):
    if fObject.IsKindOf(acm.FSettlement):
        return "Settlement"
    if fObject.IsKindOf(acm.FConfirmation):
        return "Confirmation"
    return "Unknown class"


def ReleaseDocument(document, fObject, docService):
    """
    Release (send) the specified object document.
    """
    if ShouldProcessViaContingencyPlan(fObject):
        return ContingencyPlanReleaseDocument(document)
    else:
        return CoreReleaseDocument(document, fObject, docService)


def ContingencyPlanReleaseDocument(document):
    """
    Release (send) the specified payment contingency plan settlement
    document.

    This is accomplished by marking the operations document as being
    sent without actually sending it to the document service.  The
    related settlement will then be extracted and marked as success-
    fully sent during the next payment contingency plan file creation.
    """
    message = "Releasing document for payment contingency plan "
    message += "settlement {settlement_oid}."
    Utils.LogAlways(message.format(
        settlement_oid=document.Settlement().Oid()
    ))
    document.Status(OperationsDocumentStatus.SENDING)
    return document


def CoreReleaseDocument(document, fObject, docService):
    """
    Default/Core behaviour for releasing the specified object
    document.
    """
    transport = GetTransportString(fObject, document)

    className = GetClassName(fObject)
    try:
        docService.SendDocumentByRouterName(document.DocumentId(), transport)
        Utils.LogVerbose('Sending document %d by %s.' % (document.DocumentId(), transport))
        if document.Type() == OperationsDocumentType.LONGFORM:
            document.Status(OperationsDocumentStatus.SENT_SUCCESSFULLY)
        elif document.Type() == OperationsDocumentType.SWIFT:
            import FDocumentationParameters as Params

            if Params.alwaysAcknowledgeSWIFTMessages:
                document.Status(OperationsDocumentStatus.SENT_SUCCESSFULLY)
            else:
                document.Status(OperationsDocumentStatus.SENDING)

    except (TypeError, ValueError):
        document.Status(OperationsDocumentStatus.SEND_FAILED)
        document.StatusExplanation("No valid document id: %d" % document.DocumentId())
        Utils.LogAlways('Failed to send document because '+ str(className) + str(fObject.Oid()) +' does not contain a valid document id.')
    except FOperationsDocumentService.DocumentServiceException as e:
        Utils.LogAlways('Failed to send document for %s %d: %s.' % (className, fObject.Oid(), e))
        document.Status(OperationsDocumentStatus.SEND_FAILED)
        document.StatusExplanation("Failed to send document. " + str(getExceptionFromXML(str(e))))
    return document


def GetTransportString(fObject, document):
    import FDocumentationParameters as Params

    transport = ""
    carbonCopySwift = "CarbonCopySWIFT"
    carbonCopyFreeform = "CarbonCopyFreeform"
    if fObject.IsKindOf(acm.FSettlement):
        hookAdmin = GetHookAdministrator()
        transport = hookAdmin.HA_CallHook(OperationsDocumentHooks.SETTLEMENT_TRANSPORT_ROUTER, document)
        if Params.saveCarbonCopySWIFT:
            transport = ",".join([transport, carbonCopySwift])
    elif fObject.IsKindOf(acm.FConfirmation):
        transport = fObject.Transport()
        if fObject.IsApplicableForSWIFT():
            if Params.saveCarbonCopySWIFT:
                transport = ",".join([transport, carbonCopySwift])
        else:
            if Params.saveCarbonCopyFreeform:
                transport = ",".join([transport, carbonCopyFreeform])
    return transport


def SendDocuments(fObject, documents, docService):
    sentDocuments = list()
    for i in documents:
        sentDocuments.append(ReleaseDocument(i, fObject, docService))
    return sentDocuments


def GetXMLSpecifier(fObject, isSWIFTMessage):
    generator = acm.FAMBAMessageGenerator()
    ambaBuffer = amb.mbf_create_buffer_from_data(str(generator.Generate(fObject)))
    ambaMessage = ambaBuffer.mbf_read()

    if fObject.IsKindOf(acm.FSettlement):
        return XmlSettleSwiftSpecifier.SettlementSwiftXMLSpecifier(ambaMessage)
    if fObject.IsKindOf(acm.FConfirmation):
        if isSWIFTMessage:
            return XmlConfSwiftSpecifier.ConfirmationSwiftXMLSpecifier(ambaMessage)
        else:
            return XmlConfDocSpecifier.ConfirmationDocumentXMLSpecifier(ambaMessage)


def __TransformXML(xml, xmlSpecifier, confirmationDocumentXSLTransformer):
    ''' Transforms the XML using XSLT. '''
    isConfDocXML = isinstance(xmlSpecifier, XmlConfDocSpecifier.ConfirmationDocumentXMLSpecifier)
    if confirmationDocumentXSLTransformer and isConfDocXML:
        return confirmationDocumentXSLTransformer.Transform(xml, xmlSpecifier)
    else:
        return xml


def ConvertSWIFTMTTagToInt(mt):
    '''This function is used from Documentation ATS when
    releasing a record and int value of the SWIFT message
    is returned. Default value is Zero (no such MT, error).
    Result of this function can be 192199 meaning that the document
    will be cancellation message MT 192 but for previous MT 199.
    Note that FSwiftMessageTypeExtractor implements similar code.'''
    ret = 0             # Consider 0 as unset value
    if mt.find("SWIFT_MT_192_FOR_199") != -1:
        ret = 192199
    elif mt.find("SWIFT_MT_292_FOR_299") != -1:
        ret = 292299
    elif mt.find("SWIFT_MT_") != -1:
        try:
            ret = int(mt.strip("SWIFT_MT_")[-3:])
        except TypeError:
            Utils.LogAlways('Could not retrieve swift message type. Got: %s ' % mt)
    return ret


def CreateDocumentFromSpecifier(fObject, xmlSpecifier, docService, confirmationDocumentXSLTransformer):
    '''Creates xml document, transforms it via xslt and sends it to documentation module.'''
    import FDocumentationParameters as Params

    xmlDirectory = Params.xmlDirectory
    import FOperationsDocumentXMLCreator as XmlCreator
    xml2 = XmlCreator.ToXml(xmlSpecifier)

    if not xml2:
        return ([], '')

    if fObject.IsKindOf(acm.FConfirmation):
        transformedXML = __TransformXML(xml2, xmlSpecifier, confirmationDocumentXSLTransformer)
    else:
        transformedXML = xml2
    XmlCreator.SaveXml(docService.GetXML(transformedXML), xmlDirectory, xmlSpecifier.GetUniqueFilename())
    docId = docService.CreateDocument(transformedXML)
    return (docId, transformedXML)


def DocumentAlreadyInStatusAck(settlementOrConfirmation, MTMessageType):
    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    if settlementOrConfirmation.IsKindOf(acm.FSettlement):
        query.AddAttrNode('Settlement.Oid', 'EQUAL', settlementOrConfirmation.Oid())
    if settlementOrConfirmation.IsKindOf(acm.FConfirmation):
        query.AddAttrNode('Confirmation.Oid', 'EQUAL', settlementOrConfirmation.Oid())

    if MTMessageType > 0:
        query.AddAttrNode('SwiftMessageType', 'EQUAL', MTMessageType)
    node = query.AddOpNode('OR')
    node.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SENT_SUCCESSFULLY)
    node.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.PENDING_GENERATION)
    return  len(query.Select()) > 0


def GetStatusExplanationFromException(exception):
    explanation = 'System error'
    exceptionText = getExceptionFromXML(str(exception))
    if isinstance(exception, FOperationsDocumentService.DocumentTemplateException):
        explanation = 'Insufficient message data'
    elif isinstance(exception, FOperationsDocumentService.DocumentServiceException):
        innerException = exception.GetInnerException()
        if isinstance(innerException, FOperationsDocumentService.DocumentServiceTimeOutException):
            if (str(exception).find("Connection refused") != -1):
                explanation = 'Interface failure'
            else:
                explanation = 'Insufficient message data'
        else:
            explanation = 'Insufficient message data'
    elif isinstance(exception, XSLTransformerException):
        explanation = 'Failed to transform XML'

    if len(exceptionText):
        explanation = "%s %s" % (explanation, exceptionText)

    return explanation


def CreateDocuments(fObject, docService, confirmationDocumentXSLTransformer):
    """
    Create the documents for the specified object.
    """
    if ShouldProcessViaContingencyPlan(fObject):
        return ContingencyPlanCreateDocuments(fObject)
    else:
        return CoreCreateDocuments(fObject, docService, confirmationDocumentXSLTransformer)


def ContingencyPlanCreateDocuments(settlement):
    """
    Create the documents for the specified payment contingency plan
    settlement.

    This is accomplished by creating an operations document that has
    a zero document id and no XML content.  The payment contingency
    plan does not attempt to generate document ids as these could
    theoretically clash with those generated by the normal document
    service.  Note that it is not possible to use a prefix or nega-
    tive id as Front Arena expects a document id to be a positive
    integer.
    """
    message = "Creating document for payment contingency plan "
    message += "settlement {settlement_oid}."
    Utils.LogAlways(message.format(
        settlement_oid=settlement.Oid()
    ))
    status = OperationsDocumentStatus.PENDING_GENERATION
    mt_type = Calculate(settlement)
    document_id = 0
    status_explanation = PaymentContingencyPlanGeneral.get_document_status_explanation()
    xml_content = ''
    document_type = OperationsDocumentType.SWIFT
    operations_document = CreateOperationsDocument(status, mt_type, document_id, status_explanation, xml_content,
        document_type, settlement)
    return [operations_document]


def CoreCreateDocuments(fObject, docService, confirmationDocumentXSLTransformer):
    """
    Default/Core behaviour for creating documents for the specified
    object.
    """
    documents = list()
    isSWIFTMessage = True
    messageType = OperationsDocumentType.SWIFT
    if fObject.IsKindOf(acm.FConfirmation):
        if not fObject.IsApplicableForSWIFT():
            messageType = OperationsDocumentType.LONGFORM
            isSWIFTMessage = False

    MTType = 0
    try:
        xmlSpecifier = GetXMLSpecifier(fObject, isSWIFTMessage)
        idList, XML = CreateDocumentFromSpecifier(fObject, xmlSpecifier, docService, confirmationDocumentXSLTransformer)
        for documentID in idList:
            documentInfo = docService.GetDocumentInfo(abs(documentID))
            MTType = ConvertSWIFTMTTagToInt(documentInfo['TreatmentEvent'])
            if not DocumentAlreadyInStatusAck(fObject, MTType):
                if (documentID < 0):
                    documents.append(CreateOperationsDocument(OperationsDocumentStatus.EXCEPTION, MTType, documentID, "", XML, messageType, fObject))
                else:
                    status = OperationsDocumentStatus.PENDING_GENERATION
                    if fObject.IsKindOf(acm.FConfirmation):
                        status = OperationsDocumentStatus.GENERATED
                    documents.append(CreateOperationsDocument(status, MTType, documentID, "", XML, messageType, fObject))
                    Utils.LogVerbose('Document %s created for %s %d.' % (documentID, fObject.RecordType(), fObject.Oid()))
            else:
                Utils.LogVerbose('Document of type %d already exists for %s %d.' % (MTType, fObject.RecordType(), fObject.Oid()))
    except (FOperationsDocumentService.DocumentServiceException, XSLTransformerException) as e:
        se = GetStatusExplanationFromException(e)
        Utils.LogVerbose('Failed to create document for ' + (GetClassName(fObject)) + ' %d: %s' % (fObject.Oid(), e))
        documents.append(CreateOperationsDocument(OperationsDocumentStatus.EXCEPTION, MTType, 0, se, "", messageType,  fObject))
    except Exception as e:
        Utils.LogVerbose('Failed to create document for ' + (GetClassName(fObject)) + ' %d: %s' % (fObject.Oid(), e))
        documents.append(CreateOperationsDocument(OperationsDocumentStatus.EXCEPTION, MTType, 0, str(e), "", messageType,  fObject))

    return documents


def CreateOperationsDocuments(fObject):
    documents = list()

    if fObject.IsKindOf(acm.FSettlement):
        messageType = OperationsDocumentType.SWIFT
        MTType = Calculate(fObject)
        documents.append(CreateOperationsDocument(OperationsDocumentStatus.NEW, MTType, 0, "", "", messageType, fObject))

    return documents


def InitXSLTransformers():
    ''' Create XSLTransformer instances. '''
    import FDocumentationParameters as Params

    extension = Params.xslTemplateExtensionForConfirmationDocuments
    directory = Params.xsltDirectoryForConfirmationDocuments
    filenameExtension = Params.xsltFilenameExtensionForConfirmationDocuments
    if extension != '':
        Utils.LogAlways('XSLT for confirmation documents enabled.')
        confirmationDocumentXSLTransformer = XSLTransformer(extension, directory, filenameExtension)
    else:
        Utils.LogAlways('XSLT for confirmation documents disabled.')
        confirmationDocumentXSLTransformer = None
    return confirmationDocumentXSLTransformer


def DefaultProcessing(fObject, confirmationDocumentXSLTransformer, docService):
    if not (fObject.IsKindOf(acm.FSettlement) or fObject.IsKindOf(acm.FConfirmation)):
            return

    isConfirmation = fObject.IsKindOf(acm.FConfirmation)
    isSwiftObject = (isConfirmation and fObject.IsApplicableForSWIFT()) or not isConfirmation

    if not ShouldProcessViaContingencyPlan(fObject):
        try:
            if (isSwiftObject and UseSwiftWriterForMessage(fObject)):
                Utils.LogVerbose('Operations Document processing for {} {} handled by SwiftWriter.'.format(GetClassName(fObject), fObject.Oid()))
                return
        except SwiftWriterAPIException as error:
            Utils.LogAlways('Operations Document processing aborted, error given: {}'.format(error))
            return

    try:
        Utils.LogVerbose('Processing ' + str(GetClassName(fObject)) + " with id = "+ str(fObject.Oid()) + " in status " +str(fObject.Status()) )
        newDocuments = list()

        acm.BeginTransaction()
        if ShouldDocumentsBeDeleted(fObject):
            documentsToDelete = RemoveOperationsDocument(fObject)
            for operationsDocument in documentsToDelete:
                Utils.LogAlways('Removing document from ' + str(GetClassName(fObject)) + " with id = "+ str(fObject.Oid()))
                operationsDocument.Delete()
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        Utils.LogAlways(str(e))

    try:
        acm.BeginTransaction()
        if fObject.IsKindOf(acm.FSettlement) and fObject.MTMessages() and \
           InOperationsDocumentCreationStatus(fObject) and IsMissingMTDocument(fObject):
            newDocuments = CreateOperationsDocuments(fObject)
            for i in newDocuments:
                i.Commit()
                Utils.LogAlways('Creating FOperationsDocument for ' + str(GetClassName(fObject)) + " with id = "+ str(fObject.Oid()))
        if InDocumentCreationStatus(fObject) and IsMissingMTDocument(fObject):
            shouldCreateDocument = True
            if isSwiftObject:
                if not fObject.MTMessages():
                    shouldCreateDocument = False
                    Utils.LogVerbose('Ignoring FOperationsDocument generation for {} with id = {} because of no MT'.format(GetClassName(fObject), fObject.Oid()))

            if shouldCreateDocument:
                newDocuments = CreateDocuments(fObject, docService, confirmationDocumentXSLTransformer)
                for i in newDocuments:
                    i.Commit()
                    Utils.LogAlways('Creating FOperationsDocument for ' + str(GetClassName(fObject)) + " with id = "+ str(fObject.Oid()))

        documentsToSend = list()
        if InSendDocumentStatus(fObject):
            documentsToSend = GetDocumentsToSend(fObject, newDocuments)

        documents = SendDocuments(fObject, documentsToSend, docService)
        for i in documents:
            i.Commit()
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        Utils.LogAlways(str(e))


def GetOperationsDocumentFromDocumentId(documentId):
    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    query.AddAttrNode('DocumentId', 'EQUAL', documentId)
    resultSet = query.Select()
    if resultSet.Size() > 0:
        if (resultSet.Size() > 1):
            Utils.LogVerbose('More than one FOperationsDocument referencing document ID %d' % documentId)
            Utils.LogVerbose('This might cause ACK/NAK processing to fail')
        return resultSet.First()
    else:
        return None


def AckNakProcessing(msg):
    acknowledgement = msg.mbf_find_object('ACKNOWLEDGMENT')
    if not acknowledgement:
        Utils.LogVerbose('AMBA message was not of type ACKNOWLEDGMENT')
        return

    xml2 = acknowledgement.mbf_find_object('XML')
    miniDom = xml.dom.minidom.parseString(xml2.mbf_get_value())

    swiftStatusString = FOperationsDocumentService.GetTagData(miniDom, 'SWIFT_STATUS')
    documentId = int(FOperationsDocumentService.GetTagData(miniDom, 'DOCUMENT_ID'))
    operationsDocument = GetOperationsDocumentFromDocumentId(documentId)
    if not operationsDocument:
        err = "Incoming '%s' message will not be handled due to no existing operations document with document id %d!" % (swiftStatusString.encode('ascii', 'ignore'), documentId)
        Utils.LogVerbose(err)
        return

    settlement = operationsDocument.Settlement()
    confirmation = operationsDocument.Confirmation()
    if settlement and settlement.Status() == SettlementStatus.ACKNOWLEDGED:
        Utils.LogVerbose("AMBA message ignored because settlement in status Acknowledged")
        return
    elif confirmation and confirmation.Status() == ConfirmationStatus.ACKNOWLEDGED:
        Utils.LogVerbose("AMBA message ignored because confirmation in status Acknowledged")
        return

    try:
        if operationsDocument.Type() == OperationsDocumentType.SWIFT and \
           ((settlement and UseSwiftWriterForMessage(settlement)) or \
            (confirmation and UseSwiftWriterForMessage(confirmation))):
            Utils.LogVerbose('Ack/Nak processing handled by SwiftWriter.')
            return
    except SwiftWriterAPIException as error:
        Utils.LogAlways("Ack/Nak processing aborted, error given: " + str(error))
        return

    swiftError = ""
    swiftErrorExplanation = ""

    if swiftStatusString == 'Nak':
        swiftError = FOperationsDocumentService.GetTagData(miniDom, 'SWIFT_ERROR')
        swiftErrorExplanation = FOperationsDocumentService.GetTagData(miniDom, 'SWIFT_ERROR_EXPL')

    HandleAckNakForOperationsDocument(swiftStatusString, operationsDocument, swiftError, swiftErrorExplanation)


def HandleAckNakForOperationsDocument(swiftStatusString, operationsDocument, swiftError = "", swiftErrorExplanation = ""):
    if operationsDocument:
        if swiftStatusString == 'Ack':
            if operationsDocument.Status() == OperationsDocumentStatus.SEND_FAILED:
                operationsDocument.StatusExplanation("")
            operationsDocument.Status(OperationsDocumentStatus.SENT_SUCCESSFULLY)
        elif swiftStatusString == 'Nak':
            explanation = swiftError + ': ' + swiftErrorExplanation
            operationsDocument.Status(OperationsDocumentStatus.SEND_FAILED)
            explanation = explanation.encode('ascii', 'ignore')
            operationsDocument.StatusExplanation(explanation)
        else:
            Utils.LogVerbose('Incorrect swift status %s' % swiftStatusString.encode('ascii', 'ignore'))
            return
        try:
            operationsDocument.Commit()
        except Exception as e:
            Utils.RaiseCommitException(e)


def getExceptionFromXML(err):
    '''Adaptiv stack trace can include xml, removing only the message from the
    exception tag. If no xml is included, deployed string is returned.'''
    ret = err
    hasXML = err.find("<?xml")
    if hasXML != -1:
        ret = err[:hasXML]
        msgs = err.split("essage>")
        if len(msgs):
            ret = "%s%s" % (ret, msgs[1][:-3])
    return ret


def ShouldProcessViaContingencyPlan(fObject):
    """
    Determines whether or not an object should be processed by the
    payment contingency plan.
    """
    if not PaymentContingencyPlanGeneral.is_enabled():
        return False
    if not fObject.IsKindOf(acm.FSettlement):
        return False
    return PaymentContingencyPlanGeneral.is_supported_settlement(fObject)
