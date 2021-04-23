""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSODictToFrnDetailsDict.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSODictToFrnDetailsDict - 

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Responsible for transforming WSO formatted contract detail dictionaries to a multi layered Front Arena adapted contract IPF dictionary.
    Note: The three-layered dictionary is of the form {Contract_ID: {ContractDetail_ID: {ContractDetailIPF_ID: {ContractDetailIPFXML}, ...}, ...}, ...}.
    
-------------------------------------------------------------------------------------------------------"""

from FWSOUtils import WSOUtils as utils
from FWSODictAccessor import WSODictAccessor
from FWSOIPFCalculations import WSOIPFCalculations, ContractDetail
from FWSOUtils import WsoLogger

logger = WsoLogger.GetLogger()


class IPFPeriods(object):

    def __init__(self, contractIdContractDetailsDicts):
        self.contractIdContractDetailsDicts = contractIdContractDetailsDicts

    def _IPFDatesFromFile(self):
        ipfDatesFromFile = set()
        for contractDetailDicts in self.contractIdContractDetailsDicts.values():
            for contractDetailDict in contractDetailDicts.values():
                contractDetail = ContractDetail(contractDetailDict)
                ipfDates = contractDetail.IPFDatesSet()
                ipfDatesFromFile.update(ipfDates)
        return ipfDatesFromFile

    def _IPFPeriods(self, ipfDatesFromFileSorted):
        ipfPeriods = list()
        for i in range(len(ipfDatesFromFileSorted)-1):
            period = [ipfDatesFromFileSorted[i], ipfDatesFromFileSorted[i+1]]
            ipfPeriods.append(period)
        return ipfPeriods

    def GetPeriods(self):
        ipfDatesFromFile = self._IPFDatesFromFile()
        ipfDatesFromFileSorted = sorted(ipfDatesFromFile)
        ipfPeriods = self._IPFPeriods(ipfDatesFromFileSorted)
        return ipfPeriods


class ContractIdContractDetailIPFDictsCreator(object):

    CONTRACT_IPF_PREFIX = 'ContractIPF_ID_'

    def __init__(self, contractDict):
        self.contractDict = contractDict

    def ContractDicts(self):
        return WSODictAccessor.Contract()
    
    def ContractId(self):
        return self.contractDict.get('Contract_ID')

    def _ContractDetailIdsFromContractId(self, wsoContractDict):
        contractId = wsoContractDict.get('Contract_ID')
        contractDetailDicts = self.ContractDetailDicts()
        contractDetailIds = list()
        for contractDetailDict in contractDetailDicts.values():
            contractDetail = ContractDetail(contractDetailDict)
            if contractDetail.ContractId() == contractId:
                contractDetailIds.append(contractDetail.ContractIPFId())
        return contractDetailIds
    
    def _ContractIdContractDetailDicts(self):
        facilityId = self.contractDict.get('Contract_Facility_ID')
        contractIdContractDetailsDicts = dict()
        contractIds = set()
        wsoContractsDict = self.ContractDicts()
        for contractId, wsoContractDict in wsoContractsDict.items():
            if not wsoContractDict.get('Contract_Facility_ID') == facilityId:
                continue
            contractIds.add(contractId)
            contractDetailIds = self._ContractDetailIdsFromContractId(wsoContractDict)
            contractDetailDicts = self._GetContractDetailDictsFromIds(contractDetailIds)
            contractIdContractDetailsDicts[contractId] = contractDetailDicts
        return contractIdContractDetailsDicts
        
    @classmethod
    def ContractIPFPrefix(cls):
        return cls.CONTRACT_IPF_PREFIX
       
    def ContractDetailDicts(self):
        return WSODictAccessor.ContractDetail()

    def _GetContractDetailDictsFromIds(self, contractDetailIds):
        contractDetailDicts = self.ContractDetailDicts()
        contractDetailDictsReturn = dict()
        for contractDetailId in contractDetailIds:
            contractDetailDict = contractDetailDicts.get(contractDetailId)
            contractDetailDictsReturn[contractDetailId] = contractDetailDict
        return contractDetailDictsReturn

    def ContractIdContractDetailIPFDicts(self):
        contractIdContractDetailsDicts = self._ContractIdContractDetailDicts()
        contractDetailPrefix = self.ContractIPFPrefix()
        contractIdContractDetailsIpfDicts = dict()
        ipfPeriods = IPFPeriods(contractIdContractDetailsDicts).GetPeriods()
        for contractId, contractDetailDicts in contractIdContractDetailsDicts.items():
            contractIdContractDetailsIpfDicts[contractId] = contractDetailDicts
            for contractDetailId, contractDetailDict in contractDetailDicts.items():
                contractIdContractDetailsIpfDicts[contractId][contractDetailId] = contractDetailDict
                contractDetail = ContractDetail(contractDetailDict)
                contractIPFDicts = contractDetail.ConstructIPFSubPeriodDictionaries(contractDetailPrefix, ipfPeriods)
                for contractIPFDictId, contractIPFDict in contractIPFDicts.items():
                    contractIdContractDetailsIpfDicts[contractId][contractDetailId][contractIPFDictId] = contractIPFDict
        return contractIdContractDetailsIpfDicts
        

class WsoDictToFrnDetailsDict(object):
    ''' Class responsible for creating Front Arena adapted 
        contract IPF dictionaries. To be used primarily for 
        generating cashflows for each respective IPF period.'''
                
    def __init__(self, contractDict):
        self.contractIdContractDetailIPFDictsCreator = ContractIdContractDetailIPFDictsCreator(contractDict)
        self.contractIdContractDetailsIPFDicts = self._ConstructContractIdContractDetailContractIPFDictsPreInit()
        
    def _ConstructContractIdContractDetailContractIPFDictsPreInit(self):
        return self.contractIdContractDetailIPFDictsCreator.ContractIdContractDetailIPFDicts()
    
    def _ContractIdContractDetailsIPFDicts(self):
        return self.contractIdContractDetailsIPFDicts
    
    def _ContractDetailsIPFDicts(self):
        return self.contractIdContractDetailsIPFDicts.get(self._ContractId())
        
    def _ContractId(self):
        return self.contractIdContractDetailIPFDictsCreator.ContractId()
        
          
    '''Attribute methods. '''
    
    def CashFlowType(self):
        return 'Float Rate'
    
    def EndDate(self, ipfDict):
        return utils.AsDate(ipfDict.get('ContractIPF_DateTo'))  
    
    def NominalFactor(self, contractId, contractDetailId, ipfId, ipfDict, contractIdContractDetailsIpfDicts):
        return WSOIPFCalculations.ComputeIPFNominalFactor(contractId, contractDetailId, ipfId, ipfDict, contractIdContractDetailsIpfDicts)
    
    def PayDate(self, contractDetailDict):
        return utils.AsDate(contractDetailDict.get('Contract_MaturityDate'))
    
    def Spread(self, contractDetailDict):
        return utils.AsFloat(contractDetailDict.get('ContractIPF_Spread'))
    
    def StartDate(self, ipfDict):
        return utils.AsDate(ipfDict.get('ContractIPF_DateFrom'))
            
    def _ConstructFrnDetailsIPFDictionary(self):
        ''' Method responsible for constructing IPF dictionaries.'''
                      
        frnDetailsDict = dict()
        contractIdContractDetailsIpfDicts = self._ContractIdContractDetailsIPFDicts()
        contractId = self._ContractId()
        # Construct FA adapted IPF dictionary
        contractDetailsIpfDicts = self._ContractDetailsIPFDicts()
        for contractDetailId, contractDetailDict in contractDetailsIpfDicts.items():
            frnDetailsDict[contractDetailId] = {}
            for ipfId, ipfDict in contractDetailDict.items():
                if not ipfId.startswith(self.contractIdContractDetailIPFDictsCreator.ContractIPFPrefix()):
                    continue   
       
                frnIPFDetailDict = {
                    'CashFlowType': self.CashFlowType(),
                    'StartDate': self.StartDate(ipfDict),
                    'EndDate': self.EndDate(ipfDict),
                    'NominalFactor': self.NominalFactor(contractId, contractDetailId, ipfId, ipfDict, contractIdContractDetailsIpfDicts),
                    'PayDate': self.PayDate(contractDetailDict),
                    'Spread': self.Spread(contractDetailDict),
                }    
                
                frnDetailsDict[contractDetailId][ipfId] = frnIPFDetailDict
            
        return frnDetailsDict

    
    def FrnDetailsDict(self):
        ''' Public method for retrieving Front Arena adapted 
            contract IPF information. The return value is a 
            dictionary of dictionaries, where the outer keys are 
            contract detail ID:s and the inner keys are IPF ID:s.
            The innermost dictionaries contain IPF specific data. '''
    
        frnDetailDict = self._ConstructFrnDetailsIPFDictionary()
        return frnDetailDict
