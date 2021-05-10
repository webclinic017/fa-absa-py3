
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_HEART_BEAT_OBJECT_SYSTEM
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will create a SYSTEM Heart Beat object containing all relevant
                                statistics regarding the system (Machine/Server). This information will be
                                send to the DB for monitoring.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
import datetime, psutil, socket

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
from FC_UTILS import FC_UTILS as UTILS

'''----------------------------------------------------------------------------------------------------------
Class describing a Heat Beat System Object
----------------------------------------------------------------------------------------------------------'''
class FC_HEART_BEAT_OBJECT_SYSTEM(object):
    def __init__(self):
        self.__componentName = UTILS.ComponentName
        self.__cpuPercent = psutil.cpu_percent(interval = 0)
        self.__cpuTimes = psutil.cpu_times()
        self.__cpuTimeUserMode = self.__cpuTimes[0]
        self.__cpuTimeSystemMode = self.__cpuTimes[1]
        self.__cpuTimeIdleMode = self.__cpuTimes[2]
        self.__cpuTimePerCPU = psutil.cpu_times(percpu = True)
        self.__cpuTimesPercent = psutil.cpu_times_percent(interval = 0)
        self.__cpuTimePercentUserMode = self.__cpuTimesPercent[0]
        self.__cpuTimePercentSystemMode = self.__cpuTimesPercent[1]
        self.__cpuTimePercentIdleMode = self.__cpuTimesPercent[2]
        self.__cpuTimePercentPerCPU = psutil.cpu_times_percent(interval = 0, percpu = True)
        self.__cpuCount = psutil.cpu_count()
        self.__virtualMemory = psutil.virtual_memory()
        self.__virtualMemoryTotal = self.__virtualMemory[0]
        self.__virtualMemoryAvailable = self.__virtualMemory[1]
        self.__virtualMemoryPercent = self.__virtualMemory[2]
        self.__virtualMemoryUsed = self.__virtualMemory[3]
        self.__virtualMemoryFree = self.__virtualMemory[4]
        self.__swapMemory = psutil.swap_memory()
        self.__swapMemoryTotal = self.__swapMemory[0]
        self.__swapMemoryUsed = self.__swapMemory[1]
        self.__swapMemoryFree = self.__swapMemory[2]
        self.__swapMemoryPercent = self.__swapMemory[3]
        self.__swapMemorySwapInFromDisk = self.__swapMemory[4]
        self.__swapMemorySwapOutFromDisk = self.__swapMemory[5]
        self.__bootTime = datetime.datetime.fromtimestamp(psutil.boot_time())
        self.__diskPartitions = psutil.disk_partitions(all = True)
        self.__diskUsage = {}
        for diskPartition in self.__diskPartitions:
            try:
                self.__diskUsage[diskPartition.device] = str(psutil.disk_usage(diskPartition.device))
            except:
                self.__diskUsage[diskPartition.device] = 'No Information'
        self.__diskIOCounters = psutil.disk_io_counters()
        self.__diskIOCounterReadCount = self.__diskIOCounters[0]
        self.__diskIOCounterWriteCount = self.__diskIOCounters[1]
        self.__diskIOCounterReadBytes = self.__diskIOCounters[2]
        self.__diskIOCounterWriteBytes = self.__diskIOCounters[3]
        self.__diskIOCounterReadTime = self.__diskIOCounters[4]
        self.__diskIOCounterWriteTime = self.__diskIOCounters[5]
        self.__hostName = socket.gethostname()
        self.__ipAddress = socket.gethostbyname(self.__hostName)
    
    @property
    def ComponentName(self):
        return self.__componentName
        
    @property
    def CpuPercent(self):
        return self.__cpuPercent
    
    @property
    def CpuTimeUserMode(self):
        return self.__cpuTimeUserMode
        
    @property
    def CpuTimeSystemMode(self):
        return self.__cpuTimeSystemMode
        
    @property
    def CpuTimeIdleMode(self):
        return self.__cpuTimeIdleMode
    
    @property
    def CpuTimePerCPU(self):
        return self.__cpuTimePerCPU
    
    @property
    def CpuTimePercentUserMode(self):
        return self.__cpuTimePercentUserMode
        
    @property
    def CpuTimePercentSystemMode(self):
        return self.__cpuTimePercentSystemMode
        
    @property
    def CpuTimePercentIdleMode(self):
        return self.__cpuTimePercentIdleMode
    
    @property
    def CpuTimePercentPerCPU(self):
        return self.__cpuTimePercentPerCPU
    
    @property
    def CpuCount(self):
        return self.__cpuCount
    
    @property
    def VirtualMemoryTotal(self):
        return self.__virtualMemoryTotal
    
    @property
    def VirtualMemoryAvailable(self):
        return self.__virtualMemoryAvailable
    
    @property
    def VirtualMemoryPercent(self):
        return self.__virtualMemoryPercent
    
    @property
    def VirtualMemoryUsed(self):
        return self.__virtualMemoryUsed
    
    @property
    def VirtualMemoryFree(self):
        return self.__virtualMemoryFree
    
    @property
    def SwapMemoryTotal(self):
        return self.__swapMemoryTotal
        
    @property
    def SwapMemoryUsed(self):
        return self.__swapMemoryUsed
        
    @property
    def SwapMemoryFree(self):
        return self.__swapMemoryFree
        
    @property
    def SwapMemoryPercent(self):
        return self.__swapMemoryPercent
        
    @property
    def SwapMemorySwapInFromDisk(self):
        return self.__swapMemorySwapInFromDisk
        
    @property
    def SwapMemorySwapOutFromDisk(self):
        return self.__swapMemorySwapOutFromDisk
    
    @property
    def BootTime(self):
        return self.__bootTime
    
    @property
    def DiskPartitions(self):
        return self.__diskPartitions
    
    @property
    def DiskUsage(self):
        return self.__diskUsage
    
    @property
    def DiskIOCounterWriteCount(self):
        return self.__diskIOCounterWriteCount
    
    @property
    def DiskIOCounterWriteCount(self):
        return self.__diskIOCounterWriteCount
    
    @property
    def DiskIOCounterReadBytes(self):
        return self.__diskIOCounterReadBytes
    
    @property
    def DiskIOCounterWriteBytes(self):
        return self.__diskIOCounterWriteBytes
    
    @property
    def DiskIOCounterReadTime(self):
        return self.__diskIOCounterReadTime
    
    @property
    def DiskIOCounterWriteTime(self):
        return self.__diskIOCounterWriteTime

    @property
    def HostName(self):
        return self.__hostName
        
    @property
    def IPAddress(self):
        return self.__ipAddress
