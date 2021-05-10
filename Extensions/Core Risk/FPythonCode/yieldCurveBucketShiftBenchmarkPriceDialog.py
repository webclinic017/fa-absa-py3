
import acm
import FUxUtils
import FUxCore
import string

from BucketShiftBaseDialog import BucketShiftBaseDialog
from BucketShiftBaseDialog import AsSymbol
from BucketShiftBaseDialog import GetCriteria
from BucketShiftBaseDialog import GetNiceName
from BucketShiftBaseDialog import GetCriteriaTopOnly

def TransformOldParameters( parameters ):
    if parameters.Size() == 0 or parameters.HasKey( AsSymbol( 'Shifts' ) ):
        pass
    else:
        newParameters = acm.FDictionary()
        newParameters.AtPut( AsSymbol( 'Time Buckets' ), parameters[ 'Time Buckets' ] )
        newParameters.AtPut( AsSymbol( 'Stored Time Buckets' ), parameters[ 'Stored Time Buckets' ] )
        shifts = acm.FDictionary()
        newParameters.AtPut( AsSymbol( 'Shifts' ), shifts )
        bpsShifts = string.split( parameters[ 'Benchmark Price Shift' ], ' ' )
        shiftsByTb = acm.FDictionary()
        shifts.AtPut( AsSymbol( 'Basis Points' ), shiftsByTb )
        for idx, tb in enumerate( parameters[ 'Time Buckets' ] ):
            shiftsByTb.AtPut( tb.AsSymbol(), bpsShifts[idx] )
        parameters.Clear()
        parameters.AddAll( newParameters )

class YieldCurveBucketShiftBenchmarkPriceDialog (BucketShiftBaseDialog):

    def ShiftLabels(self):
        return ["Basis Points"]
    
    def CriteriaClass( self ):
        return acm.FYieldCurve
        
    def CreateToolTip(self):
        BucketShiftBaseDialog.CreateToolTip( self )
        self.m_criteriaBtn.ToolTip( "Specify a filter if shifts should only be applied to a specific set of curves of type Benchmark or Spread." )
        self.m_criteriaText.ToolTip( "Specify a filter if shifts should only be applied to a specific set of curves of type Benchmark or Spread." )

    def CreateLayoutImpl(self, builder):
        pass
    
    def HandleCreate(self, dlg, layout):
        BucketShiftBaseDialog.HandleCreate( self, dlg, layout )
        self.m_fuxDlg.Caption( 'Steepener - Flattener Benchmark Price Shifts' )

def ael_custom_dialog_show( shell, params ):
    dialogData = FUxUtils.UnpackInitialData( params )
    customDlg = YieldCurveBucketShiftBenchmarkPriceDialog()
    TransformOldParameters( dialogData )
    customDlg.AddParameters( dialogData )
    return acm.UX().Dialogs().ShowCustomDialogModal( shell, customDlg.CreateLayout(), customDlg )

def ael_custom_dialog_main( parameters, dictExtra ):
    displayName = GetNiceName( 'Benchmark Price Bucket Shift', parameters )
    TransformOldParameters( parameters )
    timeBuckets = parameters[ AsSymbol( 'Time Buckets' ) ]
    dates = [ tb.BucketDate() for tb in timeBuckets ]
    shifts = parameters[ AsSymbol( 'Shifts' )][ AsSymbol( 'Basis Points' ) ]
    bpShifts = None
    if shifts:
        bpShifts = [ shifts[tb.AsSymbol()] for tb in timeBuckets ] 
    shiftVector = acm.CreateShiftVector( 'shiftBenchmarkPriceInPeriods', 'benchmark curve', GetCriteria( parameters ), acm.FYieldCurveFilter, GetCriteriaTopOnly( parameters ) )
    shiftVector.AddShiftItem( [dates, bpShifts], displayName )
    return shiftVector
