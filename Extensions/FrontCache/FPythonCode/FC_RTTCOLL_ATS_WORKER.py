
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_RTTCOLL_ATS_WORKER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module is the base module for Realtime Trade ATSs. It will connect to the
                                AMB and prcess Realtime Trade Requests. It will retreive the data from Front
                                Arena, save the data to the database and post reponse messages to the AMB.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Busisiwe Masango/Sizwe Sokopo
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
import FC_COLL_ATS_WORKER_BASE as COLL_ATS_WORKER_BASE
import FC_DATA_HELPER as DATA_HELPER
from FC_DATA_TRD_BUILDER_OPTIONS import FC_DATA_TRD_BUILDER_OPTIONS as  fcDataTradeBuilderOptions
import FC_ENUMERATIONS as ENUMERATIONS
    
'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_RTTCOLL_ATS_WORKER(COLL_ATS_WORKER_BASE.FC_COLL_ATS_WORKER_BASE):
    def __init__(self):
        COLL_ATS_WORKER_BASE.FC_COLL_ATS_WORKER_BASE.__init__(self)
    
    def SaveData(self, requestId, reportDate, startIndex, numbers, buildControlMeasures, retryCount, requestType,
scopeName):
        self._buildOptions =   fcDataTradeBuilderOptions()
        self._buildOptions.SerializationType = ENUMERATIONS.SerializationType.XML_COMPRESSED
        self._buildOptions.HistoricalCashflowRange = 5
        self._buildOptions.BuildControlMeasures = buildControlMeasures
        return DATA_HELPER.BuildAndSaveTrades(requestId, reportDate, startIndex, numbers, self._buildOptions, retryCount)
