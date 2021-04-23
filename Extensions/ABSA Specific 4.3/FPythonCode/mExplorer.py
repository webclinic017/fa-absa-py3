
"""-----------------------------------------------------------------------------
MODULE
    myExplorer

DESCRIPTION
    Date                : 2017-10-17
    Purpose             : Task tracking tool
    Department and Desk : BTB
    Requester           : Ondrej Bahounek
    Developer           : Ondrej Bahounek
    CR Number           : CHNG0004998717

Info:  
This tool simplifies daily work with tasks and python modules.
Enables to see all tasks in FA together their latest run status.
Allows to open Python Editor directly from a task.
It is possible to switch to live mode, where tasks' statuses are updated on the fly.

ENDDESCRIPTION

HISTORY
=============================================================================================
Date       Change no    Developer          Description
------------------------------------------------------------------------------------------"""

from datetime import datetime
import time

import acm
import ael
import FUxCore


def start(eii):
    extension_object = eii.ExtensionObject()
    shell = extension_object.Shell()
    dialog = ExplorerDialog()
    builder = dialog.CreateLayout()
    acm.UX().Dialogs().ShowCustomDialog(shell, builder, dialog)


class MyGeneralCommandItem(FUxCore.MenuItem):
    def __init__(self):
        pass
        
    def Invoke(self, cd):
        return False
    
    def Applicable(self):
        return True
        
    def Enabled(self):
        return True
    
    def Checked(self):
        return False
        

class MyCommandItem_RunModule(MyGeneralCommandItem):

    def Invoke(self, cd):
        task = cd.ExtensionObject().GetSelectedItem().GetData()
        print("Running module '%s'" % task.ModuleName())
        acm.RunModuleWithParameters(task.ModuleName(), acm.GetDefaultContext())
        

class MyCommandItem_ViewModule(MyGeneralCommandItem):

    def Invoke(self, cd):
        task = cd.ExtensionObject().GetSelectedItem().GetData()
        module = acm.FAel[task.ModuleName()]
        if not module:
            print("Can't find '%s' in python modules" % task.ModuleName())
            return
        print("Viewing python module '%s'" % module.Name())
        acm.StartApplication('Python Editor', module)

        
class MyCommandItem_DeleteTask(MyGeneralCommandItem):

    def __init__(self, dialog_obj):
        self.dialog_obj = dialog_obj
    
    def Invoke(self, cd):
    
        tasks = [t.GetData() for t in cd.ExtensionObject().GetSelectedItems()]
        tasks_len = len(tasks)
        if tasks_len == 0:
            return
        if tasks_len == 1:
            msg = "Delete '%s' task?" % tasks[0].Name()
        else:
            msg = "Are you sure you want to delete all %d tasks?" % tasks_len
            
        ret_val = acm.UX().Dialogs().MessageBox(self.dialog_obj.m_fux_dlg.Shell(), "Question", msg,
            "Yes", "No", None, "Button1", "Button2")
        
        if ret_val == "Button1":
            tasks_ids = [t.Oid() for t in tasks]
            for task_id in tasks_ids:
                task = acm.FAelTask[task_id]
                print("Deleting task: '%s'" % task.Name())
                task.Delete()
            
            self.dialog_obj.refresh()


class ExplorerDialog(FUxCore.LayoutDialog):

    SORT_BY_DEFAULT = "Default"
    SORT_BY_UPDAT_TIME = "Update Time"
    SORT_BY_START = "Start Time"
    SORT_BY_STOP = "Stop Time"
    SORT_BY_STATUS = "Status"
    SORT_ITEMS = [SORT_BY_DEFAULT, SORT_BY_UPDAT_TIME, SORT_BY_START, SORT_BY_STOP, SORT_BY_STATUS]
    
    COL_WHITE = acm.UX().Colors().Create(255, 255, 255).ColorRef()
    COL_RED = 8686  # acm.UX().Colors().Create(255, 0, 0).ColorRef()
    COL_GREEN = 42544  # acm.UX().Colors().Create(0, 255, 0).ColorRef()
    COL_BLACK = 0
    COL_GRAY = acm.UX().Colors().Create(180, 180, 180).ColorRef()
    COL_ORANGE = 22258
    
    STATUS_SUCC = 'Succeeded'
    STATUS_FAIL = 'Failed'
    STATUS_STARTED = 'Started'
    
    def __init__(self):
        self.full_list = None
        self.prev_bus_day = acm.FInstrument['ZAR'].Calendar().AdjustBankingDays(acm.Time.DateToday(), -1)
        self.prev_bus_day = time.mktime(datetime.strptime(self.prev_bus_day, "%Y-%m-%d").timetuple())
        self.task_map = {}
        
    def _unsubscribe(self):
        try:
            ael.Task.unsubscribe(ExplorerDialog.task_callb, self)
            ael.TaskHistory.unsubscribe(ExplorerDialog.task_callb, self)
            ael.Task.unsubscribe(ExplorerDialog.task_callb)
            ael.TaskHistory.unsubscribe(ExplorerDialog.task_callb)
        except NameError:
            pass
            
    def _set_subscriber(self):
        self._unsubscribe()
        
        ael.Task.subscribe(ExplorerDialog.task_callb, self)
        ael.TaskHistory.subscribe(ExplorerDialog.task_callb, self)
            
    @staticmethod
    def task_callb(table, ael_obj, arg, operation):
        if table not in (ael.Task, ael.TaskHistory):
            return
        
        if not operation or operation != 'update':
            return
        
        #print "callback on '%s'" % ael_obj, arg, operation
        
        if table == ael.TaskHistory:
            ael_obj = ael_obj.tasknbr
        
        task = acm.FAelTask[ael_obj.name]
        
        arg.update(task)
        
        #arg.refresh()
        
    def HandleDestroy(self):
        self._unsubscribe()
        
    def HandleCancel(self):
        self._unsubscribe()
        return True
        
    def HandleCreate(self, dlg, layout):
        """
        Handle the dialog's create event.
        """
        # general
        self.m_fux_dlg = dlg
        self.m_fux_dlg.Caption("my Explorer")
        
        self.m_list = layout.GetControl('list_tasks')
        
        # inputs
        self.inpt_task_name = layout.GetControl('inpt_task_name')
        self.inpt_module_name = layout.GetControl('inpt_module_name')
        
        # check boxes
        self.chb_show_hist = layout.GetControl('chb_show_hist')
        self.chb_refresh = layout.GetControl('chb_refresh')
        
        # button
        self.btn_refresh = layout.GetControl('btn_refresh')
        
        # option
        self.opt_sort_by = layout.GetControl('opt_sort_by')
        
        # callbacks
        self.m_list.AddCallback("SelectionChanged", self.OnListSelectionChanged, None)
        self.inpt_task_name.AddCallback("Changed", self.OnInptChanged, None)
        self.inpt_module_name.AddCallback("Changed", self.OnInptChanged, None)
        self.m_list.AddCallback("ContextMenu", self.OnTaskContext, None)
        self.m_list.AddCallback("DefaultAction", self.OnTaskDoubleClick, None)
        self.chb_show_hist.AddCallback("Activate", self.OnChbShowHistChecked, None)
        self.chb_refresh.AddCallback("Activate", self.OnChbRefreshChecked, None)
        self.btn_refresh.AddCallback("Activate", self.OnRefresh, None)
        self.opt_sort_by.AddCallback("Changing", self.OnOptionSortByChanged, None)
        
        # ========================
        # setting controls
        self.m_list.Visible(True)
        self.m_list.EnableMultiSelect(True)
        for lst in (self.m_list, ):
            lst.ShowGridLines()
            lst.ShowColumnHeaders()
            lst.EnableHeaderSorting(True)
            
            for ci in range(lst.ColumnCount()):
                lst.AdjustColumnWidthToFitItems(ci)
        
        self.chb_show_hist.Checked(False)
        self.chb_refresh.Checked(False)
        self.opt_sort_by.Visible(False)
        
        self.PopulateData()
        
        for sort_item in self.SORT_ITEMS:
            self.opt_sort_by.AddItem(sort_item)
        self.opt_sort_by.SetData(self.SORT_BY_DEFAULT)
            
        
    def _add_column(self, the_list, col_name, col_desc):
        the_list.RemoveColumn(the_list.ColumnCount() - 1)
        the_list.AddColumn(col_name, -1, col_desc)
        the_list.AddColumn("", -1, "")
        
    def _date_from_time(self, timestamp):
        return datetime.fromtimestamp(timestamp)
        
    def _reset_list(self, the_list):
        the_list.RemoveAllItems()
        for i in range(the_list.ColumnCount()):
            the_list.RemoveColumn(0)
        
        the_list.AddColumn("Task", -1, "Task name")
        the_list.AddColumn("Module", -1, "Module name")
        the_list.AddColumn("Update User", -1, "Last user who update module")
        the_list.AddColumn("Update Time", -1, "Time of last update")
        the_list.AddColumn("", -1, "")
        
    def _fill_list(self, the_list, task_name_like, module_name_like, show_hist=False):
        self._reset_list(the_list)
        
        if show_hist:
            the_list.RemoveColumn(the_list.ColumnCount() - 1)
            the_list.AddColumn("Status", -1, ("Colored are tasks that started "
                "after last buss day and had not succeeded yet."))
            the_list.AddColumn("Start Time", -1, "Last start time")
            the_list.AddColumn("Stop Time", -1, "Last stop time")
            the_list.AddColumn("Duration", -1, "Running time")
            the_list.AddColumn("", -1, "")            
            
        nlist = list(range(the_list.ColumnCount()))
        root_item = the_list.GetRootItem()
        
        if not task_name_like and not module_name_like:
            tasks = acm.FAelTask.Select('')
        else:
            tasks = acm.FAelTask.Select("name like '%s*' and moduleName like '%s*'" % (task_name_like, module_name_like))
        
        self.task_map = {}
        back_col = self.COL_WHITE
        
        for task in sorted(tasks):
            cols = [task.Name(), task.ModuleName(), task.UpdateUser().Name(), str(self._date_from_time(task.UpdateTime()))]
            do_red = False
            is_bold = True
            if show_hist:
                task_hist = self.get_task_hist(task.Name())
                if task_hist:
                    cols.append(task_hist.Status())
                    start_time = str(self._date_from_time(task_hist.StartTime())) 
                    cols.append(start_time)
                    cols.append(str(self._date_from_time(task_hist.StopTime())))
                    diff = task_hist.StopTime() - task_hist.StartTime()
                    
                    back_col = self.COL_WHITE
                    if task_hist.Status() == self.STATUS_FAIL:
                            back_col = self.COL_RED
                    elif task_hist.Status() == self.STATUS_STARTED:
                        back_col = self.COL_ORANGE

                    if task_hist.StartTime() < self.prev_bus_day and task_hist.Status() != self.STATUS_SUCC:
                        is_bold = False
                        back_col = self.COL_GRAY
                            
                    if diff > 0:
                        cols.append(datetime.utcfromtimestamp(diff).strftime("%H:%M:%S"))
                    else:
                        cols.append('')
                else:
                    continue
            cols.append('')
            
            child = root_item.AddChild()
            for cn, ci in zip(cols, nlist):
                child.Label(cn, ci)
            self.task_map[task.Name()] = child

            #if do_red:
                # 4 - refers to column index - Status column
                # 0 - not bold
                # 254 - red color, 42544 - GREEN, 22258 - ORANGE, RED - 8686
                # 30 - not very dark color
            if show_hist:
                child.Style(4, False, 0, back_col)

            child.SetData(task)
            
        for i in range(the_list.ColumnCount()):
            the_list.AdjustColumnWidthToFitItems(i)
            
    def get_task_hist(self, task_name):
        failed_hist = acm.FAelTaskHistory.Select("task='%s'" % task_name)
        if failed_hist:
            latest = max(failed_hist, key=lambda th: th.Oid())
            return latest
            
    def CreateCommand_RunModule(self):
        return MyCommandItem_RunModule()
        
    def CreateCommand_ViewModule(self):
        return MyCommandItem_ViewModule()
    
    def CreateCommand_DeleteTask(self):
        return MyCommandItem_DeleteTask(self)
            
    def AddCustomContextItemsCB(self, passed_arg, menu_builder):
        
        # register our custom commands. 
        menuBuilder = menu_builder.At('menuBuilder')
        
        # itemName, parent, path, tooltiptext, accelerator, mnemonic, callback, is_default
        commands =[
        ['view_mod', '', 'View Module', 'Open in Python Editor', '', '', self.CreateCommand_ViewModule, True],  # True = set as default
        ['run_mod', '', 'Run Module', 'Open empty task of the module', '', '', self.CreateCommand_RunModule, False],
        FUxCore.Separator(),
        ['del_task', '', 'Delete Task', 'Delete all selected tasks', '', '', self.CreateCommand_DeleteTask, False]
        ]
        
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))
        
    def OnTaskContext(self, ud, cd):
        
        #cd contains a dictionary containing a FUxContextMenuBuilder at key 'menuBuilder'
        #For a FUxListControl it also contains an FArray of FUxListItems representing 
        # the selected items at key 'items'
        #For a FUxTreeControl it also contains an FArray of FUxTreeItems representing 
        # the selected items at key 'items'
        #For a FUx2DChartControl it also contains the index of the series being 
        # right clicked at key 'seriesIndex', the index of the point being right clicked 
        # at key 'objectIndex' and the populated object in the point at key 'object'.
        #For a FUxPieChartControl it also contains the index of the sector being 
        # right clicked at key 'sectorIndex' and the populated object in the sector at key 'object'.

        #Get the menu builder and the tree items
        menuBuilder = cd.At('menuBuilder')
        items = cd.At('items')
        
        objects = acm.FArray()
        
        arg_to_pass = None
        
        #Populate an array with the actual data(in this case a FAelTask contained in the FUxListItems
        for item in items:
            objects.Add(item.GetData())
        
        #Build the standard context menu for FVolatilityStructures and add our own menu items in callback
        #AddCustomContextItemsCB
        #If no standard item is needed simply register your commands here. If no own menu items are needed
        #simply ignore the userDefinedCommandsCB and userDefinedArgs parameters.
        #BuildStandardObjectContextMenu makes sure that our custom items will be added at the correct place in
        #the menu. Setting the third argument to False will exclude the 'Delete' command from the menu.
        acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, objects, False, 
            self.AddCustomContextItemsCB, arg_to_pass)
        
        
    def OnTaskContext__(self, cd, data):
        menu_builder = data.At('menuBuilder')
        task = data.At('items')[0].GetData()
        objects = [task]
        
    def PopulateData(self):
        self._fill_list(self.m_list, '', '')
        
    def OnListSelectionChanged(self, cd, data):
        return
        
    def _sort_by(self, sort_by_param=None):
        if not sort_by_param:
            sort_by_param = self.opt_sort_by.GetData()
            
        if sort_by_param == self.SORT_BY_DEFAULT:
            #self.m_list.SortColumn(0, 1)  # 1 - ASC
            return
        elif sort_by_param == self.SORT_BY_UPDAT_TIME:
            self.m_list.SortColumn(3, 2)  # 2 - DESC
        elif sort_by_param == self.SORT_BY_START:
            self.m_list.SortColumn(5, 2)  # 2 - DESC
        elif sort_by_param == self.SORT_BY_STOP:
            self.m_list.SortColumn(6, 2)  # 2 - DESC
        elif sort_by_param == self.SORT_BY_STATUS:
            self.m_list.SortColumn(4, 1)  # 1 - ACS
        
        
    def OnOptionSortByChanged(self, cd, data):
        self._sort_by(self.opt_sort_by.GetData())
        
    def OnChbShowHistChecked(self, cd, data):
        self._visible_on_off()
        self._fill_task_list()
        
    def _visible_on_off(self):
        if self.chb_refresh.Checked():
            self.btn_refresh.Visible(False)
        else:
            self.btn_refresh.Visible(True)
        
        if self.chb_refresh.Checked() and self.chb_show_hist.Checked():
            self.opt_sort_by.Visible(True)
        else:
            self.opt_sort_by.Visible(False)
        
        
    def OnChbRefreshChecked(self, cd, data):
        self._visible_on_off()
        if self.chb_refresh.Checked():
            self._set_subscriber()
        else:
            self._unsubscribe()
        
    def _fill_task_list(self):
        task_name = self.inpt_task_name.GetData()
        module_name = self.inpt_module_name.GetData()
        show_hist = self.chb_show_hist.Checked()
        
        self.m_list.Visible(False)
        self._fill_list(self.m_list, task_name, module_name, show_hist)
        self._sort_by()
        self.m_list.Visible(True)
            
    def OnInptChanged(self, cd, data):
        self._fill_task_list()
        
    def refresh(self):
        #acm.PollDbEvents()
        self._fill_task_list()
        
    def update(self, task):
        list_item = self.task_map.get(task.Name(), None)
        if not list_item:
            self.refresh()
            return
        
        self.set_task_to_lst_item(list_item, task)
        self._sort_by()
        
        for i in range(self.m_list.ColumnCount()):
            self.m_list.AdjustColumnWidthToFitItems(i)
        
    def set_task_to_lst_item(self, list_item, task):
    
        nlist = list(range(self.m_list.ColumnCount()))
        cols = [task.Name(), task.ModuleName(), task.UpdateUser().Name(),
            str(self._date_from_time(task.UpdateTime()))]
        
        
        back_col = self.COL_WHITE
        hist_checked = self.chb_show_hist.Checked()
        if hist_checked:
            task_hist = self.get_task_hist(task.Name())
            if task_hist:
                cols.append(task_hist.Status())
                start_time = str(self._date_from_time(task_hist.StartTime()))
                cols.append(start_time)
                cols.append(str(self._date_from_time(task_hist.StopTime())))
                diff = task_hist.StopTime() - task_hist.StartTime()
                
                back_col = self.COL_WHITE
                if task_hist.Status() == self.STATUS_FAIL:
                    back_col = self.COL_RED
                elif task_hist.Status() == self.STATUS_STARTED:
                    back_col = self.COL_ORANGE

                if task_hist.StartTime() < self.prev_bus_day and task_hist.Status() != self.STATUS_SUCC:
                    back_col = self.COL_GRAY
        
                if diff > 0:
                    cols.append(datetime.utcfromtimestamp(diff).strftime("%H:%M:%S"))
                else:
                    cols.append('')

        cols.append('')
        
        for cn, ci in zip(cols, nlist):
            list_item.Label(cn, ci)
        #self.task_map[task.Name()] = child

        #if do_red:
            # 4 - refers to column index - Status column
            # 0 - not bold
            # 254 - red color
            # 30 - not very dark color
        if hist_checked:
            list_item.Style(4, 0, 0, back_col)
        
    def OnRefresh(self, cd, data):
        self.refresh()
        
    def OnTaskDoubleClick(self, cd, data):
        item = self.m_list.GetSelectedItem()
        task = item.GetData()
        acm.StartRunScript(task, None)
        
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('EtchedIn', 'Filter Task', 'vertbox1')
        b.    BeginHorzBox('None')
        b.      AddInput('inpt_task_name', 'Task:', 25, 25)
        b.      AddSpace(30)
        b.      AddInput('inpt_module_name', 'Module:', 25, 25)
        b.      AddFill()
        b.      AddCheckbox('chb_refresh', 'Refresh Automatically?')
        b.      AddOption('opt_sort_by', 'Fixed Sort by:', 20, 20)
        b.      AddButton('btn_refresh', 'Refresh')
        b.      AddSpace(50)
        b.      AddCheckbox('chb_show_hist', 'Show History Status?')
        b.    EndBox()
        b.  EndBox()
        b.    AddList('list_tasks', 21, -1, 157, -1)
        b.EndBox()
        return b


        
def standalone_launch():
    shell = acm.UX().SessionManager().Shell()
    dialog = ExplorerDialog()
    builder = dialog.CreateLayout()
    acm.UX().Dialogs().ShowCustomDialog(shell, builder, dialog)

#standalone_launch()
