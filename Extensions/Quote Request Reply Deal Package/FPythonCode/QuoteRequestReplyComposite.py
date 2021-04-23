from __future__ import print_function
import acm
from DealPackageDevKit import CompositeAttributeDefinition, Object, Str, Action, Box, Label, CalcVal, ReturnDomainDecorator
from QuoteRequestReply import ignore_and_send, send_reply_with_unfirm_alert, send_reply_without_unfirm_alert, stop_unfirm_alert, take_countered_price

from QuoteRequestReplyCustomizations import QuoteRequestReplyCustomDefinition
from QuoteRequestReplyUtil import TimeFormatting, TradingInterface, TickSizeSettings, Amount, MethodDirection


class QuoteRequestReplyColors(object):
    background = acm.Get('Colors/Silver')
    red = acm.Get('Colors/Red')
    darkRed = acm.Get('Colors/DarkRed')
    grey = acm.Get('Colors/Grey')
    blue = acm.Get('Colors/Blue')
    lightBlue = acm.Get('Colors/LightBlue')
    white = acm.Get('Colors/White')
    
def QRROnTimeLeftTimerTick(pSelf, *args):
    try:
        if pSelf.QuoteController():
            pSelf.timeLeft = pSelf.GetFromDataSourceImpl(pSelf.QuoteController(), 'Quote Request Reply Time Left')
        pSelf.RegisterTimeLeftTicker()
    except Exception as e:
        print ('QRR Timer Tick failure: ', e)
            
class QuoteRequestReplyCompositeDefinition(CompositeAttributeDefinition):
    def Attributes(self):
        attributes = {}
        ''' Top Panel Labels '''
        attributes.update({
                'topPanel': Box(      label='',
                                                            vertical=False,
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor')),

                'quoteRequestOrigin': Label(    label=self.UniqueCallback('@GetFromDataSource'),
                                                            _dataSourceColumn = 'Quote Request Origin /QRR',
                                                            labelFont=self.UniqueCallback('@FontArial13'),
                                                            width=150,
                                                            maxWidth=150),
        
                'marketName': Label(    label=self.UniqueCallback('@GetFromDataSource'),
                                                            _dataSourceColumn = 'Market Name /QRR',
                                                            labelFont=self.UniqueCallback('@FontArial13Bold'),
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            width=250),
        
                'quoteRequestStatus': Label(    label=self.UniqueCallback('@GetFromDataSource'),
                                                            _dataSourceColumn = 'Quote Request Status /QRR',
                                                            labelFont=self.UniqueCallback('@FontArial13Bold'),
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            width=150,
                                                            alignment='Right',
                                                            ),        
                                                            
                'quoteRequestQuantity': Label(    label=self.UniqueCallback('@GetFromDataSource'),
                                                            _dataSourceColumn = 'Quote Requested Quantity /QRR',
                                                            labelFont=self.UniqueCallback('@FontArial13Bold'),
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            formatter='InstrumentDefinitionQuantity',
                                                            width=150,
                                                            maxWidth=150
                                                            ), 
                                                           
                'instrumentName': Label(    label=self.UniqueCallback('@GetFromDataSource'),
                                                            _dataSourceColumn = 'Instrument Name /QRR',
                                                            labelFont=self.UniqueCallback('@FontArial13Bold'),
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            width=540
                                                            ), 
                                                          
                'instrumentISIN': Label(    label=self.UniqueCallback('@GetFromDataSource'),
                                                            _dataSourceColumn = 'ISIN /QRR',
                                                            labelFont=self.UniqueCallback('@FontArial8'),
                                                            visible=self.UniqueCallback('@ISINVisible'),
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            width=150,
                                                            alignment='Right'),
        
        })

        ''' Labels '''
        attributes.update({              
                'sendingCompany': Label(    label=self.UniqueCallback('@GetFromDataSource'),
                                                            _dataSourceColumn = 'Quote Request Sending Company /QRR',
                                                            labelFont=self.UniqueCallback('@FontArial13'),
                                                            maxWidth=100),

                'counterpartyRating': Label(    label=self.UniqueCallback('@GetFromDataSource'),
                                                            _dataSourceColumn = 'Quote Request Counterparty Rating /QRR',
                                                            labelFont=self.UniqueCallback('@FontArial13'),
                                                            maxWidth=100),
                                                            
                'sendingBroker': Label(    label=self.UniqueCallback('@GetFromDataSource'),
                                                            _dataSourceColumn = 'Quote Request Sending Broker /QRR',
                                                            labelFont=self.UniqueCallback('@FontArial12'),
                                                            width=180),
                                                            
                'errorMessagePanel': Box(      label='',
                                                            vertical=False,
                                                            backgroundColor=self.UniqueCallback('@ErrorBackgroundColor')),
                                                            
                'errorMessage': Label(    label=self.UniqueCallback('@GetFromDataSource'),
                                                            _dataSourceColumn = 'Quote Error Message /QRR',
                                                            alignment='Center',
                                                            width=540,
                                                            backgroundColor=self.UniqueCallback('@ErrorBackgroundColor')),

        })
        
        ''' Timers '''
        attributes.update({
                'timeLeft'                      : Str(      label=''),


                'timeLeftLabel'                 : Label(    label=self.UniqueCallback('@TimeLeftLabel'),
                                                            labelFont=self.UniqueCallback('@FontArial32'),
                                                            textColor=self.UniqueCallback('@BlueTextFont'),
                                                            alignment='Right',
                                                            width=250)
        })
        
        ''' Data Source Object Mappings '''
        attributes.update({
                'wireTime': Object(   label='Wire Time',
                                                            objMapping=self.UniqueCallback('WireTime'),
                                                            formatter='SecondsSpan',
                                                            domain='double',
                                                            transform=self.UniqueCallback('@TransformWireTime'),
                                                            editable=self.UniqueCallback('@Editable')),
                                                            
                'settlementDate': Object(   label=self.UniqueCallback('@SettlementDateLabel'),
                                                            objMapping=self.UniqueCallback('SettlementDate'),
                                                            editable = self.UniqueCallback('@Editable')),
                                                            
                'settlementCurrency': Object(   label='Settle Currency',
                                                            domain='FCurrency',
                                                            objMapping=self.UniqueCallback('SettlementCurrency'),
                                                            editable=False,
                                                            width=18,
                                                            maxWidth=18),
                                                            
                'settlementRate': Object(   label='Fx Rate',
                                                            objMapping=self.UniqueCallback('SettlementRate'),
                                                            editable=False,
                                                            width=18,
                                                            maxWidth=18),           
                                                 
                'currency': Object(   label='Currency',
                                                            domain='FCurrency',
                                                            objMapping=self.UniqueCallback('Currency'),
                                                            editable=False),  
                                               
                'coveredPrice': Object(   label='Covered Price',
                                                            domain='double',
                                                            objMapping=self.UniqueCallback('CoveredPrice'),
                                                            editable=False,
                                                            formatter='Price'),
                                                            
                'position': Object(   label='Position',
                                                            domain='double',
                                                            objMapping=self.UniqueCallback('Position'),
                                                            editable=False,
                                                            formatter='Imprecise'),

                'quoteRequestTime': Object(   label='Request Time',
                                                            objMapping=self.UniqueCallback('QuoteRequestTime'),
                                                            editable=False,
                                                            formatter='TimeOnly'),
                                                            
                'messageText': Object(   label='Message',
                                                            editable=False,
                                                            objMapping=self.UniqueCallback('QuoteRequestMessageText')), 

                'replyText': Object(   label='Reply',
                                                            editable = self.UniqueCallback('@Editable'),
                                                            objMapping=self.UniqueCallback('QuoteRequestReplyText')),
                                
                'proposedBidPrice': Object(   label='Bid',
                                                            labelFont=self.UniqueCallback('@Font18'),
                                                            textFont=self.UniqueCallback('@Font18'),
                                                            enabled=self.UniqueCallback('@IsBidOr2Way'),
                                                            transform=self.UniqueCallback('@TransformPrice'),
                                                            objMapping=self.UniqueCallback('ProposedBidPrice'),
                                                            formatter=self.UniqueCallback('@PriceFormatter'),
                                                            editable = self.UniqueCallback('@Editable'),
                                                            tick=self.UniqueCallback('@PriceTick'),
                                                            backgroundColor=self.UniqueCallback('@BidPriceColor')),
                                                            
                'lastQuotedBidPrice': Object(   label='Prev Bid',
                                                            enabled=self.UniqueCallback('@IsBidSide'),
                                                            visible=self.UniqueCallback('@IsCounter'),
                                                            objMapping=self.UniqueCallback('LastBidPrice'),
                                                            formatter=self.UniqueCallback('@PriceFormatter'),
                                                            editable=False),
                                                            
                'counteredBidPrice': Object(   label='Req Bid',
                                                            enabled=self.UniqueCallback('@IsBidSide'),
                                                            visible=self.UniqueCallback('@IsCounter'),
                                                            objMapping=self.UniqueCallback('CounteredBidPrice'),
                                                            formatter=self.UniqueCallback('@PriceFormatter'),
                                                            editable=False),               
                
                'replyBidQuantity': Object(   label='Bid Qty',
                                                            enabled=self.UniqueCallback('@IsBidOr2Way'),
                                                            objMapping=self.UniqueCallback('ReplyBidQuantity'),
                                                            formatter='InstrumentDefinitionQuantity',
                                                            editable = self.UniqueCallback('@Editable'),
                                                            visible=self.UniqueCallback('@QuantityVisible'),
                                                            tick=True),
                
                'replyBidNominal': Object(   label='Bid Nom',
                                                            enabled=self.UniqueCallback('@IsBidOr2Way'),
                                                            objMapping=self.UniqueCallback('ReplyBidNominal'),
                                                            formatter='InstrumentDefinitionNominal',
                                                            editable=self.UniqueCallback('@Editable'),
                                                            visible=self.UniqueCallback('@NominalVisible'),
                                                            tick=self.UniqueCallback('@NominalTick')),
                
                'replyBidNomInQuot': Object(   label='Bid Nom In Quot',
                                                            enabled=self.UniqueCallback('@IsBidOr2Way'),
                                                            objMapping=self.UniqueCallback('ReplyBidNomInQuot'),
                                                            formatter='InstrumentDefinitionNominal',
                                                            editable=self.UniqueCallback('@Editable'),
                                                            visible=self.UniqueCallback('@NomInQuotVisible'),
                                                            tick=self.UniqueCallback('@NominalTick')),
                                             
                'proposedAskPrice': Object(   label='Ask',
                                                            labelFont=self.UniqueCallback('@Font18'),
                                                            textFont=self.UniqueCallback('@Font18'),
                                                            enabled=self.UniqueCallback('@IsAskOr2Way'),
                                                            transform=self.UniqueCallback('@TransformPrice'),
                                                            objMapping=self.UniqueCallback('ProposedAskPrice'),
                                                            formatter=self.UniqueCallback('@PriceFormatter'),
                                                            editable = self.UniqueCallback('@Editable'),
                                                            tick=self.UniqueCallback('@PriceTick'),
                                                            backgroundColor=self.UniqueCallback('@AskPriceColor')),
                                                            
                'lastQuotedAskPrice': Object(   label='Prev Ask',
                                                            enabled=self.UniqueCallback('@IsAskSide'),
                                                            visible=self.UniqueCallback('@IsCounter'),
                                                            objMapping=self.UniqueCallback('LastAskPrice'),
                                                            formatter=self.UniqueCallback('@PriceFormatter'),
                                                            editable=False),
                                                            
                'counteredAskPrice': Object(   label='Req Ask',
                                                            enabled=self.UniqueCallback('@IsAskSide'),
                                                            visible=self.UniqueCallback('@IsCounter'),
                                                            objMapping=self.UniqueCallback('CounteredAskPrice'),
                                                            formatter=self.UniqueCallback('@PriceFormatter'),
                                                            editable=False),
                
                'replyAskQuantity': Object(   label='Ask Qty',
                                                            enabled=self.UniqueCallback('@IsAskOr2Way'),
                                                            objMapping=self.UniqueCallback('ReplyAskQuantity'),
                                                            formatter='InstrumentDefinitionQuantity',
                                                            editable = self.UniqueCallback('@Editable'),
                                                            visible=self.UniqueCallback('@QuantityVisible'),
                                                            tick=True),
                
                'replyAskNominal': Object(   label='Ask Nom',
                                                            enabled=self.UniqueCallback('@IsAskOr2Way'),
                                                            objMapping=self.UniqueCallback('ReplyAskNominal'),
                                                            formatter='InstrumentDefinitionNominal',
                                                            editable=self.UniqueCallback('@Editable'),
                                                            visible=self.UniqueCallback('@NominalVisible'),
                                                            tick=self.UniqueCallback('@NominalTick')),
                
                'replyAskNomInQuot': Object(   label='Ask Nom In Quot',
                                                            enabled=self.UniqueCallback('@IsAskOr2Way'),
                                                            objMapping=self.UniqueCallback('ReplyAskNomInQuot'),
                                                            formatter='InstrumentDefinitionNominal',
                                                            editable=self.UniqueCallback('@Editable'),
                                                            visible=self.UniqueCallback('@NomInQuotVisible'),
                                                            tick=self.UniqueCallback('@NominalTick')),
        })
        
        ''' CalcVals '''
        attributes.update({
                                                            
                'insNominalFactor'              : CalcVal(  calcMapping=self.UniqueCallback('Trade') + ':FTradeSheet:Standard Calculations Instrument Nominal Factor')
        })
        
        ''' Actions '''
        attributes.update({
                                                            
                'sendQuoteRequestReply': Action(   label=self.UniqueCallback('@SendQuoteRequestReplyButtonLabel'),
                                                            action=self.UniqueCallback('@OnSendQuoteRequestReply'),
                                                            enabled=self.UniqueCallback('@SendQuoteRequestReplyButtonEnabled'),
                                                            backgroundColor=self.UniqueCallback('@SendQuoteRequestReplyButtonColor')),
                                                            
                'updatePriceOnRequestReply': Action(   label='Update',
                                                            action=self.UniqueCallback('@OnUpdatePriceOnRequestReply'),
                                                            visible=self.UniqueCallback('@OnUpdatePriceOnRequestReplyVisible'),
                                                            backgroundColor=self.UniqueCallback('@UpdateQuoteRequestButtonColor')),

                'sendReplyWithoutUnfirmAlert': Action(   label=self.UniqueCallback('@SendReplyWithoutUnfirmAlertLabel'),
                                                            action=self.UniqueCallback('@OnSendReplyWithoutUnfirmAlert'),
                                                            enabled=self.UniqueCallback('@SendReplyWithoutUnfirmAlertEnabled')),

                'ignoreAndSend': Action(   label='Ignore breached safety rules & send',
                                                            action=self.UniqueCallback('@OnIgnoreAndSend'),
                                                            enabled=self.UniqueCallback('@IgnoreAndSendEnabled')),

                'stopUnfirmAlert': Action(   label='Stop Monitoring',
                                                            action=self.UniqueCallback('@OnStopUnfirmAlert'),
                                                            enabled=self.UniqueCallback('@StopUnfirmAlertEnabled')),

                'takeCounteredPrice': Action(   label='Take countered price',
                                                            action=self.UniqueCallback('@OnTakeCounteredPrice'),
                                                            enabled=self.UniqueCallback('@TakeCounteredPriceEnabled')),
                
                'additionalSendQuoteActions': Action(   label='>',
                                                            actionList=self.UniqueCallback('@OnAdditionalSendQuoteActions'),
                                                            enabled=self.UniqueCallback('@SendQuoteRequestReplyButtonEnabled'),
                                                            backgroundColor=self.UniqueCallback('@SendQuoteRequestReplyButtonColor'),
                                                            sizeToFit=True),

                'rejectQuoteRequest': Action(   label='Reject',
                                                            action=self.UniqueCallback('@OnRejectQuoteRequest'),
                                                            enabled=self.UniqueCallback('@RejectQuoteRequestButtonEnabled'),
                                                            textColor=self.UniqueCallback('@WhiteTextFont'),
                                                            backgroundColor=self.UniqueCallback('@RejectQuoteRequestButtonColor')),

                'ignoreQuoteRequest': Action(   label='Ignore',
                                                            action=self.UniqueCallback('@OnIgnoreQuoteRequest'),
                                                            enabled=self.UniqueCallback('@IgnoreQuoteRequestButtonEnabled'),
                                                            textColor=self.UniqueCallback('@WhiteTextFont'),
                                                            backgroundColor=self.UniqueCallback('@IgnoreQuoteRequestButtonColor')),

                'excludeQuoteRequestUser': Action(   label='Not Mine',
                                                            action=self.UniqueCallback('@OnExcludeQuoteRequestUser'),
                                                            enabled=self.UniqueCallback('@ExcludeQuoteRequestUserEnabled'),
                                                            textColor=self.UniqueCallback('@WhiteTextFont'),
                                                            backgroundColor=self.UniqueCallback('@ExcludeQuoteRequestUserButtonColor')),
                
                'goToQuoteRequest': Action(   label='Go to RFQ',
                                                            action=self.UniqueCallback('@OnGoToQuoteRequest')),
                                                            
                'deleteQuoteRequest': Action(   label='Off',
                                                            action=self.UniqueCallback('@OnDeleteQuoteRequest'),
                                                            enabled=self.UniqueCallback('@DeleteQuoteRequestButtonEnabled'),
                                                            textColor=self.UniqueCallback('@WhiteTextFont'),
                                                            backgroundColor=self.UniqueCallback('@DeleteQuoteRequestButtonColor')),
        })

        ''' Extension point '''
        attributes.update({
        
                'customAttributes'              : QuoteRequestReplyCustomDefinition(
                                                            instrumentMethod=self.UniqueCallback('Instrument'),
                                                            originalTradeMethodName=self.UniqueCallback('OriginalTrade'),
                                                            dealPackageMethod=self.UniqueCallback('QRRDealPackage'),
                                                            quoteControllerMethod=self.UniqueCallback('QuoteController'))
        })

        return attributes

    '''********************************************************************
    * Deal Misc
    ********************************************************************'''
    def OnInit(self, quoteControllerName, tradeMethodName, qrrDealPackageName, **kwargs):
        self._quoteControllerName = quoteControllerName
        self._tradeMethodName = tradeMethodName
        self._qrrDealPackageName = qrrDealPackageName
        self._timerEvent = None
        
    def OnNew(self):
        self.RegisterTimeLeftTicker()
    
    def OnDismantle(self):
        pass

    '''********************************************************************
    * Object Access Methods
    ********************************************************************'''
    def DealPackage(self):
        return self.GetMethod('DealPackage')()
    
    def Trade(self, *args):
        return self.GetMethod(self._tradeMethodName)()

    def Instrument(self, *args):
        return self.QuoteController().Instrument()
    
    def OriginalTrade(self, *args):
        return self.Trade().Originator()
        
    def QRRDealPackage(self, *args):
        return self.GetMethod(self._qrrDealPackageName)()
        
    def QuoteController(self, *args):
        return self.GetMethod(self._quoteControllerName)()

    def QuoteRequestReply(self, *args):
        return self.QuoteController().QuoteRequestReply()
        
    def TradingInterface(self, *args):
        return self.QuoteController().TradingInterface()

    def QuoteRequest(self, *args):
        return self.QuoteRequestReply().QuoteRequest()
        
    '''********************************************************************
    * Timer
    ********************************************************************'''        
    def RegisterTimeLeftTicker(self):
        self._timerEvent = acm.Time().Timer().CreateTimerEvent(0.25, QRROnTimeLeftTimerTick, self)

    def RemoveTimerEvent(self):
        if self._timerEvent:
            acm.Time().Timer().RemoveTimerEvent(self._timerEvent)
            self._timerEvent = None

    '''********************************************************************
    * Values from Quote Controller Data Source
    ********************************************************************'''
    def GetFromDataSourceImpl(self, controller, columnId):
        try:
            return controller.CreateDataSource(columnId).Get()
        except Exception as e:
            pass
    
    def SetOnDataSourceImpl(self, controller, columnId, value):
        try:
            return controller.CreateDataSource(columnId).Set(value)
        except Exception as e:
            pass
    
    def MappingToDataSource(self, columnId, value='NoInputValue'):
        if value == 'NoInputValue':
            return self.GetFromDataSourceImpl(self.QuoteController(), columnId)
        else:
            self.SetOnDataSourceImpl(self.QuoteController(), columnId, value)
            
    def GetFromDataSource(self, attrName, *args):
        if self.QuoteController():
            columnId = self.DealPackage().GetAttributeMetaData(attrName, '_dataSourceColumn')()
            formatter = self.DealPackage().GetAttributeMetaData(attrName, 'formatter')()
            val = self.GetFromDataSourceImpl(self.QuoteController(), columnId)
            return formatter.Format(val) if formatter else val
            
    '''********************************************************************
    * Object Mappings with Data Source 
    ********************************************************************'''
    def WireTime(self, inputVal = 'NoInputValue'):
        return self.MappingToDataSource('Quote Request Reply Wire Time /QRR', inputVal)  
       
    def SettlementDate(self, inputVal = 'NoInputValue'):
        return self.MappingToDataSource('Quote Request Settlement Date /QRR', inputVal)  
       
    def Currency(self, inputVal = 'NoInputValue'):
        return self.MappingToDataSource('Currency /QRR', inputVal)  
                
    def QuoteRequestTime(self, inputVal = 'NoInputValue'):
        return self.MappingToDataSource('Quote Request Time /QRR', inputVal)  
    
    def SettlementCurrency(self, inputVal = 'NoInputValue'):
        return self.MappingToDataSource('Quote Request Settlement Currency /QRR', inputVal) 

    def SettlementRate(self, inputVal = 'NoInputValue'):
        return self.MappingToDataSource('Quote Request Settlement Rate /QRR', inputVal)
 
    def CoveredPrice(self, inputVal = 'NoInputValue'):
        return self.MappingToDataSource('Quote Request Covered Price /QRR', inputVal) 
        
    def Position(self, inputVal = 'NoInputValue'):
        return self.MappingToDataSource('Portfolio Position /QRR;', inputVal) 
            
    def QuoteRequestMessageText(self, inputVal = 'NoInputValue'):
        return self.MappingToDataSource('Quote Requested Message /QRR', inputVal) 
            
    def QuoteRequestReplyText(self, inputVal = 'NoInputValue'):
        return self.MappingToDataSource('Quote Request Message /QRR', inputVal) 
        
    def ProposedBidPrice(self, inputVal='NoInputValue'):
        return self.MappingToDataSource('Proposed Bid Price /QRR', inputVal)
        
    def LastBidPrice(self, inputVal='NoInputValue'):
        return self.MappingToDataSource('Last Quote Bid Price /QRR', inputVal)  
              
    def CounteredBidPrice(self, inputVal='NoInputValue'):
        return self.MappingToDataSource('Quote Request Countered Price Bid /QRR', inputVal)  
    
    @ReturnDomainDecorator('double')
    def ReplyBidQuantity(self, inputVal='NoInputValue'):
        return self.MappingToDataSource('Proposed Reply Bid Volume /QRR', inputVal)
    
    @ReturnDomainDecorator('double')
    def ReplyBidNominal(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.QuantityToNominal(self.replyBidQuantity)
        else:
            self.replyBidQuantity = self.NominalToQuantity(val)
    
    @ReturnDomainDecorator('double')
    def ReplyBidNomInQuot(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.QuantityToNomInQuot(self.replyBidQuantity)
        else:
            self.replyBidQuantity = self.NomInQuotToQuantity(val)
  
    def ProposedAskPrice(self, inputVal='NoInputValue'):
        return self.MappingToDataSource('Proposed Ask Price /QRR', inputVal)  
    
    def LastAskPrice(self, inputVal='NoInputValue'):
        return self.MappingToDataSource('Last Quote Ask Price /QRR', inputVal)  
       
    def CounteredAskPrice(self, inputVal='NoInputValue'):
        return self.MappingToDataSource('Quote Request Countered Price Ask /QRR', inputVal)  
    
    @ReturnDomainDecorator('double')
    def ReplyAskQuantity(self, inputVal='NoInputValue'):
        return self.MappingToDataSource('Proposed Reply Ask Volume /QRR', inputVal)
    
    @ReturnDomainDecorator('double')
    def ReplyAskNominal(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.QuantityToNominal(self.replyAskQuantity)
        else:
            self.replyAskQuantity = self.NominalToQuantity(val)
    
    @ReturnDomainDecorator('double')
    def ReplyAskNomInQuot(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.QuantityToNomInQuot(self.replyAskQuantity)
        else:
            self.replyAskQuantity = self.NomInQuotToQuantity(val)

    '''********************************************************************
    * Nominal-Quantity Conversions
    ********************************************************************'''  
    def InstrumentNominal(self):
        nominalFactor = self.insNominalFactor.Value() if self.insNominalFactor else 0
        return nominalFactor * self.Instrument().ContractSize()
        
    def NominalToQuantity(self, nominal):
        return Amount.NominalToQuantity(nominal, self.InstrumentNominal())
    
    def QuantityToNominal(self, quantity):
        return Amount.QuantityToNominal(quantity, self.InstrumentNominal())
    
    def NomInQuotToQuantity(self, nomInQuot):
        return Amount.NomInQuotToQuantity(nomInQuot, self.InstrumentNominal(), self.Instrument().Quotation())
    
    def QuantityToNomInQuot(self, quantity):
        return Amount.QuantityToNomInQuot(quantity, self.InstrumentNominal(), self.Instrument().Quotation())
    
    '''********************************************************************
    * Action Methods
    ********************************************************************'''
    def OnAdditionalSendQuoteActions(self, *args):
        return [self.PrefixedName('sendQuoteRequestReply'),
                self.PrefixedName('sendReplyWithoutUnfirmAlert'),
                self.PrefixedName('ignoreAndSend'),
                self.PrefixedName('stopUnfirmAlert'),
                self.PrefixedName('takeCounteredPrice')]
                
    def TopPanelActions(self, *args):
        actions = []
        topPanelActions = self.customAttributes.TopPanelActions()
        actions.extend(topPanelActions)
        return actions
        
    def OnSendQuoteRequestReply(self, *args):
        send_reply_with_unfirm_alert(self.QuoteController().UI()) 
    
    def OnUpdatePriceOnRequestReply(self, *args):
        self.OnSendQuoteRequestReply()
        
    def OnSendReplyWithoutUnfirmAlert(self, *args):
        send_reply_without_unfirm_alert(self.QuoteController().UI()) 
        
    def OnIgnoreAndSend(self, *args):
        ignore_and_send(self.QuoteController().UI())

    def OnStopUnfirmAlert(self, *args):
        stop_unfirm_alert(self.QuoteController().UI())

    def OnTakeCounteredPrice(self, *args):
        take_countered_price(self.QuoteController().UI())

    def OnRejectQuoteRequest(self, *args):
        quoteControllerUI = self.QuoteController().UI()
        quoteControllerUI.RejectQuoteRequest()

    def OnIgnoreQuoteRequest(self, *args):
        quoteControllerUI = self.QuoteController().UI()
        quoteControllerUI.IgnoreQuoteRequest()
    
    def OnGoToQuoteRequest(self, *args):
        acm.MarketMaking.NavigateToQuoteController(self.QuoteController())

    def OnDeleteQuoteRequest(self, *args):
        quoteControllerUI = self.QuoteController().UI()
        quoteControllerUI.DeleteQuote()
        
    def OnExcludeQuoteRequestUser(self, *args):
        quoteControllerUI = self.QuoteController().UI()
        quoteControllerUI.ExcludeQuoteRequestUser()
        
    '''********************************************************************
    * Enabled Methods
    ********************************************************************'''
    def IsDeleted(self):
        return self.QuoteRequest().IsDeleted()
        
    def SendQuoteRequestReplyButtonEnabled(self, *args):
        return self.QuoteRequestReply().CanBeAnswered() and not self.IsDeleted()

    def SendReplyWithoutUnfirmAlertEnabled(self, *args):
        return self.QuoteRequestReply().CanBeAnswered() and not self.IsDeleted()

    def IgnoreAndSendEnabled(self, *args):
        return self.QuoteRequestReply().CanBeAnswered() and not self.IsDeleted()

    def StopUnfirmAlertEnabled(self, *args):
        return self.QuoteRequestReply().IsUnfirmQuoteAlertEnabled() and not self.IsDeleted()

    def TakeCounteredPriceEnabled(self, *args):
        return self.QuoteRequestReply().CanTakeCountered() and not self.IsDeleted()

    def RejectQuoteRequestButtonEnabled(self, *args):
        return self.QuoteRequestReply().CanBeRejected() and not self.IsDeleted()

    def IgnoreQuoteRequestButtonEnabled(self, *args):
        return self.QuoteRequestReply().CanBeIgnored() and not self.IsDeleted()

    def DeleteQuoteRequestButtonEnabled(self, *args):
        return self.quoteRequestStatus in ['On Stream']
        
    def ExcludeQuoteRequestUserEnabled(self, *args):    
        return self.QuoteRequestReply().CanBeExcluded()
        
    '''********************************************************************
    * Editable Methods
    ********************************************************************'''
    def Editable(self, *args):
        try:
            editable = True
            brokerId = self.QuoteRequest().ToBrokerId()
            if brokerId != acm.User().Name() and brokerId != "" and brokerId is not None:
                editable = False
        except:
            pass
        return editable
        
    '''********************************************************************
    * Transform
    ********************************************************************'''
    def TransformWireTime(self, attrName, inputStr, *args):
        transformed = None
        if inputStr and inputStr != '0':
            transformed = TimeFormatting.ParseTimeSpan(inputStr)
        else:
            transformed = -1
        return transformed

    def TransformPrice(self, attrName, inputStr, *args):
        if inputStr == "":
            inputStr = float('NaN')
        return inputStr
        
    '''********************************************************************
    * Label Methods
    ********************************************************************'''
    def SendQuoteRequestReplyButtonLabel(self, *args):
        label = 'Send'
        constraint = self.QuoteRequestReply().Constraint()
        if constraint == 'Ask':
            label = 'You sell'
        elif constraint == 'Bid':
            label = 'You buy'
        return label
    
    def SendReplyWithoutUnfirmAlertLabel(self, *args):
        return self.SendQuoteRequestReplyButtonLabel() + ' & forget'

    def TimeLeftLabel(self, *args):
        time = "    "
        try:
            time = TimeFormatting.SecondsSpanFormat(float(self.timeLeft))
        except:
            pass
        if time is "":
            time = "    "
        return time
        
    def SettlementDateLabel(self, *args):
        return 'Settle (' + str(self.QuoteRequestReply().RelativeSettlementDate()) + ')'

    '''********************************************************************
    * Formatters
    ********************************************************************'''        
    def PriceFormatter(self, *args):
        return acm.FNumFormatter('VeryDetailedShowZeroHideNaN')

    '''********************************************************************
    * Visible
    ********************************************************************'''
    def IsBidOr2Way(self, *args):
        return not self.IsAskSide()

    def IsAskOr2Way(self, *args):
        return not self.IsBidSide()

    def IsBidSide(self, *args):
        return self.QuoteRequestReply().Constraint() == 'Bid'

    def IsAskSide(self, *args):
        return self.QuoteRequestReply().Constraint() == 'Ask'

    def IsCounter(self, *args):
        return self.QuoteRequest().Price() != 0.0
        
    def OnUpdatePriceOnRequestReplyVisible(self, *args):
        return self.DeleteQuoteRequestButtonEnabled()
        
    def ISINVisible(self, *args):
        return self.instrumentISIN and len(self.instrumentISIN)
    
    def QuantityVisible(self, *args):
        return Amount.UseQuantity(self.Instrument(), self.QRRDealPackage())
    
    def NominalVisible(self, *args):
        return not Amount.UseQuantity(self.Instrument(), self.QRRDealPackage())
    
    def NomInQuotVisible(self, *args):
        return Amount.NomInQuotRelevant(self.Instrument(), self.QRRDealPackage()) #and self.IsShowModeDetail()
        
    '''********************************************************************
    * Background Colors
    ********************************************************************'''
    def ColorFromDirection(self):
        colorName = 'TwoWayColor'
        constraint = self.QuoteRequestReply().Constraint()
        if constraint == 'Ask':
            colorName = 'SellColor'
        elif constraint == 'Bid':
            colorName = 'BuyColor'    
        return self.CreateColor(colorName) 

    def TopPanelColor(self, *args):
        return self.ColorFromDirection()
        
    def InstrumentTopPanelColor(self, *args):
        return self.ColorFromDirection()

    def CreateColor(self, name):
        color = acm.GetDefaultContext().GetExtension('FColor', acm.FColor, name)
        return color.Value()

    def SendQuoteRequestReplyButtonColor(self, *args):
        return self.ColorFromDirection()

    def RejectQuoteRequestButtonColor(self, *args):
        return QuoteRequestReplyColors.darkRed

    def IgnoreQuoteRequestButtonColor(self, *args):
        return QuoteRequestReplyColors.grey

    def DeleteQuoteRequestButtonColor(self, *args):
        return QuoteRequestReplyColors.blue
        
    def ExcludeQuoteRequestUserButtonColor(self, *args):
        return QuoteRequestReplyColors.blue
        
    def UpdateQuoteRequestButtonColor(self, *args):
        return QuoteRequestReplyColors.lightBlue

    def ErrorBackgroundColor(self, attrName, *args):
        return QuoteRequestReplyColors.red if self.errorMessage else None

    def PriceColor(self, price):
        color = QuoteRequestReplyColors.white
        if acm.Math.IsFinite(price):
            color = self.CreateColor('TwoWayColor')
        return color
            
    def AskPriceColor(self, *args):
        return self.PriceColor(self.proposedAskPrice)
        
    def BidPriceColor(self, *args):
        return self.PriceColor(self.proposedBidPrice)
        
        
    '''********************************************************************
    * Font Color
    ********************************************************************'''
    def WhiteTextFont(self, *args):
        return QuoteRequestReplyColors.white

    def BlueTextFont(self, *args):
        return QuoteRequestReplyColors.blue

    '''********************************************************************
    * Font Methods
    ********************************************************************'''
    def FontArial8(self, *args):
        return {'font':'Arial', 'bold':False, 'italic':False, 'size':8}

    def FontArial13(self, *args):
        return {'font':'Arial', 'bold':False, 'italic':False, 'size':13}

    def FontArial13Bold(self, *args):
        return {'font':'Arial', 'bold':True, 'italic':False, 'size':13}

    def FontArial12(self, *args):
        return {'font':'Arial', 'bold':False, 'italic':False, 'size':12}

    def FontArial32(self, *args):
        return {'font':'Arial', 'bold':False, 'italic':False, 'size':32}
         
    def Font18(self, *args):
        return {'size':'18'}
        
    '''********************************************************************
    * Tick
    ********************************************************************'''  
    def PriceTick(self, attrName, value, increment):
        return TradingInterface.TickValue(value, increment, TickSizeSettings.PriceTickSize, self.Instrument(), self.TradingInterface())
    
    def NominalTick(self, attrName, value, increment):
        return TradingInterface.TickValue(value, increment, TickSizeSettings.NominalTickSize, self.Instrument(), self.TradingInterface())
       
