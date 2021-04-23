"""
DESCRIPTION:
This module is called by Trading Manager column: FRTB SA DRC Validation.
This is used to evaluate/inspect the DRC calculation of a position that
is added to the Trading Manager. The two FRTB columns for DRC calculation
can be selected: "FRTB DRC Bond Equivalent Notional",
"FRTB DRC Bond Equivalent Market Value" to be able to view the calculation
result.
"""
import acm
import FUxCore
import FRTBDynamicDimensions
reload(FRTBDynamicDimensions)

class FRTBValidationParameter( FUxCore.LayoutDialog ):	
    def __init__( self, row, eii, shell):
        self._columnName                = None
        self._rfHierarchySetupControl   = None
        self.row                        = row
        self.eii                        = eii
        self.shell                      = shell
        self._InitDataBindingControls()
        
    def msg_box_ok(self, msg):
        msgBox = acm.GetFunction('msgBox', 3)
        return  msgBox("Warning", msg, 1)
	
    def HandleApply( self ):
        columnName      = self._columnName .GetData()
        rfHierachy      = self._rfHierarchySetupControl.GetValue().Name()
        calcSpace       = acm.Calculations().CreateCalculationSpaceCollection().GetSpace(acm.FPortfolioSheet, acm.GetDefaultContext())
        params = acm.FDictionary()
        params[acm.FSymbol('hierarchy')] = rfHierachy

        try:
            vConfig = acm.Risk.CreateDynamicVectorConfiguration( acm.GetDefaultContext(), 'FRTB DRC Dimensions', params )
            config = acm.Sheet().Column().ConfigurationFromVectorConfiguration( vConfig, None )
            calc = calcSpace.CreateCalculation( self.row, columnName, config )
            acm.StartApplication( 'Valuation Viewer', calc )
        except Exception as e:
            print(e)
    
        return None
        
    def HandleDestroy( self ):
        return None
        
    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()	
        b.BeginVertBox('None')
        b.  AddOption('columnName', 'Column Name*:', 40, 40) 	 	
        self._rfHierarchySetupControl.BuildLayoutPart(b, 'Risk Factor Hierarchy*:')
        b. BeginHorzBox('None')	
        b.  AddButton('ok', 'OK', True)	
        b.  AddButton('cancel', 'Cancel', True)	
        b. EndBox()
        b.EndBox()
        return b
        
    def _InitDataBindingControls(self):
        self._bindings = acm.FUxDataBindings()
        self._rfHierarchySetupControl = self._bindings.AddBinder('rfHieracrhy', acm.GetDomain('FHierarchy'), None)
        self._bindings.AddDependent(self)

    def HandleCreate( self, dlg, layout):
        self.fuxDlg = dlg	
        self.fuxDlg.Caption('FRTB Calculation Parameters')	
        self.layout = layout	
        self.binder = acm.FUxDataBindings()
        gc = self.layout.GetControl
        self._columnName = gc('columnName')
        self._rfHierarchySetupControl.InitLayout(self.layout)
        columnName      = ("FRTB DRC Bond Equivalent Notional", "FRTB DRC Bond Equivalent Market Value")
        
        # Setup drop down lists
        for cn in columnName:
            self._columnName.AddItem(cn)
            

def StartDialogFromMenu(eii):
    shell       = eii.ExtensionObject().Shell()	
    trdManager  = eii.ExtensionObject()	
    sheet       = trdManager.ActiveSheet()	
    selection   = sheet.Selection()	
    selectedCell= selection.SelectedCell()	
    row         = selectedCell.BusinessObject()	
    customDlg   = FRTBValidationParameter(row, eii, shell)	
    result      = acm.UX().Dialogs().ShowCustomDialogModal( shell, customDlg.CreateLayout(), customDlg )


def onActionClick(invokationInfo):
    StartDialogFromMenu(invokationInfo)


def onCreateClick(invokationInfo):
    rowObject = None
    cell      = invokationInfo.Parameter("Cell")
    button    = invokationInfo.Parameter('ClickedButton')
    if cell:
        try:
            rowObject = cell.RowObject()
        except:
            pass
    elif button:
        try:
            rowObject = button.RowObject()
        except:
            pass

    if rowObject and rowObject.IsKindOf(acm.FSingleInstrumentAndTrades):
        return True
        
    return None


def enable(invokationInfo):
    return True

