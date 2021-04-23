"""---------------------------------------------------------------------------
MODULE
    FANotification - Interprocess communication of messages from ATS
    and AMBA to the requesting PRIME user via AMB (Prime LOG window),
    MAIL and Prime popup message window.

DESCRIPTION
    This module sends log messages to AMB and then AMB receiver
    will notify these log messages to user by sending it to
    Prime LOG window. It also sends messages via Mail, Prime
    message window based on user specified Notification media.
    FANotification creates instance of FLogger internally to log messages.
    
    Parameters:
    ===========
    The notifier can instantiated using the FANotification class constructor and can be reinitialized 
    using the Reinitialize() method. The parameters to the constructor are below. With the
    exception of name, they are also the parameters to Reinitialize.
         
    name - String parameter: name of the notifier. notifiers with different names will be indepenedent. 
        The notifier name is used as a logging source while logging message. FLogger instance is created 
        using same name.
         
    notification_media - String / List parameter: 
        PRIME_LOG for notfying logs in Prime log window. All the log messages are stored in AMB.
        PRIME_LOG_TRANSIENT for notfying logs in Prime log window. log message are not stored in AMB. 
            If Prime is not up and running then the notification mesages written to AMB via ATS and AMBA will be lost.
        MAIL for notfying errors and warnings via email
        MESSAGE for notifying errors and warnings via prime message window.
        OFF for no notifications. In this case the logs are logged in respective process i.e. in ATS and AMBA log file.
            The logs are not sent to Prime log window.
         
    notify_level - String parameter: TRACK for notifying LOG level messages, DEBUG for notifying 
        debug (DLOG) level messages, WARNING for notifying warning (WLOG) messages, ERROR for notifying 
        error (ELOG) messages, SUCCESS for notifying success messages
         
    logging_level - String parameter: INFO for logging LOG level messages, DEBUG for logging debug 
        level messages, WARN for logging warning messages, ERROR for logging error messages.
         
    message_broker - String parameter: AMB address to connect and used for stroing notification messages. 
    
    user - ACM user to notify logs.
                         
    user_emails - String / List parameter: email address to send notification messages via Email.
                      
    smtp_server - String parameter: STMP server name that is used for sending emails.       
         
     
    Reinitialize Parameter:
    =======================
    The paramters to Reinitialize are the same as above except there is no name parameter.
     
    
    Pre-requisite:
    ===============
    * All below pre-requisite is needed only when the notification_media is set as PRIME_LOG or PRIME_LOG_TRANSIENT.
     
    FANotification writes log messages to AMB. FANotification AMB writer is initialized under the hook 
    when creating instance of FANotification. All the written messages to AMB will get logged in Prime 
    window by calling AMB reader with message subject.
     
     1. For writing AMB messages, channel NOTIFY_SENDER should be created in AMB database
     2. For receiving AMB messages, channel NOTIFY_(USER) should be created in AMB database. 
        USER is the Prime logged in user name. Example 'NOTIFY_SMITH'
     3. In case of using more than one users to notify messages to, user should create channels for each user.
        Example 'NOTIFY_JOHN', 'NOTIFY_ARENASYS'.
     4. In order to receive the notification messages from AMB in Prime, a AMB reader should be initialized. 
        This can also be done in Prime-startup script so that user will get all the logs from AMB as soon 
        he logins. The reader can to be initialized as below:
     
        import FANotification
        message_broker = 'localhost:9999'
        source_of_notification = 'MyProduct' # Name passed to the FANotification 
        FANotification.NotifyReceiver(message_broker, source_of_notification)
     
    Usage:
    =======
    To use FANotification you must obtain an instance of the notifier via the FANotification constructor.
    The constructor uses the default values from the FParameters defined in FANotification module. User can
    configure these FParameter according to their needs.
         
    The FANotification class is designed as a shared state class insuring that all notifier objects 
    (existing and new) always share the same state if the have the same name.
     
    The notifier for a given name can be reintialized via the Reinitialize() method.  
     
    One can reinitialize it at any time. The state of all existing notifier objects with the 
    same name are automatically updated to reflect the new state of the notifier. 
     
    Notification should be done through the interface functions:
         
         INFO      - information
         WARN     - warnings
         ERROR     - errors
         DEBUG     - debug information
         SUCCESS     - critical information
         
         or 
    
    When using existing FLogger and passing parameter flogger to FANotification as described above
    
        LOG      - information
        WLOG     - warnings
        ELOG     - errors
        DLOG     - debug information
        CLOG     - critical information
         
        or 
         
        info     - information
        warn     - warnings
        error    - errors
        debug    - debug information
        critical - critical information
        
    In order to get notification via email or message, NotifyByMailsAndMessages() needs to be called.
     
    Example Usage:
    ===============
    import FANotification
     
    notifier = FANotification.FANotification(name='MyProduct')
     
    notifier.INFO('This is a info message')
    notifier.Reintialize(user='SMITH') 
    notifier.DEBUG('This is a debug message')
    notifier.Reinitialize(notification_media=MAIL) 
    notifier.ERROR('This is a error message')
                          
    See more example at bottom.

---------------------------------------------------------------------------"""
try:
    import threading
except ImportError:
    threading = None
import smtplib
    
import acm, ael
import FLogger

import FANotifyUtils
import FANotifyAMBOps
from FANotifyAMBOps import AMBNotification

logger = FLogger.FLogger('FANotification')

# Deafult Notification parameters
default_notification_media = 'OFF'
default_notify_level = 'ERROR'
default_logging_level = 'INFO'
default_message_broker = 'localhost:9100'
default_user_emails = ''
default_smtp_server = ''
default_user = [acm.FUser[acm.UserName()].Name()]


#_lock is used to serialize the construction of FANotification objects.
_lock = None

def _acquireLock():
    """Acquire the module-level lock for serializing access to shared data. This
    should be released with _releaseLock()"""
    global _lock
    if (not _lock) and threading:
        _lock = threading.RLock()
    if _lock:
        _lock.acquire()
    
def _releaseLock():
    """Release the module-level lock acquired by calling _acquireLock()"""
    if _lock:
        _lock.release()
        


class FANotification(object):
    """This contains different notify level functions to log messages.
    A log message is logged to Prime LOG window/Mail/Message window
    based on user specified notification media.

    """
    
    NOTIFY_INSTANCES = {}
    
    def __new__(cls, *args, **kwargs):
        name = None
        if args:
            name = args[0]
        if not name and kwargs:
            name = kwargs.get('name')
            
        if cls.NOTIFY_INSTANCES.get(name):     
            return cls.NOTIFY_INSTANCES.get(name)
        else:
            return super(FANotification, cls).__new__(cls)
                    
    def __init__(self, name=None, notification_media=default_notification_media, notify_level=default_notify_level, \
                    logging_level=default_logging_level, message_broker=default_message_broker, user=default_user, \
                    user_emails=default_user_emails, smtp_server=default_smtp_server, *args):
        # The name if notification is used as a log source while notifying messages        
        if not name or not isinstance(name, str):
            raise Exception("Notification name is mandatory.")
        
        _acquireLock()
        
        # Validate values of parameters
        self.validate_parameter_values(notification_media, notify_level, logging_level, user, message_broker, smtp_server)
        
        try:
            self.notification_name = name
            # return same instane when initiating second time
            instance = FANotification.NOTIFY_INSTANCES.get(name)
            
            if not instance:
                FANotification.NOTIFY_INSTANCES[name] = self
                # Create new instance of FLogger with logger name as Notification name 
                self.logger = FLogger.FLogger(name=name, keep=True, logToConsole=True, logToPrime=False)
            self.set_parameter_values(name, notification_media, notify_level, logging_level, message_broker, \
                                user_emails, smtp_server, user)
        finally:
            _releaseLock()
                        
    def validate_parameter_values(self, notification_media, notify_level, logging_level, user, message_broker, smtp_server):
        self._validate_notification_media(notification_media)
        self._validate_notify_level(notify_level)
        self._validate_logging_level(logging_level)
        self._validate_user(user)
        notification_media_list = FANotifyUtils.string_as_list(notification_media)
        if not message_broker and ('PRIME_LOG' in notification_media_list or 'PRIME_LOG_TRANSIENT' in notification_media_list):
            raise Exception("No Message Broker specified by user")
                        
        if not smtp_server and 'MAIL' in notification_media_list:
            raise Exception("SMTP server not specified for notification via MAIL")
            
    def _validate_notification_media(self, notification_media):
        notification_media_list = []
        if notification_media:
            notification_media_list = FANotifyUtils.string_as_list(notification_media)
            if 'PRIME_LOG' not in notification_media_list and 'PRIME_LOG_TRANSIENT' not in notification_media_list and  \
                    'MAIL' not in notification_media_list and 'MESSAGE' not in notification_media_list and 'OFF' not in \
                    notification_media_list:
                raise Exception("Invalid value of notification_media <%s>"%notification_media)
                
    def _validate_notify_level(self, notify_level):
        if notify_level:
            if notify_level not in ['TRACK', 'DEBUG', 'WARNING', 'ERROR', 'SUCCESS']:
                raise Exception("Invalid value of notify_level <%s>"%notify_level)
                                
    def _validate_logging_level(self, logging_level):
        if logging_level:
            if logging_level not in ['INFO', 'DEBUG', 'WARN', 'ERROR']:
                raise Exception("Invalid value of logging_level <%s>"%logging_level)
                
    def _validate_user(self, user):
        if user:
            acm_users, invalid_users = FANotifyUtils.get_acm_user(user)
            if invalid_users:
                logger.WLOG("Invalid ACM users %s"%invalid_users)
            if not acm_users:
                raise Exception("No valid ACM user found to notify logs")
            
    def set_parameter_values(self, notification_name, notification_media, notify_level, logging_level, message_broker, \
                            user_emails, smtp_server, user):                            
        # Set parameters passed to FANotification
        self.logging_source = FANotifyUtils.string_padding(notification_name, 12)
        self.notification_media = FANotifyUtils.string_as_list(notification_media)
        self.notify_level = notify_level
        self.logging_level = logging_level
        self.message_broker = message_broker
        self.notification_message_source = notification_name 
        self.user_emails = FANotifyUtils.string_as_list(user_emails)
        self.smtp_server = smtp_server
        if user:
            self.user, invalid_users = FANotifyUtils.get_acm_user(user)
                
        self.set_amb_notify_sender()
    
    def set_amb_notify_sender(self):
        # Initiate AMB notification writer
        self.amb_notify_sender = None
        # get instance of AMBNotification class and initiate AMB writer
        if 'PRIME_LOG' in self.notification_media or 'PRIME_LOG_TRANSIENT' in self.notification_media:
            try:
                notify_sender_channel = self.notification_name + '_NOTIFY_SENDER'
                obj = FANotifyAMBOps.notification_sender(self.message_broker, self.notification_message_source)
                self.amb_notify_sender = obj.sender_id()
            except Exception as e:
                self.logger.ELOG(str(e), exc_info=1)
            
        if 'OFF' in self.notification_media:
            self.amb_notify_sender = None
            self.logger.Reinitialize(logToConsole=True, logToPrime=False)
            
    def Reinitialize(self, notification_media=None, notify_level=None, logging_level=None, message_broker=None, \
                    user=None, user_emails=None, smtp_server=None, flogger=None):
        """ Reinitialize NotifyUser"""
        if _lock is not None:
            if notification_media:
                self.notification_media = FANotifyUtils.string_as_list(notification_media)
                self.set_amb_notify_sender()
            if notify_level:
                self.notify_level = notify_level
            if logging_level:
                self.logging_level = logging_level
            if message_broker:
                self.message_broker = message_broker
            if user:
                self.user, invalid_users = FANotifyUtils.get_acm_user(user)
                if invalid_users :
                    self.logger.WLOG("Invalid ACM users %s"%invalid_users)
            if user_emails:
                self.user_emails = FANotifyUtils.string_as_list(user_emails)
            if smtp_server:
                self.smtp_server = smtp_server
            if flogger:
                self.logger = flogger
                self.logger.Reinitialize(keep=True, logToConsole=False, logToPrime=True)
            
    def INFO(self, msg, *args, **kwargs):  
        """Use to log and notify log level messages"""
        
        #self.logger.LOG(msg, *args)
        self._message_logger(msg, 'INFO', 'INFO', *args, **kwargs)
        
    def SUCCESS(self, msg, *args, **kwargs):
        """Use to log and notify success messages"""
        self._message_logger(msg, 'INFO', 'SUCCESS',  *args, **kwargs)
        
    def WARN(self, msg,  *args, **kwargs):
        """Use to log and notify warning messages"""
        self._message_logger(msg, 'WARN', 'WARN',  *args, **kwargs)
        
    def ERROR(self, msg,  *args, **kwargs):
        """Use to log and notify error messages"""
        #self.logger.ELOG(msg)
        self._message_logger(msg, 'ERROR', 'ERROR',  *args, **kwargs)
        
    def DEBUG(self, msg,  *args, **kwargs):
        """Use to log debug messages"""
        self._message_logger(msg, 'DEBUG', 'DEBUG', *args, **kwargs)
        
    def _message_logger(self, msg,  log_level, notify_level, *args, **kwargs):
        self._log_message(msg, log_level,  *args, **kwargs)
        msg = self._format_message(msg, notify_level)
        self._notify_message(msg, notify_level)
    
    def _format_message(self, msg, notify_level):
        """Adds log source i.e. notification name to the log messages"""
        log_source = self.logging_source
	if len(self.logging_source) < 12:
            log_source = self.logging_source + (12-len(self.logging_source)) * ' ' 
        else:
            log_source = self.logging_source[:12]
            
        if len(notify_level) < 7:
            notify_level  =  notify_level + ' '*(7-len(notify_level))
        msg = notify_level + ' [%s] ' % log_source + msg
        return msg
        
    def _log_message(self, msg,  log_type,  *args, **kwargs):       
        """log messages to Prime LOG window"""
        msg_txt = msg
        if log_type == 'INFO' and self.logging_level in ['INFO', 'DEBUG']:
            self.logger.LOG(msg_txt, *args, **kwargs)
        elif log_type == 'DEBUG' and self.logging_level in ['DEBUG']:
            self.logger.Reinitialize(level=2)
            self.logger.DLOG(msg_txt, *args, **kwargs)
        elif log_type == 'WARN' and self.logging_level in ['WARNING', 'INFO', 'DEBUG']:
            self.logger.WLOG(msg_txt,   *args, **kwargs)
        elif log_type == 'ERROR' and self.logging_level in ['ERROR', 'INFO', 'WARNING', 'DEBUG']:
            self.logger.ELOG(msg_txt,  *args, **kwargs)
                
    def _notify_message(self, msg, notify_typ):
        if self.amb_notify_sender and ('PRIME_LOG_TRANSIENT' in self.notification_media or \
                                        'PRIME_LOG' in self.notification_media):
            if notify_typ == 'INFO' and self.notify_level in ['TRACK', 'DEBUG']:
                self._send_notification_to_amb(msg, notify_typ)
            if notify_typ == 'SUCCESS':
                self._send_notification_to_amb(msg, 'INFO')
                self.NotifyByMailsAndMessages(msg, 'Success Notification')  
            if notify_typ == 'WARN' and self.notify_level in ['TRACK', 'DEBUG', 'WARNING', 'SUCCESS']:
                self._send_notification_to_amb(msg, notify_typ)
            if notify_typ == 'ERROR' and self.notify_level in ['ERROR', 'WARNING', 'SUCCESS', 'DEBUG', 'TRACK']:
                self._send_notification_to_amb(msg, notify_typ)
            if notify_typ == 'DEBUG' and self.notify_level in ['DEBUG']:
                self._send_notification_to_amb(msg, notify_typ)
                
    def _send_notification_to_amb(self, msg_txt, notify_typ):
        """writes the log message to AMB queue"""
        if msg_txt:
            if 'PRIME_LOG_TRANSIENT' in self.notification_media:
                transient_log = True
            elif 'PRIME_LOG' in self.notification_media:
                transient_log = False
            AMBNotification.send_text \
                    (transient_log, self.user, \
                    self.notification_message_source, self.amb_notify_sender, str(msg_txt))
    
    def NotifyByMailsAndMessages(self, msg_text=None, msg_subject='WARNING/ERROR Notification', notify_level='WARNING'):
        """This sends the error and warning logs via mails and Prime message window. Any INFO, DEBUG 
        logs are not notified via mails and message. A single mail is sent for all warnings and errors
        clubed together. Similarly single message window in pop-up for all warnings and errors. 
        A new different mail or message is sent for any SUCCESS logs.
        """
        warn_msg_lst = []
        error_msg_lst = []
        info_msg_lst = []
        debug_msg_lst = []
        msg_txt = ''
        
        warn_msg_lst = self.logger.GetWarningMessages(all=False)
        error_msg_lst = self.logger.GetErrorMessages(all=False)
        info_msg_lst = self.logger.GetInfoMessages(all=False)
        debug_msg_lst = self.logger.GetDebugMessages(all=False)
        
        notify_msg_dict = {'WARNING': [(warn_msg_lst, 'WARN'), (error_msg_lst, 'ERROR')],
                            'ERROR': [(error_msg_lst, 'ERROR')],
                            'TRACK': [(info_msg_lst, 'INFO'), (warn_msg_lst, 'WARN'), (error_msg_lst, 'ERROR')],
                            'DEBUG': [(info_msg_lst, 'INFO'), (warn_msg_lst, 'WARN'), (error_msg_lst, 'ERROR'), (debug_msg_lst, 'DEBUG')],
                            }
            
        msg_typ_lst = notify_msg_dict.get(notify_level, None)
        if msg_typ_lst:
            for each_msg_typ in msg_typ_lst:
                for msg in each_msg_typ[0]:
                    msg_txt = msg_txt + ' ' + each_msg_typ[1] + ' ' + msg[0] + '\n'
                   
        self.logger.ClearAllMessages(all=False)
        
        if msg_text:
            msg_txt = msg_txt + msg_text
        
        if msg_txt:
            subject = self.notification_name.strip() + ' ' + msg_subject
            if 'MESSAGE' in self.notification_media:
                self.send_message_window(msg_txt, subject)
            if 'MAIL' in self.notification_media:
                self.send_mail(msg_txt, subject)
    
    def send_message_window(self, msg_txt, subject):
        """Notify logs via Prime message window"""
        
        for usr in self.user:
            self.logger.DLOG("Notify logs via message window to <%s>" % (usr))
            try:
                ael.sendmessage(usr, subject, msg_txt)
            except Exception as e:
                self.logger.ELOG("Failed to notify logs in Prime Message Window: %s"%str(e))

    def send_mail(self, msg_txt, subject):
        """Notify logs via Mail"""
        msg_txt = msg_txt.replace('\n', '\n\n')
        mail_from = acm.UserName()
        if acm.User().Email():
            mail_from = acm.User().Email()
            self.logger.DLOG("use mail FROM=%s" %acm.User().Email())
        else:
            self.logger.WLOG("No email found for acm user <%s>"%acm.UserName())
            self.logger.DLOG("use mail FROM=%s" %acm.UserName())

        email_ids = []
        if self.user:
            for usr in self.user:
                if acm.FUser[usr].Email():
                    email_ids.append(acm.FUser[usr].Email())
        if self.user_emails:
            for email in self.user_emails:
                email_ids.append(email)
        if email_ids:
            try:
                for email in set(email_ids):
                    FROM = mail_from
                    TO = email.strip()
                    message = """\
From: %s
To:%s
Subject: %s

%s
""" % (FROM, TO, subject, str(msg_txt))
                    server = smtplib.SMTP(self.smtp_server)
                    self.logger.DLOG("Notify logs via mails to <%s>" % (TO))
                    server.sendmail(FROM, TO, message)
                    server.quit()
            except Exception as e:
                self.logger.WLOG('%s', str(e))
    
    @classmethod
    # This is to initiate AMB receiver to read and log notification messages from AMB to Prime window.
    def NotifyReceiver(cls, message_broker, source_of_notification):
        receiver_obj = FANotifyAMBOps.notification_receiver(message_broker, source_of_notification)
        
    @classmethod
    # This is to initiate AMB sende to read and log notification messages from AMB to Prime window.
    def NotifySender(cls, message_broker, source_of_notification):
        receiver_obj = FANotifyAMBOps.notification_sender(message_broker, source_of_notification)
        
    @classmethod
    def AMBSenderId(cls):
        return FANotifyAMBOps.notification_sender_id()
    
    @classmethod
    def AMBReceiverId(cls):
        return FANotifyAMBOps.notification_receiver_id()
                
    # get methods
    def Name(self):
        return self.notification_name
        
    @property        
    def NotificationMedia(self):
        return self.notification_media
    @NotificationMedia.setter
    def NotificationMedia(self, value):
        self._validate_notification_media(value)
        self.notification_media = value
        self.set_amb_notify_sender()
        
    @property        
    def NotifyLevel(self):
        return self.notify_level
    @NotifyLevel.setter
    def NotifyLevel(self, value):
        self._validate_notify_level(value)
        self.notify_level = value
        
    @property        
    def LoggingLevel(self):
        return self.logging_level
    @LoggingLevel.setter
    def LoggingLevel(self, value):
        self._validate_logging_level(value)
        self.logging_level = value
        
    @property        
    def MessageBroker(self):
        return self.message_broker
    @MessageBroker.setter
    def MessageBroker(self, value):
        self.message_broker = value
        
    @property        
    def UserEmails(self):
        return self.user_emails
    @UserEmails.setter
    def UserEmails(self, value):
        self.user_emails = value
        
    @property        
    def STMPServer(self):
        return self.smtp_server
    @STMPServer.setter
    def STMPServer(self, value):
        self.smtp_server = value
        
    @property        
    def NotifyUsers(self):
        return self.user
    @NotifyUsers.setter
    def NotifyUsers(self, value):
        self._validate_user(value)
        self.user = value
        
    @property        
    def NotifyLogger(self):
        return self.logger
        
            
    class FANotificationLogger(FLogger.FLogger):
        LOGGER_INSTANCES = {}
        def __new__(cls, *args, **kwargs):
            logger = None
            name = None
            if args:
                name = args[0]
            if len(args) >= 9:
                logger = args[8]
            if kwargs:
                if not name:
                    name = kwargs.get('name')
                if not logger:
                    logger = kwargs.get('flogger')
            if not logger:
                raise Exception("No logger instance specified for logging")
            if not name:
                raise Exception("Notification Name is mandatory")
                
            if logger and name:
                if logger.name != name:
                    raise Exception("logger name should match with Notification name")
                
            if FANotification.FANotificationLogger.LOGGER_INSTANCES.get(name):     
                return FANotification.FANotificationLogger.LOGGER_INSTANCES.get(name)
            else:
                return super(FANotification.FANotificationLogger, cls).__new__(cls)
        
        def __init__(self, name=None, notification_media=default_notification_media, notify_level=default_notify_level, \
                    logging_level=default_logging_level, message_broker=default_message_broker, user=default_user, \
                    user_emails=default_user_emails, smtp_server=default_smtp_server, flogger=None, *args):
            self.name = name
            self.flogger = flogger
            self.flogger.Reinitialize(keep=True, logToConsole=True, logToPrime=False)
            if not FANotification.FANotificationLogger.LOGGER_INSTANCES.get(name):
                FANotification.FANotificationLogger.LOGGER_INSTANCES[name] = self
            self.notify_obj = FANotification(name=name, notification_media=notification_media, notify_level=notify_level, \
                    logging_level=logging_level, message_broker=message_broker, user=user, \
                    user_emails=user_emails, smtp_server=smtp_server)
            self.notify_obj.logger = self.flogger
                        
        @property        
        def Notifier(self):
            return self.notify_obj
        
        def LOG(self, msg, *args, **kwargs):
            self.notify_obj.INFO(msg, *args, **kwargs)
            
        def WLOG(self, msg, *args, **kwargs):
            self.notify_obj.WARN(msg, *args, **kwargs)
            
        def DLOG(self, msg, *args, **kwargs):
            self.notify_obj.DEBUG(msg, *args, **kwargs)
            
        def ELOG(self, msg, *args, **kwargs):
            self.notify_obj.ERROR(msg, *args, **kwargs)
            #self.flogger.ELOG(msg,args, kwargs )
            
        def CLOG(self, msg, *args, **kwargs):
            self.notify_obj.ERROR(msg, *args, **kwargs)
            
        def info(self, msg, *args, **kwargs):
            self.notify_obj.INFO(msg, *args, **kwargs)
            
        def debug(self, msg, *args, **kwargs):
            self.notify_obj.DEBUG(msg, *args, **kwargs)
            
        def warn(self, msg, *args, **kwargs):
            self.notify_obj.WARN(msg, *args, **kwargs)
            
        def error(self, msg, *args, **kwargs):
            self.notify_obj.ERROR(msg, *args, **kwargs)
            
        def critical(self, msg, *args, **kwargs):
            self.notify_obj.ERROR(msg, *args, **kwargs)
    
    
        
def test1():
    # First initiate notify receiver to read messages from AMB in Prime
    FANotification.NotifyReceiver('localhost:9100', 'FrontArena')
    
    # Use FANotification to define logs
    notifier = FANotification('FrontArena', notification_media='PRIME_LOG', notify_level='WARNING')
    notifier.INFO('This is notifier info message')
    notifier.WARN('This is notifier warning message')
    notifier.ERROR('This is notifier error message')
    notifier.DEBUG('This is notifier debug message')
    notifier.SUCCESS('This is notifier success message')
    
def test2():
    # First initiate notify receiver to read messages from AMB in Prime
    FANotification.NotifyReceiver('localhost:9100', 'FrontArena')
    
    # Use FANotification to define logs
    notifier = FANotification('FrontArena', notification_media='PRIME_LOG, MAIL, MESSAGE', \
                                            notify_level='DEBUG')
    notifier.INFO('This is notifier info message')
    notifier.WARN('This is notifier warning message')
    notifier.ERROR('This is notifier error message')
    notifier.DEBUG('This is notifier debug message')
    notifier.SUCCESS('This is notifier success message')
    
    # Notify via mail or message 
    notifier.NotifyByMailsAndMessages()
    
def test3():
    # Logger in exisitng product
    logger = FLogger.FLogger('FrontArena')
    logger.LOG("This is log via FLogger")
    logger.ELOG("This is elog via FLogger")
    
    
    # Pass this logger and logger name to FANotification.FANotificationLogger with other FANotification arguments
    logger = FANotification.FANotificationLogger(name='FrontArena', flogger=logger)
    
    # Use logger similar to FLogger used on existing product
    logger.LOG("This is log via FANotification")
    logger.ELOG("This is elog via FANotification")
    
    # Notify via mail or message 
    logger.Notifier.NotifyByMailsAndMessages()
    
    
        
if __name__ == "FANotification":
    # Example 1: Using FANotification to notify logs in Prime window
    #test1()
    # Example 2: Using FANotification to notify logs in Prime window along with mail and message
    #test2()
    # Example 3: Using FLogger of existing product and passing to FANotification 
    #test3()
    pass


