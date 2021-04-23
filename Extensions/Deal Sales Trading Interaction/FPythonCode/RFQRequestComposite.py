import acm

from DealPackageDevKit import CompositeAttributeDefinition
from DealPackageDevKit import Int, Action, Str, Object, Float, Label, Bool
from DealPackageDevKit import DealPackageException, DealPackageUserException, PortfolioChoices, CounterpartyChoices, DealPackageChoiceListSource

from RFQUtils import TradingInterface, Colors, Time, Direction, Status, MethodDirection
from RFQUtils import Amount, Validation, Misc
from TradeCreationUtil import TradeCreation, TradeCreationUtil

from SalesTradingCustomizations import ButtonLabels, TickSizeSettings, OrderBookCreation, RFQTimerDefaultSettings, Limits

class RFQRequest(CompositeAttributeDefinition):

    def Attributes(self):
        attributes = {}
        
        ''' Reply '''
        attributes.update({
                
                'isRfq': Bool(   defaultValue=True,
                                                  label='Soft'),
        
                'direction': Str(    objMapping=self._qrData + '.Direction'),


                'buy': Action( label=self.UniqueCallback('@BuyLabel'),
                                                  action=self.UniqueCallback('@OnBuy'),
                                                  backgroundColor=self.UniqueCallback('@BuyButtonColor'),
                                                  textFont=self.UniqueCallback('@BuyButtonFont'),
                                                  enabled=self.UniqueCallback('@RequestNotSent'),
                                                  visible=self.UniqueCallback('@RequestNotSent')),   
                
                'twoSided': Action( label=self.UniqueCallback('@TwoWayLabel'),
                                                  action=self.UniqueCallback('@OnTwoWay'),
                                                  backgroundColor=self.UniqueCallback('@TwoSidedButtonColor'),
                                                  textFont=self.UniqueCallback('@TwoSidedButtonFont'),
                                                  enabled=self.UniqueCallback('@RequestNotSent'),
                                                  visible=self.UniqueCallback('@RFQModeAndRequestNotSent')),
                                                  
                'sell': Action( label=self.UniqueCallback('@SellLabel'),
                                                  action=self.UniqueCallback('@OnSell'),
                                                  backgroundColor=self.UniqueCallback('@SellButtonColor'),
                                                  textFont=self.UniqueCallback('@SellButtonFont'),
                                                  enabled=self.UniqueCallback('@RequestNotSent'),
                                                  visible=self.UniqueCallback('@RequestNotSent')),   
                                           
                'requestedQuantity': Object( label=self.UniqueCallback('@QuantityLabel'),
                                                  objMapping=self._qrData + '.RequestedQuantity',
                                                  onChanged=self.UniqueCallback('@ResetLimitChecks'),
                                                  editable=self.UniqueCallback('@RequestNotSent'),
                                                  visible=self.UniqueCallback('@QuantityVisible'),
                                                  formatter='InstrumentDefinitionQuantity',
                                                  validate=self.UniqueCallback('@ValidateQuantity'),
                                                  initialFocus=self.UniqueCallback('@InitialFocus'),
                                                  tick=True),
       
                'requestedNominal': Object( label='Nominal',
                                                  objMapping=self._qrData + '.RequestedNominal',
                                                  editable=self.UniqueCallback('@RequestNotSent'),
                                                  visible=self.UniqueCallback('@NominalVisible'),
                                                  formatter='InstrumentDefinitionNominal',
                                                  validate=self.UniqueCallback('@ValidateNominal'),
                                                  initialFocus=True,
                                                  tick=self.UniqueCallback('@NominalTick')),
                
                'requestedNomInQuot': Object( label='Nom In Quot',
                                                  objMapping=self._qrData + '.RequestedNomInQuot',
                                                  editable=self.UniqueCallback('@RequestNotSent'),
                                                  visible=self.UniqueCallback('@NomInQuotVisible'),
                                                  formatter='InstrumentDefinitionNominal',
                                                  validate=self.UniqueCallback('@ValidateNominal'),
                                                  initialFocus=False,
                                                  tick=self.UniqueCallback('@NominalTick')),
                
                'minimumQuantity': Object( label=self.UniqueCallback('@MinimumQuantityLabel'),
                                                  objMapping=self._qrData + '.MinimumQuantity',
                                                  editable=self.UniqueCallback('@RequestNotSent'),
                                                  visible=self.UniqueCallback('@MinimumQuantityVisible'),
                                                  formatter='InstrumentDefinitionQuantity',
                                                  validate=self.UniqueCallback('@ValidateMinimumQuantity'),
                                                  tick=True),
       
                'minimumNominal': Object( label='Min Nominal',
                                                  objMapping=self._qrData + '.MinimumNominal',
                                                  editable=self.UniqueCallback('@RequestNotSent'),
                                                  visible=self.UniqueCallback('@MinimumNominalVisible'),
                                                  formatter='InstrumentDefinitionNominal',
                                                  validate=self.UniqueCallback('@ValidateMinimumNominal'),
                                                  initialFocus=True,
                                                  tick=self.UniqueCallback('@NominalTick')),
                
                'minimumNomInQuot': Object( label='Min Nom In Quot',
                                                  objMapping=self._qrData + '.MinimumNomInQuot',
                                                  editable=self.UniqueCallback('@RequestNotSent'),
                                                  visible=self.UniqueCallback('@MinimumNomInQuotVisible'),
                                                  formatter='InstrumentDefinitionNominal',
                                                  validate=self.UniqueCallback('@ValidateMinimumNominal'),
                                                  initialFocus=False,
                                                  tick=self.UniqueCallback('@NominalTick')),
                
                'priceLimit': Object( label='Fee',
                                                  objMapping=self._qrData + '.PriceLimit',
                                                  visible=self.UniqueCallback('@OrderModeAndRequestNotSent'),
                                                  formatter='SolitaryPrice',
                                                  initialFocus=False,
                                                  tick=self.UniqueCallback('@PriceTick')),
                                                  
                'client': Object( objMapping=self._qrData + '.Client',
                                                  label='Client',
                                                  choiceListSource=CounterpartyChoices(),
                                                  onChanged=self.UniqueCallback('@OnClientChanged'),
                                                  editable=self.UniqueCallback('@RequestNotSent'),
                                                  visible=self.UniqueCallback('@RequestNotSent')),
                
                'investmentDecider': Object( objMapping=self._qrData + '.InvestmentDecider',
                                                  onChanged=self.UniqueCallback('@OnInvestmentDeciderChanged')),
                
                'investmentDeciderName': Str(    label='Inv Decider',
                                                  choiceListSource=self.UniqueCallback('@InvestmentDeciderDisplayNameChoices'),
                                                  editable=self.UniqueCallback('@RequestNotSent'),
                                                  visible=self.UniqueCallback('@RequestNotSentAndShowModeDetail2'),
                                                  onChanged=self.UniqueCallback('@OnInvestmentDeciderNameChanged')),

                'salesPortfolio': Object( label='Portfolio',
                                                  objMapping=self._qrData + '.SalesPortfolio',
                                                  onChanged=self.UniqueCallback('@ResetLimitChecks'),
                                                  choiceListSource=PortfolioChoices(),
                                                  editable=self.UniqueCallback('@RequestNotSent'),
                                                  visible=self.UniqueCallback('@SalesPortfolioVisible')),

                'toTrader': Object( label='Trader',
                                                  objMapping=self._qrData + '.ToTrader',
                                                  visible=self.UniqueCallback('@RequestNotSentAndShowModeDetail2'),
                                                  editable=self.UniqueCallback('@RequestNotSent')),

                'comment': Object( objMapping=self._qrData + '.Comment',
                                                  label='Comment'),

                'settlementDate': Object( label=self.UniqueCallback('@SettlementLabel'),
                                                  visible=self.UniqueCallback('@RequestNotSentAndShowModeDetail2'),
                                                  objMapping=self.UniqueCallback('Trade') + '.ValueDay',
                                                  editable=False),
                
                'replyTime': Object( label='',
                                                  objMapping=self._qrData + '.ReplyTime',
                                                  formatter='SecondsSpan',
                                                  transform=self.UniqueCallback('@TransformTimeSpan'),
                                                  visible=self.UniqueCallback('@ReplyTimeVisible'),
                                                  editable=self.UniqueCallback('@RequestNotSent'),
                                                  validate=self.UniqueCallback('@ValidateReplyTime'),
                                                  width=19,
                                                  maxWidth=19),  
                                                  
                'replyExpiry': Object( label='',
                                                  objMapping=self._qrData + '.ReplyExpiry',
                                                  formatter='TimeOnlyIfToday',
                                                  transform=self.UniqueCallback('@TransformExpiry'),
                                                  visible=self.UniqueCallback('@ReplyExpiryVisible'),
                                                  editable=self.UniqueCallback('@RequestNotSentAndShowModeDetail2'),
                                                  validate=self.UniqueCallback('@ValidateReplyExpiry'),
                                                  width=19,
                                                  maxWidth=19),
                                                  
                'replyTimeoutType': Object( label='Reply Time',
                                                  visible=self.UniqueCallback('@RequestNotSentAndShowModeDetail2'),
                                                  objMapping=self._qrData + '.ReplyTimeoutType',
                                                  choiceListSource=self.UniqueCallback('@TimeoutTypes')),
                
                'negotiationTime': Object( label='',
                                                  objMapping=self._qrData + '.NegotiationTime',
                                                  formatter='SecondsSpan',
                                                  transform=self.UniqueCallback('@TransformTimeSpan'),
                                                  visible=self.UniqueCallback('@NegotiationTimeVisible'),
                                                  editable=self.UniqueCallback('@RequestNotSent'),
                                                  validate=self.UniqueCallback('@ValidateNegotiationTime'),
                                                  width=19,
                                                  maxWidth=19),    
    
                'negotiationExpiry': Object( label='',
                                                  objMapping=self._qrData + '.NegotiationExpiry',
                                                  formatter='TimeOnlyIfToday',
                                                  transform=self.UniqueCallback('@TransformExpiry'),
                                                  visible=self.UniqueCallback('@NegotiationExpiryVisible'),
                                                  editable=self.UniqueCallback('@RequestNotSent'),
                                                  validate=self.UniqueCallback('@ValidateNegotiationExpiry'),
                                                  width=19,
                                                  maxWidth=19),
                                                  
                'negotiationTimeoutType': Object( label='Expiry',
                                                  visible=self.UniqueCallback('@RequestNotSentAndShowModeDetail2'),
                                                  objMapping=self._qrData + '.NegotiationTimeoutType',
                                                  choiceListSource=self.UniqueCallback('@TimeoutTypes')),
                                                          
                'tradeCreationSetting': Object( label='Trade Flow',
                                                  choiceListSource=self.UniqueCallback('@TradeSettingChoices'),
                                                  objMapping=self.UniqueCallback('TradeCreationSetting'),
                                                  visible=self.UniqueCallback('@TradeSettingVisible'),
                                                  enabled=self.UniqueCallback('@TradeSettingEnabled')),
 
                'request': Action( label='Request',
                                                  action=self.UniqueCallback('@OnRequestQuote'),
                                                  backgroundColor=self.UniqueCallback('@RequestButtonColor'),
                                                  enabled=self.UniqueCallback('@RequestEnabled'),
                                                  visible=self.UniqueCallback('@RequestVisible')),
                
                'sendOrder': Action( label='Send Order',
                                                  action=self.UniqueCallback('@OnSendOrder'),
                                                  backgroundColor=self.UniqueCallback('@RequestButtonColor'),
                                                  enabled=self.UniqueCallback('@RequestEnabled'),
                                                  visible=self.UniqueCallback('@SendOrderVisible')),
                
                'checkLimits': Action( label='Check Limits',
                                                  action=self.UniqueCallback('@OnCheckLimits'),
                                                  enabled=self.UniqueCallback('@CheckLimitsEnabled'),
                                                  visible=self.UniqueCallback('@CheckLimitsVisible')),
                 
                'newInsAndTrade': Action( label=self.UniqueCallback('@NewInsAndTradeLabel'),
                                                  action=self.UniqueCallback('@OnNewInsAndTrade'),
                                                  visible=self.UniqueCallback('@NewInsAndTradeActionVisible')),
                
                'newTrade': Action( label=self.UniqueCallback('@NewTradeLabel'),
                                                  action=self.UniqueCallback('@OnNewTrade'),
                                                  visible=self.UniqueCallback('@NewTradeActionVisible')),
                
                'newActions': Action( label='New >',
                                                  actionList=self.UniqueCallback('@NewActions'),
                                                  visible=self.UniqueCallback('@NewRequestValid')),

                'withdraw': Action( label=self.UniqueCallback('@WithdrawLabel'),
                                                  action=self.UniqueCallback('@OnWithdrawQuoteRequest'),
                                                  visible=self.UniqueCallback('@QuoteRequestWithdrawValid')),

                'updateRequest': Action( label='Update request',
                                                  action=self.UniqueCallback('@OnUpdateQuoteRequest'),
                                                  visible=self.UniqueCallback('@UpdateRequestValid'),
                                                  enabled=self.UniqueCallback('@CommentEntered')),

                'sendMessage': Action( label='Send Msg',
                                                  action=self.UniqueCallback('@OnQuoteRequestSendMsg'),
                                                  visible=self.UniqueCallback('@QuoteRequestSendMsgValid'),
                                                  enabled=self.UniqueCallback('@CommentEntered')),
                
                'atMarketPrice': Action( label='Market',
                                                  action=self.UniqueCallback('@AtMarketPriceAction'),
                                                  visible=self.UniqueCallback('@OrderModeAndRequestNotSent'),
                                                  enabled=self.UniqueCallback('@OrderModeAndRequestNotSent')),
                                                
                'atLimitedPrice': Action( label='Limited',
                                                  action=self.UniqueCallback('@AtLimitedPriceAction'),
                                                  visible=self.UniqueCallback('@OrderModeAndRequestNotSent'),
                                                  enabled=self.UniqueCallback('@OrderModeAndRequestNotSent')),
                
                'priceType': Action( label='>',
                                                  actionList=self.UniqueCallback('@PriceTypeActionList'),
                                                  sizeToFit=True,
                                                  visible=self.UniqueCallback('@OrderModeAndRequestNotSent'),
                                                  enabled=self.UniqueCallback('@OrderModeAndRequestNotSent')),

                'requestActions': Action( label='>',
                                                  sizeToFit=True,
                                                  actionList=self.UniqueCallback('@RequestActions'),
                                                  visible=self.UniqueCallback('@RequestActionsVisible')),

                'requestButtonClicked': Bool(   defaultValue=False,
                                                  label=''),    

                'limitsChecked': Bool(   defaultValue=False,
                                                  label=''),

        })
        
        self.CreateNominalIncrementAttributes(attributes)
        
        return attributes
        
    '''********************************************************************
    * Deal Definition
    ********************************************************************'''    
    def OnInit(self, createNewQuoteRequest, reOpening, checkLimits, **kwargs):
        self._qrData = kwargs['qrDataMethod']
        self._imInterface = kwargs['imInterfaceMethod']
        self._instrument = kwargs['instrumentMethod']
        self._dealPackage = kwargs['dealPackageMethod']
        self._isRfqOnDealPackage = kwargs['isRfqOnDealPackageMethod']
        self._trade = kwargs['tradeMethod']
        self._customAttributes = kwargs['customAttributesMethod']
        self._originalObject = kwargs['originalObjectMethod']
        self._reOpening = reOpening
        self._checkLimits = checkLimits
        self._createNewQuoteRequest = createNewQuoteRequest
        self._investmentDeciderDict = None
        self._investmentDeciderChoices = DealPackageChoiceListSource()
        self._tradeSettingChoices = DealPackageChoiceListSource()
        self._tradeCreationSetting = None
        self._MARKET_PRICE = acm.GetFunction('marketPrice', 0)()
        
    def OnNew(self):
        self.CreateInvestmentDeciderDict()
        self.InitiateTradeCreationSetting()
        if not self.WillReOpenLiveQuoteRequest():
            if self.OriginalCustomerQuoteRequest():
                self.InitiateRequestAttributesFromOriginalQuoteRequest()
            elif self.ShouldInitiateFromOriginalTrade():
                self.InitiateRequestAttributesFromOriginalTrade()
            elif self.ShouldInitiateFromOriginalDealPackage():
                self.InitiateRequestAttributesFromOriginalDealPackage()
            else:
                self.SetDefaultValues()
            self.SetDefaultNegotiationAndReplyTime()
    
    def ShouldInitiateFromOriginalTrade(self):
        return not self.IsRFQOnDealPackage() and self.OriginalTrade() and self.OriginalTrade().StorageId() > 0
    
    def ShouldInitiateFromOriginalDealPackage(self):
        return self.OriginalDealPackage() and self.OriginalDealPackage().StorageId() > 0
        
    def InitiateTradeCreationSetting(self):
        self.tradeCreationSetting = TradeCreationUtil.InitialTradeCreationSetting(self.Trade(), self.RFQDealPackage())
        
    def InitiateRequestAttributesFromOriginalQuoteRequest(self):
        qr = self.OriginalCustomerQuoteRequest()
        self.salesPortfolio = qr.Account() or self.CustomAttributeMethod('DefaultSalesPortfolio')()
        self.client = qr.Client()
        self.requestedQuantity = qr.Quantity()
        self.direction = qr.BidOrAsk()
        
    def InitiateRequestAttributesFromOriginalTrade(self):
        trade = self.OriginalTrade()
        self.requestedNominal = 0 if trade.Instrument().IsExpired() else abs(trade.Nominal())
        self.client = trade.Counterparty()
        self.salesPortfolio = trade.Portfolio()
        self.direction = Direction.FromQuantity(-trade.Quantity(), trade.Instrument())
            
    def InitiateRequestAttributesFromOriginalDealPackage(self):
        dealPackage = self.RFQDealPackage()
        salesTradingInteraction = dealPackage.GetAttribute('salesTradingInteraction')
        if salesTradingInteraction:
            if salesTradingInteraction.At('clientAttr'):
                self.client = dealPackage.GetAttribute(salesTradingInteraction.At('clientAttr'))
            if salesTradingInteraction.At('portfolioAttr'):
                self.salesPortfolio = dealPackage.GetAttribute(salesTradingInteraction.At('portfolioAttr'))
            amountInfo = salesTradingInteraction.At('amountInfo')
            if amountInfo:
                amount = dealPackage.GetAttribute(amountInfo['amountAttr'])
                if not amount:
                    self.SetAttribute('requestedQuantity', 1, silent=True)
                else:
                    self.SetAttribute('requestedQuantity', abs(amount))
            bidOrAsk = Direction.bid if amount > 0 else Direction.ask
            self.direction = bidOrAsk
            
    '''********************************************************************
    * Object Mappings
    ********************************************************************'''          
    def QRData(self):
        return self.GetMethod(self._qrData)()

    def IMInterface(self):
        return self.GetMethod(self._imInterface)()
    
    def TradingInterface(self):
        return self.IMInterface().TradingInterface() if self.IMInterface() else None

    def Instrument(self):
        return self.GetMethod(self._instrument)()

    def Trade(self):
        return self.GetMethod(self._trade)()
        
    def RFQDealPackage(self):
        return self.GetMethod(self._dealPackage)()
    
    def IsRFQOnDealPackage(self):
        return self.GetMethod(self._isRfqOnDealPackage)()
    
    def OriginalObject(self):
        return self.GetMethod(self._originalObject)()  

    def OriginalTrade(self):
        originalObject = self.OriginalObject()
        return originalObject if hasattr(originalObject, 'IsKindOf') and originalObject.IsKindOf(acm.FTrade) else None
    
    def OriginalDealPackage(self):
        originalObject = self.OriginalObject()
        return originalObject if hasattr(originalObject, 'IsKindOf') and originalObject.IsKindOf(acm.FDealPackage) else None
        
    def OriginalCustomerQuoteRequest(self):
        originalObject = self.OriginalObject()
        return originalObject if hasattr(originalObject, 'IsKindOf') and originalObject.IsKindOf(acm.FQuoteRequestInfo) else None

    def CustomAttributesAttr(self):
        return self.GetMethod(self._customAttributes)()

    def CustomAttributeMethod(self, methodName):
        customAttributes = self.CustomAttributesAttr()
        return getattr(customAttributes, methodName)
 
    def NominalIncrements(self):
        return self.CustomAttributeMethod('NominalIncrements')()
        
    def CheckInstrumentIsValidToSendQuoteRequest(self):
        self.CustomAttributeMethod('CheckInstrumentIsValidToSendQuoteRequest')(self.requestedNominal, self.client)
    
    def TradeCreationSetting(self, tradeSettingName = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(tradeSettingName):
            return TradeCreation.TradeSettingName(self._tradeCreationSetting, self.IsRFQOnDealPackage())
        else:
            self._tradeCreationSetting = TradeCreation.EnumValue(tradeSettingName, self.IsRFQOnDealPackage())
    
    def CheckLimits(self):
        return self.GetMethod(self._checkLimits)()
    
    def ReOpening(self):
        return self.GetMethod(self._reOpening)()
    
    def WillReOpenLiveQuoteRequest(self):
        return self.ReOpening() and self.OriginalCustomerQuoteRequest()

    '''********************************************************************
    * Actions
    ********************************************************************'''
    def RequestActions(self, *args):
        actions = []
        def Add(internalName):
            actions.append(self.PrefixedName(internalName))
        Add('request')
        Add('sendMessage')
        Add('updateRequest')
        Add('withdraw')
        return actions
    
    def PriceTypeActionList(self, *args):
        return [self.PrefixedName('atMarketPrice'),
                self.PrefixedName('atLimitedPrice')]
                
    def NewActions(self, *args):
        actions = []
        def Add(internalName):
            actions.append(self.PrefixedName(internalName))
        Add('newInsAndTrade')
        Add('newTrade')
        return actions

    def OnBuy(self, *args):
        self.direction = Direction.ask
        
    def OnSell(self, *args):
        self.direction = Direction.bid
        
    def OnTwoWay(self, *args):
        self.direction = Direction.twoWay
    
    def OnCheckLimits(self, *args):
        limitsOk = self.CheckLimits()
        self.limitsChecked = limitsOk
        self.UpdateTradeSettingChoices()
        self.tradeCreationSetting = TradeCreation.Update(self.IsRFQOnDealPackage())

    def CheckValidToSendQuoteRequest(self):
        instrument = self.Instrument()
        if not self.requestedNominal > 0:
            raise DealPackageUserException('Cannot send quote request with zero quantity')
        self.CheckInstrumentIsValidToSendQuoteRequest()
        Validation.Nominal(self.requestedNominal, instrument)
        if not self.salesPortfolio:
            raise DealPackageUserException('No sales portfolio')
        if self.NegotiationTimeOrExpiry() != 0 and Time.Compare(self.ReplyTimeOrExpiry(), self.NegotiationTimeOrExpiry()):
            self.RaiseReplyTimeCannotBeLargerThanExpiry()
        self.IMInterface().VerifyIsConnected()
    
    def RequestQuote(self):
        try:
            if not self.requestButtonClicked:
                self.requestButtonClicked = True
                self.SetReplyTime()
                self.SetNegotiationTime()
                self.IMInterface().SetCustomDict(self.CreateCustomDict())
                self.IMInterface().RequestQuote()
        except Exception as e:
            self.requestButtonClicked = False
    
    def SendOrder(self):
        try:
            if not self.requestButtonClicked:
                self.requestButtonClicked = True
                self.SetReplyTime()
                self.SetNegotiationTime()
                self.IMInterface().SetCustomDict(self.CreateCustomDict())
                self.IMInterface().SendOrder()
        except Exception as e:
            self.requestButtonClicked = False
    
    def OnRequestQuote(self, *args):
        self.CheckValidToSendQuoteRequest()
        self.RequestQuote()
    
    def OnSendOrder(self, *args):
        self.CheckValidToSendQuoteRequest()
        self.SendOrder()
        
    def OnNewTrade(self, *args):
        self.tradeCreationSetting = TradeCreation.CreateNewTrade(self.IsRFQOnDealPackage())
        self.OnNewQuoteRequest()
    
    def OnNewInsAndTrade(self, *args):
        self.tradeCreationSetting = TradeCreation.CreateNewInsAndTrade(self.IsRFQOnDealPackage())
        self.OnNewQuoteRequest()
                
    def OnNewQuoteRequest(self, *args):
        valueDict = self.RememberTraitValues()
        self.CreateNewQuoteRequest()
        self.RestoreTraitValues(valueDict)
        self.requestButtonClicked = False
        self.limitsChecked = False
        self.CreateInvestmentDeciderDict()
        self.UpdateTradeSettingChoices()

    def OnWithdrawQuoteRequest(self, *args):
        self.IMInterface().Withdraw()

    def OnQuoteRequestSendMsg(self, *args):
        self.IMInterface().QuoteRequestSendMsg()

    def OnUpdateQuoteRequest(self, *args):
        self.IMInterface().SetCustomDict(self.CreateCustomDict())
        self.IMInterface().UpdateQuoteRequest()
    
    def AtMarketPriceAction(self, *args):
        self.priceLimit = self._MARKET_PRICE
        
    def AtLimitedPriceAction(self, *args):
        self.priceLimit = 0.0

    '''********************************************************************
    * Labels
    ********************************************************************'''
    def BuyLabel(self, *args):
        return ButtonLabels.ButtonLabels(self.Instrument())[2].upper()
    
    def TwoWayLabel(self, *args):
        return ButtonLabels.ButtonLabels(self.Instrument())[1].upper()
        
    def SellLabel(self, *args):
        return ButtonLabels.ButtonLabels(self.Instrument())[0].upper()

    def SettlementLabel(self, *args):
        return 'Settle (T+' + str(self.Instrument().SpotBankingDaysOffset()) +')'
        
    def IncrementButtonLabel(self, attrName, *args):
        buttonIndex = self.ButtonNameToButtonIndex(attrName)
        label = self.GetNominalIncrement(buttonIndex)[0]
        return label
    
    def QuantityLabel(self, attrName, *args):
        return Amount.QuantityLabel('Quantity', self.RFQDealPackage())
    
    def MinimumQuantityLabel(self, attrName, *args):
        return 'Minimum ' + Amount.QuantityLabel('Quantity', self.RFQDealPackage())
    
    def NewInsAndTradeLabel(self, *args):
        return TradeCreation.CreateNewInsAndTrade(self.IsRFQOnDealPackage())
    
    def NewTradeLabel(self, *args):
        return TradeCreation.CreateNewTrade(self.IsRFQOnDealPackage())
    
    def WithdrawLabel(self, *args):
        return 'Cancel' if not self.isRfq else 'Withdraw'

    '''********************************************************************
    * Transform
    ********************************************************************'''
    def TransformTimeSpan(self, attrName, inputStr, *args):
        return Time.ParseTimeSpan(inputStr)
    
    def DefaultReplyExpiry(self):
        if self.negotiationTimeoutType == RFQTimerDefaultSettings.gtd:
            value = Time.MinExpiry(RFQTimerDefaultSettings.defaultReplyExpiry, self.negotiationExpiry)
        elif self.negotiationTimeoutType == RFQTimerDefaultSettings.timeSpan:
            value = Time.MinExpiry(RFQTimerDefaultSettings.defaultReplyExpiry, self.negotiationTime)
        else:
            value = RFQTimerDefaultSettings.defaultReplyExpiry
        return value
    
    def DefaultNegotiationExpiry(self, value):
        if self.replyTimeoutType == RFQTimerDefaultSettings.gtd:
            value = Time.MaxExpiry(RFQTimerDefaultSettings.defaultNegotiationExpiry, self.replyExpiry)
        elif self.replyTimeoutType == RFQTimerDefaultSettings.timeSpan:
            value = Time.MaxExpiry(RFQTimerDefaultSettings.defaultNegotiationExpiry, self.replyTime)
        return value
    
    def TransformExpiry(self, attrName, inputStr, *args):
        value = inputStr
        defaultValue = self.DefaultReplyExpiry() if attrName == self.PrefixedName('replyExpiry') else self.DefaultNegotiationExpiry(value)
        if acm.Time().PeriodSymbolToDate(inputStr) or Time.ParsePeriod(inputStr):
            value = Time.PeriodToDateTime(inputStr)
        else:
            value = Time.OnlyIfTodayParse(inputStr)
            if not value:
               value = defaultValue
            elif acm.Time.DateTimeToTime(value) <= acm.Time.DateTimeToTime(acm.Time.TimeNow()):
                if acm.Time.AsDate(value) == acm.Time.DateToday():
                    value = acm.Time().DateTimeAdjustPeriod(value, '1d', None, 0)
                else:
                    value = defaultValue
        return value

    '''********************************************************************
    * Tick
    ********************************************************************'''  
    def NominalTick(self, attrName, value, increment):
        return TradingInterface.TickValue(value, increment, TickSizeSettings.NominalTickSize, self.Instrument(), self.TradingInterface())
    
    def PriceTick(self, attrName, value, increment):
        return TradingInterface.TickValue(value, increment, TickSizeSettings.PriceTickSize, self.Instrument(), self.TradingInterface())
        
    '''********************************************************************
    * Enabled
    ********************************************************************'''
    def RequestNotSent(self, *args):
        return False if self.requestButtonClicked else True        
    
    def RFQMode(self, *args):
        return self.isRfq
    
    def RFQModeAndRequestNotSent(self, *args):
        return self.RFQMode() and self.RequestNotSent()
    
    def OrderModeAndRequestNotSent(self, *args):
        return not self.RFQMode() and self.RequestNotSent()
        
    def CommentEntered(self, *args):
        return self.comment != ''

    def RequestEnabled(self, *args):
        return self.NominalAndClientSpecified() 
    
    def CheckLimitsEnabled(self, *args):
        return self.NominalAndClientSpecified()
    
    def NominalAndClientSpecified(self, *args):
        return self.requestedNominal >= 0.0 and self.client != None 
    
    def TradeSettingEnabled(self, *args):
        checkLimitsRequired = Limits.CheckLimitsRequired(self.Trade(), self.RFQDealPackage())
        return self.RequestNotSent() and (not checkLimitsRequired or not self.limitsChecked)

    '''********************************************************************
    * Visible
    ********************************************************************'''
    def CheckLimitsVisible(self, *args):
        return self.RequestNotSent() and Limits.CheckLimitsRequired(self.Trade(), self.RFQDealPackage()) and not self.limitsChecked
        
    def RequestVisible(self, *args):
        return self.RFQMode() and self.RequestNotSent() and (self.limitsChecked or not Limits.CheckLimitsRequired(self.Trade(), self.RFQDealPackage()))
    
    def SendOrderVisible(self, *args):
        return not self.RFQMode() and self.RequestNotSent() and (self.limitsChecked or not Limits.CheckLimitsRequired(self.Trade(), self.RFQDealPackage()))
    
    def TradeSettingVisible(self, *args):
        dpType = self.RFQDealPackage().DefinitionName() if self.RFQDealPackage() else None
        visible = TradeCreation.SettingVisibleInDialog(self.Instrument().InsType(), dpType)
        return (visible and self.RequestNotSent()) if self.IsShowModeDetail() else False
        
    def RFQInitiated(self, *args):
        return self.QRData().QuoteRequestStatus() != ''
    
    def SalesPortfolioVisible(self, *args):
        return self.isRfq and self.RequestNotSentAndShowModeDetail2()
        
    def RequestNotSentAndShowModeDetail2(self, *args):
        visible = self.RequestNotSent()
        if visible:
            visible = self.IsShowModeDetail()
        return visible
    
    def NewTradeActionVisible(self, *args):
        return self.NewRequestValid() and TradeCreation.CreateNewTrade(self.IsRFQOnDealPackage()) in TradeCreationUtil.ValidTradeCreationChoices(self.Trade(), self.RFQDealPackage())
    
    def NewInsAndTradeActionVisible(self, *args):
        return self.NewRequestValid() and TradeCreation.CreateNewInsAndTrade(self.IsRFQOnDealPackage()) in TradeCreationUtil.ValidTradeCreationChoices(self.Trade(), self.RFQDealPackage())

    def NewRequestValid(self, *args):
        status = self.QRData().QuoteRequestStatus()
        return status in [Status.passed, Status.rejected, Status.cancelled, Status.noAnswer, Status.expired, Status.accepted] and not self.UpdateOrWithdrawRequired()
    
    def RequestActionsVisible(self, *args):
        return self.RequestNotSent() or self.QuoteRequestSendMsgValid() or self.UpdateRequestValid() or self.QuoteRequestWithdrawValid()
    
    def UpdateOrWithdrawRequired(self):
        return self.QRData().UpdateOrWithdrawRequired()

    def UpdateRequestValid(self, *args):
        valid = False
        status = self.QRData().QuoteRequestStatus()
        if status in [Status.firm, Status.subject, Status.stream] or self.UpdateOrWithdrawRequired():
            valid = True
        return valid

    def QuoteRequestSendMsgValid(self, *args):
        status = self.QRData().QuoteRequestStatus()
        return status in [Status.pending, Status.countered] and not self.UpdateRequestValid()

    def QuoteRequestWithdrawValid(self, *args):
        status = self.QRData().QuoteRequestStatus()
        return status in [Status.pending, Status.subject, Status.firm, Status.subjAccept, Status.stream] or self.UpdateOrWithdrawRequired()
    
    def ReplyTimeVisible(self, *args):
        return self.RequestNotSent() and self.replyTimeoutType == RFQTimerDefaultSettings.timeSpan and self.IsShowModeDetail()
    
    def ReplyExpiryVisible(self, *args):
        return self.RequestNotSent() and self.replyTimeoutType == RFQTimerDefaultSettings.gtd and self.IsShowModeDetail()
        
    def NegotiationTimeVisible(self, *args):
        return self.RequestNotSent() and self.negotiationTimeoutType == RFQTimerDefaultSettings.timeSpan and self.IsShowModeDetail()
    
    def NegotiationExpiryVisible(self, *args):
        return self.RequestNotSent() and self.negotiationTimeoutType == RFQTimerDefaultSettings.gtd and self.IsShowModeDetail()
        
    def QuantityVisible(self, *args):
        return self.RequestNotSent() and Amount.UseQuantity(self.Instrument(), self.RFQDealPackage())
    
    def NominalVisible(self, *args):
        return self.RequestNotSent() and not Amount.UseQuantity(self.Instrument(), self.RFQDealPackage())
    
    def NomInQuotVisible(self, *args):
        return self.RequestNotSentAndShowModeDetail2() and Amount.NomInQuotRelevant(self.Instrument(), self.RFQDealPackage())
    
    def MinimumQuantityVisible(self, *args):
        return not self.isRfq and self.QuantityVisible()
    
    def MinimumNominalVisible(self, *args):
        return not self.isRfq and self.NominalVisible()
    
    def MinimumNomInQuotVisible(self, *args):
        return not self.isRfq and self.NomInQuotVisible()
    
    '''********************************************************************
    * Initial focus
    ********************************************************************'''
    def InitialFocus(self, attrName, *args):
        initialFocus = False
        if attrName == self.PrefixedName('requestedQuantity') and self.QuantityVisible():
            initialFocus = True
        elif attrName == self.PrefixedName('requestedNominal') and self.NominalVisible():
            initialFocus = True
        return initialFocus
        
    '''********************************************************************
    * On Changed
    ********************************************************************'''  
    def OnClientChanged(self, *args):
        self.ResetLimitChecks()
        self.UpdateInvestmentDeciderChoices()
        
    def ResetLimitChecks(self, *args):
        self.limitsChecked = False
        
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

    '''********************************************************************
    * Validate 
    ********************************************************************'''
    def RaiseReplyTimeCannotBeLargerThanExpiry(self):
        raise DealPackageUserException('Reply time cannot be larger than the total expiry time.')
    
    def ValidateNominal(self, name, value):
        Validation.InstrumentIsExpired(self.Instrument())
        Validation.Nominal(value, self.Instrument(), 'Nominal')
    
    def ValidateQuantity(self, name, value):
        Validation.InstrumentIsExpired(self.Instrument())
        Validation.Nominal(self.QRData().QuantityToNominal(value), self.Instrument(), self.QuantityLabel(''))
    
    def ValidateMinimumNominal(self, name, value):
        Validation.MinimumAmount(value, self.requestedNominal, 'Nominal')
    
    def ValidateMinimumQuantity(self, name, value):
        Validation.MinimumAmount(value, self.requestedQuantity, self.QuantityLabel(''))
    
    def ValidateReplyExpiry(self, name, value):
        if self.NegotiationTimeOrExpiry() != 0 and Time.Compare(value, self.NegotiationTimeOrExpiry()):
            self.RaiseReplyTimeCannotBeLargerThanExpiry()
    
    def ValidateReplyTime(self, name, value):
        if value < 0:
            raise DealPackageUserException('Reply time cannot be negative.')
        elif self.negotiationTimeoutType == RFQTimerDefaultSettings.gtd and value > Time.TimeLeft(self.negotiationExpiry):
            self.RaiseReplyTimeCannotBeLargerThanExpiry()
    
    def ValidateNegotiationExpiry(self, name, value):
        if Time.Compare(self.ReplyTimeOrExpiry(), value):
            self.RaiseReplyTimeCannotBeLargerThanExpiry()
    
    def ValidateNegotiationTime(self, name, value):
        if value < 0:
            raise DealPackageUserException('Negotiation time cannot be negative.')
        elif self.replyTimeoutType == RFQTimerDefaultSettings.gtd and value < Time.TimeLeft(self.replyExpiry):
            self.RaiseReplyTimeCannotBeLargerThanExpiry()

    '''********************************************************************
    * Colors
    ********************************************************************'''       
    def GetButtonColor(self, buttonDirection):
        color = Colors.Color(buttonDirection)
        if color.ColorRef() != Direction.Color(self.direction, self.Instrument()).ColorRef():
            color = Colors.Color(buttonDirection + '_Inactive')
        return color
 
    def BuyButtonColor(self, attrName, *args):
        return self.GetButtonColor('Buy')
        
    def TwoSidedButtonColor(self, attrName, *args):
        return self.GetButtonColor('2Way')
        
    def SellButtonColor(self, attrName, *args):
        return self.GetButtonColor('Sell')
        
    def RequestButtonColor(self, attrName, *args):
        return Direction.Color(self.direction, self.Instrument())
    
    '''********************************************************************
    * Fonts
    ********************************************************************'''
    def IncrementButtonFont(self, *args):
        return {}
    
    def UseBoldFont(self, bold):
        return {'bold':bold}
        
    def BuyButtonFont(self, attrName, *args):
        useBoldFont = Direction.IsAsk(self.direction)
        return self.UseBoldFont(useBoldFont)
        
    def TwoSidedButtonFont(self, attrName, *args):
        return self.UseBoldFont(Direction.IsTwoWay(self.direction))

    def SellButtonFont(self, attrName, *args):
        useBoldFont = Direction.IsBid(self.direction)
        return self.UseBoldFont(useBoldFont)
     
    '''********************************************************************
    * Choicelists
    ********************************************************************'''        
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
    
    def TimeoutTypes(self, *args):
        return [RFQTimerDefaultSettings.gtd, RFQTimerDefaultSettings.gtc, RFQTimerDefaultSettings.timeSpan]
    
    def TradeSettingChoices(self, *args):
        if self._tradeSettingChoices.IsEmpty():
            self.UpdateTradeSettingChoices()
        return self._tradeSettingChoices
    
    def UpdateTradeSettingChoices(self):
        try:
            self._tradeSettingChoices.Populate(TradeCreationUtil.ValidTradeCreationChoices(self.Trade(), self.RFQDealPackage()))
        except Exception as e:
            print ('TradeSettingChoices failed', e)
        return []
      
    '''********************************************************************
    * Nominal Buttons
    ********************************************************************'''            
    def CreateNominalIncrementAttributes(self, attributeDict):
        for i in range(0, 6):
            key = 'nominal' + str(i)
            attributeDict[key] = Action( label=self.UniqueCallback('@IncrementButtonLabel'),
                                         action=self.UniqueCallback('@IncrementNominal'),
                                         textFont=self.UniqueCallback('@IncrementButtonFont'),
                                         sizeToFit=True,
                                         tabStop=False,
                                         enabled=self.UniqueCallback('@RequestNotSent'),
                                         visible=self.UniqueCallback('@RequestNotSent'))
            
    def IncrementNominal(self, attrName, *args):
        buttonIndex = self.ButtonNameToButtonIndex(attrName)
        increment = self.GetNominalIncrement(buttonIndex)[1]
        self.requestedNominal += increment
        
    def ButtonNameToButtonIndex(self, buttonName):
        buttonIndex = buttonName.replace(self.PrefixedName('nominal'), '')
        return int(buttonIndex)  
    
    def GetNominalIncrement(self, buttonIndex):
        incrementTuple = 0
        try:
            incrementTuples = self.NominalIncrements()
            if len(incrementTuples) == 6:
                incrementTuple = incrementTuples[buttonIndex]
            else:
                raise DealPackageException('Array of nominal increments must be of length 3')
        except Exception as e:
            raise DealPackageException('Could not interpret nominal increment: ' + str(e))
        return incrementTuple
        
    '''********************************************************************
    * Utils
    ********************************************************************'''    
    def CreateInvestmentDeciderDict(self):
        self._investmentDeciderDict = Misc.FindInvestmentDeciderChoices(self.client)
                
    def CreateNewQuoteRequest(self):
        self.GetMethod(self._createNewQuoteRequest)()
    
    def RememberTraitValues(self):
        valueDict = {}
        valueDict['salesPortfolio'] = self.salesPortfolio
        valueDict['direction'] = self.direction
        valueDict['nominal'] = self.requestedNominal
        valueDict['client'] = self.client
        valueDict['investmentDecider'] = self.investmentDecider
        valueDict['negotiationTimeoutType'] = self.negotiationTimeoutType
        if self.negotiationTimeoutType == RFQTimerDefaultSettings.timeSpan:
            valueDict['negotiationTime'] = self.negotiationTime
        elif self.negotiationTimeoutType == RFQTimerDefaultSettings.gtd:
            valueDict['negotiationExpiry'] = self.negotiationExpiry
        valueDict['replyTimeoutType'] = self.replyTimeoutType
        if self.replyTimeoutType == RFQTimerDefaultSettings.timeSpan:
            valueDict['replyTime'] = self.replyTime
        elif self.replyTimeoutType == RFQTimerDefaultSettings.gtd:
            valueDict['replyExpiry'] = self.replyExpiry
        return valueDict
        
    def RestoreTraitValues(self, valueDict):
        self.salesPortfolio = valueDict['salesPortfolio']
        self.direction = valueDict['direction']
        self.requestedNominal = valueDict['nominal']
        self.client = valueDict['client']
        self.investmentDecider = valueDict['investmentDecider']
        self.negotiationTimeoutType = valueDict['negotiationTimeoutType']
        if self.negotiationTimeoutType == RFQTimerDefaultSettings.timeSpan:
            self.negotiationTime = valueDict['negotiationTime']
        elif self.negotiationTimeoutType == RFQTimerDefaultSettings.gtd:
            self.negotiationExpiry = valueDict['negotiationExpiry']
        self.replyTimeoutType = valueDict['replyTimeoutType']
        if self.replyTimeoutType == RFQTimerDefaultSettings.timeSpan:
            self.replyTime = valueDict['replyTime']
        elif self.replyTimeoutType == RFQTimerDefaultSettings.gtd:
            self.replyExpiry = valueDict['replyExpiry']
    
    def ReplyTimeOrExpiry(self):
        if self.replyTimeoutType == RFQTimerDefaultSettings.gtd:
            timeOrExpiry = self.replyExpiry
        elif self.replyTimeoutType == RFQTimerDefaultSettings.timeSpan:
            timeOrExpiry = self.replyTime
        else:
            timeOrExpiry = 0
        return timeOrExpiry
    
    def NegotiationTimeOrExpiry(self):
        if self.negotiationTimeoutType == RFQTimerDefaultSettings.gtd:
            timeOrExpiry = self.negotiationExpiry
        elif self.negotiationTimeoutType == RFQTimerDefaultSettings.timeSpan:
            timeOrExpiry = self.negotiationTime
        else:
            timeOrExpiry = 0
        return timeOrExpiry

    def SetReplyTime(self):
        if self.replyTimeoutType == RFQTimerDefaultSettings.gtd:
            self.replyTime = Time.TimeLeft(self.replyExpiry)
        elif self.replyTimeoutType == RFQTimerDefaultSettings.gtc:
            self.replyTime = 0
        
    def SetNegotiationTime(self):
        if self.negotiationTimeoutType == RFQTimerDefaultSettings.gtd:
            self.negotiationTime = Time.TimeLeft(self.negotiationExpiry)
        elif self.negotiationTimeoutType == RFQTimerDefaultSettings.gtc:
            self.negotiationTime = 0
    
    def IsCustomAmount(self):
        return Amount.IsCustomAmount(self.RFQDealPackage())
        
    def Refresh(self):
        if self.RequestNotSent() and self.IsCustomAmount():
            self.SetAttribute('requestedQuantity', 1, silent=True)
    
    def CreateCustomDict(self):
        def SetObjectsToQuote(objectsToQuote, quoteOnlyInstrumentPart):
            tradingQRData = self.QRData().TradingQuoteRequestsData()
            for componentName in tradingQRData.Components().Keys():
                objectToQuote = tradingQRData.ObjectToQuoteAt(componentName, quoteOnlyInstrumentPart)
                objectsToQuote.AtPut(componentName, objectToQuote)
                
        return TradeCreationUtil.CreateCustomDict(self.RFQDealPackage(),
                                                  self.IsRFQOnDealPackage(),
                                                  self.Trade(), 
                                                  self.tradeCreationSetting, 
                                                  self.CustomAttributesAttr(),
                                                  SetObjectsToQuote)
    
    def OnRequestQuoteComplete(self, customerQuoteRequestInfo):
        try:
            TradeCreationUtil.TagTradesIfNecessary(self.Trade(), self.RFQDealPackage(), 'QuoteRequestId', customerQuoteRequestInfo.Id(), self.tradeCreationSetting, self.IsRFQOnDealPackage())
        except Exception as e:
            print ("OnRequestQuoteComplete failed", e)
    
    def OnSendOrderComplete(self, orderHandler):
        pass
    
    '''********************************************************************
    * Default values
    ********************************************************************'''
    def SetDefaultTimeoutTypes(self):
        self.negotiationTimeoutType = RFQTimerDefaultSettings.defaultNegotiationTimeoutType
        self.replyTimeoutType = RFQTimerDefaultSettings.defaultReplyTimeoutType

    def SetDefaultReplyTime(self):
        if self.replyTimeoutType == RFQTimerDefaultSettings.gtd:
            self.replyExpiry = RFQTimerDefaultSettings.defaultReplyExpiry
        elif self.replyTimeoutType == RFQTimerDefaultSettings.timeSpan:
            self.replyTime = RFQTimerDefaultSettings.defaultReplyTime
    
    def SetDefaultNegotationTime(self):
        if self.negotiationTimeoutType == RFQTimerDefaultSettings.gtd:
            self.negotiationExpiry = RFQTimerDefaultSettings.defaultNegotiationExpiry
        elif self.negotiationTimeoutType == RFQTimerDefaultSettings.timeSpan:
            self.negotiationTime = RFQTimerDefaultSettings.defaultNegotiationTime
    
    def SetDefaultValues(self):
        self.salesPortfolio = self.CustomAttributeMethod('DefaultSalesPortfolio')()
        self.toTrader = self.CustomAttributeMethod('DefaultTrader')()
    
    def SetDefaultNegotiationAndReplyTime(self):
        self.SetDefaultTimeoutTypes()  
        self.SetDefaultNegotationTime()
        self.SetDefaultReplyTime()
        
        
