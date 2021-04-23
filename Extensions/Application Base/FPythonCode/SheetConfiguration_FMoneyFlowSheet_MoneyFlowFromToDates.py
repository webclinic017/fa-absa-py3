
import acm
import FUxCore

def ael_custom_dialog_show(shell, params):
    result = None
    if params:
        mfDatePair = params['moneyFlowFromToDatePair']
        mfSettlementTypes = params['moneyFlowSettlementTypes']
    return ShowMoneyFlowDatePeriodDialog( shell, mfDatePair, mfSettlementTypes )
    

def ael_custom_dialog_main( parameters, dictExtra ):
    mfDatePair = parameters['moneyFlowFromToDatePair']
    settlementTypes = parameters['moneyFlowSettlementTypes']
    extensionObject = dictExtra['customData'].ExtensionObject()
    extensionObject.ColumnSetupExtensionAttribute('_defaultColumnsMoneyFlowSheet')    
    extensionObject.MoneyFlowFromToDatePair(mfDatePair)
    extensionObject.MoneyFlowSettlementTypes(settlementTypes)
    return extensionObject


def ShowMoneyFlowDatePeriodDialog( shell, mfDatePair, mfSettlementTypes ):
    dlg = MoneyFlowDatePeriodDialog( shell, mfDatePair, mfSettlementTypes )
    return acm.UX().Dialogs().ShowCustomDialogModal( shell, dlg.CreateLayout(), dlg )    

def OnCheckChangedCB(self, cd):
    self.UpdateControls()

def OnToggleAllSettlementsCB(self, cd):
    checked = self.m_allSettlementTypes.Checked()
    root = self.m_settlementTypesCtrl.GetRootItem()
    for child in root.Children():
        child.Check(checked)
    self.UpdateControls()

class MoneyFlowDatePeriodDialog( FUxCore.LayoutDialog ):

    def __init__( self, shell, mfDatePair, mfSettlementTypes ):

        self.m_okBtn = 0
        self.m_mfDatePair = mfDatePair
        self.m_mfSettlementTypes = mfSettlementTypes
        self.m_shell = shell
        self.m_fromDate = 0
        self.m_toDate = 0
        self.m_caption = "Include Money Flows"
        self.m_settlementTypes = acm.GetDomain('enum(SettlementCashFlowType)')
        self.InitControls()

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        pass

    
    def HandleApply( self ):

        if self.m_settlementTypesCtrl.CheckedCount() == 0:
            acm.UX().Dialogs().MessageBoxInformation(self.m_shell, 'At least one Settlement Type must be selected.')
            return None
            
        params = acm.FDictionary()
        fromDate = self.m_fromDate.GetValue()
        toDate = self.m_toDate.GetValue()
        if not toDate:
            toDate = ""
        if not fromDate:
            fromDate = ""
        datePair = acm.FPair()
        datePair.First( fromDate )
        datePair.Second( toDate )
        
        params.AtPut('moneyFlowFromToDatePair', datePair)
        
        includeSettlementTypes = acm.FArray()
        for child in self.m_settlementTypesCtrl.GetCheckedItems():
            includeSettlementTypes.Add(self.m_settlementTypes.Enumeration(child.GetData()))
        
        params.AtPut('moneyFlowSettlementTypes', includeSettlementTypes)
        
        return params

    def HandleCreate( self, dlg, layout):

        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)
        self.m_bindings.AddLayout(layout)

        if self.m_mfDatePair:
            fromDate = str( self.m_mfDatePair.First() )
            toDate = str( self.m_mfDatePair.Second() )
            self.m_fromDate.SetValue(fromDate)
            self.m_toDate.SetValue(toDate)
        
        self.m_fromDate.ToolTip("Date period specifying the time span for money flows to be inserted")
        self.m_toDate.ToolTip("Date period specifying the time span for money flows to be inserted")
   
        self.m_settlementTypesCtrl = layout.GetControl('settlementTypes')
        self.m_settlementTypesCtrl.Populate( self.m_settlementTypes.Values().Sort() )
        self.m_settlementTypesCtrl.ShowCheckboxes()
        
        rootItem = self.m_settlementTypesCtrl.GetRootItem()
        for child in rootItem.Children():
            child.Check(True)
            
        self.m_allSettlementTypes = layout.GetControl('allSettlementTypes')
        self.m_settlementTypesCtrl.AddCallback('ItemCheckStateChanged', OnCheckChangedCB, self)
        self.m_allSettlementTypes.AddCallback('Activate', OnToggleAllSettlementsCB, self)
        
        self.UpdateControls()

    def UpdateControls( self ):
        if self.m_settlementTypesCtrl.CheckedCount() == 0:
            self.m_allSettlementTypes.SetCheck('Unchecked')
        elif self.m_settlementTypesCtrl.CheckedCount() == self.m_settlementTypesCtrl.ItemCount():
            self.m_allSettlementTypes.SetCheck('Checked')
        else:
            self.m_allSettlementTypes.SetCheck('Indeterminate')

    def InitControls(self):

        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        self.m_fromDate = self.m_bindings.AddBinder( 'fromDate', acm.GetDomain('FDatePeriod') )
        self.m_toDate = self.m_bindings.AddBinder( 'toDate', acm.GetDomain('FDatePeriod') )
        
    def CreateLayout( self ):

        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('Invisible')
        b.    BeginVertBox('None')
        
        self.m_fromDate.BuildLayoutPart(b, 'From')
        self.m_toDate.BuildLayoutPart(b, 'To')
        
        b.    EndBox()
        b.    BeginVertBox('None')
        
        b.      AddLabel('settlementTypesLabel', 'Settlement Types:')
        b.      AddList('settlementTypes', -1, -1, -1, -1)
        b.      AddCheckbox('allSettlementTypes', 'Toggle all settlement types')
        
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.          AddFill()
        b.          AddButton('ok', 'OK')
        b.          AddButton('cancel', 'Cancel')
        b.  EndBox()

        b.EndBox()
        

        return b
