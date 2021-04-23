'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_AD_HOC_MESSAGE_REPLAY
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will allow the replay of any type of Request message.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
import FC_ERROR_HANDLER_DEFAULT as ERROR_HANDLER_DEFAULT
import ael, traceback, amb, os

'''----------------------------------------------------------------------------------------------------------
Importing custom modules.
----------------------------------------------------------------------------------------------------------'''
try:
    from FC_UTILS import FC_UTILS as UTILS
except ImportError as e:
    ERROR_HANDLER_DEFAULT.handelError('Import Error in module %s.' %__name__, e, traceback)
    raise ImportError('Import Error in module %s. ERROR: %s.' %(__name__, str(e)))

try:
    UTILS.Initialize(__name__)
except Exception as e:
    ERROR_HANDLER_DEFAULT.handelError('Initialization Error in module %s. FC_UTILS could not be initialized. '
                                    'No Parameters, Logging or Error Handling could be loaded. '
                                    'The ATS will not start until the root issue is resolved.' %__name__, e, traceback)
    raise Exception('Initialization Error in module %s. FC_UTILS could not be initialized. '
                    'No Parameters, Logging or Error Handling could be loaded. '
                    'The ATS will not start until the root issue is resolved. ERROR: %s. ' %(__name__, str(e)))

try:
    from FC_EXCEPTION import FC_EXCEPTION as EXCEPTION
except ImportError as e:
    ERROR_HANDLER_DEFAULT.handelError('Import Error in module %s. FC_EXCEPTION could not be imported. '
                                    'No Error Handling could be loaded. '
                                    'The ATS will not start until the root issue is resolved.' %__name__, e, traceback)
    raise Exception('Import Error in module %s. FC_EXCEPTION could not be imported. '
                    'No Error Handling could be loaded. '
                    'The ATS will not start until the root issue is resolved. ERROR: %s. ' %(__name__, str(e)))

try:
    from FC_HANDLER_CONTAINER import FC_HANDLER_CONTAINER as HANDLER_CONTAINER
except ImportError as e:
    UTILS.ErrorHandler.processError(None, EXCEPTION('Could not import the worker module in module %s' %__name__, traceback, 'CRITICAL', None), __name__)
    raise Exception('Could not import the worker module in module %s. ERROR: %s' %(__name__, str(e)))

try:
    from AMBA_Helper_Functions import AMBA_Helper_Functions as AMBA_Helpers
except ImportError as e:
    UTILS.ErrorHandler.processError(None, EXCEPTION('Could not import the AMB Helper Functions in module %s' %__name__, traceback, 'CRITICAL', None), __name__)
    raise Exception('Could not import the AMB Helper Functions in module %s. ERROR: %s' %(__name__, str(e)))

try:
    from FC_PARAMETERS_ENVIRONMENT import FC_PARAMETERS_ENVIRONMENT as PARAMETERS_ENVIRONMENT
except ImportError as e:
    UTILS.ErrorHandler.processError(None, EXCEPTION('Could not import the Environment Parameters in module %s' %__name__, traceback, 'CRITICAL', None), __name__)
    raise Exception('Could not import the Environment Parameters in module %s. ERROR: %s' %(__name__, str(e)))

try:
    from FC_PARAMETERS_COMPONENT import FC_PARAMETERS_COMPONENT as PARAMETERS_COMPONENT
except ImportError as e:
    UTILS.ErrorHandler.processError(None, EXCEPTION('Could not import the Component Parameters in module %s' %__name__, traceback, 'CRITICAL', None), __name__)
    raise Exception('Could not import the Component Parameters in module %s. ERROR: %s' %(__name__, str(e)))
    
'''----------------------------------------------------------------------------------------------------------
Global variables
----------------------------------------------------------------------------------------------------------'''
global writerHandlerCollection
writerHandlerCollection = None
atsList = []
invalidATSList = ['#text', 'GENERIC_PARAMETERS', 'FC_HEART_BEAT_SYSTEM_01_ATS', 'FC_AD_HOC_REQUEST_GENERATOR', 'FC_AD_HOC_MESSAGE_REPLAY', 'FC_RT_01_ATS']

subjectRequestTypeValidation = {'FC_REQ_COORD_01_ATS' : 'REQUEST',
                                'FC_RES_COORD_01_ATS' : 'RESPONSE',
                                'FC_REQT_ST_01_ATS' : 'REQUEST_SINGLE_TRADE',
                                'FC_REQT_PT_01_ATS' : 'REQUEST_PORTFOLIO_TRADES',
                                'FC_REQT_IT_01_ATS' : 'REQUEST_INSTRUMENT_TRADES',
                                'FC_TCOLL_01_ATS_01' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_02' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_03' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_04' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_05' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_06' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_07' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_08' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_09' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_10' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_11' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_12' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_13' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_14' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_15' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_16' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_17' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_18' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_19' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_20' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_21' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_22' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_23' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_24' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_25' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_26' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_27' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_28' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_29' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_30' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_31' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_32' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_33' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_34' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_35' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_36' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_37' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_38' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_39' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_40' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_41' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_42' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_43' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_44' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_45' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_46' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_47' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_48' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_49' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_50' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_51' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_52' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_53' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_54' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_55' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_56' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_57' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_58' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_59' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_60' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_61' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_62' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_63' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_64' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_65' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_69' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_71' : 'REQUEST_TRADE_COLLECTION',
                                'FC_TCOLL_01_ATS_128' : 'REQUEST_TRADE_COLLECTION',
                                'FC_SCOLL_01_ATS_01' : 'REQUEST_SETTLEMENT_COLLECTION'
                                }

def createAmbWriterHandler():
    global writerHandlerCollection
    writerHandlerCollection = HANDLER_CONTAINER()
    writerHandlerCollection.initialise()
    
def postAMBAMessageToAMB(AMBAMessage, requestType, senderSubject):
    global writerHandlerCollection
    writerHandlerCollection.ambWriterHandlers['REQUEST'].ambWriter.post_Message_To_AMB_With_Subject(AMBAMessage, senderSubject)

def postOutgoingAMBAMessagesToAMB(outgoingAMBAMessages):
    for outgoingAMBAMessage in outgoingAMBAMessages:
            postAMBAMessageToAMB(outgoingAMBAMessage[1], outgoingAMBAMessage[0], outgoingAMBAMessage[2])

def constructATSList():
    for childNode in PARAMETERS_ENVIRONMENT.environment.childNodes:
        if str(childNode.nodeName) not in invalidATSList:
            atsList.append(str(childNode.nodeName))
constructATSList()

ael_variables = [
                    ['inputPath', 'Input File Path', 'string', None, 'C:/', 1, 0, 'Path where the input file will be located to enter the messages to be replayed.', None, 1],
                    ['inputFileName', 'Input File Name', 'string', None, 'FC_AD_HOC_MESSAGE_REPLAY.txt', 1, 0, 'Name of the file where the messages will be entered. Messages to be seperated by "\xbf", a character with decimal value of 191, (BF in hexadecimal), can be typed by Alt+168.', None, 1],
                    ['targetATS', 'Target ATS', 'string', atsList, '', 1, 0, 'Which ATS should be receiving the message?', None, 1]
                ]

def ael_main(dict):
    global writerHandlerCollection
    
    try:
        createAmbWriterHandler()
    except Exception as e:
        UTILS.ErrorHandler.processError(None, EXCEPTION('Could not create the AMB writers in module %s.' %__name__,\
            traceback, 'CRITICAL', e))
        return
    
    inputPath = dict['inputPath']
    inoutFileName = dict['inputFileName']
    targetATS = dict['targetATS']
    
    filePathAndName = os.path.join(inputPath, inoutFileName)
    
    try:
        file = os.system("notepad.exe %s" %filePathAndName)
    except Exception as e:
        UTILS.ErrorHandler.processError(None, EXCEPTION('Could not create the input file %s in module %s.' %(filePathAndName, __name__),\
            traceback, 'CRITICAL', e))
        return

    try:
        file = open(filePathAndName, 'r')
    except Exception as e:
        UTILS.ErrorHandler.processError(None, EXCEPTION('Could not open the input file %s in module %s.' %(filePathAndName, __name__),\
            traceback, 'CRITICAL', e))
        return
    
    try:
        fileString = file.read()
    except Exception as e:
        UTILS.ErrorHandler.processError(None, EXCEPTION('Could not read the context of the input file %s in module %s.' %(filePathAndName, __name__),\
            traceback, 'CRITICAL', e))
        return

    msgsString = fileString.split('\xbf')

    outgoingAMBAMessages = []
    
    for msgString in msgsString:
        try:
            strippedMsgString = msgString.lstrip().rstrip()
        except Exception as e:
            UTILS.ErrorHandler.processError(None, EXCEPTION('Could not remove the white spaces pre and post the message %s in module %s.' %(msgString, __name__),\
            traceback, 'CRITICAL', e))
            continue
        
        try:
            buffer = amb.mbf_create_buffer_from_data(strippedMsgString)
        except Exception as e:
            UTILS.ErrorHandler.processError(None, EXCEPTION('Could not create a mbf buffer for message %s in module %s.' %(msgString, __name__),\
            traceback, 'CRITICAL', e))
            continue
        
        try:
            msg = buffer.mbf_read()
        except Exception as e:
            UTILS.ErrorHandler.processError(None, EXCEPTION('Could not read the AMB object for message %s in module %s.' %(msgString, __name__),\
            traceback, 'CRITICAL', e))
            continue
        
        try:
            messageType = AMBA_Helpers.get_AMBA_Object_Value(msg, 'TYPE')
        except Exception as e:
            UTILS.ErrorHandler.processError(None, EXCEPTION('Could not retreive the TYPE attribute from the message %s in module %s.' %(msgString, __name__),\
            traceback, 'CRITICAL', e))
            continue
        
        try:
            subjects = PARAMETERS_COMPONENT(targetATS).componentSubscriptionSubjects
        except Exception as e:
            UTILS.ErrorHandler.processError(None, EXCEPTION('Could not retreive the subjects from the component config %s in module %s.' %(targetATS, __name__),\
            traceback, 'CRITICAL', e))
            continue
        
        if len(subjects) == 1:
            subject = subjects[0]
        
        if subjectRequestTypeValidation[targetATS] != messageType:
            UTILS.ErrorHandler.processError(None, EXCEPTION('The AMBA Message TYPE, %s, entered does not match the subscription of the target ATS %s.' %(messageType, targetATS),\
            traceback, 'CRITICAL', None))
            continue
        
        outgoingAMBAMessages.append((messageType, msg, subject))
    
    postOutgoingAMBAMessagesToAMB(outgoingAMBAMessages)
        
    try:
        for requestType in writerHandlerCollection.ambWriterHandlers.keys():
            writerHandlerCollection.ambWriterHandlers[requestType].ambWriter.close_AMB_Connection()
            UTILS.Logger.flogger.info('AMB Sender Connection to the AMB is now closed for writer posting Message Type %s.' %requestType)
    except Exception as e:
        UTILS.ErrorHandler.processError(None, EXCEPTION('Could not close all of the AMB connections in module %s.' %__name__,\
            traceback, 'CRITICAL', e))
    
    try:
        file.close()
    except Exception as e:
        UTILS.ErrorHandler.processError(None, EXCEPTION('Could not close the input file %s in module %s.' %(filePathAndName, __name__),\
            traceback, 'CRITICAL', e))
        return
