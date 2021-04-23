
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_AD_HOC_QUERYFOLDER_TRD_MSG
PROJECT                 :       Front Cache
PURPOSE                 :       This module contains a REQUEST type that inherits from the MESSAGE OBJECT BASE.
                                It contains a couple of additional properties only applicable for a REQUEST
                                Message Type.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Busisiwe Masango
CR NUMBER               :       XXXXXX

----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python and custom modules needed for the FC AD HOC QUERYFOLDER TRD MSG REQUEST GENERATOR to initialize.
Initializing the FC_UTILS module to load all Parameters, Logging, Error Handler.
----------------------------------------------------------------------------------------------------------'''

import FC_ERROR_HANDLER_DEFAULT as ERROR_HANDLER_DEFAULT
import acm, ael, datetime, traceback, locale, re, at, at_time

ael_variables = [
                    ['query_folder', 'Query Folder', acm.FStoredASQLQuery, acm.FStoredASQLQuery, None, 1, 0, 'Query folder containing the trades required.', None, 1],
                    ['tradeTopic', 'Topic', 'string', None, 'INTRADAY_TRADE_REQUEST', 0, 0, '', None, 0],
                    ['tradeDateToday', 'Connect with Date Today', 'int', [0, 1], 0, 0, 0, '', None, 1]
                ]
                

try:
    from FC_UTILS import FC_UTILS as UTILS
except ImportError, e:
    ERROR_HANDLER_DEFAULT.handelError('Import Error in module %s.' %__name__, e, traceback)
    raise ImportError('Import Error in module %s. ERROR: %s.' %(__name__, str(e)))

try:
    UTILS.Initialize('FC_AD_HOC_REQUEST_GENERATOR')
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
    import FC_DB_MSSQL_PROVIDER as DB_MSSQL_PROVIDER
except ImportError, e:
    UTILS.ErrorHandler.processError(None, EXCEPTION('Could not import the worker module in module %s' %__name__, traceback, 'CRITICAL', None), __name__)
    raise Exception('Could not import the worker module in module %s. ERROR: %s' %(__name__, str(e)))

try:
    import FC_DATA_HELPER as DATA_HELPER
except ImportError, e:
    UTILS.ErrorHandler.processError(None, EXCEPTION('Could not import the worker module in module %s' %__name__, traceback, 'CRITICAL', None), __name__)
    raise Exception('Could not import the worker module in module %s. ERROR: %s' %(__name__, str(e)))

try:
    from FC_HANDLER_CONTAINER import FC_HANDLER_CONTAINER as HANDLER_CONTAINER
except ImportError, e:
    UTILS.ErrorHandler.processError(None, EXCEPTION('Could not import the worker module in module %s' %__name__, traceback, 'CRITICAL', None), __name__)
    raise Exception('Could not import the worker module in module %s. ERROR: %s' %(__name__, str(e)))

try:
    from AMBA_GENERATE_MESSAGE import AMBA_GENERATE_MESSAGE as AMBA_MESSAGE_GENERATOR
except ImportError, e:
    UTILS.ErrorHandler.processError(None, EXCEPTION('Could not import the worker module in module %s' %__name__, traceback, 'CRITICAL', None), __name__)
    raise Exception('Could not import the worker module in module %s. ERROR: %s' %(__name__, str(e)))

try:
    from FC_MESSAGE_OBJECT_REQUEST import FC_MESSAGE_OBJECT_REQUEST as MESSAGE_OBJECT_REQUEST
except ImportError, e:
    UTILS.ErrorHandler.processError(None, EXCEPTION('Could not import the worker module in module %s' %__name__, traceback, 'CRITICAL', None), __name__)
    raise Exception('Could not import the worker module in module %s. ERROR: %s' %(__name__, str(e)))

try:
    from FC_MESSAGE_OBJECT_RESPONSE import FC_MESSAGE_OBJECT_RESPONSE as MESSAGE_OBJECT_RESPONSE
except ImportError, e:
    UTILS.ErrorHandler.processError(None, EXCEPTION('Could not import the worker module in module %s' %__name__, traceback, 'CRITICAL', None), __name__)
    raise Exception('Could not import the worker module in module %s. ERROR: %s' %(__name__, str(e)))

'''----------------------------------------------------------------------------------------------------------
Global variables
----------------------------------------------------------------------------------------------------------'''
global writerHandlerCollection
writerHandlerCollection = None

'''----------------------------------------------------------------------------------------------------------
CONSTANTS
----------------------------------------------------------------------------------------------------------'''

def demacroize(s):
    """Returns the input string with macros replaced."""
    def todayrepl_format(matchobj):
        """Today."""
        today = at.date_to_datetime(acm.Time.DateToday())
        return today.strftime(matchobj.group(1))

    def nextbdrepl_format(matchobj):
        """Next business day."""
        cal = acm.FInstrument['ZAR'].Calendar()
        today = acm.Time.DateToday()
        nextbd = at.date_to_datetime(cal.AdjustBankingDays(today, 1))
        return nextbd.strftime(matchobj.group(1))

    def yesterdayrepl_format(matchobj):
        """Yesterday."""
        today = at_time.date_today()
        yesterday = at_time.add_days(today, -1)
        return yesterday.strftime(matchobj.group(1))

    def prevbdrepl_format(matchobj):
        """Previous Banking Day."""
        cal = acm.FInstrument['ZAR'].Calendar()
        today = acm.Time.DateToday()
        prevbd = at.date_to_datetime(cal.AdjustBankingDays(today, -1))
        return prevbd.strftime(matchobj.group(1))

    s = re.sub('{TODAY:([^}]+)}', todayrepl_format, s)
    s = re.sub('{NEXTBD:([^}]+)}', nextbdrepl_format, s)
    s = re.sub('{YESTERDAY:([^}]+)}', yesterdayrepl_format, s)
    s = re.sub('{PREVBD:([^}]+)}', prevbdrepl_format, s)
    # add more macros here if necessary...
    return s

def createAmbWriterHandler():
    global writerHandlerCollection
    writerHandlerCollection = HANDLER_CONTAINER()
    writerHandlerCollection.initialise()

def createOutgoingMessageObjectRequest(ambaTxNbr, batchId, isEOD, reportDate, requestDateTime, requestEventType,
                                       requestId, requestSource, requestType, requestUserId, scopeName, scopeNumber,
                                       topic, type, isDateToday):
    outgoingMessageObject = MESSAGE_OBJECT_REQUEST()
    outgoingMessageObject.ambaTxNbr = ambaTxNbr
    outgoingMessageObject.batchId = batchId
    outgoingMessageObject.isEOD = isEOD
    outgoingMessageObject.reportDate = reportDate
    outgoingMessageObject.requestDateTime = requestDateTime
    outgoingMessageObject.requestEventType = requestEventType
    outgoingMessageObject.requestId = requestId
    outgoingMessageObject.requestSource = requestSource
    outgoingMessageObject.requestType = requestType
    outgoingMessageObject.requestUserId = requestUserId
    outgoingMessageObject.scopeName = scopeName
    outgoingMessageObject.scopeNumber = scopeNumber
    outgoingMessageObject.requestCollectionPrimaryKeys = scopeNumber
    #outgoingMessageObject.senderSubject = 'SenderSubject'
    outgoingMessageObject.topic = topic
    outgoingMessageObject.type = type
    outgoingMessageObject.isDateToday = isDateToday

    return outgoingMessageObject

def createOutgoingMessageObjectResponse(ambaTxNbr, batchId, isEOD, reportDate, requestDateTime, requestEventType, requestId, requestSource, requestType, requestUserId, scopeName, scopeNumber, topic, type, responseType, expectedObjectCount, outgoingMsgType):
    outgoingMessageObject = MESSAGE_OBJECT_RESPONSE()
    outgoingMessageObject.ambaTxNbr = ambaTxNbr
    outgoingMessageObject.batchId = batchId
    outgoingMessageObject.isEOD = isEOD
    outgoingMessageObject.reportDate = reportDate
    outgoingMessageObject.requestDateTime = requestDateTime
    outgoingMessageObject.requestEventType = requestEventType
    outgoingMessageObject.requestId = requestId
    outgoingMessageObject.requestSource = requestSource
    outgoingMessageObject.requestType = requestType
    outgoingMessageObject.requestUserId = requestUserId
    outgoingMessageObject.scopeName = scopeName
    outgoingMessageObject.scopeNumber = scopeNumber
    #outgoingMessageObject.senderSubject = 'SenderSubject'
    outgoingMessageObject.topic = topic
    outgoingMessageObject.type = type
    outgoingMessageObject.responseType = responseType
    outgoingMessageObject.expectedObjectCount = expectedObjectCount

    return outgoingMessageObject

def mapOutgoingMessageObjectsToAMBADataDictionaries(outgoingMessageObjects):
    outgoingAMBADataDictionaries = []
    for outgoingMessageObject in outgoingMessageObjects:
        outgoingAMBADataDictionary = outgoingMessageObject.mapMessageObjectToAMBADataDictionary()
        outgoingAMBADataDictionaries.append((outgoingMessageObject.type, outgoingAMBADataDictionary))
    return outgoingAMBADataDictionaries

def generateOutgoingAMBAMessages(outgoingAMBADataDictionaries):
    outgoingAMBAMessages = []
    for outgoingAMBADataDictionary in outgoingAMBADataDictionaries:
        AMBADataInputList = [(None, 'DATA', outgoingAMBADataDictionary[1])]

        #Determine the Subject that should be used in the message going out.
        outgoingAMBAMessageObject = AMBA_MESSAGE_GENERATOR(None, outgoingAMBADataDictionary[0], '1.0', None, __name__, AMBADataInputList)

        outgoingAMBAMessageObject.generate_AMBA_Message()
        outgoingAMBAMessages.append((outgoingAMBADataDictionary[0], outgoingAMBAMessageObject.AMBA_Message))
    return outgoingAMBAMessages

def postAMBAMessageToAMB(AMBAMessage, requestType):
    global writerHandlerCollection
    writerHandlerCollection.ambWriterHandlers[requestType].ambWriter.post_Message_To_AMB(AMBAMessage)

def postOutgoingAMBAMessagesToAMB(outgoingAMBAMessages):
    for outgoingAMBAMessage in outgoingAMBAMessages:
            postAMBAMessageToAMB(outgoingAMBAMessage[1], outgoingAMBAMessage[0])

def ael_main(ael_dict):
    global writerHandlerCollection
    
    sheet_type = 'FTradeSheet'
    context = acm.GetDefaultContext()
    calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)
    queryObj = ael_dict['query_folder'].Value()
    node = calc_space.InsertItem(queryObj)
    calc_space.Refresh()
    
    tradeList = node.Item().Children()
    tradeReportDate = datetime.datetime.today().strftime('%Y-%m-%d')
    tradeReportDateTime = '%s 00:00:00' %tradeReportDate
    tradeTopic = ael_dict['tradeTopic']
    tradeDateToday = ael_dict['tradeDateToday']
    
    try:
        createAmbWriterHandler()
    except Exception, e:
        UTILS.ErrorHandler.processError(None, EXCEPTION('Could not create the AMB writers in module %s.' %__name__,\
            traceback, 'CRITICAL', e))
    
    singleTradeList = tradeList
    singleTradeListLength = len(singleTradeList)

    try:
        if singleTradeListLength > 0:
            outgoingMessageObjectsSingleTrades = []
            outgoingMessageObjectsSingleTradesBatchStartList = []
            tradeBatchId = '0'
            if singleTradeListLength > 1:
                UTILS.Logger.flogger.info('%i Trade selected. Registering Batch...' %singleTradeListLength)
                tradeBatchId = DATA_HELPER.RegisterBatch(tradeReportDate, '0', tradeTopic, singleTradeListLength)
                
                if tradeBatchId:
                    outgoingMessageObjectSingleTradeBatchStart = createOutgoingMessageObjectResponse('0', str(tradeBatchId), '0', tradeReportDate,\
                                                                                            tradeReportDateTime, 'INTRADAY_TRADE', '', __name__,\
                                                                                            'SINGLE_TRADE', acm.User().Name(), '', '', tradeTopic,\
                                                                                            'RESPONSE', 'BATCH_START', singleTradeListLength, 'EVENT_RESPONSE')
                    outgoingMessageObjectsSingleTradesBatchStartList.append(outgoingMessageObjectSingleTradeBatchStart)
                    outgoingMessageObjectsToAMBADataDictionariesSingleTradesBatchStart = mapOutgoingMessageObjectsToAMBADataDictionaries(outgoingMessageObjectsSingleTradesBatchStartList)
                    outgoingAMBAMessagesSingleTradesBatchStart = generateOutgoingAMBAMessages(outgoingMessageObjectsToAMBADataDictionariesSingleTradesBatchStart)
                    postOutgoingAMBAMessagesToAMB(outgoingAMBAMessagesSingleTradesBatchStart)
                    UTILS.Logger.flogger.info('Batch successfully registered. Corresponding BatchId : %i' %tradeBatchId)
                else:
                    UTILS.Logger.flogger.info('Batch regestration error. Will continue to send requests for trades. No Batch Id to subscribe on. Please use Topic if supplied.')

            for singleTrade in singleTradeList:
                outgoingMessageObjectSingleTrade = createOutgoingMessageObjectRequest('0', str(tradeBatchId), '0',
                                                                                      tradeReportDate,
                                                                                      tradeReportDateTime,
                                                                                      'INTRADAY_TRADE', '', __name__,
                                                                                      'SINGLE_TRADE', acm.User().Name(),
                                                                                      singleTrade.Trade().Name(),
                                                                                      str(singleTrade.Trade().Oid()),
                                                                                      tradeTopic, 'REQUEST', tradeDateToday)
                outgoingMessageObjectsSingleTrades.append(outgoingMessageObjectSingleTrade)
            outgoingMessageObjectsToAMBADataDictionariesSingleTrades = mapOutgoingMessageObjectsToAMBADataDictionaries(outgoingMessageObjectsSingleTrades)
            outgoingAMBAMessagesSingleTrades = generateOutgoingAMBAMessages(outgoingMessageObjectsToAMBADataDictionariesSingleTrades)
            postOutgoingAMBAMessagesToAMB(outgoingAMBAMessagesSingleTrades)
    except Exception, e:
        UTILS.ErrorHandler.processError(None, EXCEPTION('Could not process the Single Trade GUI Request(s) in module %s.' %__name__,\
            traceback, 'CRITICAL', e))

    UTILS.Logger.flogger.info('STEP 2 - Complete at %s' %datetime.datetime.now())
    UTILS.Logger.flogger.info('-'*70)
    UTILS.Logger.flogger.info('STEP 2.5 - Starting SINGLE_SETTLEMENTS Requests at %s' %datetime.datetime.now())
