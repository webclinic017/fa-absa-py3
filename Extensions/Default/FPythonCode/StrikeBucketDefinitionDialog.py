
import acm
import FUxCore

import StrikeBucketDefinitionDialogUtils

STRIKE_BUCKET_ICON = 'BlueBall'
STRIKE_BUCKET_DEFINITION_ICON = 'BlueBall'
STRIKE_BUCKET_GENERATORS_GROUP = 'dynamic strike bucket definitions'

#------------------------------------------------------------------------------
def StartStrikeBucketDialog( shell, storedStrikeBuckets, isEdit):
    customDlg = StrikeBucketDefinitionDialog( storedStrikeBuckets, isEdit )
    customDlg.InitControls()
    builder = customDlg.CreateLayout()
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )

#------------------------------------------------------------------------------
# Callbacks
#------------------------------------------------------------------------------
def OnAddButtonPressed( self, cd ):
    selectedButton = self.m_radioButtonManager.Selected()

    if selectedButton == self.m_manualRadioButton:
        self.AddManualStrikeBucketDefinition()
        self.IncreaseStrikeValue()
    else:
        self.AddGenerationStrikeBucketDefinition()
    
    self.EnableAddButton()
    
    if self.m_strikeBucketList.Visible():
        self.PopulateStrikeBucketList()

#------------------------------------------------------------------------------
def OnRadioButton(self, cd) :
    selectedButton = self.m_radioButtonManager.Selected()
    
    if selectedButton == self.m_manualRadioButton:
        self.EnableGeneration( isManual=True )
    elif selectedButton == self.m_generateRadioButton:
        self.EnableGeneration( isManual=False )
        
    self.EnableAddButton()

#------------------------------------------------------------------------------
def OnViewButtonPressed( self, cd ):
    if self.m_strikeBucketList.Visible():
        self.m_strikeBucketList.Visible( False )
        self.m_viewButton.Label( 'Preview' )
    else:
        self.PopulateStrikeBucketList()
        self.m_strikeBucketList.Visible( True )
        self.m_viewButton.Label( 'Hide Preview' )

#------------------------------------------------------------------------------
def OnRemoveButtonPressed( self, cd ):
    self.RemoveStrikeBucketDefinition()
    
#------------------------------------------------------------------------------
def OnStrikeBucketGeneratorChanged( self, cd ):
    self.EnableAddButton()
    
#------------------------------------------------------------------------------
def OnHandleDefaultAction( self, cd ):
    self.RemoveStrikeBucketDefinition()
    
#------------------------------------------------------------------------------    
def OnStrikeBucketsNameChanged( self, cd ):
    name = self.m_storedStrikeBucketsName.GetData()
    
    if name:
        self.m_okButton.Enabled( True )
    else:
        self.m_okButton.Enabled( False )

#------------------------------------------------------------------------------
# StrikeBucketDefinitionDialog
#------------------------------------------------------------------------------
class StrikeBucketDefinitionDialog( FUxCore.LayoutDialog ):

    def __init__( self, storedStrikeBuckets, isEdit=True ):
        self.m_bindings = None
        self.m_radioButtonManager = acm.FUxRadioButtonManager()
        
        self.m_isEdit = isEdit
        self.m_storedStrikeBuckets = storedStrikeBuckets
    
        self.m_parameterGUIDefinitionByDisplayName = StrikeBucketDefinitionDialogUtils.GetFParameterGUIDefinitions( STRIKE_BUCKET_GENERATORS_GROUP )
    
    #------------------------------------------------------------------------------    
    def HandleApply( self ):
        strikeBucketsDefinition = self.CreateStrikeBucketsDefinition()
        strikeBucketsDefinition.Name( self.m_storedStrikeBucketsName.GetData() )
        
        self.m_storedStrikeBuckets.StrikeBucketsDefinition( strikeBucketsDefinition )

        if (not self.m_isEdit) and self.m_createShared.Checked():
            self.m_storedStrikeBuckets.AutoUser( False )
            self.m_storedStrikeBuckets.User( None )

        return self.m_storedStrikeBuckets
    
    #------------------------------------------------------------------------------    
    def InitControls( self ):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        
        self.m_strikeValueCtrl = self.m_bindings.AddBinder( 'strikeValueCtrl', acm.GetDomain('double'), None )
        self.m_stepCtrl = self.m_bindings.AddBinder( 'stepCtrl', acm.GetDomain('double'), None )
    
    #------------------------------------------------------------------------------    
    def ServerUpdate( self, sender, aspectSymbol, parameter ):
        self.EnableAddButton()
        
    #------------------------------------------------------------------------------    
    def EnableAddButton( self ):
        enableAddButton = False
        
        selectedButton = self.m_radioButtonManager.Selected()
        
        if selectedButton == self.m_manualRadioButton:
            validStrikeValue = self.m_strikeValueCtrl.Validate( False )
            validStepValue = self.m_stepCtrl.Validate( False )
            
            if validStrikeValue and validStepValue:
                strikeValue = self.m_strikeValueCtrl.GetValue()
                
                if strikeValue != None:
                    enableAddButton = self.IsUniqueManualDefinition()
            
        elif self.m_generator.GetData():
            enableAddButton = True
            
        self.m_addButton.Enabled( enableAddButton )
        
    #------------------------------------------------------------------------------
    def RemoveStrikeBucketDefinition( self ):
        self.m_strikeBucketDefinitionsList.RemoveAllSelectedItems( True )
        
        if self.m_strikeBucketList.Visible():
            self.PopulateStrikeBucketList()
            
    #------------------------------------------------------------------------------
    def IsUniqueManualDefinition( self ):
        strikeValue = self.m_strikeValueCtrl.GetValue()
        
        definitions, _ = self.GetStrikeBucketDefinitions()
        
        return not any(strikeValue == definition.StrikeMid() for definition in definitions)
        
    #------------------------------------------------------------------------------
    def IsUniqueGenerationInfo( self, newGenerationInfo ):        
        _, generationInfos = self.GetStrikeBucketDefinitions()
        
        if len( generationInfos ):
            return not any(newGenerationInfo == generationInfo for generationInfo in generationInfos)
        else:
            return True
            
    #------------------------------------------------------------------------------
    def PopulateStrikeBucketList( self ):
        strikeBuckets = self.CreateStrikeBuckets()
        
        self.m_strikeBucketList.RemoveAllItems()
        root = self.m_strikeBucketList.GetRootItem()
        
        for strikeBucket in strikeBuckets:
            node = root.AddChild()
            node.SetData( strikeBucket )
            node.Icon( STRIKE_BUCKET_ICON )
            node.Label( strikeBucket.Name(), 0 )
            node.Label( strikeBucket.StrikeStart(), 1 )
            node.Label( strikeBucket.StrikeMid(), 2 )
            node.Label( strikeBucket.StrikeEnd(), 3 )

    #------------------------------------------------------------------------------
    def PopulateStrikeBucketGenerators( self ):
        if len( self.m_parameterGUIDefinitionByDisplayName ):
            for definition in self.m_parameterGUIDefinitionByDisplayName.keys():
                self.m_generator.AddItem( definition )
            
            startValue = self.m_parameterGUIDefinitionByDisplayName.keys()[0]
            self.m_generator.SetData( startValue )
    
    #------------------------------------------------------------------------------
    def PopulateFromStoredStrikeBucket( self ):
        if self.m_isEdit:
            strikeBucketsDefinition = self.m_storedStrikeBuckets.StrikeBucketsDefinition()
            
            for strikeBucketDefinition in strikeBucketsDefinition.StrikeBucketDefinitions():
                self.AddStrikeBucketDefinition( strikeBucketDefinition )
                
            for generationInfo in strikeBucketsDefinition.StrikeBucketGenerationInfos():
                self.AddStrikeBucketDefinition( generationInfo )
    
    #------------------------------------------------------------------------------
    def CreateStrikeBucketsDefinition( self ):
        strikeType = self.m_strikeType.GetData()
        definitions, generationInfos = self.GetStrikeBucketDefinitions()
        
        return acm.Risk().CreateStrikeBucketsDefinition( strikeType, definitions, generationInfos)
    
    #------------------------------------------------------------------------------
    def CreateStrikeBuckets( self ):
        strikeBucketsDefinition = self.CreateStrikeBucketsDefinition()
        return acm.Risk().CreateStrikeBuckets( strikeBucketsDefinition )       
    
    #------------------------------------------------------------------------------
    def GetStrikeBucketDefinitions( self ):
        strikeBuckeDefListRoot = self.m_strikeBucketDefinitionsList.GetRootItem()
        
        definitions = []
        generationInfos = []
        
        for listItem in strikeBuckeDefListRoot.Children():
            definition = listItem.GetData()
            
            if definition.Class() == acm.FStrikeBucketDefinition:
                definitions.append( definition )
            else:
                generationInfos.append( definition )
        
        return definitions, generationInfos
    
    #------------------------------------------------------------------------------
    def AddManualStrikeBucketDefinition( self ):
        midStrike = self.m_strikeValueCtrl.GetValue()
        definition = acm.Risk.CreateStrikeBucketDefinition( midStrike )
        
        self.AddStrikeBucketDefinition( definition )
        
    #------------------------------------------------------------------------------
    def AddGenerationStrikeBucketDefinition( self ):
        parameterGUIDefinition = self.m_parameterGUIDefinitionByDisplayName[self.m_generator.GetData()]
        guiDefinitionWrapper = StrikeBucketDefinitionDialogUtils.FParameterGUIDefinitionWrapper( parameterGUIDefinition )
        
        try:
            guiDefinitionWrapper.RunGUI( self.m_fuxDlg.Shell(), acm.FDictionary() )
            generationInfo = guiDefinitionWrapper.StrikeBucketGenerationInfo()

            if self.IsUniqueGenerationInfo( generationInfo ):
                self.AddStrikeBucketDefinition( generationInfo )

        except Exception as e:
            pass

    #------------------------------------------------------------------------------
    def AddStrikeBucketDefinition( self, definition ):
        root = self.m_strikeBucketDefinitionsList.GetRootItem()

        node = root.AddChild()
        node.SetData( definition )
        node.Icon( STRIKE_BUCKET_DEFINITION_ICON )
        node.Label( definition.StringKey() )
    
    #------------------------------------------------------------------------------
    def IncreaseStrikeValue( self ):
        strikeValue = self.m_strikeValueCtrl.GetValue()
        stepValue = self.m_stepCtrl.GetValue()
        
        if (strikeValue != None) and (stepValue != None):
            self.m_strikeValueCtrl.SetValue( strikeValue + stepValue )
        
    #------------------------------------------------------------------------------
    # Create/Setup GUI
    #------------------------------------------------------------------------------
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        dlg.Caption( 'Create Strike Buckets' )
        
        self.m_okButton = layout.GetControl( 'ok' )
        self.m_okButton.Enabled( self.m_isEdit )
        
        self.m_createShared = layout.GetControl( 'createAsShared' )
        self.m_createShared.Checked( self.m_storedStrikeBuckets.User() is None )
        self.m_createShared.Enabled( not self.m_isEdit )
        
        self.CreateStoredStrikeBucketsName( layout )
        self.CreateStrikeBucketsGenerationSection( layout )
        self.CreateStikeBucketDefinitionsSection( layout )
        self.CreateGeneralSettingsSection( layout )
        self.CreateStrikeBucketsSection( layout )
        
        self.PopulateFromStoredStrikeBucket()
    
    #------------------------------------------------------------------------------
    def CreateStoredStrikeBucketsName( self, layout ):
        self.m_storedStrikeBucketsName = layout.GetControl( 'storedStrikeBucketsName' )
        self.m_storedStrikeBucketsName.AddCallback( 'Changed', OnStrikeBucketsNameChanged, self )
        
        if self.m_isEdit:
            self.m_storedStrikeBucketsName.SetData( self.m_storedStrikeBuckets.Name() )
            self.m_storedStrikeBucketsName.Enabled( False )        
        else:
            self.m_storedStrikeBucketsName.Enabled( True )
        
        self.m_storedStrikeBucketsName.ToolTip( 'Enter the name of the stored strike buckets' )
    
    #------------------------------------------------------------------------------
    def CreateStrikeBucketsGenerationSection( self, layout ):
        self.m_bindings.AddLayout( layout )
    
        self.SetupRadioButtons( layout )
    
        self.m_addButton = layout.GetControl( 'strikeBucketAdd' )
        self.m_addButton.AddCallback( 'Activate', OnAddButtonPressed, self )
        self.m_addButton.Enabled( False )
                
        self.m_generator = layout.GetControl( 'strikeBucketGenerator' )
        self.m_generator.AddCallback( "Changed", OnStrikeBucketGeneratorChanged, self )
        self.m_generator.Editable( False )
        
        self.PopulateStrikeBucketGenerators()

    #------------------------------------------------------------------------------
    def CreateStikeBucketDefinitionsSection( self, layout ):
        self.m_strikeBucketDefinitionsList = layout.GetControl( 'strikeBucketDefinitions' )
        self.m_strikeBucketDefinitionsList.ShowColumnHeaders()
        self.m_strikeBucketDefinitionsList.EnableHeaderSorting( True )
        self.m_strikeBucketDefinitionsList.AddColumn( 'Specification', 330 )
        self.m_strikeBucketDefinitionsList.AddCallback( 'DefaultAction', OnHandleDefaultAction, self )
        
        self.m_viewButton = layout.GetControl( 'viewStrikeBuckets' )
        self.m_viewButton.AddCallback( 'Activate', OnViewButtonPressed, self )
        
        self.m_removeButton = layout.GetControl( 'removeStrikeBucketDefinition' )
        self.m_removeButton.AddCallback( 'Activate', OnRemoveButtonPressed, self )
    
    #------------------------------------------------------------------------------
    def CreateGeneralSettingsSection( self, layout ):
        self.m_strikeType = layout.GetControl( 'strikeType' )
        
        self.m_strikeType.AddItem( 'Absolute' )
        self.m_strikeType.AddItem( 'None' )
        self.m_strikeType.SetData( 'None' )
        
        self.m_strikeType.Enabled( False )
        self.m_strikeType.ToolTip( 'Strike bucket values are interpreted as the strike type of the volatility structure' )
    
    #------------------------------------------------------------------------------
    def CreateStrikeBucketsSection( self, layout ):
        self.m_strikeBucketList = layout.GetControl( 'strikeBucketList' )
        self.m_strikeBucketList.Visible( False )
        
        self.m_strikeBucketList.ShowColumnHeaders()
        self.m_strikeBucketList.EnableHeaderSorting( True )
        self.m_strikeBucketList.AddColumn( 'Label', 75 )
        self.m_strikeBucketList.AddColumn( 'Start', 75 )
        self.m_strikeBucketList.AddColumn( 'Mid', 75 )
        self.m_strikeBucketList.AddColumn( 'End', 75 )
        
    #------------------------------------------------------------------------------    
    def SetupRadioButtons( self, layout ):
        self.m_manualRadioButton = layout.GetControl( 'manual' )
        self.m_generateRadioButton = layout.GetControl( 'generate' )
        
        self.m_radioButtonManager.Add( self.m_manualRadioButton )
        self.m_radioButtonManager.Add( self.m_generateRadioButton )
        self.m_radioButtonManager.Select( self.m_manualRadioButton, True ) 
        self.m_radioButtonManager.AddCallback('Activate', OnRadioButton, self)
            
    #------------------------------------------------------------------------------
    def EnableGeneration( self, isManual ):
        self.m_strikeValueCtrl.Editable( isManual )
        self.m_stepCtrl.Editable( isManual )
        
        self.m_generator.Editable( not isManual )

    #------------------------------------------------------------------------------
    def CreateLayout( self ):
        spaceSize = 7

        b = acm.FUxLayoutBuilder()
        
        b.BeginVertBox()
        b.  BeginHorzBox()
        b.    AddInput( 'storedStrikeBucketsName', 'Name', -1, 35 )
        b.  EndBox()
        b.  AddSpace( spaceSize )
        b.  BeginHorzBox()
        b.    BeginVertBox()
        b.      BeginVertBox( 'EtchedIn', 'Strike Buckets' ) 
        b.        AddRadioButton( 'manual', 'Manual' )
        b.        AddSpace( spaceSize )
        b.        BeginHorzBox()
        b.          AddSpace( spaceSize )
        b.          BeginVertBox()
        self.m_strikeValueCtrl.BuildLayoutPart( b, 'Value' )
        self.m_stepCtrl.BuildLayoutPart( b, 'Step' )
        b.          EndBox()
        b.        EndBox()
        b.        AddSpace( spaceSize )
        b.        AddRadioButton( 'generate', 'Generate' )
        b.        AddSpace( spaceSize )
        b.        BeginHorzBox()
        b.          AddSpace( spaceSize )
        b.          BeginVertBox()
        b.            AddOption( 'strikeBucketGenerator', '', 40 )
        b.          EndBox()
        b.        EndBox()
        b.        AddSpace( spaceSize )
        b.        BeginHorzBox()
        b.          AddFill()
        b.          AddButton( 'strikeBucketAdd', 'Add' )
        b.        EndBox()
        b.      EndBox()
        b.      BeginHorzBox( 'EtchedIn', 'General Settings' )
        b.        AddOption( 'strikeType', 'Strike Type' )
        b.      EndBox()
        b.    EndBox()
        b.    BeginVertBox()
        b.      BeginVertBox( 'EtchedIn', 'Bucket Definitions' )
        b.        AddList( 'strikeBucketDefinitions', 15, 15, 70 )
        b.        AddSpace( spaceSize )
        b.        BeginHorzBox()
        b.          AddButton( 'viewStrikeBuckets', 'Preview' )
        b.          AddFill()
        b.          AddButton( 'removeStrikeBucketDefinition', 'Remove' )
        b.        EndBox()
        b.      EndBox()
        b.      BeginVertBox( 'EtchedIn', 'Preview' )
        b.        AddList( 'strikeBucketList', 15, 15, 70 )
        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.  AddSpace( spaceSize )
        b.  BeginHorzBox()
        b.    AddFill()
        b.    AddCheckbox( 'createAsShared', 'Create as shared' )
        b.    AddButton( 'ok', 'OK' )
        b.    AddButton( 'cancel', 'Cancel' )
        b.  EndBox()
        b.EndBox()
        
        return b
