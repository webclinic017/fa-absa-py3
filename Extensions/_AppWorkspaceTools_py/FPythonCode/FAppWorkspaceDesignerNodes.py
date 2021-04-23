""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/AppWorkspaceTools/etc/FAppWorkspaceDesignerNodes.py"
""" Compiled: 2018-06-07 17:06:19 """

#__src_file__ = "extensions/AppWorkspaceTools/etc/FAppWorkspaceDesignerNodes.py"
import acm
import FUxCore
import Contracts_AppConfig_Messages_AppWorkspace as AppWorkspace

class NodeBase():
    def __init__(self, icon=''):
        self.icon = icon
        
    def Label(self):
        raise NotImplementedError('Label')
    
    def Icon(self):
        return self.icon

class WorkspaceNode(NodeBase):
    def __init__(self, workspace, label):
        NodeBase.__init__(self, 'FWorkspace')
        self.contents = workspace
        self.label = label
    
    def Label(self):
        return self.label
    
    def OnSelection(self, treePanel):
        # TODO Don't navigate to siblings, go through parent
        workspacePanel = treePanel.parent.workspacePanel
        workspacePanel.nodeData = self
        workspacePanel.SetupWorkspaceControls()
    
class DashboardTabNode(NodeBase):
    def __init__(self, tabContent):
        NodeBase.__init__(self, 'WindowSwitch')
        self.tabContent = tabContent
        self.contents = self.Contents()
        self.userSettings = self.Settings()
    
    def Label(self):
        label = self.tabContent.caption.encode('utf-8')
        return label or '<Dashboard>'
    
    def Contents(self):
        contents = AppWorkspace.DashboardContent()
        contents.ParseFromString(self.tabContent.contents)
        return contents
        
    def Settings(self):
        userSettings = AppWorkspace.DashboardSettings()
        userSettings.ParseFromString(self.tabContent.userSettings)
        return userSettings
        
    def OnSelection(self, treePanel):
        workspacePanel = treePanel.parent.workspacePanel
        workspacePanel.nodeData = self
        workspacePanel.SetupDashboardTabControls()
    
class WorkbenchTabNode(NodeBase):
    def __init__(self, tabContent):
        NodeBase.__init__(self, 'Layout')
        self.tabContent = tabContent
        self.contents = self.Contents()
        self.userSettings = self.Settings()
    
    def Label(self):
        label = self.tabContent.caption.encode('utf-8') 
        return label or '<Workbench>'
    
    def Contents(self):
        contents = AppWorkspace.WorkbenchContent()
        contents.ParseFromString(self.tabContent.contents)
        return contents
        
    def Settings(self):
        userSettings = AppWorkspace.WorkbenchSettings()
        userSettings.ParseFromString(self.tabContent.userSettings)
        return userSettings
        
    def OnSelection(self, treePanel):
        workspacePanel = treePanel.parent.workspacePanel
        workspacePanel.nodeData = self.tabContent
        workspacePanel.SetupWorkbenchTabControls()
        
class DashboardPartNode(NodeBase):
    def __init__(self, part, settings, label=None):
        NodeBase.__init__(self, 'FExtension')
        self.part = part 
        self.settings = settings
            
    def Label(self):
        v = self.part.view
        label = v.caption if v.HasField('caption') and v.caption else v.viewName
        return label.encode('utf-8') or '<Part>'
        
    def OnSelection(self, treePanel):
        workspacePanel = treePanel.parent.workspacePanel
        workspacePanel.nodeData = self
        workspacePanel.SetupDashboardPartControls()

class DockPartNode(NodeBase):
    def __init__(self, part):
        NodeBase.__init__(self, 'FExtension')
        self.part = part
    
    def Label(self):
        v = self.part.view
        label = v.caption if v.HasField('caption') and v.caption else v.viewName
        return label.encode('utf-8') or '<Part>'

    def GetButtons(self):
        return self.part.selectionActionButtons
        
    def OnSelection(self, treePanel):
        workspacePanel = treePanel.parent.workspacePanel
        workspacePanel.nodeData = self.part
        workspacePanel.SetupDockSectionPartControls()

class MainViewNode(NodeBase):
    def __init__(self, view):
        NodeBase.__init__(self, 'DisplayTabs')
        self.view = view
    
    def Label(self):
        return 'Main View'
    
    def OnSelection(self, treePanel):
        workspace = treePanel.parent.workspacePanel
        workspace.nodeData = self.view
        workspace.SetupMainViewControls()
        
class DockSectionNode(NodeBase):
    def __init__(self, label, icon, contents, settings):
        NodeBase.__init__(self, icon)
        self.label = label
        self.contents = contents
        self.settings = settings
    
    def Label(self):
        return self.label
    
    def OnSelection(self, treePanel):
        workspace = treePanel.parent.workspacePanel
        workspace.nodeData = self
        workspace.SetupDockSectionControls()
        
class ToolbarNode(NodeBase):
    def __init__(self, toolbar):
        NodeBase.__init__(self, 'InstrumentAppBkg+SettingsOverlay')
        self.toolbar = toolbar
    
    def Label(self):
        return 'Toolbar'

    def GetButtons(self):
        return self.toolbar.buttons        

    def OnSelection(self, treePanel):
        workspacePanel = treePanel.parent.workspacePanel
        workspacePanel.nodeData = self.toolbar.quickOpen
        workspacePanel.SetupToolbarControls()
        
class ButtonNode(NodeBase):
    def __init__(self, button, isDockPartNode):
        NodeBase.__init__(self, 'TradeEntryApp')
        self.button = button
        self.isDockPartNode = isDockPartNode
    
    def Label(self):
        label = self.button.HasField('label') and \
                self.button.label.encode('utf-8')
        return label or '<Buttons>'

    def OnSelection(self, treePanel):
        workspacePanel = treePanel.parent.workspacePanel
        workspacePanel.nodeData = self.button
        workspacePanel.SetupButtonControls(self.isDockPartNode)