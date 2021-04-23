'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_ATS_WORKER_BASE
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module is the base class of the ATS Workers. Logival workfow for the ATS
                                Start, Work and Stop functions is defined which can be overridden in the
                                classes which inherites from this class.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules. TEST
----------------------------------------------------------------------------------------------------------'''
import amb, acm, collections, datetime, os, platform, time, traceback

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
from FC_UTILS import FC_UTILS as UTILS
from FC_EXCEPTION import FC_EXCEPTION as EXCEPTION
from AMBA_GENERATE_MESSAGE import AMBA_GENERATE_MESSAGE as AMBA_MESSAGE_GENERATOR
from FC_HANDLER_CONTAINER import FC_HANDLER_CONTAINER as HANDLER_CONTAINER
from FC_HEART_BEAT_TIMER_PROCESS import FC_HEART_BEAT_TIMER_PROCESS as HEART_BEAT_TIMER_PROCESS
import FC_DATA_HELPER as DATA_HELPER
import AMB_Reader_Writer as ambReaderWriter
import FC_UTILS as FC_UTILS
'''----------------------------------------------------------------------------------------------------------
Global variables
----------------------------------------------------------------------------------------------------------'''
global messageQueue
messageQueue = collections.deque()
UTILS.MessageQueueDepth = len(messageQueue)
isConnected = False
'''----------------------------------------------------------------------------------------------------------
Event callback function for reading AMB messages. The events are placed in a queue that is then processed by 
invoking the Work function. 
----------------------------------------------------------------------------------------------------------'''
def event_cb_reader(channel, event, arg):
    global messageQueue
    global isConnected
    eventString = amb.mb_event_type_to_string(event.event_type)
    if eventString == UTILS.Constants.fcGenericConstants.DISCONNECT:
        #raise RuntimeError(UTILS.Constants.fcExceptionConstants.AMB_READER_RECEIVED_DISCONNECT_EVENT)
        UTILS.Logger.flogger.info(UTILS.Constants.fcExceptionConstants.AMB_READER_RECEIVED_DISCONNECT_EVENT)
        isConnected = False
        UTILS.Logger.flogger.info(UTILS.Constants.fcExceptionConstants.AMB_READER_RECEIVED_DISCONNECT_EVENT)
    elif eventString == UTILS.Constants.fcGenericConstants.MESSAGE:
        #uncomment for super fast clearing of messages
        #(incomingAMBAMessageObject, currentAMBChannel) = (amb.mb_copy_message(event.message), channel)
        #acceptResult = amb.mb_queue_accept(currentAMBChannel, incomingAMBAMessageObject, str(incomingAMBAMessageObject.id))
        #UTILS.MessageQueueDepth += 1
        #UTILS.Logger.flogger.info('%s messages cleared off the queue' %UTILS.MessageQueueDepth)
        #return
        messageQueue.append((amb.mb_copy_message(event.message), channel))
        UTILS.MessageQueueDepth = len(messageQueue)       

'''----------------------------------------------------------------------------------------------------------
Create the AMB writer to post Real Time Request Events onto the AMB so that the Request Coordinater can 
process the messages.
----------------------------------------------------------------------------------------------------------'''
'''def event_cb_writer(channel, event, arg):
    eventString = amb.mb_event_type_to_string(event.event_type)
    if eventString == 'Disconnect':
        raise RuntimeError('The AMB reader received a disconnect event.\nThe ATS will not be able to continue reading from the AMB.')
'''     
'''----------------------------------------------------------------------------------------------------------
Base class for the ATS. This class contains methods for the Start, Work and Stop of the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_ATS_WORKER_BASE():
    def __init__(self):
        self._platformName = platform.system()
        self._processId = os.getpid()
        self._ambReader = None
        self._heartBeatProcess = None
        self.heartBeatSystem = None
        self._shutdownProcess = None
        self.heartBeatCandidateComponent = None
        self.ATS_STATUS = None
        self._writerHandlerCollection = None
        self.incomingAMBAMessageObject = None
        self.incomingAMBAMessageData = None
        self.incomingMessageObject = None
        self.currentAMBChannel = None
        self.outgoingMessageObjects = []
        self.outgoingAMBADataDictionaries = [] #List of tuples (identify AMB Handler to write, data dictionary)
        self.outgoingAMBAMessages = [] #List of tuples (identify AMB Handler to write, amba message)
        self.reportDate = ''
        self.requestId = None
        self.currentMessageId = None
        self.last_processed_messageId = None
        self._recovery_mode = False

    '''----------------------------------------------------------------------------------------------------------
    Function to start the ATS
    ----------------------------------------------------------------------------------------------------------'''
    def start(self):
        global messageQueue
        global isConnected
        #Used as a parameter for ats shutdown
        FC_UTILS.Ats_startup_datetime = datetime.datetime.now()

        try:
            print FC_UTILS.getAtsServiceName(UTILS.ComponentName)
            FC_UTILS.Ats_service_name, FC_UTILS.HistoricalDate, FC_UTILS.DateToday = FC_UTILS.getAtsServiceName(UTILS.ComponentName)
        except Exception, e:
            UTILS.ErrorHandler.processError(None, EXCEPTION('Could not get historical date and name %s' %__name__,\
                    traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

        try:
            self.__logATSHeaderInformation()
        except Exception, e:
            UTILS.ErrorHandler.processError(None, EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_LOG_ATS_HEADER_INFO_S %__name__,\
                    traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

        try:
            self.__loadWriterHandlerCollection()
        except Exception, e :
            UTILS.ErrorHandler.processError(None, EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_LOAD_WRITER_HANDLERS_S %__name__,\
                    traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

        try:
            self.__initialiseWriterHandlers()
            isConnected = True
        except Exception, e:
            UTILS.ErrorHandler.processError(None, EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_INITIALIZE_WRITER_HANDLERS %__name__,\
                    traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.AMB_WRITER_CONNECTION_EST)

        try:
            self.__createAMBReader()
            isConnected = True
        except Exception, e:
            UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_CREATE_AMB_READER_S %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.AMB_READER_CONNECTION_EST)

        try:
            self._heartBeatProcess = HEART_BEAT_TIMER_PROCESS()
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.HEART_BEAT_PROCESS_TIMER_STARTED_S %datetime.datetime.now())
        except Exception, e:
            UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_CREATE_HEART_BEAT_S %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

        try:
            self.__logATSHeaderStartupComplete()
        except Exception, e:
            UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_COMPLETE_ATS_START_HEADER_INFO_S %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

        try:
            self.getLastProcessedMessageId()
        except Exception, e:
            UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.MESSAGE_STATE_INFO_FAILED, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

        self.ATS_STATUS = UTILS.Constants.fcGenericConstants.RUNNING
        amb.mb_poll()
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.MSG_QUEUE_START_UP_DEPTH_I %len(messageQueue))

    '''----------------------------------------------------------------------------------------------------------
    Method that gets executed when the ATS is stopped.
    ----------------------------------------------------------------------------------------------------------'''
    def stop(self):
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.STOPPING_ATS_S %datetime.datetime.now())
        #self.ATS_STATUS = UTILS.Constants.fcGenericConstants.STOP --> this constant needs to be added into GENERICS CONSTANTS
        
        try:
            self.__closeAMBConnections()
        except Exception, e:
            UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_CLOSE_AMB_CONNECTIONS_NORMALLY_S %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))
                
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.STOPPING_HEART_BEAT_PROCESS_S %datetime.datetime.now())
        
        try:
            self._heartBeatProcess.stopTimer()
        except Exception, e:
            UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_STOP_PROCESS_HEART_BEAT_S %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

        if self.heartBeatSystem:
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.STOPPING_SYSTEM_HEAR_BEAT_S %datetime.datetime.now())
            try:
                self.heartBeatSystem.stopTimer()
            except Exception, e:
                UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_STOP_SYSTEM_HEART_BEAT_S %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

    '''----------------------------------------------------------------------------------------------------------
    Method that does all the work. This method is being called by the ATS.
    ----------------------------------------------------------------------------------------------------------'''
    def work(self):

        global messageQueue
        global isConnected

        if isConnected is False:
            self.ambReconnectRoutine()
            isConnected = True
            amb.mb_poll()
        '''----------------------------------------------------------------------------------------------------------
        The ATS needs to be in a RUNNING state to be able to continue. If not in RUNNING state, there is a high
        possibility that the memory consumption is too high resulting in the ATS to restart itself.
        ----------------------------------------------------------------------------------------------------------'''
        if self.ATS_STATUS != UTILS.Constants.fcGenericConstants.RUNNING:
            self.__checkShutdown()
            return

        '''----------------------------------------------------------------------------------------------------------
        If there are no messages on the interal queue there is nothing to process and the the work fuction will return.
        ----------------------------------------------------------------------------------------------------------'''
        if len(messageQueue) == 0:
            UTILS.MessageQueueDepth = len(messageQueue)
            date_now = str(time.strftime("%Y-%m-%d"))
            if FC_UTILS.RestartAtsForDateToday(date_now, FC_UTILS.Ats_service_name, FC_UTILS.DateToday):
                UTILS.Logger.flogger.info("Ats is not the correct date_today. Ats will update registry and restart")
                self.__restartATS()
            if FC_UTILS.RestartAtsForHistoricalDate(date_now, FC_UTILS.Ats_service_name, FC_UTILS.HistoricalDate):
                UTILS.Logger.flogger.info("Ats is not the correct historical date. Ats will update registry and restart")
                self.__restartATS()
            self.__checkShutdown()
            return

        '''----------------------------------------------------------------------------------------------------------
        Pop the first message off the queue (left)
        ----------------------------------------------------------------------------------------------------------'''        
        while len(messageQueue) > 0:
            try:
                self.__readFirstMessageFromQueue()
            except Exception, e:
                UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_READ_FIRST_MSG_FROM_AMB_S %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

            '''----------------------------------------------------------------------------------------------------------
            Read the message content
            ----------------------------------------------------------------------------------------------------------'''
            try:
                self.__readIncommingAMBAMessageData()
            except Exception, e:
                UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_READ_AMBA_MSG_DATA %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

            '''----------------------------------------------------------------------------------------------------------
            Uncomment to clear the queue without processing any messages
            ----------------------------------------------------------------------------------------------------------'''
            #self.__acceptAMBAMessageFromAMB()
            #return False
            
            '''----------------------------------------------------------------------------------------------------------
            Map the incoming AMBA message to a Message Object. This Message Object is a common object which the ATS 
            understands. It is abstracted from what type of Request or Response message the incoming message is. 
            ----------------------------------------------------------------------------------------------------------'''
            try:
                self.mapIncomingAMBAMessageToIncomingMessageObject()
            except Exception, e:
                UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_MAP_INCOMING_AMBA_MSG_TO_AN_INCOMING_MSG_OBJ_S %__name__,\
                    traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))
            
            '''----------------------------------------------------------------------------------------------------------
            Specific work that the ATS needs to do in processing the message
            ----------------------------------------------------------------------------------------------------------'''
            try:
                self.processIncommingAMBAMessage()
            except Exception, e:
                UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_PROCESS_INCOMING_AMBA_MSG_OR_MSG_OBJ %__name__,\
                    traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e), __name__, 'FC_ERROR_MESSAGE', UTILS.Parameters.fcComponentParameters.componentReceiverName)


            if self._recovery_mode is True:
                UTILS.Logger.flogger.info('ATS exiting recovery_mode')
                self._recovery_mode = False


            '''----------------------------------------------------------------------------------------------------------
            Generate OutgoingMessageObjects. This can be requests objects that eeds to be passed on or responnse objects.
            ----------------------------------------------------------------------------------------------------------'''
            try:
                self.createOutgoingMessageObjects()
            except Exception, e:
                UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_CREATE_OUTGOING_MSG_OBJ_S %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))        
            
            '''----------------------------------------------------------------------------------------------------------
            Generate an AMBA message.
            ----------------------------------------------------------------------------------------------------------'''
            try:
                self.__generateOutgoingAMBAMessages()
            except Exception, e:
                UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_GENERATE_OUTGOING_AMBA_MSG_S %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))
            
            '''----------------------------------------------------------------------------------------------------------
            Post Real Time Request AMBA Message to AMB -- This can be done in outer loop
            ----------------------------------------------------------------------------------------------------------'''
            try:
                self.postOutgoingAMBAMessagesToAMB()
            except Exception, e:
                UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_POST_OUTGOING_AMBA_MSG_TO_AMB_S %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))
            
            '''----------------------------------------------------------------------------------------------------------
            First try accept the message off the AMB (to elminate duplicates when the ATS restarts
            ----------------------------------------------------------------------------------------------------------'''
            try:
                self.__acceptAMBAMessageFromAMB()
            except Exception, e:
                UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_ACCEPT_PROCESSED_MSG_FROM_AMB_QUEUE_S %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

            
            '''----------------------------------------------------------------------------------------------------------
            Clean up process. Dispose objects that is not needed anymore after accepting the message
            ----------------------------------------------------------------------------------------------------------'''
            self.__dataCleanUp()

            self.__checkShutdown()

            '''----------------------------------------------------------------------------------------------------------
            Checking memory threashold. If Memory usage if more than threashold, the ATS will restart.
            ----------------------------------------------------------------------------------------------------------'''
            try:
                self.__checkMemoryThreshold()
            except Exception, e:
                UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_CHECK_MEMORY_THRESHHOLD_S %__name__, traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

            if UTILS.Parameters.fcGenericParameters.RestartAfterWork is True:
                try:
                    UTILS.Logger.flogger.info('Restarting ats due to RestartAfterWork config setting')
                    self.RestartAts()
                except Exception, e:
                    UTILS.Logger.flogger.info('RestartAfterWorkFailed : %s' % str(e))


    '''----------------------------------------------------------------------------------------------------------
    Post AMBA Message to AMB
    ----------------------------------------------------------------------------------------------------------'''
    def postAMBAMessageToAMB(self, AMBAmessage, requestType, subject):
        global isConnected
        if isConnected is False:
            self.ambReconnectRoutine()
            isConnected = True
            amb.mb_poll()

        if not self._writerHandlerCollection.ambWriterHandlers[requestType].ambWriter.post_Message_To_AMB_With_Subject(AMBAmessage, subject):
            raise RuntimeError(UTILS.Constants.fcExceptionConstants.COULD_NOT_POST_MSG_WITH_TYPE_S_AND_SUBJECT_S_TO_THE_AMB_S %(requestType, subject,\
                            AMBAmessage.mbf_object_to_string()))

    def __reconnect(self):
        global isConnected
        try:
            self.__initialiseWriterHandlers()
            isConnected = True
            self.__createAMBReader()
            UTILS.Logger.flogger.info('Ats reconnected to AMB')
            return True
        except RuntimeError, e:
            UTILS.Logger.flogger.info('Amb connection failed with reason (%s)' %str(e))
            return False

    def ambReconnectRoutine(self):
        while True:
            UTILS.Logger.flogger.info('Trying to reconnect in 5 seconds to AMB...')
            time.sleep(5.0)
            isReconnected = self.__reconnect()
            if isReconnected:
                break

    '''----------------------------------------------------------------------------------------------------------
    Function to log the ATS startup Information
    ----------------------------------------------------------------------------------------------------------'''
    def __logATSHeaderInformation(self):
        UTILS.Logger.flogger.info('*'*80)
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.ATS_STARTED_AT_S % str(time.ctime()))
        UTILS.Logger.flogger.info('*'*80)
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.ATS_NAME_S % str(UTILS.ComponentName))
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.PLATFORM_S % str(self._platformName))
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.PROCESS_ID_S % str(self._processId))
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.RESTART_ON_MEMORY_THRESHOLD_S % str(UTILS.Parameters.fcGenericParameters.restartIfMemoryThresholdExceeded))
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.MEMORY_THRESHOLD_S % str(UTILS.Parameters.fcGenericParameters.memoryThreshold))
        UTILS.Logger.flogger.info('*'*80)
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.SETTING_UP_AMBA_CONNECTIONS)
        UTILS.Logger.flogger.info('*'*80)
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.AMBA_HOST_S % str(UTILS.Parameters.fcComponentParameters.componentAMBHost))
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.AMB_READER_S % str(UTILS.Parameters.fcComponentParameters.componentReceiverName))
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.AMB_READER_SUBJECTS_S % str(UTILS.Parameters.fcComponentParameters.componentSubscriptionSubjects))
        UTILS.Logger.flogger.info('*'*80)

    '''----------------------------------------------------------------------------------------------------------
    Function to log the ATS startup complete Information
    ----------------------------------------------------------------------------------------------------------'''
    def __logATSHeaderStartupComplete(self):
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.ATS_STARTUP_COMPLETE)
        UTILS.Logger.flogger.info('*'*80)

    '''----------------------------------------------------------------------------------------------------------
    Create the AMB reader for receiving messages from the external request services (In this case it will be the
    specific AMBAs subscribing to events from Front Arena)
    ----------------------------------------------------------------------------------------------------------'''
    def __createAMBReader(self):
        if 'None' in (UTILS.Parameters.fcComponentParameters.componentAMBHost, \
                        UTILS.Parameters.fcComponentParameters.componentAMBPort, \
                        UTILS.Parameters.fcComponentParameters.componentReceiverName, \
                        UTILS.Parameters.fcComponentParameters.componentSubscriptionSubjects):
            return
        self._ambReader = ambReaderWriter.AMB_Reader('%s:%s' %(UTILS.Parameters.fcComponentParameters.componentAMBHost, UTILS.Parameters.fcComponentParameters.componentAMBPort),\
                            UTILS.Parameters.fcComponentParameters.componentReceiverName, \
                            event_cb_reader, \
                            UTILS.Parameters.fcComponentParameters.componentSubscriptionSubjects)
        if self._ambReader.open_AMB_Receiver_Connection_Kerberos(UTILS.Parameters.fcGenericParameters.AmbPrincipal,
                                                                     UTILS.Parameters.fcGenericParameters.AmbUser, '',
                                                                     UTILS.ComponentName, int(
                        UTILS.Parameters.fcGenericParameters.AmbSingleSignOn), isConnected) is False:
        #if not self._ambReader.open_AMB_Receiver_Connection():
            raise RuntimeError(UTILS.Constants.fcExceptionConstants.AMB_READER_CONNECTION_COULD_NOT_HAVE_BEEN_EST\
                    %(UTILS.Parameters.fcComponentParameters.componentAMBHost, UTILS.Parameters.fcComponentParameters.componentAMBPort,\
                    UTILS.Parameters.fcComponentParameters.componentReceiverName, UTILS.Parameters.fcComponentParameters.componentSubscriptionSubjects))
    
    '''----------------------------------------------------------------------------------------------------------
    Load AMB Writer Handler Dictionary and DB Writer Handler
    ----------------------------------------------------------------------------------------------------------'''
    def __loadWriterHandlerCollection(self):
        global isConnected
        self._writerHandlerCollection = HANDLER_CONTAINER(isConnected)
    
    def __initialiseWriterHandlers(self):
        self._writerHandlerCollection.initialise()
        
    '''----------------------------------------------------------------------------------------------------------
    Closing AMB Reader and Writer Connections
    ----------------------------------------------------------------------------------------------------------'''
    def __closeAMBConnections(self):
        global isConnected
        if self._ambReader:
            self._ambReader.close_AMB_Connection()
            isConnected = False
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.AMB_READER_CONNECTION_TO_AMB_CLOSED)
        for requestType in self._writerHandlerCollection.ambWriterHandlers.keys():
            self._writerHandlerCollection.ambWriterHandlers[requestType].ambWriter.close_AMB_Connection()
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.AMB_SENDER_CONN_TO_AMB_CLOSED_S %requestType)

    '''----------------------------------------------------------------------------------------------------------
    Returns the current process's virtual memory usage
    ----------------------------------------------------------------------------------------------------------'''
    def __getVirtualMemory(self):
        if self._platformName == UTILS.Constants.fcGenericConstants.WINDOWS:
            return int(acm.Memory().VirtualMemorySize()) / 1024.0
        elif self._platformName == UTILS.Constants.fcGenericConstants.LINUX:
            return os.popen('ps -p %d -o %s | tail -1' %(self._processId, 'vsz')).read()
        else:
            return 0

    '''----------------------------------------------------------------------------------------------------------
    Restarting the ATS Component
    ----------------------------------------------------------------------------------------------------------'''
    def __restartATS(self):
        self.ATS_STATUS = UTILS.Constants.fcGenericConstants.SHUTTING_DOWN
        try:
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.CLOSING_BOTH_AMB_READER_WRITER_CONNECTIONS_AMB)
            self.__closeAMBConnections()
        except RuntimeError, e:
            UTILS.ErrorHandler.processError(None, EXCEPTION(UTILS.Constants.fcExceptionConstants.AMB_READER_WRITER_CONNECTIONS_COULD_NOT_BE_CLOSED %__name__,\
                        traceback, UTILS.Constants.fcGenericConstants.MEDIUM, e))
        os._exit(1)

    def __checkShutdown(self):
        try:
            configuredTimes = UTILS.Parameters.fcGenericParameters.ShutdownTimes
            for configuredTime in configuredTimes:
                configuredTime = datetime.datetime.strptime(configuredTime, "%H:%M:%S").time()
                configured_datetime = FC_UTILS.Ats_startup_datetime.replace(hour=configuredTime.hour, minute=configuredTime.minute, second=0, microsecond=0)
                if datetime.datetime.now() >= configured_datetime and FC_UTILS.Ats_startup_datetime <= configured_datetime:
                    UTILS.ErrorHandler.forceShutDownWithMessage('FORCING THE ATS TO SHUT DOWN DUE TO SHUTDOWN CONFIGURATION...')
        except RuntimeError, e:
            UTILS.ErrorHandler.processError(None, EXCEPTION("ATS could not check the shutdown time %s" %__name__,\
traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

    '''----------------------------------------------------------------------------------------------------------
    Checking Memory Consumption. If memory usage is above threashold, the ATS will restart.
    ----------------------------------------------------------------------------------------------------------'''
    def __checkMemoryThreshold(self):
        global messageQueue
        
        currentVirtualMemory  = self.__getVirtualMemory()
        if UTILS.Parameters.fcGenericParameters.restartIfMemoryThresholdExceeded:
            if(int(currentVirtualMemory) > int(UTILS.Parameters.fcGenericParameters.memoryThreshold)):
                messageQueue.clear()
                UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.CURRENT_VIRTUAL_MEMORY_USAGE_S_EXCEEDS_MEMORY_THRESHOLD_S\
                                %(str(currentVirtualMemory), str(UTILS.Parameters.fcGenericParameters.memoryThreshold)))
                self.__restartATS()

    def RestartAts(self):
        self.__restartATS()

    def processIncommingAMBAMessage(self):
        raise NotImplementedError(UTILS.Constants.fcExceptionConstants.ATS_WORKER_IMPLEMENT_PROCESS_INCOMING_AMBA_MESSAGE)

    def mapIncomingAMBAMessageToIncomingMessageObject(self):
        raise NotImplementedError(UTILS.Constants.fcExceptionConstants.ATS_WORKER_IMLPEMENT_MAP_INCOMING_AMBA_MSG_TO_INCOMING_MSG_OBJ)

    def getLastProcessedMessageId(self):
        pass

    def createOutgoingMessageObjects(self):
        raise NotImplementedError(UTILS.Constants.fcExceptionConstants.ATS_WORKER_IMPLEMENT_CREATE_OUTGOING_MSG_OBJ)

    def mapOutgoingMessageObjectsToAMBADataDictionaries(self):
        for outgoingMessageObject in self.outgoingMessageObjects:
            outgoingAMBADataDictionary = outgoingMessageObject.mapMessageObjectToAMBADataDictionary()
            self.outgoingAMBADataDictionaries.append((outgoingMessageObject.type, outgoingAMBADataDictionary))
    
    def __readFirstMessageFromQueue(self):
        global messageQueue
        
        messageQueueItem = messageQueue.popleft()
        (self.incomingAMBAMessageObject, self.currentAMBChannel) = messageQueueItem
        messageid = self.incomingAMBAMessageObject.id
        self.currentMessageId = messageid
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.MSG_EVENT_RECEIVED_S % str(messageid))
        
    def __readIncommingAMBAMessageData(self):
        buffer = amb.mbf_create_buffer_from_data(self.incomingAMBAMessageObject.data_p)
        try:
            self.incomingAMBAMessageData = buffer.mbf_read()
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.MSG_RECEIVED_AMB_FORMAT_S %self.incomingAMBAMessageData.mbf_object_to_string())
        except Exception, e:
            UTILS.ErrorHandling.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION(UTILS.Constants.fcExceptionConstants.COULD_NOT_EXECUTE_BUFFER_MBF_READ_S %(str(self.incomingAMBAMessageObject.data_p), __name__),\
                    traceback, UTILS.Constants.fcGenericConstants.CRITICAL, e))

    def __generateOutgoingAMBAMessages(self):
        for outgoingAMBADataDictionary in self.outgoingAMBADataDictionaries:
            AMBADataInputList = [(None, UTILS.Constants.fcGenericConstants.DATA, outgoingAMBADataDictionary[1])]
            outgoingMessageSubject = ''    
            if UTILS.Constants.fcGenericConstants.SENDER_SUBJECT in outgoingAMBADataDictionary[1] and len(outgoingAMBADataDictionary[1][UTILS.Constants.fcGenericConstants.SENDER_SUBJECT]) > 0:             
                outgoingMessageSubject = outgoingAMBADataDictionary[1][UTILS.Constants.fcGenericConstants.SENDER_SUBJECT]
                #print 'using heartbeat***************************************', outgoingMessageSubject  
            else:                
                outgoingMessageSubject = self.__getOutgoingMessageSubject(outgoingAMBADataDictionary[0])
                #print 'using round robin**************************************', outgoingMessageSubject
                if UTILS.Parameters.fcComponentParameters.componentSenderHandlers[outgoingAMBADataDictionary[0]][2] == True:                
                    self.__increaseMultiSubjectNumber(outgoingAMBADataDictionary[0])
                
            outgoingAMBAMessageObject = AMBA_MESSAGE_GENERATOR(None, outgoingAMBADataDictionary[0], '1.0',\
                    None, UTILS.Parameters.fcComponentParameters.componentSenderHandlers[outgoingAMBADataDictionary[0]][1], AMBADataInputList)
                    
            outgoingAMBAMessageObject.generate_AMBA_Message()
            self.outgoingAMBAMessages.append((outgoingAMBADataDictionary[0], outgoingAMBAMessageObject.AMBA_Message, outgoingMessageSubject))
    
    # Round Robin
    def __getOutgoingMessageSubject(self, componentSenderHandlerName):
        if UTILS.Parameters.fcComponentParameters.componentSenderHandlers[componentSenderHandlerName][2] == True:
            subjectumber = self.__formatMultiSubjectNumber(componentSenderHandlerName)
            outgoingMessageSubject = '%s_%s' %(componentSenderHandlerName, subjectumber)
        else:
            outgoingMessageSubject = componentSenderHandlerName
        return outgoingMessageSubject
    
    def getOutgoingMessageSubject(self, componentSenderHandlerName):
        return self.__getOutgoingMessageSubject(componentSenderHandlerName)
    
    def __formatMultiSubjectNumber(self, componentSenderHandlerName):
        if len(str(self._writerHandlerCollection.ambWriterHandlers[componentSenderHandlerName].multiSubjectAllocationNbr)) < 2:
            subjectNumber = '0%s' %str(self._writerHandlerCollection.ambWriterHandlers[componentSenderHandlerName].multiSubjectAllocationNbr)
        else:
            subjectNumber = str(self._writerHandlerCollection.ambWriterHandlers[componentSenderHandlerName].multiSubjectAllocationNbr)
        return subjectNumber
    
    def __increaseMultiSubjectNumber(self, componentSenderHandlerName):
        if self._writerHandlerCollection.ambWriterHandlers[componentSenderHandlerName].multiSubjectAllocationNbr < UTILS.Parameters.fcComponentParameters.componentSenderHandlers[componentSenderHandlerName][3] +\
                                                                                                                    UTILS.Parameters.fcComponentParameters.componentSenderHandlers[componentSenderHandlerName][4] - 1:
            self._writerHandlerCollection.ambWriterHandlers[componentSenderHandlerName].multiSubjectAllocationNbr = self._writerHandlerCollection.ambWriterHandlers[componentSenderHandlerName].multiSubjectAllocationNbr + 1
        else:
            self._writerHandlerCollection.ambWriterHandlers[componentSenderHandlerName].multiSubjectAllocationNbr = UTILS.Parameters.fcComponentParameters.componentSenderHandlers[componentSenderHandlerName][4]
         
    def postOutgoingAMBAMessagesToAMB(self):
        for outgoingAMBAMessage in self.outgoingAMBAMessages:
            self.postAMBAMessageToAMB(outgoingAMBAMessage[1], outgoingAMBAMessage[0], outgoingAMBAMessage[2])
    
    def __acceptAMBAMessageFromAMB(self):
        global messageQueue
        global isConnected

        if isConnected is False:
            self.ambReconnectRoutine()
            isConnected = True
            amb.mb_poll()

        acceptResult = amb.mb_queue_accept(self.currentAMBChannel, self.incomingAMBAMessageObject, str(self.incomingAMBAMessageObject.id))
        
        if acceptResult != None:
            raise RuntimeError(UTILS.Constants.fcExceptionConstants.COULD_NOT_EXCEPT_MSG_S_FROM_AMB % str(self.incomingAMBAMessageObject.id))

        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.MSG_ACCEPTED_I % int(self.incomingAMBAMessageObject.id))
        
        '''----------------------------------------------------------------------------------------------------------
        Poll messages that might be waiting on the AMB.
        ----------------------------------------------------------------------------------------------------------'''
        amb.mb_poll()
        
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.S_MSG_REMAINING_IN_QUEUE %len(messageQueue))
        UTILS.MessageQueueDepth = len(messageQueue)

    def __dataCleanUp(self):
        self.incomingAMBAMessageObject = None
        self.incomingAMBAMessageData = None
        self.incomingMessageObject = None
        self.currentAMBChannel = None
        self.heartBeatCandidateComponent = None
        self.outgoingAMBADataDictionaries = []
        self.outgoingMessageObjects = []
        self.outgoingAMBAMessages = []

    def __deleteHeartBeat(self):
        UTILS.Logger.flogger.info('Delete any Current Heart Beat entries.')
        try:
            DATA_HELPER.DeleteHeartBeatProcess()
        except Exception, e:
            UTILS.ErrorHandler.processError(self._writerHandlerCollection.ambWriterHandlers[UTILS.Constants.fcGenericConstants.FC_ERROR_MESSAGE],\
                    EXCEPTION('Could not delete the Curret Heart Beat in module %s.' %__name__, traceback, 'CRITICAL', e))

    def getTradeIndexBatches(self, batchSize, tradeCount):
        try:
            batches = []
            if tradeCount==0:
                batches.append((0, 0))
            elif tradeCount <= batchSize:
                batches.append((0, tradeCount-1))
            else:
                i = 1
                startIndex=0
                endIndex = (i * batchSize) - 1
                remainder=0
                while endIndex < tradeCount-1:
                    batches.append((startIndex, endIndex))
                    startIndex = endIndex + 1
                    i = i + 1
                    endIndex = (i * batchSize) - 1
                
                #Get the remainder
                previousEndIndex = ((i-1) * batchSize) - 1
                remainder = tradeCount - previousEndIndex
                if (remainder) > 0:
                    startIndex = previousEndIndex + 1
                    endIndex = tradeCount-1
                    batches.append((startIndex, tradeCount-1))
            return batches
        except Exception, error:
            raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_GET_TRADE_INDEX_BATCHES_S % str(error))
            
    def setHeartBeatCandidateComponent(self, requestType):
        self.heartBeatCandidateComponent = DATA_HELPER.GetHeartbeatCandidateComponent(requestType)
