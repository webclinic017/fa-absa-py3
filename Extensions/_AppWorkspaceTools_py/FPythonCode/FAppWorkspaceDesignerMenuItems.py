""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/AppWorkspaceTools/etc/FAppWorkspaceDesignerMenuItems.py"
""" Compiled: 2018-06-07 17:06:19 """

#__src_file__ = "extensions/AppWorkspaceTools/etc/FAppWorkspaceDesignerMenuItems.py"
import acm, FUxCore
import FAppWorkspaceDesignerNodes as Nodes

class NodeCommand(FUxCore.MenuItem):
    def __init__(self, treeMenuPanel, alwaysApplicable, applicableFor):
        self._treeMenuPanel = treeMenuPanel
        self._alwaysApplicable = alwaysApplicable
        self._applicableFor = applicableFor
    
    def Applicable(self):
        return self._alwaysApplicable or self._ApplicableImpl()
        
    def Enabled(self):
        return self._ApplicableImpl()
    
    def Checked(self):
        return False
    
    def _ApplicableImpl(self):
        selectedNode = self._SelectedNode()
        data = selectedNode and selectedNode.GetData()
        return bool(data and isinstance(data, self._applicableFor))
    
    def _SelectedNode(self):
        return self._treeMenuPanel.tree.GetSelectedItem()

class AddDashboardTab(NodeCommand):
    def __init__(self, treeMenuPanel, alwaysVisible=False):
        applicableFor = (Nodes.WorkspaceNode,)
        NodeCommand.__init__(self, treeMenuPanel, alwaysVisible, applicableFor)
        
    def Invoke(self, cd):
        self._treeMenuPanel.AddNewDashboardTab(self._SelectedNode())
        
class AddWorkbenchTab(NodeCommand):
    def __init__(self, treeMenuPanel, alwaysVisible=False):
        applicableFor = (Nodes.WorkspaceNode,)
        NodeCommand.__init__(self, treeMenuPanel, alwaysVisible, applicableFor)
        
    def Invoke(self, cd):
        self._treeMenuPanel.AddNewWorkbenchTab(self._SelectedNode())
        
class AddPart(NodeCommand):
    def __init__(self, treeMenuPanel, alwaysVisible=False):
        applicableFor = (Nodes.DashboardTabNode, Nodes.DockSectionNode)
        NodeCommand.__init__(self, treeMenuPanel, alwaysVisible, applicableFor)
        
    def Invoke(self, cd):
        node = self._SelectedNode()
        data = node.GetData()
        if isinstance(data, Nodes.DashboardTabNode):
            self._treeMenuPanel.AddNewDashboardPart(node)
        elif isinstance(data, Nodes.DockSectionNode):
            self._treeMenuPanel.AddNewDockPart(node)
        
class AddButtons(NodeCommand):
    def __init__(self, treeMenuPanel, alwaysVisible=False):
        applicableFor = (Nodes.ToolbarNode, Nodes.DockPartNode)
        NodeCommand.__init__(self, treeMenuPanel, alwaysVisible, applicableFor)
        
    def Invoke(self, cd):
        self._treeMenuPanel.AddNewButtons(self._SelectedNode())

class RemoveNode(NodeCommand):
    def __init__(self, treeMenuPanel, alwaysVisible=False):
        applicableFor = (Nodes.DashboardTabNode,\
                         Nodes.WorkbenchTabNode,\
                         Nodes.DockPartNode,\
                         Nodes.DashboardPartNode,\
                         Nodes.ButtonNode)
        NodeCommand.__init__(self, treeMenuPanel, alwaysVisible, applicableFor)
        
    def Invoke(self, cd):
        node = self._SelectedNode()
        data = node.GetData()
        if isinstance(data, (Nodes.DashboardTabNode, Nodes.WorkbenchTabNode)):
            self._treeMenuPanel.RemoveTab(node)
        elif isinstance(data, Nodes.DockPartNode):
            self._treeMenuPanel.RemoveDockSectionPart(node)
        elif isinstance(data, Nodes.DashboardPartNode):
            self._treeMenuPanel.RemoveDashboardPart(node)
        elif isinstance(data, Nodes.ButtonNode):
            self._treeMenuPanel.RemoveButtons(node)

class MoveNode(NodeCommand):
    def __init__(self, treeMenuPanel, moveDown, alwaysVisible=True):
        applicableFor = (Nodes.WorkspaceNode,\
                         Nodes.DashboardTabNode,\
                         Nodes.WorkbenchTabNode,\
                         Nodes.DashboardPartNode,\
                         Nodes.DockPartNode,\
                         Nodes.ButtonNode)
        NodeCommand.__init__(self, treeMenuPanel, alwaysVisible, applicableFor)
        self._treeMenuPanel = treeMenuPanel
        self._moveDown = moveDown
        
    def Enabled(self):
        applicableForNode = NodeCommand.Enabled(self)
        selected, sibling = self.__NodesToSwap()
        return applicableForNode and bool(selected and sibling)
    
    def Checked(self):
        return False
    
    def Invoke(self, cd):
        selected, sibling = self.__NodesToSwap()
        self._treeMenuPanel.SwapNodes(selected, sibling)
        
    def __NodesToSwap(self):
        tree = self._treeMenuPanel.tree
        selected = tree.GetSelectedItem()
        sibling = selected and selected.Sibling(self._moveDown)
        return selected, sibling