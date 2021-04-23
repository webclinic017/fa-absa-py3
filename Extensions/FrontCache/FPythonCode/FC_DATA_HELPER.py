
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_HELPER
PROJECT                 :       Front Cache
PURPOSE                 :       Data helper class for data operations
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX

Date            CR Number       Developer               Description
2019-07-18      XXXXXX          Sizwe Sokopo            Added UpdateRequestCollectionStart 
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant custom modules.
----------------------------------------------------------------------------------------------------------'''
import FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
import FC_DATA_BATCH_TRACK_REPOSITORY as fcDataBatchTrackerRepository
import FC_DATA_REQ_REPOSITORY as fcDataRequestRepository
import FC_DATA_REQ_TRACK_REPOSITORY as fcDataRequestTrackerRepository
import FC_DATA_REQ_COLL_TRK_REPOSITORY as fcDataRequestCollectionTrackerRepository
import FC_DATA_TRADE_REPOSITORY as fcDataTradeRepository
import FC_DATA_SETTLEMENT_REPOSITORY as fcDataSettlementRepository
import FC_DATA_TRANSACTIONOBJ_REPOSITORY as fcDataTransactionObjRepository
import FC_DATA_SEN_REPOSITORY as fcDataSensitivityRepository
import FC_DB_MSSQL_PROVIDER as fcDBMsSqlProvider
from FC_DATA_TRD_BUILDER import FC_DATA_TRD_BUILDER as fcDataTradeBuilder
from FC_DATA_STL_BUILDER import FC_DATA_STL_BUILDER as fcDataSettlementBuilder
from FC_DATA_SEN_BUILDER import FC_DATA_SEN_BUILDER as fcDataSensitivityBuilder
from FC_CALCULATION_SINGLETON import FC_CALCULATION_SINGLETON as fcCalculationSingleton
from FC_HEARTBEAT_PROCESS_REPOSITORY import FC_HEARTBEAT_PROCESS_REPOSITORY as HEARTBEAT_PROCESS_REPOSITORY
import FC_ENUMERATIONS
import FC_CallStatementServices
import FC_TermStatementServices
import threading
import ael
import acm
from decimal import *
import math
import xml.etree.ElementTree as etree
from datetime import datetime

#*********************************************************#
#Creating a SQL Data provider
#*********************************************************#
sqlDBProvider = None
def getSqlDBProvider():
    global sqlDBProvider
    try:
        dataSource= UTILS.Parameters.fcGenericParameters.DataSource
        initialCatalog= UTILS.Parameters.fcGenericParameters.InitialCatalog
        if not sqlDBProvider:
            sqlProvider = fcDBMsSqlProvider.FC_DB_MSSQL_PROVIDER(dataSource, initialCatalog)
        return sqlProvider
    except Exception, ex:
        raise Exception(UTILS.Constants.fcExceptionConstants.THE_SQL_DATA_PROVIDER_S % str(ex))
    

#***********************************************************************#
#Registering Batches
#*************************************************************************#
def RegisterBatch(reportDate, isEod, topic, expectedCount):
    try:
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        
        #Create the batchTracker repository
        batchTrackerRepository = fcDataBatchTrackerRepository.FC_DATA_BATCH_TRACK_REPOSITORY(dbProvider)
        
        #Create the bacth tracker and return the batch ID
        return batchTrackerRepository.create(reportDate, isEod, topic, expectedCount)
    except Exception, e:
        raise Exception((UTILS.Constants.fcExceptionConstants.REGISTER_THE_BATCH_S % str(e)))
        
#***********************************************************************#
#Requests
#*************************************************************************#
def RegisterRequest(requestMessage, recovery_mode):
    try:
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        
        #Create the request repository
        requestRepository = fcDataRequestRepository.FC_DATA_REQUEST_REPOSITORY(dbProvider)
        
        #Create the bacth tracker and return the batch ID
        return requestRepository.create(requestMessage, recovery_mode)
    except Exception, e:
        raise Exception(UTILS.Constants.fcExceptionConstants.REGISTER_THE_BATCH_S % str(e))

#***********************************************************************#
#Request Tracking
#*************************************************************************#
def SetRequestTrackerStart(requestId, expectedCount):
    try:
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        
        #Create the request tracker repository
        requestTrackerRepository = fcDataRequestTrackerRepository.FC_DATA_REQ_TRACK_REPOSITORY(dbProvider)
        
        #Update the request tracker with the expected count
        requestTrackerRepository.updateRequestTrackerStart(requestId, expectedCount)
        
    except Exception, e:
        raise Exception(UTILS.Constants.fcExceptionConstants.TRACKER_AS_STARTED_S % str(e))


#***********************************************************************#
#Request Collection Tracking
#*************************************************************************#
def UpdateRequestCollectionStart(requestId, startIndex):
    try:
        dbProvider = getSqlDBProvider()
        
        requestCollectionTrackerRepository = fcDataRequestCollectionTrackerRepository.FC_DATA_REQ_COLL_TRK_REPOSITORY(dbProvider)
        
        requestCollectionTrackerRepository.updateRequestCollectionTrackerStart(requestId, startIndex)
        
    except Exception, e:
        raise Exception(UTILS.Constants.fcExceptionConstants.COLLECTION_TRACKER_S % str(e))
        
def GetIndependentTradeCount(reportDate, bookName):
    try:
        dbProvider = getSqlDBProvider()
        requestRepository = fcDataRequestRepository.FC_DATA_REQUEST_REPOSITORY(dbProvider)
        return requestRepository.getIndependentTradeCount(reportDate, bookName)
    except Exception, e:
        raise Exception('GetIndependentTradeCount failed. %s' % str(e))

def RecordFailedSelection(reportDate, bookName, requestMessage):
    try:
        dbProvider = getSqlDBProvider()
        requestRepository = fcDataRequestRepository.FC_DATA_REQUEST_REPOSITORY(dbProvider)
        return requestRepository.recordFailedSelection(reportDate, bookName, requestMessage)
    except Exception, e:
        raise Exception('RecordFailedSelection failed. %s' % str(e))

def SetRequestTrackerEnd(requestId, processedCount, errorCount, requestCollectionTrackerId, batchId, errorTradeNumbers):
    try:
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        errorTrades = ','.join(str(x) for x in errorTradeNumbers)
        if errorTrades == '':
            errorTrades = None
        batchTrackerRepository = fcDataBatchTrackerRepository.FC_DATA_BATCH_TRACK_REPOSITORY(dbProvider)
        return batchTrackerRepository.updateBatchRequestEnd(requestId, processedCount, errorCount,
                                                            requestCollectionTrackerId, batchId, errorTrades)
        
    except Exception, e:
        raise Exception(UTILS.Constants.fcExceptionConstants.TRACKER_AS_COMPLETED_S % str(e))


def SendConfirmation(requestId):
    try:
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        
        requestTrackerRepository = fcDataRequestTrackerRepository.FC_DATA_REQ_TRACK_REPOSITORY(dbProvider)
        
        #Create request tracker with the expected count
        return requestTrackerRepository.SendConfirmationOfEndMessage(requestId)
        
    except Exception, e:
        raise Exception(UTILS.Constants.fcExceptionConstants.CONFIRMATION_FAILED % str(e))
	
	
def CheckChunkHasCompleted(requestCollectionTrackerId):
    try:
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        
        requestTrackerRepository = fcDataRequestTrackerRepository.FC_DATA_REQ_TRACK_REPOSITORY(dbProvider)
        
        #Create request tracker with the expected count
        return requestTrackerRepository.CheckChunkHasCompleted(requestCollectionTrackerId)
        
    except Exception, e:
        raise Exception('Chunk checking failed %s' % str(e))

def GetLastProcessedMessageInfo(serviceComponentId):
    try:
        dbProvider = getSqlDBProvider()
        result = dbProvider.executeNoParams("SELECT MessageId,RequestId,RetryCount FROM FrontCache.ServiceComponentMessageTracker WHERE [ServiceComponentId] = %s" %serviceComponentId)
        if len(result) > 0:
            return result[0][0], result[0][1], int(result[0][2])
        return None, None, None
    except Exception, e:
        raise Exception('Last processed message retrieval failed with reason %s' % str(e))


def RegisterMessageId(serviceComponentId, messageId, requestId, retryCount = 0):
    try:
        dbProvider = getSqlDBProvider()
        dbProvider.executeNoParamsNoReturn("UPDATE FrontCache.ServiceComponentMessageTracker SET MessageId = %s, RequestId = %s, RetryCount = %s WHERE [ServiceComponentId] = '%s' " %(messageId, requestId, retryCount, serviceComponentId))
    except Exception, e:
        raise Exception('Failed to register messageId with reason %s' % str(e))


def ResetRegisterMessageIdRequestId(serviceComponentId):
    try:
        dbProvider = getSqlDBProvider()
        dbProvider.executeNoParamsNoReturn("UPDATE FrontCache.ServiceComponentMessageTracker SET MessageId = NULL, RequestId = NULL, RetryCount = 0 WHERE [ServiceComponentId] = '%s' " % serviceComponentId)
    except Exception, e:
        raise Exception('Failed to reset messageId and requestid with reason %s' % str(e))

#***********************************************************************#
#Building and saving trades
#*************************************************************************#
#Constructs a single trade object based on the options provided
def BuildTrade(reportDate, tradeNumber, buildOptions):
    
    
    tradeBuilder = fcDataTradeBuilder(tradeNumber)
    if bool(buildOptions.BuildTradeStatic):
        tradeBuilder = tradeBuilder.CreateStatic()
    if bool(buildOptions.BuildTradeScalar):
        tradeBuilder = tradeBuilder.CreateScalar()
    if bool(buildOptions.BuildTradeInstrument):
        tradeBuilder = tradeBuilder.CreateInstrument()
    if bool(buildOptions.BuildTradeLegs):
        tradeBuilder = tradeBuilder.CreateLegs()
    if bool(buildOptions.BuildUnderlyingInstruments):
        tradeBuilder = tradeBuilder.CreateUnderlyingInstruments()
    if bool(buildOptions.BuildUnderlyingKeys):
        tradeBuilder = tradeBuilder.CreateUnderlyingKeys()
    if bool(buildOptions.BuildMoneyflows):
        tradeBuilder = tradeBuilder.CreateMoneyflows(reportDate, buildOptions.HistoricalCashflowRange)
    if bool(buildOptions.BuildSalesCredits):
        tradeBuilder = tradeBuilder.CreateSalesCredits()
    #Done building, now calculate
    trade = tradeBuilder.CalculateAndBuild()
    trade.SerializationType = buildOptions.SerializationType
    trade.Serialize()
    return trade
    
#***********************************************************************#
#Building and saving settlements
#*************************************************************************#
#Constructs a single settlement object based on the options provided
def BuildSettlement(reportDate, settlementNumber, buildOptions):
    settlementBuilder = fcDataSettlementBuilder(settlementNumber)
    if bool(buildOptions.BuildSettlementData):
        settlementBuilder = settlementBuilder.CreateData()
    #Done building, now calculate
    settlement = settlementBuilder.CalculateAndBuild()
    settlement.SerializationType = buildOptions.SerializationType
    settlement.Serialize()
    return settlement


def BuildCallTx(requestId, reportDate, instrumentName, buildOptions):
    instrument = acm.FInstrument[instrumentName]
    if instrument is None:
        # this is to cater for the trade update to the call account instrument.
        instrument = acm.FTrade[instrumentName].Instrument()
    statement_date = str(datetime.strptime(FC_UTILS.dateTimeStringFromISODateTimeString(reportDate), '%Y-%m-%d %H:%M:%S').date())
    #to_date = acm.Time.DateToday()
    for trade in instrument.Trades().AsArray():
        if FC_CallStatementServices.is_eligible_for_statement(trade):
            statement_xml = FC_CallStatementServices.generate_statement_xml(trade, statement_date, statement_date)
            UTILS.Logger.flogger.info('Generated statement (%s)' % statement_xml)
            data = etree.XML(statement_xml)
            reportDate = etree.SubElement(data, 'REPORT_DATE')
            reportDate.text = statement_date
            requestid = etree.SubElement(data, "REQUEST_ID")
            requestid.text = str(requestId)
            root = etree.Element('TransactionalData')
            root.text = FC_UTILS.deflate_and_base64_encode(etree.tostring(data))
            return  etree.tostring(root)
            #return FC_UTILS.deflate_and_base64_encode(etree.tostring(data))

def BuildTermTx(requestId, reportDate, tradeNumber, buildOptions):
    acquirer = acm.FParty['Funding Desk']
    counterparty = acm.FTrade[tradeNumber].Counterparty()

    statement_date = str(datetime.strptime(FC_UTILS.dateTimeStringFromISODateTimeString(reportDate), '%Y-%m-%d %H:%M:%S').date())
    statement_xml = FC_TermStatementServices.generate_statement_xml(acquirer, counterparty, statement_date, statement_date)
    UTILS.Logger.flogger.info('Generated statement (%s)' %statement_xml)
    data = etree.XML(statement_xml)
    reportDate = etree.SubElement(data, 'REPORT_DATE')
    reportDate.text = statement_date
    requestid = etree.SubElement(data, "REQUEST_ID")
    requestid.text = str(requestId)
    root = etree.Element('TransactionalData')
    root.text = FC_UTILS.deflate_and_base64_encode(etree.tostring(data))
    return etree.tostring(root)
    #return FC_UTILS.deflate_and_base64_encode(etree.tostring(data))

def BuildObject(reportDate, objectNumber, buildOptions, sensType, portfolioName=None, portfolioNumber=None):
    if(UTILS.Constants.fcGenericConstants.ZAR_SWAP_CURVE_CALIBRATION_BOOKS.__contains__(objectNumber)):
        portfolio = acm.FPhysicalPortfolio[objectNumber]
        if(portfolio.MemberLinks()):
            if(portfolio.MemberLinks().First()):
                parentPrf = portfolio.MemberLinks().First().OwnerPortfolio()
                objectBuilder = fcDataSensitivityBuilder(parentPrf.Oid(), sensType, portfolioName, portfolioNumber)
                if bool(buildOptions.BuildSensitivityData):
                    objectBuilder = objectBuilder.CreateSensitivityCalc()
                object = objectBuilder.CalculateAndBuild()
    objectBuilder = fcDataSensitivityBuilder(objectNumber, sensType, portfolioName, portfolioNumber)
    if bool(buildOptions.BuildSensitivityData):
        objectBuilder = objectBuilder.CreateSensitivityCalc()
    object = objectBuilder.CalculateAndBuild()
    object.SerializationType = buildOptions.SerializationType
    object.Serialize()
    return object

def is_number(s):
    try:
        if s == '':
            s = 0
        val = Decimal(s)
        if math.isnan(val):
            return None, False
        return val, True
    except ValueError:        
        return None, False
    except InvalidOperation:
        return None, False
    
def formatControlMeasureResults(container):
    for item in container:
        container[item] = FC_UTILS.formatCMNumber(str(container[item]))

def getInvalidTradePortfolioCounts(reportDate, batchId):
    dbProvider = getSqlDBProvider()
    tradeRepository = fcDataTradeRepository.FC_DATA_TRADE_REPOSITORY(dbProvider)
    return tradeRepository.getInvalidTradePortfolioCounts(reportDate, batchId)

def BuildAndSaveTrades(requestId, reportDate, startIndex, tradeNumbers, buildOptions, retryCount=0):
    try:
        trades = []
        tradeIds = {}
        errors = {}
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        tradeRepository = fcDataTradeRepository.FC_DATA_TRADE_REPOSITORY(dbProvider)

        #Apply Global Simulation on Trading Manager
        dateFormatForReportDate = FC_UTILS.dateStringFromISODateTimeString(reportDate)
        
        if reportDate and ael.date(dateFormatForReportDate) < ael.date_today():
            fcCalculationSingleton.Instance().ApplyGlobalSimulation(None, dateFormatForReportDate, None)
        
        controlMeasures = {}
        controlMeasureErrors = []
        for item in UTILS.Parameters.fcGenericParameters.ControlMeasureColumnsList:
            controlMeasures[item] = ''
        createControlMeasures = str(buildOptions.BuildControlMeasures) == 'True'
        UTILS.ControlMeasureResults = None

        #payloadDict = []
        #connection = FC_UTILS.createRedisConnection()
        
        for tradeNumber in tradeNumbers:
            tradeId = 0
            #try building the trade object
            try:
                trade = BuildTrade(reportDate, tradeNumber, buildOptions)
                #Sum control measure values per chunk                                
                if createControlMeasures:
                    controlMeasureContainer = fcCalculationSingleton.Instance().GetControlMeasureContainer()
                    for controlValue in controlMeasureContainer:    
                        (val, isNumber) = is_number(controlMeasureContainer[controlValue])                    
                        if isNumber is True:
                            if controlMeasures[controlValue] == '': controlMeasures[controlValue] = val
                            else: controlMeasures[controlValue] += val
                        else: controlMeasureErrors.append(controlValue)
                    
                fcCalculationSingleton.Instance().ResetControlMeasureContainer()
                trades.append(trade)
                
                #FC_UTILS.postEvent(str(requestId) + '_' + str(startIndex),payloadDict,connection,'TradeMetric')
                #payloadDict = []
                
                #Set all trade id's to 0, cannot get back on bulk...ugly, but assuming all trades will succeed!
                tradeIds[tradeNumber] = tradeId
            except Exception, e:
                fcCalculationSingleton.Instance().ResetControlMeasureContainer()
                errors[tradeNumber] = str(e)
                if retryCount + 1 <= UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
                    return tradeIds, errors
                UTILS.Logger.flogger.info('ATS unable to resolve issues with (%s) retries.' % (retryCount))

        if createControlMeasures is True:
            UTILS.ControlMeasureResults = FC_UTILS.CreateControlMeasuresParameter(requestId, controlMeasures, controlMeasureErrors)
                
        #Now try the bulk commmit
        try:
            if len(trades)>0:
                tradeRepository.createTvp(requestId, reportDate, startIndex, trades, UTILS.ControlMeasureResults)
        except Exception, e:
            print 'Create many failed', str(e)
            #try committing one by one
            indexCount = startIndex
            for trade in trades:
                try:
                    tradeId = tradeRepository.create(requestId, reportDate, indexCount, trade)
                    tradeIds[trade.Static.FTrade.Oid()]=tradeId
                except Exception, e:
                    errors[trade.Static.FTrade.Oid()] = str(e)
                indexCount = indexCount + 1
        return tradeIds, errors  
            
        
        #Remove Global Simulations
        if reportDate and ael.date(dateFormatForReportDate) < ael.date_today():
            fcCalculationSingleton.Instance().RemoveGlobalSimulation()
        
        return tradeIds, errors  
    except Exception, e:
        raise Exception(UTILS.Constants.fcExceptionConstants.SAVE_THE_TRADES_S % str(e))

def BuildAndSaveSettlements(requestId, reportDate, startIndex, settlementNumbers, buildOptions, retryCount=0):
    try:        
        settlementIds = {}
        errors = {}
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        settlementRepository = fcDataSettlementRepository.FC_DATA_SETTLEMENT_REPOSITORY(dbProvider)
        indexCount = startIndex

        payloadDict = []
        #connection = FC_UTILS.createRedisConnection()
        for settlementNumber in settlementNumbers:
            payloadDict = []
            settlementId = 0
            try:
                settlement = BuildSettlement(reportDate, settlementNumber, buildOptions)
                settlementId = settlementRepository.create(requestId, reportDate, indexCount, settlement)
                settlementIds[settlementNumber]=settlementId
                indexCount = indexCount + 1
            except Exception, e:
                errors[settlementNumber] = str(e)
                
            #FC_UTILS.postEvent(str(requestId) + '_' + str(startIndex),payloadDict,connection,'STLMetric')
            #fcCalculationSingleton.Instance().clearAllCalcSpaces()
        return settlementIds, errors  
    except Exception, e:
        raise Exception(UTILS.Constants.fcExceptionConstants.SAVE_THE_SETTLEMENTS_S % str(e))

def BuildAndSaveCallTx(requestId, reportDate, startIndex, callAccountNumber, tradeNumbers, buildOptions, retryCount=0):
    try:
        transactionIds = {}
        errors = {}
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        transactionObjRepository = fcDataTransactionObjRepository.FC_DATA_TRANSACTIONOBJ_REPOSITORY(dbProvider)
        indexCount = startIndex
        transactionId = 0
        try:
            transactionObj = BuildCallTx(requestId, reportDate, callAccountNumber, buildOptions)
            transactionId = transactionObjRepository.create(requestId, reportDate, indexCount, transactionObj, 'Call')
            transactionIds[callAccountNumber]=transactionId
            indexCount = indexCount + 1
        except Exception, e:
            UTILS.Logger.flogger.info('Error (%s)' % str(e))
            errors[callAccountNumber] = str(e)
        #fcCalculationSingleton.Instance().clearAllCalcSpaces()
        return transactionIds, errors
    except Exception, e:
        raise Exception('Could not build and save the call transaction. %s' % str(e))

def BuildAndSaveTermTx(requestId, reportDate, startIndex,scopeName, tradeNumbers, buildOptions, retryCount=0):
    try:
        transactionIds = {}
        errors = {}
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        transactionObjRepository = fcDataTransactionObjRepository.FC_DATA_TRANSACTIONOBJ_REPOSITORY(dbProvider)
        indexCount = startIndex
        for tradeNumber in tradeNumbers:
            transactionId = 0
            try:
                transactionObj = BuildTermTx(requestId, reportDate, tradeNumber, buildOptions)
                transactionId = transactionObjRepository.create(requestId, reportDate, indexCount, transactionObj, 'Term')
                transactionIds[tradeNumber]=transactionId
                indexCount = indexCount + 1
            except Exception, e:
                UTILS.Logger.flogger.info('Error (%s)' % str(e))
                errors[tradeNumber] = str(e)
            #fcCalculationSingleton.Instance().clearAllCalcSpaces()
        return transactionIds, errors
    except Exception, e:
        raise Exception('Could not build and save the term transaction. %s' % str(e))

def BuildAndSaveSensitivities(requestId, reportDate, startIndex, objectNumbers, buildOptions, sensType,
                              portfolioName=None, portfolioNumber=None):
    try:        
        objectIds = {}
        errors = {}
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        objectRepository = fcDataSensitivityRepository.FC_DATA_SEN_REPOSITORY(dbProvider)
        indexCount = startIndex

        controlMeasures = {}
        controlMeasureErrors = []

        if objectNumbers is not None:
            #for objectNumber in objectNumbers:
            objectId = 0
            try:
                payloadDict = []
                #connection = FC_UTILS.createRedisConnection()
                object = BuildObject(reportDate, objectNumbers, buildOptions, sensType, portfolioName, portfolioNumber)
                #FC_UTILS.postEvent(str(requestId) + '_' + str(startIndex),payloadDict,connection,'SensMetric')
                
                controlMeasureResult = None
                columnName = 'absSum'
                for kvp in object.SensitivityWorkbook.CalculationResults:
                    value = object.SensitivityWorkbook.CalculationResults[kvp]
                    (val, isNumber) = is_number(str(value))
                    if isNumber is True:
                        if val < 0:
                            val = val * -1

                        if columnName in controlMeasures:
                            controlMeasures[columnName] += val
                        else:
                            controlMeasures[columnName] = val

                #controlMeasureResult = FC_UTILS.CreateControlMeasuresParameter(requestId, controlMeasures, controlMeasureErrors)

                objectId = objectRepository.create(requestId, reportDate, indexCount, object)
                objectIds[objectNumbers] = objectId
                indexCount = indexCount + 1
            except Exception, e:
                errors[objectNumbers] = str(e)
        return objectIds, errors
    except Exception, e:
        raise Exception(UTILS.Constants.fcExceptionConstants.SAVE_THE_SETTLEMENTS_S % str(e))

#Delete the Process Heart Beat from the DB
def DeleteHeartBeatProcess():
    try:
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        heartBeatProcessRepository = HEARTBEAT_PROCESS_REPOSITORY(dbProvider)
        heartBeatProcessRepository.delete()
    except Exception, e:
        raise Exception('Could not delete the process heart beat for component %s in module %s. ERROR: %s' %(UTILS.ComponentName, __name__, str(e)))
    
#Insert or Update a Heart Beat
def ReportHeartBeatProcess(reportDate, heartBeatInfoProcess):
    try:
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        heartBeatProcessRepository = HEARTBEAT_PROCESS_REPOSITORY(dbProvider)
        heartBeatProcessRepository.create(heartBeatInfoProcess)
    except Exception, e:
        raise Exception('Could not report the process heart beat for component %s in module %s. ERROR: %s' %(UTILS.ComponentName, __name__, str(e)))
    
#Retreiving the next available ATS
def GetHeartbeatCandidateComponent(expectedRequestType, processedCount, isRT):
    try:
        #fetch the SQL data provider
        dbProvider = getSqlDBProvider()
        heartBeatProcessRepository = HEARTBEAT_PROCESS_REPOSITORY(dbProvider)
        #print 'Expected Request Type : %s' %expectedRequestType
        serviceComponentId = heartBeatProcessRepository.getCandidateComponent(expectedRequestType, isRT)
        #print 'Candicate Component Name : %s' %candidateComponentName
        if serviceComponentId:
            try:
                UpdateComponentQueueDepth(FC_ENUMERATIONS.ServiceComponent.tostring(serviceComponentId), processedCount)
            except Exception, e:
                raise Exception('Could not increment the queue depth of the candidate component for component %s in module %s. ERROR: %s' %(UTILS.ComponentName, __name__, str(e)))
        return FC_ENUMERATIONS.ServiceComponent.tostring(serviceComponentId)
    except Exception, e:
        raise Exception('Could not get a candidate component for component %s in module %s. ERROR: %s' %(UTILS.ComponentName, __name__, str(e)))

''' Obsolete
def UpdateHeartbeatCandidateComponent(targetComponentName):
    try:
        dbProvider = getSqlDBProvider()
        heartBeatProcessRepository = HEARTBEAT_PROCESS_REPOSITORY(dbProvider)
        heartBeatProcessRepository.incrementComponet(targetComponentName)
    except Exception, e:
        raise Exception('Could not update candidate component for component %s in module %s. ERROR: %s' %(UTILS.ComponentName, __name__, str(e)))'''

def CheckIfTradesExistForRequestId(requestId, tradeNumbers, reportDate):
    try:
        tradeNumbers = ','.join(str(oid) for oid in tradeNumbers)
        sql = """
            SELECT 1 FROM FRONTCACHE.TRADE WHERE REQUESTID = %s AND ReportDate = '%s' AND TRADENUMBER IN (%s)
        """ % (requestId, reportDate, tradeNumbers)
        #print sql
        dbProvider = getSqlDBProvider()
        result = dbProvider.executeNoParamsScalar(sql)

        if result and len(result)==1:
            UTILS.Logger.flogger.info("Found existing tradenumbers %s for requestId %s" % (tradeNumbers, requestId))
            return True
        return False
    except Exception, e:
        raise Exception('CheckIfTradesExistForRequestId failed %s' % str(e))

def CheckIfSensitivityExistForRequestId(requestId, scopename, reportDate):
    try:
        sql = """
            SELECT 1 from frontcache.Sensitivity WHERE REQUESTID = %s AND ReportDate = '%s' AND ScopeName = '%s'
        """ % (requestId, reportDate, scopename)
        #print sql
        dbProvider = getSqlDBProvider()
        result = dbProvider.executeNoParamsScalar(sql)

        if result and len(result)==1:
            UTILS.Logger.flogger.info("Found existing sensitivity %s for requestId %s" % (scopename, requestId))
            return True
        return False
    except Exception, e:
        raise Exception('CheckIfTradesExistForRequestId failed %s' % str(e))

def GetProcessedCountForRequestCollectionTrackerId(requestCollectionTrackerId):
    try:
        sql = """
            SELECT ProcessedCount
            FROM FrontCache.RequestCollectionTracker
            WHERE RequestCollectionTrackerId = %s
        """ % requestCollectionTrackerId
        dbProvider = getSqlDBProvider()
        result = dbProvider.executeNoParamsScalar(sql)
        if result and len(result)==1:
            return int(result[0])
        return 0
    except Exception, e:
        raise Exception('GetProcessedCountForRequestCollectionTrackerId failed %s' % str(e))

def UpdateComponentQueueDepth(componentName, processedCount):
    try:
        dbProvider = getSqlDBProvider()
        serviceComponentId = FC_ENUMERATIONS.ServiceComponent.fromstring(componentName)
        from FC_HEARTBEAT_PROCESS_REPOSITORY import FC_HEARTBEAT_PROCESS_REPOSITORY as HEARTBEAT_PROCESS_REPOSITORY
        heartBeatProcessRepository = HEARTBEAT_PROCESS_REPOSITORY(dbProvider)
        heartBeatProcessRepository.updateComponentQueue(serviceComponentId, processedCount)
        
    except Exception, e:
        raise Exception('Update component queue depth failed %s' % str(e))        

