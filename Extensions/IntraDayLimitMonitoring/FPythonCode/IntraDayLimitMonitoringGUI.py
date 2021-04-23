
import acm
import ael
import operator
import FUxCore

import IntraDayLimitMonitoring as limits
import IntraDayLimitMonitoringSetup as setup
 
log = limits.log 

def ReallyStartDialog(shell, count):
    builder = CreateMainLayout()
    customDlg = IntraDayLimitMonitoringCustomDialog()
    customDlg.m_count = count
    customDlg.m_shell = shell
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg)

def StartDialog(eii):
    if acm.User().UserGroup().Name() in ('Market Risk', 'IT BTB', 'IT RTB'):
        shell = eii.ExtensionObject().Shell()    
        ReallyStartDialog(shell, 0);
    else:
        print 'You do not have the right to open this window - need to be in user group Market Risk/IT BTB/IT RTB'

def StartDialogFromScript():
    shell = acm.UX().SessionManager().Shell()
    ReallyStartDialog(shell, 0)

def CreateMainLayout():
    b = acm.FUxLayoutBuilder()
    # Bottom Layout
    b.  BeginHorzBox('None')
    b.    AddFill()
    b.    AddButton('ok', 'OK')
    b.    AddButton('cancel', 'Cancel')
    b.  EndBox()
    return b

def StartColumnDialog(shell, selected_column=None):
    dlg = IntraDayLimitMonitoringColumnDialog()
    dlg.InitControls()
    dlg.m_shell = shell
    dlg.m_selected_column = selected_column
    log(acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg))

def StartDeskDialog(shell, selected_desk=None):
    dlg = IntraDayLimitMonitoringDeskDialog()
    dlg.InitControls()
    dlg.m_shell = shell
    dlg.m_selected_desk = selected_desk
    log(acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg))

def StartLimitDialog(shell, call_back):
    dlg = IntraDayLimitMonitoringLimitDialog()
    dlg.InitControls()
    dlg.m_shell = shell
    dlg.m_call_back = call_back
    log(acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg))



class IntraDayLimitMonitoringCustomDialog(FUxCore.LayoutTabbedDialog):

    def __init__(self):        
        # Main dialog
        self.m_fuxDlg = 0
        self.m_information = 0
        self.m_informationText = 'Configure Intra Day Limit Monitoring'

    def OnSetupClicked(self, arg1, arg2):
        log('Setup')
        setup.setup()
        self.PopulateData()        
        
    def OnCleanupClicked(self, arg1, arg2):
        log('Cleanup')
        setup.cleanup()
        self.PopulateData()        
                 
    def OnImportClicked(self, arg1, arg2):
        log('import')
        setup.importTextObject(self.m_file_name.GetData())

    def OnExportClicked(self, arg1, arg2):
        log('Export')
        setup.exportTextObject(self.m_file_name.GetData())
        
    def OnImportDesksClicked(self, arg1, arg2):
        log('Import Desks')
        setup.importDesks(self.m_fileNameDesks.GetData())
        self.PopulateDesks()
        self.PopulateLimits()
        
    def OnExportDesksClicked(self, arg1, arg2):
        log('Export Desks')
        setup.exportDesks(self.m_fileNameDesks.GetData())
        
    def OnImportLimitsClicked(self, arg1, arg2):
        log('Import Limits')
        setup.importLimits(self.m_fileNameLimits.GetData())
        self.PopulateDesks()
        self.PopulateLimits()
        

    def OnExportLimitsClicked(self, arg1, arg2):
        log('Export Limits')
        setup.exportLimits(self.m_fileNameLimits.GetData())
        
    def OnTasksVsDesksClicked(self, arg1, arg2):
        log('Check Tasks vs Desks')
        setup.checkTasksVsDesks()
        
        
        


    def HandleApply(self):
        return ""
    
    def DeleteColumns(self, arg1, arg2):
        log('DeleteColumns')
        choiceList = acm.FChoiceList[limits.choiceListName]
        data = limits.getData()
        columns = data.columns
        items = self.m_columns.GetSelectedItems()   
        for item in items:
            log('Deleting column %s' % item.GetData().column_name)
            del columns[item.GetData().column_name]
            if choiceList: 
                for c in choiceList.Choices().AsList():
                    if c.Name() == item.GetData().column_name:
                        log('Deleting Choice %s' % c.Name())
                        c.Delete()

        limits.persistData(data)           
        self.PopulateColumns()        
            
    def AddColumns(self, arg1, arg2):
        log('AddColumns')
        StartColumnDialog(self.m_shell)
        self.PopulateColumns()        

    def EditColumns(self, arg1, arg2):
        log('EditColumns')
        if self.m_columns.GetSelectedItem():     
            StartColumnDialog(self.m_shell, self.m_columns.GetSelectedItem())
            self.PopulateColumns()        

    def DeleteTimeSeries(self, arg1, arg2):
        log('DeleteTimeSeries')
        items = self.m_timeSeries.GetSelectedItems()                
        for item in items:
            item.GetData().Delete()
        self.PopulateTimeSeries()        

    def RefreshTimeSeries(self, arg1, arg2):
        log('RefreshTimeSeries')
        self.PopulateTimeSeries()        

    def AddDesk(self, arg1, arg2):
        log('AddDesk')
        StartDeskDialog(self.m_shell)
        self.PopulateDesks()
        self.PopulateLimits()

    def EditDesk(self, arg1, arg2):
        log('EditDesk')    
        if self.m_desks.GetSelectedItem():     
            StartDeskDialog(self.m_shell, self.m_desks.GetSelectedItem())
            self.PopulateDesks()
            self.PopulateLimits()        

    def DeleteDesks(self, arg1, arg2):
        log('DeleteDesks')
        data = limits.getData()
        desks = data.desks
        items = self.m_desks.GetSelectedItems()   
        for item in items:
            log('Deleting desk %s' % item.GetData().desk_name)
            del desks[item.GetData().desk_name]

        limits.persistData(data)             
        self.PopulateData()        

    def EditLimit(self, arg1, arg2):
        log('EditLimit')
        StartLimitDialog(self.m_shell, self.PopulateLimits)
        self.PopulateLimits()

    def PopulateColumns(self):
        self.m_columns.RemoveAllItems()
        ael.poll()
        rootItem = self.m_columns.GetRootItem()        

        data = limits.getData()
        if data:
            columns = data.columns
            for column in (sorted(columns.values(), key=operator.attrgetter('report_order'))):
            #for key in sorted(columns.iterkeys()):
                #column = columns[key]                     
                child = rootItem.AddChild()
                child.Label(column.column_name, 0)
                child.Label(column.column_id, 1)
                child.Label(column.column_label, 2)
                child.Label(column.__class__.__name__, 3)
                
                if isinstance(column, limits.StandardColumn):
                    child.Label(None, 4)
                    child.Label(None, 5)
                       
                if isinstance(column, limits.TimeBucketColumn):
                    child.Label(column.bucket, 4)
                    child.Label(None, 5)
                     
                if isinstance(column, limits.VectorColumn):
                    child.Label(column.vector_value, 4)
                    child.Label(column.vector_type, 5)
                
                child.Label(column.report_order, 6)
                child.Label(column.active, 7)
                child.SetData(column)
                
                
            self.m_columns.AdjustColumnWidthToFitItems(0)
            self.m_columns.AdjustColumnWidthToFitItems(1)
            self.m_columns.AdjustColumnWidthToFitItems(2)
            self.m_columns.AdjustColumnWidthToFitItems(3)
            self.m_columns.AdjustColumnWidthToFitItems(4)
            self.m_columns.AdjustColumnWidthToFitItems(5)
            self.m_columns.AdjustColumnWidthToFitItems(6)
            self.m_columns.AdjustColumnWidthToFitItems(7)

    def PopulateTimeSeries(self):
        self.m_timeSeries.RemoveAllItems()
        ael.poll()
        rootItem = self.m_timeSeries.GetRootItem()        

        spec = limits.getTimeSeriesSpec()
        if spec:
            tss = spec.TimeSeriesDv()
            for ts in tss:            
                portfolio = acm.FPhysicalPortfolio.Select('oid = %s' % ts.RecordAddress1())[0]
                choiceLists = acm.FChoiceList.Select('oid = %s' % ts.RecordAddress2())                
                child = rootItem.AddChild()
                child.Label(ts.StorageDate(), 0)
                child.Label(portfolio.Name(), 1)
                if len(choiceLists) > 0:
                    child.Label(choiceLists[0].Name(), 2)
                else:
                    child.Label('NOT FOUND', 2)
                child.Label(ts.DvValue(), 3)
                if ts.DvCurrency():
                    child.Label(ts.DvCurrency().Name(), 4)                
                else:
                    child.Label('None', 4)                
                child.Label(ts.DvDate(), 5)
                child.Label(acm.Time.DateTimeFromTime(ts.UpdateTime()), 6)                
                child.Label(ts.UpdateUser(), 7)                
                child.SetData(ts)
                           
            self.m_timeSeries.AdjustColumnWidthToFitItems(0)
            self.m_timeSeries.AdjustColumnWidthToFitItems(1)
            self.m_timeSeries.AdjustColumnWidthToFitItems(2)
            self.m_timeSeries.AdjustColumnWidthToFitItems(3)
            self.m_timeSeries.AdjustColumnWidthToFitItems(4)
            self.m_timeSeries.AdjustColumnWidthToFitItems(5)
            self.m_timeSeries.AdjustColumnWidthToFitItems(6)
            self.m_timeSeries.AdjustColumnWidthToFitItems(7)
                        
    def PopulateDesks(self):
        log('PopulateDesks')
        self.m_desks.RemoveAllItems()
        ael.poll()        
        rootItem = self.m_desks.GetRootItem()        

        data = limits.getData()
        if data:    
            desks = data.desks
            for key in sorted(desks.iterkeys()):
                desk = desks[key]            
                desk.portfolio_names.sort()
                child = rootItem.AddChild()
                child.Label(desk.desk_name, 0)
                child.Label(str(desk.portfolio_names), 1)
                child.SetData(desk)
                           
            self.m_desks.AdjustColumnWidthToFitItems(0)
            self.m_desks.AdjustColumnWidthToFitItems(1)
        
    def PopulateLimits(self):
        log('PopulateLimits')
        self.m_limits.RemoveAllItems()
        ael.poll()        
        rootItem = self.m_limits.GetRootItem()        

        data = limits.getData()
        if data:
            columns = data.columns
            sorted_columns = (sorted(columns.values(), key=operator.attrgetter('report_order')))
            if data:    
                desks = data.desks
                for key in sorted(desks.iterkeys()):
                    desk = desks[key]                     
                    desk.portfolio_names.sort()
                    child = rootItem.AddChild()
                    child.Label(desk.desk_name, 0)
                    for idx, column in enumerate(sorted_columns):
                        if column.column_name in desk.limits:
                            limit = desk.limits[column.column_name]
                            child.Label(limit.limit_value, idx + 1)                        
                    child.SetData(desk)
                               
                self.m_limits.AdjustColumnWidthToFitItems(0)
                for idx, column in enumerate(sorted_columns):
                    self.m_limits.AdjustColumnWidthToFitItems(idx + 1)
                        
    def PopulateData(self):
        log('Populate')
        
        self.m_information.SetData(self.m_informationText)

        self.PopulateColumns()
        self.PopulateDesks()
        self.PopulateLimits()
    
    def HandleCreate(self, dlg, layout):        
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Intra Day Limit Monitoring')
        
        # TopLayout
        topBuilder = acm.FUxLayoutBuilder()
        topBuilder.BeginVertBox('None')
        topBuilder.    AddLabel('BasicInfo', 'Basic Information')
        topBuilder.    AddText('information', 10, 80, 70, -1);
        topBuilder.EndBox()
        
        topLayout = dlg.AddTopLayout("Top", topBuilder)        
        self.m_information = topLayout.GetControl("information")
                
        # Columns
        c = acm.FUxLayoutBuilder()
        
        c.BeginVertBox('None')
        c.  BeginHorzBox('EtchedIn', None)
        c.    AddList("columns", 10, 80, 70, -1)
        c.  EndBox()     
        c.  BeginHorzBox('EtchedIn', None)
        c.    AddButton('addColumns', 'Add')
        #c.    AddButton('editColumns', 'Edit')
        c.    AddButton('deleteColumns', 'Delete')
        c.  EndBox()        
        c.EndBox()

        columnsLayout = dlg.AddPane("Columns", c) 
               
        self.m_columns = columnsLayout.GetControl('columns')
        self.m_deleteColumnsBtn = columnsLayout.GetControl("deleteColumns")
        self.m_deleteColumnsBtn.AddCallback("Activate", self.DeleteColumns, self)        
        self.m_addColumnsBtn = columnsLayout.GetControl("addColumns")
        self.m_addColumnsBtn.AddCallback("Activate", self.AddColumns, self)        
        #self.m_editColumnsBtn = columnsLayout.GetControl("editColumns")
        #self.m_editColumnsBtn.AddCallback("Activate", self.EditColumns, self)        
        
        
        self.m_columns.ShowGridLines()
        self.m_columns.EnableMultiSelect()        
        self.m_columns.ShowColumnHeaders()
        self.m_columns.AddColumn('ColumnName', -1, "Choice List Item Name")
        self.m_columns.AddColumn('ColumnId', -1, "Column Id")               
        self.m_columns.AddColumn('ColumnLabel', -1, "ColumnLabel")               
        self.m_columns.AddColumn('Class', -1, "Column Type")               
        self.m_columns.AddColumn('Parameter', -1, "Parameter for the specific Class")                        
        self.m_columns.AddColumn('Type', -1, "Parameter Type")                        
        self.m_columns.AddColumn('ReportOrder', -1, "Report Order")                        
        self.m_columns.AddColumn('Active', -1, "Active")                        

        # Desks
        d = acm.FUxLayoutBuilder()
        
        d.BeginVertBox('None')
        d.  BeginHorzBox('EtchedIn', None)
        d.    AddList("desks", 10, 80, 70, -1)
        d.  EndBox()     
        d.  BeginHorzBox('EtchedIn', None)
        d.    AddButton('addDesk', 'Add')
        d.    AddButton('editDesk', 'Edit')
        d.    AddButton('deleteDesks', 'Delete')
        d.  EndBox()        
        d.EndBox()

        desksLayout = dlg.AddPane("Desks", d) 
               
        self.m_addDeskBtn = desksLayout.GetControl("addDesk")
        self.m_addDeskBtn.AddCallback("Activate", self.AddDesk, self)        
        self.m_editDeskBtn = desksLayout.GetControl("editDesk")
        self.m_editDeskBtn.AddCallback("Activate", self.EditDesk, self)        
        self.m_deleteDeskBtn = desksLayout.GetControl("deleteDesks")
        self.m_deleteDeskBtn.AddCallback("Activate", self.DeleteDesks, self)        
        
        self.m_desks = desksLayout.GetControl('desks')
        self.m_desks.ShowGridLines()
        self.m_desks.EnableMultiSelect()        
        self.m_desks.ShowColumnHeaders()
        self.m_desks.AddColumn('DeskName', -1)
        self.m_desks.AddColumn('Portfolios', -1)

        # Limits
        l = acm.FUxLayoutBuilder()
        
        l.BeginVertBox('None')
        l.  BeginHorzBox('EtchedIn', None)
        l.    AddList("limits", 10, 80, 70, -1)
        l.  EndBox()     
        l.  BeginHorzBox('EtchedIn', None)
        l.    AddButton('editLimit', 'Edit')
        l.  EndBox()        
        l.EndBox()

        limitLayout = dlg.AddPane("Limits", l) 
        self.m_editLimitBtn = limitLayout.GetControl("editLimit")
        self.m_editLimitBtn.AddCallback("Activate", self.EditLimit, self)        

        self.m_limits = limitLayout.GetControl('limits')
        self.m_limits.ShowGridLines()
        self.m_limits.EnableMultiSelect()        
        self.m_limits.ShowColumnHeaders()
        self.m_limits.AddColumn('DeskName', -1)
        data = limits.getData()
        if data:
            columns = data.columns
            sorted_columns = (sorted(columns.values(), key=operator.attrgetter('report_order')))
            for idx, column in enumerate(sorted_columns):
                self.m_limits.AddColumn(column.column_name, -1)


        # Time Series
        ts = acm.FUxLayoutBuilder()
        
        ts.BeginVertBox('None')
        ts.  BeginHorzBox('EtchedIn', None)
        ts.    AddList("timeseries", 10, 80, 70, -1)
        ts.  EndBox()     
        ts.  BeginHorzBox('EtchedIn', None)
        ts.    AddButton('deleteTimeSeries', 'Delete')
        ts.    AddButton('refreshTimeSeries', 'Refresh')
        ts.  EndBox()        
        ts.EndBox()

        timeSeriesLayout = dlg.AddPane("Time Series", ts) 
               
        self.m_deleteTimeSeriesBtn = timeSeriesLayout.GetControl("deleteTimeSeries")
        self.m_deleteTimeSeriesBtn .AddCallback("Activate", self.DeleteTimeSeries, self)        
        self.m_refreshTimeSeriesBtn = timeSeriesLayout.GetControl("refreshTimeSeries")
        self.m_refreshTimeSeriesBtn .AddCallback("Activate", self.RefreshTimeSeries, self)        
        
        self.m_timeSeries = timeSeriesLayout.GetControl('timeseries')
        self.m_timeSeries.ShowGridLines()
        self.m_timeSeries.EnableMultiSelect()        
        self.m_timeSeries.ShowColumnHeaders()
        self.m_timeSeries.AddColumn('StorageDate', -1)
        self.m_timeSeries.AddColumn('Portfolio', -1)
        self.m_timeSeries.AddColumn('Column', -1)               
        self.m_timeSeries.AddColumn('Value', -1)               
        self.m_timeSeries.AddColumn('Currency', -1)                        
        self.m_timeSeries.AddColumn('Date', -1,)               
        self.m_timeSeries.AddColumn('UpdateTime', -1)                        
        self.m_timeSeries.AddColumn('UpdateUser', -1)                        
        
        # Setup
        s = acm.FUxLayoutBuilder()
        
        s.BeginVertBox('None')
        s.  BeginVertBox('EtchedIn', 'Text Object')
        s.   BeginHorzBox('None', 'None')
        s.     AddInput('file_name', 'File Name')
        s.   EndBox()        
        s.   BeginHorzBox('None', 'None')
        s.     AddButton('import', 'Import')
        s.     AddButton('export', 'Export')
        s.   EndBox()  
        s.  EndBox()   
        s.  BeginVertBox('EtchedIn', 'Desks')
        s.    BeginHorzBox('None', 'None')
        s.      AddInput('file_name_desks', 'File Name')
        s.    EndBox()      
        s.    BeginHorzBox('None', 'None')
        s.      AddButton('import_desks', 'Import')
        s.      AddButton('export_desks', 'Export')
        s.    EndBox()      
        s.  EndBox()
        s.  BeginVertBox('EtchedIn', 'Limits')
        s.    BeginHorzBox('None', 'None')
        s.      AddInput('file_name_limits', 'File Name')
        s.    EndBox()      
        s.    BeginHorzBox('None', 'None')
        s.      AddButton('import_limits', 'Import')
        s.      AddButton('export_limits', 'Export')
        s.    EndBox()      
        s.  EndBox()
        s.  BeginVertBox('EtchedIn', 'Check Tasks vs Desks')
        s.    BeginHorzBox('None', 'None')
        s.      AddButton('check_tasks_desks', 'Check')
        s.    EndBox()      
        s.  EndBox()
        s.   BeginHorzBox('EtchedIn', 'Setup')
        s.     AddButton('setup', 'Setup')
        s.     AddButton('cleanup', 'Cleanup')
        s.   EndBox()        
             
        s.EndBox()
        
        configLayout = None        
        # Comment out the line below to remove Setup tab
        configLayout = dlg.AddPane("Setup", s) 

        if configLayout:              
            self.m_setupBtn = configLayout.GetControl("setup")
            self.m_setupBtn.AddCallback("Activate", self.OnSetupClicked, self)        
            self.m_cleanupBtn = configLayout.GetControl("cleanup")
            self.m_cleanupBtn.AddCallback("Activate", self.OnCleanupClicked, self)   
            self.m_importBtn = configLayout.GetControl("import")
            self.m_importBtn.AddCallback("Activate", self.OnImportClicked, self)   
            self.m_exportBtn = configLayout.GetControl("export")
            self.m_exportBtn.AddCallback("Activate", self.OnExportClicked, self)  
            
            
            self.m_importDesksBtn = configLayout.GetControl("import_desks")
            self.m_importDesksBtn.AddCallback("Activate", self.OnImportDesksClicked, self) 
            self.m_exportDesksBtn = configLayout.GetControl("export_desks")
            self.m_exportDesksBtn.AddCallback("Activate", self.OnExportDesksClicked, self)   
            
            self.m_importLimitsBtn = configLayout.GetControl("import_limits")
            self.m_importLimitsBtn.AddCallback("Activate", self.OnImportLimitsClicked, self)   
            self.m_exportLimitsBtn = configLayout.GetControl("export_limits")
            self.m_exportLimitsBtn.AddCallback("Activate", self.OnExportLimitsClicked, self)
            
            self.m_checkTasksDesksBtn = configLayout.GetControl("check_tasks_desks")
            self.m_checkTasksDesksBtn.AddCallback("Activate", self.OnTasksVsDesksClicked, self)   
            
            
            if acm.User().UserGroup().Name() not in ('IT BTB', 'IT RTB'):
                self.m_setupBtn.Enabled(False)
                self.m_cleanupBtn.Enabled(False)
                self.m_importBtn.Enabled(False)
                self.m_exportBtn.Enabled(False)
                
            

            self.m_file_name = configLayout.GetControl("file_name")
            self.m_file_name.SetData("C:\\temp\\IntraDayLimitMonitoringTextObject.txt")
            
            self.m_fileNameDesks = configLayout.GetControl("file_name_desks")
            self.m_fileNameDesks.SetData(r"C:\temp\Desks.csv")
            self.m_fileNameLimits = configLayout.GetControl("file_name_limits")
            self.m_fileNameLimits.SetData(r"C:\temp\Limits.csv")
        

        # Populate 
        self.PopulateData()

class IntraDayLimitMonitoringColumnDialog(FUxCore.LayoutDialog):
    def __init__(self):
        self.m_bindings = None
        self.m_okBtn = None
        
    def HandleApply(self):     
        msg = ""
        column_name = self.m_column_name.GetData()
        column_label = self.m_column_label.GetData()
        parameter = self.m_parameter.GetData()
        vectorType = self.m_typeCtrl.GetValue()
        column_class = self.m_classCtrl.GetValue()
        report_order = self.m_report_order.GetData()
        active = self.m_active.GetData()
        
        data = limits.getData()
        columns = data.columns
        if not column_name:
            msg += "Must specify column name\n"
        if columns.has_key(column_name):
            msg += "Column Name already exists\n"

        if not column_class:
            msg += "Must specify a Class\n"

        if self.m_column.GetData() == None:
            msg += "Must specify a column\n"
        
        if msg != "":
            acm.UX().Dialogs().MessageBoxInformation(self.m_shell, msg)
            return 
        
        column_id = self.m_column.GetData().Name()
        
        choiceListExists = False
        for c in acm.FChoiceList[limits.choiceListName].Choices():
            if c.Name() == column_name:
                choiceListExists = True
        if not choiceListExists:
            log("Creating ChoiceList %s" % column_name)
            cl = acm.FChoiceList()
            cl.Name = column_name
            cl.List = limits.choiceListName
            cl.Commit()
        else:
            log("ChoiceList %s already exists" % column_name)
        
        column = None
        if column_class == 'StandardColumn':
            column = limits.StandardColumn(column_name, column_id, column_label, report_order, active)
        if column_class == 'TimeBucketColumn':
            column = limits.TimeBucketColumn(column_name, column_id, column_label, report_order, active, parameter)
        if column_class == 'VectorColumn':
            column = limits.VectorColumn(column_name, column_id, column_label, report_order, active, vectorType, parameter)

        if column:
            columns[column.column_name] = column
            limits.persistData(data)        
        
        return ""
        
    def UpdateControls(self):
        pass
        
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Add Custom Column')
        
        self.m_column_name = layout.GetControl("column_name")        
        self.m_column = layout.GetControl("columnCtrl")        
        self.m_column_label = layout.GetControl("column_label")        
        self.m_parameter = layout.GetControl("parameter")        
        self.m_report_order = layout.GetControl("reportOrder")        
        self.m_active = layout.GetControl("active")        

        if self.m_selected_column:
            self.m_fuxDlg.Caption('Edit Custom Column')
            
            self.m_column_name.SetData(self.m_selected_column.GetData().column_name)
            self.m_column_label.SetData(self.m_selected_column.GetData().column_label)            
            self.m_report_order.SetData(self.m_selected_column.GetData().report_order)            
            self.m_active.SetData(self.m_selected_column.GetData().active)            

            if isinstance(self.m_selected_column.GetData(), limits.StandardColumn):
                self.m_classCtrl.SetValue('StandardColumn')
                pass
            if isinstance(self.m_selected_column.GetData(), limits.TimeBucketColumn):
                pass
            if isinstance(self.m_selected_column.GetData(), limits.VectorColumn):
                pass
        
        self.m_okBtn = layout.GetControl("ok")
        self.m_bindings.AddLayout(layout)
        self.UpdateControls()
        
    def InitControls(self):        
        classes = ['StandardColumn', 'TimeBucketColumn', 'VectorColumn']
        types = ['Currency', 'YieldCurve']
        columns = limits.getColumnList()
                
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)
        
        self.m_columnCtrl = self.m_bindings.AddBinder('columnCtrl', acm.GetDomain('string'), None, columns)
        self.m_classCtrl = self.m_bindings.AddBinder('classCtrl', acm.GetDomain('string'), None, classes)
        self.m_typeCtrl = self.m_bindings.AddBinder('typeCtrl', acm.GetDomain('string'), None, types)
                
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddInput('column_name', 'ColumnName')
        self.m_columnCtrl.BuildLayoutPart(b, 'Column')
        b.  AddInput('column_label', 'ColumnLabel')
        self.m_classCtrl.BuildLayoutPart(b, 'Class')
        b.  AddInput('parameter', 'Parameter')
        self.m_typeCtrl.BuildLayoutPart(b, 'Type')
        b.  AddInput('reportOrder', 'ReportOrder')
        b.  AddInput('active', 'Active')
        b.  BeginHorzBox('None')
        b.    AddSpace(50)
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b

class IntraDayLimitMonitoringDeskDialog(FUxCore.LayoutDialog):
    def __init__(self):
        self.m_bindings = None
        self.m_okBtn = None
        
    def HandleApply(self):
        desk_name = self.m_desk_name.GetData()
                
        portfolio_names = []
        for item in self.m_portfolios.GetCheckedItems():
            portfolio_names.append(item.GetData())
        
        desk = limits.Desk(desk_name, portfolio_names)
        desk.portfolio_names = portfolio_names
        
        data = limits.getData()
        data.desks[desk_name] = desk
        
        limits.persistData(data)
                
        return ""
        
    def UpdateControls(self):
        pass
        
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Add Desk')
        
        self.m_desk_name = layout.GetControl("desk_name")        

        if self.m_selected_desk:
            self.m_fuxDlg.Caption('Edit Desk')
            self.m_desk_name.SetData(self.m_selected_desk.GetData().desk_name)

        self.m_portfolios = layout.GetControl('portfolios')
        
        self.m_portfolios.RemoveAllItems()
        rootItem = self.m_portfolios.GetRootItem()        

        portfolios = acm.FPhysicalPortfolio.Select('')
        portfolio_names = [p.Name() for p in portfolios]
        portfolio_names.sort()

        self.m_portfolios.ShowGridLines()
        self.m_portfolios.EnableMultiSelect()        
        self.m_portfolios.ShowColumnHeaders()   
        self.m_portfolios.ShowCheckboxes()
            
        for portfolio_name in portfolio_names:
            child = rootItem.AddChild()
            child.Label(portfolio_name, 0)
            child.SetData(portfolio_name)            
            if self.m_selected_desk and portfolio_name in self.m_selected_desk.GetData().portfolio_names:
                child.Check(True)
                
                       
        self.m_portfolios.AdjustColumnWidthToFitItems(0)
        self.m_portfolios.AdjustColumnWidthToFitItems(1)
            
        self.m_portfolios.AddColumn('Portfolio Name', -1)
                        
        self.m_bindings.AddLayout(layout)
        self.UpdateControls()
        
    def InitControls(self):                                        
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)
                        
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddInput('desk_name', 'DeskName')
        b.  BeginVertBox('EtchedIn', 'Portfolios')
        b.    AddList("portfolios", 10, 80, 70, -1)
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddSpace(50)
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b


class IntraDayLimitMonitoringLimitDialog(FUxCore.LayoutDialog):
    def __init__(self):
        self.m_bindings = None
        self.m_okBtn = None
        
    def HandleApply(self):
        msg = ""
        data = limits.getData()

        desk_value = self.m_deskCtrl.GetValue()
        column_value = self.m_columnCtrl.GetValue()
        limit_value = self.m_limit.GetData()
        
        if not desk_value:
            msg += "Must specify a desk\n"
        if not column_value:
            msg += "Must specify a column\n"
        
        if msg != "":
            acm.UX().Dialogs().MessageBoxInformation(self.m_shell, msg)
            return 
        
        desk = data.desks[desk_value]
        if limit_value:
            limit = limits.Limit(column_value, limit_value)
            desk.limits[column_value] = limit
        else:
            del desk.limits[column_value]
                
        limits.persistData(data)
        self.m_call_back()
        
    def UpdateControls(self):
        pass
        
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Add Limit')
        
        self.m_limit = layout.GetControl("limit")        
                        
        self.m_bindings.AddLayout(layout)
        self.UpdateControls()
        
    def InitControls(self):                                        
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)

        data = limits.getData()
        columns = data.columns.keys()
        desks = data.desks.keys()
        
        self.m_deskCtrl = self.m_bindings.AddBinder('deskCtrl', acm.GetDomain('string'), None, desks)
        self.m_columnCtrl = self.m_bindings.AddBinder('columnCtrl', acm.GetDomain('string'), None, columns)

                        
                        
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        self.m_deskCtrl.BuildLayoutPart(b, 'Desk')
        self.m_columnCtrl.BuildLayoutPart(b, 'Column')
        b.  AddInput('limit', 'Limit')
        b.  BeginHorzBox('None')
        b.    AddSpace(50)
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b

