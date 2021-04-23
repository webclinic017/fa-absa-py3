""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_position_rolls/etc/FFxSwapRateFixingPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FFxSwapRateFixingPerform - Module which calculates and stores 
    points on mapped swap funding instruments

DESCRIPTION
    
----------------------------------------------------------------------------"""

import acm
import ael

from FBDPCurrentContext import Logme
import FFxCommon
import FFxSpotRolloverPerform
OVERNIGHT = 'ON'
TOMNEXT = 'TN'
SPOTNEXT = 'SN'
SUFFIXES = [OVERNIGHT, TOMNEXT, SPOTNEXT]

def perform_swap_rate_fixing(args):
    f = FFxSwapRateFixingPerform()
    f.perform(args)

class FFxSwapRateFixingPerform(object):

    def __init__(self):
        self.calcSpace   = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        self.yearsBetween = acm.GetFunction('yearsBetween', 4)
    
    def perform(self, ael_dict):
        market = None
        self.deposits = self.getDeposits(ael_dict)
        self.fxSwaps = self.getFXSwaps(ael_dict)
        
        if ael_dict['market']:
            market = ael_dict['market'][0]
        
        if ael_dict['calendar']:
            self.defaultCalendar = ael_dict['calendar'][0]
        
        self.fixRates(self.fxSwaps, market)
    
    def calculatePoints(self, bidAsk, currencyPair, market, nearDate, farDate, suffix):
        
        if bidAsk == 'Bid':
            ccy1BidAsk = 'Ask'
            ccy2BidAsk = 'Bid'
        elif bidAsk == 'Ask':
            ccy1BidAsk = 'Bid'
            ccy2BidAsk = 'Ask'
            
        ccy1Rate = self.getRate(currencyPair.Currency1(), market, nearDate, farDate, ccy1BidAsk, suffix)
        Logme() ('Rate for "%s" to "%s" for "%s" is: %s' %
        (nearDate, farDate, currencyPair.Currency1().Name(), str(ccy1Rate)), 'DEBUG')
        ccy2Rate = self.getRate(currencyPair.Currency2(), market, nearDate, farDate, ccy2BidAsk, suffix)
        Logme() ('Rate for "%s" to "%s" for "%s" is: %s' %
        (nearDate, farDate, currencyPair.Currency2().Name(), str(ccy2Rate)), 'DEBUG')
        spotFXDate = currencyPair.SpotDate(acm.Time().DateToday())
        spotFXRate = FFxCommon.getFxRate(spotFXDate, currencyPair.Currency1(), currencyPair.Currency2())
        Logme() ('Spot FX Rate for "%s" for "%s" is: %s' %(spotFXDate, 
                currencyPair.Name(), str(spotFXRate)), 'INFO')
        dayCountMethod = self.getDayCountBasis(currencyPair)
        calendar = self.getCalendar(currencyPair)
        dayCountFraction = self.yearsBetween(nearDate, farDate, dayCountMethod, calendar)
        
        Logme() ('DayCountFraction is "%s"' %(dayCountFraction), 'DEBUG')
        points = spotFXRate * (ccy2Rate - ccy1Rate)*dayCountFraction/((1+ccy1Rate*dayCountFraction)*currencyPair.PointValue())
        if nearDate < spotFXDate:
            points *= -1
        
        Logme() ('"%s" "%s" points for "%s" are "%s"' %(suffix, bidAsk, currencyPair.Name(), points), 'INFO')
        return points
    
    def getCalendar(self, instrument):
        if type(instrument) == type(acm.FCurrencyPair()):
            calendar = instrument.SpotCalendar()
        else:
            calendar = instrument.Calendar()
        if not calendar:
            calendar = self.defaultCalendar
        
        return calendar
    
    def getDayCountBasis(self, currencyPair):
        dayCount1 = currencyPair.Currency1().DayCountMethod()
        dayCount2 = currencyPair.Currency2().DayCountMethod()
        if dayCount1 != dayCount2:
            if dayCount1 == 'Act/360':
                dayCount = dayCount2
            else:
                dayCount = dayCount1
        else:
            dayCount = dayCount1
        Logme() ('Using daycount method: "%s"' %(dayCount), 'DEBUG')
        return dayCount
    
    def getRate(self, curr, market, nearDate, farDate, bidAsk, suffix):
        deposit = self.getDeposit(curr, nearDate, farDate, suffix)
        if deposit:
            try:
                rate = self.getDepositRate(deposit, market, bidAsk)/100
            except Exception, e:
                print str(e)
                rate = 0.0
            return rate
        else:
            Logme() ('"%s" Deposit could not be found for: "%s"' %(suffix, curr.Name()), 'INFO')
            return 0.0
    
    def getFXSwaps(self, ael_dict):
        fxSwaps = []
        if 'fxSwaps' in ael_dict:
            fxSwaps = ael_dict['fxSwaps']
            if len(fxSwaps) > 0:
                return fxSwaps
        
        
        if 'fxSwapPrefix' in ael_dict:
            fxSwap_prefix = ael_dict['fxSwapPrefix']
            currencyPairs = acm.FCurrencyPair.Select('')
            fxSwaps = []
            for currencyPair in currencyPairs:

                for suffix in SUFFIXES:
                    fxSwapName = fxSwap_prefix + '_' + currencyPair.Name() + '_' + suffix
                    fxSwap = acm.FFxSwap[fxSwapName]
                    if fxSwap is None:
                        
                        fxSwap = self.create_fx_swap(fxSwapName, currencyPair.Currency1(),
                            currencyPair.Currency2(), suffix)
                    fxSwaps.append(fxSwap)
            
            return fxSwaps
    
    def getDepositNames(self, prefix):
        
        depositNames = {}
        
        currencies = acm.FCurrency.Select('')
        
        for currency in currencies:
            depositName = prefix + '_' + currency.Name()
            for suffix in SUFFIXES:
                depositNames[depositName + '_' + suffix] = currency
        
        return depositNames
    
    def getDeposits(self, ael_dict):
        
        deposits = []
        if 'deposits' in ael_dict:
            deposits = ael_dict['deposits']
            if len(deposits) > 0:
                return deposits
        
        if 'depositPrefix' in ael_dict:
            deposits = []
            prefix = ael_dict['depositPrefix']
            depositNames = self.getDepositNames(prefix)
            for depositName in depositNames:
                deposit = acm.FDeposit[depositName]
                currency = depositNames[depositName]
                if not deposit:
                    deposit = self.createDeposit(currency, depositName)
                deposits.append(deposit)
            acm.PollDbEvents()
            return deposits
    
    def createDeposit(self, currency, depositName):
        #get the near date far date
        nearDate, farDate = self.getNearAndFarDates(currency, depositName)
        return self.createDepositInstrument(currency, depositName, 100000, 0.0,
            nearDate, farDate)
    
    def getDeposit(self, curr, nearDate, farDate, suffix):
        if not self.deposits:
            raise Exception('No deposit Instruments.')
        for deposit in self.deposits:
            if deposit.Currency() != curr:
                continue
            if deposit.Name()[-2:] == suffix:
                return deposit
        
    def getDepositRate(self, deposit, market, bidAsk):
        price = self.get_last_price(deposit, market)
        if not price:
            raise Exception('Deposit ' + deposit.Name() + ' has no prices.')
        if bidAsk == 'Bid':
            return price.Bid()
        elif bidAsk == 'Ask':
            return price.Ask()
       
    def fixRate(self, fxSwap, market, currencyPair, nearDate, farDate):
        suffix = fxSwap.Name()[-2:]
        bidPoints = self.calculatePoints('Bid', currencyPair, market, nearDate, farDate, suffix)
        askPoints = self.calculatePoints('Ask', currencyPair, market, nearDate, farDate, suffix)

        price     = self.get_last_price(fxSwap, market)
        
        if price == None:
            price = acm.FPrice()
            price.Instrument(fxSwap)
            price.Market(market)

        price.Day(acm.Time().DateToday())
        price.Currency(fxSwap.Currency())
        price.Bid(bidPoints)
        price.Ask(askPoints)
        
        try:    
            price.Commit()
        except Exception, e:
            Logme() ('Failed to save price for %s for reason: %s' %(fxSwap.Name(), e), 'DEBUG')
            pass
        return
        
    def getNearAndFarDates(self, instrument, depositName):
    
        suffix = depositName[-2:]
        today = acm.Time().DateToday()
        calendar = self.getCalendar(instrument)
        nearDate = today
        if suffix == OVERNIGHT:
            nearDate = today
        elif suffix == TOMNEXT:
            nearDate = calendar.AdjustBankingDays(today, 1)
        elif suffix == SPOTNEXT:
            nearDate = calendar.AdjustBankingDays(today, instrument.SpotBankingDaysOffset())
        farDate = calendar.AdjustBankingDays(nearDate, 1)
        return nearDate, farDate

    def fixRates(self, fxSwaps, market):
        
        for fxSwap in fxSwaps:
            if not fxSwap:
                continue
            
            curr1           = fxSwap.Legs()[0].Currency()
            curr2           = fxSwap.Legs()[1].Currency()
            currencyPair    = curr1.CurrencyPair(curr2)
            
            nearDate, farDate = self.getNearAndFarDates(currencyPair, fxSwap.Name())
            
            self.fixRate(fxSwap, market, currencyPair, nearDate, farDate)
            
    def get_last_price(self, instrument, market):
        prices = instrument.Prices()
        if len(prices) > 0:
            return prices[0]
        else:
            histPrices = instrument.HistoricalPrices()
            last = None
            for hp in histPrices:
                if hp.Market() == market and hp.Currency() == instrument.Currency():
                    if hp.Day() == acm.Time().DateToday():
                        last = hp
                        break
                    # Find latest available before MtM date
                    if hp.Day() < acm.Time().DateToday():
                        if not last:
                            last = hp
                        elif hp.Day() > last.Day():
                            last = hp
            return last
    
    def create_fx_swap(self, name, curr1, curr2, suffix):

        s = acm.FFxSwap()
        s.Name(name)
        s.Generic(True)
        s.Currency(curr1)
        #s.ContractSize(10000)
        s.Quotation('Per Contract')
        today = acm.Time().DateToday()
        s.StartDate(today)
        expiry_period = 1
        if suffix == OVERNIGHT:
            expiry_period = 1
        elif suffix == TOMNEXT:
            expiry_period = 2
        elif suffix == SPOTNEXT:
            expiry_period = 3
        else:
            raise Exception('unknown suffix for FX Swap')
        s.ExpiryPeriod_unit(1)
        s.ExpiryPeriod_count(expiry_period)
        
        expiry = acm.Time().DateAddDelta(today, 0, 0, expiry_period)
        leg1 = s.CreateLeg(1)
        leg1.NominalFactor(1)
        leg1.Currency(curr1)
        leg1.StartDate(today)
        leg1.EndDate(expiry)
        leg1.FixedRate(0)
        leg1.FixedCoupon(0)
        leg1.LegType('Fixed')
        leg1.DayCountMethod('Act/360')

        leg2 = s.CreateLeg(0)
        leg2.NominalFactor(1)
        leg2.Currency(curr2)
        leg2.StartDate(today)
        leg2.EndDate(expiry)
        leg2.FixedRate(0)
        leg2.FixedCoupon(0)
        leg2.LegType('Fixed')
        leg2.DayCountMethod('Act/360')
        s.Commit()
        Logme() ('Created FX Swap: %s' %(s.Name()), 'INFO')
        return s
    
    def createDepositInstrument(self, currency, name, contractSize, rate, fromDate,
                         toDate):
        """
        Return an newly created deposit instrument with the given parameters.
        """

        ins = acm.FDeposit()
        ins.Name(name)
        ins.Generic(True)
        ins.Currency(currency)
        ins.Quotation('Coupon')
        ins.ContractSize(contractSize)

        # Create the receive leg
        receiveLeg = ins.CreateLeg(False)
        receiveLeg.LegType('Fixed')
        receiveLeg.Currency(currency)
        receiveLeg.ResetType('None')
        receiveLeg.StartDate(fromDate)
        receiveLeg.AmortStartDay(fromDate)
        receiveLeg.RollingPeriodBase(fromDate)
        receiveLeg.EndDate(toDate)
        receiveLeg.AmortEndDay(toDate)
        receiveLeg.FixedRate(rate)

        # The new deposit instrument's rounding specification should be that of
        # the default deposit instrument.  If it is not defined, use that of
        # the currency
        roundingSpec = None
        depositDefaultIns = acm.FDeposit['DepositDefault']
        if depositDefaultIns is not None:
            roundingSpec = depositDefaultIns.RoundingSpecification()
        if roundingSpec is None:
            roundingSpec = currency.RoundingSpecification()
        if roundingSpec is not None:
            ins.RoundingSpecification(roundingSpec)
        ins.Commit()
        Logme() ('Created Deposit: %s' %(ins.Name()), 'INFO')
        return ins

