""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCorporateActionTreePanel.py"
import acm
import FUxCore
from FPanel import Panel
from FEvent import EventCallback
from FCorpActionsWorkbenchLogger import logger
from FCorporateActionsWorkbenchEvent import OnCorporateActionSelected
from FCorporateActionsWorkbenchEvent import OnCorporateAction
from FCorporateActionsWorkbenchEvent import OnCorporateActionChoice
from FCorporateActionsWorkbenchEvent import OnCorporateActionPayout
from FCorporateActionsWorkbenchEvent import OnTreeItemSelected
from FCorporateActionsWorkbenchMenuItem import CreateNewCorporateActionChoiceFromTreeViewMenuItem
from FCorporateActionsWorkbenchMenuItem import CreateNewCorporateActionPayoutFromTreeViewMenuItem



class CorporateActionTreePanel(Panel):

    def __init__(self):
        super(CorporateActionTreePanel, self).__init__()
        self._treeCtrl = None
        self._selectedActions = []

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('Invisible')
        b.  AddSpace(2)
        b.  AddTree('treeCtrl', width=200, height=70)
        b.EndBox()
        return b

    @EventCallback
    def OnCorporateActionSelected(self, event):
        self._selectedActions[:] = []
        
        for rowObject in event.Objects():
            self._selectedActions.append(rowObject)
        self.PopulateCorporateActionsTreeView(self._selectedActions)

    @EventCallback
    def OnCorporateAction(self, event):
        self.PopulateCorporateActionsTreeView(self._selectedActions)

    @EventCallback
    def OnCorporateActionChoice(self, event):
        self.PopulateCorporateActionsTreeView(self._selectedActions)

    @EventCallback
    def OnCorporateActionPayout(self, event):
        self.PopulateCorporateActionsTreeView(self._selectedActions)

    def PopulateCorporateActionsTreeView(self, corpActs):
        treeRoot = self._treeCtrl.GetRootItem()
        caItems = [caItem for caItem in treeRoot.Children()]
        caInTree = [caItem.GetData() for caItem in caItems]
        
        removed = list(set(caInTree) - set(corpActs))
        for child in removed:
            index = caInTree.index(child)
            caItems[index].Remove()

        if corpActs and len(corpActs):
            for ca in corpActs:
                if ca in caInTree:
                    index = caInTree.index(ca)
                    self.AddItem(ca, caItems[index])
                    self.RefreshSubTree(caItems[index], 'CaChoices', 'CaPayouts')
                else:
                    treeCA = treeRoot.AddChild()
                    self.AddItem(ca, treeCA)
                    self.RefreshSubTree(treeCA, 'CaChoices', 'CaPayouts')
        self._treeCtrl.ForceRedraw()


    def RefreshSubTree(self, parentItem, childrenFuncName, grandChildrenFuncName):

        parent = parentItem.GetData()
        children = getattr(parent, childrenFuncName)().SortByProperty('Oid')
        children = [c for c in children]
        childrenItems = [item for item in parentItem.Children()]
        childrenInTreeView = [item.GetData() for item in childrenItems]

        removed = list(set(childrenInTreeView) - set(children))
        for child in removed:
            index = childrenInTreeView.index(child)
            childrenItems[index].Remove()
        
        for child in children:
            if child in childrenInTreeView:
                index = childrenInTreeView.index(child)
                self.AddItem(child, childrenItems[index])
                if child.IsKindOf(acm.FCorporateActionChoice):
                    self.RefreshSubTree(childrenItems[index], 'CaPayouts', None)
            else:
                childItem = self.AddChild(child, parentItem)
                if grandChildrenFuncName:
                    grandChildren = getattr(child, grandChildrenFuncName)().SortByProperty('Oid')
                    for grandChild in grandChildren:
                        self.AddChild(grandChild, childItem)


    def AddChild(self, child, item):
        treeChild = item.AddChild()
        return self.AddItem(child, treeChild)

    def treeItemLabel(self, acmObj):
        if acmObj.IsKindOf(acm.FCorporateActionPayout):
            if acmObj.Name() == '':
                return 'Payout ' + str(acmObj.Oid())
        return acmObj.Name()

    def AddItem(self, acmObj, item):
        label = self.treeItemLabel(acmObj)
        item.Label(label)
        if acmObj.IsKindOf(acm.FCorporateAction):
            item.Icon('Tree+GreenPlusOverlay', 'Tree+GreenPlusOverlay')
        elif acmObj.IsKindOf(acm.FCorporateActionChoice):
            item.Icon('Tree+ExportOverlay', 'Tree+ExportOverlay')
        elif acmObj.IsKindOf(acm.FCorporateActionPayout):
            item.Icon('PayGoodValue', 'PayGoodValue')
        item.SetData(acmObj)
        return item

    def InitControls(self, layout):
        self.InitTreeControl(layout)

    def InitTreeControl(self, layout):
        self._treeCtrl = layout.GetControl('treeCtrl')
        self._treeCtrl.AddCallback('SelectionChanged', self.OnSelectionChanged, None)
        self._treeCtrl.AddCallback('ContextMenu', self.OnTreeContextMenu, None)
        self._treeCtrl.AddCallback('DefaultAction', self.OnDoubleClicked, None)

    def OnSelectionChanged(self, *args):
        if self._treeCtrl.GetSelectedItem() and self._treeCtrl.GetSelectedItem().GetData():
            selectedObject = self._treeCtrl.GetSelectedItem().GetData()
            self.SendEvent(OnTreeItemSelected(self, [selectedObject]))

    def OnTreeContextMenu(self, *args):
        selectedItems = args[1].At('items')
        menuBuilder = args[1].At('menuBuilder')
        objects = [item.GetData() for item in selectedItems]
        self.SendEvent(OnTreeItemSelected(self, [objects[0]]))
        acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, objects, True, self.AddCustomContextItemsCB, None)

    def CreateCommandAddChoiceCB(self):
        return CreateNewCorporateActionChoiceFromTreeViewMenuItem(self.Owner())

    def CreateCommandAddPayoutCB(self):
        return CreateNewCorporateActionPayoutFromTreeViewMenuItem(self.Owner())

    def AddCustomContextItemsCB(self, *args):
        menuBuilder = args[1].At('menuBuilder')
        commands = acm.FArray()
        selectedObject = self._treeCtrl.GetSelectedItem().GetData()
        if selectedObject.IsKindOf(acm.FCorporateAction):
            commands.Add(['newCorporateActionChoiceFromTreeView', '', 'Add Choice', '', '', '',
                        self.CreateCommandAddChoiceCB, False])
        elif selectedObject.IsKindOf(acm.FCorporateActionChoice):
            commands.Add(['newCorporateActionPayoutFromTreeView', '', 'Add Payout', '', '', '',
                        self.CreateCommandAddPayoutCB, False])
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))

    def OnDoubleClicked(self, *args):
        selectedObject = self._treeCtrl.GetSelectedItem().GetData()
        self.SendEvent(OnTreeItemSelected(self, [selectedObject]))
        acm.StartRunScript(selectedObject, 'Modify')
