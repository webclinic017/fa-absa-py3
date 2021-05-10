
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_CONSTANTS_SINGLETON
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will expose Generic, Exception and Logger constants as properties
                                which will be accessible form FC_UTILS. This retreival of information will only
                                be done once.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       BBD
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules modules needed for Real Time ATS Worker.
----------------------------------------------------------------------------------------------------------'''
from FC_CONSTANTS_LOGGER import FC_CONSTANTS_LOGGER as LOGGER_CONSTANTS
from FC_CONSTANTS_EXCEPTIONS import FC_CONSTANTS_EXCEPTIONS as EXCEPTION_CONSTANTS
from FC_CONSTANTS_GENERIC import FC_CONSTANTS_GENERIC as GENERIC_CONSTANTS

'''----------------------------------------------------------------------------------------------------------
Class that creates only one instance of the Parameters to be used which ca be used throughout the program
via FC_UTILS without initializing it every time.
----------------------------------------------------------------------------------------------------------'''
class FC_CONSTANTS_SINGLETON(object):
    instance = None
    __fcExceptionConstants = None
    __fcFloggerConstants = None
    __fcGenericConstants = None
    
    class FC_CONSTANTS_HELPER:
        def __call__(self, *args, **kwargs):
            if FC_CONSTANTS_SINGLETON.instance is None:
                object = FC_CONSTANTS_SINGLETON()
                FC_CONSTANTS_SINGLETON.instance = object
            return FC_CONSTANTS_SINGLETON.instance
                
    Instance = FC_CONSTANTS_HELPER()
    
    def __init__(self):
        if not FC_CONSTANTS_SINGLETON.instance == None:
            raise RuntimeError('Only one instance of FC_CONSTANTS_SINGLETON is allowed!')
        else:
            self.__fcExceptionConstants = EXCEPTION_CONSTANTS()
            self.__fcFloggerConstants = LOGGER_CONSTANTS()
            self.__fcGenericConstants = GENERIC_CONSTANTS()

    @property
    def fcGenericConstants(self):
        return self.__fcGenericConstants
        
    @property
    def fcFloggerConstants(self):
        return self.__fcFloggerConstants

    @property
    def fcExceptionConstants(self):
        return self.__fcExceptionConstants
