""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/AppWorkspaceTools/etc/FAppWorkspaceDesignerApplication.py"
from __future__ import print_function
""" Compiled: 2018-06-07 17:06:19 """

#__src_file__ = "extensions/AppWorkspaceTools/etc/FAppWorkspaceDesignerApplication.py"
import acm
import FUxCore
import FAppWorkspaceDesignerPanels
import FAppWorkspaceDesignerTreePanel
import FAppWorkspaceDesignerMenuItems

import Contracts_AppConfig_Messages_AppWorkspace as AppWorkspace


def StartApplication(eii):
    acm.StartApplication('App Workspace Designer', None)
        
def CreateApplicationInstance():
    return AppWorkspaceDesignerApplication()
        
class AppWorkspaceDesignerApplication(FUxCore.LayoutApplication):

    def __init__(self):
        FUxCore.LayoutApplication.__init__(self)
        self.treePanel = None
        self.workspacePanel = None
        self.appWsTpl = None
        self.fileCommands = {
            'FileOpen'  : self.OnFileOpen,
            'FileSave'  : self.OnFileSave,
            'FileSaveAs': self.OnFileSaveAs,
            'FileNew'   : self.OnFileNew,
            'FileDelete': self.OnFileDelete
        }

    # -------------------------------------------------------------------------
    # Settings overrides
    # -------------------------------------------------------------------------
        
    def DoOverrideApplicationDefaultSize(self):
        return [550, 700]
    
    def DoChangeCreateParameters(self, params):
        params.SplitHorizontal(True)
        params.UseSplitter(True)

    # -------------------------------------------------------------------------
    # Standard handlers
    # -------------------------------------------------------------------------
        
    def HandleRegisterCommands(self, builder):
        commands = self.treePanel.CustomCommands(True)
        builder.RegisterCommands(FUxCore.ConvertCommands(commands), self.fileCommands.keys())
    
    def HandleStandardFileCommandInvoke(self, commandName):
        def UnknownCommand():
            print('Unknown Command:', commandName)
        self.fileCommands.get(commandName, UnknownCommand)()
        
    def HandleStandardFileCommandEnabled(self, commandName):
        ret = True
        if commandName == 'FileSaveAs':
            ret = self.appWsTpl is not None
        elif commandName == 'FileSave':
            ret = self.IsDirty()
        elif commandName == 'FileDelete':
            ret = self.appWsTpl and not self.appWsTpl.IsInfant()
        return ret

    def HandleCreate( self, creationInfo ):
        self.CreateTreeMenuPanel(creationInfo)
        self.CreateWorkspaceTabPanel(creationInfo)
        if self.appWsTpl:
            self.DoOpen()
        
    def HandleSetContents(self, contents):
        if contents:
            self.appWsTpl = contents.StorageImage()
            
    def HandleClose(self):
        return self.CheckPendingChanges()
        
    # -------------------------------------------------------------------------
    # Command handlers
    # -------------------------------------------------------------------------
        
    def OnFileOpen(self):
        if self.CheckPendingChanges():
            items = acm.FAppWorkspaceTemplate.Instances()
            toOpen = acm.UX().Dialogs().SelectObject(self.Shell(), 'Select App Workspace Template', 'App Workspace Template', items, None)
            if toOpen:
                self.appWsTpl = toOpen.StorageImage()
                self.DoOpen()
        
    def OnFileSave(self):
        try:
            self.DoSave()
            self.OnWorkspaceChanged()
        except Exception as e:
            acm.UX().Dialogs().MessageBoxInformation(self.Shell(), 'Unable to save workspace "%s". See log for details.' % self.appWsTpl.Name())

    def OnFileSaveAs(self):
        items = acm.FAppWorkspaceTemplate.Instances()
        
        def ValidateSaveAsCB(ud, name, existingItem, p3):
            isValidSave = existingItem == None

            if existingItem:
                ret = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Question', 'Are you sure you want to replace workspace "%s"?' % existingItem.StringKey())
                if ret == 'Button1':
                    try:
                        existingItem.Delete()
                        isValidSave = True
                    except RuntimeError as ex:
                        acm.UX().Dialogs().MessageBoxInformation(self.Shell(), 'Unable delete workspace "%s". See log for details.' % existingItem.StringKey())

            return isValidSave
            
        saved = acm.UX().Dialogs().SaveObjectAs(self.Shell(), 'Save App Workspace Template As...', 'App Workspace Templates',  items, None, ValidateSaveAsCB, None) 

        if saved:            
            orig = self.appWsTpl.Originator()
            try:
                self.appWsTpl.StorageSetNew()
                if isinstance(saved, str):
                    self.SetWorkspaceName(saved)
                else:
                    self.SetWorkspaceName(saved.Name())
                self.DoSave()
                self.OnWorkspaceChanged()
            except Exception as e:
                self.appWsTpl = orig.StorageImage()
                self.treePanel.SetTopNodeLabel(self.appWsTpl.Name())
                acm.UX().Dialogs().MessageBoxInformation(self.Shell(), e)

    def OnFileNew(self):
        if self.CheckPendingChanges():
            self.appWsTpl = acm.FAppWorkspaceTemplate()
            self.appWsTpl.Name('New App Workspace')
            self.treePanel.LoadWorkspace(AppWorkspace.Workspace(), self.appWsTpl.Name())
            self.OnWorkspaceChanged()
        
    def OnFileDelete(self):
        dialogOutput = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Question', 'Are you sure you want to delete workspace "%s" ?' % self.appWsTpl.Name())
        if dialogOutput == 'Button1':
            self.treePanel.Clear()
            self.workspacePanel.HideAllControls()
            self.SetContentCaption('')
            self.appWsTpl.Delete()
            self.appWsTpl = None
        
    # -------------------------------------------------------------------------
    # Internal methods
    # -------------------------------------------------------------------------

    def DoOpen(self):
        ws = AppWorkspace.Workspace()
        contents = self.appWsTpl.Contents()
        if contents:
            ws.ParseFromString(contents)
        self.treePanel.LoadWorkspace(ws, self.appWsTpl.Name())
        self.OnWorkspaceChanged()

    def DoSave(self):
        self.appWsTpl.Contents(self.treePanel.SerializedTopNode())
        self.appWsTpl.AutoUser(False)
        self.appWsTpl.Commit()
        self.appWsTpl = self.appWsTpl.StorageImage()

    def CheckPendingChanges(self):
        if self.IsDirty():
            ret = acm.UX().Dialogs().MessageBoxYesNoCancel(self.Shell(), 'Question', 'Save changes?')
            if ret == 'Button1':
                # Yes
                self.DoSave()
                return True
            elif ret == 'Button2':
                # No
                return True
            else:
                # Cancel
                return False
        return True
        
    def OnWorkspaceChanged(self):
        self.treePanel.OnTreeSelectionChanged(None, True)
        self.SetContentCaption(self.appWsTpl.Name())
        
    def CreateTreeMenuPanel(self, creationInfo):
        self.treePanel = FAppWorkspaceDesignerTreePanel.TreeMenuPanel(self)
        layout = creationInfo.AddPane(self.treePanel.CreateLayout(), self.treePanel.__name__)
        self.treePanel.HandleCreate(layout)
        
    def CreateWorkspaceTabPanel(self, creationInfo):
        self.workspacePanel = FAppWorkspaceDesignerPanels.WorkspaceTabPanel(self)
        layout = creationInfo.AddPane(self.workspacePanel.CreateLayout(), self.workspacePanel.__name__)
        self.workspacePanel.HandleCreate(layout)
        
    def SetWorkspaceName(self, name):
        self.appWsTpl.Name(name)
        self.treePanel.SetTopNodeLabel(name)
        
    def IsDirty(self):
        if self.appWsTpl:
            originator = self.appWsTpl.Originator()
            if originator:
                if originator.IsInfant() or self.appWsTpl.Name() != originator.Name():
                    return True
                else:
                    opened = originator.Contents()
                    if opened is None:
                        # When a persistent archive is loaded, empty contents are None rather than an empty string.
                        # This is the special case of saving a completely new workspace
                        opened = ''
                    # Simple but potentially expensive way to compare. 
                    current = self.treePanel.SerializedTopNode()
                    return opened != current
        else:
            return False