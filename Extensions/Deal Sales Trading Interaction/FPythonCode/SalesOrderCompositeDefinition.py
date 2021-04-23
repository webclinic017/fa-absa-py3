import acm
from functools import partial
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageUserException, UXDialogsWrapper
from DealPackageDevKit import CalcVal, Float, Object, Bool, Str, Action, Label, Box, CounterpartyChoices, PortfolioChoices, ReturnDomainDecorator, DealPackageChoiceListSource
from DealPackageUtil import SalesTradingInteraction, SalesTradingInfo
from CompositeAttributesLib import BuySell
from RFQUtils import Direction, Misc, MethodDirection, Open
from RFQUtils import Time, Amount, TradingInterface, Validation
from RFQUtils import PriceAndMarginConversions
from RFQMarketComposite import RFQMarket
from TradeCreationUtil import TradeCreation, TradeCreationUtil

from SalesTradingCustomizations import TickSizeSettings, OrderBookCreation, ButtonLabels, Limits
from SalesTradingCustomizations import PriceAndMarginConversions as ConversionCustomizations
from SalesOrderCustomizations import SalesOrderCustomDefinition

def DoRefreshCallback(pSelf, *args):
    pSelf.DoRefresh()
    
class OrderHandlerProxy(object):
    def __init__(self):
        self._transientValues = acm.FDictionary()
        self._orderHandler = None
        
    def OrderHandler(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._orderHandler
        else:
            self._orderHandler = val
        
    def TransientValue(self, attr, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._transientValues.At(attr)
        else:
            self._transientValues.AtPut(attr, val)

    def OrderHandlerValue(self, attr, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return getattr(self._orderHandler, attr)()
        else:
            setattr(self._orderHandler, attr, val)
    
    def __getattr__(self, attr):
        val = None
        if attr == 'OrderHandler':
            val = self.OrderHandler
        elif self._orderHandler:
            val = partial(self.OrderHandlerValue, attr)
        else:
            val = partial(self.TransientValue, attr)
        return val

class SalesOrderDefinition(CompositeAttributeDefinition):
    def Attributes(self):
        attributes = {}
            
        ''' Top Section '''
        attributes.update({
            'initFromOrderHandler': Action(  action=self.UniqueCallback('@InitFromOrderHandlerAction')),
            
            'insNameLabel': Label(        label=self.UniqueCallback('@InstrumentLabel'),
                                                labelFont=self.UniqueCallback('@Arial14'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                alignment='Center',
                                                width=570),  
    
                                                     
            'insISINLabel': Label(        label=self.UniqueCallback('@TopISINLabel'),
                                                labelFont=self.UniqueCallback('@Arial'),
                                                visible=self.UniqueCallback('@TopISINVisible'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                alignment='Center', 
                                                width=570),
                                                
            'panel': Box(          label='',
                                                vertical=False,
                                                backgroundColor=self.UniqueCallback('@TopPanelColor')),
                                                
            'insPanel': Box(          label='',
                                                vertical=True,
                                                backgroundColor=self.UniqueCallback('@TopPanelColor')),
  
            'typeLabel': Label(        label=self.UniqueCallback('@TopTypeLabel'), 
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                width=190),
                                                
            'clientName': Label(        label=self.UniqueCallback('@TopTypeClientName'), 
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                width=190),
                                                
            'validThrough': Label(        label=self.UniqueCallback('@ValidThroughLabel'), 
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                width=190),
                                                
            'amountLabel': Label(        label=self.UniqueCallback('@TopAmountLabel'),
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                width=190),       
                                 
            'directionLabel': Label(        label=self.UniqueCallback('@TopDirectionLabel'),
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                width=190),   
                                                  
            'priceLabel': Label(        label=self.UniqueCallback('@OrderPriceLabel'),
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                width=190), 
                                                
            'quotationLabel': Label(        label=self.UniqueCallback('@TopQuotationLabel'),
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),      
                                                width=190),  
                                                
            'salesState': Label(        label=self.UniqueCallback('@SalesStateName'), 
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                alignment='Right',
                                                width=190),

            'traderLabel': Label(        label=self.UniqueCallback('@TopTraderLabel'),
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                alignment='Right',
                                                width=190),
                                                
            'market': RFQMarket(    instrumentName=self.UniqueCallback('SalesOrderCalcInstrument')),

            'prices': Label(        label=self.UniqueCallback('@TopPricesLabel'),
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                alignment='Right',
                                                width=190),
                                                  
        })


        ''' Price and limits '''
        attributes.update({
            'customerPrice': Float(        label='Client Price',
                                                formatter=self.UniqueCallback('@PriceFormatter'),
                                                onChanged=self.UniqueCallback('@OnCustomerPriceChanged'),
                                                tick=self.UniqueCallback('@PriceTick'),
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent')),
                                                    
            'salesSpread': Float(        label='Spread',
                                                formatter=self.UniqueCallback('@PriceFormatter'),
                                                onChanged=self.UniqueCallback('@OnSalesSpreadChanged'),
                                                tick=self.UniqueCallback('@PriceTick'),
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent')),
                                                       
            'traderPrice': Float(        label='Trader Price',
                                                formatter=self.UniqueCallback('@PriceFormatter'),
                                                objMapping=self.UniqueCallback('TraderPrice'),
                                                tick=self.UniqueCallback('@PriceTick'),
                                                editable=False,
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent')),
                                                       
            'atMarketPrice': Action(       label='Market',
                                                action=self.UniqueCallback('@AtMarketPriceAction'),
                                                enabled=self.UniqueCallback('@OrderSupportsUnlimited')),
                                                
            'atLimitedPrice': Action(       label='Limited',
                                                action=self.UniqueCallback('@AtLimitedPriceAction'),
                                                enabled=self.UniqueCallback('@OrderSupportsLimited')),
                                                
            'customerPriceType': Action(       label='>',
                                                actionList=self.UniqueCallback('@PriceTypeActionList'),
                                                sizeToFit=True,
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent')),

            'traderPriceType': Action(         label='>',
                                                actionList=self.UniqueCallback('@PriceTypeActionList'),
                                                sizeToFit=True,
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent')),
        })
                                         

        ''' Validity '''
        attributes.update({
            'validityCondition': Object(       label='Validity',
                                                domain='FCapabilityChoice',
                                                objMapping=self.UniqueCallback('ValidityCondition'),
                                                transform=self.UniqueCallback('@TransformValidityCondition'),
                                                choiceListSource=self.UniqueCallback('@ValidityConditionChoices'),
                                                visible=self.UniqueCallback('@InShowModeDetail'),
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent')),
            
            'expirationDateTime': Object(       defaultValue=acm.Time().TodayAt(23, 59, 59, 0, False),
                                                label='',
                                                domain='datetime',
                                                objMapping=self.UniqueCallback('ExpirationDateTime'),
                                                transform=self.UniqueCallback('@TransformExpirationDateTime'),
                                                visible=self.UniqueCallback('@ValidityConditionIsGoodTillCancel'),
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent')),
        })
        
        ''' General '''
        attributes.update({
            'customAttributes'  : SalesOrderCustomDefinition(
                                                instrumentMethod=self.UniqueCallback('SalesOrderInstrument'),
                                                orderHandlerMethod=self.UniqueCallback('SalesOrderHandlerProxy'),
                                                dealPackageMethod=self.UniqueCallback('SalesOrderDealPackage')),
            

            'tradeCreationSetting'  : Object(   label='Trade Flow',
                                                choiceListSource=self.UniqueCallback('@TradeSettingChoices'),
                                                objMapping=self.UniqueCallback('TradeCreationSetting'),
                                                visible=self.UniqueCallback('@TradeSettingVisible'),
                                                enabled=self.UniqueCallback('@TradeSettingEnabled')),
                                                                                                  
            'buySellQuantity'   : Object(       defaultValue='Buy',
                                                label=self.UniqueCallback('@QuantityLabel'),
                                                choiceListSource=self.UniqueCallback('@BuySellChoices'),
                                                objMapping=self.UniqueCallback('BuyOrSell'),
                                                onChanged=self.UniqueCallback('@OnQuantityChanged'),
                                                maxWidth=self.UniqueCallback('@BuySellWidth'),
                                                width=self.UniqueCallback('@BuySellWidth'),
                                                visible=self.UniqueCallback('@QuantityVisible'),
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent'),
                                                editable=self.UniqueCallback('@NotInModifyState')),
            
            'buySellNominal'   : Object(        defaultValue='Buy',
                                                label='Nominal',
                                                choiceListSource=self.UniqueCallback('@BuySellChoices'),
                                                objMapping=self.UniqueCallback('BuyOrSell'),
                                                maxWidth=self.UniqueCallback('@BuySellWidth'),
                                                width=self.UniqueCallback('@BuySellWidth'),
                                                visible=self.UniqueCallback('@NominalVisible'),
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent'),
                                                editable=self.UniqueCallback('@NotInModifyState')),
            
            'buySellNomInQuot' : Object(        defaultValue='Buy',
                                                label='Nom In Quot',
                                                choiceListSource=self.UniqueCallback('@BuySellChoices'),
                                                objMapping=self.UniqueCallback('BuyOrSell'),
                                                maxWidth=self.UniqueCallback('@BuySellWidth'),
                                                width=self.UniqueCallback('@BuySellWidth'),
                                                visible=self.UniqueCallback('@NomInQuotVisible'),
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent'),
                                                editable=self.UniqueCallback('@NotInModifyState')),
                                                
            'quantity'          : Object(       label='',
                                                objMapping=self.UniqueCallback('Quantity'),
                                                onChanged=self.UniqueCallback('@OnQuantityChanged'),
                                                formatter=self.UniqueCallback('@QuantityFormatter'),
                                                tick=self.UniqueCallback('@NominalTick'),
                                                validate=self.UniqueCallback('@ValidateQuantity'),
                                                domain='double',
                                                visible=self.UniqueCallback('@QuantityVisible'),
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent')),
                                                
            'nominal'           : Object(       label='',
                                                objMapping=self.UniqueCallback('Nominal'),
                                                formatter=self.UniqueCallback('@NominalFormatter'),
                                                tick=self.UniqueCallback('@NominalTick'),
                                                validate=self.UniqueCallback('@ValidateQuantity'),
                                                domain='double',
                                                visible=self.UniqueCallback('@NominalVisible'),
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent')),
            
            'nomInQuot'         : Object(       label='',
                                                objMapping=self.UniqueCallback('NomInQuot'),
                                                formatter=self.UniqueCallback('@NominalFormatter'),
                                                tick=self.UniqueCallback('@NominalTick'),
                                                domain='double',
                                                visible=self.UniqueCallback('@NomInQuotVisible'),
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent')),

            'investmentDecider' : Object(       objMapping=self.UniqueCallback('InvestmentDecider'),
                                                onChanged=self.UniqueCallback('@OnInvestmentDeciderChanged')),
                
            'investmentDeciderName' : Str(      label='Inv Decider',
                                                choiceListSource=self.UniqueCallback('@InvestmentDeciderDisplayNameChoices'),
                                                editable=self.UniqueCallback('@NotInModifyState'),
                                                visible=self.UniqueCallback('@InShowModeDetail'),
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent'),
                                                onChanged=self.UniqueCallback('@OnInvestmentDeciderNameChanged')),
                                                
            'trader'            : Object(       label='Trader',
                                                domain=acm.FUser,
                                                objMapping=self.UniqueCallback('Trader'),
                                                choiceListSource=self.UniqueCallback('@UserChoices'),
                                                visible=self.UniqueCallback('@InShowModeDetail'),
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent'),
                                                editable=self.UniqueCallback('@NotInModifyState')),

            'client'            : Object(       label='Client',
                                                domain='FParty',
                                                objMapping=self.UniqueCallback('Client'),
                                                onChanged=self.UniqueCallback('@OnClientChanged'),
                                                choiceListSource=CounterpartyChoices(),
                                                width=30,
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent')),
                                                
            'portfolio'         : Object(       label='Portfolio',
                                                domain='FPhysicalPortfolio',
                                                objMapping=self.UniqueCallback('Portfolio'),
                                                onChanged=self.UniqueCallback('@ResetLimitChecks'),
                                                choiceListSource=PortfolioChoices(),
                                                visible=self.UniqueCallback('@InShowModeDetail'),
                                                width=30,
                                                enabled=self.UniqueCallback('@EnabledIfNotOrderSent')),
            
            'insNominalFactor'  : CalcVal(      calcMapping=self.UniqueCallback('SalesOrderTrade') + ':FTradeSheet:Standard Calculations Instrument Nominal Factor'),
                                                
            'sendOrder'         : Action(       label=self.UniqueCallback('@BuyOrSellLabel'),
                                                enabled=self.UniqueCallback('@SendOrderEnabled'),
                                                visible=self.UniqueCallback('@SendOrderVisible'),
                                                action=self.UniqueCallback('@OnSendOrder'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor')),
            
            'checkLimits'       : Action(       label='Check Limits',
                                                action=self.UniqueCallback('@OnCheckLimits'),
                                                enabled=self.UniqueCallback('@CheckLimitsEnabled'),
                                                visible=self.UniqueCallback('@CheckLimitsVisible')),
                                                                        
                        
            'orderActions'      : Action(       label='>',
                                                sizeToFit=True,
                                                actionList=self.UniqueCallback('@OrderActions')),
            
            'newInsAndTrade'    : Action(       label=self.UniqueCallback('@NewInsAndTradeLabel'),
                                                action=self.UniqueCallback('@OnNewInsAndTrade'),
                                                visible=self.UniqueCallback('@NewInsAndTradeActionVisible')),
                
            'newTrade'          : Action(       label=self.UniqueCallback('@NewTradeLabel'),
                                                action=self.UniqueCallback('@OnNewTrade'),
                                                visible=self.UniqueCallback('@NewTradeActionVisible')),
            
            'newActions'        : Action(       label='New >',
                                                actionList=self.UniqueCallback('@NewActions'),
                                                visible=self.UniqueCallback('@NewOrderValid')),
                                                
            'doneQuantity'      : CalcVal(      label='Done Qty',
                                                valuationDetails=False,
                                                toolTip='The quantity othat has been filled in the market (so far).',
                                                editable=False,
                                                visible=self.UniqueCallback('@DoneVisible'),
                                                calcMapping=self.UniqueCallback('SalesOrderHandlerCalcObj') + ':FOrderSheet:Done Quantity'),

            'donePrice'         : CalcVal(      label='Avg Price',
                                                valuationDetails=False,
                                                toolTip='The average price for the completed (Done) part of the partially filled order.',
                                                editable=False,
                                                visible=self.UniqueCallback('@DoneVisible'),
                                                calcMapping=self.UniqueCallback('SalesOrderHandlerCalcObj') + ':FOrderSheet:Done Price'),

            'modifyOrder'       : Action(       label='Modify Order',
                                                action=self.UniqueCallback('@OnModifyOrder'),
                                                visible=self.UniqueCallback('@ModifyOrderEnabled')),
                                                
            'cancelOrder'       : Action(       label='Cancel Order',
                                                action=self.UniqueCallback('@OnCancelOrder'),
                                                visible=self.UniqueCallback('@CancelOrderVisible')),
                        
            'closeDialog'       : Action(       label='Close',
                                                action=self.UniqueCallback('@OnCloseDialog'),
                                                visible=self.UniqueCallback('@CloseDialogVisible')),
                                                
            'showDetails'       : Action(       label=self.UniqueCallback('@ShowDetailsLabel'),
                                                action=self.UniqueCallback('@FlipDetailsMode')),
                                                
            'open'              : Action(       label='Open',
                                                action=self.UniqueCallback('@OpenEntity'),
                                                visible=self.UniqueCallback('@OpenVisible')),
                        
            'topPanelActions'   : Action(       label='>',
                                                sizeToFit=True,
                                                actionList=self.UniqueCallback('@TopPanelActions')),

            'orderIsSent'       : Bool(         defaultValue = False),
            
            'sendInProgress'    : Bool(         defaultValue = False),
            
            'connectedTradesViewer' : Action(   dialog=self.UniqueCallback('@ConnectedTradesViewer')),
            
            'limitsChecked'         : Bool(   defaultValue=False,
                                                  label=''),

                                                
             # Private attributes
            'topDirectionLabel' :    Object(   objMapping = self.UniqueCallback('TopDirection'),
                                                onChanged =  self.UniqueCallback('@UpdateBuySellChoices'))
        })
        return attributes
        
    '''********************************************************************
    * Deal Misc
    ********************************************************************'''
    def OnInit(self, trade, dealPackage, originalObject, initiatedFromTradingInterface, reOpening, checkLimits, **kwargs):
        self._trade = trade
        self._originalObject = originalObject
        self._dealPackage = dealPackage
        self._initiatedFromTradingInterface = initiatedFromTradingInterface
        self._reOpening = reOpening
        self._checkLimits = checkLimits
        self._priceFormatter = acm.Get('formats/SolitaryPrice')
        self._quantityFormatter = acm.FNumFormatter('AbsInstrumentDefinitionQuantity')
        self._nominalFormatter = acm.FNumFormatter('AbsInstrumentDefinitionNominal')
        self._modifyOrderState = False
        self._salesOrderHandlerProxy = OrderHandlerProxy()
        self._MARKET_PRICE = acm.GetFunction('marketPrice', 0)()
        self._investmentDeciderDict = None
        self._investmentDeciderChoices = DealPackageChoiceListSource()
        self._buySellChoices = DealPackageChoiceListSource()
        self._initialDealPackageAmount = None
        self._defaultMarketPlace = None
        self._tradeCreationSetting = None
        self._tradeSettingChoices = DealPackageChoiceListSource()
        
    def OnNew(self):
        self.CreateInvestmentDeciderDict()
        self.InitiateTradeCreationSetting()
        if not self.WillReOpenLiveSalesOrder():
            if self.OriginalSalesOrderHandler():
                self.InitiateSalesOrderAttributesFromOriginalSalesOrder()
            elif self.ShouldInitiateFromOriginalTrade():
                self.InitiateSalesOrderAttributesFromOriginalTrade()
            elif self.ShouldInitiateFromOriginalDealPackage():
                self.InitiateSalesOrderAttributesFromOriginalDealPackage()
            else:
                self.portfolio = self.customAttributes.DefaultSalesPortfolio()
                
    '''********************************************************************
    * Objects
    ********************************************************************''' 
    def DefaultMarketPlace(self):
        if not self._defaultMarketPlace:
            self._defaultMarketPlace = acm.FMarketPlace[OrderBookCreation.DefaultMarket(self.SalesOrderInstrument())]
        return self._defaultMarketPlace
    
    def OriginalObject(self):
        return self.GetMethod(self._originalObject)()  

    def OriginalTrade(self):
        originalObject = self.OriginalObject()
        return originalObject if hasattr(originalObject, 'IsKindOf') and originalObject.IsKindOf(acm.FTrade) else None
    
    def OriginalDealPackage(self):
        originalObject = self.OriginalObject()
        return originalObject if hasattr(originalObject, 'IsKindOf') and originalObject.IsKindOf(acm.FDealPackage) else None
        
    def OriginalSalesOrderHandler(self):
        originalObject = self.OriginalObject()
        return originalObject if hasattr(originalObject, 'IsKindOf') and originalObject.IsKindOf(acm.FOrderHandler) else None
        
    def SalesOrderDealPackage(self):
        return self.GetMethod(self._dealPackage)()
          
    def SalesOrderInstrument(self):
        return self.SalesOrderTrade().Instrument()
    
    def SalesOrderCalcInstrument(self):
        instrument = self.SalesOrderInstrument()
        return None if instrument.IsExpired() else instrument
    
    def SalesOrderTrade(self):
        return self.GetMethod(self._trade)()

    def SalesOrderHandlerProxy(self):
        return self._salesOrderHandlerProxy
        
    def OriginalTradeId(self):
        oid = self.SalesOrderTrade().Originator().StorageId()
        return oid if oid > 0 else 0 
    
    def TradingInterface(self):
        tradingInterface = None
        interfaces = acm.Trading().TradingInterfaces(self.SalesOrderInstrument().Originator())
        for interface in interfaces:
            if interface.MarketPlace() == self.DefaultMarketPlace():
                tradingInterface = interface
                break
        return tradingInterface
    
    def InitiatedFromTradingInterface(self):
        return self.GetMethod(self._initiatedFromTradingInterface)()

    def SalesOrderHandlerCalcObj(self, *args):
        return self.SalesOrderHandlerProxy().OrderHandler()
    
    def CheckLimits(self):
        return self.GetMethod(self._checkLimits)()
    
    def ReOpening(self):
        return self.GetMethod(self._reOpening)()
    
    def WillReOpenLiveSalesOrder(self):
        return self.ReOpening() and self.OriginalSalesOrderHandler()

    '''********************************************************************
    * Subscriptions
    ********************************************************************'''     
    def DoRefresh(self):
        try:
            self.Owner().DealPackage().RefreshNeeded(True)     
        except Exception as e:
            print ('DoRefresh Failed', e)
    
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        if str(aspectSymbol) == 'update':
            acm.AsynchronousCall(DoRefreshCallback, [self])
        
    def DoAddDependent(self, orderHandlerProxy, orderHandler):
        if orderHandler:
            self.RemoveDependent()
            orderHandlerProxy.OrderHandler(orderHandler)
            orderHandler.AddDependent(self)
    
    def DoRemoveDependent(self, orderHandler):
        if orderHandler:
            orderHandler.RemoveDependent(self)

    def SetSalesOrderHandler(self, orderHandler):
        self.DoAddDependent(self.SalesOrderHandlerProxy(), orderHandler)
                
    def RemoveDependent(self):
        self.DoRemoveDependent(self.SalesOrderHandlerProxy().OrderHandler())

    def AmountAttribute(self):
        return 'quantity' if self.QuantityVisible() else 'nominal'
        
    def IsCustomAmount(self):
        return Amount.IsCustomAmount(self.SalesOrderDealPackage())    

    def Refresh(self):
        if not self.SalesOrderHandlerProxy().OrderHandler() and self.IsCustomAmount():
            self.SetAttribute('quantity', 1, silent=True)
            
    '''********************************************************************
    * Initiate from existing object
    ********************************************************************'''      
    def ShouldInitiateFromOriginalTrade(self):
        return not self.InitiatedFromTradingInterface() and not self.IsSalesOrderOnDealPackage() and self.OriginalTrade() and self.OriginalTrade().StorageId() > 0
    
    def ShouldInitiateFromOriginalDealPackage(self):
        return self.OriginalDealPackage() and self.OriginalDealPackage().StorageId() > 0
    
    def SetAttributesFromOrder(self, order):
        self.buySellQuantity = order.BuyOrSell()
        self.quantity = order.Quantity()
        self.client = order.Client()
        self.portfolio = order.Account() or DefaultSalesPortfolio()
        
    def InitiateTradeCreationSetting(self):
        self.tradeCreationSetting = TradeCreationUtil.InitialTradeCreationSetting(self.SalesOrderTrade(), self.SalesOrderDealPackage())
    
    def InitiateSalesOrderAttributesFromOriginalSalesOrder(self):
        order = self.OriginalSalesOrderHandler()
        self.SetAttributesFromOrder(order)
        self.SetCustomerPriceAndSpreadOnOpen(order)
        
    def InitiateSalesOrderAttributesFromOriginalTrade(self):
        trade = self.OriginalTrade()
        if trade:
            self.nominal = 0 if trade.Instrument().IsExpired() else abs(trade.Nominal()) 
            self.buySellNominal = 'Buy' if trade.BoughtAsString() == 'Sell' else 'Sell'
            self.buySellQuantity = self.buySellNominal
            self.client = trade.Counterparty()
            self.portfolio = trade.Portfolio()
            self.customerPrice = trade.Price()
    
    def InitiateSalesOrderAttributesFromOriginalDealPackage(self):
        dealPackage = self.SalesOrderDealPackage()
        if dealPackage:
            salesTradingInteraction = dealPackage.GetAttribute('salesTradingInteraction')
            if salesTradingInteraction:
                if salesTradingInteraction.At('clientAttr'):
                    self.client = dealPackage.GetAttribute(salesTradingInteraction.At('clientAttr'))
                if salesTradingInteraction.At('portfolioAttr'):
                    self.portfolio = dealPackage.GetAttribute(salesTradingInteraction.At('portfolioAttr'))
                amountInfo = salesTradingInteraction.At('amountInfo')
                if amountInfo:
                    amount = dealPackage.GetAttribute(amountInfo['amountAttr'])
                    if not amount:
                        self.SetAttribute('quantity', 1, silent=True)
                    else:
                        self.SetAttribute('quantity', abs(amount))
                    self.buySellNominal = 'Buy' if amount < 0 else 'Sell'
                    self.buySellQuantity = self.buySellNominal
            
    '''********************************************************************
    * Object Mappings
    ********************************************************************'''      
    def TradeCreationSetting(self, tradeSettingName = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(tradeSettingName):
            return TradeCreation.TradeSettingName(self._tradeCreationSetting, self.IsSalesOrderOnDealPackage())
        else:
            self._tradeCreationSetting = TradeCreation.EnumValue(tradeSettingName, self.IsSalesOrderOnDealPackage())
            
    def Client(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            clientName = self.SalesOrderHandlerProxy().Client()
            return acm.FParty[clientName] if clientName else None
        else:
            self.SalesOrderHandlerProxy().Client(val.Name() if val else None)
            
    def Portfolio(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            account = self.SalesOrderHandlerProxy().Account()
            return acm.FPhysicalPortfolio[account] if account else None
        else:
            self.SalesOrderHandlerProxy().Account(val.Name() if val else None)
            
    def ExpirationDateTime(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.SalesOrderHandlerProxy().ExpirationDateTime()
        else:
            self.SalesOrderHandlerProxy().ExpirationDateTime(val)
            
    def ValidityCondition(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.SalesOrderHandlerProxy().ValidityCondition()
        else:
            self.SalesOrderHandlerProxy().ValidityCondition(val)
    
    @ReturnDomainDecorator('double')
    def Quantity(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.SalesOrderHandlerProxy().Quantity()
        else:
            val = 0.0 if val is None else val
            return self.SalesOrderHandlerProxy().Quantity(abs(val))
    
    @ReturnDomainDecorator('double')
    def Nominal(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.QuantityToNominal(self.SalesOrderHandlerProxy().Quantity())
        else:
            self.SalesOrderHandlerProxy().Quantity(self.NominalToQuantity(abs(val)))
    
    @ReturnDomainDecorator('double')
    def NomInQuot(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.QuantityToNomInQuot(self.SalesOrderHandlerProxy().Quantity())
        else:
            self.SalesOrderHandlerProxy().Quantity(self.NomInQuotToQuantity(abs(val)))
    
    @ReturnDomainDecorator('FContact')
    def InvestmentDecider(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            investmentDeciderName = self.SalesOrderHandlerProxy().InvestmentDecisionMaker()
            self.CreateInvestmentDeciderDict()
            return self._investmentDeciderDict.At(investmentDeciderName)
        else:
            self.SalesOrderHandlerProxy().InvestmentDecisionMaker(val.Name() if val else None)

    def SalesStateDescription(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.SalesOrderHandlerProxy().SalesStateDescription()
        else:
            self.SalesOrderHandlerProxy().SalesStateDescription(val)
       
    def TraderPrice(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            price = self.SalesOrderHandlerProxy().Price()
            if price is None:
                price = 0.0
            if hasattr(price, 'IsKindOf') and price.IsKindOf(acm.FDenominatedValue):
                price = price.Value().Number()
            return price
        else:
            self.SalesOrderHandlerProxy().Price(val)
            
    def BuyOrSell(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            if self.SalesOrderHandlerProxy().BuyOrSell()=='Buy':
                return ButtonLabels.ButtonLabels(self.SalesOrderInstrument())[2]
            else:
                return ButtonLabels.ButtonLabels(self.SalesOrderInstrument())[0]
        else:
            buySell=self.TransformToBuySell(val)
            self.SalesOrderHandlerProxy().BuyOrSell(buySell)
                            
    def Trader(self, val = MethodDirection.asGetMethod):
        def FindUserIgnoreCase(userId):
            user = acm.FUser[userId] if userId else None
            if user:
                return user
            else:
                for user in self.UserChoices():
                    if user.Name().lower() == userId.lower():
                        return user
            return None
            
        if MethodDirection.AsGetMethod(val):
            userId = self.SalesOrderHandlerProxy().UserId()
            return FindUserIgnoreCase(userId) if userId else None
        else:
            self.SalesOrderHandlerProxy().UserId(val.Name() if val else None)
            
    '''********************************************************************
    * Action Callbacks
    ********************************************************************'''
    def OnCheckLimits(self, *args):
        limitsOk = self.CheckLimits()
        self.UpdateTradeSettingChoices()
        self.tradeCreationSetting = TradeCreation.Update(self.IsSalesOrderOnDealPackage())
        self.limitsChecked = limitsOk
    
    def StartApplication(self, appName, obj):
        startAppCb = self.Owner().GetAttribute('uxCallbacks').At('startApplication')
        if startAppCb:
            startAppCb(appName, obj)
    
    def OpenConnectedTradesViewer(self, taggedTrades):
        dialogCb = self.Owner().GetAttribute('uxCallbacks').At('dialog')
        if dialogCb:
            dialogCb(self.Owner().DealPackage(), self.PrefixedName('connectedTradesViewer'), taggedTrades)
            
    def OpenEntity(self, *args):
        Open.OpenEntity(self.SalesOrderDealPackage(),
                        self.SalesOrderTrade(),
                        self.tradeCreationSetting in [TradeCreation.CreateNewInsAndTrade(self.IsSalesOrderOnDealPackage()), TradeCreation.CreateNewTrade(self.IsSalesOrderOnDealPackage())],
                        'SalesOrderId', 
                        self.SalesOrderHandlerProxy().OrderId(),
                        self.StartApplication,
                        self.OpenConnectedTradesViewer)
    
    def ConnectedTradesViewer(self, attrName, taggedTrades):
        return UXDialogsWrapper(acm.DealCapturing().UX().ConnectedTradesViewerDialog, taggedTrades)

    def TopPanelActions(self, *args):
        actions = [self.PrefixedName('open')]
        topPanelActions = self.customAttributes.TopPanelActions()
        actions.extend(topPanelActions)
        return actions
        
    def OrderActions(self, *args):
        return [self.PrefixedName('sendOrder'), self.PrefixedName('newInsAndTrade'), self.PrefixedName('newTrade'), self.PrefixedName('modifyOrder'), self.PrefixedName('cancelOrder'), ]
    
    def NewActions(self, *args):
        actions = []
        def Add(internalName):
            actions.append(self.PrefixedName(internalName))
        Add('newInsAndTrade')
        Add('newTrade')
        return actions
        
    def AtMarketPriceAction(self, *args):
        self.customerPrice = self._MARKET_PRICE
        self.traderPrice = self._MARKET_PRICE
        
    def AtLimitedPriceAction(self, *args):
        self.customerPrice = 0.00
        self.traderPrice = 0.00
        
    '''********************************************************************
    * Attribute Validation
    ********************************************************************'''
    def ValidateQuantity(self, attrName, value):
        Validation.InstrumentIsExpired(self.SalesOrderInstrument())

    '''********************************************************************
    * Action list Callbacks
    ********************************************************************'''
    def PriceTypeActionList(self, *args):
        return [self.PrefixedName('atMarketPrice'),
                self.PrefixedName('atLimitedPrice')]
                
    '''********************************************************************
    * Label Callbacks
    ********************************************************************'''  
    def TopDirectionLabel(self, *args):
        return self.topDirectionLabel

    def TopDirection(self, *args):
        direction = Direction.ask if self.IsAskSide() else Direction.bid
        return Direction.Label(direction, self.SalesOrderInstrument())
        
    def BuyOrSellLabel(self, *args):
        return self.BuyOrSell()

    def InstrumentLabel(self, *args):
        if self.IsSalesOrderOnDealPackage():
            name  = self.SalesOrderDealPackage().InstrumentPackage().Originator().Name()
        else:
            name = self.SalesOrderInstrument().Originator().Name()
        return name        
        
    def TopISINLabel(self, *args):
        if self.IsSalesOrderOnDealPackage():
            isin  = ''
        else:
            isin = self.SalesOrderInstrument().Isin()
        return isin
        
    def TopTypeClientName(self, *args):
        return self.client.Name() if self.client else ''
        
    def ValidThroughLabel(self, *args):
        validThrough = ''
        if self.validityCondition:
            validThrough = self.validityCondition.Name()[:3]
            if validThrough == 'GTD':
                validThrough = self.expirationDateTime
        return validThrough
        
    def TopAmountLabel(self, *args):
        label = Amount.TopAmountLabel(self.nomInQuot, self.SalesOrderDealPackage())
        return '' if label in ['NaN'] else label
            
    def OrderPriceLabel(self, *args):
        return self._priceFormatter.Format(self.customerPrice)
        
    def TopQuotationLabel(self, *args):
        return Amount.QuotationLabel(self.SalesOrderInstrument(), self.SalesOrderDealPackage())
                
    def SalesStateName(self, *args):
        return self.SalesStateDescription()
        
    def TopTraderLabel(self, *args):
        return self.Trader().Name() if self.Trader() else ''
        
    def TopPricesLabel(self, *args):
        priceLabel = ''
        noPrice = '-'
        def GetPrice(price):
            formattedPrice = noPrice
            if price:
                formattedPrice = price.FormattedValue()
            return formattedPrice
        if not self.SalesOrderInstrument().IsExpired():
            ask = GetPrice(self.market_askPrice)
            bid = GetPrice(self.market_bidPrice)
            if ask in [noPrice, priceLabel] and bid in [noPrice, priceLabel]:
                priceLabel = ''
            else:
                priceLabel = bid + ' / ' + ask
        return priceLabel
        
    def TopTypeLabel(self, *args):
        label = ''
        if self.IsSalesOrderOnDealPackage():
            label = self.SalesOrderDealPackage().DefinitionName()
        else:
            label = self.SalesOrderInstrument().InsType()
        return label
    
    def ShowDetailsLabel(self, *args):
        return self.Owner().DealPackage().GetAttributeMetaData('toggleAllShowModes', 'label')()
    
    def QuantityLabel(self, attrName, *args):
        return Amount.QuantityLabel('Quantity', self.SalesOrderDealPackage())
    
    def NewInsAndTradeLabel(self, *args):
        return TradeCreation.CreateNewInsAndTrade(self.IsSalesOrderOnDealPackage())
    
    def NewTradeLabel(self, *args):
        return TradeCreation.CreateNewTrade(self.IsSalesOrderOnDealPackage())
        
    '''********************************************************************
    * Choices Callbacks
    ********************************************************************'''            
    def UpdateBuySellChoices(self, *args):
        self._buySellChoices.Populate([ButtonLabels.ButtonLabels(self.SalesOrderInstrument())[0], ButtonLabels.ButtonLabels(self.SalesOrderInstrument())[2]])

    def BuySellChoices(self, *args):
        if self._buySellChoices.IsEmpty():
            self.UpdateBuySellChoices()
        return self._buySellChoices

    def InvestmentDeciderDisplayNameChoices(self, *args):
        if self._investmentDeciderChoices.IsEmpty():
            self.UpdateInvestmentDeciderChoices()
        return self._investmentDeciderChoices

    def UpdateInvestmentDeciderChoices(self, *args):
        if self.client:
            self.CreateInvestmentDeciderDict()
            self._investmentDeciderChoices.Populate(self._investmentDeciderDict.Keys())
            self.investmentDecider = None
        else:
            self._investmentDeciderChoices.Populate([])
        
    def UserChoices(self, *args):
        return acm.FUser.Instances()
        
    def ValidityConditionChoices(self, *args):
        try:
            capabilites = None
            if self.TradingInterface():
                capabilites = self.TradingInterface().Capabilities()
            else:
                marketPlaceName = OrderBookCreation.DefaultMarket(self.SalesOrderInstrument())
                capabilites = acm.FMarketPlace[marketPlaceName].MarketService().Capabilities()
            choices = acm.Capabilities().GetChoiceList(capabilites, 'Order', 'ValidityCondition').Choices()
            if choices and choices.First() and (self.validityCondition is None):
                self.validityCondition = choices.First()
            return choices
        except Exception as e:
            print ('Failed to find Validity Conditions', e)
    
    def TradeSettingChoices(self, *args):
        if self._tradeSettingChoices.IsEmpty():
            self.UpdateTradeSettingChoices()
        return self._tradeSettingChoices
    
    def UpdateTradeSettingChoices(self):
        try:
            self._tradeSettingChoices.Populate(TradeCreationUtil.ValidTradeCreationChoices(self.SalesOrderTrade(), self.SalesOrderDealPackage()))
        except Exception as e:
            print ('TradeSettingChoices failed', e)
        return []
        
        
    '''********************************************************************
    * Width Callbacks
    ********************************************************************'''    
    def BuySellWidth(self, *args):
        width=0
        for choice in self.BuySellChoices().Source():
            if len(choice) > width:
                width = len(choice)
        return width+4
        
    '''********************************************************************
    * On Changed Callbacks
    ********************************************************************'''    
    def OnClientChanged(self, *args):
        self.ResetLimitChecks()
        self.UpdateInvestmentDeciderChoices()
        
    def OnInvestmentDeciderChanged(self, attr, oldValue, newValue, *args):
        if newValue is not None:
            self.CreateInvestmentDeciderDict()
            for key in self._investmentDeciderDict:
                value = self._investmentDeciderDict.At(key)
                if newValue == value:
                    self.investmentDeciderName = key
                    break
        else:
            self.investmentDeciderName = ''
 
    def OnInvestmentDeciderNameChanged(self, attr, oldValue, newValue, *args):
        self.CreateInvestmentDeciderDict()
        self.investmentDecider = self._investmentDeciderDict.At(newValue)
                   
    def OnSalesSpreadChanged(self, attrName, oldValue, newValue, *args):
        self.ResetLimitChecks()
        price = PriceAndMarginConversions.Price(newValue, self.customerPrice, self.IsAskSide(), self.TradingInterface(), self.SalesOrderInstrument())
        self.traderPrice = price
     
    def OnCustomerPriceChanged(self, attrName, oldValue, newValue, *args):
        self.ResetLimitChecks()
        price = PriceAndMarginConversions.Price(self.salesSpread, newValue, self.IsAskSide(), self.TradingInterface(), self.SalesOrderInstrument())
        self.SetAttribute('traderPrice', price, True)

    def OnQuantityChanged(self, attrName, oldValue, newValue, *args):
        self.ResetLimitChecks()
        if not self.orderIsSent: # Never change traderPrice on an order that is sent
            price = PriceAndMarginConversions.Price(self.salesSpread, self.customerPrice, self.IsAskSide(), self.TradingInterface(), self.SalesOrderInstrument())
            self.SetAttribute('traderPrice', price, True)
    
    def ResetLimitChecks(self, *args):
        self.limitsChecked = False
        
    '''********************************************************************
    * Transform Callbacks
    ********************************************************************'''
    def TransformExpirationDateTime(self, attrName, inputStr):
        if not inputStr:
            asDate = acm.Time().TodayAt(23, 59, 59, 0, False)
        else:
            asDate = inputStr
            if acm.Time().PeriodSymbolToDate(inputStr):
                asDate = Time.PeriodToDateTime(inputStr)
        return asDate
        
    def TransformValidityCondition(self, attrName, inputStr):
        if not inputStr:
            inputStr = self.ValidityConditionChoices().First()
        return inputStr
        
    '''********************************************************************
    * Formatter Callbacks
    ********************************************************************'''
    def PriceFormatter(self, *args):
        return self._priceFormatter
        
    def QuantityFormatter(self, *args):
        return self._quantityFormatter
    
    def NominalFormatter(self, *args):
        return self._nominalFormatter
         
    '''********************************************************************
    * Tick Callbacks
    ********************************************************************'''
    def NominalTick(self, attrName, value, increment):
        return TradingInterface.TickValue(value, increment, TickSizeSettings.NominalTickSize, self.SalesOrderInstrument(), self.TradingInterface())

    def PriceTick(self, attrName, value, increment):
        return TradingInterface.TickValue(value, increment, TickSizeSettings.PriceTickSize, self.SalesOrderInstrument(), self.TradingInterface())

    def SalesSpreadTick(self, attrName, value, increment):
        return TradingInterface.TickValue(value, increment, TickSizeSettings.SalesSpreadTickSize, self.SalesOrderInstrument(), self.TradingInterface())
        
    '''********************************************************************
    * Editable Callbacks
    ********************************************************************'''
    def NotInModifyState(self, *args):
        return not self._modifyOrderState
        
    '''********************************************************************
    * Visible Callbacks
    ********************************************************************'''
    def CheckLimitsVisible(self, *args):
        return not self.orderIsSent and Limits.CheckLimitsRequired(self.SalesOrderTrade(), self.SalesOrderDealPackage()) and not self.limitsChecked
        
    def TopISINVisible(self, *args):
        return self.insISINLabel and len(self.insISINLabel)

    def ValidityConditionIsGoodTillCancel(self, *args):
        name = self.validityCondition.Name() if self.validityCondition else None
        return True if name == 'GTD - Good Till Date' and self.IsShowModeDetail() else False
        
         
    def InShowModeDetail(self, *args):
        return self.IsShowModeDetail()
        
    def CloseDialogVisible(self, *args):
        return self.orderIsSent
        
    def CancelOrderVisible(self, *args):
        return self.CloseDialogVisible() and not self.SalesStateDescription() in ['Completed', 'Cancelled']
    
    def DoneVisible(self, *args):
        return self.CloseDialogVisible() and not self.SalesStateDescription() in ['Pending']
    
    def SendOrderVisible(self, *args):
        return not self.orderIsSent and (self.limitsChecked or not Limits.CheckLimitsRequired(self.SalesOrderTrade(), self.SalesOrderDealPackage()))

    def OpenVisible(self, *args):
        return Open.OpenButtonVisible(self.SalesOrderDealPackage(), self.SalesOrderInstrument(), self.orderIsSent, self.tradeCreationSetting == TradeCreation.CreateNewInsAndTrade(self.IsSalesOrderOnDealPackage()))
    
    def QuantityVisible(self, *args):
        return Amount.UseQuantity(self.SalesOrderInstrument(), self.SalesOrderDealPackage())
    
    def NominalVisible(self, *args):
        return not Amount.UseQuantity(self.SalesOrderInstrument(), self.SalesOrderDealPackage())
    
    def NomInQuotVisible(self, *args):
        return self.InShowModeDetail() and Amount.NomInQuotRelevant(self.SalesOrderInstrument(), self.SalesOrderDealPackage())
        
    def TradeSettingVisible(self, *args):
        dpType = self.SalesOrderDealPackage().DefinitionName() if self.SalesOrderDealPackage() else None
        visible = TradeCreation.SettingVisibleInDialog(self.SalesOrderInstrument().InsType(), dpType)
        return (visible and not self.orderIsSent) if self.IsShowModeDetail() else False
    
    def NewTradeActionVisible(self, *args):
        return self.NewOrderValid() and TradeCreation.CreateNewTrade(self.IsSalesOrderOnDealPackage()) in TradeCreationUtil.ValidTradeCreationChoices(self.SalesOrderTrade(), self.SalesOrderDealPackage())
    
    def NewInsAndTradeActionVisible(self, *args):
        return self.NewOrderValid() and TradeCreation.CreateNewInsAndTrade(self.IsSalesOrderOnDealPackage()) in TradeCreationUtil.ValidTradeCreationChoices(self.SalesOrderTrade(), self.SalesOrderDealPackage())
    
    def NewOrderValid(self, *args):
        return self.orderIsSent and self.SalesStateDescription() in ['Completed', 'Cancelled']
        
    '''********************************************************************
    * Enabled Callbacks
    ********************************************************************'''
    def TradeSettingEnabled(self, *args):
        checkLimitsRequired = Limits.CheckLimitsRequired(self.SalesOrderTrade(), self.SalesOrderDealPackage())
        return not self.orderIsSent and (not checkLimitsRequired or not self.limitsChecked)
        
    def CheckLimitsEnabled(self, *args):
        return self.QuantityAndClientSpecified()
    
    def QuantityAndClientSpecified(self, *args):
        return self.quantity >= 0.0 and self.client != None 
        
    def DisabledIfInitiatedFromTradingInterface(self, *args):
        if self.InitiatedFromTradingInterface():
            return False
        else:
            return self.EnabledIfNotOrderSent()
    
    def EnabledIfNotOrderSent(self, *args):
        return not self.orderIsSent
        
    def OrderSupportsUnlimited(self, *args):
        return self.EnabledIfNotOrderSent()
        
    def OrderSupportsLimited(self, *arags):
        return self.EnabledIfNotOrderSent()
        
    def SendOrderEnabled(self, *args):
        return (self.client and self.portfolio)
        
    def ModifyOrderEnabled(self, *args):
        enabled = self.orderIsSent and not self.SalesStateDescription() in ['Completed', 'Cancelled']
        if enabled and self.IsSalesOrderOnDealPackage():
            enabled = self.SalesStateDescription() not in ['In Exec', 'In Exec (R)']
        return enabled
        
    '''********************************************************************
    * Fonts Callbacks
    ********************************************************************'''
    def Arial(self, *args):
        return {'font':'Arial'}
        
    def Arial14(self, *args):
        return {'font':'Arial', 'bold':False, 'italic':False, 'size':14}
            
    def Arial12(self, *args):
        return {'font':'Arial', 'bold':False, 'italic':False, 'size':12}
            
    
    '''********************************************************************
    * New Sales Order From existing windows
    ********************************************************************'''       
    def CreateNewSalesOrder(self):
        self._modifyOrderState = False
        self._salesOrderHandlerProxy = OrderHandlerProxy()
        self.CreateInvestmentDeciderDict()
        self._investmentDeciderChoices = DealPackageChoiceListSource()
        
        self.orderIsSent = False
        self.limitsChecked = False
        self.sendInProgress = False
        
    def RememberTraitValues(self):
        valueDict = {}
        valueDict['buySellQuantity'] = self.buySellQuantity
        valueDict['quantity'] = self.quantity
        valueDict['customerPrice'] = self.customerPrice
        valueDict['salesSpread'] = self.salesSpread
        valueDict['validityCondition'] = self.validityCondition
        valueDict['expirationDateTime'] = self.expirationDateTime
        
        valueDict['client'] = self.client
        valueDict['portfolio'] = self.portfolio
        valueDict['investmentDeciderName'] = self.investmentDeciderName
        valueDict['trader'] = self.trader
        return valueDict
        
    def RestoreTraitValues(self, valueDict):
        self.buySellQuantity = valueDict['buySellQuantity']
        self.quantity = valueDict['quantity']
        self.customerPrice = valueDict['customerPrice']
        self.salesSpread = valueDict['salesSpread']
        self.validityCondition = valueDict['validityCondition']
        self.expirationDateTime = valueDict['expirationDateTime']
        
        self.client = valueDict['client']
        self.portfolio = valueDict['portfolio']
        self.investmentDeciderName = valueDict['investmentDeciderName']
        self.trader = valueDict['trader']
        
    '''********************************************************************
    * Action Callbacks
    ********************************************************************'''   
    def OnNewTrade(self, *args):
        self.tradeCreationSetting = TradeCreation.CreateNewTrade(self.IsSalesOrderOnDealPackage())
        self.OnNewSalesOrder()
    
    def OnNewInsAndTrade(self, *args):
        self.tradeCreationSetting = TradeCreation.CreateNewInsAndTrade(self.IsSalesOrderOnDealPackage())
        self.OnNewSalesOrder()
        
    def OnNewSalesOrder(self, *args):
        self._initialDealPackageAmount = None
        valueDict = self.RememberTraitValues()
        self.limitsChecked = False
        self.CreateNewSalesOrder()
        self.RestoreTraitValues(valueDict)
        self.UpdateTradeSettingChoices()
        
    def ValidateCancelOrderResult(self, task):  
        try:
            task.ResultOrThrow()
        except Exception as e:
            print ('Failed to Cancel Order', e)
    
    def OnCancelOrder(self, *args):
        orderHandler = self.SalesOrderHandlerProxy().OrderHandler()
        if orderHandler:
            acm.Trading().CancelOrder(orderHandler).ContinueWith(self.ValidateCancelOrderResult)

    def OnCloseDialog(self, *args):
        self.RemoveDependent()
        self.CloseDialog()
        
    def OnModifyOrder(self, *args):
        self.orderIsSent = False
        self._modifyOrderState = True
        
    def CheckInstrumentIsValidToSendOrder(self):
        return self.customAttributes.CheckInstrumentIsValidToSendOrder(self.TransformToBuySell(self.buySellQuantity), self.quantity, self.client, self.portfolio)
     
    def CheckValidToSendOrder(self):
        valid = True
        try:
            Validation.IsConnected(self.DefaultMarketPlace())
            valid = self.CheckInstrumentIsValidToSendOrder()
        except Exception as e:
            valid = False
            raise DealPackageUserException(str(e))
        return valid
    
    def SendOrder(self):
        if not self.sendInProgress:
            self.sendInProgress = True
            if self.SalesOrderHandlerProxy().OrderHandler():
                self.ModifyOrderFromOrderHandler(self.SalesOrderHandlerProxy().OrderHandler())
            else:
                if self.TradingInterface():
                    self.TradingInterface().Subscribe('RealTime', self).ContinueWith(self.CreateCustomerRequest)
                else:
                    createInfo = TradingInterface.CreateOrderBookCreateInfo(self.SalesOrderInstrument())
                    createInfo.Create().ContinueWith(self.SendOrderAsynch)
        
    def OnSendOrder(self, *args):
        if self.CheckValidToSendOrder():
            self.SendOrder()

    def FlipDetailsMode(self, *args):
        self.Owner().DealPackage().GetAttribute('toggleAllShowModes')()
        
    '''********************************************************************
    * Colors
    ********************************************************************'''      
    def IsAskSide(self):
        return True if self.TransformToBuySell(self.buySellQuantity) == 'Buy' else False
       
    def TopPanelColor(self, *args):
        direction = Direction.ask if self.IsAskSide() else Direction.bid
        return Direction.Color(direction, self.SalesOrderInstrument())

    '''********************************************************************
    * Utils
    ********************************************************************'''  
    def TransformToBuySell(self, label):
        if label == ButtonLabels.ButtonLabels(self.SalesOrderInstrument())[2]:
                return 'Buy'
        elif label == ButtonLabels.ButtonLabels(self.SalesOrderInstrument())[0]:
                return 'Sell'
                
    def IsSalesOrderOnDealPackage(self):
        return self.SalesOrderDealPackage() != None and not self.SalesOrderDealPackage().IsDeal()
    
    def CreateInvestmentDeciderDict(self):
        self._investmentDeciderDict = Misc.FindInvestmentDeciderChoices(self.client)
    
    def CreateTradesOnRequest(self):
        return TradeCreationUtil.CreateTradesOnRequest(self.SalesOrderTrade(), self.SalesOrderDealPackage())
    
    def UpdateSalesOrderIdAddInfo(self, orderId):
        try:
            TradeCreationUtil.TagTradesIfNecessary(self.SalesOrderTrade(), self.SalesOrderDealPackage(), 'SalesOrderId', orderId, self.tradeCreationSetting, self.IsSalesOrderOnDealPackage())
        except Exception as e:
            print ("UpdateSalesOrderIdAddInfo failed", e)
    
    def SetCustomerPriceAndSpread(self, order):
        priceDv = order.Price() if order.IsKindOf('FInternalMarketOrderHandler') else order.PriceLimit()
        traderPrice = priceDv.Number() if hasattr(priceDv, 'Number') else priceDv
        priceDiff = self.GetSalesSpreadAsExtendedDataShapePriceMargin(order)
        spread = ConversionCustomizations.MarginFromPriceDifference(priceDiff, self.TradingInterface(), self.SalesOrderInstrument())
        customerPrice = PriceAndMarginConversions.AllInPrice(spread, traderPrice, self.IsAskSide(), self.TradingInterface(), self.SalesOrderInstrument())
        if not self.orderIsSent:
            self.SetAttribute('traderPrice', traderPrice, True)
        self.SetAttribute('customerPrice', customerPrice, True)
        self.SetAttribute('salesSpread', spread, True) 
        
        
    def SetCustomerPriceAndSpreadOnOpen(self, order):
        try:
            self.SetCustomerPriceAndSpread(order)
        except Exception as e:
            print ('Failed to SetCustomerPriceAndSpreadOnOpen', e)
        
    def InitFromOrderHandlerAction(self, *args):        
        order = args[1]
        self.orderIsSent = True
        self.SetSalesOrderHandler(order)
        self.SetCustomerPriceAndSpreadOnOpen(order)
 
    def SalesOrderCustomAttributes(self):
        attrValDict = acm.FDictionary()
        try:
            for key in self.customAttributes.Attributes().keys():
                attrValDict.AtPut(key, self.customAttributes.GetAttribute(key))
        except Exception as e:
            print ('SalesOrderCustomAttributes fail', e)
        return attrValDict
    
    def ObjectToQuote(self, quoteOnlyInstrumentPart):
        return TradeCreationUtil.ObjectToQuote(self.SalesOrderDealPackage(), self.SalesOrderInstrument(), quoteOnlyInstrumentPart)

    def CreateCustomDict(self):
        def SetObjectsToQuote(objectsToQuote, quoteOnlyInstrumentPart):
            objectToQuote = self.ObjectToQuote(quoteOnlyInstrumentPart)
            objectsToQuote.AtPut(SalesTradingInteraction.SALES_NAME, objectToQuote)
                
        return TradeCreationUtil.CreateCustomDict(self.SalesOrderDealPackage(),
                                                  self.IsSalesOrderOnDealPackage(),
                                                  self.SalesOrderTrade(), 
                                                  self.tradeCreationSetting, 
                                                  self.SalesOrderCustomAttributes(),
                                                  SetObjectsToQuote)
    
    def CallExtensionPointForOrderCustomization(self):
        customDict = self.CreateCustomDict()
        SalesTradingInfo.SetSalesTradingExtendedData(self.SalesOrderHandlerProxy().OrderHandler(), SalesTradingInteraction.SALES_NAME, customDict, 1)
        self.customAttributes.OnCreateSalesOrder(SalesTradingInteraction.SALES_NAME, customDict)
        
    def SetSalesSpread(self, orderHandler):
        spreadAsPriceDiff = ConversionCustomizations.PriceDifferenceFromMargin(abs(self.salesSpread), self.TradingInterface(), self.SalesOrderInstrument())
        self.SetSalesSpreadAsExtendedDataShapePriceMargin(orderHandler, spreadAsPriceDiff)

    def SetOrderHandlerData(self, orderHandler):
        orderHandler.BuyOrSell(self.TransformToBuySell(self.buySellQuantity))
        orderHandler.Price(self.traderPrice)
        orderHandler.Quantity(self.quantity)
        orderHandler.Client(self.client.Name() if self.client else None)
        orderHandler.Account(self.portfolio.Name() if self.portfolio else None)
        orderHandler.ExpirationDateTime(self.expirationDateTime)
        orderHandler.SalesPerson(acm.User().Name())
        orderHandler.ValidityCondition(self.validityCondition)
        orderHandler.InvestmentDecisionMaker(self.investmentDecider.StringKey() if self.investmentDecider else '')
        if self.trader:
            orderHandler.UserId(self.trader.Name())
        self.SetSalesSpread(orderHandler)
        
    def ModifyOrderFromOrderHandler(self, orderHandler):
        try:
            self.SetSalesSpread(orderHandler)
            self.CallExtensionPointForOrderCustomization()    
            acm.Trading().SendOrder(orderHandler).ContinueWith(self.HandleSendOrderResult)
        except Exception as e:
            self.sendInProgress = False
            print ('Failed to ModifyOrderFromOrderHandler', e)
    
    def SendOrderFromOrderHandler(self, orderHandler):
        try:
            self.SetOrderHandlerData(orderHandler)
            acm.Trading().SetPendingExecution(orderHandler)
            self.CallExtensionPointForOrderCustomization()    
            acm.Trading().SendOrder(orderHandler).ContinueWith(self.HandleSendOrderResult)
        except Exception as e:
            self.sendInProgress = False
            print ('Failed to SendOrderFromOrderHandler', e)
       
    def SendOrderAsynch(self, task):
        try:
            tradingInterface = task.ResultOrThrow()
        except Exception as e:
            self.sendInProgress = False
            errorStr = 'Failed to create Trading Interface: ' + str(e)
            print errorStr
        else:
            tradingInterface.Subscribe('RealTime').ContinueWith(self.CreateCustomerRequest)  
            return True
     
    def SetSalesSpreadAsExtendedDataShapePriceMargin(self, orderHandler, spread):
        try:
            orderHandler.SetExtendedData('Shape Price Margin', spread)
        except Exception as e:
            print ('Cannot set Extended Data Shape_Price_Margin', e)
           
    def GetSalesSpreadAsExtendedDataShapePriceMargin(self, order):
        try:
            return order.GetExtendedData("Shape Price Margin")
        except Exception as e:
            print ('Cannot get Extended Data Shape_Price_Margin', e)
            
    def HandleSendOrderResult(self, task):
        try:
            self.sendInProgress = False
            orderHandler = task.ResultOrThrow()
            self.UpdateSalesOrderIdAddInfo(orderHandler.OrderId())
            self.orderIsSent = True
            self._modifyOrderState = False
            self.DoRefresh()
        except Exception as e:
            print ('Failed to send order', str(e))
            
    def CreateCustomerRequest(self, task):
        try:
            marketId = self.DefaultMarketPlace().Name() 
            clientName = self.client.Name()
            customerRequstName = self.customAttributes.SuggestCustomerRequestName(self.client)
            customerRequest = acm.Trading().CreateCustomerRequest(marketId, clientName, customerRequstName, '')
            acm.Trading().SendCustomerRequest(customerRequest).ContinueWith(self.SendSalesOrder)
        except Exception as e:
            self.sendInProgress = False
            print ('Failed to subscribe to order book', e)
            
    def SendSalesOrder(self, task):
        try:
            customerRequest = task.ResultOrThrow()
            trading = self.TradingInterface()
            tradingSession = acm.Trading().DefaultTradingSession()
            salesOrderHandler = tradingSession.NewSalesOrder(trading)
            salesOrderHandler.CustomerRequest(customerRequest)
            self.SetSalesOrderHandler(salesOrderHandler)
            self.SendOrderFromOrderHandler(salesOrderHandler)
        except Exception as e:
            self.sendInProgress = False
            print ('Failed to create customer request', e)
    
    def InstrumentNominal(self):
        nominalFactor = self.insNominalFactor.Value() if self.insNominalFactor else 0
        return nominalFactor * self.SalesOrderTrade().Instrument().ContractSize()
        
    def NominalToQuantity(self, nominal):
        return Amount.NominalToQuantity(nominal, self.InstrumentNominal()) if nominal is not None else 0.0
    
    def QuantityToNominal(self, quantity):
        return Amount.QuantityToNominal(quantity, self.InstrumentNominal()) if quantity is not None else 0.0
        
    def NomInQuotToQuantity(self, nomInQuot):
        return Amount.NomInQuotToQuantity(nomInQuot, self.InstrumentNominal(), self.SalesOrderInstrument().Quotation()) if nomInQuot is not None else 0.0
    
    def QuantityToNomInQuot(self, quantity):
        return Amount.QuantityToNomInQuot(quantity, self.InstrumentNominal(), self.SalesOrderInstrument().Quotation()) if quantity is not None else 0.0
    
