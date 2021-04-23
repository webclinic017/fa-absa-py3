
from __future__ import print_function
import acm 

from DealPackageDevKit import DealPackageDefinition, CompositeAttributeDefinition, ReturnDomainDecorator, DealPackageChoiceListSource, AttributeDialog, Object, Label, Settings, DealPackageException, Delegate, Action, Int, Str, TradeActions, CorrectCommand, NovateCommand, CloseCommand, MirrorCommand, Bool, Float, InstrumentPart, TradeStatusChoices, ContextMenu, ContextMenuCommand, SalesTradingInteraction, CustomActions, DealPackageUserException, Text, NoOverride, List
from DealPackageUtil import NoChange
from CompositeAttributesLib import PaymentsDialog, OperationsPanel

from CommodityStripPopulators import ChoiceListPopulator
from CommodityStripCompositeAttributes import CommodityStripDates, CommodityStripOptionData
from CommodityStripExtensionPoints import CustomAttributeOverrides, CustomAttributes, StripDealTypeMapping, DefaultStripType, PageGroup, SuggestInstrumentPackageName, OnInstrumentsUpdated, SumForContractSize, GetConfig, DealPackageDefaultValues, InstrumentPackageDefaultValues, LiveTradesOrAll, SetDefaultValuesOnChange, InitTrade, OnSave, IsValid, CommodityCanUseCurrentFuture

from CommodityStripUtils import FirstDate, LastDayOfMonth, GetStripTypeFromInstruments, GetExpiryTypeFromInstruments, GetStructureTypeFromInstruments, CopyTrade, GetMonth, UpdateTradeInstrument, TransactionHistoryAction, Clipboard, LockedInstrumentPartAttributes, GetCurrentFutures, GetIsCurrentFutureFromInstruments, StripPriceFormatter

def GetDefaultAutoGenerate():
    extValue = acm.GetDefaultContext().GetExtension(acm.FExtensionValue, acm.FObject, 'autoGenerateCommodityStrip')
    if extValue:
        autoGenerate = str(extValue.Value()).lower() == 'true'
    else:
        autoGenerate = True
    return autoGenerate

class CommodityStripSTI(SalesTradingInteraction):
    createTradesOnRequest=True
    allInPriceAttr='price'
    statusAttr='tradeStatus'
    status='FO Confirmed'
    amountInfo = {'name' : 'Quantity',
                  'amountAttr' : 'nominalInQuotation_value',
                  'amountLabelAttr' : 'nominalInQuotationFormatted',
                  'quotationLabelAttr' : 'quotationFormatted'} 
    tradeTimeAttr='tradeTime'
    clientAttr='counterParty' 
    acquirerAttr='acquirer'
    portfolioAttr='portfolio' 
    salesCustomPane='CustomPanes_CommodityStripRFQ'
    tradingCustomPane='CustomPanes_CommodityStripQRR'
            
@CommodityStripSTI()
@Settings(
    GraphApplicable=False,
    MultiTradingEnabled=True)
@CustomActions(
    transactionHistory=TransactionHistoryAction)
@TradeActions( 
    close=CloseCommand(nominal='aggregateNominal'),
    novate=NovateCommand(nominal='aggregateNominal'),
    correct=CorrectCommand(statusAttr='tradeStatus', newStatus='Simulated'),
    mirror=MirrorCommand(statusAttr='tradeStatus', newStatus='Simulated'))
class CommodityStrip(DealPackageDefinition):
    ONCHANGED_MODE = 2
    
    errorState = Text(label='Error',
                      editable=False,
                      height=80,
                      visible='@InErrorState',
                      textColor='SyntaxPythonOperator',
                      silent=True)
    
    def InErrorState(self, *args):
        return bool(self.errorState)
    
    def NotInErrorState(self, *rest):
        return not self.InErrorState()
    
    # "Empty composite attribute" to use when adding custom fields
    customAttributes =  CustomAttributes( tradesMethod='Trades',
                                          instrumentsMethod='Instruments', 
                                          stripComponents='Deals',
                                          templateModel='TemplateModel' )

    # Data on what to generate in strip
    stripDates =        CommodityStripDates ( objectMappingStart='StartDate',
                                              objectMappingEnd='EndDate')
                                                  
    structureType =     Object(  objMapping=InstrumentPart('StructureType'),
                                 label='Structure',
                                 toolTip='Strip - recurring payments\nSingle Leg - one paymet for entire period',
                                 choiceListSource='@ChoicesCallback',
                                 onChanged='@SetCurrentFutures|GenerateStripCB')

    stripType =         Object ( objMapping=InstrumentPart('StripType'),
                                 label='Calculation',
                                 toolTip="@StripTypeTooltip",
                                 choiceListSource='@ChoicesCallback',
                                 editable='@NotInErrorState',
                                 onChanged='@SetCurrentFutures|GenerateStripCB')

    isOptionStrip =     Bool(    objMapping='IsOptionStrip',
                                 toolTip='Determines if it is an option or a forward strip. Option strips are only available for calculation "Bullet".',
                                 enabled='@IsBullet',
                                 label='Option Strip',
                                 onChanged='@SetCashSettlement|UpdateValueDate|GenerateStripCB')

    expiryType =        Object(  objMapping=InstrumentPart('ExpiryType'),
                                 label='Expiry Type',
                                 toolTip="@ExpiryTypeToolTip",
                                 choiceListSource='@ChoicesCallback',
                                 onChanged='@ResetStartEndDateIfNeeded|GenerateStripCB')

    stripComponents =   Object ( objMapping='ActualDeals',
                                 columns='@ListTradeColumns',
                                 visible='@IsAutoGenerate',
                                 sortIndexCallback='@ListTradeSortingCallback',
                                 addNewItem =['Last', 'Sorted'],
                                 onRightClick=ContextMenu('@OpenTradeContextMenuItem'),
                                 onSelectionChanged='@SelectedDeal',
                                 dialog=AttributeDialog( 
                                    label='Edit Selected Instrument', 
                                    customPanes='@SelectedDealLayout',
                                    dealPackage='@SelectedDeal'))
                                     
    # Instrument fields
    
    enableEdit =        Action( label='Enable Edit',
                                action='@EnableEdit',
                                visible='@IsEditDisabled',
                                toolTip='Enable editing of instruments')
    
    pageGroup =         Object( domain=acm.FPageGroup)
                                
    instrumentGroup =   Object( objMapping=InstrumentPart('InstrumentGroup'),
                                domain=acm.FPhysInstrGroup,
                                label='Group',
                                onChanged='@SetChoiceListsDirty',
                                choiceListSource='@ChoicesCallback',
                                visible='@ShowGroup')

    baseUnderlying =    Delegate ( attributeMapping='Deals.baseUnderlying',
                                   label='Commodity',
                                   onChanged='@SetUnderlying|SetTradeCurrency|SetCurrentFutures|GenerateIfCurrentFuture',
                                   choiceListSource='@ChoicesCallback',
                                   visible='@DealIsVisible')

    underlying =        Delegate ( attributeMapping='Deals.underlying',
                                   label="Ref Instrument",
                                   toolTip="Instrument that is fixed against",
                                   validateMapping=False,
                                   onChanged='@SetDefaultQuotation',
                                   choiceListSource='@ChoicesCallback',
                                   visible='@DealIsVisibleAndNotUseCurrentFuture')

    useCurrentFuture =  Object (   objMapping=InstrumentPart('UseCurrentFuture'),
                                   label="Use current future",
                                   onChanged='@SetUnderlying|GenerateStripCB',
                                   visible='@UseCurrentFutureAvailable',
                                   editable="@CurrentFuturesAvailableAndStandardExpiry")

    currentFutures =    Object (   objMapping = InstrumentPart('CurrentFutures'),
                                   onChanged='@UntoggleUseCurrentFutureIfEmpty',
                                   visible=False)

    quotation =         Delegate ( attributeMapping='Deals.quotation',
                                   label='Quotation',
                                   toolTip='Unit of trade price, theoretical price, market price, MtM price etc for this instrument',
                                   choiceListSource='@ChoicesCallback',
                                   visible='@DealIsVisible')
    
    quotationFormatted = Label( label='@QuotationFormatted')

    contractSizeInQuotation = Object(label='Quot Size',
                                   objMapping='ContractSizeInQuotation',
                                   toolTip="Contract Size expressed in instrument's quotation",
                                   visible='@ContractSizeInQuotationVisible',
                                   editable=False)
    
    currency =          Delegate ( attributeMapping='Deals.currency',
                                   label='Currency',
                                   toolTip="Currency of strip and component instruments",
                                   onChanged='@SetTradeCurrency',
                                   choiceListSource='@ChoicesCallback',
                                   visible='@DealIsVisible')

    otc =               Delegate ( attributeMapping='Deals.otc',
                                   onChanged='@GenerateStripCB',
                                   label='Otc')

    payDayOffset =      Delegate ( attributeMapping='Deals.payDayOffset',
                                   toolTip="@PayDayOffsetTooltip",
                                   validateMapping=False)

    payOffsetMethod =   Delegate ( attributeMapping='Deals.payOffsetMethod',
                                   validateMapping=False,
                                   toolTip="Day adjustment method",
                                   label='')
                                   
    payDayMethod =      Delegate ( attributeMapping='Deals.payDayMethod',
                                   validateMapping=False,
                                   domain='enum(BusinessDayMethod)',
                                   visible='@VisibleIfDelagatesHaveAttribute',
                                   label='')

    fxSource =          Delegate ( attributeMapping='Deals.fxSource',
                                   validateMapping=False,
                                   toolTip="Source where FX rates are observed",
                                   choiceListSource='@ChoicesCallback',
                                   visible='@DealIsVisible' )
                        
    convType =          Delegate ( attributeMapping='Deals.convType',
                                   toolTip="Type of FX translation used to calculate Payoff in strip currency",
                                   validateMapping=False,
                                   choiceListSource='@ChoicesCallback',
                                   visible='@DealIsVisible' )
    
    fxFixRule =         Delegate ( attributeMapping='Deals.fxFixRule',
                                   validateMapping=False,
                                   choiceListSource='@ChoicesCallback',
                                   visible='@DealIsVisible')
                                   
    fixingSource =      Delegate ( attributeMapping='Deals.fixingSource',
                                   toolTip="Source where prices of reference instrument are observed",
                                   validateMapping=False,
                                   choiceListSource='@ChoicesCallback',
                                   visible='@DealIsVisible' )
                                   
    importStripComponents = Action(label='Import',
                                   enabled=False,
                                   visible='@IsAutoGenerate',
                                   action='@ImportStripComponents')
                                   
    exportStripComponents = Action(label='Export',
                                   enabled=False,
                                   visible='@IsAutoGenerate',
                                   action='@ExportStripComponents',
                                   silent=True )
    
    # Operations tab
    operationsPanel =   OperationsPanel() 
    
    # Deal Package fields
    
    insPackageName =    Object ( objMapping='InstrumentPackage.Name',
                                 label='Name')
    
    suggestNameButton = Action(  label='Suggest',
                                 action='@SuggestNameButton')

    # Trade fields
    quantity_value =    Delegate ( attributeMapping = 'Deals.quantity_value',
                                   visible='@IsForwardStrip',
                                   toolTip='@QuantityTooltip',
                                   validateMapping=False)

    quantity_buySell =  Delegate ( attributeMapping = 'Deals.quantity_buySell',
                                   visible='@IsForwardStrip',
                                   toolTip='@QuantityTooltip',
                                   validateMapping=False)
      
    nominalInQuotation_value = Delegate ( attributeMapping = 'Deals.nominalInQuotation_value',
                                   validateMapping=False)
    
    nominalInQuotationFormatted = Label( label='@NominalInQuotationFormatted')

    counterParty =      Object (   objMapping='Trades.Counterparty',
                                   choiceListSource='@ChoicesCallback',
                                   label='Cpty')
    
    tradeCurrency =     Object (   objMapping='Trades.Currency',
                                   choiceListSource='@ChoicesCallback',
                                   label='Premium Currency',
                                   visible='@IsOptionStrip')

    tradeCurrencyRedec = Object(   objMapping='RedecoratedTrades.Currency',
                                   visible=False)
    
    portfolio =         Object (   objMapping='Trades.Portfolio',
                                   choiceListSource='@ChoicesCallback',
                                   label='Portfolio')
    
    acquirer =          Object (   objMapping='Trades.Acquirer',
                                   choiceListSource='@ChoicesCallback',
                                   toolTip='The internal department which is the acquirer for this trade',
                                   label='Acquirer')

    broker =            Object (   objMapping='Trades.Broker', 
                                   choiceListSource='@ChoicesCallback',
                                   label='Broker') 

    tradeTime =         Object (   objMapping='Trades.TradeTime',
                                   transform='@TransformPeriodToDate',
                                   label='Trd Time')
    
    valueDay =          Object (   objMapping='Trades.ValueDay',
                                   validateMapping=False,
                                   toolTip='@ValueDayTooltip',
                                   transform='@TransformPeriodToDate',
                                   label='Value Day')

    acquireDay =        Object (   objMapping='Trades.AcquireDay',
                                   validateMapping=False,
                                   transform='@TransformPeriodToDate',
                                   label='Acquire Day')
                                   
    tradeStatus =       Object (   objMapping='LiveTradesOrAll.Status',
                                   choiceListSource=TradeStatusChoices(),
                                   toolTip='Shows the current status in the life of a trade. The possibility to change the trade status is regulated by the priviliges of the user.',
                                   label = 'Status')
    
    trader =            Object (   objMapping='Trades.Trader',
                                   label = 'Trader')
                                   
    price =             Delegate ( attributeMapping='Deals.price',
                                   formatter=StripPriceFormatter,
                                   toolTip='@PriceTooltip',
                                   visible='@IsForwardStrip',
                                   validateMapping=False)

    uti =               Delegate ( attributeMapping='Deals.uti',
                                   visible='@IsForwardStrip',
                                   label='UTI',
                                   validateMapping=False)
    
    totalQuantity =     Object (   objMapping='TotalQuantity',
                                   label='Total Qty',
                                   toolTip='@TotalQuantityTooltip',
                                   visible='@IsForwardStrip',
                                   editable=False)
                                   
    premium =           Float(     objMapping='TradePremium',
                                   label='Premium',
                                   visible='@IsOptionStrip')
    
    payments =          PaymentsDialog( trade ='LeadTrade',
                                        visible='@ShowPayments',
                                        enabled='@PackageContainsTrades')
    
    tradePayments =     PaymentsDialog( trade ='SelectedTrade',
                                        visible='@ShowTradePayments',
                                        enabled='@HasSelectedTrade' )
    
    remove =            Action(     label='Remove',
                                    action='@RemoveSelected',
                                    visible='@ShowTradePayments',
                                    enabled='@HasSelectedAndMoreThanOneDeal')
    
    
    text1 =             Object(    label='Void Reason 1',
                                   objMapping='VoidedTradesOrLead.Text1',
                                   visible='@IsStatusVoid',
                                   mandatory='@IsStatusVoid')

    text2 =             Object(    label='Void Reason 2',
                                   objMapping='VoidedTradesOrLead.Text2',
                                   visible='@IsStatusVoid')

    # B2B parameters
    b2bParams = Object(objMapping = 'B2BTradeParams')

    b2bEnabled =        Delegate ( label='B2B Cover',
                                   attributeMapping='Deals.b2bEnabled',
                                   toolTip='If selected back to back sales cover is used',
                                   visible='@IsShowModeDetailOrIsB2B')

    b2bMargin =         Delegate ( attributeMapping='Deals.b2bMargin',
                                   formatter=StripPriceFormatter,
                                   enabled='@IsB2B',
                                   toolTip='@b2BMarginTooltip',
                                   visible='@IsShowModeDetailOrIsB2B',
                                   validateMapping=False )

    b2bPrice =          Delegate ( attributeMapping='Deals.b2bPrice',
                                   formatter=StripPriceFormatter,
                                   visible='@DealIsVisibleAndIsForward',
                                   toolTip='@b2BPriceTooltip',
                                   validateMapping=False )

    b2bPrf =            Delegate ( label='Trader Portfolio',
                                   attributeMapping='Deals.b2bPrf',
                                   choiceListSource='@ChoicesCallback',
                                   toolTip="The portfolio in which the trader's internal trades are booked",
                                   onChanged = '@PackageChanged',
                                   visible='@DealIsVisible'  )

    b2bAcq =            Delegate ( label='Trader Acquirer',
                                   attributeMapping='Deals.b2bAcq',
                                   choiceListSource='@ChoicesCallback',
                                   onChanged = '@PackageChanged',
                                   toolTip='The internal counterpart with which the internal, mirrored, trades are booked',
                                   visible='@DealIsVisible'  )
            
    yourRef =           Object (   objMapping='Trades.YourRef',
                                   label='Cpty Ref')
    
    #Option Fields - onyl applicable for option strips
    contractsPerPeriod = Object(objMapping=InstrumentPart('ContractsPerPeriod'),
                                label='Options/Period',
                                choiceListSource=list(range(1,6)),
                                onChanged='@ForceGenerateStripCB',
                                visible='@IsOptionStrip')

    optionData1 =        CommodityStripOptionData(1)
    optionData2 =        CommodityStripOptionData(2)
    optionData3 =        CommodityStripOptionData(3)
    optionData4 =        CommodityStripOptionData(4)
    optionData5 =        CommodityStripOptionData(5)
    
    exerciseType =      Delegate(attributeMapping='Deals.exerciseType',
                                 domain='enum(ExerciseType)',
                                 choiceListSource='@ChoicesCallback',
                                 visible='@VisibleIfDelagatesHaveAttribute')
                                 
    settlementType =    Delegate(attributeMapping='Deals.settlementType',
                                 domain='enum(settlementTypeShortName)',
                                 choiceListSource='@ChoicesCallback',
                                 label='Settlement Type',
                                 defaultValue='Cash',
                                 visible='@VisibleIfDelagatesHaveAttribute')

    payType =           Delegate(attributeMapping='Deals.payType',
                                 domain='enum(PayType)',
                                 label='',
                                 choiceListSource='@ChoicesCallback',
                                 visible='@VisibleIfDelagatesHaveAttribute')
                                 
    spotDaysOffset =    Delegate(attributeMapping='Deals.spotDaysOffset',
                                 domain='int',
                                 editable='@IsPayTypeSpot',
                                 onChanged='@UpdateValueDate',
                                 visible='@VisibleIfDelagatesHaveAttribute')

    config =            Action ( action='@GetConfig', 
                                 silent=True)

    autoGenerate =      Action ( action='@AutoGenerate',
                                 label="Generate",
                                 visible='@IsNotAutoGenerate',
                                 toolTip='After activating this button, the strip will be generated in real time')
    
    _autoGenerate =     Bool(   )

    reEvaluateObjectMappings =  Action( action = '@ReEvaluateObjectMappings')
    
    # Action used by unittests to ensure that deal package field quantity is updating
    # correctly when amending single deal quantity
    updateDealQuantity =       Action (action='@UpdateDealQuantity')
    
    def UpdateDealQuantity(self, attributeName, dealIndex, newQuantity):
        try:
            self.Deals().At(dealIndex).SetAttribute('quantity_value', newQuantity)
        except:
            print ('Failed to update quantity of deal at index %i' % dealIndex)
    
    @ReturnDomainDecorator('FDealPackageCollection')
    def Deals(self, value='*READING*', *args):
        return self.PreviousDeals() if self._previousNonFailingStrip else self.ActualDeals()
        
    def Trades(self):
        if self.DealPackage().Trades().IsEmpty() and self._previousNonFailingStrip:
            return self._previousNonFailingStrip.Trades() 
        else:
            return self.DealPackage().Trades()
        
    def Instruments(self):
        if self.DealPackage().Instruments().IsEmpty() and self._previousNonFailingStrip:
            return self._previousNonFailingStrip.Instruments() 
        else:
            return self.DealPackage().Instruments()

    def B2BTradeParams(self):
        return [self.B2BTradeParamsAt(key) for key in self.DealPackage().TradeKeys()]
    
    @ReturnDomainDecorator('FDealPackageCollection')
    def ActualDeals(self, value='*READING*', *args):
        return self.DealsFromPackage(value, self.DealPackage())
        
    def SetTradeCurrency(self, *args):
        self.tradeCurrencyRedec = self.currency

    @ReturnDomainDecorator('FDealPackageCollection')
    def PreviousDeals(self, value='*READING*', *args):
        return self.DealsFromPackage(value, self._previousNonFailingStrip)

    def DealsFromPackage(self, value, package):
        if value == '*READING*':
            def WrapBlock(tradeLink, deal, aspect):
                with NoChange(tradeLink.DealPackage().InstrumentPackage()):
                    if aspect == acm.FSymbol('insert'):
                        dealDefinition = StripDealTypeMapping().get(self._stripType + ('Option' if self.IsOptionStrip() and not self._stripType.endswith('Option') else ''))
                        return acm.Deal.Wrap(tradeLink.Trade(), dealDefinition)
                    if aspect == acm.FSymbol('remove'):
                        deal.Dismantle()
            collection = package.WrappedCollectionAt('deals')
            if not collection:
            	collection = package.WrapCollectionAt('deals', package.TradeLinks(), WrapBlock)
            return collection
    
    def StripToUse(self):
        stripToUse = self._previousNonFailingStrip if self._previousNonFailingStrip else self.DealPackage()
        return stripToUse
    
    def PackageContainsTrades(self, *args):
        return False if self.DealPackage().Trades().IsEmpty() else True
    
    def Trades(self):
        return self.StripToUse().Trades()
        
    def Instruments(self):
        return self.StripToUse().Instruments()

    def RedecoratedTrades(self):
        redecoratedTrades = []
        for trade in self.Trades():
            redecoratedTrades.append(acm.FBusinessLogicDecorator.WrapObject(trade.DecoratedObject(), acm.FBusinessLogicGUIDefault()))
        return redecoratedTrades
        
    def DealsPerMonth(self, stripToUse=None):
        deals = {}
        components = self.Deals()
        if stripToUse and stripToUse != self.DealPackage():
            components = stripToUse.GetAttribute('stripComponents')
        if components:
            for deal in components:
                month = GetMonth(deal.GetAttribute('endDate'))
                deals.setdefault(month, []).append(deal)
        return deals
            
    def SelectedDeal(self, attrName=None, selectedDeal='*Reading*'):
        if selectedDeal != '*Reading*':
            self._selectedDeal = selectedDeal
        return self._selectedDeal or []
    
    def SelectedTrade(self):
        return self._selectedDeal.Trades().First() if self._selectedDeal else []
    
    def HasSelectedTrade(self, *args):
        return bool(self.SelectedTrade())
    
    def HasSelectedAndMoreThanOneDeal(self, *args):
        return self.HasSelectedTrade() and len(self.Deals()) > 1
    
    def SelectedDealLayout(self, attrName):
        return self.SelectedDeal(attrName).GetAttribute('customPanes')

    def OnInit(self):
        self.uniqueKey = 0
        for trade in self.DealPackage().AllOpeningTrades():
            self._stripType = GetStripTypeFromInstruments([trade.Instrument()])
            if self._stripType.endswith('Option') and not self._stripType in []:
                self._stripType = self._stripType.replace('Option', '')
            break
        else:
            self._stripType = DefaultStripType()

        self._editEnabled = False
        self._config = None
        self._selectedDeal = None
        self._choiceListSources = {}
        self._choiceListPopulators = {}
        self._instrumentsUpdated = False
        self._startDate = None
        self._endDate = None
        self._generateStrip = None
        self._structureType = 'Strip'
        self._expiryType = 'Standard'
        self._instrumentGroup = None
        self._contractsPerPeriod = 0
        self._previousNonFailingStrip = None
        self._updatedAttributes = []
        self._useCurrentFuture = False
        self._currentFutures = acm.FDictionary()
        
        self.RegisterCallbackOnAttributeChanged(self.UpdateConfig)
        self.RegisterCallbackOnAttributeChanged(self.RegisterUpdatedAttribute)
    
    def AssemblePackage(self, *args):
        dealDefinition = StripDealTypeMapping().get(self._stripType)
        customInsDef =  acm.DealCapturing().CustomInstrumentDefinition(dealDefinition)
        trade = acm.DealCapturing().CreateNewCustomTrade(customInsDef.Name())
        self.DealPackage().AddTrade(trade, self._UniqueInstrumentKey())
    
    def GetInstrumentGroup(self, instrument):
        if instrument and self.GetAttributeMetaData('instrumentGroup', 'visible')():
            for group in self.GetAttributeMetaData('instrumentGroup', 'choiceListSource')().GetChoiceListSource():
                if group and instrument.Originator() in group.Instruments():
                    return group

    def AutoGenerate(self, attrName, value='*Reading*'):
        self._autoGenerate = True

    def OnNew(self):
        insPkgInfant = self.DealPackage().InstrumentPackage().IsInfant()
        dealPkgInfant = self.DealPackage().IsInfant()
        self.pageGroup = PageGroup(self)
        if insPkgInfant:
            self._autoGenerate = GetDefaultAutoGenerate()
            self._editEnabled = True
            self._generateStrip = True
            self.otc = True
            if self.underlying:
                self.SetDefaultQuotation('underlying', None, self.underlying)
                self.SetAttribute('currency', self.underlying.Currency(), True)
        elif dealPkgInfant:
            self._generateStrip = False
            self._autoGenerate = True
            self._editEnabled = self.InstrumentPackageHasNoInfantDealPackage()
        self.SetDefaultValues()
        self.TriggerChoiceListUpdate(silent=True)
        if not insPkgInfant:
            self.ReadValuesFromInstrument()
            self.SetCurrentFutures(None)
        self.instrumentGroup = self.GetInstrumentGroup(self.baseUnderlying)
        self.expiryType = GetExpiryTypeFromInstruments(self.DealPackage().Instruments())
        self.UpdateConfig()
        if insPkgInfant:
            self._SetDefaultValuesOnChange()
            self.GenerateStrip(startDate = self.StartDate(), 
                               endDate = self.EndDate())
        if dealPkgInfant:
            self.SetTradeCurrency()
        self.TriggerChoiceListUpdate(silent=True)
        self.ChoiceListsDirty(False)
        
    def SetDefaultValues(self):
        if self.DealPackage().InstrumentPackage().IsInfant():
            defaultValues = InstrumentPackageDefaultValues(self)
            for attributeName in defaultValues:
                self.SetAttribute(attributeName, defaultValues[attributeName])
        if self.DealPackage().IsInfant():
            defaultValues = DealPackageDefaultValues(self)
            for attributeName in defaultValues:
                self.SetAttribute(attributeName, defaultValues[attributeName])
    
    def GetConfig(self, *args):
        if not self._config:
            self.UpdateConfig()
        return self._config
    
    def UpdateConfig(self, *args):
        self._config = GetConfig(self)

    def PackageChanged(self, attrName, *rest):
        self.DealPackage().Changed()
    
    def RegisterUpdatedAttribute(self, attrName, *args):
        if not attrName in self._updatedAttributes:
            self._updatedAttributes.append(attrName)
    
    def ChoiceListsDirty(self, value=None):
        d = self.Deals().First()
        if value is not None:
            d.SetAttribute('choiceListsDirty', value)
        else:
            return d.GetAttribute('choiceListsDirty')
    
    def LiveTradesOrAll(self):
        return LiveTradesOrAll(self)
    
    def IsStatusVoid(self, *args):
        return self.LeadTrade().Status() == 'Void' if self.LeadTrade() else False

    def VoidedTradesOrLead(self):
        voidedTradesOrLead = acm.FArray()
        for t in self.Trades():
            if t.Status() == 'Void':
                voidedTradesOrLead.Add(t)
        if not voidedTradesOrLead:
            voidedTradesOrLead.Add(self.LeadTrade())
        return voidedTradesOrLead
    
    def SetChoiceListsDirty(self, *args):
        self.ChoiceListsDirty(True)
    
    def _SetDefaultValuesOnChange(self):
        if self._updatedAttributes:
            try:
                SetDefaultValuesOnChange(self, self._updatedAttributes)
            except Exception as e:
                self.errorState = 'SetDefaultValuesOnChange failed. %s'%str(e)
            self._updatedAttributes = []

    def ValidateEndDateAndUnderlying(self):
        if self.underlying and self.underlying.InsType() == 'Future/Forward' and not self.underlying.Generic():
            if acm.Time.DateDifference(self.underlying.ExpiryDate(), self._endDate) < 0:
                raise DealPackageUserException('End date cannot be after the expiry of the reference instrument')

    def Refresh(self):
        try:
            errorBefore = self.errorState
            self.errorState = ''
            if not self._editEnabled and self.InstrumentPackage().IsInfant():
                self._editEnabled = True
            self.ValidateEndDateAndUnderlying()
            if self._editEnabled and not self._registeringAllObjMappingsOnNew:
                if self.ChoiceListsDirty():
                    self.TriggerChoiceListUpdate()
                    self.ChoiceListsDirty(False)
                self._SetDefaultValuesOnChange()
                updateDelegations = False
                if self._autoGenerate:
                    if self._generateStrip:
                        self.GenerateStrip(startDate = self.StartDate(), 
                                           endDate = self.EndDate())
                        self.TriggerChoiceListUpdate(silent=True)
                        updateDelegations = True
                    for d in self.Deals():
                        updateDelegations |= d.Refresh()
                if updateDelegations:
                    self.UpdateParentDelegateTraits()
                if self._instrumentsUpdated:
                    self._instrumentsUpdated = False
                    if self._autoGenerate:
                        OnInstrumentsUpdated(self.DealPackage(), None)
                        self.UpdateParentDelegateTraits()
                if self._previousNonFailingStrip and not self.errorState:
                    self.errorState = errorBefore
        except Exception as e:
            self.errorState = str(e)

    def UpdateParentDelegateTraits(self):
        self._UpdateDelegations() # Reset metadata on delegations
        self.StripToUse().GetAttribute('updateParentDelegateTraits')()
                
    def SuggestName(self): 
        name = ''
        try:
            name = SuggestInstrumentPackageName(self.StripToUse())
        except:
            pass
        return name

    def _CopyB2BFields(self, copyTo, copyFrom):
        fieldsToCopy = ['b2bEnabled', 'b2bMargin', 'b2bPrice', 'b2bPrf', 'b2bAcq']
        for field in fieldsToCopy:
            copyTo.SetAttribute(field, copyFrom.GetAttribute(field))

    def CopyOriginalB2BFields(self, originalDealPackage):
        for nbr, deal in enumerate(originalDealPackage.GetAttribute('stripComponents')):
            self._CopyB2BFields(self.stripComponents.At(nbr), deal)

    def _CopyB2BFieldsToParameter(self, b2bParams, deal):
        b2bParams.SalesCoverEnabled(deal.GetAttribute('b2bEnabled'))
        b2bParams.SalesMargin(deal.GetAttribute('b2bMargin'))
        b2bParams.TraderPrice(deal.GetAttribute('b2bPrice'))
        b2bParams.TraderPortfolio(deal.GetAttribute('b2bPrf'))
        b2bParams.TraderAcquirer(deal.GetAttribute('b2bAcq'))

    def CopyB2BFieldsToStripParameters(self):
        for nbr, b2bParams in enumerate(self.b2bParams):
            self._CopyB2BFieldsToParameter(b2bParams, self.stripComponents.At(nbr))
    
    def OnOpen(self):
        self.pageGroup = PageGroup(self)
        self.TriggerChoiceListUpdate(silent=True)
        self.ReadValuesFromInstrument()
        self.SetCurrentFutures(None)
        self._generateStrip = False
        self._autoGenerate = True
    
    def OnCopy(self, originalDealPackage, aspect):
        self.TriggerChoiceListUpdate(silent=True)
        self.CopyOriginalB2BFields(originalDealPackage)
        self.ReadValuesFromInstrument()
        self._generateStrip = False

    def ReEvaluateObjectMappings(self, *rest):
        # Empty action to re-evaluate object mappings
        pass

    def ReadValuesFromInstrument(self):
        self.pageGroup = PageGroup(self)
        self.SetAttribute('instrumentGroup', self.GetInstrumentGroup(self.baseUnderlying), True)
        self.SetAttribute('structureType', GetStructureTypeFromInstruments(self.DealPackage().Instruments()), True)
        self.UpdateChoices('expiryType', silent=True)
        self.SetAttribute('expiryType', GetExpiryTypeFromInstruments(self.DealPackage().Instruments()), True)
        self.SetAttribute('useCurrentFuture', GetIsCurrentFutureFromInstruments(self.DealPackage().Instruments()), True)
        self.GetAttribute('reEvaluateObjectMappings')()

    def OnSave(self, config):
        if not self._autoGenerate:
            raise DealPackageUserException('Cannot save without generating first.')
        self.CopyB2BFieldsToStripParameters()
        OnSave(self, config)

    # ###############################
    # Validation of deal package
    # ###############################

    def ValidateIndividualOptionContract(self, contractNbr, exceptionAccumulator):
        for nbr in range(1, contractNbr):
            isEqual = True
            for attribute in ['optionType', 'strikePrice']:
                if self.GetAttribute('optionData%i_%s' % (contractNbr, attribute)) != self.GetAttribute('optionData%i_%s' % (nbr, attribute)):
                    isEqual = False
            if isEqual:
                exceptionAccumulator('Option contracts %i and %i are identical' % (nbr, contractNbr))

    def ValidateContractsInPeriod(self, exceptionAccumulator):
        if self.isOptionStrip and self.contractsPerPeriod > 1:
            for nbr in range(2, self.contractsPerPeriod + 1):
                self.ValidateIndividualOptionContract(nbr, exceptionAccumulator)

    def ValidateErrorState(self, exceptionAccumulator):
        if self.errorState != '':
            exceptionAccumulator(self.errorState)
    
    def IsValid(self, exceptionAccumulator, aspect):
        self.ValidateErrorState(exceptionAccumulator)
        self.ValidateContractsInPeriod(exceptionAccumulator)
        IsValid(self, exceptionAccumulator, aspect)
                
    def AttributeOverrides(self, overrideAccumulator):
        CustomAttributeOverrides(self, overrideAccumulator)
        overrideDict =      {'stripDates_startDate': dict(label='@DateLabel',
                                                          enabled = '@StartDateIsVisible',
                                                          toolTip = "Start and end period",
                                                          onChanged = "@SetCurrentFutures"),
                             'stripDates_endDate':   dict(label='',
                                                          onChanged = "@SetCurrentFutures")}

        for attribute in LockedInstrumentPartAttributes:
            attributeDict = overrideDict.get(attribute, {})
            attributeDict['editable']='@InstrumentPartEditable'
            overrideDict[attribute] = attributeDict
        overrideAccumulator(overrideDict)

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_CommodityStrip')
        
    def LeadTrade(self):        
        if not self.Trades():
            return []
        leadTrade = self.Trades().First()
        for trade in self.Trades():
            ins = trade.Instrument()
            if ins.ExpiryDate() > leadTrade.Instrument().ExpiryDate():
                leadTrade = trade
        return leadTrade

    def IsShowModeInstrumentDetail(self, *args):    
        return self.IsShowModeDetail()
        
    def IsShowModeTradeDetail(self, *args):
        return self.IsShowModeDetail2()

    def TriggerChoiceListUpdate(self, silent=False):
        for clAttribute in self.GetAttributes():
            if hasattr(self, clAttribute):
                clSourceMetaData = self.GetAttributeMetaData(clAttribute, 'choiceListSource')
                if not clSourceMetaData.IsDefault() and clSourceMetaData.Definition() == '@ChoicesCallback':
                    try:
                        self.UpdateChoices(clAttribute, silent)
                    except Exception as e:
                        print ('Failed to update choice list, ', clAttribute, str(e))

    # Attribute callbacks
    def SetUnderlying(self, attrName, oldValue, newValue, *rest):
        self.underlying = self.baseUnderlying

    def UpdateValueDate(self, attrName, *rest):
        for trade in self.Trades():
            trade.ValueDay = trade.SpotDate()

    def ExpiryTypeToolTip(self, attrName, *rest):
        if self.IsAsian(attrName):
            return "Standard - monthly periods with daily fixings from first- to last of month\nCustom - ability to specify start date of first period and end date of end period. Same as Standard for periods in between\nCustom Settlement - ability to specify other rolling base date than first day of month. "
        else:
            return "Standard - standard expiries from start to end month (inclusive)\nCustom - ability to specify a custom expiry for the end period"

    def ValueDayTooltip(self, attrName, *rest):
        if self.isOptionStrip:
            return 'Day when premium for this trade is to be paid'
        else:
            return ''

    def PayDayOffsetTooltip(self, attrName, *rest):
        if self.stripType == 'Bullet':
            return 'Offset from expiry date to date of resulting payment'
        else:
            return 'Offset from end of period to date of resulting payment'

    def StripTypeTooltip(self, attrName, *rest):
        if self.isOptionStrip:
            return "Bullet - payoff is based on just one fixing price"
        else:
            return "Asian - payoff depends on average of observed prices\nBullet - payoff is based on just one fixing price"

    def TotalQuantityTooltip(self, attrName, *rest):
        return "Total number of %s for entire strip" % self.quotation.Name() if self.quotation else 'units in selected quotation'

    def QuantityTooltip(self, attrName, *rest):
        return 'Contracts per period. If individual components have different quantities, this field will be empty.'

    def b2BMarginTooltip(self, attrName, *rest):
        return 'Determines how much of the Trader Price that consists of sales margin (spread)'
    
    def b2BPriceTooltip(self, attrName, *rest):
        return 'The internal price between the sales person and the trader'

    def PriceTooltip(self, attrName, *rest):
        return 'Price for each strip component. If individual components have different prices, this field will be empty.'

    def IsNotOne(self, attrName):
        return abs(self.GetAttribute(attrName) - 1) > 1.0e-9

    def UseCurrentFutureAvailable(self, attrName, *rest):
        return (CommodityCanUseCurrentFuture(self.baseUnderlying) and 
                self.IsBullet(attrName) and 
                self.structureType == 'Strip')

    def UntoggleUseCurrentFutureIfEmpty(self, attrName, *rest):
        if len(self.currentFutures) <= 1:
            self.useCurrentFuture = False
    
    def SetCurrentFutures(self, attrName, *rest):
        allCurrentFutures = acm.FDictionary()
        if self.UseCurrentFutureAvailable(attrName):
            allCurrentFutures = GetCurrentFutures(self.DealPackage())
            if len(allCurrentFutures.Keys()) < 2:
                allCurrentFutures = acm.FDictionary()
        self.SetAttribute('currentFutures',allCurrentFutures)

    def ContractSizeInQuotationVisible(self, attrName):
        show = True
        if not SumForContractSize(self.Instruments().First().Quotation().Name()):
            current = self.Instruments().First()
            for i in self.Instruments():
                show &= i.ContractSizeInQuotation() == current.ContractSizeInQuotation()
                current = i
                if not show:
                    break
        return self.IsAutoGenerate(attrName) and show and self.IsNotOne(attrName)

    def IsPayTypeSpot(self, *args):
        return self.payType == 'Spot'

    def DealIsVisible(self, attrName, *rest):
        return self.Deals().First().HasAttribute(attrName) and self.Deals().First().GetAttributeMetaData(attrName, 'visible')()

    def DealIsVisibleAndNotUseCurrentFuture(self, attrName, *rest):
        return self.DealIsVisible(attrName) and not self.useCurrentFuture

    def IsForwardStrip(self, attrName, *rest):
        return not self.isOptionStrip

    def DealIsVisibleAndIsForward(self, attrName, *rest):
        return self.DealIsVisible(attrName) and self.IsForwardStrip(attrName)

    def IsB2B(self, attributeName, *rest):
        return self.b2bEnabled
 
    def IsShowModeDetailOrIsB2B(self, attrName, *rest):
        return self.IsShowModeDetail() or self.IsB2B(attrName)

    def CurrentFuturesAvailable(self, attrName, *rest):
        return bool(self.currentFutures)

    def CurrentFuturesAvailableAndStandardExpiry(self, attrName, *rest):
        return self.CurrentFuturesAvailable(attrName) and self.expiryType == 'Standard'

    def ResetStartEndDateIfNeeded(self, *args):
        if self.errorState == '' and self.IsAutoGenerate():
            self._startDate = self.GetAttributeMetaData('stripDates_startDate', 'transform')(self.FindStartDate())
            self._endDate = self.GetAttributeMetaData('stripDates_endDate', 'transform')(self.FindEndDate())
    
    def ShowGroup(self, attrName, *rest):
        return self.pageGroup and self.pageGroup.SubGroups()
        
    def DateLabel(self, attrName, *rest):
        return 'Period' if self.StartDateIsVisible() else 'Month'
    
    def StartDateIsVisible(self, *rest):
        return self.structureType != 'Single Leg' or self.stripType != 'Bullet'

    def EnableEdit(self, *args):
        self.suggestNameButton()
        self._editEnabled = True

    def InstrumentPackageHasNoInfantDealPackage(self):
        for dp in self.InstrumentPackage().Originator().DealPackages():
            if not dp.Originator().IsInfant():
                return False
        return True

    def InstrumentPartEditable(self, *rest):
        noStoredDealPackage = self.InstrumentPackageHasNoInfantDealPackage()
        return False if not (noStoredDealPackage or self._editEnabled) else NoOverride
    
    def IsEditDisabled(self, *args):
        return not self._editEnabled and self.DealPackage().IsInfant() and not self.InstrumentPackageHasNoInfantDealPackage()
    
    def SuggestNameButton(self, *args):
        if len(self.Deals()):
            self.DealPackage().SuggestName()
    
    def SetDefaultQuotation(self, attrName, oldValue, newValue, *rest):
        self.SetDefaultQuotationAndQuantSizeImpl()

    def SetDefaultQuotationSilent(self, attrName, oldValue, newValue, *rest):
        self.SetDefaultQuotationAndQuantSizeImpl(True)

    def SetCashSettlement(self, attrName, oldValue, newValue, *rest):
        if attrName == 'isOptionStrip' and newValue is True and oldValue is False:
            self.settlementType = 'Cash'

    def ListTradeColumns(self, attrName, *rest):
        tradeCols = [    
                        {'methodChain': 'Instruments.First.Name',          'label': 'Name'},
                        {'methodChain': 'Trades.First.OriginalOrSelf.Oid', 'label': 'Trade'},
                        {'methodChain': 'Trades.First.Quantity',           'label': 'Quantity'},
                        {'methodChain': 'Instruments.First.ContractSizeInQuotation', 'label': 'Contract Size'}
                    ]
        return tradeCols
        
    def ListTradeSortingCallback(self, attrName, columnNbr, value1, formatter, obj):
        return acm.Time.DateTimeToTime(obj.GetAttribute('endDate'))

    def OpenTradeContextMenuItem(self, attrName):
        return ContextMenuCommand(commandPath = 'Open Trade', 
                                  invoke = '@OpenTrade')
                                  
    def OpenTrade(self, attrName):
        if self.SelectedTrade():
            acm.StartApplication('Instrument Definition', self.SelectedTrade().Originator())
            
    def TransformPeriodToDate(self, name, date, *args):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date
        
    def VisibleIfDelagatesHaveAttribute(self, attribute):
        attributeMapping = self.GetAttributeMetaData(attribute, 'attributeMapping')()
        callBackName, attr = attributeMapping.split('.', 1)
        for deal in getattr(self, callBackName)():
            if deal.HasAttribute(attr):
                return deal.GetAttributeMetaData(attr, 'visible')()
        return False
        
    def ImportStripComponents(self, *args):
        clipboard = Clipboard(self.DealPackage())
        clipboard.ClipboardToDp()
        
    def ExportStripComponents(self, *args):
        clipboard = Clipboard(self.DealPackage())
        clipboard.DpToClipboard()

    # Choice list sources

    def ChoicesCallback(self, attrName, *rest):
        clSource = self._choiceListSources.setdefault(attrName, DealPackageChoiceListSource())
        if attrName not in self._choiceListPopulators:
            self._choiceListPopulators[attrName] = acm.FIndexedPopulator(clSource._source)
        populator = self._choiceListPopulators[attrName]
        return populator
    
    def ListsEqual(self, a, b):
        return len(a) == len(b) and list(a) == list(b)
    
    def UpdateChoices(self, attrName, silent=False):
        clSource = self._choiceListSources.setdefault(attrName, DealPackageChoiceListSource())
        allNewItems = ChoiceListPopulator(self, attrName)
        if allNewItems is None:
            clSource.Clear()
        else:
            if not self.ListsEqual(clSource._source, allNewItems):
                clSource.Clear()
                clSource.AddAll(allNewItems)
            obj = self.GetAttribute(attrName)
            for item in allNewItems:
                if self.IsEqual(obj, item):
                    break
            else:
                if self.InstrumentPackage().IsInfant():
                    self.SetAttribute(attrName, allNewItems[0] if allNewItems else None, silent)
                else:
                    clSource.Add(obj)
                    
        if attrName not in self._choiceListPopulators:
            self._choiceListPopulators[attrName] = acm.FIndexedPopulator(clSource._source)
            
    
    def IsEqual(self, obj1, obj2):
        return (obj1 == obj2 
            or (hasattr(obj1, 'Originator') and hasattr(obj2, 'Originator') and obj1.Originator() == obj2.Originator())
            or (isinstance(obj1, basestring) and not isinstance(obj2, basestring) and hasattr(obj2, 'Name') and obj1 == obj2.Name())
            or (isinstance(obj2, basestring) and not isinstance(obj1, basestring) and hasattr(obj1, 'Name') and obj2 == obj1.Name()))
            
            
    #
    # Labels
    #
    
    def NominalInQuotationFormatted(self, *args):
        if self.quantity_value:
            formatter = acm.Get('formats/InstrumentDefinitionQuantity')
            return formatter.Format(self.nominalInQuotation_value)
        else:
            return '1'
    
    def QuotationFormatted(self, *args):
        if self.quantity_value:
            return self.quotation
        else:
            return 'Per Deal Package'
    
    # 
    # ObjectMappings
    #
    
    @ReturnDomainDecorator('datetime')
    def StartDate(self, value = 'NoValue'): 
        if value == 'NoValue':
            if self._startDate == None:
                self._startDate = self.FindStartDate()
            return self._startDate
        else:
            if acm.Time.DateDifference(value, self.StartDate()) != 0:
                self._startDate = value
                self.GenerateStripCB()
                
    @ReturnDomainDecorator('datetime')
    def EndDate(self, value = 'NoValue'):
        if value == 'NoValue':
            if self._endDate == None:
                self._endDate = self.FindEndDate()
            return self._endDate
        else:
            if acm.Time.DateDifference(value, self.EndDate()) != 0:
                self._endDate = value
                self.GenerateStripCB()
                
    @ReturnDomainDecorator('string')
    def StripType(self, value = 'NoValue', **kwargs):
        if value == 'NoValue':
            return self._stripType
        else:
            isOptionStrip = kwargs.get('isOptionStrip', self.isOptionStrip)
            suffix = 'Option' if isOptionStrip and not self._stripType.endswith('Option') and not value.endswith('Option') else ''
            if self._stripType != value or (suffix == 'Option') != self.isOptionStrip:
                self._stripType = value
                self.UpdateDeals(value + suffix)
            else:
                self.SetChoiceListsDirty()
            
    @ReturnDomainDecorator('string')
    def StructureType(self, value = 'NoValue', **kwargs):
        if value == 'NoValue':
            return self._structureType
        else:
            self._structureType = value
            
    def StructureTypeDefault(self, *args):    
        if len(self.Deals()) == 1:
            dealAttr = self.Deals().First().GetAttribute
            if acm.Time.DateDifference(dealAttr('endDate'), acm.Time.DateAdjustPeriod(dealAttr('startDate'), '1M')) >= 0:
                return 'Single Leg'
        return 'Strip'
            
    @ReturnDomainDecorator('string')
    def ExpiryType(self, value = 'NoValue', **kwargs):
        if value == 'NoValue':
            return self._expiryType
        else:
            self._expiryType = value
            
    @ReturnDomainDecorator('FPhysInstrGroup')
    def InstrumentGroup(self, value = 'NoValue', **kwargs):
        if value == 'NoValue':
            return self._instrumentGroup
        else:
            self._instrumentGroup = value

    @ReturnDomainDecorator('bool')
    def UseCurrentFuture(self, value = 'NoValue'):
        if value == 'NoValue':
            return self._useCurrentFuture
        else:
            self._useCurrentFuture = value
            for deal in self.Deals():
                deal.SetAttribute('useCurrentFuture', value)
                                   
    @ReturnDomainDecorator('FDictionary')
    def CurrentFutures(self, value = 'NoValue'):
        if value == 'NoValue':
            return self._currentFutures
        else:
            self._currentFutures = value

    def UpdateDeals(self, dealType):
        self.SelectedDeal(attrName=None, selectedDeal=None)
        for i, deal in enumerate(self.Deals()):
            newDeal = self.CopyDealToNewDeal(deal, dealType)
            assert newDeal, 'Failed to update deals'
            oldDeal = self.Deals().At(i)
            self.Deals().AtPut(i, newDeal)
            oldDeal.Dismantle()
        if not self.GetAttributeMetaData('contractsPerPeriod', 'visible')():
            self.contractsPerPeriod = 1
        self._UpdateDelegations() # Reset metadata on delegations
        self.SetChoiceListsDirty()

    def IsOptionStrip(self, value = 'NoValue', *rest):
        if isinstance(value, bool):
            if self.InstrumentPackage().IsInfant():
                if not value and self._stripType.endswith('Option'):        
                    self._stripType = self._stripType.replace('Option', '')
                self.StripType(self._stripType, isOptionStrip = value)
        else:
            instr = self.Instruments().First() if self.Instruments() else None
            return instr.IsKindOf('FOption') if instr else False
                
    @ReturnDomainDecorator('double')
    def TotalQuantity(self, value=None):
        if value is None:
            return sum(deal.GetAttribute('quantity_value') * deal.Instruments().First().ContractSizeInQuotation() for deal in self.Deals())
    
    @ReturnDomainDecorator('int')
    def ContractsPerPeriod(self, value=None):
        if value is None:
            if not self._contractsPerPeriod:
                self._contractsPerPeriod = max(map(len, self.DealsPerMonth().values())) if self.IsOptionStrip() else 1
            return self._contractsPerPeriod
        else:
            self._contractsPerPeriod = int(value)
    
    def TradePremium(self):
        return sum(deal.Trades().First().Premium() for deal in self.Deals())

    @ReturnDomainDecorator('double')
    def ContractSizeInQuotation(self, *args):
        if self.Instruments():
            if SumForContractSize(self.Instruments().First().Quotation().Name()):
                return sum(i.ContractSizeInQuotation() for i in self.Instruments())
            else:
                return self.LeadTrade().Instrument().ContractSizeInQuotation()

    ''' Used in trade action close '''

    aggregateNominal = Object( objMapping = 'AggregateNominal',
                               domain = 'float')

    def IsLiveTrade(self, trade):
        return not trade.Instrument().IsExpired()
        
    def _SetTradeNominals(self, value):
        if self.AggregateNominal() and value:
            factor = value / abs(self.AggregateNominal())
            for trade in self.Trades():
                if self.IsLiveTrade(trade):
                    trade.Nominal(abs(trade.Nominal()) * factor)  
                  
    def AggregateNominal(self, value = "Reading", *args):
        if value == "Reading":
            return sum( trd.Nominal() for trd in self.LiveTrades() )
        else:
            self._SetTradeNominals(value)

    # Util

    def SetLastComponentExpiry(self, component, endDate):
        if self.expiryType == 'Custom':
            # Set the date as a period to trigger transform logic adding a default time stamp
            component.SetAttribute('endDateIsCustom', True)
            endDateAsPeriod = '%iD' % acm.Time.DateDifference(endDate, acm.Time.DateToday())
            component.SetAttribute('customExpiry', endDateAsPeriod)
        # Make sure to capture the transformed forward expiry as strip end date
        self._endDate = component.GetAttribute('endDate')
        
    def SetUnderlyingKeepingQuotation(self, deal, und):
        quotation = deal.GetAttribute('quotation')
        deal.SetAttribute('underlying', und)
        deal.SetAttribute('quotation', quotation)

    def SetDefaultQuotationAndQuantSizeImpl(self, setSilent = False):
        if self.underlying and self.quotation != self.underlying.Quotation():
            self.SetAttribute('quotation', self.underlying.Quotation(), setSilent)
            for i in self.Instruments():
                i.ContractSizeInQuotation(1.0)

    def IsAsian(self, attrName, *rest):
        return self.stripType == 'Asian'

    def IsBullet(self, attrName, *rest):
        return self.stripType in ('Bullet', 'BulletOption')

    def FindStartDate(self):
        startDate = None
        for deal in self.Deals():
            componentStartDate = deal.GetAttribute('startDate')
            if not startDate or acm.Time.DateDifference(componentStartDate, startDate) < 0:
                startDate = componentStartDate
        return startDate
    
    def FindEndDate(self):
        endDate = None
        for deal in self.Deals():
            componentEndDate = deal.GetAttribute('endDate')
            if not endDate or acm.Time.DateDifference(componentEndDate, endDate) > 0:
                endDate = componentEndDate
        return endDate

    # --------------------------------------
    # Working with components
    # --------------------------------------

    def CreateNewDeal(self, type):
        dealDefinition = StripDealTypeMapping().get(type)
        return acm.Deal.New(dealDefinition)
        
    def CopyDealToNewDeal(self, compDeal, newType):
        dealDefinition = StripDealTypeMapping().get(newType)
        return acm.Deal.Wrap(compDeal, dealDefinition)
    
    def AddDeal(self, newDeal):
        trade = newDeal.Trades().First()
        # Must remove trade from Deal to be allowed to add it to a deal package
        newDeal.RemoveTrade(trade)
        newDeal.Dismantle()
        if not self.DealPackage().IncludesTrade(trade):
            self.DealPackage().AddTrade(trade, self._UniqueInstrumentKey())

    def Remove(self, deal):
        trade = deal.Trades().First().Trade()
        instrument = trade.Instrument()
        tradesInIns = [t for t in self.DealPackage().Trades() if t.Trade().Instrument().Oid() == instrument.Oid()]
        if len(tradesInIns) > 1:
            self.DealPackage().RemoveTrade(trade)
        else:
            self.DealPackage().RemoveInstrument(instrument)
    
    def RemoveSelected(self, *args):
        if self.HasSelectedAndMoreThanOneDeal():
            self.DealPackage().RemoveInstrument(self.SelectedTrade().Instrument())
            self._startDate = self.FindStartDate()
            self._endDate = self.FindEndDate()
            self._instrumentsUpdated = True

    def _findHighestKey(self):
        highest = 0
        for insKey in self.DealPackage().InstrumentKeys():
            intKey = int(insKey[3:])
            if intKey > highest:
                highest = intKey
        return highest
    
    def _UniqueInstrumentKey(self):
        if self.uniqueKey == 0:
            self.uniqueKey = self._findHighestKey()
        self.uniqueKey += 1
        return 'ins' + str(self.uniqueKey)

    # ---------------------------------
    # Generating the strip
    # ---------------------------------
    def GenerateStripCB(self, attr=None, old=None, new=None, *rest):
        if self._generateStrip != None:
            self._generateStrip = True
        self.SetChoiceListsDirty()
        
    def ForceGenerateStripCB(self, attr=None, old=None, new=None, *rest):
        if self._generateStrip != None:
            self._generateStrip = True
        
        if not self._autoGenerate:
            self.GenerateStrip(startDate = self.StartDate(), 
                               endDate = self.EndDate())     
        self.SetChoiceListsDirty()

    def GenerateIfCurrentFuture(self, attrName, *rest):
        if self.useCurrentFuture is True:
            self.GenerateStripCB()

    def ShouldAdjustEndDate(self, startDate, endDate):
        return (not acm.Time.IsValidDateTime(endDate) or
                acm.Time.DateDifference(endDate, acm.Time.BigDate()) == 0 or
                acm.Time.DateDifference(startDate, endDate) > 0)

    def ShouldAdjustStartDate(self, startDate):
        return  not acm.Time.IsValidDateTime(startDate) or \
                acm.Time.DateDifference(startDate, acm.Time.SmallDate()) == 0 or \
                not self.GetAttributeMetaData('stripDates_startDate', 'visible')()

    def GetCurrentDeals(self, month):
        return [deal for deal in self.Deals() if month == GetMonth(deal.GetAttribute('startDate'))]
        
    def _GenerateStripFromInstruments(self, instruments):
        toRemove = list(self.Deals())
        previous = None
        if not self._previousNonFailingStrip:
            if not instruments:
                self._previousNonFailingStrip = self.DealPackage().Copy()
        if instruments:
            previous = self._previousNonFailingStrip
            self._previousNonFailingStrip = None
        stripToUse = previous if previous else self.DealPackage()
        dealsPerMonth = self.DealsPerMonth(stripToUse)
        templates = []
        for month, deals in dealsPerMonth.iteritems():
            if len(templates) < len(deals):
                templates = deals
        
        dealsPerMonthNew = len(instruments)/self.contractsPerPeriod
        for i, instrument in enumerate(instruments):
            template = templates[min(int(i/dealsPerMonthNew), len(templates)-1)]
            newTrade = CopyTrade(template.Trades().First())
            newTrade.Instrument = instrument
            InitTrade(newTrade)
            self.DealPackage().AddTrade(newTrade, self._UniqueInstrumentKey())
        
        for deal in toRemove:
            self.Remove(deal)
        
        if previous:
            previousTrades = previous.Trades()
            for previousTrade in previousTrades:
                previous.RemoveTrade(previousTrade)
            previous.Dismantle()

    def _GenerateStripDefault(self, startDate, endDate, rollingPeriod):
        endMonth = GetMonth(endDate)
        date = startDate
        nbrOfPeriods = 0
        periodEndDate = self.CalculatePeriodEndDate(date, startDate, rollingPeriod, nbrOfPeriods)
        month = GetMonth(endDate if self.structureType == 'Single Leg' else periodEndDate)
        previousComponents = []
        currentTrades = acm.FSet()

        while month <= endMonth:
            if not self.useCurrentFuture or self.currentFutures.HasKey(month):
                components = self.GetCurrentDeals(month)
                components = components[:self.contractsPerPeriod] + [None] * (self.contractsPerPeriod-len(components))
                for i, component in enumerate(components):
                    if not component:
                        if len(previousComponents) > i:
                            template = previousComponents[i]
                        elif i and components[i-1]:
                            template = components[i-1]
                        else:
                            template = self.Deals().First()
                            
                        newTrade = CopyTrade(template.Trades().First())
                        InitTrade(newTrade)
                        self.DealPackage().AddTrade(newTrade, self._UniqueInstrumentKey())
                        component = self.Deals().Last()
                        self._CopyB2BFields(component,template)
                        components[i:i+1] = [component]
                        component.SetAttribute('useCurrentFuture', self.useCurrentFuture)
                    component.SetAttribute('endDateIsCustom', False)
                    # Current Future, set underlying:
                    if self.useCurrentFuture:
                        self.SetUnderlyingKeepingQuotation(component, self.currentFutures.At(month))
                    self.SetComponentDates(component, date, periodEndDate, startDate, endDate, month, endMonth)
                    # For bullet custom expiry type, set the custom end date
                    if self.stripType == 'Bullet' and month == endMonth:
                        self.SetLastComponentExpiry(component, endDate)
                    currentTrades.Add(component.Trades().First())
                if self.structureType == 'Single Leg':
                    break
                previousComponents = components
            nbrOfPeriods += 1
            date = self.CalculateNextStartDate(startDate, rollingPeriod, nbrOfPeriods)
            periodEndDate = self.CalculatePeriodEndDate(date, startDate, rollingPeriod, nbrOfPeriods)
            month = GetMonth(periodEndDate)

        for deal in list(self.Deals()):
            if not currentTrades.Includes(deal.Trades().First()):
                self.Remove(deal)

    def CalculatePeriodEndDate(self, periodDate, startDate, rollingPeriod, nbrOfPeriods):
        if self.expiryType in ('Standard', 'Custom'):
            return periodDate
        else:
            if self.structureType == 'Single Leg':
                return self.stripDates_endDate
            elif GetMonth(self.stripDates_startDate) == GetMonth(self.stripDates_endDate):
                return LastDayOfMonth(periodDate)
            return acm.Time.DateAddDelta(self.CalculateNextStartDate(startDate, rollingPeriod, nbrOfPeriods + 1), 0, 0, -1)

    def SetComponentDates(self, component, periodDate, periodEndDate, startDate, endDate, month, endMonth):
        if self.expiryType in ('Standard', 'Custom'):
            component.SetAttribute('startDate', ('!%s' % startDate) if periodDate == startDate else periodDate)
            component.SetAttribute('endDate', ('!%s' % endDate) if month == endMonth else periodDate)
        else:
            component.SetAttribute('startDate', '!%s' % periodDate)
            component.SetAttribute('endDate', '!%s' % periodEndDate)

    def CalculatePeriodFromStart(self, rollingPeriod, nbrPeriods):
        return '%i%s' % (int(rollingPeriod[:len(rollingPeriod)-1]) * nbrPeriods, rollingPeriod[len(rollingPeriod)-1:])

    def CalculateNextStartDate(self, startDate, rollingPeriod, nbrOfPeriods):
        return acm.Time.DateAdjustPeriod(startDate, self.CalculatePeriodFromStart(rollingPeriod, nbrOfPeriods))

    def GenerateStrip(self, startDate, endDate, rollingPeriod = '1M'):
        from CommodityStripSearchHook import CustomFindInstruments
        # this will generate a sequence needed for the strip
        if not (acm.Time.IsValidDateTime(startDate) and acm.Time.IsValidDateTime(endDate)):
            return
        # Make sure to only re/create, regenerate the instruments necessary

        if (acm.Time.DateDifference(startDate, acm.Time.SmallDate()) == 0
            and acm.Time.DateDifference(endDate, acm.Time.BigDate()) == 0):
            return

        # If the new start date is after end date or end date is not yet set
        if self.ShouldAdjustEndDate(startDate, endDate):
            endDate = LastDayOfMonth(startDate)

        # Start date is not yet set
        if self.ShouldAdjustStartDate(startDate):
            startDate = acm.Time.FirstDayOfMonth(endDate)
        
        try:
            instruments = CustomFindInstruments(self.DealPackage(), startDate, endDate)
        except Exception as e:
            self.errorState = str(e)
            instruments = []
            
        # Store selected row before re-generating in order to re-set selection after re-generation
        # If not re-set, an error will occur if user double clicks on previously selected row before
        # selecting a row
        if self.SelectedDeal() != []:
            index = self.stripComponents.IndexOf(self.SelectedDeal())
            self.SelectedDeal(attrName=None, selectedDeal=None)
        else:
            index = None
            
        if instruments is not None:
            self._GenerateStripFromInstruments(instruments)
        else:
            self._GenerateStripDefault(startDate, endDate, rollingPeriod)
        
        self._instrumentsUpdated = True
        self._generateStrip = False
        
        # Reset Selected Deal
        if index is not None and len(self.stripComponents) > index:
            self.SelectedDeal(attrName=None, selectedDeal=self.stripComponents[index])
        else:
            self.SelectedDeal(attrName=None, selectedDeal=None)
            
    # ---------------------------------
    # End generate strip
    # ---------------------------------

    def IsAutoGenerate(self, *args):
        return self._autoGenerate

    def IsNotAutoGenerate(self, *args):
        return not self.IsAutoGenerate(*args)

    def ShowPayments(self, *args):
        return self.IsOptionStrip(*args) and self.IsAutoGenerate(*args)
    
    def ShowTradePayments(self, *args):
        return self.IsForwardStrip(*args) and self.IsAutoGenerate(*args)
    

    
''' Start application '''
def StartCommodityStripApplication(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'CommodityStrip')
