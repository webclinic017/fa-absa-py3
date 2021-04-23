
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_HEARTBEAT_PROCESS_REPOSITORY
PROJECT                 :       Front Cache
PURPOSE                 :       This repository for heart beat database operations
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

from FC_DATA_BASE_REPOSITORY import FC_DATA_BASE_REPOSITORY as fcDataBaseRepository
from FC_UTILS import FC_UTILS as UTILS

class FC_HEARTBEAT_PROCESS_REPOSITORY(fcDataBaseRepository):
    createSql = 'FrontCache.UpdateHeartbeatProcessCurrent'
    deleteSql = 'FrontCache.DeleteHeartbeatCurrent'
    candidateComponentSql = 'FrontCache.GetHeartbeatCandidateComponent'
    updateComponentSql = 'FrontCache.UpdateHeartbeatComponentQueue'
    stickyComponentSql = 'FrontCache.GetHeartbeatStickyComponent'

    #Constructor
    def __init__(self, dbProvider):
        fcDataBaseRepository.__init__(self, dbProvider)
    
    #Methods
    #Creates a heart beat process database row as part of a transaction (commit needs to be called on the dbProvider)
    def create(self, heartBeatProcess):
        sqlParams = self.createSqlParams(heartBeatProcess)
    
        #Test sql params
        if not sqlParams or len(sqlParams) == 0:
            raise Exception('Could not create SQL parameters')
        #Commit and get the heart beat process id saved
        try:
            self.dbProvider.executeNoReturn(self.createSql, sqlParams)
        except Exception as e:
            self.dbProvider.rollback()
            raise Exception('Could not create the Heart Beat Process. %s' %str(e))

    #Delete a heart beat process database entry of a component (commit needs to be called on the dbProvider)
    def delete(self):
        sqlParams = self.deleteSqlParams()
        
        #Test sql params
        if not sqlParams or len(sqlParams) == 0:
            raise Exception('Could not create SQL parameters for Delete.')
        #Delete the heartbeat
        try:
            self.dbProvider.executeNoReturn(self.deleteSql, sqlParams)
        except Exception as e:
            self.dbProvider.rollback()
            raise Exception('Could not delete the Heart Beat Process. %s' %str(e))

    #Fetches the best possible candidate for handling a request based on collected heartbeat information
    def getCandidateComponent(self, expectedRequestType, isRT):
        sqlParams = self.candidateComponentSqlParams(expectedRequestType, isRT)
        try:
            result=self.dbProvider.executeScalar(self.candidateComponentSql, sqlParams)
            if result and len(result)==1:
                return result[0]
            else:
                return None
        except Exception as e:
            self.dbProvider.rollback()
            raise Exception('Could not fetch a candidate component for processing the request type. %s' % str(e))
    
    #Getting components that are not responding.
    def getStickyComponent(self, activeTimeRestriction):
        sqlParams = self.stickyComponentSqlParams(activeTimeRestriction)
        try:
            result = self.dbProvider.execueScalar(self.stickyComponentSql, sqlParams)
            if result or len(result) > 0:
                return result
        except Exception as e:
            self.dbProvider.rollback()
            raise Exception('Could not fetch sticky component for processing the request type. %s' % str(e))

    #Updating component queue
    def updateComponentQueue(self, componentName, processedCount): 
        sqlParams = self.updateComponentQueueParams(componentName, processedCount)
        try:
            self.dbProvider.executeNoReturn(self.updateComponentSql, sqlParams)
        except Exception as e:
            self.dbProvider.rollback()
            raise Exception('Could not update the Heart Beat Queue. %s' %str(e))

    def createSqlParams(self, ServiceComponentId):
        sqlParams = [
            ServiceComponentId,
        ]
        
        return sqlParams

    def deleteSqlParams(self):
        
        sqlParams = [UTILS.ComponentName]
        return sqlParams
        
    def candidateComponentSqlParams(self, expectedRequestType, isRT):
        
        sqlParams = [expectedRequestType, UTILS.Parameters.fcGenericParameters.HeartbeatTrackInterval*3, isRT]
        return sqlParams
    
    def updateComponentQueueParams(self, componentName, processedCount):
    
        sqlParams = [componentName, processedCount]
        return sqlParams
