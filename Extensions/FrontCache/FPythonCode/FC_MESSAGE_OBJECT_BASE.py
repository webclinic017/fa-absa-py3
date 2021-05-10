
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_MESSAGE_OBJECT_BASE
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module contains the base object for a MESSAGE OBJECT. The REQUEST and RESPOSE
                                MESSAGE OBJECT will derive from this class. It contains common properties
                                that belongs to a MESSAGE OBJECT.
                                Message Type.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Class defining the MESSAGE OBJECT
----------------------------------------------------------------------------------------------------------'''
class FC_MESSAGE_OBJECT_BASE():
    def __init__(self):
        self.ambaTxNbr = 0
        self.batchId = 0
        self.isEOD = 0
        self.reportDate = None
        self.requestDateTime = None
        self.requestEventType = None
        self.requestId = 0
        self.requestSource = None
        self.requestType = None
        self.requestUserId = None
        self.scopeName = None
        self.scopeNumber = None
        self.topic = None
        self.type = None
        self.replay = False
        self.isDateToday = 0
        self.backDateStart = None

    def mapMessageObjectToAMBADataDictionary(self):
        raise NotImplementedError('The method mapMessageObjectToAMBADataDictionary defined in Base Class %s needs to be implemented.' %__name__)
