
import acm
import FUxUtils
import FUxCore

from BucketShiftBaseDialog import BucketShiftBaseDialog
from BucketShiftBaseDialog import AsSymbol

def AdjustVectorValues( vector, targetSize, defaultValue ):
    if len(vector) == 1:
        if float(vector[0]) == defaultValue:
            index = 1
            while index < targetSize:
                vector.Add( defaultValue )
                index = index + 1
    return vector

def CollectShiftValues( vectorShifts, vectorFactors, size, parameters ):
    listShifts = str(parameters['Absolute Shift']).split(' ')
    for shift in listShifts:
        vectorShifts.Add( float(shift) )
    listFactors = str(parameters['Relative Shift']).split(' ')
    for factor in listFactors:
        vectorFactors.Add( factor )
    vectorShifts = AdjustVectorValues( vectorShifts, size, 0.0 )
    vectorFactors = AdjustVectorValues( vectorFactors, size, 1.0 )
    
def TransformOldParameters( parameters ):
    if parameters.Size() == 0 or parameters.HasKey( AsSymbol( 'Shifts' ) ):
        pass
    else:
        newParameters = acm.FDictionary()
        newParameters.AtPut( AsSymbol( 'Time Buckets' ), parameters[ 'Time Buckets' ] )
        newParameters.AtPut( AsSymbol( 'DifferenceType'), 'RelativeAndAbsolute' )
        newParameters.AtPut( AsSymbol( 'Floor' ), parameters[ 'Floor' ] )
        shifts = acm.FDictionary()
        newParameters.AtPut( AsSymbol( 'Shifts' ), shifts )
        factors = acm.FArray()
        absShifts = acm.FArray()
        CollectShiftValues( absShifts, factors, parameters[ 'Time Buckets' ].Size(), parameters )
        shifts.AtPut( AsSymbol( 'Absolute (bps)'), acm.FDictionary() )
        shifts.AtPut( AsSymbol( 'Relative %'), acm.FDictionary() )
        for idx, tb in enumerate( newParameters.At( AsSymbol( 'Time Buckets' ) ) ):
            shifts.At( AsSymbol( 'Absolute (bps)' ) ).AtPut( tb.AsSymbol(), float(absShifts[idx]) )
            shifts.At( AsSymbol( 'Relative %' ) ).AtPut( tb.AsSymbol(), 100.0 * ( float(factors[idx]) - 1.0 ) )
        parameters.Clear()
        parameters.AddAll( newParameters )

def CreateShiftParameters( parameters ):
    absShifts = []
    factors = []
    dates = []
    diffType = parameters.At( AsSymbol( 'DifferenceType' ) )
    shifts = parameters.At( AsSymbol( 'Shifts' ) ) 
    for tb in parameters.At( AsSymbol( 'Time Buckets' ) ):
        if diffType in ['Absolute', 'RelativeAndAbsolute', 'Replace']:
            shift = shifts.At( AsSymbol( 'Absolute (bps)' ) ).At( tb.AsSymbol() )
            absShifts.append( 0.0001 * shift )
        if diffType in ['Relative', 'RelativeAndAbsolute']:
            factor = shifts.At( AsSymbol( 'Relative %' ) ).At( tb.AsSymbol() )
            factors.append( 1 + 0.01 * factor )
        if diffType in ['Replace']:
            factors.append( 0.0 )
        if diffType in ['Absolute']:
            factors.append( 1.0 )
        if diffType in ['Relative']:
            absShifts.append( 0.0 )
    dates = parameters.At( AsSymbol( 'Time Buckets' ) )
    return [dates, absShifts, factors]
    
class YieldCurveBucketBaseDialog (BucketShiftBaseDialog):

    def ShiftLabels(self):
        diffType = self.m_diffTypeCtrl.GetValue()
        if diffType == 'RelativeAndAbsolute':
            return ['Relative %', 'Absolute (bps)']
        elif diffType == 'Relative':
            return ['Relative %']
        elif diffType == 'Absolute':
            return ['Absolute (bps)']
        elif diffType == 'Replace':
            return ['Absolute (bps)']
        return None
        
    def __init__(self):
        self.m_bindings = None
        self.m_diffTypeCtrl = None
    
    def CreateToolTip(self):
        BucketShiftBaseDialog.CreateToolTip( self )
        self.m_diffTypeCtrl.ToolTip( "Specify if the shift type should be Absolute and/or Relative or Fixed values (Replace)." )
        
    def HandleCreate(self, dlg, layout):
        self.m_bindings.AddLayout(layout)
        BucketShiftBaseDialog.HandleCreate( self, dlg, layout )
        self.m_diffTypeCtrl.SetValue( self.GetParameter( 'DifferenceType' ) )

    def HandleApply( self ):
        params = BucketShiftBaseDialog.HandleApply( self )
        self.AddParameter( 'DifferenceType', self.m_diffTypeCtrl.GetValue() )
        return params

    def CreateLayoutImpl(self, builder):
        self.m_diffTypeCtrl.BuildLayoutPart( builder, 'Shift Type' )
        
    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        domain = acm.GetDomain('enum(RiskFactorDifferenceType)')
        self.m_diffTypeCtrl = self.m_bindings.AddBinder( 'DifferenceType', acm.GetDomain('enum(RiskFactorDifferenceType)'), None, domain.Enumerators()[1:] )

