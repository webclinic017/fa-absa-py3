"""
DESCRIPTION:
This module is called by Trading Manager column: FRTB SA SBA Validation.
This is used to evaluate/inspect the SBA calculation of a position that
is added to the Trading Manager. Any one of the RiskClasses and 
Measure Types can be selected witht he hierarchy and risk factor setup
to see the calculation results.
"""
import acm
import FUxCore
import FRTBDynamicDimensions
reload(FRTBDynamicDimensions)

class FRTBValidationParameter( FUxCore.LayoutDialog ):	
    def __init__( self, row, eii, shell):
        self._measureControl            = None
        self._riskClassControl          = None
        self._rfSetupControl            = None
        self._rfHierarchySetupControl   = None
        self.row                        = row
        self.eii                        = eii
        self.shell                      = shell
        self._InitDataBindingControls()
        
    def msg_box_ok(self, msg):
        msgBox = acm.GetFunction('msgBox', 3)
        return  msgBox("Warning", msg, 1)
	
    def HandleApply( self ):
        measureType     = self._measureControl.GetData()
        riskClass       = self._riskClassControl.GetData() 
        rfSetup         = self._rfSetupControl.GetValue().Name()
        rfHierachy      = self._rfHierarchySetupControl.GetValue().Name()
        calcSpace       = acm.Calculations().CreateCalculationSpaceCollection().GetSpace(acm.FPortfolioSheet, acm.GetDefaultContext())
        params = acm.FDictionary()
        params[acm.FSymbol("measureType")] = measureType
        params[acm.FSymbol("riskClass")] = riskClass
        params[acm.FSymbol('rfsetup')] = rfSetup
        params[acm.FSymbol('hierarchy')] = rfHierachy

        try:
            vConfig = acm.Risk.CreateDynamicVectorConfiguration( acm.GetDefaultContext(), 'FRTB Dynamic Dimensions', params )
            config = acm.Sheet().Column().ConfigurationFromVectorConfiguration( vConfig, None )
            calc = calcSpace.CreateCalculation( self.row, 'FRTB Measure', config )
            acm.StartApplication( 'Valuation Viewer', calc )
        except Exception as e:
            print(e)
    
        return None
        
    def HandleDestroy( self ):
        return None
        
    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()	
        b.BeginVertBox('None')
        b.  AddOption('riskClass', 'Risk Class*:', 40, 40) 	 	
        b.  AddOption('measureType', 'Risk Class*:')
        self._rfSetupControl.BuildLayoutPart(b, 'Risk Factor Setup*:')
        self._rfHierarchySetupControl.BuildLayoutPart(b, 'Risk Factor Hierarchy*:')
        b. BeginHorzBox('None')	
        b.  AddButton('ok', 'OK', True)	
        b.  AddButton('cancel', 'Cancel', True)	
        b. EndBox()
        b.EndBox()
        return b
        
    def _InitDataBindingControls(self):
        self._bindings = acm.FUxDataBindings()
        self._rfSetupControl = self._bindings.AddBinder('rfSetup', acm.GetDomain('FRiskFactorSetup'), None)
        self._rfHierarchySetupControl = self._bindings.AddBinder('rfHieracrhy', acm.GetDomain('FHierarchy'), None)
        self._bindings.AddDependent(self)

    def HandleCreate( self, dlg, layout):
        self.fuxDlg = dlg	
        self.fuxDlg.Caption('FRTB Calculation Parameters')	
        self.layout = layout	
        self.binder = acm.FUxDataBindings()
        gc = self.layout.GetControl
        self._riskClassControl          = gc('riskClass')
        self._measureControl            = gc('measureType')
        self._rfSetupControl.InitLayout(self.layout)
        self._rfHierarchySetupControl.InitLayout(self.layout)
        riskClass       = acm.FChoiceList['FRTB SA Risk Class'].Choices()
        riskMeasure     = ("Delta", "Vega", "Curvature Up", "Curvature Down")
        
        # Setup drop down lists
        for rm in riskMeasure:
            self._measureControl.AddItem(rm)
        for rc in riskClass:
            self._riskClassControl.AddItem(rc)
            

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

