
import acm

class StorageNamePart(object):
    
    def __init__(self):
        self.m_nameCtrl = None
        self.m_storage = None
        self.m_isDirty = False
        
    def BuildLayout( self, builder ):
        builder.  AddInput('storageNameCtrl', "Name:")
    
    def OnNameChanged( self, ud, ad ):
        self.m_isDirty = True
        
    def HandleCreate(self, layout, shell):
        self.m_nameCtrl = layout.GetControl( 'storageNameCtrl' )
        self.m_nameCtrl.SetData( self.m_storage.Name() )
        self.m_nameCtrl.AddCallback( 'Changed', self.OnNameChanged, None )
        
    def SetContents( self, contents ):
        self.m_storage = contents

    def HandleApply( self ):
        self.m_storage.Name( self.m_nameCtrl.GetData() )
        self.m_isDirty = False
        
    def IsDirty( self ):
        return self.m_isDirty
