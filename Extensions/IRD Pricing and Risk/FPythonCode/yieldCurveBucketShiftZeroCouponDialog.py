
import acm
import FUxUtils
import FUxCore

from yieldCurveBucketShiftBaseDialog import YieldCurveBucketBaseDialog

class YieldCurveBucketShiftZeroCouponDialog (YieldCurveBucketBaseDialog):

    def __init__(self):
        YieldCurveBucketBaseDialog.__init__( self )
        self.m_shiftShapeCtrl = None
        self.m_shiftFloorCtrl = None

    def CreateToolTip(self):
        YieldCurveBucketBaseDialog.CreateToolTip( self )
        self.m_criteriaBtn.ToolTip( "Specify a filter if shifts should only be applied to a specific set of yield curves." )
        self.m_criteriaText.ToolTip( "Specify a filter if shifts should only be applied to a specific set of yield curves." )
        self.m_shiftShapeCtrl.ToolTip( "Specify the bucket shape of the shifts. If not selected ‘Rectangle’ is used per default regardless of valuation parameters setting ‘Yield Shift Shape’." )
        self.m_shiftFloorCtrl.ToolTip( "Total rate values, as expressed in each curves Calculation Format, will not be shifted below this bps floor value. Any calculation format rate used in valuation, already being below the floor, will in the shifted calculations be moved to the defined floor value (and be shifted above the floor if applicable)." )
        
    def CriteriaClass( self ):
        return acm.FYieldCurve

    def HandleApply( self ):
        params = YieldCurveBucketBaseDialog.HandleApply( self )
        self.AddParameter( 'ShiftShape', self.m_shiftShapeCtrl.GetValue() )
        self.AddParameter( 'Floor', self.m_shiftFloorCtrl.GetValue() )
        return params

    def HandleCreate(self, dlg, layout):
        YieldCurveBucketBaseDialog.HandleCreate( self, dlg, layout )
        self.m_shiftShapeCtrl.SetValue( self.GetParameter( 'ShiftShape' ) )
        self.m_shiftFloorCtrl.SetValue( self.GetParameter( 'Floor' ) )
        self.m_fuxDlg.Caption( 'Steepener - Flattener Zero Coupon Shifts' )

    def CreateLayoutImpl(self, builder):
        YieldCurveBucketBaseDialog.CreateLayoutImpl( self, builder )
        self.m_shiftShapeCtrl.BuildLayoutPart( builder, 'Shift Shape' )
        self.m_shiftFloorCtrl.BuildLayoutPart( builder, 'Floor (bps)' )

    def InitControls(self):
        YieldCurveBucketBaseDialog.InitControls( self )
        domain = acm.GetDomain('enum(IrShiftType)')
        self.m_shiftShapeCtrl = self.m_bindings.AddBinder( 'ShiftShape', domain, None, domain.Enumerators()[1:4] )
        self.m_shiftFloorCtrl = self.m_bindings.AddBinder( 'Floor', acm.GetDomain('double'), None) 
