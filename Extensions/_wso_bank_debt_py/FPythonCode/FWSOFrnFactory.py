""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOFrnFactory.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSOFrnFactory -

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION


-------------------------------------------------------------------------------------------------------"""

import acm
from FWSOUtils import WsoLogger

logger = WsoLogger.GetLogger()


class FrnFactory(object):

    def __init__(self, frn, frnLegDict):
        self.frn = frn
        self.leg = self.frn.FirstFloatLeg()
        self.frnLegDict = frnLegDict

    def _IsLegMethod(self, methodName):
        return methodName.startswith('Leg.')

    def _LegMethod(self, methodName):
        ''' All leg-methods in the dictionary starts with "Leg." to distinguish them
            from the FRN-methods. Returns the actual name of the Leg-method (without "Leg.").
        '''
        return methodName.split('Leg.')[1] if self._IsLegMethod(methodName) else None

    def _CallSetMethodWithValue(self, subject, methodName, value):
        setMethod = getattr(subject, methodName)
        try:
            setMethod(value)
            logger.debug('Successfully set value %s on attribute %s.' % (value, methodName))
        except Exception:
            raise Exception('Failed to set value %s on attribute %s.' % (value, methodName))

    def _SetAttributesOnLeg(self):
        for methodName, value in self.frnLegDict.items():
            legMethodName = self._LegMethod(methodName)
            self._CallSetMethodWithValue(self.leg, legMethodName, value)
            
    def _AutoGenerateCashflows(self):
        logger.debug('Auto generating cashflows for FRN %s.' % self.frn.Name())
        self.leg.GenerateCashFlows(0.0)
        if not self.leg.CashFlows().Size() > 0:
            raise Exception('Failed to auto generate future cashflows for FRN %s.' % self.frn.Name())
        logger.debug('Auto generated %d cashflows.' % self.leg.CashFlows().Size() )
            
    def _DayCountMethod(self):
        return self.frnLegDict.get('Leg.DayCountMethod')
        
    def _Currency(self):
        return self.frnLegDict.get('Leg.Currency')
        
    def _RateIndexName(self):
        return self.frnLegDict.get('Leg.FloatRateReference')
        
    def _LegStartDate(self):
        return self.frnLegDict.get('Leg.StartDate')
        
    def _LegEndDate(self):
        return self.frnLegDict.get('Leg.EndDate')
        
    def _NextPaymentDay(self):
        return self.frnLegDict.get('Leg.RollingPeriodBase')
                
    def _RemoveCashFlowResets(self, cashflow):
        for reset in reversed(cashflow.Resets()):
            cashflow.Resets().Remove(reset)
            logger.debug('Deleting reset on cashflow %s.' % cashflow.Oid())
            if not reset.IsDeleted():
                reset.Delete()

    def _ValidateAttributesToSetOnLeg(self):
        isInconsistentDates = bool(self._LegEndDate() < self._LegStartDate())
        if isInconsistentDates:
            raise Exception('FRN %s start date (%s) occur after maturity date (%s).' % (self.frn.Name(), self._LegStartDate(), self._LegEndDate()))
    
    def _IsCashflowDatesSameAsForLeg(self, cashflow):
        cashflowStartDate = cashflow.StartDate()
        cashflowEndDate = cashflow.EndDate()
        legStartDate = self._LegStartDate()
        nextPaymentDay = self._NextPaymentDay()
        return (cashflowStartDate == legStartDate) and (cashflowEndDate == nextPaymentDay)

    def _RaiseErrorIfNoRateIndexName(self):
        if not self._RateIndexName():
            raise Exception('No proper rate index provided for %s.' % self.frn.Name())

    def _RaiseErrorIfNoRateIndex(self):
        rateIndexName = self._RateIndexName()
        rateIndex = acm.FRateIndex[rateIndexName]
        if not rateIndex:
            raise Exception('The float rate reference %s does not exist.' % rateIndexName)
        logger.debug('The float rate reference %s was found in the ADS.' % rateIndexName)
        return rateIndex

    def ClearRedundantCashFlowFromActiveContract(self):
        for cashflow in self.leg.CashFlows().AsList():
            if not self._IsCashflowDatesSameAsForLeg(cashflow):
                continue
            logger.debug('Deleting redundant cashflow with start date %s and end date %s, respectively, for FRN %s.' % (cashflow.StartDate(), cashflow.EndDate(), self.frn.Name()))
            self._RemoveCashFlowResets(cashflow)
            if not cashflow.IsDeleted():
                self.leg.CashFlows().Remove(cashflow)
                cashflow.Delete() 

    def UpdateLeg(self):
        logger.debug('Updating FRN %s.' % self.frn.Name())     

        if self.frn.Quotation() != 'Clean':
            self.frn.Quotation('Clean')
            logger.debug('FRN quotation was set to Clean.')

        self._ValidateAttributesToSetOnLeg()
        self._SetAttributesOnLeg()

        # Check that float rate reference exists in the ADS
        self._RaiseErrorIfNoRateIndexName()
        self._RaiseErrorIfNoRateIndex()

        self._AutoGenerateCashflows()
