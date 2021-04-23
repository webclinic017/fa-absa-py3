""" Compiled: 2017-11-06 12:31:15 """

#__src_file__ = "extensions/ConvertiblePricingAndRisk/etc/FAscotUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FAscotUtils

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Helper module to set up a recall swap to be used within the theoretical pricing regime for Ascots.

-------------------------------------------------------------------------------------------------------"""

import acm
import FAssetManagementUtils
from FAscotValuationFunctions import GetRecallSwap
logger = FAssetManagementUtils.logger

def _IsAscot(eii):
    ascot = _InsFromExtObj(eii)
    if not ascot:
        return
    if not (ascot.IsKindOf(acm.FOption) and ascot.Underlying().IsKindOf(acm.FConvertible)):
        logger.error('Selected instrument is not an ascot (option) written on a convertible.')
        return
    return ascot

def _InsFromExtObj(eii):
    instruments = FAssetManagementUtils.GetInstruments(eii)
    if not instruments:
        logger.error('No instrument selected.')
        return
    ins = instruments[0]
    if not hasattr(ins, 'Underlying'):
        logger.error('Selected instrument has no underlying.')
        return
    return ins

class SwapFromConvertibleCreator(object):
    ''' Helper class responsible for creating a swap based on a convertible. '''

    def __init__(self, convertible):
        self.convertible = convertible

    @classmethod
    def _CreateSwapFromLeg(cls, leg):
        return leg.CreateAssetSwap(None)

    @classmethod
    def _GetDefaultFloatRateReference(cls, leg):
        curr = leg.Currency().Name()
        ri = acm.FRateIndex.Select('currency=%s'%curr)
        if ri.IsEmpty():
            return None
        return ri[0]

    @classmethod
    def _SetupRecLegOfSwapFromLeg(cls, swap, fromLeg):
        # Setup the receive leg using the (convertible) leg as template
        recLeg = swap.RecLeg()
        recLeg.NominalFactor(fromLeg.NominalFactor())
        recLeg.NominalAtStart(False)
        recLeg.NominalAtEnd(False)
        recLeg.LongStub(fromLeg.LongStub())
        recLeg.Currency(fromLeg.Currency())
        recLeg.DayCountMethod(fromLeg.DayCountMethod())
        recLeg.FixedRate(fromLeg.FixedRate())
        recLeg.FixedCoupon(False)
        recLeg.LegType(fromLeg.LegType())
        recLeg.FloatRateReference(fromLeg.FloatRateReference())
        recLeg.FloatRateFactor(fromLeg.FloatRateFactor())
        recLeg.RollingPeriod(fromLeg.RollingPeriod())
        recLeg.RollingPeriodBase(fromLeg.RollingPeriodBase())
        return recLeg

    @classmethod
    def _RemoveAllCashflows(cls, leg):
        for cashflow in reversed(leg.CashFlows()):
            cashflow.Delete()

    @classmethod
    def _CashflowsToCopy(cls, fromLeg, minDate, maxDate):
        cashflowsToCopy = list()
        if not maxDate:
            maxDate = fromLeg.EndDate()
        for cashflow in fromLeg.CashFlows():
            if cls._NoCopyCashFlow(cashflow, minDate, maxDate):
                continue
            cashflowsToCopy.append(cls._AdjustCashFlowStartDate(cls._Clone(cashflow), minDate))
        return cashflowsToCopy
        
    @classmethod
    def _Clone(cls, cashflow):
        return cashflow.Clone()

    @classmethod
    def _AdjustCashFlowStartDate(cls, cf, minDate):
        cf.StartDate(max(cf.StartDate(), minDate))
        return cf

    @classmethod
    def _NoCopyCashFlow(cls, cashflow, minDate, maxDate):
        payDate = cashflow.PayDate()
        return (cashflow.CashFlowType() in ('Fixed Amount',)) or (maxDate < payDate) or (minDate > payDate)

    @classmethod
    def _SubstituteCashflows(cls, recLeg, templateCashflows):
        ''' Create new cashflows and remove the old ones.
        '''
        newCashflows = list()
        # Create new cashflows
        for templateCashflow in templateCashflows:
            newCashflow = recLeg.CreateCashFlow()
            newCashflow.Apply(templateCashflow)
            newCashflows.append(newCashflow)
        # Remove the old cashflows (reverse needed to ensure all cashflows are removed)
        for cashflow in reversed(recLeg.CashFlows()):
            if cashflow.Oid() not in [newCashflow.Oid() for newCashflow in newCashflows]:
                cashflow.Delete()
        return newCashflows

    @classmethod
    def _SetupPayLegOfSwap(cls, swap):
        payLeg = swap.PayLeg()
        payLeg.LegType('Float')        
        payLeg.NominalFactor(1.0)
        payLeg.FloatRateFactor(1.0)
        payLeg.ResetType('Single')
        payLeg.FixedRate(0.0)
        payLeg.Spread(0.0)
        payLeg.DayCountMethod('Act/360')
        payLeg.PayDayMethod('Following')
        payLeg.LongStub(False)
        floatRateReference = cls._GetDefaultFloatRateReference(payLeg)
        payLeg.FloatRateReference(floatRateReference)
        if floatRateReference:
            payLeg.RollingPeriod(floatRateReference.Legs()[0].EndPeriod())
        else:
            payLeg.RollingPeriod('6m')
        return payLeg

    def _SetQuotation(self, irs, defaultQuotation = True):
        # Only default quotation supported at the moment
        if defaultQuotation:
            irs.Quotation(self.Convertible().Quotation())

    def _SetRollingPeriodToZeroIfNoCashflows(self, leg):
        ''' In order to avoid auto-generation of all cashflows when
            no cashflows are present, rolling period is set to zero.
        '''
        if leg.CashFlows().Size() == 0:
            self._SetRollingPeriodToZero(leg)

    def _SetRollingPeriodToZero(self, leg):
        leg.RollingPeriod('0d')

    def _AdjustDates(self, swap, endDate, spotBankingDaysOffset):
        recLeg = swap.RecLeg()
        payLeg = swap.PayLeg()
        if spotBankingDaysOffset:
            swap.SpotBankingDaysOffset(spotBankingDaysOffset)
        recLeg.EndDate(endDate)
        payLeg.EndDate(endDate)
        
    def _CreateFixedAmountCashFlow(self, recLeg):
        cashflow = recLeg.CreateCashFlow()
        cashflow.CashFlowType = 'Fixed Amount'
        cashflow.NominalFactor(1.0)
        cashflow.Leg = recLeg   
        return cashflow   

    def _AdjustReceiveLegIfCBHasPutEvent(self, receiveLeg, cbPutEvent): 
        if cbPutEvent:
            cashflow = self._CreateFixedAmountCashFlow(receiveLeg)
            cashflow.FixedAmount = self._NormalizedStrikeAmount(cbPutEvent)            
            cashflow.PayDate = cbPutEvent.Date()
            
    def _AdjustReceiveLegAtExpiry(self, recLeg, ascotExpiryDate):
        cfs = self._CBFixedAmountCashflows()
        numCfs = len(cfs)
        fixedAmount = 0.0
        if numCfs == 2:
            # Case 1: Redemption cashflow split
            for cf in cfs:
                if abs(cf.FixedAmount() - 1.0) > 1e-6:
                    fixedAmount = cf.FixedAmount()
                    break
        elif numCfs == 1:
            # Case 2: No redemption cashflow split
            fixedAmount = cfs[0].FixedAmount() - 1.0
        if fixedAmount:
            cashflow = self._CreateFixedAmountCashFlow(recLeg)
            cashflow.FixedAmount = fixedAmount
            cashflow.PayDate = ascotExpiryDate
                
    def _NormalizedStrikeAmount(self, putEvent):
        return putEvent.Strike()/100 - 1                
                
    def _AscotExpiryDate(self, recLeg):
        return recLeg.EndDate()                
            
    def _CBFixedAmountCashflows(self):
        return [cf for cf in self.Convertible().Legs().First().CashFlows() if cf.CashFlowType() == 'Fixed Amount']        
        
    def _ExerciseEventsSorted(self):
        ees = acm.FArray()
        if self.Convertible().Putable():
            constraint = 'instrument="' + self.Convertible().Name() + '" and type = "Put"'
            ees.AddAll(acm.FExerciseEvent.Select(constraint).SortByProperty('expiryDate'))
        return ees
        
    def _GenerateCashFlowsForLeg(self, leg):
        leg.GenerateCashFlows(0.0)     

    def _AddFixedAmountCashFlowToRecLeg(self, recLeg):
        ''' If applicable, add a cashflow corresponding to the excess spread of the
            put option on the next put date of the convertible. This cashflow will 
            effect the recall price of the swap, since the swap agreement is terminated 
            if the  convertible is exercised. Put cashflows are calculated as 
            Put Price/100 - 1.

            If no such put event exists, the excess yield with respect to the redemption 
            amount as of the maturity date of the asset swap is taken. This cashflow will 
            effect the recall price of the swap, since the swap agreement is terminated if 
            the  convertible is exercised.
        '''       
        cbPutEvents = self._ExerciseEventsSorted()
        ascotExpiryDate = self._AscotExpiryDate(recLeg)
        fixedPutEvent = None
        if ascotExpiryDate > acm.Time.DateToday():
            if not cbPutEvents.IsEmpty():
                for cbPutEvent in cbPutEvents:
                    if cbPutEvent.ExpiryDate() == ascotExpiryDate:
                        fixedPutEvent = cbPutEvent
                        break
            if fixedPutEvent:
                self._AdjustReceiveLegIfCBHasPutEvent(recLeg, fixedPutEvent)
            elif self.Convertible().ExpiryDateOnly() == ascotExpiryDate:
                self._AdjustReceiveLegAtExpiry(recLeg, ascotExpiryDate)
        
    def Convertible(self):
        return self.convertible    

    def CreateSwap(self, endDate = None, spotBankingDaysOffset = None):
        ''' Creates a swap. The cashflows of the convertible are copied to
            the receive leg. Pay leg is defined in _SetupPayLegOfSwap,
            except its float rate reference (defined externally). The swap
            is not committed.
        '''
        cbLeg = self.Convertible().Legs().First()
        swap = self._CreateSwapFromLeg(cbLeg)
        self._SetQuotation(swap)
        # Receive leg of swap
        recLeg = self._SetupRecLegOfSwapFromLeg(swap, cbLeg)
        self._AddFixedAmountCashFlowToRecLeg(recLeg)
        self._SetRollingPeriodToZeroIfNoCashflows(recLeg)
        # Pay leg of swap
        self._SetupPayLegOfSwap(swap)
        self._AdjustDates(swap, endDate, spotBankingDaysOffset)
        swap.Name = swap.SuggestName()
        return swap

    def UpdateSwapFromCB(self, swap):
        ''' Applicable to accretion style convertibles '''
        cbLeg = self.Convertible().Legs().First()
        recLeg = swap.RecLeg()
        self._RemoveAllCashflows(recLeg)
        minDate = recLeg.StartDate()
        maxDate = recLeg.EndDate()
        templateCashflows = self._CashflowsToCopy(cbLeg, minDate, maxDate)
        self._SubstituteCashflows(recLeg, templateCashflows)
        self._AddFixedAmountCashFlowToRecLeg(recLeg)
        self._SetRollingPeriodToZero(recLeg)
        return swap

    def GenerateCashFlowsForPayLeg(self, payLeg):
        self._GenerateCashFlowsForLeg(payLeg)

    def GenerateCashFlowsForReceiveLeg(self, recLeg):
        self._GenerateCashFlowsForLeg(recLeg)
        self._AddFixedAmountCashFlowToRecLeg(recLeg)

'''Function for updating swap from option ins def'''
def GetRecallSwapCashFlowsFromConvertible(extObj):
    ascots = FAssetManagementUtils.GetInstruments(extObj)
    for ascot in ascots:
        if hasattr(ascot, 'Underlying'):
            cb = ascot.Underlying()
        else:
            logger.DLOG("Failed to copy cash flows - No instrument selected")
            return
        if not cb.IsKindOf(acm.FConvertible):
            logger.DLOG("Failed to copy cash flows - Underlying is not a convertible")
            return
        swap = GetRecallSwap(ascot)
        if not swap:
            logger.DLOG("Failed to copy cash flows - Could not find recall swap")
            return
        SwapFromConvertibleCreator(cb).UpdateSwapFromCB(swap)
        swap.Commit()

'''Functions for opening other applications from an instrument definition'''
def OpenRecallSwapThroughInsDef(eii):
    ascot = _IsAscot(eii)
    if not ascot:
        return
    recallSwap = GetRecallSwap(ascot)
    if not recallSwap:
        logger.error('Could not retrieve recall swap from Ascot %s' % ascot.Name())
        return
    acm.StartApplication('Instrument Definition', recallSwap)
