import acm
import FUxCore
import math
PV = 'PV'
ACC = 'ACC'
NOMINAL = 'NOMINAL'
PVPAYTYPE = 'PVPayType'
ACCPAYTYPE = 'AccPayType'
NOMINALPAYTYPE = 'NominalPayType'

def OnOkButtonClicked(self, cd):
    self.StoreParameters()
    self.m_fuxDlg.CloseDialogOK()

def OnConnectedButtonClicked(self, cd):
    self.OpenConnectedTrades()

def OnValueDateChanged(self, cd):
    try:valueDate = self.GetValueDate()
    except Exception as err:return
    if self.m_instrument.IsKindOf('FOdf'):
        faceValue = self.m_trade.RemainingDrawdownAmount()
    else:
        faceValue = acm.TradeActionUtil().RemainingNominal(self.m_trade, valueDate, valueDate)
    self.SetControlValues(valueDate, faceValue)

def OnFaceValueChanged(self, cd):
    try:
        faceValue = self.m_faceValueCtrl.GetValue()
        valueDate = self.GetValueDate()
    except Exception as err:return
    self.SetFaceValue(faceValue)
    
def OnSplitChanged(self, cd):
    checked = self.m_splitBox.Checked()
    self.UpdateSplitControls(checked)
    
def OnNominalSplitChanged(self, cd):
    checked = self.m_nominalSplitBox.Checked()
    self.UpdateNominalSplitControls(checked)    
    self.SetFaceValue(self.m_faceValueCtrl.GetValue()) # Resetting (same) face value will trigger new PV calculation    

def OnCreatePaymentsChanged(self, cd):
    checked = self.m_createPaymentsBox.Checked()
    self.UpdateCreatePayments(checked)
    if self.m_instrument.Legs().Size() > 1:
        if checked:
            self.UpdateSplitControls(self.m_splitBox.Checked())

def OnCurrencyChanged(self, cd):
    self.UpdatePaymentsWithNewCurrency()
    
def OnPaymentChanged(self, cd):
    try:
        self.m_pvCtrl.GetValue()
    except Exception as err:
        self.m_pvCtrl.SetValue(0.0)
        
def OnAccruedInterestChanged(self, cd):
    try:
        self.m_accCtrl.GetValue()
    except Exception as err:
        self.m_accCtrl.SetValue(0.0)

def OnPaymentFarLegChanged(self, cd):
    try:
        self.m_pvCtrlFarLeg.GetValue()
    except Exception as err:
        self.m_pvCtrlFarLeg.SetValue(0.0)


# ########################## CloseTradeDialogBase #####################################
class CloseTradeDialogBase (FUxCore.LayoutDialog):
    def __init__(self, trade, connectedTrades):
        self.m_trade = trade                           
        self.m_connected = connectedTrades     
        self.m_instrument = trade.Instrument()   
        self.m_faceValueCtrl = None              
        self.m_origFaceValueCtrl = None       
        self.m_pvCtrl = None                
        self.m_pvPayTypeCtrl = None  
        self.m_connectedBtn = None      
        self.m_okBtn = None               
        self.m_cancelBtn = None             
        self.m_splitBox = None             
        self.m_parameters = acm.FDictionary()   
        self.m_spaceCollection = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        self.m_layout = None                         
        self.m_calculatedPremium = 0.0
        self.m_createPaymentsBox = None          
            
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        if aspectSymbol == acm.FSymbol('ControlValueChanged'):
            self.HandleControlChanged(parameter)
            
    def HandleControlChanged(self, binder):
        if binder == self.m_faceValueCtrl:
            OnFaceValueChanged(self, None)
            
        if binder == self.m_pvCtrl:
            OnPaymentChanged(self, None)
            
    def _SetupLayout_(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_layout = layout
        self.m_fuxDlg.Caption( 'Close Trade ' + str(self.m_trade.StringKey()) )
        if self.m_connected.Size():
            self.m_connctedBtn = layout.GetControl("connected")
            self.m_connctedBtn.AddCallback( "Activate", OnConnectedButtonClicked, self )
        self.m_okBtn = layout.GetControl("ok")
        self.m_okBtn.AddCallback( "Activate", OnOkButtonClicked, self )    
        self.m_bindings.AddLayout(layout)
    
    def _SetLayoutInitValues_(self):
        now = acm.Time().DateNow() 
        currency = self.m_instrument.Currency()
        calendar = currency.Calendar()
        valueDate = self.GetAdjustedValueDate(now, calendar)
        if acm.Time.DateDifference(valueDate, self.m_trade.ValueDay()) < 0:
            valueDate = self.m_trade.ValueDay()
        self.SetValueDate(valueDate)
        faceValue = self.GetRemainingNominal(valueDate)
        self.SetControlValues(valueDate, faceValue)
        self.m_origFaceValueCtrl.SetValue(faceValue)
        self.SetPaymentTypeControls()
        self.m_origFaceValueCtrl.Editable(False)
        self.m_pvPayTypeCtrl.SetValue('Termination Fee')

    def GetAdjustedValueDate(self, now, calendar):
        if self.m_instrument.OpenEnd() == 'Open End' and self.m_instrument.IsCashFlowInstrument():
            return self.m_instrument.SuggestOpenEndTerminationDate()
        else:
            return self.m_instrument.SpotDate(now, calendar)

    def _SetFaceValueAndValueDate_(self, valueDate, faceValue):
        self.tradeClone = self.m_trade.Clone()
        self.tradeClone.ValueDay(valueDate)
        self.tradeClone.AcquireDay(valueDate)
        self.tradeClone.FaceValue(faceValue)
        self.tradeClone.Premium(0.0)
        tradePV = self.tradeClone.Calculation().PresentValueSource(self.m_spaceCollection).Value()
        self.m_pvCtrl.SetValue(tradePV)
        self.m_calculatedPremium = -self.tradeClone.Calculation().PriceToPremium(self.m_spaceCollection, self.GetAcquireDate(), self.m_trade.Price()).Number()      

    def _SetControlValues_( self, valueDate, faceValue ):
        self.m_faceValueCtrl.SetValue(faceValue)
        self.SetFaceValueAndValueDate(valueDate, faceValue)
        
    def SetFaceValue(self, faceValue):
        valueDate = self.GetValueDate() 
        self.SetFaceValueAndValueDate(valueDate, faceValue)  
        
    def StoreInstrumentPayments(self, payments):
        payments.Add(self.CreatePayment(self.m_instrument.Currency(), self.m_pvCtrl, self.m_pvPayTypeCtrl))
        payments.Add(self.CreatePayment(self.m_instrument.Currency(), self.m_accCtrl, self.m_accPayTypeCtrl))
        
    def _InitControls_(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        formatter = acm.Get('formats/InstrumentDefinitionNominalSigDig')
        self.m_faceValueCtrl = self.m_bindings.AddBinder( 'faceValueCtrl', acm.GetDomain('double'), formatter )
        self.m_origFaceValueCtrl = self.m_bindings.AddBinder( 'origFaceValueCtrl', acm.GetDomain('double'), formatter )
        self.m_pvPayTypeCtrl = self.CreatePayTypeControl('pvPayTypeCtrl')
        
    def CreateDoubleControl(self, key, numberOfDecimals):
        formatter = acm.FNumFormatter('myFormatter')
        formatter.NumDecimals(numberOfDecimals)
        ctrl = self.m_bindings.AddBinder(key, acm.GetDomain('double'), formatter)
        return ctrl

    def CreatePayTypeControl(self, key):
        ctrl = self.m_bindings.AddBinder(key, acm.GetDomain('enum(PaymentType)'), None )
        return ctrl

    def StoreParameters(self):
        self.m_parameters.AtPut( 'acquireDay', self.GetAcquireDate() )
        self.m_parameters.AtPut( 'valuationDay', self.GetValueDate() ) 
        self.m_parameters.AtPut( 'payments', self.GetPayments() )
        self.m_parameters.AtPut( 'faceValue', -self.m_faceValueCtrl.GetValue() )
        self.m_parameters.AtPut( 'premium', self.GetPremium() )
        
    def StoreLegPayments(self, payments):
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                    legDict = self.m_legControls.At(leg)
                    payments.Add(self.CreatePayment(leg.Currency(), legDict.At(PV), legDict.At(PVPAYTYPE)))
                    payments.Add(self.CreatePayment(leg.Currency(), legDict.At(ACC), legDict.At(ACCPAYTYPE)))

    def CreatePayment(self, currency, amountControl, payTypeControl, text=""):
        if amountControl.GetValue() != 0.0:
            payment = acm.FPayment()
            payment.Amount(amountControl.GetValue())
            payment.Type(payTypeControl.GetValue())
            payment.Party(self.m_trade.Counterparty())
            payment.Currency(currency)
            if text != "":
                payment.Text(text)
            
            payment.PayDay(self.GetValueDate())
            payment.ValidFrom(acm.Time().DateToday())
            return payment

    def GetParameters(self):
        return self.m_parameters
        
    def UpdateSplitControls(self, checked):
        notChecked = not checked
        self.m_pvCtrl.Editable(notChecked)
        self.m_accCtrl.Editable(notChecked)
        self.m_pvPayTypeCtrl.Editable(notChecked)
        self.m_accPayTypeCtrl.Editable(notChecked)
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                legDict = self.m_legControls.At(leg)
                legDict.At(PV).Editable(checked)
                legDict.At(PVPAYTYPE).Editable(checked)
                legDict.At(ACC).Editable(checked)
                legDict.At(ACCPAYTYPE).Editable(checked)
                
    def UpdateCreatePayments(self, checked):
        self.m_pvCtrl.Editable( checked )
        self.m_accCtrl.Editable( checked )
        self.m_pvPayTypeCtrl.Editable( checked )
        self.m_accPayTypeCtrl.Editable( checked )
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                self.m_splitBox.Editable( checked )
                legDict = self.m_legControls.At(leg)
                legDict.At(PV).Editable( checked )
                legDict.At(PVPAYTYPE).Editable( checked )
                legDict.At(ACC).Editable( checked )
                legDict.At(ACCPAYTYPE).Editable( checked )
    
    def OpenConnectedTrades(self):
        for trade in self.m_connected:
            acm.UX().SessionManager().StartApplication('Instrument Definition', trade)
    
    def GetRemainingNominal(self, valueDate):
        return acm.TradeActionUtil().RemainingNominal(self.m_trade, valueDate, valueDate)


# ######################### CloseTradeDialogFX ####################################
class CloseTradeDialogFX (CloseTradeDialogBase):
    def __init__(self, trade, connectedTrades):
        CloseTradeDialogBase.__init__(self, trade, connectedTrades)
        self.m_currencyCtrl = None
        self.m_previousCurrency = None
        self.m_valueDate = None

    def HandleCreate( self, dlg, layout ):
        CloseTradeDialogBase._SetupLayout_(self, dlg, layout)
        self.m_layout.GetControl('currencyCtrl').AddCallback("Changed", OnCurrencyChanged, self)
        self.m_currencyCtrl.SetValue(self.m_trade.Currency()) 
        self.m_previousCurrency = self.m_currencyCtrl.GetValue()
        CloseTradeDialogBase._SetLayoutInitValues_(self)
        now = acm.Time().DateNow()
        valueDate = self.m_trade.ValueDay()
        if acm.Time.DateDifference(valueDate, now) < 0:
            valueDate = now
        self.SetValueDate(valueDate)  
        self.SetAcquireDate(valueDate)
        self.m_createPaymentsBox = layout.GetControl('createPaymentsBox')
        self.m_createPaymentsBox.Checked(True)
        self.m_createPaymentsBox.AddCallback("Activate", OnCreatePaymentsChanged, self )

    def GetPayments(self):
        payments = acm.FArray()
        if self.m_createPaymentsBox.Checked():
            self.StoreInstrumentPayments(payments)
        return payments        

    def UpdateCreatePayments(self, checked):
        self.m_pvCtrl.Editable(checked)        
        self.m_pvPayTypeCtrl.Editable(checked)
        self.m_currencyCtrl.Editable(checked)
        
    def GetPremium(self):
        return self.m_calculatedPremium

    def InitControls(self):
        CloseTradeDialogBase._InitControls_(self)
        self.m_pvCtrl = self.CreateDoubleControl('pvCtrl', 6)
        allCurrencies = self.GetAllCurrencies()
        self.m_currencyCtrl = self.m_bindings.AddBinder('currencyCtrl', acm.GetDomain('FCurrency'), None, allCurrencies)    

    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginVertBox('Invisible')
        self.m_faceValueCtrl.BuildLayoutPart(b, 'Nominal')
        self.m_origFaceValueCtrl.BuildLayoutPart(b, 'Total Nominal')
        b.  EndBox()
        b.  BeginVertBox('Invisible')
        b.  AddCheckbox('createPaymentsBox', 'Create Payments')
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Close Out Payments')
        self.m_currencyCtrl.BuildLayoutPart(b, 'Currency')
        b.    BeginHorzBox()
        self.m_pvCtrl.BuildLayoutPart(b, 'PV')
        self.m_pvPayTypeCtrl.BuildLayoutPart(b, None)
        b.    EndBox()
        b.  EndBox()
        b.  AddSpace(5)
        if self.m_connected.Size():
            b.    BeginVertBox('EtchedIn', 'Connected Trades')
            b.    AddButton('connected', 'Connected...')
            for trade in self.m_connected:
                b.    AddLabel('label' + str(trade.Oid()), '%s, %s' % (trade.Instrument().Name(), str(trade.Oid())))
            b.    EndBox()
        b.  BeginVertBox()
        b.    AddSpace(10)
        b.    BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b
          
    def StoreInstrumentPayments(self, payments):
        payments.Add(self.CreatePayment(self.m_currencyCtrl.GetValue(), self.m_pvCtrl, self.m_pvPayTypeCtrl))

    def GetPriceToPremium(self, incomingValue, price):
        tradeClone = self.m_trade.Clone()
        tradeClone.ValueDay(self.m_trade.ValueDay())
        tradeClone.AcquireDay(self.m_trade.ValueDay())
        tradeClone.FaceValue(incomingValue)
        tradeClone.Premium(0.0)
        return tradeClone.Calculation().PriceToPremium(self.m_spaceCollection, self.m_trade.ValueDay(), price).Number()

    def SetFaceValueAndValueDate(self, valueDate, faceValue):
        if self.m_trade.QuantityIsDerived():
            self.m_calculatedPremium = self.GetPriceToPremium(faceValue, 1/self.m_trade.Price())
            self.m_pvCtrl.SetValue(self.GetTradePV(self.m_calculatedPremium, self.m_trade))
        else:
            self.m_calculatedPremium = -self.GetPriceToPremium(faceValue, self.m_trade.Price())
            self.m_pvCtrl.SetValue(self.GetTradePV(faceValue, self.m_trade))

    def GetTradePV(self, faceValue, trade):
        scaleFactor = 1.0*faceValue/trade.Nominal()
        tradeTPL = trade.Calculation().TotalProfitLoss(self.m_spaceCollection, acm.Time().SmallDate(), acm.Time().DateNow(), trade.Currency()).Number()
        tradeTPL = self.ConvertToOtherCurrency(tradeTPL, trade.Currency())
        return tradeTPL*scaleFactor        
        
    def ConvertToOtherCurrency(self, value, previousCurrency):
        if self.m_currencyCtrl.GetValue() != None:
            currRate = 1.0
            if previousCurrency != self.m_currencyCtrl.GetValue():
                currRate = previousCurrency.Calculation().FXRate(self.m_spaceCollection, self.m_currencyCtrl.GetValue()).Number()
                if currRate == 0.0 or math.isnan(currRate) or math.isinf(currRate):
                    currRate = 0.0
                    self.LogZeroFXRate(previousCurrency)
            value = value * currRate
        return value    
        
    def LogZeroFXRate(self):
        acm.Log('FX rate is zero for currency pair %s/%s' % (self.m_currencyCtrl.GetValue().Name(), self.m_trade.Currency().Name()))
        
    def UpdatePaymentsWithNewCurrency(self):
        if self.m_currencyCtrl.GetValue() is not None:
            self.SetPaymentToControls(self.m_pvCtrl, self.m_previousCurrency)
            self.m_previousCurrency = self.m_currencyCtrl.GetValue()
                
    def SetPaymentToControls(self, paymentControl, previousCurrency):
        convertedPayment = self.ConvertToOtherCurrency(paymentControl.GetValue(), previousCurrency)
        paymentControl.SetValue(convertedPayment)
        
    def SetControlValues( self, valueDate, faceValue ):
        self.SetAcquireDate(self.m_trade.ValueDay())
        CloseTradeDialogBase._SetControlValues_(self, valueDate, faceValue)

    def GetAllCurrencies(self):
        allCurrencies = acm.FCurrency.Select('')
        return allCurrencies.AsList()        
  
    def SetPaymentTypeControls(self): 
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                legDict = self.m_legControls.At(leg)
                pvPayTypeCtrl = legDict.At(PVPAYTYPE)
                pvPayTypeCtrl.SetValue('Termination Fee')
  
    def GetValueDate(self):
        return self.m_valueDate
        
    def SetValueDate(self, valueDate):
        self.m_valueDate = valueDate
        
    def GetAcquireDate(self):
        return self.m_acquireDate
        
    def SetAcquireDate(self, acquireDate):
        self.m_acquireDate = acquireDate
    
  
# ######################### CloseTradeDialogFXODF ####################################  
class CloseTradeDialogFXODF (CloseTradeDialogFX):
    def __init__(self, trade, connectedTrades):
        CloseTradeDialogFX.__init__(self, trade, connectedTrades)
    
    def GetRemainingNominal(self, valueDate):
        return self.m_trade.RemainingDrawdownAmount()
    
    def StoreParameters(self):
        self.m_parameters.AtPut( 'acquireDay', self.GetAcquireDate() )
        self.m_parameters.AtPut( 'valuationDay', self.GetValueDate() ) 
        self.m_parameters.AtPut( 'payments', self.GetPayments() )
        self.m_parameters.AtPut( 'faceValue', self.m_faceValueCtrl.GetValue() )
        self.m_parameters.AtPut( 'premium', self.GetPremium() )

# ######################### CloseTradeDialogFXSwap ####################################  
class CloseTradeDialogFXSwap (CloseTradeDialogFX):
    def __init__(self, trade, connectedTrades, farLegTrade):
        CloseTradeDialogFX.__init__(self, trade, connectedTrades)  
        self.m_farLegTrade = farLegTrade
        self.m_pvCtrlFarLeg = None
        self.m_pvPayTypeCtrlFarLeg = None
        self.m_calculatedPremiumFarLeg = None 
        self.m_faceValueFarLeg = None
        
    def HandleCreate( self, dlg, layout ):
        CloseTradeDialogFX.HandleCreate(self, dlg, layout)
        self.m_pvPayTypeCtrlFarLeg.SetValue('Termination Fee')
        self.m_layout.GetControl('pvCtrlFarLeg').AddCallback( "Changed", OnPaymentFarLegChanged, self )
        
    def InitControls(self):
        CloseTradeDialogBase._InitControls_(self)
        self.m_pvCtrl = self.CreateDoubleControl('pvCtrl', 6)
        allCurrencies = self.GetAllCurrencies()
        self.m_currencyCtrl = self.m_bindings.AddBinder('currencyCtrl', acm.GetDomain('FCurrency'), None, allCurrencies)
        self.m_pvCtrlFarLeg = self.CreateDoubleControl('pvCtrlFarLeg', 6)
        self.m_pvPayTypeCtrlFarLeg = self.CreatePayTypeControl('pvPayTypeCtrlFarLeg')
        
    def UpdateCreatePayments(self, checked):
        CloseTradeDialogFX.UpdateCreatePayments(self, checked)        
        self.m_pvCtrlFarLeg.Editable(checked)
        self.m_pvPayTypeCtrlFarLeg.Editable(checked)

    def UpdatePaymentsWithNewCurrency(self):
        if self.m_currencyCtrl.GetValue() is not None:
            self.SetPaymentToControls(self.m_pvCtrl, self.m_previousCurrency)
            self.SetPaymentToControls(self.m_pvCtrlFarLeg, self.m_previousCurrency)
            self.m_previousCurrency = self.m_currencyCtrl.GetValue()

    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginVertBox('Invisible')
        self.m_faceValueCtrl.BuildLayoutPart(b, 'Nominal')
        self.m_origFaceValueCtrl.BuildLayoutPart(b, 'Total Nominal')
        b.  EndBox()
        b.  BeginVertBox('Invisible')
        b.  AddCheckbox('createPaymentsBox', 'Create Payments')
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Close Out Payments')
        self.m_currencyCtrl.BuildLayoutPart(b, 'Currency')
        b.    BeginHorzBox()
        self.m_pvCtrl.BuildLayoutPart(b, 'PV Near Leg')
        self.m_pvPayTypeCtrl.BuildLayoutPart(b, None)
        b.    EndBox()
        b.    BeginHorzBox()
        self.m_pvCtrlFarLeg.BuildLayoutPart(b, 'PV Far Leg')
        self.m_pvPayTypeCtrlFarLeg.BuildLayoutPart(b, None)
        b.    EndBox()
        b.  EndBox()
        b.  AddSpace(5)
        if self.m_connected.Size():
            b.    BeginVertBox('EtchedIn', 'Connected Trades')
            b.    AddButton('connected', 'Connected...')
            for trade in self.m_connected:
                b.    AddLabel('label' + str(trade.Oid()), '%s, %s' % (trade.Instrument().Name(), str(trade.Oid())))
            b.    EndBox()
        b.  BeginVertBox()
        b.    AddSpace(10)
        b.    BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b  
  
    def GetFarLegPriceToPremium(self, value, price):
        tradeClone = self.m_farLegTrade.Clone()
        tradeClone.ValueDay(self.m_farLegTrade.ValueDay())
        tradeClone.AcquireDay(self.m_farLegTrade.ValueDay())
        tradeClone.FaceValue(value)
        tradeClone.Premium(0.0)
        return -tradeClone.Calculation().PriceToPremium(self.m_spaceCollection, self.m_farLegTrade.AcquireDay(), price).Number()
  
    def SetFaceValueAndValueDate(self, valueDate, faceValue):
        CloseTradeDialogFX.SetFaceValueAndValueDate(self, valueDate, faceValue)
        if self.m_farLegTrade.QuantityIsDerived():
            scaleFactor = math.fabs(faceValue / self.m_trade.Premium())
            self.m_calculatedPremiumFarLeg = -self.GetFarLegPriceToPremium(self.m_farLegTrade.Premium()*scaleFactor, 1/self.m_farLegTrade.Price())
            self.m_faceValueFarLeg = self.m_farLegTrade.Premium() * scaleFactor
        else:
            scaleFactor = math.fabs(faceValue / self.m_trade.Nominal())
            self.m_calculatedPremiumFarLeg = self.GetFarLegPriceToPremium(self.m_farLegTrade.Nominal()*scaleFactor, self.m_farLegTrade.Price())
            self.m_faceValueFarLeg = self.m_farLegTrade.Nominal() * scaleFactor
            
        self.m_pvCtrlFarLeg.SetValue(self.GetTradePV(self.m_farLegTrade.Nominal()*scaleFactor, self.m_farLegTrade)) 
 
    def StoreInstrumentPayments(self, payments):
        payments.Add(self.CreatePayment(self.m_currencyCtrl.GetValue(), self.m_pvCtrl, self.m_pvPayTypeCtrl, "Near leg"))
        payments.Add(self.CreatePayment(self.m_currencyCtrl.GetValue(), self.m_pvCtrlFarLeg, self.m_pvPayTypeCtrlFarLeg, "Far leg"))        
        
    def GetParameters(self):
        return self.m_parameters
        
    def StoreParameters(self):
        CloseTradeDialogFX.StoreParameters(self)
        self.m_parameters.AtPut( 'faceValueFarLeg', -self.m_faceValueFarLeg )
        self.m_parameters.AtPut( 'premiumFarLeg', self.m_calculatedPremiumFarLeg )
        self.m_parameters.AtPut( 'valueDayFarLeg', self.m_farLegTrade.ValueDay() )
        self.m_parameters.AtPut( 'acquireDayFarLeg', self.m_farLegTrade.AcquireDay() ) 
        
        
# ######################### CloseTradeDialog ####################################
class CloseTradeDialog (CloseTradeDialogBase):
    def __init__(self, trade, connectedTrades):
        CloseTradeDialogBase.__init__(self, trade, connectedTrades)
        self.m_accCtrl = None                           
        self.m_accPayTypeCtrl = None                    
        self.m_legControls = acm.FDictionary()          
        self.m_splitBox = None                          
        self.m_valueDateCtrl = None                   
        self.m_acqDateCtrl = None                         

    def HandleCreate( self, dlg, layout ):
        CloseTradeDialogBase._SetupLayout_(self, dlg, layout)
        if self.m_instrument.InsType() == 'CreditDefaultSwap':
            self.SetAcquireDate(self.m_instrument.CDSEffectiveDate(acm.Time().DateNow()))  
        CloseTradeDialogBase._SetLayoutInitValues_(self)   
        self.m_acqDateCtrl.Editable(False)
        self.m_createPaymentsBox = layout.GetControl('createPaymentsBox')
        self.m_createPaymentsBox.Checked(True)
        self.m_createPaymentsBox.AddCallback( "Activate", OnCreatePaymentsChanged, self )
        if self.m_instrument.Legs().Size() > 1:
            self.m_splitBox = layout.GetControl('splitOnLegsBox')
            self.m_splitBox.Checked(True)
            self.m_splitBox.AddCallback( "Activate", OnSplitChanged, self )               
        self.m_accPayTypeCtrl.SetValue('Interest Accrued')
        if self.m_instrument.Legs().Size() > 1: 
            self.m_pvPayTypeCtrl.Editable(False)
            self.m_accPayTypeCtrl.Editable(False)
            self.m_pvCtrl.Editable(False)
            self.m_accCtrl.Editable(False)    

    def HandleControlChanged(self, binder):
        CloseTradeDialogBase.HandleControlChanged(self, binder)
        
        if binder == self.m_accCtrl:
            OnAccruedInterestChanged(self, None)
        
        if binder == self.m_valueDateCtrl:
            OnValueDateChanged(self, None)
    
    def SetFaceValueAndValueDate(self, valueDate, faceValue):
        CloseTradeDialogBase._SetFaceValueAndValueDate_(self, valueDate, faceValue)
        smallDate = acm.Time().SmallDate()
        acquireDate =  self.GetAcquireDate()
        tradeAcc = self.tradeClone.Calculation().AccruedInterestSpotOverrideSource(self.m_spaceCollection, smallDate, acquireDate, 2).Value()
        self.m_accCtrl.SetValue(tradeAcc)
        self.CalculateAndSetLegValues(self.tradeClone, smallDate, acquireDate)    
        
    def GetPayments(self):
        payments = acm.FArray()
        if self.m_createPaymentsBox.Checked():
            if self.m_instrument.Legs().Size() > 1:
                if self.m_splitBox.Checked():
                    self.StoreLegPayments(payments)
                else:
                    self.StoreInstrumentPayments(payments)
            else:
                self.StoreInstrumentPayments(payments)
        return payments        
        
    def GetPremium(self):
        if not self.m_createPaymentsBox.Checked():
            return self.m_calculatedPremium
        return 0.0        

    def InitControls(self):
        CloseTradeDialogBase._InitControls_(self)
        self.m_pvCtrl = self.CreateDoubleControl('pvCtrl', 2)
        self.m_valueDateCtrl = self.m_bindings.AddBinder( 'valueDateCtrl', acm.GetDomain('date'), None )
        self.m_acqDateCtrl = self.m_bindings.AddBinder( 'acqDateCtrl', acm.GetDomain('date'), None )        
        self.m_accCtrl = self.CreateDoubleControl('accCtrl', 2)
        self.m_accPayTypeCtrl = self.CreatePayTypeControl('accPayTypeCtrl')
        self.InitLegControls()
        
    def InitLegControls(self):
        i = 0
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                dict = acm.FDictionary()
                dict.AtPut(PV, self.CreateDoubleControl(PV + str(i), 2))
                dict.AtPut(ACC, self.CreateDoubleControl(ACC + str(i), 2))
                dict.AtPut(PVPAYTYPE, self.CreatePayTypeControl(PVPAYTYPE + str(i)))
                dict.AtPut(ACCPAYTYPE, self.CreatePayTypeControl(ACCPAYTYPE + str(i)))
                self.m_legControls.AtPut(leg, dict)
                i = i + 1        
        
    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginVertBox('Invisible')
        self.m_valueDateCtrl.BuildLayoutPart(b, 'Value Day')
        self.m_acqDateCtrl.BuildLayoutPart(b, 'Acquire Day')
        self.m_faceValueCtrl.BuildLayoutPart(b, 'Nominal')
        self.m_origFaceValueCtrl.BuildLayoutPart(b, 'Total Nominal')
        b.  EndBox()
        b.  BeginVertBox('Invisible')
        b.  AddCheckbox('createPaymentsBox', 'Create Payments' )
        if self.m_instrument.Legs().Size() > 1:
            b.  AddCheckbox('splitOnLegsBox', 'Split On Legs' )
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Close Out Payments')
        b.    BeginHorzBox()
        self.m_pvCtrl.BuildLayoutPart(b, 'PV')
        self.m_pvPayTypeCtrl.BuildLayoutPart(b, None)
        b.    EndBox()
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                b.    BeginHorzBox()
                legDict = self.m_legControls.At(leg)
                pvCtrl = legDict.At(PV)
                pvPayTypeCtrl = legDict.At(PVPAYTYPE)
                key = ''
                if leg.PayLeg():
                    key = 'Pay Leg PV'
                else:
                    key = 'Receive Leg PV'
                pvCtrl.BuildLayoutPart(b, key)
                pvPayTypeCtrl.BuildLayoutPart(b, None)
                b.    EndBox()
        b.  EndBox()
        b.  AddSpace(5)
        b.  BeginVertBox('EtchedIn', 'Accrued Interest Payments')
        b.    BeginHorzBox()
        self.m_accCtrl.BuildLayoutPart(b, 'Accrued')
        self.m_accPayTypeCtrl.BuildLayoutPart(b, None)
        b.    EndBox()
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                b.    BeginHorzBox()
                legDict = self.m_legControls.At(leg)
                key = ''
                if leg.PayLeg():
                    key = 'Pay Leg Accrued'
                else:
                    key = 'Receive Leg Accrued'
                accCtrl = legDict.At(ACC)
                accPayTypeCtrl = legDict.At(ACCPAYTYPE)
                accCtrl.BuildLayoutPart(b, key)
                accPayTypeCtrl.BuildLayoutPart(b, None)
                b.    EndBox()
        b.  EndBox()
        if self.m_connected.Size():
            b.    BeginVertBox('EtchedIn', 'Connected Trades')
            b.    AddButton('connected', 'Connected...')
            for trade in self.m_connected:
                b.    AddLabel('label' + str(trade.Oid()), '%s, %s' % (trade.Instrument().Name(), str(trade.Oid())))
            b.    EndBox()
        b.  BeginVertBox()
        b.    AddSpace(10)
        b.    BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b
        
    def SetControlValues( self, valueDate, faceValue ):
        if self.m_instrument.InsType() != 'CreditDefaultSwap':
            self.SetAcquireDate(valueDate)
        CloseTradeDialogBase._SetControlValues_(self, valueDate, faceValue)
        
    def CalculateAndSetLegValues(self, tradeClone, accruedStart, accruedEnd):
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                legPV = leg .Calculation().PresentValueSource(self.m_spaceCollection, tradeClone).Value()
                legAcc = leg .Calculation().AccruedInterestSpotOverrideSource(self.m_spaceCollection, tradeClone, accruedStart, accruedEnd, 2).Value()
                legDict = self.m_legControls.At(leg)
                pvCtrl = legDict.At(PV)
                accCtrl = legDict.At(ACC)
                pvCtrl.SetValue(legPV)
                accCtrl.SetValue(legAcc)        
        
    def SetPaymentTypeControls(self): 
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                legDict = self.m_legControls.At(leg)
                pvPayTypeCtrl = legDict.At(PVPAYTYPE)
                accPayTypeCtrl = legDict.At(ACCPAYTYPE)
                pvPayTypeCtrl.SetValue('Termination Fee')
                accPayTypeCtrl.SetValue('Interest Accrued')        
        
    def GetValueDate(self):
        return self.m_valueDateCtrl.GetValue()
        
    def SetValueDate(self, valueDate):
        self.m_valueDateCtrl.SetValue(valueDate)       

    def GetAcquireDate(self):
        return self.m_acqDateCtrl.GetValue()
        
    def SetAcquireDate(self, acquireDate):
        self.m_acqDateCtrl.SetValue(acquireDate)
 
        
# ######################### CloseTradeDialogCurrencySwap #################################### 
class CloseTradeDialogCurrencySwap (CloseTradeDialog):
    def __init__(self, trade, connectedTrades):
        CloseTradeDialog.__init__(self, trade, connectedTrades)

    def HandleCreate( self, dlg, layout ):
        if self.m_instrument.Legs().Size() > 1:
                self.m_nominalSplitBox = layout.GetControl('splitOnNominalsBox')
                self.m_nominalSplitBox.Checked( self.m_instrument.Legs()[0].NominalAtStart() )
                self.m_nominalSplitBox.AddCallback( "Activate", OnNominalSplitChanged, self )     
        CloseTradeDialog.HandleCreate(self, dlg, layout)
        
    def UpdateNominalSplitControls(self, checked):
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                legDict = self.m_legControls.At(leg)
                legDict.At(NOMINAL).Editable(checked)
                legDict.At(NOMINALPAYTYPE).Editable(checked) 

    def InitLegControls(self):
        CloseTradeDialog.InitLegControls(self)
        i = 0
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                legDict = self.m_legControls.At(leg)
                legDict.AtPut(NOMINAL, self.CreateDoubleControl(NOMINAL + str(i), 2))
                legDict.AtPut(NOMINALPAYTYPE, self.CreatePayTypeControl(NOMINALPAYTYPE + str(i)))
                self.m_legControls.AtPut(leg, legDict)
                i = i + 1

    def SetPaymentTypeControls(self): 
        CloseTradeDialog.SetPaymentTypeControls(self)
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                legDict = self.m_legControls.At(leg)
                nominalPayTypeCtrl = legDict.At(NOMINALPAYTYPE)
                nominalPayTypeCtrl.SetValue('Premium')                

    def UpdateSplitControls(self, checked):
        CloseTradeDialog.UpdateSplitControls(self, checked)
        if self.m_instrument.Legs().Size() > 1:
            self.m_nominalSplitBox.Editable( checked )
            for leg in self.m_instrument.Legs():              
                legDict = self.m_legControls.At(leg)
                legDict.At(NOMINAL).Editable(checked and self.m_nominalSplitBox.Checked())
                legDict.At(NOMINALPAYTYPE).Editable(checked and self.m_nominalSplitBox.Checked())

    def UpdateCreatePayments(self, checked):
        CloseTradeDialog.UpdateCreatePayments(self, checked)
        if self.m_instrument.Legs().Size() > 1:
            self.m_nominalSplitBox.Editable( checked )
            for leg in self.m_instrument.Legs():
                legDict = self.m_legControls.At(leg)
                legDict.At(NOMINAL).Editable( checked )
                legDict.At(NOMINALPAYTYPE).Editable( checked )

    def StoreLegPayments(self, payments):
        CloseTradeDialog.StoreLegPayments(self, payments)
        if self.m_instrument.Legs().Size() > 1:
            if self.m_nominalSplitBox.Checked():
                for leg in self.m_instrument.Legs():
                        legDict = self.m_legControls.At(leg)
                        payments.Add(self.CreatePayment(leg.Currency(), legDict.At(NOMINAL), legDict.At(NOMINALPAYTYPE)))
        
    def CalculateAndSetLegValues(self, tradeClone, accruedStart, accruedEnd):
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                scaleAlreadyClosedOut = self.GetRemainingNominal(self.GetValueDate()) / self.m_trade.Nominal()
                legNominalClosedOutScaled = self.m_instrument.NominalAmount() * leg.NominalFactor() * scaleAlreadyClosedOut
                scaleAmountUserWantsToClose = self.m_faceValueCtrl.GetValue() / self.GetRemainingNominal(self.GetValueDate())
                legNominalFloat = legNominalClosedOutScaled * scaleAmountUserWantsToClose
                legPVOriginal = leg .Calculation().PresentValueSource(self.m_spaceCollection, tradeClone).Value()

                if leg.PayLeg():
                    legNominal = acm.DenominatedValue( -legNominalFloat, leg.Currency(), acm.Time().TimeNow() )
                else:
                    legNominal = acm.DenominatedValue( legNominalFloat, leg.Currency(), acm.Time().TimeNow() )

                if self.m_nominalSplitBox.Checked() and leg.NominalAtStart() and self.GetValueDate() > leg.StartDate():
                    legPV = acm.DenominatedValue( legPVOriginal.Number() - legNominal.Number(), legPVOriginal.Unit(), legPVOriginal.DateTime() ) # Remove nominal from PV
                else:
                    legPV = legPVOriginal
                legAcc = leg .Calculation().AccruedInterestSpotOverrideSource(self.m_spaceCollection, tradeClone, accruedStart, accruedEnd, 2).Value()
                legDict = self.m_legControls.At(leg)
                pvCtrl = legDict.At(PV)
                accCtrl = legDict.At(ACC)
                nominalCtrl = legDict.At(NOMINAL)
                pvCtrl.SetValue(legPV)
                accCtrl.SetValue(legAcc)        
                nominalCtrl.SetValue(legNominal)
                nominalCtrl.Editable( self.m_nominalSplitBox.Checked() )
                legDict.At(NOMINALPAYTYPE).Editable( self.m_nominalSplitBox.Checked() )    
                
    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginVertBox('Invisible')
        self.m_valueDateCtrl.BuildLayoutPart(b, 'Value Day')
        self.m_acqDateCtrl.BuildLayoutPart(b, 'Acquire Day')
        self.m_faceValueCtrl.BuildLayoutPart(b, 'Nominal')
        self.m_origFaceValueCtrl.BuildLayoutPart(b, 'Total Nominal')
        b.  EndBox()
        b.  BeginVertBox('Invisible')
        b.  AddCheckbox('createPaymentsBox', 'Create Payments' )
        if self.m_instrument.Legs().Size() > 1:
            b.  AddCheckbox('splitOnLegsBox', 'Split On Legs' )
            b.  AddCheckbox('splitOnNominalsBox', 'Split On Nominals' )
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Close Out Payments')
        b.    BeginHorzBox()
        self.m_pvCtrl.BuildLayoutPart(b, 'PV')
        self.m_pvPayTypeCtrl.BuildLayoutPart(b, None)
        b.    EndBox()
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                b.    BeginHorzBox()
                legDict = self.m_legControls.At(leg)
                pvCtrl = legDict.At(PV)
                pvPayTypeCtrl = legDict.At(PVPAYTYPE)
                nominalCtrl = legDict.At(NOMINAL)
                nominalPayTypeCtrl = legDict.At(NOMINALPAYTYPE)
                key = ''
                if leg.PayLeg():
                    key = 'Pay Leg PV'
                    key2 = 'Pay Leg Nominal'
                else:
                    key = 'Receive Leg PV'
                    key2 = 'Receive Leg Nominal'
                pvCtrl.BuildLayoutPart(b, key)
                pvPayTypeCtrl.BuildLayoutPart(b, None)
                b.    EndBox()
                b.    BeginHorzBox()
                nominalCtrl.BuildLayoutPart(b, key2)
                nominalPayTypeCtrl.BuildLayoutPart(b, None)                
                b.    EndBox()
        b.  EndBox()
        b.  AddSpace(5)
        b.  BeginVertBox('EtchedIn', 'Accrued Interest Payments')
        b.    BeginHorzBox()
        self.m_accCtrl.BuildLayoutPart(b, 'Accrued')
        self.m_accPayTypeCtrl.BuildLayoutPart(b, None)
        b.    EndBox()
        if self.m_instrument.Legs().Size() > 1:
            for leg in self.m_instrument.Legs():
                b.    BeginHorzBox()
                legDict = self.m_legControls.At(leg)
                key = ''
                if leg.PayLeg():
                    key = 'Pay Leg Accrued'
                else:
                    key = 'Receive Leg Accrued'
                accCtrl = legDict.At(ACC)
                accPayTypeCtrl = legDict.At(ACCPAYTYPE)
                accCtrl.BuildLayoutPart(b, key)
                accPayTypeCtrl.BuildLayoutPart(b, None)
                b.    EndBox()
        b.  EndBox()
        if self.m_connected.Size():
            b.    BeginVertBox('EtchedIn', 'Connected Trades')
            b.    AddButton('connected', 'Connected...')
            for trade in self.m_connected:
                b.    AddLabel('label' + str(trade.Oid()), '%s, %s' % (trade.Instrument().Name(), str(trade.Oid())))
            b.    EndBox()
        b.  BeginVertBox()
        b.    AddSpace(10)
        b.    BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b                
        
        
# ######################### Perform close trade ####################################

def OpenClosingTrade(trade):
    initData = acm.TradeActionData().CloseTradeData( trade )
    acm.UX().SessionManager().StartApplication('Instrument Definition', initData)

def GetConnectedTrades(trade):
    trades = acm.FArray()
    if trade.TrxTrade():
        trxTrades = acm.FTrade.Select('trxTrade = %s' % trade.TrxTrade().Oid())
        for trxTrade in trxTrades:
            if not acm.TradeActionUtil().ValidateTradeToClose(trxTrade):
                trades.Add(trxTrade)
        trades.Remove(trade)
    return trades

def InstrumentIsFXForward(instrument):
    return instrument.IsKindOf('FFuture') and instrument.Underlying().IsKindOf('FCurrency') and instrument.PayType() == 'Forward'
    
def InstrumentIsFXODF(instrument):
    return instrument.InsType() == "FXOptionDatedFwd"
    
def InstrumentIsFXCash(trade):
    return trade.IsFXCash() or trade.IsPMCash()

def validateFXForwardTradeToClose(trade):
    now = acm.Time().DateNow()
    if trade.Instrument().IsKindOf('FFuture') and trade.Instrument().ExpiryDate() >= now:
        return True
    if IsActive(trade): 
        return True
    return False

def IsExpired(trade):
    now = acm.Time().DateNow()
    if trade.ValueDay() >= now and trade.AcquireDay() >= now:
        return False
    return True

def IsActive(trade):
    return not IsExpired(trade)

def InstrumentIsFX(trade):
    if InstrumentIsFXForward(trade.Instrument()) or InstrumentIsFXCash(trade) or InstrumentIsFXODF(trade.Instrument()):
        return True
    return False
    
def InstrumentIsCurrencySwap(instrument):
    return instrument.InsType() == "CurrSwap"

def GetCloseTradeDialogForFX(trade, connectedTrades):
    if InstrumentIsFXForward(trade.Instrument()) and validateFXForwardTradeToClose(trade):
        dialog = CloseTradeDialogFX(trade, connectedTrades)

    elif InstrumentIsFXODF(trade.Instrument()):
        dialog = CloseTradeDialogFXODF(trade, connectedTrades)

    elif InstrumentIsFXCash(trade):
        if trade.IsFxSwap():
            nearLegTrade = trade
            farLegTrade = nearLegTrade.FxSwapFarLeg()
            if IsActive(nearLegTrade) and IsActive(farLegTrade): 
                dialog = CloseTradeDialogFXSwap(nearLegTrade, connectedTrades, farLegTrade)
            elif IsExpired(nearLegTrade) and IsActive(farLegTrade):
                dialog = CloseTradeDialogFX(farLegTrade, connectedTrades)
            else:
                dialog = None
        elif IsActive(trade):
            dialog = CloseTradeDialogFX(trade, connectedTrades)
        else:
            dialog = None
    else:
        dialog = None

    return dialog

def QuantityIsDerived(trade, faceValue, premium):
    if trade.QuantityIsDerived() is True:
        temp = faceValue
        faceValue = -premium
        premium = temp
    return faceValue, premium

def CreateClosingTrade(trade, parameters):
    acquireDay = parameters.At('acquireDay')
    valuationDay = parameters.At('valuationDay')
    faceValue = parameters.At('faceValue')
    payments = parameters.At('payments')
    premium = parameters.At('premium')
    faceValue, premium = QuantityIsDerived(trade, faceValue, premium)
    if trade.IsFxSwap():
        nearLegTrade = trade
        farLegTrade = nearLegTrade.FxSwapFarLeg()
        if IsExpired(nearLegTrade):
            acquireDayNearLegTrade = None
            valueDayNearLegTrade = None
            acquireDayFarLegTrade = acquireDay
            valueDayFarLegTrade = valuationDay
            nominalNearLegTrade = 0.0
            nominalFarLegTrade = faceValue
            premiumNearLegTrade = 0.0
            premiumFarLegTrade = premium
            payments = payments
        else:
            acquireDayNearLegTrade = acquireDay
            valueDayNearLegTrade = valuationDay
            acquireDayFarLegTrade = parameters.At('acquireDayFarLeg')
            valueDayFarLegTrade = parameters.At('valueDayFarLeg')
            nominalNearLegTrade = faceValue
            nominalFarLegTrade = parameters.At('faceValueFarLeg')
            premiumNearLegTrade = premium
            premiumFarLegTrade = parameters.At('premiumFarLeg')
            payments = payments
        close = acm.TradeActions().CloseTradeFXSwap(nearLegTrade,
                                                    farLegTrade,
                                                    acquireDayNearLegTrade,
                                                    valueDayNearLegTrade,
                                                    acquireDayFarLegTrade,
                                                    valueDayFarLegTrade,
                                                    nominalNearLegTrade,
                                                    nominalFarLegTrade,
                                                    premiumNearLegTrade,
                                                    premiumFarLegTrade,
                                                    payments,
                                                    IsExpired(nearLegTrade))
    else:
        close = acm.TradeActions().CloseTrade(trade, acquireDay, valuationDay, faceValue, premium, payments)
        if close.Instrument().PayType() == 'Forward':
            close.Premium(0.0)
    return close

def GetDialog(trade, connectedTrades):
    if InstrumentIsFX(trade):
        dialog = GetCloseTradeDialogForFX(trade, connectedTrades)
    elif InstrumentIsCurrencySwap(trade.Instrument()):
        dialog = CloseTradeDialogCurrencySwap(trade, connectedTrades)
    else:
        dialog = CloseTradeDialog(trade, connectedTrades)
    return dialog
            

def CloseTrade(shell, trade, connectedTrades):
    message = acm.TradeActionUtil().ValidateTradeToClose(trade)
    if not message:
        dialog = GetDialog(trade, connectedTrades)
        if dialog == None:
            acm.UX().Dialogs().MessageBoxInformation(shell, "Trade is not available to close.")
        else:
            dialog.InitControls()
            if acm.UX().Dialogs().ShowCustomDialogModal(shell, dialog.CreateLayout(), dialog):
                parameters = dialog.GetParameters()
                close = CreateClosingTrade(trade, parameters)
                OpenClosingTrade(close)
    else:
        acm.UX().Dialogs().MessageBoxInformation(shell, message)

def PerformCloseTrade(eii):
    insdef = eii.ExtensionObject()
    shell = insdef.Shell()
    trade =  insdef.OriginalTrade()
    if trade:
        CloseTrade(shell, trade, GetConnectedTrades(trade))
    else:
        acm.UX().Dialogs().MessageBoxInformation(shell, "Not possible to close an unsaved trade.")
