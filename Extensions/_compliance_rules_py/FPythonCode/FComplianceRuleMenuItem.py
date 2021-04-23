""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FComplianceRuleMenuItem.py"
"""--------------------------------------------------------------------------
MODULE
    FComplianceRuleMenuItem

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    A collection of classes and functions related to compliance rule menus.
    
-----------------------------------------------------------------------------"""
from contextlib import contextmanager

import acm
import FUxCore
import FRunScriptGUI
import FComplianceCheck
import FComplianceRulesUtils
import FSheetUtils
import FGrouperUtils
from ACMPyUtils import Transaction

VIEW_ALERTS_PANEL_CREATE = 'ViewAlertsPanelCreateDockWindow'
VIEW_ALERTS_PANEL = 'ViewAlertsPanelDockWindow'

#------------------------------------------------------------------------------
# Helper functions
#------------------------------------------------------------------------------

def GetAlerts(rowObjects):
    alerts = []    
    rules = []
    if rowObjects is None:
        return alerts
    for rowObject in rowObjects:
        if rowObject.IsKindOf(acm.FCustomMultiItem):
            rules.extend(rowObject.Objects())
        elif rowObject.IsKindOf(acm.FASQLQueryFolder):
            rules.extend(rowObject.Query().Select())
        elif rowObject.IsKindOf(acm.FItemsFolder):
            rules.extend(rowObject.Items())
        else:
            rules.append(rowObject)
    
    for rule in rules:
        for ar in rule.AppliedRules():
            alerts.extend(ar.Alerts())
    return alerts

def ViewRule(alert, eii):
    if alert and alert.IsKindOf(acm.FAlert):
        acm.StartApplication('Compliance Rule Editor', alert.AppliedRule().ComplianceRule())
    else:
        gui = acm.FBusinessLogicGUIShell()
        gui.SetFUxShell(eii.Shell())
        acm.StartApplication('Compliance Rule Editor', acm.EditableObject.New('Compliance Rule', gui))

def ViewRuleDoubleClick(eii):
    cell = eii.Parameter('sheet').Selection().SelectedCell()
    if cell and cell.RowObject() and cell.RowObject().Class() == acm.FComplianceRule:
        acm.StartApplication('Compliance Rule Editor', cell.RowObject())
    elif cell and cell.RowObject() and cell.RowObject().Class() == acm.FAlert:
        acm.StartApplication('Compliance Rule Editor', cell.RowObject().AppliedRule().ComplianceRule())
        
def StartCommonObjectApplication(commonObject):
    app = acm.GetDefaultApplication(commonObject.Class())
    if app:
        acm.StartApplication(app, commonObject)

def SelectedObjectFromExtensionInvokationInfo(eii, cls):
    activeSheet = eii.Parameter('sheet')
    cell = activeSheet.Selection().SelectedCell()
    if cell and cell.RowObject() and cell.RowObject().Class() == cls:
       return cell.RowObject()

def ViewAlerts(eii):
    frame = eii.ExtensionObject()
    sheet = eii.Parameter('sheet')
    selectedObjects = sheet.Selection().SelectedRowObjects()
    alerts = GetAlerts(selectedObjects)
    
    dockWindow = frame.GetCustomDockWindow(VIEW_ALERTS_PANEL)
    if not dockWindow:
        dockWindow = frame.CreateRegisteredDockWindow(VIEW_ALERTS_PANEL_CREATE, VIEW_ALERTS_PANEL, 'View Alerts', 'Bottom')
        
    alertPanel = dockWindow.CustomLayoutPanel()
    if alerts:
        alertPanel.InsertAlerts(alerts)

def InspectRule(appliedRule, alert=None):   
    interface = FComplianceRulesUtils.RuleInterface(appliedRule.ComplianceRule())
    try:
        interface().OnDetails(appliedRule, alert)
    except AttributeError: # OnDetails not implemented for interface
        if alert:
            StartCommonObjectApplication(alert.Subject())
        else:
            msg = 'Inspect is not implemented for rule type {0}'.format(appliedRule.ComplianceRule().DefinitionInfo())
            FComplianceRulesUtils.logger.info(msg)

#------------------------------------------------------------------------------
# Menu item classes
#------------------------------------------------------------------------------

class CreateAddSheetMenuItem(FUxCore.MenuItem):

    def __init__(self, extObj, sheet):
        self._app = extObj
        self._sheet = sheet
           
    def Invoke(self, eii):
        self.AddSheet(self._sheet)
    
    def AddSheet(self, sheetType):
        workbook = self._app.ActiveWorkbook()
        workbook.NewSheet(sheetType)


class AlertMenuItem(FUxCore.MenuItem):

    def __init__(self, extObj, invokeFunc=None, enabledFunc=None, validateFunc=None):
        self._extObj = extObj
        self._invokeFunc = invokeFunc
        self._enabledFunc = enabledFunc
        self._validateFunc = validateFunc
    
    def Enabled(self):
        if callable(self._enabledFunc):
            return self._enabledFunc(self._SelectedAlerts())
        return bool(self._SelectedAlerts())

    def Invoke(self, _eii):
        if callable(self._invokeFunc):
            self._invokeFunc(self._SelectedAlert())
        
    def _SelectedAlerts(self):
        alerts = []
        activeSheet = self._extObj.ActiveSheet()
        if activeSheet:
            selection = activeSheet.Selection()
            if selection:
                alerts = [alert for alert in selection.SelectedRowObjects()
                            if alert.IsKindOf(acm.FAlert)]
        
        if callable(self._validateFunc):
            alerts = [alert for alert in alerts if self._validateFunc(alert)]
        return alerts

    def _SelectedAlert(self):
        alerts = self._SelectedAlerts()
        return alerts[0] if alerts else None
      
      
class AlertInactivateMenuItem(AlertMenuItem):

    def __init__(self, extObj):
        AlertMenuItem.__init__(self, extObj,
                               validateFunc=lambda a: bool(not a.Originator().IsInfant())
                               )
    
    def Checked(self):
        alerts = self._SelectedAlerts()
        return self._AnyInactivated(alerts)
    
    def ConfirmationDialog(self, eii):
        text = 'Do you really want to inactivate the selected alerts? \nInactivated alerts will not be included in future compliance checks.'
        shell = eii.ExtensionObject().Shell()
        result = acm.UX().Dialogs().MessageBoxOKCancel(shell, 'Question', text)
        return result == 'Button1'
    
    def Invoke(self, eii):
        alerts = self._SelectedAlerts()
        newState = 'Active' if self._AnyInactivated(alerts) else 'Inactive'
        if newState == 'Inactive' and not self.ConfirmationDialog(eii):
            return           
        else:
            with Transaction():
                for alert in alerts:
                    alert.State(newState)
                    alert.Commit()
    
    @staticmethod
    def _AnyInactivated(alerts):
        return any(alert.State() == 'Inactive' for alert in alerts)


class AlertAcknowledgedMenuItem(AlertMenuItem):
    
    def __init__(self, extObj):
        AlertMenuItem.__init__(self, extObj,
                               validateFunc=lambda a: bool(not a.Originator().IsInfant())
                               )
    
    def Checked(self):
        alerts = self._SelectedAlerts()
        return not self._AnyUnacknowledged(alerts)
    
    def Invoke(self, eii):
        alerts = self._SelectedAlerts()
        anyUnacknowledged = self._AnyUnacknowledged(alerts)
        with Transaction():
            for alert in alerts:
                alert.Acknowledged(anyUnacknowledged)
                alert.Commit()

    @staticmethod
    def _AnyUnacknowledged(alerts):
        return any(not alert.Acknowledged() for alert in alerts)


class DeleteAlertMenuItem(AlertMenuItem):
    
    def __init__(self, extObj):
        AlertMenuItem.__init__(self, extObj,
                               validateFunc=lambda a: bool(not a.Originator().IsInfant())
                               )
    
    def Invoke(self, eii):
        text = 'Do you really want to delete the selected alerts?'
        shell = eii.ExtensionObject().Shell()
        result = acm.UX().Dialogs().MessageBoxOKCancel(shell, 'Question', text)
        if result == 'Button1':
            for alert in self._SelectedAlerts():
                alert.Delete()


class InspectAlertMenuItem(AlertMenuItem):

    def Invoke(self, eii):
        alert = self._SelectedAlert()
        InspectRule(alert.AppliedRule(), alert)


class ManualCheckMenuItem(FUxCore.MenuItem):
    
    def __init__(self, app):
        self._app = app
    
    def Enabled(self):
        return not self._app.Rule().IsInfant()
    
    @staticmethod
    def _BuildAelParams(module, extraParam):
        params = {p[FRunScriptGUI.Controls.NAME]: p[FRunScriptGUI.Controls.VALUES] for p in getattr(module, 'ael_variables')}
        params.update(extraParam)
        strParams = acm.FDictionary()
        for k, v in params.iteritems():
            strParams.AtPutStrings(k, v)
        return strParams

    @contextmanager
    def CreateTransientTask(self, module, extraParam):
        task = acm.FAelTask()
        task.ModuleName = module.__name__
        task.Parameters(self._BuildAelParams(module, extraParam) )
        task.RegisterInStorage()
        yield task
        task.Unsimulate()
        
    def Invoke(self, _eii):
        rules = [self._app.Rule()]
        extraParam = dict(Rules = ','.join(str(r.Name()) for r in rules),
                          StoreAlerts = True)
        with self.CreateTransientTask(FComplianceCheck, extraParam) as task:
            acm.StartApplication("Run Script", task)


class ViewAlertsMenuItem(FUxCore.MenuItem):
    
    def __init__(self, app):
        self._app = app
    
    def Enabled(self):
        return not self._app.Rule().IsInfant()
    
    def Invoke(self, _eii):
        rule = self._app.Rule()
        alerts = self._ActiveAlerts(rule)
        if alerts:
            self.DisplayAlertSheet(alerts)
        else:
            acm.UX.Dialogs().MessageBoxInformation(self._app.Shell(), 'There are no active alerts for this rule')
            
    def DisplayAlertSheet(self, alerts):
        dlg = FComplianceRulesUtils.AlertSheetDialog(alerts)
        acm.UX.Dialogs().ShowCustomDialog(self._app.Shell(), dlg.CreateLayout(), dlg)
        
    @staticmethod
    def _ActiveAlerts(rule):
        alerts = []
        for appliedRule in rule.AppliedRules():
            for alert in appliedRule.Alerts():
                if alert.State() in ['Active', 'Error']:
                    alerts.append(alert)
        return alerts
               

class ViewAlertsPanel(FUxCore.LayoutPanel):

    def __init__(self, frame):
        self._sheetCtrl = None
        self._frame = frame
        self._frame.AddDependent(self)
        self._sheet = None
        self._lastSelection = None
                    
    def Sheet(self):
        return self._frame.ActiveSheet()
        
    def ServerUpdate(self, sender, aspect, param):
        if str(aspect) == 'SelectionChanged':
            rowObjects = self.Sheet().Selection().SelectedRowObjects()
            if self._lastSelection is None or (rowObjects != self._lastSelection):
                self._lastSelection = rowObjects
                self.InsertAlerts(GetAlerts(rowObjects))
    
    def HandleDestroy(self):
        self._frame.RemoveDependent(self)                
                                                
    def HandleCreate(self):
        layout = self.SetLayout(self.CreateLayout())
        self._sheetCtrl = layout.GetControl('sheet')
        self._sheet = self._sheetCtrl.GetCustomControl()
                
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddCustom('sheet', 'sheet.FAlertSheet', 800, 250)
        b.EndBox()
        return b
    
    def InsertAlerts(self, alerts):
        self._sheet.RemoveAllRows()
        folder = FSheetUtils.GetObjectsAsFolder(alerts, label='Alerts')
        self._sheet.InsertObject(folder, 'IOAP_LAST')
        grouper = FGrouperUtils.GetGrouper('Rule', acm.FAlertSheet)
        FSheetUtils.ApplyGrouperInstanceToSheet(self._sheet, grouper)
        FSheetUtils.ExpandTree(self._sheet, 3)

#------------------------------------------------------------------------------
# Dialogs
#------------------------------------------------------------------------------

class SelectAppliedRuleDialog(FUxCore.LayoutDialog):

    def __init__(self, rule):
        self.m_closeBtn = None
        self._rule = rule
        self._listCtrl = None
        self._appliedRules = {ar.Target():ar for ar in self._rule.AppliedRules()}
        
    def HandleApply(self):
        return self._appliedRules[self._listCtrl.GetData()]
    
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Select Rule Target')
        self._listCtrl = layout.GetControl('list1')
        self._listCtrl.Populate(sorted(self._appliedRules.keys()))

    @staticmethod
    def CreateLayout():
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddList('list1', 5, 20, 25, 100)
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('ok', 'Select')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b

#------------------------------------------------------------------------------
# Menu item functions
#------------------------------------------------------------------------------

def ViewRuleFromAlertRightClick(eii):
    alert = SelectedObjectFromExtensionInvokationInfo(eii, acm.FAlert)
    if alert:
        acm.StartApplication('Compliance Rule Editor', alert.ComplianceRule())

def InspectAlertFromAlertRightClick(eii):
    alert = SelectedObjectFromExtensionInvokationInfo(eii, acm.FAlert)
    if alert:
        InspectRule(alert.AppliedRule(), alert)

def InspectRuleFromRightClick(eii):
    rule = SelectedObjectFromExtensionInvokationInfo(eii, acm.FComplianceRule)
    if rule:
        dlg = SelectAppliedRuleDialog(rule)
        shell = eii.ExtensionObject().Shell()
        appliedRule = acm.UX.Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)
        if appliedRule:
            InspectRule(appliedRule)

def CreateAlertInactivateMenuItem(eii):
    return AlertInactivateMenuItem(eii)

def CreateAlertAcknowledgedMenuItem(eii):
    return AlertAcknowledgedMenuItem(eii)

def CreateViewRuleMenuItem(eii):
    return AlertMenuItem(eii,
            invokeFunc=lambda a: ViewRule(a, eii),
            enabledFunc=lambda a: True)

def CreateViewAlertSubjectMenuItem(eii):
    return AlertMenuItem(eii,
            invokeFunc=lambda a: StartCommonObjectApplication(a.Subject()),
            enabledFunc=lambda alerts: bool(alerts and alerts[0].Subject()))

def CreateDeleteAlertMenuItem(eii):
    return DeleteAlertMenuItem(eii)

def CreateManualCheckMenuItem(eii):
    return ManualCheckMenuItem(eii)

def CreateViewAlertsMenuItem(eii):
    return ViewAlertsMenuItem(eii)

def CreateInspectAlertMenuItem(eii):
    return InspectAlertMenuItem(eii)

def CreateAddAlertSheetMenuItem(eii):
    return CreateAddSheetMenuItem(eii, 'AlertSheet')
    
def CreateAddRuleSheetMenuItem(eii):
    return CreateAddSheetMenuItem(eii, 'RuleSheet')

def CreateViewAlertsPanel(eii):
    basicApp = eii.ExtensionObject()
    return ViewAlertsPanel(basicApp)

def OnRegisterAlertDockWindow(eii):
    basicApp = eii.ExtensionObject()
    basicApp.RegisterDockWindowType(VIEW_ALERTS_PANEL_CREATE, 'FComplianceRuleMenuItem.CreateViewAlertsPanel')
