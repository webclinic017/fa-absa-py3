"""-----------------------------------------------------------------------------
PROJECT                 :  N/A
PURPOSE                 :  Sweeps bond positions into a specified portfolio
DEPATMENT AND DESK      :  FIXED INCOME
REQUESTER               :  Kelly Hattingh
DEVELOPER               :  Francois Truter
CR NUMBER               :  549170
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                         Description
--------------------------------------------------------------------------------
2010-06-28 355193   Francois Truter     Initial Implementation
2010-08-26 412608   Francois Truter     Added Valuation Group parameter
2010-12-07 518491   Francois Truter     Using decorators + _isNumber 
                                        accepts arrays with one number
2011-01-18 549170   Francois Truter     Added bid and offer adjustments
2010-06-28 355193   Francois Truter     Initial Implementation
2010-08-26 412608   Francois Truter     Added Valuation Group parameter
2010-12-07 518491   Francois Truter     Using decorators + _isNumber 
                                        accepts arrays with one number
2011-01-18 549170   Francois Truter     Added bid and offer adjustments
2010-06-28 355193   Francois Truter     Initial Implementation
2010-08-26 412608   Francois Truter     Added Valuation Group parameter
2010-12-07 518491   Francois Truter     Using decorators + _isNumber 
                                        accepts arrays with one number
2011-01-18 549170   Francois Truter     Added bid and offer adjustments
2014-12-02 abcdef   Peter Fabian        Determine price for corp bonds 
                                        from underlying govt bond plus 
                                        spread if they are defined 
                                        in the spread curve


2014-12-09 CHNG0002507135       Sanele Macanda          catered for the REPO RATES LINKERS csv file
2016-10-05                      Faize Adams             Updated adjustment logic for net positions.
                                                        Net long positions use the bid rate.
                                                        Net short positions use the offer rate.
2017-05-16 4576458  Ondrej Bahounek         Update RefValue calculation.
"""

import os
import math
import acm
import csv, string
import ael

def _isNumber(object):
    try:
        if (hasattr(object, '__iter__') or (hasattr(object, 'IsKindOf') and object.IsKindOf(acm.FCollection))) and len(object) == 1:
            object = object[0]
        if object != object:
            isNumber = False
        else:
            object = float(object)
            isNumber = True
    except:
        isNumber = False
    
    return isNumber, object
    
def aelDateToAcm(date):
    ymd = date.to_ymd ()
    return acm.Time().DateFromYMD(ymd[0], ymd[1], ymd[2])
        
class RepoRateHelper:

    bid = 'bid'
    offer = 'offer'
    
    def __init__(self, filepath):
        self._filepath = filepath
        self._read = False
        self._rates = {}
            
    def _readRates(self):
        with open(self._filepath, "r") as file:
            #reader = csv.reader(file)
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                try:
                    if len(row) == 3:
                        instrumentName = row['Instrument']
                        bidStr = row['BID']
                        bid = float(bidStr)
                        offerStr = row['Offer']
                        offer = float(offerStr)
                        self._rates[instrumentName] = {RepoRateHelper.bid: bid, RepoRateHelper.offer: offer}
                        
                    else:
                        instrumentName = row['Instrument']
                        bid = bidStr = None
                        offerStr =row['Offer']
                        offer = float(offerStr)
                        self._rates[instrumentName] = {RepoRateHelper.bid: bid, RepoRateHelper.offer: offer} # missing {RepoRateHelper.bid: bid} this might be a problem further down 
                        
                except Exception, ex:
                    raise Exception('The rates [%(bid)s, %(offer)s] for [%(instrument)s] is invalid, please correct it in the file [%(filepath)s]: %(exception)s' % \
                        {'bid': bidStr, 'offer': offerStr, 'instrument': instrumentName, 'filepath': self._filepath, 'exception': str(ex)})
        
        self._read = True
        
    def getRepoRates(self, instrument, bidOrOffer):
        if not self._read:
            self._readRates()

        key = instrument.Name()
        if self._rates.has_key(key):
            try:
                return self._rates[key][bidOrOffer]
            except KeyError:
                acm.Log("Unable to obtain {0} rate for {1}".format(bidOrOffer, key))
                return None
        else:
            return None
            
class Position:
    
    def __init__(self, portfolio, instrument, amount, rate):
        self.portfolio = portfolio
        self.instrument = instrument
        self.amount = amount
        self.rate = rate
            
class CapMarketBuySellBack:

    def __init__(self, ratesFilepath, tradeFilter, aquiringPortfolio, startDate, endDate, valGroup, bidAdjustment, offerAdjustment):
        self._tradeFilter = tradeFilter
        self._aquiringPortfolio = aquiringPortfolio
        self._startDate = aelDateToAcm(startDate)
        self._startDateAel = startDate
        self._endDate = aelDateToAcm(endDate)
        self._positions = []
        self._ratesFilepath = ratesFilepath
        self._rateHelper = RepoRateHelper(ratesFilepath)
        self._valuationGroup = valGroup
        self._bidAdjustment = bidAdjustment
        self._offerAdjustment = offerAdjustment
        

    def _buildPositions(self):
        portfolioPositions = {}
        bookings = []
        portfolioGrouper = acm.FAttributeGrouper('Trade.Portfolio')
        underlyingGrouper = acm.FAttributeGrouper('Underlying')
        calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
        calc_space.SimulateGlobalValue('Valuation Date', self._startDate)
        
        top_node = calc_space.InsertItem(self._tradeFilter)
        top_node.ApplyGrouper(acm.FChainedGrouper([underlyingGrouper, portfolioGrouper]))
        calc_space.Refresh()
        
        positionColumn = 'Portfolio Inventory'
        time_buckets = acm.Time.CreateTimeBuckets(self._startDate, "'0d'", None, None, 0, True, False, False, False, False)
        column_config = acm.Sheet.Column().ConfigurationFromTimeBuckets(time_buckets)
            
        instrumentIterator = top_node.Iterator().FirstChild()                       
        
        while instrumentIterator:
            instrument = acm.FInstrument[instrumentIterator.Tree().Item().StringKey()]
            if instrument and instrument.InsType() in ('Bond', 'IndexLinkedBond', 'SecurityLoan'):
                portfolioIterator = instrumentIterator.Clone().FirstChild()
                while portfolioIterator:
                    portfolio = acm.FPhysicalPortfolio[portfolioIterator.Tree().Item().StringKey()]
                    if portfolio:
                        value = calc_space.CreateCalculation(portfolioIterator.Tree(), positionColumn, column_config).Value()
                        isNumber, value = _isNumber(value)
                        if isNumber:
                            amount = float(value)
                            roundedAmount = round(amount, 2)
                            if roundedAmount != 0.00:
                                if portfolioPositions.get(portfolio.Name(), False):
                                    portfolioPositions[portfolio.Name()] = portfolioPositions[portfolio.Name()]+roundedAmount
                                else:
                                    portfolioPositions[portfolio.Name()] = roundedAmount
                                row = (portfolio, instrument, amount)
                                bookings.append(row)
                    portfolioIterator = portfolioIterator.NextSibling()
            instrumentIterator = instrumentIterator.NextSibling()

        totalPosition = sum(portfolioPositions.values())

        for portfolio, instrument, amount in bookings:
            rateType = RepoRateHelper.bid if totalPosition >= 0.00 else RepoRateHelper.offer 
            specificRate = self._rateHelper.getRepoRates(instrument, rateType)
            if specificRate:
                self._positions.append(Position(portfolio, instrument, amount, round(specificRate, 6)))
            else:
                acm.Log('    Skipping instrument [%(instrument)s] %(prf)s amount %(am)s : no %(type)s rate in file [%(file)s].' % \
                            {'instrument': instrument.Name(), 'file': self._ratesFilepath, 'type': str(rateType), 'am': amount, 'prf': portfolio.Name()})
                    
            
    def _getTradeArea(self, portfolio):
        tradeArea = {
             'JOB1':       'SPT001'
            ,'JOBX1':      'SPT001'
            ,'JOB2':       'SPT002'
            ,'JOB4':       'SPT004'
            ,'JOB5':       'SPT005'
            ,'JOB8':       'SPT008'
            ,'JOB10':      'SPT010'
            ,'JOB11':      'SPT011'
            ,'DERV':       'DER001'
            ,'DERV2':      'DER002'
            ,'DERV3':      'DER003'
            ,'MAN_BOND':   'MAN_Bond'
            ,'MAN_BOND_2': 'MAN_Bond'
        }
        
        key = portfolio.Name()
        if tradeArea.has_key(key):
            return acm.FChoiceList.Select01('list = "TradArea" and name = "%s"' % tradeArea[key], 'More than one Trade Area returned: %s' % tradeArea[key])
        else:
            return acm.FChoiceList.Select01('list = "TradArea" and oid = 0', '')
    
    def  _refPrice(self, ins):
        if not hasattr(self, "_spreads"):
            # Initialise the dict of spreads 
            spreadCurve = acm.FYieldCurve['ZAR-CORPBONDS-SPREADS']
            # cache: ins -> spread record
            self._spreads = dict([(spread.Instrument(), spread) 
                              for spread in spreadCurve.InstrumentSpreads()])
            
        finalPrice = 0
        if ins in self._spreads:
            spread = self._spreads[ins]
            if not spread.Benchmark():
                raise RuntimeError("Instrument %s is listed in spread curve,"
                                   " but doesn't have a benchmark" % ins.Name())
            finalPrice = (spread.Benchmark().used_price() + spread.Spread()
                          / ins.Quotation().QuotationFactor())
        else:
            finalPrice = ins.used_price()
        # if no price is defined, used_price() returns nan
        if math.isnan(finalPrice):
            raise RuntimeError("Invalid price for instrument %s"
                               % ins.Name())
        return finalPrice 
        
    
    def _createBuySellBackInstrument(self, rate, underlying, businessLogicHandler):
        instrument = acm.FBuySellBack()
        decorator = acm.FBuySellBackDecorator(instrument, businessLogicHandler)
        decorator.StartDate(self._startDate)
        decorator.ExpiryDate(self._endDate)
        decorator.Rate(rate)
        decorator.Underlying(underlying)
        decorator.DayCountMethod('Act/365')
        decorator.RefPrice(self._refPrice(underlying))
        quotationFactor = instrument.Quotation().QuotationFactor()
        decorator.RefValue(instrument.ContractSize() / (instrument.RefPrice() * quotationFactor))
        decorator.ValuationGrpChlItem(self._valuationGroup)
        instrument.Commit()
        return instrument, decorator
        
    def _bookBuySellBackTrade(self, portfolio, underlying, amount, rate, businessLogicHandler): 
        if portfolio.Name() == 'JOB15':
            portfolio = acm.FPhysicalPortfolio['JOB14']
            if not portfolio:
                raise Exception('Could not load portfolio [JOB14].')
        
        instrument, instrumentDecorator = self._createBuySellBackInstrument(rate, underlying, businessLogicHandler)
        trade = acm.FTrade()
        tradeDecorator = acm.FTradeLogicDecorator(trade, businessLogicHandler)
        tradeDecorator.Instrument(instrument)
        tradeDecorator.Currency(instrument.Currency())
        tradeDecorator.TradeTime(min(self._startDate, acm.Time().DateNow()))
        tradeDecorator.Acquirer(self._aquiringPortfolio.PortfolioOwner())
        tradeDecorator.Portfolio(self._aquiringPortfolio)  
        tradeDecorator.Counterparty(portfolio.PortfolioOwner())
        tradeDecorator.AcquireDay(self._startDate)
        tradeDecorator.ValueDay(self._startDate)
        tradeDecorator.HaircutType('Discount')
        tradeDecorator.Quantity(float(amount)/instrument.ContractSize())
        tradeDecorator.Status('Simulated')
        tradeDecorator.Text1('Booked cm_BuySellBackProcess')
        tradeDecorator.Price(self._refPrice(underlying))
        tradeDecorator.OptKey1(acm.FChoiceList.Select01('list = "TradArea" and name = "SPT006"', 'More than one Trade Area returned: SPT006'))
        tradeDecorator.PremiumCalculationMethod('Consideration')
        tradeDecorator.Trader(acm.User())
        tradeDecorator.MirrorPortfolio(portfolio)
        
        trade.Commit()
        
        '''These calculations aren't available in ACM, therefore accessing them using the AEL trade object'''
        ael_trade = ael.Trade[trade.Oid()]
        tradeDecorator.Premium(ael_trade.premium_from_quote(self._startDateAel, trade.Price()))
        trade.Commit()
        
        instrumentDecorator.RefPrice(ael_trade.buy_sellback_ref_price())
        instrumentDecorator.RefValue(ael_trade.buy_sellback_ref_value())
        instrument.Commit()
        
        mirrorTrade = trade.MirrorTrade()
        mirrorTrade.OptKey1(self._getTradeArea(portfolio))
        mirrorTrade.Commit()
        
        return trade.Oid(), mirrorTrade.Oid()
        
    def _processPositions(self):
        if not self._positions:
            acm.Log('    No positions to book for.')
            return

        businessLogicGUIDefaultHandler = acm.FBusinessLogicGUIDefault()
        for position in self._positions:
            try:
                tradeNumber, mirrorNumber = self._bookBuySellBackTrade(position.portfolio, position.instrument, position.amount, position.rate, businessLogicGUIDefaultHandler)
                acm.Log('    Booked Buy-Sell-Back for portfolio [%(portfolio)s], instrument [%(instrument)s], amount [%(amount)f]: %(tradeNumber)i, %(mirrorNumber)i' % \
                    {'portfolio': position.portfolio.Name(), 'instrument': position.instrument.Name(), 'amount': position.amount, 'tradeNumber': tradeNumber, 'mirrorNumber': mirrorNumber})
            except Exception, ex:
                acm.Log('    Could not process portfolio [%(portfolio)s], instrument [%(instrument)s], amount [%(amount)f]: %(ex)s' % \
                    {'portfolio': position.portfolio.Name(), 'instrument': position.instrument.Name(), 'amount': position.amount, 'ex': str(ex)})
            
    def run(self):
        acm.Log('Starting Capital Markets Buy-Sell-Back process at %s' % str(acm.Time().TimeNow()))
        acm.Log('  Counterparty Trade Filter: %s' % self._tradeFilter.Name())
        acm.Log('  Aquiring Portfolio: %s' % self._aquiringPortfolio.Name())
        acm.Log('  Start Date: %s' % str(self._startDate))
        acm.Log('  End Date: %s' % str(self._endDate))
        
        if not os.access(self._ratesFilepath, os.R_OK):
            acm.Log('  Aborting process: cannot access rates file [%s].' % self._ratesFilepath)
        else:
            acm.Log('  Reading positions...')
            self._buildPositions()
            
            acm.Log('  Booking Trades...')
            self._processPositions()
    
        acm.Log('Capital Markets Buy-Sell-Back process completed at %s' % str(acm.Time().TimeNow()))

