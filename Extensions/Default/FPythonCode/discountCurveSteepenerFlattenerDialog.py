
import acm
import FUxUtils
import FUxCore

from yieldCurveBucketShiftZeroCouponDialog import YieldCurveBucketShiftZeroCouponDialog
from yieldCurveBucketShiftBaseDialog import TransformOldParameters
from yieldCurveBucketShiftBaseDialog import CreateShiftParameters
from BucketShiftBaseDialog import GetCriteria
from BucketShiftBaseDialog import GetNiceName
from BucketShiftBaseDialog import AsSymbol
from BucketShiftBaseDialog import GetCriteriaTopOnly

def ael_custom_dialog_show( shell, params ):
    dialogData = FUxUtils.UnpackInitialData( params )
    customDlg = YieldCurveBucketShiftZeroCouponDialog()
    TransformOldParameters( dialogData )
    customDlg.AddParameters( dialogData )
    customDlg.InitControls()
    return acm.UX().Dialogs().ShowCustomDialogModal( shell, customDlg.CreateLayout(), customDlg )

def ael_custom_dialog_main( parameters, dictExtra ):
    displayName = GetNiceName( 'Zero Coupon Bucket Shift', parameters )
    TransformOldParameters( parameters )
    shiftVector = acm.CreateShiftVector( 'shiftCurveZeroCouponPeriods', 'discount curve', GetCriteria( parameters ), acm.FYieldCurveFilter, GetCriteriaTopOnly( parameters ) )
    shiftParameters = CreateShiftParameters( parameters )
    shiftParameters.append( parameters.At( AsSymbol( 'ShiftShape' ) ) or 'Rectangle' )
    shiftParameters.append( parameters.At( AsSymbol( 'Floor' ) ) )
    shiftVector.AddShiftItem( shiftParameters, displayName )
    return shiftVector

