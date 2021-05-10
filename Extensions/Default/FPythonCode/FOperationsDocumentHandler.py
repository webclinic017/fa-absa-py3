""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentHandler.py"
import amb
import acm

def event_cb(channel, event_p, *arg_p):
    1


class DocumentStatusOnMessageBrokerSender:
    def __init__(self):
        import FDocumentationParameters as Params

        source = Params.receiverSource
        init_string = Params.ambAddress
        sender = Params.AMBSenderForAckNack
        amb.mb_init(init_string)
        self.__channel = amb.mb_queue_init_writer(sender, event_cb, source)

    def __del__ (self):
        amb.mb_close()

    def Send(self, status, errorMessage, documentId, objectType, aelId):
        """
        DESCRIPTION: This method will send an OperationsDocument message on the AMB.
                     Used for determining the status transition from Released to either
                     Acknowledged or Not Acknowledged, for a settlement/confirmation record.
                     When the OperationsDocument message has been sent on the AMB, the settlement or
                     confirmation ATS will update the settlement/confirmation status accordingly.

        INPUT:       status      - String reflecting the SWIFT reply. If SWIFT reply was ACK status
                                   shall be 'Sent successfully', if NAK status shall be 'Send failed'.

                    errorMessage - If NAK, supply an error message string

                    documentId   - Integer identifier of the OperationsDocument referencing the
                                   released settlement/confirmation

                    objectType   - String determining the released object. Either 'Settlement' or
                                   'Confirmation'

                    aelId        - Integer identifier of the released settlement or confirmation.

        OUTPUT:    An AMB message being sent on the AMB.
        """
        import FDocumentationParameters as Params

        source = Params.receiverSource
        subject = "%s/OPERATIONSDOCUMENT" % source

        message = amb.mbf_start_message(None, "UPDATE_OPERATIONSDOCUMENT", "1.0", None, source)
        mb_msg = message.mbf_start_list("!OPERATIONSDOCUMENT")
        mb_msg.mbf_add_string("RECORD_TYPE", "OperationsDocument")
        mb_msg.mbf_add_string("STATUS", status)
        mb_msg.mbf_add_string("STATUS_EXPLANATION", errorMessage)
        if objectType == "Settlement":
            mb_msg.mbf_add_string("SETTLEMENT_SEQNBR", str(aelId))
            query =  "documentId = %s and settlement= %s" % (str(documentId), str(aelId))
            document = acm.FOperationsDocument.Select(query)
            if document.Size() > 0:
                mb_msg.mbf_add_string("SEQNBR", str(document[0].Oid()))

        if objectType == "Confirmation":
            mb_msg.mbf_add_string("CONFIRMATION_SEQNBR", str(aelId))
            query =  "documentId = %s and confirmation= %s" % (str(documentId), str(aelId))
            document = acm.FOperationsDocument.Select(query)
            if document.Size()  > 0:
                mb_msg.mbf_add_string("SEQNBR", str(document[0].Oid()))

        mb_msg.mbf_add_string("DOCUMENT_ID", str(documentId))
        mb_msg.mbf_end_list()
        message.mbf_end_message()

        mbuf_p = amb.mbf_create_buffer()
        message.mbf_generate(mbuf_p)
        queue_write_error = amb.mb_queue_write(self.__channel,
                                        subject,
                                        mbuf_p.mbf_get_buffer_data(),
                                        mbuf_p.mbf_get_buffer_data_size(),
                                        'status_buf')

        message.mbf_destroy_object()
        mbuf_p.mbf_destroy_buffer()

        return (queue_write_error == None)

