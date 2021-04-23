'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_ABSTRACT
PROJECT                 :       Front Cache
PURPOSE                 :       ABC for FC_DATA_STL and FC_DATA_TRD
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       BBD
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

#*********************************************************#
#Importing Modules
#*********************************************************#
from abc import abstractmethod
from abc import ABCMeta


class FC_DATA_ABSTRACT(metaclass=ABCMeta):
    @abstractmethod
    def Calculate(self):
        pass

    @abstractmethod
    def Serialize(self):
        pass

    @abstractmethod
    def GetInfoAsXml(self):
        pass

    @abstractmethod
    def GetErrorsAsXml(self):
        pass
        
    
