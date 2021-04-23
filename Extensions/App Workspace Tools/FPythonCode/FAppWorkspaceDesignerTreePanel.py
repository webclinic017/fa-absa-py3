""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/AppWorkspaceTools/etc/FAppWorkspaceDesignerTreePanel.py"
""" Compiled: 2018-06-07 17:06:19 """

#__src_file__ = "extensions/AppWorkspaceTools/etc/FAppWorkspaceDesignerTreePanel.py"
import acm
import FUxCore
import FAppWorkspaceDesignerNodes as Nodes
import Contracts_AppConfig_Messages_AppWorkspace as AppWorkspace
from contextlib import contextmanager
import GetShortNameDialog
import FAppWorkspaceDesignerMenuItems as MenuItems

class TreeMenuPanel(FUxCore.LayoutPanel):
    __name__ = 'treeMenu'
    
    def __init__(self, parent):
        self.parent = parent
        self.tree = None
        self.name = None
        self._forceRedrawCount = 0

    # Node is a TabContent
    def GetSerializedContent(self, node):
        return node.GetData().contents.SerializeToString()
        
    # Node is a TabContent
    def GetSerializedSettings(self, node):
        return node.GetData().userSettings.SerializeToString()
        
    def CopyDashboardViewName(self, tabNode):
        if isinstance(tabNode.GetData(), Nodes.DashboardTabNode):
            parts = tabNode.GetData().contents.parts
            for i, part in enumerate(parts):
                tabNode.GetData().userSettings.partSettings[i].viewName = part.view.viewName
        
    def SerializedTopNode(self):
        topNode = self.tree.GetFirstItem()
        data = topNode.GetData()
        for i, child in enumerate(topNode.Children()):
            self.CopyDashboardViewName(child)
            data.contents.tabs[i].contents = self.GetSerializedContent(child)
            data.contents.tabs[i].userSettings = self.GetSerializedSettings(child)
        return data.contents.SerializeToString()

    @FUxCore.aux_cb
    def OnTreeSelectionChanged(self, *args):
        if len(args) > 0:
            focus = args[1]
            if focus:
                newNode = self.tree.GetSelectedItem()
                nodeData = newNode.GetData()
                nodeData.OnSelection(self)
    
    @FUxCore.aux_cb
    def TreeContextMenuCB(self, ud, cd):            
        builder = cd.At('menuBuilder')
        objects = cd.At('items')
        nodeData = objects[0].GetData()
        nodeData.OnSelection(self)
        acm.UX().Menu().BuildStandardObjectContextMenu(builder, None, False, self.ContextMenuCb, None)
    
    def ContextMenuCb(self, ud, cd):
        commands = self.CustomCommands(False)
        menuBuilder = cd.At('menuBuilder')
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))
    
    def CustomCommands(self, isRibbonCommand):
        def AddWorkbenchTabCB():
            return MenuItems.AddWorkbenchTab(self, isRibbonCommand)
        def AddDashboardTabCB():
            return MenuItems.AddDashboardTab(self, isRibbonCommand)
        def AddPartCB():
            return MenuItems.AddPart(self, isRibbonCommand)
        def RemoveNodeCB():
            return MenuItems.RemoveNode(self, isRibbonCommand)
        def AddButtonsCB():
            return MenuItems.AddButtons(self, isRibbonCommand)
        def MoveNodeUpCB():
            return MenuItems.MoveNode(self, False, isRibbonCommand)
        def MoveNodeDownCB():
            return MenuItems.MoveNode(self, True, isRibbonCommand)
        
        return [
        ['addWorkbenchTab', 'View', 'Add Workbench Tab', '', '', '', AddWorkbenchTabCB, False],
        ['addDashboardTab', 'View', 'Add Dashboard Tab', '', '', '', AddDashboardTabCB, False],
        ['addPart', 'View', 'Add Part', '', '', '', AddPartCB, False],
        ['addButtons', 'View', 'Add Buttons', '', '', '', AddButtonsCB, False],
        ['moveNodeUp', 'View', 'Move Up', '', '', '', MoveNodeUpCB, False],
        ['moveNodeDown', 'View', 'Move Down', '', '', '', MoveNodeDownCB, False],
        ['removeNode', 'View', 'Remove', '', '', '', RemoveNodeCB, False],
        ]
    
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('None')
        b. AddTree('tree', 200, 500)
        b.EndBox()
        return b

    def Shell(self):
        return self.parent.Shell()
    
    def AddNewDashboardTab(self, node):
        newCaption = GetShortNameDialog.Show(self.Shell(), 'Add New Dashboard Tab', 'Caption', '')
        if newCaption:
            with self.ForceRedraw():
                tabData = node.GetData().contents.tabs.add()
                tabData.tabType = 'dashboard'
                tabData.caption = newCaption
                tabData.iconName = 'SessionMgr'
                newNode = self.AddDashboardTab(node, tabData)
                self.AfterNodeAdd(newNode)
        
    def AddDashboardTab(self, node, tabContent):
        data = Nodes.DashboardTabNode(tabContent)
        newNode = self.AddChildNode(node, data)
        self.AddDashboardParts(newNode)
        return newNode
        
    def AddNewWorkbenchTab(self, node):
        newCaption = GetShortNameDialog.Show(self.Shell(), 'Add New Workbench Tab', 'Caption', '')
        if newCaption:
            with self.ForceRedraw():
                tabData = node.GetData().contents.tabs.add()
                tabData.tabType = 'workbench'
                tabData.caption = newCaption
                tabData.iconName = 'EmptySheet'
                newNode = self.AddWorkbenchTab(node, tabData)
                self.AfterNodeAdd(newNode)
        
    def AddWorkbenchTab(self, node, tabData):
        data = Nodes.WorkbenchTabNode(tabData)
        newNode = self.AddChildNode(node, data)
        self.AddDockSections(newNode)
        self.AddToolbars(newNode)
        return newNode
        
    def AddNewDashboardPart(self, node):
        with self.ForceRedraw():
            label = 'New Part (%d)' % (len(node.GetData().contents.parts) + 1)
            newPartContent = node.GetData().contents.parts.add()
            newPartSettings = node.GetData().userSettings.partSettings.add()
            newPartContent.view.caption = label
            data = Nodes.DashboardPartNode(newPartContent, newPartSettings)
            newNode = self.AddChildNode(node, data)
            self.AfterNodeAdd(newNode)
        
    def AddDashboardParts(self, parentNode):
        for i, partContent in enumerate(parentNode.GetData().contents.parts):
            data = Nodes.DashboardPartNode(partContent,
                                parentNode.GetData().userSettings.partSettings[i])
            self.AddChildNode(parentNode, data)
        
    def AddNewDockPart(self, node):
        with self.ForceRedraw():
            parts = node.GetData().contents.parts
            label = 'New Part (%d)' % (len(parts) + 1)
            newPart = parts.add()
            newPart.view.caption = label
            data = Nodes.DockPartNode(newPart)
            newNode = self.AddChildNode(node, data)
            self.AfterNodeAdd(newNode)
        
    def AddDockedParts(self, parentNode, dockedContent):
        try:
            for part in dockedContent.parts:
                data = Nodes.DockPartNode(part)
                partNode = self.AddChildNode(parentNode, data)
                self.AddButtons(partNode)
        except StandardError as e:
            pass
        
    def AddMainView(self, parent, workbenchContent):
        data = Nodes.MainViewNode(workbenchContent.view)
        self.AddChildNode(parent, data)
        
    def AddDockedBelow(self, parent, contents, settings):
        data = Nodes.DockSectionNode('Docked Below', 'BottomPane', contents.dockedBelow, settings.dockedBelow)
        dockedBelow = self.AddChildNode(parent, data)
        self.AddDockedParts(dockedBelow, contents.dockedBelow)
        
    def AddDockedRight(self, parent, contents, settings):
        data = Nodes.DockSectionNode('Docked Right', 'RightPane', contents.dockedRight, settings.dockedRight)
        dockedRight = self.AddChildNode(parent, data)
        self.AddDockedParts(dockedRight, contents.dockedRight)
        
    def AddDockSections(self, parent):
        contents = parent.GetData().contents
        settings = parent.GetData().userSettings

        self.AddMainView(parent, contents)
        dockedBelow = self.AddDockedBelow(parent, contents, settings)
        dockedRight = self.AddDockedRight(parent, contents, settings)
        
        self.AddDockedParts(dockedBelow, contents.dockedBelow)
        self.AddDockedParts(dockedRight, contents.dockedRight)
        
    def AddToolbars(self, parent):
        parentData = parent.GetData().contents
        data = Nodes.ToolbarNode(parentData.toolbar)
        toolbar = self.AddChildNode(parent, data)
        self.AddButtons(toolbar)
        
    def AddNewButtons(self, node):
        with self.ForceRedraw():
            button = node.GetData().GetButtons().add()        
            isDockPartNode = isinstance(node.GetData(), Nodes.DockPartNode)
            if isDockPartNode:
                button.selectionControlled = True
            label = 'New Buttons (%d)' % len(node.GetData().GetButtons())
            button.label = label
            buttonNode = Nodes.ButtonNode(button, isDockPartNode)            
            newNode = self.AddChildNode(node, buttonNode)
            self.AfterNodeAdd(newNode)
        
    def AddButtons(self, node):
        isDockPartNode = isinstance(node.GetData(), Nodes.DockPartNode)
        buttons = node.GetData().GetButtons()
        for i, b in enumerate(buttons):
            data = Nodes.ButtonNode(b, isDockPartNode)
            self.AddChildNode(node, data)

    def SetTopNodeLabel(self, label):
        node = self.tree.GetFirstItem()
        node.GetData().label = label
        self.UpdateNode(node)
        
    def UpdateSelectedNode(self):
        self.UpdateNode(self.tree.GetSelectedItem())
    
    def UpdateNode(self, node):
        data = node.GetData()
        node.Label(data.Label())
        node.Icon(data.Icon(), data.Icon())
        
    def AddTabs(self, workspaceNode):
        try:
            for tab in workspaceNode.GetData().contents.tabs:
                if tab.tabType == 'dashboard':
                    self.AddDashboardTab(workspaceNode, tab)
                elif tab.tabType == 'workbench':
                    self.AddWorkbenchTab(workspaceNode, tab)
        except StandardError as e:
            import traceback
            traceback.print_exc()
    
    def Clear(self):
        self.tree.RemoveAllItems()
        
    def LoadWorkspace(self, workspace, name):
        self.Clear()
        workspaceNode = self.AddWorkspace(workspace, name)
        self.AddTabs(workspaceNode)
        self.tree.GetFirstItem().Expand()

    def AddWorkspace(self, workspace, name):
        # TODO Roll into LoadWorkspace
        try:
            data = Nodes.WorkspaceNode(workspace, name)
            return self.AddChildNode(self.treeRoot, data)
        except StandardError as e:
            import traceback
            traceback.print_exc()    
            
    def HandleCreate( self, layout ):
        self.tree = layout.GetControl('tree')
        self.tree.AddCallback('ContextMenu', self.TreeContextMenuCB, None)
        self.treeRoot = self.tree.GetRootItem()
        self.tree.AddCallback("SelectionChanged", self.OnTreeSelectionChanged, None)
        
    def RemoveTab(self, node):
        parentData = node.Parent().GetData()
        nodeData = node.GetData()
        parentData.contents.tabs.remove(nodeData.tabContent)
        node.Remove()
    
    def RemoveDockSectionPart(self, node):
        partContent = node.GetData()
        tabContent = node.Parent().GetData().contents
        tabContent.parts.remove(partContent.part)
        node.Remove()
        
    def RemoveDashboardPart(self, node):
        parentContentData = node.Parent().GetData().contents
        parentSettingsData = node.Parent().GetData().userSettings
        
        partContent = node.GetData().part
        partSettings = node.GetData().settings
        
        parentContentData.parts.remove(partContent)
        parentSettingsData.partSettings.remove(partSettings)
        
        node.Remove()
    
    def RemoveButtons(self, node):
        parentData = node.Parent().GetData()
        nodeData = node.GetData().button
        parentData.GetButtons().remove(nodeData)
        node.Remove()
    
    def AddChildNode(self, parent, childData):
        newNode = parent.AddChild()
        newNode.SetData(childData)
        self.UpdateNode(newNode)
        return newNode
    
    def ExpandRecursive(self, node):
        node.Expand()
        for child in node.Children():
            self.ExpandRecursive(child)
    
    def AfterNodeAdd(self, newNode):
        self.ExpandRecursive(newNode)
        parent = newNode.Parent()
        parent.Expand()
        newNode.Select()
    
    def SwapNodes(self, first, second):
        def SortButtons(a, b):
            for child in parent.Children():
                if child.GetData().button == a:
                    return -1
                if child.GetData().button == b:
                    return 1
        def SortParts(a, b):
            for child in parent.Children():
                if child.GetData().part == a:
                    return -1
                if child.GetData().part == b:
                    return 1
        def SortTabs(a, b):
            for child in parent.Children():
                if child.GetData().tabContent == a:
                    return -1
                if child.GetData().tabContent == b:
                    return 1
        parent = first.Parent()
        self.tree.Swap(first, second)
        parentData = parent.GetData()
        if isinstance(parentData, Nodes.ToolbarNode):
            parentData.toolbar.buttons.sort(SortButtons)
        elif isinstance(parentData, Nodes.WorkspaceNode):
            parentData.contents.tabs.sort(SortTabs)
        elif isinstance(parentData, (Nodes.DashboardTabNode, Nodes.DockSectionNode)):
            parentData.contents.parts.sort(SortParts)
    
    @contextmanager
    def ForceRedraw(self):
        def Begin():
            self._forceRedrawCount += 1
            
        def End():
            self._forceRedrawCount -= 1
            if (self._forceRedrawCount == 0):
                self.tree.ForceRedraw()
        Begin()
        try:
            yield None
        finally:
            End()
