""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SchedulingDashboard/etc/SchedulingDashboardTaskPanel.py"
from __future__ import print_function
""" Panel class for Scheduling Dashboard """

__version__ = '0.0'
__author__ = 'Louise Wiksten'

import acm
import FUxCore
from SchedulingDashboardDialogs import NewDependencyDialog
from SchedulingDashboardMenuItems import TaskMenuItems

class TaskPanel(FUxCore.LayoutPanel):
    def __init__(self):
        self.parent = None
        self.task = None

    def HandleCreate(self):
        layout = self.SetLayout(self.CreateLayout())
        self.taskName = layout.GetControl('taskName')
        self.moduleName = layout.GetControl('moduleName')
        self.moduleName.Editable(False)
        self.ctxName = layout.GetControl('ctxName')
        self.ctxName.Editable(False)
        self.description = layout.GetControl('description')
        self.historyLength = layout.GetControl('historyLength')
        self.historyUnit = layout.GetControl('historyUnit')
        units = acm.FEnumeration['enum(DatePeriodUnit)'].Values()
        for unit in units:
            self.historyUnit.AddItem(unit)
        self.historyUnit.SetData(units[0])

        self.saveTask = layout.GetControl('saveTask')
        self.saveTask.SetIcon('Save', False)
        self.saveTask.Enabled(False)
        self.saveTask.AddCallback('Activate', self.SaveTaskData, None)

        self.dependencyList = layout.GetControl('dependencyList')
        self.dependencyList.AddCallback('ContextMenu', self.DepCtxMenu, None)
        self.addDependency = layout.GetControl('addDependency')
        self.addDependency.Enabled(False)
        self.addDependency.AddCallback('Activate', self.NewDependency, None)

        self.scheduleList = layout.GetControl('scheduleList')
        self.scheduleList.AddCallback('ContextMenu', self.SchdCtxMenu, None)
        self.scheduleList.AddCallback('DefaultAction', self.OpenSchdule, None)

    def CreateLayout(self):
        builder = acm.FUxLayoutBuilder()
        builder.BeginHorzBox('None')
        builder.AddSpace(5) #Margin
        builder.BeginVertBox('None')
        builder.AddLabel('Invisible', 'Task Data')
        builder.AddInput('taskName', 'Name', 25)
        builder.AddInput('moduleName', 'Module')
        builder.AddInput('ctxName', 'Context')
        builder.AddInput('description', 'Description')
        builder.AddInput('historyLength', 'History Length')
        builder.AddOption('historyUnit', 'History Unit')
        builder.BeginHorzBox('None')
        builder.AddFill()
        builder.AddButton('saveTask', 'Save')
        builder.EndBox()
        
        builder.AddSpace(10)
        builder.AddLabel('preDep', 'Dependent On Tasks')
        builder.AddList('dependencyList', numlines=3, maxnumlines=3)
        builder.BeginHorzBox('None')
        builder.AddFill()
        builder.AddButton('addDependency', 'Add Dependency')
        builder.EndBox()

        builder.AddLabel('schedulesLabel', 'Schedules')
        builder.AddList('scheduleList', numlines=3, maxnumlines=3)

        builder.EndBox()
        builder.AddSpace(5) #Margin
        builder.EndBox()
        return builder

    def CreateCommandCB(self):
        """ Create a command item of class MenuItems. """
        ctrl = TaskMenuItems()
        ctrl.SetPanel(self)
        return ctrl

    def SetParent(self, parent):
        self.parent = parent

    def SetCurrentTask(self, task):
        self.task = task
        self.UpdateFields()

    def ClearFields(self):
        self.dependencyList.Clear()
        self.scheduleList.Clear()
        self.taskName.SetData('')
        self.moduleName.SetData('')
        self.ctxName.SetData('')
        self.description.SetData('')
        self.historyLength.SetData('')
        self.historyUnit.SetData('None')
        self.addDependency.Enabled(False)
        self.saveTask.Enabled(False)

    def LoadDependencies(self):
        self.dependencyList.Clear()
        root = self.dependencyList.GetRootItem()
        for dep in self.task.Dependencies():
            if dep in self.parent.changesMade['delDep']: #To be deleted.
                continue
            depItem = root.AddChild()
            pre_task = dep.Predecessor()
            grpLabel = ''
            if pre_task.Group() != self.task.Group():
                if pre_task.Group():
                    grpLabel = ' (%s)' % pre_task.Group().Name()
                else:
                    grpLabel = ' (No group)'
            depItem.Label('%s%s' % (pre_task.Name(), grpLabel))
            depItem.SetData(dep)
        for dep in self.parent.changesMade['newDep']: #New dependencies.
            if dep[0] != self.task:
                continue
            depItem = root.AddChild()
            pre_task = dep[1]
            depItem.Label('%s' % (pre_task.Name()))
            depItem.SetData(dep)

    def LoadSchedules(self):
        self.scheduleList.Clear()
        root = self.scheduleList.GetRootItem()
        for schedule in self.task.Schedules():
            scheduleItem = root.AddChild()
            scheduleItem.Label(schedule.Schedule())
            scheduleItem.SetData(schedule)

    def UpdateFields(self):
        if not self.task:
            self.ClearFields()
            return
        self.addDependency.Enabled(True)
        self.saveTask.Enabled(True)
        self.taskName.SetData(self.task.Name())
        self.moduleName.SetData(self.task.ModuleName())
        self.ctxName.SetData(self.task.ContextName())
        self.description.SetData(self.task.Description())
        self.historyLength.SetData(self.task.HistoryLength_count())
        self.historyUnit.SetData(self.task.HistoryLength_unit())

        self.LoadDependencies()
        self.LoadSchedules()

    def SaveTaskData(self, arg0, arg1):
        if self.ValidName(self.taskName.GetData()):
            self.task.Name(self.taskName.GetData()) 
        self.task.Description(self.description.GetData())
        # TODO: Validate history lenght input
        self.task.HistoryLength_count(self.historyLength.GetData())
        self.task.HistoryLength_unit(self.historyUnit.GetData())
        
        try: 
            self.task.Commit()
            self.parent.RedrawEditedGroup()
        except Exception as e:
            print('Failed to save the task.', e)
            msg = 'Failed to save the updates to the task. See the log ' + \
                  'for error message.'
            acm.UX().Dialogs().MessageBoxInformation(self.Shell(), msg)

    def ValidName(self, name):
        if not name:
            return False
        task = acm.FAelTask[name]
        if task and self.task != task:
            return False
        return True

    def NewDependency(self, arg1, arg2):
        dependencyDlg = NewDependencyDialog()
        dependencyDlg.application = self.parent
        dependencyDlg.task = self.task
        dependencyDlg.group = self.parent.groupList.GetSelectedItem().GetData()
        builder = dependencyDlg.BuildLayout()
        action = acm.UX().Dialogs().ShowCustomDialogModal(self.Shell(),
                                                          builder,
                                                          dependencyDlg)
        if action:
            self.parent.RedrawEditedGroup()

    def DeleteDependency(self):
        item = self.dependencyList.GetSelectedItem()
        if not item or not item.GetData():
            return
        dep = item.GetData()
        #Type checking:
        if dep in acm.GetClass('FAelTaskDependency').InstancesKindOf():
            # Add to delete list
            self.parent.groupEdited = True
            self.parent.saveGrpBtn.Enabled(True)
            self.parent.changesMade['delDep'].append(dep)
            self.parent.RedrawEditedGroup()
            return
        # New dependency, remove it from new dependency list.
        for newDep in self.parent.changesMade['newDep']:
            if newDep[0] == dep[0] and newDep[1] == dep[1]:
                self.parent.changesMade['newDep'].remove(newDep)
                self.parent.RedrawEditedGroup()
                return
    
    def OpenSchdule(self, arg0, arg1):
        scheduleItem = self.scheduleList.GetSelectedItem()
        if not scheduleItem or not scheduleItem.GetData():
            return
        acm.UX().SessionManager().StartApplication('Manage Ael Task Schedule',
                                                   scheduleItem.GetData())
        # Wait for completion and update?  (self.LoadSchedules())

    def DeleteSchedule(self):
        scheduleItem = self.scheduleList.GetSelectedItem()
        if not scheduleItem or not scheduleItem.GetData():
            return
        schedule = scheduleItem.GetData()
        msg = 'Are you sure you want to delete this schedule ' + \
              'for %s?' % self.task.Name()
        action = acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 
                                                       'Warning',
                                                       msg)
        if action == 'Button1':
            try: 
                schedule.Delete()
                self.LoadSchedules()
            except Exception as e:
                print('Could not delete the schedule.', e)

    @FUxCore.aux_cb
    def DepCtxMenu(self, ud, cd): 
        menuBuilder = cd.At('menuBuilder')
        items = cd.At('items')
        objects = acm.FArray()
        for item in items:
            objects.Add(item.GetData())
        if objects.Size() < 1:
            return
        acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder,
                                                       objects,
                                                       False, 
                                                       self.DepCtxItems,
                                                       None)

    def DepCtxItems(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        commands = acm.FArray()
        commands.Add(['deleteDependency', '', 'Delete', '', '', '',
                      self.CreateCommandCB, False])
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))

    @FUxCore.aux_cb
    def SchdCtxMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        items = cd.At('items')
        objects = acm.FArray()
        for item in items:
            objects.Add(item.GetData())
        if objects.Size() < 1:
            return
        acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder,
                                                       objects,
                                                       False, 
                                                       self.SchdCtxItems,
                                                       None)

    def SchdCtxItems(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        commands = acm.FArray()
        commands.Add(['deleteSchedule', '', 'Delete', '', '',
                      '', self.CreateCommandCB, False])
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))
