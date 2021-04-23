""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendHandler.py"

"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendHandler

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Business logic for creating / modifying security loans. Private classes.
------------------------------------------------------------------------------------------------"""

import acm
from DealDevKit import ReturnDomainDecorator
from ACMPyUtils import Transaction

sentinel = object()

class SecurityLoanMoneyFlowsCalculationCache(object):
    def __init__(self):
        self.resets = acm.FDictionary()
        self.maxResets = 100
        self.calcSpaceCollection = None
        self.calcSpace = None
    
    def Clear(self):
        self.resets.Clear()
        self.calcSpace = None

    def Stamp(self, reset):
        stamp = str(reset.Leg())
        for r in reset.CashFlow().Resets():
            stamp = stamp + str(r)
        return stamp

    def Add(self, reset):
        self.resets.AtPut(reset, self.Stamp(reset))

    def CalcSpace(self, reset):
        if reset in self.resets:
            resets = self.resets[reset]
            if resets != self.Stamp(reset):
                self.Clear()
                self.Add(reset)
        else:
            if len(self.resets) > self.maxResets:
                self.Clear()
            self.Add(reset)
            
        if not self.calcSpace:
            self.calcSpaceCollection = acm.Calculations().CreateCalculationSpaceCollection()
            self.calcSpace = self.calcSpaceCollection.GetSpace('FMoneyFlowSheet', acm.GetDefaultContext())
        
        return self.calcSpace
    
    def CalcValue(self, reset, column):
        calculation = self.CalcSpace(reset).CreateCalculation(reset, column, None)
        return calculation.Value().Number() if calculation.Value().IsNumber() else acm.Math().NotANumber()

class FxRateCalcCache(object):
    def __init__(self):
        self._currPairs = acm.FDictionary()
        self._calcSpaceCollection = acm.Calculations().CreateStandardCalculationsSpaceCollection()

    def CreateCacheKey(self, fromCurr, toCurr):
        return str(fromCurr.Name() + '/' + toCurr.Name())
        
    def FXRateFromCache(self, fromCurr, toCurr, date):
        fxRate = None
        cacheKey = self.CreateCacheKey(fromCurr, toCurr)
        dateCache = self._currPairs.At(cacheKey)
        if dateCache:
            fxRate = dateCache.At(date)
        return fxRate
        
    def FXRateToCache(self, fromCurr, toCurr, date, fxRate):
        cacheKey = self.CreateCacheKey(fromCurr, toCurr)
        dateCache = self._currPairs.At(cacheKey)
        if not dateCache:
            dateCache = acm.FDictionary()
            self._currPairs.AtPut(cacheKey, dateCache)
        dateCache.AtPut(date, fxRate)
        
    def CalcFXRate(self, fromCurr, toCurr, date):
        fxRate = 1
        try: 
            fxRate = fromCurr.Calculation().FXRate(self._calcSpaceCollection, toCurr, date).Number()
        except:
            pass
        return fxRate
        
    def FXRate(self, fromCurr, toCurr, date):
        fxRate = self.FXRateFromCache(fromCurr, toCurr, date)
        if fxRate is None:
            fxRate = self.CalcFXRate(fromCurr, toCurr, date)
            self.FXRateToCache(fromCurr, toCurr, date, fxRate)
        return fxRate
        
# Utility class that provides functionalities to handle Security Loans Instruments.
class SecurityLoanHandler(object):

    def __init__(self, instrument):
        self.instrument = instrument
        self.calcCache = SecurityLoanMoneyFlowsCalculationCache()

    def CalcValue(self, calcObject, column):
        return self.calcCache.CalcValue(calcObject, column)

    def ReceiveLeg(self):
        return self.Instrument().FirstReceiveLeg()

    def PayLeg(self):
        return self.Instrument().FirstPayLeg()

    def Legs(self):
        if self.Instrument().FirstReceiveLeg():
            return [self.Instrument().FirstPayLeg(), self.Instrument().FirstReceiveLeg()]
        else:
            return [self.Instrument().FirstPayLeg()]

    def RebateLeg(self):
        return self.ReceiveLeg()

    def Instrument(self):
        return self.instrument

    # Returns a wrapper to set/get the fee
    def FeePayLeg(self):
        return SecurityLoanLegHandler(self.PayLeg())

    def FeeReceiveLeg(self):
        return SecurityLoanLegHandler(self.ReceiveLeg())

    def FeeRebateLeg(self):
        return SecurityLoanLegHandler(self.RebateLeg())

    # -------------   Rebate related functions -------------
    def IsRebate(self, value='NoValue', *args):
        if value == 'NoValue':
            prodType = self.Instrument().ProductTypeChlItem()
            if (prodType is not None) and (prodType.StringKey() == 'Rebate Security Loan'):
                return True
            else:
                return False
        elif value is True and self.IsRebate() is False:
            daycountMethod = self.PayLeg().DayCountMethod()
            self.Instrument().ProductTypeChlItem = 'Rebate Security Loan'
            self.HasCashCollateralPool(True)
            self.FeeRebateLeg().StartingFee(-self.FeePayLeg().StartingFee())
            self.PayLeg().LegType = 'Fixed'
            self.PayLeg().NominalScaling = 'Initial Price'
            self.PayLeg().FixedRate = 0
            self.PayLeg().RollingPeriod = '0d'
            self.PayLeg().DayCountMethod = daycountMethod
            self.ReceiveLeg().NominalScaling = 'Initial Price'
            self.SpreadFixings(self.PayLeg(), False)
            
        elif value is False and self.IsRebate() is True:
            self.Instrument().ProductTypeChlItem = None
            self.PayLeg().NominalScaling = 'Price'
            self.PayLeg().InitialIndexValue(0.0)
            if self.PayLeg().IndexRef() and self.PayLeg().IndexRef().Currency() != self.PayLeg().Currency():
                self.PayLeg().IndexRefFXFixingType = 'Explicit'
            else:
                self.PayLeg().IndexRefFXFixingType = 'None'
            self.PayLeg().RollingPeriod = self.ReceiveLeg().RollingPeriod()
            self.PayLeg().IndexRefFixingDateRule = self.GetOrCreateDefaultIndexRefFixingDateRule(self.Instrument().Underlying())
            self.PayLeg().FloatRateFactor2 = 1.0
            self.PayLeg().ResetDayOffset(-self.PayLeg().Currency().Calendar().SpotBankingDays())
            
            self.HasCashCollateralPool(False)
            self.SpreadFixings(self.PayLeg(), True)


    def SpreadFixings(self, leg, spreadFixings):
        leg.GenerateSpreadFixings(spreadFixings)
        self.RegenerateCashFlows(False)

    def IsFloatRebate(self, *args):
        return self.IsRebate() and self.RebateLeg().LegType() == 'Float'

    def GetLegCurrentSingleReset(self, leg):
        current = None
        for cf in leg.CashFlows().SortByProperty('StartDate'):
            if (cf.StartDate() > acm.Time.DateToday()) and current is not None:
                break
            for reset in cf.Resets():
                if reset.ResetType() == 'Single':
                    current = reset
                    break
        return current

    def GetSuggestedReferenceRate(self, leg):
        currentReset = self.GetLegCurrentSingleReset(leg)
        if currentReset is not None:
            if currentReset.IsFixed():
                return currentReset.FixFixingValue()
            else:
                value = self.CalcValue(currentReset,  'Cash Analysis Fixing Estimate')
                if acm.Math.IsFinite(value):
                    return value
        return 0

    def RebateRate(self, value='NoValue'):
        if self.IsRebate():
            if value == 'NoValue':
                if self.RebateLeg().FloatRateReference():
                    return self.FeeRebateLeg().Fee() + self.GetSuggestedReferenceRate(self.RebateLeg())
                else:
                    return acm.Math.NotANumber()
            else:
                if self.RebateLeg().FloatRateReference():
                    self.FeeRebateLeg().Fee(value - self.GetSuggestedReferenceRate(self.RebateLeg()))

    def RebatePrice(self, value='NoValue'):
        if self.IsRebate():
            if value == 'NoValue':
                if self.RebateLeg().InitialIndexValue():
                    return self.RebateLeg().InitialIndexValue() * self.RebateLeg().NominalFactor()
                else:

                    return self.RebateLeg().SuggestInitialIndexValue() * self.RebateLeg().NominalFactor()
            else:
                for l in self.Legs():
                    l.InitialIndexValue = value / self.RebateLeg().NominalFactor()

    # -------------  Helper methods for programmatic access  -------------

    def Security(self, value='NoValue'):
        if value == 'NoValue':
            return self.Instrument().Underlying()
        else:
            if self.Instrument().Underlying() != value:
                self.Instrument().Underlying = value
                self.Instrument().Currency = self.Security().Currency()
            for l in self.Legs():
                l.IndexRef = value
                l.InitialIndexValue = l.SuggestInitialIndexValue()

    def LegNeedsFxReset(self, leg):
        return leg.IndexRef() and leg.IndexRef().Currency() != leg.Currency() and leg.NominalScaling() == 'Price'

    def GetLegInitialReset(self, leg, resetType):
        resets = leg.Resets().SortByProperty('Day', False)
        first = None
        for reset in resets:
            if reset.ResetType() == resetType and (not first or (acm.Time().DateNow() < reset.EndDate() and  reset.Day() < first.Day())):
                first = reset
        return first

    def GetLegInitialIndexFXReset(self, leg):
        return self.GetLegInitialReset(leg, 'Index Reference FX')
        
    def GetLegInitialNominalScalingReset(self, leg):
        return self.GetLegInitialReset(leg, 'Nominal Scaling')

    def SetInitialPrices(self, value):
        for l in self.Legs():
            l.InitialIndexValue = value
            self.LegInitialIndexNominalScalingEstimate(l, value)

    def FixSpreadResets(self, oldFee, newFee, rerateDate):
        for leg in self.Legs():
            for cf in leg.CashFlows():
                for r in cf.Resets():
                    if r.ResetType() == 'Spread' and not r.IsFixed() and r.Day() < rerateDate:
                        r.FixFixingValue = oldFee
                    elif  r.ResetType() == 'Spread' and r.IsFixed() and r.Day() > rerateDate:
                        r.FixFixingValue = newFee

    # Defined in Deal Definition SecurityLoan_DP.
    def LegInitialIndexFXEstimate(self, leg, value='NoValue'):
        assert leg, 'No leg'
        first = self.GetLegInitialIndexFXReset(leg)
        if value == 'NoValue':
            initialFX = 0.0
            if first:
                if first.IsFixed():
                    initialFX = first.FixingValue()
                else:
                    try:
                        initialFX = self.CalcValue(first,  'Cash Analysis Fixing Estimate')
                    except:
                        pass
            return initialFX
        elif first:
            first.FixFixingValue = value

    def LegInitialIndexNominalScalingEstimate(self, leg, value='NoValue'):
        assert leg, 'No leg'
        first = self.GetLegInitialNominalScalingReset(leg)
        if value == 'NoValue':
            initialFX = 0.0
            if first:
                if first.IsFixed():
                    initialFX = first.FixingValue()
                else:
                    try:
                        initialFX = self.CalcValue(first,  'Cash Analysis Fixing Estimate')
                    except:
                        pass
            return initialFX
        elif first:
            first.FixFixingValue = value

    def LegInitialNominalScalingEstimate(self, leg):
        estimate =  self.LegInitialIndexNominalScalingEstimate(leg)
        return estimate or leg.InitialIndexValue()

    def UpdateCashLegOnly(self):
        cashLegOnly = False
        if self.IsDvPSettled() and 'Price' == self.PayLeg().NominalScaling():
            first = self.GetLegInitialNominalScalingReset(self.PayLeg())
            cashLegOnly = first and not first.IsFixed()
        return cashLegOnly

    # -------------  Methods used in deal entry UI  -------------

    def MinOfPeriods(self, period1, period2):
        date1 = acm.Time().PeriodSymbolToDate(period1)
        date2 = acm.Time().PeriodSymbolToDate(period2)
        return period2 if acm.Time().DateDifference(date1, date2) > 0 else period1
        
    def GetRateIndex(self, leg):
        query = ("insType = 'RateIndex' and currency = '%s' and generic = true" % (leg.Currency().Name()))
        rateIndexes = acm.FInstrument.Select(query)
        tenorPeriod = self.MinOfPeriods(leg.NominalScalingPeriod(), leg.NominalScalingPeriod())
        tenorPeriodCount = acm.Time().DatePeriodCount(tenorPeriod)
        tenorPeriodUnit = acm.Time().DatePeriodUnit(tenorPeriod)
        
        for rateIndex in rateIndexes:
            leg = rateIndex.Legs().First()
            if leg.EndPeriodCount() == tenorPeriodCount and leg.EndPeriodUnit() == tenorPeriodUnit:
                return rateIndex
        return None
     
     
    def HasCashCollateralPool(self, value=None):
        if value is None:
            return len(self.Instrument().Legs()) == 2
        else:
            if value is True and len(self.Instrument().Legs()) < 2:
                leg = self.Instrument().CreateLeg('Float', 'Receive')
                leg = acm.FBusinessLogicDecorator.WrapObject(leg, None)
                leg.NominalScaling = 'Price'
                leg.InitialIndexValue = 0
                leg.NominalScalingPeriod = self.PayLeg().NominalScalingPeriod()
                if self.PayLeg().IndexRef() and self.PayLeg().IndexRef().Currency() != self.PayLeg().Currency():
                    leg.IndexRefFXFixingType = 'Explicit'
                else:
                    leg.IndexRefFXFixingType = self.PayLeg().IndexRefFXFixingType()
                leg.IndexRef = self.PayLeg().IndexRef()
                leg.StartPeriod = self.PayLeg().StartPeriod()
                leg.StartDate = self.PayLeg().StartDate()
                leg.EndPeriod = self.PayLeg().EndPeriod()
                leg.EndDate = self.PayLeg().EndDate()
                leg.RollingPeriod = self.PayLeg().RollingPeriod()
                leg.RollingPeriodBase = self.PayLeg().RollingPeriodBase()
                leg.Leg().Currency = self.PayLeg().Currency()
                rateIndex = self.GetRateIndex(leg.Leg())
                if rateIndex:
                    leg.Leg().FloatRateReference(rateIndex)
                self.Instrument().SpotBankingDaysOffset = 0
                leg.IndexRefFixingDateRule = self.PayLeg().IndexRefFixingDateRule()
                leg.DayCountMethod = self.PayLeg().DayCountMethod()
                leg.PayCalendar = self.PayLeg().PayCalendar()
                leg.Pay2Calendar = self.PayLeg().Pay2Calendar()
                leg.GenerateSpreadFixings(True)
                leg.GenerateCashFlows(0.0)
                
            elif value == self.HasCashCollateralPool():
                pass
            else:
                self.ReceiveLeg().Unsimulate()


    def RollType(self, value='NoValue', *args):
        if value == 'NoValue':
            openEnd = self.Instrument().OpenEnd()
            if openEnd == 'None':
                return 'Bullet'
            elif openEnd == 'Terminated':
                return 'Terminated'
            elif openEnd == 'Open End':
                if self.Instrument().NoticePeriod() == self.UnderlyingSpotDays() or self.Instrument().NoticePeriod() == '1d':
                    return 'Open'
                else:
                    return 'Evergreen'
        else:
            if value == 'Bullet':
                self.Instrument().OpenEnd = 'None'
                self.Instrument().FirstPayLeg().EndPeriod('1w')
                self.Instrument().NoticePeriod('0d')
                recLeg = self.Instrument().FirstReceiveLeg()
                if recLeg:
                    recLeg.EndPeriod('1w')
            elif value == 'Terminated':
                self.Instrument().OpenEnd = 'Terminated'
            elif value == 'Open':
                self.Instrument().OpenEnd = 'Open End'
                self.Instrument().NoticePeriod = self.UnderlyingSpotDays()
            elif value == 'Evergreen':
                self.Instrument().OpenEnd = 'Open End'
                self.Instrument().NoticePeriod = '90d'
            self.RegenerateCashFlows(True)

    def IsDvPSettled(self, value='NoValue', *args):
        if value == 'NoValue':
            settleCategory = self.Instrument().SettleCategoryChlItem()
            return settleCategory.StringKey() == 'DvP' if settleCategory else False
        else:
            if not self.IsRebate():
                self.HasCashCollateralPool(value is True)
                if value is True:
                    self.ReceiveLeg().Leg().InitialIndexValue = self.LegInitialNominalScalingEstimate(self.PayLeg())
                    self.LegInitialIndexNominalScalingEstimate(self.ReceiveLeg(), self.ReceiveLeg().InitialIndexValue())
            self.Instrument().SettleCategoryChlItem = ('DvP' if value is True else None)

    def ExtendOpenEnd(self, newEndDate):
        for l in self.Legs():
            if self.Instrument().OpenEnd() == "Open End":
                endDate = l.CashFlows().SortByProperty('EndDate', False).First().EndDate()
                l.EndDate = newEndDate
                l.ExtendToEnd(endDate)

    def RegenerateCashFlows(self, excludeHistorical):
        self.Instrument().RegenerateCashFlowsIfNeeded(True, excludeHistorical, False, False, False, False, False, False,
                                                      False, None, None)

    def UnderlyingSpotDays(self):
        try:
            spotDays = str(self.Instrument().Underlying().SpotBankingDaysOffset()) + 'd'
        except:
            spotDays = '2d'
        return spotDays

    #---------------- Methods used in the Security Loan Default Fields creation --------------

    def SecurityLoanSetDefaultFields(self,
                                     underlying=None,
                                     currency=None, legStartDate=None,
                                     legEndDate=None, legStartPeriod='1d',
                                     legEndPeriod='1d', rollingPeriod='1d',
                                     openEnd='Open End', noticePeriod='2d',
                                     dayCountMethod='Act/360', nominalFactor=1.0,
                                     dividendFactor=1.0, spotDays=0,
                                     fixedPrice=False, generateSpreadFixings=True,
                                     isRebate=False, fee=0, productType=None):

        instrument = self.Instrument()
        #Set Instrument settings
        self._SetUnderlyingAndCurrency(instrument, underlying, currency)
        instrument.SpotBankingDaysOffset = spotDays
        instrument.DividendFactor = dividendFactor
        instrument.RefValue = 1.0
        instrument.RefPrice = 1.0
        instrument.ContractSize = 1.0
        instrument.OpenEnd = openEnd
        instrument.NoticePeriod = noticePeriod
        instrument.ProductTypeChlItem = productType
        self._SetStartAndEnd(instrument, legStartDate, legStartPeriod, legEndDate, legEndPeriod)

        #Setting PayLeg
        leg = self.PayLeg()
        leg.LegType = 'Fixed'
        leg.FixedRate = 0
        leg.NominalScaling = 'Initial Price' if fixedPrice is True else 'Price'
        leg.NominalScalingPeriod = '1d'
        leg.IndexRefFXFixingType('None')
        leg.IndexRef = underlying
        leg.DayCountMethod = dayCountMethod
        leg.NominalFactor = nominalFactor
        leg.IndexRefFixingDateRule = self.GetOrCreateDefaultIndexRefFixingDateRule(underlying)
        iiv = leg.SuggestInitialIndexValue() if fixedPrice is True else 0.0
        if acm.Math.IsFinite(iiv):
            leg.InitialIndexValue = iiv
        leg.RollingPeriod = rollingPeriod

        self.SpreadFixings(leg, generateSpreadFixings)
        self.FeePayLeg().StartingFee(fee)

        #Helper from Deal entry utils
        self.IsRebate(isRebate)

        #Setting the Fee at the end. Generating the Rebate Leg we might miss the fee.
        if isRebate:
            self.FeeRebateLeg().StartingFee(fee)


    def _SetUnderlyingAndCurrency(self, instrument, underlying, currency):
        if underlying is None:
            instrument.UnderlyingType = 'Stock'
        else:
            instrument.Underlying = underlying
        if currency is None:
            if underlying is not None:
                instrument.Currency = underlying.Currency()
        else:
            instrument.Currency = currency

    def _SetStartAndEnd(self, instrument, legStartDate, legStartPeriod, legEndDate, legEndPeriod):
        if legStartDate is None:
            instrument.LegStartPeriod(legStartPeriod)
        else:
            instrument.LegStartDate(legStartDate)
        if legEndDate is None:
            instrument.LegEndPeriod(legEndPeriod)
        else:
            instrument.LegEndDate(legEndDate)

    def GetOrCreateDefaultIndexRefFixingDateRule(self, underlying):
        if underlying:
            curr = underlying.Currency()
            name = 'SecurityLoan' + curr.Name() + 'Default'
            fixingDateRule = acm.FFixingDateRule[name]
            if fixingDateRule is None:
                fixingDateRule = acm.FFixingDateRule()
                fixingDateRule.AdjustmentCalendar1 = curr.Calendar()
                fixingDateRule.Name = name
                fixingDateRule.FixingOffset = -1
                fixingDateRule.FixingCalendarAdjustmentRule = 'All'
                fixingDateRule.Commit()
            return fixingDateRule
        else:
            return None

    def MasterSecurityLoanSetDefaultFields(self,
                                           underlying=None,
                                           currency=None,
                                           legStartDate=None,
                                           legEndDate=None,
                                           legStartPeriod='0d',
                                           legEndPeriod='1d',
                                           openEnd='Open End',
                                           noticePeriod='2d',
                                           dayCountMethod='Act/360',
                                           rollingPeriod='1d',
                                           dividendFactor=1.0,
                                           spotDays=0,
                                           nominalFactor=1.0,
                                           fixedPrice=False,
                                           generateSpreadFixings=True
                                           ):

        instrument = self.Instrument()
        self._SetUnderlyingAndCurrency(instrument, underlying, currency)
        instrument.SpotBankingDaysOffset = spotDays
        instrument.DividendFactor = dividendFactor
        instrument.RefValue = 1.0
        instrument.RefPrice = 1.0
        instrument.ContractSize = 1.0
        instrument.OpenEnd = openEnd
        instrument.NoticePeriod = noticePeriod
        instrument.ProductTypeChlItem("Master Security Loan")
        self._SetStartAndEnd(instrument, legStartDate, legStartPeriod, legEndDate, legEndPeriod)


        leg = instrument.FirstPayLeg()
        leg.LegType = 'Fixed'
        leg.FixedRate = 0
        leg.NominalScaling = 'Initial Price' if fixedPrice is True else 'Price'
        leg.NominalFactor = nominalFactor
        leg.NominalScalingPeriod = '1d'
        leg.IndexRefFXFixingType("Explicit")
        leg.IndexRef = underlying
        leg.DayCountMethod = dayCountMethod
        leg.NominalFactor = nominalFactor
        leg.IndexRefFixingDateRule = self.GetOrCreateDefaultIndexRefFixingDateRule(underlying)
        leg.RollingPeriod = rollingPeriod

        self.SpreadFixings(leg, generateSpreadFixings)


        if instrument.Underlying():
            insName = "%s/%s/MASTER" % (instrument.Underlying().Name(), instrument.Currency().Name())
            instrument.Name(insName)


class SecurityLoanTradeHandler(object):

    def __init__(self, trade):
        self.trade = trade
        self.handler = SecurityLoanHandler(trade.Instrument())
        self.fxRateCache = FxRateCalcCache()
        
    def Trade(self):
        return self.trade

    def Instrument(self):
        return self.trade.Instrument()

    def SecurityLoanTradeSetDefaultFields(self,
                                          quantity=1,
                                          acquirer=sentinel,
                                          portfolio=sentinel,
                                          counterparty=sentinel,
                                          collateralAgreement=None,
                                          slAccount=sentinel,
                                          status=sentinel,
                                          source='Manual',
                                          valueday=None,
                                          pendingOrder=False,
                                          orderType=sentinel,
                                          holdTime=False,
                                          feeLimit=sentinel,
                                          requestHold=sentinel):
        self.trade.Quantity = quantity
        self.trade.Market = source
        self.trade.TradeCategory = 'Cash'
        if status is not sentinel:
            self.trade.Status = status
        if collateralAgreement is not None:
            self.trade.AddInfoValue("CollateralAgreement", collateralAgreement)
        if slAccount is not sentinel:
            self.trade.AddInfoValue("SL_Account", slAccount)
        if portfolio is not sentinel:
            self.trade.Portfolio = portfolio
        if counterparty is not sentinel:
            self.trade.Counterparty = counterparty
        if acquirer is not sentinel:
            self.trade.Acquirer = acquirer
        if orderType is not sentinel:
            self.trade.AddInfoValue("SBL_OrderType", orderType)
        if requestHold is not sentinel:
            self.trade.AddInfoValue("SBL_RequestHold", requestHold)

        self.trade.ValueDay = self.trade.Instrument().StartDate() if valueday is None else valueday
        self.trade.AddInfoValue("SBL_PendingOrder", pendingOrder)
        
        if feeLimit is not sentinel:
            self.trade.AddInfoValue('SBL_LimitFee', feeLimit)
        if holdTime:
            from FSecLendHoldTrade import HoldTrade
            HoldTrade(self.trade)
                        

    # Mix method that requires the Trade (quantity) but changes the state of the Legs.
    def InitialCashAmount(self, value='NoValue'):
        leg = self.handler.ReceiveLeg()
        if value == 'NoValue':
            if leg is None:
                return None
            else:
                val = self.handler.LegInitialNominalScalingEstimate(leg)
                val *= self.handler.LegInitialIndexFXEstimate(leg) if self.handler.LegNeedsFxReset(leg) else 1.0
                val *= self.Instrument().ContractSize()
                val *= self.Trade().Quantity()
                val *= leg.NominalFactor()
                return val * -1
        else:
            factor = self.Trade().Quantity()
            factor *= self.Instrument().ContractSize()
            factor *= self.handler.LegInitialIndexFXEstimate(leg) if self.handler.LegNeedsFxReset(leg) else 1.0
            factor *= leg.NominalFactor()
            initialPrice = abs(value / factor)
            if self.handler.UpdateCashLegOnly():
                leg.InitialIndexValue(initialPrice)
                self.handler.LegInitialIndexNominalScalingEstimate(leg, initialPrice)
            else:
                self.Trade().Quantity = self.Trade().Quantity() * value / self.InitialCashAmount()
                
            if self.IsPaymentDvPSettled():
                self.DvPPaymentCashAmount(value)

    def Nominal(self, value='NoValue'):
        leg = self.handler.PayLeg()
        if value == 'NoValue':
            if leg is None:
                return None
            else:
                val = self.handler.LegInitialNominalScalingEstimate(leg)
                val *= self.handler.LegInitialIndexFXEstimate(leg) if self.handler.LegNeedsFxReset(leg) else 1.0
                val *= self.Instrument().ContractSize()
                val *= self.Trade().Quantity()
                val *= leg.NominalFactor()
                return val
        else:
            self.Trade().Quantity = self.Trade().Quantity() * value / self.Nominal()

    def CalcFXRate(self, fromCurr, toCurr, *args):
        fxRate = 1
        try: 
            calendarInfoFunc = acm.GetFunction('createCalendarInformation', 1)
            underlying = self.Instrument().Underlying()
            calendarInfo = calendarInfoFunc([underlying.Currency().Calendar()])
            resetDate = calendarInfo.AdjustBankingDays(self.Trade().ValueDay(), -1)
            resetValueDay = underlying.PriceDateToValueDate(resetDate)
            fxRate = self.fxRateCache.FXRate(fromCurr, toCurr, resetValueDay)
        except:
            pass
        return fxRate

    def DvPPaymentCashAmount(self, value='NoValue', *args): 
        payment = self.FindPayment()
        if value == 'NoValue':
            return payment.Amount() if payment else 0.0
        else:
            if payment:
                if value is None:
                    import traceback
                    traceback.print_stack()
                payment.Amount(value)
                qty = self.Trade().Quantity()
                if value and ((value > 0 and qty > 0) or (value < 0 and qty < 0)):
                    #Change sign of Nominal
                    self.Nominal(-self.Nominal())
            else:
                raise Exception('No DvP payment found')
        
    def FindPayment(self):
        for payment in self.Trade().Payments():
            if payment.Type() == 'Cash' and payment.Text() == 'Payment DvP':
                return payment
        return None
        
    def FindOrCreatePayment(self):
        payment = self.FindPayment()
        if not payment:
            payment = self.Trade().CreatePayment()
        return payment
      
    def RefreshDvPPaymentAmount(self, oldNominal, newNominal):
        if self.IsPaymentDvPSettled():
            payment = self.FindPayment()
            if payment and payment.Currency() == self.Trade().Currency():
                initialMargin = abs(self.DvPPaymentCashAmount() / oldNominal) if oldNominal != 0.0 else 1
                self.DvPPaymentCashAmount(-newNominal * initialMargin)

    def DvpPaymentCashCurrency(self, value='NoValue', *args): 
        payment = self.FindPayment()
        if value == 'NoValue':
            return payment.Currency() if payment else self.Trade().Currency()
        else:
            payment.Currency(value) if payment else None
                
    def UpdateDvPPayment(self, updateCurrency = False, *args):
        if self.IsPaymentDvPSettled():
            payment = self.FindPayment()
            if payment:
                t = self.Trade()
                payment.Party(t.Counterparty())
                payment.PayDay(t.ValueDay())
                payment.ValidFrom(acm.Time().AsDate(t.TradeTime()))
                if updateCurrency:
                    payment.Currency(t.Instrument().Currency())
    
    def SetPaymentDvP(self, isDvP):
        if isDvP:
            t = self.Trade()
            payment = self.FindOrCreatePayment()
            payment.Currency(t.Instrument().Currency())
            payment.Party(t.Counterparty())
            payment.Type('Cash')
            payment.Text('Payment DvP')
            payment.PayDay(t.ValueDay())
            payment.ValidFrom(acm.Time().AsDate(t.TradeTime()))
            payment.Amount(self.InitialCashAmount() if self.handler.IsRebate() else -self.Nominal())
        else:
            payment = self.FindPayment()
            if payment:
                payment.Unsimulate()
        
    def IsPaymentDvPSettled(self, value='NoValue', *args):
        if value == 'NoValue':
            settleCategory = self.Instrument().SettleCategoryChlItem()
            return settleCategory.StringKey() == 'Payment DvP' if settleCategory else False
        else:
            self.Instrument().SettleCategoryChlItem = ('Payment DvP' if value is True else None)
            self.SetPaymentDvP(value)

    @ReturnDomainDecorator('double')
    def DvpPaymentInitialMargin(self, value='NoValue', *args):
        payment = self.FindPayment()
        nominal = self.Nominal()
        if payment and payment.Currency() != self.Trade().Currency():
            nominal = nominal * self.CalcFXRate(self.Trade().Currency(), payment.Currency())
        
        if value == 'NoValue':
            return abs(self.DvPPaymentCashAmount() / nominal) if nominal != 0.0 else 1
        else:
            self.DvPPaymentCashAmount(float(value)/100.0 * nominal * -1)
        
#Utility class for handling Trade Actions
class SecurityLoanTradeAction(object):

    @classmethod
    def CreateTradeActionTrade(cls,
                               trade,
                               quantity,
                               valueDay=None,
                               tradeTime=None,
                               status=None,
                               orderType=None,
                               pendingOrder=None):

        remaining = cls._RemainingQuantity(trade)
        if not acm.Math.AlmostZero(remaining, 1e-10) and abs(remaining + quantity) < abs(remaining):
            return cls.CreateCloseTrade(trade, quantity, valueDay=valueDay, tradeTime=tradeTime, status=status, orderType=orderType, pendingOrder=pendingOrder)
        else:
            return cls.CreateAdjustTrade(trade, quantity, valueDay=valueDay, tradeTime=tradeTime, status=status, orderType=orderType, pendingOrder=pendingOrder)

    @classmethod
    def CreateCloseTrade(cls,
                         trade,
                         quantity,
                         valueDay=None,
                         tradeTime=None,
                         status=None,
                         orderType=None,
                         pendingOrder=False):

        assert quantity, 'No quantity to adjust with'
        valueDay = cls._AdjustValueDate(trade, valueDay) #TODO:move from here
        closeTrade = acm.TradeActions.CloseTrade(
            trade,
            valueDay,
            valueDay,
            quantity,
            0,
            [])
        if tradeTime is not None:
            decoratedTrade = acm.FBusinessLogicDecorator.WrapObject(closeTrade)
            decoratedTrade.TradeTime = tradeTime
            decoratedTrade.ValueDay = valueDay
        if status is not None:
            closeTrade.Status = status
        if hasattr(closeTrade.AdditionalInfo(), 'SBL_OrderType'):
            closeTrade.AddInfoValue('SBL_OrderType', orderType)
        if hasattr(closeTrade.AdditionalInfo(), 'SBL_PendingOrder'):
            closeTrade.AddInfoValue('SBL_PendingOrder', pendingOrder)
        return closeTrade

    @classmethod
    def CreateRecallTrade(cls,
                          trade,
                          quantity,
                          valueDay=None,
                          tradeTime=None,
                          status=None,
                          orderType=None,
                          pendingOrder=None):

        closeTrade = cls.CreateCloseTrade(trade, quantity, valueDay, tradeTime, status, orderType, pendingOrder)
        calendarInfo = trade.Instrument().Underlying().Currency().Calendar().CalendarInformation()
        valueDay = calendarInfo.AdjustBankingDays(acm.Time.DateToday(), trade.Instrument().NoticePeriodCount())
        closeTrade.ValueDay = valueDay
        closeTrade.Type = 'Rollout'
        return closeTrade

    @classmethod
    def CreateAdjustTrade(cls,
                          trade,
                          quantity,
                          valueDay=None,
                          tradeTime=None,
                          status=None,
                          orderType=None,
                          pendingOrder=None):

        closeTrade = cls.CreateCloseTrade(trade, quantity, valueDay, tradeTime, status, orderType, pendingOrder)
        closeTrade.Type = 'Adjust'
        return closeTrade

    @classmethod
    def _RemainingQuantity(cls, trade):
        trades = acm.FTrade.Select('contract = {0}'.format(trade.Oid()))
        excludeStatuses = ["Void", "Confirmed Void", "Simulated", ]
        quantities = [t.Quantity() if t.Status() not in excludeStatuses else 0 for t in trades]
        return sum(quantities)

    @classmethod
    def _AdjustValueDate(cls, trade, valueDay):
        calendarInfo = trade.Instrument().Underlying().Currency().Calendar().CalendarInformation() 
        if valueDay:# an increase?
            if calendarInfo and calendarInfo.IsNonBankingDay(valueDay):
                return calendarInfo.Modify(valueDay, "Following")
            else:
                return valueDay
        else: #a return?
            return calendarInfo.AdjustBankingDays(acm.Time.DateToday(), cls.GetDefaultSettlementDelay())

    @classmethod
    def GetDefaultSettlementDelay(cls):
        return 1 # Always default to one day in the future. Market standard is typically underlying spot day - 1, i.e. typically 1 day.

class SecurityLoanLegHandler(object):

    def __init__(self, leg):
        self.leg = leg

    def Leg(self):
        return self.leg

    # Rate functionality
    def FeeAtDate(self, date, fee='NoValue'):
        reset = self.SpreadResetAtDate(date)
        return self.FeeFromReset(reset, fee) if reset is not None else acm.Math.NotANumber()

    def FeeFromReset(self, reset, fee='NoValue'):
        if reset is None:
            return
        if fee == 'NoValue':
            if reset.IsFixed():
                value = reset.FixFixingValue()
            else:
                a = acm.FArray()
                a.Add(reset.Day())
                estimate = self.GetFixingEstimates(a)
                value = float(estimate[0]) if len(estimate) > 0 else acm.Math.NotANumber()
            return value
        else:
            reset.FixFixingValue = fee

    def Fee(self, fee='NoValue'):
        return self.FeeFromReset(self.SpreadReset(), fee)

    def FirstFeeDay(self):
        return self.SpreadResetBoundaries()[0]

    def LastFeeDay(self):
        return self.SpreadResetBoundaries()[1]

    def SpreadResetBoundaries(self):
        resetDays = [r.Day() for cf in self.Leg().CashFlows() for r in cf.Resets() if r.ResetType() == "Spread"]
        resetMin = min(resetDays) if resetDays else None
        resetMax = max(resetDays) if resetDays else None
        return resetMin, resetMax

    def ReferenceDate(self):
        return self.AdjustFixingDate(acm.Time.DateToday())

    def AdjustFixingDate(self, baseDate):
        minBoundary, maxBoundary = self.SpreadResetBoundaries()
        if baseDate < minBoundary:
            adjustedDate = minBoundary
        elif baseDate > maxBoundary:
            adjustedDate = maxBoundary
        else:
            adjustedDate = self.CalendarInformation().Modify(baseDate, 'Following')
        return adjustedDate

    def SpreadReset(self):
        return self.SpreadResetAtDate(self.ReferenceDate())

    def SpreadResetAtDate(self, date):
        reset = None
        for cf in self.Leg().CashFlows():
            for r in cf.Resets():
                if r.ResetType() == "Spread" and r.Day() == date:
                    reset = r
                    break
        return reset

    def StartingFee(self, value='NoValue'):
        reset = self.FirstSpreadReset()
        if reset is None:
            return acm.Math.NotANumber() if value == 'NoValue' else None
        if value == 'NoValue':
            if value is not None:
                return reset.FixFixingValue() if reset.IsFixed() else 0.0
            else:
                return acm.Math.NotANumber()
        else:
            reset.FixFixingValue(value)

    def FirstSpreadReset(self):
        first = None
        for cf in self.Leg().CashFlows():
            for r in cf.Resets():
                if r.ResetType() == "Spread":
                    if (first is None) or first.Day() > r.Day():
                        first = r
        return first

    def LastSpreadReset(self):
        last = None
        for cf in self.Leg().CashFlows():
            for r in cf.Resets():
                if r.ResetType() == "Spread":
                    if (last is None) or last.Day() < r.Day():
                        last = r
        return last

    def FirstOrLastFixedStoredSpreadReset(self):
        last = None
        first = None
        for cf in self.Leg().CashFlows():
            for r in cf.Resets():
                if r.ResetType() == "Spread":
                    if (last is None) or last.Day() < r.Day():
                        if r.IsFixed():
                            last = r
                    if last is None and ((first is None) or first.Day() > r.Day()):
                        first = r
        return last or first

    def CalendarInformation(self):
        calendars = acm.FArray()
        for c in [self.Leg().PayCalendar(), \
                  self.Leg().Pay2Calendar(), \
                  self.Leg().Pay3Calendar(), \
                  self.Leg().Pay4Calendar()]:
            if c is not None:
                calendars.Add(c)
        return acm.GetFunction('createCalendarInformation', 1)(calendars)

    def GetFixingEstimates(self, estimateDates):
        try:
            if estimateDates.IsEmpty():
                return []
            spreadFixings = acm.FArray()
            spreadFixings.AddAll([v for cf in self.leg.CashFlows() for v in cf.Resets() if v.ResetType() == "Spread"])
            spreadFixings.SortByProperty('Day')
            spreadFixingEstimateValues = list()
            i = 0
            value = 0.0
            for f in spreadFixings:
                if i >= len(estimateDates):
                    break
                if f.IsFixed():
                    value = f.FixFixingValue()
                if f.Day() == acm.Time.AsDate(estimateDates[i]):
                    spreadFixingEstimateValues.append(
                        acm.GetFunction('denominatedvalue', 4)(value, None, None, estimateDates[i])
                    )
                    i = i + 1
            return spreadFixingEstimateValues
        except Exception as e:
            return [acm.Math.NotANumber()]


