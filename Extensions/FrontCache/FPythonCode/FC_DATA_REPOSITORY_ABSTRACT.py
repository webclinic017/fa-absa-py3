'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_REPOSITORY_ABSTRACT
PROJECT                 :       Front Cache
PURPOSE                 :       This is the abc for settlement and trade data repository
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       BBD
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
from abc import abstractmethod
from abc import ABCMeta


class FC_DATA_REPOSITORY_ABSTRACT(metaclass=ABCMeta):
    @abstractmethod
    def create(self, requestId, reportDate, settlementIndex, settlement):
        pass

    @abstractmethod
    def createSqlParams(self, requestId, reportDate, settlementIndex, settlement):
        pass
