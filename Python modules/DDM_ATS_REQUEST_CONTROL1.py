
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       DDM_ATS_REQUEST_CONTROL1
PROJECT                 :       Pegasus - Data Distribution Model (DDM)
PURPOSE                 :       This is the ATS module for the ATS_DDM_REQUEST_CONTROL1 service
DEPARTMENT AND DESK     :       PCG Change
REQUASTER               :       Pegasus Project
DEVELOPER               :       Heinrich Momberg/Heinrich Cronje
CR NUMBER               :       TBA
-------------------------------------------------------------------------------------------------------------
'''
from DDM_REQUEST_CONTROL import DDM_REQUEST_CONTROL 
import DDM_ATS_PARAMS as params

#Globals
controller = None
nodeNumber = 1
atsName = '%s%i' %(params.requestControlATSNameTemplate, int(nodeNumber))
readerMBName = params.requestControlReaderMBName
readerSubjects = ['%s%i' %(params.requestControlReaderSubjectTemplate, int(nodeNumber))]

def work():
    global controller
    if not controller:
        raise Exception('Controller class not instantiated') 
    controller.work()
   

def start():
    global controller
    
    global atsName
    global readerSubjects
    if not controller:
        controller = DDM_REQUEST_CONTROL(atsName, readerMBName, readerSubjects)
    controller.start()
   

