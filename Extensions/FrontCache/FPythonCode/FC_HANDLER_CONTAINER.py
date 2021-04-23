
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_HANDLER_CONTAINER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module server as a container of handlers. The specific type of handlers
                                can be database handlers, AMB writer handlers, ...
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
from FC_UTILS import FC_UTILS as UTILS
from FC_HANDLER_AMB_WRITER import FC_HANDLER_AMB_WRITER as HANDLER_AMB_WRITER

'''----------------------------------------------------------------------------------------------------------
Class represending a container of handlers
----------------------------------------------------------------------------------------------------------'''
class FC_HANDLER_CONTAINER():
    def __init__(self, isConnected = True):
        self.ambWriterHandlers = {}
        self.dbWriter = None
        self.__loadHandlers(isConnected)
    
    def __loadHandlers(self, isConnected):
        if UTILS.Parameters.fcComponentParameters.componentHandlerAMBSenderFlag:
            componentHandlersSettings = UTILS.Parameters.fcComponentParameters.componentSenderHandlers
            for requestType in list(componentHandlersSettings.keys()):
                ambWriter = HANDLER_AMB_WRITER(UTILS.Parameters.fcComponentParameters.componentAMBHost,\
                                UTILS.Parameters.fcComponentParameters.componentAMBPort,\
                                componentHandlersSettings[requestType][0],\
                                componentHandlersSettings[requestType][1],\
                                requestType,
                                componentHandlersSettings[requestType][4],
                                isConnected)
                isConnected = True
                self.ambWriterHandlers[requestType] = ambWriter
            
    def initialise(self):
        for requestType in list(self.ambWriterHandlers.keys()):
            self.ambWriterHandlers[requestType].initialise()
