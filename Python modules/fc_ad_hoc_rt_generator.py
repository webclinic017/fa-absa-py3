import FC_ERROR_HANDLER_DEFAULT as ERROR_HANDLER_DEFAULT
import acm, ael, datetime, traceback, locale, re, at, at_time, amb
from AMBA_Helper_Functions import AMBA_Helper_Functions as AMBA_Helpers
from FC_PARAMETERS_COMPONENT import FC_PARAMETERS_COMPONENT as PARAMETERS_COMPONENT
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
    UTILS.Initialize('FC_RT_01_ATS')
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

def postAMBAMessageToAMB(AMBAMessage, requestType, senderSubject):
    global writerHandlerCollection
    writerHandlerCollection.ambWriterHandlers['REQUEST'].ambWriter.post_Message_To_AMB_With_Subject(AMBAMessage, senderSubject)

def postOutgoingAMBAMessagesToAMB(outgoingAMBAMessages):
    for outgoingAMBAMessage in outgoingAMBAMessages:
            postAMBAMessageToAMB(outgoingAMBAMessage[1], outgoingAMBAMessage[0], outgoingAMBAMessage[2])

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

dateDisplayList = ['{TODAY:%Y-%m-%d}', '{YESTERDAY:%Y-%m-%d}', '{PREVBD:%Y-%m-%d}']
eventDisplayList = ['UPDATE', 'DELETE', 'INSERT']
receiverDisplayList = ['U_FC_TRD_01_AMBA/TRADE', 'D_FC_TRD_01_AMBA/TRADE']

ael_variables = [                                    
                    ['portfolioList', 'Portfolios_Portfolios Trades Request', acm.FPhysicalPortfolio, '', 'PB_PSWAP_CORO_CFS_CR', 0, 1, 'PORTFOLIO_TRADES requests will be send for the portfolios selected.', None, 1],
                    ['portfolioReportDate', 'Portfolio Report Date_Portfolios Trades Request', 'string', dateDisplayList, '{TODAY:%Y-%m-%d}', 1, 0, 'Report date for the PORTFOLIO_TRADES requests will be send.', None, 1],
                    #['portfolioIsEOD', 'Official EOD Run_Portfolios Trades Request', 'string', boolEODDictDisplay, 'No', 1, 0, 'The Request will be flagged as the official EOD Batch.', setPortfolioIsEODValues, 1],
                    ['portfolioTree', 'On/Off Tree_Portfolios Trades Request', 'string', onOffTreeList, '', 0, 0, 'ON TREE will send PORTFOLIO_TRADES requests for all physical portfolios under %s. OFF TREE will send PORTFOLIO_TRADES requests for all physical portfolios NOT under %s.' %(ON_TREE_COMPOUND_PORTFOLIO, ON_TREE_COMPOUND_PORTFOLIO), setPortfolioTreeOnTreeOffTreeValues, 0],
                    #['portfolioTopic', 'Topic_Portfolios Trades Request', 'string', None, 'INTRADAY_PORTFOLIO_TRADES_REQUEST', 0, 0, 'Topic on which the requester can subscribe to get the result from this request.', None, 1],
                    ['portfolioReceiver', 'Portfolio Receiver_Portfolios Trades Request', 'string', receiverDisplayList, 'D_FC_TRD_01_AMBA/TRADE', 1, 0, 'Receiver for the PORTFOLIO_TRADES requests messages.', None, 1],
                    ['portfolioEventType', 'Portfolio Event Type_Portfolios Trades Request', 'string', eventDisplayList, 'UPDATE', 1, 0, 'Event Type for the PORTFOLIO_TRADES requests will be send.', None, 1],
                ]

def ael_main(dict):
    global writerHandlerCollection
    
    UTILS.Logger.flogger.info('-'*70)
    UTILS.Logger.flogger.info('Starting %s at %s' %(__name__, datetime.datetime.now()))
    UTILS.Logger.flogger.info('-'*70)
    
    portfolioList = dict['portfolioList']
    portfolioReportDate = demacroize(dict['portfolioReportDate'])
    portfolioReportDateTime = '%s 00:00:00' %portfolioReportDate
    #portfolioIsEOD = dict['portfolioIsEOD']
    portfolioTree = dict['portfolioTree']
    #portfolioTopic = dict['portfolioTopic']
    receiver = dict['portfolioReceiver']
    eventType = dict['portfolioEventType']


    print 'RECEIVER', receiver
    print 'Type', eventType
    
    #portfolioExcludePortfolioList = dict['portfolioExcludePortfolioList']   
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
    
    
    UTILS.Logger.flogger.info('STEP 4 - Starting PORTFOLIO_TRADES Requests at %s' %datetime.datetime.now())
    
    try:
        '''physicalExcludePortfolioTradesList = []
        for excludePortfolio in portfolioExcludePortfolioList:
            if isPhysicalPortfolio(excludePortfolio):
                physicalExcludePortfolioTradesList.append(excludePortfolio)
            else:
                for physicalExcludePortfolio in getAllPhysicalPortfoliosFromCompoundPortfolio(excludePortfolio):
                    physicalExcludePortfolioTradesList.append(physicalExcludePortfolio)'''
        
        physicalPortfolioTradesList = []
        for portfolio in portfolioList:
            sql = r'''SELECT t.trdnbr
                                            from
                                            Trade t
                                            WHERE t.prfnbr = %s
                                ''' %portfolio.Oid()

            dataSelection = ael.asql(sql)

            dataSelection.sort()
            msgs = {}

            for trd in dataSelection[0][0]:    
                message = '''[MESSAGE]
                                TYPE='''+ '%s_TRADE' %eventType + '''
                                VERSION=1.0
                                TIME='''+ portfolioReportDateTime + '''
                                SOURCE=FC_AD_HOC_RT_GENERATOR
                                TXNBR=1057828663
                                [TRADE]
                                    UPDAT_TIME='''+ portfolioReportDateTime + '''
                                    UPDAT_USRNBR=130
                                    UPDAT_USRNBR.USERID=SIMULATED_EVENT                                
                                    TRDNBR=''' + str(trd[0]) + '''
                                [/TRADE]
                              [/MESSAGE]'''
                msgs[trd] = message
                
        outgoingAMBAMessages = []
        
        for x in msgs:
            msgString = msgs[x]            
            try:
                strippedMsgString = msgString.lstrip().rstrip()
            except Exception, e:
                UTILS.ErrorHandler.processError(None, EXCEPTION('Could not remove the white spaces pre and post the message %s in module %s.' %(msgString, __name__),\
                traceback, 'CRITICAL', e))
                continue
            
            try:
                buffer = amb.mbf_create_buffer_from_data(strippedMsgString)
            except Exception, e:
                UTILS.ErrorHandler.processError(None, EXCEPTION('Could not create a mbf buffer for message %s in module %s.' %(msgString, __name__),\
                traceback, 'CRITICAL', e))
                continue
            
            try:
                msg = buffer.mbf_read()
            except Exception, e:
                UTILS.ErrorHandler.processError(None, EXCEPTION('Could not read the AMB object for message %s in module %s.' %(msgString, __name__),\
                traceback, 'CRITICAL', e))
                continue
            
            try:
                messageType = AMBA_Helpers.get_AMBA_Object_Value(msg, 'TYPE')
            except Exception, e:
                UTILS.ErrorHandler.processError(None, EXCEPTION('Could not retreive the TYPE attribute from the message %s in module %s.' %(msgString, __name__),\
                traceback, 'CRITICAL', e))
                continue
            
            try:
                subjects = PARAMETERS_COMPONENT('FC_RT_01_ATS').componentSubscriptionSubjects
            except Exception, e:
                UTILS.ErrorHandler.processError(None, EXCEPTION('Could not retreive the subjects from the component config %s in module %s.' %('FC_RT_01_ATS', __name__),\
                traceback, 'CRITICAL', e))
                continue
            
            if len(subjects) == 1:
                subject = subjects[0]
            
            
            outgoingAMBAMessages.append((messageType, msg, receiver))
        
        postOutgoingAMBAMessagesToAMB(outgoingAMBAMessages)
            
        try:
            for requestType in writerHandlerCollection.ambWriterHandlers.keys():
                writerHandlerCollection.ambWriterHandlers[requestType].ambWriter.close_AMB_Connection()
                UTILS.Logger.flogger.info('AMB Sender Connection to the AMB is now closed for writer posting Message Type %s.' %requestType)
        except Exception, e:
            UTILS.ErrorHandler.processError(None, EXCEPTION('Could not close all of the AMB connections in module %s.' %__name__,\
                traceback, 'CRITICAL', e))        
                
          
    except Exception, e:
        print str(e)




