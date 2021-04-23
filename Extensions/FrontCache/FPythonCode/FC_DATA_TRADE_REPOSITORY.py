
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_TRADE_REPOSITORY
PROJECT                 :       Front Cache
PURPOSE                 :       This repository for trade database operations
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
from FC_DATA_BASE_REPOSITORY import FC_DATA_BASE_REPOSITORY as fcDataBaseRepository
import FC_UTILS
from FC_UTILS import FC_UTILS as UTILS

class FC_DATA_TRADE_REPOSITORY(fcDataBaseRepository):
    createSql = UTILS.Constants.fcGenericConstants.FRONTCACHE_CREATE_TRADE_ENTITY
    createSqlCollection = UTILS.Constants.fcGenericConstants.FRONTCACHE_CREATE_TRADE_ENTITIES_COLLECTION
    portfolioCountSql = '''
     SELECT BookId
     FROM FrontCache.PortfolioTradeCount
     WHERE CONVERT(date, dbtimestamp) = '%s' and HasFailedValidation = 1 and
     Bookid in (SELECT ScopeNumber from FrontCache.Request WHERE BatchId = %s)
    '''
    enumDict = {}
    #Constructor
    def __init__(self, dbProvider):
        fcDataBaseRepository.__init__(self, dbProvider)      
    
    #Methods
    #Creates a trade static database row as part of a transaction (commit needs to be called on the dbProvider)
    def create(self, requestId, reportDate, tradeIndex, trade):
        sqlParams=self.createSqlParams(requestId, reportDate, tradeIndex, trade)
        
        #Test sql params
        if not sqlParams or len(sqlParams)==0:
            raise Exception(UTILS.Constants.fcExceptionConstants.CREATE_SQL_PARAMETERS)
        #Commit and get the trade id saved
        result = self.dbProvider.executeScalar(self.createSql, sqlParams)
        if not result and len(result)!=1:
            raise Exception(UTILS.Constants.fcExceptionConstants.CREATE_THE_TRADE)
        return result[0]

    #Creates trade database rows and do the insert in bulk
    def createMany(self, requestId, reportDate, startIndex, trades):
        sqlParams = []
        tradeIndex = startIndex
        for trade in trades:            
            tradeSqlParams = self.createSqlParams(requestId, reportDate, tradeIndex, trade)
            sqlParams.append(tradeSqlParams)
            tradeIndex = tradeIndex + 1
        
        
        #Commit all the trades
        self.dbProvider.executeMany(self.createSql, sqlParams)

    #Creates trade database rows and do the insert in bulk
    def createTvp(self, requestId, reportDate, startIndex, trades, cmParms):
        sqlParams = []
        tradeIndex = startIndex
        for trade in trades:        
            tradeSqlParams = self.createSqlParams(requestId, reportDate, startIndex, trade)
            sqlParams.append(tradeSqlParams)
            tradeIndex = tradeIndex + 1            
                
        #Commit all the trades
        self.dbProvider.executeTvp(self.createSqlCollection, sqlParams, cmParms)


    def createSqlParams(self, requestId, reportDate, tradeIndex, trade):
        
        #Basic Validation on the trade static contained before we persist
        f_trade = trade.Static.FTrade
        if not f_trade:
            raise Exception(UTILS.Constants.fcExceptionConstants.TRD_STATIC_CONTAINS_NO_VALID_FTRADE_INSTANCE)
        elif not trade.SerializedData:
            raise Exception(UTILS.Constants.fcExceptionConstants.TRD_STATIC_CONTAINER_NO_SERIALIZED_DATA)


        #Fetch (and format) some meta data of the FTrade instance
        #This is the official mapping to the database table
        #tradeNumber
        tradeNumber = f_trade.Oid()

        #connectedTradeNumber
        connectedTradeNumber=0
        connected_trade = f_trade.ConnectedTrade()
        if connected_trade:
            connectedTradeNumber = connected_trade.Oid()

        #externalId (optional Key)
        externalId = f_trade.OptionalKey()

        #portfolioNumber
        portfolioNumber=0
        if f_trade.Portfolio():
            portfolioNumber = f_trade.Portfolio().Oid()

        #instrument, underlying and derived values based on instrument type
        bookCode = 0
        bookName = None            
        instrumentType = None
        instrumentName = None
        instrumentNumber = 0
        underlyingInstrumentType = None

        f_trade_instrument = f_trade.Instrument()
        f_trade_acquirer = f_trade.Acquirer()
        if f_trade_instrument:
            #instrument type
            instrumentType = FC_UTILS.getEnum('InsType', f_trade_instrument.InsType())

            #instrument name
            try:
                instrumentName = unicode(f_trade_instrument.Name())
            except UnicodeDecodeError, e:
                UTILS.Logger.flogger.info('Failed to decode instrument name')
                instrumentName = unicode(f_trade_instrument.Name(), errors='ignore')

            #instrument number
            instrumentNumber = f_trade_instrument.Oid()

            #underlyingInstrument type
            if f_trade_instrument.Underlying():
                underlyingInstrumentType = FC_UTILS.getEnum('InsType', f_trade_instrument.Underlying().InsType())

            #Book Logic - use Desk (Acquired) as book for Curr
            if instrumentType=='Curr':
                if f_trade_acquirer:
                    bookCode = f_trade_acquirer.Oid()
                    bookName = f_trade_acquirer.Name()
            else:
                if trade.FTrade.Portfolio():
                    bookCode = f_trade.Portfolio().Oid()
                    try:
                        bookName = unicode(f_trade.Portfolio().Name())
                    except UnicodeDecodeError, e:
                        UTILS.Logger.flogger.info('Failed to decode portfolio name')
                        bookName = unicode(f_trade.Portfolio().Name(), errors='ignore')

        #acquirerNumber
        acquirerNumber = 0
        if f_trade_acquirer:
            acquirerNumber = f_trade_acquirer.Oid()
            
        #counterpartyNumber
        counterpartyNumber = 0
        if f_trade.Counterparty():
            counterpartyNumber = trade.FTrade.Counterparty().Oid()          

        #tradeCurrency
        tradeCurrency = None
        if f_trade.Currency():
            tradeCurrency = f_trade.Currency().Name()

        #tradeStatus
        tradeStatus= FC_UTILS.getEnum('TradeStatus', f_trade.Status())

        #tradeDateTime
        tradeDateTime=FC_UTILS.formatDate(f_trade.TradeTime())

        #executionDateTime
        executionDateTime = FC_UTILS.formatDate(f_trade.ExecutionTime())

        #valueDate
        valueDate=FC_UTILS.formatDate(f_trade.ValueDay())

        #maturityDate
        maturityDate = None
        try:
            maturityDate=FC_UTILS.formatDate(f_trade.maturity_date())
        except:
            maturityDate = None

        #traderNumber
        traderNumber = 0
        if f_trade.Trader():
            traderNumber = f_trade.Trader().Oid()

        #isOTC
        isOTC=False #Need some logic to determine

        #createUserNumber
        createUserNumber = 0
        if f_trade.CreateUser():
            createUserNumber= f_trade.CreateUser().Oid()

        #createDateTime
        createDateTime=FC_UTILS.formatDate(f_trade.CreateTime())

        #updateUserNumber
        updateUserNumber = 0
        if f_trade.UpdateUser():
            updateUserNumber= f_trade.UpdateUser().Oid()

        #updateDateTime
        updateDateTime=FC_UTILS.formatDate(f_trade.UpdateTime())

        #get the tradeInfo and trade error Xml
        tradeInfoXml = trade.GetInfoAsXml()
        tradeErrorXml = trade.GetErrorsAsXml()

        #get versionID
        versionID = 0
        try:
            versionID = f_trade.VersionId()
        except:
            versionID = 0        
        sqlParams=[
            requestId,
            tradeIndex,
            reportDate,
            tradeNumber,
            connectedTradeNumber,
            externalId,
            versionID,
            portfolioNumber,
            bookCode,
            bookName,
            instrumentName,
            instrumentNumber,
            instrumentType,
            underlyingInstrumentType,
            acquirerNumber,
            counterpartyNumber,
            tradeCurrency,
            tradeStatus,
            tradeDateTime,
            executionDateTime,
            valueDate,
            maturityDate,
            traderNumber,
            isOTC,
            createUserNumber,
            createDateTime,
            updateUserNumber,
            updateDateTime,
            self.DBCreateProcess,
            tradeInfoXml,
            trade.SerializedData,
            tradeErrorXml
        ]
        return sqlParams
       
    def getInvalidTradePortfolioCounts(self, reportDate, batchId):
        results = self.dbProvider.executeNoParams(self.portfolioCountSql %(reportDate, batchId))
        return results
#Test
#tradeStaticRepository = FC_DATA_TRADE_STATIC_REPOSITORY(None)
#print dir(tradeStaticRepository)
