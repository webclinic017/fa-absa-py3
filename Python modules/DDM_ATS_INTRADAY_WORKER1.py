'''----------------------------------------------------------------------------------------------------------
MODULE                  :       DDM_ATS_INTRADAY_WORKER1
PROJECT                 :       Pegasus - Data Distribution Model (DDM)
PURPOSE                 :       This is the ATS module for the ATS_DDM_INTRADAY_WORKER1 service
DEPARTMENT AND DESK     :       PCG Change
REQUASTER               :       Pegasus Project
DEVELOPER               :       Heinrich Momberg/Heinrich Cronje
CR NUMBER               :       TBA
-------------------------------------------------------------------------------------------------------------
'''
from DDM_INTRADAY_WORKER import DDM_INTRADAY_WORKER 
import DDM_ATS_PARAMS as params

#Globals
worker = None
nodeNumber = 1
atsName = '%s%i' %(params.intradayWorkerATSNameTemplate, int(nodeNumber))
readerMBName = params.intradayWorkerReaderMBName
readerSubjects = params.intradayAMBAReaderSubjectList

def work():
    global worker
    if not worker:
        raise Exception('Worker class not instantiated') 
    worker.work()

def start():
    global worker
    global atsName
    global readerSubjects
    if not worker:
        worker = DDM_INTRADAY_WORKER(atsName, readerMBName, readerSubjects)
    worker.start()
