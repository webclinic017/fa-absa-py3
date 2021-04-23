""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOIPFCalculations.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSOIPFCalculations - 

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Responsible for creating Front Arena adapted IPF dictionaries and performing IPF computations. 
    
-------------------------------------------------------------------------------------------------------"""

from FWSOUtils import WSOUtils as utils
from FWSOUtils import WsoLogger

logger = WsoLogger.GetLogger()


class ContractDetail(object):

    def __init__(self, contractDetailDict):
        self.contractDetailDict = contractDetailDict

    def ContractId(self):
        return self.contractDetailDict.get('Contract_ID')    
        
    def ContractIPFId(self):
        return self.contractDetailDict.get('ContractIPF_ID')
        
    def ContractIPFStartDate(self):
        return utils.AsDate(self.contractDetailDict.get('ContractIPF_DateFrom'))

    def ContractIPFEndDate(self):
        return utils.AsDate(self.contractDetailDict.get('ContractIPF_DateTo'))
        
    def ContractDetailIPFSubAmount(self):
        return utils.AsFloat(self.contractDetailDict.get('ContractIPF_Amount'))
    
    def AddContractAmountForIPFPeriod(self, contractDetailDicts):
        contractDetail = ContractDetail(self.contractDetailDict)
        ipfStartDate = contractDetail.ContractIPFStartDate()
        ipfEndDate = contractDetail.ContractIPFEndDate()
        for contractDetailDict in list(contractDetailDicts.values()):
            contractDetail = ContractDetail(contractDetailDict)
            parallelContractStartDate = contractDetail.ContractIPFStartDate()
            parallelContractEndDate =  contractDetail.ContractIPFEndDate()
            if contractDetail.OriginalIPFPeriodOverlapsIPFSubPeriod(ipfStartDate, ipfEndDate, parallelContractStartDate, parallelContractEndDate):
                return contractDetail.ContractDetailIPFSubAmount()
        return 0.0
    
    @classmethod
    def ConstructIPFSubPeriodDictionaryFromOriginalContractDetailDict(cls, periodStartDate, periodEndDate):
        ipfSubDict = dict()
        ipfSubDict['ContractIPF_DateFrom'] = periodStartDate
        ipfSubDict['ContractIPF_DateTo'] = periodEndDate
        return ipfSubDict
    
    def IPFDatesSet(self):
        ipfDates = set()
        ipfDates.add(self.ContractIPFStartDate())
        ipfDates.add(self.ContractIPFEndDate())
        return ipfDates
    
    @classmethod
    def OriginalIPFPeriodOverlapsIPFSubPeriod(cls, ipfStartDate, ipfEndDate, parallelContractStartDate, parallelContractEndDate):
        return ipfStartDate >= parallelContractStartDate and ipfEndDate <= parallelContractEndDate
    
    def ConstructIPFSubPeriodDictionaries(self, contractDetailPrefix, ipfPeriods):
        contractIPFStartDate = self.ContractIPFStartDate()
        contractIPFEndDate = self.ContractIPFEndDate()
        ipfSubPeriodDict = dict()
        counter = 1
        for period in ipfPeriods:
            ipfPeriodStartDate = period[0]
            ipfPeriodEndDate = period[1]
            if self.OriginalIPFPeriodOverlapsIPFSubPeriod(ipfPeriodStartDate, ipfPeriodEndDate, contractIPFStartDate, contractIPFEndDate):
                primaryKey = contractDetailPrefix + str(counter) 
                ipfSubPeriodDict[primaryKey] = self.ConstructIPFSubPeriodDictionaryFromOriginalContractDetailDict(ipfPeriodStartDate, ipfPeriodEndDate)
                counter += 1
        return ipfSubPeriodDict


class WSOIPFCalculations(object):
    
    @classmethod
    def _TotalContractAmountForPeriod(cls, contractAmountForIPFPeriod):
        totalContractAmountForPeriod = 0.0
        for contractAmount in list(contractAmountForIPFPeriod.values()):
            totalContractAmountForPeriod += contractAmount
        return totalContractAmountForPeriod
    
    @classmethod
    def _ComputeGlobalIPFNominalAmountForPeriod(cls, contractId, contractDetailId, ipfSubId, ipfSubDict, contractIdContractDetailsSubDicts):
        contractDetailIPFSubDict = contractIdContractDetailsSubDicts.get(contractId).get(contractDetailId).get(ipfSubId)
        contractDetail = ContractDetail(contractDetailIPFSubDict)
        contractAmountForIPFPeriod = dict()
        for contractId, contractDetailDicts in list(contractIdContractDetailsSubDicts.items()):
            contractAmount = contractDetail.AddContractAmountForIPFPeriod(contractDetailDicts)
            contractAmountForIPFPeriod[contractId] = contractAmount
        totalContractAmountForPeriod = cls._TotalContractAmountForPeriod(contractAmountForIPFPeriod)
        return totalContractAmountForPeriod
    
    @classmethod
    def ComputeIPFNominalFactor(cls, contractId, contractDetailId, ipfSubId, ipfSubDict, contractIdContractDetailsSubDicts):
        contractDetailDicts = contractIdContractDetailsSubDicts.get(contractId)
        contractDetailDict = contractDetailDicts.get(contractDetailId)
        contractDetail = ContractDetail(contractDetailDict)
        contractDetailIPFSubAmount = contractDetail.ContractDetailIPFSubAmount()
        totalContractDetailIPFAmount = cls._ComputeGlobalIPFNominalAmountForPeriod(contractId, contractDetailId, ipfSubId, ipfSubDict, contractIdContractDetailsSubDicts)
        if not totalContractDetailIPFAmount:
            return 0.0
        ipfNominalFactor = utils.AsFloat(contractDetailIPFSubAmount/totalContractDetailIPFAmount)
        return ipfNominalFactor     
