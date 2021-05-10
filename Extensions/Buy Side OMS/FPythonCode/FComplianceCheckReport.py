""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FComplianceCheckReport.py"
"""--------------------------------------------------------------------------
MODULE
    FComplianceCheckReport

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Functionality for producing reports of compliance checks

-----------------------------------------------------------------------------"""
import os
import acm
import FSheetUtils
import FFileUtils
from FParameterSettings import ParameterSettingsCreator

SETTINGS = ParameterSettingsCreator.FromRootParameter('ComplianceCheckReportSettings')


class ComplianceCheckReport(object):

    def __init__(self, output):
        self._alerts = None
        self._reportName = ' '.join((SETTINGS.ReportName(), acm.Time.TimeNow()))
        self._report = acm.Report.CreateReport(self._reportName, output)
        self._reportGrid = self.CreateDefaultReportGrid()
        
    def GridBuilder(self):
        return self._reportGrid.GridBuilder()
        
    def Report(self):
        return self._report
   
    def Generate(self, alerts):
        self._SetColumnCreators()
        self.GridBuilder().InsertItem(alerts)
        self._SaveReport()
        
    def _SaveReport(self):       
        self._reportGrid.Generate()
            
    def CreateDefaultReportGrid(self, includeInsAndLeg=True, includeRows=True):
        gridConfig = acm.Report.CreateGridConfiguration(includeInsAndLeg, includeRows)
        return self.Report().OpenSheet(acm.FAlertSheet(), gridConfig, None)
        
    def _SetColumnCreators(self):
        columnIds = FSheetUtils.ColumnIds('_defaultColumnsAlertSheet', "FAlertSheet")
        columnCreators = FSheetUtils.ColumnCreators(columnIds)
        i = 0
        while i < columnCreators.Size():
            creator = columnCreators.At(i)
            self.GridBuilder().ColumnCreators().Add(creator)
            i = i + 1


class XmlReportOutputBase(object):
    
    SEPARATOR = ' '
    
    def __init__(self, name, writer = None):
        self.name = name
        self.writer = writer
        
    def Writer(self):
        if self.writer is None:
            self.writer = self.CreateXmlReportOutput()
            self.writer.IncludeColorInformation(True)
            self.writer.IncludeFormattedData(True)
            self.writer.IncludeRawData(False)
            self.writer.IncludeFullData(False)
        return self.writer

    def CreateXmlReportOutput(self):
        raise NotImplementedError
        
    def StoreAndGenerateKey(self):
        return self.name

class XmlReportOutputFile(XmlReportOutputBase):

    FILE_TYPE = '.xml'
        
    def CreateDirectory(self):
        return FFileUtils.createDirectory(
                r'{0}'.format(SETTINGS.ReportDir()), 
                SETTINGS.SubDir(), 
                dirNameSeparator=self.SEPARATOR)
        
    def FilePath(self):
        return FFileUtils.getFilePath(
                self.CreateDirectory(), 
                self.name, 
                self.FILE_TYPE,  
                dateBeginning=True,
                overwriteIfFileExists=SETTINGS.Overwrite(),
                fileNameSeparator=self.SEPARATOR)
        
    def CreateXmlReportOutput(self):
        output = acm.FXmlReportOutputFile(self.FilePath())
        output.EnableWhitespace(True)
        return output
        
    def StoreAndGenerateKey(self):
        return os.path.relpath(str(self.Writer().Name()), r'{0}'.format(SETTINGS.ReportDir()))

class XmlReportOutput(XmlReportOutputBase):

    PREFIX = 'ComplianceCheckReport'
    
    def CreateXmlReportOutput(self):
        output = acm.FXmlReportOutput("") 
        output.EnableWhitespace(False)
        return output
        
    @staticmethod
    def CreateFile(archiveName):
        archive = acm.FLimitCheckReport()
        archive.Name(archiveName)
        archive.AutoUser(False)
        return archive

    def GetNextArchiveName(self, suggested_name):
        i=1
        newFileName = suggested_name
        while self.ArchiveOrNone(newFileName) is not None:
            if i == 1:
                numbering = ''
            else:
                numbering = '#' + str(i)
            newFileName = suggested_name + numbering
            i = i + 1
        return newFileName
            
    def LimitCheckReportTextObject(self):
        suggested_name = '_'.join((self.PREFIX, self.name))
        if SETTINGS.Overwrite():
            existingFile = self.ArchiveOrNone(suggested_name)
            if not existingFile:
                file = self.CreateFile(suggested_name)
            else:       
                file = existingFile.StorageImage()
        else:
            fileName = self.GetNextArchiveName(suggested_name)
            file = self.CreateFile(fileName)
        return file
        
    def StoreAndGenerateKey(self):
        archive = self.LimitCheckReportTextObject()
        archive.XmlData(self.Writer().AsString())
        archive.Commit()
        return str(archive.Oid())

    @staticmethod
    def ArchiveOrNone(filename):
        try:
            return acm.FLimitCheckReport.Select('name="{0}"'.format(filename))[0]
        except IndexError:
            return 

def CreateComplianceReportFile(alerts, name):
        if SETTINGS.Storage() == 'ADS':
            output = XmlReportOutput(name)
        elif SETTINGS.Storage()  == 'File':
            output = XmlReportOutputFile(name)
        else:
            logger.error('Unknown storage place %s'%STORAGE)
            return
        ComplianceCheckReport(output.Writer()).Generate(alerts)
        return output.StoreAndGenerateKey()
