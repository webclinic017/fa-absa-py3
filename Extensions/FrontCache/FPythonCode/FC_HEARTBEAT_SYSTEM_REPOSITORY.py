
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_HEARTBEAT_SYSTEM_REPOSITORY
PROJECT                 :       Front Cache
PURPOSE                 :       This repository for system heart beat database operations
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

from FC_DATA_BASE_REPOSITORY import FC_DATA_BASE_REPOSITORY as fcDataBaseRepository
from FC_UTILS import FC_UTILS as UTILS

class FC_HEARTBEAT_SYSTEM_REPOSITORY(fcDataBaseRepository):
    createSql = 'FrontCache.ReportHeartbeatSystem'

    #Constructor
    def __init__(self, dbProvider):
        fcDataBaseRepository.__init__(self, dbProvider)
    
    #Methods
    #Creates a heart beat system database row as part of a transaction (commit needs to be called on the dbProvider)
    def create(self, reportDate, heartBeatSystem):
        sqlParams = self.createSqlParams(reportDate, heartBeatSystem)
    
        #Test sql params
        if not sqlParams or len(sqlParams) == 0:
            raise Exception('Could not create SQL parameters')
        #Commit and get the heart beat process id saved
        try:
            self.dbProvider.executeNoReturn(self.createSql, sqlParams)
        except Exception as e:
            self.dbProvider.rollback()
            raise Exception('Could not create the Heart Beat Process. %s' %str(e))
    
    def createSqlParams(self, reportDate, heartBeatSystem):
        
        sqlParams = [
            heartBeatSystem.HostName,
            heartBeatSystem.IPAddress,
            UTILS.FrontArenaInstanceName,
            heartBeatSystem.ComponentName,
            reportDate,
            heartBeatSystem.CpuCount,
            heartBeatSystem.CpuPercent,
            heartBeatSystem.CpuTimeIdleMode,
            heartBeatSystem.CpuTimePercentIdleMode,
            heartBeatSystem.CpuTimePercentSystemMode,
            heartBeatSystem.CpuTimePercentUserMode,
            heartBeatSystem.CpuTimeSystemMode,
            heartBeatSystem.CpuTimeUserMode,
            heartBeatSystem.DiskIOCounterReadBytes,
            heartBeatSystem.DiskIOCounterReadCount,
            heartBeatSystem.DiskIOCounterReadTime,
            heartBeatSystem.DiskIOCounterWriteBytes,            
            heartBeatSystem.DiskIOCounterWriteCount,
            heartBeatSystem.DiskIOCounterWriteTime,
            heartBeatSystem.SwapMemoryFree,
            heartBeatSystem.SwapMemoryPercent,
            heartBeatSystem.SwapMemorySwapInFromDisk,
            heartBeatSystem.SwapMemorySwapOutFromDisk,
            heartBeatSystem.SwapMemoryTotal,
            heartBeatSystem.SwapMemoryUsed,
            heartBeatSystem.VirtualMemoryAvailable,
            heartBeatSystem.VirtualMemoryFree,
            heartBeatSystem.VirtualMemoryPercent,
            heartBeatSystem.VirtualMemoryTotal,
            heartBeatSystem.VirtualMemoryUsed,
            UTILS.Parameters.fcComponentParameters.componentDedicatedEod
            #heartBeatSystem.CpuTimePerCPU,
            #heartBeatSystem.CpuTimePercentPerCPU,
            #heartBeatSystem.BootTime,
            #heartBeatSystem.DiskPartitions,
            #heartBeatSystem.DiskUsage,
        ]
        
        return sqlParams
