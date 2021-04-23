import acm
import FUxCore

'''*******************************************************************
*******************************************************************'''   
class SafeResetOfUpdateInProgress():
    def __init__(self, dialog):
        self.m_dialog = dialog
    def __enter__(self):
        self.m_dialog.m_updateInProgress = True
    def __exit__(self, type, value, traceback):
        self.m_dialog.m_updateInProgress = False

'''*******************************************************************
*******************************************************************'''   
class AdjustDepositDialog( FUxCore.LayoutDialog ):
    def __init__( self, ins, shell ):
        self.m_instrumentToAdjust = ins
        self.m_okBtn = 0
        self.m_adjustDate = None
        self.m_adjustAmount = 0.0
        self.m_adjustDateCtrl = 0
        self.m_adjustAmountCtrl = 0
        self.m_shell = shell
        self.m_updateInProgress = False
        
        
    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        self.m_adjustAmountCtrl = self.m_bindings.AddBinder( 'adjustDepositCtrl', acm.GetDomain('double'), None )
        self.m_adjustDateCtrl = self.m_bindings.AddBinder( 'adjustDateCtrl', acm.GetDomain('date'), None )


    def AdjustmentCalendar(self):
        instrument = self.m_instrumentToAdjust
        calendar = None
        if instrument.Legs()[0]:
            calendar = instrument.Legs()[0].PayCalendar()
        if not calendar:
            calendar = instrument.Currency().Calendar()
        return calendar
        
        
    def AskBusinessDayModifyAdjustDate(self):
        instrument = self.m_instrumentToAdjust
        calendar = self.AdjustmentCalendar()
        if calendar.IsNonBankingDay(None, None, self.m_adjustDate ):
            weekDay = acm.Time().DayOfWeek(self.m_adjustDate)
            question = "Value Date is not a valid business day, ("+weekDay+"), according to the "+calendar.Name()+" calendar."
            button = acm.UX().Dialogs().MessageBox(self.m_shell, "Question", question, "Ok", "Adjust", None, 'Button1', 'Button3' )
            if button == 'Button2':
                self.m_adjustDate = calendar.ModifyDate(None, None, self.m_adjustDate, "Following")
                self.UpdateControls()
                
                
    def ValidateAdjustDateInLegRange(self):
        leg = self.m_instrumentToAdjust.Legs()[0]
        errorStr = None
        if leg:
            if acm.Time().DateDifference(self.m_adjustDate, leg.StartDate()) < 0:
                errorStr = "The Adjust Value Date is prior to the Start Date."
            elif acm.Time().DateDifference(self.m_adjustDate, leg.EndDate()) > 0:
                errorStr = "The Adjust Value Date is after the End Date."
        if errorStr:
            acm.UX().Dialogs().MessageBox(self.m_shell, "Error", errorStr, "Ok", None, None, 'Button1', 'Button1')
            return False
        return True
            
    
    def ValidateAdjustDateBeforeNoticeDate(self):
        leg = self.m_instrumentToAdjust.Legs()[0]
        if leg:
            if acm.Time().DateDifference(self.m_adjustDate, self.m_instrumentToAdjust.AdjustDepositDefaultValueDate()) < 0:
                question = "Value Date is prior to the Notice Day."
                button = acm.UX().Dialogs().MessageBox(self.m_shell, "Information", question, "Ok", "Adjust", None, 'Button1', 'Button3' )
                if button == 'Button2':
                    self.m_adjustDate = self.m_instrumentToAdjust.AdjustDepositDefaultValueDate()
                    self.UpdateControls()
      
      
    def ValidateAdjustDateOnApply(self):
        if self.ValidateAdjustDateInLegRange():
            return True
        return False
            
    
    def ValidateAdjustDate(self, newAdjustDate):
        self.m_adjustDate = newAdjustDate
        self.ValidateAdjustDateBeforeNoticeDate()
        self.AskBusinessDayModifyAdjustDate()
        
        
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        if str(aspectSymbol) == 'ControlValueChanged':
            if not self.m_updateInProgress:
                if parameter == self.m_adjustDateCtrl:
                    with SafeResetOfUpdateInProgress(self):
                        self.ValidateAdjustDate(self.m_adjustDateCtrl.GetValue())
                if parameter == self.m_adjustAmountCtrl:
                    with SafeResetOfUpdateInProgress(self):
                        self.m_adjustAmount = self.m_adjustAmountCtrl.GetValue()
        
    def PopulateData( self ):
        self.m_adjustAmount = 0.0
        self.m_adjustDate = self.m_instrumentToAdjust.AdjustDepositDefaultValueDate()
        self.UpdateControls()
        
        
    def HandleApply( self ):
        if self.ValidateAdjustDateOnApply():
            if self.CommitAdjustDeposit() == 1:
                self.m_fuxDlg.CloseDialogCancel()
                return
                    
        
    def CommitAdjustDeposit( self ):
        adjustDepositAmount = self.m_adjustAmountCtrl.GetValue()
        adjustDepositDate = self.m_adjustDateCtrl.GetValue()
        adjustDepositQuantity = self.AdjustDepositQuantity()
        if( not self.m_instrumentToAdjust.AdjustDeposit(adjustDepositAmount, adjustDepositDate, adjustDepositQuantity) ):
            acm.UX().Dialogs().MessageBox(self.m_shell, "Error", "Could not adjust deposit", "Ok", None, None, 'Button1', 'Button3' )
        else:
            return 1
            
    def AdjustDepositQuantity( self ):
        trade = None
        for t in self.m_instrumentToAdjust.Trades():
            if not t.MirrorTrade() or  not t.IsEqual(t.MirrorTrade()):
                trade = t
                break
        
        return trade.Quantity()
        
        
    def UpdateControls(self):
        self.m_adjustAmountCtrl.SetValue(self.m_adjustAmount) 
        self.m_adjustDateCtrl.SetValue(self.m_adjustDate)


    def HandleCreate( self, dlg, layout ):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption( 'Adjust Deposit' )  
        self.m_bindings.AddLayout( layout )
        self.m_okBtn = layout.GetControl( "ok" )
        self.PopulateData()
        
        
    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox( 'None' )
        b.      BeginVertBox( 'Invisible' )
        self.m_adjustDateCtrl.BuildLayoutPart( b, 'Value Date' )
        self.m_adjustAmountCtrl.BuildLayoutPart( b, 'Amount' )
        b.      EndBox()
        b.      BeginHorzBox( 'Invisible' )
        b.              AddFill()
        b.              AddButton( 'ok', 'OK' )
        b.              AddButton( 'cancel', 'Cancel' )
        b.      EndBox()
        b.EndBox()
        return b


def ReallyStartDialog( shell, ins ):
    adjustDepositDlg = AdjustDepositDialog( ins, shell )
    adjustDepositDlg.InitControls()
    acm.UX().Dialogs().ShowCustomDialogModal( shell, adjustDepositDlg.CreateLayout(), adjustDepositDlg )

'''*******************************************************************
*******************************************************************'''
class CallDepositMenuItemTM(FUxCore.MenuItem):
    def __init__(self, extObj):
        self.m_extObj = extObj
    
    def IsMenuApplicable(self, extObj):
        applicable = False
        try:
            instrument = extObj.ActiveSheet().Selection().SelectedCell().RowObject().Instrument()
        except:
            instrument = None
            
        if instrument:
            if instrument.IsCallAccount():
                if instrument.Trades().Size() == 1:
                    applicable = True
        return applicable
            
    def Invoke(self, eii):
        extObj = eii.ExtensionObject()
        if self.IsMenuApplicable(extObj):
            ins = extObj.ActiveSheet().Selection().SelectedCell().RowObject().Instrument()
            shell = eii.ExtensionObject().Shell()
            ReallyStartDialog( shell, ins )
        else:
            error = "Adjust Deposit only valid for call deposits with exactly one trade"
            acm.UX().Dialogs().MessageBox(eii.ExtensionObject().Shell(), "Error", error, "Ok", None, None, 'Button1', 'Button3' )
    
    def Applicable(self):
        return self.IsMenuApplicable(self.m_extObj)
        

def CreateCallDepositMenuItemTM(extObj):
    return CallDepositMenuItemTM(extObj)

'''*******************************************************************
*******************************************************************'''
class CallDepositMenuItemInsDef(FUxCore.MenuItem):
    def __init__(self, extObj):
        self.m_extObj = extObj
    
    def IsMenuEnabled(self, extObj):
        enabled = False
        trade = extObj.OriginalTrade()
        if trade:
            isCall = trade.Instrument().IsCallAccount()
            voided = trade.Status() == "Void" or trade.Status() == "Confirmed Void"
            enabled = isCall and not voided
        return enabled
        
    def Invoke(self, eii):
        extObj = eii.ExtensionObject()
        if self.IsMenuEnabled(extObj):
            ins = extObj.OriginalTrade().Instrument()
            shell = eii.ExtensionObject().Shell()
            ReallyStartDialog( shell, ins )
        else:
            error = "Adjust Deposit only valid for call deposits with exactly one trade"
            acm.UX().Dialogs().MessageBox(eii.ExtensionObject().Shell(), "Error", error, "Ok", None, None, 'Button1', 'Button3' )
        
    def Enabled(self):
        return self.IsMenuEnabled(self.m_extObj)
        
    def Applicable(self):
        return True

def CreateCallDepositMenuItemInsDef(extObj):
    return CallDepositMenuItemInsDef(extObj)
    
'''*******************************************************************
*******************************************************************'''
