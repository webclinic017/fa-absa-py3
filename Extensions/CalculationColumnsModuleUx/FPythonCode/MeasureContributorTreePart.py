
import acm
import FUxCore
import MeasureSpecificationGenerator
from MeasureSpecificationGenerator import Contributor

import DisplayCurrencyParameterization
import VectorContributorDialog

import CommandCallbacks

from CommandCallbacks import DimensionsFromColumnId
from CommandCallbacks import customContributorTemplates

class TypeInfo(object) :
    def __init__(self, typeName, callbackClass, editEnabled, addAsParentEnabled, parentTypeName) :
        self.m_typeName = typeName
        self.m_callbackClass = callbackClass
        self.m_editEnabled = editEnabled
        self.m_addAsParentEnabled = addAsParentEnabled
        self.m_parentTypeName = parentTypeName


    
class TreeNodeCommand( FUxCore.MenuItem ):
    def __init__(self, parent, invokeCB, userData = None, enabled = True):
        self.m_parent = parent
        self.m_invokeCB = invokeCB
        self.m_userData = userData
        self.m_enabled = enabled

    def Enabled( self ):
        return self.m_enabled
        
    def Invoke( self, cd ):
        self.m_invokeCB(self.m_userData, None)

class MenuCommandCallbackCreator( object ):
    def __init__(self, parent, enabledCB, createCB, addAsParent, userData):
        self.m_parent = parent
        self.m_userData = userData
        self.m_enabledCB = enabledCB
        self.m_createCB = createCB
        self.m_addAsParent = addAsParent
        
    def CreateCB(self):
        enabled = self.m_enabledCB( self.m_parent, self.m_userData )
        return TreeNodeCommand( self.m_parent, self.m_createCB, [self.m_addAsParent, self.m_userData], enabled )
   
class MeasureContributorTreePart( object ):
    
    def __init__(self):
        self.m_shell = None
        self.m_storage = None
        self.m_typeInfoByName = {}
        self.m_menuTypeInfo = []
        self.m_params = None
        self.m_changed = False
        
        self.m_filterCtrl = None
        self.m_treeCtrl = None
        self.m_rootNode = None
        self.m_addButton = None
        self.m_removeButton = None
        
        self.m_allDimensionsNamesAndDefinitions = None

        self.m_copiedTrees = None

        self.RegisterTypeInfos()
        self.InitializeDefaultDimensions()

    def UpdateControls(self) :
        item = self.m_treeCtrl.GetSelectedItem()

        self.m_removeButton.Enabled(item != self.GetRootItem())

    def GetTypeInfo(self, typeInfoName ):
        return self.m_typeInfoByName.get(typeInfoName, None)

    def GetTypeInfoFromTreeItem(self, treeItem) :
        contributor = treeItem.GetData()
        typeInfo = None
        if contributor :
            typeInfo = self.GetTypeInfo(contributor.m_type)

        return typeInfo

    def RegisterTypeInfo(self, typeName, callbackClass, editEnabled, addAsParentEnabled, parentTypeName, addToMenu) :
        infoType = TypeInfo(typeName, callbackClass, editEnabled, addAsParentEnabled, parentTypeName)
        self.m_typeInfoByName[typeName] = infoType

        if addToMenu :
            self.m_menuTypeInfo.append(infoType)

    def RegisterTypeInfos(self) :
        self.RegisterTypeInfo('Column', CommandCallbacks.Column, False, False, None, True)
        self.RegisterTypeInfo('Parameters', CommandCallbacks.Parameter, True, True, None, True)
        self.RegisterTypeInfo('Vector', CommandCallbacks.Vector, True, True, None, True)
        self.RegisterTypeInfo('Scenario', CommandCallbacks.Scenario, True, True, None, True)
        self.RegisterTypeInfo('FRTB SA', CommandCallbacks.Custom, True, False, 'Custom', True)
        self.RegisterTypeInfo('Display Currencies', CommandCallbacks.Custom, True, True, 'Custom', True)
        
    def InitializeDefaultDimensions( self ):
        self.m_allDimensionsNamesAndDefinitions = acm.FDictionary()
        colDefs = acm.ExtensionTools().GetDefaultContext().GetAllExtensions(
            acm.FColumnDefinition,
            acm.FTradingSheet,
            False,
            False,
            'sheet columns',
            'positionsheet',
            True
        )
        for colDef in colDefs:
            DimensionsFromColumnId( colDef.Name(), self.m_allDimensionsNamesAndDefinitions )
    
    def Icon( self, contributor ):
        def add( icon, addon ):
            if len(icon) > 0:
                return icon + '+' + addon
            return addon
        icon = ''
        if contributor.m_scenario:
            icon = add( icon, 'RiskMatrix')
        if contributor.m_parameters:
            icon = add( icon, 'ParamContext')
        if contributor.m_columnId:
            icon = add( icon, 'EmptySheet')
        if contributor.m_customContributor:
            icon = add( icon, 'ForceToState')
        if contributor.m_vectors:
            icon = add( icon, 'AgainOverlay')
        return icon
        
    def CreateShowOnlyThisCB( self ):
        return TreeNodeCommand( None, self.OnShowOnlyThis ) 
        
    def CreateShowAllCB( self ):
        return TreeNodeCommand( None, self.OnShowAll ) 

    def CreatePasteCB( self ):
        enabled = self.m_copiedTrees is not None
        if enabled:
            if self.SelectionDefinesColumns():
                columnIds = set()
                for treeData in self.m_copiedTrees:
                    self.TreeDataDo( treeData, lambda x: columnIds.add( x.DefinesColumns() ) )
                enabled = not (True in columnIds)
        return TreeNodeCommand( None, self.OnPaste, None, enabled ) 

    def CreateCopyCB( self ):
        return TreeNodeCommand( None, self.OnCopy ) 
    
    def CreateEditCB( self ):
        enabled = False
        if len(self.m_treeCtrl.GetSelectedItems()) == 1:
            typeInfo = self.GetTypeInfoFromTreeItem( self.m_treeCtrl.GetSelectedItem())
            enabled = typeInfo.m_editEnabled

        return TreeNodeCommand( None, self.OnEdit, None, enabled ) 

    def ShowOnlyThis( self, items ):
        visibleNodes = set()
        for item in items:
            self.PathDo( item, lambda x: visibleNodes.add( x ) )
        self.TreeDo( self.GetRootItem(), lambda x: x.Visible( x in visibleNodes ) )
        for item in items:
            self.TreeDo( item, lambda x: x.Visible( True ) )
        self.m_treeCtrl.ForceRedraw() 
        
    def OnShowOnlyThis( self, ud, cd ):
        self.ShowOnlyThis( self.m_treeCtrl.GetSelectedItems() )

    def ShowAll( self ):
        self.TreeDo( self.GetRootItem(), lambda x: x.Visible( True ) )
        self.m_treeCtrl.ForceRedraw()
        
    def OnShowAll( self, ud, cd ):
        self.ShowAll()
        
    def Commands( self ):
        isRoot = self.m_treeCtrl.GetSelectedItem() == self.GetRootItem()
        commands = []
        
        for typeInfo in self.m_menuTypeInfo:
            itemName = 'addChild' + typeInfo.m_typeName
            parent = 'View'
            if typeInfo.m_parentTypeName:
                path = 'Add Child/' + typeInfo.m_parentTypeName + '/' + typeInfo.m_typeName + '...'
            else:
                path = 'Add Child/' + typeInfo.m_typeName + '...'
            toolTip = ''
            accelerator = ''
            mnemonic = ''
            cbCreator = MenuCommandCallbackCreator( self, typeInfo.m_callbackClass.Enabled, self.OnAddContributor, False, typeInfo.m_typeName )
            cb = cbCreator.CreateCB
            commands.append( [itemName, parent, path, toolTip, accelerator, mnemonic, cb, False] )
            if not isRoot : 
                if typeInfo.m_addAsParentEnabled:
                    itemName = 'addParent' + typeInfo.m_typeName
                    parent = 'View'
                    if typeInfo.m_parentTypeName:
                        path = 'Add Parent/' + typeInfo.m_parentTypeName + '/' + typeInfo.m_typeName + '...'
                    else:
                        path = 'Add Parent/' + typeInfo.m_typeName + '...'
                    toolTip = ''
                    accelerator = ''
                    mnemonic = ''
                    cbCreator = MenuCommandCallbackCreator( self, typeInfo.m_callbackClass.Enabled, self.OnAddContributor, True, typeInfo.m_typeName )
                    cb = cbCreator.CreateCB
                    commands.append( [itemName, parent, path, toolTip, accelerator, mnemonic, cb, False] )
        
        if not isRoot : 
            commands.extend( [
                FUxCore.Separator(),
                ['showOnlyThis',    'View',  'Show Only This',      '', 'Ctrl+T',   'o',    self.CreateShowOnlyThisCB,  False ],
                ['showAll',         'View',  'Show All',            '', 'Ctrl+L',   'a',    self.CreateShowAllCB,       False ],
                FUxCore.Separator(),
                ['copySubTree',     'View',  'Copy',                '', 'Ctrl+C',   'y',    self.CreateCopyCB,          False ],
                ['pasteSubTree',    'View',  'Paste',               '', 'Ctrl+V',   'e',    self.CreatePasteCB,         False ],
                FUxCore.Separator(),
                ['editNodeData',    'View',  'Edit...',             '', 'Ctrl+E',   'd',    self.CreateEditCB,          False ]
            ] )
        
        return commands
        
    def OnTreeContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(self.Commands()))

    def GetParams( self ):
        if not self.m_params:
            measureGenerator = self.m_storage.CalculationColumnSpecificationCollection()
        
            if measureGenerator == None:
                self.m_params = acm.FDictionary()
                self.m_params['tree'] = acm.FDictionary()
            else:
                self.m_params = measureGenerator.Parameters()
        return self.m_params
        
    def GetSelectedItems(self):
        return self.m_treeCtrl.GetSelectedItems()

    def Generate(self, uniqueIds):
        root = self.GetRootItem()
        params = acm.FDictionary()
        params['tree'] = acm.FDictionary()
        self.Traverse( root, params['tree'] )
        return MeasureSpecificationGenerator.Generate( params, uniqueIds )
        
    def AddToTree( self, parents, contributor ):
        new = None
        if not parents:
            parents = [self.GetRootItem()]
        for parent in parents:
            new = parent.AddChild()
            new.SetData( contributor )
            new.Icon( self.Icon( contributor), self.Icon( contributor) )
            new.Label( contributor.m_displayName )
            parent.Expand()
        self.m_changed = True
        return new

    def AddToTreeAsParent( self, children, contributor ):
        byParent = {}
        for child in children:
            tmp = byParent.setdefault( child.Parent() or self.GetRootItem(), [] )
            tmp.append( child )
        newItems = []
        for parent in byParent:
            items = byParent[parent]
            newItem = parent.AddChild()
            newItem.SetData( contributor )
            newItem.Icon( self.Icon( contributor), self.Icon( contributor) )
            newItem.Label( contributor.m_displayName )
            for item in items:
                self.CopySubTreeTo( newItem, item )
                item.Remove()
            parent.Expand()
            newItems.append( newItem )
        self.m_treeCtrl.SetSelectedItems( newItems )
    
    def AddContributorToTree( self, items, contributor, addAsParent ):
        if addAsParent:
            self.AddToTreeAsParent( items, contributor )
        else:
            self.AddToTree( items, contributor )
            
    def OnRemoveBranch( self, ud):
        for item in self.m_treeCtrl.GetSelectedItems():
            item.Remove()
        self.m_changed = True
        self.m_treeCtrl.ForceRedraw()
        
    def GetRootItem(self) :
        if not self.m_rootNode :
            self.m_rootNode = self.m_treeCtrl.GetRootItem().AddChild()
            self.m_rootNode.Label('Contributors')
            self.m_rootNode.Icon('Folder', 'OpenFolder')

        
        return self.m_rootNode

    def GetRemoveMenu(self):
        menu = acm.FUxMenu()
        menu.AddItem( self.OnRemoveNode, None, 'Node', '', True )
        menu.AddItem( self.OnRemoveBranch, None, 'Branch', '', True )

        return menu

    def OnRemoveButton(self, ud, cd) :
        menu = self.GetRemoveMenu()
        menu.Track( self.m_removeButton )
        

    def OnRemoveNode( self, ud):
        items = self.m_treeCtrl.GetSelectedItems()
        for item in items:
            parent = item.Parent() or self.GetRootItem()
            for child in item.Children():
                self.CopySubTreeTo( parent, child )
                child.Remove()
            item.Remove()
        self.m_changed = True
        self.m_treeCtrl.ForceRedraw()
        
    def OnCopy( self, ud, cd ):
        items = self.m_treeCtrl.GetSelectedItems()
        self.m_copiedTrees = []
        for item in items:
            tree = acm.FDictionary()
            self.Traverse( item, tree )
            self.m_copiedTrees.append( tree )
        
    def OnPaste( self, ud, cd ):
        parents = self.m_treeCtrl.GetSelectedItems() or [self.GetRootItem()]
        for tree in self.m_copiedTrees:
            for parent in parents:
                self.PopulateTreeControl( parent, tree )
        self.m_copiedTrees = None
        
    def ValidDimensions( self, node ):    
        if self.SelectionDefinesColumns():
            def tmp( item, namesAndDimensions ):
                if item.GetData().m_columnId:
                    DimensionsFromColumnId( item.GetData().m_columnId, namesAndDimensions )
            
            namesAndDimensions = acm.FDictionary()
            self.PathDo( node, lambda x: tmp(x, namesAndDimensions ) )
            return namesAndDimensions
        return None
    
    def ValidDimensionForSelection( self ):
        parents = self.m_treeCtrl.GetSelectedItems()
        namesAndDimensions = None

        for parent in parents:
            nad = self.ValidDimensions( parent )
            if nad is not None:
                if not namesAndDimensions:
                    namesAndDimensions = acm.FDictionary()
                namesAndDimensions.JoinWithSymbolicKeys( nad )
        return namesAndDimensions if namesAndDimensions is not None else self.m_allDimensionsNamesAndDefinitions
        
    def ValidParameterNames( self, node ):
        def tmp( item, validNames ):
            if item.GetData().m_columnId:
                liveColDef = acm.Risk.CreateLiveColumnDefinition( item.GetData().m_columnId, acm.ExtensionTools().GetDefaultContext().Name() )
                if liveColDef.UnfixedParameters() is not None:
                    for param in liveColDef.UnfixedParameters():
                        validNames.add( str(param.Name()) )
            
        validNames = set()
        self.PathDo( node, lambda x: tmp(x, validNames ) )
        return len(validNames) > 0 and validNames or None
    
    def AddContributor( self, contributorType, addAsParent ):
        typeInfo = self.GetTypeInfo( contributorType )
        parents = self.m_treeCtrl.GetSelectedItems() or [self.GetRootItem()]
        source = typeInfo.m_callbackClass.ShowDialog( self, contributorType, None )
        for sourceItem in source:
            contributor = typeInfo.m_callbackClass.ContributorFromSource( sourceItem )
            self.AddContributorToTree( parents, contributor, addAsParent )

    def OnAddContributor( self, ud, cd ):
        self.AddContributor( ud[1], ud[0] )
        
    def EditContributor( self, treeNode, contributor ):
        typeInfo = self.GetTypeInfo( contributor.m_type )
        source =typeInfo.m_callbackClass.SourceFromContributor( contributor )
        editedSource = typeInfo.m_callbackClass.ShowDialog( self, contributor.m_type, source )
        if editedSource:
            for sourceItem in editedSource:
                contributor = typeInfo.m_callbackClass.ContributorFromSource( sourceItem )
                treeNode.SetData( contributor )
                treeNode.Label( contributor.m_displayName )
            self.m_changed = True

    def OnEdit( self, ud, cd ):
        item = self.m_treeCtrl.GetSelectedItem()
        self.EditContributor( item, item.GetData() )
        self.m_treeCtrl.ForceRedraw()
        
    def CopySubTreeTo( self, targetParent, subTree ):
        childTree = acm.FDictionary()
        self.Traverse( subTree, childTree )
        self.PopulateTreeControl( targetParent, childTree )
            
    def OnInPlaceEditingBegin( self, ud, cd ):
        info = cd.At('InPlaceEditingInfo')
        contributor = info.Item().GetData()

    def OnInPlaceEditingEnd( self, ud, cd ):
        info = cd.At('InPlaceEditingInfo')
        contributor = info.Item().GetData()
        contributor.m_displayName = info.GetValue()
    
    def SelectionDefinesColumns( self ):
        items = self.m_treeCtrl.GetSelectedItems()
        columnIds = set()
        for item in items:
            self.PathDo( item, lambda x: columnIds.add( x.GetData().DefinesColumns() ) )
        return True in columnIds
        
    def OnFilterChanged( self, ud, cd ):
        filterString = self.m_filterCtrl.GetData()

        if len(filterString) > 0:
            def Match( item, filterString, matchedItems ):
                if filterString.lower() in str(item.GetData().m_displayName).lower():
                    matchedItems.add( item )
            
            matched = set()
            
            self.TreeDo( self.GetRootItem(), lambda x: Match( x, filterString, matched ) )
            self.ShowOnlyThis( matched )
        else:
            self.ShowAll()
    
    def MenuCB( self, args ):
        self.AddContributor( args[1], args[0] )
        
    def GetAddMenu(self):
        menu = acm.FUxMenu()
        childSubMenu = menu.AddSubMenu( 'Add Child' )
        childCustomSubMenu = None

        for typeInfo in self.m_menuTypeInfo:
            if typeInfo.m_parentTypeName:
                if not childCustomSubMenu:
                    childCustomSubMenu = childSubMenu.AddSubMenu(  typeInfo.m_parentTypeName )
                childCustomSubMenu.AddItem( self.MenuCB, [False, typeInfo.m_typeName], typeInfo.m_typeName, '', typeInfo.m_callbackClass.Enabled( self, typeInfo.m_typeName ) )
            else:
                childSubMenu.AddItem( self.MenuCB, [False, typeInfo.m_typeName], typeInfo.m_typeName, '', typeInfo.m_callbackClass.Enabled( self, typeInfo.m_typeName ) )

        parentSubMenu = menu.AddSubMenu( 'Add Parent' )
        parentCustomSubMenu = None

        for typeInfo in self.m_menuTypeInfo:
            if typeInfo.m_addAsParentEnabled:
                if typeInfo.m_parentTypeName:
                    if not parentCustomSubMenu:
                        parentCustomSubMenu = parentSubMenu.AddSubMenu( typeInfo.m_parentTypeName )
                    parentCustomSubMenu.AddItem( self.MenuCB, [True, typeInfo.m_typeName], typeInfo.m_typeName, '', typeInfo.m_callbackClass.Enabled( self, typeInfo.m_typeName ) )
                else:
                    parentSubMenu.AddItem( self.MenuCB, [True, typeInfo.m_typeName], typeInfo.m_typeName, '', typeInfo.m_callbackClass.Enabled( self, typeInfo.m_typeName ) )

        return menu


    def OnAdd( self, ud, cd ):
        menu = self.GetAddMenu()
        menu.Track( self.m_addButton )


    def OnTreeSelectionCanged( self, ud, cd ):
        self.UpdateControls()

    def HandleCreate(self, layout, shell):
        self.m_shell = shell

        self.m_removeButton = layout.GetControl( 'removeButton' )
        self.m_removeButton.AddCallback( 'Activate', self.OnRemoveButton, None )
        self.m_filterCtrl = layout.GetControl( 'filter' )
        self.m_filterCtrl.AddCallback( 'UserTyped', self.OnFilterChanged, None )
        self.m_treeCtrl = layout.GetControl( 'contributorTree' )
        self.m_treeCtrl.EnableMultiSelect( True )
        self.m_treeCtrl.ShowHierarchyLines( False )
        self.m_treeCtrl.AddCallback( 'InPlaceEditingBegin', self.OnInPlaceEditingBegin, None )
        self.m_treeCtrl.AddCallback( 'InPlaceEditingEnd', self.OnInPlaceEditingEnd, None )
        self.m_treeCtrl.AddCallback( 'ContextMenu', self.OnTreeContextMenu, None )
        self.m_treeCtrl.AddCallback( 'SelectionChanged', self.OnTreeSelectionCanged, None )
        self.m_addButton = layout.GetControl( 'addButton' )
        self.m_addButton.AddCallback( 'Activate', self.OnAdd, None )
        
        self.HandleParams( self.GetParams() )
        self.UpdateControls()
    
    def PathDo( self, item, doBlock ):
        if item:
            if item != self.GetRootItem():
                doBlock( item )
            if item.Parent():
                self.PathDo( item.Parent(), doBlock )
   
    def TreeDataDo( self, nodeData, doBlock ):
        if nodeData['contributor']:
            contributor = Contributor( nodeData['contributor'] )
            doBlock( contributor )
        if nodeData['children']:
            for child in nodeData['children']:
                self.TreeDataDo( child, doBlock )
        
    def PopulateTreeControl( self, parent, nodeData ):
        new = None
        if nodeData['contributor']:
            contributor = Contributor( nodeData['contributor'] )
            new = self.AddToTree( [parent], contributor )
        if nodeData['children']:
            for child in nodeData['children']:
                self.PopulateTreeControl( new or parent, child )
    def ClearTree(self) :
        self.m_treeCtrl.RemoveAllItems()
        self.m_rootNode = None

    def HandleParams( self, params ):
        self.ClearTree()

        treeData = params and params['tree']
        if treeData:
            self.PopulateTreeControl( self.GetRootItem(), treeData )
            self.m_changed = False

    def TreeDo( self, item, doBlock ):
        if item:
            if item != self.GetRootItem():
                doBlock( item )
            for c in item.Children():
                self.TreeDo( c, doBlock )

    def Traverse( self, node, data ):
        if node.GetData():
            data['contributor'] = node.GetData().AsDictionary()
        if node.Children() and node.Children().Size() > 0:
            data['children'] = acm.FArray()
            for child in node.Children():
                childData = acm.FDictionary()
                self.Traverse( child, childData )
                data['children'].Add( childData )

    def CreateCurrentParams(self):
        params = acm.FDictionary()
        root = self.GetRootItem()
        params['tree'] = acm.FDictionary()
        params['idPrefix'] = self.m_storage.Name()
        self.Traverse( root, params['tree'] )
        
        return params

    def HandleApply( self ):
        params = self.CreateCurrentParams()

        self.m_storage.CalculationColumnSpecificationCollection( 
            acm.PositionStorage().CreateCalculationColumnSpecificationGenerator(
                'MeasureSpecificationGenerator',
                acm.ExtensionTools().GetDefaultContext().Name(),
                params
            )
        )
        self.m_changed = False

    def BuildLayout( self, builder ):
        builder.BeginVertBox()
        builder.  AddTree( 'contributorTree', 300, 300)
        builder.  BeginHorzBox()
        builder.    AddInput( 'filter', '' )
        builder.    AddButton( 'addButton', 'Add >' )
        builder.    AddButton( 'removeButton', 'Remove >' )
        builder.  EndBox()
        builder.EndBox()
        
    def SetContents( self, contents ):
        self.m_storage = contents
        
    def IsDirty( self ):
        return self.m_changed

def Create(shell):
    return MeasureGenerator(shell)
