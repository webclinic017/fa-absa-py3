
import acm
import FUxCore
import GetShortNameDialog
import HierarchyEditorUtils 
import OpenHierarchyDialog

def Show(shell, caption, initialText, validateNameCB, columnSpecification = None):
    customDlg = CreateHierarchyColumnSpecificationDialog(initialText, columnSpecification, validateNameCB, caption)

    columnSpecification = None

    builder = customDlg.CreateLayout()
    
    ret = acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )

    if ret :
        columnSpecification = customDlg.m_columnSpecification

    return columnSpecification

    
class CreateHierarchyColumnSpecificationDialog (FUxCore.LayoutDialog):
    def __init__(self, initialText, columnSpecification, validateNameCB, caption):
        self.m_okButton = 0
        self.m_nameCtrl = None
        self.m_dataDomainCtrl = None
        self.m_dataTypeInfoCtrl = None
        self.m_descriptionCtrl = None
        self.m_restrictionsCtrl = None
        self.m_mandatoryCtrl = None
        self.m_uniqueValuesCtrl = None
        self.m_domainTypeCtrl = None
        self.m_initialText = initialText
        self.m_columnSpecification = columnSpecification
        self.m_domainTypes = {}
        self.m_standardDomains = acm.FEnumeration['enum(B92StandardType)'].EnumeratorStringsSkipFirst().Sort()
        self.m_enumDomains = acm.FEnumeration['enum(B92EnumType)'].EnumeratorStringsSkipFirst().Sort()
        self.m_refsDomains = acm.FEnumeration['enum(B92RecordType)'].EnumeratorStringsSkipFirst().Sort()
        self.m_columnSpecificationRestriction = acm.FEnumeration['enum(HierarchyColumnRestriction)'].Enumerators()

        self.m_choiceListsPopulated = False
        self.m_validateNameCB = validateNameCB
        self.m_caption = caption
        self.m_editableInfoLink = None

    def GetDataTypeInteger( self ):
        dataTypeString = self.m_dataDomainCtrl.GetData()
        domainType = self.m_domainTypeCtrl.GetData()
        enumeration = 0

        if domainType == 'Standard' :
            enumeration = acm.FEnumeration['enum(B92StandardType)']
        elif domainType == 'Enum' :
            enumeration = acm.FEnumeration['enum(B92EnumType)']
        elif domainType == 'RecordRef' :
            enumeration = acm.FEnumeration['enum(B92RecordType)']

        return enumeration.Enumeration(dataTypeString) if enumeration else 0
        

    def HandleApply( self ):
        name = self.m_nameCtrl.GetData()

        if self.m_validateNameCB and not self.m_validateNameCB(name, self.m_columnSpecification) :
            self.m_nameCtrl.SetFocus()
            self.m_nameCtrl.SetTextSelection(0, -1)
            return None

        if not self.m_columnSpecification :
            self.m_columnSpecification = acm.FHierarchyColumnSpecification()

        self.m_columnSpecification.Name(name)
        self.m_columnSpecification.Description(self.m_descriptionCtrl.GetData())
        self.m_columnSpecification.Restriction(self.m_restrictionsCtrl.GetData())
        self.m_columnSpecification.Mandatory(self.m_mandatoryCtrl.Checked())
        self.m_columnSpecification.UniqueValues(self.m_uniqueValuesCtrl.Checked())
        self.m_columnSpecification.DataTypeGroup(self.m_domainTypeCtrl.GetData())
        self.m_columnSpecification.DataTypeType(self.GetDataTypeInteger())

        category = self.m_columnCategory.GetData()
        self.m_columnSpecification.ColumnCategory(category if category else None)

        if self.m_dataTypeInfoCtrl.Visible() :
            self.m_columnSpecification.DataTypeInfo(self.m_dataTypeInfoCtrl.GetData())


        return True

    def UpdateControlsValues(self) :
        if self.m_columnSpecification:
            self.m_nameCtrl.SetData(self.m_columnSpecification.Name())
            self.m_descriptionCtrl.SetData(self.m_columnSpecification.Description())
            self.m_restrictionsCtrl.SetData(self.m_columnSpecification.Restriction())
            self.m_mandatoryCtrl.Checked(self.m_columnSpecification.Mandatory())
            self.m_uniqueValuesCtrl.Checked(self.m_columnSpecification.UniqueValues())

            self.m_columnCategory.SetData(self.m_columnSpecification.ColumnCategory())

            typeGroup = self.m_columnSpecification.DataTypeGroup()
            self.m_domainTypeCtrl.SetData(typeGroup)
            self.PopulateDomains()
            
            enumName = HierarchyEditorUtils.GetEnumValueAsString(typeGroup, self.m_columnSpecification.DataTypeType())
            self.m_dataDomainCtrl.SetData(enumName)

            if enumName == 'ChoiceList' :
                self.m_dataTypeInfoCtrl.Visible(True)
                self.PopulateChoiceList()
                self.m_dataTypeInfoCtrl.SetData(self.m_columnSpecification.DataTypeInfo())
                self.m_dataTypeInfoCtrl.ToolTip('The data type info for the column')



    def OnEditChanged(self, ud, cd):
        self.UpdateControls()

    def UpdateControls(self) :
        enableOk = False
        if self.m_nameCtrl.GetData():
            enableOk = True

        self.m_okButton.Enabled(enableOk)

        dataDomain = self.m_dataDomainCtrl.GetData()

        if dataDomain == 'ChoiceList' :
            self.m_dataTypeInfoCtrl.Visible(True)
            self.PopulateChoiceList()
        else:
            self.m_dataTypeInfoCtrl.Visible(False)

    def OnDataDomainComboChanged(self, ud, cd) :
        self.UpdateControls()

    def OnDomainTypeComboChanged(self, ud, cd) :
        self.PopulateDomains()

    def OnNameCtrlChanged(self, ud, cd) :
        self.UpdateControls()

    def OnEditableLinkCtrlClicked(self, ud, cd) :
        if self.m_columnSpecification :
            OpenHierarchyDialog.Show(self.m_fuxDlg.Shell(), 'Existing Hierarchies', False, self.m_columnSpecification.HierarchyType().Name())

    def InitDomainTypes(self):
        self.m_domainTypes['Standard'] = self.m_standardDomains
        self.m_domainTypes['Enum'] = self.m_enumDomains
        self.m_domainTypes['RecordRef'] = self.m_refsDomains

    def PopulateDomainTypes(self):

        for type in list(self.m_domainTypes.keys()) :
            self.m_domainTypeCtrl.AddItem(type)

        self.m_domainTypeCtrl.SetData('Standard')

    def PopulateDomains(self) :
        domainType = self.m_domainTypeCtrl.GetData()

        domains = self.m_domainTypes[domainType]
        self.m_dataDomainCtrl.Clear()

        first = None
        for domain in domains :
            self.m_dataDomainCtrl.AddItem(domain)

            if not first :
                first = domain

        self.m_dataDomainCtrl.SetData(first)


    def PopulateChoiceList(self) :
        if not self.m_choiceListsPopulated :
            master = acm.FChoiceList['MASTER']

            choiceLists = master.Choices()
            choiceLists = choiceLists.SortByProperty('StringKey')
            first = None
            for choiceList in choiceLists :
                if choiceList.StringKey() not in ['MASTER', 'ADM Choicelist Mappings'] :
                    self.m_dataTypeInfoCtrl.AddItem(choiceList)
                    if not first:
                        first = choiceList

            if first:
                self.m_dataTypeInfoCtrl.SetData(first)

            self.m_choiceListsPopulated = True

    def HandleCreate( self, dlg, layout):
        self.InitDomainTypes()

        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)
        self.m_okButton = layout.GetControl('ok')

        self.m_nameCtrl = layout.GetControl('nameCtrl')
        self.m_domainTypeCtrl = layout.GetControl('domainType')
        self.m_dataDomainCtrl = layout.GetControl('dataDomain')
        self.m_dataTypeInfoCtrl = layout.GetControl('dataTypeInfo')
        self.m_descriptionCtrl = layout.GetControl('descriptionCtrl')
        self.m_restrictionsCtrl= layout.GetControl('restrictionCombo')
        self.m_columnCategory = layout.GetControl('columnCategoryCombo')
        self.m_mandatoryCtrl = layout.GetControl('mandatoryCheckbox')
        self.m_uniqueValuesCtrl = layout.GetControl('uniqueValues')
        self.m_editableInfoLink = layout.GetControl('editableInfo')

        self.m_nameCtrl.ToolTip('The name of the column')
        self.m_domainTypeCtrl.ToolTip('The domain type of the column')
        self.m_dataDomainCtrl.ToolTip('The data domain of the column')
        self.m_dataTypeInfoCtrl.ToolTip('The data type info for the column')
        self.m_descriptionCtrl.ToolTip('The description of the column')
        self.m_restrictionsCtrl.ToolTip('Restriction on the column values, it can only be added as a leaf or group depending on the restriction')
        self.m_columnCategory.ToolTip('The category of the column, defined by the Hierarchy Column Category choice list')
        self.m_mandatoryCtrl.ToolTip('')
        self.m_uniqueValuesCtrl.ToolTip('The value in the column needs to be unique in regards to other values in the hierarchy')
        self.m_editableInfoLink.ToolTip('')


        self.m_mandatoryCtrl.Visible(False)
        
        for restriction in self.m_columnSpecificationRestriction :
            self.m_restrictionsCtrl.AddItem(restriction)

        self.m_restrictionsCtrl.SetData('None')

        choiceList = acm.FChoiceList.Select('name="Hierarchy Column Category" and list="MASTER"')

        if choiceList :
            choiceList = choiceList[0]
            choices = choiceList.ChoicesSorted()
            if choices:
                self.m_columnCategory.AddItem('')
                for choice in choices :
                    self.m_columnCategory.AddItem(choice)

        self.PopulateDomainTypes()
        self.PopulateDomains()

        if self.m_columnSpecification :
            hierarchies = self.m_columnSpecification.HierarchyType().Hierarchies()

            if hierarchies :
                self.m_domainTypeCtrl.Enabled(False)
                self.m_dataDomainCtrl.Enabled(False)
                self.m_dataTypeInfoCtrl.Enabled(False)
                self.m_restrictionsCtrl.Enabled(False)
                self.m_mandatoryCtrl.Enabled(False)
                self.m_uniqueValuesCtrl.Enabled(False)
                self.m_editableInfoLink.SetData('References to the column definition exists so changes are limited')
            else:
                self.m_editableInfoLink.Visible(False)
                

        self.m_editableInfoLink.AddCallback('Activate', self.OnEditableLinkCtrlClicked, self)
        self.m_nameCtrl.AddCallback('Changed', self.OnNameCtrlChanged, self)
        self.m_domainTypeCtrl.AddCallback('Changed', self.OnDomainTypeComboChanged, self)
        self.m_dataDomainCtrl.AddCallback('Changed', self.OnDataDomainComboChanged, self)
        self.m_nameCtrl.SetData(self.m_initialText)

        self.UpdateControlsValues()
        self.UpdateControls()

        self.m_nameCtrl.SetFocus()
        self.m_nameCtrl.SetTextSelection(0, -1)


    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  AddHyperLink('editableInfo')
        b.  AddInput('nameCtrl', 'Name', 40)
        b.  AddOption('domainType', 'Domain Type')
        b.  AddOption('dataDomain', 'Domain')
        b.  AddOption('dataTypeInfo', 'Data Type Info')
        b.  AddInput('descriptionCtrl', 'Description')
        b.  AddSpace(10)
        b.  BeginVertBox()
        b.      AddOption('restrictionCombo', 'Restrictions')
        b.      AddOption('columnCategoryCombo', 'Category')
        b.      AddCheckbox('mandatoryCheckbox', 'Mandatory')
        b.      AddCheckbox('uniqueValues', 'Unique Values')
        b.  EndBox() 
        b.  AddSpace(10)
        b.  BeginHorzBox()
        b.          AddFill()
        b.          AddButton('ok', 'OK')
        b.          AddButton('cancel', 'Cancel')
        b.  EndBox() 
        b.EndBox()
        return b
