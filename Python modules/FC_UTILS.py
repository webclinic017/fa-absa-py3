'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_UTILS
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will contain properties for Frotn Cache Parameters, Logging and
                                Error Handling. There will be no need to import any of these underlying modules
                                in any of the Front Cache modules. All relevant information can be accessed
                                via these properties. This module also includes a couple of standard stand alone
                                helper functions.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje/Heinrich Momberg
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
import hashlib, zlib
import base64
import time, locale, _winreg
from datetime import datetime, date
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
from _winreg import *
from string import letters
import acm
'''----------------------------------------------------------------------------------------------------------
Setting Grouping format for numbers
----------------------------------------------------------------------------------------------------------'''
locale.setlocale(locale.LC_ALL, '')

'''----------------------------------------------------------------------------------------------------------
Importing all relevant custom modules.
----------------------------------------------------------------------------------------------------------'''
from FC_PARAMETERS_SINGLETON import FC_PARAMETERS_SINGLETON as PARAMETERS
from FC_FLOGGER_SINGLETON import FC_FLOGGER_SINGLETON as FLOGGER
from FC_ERROR_HANDLING import FC_ERROR_HANDLING as ERROR_HANDLER
from FC_CONSTANTS_SINGLETON import FC_CONSTANTS_SINGLETON as CONSTANTS
from FC_PARAMETERS_COMPONENT import FC_PARAMETERS_COMPONENT as COMPONENT

'''----------------------------------------------------------------------------------------------------------
FC_UTILS class containing properties for Parameters, Logger and Error Handler.
----------------------------------------------------------------------------------------------------------'''
class FC_UTILS(object):
    #move to config.....to be used as trade domain in the trade (Africa vs SAfrica)
    _frontArenaInstanceName = None
    _componentName = None
    _parameters = None
    _isInitialized = False
    _logger = None
    _constants = None
    _errorHandler = None
    _expectedMessageType = None
    _senderSubject = None
    _messageQueueDepth = 0
    _controlMeasuresResults = None
    _ats_startup_datetime = None
    _historicalDate = ''
    _Ats_service_name = ''

    class __metaclass__(type):
        @property
        def FrontArenaInstanceName(cls):
            if not cls._frontArenaInstanceName:
                cls._frontArenaInstanceName = cls._parameters.fcGenericParameters.FrontArenaInstanceName
            return cls._frontArenaInstanceName

        @FrontArenaInstanceName.setter
        def FrontArenaInstanceName(cls, value):
            cls._frontArenaInstanceName = value

        @property
        def ExpectedMessageType(cls):
            if not cls._expectedMessageType:
                cls._expectedMessageType = cls._parameters.fcComponentParameters.componentSubscriptionSubjects[0]
            return cls._expectedMessageType

        @ExpectedMessageType.setter
        def ExpectedMessageType(cls, value):
            cls._expectedMessageType = value

        @property
        def SenderSubject(cls):
            if not cls._senderSubject:
                cls._senderSubject = 'SenderSubject'
            return cls._senderSubject

        @SenderSubject.setter
        def SenderSubject(cls, value):
            cls._senderSubject = value

        @property
        def Ats_startup_datetime(cls):
            return cls._ats_startup_datetime

        @Ats_startup_datetime.setter
        def Ats_startup_datetime(cls, value):
            cls._ats_startup_datetime = value

        @property
        def HistoricalDate(cls):
            return cls._historicalDate

        @HistoricalDate.setter
        def HistoricalDate(cls, value):
            cls._historicalDate = value

        @property
        def Ats_service_name(cls):
            return cls._Ats_service_name

        @Ats_service_name.setter
        def Ats_service_name(cls, value):
            cls._Ats_service_name = value

        @property
        def ComponentName(cls):
            return cls._componentName

        @property
        def Parameters(cls):
            return cls._parameters

        @property
        def Logger(cls):
            return cls._logger

        @property
        def ErrorHandler(cls):
            return cls._errorHandler

        @property
        def Constants(cls):
            return cls._constants

        @property
        def MessageQueueDepth(cls):
            return cls._messageQueueDepth

        @MessageQueueDepth.setter
        def MessageQueueDepth(cls, value):
            cls._messageQueueDepth = value

        @property
        def ControlMeasureResults(cls):
            return cls._controlMeasuresResults

        @ControlMeasureResults.setter
        def ControlMeasureResults(cls, value):
            cls._controlMeasuresResults = value

        def __setParameters(cls):
            PARAMETERS.componentName = cls._componentName
            cls._parameters = PARAMETERS.Instance()

        def __setConstants(cls):
            cls._constants = CONSTANTS.Instance()

        def __setLogger(cls):
            cls._logger = FLOGGER.Instance()
            cls.__setLoggerProperties()
            cls.__reinitializeLogger()

        def __setLoggerProperties(cls):
            cls._logger.LogLevel = cls._parameters.fcFloggerParameters._floggerLevel
            cls._logger.Keep = cls._parameters.fcFloggerParameters._floggerKeep
            cls._logger.LogOnce = cls._parameters.fcFloggerParameters._floggerLogOnce
            cls._logger.LogToConsole = cls._parameters.fcFloggerParameters._floggerLogToConsole
            cls._logger.LogToPrime = cls._parameters.fcFloggerParameters._floggerLogToPrime
            cls._logger.LogToFileAtSpecificPath = cls._parameters.fcFloggerParameters._floggerLogToFileAtSpecificPath
            cls._logger.Filters = cls._parameters.fcFloggerParameters._floggerFilters

        def __reinitializeLogger(cls):
            cls._logger.Reinitialize()

        def __setErrorHandler(cls):
            cls._errorHandler = ERROR_HANDLER

        def Initialize(cls, value):
            if not cls._isInitialized:
                cls._componentName = value
                cls.__setParameters()
                cls.__setLogger()
                cls._isInitialized = True
                cls.__setErrorHandler()
                cls.__setConstants()

'''----------------------------------------------------------------------------------------------------------
Static Helper Methods
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Compress a string in base 64 encoding
----------------------------------------------------------------------------------------------------------'''
def deflate_and_base64_encode(input):
    zlibbed_str = zlib.compress(input)
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string)

'''----------------------------------------------------------------------------------------------------------
Gets the lapsed time between two datetime values in seconds - used for performance monitoring
---------------------------------------------------------------------------------------------------------'''
def getLapsedTimeInSeconds(startDateTime, endDateTime):
    timeDiff = endDateTime-startDateTime
    totalSeconds =timeDiff.seconds
    totalMicroSeconds = timeDiff.microseconds / 1000000.0
    totalTime = totalSeconds + totalMicroSeconds
    return totalTime

'''----------------------------------------------------------------------------------------------------------
Calculate hash total for a string using the SHA512 algorithm
----------------------------------------------------------------------------------------------------------'''
def calcSHA512(input):
    sha = hashlib.sha512()
    sha.update(input)
    return sha.hexdigest()

'''----------------------------------------------------------------------------------------------------------
Create a datetime in ISO format (xml types)
----------------------------------------------------------------------------------------------------------'''
def dateTimeFromInt(input):
    if not input:
        return ''
    return datetime.fromtimestamp(input)

'''----------------------------------------------------------------------------------------------------------
Create a date time object from a ISO date string
----------------------------------------------------------------------------------------------------------'''
def dateFromISODateTimeString(input):
    if not input:
        return ''
    try:
        return datetime.strptime(input, '%Y-%m-%dT%H:%M:%S')
    except:
        return datetime.strptime(input, '%Y-%m-%d')

'''----------------------------------------------------------------------------------------------------------
Create a date time object from a date time string
----------------------------------------------------------------------------------------------------------'''
def dateFromDateTimeString(input):
    if not input:
        return ''
    try:
        return datetime.strptime(input, '%x %X')
    except:
        return datetime.strptime(input, '%Y-%m-%d %H:%M:%S')



'''----------------------------------------------------------------------------------------------------------
Create a date time object from a date time AM PM string
----------------------------------------------------------------------------------------------------------'''
def dateFromDateTimeAMPMString(input):
    if not input:
        return ''
    try:
        return datetime.strptime(input, '%x %I:%M:%S %p')
    except:
        return datetime.strptime(input, '%Y-%m-%d %I:%M:%S %p')

'''----------------------------------------------------------------------------------------------------------
Create a date time object from a string
----------------------------------------------------------------------------------------------------------'''
def dateFromDateString(input):
    if not input:
        return ''
    return datetime.strptime(input, '%Y-%m-%d').date()

'''----------------------------------------------------------------------------------------------------------
Create a date time string from a ISO date time string
----------------------------------------------------------------------------------------------------------'''
def dateTimeStringFromISODateTimeString(input):
    if not input:
        return ''
    return dateFromISODateTimeString(input).strftime('%Y-%m-%d %H:%M:%S')

'''----------------------------------------------------------------------------------------------------------
Create a date time string from a ISO date time string
----------------------------------------------------------------------------------------------------------'''
def dateStringFromISODateTimeString(input):
    if not input:
        return ''
    return dateFromISODateTimeString(input).strftime('%Y-%m-%d')

'''----------------------------------------------------------------------------------------------------------
Create a date string from a date object
----------------------------------------------------------------------------------------------------------'''
def dateStringFromDate(input):
    if not input:
        return ''
    return input.strftime('%Y-%m-%d')

'''----------------------------------------------------------------------------------------------------------
Create a Date in String format from a Date Time in String Format
----------------------------------------------------------------------------------------------------------'''
def dateStringFromDateTimeString(input):
    if not input:
        return ''
    try:
        return datetime.strptime(input, '%x %X').date().isoformat()
    except:
        return datetime.strptime(input, '%Y-%m-%d %H:%M:%S').date().isoformat()

'''----------------------------------------------------------------------------------------------------------
Create an ISO date time from a float, int or string date time
----------------------------------------------------------------------------------------------------------'''
def formatDate(input):
    if not input or input=='':
        return input
    elif bool(type(input)==float) or bool(type(input)==int):
        return dateTimeFromInt(input).isoformat()
    elif bool(type(input)==str):
        try:
            return dateFromDateString(input).isoformat()
        except:
            try:
                return dateFromDateTimeString(input).isoformat()
            except:
                try:
                    return dateFromDateTimeAMPMString(input).isoformat()
                except:
                    return input

'''----------------------------------------------------------------------------------------------------------
Create a dateTime from a date or dateTime string
----------------------------------------------------------------------------------------------------------'''
def dateTimeFromStringDateOrStringDateTime(input):
    if not input:
        return ''
    try:
        return datetime.strptime(input, '%x %X')
    except:
        try:
            return datetime.strptime(input, '%Y-%m-%d %H:%M:%S')
        except:
            try:
                return datetime.strptime(input, '%x')
            except:
                try:
                    return datetime.strptime(input, '%Y-%m-%d')
                except:
                    return input

'''----------------------------------------------------------------------------------------------------------
Create an ISO date time from a string date or dateTime
----------------------------------------------------------------------------------------------------------'''
def ISODateTimeFromStringDateOrStringDateTime(input):
    if not input:
        return ''
    try:
        return dateTimeFromStringDateOrStringDateTime(input).isoformat()
    except:
        return input

'''----------------------------------------------------------------------------------------------------------
Format all numbers to a standard
----------------------------------------------------------------------------------------------------------'''
'''
def formatNumber(input):
    #global setting - do we want all number formatting the same?
    decimalFormat = '{0:0.08f}'
    if bool(type(input)==float):
        return decimalFormat.format(float(input))
    elif bool(type(input)==int):
        return int(input)
    else:
        return str(input)
'''
def formatNumber(input):
    #global setting - do we want all number formatting the same?
    decimalFormat = '{0:0.08f}'

    type_desc = str(type(input))
    try:
        if 'FDenominatedValue' in type_desc:
            str_i = str(input)
            curr = ''.join([c for c in str_i if c.isupper()])
            input = str(input).translate(None, curr).split('@')[0].split('[')[0].split('/')[0]
            try:
                currencyFloat = float(input)
                currencyFloat = decimalFormat.format(currencyFloat)
                #print 'Float', currencyFloat
                return currencyFloat
            except:
                #print 'Except', input
                splt = str(input).split('@')
                if len(splt) > 0:
                    input = splt[0].translate(None, letters).translate(None, '#/@(\([^)]*\)')
        return locale.atoi(input)
    except:
        try:
            return decimalFormat.format(locale.atof(input))
        except:
            try:
                return decimalFormat.format(input)
            except:
                return str(input)
 
'''----------------------------------------------------------------------------------------------------------
Format all numbers for control measures
----------------------------------------------------------------------------------------------------------'''
def formatCMNumber(input):
    decimalFormat = '{0:0.08f}'
    try:
        if locale.atof(str(input)) != 0:
            return str(input)
        else:
            return decimalFormat.format(locale.atof(str(input)))
    except:
        try:
            return decimalFormat.format(input)
        except:
            return str(input)

'''----------------------------------------------------------------------------------------------------------
Creates a root xml element plus child elements
----------------------------------------------------------------------------------------------------------'''
def createRootElementAndChildren(rootElementName, attributes):
    rootElement = Element(rootElementName)
    addAttributesToElement(rootElement, attributes)
    return rootElement

'''----------------------------------------------------------------------------------------------------------
Add text to an element
----------------------------------------------------------------------------------------------------------'''
def createRootElementWithText(rootElementName, text):
    rootElement = Element(rootElementName)
    rootElement.text = text
    return rootElement

'''----------------------------------------------------------------------------------------------------------
Create a root element plus attributes
----------------------------------------------------------------------------------------------------------'''
def createRootElementWithAttributes(rootElementName, attributes):
    rootElement = Element(rootElementName, attributes)
    return rootElement

'''----------------------------------------------------------------------------------------------------------
Adds a collection of key/value pairs as child elements to a parent xml element
----------------------------------------------------------------------------------------------------------'''
def addAttributesToElement(element, attributes):
    for attName in attributes:
        if attributes[attName]:
            AddXmlChildElement(element, str(attName), str(attributes[attName]))

'''----------------------------------------------------------------------------------------------------------
Add an xml child element to a parent
----------------------------------------------------------------------------------------------------------'''
def AddXmlChildElement(parent, elementName, elementValue):
    childTag = Element(elementName)
    childTag.text = elementValue
    parent.append(childTag)
    return childTag

'''----------------------------------------------------------------------------------------------------------
Serialize a dictionary using XML
----------------------------------------------------------------------------------------------------------'''
def GetXMLDictionary(dictionary, rootElementName):
    rootElement = Element(rootElementName)
    addAttributesToElement(rootElement, dictionary)
    return tostring(rootElement)

def CreateControlMeasuresParameter(requestid, controlMeasures, errors):
    controlMeasureList = []
    try:
        for controlMeasure in sorted(controlMeasures):
            hasError = controlMeasure in errors
            controlMeasureList.append((requestid, controlMeasure, controlMeasures[controlMeasure], hasError))
    except Exception, e:
        print str(e)

    return controlMeasureList

def GetSenderSubject(targetComponent):
    senderSubject = None
    if targetComponent:
        component = COMPONENT(targetComponent)
        senderSubject = component.componentSubscriptionSubjects[0]
        return senderSubject
    return 'None'



def getHistoricalDate(componentName):
    try:
        regKeyPath = "SOFTWARE\Front\Front Arena\ATS\%s" %componentName
        CreateKey(HKEY_LOCAL_MACHINE, regKeyPath)
        regKey = OpenKey(HKEY_LOCAL_MACHINE, regKeyPath, 0, KEY_READ)
        value = QueryValueEx(regKey, "historicaldate")
        if value:
            return value
    except Exception, e:
        print str(e)
        return ("", "")

def __setHistoricalDate(date, regKeyPath):
    try:
        CreateKey(HKEY_LOCAL_MACHINE, regKeyPath)
        regKey = OpenKey(HKEY_LOCAL_MACHINE, regKeyPath, 0, KEY_WRITE)
        SetValueEx(regKey, "historicaldate", 0, REG_SZ, date)
        CloseKey(regKey)
        return True
    except Exception, e:
        print str(e)
        return False


def __deleteHistoricalDate(regKeyPath):
    try:
        regKey = OpenKey(HKEY_LOCAL_MACHINE, regKeyPath, 0, KEY_WRITE)
        DeleteValue(regKey, "historicaldate")
        CloseKey(regKey)
        return True
    except Exception, e:
        print str(e)
        return False

def __isHistoricalDateNeeded(reportDate):
    today = str(time.strftime("%Y-%m-%d"))
    return today != reportDate

def RestartAtsForHistoricalDate(reportDate, componentName, historicalDate):
    regKeyPath = "SOFTWARE\Front\Front Arena\ATS\%s" %componentName
    restart = False
    if not __isHistoricalDateNeeded(reportDate):
        if historicalDate != "":
            restart = __deleteHistoricalDate(regKeyPath)
        historicalDate = ""
    else:
        if historicalDate != reportDate:
            historicalDate = reportDate
            return __setHistoricalDate(reportDate, regKeyPath)
    return restart
            #restart ATS

def getAtsServiceName(moduleName):
    interRegKey = "SOFTWARE\Front\Front Arena\ATS"
    CreateKey(HKEY_LOCAL_MACHINE, interRegKey)
    parentKey = OpenKey(HKEY_LOCAL_MACHINE, interRegKey, 0, KEY_READ)
    for i in range(150):
        atsName = _winreg.EnumKey(parentKey, i)
        newKeyName = interRegKey + "\\" + atsName
        CreateKey(HKEY_LOCAL_MACHINE, newKeyName)
        subKey = OpenKey(HKEY_LOCAL_MACHINE, newKeyName, 0, KEY_READ)
        subKeyValue = QueryValueEx(subKey, "module_name")
        historicalDate = ('', '')
        try:
            historicalDate = QueryValueEx(subKey, "historicaldate")
        except:
            pass
        if subKeyValue[0] == moduleName:
            return atsName, historicalDate[0]
    return ("", "")

def getCorrectReportDate(inputDate):
    if inputDate:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        date = datetime.strptime(inputDate, "%Y-%m-%d 00:00:00")
        dif = abs(today - date)
        if dif.days > 7:
            print 'From', inputDate, 'Corrected to', str(today)
            return str(today)
    return inputDate


enumDict = {}
def getEnum(enumType, enumValue):
    ''' Example usage::
        GetEnum('InsType', 'Bond')
        returns the numeric representation of the enum. '''
    enum = -1
    foundInCache = False
    enumDictKey = str(enumType) + '.' + str(enumValue)
    if (enumDict.has_key(enumDictKey)):
        foundInCache = True
        enum =enumDict[enumDictKey]    # Get it from the cache dict

    if not foundInCache:
        enums = acm.FEnumeration['enum(%s)' % enumType]
        if enums == None:
            raise LookupError('The enum type "%s" could not be found.' % enumType)
        try:
            enum = enums.Enumeration(enumValue)
            enumDict[enumDictKey] = enum    # Cache the enum value
        except RuntimeError, error:
            raise LookupError('Error when trying to get enum value "%s" in enum "%s"' % (enumValue, enumType))
    return enum
