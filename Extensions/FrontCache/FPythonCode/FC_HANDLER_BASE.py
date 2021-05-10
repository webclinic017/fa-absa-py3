
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_HANDLER_BASE
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module serves as a base for any Handler. It forces the implementation of
                                initialise and __createAMBWriter,... methods
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Class forcing the implemtation of specific functions for the Handler being created.
----------------------------------------------------------------------------------------------------------'''
from FC_UTILS import FC_UTILS as UTILS
class FC_HANDLER_BASE():
    def initialise(self):
        #The handler class needs to override the initialise method.
        raise NotImplementedError(UTILS.Constants.fcExceptionConstants.HANDLER_CLASS_OVERRIDE_HANDLER_METHOD)
    
    def __createAMBWriter(self):
        #If the specific handler needs to write to the AMB this function needs to be overridden in the class that inherents from the base.
        raise NotImplementedError(UTILS.Constants.fcExceptionConstants.HANDLER_CLASS_OVERRIDE_CREATEAMBWRITER_METHOD)
