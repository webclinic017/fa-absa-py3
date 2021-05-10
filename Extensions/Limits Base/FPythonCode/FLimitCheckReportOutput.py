""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitCheckReportOutput.py"
"""--------------------------------------------------------------------------
MODULE
    FLimitCheckReportOutput

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Functionality for producing reports of limit checks

-----------------------------------------------------------------------------"""

import acm
import FLimitSettings
import FAssetManagementUtils
import FFileUtils
import os
logger = FAssetManagementUtils.GetLogger()


class XmlReportOutputBase(object):

    def __init__(self, name, writer = None):
        self.name = name
        self.writer = writer
        
    def Writer(self):
        if self.writer is None:
            self.writer = self.CreateXmlReportOutput()
        return self.writer

    def CreateXmlReportOutput(self):
        raise NotImplementedError
        
    def StoreAndGenerateKey(self):
        return self.name


class XmlReportOutputFile(XmlReportOutputBase):

    SEPARATOR = ' '
    FILE_TYPE = '.xml'
        
    def CreateDirectory(self):
        return FFileUtils.createDirectory(
                FLimitSettings.ReportDir(), 
                FLimitSettings.SubDirName(), 
                FLimitSettings.DirNameDateFormat(),
                self.SEPARATOR)
        
    def FilePath(self):
        return FFileUtils.getFilePath(
                self.CreateDirectory(), 
                self.name, 
                self.FILE_TYPE, 
                FLimitSettings.FileNameDateFormat(), 
                FLimitSettings.DateInFileNameBeginning(), 
                FLimitSettings.Overwrite(), 
                FLimitSettings.MaximumReportsInPath(), 
                self.SEPARATOR)
        
    def CreateXmlReportOutput(self):
        output = acm.FXmlReportOutputFile( self.FilePath() )
        output.EnableWhitespace = False
        output.IncludeColorInformation = True
        output.IncludeFormattedData( True )
        output.IncludeRawData( False )
        output.IncludeFullData( False )
        return output
        
    def StoreAndGenerateKey(self):
        return os.path.relpath(str(self.Writer().Name()), FLimitSettings.ReportDir())

class XmlReportOutput(XmlReportOutputBase):

    SEPARATOR = ' '
    PREFIX = 'LimitCheckReport'
    
    @staticmethod
    def CreateXmlReportOutput():
        writer = acm.FXmlReportOutput( "" ) 
        writer.EnableWhitespace = False
        writer.IncludeColorInformation = True
        writer.IncludeFormattedData( True )
        writer.IncludeRawData( False )
        writer.IncludeFullData( False )
        return writer
        
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
            
    def LimitCheckReport(self):
        suggested_name = '_'.join((self.PREFIX, self.name))
        if FLimitSettings.Overwrite():
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
        archive = self.LimitCheckReport()
        archive.XmlData(self.Writer().AsString())
        archive.Commit()
        return str(archive.Oid())

    @staticmethod
    def ArchiveOrNone( filename ):
        try:
            return acm.FLimitCheckReport.Select('name="{0}"'.format(filename))[0]
        except IndexError:
            return 
