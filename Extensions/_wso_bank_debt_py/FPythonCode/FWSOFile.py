""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOFile.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSOFile -

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Responsible for reading data from WSO XML-file and making it accessible via a class.

-------------------------------------------------------------------------------------------------------"""

from FWSOFileFormatHook import ParseXMLReconciliationDocument


class WSOFile(object):
    ''' Represents a WSO file. Can construct an item handler-object
        from where the data can easily be accessed.
    '''
    def __init__(self, filePath, primaryKeyName):
        self.filePath = filePath
        self.primaryKeyName = primaryKeyName
        
    def WsoDict(self):
        wsoDict = dict()
        fileHandler = open(self.filePath, 'r')
        itemDicts = ParseXMLReconciliationDocument(fileHandler)
        
        for itemDict in itemDicts:
            primaryKey = itemDict.get(self.primaryKeyName)
            wsoDict[primaryKey] = itemDict
        return wsoDict
