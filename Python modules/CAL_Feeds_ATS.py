import collections
import gc

import acm
import amb

import CAL_Feeds_Reporting
from at_logging import getLogger
from AMB_Reader_Writer import AMB_Reader
from CAL_Feeds_Processing import CalFeedsProcessor
from SecureConfigReader import SecureConfigReader


LOGGER = getLogger(__name__)
WORKER_QUEUE = collections.deque()
ATS_PARAMS = {
    'message_number': 0,
}
CONFIG_MODULE = 'CALConfigSettings'


def set_up_csv_file():
    cal_output = CAL_Feeds_Reporting.CalFeedsOutput()
    cal_output.initialise_csv_file()
    cal_output.initialise_control_file()


def trade_event_cb(channel, event, arg):
    event_string = amb.mb_event_type_to_string(event.event_type)
    if event_string == "Message":
        ATS_PARAMS['message_number'] += 1
        WORKER_QUEUE.append((amb.mb_copy_message(event.message), channel, ATS_PARAMS['message_number']))
    else:
        LOGGER.info("Unspecified event..." + event_string + " type.")


def start():
    set_up_csv_file()
    
    secureConfigReader = SecureConfigReader(CONFIG_MODULE)
    
    amba_server_ip = secureConfigReader.getElementValue('AMBAServerIP')
    mb_name =  secureConfigReader.getElementValue('MBName')
    subject_string = secureConfigReader.getElementValue('SubjectSubstring')
    username = secureConfigReader.getElementValue('UserName')
    password = secureConfigReader.getElementValue('Password')
    ambaConnectionMethod = secureConfigReader.getElementValue('AmbaConnectionMethod')
    
    try:
        LOGGER.info("Trades ATS start-up commencing at %s" % acm.Time.TimeNow())
        try:
            amb_reader = AMB_Reader(amba_server_ip, mb_name, trade_event_cb, [subject_string])
            if ambaConnectionMethod == 'init2':
                LOGGER.info("Attempting init2 AMBA connection.")
                if not amb_reader.open_AMB_Receiver_Connection_Init2(username, password):
                    LOGGER.error("Could not open Receiver AMB connection.")
                    raise Exception("Could not open Receiver AMB connection.")
            else:
                LOGGER.info("Attempting AMBA connection.")
                if not amb_reader.open_AMB_Receiver_Connection():
                    LOGGER.error("Could not open Receiver AMB connection.")
                    raise Exception("Could not open Receiver AMB connection.")               
        except RuntimeError:
            LOGGER.exception("Trades ATS start-up failed.")
        else:
            LOGGER.info(">>> Waiting for trade events...")
            LOGGER.info("Trades ATS start-up completed.")
        amb.mb_poll()
    except Exception:
        LOGGER.exception("Start-up failed.")


def work():
    while len(WORKER_QUEUE) > 0:
        event_copy, channel_number, amb_message_number = WORKER_QUEUE.popleft()
        LOGGER.info('Started processing: %s' % amb_message_number)
        message_buffer = amb.mbf_create_buffer_from_data(event_copy.data_p)
        amba_message = message_buffer.mbf_read()
        cal_feeds_processor = CalFeedsProcessor(amba_message)
        cal_feeds_processor.process_trade_ambas()
        amb.mb_queue_accept(channel_number, event_copy, str(amb_message_number))
        amba_message.mbf_destroy_object()
        message_buffer.mbf_destroy_buffer()
        collect_garbage()
        LOGGER.info(">>> Waiting for trade events...")


def stop():
    return


def status():
    return


def collect_garbage():
    acm.Memory().GcWorldStoppedCollect()
    gc.collect()
