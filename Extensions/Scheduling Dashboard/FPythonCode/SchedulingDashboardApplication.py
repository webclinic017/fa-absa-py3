""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SchedulingDashboard/etc/SchedulingDashboardApplication.py"
from __future__ import print_function
""" Application class for Scheduling Dashboard """

__version__ = '1.0'
__author__ = 'Louise Wiksten'

import acm
import FUxCore
import FUxNet

import SchedulingDashboardMenuItems
from SchedulingDashboardTaskPanel import TaskPanel
from SchedulingDashboardDialogs import NewGroupDialog, NewDependencyDialog
import clr
import time

clr.AddReference('Nevron.Diagram')
clr.AddReference('Nevron.Diagram.Shapes')
clr.AddReference('Nevron.Diagram.WinForm')

# ---- ---- For building locally ---- ----
# clr.AddReference('\\..\\..\\Release\\Nevron.Diagram')
# clr.AddReference('\\..\\..\\Release\\Nevron.Diagram.Shapes')
# clr.AddReference('\\..\\..\\Release\\Nevron.Diagram.WinForm')

from System.Windows import Forms
from Nevron.Diagram import Shapes
from Nevron.Diagram import Layout

# Colors used in the application
_SYSCOLOR_RUNNING = clr.System.Drawing.Color.Lime
_SYSCOLOR_FINISHED = clr.System.Drawing.Color.Green
_SYSCOLOR_FAILED = clr.System.Drawing.Color.Red
_SYSCOLOR_PRE_FAILED = clr.System.Drawing.Color.Orange
_SYSCOLOR_NOTSTARTED = clr.System.Drawing.Color.LightGray
_SYSCOLOR_LONG = clr.System.Drawing.Color.Coral

_FCOLOR_RUNNING = acm.UX().Colors().Create(0, 255, 0)
_FCOLOR_FINISHED = acm.UX().Colors().Create(0, 128, 0)
_FCOLOR_PRE_FAILED = acm.UX().Colors().Create(255, 165, 0)
_FCOLOR_FAILED = acm.UX().Colors().Create(255, 0, 0)
_FCOLOR_NOTSTARTED = acm.UX().Colors().Create(211, 211, 211)
_FCOLOR_LONG = acm.UX().Colors().Create(211, 211, 211) #TODO: Select color.

_FONT_SIZE = 5

def StartApplication(eii):
    shell = eii.ExtensionObject().Shell()
    StartSchedulingDashboard(shell, 0)

def StartSchedulingDashboard(shell, count):
    acm.UX().SessionManager().StartApplication('Scheduling Dashboard', None)

def CreateApplicationInstance():
    return DashboardApplication()

def OpenItem(item):
    acm.UX().SessionManager().StartApplication('Task Management', item)

class UpdateHandler:
    def __init__(self):
        self.application = None

    def ServerUpdate(self, sender, aspect, param):
        # aspect - information on the type of server update.
        self.application.UpdateView()

class DashboardApplication(FUxCore.LayoutApplication):
    def __init__(self):
        self.taskPane = None
        self.drawingView = None
        self.drawingDocument = None
        self.taskgroups = []
        self.groupEdited = False
        self.changesMade = {'group': None, 'added': [], 'removed': [],
                            'newDep': [], 'delDep': []}
        self.currentUser = None
        self.userLevel = 0 #Give different users different privileges.

    def HandleClose(self):
        if self.groupEdited:
            res = acm.UX().Dialogs().MessageBoxYesNoCancel(
                self.Shell(), 'Warning', 'You have unsaved changes. ' + \
                'Do you want to save the changes before exiting?')
            if res == 'Button1':
                self.OnSaveGroup(None, None)
            elif res == 'Button3' or res == 'None':
                return False
        self.historyTable.RemoveDependent(self.updateHandler)
        self.historyTable.Commit()
        return True

    def GetApplicationIcon(self):
        return 'Tasks'

    @FUxCore.aux_cb
    def UpdateView(self):
        self.drawingDocument.BeginUpdate() # Update task view.
        for node in self.drawingDocument.ActiveLayer.Children(None):
            if isinstance(node, clr.Nevron.Diagram.NRectangleShape):
                task = acm.FAelTask[str(node.Text)]
                node.Style.FillStyle.Color = GetColorOfStatus(task)
        self.drawingDocument.EndUpdate()
        self.drawingDocument.UpdateAllViews() #Force redraw of view.
        self.UpdateTaskGroups() #Updates task group list statuses
        #self.groupList.SortColumn(2, 'Ascending') #Sort on status.

    def UpdateTaskGroups(self):
        for taskNode in self.groupList.GetRootItem().Children():
            taskgroup = taskNode.GetData()
            taskNode.Label(taskgroup.Name())
            taskNode.Label(taskgroup.Tasks().Size(), 1)
            status = GetTaskGroupStatus(taskgroup)
            taskNode.Label(status, 2)
            if status == 'Running': 
                taskNode.Style(2, False, 0, _FCOLOR_RUNNING.ColorRef())
            elif status == 'Finished':
                taskNode.Style(2, False, 0, _FCOLOR_FINISHED.ColorRef())
            elif status == 'Failed':
                taskNode.Style(2, True, 0, _FCOLOR_FAILED.ColorRef())
            elif status == 'Not started':
                taskNode.Style(2, False, 0, _FCOLOR_NOTSTARTED.ColorRef())
            elif status == 'Too slow':
                taskNode.Style(2, True, 0, _FCOLOR_LONG.ColorRef())

        for i in range(0, self.groupList.ColumnCount()):
            self.groupList.AdjustColumnWidthToFitItems(i)
        
    def DoChangeCreateParameters(self, createParams):
        createParams.UseSplitter(True)
        createParams.SplitHorizontal(True)
        createParams.LimitMinSize(True)
        createParams.AutoShrink(False)
        createParams.AdjustPanesWhenResizing(True)
        createParams.ShowMostRecentlyUsedList(True)
        
    def CreateCommandCB(self):
        """ Create a command item. """
        mItems = SchedulingDashboardMenuItems.menuItems()
        mItems.SetApplication(self)
        return mItems

    def HandleRegisterCommands(self, builder):
        commands = acm.FArray()
        commands.Add(['TaskManagement', 'View', 
                      'Open the Task Management application',
                      '', '', '', self.CreateCommandCB, False])
        fileCmds = acm.FSet()
        builder.RegisterCommands(FUxCore.ConvertCommands(commands), fileCmds)

    def HandleCreate(self, creationContext):
        self.currentUser = acm.FUser[acm.UserName()]

        self.taskPanel = TaskPanel()
        self.taskPanel.SetParent(self)
        self.Frame().CreateCustomDockWindow(self.taskPanel, 'taskDetails',
                                            'Task Details', 'Right')
        self.Frame().ShowDockWindow('taskDetails', False)
        self.taskgroups = acm.FAelTaskGroup.Select('')

        #Panel for the list of task groups
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.BeginHorzBox('None')
        b.AddLabel('taskGrps', 'Task Groups')
        b.EndBox()
        b.AddList('groupList', numlines=20, width=45)
        b.BeginHorzBox('None')
        b.AddFill()
        b.AddButton('addGrpBtn', 'New Group')
        b.EndBox()
        b.EndBox()
        layout = creationContext.AddPane(b, 'ListPane')
        
        self.groupList = layout.GetControl('groupList')
        self.groupList.AddColumn('Name')
        self.groupList.AddColumn('Tasks', toolTip='Number of tasks in group')
        self.groupList.AddColumn('Status', toolTip='Runtime status of tasks')
        self.groupList.EnableHeaderSorting()
        self.groupList.ShowColumnHeaders()
        self.groupList.AddCallback('Changing', self.SelectionChanging, None)
        self.groupList.AddCallback('ContextMenu', self.ListContextMenu, None)
        self.groupList.AddCallback('SelectionChanged',
                                   self.ListSelectionChanged, None)

        self.addGrpBtn = layout.GetControl('addGrpBtn')
        self.addGrpBtn.SetIcon('Add', False)
        self.addGrpBtn.AddCallback('Activate',
                                   self.AddNewGroup,
                                   None)
        self.AddTaskGroups()

        # Panel for task groups and tasks in graphical view
        builder  = acm.FUxLayoutBuilder()
        builder.BeginVertBox('None')
        builder.BeginHorzBox('None')
        builder.AddLabel('taskgrpLbl', 'The nice task group shown is this')
        builder.AddFill()
        builder.AddButton('saveGrpBtn', '')
        builder.EndBox()
        FUxNet.AddWinFormsControlToBuilder(builder, 'panel',
                                           'System.Windows.Forms.Panel',
                                           'System.Windows.Forms',
                                           400, 300)
        builder.BeginHorzBox('None')
        builder.AddFill()
        builder.AddButton('newTaskButton', 'Add Task')
        builder.EndBox()
        builder.EndBox()

        graphLayout = creationContext.AddPane(builder, 'GraphPane')
        self.taskGroupLabel = graphLayout.GetControl('taskgrpLbl')
        self.taskGroupLabel.Label('')
        self.saveGrpBtn = graphLayout.GetControl('saveGrpBtn')
        self.saveGrpBtn.SetIcon('Save', False)
        self.saveGrpBtn.ToolTip('Save changes made to current group')
        self.saveGrpBtn.AddCallback('Activate', self.OnSaveGroup, None)
        self.saveGrpBtn.Enabled(False)
        self.newTaskButton = graphLayout.GetControl('newTaskButton')
        self.newTaskButton.Enabled(False) #No task grp selected by default
        self.newTaskButton.AddCallback('Activate', self.AddNewTask, None)

        self.m_graphPanel = graphLayout.GetControl('panel').GetCustomControl()
        self.m_graphPanel.BorderStyle = Forms.BorderStyle.FixedSingle
        
        self.drawingView = clr.Nevron.Diagram.WinForm.NDrawingView()
        self.drawingView.Size = clr.System.Drawing.Size(400, 300)
        self.drawingDocument = clr.Nevron.Diagram.NDrawingDocument()

        #Init view
        self.drawingView.BeginInit()
        #Init drawing document
        self.drawingView.Document = self.drawingDocument
        self.drawingDocument.BeginInit()
        self.drawingView.ViewLayout = clr.Nevron.Diagram.ViewLayout.Fit
        self.drawingView.Dock = Forms.DockStyle.Fill
        self.drawingView.BackColor = clr.System.Drawing.Color.White
        self.drawingView.Grid.Visible = False
        self.drawingView.GlobalVisibility.ShowPorts = False
        self.drawingView.HorizontalRuler.Visible = False
        self.drawingView.VerticalRuler.Visible = False
        self.drawingView.ScrollBars = Forms.ScrollBars.Vertical

        # SELECTIONS OF NODES
        selectHandler = clr.Nevron.Dom.NodeEventHandler(self.NodeSelected)
        self.drawingView.NodeSelected += selectHandler
        deselectHandler = clr.Nevron.Dom.NodeEventHandler(self.NodeDeselected)
        self.drawingView.NodeDeselected += deselectHandler

        rightClickHandler = clr.System.EventHandler(self.NodeRightClick)
        self.drawingView.Click += rightClickHandler

        #multiHandler = clr.System.EventHandler(self.MultiNodeSelcted)
        #self.drawingView.MultiSelectionEnded += multiHandler

        # TODO: Choose a good/relevant/intuitive color for highlighting!!
        # Style for selected items.
        strokeStyle = clr.Nevron.GraphicsCore.NStrokeStyle(clr.System.Drawing.Color.Yellow)
        self.drawingView.InteractiveAppearance.SelectedStrokeStyle = strokeStyle
        fillStyle = clr.Nevron.GraphicsCore.NColorFillStyle(clr.System.Drawing.Color.Yellow)
        self.drawingView.InteractiveAppearance.SelectedTextFillStyle = fillStyle
         
        self.drawingDocument.SizeToContent( 
            self.drawingDocument.AutoBoundsMinSize,
            self.drawingDocument.AutoBoundsPadding,
            clr.Nevron.Diagram.Filters.NFilters.Visible)

        self.drawingDocument.EndInit()

        tool = self.drawingView.Controller.Tools.GetToolByName(
            clr.Nevron.Diagram.WinForm.NDWFR.ToolSelector)
        tool.Enabled = True
        tool = self.drawingView.Controller.Tools.GetToolByName(
            clr.Nevron.Diagram.WinForm.NDWFR.ToolMouseEventDelegator)
        tool.Enabled = True
        self.drawingView.EndInit()  

        self.m_graphPanel.SuspendLayout()
        self.m_graphPanel.Controls.Add(self.drawingView)
        self.m_graphPanel.ResumeLayout()

        # Update on new history entries.
        self.updateHandler = UpdateHandler()
        self.updateHandler.application = self
        self.historyTable = acm.FAelTaskHistory.Select('')
        self.historyTable.AddDependent(self.updateHandler)
        self.historyTable.Commit()

# ------- Various application helper functions -------
    def OnSaveGroup(self, arg0, arg1):
        group = self.changesMade['group']
        acm.BeginTransaction()
        for task in self.changesMade['added']: # Add tasks to group
            task.Group(group)
            task.Commit()
        for task in self.changesMade['removed']: # Remove tasks from group
            task.Group(None)
            task.Commit()
        for newDep in self.changesMade['newDep']: # Add dependency
            newDependency = acm.FAelTaskDependency()
            newDependency.Predecessor(newDep[1])
            newDependency.Successor(newDep[0])
            newDependency.Commit()
        for dependency in self.changesMade['delDep']: #Delete dependency
            dependency.Delete()

        try: 
            acm.CommitTransaction()
            self.ClearSavedItems()
            self.UpdateTaskGroups()
            self.DisplayTasks(group)
        except Exception as e:
            print('Failed to commit.', e)

    def ClearSavedItems(self):
        #Removes all the items that were to be saved.
        self.changesMade = {'group': None, 'added': [], 'removed': [],
                            'newDep': [], 'delDep': []}
        self.groupEdited = False
        self.saveGrpBtn.Enabled(False)

    def AddNewTask(self, arg0, arg1):
        selItem = self.groupList.GetSelectedItem()
        if not selItem or not selItem.GetData():
            return
        group = selItem.GetData()
        tasks = acm.UX().Dialogs().SelectObjectsInsertItems(
                self.Shell(), acm.FAelTask, True)
        if not tasks:
            return
        tasksWGroups = acm.FArray()
        for task in tasks:
            if task.Group() and task.Group() != group:
                tasksWGroups.Add(task)

        if tasksWGroups.Size() > 0:
            msg = 'The following tasks are aldready part of a group:\n'
            for task in tasksWGroups:
                msg += '\n%s (%s)' % (task.Name(), task.Group().Name())
            msg += '\n\nDo you want to remove them from their current ' + \
                   'group and add them to %s?' % (group.Name())
            res = acm.UX().Dialogs().MessageBoxYesNoCancel(self.Shell(),
                                                           'Warning', msg)
            if res == 'Button3' or res == 'None': #Cancel or X
                return
            elif res == 'Button2': #No
                tasks = tasks.RemoveAll(tasksWGroups)
        for task in tasks:
            if task in self.changesMade['removed']:
                self.changesMade['removed'].remove(task)
                continue
            self.changesMade['added'].append(task)
        self.groupEdited = True
        self.saveGrpBtn.Enabled(True)
        self.RedrawEditedGroup()

    def AddNewGroup(self, arg0, arg1):
        grpDialog = NewGroupDialog()
        grpDialog.application = self
        builder = grpDialog.BuildLayout()
        added = acm.UX().Dialogs().ShowCustomDialogModal(self.Shell(),
                                                         builder,
                                                         grpDialog)
        if added:
            self.taskgroups = acm.FAelTaskGroup.Select('')
            self.AddTaskGroups()

    def DeleteGroup(self):
        selItem = self.groupList.GetSelectedItem()
        if not selItem or not selItem.GetData():
            return
        msg = 'Are you sure you want to permanently delete the group?\n' + \
              'Note! If there are any tasks in the group, they ' + \
              'will be removed from the group (but not deleted).'
        action = acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 
                                                       'Warning', msg)
        if action == 'Button2':
            return

        group = selItem.GetData() 
        while group.Tasks():
            task = group.Tasks().First()
            task.Group(None)
            try:
                task.Commit()
            except:
                print('Could not remove task %s from the ' % task.Name() + \
                      'group. The group may not have been deleted.')
                return
        try:
            group.Delete()
        except Exception as e:
            print('Could not delete the group.', e)
            return

        self.AddTaskGroups() #Reload list
        self.DisplayTasks(None)

    def GetTaskGroup(self, name):
        for taskgrp in self.taskgroups:
            if taskgrp.Name() == name:
                return taskgrp
        return None

    def AddTaskGroups(self):
        self.groupList.Clear()
        rootItem = self.groupList.GetRootItem()
        for taskgroup in self.taskgroups:
            node = rootItem.AddChild()
            node.SetData(taskgroup)
        self.UpdateTaskGroups()

    @FUxCore.aux_cb
    def DisplayTasks(self, taskgroup):
        dct = CreateTaskDependencyList(taskgroup)
        self.drawingDocument.ActiveLayer.RemoveAllChildren()    
        if not dct: #No task group selected
            return
        self.DrawTasks(taskgroup, dct)

    @FUxCore.aux_cb
    def DrawTasks(self, taskgroup, dct):
        factory = Shapes.NFlowChartingShapesFactory(self.drawingDocument)
        nodeDict = dict() #Keep reference to all nodes in a dictionary
        for task in dct: #Create vertices of all tasks.
            node = factory.CreateShape(Shapes.FlowChartingShapes.Process)
            node.Text = task.Name()
            node.Bounds = clr.Nevron.GraphicsCore.NRectangleF(0, 0, 100, 50)
            #Color is set for each individual task.
            style = clr.Nevron.Diagram.NStyle()
            fillStyle = clr.Nevron.GraphicsCore.NColorFillStyle()
            style.FillStyle = fillStyle
            textStyle = clr.Nevron.GraphicsCore.NTextStyle()
            font = textStyle.FontStyle
            font.EmSize = clr.Nevron.GraphicsCore.NLength(_FONT_SIZE)
            textStyle.FontStyle = font
            style.TextStyle = textStyle
            fillStyle.Color = GetColorOfStatus(task)
            node.Style = style

            prot = node.Protection
            prot.Rotate = True
            prot.MoveX = True
            prot.MoveY = True
            prot.ResizeX = True
            prot.ResizeY = True
            prot.Delete = True
            prot.InplaceEdit = True
            node.Protection = prot

            # Change what can be edited on the node.
            interactionStyle = node.InteractionStyle #NInteractionStyle
            interactionStyle.Bounds = False
            interactionStyle.GeometryMidPoints = False
            interactionStyle.GeometryPoints = False
            interactionStyle.PinPoint = False
            interactionStyle.RotatedBounds = False
            interactionStyle.Rotation = False
            interactionStyle.ShapeControlPoints = False
            interactionStyle.ShapePlugs = False
            node.InteractionStyle = interactionStyle

            self.drawingDocument.ActiveLayer.AddChild(node)
            nodeDict[task] = node

            #TODO: Add mouseover (maybe with information on status/error)!!!
            dClick = clr.Nevron.Diagram.NodeViewEventHandler(self.DoubleClick)
            node.DoubleClick += dClick

        for task in dct: #Create edges between dependant tasks.
            for dependency in dct[task]:
                connector = clr.Nevron.Diagram.NRoutableConnector()
                self.drawingDocument.ActiveLayer.AddChild(connector)
                connector.ToShape = nodeDict[dependency]
                connector.FromShape = nodeDict[task]
                connector.StyleSheetName = clr.Nevron.Diagram.NDR.NameConnectorsStyleSheet
                prot = connector.Protection
                prot.Select = True
                prot.InplaceEdit = True
                connector.Protection = prot

        shapes = self.drawingDocument.ActiveLayer.Children(
            clr.Nevron.Diagram.Filters.NFilters.Shape2D)

        #Use layered graph layout
        layout = Layout.NLayeredGraphLayout()
        layout.Direction = Layout.LayoutDirection.TopToBottom #Default
        layout.NodeRank = Layout.LayeredLayoutNodeRank.TopMost
        layout.LayerAlignment = Layout.RelativeAlignment.Near
        layout.EdgeRouting = Layout.LayeredLayoutEdgeRouting.Orthogonal
        layout.VertexSpacing = 30
        layout.LayerSpacing = 30
        layout.Compact = True

        layout.Layout(shapes, Layout.NDrawingLayoutContext(self.drawingDocument))
        self.drawingDocument.SizeToContent(
            self.drawingDocument.AutoBoundsMinSize,
            self.drawingDocument.AutoBoundsPadding,
            clr.Nevron.Diagram.Filters.NFilters.Visible)

    def RedrawEditedGroup(self):
        self.drawingDocument.ActiveLayer.RemoveAllChildren()  
        group = self.changesMade['group']
        if not group: #TODO ::: LOOK INTO FURTHER - might need to handle.
            return
        tasklist = []
        for task in group.Tasks():
            tasklist.append(task)
        for task in self.changesMade['added']: #Add tasks in view to simulate
            tasklist.append(task)
        for task in self.changesMade['removed']: #Remove tasks to remove from group
            tasklist.remove(task)

        adj_list = dict()
        for task in tasklist:
            adj_list[task] = []

        for task in tasklist:
            for dep in task.Dependencies():
                if dep in self.changesMade['delDep']:
                    continue #Hide.
                pre_task = dep.Predecessor()
                if pre_task.Group() != group or pre_task in self.changesMade['removed']:
                    continue
                adj_list[pre_task].append(task)

        for dpcy in self.changesMade['newDep']:
            adj_list[dpcy[1]].append(dpcy[0])
        
        self.DrawTasks(group, adj_list)

# ------- Action event handlers -------
    @FUxCore.aux_cb
    def SelectionChanging(self, arg0, arg1):
        if self.groupEdited:
            grp = self.changesMade['group']
            res = acm.UX().Dialogs().MessageBoxYesNo(
                self.Shell(), 'Warning', 'You have unsaved changes to group ' + \
                '%s. Do you want to save the changes?' % grp.Name())
            if res == 'Button1':
                self.OnSaveGroup(None, None)
            elif res == 'Button2':
                self.ClearSavedItems()
                # If nothing clicked - clear view or redraw it.
            elif res == 'Button3' or res == 'None':# TODO: STAY ON ITEM, CHANGE MESSAGE BOX.
                pass 

    @FUxCore.aux_cb
    def ListSelectionChanged(self, arg0, arg1):
        item = self.groupList.GetSelectedItem()
        if item and item.GetData():
            self.taskPanel.SetCurrentTask(None)
            self.changesMade['group'] = item.GetData()
            self.taskGroupLabel.Label(item.GetData().Name())
            self.newTaskButton.Enabled(True)
            self.DisplayTasks(item.GetData())
        else:
            self.taskGroupLabel.Label('')
            self.newTaskButton.Enabled(False)
            self.DisplayTasks(None)

    @FUxCore.aux_cb
    def ListContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        items = cd.At('items')
        objects = acm.FArray()
        for item in items:
            objects.Add(item.GetData())
        if objects.Size() < 1:
            return
        acm.UX().Menu().BuildStandardObjectContextMenu(
                menuBuilder, objects, False, self.ListContextItems, None)

    def ListContextItems(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        commands = acm.FArray()
        commands.Add(['DeleteGroup', '', 'Delete group', '', '',
                      '', self.CreateCommandCB, False])
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))

    @FUxCore.aux_cb
    def NodeSelected(self, args):
        item = args.Node
        if item:
            task = acm.FAelTask[str(item.Text)]
            if task: 
                self.Frame().ShowDockWindow('taskDetails', True)
                self.taskPanel.SetCurrentTask(task)

    @FUxCore.aux_cb
    def NodeDeselected(self, args):
        self.taskPanel.SetCurrentTask(None)
        ### self.Frame().ShowDockWindow('taskDetails', False) # Hide panel

    @FUxCore.aux_cb
    def DoubleClick(self, args):
        item = args.Node
        if item:
            task = acm.FAelTask[str(item.Text)]
            if task:
                OpenItem(task)

    @FUxCore.aux_cb
    def MultiNodeSelcted(self, sender, args):
        pass

    @FUxCore.aux_cb
    def NodeRightClick(self, sender, mouseArgs):
        if mouseArgs.Button != clr.System.Windows.Forms.MouseButtons.Right:
            return
        location = clr.Nevron.GraphicsCore.NPointF(mouseArgs.Location)
        shapes = self.drawingDocument.HitTest(
                location, -1, clr.Nevron.Diagram.Filters.NFilters.Shape2D,
                self.drawingView.ProvideDocumentHitTestContext())
        if shapes.Count == 0:
            return

        taskShape = shapes[0]
        if not taskShape or not acm.FAelTask[str(taskShape.Text)]:
            return
        self.selectedTask = acm.FAelTask[str(taskShape.Text)]
        
        contextMenu = clr.System.Windows.Forms.ContextMenuStrip()
        openTaskItem = clr.System.Windows.Forms.ToolStripMenuItem(
            'Open task', None, clr.System.EventHandler(self.OnOpenTaskCmd))
        contextMenu.Items.Add(openTaskItem)
        openWScriptItem = clr.System.Windows.Forms.ToolStripMenuItem(
            'Open with Runscript', None, clr.System.EventHandler(self.OnOpenTaskWithRunscript))
        #contextMenu.Items.Add(openWScriptItem)
        contextMenu.Items.Add('-')
        runOnServerItem = clr.System.Windows.Forms.ToolStripMenuItem(
            'Run on server', None, clr.System.EventHandler(self.OnExecuteOnServer))
        revokeOnServerItem = clr.System.Windows.Forms.ToolStripMenuItem(
            'Revoke', None, clr.System.EventHandler(self.OnRevokeOnServer))
        if self.selectedTask.GroupStatus() != 'None':
            contextMenu.Items.Add(revokeOnServerItem)
        else:
            contextMenu.Items.Add(runOnServerItem)
        contextMenu.Items.Add('-')
        ######################################TODO --- FIX add dependency (PRIME CRASHES)
        addDepItem = clr.System.Windows.Forms.ToolStripMenuItem(
            'Add dependency', None, clr.System.EventHandler(self.OnAddDependency))
        #contextMenu.Items.Add(addDepItem)
        removeFromGrpItem = clr.System.Windows.Forms.ToolStripMenuItem(
            'Remove from group', None, clr.System.EventHandler(self.OnRemoveFromGroup))
        contextMenu.Items.Add(removeFromGrpItem)
        contextMenu.Items.Add('-')
        propertiesItem = clr.System.Windows.Forms.ToolStripMenuItem(
            'Properties', None, clr.System.EventHandler(self.OnTaskProperties))
        contextMenu.Items.Add(propertiesItem)

        # Display the context menu at the point clicked in screen coordinates
        point = clr.System.Drawing.Point(int(location.X), int(location.Y))
        contextMenu.Show(self.drawingView, point)

    @FUxCore.aux_cb
    def OnOpenTaskCmd(self, sender, e):
        if self.selectedTask:
            OpenItem(self.selectedTask)

    @FUxCore.aux_cb
    def OnOpenTaskWithRunscript(self, sender, e):
        if self.selectedTask:
            pass #TODO - not sure how to handle.

    @FUxCore.aux_cb
    def OnExecuteOnServer(self, sender, e):
        if self.selectedTask:
            res = self.selectedTask.ExecuteOnServer()
            if not res:
                print('Failed to execute task on server.')

    @FUxCore.aux_cb
    def OnRevokeOnServer(self, sender, e):
        if self.selectedTask:
            res = self.selectedTask.RevokeExecuteOnServer()
            if not res:
                print('Could not revoke execution on server.')

    @FUxCore.aux_cb
    def OnAddDependency(self, sender, e):
        if self.selectedTask:
            dependencyDlg = NewDependencyDialog()
            #dependencyDlg.application = self
            dependencyDlg.task = self.selectedTask
            builder = dependencyDlg.BuildLayout()
            action = acm.UX().Dialogs().ShowCustomDialogModal(self.Shell(),
                                                              builder,
                                                              dependencyDlg)
            if action:
                #self.LoadDependencies()
                self.DisplayTasks(self.task.Group())

    @FUxCore.aux_cb
    def OnRemoveFromGroup(self, sender, e):
        if self.selectedTask:
            grp = self.selectedTask.Group()
            if not grp:
                grp = self.groupList.GetSelectedItem().GetData()
            if self.selectedTask in self.changesMade['added']:
                self.changesMade['added'].remove(self.selectedTask)
                return
            self.changesMade['removed'].append(self.selectedTask)
            self.saveGrpBtn.Enabled(True)
            self.groupEdited = True
            self.RedrawEditedGroup()

    @FUxCore.aux_cb
    def OnTaskProperties(self, sender, e):
        if self.selectedTask:
            self.selectedTask.Inspect()

def CreateTaskDependencyList(taskgroup):
    if not taskgroup:
        return None
    tasks = taskgroup.Tasks()
    adj_list = dict()
    for task in tasks:
        adj_list[task] = []

    for task in tasks:
        for dep in task.Dependencies():
            pre_task = dep.Predecessor()
            if pre_task.Group() != taskgroup:
                continue
            adj_list[pre_task].append(task)
    return adj_list

def GetTaskGroupStatus(taskgroup):
    if taskgroup.Tasks().Size() == 0:
        return 'No tasks in group'
    currStat = 0
    for task in taskgroup.Tasks():
        taskStatus = GetTaskStatusNumber(task)
        if taskStatus == 5:
            return StatusFromNumber(5)
        if taskStatus > currStat:
            currStat = taskStatus
    return StatusFromNumber(currStat)

def GetColorOfStatus(task):
    taskStatus = GetTaskStatus(task)
    if taskStatus == 'Scheduled':
        return _SYSCOLOR_NOTSTARTED
    elif taskStatus == 'Running':
        return _SYSCOLOR_RUNNING
    elif taskStatus == 'Prev Failed':
        return _SYSCOLOR_PRE_FAILED
    elif taskStatus == 'Failed':
        return _SYSCOLOR_FAILED
    elif taskStatus == 'Finished':
        return _SYSCOLOR_FINISHED 
    elif taskStatus == 'Running Long':
        return _SYSCOLOR_LONG
    elif taskStatus == 'Pending':
        return _SYSCOLOR_NOTSTARTED
    return _SYSCOLOR_NOTSTARTED

def GetTaskStatus(task):
    return StatusFromNumber(GetTaskStatusNumber(task))

def StatusFromNumber(taskStatus):
    # Scheduled = 0 | Finished = 1 | Running = 2 | Waiting = 3 |
    # Prev Failed = 4 | Failed = 5
    if taskStatus == 0:
        return 'Scheduled'
    elif taskStatus == 1:
        return 'Finished'
    elif taskStatus == 2:
        return 'Running'
    elif taskStatus == 3:
        return 'Too slow'
    elif taskStatus == 4:
        return 'Prev Failed'
    elif taskStatus == 5:
        return 'Failed'

def GetTaskStatusNumber(task):
    # ##### 'TODO: Get correct task status!' #####
    if not task:
        return 0
    if PredecessorRunAfter(task) or PredecessorsRunning(task):
        return 0
    if PredecessorsFailed(task):
        return 4
    # Gets its own status - predecessors are successfully finished.    
    if task.History().Size() == 0:
        return 0
    lastEntry = task.History().Last()
    taskStatus = lastEntry.Status()
    if task.IsPendingOnServer():
        return 0
    if taskStatus == 'Started': 
        return 2
    elif taskStatus == 'Failed':
        return 5
    elif taskStatus == 'Succeeded':
        return 1
    return 0

def PredecessorRunAfter(task):
    if task.History().Size() < 1:
        return False
    for dependency in task.Dependencies():
        pre_task = dependency.Predecessor()
        lastEntry = task.History().Last()
        if pre_task.History().Size() > 0:
            pre_last = pre_task.History().Last()
            if pre_last.StartTime() > lastEntry.StartTime():
                return True
            if PredecessorRunAfter(pre_task):
                return True
    return False

def PredecessorsRunning(task):
    for dependency in task.Dependencies():
        pre_task = dependency.Predecessor()
        if pre_task.IsPendingOnServer():
            return True
        if pre_task.History().Size() > 0:
            if pre_task.History().Last().Status() == 'Started':
                return True
            if PredecessorsRunning(pre_task):
                return True
    return False

def PredecessorsFailed(task):
    for dependency in task.Dependencies():
        pre_task = dependency.Predecessor()
        if pre_task.History().Size() > 0:
            if pre_task.History().Last().Status() == 'Failed':
                return True
            if PredecessorsFailed(pre_task):
                return True
    return False