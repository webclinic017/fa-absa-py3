""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentService.py"
from FOperationsExceptions import WrapperException
from FOperationsCustomDocServiceTemplate import CustomDocumentServiceTemplate
from FOperationsDocumentEnums import DocumentFormat, DataType

import FOperationsDocumentAMBXmlCreator
import FOperationsUtils
import amb
import binascii
import sys
import time
import xml.dom.minidom

NO_REPLY_FROM_DOC_SERVICE = "NO_REPLY_FROM_DOC_SERVICE"

class DocumentServiceException(WrapperException):
    def __init__(self, message, innerException = None):
        super(DocumentServiceException, self).__init__(message, innerException)

class DocumentTemplateException(DocumentServiceException):
    def _init__(self, message, innerException = None):
        super(DocumentTemplateException, self).__init__(message, innerException)

class DocumentServiceTimeOutException(WrapperException):
    def __init__(self, message, innerException = None):
        super(DocumentServiceTimeOutException, self).__init__(message, innerException)

class Document:

    def __init__(self, documentId, data, dataType):
        self.__documentId = documentId
        self.__data = data
        self.__dataType = dataType

    def GetDocumentId(self):
        return self.__documentId

    def GetData(self):
        return self.__data

    def GetDataType(self):
        return self.__dataType


class DocumentService:

    def __init__(self):
        if self.__class__ is DocumentService:
            raise NotImplementedError

    def IsConnected(self):
        raise NotImplementedError

    def GetDocument(self, documentId, documentFormat):
        raise NotImplementedError

    def GetDocumentInfo(self, documentId):
        raise NotImplementedError

    def SendDocumentByRouterName(self, documentId, routerName):
        raise NotImplementedError

    def CreateDocument(self, xml):
        raise NotImplementedError

    def Disconnect(self):
        raise NotImplementedError


class AdaptivDoc111(DocumentService):

    def __init__(self, parameters):
        DocumentService.__init__(self)
        hasConnection = True
        if self.IsPrime() or self.IsArenaPython():
            import FDocumentationParameters as Params

            hasConnection = FOperationsUtils.GetConnectToAMBSingleton(Params.ambAddress)

        if hasConnection == None:
            raise DocumentServiceException("Failed to connect to AMB (%s), please check FDocumentationParameters!" % (str(parameters.ambAddress)))

        self.ambCommunicator = AmbCommunicator()

    def IsConnected(self):
        '''AMB based connection to Document service'''
        requestReplyData = RequestReplyData()
        self.ambCommunicator.IsConnectedRequestAndApply(requestReplyData)
        return requestReplyData.result

    def GetDocument(self, documentId, documentFormat):
        ''' '''
        requestReplyData = RequestReplyData()
        documentId = abs(documentId) #docid on the adaptiv side is always positive
        requestReplyData.docid = documentId
        if documentFormat == DocumentFormat.PDF:
            self.ambCommunicator.GetDocumentAsPDFRequestAndApply(requestReplyData, documentId)
        elif documentFormat == DocumentFormat.RTF:
            self.ambCommunicator.GetDocumentAsRTFRequestAndApply(requestReplyData, documentId)
        elif documentFormat == DocumentFormat.ASCII:
            self.ambCommunicator.GetDocumentAsASCIIRequestAndApply(requestReplyData, documentId)
        else:
            raise DocumentServiceException('Unsupported document format: %d', documentFormat)
        return requestReplyData.result

    def GetDocumentInfo(self, documentId):
        ''' Adaptiv111 '''
        requestReplyData = RequestReplyData()
        requestReplyData.docid = documentId
        self.ambCommunicator.GetDocumentInfoRequestAndApply(requestReplyData, documentId)
        return requestReplyData.result

    def SendDocumentByRouterName(self, documentId, routerName):
        requestReplyData = RequestReplyData()
        requestReplyData.docid = documentId
        requestReplyData.routerName = routerName
        requestReplyData.result = NO_REPLY_FROM_DOC_SERVICE # a trick to see if Document service replied or not
        self.ambCommunicator.SendDocumentByRouterNameRequestAndApply(requestReplyData, documentId, routerName)
        return requestReplyData.result

    def CreateDocument(self, xml2):
        '''Returns list of ints '''
        requestReplyData = RequestReplyData()
        self.ambCommunicator.CreateDocumentRequestAndApply(requestReplyData, xml2)
        return requestReplyData.result

    def GetXML(self, xml2):
        '''Returns new XML structure based on createDocument Document service call.
        Note that no encoding is in the header as per design.'''
        return self.ambCommunicator.xmlWriter.CreateDocumentXML(xml2)

    def IsPrime(self):
        '''Only prime user should connect to amb '''
        return sys.executable.endswith("prime.exe")

    def IsArenaPython(self):
        return sys.executable.endswith("arena_python.exe")

    def Disconnect(self):
        '''Not needed, singleton is holding amb connection that is cleaned out when prime is closed '''
        pass

def CreateDocumentService(parameters):
    EXCEPTION_MSG = 'Could not create document service: '

    if parameters == None:
        raise DocumentServiceException(EXCEPTION_MSG + 'Parameters not provided.')
    try:
        if parameters.useAdaptivDocumentService == False:
            return GetCustomDocumentService(parameters)
        else:
            return AdaptivDoc111(parameters)
    except AttributeError as e:
        raise DocumentServiceException(EXCEPTION_MSG + 'Parameter not found: ', e)


class RequestReplyData:
    ''' '''
    def __init__(self, binary = False):
        self.binary = binary
        self.buf = None
        self.data = None
        self.docid = 0
        self.errorMsg = ""
        self.result = None
        self.routerName = ""

    def __str__(self):
        s = ""
        for k, v in list(self.__dict__.items()):
            s += ( str(k) +  " --> " + str(v) + "\n")
        return s

    def destroyDataAndBuf(self):
        '''Buffer must be destroyed after parsing the result.'''
        if self.data:
            self.data = None
        if self.buf:
            self.buf.mbf_destroy_buffer()

class AmbCommunicator:
    ''' '''
    def __init__(self):
        try:
            import FDocumentationParameters as Params

            self.subject = Params.AMBSubjectForDocumentation
            self.xmlWriter = FOperationsDocumentAMBXmlCreator.AMBXmlCreator()
            self.writer = amb.mb_queue_init_writer(Params.AMBSenderForDocumentation, AmbCommunicator.AmbCallbackForWriter, None)
        except Exception as e:
            raise DocumentServiceException("Failed to connect to AMB, please check AMBSenderForDocumentation in FDocumentationParameters: " + str(e))


    def __str__(self):
        s = ""
        for k, v in list(self.__dict__.items()):
            s += ( str(k) +  " --> " + str(v) + "\n")
        return s

    def __PollForReplyResult(self, requestReplyData):
        '''amb.mb_poll is done in order to receive result from mb_queue_reqest via cb '''
        import FDocumentationParameters as Params

        noResult = [None, NO_REPLY_FROM_DOC_SERVICE]
        ms = .001
        if sys.platform != "win32":
            ms = .5
        timer_sec = Params.documentServiceTimeoutInSeconds
        for dummy in range(0, Params.documentServiceRetriesOnTimeout):
            elapsed = 0
            if requestReplyData.result not in noResult or requestReplyData.errorMsg:
                break
            while elapsed < timer_sec:
                if requestReplyData.result not in noResult or requestReplyData.errorMsg:
                    break
                time.sleep(ms)
                elapsed = elapsed + ms
                amb.mb_poll()
        hasTimedOut = (requestReplyData.result in noResult) and not requestReplyData.errorMsg
        if hasTimedOut:
            timeoutMsg = 'Timed out while waiting for reply from Document service.'
            raise DocumentServiceException('Connection refused.', DocumentServiceTimeOutException(timeoutMsg))

    def IsConnectedRequestAndApply(self, requestReplyData):
        ''' '''
        data = self.xmlWriter.IsConnectedXML()
        amb.mb_queue_request(self.writer, self.subject, data, len(data), AmbCommunicator.IsConnectedCallback, requestReplyData)
        self.__PollForReplyResult(requestReplyData)

        if not requestReplyData.result or requestReplyData.errorMsg:
            raise DocumentServiceException(requestReplyData.errorMsg)
        return

    def CreateDocumentRequestAndApply(self, requestReplyData, xml):
        ''' '''
        data = RemoveHeader(self.xmlWriter.CreateDocumentXML(xml))
        amb.mb_queue_request(self.writer, self.subject, data, len(data), AmbCommunicator.CreateDocumentCallback, requestReplyData)
        self.__PollForReplyResult(requestReplyData)

        if requestReplyData.result:
            return

        if ('%s' % requestReplyData.errorMsg).find('No treatments matched') >= 0:
            raise DocumentTemplateException(requestReplyData.errorMsg)
        else:
            raise DocumentServiceException(requestReplyData.errorMsg)


    def GetDocumentAsPDFRequestAndApply(self, requestReplyData, documentId):
        ''' '''
        data = self.xmlWriter.GetDocumentXML(documentId, DocumentFormat.PDF)
        amb.mb_queue_request(self.writer, self.subject, data, len(data), AmbCommunicator.GetDocumentAsPDFCallback, requestReplyData)
        self.__PollForReplyResult(requestReplyData)
        if not requestReplyData.result or requestReplyData.errorMsg:
            raise DocumentServiceException(requestReplyData.errorMsg)
        return

    def GetDocumentAsRTFRequestAndApply(self, requestReplyData, documentId):
        ''' '''
        data = self.xmlWriter.GetDocumentXML(documentId, DocumentFormat.RTF)
        amb.mb_queue_request(self.writer, self.subject, data, len(data), AmbCommunicator.GetDocumentAsRTFCallback, requestReplyData)
        self.__PollForReplyResult(requestReplyData)
        if not requestReplyData.result or requestReplyData.errorMsg:
            raise DocumentServiceException(requestReplyData.errorMsg)
        return

    def GetDocumentAsASCIIRequestAndApply(self, requestReplyData, documentId):
        ''' '''
        data = self.xmlWriter.GetDocumentXML(documentId, DocumentFormat.ASCII)
        amb.mb_queue_request(self.writer, self.subject, data, len(data), AmbCommunicator.GetDocumentAsASCIICallback, requestReplyData)
        self.__PollForReplyResult(requestReplyData)
        if not requestReplyData.result or requestReplyData.errorMsg:
            raise DocumentServiceException(requestReplyData.errorMsg)
        return

    def GetDocumentInfoRequestAndApply(self, requestReplyData, documentId):
        ''' '''
        data = self.xmlWriter.GetDocumentInfoXML(documentId)
        amb.mb_queue_request(self.writer, self.subject, data, len(data), AmbCommunicator.GetDocumentInfoCallback, requestReplyData)
        self.__PollForReplyResult(requestReplyData)
        if not requestReplyData.result or requestReplyData.errorMsg:
            raise DocumentServiceException(requestReplyData.errorMsg)
        return

    def SendDocumentByRouterNameRequestAndApply(self, requestReplyData, documentId, routerName):
        ''' '''
        data = self.xmlWriter.SendDocumentByRouterXML(documentId, routerName)
        data = cleanXmlTag(data, "RouterName")
        amb.mb_queue_request(self.writer, self.subject, data, len(data), AmbCommunicator.SendDocumentByRouterNameCallback, requestReplyData)
        self.__PollForReplyResult(requestReplyData)
        # result is ok if empty string is returned from Document service
        if requestReplyData.result or requestReplyData.errorMsg:
            if requestReplyData.result == NO_REPLY_FROM_DOC_SERVICE:
                err = 'No reply received from Document service'
                requestReplyData.errorMsg = err
            raise DocumentServiceException(requestReplyData.errorMsg)
        return

    @staticmethod
    def IsConnectedCallback(msg, status, requestReplyData):
        ''' '''
        replyAsXML = AmbCommunicator.getReplyDetailsAsXml(msg, status, requestReplyData)
        if replyAsXML:
            connected = GetTagData(replyAsXML, "Message").encode('ascii', 'ignore')
            if connected == "Connected Succesfully!":
                requestReplyData.result = True
            else:
                requestReplyData.result = False
                err = "Can not connect to Document service! %s" % str(connected)
                requestReplyData.errorMsg = err
        else:
            requestReplyData.result = False
            err = "Can not connect to Document service!"
            requestReplyData.errorMsg = err


    @staticmethod
    def CreateDocumentCallback(msg, status, requestReplyData):
        ''' '''
        res = []
        replyAsXML = AmbCommunicator.getReplyDetailsAsXml(msg, status, requestReplyData)
        if replyAsXML:
            docids = GetTagValues(replyAsXML, "d2p1:int")
            for rr in docids:
                docid = int(rr)
                if docid != 0:
                    res.append(docid)

        if not len(res):
            if replyAsXML:
                replyAsXML = str(replyAsXML.toxml())
            else:
                replyAsXML = ""
            err = "Failed to create document! %s" % replyAsXML
            requestReplyData.errorMsg = err
        requestReplyData.result = res


    @staticmethod
    def GetDocumentInfoCallback(msg, status, requestReplyData):
        ''' '''
        infos = ["TreatmentEvent", "TemplateName", "RoutingName", "MessageReference", "MsgSrcId", "SourceId", "ResultId", "Status"]
        info = {}
        replyAsXML = AmbCommunicator.getReplyDetailsAsXml(msg, status, requestReplyData)
        if replyAsXML:
            for tag in infos:
                xml_tag = "d2p1:%s" % tag
                val = GetTagData(replyAsXML, xml_tag).encode('ascii', 'ignore')
                if val:
                    info[tag] = val

        if info == {}:
            if replyAsXML:
                err = 'Failed to get document info from Document service for doc %d! %s' % (requestReplyData.docid, replyAsXML.toxml())
            else:
                err = 'Failed to get document info from Document service for doc %d!' % (requestReplyData.docid)
            requestReplyData.errorMsg = err

        requestReplyData.result = info


    @staticmethod
    def SendDocumentByRouterNameCallback(msg, status, requestReplyData):
        ''' '''
        replyAsXML = AmbCommunicator.getReplyDetailsAsXml(msg, status, requestReplyData)
        if not replyAsXML:
            requestReplyData.result = ""
        else:
            err = 'Failed to send document %d by router %s! %s' % (requestReplyData.docid, requestReplyData.routerName, replyAsXML.toxml())
            requestReplyData.errorMsg = err
            requestReplyData.result = err

    @staticmethod
    def GetDocumentAsPDFCallback(msg, status, requestReplyData):
        ''' '''
        AmbCommunicator.setBufAndDataFromReplyDetails(msg, status, requestReplyData)
        s = getTagAsString(requestReplyData.data, "PDFStream")
        if len(s) == 0:
            err = 'Failed to get document with id %d as PDF.' % requestReplyData.docid
            requestReplyData.errorMsg = err
        else:
            blob = binascii.a2b_base64(s)
            requestReplyData.result = Document(requestReplyData.docid, blob, DataType.BINARY)
        requestReplyData.destroyDataAndBuf()

    @staticmethod
    def GetDocumentAsRTFCallback(msg, status, requestReplyData):
        ''' '''
        AmbCommunicator.setBufAndDataFromReplyDetails(msg, status, requestReplyData)
        rtf = getTagAsString(requestReplyData.data, "RTFText")
        if len(rtf) == 0:
            err = 'Failed to get document with id %d as RTF.' % requestReplyData.docid
            requestReplyData.errorMsg = err
        else:
            requestReplyData.result = Document(requestReplyData.docid, rtf, DataType.TEXT)
        requestReplyData.destroyDataAndBuf()

    @staticmethod
    def GetDocumentAsASCIICallback(msg, status, requestReplyData):
        ''' '''
        AmbCommunicator.setBufAndDataFromReplyDetails(msg, status, requestReplyData)
        txt = getTagAsString(requestReplyData.data, "ASCIIText")
        if len(txt) == 0:
            err = 'Failed to get document with id %d as ASCII.' % requestReplyData.docid
            requestReplyData.errorMsg = err
        else:
            requestReplyData.result = Document(requestReplyData.docid, txt, DataType.TEXT)
        requestReplyData.destroyDataAndBuf()

    @staticmethod
    def setBufAndDataFromReplyDetails(msg, status, requestReplyData):
        '''msg is the reply and must be converted to buffer that is to be destroyed later
        after calling this function. status is also returned from amb adapter (doc service).
        Do not raise exception here put on requestReplyData since amb sdk does not propagate
        exception up to the caller. Hence do check on requestReplyData.errorMsg!'''
        if msg:
            requestReplyData.buf = amb.mbf_create_buffer_from_data(msg.data_p)
            requestReplyData.data = requestReplyData.buf.mbf_get_buffer_data()
        else:
            err = "No reply from Documentation Service, requestReplyData.buf and requestReplyData.data are None and status is %s" % status
            requestReplyData.errorMsg = err


    @staticmethod
    def getReplyDetailsAsXml(msg, status, requestReplyData):
        '''Returns amb reply in XML format without utf-16 header.
        If empty answer received None returned.
        Send doc returns nothing so do checks if this function returns anything.'''
        AmbCommunicator.setBufAndDataFromReplyDetails(msg, status, requestReplyData)
        ret = None
        if len(requestReplyData.data) > 0:
            ret = xml.dom.minidom.parseString(RemoveHeader(requestReplyData.data))
        requestReplyData.destroyDataAndBuf()
        return ret


    @staticmethod
    def AmbCallbackForWriter(channel, event, arg):
        '''Empty function, needed only when creating amb writer '''
        pass

def RemoveHeader(x):
    '''XML that includes header such as
    <?xml version="1.0" encoding="ISO-8859-1" ?>
    gets header cleaned out.'''
    h1 = x.find("<?xml")
    if h1 != -1:
        end = "?>"
        h2 = x.find(end)
        return x[h2+len(end):]
    return x

def getTagAsString(reply, tag):
    '''Returns value of the tag from the content in the reply.
    getTagAsString("<a>tagvalue</a>", "a") would return tagvalue
    getTagAsString("<a arg=1 />", "") would return empty string
    This function is suited for places in the code where
    minidom approach should not be used!'''
    t1 = reply.find(tag)
    if t1 != -1:
        t12 = reply.find(">")
        if t12 > -1:
            t13 = reply.find("/>")
            if t13 > -1 and t13-1 == t12:
                t12 = t13 + 2
            else:
                t12 = t12 + 1
        elif t12 + 1 <= len(reply):
            t12 = t12 + 1

        start_tag = reply[t1-1:t12]

        if len(start_tag) >= len(reply):
            #empty tag
            return ""

        t22 = reply.find("</%s" % (tag))
        end_tag = None
        if t22 > -1:
            end_tag = reply[t22:]

        if start_tag and end_tag:
            s1 = reply.find(start_tag) + len(start_tag)
            s2 = reply.find(end_tag)
            return reply[s1:s2]
    return reply

def cleanXmlTag(xmlString, tagName):
    '''tagName includes newlines or spaces when it should not.
    This function cleans out these chars and returns back the xmlString.
    If tagName not found in the xml intact xmlString will be returned.'''
    ret = xmlString
    startTag = "<%s>" % (tagName)
    endTag  = "</%s>" % (tagName)
    firstEndingPosition = xmlString.find(startTag)
    if firstEndingPosition > -1:
        firstEndingPosition = firstEndingPosition + len(startTag)
    secondStartEndingPosition = xmlString.find(endTag)
    if secondStartEndingPosition > -1 and firstEndingPosition > -1:
        part1 = xmlString[:firstEndingPosition]
        cleanTag = xmlString[firstEndingPosition:secondStartEndingPosition].strip()
        part2 = xmlString[secondStartEndingPosition:]
        ret = "%s%s%s" % (part1, cleanTag, part2)
    return ret

def GetCustomDocumentService(parameters):
    try:
        import FOperationsCustomDocService
        return FOperationsCustomDocService.CustomDocumentService(parameters)
    except ImportError:
        return CustomDocumentServiceTemplate(parameters)

def GetTagData(miniDom, tagName):
    tagDataString = ''
    elements = miniDom.getElementsByTagName(tagName)

    if len(elements) > 0:
        for node in elements[0].childNodes:
            if node.nodeType == node.TEXT_NODE:
                tagDataString = node.data
    return tagDataString

def GetTagValues(miniDom, tagName):
    values = []
    elements = miniDom.getElementsByTagName(tagName)

    if len(elements) > 0:
        for e in elements:
            for node in e.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    values.append(node.data)
    return values

