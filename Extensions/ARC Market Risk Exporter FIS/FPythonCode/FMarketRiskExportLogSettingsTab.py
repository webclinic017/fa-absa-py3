""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportLogSettingsTab.py"
"""----------------------------------------------------------------------------
MODULE
    FMarketRiskExportLogSettingsTab - General output settings

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FMarketRiskExport GUI which contains settings
    which are changed frequently, e.g. name of the report.

----------------------------------------------------------------------------"""

import FRunScriptGUI
import FBDPWorld

class MarketRiskExportLogSettingsTab(FRunScriptGUI.AelVariablesHandler):

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

    def __init__(self):

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

        messageTypes = ['Full Log', 'START', 'FINISH', 'ABORT', 'ERROR',
                'WARNING', 'NOTIME', 'INFO', 'DEBUG']
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['Logmode',
                        'Logmode_Logging',
                        'int', [0, 1, 2], 0,
                        2, 0, ttLogMode],
                ['LogToConsole',
                        'Log to console_Logging',
                        'int', [1, 0], 1,
                        1, 0, ttLogToCon],
                ['LogToFile',
                        'Log to file_Logging',
                        'int', [1, 0], 1,
                        1, 0, ttLogToFile, self.logfile_cb],
                ['Logfile',
                        'Logfile_Logging',
                        'string', None, 'c:\\temp\\market_risk_export.log',
                        0, 0, ttLogFile, None, None],
                ['SendReportByMail',
                        'Send report by mail_Logging',
                        'int', [1, 0], None,
                        0, 0, ttSendReportByMail, self.sendReportByMail_cb],
                ['MailList',
                        'MailList_Logging',
                        'string', None, None,
                        0, 0, ttMailList],
                ['ReportMessageType',
                        'ReportMessageType_Logging',
                        'string', messageTypes, 'Full Log',
                        2, 1, ttReportMessageType, self.reportMessageType_cb]
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)


def getAelVariables():
    outtab = MarketRiskExportLogSettingsTab()
    outtab.LoadDefaultValues(__name__)
    return outtab

def logger_setup(ael_variables):
    logger = FBDPWorld.CreateWorld(ael_variables)
    return logger
