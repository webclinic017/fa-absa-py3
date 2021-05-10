

import acm
import FUxUtils
import FUxCore


from BucketShiftBaseDialog import BucketShiftBaseDialog
from BucketShiftBaseDialog import AsSymbol
from BucketShiftBaseDialog import GetCriteria
from BucketShiftBaseDialog import GetNiceName
from BucketShiftBaseDialog import GetCriteriaTopOnly

diffTypes = ["Absolute % Points", "Relative %"]

class VolatilityBucketShiftDialog (BucketShiftBaseDialog):

    def ShiftLabels(self):
        return [self.m_diffTypeCtrl.GetData()]

    def CriteriaClass( self ):
        return acm.FVolatilityStructure
        
    def __init__(self):
        self.m_diffTypeCtrl = None
        
    def CreateToolTip(self):
        BucketShiftBaseDialog.CreateToolTip( self )
        self.m_diffTypeCtrl.ToolTip("Specify if the shift type should be Absolute number of percentage points or Relative changes in percentage terms.")
        self.m_criteriaBtn.ToolTip( "Specify a filter if shifts should only be applied to a specific set of volatility structures." )
        self.m_criteriaText.ToolTip( "Specify a filter if shifts should only be applied to a specific set of volatility structures." )
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption( 'Steepener - Flattener Volatility' )
        self.m_diffTypeCtrl = layout.GetControl( 'DifferenceType' )
        for d in diffTypes:
            self.m_diffTypeCtrl.AddItem( d )
        self.m_diffTypeCtrl.SetData( self.GetParameter('DifferenceType') )
        BucketShiftBaseDialog.HandleCreate( self, dlg, layout )

    def HandleApply( self ):
        params = BucketShiftBaseDialog.HandleApply( self )
        self.AddParameter( 'DifferenceType', self.m_diffTypeCtrl.GetData() )
        return params
        
    def CreateLayoutImpl(self, builder):
        builder.AddOption('DifferenceType', 'Shift Type')
        
    def InitControls(self):
        pass
        
def ael_custom_dialog_show( shell, params ):
    dialogData = FUxUtils.UnpackInitialData( params )
    customDlg = VolatilityBucketShiftDialog()
    customDlg.AddParameters( dialogData )
    customDlg.InitControls()
    return acm.UX().Dialogs().ShowCustomDialogModal( shell, customDlg.CreateLayout(), customDlg )

def ael_custom_dialog_main( parameters, dictExtra ):
    displayName = GetNiceName( 'Volatility', parameters )
    diffType = parameters[ AsSymbol( 'DifferenceType' ) ]
    timeBuckets = parameters[ AsSymbol( 'Time Buckets' ) ]
    shiftParameters = [[ tb.BucketDate() for tb in timeBuckets ]]
    shifts = parameters[ AsSymbol( 'Shifts' ) ][ AsSymbol( diffType ) ]
    if diffType == "Relative %":
        shiftParameters.append( [1.0 + 0.01 * shifts[tb.AsSymbol()] for tb in timeBuckets] )
    else:
        shiftParameters.append( [1.0 for tb in timeBuckets] )
    if diffType == "Absolute % Points":
        shiftParameters.append( [0.01 * shifts[tb.AsSymbol()] for tb in timeBuckets] )
    else:
        shiftParameters.append( [0.0 for tb in timeBuckets] )
    shiftVector = acm.CreateShiftVector( 'shiftVolatilityPeriods', 'volatility information', GetCriteria( parameters), acm.FVolatilityStructureFilter, GetCriteriaTopOnly( parameters ) )
    shiftVector.AddShiftItem( shiftParameters, displayName )
    return shiftVector
