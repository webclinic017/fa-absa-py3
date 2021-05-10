import acm
from DealPackageDevKit import CompositeAttributeDefinition
from DealPackageDevKit import Box, Label, Action, UXDialogsWrapper
from RFQUtils import Direction, Time, Amount, Open, Misc

from TradeCreationUtil import TradeCreation

class RFQTopPanel(CompositeAttributeDefinition):
    def Attributes(self):
        attributes = {}
        
        attributes.update({
                'insNameLabel'          : Label(  label=self.UniqueCallback('@TopNameLabel'),
                                                  labelFont=self.UniqueCallback('@Arial15'),
                                                  alignment='Center',   
                                                  backgroundColor=self.UniqueCallback('@InstrumentTopPanelColor'), 
                                                  visible=self.UniqueCallback('@InstrumentPartVisible'),
                                                  width=540),  
            
                'panel'                 : Box(    label='',
                                                  vertical=False,
                                                  backgroundColor=self.UniqueCallback('@TopPanelColor')),
                                                  
                'insPanel'              : Box(    label='',
                                                  vertical=True,
                                                  backgroundColor=self.UniqueCallback('@InstrumentTopPanelColor'), 
                                                  visible=self.UniqueCallback('@InstrumentPartVisible')),
                                                  
                'amountLabel'           : Label(  label=self.UniqueCallback('@TopAmountLabel'),
                                                  labelFont=self.UniqueCallback('@LabelFont'),
                                                  backgroundColor=self.UniqueCallback('@TopPanelColor'),      
                                                  width=200),  
                                                  
                'quotationLabel'        : Label(  label=self.UniqueCallback('@TopQuotationLabel'),
                                                  labelFont=self.UniqueCallback('@LabelFont'),
                                                  backgroundColor=self.UniqueCallback('@TopPanelColor'),      
                                                  width=200),  
                                     
                'directionLabel'        : Label(  label=self.UniqueCallback('@TopDirectionLabel'),
                                                  labelFont=self.UniqueCallback('@LabelFont'),
                                                  backgroundColor=self.UniqueCallback('@TopPanelColor'),   
                                                  width=200),   
                                               
                'clientLabel'           : Label(  label=self.UniqueCallback('@TopClientLabel'),
                                                  labelFont=self.UniqueCallback('@LabelFont'),
                                                  backgroundColor=self.UniqueCallback('@TopPanelColor'), 
                                                  alignment='Left',
                                                  width=200),
                
                'insISINLabel'          : Label(  label=self.UniqueCallback('@TopISINLabel'),
                                                  labelFont=self.UniqueCallback('@Arial'),
                                                  visible=self.UniqueCallback('@TopISINVisible'),
                                                  alignment='Center', 
                                                  backgroundColor=self.UniqueCallback('@InstrumentTopPanelColor'),
                                                  width=150),
               
                'instrumentType'        : Label(  label=self.UniqueCallback('@TopPanelInsType'),
                                                  labelFont=self.UniqueCallback('@LabelFont'),
                                                  backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                  width=170),

                #'prices'                : Label(  label=self.UniqueCallback('@TopPricesLabel'),
                #                                  labelFont=self.UniqueCallback('@LabelFont'),
                #                                  backgroundColor=self.UniqueCallback('@TopPanelColor'),      
                #                                  width=170),
                     
                'statusLabel'           : Label(  label=self.UniqueCallback('@TopStatusLabel'),
                                                  labelFont=self.UniqueCallback('@LabelFont'),
                                                  backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                  alignment='Right',      
                                                  width=140),
                
                'customerStatusLabel'   : Label(  label=self.UniqueCallback('@TopCustomerStatusLabel'),
                                                  labelFont=self.UniqueCallback('@LabelFont'),
                                                  backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                  alignment='Left',      
                                                  width=140),
                
                'timeLeftLabel'         : Label(  label=self.UniqueCallback('@TimeLeft'),
                                                  labelFont=self.UniqueCallback('@LabelFont'),
                                                  backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                  alignment='Right',    
                                                  width=140),
                
                'customerTimeLeftLabel' : Label(  label=self.UniqueCallback('@CustomerTimeLeft'),
                                                  labelFont=self.UniqueCallback('@LabelFont'),
                                                  backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                  alignment='Left',    
                                                  width=140),
                                                  
                'toTrader'              : Label(  label=self.UniqueCallback('@ToTraderLabel'),
                                                  labelFont=self.UniqueCallback('@LabelFont'),
                                                  backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                  alignment='Right',         
                                                  width=140), 
                
                'open'                  : Action(   label='Open',
                                                    action=self.UniqueCallback('@OpenEntity'),
                                                    visible=self.UniqueCallback('@OpenVisible')),
                
                'topPanelActions'       : Action(   label='>',
                                                    sizeToFit=True,
                                                    actionList=self.UniqueCallback('@TopPanelActions'),
                                                    visible=self.UniqueCallback('@InstrumentPartVisible')),
                
                'connectedTradesViewer' : Action(   dialog=self.UniqueCallback('@ConnectedTradesViewer'))

                                                  
        })
                        
        return attributes
        
    '''********************************************************************
    * Deal Definition
    ********************************************************************'''    
    def OnInit(self, timeLeft, customerTimeLeft, status, customerStatus, tradeCreationSetting, topPanelActions, customerQuoteRequestInfoMethod, requestSent, **kwargs):
         self._qrData = kwargs['qrDataMethod']
         self._instrument = kwargs['instrumentMethod']
         self._dealPackage = kwargs['dealPackageMethod']
         self._isRfqOnDealPackage = kwargs['isRfqOnDealPackageMethod']
         self._trade = kwargs['tradeMethod']
         self._timeLeft = timeLeft
         self._customerTimeLeft = customerTimeLeft
         self._status = status
         self._customerStatus = customerStatus
         self._tradeCreationSetting = tradeCreationSetting
         self._topPanelActions = topPanelActions
         self._customerQuoteRequestInfo = customerQuoteRequestInfoMethod
         self._requestSent = requestSent
         
    '''********************************************************************
    * Object Mappings
    ********************************************************************'''    
                
    def Instrument(self):
        return self.GetMethod(self._instrument)()
    
    def RFQDealPackage(self):
        return self.GetMethod(self._dealPackage)()
    
    def IsRFQOnDealPackage(self):
        return self.GetMethod(self._isRfqOnDealPackage)()
    
    def Trade(self):
        return self.GetMethod(self._trade)()

    def QRData(self):
        return self.GetMethod(self._qrData)()

    def Direction(self):
        return self.QRData().Direction()
    
    def RequestSent(self):
        return self.GetMethod(self._requestSent)()
    
    def CustomerQuoteRequestId(self):
        quoteRequest = self.GetMethod(self._customerQuoteRequestInfo)()
        return quoteRequest.Id() if quoteRequest else None
        
    def QuoteRequestStatus(self):
        return getattr(self.Owner(), self._status)
    
    def CustomerQuoteRequestStatus(self):
        return getattr(self.Owner(), self._customerStatus)
        
    def RequestedNominal(self):
        return self.QRData().RequestedNominal()
    
    def RequestedQuantity(self):
        return self.QRData().RequestedQuantity()
    
    def RequestedNomInQuot(self):
        return self.QRData().RequestedNomInQuot()
        
    def TimeLeft(self, *args):
        return getattr(self.Owner(), self._timeLeft)()
    
    def CustomerTimeLeft(self, *args):
        return Time.SecondsSpanFormat(getattr(self.Owner(), self._customerTimeLeft)())
    
    def TradeCreationSetting(self):
        return self.GetMethod(self._tradeCreationSetting)()
        
    '''********************************************************************
    * Labels
    ********************************************************************'''
    def TopStatusLabel(self, *args):
        return str(self.QuoteRequestStatus())
    
    def TopCustomerStatusLabel(self, *args):
        return str(self.CustomerQuoteRequestStatus())

    def TopClientLabel(self, *args):
        return self.QRData().ClientName()
    
    def TopISINLabel(self, *args):
        if self.IsRFQOnDealPackage():
            isin  = ''
        else:
            isin = self.Instrument().Isin()
        return isin
    
    def TopPanelInsType(self, *args):
        if self.IsRFQOnDealPackage():
            type = self.RFQDealPackage().DefinitionName()
        else:
            type = self.Instrument().InsType()
        return type
        
    def TopNameLabel(self, *args):
        if self.IsRFQOnDealPackage():
            name = self.RFQDealPackage().InstrumentPackage().Name()
        else:
            name = self.Instrument().Name()
        return name
    
    def TopAmountLabel(self, *args):
        return Amount.TopAmountLabel(self.RequestedNomInQuot(), self.RFQDealPackage())
        
    def TopQuotationLabel(self, *args):
        return Amount.QuotationLabel(self.Instrument(), self.RFQDealPackage())
    
    def TopDirectionLabel(self, *args):
        return Direction.Label(self.Direction(), self.Instrument())
        
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
     
    def ToTraderLabel(self, *args):
        trader = self.QRData().ToTrader()
        return trader.Name() if trader else ''
        
        
    '''********************************************************************
    * Fonts
    ********************************************************************'''
    def Arial(self, *args):
        return {'font':'Arial'}
        
    def Arial15(self, *args):
        return {'font':'Arial', 'bold':False, 'italic':False, 'size':14}
    
    def LabelFont(self, *args):
        return {'font':'Arial', 'bold':False, 'italic':False, 'size':12}

    '''********************************************************************
    * Colors
    ********************************************************************'''        
    def TopPanelColor(self, *args):
        return Direction.Color(self.Direction(), self.Instrument())
        
    def InstrumentTopPanelColor(self, *args):
        return Direction.Color(self.Direction(), self.Instrument())
    
    '''********************************************************************
    * Visible
    ********************************************************************'''
    def OpenVisible(self, *args):
        isCreateNewInsAndTrade = self.TradeCreationSetting() == TradeCreation.CreateNewInsAndTrade(self.IsRFQOnDealPackage())
        return Open.OpenButtonVisible(self.RFQDealPackage(), self.Instrument(), self.RequestSent(), isCreateNewInsAndTrade)
               
    def TopISINVisible(self, *args):
        return self.InstrumentPartVisible() and self.insISINLabel and len(self.insISINLabel)
        
    def InstrumentPartVisible(self, *args):    
        return self.insNameLabel and len(self.insNameLabel)
        
    '''********************************************************************
    * Actions
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
        return Open.OpenEntity(self.RFQDealPackage(),
                        self.Trade(),
                        self.TradeCreationSetting() in [TradeCreation.CreateNewInsAndTrade(self.IsRFQOnDealPackage()), TradeCreation.CreateNewTrade(self.IsRFQOnDealPackage())],
                        'QuoteRequestId', 
                        self.CustomerQuoteRequestId(),
                        self.StartApplication,
                        self.OpenConnectedTradesViewer)
    
    def TopPanelActions(self, *args):
        actions = [self.PrefixedName('open')]
        topPanelActions = self.GetMethod(self._topPanelActions)()
        actions.extend(topPanelActions)
        return actions
    
    def ConnectedTradesViewer(self, attrName, taggedTrades):
        return UXDialogsWrapper(acm.DealCapturing().UX().ConnectedTradesViewerDialog, taggedTrades)
