'''
Created on 12 Jul 2016

@author: conicova
'''
from contextlib import contextmanager
import logging

from at_logging_handlers import BufferingSMTPHandler, LogmeHandler, CounterHandler

OUTPUT = 60  # higher value so that it is not turned off
REPORT = 70

FA_DASHBOARD_LOGGER_CREATED = False

class LazyLogger(object):
    '''We don't want to initialise it before it is required (basicConfig).
    '''
    def __init__(self):
        self._LOGGER = None

    @property
    def LOGGER(self):
        if not self._LOGGER:
           # This has to be the logger that writes to the MQ, otherwise important data will be lost
           self._LOGGER = getLogger(__name__)

        return self._LOGGER

LAZY_LOGGER = LazyLogger()

class FALogger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET):
        logging.Logger.__init__(self, name, level)
        self.msg_tracker = CounterHandler()
        self.addHandler(self.msg_tracker)

    def reset_msg_tracker(self):
        self._reset_msg_tracker_children()
        self._reset_msg_tracker_parent(self.msg_tracker)

    def _reset_msg_tracker_parent(self, msg_tracker):
        if self.parent and hasattr(self.parent, "_reset_msg_tracker_parent"):  # don't know how to check if isinstance
            self.parent._reset_msg_tracker_parent(msg_tracker)
        self.msg_tracker.reset(msg_tracker)

    def  _reset_msg_tracker_children(self):
        for logger_name in logging.Logger.manager.loggerDict.keys():
            if logger_name.startswith(self.name+"."):
                child_logger = getLogger(logger_name)
                if hasattr(child_logger, "_reset_msg_tracker_children"):
                    child_logger._reset_msg_tracker_children()
                    child_logger.msg_tracker.reset()

    def output(self, file_path, msg=None, *args, **kwargs):
        """
        Log 'msg % args' with severity 'OUTPUT'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.output("c:/tmp/report.csv", "interesting problem", exc_info=1)
        """
        self._log(OUTPUT, file_path, args, **kwargs)
        self.info("Secondary output wrote to %s", file_path)  # just for RTB
        if msg:
            self.info(msg, *args, **kwargs)

    def report(self, report_id, *args, **kwargs):
        self._log(REPORT, report_id, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        logging.Logger.warning(self, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        logging.Logger.error(self, msg, *args, **kwargs)

logging.addLevelName(OUTPUT, "OUTPUT")
logging.addLevelName(REPORT, "REPORT")
logging.setLoggerClass(FALogger)

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                '-35s %(lineno) -5d: %(message)s')

LOG_FORMAT = '%(levelname) -10s %(message)s'

# These are RabbitMQ related modules. No need to display messages.
logging.getLogger("async_publisher").setLevel(logging.WARNING)
logging.getLogger("at_log_message").setLevel(logging.CRITICAL)


def getLogger(source="", level=logging.INFO, format=LOG_FORMAT):
    """
    This function calls the basicConfig, that creates the default handler
    !!! and sets the level and format.
    Call basicConfig before this function to set the level and format

    Arguments:
    source - the module name that initialises the logger (use __name__)
    """
    global FA_DASHBOARD_LOGGER_CREATED
    logging.basicConfig(level=level, format=format)
    logger_name = "fa_dashboard"
    if not FA_DASHBOARD_LOGGER_CREATED:
        # we want to make sure that the root fa_dashboard logger is created
        # so that we don't loose some messages (child->parent)
        logging.getLogger(logger_name)
        FA_DASHBOARD_LOGGER_CREATED = True
    if source:
        if not source.startswith(logger_name):
            logger_name = "{0}.{1}".format(logger_name, source)
        else:
            logger_name = source
    logger = logging.getLogger(logger_name)

    return logger

from at_log_dummy_handler import DummyHandler as LogHandler

LOGGING_UTIL = {}

def prepareHandler(process_name, run_name=None, timeout=None, is_async=True, ael_main_args={}, use_mq_handler=True):
    """ The process (BP) name identifies the handler.
    There might be multiple BP running at the same time.
    """
    basicConfig(level=logging.INFO, format=LOG_FORMAT)
    if not process_name:
        LAZY_LOGGER.LOGGER.warning("Trying to create a handler without a name.")
        return None
    if process_name not in LOGGING_UTIL:
        logging_util = LoggingUtil(process_name, run_name, timeout, is_async, ael_main_args, use_mq_handler)
        LOGGING_UTIL[process_name] = logging_util

    return LOGGING_UTIL[process_name]

def closeHandler(process_name, is_silent=False):
    """ This will send a closing message only to the appropriate
    handler."""
    if not process_name:
        return
    if process_name in LOGGING_UTIL:
        LOGGING_UTIL[process_name].close_handler(getLogger(), is_silent)
        LOGGING_UTIL.pop(process_name)
    else:
        LAZY_LOGGER.LOGGER.warning("Trying to close an unexisting process: {0}".format(process_name))

def setFormat(format, datefmt=None):
    '''Forces the change of the output format.
    '''
    fmt = logging.Formatter(format, datefmt)
    for handler in logging.root.handlers:
        handler.setFormatter(fmt)

def basicConfig(**kwargs):
    '''This has efect only when called the first time'''
    logging.basicConfig(**kwargs)

@contextmanager
def bp_start(process_name, run_name=None, timeout=None, is_async=True, is_silent=False, ael_main_args={}, use_mq_handler=True):
    try:
        yield prepareHandler(process_name, run_name, timeout, is_async, ael_main_args, use_mq_handler)
    except Exception:
        LAZY_LOGGER.LOGGER.exception("Something went wrong.")
        # make sure that the process is marked as failed
        raise
    finally:
        closeHandler(process_name, is_silent)

# we need the datetime in the message
ATS_LOG_FORMAT = '%(asctime)s %(levelname) -10s %(message)s'
def ats_start(process_name, format=ATS_LOG_FORMAT):
    setFormat(format)
    if not process_name.startswith("ats."):
        process_name = "ats." + process_name
    return prepareHandler(process_name)


def ats_stop(handler):
    closeHandler(handler)


class LoggingUtil(object):
    """ Each business process (BP) needs to have its own handler. There might be multiple BP
    running at the same time, and when finishing one of them, all the other should remain
    alive. """
    def __init__(self, process_name, run_name=None, timeout=None, is_async=True, ael_main_args={}, use_mq_handler=True):
        self.loggers = []
        self.process_name = process_name
        self.run_name = run_name
        self.timeout = timeout
        self.is_async = is_async
        self.ael_main_args = ael_main_args
        self.handler = None
        self.logme_handler = None
        self.buffer_smtp_handler = None

        if use_mq_handler:
            try:
                self.handler = LogHandler(self.process_name, logging.INFO, self.run_name, self.timeout, self.is_async, self.ael_main_args)
                self.append_handler(self.handler, getLogger())
                LAZY_LOGGER.LOGGER.info("Started: %s", self.handler.process_run_name)
            except:
                LAZY_LOGGER.LOGGER.debug("Handler not initialised.", exc_info=1)
        if 'Logmode' in ael_main_args and False:  # turn this off until not ready
            self.logme_handler = LogmeHandler(process_name, ael_main_args)
            self.append_handler(self.logme_handler, getLogger())
        if ael_main_args.get('BSMTPSendReportByMail'):
            levels = [logging.getLevelName(level) for level
                      in ael_main_args['BSMTPTriggerLevel']]
            self.buffer_smtp_handler = BufferingSMTPHandler(
                ael_main_args['BSMTPMailList'].split(','),
                subject=ael_main_args['BSMTPEmailSubject'],
                trigger_levels=levels)
            self.append_handler(self.buffer_smtp_handler, getLogger())

    def append_handler(self, handler, logger):
        """Append the existing handler to the provided logger"""
        # the handler will be added only once
        logger.addHandler(handler)
        # keep only unique loggers
        if logger not in self.loggers:
            self.loggers.append(logger)

    def _close(self):
        if self.handler:
            self.handler.close()
        if self.logme_handler:
            self.logme_handler.close()
        if self.buffer_smtp_handler:
            self.buffer_smtp_handler.close()
        for logger in self.loggers:
            logger.removeHandler(self.handler)

    def close_handler(self, logger, is_silent=False):
        if not is_silent and self.handler:
            # This has to be sent to MQ so that we know that the process has ended
            logger.info("Finished:{0}".format(self.handler.process_run_name))
        if self.logme_handler:
            self.logme_handler.logme(None, "FINISH")
        self._close()

def get_FBDPGuiLogVariables():
    import FBDPGui
    return FBDPGui.LogVariables()

def get_buffering_smtp_variables():
    """ Adds the following ael variables:
        BSMTPSendReportByMail - bool
        BSMTPEmailSubject - string
        BSMTPMailList - string (emails delimited by ',')
        BSMTPReportMessageType - list (predefined values)
    """
    result = []

    send_report_by_mail = 'Send reports by email when procedure is finished'
    mail_list = 'Comma separated list of email recipients'
    report_message_type = (
        'Triggering logging level. Logging records of a selected severity '
        'or higher will be send by email.')

    result.append(['BSMTPSendReportByMail',
                   'Send Report By Mail_Logging',
                   'int', [1, 0], None, 0, 0,
                   send_report_by_mail, None])
    result.append(['BSMTPEmailSubject',
                    'Email Subject_Logging',
                    'string', None, None,
                    0, 0, '', None])
    result.append(['BSMTPMailList',
                   'Mail List_Logging',
                   'string', None, None,
                   0, 0, mail_list])
    levels = filter(lambda l: not isinstance(l, int), logging._levelNames.values())
    result.append(['BSMTPTriggerLevel',
                   'Log Level_Logging',
                   'string', levels, 'ERROR',
                   2, 1, report_message_type, None])

    return result
