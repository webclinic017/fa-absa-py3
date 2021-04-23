""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FColumnToXMLGenerator.py"
""" Compiled: 2017-08-02 17:42:32 """

#__src_file__ = "extensions/export/./etc/FColumnToXMLGenerator.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FColumnToXMLGenerator

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    See ExportBaseReadMe.py for more information about this module

-------------------------------------------------------------------------------------------------------"""
import acm
import FExportUtils
import FLogger
logger = FLogger.FLogger.GetLogger("BD Export")



class FColumnToXMLGenerator():

    def __init__(self, exporterProcess):
        assert (exporterProcess)
        self._exportProcess = exporterProcess

    def Execute(self, validateOutput=True):
        """
        This will generate XMLs based on information within the ExportProcess
        """
        integrationId = self._exportProcess.Integration().Id()
        for key, singleExport in self._exportProcess:
            if not singleExport.IsExportable() and not self._exportProcess.GenerateEmptyFile():
                continue
            try:
                sheetTemplate = acm.FTradingSheetTemplate[singleExport.SheetTemplateId()]
                sheetTemplate.TradingSheet().RemoveAllRows()
                xmlReportWriter = _FXMLReportWriter(singleExport.SheetTemplateId(), integrationId + str(key))
                for businessProcess in singleExport.ExportableBusinessProcesses():
                    subject = businessProcess.Subject()
                    try:
                        xmlReportWriter.AddObjectToSheet(subject)
                    except Exception as error:
                        raise Exception("XML generation error for %s %i (sheet template '%s'): %s" % \
                            (subject.ClassName(), subject.Oid(), singleExport.SheetTemplateId(), error))

                xmlOutput = xmlReportWriter.GetXMLOutput()
                assert(xmlOutput)
                if validateOutput and not self._exportProcess.GenerateEmptyFile():
                    try:
                        xmlReportWriter.ValidateXMLOutput(xmlOutput)
                    except ValueError as error:
                        raise Exception('Generated report failed validation: ' + str(error))
                singleExport.XMLData(xmlOutput)
            except Exception as error:
                logger.error(error)
                singleExport.Failed(error)


class _FXMLReportWriter():

    def __init__(self, sheetTemplateName, reportName = ''):
        self._XMLoutput = acm.FXmlReportOutput('')
        self._XMLoutput.IncludeRawData(True)
        self._XMLoutput.IncludeFullData(True)
        self._XMLoutput.IncludeFormattedData(True)
        self._config = acm.Report.CreateGridConfiguration(False, True)
        self._grid = acm.Report.CreateReport(reportName, self._XMLoutput)
        try:
            self._grid.OpenSheetTemplate(sheetTemplateName, self._config)
        except TypeError:
            errStr = "Could not open sheet template named '%s'" % (sheetTemplateName)
            logger.error(errStr)
            raise
        self._gridBuilder = self._grid.GridBuilder()
        self._rows = []

    def AddObjectToSheet(self, rowObject):
        self._gridBuilder.InsertItem(rowObject)
        self._rows.append(rowObject)

    def GetXMLOutput(self):
        self._grid.Generate()
        return self._XMLoutput.AsString()

    def ValidateXMLOutput(self, xml):
        import xml.etree.ElementTree as et
        root = et.fromstring(xml)
        columnIds = [node.text for node in root.findall('.//Table/Columns/Column/ColumnId')]
        for i, row in enumerate(root.findall('.//Table/Rows/Row')):
            for j, column in enumerate(row.findall('.//Cell')):
                try:
                    if column.find('ValueType').text == 'StaticError':
                        errorText = column.find('RawData').text
                        raise ValueError('Row object %s %d has invalid value for column "%s": %s' % \
                                (self._rows[i].ClassName(), self._rows[i].Oid(), columnIds[j], errorText))
                except AttributeError:
                    pass
