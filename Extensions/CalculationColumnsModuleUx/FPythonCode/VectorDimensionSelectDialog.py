
import acm
import FUxCore

class VectorDimensionSelectDialog( FUxCore.LayoutDialog ):

    def __init__(self, dimensions, params):
        self.m_dimensions = dimensions
        
    def OnDimensionChanged( self, ud, ad ):
        self.m_currentCoordinates = None
        logicalDimensionName = str( self.m_dimensionCtrl.GetData() )
        dimensions = self.m_dimensions[ logicalDimensionName ]
        self.m_dimensionDefCtrl.Populate( dimensions )
        
    def HandleCreate(self, dlg, layout):
        self.m_dimensionCtrl = layout.GetControl( 'dimension' )
        self.m_dimensionCtrl.Populate( [acm.FSymbol(key) for key in self.m_dimensions.Keys()] )
        self.m_dimensionCtrl.AddCallback( 'Changed', self.OnDimensionChanged, None )
        self.m_dimensionDefCtrl = layout.GetControl( 'dimensionDef' )

    def CreateLayout( self ):
        
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        builder.  AddComboBox( 'dimension', "Dimension" )
        builder.  AddComboBox( 'dimensionDef', "Dimension Definition" )
        builder.  BeginHorzBox()
        builder.    AddFill()
        builder.    AddButton( 'ok', "Ok" )
        builder.    AddButton( 'cancel', "Cancel" )
        builder.  EndBox()
        builder.EndBox()
        return builder
        
    def HandleApply( self ):
        params = acm.FDictionary()
        params["logicalDimensionName"] = self.m_dimensionCtrl.GetData()
        params["dimDefName"] = self.m_dimensionDefCtrl.GetData().Name()
        return params
