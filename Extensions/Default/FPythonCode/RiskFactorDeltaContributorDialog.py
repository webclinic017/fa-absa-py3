
import acm
import FUxCore

from ContributorDialog import ContributorDialog

    
class RiskFactorDeltaContributorDialog( ContributorDialog ):

    def __init__(self, params):
        ContributorDialog.__init__( self, params )
        self.m_bindings = acm.FUxDataBindings()
        self.m_rfSetupCtrl = None
        self.m_shiftTypeCtrl = None
        self.m_shiftUnitCtrl = None
        formatterSixDecimals = acm.FNumFormatter('').Clone()
        formatterSixDecimals.NumDecimals(6)
        self.m_shiftSizeBinder = self.m_bindings.AddBinder( 'shiftSize', acm.GetDomain('double'), formatterSixDecimals )
        self.m_shiftScaleBinder = self.m_bindings.AddBinder( 'shiftScale', acm.GetDomain('double'), formatterSixDecimals )
        self.m_riskFactorTypeCtrl = None
        self.m_dimensionsListCtrl = None

    def HandleParams( self, params ):
        ContributorDialog.HandleParams( self, params )

    def OnRiskFactorSetupChanged( self, ud, cd ):
        setup = self.m_rfSetupCtrl.GetData()
        types = set()
        for coll in setup.RiskFactorCollections():
            types.add( coll.RiskFactorType() )
        self.m_riskFactorTypeCtrl.Populate( list(types) )
    
    def OnRiskFactorTypeChanged( self, ud, cd ):
        setup = self.m_rfSetupCtrl.GetData()
        type = self.m_riskFactorTypeCtrl.GetData()
        
        dimensions = set()
        if type and setup:
            propertySpecs = setup.RiskFactorPropertySpecifications()
            for propertySpec in propertySpecs:
                addInfoSpec = propertySpec.AdditionalInfoSpec()
                if addInfoSpec.ExtendedClass() == acm.FRiskFactorInstance:
                    dimensions.add( "i." + str(addInfoSpec.MethodName()) )
                else:
                    dimensions.add( "c." + str(addInfoSpec.MethodName()) )
            for collection in setup.RiskFactorCollections():
                if collection.RiskFactorType() == type:
                    for dim in collection.RiskFactorDimensions():
                        dimensions.add( str(dim.DisplayName()) )
        self.m_dimensionsListCtrl.Populate( list( dimensions ) )
    
    def HandleCreate(self, dlg, layout):
        ContributorDialog.HandleCreate( self, dlg, layout )
        self.m_rfSetupCtrl = layout.GetControl( 'rfSetup' )
        self.m_rfSetupCtrl.Populate( acm.FRiskFactorSetup.Select("") )
        self.m_rfSetupCtrl.AddCallback( 'Changed', self.OnRiskFactorSetupChanged, None )
        self.m_shiftTypeCtrl = layout.GetControl( 'shiftType' )
        self.m_shiftTypeCtrl.Populate( ["Absolute", "Relative"] )
        self.m_shiftUnitCtrl = layout.GetControl( 'shiftUnit' )
        self.m_shiftUnitCtrl.Populate(  acm.GetDomain('enum(RiskFactorValueUnit)').EnumeratorStringsSkipFirst() )
        self.m_shiftSizeBinder.InitLayout( layout )
        self.m_shiftScaleBinder.InitLayout( layout )
        self.m_riskFactorTypeCtrl = layout.GetControl( 'riskFactorType' )
        self.m_riskFactorTypeCtrl.AddCallback( 'Changed', self.OnRiskFactorTypeChanged, None )
        self.m_dimensionsListCtrl = layout.GetControl( 'dimensions' )
        self.m_dimensionsListCtrl.EnableMultiSelect( True )
        
        self.HandleParams( self.m_params )

    def CreateLayout_Override( self, builder ):
        builder.BeginVertBox('EtchedIn', 'Input' )
        builder.AddOption( 'shiftType', 'Shift Type' )
        builder.AddOption( 'shiftUnit', 'Shift Unit' )
        self.m_shiftSizeBinder.BuildLayoutPart( builder, 'Shift Size')
        self.m_shiftScaleBinder.BuildLayoutPart( builder, 'Shift Scale Factor' )
        builder.AddOption( 'rfSetup', "Risk Factor Setup" )
        builder.AddOption( 'riskFactorType', "Risk Factor Type" )
        builder.AddList( 'dimensions', 6, 10, 40, -1 )
        builder.EndBox()
        
    def HandleApply( self ):
        ContributorDialog.HandleApply( self )
        self.m_params["columnName"] = self.m_params["name"]
        
        self.m_params["shiftType"] = self.m_shiftTypeCtrl.GetData()
        self.m_params["shiftUnit"] = self.m_shiftUnitCtrl.GetData()
        self.m_params["shiftSize"] =  self.m_shiftSizeBinder.GetValue()
        self.m_params["scaleFactor"] =  self.m_shiftScaleBinder.GetValue()
        self.m_params["rfSetup"] = self.m_rfSetupCtrl.GetData()
        self.m_params["riskFactorType"] = self.m_riskFactorTypeCtrl.GetData()
        dimensions = acm.FArray()
        self.m_params["dimensions"] = dimensions
        for item in self.m_dimensionsListCtrl.GetSelectedItems():
            dimensions.Add( item.GetData() )
        
        return self.m_params

def Create(params):
    return RiskFactorDeltaContributorDialog( params )
