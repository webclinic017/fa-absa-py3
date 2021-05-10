import acm
import FUxCore
import RiskFactorNewAttributeDialog


def Show(shell, caption, riskFactorSetup, addInfoRecType) :
    dlg = RiskFactorSelectPropertySpecDialog(caption, riskFactorSetup, addInfoRecType)

    return acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg) 

class RiskFactorSelectPropertySpecDialog( FUxCore.LayoutDialog ):
    
    def __init__(self, name, riskFactorSetup, addInfoRecType):
        self.m_name = name
        self.m_addInfoSpecList = None
        self.m_riskFactorSetup = riskFactorSetup
        self.m_addInfoRectType = addInfoRecType
        self.m_newButton = None
        self.m_editButton = None
        self.m_removeButton = None

    def CreateToolTip(self):
        pass
        
    def HandleCreate( self, dlg, layout ):
        self.m_fuxDlg = dlg
        if self.m_name:
            self.m_fuxDlg.Caption( self.m_name )

        self.m_addInfoSpecList = layout.GetControl('addInfoSpecList')
        self.m_addInfoSpecList.AddColumn('Name')
        self.m_addInfoSpecList.AddColumn('Description')

        self.m_addInfoSpecList.ShowColumnHeaders(True)
        self.m_addInfoSpecList.ShowCheckboxes(True)

        self.m_addInfoSpecList.AddCallback('SelectionChanged', self.OnSelectionChanged, None)


        self.m_newButton = layout.GetControl('newButton')
        self.m_newButton.AddCallback('Activate', self.OnNewButton, None)

        self.m_editButton = layout.GetControl('editButton')
        self.m_editButton.AddCallback('Activate', self.OnEditButton, None)

        self.m_removeButton = layout.GetControl('removeButton')
        self.m_removeButton.AddCallback('Activate', self.OnRemoveButton, None)

        self.Populate()
        self.UpdateControls()

    def Populate(self, selection = None) :
        self.m_addInfoSpecList.Clear()

        addInfoSpecs = acm.FAdditionalInfoSpec.Select('recType=' + self.m_addInfoRectType)
        usedFieldNames = [x.AdditionalInfoSpec().FieldName() for x in self.m_riskFactorSetup.RiskFactorPropertySpecifications()]

        root = self.m_addInfoSpecList.GetRootItem()
        for addInfoSpec in addInfoSpecs:
            child = root.AddChild()
            child.Label(addInfoSpec.FieldName(), 0)
            child.Label(addInfoSpec.Description(), 1)
            child.SetData(addInfoSpec)
            child.Icon('AddInfo')

            if addInfoSpec.FieldName() in usedFieldNames or addInfoSpec.Mandatory():
                child.Check(True)

            if addInfoSpec == selection:
                child.Select(True)

        for column in range(0, self.m_addInfoSpecList.ColumnCount()) :
            self.m_addInfoSpecList.AdjustColumnWidthToFitItems(column)

    def OnSelectionChanged(self, cd, ud) :
        self.UpdateControls()

    def UpdateControls(self) :
        item = self.m_addInfoSpecList.GetSelectedItem()

        self.m_editButton.Enabled(item != None)
        self.m_removeButton.Enabled(item != None)

    def OnNewButton(self, cd, ud) :
        caption = 'New Risk Factor Collection Attribute' if self.m_addInfoRectType == 'RiskFactorCollection' else 'New Risk Factors Attribute'
        addInfoSpec = RiskFactorNewAttributeDialog.Show(self.m_fuxDlg.Shell(), caption, self.m_addInfoRectType, None) 
        if addInfoSpec :
            self.Populate(addInfoSpec)

    def OnRemoveButton(self, cd, ud) :
        item = self.m_addInfoSpecList.GetSelectedItem()

        if item :
            try :
                addInfoSpec = item.GetData()
                addInfoSpec.Delete()
                item.Remove()
            except RuntimeError as e:
                acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'Unable to delete attribute specification: ' + e.message)


    def OnEditButton(self, cd, ud) :
        item = self.m_addInfoSpecList.GetSelectedItem()

        if item :
            caption = 'Edit Risk Factor Collection Attribute' if self.m_addInfoRectType == 'RiskFactorCollection' else 'New Risk Factors Attribute'
            addInfoSpec = RiskFactorNewAttributeDialog.Show(self.m_fuxDlg.Shell(), caption, self.m_addInfoRectType, item.GetData()) 
            if addInfoSpec :
                self.Populate(addInfoSpec)

    def HandleApply(self):
        addInfoSpecs = []

        addInfoSpecListItems = self.m_addInfoSpecList.GetCheckedItems()
    
        for addInfoSpecListItem in addInfoSpecListItems :
            addInfoSpecs.append(addInfoSpecListItem.GetData())

        return addInfoSpecs
        
            
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddList('addInfoSpecList', 6, -1, 60)
        b.  BeginHorzBox()
        b.      AddFill()
        b.      AddButton('newButton', 'New...')
        b.      AddButton('editButton', 'Edit...')
        b.      AddButton('removeButton', 'Delete')
        b.  EndBox()
        b.  AddSpace(10)
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b
