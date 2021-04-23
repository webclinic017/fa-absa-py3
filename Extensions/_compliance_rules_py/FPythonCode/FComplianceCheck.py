""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FComplianceCheck.py"
"""--------------------------------------------------------------------------
MODULE
    FComplianceCheck

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Runscript for checking compliance rules and creating alerts. New alerts will
    be created and existing ones will be updated if their state has changed.
    Can check for a list of rules or a query of rules.
    
-----------------------------------------------------------------------------"""
from  collections import namedtuple

import acm
import FRunScriptGUI
import FSheetUtils
import FAlertGenerator
import FComplianceNotifications
from FComplianceRulesUtils import logger


# ----------------------------------------------- Create Alerts -----------------------------------------------

def GenerateAlerts(rules, createWhenCompliant=False, saveAlerts=False):
    params = type('Params', (object,), {
                  'CreateWhenCompliant': lambda self: createWhenCompliant,
                  'SaveAlerts': lambda self: saveAlerts
                  })()
    alerts = []
    for rule in rules:
        if not rule.Inactive():
            logger.debug('Checking alerts for rule "{0}" on target {1}.'.format(rule.ComplianceRule().Name(), rule.Target().Name()))
            generator = FAlertGenerator.Create(rule, params)
            alerts.extend(generator.AlertsFromCheck(rule.Check()))
        else:
            logger.debug('Rule target "{0}" for rule "{1}" is not activated and will not '
                                     'be checked'.format(rule.Target().Name(), rule.ComplianceRule().Name()))
    return alerts

# ----------------------------------------------- Display Alerts -----------------------------------------------

def Sheet(workbook, sheetTemplate):
    if sheetTemplate:
        workbook.InsertSheet(sheetTemplate)
        return workbook.ActiveSheet()
    else:
        return workbook.NewSheet('AlertSheet')

def InsertAlerts(sheet, alerts):
    folder = acm.FItemsFolder(acm.FAlert)
    folder.Name('Alerts')
    folder.AddAll(alerts)
    sheet.InsertObject(folder, 'IOAP_REPLACE')
        
def ApplyGrouper(sheet, sheetTemplate): # Workaround since Initial Grouper currently doesn't work in Alert Sheet.
    if sheetTemplate:
        grouper = sheetTemplate.FromArchive('TradingSheet').FromArchive('InitialGrouper')
        FSheetUtils.ApplyGrouperInstanceToSheet(sheet, grouper)
    FSheetUtils.ExpandTree(sheet)

def DisplayInAlertSheet(alerts, sheetTemplate=None):
    frame = acm.StartApplication('Operations Manager', None)
    sheet = Sheet(frame.ActiveWorkbook(), sheetTemplate)
    InsertAlerts(sheet, alerts)
    ApplyGrouper(sheet, sheetTemplate)

# ----------------------------------------------- Runscript -----------------------------------------------

class ComplianceCheckRunscript(FRunScriptGUI.AelVariablesHandler):

    GUI_PARAMETERS = {
        'runButtonLabel':   '&&Run',
        'hideExtraControls': False,
        'windowCaption' : __name__
        }
    LOG_LEVELS = {
        '1. Normal': 1,
        '2. Warnings/Errors': 3,
        '3. Debug': 2
        }

    def __init__(self):
        FRunScriptGUI.AelVariablesHandler.__init__(self, self._GetVariableDefinitions())

    @staticmethod
    def GetParameters(params):
        paramClass = namedtuple('RuleParameters', list(params.keys()))
        return paramClass(**params)

    @classmethod
    def GetLoggingLevel(cls, logLevel):
        return cls.LOG_LEVELS.get(logLevel, 1)
        
    def _NotificationsSetEnabled(self, index, field_values):
        if self.ael_variables[index][FRunScriptGUI.Controls.NAME] in ['SendEmail', 'SendMessage']:
            enabled = field_values[index] == 'true'
            self.ael_variables[index+1][FRunScriptGUI.Controls.ENABLED] = enabled
            self.ael_variables[index+2][FRunScriptGUI.Controls.ENABLED] = enabled
        return field_values

    def _GetVariableDefinitions(self):
        logLevels = sorted(self.LOG_LEVELS)
        users = acm.FUser.Select('')
        threshold_types = acm.FChoiceList['Threshold Type'].Choices()
        
        tt_Rules = 'Select the individual rules(s) to check.'
        tt_RuleQueries = 'Select the insert item query or queries containing rules to check.'
        tt_TestMode = 'In test mode alerts will be generated by the compliance check, but they will not be stored in ADS.'
        tt_CreateAlertWhenCompliant = 'Used with test mode. If checked, alerts will be created when results are compliant in order to verify that a rule works correctly.'
        tt_DisplayAlerts = 'If checked, created alerts will be displayed in the Operations Manager.'
        tt_SheetTemplate = 'Set the sheet tempalte that will be used when displaying the alerts.'
        tt_SendEmail = 'Send notification via email.'
        tt_EmailRecipients = 'Select users or enter email recipient addresses (comma separated).'
        tt_ThresholdTypeEmail = 'Choose Threshold type(s)'
        tt_SendMessage = 'Send notification as a message.'
        tt_MessageRecipients = 'Select or enter users.'
        tt_ThresholdTypeMessage = 'Choose Threshold type(s)'
        tt_LogLevel = 'Select the verbosity of logging output by the compliance engine task.'
        
        return (
            ('Rules', 'Rules_General', 'FComplianceRule', None, self._GetRuleOidQuery(), True, True, tt_Rules, None, True), 
            ('RuleQueries', 'Rule query_General', 'FStoredASQLQuery', None, self._GetRuleInsertItemQueries(), True, True, tt_RuleQueries, None, True),
            ('TestMode', 'Test Mode_General', 'bool', [True, False], False, False, False, tt_TestMode, self._TestModeCallback, True),
            ('CreateAlertWhenCompliant', 'Create alert when compliant_General', 'bool', [True, False], False, False, False, tt_CreateAlertWhenCompliant, None, False),
            ('DisplayAlerts', 'Display alerts in Operations Manager_General', 'bool', [True, False], False, False, False, tt_DisplayAlerts, self._DisplayAlertsCallback, True),
            ('SheetTemplate', 'SheetTemplate_General', 'FTradingSheetTemplate', self._GetSheetTemplates(), None, False, 0, tt_SheetTemplate, None, True),
             
            ('SendEmail', 'Send email_Notifications', 'bool', [True, False], False, False, False, tt_SendEmail, self._NotificationsSetEnabled, True),
            ('EmailRecipients', 'Recipients_Notifications', 'string', users, None, 0, 1, tt_EmailRecipients, None, 0),
            ('ThresholdTypeEmail', 'Threshold Type_Notifications', 'FChoiceList', threshold_types, None, 0, 1, tt_ThresholdTypeEmail, None, 0),
            ('SendMessage', 'Send user message_Notifications', 'bool', [True, False], False, False, False, tt_SendMessage, self._NotificationsSetEnabled, True),
            ('MessageRecipients', 'Recipients_Notifications', 'FUser', users, None, 0, 1, tt_MessageRecipients, None, 0),
            ('ThresholdTypeMessage', 'Threshold Type_Notifications', 'FChoiceList', threshold_types, None, 0, 1, tt_ThresholdTypeMessage, None, 0),

            ('LogLevel', 'Logging Level_Logging', 'string', logLevels, logLevels[0], 2, 0, tt_LogLevel),
            )
    
    def _TestModeCallback(self, index, fieldValues):
        enabled = fieldValues[index] == 'true'
        for var in self.ael_variables:
            if var[FRunScriptGUI.Controls.NAME] == 'CreateAlertWhenCompliant':
                var[FRunScriptGUI.Controls.ENABLED] = enabled
        return fieldValues
    
    def _DisplayAlertsCallback(self, index, fieldValues):
        self._SheetTemplateSetEnabled(fieldValues)
        return fieldValues
    
    def _VariableIndex(self, varName):
        for i, var in enumerate(self.ael_variables):
            if var[FRunScriptGUI.Controls.NAME] == varName:
                return i
    
    def _SheetTemplateSetEnabled(self, fieldValues):
        displayAlerts = fieldValues[self._VariableIndex('DisplayAlerts')]
        enabled = 'true' in [displayAlerts]
        self.ael_variables[self._VariableIndex('SheetTemplate')][FRunScriptGUI.Controls.ENABLED] = enabled
        
    @staticmethod
    def _GetRuleOidQuery():
        q = acm.CreateFASQLQuery(acm.FComplianceRule, 'AND')
        op = q.AddOpNode('AND')
        op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
        op = q.AddOpNode('AND')
        op.AddAttrNode('RuleCategory.Name', 'EQUAL', None)
        return q

    @staticmethod
    def _GetRuleInsertItemQueries():
        q = acm.CreateFASQLQuery(acm.FStoredASQLQuery, 'AND')
        q.AddOpNode('AND').AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
        q.AddOpNode('AND').AddAttrNode('SubType', 'RE_LIKE_NOCASE', 'FComplianceRule')
        return q
        
    @staticmethod
    def _GetSheetTemplates():
        return acm.FTradingSheetTemplate.Select('subType = FAlertSheet').SortByProperty('Name')
    
def DisplayAlerts(options):
    return acm.IsSessionUserInteractive() and options.DisplayAlerts


ael_variables = ComplianceCheckRunscript()
ael_gui_parameters = ael_variables.GUI_PARAMETERS

def ael_main(params):
    options = ComplianceCheckRunscript.GetParameters(params)
    logger.Reinitialize(level=ComplianceCheckRunscript.GetLoggingLevel(options.LogLevel))
    logger.info('Running compliance check ...')
    
    TestMode = options.TestMode
    createWhenCompliant = options.CreateAlertWhenCompliant and TestMode
    saveAlerts = bool(TestMode==False)
    
    rules = acm.FArray()
    rules.AddAll([rule for rule in options.Rules])    
    for query in options.RuleQueries:
        rules.AddAll(query.Query().Select())
    
    appliedRules = [ar for rule in rules for ar in rule.AppliedRules()]
    alerts = GenerateAlerts(appliedRules, createWhenCompliant, saveAlerts)
    
    if DisplayAlerts(options):
        if alerts:
            DisplayInAlertSheet(alerts, options.SheetTemplate)
        else:
            shell = acm.UX.SessionManager().Shell()
            msg = 'No alerts were created for this compliance check'
            logger.debug(msg)
            acm.UX.Dialogs().MessageBoxInformation(shell, msg)
        
    if options.SendEmail:
        FComplianceNotifications.send_email_notification(alerts, options)
        
    if options.SendMessage:
        FComplianceNotifications.send_message_notification(alerts, options)
    logger.info('Compliance check completed')
