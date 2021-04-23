""" Compiled: NONE NONE """

import amb
import acm
try:
    import ATSParameters as Params
except ImportError:
    import FDocumentationParametersTemplate as Params
import FOperationsUtils as Utils

def event_cb(channel, event_p, *arg_p):
    Utils.LogTrace()
    pass

def SendDocumentStatusOnMessageBroker(Status, ErrorMessage, AMBSender, documentId, objectType, AEL_ID, cpRef):
    Utils.LogTrace()
    source = Params.receiverSource
    init_string = Params.ambAddress
    sender = AMBSender
    subject = "%s/OPERATIONSDOCUMENT" % source

    amb.mb_init(init_string)
    Utils.LogTrace()
    Utils.LogTrace()
    print sender
    print source
    channel = amb.mb_queue_init_writer(sender, event_cb, source)

    message = amb.mbf_start_message(None, "UPDATE_OPERATIONSDOCUMENT", "1.0", None, source)
    mb_msg = message.mbf_start_list("!OPERATIONSDOCUMENT")
    mb_msg.mbf_add_string("RECORD_TYPE", "OperationsDocument")
    mb_msg.mbf_add_string("STATUS", Status)
    mb_msg.mbf_add_string("TYPE", "OPERATIONSDOCUMENT")
    mb_msg.mbf_add_string("STATUS_EXPLANATION", ErrorMessage)
    mb_msg.mbf_add_string("CPREF", cpRef)
    if objectType == "Settlement":
        mb_msg.mbf_add_string("SETTLEMENT_SEQNBR", str(AEL_ID))
        query =  "documentId = %s and settlement= %s" %(str(documentId), str(AEL_ID))
        document = acm.FOperationsDocument.Select(query)
        if document.Size() > 0:
            mb_msg.mbf_add_string("SEQNBR", str(document[0].Oid()))

    if objectType == "Confirmation":
        mb_msg.mbf_add_string("CONFIRMATION_SEQNBR", str(AEL_ID))
        query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
        query.AddAttrNode('Confirmation.Oid', 'EQUAL', acm.FConfirmation[int(AEL_ID)].Oid())
        documents = query.Select()

        if not documents.IsEmpty():
            document = documents.First()
            mb_msg.mbf_add_string("SEQNBR", str(document.Oid()))

    mb_msg.mbf_add_string("DOCUMENT_ID", str(documentId))
    mb_msg.mbf_end_list()
    message.mbf_end_message()

    mbuf_p = amb.mbf_create_buffer()
    message.mbf_generate(mbuf_p)
    queue_write_error = amb.mb_queue_write(channel,
                                    subject,
                                    mbuf_p.mbf_get_buffer_data(),
                                    mbuf_p.mbf_get_buffer_data_size(),
                                    'status_buf')
    print mbuf_p.mbf_get_buffer_data()
    return (queue_write_error == None)




def start(dict ):

    import FOperationsDocumentHandler as DocumentHandler
    import FDocumentationParameters as Params

    confirmationToReleases = dict['confirmationToReleases']
    documentID = 0

    if dict['sending'] == 'Yes':
        status = "Dispatched"
    if dict['matched'] == 'Yes':
        status = "Matched"
    if dict['Generated'] == 'Yes':
        status = "Awaiting Dispatch"
    if dict['DNR'] == 'Yes':
        status = "Document Not Required(Pre Release)"
    if dict['DNRPost'] == 'Yes':
        status = "Document Not Required(Post Release)"
    if dict['CounterpartyToProduce'] == 'Yes':
        status = "Counterparty To Produce"
    if dict['matchingFailed'] == 'Yes':
        status = "Matching Failed"
    if dict['Affirmation Acknowledged'] == 'Yes':
        status = "Affirmation Acknowledged"
    if dict['Affirmation Financials Agreed'] == 'Yes':
        status = "Affirmation Financials Agreed"
    if dict['Affirmation Counterparty Does Not Recognise Deal'] == 'Yes':
        status = "Affirmation Counterparty Does Not Recognise Deal"
    if dict['Affirmation Terms Disputed'] == 'Yes':
        status = "Affirmation Terms Disputed"


    documentID = dict['AffirmationCPRef']

    SendDocumentStatusOnMessageBroker(status, "", Params.tridentConnectionSenderMBName, documentID, "Confirmation", confirmationToReleases, "666")



"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
try:
    if __name__ == "__main__":
        import sys, getopt

    import acm, time, ael
    import FOperationsUtils as Utils

    ael_variables = [('confirmationToReleases', 'Confirmation:',
                       'int', None, 0, 0),
                       ('AffirmationCPRef', 'Affirmation CP Ref:',
                       'int', None, 0, 0),
                       ('Generated', 'Awaiting Dispatch:',
                       'string', ['Yes', 'No'], 'No', 0),
                       ('DNR', 'Document Not Required(Pre Release):',
                       'string', ['Yes', 'No'], 'No', 0),
                       ('sending', 'Dispatched:',
                       'string', ['Yes', 'No'], 'No', 0),
                       ('CounterpartyToProduce', 'Counterparty To Produce:',
                       'string', ['Yes', 'No'], 'No', 0),
                       ('matchingFailed', 'Matching Failed',
                       'string', ['Yes', 'No'], 'No', 0),
                       ('DNRPost', 'Document Not Required(Post Release):',
                       'string', ['Yes', 'No'], 'No', 0),
                       ('matched', 'Matched:',
                       'string', ['Yes', 'No'], 'No', 0),
                       ('Affirmation Acknowledged', 'Affirmation Acknowledged:',
                       'string', ['Yes', 'No'], 'No', 0),
                       ('Affirmation Financials Agreed', 'Affirmation Financials Agreed:',
                       'string', ['Yes', 'No'], 'No', 0),
                       ('Affirmation Counterparty Does Not Recognise Deal', 'Affirmation Counterparty Does Not Recognise Deal:',
                       'string', ['Yes', 'No'], 'No', 0),
                       ('Affirmation Terms Disputed', 'Affirmation Terms Disputed :',
                       'string', ['Yes', 'No'], 'No', 0),
                        ]

    def ael_main(dict):
        start(dict )

except Exception, e:
    if globals().has_key('ael_variables'):
        del globals()['ael_variables']
    if globals().has_key('ael_main'):
        del globals()['ael_main']
    Utils.Log(True, str(e))
