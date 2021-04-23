import ael, acm, time
from ABSAFOperationsXML import ABSAFOperationsXML

MESSAGE_TYPE_LIST = ['Document Status', 'Affirmation Status', 'Counterparty Reference']
STATUS = ['Awaiting Dispatch', 'Dispatched', 'Document Not Required', 'Counterparty To Produce', 'Mismatched', 'Matched', 'Acknowledged', 'Financials Agreed', 'Counterparty Does Not Recognise Deal', 'Terms Disputed']

DOCUMENT_STATUS = ''
MESSAGE_TYPE = ''
CP_REF = ''

ael_variables = [['conf', 'Confirmation Seqnbr', 'int', None, None, 1, 0],
                 ['messageType', 'Message Type', 'string', MESSAGE_TYPE_LIST, 'Document Status', 1, 0],
                 ['status', 'Status', 'string', STATUS, 'Awaiting Dispatch', 1, 0],
                 ['cpRef', 'Reference', 'string', None, None, 0, 0]]

def get_Date(conf):
    return ael.date_today()

def get_Time(conf):
    return str(time.localtime()[3]) + ':' + str(time.localtime()[4]) + ':' + str(time.localtime()[5])

def get_OpDocId(conf):
    return conf.Documents()[0].Oid()

def set_DocumentStatus(value):
    global DOCUMENT_STATUS
    DOCUMENT_STATUS = value

def get_DocumentStatus(conf):
    global DOCUMENT_STATUS
    return DOCUMENT_STATUS

def set_MessageType(value):
    global MESSAGE_TYPE
    MESSAGE_TYPE = value

def get_MessageType(conf):
    global MESSAGE_TYPE
    return MESSAGE_TYPE

def set_CP_Ref(value):
    global CP_REF
    CP_REF = value

def get_CP_Ref(conf):
    global CP_REF
    return CP_REF
    
def get_Status_Msg(confirmation):
    document = '''<BCDocument>
        <header>
            <version edition="0" major="0" minor="0" revision="0" patch="0" branch="0" build="0" /> 
        </header>
        <document>
            <date><acmCode method = "get_Date" file = 'Confirmation_Status_Message'/></date> 
            <time><acmCode method = "get_Time" file = 'Confirmation_Status_Message'/></time> 
            <counterParty>
                <partyId>
                    <id type="sdsCounterpartyId"><acmCode eval = 'Counterparty().AdditionalInfo().BarCap_SMS_CP_SDSID()'/></id> 
                </partyId>
            </counterParty>
            <documentId>
                <id type="FA_IRD" version="10405952"><acmCode method = 'Trade.Oid'/></id> 
                <alternateId type="tridentTradeEventId">1234</alternateId> 
                <alternateId type="tridentImageOutboundId">5678</alternateId> 
                <alternateId type="abcapFrontarenaEventId"><acmCode method = "get_OpDocId" file = 'Confirmation_Status_Message'/></alternateId> 
            </documentId>
            <documentStatus><acmCode method = "get_DocumentStatus" file = 'Confirmation_Status_Message'/></documentStatus> 
            <affirmationStatus><acmCode method = "get_DocumentStatus" file = 'Confirmation_Status_Message'/></affirmationStatus> 
            <dispatchMethod>Email</dispatchMethod> 
            <counterpartyReference><acmCode method = "get_CP_Ref" file = 'Confirmation_Status_Message'/></counterpartyReference> 
            <messageReason><acmCode method = "get_MessageType" file = 'Confirmation_Status_Message'/></messageReason> 
        </document>
      </BCDocument>
    '''
    return ABSAFOperationsXML.GenerateXmlFromTemplateAsString(document, confirmation)

def ael_main(dict):
    confirmation = acm.FConfirmation[dict['conf']]
    set_DocumentStatus(dict['status'])
    set_MessageType(dict['messageType'])
    set_CP_Ref(dict['cpRef'])
    print get_Status_Msg(confirmation)
