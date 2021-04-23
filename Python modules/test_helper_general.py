"""-----------------------------------------------------------------------------
PROJECT                 :  N/A
PURPOSE                 :  General unit test helper classes
DEPATMENT AND DESK      :  N/A
REQUESTER               :  N/A
DEVELOPER               :  Francois Truter
CR NUMBER               :  526074
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
-----------------------------------------------------------------------------
2010-11-16 494829    Francois Truter    Initial implementation
2010-12-17 526074    Francois Truter    Updated
2011-04-04 619099    Francois Truter    Added AssertRaises
"""

import acm
import uuid
import unittest
import math
import os
import csv
import decimal
import ael
import test_helper_instruments

def _toDecimal(value):
    if not isinstance(value, decimal.Decimal):
            value = decimal.Decimal(str(value))
    return value

def _startsWith(stringToSearch, stringToLookFor):
    if stringToSearch.find(stringToLookFor) == 0:
        return True
    else:
        return False
        
class PriceHelper:

    @staticmethod
    def AssertPrice(testCase, expected, actual, message):
        testCase.assertEqual(expected, actual, message + ' Expected %(expected)s, got %(actual)s' % {'expected': expected, 'actual': actual})
        
    @staticmethod
    def AssertMarketPrices(testCase, instrument, market, expectedPrices, message):
        actualPrices = PriceHelper.GetMarketPrices(instrument, market)
        expectedLen = len(expectedPrices)
        actualLen =len(actualPrices)
        testCase.assertEqual(expectedLen, actualLen, message + ' Number of prices not as expected. Expected %(expected)i, got %(actual)i' % {'expected': expectedLen, 'actual': actualLen})
        for tuple in expectedPrices:
            date = tuple[0]
            value = tuple[1]
            for price in actualPrices:
                if price.Day() == date and \
                    price.Ask() == value and \
                    price.Bid() == value and \
                    price.High() == value and \
                    price.Last() == value and \
                    price.Low() == value and \
                    price.Open() == value and \
                    price.Settle() == value:
                    actualPrices.remove(price)
                    break
            else:
                testCase.fail(message + 'Could not find price: %(date)s, %(price)s' % {'date': date, 'price': value})
        
    @staticmethod
    def GetMarketPrices(instrument, market):
        prices = []
        for price in instrument.Prices():
            if price.Market() == market:
                prices.append(price)
        for price in instrument.HistoricalPrices():
            if price.Market() == market:
                prices.append(price) 
                
        return prices
        
    @staticmethod
    def GetAllMarketPrices(market):
        query = acm.CreateFASQLQuery('FPrice', 'AND')
    
        op = query.AddOpNode('AND')
        op.AddAttrNode('Market.Name', 'EQUAL', market.Name())
                
        return query.Select()
    
    @staticmethod
    def CreatePrice(instrument, price=1, date=acm.Time().DateNow(), market=acm.FParty['SPOT']):
        fprice = acm.FPrice()
        fprice.Instrument(instrument)
        fprice.Ask(price)
        fprice.Bid(price)
        fprice.Currency(instrument.Currency())
        fprice.Day(date)
        fprice.High(price)
        fprice.Last(price)
        fprice.Low(price)
        fprice.Market(market)
        fprice.Open(price)
        fprice.Settle(price)
        fprice.Commit()
        
    @staticmethod
    def DeletePrice(price):
        price.Delete()

class PartyHelper:
    
    @staticmethod
    def AssertParty(testCase, expected, actual, message):
        testCase.assertEqual(expected, actual, message + ' Expected %(expected)s, got %(actual)s' % {'expected': expected.Name(), 'actual': actual.Name()})

    @staticmethod
    def CreatePersistantCounterparty():
        party = acm.FCounterParty()
        party.Name(str(uuid.uuid4()))
        party.Commit()
        party.AdditionalInfo().FICA_Compliant(True)
        return party

    @staticmethod
    def CreatePersistantClient():
        party = acm.FClient()
        party.Name(str(uuid.uuid4()))
        party.Commit()
        party.AdditionalInfo().FICA_Compliant(True)
        return party
        
    @staticmethod    
    def CreatePersistantInternalDepartment():
        party = acm.FInternalDepartment()
        party.Name(str(uuid.uuid4()))
        party.Commit()
        party.AdditionalInfo().FICA_Compliant(True)
        return party
        
    @staticmethod
    def GetPersistantMarketPlace():
        party = acm.FMarketPlace()
        party.Name(str(uuid.uuid4()))
        party.Commit()
        return party
        
    @staticmethod
    def GetPersistantFMTMMarket():
        party = acm.FMTMMarket()
        party.Name(str(uuid.uuid4()))
        party.Commit()
        return party
        
    @staticmethod
    def GetPartyNameNotExists():
        name = str(uuid.uuid4())
        while True:
            party = acm.FParty[name]
            if not party:
                break
            name = str(uuid.uuid4())
        return name
        
    @staticmethod
    def DeleteParty(party):
        prices = PriceHelper.GetAllMarketPrices(party)
        for price in prices:
            PriceHelper.DeletePrice(price)
        
        party.Delete()
        
class PortfolioHelper:
    
    @staticmethod
    def CreateTemporaryPortfolio():
        portfolio = acm.FPhysicalPortfolio()
        portfolio.Name(str(uuid.uuid4()))
        return portfolio
        
    @staticmethod
    def CreatePersistantPortfolio(owner = None):
        portfolio = acm.FPhysicalPortfolio()
        name = str(uuid.uuid4())
        portfolio.Name(name)
        portfolio.AssignInfo(name)
        portfolio.Currency(acm.FCurrency['ZAR'])
        if owner != None:
            portfolio.PortfolioOwner(owner)
        portfolio.Commit()
        return portfolio
        
    @staticmethod
    def CreatePersistantSweepingPortfolio(owner, desk, type = None):
        acm.BeginTransaction()
        try:
            portfolio = PortfolioHelper.CreatePersistantPortfolio(owner)
            portfolio.AdditionalInfo().SL_AllocatedDesk(desk)
            portfolio.AdditionalInfo().SL_Sweeping('Yes')
            if type:
                portfolio.AdditionalInfo().SL_Portfolio_Type(type)
            
            acm.CommitTransaction()
            return portfolio
        except Exception, ex:
            acm.AbortTransaction()
            raise ex
        
    @staticmethod
    def GetTradingDesk():
        deskName = str(uuid.uuid4())
        choiceList = acm.FChoiceList.Select("list = 'AllocatedDesk'")
        for choice in choiceList:
            if choice.Name() == deskName:
                return deskName
        
        choice = acm.FChoiceList()
        choice.List('AllocatedDesk')
        choice.Name(deskName)
        choice.Commit()
        return deskName
        
class TradeFilterHelper:
    counter = 1
    
    @staticmethod
    def CreateTradeFilter(portfolios):
        query = []
        condition = ''
        for portfolio in portfolios:
            query.append((condition, '', 'Portfolio', 'equal to', portfolio.Name(), ''))
            condition = 'Or'

        tradeFilter = ael.TradeFilter.new()
        name = str(acm.Time().TimeNow()) + str(TradeFilterHelper.counter)
        TradeFilterHelper.counter += 1
        tradeFilter.fltid = name
        tradeFilter.set_query(query)
        tradeFilter.commit()
        
        return acm.FTradeSelection[name]

class TimeSeriesHelper:

    @staticmethod
    def GetLastRunNo(timeSeriesSpec, date):
        result = ael.asql("SELECT max(run_no) FROM TimeSeries WHERE ts_specnbr = %i and day = '%s'" % (timeSeriesSpec.Oid(), str(date)))[1][0]
        if len(result) == 0:
            return 0
        else:
            return result[0][0]
            
    @staticmethod
    def GetTimeSeries(timeSeriesSpec, date, runNo):
        return acm.FTimeSeries.Select01("timeSeriesSpec = %(timeSeriesSpec)i and day = '%(day)s' and runNo = %(runNo)i" % \
            {'timeSeriesSpec': timeSeriesSpec.Oid(), 'day': str(date), 'runNo': runNo}, 'More than one TimeSeries returned.')
    
    @staticmethod
    def DeleteSeriesData(timeSeriesSpec, date, slBatchType):
        seriesData = acm.FTimeSeries.Select("timeSeriesSpec = %(timeSeriesSpec)i and day = '%(day)s'" % \
            {'timeSeriesSpec': timeSeriesSpec.Oid(), 'day': str(date)})
        for i in seriesData.AsArray():
            if slBatchType:
                test_helper_instruments.InstrumentHelper.ClearSlBatchNumber(slBatchType, i.Value())
                
            i.Delete()

class GeneralHelper:

    @staticmethod             
    def AssertTypeAndValue(testCase, actualValue, expectedValue, expectedType, message):
        testCase.failUnless(isinstance(actualValue, expectedType), '%s: Expected %s, got %s' % (message, str(expectedType), str(type(actualValue))))
        testCase.assertEqual(expectedValue, actualValue, '%s: Expected [%f], got [%f]' % (message, expectedValue, actualValue))
    
    @staticmethod
    def AssertRaises(testCase, callable, expectedMessage, *args):
        try:
            callable(*args)
        except Exception, ex:
            testCase.assert_(_startsWith(str(ex), expectedMessage), 'Exception message not as expected. Expected "%s", got "%s"' % (expectedMessage, ex))
        else:
            testCase.fail('Expected an exception: ' + expectedMessage)
