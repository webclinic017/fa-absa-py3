""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SchedulingDashboard/etc/SchedulingDashboardDialogs.py"

""" Dialog classes used in the Scheduling Dashboard application """

__version__ = '0.0'
__author__ = 'Louise Wiksten'

import acm
import FUxCore

class NewGroupDialog(FUxCore.LayoutDialog):
    def __init__(self):
        self.application = None

    def HandleApply(self):
        grpName = self.nameCtrl.GetData()
        if grpName == 0:
            return
        taskgroup = acm.FAelTaskGroup()
        taskgroup.Name(grpName)
        try:
            taskgroup.Commit()
        except Exception as e:
            print(e)
            action = self.ShowMessage(
                    'Error', 
                    'Could not create group. See log for information.\n' +\
                    'Do you want to try another name for the group?')
            if action == 'Button1':
                return None
        return True
    
    def HandleCreate(self, dialog, layout):
        self.dialog = dialog
        self.dialog.Caption('Create a new task group')

        self.nameCtrl = layout.GetControl('name')
        self.nameCtrl.AddCallback('Changed', self.CheckInputLength, None)
        self.okBtn = layout.GetControl('ok')
        self.okBtn.Enabled(False)

    def ShowMessage(self, msgType, msg):
        return acm.UX().Dialogs().MessageBoxOKCancel(self.dialog.Shell(), 
                                                     msgType,
                                                     msg)

    def CheckInputLength(self, arg0, arg1):
        nameInput = self.nameCtrl.GetData()
        if len(nameInput) > 0:
            self.okBtn.Enabled(True)
        else:
            self.okBtn.Enabled(False)

    def BuildLayout(self):
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox('None')
        builder.AddSpace(10)
        builder.AddInput('name', 'Name', 30)
        builder.AddSpace(5)
        builder.BeginHorzBox('None')
        builder.AddFill()
        builder.AddButton('ok', 'Save')
        builder.AddButton('cancel', 'Cancel')
        builder.AddFill()
        builder.EndBox()
        builder.EndBox()
        return builder

class NewDependencyDialog(FUxCore.LayoutDialog):
    def __init__(self):
        self.application = None
        self.dialog = None
        self.task = None
        self.group = None
        self.bindings = None

    def HandleApply(self):
        preTask = acm.FAelTask[self.tasks.GetData()]
        if not preTask:
            msg = 'Could not find the selected task. ' + \
                  'Make sure it has not been deleted.'
            acm.UX().Dialogs().MessageBoxInformation(self.dialog.Shell(), msg)
            return None

        if not self.ValidDependency(preTask, self.task):
            msg = 'Invalid dependency. This dependency is redundant or ' + \
                  'would lead to circular dependencies. Please select ' +\
                  'another task or remove existing dependencies.'
            acm.UX().Dialogs().MessageBoxInformation(self.dialog.Shell(), msg)
            return None
        
        # If the same dependency was deleted, remove it from the deleted-list.
        for dep in self.application.changesMade['delDep']:
            if dep.Predecessor() == preTask and dep.Successor() == self.task:
                self.application.changesMade['delDep'].remove(dep)
                return True

        self.application.groupEdited = True
        self.application.saveGrpBtn.Enabled(True)
        self.application.changesMade['newDep'].append((self.task, preTask))
        return True

    def ValidDependency(self, preTask, dependentTask):
        if self.DependencyExists(dependentTask, preTask): # Redundant
            return False
        if self.DependencyExists(preTask, dependentTask): # Circular
            return False
        return True

    def DependencyExists(self, currentTask, taskToFind):
        for dependency in currentTask.Dependencies():
            if dependency in self.application.changesMade['delDep']:
                continue #The dependency is to be deleted - no problem.
            if dependency.Predecessor() == taskToFind:
                return True
            if self.DependencyExists(dependency.Predecessor(), taskToFind):
                return True
        for dependency in self.application.changesMade['newDep']:
            if dependency[0] == currentTask and dependency[1] == taskToFind:
                return True
        return False

    def HandleCreate(self, dialog, layout):
        self.dialog = dialog
        self.dialog.Caption('Add dependency for %s'%self.task.Name())
        self.bindings.AddLayout(layout)

        self.tasks = layout.GetControl('tasks')
        self.tasks.AddItem('')

        for task in self.group.Tasks():
            if task == self.task or task in self.application.changesMade['removed']:
                continue
            self.tasks.AddItem(task.Name())
        for task in self.application.changesMade['added']:
            if task == self.task:
                continue
            self.tasks.AddItem(task.Name())

        self.tasks.SetData('')
        self.tasks.AddCallback('Changed', self.CheckFields, None)        

        self.timeout.SetValue(0)
        self.timeout.ToolTip('The maximum time (in seconds) to wait for ' + \
                             'another task to finish executing, before ' + \
                             'considering the depencency failed. ' + \
                             '0 means off.')
        self.timeout.Visible(False)

        self.okBtn = layout.GetControl('ok')
        self.okBtn.Enabled(False)

    def CheckFields(self, arg0, arg1):
        if self.tasks.GetData() != '':
            self.okBtn.Enabled(True)
        else:
            self.okBtn.Enabled(False)
    
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        pass
    
    def UpdateControls(self):
        pass

    def BuildLayout(self):
        self.bindings = acm.FUxDataBindings()
        self.bindings.AddDependent(self)
        self.timeout = self.bindings.AddBinder('timeout', acm.GetDomain('int'))
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox('None')
        # TODO: add additional input fields if needed.
        builder.AddSpace(5)
        builder.AddOption('tasks', 'Select Task', 40)
        self.timeout.BuildLayoutPart(builder, 'Timeout')
        builder.AddSpace(5)
        builder.BeginHorzBox('None')
        builder.AddFill()
        builder.AddButton('ok', 'Save')
        builder.AddButton('cancel', 'Cancel')
        builder.AddFill()
        builder.EndBox()

        builder.EndBox()
        return builder
