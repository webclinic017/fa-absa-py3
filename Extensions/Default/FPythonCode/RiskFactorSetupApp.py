from __future__ import print_function

import acm
import FUxCore

import RiskFactorUtils
import RiskFactorAddUtils
import RiskFactorTimeBuckets

import RiskFactorAddCollectionDialog
import RiskFactorAddDialog
import RiskFactorEditInstanceDialog
import RiskFactorSelectPropertySpecDialog
import RiskFactorAddInfoSpecCallback
import RiskFactorIdentification

try:
    import RiskFactorShowRiskFactorValueDialog
    hasRiskFactorValueDialog = True
except ImportError as e:
    hasRiskFactorValueDialog = False

s_sortParamItem1Sym = acm.FSymbol('item1')
s_sortParanItem2Sym = acm.FSymbol('item2')
s_sortParamsColumnSym  = acm.FSymbol('column')

def CopyIcon(iconName, newIconName) :
    if not acm.UX().IconFromName(newIconName) :
        icon = acm.UX().IconFromName(iconName)
        icon.Name(newIconName)
        icon.RegisterIcon()

def CreateApplicationInstance():
    CopyIcon('FRiskMatrixSheet', 'FRiskFactorSetup')
    CopyIcon('FRiskMatrixSheet', 'FRiskFactorCollection')
    CopyIcon('FreezePane', 'FRiskFactorDimension')
    reload(RiskFactorAddInfoSpecCallback)
    return RiskFactorSetupApplication()
    
def ReallyStartApplication(shell, count):
    acm.UX().SessionManager().StartApplication('Risk Factor Setup', None)

def StartApplication(eii):
    shell = eii.ExtensionObject().Shell()
    ReallyStartApplication(shell, 0);

class RiskFactorMenuCommand(FUxCore.MenuItem):
    def __init__(self, parent, invokeCB, enabledCB):
        self.m_parent = parent
        self.m_invokeCB = invokeCB
        self.m_enabledCB = enabledCB
        
    def Invoke(self, cd):
        self.m_invokeCB()	

    def Applicable(self):
        return True
        
    def Enabled(self):
        return self.m_enabledCB()
    
    def Checked(self):
        return False

class EditSpecCommand(FUxCore.MenuItem):
    def __init__(self, editCB, cd, enabledCB = None, applicable = True):
        self.m_editCB = editCB
        self.m_cd = cd
        self.m_applicable = applicable
        self.m_enabledCB = enabledCB

    def Invoke(self, cd):
        self.m_editCB(self.m_cd)

    def Applicable(self):
        return self.m_applicable

    def Enabled(self):
        return self.m_enabledCB() if self.m_enabledCB else True
    
    def Checked(self):
        return False

class EditInstanceAddInfoValues(FUxCore.MenuItem):
    def __init__(self, editCB, arg):
        self.m_editCB = editCB
        self.m_cd = arg

    def Invoke(self, cd):
        self.m_editCB(self.m_cd)

    def Applicable(self):
        return True

    def Enabled(self):
        return True
    
    def Checked(self):
        return False

class RiskCoordinatesCommand(FUxCore.MenuItem):
    def __init__(self, parent, enableCB):
        self.m_parent = parent
        self.m_enableCB = enableCB
        
    def Invoke(self, cd):
        if str(cd.Definition().GetName()) =='addCoordinates':
            app = cd.ExtensionObject().CustomLayoutApplication()
            app.AddCoordinates()
        elif str(cd.Definition().GetName()) =='removeCoordinates':
            app = cd.ExtensionObject().CustomLayoutApplication()
            app.RemoveCoordinates()
        elif str(cd.Definition().GetName()) =='editCoordinates':
            app = cd.ExtensionObject().CustomLayoutApplication()
            app.EditCoordinates()
        elif str(cd.Definition().GetName()) =='addRiskFactorsFromValuation':
            app = cd.ExtensionObject().CustomLayoutApplication()
            app.AddFromValuation()
        elif str(cd.Definition().GetName()) == 'addRiskFactorsFromInsertItems':
            app = cd.ExtensionObject().CustomLayoutApplication()
            app.AddFromInsertItems()
        elif str(cd.Definition().GetName()) == 'displayValues':
            app = cd.ExtensionObject().CustomLayoutApplication()
            app.ShowRiskFactorValue()

    def Applicable(self):
        return True
        
    def Enabled(self):
        return self.m_enableCB()
    
    def Checked(self):
        return False


class RiskFactorCollectionData :
    def __init__(self, parent):
        self.m_parent = parent
        
        self.m_riskFactorInstancesListCtrl = None
        
        self.m_riskFactorCollection = None
        self.m_riskFactorInfoLabelCtrl = None
        self.m_factorSetupInfoLabelCtrl = None

        self.m_columnIndexByDimension = {}
        self.m_columnIndexByAddInfoSpec = {}
        self.m_sorterByColumnIndex = {}
        self.m_addInfoSpec = []
        self.m_filterControls = None
        self.m_filterValues = RiskFactorUtils.FilterValues()
        self.m_imageDimensionByUniqueId = {}
        self.m_rowsByRiskFactorInstance = {}
        self.m_instanceKeys = set()
        self.m_pendingPopulate = False
        self.m_pendingUpdateFilterControl = False
        
        self.m_timeBucketMap = None
        self.m_riskFactorIdentifier = RiskFactorIdentification.RiskFactorIdentifier()
        self.m_previousSelection = {}
        
        self.m_selectionChanged = False
        self.m_selectionCount = 0

    def UpdateContents(self, riskFactorCollection) :
        self.m_riskFactorCollection = riskFactorCollection
        
        self.m_filterControls = None
        
        dimensions = self.GetRiskFactorDimensions()
        addInfoSpecs = RiskFactorUtils.GetAddInfoSpecs( self.m_riskFactorCollection, 'RiskFactorInstance', False )
        
        if dimensions:
            sortersByDimension = RiskFactorUtils.CreateSortersForCollection( self.m_riskFactorCollection )
            self.m_filterControls = RiskFactorUtils.FilterControlCollection( dimensions, addInfoSpecs, sortersByDimension )
            
        self.m_filterValues = RiskFactorUtils.FilterValues()

        self.UpdateRiskFactorInfo()
        self.UpdateFactorSetupInfo()
    
    def IsInstanceKeyUnique(self, key) :
        return not key in self.m_instanceKeys

    def UpdateImageRiskFactorCollection(self, riskFactorCollection) :
        self.m_riskFactorCollection = riskFactorCollection

        root = self.m_riskFactorInstancesListCtrl.GetRootItem()

        self.m_rowsByRiskFactorInstance = {}
        
        instanceByKey = {}
        
        instances = riskFactorCollection.RiskFactorInstances()
        for instance in instances:
            if self.IsRiskFactorInstanceVisible( instance ):
                self.SetRiskFactorCoordinatesValues( instance)
            instanceByKey[ RiskFactorUtils.GetRiskFactorInstanceKey(instance) ] = instance

        for child in root.Children() :
            oldInstance = child.GetData() 
            key = RiskFactorUtils.GetRiskFactorInstanceKey(oldInstance)
            instance = instanceByKey.get( key )
            if instance:
                child.SetData(instance)

    def HasSelectedInstance(self) :
        return self.m_riskFactorInstancesListCtrl != None and self.m_riskFactorInstancesListCtrl.GetSelectedItem() != None

    def GetRiskFactorCollection( self ):
        return self.m_riskFactorCollection

    def ColumnIndexFromCoordinate(self, coordinate) :
        dimension = self.ImageDimensionFromCoordinate(coordinate)
    
        return self.m_columnIndexByDimension.get(dimension.UniqueId(), -1)
    
    def ColumnIndexFromAddInfoSpec(self, addInfoSpec) :
        return self.m_columnIndexByAddInfoSpec.get(addInfoSpec, -1)
    
    def SetAddInfoValue(self, node, addInfoSpec, addInfoValue, values) :
        index = self.ColumnIndexFromAddInfoSpec(addInfoSpec)
        if index != -1 :
            addInfoValue = RiskFactorUtils.FormatAddInfoValue(addInfoSpec.DataDomain(), addInfoValue)
            values[index] = addInfoValue
            if node :
                node.Label(addInfoValue, index)

    def SetRiskFactorCoordinatesValues( self, instance, node = None):
        riskFactorCoordinates = instance.RiskFactorCoordinates() 
        
        numberColumns = self.m_riskFactorInstancesListCtrl.ColumnCount()
        values = numberColumns * [None]

        for coordinate in riskFactorCoordinates :
            index = self.ColumnIndexFromCoordinate(coordinate)
            if index != -1 :
                value = coordinate.CoordinateValue()
                value = RiskFactorTimeBuckets.GetCoordinateDisplayValue( self.m_timeBucketMap, coordinate.RiskFactorDimensionUniqueId(), value )
                
                values[index] = value
                if node :
                    node.Label(value, index)

        for addInfoSpec in self.m_addInfoSpec :
            addInfoValue, desc = RiskFactorUtils.getAddInfo(addInfoSpec, instance)
            self.SetAddInfoValue(node, addInfoSpec, addInfoValue, values)

        self.m_rowsByRiskFactorInstance[instance] = values
        self.UpdateFilterControlsOnIdle()

    def AddRiskFactorInstance(self, instance, node):
        node = node.AddChild()
        node.SetData( instance )
        self.SetRiskFactorCoordinatesValues( instance, node )

    def IsRiskFactorInstanceVisible( self, riskFactorInstance):
        riskFactorCoordinates = riskFactorInstance.RiskFactorCoordinates()
        valuesByDimension = {}
        valuesByAddInfoSpec = {}

        for coordinate in riskFactorCoordinates :
            valuesByDimension[self.ImageDimensionFromCoordinate(coordinate).UniqueId()] = coordinate.CoordinateValue()

        for addInfoSpec in self.m_addInfoSpec :
            addInfoValue, desc = RiskFactorUtils.getAddInfo(addInfoSpec, riskFactorInstance)
            addInfoValue = RiskFactorUtils.FormatAddInfoValue(addInfoSpec.DataDomain(), addInfoValue)
            valuesByAddInfoSpec[addInfoSpec] = addInfoValue

        isVisible = True

        for uniqueId, value in self.m_filterValues.m_filterByDimension.iteritems():
            if value:
                coordinate = RiskFactorTimeBuckets.GetCoordinateDisplayValue( self.m_timeBucketMap, uniqueId, valuesByDimension[uniqueId] )
            
                if coordinate != value :
                    isVisible = False
                    break

        if isVisible :
            for addInfoSpec, value in self.m_filterValues.m_filterByAddInfoSpec.iteritems():
                if value:
                    if valuesByAddInfoSpec[addInfoSpec] != value :
                        isVisible = False
                        break
            
        return isVisible

    def AdjustColumnWidth(self, list):
        for column in range(0, list.ColumnCount()) :
            list.AdjustColumnWidthToFitItems(column)
            if column != (list.ColumnCount() - 1) :
                list.ColumnWidth(column, list.ColumnWidth(column) + 30)

    def UpdateFilterControlsOnIdle(self) :
        self.m_pendingUpdateFilterControl = True

    def PopulateRiskFactorInstancesOnIdle(self) :
        self.m_pendingPopulate = True
               
    def PopulateRiskFactorInstances(self) :
        self.m_riskFactorInstancesListCtrl.RedrawEnable(False)
        self.m_riskFactorInstancesListCtrl.RemoveAllItems()
        self.m_rowsByRiskFactorInstance = {}
        self.m_instanceKeys = set()

        riskFactorCollection = self.GetRiskFactorCollection()

        maxValue = 1
        if riskFactorCollection:
            root = self.m_riskFactorInstancesListCtrl.GetRootItem()

            instances = riskFactorCollection.RiskFactorInstances()
            
            maxValue = len(instances)
            stepSize = max(maxValue / 20, 1)
            self.m_parent.m_statusBarProgressPane.SetPosition(0, maxValue)

            for index, instance in enumerate(instances):
                self.m_instanceKeys.add(RiskFactorUtils.GetRiskFactorInstanceKey(instance))
                if self.IsRiskFactorInstanceVisible( instance ):
                    self.AddRiskFactorInstance( instance, root )

                if index % stepSize == 0 :
                    self.m_parent.m_statusBarProgressPane.SetPosition(index, maxValue)
                

        self.AdjustColumnWidth(self.m_riskFactorInstancesListCtrl)

        if maxValue < 500 : # too slow...
            if self.m_riskFactorInstancesListCtrl.ColumnCount() > 0 :
                self.m_riskFactorInstancesListCtrl.SortColumn(0, 'Ascending')

        self.m_riskFactorInstancesListCtrl.RedrawEnable(True)
        self.m_parent.m_statusBarProgressPane.SetPosition(maxValue, maxValue)


    def UpdateControls( self ):
        self.UpdateRiskFactorInfo()

    def ImageDimensionFromCoordinate(self, coordinate):
        return self.m_imageDimensionByUniqueId[coordinate.RiskFactorDimensionUniqueId()]

    def UpdateFilterControls( self ):
        riskFactorCollection = self.GetRiskFactorCollection()
        orderedFilterByDimension = {}
        addedFilterByDimension = {}
        filterByAddInfoSpec = {}

        if riskFactorCollection:

            addInfoSpecs = RiskFactorUtils.GetAddInfoSpecs(riskFactorCollection, 'RiskFactorInstance', False)

            for addInfoSpec in addInfoSpecs :
                filterByAddInfoSpec[addInfoSpec] = set()

            instances = riskFactorCollection.RiskFactorInstances()

            for instance in instances:
                for addInfoSpec in addInfoSpecs :
                    addInfoValue, desc = RiskFactorUtils.getAddInfo(addInfoSpec, instance)
                    addInfoValue = RiskFactorUtils.FormatAddInfoValue(addInfoSpec.DataDomain(), addInfoValue)
                    if addInfoValue:
                        filterByAddInfoSpec[addInfoSpec].add(addInfoValue)

                riskFactorCoordinates = instance.RiskFactorCoordinates()
                for coordinate in riskFactorCoordinates :
                    value = str(coordinate.CoordinateValue())
                    dimension = self.ImageDimensionFromCoordinate(coordinate)
                    filter = addedFilterByDimension.get(dimension)
                    if not filter:
                        filter = set()
                        addedFilterByDimension[dimension] = filter
                        orderedFilterByDimension[dimension] = []

                    value = RiskFactorTimeBuckets.GetCoordinateDisplayValue( self.m_timeBucketMap, coordinate.RiskFactorDimensionUniqueId(), value )

                    if not value in filter :
                        filter.add(value)
                        orderedFilterByDimension[dimension].append(value)

            if self.m_filterControls.Populate(orderedFilterByDimension, filterByAddInfoSpec) :
                self.m_filterValues = self.m_filterControls.GetFilterValues()
                self.PopulateRiskFactorInstancesOnIdle()

    def SetPreviousAddFromValuationSelection( self, selection ):
        self.m_previousSelection = selection.GetSelection()

    def UpdateOnApplyCallback( self ):
        self.UpdateFilterControls()
        self.PopulateRiskFactorInstances()
        self.UpdateControls()

    def OnAddFromInsertItems( self ):
        caption = 'Add - From Insert Items'
        
        selectionCtrl, dependentDimensions = RiskFactorAddUtils.ComputeSelectionControlAndDimensionDependances( self.m_riskFactorCollection )
        riskFactorGenerator = RiskFactorAddUtils.RiskFactorCombinationGenerator(dependentDimensions)
    
        RiskFactorAddDialog.Show( self.m_parent.Shell(), caption, self.m_riskFactorCollection, riskFactorGenerator, selectionCtrl,  self.UpdateOnApplyCallback, self.IsInstanceKeyUnique )
        
    def OnShowRiskFactorValue( self ):
        RiskFactorShowRiskFactorValueDialog.Show(self.m_parent.Shell(), self.m_riskFactorCollection)

    def OnAddFromValuation( self ):
        caption = 'Add - From Valuation'
        
        selectionCtrl = RiskFactorAddUtils.CreateAddFromValuationSelection( self.m_previousSelection )
        riskFactorGenerator = RiskFactorAddUtils.RiskFactorDetectionGenerator( self.m_riskFactorIdentifier, self.m_riskFactorCollection )

        RiskFactorAddDialog.Show( self.m_parent.Shell(), caption, self.m_riskFactorCollection, riskFactorGenerator, selectionCtrl, self.UpdateOnApplyCallback, self.IsInstanceKeyUnique )
        self.SetPreviousAddFromValuationSelection( selectionCtrl )
    
    def OnSpecDefaultAction( self, d, ud ):
        self.OnEdit()

    def OnEdit(self):
        instanceListItems = self.m_riskFactorInstancesListCtrl.GetSelectedItems()
        instance = None
        fields = []
        onlyBoolFields = True

        if instanceListItems.Size() == 1 :
            instance = instanceListItems[0].GetData()
            onlyBoolFields = False
            addInfoSpecs = RiskFactorUtils.GetAddInfoSpecs(self.m_riskFactorCollection, 'RiskFactorInstance', onlyBoolFields)        

            for addInfoSpec in addInfoSpecs :
                value, description = RiskFactorUtils.getAddInfo(addInfoSpec, instance)
                fields.append(RiskFactorEditInstanceDialog.EditField(addInfoSpec.MethodName(), addInfoSpec.FieldName(), addInfoSpec.DataDomain().Name(), value))

            values = RiskFactorEditInstanceDialog.Show( self.m_parent.Shell(), fields )

            if values:
                for instanceListItem in instanceListItems:
                    instance = instanceListItem.GetData()

                    for addInfoSpec in addInfoSpecs :
                        value = values[addInfoSpec.MethodName()]
                        if value :
                            RiskFactorUtils.setAddInfo(addInfoSpec, instance, value)
                        else :
                            RiskFactorUtils.clearAddInfo(addInfoSpec, instance)


                    self.SetRiskFactorCoordinatesValues( instance, instanceListItem)

            self.UpdateRiskFactorInfo()


    def OnRemoveButtonClicked( self, d, ud):
        self.OnRemove()

    def OnRemove(self):
        ret = acm.UX().Dialogs().MessageBoxYesNo(self.m_parent.Shell(), 'Question', 'Are you sure you want to remove the selected risk factors?')

        if ret == 'Button1' :
            instanceListItems = self.m_riskFactorInstancesListCtrl.GetSelectedItems()

            for instanceListItem in instanceListItems:
                instance = instanceListItem.GetData()
                self.m_instanceKeys.remove(RiskFactorUtils.GetRiskFactorInstanceKey(instance))
                instance.Unsimulate()

            self.m_riskFactorInstancesListCtrl.RemoveAllSelectedItems( True )
            self.UpdateRiskFactorInfo()
            self.UpdateFilterControlsOnIdle()



    def SetCoordinates( self, fi ):
        items = fi.GetItems()
        if items:
            dimensionId = fi.Id()
            self.GetRiskFactorCollection().AddCoordinates( acm.FSymbol(dimensionId), items )
            self.UpdateFilterCoordinates( dimensionId )

        self.UpdateControls() 

    def OnFilterChanged( self, d, ud ):
        self.m_filterValues = self.m_filterControls.GetFilterValues()
        self.PopulateRiskFactorInstancesOnIdle()
        
    def OnShowExternalCallback(self, cd, ud) :
        self.m_showExternal = cd.Checked()
        self.UpdateControls()

    def GetLayoutBuilder(self, builder) :
        builder.BeginVertBox('None')
        builder.    BeginVertBox('EtchedIn', 'Risk Factors')
        if self.m_filterControls != None :
            self.m_filterControls.BuildLayout( builder )
        builder.        AddList('riskFactorSpecs')
        builder.        BeginVertBox()
        builder.            AddInput('riskFactorInfoLabel', '')
        builder.            AddInput('factorSetupInfoLabel', '')
        builder.        EndBox()
        builder.    EndBox()
        builder.EndBox()

        return builder


    def GetRiskFactorSetupCollectionColumns(self, riskFactorCollection) :
        self.m_addInfoSpec = []
        self.m_columnIndexByDimension = {}
        self.m_columnIndexByAddInfoSpec = {}

        columnIndex = 0
        dimensions = riskFactorCollection.RiskFactorDimensions()
        for dimension in dimensions:
            self.m_columnIndexByDimension[dimension.UniqueId()] = columnIndex
            
            self.m_riskFactorInstancesListCtrl.AddColumn(dimension.DisplayName(), 150)
            columnIndex += 1

        addInfoSpecs = RiskFactorUtils.GetAddInfoSpecs(self.m_riskFactorCollection, 'RiskFactorInstance', False)

        for addInfoSpec in addInfoSpecs :
            self.m_columnIndexByAddInfoSpec[addInfoSpec] = columnIndex
            self.m_addInfoSpec.append(addInfoSpec)
            
            self.m_riskFactorInstancesListCtrl.AddColumn(addInfoSpec.Name(), 150)
            columnIndex += 1
            
        self.m_timeBucketMap = RiskFactorTimeBuckets.TimeBucketMap( self.m_riskFactorCollection )
        
        self.SetSortersByColumnIndex()
        
    def SetSortersByColumnIndex( self ):
        self.sortersByColumnIndex = {}
        
        soretersByDimension = RiskFactorUtils.CreateSortersForCollection( self.m_riskFactorCollection )
        
        for dim, sorter in soretersByDimension.iteritems():
            self.sortersByColumnIndex[self.m_columnIndexByDimension[dim]] = sorter

    def SetupColumns(self) :
        self.m_riskFactorInstancesListCtrl.RemoveAllItems()
        self.m_rowsByRiskFactorInstance = {}

        while self.m_riskFactorInstancesListCtrl.ColumnCount() > 0 :
            self.m_riskFactorInstancesListCtrl.RemoveColumn(0)

        if self.m_riskFactorCollection :
            self.GetRiskFactorSetupCollectionColumns(self.m_riskFactorCollection)
          
    def Init(self, layout):
        if self.m_filterControls != None :
            self.m_filterControls.HandleCreate( layout )
            self.m_filterControls.AddFilterCallback( self.OnFilterChanged )

        self.m_riskFactorInstancesListCtrl = layout.GetControl('riskFactorSpecs')
        self.m_riskFactorInstancesListCtrl.AddCallback( 'DefaultAction', self.OnSpecDefaultAction, None )
        self.m_riskFactorInstancesListCtrl.AddCallback( 'ContextMenu', self.OnSpecContextMenu, None )
        self.m_riskFactorInstancesListCtrl.AddCallback( 'SelectionChanged', self.OnSpecSelectionChanged, None )
        self.m_riskFactorInstancesListCtrl.EnableMultiSelect( True )
        self.m_riskFactorInstancesListCtrl.EnableHeaderSorting( True )
        self.m_riskFactorInstancesListCtrl.SetSortCallback(self.OnHeaderSortCB, self)

        self.m_riskFactorInfoLabelCtrl = layout.GetControl('riskFactorInfoLabel')
        self.m_riskFactorInfoLabelCtrl.Editable(False)
        self.m_riskFactorInfoLabelCtrl.SetAlignment('Right')

        self.m_factorSetupInfoLabelCtrl = layout.GetControl('factorSetupInfoLabel')
        self.m_factorSetupInfoLabelCtrl.Editable(False)
        self.m_factorSetupInfoLabelCtrl.SetAlignment('Right')

        self.SetupColumns()
        self.m_riskFactorInstancesListCtrl.ShowColumnHeaders()
        self.UpdateImageDimensionByOriginal()
        self.UpdateFilterControlsOnIdle()
        self.PopulateRiskFactorInstancesOnIdle()

    def OnHeaderSortCB( self, params, ud ) :
        item1 = params.At(s_sortParamItem1Sym)
        item2 = params.At(s_sortParanItem2Sym)
        column = params.At(s_sortParamsColumnSym)
        
        sortFunc = self.sortersByColumnIndex.get( column, None )

        row1 = self.m_rowsByRiskFactorInstance.get(item1.GetData(), None)
        row2 = self.m_rowsByRiskFactorInstance.get(item2.GetData(), None)

        ret = 0

        if row1 and row2 and len(row1) > column and len(row2) > column:
            value1 = row1[column]
            value2 = row2[column]

            if sortFunc:
                value1 = sortFunc( value1 )
                value2 = sortFunc( value2 )

            if value1 < value2 :
                ret = -1
            elif value1 > value2 :
                ret = 1

        return ret

    def UpdateImageDimensionByOriginal(self) :
        self.m_imageDimensionByUniqueId = {}
        if self.m_riskFactorCollection :
            dimensions = self.m_riskFactorCollection.RiskFactorDimensions()
            
            for dimension in dimensions :
                self.m_imageDimensionByUniqueId[dimension.UniqueId()] = dimension

    def GetValueParametersDisplayName(self, parameterKey):
        riskFactorCollection = self.GetRiskFactorCollection()
        displayName = parameterKey

        if riskFactorCollection :
            riskFactorType = acm.RiskFactor().RiskFactorType(riskFactorCollection.RiskFactorType())
            valueFormatData = riskFactorType.ValueFormatData()

            formatData = valueFormatData.At(parameterKey)
            displayName = formatData.At(acm.FSymbol('DisplayName'))
        
        return displayName

    def UpdateFactorSetupInfo(self):
        riskFactorCollection = self.GetRiskFactorCollection()
        text = ''
        if riskFactorCollection :
            for valueParams in riskFactorCollection.RiskFactorValueParameters() :
                text = text + ' ' + self.GetValueParametersDisplayName(valueParams.ParameterKey()) + ': ' + valueParams.ParameterValue() + '.'

        self.m_factorSetupInfoLabelCtrl.SetData(text)


    def UpdateRiskFactorInfo(self):
        riskFactorCollection = self.GetRiskFactorCollection()
        riskFactors = 0

        if riskFactorCollection:
            addInfoSpecs = RiskFactorUtils.GetAddInfoSpecs(self.m_riskFactorCollection, 'RiskFactorInstance', True)
            countByAddInfos = {}
            for addInfoSpec in addInfoSpecs :
                countByAddInfos[addInfoSpec] = 0


            for instance in riskFactorCollection.RiskFactorInstances():
                riskFactors += 1
                for addInfoSpec in countByAddInfos.keys() :
                    value, descripton = RiskFactorUtils.getAddInfo(addInfoSpec, instance)
                    if  value:
                        countByAddInfos[addInfoSpec] += 1

            text = '  Risk Factors: ' + str(riskFactors) + '.'
            for addInfoSpec, count in countByAddInfos.iteritems() :
                text = text + ' ' + addInfoSpec.FieldName() + ': ' + str(count) + '.'


            self.m_riskFactorInfoLabelCtrl.SetData(text)


    def GetRiskFactorDimensions(self):
        dimensions = []

        riskFactorCollection = self.GetRiskFactorCollection()
        if  riskFactorCollection:
            dimensionPersitentSet = riskFactorCollection.RiskFactorDimensions()

            for dimension in dimensionPersitentSet :
                dimensions.append(dimension)

        return dimensions

    def CreateCommand(self, cmdName, displayName, cb) :
        command = []

        command.append(cmdName)
        command.append('')
        command.append(displayName)
        command.append('')
        command.append('')
        command.append('')
        command.append(cb)
        command.append(False)

        return command

    def GetRowValues(self, instance) :
        rowValues = self.m_rowsByRiskFactorInstance.get(instance)
        if not rowValues :
            numberColumns = self.m_riskFactorInstancesListCtrl.ColumnCount()
            rowValues = numberColumns * [None]
            self.m_rowsByRiskFactorInstance[instance] = rowValues

        return rowValues

    def OnEditValueCallback(self, addInfoSpec) :
        instanceListItems = self.m_riskFactorInstancesListCtrl.GetSelectedItems()
        value = None
        fields = []

        if instanceListItems.Size() == 1 :
            instance = instanceListItems[0].GetData()
            value, description = RiskFactorUtils.getAddInfo(addInfoSpec, instance)

        fields.append(RiskFactorEditInstanceDialog.EditField(addInfoSpec.MethodName(), addInfoSpec.FieldName(), addInfoSpec.DataDomain().Name(), value))
        values = RiskFactorEditInstanceDialog.Show( self.m_parent.Shell(), fields )

        if values:
            value = values[addInfoSpec.MethodName()]

            self.UpdateAddInfoValue(addInfoSpec, value, instanceListItems)


    def SetAddInfoBoolValueTrue(self, addInfoSpec) :
        self.UpdateAddInfoValue(addInfoSpec, 'Yes', self.m_riskFactorInstancesListCtrl.GetSelectedItems())

    def SetAddInfoBoolValueFalse(self, addInfoSpec) :
        self.UpdateAddInfoValue(addInfoSpec, 'No', self.m_riskFactorInstancesListCtrl.GetSelectedItems())
        
    def UpdateAddInfoValue(self, addInfoSpec, value, instanceListItems):
        for item in instanceListItems:
            instance = item.GetData()
            rowValues = self.GetRowValues(instance)
            RiskFactorUtils.setAddInfo(addInfoSpec, instance, value)
            self.SetAddInfoValue(item, addInfoSpec, value, rowValues)
            
        self.UpdateRiskFactorInfo()
        self.UpdateFilterControlsOnIdle()

    def OnApplyHierarchyNode(self, arg) :
        addInfoSpec, value = arg

        self.UpdateAddInfoValue(addInfoSpec, value, self.m_riskFactorInstancesListCtrl.GetSelectedItems())

     
    def AddHierarchyMenuItem(self, commands, addInfoSpec, parentMenuName, hierarchyTree, hierarchyNode):
        children = hierarchyTree.Children(hierarchyNode)
        if children :
            for node in  children:
                subMenu = parentMenuName + node.DisplayName()
                
                if not hierarchyTree.Children(node) :
                    commands.append(self.CreateCommand('hierarchyMenu' + str(subMenu), subMenu, lambda x = (addInfoSpec, node): EditSpecCommand(self.OnApplyHierarchyNode, x)))

                self.AddHierarchyMenuItem(commands, addInfoSpec, subMenu + '/', hierarchyTree, node)

    def BuildHierarchyContextMenu(self, commands, addInfoSpec):
        parentMenuName = str(addInfoSpec.FieldName()) + '/Add To/'
        hierarchyName = str(addInfoSpec.Description())

        
        hierarchy = acm.FHierarchy[hierarchyName]
        if hierarchy :
            hierarchyTree = acm.FHierarchyTree()
            hierarchyTree.Hierarchy(hierarchy)
    
            self.AddHierarchyMenuItem(commands, addInfoSpec, parentMenuName, hierarchyTree, hierarchyTree.RootNode())

    def GenerateCommandsFromPropertySpecifications(self, riskFactorCollection, commands) :
        if riskFactorCollection :
            addInfoSpecs = RiskFactorUtils.GetAddInfoSpecs(self.m_riskFactorCollection, 'RiskFactorInstance', False)

            for index, addInfoSpec in enumerate(addInfoSpecs):
                subMenuName = str(addInfoSpec.FieldName()) + '/'

                commands.append(self.CreateCommand('editValueCallback' + str(index),  subMenuName + 'Edit', lambda x = addInfoSpec: EditSpecCommand(self.OnEditValueCallback, x)))
                commands.append(self.CreateCommand('FUxMenuItemSeparator', subMenuName, None))

                if RiskFactorUtils.IsAddInfoSpecDomain(addInfoSpec, 'bool') :
                    commands.append(self.CreateCommand('cmdYes' + str(index), subMenuName + 'Yes', lambda x = addInfoSpec: EditInstanceAddInfoValues(self.SetAddInfoBoolValueTrue, x)))
                    commands.append(self.CreateCommand('cmdNo' + str(index), subMenuName + 'No', lambda x= addInfoSpec: EditInstanceAddInfoValues(self.SetAddInfoBoolValueFalse, x)))
                    commands.append(self.CreateCommand('FUxMenuItemSeparator', subMenuName, None))

                if RiskFactorUtils.IsAddInfoSpecDomain(addInfoSpec, 'FHierarchyNode') :
                    self.BuildHierarchyContextMenu(commands, addInfoSpec)

                commands.append(self.CreateCommand('applyValueCallback' + str(index), subMenuName + 'Custom Value', lambda x = addInfoSpec: EditSpecCommand(self.OnApplyValueCallback, x)))
                commands.append(self.CreateCommand('FUxMenuItemSeparator', subMenuName, None))
                commands.append(self.CreateCommand('clearValue' + str(index), subMenuName + 'Clear', lambda x = addInfoSpec: EditSpecCommand(self.OnClearValueCallback, x)))


    def AddSpecContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        
        commands = []

        commands.append(['editSpec',                    '', 'Edit',                         '', '', '', self.CreateEditCommand,                     False ])
        commands.append(FUxCore.Separator())
        self.GenerateCommandsFromPropertySpecifications(self.m_riskFactorCollection, commands)
        commands.append(FUxCore.Separator())
        commands.append(['removeSpec',                  '', 'Remove',                       '', '', '', self.CreateRemoveCommand,                   False ])
        
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))

    def OnSpecContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')

        item = self.m_riskFactorInstancesListCtrl.GetSelectedItem()
        if item :
            obj = item.GetData()

            acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, [obj], False, self.AddSpecContextMenu, None)

    def OnSpecSelectionChanged( self, ud, cd ):
        self.m_selectionChanged = True

    def OnEditFromContextMenu(self, value) :
        self.OnEdit()

    def OnRemoveFromContextMenu(self, value) :
        self.OnRemove()

    def OnClearValueCallback(self, addInfoSpec):
        for item in self.m_riskFactorInstancesListCtrl.GetSelectedItems():
            riskFactorInstance = item.GetData()
            RiskFactorUtils.clearAddInfo(addInfoSpec, riskFactorInstance)
            self.SetRiskFactorCoordinatesValues(riskFactorInstance, item)

        self.UpdateRiskFactorInfo()
        self.UpdateFactorSetupInfo()

    def OnApplyValueCallback(self, addInfoSpec):
        try:
            for item in self.m_riskFactorInstancesListCtrl.GetSelectedItems():
                riskFactorInstance = item.GetData()
                value = RiskFactorAddInfoSpecCallback.CustomValue(riskFactorInstance, addInfoSpec)

                if value != None:
                    if type(value) == type(True) :
                        value = 'Yes' if value else 'No'

                    RiskFactorUtils.setAddInfo(addInfoSpec, riskFactorInstance, value)

                self.SetRiskFactorCoordinatesValues(riskFactorInstance, item)

            self.UpdateRiskFactorInfo()

        except RuntimeError as e:
            print ('Error in RiskFactorGenerateProperySpecValueCallback.Name: ' + str(e))

    def CreateRemoveCommand(self):
        applicable = True
        selected = self.m_riskFactorInstancesListCtrl.GetSelectedItems()
        
        if selected != None:
            applicable = True
        
        return EditSpecCommand(self.OnRemoveFromContextMenu, True, None, applicable)


    def CanAddRiskFactors( self ) :
        return self.GetRiskFactorCollection() is not None

    def CanEditCoordinates(self) :
        if 1 == self.m_selectionCount:
            addInfoSpecs = RiskFactorUtils.GetAddInfoSpecs(self.m_riskFactorCollection, 'RiskFactorInstance', False)
            
            return len( addInfoSpecs ) >= 1
        
        return False   

    def CanRemoveCoordinates(self) :
        return self.m_selectionCount > 0

    def CreateEditCommand(self):
        return EditSpecCommand(self.OnEditFromContextMenu, True, self.CanEditCoordinates)

    def CreateAddInfoSpecContextMenuCommand(self) :
        pass

    def CreateNonModellableTrueCommandCB(self):
        return EditSpecCommand(self.SetIncludeNonModellabelToSelected, True)

    def CreateNonModellableFalseCommandCB(self):
        return EditSpecCommand(self.SetIncludeNonModellabelToSelected, False)


    def OnIdle(self) :
        if self.m_pendingUpdateFilterControl:
            self.UpdateFilterControls()
            self.m_pendingUpdateFilterControl = False

        if self.m_pendingPopulate:
            self.PopulateRiskFactorInstances()
            self.m_pendingPopulate = False

        if self.m_selectionChanged:
            self.m_selectionChanged = False
            
            selectedItems = self.m_riskFactorInstancesListCtrl.GetSelectedItems()
            self.m_selectionCount = selectedItems.Size()

class RiskFactorSetupApplication(FUxCore.LayoutApplication):
    def __init__(self):
        FUxCore.LayoutApplication.__init__(self)

        self.m_imageRiskFactorSetup = None
        self.m_originalRiskFactorSetup = None
        self.m_setups = None
        self.m_dynMenuCount = 0
        
        self.m_index = 0
        self.m_riskFactorData = RiskFactorCollectionData(self)
        self.m_riskFactorCollectionPane = None
        self.m_listPane = None
        self.m_listCtrl = None
        self.m_columnIndexByAddInfoSpec = {}
        
    
    def CreateRiskFactorCollectionAddCommandCB(self):
        return RiskFactorMenuCommand(self, self.ShowSetupCollectionDialog, self.RiskFactorCollectionAddCommandEnabled )
    
    def CreateRiskFactorCollectionRemoveCommandCB(self):
        return RiskFactorMenuCommand(self, self.RemoveRiskFactor, self.RiskFactorCommandsEnabled)    

    def CreateRiskFactorCollectionEditCommandCB(self):
        return RiskFactorMenuCommand(self, self.RenameRiskFactor, self.RiskFactorCommandsEnabled)    
    
    def CreateRiskCoordinatesCommandCB(self):
        return RiskCoordinatesCommand(self, self.m_riskFactorData.CanEditCoordinates)

    def CreateRemoveCoordinatesCommandCB(self):
        return RiskCoordinatesCommand(self, self.m_riskFactorData.CanRemoveCoordinates)

    def CreateAddRiskFactorsCommandCB(self) :
        return RiskCoordinatesCommand(self, self.m_riskFactorData.CanAddRiskFactors )

    def CreateDisplayRiskFactorValuesCommandCB(self) :
        return RiskCoordinatesCommand(self, self.m_riskFactorData.CanAddRiskFactors)


    def CreateManageSplitDefinitionsCommandCB(self):
        return EditSpecCommand(self.OnManageSplitDefinitions, True)

    def CreateSelectInstanceAttributesCommandCB(self) :
        return EditSpecCommand(self.OnSelectInstanceAttribute, True)

    def CreateSelectCollectionAttributesCommandCB(self) :
        return EditSpecCommand(self.OnSelectCollectionAttribute, True)
        


    def OnManageSplitDefinitions(self, ud) :
        RiskFactorManageChoiceListsDialog.Show(self.Shell(), 'Manage Custom Dimensions', RiskFactorAddCollectionDialog.s_choiceListName)
            
    def HandleRegisterCommands(self, builder):
        
        commands =[

        ['addRiskFactorCollection',       'View', 'Add Risk Factor Colelction',    'Add Risk Factor Collection',           'Ctrl+D', 'A',      self.CreateRiskFactorCollectionAddCommandCB, False ],
        ['removeRiskFactorCollection',    'View', 'Remove Risk Factor Collection', 'Remove Risk Factor Collection',        'Ctrl+R', 'R',      self.CreateRiskFactorCollectionRemoveCommandCB, False ],
        ['renameRiskFactorCollection',    'View', 'Rename Risk Factor Collection', 'Rename Risk Factor Collection',        'Ctrl+E', 'e',      self.CreateRiskFactorCollectionEditCommandCB, False ],
        ['addCoordinates',                'View', 'Add Coordinate',                'Add Risk Factors',                     '',       'd',      self.CreateRiskCoordinatesCommandCB, False ],
        ['removeCoordinates',             'View', 'Remove Coordinate',             'Remove Risk Factors',                  '',       'm',      self.CreateRemoveCoordinatesCommandCB, False ],
        ['editCoordinates',               'View', 'Edit Coordinate',               'Edit Risk Factors',                    '',       'i',      self.CreateRiskCoordinatesCommandCB, False ],
        ['selectInstanceAttribute',       'View', 'Instance Attribute',            'Select the instance attributes',       '',       'c',      self.CreateSelectInstanceAttributesCommandCB, False ],
        ['selectCollectionAttribute',     'View', 'Collection Attribute',          'Select the collection attributes',     '',       't',      self.CreateSelectCollectionAttributesCommandCB, False ],
        ['addRiskFactorsFromValuation',   'View', 'From Valuation',                'From Valuation',                       '',       '',       self.CreateAddRiskFactorsCommandCB, False ],
        ['addRiskFactorsFromInsertItems', 'View', 'From Insert Items',             'From Insert Items',                    '',       '',       self.CreateAddRiskFactorsCommandCB, False ]
        ]
        
        if hasRiskFactorValueDialog:
            commands.append( ['displayValues', 'View', 'Dispay risk factor values', 'Display Risk Factor Values', '', '', self.CreateDisplayRiskFactorValuesCommandCB, False ] )
        
        #To be able to use the standard File commands(Open,Save,Save As etc) create an FSet and add the enumerator values corresponding
        #to the commands desired. Look at the FUxStandardFileCommands enum for a list of available commands.
        fileCommands = acm.FSet()
        
        fileCommands.Add('FileNew')
        fileCommands.Add('FileOpen')
        fileCommands.Add('FileSave')
        fileCommands.Add('FileSaveAs')
        fileCommands.Add('FileDelete')
            
        builder.RegisterCommands(FUxCore.ConvertCommands(commands), fileCommands)
    
    def HandleStandardFileCommandInvoke(self, commandName):
        if commandName == 'FileNew':
            self.OnFileNew()
        if commandName == 'FileOpen':
            self.OnFileOpen()
        if commandName == 'FileSaveAs':
            self.OnFileSaveAs()
        if commandName == 'FileSave':
            self.OnFileSave()
        if commandName == 'FileDelete':
            self.OnFileDelete()
            
    def HandleStandardFileCommandEnabled(self, commandName):
        ret = True
        if commandName == 'FileSaveAs':
            ret = self.m_imageRiskFactorSetup != None
        if commandName == 'FileSave':
            ret = self.HasRiskFactorChanged()
        if commandName == 'FileDelete':
            ret = self.m_originalRiskFactorSetup != None

        return ret

    def HasRiskFactorChanged(self) :
        changed = False
        if self.m_imageRiskFactorSetup:
            changed = self.m_imageRiskFactorSetup.IsModified()

        return changed

    def ValidateSaveCB(self, ud, namn, existingItem, p3):
        isValidSave = existingItem == None or existingItem == self.m_originalRiskFactorSetup

        if not isValidSave :
            ret = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Question', 'Are you sure you want to replace the Risk Factor Setup ' + existingItem.StringKey() + '?')
            if ret == 'Button1' :
                try:
                    existingItem.Delete()
                    isValidSave = True
                except RuntimeError as ex:
                    acm.UX().Dialogs().MessageBoxInformation(self.Shell(), 'Unable delete object ' + existingItem.StringKey() + '. Message: ' + ex.message)
                

        return isValidSave

    def OnSelectCollectionAttribute(self, cd):
        if self.SelectAttribute('Risk Factor Collection Attributes', 'RiskFactorCollection') :
            self.SetupRiskFactorCollectionAttributeColumns()
            
            root = self.m_listCtrl.GetRootItem()
            items = root.Children()
            
            for item in items:
                self.PopulateColumns( item )
                
            self.m_riskFactorData.AdjustColumnWidth(self.m_listCtrl)
            
    
    def OnSelectInstanceAttribute(self, cd):
        self.SelectAttribute('Risk Factors Attributes', 'RiskFactorInstance')

    def SelectAttribute(self, caption, addInfoRecType):
        riskFactorSetup = self.m_imageRiskFactorSetup
        ret = False
        if riskFactorSetup :
            addInfoSpecs = RiskFactorSelectPropertySpecDialog.Show(self.Shell(), caption, riskFactorSetup, addInfoRecType)
            if addInfoSpecs != None:
                riskFactorSpecs = riskFactorSetup.RiskFactorPropertySpecifications()
                
                i = 0
                while len(riskFactorSpecs) > i:
                    riskFactorPropertySpecification = riskFactorSpecs[i]
                    
                    if riskFactorPropertySpecification.AdditionalInfoSpec().RecType() == addInfoRecType :
                        riskFactorPropertySpecification.Unsimulate()
                    else:
                        i += 1

                for addInfoSpec in addInfoSpecs :
                    riskFactorPropertySpecification = acm.FRiskFactorPropertySpecification()
                    riskFactorPropertySpecification.AdditionalInfoSpec(addInfoSpec)
                    riskFactorPropertySpecification.RiskFactorSetup(riskFactorSetup)
                    riskFactorPropertySpecification.RegisterInStorage()

                self.ReloadRiskFactorData()
                ret = True

        return ret

    def DoFileNew(self):
        riskFactorSetup = acm.FRiskFactorSetup()
        riskFactorSetup.RegisterInStorage()

        self.HandleObject(riskFactorSetup)

    def OnFileNew(self):
        if self.VerifyCloseSetup('Do you want to save the current setup?'):
            self.DoFileNew()

    def OnFileDelete(self):
        ret = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Question', 'Are you sure you want to delete the current setup?')

        if ret == 'Button1' :
            if self.m_originalRiskFactorSetup :
                self.m_originalRiskFactorSetup.Delete()
                self.DoFileNew()

    def CommitRiskFactorSetup(self, createdNew) :
            if self.m_imageRiskFactorSetup:
                try :
                    self.m_imageRiskFactorSetup.Commit()
                    self.m_imageRiskFactorSetup = self.m_originalRiskFactorSetup.StorageImage()
                    if createdNew :
                        self.Populate()
                        self.AddObjectToMostRecentlyUsedList(self.m_originalRiskFactorSetup)
                        self.SetCaption()
                        self.UpdateControls()
                    else:
                        self.UpdateImageRiskFactorSetup()
                        self.SetCaption()
                except RuntimeError as ex:
                    msg = ex.message.partition('\n')[0] #take first row
                    msg = msg.partition(':')[-1]        #take part after ':' -sign
                    acm.UX().Dialogs().MessageBoxInformation(self.Shell(), 'Unable to save risk factor: ' + self.m_imageRiskFactorSetup.StringKey() + '. \nMessage:' + msg)
                    
    def IsCollectionEqual(self, riskFactorCollection, oldRiskFactorCollection) :
        isEqual = False    
        
        if oldRiskFactorCollection.Original() == riskFactorCollection.Original() :
            isEqual = True
        elif oldRiskFactorCollection.Original() == None: 
            # if the Risk Factor Collection is an infant it doesn't have a Original so compare the DisplayNames then (this should be safe since the UI guarantees uniqness)
            isEqual = oldRiskFactorCollection.DisplayName() == riskFactorCollection.DisplayName()
    
        return isEqual

    def UpdateImageRiskFactorSetup(self) :
        self.m_riskFactorData.UpdateImageDimensionByOriginal()

        root = self.m_listCtrl.GetRootItem()
        riskFactorCollections = self.m_imageRiskFactorSetup.RiskFactorCollections()
        
        for child in root.Children() :
            oldRiskFactorCollection = child.GetData()
            
            for riskFactorCollection in riskFactorCollections :
                if self.IsCollectionEqual(riskFactorCollection, oldRiskFactorCollection) :
                    child.SetData(riskFactorCollection)
                    break

        selectedItem = self.m_listCtrl.GetSelectedItem()


        if selectedItem :
            riskFactorCollection = selectedItem.GetData()
            self.m_riskFactorData.UpdateImageRiskFactorCollection(riskFactorCollection)

    def CreateNewImageRiskFactorIfApplicable(self, name) :
        createdNew = False
        if not self.m_imageRiskFactorSetup.IsInfant():
            createdNew = True
            self.m_imageRiskFactorSetup.StorageSetNew()
            self.m_originalRiskFactorSetup = self.m_imageRiskFactorSetup

            for riskFactorCollection in self.m_imageRiskFactorSetup.RiskFactorCollections() :
                coordinatesByDimensionUniqueId = {}

                for riskFactorInstance in riskFactorCollection.RiskFactorInstances() :
                    for riskFactorCoordinate in riskFactorInstance.RiskFactorCoordinates() :
                        coordinates = coordinatesByDimensionUniqueId.setdefault(riskFactorCoordinate.RiskFactorDimensionUniqueId(), []).append(riskFactorCoordinate)

                for riskFactorDimension in riskFactorCollection.RiskFactorDimensions() :
                    uniqueId = acm.FRiskFactorDimension().UniqueId() #will generate a unqiueId in constructor

                    coordinates = coordinatesByDimensionUniqueId.get(riskFactorDimension.UniqueId(), [])
                    riskFactorDimension.UniqueId(uniqueId)

                    for coordinate in coordinates :
                        coordinate.RiskFactorDimensionUniqueId(uniqueId)
                    
        self.m_imageRiskFactorSetup.Name(name)

        return createdNew

    def DoSaveRiskFactorSetupAs(self) :
        riskFactorSetup  = acm.UX().Dialogs().SaveObjectAs(self.Shell(), 'Save Risk Factor Setup as...', 'Risk Factor Setups',  self.GetSetups(), None, self.ValidateSaveCB, None) 

        if riskFactorSetup != None:
            createdNew = False
            if riskFactorSetup != self.m_originalRiskFactorSetup :
                createdNew = self.CreateNewImageRiskFactorIfApplicable(riskFactorSetup)

            self.CommitRiskFactorSetup(createdNew)

    def OnFileSave(self):
        if self.m_originalRiskFactorSetup.IsInfant():
            self.DoSaveRiskFactorSetupAs()
        else:
            self.CommitRiskFactorSetup(False)
        
    def OnFileSaveAs(self):
        self.DoSaveRiskFactorSetupAs()

        
    def OnFileOpen(self):
        if self.VerifyCloseSetup('Do you want to save the current setup?'):
            selectedObject = acm.UX().Dialogs().SelectObject(self.Shell(), 'Select Risk Factor Setup', 'Risk Factor Setups', self.GetSetups(), None)
            if selectedObject != None:
                self.HandleObject(selectedObject)
    
    def GetSetups(self):
        if self.m_setups == None:
            self.m_setups = acm.FRiskFactorSetup.Select('').SortByProperty('Name')

        return self.m_setups

    def DoOverrideApplicationDefaultSize(self):
        return 1000, 800 #width, height

    def HandleBuildContextMenu(self, builder, cd):
        #Look at HandleRegisterCommands for more information about the command list
        commands =[
        ['addRiskFactorCollection', '', 'Add Risk Factor Collection', '', '', '', self.CreateCommandCB, False ],
        ['editRiskFactorCollection', '', 'Edit Risk Factor Collection', '', '', '', self.CreateCommandCB, True ],
        ]
        
        builder.RegisterCommands(FUxCore.ConvertCommands(commands))
        
    def HandleDefaultAction(self, shell, cd):
        pass
        
    def HandleSetContents(self, contents):
        if contents != None:
            if contents.IsKindOf('FRiskFactorSetup'):
                self.HandleObject(contents)
    
    def HandleGetContents(self):
        return self.m_originalRiskFactorSetup
        
    def GetCurrentObject(self) :
        return self.m_originalRiskFactorSetup

    def CanHandleObject(self, obj):
        ret = False

        if obj :
            ret = obj.IsKindOf('FRiskFactorSetup')

        return ret

    def Populate(self):
        self.SetupRiskFactorCollectionAttributeColumns()

        self.m_listCtrl.RemoveAllItems()
        riskFactorCollections = self.m_imageRiskFactorSetup.RiskFactorCollections()

        riskFactorCollections = riskFactorCollections.SortByProperty('StringKey')
        firstriskFactorCollection = None

        for riskFactorCollection in riskFactorCollections:
            item = self.AddListItem(riskFactorCollection)

            if firstriskFactorCollection == None :
                firstriskFactorCollection = riskFactorCollection
                item.Select()

        self.m_riskFactorData.AdjustColumnWidth(self.m_listCtrl)

        self.UpdateRiskFactorData(firstriskFactorCollection)


    def HandleObject(self, obj):
        if obj.IsKindOf('FRiskFactorSetup'):
            self.m_originalRiskFactorSetup = obj
            if obj.IsInfant():
                self.m_imageRiskFactorSetup = self.m_originalRiskFactorSetup
            else:
                self.m_imageRiskFactorSetup = self.m_originalRiskFactorSetup.StorageImage()

        if self.m_listCtrl :
            self.Populate()
            self.AddObjectToMostRecentlyUsedList(obj)
            self.SetCaption()
            self.UpdateControls()

    def GetApplicationIcon(self):
        return 'FRiskMatrixSheet'
    
    def UpdateControls(self):
        pass
     
    def OnListCtrlChanged(self, ud, cd) :
        item = self.m_listCtrl.GetSelectedItem()

        if item != None:
            riskFactorCollection = item.GetData()
            self.Shell().CallAsynch(self.UpdateRiskFactorDataAsync, riskFactorCollection)

    def UpdateRiskFactorDataAsync(self, riskFactorCollection):
        self.UpdateRiskFactorData(riskFactorCollection)

    def ReloadRiskFactorData(self) :
        self.UpdateRiskFactorData(self.m_riskFactorData.m_riskFactorCollection)

    def UpdateRiskFactorData( self, riskFactorCollection ):

        self.m_riskFactorData.UpdateContents(riskFactorCollection)

        builder = acm.FUxLayoutBuilder()
        self.m_riskFactorData.GetLayoutBuilder(builder)

        self.m_riskFactorCollectionPane.SetLayout(builder, 'riskFactorDataLayout')
        self.m_riskFactorData.Init(self.m_riskFactorCollectionPane)

        self.m_riskFactorData.UpdateControls()
        self.m_riskFactorData.UpdateFactorSetupInfo()

    def GetCurrentRiskFactorNames(self) :
        names = []

        for riskFactorCollection in self.m_imageRiskFactorSetup.RiskFactorCollections() :
            names.append(riskFactorCollection.DisplayName())

        return names

    def ShowSetupCollectionDialog( self ):
        riskFactorCollection = RiskFactorAddCollectionDialog.ShowAdd(self.Shell(), self.GetCurrentRiskFactorNames(), self.m_imageRiskFactorSetup)

        if riskFactorCollection :
            self.UpdateRiskFactorData(riskFactorCollection)
            item = self.AddListItem(riskFactorCollection)
            self.m_listCtrl.SelectAllItems(False)
            item.Select()
            self.UpdateControls()
            
    def UpdateListItem(self, item, riskFactorCollection):
        item.Icon('FRiskMatrixSheet')
        item.SetData(riskFactorCollection)

        self.PopulateColumns( item )

    def PopulateColumns( self, item ):
        riskFactorCollection = item.GetData()
    
        item.Label(riskFactorCollection.DisplayName(), 0)
        item.Label(riskFactorCollection.RiskFactorType(), 1)
    
        for addInfoSpec, index in self.m_columnIndexByAddInfoSpec.iteritems() :
            value, description = RiskFactorUtils.getAddInfo(addInfoSpec, riskFactorCollection)
            
            if value :
                item.Label(value, index)
            else:
                item.Label('', index)

    def AddListItem(self, riskFactorCollection) :
        item = self.m_listCtrl.GetRootItem().AddChild()

        self.UpdateListItem(item, riskFactorCollection)

        return item

    def RenameRiskFactor(self) :
        item = self.m_listCtrl.GetSelectedItem()

        if item :
            riskFactorCollection = item.GetData()
            ok = RiskFactorAddCollectionDialog.ShowEdit(self.Shell(), self.GetCurrentRiskFactorNames(), riskFactorCollection)

            if ok:
                self.UpdateListItem(item, riskFactorCollection)

    def OnRenameRiskFactor(self, cd, ud) :
        self.RenameRiskFactor()

    def RemoveRiskFactor(self) :
        item = self.m_listCtrl.GetSelectedItem()

        if item :
            riskFactorCollection = item.GetData()
            ret = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Question', 'Are you sure you want to remove the risk factor collection: %s' % riskFactorCollection.DisplayName())

            if ret == 'Button1' :
                nextItem = item.Sibling(True)
                if not nextItem :
                    nextItem = item.Sibling(False)

                riskFactorCollection.Unsimulate()
                item.Remove()

                if nextItem:
                    nextItem.Select()
                else:
                    self.UpdateRiskFactorData(None)
    
    def AddFromValuation( self ):
        self.m_riskFactorData.OnAddFromValuation()
        
    def AddFromInsertItems( self ):
        self.m_riskFactorData.OnAddFromInsertItems()
        
    def ShowRiskFactorValue( self ):
        self.m_riskFactorData.OnShowRiskFactorValue()

    def RemoveCoordinates(self):
        self.m_riskFactorData.OnRemove()

    def EditCoordinates(self):
        self.m_riskFactorData.OnEdit()

    def RiskFactorCollectionAddCommandEnabled(self) :
        return self.m_imageRiskFactorSetup != None

    def RiskFactorCommandsEnabled(self):
        return (self.m_listCtrl != None) and (self.m_listCtrl.GetSelectedItem() != None)

    def RiskCoordinatesCommandsEnabled(self):
        return self.m_riskFactorData.HasSelectedInstance()
            
    def SetupRiskFactorCollectionAttributeColumns(self) :
        self.m_columnIndexByAddInfoSpec = {}

        while self.m_listCtrl.ColumnCount() > 2 :
            self.m_listCtrl.RemoveColumn(2)

        addInfoSpecs = RiskFactorUtils.GetAddInfoSpecsFromRiskFactorSetup(self.m_imageRiskFactorSetup, 'RiskFactorCollection', False)
        
        for addInfoSpec in addInfoSpecs :
            self.m_columnIndexByAddInfoSpec[addInfoSpec] = self.m_listCtrl.ColumnCount()
            self.m_listCtrl.AddColumn(addInfoSpec.Name(), 100)

    def HandleCreate( self, creationInfo ):

        listBuilder = acm.FUxLayoutBuilder()
        riskFactorCollectionBuilder = acm.FUxLayoutBuilder()

        listBuilder.BeginVertBox('EtchedIn', 'Risk Factor Collections' )
        listBuilder.    AddList('paneList', 8, -1, 70)
        listBuilder.EndBox()

        self.m_riskFactorData.GetLayoutBuilder(riskFactorCollectionBuilder)

        self.m_listPane = creationInfo.AddPane(listBuilder, 'listPane')
        self.m_riskFactorCollectionPane = creationInfo.AddPane(riskFactorCollectionBuilder, 'riskFactorCollectionPane')

        self.m_listCtrl = self.m_listPane.GetControl('paneList')
        self.m_listCtrl.AddColumn('Name', 150)
        self.m_listCtrl.AddColumn('Risk Factor Type', 140)
        self.SetupRiskFactorCollectionAttributeColumns()
        
        self.m_listCtrl.ShowColumnHeaders(True)
        self.m_listCtrl.AddCallback('Changed', self.OnListCtrlChanged, self)
        self.m_listCtrl.EnableHeaderSorting(True)
        self.m_listCtrl.AddCallback('DefaultAction', self.OnRenameRiskFactor, self)
        self.m_listCtrl.AddCallback('ContextMenu', self.OnRiskFactorCollectionListCtrlContextMenu, self)

        self.m_riskFactorData.Init(self.m_riskFactorCollectionPane)
        
        self.UpdateControls()

        if self.m_imageRiskFactorSetup :
            self.Populate()
            self.AddObjectToMostRecentlyUsedList(self.m_imageRiskFactorSetup)
            self.SetCaption()
        else :
            self.DoFileNew()

        self.EnableOnIdleCallback(True)

        

    def AddRiskFactorCollectionListCtrlContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        commands = [
        ['editRiskFactors',         'View', 'Edit',         'Edit Risk Factor Collection',        'Ctrl+R',   'E',      self.CreateRiskFactorCollectionEditCommandCB, False ],
        FUxCore.Separator(),
        ['removeRiskFactors',       'View', 'Remove',       'Remove Risk Factor Collection',        'Ctrl+R',   'R',      self.CreateRiskFactorCollectionRemoveCommandCB, False ]
        ]

        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))

    def OnRiskFactorCollectionListCtrlContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        
        item = self.m_listCtrl.GetSelectedItem()
        if item :
            obj = item.GetData()

            acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, [obj], False, self.AddRiskFactorCollectionListCtrlContextMenu, None)


    def IsModified(self) :
        ok = True

        ok = ok and self.m_imageRiskFactorSetup != None
        ok = ok and (self.m_imageRiskFactorSetup.IsModified() or self.m_imageRiskFactorSetup.IsInfant())
        ok = ok and self.m_imageRiskFactorSetup.RiskFactorCollections() != None
        ok = ok and len(self.m_imageRiskFactorSetup.RiskFactorCollections()) > 0

        return ok


    def VerifyCloseSetup(self, text) :
        if self.IsModified():
            ret = acm.UX().Dialogs().MessageBoxYesNoCancel(self.Shell(), 'Information', text)

            if ret == 'Button1' :
                return self.OnFileSave()

            if ret == 'Button2' :
                return True

            if ret == 'Button3' :
                return False

        return True

    def HandleClose(self):
        return self.VerifyCloseSetup('Do you want to save before closing the Risk Factor Setup Application?')

    def SetCaption(self):
        if self.m_imageRiskFactorSetup:
            self.SetContentCaption(self.m_imageRiskFactorSetup.StringKey())
    
    def DoChangeCreateParameters( self, createParams ):
        createParams.UseSplitter(True)
        createParams.SplitHorizontal(False)
        createParams.LimitMinSize(True)
        createParams.AutoShrink(False)
        createParams.AdjustPanesWhenResizing(True)
        createParams.ShowMostRecentlyUsedList(True)
        
        
    def HandleCreateStatusBar(self, sb):
        self.m_statusBarProgressPane = sb.AddProgressPane(200)

    def HandleOnIdle(self):
        if self.m_riskFactorData :
            self.m_riskFactorData.OnIdle()
