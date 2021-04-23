""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FileCreator.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FFileCreator

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    See ExportBaseReadMe.py for more information about this module

-------------------------------------------------------------------------------------------------------"""
import os

import acm
import FLogger

logger = FLogger.FLogger.GetLogger("BD Export")

class FFileCreator():

    def __init__(self, exportProcess, header, footer):
        self._exportProcess = exportProcess
        self.header=header
        self.footer=footer

    @classmethod
    def _GetFilePath(cls, filePath, fileName):
        return os.path.join(filePath, fileName)

    @classmethod
    def _TransformXml(cls, reportXml, xslTemplate):
        transformedXML = None
        pt = acm.GetDefaultContext().GetExtension('FXSLTemplate', 'FObject', xslTemplate)
        if not pt:
            raise ValueError("Failed to load XSLT template " + xslTemplate)
        xsl = pt.Value()
        try:
            transformer = acm.CreateWithParameter('FXSLTTransform', xsl)
            transformedXML = transformer.Transform(reportXml)
        except StandardError as err:
            raise StandardError("Failed to transform XML: " + str(err)) 
        return transformedXML

    @classmethod
    def _AssertFileData(cls, reportXml, xslTemplate, filePath):
        assert(reportXml), "XML data missing"
        assert(xslTemplate), "XSLTemplate missing"
        assert(filePath), "No file path set"

    @classmethod
    def _GetFileData(cls, singleExport):
        reportXml = singleExport.XMLData()
        xsltTemplate = singleExport.Integration().XSLTTemplateFinderFunction()(singleExport.SingleExportIdentifier())
        filePath = cls._GetFilePath(singleExport.FilePath(), singleExport.Filename())
        cls._AssertFileData(reportXml, xsltTemplate, filePath)
        return reportXml, xsltTemplate, filePath

    def _WriteFile(self, reportXml, xslTemplate, filePath):
        #generate empty a file if no header as well
        output = self._TransformXml(reportXml, xslTemplate)
        if not output and not self._exportProcess.GenerateEmptyFile(): 
            raise ValueError('Transformed XML report using template "%s" is empty' % xslTemplate)
        try:
            with open(filePath, "wb") as outputFile:
                outputFile.write(self.header)
                if self.header!='':
                    outputFile.write("\r\n")
                outputFile.write(output)
                outputFile.write("\r\n")
                outputFile.write(self.footer)
            logger.info("Writing output file to %s", filePath)
        except IOError as e:
            raise StandardError("Failed to write file: " + str(e))
            
    def Execute(self):
        """
        This will write the output files based on information within the ExportProcess
        """
        for singleExport in self._exportProcess.SingleExportsAsList():
            if not singleExport.IsExportable() and not self._exportProcess.GenerateEmptyFile():
                continue
            try:
                reportXml, xsltTemplate, filePath = self._GetFileData(singleExport)
                self._WriteFile(reportXml, xsltTemplate, filePath)
            except StandardError as e:
                errStr = 'Failed to transform xml and write it to file: ' + str(e)
                logger.error(errStr)
                singleExport.Failed(errStr)