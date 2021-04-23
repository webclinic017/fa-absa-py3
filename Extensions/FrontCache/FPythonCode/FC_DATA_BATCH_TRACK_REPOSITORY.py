
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_BATCH_TRACK_REPOSITORY
PROJECT                 :       Front Cache
PURPOSE                 :       This repository for batch tracker database operations
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
import FC_ENUMERATIONS
from FC_DATA_BASE_REPOSITORY import FC_DATA_BASE_REPOSITORY as fcDataBaseRepository
from FC_UTILS import FC_UTILS as UTILS
  
class FC_DATA_BATCH_TRACK_REPOSITORY(fcDataBaseRepository):
    createBatchTrackerSql = UTILS.Constants.fcGenericConstants.FRONTCACHE_CREATE_BATCH_TRACKER
    updateBatchTrackerSql = UTILS.Constants.fcGenericConstants.FRONT_CACHE_UPDATE_BATCH_TRACKER_END
    updateBatchRequestEndSql = UTILS.Constants.fcGenericConstants.FRONTCACHE_UPDATE_BATCH_REQUEST_END
    
    def __init__(self, dbProvider):
        fcDataBaseRepository.__init__(self, dbProvider)      
        
    def create(self, reportDate, isEod, topic, expectedCount):
        sqlParams=self.createSqlParams(reportDate, isEod, topic, expectedCount)
        try:
            result=self.dbProvider.executeScalar(self.createBatchTrackerSql, sqlParams)
            
            if result and len(result)==1:
                return result[0]
            else:
                return None
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.BATCH_TRACKER_FAILED_S % str(e))
    
    def update(self, requestId):
        sqlParams=[requestId]
        try:
            self.dbProvider.executeNoReturn(self.updateBatchTrackerSql, sqlParams)
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.TRACKER_FAILED_S % str(e))
            
    def updateBatchRequestEnd(self, requestId, processedCount, errorCount, requestCollectionTrackerId, batchId,
                              errorTradeNumbers):
        sqlParams= self.updateBatchRequestEndSqlParams(requestId, processedCount, errorCount,
                                                       requestCollectionTrackerId, batchId, errorTradeNumbers)
        try:
            result = self.dbProvider.executeScalar(self.updateBatchRequestEndSql, sqlParams)
            #result = self.dbProvider.executeScalarCustom(requestId, processedCount, errorCount,
                                 #                        requestCollectionTrackerId, batchId,errorTradeNumbers)
            if result and len(result) == 1:
                return result[0]
            else:
                return None
        except Exception, e:
            self.dbProvider.rollback()
            print sqlParams
            raise Exception(UTILS.Constants.fcExceptionConstants.REQUEST_END_FAILED_S % str(e))
            
    def createSqlParams(self, reportDate, isEod, topic, expectedCount):
        try:
            sqlParams=[reportDate,
                       self.TradeDomain,
                       isEod,
                       FC_ENUMERATIONS.RequestTopic.fromstring(topic),
                       expectedCount,
                       self.DBCreateProcess
                       ]
            return sqlParams
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.CREATE_SQL_PARAMETERS_FAILED % str(e))
            
    def updateBatchRequestEndSqlParams(self, requestId, processedCount, errorCount, requestCollectionTrackerId, batchId,
                                       errorTradeNumbers):
        try:
            sqlParams = [requestId,
                         processedCount,
                         errorCount,
                         requestCollectionTrackerId,
                         batchId,
                         errorTradeNumbers]
            return sqlParams
        except Exception, e:
            raise Exception(UTILS.Constants.fcFloggerConstants.CALL_IN_MODULE_S_ERROR_S %(__name__, str(e)))
    
