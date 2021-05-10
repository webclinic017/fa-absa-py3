""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsIO.py"
import acm, os

from FOperationsExceptions import InvalidInputException

#-------------------------------------------------------------------------
def ShowInvalidDataDialog(msgString, shell):
    acm.UX().Dialogs().MessageBox(shell, 'Error', msgString, 'Close', None, None, 'Button1', 'Button1')

#-------------------------------------------------------------------------
def GetDefaultPath():
    return "c:\\Temp\\"

#-------------------------------------------------------------------------
def IsValidFileLogParameters(logFilePath, logFileName):
    try:
        __IsValidInput(logFilePath, logFileName)
    except InvalidInputException as e:
        raise InvalidInputException('ERROR: Invalid input for file logging: {}'.format(str(e)))

#-------------------------------------------------------------------------
def __IsValidInput(logFilePath, logFileName):
    if not IsPathValid(logFilePath):
        raise InvalidInputException('Log file path does not exist.')
    if not IsFileNameValid(logFileName):
        raise InvalidInputException('Log file name contains invalid characters.')
    if not logFileName:
        raise InvalidInputException('No log file name.')    

#-------------------------------------------------------------------------
def IsPathValid(path):
    try:
        pathDirectory = str(path)
        if not os.path.exists(pathDirectory):
            raise Exception()
        return True
    except Exception as _:
        return False

#-------------------------------------------------------------------------
def IsFileNameValid(logfileName):
    invalidChars = "\\/:*<>|"
    fileName = str(logfileName)
    if __ContainsAny(fileName, invalidChars):
        return False
    return True

#-------------------------------------------------------------------------
def __ContainsAny(string, aSet):
    return 1 in [c in string for c in aSet]
