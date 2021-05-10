""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/bdp_benchmark_test/./etc/FBDPBenchmarkTest_Perform.py"
"""----------------------------------------------------------------------------
MODULE
    FBDPBenchmarkTest_Perform - Module which performs BDPBenchmarkTest.

    Requirements:
    
    BDP benchmark test creates instruments, prices, counterparties,
    acquirers, and trades measure the time taken. It also can clone
    the existing trades and measure performance. All the test data
    can be cleaned after the tests complete.

DESCRIPTION
    This module performs the BDP benchmark test based on the
    parameters passed from the script FBDPBenchmarkTest.

----------------------------------------------------------------------------"""

import sys
import random
import time
from contextlib import contextmanager
import acm
import ael
import FBDPCommon
from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme

INSTRUMENT_NAME_PREFIX = 'BDPBenchmark_INS_'
STOCK_NAME_PREFIX = 'BDPBenchmark_INS_STOCK_'
PORTFOLIO_NAME_PREFIX = 'BDPBenchmarkPort_'
COUNTERPARTY_NAME_PREFIX = 'BDPBenchmarkCP_'
ACQUIRER_NAME_PREFIX = 'BDPBenchmarkACQ_'
NUMBER_OF_PORTFOLIOS = 4
NUMBER_OF_COUNTERPARTIES = 10
NUMBER_OF_ACQUIRERS = 10
PRICEMARKET = 'SPOT'


def perform_test(execParam):
    e = BenchmarkTest(execParam)
    e.perform()
    Summary().log(execParam)
    Logme()(None, 'FINISH')


def getChangeFactor(minFact=0.8, maxFact=1.25):
    return round(float(random.uniform(minFact, maxFact)), 2)


def createCounterParty(name, *argv):
    cpty = acm.FCounterParty()
    cpty.Name(name)
    cpty.Commit()
    Summary().ok(cpty, Summary().CREATE, cpty.Oid())
    return cpty


def createPhysicalPortfolio(name, *argv):
    prf = acm.FPhysicalPortfolio()
    prf.Name(name)
    prf.AssignInfo(name)
    prf.Currency(acm.FCurrency['EUR'])
    prf.Commit()
    Summary().ok(prf, Summary().CREATE, prf.Oid())
    return prf


def createInternalDepartment(name, *argv):
    acq = acm.FInternalDepartment()
    acq.Name(name)
    acq.Commit()
    Summary().ok(acq, Summary().CREATE, acq.Oid())
    return acq


def getEntities(namePrefix, entityName):
    return acm.GetClass('F' + entityName).Select(
                'name like %s' % (namePrefix + '*'))


def getEntityNames(namePrefix, entityName):
    return [e.Name() for e in
                getEntities(namePrefix, entityName)]
    

def getEntityStartIndex(namePrefix, entityName):
    return getEntities(namePrefix, entityName).Size()


def createEntities(namePrefix, entityName, numberOfEntities, *argv):
    eList = []
    startIndex = getEntityStartIndex(namePrefix, entityName)
    for i in range(numberOfEntities):
        uName = namePrefix + str(i + 1 + startIndex)
        cpty = getattr(sys.modules[__name__],
                        "create%s" % entityName)(uName, argv)
        eList.append(cpty)
    return eList


def DeleteEntities(namePrefix, entityName):
    for name in getEntityNames(namePrefix, entityName):
        Logme()(name, "DEBUG")
        Summary().ok(acm.GetClass('F' + entityName)[name], Summary().DELETE, name)
        acm.GetClass('F' + entityName)[name].Delete()


def getRandomDate(lastDate, firstDate):
    days = acm.Time.DateDifference(lastDate, firstDate)
    if days < 0:
        raise RuntimeError('lastDate has to larger than firstDate')
    offset = random.randint(0, days)
    return acm.Time.DateAddDelta(firstDate, 0, 0, offset)


@contextmanager  
def measureTime(title):
    t1 = time.clock()
    yield
    t2 = time.clock()
    Logme()('%s: %0.2f seconds elapsed' % (title, t2 - t1))

class BenchmarkTest(object):
    
    def createInstruments(self):
        instruments = []
        self.startIndex = getEntityStartIndex(STOCK_NAME_PREFIX, 'Instrument')

        for i in range(self.numberOfInstruments):
            insName = STOCK_NAME_PREFIX\
                    + str(i + 1 + self.startIndex)
            ins = Stock(insName)
            instruments.append(ins)
        return instruments

    def readArguments(self, execParam):
        self.lastTradeDate = FBDPCommon.toDate(
                    execParam.get('lastTradeDate', 'Today'))
        self.firstTradeDate = FBDPCommon.toDate(
                    execParam.get('firstTradeDate', '-6m'))

        self.numberOfInstruments = execParam.get('numberOfInstruments', 1)
        self.numberOfTradesPerIns = execParam.get('numberOfTradesPerIns', 1000)        
        self.clone = execParam.get('simulate', 0)
        self.createNew = execParam.get('createNew', 0)
        self.cleanUp = execParam.get('cleanUp', 0)
        self.simulateIns = execParam.get('Instruments', None)
        self.prfs = execParam.get('TradingPortfolios', None)
        self.numberOfClone = execParam.get('numberOfCloneTrades', 10)
        
    
    def __init__(self, execParam):
        self.readArguments(execParam)

    def doCleanUp(self):

        for p in getEntities(PORTFOLIO_NAME_PREFIX, 'PhysicalPortfolio'):
            tOids = [t.Oid() for t in p.Trades()]
            for oid in tOids:
                Logme()(oid, "DEBUG")
                Summary().ok(acm.FTrade[oid], Summary().DELETE, oid)
                acm.FTrade[oid].Delete()

        DeleteEntities(PORTFOLIO_NAME_PREFIX, 'PhysicalPortfolio')
        DeleteEntities(COUNTERPARTY_NAME_PREFIX, 'CounterParty')
        DeleteEntities(ACQUIRER_NAME_PREFIX, 'InternalDepartment')

        names = getEntityNames(INSTRUMENT_NAME_PREFIX, 'Instrument')
        for n in names:
            Logme()(n, "DEBUG")
            query = ('instrument={0} and currency={1}'.format(
                acm.FInstrument[n].Oid(), acm.FInstrument[n].Currency().Oid()))
            prices = acm.FPrice.Select(query)
            pOids = [p.Oid() for p in prices]
            for p in pOids:
                Logme()(p, "DEBUG")
                Summary().ok(acm.FPrice[p], Summary().DELETE, p)
                acm.FPrice[p].Delete()
            Summary().ok(acm.FInstrument[n], Summary().DELETE, n)
            acm.FInstrument[n].Delete()
        

    def perform(self):
        if self.cleanUp:
            Logme()('Clean up test data.....', "DEBUG")
            self.doCleanUp()
        elif self.createNew:
            Logme()('Create new data.....', "DEBUG")
            with measureTime('Portfolios creation time'):
                self.portfolioNames = createEntities(
                        PORTFOLIO_NAME_PREFIX, 'PhysicalPortfolio', NUMBER_OF_PORTFOLIOS)
            with measureTime('Counterparties creation time'):
                self.counterparties = createEntities(
                        COUNTERPARTY_NAME_PREFIX, 'CounterParty', NUMBER_OF_COUNTERPARTIES)
            with measureTime('Acquirers creation time'):
                self.acquirers = createEntities(
                        ACQUIRER_NAME_PREFIX, 'InternalDepartment', NUMBER_OF_ACQUIRERS)
            
            with measureTime('Instruments creation time'):
                self.instruments = self.createInstruments()                    

            with measureTime('Prices creation time'):
                for ins in self.instruments:
                    ins.createPrice(self.lastTradeDate)
            with measureTime('Trades creation time'):
                for ins in self.instruments:
                    ins.createTrades(self.numberOfTradesPerIns,
                            self.lastTradeDate, self.firstTradeDate,
                            self.portfolioNames, self.counterparties,
                            self.acquirers)
        elif self.clone:
            Logme()('Cloning existing data.....', "DEBUG")
            
            with measureTime('Instruments clone time'):
                for ins in self.simulateIns:
                    insClone = ins.Clone()
                    insClone.Name(INSTRUMENT_NAME_PREFIX + ins.Name())
                    insClone.Commit()
            with measureTime('Trades clone time'):
                for ins in self.simulateIns:
                    count = 0
                    for t in ins.Trades():
                        tc = t.Clone()
                        tc.Instrument(acm.FInstrument[
                            INSTRUMENT_NAME_PREFIX + ins.Name()])
                        tc.Status('Simulated')
                        tc.Commit()
                        tc.ConnectedTrade(tc)
                        tc.Commit()
                        count = count + 1
                        if count >= self.numberOfClone:
                            break


class InstrumentBase(object):
    def __init__(self, ins_name):
        self.ins.Name(ins_name)
        
    def createPrice(self, price_date, price, price_market=PRICEMARKET):
        ael_date = ael.date(price_date)
        
        ael_market = ael.Party[price_market]
        ael_ins = ael.Instrument[self.ins.Name()]
        try:
            newPrice = ael.Price.new()
            newPrice.insaddr = ael_ins
            newPrice.curr = ael_ins.curr
            newPrice.day = ael_date
            newPrice.ptynbr = ael_market
            newPrice.bid = price
            newPrice.ask = price
            newPrice.last = price
            newPrice.settle = price
            newPrice.commit()
            Summary().ok(newPrice, Summary().CREATE, newPrice.prinbr)
            return price

        except Exception as msg:
            if (ael_date == ael.date_today()) and (ael_market.type == 'Market'):
                for p in ael_ins.prices():
                    if (ael_market == p.ptynbr):
                        thePrice = p
                        break
            else:
                for p in ael_ins.historical_prices():
                    if (ael_date == p.day) and (ael_market == p.ptynbr):
                        thePrice = p
                        break
            updPrice = thePrice.clone()
            updPrice.day = ael_date
            updPrice.bid = price
            updPrice.ask = price
            updPrice.last = price
            updPrice.settle = price
            updPrice.commit()
            return price


class Stock(InstrumentBase):
    def __init__(self, ins_name):
        self.ins = acm.FStock()
        super(Stock, self).__init__(ins_name)
        self.ins.Commit()
        Summary().ok(self.ins, Summary().CREATE, self.ins.Oid())

    def createPrice(self, price_date, price=None):
        if not price:
            price = 100 * getChangeFactor()
        else:
            price = float(price)
        return super(Stock, self).createPrice(price_date, price)
    
    def createTrades(self, numberOfTrades, lastDate, firstDate,
                    portfolioList, cpList, acList):

        numberOfPortfolios = len(portfolioList)
        numberOfCP = len(cpList)
        numberOfAcq = len(acList)
        for i in range(numberOfTrades):
            acm.BeginTransaction()
            trd=acm.FTrade()
            trd.Currency(self.ins.Currency())
            trd_time = getRandomDate(lastDate, firstDate)
            trd.TradeTime(trd_time)
            val_day = FBDPCommon.businessDaySpot(self.ins, trd_time)
            trd.ValueDay(val_day)
            trd.AcquireDay(val_day)
            trd.Quantity(100)
            price = 100 * getChangeFactor()
            trd.Price(price)
            trd.Portfolio(portfolioList[random.randint(0, numberOfPortfolios - 1)])
            trd.Counterparty(cpList[random.randint(0, numberOfCP - 1)])
            trd.Acquirer(acList[random.randint(0, numberOfAcq - 1)])
            trd.Instrument(self.ins)
            trd.UpdatePremium(True)
            trd.Status('Simulated')
            trd.Commit()
            Summary().ok(trd, Summary().CREATE, trd.Oid())
            acm.CommitTransaction()

