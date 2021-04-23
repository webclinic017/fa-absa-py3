""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/MarkitSecuritiesFinance/etc/FMarkitDataUpload.py"
from __future__ import print_function
import os
import acm, ael
import FRunScriptGUI
import FMarkitPerform
import MarkitPopulateData
from FOperationsIO import GetDefaultPath
from ACMPyUtils import Transaction
import datetime

class MarkitAelVariables(object):

    def __init__(self):
        self.ael_variables = []
        self._fileinfo()
        self._Logging()
    
    def _fileinfo(self):
        dirSelectionFile = FRunScriptGUI.DirectorySelection()
        dirSelectionFile.SelectedDirectory(str(GetDefaultPath()))
        vars = [['filedir', 'File path', dirSelectionFile, None, dirSelectionFile, 1, 1, '', None, None],
        ['filename', 'File name', 'string', None, '', 1, 0, '', None, None],
        ['clearDataBeforeUpload', 'Clear Data', 'int', [1, 0], 0, 0, 0, 'Clear data before upload', None, None]]
        self.ael_variables.extend(vars)

    def _Logging(self):
        ttLogMode = 'Defines the amount of logging produced.'
        ttLogToCon = ('Whether logging should be done in the Log Console or '
                'not.')
        ttLogToFile = 'Defines whether logging should be done to file.'
        ttLogFile = ('Name of the logfile. Could include the whole path, '
                'c:\log\...')
        ttSendReportByMail = ('Send reports by email when procedure is '
                'finished.')
        ttMailList = ('Specify mail recipients. Specify them in the form: '
                'user1@address.com, user2@address.com.')
        ttReportMessageType = ('Whether the report should be the full log, or '
                'if it should be only the selected messagetypes. If the '
                'selected messagetypes does not occur, no mail will be sent.')

        messageTypes = ['Full Log', 'START', 'FINISH', 'ABORT', 'ERROR', 'WARNING', 'NOTIME', 'INFO', 'DEBUG']
        vars = [['Logmode', 'Logmode_Logging', 'int', [0, 1, 2], 1, True, False, ttLogMode],
        ['LogToConsole', 'Log To Console_Logging', 'int', [1, 0], 1, True, False, ttLogToCon],
        ['LogToFile', 'Log To File_Logging', 'int', [1, 0], 0, False, False, ttLogToFile, self.enableLogtoFile],
        ['Logfile', 'Logfile_Logging', 'string', None, 'Markit.log', False, False, ttLogFile, None, 0],
        ['SendReportByMail', 'Send Report By Mail_Logging', 'int', [1, 0], None, False, False, ttSendReportByMail, self.enableemail],
        ['MailList', 'MailList_Logging', 'string', None, None, False, False, ttMailList, None, 0],
        ['ReportMessageType', 'ReportMessageType_Logging', 'string', messageTypes, 'Full Log', True, True, ttReportMessageType, self.reportMessageType_cb, 0]]
        self.ael_variables.extend(vars)
    
    def enableLogtoFile(self, index, fieldArray):
        nameIndex = FRunScriptGUI.Controls.NAME
        fieldPrefix = "Logfile"
        enableIndex = FRunScriptGUI.Controls.ENABLED
        for i in range(len(self.ael_variables)):
            if self.ael_variables[i][nameIndex].startswith(fieldPrefix):
                self.ael_variables[i][enableIndex] = fieldArray[index]
        return fieldArray
     
    def enableemail(self, index, fieldArray):
        nameIndex = FRunScriptGUI.Controls.NAME
        fieldPrefix = "MailList"
        enableIndex = FRunScriptGUI.Controls.ENABLED
        for i in range(len(self.ael_variables)):
            if self.ael_variables[i][nameIndex].startswith(fieldPrefix):
                self.ael_variables[i][enableIndex] = fieldArray[index]
        fieldPrefix = "ReportMessageType"
        for i in range(len(self.ael_variables)):
            if self.ael_variables[i][nameIndex].startswith(fieldPrefix):
                self.ael_variables[i][enableIndex] = fieldArray[index]
        return fieldArray   
    
    def logfile_cb(self, index, fieldValues):
        self.Logfile.enable(fieldValues[index], 'You have to check Log To '
                'File to be able to select a Logfile.')
        return fieldValues

    def sendReportByMail_cb(self, index, fieldValues):
        tt = ('This field is only applicable if Send Report By Mail is '
                'selected.')
        self.MailList.enable(fieldValues[index], tt)
        self.ReportMessageType.enable(fieldValues[index], tt)
        return fieldValues

    def reportMessageType_cb(self, index, fieldValues):
        if 'Full Log' in fieldValues[index]:
            fieldValues[index] = 'Full Log'
        return fieldValues
        
    def enable(self, enabled, disabledTooltip=None):
        enabled = self._parseBool(enabled)
        was_enabled = self.enabled
        self.enabled = enabled
        self.mandatory = self.mandatory and self.enabled
        if self.enabled:
            self.tooltip = self.oldTooltip
        else:
            if was_enabled:
                self.oldTooltip = self.tooltip
            self.tooltip = disabledTooltip or ''    
    
    def GetVariables(self):
        return self.ael_variables

ael_variables = MarkitAelVariables().GetVariables()

def ael_main(dict): 
    dict['ScriptName'] = 'Markit Securities Finance'
    try:
        with Transaction():
            FMarkitPerform.execute_perform(MarkitPopulateData.perform, dict)
    except Exception as e:
        print(datetime.datetime.now().strftime('%H:%M:%S'), str(e))
