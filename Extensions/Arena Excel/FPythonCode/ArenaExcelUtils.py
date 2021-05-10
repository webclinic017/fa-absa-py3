""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/ArenaExcelUtils.py"
import acm
import FLogger

def GetLogger(name='Arena Excel'):
    aLogger = FLogger.FLogger.GetLogger(name)
    return aLogger

def SetLoggingLevel(aLogger, level):
    ''' Levels are 1-4 signifying
        1: Info: get warnings, errors and info
        2: Debug: get everything
        3: Warn: get warnings and errors
        4: Error: get only errors
    '''
    aLogger.Reinitialize(level=level)


logger = GetLogger()

def GetSettings(name):
    return acm.GetDefaultContext().GetExtension('FParameters', 
                                                'FObject', 
                                                name).Value()
                                                
def ClipboardSettings():
    return GetSettings('ClipboardSettings')
