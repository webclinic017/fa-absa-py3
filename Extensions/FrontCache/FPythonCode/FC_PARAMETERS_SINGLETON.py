
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_PARAMETERS_SINGLETON
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will expose Generic, Component and Logger parameters as properties
                                which will be accessible form FC_UTILS. This retreival of information will only
                                be done once.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules modules needed for Real Time ATS Worker.
----------------------------------------------------------------------------------------------------------'''
from FC_PARAMETERS_COMPONENT import FC_PARAMETERS_COMPONENT as COMPONENT_PARAMETERS
from FC_PARAMETERS_GENERIC import FC_PARAMETERS_GENERIC as GENERIC_PARAMETERS
from FC_PARAMETERS_FLOGGER import FC_PARAMETERS_FLOGGER as FLOGGER_PARAMETERS

'''----------------------------------------------------------------------------------------------------------
Class that creates only one instance of the Parameters to be used which ca be used throughout the program
via FC_UTILS without initializing it every time.
----------------------------------------------------------------------------------------------------------'''
class FC_PARAMETERS_SINGLETON(object):
    instance = None
    __componentName = None
    __fcComponentParameters = None
    __fcGenericParameters = None
    __fcFloggerParameters = None
    
    class FC_PARAMETERS_HELPER:
        def __call__(self, *args, **kwargs):
            if FC_PARAMETERS_SINGLETON.instance is None:
                object = FC_PARAMETERS_SINGLETON()
                FC_PARAMETERS_SINGLETON.instance = object
            return FC_PARAMETERS_SINGLETON.instance
                
    Instance = FC_PARAMETERS_HELPER()
    
    def __init__(self):
        if not FC_PARAMETERS_SINGLETON.instance == None:
            raise RuntimeError('Only one instance of FC_PARAMETERS_SINGLETON is allowed!')
        else:
            self.__fcComponentParameters = COMPONENT_PARAMETERS(self.componentName)
            self.__fcGenericParameters = GENERIC_PARAMETERS()
            self.__fcFloggerParameters = FLOGGER_PARAMETERS(self.componentName)
        
    @property
    def fcComponentParameters(self):
        return self.__fcComponentParameters

    @property
    def fcGenericParameters(self):
        return self.__fcGenericParameters

    @property
    def fcFloggerParameters(self):
        return self.__fcFloggerParameters
    
    @property
    def componentName(self):
        return self.__componentName
    
    @componentName.setter
    def componentName(self, value):
        self.__componentName = value
