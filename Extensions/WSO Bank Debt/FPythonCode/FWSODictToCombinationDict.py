""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSODictToCombinationDict.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSODictToCombinationDict - 

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Responsible for transforming a WSO formatted facility dictionary to Front Arena adapted combination dictionary.
    
-------------------------------------------------------------------------------------------------------"""

from FWSODictAccessor import WSODictAccessor

    
class WsoDictToAssetDict(object):

    def __init__(self, assetDict):
        self.assetDict = assetDict
        
    def _AssetId(self):
        return self.AssetDict().get('Asset_ID')
        
    def AssetDict(self):
        return self.assetDict
    
    def FacilityDict(self):
        raise NotImplementedError('Base class Asset does not support facilities.')
        
    def PositionIdsFromAssetId(self):
        assetId = self._AssetId()
        positionsDict = WSODictAccessor.Position()
        positionIds = set()
        for positionId, positionDict in list(positionsDict.items()):
            if not positionDict.get('Position_Asset_ID') == assetId:
                continue
            positionIds.add(positionId)
        return positionIds

class WsoDictToCombinationDict(WsoDictToAssetDict):
    
    def __init__(self, facilityDict):
        _assetDict = self._AssetDictFromFacilityDictPreInit(facilityDict)
        super(WsoDictToCombinationDict, self).__init__(_assetDict)
        self.facilityDict = facilityDict
    
    def _AssetDictFromFacilityDictPreInit(self, facilityDict):
        facilityAssetId = facilityDict.get('Facility_Asset_ID')
        assetDicts = WSODictAccessor.AssetBase()
        return assetDicts.get(facilityAssetId)
    
    def CurrencyByIdentifier(self):
        currency = self.AssetDict().get('CurrencyType_Identifier')
        return currency
        
    def FacilityDict(self):
        return self.facilityDict
        
    def _FacilityId(self):
        return self.FacilityDict().get('Facility_ID')
        
    def AssetId(self):
        return self._AssetId()
        
    def FacilityId(self):
        return self._FacilityId()
        
    def FacilityMaturity(self):
        return self.FacilityDict().get('Facility_Maturity')

    def Currency(self):
        return self.CurrencyByIdentifier()
        
    def _GetWSOFacilityPrefix(self):
        return 'WSO_Facility_'
        
    def ExternalId1(self):
        wsoFacilityPrefix = self._GetWSOFacilityPrefix()
        assetId = self.AssetId()
        return wsoFacilityPrefix + assetId

    def _GetWSOFacilityFreeText(self):
        return 'WSO_BankDebt'
        
    def _ContractFacilityId(self, contractDict):
        return contractDict.get('Contract_Facility_ID')
        
    def _ContractPositionId(self, contractDict):
        return contractDict.get('Position_ID')
        
    def ContractsInFacility(self):
        facilityId = self._FacilityId()
        contractDicts = WSODictAccessor.Contract()
        contractIds = set()
        for contractId, contractDict in list(contractDicts.items()):
            if not self._ContractFacilityId(contractDict) == facilityId:
                continue
            contractIds.add(contractId)
        return contractIds

    def FreeText(self):
        return self._GetWSOFacilityFreeText()
        
    def PositionIdsFromFacilityId(self):
        contractDicts = WSODictAccessor.Contract()
        contractIds = self.ContractsInFacility()
        positionIds = set()
        for contractId in contractIds:
            contractDict = contractDicts.get(contractId)
            positionIds.add(self._ContractPositionId(contractDict))
        return positionIds
        
    def ContractSize(self):
        return 1.0

    def ContractIdsFromFacilityId(self):
        contractsDict = WSODictAccessor.Contract()
        facilityId = self.FacilityId()
        matchingContractIds = []
        for contractId, contractDict in list(contractsDict.items()):
            if contractDict.get('Contract_Facility_ID') == facilityId:
                matchingContractIds.append(contractId)
        return matchingContractIds

    def CombinationDict(self):
        ''' assetDict = AssetBase dictionary (WSO format)
            facilityDict = Facility dictionary (WSO format)
            Returns combination dictionary to be used by factory.
        '''
        
        combinationDict = {
            'FA_Currency': self.Currency(),
            'FA_ContractSize': self.ContractSize(),
            'FA_FreeText': self.FreeText(),
            'FA_ExternalId1': self.ExternalId1(),
        }
        return combinationDict
