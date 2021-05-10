
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_EXCEPTION
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module contains a class which is a Front Cache Exception. It will be used
                                as a container of exceptions picked up in the code. This Exception class can
                                be given to FC_ERROR_HANDLER to handel the exception and all the inner 
                                Excepitons.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

class FC_EXCEPTION(Exception):
    def __init__(self, textMsg, traceback, severity, innerException):
        self.__textMsg = None
        self.__traceback = None
        self.__severity = None
        self.__innerException = None
        
        if textMsg != None:
            self.__textMsg = str(textMsg)
        if traceback != None:
            self.__traceback = traceback.format_exc()
        if severity != None:
            self.__severity = str(severity)
        if innerException != None:
            self.__innerException = innerException

    @property
    def TextMsg(self):
        return self.__textMsg
    
    @property
    def Traceback(self):
        return self.__traceback
    
    @property
    def Severity(self):
        return self.__severity
    
    @property
    def InnerException(self):
        return self.__innerException
