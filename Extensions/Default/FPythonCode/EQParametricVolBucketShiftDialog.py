

import acm
import FUxUtils
import FUxCore


from BucketShiftBaseDialog import BucketShiftBaseDialog
from BucketShiftBaseDialog import AsSymbol
from BucketShiftBaseDialog import GetCriteria
from BucketShiftBaseDialog import GetNiceName
from BucketShiftBaseDialog import GetCriteriaTopOnly

skewParams = ["ATM Vol", "ATM Ref", "Slope", "Curve L", "Curve R", "Cutoff L", "Cutoff R", "Left Wing", "Right Wing"]

class EQParametricVolBucketShiftDialog (BucketShiftBaseDialog):

    def SelectItems(self):
        shifts = self.GetParameter( 'Shifts' )
        if shifts:
            items = []
            for key in shifts.Keys():
                for listitem in self.m_paramCtrl.GetRootItem().Children():
                    if AsSymbol( listitem.GetData() ) == AsSymbol( key ):
                        items.append( listitem )
            self.m_paramCtrl.SetSelectedItems( items )
    
    def ShiftLabels(self):
        return [item.GetData() for item in self.m_paramCtrl.GetSelectedItems()]
        
    def CriteriaClass( self ):
        return acm.FVolatilityStructure
        
    def __init__(self):
        self.m_bindings = None
        self.m_diffTypeCtrl = None
        self.m_paramCtrl = None
        
    def CreateToolTip(self):
        BucketShiftBaseDialog.CreateToolTip( self )
        self.m_diffTypeCtrl.ToolTip("Set whether Absolute or Relative shifts should be applied.")
        self.m_paramCtrl.ToolTip("Set which parameters should be shifted.")
        self.m_criteriaBtn.ToolTip( "Specify a filter if shifts should only be applied to a specific set of volatility structures." )
        self.m_criteriaText.ToolTip( "Specify a filter if shifts should only be applied to a specific set of volatility structures." )
        
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption( 'Steepener - Flattener Volatility' )
        self.m_bindings.AddLayout(layout)
        self.m_paramCtrl = layout.GetControl('Parameters')
        self.m_paramCtrl.EnableMultiSelect( True )
        self.m_paramCtrl.Populate( skewParams )
        self.m_diffTypeCtrl.SetValue( self.GetParameter('DifferenceType') )
        self.SelectItems()
        BucketShiftBaseDialog.HandleCreate( self, dlg, layout )

    def HandleApply( self ):
        params = BucketShiftBaseDialog.HandleApply( self )
        self.AddParameter( 'DifferenceType', self.m_diffTypeCtrl.GetValue() )
        return params
        
    def CreateLayoutImpl(self, builder):
        self.m_diffTypeCtrl.BuildLayoutPart( builder, 'Shift Type' )
        builder.AddList( 'Parameters' )
        
    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        domain = acm.GetDomain('enum(ParametricShiftType)')
        self.m_diffTypeCtrl = self.m_bindings.AddBinder( 'DifferenceType', domain, None, domain.Enumerators()[1:] )

def ael_custom_dialog_show( shell, params ):
    dialogData = FUxUtils.UnpackInitialData( params )
    customDlg = EQParametricVolBucketShiftDialog()
    customDlg.AddParameters( dialogData )
    customDlg.InitControls()
    return acm.UX().Dialogs().ShowCustomDialogModal( shell, customDlg.CreateLayout(), customDlg )

def ael_custom_dialog_main( parameters, dictExtra ):
    displayName = GetNiceName( 'EQ Param Vol', parameters )
    shiftParameters = [parameters.At( AsSymbol( 'DifferenceType' ) )]
    for key in skewParams:
        storedShifts = parameters[ AsSymbol( 'Shifts' ) ][ AsSymbol( key ) ]
        shifts = None
        if storedShifts:
            shifts = [storedShifts[ tb.AsSymbol() ] and float(storedShifts[ tb.AsSymbol() ]) or 0.0 for tb in parameters[ AsSymbol( 'Time Buckets' ) ] ]
        shiftParameters.append( shifts )
    shiftParameters.append( [tb.BucketDate() for tb in parameters[ AsSymbol( 'Time Buckets' ) ] ] )
    shiftVector = acm.CreateShiftVector( 'shiftEqSkewsPeriods', 'volatility information', GetCriteria( parameters ), acm.FVolatilityStructureFilter, GetCriteriaTopOnly( parameters ) )

    shiftVector.AddShiftItem( shiftParameters, displayName )
    return shiftVector


