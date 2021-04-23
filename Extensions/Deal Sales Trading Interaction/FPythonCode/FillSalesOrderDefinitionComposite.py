import acm
from DealPackageDevKit import CompositeAttributeDefinition, ReturnDomainDecorator
from DealPackageDevKit import CompositeAttributeDefinition, UXDialogsWrapper
from DealPackageDevKit import Label, Box, Float, Action, CalcVal, Object
from RFQMarketComposite import RFQMarket
from RFQUtils import Direction, Amount, Misc, MethodDirection, TradingInterface, Open

from SalesTradingCustomizations import TickSizeSettings, IsYieldQuoted
from FillSalesOrderCustomizations import FillSalesOrderCustomDefinition


WHITE = acm.Get('Colors/White')
BLUE = acm.Get('Colors/Blue')

def DoRefreshCallback(pSelf, *args): 
    pSelf.Owner()._RegisterAllObjectMappings()
    pSelf.Owner().DealPackage().RefreshNeeded(True)
    
class FillSalesOrderDefinitionComposite(CompositeAttributeDefinition):
    def Attributes(self):
        attributes = {}
        
        ''' Top Panel '''
        attributes.update({  
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

            'market': RFQMarket(    instrumentName=self.UniqueCallback('SalesOrderInstrument')),
  
 
            'validThrough': Label(        label=self.UniqueCallback('@ValidThroughLabel'), 
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                width=190),
            
            'typeLabel': Label(        label=self.UniqueCallback('@TopTypeLabel'), 
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                width=190),
                      
            'salesPersonLabel': Label(        label=self.UniqueCallback('@SalesPersonLabel'),
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                width=190),
                                                
            'amountLabel': Label(        label=self.UniqueCallback('@TopAmountLabel'),
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                width=220),       
                                 
            'directionLabel': Label(        label=self.UniqueCallback('@TopDirectionLabel'),
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                width=220),   
                                                
            'orderPriceLabel': Label(        label=self.UniqueCallback('@TopOrderPriceLabel'),
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                width=220),

                                                  
            'quotationLabel': Label(        label=self.UniqueCallback('@TopQuotationLabel'),
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),      
                                                width=120),  
             
            'salesState': Label(        label=self.UniqueCallback('@SalesStateLabel'), 
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                alignment='Right',
                                                width=150),

            'traderLabel': Label(        label=self.UniqueCallback('@TraderLabel'),
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                alignment='Right',
                                                width=150),
                                                
            'prices': Label(        label=self.UniqueCallback('@TopPricesLabel'),
                                                labelFont=self.UniqueCallback('@Arial12'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                alignment='Right',
                                                width=150),
                                                

        })
        
        ''' General '''
        
        attributes.update({
            'infoMessagePanel'  : Box(          label='',
                                                vertical=False,
                                                textColor=WHITE,
                                                backgroundColor=self.UniqueCallback('@InfoMessageColor'),
                                                visible=self.UniqueCallback('@IsReqCancel')),
                                                            
            'infoMessage'       : Label(        label=self.UniqueCallback('@InfoMessage'),
                                                alignment='Center',
                                                width=540,
                                                labelColor=WHITE,
                                                backgroundColor=self.UniqueCallback('@InfoMessageColor'),
                                                visible=self.UniqueCallback('@IsReqCancel')),
                                                
            'fillQuantity'      : Float(        label='Quantity',
                                                formatter=self.UniqueCallback('@QuantityFormatter'),
                                                tick=True,
                                                visible=self.UniqueCallback('@QuantityVisible'),
                                                enabled=self.UniqueCallback('@PartialFillEnabled'),
                                                width=30),
                                                
            'fillNominal'       : Object(       label='Nominal',
                                                objMapping=self.UniqueCallback('FillNominal'),
                                                formatter=self.UniqueCallback('@NominalFormatter'),
                                                tick=self.UniqueCallback('@NominalTick'),
                                                visible=self.UniqueCallback('@NominalVisible'),
                                                enabled=self.UniqueCallback('@PartialFillEnabled')),
            
            'fillNomInQuot'     : Object(       label='Nom In Quot',
                                                objMapping=self.UniqueCallback('FillNomInQuot'),
                                                formatter=self.UniqueCallback('@NominalFormatter'),
                                                tick=self.UniqueCallback('@NominalTick'),
                                                visible=self.UniqueCallback('@NomInQuotVisible'),
                                                enabled=self.UniqueCallback('@PartialFillEnabled')),
            
                                                
            'fillPrice'         : Float(        defaultValue=0.0,
                                                label='Fill Price',
                                                formatter=self.UniqueCallback('@PriceFormatter'),
                                                tick=self.UniqueCallback('@PriceTick'),
                                                enabled=self.UniqueCallback('@DoFillEnabled'),
                                                width=30),
                                                
            'doFill'            : Action(       label=self.UniqueCallback('@FillLabel'),
                                                action=self.UniqueCallback('@DoFill'),
                                                backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                enabled=self.UniqueCallback('@DoFillEnabled')),
            
            'close'             : Action(       label='Close',
                                                action=self.UniqueCallback('@DoClose')),
            
            'doCancel'          : Action(       label='Cancel Order',
                                                action=self.UniqueCallback('@DoCancel'),
                                                backgroundColor=BLUE,
                                                textColor=WHITE,
                                                visible=self.UniqueCallback('@DoCancelVisible')),
                                    
            'customAttributes'      : FillSalesOrderCustomDefinition(
                                                instrumentMethod=self.UniqueCallback('SalesOrderInstrument'),
                                                orderHandlerMethod=self.UniqueCallback('SalesOrderHandler'),
                                                dealPackageMethod=self.UniqueCallback('SalesOrderDealPackage')),

            
            'open'                  : Action(   label='Open',
                                                action=self.UniqueCallback('@OpenEntity'),
                                                visible=self.UniqueCallback('@OpenVisible')),
            
            'topPanelActions'       : Action(   label='>',
                                                sizeToFit=True,
                                                actionList=self.UniqueCallback('@TopPanelActions')),
            
            'insNominalFactor'      : CalcVal(  calcMapping=self.UniqueCallback('SalesOrderTrade') + ':FTradeSheet:Standard Calculations Instrument Nominal Factor'),
            
            'connectedTradesViewer'         : Action(   dialog=self.UniqueCallback('@ConnectedTradesViewer'))


        })
        return attributes
        
    def OnInit(self, salesOrderName, salesOrderDealPackageName, salesOrderTrade, **kwargs):
        self._salesOrderName = salesOrderName
        self._salesOrderDealPackageName = salesOrderDealPackageName
        self._tradeName = salesOrderTrade
        self._priceFormatter = acm.Get('formats/SolitaryPrice')
        self._quantityFormatter = acm.FNumFormatter('AbsInstrumentDefinitionQuantity')
        self._nominalFormatter = acm.FNumFormatter('AbsInstrumentDefinitionNominal')
        self._salesOrderHandler = None
        self._MARKET_PRICE = acm.GetFunction('marketPrice', 0)()
        
    def GetInitialQuantity(self):
        quantity = 0
        if self.DoFillEnabled():
            quantity = self.SalesOrderHandler().Balance()
        return quantity
        
    def GetInitialPrice(self):
        price = 0.0
        if self.DoFillEnabled():
            price = self.SalesOrderHandler().Price()
            if price:
                if hasattr(price, 'IsKindOf') and price.IsKindOf(acm.FDenominatedValue):
                    price = price.Value().Number()
                if price == self._MARKET_PRICE:
                    price = 0.0
            else:
                price = 0.0
        return price

    def OnNew(self, *args):
        self.SetOrderHandler(self.GetOrderHandlersFromOrder(self.GetMethod(self._salesOrderName)()))
        self.fillQuantity = self.GetInitialQuantity()
        self.fillPrice = self.GetInitialPrice()    
        
    def OnDismantle(self):
        self.DoRemoveDependent()

    def SetOrderHandler(self, orderHandler):
        self.DoAddDependent(orderHandler)
        self._salesOrderHandler = orderHandler
        
    def GetOrderHandlersFromOrder(self, salesOrder):
        if salesOrder:
            tradingSession = acm.Trading().DefaultTradingSession()
            salesOrderHandler = tradingSession.AttachOrder(salesOrder)
        return salesOrderHandler
        
    def SalesOrderHandler(self):
        return self._salesOrderHandler

    def SalesOrderInstrument(self):
        return self.GetMethod(self._salesOrderName)().Instrument()
        
    def SalesOrderDealPackage(self):
        return self.GetMethod(self._salesOrderDealPackageName)()
    
    def SalesOrderTrade(self):
        return self.GetMethod(self._tradeName)()

    '''********************************************************************
    * Subscriptions
    ********************************************************************'''              
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        if str(aspectSymbol) == 'update':
            acm.AsynchronousCall(DoRefreshCallback, [self])
        
    def DoAddDependent(self, orderHandler):
        self.DoRemoveDependent()
        if orderHandler:
            orderHandler.AddDependent(self)
    
    def DoRemoveDependent(self):
        if self._salesOrderHandler:
            self._salesOrderHandler.RemoveDependent(self)     
   
    '''********************************************************************
    * Label Callbacks
    ********************************************************************'''
    def InstrumentLabel(self, *args):
        name = ''
        if self.SalesOrderDealPackage() and not self.IsDeal():
            name = self.SalesOrderDealPackage().InstrumentPackage().Name()
        else:
            name = self.SalesOrderInstrument().Name()
        return name

    def ValidThroughLabel(self, *args):
        validThrough = ''
        if self.SalesOrderHandler().ValidityCondition():
            validThrough = self.SalesOrderHandler().ValidityCondition().Name()[:3]
            if validThrough == 'GTD':
                validThrough = self.SalesOrderHandler().ExpirationDateTime()
        return validThrough
        
    def SalesPersonLabel(self, *args):
        return self.SalesOrderHandler().SalesPerson()
        
    def TopTypeLabel(self, *args):
        label = ''
        if self.SalesOrderDealPackage():
            label = self.SalesOrderDealPackage().DefinitionName()
        else:
            label = self.SalesOrderInstrument().InsType()
        return label
        
    def TopAmountLabel(self, *args):
        originalAmount = self.QuantityToNomInQuot(self.SalesOrderHandler().OriginalQuantity())
        filledQuantity = self.QuantityToNomInQuot(self.SalesOrderHandler().FilledQuantity('Trade'))
        label =  self._nominalFormatter.Format(originalAmount)
        if filledQuantity > 0.0:
            label +=  ' (' + self._nominalFormatter.Format(filledQuantity) + ')'
        return label
    
    def TopDirectionLabel(self, *args):
        direction = Direction.ask if self.SalesOrderHandler().BuyOrSell() == 'Buy' else Direction.bid
        return Direction.Label(direction, self.SalesOrderInstrument())
    
    def DirectionLabel(self, *args):
        return str(self.SalesOrderHandler().BuyOrSell())
        
    def SalesStateLabel(self, *args):
        return self.SalesOrderHandler().SalesState()

    def TraderLabel(self, *args):
        return self.SalesOrderHandler().UserId()
        
    def TopPricesLabel(self, *args):
        noPrice = '-'
        def GetPrice(price):
            formattedPrice = ''
            if price:
                formattedPrice = price.FormattedValue()
            if formattedPrice == '':
                formattedPrice = noPrice
            return formattedPrice
        ask = GetPrice(self.market_askPrice)
        bid = GetPrice(self.market_bidPrice)
        if ask == noPrice and bid == noPrice:
            return ''
        else:
            return bid + ' / ' + ask
            
    def TopOrderPriceLabel(self, *args):
        label = self.PriceFormatter().Format(self.SalesOrderHandler().Price())
        filledPrice = self.SalesOrderHandler().FilledPrice()
        if filledPrice > 0.0:
            label +=  ' (' + self.PriceFormatter().Format(filledPrice) + ')'
        return label

    def TopQuotationLabel(self, *args):
        return Amount.QuotationLabel(self.SalesOrderInstrument(), self.SalesOrderDealPackage())
        
    def TopISINLabel(self, *args):
        if self.SalesOrderDealPackage():
            isin  = ''
        else:
            isin = self.SalesOrderInstrument().Isin()
        return isin

    def FillLabel(self, *args):
        return 'Fill & Cancel' if self.IsReqCancel() else 'Fill'

    def InfoMessage(self, *args):
        msg = ''
        if self.IsReqCancel():
            msg = '%s has requested to cancel this order.' % self.salesPersonLabel
        return msg

    '''********************************************************************
    * Action Callbacks
    ********************************************************************'''
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
                        False,
                        'SalesOrderId', 
                        self.SalesOrderHandler().OrderId(),
                        self.StartApplication,
                        self.OpenConnectedTradesViewer,
                        False)
    
    def ConnectedTradesViewer(self, attrName, taggedTrades):
        return UXDialogsWrapper(acm.DealCapturing().UX().ConnectedTradesViewerDialog, taggedTrades)

    def TopPanelActions(self, *args):
        actions = [self.PrefixedName('open')]
        topPanelActions = self.customAttributes.TopPanelActions()
        actions.extend(topPanelActions)
        return actions
        
    def GetExtensionValue(self, extensionValueName):
        tradingInterface = self.SalesOrderHandler().TradingInterface()
        context = acm.GetDefaultContext()
        return tradingInterface.GetDefaultValueEx(extensionValueName, context)

    def ValidateQuantity(self):
        isValid = True
        quantity = self.fillQuantity
        remainingQuantity = self.SalesOrderHandler().Balance()
        if quantity > remainingQuantity:
            quantityStr = self._quantityFormatter.Format(quantity)
            remainingQuantityStr = self._quantityFormatter.Format(remainingQuantity)
            msgStr = 'The Fill quantity %s exceeds the order balance of %s.' % (quantityStr, remainingQuantityStr)
            if self.GetExtensionValue('ownOrderIsOverFillAllowed'):
                msgStr = msgStr + '\nAre you sure you would like to overfill the Sales Order?'
                isValid = self.Owner().DealPackage().GUI().GenericYesNoQuestion(msgStr)
            else:
                msgStr = msgStr + '\nYou are not allowed to overfill the Sales Order!'
                self.Owner().DealPackage().GUI().GenericMessage(msgStr)
                isValid = False
        return isValid
        
    def ValidatePrice(self):
        isValid = True
        if not self.SalesOrderHandler().IsUnlimitedPriceOrder():
            buyOrSell = self.SalesOrderHandler().BuyOrSell()
            isYield = IsYieldQuoted(self.SalesOrderHandler().TradingInterface(), self.SalesOrderInstrument())

            buyOrSellSign = 1 if buyOrSell == 'Buy' else -1
            yieldSign = -1 if isYield else 1
            price = self.fillPrice
            
            limit = self.SalesOrderHandler().Price().Value().Number()

            if ((limit - price) * yieldSign * buyOrSellSign) < 0:
                priceStr = self.PriceFormatter().Format(price)
                limitPriceStr = self.PriceFormatter().Format(self.SalesOrderHandler().Price())
                msgStr = 'The Fill price %s breaks the price limit of %s on the Sales Order.\nAre you sure you would like to proceed?' % (priceStr, limitPriceStr)
                isValid = self.Owner().DealPackage().GUI().GenericYesNoQuestion(msgStr)
        return isValid
    
    def ValidateValidPriceAndQuantity(self):
        return self.ValidateQuantity() and self.ValidatePrice()
        
    def EnterFillResult(self, task):
        try:
            task.ResultOrThrow()
        except Exception as e:
            print ('Enter Fill failed', e)
    
    def EnterFillResultAndCancelOrder(self, task):
        self.EnterFillResult(task)
        self.CancelOrder()
    
    def CancelOrder(self):
        hhmmss = "000000"
        self.SalesOrderHandler().SetExtendedData('AS ShapeTime', hhmmss)
        acm.Trading.SendOrder(self.SalesOrderHandler()).ContinueWith(self._CancelOrderTask)
    
    def _CancelOrderTask(self, task):
        try:
            task.ResultOrThrow()
            acm.Trading.CancelOrder(self.SalesOrderHandler()).ContinueWith(self.CancelOrderResult)
        except Exception as e:
            print ('Send Order failed', e)
    
    def CancelOrderResult(self, task):
        try:
            task.ResultOrThrow()
        except Exception as e:
            print ('Cancel Order failed', e)
    
    def DoFill(self, *args):    
        if self.ValidateValidPriceAndQuantity():
            tradingSession = acm.Trading().DefaultTradingSession()
            tradingInterface = self.SalesOrderHandler().TradingInterface()
            tradeReport = acm.FTradeReport(tradingInterface)
            tradeReport.BidOrAsk(0 if self.SalesOrderHandler().IsBuy() else 1)        
            tradeReport.Quantity(self.fillQuantity)
            tradeReport.Price(self.fillPrice)
            tradeReport.Account(self.SalesOrderHandler().Account())
            tradeReport.CounterpartyAccount(self.customAttributes.DefaultSalesOrderTradingPortfolioName())
            
            fillOrFillAndCancel = self.EnterFillResult
            if self.IsReqCancel():
                fillOrFillAndCancel = self.EnterFillResultAndCancelOrder
            
            acm.Trading().EnterFill(self.SalesOrderHandler(), tradeReport).ContinueWith(fillOrFillAndCancel)
            
            self.DoRemoveDependent()
            self.CloseDialog()
    
    def DoCancel(self, *args):
        self.CancelOrder()
        
        self.DoRemoveDependent()
        self.CloseDialog()
            
    def DoClose(self, *args):
        self.CloseDialog()
    
    '''********************************************************************
    * Object Mappings
    ********************************************************************'''
    @ReturnDomainDecorator('double')
    def FillNominal(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.QuantityToNominal(self.fillQuantity)
        else:
            self.fillQuantity = self.NominalToQuantity(abs(val))
    
    @ReturnDomainDecorator('double')
    def FillNomInQuot(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.QuantityToNomInQuot(self.fillQuantity)
        else:
            self.fillQuantity = self.NomInQuotToQuantity(abs(val))
        
    '''********************************************************************
    * Visible Callbacks
    ********************************************************************'''
    def TopISINVisible(self, *args):
        return self.insISINLabel and len(self.insISINLabel)

    def OpenVisible(self, *args):
        return Open.OpenButtonVisible(self.SalesOrderDealPackage(), self.SalesOrderInstrument())
    
    def QuantityVisible(self, *args):
        return Amount.UseQuantity(self.SalesOrderInstrument(), self.SalesOrderDealPackage())
    
    def NominalVisible(self, *args):
        return not Amount.UseQuantity(self.SalesOrderInstrument(), self.SalesOrderDealPackage())
    
    def NomInQuotVisible(self, *args):
        return Amount.NomInQuotRelevant(self.SalesOrderInstrument(), self.SalesOrderDealPackage())
    
    def DoCancelVisible(self, *args):
        return self.SalesOrderHandler().SalesState() == 'Req Cancel'
        
    def IsDeal(self):
        return self.SalesOrderDealPackage() and self.SalesOrderDealPackage().IsDeal()
        
    '''********************************************************************
    * Enabled Callbacks
    ********************************************************************'''
    def DoFillEnabled(self, *args):
        return self.SalesOrderHandler().SalesState() in ['In Exec', 'Req Cancel']
    
    def PartialFillEnabled(self, *args):
        return self.DoFillEnabled() and (not self.SalesOrderDealPackage() or self.IsDeal())
    
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
    * Colors
    ********************************************************************'''        
    def TopPanelColor(self, *args):
        direction = Direction.ask if self.SalesOrderHandler().BuyOrSell() == 'Buy' else Direction.bid
        return Direction.Color(direction, self.SalesOrderInstrument())
    
    def InfoMessageColor(self, *args):
        return BLUE if self.infoMessage else None
    
    '''********************************************************************
    * Tick Callbacks
    ********************************************************************'''
    def NominalTick(self, attrName, value, increment):
        return TradingInterface.TickValue(value, increment, TickSizeSettings.NominalTickSize, self.SalesOrderInstrument(), self.SalesOrderHandler().TradingInterface())

    def PriceTick(self, attrName, value, increment):
        return TradingInterface.TickValue(value, increment, TickSizeSettings.PriceTickSize, self.SalesOrderInstrument(), self.SalesOrderHandler().TradingInterface())
        
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
    * Utils
    ********************************************************************'''
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
        
    def IsReqCancel(self, *args):
        return self.SalesOrderHandler().SalesState() == 'Req Cancel'
