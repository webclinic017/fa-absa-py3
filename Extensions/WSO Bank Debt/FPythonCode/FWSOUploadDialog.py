""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOUploadDialog.py"
"""--------------------------------------------------------------------------
MODULE
    FWSOUploadDialog

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import collections
import datetime

import acm
import FReconciliationSpecification
import FRunScriptGUI

class WSOUploadDialog(FRunScriptGUI.AelVariablesHandler):

    NAMESPACE = 'Reconciliation'
    GUI_PARAMETERS = {'runButtonLabel':   '&&Run',
                      'hideExtraControls': False,
                      'windowCaption' : None}
    LOG_LEVELS = {'1. Normal': 1,
                  '2. Warnings/Errors': 3,
                  '3. Debug': 2}

    def __init__(self, namespace=None):
        variables = []
        self.Namespace(namespace)
        self.isUpload = (namespace == 'Data Upload')        
        #variables.extend(self.getFilenameVariableSpec())
        variables.extend(self.getReconciliationSpecificationVariableSpec())
        variables.extend(self.getDisplayOptionSpec())
        
        #tab=Reconcilation date
        variables.extend(self.getReconciliationStartDate())
        variables.extend(self.getReconciliationStartDateCustom())
        variables.extend(self.getReconciliationEndDate())
        variables.extend(self.getReconciliationEndDateCustom())
        #tab=Logging
        variables.extend(self.getOverrideReRunCheck())
        variables.extend(self.getLoggingLevelVariableSpec())
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)
        
    def Namespace(self, namespace=None):
        if namespace is None:
            return self.__class__.NAMESPACE
        self.__class__.NAMESPACE = namespace

    @staticmethod
    def getParameters(ael_params):
        paramClass = collections.namedtuple('ReconciliationParameters', list(ael_params.keys()))
        return paramClass(**ael_params)

    @classmethod
    def getLoggingLevelVariableSpec(cls, tab='Logging'):
        logLevels = sorted(cls.LOG_LEVELS)
        return (('LogLevel', 'Logging Level_' + tab, 'string', logLevels, logLevels[0], 2, 0,
                 'Select the verbosity of logging output by the reconciliation tasks.'),
            )
    
    def GUIParams(self):
        self.__class__.GUI_PARAMETERS['windowCaption'] = self.Namespace()
        return self.__class__.GUI_PARAMETERS

    def getFilenameVariableSpec(self):
        fileFilters = (
                'CSV Files (*.csv)|*.csv',
                'Excel Files (*.xl*)|*.xl*',
                'XML Files (*.xml)|*.xml',
                'Text Files (*.txt)|*.txt',
                'All Files (*.*)|*.*',
            )
        fileSelection = FRunScriptGUI.InputFileSelection('|'.join(fileFilters))
        tab = self.Namespace()
        tooltip = 'The %s document file to import.' % tab.lower()
        return (
            ('Filename', '_'.join(('Filename', tab)), fileSelection, None, fileSelection, 1, 1,
             tooltip, None, 1),
            )

    def getDisplayOptionSpec(self):
        tab = self.Namespace()
        label = 'Display results in Operations Manager'
        tooltip = ('Select this to view the resulting business processes '
                   'and %s items in the Operations Manager.' % tab.lower())
        return (
            ('DisplayOption', '_'.join((label, tab)), 'string', ["1", "0"], "1", 0, 0, tooltip),
            )

    def getReconciliationSpecificationVariableSpec(self):
        label = tab = self.Namespace()
        tooltip = 'The name of the %s specification to be performed.' % label.lower()
        reconSpecifications = sorted(FReconciliationSpecification.GetReconciliationSpecificationNames(self.isUpload))
        return (
            ('ReconciliationSpecification', '_'.join((label, tab)), 'string',
            reconSpecifications, reconSpecifications[0] if reconSpecifications else '',
            1, 0, tooltip, None, 1),
            )

    def getOverrideReRunCheck(self):
        tab = self.Namespace()
        keyword = 'reconciled' if tab in ('Reconciliation',) else 'uploaded'
        label = 'Force re-run of previously %s file' % keyword
        tooltip = 'Select this to force a re-run of a file that has previously been %s.' % keyword
        return (
            ('ForceReRun', '_'.join((label, tab)), 'string', ["1", "0"], "1", 0, 0, tooltip),
            )

    def getReconciliationStartDate(self, tab='date'):
        keyword = self.Namespace()
        label = '%s Start Date' % keyword
        tooltip = 'The start date of the %s to be performed.' % keyword.lower()
        startDateEnums = self.GetReconciliationDateEnum('Start')
        return (
            ('StartDate', '_'.join((label, tab)), 'string', startDateEnums, startDateEnums[0],
            0, 0, tooltip, self.EnableCustomField, 1),
            )

    def getReconciliationEndDate(self, tab='date'):
        keyword = self.Namespace()
        label = '%s End Date' % keyword
        tooltip = 'The end date of the %s to be performed.' % keyword.lower()
        endDateEnums = self.GetReconciliationDateEnum('End')
        return (
            ('EndDate', '_'.join((label, tab)), 'string', endDateEnums, endDateEnums[0],
            0, 0, tooltip, self.EnableCustomField, 1),
            )

    def getReconciliationStartDateCustom(self, tab='date'):
        keyword = self.Namespace()
        label = '%s Start Date Custom' % keyword
        tooltip = 'The custom start date of the %s to be performed.' % keyword.lower()
        return (
            ('CustomStartDate', '_'.join((label, tab)), 'string', None, None,
            0, 0, tooltip, self.DateQuickEntry, 0),
            )

    def getReconciliationEndDateCustom(self, tab='date'):
        keyword = self.Namespace()
        label = '%s End Date Custom' % keyword
        tooltip = 'The custom end date of the %s to be performed.' % keyword.lower()
        return (
            ('CustomEndDate', '_'.join((label, tab)), 'string', None, None,
            0, 0, tooltip, self.DateQuickEntry, 0),
            )

    @classmethod
    def GetReconciliationDateEnum(cls, tag):
        context = acm.GetDefaultContext()
        enumFormatter = context.GetExtension('FEnumFormatter', 'FObject', 'EnumPL' + tag + 'Date')
        return enumFormatter.Value().Enumeration().Enumerators()

    def EnableCustomField(self, index, fieldValues):
        if fieldValues[index] in ('Custom Date'):
            self.ael_variables[index+1][9] = 1
        else: 
            self.ael_variables[index+1][9] = 0
        return fieldValues

    @classmethod
    def DateQuickEntry(cls, index, fieldValues):
        try:
            valueDate = acm.Time.DateValueDay()
            fieldValues[index] = acm.Time.DateAdjustPeriod(valueDate, fieldValues[index])
        except TypeError:
            try:
                datetime.datetime.strptime(fieldValues[index], '%Y-%m-%d')
            except ValueError:
                fieldValues[index] = valueDate
        return fieldValues
