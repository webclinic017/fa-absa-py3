""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSODictAccessor.py"
"""--------------------------------------------------------------------------
MODULE
    FWSODictAccessor

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

from FWSOUtils import MissingDataSourceException


def GetWSODictsCache():
    from FWSODirToWSODict import WSODirToWSODict
    return WSODirToWSODict()
    

class WSODictAccessor(object): 
    ''' Accessor class responsible for retrieving WSO
        data and passing it on to the caller.
    '''

    @classmethod
    def _WSODict(cls, wsoType):
        ''' Returns the WSO dict of the specified WSO type '''
        wsoDirToWsoDict = GetWSODictsCache()
        wsoDicts = wsoDirToWsoDict.WSODicts()
        wsoDict = wsoDicts.get(wsoType)
        if wsoDict == None:
            raise MissingDataSourceException('Cannot retrieve WSO data for %s. Verify that the data source exists.' % wsoType)
        return wsoDict
    
    @classmethod
    def AssetBase(cls):
        return cls._WSODict('Asset')
    
    @classmethod
    def Bank(cls):
        return cls._WSODict('Bank')
    
    @classmethod        
    def Contract(cls):
        return cls._WSODict('Contract')
        
    @classmethod
    def ContractDetail(cls):
        return cls._WSODict('ContractDetail')

    @classmethod
    def Facility(cls):
        return cls._WSODict('Facility')
        
    @classmethod
    def Issuer(cls):
        return cls._WSODict('Issuer')
    
    @classmethod    
    def Portfolio(cls):
        return cls._WSODict('Portfolio')
    
    @classmethod
    def Position(cls):
        return cls._WSODict('Position')
    
    @classmethod
    def Trade(cls):
        return cls._WSODict('Trade')
    
    @classmethod
    def TranCash(cls):
        return cls._WSODict('TranCash')
