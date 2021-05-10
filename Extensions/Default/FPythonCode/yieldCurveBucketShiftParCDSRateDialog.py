
import acm
import FUxUtils
import FUxCore

from yieldCurveBucketShiftBaseDialog import YieldCurveBucketBaseDialog
from yieldCurveBucketShiftBaseDialog import TransformOldParameters
from yieldCurveBucketShiftBaseDialog import CreateShiftParameters
from BucketShiftBaseDialog import AsSymbol

class yieldCurveBucketShiftParCDSRateDialog (YieldCurveBucketBaseDialog):

    def __init__( self ):
        YieldCurveBucketBaseDialog.__init__(self)
        self.m_shiftFloorCtrl = None
    
    def CreateToolTip( self ):
        YieldCurveBucketBaseDialog.CreateToolTip( self )
        self.m_shiftFloorCtrl.ToolTip( "Credit spread curve values, expressed as Par CDS Rates in Act/360 and Quarterly, will not be shifted below this floor value." )

    def HandleApply( self ):
        params = YieldCurveBucketBaseDialog.HandleApply( self )
        self.AddParameter( 'Floor', self.m_shiftFloorCtrl.GetValue() )
        return params

    def HandleCreate( self, dlg, layout ):
        YieldCurveBucketBaseDialog.HandleCreate( self, dlg, layout )
        self.m_shiftFloorCtrl.SetValue( self.GetParameter( 'Floor' ) )
        self.m_fuxDlg.Caption( 'Steepener - Flattener Par CDS Rate Shifts' )

    def CreateLayoutImpl( self, builder ):
        YieldCurveBucketBaseDialog.CreateLayoutImpl( self, builder )
        self.m_shiftFloorCtrl.BuildLayoutPart( builder, 'Floor (bps)' )
        
    def InitControls( self ):
        YieldCurveBucketBaseDialog.InitControls( self )
        self.m_shiftFloorCtrl = self.m_bindings.AddBinder( 'Floor', acm.GetDomain('double'), None )

def ael_custom_dialog_show( shell, params ):
    dialogData = FUxUtils.UnpackInitialData( params )
    customDlg = yieldCurveBucketShiftParCDSRateDialog()
    TransformOldParameters( dialogData )
    customDlg.AddParameters( dialogData )
    customDlg.InitControls()
    return acm.UX().Dialogs().ShowCustomDialogModal( shell, customDlg.CreateLayout(), customDlg )

def ael_custom_dialog_main( parameters, dictExtra ):
    displayName = 'Par CDS Rate Bucket Shift'
    TransformOldParameters( parameters )
    shiftVector = acm.CreateShiftVector( 'shiftCurveParCDSRatePeriods', 'credit yield curve', None )
    shiftParameters = CreateShiftParameters( parameters )
    shiftParameters.append( parameters.At( AsSymbol( 'Floor' ) ) ) 
    shiftVector.AddShiftItem( shiftParameters, displayName )
    return shiftVector
