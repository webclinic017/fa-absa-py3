""" Compiled: NONE NONE """

import amb
try:
    import ATSParameters as Params
except ImportError:
    print "Failed to import BARMLParameters"

from xml.etree.ElementTree import Element, SubElement, dump, XML, tostring, ElementTree, parse, fromstring

import FOperationsUtils as Utils

oldNewMap = {'AwaitingDispatch' : 'Awaiting Dispatch', 
          'Dispatched' : 'Dispatched',
          'NotRequired' : 'Document Not Required',
          'CounterpartyToProduce' : 'Counterparty To Produce',
          'Mismatched' : 'Mismatched',
          'Confirmed' : 'Matched'}

def event_cb(channel, event_p, *arg_p):
    pass

class FBARMLMessage(object):
    def __init__(self, XMLString):
        self.__status = ""

        self.__tridentID = ""
        self.__frontID = ""
        self.__cpRef = ""
        if XMLString == "":
            return
        XML = ElementTree(fromstring(XMLString))
        
        for node in XML.find('/identification'):
            if node.get('type') == 'tridentConfirmationDocumentId':
                self.__tridentID = node.text
            if node.get('type') == 'abcapFrontarenaEventId':
                self.__frontID = node.text
                self.__status = ""

        messageReason = XML.find('/event/name').text
                
        if messageReason == 'ConfirmationStatusUpdate':
            node = XML.find('/content/documentStatus/confirmationStatus/id')
            if node.text == 'Unconfirmed':
                subNode = XML.find('/content/documentStatus/publisherConfirmationSubStatus/id')
                self.__status = oldNewMap[subNode.text]
            elif node.text == 'NotRequired':
                self.__status = oldNewMap[node.text]
            elif node.text == 'Confirmed':
                self.__status = oldNewMap[node.text]
                
        if messageReason == 'DocumentAffirmationStatusUpdate':
            node = XML.find('/content/documentStatus/documentAffirmationStatus/id')
            self.__status = node.text
        if messageReason == 'CounterPartyReferenceUpdate':
            self.__status = 'CounterpartyReference'
            self.__cpRef = "tbc"

        
    def GetStatus(self):
        return self.__status

    def GetTridentID(self):
        return self.__tridentID

    def GetFrontID(self):
        return self.__frontID
    
    def GetCPRef(self):
        return self.__cpRef

class ABSABARMLAMBAPoster(object):
    def __init__(self):
        Utils.LogTrace()
        self.__source = Params.receiverSource
        self.__subject = "%s/OPERATIONSDOCUMENT" % self.__source

        amb.mb_init(Params.ambAddress)
        self.__channel = amb.mb_queue_init_writer(Params.tridentConnectionSenderMBName, event_cb, self.__source)

    def ConvertToAmbaAndPost(self, BARML):
        BARMLMessage = FBARMLMessage(BARML)
        if BARMLMessage.GetStatus() != "" and BARMLMessage.GetTridentID() != "" and BARMLMessage.GetFrontID() != "":
            if BARMLMessage.GetStatus() == 'CounterpartyReference':
                tridentID = BARMLMessage.GetCPRef()
            else:
                tridentID = BARMLMessage.GetTridentID()
                
            self.SendDocumentStatusOnMessageBroker(BARMLMessage.GetStatus(), tridentID, BARMLMessage.GetFrontID())

    def SendDocumentStatusOnMessageBroker(self, Status, tridentID, documentId):
        import acm
        #conf = acm.FConfirmation[documentId]
        doc = acm.FOperationsDocument[documentId]
        
        if doc and not doc.IsDeleted():
            conf = doc.Confirmation()
            message = amb.mbf_start_message(None, "UPDATE_OPERATIONSDOCUMENT", "1.0", None, self.__source)
            mb_msg = message.mbf_start_list("!OPERATIONSDOCUMENT")
            mb_msg.mbf_add_string("RECORD_TYPE", "OperationsDocument")
            
            if Status == "Document Not Required":
                if conf.Status() in ("New", "Pending Document Generation", "Authorised"):
                    Status = "Document Not Required(Pre Release)"
                else:
                    Status = "Document Not Required(Post Release)"
                    
            mb_msg.mbf_add_string("STATUS", Status)
            mb_msg.mbf_add_string("TYPE", "OPERATIONSDOCUMENT")

            #documentId = str(conf.Documents()[0].Oid())
            mb_msg.mbf_add_string("SEQNBR", documentId)
            
            mb_msg.mbf_add_string("DOCUMENT_ID", tridentID)
            mb_msg.mbf_end_list()
            message.mbf_end_message()

            mbuf_p = amb.mbf_create_buffer()
            message.mbf_generate(mbuf_p)
            queue_write_error = amb.mb_queue_write(self.__channel,
                                            self.__subject,
                                            mbuf_p.mbf_get_buffer_data(),
                                            mbuf_p.mbf_get_buffer_data_size(),
                                            'status_buf')
            print mbuf_p.mbf_get_buffer_data()
            return (queue_write_error == None)
        
        if not doc:
            raise Exception('Operations Document does not exist.')
            
        return True
