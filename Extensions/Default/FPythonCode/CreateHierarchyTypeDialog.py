
import acm
import FUxCore
import GetShortNameDialog
import CreateHierarchyColumnSpecificationDialog
import HierarchyEditorUtils

def Show(shell, caption):
    customDlg = CreateHierarchyTypeDialog()
    customDlg.m_caption = caption

    builder = customDlg.CreateLayout()
    
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )
    


    
class CreateHierarchyTypeDialog (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_okButton = 0
        self.m_typesList = None
        self.m_columnsTree = None
        self.m_addTypesButton = None
        self.m_editTypesButton = None
        self.m_removeTypesButton = None
        self.m_moveUpButton = None
        self.m_moveDownButton = None
        self.m_addButton = None
        self.m_editButton = None
        self.m_removeButton = None
        self.m_columnsTreeColumnCount = 0
        self.m_columnDefinitionNames = None
        self.m_columnSpecificationRestriction = acm.FEnumeration['enum(HierarchyColumnRestriction)'].Enumerators()

    def HandleApply( self ):
        return True

    def OnEditChanged(self, ud, cd):
        self.UpdateControls()
        
    def MoveButtonIsEnabled(self, up) :
        enabled = False
        item = self.m_columnsTree.GetSelectedItem()

        if item :
            enabled = item.Sibling(not up) != None

        return enabled

    def UpdateControls(self) :
        self.m_moveDownButton.Enabled(self.MoveButtonIsEnabled(False))
        self.m_moveUpButton.Enabled(self.MoveButtonIsEnabled(True))

        self.m_addButton.Enabled(self.m_typesList.GetSelectedItems().Size() == 1)
        self.m_editButton.Enabled(self.m_columnsTree.GetSelectedItems().Size() == 1)
        self.m_removeButton.Enabled(self.m_columnsTree.GetSelectedItems().Size() > 0)

        self.m_editTypesButton.Enabled(self.m_typesList.GetSelectedItems().Size() == 1)
        self.m_removeTypesButton.Enabled(self.m_typesList.GetSelectedItems().Size() > 0)

    def PopulateTypesList(self) :
        self.m_typesList.RemoveAllItems()
        self.m_typesList.Populate(acm.FHierarchyType.Select('').SortByProperty('Name'))
        children = self.m_typesList.GetRootItem().Children()

        if children :
            children[0].Select(True)

    def UpdateColumnSpecificationListItem(self, listItem, columnSpecification) :
        listItem.Icon('FreezePane', 'FreezePane')
        
        listItem.Label(columnSpecification.Name(), 0)
        listItem.Label(columnSpecification.DataTypeGroup(), 1)
        listItem.Label(HierarchyEditorUtils.GetEnumValueAsString(columnSpecification.DataTypeGroup(), columnSpecification.DataTypeType()), 2)
        listItem.Label(columnSpecification.DataTypeInfo(), 3)
        listItem.Label(columnSpecification.Description(), 4)
        listItem.Label(columnSpecification.Restriction(), 5)
        listItem.Label(HierarchyEditorUtils.BoolToString(columnSpecification.UniqueValues()), 6)
        listItem.Label(columnSpecification.ColumnCategory(), 7)
        #listItem.Label(HierarchyEditorUtils.BoolToString(columnSpecification.Mandatory()), 7)

        listItem.SetData(columnSpecification)

        self.m_columnDefinitionNames.add(columnSpecification.Name())


    def PopulateColumnsTree(self) :
        item = self.m_typesList.GetSelectedItem()
        self.m_columnsTree.RemoveAllItems()
        self.m_columnDefinitionNames = set()
        rootItem = self.m_columnsTree.GetRootItem()

        if item :
            hierarchyType = item.GetData()
            sortedHierarchyColumnSpecifications = hierarchyType.SortedHierarchyColumnSpecifications()
            for columnSpecification in sortedHierarchyColumnSpecifications :
                child = rootItem.AddChild()
                self.UpdateColumnSpecificationListItem(child, columnSpecification)

            #for index in range(0, self.m_columnsTreeColumnCount):
            #    self.m_columnsTree.AdjustColumnWidthToFitItems(index)

    def OnTypesListChanged(self, ud, cd):
        self.PopulateColumnsTree()
        self.UpdateControls()

    def OnColumnsTreeChanged(self, ud, cd ):
        self.UpdateControls()

    def GetHierarhyTypeNames(self):
        names = []
        types = acm.FHierarchyType.Select('')

        for type in types :
            names.append(str(type.Name()))

        return names

    def OnAddTypesButton(self, ud, cd) :
        typeName = GetShortNameDialog.Show(self.m_fuxDlg.Shell(), 'New Hierarchy Type', 'Name', 'New Hierarchy Type', -1, False, self.GetHierarhyTypeNames())

        if typeName:
            hierarchyType = acm.FHierarchyType()
            hierarchyType.Name(typeName)
            if HierarchyEditorUtils.CommitObject(hierarchyType, self.m_fuxDlg.Shell()) :
                child = self.m_typesList.GetRootItem().AddChild()
                child.Label(typeName)
                child.Icon(hierarchyType.Icon())
                child.SetData(hierarchyType)
                child.Select()
                child.EnsureVisible()

    def OnEditTypesButton(self, ud, cd) :
        item = self.m_typesList.GetSelectedItem()

        if item :
            hierarchyType = item.GetData()
            typeName = GetShortNameDialog.Show(self.m_fuxDlg.Shell(), 'New Hierarchy Type', 'Name', str(hierarchyType.Name()), -1, False, self.GetHierarhyTypeNames())
            
            if typeName :
                hierarchyType.Name(typeName)
                if HierarchyEditorUtils.CommitObject(hierarchyType, self.m_fuxDlg.Shell()) :
                    item.Label(typeName)

    def OnRemoveTypesButton(self, ud, cd) :
        item = self.m_typesList.GetSelectedItem()

        if item :
            ret = acm.UX().Dialogs().MessageBoxYesNo(self.m_fuxDlg.Shell(), 'Question', 'Are you sure you want to delete the current hierarchy type?')

            if ret == 'Button1':
                hierarchyType = item.GetData()
                if HierarchyEditorUtils.DeleteObject(hierarchyType, self.m_fuxDlg.Shell()) :
                    item.Remove()
        
    def UpdateColumnSpecification(self, listItem, columnSpecification) :
        typeItem = self.m_typesList.GetSelectedItem()
        hierarchyType = typeItem.GetData()
        columnSpecification.HierarchyType(hierarchyType)

        if HierarchyEditorUtils.CommitObject(columnSpecification, self.m_fuxDlg.Shell()) :
            if not listItem :
                listItem = self.m_columnsTree.GetRootItem().AddChild()

            prevSibling = listItem.Sibling(False)

            if prevSibling :
                columnSpecification.PreviousColumnSpecificationName(prevSibling.GetData().Name())

            self.UpdateColumnSpecificationListItem(listItem, columnSpecification)
            listItem.Select()


    def UpdateColumnSpecificationsOrder(self) :
        acm.BeginTransaction()
        previousColumnSpecificationName = ''
        for item in self.m_columnsTree.GetRootItem().Children() :
            columnSpecification = item.GetData()
            columnSpecification.PreviousColumnSpecificationName(previousColumnSpecificationName)
            previousColumnSpecificationName = columnSpecification.Name()
            columnSpecification.Commit()

        try :
            acm.CommitTransaction()
        except RuntimeException as ex :
            print (ex)    
            acm.AbortTransaction()

        
    def Move(self, up):
        item1 = self.m_columnsTree.GetSelectedItem()
        item2 = item1.Sibling(not up)

        self.m_columnsTree.Swap(item1, item2)

        self.UpdateControls()
        self.UpdateColumnSpecificationsOrder()

    def OnMoveUpButton(self, ud, cd ):
        self.Move(True)

    def OnMoveDownButton(self, ud, cd ):
        self.Move(False)

    def ValidateColumnDefinitionName(self, columnDefinitionName, columnDefinition):
        ret = True
            
        if not columnDefinition or columnDefinition.Name() != columnDefinitionName :
            if columnDefinitionName in self.m_columnDefinitionNames:
                acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'A column definition with the name ' + columnDefinitionName + ' already exist, please select another name')
                ret = False

        return ret         

    def OnAddButton(self, ud, cd) :
        columnSpecification = CreateHierarchyColumnSpecificationDialog.Show(self.m_fuxDlg.Shell(), 'New Hierarchy Column Definition', 'New Column Definition', self.ValidateColumnDefinitionName)

        if columnSpecification :
            self.UpdateColumnSpecification(None, columnSpecification)
            self.UpdateControls()

    def OnEditButton(self, ud, cd) :
        listItem = self.m_columnsTree.GetSelectedItem()

        if listItem :
            columnSpecification = listItem.GetData()
            columnSpecification = CreateHierarchyColumnSpecificationDialog.Show(self.m_fuxDlg.Shell(), 'Edit Hierarchy Column Definition', '', self.ValidateColumnDefinitionName, columnSpecification)

            if columnSpecification :
                self.UpdateColumnSpecification(listItem, columnSpecification)

    def RemoveColumnSpecification(self, columnSpecification, previousColumnSpecification, nextColumnSpecification):
        ret = False

        columnDefinitionName = columnSpecification.Name()
        if HierarchyEditorUtils.DeleteObject(columnSpecification, self.m_fuxDlg.Shell()) :
            ret = True
            self.m_columnDefinitionNames.remove(columnDefinitionName)

            if nextColumnSpecification :
                previousColumnSpecificationName = ''

                if previousColumnSpecification :
                    previousColumnSpecificationName = previousColumnSpecification.Name()
                    
                nextColumnSpecification.PreviousColumnSpecificationName(previousColumnSpecificationName)
                ret = HierarchyEditorUtils.CommitObject(nextColumnSpecification, self.m_fuxDlg.Shell())

        return ret

    def OnRemoveColumnButton(self, ud, cd) :
        item = self.m_columnsTree.GetSelectedItem()

        if item :
            ret = acm.UX().Dialogs().MessageBoxYesNo(self.m_fuxDlg.Shell(), 'Question', 'Are you sure you want to delete the current column definition?')

            if ret == 'Button1':
                prevSibling = item.Sibling(False)
                nextSibling = item.Sibling(True)
                    
                columnSpecification = item.GetData()
                prevColumnSpecification = prevSibling.GetData() if prevSibling else None
                nextColumnSpecification = nextSibling.GetData() if nextSibling else None

                if self.RemoveColumnSpecification(columnSpecification, prevColumnSpecification, nextColumnSpecification) :
                    item.Remove()
                    self.UpdateControls()

    def AddColumnsTreeColumn(self, label) :
        self.m_columnsTree.AddColumn(label, 100)
        self.m_columnsTreeColumnCount = self.m_columnsTreeColumnCount + 1

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)
        self.m_okButton = layout.GetControl('ok')
        self.m_typesList = layout.GetControl('typesList')
        self.m_columnsTree = layout.GetControl('columnsTree')

        self.m_typesList.AddColumn('Hierarchy Type')
        self.m_typesList.ShowColumnHeaders(True)
        self.m_typesList.EnableHeaderSorting()
        self.m_typesList.AddCallback('SelectionChanged', self.OnTypesListChanged, self)

        self.m_columnsTree.ColumnLabel(0, 'Name')

        self.AddColumnsTreeColumn('Domain Type')
        self.AddColumnsTreeColumn('Domain')
        self.AddColumnsTreeColumn('Data Type Info')
        self.AddColumnsTreeColumn('Description')
        self.AddColumnsTreeColumn('Restrictions')
        self.AddColumnsTreeColumn('Unique Values')
        self.AddColumnsTreeColumn('Category')
        #self.m_columnsTree.AddColumn('Mandatory')

        self.m_columnsTree.ColumnWidth(0, 100)
        self.m_columnsTree.ShowHierarchyLines(False)
        self.m_columnsTree.ShowColumnHeaders(True)
        self.m_columnsTree.AddCallback('SelectionChanged', self.OnColumnsTreeChanged, self)
        self.m_columnsTree.AddCallback('DefaultAction', self.OnEditButton, self)

        self.m_addTypesButton = layout.GetControl('addTypesButton')
        self.m_editTypesButton = layout.GetControl('editTypesButton')
        self.m_removeTypesButton = layout.GetControl('removeTypesButton')

        self.m_moveUpButton = layout.GetControl('moveUpButton')
        self.m_moveDownButton = layout.GetControl('moveDownButton')
        self.m_addButton = layout.GetControl('addButton')
        self.m_editButton = layout.GetControl('editButton')
        self.m_removeButton = layout.GetControl('removeButton')

        self.m_addTypesButton.AddCallback('Activate', self.OnAddTypesButton, self)
        self.m_editTypesButton.AddCallback('Activate', self.OnEditTypesButton, self)
        self.m_removeTypesButton.AddCallback('Activate', self.OnRemoveTypesButton, self)

        self.m_moveUpButton.AddCallback('Activate', self.OnMoveUpButton, self)
        self.m_moveDownButton.AddCallback('Activate', self.OnMoveDownButton, self)
        self.m_addButton.AddCallback('Activate', self.OnAddButton, self)
        self.m_editButton.AddCallback('Activate', self.OnEditButton, self)
        self.m_removeButton.AddCallback('Activate', self.OnRemoveColumnButton, self)

        self.PopulateTypesList()
        self.UpdateControls()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginVertBox()
        b.      AddList('typesList', 8, -1, 120)
        b.      BeginHorzBox()
        b.          AddFill()
        b.          AddButton('addTypesButton', 'Add')
        b.          AddButton('editTypesButton', 'Edit')
        b.          AddButton('removeTypesButton', 'Remove')
        b.      EndBox()
        b.  EndBox()
        b.  AddSpace(5)
        b.  BeginVertBox()
        b.      AddTree('columnsTree', -1, 200)
        b.      BeginHorzBox()
        b.          AddFill()
        b.          AddButton('moveUpButton', 'Move Up')
        b.          AddButton('moveDownButton', 'Move Down')
        b.          AddButton('addButton', 'Add')
        b.          AddButton('editButton', 'Edit')
        b.          AddButton('removeButton', 'Remove')
        b.      EndBox()
        b.  EndBox()
        b.  AddSpace(10)
        b.  BeginHorzBox()
        b.          AddFill()
        b.          AddButton('ok', 'Close')
        b.  EndBox()    
        b.EndBox()
        return b
