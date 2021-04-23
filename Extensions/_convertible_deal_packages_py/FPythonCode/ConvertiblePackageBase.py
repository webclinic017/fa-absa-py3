""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ConvertibleDealPackages/etc/ConvertiblePackageBase.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    ConvertiblePackageBase

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import FAssetManagementUtils
from DealPackageDevKit import DealPackageDefinition, Date, Str, Object, Float, Action, DealPackageException, Settings, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, TradeActions, CorrectCommand, NovateCommand, CloseCommand
from TraitBasedDealPackage import MuteNotificationsWithSafeExit
from FAscotUtils import SwapFromConvertibleCreator
from FAscotValuationFunctions import SetRecallSwap
import ConvertiblePackageUtils as utils
import ConvertiblePackageHooks as hooks
from CompositeAttributes import PaymentsDialog

logger = FAssetManagementUtils.GetLogger()

class ConvertibleDealPackageException(Exception):
    pass

@TradeActions( correct = CorrectCommand(statusAttr='status', newStatus='FO Confirmed'),
               novate = NovateCommand(nominal='nominal'),
               close  = CloseCommand(nominal='nominal'))
@Settings(ShowSheetInitially=True, GraphApplicable=False, ShowGraphInitially=False, SheetDefaultColumns=['Instrument Type', 'Trade Nominal', 'Portfolio Currency'])
class ConvertiblePackageBase(DealPackageDefinition):
    # pylint: disable-msg=R0904

    def __init__(self, *args, **kwds):
        DealPackageDefinition.__init__(self, *args, **kwds)
        self._customPaneName = ''
        self.insNew = None
        self.rateIndexChoices = acm.FArray()
        self.instrumentList = acm.FArray()
        # Create Addinfo Specs needed for Deal Packages
        self.CreateOnSwapDeltaAddinfoSpec()
                
    def OnNew(self):
        if self.GetAttribute('nominal'):
            self.SetAttribute('buySell', utils.BUY_SELL_MAP[self.GetAttribute('nominal')/abs(self.GetAttribute('nominal'))])
        else:
            self.SetAttribute('buySell', utils.BUY_SELL_MAP[self.GetAttribute('nominal')])            
        super(ConvertiblePackageBase, self).OnNew()    

    def OnOpen(self):
        self.SetBuySellButtonAtOnOpen()
        super(ConvertiblePackageBase, self).OnOpen()            

    def CreateOnSwapDeltaAddinfoSpec(self):
        FAssetManagementUtils.CreateAdditionalInfo("OnSwapDelta", "DealPackage", "Standard", "Double")

    def _GetDecoratedObjectIfExists(self, obj):
        if hasattr(obj, 'DecoratedObject'):
            return obj.DecoratedObject()
        return obj

    # Methods to access deal package parts
    def _GetInstrumentPart(self, name):
        # pylint: disable-msg=E1101
        ins = None
        try:
            ins = self.InstrumentAt(name)
        except DealPackageException as err:
            logger.debug('No %s "%s"' % (name, err))
        return ins

    def CB(self):
        cb = self._GetInstrumentPart('cb')
        if not cb:
            if not self.Ascot():
                raise ConvertibleDealPackageException('Ascot in dealpackage is None.')
            cb = self.Ascot().Underlying()
        return cb

    def Ascot(self):
        return self._GetInstrumentPart('ascot')

    def IRS(self):
        return self._GetInstrumentPart('irs')

    def Stock(self):
        return self._GetInstrumentPart('stock')

    def Option(self):
        return self._GetInstrumentPart('option')

    def CBLeg(self):
        return self.CB().Legs().First()

    def IRSPayLeg(self):
        return self.IRS().PayLeg()

    def IRSRecLeg(self):
        return self.IRS().RecLeg()

    def _GetTradePart(self, name):
    # pylint: disable-msg=E1101
        trade = None
        try:
            trade = self.TradeAt(name)
        except DealPackageException as err:
            logger.debug('No %s trade "%s"' % (name, err))
        return trade

    def CBTrade(self):
        return self._GetTradePart('cb')

    def AscotTrade(self):
        return self._GetTradePart('ascot')

    def IRSTrade(self):
        return self._GetTradePart('irs')

    def StockTrade(self):
        return self._GetTradePart('stock')

    def OptionTrade(self):
        return self._GetTradePart('option')

    def Instrument(self):
        return self._GetInstrumentPart('ins')

    def InsTrade(self):
        return self._GetTradePart('ins')

    def InsB2B(self):
        return self._GetB2BPart('ins')

    def _GetB2BPart(self, name):
    # pylint: disable-msg=E1101
        b2b = None
        try:
            b2b = self.B2BTradeParamsAt(name)
        except DealPackageException as err:
            logger.debug('No %s b2b "%s"' % (name, err))
        return b2b

    def CBB2B(self):
        return self._GetB2BPart('cb')

    def AscotB2B(self):
        return self._GetB2BPart('ascot')

    def IRSB2B(self):
        return self._GetB2BPart('irs')

    def StockB2B(self):
        return self._GetB2BPart('stock')

    def OptionB2B(self):
        return self._GetB2BPart('option')

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue(self._customPaneName)

    def Refresh(self):
    # pylint: disable-msg=E1002
        logger.debug('Refresh')
        super(ConvertiblePackageBase, self).Refresh()
        self.SetNewInsIfNeeded()

    def SetNewInsIfNeeded(self):
        pass

    def SuggestName(self):
    # pylint: disable-msg=E1101
        logger.debug('SuggestName')
        try:
            return hooks.SuggestName(self.DealPackage())
        except StandardError as err:
            logger.error('Failed to invoke "ConvertiblePackageHooks.SuggestName" hook: %s', err)

    def OnSave(self, config):
        super(ConvertiblePackageBase, self).OnSave(config)

    def OnSaveNew(self, config):
    # pylint: disable-msg=E1002
        logger.debug('OnSaveNew')
        super(ConvertiblePackageBase, self).OnSaveNew(config)

    def AssemblePackage(self):
    # pylint: disable-msg=E1002
        logger.debug('OnNew')
        super(ConvertiblePackageBase, self).OnNew()
        self.Refresh()

    def IsValid(self, errorAccumulator, aspect):
    # pylint: disable-msg=E1002
        logger.debug('IsValid')
        super(ConvertiblePackageBase, self).IsValid(errorAccumulator, aspect)

    def _ForceUpdateOfAttribute(self, dealPackage, attribute):
        methodName = '_' + attribute + '_changed'
        m = None
        try:
            m = getattr(self, methodName)
            m(attribute, None, dealPackage.GetAttribute(attribute))
        except AttributeError as e:
            logger.debug('_ForceUpdateOfAttribute generated the following error: %s' % str(e))
            return
            
    def FirstExerciseDate(self, value = 'Reading', *args):
        ''' Retrieves the first exercise date of an ASCOT. For backwards compability, 
            if no such date is found, look for a first exercise date in the mapped exercise event
            table. 
        '''
        if value == 'Reading':
            firstExerciseDate = self.Ascot().FirstNoticeDate()
            if not firstExerciseDate:
                firstExerciseDate = self.__FirstExerciseDateFromExerciseEvents()
            return firstExerciseDate
        elif value:
            self.Ascot().FirstNoticeDate(value)
                        
    def __FirstExerciseDateFromExerciseEvents(self):
        exerciseEvents = self.Ascot().ExerciseEvents()
        foundExerciseEvent = None
        if not exerciseEvents.IsEmpty():
            for exerciseEvent in exerciseEvents:
                if not exerciseEvent.Type() == 'UserDefined':
                    continue
                foundExerciseEvent = exerciseEvent
                break
        firstExerciseEventDate = foundExerciseEvent.StartDate() if foundExerciseEvent else None
        return firstExerciseEventDate

    def SetAttributeAndForceUpdate(self, dealPackage, attribute, value):
        # This exception handling is kept as a precaution
        try:
            dealPackage.SetAttribute(attribute, value)
        except Exception:
            pass
        self._ForceUpdateOfAttribute(dealPackage, attribute)

    def SetDefaultTradeAttributes(self):
    # pylint: disable-msg=E1101
        dealPackage = self.DealPackage()
        leadTrade = self.LeadTrade()
        leadB2B = self.LeadB2B()
        self.SetAttributeAndForceUpdate(dealPackage, 'currency', leadTrade.Instrument().Currency().Name())
        self.SetAttributeAndForceUpdate(dealPackage, 'nominal', leadTrade.Nominal())
        self.SetAttributeAndForceUpdate(dealPackage, 'price', leadTrade.Price())
        self.SetAttributeAndForceUpdate(dealPackage, 'trader', leadTrade.Trader())
        self.SetAttributeAndForceUpdate(dealPackage, 'acquirer', leadTrade.Acquirer())
        self.SetAttributeAndForceUpdate(dealPackage, 'counterparty', leadTrade.Counterparty())
        # Setting trade time updates value day
        valueDay = leadTrade.ValueDay()
        self.SetAttributeAndForceUpdate(dealPackage, 'tradeTime', leadTrade.TradeTime())
        self.SetAttributeAndForceUpdate(dealPackage, 'valueDay', valueDay)
        self.SetAttributeAndForceUpdate(dealPackage, 'status', leadTrade.Status())
        self.SetAttributeAndForceUpdate(dealPackage, 'portfolio', leadTrade.Portfolio())
        self.SetAttributeAndForceUpdate(dealPackage, 'salesCredit', leadTrade.SalesCredit())
        self.SetAttributeAndForceUpdate(dealPackage, 'salesPerson', leadTrade.SalesPerson())
        self.SetAttributeAndForceUpdate(dealPackage, 'b2bAcq', leadB2B.TraderAcquirer())
        self.SetAttributeAndForceUpdate(dealPackage, 'b2bEnabled', leadTrade.IsB2BSalesCover())
        self.SetAttributeAndForceUpdate(dealPackage, 'b2bPrf', leadB2B.TraderPortfolio())
        leadTrade.UpdatePremium(False)
        self.SetPremium()

    def SetDefaultAscotAttributes(self, longStub=False):
    # pylint: disable-msg=E1101
        dealPackage = self.DealPackage()
        ascot = self.Ascot()
        self.SetAttributeAndForceUpdate(dealPackage, 'ascotName', ascot.Name())
        self.SetAttributeAndForceUpdate(dealPackage, 'ascotContractSize', ascot.ContractSize())
        self.SetAttributeAndForceUpdate(dealPackage, 'exerciseType', ascot.ExerciseType())
        self.SetAttributeAndForceUpdate(dealPackage, 'settlementType', ascot.SettlementType())
        self.SetAttributeAndForceUpdate(dealPackage, 'payDayOffset', ascot.PayDayOffset())
        self.SetAttributeAndForceUpdate(dealPackage, 'dayCountMethod', 'Act/360')
        self.SetAttributeAndForceUpdate(dealPackage, 'firstExerciseDate', self.DefaultFirstExerciseDate())  
        self.SetAttributeAndForceUpdate(dealPackage, 'floatSpread', 0.0)
        self.SetIRSStartDate()

    def SetDefaultOptionAttributes(self):
    # pylint: disable-msg=E1101
        dealPackage = self.DealPackage()
        option = self.Option()
        self.SetAttributeAndForceUpdate(dealPackage, 'optionName', option.Name())
        self.SetAttributeAndForceUpdate(dealPackage, 'maturityDateTime', option.ExpiryDate())
        self.SetAttributeAndForceUpdate(dealPackage, 'exerciseType', option.ExerciseType())
        self.SetAttributeAndForceUpdate(dealPackage, 'optionType', option.OptionType())
        self.SetAttributeAndForceUpdate(dealPackage, 'strikePrice', option.StrikePrice())
        self.SetAttributeAndForceUpdate(dealPackage, 'payDayOffset', option.PayDayOffset())
        self.SetAttributeAndForceUpdate(dealPackage, 'settlementType', option.SettlementType())

    def SetDefaultIRSAttributes(self):
    # pylint: disable-msg=E1101
        dealPackage = self.DealPackage()
        irs = self.IRS()
        irsPayLeg = self.IRSPayLeg()
        floatRateRef = irsPayLeg.FloatRateReference()
        self.SetAttributeAndForceUpdate(dealPackage, 'irsName', irs.Name())
        self.SetAttributeAndForceUpdate(dealPackage, 'irsStartDate', irsPayLeg.StartDate())
        self.SetAttributeAndForceUpdate(dealPackage, 'maturityDateTime', irsPayLeg.EndDate())
        self.SetAttributeAndForceUpdate(dealPackage, 'irsPayCalendar', irsPayLeg.PayCalendar())
        self.SetAttributeAndForceUpdate(dealPackage, 'irsPay2Calendar', irsPayLeg.Pay2Calendar())
        self.SetAttributeAndForceUpdate(dealPackage, 'irsPay3Calendar', irsPayLeg.Pay3Calendar())
        self.SetAttributeAndForceUpdate(dealPackage, 'irsPay4Calendar', irsPayLeg.Pay4Calendar())
        self.SetAttributeAndForceUpdate(dealPackage, 'payDayMethod', irsPayLeg.PayDayMethod())
        self.SetAttributeAndForceUpdate(dealPackage, 'dayCountMethod', irsPayLeg.DayCountMethod())
        self.SetAttributeAndForceUpdate(dealPackage, 'fixedRate', irsPayLeg.FixedRate())
        self.SetAttributeAndForceUpdate(dealPackage, 'floatSpread', irsPayLeg.Spread())
        self.SetAttributeAndForceUpdate(dealPackage, 'legType', irsPayLeg.LegType())
        self.SetAttributeAndForceUpdate(dealPackage, 'longStub', irsPayLeg.LongStub())
        self.SetAttributeAndForceUpdate(dealPackage, 'fixedCoupon', irsPayLeg.FixedCoupon())
        self.SetAttributeAndForceUpdate(dealPackage, 'floatRateReference', floatRateRef)

    def SetDefaultOnSwapStockAttributes(self):
    # pylint: disable-msg=E1101
        dealPackage = self.DealPackage()
        stock = self.Stock()
        stockTrade = self.StockTrade()
        dealPackage.SetAttribute('stockName', stock.Name())
        self.SetAttributeAndForceUpdate(dealPackage, 'stockPrice', stockTrade.Price())
        self.SetAttributeAndForceUpdate(dealPackage, 'stockQuantity', stockTrade.Quantity())
        self.SetAttributeAndForceUpdate(dealPackage, 'stockValueDay', stockTrade.ValueDay())

    def SetDefaultCBAttributes(self):
    # pylint: disable-msg=E1101
        dealPackage = self.DealPackage()
        cb = self.CB()
        cbLeg = self.CBLeg()
        self.SetAttributeAndForceUpdate(dealPackage, 'isin', cb.Isin())
        self.SetAttributeAndForceUpdate(dealPackage, 'payCalendar', cbLeg.PayCalendar())
        self.SetAttributeAndForceUpdate(dealPackage, 'pay2Calendar', cbLeg.Pay2Calendar())


    # Package fields
    
    ipName =          Str(  label='Name',
                            objMapping='InstrumentPackage.Name',
                            toolTip='The name of the instrument package',
                            enabled=True )
                            
    suggestName =     Action(  label='Suggest',
                               action='@SuggestNameAction',
                               toolTip='Suggest a name for the instrument package',
                               width=2000,
                               maxWidth=2000 )

    # Trade fields

    currency =          Object( label='Currency',
                                objMapping='LeadTrade.Currency',
                                toolTip='Notional currency',
                                enabled=False )

    nominal =           Float(  label='Nominal',
                                objMapping='LeadTrade.Nominal',
                                onChanged = '@UpdateBuySellButton',
                                toolTip='Nominal amount',
                                formatter='PackageAbsNominal',
                                transform = '@TransformNominal',
                                backgroundColor='@NominalBackgroundColor')
                                
    buySell =           Str(  label = 'B/S',
                              onChanged = '@UpdateNominal',
                              choiceListSource = ['B', 'S', '-'],   
                              toolTip = 'Buy/Sell',
                            )                                     

    acquirer =          Object( label='Acquirer',
                                objMapping='Trades.Acquirer',
                                choiceListSource = AcquirerChoices() )

    counterparty =      Object( label='Counterparty',
                                objMapping='Trades.Counterparty',
                                choiceListSource= CounterpartyChoices() )

    payments =          PaymentsDialog( trade="GetTradeForPayments" )

    portfolio =         Object( label='Portfolio',
                                objMapping='Trades.Portfolio',
                                choiceListSource= PortfolioChoices() )

    price =             Float(  label='Price',
                                objMapping='LeadTrade.Price',
                                formatter='InstrumentDefinitionStrikePrice' )

    salesCredit =       Object( label='Sales Credit',
                                objMapping='LeadTrade.SalesCredit',
                                formatter='PercentShowZero')

    salesPerson =       Object( label='Sales Person',
                                objMapping='LeadTrade.SalesPerson' )

    status =            Object( label='Status',
                                objMapping='LeadTrade.Status',
                                choiceListSource= TradeStatusChoices() )

    trader =            Object( label='Trader',
                                objMapping='Trades.Trader' )

    tradeTime =         Object( label='Trade Time',
                                objMapping='LeadTrade.TradeTime',
                                transform='@TransformPeriodToDate' )

    valueDay =          Date(   label='Value Day',
                                objMapping='LeadTrade.ValueDay',
                                transform='@TransformPeriodToDate' )

    premium =           Float(  label='Premium',
                                objMapping='LeadTrade.Premium',
                                toolTip='Premium for lead trade',
                                formatter='InstrumentDefinitionNominal',
                                enabled=False)

    # --------------------------------------------------------------------------
    # GUI Callbacks
    # --------------------------------------------------------------------------
    def InstrumentChanged(self, attr, oldIns, newIns):
    # pylint: disable-msg=W0613
        if oldIns and newIns and oldIns != newIns:
            self.insNew = newIns
            self.SetNewInsIfNeeded()
            self.Refresh()

    def _ascotName_changed(self, attribute, oldValue, newValue, *args):
    # pylint: disable-msg=W0613
        pass

    def _cb_changed(self, attr, oldIns, newIns, *args):
        self.InstrumentChanged(attr, oldIns, newIns)

    def _ins_changed(self, attr, oldIns, newIns, *args):
        self.InstrumentChanged(attr, oldIns, newIns)

    def _ascot_changed(self, attr, oldIns, newIns, *args):
        self.InstrumentChanged(attr, oldIns, newIns)

    def _stock_changed(self, attr, oldIns, newIns, *args):
        self.InstrumentChanged(attr, oldIns, newIns)

    def _dayCountMethod_changed(self, attribute, oldValue, newValue, *args):
        # pylint: disable-msg=W0613
        if self.IRS():
            self.IRSPayLeg().DayCountMethod(newValue)
            self.IRSRecLeg().DayCountMethod(newValue)
            self.GenerateCashFlowsAndRelinkSwap()

    def _payDayOffset_changed(self, attribute, oldValue, newValue, *args):
    # pylint: disable-msg=W0613
        if self.IRS():
            self.SetIRSSpotBankingDaysOffset(newValue)
            self.GenerateCashFlowsAndRelinkSwap()
        self.SetLastExerciseDate()

    def _irsPayCalendar_changed(self, attribute, oldValue, newValue, *args):
    # pylint: disable-msg=W0613
        self.SetIRSStartDate()
        self.GenerateCashFlowsAndRelinkSwap(True)

    def _irsPay2Calendar_changed(self, attribute, oldValue, newValue, *args):
    # pylint: disable-msg=W0613
        self.SetIRSStartDate()
        self.GenerateCashFlowsAndRelinkSwap(True)

    def _irsPay3Calendar_changed(self, attribute, oldValue, newValue, *args):
    # pylint: disable-msg=W0613
        self.SetIRSStartDate()
        self.GenerateCashFlowsAndRelinkSwap(True)

    def _irsPay4Calendar_changed(self, attribute, oldValue, newValue, *args):
    # pylint: disable-msg=W0613
        self.SetIRSStartDate()
        self.GenerateCashFlowsAndRelinkSwap(True)

    def _maturityType_changed(self, attribute, oldValue, newValue, *args):
    # pylint: disable-msg=W0613
        ascotExpiryDate = self.Ascot().ExpiryDateOnly()
        newMaturityDate = None
        newMaturityType = str(newValue)
        if newMaturityType == utils.CB_MAT:
            newMaturityDate = self.CB().EndDate()
        elif newMaturityType == utils.CB_MAT_2BD:
            newMaturityDate = utils.GetCBMaturityDate2BD(self.CB())
        elif newMaturityType == utils.CB_PUT:
            newMaturityDate = utils.GetCBNextPutDate(self.CB())
        elif newMaturityType == utils.CB_PUT_2BD:
            newMaturityDate = utils.GetCBNextPutDate2BD(self.CB())
        else:
            newMaturityDate = ascotExpiryDate
        if newMaturityDate != ascotExpiryDate:
            self.maturityDateTime = newMaturityDate
        self.RemoveSimulation('maturityType')


    def _insType_changed(self, attribute, oldValue, newValue, *args):
    # pylint: disable-msg=W0613
        return
        
    def DefaultFirstExerciseDate(self):
        return self.AscotTrade().ValueDay()

    def SetIRSStartDate(self, *args):
        if self.IRS() and (self.firstExerciseDate is not None):
            calendarsAdjustBankingDays = acm.GetFunction('calendarsAdjustBankingDays', 3)
            payCalenders = self.IRSPayLegCalendars()
            startDate = self.firstExerciseDate if payCalenders.IsEmpty() else calendarsAdjustBankingDays(payCalenders, self.firstExerciseDate, 1)
            self.irsStartDate = startDate
            self.GenerateCashFlowsAndRelinkSwap()

    def _irsStartDate_changed(self, attribute, oldValue, newValue, *args):
    # pylint: disable-msg=W0613
        if self.IRS():
            self.GenerateCashFlowsAndRelinkSwap()

    def _irsEndDate_changed(self, attribute, oldValue, newValue, *args):
        # pylint: disable-msg=W0613
        if self.IRS():
            self.SetRollingPeriodBase(newValue)
            self.GenerateCashFlowsAndRelinkSwap()

    def _LastExerciseDate(self):
        # pylint: disable-msg=E1101
        cbLeg = self.CBLeg()
        calendar = cbLeg.PayCalendar()
        ascot = self.Ascot()
        lastExerciseDateOffset = -ascot.PayDayOffset()
        lastExerciseDate = utils.AdjustBankingDays(calendar, self.IRSPayLeg().EndDate(), lastExerciseDateOffset)
        return lastExerciseDate

    def SetRollingPeriodBase(self, rollingPeriodBase):
        self.IRSPayLeg().RollingPeriodBase = rollingPeriodBase
        self.IRSRecLeg().RollingPeriodBase = rollingPeriodBase

    def SetIRSSpotBankingDaysOffset(self, spotBankingDays):
        self.IRS().SpotBankingDaysOffset(spotBankingDays)

    def SetLastExerciseDate(self):
        #pylint: disable-msg=E1101
        lastExerciseDate = self._LastExerciseDate()
        self.SetAttributeAndForceUpdate(self.DealPackage(), 'lastExerciseDate', lastExerciseDate)

    def _maturityDateTime_changed(self, attribute, oldValue, newValue, *args):
        # pylint: disable-msg=W0613
        if self.Ascot():
            if self.IRS():
                self.SetRollingPeriodBase(newValue)
                self.GenerateCashFlowsAndRelinkSwap()
            self.SetLastExerciseDate()


    def _longStub_changed(self, attribute, oldValue, newValue, *args):
        # pylint: disable-msg=W0613
        self.GenerateCashFlowsAndRelinkSwap(True)

    def _payDayMethod_changed(self, attribute, oldValue, newValue, *args):
        self.GenerateCashFlowsAndRelinkSwap(True)

    def _fixedCoupon_changed(self, attribute, oldValue, newValue, *args):
        self.GenerateCashFlowsAndRelinkSwap(True)

    def _legType_changed(self, attribute, oldValue, newValue, *args):
        # pylint: disable-msg=W0613
        self.GenerateCashFlowsAndRelinkSwap(True)

    def _couponFrequency_changed(self, attribute, oldValue, newValue, *args):
        self.GenerateCashFlowsAndRelinkSwap(True)

    def _fixedRate_changed(self, attribute, oldValue, newValue, *args):
        # pylint: disable-msg=W0613
        self.GenerateCashFlowsAndRelinkSwap(True)

    def _floatSpread_changed(self, attribute, oldValue, newValue, *args):
        # pylint: disable-msg=W0613
        self.GenerateCashFlowsAndRelinkSwap(True)

    def _floatRateReference_changed(self, attribute, oldValue, newValue, *args):
        # pylint: disable-msg=W0613
        period = utils.GetRollingPeriodFromFloatRateReference(newValue)
        if self.IRS():
            self.couponFrequency = period
            self.SetResetCalendar(newValue)
            self.GenerateCashFlowsAndRelinkSwap(True)

    def SetResetCalendar(self, floatRateRef):
        reset_cal = floatRateRef.Legs()[0].ResetCalendar()
        if self.IRS():
            self.IRSPayLeg().ResetCalendar(reset_cal)

    def _price_changed(self, attribute, oldValue, newValue, *args):
        # pylint: disable-msg=W0613
        self.SetPremium()

    def _nominal_changed(self, attribute, oldValue, newValue, *args):
        # pylint: disable-msg=W0613
        if self.Stock():
            with MuteNotificationsWithSafeExit(self):
                self.SetStockQuantity()
        if self.IRS():
            self.GenerateCashFlowsAndRelinkSwap()
        self.SetPremium()

    def _optionType_changed(self, attribute, oldValue, newValue, *args):
        self._nominal_changed(attribute, oldValue, newValue)

    def _tradeTime_changed(self, attribute, oldValue, newValue, *args):
    # pylint: disable-msg=E1101, W0613
        self.valueDay = self.LeadTrade().ValueDay()
        self.SetTradeTimeOnNonLeadTrades()

    def _onSwapDelta_changed(self, attribute, oldValue, newValue, *args):
        with MuteNotificationsWithSafeExit(self):
            self.SetStockQuantity()

    def _stockQuantity_changed(self, attribute, oldValue, newValue, *args):
        with MuteNotificationsWithSafeExit(self):
            self.SetOnSwapDelta()

    def _portfolio_changed(self, attribute, oldValue, newValue, *args):
        try:
            hooks.PortfolioChanged(self)
        except StandardError as err:
            logger.error('Failed to invoke "ConvertiblePackageHooks.PortfolioChanged" hook: %s', err)

    def _status_changed(self, attribute, oldValue, newValue, *args):
        self.SetTradeStatusOnNonLeadTrades()
        
    def _ButtonSignKey(self, value):
        if value > 0:
            key = 1
        elif value < 0:
            key = -1
        else:
            key = 0
        return key               

    def SetBuySellButtonAtOnOpen(self):
        key = self._ButtonSignKey(self.GetAttribute('nominal'))
        buttonSign = utils.BUY_SELL_MAP[key]
        self.SetAttribute('buySell', buttonSign)        
        
    def UpdateNominal(self, attrName, oldValue, newValue, *args):
        sign = utils.BUY_SELL_MAP[newValue]
        self.SetAttribute('nominal', abs(self.GetAttribute('nominal'))*sign)    

    def UpdateBuySellButton(self, attrName, oldValue, newValue, *args):
        key = self._ButtonSignKey(newValue)
        buttonSign = utils.BUY_SELL_MAP[key]
        self.SetAttribute('buySell', buttonSign)
        
    def SetCBB2BPrice(self, *args):
        self._SetB2BPrice(self.CBB2B(), self.price)

    def SetInsB2BPrice(self, *args):
        self._SetB2BPrice(self.InsB2B(), self.price)

    def SetStockB2BPrice(self, *args):
        self._SetB2BPrice(self.StockB2B(), self.stockPrice)

    def SetOptionB2BPrice(self, *args):
        self._SetB2BPrice(self.OptionB2B(), self.price)

    def SetAscotB2BPrice(self, *args):
        self._SetB2BPrice(self.AscotB2B(), self.price)

    def SetNonLeadAscotB2BPrice(self, *args):
        self._SetB2BPrice(self.AscotB2B(), self.ascotPrice)

    def _SetB2BPrice(self, b2bParams, price, salesMargin = 0.0):
        b2bParams.TraderPrice = price
        b2bParams.SalesMargin = salesMargin

    def SetStockQuantity(self):
    # pylint: disable-msg=E1101
        ratio = self.CB().ConversionRatio()
        quantity = self.LeadTrade().Quantity()
        newDelta = self.DealPackage().GetAttribute('onSwapDelta')
        if not newDelta:
            newDelta = 1.0
        newStockQuantity = utils.GetTradeableAmount(-ratio*quantity*newDelta, self.Stock())
        self.stockQuantity = newStockQuantity

    def SetOnSwapDelta(self):
    # pylint: disable-msg=E1101
        ratio = self.CB().ConversionRatio()
        quantity = self.LeadTrade().Quantity()
        stockQuantity = self.stockQuantity
        if ratio*quantity != 0.0:
            newDelta = max(-stockQuantity/(ratio*quantity), 0.0)
            self.onSwapDelta = newDelta

    def SetInsType(self):
    # pylint: disable-msg=E1101
        insType = self.Instrument().InsType()
        insTypeInGUI = utils.InsTypeToGUI(insType)
        self.DealPackage().SetAttribute('insType', insTypeInGUI)

    def SetPremium(self):
    # pylint: disable-msg=E1101
        self.premium = self.LeadTrade().Premium()

    def SetTradeStatusOnNonLeadTrades(self):
    # pylint: disable-msg=E1101
        for trade in self.DealPackage().Trades():
            if trade == self.LeadTrade():
                continue
            trade.Status(self.LeadTrade().Status())

    def SetTradeTimeOnNonLeadTrades(self):
    # pylint: disable-msg=E1101
        for trade in self.DealPackage().Trades():
            if trade == self.LeadTrade():
                continue
            trade.TradeTime(self.LeadTrade().TradeTime())

    # --------------------------------------------------------------------------
    # Utility functions
    # --------------------------------------------------------------------------

    def GenerateCashFlowsAndRelinkSwap(self, onlyPayLeg = False):
        SetRecallSwap(self.Ascot(), self.IRS())
        self.GenerateCashFlows(onlyPayLeg)

    def GenerateCashFlows(self, onlyPayLeg = False):
        try:
            swapConvertibleCreator = SwapFromConvertibleCreator(self.CB())
            swapConvertibleCreator.GenerateCashFlowsForPayLeg(self.IRSPayLeg())
            if onlyPayLeg:
                return
            if self.IRSRecLeg().RollingPeriod() == '0d':
                swapConvertibleCreator.UpdateSwapFromCB(self.IRS())
            else:
                swapConvertibleCreator.GenerateCashFlowsForReceiveLeg(self.IRSRecLeg())
        except Exception as e:
            logger.error('Failed to generate cash flows: %s'%e)

    def _ClearList(self, acmList):
        acmList.Clear()

    def UpdateRateIndexChoices(self):
        self._ClearList(self.rateIndexChoices)
        self.rateIndexChoices.AddAll(acm.FRateIndex.Select(''))

    def UpdateInstrumentList(self):
        self._ClearList(self.instrumentList)
        self.instrumentList.AddAll(self.AllCBChoices())
        self.instrumentList.AddAll(self.AllAscotChoices())

    def IRSPayLegCalendars(self):
        calendars = acm.FSet()
        leg = self.IRS().PayLeg()
        if leg.PayCalendar():
            calendars.Add(leg.PayCalendar())
        if leg.Pay2Calendar():
            calendars.Add(leg.Pay2Calendar())
        if leg.Pay3Calendar():
            calendars.Add(leg.Pay3Calendar())
        if leg.Pay4Calendar():
            calendars.Add(leg.Pay4Calendar())
        return calendars

    def RateIndexChoices(self, *args):
        self.UpdateRateIndexChoices()
        return self.rateIndexChoices

    def InstrumentList(self, *args):
        self.UpdateInstrumentList()
        return self.instrumentList

    def AllCBChoices(self, *args):
        return utils.AllCBChoices()

    def AllAscotChoices(self, *args):
        today = acm.Time.DateToday()
        constraint = 'underlyingType="Convertible" and expiryDate>"' + today + '"'
        logger.debug('AllAscotChoices constraint %s' %(constraint))
        return acm.FOption.Select(constraint).SortByProperty('Name')

    def AllStockChoices(self, *args):
        return acm.FStock.Select('').SortByProperty('Name')

    def ValidLegTypes(self, *args):
        legTypes = ['Fixed', 'Float']
        return legTypes

    def ValidOptionTypes(self, *args):
        optionTypes = ['Call', 'Put']
        return optionTypes

    def ValidDayCountMethods(self, *args):
        values = ['Act/360', 'Act/365', 'Act/ActISDA', '30/360', '30E/360']
        return values

    def ValidMaturityTypes(self, *args):
        types = [utils.CB_MAT, utils.CB_PUT]
        return types

    def ValidInstrumentTypes(self, *args):
        insTypes = [utils.INSTYPE_ASCOT, utils.INSTYPE_CB]
        return insTypes

    def RemoveSimulation(self, traitName):
        if self.IsCalculationSimulated(traitName):
            self.SimulateCalculation(traitName, "")

    def SuggestNameAction(self, *args, **kwargs):
        self.DealPackage().SuggestName()

    #---------------PAYMENTS-------------------------------#
    def GetTradeForPayments(self):
        # pylint: disable-msg=E1128
        try:
            trade = hooks.TradeForPayments(self.DealPackage())
            if trade and trade.IsKindOf(acm.FTrade):
                return trade
            logger.debug('The TradeForPayments hook defined in ConvertiblePackageHooks did not return a trade object. Check implementation.')
        except ImportError as err:
            logger.error('The module ConvertiblePackageHooks could not be imported: %s', err)
        except AttributeError as err:
            logger.debug('No TradeForPayments hook in ConvertiblePackageHooks has been defined')
        except Exception as err:
            logger.error('Failed to invoke "ConvertiblePackageHooks.TradeForPayments" hook. Reason: %s', err)
        logger.debug('Trade payments dialog will run in default mode and use the lead trade')
        return self.LeadTrade()

    def TransformPeriodToDate(self, name, date, *args):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date
                
    def TransformNominal(self, name, nominal):
        if not isinstance(nominal, basestring):
            return nominal
        parsedInput = self.DealPackage().GetAttributeMetaData(name, 'formatter')().Parse(nominal)
        if parsedInput is None:
            return nominal
        if nominal.startswith( ('+', '-') ):
            sign = {'+' : 1, '-' : -1}[nominal[0]]
        else:
            sign = utils.BUY_SELL_MAP[self.buySell] if utils.BUY_SELL_MAP[self.buySell] else 1
        return sign * abs(parsedInput)                 

    def NominalBackgroundColor(self, *args):
        return 'BkgTickerOwnBuyTrade' if self.nominal >= 0 else 'BkgTickerOwnSellTrade'

    def StockQuantityBackGroundColor(self, *args):
        return 'BkgTickerOwnBuyTrade' if self.stockQuantity >= 0 else 'BkgTickerOwnSellTrade'
