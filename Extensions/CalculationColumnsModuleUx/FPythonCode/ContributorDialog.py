
import acm
import FUxCore

    
class ContributorDialog( FUxCore.LayoutDialog ):

    def __init__(self, params):
        self.m_params = params or acm.FDictionary()
        self.m_nameCtrl = None

    def HandleParams( self, params ):
        if params["name"]:
            self.m_nameCtrl.SetData( params["name"] )

    def HandleCreate(self, dlg, layout):
        self.m_nameCtrl = layout.GetControl( "name" )

    def CreateLayout_Override( self, builder ):
        pass
        
    def CreateLayout( self ):
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        self.CreateLayout_Override( builder )
        builder.  AddInput( 'name', "Name" )
        builder.  BeginHorzBox()
        builder.    AddFill()
        builder.    AddButton( 'ok', "Ok" )
        builder.    AddButton( 'cancel', "Cancel" )
        builder.  EndBox()
        builder.EndBox()
        return builder
        
    def HandleApply( self ):
        self.m_params["name"] = self.m_nameCtrl.GetData()
        return self.m_params
        
