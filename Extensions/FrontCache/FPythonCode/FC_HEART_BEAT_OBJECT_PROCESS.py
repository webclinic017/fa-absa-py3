
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_HEART_BEAT_OBJECT_PROCESS
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will create a PROCESS Heart Beat object containing all relevant
                                statistics regarding the current process running. This information will be
                                send to the DB for monitoring as well as decision makign regarding message 
                                distribution.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
import datetime, os, psutil

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
from FC_UTILS import FC_UTILS as UTILS

'''----------------------------------------------------------------------------------------------------------
Class describing a Heat Beat Process Object
----------------------------------------------------------------------------------------------------------'''
class FC_HEART_BEAT_OBJECT_PROCESS(object):
    def __init__(self):
        self.__componentName = UTILS.ComponentName
        self.__expectedMessageType = ''
        self.__queueDepth = UTILS.MessageQueueDepth
        self.__process = psutil.Process(os.getpid())
        self.__pid = self.__process.pid
        self.__ppid = self.__process.ppid()
        self.__parent = self.__process.parent()
        self.__name = self.__process.name()
        self.__exe = self.__process.exe()
        self.__createTime = datetime.datetime.fromtimestamp(self.__process.create_time())
        self.__ioCounter = self.__process.io_counters() #<--- idles at 2, peaks at 4
        self.__ioCounterReadCount = self.__ioCounter[0]
        self.__ioCounterWriteCount = self.__ioCounter[1]
        self.__ioCounterReadBytes = self.__ioCounter[2]
        self.__ioCounterWriteBytes = self.__ioCounter[3]
        self.__cpuTimes = self.__process.cpu_times()
        self.__cpuTimeUserMode = self.__cpuTimes[0]
        self.__cpuTimeSystemMode = self.__cpuTimes[1]
        self.__cpuPercent = self.__process.cpu_percent(interval = 0)
        self.__cpuAffinity = self.__process.cpu_affinity()
        self.__memoryInfo = self.__process.memory_info()
        self.__memoryUsage = self.__memoryInfo[0]
        self.__memoryVirtualSize = self.__memoryInfo[1]
        self.__memoryExtInfo = self.__process.memory_info_ex()
        self.__memoryPageFaults = self.__memoryExtInfo[0]
        self.__memoryPeakWorkingSet = self.__memoryExtInfo[1]
        self.__memoryWorkingSet = self.__memoryExtInfo[2]
        self.__memoryPeakPagedPool = self.__memoryExtInfo[3]
        self.__memoryPagedPool = self.__memoryExtInfo[4]
        self.__memoryPeakNonPagedPool = self.__memoryExtInfo[5]
        self.__memoryNonPagedPool = self.__memoryExtInfo[6]
        self.__memoryPageFile = self.__memoryExtInfo[7]
        self.__memoryPeakPageFile = self.__memoryExtInfo[8]
        self.__memoryPrivate = self.__memoryExtInfo[9]
        self.__memoryPercent = self.__process.memory_percent()        
        self.__isRunning = self.__process.is_running() #<--- idles at 2, peaks at 3
        #self.__isRunning = 1
    
    @property
    def ComponentName(self):
        return self.__componentName
    
    @property
    def ExpectedMessageType(self):
        return self.__expectedMessageType
    
    @property
    def QueueDepth(self):
        return self.__queueDepth
        
    @property
    def Id(self):
        return self.__pid
    
    @property
    def ParentId(self):
        return self.__ppid

    @property
    def ParentObject(self):
        return self.__parent
    
    @property
    def Name(self):
        return self.__name
    
    @property
    def ExePath(self):
        return self.__exe
    
    @property
    def CommandLine(self):
        return self.__cmdline
    
    @property
    def CreateTime(self):
        return self.__createTime
    
    @property
    def UserName(self):
        return self.__username
    
    @property
    def Status(self):
        return self.__status
    
    @property
    def Priority(self):
        return self.__priority
    
    @property
    def CurrentWorkingDirectory(self):
        return self.__currentWorkingDirectory
    
    @property
    def IOCounterReadCount(self):
        return self.__ioCounterReadCount
    
    @property
    def IOCounterWriteCount(self):
        return self.__ioCounterWriteCount
    
    @property
    def IOCounterReadBytes(self):
        return self.__ioCounterReadBytes
        
    @property
    def IOCounterWriteBytes(self):
        return self.__ioCounterWriteBytes
        
    @property
    def IOPriority(self):
        return self.__ioPriority
    
    @property
    def NbrHandles(self):
        return self.__nbrHandles
    
    @property
    def NbrThreads(self):
        return self.__nbrThreads
    
    @property
    def Threads(self):
        return self.__threads
    
    @property
    def NbrContexSwitchesVoluntary(self):
        return self.__nbrCtxSwitchesVoluntary 
    
    @property
    def NbrContexSwitchesInVoluntary(self):
        return self.__nbrCtxSwitchesInVoluntary
    
    @property
    def CpuTimeUserMode(self):
        return self.__cpuTimeUserMode
        
    @property
    def CpuTimeSystemMode(self):
        return self.__cpuTimeSystemMode
    
    @property
    def CpuPercent(self):
        return self.__cpuPercent
        
    @property
    def CpuAffinity(self):
        return self.__cpuAffinity
    
    @property
    def MemoryUsage(self):
        return self.__memoryUsage
    
    @property
    def MemoryVirtualSize(self):
        return self.__memoryVirtualSize

    @property
    def MemoryPageFaults(self):
        return self.__memoryPageFaults
    
    @property
    def MemoryPeakWorkingSet(self):
        return self.__memoryPeakWorkingSet
        
    @property
    def MemoryWorkingSet(self):
        return self.__memoryWorkingSet
        
    @property
    def MemoryPeakPagedPool(self):
        return self.__memoryPeakPagedPool
        
    @property
    def MemoryPagedPool(self):
        return self.__memoryPagedPool
        
    @property
    def MemoryPeakNonPagedPool(self):
        return self.__memoryPeakNonPagedPool
        
    @property
    def MemoryNonPagedPool(self):
        return self.__memoryNonPagedPool
        
    @property
    def MemoryPageFile(self):
        return self.__memoryPageFile
        
    @property
    def MemoryPeakPageFile(self):
        return self.__memoryPeakPageFile

    @property
    def MemoryPrivate(self):
        return self.__memoryPrivate
    
    @property
    def MemoryPercent(self):
        return self.__memoryPercent
    
    @property
    def Children(self):
        return self.__children
    
    @property
    def OpenFiles(self):
        return self.__openFiles
    
    @property
    def Connections(self):
        return self.__connections
    
    @property
    def IsRunning(self):
        return self.__isRunning
