'''----------------------------------------------------------------------------------------------------------
MODULE                  :       DDM_ATS_REQUEST_WORKER14
PROJECT                 :       Pegasus - Data Distribution Model (DDM)
PURPOSE                 :       This is the ATS module for the ATS_DDM_REQUEST_WORKER14 service
DEPARTMENT AND DESK     :       PCG Change
REQUASTER               :       Pegasus Project
DEVELOPER               :       Heinrich Momberg/Heinrich Cronje
CR NUMBER               :       TBA
-------------------------------------------------------------------------------------------------------------
'''
from DDM_REQUEST_WORKER import DDM_REQUEST_WORKER 
import DDM_ATS_PARAMS as params

#Globals
worker = None
nodeNumber = 14
atsName = '%s%i' %(params.requestWorkerATSNameTemplate, int(nodeNumber))
readerMBName = '%s_%i' % (params.requestWorkerReaderMBTemplate, int(nodeNumber))
readerSubjects = ['%s%i' %(params.requestWorkerReaderSubjectTemplate, int(nodeNumber))]

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
        worker = DDM_REQUEST_WORKER(atsName, readerMBName, readerSubjects)
    worker.start()
