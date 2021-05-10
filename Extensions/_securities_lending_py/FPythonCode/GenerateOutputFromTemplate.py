""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/GenerateOutputFromTemplate.py"
"""------------------------------------------------------------------------------------------------
MODULE
    GenerateOutputFromTemplate

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Generate Output From Template

------------------------------------------------------------------------------------------------"""

import acm
from FReportAPI import FWorksheetReportApiParameters
from FReportAPIBase import FReportBuilder
from FReportAPIBaseUtils import logger
import FReportUtils

class WorksheetReportWithStringReturn(FReportBuilder):
    def generateOutputAsString(self, reportXml):
        return FReportUtils.transformXML(reportXml, self.params.secondaryTemplate)
        
    def produceOutput(self, reportXml):
        self.outputAsString = ''
        if self.params.fileDestination == 'Clipboard':
            self.outputAsString = self.generateOutputAsString(reportXml)
        else:
            FReportBuilder.produceOutput(self, reportXml)
            self.outputAsString = self.generatedFilePaths[0]

class WorksheetReportWithStringReturnAPI(FWorksheetReportApiParameters):
    def RunScript(self):
        report_generator = WorksheetReportWithStringReturn(self)
        report_generator.generateReport()
        return report_generator.outputAsString

class ReportGenerator(object):
    def CreateReport(self, fileDestination, trades, fileName, filePath, fileType, sheetTemplate, outputTemplate):
        output = WorksheetReportWithStringReturnAPI()
        output.fileDestination = fileDestination
        
        output.template = sheetTemplate
        output.trades = trades
        output.htmlToFile = False
        output.htmlToScreen = False
        output.createDirectoryWithDate = False
        
        output.fileDateFormat = '%Y%m%d_%H%M%S'
        output.secondaryOutput = True
        output.secondaryTemplate = outputTemplate
        output.includeDefaultData = False
        output.includeFormattedData = True
        output.includeColorInformation = False
        
        if fileDestination not in ['Clipboard']:
            output.fileName = str(fileName + '_')
            output.filePath = filePath
            output.secondaryFileExtension = fileType
            
        logger.Reinitialize(level=3, logOnce=True)
        return output.RunScript()
