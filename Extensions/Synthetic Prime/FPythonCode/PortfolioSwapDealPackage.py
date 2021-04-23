
import acm
import re
from DealPackageDevKit import Bool, DealPackageDefinition, Date, Str, Object, Float, DealPackageUserException, CalcVal, Action, ReturnDomainDecorator, DealPackageChoiceListSource, Settings, PortfolioChoices, TradeStatusChoices, AcquirerChoices, AttributeDialog, ValGroupChoices
import FUxCore
import PortfolioSwapMetaLegs
from CompositeFilterFields import FilterFields
from PortfolioSwapParameters import DealPackageParameters
from FSyntheticPrimeActions import GeneratePortfolioSwap, Extend, Fix, Terminate, TradeAssign, SweepCash, Roll, AdjustCash
from TraitBasedDealPackage import MuteNotificationsWithSafeExit
from FSyntheticPrimeUtil import AdjustBankingDays, ClearPortfolioSwapLegs, ClearFeeDividendAndSyntheticCashflows, ClearPerformanceFinancingAndStockBorrowCashflows
from DealPackageUtil import SetNew

@Settings(ShowGraphInitially=False)
class PortfolioSwapDefinition(DealPackageDefinition):
    #Deal Package 
    name = Object(                   defaultValue='',
                                     label='Name',
                                     objMapping='DealPackage.InstrumentPackage.Name',
                                     onChanged='@NameChanged')
    #Instrument
    currency = Object(               label='Currency',
                                     onChanged='@UpdateCashRateIndexChoices|UpdateDayCount|UpdatePayCalendars',
                                     objMapping='Instrument.Currency|Trade.Currency|MetaInstrument.Currency|MetaLegs.Currency|ClientSpreadIndex.Currency')

    equityCurr = Object (            label='Equity Curr',
                                     objMapping='FeeMetaLeg.OriginalCurr',
                                     onChanged='@UpdateResetCalendars')
                            
    startDate = Object(              defaultValue=acm.Time.DateToday(),
                                     label='Start Date',
                                     objMapping='Instrument.StartDate',
                                     onChanged='@StartDateChanged',
                                     validate='@StartDateValidate',
                                     transform='@TransformStartPeriodToDate')
                            
    expiryDate = Object(             defaultValue=acm.Time.DateAdjustPeriod(acm.Time.DateToday(), '1y'),
                                     label='Expiry Date',
                                     objMapping='Instrument.ExpiryDateOnly',
                                     validate='@EndDateValidate',
                                     transform='@TransformExpPeriodToDate')
                            
    openEnd = Object(                defaultValue='Open End',
                                     label='Status',
                                     visible='@PortfolioSwapIsTerminated',
                                     enabled=False,
                                     objMapping='Instrument.OpenEnd')
                            
    noticePeriod = Object(           defaultValue='0d',
                                     label='Notice Period',
                                     objMapping='Instrument.NoticePeriod')
    
    syntheticPortfolio = Object(     label='Synthetic Prf',
                                     domain='FPhysicalPortfolio',
                                     objMapping='Instrument.FundPortfolio',
                                     onChanged='@SyntheticPortfolioChanged|UpdateFinancingRateIndexChoices',
                                     mandatory=True)
    
    filteredPortfolio = Object(      objMapping='FilteredPortfolio' )

    synthPrfCurr = Object(           label='Synth Prf Curr',
                                     domain='FCurrency',
                                     enabled=False,
                                     visible='@SyntheticPortfolioChosen',
                                     objMapping='SyntheticPortfolioCurrency')
    
    valGroup = Object(               defaultValue=None,
                                     label='Val Group',
                                     objMapping='Instrument.ValuationGrpChlItem',
                                     visible='@IsShowModeDetail',
                                     choiceListSource=ValGroupChoices())
    
    #Client Spreads
    clientLongSpread = Float(        defaultValue=0,
                                     label='Long',
                                     onChanged='@ClientLongSpreadChanged',
                                     visible='@FinancingLegSpreadFixingEnabled')
                                 
    clientShortSpread = Float(       defaultValue=100.0,
                                     label='Short',
                                     onChanged='@ClientShortSpreadChanged',
                                     visible='@FinancingLegSpreadFixingEnabled')
                                 
    #Legs - Broadcasting
    dayCountMethod = Object(         label='Day Count Method',
                                     objMapping='MetaLegs.DayCountMethod|ClientSpreadIndex.LongestLeg.DayCountMethod',
                                     validateMapping=False)

    dayOffsetMethod = Object(        defaultValue='Following',
                                     label='Day Offset Method',
                                     objMapping='MetaLegs.ResetDayMethod|MetaLegs.PayDayMethod',
                                     choiceListSource='@DayOffsetMethodChoices',
                                     validateMapping=False)
                                     
    rollingBaseDate  = Object(       defaultValue='0d',
                                     label='Rolling Base Date',
                                     objMapping='MetaLegs.RollingPeriodBase',
                                     transform='@TransformStartPeriodToDate',
                                     validateMapping=False)
                                     
    rollingPeriod = Object(          defaultValue='0d',
                                     label='Rolling Period',
                                     objMapping='MetaLegsNoUPL.RollingPeriod',
                                     validateMapping=False)
                                 
    payCalendar = Object(            label='Pay Calendar',
                                     objMapping='MetaLegs.PayCalendar',
                                     validateMapping=False)
                                     
    resetCalendar = Object(          label='Reset Calendar',
                                     objMapping='MetaLegs.ResetCalendar',
                                     validateMapping=False)

    payOffset = Object(              label='Pay Offset',
                                     objMapping='MetaLegs.PayOffset',
                                     enabled='@PayOffsetEnabled',
                                     validateMapping=False)
                                 
    #Finaning Leg                
    financingRolling = Object(       defaultValue='0d',
                                     label='Rolling Period',
                                     objMapping='FinancingMetaLeg.RollingPeriod',
                                     visible='@IsShowModeDetail')

    financingFloatRateRef = Object(  label='Float Rate Ref',
                                     objMapping='FinancingMetaLeg.FloatRateReference',
                                     choiceListSource='@FinancingRateIndexChoices',
                                     mandatory=True)
                                 
    financingRollingBaseDate = Object( defaultValue='0d',
                                     label='Rolling Base Date',
                                     objMapping='FinancingMetaLeg.RollingPeriodBase',
                                     transform='@TransformStartPeriodToDate',
                                     visible='@IsShowModeDetail')
                                 
    financingSpreadFixings = Object( defaultValue=True,
                                     label='Spread Fixings',
                                     objMapping='FinancingMetaLeg.GenerateSpreadFixings')
                                 
    financingResetType = Object(     defaultValue='Simple Overnight',
                                     label='Reset Type',
                                     objMapping='FinancingMetaLeg.ResetType',
                                     choiceListSource='@ResetTypeChoices')

    financingResetPeriod = Object(   label='Reset Period',
                                     objMapping='FinancingMetaLeg.ResetPeriod',
                                     visible='@FinancingHasWeightedResets' )
                                     
    financingLongStub = Object(      defaultValue=False,
                                     label='Long Stub',
                                     objMapping='FinancingMetaLeg.LongStub',
                                     visible='@ShowInDetailBool')
    
    financingFixPeriod = Object(     defaultValue=False,
                                     label='Fix Period',
                                     objMapping='FinancingMetaLeg.FixedCoupon',
                                     visible='@ShowInDetailBool')
                                     
    financingPayOffset = Object(     label='Pay Offset',
                                     objMapping='FinancingMetaLeg.PayOffset',
                                     visible='@PayOffsetVisible')
                                     
    financingResetCalendar = Object( label='Reset Calendar',
                                     objMapping='FinancingMetaLeg.ResetCalendar',
                                     visible='@IsShowModeDetail')                                      
                                 
    #Synthetic Cash Leg
    cashEnabled = Bool(              defaultValue=True,
                                     label='Enabled',
                                     onChanged='@UpdateSyntheticCashEnabledChanged')   
    
    cashRolling = Object(            defaultValue='0d',
                                     label='Rolling Period',
                                     objMapping='SyntheticCashMetaLeg.RollingPeriod',
                                     visible='@SyntheticCashShowInDetail')

    cashFloatRateRef = Object(       label='Float Rate Ref',
                                     objMapping='SyntheticCashMetaLeg.FloatRateReference',
                                     choiceListSource='@CashRateIndexChoices',
                                     mandatory='@SyntheticCashVisible',
                                     visible='@SyntheticCashVisible')
                                 
    cashRollingBaseDate = Object(    defaultValue='0d',
                                     label='Rolling Base Date',
                                     objMapping='SyntheticCashMetaLeg.RollingPeriodBase',
                                     transform='@TransformStartPeriodToDate',
                                     visible='@SyntheticCashShowInDetail')    
                                         
    cashResetType = Object(          defaultValue='Simple Overnight',
                                     label='Reset Type',
                                     objMapping='SyntheticCashMetaLeg.ResetType',
                                     choiceListSource='@ResetTypeChoices',
                                     visible='@SyntheticCashVisible')
                                 
    cashResetPeriod = Object(        label='Reset Period',
                                     objMapping='SyntheticCashMetaLeg.ResetPeriod',
                                     visible='@CashHasWeightedResets')
                                     
    cashPayOffset = Object(          label='Pay Offset',
                                     objMapping='SyntheticCashMetaLeg.PayOffset',
                                     visible='@SyntheticCashShowInDetail')

    cashResetCalendar = Object(      label='Reset Calendar',
                                     objMapping='SyntheticCashMetaLeg.ResetCalendar',
                                     visible='@SyntheticCashShowInDetail')                                      

    #Performance Leg                     
    performanceRolling = Object(     defaultValue='0d',
                                     label='Rolling Period',
                                     objMapping='PerformanceMetaLeg.RollingPeriod',
                                     visible='@NoUplRplSplitEnabled')

    performanceRollingBaseDate = Object( defaultValue='0d',
                                     label='Rolling Base Date',
                                     objMapping='PerformanceMetaLeg.RollingPeriodBase',
                                     transform='@TransformStartPeriodToDate',
                                     visible='@NoUplRplSplitEnabled')
                                     
    performancePayOffset = Object(   label='Pay Offset',
                                     objMapping='PerformanceMetaLeg.PayOffset',
                                     visible='@PayOffsetVisibleAndNoUplRplSplitEnabled') 
                                     
    performanceResetCalendar = Object( label='Reset Calendar',
                                     objMapping='PerformanceMetaLeg.ResetCalendar',
                                     visible='@NoUplRplSplitEnabled') 

    #If enabled, the Performance will be handled by one leg (TPL) instead of two legs (UPL/RPL)                     
    enableNoPerformanceSplit = Bool( defaultValue=False,
                                     label='TPL',
                                     onChanged='@UpdateNoPerformanceSplitEnabledChanged',
                                     visible='@HasLegCategoryUPL')

    #Performance RPL Leg                     
    rplPerformanceRolling = Object(  defaultValue='0d',
                                     label='Rolling Period',
                                     objMapping='PerformanceRPLMetaLeg.RollingPeriod',
                                     visible='@UplRplSplitEnabled')

    rplPerformanceRollingBaseDate = Object( defaultValue='0d',
                                     label='Rolling Base Date',
                                     objMapping='PerformanceRPLMetaLeg.RollingPeriodBase',
                                     transform='@TransformStartPeriodToDate',
                                     visible='@UplRplSplitEnabled')
                                     
    rplPerformancePayOffset = Object(label='Pay Offset',
                                     objMapping='PerformanceRPLMetaLeg.PayOffset',
                                     visible='@PayOffsetVisibleAndUplRplSplitEnabled') 
                                     
    rplPerformanceResetCalendar = Object( label='Reset Calendar',
                                     objMapping='PerformanceRPLMetaLeg.ResetCalendar',
                                     visible='@UplRplSplitEnabled') 
    #Performance UPL Leg                     
    uplPerformanceRolling = Object(  defaultValue='0d',
                                     label='Rolling Period',
                                     editable=False,
                                     objMapping='PerformanceUPLMetaLeg.RollingPeriod',
                                     visible='@UplRplSplitEnabled')

    uplPerformanceRollingBaseDate = Object( defaultValue='0d',
                                     label='Rolling Base Date',
                                     editable=False,
                                     objMapping='PerformanceUPLMetaLeg.RollingPeriodBase',
                                     transform='@TransformStartPeriodToDate',
                                     visible='@UplRplSplitEnabled')

    uplPerformancePayOffset = Object(label='Pay Offset',
                                     objMapping='PerformanceUPLMetaLeg.PayOffset',
                                     visible='@PayOffsetVisibleAndUplRplSplitEnabled') 
                                     
    uplPerformanceResetCalendar = Object( label='Reset Calendar',
                                     objMapping='PerformanceUPLMetaLeg.ResetCalendar',
                                     visible='@UplRplSplitEnabled') 
                                     
    #Dividend Settings
    performancePassType = Object(    defaultValue='Dividend Payday',
                                     label='Pass Type',
                                     objMapping='PerformanceDividendMetaLeg.PassingType',
                                     choiceListSource='@PassTypeChoices')
                                     
    performanceTaxHandling = Object( defaultValue='None',
                                     label='Tax Handling',
                                     objMapping='PerformanceDividendMetaLeg.IncludeTaxFactor',
                                     visible='@PassTypeNotNone')

    #Stock Borrow Leg
    stockBorrowEnabled = Bool(       label='Enabled',
                                     onChanged='@UpdateStockBorrowEnabledChanged')        
                        
    stockBorrowRolling = Object(     defaultValue='0d',
                                     label='Rolling Period',
                                     objMapping='StockBorrowMetaLeg.RollingPeriod',
                                     visible='@StockBorrowShowInDetail')

    stockBorrowRollingBaseDate = Object(defaultValue='0d',
                                     label='Rolling Base Date',
                                     objMapping='StockBorrowMetaLeg.RollingPeriodBase',
                                     transform='@TransformStartPeriodToDate',
                                     visible='@StockBorrowShowInDetail')    
                                     
    stockBorrowLongStub = Object(    defaultValue=False,
                                     label='Long Stub',
                                     objMapping='StockBorrowMetaLeg.LongStub',
                                     visible='@StockBorrowShowInDetailBool')
    
    stockBorrowFixPeriod = Object(   defaultValue=False,
                                     label='Fix Period',
                                     objMapping='StockBorrowMetaLeg.FixedCoupon',
                                     visible='@StockBorrowShowInDetailBool')
                                     
    stockBorrowPayOffset = Object(   label='Pay Offset',
                                     objMapping='StockBorrowMetaLeg.PayOffset',
                                     visible='@StockBorrowPayOffsetVisible') 

    stockBorrowResetCalendar = Object( label='Reset Calendar',
                                     objMapping='StockBorrowMetaLeg.ResetCalendar',
                                     visible='@StockBorrowShowInDetail')                                     
                                     
    regenerateStartDate = Date(      defaultValue=acm.Time().SmallDate(),
                                     label='Start Date',
                                     validate='@StartDateValidate',
                                     transform='@PeriodToStartDateTransform')
                                     
    regenerateEndDate = Date(        defaultValue=acm.Time().DateToday(),
                                     label='End Date',
                                     validate='@EndDateValidate',
                                     transform='@PeriodToEndDateTransform')

    rollName = Str(                  defaultValue='',
                                     label='Name')
    
    rollExpiryDate = Date(           defaultValue=acm.Time.DateAdjustPeriod(acm.Time.DateToday(), '1y'),
                                     label='Expiry Date',
                                     validate='@EndDateValidate',
                                     transform='@PeriodToDateFromToday')
                            
    terminateDate     = Date(        defaultValue=acm.Time().SmallDate(),
                                     label='Termination Date',
                                     validate='@StartDateValidate',
                                     transform='@PeriodToDateFromToday')
                            
    adjustCashAmount =   Float(      label='Amount')
    
    adjustCashCurrency = Object(     domain='FCurrency',
                                     enabled=False,
                                     label = 'Currency')

    adjustCashDate =     Date(       label = 'Pay Date')

    #Trade                        
    buySell = Object(                label='Buy/Sell',
                                     objMapping='BuySell',
                                     choiceListSource=['Buy', 'Sell'])
                                
    counterparty = Object(           label='Counterparty',
                                     objMapping='Trade.Counterparty',
                                     choiceListSource='@CounterpartyChoices',
                                     mandatory=True)
                                 
    portfolio = Object(              label='Portfolio',
                                     objMapping='Trade.Portfolio',
                                     choiceListSource=PortfolioChoices() )
    
    acquirer = Object(               label='Acquirer',
                                     objMapping='Trade.Acquirer',
                                     choiceListSource=AcquirerChoices() )
    
    tradeTime = Object(              label='Trade Time',
                                     objMapping='Trade.TradeTime',
                                     transform='@TransformPeriodToDate' )                   

    valueDay = Object(               label='Value Day',
                                     objMapping='Trade.ValueDay' )                   

    status = Object(                 defaultValue='Simulated',
                                     label='Trade Status',
                                     objMapping='Trade.Status',
                                     choiceListSource=TradeStatusChoices())
                                 
    matchingMethod = Str(            defaultValue='DEFAULT',
                                     label='Matching Meth',
                                     choiceListSource='@MatchingMethodChoices',
                                     onChanged='@PerformTouch' )
    
    trdNbr = Object(                 label='Trade No',
                                     objMapping='TradeOid',
                                     visible='@TradeOid')
    
    clientSpreadPrice = Object(      domain='FPrice')
                                      
    
    #Actions
    terminate = Action(              action='@Terminate',
                                     dialog=AttributeDialog(label='Terminate', 
                                                            customPanes='@TerminatePane',
                                                            btnLabel='Perform')) 
    
    regenerateAll = Action(          dialog=AttributeDialog(label='Regenerate Between', 
                                                            customPanes='@RegeneratePane',
                                                            btnLabel='Run'),
                                     action='@RegenerateAll')
    
    tradeAssign = Action(            action='@TradeAssign')
 
    legPerSecAndType = Action(       action='@LegPerSecurityAndType')
    
    clientSpreadInstr = Action(      action='@ClientSpreadInstrument')
    
    securitySpreadInstr = Action(    action='@SecuritySpreadInstrument')
    
    financingMetaLeg = Action(       action='@FinancingMetaLeg')

    performanceMetaLeg = Action(     action='@PerformanceMetaLeg')
    
    rplPerformanceMetaLeg = Action(  action='@PerformanceRPLMetaLeg')
    
    uplPerformanceMetaLeg = Action(  action='@PerformanceUPLMetaLeg')
    
    stockBorrowMetaLeg = Action(     action='@StockBorrowMetaLeg')
    
    syntheticCashMetaLeg = Action(   action='@SyntheticCashMetaLeg')
    
    feeMetaLeg = Action(             action='@FeeMetaLeg')
    
    filterFields = FilterFields()
    
    prfQueryFolder = Object(         objMapping='FilteredPortfolioQueryFolder')
    
    sweepCash = Action(              action='@SweepCash',
                                     enabled='@SyntheticCashVisible')

    extendPortfolioSwap = Action(    action='@Extend')

    fixPortfolioSwap = Action(       action='@Fix')

    roll = Action(                   action='@Roll',
                                     dialog=AttributeDialog(label='Roll', 
                                                            customPanes='@RollPane',
                                                            btnLabel='Perform'))
    
    isExtended = Action(             action='@IsExtended')
    
    adjustCash = Action(             action='@AdjustCash',
                                     enabled='@SyntheticCashVisible',
                                     dialog=AttributeDialog(label='Adjust Cash', 
                                                            customPanes='@AdjustCashPane',
                                                            btnLabel='Adjust Cash'))

    
    def CustomPanes(self):
        if self.filterFields.TabVisible():
            return self.GetCustomPanesFromExtValue('CustomPanes_PortfolioSwap_Filter')
        else:
            return self.GetCustomPanesFromExtValue('CustomPanes_PortfolioSwap')
        
    def RegeneratePane(self, *args):
        return [
                    {'Period' : '''
                                regenerateStartDate;
                                regenerateEndDate;
                                '''
                    }
                ]
    
    def RollPane(sefl, *args):
        return [
                    {'Roll Portfolio Swap' : '''
                                rollName;
                                terminateDate;
                                rollExpiryDate;
                                '''
                    }
                ]
    
    def TerminatePane(sefl, *args):
        return [
                    {'Terminate Portfolio Swap' : '''
                                terminateDate;
                                '''
                    }
                ]
    
    def AdjustCashPane(self, *args):
        return [
                    {'Adjust Cash' : '''
                            adjustCashAmount;
                            adjustCashCurrency;
                            adjustCashDate;
                            '''
                    }
                ]
                
    def PeriodToDateFromToday(self, attributeName, date):
        return self.DateAdjustPeriod(acm.Time.DateToday(), date)
    
    def PeriodToStartDateTransform(self, attributeName, startDate):
        return self.DateAdjustPeriod(self.Instrument().StartDate(), startDate)

    def StartDateValidate(self, attributeName, startDate):
        if attributeName == 'regenerateStartDate':
            self.ValidateStartEndDates(startDate, self.DealPackage().GetAttribute('regenerateEndDate'))
        else:
            self.ValidateStartEndDates(startDate, self.DealPackage().GetAttribute('expiryDate'))
            
    def PeriodToEndDateTransform(self, attributeName, endDate):
        return self.DateAdjustPeriod(self.DealPackage().GetAttribute('regenerateStartDate'), endDate)
 
    def EndDateValidate(self, attributeName, endDate):
        if attributeName == 'rollExpiryDate':
            self.ValidateStartEndDates(self.DealPackage().GetAttribute('terminateDate'), endDate)
        elif attributeName == 'regenerateEndDate':
            self.ValidateStartEndDates(self.DealPackage().GetAttribute('regenerateStartDate'), endDate)
        else:
            self.ValidateStartEndDates(self.DealPackage().GetAttribute('startDate'), endDate)
        
    def DateAdjustPeriod(self, fromDate, period):
        if acm.Time().PeriodSymbolToDate(period):
            return acm.Time().DateAdjustPeriod(fromDate, period)
        return period
            
    def ValidateStartEndDates(self, startDate, endDate):
        if not endDate:
            raise DealPackageUserException('End date should be specified')
        if not startDate:
            raise DealPackageUserException('Start date should be specified')
        if acm.Time.DateDifference(startDate, endDate) > 0:
            raise DealPackageUserException('Can not have end date before start date')
        
    #Object Mapping Methods
    def Instrument(self):
        return self.InstrumentAt('PrfSwap')
        
    def Trade(self):        
        return self.TradeAt('PrfSwap')
        
    def LeadTrade(self):
        return self.Trade()
               
    def MetaInstrument(self):
        return self.InstrumentAt('MetaLegs')
    
    def TradeOid(self, *args):
        trdNbr = self.Trade().OriginalOrSelf().Oid()
        return trdNbr if trdNbr > 0 else ''
    
    def MetaLegs(self):
        return self.MetaInstrument().Legs()
        
    def MetaLegsNoUPL(self):
        legs=self.MetaInstrument().Legs().AsArray()
        for leg in legs:
            if self.IsCategoryChlItem(leg, PortfolioSwapMetaLegs.LEG_CATEGORY_PERFORMANCE_UPL):
                legs.Remove(leg)
        return legs     
            
    def IsCategoryChlItem(self, leg, categoryChlItem):
        legCategory = leg.CategoryChlItem() if leg else None
        return legCategory is not None and legCategory == categoryChlItem
        
    def FinancingMetaLeg(self, *args):
        for leg in self.MetaLegs():
            if self.IsCategoryChlItem(leg, PortfolioSwapMetaLegs.LEG_CATEGORY_FINANCING):
                return acm.FBusinessLogicDecorator.WrapObject(leg, self.MetaInstrument().GUI())
        return self.DummyLeg()
        
    def PerformanceMetaLeg(self, *args):
        for leg in self.MetaLegs():
            if self.IsCategoryChlItem(leg, PortfolioSwapMetaLegs.LEG_CATEGORY_PERFORMANCE):
                return acm.FBusinessLogicDecorator.WrapObject(leg, self.MetaInstrument().GUI())
        return self.DummyLeg()

    def PerformanceDividendMetaLeg(self, *args):
        dividendLeg = None
        if self.enableNoPerformanceSplit:
            dividendLeg = self.PerformanceMetaLeg()
        else:
            dividendLeg = self.PerformanceRPLMetaLeg()
        return dividendLeg
        
    def PerformanceUPLMetaLeg(self, *args):
        for leg in self.MetaLegs():
            if self.IsCategoryChlItem(leg, PortfolioSwapMetaLegs.LEG_CATEGORY_PERFORMANCE_UPL):
                return acm.FBusinessLogicDecorator.WrapObject(leg, self.MetaInstrument().GUI())
        return self.DummyLeg()
        
    def PerformanceRPLMetaLeg(self, *args):
        for leg in self.MetaLegs():
            if self.IsCategoryChlItem(leg, PortfolioSwapMetaLegs.LEG_CATEGORY_PERFORMANCE_RPL):
                return acm.FBusinessLogicDecorator.WrapObject(leg, self.MetaInstrument().GUI())
        return self.DummyLeg()
        
    def StockBorrowMetaLeg(self, *args):
        for leg in self.MetaLegs():
            if self.IsCategoryChlItem(leg, PortfolioSwapMetaLegs.LEG_CATEGORY_STOCK_BORROW):
                return leg
        return self.DummyLeg()

    def SyntheticCashMetaLeg(self, *args):
        for leg in self.MetaLegs():
            if self.IsCategoryChlItem(leg, PortfolioSwapMetaLegs.LEG_CATEGORY_SYNTHETIC_CASH):
                return acm.FBusinessLogicDecorator.WrapObject(leg, self.MetaInstrument().GUI())
        return self.DummyLeg()
        
    def FeeMetaLeg(self, *args):
        for leg in self.MetaLegs():
            if self.IsCategoryChlItem(leg, PortfolioSwapMetaLegs.LEG_CATEGORY_FEE):
                return leg
        return self.DummyLeg()
            
    def ClientSpreadIndex(self):
        return self.InstrumentAt('clientSpreadIndex')
    
    def SyntheticPortfolioCurrency(self, *args):
        if self.syntheticPortfolio:
            return self.syntheticPortfolio.Currency()
        else:
            return None

    #Changed callbacks
    def NameChanged(self, attrName, previousName, newName, *args):
        if previousName != newName:
            self.SetAndValidateInstrumentNames()
        
    def StartDateChanged(self, attrName, previousDate, newDate, *args):
        if newDate:
            self.rollingBaseDate = newDate
                    
    def ClientLongSpreadChanged(self, attrName, previousSpread, newSpread, *args):
        if self.clientSpreadPrice:
            bidPrice = newSpread
            if bidPrice != 0:
                bidPrice = bidPrice/100.0
            self.clientSpreadPrice.Bid(bidPrice)
            self.clientSpreadPrice.Day(acm.Time().DateToday())
            self.Touch()
     
    def ClientShortSpreadChanged(self, attrName, previousSpread, newSpread, *args):
        if self.clientSpreadPrice:
            askPrice = newSpread
            if askPrice != 0:
                askPrice = askPrice/100.0
            self.clientSpreadPrice.Ask(askPrice)
            self.clientSpreadPrice.Day(acm.Time().DateToday())
            self.Touch()
        
    def PerformTouch(self, attrName, previousValue, newValue, *args):
        if previousValue and previousValue != newValue:
            self.Touch()
    
    def Touch(self):
        self.DealPackage().DealPackage().Touch()
        self.DealPackage().DealPackage().Changed()
        
    def SyntheticPortfolioChanged(self, attrName, previousSyntheticPortfolio, newSyntheticPortfolio, *args):
        if newSyntheticPortfolio:
            self.SetMatchingMethodFromSyntheticPortfolio()
            self.synthPrfCurr=self.syntheticPortfolio.Currency()
            self.currency=self.syntheticPortfolio.Currency()
            self.equityCurr=self.syntheticPortfolio.Currency()
            self.UpdateFilteredPortfolio()

    def UpdateStockBorrowEnabledChanged(self, attrName, previouslyEnabled, nowEnabled, *args):
        self.UpdateStockBorrowMetaLegEnabled()
        self._RegisterAllObjectMappings()
        self.Touch()
        
    def UpdateNoPerformanceSplitEnabledChanged(self, attrName, previouslyEnabled, nowEnabled, *args):
        self.UpdateUplRplPerformanceMetaLegEnabled()
        self._RegisterAllObjectMappings()
        self.Touch()
        
    def UpdateSyntheticCashEnabledChanged(self, attrName, previouslyEnabled, nowEnabled, *args):
        self.UpdateSyntheticCashMetaLegEnabled()
        self._RegisterAllObjectMappings()
        self.Touch()
        
    def UpdateDayCount(self, attrName, previousValue, newValue, *args):
        self.dayCountMethod = newValue.DayCountMethod()
        
    def UpdatePayCalendars(self, attrName, previousValue, newValue, *args):
        calendar = newValue.LongestLeg().PayCalendar()
        self.payCalendar = calendar
        
    def UpdateResetCalendars(self, attrName, previousValue, newValue, *args):
        calendar = newValue.LongestLeg().PayCalendar()
        self.stockBorrowResetCalendar = calendar
        self.performanceResetCalendar = calendar
        self.FeeMetaLeg().ResetCalendar = calendar
        
    #Appearance Methods
    def PortfolioSwapIsTerminated(self, *args):
        return self.openEnd == 'Terminated'
    
    def FinancingLegSpreadFixingEnabled(self, *args):
        return self.financingSpreadFixings
        
    def PayOffsetEnabled(self, *args):
        return not self.SyntheticCashVisible()
        
    def PayOffsetVisible(self, *args):
        return self.IsShowModeDetail() and not self.SyntheticCashVisible()
        
    def StockBorrowVisible(self, *args):
        return self.stockBorrowEnabled

    def PassTypeNotNone(self, *args):
        return self.performancePassType != "None"
        
    def UplRplSplitEnabled(self, *args):
        return not self.enableNoPerformanceSplit and self.HasLegCategoryUPL()

    def HasLegCategoryUPL(self, *args):
        return self.IsShowModeDetail() and PortfolioSwapMetaLegs.LEG_CATEGORY_PERFORMANCE_UPL is not None

    def NoUplRplSplitEnabled(self, *args):
        return self.IsShowModeDetail() and self.enableNoPerformanceSplit

    def PayOffsetVisibleAndNoUplRplSplitEnabled(self, *args):
        return self.NoUplRplSplitEnabled() and not self.SyntheticCashVisible()

    def PayOffsetVisibleAndUplRplSplitEnabled(self, *args):
        return self.UplRplSplitEnabled() and not self.SyntheticCashVisible()

    def StockBorrowPayOffsetVisible(self, attrName):
        return self.StockBorrowVisible() and self.PayOffsetVisible()
    
    def StockBorrowShowInDetail(self, *args):
        return self.StockBorrowVisible() and self.IsShowModeDetail()
    
    def StockBorrowShowInDetailBool(self, attrName):
        return self.StockBorrowVisible() and self.ShowInDetailBool(attrName)
    
    def ShowInDetailBool(self, attrName):
        return self.IsShowModeDetail() or self.GetAttribute(attrName)
    
    def SyntheticCashVisible(self, *args):
        return self.cashEnabled
    
    def SyntheticCashShowInDetail(self, *args):
        return self.SyntheticCashVisible() and self.IsShowModeDetail()
        
    def FinancingHasWeightedResets(self, *args):
        return self.financingResetType == 'Weighted'

    def CashHasWeightedResets(self, *args):
        return self.SyntheticCashVisible(*args) and self.cashResetType == 'Weighted'
        
    def SyntheticPortfolioChosen(self, *args):
        if self.syntheticPortfolio:
            return True
        else:
            return False
        

    #Choices Methods
    def CashRateIndexChoices(self, *args):
        if self.m_cashRateIndexChoices.IsEmpty():
            self.UpdateCashRateIndexChoices()
        return self.m_cashRateIndexChoices
        
    def FinancingRateIndexChoices(self, *args):
        if self.m_financingRateIndexChoices.IsEmpty():
            self.UpdateFinancingRateIndexChoices()
        return self.m_financingRateIndexChoices
        
    def RateIndexChoicesImpl(self, curr = None):
        selectQ = ''
        rateIndices = acm.FRateIndex.Select('')
        if curr:
            rateIndices = acm.FFilteredSet(rateIndices)
            filter = acm.Filter.SimpleAndQuery(acm.FInstrument, ['Currency'], ['EQUAL'], curr.Name())
            rateIndices.Filter(filter)
        rateIndices = rateIndices.AsArray()
        return rateIndices
    
    def UpdateCashRateIndexChoices(self, *args):
        self.m_cashRateIndexChoices.Clear()
        rateIndices = self.RateIndexChoicesImpl(self.currency)
        if rateIndices.Size():
            self.m_cashRateIndexChoices.AddAll(rateIndices)
            if self.cashFloatRateRef and self.cashFloatRateRef not in self.m_cashRateIndexChoices.Source():
                floatRef = None
                for rateIndex in rateIndices:
                    if rateIndex.LongestLeg().EndPeriod() == '1d':
                        floatRef = rateIndex
                if floatRef:
                    self.cashFloatRateRef = floatRef
                else:
                     self.cashFloatRateRef = self.m_cashRateIndexChoices.First()
               
    def UpdateFinancingRateIndexChoices(self, *args):
        self.m_financingRateIndexChoices.Clear()
        rateIndices = self.RateIndexChoicesImpl(self.synthPrfCurr)
        if rateIndices.Size():
            self.m_financingRateIndexChoices.AddAll(rateIndices)
            if self.financingFloatRateRef and self.financingFloatRateRef not in self.m_financingRateIndexChoices.Source():
                floatRef = None
                for rateIndex in rateIndices:
                    if rateIndex.LongestLeg().EndPeriod() == '1d':
                        floatRef = rateIndex
                if floatRef:
                    self.financingFloatRateRef = floatRef
                else:
                    self.financingFloatRateRef = self.m_financingRateIndexChoices.First()    
        
    def CurrencyChoices(self, *args):
        return acm.FCurrency.Select('')
        
    def PassTypeChoices(self, *args):
        return ['None', 'Dividend Payday', 'CashFlow Payday']
    
    def CounterpartyChoices(self, *args):
        validCounterParties = acm.FParty.Select("type = 'Counterparty'").AsArray()
        return validCounterParties
        
    def MatchingMethodChoices(self, *args):
        return acm.FAccountingParameters.Instances()
        
    def Context(self, *args):
        try:
            from PortfolioSwapDealPackageCustomization import GetContext
            context = GetContext(self.DealPackage())
        except:
            context = 'Global'
        return context

    def DayOffsetMethodChoices(self, *args):
        return ['None', 'Following', 'Preceding', 'Mod. Following', 'Mod. Preceding']
        
    def ResetTypeChoices(self, *args):
        return ['None', 'Simple Overnight', 'Single', 'Weighted']
        
        
    #Attribute Callbacks       
    def TransformStartPeriodToDate(self, name, newDate):
        date = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            date = self.Instrument().StartDateFromPeriod(newDate)
        return date
    
    def TransformExpPeriodToDate(self, name, newDate):
        date = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            decoNoGUI = acm.FBusinessLogicDecorator.WrapObject(self.Instrument().Instrument())
            date = decoNoGUI.ExpiryDateFromPeriod(newDate)
        return date
        
        
    #Actions
    def Terminate(self, _, date = None):
        return Terminate(DealPackageParameters(self.DealPackage()), date)
        
    def RegenerateAll(self, *args):
    
        def BetweenDates():
            startDate = self.Instrument().StartDate()
            endDate = acm.Time().DateToday()
            if args:
                if 2 == len(args):
                    endDate = args[1]
                if 3 == len(args):    
                    startDate = args[1]
                    endDate = args[2]
            return [startDate, endDate]
            
        self.UpdateStockBorrowMetaLegEnabled()
        self.UpdateUplRplPerformanceMetaLegEnabled()
        self.UpdateSyntheticCashMetaLegEnabled()
        parameters = DealPackageParameters(self.DealPackage())
        startDate, endDate = BetweenDates()
        GeneratePortfolioSwap(parameters, startDate, endDate)
        
    def TradeAssign(self, _, date = None):
        date = date if date else acm.Time().DateToday()
        TradeAssign(DealPackageParameters(self.DealPackage()), date, date)

    def LegPerSecurityAndType(self, _, security, type):
        for leg in self.Instrument().Legs():
            if leg.CategoryChlItem() == type and leg.IndexRef() == security:
                return leg
        return None
     
    def SweepCash(self, _, date = None):
        date = date if date else acm.Time().DateToday()
        SweepCash(DealPackageParameters(self.DealPackage()), date)
    
    def Roll(self, _, date = None, newName = None, terminateDate = None):
        return Roll(DealPackageParameters(self.DealPackage()), date, newName, terminateDate)

    def AdjustCash(self, _, amount = None, currency = None, date = None):
        AdjustCash(DealPackageParameters(self.DealPackage()), amount, currency, date)

    def Extend(self, _, startDate = None):
        startDate = startDate if startDate else acm.Time().DateToday()
        Extend(DealPackageParameters(self.DealPackage()), startDate)

    def Fix(self, _, startDate = None):
        startDate = startDate if startDate else acm.Time().DateToday()
        Fix(DealPackageParameters(self.DealPackage()), startDate)
      
    def ClientSpreadInstrument(self, *args):
        return self.ClientSpreadIndex().Instrument()
    
    def SecuritySpreadInstrument(self, _, security):
        try:
            from PortfolioSwapDealPackageCustomization import GetSecuritySpreadRateIndex
            return GetSecuritySpreadRateIndex(security)
        except:
            pass
        return None
    
    def IsExtended(self, *args):
        leg = self.Instrument().LongestLeg()
        return leg and leg.EndDate() >= acm.Time().DateToday()
    
    #Misc.        
    def SetComponentNames(self):
        if not self.name:
            self.DealPackage().SuggestName()
        self.SetAndValidateInstrumentNames()

    def SetAndValidateInstrumentNames(self):
        name = self.DealPackage().InstrumentPackage().Name()
        if name:
            self.Instrument().Name(name)
            self.DealPackage().InstrumentAt('MetaLegs').Name('ML_'+name)
            self.DealPackage().InstrumentAt('clientSpreadIndex').Name('CL_'+name)
    
    def GetClientSpreadRateIndexMarket(self):
        try:
            from PortfolioSwapDealPackageCustomization import GetClientSpreadRateIndexMarket
            market = GetClientSpreadRateIndexMarket()
        except:
            market = acm.FParty['SPOT']
        return market
            
    def FindClientSpreadIndexPrice(self):
        for price in self.ClientSpreadInstrument().Originator().Prices():
            if price.Market() == self.GetClientSpreadRateIndexMarket():
                return price.StorageImage()
        return None
        
    def FindOrCreateClientSpreadIndexPrice(self):
        price = self.FindClientSpreadIndexPrice()
        if not price:
            price = self.CreateNewPriceImpl(self.ClientSpreadInstrument())
        return price
            
    def SetClientSpreadOnOpen(self):
        price = self.FindOrCreateClientSpreadIndexPrice()
        self.DealPackage().SetAttribute('clientLongSpread', price.Bid()*100)
        self.DealPackage().SetAttribute('clientShortSpread', price.Ask()*100)
        self.DealPackage().SetAttribute('clientSpreadPrice', price)
            
    def SetMatchingMethodFromSyntheticPortfolio(self):
        matchingMethod = None
        if self.syntheticPortfolio:
            matchingMethod = self.syntheticPortfolio.MappedAccountingParametersLink().Link().Name()
        self.DealPackage().SetAttribute('matchingMethod', matchingMethod)
        
    def StockBorrowLegIsValid(self):
        return self.IsCategoryChlItem(self.StockBorrowMetaLeg(), PortfolioSwapMetaLegs.LEG_CATEGORY_STOCK_BORROW)
        
    def PerformanceLegIsValid(self):
        return self.IsCategoryChlItem(self.PerformanceMetaLeg(), PortfolioSwapMetaLegs.LEG_CATEGORY_PERFORMANCE)
    
    def PerformanceUPLandRPLLegsAreValid(self):
        rplValid = self.IsCategoryChlItem(self.PerformanceRPLMetaLeg(), PortfolioSwapMetaLegs.LEG_CATEGORY_PERFORMANCE_RPL)
        uplValid = self.IsCategoryChlItem(self.PerformanceUPLMetaLeg(), PortfolioSwapMetaLegs.LEG_CATEGORY_PERFORMANCE_UPL)
        return rplValid and uplValid
        
    def SyntheticCashLegIsValid(self):
        return self.IsCategoryChlItem(self.SyntheticCashMetaLeg(), PortfolioSwapMetaLegs.LEG_CATEGORY_SYNTHETIC_CASH)
        
    def SetStockBorrowSpreadEnabled(self):
        self.stockBorrowEnabled = self.StockBorrowLegIsValid()
    
    def SetPerformanceUplRplSplitEnabled(self):
        self.enableNoPerformanceSplit = self.PerformanceLegIsValid()
        
    def SetCashEnabled(self):
        self.cashEnabled = self.SyntheticCashLegIsValid()
                
    def MatchingMethodLink(self):
        link = None
        if self.syntheticPortfolio:
            context = self.ContextAsString()
            query = "context = '" + context + "' and portfolio = '" + self.syntheticPortfolio.Name() + "' and type = 'Accounting parameter' and mappingType = 'Portfolio'"
            link = acm.FContextLink.Select01(query, '')
            if link:
                link = link.StorageImage()
            else:
                link = acm.FContextLink()
                link.Context(context)
                link.Type('Accounting Parameter')
                link.MappingType('Portfolio')
                link.Portfolio(self.syntheticPortfolio)
            link.Name(self.matchingMethod)
        return link

    def ContextAsString(self):
        cntx = self.Context()
        if not isinstance(cntx, basestring):
            cntx = cntx.Name()
        return cntx

    def CreateNewPriceImpl(self, clientSpreadIndex):
        newPriceRecord = acm.FPrice()
        newPriceRecord.RegisterInStorage()
        newPriceRecord.Instrument(clientSpreadIndex)
        newPriceRecord.Currency(clientSpreadIndex.Currency())
        newPriceRecord.Market(self.GetClientSpreadRateIndexMarket())
        newPriceRecord.Day(acm.Time().DateToday())
        longSpread = self.clientLongSpread
        if longSpread != 0:
            longSpread = longSpread/100.0
        shortSpread = self.clientShortSpread
        if shortSpread != 0:
            shortSpread = shortSpread/100.0
        newPriceRecord.Bid(longSpread)
        newPriceRecord.Ask(shortSpread)
        newPriceRecord.Bits(1027)
        return newPriceRecord
        
    def CreateNewPrice(self, clientSpreadIndex):
        self.DealPackage().SetAttribute('clientSpreadPrice', self.CreateNewPriceImpl(clientSpreadIndex))
  
    def GetAdditionalSaveRecords(self):
        addRecords = acm.FArray()
        if self.clientSpreadPrice and self.MatchingMethodLink():
            addRecords.Add(self.clientSpreadPrice)
            addRecords.Add(self.MatchingMethodLink())
        addRecords.Add(self.syntheticPortfolio)
        return addRecords
        
    def ValidateOrCreateStockBorrowLeg(self):
        if not self.StockBorrowLegIsValid():
            PortfolioSwapMetaLegs.CreateNewStockBorrowMetaLeg(self.MetaInstrument())
            self._RepairDivergingMapping( self.StockBorrowMetaLeg() )
            self.RestoreDefaultValues('stockBorrowRolling')
            
    def ValidateOrCreatePerformanceLeg(self):
        if not self.PerformanceLegIsValid():    
            try:
                stockSelectQ = PortfolioSwapMetaLegs.StockSelectQuery(self.Instrument())
                defaultStock = acm.FInstrument.Select(stockSelectQ).First()
            except:
                raise DealPackageUserException('Cannot create Meta Legs - No valid default Stock available in ADS')

            PortfolioSwapMetaLegs.CreateNewPerformanceMetaLeg(self.MetaInstrument(), defaultStock)
            self.RestoreDefaultValues('performanceRolling',
                                      'performanceRollingBaseDate',
                                      'performancePayOffset',
                                      'performanceResetCalendar')
            self._RepairDivergingMapping( self.PerformanceMetaLeg() )

    def ValidateOrCreateUPLandRPLLegs(self):
        if not self.PerformanceUPLandRPLLegsAreValid():
            try:
                stockSelectQ = PortfolioSwapMetaLegs.StockSelectQuery(self.Instrument())
                defaultStock = acm.FInstrument.Select(stockSelectQ).First()
            except:
                raise DealPackageUserException('Cannot create Meta Legs - No valid default Stock available in ADS')
  
            PortfolioSwapMetaLegs.CreateNewPerformanceRPLMetaLeg(self.MetaInstrument(), defaultStock)
            PortfolioSwapMetaLegs.CreateNewPerformanceUPLMetaLeg(self.MetaInstrument(), defaultStock)
        
            self.RestoreDefaultValues('rplPerformanceRolling',
                                      'rplPerformanceRollingBaseDate',
                                      'rplPerformancePayOffset',
                                      'rplPerformanceResetCalendar',
                                      'uplPerformanceRolling',
                                      'uplPerformanceRollingBaseDate',
                                      'uplPerformancePayOffset',
                                      'uplPerformanceResetCalendar')
                                      
            self.performanceTaxHandling = 'None'
            self._RepairDivergingMapping( self.PerformanceRPLMetaLeg() )
            self._RepairDivergingMapping( self.PerformanceUPLMetaLeg() )

    def ValidateOrCreateSyntheticCashLeg(self):
        if not self.SyntheticCashLegIsValid():
            PortfolioSwapMetaLegs.CreateNewSyntheticCashMetaLeg(self.MetaInstrument())
            self._RepairDivergingMapping( self.SyntheticCashMetaLeg() )
            self.RestoreDefaultValues('cashFloatRateRef',
                                      'cashResetType',
                                      'cashRolling',
                                      'cashRollingBaseDate')
    
    def _RepairDivergingMapping(self, leg):
        if self.dayCountMethod:
            leg.DayCountMethod = self.dayCountMethod
        else:
            leg.DayCountMethod = self.currency.DayCountMethod()
        leg.ResetDayMethod = self.dayOffsetMethod
        leg.PayDayMethod = self.dayOffsetMethod
        if self.payCalendar:
            leg.PayCalendar = self.payCalendar
        else: 
            leg.PayCalendar = self.currency.LongestLeg().PayCalendar()
        if self.resetCalendar:
            leg.ResetCalendar = self.resetCalendar
        else:
            if self.IsCategoryChlItem(leg, PortfolioSwapMetaLegs.LEG_CATEGORY_STOCK_BORROW):
                leg.ResetCalendar = self.equityCurr.LongestLeg().PayCalendar()
            else:
                leg.ResetCalendar = self.currency.LongestLeg().PayCalendar()
        if self.payOffset:
            leg.PayOffset = self.payOffset
        else:
            leg.PayOffset = '0d'
        leg.RollingPeriodBase = self.startDate
                                 
    def RemoveStockBorrowLeg(self):
        PortfolioSwapMetaLegs.RemoveStockBorrowMetaLeg(self.MetaInstrument())
    
    def RemovePerformanceUPLandRPLLeg(self):
        PortfolioSwapMetaLegs.RemovePerformanceUPLMetaLeg(self.MetaInstrument())
        PortfolioSwapMetaLegs.RemovePerformanceRPLMetaLeg(self.MetaInstrument())
        
    def RemovePerformanceLeg(self):
        PortfolioSwapMetaLegs.RemovePerformanceMetaLeg(self.MetaInstrument())
        
    def RemoveSyntheticCashBorrowLeg(self):
        PortfolioSwapMetaLegs.RemoveSyntheticCashMetaLeg(self.MetaInstrument())
        
    def UpdateStockBorrowMetaLegEnabled(self):
        if self.stockBorrowEnabled:
            self.ValidateOrCreateStockBorrowLeg()
        else:
            self.RemoveStockBorrowLeg()
    
    def UpdateUplRplPerformanceMetaLegEnabled(self):
        if self.enableNoPerformanceSplit:
            self.ValidateOrCreatePerformanceLeg()
            self.RemovePerformanceUPLandRPLLeg()
        else:
            self.ValidateOrCreateUPLandRPLLegs()
            self.RemovePerformanceLeg()
            
    def UpdateSyntheticCashMetaLegEnabled(self):
        if self.cashEnabled:
            self.ValidateOrCreateSyntheticCashLeg()
        else:
            self.RemoveSyntheticCashBorrowLeg()

    def RegenerateIfNotHistorical(self, saveConfig):
        startDate=self.startDate
        if self.GetAttribute('financingSpreadFixings') and self.startDate<acm.Time().DateToday():
            if saveConfig.DealPackage() == 'SaveNew':
                ClearFeeDividendAndSyntheticCashflows(self.Instrument(), startDate)
                ClearPerformanceFinancingAndStockBorrowCashflows(self.Instrument(), startDate)
                ClearPortfolioSwapLegs(self.Instrument(), startDate)
                acm.Log('Historical prices missing for client spread rate index '+self.ClientSpreadIndex().Name()+'. Add prices and then regenerate portfolio swap.')
        else:
            endDate=acm.Time().DateToday()
            self.RegenerateAll(None, startDate, endDate)
            
    #Deal Package Proxy Methods        
    def OnInit(self):
        self.m_cashRateIndexChoices = DealPackageChoiceListSource()
        self.m_financingRateIndexChoices = DealPackageChoiceListSource()
        self.m_filteredPortfolio = None
        self.m_filteredPortfolioQueryFolder = None
        self.m_dummyLeg = None

    def DummyLeg(self):
        if self.m_dummyLeg is None:
            bond = acm.FBond()
            leg = acm.FLeg()
            leg.Instrument(bond)
            self.m_dummyLeg = acm.FBusinessLogicDecorator.WrapObject(leg)
        return self.m_dummyLeg
        
    def OnOpen(self):
        with MuteNotificationsWithSafeExit(self):
            self.SetClientSpreadOnOpen()
            self.SetStockBorrowSpreadEnabled()
            self.SetCashEnabled()
            self.SetMatchingMethodFromSyntheticPortfolio()
        self.SetPerformanceUplRplSplitEnabled()
        self.synthPrfCurr = self.Instrument().FundPortfolio().Currency()
            
    def OnCopy(self, originalDealPackage, anAspectSymbol):
        if not self.clientSpreadPrice.IsInfant():
            self.clientSpreadPrice = self.clientSpreadPrice.StorageImage()
        self.clientSpreadPrice.Instrument(self.ClientSpreadInstrument())
        self.matchingMethod = originalDealPackage.GetAttribute('matchingMethod')
            
    def OnSave(self, saveConfig):
        if saveConfig.DealPackage() == 'SaveNew':
            saveConfig.InstrumentPackage('SaveNew')
            SetNew(self.Trades(),
                        self.Instruments())
            self.CreateNewPrice(self.ClientSpreadInstrument())
        self.SetComponentNames()
        self.UpdateStockBorrowMetaLegEnabled()
        self.UpdateUplRplPerformanceMetaLegEnabled()
        self.UpdateSyntheticCashMetaLegEnabled()
        self._RegisterAllObjectMappings()
        if (saveConfig.DealPackage() == 'SaveNew' or self.DealPackage().IsInfant()):
            self.RegenerateIfNotHistorical(saveConfig)
        return {'commit':self.GetAdditionalSaveRecords(),
                'delete':[]}
        
    def AssemblePackage(self):
    
        def AddPortfolioSwapToPackage():
            portfolioSwap = acm.DealCapturing().CreateNewInstrument('Portfolio Swap')
            portfolioSwapTrade = acm.DealCapturing().CreateNewTrade(portfolioSwap)
            portfolioSwapTrade.Quantity(-1)
            self.DealPackage().AddTrade(portfolioSwapTrade, 'PrfSwap')

        def AddNewMetaLegDataToPackage():
            cfeInstrument = PortfolioSwapMetaLegs.CreateDefaultLegs()
            self.DealPackage().AddInstrument(cfeInstrument, 'MetaLegs')
            
        def AddNewClientSpreadRateIndexToPackage():
            clientSpreadIndex = acm.DealCapturing().CreateNewInstrument('Rate Index')
            clientSpreadIndex.MtmFromFeed(True)
            self.CreateNewPrice(clientSpreadIndex)         
            self.DealPackage().AddInstrument(clientSpreadIndex, 'clientSpreadIndex')

        def SetDefaultAttributes():
            package = self.DealPackage()
            stockBorrowDefaultEnabled = acm.GetDefaultValueFromName(acm.GetDefaultContext(), 'FObject', 'StockBorrowSpreadCustomImplementation') != None
            package.SetAttribute('stockBorrowEnabled', stockBorrowDefaultEnabled)
            
        def CreateDefaultPortfolioSwapPackage():    
            AddPortfolioSwapToPackage()
            AddNewMetaLegDataToPackage()
            AddNewClientSpreadRateIndexToPackage()
            SetDefaultAttributes()

        CreateDefaultPortfolioSwapPackage()

    def OnDelete(self, allTrades):
        deleteObjects = []
        if allTrades:
            deleteObjects.append(self.DealPackage().InstrumentPackage())
            deleteObjects.extend(self.DealPackage().Instruments())
        return {'commit':[],
                'delete':deleteObjects}
                
    def Refresh(self):
        pass
        
    def IsValid(self, exceptionAccumulator, aspect):
        if self.syntheticPortfolio and self.syntheticPortfolio.Originator() == self.portfolio:
            exceptionAccumulator('Portfolio cannot be equal to Synthetic Portfolio')
        
    def SuggestName(self):
        currName = self.currency.Name() if self.currency else ''
        counterName = self.counterparty.Name() if self.counterparty else ''
        name = currName + '/PS/' + counterName
        return name
    
    def TransformPeriodToDate(self, name, date):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date
        
    def UpdateFilteredPortfolio(self):
        queryFolder = self.FilteredPortfolioQueryFolderImpl()
        if queryFolder:
            self.m_filteredPortfolioQueryFolder = queryFolder
            self.m_filteredPortfolio = acm.FASQLPortfolio(queryFolder)
            self.m_filteredPortfolio.Currency(self.syntheticPortfolio.Currency())
    
    def FilteredPortfolioQueryFolderImpl(self):
        def _CallMethodChain(obj, methodChain):
            chainAsList = methodChain.split('.')
            for method in chainAsList:
                if obj:
                    obj = getattr(obj, method)()
                else:
                    return None
            return obj
        
        def AddExtensionValueConstraints(query):
            filterMaps = acm.DealCapturing.CreatePrfSwapFilterMaps()
            for filterMap in filterMaps:
                criteriaPair = filterMap.Second()
                resultExpr = str(criteriaPair.First())
                attr = str(criteriaPair.Second())
                result = _CallMethodChain(self, resultExpr)
                if not result:
                    result = 0
                    attr = re.sub(r"(\.Name$)|(\.Cid$)", '.Oid', attr)
                query.AddAttrNode(attr, 'EQUAL', result)
            return filterMaps.Size() > 0
        
        def AddPortfolioConstraint(query):
            portfolioNode = query.AddOpNode('OR')
            allPortfolios = acm.FArray()
            if self.syntheticPortfolio.IsKindOf(acm.FCompoundPortfolio):
                allPortfolios = self.syntheticPortfolio.AllPhysicalPortfolios()
            else:
                allPortfolios.Add(self.syntheticPortfolio)
            for portfolio in allPortfolios:
                portfolioNode.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())

        if self.syntheticPortfolio:
            query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
            isFiltered = AddExtensionValueConstraints(query)
            query.AddAttrNode('Instrument.Cid', 'NOT_EQUAL', 'Portfolio Swap')
            AddPortfolioConstraint(query)
            
            prfCaption = self.syntheticPortfolio.Name() + ' (Filtered)' if isFiltered else self.syntheticPortfolio.Name()
            folder = acm.FASQLQueryFolder()
            folder.AsqlQuery(query)
            folder.Name(prfCaption)
            return folder
        else:
            return None
    
    @ReturnDomainDecorator('string')
    def BuySell(self, value = '*Reading*'):
        if value == '*Reading*':
            if self.Trade().Quantity() == -1:
                return 'Sell'
            elif self.Trade().Quantity() == 1:
                return 'Buy'
            else:
                raise DealPackageUserException('Invalid Quantity. It should be -1 or 1')
        else:
            if value == 'Sell':
                self.Trade().Quantity(-1)
            elif value == 'Buy':
                self.Trade().Quantity(1)
                
    @ReturnDomainDecorator('FPortfolio')
    def FilteredPortfolio(self, value='*READING*'):
        if value == '*READING*':
            if not self.m_filteredPortfolioQueryFolder:
                self.UpdateFilteredPortfolio()
            return self.m_filteredPortfolio
        else:
            pass
    
    @ReturnDomainDecorator('FASQLQueryFolder')
    def FilteredPortfolioQueryFolder(self, value='*READING*'):
        if value == '*READING*':
            return self.m_filteredPortfolioQueryFolder
        else:
            pass
        
    @classmethod
    @FUxCore.aux_cb
    def SetUp(cls, definitionSetUp):
        from DealPackageSetUp import ChoiceListSetUp
        entries = ['Dividend', 'Fee', 'Financing', 'Performance', 'Performance RPL', 
                   'Performance UPL', 'Stock Borrow', 'Synthetic Cash']
        for entry in entries:
            definitionSetUp.AddSetupItem(
                                ChoiceListSetUp(
                                    list='Leg Category', 
                                    entry=entry, 
                                    descr='')
            )
        try:
            from PortfolioSwapDealPackageCustomization import SetUpCustomizedPortfolioSwapDefinition
        except:
            return 
        SetUpCustomizedPortfolioSwapDefinition(definitionSetUp)
        
