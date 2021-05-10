"""-----------------------------------------------------------------------------
PROJECT                 :  N/A
PURPOSE                 :  FTrade unit test helper classes
DEPATMENT AND DESK      :  N/A
REQUESTER               :  N/A
DEVELOPER               :  Francois Truter
CR NUMBER               :  494829
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-11-16 494829    Francois Truter    Initial implementation
"""

import acm
import ael
from test_helper_general import PartyHelper
from test_helper_general import PortfolioHelper
from test_helper_general import TimeSeriesHelper
from test_helper_instruments import InstrumentHelper

class TradeHelper:
    defaultPortfolio = None
    defaultCounterparty = None
    defaultAcquirer = None

    @staticmethod
    def _getDefaultPortfolio():
        if TradeHelper.defaultPortfolio == None:
            TradeHelper.defaultPortfolio = PortfolioHelper.CreatePersistantPortfolio()
        return TradeHelper.defaultPortfolio
        
    @staticmethod
    def _getDefaultCounterparty():
        if TradeHelper.defaultCounterparty == None:
            TradeHelper.defaultCounterparty = PartyHelper.CreatePersistantCounterparty()
        return TradeHelper.defaultCounterparty
        
    @staticmethod
    def _getDefaultAcquirer():
        if TradeHelper.defaultAcquirer == None:
            TradeHelper.defaultAcquirer = PartyHelper.CreatePersistantCounterparty()
        return TradeHelper.defaultAcquirer
    
    @staticmethod
    def _getMirrorTrade(acmTrade):
        aelTrade = ael.Trade[acmTrade.Oid()]
        mirrorTrade = aelTrade.get_mirror_trade()
        if mirrorTrade:
            return acm.FTrade[mirrorTrade.trdnbr]
        else:
            return None

    @staticmethod
    def AssertSecurityLoanTrade(testCase, actualTrade, expectedStartDate, expectedEndDate, expectedUnderlying, expectedQuantity, \
    expectedSlMinimumFee, expectedSlDividendFactor, expectedSlTradingCapacity, expectedSlExternalInternal, expectedSlVat, \
    expectedPortfolio, expectedAcquirer, expectedBroker, expectedStatus, expectedSlCfd):
        instrument = actualTrade.Instrument()
        additionalInfo = instrument.AdditionalInfo()
        quantity = TradeHelper.TradeQuantity(expectedQuantity, instrument)

        testCase.assertEqual(instrument.InsType(), 'SecurityLoan', 'Expected a Security Loan trade')
        testCase.assertEqual(instrument.StartDate(), expectedStartDate, 'Start Date not as expected')
        testCase.assertEqual(instrument.EndDate(), expectedEndDate, 'End Date not as expected')
        testCase.assertEqual(instrument.Underlying(), expectedUnderlying, 'Underlying not as expected')
        testCase.assertEqual(actualTrade.Quantity(), quantity, 'Quantity not as expected. Actual %f, Expected %f' % (actualTrade.Quantity(), quantity))
        testCase.assertEqual(actualTrade.Portfolio(), expectedPortfolio, 'Portfolio not as expected')
        testCase.assertEqual(actualTrade.Acquirer(), expectedAcquirer, 'Acquirer not as expected')
        testCase.assertEqual(actualTrade.Broker(), expectedBroker, 'Broker not as expected')
        testCase.assertEqual(actualTrade.Status(), expectedStatus, 'Status not as expected')
        testCase.assertEqual(additionalInfo.SL_Minimum_Fee(), expectedSlMinimumFee, 'Minimum Fee not as expected')
        testCase.assertEqual(additionalInfo.SL_Dividend_Factor(), expectedSlDividendFactor, 'Dividend Factor not as expected')
        testCase.assertEqual(additionalInfo.SL_Trading_Capacity(), expectedSlTradingCapacity, 'Trading Capacity not as expected')
        testCase.assertEqual(additionalInfo.SL_ExternalInternal(), expectedSlExternalInternal, 'External Internal not as expected')
        testCase.assertEqual(additionalInfo.SL_VAT(), expectedSlVat, 'VAT not as expected')
    
    @staticmethod    
    def Contains(actualTrades, expectedStartDate, expectedEndDate, expectedUnderlying, expectedQuantity, \
    expectedSlMinimumFee, expectedSlDividendFactor, expectedSlTradingCapacity, expectedSlExternalInternal, expectedSlVat, \
    expectedPortfolio, expectedMirrorPortfolio, expectedCounterparty, expectedAcquirer, expectedBroker, expectedStatus, expectedSlCfd, expectedRate):
        for actualTrade in actualTrades:
            instrument = actualTrade.Instrument()
            additionalInfo = instrument.AdditionalInfo()
            leg = instrument.FirstFixedLeg()
            quantity = TradeHelper.TradeQuantity(expectedQuantity, instrument)
            mirrorPortfolio = TradeHelper._getMirrorTrade(actualTrade).Portfolio()
            
            if instrument.InsType() == 'SecurityLoan' and \
                instrument.StartDate() == expectedStartDate and \
                instrument.EndDate() == expectedEndDate and \
                instrument.Underlying() == expectedUnderlying and \
                actualTrade.Quantity() == quantity and \
                actualTrade.Portfolio() == expectedPortfolio and \
                mirrorPortfolio == expectedMirrorPortfolio and \
                actualTrade.Counterparty() == expectedCounterparty and \
                actualTrade.Acquirer() == expectedAcquirer and \
                actualTrade.Broker() == expectedBroker and \
                actualTrade.Status() == expectedStatus and \
                additionalInfo.SL_Minimum_Fee() == expectedSlMinimumFee and \
                additionalInfo.SL_Dividend_Factor() == expectedSlDividendFactor and \
                additionalInfo.SL_Trading_Capacity() == expectedSlTradingCapacity and \
                additionalInfo.SL_ExternalInternal() == expectedSlExternalInternal and \
                additionalInfo.SL_VAT() == expectedSlVat and \
                additionalInfo.SL_CFD() == expectedSlCfd and \
                leg.FixedRate() == expectedRate:
            
                return True
        return False

    @staticmethod
    def UnderlyingQuantity(tq, i):
        return i.RefValue() * tq

    @staticmethod
    def TradeQuantity(uq, i):
        return uq / i.RefValue()
        
    @staticmethod
    def GetTrades(portfolio, instrument):
        query = acm.CreateFASQLQuery('FTrade', 'AND')
        
        if portfolio != None:
            op = query.AddOpNode('AND')
            op.AddAttrNode('Portfolio.Oid', 'EQUAL', portfolio.Oid())
        
        op = query.AddOpNode('AND')
        op.AddAttrNode('Instrument.Underlying.Oid', 'EQUAL', instrument.Oid())
        
        return query.Select()
        
    @staticmethod
    def GetLatestSweepingBatchTrades(date):
        timeSeriesSpec = acm.FTimeSeriesSpec['SBL Sweeping Batch']
        runNo = TimeSeriesHelper.GetLastRunNo(timeSeriesSpec, date)
        timeSeries = acm.FTimeSeries.Select01("timeSeriesSpec = %i and runNo = %i and day = '%s'" % (timeSeriesSpec.Oid(), runNo, date), 'More than one Time Series returned when searching for sweeping batch number')
        batchNumber = timeSeries.Value()
        
        query = acm.CreateFASQLQuery('FTrade', 'AND')
        
        op = query.AddOpNode('AND')
        op.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'SecurityLoan'))
        op.AddAttrNode('Instrument.AdditionalInfo.SL_SweepingBatchNo', 'EQUAL', batchNumber)
        
        return query.Select()
    
    @staticmethod
    def GetSecurityLoanCount():
        result = ael.asql("SELECT COUNT(trdnbr) FROM Instrument, Trade WHERE Instrument.instype = 'SecurityLoan' AND Instrument.insaddr = Trade.insaddr")
        return result[1][0][0][0]
    
    @staticmethod    
    def BookSecurityLoan(instrument, status, startDate = acm.Time().TimeNow(), quantity = 1):
        trade = acm.FTrade()
        trade.Instrument(instrument)
        trade.Currency(instrument.Currency())
        trade.TradeTime(startDate)
        trade.AcquireDay(startDate)
        trade.ValueDay(startDate)
        trade.Acquirer(TradeHelper._getDefaultAcquirer())
        trade.Portfolio(TradeHelper._getDefaultPortfolio())
        trade.Counterparty(TradeHelper._getDefaultCounterparty())
        trade.Quantity(TradeHelper.TradeQuantity(quantity, instrument))
        trade.Status(status)
        trade.Commit()
        
        return trade
    
    @staticmethod    
    def BookCFDSecurityLoanAndTrade(startDate, endDate, status, quantity):
        instrument = InstrumentHelper.CreatePersistantCFDSecurityLoan(startDate, endDate)
        trade = TradeHelper.BookSecurityLoan(instrument, status, startDate, quantity)
        instrument.SLGenerateCashflows()
        return trade
    
    @staticmethod
    def BookSecurityLoanFromUnderlying(portfolio, underlying, quantity, refPrice, rate, slExtInt, startDate, status):
        instrument = InstrumentHelper.CreateSecurityLoanFromUnderlying(underlying, refPrice, rate, slExtInt, startDate, None, None)
        setTerminated = status == 'Terminated'
        if setTerminated:
            status = 'BO Confirmed'
        trade = acm.FTrade()
        trade.Instrument(instrument)
        trade.Currency(instrument.Currency())
        trade.TradeTime(startDate)
        trade.AcquireDay(startDate)
        trade.ValueDay(startDate)
        trade.Acquirer(TradeHelper._getDefaultAcquirer())
        trade.Portfolio(portfolio)
        trade.Counterparty(TradeHelper._getDefaultCounterparty())
        trade.Quantity(TradeHelper. TradeQuantity(quantity, instrument)) 
        trade.Status(status)
        trade.Commit()
        
        if setTerminated:
            trade.Status('Terminated')
            trade.Commit()
            
        return trade
    
    @staticmethod
    def BookTrade(portfolio, instrument, date, quantity, status = 'FO Confirmed'):
        setTerminated = status == 'Terminated'
        if setTerminated:
            status = 'BO Confirmed'
        date = acm.Time().TimeNow()
        trade = acm.FTrade()
        trade.Instrument(instrument)
        trade.Currency(instrument.Currency())
        trade.TradeTime(date)
        trade.AcquireDay(date)
        trade.ValueDay(date)
        trade.Acquirer(TradeHelper._getDefaultAcquirer())
        trade.Portfolio(portfolio)
        trade.Counterparty(TradeHelper._getDefaultCounterparty())
        trade.Quantity(quantity)
        trade.Status(status)
        trade.Commit()
        
        if setTerminated:
            trade.Status('Terminated')
            trade.Commit()
        
        return trade
