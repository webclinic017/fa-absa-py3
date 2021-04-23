""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSODirToWSODict.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSODirToWSODict -

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FWSOFile import WSOFile
from FWSOUtils import ParameterReader, WsoLogger
import os

logger = WsoLogger.GetLogger()


class DefaultWSOFileTypeFinder(object):
    ''' Returns dictionary where keys are the WSO types and the
        values are the filepaths to the corresponding file.
        WSO types are identified based on occurence in file name.
    '''    
    
    # Note: Order is important for ContractDetail vs. Contract
    WSO_TYPES = [
        'AssetBase',
        'Bank',
        'ContractDetail',
        'Contract',
        'Facility',
        'Issuer',
        'Portfolio',
        'Position',
        'Trade',
    ]

    @classmethod
    def _FilePath(cls, dirPath, fileName):
        return os.path.join(dirPath, fileName)

    @classmethod
    def WSOFilesInDir(cls, dirPath):
        wsoFilesInDir = dict()
        for fileName in os.listdir(dirPath):
            filePath = cls._FilePath(dirPath, fileName)
            isFile = os.path.isfile(filePath)
            if not isFile:
                continue
            for wsoType in cls.WSO_TYPES:
                if not wsoType in fileName:
                    continue
                key = wsoType
                if wsoType == 'AssetBase':
                    key = 'Asset'
                wsoFilesInDir[key] = filePath
                break
        return wsoFilesInDir


def SingletonDecorator(cls):
    instances = {}
    def getinstance(*args):
        if cls.__name__ not in instances.keys():
            instances[cls.__name__] = cls(*args)
        return instances[cls.__name__]
    return getinstance


@SingletonDecorator
class WSODirToWSODict(object):
    ''' Responsible for returning WSO XML dictionaries based on the
        WSO Types (e.g. Contract, Position etc.). Dictionaries use the
        WSO data attributes and values.
    '''

    def __init__(self, dirPath = None):
        self.dirPath = self.WSODirPath()
        dirExists = os.path.isdir(self.dirPath)
        if not dirExists:
            raise Exception('Invalid directory path: %s' % self.dirPath)
        self.wsoDicts = self._WSODicts()

    def ClearCache(self):
        ''' Clears the singletonian cache memory. This method must be called
            if the external directory has changed, i.e. if files have been
            added, removed, or modified, or if the files have been moved to a
            new file location. Note that this method does not release
            the memory of the singletonian itself, but its constituents; thus
            the values of the singletonian must be read all over again. '''

        logger.debug('Clearing cached memory...')
        self.dirPath = None
        self.wsoDicts = None
        assert self.dirPath is None
        assert self.wsoDicts is None
        logger.debug('Successfully cleared cached memory.')
        return True

    @classmethod
    def WSODirPath(cls):
        ''' Returns the path to the directory with WSO files to be read '''
        return ParameterReader.WSODirPath()

    def WSOFilesInDir(self):
        ''' Returns a dictionary where the keys are the WSO types (e.g. Trade,
            Facility etc.) and the values are the file paths to the corresponding
            WSO XML file. Looks first for a hook function. If it exists it will be called 
            and the result will be returned.
            Hook function:
                Signature: WSOFilesInDir(dirPath)
                Returns: A dictionary. Keys are the WSO file types (Facility, Trade etc.)
                            and values are the file paths to each corresponding XML.
        '''
        try:
            import FWSOCustomHooks
            wsoFilePathsDict = FWSOCustomHooks.WSOFilesInDir(self.WSODirPath())
            return wsoFilePathsDict
        except ImportError:
            logger.debug('A custom hook function has not been defined for identifying WSO files. Using default logic.')
        except AttributeError:
            logger.debug('A custom hook function has not been defined for identifying WSO files. Using default logic.')
        except Exception as e:
            logger.error('An error occurred when calling the hook function WSOFilesInDir: %s' % e)
        return DefaultWSOFileTypeFinder.WSOFilesInDir(self.WSODirPath())

    def _PrimaryKeyFromWSOType(self, wsoType):
        ''' Returns the primary key of a WSO Type (needs to be revised
            in case new WSO file types are used in the future).
        '''
        if wsoType == 'ContractDetail':
            return 'ContractIPF_ID'
        return wsoType + '_ID'

    def _WsoDictFromWsoFile(self, filePath, wsoFileType):
        ''' Creates a dictionary based on a WSO XML file, where the key is the
            primary key (e.g. TradeId or ContractId) and the value is the object
            dictionary (representing e.g. a single trade).
        '''
        wsoDict = dict()
        primaryKey = self._PrimaryKeyFromWSOType(wsoFileType)
        wsoFile = WSOFile(filePath, primaryKey)
        wsoDict = wsoFile.WsoDict()
        return wsoDict

    def _WSODicts(self):
        ''' Returns dictionary with key-value pairs wsoFileType : wsoDict
        '''
        wsoFilesInDir = self.WSOFilesInDir()
        wsoDicts = dict()
        for wsoFileType, filePath in wsoFilesInDir.items():
            wsoDict = self._WsoDictFromWsoFile(filePath, wsoFileType)
            wsoDicts[wsoFileType] = wsoDict
            logger.info('Found WSO file for %s' % wsoFileType)
        return wsoDicts

    def WSODicts(self):
        if not self.wsoDicts:
            self.wsoDicts = self._WSODicts()
        return self.wsoDicts
