from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FAOTCMarketServer - Update Derivatech Market Data Server (MDS)
	with spot rates, deposit rates, and volatility surfaces
	from FRONT ARENA.
    
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
    (e.g. 0:01) and run all day.
    
    When running as a task in ATS, starts a SimpleXMLRPCServer thread
    that listens to a controller port for commands, such as for shutdown.

ENDDESCRIPTION
"""
import OTCFAConfiguration
import atexit
import copy
import cStringIO
import os
import signal
import SimpleXMLRPCServer
import string
import sys
import threading
import time 
import traceback
import xmlrpclib
import math

# For signal handler to shut down server.
global server
server = None

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

from Fnorb.orb import CORBA

import DTCOMMON
import DTRemoteObjectException
import DTSession
import DTSessionMediator
import DTMDS
import DTDateCalcMediator
import DTMDSBulkMediator

import acm

class FunctionTimer(object):
    def __init__(self, function):
        self.began = time.clock()
        self.prior_ended = self.began
        self.ended = self.began
        self.function = function
        self.block_count = 0
    def stop(self, block_label = ''):
        self.block_count = self.block_count + 1
        self.prior_ended = self.ended
        self.ended = time.clock()
        self.block_elapsed = self.ended - self.prior_ended
        self.total_elapsed = self.ended - self.began
        logme('TIME IN %s:  BLOCK: %d %s %s  TOTAL: %s' % (self.function, self.block_count, block_label, self.block_elapsed, self.total_elapsed), 'INFO')
  
if False:
    print (help(DTSessionMediator))
    print (help(DTSession))
    print (help(DTMDSBulkMediator))

def resolveObject(reference, clazz):
        if type(reference) == type(1) or type(reference) == type('') or type(reference) == type(1.0):
            return clazz[reference]
        else:
            return reference
    
def adjustDepositDate(date, bankingCurrency, currency1, currency2):
    method = 'Mod. Following'
    ccy1 = bankingCurrency.Name()
    ccy2 = currency1.Name()
    ccy3 = currency2.Name()
    adjustedDate = bankingCurrency.Calendar().ModifyDate(currency1.Calendar(), currency2.Calendar(), date)
    return adjustedDate
        
def getForwardDateForExpiry(date, bankingCurrency, currency1, currency2):
    method = 'Mod. Following'
    ccy1 = bankingCurrency.Name()
    ccy2 = currency1.Name()
    ccy3 = currency2.Name()
    adjustedDate = bankingCurrency.Calendar().ModifyDate(currency1.Calendar(), currency2.Calendar(), date)
    return adjustedDate
    
periodComparisons = {}
periodComparisons['O/N'] = 1
periodComparisons['1 Week'] = 7
periodComparisons['2 Week'] = 7 * 2
periodComparisons['3 Week'] = 7 * 3
periodComparisons['1 Month'] = 30
periodComparisons['2 Month'] = 2 * 30
periodComparisons['3 Month'] = 3 * 30
periodComparisons['6 Month'] = 6 * 30
periodComparisons['9 Month'] = 9 * 30
periodComparisons['1 Year'] = 360
periodComparisons['2 Year'] = 360 * 2
periodComparisons['3 Year'] = 360 * 3
periodComparisons['4 Year'] = 360 * 4
periodComparisons['5 Year'] = 360 * 5
periodComparisons['6 Year'] = 360 * 6
periodComparisons['7 Year'] = 360 * 7
periodComparisons['8 Year'] = 360 * 8
periodComparisons['9 Year'] = 360 * 9
periodComparisons['10 Year'] = 360 * 10

def skewComparator(a_, b_):
    a = a_.volPeriod
    b = b_.volPeriod
    if periodComparisons[a] < periodComparisons[b]:
        return -1
    if periodComparisons[a] > periodComparisons[b]:
        return 1
    return 0

defaultParameters = OTCFAConfiguration.configuration.getParametersForModule(__name__)

# Must be connected to ACM to import Front modules...
if __name__ == '__main__':
    print ('RUNNING STANDALONE...')
    try:
        for key,value in defaultParameters.items():
            print ('Default parameter: %s = %s' % (key, value))
        print ('Connecting to ACM...')
        acm.Connect(defaultParameters['ads_url'], defaultParameters['ads_username'], defaultParameters['ads_password'], defaultParameters['ads_password'])
    except:
        traceback.print_ex()

import FBDPString
reload(FBDPString)
import FBDPGui
reload(FBDPGui)

global logme
logme = FBDPString.logme

# ...but can't connect to ORB if already connected to ACM!
if __name__ == '__main__':
    try:
        for i in range(10):
            acm.PollDbEvents(100)
        acm.Disconnect()                
    except:
        logme(traceback.format_exc(), 'ERROR')

def ael_callback(caller, argument):
    logme('ael_callback: caller %s  argument %s' % (caller, argument), 'INFO')
    
def identify(whatisit):
    if whatisit == None:
        return 'None'
    name = None
    typename = str(type(whatisit))
    try:
        name = str(whatisit.Name())
    except:
        pass
    if name == None:
        try:
            name = str(whatisit.Oid())
        except:
            pass
    if name == None:
        try:
            name = str(whatisit.UniqueId())
        except:
             pass
    if name == None:
        name = 'no name'
    return "%s %s %s" % (typename, name, whatisit.Hash())
        
class FAOTCMarketServer(object):
    def __init__(self, parameters):
        logme('INITIALIZING FAOTCMarketServer...', 'INFO')
        self.__dict__.update(parameters)
        self.parameters = parameters
        self.objectServer = str(acm.ObjectServer())
        logme('Object server: %s' % (self.objectServer))
        self.useFxBasisCurves = True
        self.usePlainVolatilities = True
        self.server_type = ''
        self.server_name = ''
        self.db_name = ''
        self.schema_name = ''
        # CORBA entry points.
        # self.nameServiceCorbaloc = 'corbaloc:iiop:frt-ny-ws006:2591/NameService'
        # self.nameServiceCorbaloc = 'IOR:000000000000002849444c3a6f6d672e6f72672f436f734e616d696e672f4e616d696e67436f6e746578743a312e300000000001000000000000006d000100000000000d4652542d4e592d575330303600000a1f000000513a5c4652542d4e592d57533030363a4e533a4e435f315f467269205365702032322031372331372330312045445420323030363a3a4946523a436f734e616d696e675f4e616d696e67436f6e7465787400'
        # self.dtSessionMediatorCorbaloc = 'corbaloc:iiop:frt-ny-ws006:2591/DerivaTechConsulting/MarketDataServer/DTSessionMediator'
        self.dtSessionMediatorCorbaloc = 'IOR:000000000000001a49444c3a445453657373696f6e4d65646961746f723a312e3000000000000002000000000000005c000101000000000e6672742d6e792d6e6237343535000622000000393a5c6672742d6e792d6e62373435353a4d61726b6574446174615365727665723a303a3a49523a445453657373696f6e4d65646961746f72000000000000000000000001000000180100000001000000000000000800000001000000305f5449'

        # Fnorb corbaloc and naming don't inter-operate with Orbix,
        # because of incorrect CosNaming classpaths in Fnorb,
        # so we must look up the IOR which MDS logs when it starts.
        # Fortunately this is the only IOR that we need --
        # all the objects come out of this IOR as 'Mediators.'
        self.dtSessionMediatorCorbaloc = self.findDTSessionMediatorIOR(self.mds_ior_path)
        logme('DTSessionMediator corbaloc: %s' % (self.dtSessionMediatorCorbaloc), 'INFO')
        self.currencyWatchlist = {}
        self.yieldCurveWatchlist = {}
        self.benchmarkPriceWatchlist = {}
        self.priceWatchlist = {}
        self.currencyPairWatchlist = {}
        self.volatilityStructureWatchlist = {}
        self.instrumentsForVolatilityStructures = {}
        self.currenciesForVolatilityStructures = {}
        self.forwardDatesForCurrencies = {}
        self.keepRunning = True
        self.ms_controller_port = int(self.ms_controller_port)
        self.entitiesForSubscribedObjects = {}
        self.subscribedObjectsForEntities = {}
        self.updatesForCurrencyPairSpotRate = []
        self.updatesForDepositRateFromDeposit = []
        self.updatesForDepositRateFromYieldCurve = []
        self.updatesForVolatilitySurface = []
        self.updatesForDepositRate = []
    def tenorForVolPeriod(self, volPeriod):
        if volPeriod == 'O/N':
            return '1 Day'
        else:
            return volPeriod
    def printVolatility(self, volatility):
        print ('volatility.uniformMarketID:', volatility.uniformMarketID)
        print ('volatility.vObj.transObj.user:', volatility.vObj.transObj.user)
        print ('volatility.vObj.transObj.schema:', volatility.vObj.transObj.schema)
        print ('volatility.vObj.transObj.lockedForUpdate:', volatility.vObj.transObj.lockedForUpdate)
        print ('volatility.vObj.transObj.lUpdatable:', volatility.vObj.transObj.lUpdatable)
        print ('volatility.vObj.transObj.userLockedForUpdate:', volatility.vObj.transObj.userLockedForUpdate)
        print ('volatility.vObj.transObj.secondsLocked:', volatility.vObj.transObj.secondsLocked)
        print ('volatility.vObj.transObj.status:', volatility.vObj.transObj.status)
        print ('volatility.vObj.transObj.seconds:', volatility.vObj.transObj.seconds)
        print ('volatility.vObj.snapshot:', volatility.vObj.snapshot)
        print ('volatility.vObj.day:', volatility.vObj.day)
        print ('volatility.vObj.month:', volatility.vObj.month)
        print ('volatility.vObj.year:', volatility.vObj.year)
        print ('volatility.Fx1:', volatility.Fx1)
        print ('volatility.Fx2:', volatility.Fx2)
        print ('volatility.volHolidayWeightFX1:', volatility.volHolidayWeightFX1)
        print ('volatility.volHolidayWeightFX2:', volatility.volHolidayWeightFX2)
        print ('volatility.volWeekendWeight:', volatility.volWeekendWeight)
        print ('volatility.volAtmVolInput:', volatility.volAtmVolInput)
        print ('volatility.volEntryMethodCode:', volatility.volEntryMethodCode)
        print ('volatility.volEntryMethodDesc:', volatility.volEntryMethodDesc)
        volatility.volList.sort(skewComparator)
        for volForPeriod in volatility.volList:
            print (' volForPeriod.volPeriod:', volForPeriod.volPeriod)
            print ('  volForPeriod.volAsk:', volForPeriod.volAsk)
            print ('  volForPeriod.volBid:', volForPeriod.volBid)
            print ('  volForPeriod.volcDelta1Ask:', volForPeriod.volcDelta1Ask)
            print ('  volForPeriod.volcDelta1Bid:', volForPeriod.volcDelta1Bid)
            print ('  volForPeriod.volcDelta10Ask:', volForPeriod.volcDelta10Ask)
            print ('  volForPeriod.volcDelta10Bid:', volForPeriod.volcDelta10Bid)
            print ('  volForPeriod.volcDelta25Ask:', volForPeriod.volcDelta25Ask)
            print ('  volForPeriod.volcDelta25Bid:', volForPeriod.volcDelta25Bid)
            print ('  volForPeriod.volpDelta1Ask:', volForPeriod.volpDelta1Ask)
            print ('  volForPeriod.volpDelta1Bid:', volForPeriod.volpDelta1Bid)
            print ('  volForPeriod.volpDelta10Ask:', volForPeriod.volpDelta10Ask)
            print ('  volForPeriod.volpDelta10Bid:', volForPeriod.volpDelta10Bid)
            print ('  volForPeriod.volpDelta25Ask:', volForPeriod.volpDelta25Ask)
            print ('  volForPeriod.volpDelta25Bid:', volForPeriod.volpDelta25Bid)
            print ('  volForPeriod.volcDelta1Stat:', volForPeriod.volcDelta1Stat)
            print ('  volForPeriod.volcDelta10Stat:', volForPeriod.volcDelta10Stat)
            print ('  volForPeriod.volcDelta25Stat:', volForPeriod.volcDelta25Stat)
            print ('  volForPeriod.volpDelta1Stat:', volForPeriod.volpDelta1Stat)
            print ('  volForPeriod.volpDelta10Stat:', volForPeriod.volpDelta10Stat)
            print ('  volForPeriod.volpDelta25Stat:', volForPeriod.volpDelta25Stat)
            print ('  volForPeriod.volpATMStat:', volForPeriod.volpATMStat)
            print ('  volForPeriod.DeltaInputFlag:', volForPeriod.DeltaInputFlag)
        print ('volatility.volATMVolInterpMethod:', volatility.volATMVolInterpMethod)
        print ()
    def findDTSessionMediatorIOR(self, mdsPath):
        for root, dirs, filenames in os.walk(mdsPath):
            for filename in filenames:
                if filename.find('.log') >= 0:
                    ms_logfile = file(os.path.join(root, filename))    
                    while True:
                        line = ms_logfile.readline()
                        if line.find('Session Manager IOR:') >= 0:
                            tokens = string.split(line)
                            dtSessionMediatorCorbaloc = tokens.pop()                        
                            self.dtSessionMediatorCorbaloc = dtSessionMediatorCorbaloc
                            return self.dtSessionMediatorCorbaloc
                        if not line:
                            break
        return self.dtSessionMediatorCorbaloc
    def createCalculationSpace(self):
        self.space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    def connectACM(self):
        try:
            logme('CONNECTING TO ACM...', 'INFO')
            acm.Connect(self.ads_url, self.ads_username, self.ads_password, self.ads_password)
        except:
            logme(traceback.format_exc(), 'ERROR')
    def disconnectACM(self):
        try:
            logme('DISCONNECTING FROM ACM...', 'INFO')
            for i in range(10):
                acm.PollDbEvents(100)
                self.IdleCallback()
            acm.Disconnect()                
        except:
            logme(traceback.format_exc(), 'ERROR')
    def connectMDS(self):
        retries = int(self.parameters['failover_retries'])
        interval = int(self.parameters['failover_interval'])
        for retry in range(retries):
            logme('CONNECTING TO MDS, ATTEMPT %d of %d...' % ((1 + retry), retries), 'INFO')
            try:
                argv = []
                try:
                    argv = sys.argv
                except:
                    logme('No sys.argv', 'WARNING')
                self.orb = CORBA.ORB_init(argv, CORBA.ORB_ID)
                self.orb._fnorb_override_options({'Threading Model': 'Threaded'})
                logme('CORBA ORB = %s' % (self.orb), 'DEBUG')
                self.dtSessionMediator = self.orb.string_to_object(self.dtSessionMediatorCorbaloc)
                # Narrowing is not necessary with Fnorb.
                logme('objectReference %s = %s' % (self.dtSessionMediatorCorbaloc, self.dtSessionMediator), 'INFO')
                self.dtSessionMediator = self.dtSessionMediator._narrow(DTSessionMediator.DTSessionMediator)
                logme('dtSessionMediator = %s ' % (self.dtSessionMediator), 'INFO')
                self.dtSession = self.dtSessionMediator.logIn(self.server_type, self.server_name, self.mds_username, self.mds_password, self.db_name, self.schema_name)
                logme('dtSession = %s ' % (self.dtSession), 'INFO')
                self.dtBulkMarketDataMediator = self.dtSession.getMediator(11)
                logme('dtBulkMarketDataMediator = %s' % (self.dtBulkMarketDataMediator))
                self.dtMDSBulkMediator = self.dtSession.getMediator(14)
                logme('dtMDSBulkMediator = %s' % (self.dtMDSBulkMediator), 'INFO')
                self.dtDateCalcMediator = self.dtSession.getMediator(15)
                logme('dtDateCalcMediator = %s' % (self.dtDateCalcMediator), 'INFO')
                self.dtTransactionManager = self.dtSession.getTransactionManager()
                logme('dtTransactionManager = %s' % (self.dtTransactionManager), 'INFO')
                return
            except:
                logme(traceback.format_exc(), 'ERROR')
                logme('Waiting %s seconds to retry connecting to MDS...' % interval, 'WARNING')
                time.sleep(interval)
        logme('FAILED TO CONNECT TO MDS...' % retry, 'ERROR')
        self.shutdown()
    def reconnectMDS(self):
        self.connectMDS()
        self.initialUpdate()
    def disconnectMDS(self):
        try:
            logme('DISCONNECTING FROM MDS AND CORBA...', 'INFO')
            # Hangs.
            # CORBA.ORB_delete()
        except:
            logme(traceback.format_exc(), 'ERROR')
    def DateToday(self):
        return acm.Time().DateNow()
    def getForwardDateForExpiry(self, date, bankingCurrency, currency1, currency2):
        method = 'Mod. Following'
        ccy1 = bankingCurrency.Name()
        ccy2 = currency1.Name()
        ccy3 = currency2.Name()
        adjustedDate = bankingCurrency.Calendar().ModifyDate(currency1.Calendar(), currency2.Calendar(), date)
        return adjustedDate
    def getSpotDate(self, instrument, currency):
        currencyPair = instrument.CurrencyPair(currency)
        nearDate = self.DateToday()
        spotDate = currencyPair.SpotDate(nearDate)    
        return spotDate
    def getMarketBid(self, instrument, spotDate, currency):
        params = acm.FDictionary()
        params['priceDate'] = spotDate
        params['typeOfPrice'] = 'BestBidPrice'
        params['currency'] = currency
        foreign = instrument
        domestic = currency
        fxRate = acm.FX.CreateFxRate(foreign, domestic)
        spotPrice = fxRate.Calculation().MarketPriceParams(self.space, params).Value().Number()
        return spotPrice
    def getMarketAsk(self, instrument, spotDate, currency):
        params = acm.FDictionary()
        params['priceDate'] = spotDate
        params['typeOfPrice'] = 'BestAskPrice'
        params['currency'] = currency
        foreign = instrument
        domestic = currency
        fxRate = acm.FX.CreateFxRate(foreign, domestic)
        spotPrice = fxRate.Calculation().MarketPriceParams(self.space, params).Value().Number()
        return spotPrice
    def getSpotPrice(self, instrument, currency):
        today = self.DateToday()
        spotDate = self.getSpotDate(instrument, currency)
        foreign = instrument
        domestic = currency
        fxRate = acm.FX.CreateFxRate(foreign, domestic)
        spotPrice = fxRate.Calculation().MarketPrice(self.space, spotDate, True).Value().Number()
        return spotPrice
    def getForwardPrice(self, instrument, currency, forwardDate):
        spotPrice = self.getSpotPrice(instrument, currency)
        spotDate = self.getSpotDate(instrument, currency)
        if self.useFxBasisCurves:
            instrumentYieldCurve = self.getFxBasisCurve(instrument)
            currencyYieldCurve = self.getFxBasisCurve(currency)
            instrumentDiscountFactor = instrumentYieldCurve.Discount(spotDate, forwardDate)
            currencyDiscountFactor = currencyYieldCurve.Discount(spotDate, forwardDate)
            return spotPrice * (instrumentDiscountFactor / currencyDiscountFactor)  
        else:
            fxCurve = self.getFxCurve(instrument, currency)
            forwardDiscountFactor = fxCurve.Discount(spotDate, forwardDate)
            return spotPrice * forwardDiscountFactor
    # MDS only maintains spot rates against the USD!
    def getSpots(self, fx2, fx1):
        spots = {}
        if fx1 == fx2:
            pass
        elif 'USD' == fx1:
            spot1 = ('USD' ,fx2)
            spots[spot1] = spot1
        elif 'USD' == fx2:
            spot1 = (fx1, 'USD')
            spots[spot1] = spot1
        else:
            spot2 = ('USD' ,fx1)
            spots[spot2] = spot2
            spot3 = ('USD' ,fx2)
            spots[spot3] = spot3
        return spots.keys()
    def getOrCreateMarket(self, instrument, currency):
        marketContainer = None
        marketObj = None
        marketStruct = None
        logme('getOrCreateMarket...', 'DEBUG')
        market_id = self.getMarketId(instrument, currency)
        fx2 = instrument.Name()
        fx1 = currency.Name()
        snapshot_date = ''
        # Try to find the market; if that fails, create a new one.
        marketContainer = self.dtMDSBulkMediator.getMarketContainerForUpdate()
        marketFound = False
        for market in marketContainer:
            if market.marketObj.strFx1 == fx1 and market.marketObj.strFx2 == fx2:
                marketFound = True
                marketStruct = market
                logme('Market %s for %s/%s was found.' % (market.marketObj.strMrkt_id, market.marketObj.strFx2, market.marketObj.strFx1), 'DEBUG')
                break
        if not marketFound:
            logme('Market %s for %s/%s was not found; creating new market.' % (market.marketObj.strMrkt_id, market.marketObj.strFx2, market.marketObj.strFx1), 'DEBUG')
            currencyPair = instrument.CurrencyPair(currency)
            aPoint = 1.0 / currencyPair.PointValue()
            normDec = int(math.log10(aPoint))
            invDec = int(-1 * math.log10(currencyPair.PointValueInverse()))
            # def __init__(self, _strFx1, _strFx2, _strMrkt_id, _strMaster_id, _strGroup_name, _strMarketDescription, _dMinval, _dMaxval, _dSwapDiv, _lDecimalPos, _lInvDecimalPos, _lUniformMarketType):
            marketObj = DTMDS.MarketObj(fx1, fx2, market_id, '', '', '', 0.01, 1000000., aPoint, normDec, invDec, 6)
            logme('marketObj = %s' % (marketObj), 'DEBUG')
            marketStruct = DTMDS.MarketStruct(marketObj, fx2)
            logme('marketStruct = %s' % (marketStruct), 'DEBUG')
            marketContainer = self.dtMDSBulkMediator.createMarket(marketStruct)
            self.dtTransactionManager.commitTransaction()
        return marketContainer, marketStruct
    def getOrCreateVolatility(self, instrument, currency):
        spotRateObj = None
        marketObj = None
        snapshot_date = ''
        logme('getOrCreateVolatility...', 'DEBUG')
        fx2 = instrument.Name()
        fx1 = currency.Name()
        currencyPair = instrument.CurrencyPair(currency)
        marketContainer, marketStruct = self.getOrCreateMarket(instrument, currency)
        logme('marketStruct.strBaseCurrency:                %s' % marketStruct.strBaseCurrency,'DEBUG')
        logme('marketStruct.marketObj.dMaxval:              %f' % marketStruct.marketObj.dMaxval,'DEBUG')
        logme('marketStruct.marketObj.dMinval:              %f' % marketStruct.marketObj.dMinval,'DEBUG')
        logme('marketStruct.marketObj.dSwapDiv:             %f' % marketStruct.marketObj.dSwapDiv,'DEBUG')
        logme('marketStruct.marketObj.lDecimalPos:          %d' % marketStruct.marketObj.lDecimalPos,'DEBUG')
        logme('marketStruct.marketObj.lInvDecimalPos:       %d' % marketStruct.marketObj.lInvDecimalPos,'DEBUG')
        logme('marketStruct.marketObj.lUniformMarketType:   %d' % marketStruct.marketObj.lUniformMarketType,'DEBUG')
        logme('marketStruct.marketObj.strFx1:               %s' % marketStruct.marketObj.strFx1,'DEBUG')
        logme('marketStruct.marketObj.strFx2:               %s' % marketStruct.marketObj.strFx2,'DEBUG')
        logme('marketStruct.marketObj.strGroup_name:        %s' % marketStruct.marketObj.strGroup_name,'DEBUG')
        logme('marketStruct.marketObj.strMarketDescription: %s' % marketStruct.marketObj.strMarketDescription,'DEBUG')
        logme('marketStruct.marketObj.strMaster_id:         %s' % marketStruct.marketObj.strMaster_id,'DEBUG')
        logme('marketStruct.marketObj.strMrkt_id:           %s' % marketStruct.marketObj.strMrkt_id,'DEBUG')
        # Try to find the volatility surface; if that fails, create a new one.
        market_id = marketStruct.marketObj.strMrkt_id
        newlyCreated = None
        try:
            volatilityObj = self.dtMDSBulkMediator.getVolatilityObjForUpdate(self.mds_dataset,'', market_id)
            newlyCreated = False
        except:
            logme(traceback.format_exc(), 'ERROR')
            logme('Could not find volatility surface.', 'DEBUG')
            logme('Creating new object for %s/%s:' % (fx2, fx1), 'DEBUG')
            volatilityObj = self.dtMDSBulkMediator.createVolatilityObject(market_id, self.mds_dataset, snapshot_date)
            self.dtTransactionManager.commitTransaction()
            volatilityObj = self.dtMDSBulkMediator.getVolatilityObjForUpdate(self.mds_dataset,'', market_id)
            newlyCreated = True
        finally:
            try:
                self.dtMDSBulkMediator.unlockMarketContainer(marketContainer)
            except CORBA.SystemException:
                logme(traceback.format_exc(), 'ERROR')
                self.reconnectMDS()
            except:
                logme(traceback.format_exc(), 'ERROR')
        logme('volatilityObj = %s' % (volatilityObj), 'DEBUG')
        return (volatilityObj, newlyCreated)
    def getOrCreateSpots(self, instrument, currency):
        logme('getOrCreateSpot...', 'DEBUG')
        market_id = self.getMarketId(instrument, currency)
        snapshot_date = ''
        fx2 = instrument.Name()
        fx1 = currency.Name()
        spots = self.getSpots(fx2, fx1)
        spotRateObjs = []
        for spot in spots:
            fx12 = spot[1]
            fx11 = spot[0]
            try:
                spotRateObj = self.dtMDSBulkMediator.getSpotRateObjForUpdate(self.mds_dataset, snapshot_date, fx11, fx12)
            except:
                logme(traceback.format_exc(), 'ERROR')
                logme('Could not find spot rate object', 'DEBUG')
                logme('Creating new object for %s/%s:' % (fx12, fx11), 'DEBUG')
                spotRateObj = self.dtMDSBulkMediator.createSpotRate(fx11, fx12, self.mds_dataset, snapshot_date)
                self.dtTransactionManager.commitTransaction()
                spotRateObjs.append(spotRateObj)
            logme('spotRateObj: %s' % (spotRateObj), 'DEBUG')
        return spotRateObjs
    def getOrCreateDepositRate(self, currency):
        depositRateObj = None
        snapshot_date = ''
        fx = currency.Name()
        logme('getOrCreateDepositRate(%s)...' % (fx), 'DEBUG')
        try:
            depositRateObj = self.dtBulkMarketDataMediator.getDepoRateObjForUpdate(self.mds_dataset, '', fx)
        except:
            logme(traceback.format_exc(), 'ERROR')
            logme('Could not create deposit rate object.', 'DEBUG')
            logme('Creating new object for %s:' % (fx), 'DEBUG')
            depositRateObj = self.dtMDSBulkMediator.createDepositObject(fx, self.mds_dataset, snapshot_date)
            self.dtTransactionManager.commitTransaction()
        logme('depositRateObj = %s' % (depositRateObj), 'DEBUG')
        return depositRateObj
    # Use the real-time price, if it is available.
    def updateCurrencyPairSpotRate(self, instrument, currency, price=None):
        timer = FunctionTimer('updateCurrencyPairSpotRate')
        spotRateObj = None
        try:
            self.dtTransactionManager.startTransaction()
            spotRateObjs = self.getOrCreateSpots(instrument, currency)
            if spotRateObjs:
                for spotRateObj in spotRateObjs:
                    self.dtBulkMarketDataMediator.UnLockSpotRateObject(spotRateObj)
            fx2 = str(instrument.Name())
            fx1 = str(currency.Name())
            logme('UPDATING SPOT RATE FOR MARKET %s/%s...' % (fx2, fx1), 'INFO')
            currencyPair = instrument.CurrencyPair(currency)
            spotDate = currencyPair.SpotDate(self.DateToday())
            # MDS only maintains spot rates against the USD!
            # Therefore, whenever we receive an update
            # for a non-USD spot rate, e.g. CC1 per CC2,
            # we must query FA for spot rates for
            # USD-CC1 and USD-CC2, and update those in DT.
            spots = self.getSpots(fx2, fx1)
            for spot in spots:
                try:
                    fx12 = spot[0]
                    fx11 = spot[1]
                    instrument1 = acm.FCurrency[fx12]
                    currency1 = acm.FCurrency[fx11]
                    currencyPair = instrument1.CurrencyPair(currency1)
                    spotDate = currencyPair.SpotDate(self.DateToday())
                    spotRateObj = self.dtBulkMarketDataMediator.getSpotRateObjForUpdate(self.mds_dataset, '', fx11, fx12)
                    # ALSO!... DT may order pairs differently from FA, so....
                    logme('FA:       Currency: %s per Instrument: %s' % (currency1.Name(), instrument1.Name()), 'DEBUG')
                    logme('DT:       FX1:      %s per FX2:        %s' % (spotRateObj.Fx1, spotRateObj.Fx2),   'DEBUG')
                    if spotRateObj.Fx2 == str(instrument1.Name()):
                        logme('DT FX2 == instrument', 'DEBUG')
                        if spotRateObj.Fx1 == str(currency1.Name()) and price != None:
                            logme('Using FPrice for %s-%s...' % (instrument1.Name(), currency1.Name()), 'DEBUG')
                            spotRateObj.spotBid = 1.0 / price.Bid()
                            spotRateObj.spotAsk = 1.0 / price.Ask()
                            #fxRate = acm.FX.CreateFxRate(instrument1, currency1)
                            #spotRateObj.spotBid = fxRate.used_price()
                            #spotRateObj.spotAsk = fxRate.used_price()
                        else:
                            spotRateObj.spotBid = self.getMarketBid(instrument1, spotDate, currency1)         
                            spotRateObj.spotAsk = self.getMarketAsk(instrument1, spotDate, currency1)         
                    else:
                        logme('DT FX2 != instrument', 'DEBUG')
                        if spotRateObj.Fx1 == str(instrument1.Name()) and price != None:
                            logme('Using FPrice for %s-%s...' % (currency1.Name(), instrument1.Name()), 'DEBUG')
                            spotRateObj.spotBid = price.Bid()
                            spotRateObj.spotAsk = price.Ask()
                            #fxRate = acm.FX.CreateFxRate(currency1, instrument1)
                            #spotRateObj.spotBid = fxRate.used_price()
                            #spotRateObj.spotAsk = fxRate.used_price()
                        else:
                            spotRateObj.spotBid = self.getMarketBid(currency1, spotDate, instrument1)         
                            spotRateObj.spotAsk = self.getMarketAsk(currency1, spotDate, instrument1)         
                    self.dtBulkMarketDataMediator.SaveSpotRateObj(spotRateObj)
                    self.dtTransactionManager.commitTransaction()
                    logme('Updated:  FX1:      %s per FX2:        %s  Spot value date: %s  Spot: %8.4f  Bid: %8.4f  Ask: %8.4f' % (spotRateObj.Fx1, spotRateObj.Fx2, spotDate, (spotRateObj.spotBid + spotRateObj.spotAsk) / 2.0, spotRateObj.spotBid, spotRateObj.spotAsk), 'INFO')
                except:
                    logme(traceback.format_exc(), 'ERROR')
                finally:
                    try:
                        self.dtBulkMarketDataMediator.UnLockSpotRateObject(spotRateObj)
                    except CORBA.SystemException:
                        logme(traceback.format_exc(), 'ERROR')
                        self.reconnectMDS()
                    except:
                        logme(traceback.format_exc(), 'ERROR')
        except:
            try:
                self.dtTransactionManager.rollbackTransaction()
            except CORBA.SystemException:
                logme(traceback.format_exc(), 'ERROR')
                self.reconnectMDS()
            except:
                logme(traceback.format_exc(), 'ERROR')
        timer.stop()
    def updateDepositRateFromFIrCurveInformation(self, yieldCurve):
        timer = FunctionTimer('updateDepositRateFromFIrCurveInformation')
        logme('UPDATING DEPOSIT RATE FROM YIELD CURVE INFORMATION %s...' % (type(yieldCurve)), 'INFO')
        try:
            instrument = yieldCurve.BenchmarkInstruments()[0].Currency()
            currency = yieldCurve.Currency()
            currencyPair = instrument.CurrencyPair(currency)
            self.updateDepositRate(instrument, currencyPair)
        except:
            logme(traceback.format_exc(), 'ERROR')
            try:
                self.dtTransactionManager.rollbackTransaction()
            except:
                logme(traceback.format_exc(), 'ERROR')
        timer.stop()
    def updateDepositRateFromYieldCurve(self, yieldCurve):
        timer = FunctionTimer('updateDepositRateFromYieldCurve')
        logme('UPDATING DEPOSIT RATE FROM YIELD CURVE %s...' % (yieldCurve), 'INFO')
        try:
            instrument = yieldCurve.BenchmarkInstruments()[0].Currency()
            currency = yieldCurve.Currency()
            currencyPair = instrument.CurrencyPair(currency)
            self.updateDepositRate(instrument, currencyPair)
        except:
            logme(traceback.format_exc(), 'ERROR')
            try:
                self.dtTransactionManager.rollbackTransaction()
            except:
                logme(traceback.format_exc(), 'ERROR')
        timer.stop()
    def getInterestRateSpotDate(self, currency):
        if self.fxBaseCurrency.Name() == currency.Name():
            return self.fxBaseCurrency.SpotDate(self.DateToday())
        else:
            currencyPair = self.fxBaseCurrency.CurrencyPair(currency)
            return currencyPair.SpotDate(self.DateToday())
    def getInterestRateForwardDate(self, currency, tenor):
        if self.fxBaseCurrency.Name() == currency.Name():
            # Convert tenor to days.
            currencyCalendar = self.fxBaseCurrency.Calendar()
            forwardDate = acm.FDatePeriod.DefaultFormatter().Parse(tenor)
            days = acm.Time().DateDifference(forwardDate, self.DateToday())
            # IR forward date for base currency = base spot + days in tenor + calendar adjustment.
            spotDate = self.getInterestRateSpotDate(currency)
            forwardDate = acm.Time().DateAddDelta(spotDate, 0, 0, days)
            adjustedForwardDate = currencyCalendar.ModifyDate(currencyCalendar, currencyCalendar, forwardDate)
        else:
            currencyPair = self.fxBaseCurrency.CurrencyPair(currency)
            adjustedForwardDate = currencyPair.ForwardDate(self.DateToday(), tenor)
        return adjustedForwardDate
    def updateDepositRate(self, currency, currencyPair=None):
        timer = FunctionTimer('updateDepositRate')
        logme('UPDATING DEPOSIT RATE FOR %s...' % (currency.Name()), 'INFO')
        depoRateObj = None
        try:
            depoRateObj = self.getOrCreateDepositRate(currency)
            nearDate = self.getInterestRateSpotDate(currency)
            if currencyPair == None:
                currency1 = currency
                currency2 = currency
            else:
                currency1 = currencyPair.Currency1()
                currency2 = currencyPair.Currency2()
            forwardDatesForCurrencies = self.forwardDatesForCurrencies[currency]
            forwardDatesForCurrencies['spot'] = nearDate
            fx1 = currency2.Name()
            logme('depoRateObj:                      %s' % (depoRateObj), 'DEBUG')
            logme('Spot value date:                  %s' % (nearDate), 'DEBUG')
            logme('FX1:                              %s' % (fx1), 'DEBUG')
            if self.useFxBasisCurves:
                firCurveInformation = self.getFxBasisCurve(currency)
            else:
                firCurveInformation = self.getCurrencyCurve(currency)
            printouts = {}
            for depoRateForPeriod in depoRateObj.depoList:
                tenor = self.tenorForVolPeriod(depoRateForPeriod.depoPeriodCode)
                farDate = self.getInterestRateForwardDate(currency, tenor)
                forwardDatesForCurrencies[tenor] = farDate
                rate = firCurveInformation.Rate(nearDate, farDate, 'Simple', currency.Legs()[0].DayCountMethod(), 'Spot Rate', None, 0) * 100.0
                depoRateForPeriod.depoBid = rate
                depoRateForPeriod.depoAsk = rate
                depoRateForPeriod.depoInterpolated = False
                days = acm.Time().DateDifference(farDate, nearDate)
                printout = '%-7s  %s  %s Depo: %8.3f' % (tenor, farDate, currency.Name(), rate)
                printouts[days] = printout
            self.dtBulkMarketDataMediator.SaveDepoRateObj(depoRateObj)
            self.dtTransactionManager.commitTransaction()
            days = printouts.keys()
            days.sort()
            for day in days:
                logme(printouts[day], 'DEBUG')
        except:
            logme(traceback.format_exc(), 'ERROR')
            try:
                self.dtTransactionManager.rollbackTransaction()
            except:
                logme(traceback.format_exc(), 'ERROR')
        finally:
            try:
                self.dtBulkMarketDataMediator.UnLockDepositRateObject(depoRateObj)
            except CORBA.SystemException:
                logme(traceback.format_exc(), 'ERROR')
                self.reconnectMDS()
            except:
                logme(traceback.format_exc(), 'ERROR')
        timer.stop()
    # In OTC, the base, stronger, or reference currency is FX2.
    # A currency pair is defined as FX2 / FX1;
    # on the left side of OTC it is quoted as FX1 per FX2,
    # on the right side of OTC it is quoted as FX2 per FX1 points.
    # HOWEVER!!, in MDS, the key for the Market
    # (and thus for the volatility surface) is CCY_FX1FX2,
    # i.e. CURRENCYMARKET.UNIFORMMARKETID is CCY_FX1FX2,
    # CURRENCYMARKET.CURRENCY_CD_1 is FX2,
    # and CURRENCYMARKET.CURRENCY_CD_2 is FX1.
    # In FA, FX2 is "instrument", FX1 is "currency".
    # Throughout this code, FA "instrument" is DT FX2,
    # and FA "currency" is DT FX1.
    def getMarketId(self, instrument, currency):
        market_id = 'CCY_%s%s' % (currency.Name(), instrument.Name())
        return market_id
    # Return the date period structure for a given volatility period.
    def datePeriodForVolPeriod(self, volPeriod):
        tenor = string.split(self.tenorForVolPeriod(volPeriod))
        dateCode = tenor[1][0]
        n = int(tenor[0])
        datePeriod = None
        if   dateCode == 'D' and n == 1:
            datePeriod = DTDateCalcMediator.Period(DTDateCalcMediator.enOvernightPeriod, n)
        elif dateCode == 'D':
            datePeriod = DTDateCalcMediator.Period(DTDateCalcMediator.enDayPeriod, n)
        elif dateCode == 'W':
            datePeriod = DTDateCalcMediator.Period(DTDateCalcMediator.enWeekPeriod, n)
        elif dateCode == 'M':
            datePeriod = DTDateCalcMediator.Period(DTDateCalcMediator.enMonthPeriod, n)
        elif dateCode == 'Y':
            datePeriod = DTDateCalcMediator.Period(DTDateCalcMediator.enYearPeriod, n)
        return datePeriod
    # Return the calendar date for the given horizon date (e.g. today),
    # currency pair, and volatility period.
    def expiryForVolPeriod(self, date, fx1, fx2, volPeriod):
        try:
            ymd = acm.Time().DateToYMD(date)
            horizonDate = DTCOMMON.DateStructure(ymd[2], ymd[1], ymd[0])
            useRollover = False
            period = self.datePeriodForVolPeriod(volPeriod)
            periods = [period]
            expiries, deliveries = self.dtDateCalcMediator.calcOptionExpireAndDeliveryDate(fx1, fx2, horizonDate, useRollover, periods)
            expiry = expiries[0]
            return acm.Time().DateFromYMD(expiry.Year, expiry.Month, expiry.Day)
        except:
            logme(traceback.format_exc(), 'ERROR')
    def skewPeriodForTenor(self, tenor):
        parts = string.split(tenor)
        number = int(parts[0])
        type = parts[1]
        if   type == 'Day':
            return '%dd' % number
        elif type == 'Week':
           return '%dw' % number
        elif type == 'Month':
           return '%dm' % number
        elif type == 'Year':
           return '%dy' % number
        return None
    def getStrangleVolatility(self, atmVolatility, deltaPutVolatility, deltaCallVolatility):
        return ((deltaPutVolatility + deltaCallVolatility) / 2.0) - atmVolatility
    def getRiskReversalVolatility(self, deltaPutVolatility, deltaCallVolatility, favorsCall):
        if favorsCall == True:
           return deltaCallVolatility - deltaPutVolatility
        else:
           return deltaPutVolatility - deltaCallVolatility
    def skewPeriodToTenor(self, skewPeriod):
        period = skewPeriod[-1]
        number = skewPeriod[0:-1]
        if period == 'd':
            period = 'Day'
        if period == 'w':
            period = 'Week'
        if period == 'm':
            period = 'Month'
        if period == 'y':
            period = 'Year'
        tenor = '%s %s' % (number, period)
        logme('Skew period: %s  Tenor: %s' % (skewPeriod, tenor), 'DEBUG')
        return tenor
    def updateVolatilitySurface(self, volatilityStructure):
        timer = FunctionTimer('updateVolatilitySurface')
	#struct VolObj 
	#{ 
	#	VolatileObj vObj;
	#	string<10> uniformMarketID;	// For FX the format: CCY_Fx1Fx2
	#	string<3> Fx1;			// weaker asset(currency) in the pair
	#	string<3> Fx2;			// stronger asset(currency) in the pair
	#	long volDeltaTerm;		// skew delta term, the same as pricing [MKG: NOT the same as pricing! -- see below.]
	#	double volHolidayWeightFX1;
	#	double volHolidayWeightFX2;
	#	double volWeekendWeight;
	#	long volAtmVolInput;		// 0 = ZERO_DELTA_STRADDLE, 
        #                                       // 1 = AT_THE_FORWARD
	#	long volEntryMethodCode;	// 0 = STRANGLE_AND_RISK_REVERSAL_FX1_CALLS, 
        #                                       // 1 = STRANGLE_AND_RISK_REVERSAL_FX1_PUTS, 
        #                                       // 2 = OUTRIGHT_FX1_CALL_AND_PUTS,
	#	string volEntryMethodDesc;
	#	VolPeriodsList volList;
	#	long volATMVolInterpMethod;     // 0 = LINEAR_CALENDAR_DAY, 
        #                                       // 1 = TRADE_DAY_VARIANCE
	#};
	#typedef sequence<VolObj> VolObjList;
        logme('UPDATING VOLATILITY SURFACE FOR %s...' % (volatilityStructure.Name()), 'INFO')
        try:
            logme(volatilityStructure.Name(), 'DEBUG')
            underlyingMaturity = 0
            # Or false.
            isCall = True
            total = 0
            sqrtInterpol = 0
            strikeType = volatilityStructure.StrikeType()
            subscribedVolatilityStructure = acm.FVolatilityStructure[volatilityStructure.Name()]
            logme('type(%s): %s' % (subscribedVolatilityStructure.Name(), type(subscribedVolatilityStructure)), 'DEBUG')
            mappedValuationParameters = acm.GetFunction( 'mappedValuationParameters', 0 )
            gridMaturityEpsilon = mappedValuationParameters().Parameter().GridMinimumDays()
            volatilityInformation = subscribedVolatilityStructure.VolatilityInformation(self.DateToday(), gridMaturityEpsilon)
            faSkews = subscribedVolatilityStructure.Skews()
            forwardStartSkewTenorsForExpiries = {}
            # Set DerivaTech "Forward Start" based on Front Arena volatility periods.
            for faSkew in faSkews:
                if faSkew.DeltaType() == 'Forward':
                    forwardStartSkewTenorsForExpiries[faSkew.ActualExpiryDay()] = self.skewPeriodToTenor(str(faSkew.ExpiryPeriod()))
            nearestExpiry = None
            forwardStartTenor = None
            for k, v in forwardStartSkewTenorsForExpiries.items():
                if nearestExpiry == None:
                    nearestExpiry = k
                    forwardStartTenor = v
                if k < nearestExpiry:
                    nearestExpiry = k
                    forwardStartTenor = v
            logme('Forward start: %s' % forwardStartTenor, 'DEBUG')
            currency = self.currenciesForVolatilityStructures[volatilityStructure.Name()]
            if self.useFxBasisCurves:
                currencyYieldCurve = self.getFxBasisCurve(currency)
            else:
                currencyYieldCurve = self.getCurrencyCurve(currency)
            instrument = self.instrumentsForVolatilityStructures[volatilityStructure.Name()]
            if self.useFxBasisCurves:
                instrumentYieldCurve = self.getFxBasisCurve(instrument)
            else:
                instrumentYieldCurve = self.getCurrencyCurve(instrument)
            # Makes no difference to use the instrument or None for oid.
            # oid = instrument 
            oid = None
            market_id = self.getMarketId(instrument, currency)
            timer.stop('Pre getOrCreateVolatility')
            volatility, newlyCreated = self.getOrCreateVolatility(instrument, currency)
            timer.stop('Post getOrCreateVolatility')
            logme('Volatility structure:                    %s' % (subscribedVolatilityStructure), 'DEBUG')
            logme('Market ID:                               %s' % (market_id), 'DEBUG')
            logme('volatility:                              %s' % (volatility), 'DEBUG')
            logme('volatility.uniformMarketID:              %s' % (volatility.uniformMarketID), 'DEBUG')
            logme('volatility.Fx1:                          %s' % (volatility.Fx1), 'DEBUG')
            logme('volatility.Fx2:                          %s' % (volatility.Fx2), 'DEBUG')
            logme('FVolatilityStructure.DeltaTerm:          %s' % (subscribedVolatilityStructure.DeltaTerm()), 'DEBUG')
            logme('Newly created:                           %s' % (newlyCreated), 'DEBUG')
            # Case matters. 
            # From DTMDS (NOT the same as the trade terms enum!):
            # 0 %FX2
            # 1 FX2FX1
            # 2 %FX1
            # 3 FX1FX2
            if   subscribedVolatilityStructure.DeltaTerm() == 'Pct of foreign':
                volatility.volDeltaTerm = int(0)
            elif subscribedVolatilityStructure.DeltaTerm() == 'Domestic per foreign':
                volatility.volDeltaTerm = int(1)
            else:
                raise Exception('Cannot support FVolatilityStructure.DeltaTerm of %s.' % subscribedVolatilityStructure.DeltaTerm())
            logme('volatility.volDeltaTerm:                 %s' % (volatility.volDeltaTerm), 'DEBUG')
            volatility.volHolidayWeightFX1 = float(subscribedVolatilityStructure.DomesticHolidayWeight())
            logme('volatility.volHolidayWeightFX1:          %s' % (volatility.volHolidayWeightFX1), 'DEBUG')
            volatility.volHolidayWeightFX2 = float(subscribedVolatilityStructure.ForeignHolidayWeight())
            logme('volatility.volHolidayWeightFX2:          %s' % (volatility.volHolidayWeightFX2), 'DEBUG')
            volatility.volWeekendWeight = float(subscribedVolatilityStructure.ForeignWeekendWeight() * subscribedVolatilityStructure.DomesticWeekendWeight())
            logme('volatility.volWeekendWeight:             %s' % (volatility.volWeekendWeight), 'DEBUG')
            logme('FVolatilityStructure.DeltaAtmDefinition: %s' % (subscribedVolatilityStructure.DeltaAtmDefinition()), 'DEBUG')
            # Case matters.
            if   subscribedVolatilityStructure.DeltaAtmDefinition() == 'Zero Delta Straddle':
                volatility.volAtmVolInput = int(0) # // 0 = ZERO_DELTA_STRADDLE, 
            elif subscribedVolatilityStructure.DeltaAtmDefinition() == 'Forward':
                volatility.volAtmVolInput = int(1) # // 1 = AT_THE_FORWARD
            else:
                raise Exception('Cannot support FVolatilityStructure.DeltaAtmDefinition of %s.' % subscribedVolatilityStructure.DeltaAtmDefinition())
            logme('volatility.volAtmVolInput:               %s' % (volatility.volAtmVolInput), 'DEBUG')
            logme('FVolatilityStructure.FavorCall:          %s' % (subscribedVolatilityStructure.FavourCall()), 'DEBUG')
            favorCall = subscribedVolatilityStructure.FavourCall()
            if favorCall:
                volatility.volEntryMethodCode = int(1) # // 1 = STRANGLE_AND_RISK_REVERSAL_FX1_PUTS, 
            else:
                volatility.volEntryMethodCode = int(0) # // 0 = STRANGLE_AND_RISK_REVERSAL_FX1_CALLS, 
            logme('volatility.volEntryMethodCode:           %s' % (volatility.volEntryMethodCode), 'DEBUG')
            logme('volatility.volEntryMethodDesc:           %s' % (volatility.volEntryMethodDesc), 'DEBUG')
            logme('volatility.volATMVolInterpMethod:        %s' % (volatility.volATMVolInterpMethod), 'DEBUG')
            # In FA, puts have negative deltas, and calls have positive deltas.
            currencyPair = instrument.CurrencyPair(currency)
            nearDate = self.DateToday()
            spotDate = currencyPair.SpotDate(nearDate)
            # Currently, any spread added here affects ONLY at the money volatility.
            BidAskSpread = 0.0 # 0.5
            skewsForPeriods = {}
            farDatesForPeriods = {}
            timer.stop('Pre skew loop')
            for skew in volatility.volList:
                tenor = self.tenorForVolPeriod(skew.volPeriod)   
                #timer.stop('Pre expiryForVolPeriod')
                expiryDate = self.expiryForVolPeriod(nearDate, instrument.Name(), currency.Name(), skew.volPeriod)
                #timer.stop('Post expiryForVolPeriod')
                farDate = expiryDate
                #timer.stop('Pre get rates')
                instrumentRate = instrumentYieldCurve.Rate(spotDate, farDate) #Same as:, 'Continuous', 'Act/365', 'Spot Rate', None, 0)
                currencyRate = currencyYieldCurve.Rate(spotDate, farDate) #Same as:, 'Continuous', 'Act/365', 'Spot Rate', None, 0)
                #timer.stop('Post get rates')
                '''
                Now vanished:
                 FMalzParametricVolatilityInformation.Value(
                  date expiryDate,
                  double time_to_carry,
                  double strike,
                  double und_spot,
                  double foreign_rate,
                  double domestic_rate
                  ): double const
                Does this work?
                FVol.Value(
                  date underlyingMaturityDate,
                  date expiryDate,
                  double strike,
                  bool isCall,
                  FInstrument instrument,
                  double currentUnderlyingForwardQuote,
                  bool total,
                  bool sqrtInterpol,
                  bool underlyingIsGeneric,
                  array(double) skewForwards,
                  double foreignRepoRate,
                  double domesticRepoRate
                  ): double const
                '''                
                # Call is negative delta.
                # Rates should be continuous rates.
                #timer.stop('Pre skew calculation')
                volpDelta1  = volatilityInformation.Value(expiryDate, -0.01, instrumentRate, currencyRate)
                volpDelta10 = volatilityInformation.Value(expiryDate, -0.10, instrumentRate, currencyRate)
                volpDelta25 = volatilityInformation.Value(expiryDate, -0.25, instrumentRate, currencyRate)
                atm         = volatilityInformation.Value(expiryDate)
                volcDelta25 = volatilityInformation.Value(expiryDate,  0.25, instrumentRate, currencyRate)
                volcDelta10 = volatilityInformation.Value(expiryDate,  0.10, instrumentRate, currencyRate)
                volcDelta1  = volatilityInformation.Value(expiryDate,  0.01, instrumentRate, currencyRate)
                str25 = self.getStrangleVolatility(    atm,             volpDelta25, volcDelta25)
                str10 = self.getStrangleVolatility(    atm,             volpDelta10, volcDelta10)
                str1  = self.getStrangleVolatility(    atm,             volpDelta1,  volcDelta1)
                rr25  = self.getRiskReversalVolatility(volpDelta25,     volcDelta25, favorCall)
                rr10  = self.getRiskReversalVolatility(volpDelta10,     volcDelta10, favorCall)
                rr1   = self.getRiskReversalVolatility(volpDelta1,      volcDelta1,  favorCall)
                skew.volcDelta1Ask  = float(100.0 * str1)
                skew.volcDelta1Bid  = float(100.0 * str1)                  
                skew.volcDelta10Ask = float(100.0 * str10) 
                skew.volcDelta10Bid = float(100.0 * str10)
                skew.volcDelta25Ask = float(100.0 * str25) 
                skew.volcDelta25Bid = float(100.0 * str25) 
                skew.volAsk         = float(100.0 * atm   + BidAskSpread / 2.0)
                skew.volBid         = float(100.0 * atm   - BidAskSpread / 2.0)
                skew.volpDelta25Ask = float(100.0 * rr25)  
                skew.volpDelta25Bid = float(100.0 * rr25)  
                skew.volpDelta10Ask = float(100.0 * rr10)  
                skew.volpDelta10Bid = float(100.0 * rr10)  
                skew.volpDelta1Ask  = float(100.0 * rr1)   
                skew.volpDelta1Bid  = float(100.0 * rr1)   
                skewsForPeriods[skew.volPeriod] = skew
                farDatesForPeriods[skew.volPeriod] = farDate
                #timer.stop('Post skew calculation')
            timer.stop('Post skew loop')
            skews = skewsForPeriods.values()
            skews.sort(skewComparator)
            deltaInputFlag = 'S'
            newSkews = []
            for skew in skews:
                skew.DeltaInputFlag = deltaInputFlag
                newSkews.append(skew)
                if skew.volPeriod == forwardStartTenor:
                    transitionSkew = copy.deepcopy(skew)
                    deltaInputFlag = 'F'
                    transitionSkew.DeltaInputFlag = deltaInputFlag
                    newSkews.append(transitionSkew)
            newSkews.sort(skewComparator)
            volatility.volList = newSkews
            timer.stop('Pre skew print')
            for skew in volatility.volList:
                farDate = farDatesForPeriods[skew.volPeriod]
                day = int(acm.Time().DateDifference(farDate, nearDate))
                printout = '%-7s %s  %s/%s  Strangles  1d %7.2f  10d %7.2f  25d %7.2f  ATM: %7.2f  Riskys  25d %7.2f  10d %7.2f  1d %7.2f  %s  Days: %d' \
                            % (skew.volPeriod, skew.DeltaInputFlag, instrument.Name(), currency.Name(), skew.volcDelta1Ask, skew.volcDelta10Ask, skew.volcDelta25Ask, skew.volAsk, skew.volpDelta25Ask, skew.volpDelta10Ask, skew.volpDelta1Ask, farDate, day)
                logme(printout, 'INFO')
            timer.stop('Post skew print')
            timer.stop('Pre SaveVolatilityObj')
            self.dtMDSBulkMediator.SaveVolatilityObj(volatility)
            timer.stop('Post SaveVolatilityObj')
            self.dtTransactionManager.commitTransaction()
            logme('Saved volatility surface %s.' % (market_id), 'DEBUG')
        except:
            logme(traceback.format_exc(), 'ERROR')
            try:
                self.dtTransactionManager.rollbackTransaction()
            except:
                logme(traceback.format_exc(), 'ERROR')
        finally:
            try:
                self.dtMDSBulkMediator.UnLockVolatilityObject(volatility)
            except CORBA.SystemException:
                logme(traceback.format_exc(), 'ERROR')
                self.reconnectMDS()
            except:
                logme(traceback.format_exc(), 'ERROR')
        timer.stop()
    # TODO: Fix up for leap years.
    def daysForDayCountMethod(self, method):
        if   method == 'None':
            return 365
        elif method == 'Act/ActISDA':
            return 365
        elif method == 'Act/365':
            return 365
        elif method == 'Act/360':
            return 360
        elif method == '30E/360':
            return 360
        elif method == '30/360':
            return 360
        elif method == 'NL/365':
            return 365
        elif method == 'Act/ActAFB':
            return 365
        elif method == 'Act/ActISMA':
            return 365
        elif method == 'Act/364':
            return 364
        elif method == '30/360SIA':
            return 360
        elif method == '30E/365':
            return 365
        elif method == '30/365':
            return 365
        elif method == 'NL/360':
            return 360
        elif method == 'NL/ActISDA':
            return 365
        elif method == '30U/360':
            return 360
        elif method == '30/360GERMAN':
            return 360
        return 365
    def currencyObjToString(self, currencyObj):
	#struct CurrencyObj 
	#{ 
	#	string strCCY_cd;				// Currency SWIFT code (USD, JPY, ...)
	#	string strCCY_desc;				// Currency description. (Optional)
	#	DTCOMMON::ListOfStrings lstCCY_aliases;	// Currency(Asset) aliases (Optional)
	#	long lCCY_priority;				// Currency priority (weight)
	#	double dCCY_min;				// Min valid spot
	#	double dCCY_max;				// Max valid spot
	#	double dCCY_swapDiv;			// DT internal use
	#	long dCCY_decimal;				// DT internal use
	#	long dCCY_invDecimal;			// DT internal use
	#	double dCCY_refRate;			// DT internal use	
	#	string strCCY_legacyFlg;		// EMU legacy currency flag
	#	long lCCY_daysInYear;			
	#	double dCCY_conversionRate;		// DT internal use
	#};
        buffer = cStringIO.StringIO()
        buffer.write('strCCY_cd:           %s\n' % currencyObj.strCCY_cd)
        buffer.write('strCCY_desc:         %s\n' % currencyObj.strCCY_desc)
        for alias in currencyObj.lstCCY_aliases:
            buffer.write('  lstCCY_aliases:    %s\n' % alias)
        buffer.write('lCCY_priority:       %s\n' % currencyObj.lCCY_priority)
        buffer.write('dCCY_min:            %s\n' % currencyObj.dCCY_min)
        buffer.write('dCCY_max:            %s\n' % currencyObj.dCCY_max)
        buffer.write('dCCY_swapDiv:        %s\n' % currencyObj.dCCY_swapDiv)
        buffer.write('dCCY_decimal:        %s\n' % currencyObj.dCCY_decimal)
        buffer.write('dCCY_invDecimal:     %s\n' % currencyObj.dCCY_invDecimal)
        buffer.write('dCCY_refRate:        %s\n' % currencyObj.dCCY_refRate)
        buffer.write('strCCY_legacyFlg:    %s\n' % currencyObj.strCCY_legacyFlg)
        buffer.write('lCCY_daysInYear:     %s\n' % currencyObj.lCCY_daysInYear)
        buffer.write('dCCY_conversionRate: %s\n' % currencyObj.dCCY_conversionRate)
        text = buffer.getvalue()
        buffer.close()
        return text
    '''
    Update currency day count basis,
    precisions, and holiday lists.
    '''
    def updateCurrency(self, currency):
        timer = FunctionTimer('updateCurrency')
        currencyContainer = None
        currencyHolidaysObj = None
        currencyName = None
        currencyObj = None
        try:
            currencyName = str(currency.Name())
            # There appears to be a bug in DT that corrupts the MDS when the currency is updated in this way.
            # I have not been able to find any other way of updating the currency from the non-opaque CORBA
            # interface, either. The calendars, however, can be updated and that is the most important thing.
            
            #currencyObjContainer, holidays, markets = self.dtMDSBulkMediator.getStaticDataByMarket([currencyName], [currencyName], [])
            #currencyObjContainer = self.dtMDSBulkMediator.getCCYContainerForUpdate()
            #for currencyObj in currencyObjContainer:
            #    if currencyObj.strCCY_cd == currencyName:
            #        currencyObj.lCCY_daysInYear = int(self.daysForDayCountMethod(currency.Legs()[0].DayCountMethod()))
            #        currencyObj.dCCY_decimal = int(4)
            #        currencyObj.dCCY_invDecimal = int(4)
            #        self.dtTransactionManager.startTransaction()
            #        self.dtMDSBulkMediator.saveCCY(currencyObj)
            #        self.dtTransactionManager.commitTransaction()
            #        logme('Saved currency: \n%s' % self.currencyObjToString(currencyObj), 'DEBUG')
            #        break
            pass
        except CORBA.SystemException:
            logme(traceback.format_exc(), 'ERROR')
            self.reconnectMDS()
            return
        except DTDateCalcMediator.DTRemoteObjectException as e:
            logme('Failed to save currency: \n%s' % self.currencyObjToString(currencyObj), 'ERROR')
            logme('Exception: %s' % (e.message), 'ERROR')
            logme(traceback.format_exc(), 'ERROR')
            try:
                self.dtTransactionManager.rollbackTransaction()
            except:
                logme(traceback.format_exc(), 'ERROR')
                return
        except:
            logme(traceback.format_exc(), 'ERROR')
            return
        try:
            currencyHolidaysObj = self.dtMDSBulkMediator.getCCYHolidayContainerForUpdate(currencyName)
            calendar = currency.Legs()[0].PayCalendar()
            newHolidaysList = []
            for date in calendar.Dates():
                ymd = acm.Time().DateToYMD(date.Date())
                dateStructure = DTCOMMON.DateStructure(ymd[2], ymd[1], ymd[0])
                logme('%s holiday %4d-%2d-%2d' % (currencyName, dateStructure.Year, dateStructure.Month, dateStructure.Day), 'DEBUG')
                newHolidaysList.append(dateStructure)
            currencyHolidaysObj.holidaysLst = newHolidaysList
            self.dtMDSBulkMediator.saveCCYHolidayContainer(currencyHolidaysObj)
            self.dtTransactionManager.commitTransaction()
        except:
            try:
                self.dtTransactionManager.rollbackTransaction()
            except CORBA.SystemException:
                logme(traceback.format_exc(), 'ERROR')
                self.reconnectMDS()
            except:
                logme(traceback.format_exc(), 'ERROR')
        finally:
            try:
                self.dtMDSBulkMediator.UnLockCCYHolidayContainer(currencyHolidaysObj)
            except CORBA.SystemException:
                logme(traceback.format_exc(), 'ERROR')
                self.reconnectMDS()
            except:
                logme(traceback.format_exc(), 'ERROR')
        timer.stop()
    def getFxCurveSource(self, instrument, currency):
        # Instrument is 'foreign,' currency is 'domestic'.
        foreign = instrument
        domestic = currency
        fxRate = acm.FX.CreateFxRate(foreign, domestic)
        curveSource = fxRate.Calculation()
        curveSource = curveSource.MappedDiscountCurveSource(self.space)
        return curveSource
    def getFxCurve(self, instrument, currency):
        curveSource = self.getFxCurveSource(instrument, currency)
        curve = curveSource.Value()
        logme('FX curve for %s/%s: %s' % (instrument.Name(), currency.Name(), curve), 'DEBUG')
        return curve
    def getFxBasisCurveSource(self, currency):
        curveSource = None
        try:
            curveSource = None
            if True:
                curveSource = self.getFxCurveSource(self.fxBaseCurrency, currency)
            else:
                today = self.DateToday()
                if currency.Name() == self.fxBaseCurrency.Name():
                    curveSource = self.fxBaseCurrency.MappedDiscountLink().Link(today).YieldCurveComponent()  
                else:
                    curveSource = self.fxBaseCurrency.MappedDiscountLink(currency).Link(today).YieldCurveComponent()
        except:
            logme(traceback.format_exc(), 'ERROR')
        return curveSource        
    def getFxBasisCurve(self, currency):
        curveSource = self.getFxBasisCurveSource(currency)
        curve = curveSource.Value() #IrCurveInformation()
        return curve
    def getCurrencyCurveSource(self, currency):
        calculation = currency.Calculation()
        curveSource = calculation.MappedDiscountCurveSource(self.space)
        return curveSource
    def getCurrencyCurve(self, currency):
        curveSource = self.getCurrencyCurveSource(currency)
        curve = curveSource.Value()
        return curve
    def trackSubscribedObject(self, entity, subscribedObject):
        self.entitiesForSubscribedObjects[subscribedObject] = entity
        self.subscribedObjectsForEntities[entity] = subscribedObject
    '''
    Synchronize all data in MDS to reflect ACM.
    In the future, this will include importing all static data.
    For now, we assume that markets, currencies, and volatility surfaces
    already exist in MDS for each one in ACM, and we only update.
    the values in MDS from the ACM.
    
    Also, store the database entity object corresponding to each
    object for which we subscribe to update notifications. 
    '''
    def initialUpdate(self):
        timer = FunctionTimer('initialUpdate')
        try:
            today = self.DateToday()
            self.valuation_parameters = acm.UsedValuationParameters()
            self.localBankCurrency = self.valuation_parameters.AccountingCurrency().Name()
            self.fxBaseCurrency = self.valuation_parameters.FxBaseCurrency()
            if self.fxBaseCurrency == None:
                self.fxBaseCurrency = acm.FCurrency['USD']
            try:            
                self.valuation_parameters.FxBaseCurrency(self.fxBaseCurrency)
                self.valuation_parameters.Commit()
                logme('ACM FX base currency:      %s' % (self.valuation_parameters.FxBaseCurrency().Name()), 'INFO')
            except:
                traceback.print_exc()
            logme('FX base currency:          %s' % (self.fxBaseCurrency.Name()), 'INFO')
            if self.localBankCurrency:
                try:
                    logme('Local banking currency:    %s' % (self.localBankCurrency), 'INFO')
                    self.dtMDSBulkMediator.setLocalBankCurrency(self.localBankCurrency, self.localBankCurrency)
                except:
                    traceback.print_exc()
            updatedCurrencies = {}
            for currencyPair in self.currency_pairs:
                currencyPair = resolveObject(currencyPair, acm.FCurrencyPair)
                # We ASSUME that FA Currency1 is FA "instrument" and DT "FX2" --
                # but this does not have to be the case!
                # So by convention, Currency1 is FX2, and Currency2 is FX1.
                instrument = currencyPair.Currency1()
                if instrument not in updatedCurrencies:
                    updatedCurrencies[instrument] = instrument
                    self.trackSubscribedObject(instrument, instrument)
                self.forwardDatesForCurrencies[instrument] = {}
                currency = currencyPair.Currency2()
                if currency not in updatedCurrencies:
                    updatedCurrencies[currency] = currency
                    self.trackSubscribedObject(currency, currency)
                self.forwardDatesForCurrencies[currency] = {}
                logme('INITIAL UPDATE FOR CURRENCY PAIR %s...' % (currencyPair.Name()), 'INFO')
                logme('FX2 (instrument) currency: %s' % (instrument.Name()), 'INFO')
                logme('FX1 (currency)   currency: %s' % (currency.Name()), 'INFO')
                mappedFXVolatilityLink = instrument.MappedFXVolatilityLink(currency)
                logme('mappedFXVolatilityLink: %s %s' % (mappedFXVolatilityLink, type(mappedFXVolatilityLink)), 'DEBUG')
                link = mappedFXVolatilityLink.Link(self.DateToday())
                logme('link: %s %s' % (link, type(link)), 'DEBUG')
                volatilityStructure = link.VolatilityStructure()
                logme('volatilityStructure: %s' % (volatilityStructure), 'DEBUG')
                subscribedVolatilityStructure = acm.FVolatilityStructure[volatilityStructure.Name()]
                self.trackSubscribedObject(subscribedVolatilityStructure, subscribedVolatilityStructure)
                logme('Volatility surface:  %s' % (volatilityStructure.Name()), 'DEBUG')
                self.volatilityStructureWatchlist[subscribedVolatilityStructure] = volatilityStructure
                self.instrumentsForVolatilityStructures[str(volatilityStructure.Name())] = instrument
                self.currenciesForVolatilityStructures[str(volatilityStructure.Name())] = currency
                self.updateVolatilitySurface(volatilityStructure)
                key = '%s/%s' % (instrument.Name(), currency.Name())
                currencyPair = acm.FCurrencyPair[key]
                if currencyPair != None:
                    try:
                        self.updateCurrencyPairSpotRate(instrument, currency)
                        self.currencyPairWatchlist[currencyPair] = currencyPair
                        self.trackSubscribedObject(currencyPair, currencyPair)
                        for price in instrument.Prices():
                            try:
                                if price.Currency() != None and str(price.Currency().Name()) == str(currency.Name()):
                                    self.priceWatchlist[price] = price
                                    self.trackSubscribedObject(currencyPair, price)
                                    logme('Added price for %s/%s to watchlist.' % (instrument.Name(), currency.Name()), 'DEBUG')
                            except:
                                logme('Missing Front Arena price for %s.' % (key), 'WARNING')
                                logme(traceback.format_exc(), 'ERROR')
                    except:
                        logme(traceback.format_exc(), 'ERROR')
                self.updateDepositRate(instrument, currencyPair)
                self.currencyWatchlist[instrument] = instrument
                if self.useFxBasisCurves:
                    yieldCurve = self.getFxBasisCurveSource(instrument)
                    logme('FX basis curve for %s: %s' % (instrument.Name(), yieldCurve), 'DEBUG')
                else:
                    yieldCurve = instrument.MappedDiscountLink().Link(today).YieldCurveComponent()
                    logme('MappedDiscountLink for %s: %s' % (instrument.Name(), yieldCurve.Name()), 'DEBUG')
                if yieldCurve:
                    self.yieldCurveWatchlist[yieldCurve] = yieldCurve
                    self.trackSubscribedObject(instrument, yieldCurve)
                self.updateDepositRate(currency, currencyPair)
                self.currencyWatchlist[currency] = currency
                if self.useFxBasisCurves:
                    yieldCurve = self.getFxBasisCurveSource(currency)
                    # We do this for subscription, because we can't look up the database object from FIrCalculation objects.
                    #yieldCurve = currency.MappedDiscountLink().Link(today).YieldCurveComponent()
                    logme('FX basis curve for %s: %s' % (currency.Name(), yieldCurve), 'DEBUG')
                else:
                    yieldCurve = currency.MappedDiscountLink().Link(today).YieldCurveComponent()
                    logme('MappedDiscountLink for %s: %s' % (currency.Name(), yieldCurve.Name()), 'DEBUG')
                if yieldCurve:
                    self.yieldCurveWatchlist[yieldCurve] = yieldCurve
                    self.trackSubscribedObject(currency, yieldCurve)
                if not self.run_mode == 'Market data only':
                    self.updateCurrency(instrument)
                    self.updateCurrency(currency)
        except:
            logme(traceback.format_exc(), 'ERROR')
        timer.stop()
    def IdleCallback(self, **args):
        try:
            #logme('Idle callback: %s' % (args), 'DEBUG')
            pass
        except KeyboardInterrupt:
            shutdown()
        except:
            logme(traceback.format_exc(), 'ERROR')
    def ServerUpdate(self, sender, aspect, parameter):
        try:
            entity = None
            if sender != None:
                entity = self.entitiesForSubscribedObjects[sender]
            elif parameter != None:
                entity = self.entitiesForSubscribedObjects[parameter]
            logme('ServerUpdate: Sender: %s  Aspect: %s  Parameter: %s  Entity: %s' % (identify(sender), aspect, identify(parameter), identify(entity)),'INFO')
            if entity == None:
                logme("No entity in ServerUpdate()", "ERROR")
                return
            if True: # sometimes, aspect is not there! str(aspect) == 'update':
                entity = entity.Clone()
                if   str(entity.ClassName()) == 'FVolatilityStructure' or str(entity.ClassName()) == 'FMalzVolatilityStructure':
                    # These lookups and the entity mapping are required 
                    # because acm.FVol[entity.Name()] is not always valid.
                    instrument = self.instrumentsForVolatilityStructures[entity.Name()]
                    currency = self.currenciesForVolatilityStructures[entity.Name()]
                    logme('ServerUpdate: instrument: %s  currency: %s' % (instrument.Name(), currency.Name()), 'DEBUG')
                    # Now, uses mapping link, but FMalzVolatilityStructure also now does server update calls as it should.
                    mappedFXVolatilityLink = instrument.MappedFXVolatilityLink(currency)
                    logme('mappedFXVolatilityLink: %s %s' % (mappedFXVolatilityLink, type(mappedFXVolatilityLink)), 'DEBUG')
                    link = mappedFXVolatilityLink.Link(self.DateToday())
                    logme('link: %s %s' % (link, type(link)), 'DEBUG')
                    volatilityStructure = link.VolatilityStructure()
                    logme('ServerUpdate: volatilityStructure: %s' % (volatilityStructure), 'DEBUG')
                    volatilityStructure = entity # instrument.MappedVolatilityStructure(currency, self.DateToday()).Parameter()
                    logme('ServerUpdate: volatilityStructure: %s' % (volatilityStructure.Name()), 'DEBUG')
                    # self.updateVolatilitySurface(volatilityStructure)
                    self.updatesForVolatilitySurface.append(volatilityStructure)
                elif str(entity.ClassName()) == 'FCurrency':
                    # self.updateDepositRate(entity)
                    self.updatesForDepositRate.append(entity)
                elif str(entity.ClassName()) == 'FBenchmarkCurve':
                    # self.updateDepositRateFromYieldCurve(yieldCurve)
                    self.updatesForDepositRateFromYieldCurve.append(yieldCurve)
                elif str(entity.ClassName()) == 'FDeposit':
                    # self.updateDepositRateFromDeposit(deposit)
                    self.updatesForDepositRateFromDeposit.append(deposit)
                elif str(entity.ClassName()) == 'FPrice':
                    instrument = entity.Instrument()
                    currency = entity.Currency()
                    # self.updateCurrencyPairSpotRate(instrument, currency)
                    self.updatesForCurrencyPairSpotRate.append((instrument, currency))
                elif str(entity.ClassName()) == 'FCurrencyPair' and str(sender.ClassName()) == 'FPrice':
                    instrument = sender.Instrument()
                    currency = sender.Currency()
                    price = sender
                    # self.updateCurrencyPairSpotRate(instrument, currency, price)
                    self.updatesForCurrencyPairSpotRate.append((instrument, currency, price))
        except:
            logme(traceback.format_exc(), 'ERROR')
    def unsubscribeForUpdates(self):
        try:
            if not (__name__ == '__main__' or server.objectServer == "'FACMServer'"):
                logme('No realtime updates unless running in server mode.', 'WARNING')
                return
            logme('UNSUBSCRIBING FOR UPDATES...', 'INFO')
            for subscribedObject, entity in self.entitiesForSubscribedObjects.items():
                try:
                    subscribedObject.RemoveDependent(self)
                    subscribedIdentity = identify(subscribedObject)
                    entityIdentity = identify(entity)
                    if subscribedIdentity == entityIdentity:
                        logme('%s.' % (subscribedIdentity), 'INFO')
                    else:
                        logme('%s (from %s).' % (entityIdentity, subscribedIdentity), 'INFO')
                except:
                    traceback.print_exc()
        except:
            logme(traceback.format_exc(), 'ERROR')
    def subscribeForUpdates(self):
        try:
            if not (__name__ == '__main__' or server.objectServer == "'FACMServer'"):
                logme('No realtime updates unless running in server mode.', 'WARNING')
                return
            logme('SUBSCRIBING FOR UPDATES...', 'INFO')
            subscriptions = {}
            for subscribedObject, entity in self.entitiesForSubscribedObjects.items():
                try:
                    # Avoid redundant subscriptions.
                    subscribedIdentity = identify(subscribedObject)
                    if subscribedIdentity not in subscriptions:
                        subscriptions[subscribedIdentity] = subscribedObject
                        subscribedObject.AddDependent(self)
                        entityIdentity = identify(entity)
                        if subscribedIdentity == entityIdentity:
                            logme('%s.' % (subscribedIdentity), 'INFO')
                        else:
                            logme('%s (from %s).' % (subscribedIdentity, entityIdentity), 'INFO')
                except:
                    traceback.print_exc()
        except:
            logme(traceback.format_exc(), 'ERROR')
    def report(self):
        try:
            logme('FAOTCMarketServer PARAMETERS', 'INFO')
            for parameter, value in self.parameters.items():
                logme('Parameter:   %s = %s' % (parameter, value), 'DEBUG')
        except:
            logme(traceback.format_exc(), 'ERROR')
    def shutdown(self):
        try:
            logme('SHUTTING DOWN...', 'INFO')
            self.keepRunning = False
            try:
                self.unsubscribeForUpdates()
            except:
                logme(traceback.format_exc(), 'ERROR')
            try:
                self.disconnectMDS()
            except:
                logme(traceback.format_exc(), 'ERROR')
            try:
                self.disconnectACM()
            except:
                logme(traceback.format_exc(), 'ERROR')
        except:
            logme(traceback.format_exc(), 'ERROR')
        threading.Timer(2.0, lambda: os._exit(0)).start()
    def run(self):
        try:
            self.keepRunning = True
            while self.keepRunning:
                while len(self.updatesForCurrencyPairSpotRate) > 0:
                    args = self.updatesForCurrencyPairSpotRate.pop()
                    if len(args) == 3:
                        self.updateCurrencyPairSpotRate(args[0], args[1], args[2])
                    if len(args) == 2:
                        self.updateCurrencyPairSpotRate(args[0], args[1])
                while len(self.updatesForDepositRateFromDeposit) > 0:
                    args = self.updatesForDepositRateFromDeposit.pop()
                    self.updateDepositRateFromDeposit(args)
                while len(self.updatesForDepositRateFromYieldCurve) > 0:
                    args = self.updatesForDepositRateFromYieldCurve.pop()
                    self.updateDepositRateFromYieldCurve(args)
                while len(self.updatesForVolatilitySurface) > 0:
                    args = self.updatesForVolatilitySurface.pop()
                    self.updateVolatilitySurface(args)
                while len(self.updatesForDepositRate) > 0:
                    args = self.updatesForDepositRate.pop()
                    self.updateDepositRate(args)
                acm.PollDbEvents(100)
                self.IdleCallback()
        except:
            logme(traceback.format_exc(), 'ERROR')
            

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

def signalHandler(signum, frame):
    try:
        global server
        logme('Received signal %s' % (signum), 'WARNING')
        server.shutdown()
    except:
        logme(traceback.format_exc(), 'ERROR')
        
# Run in a separate thread to listen for commands on the server control port,
# e.g. from Prime.
class RemoteController(SimpleXMLRPCServer.SimpleXMLRPCServer, threading.Thread):
    def __init__(self, faOTCMarketServer):
        SimpleXMLRPCServer.SimpleXMLRPCServer.__init__(self, ('localhost', faOTCMarketServer.ms_controller_port))
        threading.Thread.__init__(self)
        self.faOTCMarketServer = faOTCMarketServer
        self.register_function(self.report)
        self.register_function(self.shutdown)
        self.keepRunning = True
    def report(self):
        self.faOTCMarketServer.report()
        return 1
    def shutdown(self):
        self.faOTCMarketServer.shutdown()
        return 1
    def run(self):
        self.keepRunning = True
        try:
            while self.keepRunning:
                self.handle_request()
        except:
            logme(traceback.format_exc(), 'ERROR')
            
def ael_main(parameters):
    global server
    global space
    try:
        ScriptName = 'FAOTCMarketServer'
        LogMode = int(parameters['logmode'])
        LogToConsole = int(parameters['log_to_console'])
        LogToFile = int(parameters['log_to_file'])
        Logfile = parameters.get('ms_logfile')
        SendReportByMail = False
        MailList = []
        ReportMessageType = None
        logme.setLogmeVar(ScriptName, LogMode, LogToConsole, LogToFile, Logfile, SendReportByMail, MailList, ReportMessageType)
        parameters['today_date'] = acm.Time().DateNow()
        if LogMode > 1:
            for parameter, value in parameters.items():
                logme('Parameter:   %s = %s' % (parameter, value), 'DEBUG')        
        server = FAOTCMarketServer(parameters)
        server.connectMDS()
        if __name__ == '__main__':
            server.connectACM()
        server.createCalculationSpace()
        server.initialUpdate()
        if server.run_mode == 'Static data only':
            server.shutdown()
            return
        if (__name__ == '__main__') or (server.objectServer == "'FACMServer'"):
            try:
                server.subscribeForUpdates()
                atexit.register(server.shutdown)
                signal.signal(signal.SIGBREAK, signalHandler)
                signal.signal(signal.SIGSEGV, signalHandler)
                signal.signal(signal.SIGTERM, signalHandler)
                signal.signal(signal.SIGABRT, signalHandler)
                signal.signal(signal.SIGINT, signalHandler)
                logme('RUNNING...', 'INFO')
                controller = RemoteController(server)
                controller.start()
                server.run()
            except:
                logme(traceback.format_exc(), 'ERROR')
        else:
            logme('This script must be run as an ATS task in order to send real-time changes to MDS.', 'WARNING')
            time.sleep(10)
    except:
        traceback.print_exc()
        logme(traceback.format_exc(), 'ERROR')
   
if __name__ == '__main__':
    ael_main(defaultParameters)
