import acm
from QuoteRequestReplyComposite import QuoteRequestReplyCompositeDefinition
from DealPackageDevKit import Object, Action, Box, Label, CalcVal, UXDialogsWrapper

from RFQUtils import Misc, Amount, Open, QuoteRequest, Direction

from SalesTradingCustomizations import ButtonLabels

class QuoteRequestReplyCompositeDefinitionOverride(QuoteRequestReplyCompositeDefinition):
    def Attributes(self):
        attributes = {}
        
        ''' Attributes from base class '''
        attributes.update(super(QuoteRequestReplyCompositeDefinitionOverride, self).Attributes())
        
        ''' Instrument Top Panel '''
        attributes.update({
                'insTopPanel'                   : Box(      label='',
                                                            vertical=True,
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor')),
                                                            
                'instrumentOrDealPackageName'   : Label(    label=self.UniqueCallback('@InstrumentName'),
                                                            labelFont=self.UniqueCallback('@FontArial14'),
                                                            alignment='Center',
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            width=540),    
                
                'requestType'                   : Label(    label=self.UniqueCallback('@RequestType'),
                                                            labelFont=self.UniqueCallback('@FontArial14'),
                                                            alignment='Left',
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            width=100),
                
                                                            
                'open'                          : Action(   label='Open',
                                                            action=self.UniqueCallback('@OpenEntity'),
                                                            visible=self.UniqueCallback('@OpenVisible')),
                
                'topPanelActions'               : Action(   label='>',
                                                            sizeToFit=True,
                                                            actionList=self.UniqueCallback('@TopPanelActions'))
        })
        
        
        
        ''' Top Panel '''
        attributes.update({
                'direction'                     : Label(    label=self.UniqueCallback('@DirectionLabel'),
                                                            labelFont=self.UniqueCallback('@FontArial12'),
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            width=180),
                                                            
                'requestedAmount'               : Label(    label=self.UniqueCallback('@RequestedAmount'),
                                                            labelFont=self.UniqueCallback('@FontArial12'),
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            width=180),     

                'quotation'                     : Label(    label=self.UniqueCallback('@QuotationLabel'),
                                                            labelFont=self.UniqueCallback('@FontArial12'),
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            width=180),
                                                            
                'instrumentType'                : Label(    label=self.UniqueCallback('@InstrumentType'),
                                                            labelFont=self.UniqueCallback('@FontArial12'),
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            alignment='Right',
                                                            width=230),
                                                            
                'assignedToTrader'              : Label(    label=self.UniqueCallback('@AssignedToTraderLabel'),
                                                            labelFont=self.UniqueCallback('@FontArial12'),
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            alignment='Right',
                                                            width=130),

                'sendingBroker'                 : Label(    label=self.UniqueCallback('@GetFromDataSource'),
                                                            _dataSourceColumn = 'Quote Request Sending Broker /QRR',
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            labelFont=self.UniqueCallback('@FontArial12'),
                                                            width=180),

                'timeLeftLabel'                 : Label(    label=self.UniqueCallback('@TimeLeftLabel'),
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            labelFont=self.UniqueCallback('@FontArial12'),
                                                            alignment='Left',
                                                            width=130),
                                                            
                'quoteRequestStatus'            : Label(    label=self.UniqueCallback('@GetFromDataSource'),
                                                            _dataSourceColumn = 'Quote Request Status /QRR',
                                                            labelFont=self.UniqueCallback('@FontArial12'),
                                                            backgroundColor=self.UniqueCallback('@TopPanelColor'),
                                                            width=130,
                                                            alignment='Left'),     
                
                'connectedTradesViewer'         : Action(   dialog=self.UniqueCallback('@ConnectedTradesViewer'))
        })
        
        return attributes


    def OnInit(self, quoteControllerName, tradeMethodName, qrrDealPackageName, **kwargs):
        super(QuoteRequestReplyCompositeDefinitionOverride, self).OnInit(quoteControllerName, tradeMethodName, qrrDealPackageName)
            
    '''********************************************************************
    * Label Methods
    ********************************************************************'''
    def InstrumentName(self, *args):
        name = self.Instrument().Name()
        if self.QRRDealPackage() and not self.QRRDealPackage().IsDeal():
            name = self.QRRDealPackage().InstrumentPackage().Name()
        return name
    
    def RequestType(self, *args):
        return 'Order' if self.QuoteRequest() and self.QuoteRequest().Origin() == 'Order' else 'Quote Request'
            
    def DirectionLabel(self, *args):
        constraint = self.QuoteRequestReply().Constraint()
        opposite=Direction.Opposite(constraint)
        label = Direction.Label(opposite, self.Instrument())
        return label  
        
    def QuotationLabel(self, *args):
        return Amount.QuotationLabel(self.Instrument(), self.QRRDealPackage())
            
    def RequestedQuantity(self, *args):
        return self.QuoteController().CreateDataSource('Quote Requested Quantity /QRR').Get()

    def RequestedNomInQuot(self, *args):
        return self.QuantityToNomInQuot(self.RequestedQuantity())

    def RequestedAmount(self, *args):
        return Amount.TopAmountLabel(self.RequestedNomInQuot(), self.QRRDealPackage())
        
    def InstrumentType(self, *args):
        if self.QRRDealPackage():
            type = self.QRRDealPackage().DefinitionName()
        else:
            type = self.Instrument().InsType()
        return type
        
    def AssignedToTraderLabel(self, *args):
        return self.QuoteRequest().ToBrokerId()
    
    def CustomerQuoteRequestId(self):
        customerQuoteRequest = QuoteRequest.GetCustomerQuoteRequestFromQuoteRequest(self.QuoteRequest())
        customerQuoteRequestId = customerQuoteRequest.Id() if customerQuoteRequest else None
    
    '''********************************************************************
    * Visibility Methods
    ********************************************************************'''
    def OpenVisible(self, *args):
        return Open.OpenButtonVisible(self.QRRDealPackage(), self.Instrument())
    
    '''********************************************************************
    * Action Methods
    ********************************************************************'''
    def TopPanelActions(self, *args):
        actions = [self.PrefixedName('open')]
        topPanelActions = self.customAttributes.TopPanelActions()
        actions.extend(topPanelActions)
        return actions
    
    def StartApplication(self, appName, obj):
        startAppCb = self.Owner().GetAttribute('uxCallbacks').At('startApplication')
        if startAppCb:
            startAppCb(appName, obj)
    
    def OpenConnectedTradesViewer(self, taggedTrades):
        dialogCb = self.Owner().GetAttribute('uxCallbacks').At('dialog')
        if dialogCb:
            dialogCb(self.Owner().DealPackage(), self.PrefixedName('connectedTradesViewer'), taggedTrades)
        
    def OpenEntity(self, *args):
        Open.OpenEntity(self.QRRDealPackage(),
                        self.Trade(),
                        False,
                        'QuoteRequestId', 
                        self.CustomerQuoteRequestId(),
                        self.StartApplication,
                        self.OpenConnectedTradesViewer,
                        False)
    
    def ConnectedTradesViewer(self, attrName, taggedTrades):
        return UXDialogsWrapper(acm.DealCapturing().UX().ConnectedTradesViewerDialog, taggedTrades)


    '''********************************************************************
    * Font Methods
    ********************************************************************'''
    def FontArial14(self, *args):
        return {'font':'Arial', 'bold':False, 'italic':False, 'size':14}


   # Attribute override
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
                            {'instrumentISIN'       : dict(alignment='Center')})
                                

    def SendQuoteRequestReplyButtonLabel(self, *args):
            label = 'Send'
            constraint = self.QuoteRequestReply().Constraint()
            if constraint == 'Ask':
                label = 'You '+ButtonLabels.ButtonLabels(self.Instrument())[0]
            elif constraint == 'Bid':
                label = 'You '+ButtonLabels.ButtonLabels(self.Instrument())[2]
            return label
                            

