import acm
import FUxCore
import RiskFactorUtils

def Show(shell, caption, addInfoSpecRecType, addInfoSpec = None):
    customDlg = RiskFactorNewAttributeDialog(addInfoSpecRecType, addInfoSpec)
    customDlg.m_caption = caption
    columnSpecification = None

    builder = customDlg.CreateLayout()
    
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )
    
class RiskFactorNewAttributeDialog (FUxCore.LayoutDialog):
    def __init__(self, addInfoSpecRecType, addInfoSpec):
        self.m_okButton = 0
        self.m_nameCtrl = None
        self.m_dataDomainCtrl = None
        self.m_dataTypeInfoCtrl = None
        self.m_descriptionCtrl = None
        self.m_mandatoryCtrl = None
        self.m_domainTypeCtrl = None
        self.m_addInfoSpec = addInfoSpec
        self.m_domainTypes = {}
        self.m_standardDomains = acm.FEnumeration['enum(B92StandardType)'].EnumeratorStringsSkipFirst().Sort()
        self.m_enumDomains = acm.FEnumeration['enum(B92EnumType)'].EnumeratorStringsSkipFirst().Sort()
        self.m_refsDomains = acm.FEnumeration['enum(B92RecordType)'].EnumeratorStringsSkipFirst().Sort()
        self.m_choiceListsPopulated = False
        self.m_addInfoSpecRecType = addInfoSpecRecType

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
        addInfoSpec = self.m_addInfoSpec

        if not addInfoSpec :
            addInfoSpec = acm.FAdditionalInfoSpec()
        
        addInfoSpec.Name(self.m_nameCtrl.GetData())
        addInfoSpec.Description(self.m_descriptionCtrl.GetData())
        addInfoSpec.Mandatory(self.m_mandatoryCtrl.Checked())
        addInfoSpec.DataTypeGroup(self.m_domainTypeCtrl.GetData())
        addInfoSpec.DataTypeType(self.GetDataTypeInteger())
        addInfoSpec.RecType(self.m_addInfoSpecRecType)
        if self.m_dataTypeInfoCtrl.Visible() :
            addInfoSpec.Description(self.m_dataTypeInfoCtrl.GetData())        

        try :
            addInfoSpec.Commit()
        except RuntimeError as e:
            addInfoSpec = None
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'Unable to commit the attribute specification: ' + e.message)
            

        return addInfoSpec

    def UpdateControlsValues(self) :
        if self.m_addInfoSpec:
            self.m_nameCtrl.SetData(self.m_addInfoSpec.FieldName())
            self.m_descriptionCtrl.SetData(self.m_addInfoSpec.Description())
            self.m_mandatoryCtrl.Checked(self.m_addInfoSpec.Mandatory())

            typeGroup = self.m_addInfoSpec.DataTypeGroup()
            self.m_domainTypeCtrl.SetData(typeGroup)
            self.PopulateDomains()
            
            enumName = RiskFactorUtils.GetEnumValueAsString(typeGroup, self.m_addInfoSpec.DataTypeType())
            self.m_dataDomainCtrl.SetData(enumName)

            if enumName == 'ChoiceList' :
                self.m_dataTypeInfoCtrl.Visible(True)
                self.PopulateChoiceList()
                self.m_dataTypeInfoCtrl.SetData(self.m_addInfoSpec.Description())
                self.m_descriptionCtrl.Visible(False)


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
            self.m_descriptionCtrl.Visible(False)
            self.PopulateChoiceList()
        else:
            self.m_dataTypeInfoCtrl.Visible(False)
            self.m_descriptionCtrl.Visible(True)

    def OnDataDomainComboChanged(self, ud, cd) :
        self.UpdateControls()

    def OnDomainTypeComboChanged(self, ud, cd) :
        self.PopulateDomains()

    def OnNameCtrlChanged(self, ud, cd) :
        self.UpdateControls()

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
        self.m_mandatoryCtrl = layout.GetControl('mandatoryCheckbox')

        self.m_mandatoryCtrl.Visible(False)

        if self.m_addInfoSpec :
            self.m_nameCtrl.SetData(self.m_addInfoSpec.FieldName())
            self.m_nameCtrl.SetTextSelection(0, -1)

        self.PopulateDomainTypes()
        self.PopulateDomains()

        self.m_nameCtrl.AddCallback('Changed', self.OnNameCtrlChanged, self)
        self.m_domainTypeCtrl.AddCallback('Changed', self.OnDomainTypeComboChanged, self)
        self.m_dataDomainCtrl.AddCallback('Changed', self.OnDataDomainComboChanged, self)

        self.UpdateControlsValues()
        self.UpdateControls()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  AddInput('nameCtrl', 'Name', 40)
        b.  AddInput('descriptionCtrl', 'Description')
        b.  AddOption('domainType', 'Domain Type')
        b.  AddOption('dataDomain', 'Domain')
        b.  AddOption('dataTypeInfo', 'Data Type Info')
        b.  AddSpace(10)
        b.  BeginVertBox()
        b.      AddCheckbox('mandatoryCheckbox', 'Mandatory')
        b.  EndBox() 
        b.  AddSpace(10)
        b.  BeginHorzBox()
        b.          AddFill()
        b.          AddButton('ok', 'Ok')
        b.          AddButton('cancel', 'Cancel')
        b.  EndBox() 
        b.EndBox()
        return b
