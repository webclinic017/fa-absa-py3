""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsUtils.py"
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FOperationsUtils - General utility functions used by the operations scripts

    (c) Copyright 2007 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""
import acm, amb
import inspect, time

import FOperationsExceptions as Exceptions
from FOperationsEnums import BusinessEventType

detailedLogging = False
runInDebug = False
enumDict = {}
ambAddress = ''
receiverMBName = ''
receiverSource = ''

CONST_GetAMBConnection = None


def Log(logAlways, s):
    ''' Log string s if logAlways is true.  Functionality for dependency
    on the log level, similar to log should be added. '''

    if (logAlways or detailedLogging):
        if runInDebug == True:
            print(s)
        else:
            acm.Log(s)


def LogAlways(s):
    ''' Always log string s. '''
    Log(True, s)


def LogVerbose(s):
    ''' Log string s if detailed logging is enabled. '''
    Log(False, s)

def GetEnum(enumType, enumValue):
    ''' Example usage::
        GetEnum('InsType', 'Bond')
        returns the numeric representation of the enum. '''

    enum = -1
    foundInCache = False
    enumDictKey = str(enumType) + '.' + str(enumValue)
    if (enumDictKey in enumDict):
        foundInCache = True
        enum = enumDict[enumDictKey]    # Get it from the cache dict

    if not foundInCache:
        enums = acm.FEnumeration['enum(%s)' % enumType]
        if enums == None:
            raise LookupError('The enum type "%s" could not be found.' % enumType)
        try:
            enum = enums.Enumeration(enumValue)
            enumDict[enumDictKey] = enum    # Cache the enum value
        except RuntimeError as _:
            raise LookupError('Error when trying to get enum value "%s" in enum "%s"' % (enumValue, enumType))
    return enum

def SortByOid(entity1, entity2):
    """
    Compare function for sorting lists
    """
    sortResult = 0
    oid1 = entity1.Oid()
    oid2 = entity2.Oid()
    if oid1 < oid2:
        sortResult = -1
    elif oid1 > oid2:
        sortResult = 1
    return sortResult


def InitFromParameters(paramsModule, taskParameters = None):
    global detailedLogging
    global runInDebug
    global ambAddress
    global receiverMBName
    global receiverSource

    if hasattr(paramsModule, 'detailedLogging'):
        detailedLogging = paramsModule.detailedLogging
    else:
        detailedLogging = True

    if hasattr(paramsModule, 'runInDebug'):
        runInDebug = paramsModule.runInDebug
    else:
        runInDebug = False

    if hasattr(paramsModule, 'ambAddress'):
        ambAddress = paramsModule.ambAddress
    else:
        ambAddress = ''

    if (taskParameters and taskParameters.At('receiverMBName')):
        receiverMBName = taskParameters.At('receiverMBName')
    elif hasattr(paramsModule, 'receiverMBName'):
        receiverMBName = paramsModule.receiverMBName
    else:
        receiverMBName = ''

    if (taskParameters and taskParameters.At('receiverSource')):
        receiverSource = taskParameters.At('receiverSource')
    elif hasattr(paramsModule, 'receiverSource'):
        receiverSource = paramsModule.receiverSource
    else:
        receiverSource = ''

def InitAMBConnection(event_cb, dbTables):
    LogVerbose('Connecting to AMB on ' + ambAddress)
    try:
        amb.mb_init(ambAddress)
    except RuntimeError as runtimeError:
        raise Exceptions.AMBConnectionException('AMB initialisation failed:', runtimeError)

    LogVerbose('Initializing AMB reader ' + receiverMBName)
    try:
        reader = amb.mb_queue_init_reader(receiverMBName, event_cb, None)
    except RuntimeError as runtimeError:
        raise Exceptions.AMBConnectionException('Could not init reader in AMB system table:', runtimeError)

    LogVerbose('Setting up AMB subscriptions')
    for dbTable in dbTables:
        subscriptionString = receiverSource + '/' + dbTable
        try:
            amb.mb_queue_enable(reader, subscriptionString)
        except RuntimeError as runtimeError:
            raise Exceptions.AMBConnectionException('Could not set up subscriptions for ' + subscriptionString, runtimeError)

def ReconnectRoutine(eventCallback, databaseTables):
    isReconnected = False
    while True:
        LogAlways('Trying to reconnect in 20 seconds to AMB...')
        time.sleep(20.0)
        isReconnected = __Reconnect(eventCallback, databaseTables)
        if isReconnected:
            break

def __Reconnect(eventCallback, databaseTables):
    try:
        InitAMBConnection(eventCallback, databaseTables)
        LogAlways('ATS reconnected to AMB')
        print('>>> Waiting for events...\n')
        return True
    except Exceptions.AMBConnectionException:
        return False

def GetStoredQuery(queryName, queryClass):
    assert queryName, 'GetStoredQuery needs queryName as argument'
    assert queryClass, 'GetStoredQuery needs queryClass as argument'

    query = acm.FStoredASQLQuery[queryName]
    if query:
        if not (query.QueryClass() == queryClass):
            acm.Log('Error: Query %s has query class set to "%s", but "%s" was expected.' \
                % (queryName, str(query.QueryClass()), str(queryClass)))
            query = None
    else:
        acm.Log('Error: No query with name %s found. Check that the query is shared.' % (queryName))

    return query

class TradeEventType:
    NONE   = 'None'
    CANCEL = 'Cancel'
    NEW    = 'New'

def IsCorrectionTrade(trade, tradeEventType):
    isCorrectionTrade = False
    if (trade == None):
        return isCorrectionTrade
    for businessEventTradeLink in trade.BusinessEventTradeLinks():
        if businessEventTradeLink.TradeEventType() == tradeEventType:
            if businessEventTradeLink.BusinessEvent().EventType() == BusinessEventType.CORRECT_TRADE:
                isCorrectionTrade = True
                break
    return isCorrectionTrade

def IsCorrectedTrade(trade):
    return IsCorrectionTrade(trade, TradeEventType.CANCEL)

def IsCorrectingTrade(trade):
    return IsCorrectionTrade(trade, TradeEventType.NEW)

def IsTopmostCorrectingTrade(trade):
    return (IsCorrectingTrade(trade) == True and
            IsCorrectedTrade(trade)  == False)

def GetConnectToAMBSingleton(newAMBAddress):
    global CONST_GetAMBConnection
    if CONST_GetAMBConnection != None:
        if newAMBAddress == CONST_GetAMBConnection:
            return CONST_GetAMBConnection
        else:
            # user can change FDocumentationParameters, reload it and rerun
            LogVerbose('AMB connection about to change from %s to %s' % (CONST_GetAMBConnection, newAMBAddress))

    CONST_GetAMBConnection = ConnectToAMB(newAMBAddress)
    return CONST_GetAMBConnection

def ConnectToAMB(newAMBAddress):
    try:
        amb.mb_init(newAMBAddress)
        return newAMBAddress
    except RuntimeError as runtimeError:
        ret = 'AMB connection to %s failed: %s' % (str(newAMBAddress), runtimeError)
        print(ret)
        return None


def VerifyParameterModule(templateModuleName, parameterModuleName):
    templateModule = __import__(templateModuleName)
    missingAttributesString = ""

    try:
        parameterModule = __import__(parameterModuleName)
    except Exception:
        LogAlways('Could not import %s.' % parameterModuleName)
        return

    for attribute in dir(templateModule):
        if inspect.isclass(templateModule.__dict__[attribute]) or inspect.ismodule(templateModule.__dict__[attribute]):
            continue
        if False == (attribute in parameterModule.__dict__):
            missingAttributesString += ("%s\n" % attribute)

    if len(missingAttributesString):
        LogAlways(('ERROR: %s does not contain attribute(s)\n' % parameterModuleName) + missingAttributesString)
        raise Exceptions.ParameterModuleException()
    
def GetParameterFromParameterModule(moduleName, parameterName):
    module = __import__(moduleName)
    moduleDict = module.__dict__
    return moduleDict[parameterName]

def SetProtectionAndOwnerFromTrade(record, trade):
    if trade:
        record.Protection(trade.Protection())
        record.Owner(trade.Owner())
        
def RaiseCommitException(exception, fObject = None):

    if fObject:
        msg = 'Error while committing %s %d! ' % (fObject.RecordType(), fObject.Oid())
        obj = 'Failed to commit ' + str(fObject)
    else:
        msg = 'Error while committing! '
        obj = 'Failed to commit '

    if (str(exception).find("Update collision") != -1):
        msg = msg + 'An update collision occurred.'
        LogAlways(msg)
        LogVerbose(obj)
        raise Exceptions.UpdateCollisionException(exception)
    else:
        msg = msg + 'Cause: %s.' % (exception)
        LogAlways(msg)
        LogVerbose(obj)
        raise Exceptions.CommitException(exception)        

