""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_options/etc/FPriceFixingPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
    (c) Copyright 2017 SunGard Front Arena. All rights reserved.
----------------------------------------------------------------------------"""
"""----------------------------------------------------------------------------
MODULE
    FPriceFixingPerform - Stores price fixings/cut time prices into internal
            markets.

----------------------------------------------------------------------------"""


import time
import calendar
import traceback
import zoneinfo
import math


import acm
import ael
from ArenaFunctionBridge import instrument_used_price
from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme
from datetime import date


dateFormatString = "%Y-%m-%d"
dateTimeFormatString = "%Y-%m-%d %H:%M:%S"
RET_OK = 1
RET_TIMEOUT = 2
RET_FAIL = 3


def formatAelPrice(price):

    return ('%s  %s/%s \n\t Last: %10.4f\n\t Settle: %10.4f\n\t'
        % (price.ptynbr.ptyid, price.insaddr.insid, price.curr.insid,
           price.last, price.settle))


def formatAcmPrice(price):

    return ('%s  %s/%s \n\t Last: %10.4f\n\t Settle: %10.4f\n\t'
            % (price.Market().Name(), price.Instrument().Name(),
            price.Currency().Name(), price.Last(), price.Settle()))


def hoursAndMinutesFromInt(timevalue):

    minutes = timevalue % 100
    hours = (timevalue - minutes) / 100
    return hours, minutes


def secondsFromInt(timevalue):

    hours, minutes = hoursAndMinutesFromInt(timevalue)
    return float(hours * 60 * 60 + minutes * 60)


def getLastPrice(fixingSource, instrument, currency, date):

    whereClause = ("instrument=%d and day='%s' and currency=%d and market=%d" %
            (instrument.Oid(), date, currency.Oid(), fixingSource.Oid()))
    Logme()('Getting the last price where: %s' % (whereClause), 'DEBUG')
    price = acm.FPrice.Select01(whereClause, 'Price not found for "%s".' %
            (whereClause))
    return price


def getCutoffTime(parameters):

    fixingSource = parameters['fixing_source'][0]
    # Convert the market cutoff time from its local timezone to universal time.
    externalCutOffHoursMinutes = fixingSource.ExternalCutOff()
    hours, minutes = hoursAndMinutesFromInt(externalCutOffHoursMinutes)
    fixingSourceTimeZone = fixingSource.TimeZone()
    fixingSourceTimeZoneData = zoneinfo.getZone(fixingSourceTimeZone)
    if not fixingSourceTimeZoneData:
        Logme()('Invalid TimeZone Data.', 'ERROR')
        return RET_FAIL, 0, 0
    # Build the cutoff time from the universal date plus the external cutoff;
    # but this is in the market's local timezone.
    utc = time.gmtime()
    marketCutoffTime = (utc[0], utc[1], utc[2], hours, minutes, 0, utc[6],
            utc[7], utc[8])
    marketCutoffTimeSeconds = calendar.timegm(marketCutoffTime)
    # Convert to universal time from the market's local time,
    # by pretending to convert from universal time to the market's local time.
    universalCutoffTime = zoneinfo.zonetime(fixingSourceTimeZoneData,
            marketCutoffTimeSeconds)
    universalCutoffTimeSeconds = calendar.timegm(universalCutoffTime)
    # The time offset thus obtained has the right magnitude, but the wrong
    # sign; it must then be REVERSED to actually convert from the market's
    # local time to universal time.
    timeOffsetSeconds = marketCutoffTimeSeconds - universalCutoffTimeSeconds
    universalCutoffTimeSeconds = marketCutoffTimeSeconds + timeOffsetSeconds
    universalCutoffTime = time.gmtime(universalCutoffTimeSeconds)
    localCutoffTime = time.localtime(universalCutoffTimeSeconds)
    market = None
    marketName = None
    if parameters['market']:
        market = parameters['market'][0]
        marketName = market.Name()
        Logme()('Market:                                   %s' % (marketName))
    Logme()('Fixing source:                            %s' %
            (fixingSource.Name()))
    Logme()('Fixing source cutoff time:                %02d:%02d' %
            (hours, minutes))
    Logme()('Fixing source timezone:                   %s' %
            (fixingSourceTimeZone))
    Logme()('Fixing source cutoff (market local time): %s' %
            ((time.strftime(dateTimeFormatString, marketCutoffTime))))
    Logme()('Fixing source cutoff (universal time):    %s' %
            ((time.strftime(dateTimeFormatString, universalCutoffTime))))
    Logme()('Fixing source cutoff (Prime local time):  %s' %
            ((time.strftime(dateTimeFormatString, localCutoffTime))))
    return RET_OK, universalCutoffTime, localCutoffTime


def onPriceChange(priceTable, price, priceFix, operation):
    """
    Subscribes to price updates that will be committed up to
    but not after the cutoff time, if they match the task parameters.
    """
    # filter operation
    if operation == 'delete':
        Logme()('Ignoring deleted price updates.', 'DEBUG')
        return
    try:
        market = acm.FParty[price.ptynbr.ptyid]
        # filter running without market param
        if not priceFix.market:
            Logme()('Ignoring price update, no market specified.', 'DEBUG')
            return
        elif priceFix.market.Oid() != market.Oid():
            Logme()('Ignoring price update, market "%s" does not match.' %
                    (market.Name()), 'DEBUG')
            return
        instrument = acm.FInstrument[price.insaddr.insid]
        currency = acm.FInstrument[price.curr.insid]
        currencyPair = acm.FCurrencyPair.Select01(
                "currency1='%s' and currency2='%s'" % (instrument.Oid(),
                currency.Oid()), 'Currency pair not found.')
        if ((currencyPair not in priceFix.currencyPairs) and
                (instrument not in priceFix.instruments)):
            Logme()('Ignoring price update, instrument "%s" does not match.' %
                    (instrument.Name()), 'DEBUG')
            return
        # Determine a good last price using last, or mid, or bid or ask.
        last = price.last
        if last == 0.0:
            if price.bid == 0.0:
                last = price.ask
            elif price.ask == 0.0:
                last = price.bid
            else:
                last = (price.bid + price.ask) / 2.0  # Both m/b nonzero.
        Logme()('Real-time price: \n\t %s' % (formatAelPrice(price)))
        priceFix.fixPrice(priceFix.fixingSource, instrument, currency,
                priceFix.universalCutoffTime, last)
    except:
        traceback.print_exc()
        priceFix.cleanup()
        raise


def perform_fixing(parameters):
    r = PriceFixing()
    r.perform(parameters)
    Summary().log(parameters)
    Logme()(None, 'FINISH')


def num(s):
    try:
        return float(s)
    except:
        return 0


class PriceFixing(object):

    def validateParameters(self, parameters):

        if not parameters['currency_pairs'] and not parameters['instruments']:
            Logme()('Invalid parameters, no currency pairs specified and no '
                    'instruments specified.', 'ERROR')
            return False

        loginDate = acm.Time.DateToday()
        todayDate = date.today().isoformat()
        if loginDate < todayDate:
            utc = time.gmtime()
            self.universalCutoffTime = (utc[0], utc[1], utc[2], \
                23, 59, 59, utc[6], utc[7], utc[8])
            self.fixedDate = ael.date_today()
            return True

        ret, universalCutoffTime, localCutoffTime = getCutoffTime(parameters)
        self.universalCutoffTime = universalCutoffTime
        self.fixedDate = ael.date_from_time(
            int(time.mktime(self.universalCutoffTime)))
        if ret != RET_OK:
            return False
        return True

    def readArguments(self, parameters):

        self.fixingSource = parameters['fixing_source'][0]
        self.currencyPairs = (parameters['currency_pairs'] if
                'currency_pairs' in parameters else [])
        self.instruments = (parameters['instruments'] if
                'instruments' in parameters else [])
        self.market = (parameters['market'][0] if
                'market' in parameters and parameters['market'] else None)
        self.subscriptionTime = (parameters['subscribe_time'] if
                'subscribe_time' in parameters else 0)
        self.Testmode = (parameters['Testmode'] if
                'Testmode' in parameters else 0)
        self.tradeDate = acm.Time.DateToday()

    def perform(self, parameters):
        """
        Subscribes to price updates from the external market; requests prices
        from that market for designated currency pairs (or other instruments);
        continues to receive updated prices; updates an internal market (the
        fixing source) with the latest price until the cutoff time has passed
        or the subscription times out, whichever comes first.
        """
        self.readArguments(parameters)
        if not self.validateParameters(parameters):
            return

        Logme()('', 'NOTIME')
        ael.Price.subscribe(onPriceChange, self)
        self.cleanup = lambda: ael.Price.unsubscribe(onPriceChange, self)
        try:
            if (self.processInstruments(self.instruments) == RET_OK and
                    self.processInstruments(self.currencyPairs) == RET_OK):
                self.processSubscription()
        finally:
            self.cleanup()

    def processInstruments(self, instruments):

        numOfIns = len(instruments)
        count = 0
        insType = 'Currency Pair'

        class DummyPrice:
            def RecordType(self):
                return "Price"

        p = DummyPrice()
        while time.gmtime() <= self.universalCutoffTime and count < numOfIns:
            ins = instruments[count]
            count = count + 1
            if ins.IsKindOf(acm.FCurrencyPair):
                name = ins.Name()
                instrument = ins.Currency1()
                currency = ins.Currency2()
            else:
                instrument = ins
                name = instrument.Name()
                currency = instrument.Currency()
                insType = instrument.InsType()

            if self.market:
                spotPrice = instrument_used_price(instrument.Name(),
                        self.tradeDate, currency.Name(), "Last", self.market)
                if (str(spotPrice) == '1.#QNAN' or math.isnan(spotPrice) or
                        math.isinf(spotPrice)):
                    Logme()('%s %s in %s market does not have used price:    '
                            '%10.4f.' % (insType, name, self.market.Name(),
                            spotPrice))
                    Summary().ignore(p, Summary().UPDATE,
                            'No used price in %s Market on %s' %
                            (self.market.Name(), self.tradeDate), ins.Name())
                    continue
                else:
                    Logme()('%s %s in %s market has used price:    %10.4f.' %
                            (insType, name, self.market.Name(), spotPrice))
            else:  # No market Default
                spotPrice = instrument_used_price(instrument.Name(),
                        self.tradeDate, currency.Name(), "Last")
                if (str(spotPrice) == '1.#QNAN' or math.isnan(spotPrice) or
                        math.isinf(spotPrice)):
                    Logme()('%s %s does not have used price:    %10.4f.' %
                            (insType, name, spotPrice))
                    Summary().ignore(p, Summary().UPDATE,
                            'No used price in any Market on %s' %
                            (self.tradeDate), ins.Name())
                    continue
                else:
                    Logme()('%s %s has used price:    %10.4f.' %
                            (insType, name, spotPrice))
            self.fixPrice(self.fixingSource, instrument, currency,
                    self.universalCutoffTime, spotPrice)
        if time.gmtime() > self.universalCutoffTime:
            Logme()('Passed cutoff for "%s".' % (self.fixingSource.Name()))
            return RET_TIMEOUT
        else:
            return RET_OK

    def processSubscription(self):

        count = 0
        numOfPolls = num(self.subscriptionTime) * 10
        while (time.gmtime() <= self.universalCutoffTime and count < numOfPolls
               and numOfPolls > 1):
            time.sleep(.1)
            ael.poll()
            count = count + 1
        if time.gmtime() > self.universalCutoffTime:
            Logme()('Passed cutoff for "%s".' % (self.fixingSource.Name()))
        else:
            Logme()('Subscription Time out')

    def fixPrice(self, fixingSource, instrument, currency, universalCutoffTime,
            spot):
        """
        Stores the spot price (last price, or (bid+ask)/2), or nonzero bid, ask
        for the instrument in the currency into the fixing source market, but
        not if the cutoff time has passed.
        """
        try:
            price = getLastPrice(fixingSource, instrument, currency,
                    self.fixedDate)
            if not price:
                price = acm.FPrice()
            price.Market(fixingSource)
            price.Instrument(instrument)
            price.Currency(currency)
            currentTime = time.gmtime()
            price.Day(self.fixedDate)
            price.Last(spot)
            price.Settle(spot)
            Logme()("Current time is:       %s" %
                    (time.strftime(dateTimeFormatString, currentTime)),
                    'DEBUG')
            Logme()("Market cutoff time is: %s" %
                    (time.strftime(dateTimeFormatString, universalCutoffTime)),
                    'DEBUG')
            if currentTime > universalCutoffTime:
                Logme()('Passed cutoff -- not fixing price: \n\t %s' %
                        (formatAcmPrice(price)))
            else:
                Logme()('Fixing price: \n\t %s' % (formatAcmPrice(price)))
                if not self.Testmode:
                    price.Commit()
                    Summary().ok(price, Summary().UPDATE)
        except:
            traceback.print_exc()
            self.cleanup()
            raise
