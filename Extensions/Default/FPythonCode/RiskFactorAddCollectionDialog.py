import itertools
import string
import acm
import FUxCore

import RiskFactorUtils
import RiskFactorGetShortNameDialog

from RiskFactorUtils import s_supportedRiskFactorMappingTypes

s_choiceListName = 'Risk Factor Dimensions'
s_customDimensionChoices = []
s_excludedDimensions = ['FX Matrix', 'BenchmarkInstrument']
s_excludedValueParameters = ['BenchmarkShiftType']

for customDimensionChoiceList in acm.FChoiceList.Select( 'list="' + s_choiceListName + '"' ):
    s_customDimensionChoices.append( customDimensionChoiceList )

s_choiceListType = type(acm.FChoiceList())

def ShowAdd(shell, names, riskFactorSetup) :
    dlg = RiskFactorAddCollectionDialog(names, riskFactorSetup)
    
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg) 

def ShowEdit(shell, names, riskFactorCollection) :
    dlg = RiskFactorEditCollectionDialog(names, riskFactorCollection)

    return acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg) 


def HasAddInfoSpecs(riskFactorSetup) :
    addInfoSpecs = RiskFactorUtils.GetAddInfoSpecsFromRiskFactorSetup(riskFactorSetup, 'RiskFactorCollection', False)
    return addInfoSpecs != None and len(addInfoSpecs) > 0


class RiskFactorValueConfigurationControls:

    def __init__(self, layout):
        self.m_riskFactorType = None
        self.m_binders = {}
        self.m_bindings = acm.FUxDataBindings()
        self.m_layout = layout

    def UpdateRiskFactorType(self, riskFactorTypeName) :
        self.m_riskFactorType = acm.RiskFactor().RiskFactorType(riskFactorTypeName)
        self.UpdateLayout()

    def ValidKeys(self, valueFormatData):
        for name in valueFormatData.Keys():
            if str(name) not in s_excludedValueParameters:
                yield name
        
    def UpdateLayout(self):
        self.m_binders = {}
        self.m_bindings = acm.FUxDataBindings()
        self.m_layout.SetLayout(self.GetLayout(), 'riskFactorValueConfiguration')

        for binder in self.m_binders.values():
            binder.InitLayout( self.m_layout )

        valueFormatData = self.m_riskFactorType.ValueFormatData()

        for name in self.ValidKeys(valueFormatData):
            ctrl = self.m_layout.GetControl( self.GetCtrlName( name ) )
            if ctrl.ItemExists('None') :
                ctrl.RemoveItem('None')


    def AddSelectionChangedCallback( self, callback ):
        valueFormatData = self.m_riskFactorType.ValueFormatData()

        for name in self.ValidKeys(valueFormatData):
            ctrl = self.m_layout.GetControl( self.GetCtrlName( name ) )
            ctrl.AddCallback( 'Changed', callback, name )

    def GetValues( self ):
        values = {}

        for valueFormat, binder in self.m_binders.iteritems():
            values[valueFormat] = binder.GetValue()

        return values

    def GetCtrlName(self, valueFormat) :
        return  str(valueFormat)

    def GetLayout(self):
        dict = acm.FDictionary()
        dict.AtPut(acm.FSymbol('DefaultComponentDirection'), acm.FSymbol('Vertical'))

        valueFormatData = self.m_riskFactorType.ValueFormatData()
        builder = acm.FUxLayoutBuilder(dict)

        builder.BeginHorzBox()

        for name in self.ValidKeys(valueFormatData):
            formatData = valueFormatData.At(name)
            displayName = formatData.At(acm.FSymbol('DisplayName'))
            domain = formatData.At(acm.FSymbol('Domain'))
            self.m_binders[name] = self.m_bindings.AddBinderAndBuildLayoutPart( builder, name, displayName, domain)

        builder.EndBox()

        return builder

    def Enabled(self, enable) :
        for binder in self.m_binders.values():
            binder.Enabled(enable)

    def ValidSelection(self) :
        validSelection = True
        for binder in self.m_binders.values():
            if not binder.GetValue() :
                validSelection = False
                break

        return validSelection

class RiskFactorCollectionAttributesPane :
    def __init__(self, layout, riskFactorSetup, direction = 'Horizontal'):
        self.m_layout = layout
        self.m_binders = {}
        self.m_addInfoSpecByBinder = {}
        self.m_bindings = acm.FUxDataBindings()
        self.m_riskFactorSetup = riskFactorSetup
        self.m_direction = direction
        self.m_riskFactorCollection = None

    def UpdateLayout(self, riskFactorSetup = None, enabled = True) :
        if riskFactorSetup:
            self.m_riskFactorSetup = riskFactorSetup
        
        self.m_binders = {}
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)
        self.m_addInfoSpecByBinder = {}
        self.m_riskFactorCollection = None

        if self.m_riskFactorSetup :
            self.m_layout.SetLayout(self.GetLayout(), 'riskFactorCollectionAttributes')

            for binder in self.m_binders.values():
                binder.InitLayout( self.m_layout )
                binder.Enabled(enabled)


    def ServerUpdate(self, sender, aspectSymbol, parameter):
        #if aspectSymbol == 'ControlModifyFinished':
        binderValue = parameter.GetValue()
        addInfoSpec = self.m_addInfoSpecByBinder.get(parameter)

        if addInfoSpec and self.m_riskFactorCollection:
            RiskFactorUtils.setAddInfo(addInfoSpec, self.m_riskFactorCollection, binderValue)

    def Populate(self, riskFactorCollection, storeRiskFactorCollection = False):
        if riskFactorCollection:
            for addInfoSpec, binder in self.m_binders.iteritems():
                value, desc = RiskFactorUtils.getAddInfo(addInfoSpec, riskFactorCollection)
                if value:
                    binder.SetValue(value)
    
        if storeRiskFactorCollection:
            self.m_riskFactorCollection = riskFactorCollection

    def GetValues(self) :
        values = {}

        for addInfoSpec, binder in self.m_binders.iteritems():
            values[addInfoSpec] = binder.GetValue()

        return values


    def GetLayout(self):
        addInfoSpecs = RiskFactorUtils.GetAddInfoSpecsFromRiskFactorSetup(self.m_riskFactorSetup, 'RiskFactorCollection', False)

        dict = None

        if self.m_direction == 'Horizontal' :
            dict = acm.FDictionary()
            dict.AtPut(acm.FSymbol('DefaultComponentDirection'), acm.FSymbol('Vertical'))

        builder = acm.FUxLayoutBuilder(dict)
    
        if self.m_direction == 'Horizontal' :
            builder.BeginHorzBox()
        else:
            builder.BeginVertBox()

        for index, addInfoSpec in enumerate(addInfoSpecs) :
            binder = self.m_bindings.AddBinderAndBuildLayoutPart( builder, 'ctrl' + str(index), addInfoSpec.FieldName(), addInfoSpec.DataDomain())
            self.m_binders[addInfoSpec] = binder
            self.m_addInfoSpecByBinder[binder] = addInfoSpec
            
        builder.EndBox()

        return builder

class CoreDimension:
    def __init__(self, name, displayName, domain, coordinatesSource = None) :
        self.m_name = name
        self.m_domain = domain
        self.m_coordinatesSource = coordinatesSource
        self.m_displayName = displayName
 
class SelectedDimension:
    def __init__(self, displayName, coreDimension,  methodChain = None):
        self.m_displayName = displayName
        self.m_coreDimension = coreDimension
        self.m_methodChain = methodChain

    def DisplayName(self) :
        displayName = self.m_displayName
        
        if not displayName :
            displayName = self.m_methodChain

        if not displayName :
            displayName = self.m_coreDimension.m_displayName

        return displayName

def PopulateOptionAndSelectFirst(ctrl, choices) :
    firstChoice = None
    for choice in choices :
        if not firstChoice :
            firstChoice = choice

        ctrl.AddItem(choice)

    if firstChoice :
        ctrl.SetData(firstChoice)

    return firstChoice

def NameFromObject(obj) :
    name = obj.m_name
    if isinstance(name, s_choiceListType) :
        name = name.Name()

    return name


class RiskFactorEditCollectionDialog( FUxCore.LayoutDialog ):
    def __init__(self, names, riskFactorCollection):
        self.m_fuxDlg = None
        self.m_names = names
        self.m_riskFactorCollection = riskFactorCollection
        self.m_riskFactorSetup = riskFactorCollection.RiskFactorSetup()
        self.m_nameCtrl = None
        self.m_riskFactorCollectionAttributePane = None
        self.m_okButton = None


    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        
        self.m_nameCtrl = layout.GetControl('name')
        self.m_nameCtrl.SetData(self.m_riskFactorCollection.DisplayName())

        self.m_nameCtrl.AddCallback('Changed', self.OnNameCtrlChanged, None )
        self.m_okButton = layout.GetControl('ok')


        if HasAddInfoSpecs(self.m_riskFactorSetup) :
            self.m_riskFactorCollectionAttributePane  = RiskFactorCollectionAttributesPane(layout.GetChildLayout('riskFactorCollectionAttributesPane'), self.m_riskFactorSetup, 'Vertical')
            self.m_riskFactorCollectionAttributePane.UpdateLayout()
            self.m_riskFactorCollectionAttributePane.Populate(self.m_riskFactorCollection)

    def OnNameCtrlChanged( self, cd, d ):
        self.UpdateControls()

    def UpdateControls(self):
        name = self.m_nameCtrl.GetData()
        self.m_okButton.Enabled(name != None and len(name) > 0)

    def CreateLayout(self) :
        builder = acm.FUxLayoutBuilder()

        builder.BeginVertBox()
        builder.    AddInput('name', 'Name')
        if HasAddInfoSpecs(self.m_riskFactorCollection.RiskFactorSetup()) :
            builder.      AddChildLayout('riskFactorCollectionAttributesPane', -1, -1, False)
        builder.    BeginHorzBox('Invisible')
        builder.        AddFill()
        builder.        AddButton('ok', 'OK')
        builder.        AddButton('cancel', 'Cancel')
        builder.    EndBox()

        builder.EndBox()

        return builder

    def HandleApply(self):
        name = self.m_nameCtrl.GetData()
        ok = None
        if name in self.m_names and name != self.m_riskFactorCollection.DisplayName():
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'The name ' + name + ' already exist in the current setup. Please select another name')
        else :
            self.m_riskFactorCollection.DisplayName(name)
            if self.m_riskFactorCollectionAttributePane :
                values = self.m_riskFactorCollectionAttributePane.GetValues()

                for addInfoSpec, value in values.iteritems():
                    if value :
                        RiskFactorUtils.setAddInfo(addInfoSpec, self.m_riskFactorCollection, value)
                    else:
                        RiskFactorUtils.clearAddInfo(addInfoSpec, self.m_riskFactorCollection)

            ok = True

        return ok




class RiskFactorAddCollectionDialog( FUxCore.LayoutDialog ):
    def __init__(self, names, riskFactorSetup):
        self.m_fuxDlg = None
        self.m_riskFactorSetup = riskFactorSetup
        self.m_riskFactorTypeCtrl = None
        self.m_nameCtrl = None
        self.m_names = names
        self.m_coreDimensionListCtrl = None
        self.m_selectedDimensionListCtrl = None
        self.m_customDimensionGroup = None
        self.m_dimensionGroup = None
        self.m_selectedDimensionGroup = None
        self.m_addDimensionButton = None
        self.m_otherButton = None
        self.m_removeCustomButton = None
        self.m_addCustomButton = None
        self.m_createCustomButton = None
        self.m_removeDimensionButton = None
        self.m_renameDimensionButton = None
        self.m_mapDimensionButton = None
        self.m_okButton = None
        self.m_valueFormatControls = None
        self.m_riskFactorCollectionAttributePane = None

    def CoreDimensions( self):
        coreDimensions = []
        riskFactorType = acm.RiskFactor().RiskFactorType( self.m_riskFactorTypeCtrl.GetData()  )

        for dimId in riskFactorType.DimensionData().Keys():
            if str(dimId) in s_excludedDimensions:
                continue
            formatData = riskFactorType.DimensionData().At(dimId)
            displayName = formatData.At(acm.FSymbol('DisplayName'))
            domain = formatData.At(acm.FSymbol('Domain'))

            coreDimensions.append( CoreDimension( dimId, displayName, domain) )
        
        return coreDimensions
    

    def RFIsSelected(self):
        return self.m_riskFactorTypeCtrl.GetData() != None
    
    def CanAddSelectedDimensions(self) :
        selectedDimensionNames = self.GetSelectedDimensionNames()

        enableAdd = False

        if self.m_coreDimensionListCtrl.SelectedCount() > 0 :
            enableAdd = True

            for item in self.m_coreDimensionListCtrl.GetSelectedItems():
                coreDimension = item.GetData()
                text = str(coreDimension.m_name)
                if text in selectedDimensionNames:
                    enableAdd = False
                    break

        return enableAdd

    def UpdateControls(self):
        selectCount = self.m_coreDimensionListCtrl.SelectedCount()
        selectedListItem = self.m_coreDimensionListCtrl.GetSelectedItem()

        self.m_addDimensionButton.Enabled(self.CanAddSelectedDimensions())

        enableOther = selectCount == 1

        if enableOther and selectedListItem :
            dataDomain = selectedListItem.GetData()
            enableOther = hasattr(dataDomain.m_domain, 'IncludesBehavior')

            if enableOther :
                enableOther = dataDomain.m_domain.IncludesBehavior('FPersistent')

        self.m_otherButton.Enabled(enableOther)

        enableRemove = self.m_selectedDimensionListCtrl.GetSelectedItems().Size() > 0

        for item in self.m_selectedDimensionListCtrl.GetSelectedItems():
            enableRemove = enableRemove and isinstance(item.GetData(), SelectedDimension)

        enableOk = self.m_selectedDimensionListCtrl.GetRootItem().ChildrenCount() > 0

        self.m_riskFactorTypeCtrl.Enabled(not enableOk)
        #self.m_valueFormatControls.Enabled(not enableOk)
        
        if enableOk :
            data = self.m_nameCtrl.GetData()
            if not data :
                enableOk = False 

        if enableOk :
            enableOk = self.m_valueFormatControls.ValidSelection()

        self.m_okButton.Enabled(enableOk)
        
        self.AdjustColumnWidthToFitItems(self.m_coreDimensionListCtrl)

    def AdjustColumnWidthToFitItems(self, listCtrl) :
        for column in range(0, listCtrl.ColumnCount()) :
            listCtrl.AdjustColumnWidthToFitItems(column)

    def UpdateCoreDimensionList(self):
        self.m_coreDimensionListCtrl.RemoveAllItems()

        selectedDimensionNames = self.GetSelectedDimensionNames()
        coreDimensions = self.CoreDimensions()
        coreDimensions.sort(key = lambda dd: dd.m_displayName)
        firstChild = None

        for coreDimension in coreDimensions :
            name = str(coreDimension.m_name)
            displayName = str(coreDimension.m_displayName)

            child = self.m_coreDimensionListCtrl.GetRootItem().AddChild()
            child.Label(displayName, 0)
            child.SetData(coreDimension)

            if name in selectedDimensionNames :
                child.Icon('FreezePane+CheckOverlay')
            else :
                child.Icon('FreezePane')

            if not firstChild :
                firstChild = child

        self.UpdateControls()

        if firstChild :
            firstChild.EnsureVisible()

    def OnNameCtrlChanged( self, cd, d ):
        self.UpdateControls()

    def OnRiskFactorTypeChanged( self, cd, d ):
        self.UpdateCoreDimensionList()
        self.m_valueFormatControls.UpdateRiskFactorType(self.m_riskFactorTypeCtrl.GetData())
        self.m_valueFormatControls.AddSelectionChangedCallback(self.OnValueFormatChanged)

    def OnValueFormatChanged( self, cd, ud ):
        self.UpdateControls()

    def OnDimensionListChanged( self, cd, d ):
        self.UpdateControls()

    def OnSelectedDimensionListChanged( self, cd, d ):
        self.UpdateControls()

    def AddSelectedDimension( self, coreDimension, methodChain = None):
        root = self.m_selectedDimensionListCtrl.GetRootItem()
        icon = 'FreezePane'

        dimension = SelectedDimension(None, coreDimension, methodChain )
        riskFactorType = acm.RiskFactor().RiskFactorType( self.m_riskFactorTypeCtrl.GetData()  )

        newItem = root.AddChild()
        newItem.Label( dimension.DisplayName() )
        newItem.Label( NameFromObject(coreDimension), 1 )

        if dimension.m_methodChain :
            newItem.Label(dimension.m_methodChain, 2)

        if coreDimension.m_coordinatesSource :
            newItem.Label(coreDimension.m_coordinatesSource.StringKey(), 3)

        newItem.Icon(icon, icon)
        newItem.SetData( dimension )
        newItem.Select()

        self.UpdateCoreDimensionList()
        self.AdjustColumnWidthToFitItems(self.m_selectedDimensionListCtrl)


    
    def OnAddButtonClicked( self, cd, d ):
        if self.CanAddSelectedDimensions() :
            selectedItem = self.m_coreDimensionListCtrl.GetSelectedItem()

            if selectedItem:
                coreDimension = selectedItem.GetData()
                if coreDimension.m_domain.Name() == acm.FSymbol('FTimeBucket'):
                    storedTimeBuckets = acm.UX().Dialogs().SelectTimeBuckets(self.m_fuxDlg.Shell(), None)

                    if storedTimeBuckets:
                        coreDimension.m_coordinatesSource = storedTimeBuckets
                        self.AddSelectedDimension( coreDimension )
                elif coreDimension.m_domain.Name() == acm.FSymbol('FStrikeBucket'): 
                    storedStrikeBuckets = acm.UX().Dialogs().SelectStrikeBuckets(self.m_fuxDlg.Shell())
                    
                    if storedStrikeBuckets:
                        coreDimension.m_coordinatesSource = storedStrikeBuckets
                        self.AddSelectedDimension( coreDimension )
                else:
                    self.AddSelectedDimension( coreDimension)
                
            self.UpdateControls()

    def OnOtherButtonClicked( self, cd, d ):
        item = self.m_coreDimensionListCtrl.GetSelectedItem()

        if item:
            coreDimension = item.GetData()
            methodChain = acm.UX().Dialogs().BrowseForMethod(self.m_fuxDlg.Shell(), coreDimension.m_domain, True, True)

            if methodChain :
                self.AddSelectedDimension( coreDimension, str(methodChain))
                
        self.UpdateControls()


    def OnRemoveButtonClicked( self, cd, d ):
        selectedItems = self.m_selectedDimensionListCtrl.GetSelectedItems()
        rootChildren = self.m_selectedDimensionListCtrl.GetRootItem().Children()

        for item in selectedItems :
            if item in rootChildren :
                item.Remove()

        self.UpdateCoreDimensionList()

    def OnRenameButtonClicked( self, cd, d ):
        selectedItem = self.m_selectedDimensionListCtrl.GetSelectedItem()

        if selectedItem:
            data = selectedItem.GetData()

            name = RiskFactorGetShortNameDialog.Show(self.m_fuxDlg.Shell(), 'Rename Selected Dimension', 'Name', data.DisplayName())

            if name:
                data.m_displayName = name
                selectedItem.SetData(data)
                selectedItem.Label(data.DisplayName())


    
    def OnAdvancedControlsChecked( self, cd, d ):
        self.UpdateControls()
        
    def PopulateRiskTypes(self):
        s_supportedRiskFactorMappingTypes.sort()
        firstSelection = PopulateOptionAndSelectFirst(self.m_riskFactorTypeCtrl, s_supportedRiskFactorMappingTypes)
        self.m_valueFormatControls.UpdateRiskFactorType(firstSelection)
        self.m_valueFormatControls.AddSelectionChangedCallback(self.OnValueFormatChanged)
        self.UpdateCoreDimensionList()


    def HandleCreate( self, dlg, layout ):
        self.m_fuxDlg = dlg
        
        self.m_nameCtrl = layout.GetControl('name')
        self.m_nameCtrl.SetData('New Risk Collection')
        RiskFactorUtils.SetTextSelection(self.m_nameCtrl, 0, -1)

        self.m_nameCtrl.AddCallback('Changed', self.OnNameCtrlChanged, None )


        self.m_okButton = layout.GetControl('ok')

        self.m_riskFactorTypeCtrl = layout.GetControl('riskFactorType')
        self.m_riskFactorTypeCtrl.AddCallback('Changed', self.OnRiskFactorTypeChanged, None )
        
        self.m_coreDimensionListCtrl = layout.GetControl('dimensionList')
        self.m_coreDimensionListCtrl.AddColumn('Name')
        self.m_coreDimensionListCtrl.ShowColumnHeaders( True )
        self.m_coreDimensionListCtrl.AddCallback('SelectionChanged', self.OnDimensionListChanged, None )
        self.m_coreDimensionListCtrl.AddCallback('DefaultAction', self.OnAddButtonClicked, None )

        self.m_selectedDimensionListCtrl = layout.GetControl('selectedDimensionList')
        self.m_dimensionGroup = layout.GetControl('dimensionGroup')
        self.m_selectedDimensionGroup = layout.GetControl('selectedDimensionGroup')

        self.m_selectedDimensionListCtrl.AddCallback('SelectionChanged', self.OnSelectedDimensionListChanged, self.m_selectedDimensionListCtrl )
        self.m_selectedDimensionListCtrl.AddColumn('Name', 180)
        self.m_selectedDimensionListCtrl.AddColumn('Core Dimension', 100)
        self.m_selectedDimensionListCtrl.AddColumn('Property', 100)
        self.m_selectedDimensionListCtrl.AddColumn('Coordinate Source', 200)
        self.m_selectedDimensionListCtrl.ShowColumnHeaders( True )

        self.m_selectedDimensionListCtrl.AddCallback('DefaultAction', self.OnRemoveButtonClicked, self.m_selectedDimensionListCtrl )

        self.m_addDimensionButton = layout.GetControl('addButton')
        self.m_addDimensionButton.AddCallback('Activate', self.OnAddButtonClicked, None )
        self.m_otherButton = layout.GetControl('otherButton')
        self.m_otherButton.AddCallback('Activate', self.OnOtherButtonClicked, None )
        
        self.m_removeDimensionButton = layout.GetControl('removeButton')
        self.m_removeDimensionButton.AddCallback('Activate', self.OnRemoveButtonClicked, None )
        self.m_renameDimensionButton = layout.GetControl('renameButton')
        self.m_renameDimensionButton.AddCallback('Activate', self.OnRenameButtonClicked, None )

        self.m_fuxDlg.Caption('Add Risk Factor Collection')

        self.m_valueFormatControls  = RiskFactorValueConfigurationControls(layout.GetChildLayout('riskFactorValueConfiguration'))

        if HasAddInfoSpecs(self.m_riskFactorSetup) :
            self.m_riskFactorCollectionAttributePane  = RiskFactorCollectionAttributesPane(layout.GetChildLayout('riskFactorCollectionAttributesPane'), self.m_riskFactorSetup, 'Vertical')
            self.m_riskFactorCollectionAttributePane.UpdateLayout()

        self.PopulateRiskTypes()
        
    def GetSelectedDimensionNames(self) :
        selectedDimensionNames = []
        children = self.m_selectedDimensionListCtrl.GetRootItem().Children()
        
        for child in children :
            selectedDimension = child.GetData()

            if not selectedDimension.m_methodChain :
                selectedDimensionNames.append(str(selectedDimension.m_coreDimension.m_name))

        return selectedDimensionNames

    def HandleApply(self):
        name = self.m_nameCtrl.GetData()
        riskFactorCollection = None

        if name in self.m_names :
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'The name ' + name + ' already exist in the current setup. Please select another name')
        else :
            riskFactorCollection = acm.FRiskFactorCollection()
            riskFactorCollection.RiskFactorType(self.m_riskFactorTypeCtrl.GetData())
            riskFactorCollection.DisplayName(name)
            riskFactorCollection.RiskFactorSetup(self.m_riskFactorSetup)
            riskFactorCollection.RegisterInStorage()

            dimensionListItems = self.m_selectedDimensionListCtrl.GetRootItem().Children()

            for c in dimensionListItems:
                dim = c.GetData()
            
                customName = None

                riskFactorDimension = acm.FRiskFactorDimension()

                riskFactorDimension.DimensionId(dim.m_coreDimension.m_name)
                riskFactorDimension.DisplayName(dim.DisplayName())
                riskFactorDimension.MethodChain(dim.m_methodChain)
                riskFactorDimension.RiskFactorCollection(riskFactorCollection)
                riskFactorDimension.RegisterInStorage()

                if dim.m_coreDimension.m_coordinatesSource :
                    riskFactorDimension.CoordinatesSource(dim.m_coreDimension.m_coordinatesSource)


            values = self.m_valueFormatControls.GetValues()

            for key in values:
                valueParam = acm.FRiskFactorValueParameter()

                valueParam.ParameterKey( key )
                valueParam.ParameterValue( values[key] )
                riskFactorCollection.RiskFactorValueParameters().Add(valueParam)

                valueParam.RegisterInStorage()

            if self.m_riskFactorCollectionAttributePane :
                values = self.m_riskFactorCollectionAttributePane.GetValues()

                for addInfoSpec, value in values.iteritems():
                    if value :
                        RiskFactorUtils.setAddInfo(addInfoSpec, riskFactorCollection, value)


        return riskFactorCollection

       
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginVertBox('Invisible')
        b.      AddInput('name', 'Name' )
        b.      AddOption('riskFactorType', 'Risk Factor Type')
        b.  EndBox()
        b.  AddChildLayout('riskFactorValueConfiguration', -1, -1, False)
        b.  BeginHorzBox()
        b.      BeginVertBox( 'EtchedIn', 'Available Core Dimensions', 'dimensionGroup')
        b.          AddList('dimensionList', 20, -1, 25, 40)
        b.          BeginHorzBox('None')
        b.              AddFill()
        b.              AddButton('addButton', 'Add')
        b.              AddButton('otherButton', 'Other...')
        b.          EndBox()
        b.      EndBox()
        b.      BeginVertBox('EtchedIn', 'Selected Dimensions', 'selectedDimensionGroup' )
        b.          AddList('selectedDimensionList', 20, -1, 100)
        b.          BeginHorzBox('None')
        b.              AddFill()
        b.              AddButton('renameButton', 'Rename...')
        b.              AddButton('removeButton', 'Remove')
        b.          EndBox()
        b.      EndBox()
        b.  EndBox()
        if HasAddInfoSpecs(self.m_riskFactorSetup) :
            b.  BeginVertBox('EtchedIn', 'Attributes')
            b.      AddChildLayout('riskFactorCollectionAttributesPane', -1, -1, False)
            b.  EndBox()
        b.  BeginHorzBox('Invisible')
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b
