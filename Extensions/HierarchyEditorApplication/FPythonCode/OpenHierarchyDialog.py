import acm
import FUxCore
import fnmatch
import unicodedata

def caseless_equal(left, right):
    return left.lower() == right.lower()


def Show(shell, caption, openDialog, initialHierarchyType = None):
    customDlg = OpenHierarchyDialog(openDialog, initialHierarchyType)
    customDlg.m_caption = caption

    builder = customDlg.CreateLayout()
    
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )
    
    return customDlg.m_selectedHierarchy


    
class OpenHierarchyDialog (FUxCore.LayoutDialog):
    def __init__(self, openDialog, initialHierarchyType = None):
        self.m_okButton = 0
        self.m_openDialog = openDialog
        self.m_initialHierarchyType = initialHierarchyType
        self.m_hierarchies = None
        self.m_hierarchyList = None
        self.m_nameInput = None
        self.m_hierarchyTypeOption = None
        self.m_selectedHierarchy = None
        self.m_allTypesSymbol =  'All Types'       
        self.m_ignoreInputChanged = False

    def GetSelectedHierarchy(self) :
        selectedHierrachy = None
        selectedHierarchyName = self.m_nameInput.GetData()

        for hierarchy in self.m_hierarchies :
            hierarchyName = hierarchy.Name()

            if caseless_equal(hierarchyName, selectedHierarchyName) :
                selectedHierrachy = hierarchy
                break

        return selectedHierrachy


    def HandleApply( self ):
        self.m_selectedHierarchy = self.GetSelectedHierarchy()

        return True

    def HandleCancel(self):
        self.m_selectedHierarchy = None

        return True

    def OnInputChanged(self, ud, cd):
        if not self.m_ignoreInputChanged:
            self.Populate(False)
            self.UpdateControls()

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)
        self.m_okButton = layout.GetControl('ok')


        self.m_hierarchyList = layout.GetControl('hierarchyList')

        self.m_nameInput = layout.GetControl('nameInput')
        self.m_nameInput.AddCallback('Changed', self.OnInputChanged, self)
        self.m_nameInput.SetFocus()

        self.m_hierarchyList.AddColumn('Name')
        self.m_hierarchyList.AddColumn('Type')
        self.m_hierarchyList.ShowColumnHeaders(True)
        self.m_hierarchyList.AddCallback('SelectionChanged', self.OnHierarchyListChanged, self)
        self.m_hierarchyList.AddCallback('DefaultAction', self.OnHierarchySelected, self)
        self.m_hierarchyList.AddCallback('ContextMenu', self.OnHierarchyListContextMenu, self )

        self.m_hierarchyTypeOption = layout.GetControl('hierarchyTypeOption')
        self.m_hierarchyTypeOption.AddCallback('Changed', self.OnInputChanged, self)

        self.m_hierarchies = acm.FHierarchy.Select('').SortByProperty('Name')

        self.Populate(True)

        if not self.m_openDialog :
            self.m_okButton.Visible(False)
            self.m_nameInput.Visible(False)
            self.m_hierarchyTypeOption.Enabled(False)

        self.UpdateControls()

    def IsHierarchyVisible(self, hierarchyName, hierarchyTypeName, currentHierarchyName, currentHierarchyType) :
        visible = False

        if currentHierarchyType == self.m_allTypesSymbol or hierarchyTypeName == currentHierarchyType :
            visible = True

        if visible and currentHierarchyName:
            currentHierarchyName = currentHierarchyName + '*'
            
            visible = fnmatch.fnmatch(hierarchyName, currentHierarchyName)            

        return visible

    def OnHierarchyListContextMenu(self, ud, cd) :
        menuBuilder = cd.At('menuBuilder')
        item = self.m_hierarchyList.GetSelectedItem()
        if item :
            obj = item.GetData()
            acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, [obj], False, None, None)

    def Populate(self, populateTypes) :
        hierarchyTypes = set()


        self.m_hierarchyList.RemoveAllItems()
        root = self.m_hierarchyList.GetRootItem()

        currentHierarchyType = self.m_allTypesSymbol
        currentHierarchyName = self.m_nameInput.GetData()

        if not populateTypes :
            currentHierarchyType = self.m_hierarchyTypeOption.GetData()
        elif self.m_initialHierarchyType :
            currentHierarchyType = self.m_initialHierarchyType


        for hierarchy in self.m_hierarchies :
            hierarchyName = hierarchy.Name()
            hierarchyTypeName = hierarchy.HierarchyType().Name()

            if self.IsHierarchyVisible(hierarchyName, hierarchyTypeName, currentHierarchyName, currentHierarchyType) :
                child = root.AddChild()
                child.Icon('Tree')
                child.Label(hierarchyName, 0)
                child.Label(hierarchyTypeName, 1)
                child.SetData(hierarchy)

            hierarchyTypes.add(hierarchyTypeName)

        if populateTypes :
            self.m_hierarchyTypeOption.AddItem(self.m_allTypesSymbol)
            for hierarchyType in sorted(hierarchyTypes) :
                self.m_hierarchyTypeOption.AddItem(hierarchyType)

            if self.m_initialHierarchyType :
                self.m_hierarchyTypeOption.SetData(self.m_initialHierarchyType)
            else :
                self.m_hierarchyTypeOption.SetData(0)

    def OnHierarchyListChanged(self, ud, cd):
        item = self.m_hierarchyList.GetSelectedItem()

        if item :
            self.m_ignoreInputChanged = True
            self.m_selectedHierarchy = item.GetData()
            self.m_nameInput.SetData(self.m_selectedHierarchy.Name())
            self.m_nameInput.SetTextSelection(0, -1)
            self.m_ignoreInputChanged = False

        self.UpdateControls()

    def OnHierarchySelected(self, ud, cd) :
        self.m_fuxDlg.CloseDialogOK()

    def UpdateControls(self):
        item = self.GetSelectedHierarchy()
        self.m_okButton.Enabled(item != None)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox()
        b.  BeginVertBox()
        b.      AddList('hierarchyList', 12, -1, 80)
        b.      AddSpace(5)
        b.      BeginHorzBox()
        b.          BeginVertBox()
        b.              AddInput('nameInput', 'Name')
        b.              AddOption('hierarchyTypeOption', 'Type')
        b.          EndBox()
        b.          BeginVertBox()
        b.              AddButton('ok', 'Open')
        b.              AddButton('cancel', 'Cancel'if self.m_openDialog else 'Close')
        b.          EndBox()
        b.      EndBox()
        b.  EndBox()
        b.EndBox()

        return b

