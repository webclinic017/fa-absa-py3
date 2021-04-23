
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_RES_COORD_01_ATS
PROJECT                 :       This module is the entry point for the Front Cache Response Coordinator ATS.
                                This ATS will subscribe to a RESOPNSE type messages from the AMB, log them
                                to a database, give an event response to the AMB for subscribers to pick up.
PURPOSE                 :       This module handles all the Response messages for Front Arena Cache.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python and custom modules needed for the ATS to start up. Initializing the FC_UTILS
module to load all Parameters, Logging, Error Handler.
----------------------------------------------------------------------------------------------------------'''
import FC_ERROR_HANDLER_DEFAULT as ERROR_HANDLER_DEFAULT
import traceback

try:
    from FC_UTILS import FC_UTILS as UTILS
except ImportError, e:
    ERROR_HANDLER_DEFAULT.handelError('Import Error in module %s.' %__name__, e, traceback)
    raise ImportError('Import Error in module %s. ERROR: %s.' %(__name__, str(e)))

try:
    UTILS.Initialize(__name__)
except Exception, e:
    ERROR_HANDLER_DEFAULT.handelError('Initialization Error in module %s. FC_UTILS could not be initialized. '
                                    'No Parameters, Logging or Error Handling could be loaded. '
                                    'The ATS will not start until the root issue is resolved.' %__name__, e, traceback)
    raise Exception('Initialization Error in module %s. FC_UTILS could not be initialized. '
                    'No Parameters, Logging or Error Handling could be loaded. '
                    'The ATS will not start until the root issue is resolved. ERROR: %s. ' %(__name__, str(e)))
                    
try:
    from FC_EXCEPTION import FC_EXCEPTION as EXCEPTION
except ImportError, e:
    ERROR_HANDLER_DEFAULT.handelError('Import Error in module %s. FC_EXCEPTION could not be imported. '
                                    'No Error Handling could be loaded. '
                                    'The ATS will not start until the root issue is resolved.' %__name__, e, traceback)
    raise Exception('Import Error in module %s. FC_EXCEPTION could not be imported. '
                    'No Error Handling could be loaded. '
                    'The ATS will not start until the root issue is resolved. ERROR: %s. ' %(__name__, str(e)))

try:
    from datetime import datetime
except ImportError, e:
    UTILS.ErrorHandler.processError(None, EXCEPTION('Import Error in module %s. Module datetime could not be imported. '
                                                    'The ATS will not start until the root issue is resolved.' %__name__, traceback, 'CRITICAL', e), __name__)
    raise Exception('Import Error in module %s. Module datetime could not be imported. '
                    'The ATS will not start until the root issue is resolved. ERROR: %s' %(__name__, str(e)))

try:
    from FC_RES_COORD_ATS_WORKER import FC_RES_COORD_ATS_WORKER as RES_COORD_ATS_WORKER
except ImportError, e:
    UTILS.ErrorHandler.processError(None, EXCEPTION('Could not import the worker module in module %s' %__name__, traceback, 'CRITICAL', None), __name__)
    raise Exception('Could not import the worker module in module %s. ERROR: %s' %(__name__, str(e)))

'''----------------------------------------------------------------------------------------------------------
Global variables
-------------------------------------------------------------------------------------------------------------
'''
global worker
worker = None

'''----------------------------------------------------------------------------------------------------------
work function which the ATS will call once started.
-------------------------------------------------------------------------------------------------------------
'''
def work():
    global worker
    if not worker:
        UTILS.ErrorHandler.processError(None, EXCEPTION(UTILS.Constants.fcExceptionConstants.WORKER_VARIABLE_S_IS_NOT_INSTANTIATED %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, None), __name__)
    else:
        worker.work()

'''----------------------------------------------------------------------------------------------------------
start function which the ATS will call when the ATS is starting.
-------------------------------------------------------------------------------------------------------------
'''
def start():
    UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.STARTING_ATS_S_AT_S %(__name__, datetime.now()))
    global worker
    if not worker:
        worker = RES_COORD_ATS_WORKER()
    worker.start()

'''----------------------------------------------------------------------------------------------------------
stop function which the ATS will call when the ATS is stopping.
-------------------------------------------------------------------------------------------------------------
'''
def stop():
    global worker
    if not worker:
        UTILS.ErrorHandler.processError(None, EXCEPTION(UTILS.Constants.fcExceptionConstants.WORKER_VARIABLE_IN_S_IS_NOT_INSTANTIATED_STOP %__name__, traceback, UTILS.Constants.fcGenericConstants.MEDIUM, None), __name__)
    else:
        worker.stop()

#start()
#work()
#stop()
