


import numbers
import collections
import acm

#------------------------------------------------------------------------------
# CompositeSelectionCtrl
#------------------------------------------------------------------------------
class CompositeSelectionCtrl( object ):

    #------------------------------------------------------------------------------
    def __init__( self, selectionCtrls, startingSelection=None ):
        self.m_startingSelection = startingSelection if startingSelection else {}
        self.m_ctrlById = collections.OrderedDict()
        
        for ctrlId, selectionCtrl in selectionCtrls:
            self.m_ctrlById[ctrlId] = selectionCtrl
    
    #------------------------------------------------------------------------------
    def CreateLayout( self, builder ):
        idx = 0
    
        for label, ctrl in self.m_ctrlById.iteritems():
            ctrl.CreateLayout( builder, idx )
            idx += 1

    #------------------------------------------------------------------------------
    def HandleCreate( self, dlg, layout ):
        for label, ctrl in self.m_ctrlById.iteritems():
            ctrl.HandleCreate( dlg, layout )
            
            items = self.m_startingSelection.get( label, None )
            if items:
                ctrl.SetSelection( items )

    #------------------------------------------------------------------------------
    def GetSelection( self ):
        return {label : ctrl.GetSelection() for label, ctrl in self.m_ctrlById.iteritems()}
        
    #------------------------------------------------------------------------------
    def ClearSelection( self ):
        for label, ctrl in self.m_ctrlById.iteritems():
            ctrl.ClearSelection()
            
#------------------------------------------------------------------------------
# SelectionCtrl
#------------------------------------------------------------------------------
class SelectionCtrl( object ):

    #------------------------------------------------------------------------------
    def __init__( self, label, domain, enabled, mandatory, subset=None, validationCB=None, methodChain=None):
        self.m_label = label
        self.m_domain = domain.ElementDomain() if domain.IsArrayDomain() else domain
        self.m_subset = subset
        self.m_enabled = enabled
        self.m_mandatory = mandatory
        self.m_validationCB = validationCB
        self.m_methodChain = methodChain

        self.m_items = []
        
        self.m_ctrlIdx = None
        self.m_dlg = None
        self.m_inputCtrl = None
        self.m_btnCtrl = None
    
    #------------------------------------------------------------------------------
    def CreateLayout( self, builder, idx ):
        self.m_ctrlIdx = idx
        
        builder.BeginHorzBox()
        builder.  AddInput( 'input_' + str( self.m_ctrlIdx ), self.m_label, 35, -1, 40, "Default", False)
        builder.  AddButton( 'btn_' + str( self.m_ctrlIdx ), '...', False, True)
        builder.EndBox()

    #------------------------------------------------------------------------------
    def HandleCreate( self, dlg, layout ):
        self.m_dlg = dlg
        self.m_inputCtrl = layout.GetControl( 'input_' + str( self.m_ctrlIdx ) )
        self.m_btnCtrl = layout.GetControl( 'btn_' + str( self.m_ctrlIdx ) )
        
        self.m_inputCtrl.Editable( False )
        self.m_btnCtrl.Editable( self.m_enabled )
        
        self.m_btnCtrl.AddCallback( 'Activate', self.OnButtonClicked, None )

    #------------------------------------------------------------------------------
    def ClearSelection( self ):
        self.m_items = []
        self.m_inputCtrl.Clear()

    #------------------------------------------------------------------------------
    def SetSelection( self, items ):
        if items:
            self.m_items = items
            self.m_inputCtrl.SetData( ', '.join( [AsString( item ) for item in self.m_items]) )

    #------------------------------------------------------------------------------
    def GetSelection( self ):        
        if self.m_mandatory and 0 == len( self.m_items ):
            msg = "Mandatory field {} not set.".format( self.m_label )
            raise Exception( msg )
                
        return self.m_items
    
    #------------------------------------------------------------------------------
    def OnButtonClicked( self, ud, ad ):
        if self.m_subset:
            items = acm.UX().Dialogs().SelectSubset( self.m_dlg.Shell(), self.m_subset, 'Select Items', True )
        else:
            items = acm.UX().Dialogs().SelectObjectsInsertItems( self.m_dlg.Shell(), self.m_domain, True, self.m_validationCB )
            if self.m_methodChain and items:
                methodChainTransformItemList = []
                methodChain = acm.FMethodChain(self.m_methodChain) 
                for item in items:
                    i = methodChain.Call([item])
                    if i and not i in methodChainTransformItemList:
                        methodChainTransformItemList.append(i)
                
                items = methodChainTransformItemList
        
        self.SetSelection( items )

#------------------------------------------------------------------------------
class FixedSelectionCtrl( SelectionCtrl ):
    
    #------------------------------------------------------------------------------
    def __init__( self, label, domain, mandatory, subset ):
        SelectionCtrl.__init__(self, label, domain, False, mandatory, subset, None, None )
        
    #------------------------------------------------------------------------------
    def HandleCreate( self, dlg, layout ):
        SelectionCtrl.HandleCreate( self, dlg, layout )
        self.SetSelection( self.m_subset )

    #------------------------------------------------------------------------------
    def ClearSelection( self ):
        pass

#------------------------------------------------------------------------------
def AsString( item ):
    if hasattr( item, 'StringKey' ):
        item = item.StringKey()
    elif ( isinstance( item, numbers.Number) ): 
        item = str(item)
    
    return item
        
