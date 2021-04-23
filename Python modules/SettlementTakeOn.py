
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_AD_HOC_REQUEST_GENERATOR
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module contains a REQUEST type that inherits from the MESSAGE OBJECT BASE.
                                It contains a couple of additional properties only applicable for a REQUEST
                                Message Type.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX

Date            CR Number       Developer               Description
2014-08-13      XXXXXX          Heinrich Cronje         Added the Request Type and Request Event Type information
                                                        to the Batch Start Events. Also, defaulted the Batch 
                                                        Start Request Id and Scope Numbers to blank.
2014-09-18      XXXXXX          Heinrich Cronje         Added the Exclude Portfolios from the Portfolio Trades Request
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python and custom modules needed for the AD HOC REQUEST GENERATOR to initialize.
Initializing the FC_UTILS module to load all Parameters, Logging, Error Handler.
----------------------------------------------------------------------------------------------------------'''
import FC_ERROR_HANDLER_DEFAULT as ERROR_HANDLER_DEFAULT
import acm, ael, datetime, traceback, locale, re, at, at_time

'''----------------------------------------------------------------------------------------------------------
Setting Grouping format for numbers
----------------------------------------------------------------------------------------------------------'''
locale.setlocale(locale.LC_ALL, '')

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
ON_TREE_COMPOUND_PORTFOLIO = 'ABSA BANK LTD'

def createAmbWriterHandler():
    global writerHandlerCollection
    writerHandlerCollection = HANDLER_CONTAINER()
    writerHandlerCollection.initialise()

def getAllPhysicalPortfoliosFromCompoundPortfolio(compoundPortfolioObject):
    if compoundPortfolioObject and compoundPortfolioObject.Compound():
        return compoundPortfolioObject.AllPhysicalPortfolios()
    return None

def isPhysicalPortfolio(portfolioObject):
    if portfolioObject:
        if not portfolioObject.Compound():
            return True
    return False

def getOffTreePortoflios():
    offTreePortfolioList = []
    compoundPortfolios = acm.FPhysicalPortfolio.Select('compound = 1')
    for compoundPortfolio in compoundPortfolios:
        if len(compoundPortfolio.MemberLinks()) > 0:
            for memberLink in compoundPortfolio.MemberLinks():
                if memberLink.OwnerPortfolio() == None:
                    if compoundPortfolio.Name() != ON_TREE_COMPOUND_PORTFOLIO:
                        offTreePortfolioList.append(compoundPortfolio.Name())
    return offTreePortfolioList

def getStringOfOffTreePortfolios():
    offTreePortfolios = getOffTreePortoflios()
    portfolioString = offTreePortfolios[0]
    i = 1
    while i < len(offTreePortfolios):
        portfolioString = '%s,%s' %(portfolioString, offTreePortfolios[i])
        i = i + 1
    return portfolioString

def getAllPortfolios():
    allPortfolios = acm.FPhysicalPortfolio.Select('compound = 0')
    allPortfoliosString = allPortfolios[0].Name()
    i = 1
    while i < len(allPortfolios):
        allPortfoliosString = '%s,%s' %(allPortfoliosString, allPortfolios[i].Name())
        i = i + 1
    return allPortfoliosString

def getSettlementTakeOn():
    endDate = datetime.datetime.today() + datetime.timedelta(days=10)
    list = acm.FSettlement.Select('valueDay >= "%s" and valueDay <= "%s"' %(datetime.datetime.today().strftime('%y-%m-%d'), endDate.strftime('%y-%m-%d')))
    return list

def setPortfolioIsEODValues(index, fieldValues):
    #Set default fildvalues for deselecting
    if fieldValues[8] == 'No':
        ael_variables[6][9] = 1
        ael_variables[9][9] = 0
        ael_variables[9][5] = 0
        fieldValues[9] = ''
    
    if fieldValues[8] == 'Yes':
        ael_variables[6][9] = 0
        ael_variables[9][9] = 1
        ael_variables[9][5] = 1
    
    return fieldValues

def setPortfolioTreeOnTreeOffTreeValues(index, fieldValues):
    if fieldValues[9] == 'ON TREE PORTFOLIOS':
        fieldValues[6] = ON_TREE_COMPOUND_PORTFOLIO
        ael_variables[6][9] = 0
    elif fieldValues[9] == 'OFF TREE PORTFOLIOS':
        fieldValues[6] = getStringOfOffTreePortfolios()
        ael_variables[6][9] = 0
    elif fieldValues[9] == 'ON AND OFF TREE PORTFOLIOS':
        fieldValues[6] = '%s,%s' %(ON_TREE_COMPOUND_PORTFOLIO, getStringOfOffTreePortfolios())
        ael_variables[6][9] = 0
    elif fieldValues[9] == 'ALL PORTFOLIOS':
        fieldValues[6] = getAllPortfolios()
        ael_variables[6][9] = 0
    elif fieldValues[9] == 'SPECIFIC PORTFOLIO':
        ael_variables[6][9] = 1
    
    return fieldValues

def createOutgoingMessageObjectRequest(ambaTxNbr, batchId, isEOD, reportDate, requestDateTime, requestEventType, requestId, requestSource, requestType, requestUserId, scopeName, scopeNumber, topic, type, outgoingMsgType):
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
    #outgoingMessageObject.senderSubject = 'SenderSubject'
    outgoingMessageObject.topic = topic
    outgoingMessageObject.type = type

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

boolEODDict = {'Yes' : True,
                'No' : False}
boolEODDictDisplay = boolEODDict.keys()
boolEODDictDisplay.sort()

onOffTreeList = ['ON TREE PORTFOLIOS', 'OFF TREE PORTFOLIOS', 'ON AND OFF TREE PORTFOLIOS', 'ALL PORTFOLIOS', 'SPECIFIC PORTFOLIO']
onOffTreeList.sort()

boolAllPortfolioDict = {'Yes' : True,
                        'No' : False}
boolAllPortfolioDisplay = boolAllPortfolioDict.keys()
boolAllPortfolioDisplay.sort()

boolSettlementTakeOnDict = {'Yes' : True,
                            'No' : False}

dateDisplayList = ['{TODAY:%Y-%m-%d}', '{YESTERDAY:%Y-%m-%d}', '{PREVBD:%Y-%m-%d}']

ael_variables = [
                    ['tradeList', 'Trade Numbers_Single Trade Request', acm.FTrade, '', '', 0, 1, 'SINGLE_TRADE requests will be send for the trades selected.', None, 1],
                    ['tradeReportDate', 'Trade Report Date_Single Trade Request', 'string', dateDisplayList, '{TODAY:%Y-%m-%d}', 1, 0, 'Report date for the SINGLE_TRADE requests will be send.', None, 1],
                    ['tradeTopic', 'Topic_Single Trade Request', 'string', None, 'INTRADAY_TRADE_REQUEST', 0, 0, 'Topic on which the requester can subscribe to get the result from this request.', None, 1],
                    
                    ['instrumentList', 'Instruments_Instrument Trades Request', acm.FInstrument, '', '', 0, 1, 'INSTRUMENT_TRADES requests will be send for the instruments selected.', None, 1],
                    ['instrumentReportDate', 'Instrument Report Date_Instrument Trades Request', 'string', dateDisplayList, '{TODAY:%Y-%m-%d}', 1, 0, 'Report date for the INSTRUMENT_TRADES requests will be send.', None, 1],
                    ['instrumentTopic', 'Topic_Instrument Trades Request', 'string', None, 'INTRADAY_INSTRUMENT_TRADES_REQUEST', 0, 0, 'Topic on which the requester can subscribe to get the result from this request.', None, 1],
                    
                    ['portfolioList', 'Portfolios_Portfolios Trades Request', acm.FPhysicalPortfolio, '', '', 0, 1, 'PORTFOLIO_TRADES requests will be send for the portfolios selected.', None, 1],
                    ['portfolioReportDate', 'Portfolio Report Date_Portfolios Trades Request', 'string', dateDisplayList, '{TODAY:%Y-%m-%d}', 1, 0, 'Report date for the PORTFOLIO_TRADES requests will be send.', None, 1],
                    ['portfolioIsEOD', 'Official EOD Run_Portfolios Trades Request', 'string', boolEODDictDisplay, 'No', 1, 0, 'The Request will be flagged as the official EOD Batch.', setPortfolioIsEODValues, 1],
                    ['portfolioTree', 'On/Off Tree_Portfolios Trades Request', 'string', onOffTreeList, '', 0, 0, 'ON TREE will send PORTFOLIO_TRADES requests for all physical portfolios under %s. OFF TREE will send PORTFOLIO_TRADES requests for all physical portfolios NOT under %s.' %(ON_TREE_COMPOUND_PORTFOLIO, ON_TREE_COMPOUND_PORTFOLIO), setPortfolioTreeOnTreeOffTreeValues, 0],
                    ['portfolioTopic', 'Topic_Portfolios Trades Request', 'string', None, 'INTRADAY_PORTFOLIO_TRADES_REQUEST', 0, 0, 'Topic on which the requester can subscribe to get the result from this request.', None, 1],
                    ['portfolioExcludePortfolioList', 'Exclude Portfolios_Portfolios Trades Request', acm.FPhysicalPortfolio, '', '', 0, 1, 'Specific which portfolios should be excluded from the portfolios selected in the Portfolios field.', None, 1],
                    
                    ['settlementList', 'Settlement Numbers_Single Settlement Request', acm.FSettlement, '', '', 0, 1, 'SINGLE_SETTLEMENT requests will be sent for the settlements selected.', None, 1],
                    ['settlementReportDate', 'Settlement Report Date_Single Settlement Request', 'string', dateDisplayList, '{TODAY:%Y-%m-%d}', 1, 0, 'Report date for the SINGLE_SETTLEMENT requests will be send.', None, 1],
                    ['settlementTopic', 'Topic_Single Settlement Request', 'string', None, 'INTRADAY_SETTLEMENT_REQUEST', 0, 0, 'Topic on which the requester can subscribe to get the result from this request.', None, 1]
                ]

def ael_main(dict):
    global writerHandlerCollection
    
    UTILS.Logger.flogger.info('-'*70)
    UTILS.Logger.flogger.info('Starting %s at %s' %(__name__, datetime.datetime.now()))
    UTILS.Logger.flogger.info('-'*70)
    
    tradeList = dict['tradeList']
    tradeReportDate = demacroize(dict['tradeReportDate'])
    tradeReportDateTime = '%s 00:00:00' %tradeReportDate
    tradeTopic = dict['tradeTopic']
    
    instrumentList = dict['instrumentList']
    instrumentReportDate = demacroize(dict['instrumentReportDate'])
    instrumentReportDateTime = '%s 00:00:00' %instrumentReportDate
    instrumentTopic = dict['instrumentTopic']
    
    portfolioList = dict['portfolioList']
    portfolioReportDate = demacroize(dict['portfolioReportDate'])
    portfolioReportDateTime = '%s 00:00:00' %portfolioReportDate
    portfolioIsEOD = dict['portfolioIsEOD']
    portfolioTree = dict['portfolioTree']
    portfolioTopic = dict['portfolioTopic']
    portfolioExcludePortfolioList = dict['portfolioExcludePortfolioList']
    
    settlementList = dict['settlementList']
    settlementReportDate = demacroize(dict['settlementReportDate'])
    settlementReportDateTime = '%s 00:00:00' %settlementReportDate
    settlementTopic = dict['settlementTopic']
    
    UTILS.Logger.flogger.info('-'*70)
    UTILS.Logger.flogger.info('STEP 1 - Opening AMB connection at %s' %datetime.datetime.now())

    try:
        createAmbWriterHandler()
    except Exception, e:
        UTILS.ErrorHandler.processError(None, EXCEPTION('Could not create the AMB writers in module %s.' %__name__,\
            traceback, 'CRITICAL', e))

    UTILS.Logger.flogger.info('STEP 1 - Complete at %s' %datetime.datetime.now())
    UTILS.Logger.flogger.info('-'*70)
    
    UTILS.Logger.flogger.info('STEP 2 - Starting SINGLE_TRADE Requests at %s' %datetime.datetime.now())
    
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
                outgoingMessageObjectSingleTrade = createOutgoingMessageObjectRequest('0', str(tradeBatchId), '0', tradeReportDate, \
                                                tradeReportDateTime, 'INTRADAY_TRADE', '', __name__, 'SINGLE_TRADE', acm.User().Name(), \
                                                singleTrade.Name(), str(singleTrade.Oid()), tradeTopic, 'REQUEST', 'REQT_ST')
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
    # ******************************* SINGLE SETTLEMENTS ******************************************
    
    try:
        if (len(settlementList) == 0):
            settlementList = getSettlementTakeOn()
        singleSettlementList = settlementList
        singleSettlementListLength = len(singleSettlementList)
        if singleSettlementListLength > 0:
            outgoingMessageObjectsSingleSettlements = []
            outgoingMessageObjectsSingleSettlementsBatchStartList = []
            settlementBatchId = '0'
            if singleSettlementListLength > 1:
                UTILS.Logger.flogger.info('%i Settlement selected. Registering Batch...' %singleSettlementListLength)
                settlementBatchId = DATA_HELPER.RegisterBatch(settlementReportDate, '0', settlementTopic, singleSettlementListLength)
                
                if settlementBatchId:
                    outgoingMessageObjectSingleSettlementBatchStart = createOutgoingMessageObjectResponse('0', str(settlementBatchId), '0', settlementReportDate,\
                                                                                            settlementReportDateTime, 'INTRADAY_TRADE', '', __name__,\
                                                                                            'SINGLE_SETTLEMENT', acm.User().Name(), '', '', settlementTopic,\
                                                                                            'RESPONSE', 'BATCH_START', singleSettlementListLength, 'EVENT_RESPONSE')
                    outgoingMessageObjectsSingleSettlementsBatchStartList.append(outgoingMessageObjectSingleSettlementBatchStart)
                    outgoingMessageObjectsToAMBADataDictionariesSingleSettlementsBatchStart = mapOutgoingMessageObjectsToAMBADataDictionaries(outgoingMessageObjectsSingleSettlementsBatchStartList)
                    outgoingAMBAMessagesSingleSettlementsBatchStart = generateOutgoingAMBAMessages(outgoingMessageObjectsToAMBADataDictionariesSingleSettlementsBatchStart)
                    postOutgoingAMBAMessagesToAMB(outgoingAMBAMessagesSingleSettlementsBatchStart)
                    UTILS.Logger.flogger.info('Batch successfully registered. Corresponding BatchId : %i' %settlementBatchId)
                else:
                    UTILS.Logger.flogger.info('Batch regestration error. Will continue to send requests for settlements. No Batch Id to subscribe on. Please use Topic if supplied.')
                
            for singleSettlement in singleSettlementList:
                outgoingMessageObjectSingleSettlement = createOutgoingMessageObjectRequest('0', str(settlementBatchId), '0', settlementReportDate, \
                                                settlementReportDateTime, 'INTRADAY_SETTLEMENT', '', __name__, 'SINGLE_SETTLEMENT', acm.User().Name(), \
                                                singleSettlement.Name(), str(singleSettlement.Oid()), settlementTopic, 'REQUEST', 'REQT_SS')
                outgoingMessageObjectsSingleSettlements.append(outgoingMessageObjectSingleSettlement)
            outgoingMessageObjectsToAMBADataDictionariesSingleSettlements = mapOutgoingMessageObjectsToAMBADataDictionaries(outgoingMessageObjectsSingleSettlements)
            outgoingAMBAMessagesSingleSettlements = generateOutgoingAMBAMessages(outgoingMessageObjectsToAMBADataDictionariesSingleSettlements)
            postOutgoingAMBAMessagesToAMB(outgoingAMBAMessagesSingleSettlements)        
    except Exception, e:
        UTILS.ErrorHandler.processError(None, EXCEPTION('Could not process the Single Settlement GUI Request(s) in module %s.' %__name__,\
            traceback, 'CRITICAL', e))  
    UTILS.Logger.flogger.info('STEP 2 - Complete at %s' %datetime.datetime.now())
    UTILS.Logger.flogger.info('-'*70)  
    #********************************* END SINGLE SETTLEMENTS *************************************
    
    UTILS.Logger.flogger.info('STEP 3 - Starting INSTRUMENT_TRADES Requests at %s' %datetime.datetime.now())
    
    instrumentTradesList = instrumentList
    instrumentTradesListLength = len(instrumentTradesList)
    
    try:
        if instrumentTradesListLength > 0:
            instrumentBatchId = '0'
            outgoingMessageObjectsInstrumentTrades = []
            outgoingMessageObjectsInstrumentTradesBatchStartList = []
            if instrumentTradesListLength > 1:
                instrumentBatchId = DATA_HELPER.RegisterBatch(instrumentReportDate, '0', instrumentTopic, instrumentTradesListLength)
                if instrumentBatchId:
                    outgoingMessageObjectInstrumentTradesBatchStart = createOutgoingMessageObjectResponse('0', str(instrumentBatchId), '0',\
                                                                                            instrumentReportDate, instrumentReportDateTime, \
                                                                                            'INTRADAY_INSTRUMENT_TRADES', '', __name__, \
                                                                                            'INSTRUMENT_TRADES', acm.User().Name(), '', '', \
                                                                                            instrumentTopic, 'RESPONSE', 'BATCH_START', \
                                                                                            instrumentTradesListLength, 'EVENT_RESPONSE')
                    outgoingMessageObjectsInstrumentTradesBatchStartList.append(outgoingMessageObjectInstrumentTradesBatchStart)
                    outgoingMessageObjectsToAMBADataDictionariesInstrumentTradesBatchStart = mapOutgoingMessageObjectsToAMBADataDictionaries(outgoingMessageObjectsInstrumentTradesBatchStartList)
                    outgoingAMBAMessagesInstrumentTradesBatchStart = generateOutgoingAMBAMessages(outgoingMessageObjectsToAMBADataDictionariesInstrumentTradesBatchStart)
                    postOutgoingAMBAMessagesToAMB(outgoingAMBAMessagesInstrumentTradesBatchStart)
                    UTILS.Logger.flogger.info('Batch successfully registered. Corresponding BatchId : %i' %instrumentBatchId)
                else:
                    UTILS.Logger.flogger.info('Batch regestration error. Will continue to send requests for instrument trades. No Batch Id to subscribe on. Please use Topic if supplied.')
            
            for instrumentTrade in instrumentTradesList:
                outgoingMessageObjectInstrumentTrades = createOutgoingMessageObjectRequest('0', str(instrumentBatchId), '0', instrumentReportDate, \
                                                    instrumentReportDateTime, 'INTRADAY_INSTRUMENT_TRADES', '', __name__, 'INSTRUMENT_TRADES', \
                                                    acm.User().Name(), instrumentTrade.Name(), str(instrumentTrade.Oid()), instrumentTopic, 'REQUEST', 'REQT_IT')
                outgoingMessageObjectsInstrumentTrades.append(outgoingMessageObjectInstrumentTrades)
            outgoingMessageObjectsToAMBADataDictionariesInstrumentTrades = mapOutgoingMessageObjectsToAMBADataDictionaries(outgoingMessageObjectsInstrumentTrades)
            outgoingAMBAMessagesInstrumentTrades = generateOutgoingAMBAMessages(outgoingMessageObjectsToAMBADataDictionariesInstrumentTrades)
            postOutgoingAMBAMessagesToAMB(outgoingAMBAMessagesInstrumentTrades)
    except Exception, e:
        UTILS.ErrorHandler.processError(None, EXCEPTION('Could not process the Instrument Trades GUI Request(s) in module %s.' %__name__,\
            traceback, 'CRITICAL', e))

    UTILS.Logger.flogger.info('STEP 3 - Complete at %s' %datetime.datetime.now())
    UTILS.Logger.flogger.info('-'*70)
    
    UTILS.Logger.flogger.info('STEP 4 - Starting PORTFOLIO_TRADES Requests at %s' %datetime.datetime.now())
    
    try:
        physicalExcludePortfolioTradesList = []
        for excludePortfolio in portfolioExcludePortfolioList:
            if isPhysicalPortfolio(excludePortfolio):
                physicalExcludePortfolioTradesList.append(excludePortfolio)
            else:
                for physicalExcludePortfolio in getAllPhysicalPortfoliosFromCompoundPortfolio(excludePortfolio):
                    physicalExcludePortfolioTradesList.append(physicalExcludePortfolio)
        
        physicalPortfolioTradesList = []
        for portfolio in portfolioList:
            if isPhysicalPortfolio(portfolio):
                physicalPortfolioTradesList.append(portfolio)
            else:
                for physicalPortfolio in getAllPhysicalPortfoliosFromCompoundPortfolio(portfolio):
                    physicalPortfolioTradesList.append(physicalPortfolio)
        
        physicalValidPortfolioTradesList = []
        for portfolio in physicalPortfolioTradesList:
            if portfolio not in physicalExcludePortfolioTradesList:
                physicalValidPortfolioTradesList.append(portfolio)
                
        physicalValidPortfolioTradesListLength = len(physicalValidPortfolioTradesList)
        print physicalValidPortfolioTradesListLength
        if physicalValidPortfolioTradesListLength > 0:
            if portfolioIsEOD == 'Yes':
                portfolioIsEODFlag = '1'
                reqEventType = 'EOD_PORTFOLIO_TRADES'
            else:
                portfolioIsEODFlag = '0'
                reqEventType = 'INTRADAY_PORTFOLIO_TRADES'
            physicalPortfolioBatchId = '0'
            outgoingMessageObjectsPortfolioTrades = []
            outgoingMessageObjectsPortfolioTradesBatchStartList = []
            if physicalValidPortfolioTradesListLength > 1:
                physicalPortfolioBatchId = DATA_HELPER.RegisterBatch(portfolioReportDate, portfolioIsEODFlag, portfolioTopic, physicalValidPortfolioTradesListLength)
                if physicalPortfolioBatchId:
                    outgoingMessageObjectPortfolioTradesBatchStart = createOutgoingMessageObjectResponse('0', str(physicalPortfolioBatchId), \
                                                                                            portfolioIsEODFlag, portfolioReportDate, \
                                                                                            portfolioReportDateTime, reqEventType, '',\
                                                                                            __name__, 'PORTFOLIO_TRADES', acm.User().Name(), '', '',\
                                                                                            portfolioTopic, 'RESPONSE', 'BATCH_START',\
                                                                                            physicalValidPortfolioTradesListLength, 'EVENT_RESPONSE')
                    outgoingMessageObjectsPortfolioTradesBatchStartList.append(outgoingMessageObjectPortfolioTradesBatchStart)
                    outgoingMessageObjectsToAMBADataDictionariesPortfolioTradesBatchStart = mapOutgoingMessageObjectsToAMBADataDictionaries(outgoingMessageObjectsPortfolioTradesBatchStartList)
                    outgoingAMBAMessagesPortfolioTradesBatchStart = generateOutgoingAMBAMessages(outgoingMessageObjectsToAMBADataDictionariesPortfolioTradesBatchStart)
                    postOutgoingAMBAMessagesToAMB(outgoingAMBAMessagesPortfolioTradesBatchStart)
                    UTILS.Logger.flogger.info('Batch successfully registered. Corresponding BatchId : %i' %physicalPortfolioBatchId)
                else:
                    UTILS.Logger.flogger.info('Batch regestration error. Will continue to send requests for instrument trades. No Batch Id to subscribe on. Please use Topic if supplied.')
            
            for physicalPortfolioTrade in physicalValidPortfolioTradesList:
                outgoingMessageObjectPortfolioTrades = createOutgoingMessageObjectRequest('0', str(physicalPortfolioBatchId), portfolioIsEODFlag, portfolioReportDate,\
                                                portfolioReportDateTime, reqEventType, '', __name__, 'PORTFOLIO_TRADES', acm.User().Name(),\
                                                physicalPortfolioTrade.Name(), str(physicalPortfolioTrade.Oid()), portfolioTopic, 'REQUEST', 'REQT_PT')
                outgoingMessageObjectsPortfolioTrades.append(outgoingMessageObjectPortfolioTrades)
            outgoingMessageObjectsToAMBADataDictionariesPortfolioTrades = mapOutgoingMessageObjectsToAMBADataDictionaries(outgoingMessageObjectsPortfolioTrades)
            outgoingAMBAMessagesPortfolioTrades = generateOutgoingAMBAMessages(outgoingMessageObjectsToAMBADataDictionariesPortfolioTrades)
            postOutgoingAMBAMessagesToAMB(outgoingAMBAMessagesPortfolioTrades)
    except Exception, e:
        UTILS.ErrorHandler.processError(None, EXCEPTION('Could not process the Portfolio Trades GUI Request(s) in module %s.' %__name__,\
            traceback, 'CRITICAL', e))

    UTILS.Logger.flogger.info('STEP 4 - Complete at %s' %datetime.datetime.now())
    UTILS.Logger.flogger.info('-'*70)

    UTILS.Logger.flogger.info('STEP 5 - Starting Closing all AMB connections at %s' %datetime.datetime.now())
    
    try:
        for requestType in writerHandlerCollection.ambWriterHandlers.keys():
            writerHandlerCollection.ambWriterHandlers[requestType].ambWriter.close_AMB_Connection()
            UTILS.Logger.flogger.info('AMB Sender Connection to the AMB is now closed for writer posting Message Type %s.' %requestType)
    except Exception, e:
        UTILS.ErrorHandler.processError(None, EXCEPTION('Could not close all of the AMB connections in module %s.' %__name__,\
            traceback, 'CRITICAL', e))
    
    UTILS.Logger.flogger.info('STEP 5 - Complete at %s' %datetime.datetime.now())
    UTILS.Logger.flogger.info('-'*70)
