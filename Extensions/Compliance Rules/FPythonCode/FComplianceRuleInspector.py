""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FComplianceRuleInspector.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FComplianceRuleInspector

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Contains base class to help display the details of a rule or alert in a portfolio sheet
-------------------------------------------------------------------------------------------------------"""
import acm
import FSheetUtils
import FComplianceRulesUtils
import FAlertGenerator

class ComplianceRuleInspectorPortfolioSheet(object):
    
    def __init__(self, appliedRule, alert=None):
        self._appliedRule = appliedRule
        self._alert = alert
        self._valueSource = self.ValueSource(appliedRule)
        self._alertGenerator = FAlertGenerator.Create(appliedRule)
        self._sheet = None
    
    def Display(self):
        app = self.LaunchApplication()
        self._sheet = self.InsertSheet(app)
        self.InsertRuleTarget()
        self.SelectRelevantRow()
    
    def InsertSheet(self, app):
        template = self.SheetTemplate()
        if template:
            return self._InsertSheetFromTemplate(app.ActiveWorkbook(), template)
        else:
            return self._InsertNewSheet(app.ActiveWorkbook())
    
    def InsertRuleTarget(self):
        self._sheet.InsertObject(self.RuleTarget(), 'IOAP_LAST')
        self.ApplyGrouper()
        FSheetUtils.ExpandTree(self._sheet, 2)
        
    def SelectRelevantRow(self):
        if self._alert is not None:
            self._sheet.PrivateTestSyncSheetContents()
            iterator = self._sheet.RowTreeIterator(False)
            while(iterator.NextUsingDepthFirst()):
                row = iterator.Tree().Item()
                if self.RowMatchesAlertSubject(row):
                    self._sheet.NavigateTo(row)
                    break
    
    def RowMatchesAlertSubject(self, row):
        return self._alertGenerator.ToSubject(row) == self._alert.Subject()
    
    def ApplyGrouper(self):
        pass
    
    def ColumnCreators(self):
        return FSheetUtils.ColumnCreators(self.Columns())
    
    def Columns(self):
        return []
    
    def RuleTarget(self):
        return self._appliedRule.Target()
    
    def LaunchApplication(self):
        return acm.StartApplication('Trading Manager', None)
    
    def SheetTemplate(self):
        """ Implement if inspection should use a sheet template as default. """
        return None
    
    def _InsertNewSheet(self, workbook):
        sheetSetup = FSheetUtils.CreateSheetSetup()
        sheetSetup.ColumnCreators(self.ColumnCreators())
        sheetSetup.SheetTitle(self._SheetName())
        return workbook.NewSheet('PortfolioSheet', None, sheetSetup)

    def _InsertSheetFromTemplate(self, workbook, template):
        template = template.Clone()
        template.FromArchive('TradingSheet').ToArchive('sname', self._SheetName())
        workbook.InsertSheet(template)
        sheet = workbook.ActiveSheet()
        self._InsertColumns(sheet, self.ColumnCreators())
        return sheet
    
    def _SheetName(self):
        return '{0}'.format(self._appliedRule.ComplianceRule().Name())
    
    @staticmethod
    def _InsertColumns(sheet, columnCreators):
        for i in range(columnCreators.Size()):
            sheet.ColumnCreators().Add(columnCreators.At(i))
    
    @staticmethod
    def ValueSource(appliedRule):
        interface = FComplianceRulesUtils.RuleInterface(appliedRule.ComplianceRule())
        return interface().CreateValueSource(appliedRule)      
