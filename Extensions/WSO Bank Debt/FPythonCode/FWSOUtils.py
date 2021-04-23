""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSOUtils - 

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Global provider of utility methods.
    
-------------------------------------------------------------------------------------------------------"""

import acm
import FLogger


class WsoLogger(object):

    @staticmethod
    def ReinitializeLogger(wsoLogger, logLevel):
        wsoLogger.Reinitialize(level=logLevel,
                            keep=None,
                            logOnce=None,
                            logToConsole=1,
                            logToPrime=None,
                            logToFileAtSpecifiedPath=None,
                            filters=None,
                            lock=None)
        
    @classmethod
    def GetLogger(cls):
        """ Returns the FLogger instance """
        wsoLogger = FLogger.FLogger.GetLogger('WSO')
        cls.ReinitializeLogger(wsoLogger, 2)
        return wsoLogger


logger = WsoLogger.GetLogger()


class WSOUtils(object):
    ''' Utility methods used by modules in the shipped module. 
    '''
        
    @classmethod
    def StripSpaces(cls, stringToStrip):
        return stringToStrip.strip(' ')    
    
    @classmethod
    def RemoveUTFCharacters(cls, string):
        if string == None:
            return None
        import unicodedata
        string = unicodedata.normalize('NFKD', str(string)).encode('ascii', 'ignore')
        string = string[0:63]
        string = cls.StripSpaces(string)
        return string 
        
    @classmethod
    def AsFloat(cls, value):
        try:
            value = float(value)
        except:
            logger.error('Cannot convert value %s of type %s to a floating point number.' \
                          % (value, value.__class__.__name__))
        return value

    @classmethod
    def AsDate(cls, dateString):
        return dateString[0:10]


class ParameterReader(object):
    ''' (This class is to be moved to a utils-module)
        Responsible for retrieving pre-specified FParameter values.
        [Module]FObject:ExtensionName =
                    ParamName=ParamValue
                    [...]
    '''
    FWSO_DIRECTORY = 'FWSODirectory'
    FWSO_DIRPATH_KEY = 'WSO_DIRPATH'

    @classmethod
    def _GetParamValue(cls, extensionName, paramName):
        ''' Retrieves the value of an FParameter-instance '''
        defaultContext = acm.GetDefaultContext()
        paramExtensions = defaultContext.GetAllExtensions('FParameters', 'FObject', True, True, '', '', False)
        for extension in paramExtensions:
            if extension.StringKey() != extensionName:
                continue
            paramsInstance = extension.Value()
            paramValue = paramsInstance.GetString(paramName, None)
            return paramValue
        return None

    @classmethod
    def WSODirPath(cls):
        ''' Returns the WSO directory path from FParameters '''
        dirPath = cls._GetParamValue(cls.FWSO_DIRECTORY, cls.FWSO_DIRPATH_KEY)
        return dirPath


# Exception classes

class UploadException(Exception):
    ''' Base class for upload errors '''
    pass
    

class MissingDataException(UploadException):
    ''' Raised when WSO data is incomplete '''
    pass

class MissingDataSourceException(MissingDataException):
    pass    

class MissingPositionException(MissingDataException):
    pass
