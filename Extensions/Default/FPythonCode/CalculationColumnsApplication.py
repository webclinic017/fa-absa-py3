from __future__ import print_function

import acm
import FUxCore

import MeasureContributorTreePart
import SimplifiedMeasureContributorList
import StorageNamePart
import MeasureSpecificationGenerator



class CalculationColumnsApplication(FUxCore.HostedObjectLayoutApplication):
    def __init__(self):
        FUxCore.HostedObjectLayoutApplication.__init__(self)
        
        self.m_generatorPart = MeasureContributorTreePart.MeasureContributorTreePart()
        self.m_storageNamePart = StorageNamePart.StorageNamePart()
        self.m_simplifiedGeneratorPart = SimplifiedMeasureContributorList.SimplifiedMeasureContributorList()
        self.m_listCtrl  = None
        self.m_storage = None
        self.m_previewButton = None
        self.m_showPreviewListLinks = []

    def GetContextHelpID(self):
        return 1153
        
    def ScenariosString( self, scenarios ):
        return ", ".join( [scenario.Name() for scenario in scenarios] )
        
    def VectorsString( self, vectorConfig ):
        if vectorConfig:
            return ", ".join( [str(dimensionId) for dimensionId in vectorConfig.DimensionIds()] )
        return ""
        
    def GetColumnParameter( self, configuration, parameterKey ):
        if configuration and configuration.ParamDict():
            params = configuration.ParamDict()[acm.FSymbol("columnParameters")]
            if params:
                return params[parameterKey]
        return ""
        
    def Generate(self):
        uniqueIds = acm.FSet()
        params = None    
        simplifiedVisible = self.IsPaneVisible('simplifiedPane')
        if simplifiedVisible :
            params = self.m_simplifiedGeneratorPart.CreateCurrentParams()
        else:
            params = self.m_generatorPart.CreateCurrentParams()


        specs = MeasureSpecificationGenerator.Generate( params, uniqueIds )

        self.m_listCtrl.RemoveAllItems()
        root = self.m_listCtrl.GetRootItem()

        maxIdx = 0
        for key in self.m_paramNameToColIdx:
            if self.m_paramNameToColIdx[ key ] > maxIdx:
                maxIdx = self.m_paramNameToColIdx[ key ]
                
        while maxIdx > 3:
            self.m_listCtrl.RemoveColumn( maxIdx )
            maxIdx -= 1
        self.m_paramNameToColIdx = {}
        
        idx = 4
        for spec in specs:
            config = spec.ConfigurationExceptScenarios()
            if config and config.ParamDict():
                params = config.ParamDict()[acm.FSymbol("columnParameters")]
                if params:
                    for key in params.Keys():
                        if not key in self.m_paramNameToColIdx:
                            name = key
                            paramDef = acm.GetDefaultContext().GetExtension(acm.FColumnParameterDefinition, acm.FObject, key).Value()
                            if paramDef :
                                try :
                                    if not paramDef.IsValid():
                                        paramDef.Validate()

                                    name = str(paramDef.DisplayName())
                                except:
                                    name = key

                            self.m_listCtrl.AddColumn(name)

                            self.m_paramNameToColIdx[key] = idx
                            idx += 1
            
        for spec in specs:
            child = root.AddChild()
            try:
                child.SetData( spec )
                child.Label( spec )
                child.Label( spec.ColumnId(), 1 )
                child.Label( self.ScenariosString( spec.Scenarios() ), 2 )
                child.Label( self.VectorsString( spec.VectorConfiguration() ), 3 )
                
                liveColDef = acm.Risk.CreateLiveColumnDefinition( spec.ColumnId(), acm.ExtensionTools().GetDefaultContext().Name() )
                validParameterNames = set()
                if liveColDef.Parameters():
                    for param in liveColDef.Parameters():
                        validParameterNames.add( param.Name() )

                for parameterKey in self.m_paramNameToColIdx.keys():
                    param = self.GetColumnParameter( spec.ConfigurationExceptScenarios(), parameterKey )
                    child.Label( param, self.m_paramNameToColIdx[ parameterKey ] )
                    if not parameterKey in validParameterNames:
                        child.Style( self.m_paramNameToColIdx[ parameterKey ], False, acm.UX().Colors().Create(150, 150, 150).ColorRef(), acm.UX().Colors().Create(255, 255, 255).ColorRef() )
            except Exception as e:
                print(e)
        for idx in range(self.m_listCtrl.ColumnCount()):
            self.m_listCtrl.AdjustColumnWidthToFitItems( idx )
        
    def OnPreview( self, ud, ad ):
        self.Generate()

    def UpdatePreviewLists(self) :
        isVisible = self.IsPaneVisible('listPane')

        for showPreviewListLink in self.m_showPreviewListLinks :
            if isVisible:
                showPreviewListLink.SetData('Hide preview list')
            else :
                showPreviewListLink.SetData('Show preview list')
    

    def OnShowPreview( self, ud, ad ):
        show = not self.IsPaneVisible('listPane')
        if show:
            self.Generate()

        self.ShowPane('listPane', show)
        self.UpdatePreviewLists()

    def OnToggleSimplifiedAdvanced( self, ud, ad ):
        self.ToggleSimplifiedAdvanced()

    def ToggleSimplifiedAdvanced(self) :
        simplifiedVisible = self.IsPaneVisible('simplifiedPane')
        if simplifiedVisible :
            self.ShowPane('treePane', True)
            self.ShowPane('simplifiedPane', False)

            params = self.m_simplifiedGeneratorPart.CreateCurrentParams()
            self.m_generatorPart.HandleParams(params)

        else:
            self.ShowPane('treePane', False)
            self.ShowPane('simplifiedPane', True)

            params = self.m_generatorPart.CreateCurrentParams()
            self.m_simplifiedGeneratorPart.HandleParams(params)

        self.UpdatePreviewLists()

            
    def BuildSimplifiedPart(self, creationInfo) :
        builder = acm.FUxLayoutBuilder()

        builder.BeginVertBox()
        self.m_storageNamePart.BuildLayout( builder)
        builder.AddSpace(5)
        builder.    AddHyperLink('toggleSimplifiedAdvanced')
        self.m_simplifiedGeneratorPart.BuildLayout(builder)
        builder.        AddHyperLink('showPreviewListLink')
        builder.EndBox()

        layout = creationInfo.AddPane(builder, 'simplifiedPane')

        self.m_simplifiedGeneratorPart.HandleCreate( layout, self.Shell() )
        self.m_storageNamePart.HandleCreate( layout, self.Shell() )
        
        toggleSimplifiedAdvanced = layout.GetControl('toggleSimplifiedAdvanced')
        toggleSimplifiedAdvanced.SetData('Advanced')
        toggleSimplifiedAdvanced.AddCallback('Activate', self.OnToggleSimplifiedAdvanced, None)

        toggleSimplifiedAdvanced.Visible(False)

        showPreviewListLink = layout.GetControl('showPreviewListLink')
        showPreviewListLink.SetData('Show preview list')
        showPreviewListLink.AddCallback('Activate', self.OnShowPreview, None)

        self.m_showPreviewListLinks.append(showPreviewListLink)
        

    def BuildAdvancedPart(self, creationInfo):
        treeBuilder = acm.FUxLayoutBuilder()

        treeBuilder.BeginVertBox()
        self.m_storageNamePart.BuildLayout( treeBuilder )
        treeBuilder.AddSpace(5)
        treeBuilder.    AddHyperLink('toggleSimplifiedAdvanced')
        self.m_generatorPart.BuildLayout( treeBuilder )
        treeBuilder.        AddHyperLink('showPreviewListLink')
        treeBuilder.EndBox()

        treePaneLayout = creationInfo.AddPane(treeBuilder, 'treePane')

        self.m_storageNamePart.HandleCreate( treePaneLayout, self.Shell() )
        self.m_generatorPart.HandleCreate( treePaneLayout, self.Shell() )

        toggleSimplifiedAdvanced = treePaneLayout.GetControl('toggleSimplifiedAdvanced')
        toggleSimplifiedAdvanced.SetData('Simplified')
        toggleSimplifiedAdvanced.AddCallback('Activate', self.OnToggleSimplifiedAdvanced, None)

        showPreviewListLink = treePaneLayout.GetControl('showPreviewListLink')
        showPreviewListLink.SetData('Show preview list')
        showPreviewListLink.AddCallback('Activate', self.OnShowPreview, None)

        self.m_showPreviewListLinks.append(showPreviewListLink)

        self.ShowPane('treePane', False)

    def BuildPreviewPart(self, creationInfo) :
        builder = acm.FUxLayoutBuilder()

        builder.BeginVertBox()
        builder.    BeginVertBox('None', 'Measures' )
        builder.        AddList('paneList', 8, -1, 70)
        builder.        BeginHorzBox()
        builder.            AddFill()
        builder.            AddButton('preview', 'Update')
        builder.        EndBox()
        builder.    EndBox()
        builder.EndBox()

        listPaneLayout = creationInfo.AddPane(builder, 'listPane')
        self.m_previewButton = listPaneLayout.GetControl( 'preview' )
        self.m_previewButton.AddCallback( 'Activate', self.OnPreview, None )
   
        self.m_listCtrl = listPaneLayout.GetControl( 'paneList' )
        self.m_listCtrl.ShowColumnHeaders()
        self.m_listCtrl.EnableHeaderSorting( True )
        self.m_listCtrl.ShowGridLines()
        self.m_listCtrl.AddColumn("Name")
        self.m_listCtrl.AddColumn("Column")
        self.m_listCtrl.AddColumn("Scenario")
        self.m_listCtrl.AddColumn("Dimensions")
        
        self.m_paramNameToColIdx = {}

        self.ShowPane('listPane', False)

    def HandleCreate( self, creationInfo ):
        self.BuildAdvancedPart(creationInfo)
        self.BuildSimplifiedPart(creationInfo)
        self.BuildPreviewPart(creationInfo)

    def HandleObject(self, contents):
        self.m_storage = contents
        self.m_storageNamePart.SetContents( self.m_storage )        
        self.m_generatorPart.SetContents( self.m_storage )
        self.m_simplifiedGeneratorPart.SetContents(self.m_storage)
    
    def HandleApplyChanges(self):
        self.m_storageNamePart.HandleApply()

        simplifiedVisible = self.IsPaneVisible('simplifiedPane')
        if simplifiedVisible :
            self.m_simplifiedGeneratorPart.HandleApply()
        else:
            self.m_generatorPart.HandleApply()

        self.m_storage.User( None )
        self.m_storage.AutoUser( False )

        return True

    def HandleHasChanged(self):
        hasChanged = False

        hasChanged = hasChanged or (self.m_storage.Original() and self.m_storage.Original().Oid() < 0)
        hasChanged = hasChanged or self.m_storageNamePart.IsDirty()
        hasChanged = hasChanged or self.m_simplifiedGeneratorPart.IsDirty()

        return hasChanged
    
        
def CreateApplicationInstance():
    return CalculationColumnsApplication()
