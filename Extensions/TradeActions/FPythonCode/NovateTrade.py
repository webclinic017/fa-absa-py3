import acm
import math
import FUxCore

def OnConnectedButtonClicked(self, cd):
    self.OpenConnectedTrades()
    
def OnContractTradeButtonClicked(trade, cd):
    acm.UX().SessionManager().StartApplication('Instrument Definition', trade)
        
def OnOkButtonClicked(self, cd):
    self.StoreParameters()
    self.m_fuxDlg.CloseDialogOK()

def OnValueDateChanged(self, cd):
    try:valueDate = self.GetValueDate()
    except Exception as err:return
    faceValue = acm.TradeActionUtil().RemainingNominal(self.m_trade, valueDate, valueDate)
    self.SetControlValues(valueDate, faceValue)

def OnFaceValueChanged(self, cd):
    try:
        faceValue = self.m_faceValueCtrl.GetValue()
    except Exception as err:return
    self.SetFaceValue(faceValue)
    
def OnCreatePaymentsChanged(self, cd):
    self.CreatePaymentsChanged()
    
def OnCounterpartyChanged(self, cd):
    if self.m_counterPartyCtrl.GetValue() is not None:
        self.m_displayNewCounterPartyCtrl.SetValue(self.m_counterPartyCtrl.GetValue().Name())
    
def OnStepOutChanged(self, cd):
    self.StepOutChanged()

def OnCurrencyChanged(self, cd):
    self.UpdatePaymentsWithNewCurrency()

def OnNovatedPaymentChanged(self, cd):
    try:
        self.m_paymentCtrlNovated.GetValue()
    except Exception as err:
        self.m_paymentCtrlNovated.SetValue(0.0)
        
def OnNovatedAssignedPaymentChanged(self, cd):
    try:
        self.m_paymentCtrlNovatedAssigned.GetValue()
    except Exception as err:
        self.m_paymentCtrlNovatedAssigned.SetValue(0.0)
        
    
# ######################### NovationDialogBase ####################################    
class NovationDialogBase (FUxCore.LayoutDialog):
    def __init__(self, trade, contractTrades, connectedTrades):
        self.m_trade = trade
        self.m_contractTrades = contractTrades
        self.m_connected = connectedTrades  
        self.m_instrument = trade.Instrument()
        self.m_parameters = acm.FDictionary()
        self.m_calculatedPremium = 0.0
        self.m_spaceCollection = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        self.m_faceValueCtrl = None
        self.m_origFaceValueCtrl = None
        self.m_counterPartyCtrl = None
        self.m_layout = None
        self.m_okBtn = None
        self.m_cancelBtn = None
        self.m_paymentCtrlNovated = None
        self.m_paymentCtrlNovatedAssigned = None
        self.m_payTypeCtrlNovated = None
        self.m_payTypeCtrlNovatedAssigned = None
        self.m_createPaymentsBox = None
        self.m_stepOutBox = None
        self.m_displayOldCounterPartyCtrl = None
        self.m_displayNewCounterPartyCtrl = None
        self.m_contractTradeBtns = []
        self.FilterContractTrades()
        
    def FilterContractTrades(self):
        if self.m_contractTrades.Size() > 0:
            for contractTrade in self.m_contractTrades:
                if contractTrade.Oid() != self.m_trade.Oid():
                    self.m_contractTradeBtns.append(contractTrade.Oid()) 
    
    def _SetupLayout_(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_layout = layout
        self.m_fuxDlg.Caption( 'Novation for ' + str(self.m_trade.StringKey()) )
        if self.m_connected.Size():
            self.m_connectedBtn = layout.GetControl("connected")
            self.m_connectedBtn.AddCallback( "Activate", OnConnectedButtonClicked, self )
        if len(self.m_contractTradeBtns) > 0:
            for tradeBtnOid in self.m_contractTradeBtns:
                string = 'tradeBtn%s' % str(tradeBtnOid)
                tradeBtn = layout.GetControl(string)
                tradeBtn.AddCallback( "Activate", OnContractTradeButtonClicked, acm.FTrade[tradeBtnOid] )             
        self.m_okBtn = layout.GetControl("ok")
        self.m_okBtn.AddCallback( "Activate", OnOkButtonClicked, self )        
        self.m_bindings.AddLayout(layout)
        self.m_createPaymentsBox = layout.GetControl('createPaymentsBox')
        self.m_createPaymentsBox.Checked(True)
        self.m_createPaymentsBox.AddCallback("Activate", OnCreatePaymentsChanged, self )
        self.m_stepOutBox = layout.GetControl('stepOutBox')
        self.m_stepOutBox.Checked(False)
        self.m_stepOutBox.AddCallback("Activate", OnStepOutChanged, self )  
        self.m_layout.GetControl('counterPartyCtrl').AddCallback( "Changed", OnCounterpartyChanged, self )
        self.m_layout.GetControl('paymentCtrlNovated').AddCallback("Changed", OnNovatedPaymentChanged, self)
        self.m_layout.GetControl('paymentCtrlNovatedAssigned').AddCallback("Changed", OnNovatedAssignedPaymentChanged, self)
    
    def _SetLayoutInitValues_(self):        
        now = acm.Time.DateNow()
        currency = self.m_instrument.Currency()
        calendar = currency.Calendar()
        valueDate = self.GetAdjustedValueDate(now, calendar)
        if acm.Time.DateDifference(valueDate, self.m_trade.ValueDay()) < 0:
            valueDate = self.m_trade.ValueDay()
        self.SetValueDate(valueDate)
        faceValue = acm.TradeActionUtil().RemainingNominal(self.m_trade, valueDate, valueDate)
        self.m_origFaceValueCtrl.SetValue(faceValue)
        self.SetControlValues(valueDate, faceValue)    
        self.m_layout.GetControl('faceValueCtrl').AddCallback( "Changed", OnFaceValueChanged, self )
        self.m_origFaceValueCtrl.Editable(False)
        self.m_displayOldCounterPartyCtrl.Editable(False)
        self.m_displayNewCounterPartyCtrl.Editable(False)
        self.m_displayOldCounterPartyCtrl.SetValue(self.m_trade.Counterparty().Name())
        self.m_payTypeCtrlNovated.SetValue('Termination Fee')
        self.m_payTypeCtrlNovatedAssigned.SetValue('Termination Fee')
        self.m_paymentCtrlNovated.SetValue(0.0)
        self.m_paymentCtrlNovatedAssigned.SetValue(0.0)

    def SortContractTrades(self):
        closingTrades = []
        novatedTrades = []
        novatedAssignedTrades = []
        for trade in self.m_contractTrades:
            if trade.Type() == 'Closing':
                closingTrades.append(trade)
            elif trade.Type() == 'Novated':
                novatedTrades.append(trade)
            elif trade.Type() == 'Novated Assigned':
                novatedAssignedTrades.append(trade)
        
        return [closingTrades, novatedTrades, novatedAssignedTrades]
        
    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        allCounterParties = self.AllCounterParties()
        formatter = acm.Get('formats/InstrumentDefinitionNominalSigDig')
        self.m_faceValueCtrl = self.m_bindings.AddBinder( 'faceValueCtrl', acm.GetDomain('double'), formatter )
        self.m_origFaceValueCtrl = self.m_bindings.AddBinder( 'origFaceValueCtrl', acm.GetDomain('double'), formatter )        
        self.m_counterPartyCtrl = self.m_bindings.AddBinder('counterPartyCtrl', acm.GetDomain('FParty'), None, allCounterParties )
        self.m_displayOldCounterPartyCtrl = self.m_bindings.AddBinder('displayOldCounterPartyCtrl', acm.GetDomain('FParty'), None, allCounterParties )
        self.m_displayNewCounterPartyCtrl = self.m_bindings.AddBinder('displayNewCounterPartyCtrl', acm.GetDomain('FParty'), None, allCounterParties )
        decFormatter = acm.FNumFormatter('myFormatter')
        decFormatter.NumDecimals(2)
        self.m_paymentCtrlNovated = self.m_bindings.AddBinder('paymentCtrlNovated', acm.GetDomain('double'), decFormatter)
        self.m_paymentCtrlNovatedAssigned = self.m_bindings.AddBinder('paymentCtrlNovatedAssigned', acm.GetDomain('double'), decFormatter)
        self.m_payTypeCtrlNovated = self.m_bindings.AddBinder('payTypeCtrlNovated', acm.GetDomain('enum(PaymentType)'), None )
        self.m_payTypeCtrlNovatedAssigned = self.m_bindings.AddBinder('payTypeCtrlNovatedAssigned', acm.GetDomain('enum(PaymentType)'), None )
        
    def GetAdjustedValueDate(self, now, calendar):
        if self.m_instrument.OpenEnd() == 'Open End' and self.m_instrument.IsCashFlowInstrument():
            return self.m_instrument.SuggestOpenEndTerminationDate()
        else:
            return self.m_instrument.SpotDate(now, calendar)

    def _SetControlValues_( self, valueDate, faceValue ):
        self.m_faceValueCtrl.SetValue(faceValue)
        self.SetFaceValueAndValueDate(valueDate, faceValue)
        
    def _SetFaceValueAndValueDate_(self, valueDate, faceValue):
        tradeClone = self.m_trade.Clone()
        tradeClone.ValueDay(valueDate)
        tradeClone.AcquireDay(valueDate)
        tradeClone.FaceValue(faceValue)
        tradeClone.Premium(0.0)
        self.CalculatePremium(tradeClone)
        
    def AllCounterParties( self ):
        allApplicableParties = acm.FArray()
        allApplicableParties.AddAll(acm.FCounterParty.Select('notTrading = False'))
        allApplicableParties.AddAll(acm.FBroker.Select('notTrading = False'))
        allApplicableParties.AddAll(acm.FClient.Select('notTrading = False'))
        allApplicableParties.AddAll(acm.FDepot.Select('notTrading = False'))
        allApplicableParties.AddAll(acm.FMarketPlace.Select('notTrading = False'))
        allApplicableParties.AddAll(acm.FClearingHouse.Select('notTrading = False'))
        return allApplicableParties.AsList()
        
    def StoreParameters(self):
        self.m_parameters.AtPut( 'valuationDay', self.GetValueDate() )
        self.m_parameters.AtPut( 'aquireDay', self.GetValueDate() )
        self.m_parameters.AtPut( 'faceValue', -self.m_faceValueCtrl.GetValue() )        
        self.m_parameters.AtPut( 'counterParty', self.m_counterPartyCtrl.GetValue() )
        self.m_parameters.AtPut( 'premium', -self.m_calculatedPremium )
        self.m_parameters.AtPut( 'novatedPayments', self.GetNovatedPayments() )
        self.m_parameters.AtPut( 'novatedAssignedPayments', self.GetNovatedAssignedPayments() )
        self.m_parameters.AtPut( 'stepOut', self.m_stepOutBox.Checked() )

    def GetParameters(self):
        return self.m_parameters
        
    def SetFaceValue(self, faceValue):
        valueDate = self.GetValueDate()
        self.SetFaceValueAndValueDate(valueDate, faceValue)
        
    def CalculatePremium(self, tradeClone):
        self.m_calculatedPremium = tradeClone.Calculation().PriceToPremium(self.m_spaceCollection, self.GetAcquireDate(), self.m_trade.Price()).Number()
        
    def OpenConnectedTrades(self):
        for trade in self.m_connected:
            acm.UX().SessionManager().StartApplication('Instrument Definition', trade)        

    def CreatePaymentsChanged(self):
        checked = self.m_createPaymentsBox.Checked()
        self.m_paymentCtrlNovated.Editable(checked)
        self.m_payTypeCtrlNovated.Editable(checked)
        if checked == False:
            self.m_paymentCtrlNovatedAssigned.Editable(False)
            self.m_payTypeCtrlNovatedAssigned.Editable(False)
        if checked == True and self.m_stepOutBox.Checked() == False:
            self.m_paymentCtrlNovatedAssigned.Editable(True)
            self.m_payTypeCtrlNovatedAssigned.Editable(True)

    def StepOutChanged(self):
        checked = self.m_stepOutBox.Checked()
        if self.m_createPaymentsBox.Checked():
            self.m_paymentCtrlNovatedAssigned.Editable(not checked)
            self.m_payTypeCtrlNovatedAssigned.Editable(not checked)
            
    def GetNovatedPayments(self):
        payments = acm.FArray()
        if self.m_createPaymentsBox.Checked():
            self.StoreNovatedPayments(payments)
        return payments   
    
    def GetNovatedAssignedPayments(self):
        payments = acm.FArray()
        if self.m_createPaymentsBox.Checked() and not self.m_stepOutBox.Checked():
            self.StoreNovatedAssignedPayments(payments)
        return payments

    def StoreNovatedPayments(self, payments):
        payments.Add(self.CreatePayment(self.m_instrument.Currency(), self.m_paymentCtrlNovated, self.m_payTypeCtrlNovated, False, self.m_trade.Counterparty()))

    def StoreNovatedAssignedPayments(self, payments):
        payments.Add(self.CreatePayment(self.m_instrument.Currency(), self.m_paymentCtrlNovatedAssigned, self.m_payTypeCtrlNovatedAssigned, False, self.m_counterPartyCtrl.GetValue()))

    def CreatePayment(self, currency, amountControl, payTypeControl, payDayIsValueDate, counterParty):
        if amountControl.GetValue() != 0.0:
            payment = acm.FPayment()
            payment.Amount(amountControl.GetValue())
            payment.Type(payTypeControl.GetValue())
            payment.Party(counterParty)
            payment.Currency(currency)
            if payDayIsValueDate:
                payment.PayDay(self.GetValueDate()) 
            else:
                now = acm.Time().DateNow()
                payment.PayDay(now)
            return payment


# ########################### NovationDialogFX ######################################
class NovationDialogFX (NovationDialogBase):
    def __init__(self, trade, contractTrades, connectedTrades):
        NovationDialogBase.__init__(self, trade, contractTrades, connectedTrades)
        self.m_currencyCtrl = None
        self.m_previousCurrency = None
        
    def HandleCreate(self, dlg, layout):
        NovationDialogBase._SetupLayout_(self, dlg, layout)
        self.m_layout.GetControl('currencyCtrl').AddCallback("Changed", OnCurrencyChanged, self)
        self.m_currencyCtrl.SetValue(self.m_trade.Currency())
        self.m_previousCurrency = self.m_currencyCtrl.GetValue()
        NovationDialogBase._SetLayoutInitValues_(self)
        now = acm.Time().DateNow()
        valueDate = self.m_trade.ValueDay()
        if acm.Time.DateDifference(valueDate, now) < 0:
            valueDate = now
        self.SetValueDate(valueDate)
        self.SetAcquireDate(valueDate)

    def StoreParameters(self):
        NovationDialogBase.StoreParameters(self)

    def InitControls(self):
        NovationDialogBase.InitControls(self)
        allCurrencies = self.GetAllCurrencies()
        self.m_currencyCtrl = self.m_bindings.AddBinder('currencyCtrl', acm.GetDomain('FCurrency'), None, allCurrencies)         

    def CreatePaymentsChanged(self):
        self.m_currencyCtrl.Editable(self.m_createPaymentsBox.Checked())
        NovationDialogBase.CreatePaymentsChanged(self)
        
    def GetPriceToPremium(self, value, price):
        tradeClone = self.m_trade.Clone()
        tradeClone.ValueDay(self.m_trade.ValueDay())
        tradeClone.AcquireDay(self.m_trade.ValueDay())
        tradeClone.FaceValue(value)
        tradeClone.Premium(0.0)
        return tradeClone.Calculation().PriceToPremium(self.m_spaceCollection, self.m_trade.ValueDay(), price).Number()

    def UpdatePaymentsWithNewCurrency(self):
        if self.m_currencyCtrl.GetValue() is not None:
            self.SetPaymentToControls(self.m_paymentCtrlNovated, self.m_previousCurrency)
            self.SetPaymentToControls(self.m_paymentCtrlNovatedAssigned, self.m_previousCurrency)
            self.m_previousCurrency = self.m_currencyCtrl.GetValue()
            
    def SetPaymentToControls(self, paymentControl, previousCurrency):
            convertedPayment = self.ConvertToOtherCurrency(paymentControl.GetValue(), previousCurrency)
            paymentControl.SetValue(convertedPayment)

    def ConvertToOtherCurrency(self, paymentValue, previousCurrency):
        if self.m_currencyCtrl.GetValue() != None:
            currRate = 1.0
            if previousCurrency != self.m_currencyCtrl.GetValue():
                currRate = previousCurrency.Calculation().FXRate(self.m_spaceCollection, self.m_currencyCtrl.GetValue()).Number()
                if currRate == 0.0 or math.isnan(currRate) or math.isinf(currRate):
                    currRate = 0.0
                    self.LogZeroFXRate(previousCurrency)
            paymentValue = paymentValue * currRate
        return paymentValue
            
    def LogZeroFXRate(self, previousCurrency):
        acm.Log('FX rate is missing for currency pair %s/%s' % (self.m_currencyCtrl.GetValue().Name(), previousCurrency.Name()))
            
    def StoreNovatedPayments(self, payments):
        payments.Add(self.CreatePayment(self.m_currencyCtrl.GetValue(), self.m_paymentCtrlNovated, self.m_payTypeCtrlNovated, False, self.m_trade.Counterparty()))

    def StoreNovatedAssignedPayments(self, payments):
        payments.Add(self.CreatePayment(self.m_currencyCtrl.GetValue(), self.m_paymentCtrlNovatedAssigned, self.m_payTypeCtrlNovatedAssigned, False, self.m_counterPartyCtrl.GetValue()))

    def SetControlValues(self, valueDate, faceValue):
        self.SetAcquireDate(self.m_trade.ValueDay())
        NovationDialogBase._SetControlValues_(self, valueDate, faceValue)
        
    def SetFaceValueAndValueDate(self, valueDate, faceValue):
        if self.m_trade.QuantityIsDerived():
            self.m_calculatedPremium = self.GetPriceToPremium(faceValue, 1/self.m_trade.Price())
        else:
            self.m_calculatedPremium = self.GetPriceToPremium(faceValue, self.m_trade.Price())
        
    def FilterContractTrades(self):
        NovationDialogBase.FilterContractTrades(self)
        
    def GetAllCurrencies(self):
        allCurrencies = acm.FCurrency.Select('')
        return allCurrencies.AsList()   

    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginVertBox('Invisible')
        self.m_faceValueCtrl.BuildLayoutPart(b, 'Nominal')
        self.m_origFaceValueCtrl.BuildLayoutPart(b, 'Total Nominal')
        self.m_counterPartyCtrl.BuildLayoutPart(b, 'Counterparty')
        b.  EndBox()
        b.  BeginVertBox('Invisible')
        b.  AddCheckbox('stepOutBox', 'Step out')
        b.  AddCheckbox('createPaymentsBox', 'Create fee')
        b.  EndBox()
        b.   BeginVertBox('EtchedIn', 'Novation Payments')
        self.m_currencyCtrl.BuildLayoutPart(b, 'Currency')
        b.    BeginHorzBox()
        self.m_paymentCtrlNovated.BuildLayoutPart(b, 'Fee')
        self.m_payTypeCtrlNovated.BuildLayoutPart(b, None)
        self.m_displayOldCounterPartyCtrl.BuildLayoutPart(b, '')        
        b.    EndBox()
        b.    BeginHorzBox()
        self.m_paymentCtrlNovatedAssigned.BuildLayoutPart(b, 'Fee')
        self.m_payTypeCtrlNovatedAssigned.BuildLayoutPart(b, None)
        self.m_displayNewCounterPartyCtrl.BuildLayoutPart(b, '') 
        b.    EndBox()
        b.  EndBox()
        if self.m_connected.Size():
            b.    BeginVertBox('EtchedIn', 'Connected Trades')
            b.    AddButton('connected', 'Connected...')
            for trade in self.m_connected:
                b.    AddLabel('label' + str(trade.Oid()), '%s, %s' % (trade.Instrument().Name(), str(trade.Oid())))
            b.    EndBox()
            
        if len(self.m_contractTradeBtns) > 0:
            [closingTrades, novatedTrades, novatedAssignedTrades] = self.SortContractTrades()
            b.  BeginHorzBox('EtchedIn', 'Contract trades')
            b.    BeginVertBox()
            b.      AddLabel('closingLabel', 'Closing: ')
            b.      AddLabel('novatedLabel', 'Novated: ')
            b.      AddLabel('novtedAssignedLabel', 'Novated Assigned: ')
            b.    EndBox()
            b.    BeginVertBox()
            b.      BeginHorzBox()
            b.        AddLabel('dummyToFixWindowInYAxis', '')
            for closingTrade in closingTrades:
                b.    AddButton('tradeBtn%s' % str(closingTrade.Oid()), '%s' % (str(closingTrade.Oid())))
            b.      EndBox()
            b.      BeginHorzBox()
            b.        AddLabel('dummyToFixWindowInYAxis', '')
            for novatedTrade in novatedTrades:
                b.    AddButton('tradeBtn%s' % str(novatedTrade.Oid()), '%s' % (str(novatedTrade.Oid())))
            b.      EndBox()
            b.      BeginHorzBox()
            b.        AddLabel('dummyToFixWindowInYAxis', '')
            for novatedAssignedTrade in novatedAssignedTrades:
                b.    AddButton('tradeBtn%s' % str(novatedAssignedTrade.Oid()), '%s' % (str(novatedAssignedTrade.Oid())))
            b.      EndBox()
            b.    EndBox()
            b.  EndBox()
        b.  BeginVertBox()
        b.    AddSpace(10)
        b.    BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.  EndBox()
        b.EndBox()
        return b   

    def GetValueDate(self):
        return self.m_valueDate
        
    def SetValueDate(self, valueDate):
        self.m_valueDate = valueDate

    def GetAcquireDate(self):
        return self.m_acquireDate
        
    def SetAcquireDate(self, acquireDate):
        self.m_acquireDate = acquireDate
        

# ######################### NovationDialogFXSwap ####################################        
class NovationDialogFXSwap (NovationDialogFX):
    def __init__(self, trade, contractTrades, connectedTrades, farLegTrade):
        self.m_farLegTrade = farLegTrade
        self.m_calculatedPremiumFarLeg = None
        self.m_faceValueFarLeg = None
        NovationDialogFX.__init__(self, trade, contractTrades, connectedTrades)

    def StoreParameters(self):
        NovationDialogFX.StoreParameters(self)
        self.m_parameters.AtPut('faceValueFarLeg', -self.m_faceValueFarLeg)
        self.m_parameters.AtPut('premiumFarLeg', -self.m_calculatedPremiumFarLeg)
        self.m_parameters.AtPut('valueDayFarLeg', self.m_farLegTrade.ValueDay())
        self.m_parameters.AtPut('acquireDayFarLeg', self.m_farLegTrade.AcquireDay())

    def GetFarLegPriceToPremium(self, value, price):
        tradeClone = self.m_farLegTrade.Clone()
        tradeClone.ValueDay(self.m_farLegTrade.ValueDay())
        tradeClone.AcquireDay(self.m_farLegTrade.ValueDay())
        tradeClone.FaceValue(value)
        tradeClone.Premium(0.0)
        return tradeClone.Calculation().PriceToPremium(self.m_spaceCollection, self.m_farLegTrade.AcquireDay(), price).Number() 

    def SetFaceValueAndValueDate(self, valueDate, faceValue):
        NovationDialogFX.SetFaceValueAndValueDate(self, valueDate, faceValue)

        if self.m_farLegTrade.QuantityIsDerived():
            scaleFactor = math.fabs(faceValue / self.m_trade.Premium())
            self.m_calculatedPremiumFarLeg = self.GetFarLegPriceToPremium(self.m_farLegTrade.Premium()*scaleFactor, 1/self.m_farLegTrade.Price())
            self.m_faceValueFarLeg = self.m_farLegTrade.Premium() * scaleFactor
        else:
            scaleFactor = math.fabs(faceValue / self.m_trade.Nominal())
            self.m_calculatedPremiumFarLeg = self.GetFarLegPriceToPremium(self.m_farLegTrade.Nominal()*scaleFactor, self.m_farLegTrade.Price())
            self.m_faceValueFarLeg = self.m_farLegTrade.Nominal() * scaleFactor

    def FilterContractTrades(self):
        if self.m_farLegTrade == None:
            NovationDialogFX.FilterContractTrades()
        else:
            for contractTrade in self.m_contractTrades:
                if contractTrade.Oid() != self.m_trade.Oid() and contractTrade.Oid() != self.m_farLegTrade.Oid():
                    self.m_contractTradeBtns.append(contractTrade.Oid())     


# ########################## NovationDialog #####################################            
class NovationDialog (NovationDialogBase):
    def __init__(self, trade, contractTrades, connectedTrades):
        self.m_valueDateCtrl = None                   
        self.m_acqDateCtrl = None        
        NovationDialogBase.__init__(self, trade, contractTrades, connectedTrades)
        
    def InitControls(self):
        NovationDialogBase.InitControls(self)
        self.m_valueDateCtrl = self.m_bindings.AddBinder( 'valueDateCtrl', acm.GetDomain('date'), None )
        self.m_acqDateCtrl = self.m_bindings.AddBinder( 'acqDateCtrl', acm.GetDomain('date'), None )          

    def HandleCreate(self, dlg, layout):        
        NovationDialogBase._SetupLayout_(self, dlg, layout)
        NovationDialogBase._SetLayoutInitValues_(self)
        self.m_acqDateCtrl.Editable(False)
        self.m_layout.GetControl('valueDateCtrl').AddCallback( "Changed", OnValueDateChanged, self )

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginVertBox('Invisible')
        self.m_valueDateCtrl.BuildLayoutPart(b, 'Value Day')
        self.m_acqDateCtrl.BuildLayoutPart(b, 'Acquire Day')        
        self.m_faceValueCtrl.BuildLayoutPart(b, 'Nominal')
        self.m_origFaceValueCtrl.BuildLayoutPart(b, 'Total Nominal')
        self.m_counterPartyCtrl.BuildLayoutPart(b, 'Counterparty')
        b.  EndBox()
        b.  BeginVertBox('Invisible')
        b.  AddCheckbox('stepOutBox', 'Step out')
        b.  AddCheckbox('createPaymentsBox', 'Create fee')
        b.  EndBox()
        b.   BeginVertBox('EtchedIn', 'Novation Payments')
        b.    BeginHorzBox()
        self.m_paymentCtrlNovated.BuildLayoutPart(b, 'Fee')
        self.m_payTypeCtrlNovated.BuildLayoutPart(b, None)
        self.m_displayOldCounterPartyCtrl.BuildLayoutPart(b, '')        
        b.    EndBox()
        b.    BeginHorzBox()
        self.m_paymentCtrlNovatedAssigned.BuildLayoutPart(b, 'Fee')
        self.m_payTypeCtrlNovatedAssigned.BuildLayoutPart(b, None)
        self.m_displayNewCounterPartyCtrl.BuildLayoutPart(b, '') 
        b.    EndBox()
        b.  EndBox()        
        if self.m_connected.Size():
            b.    BeginVertBox('EtchedIn', 'Connected Trades')
            b.    AddButton('connected', 'Connected...')
            for trade in self.m_connected:
                b.    AddLabel('label' + str(trade.Oid()), '%s, %s' % (trade.Instrument().Name(), str(trade.Oid())))
            b.    EndBox()
            
        if len(self.m_contractTradeBtns) > 0:
            [closingTrades, novatedTrades, novatedAssignedTrades] = self.SortContractTrades()
            b.  BeginHorzBox('EtchedIn', 'Contract trades')
            b.    BeginVertBox()
            b.      AddLabel('closingLabel', 'Closing: ')
            b.      AddLabel('novatedLabel', 'Novated: ')
            b.      AddLabel('novtedAssignedLabel', 'Novated Assigned: ')
            b.    EndBox()
            b.    BeginVertBox()
            b.      BeginHorzBox()
            b.        AddLabel('dummyToFixWindowInYAxis', '')
            for closingTrade in closingTrades:
                b.    AddButton('tradeBtn%s' % str(closingTrade.Oid()), '%s' % (str(closingTrade.Oid())))
            b.      EndBox()
            b.      BeginHorzBox()
            b.        AddLabel('dummyToFixWindowInYAxis', '')
            for novatedTrade in novatedTrades:
                b.    AddButton('tradeBtn%s' % str(novatedTrade.Oid()), '%s' % (str(novatedTrade.Oid())))
            b.      EndBox()
            b.      BeginHorzBox()
            b.        AddLabel('dummyToFixWindowInYAxis', '')
            for novatedAssignedTrade in novatedAssignedTrades:
                b.    AddButton('tradeBtn%s' % str(novatedAssignedTrade.Oid()), '%s' % (str(novatedAssignedTrade.Oid())))
            b.      EndBox()
            b.    EndBox()
            b.  EndBox()
        b.  BeginVertBox()
        b.    AddSpace(10)
        b.    BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.  EndBox()
        b.EndBox()
        return b   

    def GetValueDate(self):
        return self.m_valueDateCtrl.GetValue()
        
    def SetValueDate(self, valueDate):
        self.m_valueDateCtrl.SetValue(valueDate)       

    def GetAcquireDate(self):
        return self.m_acqDateCtrl.GetValue()
        
    def SetAcquireDate(self, acquireDate):
        self.m_acqDateCtrl.SetValue(acquireDate)
        
    def SetControlValues(self, valueDate, faceValue):
        if self.m_instrument.InsType() != 'CreditDefaultSwap':
            self.SetAcquireDate(valueDate)
        NovationDialogBase._SetControlValues_(self, valueDate, faceValue)
        
    def SetFaceValueAndValueDate(self, valueDate, faceValue):
        NovationDialogBase._SetFaceValueAndValueDate_(self, valueDate, faceValue)


# ######################### Perform novation ####################################
def GetConnectedTrades(trade):
    trades = acm.FArray()
    if trade.TrxTrade():
        trxTrades = acm.FTrade.Select('trxTrade = %s' % trade.TrxTrade().Oid())
        for trxTrade in trxTrades:
            if not acm.TradeActionUtil().ValidateTradeToClose(trxTrade):
                trades.Add(trxTrade)
        trades.Remove(trade)
    return trades   

def GetContractTrades(orgTrade):
    trades = acm.FArray()
    trades = acm.FTrade.Select('contractTrdnbr = %s and oid > 0' % orgTrade.Oid())
    return trades
     
def OpenClosingTrade(trade):
    trade.InitializeUniqueIdentifiers()
    initData = acm.TradeActionData().CloseTradeData( trade )    
    acm.UX().SessionManager().StartApplication('Instrument Definition', initData)

def OpenNovatedAssignedTrade(trade, artifacts):
    trade.InitializeUniqueIdentifiers()
    businessEventHelper = acm.BusinessEventUtil.CreateBusinessEventHelper(artifacts, trade)
    initData = acm.TradeActionData.GetBusinessEventInitData(businessEventHelper) if businessEventHelper else acm.TradeActionData().CloseTradeData( trade )
    acm.UX().SessionManager().StartApplication('Instrument Definition', initData)

def InstrumentIsFX(trade):
    if InstrumentIsFXForward(trade.Instrument()) or InstrumentIsFXCash(trade):
        return True
    return False
    
def InstrumentIsFXForward(instrument):
    return instrument.IsKindOf('FFuture') and instrument.Underlying().IsKindOf('FCurrency') and instrument.PayType() == 'Forward'
    
def InstrumentIsFXCash(trade):
    return trade.IsFXCash() or trade.IsPMCash()
    
def validateFXForwardTradeToNovate(trade):
    now = acm.Time().DateNow()
    if trade.Instrument().IsKindOf('FFuture') and trade.Instrument().ExpiryDate() >= now:
        return True
    if LegTradeIsNotExpired(trade): 
        return True
    return False
    
def LegTradeIsExpired(trade):
    now = acm.Time().DateNow()
    if trade.ValueDay() >= now and trade.AcquireDay() >= now:
        return False
    return True

def LegTradeIsNotExpired(trade):
    return not LegTradeIsExpired(trade)

def GetFXFarLegTrade(nearLegTrade):
    trades = acm.FArray()
    trades = acm.FTrade.Select('connectedTrdnbr = %s and oid > 0' % nearLegTrade.Oid())
    for trade in trades:
        if nearLegTrade.Oid() != trade.Oid():
            return trade
    return None
    
def TradeIsFXSpotOrForward(nearLegTrade, farLegTrade):
    if farLegTrade == None and LegTradeIsNotExpired(nearLegTrade):
        return True
    return False

def TradeIsFXSwapNearLegExpired(nearLegTrade, farLegTrade):
    if farLegTrade != None and LegTradeIsExpired(nearLegTrade) and LegTradeIsNotExpired(farLegTrade):
        return True
    return False

def TradeIsFXSwapNoLegExpired(nearLegTrade, farLegTrade):
    if farLegTrade != None and LegTradeIsNotExpired(farLegTrade) and LegTradeIsNotExpired(nearLegTrade):
        return True
    return False

def TradeIsFXSwap(trade):
    farLegTrade = GetFXFarLegTrade(trade)
    if farLegTrade != None and (TradeIsFXSwapNearLegExpired(trade, farLegTrade) or TradeIsFXSwapNoLegExpired(trade, farLegTrade)):
        return True
    return False

def GetNovationDialogForFX(trade, contractTrades, connectedTrades):
    if InstrumentIsFXForward(trade.Instrument()) and validateFXForwardTradeToNovate(trade):
            dialog = NovationDialogFX(trade, contractTrades, connectedTrades)

    elif InstrumentIsFXCash(trade):
        farLegTrade = GetFXFarLegTrade(trade)            
        if TradeIsFXSpotOrForward(trade, farLegTrade): 
            dialog = NovationDialogFX(trade, contractTrades, connectedTrades)
        elif TradeIsFXSwapNoLegExpired(trade, farLegTrade):
            dialog = NovationDialogFXSwap(trade, contractTrades, connectedTrades, farLegTrade)
        elif TradeIsFXSwapNearLegExpired(trade, farLegTrade):
            # Since nearLeg is expired, we want the contract trades for the farLeg
            contractTradesFarLeg = GetContractTrades(farLegTrade)
            dialog = NovationDialogFX(farLegTrade, contractTradesFarLeg, connectedTrades)
        else:
            dialog = None
    else:
        dialog = None
        
    return dialog

def QuantityIsDerived(trade, faceValue, premium):
    if trade.QuantityIsDerived() is True:
        temp = faceValue
        faceValue = premium
        premium = temp
    return faceValue, premium

def InstrumentTypeIsNotValidForNovation(instrument):
    if instrument.IsKindOf('FOdf'):
        return True
    return False

class ParameterHolder:
    def __init__(self, dialog, trade):
        parameters = dialog.GetParameters()
        self.acquireDay = parameters.At('aquireDay')
        self.valuationDay = parameters.At('valuationDay')
        self.faceValue = parameters.At('faceValue')
        self.counterParty = parameters.At('counterParty')
        self.premium = parameters.At('premium')
        self.novatedPayments = parameters.At('novatedPayments')
        self.novatedAssignedPayments = parameters.At('novatedAssignedPayments')
        self.stepOut = parameters.At('stepOut')
        self.faceValue, self.premium = QuantityIsDerived(trade, self.faceValue, self.premium)
        if TradeIsFXSwap(trade):
            self.farLegTrade = GetFXFarLegTrade(trade)
            self.acquireDayFarLeg = parameters.At('acquireDayFarLeg')
            self.valueDayFarLeg = parameters.At('valueDayFarLeg')
            self.premiumFarLeg = parameters.At('premiumFarLeg')
            self.faceValueFarLeg = parameters.At('faceValueFarLeg')
            self.faceValueFarLeg, self.premiumFarLeg = QuantityIsDerived(self.farLegTrade, self.faceValueFarLeg, self.premiumFarLeg)
            
def CreateBusinessEventAndLinks(trade, novatedAssignedTrade):
    artifacts = []
    bEvent = acm.FBusinessEvent()
    bEvent.EventType = "Novation"
    artifacts.append(bEvent)
    
    if None != trade:
        origLink = acm.FBusinessEventTradeLink()
        origLink.Trade = trade
        origLink.TradeEventType = "Cancel"
        origLink.BusinessEvent = bEvent
        artifacts.append(origLink)

    if None != novatedAssignedTrade:     
        novatedAssignedLink = acm.FBusinessEventTradeLink()
        novatedAssignedLink.Trade = novatedAssignedTrade
        novatedAssignedLink.TradeEventType = "New"
        novatedAssignedLink.BusinessEvent = bEvent
        artifacts.append(novatedAssignedLink)
        
    return artifacts
        
def OpenNovatedTrades(novateTrades, shell):
    novatedTrade = novateTrades.At('Novated')
    novatedAssignedTrade = novateTrades.At('Novated Assigned')
    if novatedTrade != None and novatedAssignedTrade != None:
        OpenClosingTrade(novatedTrade)
        OpenNovatedAssignedTrade(novatedAssignedTrade, CreateBusinessEventAndLinks(novatedTrade.ContractTrdnbr(), novatedAssignedTrade))
    else:
        acm.UX().Dialogs().MessageBoxInformation(shell, "Not possible to novate trade.")

def OpenStepOutTrade(stepOutTrade, shell):
    if stepOutTrade != None:
        OpenClosingTrade(stepOutTrade)
    else:
        acm.UX().Dialogs().MessageBoxInformation(shell, "Not possible to do novate step out.")    

def PostNovateTradeFXSwap(trade, ph, shell):
    if ph.stepOut is True: 
        stepOutTrade = acm.TradeActions.NovateTradeFXSwapStepOut(trade, ph.farLegTrade, ph.acquireDay, ph.valuationDay, ph.acquireDayFarLeg, ph.valueDayFarLeg, ph.faceValue, ph.faceValueFarLeg, ph.premium, ph.premiumFarLeg, LegTradeIsExpired(trade), ph.novatedPayments)
        OpenStepOutTrade(stepOutTrade, shell)
    else:
        novateTrades = acm.TradeActions.NovateTradeFXSwap(trade, ph.farLegTrade, ph.acquireDay, ph.valuationDay, ph.acquireDayFarLeg, ph.valueDayFarLeg, ph.faceValue, ph.faceValueFarLeg, ph.premium, ph.premiumFarLeg, LegTradeIsExpired(trade), ph.counterParty, ph.novatedPayments, ph.novatedAssignedPayments)
        OpenNovatedTrades(novateTrades, shell)

def PostNovateTradeFXSwapNearLegExpired(trade, ph, shell):
    if ph.stepOut is True:
        stepOutTrade = acm.TradeActions.NovateTradeFXSwapStepOut(trade, ph.farLegTrade, None, None, ph.acquireDay, ph.valuationDay, None, ph.faceValue, None, ph.premium, LegTradeIsExpired(trade), ph.novatedPayments)    
        OpenStepOutTrade(stepOutTrade, shell)
    else:
        novateTrades = acm.TradeActions.NovateTradeFXSwap(trade, ph.farLegTrade, None, None, ph.acquireDay, ph.valuationDay, None, ph.faceValue, None, ph.premium, LegTradeIsExpired(trade), ph.counterParty, ph.novatedPayments, ph.novatedAssignedPayments)
        OpenNovatedTrades(novateTrades, shell)
        
def PostNovateTrade(trade, ph, shell):
    if ph.stepOut is True:
        stepOutTrade = acm.TradeActions.NovateTradeStepOut(trade, ph.acquireDay, ph.valuationDay, ph.faceValue, ph.premium, ph.counterParty, ph.novatedPayments)
        OpenStepOutTrade(stepOutTrade, shell)
    else:
        novateTrades = acm.TradeActions.NovateTrade(trade, ph.acquireDay, ph.valuationDay, ph.faceValue, ph.premium, ph.counterParty, ph.novatedPayments, ph.novatedAssignedPayments)
        if trade.Instrument().PayType() == 'Forward':
            novateTrades.At('Novated').Premium(0.0)
        OpenNovatedTrades(novateTrades, shell)
        
def GetUserParameters(shell, trade, contractTrades, connectedTrades, dialog):
    ph = ParameterHolder(dialog, trade)
    if ph.counterParty == None:
        acm.UX().Dialogs().MessageBoxInformation(shell, "No counterparty set.")
        NovateTrade(shell, trade, contractTrades, connectedTrades)
    else:
        if TradeIsFXSwap(trade) and LegTradeIsExpired(trade):
            PostNovateTradeFXSwapNearLegExpired(trade, ph, shell)
        elif TradeIsFXSwap(trade):
            PostNovateTradeFXSwap(trade, ph, shell)
        else:
            PostNovateTrade(trade, ph, shell)

def NovateTrade(shell, trade, contractTrades, connectedTrades):
    message = acm.TradeActionUtil().ValidateTradeToNovate(trade)
    if not message:
        if InstrumentTypeIsNotValidForNovation(trade.Instrument()):
            acm.UX().Dialogs().MessageBoxInformation(shell, "Instrument type is not applicable for novation.")
            return 
        if InstrumentIsFX(trade):
            dialog = GetNovationDialogForFX(trade, contractTrades, connectedTrades)
        else:
            dialog = NovationDialog(trade, contractTrades, connectedTrades)
            
        if dialog != None:
            dialog.InitControls()
            if acm.UX().Dialogs().ShowCustomDialogModal(shell, dialog.CreateLayout(), dialog):
                GetUserParameters(shell, trade, contractTrades, connectedTrades, dialog)            
        else:
            acm.UX().Dialogs().MessageBoxInformation(shell, "Trade is not available for novation")
    else:
        acm.UX().Dialogs().MessageBoxInformation(shell, message)

def PerformNovateTrade(eii):
    insdef = eii.ExtensionObject()
    shell = insdef.Shell()
    trade =  insdef.OriginalTrade()
    if trade:
        NovateTrade(shell, trade, GetContractTrades(trade), GetConnectedTrades(trade))
    else:
        acm.UX().Dialogs().MessageBoxInformation(shell, "Not possible to novate an unsaved trade.")        
        
