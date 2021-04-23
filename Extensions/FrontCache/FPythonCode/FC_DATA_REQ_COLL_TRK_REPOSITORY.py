
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_REQ_COLL_TRK_REPOSITORY
PROJECT                 :       Front Cache
PURPOSE                 :       This repository for request collection tracker database operations
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX

Date            CR Number       Developer               Description
2019-07-18      XXXXXX          Sizwe Sokopo            Added updateRequestCollectionTrackerStart

-------------------------------------------------------------------------------------------------------------
'''
from FC_UTILS import FC_UTILS as UTILS
from FC_DATA_BASE_REPOSITORY import FC_DATA_BASE_REPOSITORY as fcDataBaseRepository
import FC_ENUMERATIONS

class FC_DATA_REQ_COLL_TRK_REPOSITORY(fcDataBaseRepository):
    createRequestCollectionTrackerSql = UTILS.Constants.fcGenericConstants.FRONTCACHE_CREATE_REQUEST_COLLECTION_TRACKER
    updateRequestCollectionTrackerStartSql = UTILS.Constants.fcGenericConstants.FRONTCACHE_UPDATE_REQUEST_COLLECTION_TRACKER_START
    
    def __init__(self, dbProvider):
        fcDataBaseRepository.__init__(self, dbProvider)      
    
    def updateRequestCollectionTrackerStart(self, requestId, startIndex):
        try:
            sqlParams = [requestId, startIndex]
            self.dbProvider.executeNoReturn(self.updateRequestCollectionTrackerStartSql, sqlParams)
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.UPDATE_REQ_COLL_TRACKER_START_FAILED_S % str(e))
            
    def createRequestCollectionTracker(self, requestId, sourceProcess, targetProcess, internalBatchId,
                                       internalBatchCount, startIndex, endIndex, expectedCount, tradeNumbers,
                                       recovery_mode):

        if recovery_mode is True:
            try:
                sql = """
                      select RequestCollectionTrackerId
                      from frontcache.RequestCollectionTracker
                      where requestid = %s and StartIndex = %s and EndIndex = %s
                """ % (requestId, startIndex, endIndex)
                result = self.dbProvider.executeNoParamsScalar(sql)

                if result and len(result)==1:
                    UTILS.Logger.flogger.info("Found existing RequestCollectionTrackerId %s " % (str(result[0])))
                    return result[0]

            except Exception, e:
                raise Exception('Failed to recover RequestCollectionTrackerId with reason %s' % str(e))

        sqlParams=[requestId,
                   FC_ENUMERATIONS.ServiceComponent.fromstring(sourceProcess),
                   FC_ENUMERATIONS.ServiceComponent.fromstring(targetProcess),
                   internalBatchId,
                   internalBatchCount,
                   startIndex,
                   endIndex,
                   expectedCount,
                   tradeNumbers]
        try:
            result = self.dbProvider.executeScalar(self.createRequestCollectionTrackerSql, sqlParams)
           
            if result and len(result)==1:
                return result[0]
            else:
                return None
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.CREATE_REQ_COLL_TRACKER_FAILED_S % str(e))

    
    
    
    
        
    
