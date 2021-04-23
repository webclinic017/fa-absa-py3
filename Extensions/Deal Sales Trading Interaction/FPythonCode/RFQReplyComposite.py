import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageUserException
from DealPackageDevKit import Float, Action, Bool, Object, ReturnDomainDecorator
from RFQUtils import PriceAndMarginConversions, Validation, TradingInterface
from RFQUtils import Direction, Status, Time, MethodDirection, Amount
from RFQHistoryUtil import FromRequest

from SalesTradingCustomizations import IsYieldQuoted, ButtonLabels, TickSizeSettings, RFQTimerDefaultSettings

class RFQReply(CompositeAttributeDefinition):
    def Attributes(self):
        attributes = {}
        
        ''' Reply '''
        attributes.update({

                'traderPrice': Object( label='Trader Price',
                                                  objMapping=self.UniqueCallback('TraderPrice'),
                                                  formatter=self.UniqueCallback('@PriceFormatter'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  visible=self.UniqueCallback('@CounterNotVisible'),
                                                  editable=False,
                                                  tick=self.UniqueCallback('@PriceTick')),                  
        
                'salesSpread': Object( label='Sales Spread',
                                                  objMapping=self.UniqueCallback('SalesSpread'),
                                                  formatter=self.UniqueCallback('@SalesSpreadFormatter'),
                                                  editable=self.UniqueCallback('@SpreadEnabled'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  visible=self.UniqueCallback('@CounterNotVisible'),
                                                  tick=self.UniqueCallback('@SalesSpreadTick')),
                
                'marginAmount': Object( label='Margin Amount',
                                                  objMapping=self.UniqueCallback('MarginAmount'),
                                                  formatter=self.UniqueCallback('@PriceFormatter'),
                                                  editable=False,
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  visible=self.UniqueCallback('@CounterNotVisibleInDetails'),
                                                  tick=self.UniqueCallback('@MarginAmountTick')),
                                                  
                'allInPrice': Object( label='All-in Price',
                                                  objMapping=self.UniqueCallback('AllInPrice'),
                                                  formatter=self.UniqueCallback('@PriceFormatter'),
                                                  editable=self.UniqueCallback('@AllInPriceEnabled'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  visible=self.UniqueCallback('@CounterNotVisible'),
                                                  tick=self.UniqueCallback('@PriceTick')),        
        
                                                  
                'traderQuantity': Object( label=self.UniqueCallback('@TraderQuantityLabel'),
                                                  objMapping=self.UniqueCallback('TraderQuantity'),
                                                  formatter=self.UniqueCallback('@TraderQuantityFormatter'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  visible=self.UniqueCallback('@TraderQuantityVisible'),
                                                  editable=False,
                                                  tick=True),                
                                                  
                'traderNominal': Object( label='Trader Nom',
                                                  objMapping=self.UniqueCallback('TraderNominal'),
                                                  formatter=self.UniqueCallback('@TraderNominalFormatter'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  visible=self.UniqueCallback('@TraderNominalVisible'),
                                                  editable=False,
                                                  tick=self.UniqueCallback('@NominalTick')),
                                                  
                'doAccept': Action( label=self.UniqueCallback('@AcceptButtonLabel'),
                                                  action=self.UniqueCallback('@OnAcceptQuote'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  backgroundColor=self.UniqueCallback('@AcceptButtonColor'),
                                                  visible=self.UniqueCallback('@AcceptButtonVisible')),      
       
                'doReject': Action( label='Reject',
                                                  action=self.UniqueCallback('@OnRejectQuote'),
                                                  enabled=self.UniqueCallback('@QuoteCanBeRejected'),
                                                  visible=self.UniqueCallback('@RejectButtonVisible')),

                'doWithdraw': Action( label='Withdraw',
                                                  action=self.UniqueCallback('@OnRejectQuote'),
                                                  enabled=self.UniqueCallback('@QuoteCanBeRejected'),
                                                  visible=self.UniqueCallback('@WithdrawButtonVisible')),
        })
        
        ''' Propose To Client '''
        attributes.update({
                
                'doProposeToClient': Action( label=self.UniqueCallback('@ProposeLabel'),
                                                  action=self.UniqueCallback('@OnProposeToClient'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  backgroundColor=self.UniqueCallback('@ProposeButtonColor'),
                                                  visible=self.UniqueCallback('@ProposeToClientButtonVisible')),
                                                  
                'wireTime': Object( label='Wire Time',
                                                  objMapping=self._qrData + '.WireTime',
                                                  transform=self.UniqueCallback('@TransformWireTime'),
                                                  visible=self.UniqueCallback('@WireTimeVisible'),
                                                  onChanged=self.UniqueCallback('@OnWireTimeChanged'),
                                                  formatter='SecondsSpan'),    
                                                  
                'lockAllInPrice': Object( label='Lock All-in Price',
                                                  objMapping=self.UniqueCallback('LockAllInPrice'),
                                                  defaultValue=False,
                                                  visible=self.UniqueCallback('@LockAllInPriceVisible'),
                                                  onChanged=self.UniqueCallback('@OnLockAllInPriceChanged'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted')),
        })   
        
        ''' Counter '''
        attributes.update({
                'counterEnabled': Object( label='',
                                                  toolTip='Counter Order',
                                                  objMapping=self.UniqueCallback('CounterEnabled')),

                'copyProposal': Action( label=self.UniqueCallback('@CopyProposalLabel'),
                                                  action=self.UniqueCallback('@OnCopyProposal'),
                                                  enabled=self.UniqueCallback('@CopyProposalVisible'),
                                                  visible=self.UniqueCallback('@CopyProposalVisible')),   
       
                'doCounterMode': Action( label=self.UniqueCallback('@CounterModeButtonLabel'),
                                                  action=self.UniqueCallback('@OnCounterModeEnabled'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  visible=self.UniqueCallback('@CounterModeButtonVisible')),

                'counterPrice': Object( label='Counter Price',
                                                  objMapping=self.UniqueCallback('CounterPrice'),
                                                  formatter='VeryDetailedShowZeroHideNaN',
                                                  visible=self.UniqueCallback('@CounterVisible'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  tick=self.UniqueCallback('@PriceTick')),
                                                  
                'counterSalesSpread': Object( label='Sales Spread',
                                                  objMapping=self.UniqueCallback('CounterSalesSpread'),
                                                  formatter='DetailedShowZero',
                                                  visible=self.UniqueCallback('@CounterVisible'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  tick=self.UniqueCallback('@SalesSpreadTick')),
                
                'counterMarginAmount': Object( label='Margin Amount',
                                                  objMapping=self.UniqueCallback('CounterMarginAmount'),
                                                  formatter=self.UniqueCallback('@PriceFormatter'),
                                                  editable=False,
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  visible=self.UniqueCallback('@CounterVisibleInDetails'),
                                                  tick=self.UniqueCallback('@PriceTick')),
                                                  
                'counterAllInPrice': Object( label='All-in Price',
                                                  objMapping=self.UniqueCallback('CounterAllInPrice'),
                                                  formatter='VeryDetailedShowZeroHideNaN',
                                                  visible=self.UniqueCallback('@CounterVisible'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  tick=self.UniqueCallback('@PriceTick')),
                                                  
                'counterNominal': Object( label='Counter Nom',
                                                  objMapping=self.UniqueCallback('CounterNominal'),
                                                  formatter='InstrumentDefinitionNominal',
                                                  visible=self.UniqueCallback('@CounterNominalVisible'),
                                                  editable=self.UniqueCallback('@CounterAmountEditable'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  validate=self.UniqueCallback('@ValidateNominal'),
                                                  tick=self.UniqueCallback('@NominalTick')),
                
                'counterQuantity': Object( label='Counter Qty',
                                                  objMapping=self.UniqueCallback('CounterQuantity'),
                                                  formatter='InstrumentDefinitionQuantity',
                                                  visible=self.UniqueCallback('@CounterQuantityVisible'),
                                                  editable=self.UniqueCallback('@CounterAmountEditable'),
                                                  enabled=self.UniqueCallback('@PriceCanBeAccepted'),
                                                  validate=self.UniqueCallback('@ValidateQuantity'),
                                                  tick=True),
                
                                                  
                'doCounterPrice': Action( label='Counter',
                                                  action=self.UniqueCallback('@OnCounterOrder'),
                                                  backgroundColor=self.UniqueCallback('@CounterButtonColor'),
                                                  visible=self.UniqueCallback('@CounterButtonVisible'),
                                                  enabled=self.UniqueCallback('@CounterButtonEnabled')),

                'actions': Action( label='>',
                                                  sizeToFit=True,
                                                  actionList=self.UniqueCallback('@Actions'),
                                                  visible=self.UniqueCallback('@ReplySectionVisible'),
                                                  enabled=self.UniqueCallback('@ActionsEnabled') ),
        
        })
        
        return attributes
        
    '''********************************************************************
    * Deal Misc
    ********************************************************************'''    
    def OnInit(self, direction, proposeToClient, onWireTimeChanged, onLockAllInPriceChanged, copyProposal, **kwargs):
        self._qrData = kwargs['qrDataMethod']
        self._imInterface = kwargs['imInterfaceMethod']
        self._instrument = kwargs['instrumentMethod']
        self._dealPackage = kwargs['dealPackageMethod']
        self._isRfqOnDealPackage = kwargs['isRfqOnDealPackageMethod']
        self._trade = kwargs['tradeMethod']
        self._customAttributes = kwargs['customAttributesMethod']
        self._direction = direction 
        self._proposeToClient = proposeToClient
        self._onWireTimeChanged = onWireTimeChanged
        self._onLockAllInPriceChanged = onLockAllInPriceChanged
        self._fetchProposalSummary=copyProposal
    
    def OnNew(self):
        self.SetDefaultValues()
        
    '''********************************************************************
    * When a new RFQ is created from existing window
    ********************************************************************'''
    def ClearReplyFields(self):
        self.salesSpread = 0.0
        self.allInPrice = 0.0
        self.traderNominal = 0.0
        self.counterEnabled = False
        self.lockAllInPrice = False
        self.SetDefaultValues()
        
    '''********************************************************************
    * Objects
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

    '''********************************************************************
    * Object Mappings
    ********************************************************************'''           

    @ReturnDomainDecorator('double')
    def TraderPrice(self, val = MethodDirection.asGetMethod, *args):
        if MethodDirection.AsGetMethod(val):
            traderPrice = self.QRData().TraderPrice(self.Direction())
            self.allInPrice = self.QRData().AllInPrice(self.Direction()) # Sadly necessary. the _allInPrices dict in QRData is updated in QRData.TraderPrice, and here we ensure that the object mapping is re-read
            return traderPrice
        else:
            self.QRData().TraderPrice(self.Direction(), val)
        
    @ReturnDomainDecorator('double')
    def SalesSpread(self, val = MethodDirection.asGetMethod, *args):
        if MethodDirection.AsGetMethod(val):
            return PriceAndMarginConversions.Spread(self.traderPrice, self.allInPrice, self.IsAskSide(), self.TradingInterface(), self.Instrument())
        else:
            newAllInPrice = PriceAndMarginConversions.AllInPrice(val, self.traderPrice, self.IsAskSide(), self.TradingInterface(), self.Instrument())
            self.allInPrice = newAllInPrice
            self.marginAmount = PriceAndMarginConversions.MarginAmount(self.traderPrice, self.allInPrice, self.Trade(), self.RFQDealPackage(), self.TradingInterface(), self.IsAskSide())
            self.counterSalesSpread = val
            
    @ReturnDomainDecorator('double')
    def MarginAmount(self, val = MethodDirection.asGetMethod, *args):
        if MethodDirection.AsGetMethod(val):
            return self.QRData().MarginAmount(self.Direction())
        else:
            self.QRData().MarginAmount(self.Direction(), val)
    
    @ReturnDomainDecorator('double')
    def AllInPrice(self, val = MethodDirection.asGetMethod, *args):
        if MethodDirection.AsGetMethod(val):
            return self.QRData().AllInPrice(self.Direction())
        else:
            self.QRData().AllInPrice(self.Direction(), val)
            self.marginAmount = PriceAndMarginConversions.MarginAmount(self.traderPrice, val, self.Trade(), self.RFQDealPackage(), self.TradingInterface(), self.IsAskSide())
            
            
    @ReturnDomainDecorator('bool')
    def LockAllInPrice(self, val = MethodDirection.asGetMethod, *args):
        return self.QRData().LockAllInPrice(self.Direction(), val)
    
    @ReturnDomainDecorator('double')
    def CounterPrice(self, val = MethodDirection.asGetMethod, *args):
        return self.QRData().CounterPrice(self.Direction(), val)
        
    
    @ReturnDomainDecorator('double')
    def CounterAllInPrice(self, val = MethodDirection.asGetMethod, *args):
        if not MethodDirection.AsGetMethod(val):
            self.counterMarginAmount = PriceAndMarginConversions.MarginAmount(self.counterPrice, val, self.Trade(), self.RFQDealPackage(), self.TradingInterface(), self.IsAskSide())
        return self.QRData().CounterAllInPrice(self.Direction(), val)
        
    @ReturnDomainDecorator('double')
    def CounterSalesSpread(self, val = MethodDirection.asGetMethod, *args):
        if MethodDirection.AsGetMethod(val):
            return PriceAndMarginConversions.Spread(self.counterPrice, self.counterAllInPrice, self.IsAskSide(), self.TradingInterface(), self.Instrument())
        else:
            newAllInPrice = PriceAndMarginConversions.AllInPrice(val, self.counterPrice, self.IsAskSide(), self.TradingInterface(), self.Instrument())
            self.counterMarginAmount = PriceAndMarginConversions.MarginAmount(self.counterPrice, self.counterAllInPrice, self.Trade(), self.RFQDealPackage(), self.TradingInterface(), self.IsAskSide())
            self.counterAllInPrice = newAllInPrice
    
    @ReturnDomainDecorator('double')
    def CounterMarginAmount(self, val = MethodDirection.asGetMethod, *args):
        if MethodDirection.AsGetMethod(val):
            return self.QRData().CounterMarginAmount(self.Direction())
        else:
            self.QRData().CounterMarginAmount(self.Direction(), val)
    
    @ReturnDomainDecorator('double')
    def TraderQuantity(self, val = MethodDirection.asGetMethod, *args):
        return self.QRData().TraderQuantity(self.Direction(), val)
        
    @ReturnDomainDecorator('double')
    def TraderNominal(self, val = MethodDirection.asGetMethod, *args):
        return self.QRData().TraderNominal(self.Direction(), val)
    
    @ReturnDomainDecorator('bool')
    def CounterEnabled(self, val = MethodDirection.asGetMethod, *args):
        return self.QRData().CounterEnabled(self.Direction(), val)
    
    @ReturnDomainDecorator('double')
    def CounterQuantity(self, val = MethodDirection.asGetMethod, *args):
        return self.QRData().CounterQuantity(self.Direction(), val)
    
    @ReturnDomainDecorator('double')
    def CounterNominal(self, val = MethodDirection.asGetMethod, *args):
        return self.QRData().CounterNominal(self.Direction(), val)

    '''********************************************************************
    * From QRData
    ********************************************************************'''                  
    def PriceCanBeAccepted(self, *args):
        return self.QRData().QuoteRequestCanBeAccepted(self.Direction()) or self.TradingIsAccepting()

    def TradingIsAccepting(self, *args):
        return self.Direction() == self.QRData().Direction() and self.QRData().TradingQuoteRequestStatus() == Status.accepting
    
    def CustomerPriceIsFirm(self, *args):
        return self.QRData().CustomerPriceIsFirm()
    
    def SideIsCountered(self, val = MethodDirection.asGetMethod, *args):
        return self.QRData().SideIsCountered(self.Direction())
    
    def ProposedToClient(self):
        return self.QRData().ProposedToClient()

    '''********************************************************************
    * On Changed
    ********************************************************************'''      
    def OnWireTimeChanged(self, attrName, oldValue, newValue, *args):
        self.GetMethod(self._onWireTimeChanged)(newValue)

    def OnLockAllInPriceChanged(self, attrName, oldValue, newValue, *args):
        self.GetMethod(self._onLockAllInPriceChanged)(newValue)
        
    '''********************************************************************
    * Actions
    ********************************************************************'''
    def ResetCountered(self):
        self.counterEnabled = False
    
    def CheckValidToAcceptQuoteRequest(self):
        if not self.traderQuantity > 0:
            raise DealPackageUserException('Total trader quantity must be positive.')
        self.IMInterface().VerifyIsConnected()
        
    def OnAcceptQuote(self, attrName, *args):
        self.CheckValidToAcceptQuoteRequest()
        if self.ProposedToClient():
            self.IMInterface().AcceptQuote(self.Direction())

    def OnRejectQuote(self, *args):
        self.IMInterface().Withdraw()  

    def OnProposeToClient(self, *args):
        self.GetMethod(self._proposeToClient)()
        
    def OnCounterOrder(self, attrName, *args):
        self.IMInterface().CounterOrder(self.Direction(), self.counterPrice, self.counterQuantity, self.counterAllInPrice)

    def OnCounterModeEnabled(self, attrName, *args):
        self.counterEnabled = not self.counterEnabled
        self.lockAllInPrice = False

    def OnCopyProposal(self, *args):
        self.GetMethod(self._fetchProposalSummary)()
        
    def Actions(self, *args):
        actions = []
        def Add(internalName):
            actions.append(self.PrefixedName(internalName))
        
        Add('doAccept')
        Add('doProposeToClient')
        Add('doCounterPrice')
        Add('doReject')
        Add('doWithdraw')
        Add('doCounterMode')
        Add('copyProposal')
        
        return actions

    '''********************************************************************
    * Visible
    ********************************************************************'''
    def AcceptButtonVisible(self, *args):
        return self.ProposedToClient() and self.CounterNotVisible() and self.ReplySectionVisible()

    def RejectButtonVisible(self, *args):
        return not self.SideIsCountered() and self.ReplySectionVisible()
    
    def WithdrawButtonVisible(self, *args):
        return self.SideIsCountered() and self.ReplySectionVisible()

    def CounterButtonVisible(self, *args):
        return self.CounterVisible() and not self.WithdrawButtonVisible() and self.ReplySectionVisible()
        
    def ProposeToClientButtonVisible(self, *args):
        return not self.ProposedToClient() and self.ReplySectionVisible()

    def CounterVisible(self, *args):
        return self.ProposedToClient() and self.counterEnabled and self.ReplySectionVisible()
        
    def CopyProposalVisible(self, *args):
        return self.ReplySectionVisible()
    
    def CounterNotVisibleInDetails(self, *args):
        return self.CounterNotVisible() and self.IsShowModeDetail()
        
    def CounterVisibleInDetails(self, *args):
        return self.CounterVisible() and self.IsShowModeDetail()
    
    def CounterNotVisible(self, *args):
        return not self.counterEnabled and self.ReplySectionVisible()

    def ReplySectionVisible(self, *args):
        return self.QRData().TradingQuoteRequestStatus() in [Status.firm, Status.subject, Status.subjAccept, Status.stream, Status.countered, Status.accepting] 
    
    def WireTimeVisible(self, *args):
        visible = False
        if self.ProposeToClientButtonVisible() and self.PriceCanBeAccepted():
            if self.UseManualWireTime():
                visible = True
        return visible
    
    def LockAllInPriceVisible(self, *args):
        visible = False
        if self.ReplySectionVisible() and self.PriceCanBeAccepted() and not self.counterEnabled:
            visible = not self.CustomerPriceIsFirm() and not self.WireTimeVisible() and not self.SideIsCountered()
        return visible
        
    def TraderQuantityVisible(self, *args):
        return self.CounterNotVisible() and Amount.UseQuantity(self.Instrument(), self.RFQDealPackage())
        
    def TraderNominalVisible(self, *args):
        return self.CounterNotVisible() and not Amount.UseQuantity(self.Instrument(), self.RFQDealPackage())
    
    def CounterQuantityVisible(self, *args):
        return self.CounterVisible() and Amount.UseQuantity(self.Instrument(), self.RFQDealPackage()) 
    
    def CounterNominalVisible(self, *args):
        return self.CounterVisible() and not Amount.UseQuantity(self.Instrument(), self.RFQDealPackage()) 
        
    '''********************************************************************
    * Enabled
    ********************************************************************'''
    def CounterModeButtonVisible(self, *args):
        return self.ProposedToClient() and self.PriceCanBeAccepted() and not self.QRData().CanBeConfirmed()
     
    def QuoteCanBeRejected(self, *args):
        return self.PriceCanBeAccepted() or self.counterEnabled
        
    def AllInPriceEnabled(self, *args):
        return self.PriceCanBeAccepted() and not self.CustomerPriceIsFirm()

    def SpreadEnabled(self, *args):
        return self.AllInPriceEnabled()
        
    def CounterButtonEnabled(self, *args):
        enabled = False
        if self.ProposedToClient():
            if self.PriceCanBeAccepted() and self.CounterVisible():
                enabled = Validation.CounterPrice(self.traderPrice, self.counterPrice, self.IsAskSide(), IsYieldQuoted(self.TradingInterface(), self.Instrument()))
                if not enabled:
                    enabled = self.counterNominal != self.traderNominal
        return enabled

    def ActionsEnabled(self, *args):
        return self.ProposedToClient() and self.PriceCanBeAccepted() or self.QuoteCanBeRejected() or self.CounterButtonEnabled()
      
    '''********************************************************************
    * Editable
    ********************************************************************'''
    def CounterAmountEditable(self, *args):
        return not self.IsRFQOnDealPackage()
        
    '''********************************************************************
    * Labels
    ********************************************************************'''    
    def AcceptButtonLabel(self, *args):
        return ButtonLabels.ButtonLabels(self.Instrument())[4] if self.IsAskSide() else ButtonLabels.ButtonLabels(self.Instrument())[3]

    def CounterModeButtonLabel(self, *args):
        return 'Deactivate Counter' if self.counterEnabled else 'Activate Counter'
    
    def CopyProposalLabel(self, *args):
        return 'Copy Proposal'
    
    def TraderQuantityLabel(self, attrName, *args):
        return Amount.QuantityLabel('Trader Qty', self.RFQDealPackage())
    
    def ProposeLabel(self, attrName, *args):
        return 'Accept' if self.QRData().CanBeConfirmed() else 'Propose'
    
    '''********************************************************************
    * Colors
    ********************************************************************'''        
    def AcceptButtonColor(self, *args):
        if not self.counterEnabled:
            return Direction.Color(self.Direction(), self.Instrument())

    def ProposeButtonColor(self, *args):
        return Direction.Color(self.Direction(), self.Instrument()) if self.QRData().CanBeConfirmed() else None

    def CounterButtonColor(self, *args):
        if self.counterEnabled:
            return Direction.Color(self.Direction(), self.Instrument())
       
    '''********************************************************************
    * Formatters
    ********************************************************************'''        
    def PriceFormatter(self, *args):
        return acm.FNumFormatter('VeryDetailedShowZeroHideNaN')

    def SalesSpreadFormatter(self, *args):
        return acm.FNumFormatter('DetailedShowZero')

    def TraderNominalFormatter(self, *args):
        return acm.FNumFormatter('InstrumentDefinitionNominalShowZero')
    
    def TraderQuantityFormatter(self, *args):
        return acm.FNumFormatter('InstrumentDefinitionQuantityShowZero')
    
    '''********************************************************************
    * Tick
    ********************************************************************'''  
    def PriceTick(self, attrName, value, increment):
        return TradingInterface.TickValue(value, increment, TickSizeSettings.PriceTickSize, self.Instrument(), self.TradingInterface())

    def SalesSpreadTick(self, attrName, value, increment):
        return TradingInterface.TickValue(value, increment, TickSizeSettings.SalesSpreadTickSize, self.Instrument(), self.TradingInterface(), self.traderPrice)

    def MarginAmountTick(self, attrName, value, increment):
        return TradingInterface.TickValue(value, increment, TickSizeSettings.MarginAmountTickSize, self.Instrument(), self.TradingInterface())
        
    def NominalTick(self, attrName, value, increment):
        return TradingInterface.TickValue(value, increment, TickSizeSettings.NominalTickSize, self.Instrument(), self.TradingInterface())

    '''********************************************************************
    * Validation 
    ********************************************************************'''  
    def ValidateNominal(self, name, value):
        Validation.Nominal(value, self.Instrument())
    
    def ValidateQuantity(self, name, value):
        Validation.Nominal(self.QRData().QuantityToNominal(value), self.Instrument())
        return value
        
    '''********************************************************************
    * Transform
    ********************************************************************'''
    def TransformWireTime(self, attrName, inputStr, *args):
        transformed = None
        if inputStr and inputStr != '0':
            transformed = Time.ParseTimeSpan(inputStr)
        else:
            transformed = -1
        return transformed

    '''********************************************************************
    * Misc
    ********************************************************************'''
    def UseManualWireTime(self):
        return self.QRData().CustomerPriceTypeAsFirm() and self.QRData().TraderPriceIsFirmStream()

    def GetWireTime(self):
        if self.UseManualWireTime():
            wireTime = self.wireTime
        else:
            wireTime = self.QRData().TimeLeft()
        return wireTime
    
    def Direction(self):
        return self._direction
        
    def IsAskSide(self):
        return Direction.IsAsk(self._direction)

    def CustomAttributesAttr(self):
        return self.GetMethod(self._customAttributes)()

    def CustomAttributeMethod(self, methodName):
        customAttributes = self.CustomAttributesAttr()
        return getattr(customAttributes, methodName)


    '''********************************************************************
    * Default values
    ********************************************************************'''
        
    def SetDefaultValues(self):
        self.wireTime = RFQTimerDefaultSettings.defaultWireTime
