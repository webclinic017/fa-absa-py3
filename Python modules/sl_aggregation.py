"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Aggregates Security Loan Trades and Instruments
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  471048 

HISTORY
================================================================================
Date       Change no Developer              Description
--------------------------------------------------------------------------------
2010-04-22 378175    Francois Truter        Commit transactions per aggregate
                                            trade. Add time to instrument expiry
                                            date.
2010-08-05 389878    Francois Truter        Transactions created with 
                                            BO Confirmed status.
2010-10-21 471048    Francois Truter        Not setting FInstrument.EpiryDate
-----------------------------------------------------------------------------"""

import acm
from decimal import Decimal
from datetime import datetime
import sys, traceback
import math

newline = '\r\n'

archived = 1
notArchived = 0

aggregated = 2
notAggregated = 0

def ToAcmDate(aelDate):
    [y, m, d] = aelDate.to_ymd()
    return acm.Time().DateFromYMD(y, m, d)
    
def _strTime(time = datetime.now()):
    return time.strftime('%Y-%m-%d %H:%M:%S')

class Period(object):
    @staticmethod
    def _toDate(str):
        return acm.Time().AsDate(str)
    
    def __init__(self, startDate, endDate):
        self.__startDate = Period._toDate(startDate)
        self.__endDate = Period._toDate(endDate)
        
        if self.__endDate < self.__startDate:
            raise Exception('End date cannot be before start date')
        
    startDate = property(lambda self: self.__startDate)
    endDate = property(lambda self: self.__endDate)
    
class PeriodType:
    Daily = 0
    Weekly = 1
    Monthly = 2
    
class PeriodIterator:
    
    def __init__(self, startDate, endDate, periodType, calendar):
        self.__startDate = Period._toDate(startDate)
        self.__endDate = Period._toDate(endDate)
        
        if self.__endDate < self.__startDate:
            raise Exception('End date cannot be before start date')
            
        if not calendar.IsKindOf(acm.FCalendar):
            raise Exception('Calendar must be of type FCalendar')
            
        self.__type = periodType
        self.__calendar = calendar
        self.__currentPeriod = None
        self.__first = None
        self.__endDate = self._endOfPeriod(endDate)
    
    @staticmethod
    def _enumDayOfWeek(dayStr):
        if dayStr == 'Monday':
            return 1
        elif dayStr == 'Tuesday':
            return 2
        elif dayStr == 'Wednesday':
            return 3
        elif dayStr == 'Thursday':
            return 4
        elif dayStr == 'Friday':
            return 5
        elif dayStr == 'Saturday':
            return 6
        elif dayStr == 'Sunday':
            return 7
        else:
            raise Exception('Unknown day: %s' % dayStr)
        
    def _nextWeekday(self, date, weekday):
        days = weekday - PeriodIterator._enumDayOfWeek(acm.Time().DayOfWeek(date))
        if days <= 0: days += 7
        return acm.Time().DateAddDelta(date, 0, 0, days)
        
    def _nextMonth(self, date):
        nextMonth = acm.Time().DateAddDelta(date, 0, 1, 0)
        days = acm.Time().DaysInMonth(nextMonth) - acm.Time().DayOfMonth(nextMonth)
        if days != 0:
            nextMonth = acm.Time().DateAddDelta(nextMonth, 0, 0, days)
        
        return nextMonth
        
    def _prev(self, date):
        newDate = None
        if self.__type == PeriodType.Monthly:
            newDate = acm.Time().DateAddDelta(date, 0, -1, 0)
        else:
            newDate = acm.Time().DateAddDelta(date, 0, 0, -1)
        return newDate
        
    def __iter__(self):
        endOfPeriod = self._endOfPeriod(self.__startDate)
        if self.__startDate == endOfPeriod:
            endOfPeriod = self._next(self.__startDate)
        self.__currentPeriod = Period(self.__startDate, endOfPeriod)
        self.__first = True
        return self
        
    def _next(self, date):
        nextDate = None
        if self.__type == PeriodType.Daily:
            nextDate = self.__calendar.AdjustBankingDays(date, 1)
        elif self.__type == PeriodType.Weekly:
            nextDate = self._nextWeekday(date, PeriodIterator._enumDayOfWeek('Friday'))
        elif self.__type == PeriodType.Monthly:
            nextDate = self._nextMonth(date)
        else:
            raise Exception('Unknown period type. Use Daily, Weekly or Monthly.')
            
        return nextDate
        
    def _endOfPeriod(self, date):
        return self._next(self._prev(date))

    def next(self):
        if not self.__first:
            nextDate = self._next(self.__currentPeriod.endDate)            
            if nextDate > self.__endDate:
                raise StopIteration
            
            self.__currentPeriod = Period(self.__currentPeriod.endDate, nextDate)
        else:
            self.__first = False
            
        return self.__currentPeriod

class AggregatorCollection:

    def __init__(self, trades, periodType, date):
        self._periodType = periodType
        self.__date = date
        self._aggregators = dict()
        for trade in trades:
            if self._canAggregate(trade):
                self._addTrade(trade)
                
    def _isExpired(self, trade):
        partialReturnExpired = True
        if trade.SLPartialReturned():
            partialReturnExpired = self._isExpired(trade.SLPartialReturnLastTrade())
            
        instrument = trade.Instrument()
        return partialReturnExpired and instrument.InsType() == 'SecurityLoan' and instrument.ExpiryDateOnly() <= self.__date and (instrument.OpenEnd() == 'Terminated' or instrument.OpenEnd() == 'None')
    
    def _canAggregate(self, trade):
        return trade.Aggregate() == notAggregated and self._isExpired(trade)       
            
    def __str__(self):
        output = 'Trades in Aggregator Collection:'
        
        if not self._aggregators:
            output += ' None'
        else:
            for key in self._aggregators:
                output += newline
                output += str(self._aggregators[key])

        return output
            
    def _addTrade(self, trade):
        underlying = trade.Instrument().Underlying()
        
        aggregator = None
        if not underlying in self._aggregators:
            aggregator = Aggregator(underlying)
            self._aggregators[underlying] = aggregator
        else:
            aggregator = self._aggregators[underlying]
            
        aggregator.AddTrade(trade)
        
    def _createAggregateInstruments(self):
        for key in self._aggregators:
            self._aggregators[key].CreateAggregateInstrument()
        
    def Aggregate(self):
        if acm.ArchivedMode() == 1:
            print('Cannot run aggregation in archived mode.')
            return

        startTime = datetime.now()
        print('Aggregation started at %s' % _strTime(startTime))

        acm.BeginTransaction()
        try:
            self._createAggregateInstruments()
            acm.CommitTransaction()
        except Exception, ex:
            acm.AbortTransaction()
            traceback.print_exc(file=sys.stdout) 
            raise Exception('The following error occurred while creating the aggregate instruments, transaction aborted: %s' % str(ex))
        
        totalTradesAggrogated = 0
        totalAggrogateTradesCreated = 0
        totalInstrumentsArchived = 0
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        for key in self._aggregators:
            try:
                tradesAggrogated, aggrogatedTrades, instrumentsArchived = self._aggregators[key].Aggregate(calcSpace, self._periodType)
                totalTradesAggrogated += tradesAggrogated
                totalAggrogateTradesCreated += aggrogatedTrades
                totalInstrumentsArchived += instrumentsArchived
            except Exception, ex:
                traceback.print_exc(file=sys.stdout) 
                print(ex)

        endTime = datetime.now()
        timeTaken = endTime - startTime
        print('Aggregation completed at %(time)s, time taken: %(timeTaken)s' % {'time': _strTime(endTime), 'timeTaken': str(timeTaken)})
        print('Aggregation Summary: %(trades)i trades aggregated into %(aggregate)i aggregate trades, %(instruments)i instruments archived.' % \
            {'trades': totalTradesAggrogated, 'aggregate': totalAggrogateTradesCreated, 'instruments': totalInstrumentsArchived})
    
class Aggregator:

    def __init__(self, underlying):
        if not underlying.IsKindOf(acm.FInstrument):
            raise Exception('Underlying must be of type FInstrument')
            
        self.__underlying = underlying
        self.__aggregateInstrument = None
        self.__firstDate = acm.Time().DateNow()
        self.__tradeCollections = {}
        self.__instruments = set()
        self.__archivedTrades = set()
        
    def __str__(self):
        output = 'Trades for underlying instrument [%(underlying)s], aggregate instrument [%(aggregate)s]:' % \
            {'underlying': self.__underlying.Name(), 'aggregate': 'Not Assigned' if not self.__aggregateInstrument else self.__aggregateInstrument.Name() }
        
        if not self.__tradeCollections:
            output += '  None'
        else:
            for key in self.__tradeCollections:
                output += newline
                output += str(self.__tradeCollections[key])

        return output
        
    def _getAggregateName(self, new = False, counter = 0):
        suffix = '' if counter <= 0 else '#' + str(counter)
        name = 'SL Agg/' + self.__underlying.Name()
        length = 50 - (len(name) + len(suffix))
        name = name[0:length] + suffix
        if new:
            existing = acm.FInstrument[name]
            if existing:
                name = self._getAggregateName(counter + 1)
        
        return name
        
    @staticmethod
    def _archiveInstrument(instrument):
        instrument.ArchiveStatus(archived)
        instrument.Commit()
        print('Instrument %s [%i] archived.' % (instrument.Name(), instrument.Oid()))
        
        for leg in instrument.Legs():
            leg.ArchiveStatus(archived)
            leg.Commit()
            print('Leg %i archived.' % leg.Oid())
            for cashFlow in leg.CashFlows():
                cashFlow.ArchiveStatus(archived)
                cashFlow.Commit()
                print('Cash-flow %i archived.' % cashFlow.Oid())
                
        for additionalInfo in acm.FAdditionalInfo.Select('recaddr = %i' % instrument.Oid()):
            if additionalInfo.AddInf().RecType() == 'Instrument':
                additionalInfo.ArchiveStatus(archived)
                additionalInfo.Commit()
                print('Additional Info %i archived.' % additionalInfo.Oid())
    
    @staticmethod
    def ArchiveInstruments(instruments, archivedTrades):
        counter = 0
        for instrument in instruments:
            allTradesArchived = True
            
            for trade in instrument.Trades():
                if not trade in archivedTrades:
                    allTradesArchived = False
                    break
                    
            if allTradesArchived:
                Aggregator._archiveInstrument(instrument)
                counter += 1
                
        return counter
        
    def _archiveInstruments(self):
        return Aggregator.ArchiveInstruments(self.__instruments, self.__archivedTrades)
        
    @staticmethod
    def ArchiveTrade(trade):
        trade.ArchiveStatus(archived)
        trade.Commit()
        print('Trade %i aggreated.' % trade.Oid())
            
        for additionalInfo in acm.FAdditionalInfo.Select('recaddr = %i' % trade.Oid()):
            if additionalInfo.AddInf().RecType() == 'Trade':
                additionalInfo.ArchiveStatus(archived)
                additionalInfo.Commit()
                print('Additional Info %i archived.' % additionalInfo.Oid())
                
        for payment in trade.Payments():
            payment.ArchiveStatus(archived)
            payment.Commit()
            print('Payment %i archived.' % payment.Oid())
        
    def CreateAggregateInstrument(self):
        aggregateName = self._getAggregateName()
        aggregateInstrument = acm.FSecurityLoan.Select01('name = %s' % aggregateName, 'More than one instrument returned with name [%s].' % aggregateName)
        
        if not aggregateInstrument:
            new = True
            tomorrow = acm.Time().DateAddDelta(acm.Time().DateToday(), 0, 0, 1)
            aggregateInstrument = acm.FSecurityLoan()
            aggregateInstrument.OpenEnd('Open End')
            aggregateInstrument.Underlying(self.__underlying)
            aggregateInstrument.Name(self._getAggregateName(new))
            aggregateInstrument.StartDate(self.__firstDate)
            aggregateInstrument.RefPrice(1)
            aggregateInstrument.RefValue(0)
            
            leg = aggregateInstrument.CreateLeg(True)
            leg.StartDate(self.__firstDate)
            leg.EndDate(tomorrow)
            leg.LegType('Fixed')
            leg.DayCountMethod('Act/365')
            leg.FixedRate(0)
            
            aggregateInstrument.Commit()
            leg.Commit()
            
        for leg in aggregateInstrument.Legs():
            for cashFlow in leg.CashFlows():
                cashFlow.Delete()
            
        self.__aggregateInstrument = aggregateInstrument
        
    def AddTrade(self, trade):
        portfolio = trade.Portfolio()
        counterparty = trade.Counterparty()
        key = (portfolio, counterparty)

        tradeCollection = None
        if key in self.__tradeCollections:
            tradeCollection = self.__tradeCollections[key]
        else:
            tradeCollection = Aggregator.TradeCollection(portfolio, counterparty)
            self.__tradeCollections[key] = tradeCollection
            
        tradeCollection.AddTrade(trade)
        startDate = trade.Instrument().StartDate()
        if not startDate:
            startDate = trade.AcquireDay()
        if startDate < self.__firstDate:
            self.__firstDate = startDate
            
        instrument = trade.Instrument()
        self.__instruments.add(instrument)
        
    def Aggregate(self, calcSpace, periodType):
        if not self.__aggregateInstrument:
            raise Exception('No aggregate instrument assigned for underlying [%s]. Please run CreateAggregateInstrument before running aggregation.' % self.__underlying.Name())
        
        totalTradesAggrogated = 0
        aggrogateTradesCreated = 0
        instrumentsArchived = 0
        
        startTime = datetime.now()
        print('Starting with %s at %s' % (self.__underlying.Name(), _strTime(startTime)))

        for key in self.__tradeCollections:
            tradesAggrogated = self.__tradeCollections[key].Aggregate(self.__aggregateInstrument, calcSpace, periodType, self.__archivedTrades)
            if tradesAggrogated > 0:
                totalTradesAggrogated += tradesAggrogated
                aggrogateTradesCreated += 1
        
        acm.BeginTransaction()
        try:
            instrumentsArchived = self._archiveInstruments()
            acm.CommitTransaction()
        except Exception, ex:
            acm.AbortTransaction()
            instrumentsArchived = 0
            print('An error occurred while archiving instruments for %s - instruments not archived: %s' % (self.__underlying.Name(), str(ex)))
        
        endTime = datetime.now()
        timeTaken = endTime - startTime
        print('Completed %(underlying)s at %(time)s, after %(timeTaken)s: %(trades)i trades aggregated into %(aggregate)i aggregate trades, %(instruments)i instruments archived.' % \
            {'underlying': self.__underlying.Name(), 'time': _strTime(endTime), 'timeTaken': str(timeTaken), 'trades': totalTradesAggrogated, 'aggregate': aggrogateTradesCreated, 'instruments': instrumentsArchived})
            
        return totalTradesAggrogated, aggrogateTradesCreated, instrumentsArchived
            
    class TradeCollection:
        
        def __init__(self, portfolio, counterparty):
            self._portfolio = portfolio
            self._acquirer = portfolio.PortfolioOwner()
            self._counterparty = counterparty
            self._firstDate = acm.Time().DateNow()
            self._lastDate = acm.Time().DateNow()
            self._trades = []
            
        def __str__(self):
            output = '%(numTrades)i trades for Portfolio: %(portfolio)s, Counterparty: %(counterparty)s:' % \
                {'numTrades': len(self._trades), 'portfolio': self._portfolio.Name(), 'counterparty': self._counterparty.Name()}

            if not self._trades:
                output += ' None'
            else:
                for trade in self._trades:
                    output += newline
                    output += '   %i' % trade.Oid()
                
            return output
        
        def _getDefaultTrade(self, instrument):
            trade = acm.FTrade()
            trade.Aggregate(aggregated)
            trade.Instrument(instrument)
            trade.Currency(instrument.Currency())
            trade.TradeTime(self._firstDate)
            trade.Acquirer(self._acquirer)
            trade.Portfolio(self._portfolio)
            trade.Counterparty(self._counterparty)
            trade.AcquireDay(self._firstDate)
            trade.ValueDay(self._firstDate)
            trade.Quantity(0)
            trade.HaircutType('Discount')
            trade.Status('BO Confirmed')
            trade.Text1('sl_aggregation')
            trade.Type('Aggregate')
            
            return trade
         
        @staticmethod
        def _archiveTrade(trade, aggregatedTrade):
            trade.AggregateTrade(aggregatedTrade)
            Aggregator.ArchiveTrade(trade)
            
        def AddTrade(self, trade):
            instrument = trade.Instrument()
            self._trades.append(trade)
            startDate = instrument.StartDate()
            if not startDate:
                startDate = trade.AcquireDay()
            if startDate < self._firstDate:
                self._firstDate = startDate
            if instrument.ExpiryDateOnly() > self._lastDate:
                self._lastDate = instrument.ExpiryDateOnly()
            
        def Aggregate(self, aggregateInstrument, calcSpace, periodType, archivedTrades):
            if len(self._trades) < 2:
                return 0

            acm.BeginTransaction()
            try:
                aggregatedTrade =  self._getDefaultTrade(aggregateInstrument)
                aggregatedTrade.Commit()
                currency = aggregatedTrade.Currency()
                periods = PeriodIterator(self._firstDate, self._lastDate, periodType, currency.Calendar())
                
                tradeCalculations = {}
                for period in periods:
                    cashPosition = Decimal('0')
                    
                    for trade in self._trades:
                        calculation = None
                        if trade in tradeCalculations:
                            calculation = tradeCalculations[trade]
                        else:
                            calculation = trade.Calculation()
                            tradeCalculations[trade] = calculation
                        
                        calculated_cash = calculation.Cash(calcSpace, period.startDate, period.endDate, currency).Number()
                        if math.isnan(calculated_cash):
                            calculated_cash = 0.0
                        cash = Decimal(str(calculated_cash))
                        cashPosition += cash
                    
                    if cashPosition != 0:
                        payment = acm.FPayment()
                        payment.Amount(float(cashPosition))
                        payment.Type('Cash')
                        payment.Trade(aggregatedTrade)
                        payment.Party(self._counterparty)
                        payment.Currency(currency)
                        payment.PayDay(period.endDate)
                        payment.ValidFrom(period.endDate)
                        payment.Text('SBL Aggregation')                       
                        payment.Commit()
                    
                for trade in self._trades:
                    Aggregator.TradeCollection._archiveTrade(trade, aggregatedTrade)
                    archivedTrades.add(trade)
                    
                acm.CommitTransaction()
            
            except Exception, ex:
                acm.AbortTransaction()
                traceback.print_exc(file=sys.stdout) 
                raise Exception('The following error occurred while aggregating trades for [%(underlying)s, %(portfolio)s, %(counterparty)s], transaction aborted: %(error)s' % \
                    {'underlying': aggregateInstrument.Underlying().Name(), 'portfolio': self._portfolio.Name(), 'counterparty': self._counterparty.Name(), 'error': str(ex)})
            
            return len(self._trades)
            
class VoidedTradeArchiver:

    @staticmethod
    def Run(trades, date):
        instruments = set()
        archivedTrades = set()
        numTradesArchived = 0
        numInstrumentsArchived = 0
        try:
            for trade in trades:
                instrument = trade.Instrument()
                if instrument.InsType() == 'SecurityLoan' and trade.Status() == 'Void' and instrument.ExpiryDateOnly() <= date:
                    Aggregator.ArchiveTrade(trade)
                    numTradesArchived += 1
                    
                    archivedTrades.add(trade)
                    instruments.add(instrument)
                        
            numInstrumentsArchived = Aggregator.ArchiveInstruments(instruments, archivedTrades)
        except Exception, ex:
            traceback.print_exc(file=sys.stdout) 
            print('The following error occurred while archiving voided trades, transaction aborted: %s' %  str(ex))
        else:
            print('%(trades)i trades archived, %(instruments)i instruments archived' % {'trades': numTradesArchived, 'instruments': numInstrumentsArchived})
        
                    
class DeAggregator:

    @staticmethod
    def _deArchiveInstrument(instrument):
        instrument.ArchiveStatus(notArchived)
        instrument.Commit()
        print('Instrument %s moved from archive to live records.' % instrument.Name())
        
        for leg in instrument.Legs():
            leg.ArchiveStatus(notArchived)
            leg.Commit()
            print('Leg %i moved from archive to live records.' % leg.Oid())
            for cashFlow in leg.CashFlows():
                cashFlow.ArchiveStatus(notArchived)
                cashFlow.Commit()
                print('Cash-flow %i moved from archive to live records.' % cashFlow.Oid())
        
        for additionalInfo in acm.FAdditionalInfo.Select('recaddr = %i' % instrument.Oid()):
            if additionalInfo.AddInf().RecType() == 'Instrument':
                additionalInfo.ArchiveStatus(notArchived)
                additionalInfo.Commit()
                print('Additional Info %i moved from archive to live records.' % additionalInfo.Oid())
    
    @staticmethod
    def _deArchiveTrade(trade):
        trade.AggregateTrade(None)
        trade.ArchiveStatus(notArchived)
        trade.Commit()
        print('Trade %i moved from archive to live records.' % trade.Oid())
        
        for additionalInfo in acm.FAdditionalInfo.Select('recaddr = %i' % trade.Oid()):
            if additionalInfo.AddInf().RecType() == 'Trade':
                additionalInfo.ArchiveStatus(notArchived)
                additionalInfo.Commit()
                print('Additional Info %i moved from archive to live records.' % additionalInfo.Oid())
                
        for payment in trade.Payments():
            payment.ArchiveStatus(notArchived)
            payment.Commit()
            print('Payment %i moved from archive to live records.' % payment.Oid())
    
    @staticmethod
    def Run(trades):
        if acm.ArchivedMode() == 0:
            print('Must run De-Aggregation in archived mode.')
            return
                
        totalAggregatedTrades = 0    
        totalTrades = 0
        totalInstruments = 0
        try:
            aggregateTrades = {}
            for trade in trades:
                aggregateTrade = trade.AggregateTrade()
                if not aggregateTrade:
                    print('Trade %i is not aggregated - de-aggregation not performed' % trade.Oid())
                    continue
                    
                if aggregateTrade not in aggregateTrades:
                    aggregateTrades[aggregateTrade] = []
                    
                aggregateTrades[aggregateTrade].append(trade)
            
            
            for aggregateTrade in aggregateTrades:
                numTrades, numInstruments = DeAggregator(aggregateTrade, aggregateTrades[aggregateTrade]).DeAggregate()
                totalTrades += numTrades
                totalInstruments += numInstruments
                totalAggregatedTrades += 1
                
        except Exception, ex:
            print(str(ex))
            
        finally:    
            print('De-Aggregation summary: %(trades)i trades and %(instruments)i instruments were moved to the live records, %(aggregate)i aggregate trades were deleted.' % \
                {'trades': totalTrades, 'instruments': totalInstruments, 'aggregate': totalAggregatedTrades})

    def __init__(self, aggregateTrade, trades):
        self.__aggregateTrade = aggregateTrade
        self.__aggregateTradeNumber = aggregateTrade.Oid()
        self.__trades = trades
        
    def DeAggregate(self):
        if not self.__trades:
            return

        numTrades = 0
        numInstruments = 0
        acm.BeginTransaction()
        try:
            instruments = set()
            
            for trade in self.__trades:
                instrument = trade.Instrument()
                instruments.add(instrument)
                DeAggregator._deArchiveTrade(trade)
                numTrades += 1
                
            for instrument in instruments:
                if instrument.ArchiveStatus() == archived:
                    DeAggregator._deArchiveInstrument(instrument)
                    numInstruments += 1
            
            self.__aggregateTrade.Delete()
            acm.CommitTransaction()
        except Exception, ex:
            acm.AbortTransaction()
            traceback.print_exc(file=sys.stdout) 
            raise Exception('The following error occurred while de-aggregating, transaction aborted: %s' % str(ex))
        else:
            print('Aggregate trade %(aggregate)i deleted: %(trades)i trades de-aggregated and %(instruments)i instruments moved to the live records' % \
                {'aggregate': self.__aggregateTradeNumber, 'trades': numTrades, 'instruments': numInstruments})
                
        return numTrades, numInstruments
