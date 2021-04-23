""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLMessageRouter.py"
import acm
import time
import uuid
import FOperationsUtils as Utils
import FACLParameters

_messageType = 'FACL_ARML'
_messageVersion = '1.0'
_embeddedArMLMessage = 'ARML_MSG'

class FACLAMBArMLMessage:
    def __init__(self, ambModule, armlMsg, source):
        self._ambModule = ambModule
        self._mbfMsg = self._ambModule.mbf_start_message(None, _messageType, _messageVersion, None, source)
        
        if type(armlMsg) == str:
            armlMsg = {_embeddedArMLMessage:armlMsg}        
        if type(armlMsg) == dict:
            for k, v in armlMsg.iteritems():
                self._mbfMsg.mbf_add_string(k, v)
            
        self._mbfMsg.mbf_end_message()
        self._mbuf_p = self._ambModule.mbf_create_buffer()
        self._mbfMsg.mbf_generate(self._mbuf_p)

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        self._mbfMsg.mbf_destroy_object()
        self._mbuf_p.mbf_destroy_buffer()

    def QueueWrite(self, channel, subject):
        queue_write_error = self._ambModule.mb_queue_write(channel,
                                               subject,
                                               self._mbuf_p.mbf_get_buffer_data(),
                                               self._mbuf_p.mbf_get_buffer_data_size(),
                                               'status_buf')
        if queue_write_error:
            raise Exception('Could not write to queue')

class FACLArMLFromAMB:
    _buf = None
    _msg = None
    def __init__(self, ambModule, data_p):
        self._buf = ambModule.mbf_create_buffer_from_data(data_p)
        self._msg = self._buf.mbf_read()

    def Extract(self):
        source = self._msg.mbf_find_object('SOURCE').mbf_get_value()
        xmlFromMessage = self._msg.mbf_find_object(_embeddedArMLMessage).mbf_get_value()
        return (source, xmlFromMessage) 

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        self._msg.mbf_destroy_object()
        self._buf.mbf_destroy_buffer()


class FACLReadFromAMB:
    def __init__(self, receiverMBName, ambModule=None):
        self._ambModule = __import__('amb') if ambModule is None else ambModule
        self._subject=''
        self._reader = self._ambModule.mb_queue_init_reader(receiverMBName, self.amb_cb_function_reader, self)

    @staticmethod
    def amb_cb_function_reader(channel, event, arg):
        arg._EventCallbackReader(channel, event)

    def _EventCallbackReader(self, channel, event):
        eventName = self._ambModule.mb_event_type_to_string(event.event_type)
        if eventName == 'Message':
            if event.message.subject == self._subject:
                self._messageData = self._ambModule.mb_copy_message(event.message)
                self._ambModule.mb_queue_accept(self._reader, event.message, 'ok')
                self._receivedMessage=True

    def Take(self, secondsToWait, subject):
        self._subject=subject
        self._receivedMessage = False
        self._messageData = None
        self._ambModule.mb_queue_enable(self._reader, self._subject)
        startTime = time.clock()
        while not self._receivedMessage and time.clock() < startTime + secondsToWait:
            self._ambModule.mb_poll()
            if not self._receivedMessage:
                time.sleep(0.02)
        self._ambModule.mb_queue_disable(self._reader, self._subject)
        if not self._receivedMessage:
            raise Exception('Timed out waiting for message')

        extractor=FACLArMLFromAMB(self._ambModule, self._messageData.data_p)
        return extractor.Extract() 

class FACLWriteToAMB:
    def __init__(self, senderMBName, ambModule=None):
        self._ambModule = __import__('amb') if ambModule is None else ambModule
        self._writer = self._ambModule.mb_queue_init_writer(senderMBName, self.amb_cb_function_writer, self)

    @staticmethod
    def amb_cb_function_writer(channel, event, arg):
        arg._EventCallbackWriter(channel, event)

    def _EventCallbackWriter(self, channel, event):
        pass

    def Send(self, armlMsg, subject, source):
        ambMessage=FACLAMBArMLMessage(self._ambModule, armlMsg, source)
        with ambMessage:
            ambMessage.QueueWrite(self._writer, subject)

class FACLMessageRouter:
    def __init__(self, senderMBName, senderSource, timeout, receiverMBName, ambModule=None, reconnect = 0):
        self._ambModule = __import__('amb') if ambModule is None else ambModule
        self._senderSource = senderSource
        self._senderMBName = senderMBName
        self._timeout = timeout
        self._receiverMBName = receiverMBName
        self._writer = None
        self._reconnect = reconnect
        self._channels = self._FetchChannels()
        assert len(self._channels), 'Must have at least one channel available'

    def _FetchChannels(self):
        from FACLParameters import ConnectorATSSettings
        from inspect import getmembers, isclass
        
        # Every nested class in ConnectorATSSettings represents a channel
        channelClasses = [c for _, c in getmembers(ConnectorATSSettings) if isclass(c)]
        channels = [c.channel for c in channelClasses]

        if 'FACL_ADMIN' in channels:
            channels.remove('FACL_ADMIN')
            
        return channels
    
    def _GetSendSubject(self, obj):
        if obj and obj.IsKindOf(acm.FTrade):
            subject = '%s/%s' % (self._senderSource, self._GetSubjectForTrade(obj))
            id = 'Trade %d' % obj.Oid()
        else:
            subject = '%s/FACL_ADMIN' % self._senderSource
            id = '%s %d' % (obj.Class(), obj.Oid()) if obj else '<No object>'
        Utils.LogVerbose('Routing %s to %s' % (id, subject))
        return subject
            
    def _GetSubjectForTrade(self, trade):
        originalTrade = trade.OriginalOrSelf()
        index = originalTrade.Oid() % len(self._channels)
        return self._channels[index]

    def _GetWriter(self):
        if not self._writer or self._reconnect:
            self._writer = FACLWriteToAMB(self._senderMBName, self._ambModule)
        return self._writer

    def _GetReplySubject(self):
        return "FACL_REPLY/{0}_{1}".format(acm.User().Name(), str(uuid.uuid4()))

    def RouteMessagePersistentWithReply(self, obj, armlMsg):
        sendSubject = self._GetSendSubject(obj)
        replySubject = self._GetReplySubject()
        self._GetWriter().Send(armlMsg, sendSubject, replySubject)
        reader = FACLReadFromAMB(self._receiverMBName, self._ambModule)
        source, reply = reader.Take(self._timeout, replySubject)
        return reply
    
    def RouteMessage(self, obj, armlMsg):
        self._GetWriter().Send(armlMsg, self._GetSendSubject(obj), '')
