""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSODemoBundle/etc/FWSOUploadFileHandler.py"
"""--------------------------------------------------------------------------
MODULE
    FWSOUploadFileHandler

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION


-----------------------------------------------------------------------------"""

import acm
from FWSOUtils import ParameterReader
import os

import FAssetManagementUtils
logger = FAssetManagementUtils.GetLogger()

INITIAL_UPLOAD = 'WSO Bank Debt Demo Bundle Initial Upload'
SECONDARY_UPLOAD = 'WSO Bank Debt Demo Bundle Secondary Upload'


class WSOUploadFileHandler():
    
    @classmethod
    def _WSOPrefix(cls):
        return 'WSODemo'
    
    @classmethod
    def _WSOSuffix(cls):
        return 'XML'
    
    @classmethod
    def _FileFormatExtension(cls):
        return '.xml'
    
    @classmethod
    def _WSOTypes(cls):
        from FWSODirToWSODict import DefaultWSOFileTypeFinder               
        return DefaultWSOFileTypeFinder.WSO_TYPES            

    @classmethod
    def _DirPath(cls, checkIfDirExists = True):
        defaultPath = ParameterReader.WSODirPath()  
        if checkIfDirExists:
            cls._MakeDirIfNeeded(defaultPath)
        return defaultPath
        
    @classmethod
    def _MakeDirIfNeeded(cls, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        assert os.path.exists(directory)
        
    @classmethod        
    def _ConcatenateWSOTypeWithUploadNbr(cls, uploadName, WSO_COMPARISON_TYPES, wsoType):
        if uploadName in (INITIAL_UPLOAD,) or (uploadName in (SECONDARY_UPLOAD,) and not wsoType in WSO_COMPARISON_TYPES):
            return False      
        elif uploadName in (SECONDARY_UPLOAD,) and wsoType in WSO_COMPARISON_TYPES:
            return True     
        else:
            raise Exception('WSO Demo Bundle log: The menu extension name %s was not recognized.' % uploadName)
    
    @classmethod
    def _WsoTypeEnumerated(cls, uploadName, WSO_COMPARISON_TYPES, wsoType):
        needsConcatenation = cls._ConcatenateWSOTypeWithUploadNbr(uploadName, WSO_COMPARISON_TYPES, wsoType)
        return wsoType if not needsConcatenation else wsoType + '2'
        
    @classmethod
    def DeleteAllFilesInDirectory(cls):
        dirPath = cls._DirPath(False)
        logger.info('WSO Demo Bundle log: Deleting temporary created files in %s.' % dirPath)    
        dirs = os.listdir(dirPath)
        for content in dirs:
            filePath = os.path.join(dirPath, content)
            if not os.path.isfile(filePath):
                continue
            try:
                os.remove(filePath)
                logger.info('WSO Demo Bundle log: Successfully deleted %s files from %s.' % (content, dirPath) )
            except OSError:
                raise Exception('WSO Demo Bundle log: Could not delete %s from %s' % (content, dirPath) )
        logger.info('WSO Demo Bundle log: Successfully deleted all files in directory .')                
        
    @classmethod
    def _WriteSingleFile(cls, dirPath, uploadName, WSO_COMPARISON_TYPES, wsoType, wsoPrefix, wsoSuffix):
        wsoTypeEnumerated = cls._WsoTypeEnumerated(uploadName, WSO_COMPARISON_TYPES, wsoType)
        extValName = wsoPrefix + wsoTypeEnumerated + wsoSuffix
        extValues = acm.GetDefaultContext().GetAllExtensions('FExtensionValue', extValName)    
        if extValues.IsEmpty():
            raise Exception('WSO Demo Bundle log: Did not locate WSO type %s in the extension library.' % wsoType)
        xmlString = extValues.First().Value()        
        fileName = wsoPrefix + wsoTypeEnumerated
        filePath = os.path.join(dirPath, fileName + cls._FileFormatExtension())
        try:
            fileWriterHandle =  open(filePath, 'w+')
            fileWriterHandle.write(xmlString)
        except IOError as e:
            raise Exception('WSO Demo Bundle log: Could not write WSO XML data of type %s to %s. Reason: %s' % (wsoType, filePath, e))
    
    @classmethod
    def WriteInputDataToFileSystem(cls, uploadName, WSO_COMPARISON_TYPES):
        dirPath =  cls._DirPath()  
        wsoPrefix = cls._WSOPrefix()
        wsoSuffix = cls._WSOSuffix()
        wsoTypes = cls._WSOTypes()
        for wsoType in wsoTypes:
            cls._WriteSingleFile(dirPath, uploadName, WSO_COMPARISON_TYPES, wsoType, wsoPrefix, wsoSuffix)            