"""-------------------------------------------------------------------------------------------------------
MODULE
    FFileUtils - General file output functions

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    Utility functions for creating directories and generating file names.

-------------------------------------------------------------------------------------------------------"""
import acm
import os
import re
import time
import platform

def expandEnvironmentVar(path):
    regex = "";    
    if platform.system() == 'Windows':
        regex = r"\%\{?(\w+)\}?\%"
    elif platform.system() == 'Unix':
        regex = r"\$\{?(\w+)\}?"                        
        
    for var in re.compile(regex).findall(path):    
        try:
            val = os.environ[var]
        except KeyError:
            continue #Just ignore, someone could have named a folder with the environment symbol in their folder and expect it to work...                
        if platform.system() == 'Windows' :
            path = path.replace('%' + var + '%', val)
        elif platform.system() == 'Unix' :            
            path = path.replace( "$%s"%var, val ).replace( "${%s}"%var, val )        
    return path

def getFilePath(dirPath, fileName, fileExtension, dateFormat = None, dateBeginning = False, overwriteIfFileExists = True, maxNrOfFilesInDir = 256, fileNameSeparator = ''):
    if (fileName is None) or fileName == '':
        msg = 'FFileUtils.getFilePath: parameter fileName is None or empty'
        raise Exception(msg)

    if (fileExtension is None) or fileExtension == '':
        msg = 'FFileUtils.getFilePath: parameter fileExtension is None or empty'
        raise Exception(msg)

    # Add date to file name?
    if dateFormat and dateFormat != '':
        if dateBeginning:
            fileName = fileNameSeparator.join((time.strftime(dateFormat), fileName))
        else:
            fileName = fileNameSeparator.join((fileName, time.strftime(dateFormat)))

    if overwriteIfFileExists:
        return os.path.join(dirPath, fileName + fileExtension)
        
    for i in range(1, int(maxNrOfFilesInDir) + 1):
        if i == 1:
            numbering = ''
        else:
            numbering = '_' + str(i)
        testFile = os.path.join(dirPath, fileName + numbering + fileExtension)
        if not os.path.exists(testFile):
            return testFile
    msg = 'FFileUtils.getFilePath: Maximum number of files (' + str(maxNrOfFilesInDir) + ') in directory has been exceeded'
    raise Exception(msg)


def createDirectory(dirPath, dirName, dirDateFormat = None, dirNameSeparator = ''):
    newDir = None
    
    if dirPath is None:
        msg = 'FFileUtils.createDirectory: parameter dirPath is None'
        raise Exception(msg)
    
    if isinstance(dirPath, basestring):
        newDir = dirPath
    else:
        newDir = dirPath.AsString()
        
    if dirName and dirName != '':
        if dirDateFormat and dirDateFormat != '':
            newDir = os.path.join(newDir, dirNameSeparator.join((dirName, time.strftime(dirDateFormat))) + os.sep)
        else:
            newDir = os.path.join(newDir, dirName + os.sep )

    if newDir == '':
        msg = 'FFileUtils.createDirectory: new directory is empty string'
        raise Exception(msg)

    newDir = expandEnvironmentVar(newDir)

    if not os.path.exists(newDir):
        try:
            os.makedirs(newDir)
        except:
            msg = 'FFileUtils.createDirectory: Failed to create directory: ' + newDir
            raise Exception(msg)
    return newDir
