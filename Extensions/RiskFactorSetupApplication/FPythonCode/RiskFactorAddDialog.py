

import acm
import FUxCore
import RiskFactorUtils
import RiskFactorAddUtils
import RiskFactorTimeBuckets

#------------------------------------------------------------------------------
def Show( shell, caption, riskFactorCollection, riskFactorGenerator, selectionPaneCtrl, updateInstanceListCallback, verifyUniquenessCallback ) :
    dlg = RiskFactorAddDialog( caption, riskFactorCollection, riskFactorGenerator, selectionPaneCtrl, updateInstanceListCallback, verifyUniquenessCallback )
    acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)

#------------------------------------------------------------------------------
# Callbacks
#------------------------------------------------------------------------------
def OnGenerateButtonPressed( self, cd ):
    params = acm.FArray()
    params.Add(self)

    self.m_generationInformation.SetData( 'Generating risk factors...' )        
    acm.AsynchronousCall( AddRiskFactorAsync, params )
    
#------------------------------------------------------------------------------
def AddRiskFactorAsync( self ):
    self.GenerateRiskFactors()
        
    self.UpdateFilterControls()
    self.UpdateDisplayedRiskFactors()
    self.UpdateAddButton()
    
    self.m_riskFactorListCtrl.SortColumn( 0, 'Ascending' )

#------------------------------------------------------------------------------
def OnClearButtonPressed( self, cd ):
    self.Clear()
    
    self.UpdateFilterControls()
    self.UpdateAddButton()

#------------------------------------------------------------------------------
def OnDisplayRiskFactorsChanged( self, cd ):
    if 0 != len( self.m_generatedRiskFactors ):
        self.UpdateFilterControls()
        self.UpdateDisplayedRiskFactors()
        self.UpdateAddButton()

#------------------------------------------------------------------------------
def OnHandleDefaultAction( self, cd ):
    selectedItem = self.m_riskFactorListCtrl.GetSelectedItem()
    riskFactor = selectedItem.GetData()
    
    if not self.IsRiskFactorAdded( riskFactor ):
        self.AddSelectedRiskFactors()

#------------------------------------------------------------------------------
def OnSelectionChanged( self, cd ):
    self.m_selectionChanged = True

#------------------------------------------------------------------------------
# Display Options
#------------------------------------------------------------------------------
class RiskFactorDisplay( object ):
    ALL = 'All Risk Factors'
    MISSING = 'Missing Risk Factors'
    
#------------------------------------------------------------------------------
# RiskFactorAddDialog
#------------------------------------------------------------------------------
class RiskFactorAddDialog( FUxCore.LayoutDialog ):
    
    #------------------------------------------------------------------------------
    def __init__( self, caption, riskFactorCollection, riskFactorGenerator, selectionPaneCtrl, updateInstanceListCallback, verifyUniquenessCallback ):
        self.m_fuxDlg = None
        self.m_caption = caption
        
        self.m_riskFactorCollection  = riskFactorCollection
        
        self.m_verifyUniquenessCallback = verifyUniquenessCallback
        self.m_updateInstanceListCallback = updateInstanceListCallback
        
        self.m_riskFactorGenerator = riskFactorGenerator
        self.m_generatedRiskFactors = []
        
        self.m_dimensionByColumnIndex = {}
        self.m_timeBucketMap = RiskFactorTimeBuckets.TimeBucketMap( riskFactorCollection )
        
        dimensions = self.m_riskFactorCollection.RiskFactorDimensions()
        
        self.m_sorterByDimension = RiskFactorUtils.CreateSortersForCollection( self.m_riskFactorCollection )
        self.m_filterControls = RiskFactorUtils.FilterControlCollection( dimensions, {}, self.m_sorterByDimension )
        self.m_filterValues = RiskFactorUtils.FilterValues()
        
        self.m_selectionPaneCtrl = selectionPaneCtrl
        
        self.m_selectionChanged = False

    #------------------------------------------------------------------------------
    def GenerateRiskFactors( self ):
        try:
            selection = self.m_selectionPaneCtrl.GetSelection()
            self.m_generatedRiskFactors = self.m_riskFactorGenerator.GenerateRiskFactors( selection )

        except Exception as e:
            acm.UX().Dialogs().MessageBoxInformation( self.m_fuxDlg.Shell(), str( e ) )

    #------------------------------------------------------------------------------
    def HandleApply( self ):
        self.AddSelectedRiskFactors()
    
    #------------------------------------------------------------------------------
    def Clear( self ):
        self.m_generatedRiskFactors = []
        self.m_riskFactorListCtrl.RemoveAllItems()
        self.m_generationInformation.Clear()
        self.m_selectionPaneCtrl.ClearSelection()
    
    #------------------------------------------------------------------------------
    def AddSelectedRiskFactors( self ):
        for item in self.m_riskFactorListCtrl.GetSelectedItems():
            self.CreateRiskFactor( item )

        self.m_updateInstanceListCallback()
        
        if self.ShowMissingRiskFactors():
            self.RemoveSelectedRiskFactors()
            
        self.UpdateAddButton()
    
    #------------------------------------------------------------------------------
    def RemoveSelectedRiskFactors( self ):
        self.m_riskFactorListCtrl.RemoveAllSelectedItems( True )
        self.UpdateRiskFactorInformation()
        
        if not self.m_riskFactorListCtrl.ItemCount():
            self.UpdateFilterControls()
            self.UpdateDisplayedRiskFactors()
    
    #------------------------------------------------------------------------------
    def CreateRiskFactor( self, item ):
        riskFactor = item.GetData()
        
        if not self.IsRiskFactorAdded( riskFactor ):
            RiskFactorAddUtils.AddRiskFactorToCollection( riskFactor, self.m_riskFactorCollection )        
    
    #------------------------------------------------------------------------------
    def SelectionIncludesOnlyMissingRiskFactors( self ):
        selection = self.m_riskFactorListCtrl.GetSelectedItems()
        
        if selection.IsEmpty():
            return False
            
        includesOnlyMissingRiskFactors = True
        
        for item in selection:
            riskFactor = item.GetData()
            if self.IsRiskFactorAdded( riskFactor ):
                includesOnlyMissingRiskFactors = False
                break
                
        return includesOnlyMissingRiskFactors
    
    #------------------------------------------------------------------------------
    def UpdateRiskFactorInformation( self ):
        riskFactorCount = self.m_riskFactorListCtrl.ItemCount()
        self.m_generationInformation.SetData( "Risk Factors: {}".format( riskFactorCount ) )
    
    #------------------------------------------------------------------------------
    def UpdateDisplayedRiskFactors( self ):
        self.PopulateRiskFactors()
        self.UpdateRiskFactorInformation()
    
    #------------------------------------------------------------------------------
    def UpdateFilterControls( self ):
        filterByDimension = { dim : set() for dim in self.m_riskFactorCollection.RiskFactorDimensions() }

        dimensionByUniqueId = { dim.UniqueId() : dim for dim in self.m_riskFactorCollection.RiskFactorDimensions() }

        for riskFactor in self.m_generatedRiskFactors:
            if not self.HideRiskFactor( riskFactor ):
                for uniqueId, coordinate in riskFactor.iteritems():
                    coordinate = RiskFactorTimeBuckets.GetCoordinateDisplayValue( self.m_timeBucketMap, uniqueId, coordinate )
                    
                    dimension = dimensionByUniqueId[uniqueId]
                    filterByDimension[dimension].add(coordinate)

        orderedFilterByDimension = {key : list(value) for key, value in filterByDimension.iteritems()}

        if self.m_filterControls.Populate(orderedFilterByDimension, {} ) :
            self.m_filterValues = self.m_filterControls.GetFilterValues()

    #------------------------------------------------------------------------------
    def UpdateAddButton( self ):
        onlyMissingRiskFactors = self.SelectionIncludesOnlyMissingRiskFactors()
        self.m_addButton.Enabled( onlyMissingRiskFactors )
            
    #------------------------------------------------------------------------------
    def PopulateRiskFactors( self ):
        self.m_riskFactorListCtrl.RemoveAllItems()
        
        root = self.m_riskFactorListCtrl.GetRootItem()

        for riskFactor in self.m_generatedRiskFactors:
            if self.IsRiskFactorVisible( riskFactor ):
                node = root.AddChild()
                node.SetData( riskFactor )
                
                self.SetRiskFactorColumnData( riskFactor, node )            

    #------------------------------------------------------------------------------
    def SetRiskFactorColumnData( self, riskFactor, node):
        for index, dim in self.m_dimensionByColumnIndex.iteritems():
            coordinate = RiskFactorTimeBuckets.GetCoordinateDisplayValue( self.m_timeBucketMap, dim.UniqueId(), riskFactor[dim.UniqueId()] )
            node.Label( coordinate, index )

    #------------------------------------------------------------------------------
    def OnFilterChanged( self, d, ud ):
        self.m_filterValues = self.m_filterControls.GetFilterValues()
        
        self.UpdateDisplayedRiskFactors()
        self.UpdateAddButton()

    #------------------------------------------------------------------------------
    def IsRiskFactorVisible( self, riskFactor ):
        if self.HideRiskFactor( riskFactor):
            return False

        isVisible = True

        for uniqueId, value in self.m_filterValues.m_filterByDimension.iteritems():
            if value:
                coordinate = RiskFactorTimeBuckets.GetCoordinateDisplayValue( self.m_timeBucketMap, uniqueId, riskFactor[uniqueId] )
            
                if coordinate != value :
                    isVisible = False
                    break

        return isVisible

    #------------------------------------------------------------------------------
    def HideRiskFactor( self, riskFactor ):
        return self.ShowMissingRiskFactors() and self.IsRiskFactorAdded( riskFactor )

    #------------------------------------------------------------------------------
    def ShowMissingRiskFactors( self ):
        return self.m_displayedRiskFactors.GetData() == RiskFactorDisplay.MISSING

    #------------------------------------------------------------------------------
    def IsRiskFactorAdded( self, riskFactor ):
        riskFactorKey = RiskFactorUtils.GetRiskFactorInstanceKeyFromDict( self.m_riskFactorCollection, riskFactor)
        return not self.m_verifyUniquenessCallback( riskFactorKey )
        
    #------------------------------------------------------------------------------
    def SetupDisplayOptions( self ):
        self.m_displayedRiskFactors.AddItem( RiskFactorDisplay.ALL )
        self.m_displayedRiskFactors.AddItem( RiskFactorDisplay.MISSING )
        
        self.m_displayedRiskFactors.SetData( RiskFactorDisplay.ALL )
            
    #------------------------------------------------------------------------------
    def SetupRiskFactorColumns( self ):
        for idx, dim in enumerate(self.m_riskFactorCollection.RiskFactorDimensions(), 0):
            self.m_dimensionByColumnIndex[idx] = dim
            self.m_riskFactorListCtrl.AddColumn( dim.DisplayName(), 150 )

    #------------------------------------------------------------------------------
    def OnHeaderSortCB(self, params, ud) :
        item1 = params.At( 'item1' )
        item2 = params.At( 'item2' )
        column = params.At( 'column' )

        riskFactor1 = item1.GetData()
        riskFactor2 = item2.GetData()
        
        dim = self.m_dimensionByColumnIndex[column]
        uniqueId = dim.UniqueId()
        
        sortFunc = self.m_sorterByDimension.get( uniqueId, None )
        
        coordinate1 = RiskFactorTimeBuckets.GetCoordinateDisplayValue( self.m_timeBucketMap, uniqueId, riskFactor1[dim.UniqueId()] )
        coordinate2 = RiskFactorTimeBuckets.GetCoordinateDisplayValue( self.m_timeBucketMap, uniqueId, riskFactor2[dim.UniqueId()] )

        if sortFunc:
            coordinate1 = sortFunc( coordinate1 )
            coordinate2 = sortFunc( coordinate2 )

        ret = 0

        if coordinate1 < coordinate2 :
            ret = -1
        elif coordinate1 > coordinate2 :
            ret = 1

        return ret
        
    #------------------------------------------------------------------------------
    def OnTimer( self, ud ):
        if self.m_selectionChanged:
            self.UpdateAddButton()
            
        self.m_selectionChanged = False
        
    #------------------------------------------------------------------------------
    def HandleCreate( self, dlg, layout ):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption( self.m_caption )
        self.m_fuxDlg.RegisterTimer( self.OnTimer, 200)
        
        self.m_riskFactorCollectionInput = layout.GetControl( 'riskFactorCollectionInput' )
        self.m_riskFactorCollectionInput.Editable( False )
        self.m_riskFactorCollectionInput.SetData( self.m_riskFactorCollection.DisplayName() )

        self.m_selectionPaneCtrl.HandleCreate( dlg, layout )
        
        self.m_addButton = layout.GetControl( 'ok' )
        self.m_addButton.Enabled( False )
        
        self.m_generateButton = layout.GetControl( 'generate' )
        self.m_generateButton.AddCallback( 'Activate', OnGenerateButtonPressed, self )
        
        self.m_clearButton = layout.GetControl( 'clear' )
        self.m_clearButton.AddCallback( 'Activate', OnClearButtonPressed, self )
        
        self.m_filterControls.HandleCreate( layout )
        self.m_filterControls.AddFilterCallback( self.OnFilterChanged )
        
        self.m_generationInformation = layout.GetControl( 'generationInformation' )
        self.m_generationInformation.Editable( False )
        
        self.m_displayedRiskFactors = layout.GetControl( 'displayedRiskFactors' )
        self.m_displayedRiskFactors.AddCallback( 'Changed', OnDisplayRiskFactorsChanged, self )
        self.SetupDisplayOptions()
        
        self.m_riskFactorListCtrl = layout.GetControl( 'riskFactorList' )
        self.m_riskFactorListCtrl.ShowColumnHeaders()
        self.m_riskFactorListCtrl.EnableMultiSelect( True )
        self.m_riskFactorListCtrl.EnableHeaderSorting( True )
        self.m_riskFactorListCtrl.AddCallback( 'DefaultAction', OnHandleDefaultAction, self )
        self.m_riskFactorListCtrl.AddCallback( 'SelectionChanged', OnSelectionChanged, self )
        self.m_riskFactorListCtrl.SetSortCallback(self.OnHeaderSortCB, self)
        
        self.SetupRiskFactorColumns()
        
    #------------------------------------------------------------------------------
    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginVertBox( 'EtchedIn', 'Selection' )
        b.      BeginVertBox('None')
        b.        AddInput( 'riskFactorCollectionInput', 'Risk Factor Collection', 30, -1, 25 )
        self.m_selectionPaneCtrl.CreateLayout( b )
        b.      EndBox()
        b.      AddSpace( 5 )
        b.      BeginHorzBox()
        b.        AddFill()
        b.        AddButton( 'generate', 'Generate' )
        b.        AddButton( 'clear', 'Clear' )
        b.      EndBox()
        b.  EndBox()
        b.  BeginVertBox( 'EtchedIn', 'Risk Factors' )
        b.    BeginVertBox('None')
        self.m_filterControls.BuildLayout( b )
        b.      AddList( 'riskFactorList', 12 )
        b.    AddInput( 'generationInformation', '', 75 )
        b.    EndBox()
        b.    AddSpace( 5 )
        b.    BeginHorzBox()
        b.      AddLabel('displayLabel', 'Display:')
        b.      AddOption('displayedRiskFactors', '', 20, 20)
        b.      AddFill()
        b.      AddButton( 'ok', 'Add' )
        b.      AddButton( 'cancel', 'Close' )
        b.    EndBox()
        b.  EndBox()
        b.EndBox()

        return b
