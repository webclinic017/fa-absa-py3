"""
Custom logging handlers which can be used
with the logger objects derived from logging.Logger.
"""
import logging
import os
import sys
from datetime import date
from email.mime.text import MIMEText
from logging import (ERROR,
                     Formatter,
                     getLogger,
                     INFO,
                     Handler,
                     LogRecord,
                     FileHandler)
from smtplib import SMTP

import acm

import FBDPString


def log_uncaught_exceptions(logger):
    """
    Set up a hook to log uncaught exceptions using the provided logger.
    """

    def log_exception(exc_type, exc_value, traceback):
        """
        Use the logger object from an outer scope to log an exception
        described by the provided exc_info parameters.
        """
        # the logger.exception method cannot be used,
        # because it ignores the provided exc_info tuple
        logger.error("", exc_info=(exc_type, exc_value, traceback))

    sys.excepthook = log_exception


class BufferingSMTPHandler(Handler):
    """
    A logging handler which sends a single e-mail with all the logging records
    to the specified e-mail addresses when closed.

    If no logging record of a certain severity or higher has been encountered,
    no e-mail message will be sent (unless configured to always send e-mails).
    """

    def __init__(self,
                 to_addresses,
                 from_address='ABCapITRTBFrontArena@absa.africa',
                 subject=None,
                 server_address=None,
                 trigger_levels=None,
                 always_send=False):
        Handler.__init__(self)
        self.to_addresses = to_addresses
        if server_address is None:
            server_address = acm.GetCalculatedValue(
                None,
                acm.GetDefaultContext().Name(),
                "mailServerAddress").Value()
        if subject is None:
            subject = "Logging messages"
        self.server_address = server_address
        self.from_address = from_address
        self.subject = subject
        self.trigger_levels = trigger_levels or [ERROR]
        self.always_send = always_send
        self.buffer = []

        formatter = Formatter("%(levelname)s: %(message)s")
        self.setFormatter(formatter)

    def emit(self, record):
        """
        Emit a record by appending it to the buffer.
        Also check if the triggering severity has been reached.
        """
        if record.levelno in self.trigger_levels:
            self.buffer.append(record)

    def close(self):
        """
        Send e-mails with all the logging records
        if a record with a triggering or higher severity
        has been encountered.

        Then close the handler.
        """
        if self.always_send:
            # ensure that there is at least one message
            if not self.buffer:
                log_record = LogRecord(name=__name__,
                                       level=INFO,
                                       pathname=None,
                                       lineno=None,
                                       msg="No log messages encountered.",
                                       args=None,
                                       exc_info=None,
                                       func=None)
                self.buffer.append(log_record)
        if self.buffer:
            env = acm.FDhDatabase['ADM'].InstanceName()
            message = "\n".join([self.format(record)
                                 for record in self.buffer])
            mime_message = MIMEText(message)
            mime_message["From"] = self.from_address
            mime_message["Subject"] = '{} - {}'.format(self.subject, env)
            mime_message["To"] = ",".join(self.to_addresses)
            logger = getLogger(__name__)
            try:
                connection = SMTP(self.server_address)
                logger.info("sending e-mails")
                connection.sendmail(self.from_address,
                                    self.to_addresses,
                                    mime_message.as_string())
                connection.quit()
            except:
                logger.exception("Unable to send e-mail with logging messages.")
            else:
                logger.info("e-mails sent")
        Handler.close(self)


class LogmeHandler(Handler):

    def __init__(self, process_name, ael_main_args):
        logging.Handler.__init__(self, logging.NOTSET)
        self.logme = FBDPString.logme
        self.logme.setLogmeVar(process_name,
                               ael_main_args['Logmode'],
                               ael_main_args['LogToConsole'],
                               ael_main_args['LogToFile'],
                               ael_main_args['Logfile'],
                               ael_main_args['SendReportByMail'],
                               ael_main_args['MailList'],
                               ael_main_args['ReportMessageType'])
        self.logme(None, "START")

    def emit(self, record):
        """
        """

        """
        msg_type    string    Type of message
                    'INFO'  -   Information (default)
                    'WARNING' - Anything making a task being fulfilled in an
                                unusual way.
                    'ERROR' -   Anything making a task not being fulfilled.
                    'START' -   Also date and time will be printed
                    'FINISH'-   Script finished successfully
                    'ABORT' -   Script aborted due to error
                    'DEBUG' -   For developer purposes

        """
        if logging._levelNames[record.levelno] == "EXCEPTION":
            self.logme(self.format(log_record), "ERROR")
        else:
            self.logme(self.format(log_record), logging._levelNames[record.levelno])

    def close(self):
        # this will be called two time, not sure why it is called from loggin, when it has been removed
        pass


class CounterHandler(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.warnings_counter = 0
        self.errors_counter = 0

    def reset(self, msg_tracker=None):
        if msg_tracker != None:
            self.warnings_counter -= msg_tracker.warnings_counter
            self.errors_counter -= msg_tracker.errors_counter
        else:
            self.warnings_counter = 0
            self.errors_counter = 0

        if self.warnings_counter < 0:
            self.warnings_counter = 0
        if self.errors_counter < 0:
            self.errors_counter = 0

    def emit(self, record):
        if record.levelno == 30:
            self.warnings_counter += 1
        if record.levelno == 40 or record.levelno == 50:
            self.errors_counter += 1

    def close(self):
        pass

    def __str__(self):
        return "Warnings: {0}, Errors: {1}".format(self.warnings_counter, self.errors_counter)

class FileHandlerMINT(FileHandler):
    LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                '-35s %(lineno) -5d: %(tag) -10s: %(message)s')
    DEFAULT_PATH = "D:\\Data\\LogFiles\\Prime\\"

    def __init__(self, env_name, log_path, log_tag="", msg_tag=""):
        self.tag = msg_tag
        if log_tag:
            log_name = os.path.join(log_path, "{0}_{1}_{2}.log".format(env_name, log_tag, date.today().strftime("%Y%m%d")))
        else:
            log_name = os.path.join(log_path, "{0}_{1}.log".format(env_name, date.today().strftime("%Y%m%d")))
        if not os.path.exists(os.path.dirname(log_name)):
            try:
                print("Creating log directory: ", os.path.dirname(log_name))
                os.makedirs(os.path.dirname(log_name))
            except OSError as ex:
                if ex.errno != errno.EEXIST:
                    print(ex)
        self.log_path = log_name

        FileHandler.__init__(self, self.log_path)
        self.setFormatter(Formatter(FileHandlerMINT.LOG_FORMAT))

    def close(self):
        # this will be called two time, not sure why it is called from loggin, when it has been removed
        FileHandler.close(self)

    def emit(self, record):
        if self.tag:
            record.tag = self.tag
        FileHandler.emit(self, record)

    @staticmethod
    def close_all():
        ''' Close all the existing FileHandlerMINT instances
        '''
        try:
            # This will create the handler that will output to the console
            logging.basicConfig()
            logging.root.debug("Closing existing MINT handlers")

            to_remove=[]
            for handler in logging.root.handlers:
                # isinstance is not working, couldn't find why
                if "FileHandlerMINT" in str(type(handler)):
                    logging.root.info("Closing existing handler: '%s'", handler.log_path)
                    to_remove.append(handler)

            for handler in to_remove:
                logging.root.removeHandler(handler)

        except Exception:
            logging.root.exception("Something went wrong.")

    @staticmethod
    def get_instance(log_path, log_tag="", msg_tag=""):
        import acm
        return FileHandlerMINT(acm.FDhDatabase['ADM'].InstanceName(), log_path, log_tag, msg_tag)
