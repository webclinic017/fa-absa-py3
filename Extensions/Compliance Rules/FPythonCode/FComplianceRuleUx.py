""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FComplianceRuleUx.py"
"""--------------------------------------------------------------------------
MODULE
    FComplianceRuleUx

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""
import acm
import FSheetUtils
import FUxCore
from EditObjectUx import EditObjectUx
import FComplianceRuleMenuItem
import DealPackageUxDialogs


# ****************************** Edit Object Ux ******************************

class ComplianceRulesUx(EditObjectUx, object):

    def __init__(self):
        EditObjectUx.__init__(self)
        
    def HandleObject(self, obj):
        EditObjectUx.HandleObject(self, obj)
        
    def Object(self):
        return self.DealPackage().Object()
    
    def RegisterCustomCommands(self):
        commands = EditObjectUx.RegisterCustomCommands(self)
        commands.append(['manualCheck', 'View', 'Manual Check', 'Manually run a compliance check fir this rule', '', '', self.ManualCheckCb, False])
        commands.append(['activeAlerts', 'View', 'Active Alerts', 'Dispays a sheet with all active alerts for this rule', '', '', self.ActiveAlertsCb, False])         
        return commands
    
    def HandleCreate(self, layout):
        EditObjectUx.HandleCreate(self, layout)
                   
    def OnFileDelete(self):
        _delete, _cancel = self._AskDelete()
        if not _cancel:
            try:
                self.Unsubscribe()
                self.DeleteAppliedRules(self.Object().AppliedRules().AsArray())
                self.DealPackageHelper().Delete(_delete)
            except Exception as e:
                self.Subscribe()
                dialog = DealPackageUxDialogs.DealPackageExceptionDialog(self.Shell(), e)
                dialog.ShowDealPackageExceptionDialog()
    
    def OnFileSaveNewEnabled(self):
        if self.DealPackageHelper().IsModified() or self.DealPackage().IsInfant():
            if self.GetCurrentObject():
                if self.DealPackageHelper().Name() and self.DealPackageHelper().Name() != self.Rule().Name():
                    return True
            else:
                return True if self.DealPackageHelper().Name() else False
        return False
            
    def DeleteAppliedRules(self, rules):
        if rules != None:
            try:
                acm.BeginTransaction()
                for rule in rules:
                    rule.Delete()
                acm.CommitTransaction()
            except Exception:
                acm.AbortTransaction()
                            
    def Rule(self):
        return self.Originator(self.Object())
    
    def OnFileOpen(self):
        EditObjectUx.OnFileOpen(self)
                        
    def OnFileNew(self):
        gui = acm.FBusinessLogicGUIShell()
        gui.SetFUxShell(self.Shell())
        rule = acm.EditableObject.New("Compliance Rule", gui)
        self.HandleObject(rule)
        
    def HandleSetContents(self, contents):
        EditObjectUx.HandleSetContents(self, contents)
    
    def Originator(self, acmObj):
        if hasattr(acmObj, 'DecoratedObject'):
            return acmObj.DecoratedObject().Originator()
        return acmObj
    
    def ManualCheckCb(self):
        return FComplianceRuleMenuItem.ManualCheckMenuItem(self)
        
    def ActiveAlertsCb(self):
        return FComplianceRuleMenuItem.ViewAlertsMenuItem(self)
    
    def _AskDelete(self):
        dialog = DealPackageUxDialogs.DealPackageDeleteDialog(self.Shell())
        subject = self.DealPackageHelper().Subject()
        deleteTrades = dialog.ShowDealPackageFileSimpleDeleteDialog(subject)
        cancel = not deleteTrades
        return deleteTrades, cancel


# ************************** CreateApplicationInstance **************************
def CreateApplicationInstance():
    return ComplianceRulesUx()


# ****************************** StartApplication ******************************

def LaunchApplication(eii):
    gui = acm.FBusinessLogicGUIShell()
    gui.SetFUxShell(eii.ExtensionObject().Shell())
    acm.StartApplication('Compliance Rule Editor', acm.EditableObject.New('Compliance Rule', gui)) 
