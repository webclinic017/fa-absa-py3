'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_SETTLEMENT_REPOSITORY
PROJECT                 :       Front Cache
PURPOSE                 :       This repository for settlement database operations
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       BBD
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
from FC_DATA_BASE_REPOSITORY import FC_DATA_BASE_REPOSITORY as fcDataBaseRepository
import FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
from FC_DATA_REPOSITORY_ABSTRACT import FC_DATA_REPOSITORY_ABSTRACT

class FC_DATA_SETTLEMENT_REPOSITORY(fcDataBaseRepository, FC_DATA_REPOSITORY_ABSTRACT):
    createSql = UTILS.Constants.fcGenericConstants.FRONTCACHE_CREATE_SETTLEMENT_ENTITY  # Create stored proc for settlement
    
    #Constructor
    def __init__(self, dbProvider):
        fcDataBaseRepository.__init__(self, dbProvider)      
    
    #Methods
    #Creates a settlement static database row as part of a transaction (commit needs to be called on the dbProvider)
    def create(self, requestId, reportDate, settlementIndex, settlement): # Update params for settlement        
        sqlParams=self.createSqlParams(requestId, reportDate, settlementIndex, settlement) # Update params for settlement 
        #Test sql params
        if not sqlParams or len(sqlParams)==0:
            raise Exception(UTILS.Constants.fcExceptionConstants.CREATE_SQL_PARAMETERS)
        #Commit and get the settlement id saved        
        result = self.dbProvider.executeScalar(self.createSql, sqlParams)
        
        if not result and len(result)!=1:
            raise Exception(UTILS.Constants.fcExceptionConstants.CREATE_THE_SETTLEMENT)
        return result[0]
    
    def createSqlParams(self, requestId, reportDate, settlementIndex, settlement):# Update params for settlement        
        #Basic Validation on the trade static contained before we persist
        if not settlement.Data.FSettlement: # refactor
            raise Exception(UTILS.Constants.fcExceptionConstants.F_SETTLEMENT_INSTANCE)
        elif not settlement.SerializedData: #refactor
            raise Exception(UTILS.Constants.fcExceptionConstants.NOT_HAVE_SERIALIZED_DATA)
        
        #Fetch (and format) some meta data of the FTrade instance
        #This is the official mapping to the database table
        #tradeNumber
        '''
         Need to add script logic here to set sql params from settlement object.
         Note: Use UTILS to format date.
        '''

        #Fetch (and format) some meta data of the FSettlement instance
        #This is the official mapping to the database table
        #settlementNumber
        settlementNumber = settlement.Data.FSettlement.Oid()

        #connectedTradeNumber
        connectedSettlementNumber=0
        if settlement.Data.FSettlement.ConnectedSettlement():
            connectedSettlementNumber = settlement.Data.FSettlement.ConnectedSettlement().Oid()
                     
        #settlementStatus
        settlementStatus=FC_UTILS.getEnum('SettlementStatus', settlement.Data.FSettlement.Status())

        #settlementDateTime
        settlementDateTime=FC_UTILS.formatDate(settlement.Data.FSettlement.ValueDay()) # Need to find the correct value

        #executionDateTime
        #executionDateTime =  FC_UTILS.formatDate(trade.Data.FTrade.ExecutionTime())

        #valueDate
        valueDate=FC_UTILS.formatDate(settlement.Data.FSettlement.ValueDay())

        #traderNumber
        traderNumber = 0
        if settlement.Data.FSettlement.Trade():
            traderNumber = settlement.Data.FSettlement.Trade().Oid()

        #isOTC
        isOTC=False #Need some logic to determine

        #createUserNumber
        createUserNumber = 0
        if settlement.Data.FSettlement.CreateUser():
            createUserNumber=settlement.Data.FSettlement.CreateUser().Oid()

        #createDateTime
        createDateTime=FC_UTILS.formatDate(settlement.Data.FSettlement.CreateTime())

        #updateUserNumber
        updateUserNumber = 0
        if settlement.Data.FSettlement.UpdateUser():
            updateUserNumber=settlement.Data.FSettlement.UpdateUser().Oid()

        #updateDateTime
        updateDateTime=FC_UTILS.formatDate(settlement.Data.FSettlement.UpdateTime())
        cashFlowNumber = 0
        if settlement.Data.FSettlement.CashFlow():
            cashFlowNumber = settlement.Data.FSettlement.CashFlow().Oid()
        #get the tradeInfo and trade error Xml
        settlementInfoXml = settlement.GetInfoAsXml()
        settlementErrorXml = settlement.GetErrorsAsXml()
        correspondentBank = 0
        if settlement.Data.FSettlement.TheirCorrBank():
            correspondentBank = settlement.Data.FSettlement.TheirCorrBank()

        sqlParams=[settlementNumber,
                   requestId,
                   traderNumber,
                   cashFlowNumber,
                   reportDate,
                   settlementDateTime,
                   createDateTime,
                   settlementStatus,
                   connectedSettlementNumber,
                   correspondentBank,
                   self.DBCreateProcess,
                   settlementInfoXml,
                   settlement.SerializedData,
                   settlementErrorXml]

        return sqlParams
       
        
    
#Test
#tradeStaticRepository = FC_DATA_TRADE_STATIC_REPOSITORY(None)
#print dir(tradeStaticRepository)
