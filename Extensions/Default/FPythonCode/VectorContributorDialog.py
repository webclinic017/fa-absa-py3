
import acm
import FUxCore
import ContributorDialog
from ContributorDialog import ContributorDialog

_s_typeSym = acm.FSymbol("Type")
_s_vectorSym = acm.FSymbol("Vector")
_s_bucketSym = acm.FSymbol("Bucket")
_s_vectorTypesSym = acm.FSymbol("VectorTypes")
_s_vectorParamGUISym = acm.FSymbol( "VectorParameterGUIDefinition" )

class AddVectorContributorDialog( ContributorDialog ):

    def __init__(self, shell, dimensions, params):
        ContributorDialog.__init__(self, params)
        self.m_shell = shell
        self.m_dimensions = dimensions
        self.m_currentCoordinates = None

    def HandleParams( self, params ):
        self.m_dimensionCtrl.SetData( acm.FSymbol(params["logicalDimensionName"]) )
        if params["coordinatesParams"]:
            self.m_coordinatesTextCtrl.Visible( True )
            self.m_coordinatesBtnCtrl.Visible( True )
            self.m_coordinatesTextCtrl.SetData( params["coordinatesParams"] )
        ContributorDialog.HandleParams( self, params )

    def OnSetCoordinates( self, ud, ad ):
        dimension = self.m_dimensions[ str( self.m_dimensionCtrl.GetData() ) ]
        if dimension[ _s_typeSym ] == _s_bucketSym:
            self.m_currentCoordinates = acm.UX().Dialogs().SelectTimeBuckets( self.m_shell, self.m_currentCoordinates )
            self.m_coordinatesTextCtrl.SetData( self.m_currentCoordinates )
        elif dimension[ _s_typeSym ] == _s_vectorSym:
            if dimension[ _s_vectorTypesSym ]:
                self.m_currentCoordinates = acm.UX().Dialogs().CreateNamedParametersVector( self.m_shell, dimension[ _s_vectorTypesSym ], self.m_currentCoordinates )
            elif dimension[ _s_vectorParamGUISym ]:
                #TODO::JANKAR01
                pass
            else:
                assert(0)
        
    def OnDimensionChanged( self, ud, ad ):
        self.m_currentCoordinates = None
        dimension = self.m_dimensions[ str( self.m_dimensionCtrl.GetData() ) ]
        self.m_nameCtrl.SetData( self.m_dimensionCtrl.GetData() )
        self.m_coordinatesTextCtrl.Clear()
        if dimension[ _s_typeSym ]:
            self.m_coordinatesTextCtrl.Visible( True )
            self.m_coordinatesBtnCtrl.Visible( True )
        else:
            self.m_coordinatesTextCtrl.Visible( False )
            self.m_coordinatesBtnCtrl.Visible( False )
        
    def HandleCreate(self, dlg, layout):
        ContributorDialog.HandleCreate( self, dlg, layout )
        self.m_dimensionCtrl = layout.GetControl( 'dimension' )
        self.m_dimensionCtrl.Populate( [acm.FSymbol(key) for key in self.m_dimensions.Keys()] )
        self.m_dimensionCtrl.AddCallback( 'Changed', self.OnDimensionChanged, None )
        self.m_coordinatesTextCtrl = layout.GetControl( 'coordinatesText' )
        self.m_coordinatesTextCtrl.Enabled( False )
        self.m_coordinatesTextCtrl.Visible( False )
        self.m_coordinatesBtnCtrl = layout.GetControl( 'coordinatesBtn' )
        self.m_coordinatesBtnCtrl.AddCallback( 'Activate', self.OnSetCoordinates, None )
        self.m_coordinatesBtnCtrl.Visible( False )
        self.m_nameCtrl.Enabled( False )
        self.HandleParams( self.m_params )

    def CreateLayout_Override( self, builder ):
        builder.BeginVertBox( 'EtchedIn' )
        builder.AddComboBox( 'dimension', "Dimension" )
        builder.BeginHorzBox()
        builder.  AddInput( 'coordinatesText', "Coordinate" )
        builder.  AddButton( 'coordinatesBtn', "...", False, True )
        builder.EndBox()
        builder.EndBox()
        
    def HandleApply( self ):
        ContributorDialog.HandleApply(self)
        self.m_params["logicalDimensionName"] = self.m_dimensionCtrl.GetData()
        self.m_params["coordinatesParams"] = self.m_currentCoordinates
        return self.m_params
