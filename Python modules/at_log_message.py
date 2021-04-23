'''
Created on 28 Jun 2016

@author: conicova
'''
from uuid import uuid4
import json
from datetime import datetime
import logging
import socket
import getpass

LOGGER = logging.getLogger(__name__)
formatter = logging.Formatter()
UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()

class LogRecord(object):
    
    date_time_format = '%Y-%m-%d %H:%M:%S'
    def __init__(self):
        self.created = None
        self.filename = None
        self.funcName = None
        self.levelno = None
        self.lineno = None
        self.module = None
        self.msg = None
        self.name = None
        self.msg_id = 0

    @staticmethod
    def from_logging(log_record, msg_id, handler):
        result = LogRecord()
        created = datetime.fromtimestamp(log_record.created)
        created += UTC_OFFSET_TIMEDELTA 
        result.created = created.strftime(LogRecord.date_time_format) 
        result.filename = log_record.filename
        result.funcName = log_record.funcName
        result.levelno = log_record.levelno
        result.lineno = log_record.lineno
        result.module = log_record.module
        if handler:
            result.msg = handler.format(log_record)
        else:
            result.msg = log_record.msg
        result.name = log_record.name
        result.msg_id = msg_id
        
        return  result
    
    @staticmethod
    def from_json(body):
        result = LogRecord()
        if body:
            result.created = datetime.strptime(body['created'], LogRecord.date_time_format) 
            result.filename = body['filename']
            result.funcName = body['funcName']
            result.levelno = body['levelno']
            result.lineno = body['lineno']
            result.module = body['module']
            result.msg = body['msg']
            result.name = body['name']
            result.msg_id = body['msg_id']
        
        return  result
    
    def __str__(self):
        return "Log Record: {0}".format(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))
    
class SessionInfo(object):
    
    def __init__(self, process_run_name):
        self.ads_address = ''
        self.acm_class = ''
        self.user = ''
        self.data = ''
        self.process_run_name = process_run_name
        self.hostname = ''
        self.pc_user = ''
        self.instance_name = ''
        self.date_today = ''
        self.archive_mode = 0
        self.historical_mode = 0
    
    @staticmethod
    def get_current(process_run_name):
        """Returns a new instance of the SessionInfo
        with the relevant attributes populated based
        on the current FA session.        
        """
        result = SessionInfo(process_run_name)
        
        try:
            import acm
            result.ads_address = str(acm.ADSAddress())
            result.acm_class = str(acm.Class())
            result.user = str(acm.User().Name())
            result.instance_name = acm.FDhDatabase['ADM'].InstanceName()
            result.date_today = acm.Time.DateToday()
            # result.workspace = str(acm.ActiveWorkspace()) # works only in GUI
            result.archive_mode = acm.ArchivedMode()
            result.historical_mode = acm.IsHistoricalMode()
        except Exception:
            # this can fail on import error
            LOGGER.exception("Something went wrong.")
        
        try:
            result.hostname = socket.gethostname()
            result.pc_user = getpass.getuser()
        except Exception:
            LOGGER.exception("Something went wrong.")
        
        return result
    
    @staticmethod
    def from_json(body):
        if not body:
            return None
        result = SessionInfo(body['process_run_name'])  
        result.ads_address = body['ads_address']
        result.acm_class = body['acm_class']
        result.user = body['user']
        result.data = body['data']
        result.hostname = body['hostname']
        result.pc_user = body['pc_user']
        result.instance_name = body['instance_name']
        result.date_today = body['date_today']
        # result.workspace = body['workspace']
        result.archive_mode = body['archive_mode']
        result.historical_mode = body['historical_mode']
        
        return result
    
    def __str__(self):
        return "Session Info: {0}".format(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))

class LogException(object):
    
    def __init__(self):
        self.exc_type = None
        self.exc_value = None
        self.exc_traceback = None
    
    @staticmethod
    def from_logging(log_record):
        if log_record.exc_info == None:
            return None
        result = LogException()
        # Have to cater for special html symbols 
        result.exc_type = str(log_record.exc_info[0]).replace("<", "").replace(">", "")
        result.exc_value = str(log_record.exc_info[1])
        result.exc_traceback = formatter.formatException(log_record.exc_info)
        
        return  result
    
    @staticmethod
    def from_json(body):
        result = LogException()
        if body:
            result.exc_type = body['exc_type'] 
            result.exc_value = body['exc_value']
            result.exc_traceback = body['exc_traceback']
        
        return  result
    
    def __str__(self):
        return "Log Exception: {0}".format(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))

class TaskArgs(object):
    
    def __init__(self, ael_main_args):
        self.ael_main_args = {}
        try:
            if ael_main_args:
                for key, value in ael_main_args.items():
                    name = ""
                    oid = ""
                    if hasattr(value, "Oid"):
                        oid = str(value.Oid())
                    if hasattr(value, "Name"):
                        name = str(value.Name())
                    if name or oid:
                        self.ael_main_args[key] = "{0} ({1})".format(name, oid)
                    else:
                        self.ael_main_args[key] = str(value)
        except Exception:
            # this can fail on import error
            LOGGER.exception("Something went wrong.")
    
    @staticmethod
    def from_json(body):
        if not body:
            return None
        result = TaskArgs(body['ael_main_args'])  
        
        return result
    
    def to_str(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    def __str__(self):
        return "Task Args : {0}".format(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))
    
class LogMessage(object):
    
    def __init__(self, process_name, process_run_name, log_record=None, session_info=None, log_exception=None, task_args=None):
        self.log_record = log_record
        self.session_info = session_info
        self.task_args = task_args
        self.process_name = process_name
        self.process_run_name = process_run_name
        self.log_exception = log_exception
    
    @staticmethod
    def generate_run_name(process_name):
        unique_id = uuid4().get_hex()[0:10]
        return "{0}.{1}".format(process_name, unique_id)
    
    def to_json(self):
        msg = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        return msg
    
    @staticmethod
    def from_json(body):
        msg = json.loads(body)
        process_name = msg['process_name']
        process_run_name = msg['process_run_name']
        log_record = LogRecord.from_json(msg['log_record'])
        session_info = SessionInfo.from_json(msg['session_info'])
        log_exception = LogException.from_json(msg['log_exception'])
        if 'task_args' in msg:
            task_args = TaskArgs.from_json(msg['task_args'])
        else:
            task_args = None
        
        return LogMessage(process_name, process_run_name, log_record, session_info, log_exception, task_args)
        
    def __str__(self):
        result = "{0},\n {1}, \n {2},\n Process Name: {3},\n Process Run name: {4}".format(self.log_record,
                                                                                   self.session_info,
                                                                                   self.task_args,
                                                                                   self.process_name,
                                                                                   self.process_run_name)
        return result
