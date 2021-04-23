""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FExeAssPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FExeAssPerform - Module that executes ExerciseAssign.

DESCRIPTION
----------------------------------------------------------------------------"""

import time
import math
from collections import namedtuple


import acm
import ael
import FBDPCommon
import FFxCommon
import FBDPRollback
import FBDPCalculatePosition
import FBDPInstrument
import FFxCommon
import importlib
importlib.reload(FFxCommon)
from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme


# ====================== Calc space for Standard Calculations =================


space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()


# Attempt to get FBDPHook.exercise_trade,
# FBDPHook.additional_excercise_trades,
# FBDPHook.custom_exercise and
# FBDPHook.trade_status
exercise_trade_hook = None
additional_excercise_trades_hook = None
custom_exercise_hook = None
trade_status_hook = None

try:
    import FBDPHook
    importlib.reload(FBDPHook)
    exercise_trade_hook = FBDPHook.exercise_trade
except:
    Logme()('No FBDPHook.exercise_trade hook.', 'DEBUG')
try:
    import FBDPHook
    importlib.reload(FBDPHook)
    additional_excercise_trades_hook = FBDPHook.additional_excercise_trades
except:
    Logme()('No FBDPHook.additional_exercise_trades hook.', 'DEBUG')
try:
    import FBDPHook
    importlib.reload(FBDPHook)
    custom_exercise_hook = FBDPHook.custom_exercise
except:
    Logme()('No FBDPHook.custom_exercise hook.', 'DEBUG')
try:
    import FBDPHook
    importlib.reload(FBDPHook)
    trade_status_hook = FBDPHook.trade_status
except:
    Logme()('No FBDPHook.trade_status hook.', 'DEBUG')

#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------


TRADE_TIME = (21 * 60 * 60) - 1  # 20:59:59 seconds today

# Trading Manager columns for Asian options
AV_PRICE = "Asian Average Price So Far"
AV_STRIKE = "Asian Average Strike So Far"

# Logging levels
DEBUG = 'DEBUG'
INFO = 'INFO'
WARNING = 'WARNING'
ERROR = 'ERROR'

# Script actions and trade types for closing/ exercise/ assign trade
EXERCISE = 'Exercise'
ASSIGN = 'Assign'
ABANDON = 'Abandon'
CLOSE = 'Close'

# Settlement options
PHYSICAL_SETTLEMENT = "Physical Delivery"
CASH_SETTLEMENT = "Cash"
FORWARD_SETTLEMENT = 'Forward'

# Price modes for physical delivery
STRIKE_PRICE = 'Strike'
MARKET_PRICE = 'Market'

# Instrument types
BOND = 'Bond'
OPTION = 'Option'
WARRANT = 'Warrant'
FUTURES_FORWARD = 'Future/Forward'
CURRENCY = 'Curr'
COMMODITY = 'Commodity'
COMMODITY_INDEX = 'Commodity Index'
COMMODITY_VARIANT = 'Commodity Variant'
STOCK = 'Stock'
STOCK_INDEX = 'EquityIndex'
COMBINATION = 'Combination'

# Exercise types
EUROPEAN = 'European'
AMERICAN = 'American'

# Pay day offset methods
BUSINESS_DAYS = 'Business Days'
CALENDAR_DAYS = 'Calendar Days'
NO_OFFSET = 'None'

# Asian option price and strike types
AVERAGE = 'Average'
FIXED = 'Fix'
FLOAT = 'Float'
# Portfolio Average Price

TODAY = acm.Time().DateToday()

abandon_types = [OPTION, WARRANT, FUTURES_FORWARD, BOND, STOCK]

ClosingPrice = namedtuple('ClosingPrice', ['underlying', 'derivative'])

spaceCollection = acm.FStandardCalculationsSpaceCollection()
getObject = acm.GetFunction("getObject", 2)
perUnitQuotation = getObject(acm.FQuotation, "Per Unit")

def _tradeNumber(trade):
    try:
        trdnbr = trade.trdnbr
    except:
        trdnbr = trade.Oid()
    return trdnbr


def _getACMInstr(ins):
    instr = acm.FInstrument[ins.insid]
    if not instr:
        raise ValidationError('{0} has been archived.'.format(ins.insid))
    return instr


def _getColumnValue(calcSpace, nodeTree, column, instrument):
    try:
        calcObj = calcSpace.CreateCalculation(nodeTree, column)
        if not calcObj:
            Logme()('Could not get {0} for {1}. Returning 0.'.format(column,
                instrument.Name()), WARNING)
            return 0.
        # For some reason, options with geometric averages return a float,
        # while those with arithmetic ones return an FDenominatedValue...
        val = calcObj.Value()
        if isinstance(val, float):
            return val
        return val.Number()
    except Exception as e:
        Logme()('Invalid {0} found for {1}: {2}. Returning 0.'.format(column,
            instrument.Name(), e), WARNING)
    return 0.


def _convertStrikeQuote(value, option):
    if option.StrikeQuotation() == option.Underlying().Quotation():
        return value
    option = FBDPCommon.acm_to_ael(option)
    return convert_price_to_und_or_strike_quotation(option, value, 1)


def _getSettleDate(instrument, tradeDate, offset=None):
    if offset == None:
        offset = instrument.PayDayOffset()
    if instrument.PayOffsetMethod() == BUSINESS_DAYS:
        curr = instrument.Currency()
        if FBDPCommon.has_attr(instrument, 'StrikeCurrency'):
            curr = instrument.StrikeCurrency() or curr
        calendar = curr.Calendar()
        return calendar.AdjustBankingDays(tradeDate, offset)
    return acm.Time.DateAddDelta(tradeDate, 0, 0, offset)


def _getSettleDateAEL(ins, date, offset=None):
    instrument = FBDPCommon.ael_to_acm(ins)
    Date = FBDPCommon.toDate(str(date))
    settleDate = _getSettleDate(instrument, Date, offset)
    settleDateAEL = FBDPCommon.toDateAEL(str(settleDate))
    return settleDateAEL


def _getDeliveryDateAEL(ins, date, offset=None):
    acmIns = FBDPCommon.ael_to_acm(ins)
    if acmIns.IsKindOf(acm.FOption):
        if ins.exp_day <= date:
            return _getOptionDeliveryDate(ins)
        elif acmIns.UnderlyingType() == 'Curr':
            curr1 = acmIns.StrikeCurrency()
            curr2 = acmIns.Underlying()
            pair = FFxCommon.currencyPair(curr1, curr2)
            return FBDPCommon.toDateAEL(str(pair.SpotDate(date)))
    return _getSettleDateAEL(ins, date, offset)


def _getOptionDeliveryDate(ins):
    if not FBDPCommon.is_acm_object(ins):
        ins = FBDPCommon.ael_to_acm(ins)
    return FBDPCommon.toDateAEL(str(ins.DeliveryDate()))


def _getSpotOffset(ins):
    # if FX, try to get the currency pair
    if ins.und_instype == 'Curr':
        curr1 = FBDPCommon.ael_to_acm(ins.strike_curr)
        curr2 = FBDPCommon.ael_to_acm(ins.und_insaddr)
        pair = FFxCommon.currencyPair(curr1, curr2)
        if pair:
            return pair.SpotBankingDaysOffset()
    else:
        return ins.und_insaddr.pay_day_offset

def _getContractPrice(option, quote):
    underlying = option.Underlying()
    underlyingPrice = underlying.Calculation().PriceConvert(spaceCollection,
        quote, underlying.Quotation(), perUnitQuotation)
    return option.Calculation().PriceConvert(spaceCollection,
        underlyingPrice, perUnitQuotation, option.Quotation())

def _getClosingPrice(option, priceMode):

    if option.instrument.IsKindOf(acm.FCombination):
        return ClosingPrice(derivative=0, underlying=0.)

    payoff = option.settlePrice - option.strike
    if not option.instrument.IsCall():
        payoff = -payoff

    price = _getContractPrice(option.instrument, payoff)

    if option.instrument.SettlementType() == CASH_SETTLEMENT:
        return ClosingPrice(derivative=price, underlying=0.)

    # Physical settlement
    if priceMode == STRIKE_PRICE:
        return ClosingPrice(underlying=option.strike, derivative=0.)
    return ClosingPrice(underlying=option.settlePrice, derivative=price)

def _getLinkedTrade(posTrade, orgTrades, multiCurr):
    if posTrade.Oid() > 0:
        return posTrade
    if not multiCurr:
        return orgTrades[0]
    for t in orgTrades:
        if t.Currency() == posTrade.Currency():
            return t
    return posTrade


def _linkTrades(trade, link):
    trade.ConnectedTrade(link)
    trade.Contract(link)
    return trade


def _getPhysicalQuantity(posTrade, option):
    contractSize = option.PhysicalContractSize()
    if not contractSize:
        contractSize = option.ContractSize()
    underlying = option.Underlying().ContractSize()
    if underlying:
        contractSize = contractSize / underlying

    quantity = posTrade.Quantity() * contractSize
    if option.IsCallOption():
        return quantity
    return -quantity


def _getExerciseTradeType(trade):
    if trade.Quantity() > 0:
        return EXERCISE
    return ASSIGN


def _copyTrade(trade, linkTrade):
    dup = acm.FTrade()
    dup.Apply(trade)
    for p in [p for p in dup.Payments()]:
        p.Delete()
    dup.Payments().Clear()
    dup = _linkTrades(dup, linkTrade)
    return dup

def _createUnderlyingTrade(posTrade, linkTrade, tradeDate, settleDate, price):
    option = posTrade.Instrument()
    dup = _copyTrade(posTrade, linkTrade)
    dup.TradeTime(tradeDate)
    dup.ValueDay(settleDate)
    dup.AcquireDay(settleDate)
    tradeType = _getExerciseTradeType(posTrade)
    dup.Type(tradeType)

    dup.Instrument(option.Underlying())
    if dup.Instrument().InsType() == CURRENCY:
        dup.DefaultCLS()

    dup.Currency(option.StrikeCurrency())
    dup.Price(price)
    quantity = _getPhysicalQuantity(posTrade, option)
    dup.Quantity(quantity)
    dup.UpdatePremium(True)

    hook = trade_status_hook
    if hook:

        # Customized behavior
        dup.status(hook(tradeType, dup, isPreview=False))

    return dup

def _createPayment(payDay, amount, currency, party):
    payment = acm.FPayment()
    payment.Type('Cash')
    payment.Currency(currency)
    # roundingForCurrency = self.getPremiumRounding(sweepCurrency)
    payment.Amount(amount)
    payment.ValidFrom(acm.Time.DateToday())
    payment.PayDay(payDay)
    payment.Party(party)
    return payment

def _logZeroPosition(trade, option):
    Logme()('Skipping zero position: {0}:{1}.'.format(trade.Portfolio().Name(),
        option.instrument.Name()), 'DEBUG')


def _logExerciseCondition(option, exercise):
    Logme()(50 * '-', DEBUG)
    msg = ("{0} option \'{1}\' should be {2}:".format(
            ('Put', 'Call')[option.instrument.IsCallOption()],
            option.instrument.Name(),
            ('abandoned', 'exercised/assigned')[exercise]))
    Logme()(msg, DEBUG)
    Logme()("Settle price = {0}".format(option.settlePrice), DEBUG)
    Logme()("Strike price = {0}".format(option.strike), DEBUG)
    Logme()(50 * '-', DEBUG)


def _isTradedOnOrBeforeExerciseDate(acmTrade, strIsoExeDate):

    strIsoTradeTime = acmTrade.TradeTime()
    strIsoTradeDate = strIsoTradeTime[:10]
    return strIsoTradeDate <= strIsoExeDate

def _createOption(ins, preview, settleMarket):
    """
    Initializing method for creating exercise/ assign Option
    classes. Add to this method if creating new Option types for use in the
    new run() loop.
    """
    if isAsianOption(ins):
        return AsianOption(ins, preview, settleMarket)
    elif isCliquetOption(ins):
        return CliquetOption(ins, preview, settleMarket)
    elif isCombination(ins):
        return Combination(ins, preview, settleMarket)
    return BaseOption(ins, preview, settleMarket)

class ValidationError(Exception):
    """
    Exception class for raising user errors e.g. invalid arguments and other
    preconditions for running the script.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BaseOption(object):
    """
    Base class for new option types, to be used in new Exercise.run()
    loop. Provides the required methods called in the loop.
    """
    def __init__(self, ins, preview=0, market=''):
        self.instrument = _getACMInstr(ins)
        assert self.instrument.IsKindOf(acm.FOption), ("{0} ({1}) is not an "
                "Option.".format(self.instrument.Name(),
                    self.instrument.InsType()))
        self.preview = preview
        self.strike = self.instrument.StrikePrice()
        self.settlePrice = 0.
        if market:
            self.market = acm.FParty[market]
        else:
            self.market = self.instrument.FixingSource()

    def canExercise(self, exDate):
        """
        Returns true by default (i.e. assumes option is American), and for
        expired European options. Options with other exercise conditions should
        redefine this method accordingly.
        """
        if self.instrument.ExerciseType() != 'European':
            return True
        return acm.Time().DateDifference(self.instrument.ExpiryDate(),
                exDate) <= 0

    def shouldExercise(self, exDate, settlePrice=0.):
        if not self.canExercise(exDate):
            return False

        if not self.settlePrice:
            self.settlePrice = self.getSettlePrice(exDate, settlePrice)
            if not self.settlePrice:
                return False

        if not self.strike:
            self.strike = self.getStrike(exDate)
        strike = _convertStrikeQuote(self.strike, self.instrument)

        if self.instrument.IsCallOption():
            exercise = self.settlePrice > strike
        else:
            exercise = self.settlePrice < strike

        _logExerciseCondition(self, exercise)
        return exercise

    def getStrike(self, exDate=None):
        return self.strike

    def getSettlePrice(self, exDate, settlePrice=0.):
        if settlePrice:
            return settlePrice

        instr = self.instrument
        if instr.UnderlyingType() == CURRENCY:
            settlePrice = FFxCommon.getMtMFXRate(instr.Underlying(),
                    instr.StrikeCurrency(), self.market, exDate)
        else:
            settlePrice = FFxCommon.getMtMRate(instr.Underlying(),
                    instr.StrikeCurrency(), FFxCommon.SETTLE, self.market,
                    exDate)
        return settlePrice

    def isCashSettlement(self):
        return self.instrument.SettlementType() == CASH_SETTLEMENT

    def _createAbandonTrade(self, posTrade,
                        linkTrade, tradeDate, settleDate):
        dup = _copyTrade(posTrade, linkTrade)
        dup.TradeTime(tradeDate)
        dup.ValueDay(settleDate)
        dup.AcquireDay(settleDate)
        dup.Price(0.)
        dup.Quantity(-posTrade.Quantity())
        dup.Premium(0.)
        dup.Type(ABANDON)

        hook = trade_status_hook
        if hook:

            # Customized behavior
            dup.status(hook(ABANDON, dup, self.preview))
        elif self.preview:

            # Default behavior
            dup.Status('Simulated')

        return dup

    def _createClosingTrade(self, posTrade, linkTrade,
            tradeDate, settleDate, price, rollbackWrapper):
        dup = _copyTrade(posTrade, linkTrade)
        # TODO: dup.TradeTime(tradeDate.ToTime() + TRADE_TIME - 2)
        dup.TradeTime(tradeDate)
        dup.ValueDay(settleDate)
        dup.AcquireDay(settleDate)
        tradeType = _getExerciseTradeType(posTrade)
        dup.Type(tradeType)
        dup.Price(price)
        dup.Quantity(-posTrade.Quantity())
        dup.UpdatePremium(True)

        hook = trade_status_hook
        if hook:

            # Customized behavior
            dup.status(hook(tradeType, dup, self.preview))
        elif self.preview:

            # Default behavior
            dup.Status('Simulated')

        rollbackWrapper.add_trade(dup)
        return dup


class AsianOption(BaseOption):
    def __init__(self, ins, preview, market=''):
        super(AsianOption, self).__init__(ins, preview, market)
        self._getExoticProperties()

    def _getAverages(self):
        calcSpace = acm.Calculations().CreateCalculationSpace(
                acm.GetDefaultContext(), 'FPortfolioSheet')
        calcSpace.Clear()
        topNode = calcSpace.InsertItem(self.instrument)
        calcSpace.Refresh()

        node = topNode.Iterator().FirstChild()
        if not node:
            raise acm.FException("Could not get Asian Option instrument "
                    "fields from the CalculationSpace.")
        nodeTree = node.Tree()

        if self.priceType == AVERAGE:
            self.settlePrice = _getColumnValue(calcSpace, nodeTree, AV_PRICE,
                    self.instrument)
        if self.strikeType == AVERAGE:
            self.strike = _getColumnValue(calcSpace, nodeTree, AV_STRIKE,
                    self.instrument)

    def _getExoticProperties(self):
        exotics = self.instrument.Exotics()
        if not exotics or not exotics.Size():
            raise acm.FException("Asian option {0} created without Exotics "
                    "field.".format(self.instrument.Name()))

        self.priceType = exotics[0].AveragePriceType()
        self.strikeType = exotics[0].AverageStrikeType()
        if AVERAGE in (self.priceType, self.strikeType):
            self._getAverages()

    def getStrike(self, exDate=None):
        if not exDate:
            exDate = self.instrument.ExpiryDate()
        if self.strikeType == FLOAT:
            self.strike = self.getSettlePrice(exDate)
        # All other strike types (FIXED, AVERAGE) should have been initialized.
        return self.strike

class CliquetOption(BaseOption):
    def __init__(self, ins, preview=0, market=''):
        super(CliquetOption, self).__init__(ins, preview, market)
        self._getExoticProperties()

    def _getExoticProperties(self):
        exotics = self.instrument.Exotics()
        if not exotics or not exotics.Size():
            raise acm.FException("Cliquet option {0} created without Exotics "
                    "field.".format(self.instrument.Name()))

        self.cliquetType = exotics[0].CliquetOptionType()

    def _getExoticEvents(self):
        events = self.instrument.ExoticEvents()
        if not events or not events.Size():
            raise acm.FException("Cliquet option {0} created without Exotic "
                    "Events.".format(self.instrument.Name()))

        return events

    def _getCliquetEvent(self, exDate):
        if not exDate:
            raise acm.FException("Failed to find Cliquet."
                    "Event.".format(self.instrument.Name()))

        events = self._getExoticEvents()
        beforeCliquet = None
        events = events.SortByProperty('Date')
        for cliquetEvent in events:
            if cliquetEvent.Date() <= exDate:
                beforeCliquet = cliquetEvent
            else:
                if beforeCliquet:
                    return beforeCliquet

        return beforeCliquet

    def _isFinalReset(self, exDate):
        events = self._getExoticEvents()
        beforeCliquet = None
        for cliquetEvent in events:
            if cliquetEvent.Date() > exDate:
                return False

        return True

    def canExercise(self, exDate):

        event = self._getCliquetEvent(exDate)
        if not event:
            return False
        else:
            return True

    def shouldExercise(self, exDate, settlePrice=0.):
        if not self.canExercise(exDate):
            return False

        if not self.settlePrice:
            self.settlePrice = self.getSettlePrice(exDate, settlePrice)
            if not self.settlePrice:
                return False

        self.strike = self.getStrike(exDate)
        strike = _convertStrikeQuote(self.strike, self.instrument)

        if self.instrument.IsCallOption():
            exercise = self.settlePrice > strike
        else:
            exercise = self.settlePrice < strike

        _logExerciseCondition(self, exercise)
        return exercise

    def getStrike(self, exDate=None):
        if not exDate:
            raise acm.FException("Failed to find strike for Cliquet."
                    "Option.".format(self.instrument.Name()))

        event = self._getCliquetEvent(exDate)
        if event:
            return event.EventValue()
        else:
            return None

    def _createAbandonTrade(self, posTrade,
                        linkTrade, tradeDate, settleDate):
        # for a cliquet, we only abandon at the last reset date
        if not self._isFinalReset(settleDate):
            return None

        return super(CliquetOption, self)._createAbandonTrade(posTrade,
                                            linkTrade, tradeDate, settleDate)

    def _createClosingTrade(self, posTrade, linkTrade, tradeDate,
            settleDate, price, rollbackWrapper):
        # for a pay-end or pay-go cliquet, we only close out at
        # the very end but for a pay-go, we generate a cash payment
        # on a trade with zero quantity
        # for the current reset
        dup = super(CliquetOption, self)._createClosingTrade(posTrade,
                linkTrade, tradeDate, settleDate, 0.0, rollbackWrapper)
        if not self._isFinalReset(settleDate):
            dup.Quantity(0.0)

        if self.cliquetType == 'Pay Go':
            # calculate the payamount for the current reset
            cliquet = self._getCliquetEvent(settleDate)
            payout = self._calculateCashAmount(posTrade, price,
                                                settleDate, cliquet)
            payment = _createPayment(settleDate, payout,
                        self.instrument.StrikeCurrency(),
                        posTrade.Acquirer())
            payment.Trade(dup)
            rollbackWrapper.add(payment)
        elif self.cliquetType == 'Pay End':
            # calculate the payamount for all the resets
            cliquets = self._getExoticEvents()
            for cliquet in cliquets:
                payout = self._calculateCashAmount(posTrade, price,
                                                settleDate, cliquet)
                payment = _createPayment(settleDate, payout,
                        self.instrument.StrikeCurrency(),
                        posTrade.Acquirer())
                payment.Trade(dup)
                rollbackWrapper.add(payment)
        return dup

    def _calculateCashAmount(self, posTrade, price, settleDate, cliquet):
        # check settleDate is the exDate
        strike = cliquet.EventValue()
        currentPrice = self.getSettlePrice(settleDate)
        # we receive current price - strike * Q
        contractSize = posTrade.Instrument().ContractSize()
        # check if in the money
        if self.shouldExercise(settleDate, currentPrice):
            payout = contractSize * posTrade.Quantity() * \
                                        (strike - currentPrice)
        else:
            payout = 0.0
        return payout

class Combination(BaseOption):

    def __init__(self, ins, preview, market=''):
        self.instrument = _getACMInstr(ins)
        if not self.instrument.IsKindOf(acm.FCombination):
            raise acm.FException("{0} ({1}) is not an "
                "Combination.".format(self.instrument.Name(),
                    self.instrument.InsType()))

        self.preview = preview
        self.childrenOptions = []
        for child in self.instrument.Instruments():
            aelChild = FBDPCommon.acm_to_ael(child)
            option = _createOption(aelChild, preview, market)
            cashSettle = option.isCashSettlement()
            if not cashSettle:
                raise acm.FException("Not Supported: child "
                "instrument {0} in the combination is not "
                "cash settlement".format(child.Name()))

            self.childrenOptions.append(option)

    def getExerciseDate(self):
        exDate = 0
        for option in self.childrenOptions:
            date = option.getExerciseDate()
            if date > exDate:
                exDate = date
        return exDate

    def canExercise(self, exDate):

        for option in self.childrenOptions:
            if not option.canExercise(exDate):
                return False
        return True

    def shouldExercise(self, exDate, settlePrice=0.):
        if not self.canExercise(exDate):
            return False

        for option in self.childrenOptions:
            if option.shouldExercise(exDate, settlePrice):
                return True

        return False

    def getStrike(self, exDate=None):
        return 0

    def getSettlePrice(self, exDate, settlePrice=0.):
        return 0

    def isCashSettlement(self):
        return True

    def _createClosingTrade(self, posTrade, linkTrade, tradeDate,
            settleDate, price, rollbackWrapper):
        dup = super(Combination, self)._createClosingTrade(posTrade,
                    linkTrade, tradeDate, settleDate, 0, rollbackWrapper)
        payout = self._calculateCashAmount(tradeDate, -posTrade.Quantity())
        for payCurrency in payout:
            payment = _createPayment(settleDate, payout[payCurrency],
                payCurrency,
                posTrade.Acquirer())
            payment.Trade(dup)
            rollbackWrapper.add(payment)
        return dup

    def _calculateCashAmount(self, exDate, quantity):
        # check settleDate is the exDate
        payout = {}
        for option in self.childrenOptions:
            if not option.shouldExercise(exDate):
                continue
            # the option should all be CASH SETTLEMENT,
            # it doesn't matter which mode it is in.
            currency = option.instrument.StrikeCurrency()
            closingPrice = _getClosingPrice(option, STRIKE_PRICE)
            weight = self.instrument.FindInstrumentWeight(option.instrument,
                    acm.Time.AsDate(exDate))
            amount = weight * quantity * closingPrice.derivative
            if currency in payout:
                payout[currency] += amount
            else:
                payout[currency] = amount

        return payout

def perform_exercise_assign(args):
    FBDPCommon.callSelectionHook(args, 'trades', 'exercise_assign_selection')
    e = Exercise('Exercise Assign', args['Testmode'], args)
    e.perform_exercise_assign(args)
    e.end()


def getSettlePriceFromMarket(ins, date, settleMarket):
    priceCurr = ins.strike_curr if ins.instype != 'Future/Forward' else None
    settleIns = ins if ins.instype == 'Future/Forward' else ins.und_insaddr
    return FBDPInstrument.find_settle_price(ins, settleIns, date, priceCurr,
            settleMarket)

def getOptionType(exotic):

    isKnockIn = exotic.barrier_option_type in ('Double In',
            'Down & In', 'Up & In')
    isKnockOut = exotic.barrier_option_type in ('Double Out',
            'Down & Out', 'Up & Out')
    isOneTouch = 0
    isNoTouch = 0
    if exotic.digital_barrier_type == 'Barrier' and isKnockIn:
        isKnockIn = 0
        isOneTouch = 1
    elif exotic.digital_barrier_type == 'Barrier' and isKnockOut:
        isKnockOut = 0
        isNoTouch = 1
    return isKnockIn, isKnockOut, isOneTouch, isNoTouch

class Exercise(FFxCommon.FxGroupingProcess):
    INSTRUMENT_TYPES = [OPTION, WARRANT, FUTURES_FORWARD, STOCK, COMBINATION]
    DEALPKG_INTS_TYPES = [OPTION, WARRANT, FUTURES_FORWARD, COMBINATION]
    UNDERLYING_TYPES = [BOND, CURRENCY, COMMODITY, COMMODITY_INDEX,
            COMMODITY_VARIANT, FUTURES_FORWARD, STOCK, STOCK_INDEX]

    def __init__(self, rollbackName, Testmode, param):
        rollbackParam = param.get('Rollback', None)
        self.rollbackWrapper = rollbackParam
        if not rollbackParam:
            self.rollbackWrapper = FBDPRollback.RollbackWrapper(
                rollbackName, param['Testmode'], param)
        self.param = param
        self.businessEvt = param.get('BusinessEvt', None)
        self.preview = param.get('Preview', 0)
        self.instBusinessEvtMap = {}
        self.hasDealpackage = len(param.get('dealpackage', [])) != 0
        FFxCommon.FxGroupingProcess.__init__(self)

    def end(self):
        if not self.param.get('Rollback', None):
            self.rollbackWrapper.end()

    def validateValuationParams(self):
        return True

    def validateInstruments(self):
        "Basic validation of supported instrument types."

        instruments = self.param.get('instruments', [])
        for ins in instruments:
            if ins.InsType() == COMBINATION:
                return True

            if ins.InsType() not in self.INSTRUMENT_TYPES:
                raise ValidationError("Can't exercise instrument '{0}' of "
                        "type '{1}'.".format(ins.Name(), ins.InsType()))
            underlying = ins.Underlying()
            if not underlying:
                self.newInstrument = self.param.get('CAInstrument', None)
                if self.newInstrument:
                    self.newInstrument = ael.Instrument[self.newInstrument]

                if self.newInstrument:
                    return True
                else:
                    raise ValidationError("Missing rights instrument.")
            if underlying.InsType() not in self.UNDERLYING_TYPES:
                raise ValidationError("Can't exercise derivative '{0}' on "
                        "underlying type '{1}'.".format(ins.Name(),
                            underlying.InsType()))
        return True

    def readArguments(self, args):
        if 'actions_for_trades' in self.param:
            Logme()('Found \'actions_for_trades\' in ael_variables.', 'DEBUG')
            # Turn the parameter (a string) back into a real dictionary.
            self.actionsForTrades = eval(
                    self.param['actions_for_trades'])
        else:
            self.actionsForTrades = None
        self.doExeAssign = self.param['DoExeAss']
        self.doAbandon = self.param['DoAbandon']
        self.closeAll = self.param.get('close_all', True)
        self.exerciseIfATM = self.param.get('exercise_if_ATM', 0)
        self.mode = self.param['mode']
        settlePrice = self.param.get('settle_price', None)
        if settlePrice:
            self.settlePrice = float(str(settlePrice).replace(',', '.'))
        else:
            self.settlePrice = 0.
        self.settleMarket = self.param['settlemarket']
        self.portfolioGrouper = self.param.get(
                        'PortfolioGrouper', None)
        self.givenTradeIds = self.param.get('trades', None)
        if not self.givenTradeIds or self.actionsForTrades:
            self.tradingObjects = self.getTradingObjects(
                                        self.param)
        self.instruments = self.param.get('instruments', [])
        self.partialExercise = float(self.param.get(
                            'partial_exercise', '100')) / 100
        self.newInstrument = self.param.get('CAInstrument', None)
        if 'ExDate' in self.param:
            self.exDate = ael.date(self.param.get('ExDate', None))
        else:
            self.exDate = None
        self.dealPkgs = self.param.get('dealpackage', [])

    def requiredAttributesNotSet(self):
        msg = ""
        if not (self.tradingObjects or self.instruments or \
            self.hasDealpackage):
            msg = ("At least one of the fields in 'Stored Folder', "
                    "'Trade Filter', 'Instrument' 'deal package' or "
                    "'Portfolio' needs to be set.")
        if not msg:
            msg = self.requiredSubAttributesNotSet()
        if msg:
            Logme()("%s " % msg, 'ERROR')
        return msg

    def createObjectUnion(self, selectors):
        """
        Overrides base method in FFxCommon.TimeOrPorfolioSheet, which seems to
        assume all objects are variants of portfolios or trade filters.

        selectors is the return value from getTradingObjects().
        """

        # Union of trades selected by portfolio and/or trade filter
        tradeSet = acm.FIdentitySet()
        for obj in selectors:
            tradeSet.AddAll(self.getTrades(obj))

        # Union of trades selected by instrument
        instrSet = acm.FIdentitySet()
        for instr in self.instruments:
            valid = [trd for trd in instr.Trades() if self.isValidTrade(trd)]
            instrSet.AddAll(valid)

        # Intersection, not union, of the two
        merged = acm.FSet()
        if tradeSet.IsEmpty():
            merged = instrSet
        elif instrSet.IsEmpty():
            merged = tradeSet
        else:
            merged = tradeSet.Intersection(instrSet)

        portf = acm.FAdhocPortfolio()
        portf.Name("Trade Union")
        for trd in merged:
            portf.Add(trd)
        return portf

    def getTradingObjects(self, dictionary):

        objects = acm.FArray()
        if not self.actionsForTrades:
            for field in ['TradeQuery', 'TradeFilter', 'TradingPortfolios']:
                if field in dictionary and dictionary[field]:
                    objects.AddAll(dictionary[field])
        else:
            for tradeId in self.givenTradeIds:
                objects.Add(acm.FTrade[tradeId])
        return objects

    def _createPositionTrade(self, ins, depTrade, quantity,
                    portfolioName, price):
        if self.actionsForTrades and not self.portfolioGrouper:
            t = depTrade.new()
        else:
            t = ael.Trade.new(ins)
        t.curr = depTrade.curr
        t.prfnbr = None
        if acm.FPhysicalPortfolio[portfolioName]:
            t.prfnbr = acm.FPhysicalPortfolio[portfolioName].Oid()
        t.counterparty_ptynbr = ael.Party['FMAINTENANCE']
        t.acquirer_ptynbr = ael.Party['FMAINTENANCE']
        t.quantity = quantity
        t.price = price

        hook = trade_status_hook
        if hook:

            # Customized behavior
            t.status = hook(CLOSE, t, self.preview)
        else:

            # Default behavior
            t.status = 'Simulated' if self.preview else 'FO Confirmed'

        self.setTradePropertiesFromGrouper(FBDPCommon.ael_to_acm(t),
                ('Portfolio', 'Instrument.Instrument', 'Oid'))
        return t

    def _setUnderlyingTradeProcess(self, ins, t_und):
        if t_und.insaddr.instype == 'Curr':
            if ins.instype == 'Future/Forward':
                if ins.paytype == 'Forward':
                    t_und.trade_process = 1 << 13
                else:
                    t_und.trade_process = 1 << 12
        return t_und

    def _getMeanPrice(self, node, instrument, curr):
        if not FBDPCommon.is_acm_object(curr):
            curr = FBDPCommon.ael_to_acm(curr)

        self.calcSpace.SimulateValue(
            node, 'Portfolio Currency', curr)
        calcObj = self.calcSpace.CalculateValue(
                        node, 'Portfolio Mean')

        if not calcObj:
            Logme()('Could not get price for {0}. Returning 0.'.format(
                instrument.Name()), WARNING)
            return 0.
        val = calcObj.Value()
        if isinstance(val, float):
            return val
        return val.Number()

    def processPortfolio(self, tradingPort, nodes):
        FFxCommon.printEmp('Process trading portfolio: "%s".' %
                (tradingPort and tradingPort.Name()), '*')

        for (topNode, self.attributes) in nodes:
            if self.attributes:
                FFxCommon.printEmp('Process grouping position: %s' %
                        (self.attributes), '=')

            try:
                processed = False
                if custom_exercise_hook:
                    processed = custom_exercise_hook(self.attributes,
                                        self.param['Testmode'], self.mode)

                if processed:
                    msg = "Processed position: "
                    msg += str(self.attributes)
                    msg += " using custom_exercise hook"
                    Logme()("%s " % msg, INFO)
                    continue

            except Exception as e:
                Logme()("Caught exception from FBDPHook custom_exercise",
                        ERROR)
                Logme()(str(e), ERROR)

            acmIns = self.instrumentAtNode(topNode)
            aelIns = FBDPCommon.acm_to_ael(acmIns)
            date = self.getExerciseDate(aelIns)
            dependTrades = [FBDPCommon.acm_to_ael(t)
                for t in topNode.Item().Trades().AsIndexedCollection() \
                    if t.Status() not in ['Void', 'Simulated']]

            if not len(dependTrades):
                continue

            self.tradesOnDarivative = dependTrades
            depTrade = dependTrades[0]
            portfolioName = self.attributes['Portfolio']
            price = 0
            node = topNode
            while node.Iterator().HasChildren():
                node = node.Iterator().FirstChild().Tree()

            ins_is_fx_ndf = self.isFXNDF(aelIns)
            if ins_is_fx_ndf:
                quantity = self.calcSpace.CalculateValue(
                            node, 'Portfolio Profit Loss Period Position')
            else:
                quantity = self.calcSpace.CalculateValue(
                            node, 'Portfolio Position')
            price = self._getMeanPrice(node, acmIns, depTrade.curr)
            posTrade = self._createPositionTrade(aelIns, depTrade,
                        quantity, portfolioName, price)
            calcPositions = FBDPCalculatePosition.CalcTrades([])
            position = []
            posTrades = [posTrade]
            originalTrades = [FBDPCommon.acm_to_ael(t)
                    for t in topNode.Item().Trades().AsIndexedCollection()]
            position.append(posTrades)
            position.append(originalTrades)
            calcPositions.append(position)
            try:
                from FBDPHook import recalculate_position
                hookArguments = self.param
                calcPositions = recalculate_position(aelIns,
                    calcPositions, hookArguments)
            except:
                pass

            if isAsianOption(aelIns) or isCliquetOption(aelIns) or \
               isCombination(aelIns):
                try:
                    calcPositions = FBDPCalculatePosition.convertPositions(
                            calcPositions, toAel=False)
                    self.run(aelIns, calcPositions)
                except ValidationError as e:
                    Logme()('Validation error processing {0}: {1}'.format(
                        aelIns.insid, e), ERROR)
                except acm.FException as e:
                    Logme()('ACM error processing {0}: {1}'.format(
                        aelIns.insid, e), ERROR)
                continue

            self.createBusinessEventAndLinkPositionTrades(dependTrades)

            posName = '[{0}:{1}]'.format(portfolioName, aelIns.insid)
            manualAction = self.getManualOverride(aelIns)
            insIsBarrier = isBarrier(aelIns)
            self.adjustPosition(aelIns, posTrade, depTrade, date, posName,
                    manualAction, insIsBarrier, 0)

    def getPositions(self):
        """
        This function is for legacy implemention
        """
        positions = {}
        for tradeId in self.givenTradeIds:
            t = ael.Trade[tradeId]
            ins = t.insaddr
            port = t.prfnbr
            if ins not in positions:
                positions[ins] = [port]
            else:
                if positions[ins].count(port) == 0:
                    positions[ins].append(port)
        return positions

    def getDealPackagePositions(self, dealpackage):
        positions = {}
        trades = dealpackage.Trades()
        for t in trades:
            ins = t.Instrument()
            if ins.InsType() not in self.DEALPKG_INTS_TYPES:
                continue
            port = t.Portfolio()
            aelIns = FBDPCommon.acm_to_ael(ins)
            aelPort = FBDPCommon.acm_to_ael(port)
            if aelIns not in positions:
                positions[aelIns] = [aelPort]
            else:
                if positions[aelIns].count(aelPort) == 0:
                    positions[aelIns].append(aelPort)
        return positions

    def abandon(self, option, positions, exDate, dealpackage):
        """
        For each position, creates a new trade with an opposite quantity to the
        expired out-of-the-money position with a price and premium of 0 and a
        status of 'Abandon'.
        """
        settleDate = _getSettleDate(option.instrument, exDate)
        for pos in positions:
            posTrades, orgTrades = (pos[0], pos[1])
            multiCurr = len(posTrades) > 1
            for trade in posTrades:
                if not trade.Quantity():
                    continue
                link = _getLinkedTrade(trade, orgTrades, multiCurr)
                abandoned = option._createAbandonTrade(trade, link, exDate,
                        settleDate)
                if self.preview:
                    abandoned.status = 'Simulated'
                self.rollbackWrapper.add_trade(abandoned)
                self.createBusinessEventAndLinkPositionTrades(orgTrades)
                self.add_trade_link(abandoned, dealpackage)

    def exerciseAssign(self, option, positions, exDate, dealpackage):
        settleDate = _getSettleDate(option.instrument, exDate)
        cashSettle = option.isCashSettlement()
        closingPrice = _getClosingPrice(option, self.mode)

        # The structure of positions, returned from calculatePositions(), is:
        # [[
        #   [all "dependent trades"],
        #   ["original trades" for first dependent trade],
        #   ["original trades" for second dependent trade],
        #   etc.
        # ]]
        # There will be more than one position trade if there are multiple
        # premium currencies in the list of original trades.
        for pos in positions:
            posTrades, orgTrades = (pos[0], pos[1])
            multiCurr = len(posTrades) > 1
            for trade in posTrades:
                if not trade.Quantity():
                    _logZeroPosition(posTrades[0], option)
                    continue
                link = _getLinkedTrade(trade, orgTrades, multiCurr)
                closingTrade = option._createClosingTrade(trade, link, exDate,
                    settleDate, closingPrice.derivative, self.rollbackWrapper)
                # self.rollbackWrapper.add_trade(closingTrade)
                self.createBusinessEventAndLinkPositionTrades(orgTrades)
                self.add_trade_link(closingTrade, dealpackage)
                if not cashSettle:
                    underlying = _createUnderlyingTrade(trade, link, exDate,
                        settleDate, closingPrice.underlying)
                    payoff = option.settlePrice - option.strike
                    self._applyLotSizeOnAcm(underlying, closingTrade,
                                            payoff)
                    if self.preview:
                        underlying.status = 'Simulated'
                    self.rollbackWrapper.add_trade(underlying)
                    self.add_trade_link(underlying, dealpackage)

    # New loop for exercising or abandoning instruments.
    def run(self, ins, positions, dealpackage=None):
        option = _createOption(ins, self.preview, self.settleMarket)
        exDate = self.getExerciseDate(ins).to_string(ael.DATE_ISO)

        if not option.canExercise(exDate):
            Logme()("{0}-style option {1} cannot be exercised on {2}.".format(
                option.instrument.ExerciseType(), option.instrument.Name(),
                exDate), WARNING)
            return

        manualAction = self.getManualOverride(ins)
        if manualAction == EXERCISE:
            if not option.shouldExercise(exDate, self.settlePrice):
                Logme()("Forcing {0} to be exercised.".format(
                    option.instrument.Name()), INFO)
            self.exerciseAssign(option, positions, exDate, dealpackage)
            return

        if manualAction == ABANDON:
            if option.shouldExercise(exDate, self.settlePrice):
                Logme()("Forcing {0} to be abandoned.".format(
                    option.instrument.Name()), INFO)
            self.abandon(option, positions, exDate, dealpackage)
            return

        if option.shouldExercise(exDate, self.settlePrice):
            if self.doExeAssign:
                self.exerciseAssign(option, positions, exDate, dealpackage)
        else:  # for option should not be exercised
            if self.doAbandon:
                self.abandon(option, positions, exDate, dealpackage)
        # TODO: Hooks

    def add_trade_link(self, trade, dealpackage):

        evt = self.getBusinessEvent(trade)
        trdnbr = _tradeNumber(trade)
        tradeLink = acm.FBusinessEventTradeLink()
        tradeLink.Trade(trdnbr)
        tradeLink.BusinessEvent(evt)
        self.rollbackWrapper.add(tradeLink)
        Summary().ok(tradeLink, Summary().CREATE, tradeLink.Oid())

        if dealpackage:
            trd = acm.FTrade[trdnbr]
            trdInst = trd.Instrument()
            trdInstName = trdInst.Name()
            instNameL = [l.Instrument().Name() \
                for l in dealpackage.InstrumentLinks()]
            if trdInstName not in instNameL:
                instLink = acm.FDealPackageInstrumentLink()
                instLink.Instrument(trdInst.Oid())
                instPkg = dealpackage.InstrumentPackage()
                instLink.InstrumentPackage(instPkg)
                self.rollbackWrapper.add(instLink)
                Logme()("Adding Instrument {0} into instrument package {1}"\
                   .format(trdInstName, instPkg.Name()), INFO)
                Summary().ok(instLink, Summary().CREATE, instLink.Oid())

            dealpackageTrdLink = acm.FDealPackageTradeLink()
            dealpackageTrdLink.Trade(trdnbr)
            dealpackageTrdLink.DealPackage(dealpackage)
            self.rollbackWrapper.add(dealpackageTrdLink)
            Summary().ok(dealpackageTrdLink, Summary().CREATE, \
                dealpackageTrdLink.Oid())

    def exercised_trade_oids(self, dependTrades):
        toReturn = []
        for trade in dependTrades:
            trdnbr = _tradeNumber(trade)
            acmTrade = acm.FTrade[trdnbr]
            bEvent = acmTrade.BusinessEvents('Exercise/Assign')
            if bEvent:
                tradeLinks = bEvent[0].TradeLinks()
                for link in tradeLinks:
                    if link.Trade().Oid() not in toReturn:
                        toReturn.append(link.Trade().Oid())
        return toReturn

    def isValidTrade(self, trade):
        aelIns = FBDPCommon.acm_to_ael(trade.Instrument())
        aelExeDate = self.getExerciseDate(aelIns)
        strIsoExeDate = aelExeDate.to_string(ael.DATE_ISO)
        return _isTradedOnOrBeforeExerciseDate(trade, strIsoExeDate)

    def getTrades(self, obj):

        # Portfolio
        if obj.IsKindOf(acm.FPortfolio):
            return [t for t in obj.Trades() if self.isValidTrade(t)]

        # Trade filter
        elif obj.IsKindOf(acm.FTradeSelection):
            return [t for t in obj.Trades()
                if self.isValidTrade(t)]

        # StoredFolder
        elif obj.IsKindOf(acm.FStoredASQLQuery) and \
            obj.SubType() == 'FTrade':
            return [t for t in obj.Query().Select()
                if self.isValidTrade(t)]

        # Trade
        assert obj.IsKindOf(acm.FTrade), ("Invalid trading object type: "
                "{0}".format(type(obj)))
        return [obj]

    def createOrModifyGrouper(self, grouper):
        groupers = acm.FArray()
        portGrouperNeeded = True
        instrumentGrouperNeeded = True
        tradeIdGrouperNeeded = False
        if grouper and grouper.IsKindOf(acm.FChainedGrouper):
            for g in grouper.Groupers():
                groupers.Add(g)
                if str(g.Label()) == 'Trade Portfolio':
                    portGrouperNeeded = False
                if str(g.Label()) == 'Instrument.Instrument':
                    instrumentGrouperNeeded = False
        elif not grouper and self.actionsForTrades:
            tradeIdGrouperNeeded = True

        if tradeIdGrouperNeeded:
            portGrouper = acm.FAttributeGrouper("Trade.Oid")
            portGrouper.Label("Trade: Trade No")
            groupers.Add(portGrouper)

        if instrumentGrouperNeeded:
            portGrouper = acm.FAttributeGrouper("Instrument.Instrument")
            portGrouper.Label("Instrument.Instrument")
            groupers.Add(portGrouper)

        if portGrouperNeeded:
            portGrouper = acm.FAttributeGrouper("Trade.Portfolio")
            portGrouper.Label("Trade Portfolio")
            groupers.AtInsert(0, portGrouper)

        grouper = acm.FChainedGrouper(groupers)
        return grouper

    def performDealPackage(self, args):
        self.readArguments(args)
        for dealPkg in self.dealPkgs:
            dealpackage = acm.FDealPackage[dealPkg]
            if not dealpackage:
                Logme()("{Id {0} is not a dealpackage.".format(
                   dealPkg), WARNING)
                continue

            positions = self.getDealPackagePositions(dealpackage)
            self.performOnPositions(positions, dealpackage)

    def performGivenTrades(self, args):

        self.readArguments(args)

        # Populate instrument dictionary with traded portfolios
        positions = self.getPositions()
        self.performOnPositions(positions)

    def performOnPositions(self, positions, dealpackage=None):

        # positioning after hook recalculate_position
        hookArguments = {}
        try:
            from FBDPHook import recalculate_position
            hookArguments = self.param
        except:
            pass
        for (ins, portfolios) in positions.items():
            manualAction = self.getManualOverride(ins)
            insIsBarrier = isBarrier(ins)
            date = self.getExerciseDate(ins)
            if hookArguments:
                portfolios = []

            calcPositions = FBDPCalculatePosition.calculatePosition(ins,
                    end_date=date, portfolio=portfolios,
                    hookArguments=hookArguments)

            if isAsianOption(ins) or isCliquetOption(ins) or \
               isCombination(ins):
                try:
                    # Convert calcPositions to ACM trades.
                    calcPositions = FBDPCalculatePosition.convertPositions(
                            calcPositions, toAel=False)
                    self.run(ins, calcPositions, dealpackage)
                except ValidationError as e:
                    Logme()('Validation error processing {0}: {1}'.format(
                        ins.insid, e), ERROR)
                except acm.FException as e:
                    Logme()('ACM error processing {0}: {1}'.format(
                        ins.insid, e), ERROR)
                continue

            for pos in calcPositions:
                calcTrades = pos[0]
                dependTrades = pos[1]
                port = calcTrades[0].prfnbr
                posName = '[{0}:{1}]'.format(
                    (port and port.prfid or 'None'), ins.insid)
                if len(calcTrades) > 1:
                    useCurrencyDependency = True
                else:
                    useCurrencyDependency = False
                alreadyExercisedTradeOids = self.exercised_trade_oids(
                    dependTrades)
                for trd in calcTrades:
                    depTrade = None
                    if trd.trdnbr > 0:
                        depTrade = trd
                    else:
                        if useCurrencyDependency:
                            for t in dependTrades:
                                if t.curr == trd.curr:
                                    depTrade = t
                                    break
                        if not depTrade:
                            depTrade = dependTrades[0]

                    if depTrade.trdnbr in alreadyExercisedTradeOids:
                        for t in dependTrades:
                            if t.trdnbr not in alreadyExercisedTradeOids:
                                depTrade = t
                                break
                    self.createBusinessEventAndLinkPositionTrades(
                                            dependTrades,
                                            alreadyExercisedTradeOids)
                    self.adjustPosition(ins, trd, depTrade, date, posName,
                            manualAction, insIsBarrier,
                            len(dependTrades) <= 1, dealpackage)

    def getBusinessEvent(self, t):
        if self.businessEvt:
            return self.businessEvt

        trdnbr = _tradeNumber(t)
        acmTrade = acm.FTrade[trdnbr]
        ins = acmTrade.Instrument().Name()
        if ins in self.instBusinessEvtMap:
            return self.instBusinessEvtMap[ins]
        else:
            evt = acm.FBusinessEvent()
            evt.EventType('Exercise/Assign')
            self.rollbackWrapper.add(evt)
            Summary().ok(evt,
                     Summary().CREATE,
                     evt.Oid())
            self.instBusinessEvtMap[ins] = evt
            return evt

    def createBusinessEventAndLinkPositionTrades(self,
                dependTrades, exercisedTradeOids=[]):

        alreadyExercisedTradeOids = exercisedTradeOids
        if not alreadyExercisedTradeOids:
            alreadyExercisedTradeOids = self.exercised_trade_oids(
                                dependTrades)
        for t in dependTrades:
            trdnbr = _tradeNumber(t)
            if trdnbr not in alreadyExercisedTradeOids:
                self.add_trade_link(t, None)
        return

    def perform_exercise_assign(self, args):
        self.insDates = {}
        self.givenTradeIds = args.get('trades', None)
        if self.hasDealpackage:
            self.performDealPackage(args)
        elif not self.givenTradeIds or 'actions_for_trades' in args:
            self.performProcess(args)
        else:
            self.performGivenTrades(args)

    def adjustPosition(self, ins, trd, dependent_, date, posName, manualAction,
            insIsBarrier, isSingleTradePosition, dealpackage=None):
        Logme()('- ' * 23, 'DEBUG')
        Logme()('Processing {0}'.format(ins.insid), 'DEBUG')
        ignoreMsg = self.checkTradePosition(ins, trd, posName, manualAction,
                insIsBarrier)
        if ignoreMsg:
            Summary().ignore(Summary().POSITION, Summary().action, ignoreMsg,
                    posName)
            return
        trd.quantity_is_derived = dependent_.quantity_is_derived
        useTheorValue = 0
        insIsEuropeanSwaption = (insIsSwaption(ins) and
                ins.exercise_type == 'European')
        if insIsEuropeanSwaption:
            useTheorValue = 1
            i = acm.FInstrument[ins.insid]
            calcSpace = acm.FCalculationMethods(
                    ).CreateStandardCalculationsSpaceCollection()
            theor = i.Calculation().TheoreticalValue(calcSpace)
            settle = theor.Value().Number()
        elif self.settlePrice:
            # Find settle price:
            Logme()('Settle price specified manually.', 'DEBUG')
            settle = self.settlePrice
        else:
            settleMarket = self.settleMarket
            if ins.fixing_source_ptynbr:
                settleMarket = ins.fixing_source_ptynbr.ptyid
                msg = ('Using Fixing Source {0} as settle market for '
                      'instrument {1}.'.format(settleMarket, ins.insid))
                Logme()(msg, 'DEBUG')
            settle = getSettlePriceFromMarket(ins, date, settleMarket)
            if not settle:
                if manualAction:
                    msg = 'MANUALLY OVERRIDING: No settle price for underlying'
                    Summary().warning(Summary().POSITION, Summary().action,
                            msg, posName)
                else:
                    msg = 'No settle price for underlying'
                    Summary().ignore(Summary().POSITION, Summary().action,
                            msg, posName)
                    return

        if not useTheorValue:
            Logme()('Will use settle price: {0}'.format(settle), 'DEBUG')
        if ins.instype == FUTURES_FORWARD:
            return self.exercise_or_abandon(ins,
                    trd,
                    date,
                    settle,
                    mode=self.mode,
                    name=posName,
                    dependent=dependent_,
                    isSingleTradePosition=isSingleTradePosition,
                    dealpackage=dealpackage)
        if ins.instype == STOCK:
            return self.exercise_rights(ins,
                    trd,
                    self.exDate,
                    settle,
                    mode=self.mode,
                    name=posName,
                    dependent=dependent_,
                    isSingleTradePosition=isSingleTradePosition,
                    dealpackage=dealpackage)
        # Barrier Options
        if insIsBarrier:
            (errMsg, typ) = self.checkBarrierOption(ins, posName,
                    manualAction)
            if errMsg:
                args = [Summary().POSITION, Summary().action, errMsg, posName]
                if typ == 'fail':
                    Summary().fail(*args)
                else:
                    Summary().ignore(*args)
                return

        # Check if derivative is in-the-money.
        InTheMoney = 0
        AtTheMoney = 0
        strike_price = convert_price_to_und_or_strike_quotation(ins,
                ins.strike_price, 1)
        if insIsEuropeanSwaption:
            if settle:
                InTheMoney = 1
        elif ((ins.call_option == 1 and strike_price < settle) or
                (ins.call_option == 0 and strike_price > settle)):
            # ExeAss = 1 => in-the-money
            InTheMoney = 1
        elif (FBDPCommon.eps_compare(strike_price, settle)):
            AtTheMoney = 1

        exerciseATM = self.exerciseIfATM and AtTheMoney
        ExeAss = 0
        Abandon = 0

        actionFromInTheMoney = True
        # If the user has changed the default value 'Normal' value of the
        # 'Action' column in the Trade Sheet, always do what the user says,
        # period.
        if manualAction in ['Exercise', 'Abandon', 'Skip']:
            actionFromInTheMoney = False
            msg = ('Manual override for {0}: {1}.'.format(dependent_.trdnbr,
                    manualAction))
            Logme()(msg)
            # For 'Skip'  keep ExeAss=0 and Abandon=0
            if manualAction == 'Exercise':
                ExeAss = 1
            if manualAction == 'Abandon':
                Abandon = 1
        # If the value of the 'Action' column is not set or is 'Normal,'
        # always perform normal processing.
        elif insIsBarrier:
            exotic = ins.exotics()[0]
            isKnockIn, isKnockOut, isOneTouch, isNoTouch = \
                                getOptionType(exotic)
            crossedStatus = exotic.barrier_crossed_status
            if isKnockOut:
                if 'Confirmed' == crossedStatus:
                    # knocked out, can't exercise
                    Abandon = 1
                    actionFromInTheMoney = False
                elif 'None' == crossedStatus:
                    # not knocked out, might be able to exercise
                    if InTheMoney or exerciseATM:
                        ExeAss = 1
                        actionFromInTheMoney = False
                    else:
                        Abandon = 1
                        actionFromInTheMoney = False
            elif isKnockIn:
                if 'None' == crossedStatus:
                    # not knocked in, can't exercise
                    Abandon = 1
                    actionFromInTheMoney = False
                elif 'Confirmed' == crossedStatus:
                    if InTheMoney or exerciseATM:
                        ExeAss = 1
                        actionFromInTheMoney = False
                    else:
                        Abandon = 1
                        actionFromInTheMoney = False
            elif isOneTouch:
                if 'Confirmed' == crossedStatus:
                    ExeAss = 1
                    actionFromInTheMoney = False
                elif 'None' == crossedStatus:
                    Abandon = 1
                    actionFromInTheMoney = False
            elif isNoTouch:
                if 'Confirmed' == crossedStatus:
                    Abandon = 1
                    actionFromInTheMoney = False
                elif 'None' == crossedStatus:
                    ExeAss = 1
                    actionFromInTheMoney = False
        if actionFromInTheMoney:
            if InTheMoney or exerciseATM:
                if self.doExeAssign:  # all non-barrier options
                    ExeAss = 1
                else:
                    self.debugLogInOrOutTheMoney('In', ins, posName)
                    msg = ('Script executed with "Exercise ITM Normal Trades" '
                            'untoggled')
                    Summary().ignore(Summary().POSITION, Summary().action,
                            msg, posName)
                    return
            else:
                if self.doAbandon:
                    Abandon = 1
                else:
                    self.debugLogInOrOutTheMoney('Out-Of', ins, posName)
                    msg = ('Script executed with '
                            '"Abandon OTM and ATM Normal Trades" untoggled')
                    Summary().ignore(Summary().POSITION, Summary().action,
                            msg, posName)
                    return
        self.exercise_or_abandon(ins,
                    trd,
                    date,
                    settle,
                    exeass=ExeAss,
                    mode=self.mode,
                    aba=Abandon,
                    dependent=dependent_,
                    name=posName,
                    insIsBarrier=insIsBarrier,
                    isSingleTradePosition=isSingleTradePosition,
                    dealpackage=dealpackage)

    def checkTradePosition(self, ins, trd, posName, manualAction,
            insIsBarrier):
        if FBDPCommon.eps_compare(trd.quantity, 0):
            if manualAction:
                Summary().warning(Summary().POSITION, Summary().action,
                        'MANUALLY OVERRIDING: Zero position',
                        '{0}'.format(posName))
            else:
                return 'Zero position'

        if not ins.instype in self.INSTRUMENT_TYPES:
            msg = ('Instrument {0} has the unsupported instrument type '
                    '{1}.'.format(ins.insid, ins.instype))
            Logme()(msg)
            return 'Unsupported instrument type {0}'.format(ins.instype)

        if ins.settlement == 'Physical Delivery':
            if ins.und_insaddr.generic:
                if manualAction:
                    msg = ('MANUALLY OVERRIDING: Physical delivery of '
                            'generic underlying is not supported {0}'.format(
                            ins.insid))
                    Summary().warning(Summary().POSITION, Summary().action,
                            msg, posName)
                else:
                    msg = ('Physical delivery of generic underlying is not '
                            'supported {0}'.format(ins.insid))
                    return msg
            if ins.und_insaddr.notional and not ins.und_insaddr.und_insaddr:
                if manualAction:
                    msg = 'MANUALLY OVERRIDING: No CTD selected.'
                    Summary().warning(Summary().POSITION, Summary().action,
                            msg, posName)
                else:
                    return 'No CTD selected.'
        # European options can not be processed early, except for barriers
        if (ins.exercise_type == 'European' and
                ins.exp_day > ael.date_today() and
                not insIsBarrier):
            if manualAction:
                msg = ('MANUALLY OVERRIDING: European option with '
                        'Expiry > Today')
                Summary().warning(Summary().POSITION, Summary().action, msg,
                        posName)
            else:
                return 'European option with Expiry > Today'

    def checkBarrierOption(self, ins, posName, manualAction):
        include = 0
        exotic = ins.exotics()[0]
        if exotic.barrier_crossed_status == 'Crossed' and not manualAction:
            msg = ('Barrier Crossed but not yet Confirmed. Change the '
                    'trade(s) to Confirmed and resubmit:'
                    '\'{0}\'.'.format(ins.insid))
            Logme()(msg, 'ERROR')
            msg = 'Change the trade(s) to Confirmed and resubmit.'
            return (msg, 'fail')

        # include all knocked barriers, but not the european
        if (exotic.barrier_crossed_status == 'Confirmed' and
                not ins.exercise_type == 'European'):
            include = 1
        # include all expired options
        if ins.exp_day <= ael.date_today():
            include = 1
        # include knocked-out barriers. They should be abandoned.
        if (exotic.barrier_option_type in ('Double Out', 'Down & Out',
                'Up & Out') and exotic.barrier_crossed_status == 'Confirmed'):
            include = 1
        # Include knocked in Digital Barriers, they should be exercised.
        # Except Digital Barrier & Strike European. It becomes Digital Strike
        # European, thus wait until expiry.
        elif (exotic.barrier_option_type in ('Double In',
                'Down & In', 'Up & In') and ins.digital and
                exotic.barrier_crossed_status == 'Confirmed' and
                not exotic.digital_barrier_type == 'Barrier & Strike'):
            include = 1
        elif (ins.exercise_type == 'European' and
                ins.exp_day > ael.date_today()):
            include = 0
        if include == 0:
            if manualAction:
                msg = ('MANUALLY OVERRIDING: European barrier option with '
                       'Expiry > Today')
                Summary().warning(Summary().POSITION, Summary().action, msg,
                        posName)
            else:
                msg = 'European barrier option with Expiry > Today'
                return (msg, 'ignore')
        return (None, None)

    def isPhysicalDelivery(self, ins):
        val = False
        if ins.settlement == 'Physical Delivery':
            val = True
            if isBarrier(ins) and ins.digital and ins.und_instype == 'Curr':
                # FX Digital Barriers are always Cash Settled
                val = False
        else:
            val = False
        return val

    def isFXNDF(self, insaddr):
        ins_is_fx_ndf = (insaddr.instype == 'Future/Forward' and
                insaddr.und_instype == 'Curr' and
                insaddr.paytype == 'Forward' and
                insaddr.settlement == 'Cash')
        return ins_is_fx_ndf

    def _applyLotSizeOnAel(self, t_und, t, payoff):
        # using minimum piece for lot size.
        if t_und.insaddr.minimum_piece <= 0:
            return

        originalQuanity = t_und.quantity
        roundingDiff = abs(originalQuanity) % t_und.insaddr.minimum_piece
        if roundingDiff == 0:
            return

        if abs(originalQuanity) > roundingDiff:
            newQuantity = abs(originalQuanity) - roundingDiff
            if originalQuanity < 0:
                newQuantity *= -1
                roundingDiff *= -1
            t_und.quantity = newQuantity
        else:
            t_und.quantity = 0

        p = ael.Payment.new(t)
        p.payday = t.value_day
        p.amount = roundingDiff * payoff
        p.curr = t_und.curr
        p.type = 'Cash'
        p.ptynbr = t.counterparty_ptynbr
        p.valid_from = p.payday
        Summary().ok(p.record_type, Summary().CREATE, p.paynbr)

    def _applyLotSizeOnAcm(self, t_und, t, payoff):
        # using minimum piece for lot size.
        minimum_piece = t_und.Instrument().MinimumPiece()
        if minimum_piece <= 0:
            return

        originalQuanity = t_und.Quantity()
        originalPremium = t_und.Premium()

        roundingDiff = abs(originalQuanity) % minimum_piece
        if roundingDiff == 0:
            return

        if abs(originalQuanity) > roundingDiff:
            newQuantity = abs(originalQuanity) - roundingDiff
            if originalQuanity < 0:
                newQuantity *= -1
                roundingDiff *= -1
            t_und.Quantity(newQuantity)
        else:
            t_und.Quantity(0)

        t_und.UpdatePremium(True)

        pmt = acm.FPayment()
        pmt.Trade(t)
        pmt.Type('Cash')
        pmt.Amount(roundingDiff * payoff)
        pmt.Currency(t_und.Currency())
        pmt.ValidFrom(t.ValueDay())
        pmt.PayDay(t.ValueDay())
        pmt.Party(t.Counterparty())
        self.rollbackWrapper.add(pmt)
        Summary().ok(pmt, Summary().CREATE, pmt.Oid())

    def exercise_rights(self, ins, cp, exerciseDate, price, exeass=0,
            mode='Strike', aba=1, dependent=None, name=None,
            insIsBarrier=False, isSingleTradePosition=False, dealpackage=None):

        if ins.instype not in abandon_types:
            msg = ('To Exercise/Assign/Abandon/Close positions in instruments '
                    'with instype {0} is not supported'.format(ins.instype))
            Logme()(msg, 'WARNING')
            return msg

        exp_day = exerciseDate
        closing_trade = cp.new()
        if FBDPCommon.eps_compare(closing_trade.quantity, 0):
            msg = 'Skipping zero position: ' + name
            Logme()(msg, 'DEBUG')
            return msg

        for p in closing_trade.payments():
            p.delete()

        quantityAll = -closing_trade.quantity
        closing_trade.quantity = -closing_trade.quantity * self.partialExercise
        closing_trade.curr = closing_trade.insaddr.curr
        closing_trade.time = exerciseDate.to_time() + TRADE_TIME - 2

        newStock = copyTrade(closing_trade)
        newStock.insaddr = self.newInstrument
        newStock.price = price
        newStock.quantity = -closing_trade.quantity
        newStock.time = exerciseDate.to_time() + TRADE_TIME - 2
        newStock.premium = FBDPCommon.calculate_premium(newStock)
        self.add_exercise_trade(None, closing_trade, \
            isSingleTradePosition, dealpackage)
        self.add_exercise_trade(None, newStock, \
            isSingleTradePosition, dealpackage)

        return ''

    def exercise_or_abandon(self, ins, cp, exerciseDate, price, exeass=0,
            mode='Strike', aba=1, dependent=None, name=None,
            insIsBarrier=False, isSingleTradePosition=False, dealpackage=None):
        """
        Close/Abandon/Exercise/Assign a position. For future/forward a price
        can be given
        """
        if ins.instype not in abandon_types:
            msg = ('To Exercise/Assign/Abandon/Close positions in instruments '
                    'with instype {0} is not supported'.format(ins.instype))
            Logme()(msg, 'WARNING')
            return

        if ins.instype == STOCK:
            exp_day = exerciseDate
        else:
            exp_day = exp_day_to_date(ins)
        n = 0
        originalTradePrice = cp.price
        t = cp.new()

        for p in t.payments():
            p.delete()

        quantityAll = -t.quantity
        t.quantity = -t.quantity * self.partialExercise
        t.curr = t.insaddr.curr
        if FBDPCommon.eps_compare(t.quantity, 0):
            Logme()('Skipping zero position: ' + name, 'DEBUG')
            return
        if ins.instype == 'Future/Forward':
            t.type = 'Closing'
            summaryType = Summary().CLOSE
        elif exeass == 0:
            t.type = 'Abandon'
            summaryType = Summary().ABANDON
            if aba == 0:
                return
        elif t.quantity < 0:
            t.type = 'Exercise'
            summaryType = Summary().EXERCISE
        else:
            t.type = 'Assign'
            summaryType = Summary().ASSIGN

        create_payment = 0
        pay = None

        # Link exercise, and delivery trades
        # by setting their contract trade numbers equal to (one of) the
        # original trade number, in order to enable multiple original trades
        # to be closed by one exercise trade.
        if dependent:
            t.contract_trdnbr = dependent.trdnbr
            t.connected_trdnbr = None
        elif ins.instype != 'Future/Forward':
            msg = ('Not linking original, exercise, and delivery trades due '
                    'to null original.')
            Logme()(msg, 'WARNING')

        ins_is_fx_ndf = self.isFXNDF(t.insaddr)

        if any([not price, math.isinf(price), math.isnan(price)]):
            if ins_is_fx_ndf:
                errorMsg = ('No settlement price found for non-deliverable '
                        'forward {0} on {1}.'.format(ins.insid, exp_day))
                raise RuntimeError(errorMsg)
            price = suggest_abandon_price(ins, exp_day)
        if ins.instype in ['Option', 'Warrant']:
            from FBDPCommon import create_price, create_quotetype_price
            strike_price = convert_price_to_und_or_strike_quotation(ins,
                    ins.strike_price, 1)
            if (t.type == 'Abandon' or (mode == 'Strike' and
                self.isPhysicalDelivery(ins))):
                t.price = 0.0
            # plain digital without barrier, cash settle
            elif ins.digital and not insIsBarrier and ins.settlement == 'Cash':
                if ins.und_instype == 'Curr':
                    price = t.insaddr.contr_size
                    if not ins.call_option:
                        price = -price
                    t.price = create_quotetype_price(ins, price)
                else:
                    t.price = 0.0
                    create_payment = 1
                    pay = ael.Payment.new(t)
                    pay.curr = ins.strike_curr.insaddr
                    pay.type = "Cash"
                    pay.amount = -t.quantity * t.insaddr.contr_size
                    settleDate = _getSettleDateAEL(ins, exerciseDate)
                    pay.payday = settleDate
            else:
                if (ins.digital and not insIsBarrier and
                        ins.settlement != 'Cash'):
                    # plain digital without barrier, physical settle but zero
                    # price when exercised.
                    cash_price = 0.0
                elif ins.digital and insIsBarrier:
                    cash_price = 0.0
                    if ins.und_instype == 'Curr':
                        # FX digital barriers should always cash settle
                        if not ins.call_option:
                            cash_price = -t.insaddr.contr_size
                        else:
                            cash_price = t.insaddr.contr_size
                        price = 0.0
                        t.curr = ins.und_insaddr.insaddr
                        if ins.settlement == 'Physical Delivery':
                            t.curr = ins.und_insaddr.insaddr
                        else:
                            t.curr = ins.strike_curr.insaddr
                else:
                    cash_price = create_price(ins.und_insaddr,
                            price - strike_price)
                if (not ins.curr.insaddr == ins.strike_curr.insaddr):
                    if (ins.und_instype == 'Curr' and
                            ins.curr.insaddr == ins.und_insaddr.insaddr):
                        if not price == 0.0:
                            cash_price = cash_price / price
                    else:
                        exch = fx_rate(ins.strike_curr.insid, ins.curr.insid,
                                None)
                        cash_price = cash_price * exch

                if not ins.call_option:
                    cash_price = -cash_price

                t.price = create_quotetype_price(ins, cash_price)

            # barriers
            if insIsBarrier:
                exotic = ins.exotics()[0]
                self.debugLogBarrier(t, ins, exotic, insIsBarrier)

                if rebate_payment_should_be_created(ins, exotic, price,
                        strike_price):
                    if ins.digital:
                        t.price = 0.0
                    if (ins.settlement == 'Cash' or
                            (not ins.digital and
                            ins.settlement == 'Physical Delivery')):
                        # On non-digital barrier when physical settlement, if
                        # abandon then pay actual cash rebate.
                        if ins.und_instype == 'Curr':
                            t.price = -ins.rebate
                        else:
                            create_payment = 1
                            pay = ael.Payment.new(t)
                            pay.curr = ins.strike_curr.insaddr
                            pay.type = "Cash"
                            pay.amount = -ins.rebate * t.quantity \
                                    * ins.contr_size
        else:
            # FX NDF
            if ins_is_fx_ndf:
                t.reference_price = price
            t.price = price

        t.time = exerciseDate.to_time() + TRADE_TIME - 2
        # For Pay at Hit, use the hit date plus currency pair spot
        if (ins.exotics() and not ins.exotics()[0].barrier_rebate_on_expiry and
            ins.exotics()[0].barrier_cross_date and
            ins.exotics()[0].barrier_crossed_status == 'Confirmed'):
            spotOffset = _getSpotOffset(ins)
            settleDate = _getSettleDateAEL(ins, exerciseDate, spotOffset)
            deliveryDate = _getDeliveryDateAEL(ins, exerciseDate, spotOffset)
        else:
            if (ins.exercise_type == 'American' and
                ins.exp_day > ael.date_today()):
                settleDate = _getSettleDateAEL(ins, ael.date_today())
                deliveryDate = _getDeliveryDateAEL(ins, ael.date_today())
            else:
                # Should use the delivery date
                settleDate = _getSettleDateAEL(ins, exp_day)
                deliveryDate = _getDeliveryDateAEL(ins, exp_day)

        if insIsBarrier:
            # Trade time should be expiry, not barrier-crossed date
            t.time = exp_day.to_time() + TRADE_TIME - 2
            settleDate = _getSettleDateAEL(ins, ins.exp_day)
            deliveryDate = _getDeliveryDateAEL(ins, ins.exp_day)

            if create_payment == 1 and pay:
                pay.payday = settleDate

        t.value_day = t.acquire_day = settleDate

        # Create physical trade if derivative is in the money:
        t_und = None
        if (self.isPhysicalDelivery(ins) == True and
            (exeass == 1 or ins.instype == 'Future/Forward')):
            if (ins.instype in ['Option', 'Warrant'] and
                    ins.und_instype == 'Curr'):
                und_price = 0.0
                if ins.digital:
                    # 4.1 und price and und premium zero for digitals
                    pass
                elif mode == 'Strike':
                    und_price = t.insaddr.strike_price
                elif mode == 'Market':
                    und_price = price
                    und_price = convert_price_to_und_or_strike_quotation(
                            t.insaddr, und_price, 0)
                else:
                    Logme()('No physical trade price available!', 'ERROR')
                # revise: t_und.q=f(cs).
                t_und = t.generate_delivery_trade_for_fxoption(und_price)
                cs = t.insaddr.phys_contr_size
                cs_und = t_und.insaddr.contr_size
                if cs == 0:
                    cs = t.insaddr.contr_size
                if ins.digital or t.insaddr.call_option == 1:
                    t_und.quantity = -t.quantity * cs
                else:
                    t_und.quantity = t.quantity * cs
                t_und.time = t.time
                # This should be delivery date on the option
                t_und.value_day = t_und.acquire_day = deliveryDate
                t_und_acm = acm.FTrade[t_und.trdnbr]
                t_und_acm.DefaultCLS()

            else:
                t_und = copyTrade(t)
                t_und.insaddr = t.insaddr.und_insaddr
                t_und.curr = ('Future/Forward' == ins.instype and
                        t.insaddr.curr or t.insaddr.strike_curr)
                t_und.value_day = t_und.acquire_day = settleDate
                if t_und.insaddr.notional:
                    t_und.insaddr = t.insaddr.und_insaddr.und_insaddr

            if mode == 'Strike':
                if ins.digital:
                    pass
                elif (abs(ins.phys_contr_size) > 0.000001 and
                        abs(ins.phys_contr_size - ins.contr_size) > 0.000001):
                    # p never committed ???
                    p = create_excess_payment(ins, t_und, price)

            t_und.contract_trdnbr = t.contract_trdnbr
            t_und.connected_trdnbr = None
            cs = t.insaddr.phys_contr_size
            cs_und = t_und.insaddr.contr_size
            if cs == 0:
                cs = t.insaddr.contr_size
            if not (ins.instype in [OPTION, WARRANT] and
                    ins.und_instype == 'Curr'):
                if ins.digital or t.insaddr.call_option == 1:
                    t_und.quantity = -t.quantity * cs / cs_und
                else:
                    t_und.quantity = t.quantity * cs / cs_und

            if ins.instype == FUTURES_FORWARD:
                t_und.value_day = t.value_day = ins.exp_day
                t_und.quantity = -t.quantity * cs
                t_und.price = t.price

                # Forwards in Strike mode + Physical delivery should buy the
                # underlying with original trade price of the Forward.
                if t.insaddr.paytype == 'Forward' and mode == 'Strike':
                    t_und.price = originalTradePrice
                    t.price = originalTradePrice

                if t_und.insaddr.instype == 'Bond':
                    avg_price = 0
                    derivative_pos = 0
                    for trade in self.tradesOnDarivative:
                        avg_price = avg_price + trade.price * trade.quantity
                        derivative_pos = derivative_pos + trade.quantity

                    # prevets dividing by
                    if derivative_pos:
                        avg_price = avg_price / derivative_pos
                    else:
                        # exercise/assing is called on closed position
                        avg_price = 0.0

                    t_und.quantity = derivative_pos * cs

                    t_und.price = avg_price if mode == 'Strike' else price
                    conv_factor = 1.0
                    del_link = ael.DeliverableLink.read(
                            'owner_insaddr.insaddr = {0} and '
                            'member_insaddr.insaddr = {1}'.format(
                            ins.und_insaddr.insaddr, t_und.insaddr.insaddr))
                    if del_link:
                        conv_factor = del_link.conversion_factor
                    t_und.price = t_und.price * conv_factor

                    # Quotation adjustment for premium calculation
                    # Temporary change of quotation type of instrument
                    # for purpose of premium adjustment
                    # and calculation of premium.
                    original_ins = t_und.insaddr
                    t_und.insaddr = original_ins.clone()
                    t_und.insaddr.quote_type = ins.quote_type
                    t_und.premium = FBDPCommon.calculate_premium(t_und)

                    # Quotation adjustment for premium caluclation
                    # Set the original instrument of trade
                    t_und.insaddr = original_ins

                    # Price calculation aligned with "old" quotation
                    t_und.price = FBDPCommon.calculate_price_acm(
                        FBDPCommon.ael_to_acm(t_und))

                    # Derivative trade handling
                    if mode == 'Strike':
                        t.price = 0.0
                        t.premium = 0.0
                    else:
                        # Market mode
                        helper_trade = t_und.clone()
                        helper_trade.price = avg_price
                        helper_trade.insaddr = t_und.insaddr.clone()
                        helper_trade.insaddr.quotation_seqnbr =\
                                                ins.quotation_seqnbr
                        helper_trade.premium =\
                            FBDPCommon.calculate_premium_amc(
                            FBDPCommon.ael_to_acm(helper_trade))

                        # Premium on derivative's closing trades is oppside
                        # sing of premium on underlying
                        t.premium = helper_trade.premium - t_und.premium
                        t.price = price - avg_price
                        helper_trade = None
                else:
                    # Quotation adjustment for premium calculation
                    # Temporary change of quotation type of instrument
                    # for purpose of premium adjustment
                    # and calculation of premium.
                    original_und = t_und.insaddr
                    t_und.insaddr = t_und.insaddr.clone()
                    t_und.insaddr.quotation_seqnbr = ins.quotation_seqnbr
                    t_und.premium = FBDPCommon.calculate_premium_amc(
                            FBDPCommon.ael_to_acm(t_und))

                    # Set original instrument of trade
                    t_und.insaddr = original_und
                    t_und.price = FBDPCommon.calculate_price_acm(
                            FBDPCommon.ael_to_acm(t_und))

            elif (ins.instype in ['Option', 'Warrant'] and ins.digital):
                t_und.price = 0.0
            elif not (ins.instype in ['Option', 'Warrant'] and
                    ins.und_instype == 'Curr'):
                if mode == 'Strike':
                    t_und.price = t.insaddr.strike_price
                elif mode == 'Market':
                    t_und.price = price
                    t_und.price = convert_price_to_und_or_strike_quotation(
                            t.insaddr, t_und.price, 0)
                else:
                    Logme()('No physical trade price available!', 'ERROR')

            t_und = self._setUnderlyingTradeProcess(ins, t_und)
            payoff = price - t.insaddr.strike_price
            self._applyLotSizeOnAel(t_und, t, payoff)
            if exercise_trade_hook:
                t_und = exercise_trade_hook(ins, t_und)
            t_und.premium = FBDPCommon.calculate_premium(t_und)
            self.add_exercise_trade(dependent, t_und, \
                isSingleTradePosition, dealpackage)
            n += 1

        if self.closeAll:
            t.quantity = quantityAll

        if exercise_trade_hook:
            t = exercise_trade_hook(ins, t.new())

        if ins.paytype in ['Future', 'Forward']:
            if ins.und_instype != BOND:
                t.premium = 0.0
        else:
            t.premium = FBDPCommon.calculate_premium(t)

        self.add_exercise_trade(dependent, t, isSingleTradePosition, \
            dealpackage)
        if create_payment == 1 and pay:
            Logme()('trade payment. {0}'.format(pay.pp()), 'DEBUG')
        Summary().ok(Summary().POSITION, summaryType)

        if n == 0:
            Logme()("No underlying trade done.", 'DEBUG')
        ael.poll()
        hook = additional_excercise_trades_hook
        if hook:
            add_trades = hook(t.new(), t_und and t_und.new(), price,
                    self.param)
            if add_trades:
                msg = ('Adding {0} extra trades from '
                        '\'additional_excercise_trades\' hook.'.format(
                        len(add_trades)))
                Logme()(msg, 'DEBUG')
                self.rollbackWrapper.beginTransaction()
                for trade in add_trades:
                    self.add_exercise_trade(dependent, trade,
                        isSingleTradePosition, dealpackage)
                try:
                    self.rollbackWrapper.commitTransaction()
                except Exception as e:
                    self.rollbackWrapper.abortTransaction()
                    Logme()('Could not commit trades defined in '
                            'additional_excercise_trades hook.', 'ERROR')
                    raise e
        ael.poll()

    def getManualOverride(self, ins):
        """
        Return the manually defined exercise or abandon action, if any, or
        None otherwise.
        """
        if self.actionsForTrades:
            for t in ins.trades():
                if t.trdnbr in self.actionsForTrades:
                    action = self.actionsForTrades[t.trdnbr]
                    msg = ('Found {0}: {1}.'.format(t.trdnbr, action))
                    Logme()(msg, 'DEBUG')
                    if action == 'Exercise' or action == 'Abandon':
                        return action
        return None

    def getExerciseDate(self, ins):
        """
        Return the exercise date of the instrument (as an ael_date).
        """
        if FBDPCommon.is_acm_object(ins):
            ins = FBDPCommon.acm_to_ael(ins)
        if ins.insid in self.insDates:
            return self.insDates[ins.insid]

        exotic = ins.exotics()[0] if ins.exotics() else None
        isKnockIn = 0
        isOneTouch = 0
        isKnockOut = 0
        isNoTouch = 0
        if exotic:
            isKnockIn, isKnockOut, isOneTouch, isNoTouch = \
                        getOptionType(exotic)

        #get the exercise date
        if (exotic and isBarrier(ins) and
                (isOneTouch or isKnockOut or isNoTouch) and
                exotic.barrier_cross_date and
                exotic.barrier_crossed_status == 'Confirmed'):
            date = exotic.barrier_cross_date
            # exercise date for exotic option is right without code bellow
            # if exotic.barrier_rebate_on_expiry:
            #     date = ins.exp_day
        elif ins.exp_day and ins.exp_day <= ael.date_today():
            date = ins.exp_day
        else:
            date = ael.date_today()
        t = ael.date(time.strftime('%Y %m %d', time.localtime(ins.exp_time)))
        if t <= date and t > ael.date('1970-01-02'):
            date = t
        self.insDates[ins.insid] = date
        return date

    def debugLogBarrier(self, t, ins, exotic, insIsBarrier):
        msg = ('Settlement {0} |digital {1} |barrier {2} |dbtype {3} '
            '|crossed {4} |btype {5}'.format(t.insaddr.settlement,
            ins.digital, insIsBarrier, exotic.digital_barrier_type,
            exotic.barrier_crossed_status, exotic.barrier_option_type))
        Logme()(msg, 'DEBUG')

    def debugLogInOrOutTheMoney(self, inOut, ins, posName):
        msg = '\nPosition {0} skipped.'.format(posName)
        if inOut == 'In':
            param = 'Exercise ITM'
        else:
            param = 'Abandon OTM and ATM'
        msg += ('\nReason: instrument {0} is {1}-The-Money and the \'{2} '
                'Normal Trades\'-parameter is untoggled.'.format(ins.insid,
                inOut, param))
        Logme()(msg, 'DEBUG')

    def add_exercise_trade(self, aelDependent, aelTradeToAdd,
            isSingleTradePosition, dealpackage):
        if isSingleTradePosition:
            tradeNbr = 0
            try:
                tradeNbr = aelDependent.trdnbr
            except:
                if self.preview:
                    aelTradeToAdd.status = 'Simulated'
                self.rollbackWrapper.add_trade(aelTradeToAdd)
                self.add_trade_link(aelTradeToAdd, dealpackage)
                return
            acmTradeToExercise = acm.FTrade[tradeNbr]
            mirrorPortfolio = acmTradeToExercise.CounterPortfolio()
            if mirrorPortfolio:
                acmTradeToAdd = acm.FTrade[aelTradeToAdd.trdnbr]
                acmTradeToAdd.MirrorPortfolio(mirrorPortfolio)
                if self.preview:
                    acmTradeToAdd.Status('Simulated')
                self.rollbackWrapper.add_trade(acmTradeToAdd)
                self.add_trade_link(acmTradeToAdd, dealpackage)
                self.rollbackWrapper.logCreatedMirrorTrade(acmTradeToAdd)
            else:
                if self.preview:
                    aelTradeToAdd.status = 'Simulated'
                self.rollbackWrapper.add_trade(aelTradeToAdd)
                self.add_trade_link(aelTradeToAdd, dealpackage)
        else:
            if self.preview:
                aelTradeToAdd.status = 'Simulated'
            self.rollbackWrapper.add_trade(aelTradeToAdd)
            self.add_trade_link(aelTradeToAdd, dealpackage)


# ___end class Exercise___


def exp_day_to_date(ins):
    """
    Function for converting the exp_day to true exp_day
    """
    a_day = 24 * 60 * 60
    if ins.exp_time > a_day and ins.exp_time < 2 * a_day:
        return ins.exp_day.add_days(-1)
    else:
        return ins.exp_day


def fx_rate(currid1, currid2, date):
    """
    curr1.used_price(date, currid2)
    """
    curr1 = acm.FInstrument[currid1]
    curr2 = acm.FInstrument[currid2]
    if None == date:
        date = acm.Time().DateNow()
    return curr1.Calculation().MarketPrice(space, date, 0,
            curr2).Value().Number()

def instrument_accrued_interest(insid, date):
    """
    ins.interest_accrued(date)
    """
    acc = acm.FInstrument[insid].Calculation().AccruedInterest(space, None,
            date, None)
    return acc.Value()

def isBarrier(ins):
    """
    function returns one if instrument is a barrier option, else zero
    """
    if (ins.record_type == 'Instrument' and ins.instype == 'Option' and
            ins.exotic_type == 'Other' and ins.exotics() and
            ins.exotics()[0] and
            ins.exotics()[0].barrier_option_type != 'None'):
        return 1
    return 0

def isAsianOption(ins):
    instr = _getACMInstr(ins)
    return instr.IsKindOf(acm.FOption) and instr.IsAsian()

def isCliquetOption(ins):
    instr = _getACMInstr(ins)
    exoticEvents = instr.ExoticEvents()
    for event in exoticEvents:
        if event.Type() == 'Cliquet date':
            return True

    return False

def isCombination(ins):
    instr = _getACMInstr(ins)
    return instr.IsKindOf(acm.FCombination)

def insIsSwaption(ins):
    """
    Function returns 1 if instrument is a swaption, otherwise 0
    """
    if (ins.record_type == 'Instrument' and ins.instype == 'Option' and
            ins.und_insaddr.instype == 'Swap'):
        return 1
    return 0

def suggest_abandon_price(ins, date=None):
    if not date:
        try:
            date = exp_day_to_date(ins)
        except:
            date = ael.date_today()
    if ins.instype in ['Option', 'Warrant']:
        return 0.0
    elif ins.instype == 'Future/Forward':
        settle_price = FBDPInstrument.find_price(ins, date,
                settlement_market='SETTLEMENT')
        if not settle_price:
            errorMsg = ('No settlement price found for {0} on date '
                    '{1}'.format(ins.insid, date))
            raise AttributeError(errorMsg)
        return settle_price
    elif ins.instype == 'Bond':
        return 100.0
    else:
        return 0.0

def trade_premium_from_quote(trdnbr, quote, date):
    return FBDPCommon.trade_premium_from_quote(acm.FTrade[trdnbr], quote, date)

def trade_spot_date(trdnbr, date):
    """
    trade.spot_date(date)
    """
    return acm.FTrade[trdnbr].Instrument().GetSpotDay(date, None)

def rebate_payment_should_be_created(ins, exotic, price, strike_price):
    isOutBarrier = (exotic.barrier_option_type in
            ('Double Out', 'Down & Out', 'Up & Out'))
    digital_type = exotic.digital_barrier_type
    crossed = exotic.barrier_crossed_status
    call = ins.call_option
    diff = price - strike_price
    if ins.rebate == 0:
        return False

    if (ins.digital and (isOutBarrier and crossed == 'None' or
            not isOutBarrier and crossed == 'Confirmed')):
        if (digital_type == 'Barrier' or (call and diff > 0) or
                (not call and diff < 0)):
            return True
    elif (not ins.digital and (isOutBarrier and crossed == 'Confirmed' or
            not isOutBarrier and crossed == 'None')):
        return True
    return False


def convert_price_to_und_or_strike_quotation(ins, price,
        convert_to_und_quotation):
    """
    function returns the price converted to either the underlying quotation or
    the strike quotation.
    """
    if ins.record_type == 'Instrument' and ins.und_insaddr:
        if (ins.und_insaddr.quotation_seqnbr and
                ins.strike_quotation_seqnbr and (ins.strike_quotation_seqnbr
                != ins.und_insaddr.quotation_seqnbr)):
            instr = acm.FInstrument[ins.insaddr]
            und_instr = acm.FInstrument[ins.und_insaddr.insaddr]
            date_today = acm.Time().DateToday()
            # doubleCast = acm.GetFunction('double', 1)
            denom_func = acm.GetFunction('denominatedvalue', 4)
            if (convert_to_und_quotation == 1):
                if instr.IsKindOf(acm.FOption):
                    denom_val = denom_func(price, instr.StrikeCurrency(), None,
                            ael.date_today())
                else:
                    denom_val = denom_func(price, instr.Currency(), None,
                            ael.date_today())
                to_quotation = und_instr.Quotation()
                from_quotation = instr.StrikeQuotation()
            else:
                denom_val = denom_func(price, und_instr.Currency(), None,
                        ael.date_today())
                from_quotation = und_instr.Quotation()
                to_quotation = instr.StrikeQuotation()

            lprice_denom_val = instr.QuoteToQuote(denom_val, date_today,
                    None, None, from_quotation, to_quotation)
            lprice = lprice_denom_val.Number()

            return lprice
    return price


def copyTrade(t):
    d = fieldsFromTemplate(t, exclude=('trdnbr',))
    t = ael.Trade.new(t.insaddr)
    for key, value in d.items():
        setattr(t, key, value)
    return t


def fieldsFromTemplate(t, exclude=()):
    d = {}
    for c in t.columns():
        if c not in exclude:
            try:
                d[c] = getattr(t, c)
            except AttributeError:
                Logme()(c, "ERROR")
    return d


def create_accrued_payment(t):
    accrued = (instrument_accrued_interest(t.insaddr.insid,
            t.value_day).Value().Number() * t.quantity)
    p = ael.Payment.new(t)
    p.payday = t.value_day
    p.amount = -float(accrued)
    p.curr = t.curr
    p.type = 'Cash'
    p.ptynbr = t.counterparty_ptynbr
    p.text = 'Accrued Interest'
    p.valid_from = ael.date_from_time(t.time)

    s = ('Created Accrued Interest Payment: {0}, {1}'.format(p.amount,
            p.curr.insid))
    Logme()(s, 'DEBUG')
    return p


def create_excess_payment(ins, t_und, settle):
    if not (ins.instype == 'Option'):
        s = ('Trying to create Exercise Payment for {0}: {1}.  Excess '
                'payments can only be created for Options.'.format(
                ins.instype, ins.insid))
        Logme()(s, 'ERROR')
        Logme()(None, 'ABORT')
        raise RuntimeError

    excess_lots = ins.contr_size - ins.phys_contr_size
    strike_price = convert_price_to_und_or_strike_quotation(ins,
            ins.strike_price, 1)
    if ins.call_option == 1:
        trade_price = FBDPCommon.create_quotetype_price(ins,
                settle - strike_price)
    else:
        trade_price = FBDPCommon.create_quotetype_price(ins,
                strike_price - settle)

    premium = trade_premium_from_quote(t_und.trdnbr, trade_price,
            t_und.acquire_day)
    pmnt_amount = premium * excess_lots

    p = ael.Payment.new(t_und)
    p.payday = ael.date(trade_spot_date(t_und.trdnbr,
            ael.date_from_time(t_und.time)))
    p.amount = float(pmnt_amount)
    p.curr = t_und.curr
    p.type = 'Exercise Cash'
    p.ptynbr = t_und.counterparty_ptynbr
    p.valid_from = ael.date_from_time(t_und.time)

    s = ('Created Exercise Payment: {0}\nCurr: {1}'.format(p.amount,
        p.curr.insid))
    Logme()(s)
    return p
