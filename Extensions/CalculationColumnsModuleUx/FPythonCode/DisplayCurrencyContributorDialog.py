
import acm
import FUxCore
from ContributorDialog import ContributorDialog


    
class DisplayCurrencyContributorDialog( ContributorDialog ):

    def __init__(self, params):
        ContributorDialog.__init__(self, params)
        
        self.m_availableListCtrl = None
        self.m_selectedListCtrl = None
        
        self.m_addCtrl = None
        self.m_removeCtrl = None
        self.m_addAllCtrl = None
        self.m_removeAllCtrl = None

    def HandleParams( self, params ):
        ContributorDialog.HandleParams( self, params )
        if params["selectedCurrencies"]:
            for curr in params["selectedCurrencies"]:
                self.AddToList( self.m_selectedListCtrl, curr )

    def AddToList( self, listCtrl, object ):
        newItem = listCtrl.GetRootItem().AddChild()
        newItem.SetData( object )
        newItem.Label( object.StringKey() )

    def OnAdd( self, ud, cd ):
        for item in self.m_availableListCtrl.GetSelectedItems():
            self.AddToList( self.m_selectedListCtrl, item.GetData() )
            item.Remove()
            
    def OnRemove( self, ud, cd ):
        for item in self.m_selectedListCtrl.GetSelectedItems():
            self.AddToList( self.m_availableListCtrl, item.GetData() )
            item.Remove()
        self.m_availableListCtrl.SortColumn( 0, "Ascending" )
        
    def OnAddAll( self, ud, cd ):
        for item in self.m_availableListCtrl.GetRootItem().Children():
            self.AddToList( self.m_selectedListCtrl, item.GetData() )
            item.Remove()
        
    def OnRemoveAll( self, ud, cd ):
        for item in self.m_selectedListCtrl.GetRootItem().Children():
            self.AddToList( self.m_availableListCtrl, item.GetData() )
            item.Remove()
        self.m_availableListCtrl.SortColumn( 0, "Ascending" )
    
    def HandleCreate(self, dlg, layout):
        ContributorDialog.HandleCreate( self, dlg, layout )
        self.m_availableListCtrl = layout.GetControl( "available" )
        self.m_selectedListCtrl = layout.GetControl( "selected" )
        
        self.m_addCtrl = layout.GetControl( "addBtn" )
        self.m_removeCtrl = layout.GetControl( "removeBtn" )
        self.m_addAllCtrl = layout.GetControl( "addAllBtn" )
        self.m_removeAllCtrl = layout.GetControl( "removeAllBtn" )
        
        self.m_addCtrl.AddCallback( "Activate", self.OnAdd, None )
        self.m_removeCtrl.AddCallback( "Activate", self.OnRemove, None )
        self.m_addAllCtrl.AddCallback( "Activate", self.OnAddAll, None )
        self.m_removeAllCtrl.AddCallback( "Activate", self.OnRemoveAll, None )
        
        for curr in acm.FCurrency.Select(""):
            self.AddToList( self.m_availableListCtrl, curr )
            
        self.m_availableListCtrl.SortColumn( 0, "Ascending" )
        self.m_availableListCtrl.EnableMultiSelect(True)
        self.m_availableListCtrl.AddCallback( "DefaultAction", self.OnAdd, None )
        self.m_selectedListCtrl.AddCallback( "DefaultAction", self.OnRemove, None )
     
        self.HandleParams( self.m_params )

    def CreateLayout_Override( self, builder ):
        builder.  BeginHorzBox()
        builder.    BeginVertBox()
        builder.      AddLabel( "availableLbl", "Available:" )
        builder.      AddList( 'available', 10 )
        builder.    EndBox()
        builder.    BeginVertBox()
        builder.      AddFill()
        builder.      AddButton( 'addBtn', "Add" )
        builder.      AddButton( 'removeBtn', "Remove" )
        builder.      AddButton( 'addAllBtn', "Add All" )
        builder.      AddButton( 'removeAllBtn', "Remove All" )
        builder.      AddFill()
        builder.    EndBox()
        builder.    BeginVertBox()
        builder.      AddLabel( "selectedLbl", "Selected:" )
        builder.      AddList( 'selected', 10 )
        builder.    EndBox()
        builder.  EndBox()
        
    def HandleApply( self ):
        ContributorDialog.HandleApply(self)
        self.m_params["selectedCurrencies"] = acm.FArray()
        for currItem in self.m_selectedListCtrl.GetRootItem().Children():
            self.m_params["selectedCurrencies"].Add( currItem.GetData() )
        return self.m_params

def Create(params):
    return DisplayCurrencyContributorDialog( params )
