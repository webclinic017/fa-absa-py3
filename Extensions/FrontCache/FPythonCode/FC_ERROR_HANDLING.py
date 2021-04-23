
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_ERROR_HANDLING
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will handel exceptions from Front Cache. When ever an Exception
                                is thrown, this module can be called and the exception can be passed. This
                                module will log the exception and post the exception with all inner exceptions
                                onto the AMB. An error monitor ca pick up these exceptions and notice the
                                relevant parties.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
import traceback
import os
import psutil

'''----------------------------------------------------------------------------------------------------------
Importing all relevant custom modules.
----------------------------------------------------------------------------------------------------------'''
from FC_EXCEPTION import FC_EXCEPTION as EXCEPTION
from AMBA_GENERATE_MESSAGE import AMBA_GENERATE_MESSAGE as AMBA_MESSAGE_GENERATOR
from FC_FLOGGER_SINGLETON import FC_FLOGGER_SINGLETON as FLOGGER

'''----------------------------------------------------------------------------------------------------------
Class containing static methods to handel the exceptions given to the method called processError.
----------------------------------------------------------------------------------------------------------'''
class FC_ERROR_HANDLING:
    global AMBADataDictionaryList
    
    @staticmethod
    def costructAMBADataDictionary(exception):
        if type(exception) == EXCEPTION:
            ambaDataDictionary = {'TEXT_MESSAGE' : exception.TextMsg,
                                'TRACEBACK' : exception.Traceback,
                                'SEVERITY' : exception.Severity}
        else:
            ambaDataDictionary = {'TEXT_MESSAGE' : exception.message,
                                'TRACEBACK' : traceback.format_exc(),
                                'SEVERITY' : ''}
        return ambaDataDictionary
    
    @staticmethod
    def costructAMBADataDictionaryList(exception):
        global AMBADataDictionaryList
        AMBADataDictionaryList.append(FC_ERROR_HANDLING.costructAMBADataDictionary(exception))
        if type(exception) == EXCEPTION:
            if exception.InnerException:
                FC_ERROR_HANDLING.costructAMBADataDictionaryList(exception.InnerException)
    
    @staticmethod
    def constructDataSetForAMBAMessage():
        global AMBADataDictionaryList
        DataSetForAMBAMessage = []
        if not AMBADataDictionaryList:
            return DataSetForAMBAMessage
        else:
            for AMBADataDictionary in AMBADataDictionaryList:
                DataSetForAMBAMessage.append((['EXCEPTIONS'], 'EXCEPTION', AMBADataDictionary))        
        return DataSetForAMBAMessage
    
    @staticmethod
    def generateAMBAMessage(messageType, senderSource, inputDataSet, receiver):
        ABMAMessage = AMBA_MESSAGE_GENERATOR(None, messageType, '1.0', None, senderSource, inputDataSet)
        ABMAMessage.generate_AMBA_Message()
        if receiver:
            ABMAMessage.add_element_to_amb_msg('RECEIVER', receiver)
        return ABMAMessage.AMBA_Message
    
    @staticmethod
    def shutdown():
        processId = os.getpid()
        process = psutil.Process(processId)
        FLOGGER.Instance().flogger.error('Process ID of ATS: %i' %processId)
        parentProcessId = process.ppid()
        FLOGGER.Instance().flogger.error('Process ID of ATS Guard: %i' %parentProcessId)
        parentProcess = psutil.Process(parentProcessId)
        if parentProcess.name() == 'explorer.exe':
            return                  
        while parentProcess:
            try:
                parentProcess.kill()
                try:
                    parentProcess = psutil.Process(parentProcessId)
                except Exception, e:
                    FLOGGER.Instance().flogger.error('Process is not stopped')
            except:
                pass

    @staticmethod
    def forceShutDownWithMessage(msg):
        FLOGGER.Instance().flogger.error(msg)
        FC_ERROR_HANDLING.shutdown()

    @staticmethod
    def forceShutDown():
        FLOGGER.Instance().flogger.error('FORCING THE ATS TO SHUT DOWN DUE TO AN ERROR...')
        FC_ERROR_HANDLING.shutdown()
    
    @staticmethod
    def forceRestart():
        FLOGGER.Instance().flogger.error('RESTARTING THE ATS TO SHUT DOWN DUE TO AN ERROR...')
        processId = os.getpid()
        process = psutil.Process(processId)
        FLOGGER.Instance().flogger.error('Process ID of ATS: %i' %processId)
        parentProcessId = process.ppid()
        FLOGGER.Instance().flogger.error('Process ID of Parent Process: %i' %parentProcessId)
        parentProcess = psutil.Process(parentProcessId)
        if parentProcess.name() == 'explorer.exe':
            return                  
        process.kill()
    
    @staticmethod
    def processError(ambWriterHandler, exception, senderSource = __name__, messageType = 'FC_ERROR_MESSAGE', RECEIVER = ''):
        global AMBADataDictionaryList
        AMBADataDictionaryList = []
        FC_ERROR_HANDLING.costructAMBADataDictionaryList(exception)
        DataSetForAMBAMessage = FC_ERROR_HANDLING.constructDataSetForAMBAMessage()
        AMBAMessage = FC_ERROR_HANDLING.generateAMBAMessage(messageType, senderSource, DataSetForAMBAMessage, RECEIVER)        
        if ambWriterHandler:            
            ambWriterHandler.ambWriter.post_Message_To_AMB(AMBAMessage)
        FLOGGER.Instance().flogger.error(AMBAMessage.mbf_object_to_string())
        if exception.Severity == 'CRITICAL':
            #FC_ERROR_HANDLING.forceShutDown()
            FC_ERROR_HANDLING.forceRestart()
        else:
            FC_ERROR_HANDLING.forceRestart()
