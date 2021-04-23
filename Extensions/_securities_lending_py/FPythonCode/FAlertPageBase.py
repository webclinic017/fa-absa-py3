""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FAlertPageBase.py"

import acm, ael
import FSheetUtils
from FPanel import Panel
from FSecLendUtils import logger


class NoQuery:

    def IsSatisfiedBy(self, obj):
        return False
        
    def Select(self):
        return acm.FArray()
        
      
class AlertPage(Panel):

    def __init__(self, parent):
        self.parent = parent
        self.m_sheet = None
        self.query = None
        self.queryFolder = None
        self._settings = None
            
    def Filter(self):
        return self.query
      
    def SetDefaultQuery(self):
        if not self.query:
            if self.DEFAULT_FOLDER:
                self.queryFolder = acm.FStoredASQLQuery[self.DEFAULT_FOLDER]
                self.query = self.queryFolder.Query()
            else:
                self.queryFolder = None
                self.query = self.CreateDefaultQueryFromCRules()
        else:
            self.query = NoQuery
    
    def CreateDefaultQueryFromCRules(self):
        if self.COMPLIANCE_RULE:
            query = acm.CreateFASQLQuery('FAlert', 'AND')
            query.AddAttrNode('State', 'EQUAL', 1)
            node = query.AddOpNode('OR')
            for rule in self.COMPLIANCE_RULE:
                node.AddAttrNode('AppliedRule.ComplianceRule.Name', 'EQUAL', rule)
            return query
        else:
            logger.info('No Compliance Rules found')
            pass
            
    
    def SetDefaultContents(self):
        self.SetDefaultQuery()
        self.ResetFilter()
        
    def SettingsContents(self):
        return FSheetUtils.SheetContents(self.Settings()).ForControl()
        
    ''' Callbacks '''   
    
    def DismissSelectedAlerts(self, *args):
        self.m_sheet.Sheet().RemoveSelectedRows()
        
    def EditFilter(self, *args):
        qf = acm.UXDialogs.SelectStoredASQLQuery(self.parent.Shell(), acm.FAlert, self.queryFolder)
        if qf:
            self.queryFolder = qf
            self.query = qf.Query()
            self.ResetFilter()

    def ClearAlerts(self, *args):
        self.m_sheet.RemoveAllRows()
        
    def ResetFilter(self, *args):
        if self.Filter():
            alerts = self.Filter().Select().SortByProperty('UpdateTime', False)
            self.m_sheet.InsertObject(alerts, 'IOAP_REPLACE')
        else:
            pass
    
    def _GetRuleInterfaceFromAlert(self, alert):
        appliedRule = alert.AppliedRule()
        ruleClass = appliedRule.ComplianceRule().Definition().Class()
        interface = ruleClass.Interface()
        if interface:
            try:
                module, className = interface.split('.')
                func = getattr(__import__(module), className)
                return func
            except StandardError:
                pass
 
    def OnHandle(self, *args):
        alerts = self.m_sheet.Sheet().Selection().SelectedRowObjects()
        for alert in alerts:
            try:
                interface = self._GetRuleInterfaceFromAlert(alert)
                interface().OnHandle(alert, *args)
            except:
                logger.error('OnHandle function is not implemented for the rule {0}'.format(alert.AppliedRule().ComplianceRule().Name()))
            

    def OnDetails(self, *args):
        alerts = acm.FArray()
        alerts.AddAll(self.m_sheet.Sheet().Selection().SelectedRowObjects())
        # Check that only one Rule Type is selected.
        rules = acm.FSet()
        rules.AddAll([alert.AppliedRule().ComplianceRule().DefinitionInfo() for alert in alerts])
        if rules.Size() !=1:
            return acm.UX.Dialogs().MessageBoxInformation(self.parent.Shell(), 'Only one Rule Type can be selected for a Detail View')
        try:
            interface = self._GetRuleInterfaceFromAlert(alerts.First())
            interface().OnDetails(alerts, *args)
        except:
            logger.error('OnView function is not implemented for the rule {0}'.format(alerts.First().AppliedRule().ComplianceRule().Name()))
  

    ''' Subscription '''
    
    def ReplaceAlert(self, alert):
        try:
            self.RemoveAlert(alert)
            self.m_sheet.Sheet().InsertObject(alert, 'IOAP_FIRST')
        except RuntimeError as e:
            pass
            
    def RemoveAlert(self, alert):
        try:
            iterator = self.m_sheet.RowTreeIterator(False).Find(alert)
            self.m_sheet.RemoveRows([iterator])
        except RuntimeError as e:
            pass
            
    def ProcessAlert(self, alert):
        if self.Filter() and self.Filter().IsSatisfiedBy(alert):
                self.ReplaceAlert(alert)
        else:
            self.RemoveAlert(alert)


