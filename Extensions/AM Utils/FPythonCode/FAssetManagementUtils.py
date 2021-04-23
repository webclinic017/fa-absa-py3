""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FAssetManagementUtils.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FAssetManagementUtils

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    A collection of helper classes and functions for Asset Management modules.

-------------------------------------------------------------------------------------------------"""
import FLogger
import acm

logDict = {
    '1. Normal': 1,
    '2. Warnings/Errors': 3,
    '3. Debug': 2
    }

def GetLogger(name='AMI'):
    return FLogger.FLogger.GetLogger(name)

logger = GetLogger()

def ReinitializeLogger(logMode):
    logger.Reinitialize(level=logMode,
                        keep=None,
                        logOnce=None,
                        logToConsole=1,
                        logToPrime=None,
                        logToFileAtSpecifiedPath=None,
                        filters=None,
                        lock=None)


def CreateAdditionalInfo(name, recType, dataTypeGroup, dataTypeType, description='', subTypes=[]):
    # pylint: disable-msg=W0102
    addInfoSpec = acm.FAdditionalInfoSpec[name]
    if addInfoSpec:
        logger.debug('AdditionalInfoSpec with name "%s" already exists' % name)
        return addInfoSpec

    enumNameForDataTypes = 'B92StandardType' if dataTypeGroup == 'Standard' else 'B92RecordType'
    try:
        dataTypeTypeAsInt = acm.FEnumeration['enum(' + enumNameForDataTypes + ')'].Enumeration(dataTypeType)
    except RuntimeError as err:
        logger.error('Failed to translate %s to data type for AdditionalInfoSpec "%s" on %s: %s'
                     % (dataTypeType, name, recType, err))
        raise

    addInfoSpec = acm.FAdditionalInfoSpec(name=name,
                                          recType=recType,
                                          dataTypeGroup=dataTypeGroup,
                                          description=description,
                                          dataTypeType=dataTypeTypeAsInt)
    for subType in subTypes:
        addInfoSpec.AddSubType(subType)
    try:
        addInfoSpec.Commit()
    except Exception as err:
        logger.error('Failed commit AdditionalInfoSpec "%s" on %s: %s' % (name, recType, err))
        raise

    logger.info('Created AdditionalInfoSpec "%s" on %s' % (name, recType))
    return addInfoSpec

def ToFList(oldList):
    newlist = acm.FList()
    for obj in oldList:
        newlist.Add(obj)
    return newlist

def SelectedInstruments(selection):
    rowObjects = selection.SelectedRowObjects()
    if rowObjects and rowObjects[0].IsKindOf(acm.FDistributedRow):
        try:
            return [rowObj.SingleInstrumentOrSingleTrade()
                    for rowObj in rowObjects]
        except RuntimeError:
            return []
    return selection.SelectedInstruments() or []

def Instruments(extensionObject):
    if extensionObject.IsKindOf(acm.CInsDefAppFrame):
        return ToFList([extensionObject.OriginalInstrument()])
    elif extensionObject.IsKindOf(acm.FUiTrdMgrFrame):
        selection = extensionObject.ActiveSheet().Selection()
        selectedInstruments = SelectedInstruments(selection)
        if selectedInstruments:
            # Convert to type FList
            return ToFList(selectedInstruments)
        elif selection.SelectedOrderBooks():
            return ToFList([ob.Instrument() for ob in selection.SelectedOrderBooks()])
        else: #No asset selected
            return []
    elif extensionObject.IsKindOf(acm.FTrade):
        return ToFList([extensionObject.Instrument()])
    elif extensionObject.IsKindOf(acm.FArray):
        if extensionObject.Size() > 0:
            if extensionObject[0].IsKindOf(acm.CInsDefAppFrame):
                return ToFList([obj.OriginalInstrument() for obj in extensionObject])
            elif extensionObject[0].IsKindOf(acm.FTrade):
                return ToFList([obj.Instrument() for obj in extensionObject])
        else:
            raise ValueError
    return extensionObject

def GetInstruments(eii):
    try:
        instruments = Instruments(eii.ExtensionObject())
    except Exception:
        instruments = []
        logger.error('Failed to retrieve instrument from extension object')
    return instruments

def MethodNameFromDomain(cls, domain):
    for attr in cls.Attributes():
        attrDomain = attr.Domain()
        if attrDomain is domain:
            return attr.Name()
        try:
            if domain.IncludesBehavior(attrDomain):
                return attr.GetMethod().Name()
        except TypeError:
            pass
    return None

def GetFunction(functionPath):
    """Returns function from functionPath('<module>.<function>')"""
    if not functionPath:
        return None
    try:
        moduleName, functionName = functionPath.split('.')
        module = __import__(moduleName)
        return getattr(module, functionName)
    except Exception as e:
        raise ValueError('Failed to get hook function for function path "{0}".'
                         'Path should be defined as "<module>.<function>".\n {1}'.format(functionPath, e))

def CallFunction(functionPath, *args):
    """Calls function in functionPath('<module>.<function>') with args as parameters"""
    function = GetFunction(functionPath)
    if function:
        return function(*args)
    else:
        return None
    