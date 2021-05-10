import sys, time, datetime
sys.path.append(r'/front/arena/apps/lib64/pythonextensionlib27/pymqi')
import CMQC
from pymqi import MQMIError
import amb, acm
import gen_mq
import FSwiftMLUtils, FCashOutUtils
import at_logging

logger = at_logging.getLogger(__name__)
LOGGING_FORMAT = '%(asctime)s,%(msecs)03d %(levelname)s %(message)s'
LOGGING_DATE_FORMAT = '%y%m%d %H%M%S'
at_logging.setFormat(LOGGING_FORMAT, LOGGING_DATE_FORMAT)
MQ_MESSENGER = None
MQ_PARAMS = None
OUTGOING_READER = None
OutgoingMsg_QUEUE = []
VALID_STATES = ['Sent']
VALID_SC = ['FSwiftCashOut', 'FSwiftCashOutMT304', 'FSwiftFXMMConfirmationOut', 'FSwiftNarrativeOut', 'FSwiftSecLendingBorrowingOut', 'FSwiftSecurityConfirmationOut', 'FSwiftSecuritySettlementOut']
writer = None

def _event_Callback(channel, event, arg):
    pass

class MQ_TO_AMBA:

    def __init__(self, TASK_USER, AMB_ADDRESS, AMB_SENDER_NAME, AMB_SUBJECT, SOURCE, MBF_OBJECT, MBF_TAG):
        global MQ_PARAMS
        MQ_PARAMS = TASK_USER
        self.AMB_ADDRESS = AMB_ADDRESS
        self.AMB_SENDER_NAME = AMB_SENDER_NAME
        self.AMB_SUBJECT = AMB_SUBJECT
        self.SOURCE = SOURCE 
        self.MBF_OBJECT = MBF_OBJECT
        self.MBF_TAG = MBF_TAG

    def _start(self):
        logger.info('Start called at {date_time}.'.format(date_time=datetime.datetime.today()))
        try:
            global writer
            amb.mb_init(self.AMB_ADDRESS)
            writer = amb.mb_queue_init_writer(self.AMB_SENDER_NAME, _event_Callback, None)
            _connect_to_mq(True, True)
        except Exception as error:
            logger.error('Exception occurred while swift message processing: %s' % (str(error)))
            
    def _work(self):
        mt_message = _get_next_queue_message()
        while mt_message is not None:
            try:
                write_to_AMB(mt_message, self.SOURCE, self.MBF_OBJECT, self.MBF_TAG, self.AMB_ADDRESS, self.AMB_SENDER_NAME, self.AMB_SUBJECT)
            except Exception as exception:
                logger.error('Failed to process message: %s' % (str(exception)))
            mt_message = _get_next_mt_message()

    def _stop(self):
        logger.info('Stop called at {date_time}.'.format(date_time=datetime.datetime.today()))
        _disconnect_from_mq()
        amb.mb_queue_close(writer)

    def _status(self):
        return


def _connect_to_mq(connectNow = False, useFParameters = False):
    global MQ_MESSENGER
    if MQ_MESSENGER is None:
        MQ_MESSENGER = gen_mq.MqMessenger(MQ_PARAMS, connectNow, useFParameters)
        logger.info('Connected to MQ.')


def _get_next_queue_message():
    try:
        return MQ_MESSENGER.Get(True)
    except MQMIError as exception:
        if exception.comp == CMQC.MQCC_FAILED and exception.reason == CMQC.MQRC_NO_MSG_AVAILABLE:
            # Queue is empty.
            return None
        else:
            logger.error('Failed to connect: %s' % (str(exception.reason)))
            raise


def _put_queue_message(message):
    try:
        return MQ_MESSENGER.Put(message, False)
    except MQMIError as exception:
            logger.error('Failed to connect: %s' % (str(exception.reason)))
            raise


def _disconnect_from_mq():
    if MQ_MESSENGER is not None:
        MQ_MESSENGER.Disconnect()
        logger.info('Disconnected from  MQ')


def event_Callback(channel, event, arg):
    pass
        
        
def is_ACK_NAK(mt_message):
    return '{451:1}' in mt_message or '{451:0}' in mt_message


def is_number(value):
    try:
        value = float(value)
    except ValueError:
        return False
    
    if not value == value:
        return False
    return True


def is_SCANITVIOLATED(mt_message):
    return '405:SCANITVIOLATED' in mt_message


def is_SBL_settlement(Settlement):
    if not Settlement.Trade():
        return False
            
    if Settlement.Trade().TradeInstrumentType() != 'SecurityLoan' and Settlement.Trade().TradeCategory() != 'Collateral':
        return False
    
    if not Settlement.Acquirer():
        return False
    
    if Settlement.Acquirer().Name() != 'SECURITY LENDINGS DESK':
        return False
        
    return True
    
    
def apply_msg_amendments(mt_message):
    # apply SBL external referenece fix for SBL ACK/NAK
    ext_ref =  mt_message[mt_message.find('{108:') + 5: ]
    ext_ref =  ext_ref[:ext_ref.find('}')]
    ref = FSwiftMLUtils.get_field_value(mt_message, '20')
    
    if is_ACK_NAK(mt_message) and is_number(ref):
        sett = acm.FSettlement[ref]
        if sett:
            if is_SBL_settlement(sett):
                mt_message = mt_message.replace(ref, 'FAS-' + str(ref.strip()) + '-0')
                mt_message = mt_message.replace(ext_ref, str(ref.strip()))
                return mt_message
    
    # check if SCANIT IT (Sanctions) message
    if is_SCANITVIOLATED(mt_message) and ext_ref != ref:
        ref = ref.strip()
        if len(ref.split('-')) == 3:
            mt_message = mt_message.replace(ext_ref, ref)
            # update status explanation - should be moved to callback module once we figure out how to
            sett = acm.FSettlement[ref.split('-')[1]]
            if sett:
                doc = sett.Documents().Last()
                if doc:
                    doc.StatusExplanation('SCA: Sanctions Pending')
                    doc.Commit()
    return mt_message
    

def write_to_AMB(mt_message, SOURCE, MBF_OBJECT, MBF_TAG, AMB_ADDRESS, AMB_SENDER_NAME, AMB_SUBJECT):
    if is_ACK_NAK(mt_message):
        AMB_SUBJECT = 'ACKNOWLEDGEMENT'
        
    mt_message = apply_msg_amendments(mt_message)
    
    try:
        message = amb.mbf_start_message(None, 'MESSAGE', "1.0", None, SOURCE)
        mbMessage = message.mbf_start_list(MBF_OBJECT)
        mbMessage.mbf_add_string(MBF_TAG, mt_message)
        mbMessage.mbf_end_list()
        message.mbf_end_message()
        buffer = amb.mbf_create_buffer()
        message.mbf_generate(buffer)
        status = amb.mb_queue_write(writer, AMB_SUBJECT, buffer.mbf_get_buffer_data(), buffer.mbf_get_buffer_data_size(), time.strftime("%Y-%m-%d %H:%M:%S"))
        lastMid = amb.mb_last_write_message_id(writer)
        logger.info("Message %s successfully written to AMB %s" % (lastMid, AMB_ADDRESS))
    except Exception as error:
        logger.error('Exception occurred while swift message processing: %s' % (str(error)))



        
class AMB_TO_MQ:

    def __init__(self, TASK_USER, AMB_ADDRESS, AMB_SENDER_NAME, AMB_SUBJECTS, PAYMENT_TYPE):
        global MQ_PARAMS
        MQ_PARAMS = TASK_USER
        self.AMB_ADDRESS = AMB_ADDRESS
        self.OUTGOING_READER_NAME = AMB_SENDER_NAME
        self.AMB_SUBJECTS = AMB_SUBJECTS
        self.PAYMENT_TYPE = PAYMENT_TYPE

    def _start(self):
        logger.info('Start called at {date_time}.'.format(date_time=datetime.datetime.today()))
        _init_amb_reader(self.AMB_ADDRESS, self.OUTGOING_READER_NAME, self.AMB_SUBJECTS)
        amb.mb_poll()

    def _work(self):
        if list(OutgoingMsg_QUEUE):
            _connect_to_mq(False, True)
            while list(OutgoingMsg_QUEUE):
                try:
                    mt_type = ''
                    msg_id, msg_copy = OutgoingMsg_QUEUE[0]
                    buf = amb.mbf_create_buffer_from_data(msg_copy.data_p)
                    msg = buf.mbf_read()
                    obj = acm.AMBAMessage.CreateSimulatedObject(msg.mbf_object_to_string()) 
                    if obj:
                        if obj.CurrentStateName() in VALID_STATES and  obj.StateChart().Name() in VALID_SC:
                            acm_obj = FSwiftMLUtils.get_acm_object_from_bpr(obj.CurrentStep().BusinessProcess())
                            msg_type = 'MT' + str(FSwiftMLUtils.calculate_mt_type_from_acm_object(acm_obj))
                            mt_msg = FSwiftMLUtils.get_swift_data_from_bpr(obj)
                            obj_type = 'Settlement' if acm_obj.IsKindOf(acm.FSettlement) else 'Confirmation'
                            if get_message_classification(msg_type, acm_obj) == self.PAYMENT_TYPE:
                                logger.info("Adding %s %s with ID %s to MQ" % (msg_type, obj_type, str(acm_obj.Oid())))
                                _put_queue_message(mt_msg)
                    msg.mbf_destroy_object()
                    buf.mbf_destroy_buffer()
                except Exception as error:
                    logger.error('%s Exception occurred while swift message processing: %s' % (mt_type, str(error)))
                    #notifier.DEBUG(str(error), exc_info=1)
                OutgoingMsg_QUEUE.pop(0)
                amb.mb_queue_accept(OUTGOING_READER, msg_copy, 'okay')
            _disconnect_from_mq()

    def _stop(self):
        logger.info('Stop called at {date_time}.'.format(date_time=datetime.datetime.today()))
        amb.mb_queue_close(OUTGOING_READER)


    def _status(self):
        return


def get_message_classification(msg_type, acm_obj):
    if msg_type in ('MT103', 'MT200', 'MT202', 'MT202COV', 'MT199', 'MT299'):
        receivers_bic = FCashOutUtils.get_ordering_institution_bic(acm_obj)[:8]
        senders_bic = FCashOutUtils.get_senders_bic(acm_obj)[:8]
        
        if receivers_bic not in ('ABSAZAJJ', 'ABSAZAJ0'):
            return 'External Payment'
        
        if acm_obj.Currency().Name() == 'ZAR' and receivers_bic == senders_bic and receivers_bic in ('ABSAZAJJ', 'ABSAZAJ0'):
            return 'Internal Payment'
            
    return 'Non Payment'


def _event_reader_cb(reader_channel, event, arg):
    event_string = amb.mb_event_type_to_string(event.event_type)
    if event_string == 'Message':
        copy_of_msg = amb.mb_copy_message(event.message)
        msg_id = amb.mb_last_write_message_id(reader_channel)
        OutgoingMsg_QUEUE.append((msg_id, copy_of_msg))


def _init_amb_reader(AMB_ADDRESS, OUTGOING_READER_NAME, AMB_SUBJECTS):
    global OUTGOING_READER
    amb_reader_inited = False
    try:
        amb.mb_init(AMB_ADDRESS)
        OUTGOING_READER = amb.mb_queue_init_reader(OUTGOING_READER_NAME, _event_reader_cb, None)
        logger.info('Reader %s initialized' % str(OUTGOING_READER_NAME))
        for subject in AMB_SUBJECTS:
            amb.mb_queue_enable(OUTGOING_READER, subject)
            logger.info('Subscribed to subject %s' % subject)
        amb_reader_inited = True
    except Exception as error:
        logger.info("Could not initialize amb reader <'%s'>. App will now exit. %s" % (OUTGOING_READER_NAME, str(error)))
        #notifier.DEBUG(str(error), exc_info=1)
    return amb_reader_inited
