""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/GenerateOrderReportAPI.py"
"""------------------------------------------------------------------------------------------------
MODULE
    GenerateOrderReportAPI

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    API to generate Report

------------------------------------------------------------------------------------------------"""

from MatchToReportTemplate import MatchToReportTemplateHelper 
from GenerateOutputFromTemplate import ReportGenerator

def GetReportParameters(fileDestination, counterparty):
    helper = MatchToReportTemplateHelper()
    filePath, fileType, sheetTemplate, outputTemplate, reportName = helper.MatchToReportCreateInfo(fileDestination, counterparty)
    if fileDestination != 'Clipboard' and not (filePath and fileType and reportName):
        msg = 'File Export not setup correctly for Counterparty %s and Destination %s.' % (counterparty and counterparty.Name(), fileDestination)
        if not filePath:
            msg += " Path can not be empty."
        if not fileType:
            msg += " File type can not be empty."
        if not reportName:
            msg += " Report name can not be empty."
        raise Exception(msg)
    return filePath, fileType, sheetTemplate, outputTemplate, reportName
  
def GenerateOrderReport(trades, fileDestination, counterparty):
    filePath, fileType, sheetTemplate, outputTemplate, reportName = GetReportParameters(fileDestination, counterparty)
    return ReportGenerator().CreateReport(fileDestination, trades, reportName, filePath, fileType, sheetTemplate, outputTemplate)

