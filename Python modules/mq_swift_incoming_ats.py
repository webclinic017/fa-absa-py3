"""
This ATS handles all incoming non-Adaptiv SWIFT messages.

History
=======
2017-12-11      CHNG0005220511  Manan Gosh	    DIS go-live
2018-05-11      CHG1000406751   Willie vd Bank  Made changes for securities processing
2018-10-11                      Sadanand Upase  Seperated the handling for MT54X irrespecive of ISIN
2020-03-13      FAOPS-774       Cuen Edwards    Reduce durations of built-in delays (sleeps).
2020-03-18      FAOPS-777       Cuen Edwards    Complete removal of built-in delay.  Added safeguard to allow running
                                                of multiple ATSes.  Update of RTB email address.
2020-05-11      FAOPS-746       Cuen Edwards    Addition of ACK/NACK handler for SARB security transfer MT199s and
                                                start of a refactor.
"""

# FIXME - This should not be necessary.
import sys
sys.path.append(r'/front/arena/apps/lib64/pythonextensionlib27/pymqi')

import acm
from at_email import EmailHelper
import at_logging
import CMQC
import datetime
import demat_config
import demat_isin_mgmt
import demat_settmnt_mgmt
import demat_trade_mgmt
import dis_isin_mgmt
import gen_mq
import gen_swift_functions
import os
from pymqi import MQMIError
import re
from SARBSecurityTransferInstructionProcessor import SARBSecurityTransferInstructionProcessor
import security_settlements
import shutil
import time
import traceback
import uuid


LOGGER = at_logging.getLogger(__name__)
LOGGING_FORMAT = '%(asctime)s,%(msecs)03d %(levelname)s %(message)s'
LOGGING_DATE_FORMAT = '%y%m%d %H%M%S'
at_logging.setFormat(LOGGING_FORMAT, LOGGING_DATE_FORMAT)

# Refactor - config should not be DEMAT specific!
CONFIG = demat_config.get_config()

TO_PROCESS_DIRECTORY_PATH = CONFIG['swift_msg_to_process_dir']
PROCESSED_DIRECTORY_PATH = CONFIG['swift_msg_processed_dir']
ERROR_DIRECTORY_PATH = CONFIG['swift_msg_error_dir']
MANUAL_MESSAGE_DIRECTORY_PATH = CONFIG['swift_msg_to_process_manually_dir']

MQ_MESSENGER = None


class MTMessage(object):
    """
    An object encapsulating information about a received MT Message.
    """

    def __init__(self, message_file_path):
        """
        Constructor.
        """
        self.message_file_path = message_file_path
        self.message_file_name = os.path.basename(message_file_path)
        self.message = _read_file_contents(message_file_path)
        self.message_function = gen_swift_functions.get_msg_function(self.message)
        self.message_type = gen_swift_functions.get_msg_type(self.message)


def start():
    """
    Start hook for module-mode ATS.

    This hook is called when a module-mode ATS is started and is used
    to perform any start-up actions (e.g. connecting to an AMB, etc.).
    If the start hook returns False, then the ATS will shutdown.
    """
    LOGGER.info('Start called at {date_time}.'.format(date_time=datetime.datetime.today()))
    _connect_to_incoming_mq()
    _perform_demat_initialisation()
    _perform_dis_initialisation()


def work():
    """
    Work hook for module-mode ATS.

    This hook is called continuously after a module-mode ATS has been
    started and can be used to perform any periodic work.  It is
    approximately called, max 10 times/sec when idle).
    """
    mt_message = _get_next_mt_message()
    while mt_message is not None:
        try:
            _process_mt_message(mt_message)
            _move_mt_message_file_to_processed_directory(mt_message)
        except Exception as exception:
            LOGGER.exception(exception)
            _move_mt_message_file_to_error_directory(mt_message)
        mt_message = _get_next_mt_message()


def stop():
    """
    Stop hook for module-mode ATS.

    This hook is called when a module-mode ATS is stopped and is used
    to perform any shutdown actions (e.g. disconnecting from an AMB,
    etc.).
    """
    LOGGER.info('Stop called at {date_time}.'.format(date_time=datetime.datetime.today()))
    _disconnect_from_incoming_mq()
    dis_isin_mgmt.deinitialize()


def status():
    """
    Status hook for module-mode ATS.

    This hook is called to retrieve the status of a module-mode ATS.
    """
    return


def _get_next_mt_message():
    """
    Get the next MT Message to process (if any).

    If there is no next MT Message to process, None is returned.
    """
    next_message_file_path = _get_next_message_file_path()
    if next_message_file_path is None:
        return None
    return MTMessage(next_message_file_path)


def _get_next_message_file_path():
    """
    Get the file path of the next message file to process (if any).

    If there is no next message file to process, None is returned.
    """
    # Look for any manual (file) message.
    manual_message_file_path = _get_next_manual_message_file_path()
    if manual_message_file_path is not None:
        # Manual message file found.
        return manual_message_file_path
    # No manual message found - look for any queue message.
    queue_message = _get_next_queue_message()
    if queue_message is not None:
        # Queue message found.
        return _write_queue_message_to_to_process_directory(queue_message)
    # No next message to process.
    return None


def _get_next_manual_message_file_path():
    """
    Get the file path of the next manual message file to process (if
    any).

    If there is no next manual message file to process, None is
    returned.
    """
    for file_name in os.listdir(MANUAL_MESSAGE_DIRECTORY_PATH):
        file_path = os.path.join(MANUAL_MESSAGE_DIRECTORY_PATH, file_name)
        if os.path.isdir(file_path):
            continue
        # A race condition exists if multiple ATS instances are running.
        # More than one ATS may detect and attempt to process a file. To
        # avoid this we attempt to rely on the semantics of the shutil
        # move operation (that is apparently atomic for moves on the same
        # file system).  If the move succeeds, we can assume that this
        # instance of the ATS is the sole processor of the file.
        while os.path.exists(file_path):
            try:
                return _move_manual_message_file_to_to_process_directory(file_path)
            except:
                time.sleep(0.2)
    return None


def _get_next_queue_message():
    """
    Get the next queue message file to process (if any).

    If there is no next queue message to process, None is returned.
    """
    try:
        return MQ_MESSENGER.Get()
    except MQMIError as exception:
        if exception.comp == CMQC.MQCC_FAILED and exception.reason == CMQC.MQRC_NO_MSG_AVAILABLE:
            # Queue is empty.
            return None
        else:
            # Some other MQ error.
            _send_mq_error_mail()
            raise


def _move_manual_message_file_to_to_process_directory(manual_message_file_path):
    """
    Move the specified manual message file to the to_be_processed
    directory and return the path of the message file to be
    processed.
    """
    manual_message_file_name = os.path.basename(manual_message_file_path)
    destination_file_path = TO_PROCESS_DIRECTORY_PATH
    destination_file_name = _generate_message_file_name()
    to_process_message_file_path = _move_file(manual_message_file_path, destination_file_path, destination_file_name)
    message = "Manual message file '{manual_message_file_name}' received and written to "
    message += "'{to_process_message_file_path}'."
    LOGGER.info(message.format(
        manual_message_file_name=manual_message_file_name,
        to_process_message_file_path=to_process_message_file_path
    ))
    return to_process_message_file_path


def _write_queue_message_to_to_process_directory(queue_message):
    """
    Write the specified queue message to_be_processed directory and
    return the path of the message file to be processed.
    """
    destination_file_path = TO_PROCESS_DIRECTORY_PATH
    destination_file_name = _generate_message_file_name()
    to_process_message_file_path = _write_to_file(queue_message, destination_file_path, destination_file_name)
    LOGGER.info("Queue message received and written to '{to_process_message_file_path}'.".format(
        to_process_message_file_path=to_process_message_file_path
    ))
    return to_process_message_file_path


def _generate_message_file_name():
    """
    Generate a unique file name for a message file.
    """
    return str(uuid.uuid4()) + '.txt'


def _process_mt_message(mt_message):
    """
    Process the specified MT Message.
    """
    start_date_time = datetime.datetime.today()
    message_function = mt_message.message_function
    if message_function == 'F01':
        _process_fin_mt_message(mt_message)
    elif message_function == 'F21':
        _process_ack_nack_mt_message(mt_message)
    else:
        raise ValueError("Invalid message function '{message_function}' specified.".format(
            message_function=message_function
        ))
    end_date_time = datetime.datetime.today()
    duration = end_date_time - start_date_time
    LOGGER.info('Processed in: {duration}'.format(duration=duration))


def _move_mt_message_file_to_processed_directory(mt_message):
    """
    Move the file represented by the specified MT Message to the
    processed directory.
    """
    message_file_path = mt_message.message_file_path
    message_file_name = mt_message.message_file_name
    message_function = mt_message.message_function
    message_type = mt_message.message_type
    processed_directory_path = os.path.join(PROCESSED_DIRECTORY_PATH, message_function, message_type)
    _move_file(message_file_path, processed_directory_path)
    message = "Message file '{message_file_name}' moved to processed directory "
    message += "'{processed_directory_path}'."
    LOGGER.info(message.format(
        message_file_name=message_file_name,
        processed_directory_path=processed_directory_path
    ))


def _move_mt_message_file_to_error_directory(mt_message):
    """
    Move the file represented by the specified MT Message to the
    error directory.
    """
    message_file_path = mt_message.message_file_path
    message_file_name = mt_message.message_file_name
    error_directory_path = ERROR_DIRECTORY_PATH
    _move_file(message_file_path, error_directory_path)
    message = "Message file '{message_file_name}' moved to error directory "
    message += "'{error_directory_path}'."
    LOGGER.info(message.format(
        message_file_name=message_file_name,
        error_directory_path=error_directory_path
    ))


def _move_file(source_file_path, destination_directory_path, destination_file_name=None):
    """
    Move the file identified by the source file path to the
    specified destination directory path, optionally renaming the
    file if a destination file name is specified.
    """
    if not os.path.exists(destination_directory_path):
        os.makedirs(destination_directory_path)
    if destination_file_name is None:
        destination_file_name = os.path.basename(source_file_path)
    destination_file_path = os.path.join(destination_directory_path, destination_file_name)
    shutil.move(source_file_path, destination_file_path)
    return destination_file_path


def _write_to_file(file_contents, destination_directory_path, destination_file_name):
    """
    Write the file contents to a file with the specifed destination
    name in the specified destination directory.
    """
    if not os.path.exists(destination_directory_path):
        os.makedirs(destination_directory_path)
    destination_file_path = os.path.join(destination_directory_path, destination_file_name)
    with open(destination_file_path, 'w') as destination_file:
        destination_file.write(file_contents)
    return destination_file_path


def _read_file_contents(read_file_path):
    """
    Read the contents of the file at the specified file path.
    """
    with open(read_file_path, 'rt') as read_file:
        return read_file.read()


def _process_fin_mt_message(mt_message):
    """
    Process the specified FIN MT Message.
    """
    message_type = mt_message.message_type
    LOGGER.info('MT{message_type} message received.'.format(
        message_type=message_type
    ))
    message = mt_message.message
    # FIXME - The way messages are routed to handlers needs serious cleanup!
    # Because 901/902/903 must be handled differently for trade_mgmt messages
    if _is_demat_trade_mgmt_message(message) and message_type in ['598-901', '598-902', '598-903']:
        demat_trade_mgmt.trade_mgmt_incoming(message, message_type)
    # Separating the handling for MT54X incoming messages irrespective of ISIN
    elif message_type in ['544', '545', '546', '547', '548']:
        demat_func_for_msgtype[message_type](message, message_type)
    else:
        isin = gen_swift_functions.get_isin(message)
        if isin and isin[0:3] == 'ZAG':
            message_file_name = mt_message.message_file_name
            dis_func_for_msgtype[message_type](message, message_type, message_file_name)
        else:
            demat_func_for_msgtype[message_type](message, message_type)


def _process_ack_nack_mt_message(mt_message):
    """
    Process the specified ACK/NACK MT Message.
    """
    message_type = mt_message.message_type
    LOGGER.info('ACK/NACK message received for MT{message_type}.'.format(
        message_type=message_type
    ))
    message = mt_message.message
    # FIXME - The way messages are routed to handlers needs serious cleanup!
    if message_type in list(demat_ack_func_for_msgtype.keys()):
        demat_ack_func_for_msgtype[message_type](message)
    elif SARBSecurityTransferInstructionProcessor.is_handled_swift_ack_nack(message):
        SARBSecurityTransferInstructionProcessor.handle_swift_ack_nack(message)
    else:
        LOGGER.warning("Message not handled.")


def _is_demat_trade_mgmt_message(message):
    """
    Determine whether or not the specified message is a DEMAT trade
    management message
    """
    try:
        return demat_trade_mgmt.is_trade_message(message)
    except:
        return False


def _mt548_processing(message, message_type):
    """
    Perform processing of MT548 messages.
    """
    FAS_548 = False
    try:
        msg_RELA_ref = gen_swift_functions.get_trans_ref_from_tag(':20C::RELA//', message)
        if 'FAS' in msg_RELA_ref[0] or re.search(r"^[0-9]{10}$", msg_RELA_ref[0]):
            security_settlements.process_incoming(message, message_type)
            FAS_548 = True
    except Exception as exception:
        LOGGER.exception(exception)

    if not FAS_548:
        demat_trade_mgmt.trade_mgmt_incoming(message, message_type)


def _perform_demat_initialisation():
    """
    Perform any DEMAT initialisation.
    """
    global demat_func_for_msgtype
    demat_func_for_msgtype = dict()
    demat_func_for_msgtype['598-154'] = demat_isin_mgmt.isin_mgmt_incoming
    demat_func_for_msgtype['598-901'] = demat_isin_mgmt.isin_mgmt_incoming  # Format Rejection - ISIN Mgmt
    demat_func_for_msgtype['598-902'] = demat_isin_mgmt.isin_mgmt_incoming  # Invalid Content - ISIN Mgmt
    demat_func_for_msgtype['598-171'] = demat_trade_mgmt.trade_mgmt_incoming
    demat_func_for_msgtype['564'] = demat_trade_mgmt.trade_mgmt_incoming
    demat_func_for_msgtype['566'] = demat_trade_mgmt.trade_mgmt_incoming
    demat_func_for_msgtype['298-128'] = demat_settmnt_mgmt.settmnt_mgmt_incoming
    demat_func_for_msgtype['548'] = _mt548_processing
    demat_func_for_msgtype['544'] = security_settlements.process_incoming
    demat_func_for_msgtype['545'] = security_settlements.process_incoming
    demat_func_for_msgtype['546'] = security_settlements.process_incoming
    demat_func_for_msgtype['547'] = security_settlements.process_incoming
    global demat_ack_func_for_msgtype
    demat_ack_func_for_msgtype = dict()
    demat_ack_func_for_msgtype['598-155'] = demat_isin_mgmt.process_ack_nack


def _perform_dis_initialisation():
    """
    Perform any DIS initialisation.
    """
    dis_isin_mgmt.initialize()
    global dis_func_for_msgtype
    dis_func_for_msgtype = dict()
    dis_func_for_msgtype['598-154'] = dis_isin_mgmt.isin_mgmt_incoming
    dis_func_for_msgtype['564'] = dis_isin_mgmt.trade_mgmt_incoming
    global dis_ack_func_for_msgtype
    dis_ack_func_for_msgtype = dict()
    dis_ack_func_for_msgtype['598-155'] = dis_isin_mgmt.process_ack_nack


def _connect_to_incoming_mq():
    """
    Connect to the incoming MQ.
    """
    global MQ_MESSENGER
    if MQ_MESSENGER is None:
        MQ_MESSENGER = gen_mq.MqMessenger('MeridianInCustMq', True)
        LOGGER.info('Connected to incoming MQ.')


def _disconnect_from_incoming_mq():
    """
    Disconnect to the incoming MQ.
    """
    if MQ_MESSENGER is not None:
        MQ_MESSENGER.Disconnect()
        LOGGER.info('Disconnected from incoming MQ')


def _send_mq_error_mail():
    """
    Send email notification for MQ exception.
    """
    email_from = 'ABCapITRTBAMFrontAre@absa.africa'
    email_to = CONFIG['mq_connection_notifications']
    environment = acm.FInstallationData.Select('').At(0).Name()
    email_subject = 'Front Arena Incoming SWIFT ATS MQ Failure - ' + environment
    email_body = traceback.format_exc()
    email_helper = EmailHelper(body=email_body, subject=email_subject, mail_to=email_to,
        mail_from=email_from, body_type=EmailHelper.BODY_TYPE_HTML, sender_type=EmailHelper
        .SENDER_TYPE_SMTP, host=EmailHelper.get_acm_host())
    email_helper.send()
