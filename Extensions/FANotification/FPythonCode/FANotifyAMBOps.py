"""---------------------------------------------------------------------------
MODULE
    FANotifyAMBOps - Interprocess communication of messages from ATS
    and AMBA to the requesting PRIME user via AMB (Prime LOG window)

DESCRIPTION
    This module sends log messages to AMB and then AMB receiver
    will notify these log messages to user by sending it to
    Prime LOG window. All the message get stored in AMB.

---------------------------------------------------------------------------"""

import amb
import FLogger
import acm

logger = FLogger.FLogger(name='FANotification', keep=True, \
                    logToConsole=True, logToPrime=False)

def event_cb(channel, event, arg):
    (channel, amb.mb_event_type_to_string(event.event_type))
    eventstring= amb.mb_event_type_to_string(event.event_type)
    if eventstring == 'Message':
        amb.mb_queue_accept(channel, event.message, 'ok')
    elif eventstring == 'Disconnect':
        AMBNotification.SENDER_INSTANCES = {}
        AMBNotification.RECEIVER_INSTANCES = {}

def event_cb_notify(channel, event, AMBNotification):
    """Callback function for Messages and Statuses. Choose which Handler to use"""
    eventstring= amb.mb_event_type_to_string(event.event_type)
    if eventstring == 'Message':
        AMBNotification.event_cb_notification \
                (channel, event, AMBNotification.handle_received_message_to_arena_log)
    elif eventstring == 'Disconnect':
        AMBNotification.SENDER_INSTANCES = {}
        AMBNotification.RECEIVER_INSTANCES = {}
                
def notification_sender(message_broker, source_of_notification):
    return AMBNotification.initiate_notification_writer(message_broker, source_of_notification)

def notification_receiver(message_broker, source_of_notification):
    receiver_obj = AMBNotification.initiate_notification_reader(message_broker, source_of_notification)
    if receiver_obj.reader_handle:
        receiver_obj.poll()
    return receiver_obj
    
def notification_receiver_id():
    return AMBNotification.reader_handle
    
def notification_sender_id():
    return AMBNotification.writer_handle
    
    
    

class AMBNotification(object):
    """
    Pass notifications between two Front Arena processes.
    Uses AMB to pass notifications.

    """

    text_buffer = ''
    writer_handle = None
        
    SENDER_INSTANCES = {}
    RECEIVER_INSTANCES = {}
    
    MESSAGE_BROKER = None
    SOURCE_OF_NOTIFCATION = None
    
    @classmethod
    def initiate_notification_writer(cls, message_broker='', source_of_notification=''):
        if message_broker:
            cls.MESSAGE_BROKER = message_broker
        if source_of_notification:
            cls.SOURCE_OF_NOTIFCATION = source_of_notification
        instance_name = cls.SOURCE_OF_NOTIFCATION + '_NOTIFICATION_WRITER'
        channel_name = 'NOTIFY_SENDER'
        '''This is for returning same instance of class when called multiple times from a process. 
        The newly created instances are saved as class variables in the dictionary formats.
        '''
        if cls.SENDER_INSTANCES.get(instance_name):
            return cls.SENDER_INSTANCES.get(instance_name)
        else:
            if cls.MESSAGE_BROKER and cls.SOURCE_OF_NOTIFCATION:
                instance = AMBNotification(cls.MESSAGE_BROKER, channel_name, amb_connection_for='Sender', source_of_notification=cls.SOURCE_OF_NOTIFCATION)
                cls.SENDER_INSTANCES[instance_name] = instance
                return instance
            else:
                logger.ELOG("MessageBroker and Source of Notification not specified.")
            
    
            
    @classmethod
    def initiate_notification_reader(cls, message_broker='', source_of_notification='', user=''):
        instance_name = source_of_notification + '_NOTIFICATION_READER'
        if not user:
            user = acm.FUser[acm.UserName()].Name()
        channel_name = 'NOTIFY_' + user
        
        '''This is for returning same instance of class when called multiple times from a process. 
        The newly created instances are saved as class variables in the dictionary formats.
        '''
        if cls.RECEIVER_INSTANCES.get(instance_name):
            return cls.RECEIVER_INSTANCES.get(instance_name)
        else:
            instance = AMBNotification(message_broker, channel_name, amb_connection_for='Receiver', \
                        source_of_notification=source_of_notification)
            cls.RECEIVER_INSTANCES[instance_name] = instance
            return instance
            

    def __init__(self, amb_address, amb_channel, amb_connection_for='Receiver',source_of_notification=''):
        """
        amb_connection_for decides if this is the Sender object, appending messages to a
        self.text_buffer until sending off with send_text, or if this is a Receiver
        receiving the message and passing it to handle_received_message where the true
        logic is defined.

        """
        
        self.amb_channel = amb_channel # Entry in AMB System table
        self.msgType = 'NOTIFICATION'
        if source_of_notification:
            self.msgType = source_of_notification + '_' +'NOTIFICATION' #Name (Envelope) of message: [NOTIFICATION]
        self.subject =  self.msgType + '/' + acm.UserName()
        self.text_buffer = ''
        self.reader_handle = None
        self.writer_handle = None
        self.amb_connection_for = amb_connection_for
        self.amb_connection = False

        if self.amb_connection_for.strip().upper() == 'RECEIVER':
            # Create a channel for reading
            try:
                self.reader_handle = amb.mb_queue_init_reader(self.amb_channel, \
                                                    event_cb_notify, self)
                amb.mb_queue_enable(self.reader_handle, self.subject)
                AMBNotification.reader_handle = self.reader_handle
            except Exception as e:
                if str(e) == 'Not Connected':
                    if self.InitAMBConnection(amb_address):
                        try:
                            self.reader_handle = amb.mb_queue_init_reader(self.amb_channel, \
                                                        event_cb_notify, self)
                            amb.mb_queue_enable(self.reader_handle, self.subject)
                            AMBNotification.reader_handle = self.reader_handle                    
                        except RuntimeError:
                            error_message = "Could not open channels <%s> to receive log messages"%self.amb_channel
                            logger.ELOG(error_message)
                            RECEIVER_INSTANCES = {}
                    else:
                        RECEIVER_INSTANCES = {}
                else:
                    error_message = "Could not open channels <%s> to receive log messages"%self.amb_channel
                    logger.ELOG(error_message)
                    RECEIVER_INSTANCES = {}

        elif self.amb_connection_for.strip().upper() == 'SENDER':
            # Create a channel for writing to AMB
            self.clear_buffer() # The message buffer being built up until sent
            try:
                self.writer_handle = amb.mb_queue_init_writer(self.amb_channel, event_cb, self)
                AMBNotification.writer_handle = self.writer_handle
            except Exception as e:
                if str(e) == 'Not Connected':
                    if self.InitAMBConnection(amb_address):
                        try:
                            self.writer_handle = amb.mb_queue_init_writer(self.amb_channel, event_cb, self)
                            AMBNotification.writer_handle = self.writer_handle
                        except RuntimeError:
                            error_message = "Could not open channels <%s> to send log messages"%self.amb_channel
                            logger.ELOG(error_message)
                            SENDER_INSTANCES = {}
                    else:
                        SENDER_INSTANCES = {}
                else:
                    error_message = "Could not open channels <%s> to send log messages"%self.amb_channel
                    logger.ELOG(error_message)
                    SENDER_INSTANCES = {}

    def InitAMBConnection(self, amb_address):
        logger.DLOG("Connecting to AMB %s"%amb_address)
        try:
            amb_server_details = amb_address
            split_amb_address = amb_server_details.split('/')
            if len(split_amb_address) == 3 and split_amb_address[2].startswith('0x'):
                split_amb_address[2]  = base64.b64decode(split_amb_address[2][2:])
                amb_server_details = '/'.join(split_amb_address)
            amb.mb_init(amb_server_details)
            self.amb_connection = True
        except:
            error_message = "Could not connect to AMB <%s>"%amb_address
            logger.ELOG(error_message)
            self.amb_connection = False
        return self.amb_connection

    def poll(self):
        """Wait for incoming messages"""
        amb.mb_poll()

    def __del__(self):
        self.reader_handle = None
        self.writer_handle = None

    def clear_buffer(self):
        """Clear an accumulated text buffer"""
        self.text_buffer = ''

    def handle_received_message(self, mes):
        """A default function for a receiving AMBNotification. This is where you decide
        actions for a received message.

        """

        logger.LOG('Handling', mes.mbf_object_to_string( ))

    def handle_received_message_to_arena_log(self, mes):
        """Capture the message and send to acm.Log"""
        log_message = ''
        mes.mbf_find_object('SOURCE')
        notifyObject = mes.mbf_next_object()
        line = notifyObject.mbf_first_object()

        while line:
            log_message = log_message + line.mbf_get_value()
            line = notifyObject.mbf_next_object()
            if line:
                log_message = log_message + '\n'
        if log_message:
            acm.Log(log_message)

    def event_cb_notification(self, channel, event, handleFunction):
	"""Callback function for Messages and Statuses"""
        (channel, amb.mb_event_type_to_string(event.event_type))
        #eventstring= amb.mb_event_type_to_string(event.event_type)
        eventstring = amb.mb_event_type_to_string(event.event_type)
        try:
            if eventstring == 'Message':
                buf = amb.mbf_create_buffer_from_data(event.message.data_p)
                mes = buf.mbf_read( )
                handleFunction(mes)
                amb.mb_queue_accept(channel, event.message, 'ok')
        except Exception:
            return

    def sender_id():
	""" Returns notification sender channel id"""
        return AMBNotification.writer_handle
    sender_id = staticmethod(sender_id)

    def add_listening_subject(self, subject):

        """If you had set one Subject in the initialization,
        you might want to add a second subject, so that you
        will receive Notifications from two sources

        """

        amb.mb_queue_enable(self.reader_handle, subject)

    def add_text(text):
	"""Adds messages to buffer"""
        if AMBNotification.text_buffer:
            AMBNotification.text_buffer += ' \n'
        AMBNotification.text_buffer += text
    add_text = staticmethod(add_text)

    def send_text(fwdOnly, user, source, amb_notify_sender, text=''):
        """Send the accumulated buffer. May contain additional
        last text in the call.

        """
        if text:
            AMBNotification.add_text(text)

        # generate notification message
        msg_source = source + '_NOTIFICATION'
        message = amb.mbf_start_message(None, 'NOTIFICATION', '4.0', None, 'NOTIFICATION')
        mb_msg=message.mbf_start_list('NOTIFICATION')

        # Add Time to messages
        mes_time = message.mbf_find_object('TIME')
        local_time = acm.Time.UtcToLocal(str(mes_time.mbf_get_value()))
        msg_time = str(local_time) + ': '
        for line in AMBNotification.text_buffer.split(' \n'):
            line = line.strip()
            if line:
                mb_msg.mbf_add_string('LINE', msg_time + line)

        mb_msg.mbf_end_list( )

        message.mbf_end_message( )

        buffer = amb.mbf_create_buffer( )
        message.mbf_generate(buffer)

        for usr in user:
            msg_subject = source + '_NOTIFICATION' + '/' + usr
            #msg_subject = self.msgType + '/' + usr
	    if fwdOnly:
                # TRANSIENT LOGS

                if amb_notify_sender:
                    try:
                        amb.mb_queue_forward(int(amb_notify_sender), msg_subject.strip(), \
                                        buffer.mbf_get_buffer_data( ), \
                                        buffer.mbf_get_buffer_data_size( ))
                    except Exception as e:
                        if str(e) == 'Not Connected':
                            logger.LOG('AMB connection lost: Cannot write log to AMB')
                        elif str(e) == 'Not Found':
                            AMBNotification.initiate_notification_writer()
                        else:
                            logger.ELOG("Error while mb_queue_forward <%s>"%str(e))
            else:
                # PERSISTENT LOGS
                if amb_notify_sender:
                    try:
                        amb.mb_queue_write(int(amb_notify_sender), msg_subject.strip(), \
                                        buffer.mbf_get_buffer_data( ), \
                                        buffer.mbf_get_buffer_data_size( ), line)
                    except Exception as e:
                        if str(e) == 'Not Connected':
                            logger.LOG('AMB connection lost: Cannot write log to AMB')
                        elif str(e) == 'Not Found':
                            AMBNotification.initiate_notification_writer()
                        else:
                            logger.ELOG("Error while mb_queue_write <%s>"%str(e))


        AMBNotification.text_buffer = ''
    send_text = staticmethod(send_text)
