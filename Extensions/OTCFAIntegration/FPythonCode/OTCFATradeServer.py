from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    OTCFATradeServer - Update FRONT ARENA with trades
        from Derivatech OTC, which it saves as XML
        files in a subdirectory.
    
    Requirements: 
    
        1. Fnorb all-Python CORBA ORB.
        2. IONA Orbix.
        3. Derivatech MDS and database.
        4. DOM parser.
        5. The ctypes Python extension module.
    
	Copyright (c) 2006 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This module runs as an ATS task using
    parameters setup here. The task should start first thing each morning
    (e.g. 0:01), run all day, and shut down at the end o the day.

ENDDESCRIPTION
"""
import OTCFAConfiguration
import atexit
import os
import os.path
import threading
import time
import traceback
import shutil
import signal
import SimpleXMLRPCServer
import struct
import sys
import string
import types
import xml.dom
import xmlrpclib

print ('Using Python version:  %s' % (sys.version))
print ('Python interpreter is: %s' % (sys.executable))
enablePsyco = True
if enablePsyco:
    try:
        import psyco
        psyco.full()
        print ('psyco is enabled.')
    except ImportError:
        print ('psyco is not available.')
else:
    print ('psyco is not enabled.')


global useWin32
useWin32 = False
try:
    import ctypes
    useWin32 = True
except:
    useWin32 = False
    traceback.print_exc()

# For signal handler to shut down server.
global server
server = None
global controller
controller = None
global encoding
encoding = 'utf_8'

if __name__ == '__main__':
    sys.path.append(r'C:\views\michael_gogins_view_1\base\Bin\Release\intel_nt')
    sys.path.append(r'C:\views\michael_gogins_view_1\base\extensions\common')
    sys.path.append(r'C:\views\michael_gogins_view_1\base\Bin\CommonLib\PythonLib25')

import acm

def resolveObject(reference, clazz):
    if type(reference) == type(1) or type(reference) == type('') or type(reference) == type(1.0):
        result = clazz[reference]
    else:
        result = reference
    logme('resolveObject(%s, %s) returned %s.' % (reference, clazz, result), 'DEBUG')
    return result
        
defaultParameters = OTCFAConfiguration.configuration.getParametersForModule(__name__)

# Must first be connected to ACM in order to import Front modules...
if __name__ == '__main__':
    print ('RUNNING STANDALONE...')
    try:
        for key, value in defaultParameters.items():
            print ('Default parameter: %s = %s' % (key, value))
        print ('Connecting to ACM...')
        acm.Connect(defaultParameters['ads_url'], defaultParameters['ads_username'], defaultParameters['ads_password'], defaultParameters['ads_password'])
    except:
        traceback.print_exc()

import FBDPGui
reload(FBDPGui)
import FBDPString
reload(FBDPString)

global logme
logme = FBDPString.logme

def dtDateToAelDate(dtDateString):
    parts = string.split(dtDateString, '/')
    month = int(parts[0])
    day = int(parts[1])
    year = int(parts[2])
    ## return ael.date_from_ymd(year, month, day)
    return acm.Time().DateFromYMD(year, month, day)
    
def getDate(node):
    return dtDateToAelDate(getText(node))
    
def getDateValue(element, name):
    return dtDateToAelDate(getTextValue(element, name))
        
def getFloatValue(element, name):
    textValue = getTextValue(element, name)
    try:
        return float(textValue)
    except:
        return None
    
def getIntValue(element, name):
    textValue = getTextValue(element, name)
    try:
        return int(textValue)
    except:
        return None
    
def getText(node):
    text = u''
    for child in node.childNodes:
        if child.nodeType == node.TEXT_NODE:
            text = text + child.data
    return text.encode()

def getTextValue(element, name):
    nodes = element.getElementsByTagName(name)
    if nodes:
        return getText(nodes[0])
    else:       
        return None

def parseFileNotifyInformation(fileNotifyInformation):
    changes = []
    bufferPointer = ctypes.addressof(fileNotifyInformation)
    while True:
        offset, action, filenameLength = struct.unpack('III', ctypes.string_at(bufferPointer, 12))
        filename = ctypes.wstring_at(bufferPointer + 12, filenameLength / 2)
        changes.append((action, filename.encode()))
        if offset > 0:
            bufferPointer = bufferPointer + offset
        else:
            return changes

# Assumes that there is actually only one child node.            
def putText(node, value):
    for child in node.childNodes:
        if child.nodeType == node.TEXT_NODE:
            child.data = unicode(value)
            
def putTextValue(element, tag, value):
    nodes = element.getElementsByTagName(tag)
    if nodes:
        node = nodes[0]
        if node:
            putText(node, value)
            
class OTCFATradeServer(object):
    def __init__(self, parameters):
        logme('INITIALIZING FAOTCMarketServer...', 'INFO')
        self.__dict__.update(parameters)
        self.parameters = parameters
        self.objectServer = str(acm.ObjectServer())
        logme('Object server: %s' % (self.objectServer))
        self.ACTIONS = {
          1 : "Created",
          2 : "Deleted",
          3 : "Updated",
          4 : "Renamed from something",
          5 : "Renamed to something"
        }
        self.FILE_LIST_DIRECTORY = 0x0001
        self.dom = xml.dom.getDOMImplementation()
        self.fileCache = {}
        self.keepRunning = True
        self.test_mode = int(self.test_mode)
        self.polling_interval = float(self.polling_interval)
        self.ts_controller_port = int(self.ts_controller_port)
        self.fixingSourcesForLocations = {}
        try:
            self.fixingSourcesForLocations = eval(str(parameters['markets_for_locations']))
            if type(self.fixingSourcesForLocations) != type({}):
                self.self.fixingSourcesForLocations = {}
        except:
            self.fixingSourcesForLocations = {}
        # True if acm.BeginTransaction is used to surround all commits
        # within one OTC deal.
        self.commit_mode = True
        # Deals modeled by a combination of two trades.
        self.doubleTrades = ['European Range Binary', 'European Outside Range', 'Synthetic Fwd', 'Down and Out Fwd', 'Down and In Fwd', 'Up and Out Fwd', 'Up and In Fwd']
        self.digitalMarkets = ['One Touch', 'No Touch', 'Digital European', 'Double No Touch', 'Double One Touch', 'Euro Range Binary', 'Euro Outside Range', 'Partial One Touch', 'Partial No Touch', 'Partial Double One Touch', 'Partial Double No Touch']
    def isDigitalMarket(self, element):
        marketName = self.getMarketName(element)
        if marketName in self.digitalMarkets:
            return True
        else:
            return False
    def abortTransaction(self):
        if not self.test_mode and self.commit_mode:
            acm.AbortTransaction()
    def addBarrierEvent(self, element, acmInstrument, acmExotic = None):
        startDate = getDateValue(element, 'BarrierStartDate')
        if not startDate:
            logme('No start date in addBarrierEvent', 'WARNING')
            return
        endDate = getDateValue(element, 'BarrierEndDate')
        if not endDate:
            logme('No end date in addBarrierEvent', 'WARNING')
            return
        barrierStatus = self.getBarrierStatus(element)
        # Protected: 2 events, before and after protected window.
        if   barrierStatus == 0:
            valueDate = getDateValue(element, 'ValueDate')
            exoticEvent1 = acm.FExoticEvent()
            exoticEvent1.Instrument(acmInstrument)
            exoticEvent1.ComponentInstrument(acmInstrument.Underlying())
            exoticEvent1.Date(valueDate) 
            exoticEvent1.EndDate(startDate)
            exoticEvent1.Type('Barrier date')
            self.commitEntity(exoticEvent1)
            expirationDate = getDateValue(element, 'ExpireDate')
            exoticEvent2 = acm.FExoticEvent()
            exoticEvent2.Instrument(acmInstrument)
            exoticEvent2.ComponentInstrument(acmInstrument.Underlying())
            exoticEvent2.Date(endDate) 
            exoticEvent2.EndDate(expirationDate)
            exoticEvent2.Type('Barrier date')
            self.commitEntity(exoticEvent2)
        # Monitored: 1 event, which is the monitored window.
        elif barrierStatus == 1:
            exoticEvent = acm.FExoticEvent()
            exoticEvent.Instrument(acmInstrument)
            exoticEvent.ComponentInstrument(acmInstrument.Underlying())
            exoticEvent.Date(startDate) 
            exoticEvent.EndDate(endDate)
            exoticEvent.Type('Barrier date')
            self.commitEntity(exoticEvent)
        # If FExotic for instrument does not yet exist, create it.
        exotics = acmInstrument.Exotics()
        if exotics:
            acmExotic = exotics[0]
        if not acmExotic:
            acmExotic = acmInstrument.Exotic()
        # 'Window' is used for both 'Protected' and 'Monitored'.
        self.mapExoticBarrierMonitoring('Window', acmExotic)
        self.commitEntity(acmExotic)
        logme("addBarrierEvent start: %s  end: %s." % (startDate, endDate), 'DEBUG')
    def beginTransaction(self):
        if not ((self.test_mode == True) and (self.commit_mode == True)):
            acm.BeginTransaction()
    def commitEntity(self, entity):
        if not (self.test_mode == True):
            entity.Commit()
    def commitTransaction(self):
        if not ((self.test_mode == True) and (self.commit_mode == True)):
            acm.CommitTransaction()
    def connectACM(self):
        try:
            acm.Connect(self.ads_url, self.ads_username, self.ads_password, self.ads_password)
        except:
            traceback.print_exc()
    def createRangeBinaryOtherSideElement(self, side1, isOutside=False):
        side2 = side1.cloneNode(True)
        if not isOutside:
            # Map a bought ERB as:
            # side1 - sold   Digital European put with strike at low  trigger of ERB, without premium.
            # side2 - bought Digital European put with strike at high trigger of ERB, with premium.
            # Map a sold   ERB as:
            # side1 - bought Digital European put with strike at low  trigger of ERB, without premium.
            # side2 - sold   Digital European put with strike at high trigger of ERB, with premium.
            buySell = self.getBuySell(side1)
            if buySell == 'BUY':
                putTextValue(side2, 'BuySell', 'SELL')
            else:
                putTextValue(side2, 'BuySell', 'BUY')
        else:
            # Map a bought EOR as:
            # side1 - bought Digital European put  with strike at low  trigger of the EOR, with half the premium.
            # side2 - bought Digital European call with strike at high trigger of the EOR, with half the premium.
            # Map a sold   EOR as:
            # side1 - sold   Digital European put  with strike at low  trigger of the EOR, with half the premium.
            # side2 - sold   Digital European call with strike at high trigger of the EOR, with half the premium.
            callCurrency = self.getCallCurrency(side1)
            putCurrency = self.getPutCurrency(side1)
            putTextValue(side1, 'CallCurrency', putCurrency)
            putTextValue(side1, 'PutCurrency', callCurrency)
        return side2    
    # Return a clone of the deal in the element 
    # that has swapped call and put currencies, 
    # and reversed buy/sell direction.
    def createOtherSideElement(self, element):
        otherSideElement = element.cloneNode(True)
        callCurrency = self.getCallCurrency(element)
        putCurrency = self.getPutCurrency(element)
        buySell = self.getBuySell(element)
        putTextValue(otherSideElement, 'CallCurrency', putCurrency)
        putTextValue(otherSideElement, 'PutCurrency', callCurrency)
        if buySell == 'BUY':
            putTextValue(otherSideElement, 'BuySell', 'SELL')
        else:
            putTextValue(otherSideElement, 'BuySell', 'BUY')
        return otherSideElement
    # The XML leg comes in as a BUY. We create also a SELL leg
    # in which the put/call is opposite. 
    # If the premium of the original leg is negative,
    # use it on the bought leg and set the premium on the sold leg to 0;
    # if the premium of the original leg is positive,
    # use it on the sold leg and set the premium on the bought leg to 0.
    def createOtherSyntheticForwardElement(self, element):
        buySell = self.getBuySell(element)
        otherSideElement = self.createOtherSideElement(element)
        premiumCurrency = self.getPremiumCurrency(element)
        logme('Premium currency: %s' % (premiumCurrency), 'DEBUG')
        tradedType = self.getTradedType(element)
        premium = self.getPremium(element)
        logme('Original premium: %s' % (premium), 'DEBUG')
        if premium < 0:
            if buySell == 'BUY':
                putTextValue(element, 'TotalPremium', str(premium))
                putTextValue(otherSideElement, 'TotalPremium', str(0))
            else:
                putTextValue(otherSideElement, 'TotalPremium', str(premium))
                putTextValue(element, 'TotalPremium', str(0))
        else:
            if buySell == 'SELL':
                putTextValue(element, 'TotalPremium', str(premium))
                putTextValue(otherSideElement, 'TotalPremium', str(0))
            else:
                putTextValue(otherSideElement, 'TotalPremium', str(premium))
                putTextValue(element, 'TotalPremium', str(0))
        originalBuySell = getTextValue(element, 'BuySell')
        logme('originalBuySell: %s' % (originalBuySell), 'DEBUG')
        originalPremium = getTextValue(element, 'TotalPremium')
        logme('originalPremium: %s' % (originalPremium), 'DEBUG')
        otherSideBuySell = getTextValue(otherSideElement, 'BuySell')
        logme('otherSideBuySell: %s' % (otherSideBuySell), 'DEBUG')
        otherSidePremium = getTextValue(otherSideElement, 'TotalPremium')
        logme('otherSidePremium: %s' % (otherSidePremium), 'DEBUG')
        return otherSideElement
    # For double barriers: 1st barrier is 'Down', 2nd barrier is 'Up'.
    def getBarrier(self, element, barrierDirection_):
        barrierDirection = barrierDirection_
        if barrierDirection_ == 'Double':
            barrierDirection = 'Down'
        strikeType = getTextValue(element, 'StrikeType')
        if strikeType:
            strikeCurrency = self.getStrikeCurrency(element)
        else:
            strikeCurrency = self.getDigitalStrikeCurrency(element)
        fx2Currency = self.getFX2Currency(element)
        tag = None
        if strikeCurrency == fx2Currency:
            tag = 'FX2%sBarrierFX2FX1' % (barrierDirection)
            floatValue = getFloatValue(element, tag)
            if floatValue:
                return floatValue
            else:
                return 0.0
        else:
            tag = 'FX2%sBarrierFX1FX2' % (barrierDirection)
            floatValue = getFloatValue(element, tag)
            if floatValue:
                return floatValue
            else:
                return 0.0
    def getBarrierDirection(self, element):
        downBarrier = getTextValue(element, "FX2DownBarrierFX1FX2")
        upBarrier = getTextValue(element, "FX2UpBarrierFX1FX2")
        if downBarrier and upBarrier:
            return "Double"
        elif downBarrier:
            return "Down"
        elif upBarrier:
            return "Up"
        else:
            return "None"
    # For double barriers: 1st barrier is 'Down', 2nd barrier is 'Up'.
    def getBarrierDirectionFromType(self, barrierType):
        parts = string.split(barrierType)
        direction = parts[0]
        if direction == 'Double':
            return 'Down'
        else:
            return direction
    def getBarrierStatus(self, element):
        return getIntValue(element, 'BarrierStatus')
    def getBuySell(self, element):
        return getTextValue(element, 'BuySell')
    def getCallCurrency(self, element):
        return getTextValue(element, 'CallCurrency')
    def getDigitalStrikeCurrency(self, element):
        # Digital options do not have StrikeType element, therefore we assume
        # that they are always entered on the left hand side of OTC
        # which implies that the strike or barrier currency is always FX1.
        strikeCurrency = self.getFX1Currency(element)
        return strikeCurrency
    def getDigitalUnderlyingCurrency(self, element):
        # Digital options do not have a StrikeType element, therefore we assume
        # that they are always entered on the left hand side of OTC,
        # which implies that the underlying currency is always FX2.
        underlyingCurrency = self.getFX2Currency(element)
        return underlyingCurrency
    def getDocumentTag(self, xml):
        ownerDocument = xml.ownerDocument
        if not ownerDocument:
            ownerDocument = xml
        documentTag = ownerDocument.childNodes[0].nodeName
        return documentTag
    def getFX1Currency(self, element):
        return getTextValue(element, 'FX1Currency')
    def getFX2Currency(self, element):
        return getTextValue(element, 'FX2Currency')
    def getInstrumentCurrency(self, element):
        return self.getPremiumCurrency(element)
    def getMarketName(self, element):
        return getTextValue(element, 'MarketName')
    def getNewFiles(self, directory):
        newFiles = []
        fileList = os.listdir(directory)
        for filename in fileList:
            pathname = os.path.join(directory, filename)
            if pathname not in self.fileCache:
                newFiles.append(pathname)
                self.fileCache[pathname] = os.stat(pathname)
        return newFiles
    def getPayoff(self, element):
        payoff = getFloatValue(element, 'PayOffHigh')
        if not payoff:
            payoff = getFloatValue(element, 'PayOffLow')
        buySell = self.getBuySell(element)
        if buySell == 'SELL':
            tradeQuantity = payoff * -1.0
        return payoff
    def getPayoffCurrency(self, element):
        return getTextValue(element, 'PayCurrency')
    def getPayTime(self, element):
        return getTextValue(element, 'PayTime')
    def getPremium(self, element):
        floatValue = getFloatValue(element, 'TotalPremium')
        if floatValue:
            return floatValue
        else:
            return 0.0
    def getPremiumCurrency(self, element):
        return getTextValue(element, 'PremiumCurrency')
    def getPutCurrency(self, element):
        return getTextValue(element, 'PutCurrency')        
    def getRebateRate(self, element):
        return getFloatValue(element, 'RebateRate') / 100.0
    def getStrategy(self, element):
        return getTextValue(element, 'Strategy')
    def getStrategyType(self, element):
        return getTextValue(element, 'StrategyType')
    # In DT, StrikeType is CC1/CC2 - CC1 per CC2.
    # Therefore, CC2, i.e. strike currency,
    # is what I pay or receive when buying or selling 
    # an option on CC1, i.e. underlying currency.
    # In an FX option, the option is in the underlying currency,
    # which forms a currency pair with the strike currency.
    # In FA, the instrument, premium, and trade could all
    # theoretically have yet different currencies,
    # but in DT, they are all equal to the premium currency.
    def getUnderlyingCurrency(self, element):
        ##strikeType = self.getStrikeType(element)
        ##if strikeType == None:
        ##    return ''
        ##return strikeType[4:7]
        #tradedType = self.getTradedType(element)
        #underlyingCurrency = None
        #if tradedType[0] == '%':
        #    underlyingCurrency = tradedType[1:4]
        #else:
        #    underlyingCurrency = tradedType[4:7]
        #return underlyingCurrency
        if self.isDigitalMarket(element):
            underlyingCurrency = self.getFX2Currency(element)
            return underlyingCurrency
        else:
            strikeType = self.getStrikeType(element)
            if len(strikeType) == 0:
                return ''
            return strikeType[4:7]
    def getStrikeCurrency(self, element):
        if self.isDigitalMarket(element):
            strikeCurrency = self.getFX1Currency(element)
            return strikeCurrency
        else:
            strikeType = self.getStrikeType(element)
            if len(strikeType) == 0:
                return ''
            return strikeType[0:3]
    def getStrikePrice(self, element):
        strikeCurrency = self.getStrikeCurrency(element)
        fx2Currency = self.getFX2Currency(element)
        if strikeCurrency == fx2Currency:
            strikePrice = getFloatValue(element, 'StrikeFX2FX1')
        else:
            strikePrice = getFloatValue(element, 'StrikeFX1FX2')
        if strikePrice:
            return strikePrice
        else:
            return 0.0
    def getStrikeType(self, element):
        strikeType = getTextValue(element, 'StrikeType')
        if strikeType:
            return strikeType
        else:
            return ''
    def getTradeCurrency(self, element):
        return self.getPremiumCurrency(element)
    def getTradedType(self, element):
        return getTextValue(element, 'TradedType')
    def getTradeQuantity(self, element):
        strikeCurrency = self.getStrikeCurrency(element)
        fx2Currency = self.getFX2Currency(element)
        amount = None
        if strikeCurrency == fx2Currency:
            amount = getFloatValue(element, 'TradeAmountFX1')
        else:
            amount = getFloatValue(element, 'TradeAmountFX2')
        if amount == None:
            try:
                amount = getFloatValue(element, 'PayOffHigh')
            except:
                pass
        if amount == None:
            try:
                amount = getFloatValue(element, 'PayOffLow')
            except:
                pass
        buySell = self.getBuySell(element)
        if amount == None:
            amount = 0.0
        if buySell == 'SELL':
            amount = amount * -1.0
        return amount
    def IdleCallback(self, **args):
        try:
            #logme('Idle callback: %s' % (args), 'DEBUG')
            pass
        except KeyboardInterrupt:
            shutdown()
        except:
            traceback.print_exc()
    def listEntities(self, acmInstruments, label=''):
        logme(label, 'INFO')
        for acmInstrument in acmInstruments:
            logme(acmInstrument, 'INFO')
            logme(acmInstrument.AdditionalInfo(), 'INFO')
            for acmTrade in acmInstrument.Trades():
                logme(acmTrade, 'INFO')
                logme(acmTrade.AdditionalInfo(), 'INFO')
            for acmExotic in acmInstrument.Exotics():
                logme(acmExotic, 'INFO')
            for acmExoticEvent in acmInstrument.ExoticEvents():
                logme(acmExoticEvent, 'INFO')
    def mapAverageRate(self, element, xmlFilename, legNumber, averageStrikeType):
        acmInstrument = self.mapVanillaOption(element, xmlFilename, legNumber)
        self.mapInstrumentExoticType('Other', acmInstrument)
        self.commitEntity(acmInstrument)
        acmExotic = acm.FExotic()
        acmExotic.Instrument(acmInstrument)
        self.mapExoticAverageMethodType('Arithmetic', acmExotic)
        self.mapExoticAverageStrikeType(averageStrikeType, acmExotic)
        # TODO: This is a hack that must be fixed!
        self.commitTransaction()
        self.beginTransaction()
        fixingSchedule = FixingSchedule(self, element)
        for fixingPeriod in fixingSchedule.fixingPeriods:
            fixingPeriod.addEvent(acmInstrument)
            fixingPeriod.addTimeSeries(acmInstrument)
        self.commitEntity(acmExotic)
        self.commitEntity(acmInstrument)
        return acmInstrument, acmExotic
    def mapBarrier(self, element, xmlFilename, legNumber, barrierType):
        barrierDirection = self.getBarrierDirectionFromType(barrierType)
        acmInstrument = self.mapVanillaOption(element, xmlFilename, legNumber)
        self.mapInstrumentExoticType('Other', acmInstrument)
        self.mapInstrumentBarrier(element, barrierDirection, acmInstrument)
        self.mapInstrumentBarrierRebate(element, acmInstrument)
        self.commitEntity(acmInstrument)
        acmExotic = acm.FExotic()
        acmExotic.Instrument(acmInstrument)
        self.mapExoticBarrierOptionType(barrierType, acmExotic)
        self.mapExoticBarrierMonitoring('Continuous', acmExotic)
        self.mapExoticRebateCurrency(element, acmExotic)
        self.mapExoticPayTime(element, acmExotic)
        self.commitEntity(acmExotic)
        self.commitEntity(acmInstrument)
        return acmInstrument, acmExotic
    def mapDigital(self, element, xmlFilename, legNumber, exerciseOverride = None):
        barrierDirection = self.getBarrierDirection(element)
        if barrierDirection == 'Double':
            barrierDirection = 'Down'
        acmInstrument = self.mapVanillaOption(element, xmlFilename, legNumber, exerciseOverride)
        self.mapInstrumentDigital(True, acmInstrument)
        self.mapInstrumentExoticType('Other', acmInstrument)
        self.mapInstrumentBarrier(element, barrierDirection, acmInstrument)
        marketName = self.getMarketName(element)
        if marketName == 'Digital European':
            self.mapInstrumentRebate(element, acmInstrument)
        else:
            acmInstrument.Rebate(1.0)
        self.mapInstrumentDigitalStrikeCurrency(element, acmInstrument)
        self.mapInstrumentDigitalUnderlyingCurrency(element, acmInstrument)
        self.mapInstrumentDigitalIsCall(element, acmInstrument)
        self.commitEntity(acmInstrument)
        acmExotic = acm.FExotic()
        acmExotic.Instrument(acmInstrument)
        self.mapExoticDigitalBarrierType('Barrier', acmExotic)
        if barrierDirection == 'Double':
            self.mapExoticBarrierOptionType('Double In', acmExotic)
        else:
            self.mapExoticBarrierOptionType(barrierDirection + ' & In', acmExotic)
        self.mapExoticRebateCurrency(element, acmExotic)
        self.mapExoticBarrierMonitoring('Continuous', acmExotic)
        self.mapExoticPayTime(element, acmExotic)
        self.commitEntity(acmExotic)
        self.commitEntity(acmInstrument)
        return acmInstrument, acmExotic
    def mapDigitalBarrier(self, element, xmlFilename, legNumber, barrierDirection):
        acmInstrument, acmExotic = self.mapDigital(element, xmlFilename, legNumber)
        self.mapExoticDigitalBarrierType('Barrier & Strike', acmExotic)
        self.commitEntity(acmExotic)
        return acmInstrument, acmExotic
    def mapDigitalDoubleNoTouch(self, element, xmlFilename, legNumber):
        acmInstrument, acmExotic = self.mapDigital(element, xmlFilename, legNumber)
        self.mapInstrumentBarrier(element, 'Down', acmInstrument)
        self.commitEntity(acmInstrument)
        self.mapExoticBarrierOptionType('Double Out', acmExotic)
        self.mapExoticDoubleBarrier(element, 'Up', acmExotic)
        self.commitEntity(acmExotic)
        return acmInstrument, acmExotic
    def mapDigitalDoubleOneTouch(self, element, xmlFilename, legNumber):
        acmInstrument, acmExotic = self.mapDigital(element, xmlFilename, legNumber, 'European')
        self.mapExoticBarrierOptionType('Double In', acmExotic)
        self.mapInstrumentBarrier(element, 'Down', acmInstrument)
        self.mapExoticDoubleBarrier(element, 'Up', acmExotic)
        self.commitEntity(acmExotic)
        return acmInstrument, acmExotic
#static const ClassifyingInfo s_DigitalEuropeanInfo[] = {
#    { "Instrument.Digital",     TRUE,   FALSE,  INTEGER_VALUE(1),   INTEGER_VALUE(1)}, 
#    { "Instrument.ExoticType",  TRUE,   FALSE,  NONE_VALUE,         NONE_VALUE},
#    { "BarrierOptionType",      TRUE,   FALSE,  NONE_VALUE,         NONE_VALUE},
#    { "DigitalBarrierType",     TRUE,   FALSE,  NONE_VALUE,         NONE_VALUE},
    def mapDigitalEuropean(self, element, xmlFilename, legNumber):
        acmInstrument, acmExotic = self.mapDigital(element, xmlFilename, legNumber)
        self.mapInstrumentExoticType('None', acmInstrument)
        self.mapExoticDigitalBarrierType('None', acmExotic)
        self.mapExoticBarrierOptionType('None', acmExotic)
        self.commitEntity(acmInstrument)
        self.commitEntity(acmExotic)
        return acmInstrument, acmExotic
    def mapDigitalNoTouch(self, element, xmlFilename, legNumber):
        acmInstrument, acmExotic = self.mapDigital(element, xmlFilename, legNumber)
        barrierDirection = self.getBarrierDirection(element)
        self.mapExoticBarrierOptionType(barrierDirection + ' & Out', acmExotic)
        self.commitEntity(acmExotic)
        return acmInstrument, acmExotic
#static const ClassifyingInfo s_OneTouchInfo[] = {
#    { "Instrument.Digital",     TRUE,   FALSE,  INTEGER_VALUE(1),                                               INTEGER_VALUE(1)},
#    { "Instrument.ExerciseType",TRUE,   FALSE,  EUROPEAN_VALUE,                                                 EUROPEAN_VALUE},
#    { "Instrument.ExoticType",  TRUE,   FALSE,  OTHER_VALUE,                                                    OTHER_VALUE},
#    { "BarrierOptionType",      TRUE,   FALSE,  FIRST_OR_SECOND_VALUE( DOWN_AND_IN_VALUE, UP_AND_IN_VALUE ),    DOWN_AND_IN_VALUE},
#    { "DigitalBarrierType",     TRUE,   FALSE,  BARRIER_VALUE,                                                  BARRIER_VALUE},
    def mapDigitalOneTouch(self, element, xmlFilename, legNumber):
        acmInstrument, acmExotic = self.mapDigital(element, xmlFilename, legNumber, 'European')
        barrierDirection = self.getBarrierDirection(element)        
        self.mapInstrumentExoticType('Other', acmInstrument)
        self.mapExoticBarrierOptionType(barrierDirection + ' & In', acmExotic)
        return acmInstrument, acmExotic
    def mapDoubleBarrier(self, element, xmlFilename, legNumber, barrierType):
        barrierDirection = self.getBarrierDirectionFromType(barrierType)
        acmInstrument, acmExotic = self.mapBarrier(element, xmlFilename, legNumber, barrierType)
        if barrierDirection == 'Down':
            doubleDirection = 'Up'
        else:
            doubleDirection = 'Down'
        self.mapExoticDoubleBarrier(element, doubleDirection, acmExotic)
        self.mapExoticBarrierOptionType(barrierType, acmExotic)
        self.commitEntity(acmExotic)
        return acmInstrument, acmExotic
    def mapExoticAverageMethodType(self, averageMethodType, acmExotic):
        acmExotic.AverageMethodType(averageMethodType)
        logme('mapExoticAverageMethodType: %s' % (averageMethodType), 'DEBUG')
    def mapExoticAverageStrikeType(self, averageStrikeType, acmExotic):
        acmExotic.AverageStrikeType(averageStrikeType)
        logme('mapExoticAverageStrikeType: %s' % (averageStrikeType), 'DEBUG')
    def mapExoticBarrierOptionType(self, barrierType, acmExotic):
        acmExotic.BarrierOptionType(barrierType)
        logme('mapExoticBarrierOptionType: %s' % (barrierType), 'DEBUG')
    def mapExoticBarrierMonitoring(self, monitoring, acmExotic):
        acmExotic.BarrierMonitoring(monitoring)
        logme('mapExoticBarrierMonitoring: %s' % (monitoring), 'DEBUG')
    def mapExoticDigitalBarrierType(self, barrierType, acmExotic):
        acmExotic.DigitalBarrierType(barrierType)
        logme('mapExoticDigitalBarrierType: %s' % (barrierType), 'DEBUG')
    def mapExoticDoubleBarrier(self, element, barrierDirection, acmExotic):
        barrier = self.getBarrier(element, barrierDirection)
        acmExotic.DoubleBarrier(barrier)
        logme('mapExoticDoubleBarrier (%s): %s' % (barrierDirection, barrier), 'DEBUG')
    def mapExoticPayTime(self, element, acmExotic):
        payTime = self.getPayTime(element)
        if payTime == 'Expire':
            acmExotic.BarrierRebateOnExpiry(True)
        else:
            acmExotic.BarrierRebateOnExpiry(False)    
        logme('mapExoticPayTime: %s' % (payTime), 'DEBUG')
    def mapExoticRebateCurrency(self, element, acmExotic):
        rebateCurrency = self.getPayoffCurrency(element)
        if len(rebateCurrency) == 7:
            rebateCurrency = rebateCurrency[4:]
        currency = acm.FCurrency[rebateCurrency]
        acmExotic.RebateCurrency(currency)
        logme('mapExoticRebateCurrency: %s' % (currency.Name()), 'DEBUG')
#static const ClassifyingInfo s_NoTouchInfo[] = {
#    { "Instrument.Digital",     TRUE,   FALSE,  INTEGER_VALUE(1),                                               INTEGER_VALUE(1)}, 
#    { "Instrument.ExoticType",  TRUE,   FALSE,  OTHER_VALUE,                                                    OTHER_VALUE},
#    { "BarrierOptionType",      TRUE,   FALSE,  FIRST_OR_SECOND_VALUE( DOWN_AND_OUT_VALUE, UP_AND_OUT_VALUE ),  DOWN_AND_OUT_VALUE},
#    { "DigitalBarrierType",     TRUE,   FALSE,  BARRIER_VALUE,                                                  BARRIER_VALUE},
#static const ClassifyingInfo s_OneTouchInfo[] = {
#    { "Instrument.Digital",     TRUE,   FALSE,  INTEGER_VALUE(1),                                               INTEGER_VALUE(1)}, 
#    { "Instrument.ExoticType",  TRUE,   FALSE,  OTHER_VALUE,                                                    OTHER_VALUE},
#    { "BarrierOptionType",      TRUE,   FALSE,  FIRST_OR_SECOND_VALUE( DOWN_AND_IN_VALUE, UP_AND_IN_VALUE ),    DOWN_AND_IN_VALUE},
#    { "DigitalBarrierType",     TRUE,   FALSE,  BARRIER_VALUE,                                                  BARRIER_VALUE},
#static const ClassifyingInfo s_DoubleNoTouchInfo[] = {
#    { "Instrument.Digital",     TRUE,   FALSE,  INTEGER_VALUE(1),                               INTEGER_VALUE(1)}, 
#    { "Instrument.ExoticType",  TRUE,   FALSE,  OTHER_VALUE,                                    OTHER_VALUE},
#    { "BarrierOptionType",      TRUE,   FALSE,  DOUBLE_OUT_VALUE,                               DOUBLE_OUT_VALUE},
#    { "DigitalBarrierType",     TRUE,   FALSE,  BARRIER_VALUE,                                  BARRIER_VALUE},
#static const ClassifyingInfo s_DoubleOneTouchInfo[] = {
#    { "Instrument.Digital",     TRUE,   FALSE,  INTEGER_VALUE(1),                               INTEGER_VALUE(1)}, 
#    { "Instrument.ExoticType",  TRUE,   FALSE,  OTHER_VALUE,                                    OTHER_VALUE},
#    { "BarrierOptionType",      TRUE,   FALSE,  DOUBLE_IN_VALUE,                                DOUBLE_IN_VALUE},
#    { "DigitalBarrierType",     TRUE,   FALSE,  BARRIER_VALUE,                                  BARRIER_VALUE},
    def mapInstrumentBarrier(self, element, barrierDirection, acmInstrument):
        barrier = self.getBarrier(element, barrierDirection)        
        # For digital Europeans, strike is used, not barrier.
        if self.getMarketName(element) == 'Digital European':
            acmInstrument.StrikePrice(barrier)
        else:
            acmInstrument.Barrier(barrier)
        logme('mapInstrumentBarrier (%s): %s' % (barrierDirection, barrier), 'DEBUG')
    def mapInstrumentBarrierRebate(self, element, acmInstrument):
        rebate = self.getRebateRate(element) * self.getStrikePrice(element)
        acmInstrument.Rebate(rebate)
        if self.getPayoffCurrency(element) != self.getFX1Currency(element) and not (rebate == 0.0 or rebate == None):
            raise Exception("Cannot map non-zero barrier rebate except from '% of FX1' terms.")
        logme('mapInstrumentBarrierRebate: %s' % (rebate), 'DEBUG')
    def mapInstrumentContractSize(self, element, acmInstrument):
        contractSize = 1.0
        logme('mapInstrumentContractSize: %f' % (contractSize), 'DEBUG')
        acmInstrument.ContractSize(contractSize)
    def mapInstrumentCurrency(self, element, acmInstrument):
        instrumentCurrency = self.getInstrumentCurrency(element)
        logme('mapInstrumentCurrency: %s' % (instrumentCurrency), 'DEBUG')
        acmInstrument.Currency(acm.FCurrency[instrumentCurrency])
    def mapInstrumentDigital(self, digital, acmInstrument):
        acmInstrument.Digital(digital)
        logme('mapInstrumentDigital: %s' % (digital), 'DEBUG')
    def mapInstrumentDigitalIsCall(self, element, acmInstrument):
        underlyingCurrency = self.getDigitalUnderlyingCurrency(element)
        callCurrency = getTextValue(element, 'CallCurrency')
        isCall = False
        if underlyingCurrency == callCurrency:
            isCall = True
        else:
            isCall = False
        logme('mapInstrumentDigitalIsCall: %s' % (isCall), 'DEBUG')
        acmInstrument.SuggestOptionType(isCall)
    def mapInstrumentDigitalStrikeCurrency(self, element, acmInstrument):
        strikeCurrency = self.getDigitalStrikeCurrency(element)
        logme('mapInstrumentDigitalStrikeCurrency: %s' % (strikeCurrency), 'DEBUG')
        acmInstrument.StrikeCurrency(acm.FCurrency[strikeCurrency])
    def mapInstrumentDigitalUnderlyingCurrency(self, element, acmInstrument):
        underlyingCurrency = self.getDigitalUnderlyingCurrency(element)
        logme('mapInstrumentDigitalUnderlyingCurrency: %s' % (underlyingCurrency), 'DEBUG')
        acmInstrument.Underlying(acm.FCurrency[underlyingCurrency])
    def mapInstrumentExerciseType(self, element, acmInstrument, overrideType = None):
        if overrideType == None:
            exerciseType = getTextValue(element, 'Style')
        else:
            exerciseType = overrideType
        logme('mapInstrumentExerciseType: %s' % (exerciseType), 'DEBUG')
        acmInstrument.ExerciseType(exerciseType)
    def mapInstrumentExerciseStyle(self, exerciseStyle, acmInstrument):
        logme('mapInstrumentExerciseStyle: %s' % (exerciseStyle), 'DEBUG')
        acmInstrument.ExerciseType(exerciseStyle)
    def mapInstrumentExoticType(self, exoticType, acmInstrument):
        acmInstrument.ExoticType(exoticType)
        logme('mapInstrumentExoticType: %s' % (exoticType), 'DEBUG')    
    def mapInstrumentExpiryDate(self, element, acmInstrument):
        expiryDate = getDateValue(element, 'ExpireDate')
        logme('mapInstrumentExpiryDate: %s' % (expiryDate), 'DEBUG')
        acmInstrument.ExpiryDate(expiryDate)
    def mapInstrumentFixingSource(self, element, acmInstrument):
        location = getTextValue(element, 'Location')
        fixingSource = self.fixingSourcesForLocations[location][0]
        logme('  Fixing source: %s' % fixingSource, 'DEBUG')
        fixingSourceParty = acm.FParty[fixingSource]
        ##additionalInfo = acmInstrument.AdditionalInfo()
        logme('  Fixing source party: %s' % fixingSourceParty.Name(), 'DEBUG')
        acmInstrument.FixingSource(fixingSourceParty)
        logme('mapInstrumentFixingSource: %s' % acmInstrument.FixingSource(), 'DEBUG')
    def mapInstrumentIsCall(self, element, acmInstrument):
        underlyingCurrency = self.getUnderlyingCurrency(element)
        callCurrency = getTextValue(element, 'CallCurrency')
        isCall = False
        if underlyingCurrency == callCurrency:
            isCall = True
        else:
            isCall = False
        logme('mapInstrumentIsCall: %s' % (isCall), 'DEBUG')
        acmInstrument.SuggestOptionType(isCall)
    def mapInstrumentName(self, element, acmInstrument, xmlFilename, legNumber):
        path, file = os.path.split(xmlFilename)
        file, ext = os.path.splitext(file)
        instrumentName = 'DT_' + file.encode() + 'L' + str(legNumber + 1)
        logme('mapInstrumentName: %s' % (instrumentName), 'DEBUG')
        acmInstrument.Name(instrumentName) 
    def mapInstrumentPayDayOffset(self, element_, acmInstrument):
        element = element_.getElementsByTagName('DeliveryDate')[0]
        deliveryDate = getDate(element)
        element = element_.getElementsByTagName('ExpireDate')[0]
        expireDate = getDate(element)
        fx1 = self.getFX1Currency(element_)
        fx2 = self.getFX2Currency(element_)
        currencyPair = acm.FCurrency[fx1].CurrencyPair(acm.FCurrency[fx2])        
        payDayOffset = currencyPair.BusinessDaysBetween(expireDate, deliveryDate)
        logme('mapInstrumentPayDayOffset: %s' % (payDayOffset), 'DEBUG')
        acmInstrument.PayDayOffset(payDayOffset)
    def mapInstrumentPayOffsetMethod(self, element, acmInstrument):
        payOffsetMethod = "Business Days"
        logme('mapInstrumentPayOffsetMethod: %s' % (payOffsetMethod), 'DEBUG')
        acmInstrument.PayOffsetMethod(payOffsetMethod)
    def mapInstrumentQuoteType(self, element, acmInstrument):
        tradeCurrency = self.getTradeCurrency(element)
        fx2Currency = self.getFX2Currency(element)
        tradedType = self.getTradedType(element)
        if tradedType[0] == '%':
            quotation = 'Pct of Nominal'
        else:
            if self.getStrikeCurrency(element) == self.getPremiumCurrency(element):
                quotation = 'Points of UndCurr'
            else:
                quotation = 'Points of BaseCurr'
        logme('mapInstrumentQuoteType: %s' % (quotation), 'DEBUG')
        acmInstrument.Quotation(acm.FQuotation[quotation])
    def mapInstrumentRebate(self, element, acmInstrument):
        rebate = self.getRebateRate(element) * self.getPayoff(element)
        acmInstrument.Rebate(rebate)
        logme('mapInstrumentRebate: %s' % (rebate), 'DEBUG')
    # There is potentially a whole set of defaults for different markets.
    def mapInstrumentSettlementType(self, element, acmInstrument):
        # Main default value (required).
        settlementType = self.settlement_type
        # The main category is instrument type.
        instrumentType = self.getDocumentTag(element)
        # Settlement type may also be qualified in some cases by market.
        marketName = self.getMarketName(element)
        # Vanilla...
        if instrumentType.startswith('DTVanillaOptionOutright'):
            if self.settlement_type_vanilla in ('Cash', 'Physical Delivery'):
                settlementType = self.settlement_type_vanilla
            # Asian...
            if marketName.startswith('Average'):
                if self.settlement_type_asian in ('Cash', 'Physical Delivery'):
                    settlementType = self.settlement_type_asian
            # Lookback...
            if marketName.startswith('Lookback'):
                if self.settlement_type_lookback in ('Cash', 'Physical Delivery'):
                    settlementType = self.settlement_type_lookback
        # Barrier...
        elif instrumentType.startswith('DTBarrierOption'):
            # Barrier forward... note the order of cases!
            if marketName in ('Down and In Fwd', 'Down and Out Fwd', 'Up and In Fwd', 'Up and Out Fwd'):
                if self.settlement_type_barrier_forward in ('Cash', 'Physical Delivery'):
                    settlementType = self.settlement_type_barrier_forward
            elif self.settlement_type_barrier in ('Cash', 'Physical Delivery'):
                settlementType = self.settlement_type_barrier
        # Digital...
        elif self.isDigitalMarket(element):
            strikeCurrency = self.getStrikeCurrency(element)
            payoffCurrency = self.getPayoffCurrency(element)
            if payoffCurrency == strikeCurrency:
                if self.settlement_type_digital_strike in ('Cash', 'Physical Delivery'):
                    settlementType = self.settlement_type_digital_strike                
            else:
                if self.settlement_type_digital_underlying in ('Cash', 'Physical Delivery'):
                    settlementType = self.settlement_type_digital_underlying                
        settlementTypeEnum = acm.EnumFromString('SettlementType', settlementType)
        acmInstrument.SettlementType(settlementTypeEnum)
        logme('mapInstrumentSettlementType: %s: %s: %s' % (instrumentType, marketName, settlementType), 'DEBUG')
    def mapInstrumentStrikeCurrency(self, element, acmInstrument):
        strikeCurrency = self.getStrikeCurrency(element)
        logme('mapInstrumentStrikeCurrency: %s' % (strikeCurrency), 'DEBUG')
        acmInstrument.StrikeCurrency(acm.FCurrency[strikeCurrency])
    def mapInstrumentStrikePrice(self, element, acmInstrument):
        strikePrice = self.getStrikePrice(element)
        logme('mapInstrumentStrikePrice: %f' % (strikePrice), 'DEBUG')
        acmInstrument.StrikePrice(strikePrice)
    def mapInstrumentStrikeType(self, element, acmInstrument):
        strikeType = 'Absolute'
        logme('mapInstrumentStrikeType: %s' % (strikeType), 'DEBUG')        
        acmInstrument.StrikeType(strikeType)
    def mapInstrumentStrikeQuotationType(self, element, acmInstrument):
        quotation = 'Per Unit'
        if False:
            quotation = 'Per Unit Inverse'
        logme('mapInstrumentStrikeType: %s' % (quotation), 'DEBUG')        
        acmInstrument.StrikeQuotation(acm.FQuotation[quotation])
    def mapInstrumentUnderlyingCurrency(self, element, acmInstrument):
        underlyingCurrency = self.getUnderlyingCurrency(element)
        logme('mapInstrumentUnderlyingCurrency: %s' % (underlyingCurrency), 'DEBUG')
        acmInstrument.Underlying(acm.FCurrency[underlyingCurrency])
    def mapInstrumentValuationGrpChlItem(self, element, acmInstrument):
        name = self.parameters['instrument_val_group']
        valuationGroup = acm.FChoiceList.Select('list="ValGroup" and name="%s"' % name)[0]
        logme('mapInstrumentValuationGrpChlItem: %s' % (valuationGroup.display_id()), 'DEBUG')
        acmInstrument.ValuationGrpChlItem(valuationGroup)
    def logLeg(self, marketName, legElement, otcLegNumber, faLegNumber):
        logme('', 'INFO')
        logme('MAPPING %s (OTC leg %d / Front Arena leg %d)...' % (marketName, otcLegNumber, faLegNumber), 'INFO')
        logme(legElement.toprettyxml(), 'INFO')
        logme('', 'INFO')
    def mapLegs(self, document, fullFilename):
        instrumentType = self.getDocumentTag(document)
        strategyType = self.getStrategyType(document)
        strategy = self.getStrategy(document)
        otcLegNumber = 0
        faLegNumber = 0
        instruments = []
        while True:
            instrument = None
            otcLegName = 'Leg%d' % (otcLegNumber)
            elements = document.getElementsByTagName(otcLegName)
            if not elements:
                break
            legElement = elements[0]
            marketName = self.getMarketName(legElement)
            if   marketName == 'OTC European':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapVanillaOption(legElement, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
            elif marketName == 'OTC American':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapVanillaOption(legElement, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
            elif marketName == 'Down and Out':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapBarrier(legElement, fullFilename, faLegNumber, 'Down & Out')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Down and In':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapBarrier(legElement, fullFilename, faLegNumber, 'Down & In')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Up and Out':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapBarrier(legElement, fullFilename, faLegNumber, 'Up & Out')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Up and In':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapBarrier(legElement, fullFilename, faLegNumber, 'Up & In')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Double Knock In':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapDoubleBarrier(legElement, fullFilename, faLegNumber, 'Double In')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Double Knock Out':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapDoubleBarrier(legElement, fullFilename, faLegNumber, 'Double Out')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Partial Down and Out':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapPartialBarrier(legElement, fullFilename, faLegNumber, 'Down & Out')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Partial Down and In':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapPartialBarrier(legElement, fullFilename, faLegNumber, 'Down & In')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Partial Up and Out':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapPartialBarrier(legElement, fullFilename, faLegNumber, 'Up & Out')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Partial Up and In':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapPartialBarrier(legElement, fullFilename, faLegNumber, 'Up & In')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Partial Double Knock In':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapPartialDoubleBarrier(legElement, fullFilename, faLegNumber, 'Double In')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Partial Double Knock Out':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapPartialDoubleBarrier(legElement, fullFilename, faLegNumber, 'Double Out')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Average Rate':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapAverageRate(legElement, fullFilename, faLegNumber, 'Fix')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Average Strike':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapAverageRate(legElement, fullFilename, faLegNumber, 'Average')
                faLegNumber = faLegNumber + 1
            # Can't find this market in OTC.
            elif marketName == 'Double Average Rate':
                # instrument = self.mapAverageRate(legElement, fullFilename, faLegNumber, 'Average')
                logme('Market "%s" not implemented.' % (marketName), 'WARNING')    
            elif marketName == 'One Touch':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapDigitalOneTouch(legElement, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
            elif marketName == 'No Touch':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapDigitalNoTouch(legElement, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
            elif marketName == 'Digital European':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapDigitalEuropean(legElement, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
            elif marketName == 'Double One Touch':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapDigitalDoubleOneTouch(legElement, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
            elif marketName == 'Double No Touch':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapDigitalDoubleNoTouch(legElement, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
            # Map a bought ERB as:
            # side1 - sold   Digital European put with strike at low  trigger of ERB, without premium.
            # side2 - bought Digital European put with strike at high trigger of ERB, with premium.
            # Map a sold   ERB as:
            # side1 - bought Digital European put with strike at low  trigger of ERB, without premium.
            # side2 - sold   Digital European put with strike at high trigger of ERB, with premium.
            elif marketName == 'European Range Binary':
                side1element = self.createRangeBinaryOtherSideElement(legElement, False)
                self.logLeg(marketName, side1element, otcLegNumber, faLegNumber);
                side1, exotic1 = self.mapDigitalEuropean(side1element, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
                side1Barrier   = getFloatValue(legElement, "FX2DownBarrierFX1FX2")
                side1.StrikeType('Absolute')
                side1.StrikePrice(side1Barrier)
                self.commitEntity(side1)
                barrierType = 'None'
                self.mapExoticBarrierOptionType(barrierType, exotic1)
                self.commitEntity(exotic1)
                self.commitEntity(side1)
                #side1.Barrier(side1Barrier)
                self.commitEntity(side1)
                side1Trade = side1.Trades()[0]
                side1Trade.Premium(0.0)
                self.commitEntity(side1Trade)
                logme('Remapped side1 barrier for ERB: %s %s' % (barrierType, side1Barrier), 'DEBUG')
                side2element = legElement
                self.logLeg(marketName, side2element, otcLegNumber, faLegNumber);
                logme(side2element.toprettyxml(), 'INFO')
                side2, exotic2 = self.mapDigitalEuropean(side2element, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
                side2Barrier = getFloatValue(legElement, "FX2UpBarrierFX1FX2")
                side2.StrikePrice(side2Barrier)
                side2.StrikeType('Absolute')
                #side2.Barrier(side2Barrier)
                self.commitEntity(side2)
                barrierType   = 'None'
                self.mapExoticBarrierOptionType(barrierType, exotic2)
                self.commitEntity(exotic2)
                logme('Remapped side2 barrier for ERB: %s %s' % (barrierType, side2Barrier), 'DEBUG')
                instrument = (side1, side2)
            # Map a bought EOR as:
            # side1 - bought Digital European put  with strike at low  trigger of the EOR, with half the premium.
            # side2 - bought Digital European call with strike at high trigger of the EOR, with half the premium.
            # Map a sold   EOR as:
            # side1 - sold   Digital European put  with strike at low  trigger of the EOR, with half the premium.
            # side2 - sold   Digital European call with strike at high trigger of the EOR, with half the premium.
            elif marketName == 'European Outside Range':
                side1element = self.createRangeBinaryOtherSideElement(legElement, True)
                self.logLeg(marketName, side1element, otcLegNumber, faLegNumber);
                side1, exotic1 = self.mapDigitalEuropean(side1element, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
                side1Barrier   = getFloatValue(legElement, "FX2DownBarrierFX1FX2")
                side1.StrikeType('Absolute')
                side1.StrikePrice(side1Barrier)
                self.commitEntity(side1)
                barrierType = 'None'
                self.mapExoticBarrierOptionType(barrierType, exotic1)
                self.commitEntity(exotic1)
                self.commitEntity(side1)
                #side1.Barrier(side1Barrier)
                self.commitEntity(side1)
                side1Trade = side1.Trades()[0]
                side1Trade.Premium(side1Trade.Premium() / 2.0)
                self.commitEntity(side1Trade)
                logme('Remapped side1 barrier for EOR: %s %s' % (barrierType, side1Barrier), 'DEBUG')
                side2element = legElement
                self.logLeg(marketName, side2element, otcLegNumber, faLegNumber);
                side2, exotic2 = self.mapDigitalEuropean(side2element, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
                side2Barrier = getFloatValue(legElement, "FX2UpBarrierFX1FX2")
                side2.StrikePrice(side2Barrier)
                side2.StrikeType('Absolute')
                #side2.Barrier(side2Barrier)
                side2Trade = side2.Trades()[0]
                side2Trade.Premium(side2Trade.Premium() / 2.0)
                self.commitEntity(side2)
                barrierType   = 'None'
                self.mapExoticBarrierOptionType(barrierType, exotic2)
                self.commitEntity(exotic2)
                logme('Remapped side2 barrier for EOR: %s %s' % (barrierType, side2Barrier), 'DEBUG')
                instrument = (side1, side2)
            elif marketName == 'Partial One Touch':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapPartialDigitalOneTouch(legElement, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
            elif marketName == 'Partial No Touch':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapPartialDigitalNoTouch(legElement, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
            elif marketName == 'Partial Digital European':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapDigital(legElement, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
            elif marketName == 'Partial Double One Touch':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapPartialDigitalDoubleOneTouch(legElement, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
            elif marketName == 'Partial Double No Touch':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapPartialDigitalDoubleNoTouch(legElement, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
            elif marketName == 'Digital Barrier Down and Out':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapDigitalBarrier(legElement, fullFilename, faLegNumber, 'Down & Out')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Digital Barrier Down and In':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                self.mapDigitalBarrier(legElement, fullFilename, faLegNumber, 'Down & In')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Digital Barrier Up and Out':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                self.mapDigitalBarrier(legElement, fullFilename, faLegNumber, 'Up & Out')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Digital Barrier Up and In':
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                instrument = self.mapDigitalBarrier(legElement, fullFilename, faLegNumber, 'Up & In')
                faLegNumber = faLegNumber + 1
            elif marketName == 'Lookback Strike':
                #instrument = self.mapLookbackStrike(legElement, fullFilename, faLegNumber)
                logme('Market "%s" not implemented.' % (marketName), 'WARNING')                
            elif marketName == 'Compound Call':
                #instrument = self.mapCompound(legElement, fullFilename, faLegNumber)
                logme('Market "%s" not implemented.' % (marketName), 'WARNING')
            elif marketName == 'Compound Put':
                #instrument = self.mapCompound(legElement, fullFilename, faLegNumber)
                logme('Market "%s" not implemented.' % (marketName), 'WARNING')
            # A bought call plus a sold put (or a sold call plus a bought put) 
            # creates a sold synthetic forward.
            elif marketName == 'Synthetic Fwd':
                otherSideElement = self.createOtherSyntheticForwardElement(legElement)
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                side1 = self.mapVanillaOption(legElement, fullFilename, faLegNumber)
                faLegNumber = faLegNumber + 1
                self.logLeg(marketName, otherSideElement, otcLegNumber, faLegNumber);
                side2 = self.mapVanillaOption(otherSideElement, fullFilename, faLegNumber)
                instrument = (side1, side2)
                faLegNumber = faLegNumber + 1
            # Map a barrier forward as a bought (or sold) barrier call plus a
            # sold (or bought) barrier put.
            # The only difference (aside from numbers) between the OTC XML files
            # for a regular barrier and a barrier forward is the name of the market.
            # The only differences (aside from numbers) between the OTC XML files
            # for a bought call and a sold put, etc., are the call and put currencies
            # and the buy/sell directions.
            # The implementation simply copies the XML for the leg and swaps these elements.
            elif marketName == 'Down and Out Fwd':
                otherSideElement = self.createOtherSideElement(legElement)
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                side1, ignore = self.mapBarrier(legElement, fullFilename, faLegNumber, 'Down & Out')
                faLegNumber = faLegNumber + 1                
                self.logLeg(marketName, otherSideElement, otcLegNumber, faLegNumber);
                side2, ignore = self.mapBarrier(otherSideElement, fullFilename, faLegNumber, 'Down & Out')
                faLegNumber = faLegNumber + 1
                instrument = (side1, side2)
            elif marketName == 'Down and In Fwd':
                otherSideElement = self.createOtherSideElement(legElement)
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                side1, ignore = self.mapBarrier(legElement, fullFilename, faLegNumber, 'Down & In')
                faLegNumber = faLegNumber + 1                
                self.logLeg(marketName, otherSideElement, otcLegNumber, faLegNumber);
                side2, ignore = self.mapBarrier(otherSideElement, fullFilename, faLegNumber, 'Down & In')
                faLegNumber = faLegNumber + 1
                instrument = (side1, side2)
            elif marketName == 'Up and In Fwd':
                otherSideElement = self.createOtherSideElement(legElement)
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                side1, ignore = self.mapBarrier(legElement, fullFilename, faLegNumber, 'Up & In')
                faLegNumber = faLegNumber + 1                
                self.logLeg(marketName, otherSideElement, otcLegNumber, faLegNumber);
                side2, ignore = self.mapBarrier(otherSideElement, fullFilename, faLegNumber, 'Up & In')
                faLegNumber = faLegNumber + 1
                instrument = (side1, side2)
            elif marketName == 'Up and Out Fwd':
                otherSideElement = self.createOtherSideElement(legElement)
                self.logLeg(marketName, legElement, otcLegNumber, faLegNumber);
                side1, ignore = self.mapBarrier(legElement, fullFilename, faLegNumber, 'Up & Out')
                faLegNumber = faLegNumber + 1                
                self.logLeg(marketName, otherSideElement, otcLegNumber, faLegNumber);
                side2, ignore = self.mapBarrier(otherSideElement, fullFilename, faLegNumber, 'Up & Out')
                faLegNumber = faLegNumber + 1
                instrument = (side1, side2)
            if instrument:
                if isinstance(instrument, types.TupleType):
                    for object in instrument:
                        if str(object.ClassName()) == 'FOption':
                            instruments.append(object)
                else:
                    instruments.append(instrument)
            otcLegNumber = otcLegNumber + 1
        return instruments
    def mapPartialBarrier(self, element, xmlFilename, legNumber, barrierType):
        barrierDirection = self.getBarrierDirectionFromType(barrierType)
        acmInstrument, acmExotic = self.mapBarrier(element, xmlFilename, legNumber, barrierType)
        self.addBarrierEvent(element, acmInstrument, acmExotic)
        return acmInstrument, acmExotic
    def mapPartialDigitalDoubleNoTouch(self, element, xmlFilename, legNumber):
        acmInstrument, acmExotic = self.mapDigital(element, xmlFilename, legNumber)
        self.mapInstrumentBarrier(element, 'Down', acmInstrument)
        self.commitEntity(acmInstrument)
        self.mapExoticBarrierOptionType('Double Out', acmExotic)
        self.mapExoticDoubleBarrier(element, 'Up', acmExotic)
        self.commitEntity(acmExotic)
        self.addBarrierEvent(element, acmInstrument, acmExotic)
        return acmInstrument, acmExotic
    def mapPartialDigitalDoubleOneTouch(self, element, xmlFilename, legNumber):
        acmInstrument, acmExotic = self.mapDigital(element, xmlFilename, legNumber)
        self.mapInstrumentBarrier(element, 'Down', acmInstrument)
        self.commitEntity(acmInstrument)
        self.mapExoticBarrierOptionType('Double In', acmExotic)
        self.mapExoticDoubleBarrier(element, 'Up', acmExotic)
        self.addBarrierEvent(element, acmInstrument, acmExotic)
        self.commitEntity(acmExotic)
        return acmInstrument, acmExotic
    def mapPartialDigitalNoTouch(self, element, xmlFilename, legNumber):
        acmInstrument, acmExotic = self.mapDigital(element, xmlFilename, legNumber)
        barrierDirection = self.getBarrierDirection(element)
        self.mapExoticBarrierOptionType(barrierDirection + ' & Out', acmExotic)
        self.addBarrierEvent(element, acmInstrument, acmExotic)
        self.commitEntity(acmExotic)
        return acmInstrument, acmExotic
    def mapPartialDigitalOneTouch(self, element, xmlFilename, legNumber):
        acmInstrument, acmExotic = self.mapDigitalOneTouch(element, xmlFilename, legNumber)
        self.addBarrierEvent(element, acmInstrument, acmExotic)
        return acmInstrument, acmExotic
    def mapPartialDoubleBarrier(self, element, xmlFilename, legNumber, barrierType):
        barrierDirection = self.getBarrierDirectionFromType(barrierType)
        acmInstrument, acmExotic = self.mapDoubleBarrier(element, xmlFilename, legNumber, barrierType)
        self.addBarrierEvent(element, acmInstrument, acmExotic)
        return acmInstrument, acmExotic
    def mapTradeAcquireDay(self, element, acmTrade):
        acquireDay = getDateValue(element, 'ValueDate')
        logme('mapTradeAcquireDay: %s' % (acquireDay), 'DEBUG')
        ## acmTrade.AcquireDay(ael.date(acquireDay))
        acmTrade.AcquireDay(acquireDay)
    def mapTradeAcquirer(self, xmlDocument, acmTrade):
        logme('mapTradeAcquirer: %s' % (self.acquirer.Name()), 'DEBUG')
        acmTrade.Acquirer(self.acquirer)
    def mapTradeCounterparty(self, xmlDocument, acmTrade):
        logme('mapTradeCounterparty: %s' % (self.counterparty.Name()), 'DEBUG')
        acmTrade.Counterparty(self.counterparty)
    def mapTradeCurrency(self, element, acmTrade):
        tradeCurrency = self.getTradeCurrency(element)
        logme('mapTradeCurrency: %s' % (tradeCurrency), 'DEBUG')
        acmTrade.Currency(acm.FCurrency[tradeCurrency])
    def mapTradeOptionalKey(self, element, acmTrade, xmlFilename, legNumber):
        path, file = os.path.split(xmlFilename)
        file, ext = os.path.splitext(file)
        #acmTrade.OptionalKey('DTT_' + file.encode('latin-1'))  
        optionalKey = 'DTT_' + file.encode() + 'L' + str(legNumber + 1)
        logme('mapTradeOptionalKey: %s' % (optionalKey), 'DEBUG')
        acmTrade.OptionalKey(optionalKey)
    def mapTradePortfolio(self, xmlDocument, acmTrade):
        logme('mapTradePortfolio: %s' % (self.portfolio.Name()), 'DEBUG')
        acmTrade.Portfolio(self.portfolio)
    def mapTradePremium(self, element, acmTrade):
        premium = self.getPremium(element)
        buySell = self.getBuySell(element)
        if buySell == 'BUY':
            premium = premium * -1.0
        logme('mapTradePremium: %f' % (premium), 'DEBUG')
        acmTrade.Premium(premium)
    def mapTradePrice(self, element, acmTrade):
        # Should always be priced premium per FX2.
        #
        tradedType = self.getTradedType(element)
        logme('  tradedType: %s' % (tradedType), 'DEBUG')
        premiumCurrency = self.getPremiumCurrency(element)
        logme('  premiumCurrency: %s' % (premiumCurrency), 'DEBUG')
        fx2Currency = self.getFX2Currency(element)
        logme('  fx2Currency: %s' % (fx2Currency), 'DEBUG')
        if tradedType[0] == '%':
            if premiumCurrency == fx2Currency:
                tradePrice = getFloatValue(element, 'PremiumPrcntFX2') 
            else:
                ## tradePrice = 0.0 # FloatValue(element, 'PremiumPrcntFX1')
                tradePrice = getFloatValue(element, 'PremiumPrcntFX1')
                logme('mapTradePrice: Entry of price in "% of FX1" terms not supported.', 'WARNING')
            tradePrice = tradePrice
        else:
            if premiumCurrency == fx2Currency:
                ## tradePrice = 0.0 # 100000.0 * getFloatValue(element, 'PremiumFX2FX1')
                tradePrice = getFloatValue(element, 'PremiumFX2FX1')
                logme('mapTradePrice: Entry of price in "FX2 per FX1" terms not supported.', 'WARNING')
                tradePrice = getFloatValue(element, 'PremiumFX1FX2') 
                # Then divide by ACM point value for currency pair strike (FX1) per underlying (FX2).
                # If FX1 is Currency2 in Prime, use normal quoting terms; otherwise, use inverse.
                fx1 = self.getFX1Currency(element)
                fx2 = self.getFX2Currency(element)
                currencyPair = acm.FCurrency[fx1].CurrencyPair(acm.FCurrency[fx2])        
                if fx1 == str(currencyPair.Currency2().Name()):
                    pointValue = currencyPair.PointValue()
                else:
                    pointValue = currencyPair.PointValueInverse()
                tradePrice = tradePrice / pointValue
            else:
                tradePrice = getFloatValue(element, 'PremiumFX1FX2') 
                # Then divide by ACM point value for currency pair strike (FX1) per underlying (FX2).
                # If FX1 is Currency2 in Prime, use normal quoting terms; otherwise, use inverse.
                fx1 = self.getFX1Currency(element)
                fx2 = self.getFX2Currency(element)
                currencyPair = acm.FCurrency[fx1].CurrencyPair(acm.FCurrency[fx2])        
                if fx1 == str(currencyPair.Currency2().Name()):
                    pointValue = currencyPair.PointValue()
                else:
                    pointValue = currencyPair.PointValueInverse()
                tradePrice = tradePrice / pointValue
        buySell = self.getBuySell(element)
        if buySell == 'BUY':
            tradePrice = tradePrice
        logme('mapTradePrice: %f' % (tradePrice), 'DEBUG')
        acmTrade.Price(tradePrice)
    def mapTradeQuantity(self, element, acmTrade):
        tradeQuantity = self.getTradeQuantity(element)
        acmTrade.Quantity(tradeQuantity)
        logme('mapTradeQuantity: %f' % (tradeQuantity), 'DEBUG')
    def mapTradeStatus(self, element, acmTrade):
        tradeStatus = 'Simulated'
        logme('mapTradeStatus: %s' % (tradeStatus), 'DEBUG')
        acmTrade.Status(tradeStatus)
    def mapTradeStrategyType(self, element, acmTrade):
        documentTag = self.getDocumentTag(element)
        strategy = self.getStrategy(element)
        strategyType = self.getStrategyType(element)
        if strategyType == None:
            strategyType == ''
        tradeStrategyType = ('%s %s %s' % (documentTag, strategy, strategyType))
        strategyType = tradeStrategyType.encode()
        additionalInfo = acmTrade.AdditionalInfo()
        additionalInfo.Option_Strategy(str(tradeStrategyType))
        self.commitEntity(additionalInfo)
        logme('mapTradeStrategyType: %s' % (strategyType), 'DEBUG')
    def mapTradeStrategyReference(self, fullFilename, acmTrade):
        filename = os.path.basename(fullFilename)
        filename = os.path.splitext(filename)[0]
        filename = filename.encode()
        additionalInfo = acmTrade.AdditionalInfo()
        additionalInfo.Option_Reference(str(filename))
        #self.commitEntity(additionalInfo)
        logme('mapTradeStrategyReference: %s' % (filename), 'DEBUG')
    def mapTradeTime(self, xmlDocument, acmTrade):
        tradeTime = acm.FDateTime()
        logme('mapTradeTime: %s' % (tradeTime), 'DEBUG')
        acmTrade.TradeTime(tradeTime)
    def mapTradeTrader(self, xmlDocument, acmTrade):
        logme('mapTradeTrader: %s' % (self.trader.Name()), 'DEBUG')
        acmTrade.Trader(self.trader)
    def mapTradeType(self, xmlDocument, acmTrade):
        tradeType = 1
        logme('mapTradeType: %s' % (tradeType), 'DEBUG')
        acmTrade.Type(tradeType)
    def mapTradeValueDay(self, element, acmTrade):
        element = element.getElementsByTagName('ValueDate')[0]
        valueDay = getDate(element)
        logme('mapTradeValueDay: %s' % (valueDay), 'DEBUG')
        acmTrade.ValueDay(valueDay)
    # A put option to sell currency A for currency B at strike K
    # is the same as a call option to buy B with A at 1 / K.
    # Similarly, a call option to buy currency A with currency B at strike K
    # is the same as a put option to sell B for A at 1 / K.
    def mapVanillaOption(self, element, xmlFilename, legNumber, exerciseOverride = None):
        acmInstrument = acm.FOption()
        acmTrade = acm.FTrade()
        acmTrade.Instrument(acmInstrument)
        acmInstrument.Trades().Add(acmTrade)
        self.mapInstrumentContractSize(element, acmInstrument)
        self.mapInstrumentCurrency(element, acmInstrument)
        self.mapInstrumentExerciseType(element, acmInstrument, exerciseOverride)
        self.mapInstrumentExpiryDate(element, acmInstrument)
        self.mapInstrumentIsCall(element, acmInstrument)
        self.mapInstrumentName(element, acmInstrument, xmlFilename, legNumber)
        self.mapInstrumentPayOffsetMethod(element, acmInstrument)
        self.mapInstrumentPayDayOffset(element, acmInstrument)
        self.mapInstrumentQuoteType(element, acmInstrument)
        self.mapInstrumentSettlementType(element, acmInstrument)
        self.mapInstrumentStrikeCurrency(element, acmInstrument)
        self.mapInstrumentStrikePrice(element, acmInstrument)
        self.mapInstrumentStrikeType(element, acmInstrument)
        self.mapInstrumentStrikeQuotationType(element, acmInstrument)
        self.mapInstrumentUnderlyingCurrency(element, acmInstrument)
        self.mapInstrumentValuationGrpChlItem(element, acmInstrument)
        self.mapTradeAcquireDay(element, acmTrade)
        self.mapTradeAcquirer(element, acmTrade)
        self.mapTradeCounterparty(element, acmTrade)
        self.mapTradeCurrency(element, acmTrade)
        # Removed due to conflict with the use of this field for delta hedges.
        # However, the same information is encoded in the instrument ID.
        #self.mapTradeOptionalKey(element, acmTrade, xmlFilename, legNumber)
        self.mapTradePortfolio(element, acmTrade)
        self.mapTradePremium(element, acmTrade)
        self.mapTradePrice(element, acmTrade)        
        self.mapTradeQuantity(element, acmTrade)
        self.mapTradeStatus(element, acmTrade)
        self.mapTradeTime(element, acmTrade)
        self.mapTradeTrader(element, acmTrade)
        self.mapTradeType(element, acmTrade)
        self.mapTradeValueDay(element, acmTrade)
        self.mapInstrumentFixingSource(element, acmInstrument)
        self.commitEntity(acmInstrument)
        self.commitEntity(acmTrade)
        return acmInstrument
    def moveException(self, oldPath):
        try:
            parts = os.path.split(oldPath)
            exceptionDir = os.path.join(parts[0], 'exceptions')
            if not os.path.exists(exceptionDir):
                os.mkdir(exceptionDir)
            newPath = os.path.join(parts[0], 'exceptions', parts[1])
            shutil.move(oldPath, newPath)
        except:
            traceback.print_exc()
    def moveProcessed(self, oldPath):
        try:
            parts = os.path.split(oldPath)
            processedDir = os.path.join(parts[0], 'processed')
            if not os.path.exists(processedDir):
                os.mkdir(processedDir)
            newPath = os.path.join(parts[0], 'processed', parts[1])
            shutil.move(oldPath, newPath)
        except:
            traceback.print_exc()
    def parseDocument(self, fullFilename):
        beganAt = time.clock()
        logme('BEGAN parseDocument...', 'INFO')
        try:
            self.beginTransaction()
            document = xml.dom.minidom.parse(fullFilename.encode())
            instrumentType = self.getDocumentTag(document)
            instruments = None
            # Each leg is a complete dea, thus we simply skip over enclosing
            # elements of OTC multileg deals.
            if   instrumentType in ('DTVanillaOptionOutrightTrade', 'DTMultiOEOptionTrade'):
                instruments = self.mapLegs(document, fullFilename)
            elif instrumentType == 'DTBarrierOptionTrade':
                instruments = self.mapLegs(document, fullFilename)
            elif instrumentType == 'DTStraddleOptionTrade':
                instruments = self.mapLegs(document, fullFilename)
            elif instrumentType == 'DTStrangleOptionTrade':
                instruments = self.mapLegs(document, fullFilename)
            elif instrumentType == 'DTSpreadOptionTrade':
                instruments = self.mapLegs(document, fullFilename)
            elif instrumentType == 'DTTimeSpreadOptionTrade':
                instruments = self.mapLegs(document, fullFilename)
            elif instrumentType == 'DTComboOptionTrade':
                instruments = self.mapLegs(document, fullFilename)
            elif instrumentType == 'DTTimeComboOptionTrade':
                instruments = self.mapLegs(document, fullFilename)
            elif instrumentType == 'DTBarrierOptionTrade':
                instruments = self.mapLegs(document, fullFilename)
            elif instrumentType == 'DTDigitalOptionTrade':
                instruments = self.mapLegs(document, fullFilename)
            if instruments != None:
                for instrument in instruments:
                    for trade in instrument.Trades():
                        self.mapTradeStrategyType(document, trade)
                        self.mapTradeStrategyReference(fullFilename, trade)
                        self.commitEntity(trade)
                self.commitTransaction()
                self.listEntities(instruments, 'After committing:')
                self.moveProcessed(fullFilename)
            else:
                logme('No handleable instruments were found in the XML document!', 'ERROR')
        except:
            self.abortTransaction()
            traceback.print_exc()
            self.moveException(fullFilename)
        endedAt = time.clock()
        logme('ENDED parseDocument: %9.3f' % (endedAt - beganAt), 'INFO')
    def report(self):
        try:
            logme('OTCFATradeServer PARAMETERS', 'INFO')
            for parameter, value in parameters.items():
                logme('Parameter:   %s = %s' % (parameter, value), 'DEBUG')
        except:
            traceback.print_exc()
    def wasCaptured(self, filename):
        try:
            document = xml.dom.minidom.parse(filename.encode())
            path, file = os.path.split(filename)
            file, ext = os.path.splitext(file)
            instrumentName = 'DT_' + file.encode()
            # Figure out how many trades we are looking for in this market.
            otcLegNumber = 0
            faLegNumber = 0
            marketNamesForLegs = {}
            while True:
                instrument = None
                otcLegName = 'Leg%d' % (otcLegNumber)
                elements = document.getElementsByTagName(otcLegName)
                if not elements:
                    break
                legElement = elements[0]
                marketName = self.getMarketName(legElement)
                marketNamesForLegs[otcLegName] = marketName
                otcLegNumber = otcLegNumber + 1
            tradeCount = 0
            for otcLegName, marketName in marketNamesForLegs.items():
                if marketName in self.doubleTrades:
                    tradeCount = tradeCount + 2
                else:
                    tradeCount = tradeCount + 1
            logme('Looking for %d trades for instruments like "%s"...' % (tradeCount, instrumentName), 'INFO')
            instruments = acm.FOption.Select('name like %s*' % instrumentName)
            if not instruments:
                return False
            if len(instruments) == 0:
                return False
            tradesFound = 0
            for instrument in instruments:
                logme('Found instrument: "%s"' % instrument.Name(), 'INFO')
                trades = instrument.Trades()
                if not trades:
                    return False
                if len(trades) == 0:
                    return false
                for trade in instrument.Trades():
                    logme('  with trade: "%s"' % trade.Oid(), 'INFO')
                    tradesFound = tradesFound + 1
            if tradesFound == tradeCount:
                return True
            else:
                return False
        except:
            traceback.print_exc()
            return False
    def parseExistingFiles(self):
        logme('BEGAN PARSING EXISTING FILES...', 'INFO')
        try:
            newfiles = self.getNewFiles(self.otc_xml_output_path)
            for filename in newfiles:
                if filename.find('.xml') >= 0:
                    logme('Found existing document "%s" at %s.' % (filename, time.ctime(self.fileCache[filename].st_mtime)), 'INFO')
                    if self.wasCaptured(filename) == True:
                        logme('"%s" has already been captured.' % filename, 'INFO')
                        self.moveProcessed(filename)
                    else:
                        logme('"%s" has not been captured, processing...' % filename, 'INFO')
                        self.parseDocument(filename)
        except:
            traceback.print_exc()
        logme('ENDED PARSING EXISTING FILES.', 'INFO')
    def run(self):
        logme('RUNNING...', 'INFO')
        global useWin32
        try:
            self.trader = resolveObject(self.trader, acm.FUser)
            self.acquirer = resolveObject(self.acquirer, acm.FParty)
            self.counterparty = resolveObject(self.counterparty, acm.FParty)
            self.portfolio = resolveObject(self.portfolio, acm.FPhysicalPortfolio)
            self.parseExistingFiles()
            if useWin32:
                FILE_LIST_DIRECTORY = 0x000000001
                FILE_SHARE_READ	= 0x00000001
                FILE_SHARE_WRITE = 0x00000002
                OPEN_EXISTING = 3
                FILE_FLAG_BACKUP_SEMANTICS = 33554432
                FILE_NOTIFY_CHANGE_LAST_WRITE = 0x00000010
                FILE_NOTIFY_CHANGE_FILE_NAME = 0x00000001
                directoryHandle = ctypes.windll.kernel32.CreateFileA(self.otc_xml_output_path,
                                                                     FILE_LIST_DIRECTORY,
                                                                     FILE_SHARE_READ | FILE_SHARE_WRITE,
                                                                     None,
                                                                     OPEN_EXISTING,
                                                                     FILE_FLAG_BACKUP_SEMANTICS,
                                                                     None
                                                                     )
                bytesReturned = ctypes.c_int(0)
                while self.keepRunning:    
                    fileNotifyInformation = ctypes.create_string_buffer(1024)
                    result = ctypes.windll.kernel32.ReadDirectoryChangesW(directoryHandle,
                                                                          fileNotifyInformation,
                                                                          ctypes.sizeof(fileNotifyInformation),
                                                                          None,
                                                                          FILE_NOTIFY_CHANGE_FILE_NAME,
                                                                          ctypes.byref(bytesReturned),
                                                                          None,
                                                                          None
                                                                          )
                    directoryChanges = parseFileNotifyInformation(fileNotifyInformation)
                    for action, filename in directoryChanges:
                        fullFilename = os.path.join (self.otc_xml_output_path, filename)
                        if action == 5 and fullFilename.find('.xml') >= 0:
                            logme('Trade captured in: %s' % (fullFilename), 'INFO')
                            self.parseDocument(fullFilename)
            else:
                oldfiles = self.getNewFiles(self.otc_xml_output_path)
                for filename in oldfiles:
                    if filename.find('.xml') >= 0:
                        logme('Ignoring existing deal %s.' % (filename), 'DEBUG')
                logme('READY...', 'INFO')
                while self.keepRunning:
                    newfiles = self.getNewFiles(self.otc_xml_output_path)
                    for filename in newfiles:
                        if filename.find('.xml') >= 0:
                            logme('Trade captured in "%s" at %s.' % (filename, time.ctime(self.fileCache[filename].st_mtime)), 'INFO')
                            self.parseDocument(filename)
                    #time.sleep(self.polling_interval)
                    acm.PollDbEvents(self.polling_interval)
        except:
            traceback.print_exc()
    def shutdown(self):
        try:
            logme('SHUTTING DOWN...', 'INFO')
            self.keepRunning = False
        except:
            traceback.print_exc()
        threading.Timer(5.0, lambda: os._exit(0)).start()

class FixingPeriod(object):
    def __init__(self, fixingPeriodElement, fixingSchedule):
        self.fixingSchedule = fixingSchedule
        self.time =     getTextValue( fixingPeriodElement, 'Time')
        self.location = getTextValue( fixingPeriodElement, 'Location')
        self.month =    getIntValue(  fixingPeriodElement, 'Month')
        self.day =      getIntValue(  fixingPeriodElement, 'Day')
        self.year =     getIntValue(  fixingPeriodElement, 'Year')
        self.time =     getTextValue( fixingPeriodElement, 'Time')
        self.weight =   getFloatValue(fixingPeriodElement, 'Weight')
        self.type =     getTextValue( fixingPeriodElement, 'Type')
        self.rate =     getFloatValue(fixingPeriodElement, 'Rate')
    def addEvent(self, acmInstrument):
        exoticEvent = acm.FExoticEvent()
        exoticEvent.Instrument(acmInstrument)
        exoticEvent.ComponentInstrument(acmInstrument.Underlying())
        ## eventStart = ael.date_from_ymd(self.year, self.month, self.day)
        eventStart = acm.Time().DateFromYMD(self.year, self.month, self.day)
        exoticEvent.Date(eventStart) 
        exoticEvent.EventValue(-1.0)
        if self.type == 'spot':
            exoticEvent.Type('Average Price')
        elif self.type == 'strike':
            exoticEvent.Type('Average Strike')
        self.fixingSchedule.otcfaTradeServer.commitEntity(exoticEvent)
    def addTimeSeries(self, acmInstrument):        
        timeSeries = acm.FTimeSeries()
        if self.type == 'spot':
            timeSeriesSpec = acm.FTimeSeriesSpec['OTCFA Avg Price Wt']
        elif self.type == 'strike':
            timeSeriesSpec = acm.FTimeSeriesSpec['OTCFA Avg Strike Wt']
        timeSeries.TimeSeriesSpec(timeSeriesSpec)
        timeSeries.Recaddr(acmInstrument.Oid())
        ## eventStart = ael.date_from_ymd(self.year, self.month, self.day)
        eventStart = acm.Time().DateFromYMD(self.year, self.month, self.day)
        timeSeries.Value(self.weight * self.fixingSchedule.averageAtFix)
        timeSeries.Day(eventStart)
        timeSeries.RunNo(0)
        self.fixingSchedule.otcfaTradeServer.commitEntity(timeSeries)
        self.fixingSchedule.otcfaTradeServer.commitEntity(timeSeriesSpec)
        
class FixingSchedule(object):
    def __init__(self, otcfaTradeServer, element):
        self.otcfaTradeServer = otcfaTradeServer
        fixingScheduleElement = element.getElementsByTagName('FixingSchedule')[0]
        self.source =           getTextValue( fixingScheduleElement, 'Source')
        self.terms =            getTextValue( fixingScheduleElement, 'Terms')
        self.averageAtFix =     getFloatValue(fixingScheduleElement, 'AverageAtFix')
        tableElement = fixingScheduleElement.getElementsByTagName('Table')[0]
        fixingPeriodElements = tableElement.getElementsByTagName('Period')
        self.fixingPeriods = []
        for fixingPeriodElement in fixingPeriodElements:
            self.fixingPeriods.append(FixingPeriod(fixingPeriodElement, self))
        
#==================================================================
# GLOBALS
#==================================================================

try:
    import FBDPParameters
    reload(FBDPParameters)

    TestMode = 0
    Date = FBDPParameters.Date
    LogMode = FBDPParameters.LogMode
    LogToConsole = FBDPParameters.LogToConsole
    LogToFile = FBDPParameters.LogToFile
except:
    TestMode = 1
    Date = "Today"
    LogMode = 1
    LogToConsole = 1
    LogToFile = 0

#=======================================================================
# Main
#=======================================================================

ael_variables = OTCFAConfiguration.configuration.getAelVariablesForModule(__name__)

# Run in a separate thread to listen for commands from Prime.
class RemoteController(SimpleXMLRPCServer.SimpleXMLRPCServer, threading.Thread):
    def __init__(self, otcFATradeServer):
        SimpleXMLRPCServer.SimpleXMLRPCServer.__init__(self, ('localhost', otcFATradeServer.ts_controller_port))
        threading.Thread.__init__(self)
        self.otcFATradeServer = otcFATradeServer
        self.register_function(self.report)
        self.register_function(self.shutdown)
        self.keepRunning = True
    def report(self):
        self.otcFATradeServer.report()
        return 1
    def shutdown(self):
        self.otcFATradeServer.shutdown()
        return 1
    def run(self):
        self.keepRunning = True
        try:
            while self.keepRunning:
                self.handle_request()
        except:
            traceback.print_exc()
def signalHandler(signum, frame):
    logme('Received signal %s' % (signum), 'WARNING')
    try:
        global server
        if server:
            server.shutdown()
    except:
        traceback.print_exc()
        
def ael_main(parameters):
    global server
    global controller
    try:
        ScriptName = 'OTCFATradeServer'
        LogMode = int(parameters['logmode'])
        LogToConsole = int(parameters['log_to_console'])
        LogToFile = int(parameters['log_to_file'])
        Logfile = parameters.get('ts_logfile')
        SendReportByMail = False
        MailList = []
        ReportMessageType = None
        logme.setLogmeVar(ScriptName, LogMode, LogToConsole, LogToFile, Logfile, SendReportByMail, MailList, ReportMessageType)
        parameters['today_date'] = acm.Time().DateNow()
         
        if LogMode > 1:
            for parameter, value in parameters.items():
                logme('Parameter:   %s = %s' % (parameter, value), 'DEBUG')
        server = OTCFATradeServer(parameters)
        if (__name__ == '__main__') or (server.objectServer == "'FACMServer'"):
            try:
                atexit.register(server.shutdown)
                signal.signal(signal.SIGBREAK, signalHandler)
                signal.signal(signal.SIGSEGV, signalHandler)
                signal.signal(signal.SIGTERM, signalHandler)
                signal.signal(signal.SIGABRT, signalHandler)
                signal.signal(signal.SIGINT, signalHandler)
                controller = RemoteController(server)
                controller.start()
                server.run()
            except:
                traceback.print_exc()            
        else:
            logme('This script must be run as an ATS Task in order to work properly.', 'ERROR')
            time.sleep(10)
    except:
        traceback.print_exc()
    logme('Finished.', 'INFO')

if __name__ == '__main__':
    ael_main(defaultParameters)
