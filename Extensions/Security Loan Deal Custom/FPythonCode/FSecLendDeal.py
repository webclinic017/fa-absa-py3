""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecurityLoanDealCustom/etc/FSecLendDeal.py"
from __future__ import print_function
import acm
import SecurityLoan_DP
import FSecLendDealUtils
import FSecLendUtils
from contextlib import contextmanager
from DealDevKit import Bool, Object, Str, Float, Int, CalcVal, Date, ReturnDomainDecorator, DealPackageChoiceListSource, Text, TradeActions, Action, NoOverride, ParseSuffixedFloat, Settings, DealDefinition, SalesTradingInteraction
from DealPackageDevKit import CompositeAttributeDefinition, AttributeDialog
from FSecLendDealTradeActionCommands import IncreaseCommand, LinkTradeCommand, ReturnCommand, RerateCommand, ExtendCommand, RecallCommand
from CompositeAttributesLib import TradeDefinition, BuySell
from FParameterSettings import ParameterSettingsCreator
import FPortfolioRouter

_SETTINGS = ParameterSettingsCreator.FromRootParameter('SecLendSettings')

#For setting presets in trade entry
try:
    from FSecLendHooks import (PresetOnUnderlyingChanged, PresetOnCounterpartyChanged,
                               PresetOnAccountChanged,  GetAccountChoices,
                               FromShortNameToId, FromIdToShortName,
                               DefaultDealEntryColumns, GetCollateralAgreementChoices,
                               SuggestRateColumn, GetOrderSources, DefaultPortfolio,
                               DefaultAcquirer)
    useCustomHooks = True
except ImportError as e:
    useCustomHooks = False
    print (e)
except SyntaxError as e:
    useCustomHooks = False
    print (e)

def _AddMissingResets(leg):
    for c in leg.CashFlows():
        for r in c.Resets():
            leg.Resets().Add(r)


class SecurityLoanLeg(SecurityLoan_DP.SecurityLoanLeg):

    def OnInit(self, leg, trade, **kwargs):
        super(SecurityLoanLeg, self).OnInit(leg, trade, **kwargs)
        self._currentFee = 0.0
        self._initialIndexEstimate = None

    def Attributes(self):
        attributes = super(SecurityLoanLeg, self).Attributes()

        attributes['startDate']         = Object(   label='Start',
                                                    toolTip = 'Start date of the loan.',
                                                    objMapping=self._leg + '.StartDate',
                                                    transform='@StartDateTransform',
                                                    onChanged='@OnStartDateChanged')

        attributes['startPeriod']       = Object(  label='',
                                                    toolTip = 'Start period of the loan.',
                                                    width=11,
                                                    objMapping=self.UniqueCallback('StartPeriod'),
                                                    enabled=False)

        attributes['endDate']           = Object(   label='End',
                                                    toolTip = 'End date of the loan. If the loan is open ended, the first possible start date is shown.',
                                                    objMapping=self._leg + '.EndDate',
                                                    enabled = self.UniqueCallback('@EndDateEnabled'),
                                                    transform='@EndDateTransform')

        attributes['endPeriod']         = Object(   label='',
                                                    toolTip = 'End period of the loan.',
                                                    width=11,
                                                    objMapping=self._leg + '.EndPeriod',
                                                    enabled=False)

        attributes['currentFee']        = Float(    label='Fee(bp)',
                                                    width = 10,
                                                    toolTip = self.UniqueCallback('@AllFeesStringForTooltip'),
                                                    formatter='SolitaryPricePercentToBasisPointOneDecimal',
                                                    solverParameter={'minValue':-1.0, 'maxValue':100.0},
                                                    transform=self.UniqueCallback('@TransformSolverFeeFromReset'),
                                                    backgroundColor='@SolverColor',
                                                    objMapping=self.UniqueCallback('CurrentFee'))

        attributes['priceFixingStatus'] = Str(      label='',
                                                    width = 10,
                                                    toolTip = 'Indicated if the price is fixed or not',
                                                    choiceListSource = ['Market', 'Starting', 'Fixed'],
                                                    objMapping=self.UniqueCallback('PriceFixingStatus'))

        attributes['priceFixingValue'] = Object(    label=self.UniqueCallback('@PriceFixingValueLabel'),
                                                    objMapping=self.UniqueCallback('WeightedPriceFixingValue'),
                                                    formatter='DetailedShowZero',
                                                    visible=self.UniqueCallback('@IndexRefVisible'))

        attributes['priceFixingValueDomestic']  = Object( label=self.UniqueCallback('@PriceFixingValueDomesticLabel'),
                                                    objMapping=self.UniqueCallback('WeightedPriceFixingValueDomestic'),
                                                    formatter='DetailedShowZero',
                                                    visible=self.UniqueCallback('@InitialFXVisible'))

        return attributes


    #visualization callbacks
    def InitialFXVisible(self, *args):
        leg = self.Leg()
        return leg.IndexRef() and leg.IndexRef().Currency() != leg.Currency()

    def PriceFixingValueDomesticLabel(self, *args):
        return self.Leg().Instrument().Currency().StringKey() + ' Price'

    def PriceFixingValueLabel(self, *args):
        label = 'Price'
        if self.indexRef and self.indexRef.Currency() != self.Leg().Instrument().Currency():
            label = self.indexRef.Currency().StringKey() + ' Price'
        return label

    def AllFeesStringForTooltip(self, *args):
        def formatStr(val):
            f = self.GetAttributeMetaData('currentFee', 'formatter')()
            return str(f.Format(val))
        maxAmount = 10
        i = 0
        toolTip = ''
        day = acm.Time().DateToday()
        prevReset = None
        for cf in self.Leg().CashFlows().SortByProperty('StartDate', False):
            for r in cf.Resets().SortByProperty('Day', False):
                if i > maxAmount:
                    return toolTip
                if r.ResetType() == "Spread" and r.IsFixed():
                    if not prevReset:
                        prevReset = r
                        toolTip += 'Date' + ' '*16 + ('Fee\n' if self.Leg().IsFixedLeg() else 'Spread\n')
                    if r.FixFixingValue() != prevReset.FixFixingValue():
                        toolTip += str(prevReset.Day()) + ':    ' + formatStr(prevReset.FixFixingValue()) + '\n'
                        i += 1
                    prevReset = r
        if i < 10 and prevReset:
            toolTip += str(prevReset.Day()) + ':    ' + formatStr(prevReset.FixFixingValue()) + '\n'
        return toolTip


    def EndDateEnabled(self, *args):
        return self.Leg().Instrument().OpenEnd() != 'Open End'

    def PriceFixingStatusIsMarket(self, *args):
        return self.priceFixingStatus == 'Market'

    #object mappings
    @ReturnDomainDecorator('string')
    def StartPeriod(self, value = 'NoValue', *args):
        if value == 'NoValue':
            today=acm.Time().DateToday()
            startDate=self.startDate
            if startDate >= today:
                wrapper = FSecLendDealUtils.FeeWrapper(self.Leg())
                calendarInfo=wrapper.CalendarInformation()
                return str(calendarInfo.BankingDaysBetween(today, startDate))+'bd'
            else:
                return self.Leg().StartPeriod()

    @ReturnDomainDecorator('double')
    def CurrentFee(self, value = 'NoValue', *args):
        wrapper = FSecLendDealUtils.FeeWrapper(self.Leg())
        reset = wrapper.FirstOrLastFixedStoredSpreadReset()
        if value == 'NoValue':
            if reset:
                if reset.IsFixed():
                    fee = reset.FixFixingValue()
                    self._currentFee = fee
                else:
                    fee = 0
                return fee
            else:
                return 0.0
        elif reset:
            reset.FixFixingValue(value)
         
    def CalculateInitialFxFromFixing(self, fixing):
        try:
            calcSpaceCollection = acm.Calculations().CreateCalculationSpaceCollection()
            calcSpace = calcSpaceCollection.GetSpace('FMoneyFlowSheet', acm.GetDefaultContext())
            calculation = calcSpace.CreateCalculation(fixing, 'Cash Analysis Fixing Estimate', None)
            return calculation.Value().Number()
        except:
            pass
            
    def CalculateInitialFxFixing(self):
        initialFX = 0.0
        first = self.InitialFXFixing()
        if first:
            first = self.InitialFXFixing()
            if first and first.IsFixed():
                first.FixFixingValue(None)
            initialFX = self.CalculateInitialFxFromFixing(first)
        else:
            initialFX = self.CalculateInitialFxEstimate()
        
        return 0.0 if initialFX is None else initialFX

    @ReturnDomainDecorator('string')
    def PriceFixingStatus(self, value = 'NoValue'):
        if value == 'NoValue':
            if self.nominalScaling == 'Initial Price':
                return 'Fixed'
            else:
                if self.initialIndexValue != 0 and self.nominalScaling == 'Price':
                    return 'Starting'
                else:
                    return 'Market'
        else:
            fixingDateRule = self.Leg().IndexRefFixingDateRule()
            previousPriceFixingValue = self.ApplyDomesticRounding(self.priceFixingValue, value)
            if value == 'Fixed':
                self.RegenerateCashFlowsOnNominalScalingChange('Initial Price')
                self.nominalScaling = 'Initial Price'
                self.priceFixingValue = previousPriceFixingValue
            else:
                self.RegenerateCashFlowsOnNominalScalingChange('Price')
                if self.nominalScaling != 'Price':
                    self.nominalScaling = 'Price'

                if value == 'Starting':
                    self.SuggestInitialIndexValues()
                    self.priceFixingValue = previousPriceFixingValue
                else:
                    self.SuggestInitialIndexValues( 0 )
                self.initialFX = self.CalculateInitialFxFixing()
            self.Leg().IndexRefFixingDateRule( fixingDateRule )

    def RegenerateCashFlowsOnNominalScalingChange(self, newScaling):
        regenerate = self.Instrument().Originator().StorageId() < 0 or (self.Owner().GetAttribute('ins_cfgRegenerate') and self.Owner().GetAttribute('ins_cfgRegenerateAll'))          
        if regenerate and self.Leg().IndexRef() and self.Leg().NominalScaling() != newScaling:
            self.Leg().Leg().NominalScaling = newScaling
            if 'Price' == newScaling and self.Leg().IndexRef().Currency() != self.Instrument().Currency():
                self.Leg().IndexRefFXFixingType = 'Explicit'
            self.Leg().GenerateCashFlows(0.0)
            _AddMissingResets(self.Leg())

    def ApplyDomesticRounding(self, priceFixingValue, priceFixingStatus):
        initialFx = self.initialFX
        if self.InitialFXVisible() and initialFx and acm.Math.IsFinite(initialFx):
            nominalFactor = self.Leg().NominalFactor()
            if 'Market' != priceFixingStatus:
                domesticValue = priceFixingValue * nominalFactor * initialFx
                domesticValue = acm.Math().RoundTo(domesticValue, 2)
                priceFixingValue = domesticValue / (initialFx * nominalFactor)
        return priceFixingValue

    @ReturnDomainDecorator('double')
    def WeightedPriceFixingValue(self, value = 'NoValue'):
        if value == 'NoValue':
            indexVal = self.IntitialIndexEstimate() if self.PriceFixingStatusIsMarket() else self.initialIndexValue
            if self.indexRefFXFixingType == 'Explicit':
                return indexVal * self.Leg().NominalFactor()
            else:
                if self.indexRef and self.indexRef.Currency() != self.Leg().Instrument().Currency():
                    initalFx = self.initialFX
                    if initalFx:
                        return indexVal * self.Leg().NominalFactor() / self.initialFX
                else:
                    return indexVal * self.Leg().NominalFactor()
        else:
            if self.indexRefFXFixingType == 'Explicit':
                self.SetInitialIndexValue(value / self.Leg().NominalFactor())
            else:
                if self.indexRef and self.indexRef.Currency() != self.Leg().Instrument().Currency():
                    initalFx = self.initialFX
                    if initalFx:
                        self.SetInitialIndexValue(value * self.initialFX / self.Leg().NominalFactor())
                else:
                    self.SetInitialIndexValue(value / self.Leg().NominalFactor())
            if self.Owner().Wrapper().IsPaymentDvPSettled() and self.Owner().IsRebate():
                self.Owner().Wrapper().DvPPaymentCashAmount(self.Owner().initialCashAmount_value)

    @ReturnDomainDecorator('double')
    def WeightedPriceFixingValueDomestic(self, value = 'NoValue', **kwargs):
        initialFx = self.initialFX
        if initialFx and acm.Math.IsFinite(initialFx):
            if value == 'NoValue':
                indexVal = self.IntitialIndexEstimate() if self.PriceFixingStatusIsMarket() else self.initialIndexValue
                if self.indexRefFXFixingType == 'Explicit':
                    return indexVal * self.Leg().NominalFactor() * initialFx
                else:
                    return indexVal * self.Leg().NominalFactor()
            else:
                if self.indexRefFXFixingType == 'Explicit':
                    self.SetInitialIndexValue(value / (initialFx * self.Leg().NominalFactor()))
                else:
                   self.SetInitialIndexValue(value / self.Leg().NominalFactor())
                if self.Owner().Wrapper().IsPaymentDvPSettled() and self.Owner().IsRebate():
                    self.Owner().Wrapper().DvPPaymentCashAmount(self.Owner().initialCashAmount_value)   
                

    #transforms
    def TransformSolverFeeFromReset(self, attrName, value):
        goalValue = None
        topValue = None
        if isinstance(value, str):
            value = value.lower()
        if value in ['p', 'pa', 'par']:
            goalValue = 100.0 if self.Instrument().IsOnBalanceSheet() else 0.0
        if goalValue != None:
            topValue = self.PrefixedName('theorPrice')
        if (goalValue == None or topValue == None):
            f = self.GetAttributeMetaData('tradePv', 'formatter')()
            goalValue = ParseSuffixedFloat(value, suffix=['pv'], formatter=f)
            if goalValue != None:
                topValue = self.PrefixedName('tradePv')
        if goalValue != None and topValue != None:
            if self.Leg().DecoratedObject().Originator().IsInfant():
                return self.GetMethod("Solve")(topValue, "payLeg_fixedRate", goalValue)
            else:
                raise ValueError("Only possible solve for infant instrument")
        else:
            return value


    #On Changed callbacks
    def AttributeChanged(self, attributeName, oldValue, newValue, userInputAttributeName):
        super(SecurityLoanLeg, self).AttributeChanged(attributeName, oldValue, newValue, userInputAttributeName)
        wrapper = FSecLendDealUtils.FeeWrapper(self.Leg())
        reset = wrapper.FirstOrLastFixedStoredSpreadReset()
        if reset and (self._currentFee is not None) and (not reset.IsFixed()):
            reset.FixFixingValue(self._currentFee)            
        _AddMissingResets(self.Leg())
        self._initialIndexEstimate = None

    #Utils
    def SetInitialIndexValue(self, value):
        value = self.RoundedInitialIndexValue(value)
        self.SetAttribute('initialIndexValue', value)

    def RoundedInitialIndexValue(self, value):
        if self.Owner().IsRebate():
           value = acm.Math().RoundTo(value, 2)
        return value

    def IntitialIndexEstimate(self):
        if self._initialIndexEstimate is None:
            self._initialIndexEstimate = self.Owner().Wrapper().LegInitialNominalScalingEstimate(self.Leg())
        return self._initialIndexEstimate

    def UpdateIntialIndex(self, attributeName=None, oldValue=None, newValue=None, userInputAttributeName=None):
        self._initialIndexEstimate = None
        if self.priceFixingStatus != "Market":
            self.SuggestInitialIndexValues()

        self.initialFX = self.CalculateInitialFxFixing()


    def SuggestInitialIndexValues(self, value = None):
        self.Owner().SuggestInitialIndexValues(value)

    
class SecurityLoanTradeLeg(SecurityLoanLeg):


    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {
             'legType': dict(visible = '@IsShowModeInstrumentDetailNoOverride',
                                                        enabled ='@IsNotRebate'),
             'nominalScalingPeriod': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'nominalScaling': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'indexRefFXFixingType': dict(visible='@IsShowModeInstrumentDetailNoOverride'),
             'indexRefFixingDateRule': dict(visible='@IsShowModeInstrumentDetailNoOverride'),
             'indexRef': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'payCalendar': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'pay2Calendar': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'pay3Calendar': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'pay4Calendar': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'pay5Calendar': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'initialFX': dict(label ='', enabled = False),
             'currentFee': dict(enabled = '@IsNotRebate'),
             'priceFixingStatus': dict(enabled = '@IsNotRebate'),
             'priceFixingValue': dict(enabled = '@IsNotRebate'),
             'priceFixingValueDomestic': dict(enabled = '@IsNotRebate'),      
             'rollingPeriod': dict(visible='@IsShowModeInstrumentDetailNoOverride'),
             'rollingPeriodBase': dict(visible='@IsShowModeInstrumentDetailNoOverride'),
             'nominal_value': dict(label = '@NominalWithLegCurrency',
                                                        toolTip = "Value of the trade leg (Quantity multiplied with the Price).",
                                                        enabled = '@IsNotRebate',
                                                        onChanged='@OnNominalValueChanged'),
            }
            )

    def LastResetDay(self):
        resets = self.Leg().Resets().SortByProperty('Day', False)
        return resets[0].Day() if len(resets) else  self.Leg().StartDate()

    @ReturnDomainDecorator('double')
    def Nominal(self, value = 'NoValue', **kwargs):
        return self.Owner().Wrapper().Nominal(value);


class SecurityLoanCashLeg(SecurityLoanLeg):


    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {
             'legType': dict(choiceListSource = ["Fixed", "Float"]),
             'nominalScaling': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'indexRefFXFixingType': dict(visible='@IsShowModeInstrumentDetailNoOverride'),
             'indexRefFixingDateRule': dict(visible='@IsShowModeInstrumentDetailNoOverride'),
             'indexRef': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'floatRateReference': dict(),
             'nominalScalingPeriod': dict(label="Reset Period",
                                                     visible = '@IsShowModeInstrumentDetailNoOverride'),
             'initialFX': dict(label ='', enabled = False, visible = '@IsRebateNoOverride'),
             'initialMargin': dict(formatter = 'ImprecisePercentShowZero',
                                                     onChanged='@InitialMarginChanged'),
             'rollingPeriod': dict(visible='@IsShowModeInstrumentDetailNoOverride'),
             'rollingPeriodBase': dict(visible='@IsShowModeInstrumentDetailNoOverride'),
             'payCalendar': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'pay2Calendar': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'pay3Calendar': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'pay4Calendar': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'pay5Calendar': dict(visible = '@IsShowModeInstrumentDetailNoOverride'),
             'nominal_value': dict(label = '@NominalWithLegCurrency'),
             'startDate': dict(visible='@ReceiveLegVisible',
                                                     enabled=False),
             'startPeriod': dict(visible='@ReceiveLegVisible'),
             'currentFee': dict(visible='@ReceiveLegVisible',
                                                     label='@CurrentFeeLabel'),
             'endDate': dict(visible='@ReceiveLegVisibleAndNotOpenEnd',
                                                     enabled=False),
             'endPeriod': dict(visible='@ReceiveLegVisibleAndNotOpenEnd'),
             'priceFixingStatus': dict(visible='@IsRebate',
                                                     enabled = '@IsNotRebate'),
             'priceFixingValue': dict(visible='@IsRebateNoOverride',
                                                     label = self.UniqueCallback('@RebatePriceLabel'),
                                                     toolTip = "The rebate price for cash collateral (Initial Margin multiplied with the Price)."),
             'priceFixingValueDomestic': dict(toolTip = "The rebate price in the currency of the security loan.",
                                                      visible='@IsRebateNoOverride',
                                                      label = self.UniqueCallback('@RebatePriceLabelDomesticLabel')),
                }
            )
    #Visualization callbacks
    def RebatePriceLabelDomesticLabel(self, *args):
        return self.Leg().Instrument().Currency().StringKey() + ' Rebate Price'

    def RebatePriceLabel(self, *args):
        label = 'Rebate Price'
        if self.indexRef and self.indexRef.Currency() != self.Leg().Instrument().Currency():
            label = self.indexRef.Currency().StringKey() + ' Rebate Price'
        return label

    #Utils
    def SetInitialIndexValue(self, value):
        if self.Owner().IsNotRebate() and not self.Owner().isDvP:
            value = 0
        value = self.RoundedInitialIndexValue(value)
        self.SetAttribute('initialIndexValue', value)
        
    def AttributeChanged(self, attributeName, oldValue, newValue, userInputAttributeName):
        if -1 != attributeName.find('_') and -1 == attributeName.find('triggerCashFlowUpdate') and not userInputAttributeName:
            if self.Owner().ins_cfgRegenerate:
                futureOnly = self.Owner().ins_cfgRegenerateFuture and not self.Owner().ins_cfgRegenerateAll
                self.Leg().GenerateCashFlows(0.0, futureOnly)
            
        super(SecurityLoanCashLeg, self).AttributeChanged(attributeName, oldValue, newValue, userInputAttributeName)

    # Not used for cash leg
    @ReturnDomainDecorator('double')
    def Nominal(self, value = 'NoValue', **kwargs):
        return 0.0

    def SuggestInitialIndexValues(self, value = None):
        if self.Owner().Wrapper().handler.UpdateCashLegOnly():
            self.Owner().SuggestInitialIndexValuesForLeg(self, value)
        else:
            self.Owner().SuggestInitialIndexValues(value)

class SecurityLoanTrade(TradeDefinition):
        
    def Attributes(self):
        attributes = super(SecurityLoanTrade, self).Attributes()
        attributes.pop('nominal')
        attributes.pop('openNominal')
        return attributes

''' #################################################################### '''

def DefaultColumns():
    if useCustomHooks:
        return DefaultDealEntryColumns()
    else:
        return ['Price Theor']

class SecurityLoanSTI(SalesTradingInteraction):
    statusAttr='trade_status'
    status='FO Confirmed'
    tradeTimeAttr='trade_tradeTime'
    clientAttr='trade_counterparty' 
    acquirerAttr='trade_acquirer'
    portfolioAttr='trade_portfolio'
    salesCustomPane='CustomPanes_SecurityLoan'
    tradingCustomPane='CustomPanes_SecurityLoan'
    amountInfo = {'amountAttr' : 'trade_quantity_value', 'amountLabelAttr' : 'trade_quantity_value'}
    
@TradeActions(increase = IncreaseCommand(nominal="trade_quantity_value",
                                       statusAttr='trade_status',
                                       newStatus='Simulated'),
              close = ReturnCommand(nominal="trade_quantity_value",
                                       statusAttr='trade_status',
                                       newStatus='Simulated'),
              recall = RecallCommand(nominal="trade_quantity_value",
                                       statusAttr='trade_status',
                                       newStatus='Simulated'),
              rerate = RerateCommand(),
              extend = ExtendCommand())
@Settings(SheetDefaultColumns=DefaultColumns(), MultiTradingEnabled=False)
@SecurityLoanSTI()
class SecurityLoanDefinition(SecurityLoan_DP.SecurityLoanDefinition):
    
    def OnInit(self):
        SecurityLoan_DP.SecurityLoanDefinition.OnInit(self)
        self._slAccountChoices = DealPackageChoiceListSource()
        self._collateralAgreementsChoiceListSource = DealPackageChoiceListSource()
        self._currentFixedRate = 0.0
        self._securityLoanWrapper = None
        self.BorrowOutLabel = _SETTINGS.BorrowOutLabel() if _SETTINGS and _SETTINGS.BorrowOutLabel() else 'Quantity'
        self.BorrowInLabel = _SETTINGS.BorrowInLabel() if _SETTINGS and _SETTINGS.BorrowInLabel() else 'Quantity'

    def OnNew(self):
        SecurityLoan_DP.SecurityLoanDefinition.OnNew(self)
        if self.receiveLeg.Leg() == self._dummyLeg:
            self.receiveLeg.UpdateIntialIndex()
            self.OnPriceFixingValueChanged('payLeg', None, self.payLeg_priceFixingValue)
            self.receiveLeg_floatRateFactor2 = 1.0 #default value
            self.receiveLeg_initialIndexValueDomestic = self.receiveLeg.InitialIndexValueDomestic() #Updates are muted in on new, read back mapped value
            
        if not self.Trade().Originator().IsInfant():
            self.DoOnOpen()
            
        if self.Trade().IsInfant():
            self.slOrderType = _SETTINGS.DefaultOrderType()
            self.tradeSource = 'Manual'
            self.trade_portfolio = FPortfolioRouter.GetPortfolio(self.Trade())
            self.trade_acquirer = DefaultAcquirer()
       
    def DoOnOpen(self):
        if self.Instrument().Legs().Size() == 1:
            self.SetAttribute('receiveLeg_indexRef', self.Instrument().Underlying(), True)
            self.SetAttribute('receiveLeg_currency', self.Instrument().Currency(), True)
            self.SetAttribute('receiveLeg_startDate', self.Instrument().LegStartDate(), True)
            
        if self.trade_status in ('Simulated', 'Reserved'):
            self.ins_cfgRegenerateAll = True
            self.ins_cfgRegenerate = True
     
    def OnSave(self, saveConfig):
        if saveConfig.InstrumentPackage() == "SaveNew":
            if not self.Instrument().IsInfant():
                self.Instrument().Name = ''
        return DealDefinition.OnSave(self, saveConfig)
    
  
    trade                     = SecurityLoanTrade( trade='Trade')

    payLeg                    = SecurityLoanTradeLeg( leg='PayLeg', trade='Trade' )

    receiveLeg                = SecurityLoanCashLeg( leg='ReceiveOrDummyLeg', trade='Trade' )

    #Overloaded to remove buy sell version (which is default)
    tradeQuantity             = Object( label = '@TradeQuantityLabel',
                                        toolTip = "Number of contracts traded. Positive number is a borrow, negative number is a lend.",
                                        backgroundColor = '@TradeQuantityBackGroundColor',
                                        objMapping = 'Trade.Quantity',
                                        formatter = 'InstrumentDefinitionNominal',
                                        onChanged='@OnTradeQuantityChanged')

    tradeActionType        = Object( label = 'Trade Type',
                                    toolTip = "Action type of the trade.",
                                    enabled = False,
                                    visible = '@IsTradeActionTrade',
                                    objMapping = 'Trade.Type')
    # Deal fields

    putThroughClient          = Object(label = 'Put-through Client',
                                    toolTip = "Put-through client for the trade.",
                                       choiceListSource = '@PutThroughClients',
                                       objMapping = 'Trade.Guarantor')

    isRebate                  = Bool( label = 'Rebate',
                                    toolTip = "Indicating wheather this is a rebate.",
                                    objMapping = 'IsRebate')

    rebateRate                =     Float( label = 'Rebate Rate(bp)',
                                            toolTip = "Rebate rate for cash collateral in basis points.",
                                            formatter = 'SolitaryPricePercentToBasisPointOneDecimal',
                                            objMapping= 'Wrapper.RebateRate',
                                            visible='@Wrapper.IsFloatRebate')

    suggestedFee           =     CalcVal( calcMapping = 'Trade:FTradeSheet:Security Loan Suggested Fee')
    
    marketPrice         = CalcVal( label='Market Price',
                                   calcMapping = 'Underlying:FDealSheet:Instrument Market Price',
                                   valuationDetails = False,
                                   editable = False)
                                   
    corpActType         = CalcVal( label='Type',
                                   calcMapping = 'UnderlyingOriginator:FDealSheet:Corp Action Type',
                                   valuationDetails = False,
                                   visible = '@CorpActionVisible',
                                   editable = False)
                                   
    corpActName         = CalcVal( label='Name',
                                   calcMapping = 'UnderlyingOriginator:FDealSheet:Corp Action Name',
                                   valuationDetails = False,
                                   visible='@CorpActionVisible',
                                   editable = False)
                                   
    corpActDate         = CalcVal( label='Ex Date',
                                   calcMapping = 'UnderlyingOriginator:FDealSheet:Corp Action Ex Date',
                                   valuationDetails = False,
                                   visible='@CorpActionVisible',
                                   editable = False)

    note1                  = Str(label = 'Note',
                                 objMapping = 'Trade.Text1')


    underlyingSettlementCalendar = Object(label = 'Calendar',
                                          toolTip = "Calendar linked to the currency of the traded security.",
                                          enabled = False,
                                          objMapping = 'UnderlyingCalendar')

    underlyingIsin              = Object(label = 'ISIN',
                                          toolTip = "Unique ISIN identifier.",
                                          objMapping = 'UnderlyingIsin')

    underlyingSedol             = Object(label = 'SEDOL',
                                          toolTip = "Unique SEDOL identifier.",
                                          objMapping = 'UnderlyingSedol')

    slLoanId                    = Object(label = 'Loan ID',
                                          toolTip = "Loan ID.",
                                          enabled = False,
                                          objMapping = 'LoanId')

    secLoanRollType             = Object(label = 'Term',
                                         toolTip = "Term of the loan. Sets the roll type of the contract.",
                                         choiceListSource=['Open', 'Bullet', 'Evergreen', 'Terminated'],
                                         objMapping='Wrapper.RollType')

    initialCashAmount            = BuySell( label='@CashAmountWithLegCurrency',
                                            toolTip = "The collateral cash amount of the loan "
                                                    "(opposite sign of the Quantity multiplied with the Price).",
                                            objMapping='Wrapper.InitialCashAmount',
                                            visible='@ReceiveLegVisible',
                                            showBuySell=False)

    isDvP                        = Bool( label='DvP',
                                         toolTip = "Indicating wheather DvP (Delivery versus Payment) holds. "
                                                    "Sets the settlement category to 'DvP'.",
                                         objMapping='IsDvPSettled',
                                         visible='@IsDvPWithLegEnabled')

    isPaymentDvP                 = Bool( label='DvP',
                                         toolTip = "Indicating wheather DvP (Delivery versus Payment) holds. "
                                                    "Sets the settlement category to 'DvP'.",
                                         objMapping='IsPaymentDvPSettled',
                                         visible='@NotDvPWithLegEnabled')


    dvpPaymentInitialMargin      = Object( label='Initial Margin',
                                           objMapping='DvpPaymentInitialMargin',
                                           formatter = 'ImprecisePercentShowZero',
                                           visible='@IsPaymentDvPVisible')
                                           
    dvpPaymentCashAmount         = BuySell( label='Cash Amount',
                                            toolTip = "The collateral cash amount of the loan "
                                                    "(opposite sign of the Quantity multiplied with the Price).",
                                            objMapping='Wrapper.DvPPaymentCashAmount',
                                            visible='@IsPaymentDvPVisible',
                                            showBuySell=False)
                                            
    dvpPaymentCashCurrency       = Object(  label='',
                                            toolTip = "The collateral cash amount currency.",
                                            objMapping='DvpPaymentCashCurrency',
                                            visible='@IsPaymentDvPVisible')
    
    collateralType               = Object( label='Type',
                                    toolTip = "Type of collateral.",
                                    choiceListSource=['Non-Cash', 'Cash'],
                                    objMapping='CollateralType')

    tradeSource                  = Object(label='Source',
                                          toolTip = "Source from where the order came.",
                                          objMapping='OrderSource',
                                          choiceListSource = '@tradeSourceChoices')

    suggestFee                 =  Action( label = 'Suggest',
                                          toolTip = "If selected sets the fee to the suggested fee of the security.",
                                          sizeToFit=True,
                                          visible= '@PayLegIsFixed',
                                          enabled= '@IsNotRebate',
                                          action = '@DoSuggestFee')

    #AdditionalInfo deal Fields

    isinFromAddInf              = Str(label = 'ISIN',
                                         toolTip = "Unique ISIN identifier.",
                                         objMapping = 'UndIsinFromAddInf')

    slAccount                   = Str(label = 'SL Account',
                                         toolTip = "SL Account for the trade.",
                                         objMapping = 'SlAccountShortName',
                                         choiceListSource = '@slAccountChoices')

    slMinimumFee                  = Float(label = 'Minimum Fee',
                                         toolTip = "Minimum fee of the loan.",
                                         formatter = 'DetailedHideNaN',
                                         objMapping = 'SLMinimumFee')

    slOrderType                  = Str(  label = 'Order Type',
                                         toolTip = "Type of order.",
                                         choiceListSource = '@slOrderTypeChoices',
                                         objMapping = 'SLOrderType')

    slPendingOrder                = Bool(label = 'Pending Order',
                                         toolTip = "Order pending external activity such as customer reply.",
                                         enabled = False,
                                         objMapping = 'SLPendingOrder')

    slTradingStock                = Bool(label = 'Trading Stock',
                                         toolTip = "Indicating wheather this is a trading stock.",
                                         objMapping = 'SLTradingStock')

    slPrepay                      = Bool(label = 'Pre-pay',
                                       toolTip = "Indicating wheather this loan is pre-pay.",
                                       objMapping = 'SLPrePay')

    slNonBreakable                = Bool(label = 'Non-breakable',
                                        toolTip = "Indicating wheather this loan is non-breakable.",
                                        objMapping = 'SLNonBreakable')

    collateralAgreementAddInf = Object(label = 'Collateral Agreement',
                                        toolTip = "Collateral agreement for the counterparty.",
                                        width = 25, #Adding some extra width to this field to avoid a right shift of the dialog when visibility changes
                                        choiceListSource = '@CollateralAgreementsChoiceListSource',
                                      objMapping = 'SLCollateralAgreement')

    # Attribute override
    def AttributeOverrides(self, overrideAccumulator):

        def GeneralAttributes():
            return {}


        def InsAttributes():
            return {
                'ins_underlying': dict(toolTip = '@UnderlyingInformationInToolTip'),
                'insID_externalId1': dict(label = 'SL ID'),
                'ins_openEnd': dict(visible = False),
                'ins_noticePeriod': dict(visible = '@NoticePeriodApplicable'),
                'ins_startDate': dict(transform='@StartDateTransform'),
                'ins_endDate': dict(transform='@EndDateTransform',
                                                                 visible='@EndDateVisible'),
                'ins_endPeriod': dict(visible='@EndDateVisible'),
                'ins_dividendFactor': dict(formatter='ImprecisePercentShowZero'),
                'payLeg_priceFixingValue': dict(onChanged='@OnPriceFixingValueChanged'),
                'receiveLeg_priceFixingValue': dict(onChanged='@OnPriceFixingValueChanged'),
                }


        def TradeAttributes():
            return {
                'trade_collateralAgreement': dict(label = 'Collateral Profile',
                                                                  onChanged = '@SetPresetsFromHook'),
                'tradeBackOffice_trxTrade': dict(visible = '@IsShowModeTradeDetail'),
                'tradeBackOffice_tradeProcesses': dict(visible = '@IsShowModeTradeDetail'),
                'trade_payments_dialogButton': dict(visible = '@IsShowModeTradeDetail'),
                'tradeBackOffice_groupTrdnbr': dict(visible = '@IsShowModeTradeDetail'),
                'tradeBackOffice_dealPackage': dict(visible = '@IsShowModeTradeDetail'),
                'tradeBackOffice_tradePackage': dict(visible = '@IsShowModeTradeDetail'),
                'trade_counterparty': dict(onChanged = '@OnCounterpartyChanged'),
                'trade_valueDay': dict(visible = '@IsShowModeTradeDetailOrIsTradeAction'),
                }


        def TradeTypeDisableAttrs(base):
            def createEnabledDict(baseDict):
                d = dict(enabled = '@IsOpeningTrade')
                if baseDict:
                    d.update(baseDict)
                return d

            attrs = ['ins_underlyingType', 'ins_underlying', 'isinFromAddInf', 'underlyingSedol', 'ins_dividendFactor', 'ins_currency', 'payLeg_startDate', 'ins_startDate']
            return {a: createEnabledDict(base.get(a)) for a in attrs}

        accumulator = dict()
        accumulator.update(GeneralAttributes())
        accumulator.update(TradeAttributes())
        accumulator.update(InsAttributes())
        accumulator.update(TradeTypeDisableAttrs(accumulator))
        overrideAccumulator(accumulator)
    
    def Underlying(self, *args):
        return self.Instrument().Underlying()
        
    def UnderlyingOriginator(self, *args):
        if self.Underlying():
            return self.Underlying().Originator()
        else:
            return None
    
    def IsShowModeTradeDetailOrIsTradeAction(self, *args):
        return self.IsShowModeTradeDetail() or self.IsTradeActionTrade()

    def IsTradeActionTrade(self, *args):
        return not self.IsOpeningTrade()

    def IsOpeningTrade(self, *args):
        return self.Trade().Type() in ['Normal', 'None', ]

    def UnderlyingInformationInToolTip(self, *args):
        def niceStr(obj, m):
            target = getattr(obj, m)()
            return str(target.StringKey()) if hasattr(target, 'StringKey') else str(target)

        if self.ins.underlying is None:
            return ''

        tt = 'Instrument Properties: \n'
        props = ['Name', 'Isin', 'ExternalId1', 'ExternalId2', 'Currency']
        for m in props:
            lengths = [len]
            separator = ' - '
            tt += m + ': ' + niceStr(self.ins.underlying, m) + '\n'
        tt += '\nAdditional infos: \n'
        for add_inf in acm.FAdditionalInfo.Select('recType = "Instrument" and recaddr = {0}'.format(self.ins.underlying.Oid())):
            tt += niceStr(add_inf, 'AddInf') + ': ' + niceStr(add_inf, 'FieldValue') + '\n'
        return tt


    def TradeQuantityBackGroundColor(self, *args):
        if self.tradeQuantity == 0:
            return None
        elif self.tradeQuantity > 0:
            return 'BkgTickerOwnBuyTrade'
        else:
            return 'BkgTickerOwnSellTrade'

    def TradeQuantityLabel(self, *args):
        if self.tradeQuantity == 0:
            return 'Quantity'
        elif self.tradeQuantity >= 0:
            return self.BorrowInLabel
        else:
            return self.BorrowOutLabel

    def OnTradeQuantityChanged(self, attributeName, oldValue, newValue, userInputAttributeName):
        if self.IsPaymentDvPSettled() and self.IsRebate() and not userInputAttributeName:
            self.Wrapper().DvPPaymentCashAmount(self.initialCashAmount_value)
            
    def OnInstrumentCurrencyChanged(self, attributeName, oldValue, newValue, *args):
        super(SecurityLoanDefinition, self).OnInstrumentCurrencyChanged(attributeName, oldValue, newValue, *args)
        self.SetAttribute('receiveLeg_currency', newValue, True)
        self.UpdateTradeCurrAndDates()
        
    # Mapped python methods
    @ReturnDomainDecorator('string')
    def UnderlyingSedol(self, value = 'NoValue', *args):
        if value == 'NoValue':
            underlying = self.Instrument().Underlying()
            if underlying:
                alias = acm.FInstrumentAlias.Select01('instrument = "{0}" and type = "{1}"'.format(underlying.Oid(), 'SEDOL'), '')
                return alias.Alias() if alias else ''
        else:
            alias = acm.FInstrumentAlias.Select01('alias like "{0}" and type = "{1}"'.format(value, 'SEDOL'), '')
            if alias and alias.Instrument():
                self.ins.underlying = alias.Instrument()


    @ReturnDomainDecorator('string')
    def LoanId(self, value = 'NoValue', *args):
        alias = acm.FInstrumentAlias.Select01('instrument = "{0}" and type = "{1}"'.format(self.Instrument().Name(), 'SL Loan ID'), '')
        return alias.Alias() if alias else ''

    @ReturnDomainDecorator('FCalendar')
    def UnderlyingCalendar(self, *args):
        underlying = self.Instrument().Underlying()
        if underlying:
            return underlying.Currency().Calendar()


    @ReturnDomainDecorator('string')
    def OrderSource(self, value = 'NoValue', *args):
        if value == 'NoValue':
            market = self.Trade().Market()
            if market:
                return market.Name()
        else:
            market = acm.FMarketPlace.Select01('name like {0}'.format(value), None)
            if market:
                self.Trade().Market= market

    @ReturnDomainDecorator('string')
    def UnderlyingIsin(self, value = 'NoValue', *args):
        if value == 'NoValue':
            underlying = self.Instrument().Underlying()
            if underlying:
                return underlying.Isin()
        else:
            underlying = acm.FInstrument.Select01('isin like {0}'.format(value), None)
            if underlying:
                self.ins.underlying = underlying


    @ReturnDomainDecorator('string')
    def SlAccountShortName(self, value = 'NoValue', *args):
        if useCustomHooks is True:
            cpty = self.Trade().Counterparty()
            if cpty:
                if value == 'NoValue':
                    id = self.Trade().AddInfoValue("SL_Account")
                    return FromIdToShortName(cpty, id)
                else:
                    id = FromShortNameToId(cpty, value)
                    self.Trade().AddInfoValue("SL_Account", id)
            else:
                self.Trade().AddInfoValue("SL_Account", None)


    def UpdateTradeCurrAndDates(self):
        self.Trade().Trade().Currency(self.Instrument().Currency())
        self.UpdateStartDate()
        self.Instrument().SpotBankingDaysOffset(0)
        self.SetPayCalendars(self.isDvP or self.isPaymentDvP)
        self.Wrapper().UpdateDvPPayment(True)
        if self.Wrapper().IsPaymentDvPSettled() and self.IsRebate():
            self.Wrapper().DvPPaymentCashAmount(self.initialCashAmount_value)   
        
    def SetPayCalendars(self, isDvP):
        underlying = self.Instrument().Underlying()
       
        pay1Calendar = underlying.Currency().Calendar() if underlying else self.Instrument().Currency().Calendar()
        pay2Calendar = self.Instrument().Currency().Calendar() if isDvP else None
        if pay2Calendar == pay1Calendar:
            pay2Calendar = None
        
        self.PayLeg().PayCalendar(pay1Calendar)
        self.PayLeg().Pay2Calendar(pay2Calendar)
        if self.Wrapper().HasCashCollateralPool():
            self.receiveLeg.Leg().PayCalendar(pay1Calendar)
            self.receiveLeg.Leg().Pay2Calendar(pay2Calendar)
        
    def UpdateStartDate(self):
        try:
            calendarInfo = self.Instrument().Underlying().Currency().Calendar().CalendarInformation()
            self.ins.startDate = calendarInfo.AdjustBankingDays(self.Trade().TradeTime(), self.GetDefaultSettlementDelay())
            self.Trade().Trade().ValueDay = self.ins.startDate
            self.Trade().Trade().AcquireDay = self.ins.startDate
        except:
            pass

    def GetDefaultSettlementDelay(self):
        return 1 # Always default to one day in the future. Market standard is typically underlying spot day - 1, i.e. typically 1 day.

    @ReturnDomainDecorator('string')
    def UndIsinFromAddInf(self, value = 'NoValue', *args):
        if value == 'NoValue':
            underlying = self.Instrument().Underlying()
            if underlying:
                return underlying.AddInfoValue("ID_ISIN")
        else:
            if self.ins.underlying.AddInfoValue("ID_ISIN") != value:
                try:
                    add_inf = acm.FAdditionalInfoSpec.Select01('fieldName = "ID_ISIN"', None)
                    und = acm.FAdditionalInfo.Select('fieldValue like "{0}" and addInf = {1}'.format(value, add_inf.Oid()))
                    ins = und.First().Parent()
                except StandardError as e:
                    pass
                else:
                    if isinstance(ins, acm._pyClass("FInstrument")):
                        self.ins.underlying = ins
    
    @ReturnDomainDecorator('bool')
    def IsDvPSettled(self, value = 'NoValue', *args):
        if value != 'NoValue':
            self.SetPayCalendars(value)
            start = self.Instrument().LegStartDate()
            calendarInfo = self.Instrument().Currency().Calendar().CalendarInformation()
            if value and calendarInfo.IsNonBankingDay(start):
                self.DealPackage().GUI().GenericMessage('Note! Value day on a non-banking day in the Loan currency')
        return self.Wrapper().IsDvPSettled(value, *args)
        
        
    def IsPaymentDvPSettled(self, value = 'NoValue', *args):
        if value != 'NoValue':
            self.SetPayCalendars(value)
            start = self.Instrument().LegStartDate()
            calendarInfo = self.Instrument().Currency().Calendar().CalendarInformation()
            if value and calendarInfo.IsNonBankingDay(start):
                self.DealPackage().GUI().GenericMessage('Note! Value day on a non-banking day in the Loan currency')
        return self.Wrapper().IsPaymentDvPSettled(value, *args)
            
    def DvpPaymentInitialMargin(self, value = 'NoValue', *args):
        return self.Wrapper().DvpPaymentInitialMargin(value, *args)

    @ReturnDomainDecorator('FCurrency')
    def DvpPaymentCashCurrency(self, value = 'NoValue', *args):
        if value != 'NoValue':
            initialMargin = self.dvpPaymentInitialMargin
            if value and value != self.Trade().Currency():
                self.dvpPaymentCashAmount_value = -self.Wrapper().Nominal() * self.Wrapper().CalcFXRate(self.Trade().Currency(), value) * initialMargin 
            else:
                self.dvpPaymentCashAmount_value = -self.Wrapper().Nominal() * initialMargin
        return self.Wrapper().DvpPaymentCashCurrency(value, *args)
            
    @ReturnDomainDecorator('string')
    def CollateralType(self, value = 'NoValue', *args):
        if value == 'NoValue':
            return 'Cash' if self.Wrapper().HasCashCollateralPool() is True else 'Non-Cash'
        else:
            if value == 'Cash':
                self.Wrapper().HasCashCollateralPool(True)
                if self.payLeg.PriceFixingStatusIsMarket():
                    self.receiveLeg.initialFX = self.payLeg.initialFX
            else:
                self.isRebate = False
                self.isDvP = False
                self.Wrapper().HasCashCollateralPool(False)

    def slOrderTypeChoices(self, *args):
        a = acm.FArray()
        a.Add('')
        for c in acm.FChoiceList.Select("list='SBL_OrderType'"):
            a.Add(c.Name())
        return a

    def SlBooleanAddInfoField(self, obj, addInfo, value):
        if value == 'NoValue':
            return bool(obj.AddInfoValue(addInfo))
        else:
            obj.AddInfoValue(addInfo, True if value is True else None)

    @ReturnDomainDecorator('bool')
    def SLTradingStock(self, value = 'NoValue', *args):
        return self.SlBooleanAddInfoField(self.Instrument(), "SL_TradingStock", value)

    @ReturnDomainDecorator('bool')
    def SLPrePay(self, value = 'NoValue', *args):
        return self.SlBooleanAddInfoField(self.Trade(), "SL_PrePay", value)

    @ReturnDomainDecorator('bool')
    def SLNonBreakable(self, value = 'NoValue', *args):
        return self.SlBooleanAddInfoField(self.Instrument(), "SL_NonBreakable", value)

    @ReturnDomainDecorator('string')
    def SLOrderType(self, value = 'NoValue', *args):
        if value == 'NoValue':
            return self.Trade().AddInfoValue("SBL_OrderType") or ''
        else:
            self.Trade().AddInfoValue("SBL_OrderType", value if bool(value) is True else None)

    @ReturnDomainDecorator('bool')
    def SLPendingOrder(self, value = 'NoValue', *args):
        return self.SlBooleanAddInfoField(self.Trade(), "SBL_PendingOrder", value)

    @ReturnDomainDecorator(str(acm.FAdditionalInfoSpec["SL_MinimumFee"].DataDomain().Name()))
    def SLMinimumFee(self, value = 'NoValue', *args):
        if value == 'NoValue':
            return self.Instrument().AddInfoValue("SL_MinimumFee")
        else:
            self.Instrument().AddInfoValue("SL_MinimumFee", value)

    @ReturnDomainDecorator(str(acm.FAdditionalInfoSpec["CollateralAgreement"].DataDomain().Name()))
    def SLCollateralAgreement(self, value = 'NoValue', *args):
        if value == 'NoValue':
            return self.Trade().AddInfoValue("CollateralAgreement")
        else:
            self.Trade().AddInfoValue("CollateralAgreement", value)

    # Actions
    def ExtendOpenEnd(self, date):
        self.Wrapper().ExtendOpenEnd(date)

    def Rerate(self, leg, date, fee, extendToDate):
        if extendToDate is not None:
            self.ExtendOpenEnd(extendToDate)
        feeWrapper = FSecLendDealUtils.FeeWrapper(leg)
        fee = feeWrapper.FeeAtDate(date, fee)

    def DoSuggestFee(self, *args):
        if useCustomHooks:
            if self.IsRebate() is False:
                self.payLeg.currentFee = self.suggestedFee.Value()
   
    #Transforms
    def StartDateTransform(self, attr, newDate):
        try:
            newDate = str(int(newDate)) + 'd'
        except ValueError:
            pass
        if acm.Time().PeriodSymbolToDate(newDate):
            if newDate[-1:] == 'd':
                wrapper = FSecLendDealUtils.FeeWrapper(self.Leg())
                calendarInfo=wrapper.CalendarInformation()
                today = acm.Time().DateToday()
                newDate = calendarInfo.AdjustBankingDays(today, newDate[:-1])
            else:
                newDate = self.Instrument().LegStartDateFromPeriod(newDate)
        return newDate


    def EndDateTransform(self, attr, newDate):
        try:
            newDate = str(int(newDate)) + 'd'
        except ValueError:
            pass
        if acm.Time().PeriodSymbolToDate(newDate):
            newDate = self.Instrument().LegEndDateFromPeriod(newDate)
        return newDate

    #Visibility callbacks
    def EndDateVisible(self, *args):
        visible = True
        if self.Instrument().OpenEnd() == 'Open End':
            visible = self.IsShowModeInstrumentDetail()
        return visible

    def NoticePeriodApplicable(self, *args):
        return self.Instrument().OpenEnd() != 'None' and self.Instrument().NoticePeriod() != self.Wrapper().UnderlyingSpotDays()

    def IsPersisted(self, *args):
        return self.Instrument().Originator().IsInfant() == False

    def IsPersistedOpenEnd(self, *args):
        return self.IsPersisted() and self.Instrument().Originator().OpenEnd() == 'Open End'

    def IsNotRebate(self, *args):
        return not self.Wrapper().IsRebate()

    def IsCrossCurrencyRebate(self, *args):
        return self.Wrapper().IsRebate() and self.receiveLeg.InitialFXVisible()

    def IsShowModeInstrumentDetailNoOverride(self, *args):
        return NoOverride if self.IsShowModeInstrumentDetail() else False

    def IsRebateNoOverride(self, *args):
        return NoOverride if self.IsRebate() else False

    @ReturnDomainDecorator('bool')
    def IsRebate(self, value='NoValue', *args):
        if value == 'NoValue':
            return self.Wrapper().IsRebate(value, *args)
        else:
            nominal = self.Wrapper().Nominal()
            self.Wrapper().IsRebate(value, *args)
            if self.IsPaymentDvPSettled():
                if value is True:
                    self.Wrapper().DvPPaymentCashAmount(-nominal)
                elif value is False:
                    self.Wrapper().DvPPaymentCashAmount(-nominal)
        
    def PayLegIsFixed(self, *args):
        return self.PayLeg().IsFixedLeg()

    def IsPaymentDvPVisible(self, *args):
        return self.IsPaymentDvPSettled() and not self.isRebate
        
    def NotDvPWithLegEnabled(self, *args):
        return not self.IsDvPWithLegEnabled()
        
    def IsDvPWithLegEnabled(self, *args):
        return self.Wrapper().IsDvPSettled()
    
    def CorpActionVisible(self, *args):
        try:
            corpAct_cb=acm.GetFunction('get_corporate_actions', 1)
            nextcorpAct_cb=acm.GetFunction('get_next_corporate_action', 1)
            corpActs=corpAct_cb(self.UnderlyingOriginator())
            return True if nextcorpAct_cb(corpActs) else False
        except:
            return False

    #Dynamic labels

    def NominalWithLegCurrency(self, sender, *args):
        leg = None
        leg = self.receiveLeg if 'receiveLeg' in sender else self.payLeg
        if leg.InitialFXVisible():
            return leg.currency.StringKey()+ ' ' + 'Value'
        else:
            return 'Value'


    def CashAmountWithLegCurrency(self, sender, *args):
        if self.receiveLeg.InitialFXVisible():
            return self.receiveLeg.currency.StringKey()+ ' ' + 'Cash Amount'
        else:
            return 'Cash Amount'

    def CurrentFeeLabel(self, attributeName):
        if attributeName[:3] == 'pay':
            return 'Fee(bp)'
        else:
            if self.ReceiveOrDummyLeg().LegType() == 'Fixed':
                return self.ReceiveLegFixedRateLabel()
            else:
                 return 'Spread(bp)'


    def ReceiveLegFixedRateLabel(self, *args):
        return 'Rebate Rate(bp)' if self.IsRebate() else 'Rate(bp)'

    #OnChange callbacks
    def OnNominalValueChanged(self, attributeName, oldNominal, newNominal, userInputAttributeName=None):
        if not self.isRebate:
            self.Wrapper().RefreshDvPPaymentAmount(oldNominal, newNominal)
        
    def OnStartDateChanged(self, attributeName, oldValue, newValue, userInputAttributeName=None):
        self.Trade().Trade().ValueDay = self.ins.startDate
        self.Trade().Trade().AcquireDay = self.ins.startDate
        self.SetAttribute('receiveLeg_startDate', self.ins.startDate)
        if userInputAttributeName != 'collateralType':
            if self.Wrapper().HasCashCollateralPool():
                self.receiveLeg.UpdateIntialIndex()
            self.payLeg.UpdateIntialIndex()
        self.Wrapper().UpdateDvPPayment()

    def SuggestInitialIndexValueForInitialPrice(self, leg):
        value = 0.0
        if leg.IndexRef():
            insCopy = leg.Instrument().StorageNew() if self.Instrument().Originator().IsInfant() else self.Instrument().Instrument().StorageImage()
            legCopy = insCopy.FirstPayLeg() if leg.PayLeg() else insCopy.FirstReceiveLeg()
            legCopy.NominalScaling = 'Price'
            legCopy.IndexRefFixingDateRule = self.Wrapper().GetOrCreateDefaultIndexRefFixingDateRule(leg.IndexRef().Originator())
            legCopy.InitialIndexValue = 0.0
            isCrossCurr =  legCopy.IndexRef().Currency() != insCopy.Currency()
            if isCrossCurr:
                legCopy.IndexRefFXFixingType = 'Explicit'
            else:
                legCopy.IndexRefFXFixingType = 'None'
                    
            legCopy.GenerateCashFlows(0.0)
            for c in legCopy.CashFlows():
                for r in c.Resets():
                    r.FixFixingValue = acm.Math().NotANumber()
                    legCopy.Resets().Add(r)
            value = self.Wrapper().LegInitialNominalScalingEstimate(legCopy)
            if isCrossCurr:
                fx = self.Wrapper().LegInitialIndexFXEstimate(legCopy)
                if fx:
                    value = value * fx
        return value 

    def SuggestInitialIndexValues(self, value = None):
        value = self.SuggestInitialIndexValuesForLeg(self.payLeg, value);
        self.SuggestInitialIndexValuesForLeg(self.receiveLeg, value);
            
    def SuggestInitialIndexValuesForLeg(self, leg, value = None):
        if  value is None:
            if 'Initial Price' == leg.Leg().NominalScaling():
                value = self.SuggestInitialIndexValueForInitialPrice(leg.Leg().Leg())
            else:
                value = self.Wrapper().LegInitialNominalScalingEstimate(leg.Leg())
           
        leg.SetInitialIndexValue(value)
        return value

    def OnCounterpartyChanged(self, sender, *args):
        self.Trade().AddInfoValue("SL_Account", None)
        self.slAccount = None if self._slAccountChoices.IsEmpty() else self._slAccountChoices.First()
        self.collateralAgreementAddInf = None if self._collateralAgreementsChoiceListSource.IsEmpty() \
                                            else self._collateralAgreementsChoiceListSource.First()
        self.Wrapper().UpdateDvPPayment()
        self.SetPresetsFromHook(sender)
        
    def OnUnderlyingChanged(self, attributeName, oldValue, newValue, *args):
        self.SetAttribute('_indexRef', newValue, True)
        self.SetAttribute('receiveLeg_indexRef', newValue, True)
        if newValue is not None:
            self.SetAttribute('ins_currency', newValue.Currency(), True)
            self.SetAttribute('receiveLeg_currency', newValue.Currency(), True)
            self.SetAttribute('ins_noticePeriod', self.Wrapper().UnderlyingSpotDays())
            
            self.UpdateTradeCurrAndDates()
            self.payLeg.indexRefFixingDateRule = self.Wrapper().GetOrCreateDefaultIndexRefFixingDateRule(newValue)
            
            if self.Wrapper().HasCashCollateralPool(): 
                self.receiveLeg.indexRefFixingDateRule = self.payLeg.indexRefFixingDateRule
            else:
                self.receiveLeg.indexRefFixingDateRule = None
            self.UpdateIndexRefFXFixingType()
            self.SetPresetsFromHook(attributeName)
            
    def SetPresetsFromHook(self, sender, *args):
        if useCustomHooks is True:
            map = {'ins_underlying': PresetOnUnderlyingChanged,
                    'slAccount': PresetOnAccountChanged,
                    'trade_counterparty': PresetOnCounterpartyChanged }
            fkn = attrs = map.get(sender)
            if fkn:
                attrs = fkn(self.Trade())
                for k, v in attrs.iteritems():
                    self.DealPackage().SetAttribute(k, v)
                    self.DealPackage().Refresh()
                self.RefreshDynamicLists()

    def RefreshDynamicLists(self):
        self.RefreshSLAccountChoices()
        self.RefreshCollateralAgreementChoices()

    def RefreshSLAccountChoices(self):
        self._slAccountChoices.Clear()
        if useCustomHooks is True:
            cpty = self.Trade().Counterparty()
            if cpty:
                self._slAccountChoices.AddAll(GetAccountChoices(cpty))


    def RefreshCollateralAgreementChoices(self):
        self._collateralAgreementsChoiceListSource.Clear()
        if useCustomHooks is True:
            cpty = self.Trade().Counterparty()
            self._collateralAgreementsChoiceListSource.AddAll(GetCollateralAgreementChoices(cpty))

    def CollateralAgreementsChoiceListSource(self, *args):
        if self._collateralAgreementsChoiceListSource.IsEmpty():
            self.RefreshCollateralAgreementChoices()
        return self._collateralAgreementsChoiceListSource


    def InitialMarginChanged(self, attributeName, oldValue, newValue, userInputAttributeName=None):
        if self.IsPaymentDvPSettled() and self.isRebate:
            self.Wrapper().DvPPaymentCashAmount(self.Wrapper().InitialCashAmount())
            
    #Synchronize the prices between the legs       
    def OnPriceFixingValueChanged(self, attributeName, oldValue, newValue, userInputAttributeName=None):
        if oldValue != newValue and newValue is not None and userInputAttributeName != 'collateralType':
            if 'payLeg' in attributeName:
                factor = self.ReceiveOrDummyLeg().NominalFactor() / self.PayLeg().NominalFactor()
                if self.receiveLeg.priceFixingValue != newValue * factor:
                    self.SetAttribute('receiveLeg_priceFixingValue', newValue * factor, silent = True)
            else:
                if self.IsRebate():
                    factor =  self.PayLeg().NominalFactor() / self.ReceiveOrDummyLeg().NominalFactor()
                    if self.payLeg.priceFixingValue != newValue * factor:
                        self.SetAttribute('payLeg_priceFixingValue', newValue * factor, silent = True)

    #Counterparties which are marked as not trading are applicable
    def PutThroughClients(self, *args):
        return acm.FCounterParty.Select('notTrading = True')

    def slAccountChoices(self, *args):
        if self._slAccountChoices.IsEmpty():
            self.RefreshSLAccountChoices()
        return self._slAccountChoices

    def tradeSourceChoices(self, *args):
        return GetOrderSources()

    def Wrapper(self, *args):
        if self._securityLoanWrapper is None or self._securityLoanWrapper.Trade() != self.Trade():
            self._securityLoanWrapper = FSecLendDealUtils.SecurityLoanWrapper.Wrap(self.Trade())
        return self._securityLoanWrapper

    def CustomPanes(self):
        customPanes = []
        customPanes.append({'Instrument':self.GetCustomPanesFromExtValue('CustomPanes_SecurityLoanTrade')})
        customPanes.append({'Trade':self.GetCustomPanesFromExtValue('CustomPanes_SecurityLoan')})
        return customPanes


class MasterSecurityLoanDefinition(SecurityLoanDefinition):

    collateralType = Object( label='Type',
                            toolTip = "Type of collateral.",
                            choiceListSource=['Non-Cash'],
                            objMapping='CollateralType')

    def CustomPanes(self):
        customPanes = []
        customPanes.append({'Instrument':self.GetCustomPanesFromExtValue('CustomPanes_MasterSecurityLoanTrade')})
        customPanes.append({'Trade':self.GetCustomPanesFromExtValue('CustomPanes_MasterSecurityLoan')})
        return customPanes

    def OnUnderlyingChanged(self, attributeName, oldValue, newValue, *args):
        super(MasterSecurityLoanDefinition, self).OnUnderlyingChanged(attributeName, oldValue, newValue, *args)

        try:
            if FSecLendUtils.GetMasterSecurityLoan(self.ins.underlying):
                self.DealPackage().GUI().GenericMessage("WARNING: There is already a Master Security Loan over Security '{0}'".format(self.ins.underlying.Name()))
                self.ins.underlying = None
            else:
                self.SetPresetsFromHook(attributeName)
        except:
            self.DealPackage().GUI().GenericMessage("ERROR: There is more than one Master Security Loan over Security '{0}' in the system.".format(self.ins.underlying.Name()))
            self.ins.underlying = None

    def OnSave(self, saveConfig):
        if saveConfig.InstrumentPackage() == "SaveNew":
            try:
                if FSecLendUtils.GetMasterSecurityLoan(self.ins.underlying):
                    #There is an existing Master Security Loan for this underlying.
                    saveConfig.InstrumentPackage("Exclude")
                else:
                    self.Instrument().Name(self.SuggestName())
                    DealDefinition.OnSave(self, saveConfig)
            except:
                #There are more than one Master Security Loan over this underlying.
                saveConfig.InstrumentPackage("Exclude")

        if saveConfig.DealPackage() == "SaveNew":
            if saveConfig.InstrumentPackage() == "SaveNew":
                self.Instrument().Name(self.SuggestName())
            DealDefinition.OnSave(self, saveConfig)

    def SuggestName(self):
        if self.ins.underlying:
            insName = "%s/%s/MASTER" %(self.ins.underlying.Name(), self.Instrument().Currency().Name())
            return insName
