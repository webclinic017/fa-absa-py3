
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_REQ_REPOSITORY
PROJECT                 :       Front Cache
PURPOSE                 :       This repository for request database operations
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
from FC_DATA_BASE_REPOSITORY import FC_DATA_BASE_REPOSITORY as fcDataBaseRepository
from FC_UTILS import FC_UTILS as UTILS
import FC_ENUMERATIONS

from datetime import datetime

class FC_DATA_REQUEST_REPOSITORY(fcDataBaseRepository):
    createSql = UTILS.Constants.fcGenericConstants.FRONTCACHE_CREATE_REQUEST_ENTITY
    independentTradeCount = UTILS.Constants.fcGenericConstants.FRONTCACHE_GET_INDEPENDENT_TRADE_COUNT
    _recordFailedSelection = UTILS.Constants.fcGenericConstants.FRONTCACHE_RECORD_FAILED_SELECTION

    def __init__(self, dbProvider):
        fcDataBaseRepository.__init__(self, dbProvider)      
        
    def create(self, requestMessage, recovery_mode):
        sqlParams=self.createSqlParams(requestMessage)
        try:
            if recovery_mode is True and requestMessage.batchId != 0:
                sql = """
                      select top 1 RequestId
                      from frontcache.Request
                      where batchid = %s and scopenumber = %s
                """ % (requestMessage.batchId, requestMessage.scopeNumber)
                result = self.dbProvider.executeNoParamsScalar(sql)
                if result and len(result)==1: # used just for logging info
                    UTILS.Logger.flogger.info("Found existing RequestId %s " % (str(result[0])))
            else:
                result = self.dbProvider.executeScalar(self.createSql, sqlParams)
            if result and len(result)==1:
                return result[0]
            else:
                return None
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.REQUEST_ENTITY_FAILED_S % str(e))

    def getIndependentTradeCount(self, reportDate, bookId):
        try:
            sqlparms = [reportDate, bookId]
            result = self.dbProvider.executeScalar(self.independentTradeCount, sqlparms)
            if result and len(result)==1:
                return result[0]
            else:
                return None
        except Exception, e:
            raise Exception('Get independent selection data failed. %s' % str(e))

    def recordFailedSelection(self, reportDate, bookName, requestMessage):
        try:
            sqlparms = [reportDate, bookName, requestMessage]
            result = self.dbProvider.executeScalar(self._recordFailedSelection, sqlparms)
            if result and len(result)==1:
                return result[0]
            else:
                return None
        except Exception, e:
            raise Exception('Recording of failed selection failed. %s' % str(e))

    def createSqlParams(self, requestMessage):
        try:
            #Basic Validation on the request message before we persist
            if not requestMessage:
                raise Exception(UTILS.Constants.fcExceptionConstants.MUST_BE_PROVIDED)
            
            if requestMessage.batchId == 0:
                batchId = None
            else:
                batchId = requestMessage.batchId
            newName = str(requestMessage.scopeName).decode('ascii', 'ignore')
            sqlParams=[
                        batchId,
                        requestMessage.reportDate,
                        self.TradeDomain,
                        requestMessage.isEOD,
                        requestMessage.requestDateTime,
                        FC_ENUMERATIONS.RequestType.fromstring(requestMessage.requestType),
                        requestMessage.requestUserId,
                        newName,
                        requestMessage.scopeNumber,
                        FC_ENUMERATIONS.RequestTopic.fromstring(requestMessage.topic),
                        0, #ExpectedCount
                        0, #ProcessedCount
                        0, #ErrorCount
                        datetime.now(), #StartDateTIme
                        None, #EndDateTime
                        self.DBCreateProcess
                       ]
            
            
            return sqlParams
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.CREATE_SQL_PARAMETERS_FAILED % str(e))
        
    

