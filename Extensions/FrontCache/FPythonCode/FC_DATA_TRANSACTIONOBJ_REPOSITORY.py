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

class FC_DATA_TRANSACTIONOBJ_REPOSITORY(fcDataBaseRepository):
    createSql = "FrontCache.CreateTransactionEntity"
    
    #Constructor
    def __init__(self, dbProvider):
        fcDataBaseRepository.__init__(self, dbProvider)      
    
    #Methods
    #Creates a settlement static database row as part of a transaction (commit needs to be called on the dbProvider)
    def create(self, requestId, reportDate, transactionIndex, transactionObj, typeOfTx): # Update params for settlement
        sqlParams=self.createSqlParams(requestId, reportDate, transactionIndex, transactionObj, typeOfTx) # Update params for settlement
        #Test sql params
        if not sqlParams or len(sqlParams)==0:
            raise Exception(UTILS.Constants.fcExceptionConstants.CREATE_SQL_PARAMETERS)
        #Commit and get the settlement id saved        
        result = self.dbProvider.executeScalar(self.createSql, sqlParams)
        
        if not result and len(result)!=1:
            raise Exception(UTILS.Constants.fcExceptionConstants.CREATE_THE_SETTLEMENT)
        return result[0]
    
    def createSqlParams(self, requestId, reportDate, transactionIndex, transactionObj, typeOfTx):# Update params for settlement
        #Basic Validation on the trade static contained before we persist


        sqlParams=[requestId,
                   typeOfTx,
                   reportDate,
                   self.DBCreateProcess,
                   transactionObj
                   ]

        return sqlParams
       
        
    
#Test
#tradeStaticRepository = FC_DATA_TRADE_STATIC_REPOSITORY(None)
#print dir(tradeStaticRepository)
