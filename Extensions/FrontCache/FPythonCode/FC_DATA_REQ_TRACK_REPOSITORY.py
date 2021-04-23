
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_REQ_TRACK_REPOSITORY
PROJECT                 :       Front Cache
PURPOSE                 :       This repository for request tracker database operations
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
from FC_UTILS import FC_UTILS as UTILS
from FC_DATA_BASE_REPOSITORY import FC_DATA_BASE_REPOSITORY as fcDataBaseRepository
  
class FC_DATA_REQ_TRACK_REPOSITORY(fcDataBaseRepository):
    updateRequestTrackerStartSql = UTILS.Constants.fcGenericConstants.FRONTCACHE_UPDATE_REQUEST_TRACKER_START
    updateRequestTrackerEndSql = UTILS.Constants.fcGenericConstants.FRONTCACHE_UPDATE_REQUEST_TRACKER_END
    getRequestTrackerResultSql = UTILS.Constants.fcGenericConstants.FRONTCACHE_GET_REQUEST_TRACKER_RESULT
    sendConfirmationOfEndMessage = UTILS.Constants.fcGenericConstants.FRONTCACHE_SEND_CONFIRMATION_TRACKER_RESULT
    checkChunkHasCompleted = 'FrontCache.ChunkHasCompleted'
    
    def __init__(self, dbProvider):
        fcDataBaseRepository.__init__(self, dbProvider)      
        
    def updateRequestTrackerStart(self, requestId, expectedCount):
        sqlParams=[requestId, expectedCount]
        try:
            self.dbProvider.executeNoReturn(self.updateRequestTrackerStartSql, sqlParams)
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.UPDATE_REQ_TRACKER_START_FAILED_S % str(e))
    
    
    def updateRequestTrackerEnd(self, requestId, processedCount, errorCount):
        sqlParams=[requestId, processedCount, errorCount]
        try:
            self.dbProvider.executeNoReturn(self.updateRequestTrackerEndSql, sqlParams)
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.UPDATE_REQ_END_FAILED_S % str(e))
        
    def getRequestTrackerResult(self, requestId):
        sqlParams=[requestId]
        try:
            result = self.dbProvider.executeScalar(self.getRequestTrackerResultSql, sqlParams)
            if result and len(result)==1:
                return result[0]
            else:
                return None
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_GET_REQ_TRACKER_RESULT % str(e))
            
    def SendConfirmationOfEndMessage(self, requestId):
        sqlParams=[requestId]
        try:
            self.dbProvider.executeNoReturn(self.sendConfirmationOfEndMessage, sqlParams)
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.CONFIRMATION_FAILED % str(e))             
	    
    def CheckChunkHasCompleted(self, requestCollectionTrackerId):
        sqlP =[requestCollectionTrackerId]
        try:
            result = self.dbProvider.executeScalarFunction(self.checkChunkHasCompleted, sqlP)
            if result and len(result)==1:
                return result[0]
            else:
                return 0
        except Exception, e:
            raise Exception('Checking if chunk completed failed %s' % str(e))               
