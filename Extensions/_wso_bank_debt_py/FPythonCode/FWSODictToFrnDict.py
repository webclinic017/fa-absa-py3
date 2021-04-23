""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSODictToFrnDict.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSODictToFrnDict - 

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Responsible for transforming a WSO formatted contract dictionay to a Front Arena adapted FRN dictionary.
    
-------------------------------------------------------------------------------------------------------"""

from FWSOUtils import WSOUtils as utils
from FWSODictAccessor import WSODictAccessor
from FWSODictToCombinationDict import WsoDictToCombinationDict        
import FWSOHooks as WSOHooks
        
class WsoDictToFrnDict(object): 

    def __init__(self, frnDict):
        self.frnDict  = frnDict
    
    def _AsSpread(self, spread):
        return 100.0*utils.AsFloat(spread) # Percent

    def _AsDayCountMethod(self):
        monthCount = self._Contract().get('MonthCountName')
        yearCount = self._Contract().get('YearCountName')
        return monthCount.title() + '/' + yearCount
        
    def DayCountMethod(self):
        return self._AsDayCountMethod()

    def _DaysBetweenDates(self, startDateLong, endDateLong):
        ''' Returns the number of days between two dates '''
        from datetime import datetime
        startDate = utils.AsDate(startDateLong)
        endDate = utils.AsDate(endDateLong)
        startDateAsDate = datetime.strptime(startDate, '%Y-%m-%d')
        endDateAsDate = datetime.strptime(endDate, '%Y-%m-%d')
        daysDatetime = endDateAsDate - startDateAsDate
        days = daysDatetime.days
        return days
        
    def _EndDate(self):
        facilityDict = self.FacilityDict()
        wsoDictToCombDict = WsoDictToCombinationDict(facilityDict)
        endDate = wsoDictToCombDict.FacilityMaturity()
        return utils.AsDate(endDate)

    def EndDate(self):
        return self._EndDate()

    def _AssetId(self):
        facilityDict = self.FacilityDict()
        return facilityDict.get('Facility_Asset_ID')

    def _Contract(self):
        return self.frnDict

    def _ContractId(self):
        return self._Contract().get('Contract_ID')
    
    def _ContractFacilityId(self):
        return self._Contract().get('Contract_Facility_ID')
        
    def _CurrencyByIdentifier(self):
        return self._Contract().get('Contract_CurrencyType_Identifier')
        
    def _ContractExternalId1Prefix(self):
        return 'WSO_Contract_'
        
    def _ContractAmount(self):
        return self._Contract().get('Contract_Amount')
        
    def _ExternalContractPositionId(self, externalContractDict):
        return externalContractDict.get('Position_ID')   

    def _ExternalContractAmount(self, externalContractDict):
        return externalContractDict.get('Contract_Amount')
        
    def ContractDicts(self):
        return WSODictAccessor.Contract()
        
    def FacilityDicts(self):
        return WSODictAccessor.Facility()
        
    def FacilityDict(self):
        facilityDicts = self.FacilityDicts()
        facilityId = self._ContractFacilityId()     
        facilityDict = facilityDicts.get(facilityId)
        return facilityDict
        
    def Currency(self):
        return self._CurrencyByIdentifier()
        
    def _FrnNamePrefix(self):
        return 'Contract_'
        
    def _FrnName(self):        
        contractId = self._ContractId()
        prefix = self._FrnNamePrefix()
        return prefix + contractId
    
    def FrnName(self):
        return self._FrnName()
        
    def FreeText(self):
        return 'WSO_BankDebt'
        
    def ExternalId1(self):
        contractPrefix = self._ContractExternalId1Prefix()
        contractId = self._ContractId()
        return contractPrefix + contractId
        
    def OriginalNominalAmount(self):
        contractAmount = utils.AsFloat(self._ContractAmount())
        totalAmount = self.TotalFacilityAmountFromPositionIds()
        if not totalAmount:
            return 0.0
        return contractAmount/totalAmount

    def NominalAmount(self):
        return 1.0
                
    def StartDate(self):
        return utils.AsDate(self._Contract().get('Contract_StartDate'))
        
    def TotalFacilityAmountFromPositionIds(self):
        facilityDict = self.FacilityDict()
        wsoDictToCombDict = WsoDictToCombinationDict(facilityDict)
        positionIds = wsoDictToCombDict.PositionIdsFromFacilityId()   
        contractsDict = self.ContractDicts()
        globalAmount = 0.0
        for contractDict in list(contractsDict.values()):
            if not self._ExternalContractPositionId(contractDict) in positionIds:
                continue
            globalAmount += utils.AsFloat(self._ExternalContractAmount(contractDict))
        return globalAmount
        
    def _RollingPeriod(self):
        contractDict = self._Contract()
        startDate = contractDict.get('Contract_StartDate')
        endDate = contractDict.get('Contract_MaturityDate')
        numberOfDays = self._DaysBetweenDates(startDate, endDate)
        rollingPeriod = str(numberOfDays) + 'd'
        return rollingPeriod    
    
    def RollingPeriod(self):
        return self._RollingPeriod()
        
    def RollingPeriodBase(self):
        return utils.AsDate(self._Contract().get('Contract_NextPaymentDate'))
        
    def Spread(self):
        return self._AsSpread(self._Contract().get('Contract_Spread'))
        
    def FrnDict(self):
        ''' Takes a contract dictionary and returns an FRN dictionary.
        '''        
        
        frnDict = {
            # Methods on FRN
            'FA_Name': self.FrnName(),
            'FA_NominalAmount': self.NominalAmount(),
            'FA_Currency': self.Currency(),
            'FA_ExternalId1': self.ExternalId1(),
            'FA_FreeText': self.FreeText(),
        }

        return frnDict
        
    def FrnLegDict(self):
    
        frnLegDict = {
            # Leg methods
            'Leg.Currency': self.Currency(),
            'Leg.DayCountMethod': self.DayCountMethod(),
            'Leg.EndDate': self.EndDate(),
            'Leg.FloatRateReference': WSOHooks.HookOrDefault.RateIndexName(self._Contract()),
            'Leg.RollingPeriod': self.RollingPeriod(),
            'Leg.RollingPeriodBase': self.RollingPeriodBase(),
            'Leg.Spread': self.Spread(),
            'Leg.StartDate': self.StartDate(),
        }
        
        return frnLegDict