from __future__ import print_function

import acm
import FUxCore
import FUxUtils

import MeasureSpecificationGenerator
from MeasureSpecificationGenerator import Contributor

import DisplayCurrencyParameterization
import VectorContributorDialog

import CommandCallbacks

from CommandCallbacks import DimensionsFromColumnId
from CommandCallbacks import customContributorTemplates

class ColumnIndex :
    Name = 0
    Column = 1
    Scenario = 2
    Vector = 3
    Parameter = 4

class PropertiesType :
    Scenarios = 'Scenarios'
    Dimensions = 'Dimensions'
    Parameters = 'Parameters'
    Contributor = 'Contributor'

class MenuType :
    NoMenu = 0
    ColumnName = 1
    Column = 2
    Parameter = 3
    CustomParameter = 4
    CustomColumn = 5

class PropertiesData :
    def __init__(self, type, data) :
        self.m_type = type
        self.m_data = data

    def Type(self) :
        return self.m_type

    def Data(self) :
        return self.m_data

def DisplayNameFromContributor(contributor) :
    displayName = str(contributor.m_displayName)

    if contributor.m_parameters :
        displayName = ''
        first = True
        
        for key in contributor.m_parameters.Keys() :
            paramDef = acm.GetDefaultContext().GetExtension(acm.FColumnParameterDefinition, acm.FObject, key).Value()



            if not first :
                displayName += ', '
                
            value = contributor.m_parameters[key]

            if hasattr(value, 'Name') :
                value = str(value.Name())
            elif hasattr(value, 'StringKey'):
                value = str(value.StringKey())
            else :
                value = str(value)
   
            try :
                if not paramDef.IsValid() :
                    paramDef.Validate()
                
                name = str(paramDef.DisplayName()) if paramDef and paramDef.IsValid() else str(key)
            except:
                name = str(key)

            displayName += name + ':' + value
            first = False

    return displayName

class ColumnParameters :
    def __init__(self) :
        self.m_column = None
        self.m_parameters = [] 
        self.m_scenarios = []
        self.m_vectors = []
        self.m_customs = []

    def ColumnName(self):
        return self.m_column.m_columnName if self.m_column.m_columnName else self.ColumnAsString()

    def ColumnAsString(self) :
        columnAsString = ''

        if self.m_column: 
            columnAsString = str(self.m_column.m_displayName)

        if self.m_customs :
            if columnAsString :
                columnAsString += ' '

            columnAsString += self.ContributorAsString(self.m_customs)            

        return columnAsString

    def ColumnId(self) :
        columnId = None
        if self.m_column :
            columnId = self.m_column.m_columnId

        return columnId

    def RemoveContributorIfPossible(self, contributor, contributors) :
        if contributor in contributors :
            contributors.remove(contributor)

    def RemoveContributor(self, contributor) :
        self.RemoveContributorIfPossible(contributor, self.m_parameters)
        self.RemoveContributorIfPossible(contributor, self.m_scenarios)
        self.RemoveContributorIfPossible(contributor, self.m_vectors)
        self.RemoveContributorIfPossible(contributor, self.m_customs)


    def ReplaceContributorIfPossible(self, oldContributor, newContributor, contributors) :
        if oldContributor in contributors :
            index = contributors.index(oldContributor)
            contributors[index] = newContributor

    def ReplaceContributor(self, oldContributor, newContributor) :
        self.ReplaceContributorIfPossible(oldContributor, newContributor, self.m_parameters)
        self.ReplaceContributorIfPossible(oldContributor, newContributor, self.m_scenarios)
        self.ReplaceContributorIfPossible(oldContributor, newContributor, self.m_vectors)
        self.ReplaceContributorIfPossible(oldContributor, newContributor, self.m_customs)

    def SetColumn(self, contributor) :
        self.m_column = contributor

    def SetColumnName(self, columnName):
        self.m_column.m_columnName = str(columnName)

    def FindContributor(self, originalContributor, contributors, attribute) :
        foundContributor = None

        if hasattr(originalContributor, attribute):
            value = getattr(originalContributor, attribute)


            for contributor in contributors :
                if getattr(contributor, attribute) == value :
                    foundContributor = contributor  
                    break

        return foundContributor

    def FindAnyContributor(self, contributor) :
        foundContributor = None

        foundContributor = foundContributor or self.FindContributor(contributor, self.m_parameters, 'm_parameters')
        foundContributor = foundContributor or self.FindContributor(contributor, self.m_scenarios, 'm_scenario')
        foundContributor = foundContributor or self.FindContributor(contributor, self.m_vectors, 'm_displayName')

        return foundContributor

    def AddContributor(self, contributor, contributors, attribute) :
        if self.FindContributor(contributor, contributors, attribute) == None:
            contributors.append(contributor)

    def FindParameterContributor(self, contributors, paramName) :
        paramContributor = None
        for contributor in contributors :
            if contributor.m_parameters : 
                if paramName in contributor.m_parameters.Keys() :
                    paramContributor = contributor
                    break

        if not paramContributor :
            paramContributor = Contributor( acm.FDictionary() )

        return paramContributor

    def AddParameter(self, contributor) :
        for key in contributor.m_parameters.Keys() :
            parameters = acm.FDictionary()
            parameters.AtPut(key, contributor.m_parameters[key])
            paramContributor = self.FindParameterContributor(self.m_parameters, key)
            paramContributor.m_parameters = parameters
            paramContributor.m_displayName = DisplayNameFromContributor(paramContributor)
            paramContributor.m_type = "Parameters"

            self.AddContributor(paramContributor, self.m_parameters, 'm_parameters')

    def ContributorAsString(self, contributors) :
        return ', '.join(DisplayNameFromContributor(contributor) for contributor in contributors)

    def ParametersAsString(self) :
        return self.ContributorAsString(self.m_parameters)

    def AddScenario(self, contributor) :
        self.AddContributor(contributor, self.m_scenarios, 'm_scenario')

    def ScenariosAsString(self) :
        return self.ContributorAsString(self.m_scenarios)

    def AddVector(self, contributor) :
        self.AddContributor(contributor, self.m_vectors, 'm_displayName')

    def VectorsAsString(self) :
        return self.ContributorAsString(self.m_vectors)

    def AddCustom(self, contributor) :
        self.m_customs.append(contributor)

    def AddContributorToParams(self, contributor):
        params = acm.FDictionary()
        params['contributor'] = contributor.AsDictionary()
        
        return params

    def AddContributorsToParams(self, params, contributors):
        for contributor in contributors :
            childParams = self.AddContributorToParams(contributor)
            children = acm.FArray()
            children.Add(childParams)

            params['children'] = children
            params = childParams

        return params

    def ToParams(self) :
        params = None
        if self.m_column :
            params = self.AddContributorToParams(self.m_column)

            childParams = self.AddContributorsToParams(params, self.m_parameters)
            childParams = self.AddContributorsToParams(childParams, self.m_scenarios)
            childParams = self.AddContributorsToParams(childParams, self.m_vectors)
            childParams = self.AddContributorsToParams(childParams, self.m_customs)

        return params

    def FillColumnsIds(self, columnIds, contributors) :
        for contributor in contributors :
            columnIds.add(contributor.DefinesColumns())

    def DefinesColumns(self) :
        columnIds = set()
        if self.m_column :
            columnIds.add(self.m_column.DefinesColumns())

        self.FillColumnsIds(columnIds, self.m_parameters)
        self.FillColumnsIds(columnIds, self.m_scenarios)
        self.FillColumnsIds(columnIds, self.m_vectors)
        self.FillColumnsIds(columnIds, self.m_customs)

        return columnIds

    def CopyTo(self, columnParameters):
        columnParameters.m_column = self.m_column
        columnParameters.m_parameters = list(self.m_parameters)
        columnParameters.m_scenarios = list(self.m_scenarios)
        columnParameters.m_vectors = list(self.m_vectors)
        columnParameters.m_customs = list(self.m_customs)
        

    def Copy(self) :
        columnParameters = ColumnParameters()
        self.CopyTo(columnParameters)
        return columnParameters

class IntersectionColumnParameters(ColumnParameters) :
    def __init__(self):
        ColumnParameters.__init__(self)
        self.m_columnParameters = []
        self.m_contributors = {}

    def Intersect(self, contributors1, contributors2, attribute) :
        intersectedContributors = []
        for contributor in contributors1 :
            if self.FindContributor(contributor, contributors2, attribute) :
                intersectedContributors.append(contributor)

        return intersectedContributors

    def AddColumnParameter(self, columnParameters) :
        if self.m_columnParameters :
            self.m_parameters = self.Intersect(self.m_parameters, columnParameters.m_parameters, 'm_parameters')
            self.m_scenarios = self.Intersect(self.m_scenarios, columnParameters.m_scenarios, 'm_scenario')
            self.m_vectors = self.Intersect(self.m_vectors, columnParameters.m_vectors, 'm_displayName')
            #self.m_customs = self.Intersect(self.m_customs, columnParameters.m_customs, 'm_displayName')
        else :
            columnParameters.CopyTo(self)

        self.m_columnParameters.append(columnParameters)
        
    def ReplaceContributor(self, oldContributor, newContributor) :
        for columnParameters in self.m_columnParameters :
            contributor = columnParameters.FindAnyContributor(oldContributor)
            if contributor :
                columnParameters.ReplaceContributor(contributor, newContributor)

    def RemoveContributor(self, contributor) :
        for columnParameters in self.m_columnParameters :
            originalContributor = columnParameters.FindAnyContributor(contributor)
            if originalContributor :
                columnParameters.RemoveContributor(originalContributor)

class TypeInfo(object) :
    def __init__(self, typeName, displayName, callbackClass, editEnabled, shouldHaveSelection) :
        self.m_typeName = typeName
        self.m_displayName = displayName
        self.m_callbackClass = callbackClass
        self.m_editEnabled = editEnabled
        self.m_shouldHaveSelection = shouldHaveSelection

    
class TreeNodeCommand( FUxCore.MenuItem ):
    def __init__(self, parent, invokeCB, userData = None, enabled = True):
        self.m_parent = parent
        self.m_invokeCB = invokeCB
        self.m_userData = userData
        self.m_enabled = enabled

    def Enabled( self ):
        return self.m_enabled
        
    def Invoke( self, cd ):
        self.m_invokeCB(self.m_userData)

class MenuCommandCallbackCreator( object ):
    def __init__(self, parent, enabledCB, createCB, userData, shouldHaveSelection):
        self.m_parent = parent
        self.m_userData = userData
        self.m_enabledCB = enabledCB
        self.m_createCB = createCB
        self.m_shouldHaveSelection = shouldHaveSelection
        
    def CreateCB(self):
        enabled = True
        if self.m_shouldHaveSelection :
            enabled = self.m_parent.HasSelectedItems()

        enabled = enabled and self.m_enabledCB( self.m_parent, self.m_userData )
        return TreeNodeCommand( self.m_parent, self.m_createCB, self.m_userData, enabled )
   
class SimplifiedMeasureContributorList( object ):
    
    def __init__(self):
        self.m_shell = None
        self.m_storage = None
        self.m_typeInfoByName = {}
        self.m_menuTypeInfo = {}
        
        self.m_menuTypeInfo[MenuType.Column] = []
        self.m_menuTypeInfo[MenuType.CustomColumn] = []
        self.m_menuTypeInfo[MenuType.Parameter] = []
        self.m_menuTypeInfo[MenuType.CustomParameter] = []

        self.m_params = None
        self.m_changed = False
        
        self.m_contributorListCtrl = None
        self.m_addColumnButton = None
        self.m_renameButton = None
        self.m_parameterizeButton = None
        self.m_removeButton = None
        
        self.m_allDimensionsNamesAndDefinitions = None

        self.m_copiedTrees = None
        self.m_propertiesTree = None
        self.m_currentColumnParameter = None

        self.RegisterTypeInfos()
        self.InitializeDefaultDimensions()

    def GetRootItem(self) :
        return self.m_contributorListCtrl.GetRootItem()

    def UpdateControls(self) :
        intersectionColumnParameters = None

        items = self.m_contributorListCtrl.GetSelectedItems()
        if items :
            intersectionColumnParameters = IntersectionColumnParameters()
            for item in items :
                intersectionColumnParameters.AddColumnParameter(item.GetData())

        item = self.m_contributorListCtrl.GetSelectedItem()
        items = self.m_contributorListCtrl.GetSelectedItems()

        self.m_removeButton.Enabled(item != None)
        self.m_renameButton.Enabled(item != None and len(items) == 1)
        self.m_parameterizeButton.Enabled(item != None)

        self.UpdatePropertiesTree(intersectionColumnParameters)


    def GetTypeInfo(self, typeInfoName ):
        return self.m_typeInfoByName.get(typeInfoName, None)

    def GetTypeInfoFromTreeItem(self, treeItem) :
        contributor = treeItem.GetData()
        typeInfo = None
        if contributor :
            typeInfo = self.GetTypeInfo(contributor.m_type)

        return typeInfo

    def HasSelectedItem(self):
        return len(self.GetSelectedItems()) == 1 


    def HasSelectedItems(self):
        ret = False
        if self.GetSelectedItems() :
            ret = True

        return ret

    def GetSelectedItems(self):
        return self.m_contributorListCtrl.GetSelectedItems()

    def RegisterTypeInfo(self, typeName, displayName, callbackClass, editEnabled, shouldHaveSelection, menuType) :
        infoType = TypeInfo(typeName, displayName, callbackClass, editEnabled, shouldHaveSelection)
        self.m_typeInfoByName[typeName] = infoType

        if menuType != MenuType.NoMenu :
            self.m_menuTypeInfo[menuType].append(infoType)

    def RegisterTypeInfos(self) :
        self.RegisterTypeInfo('Column', 'Columns', CommandCallbacks.Column, False, False, MenuType.Column)
        self.RegisterTypeInfo('Scenario', 'Scenarios', CommandCallbacks.Scenario, True, True, MenuType.Parameter)
        self.RegisterTypeInfo('Vector', 'Dimensions', CommandCallbacks.Vector, True, True, MenuType.Parameter)
        self.RegisterTypeInfo('Parameters', 'Parameters', CommandCallbacks.Parameter, True, True, MenuType.Parameter)
        self.RegisterTypeInfo('FRTB SA', 'FRTB SA', CommandCallbacks.Custom, True, False, MenuType.CustomColumn)
        #self.RegisterTypeInfo('Risk Factor Delta', 'Risk Factor Delta', CommandCallbacks.Custom, True, False, MenuType.CustomColumn)
        #self.RegisterTypeInfo('Display Currencies', 'Display Currencies', CommandCallbacks.Custom, True, True, MenuType.CustomParameter)
        
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
            icon = add( icon, 'Columns')
        if contributor.m_customContributor:
            icon = add( icon, 'ForceToState')
        if contributor.m_vectors:
            icon = add( icon, 'AgainOverlay')
        return icon
        
    def PropertiesTypeIsSelected(self, propertiesType) :
        item = self.m_propertiesTree.GetSelectedItem()
        propertiesData = item.GetData()

        return propertiesData.Type() == propertiesType

    def CanAddProperties(self) :
        canAdd = not self.PropertiesTypeIsSelected(PropertiesType.Contributor)

        if canAdd :
            item = self.m_propertiesTree.GetSelectedItem()
            propertiesData = item.GetData()
            contributorType = self.ContributorTypeFromPropertiesType(propertiesData.Type())
            typeInfo = self.GetTypeInfo(contributorType)
            if typeInfo :
                canAdd = typeInfo.m_callbackClass.Enabled(self, None)

        return canAdd
    
    def CreateAddCB( self ):
        return TreeNodeCommand( None, self.OnAdd, self.m_currentColumnParameter, self.CanAddProperties() ) 

    def CreateEditCB( self ):
        return TreeNodeCommand( None, self.OnEdit, self.m_currentColumnParameter, self.PropertiesTypeIsSelected(PropertiesType.Contributor) ) 

    def CreateRemoveCB( self ):
        return TreeNodeCommand( None, self.OnRemove, self.m_currentColumnParameter, self.PropertiesTypeIsSelected(PropertiesType.Contributor) ) 

    def CreateCopyToCB( self ):
        return TreeNodeCommand( None, self.OnCopyToColumns, self.m_currentColumnParameter, self.HasSelectedItems()) 

    def CreateAddColumnCB( self ):
        return TreeNodeCommand( None, self.OnAddColumn, None, True) 

    def CreateRemoveColumnsCB( self ):
        return TreeNodeCommand( None, self.OnRemoveColumns, None, self.HasSelectedItems()) 

    def CreateRenameColumnsCB( self ):
        return TreeNodeCommand( None, self.OnRenameColumns, None, self.HasSelectedItem()) 

    def AddCommand(self, commands, itemName, path, cb) :
        command =  [itemName, 'View', path, '', '', '', cb, False]
        commands.append(command)

    def AddCommandFromTypeInfo(self, typeInfo, itemPreFix, parentPath, commands, menuCB = None) :
        if not menuCB:
            menuCB = self.OnAddContributor

        itemName = itemPreFix + typeInfo.m_typeName
        path = parentPath + typeInfo.m_displayName + '...'
        cbCreator = MenuCommandCallbackCreator( self, typeInfo.m_callbackClass.Enabled, menuCB, typeInfo.m_typeName, typeInfo.m_shouldHaveSelection )
        self.AddCommand(commands, itemName, path, cbCreator.CreateCB)    

    def Commands( self ):
        commands = []
        
        for typeInfo in self.m_menuTypeInfo[MenuType.Column]:
            self.AddCommandFromTypeInfo(typeInfo, 'addColumn', 'Add Columns/', commands, self.AddColumnMenuCB)
        
        if self.m_menuTypeInfo[MenuType.CustomColumn] :
            self.AddCommand(commands, 'FUxMenuItemSeparator', 'Add Columns/',  None)
            for typeInfo in self.m_menuTypeInfo[MenuType.CustomColumn]:
                self.AddCommandFromTypeInfo(typeInfo, 'addColumn', 'Add Columns/', commands)

        self.AddCommand(commands, 'FUxMenuItemSeparator', 'Add Columns/',  None)
        self.AddCommand(commands, 'copyParameterToCopyColumns', 'Add Columns/With properties from selected...', self.CreateCopyToCB)
        commands.append(FUxCore.Separator())
        

        for typeInfo in self.m_menuTypeInfo[MenuType.Parameter]:
            self.AddCommandFromTypeInfo(typeInfo, 'parameterize', 'Parameterize/', commands)

        self.AddCommand(commands, 'FUxMenuItemSeparator', 'Parameterize/',  None)

        for typeInfo in self.m_menuTypeInfo[MenuType.CustomParameter]:
            self.AddCommandFromTypeInfo(typeInfo, 'parameterize', 'Parameterize/', commands)

        commands.append(FUxCore.Separator())
        self.AddCommand(commands, 'renameColumns',  'Rename...', self.CreateRenameColumnsCB)
        commands.append(FUxCore.Separator())
        self.AddCommand(commands, 'removeColumns',  'Remove', self.CreateRemoveColumnsCB)
        
        return commands
        
    def PropertiesCommands(self) :
        commands = []

        self.AddCommand(commands, 'addNodeData',  'Add...', self.CreateAddCB)
        commands.append(FUxCore.Separator())
        self.AddCommand(commands, 'editNodeData',  'Edit...', self.CreateEditCB)
        commands.append(FUxCore.Separator())
        self.AddCommand(commands, 'removeNodeData',  'Remove', self.CreateRemoveCB)
        
        return commands

    def OnTreeContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(self.Commands()))

    def OnPropertiesContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(self.PropertiesCommands()))

    def GetParams( self ):
        if not self.m_params:
            measureGenerator = self.m_storage.CalculationColumnSpecificationCollection()
        
            if measureGenerator == None:
                self.m_params = acm.FDictionary()
                self.m_params['tree'] = acm.FDictionary()
            else:
                self.m_params = measureGenerator.Parameters()

        return self.m_params
        
    def RemoveColumns(self) :
        for item in self.m_contributorListCtrl.GetSelectedItems():
            item.Remove()

        self.m_changed = True
        self.m_contributorListCtrl.ForceRedraw()

    def OnRemoveColumns(self, ud) :
        self.RemoveColumns()	

    def OnRenameColumns(self, ud) :
        self.RenameColumn()    

    def OnRemoveButton(self, ud, cd) :
        self.RemoveColumns()
        
    def ValidDimensions( self, item ):    
        namesAndDimensions = None
        if self.ItemDefinesColumn( item ):
            columnParameters = item.GetData()
            columnId = columnParameters.ColumnId()
            
            if columnId:
                namesAndDimensions = acm.FDictionary()
                DimensionsFromColumnId( columnId, namesAndDimensions )
            
        return namesAndDimensions
    
    def ValidDimensionForSelection( self ):
        items = self.m_contributorListCtrl.GetSelectedItems()
        intersectedNamesAndDimensions = acm.FDictionary()

        for item in items:
            validDimension = self.ValidDimensions(item)
            if validDimension:
                if intersectedNamesAndDimensions :
                    toRemove = []
                    for key in intersectedNamesAndDimensions.Keys() :
                        if not key in validDimension.Keys() :
                            toRemove.append(key)

                    for key in toRemove :
                        intersectedNamesAndDimensions.RemoveKey(key)
                else:
                    intersectedNamesAndDimensions = validDimension
            else:
                intersectedNamesAndDimensions = acm.FDictionary()
                break

        return intersectedNamesAndDimensions

    def ValidParameterNames( self, item):
        columnParameter = item.GetData()
        columnId = columnParameter.ColumnId()
        validNames = set()

        if columnId:
            liveColumnDefinition = acm.Risk.CreateLiveColumnDefinition( columnId, acm.ExtensionTools().GetDefaultContext().Name() )
            if liveColumnDefinition.UnfixedParameters():
                for param in liveColumnDefinition.UnfixedParameters():
                    validNames.add( str(param.Name()) )
            
        return validNames

    def ValidParameterNamesForSelection( self ):
        items = self.m_contributorListCtrl.GetSelectedItems()
        validNames = None
        for item in items:
            validNamesForItem = self.ValidParameterNames( item )
            if validNamesForItem:
                if validNames :
                    toRemove = []
                    for name in validNames :
                        if not name in validNamesForItem :
                            toRemove.append(name)

                    for name in toRemove :
                        validNames.remove(name)
                else:
                    validNames = validNamesForItem
            else:
                validNames = None
                break

        return validNames
        
    def CandAddDimensionToColumn(self, validDimensions, contributors):
        canAdd = False

        if validDimensions :
            canAdd = True #fixme


        return canAdd
    
    def AddContributor( self, contributorType):
        typeInfo = self.GetTypeInfo( contributorType )

        if typeInfo.m_shouldHaveSelection :
            selectedItems = self.m_contributorListCtrl.GetSelectedItems()

            if selectedItems :
                source = typeInfo.m_callbackClass.ShowDialog( self, contributorType, None )
                if source :
                    contributors = []
                    for sourceItem in source:
                        contributors.extend(typeInfo.m_callbackClass.ContributorsFromSource( sourceItem ))

                    for item in selectedItems :
                        canAddContributor = True
                        if contributorType == self.ContributorTypeFromPropertiesType(PropertiesType.Dimensions) :
                            validDimension = self.ValidDimensions(item)
                            canAddContributor = self.CandAddDimensionToColumn(validDimension, contributors)

                        if canAddContributor :
                            columnParameter = item.GetData()
                            for contributor in contributors :
                                self.UpdateColumnParameter(columnParameter, contributor)
                                self.UpdateTreeItemFromColumnParameter(item, columnParameter)

                    self.m_changed = True
                    self.UpdateControls()
        else :
            source = typeInfo.m_callbackClass.ShowDialog( self, contributorType, None )
            if source :
                for sourceItem in source:
                    contributors = typeInfo.m_callbackClass.ContributorsFromSource( sourceItem )
                    for contributor in contributors:
                        columnParameter = ColumnParameters()
                        columnParameter.SetColumn(contributor)

                        item = self.AddColumnParameter(columnParameter, 'Columns+ReloadOverlay')
                        item.Select()
                        self.m_changed = True


    def OnAddContributor( self, contributorType):
        self.AddContributor( contributorType )
        
    def EditContributor( self, treeNode, contributor ):
        typeInfo = self.GetTypeInfo( contributor.m_type )
        source =typeInfo.m_callbackClass.SourceFromContributor( contributor )
        editedSource = typeInfo.m_callbackClass.ShowDialog( self, contributor.m_type, source )
        if editedSource:
            for sourceItem in editedSource:
                contributors = typeInfo.m_callbackClass.ContributorsFromSource( sourceItem )
                for contributor in contributors:
                    treeNode.SetData(  PropertiesData(PropertiesType.Contributor, contributor ) )
                    treeNode.Label( DisplayNameFromContributor(contributor))
                    
                    self.m_changed = True

        return contributor

    def GetSelectedPropertiesData(self) :
        item = self.m_propertiesTree.GetSelectedItem()
        data = None
        propertiesData = item.GetData()

        if propertiesData :
            data = propertiesData.Data()

        return data

    def ContributorTypeFromPropertiesType(self, propertiesType) :
        if propertiesType == PropertiesType.Dimensions :
            contributorType = 'Vector'
        elif propertiesType == PropertiesType.Parameters :      
            contributorType = 'Parameters'
        elif propertiesType == PropertiesType.Scenarios :      
            contributorType = 'Scenario'

        return contributorType

    def OnAdd(self, columnParameter):
        item = self.m_propertiesTree.GetSelectedItem()
        propertiesData = item.GetData()
        contributorType = self.ContributorTypeFromPropertiesType(propertiesData.Type())

        if contributorType :
            self.AddContributor( contributorType )

            

    def OnEdit( self, columnParameter):
        item = self.m_propertiesTree.GetSelectedItem()

        contributor = self.GetSelectedPropertiesData()

        if contributor:
            newContributor = self.EditContributor( item, contributor )
            columnParameter.ReplaceContributor(contributor, newContributor)
            items = self.m_contributorListCtrl.GetSelectedItems() 
            for item in items :
                self.UpdateTreeItemFromColumnParameter(item, item.GetData())

            self.m_propertiesTree.ForceRedraw()
            self.m_changed = True

    def OnRemove( self, columnParameter):
        item = self.m_propertiesTree.GetSelectedItem()
        contributor = self.GetSelectedPropertiesData()

        if contributor:
            item.Remove()
            columnParameter.RemoveContributor(contributor)
            contributorItems = self.m_contributorListCtrl.GetSelectedItems() 
            for contributorItem in contributorItems :
                self.UpdateTreeItemFromColumnParameter(contributorItem, contributorItem.GetData())

            self.m_propertiesTree.ForceRedraw()
            self.m_changed = True
    
    def ItemDefinesColumn( self, item ):
        columnParameter = item.GetData()
        return columnParameter.DefinesColumns()
        
    def SelectionDefinesColumns( self ):
        items = self.m_contributorListCtrl.GetSelectedItems()

        for item in items:
            if self.ItemDefinesColumn( item ):
                return True
                
        return False
        
    def MenuCB( self, contributorType ):
        self.AddContributor( contributorType )
        
    def AddColumnMenuCB(self, contributorType) :
        self.AddColumn()

    def GetParameterizeMenu(self):
        menu = acm.FUxMenu()
        childCustomSubMenu = None

        for typeInfo in self.m_menuTypeInfo[MenuType.Parameter]:
            menu.AddItem( self.MenuCB, typeInfo.m_typeName, typeInfo.m_displayName + '...', '', typeInfo.m_callbackClass.Enabled( self, typeInfo.m_typeName ) )

        menu.AddSeparator()

        for typeInfo in self.m_menuTypeInfo[MenuType.CustomParameter]:
            menu.AddItem( self.MenuCB, typeInfo.m_typeName, typeInfo.m_displayName + '...', '', typeInfo.m_callbackClass.Enabled( self, typeInfo.m_typeName ) )


        return menu

    def GetColumnMenu(self):
        menu = acm.FUxMenu()
        childCustomSubMenu = None

        for typeInfo in self.m_menuTypeInfo[MenuType.Column]:
            menu.AddItem( self.AddColumnMenuCB, typeInfo.m_typeName, typeInfo.m_displayName + '...', '', typeInfo.m_callbackClass.Enabled( self, typeInfo.m_typeName ) )

        menu.AddSeparator()

        for typeInfo in self.m_menuTypeInfo[MenuType.CustomColumn]:
            menu.AddItem( self.MenuCB, typeInfo.m_typeName, typeInfo.m_displayName + '...', '', typeInfo.m_callbackClass.Enabled( self, typeInfo.m_typeName ) )


        return menu


    def OnCopyToColumns(self, ud) :
        self.AddColumn()

    def OnAddColumn(self, ud) :
        self.AddColumn()

    def OnCopyToColumns(self, columnParameterSource) :
        self.AddColumn(columnParameterSource)
                
    def AddColumn(self, columnParameterSource = None) :
        source = CommandCallbacks.Column.ShowDialog( self)

        if source:
            names = self.GetColumnNames()
            self.m_contributorListCtrl.SelectAllItems(False)
        
            for sourceItem in source:
                columnParameter = columnParameterSource.Copy() if columnParameterSource else ColumnParameters()
                contributors = CommandCallbacks.Column.ContributorsFromSource( sourceItem )
                for contributor in contributors:
                    self.UpdateColumnParameter(columnParameter, contributor)

                name = columnParameter.ColumnName()
                origName = name
                count = 1
                while name in names :
                    name = origName + str(count)
                    count += 1

                names.append(name)
                columnParameter.SetColumnName(name)
                

                item = self.AddColumnParameter(columnParameter)
                item.Select()

            self.UpdateControls()
            self.m_changed = True

    def GetColumnNames(self) :
        items = self.m_contributorListCtrl.GetRootItem().Children()
        names = []
        if items :
            for item in items : 
                columnParameters = item.GetData()
                names.append(columnParameters.ColumnName())

        return names

    def RenameColumn(self):
        item = self.m_contributorListCtrl.GetSelectedItem()
        if item :
            columnParameter = item.GetData()
            if columnParameter :
                names = self.GetColumnNames()
                names.remove(columnParameter.ColumnName())

                newName = FUxUtils.ShowGetShortTextDialog(self.m_shell, 'Rename Column', 'Column Name', columnParameter.ColumnName(), -1, False, names)
                if newName :
                    columnParameter.SetColumnName(newName)
                    self.UpdateTreeItemFromColumnParameter(item, columnParameter)
                    self.m_changed = True

    def OnRenameButton(self, ud, cd) :
        self.RenameColumn()

    def OnParameterize(self, ud, cd) :
        menu = self.GetParameterizeMenu()
        menu.Track( self.m_parameterizeButton )

    def OnAddColumnButton( self, ud, cd ):
        if self.m_menuTypeInfo[MenuType.CustomColumn]:
            menu = self.GetColumnMenu()
            menu.Track( self.m_addColumnButton)
        else:
            self.AddColumn()

    def OnTreeSelectionCanged( self, ud, cd ):
        self.UpdateControls()

    def PopulateContributors(self, node, folderName, contributors) :
        folder = node.AddChild()
        folder.Label(folderName)
        folder.Icon('Folder', 'OpenFolder')
        folder.SetData(PropertiesData(folderName, None))

        for contributor in contributors :
            self.AddPropertiesItem(folder, contributor)


    def PopulateProperties( self, node, columnParameters ):
        self.PopulateContributors(node, PropertiesType.Scenarios, columnParameters.m_scenarios)
        self.PopulateContributors(node, PropertiesType.Dimensions, columnParameters.m_vectors)
        self.PopulateContributors(node, PropertiesType.Parameters, columnParameters.m_parameters)
        
    def AddPropertiesItem( self, node, contributor ):
        child = node.AddChild()
        child.SetData( PropertiesData(PropertiesType.Contributor, contributor ))
        child.Icon( self.Icon( contributor), self.Icon( contributor) )
        child.Label( DisplayNameFromContributor(contributor) )

        node.Expand()

        return child

    def UpdatePropertiesTree(self, columnParameters) :
        self.m_propertiesTree.RemoveAllItems()
        self.m_currentColumnParameter = columnParameters

        if columnParameters:
            self.m_propertiesTree.Visible(True)
            self.PopulateProperties(self.m_propertiesTree.GetRootItem(), columnParameters)
        else:
            self.m_propertiesTree.Visible(False)

            
    def HandleCreate(self, layout, shell):
        self.m_shell = shell

        self.m_removeButton = layout.GetControl( 'removeButton' )
        self.m_removeButton.AddCallback( 'Activate', self.OnRemoveButton, None )
        self.m_contributorListCtrl = layout.GetControl( 'contributorList' )
        self.m_contributorListCtrl.EnableMultiSelect( True )
        self.m_contributorListCtrl.ShowColumnHeaders(True)
        self.m_contributorListCtrl.AddCallback( 'ContextMenu', self.OnTreeContextMenu, None )
        self.m_contributorListCtrl.AddCallback( 'SelectionChanged', self.OnTreeSelectionCanged, None )
        self.m_contributorListCtrl.EnableHeaderSorting()

        self.m_contributorListCtrl.AddColumn( 'Column Name', 250)
        self.m_contributorListCtrl.AddColumn( 'Column', 250)
        self.m_contributorListCtrl.AddColumn( 'Scenario', 200 )
        self.m_contributorListCtrl.AddColumn( 'Dimensions', 200 )
        self.m_contributorListCtrl.AddColumn( 'Parameter', 200 )

    
        self.m_addColumnButton = layout.GetControl( 'addColumnButton' )
        self.m_addColumnButton.AddCallback( 'Activate', self.OnAddColumnButton, None )

        self.m_renameButton = layout.GetControl('renameButton')
        self.m_renameButton.AddCallback( 'Activate', self.OnRenameButton, None )


        self.m_parameterizeButton = layout.GetControl('parameterizeButton')
        self.m_parameterizeButton.AddCallback( 'Activate', self.OnParameterize, None )

        self.m_propertiesTree = layout.GetControl('propertiesTree')
        self.m_propertiesTree.EnableMultiSelect( False )
        self.m_propertiesTree.ShowHierarchyLines( True )
        self.m_propertiesTree.ShowColumnHeaders(True)
        self.m_propertiesTree.ColumnLabel(0, 'Properties')
        self.m_propertiesTree.ColumnWidth(0, 200)
        self.m_propertiesTree.AddCallback( 'ContextMenu', self.OnPropertiesContextMenu, None )

        self.HandleParams( self.GetParams() )
        self.UpdateControls()

        
    
    def TreeDataDo( self, nodeData, doBlock ):
        if nodeData['contributor']:
            contributor = Contributor( nodeData['contributor'] )
            doBlock( contributor )
        if nodeData['children']:
            for child in nodeData['children']:
                self.TreeDataDo( child, doBlock )

    def UpdateTreeItemFromColumnParameter(self, item, columnParameter, icon = 'Columns') :
        try:
            item.SetData( columnParameter )
            item.Label( columnParameter.ColumnName(), ColumnIndex.Name)
            item.Label( columnParameter.ColumnAsString(), ColumnIndex.Column)
            item.Label( columnParameter.ScenariosAsString(), ColumnIndex.Scenario )
            item.Label( columnParameter.VectorsAsString(), ColumnIndex.Vector)
            item.Label( columnParameter.ParametersAsString(), ColumnIndex.Parameter)
            item.Icon(icon, icon)
        except Exception as e:
            print(e)


    def AddColumnParameter(self, columnParameter, icon = 'Columns') :
        child = self.GetRootItem().AddChild()
        self.UpdateTreeItemFromColumnParameter(child, columnParameter, icon)

        return child
        
    def Populate( self, columnParameters):
        for columnParameter in columnParameters:
            self.AddColumnParameter(columnParameter)

    def ScenariosString( self, scenarios ):
        return self.ContributorAsString( [scenario.Name() for scenario in scenarios] )
        
    def VectorsString( self, vectorConfig ):
        if vectorConfig:
            return self.ContributorAsString( [str(dimensionId) for dimensionId in vectorConfig.DimensionIds()] )

        return ''

    def UpdateColumnParameter(self, columnParameter, contributor) :
        if contributor:
            if contributor.m_type == 'Parameters':
                columnParameter.AddParameter(contributor)
            elif contributor.m_type == 'Vector':
                columnParameter.AddVector(contributor)
            elif contributor.m_type == 'Scenario':
                columnParameter.AddScenario(contributor)
            elif contributor.m_type == 'Column':
                columnParameter.SetColumn(contributor)
            elif contributor.m_customContributor is not None:
                if contributor.DefinesColumns() :
                    columnParameter.SetColumn(contributor)
                else:
                    columnParameter.AddCustom(contributor)
            else:
                pass

    def CreateColumnParameters(self, columnParameter, columnParameters, params) :
        contributor = params['contributor']
        if contributor :
            contributor = Contributor(contributor)
            self.UpdateColumnParameter(columnParameter, contributor)

        columnParameterCopy = columnParameter.Copy()
        if params['children']:
            first = True
            for child in params['children']:
                if not first :
                    columnParameter = columnParameterCopy.Copy()
                    columnParameters.append(columnParameter)

                first = False
                self.CreateColumnParameters(columnParameter, columnParameters, child)

    def HandleParams( self, params ):
        self.m_contributorListCtrl.RemoveAllItems()
        if params :
            treeData = params and params['tree']
            if treeData :
                columnParameter = ColumnParameters()
                columnParameters = [columnParameter]
                self.CreateColumnParameters(columnParameter, columnParameters, treeData)

                self.Populate( columnParameters )

    def CreateCurrentParams(self):
        params = acm.FDictionary()
        root = self.GetRootItem()
        params['tree'] = acm.FDictionary()
        params['idPrefix'] = self.m_storage.Name()

        items = self.m_contributorListCtrl.GetRootItem().Children()
        children = acm.FArray()

        if items :
            for item in items : 
                columnParameters = item.GetData()
                children.Add(columnParameters.ToParams())

        if not children.IsEmpty() :
            params['tree']['children'] = children

        return params

    def HandleApply( self ):
        params = self.CreateCurrentParams();

        self.m_storage.CalculationColumnSpecificationCollection( 
            acm.PositionStorage().CreateCalculationColumnSpecificationGenerator(
                'MeasureSpecificationGenerator',
                acm.ExtensionTools().GetDefaultContext().Name(),
                params
            )
        )
        self.m_changed = False

    def BuildLayout( self, builder ):
        builder.BeginHorzBox()
        builder.    BeginVertBox()
        builder.        BeginHorzBox()
        builder.            AddList( 'contributorList', 20, -1, 50)
        builder.            AddTree('propertiesTree', 250, 250, 200)
        builder.        EndBox()
        builder.      BeginHorzBox()
        if self.m_menuTypeInfo[MenuType.CustomColumn] :
            builder.        AddButton( 'addColumnButton', 'Add Columns >' )
        else :
            builder.        AddButton( 'addColumnButton', 'Add Columns' )
        builder.        AddButton( 'parameterizeButton', 'Parameterize >' )
        builder.        AddButton( 'renameButton', 'Rename...' )
        builder.        AddButton( 'removeButton', 'Remove' )
        builder.      EndBox()
        builder.    EndBox()
        builder.EndBox()
        
    def SetContents( self, contents ):
        self.m_storage = contents
        
    def IsDirty( self ):
        return self.m_changed

def Create(shell):
    return MeasureGenerator(shell)
