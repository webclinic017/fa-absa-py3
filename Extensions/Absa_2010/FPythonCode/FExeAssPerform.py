""" Compiled: 2013-04-12 13:37:02 """

"""----------------------------------------------------------------------------
MODULE
    FExeAssPerform - Module that executes ExerciseAssign.

    (c) Copyright 2011 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This module executes the Exercise/Assign procedure based on the
    parameters passed from the scripts FExerciseAssign or FManualExercise.

----------------------------------------------------------------------------"""

from FBDPCurrentContext import Logme, Summary
from collections import namedtuple
import FBDPCalculatePosition
import FBDPCommon
import FBDPInstrument
import FBDPRollback
import FFxCommon
import acm
import ael
import time
from FTimeUtils import get_time_in_seconds

# ====================== Calc space for Standard Calculations =================


space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()


# Attempt to get FBDPHook.exercise_trade hook and
# FBDPHook.additional_excercise_trades
exercise_trade_hook = None
additional_excercise_trades_hook = None
try:
    import FBDPHook
    reload(FBDPHook)
    exercise_trade_hook = FBDPHook.exercise_trade
except:
    Logme()('No FBDPHook.exercise_trade hook.', 'DEBUG')
try:
    import FBDPHook
    reload(FBDPHook)
    additional_excercise_trades_hook = FBDPHook.additional_excercise_trades
except:
    Logme()('No FBDPHook.additional_excercise_trades hook.', 'DEBUG')


#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------


TRADE_TIME = get_time_in_seconds()
abandon_types = ['Option', 'Warrant', 'Future/Forward', 'Bond']

# Trading Manager columns for Asian options
AV_PRICE = "Asian Average Price So Far"
AV_STRIKE = "Asian Average Strike So Far"

# Logging levels
DEBUG = 'DEBUG'
WARNING = 'WARNING'
ERROR = 'ERROR'

# Script actions and trade types for closing/ exercise/ assign trade
EXERCISE = 'Exercise'
ASSIGN = 'Assign'
ABANDON = 'Abandon'

# Settlement options
PHYSICAL_SETTLEMENT = "Physical Delivery"
CASH_SETTLEMENT = "Cash"

# Price modes for physical delivery
STRIKE_PRICE = 'Strike'
MARKET_PRICE = 'Market'

# Instrument types
OPTION = 'Option'
CURRENCY = 'Curr'

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

TODAY = acm.Time().DateToday()

ClosingPrice = namedtuple('ClosingPrice', ['underlying', 'derivative'])


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
    """ gets settle date:
    either gets the defined value from the instrument (if set)
    or calculates it according to the offset
    
    accepts acm instrument
    """
    settle_date = acm.FInstrumentLogicDecorator(instrument, None).DeliveryDate()
    if settle_date:
        # Override the dates with delivery date.
        # This fixes the problem where dual calendars affect the option.
        # Value day of the underlying got changed in the original process.
        return ael.date_from_string(settle_date)
    else:
        # Default behavior, copied from the DEFAULT module
        if offset == None:
            offset = instrument.PayDayOffset()
        if instrument.PayOffsetMethod() == BUSINESS_DAYS:
            if FBDPCommon.has_attr(instrument, 'StrikeCurrency'):
                calendar = instrument.StrikeCurrency().Calendar()
            else:
                calendar = instrument.Currency().Calendar()
            
            adjusted_date = calendar.AdjustBankingDays(tradeDate, offset)
            usd_adjusted_date = _getUSDAdjustedDate(adjusted_date, calendar)
            if adjusted_date != usd_adjusted_date:
                print 'Settle date has been adjusted to USD calendar'
            
            return usd_adjusted_date
        return acm.Time.DateAddDelta(tradeDate, 0, 0, offset)

def _getUSDAdjustedDate(trade_date, original_calendar):
    """ Returns the adjusted date so that it is not a holiday
    in all CCYs involved (i.e. Primary, Secondary and USD)
    
    the USD calendar is considered under every circumstance
    because all the Cross CCY pairs are split against USD. 
    """
    # adjust to USD calendar
    usd_calendar = acm.FInstrument['USD'].Calendar()
    if usd_calendar == original_calendar:
        return trade_date 
    is_usd_banking_day = not usd_calendar.IsNonBankingDay(None, None, trade_date)
    if is_usd_banking_day:
        return trade_date
    usd_adjusted_date = usd_calendar.AdjustBankingDays(trade_date, 1)
    # have to make sure that the new date is not a holiday according to the original calendar
    adjusted_date = original_calendar.AdjustBankingDays(trade_date, 1)
    if adjusted_date == usd_adjusted_date:
        return adjusted_date
    else:
        return _getUSDAdjustedDate(adjusted_date, original_calendar)

def _getSettleDateAEL(ins, date, offset=None):
    instrument = FBDPCommon.ael_to_acm(ins)
    Date = FBDPCommon.toDate(str(date))
    settleDate = _getSettleDate(instrument, Date, offset)
    settleDateAEL = FBDPCommon.toDateAEL(str(settleDate))
    return settleDateAEL


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
    quote = underlying.DenominatedValueSpot(quote, TODAY)
    underlyingPrice = underlying.QuoteToUnitValue(quote, TODAY, True, None,
            None, underlying.Quotation(), 1.0, 0.0)
    derivPrice = option.UnitValueToQuote(underlyingPrice, TODAY, TODAY, True,
            None, None, option.Quotation(), 1.0, 0.0).Number()
    return derivPrice


def _getClosingPrice(option, priceMode):
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
    for p in dup.Payments():
        p.Delete()
    dup = _linkTrades(dup, linkTrade)
    return dup


def _createClosingTrade(posTrade, linkTrade, tradeDate, settleDate):
    dup = _copyTrade(posTrade, linkTrade)
    dup.TradeTime(tradeDate)
    dup.ValueDay(settleDate)
    dup.AcquireDay(settleDate)

    dup.Price(0.)
    dup.Quantity(-posTrade.Quantity())
    dup.Premium(0.)
    dup.Type(ABANDON)
    return dup


def _createDerivativeTrade(posTrade, linkTrade, tradeDate, settleDate, price):
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
    return dup


def _logExerciseCondition(option, exercise):
    Logme()(50 * '-', DEBUG)
    msg = ("{0} {1} option {2}:".format(
        ('Abandoning', 'Exercising/ Assigning')[exercise],
        ('put', 'call')[option.instrument.IsCallOption()],
        option.instrument.Name()))
    Logme()(msg, DEBUG)
    Logme()("Settle price = {0}".format(option.settlePrice), DEBUG)
    Logme()("Strike price = {0}".format(option.strike), DEBUG)
    Logme()(50 * '-', DEBUG)


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
    def __init__(self, ins, market=''):
        self.instrument = _getACMInstr(ins)
        assert self.instrument.InsType() == OPTION, ("{0} ({1}) is not an "
                "Option.".format(self.instrument.Name(),
                    self.instrument.InsType()))
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


class AsianOption(BaseOption):
    def __init__(self, ins, market=''):
        super(AsianOption, self).__init__(ins, market)
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


def perform_exercise_assign(args):
    """
    Entry point for the Exercise operation
    """
    FBDPCommon.callSelectionHook(args, 'trades', 'exercise_assign_selection')
    e = Exercise('Exercise Assign', args['Testmode'], args)
    e.perform()
    e.end()

    # Fix physically settled future closeouts. Please see JIRA ABITFA-2562
    # for more detail about this fix.
    if args['DoFixPhysicals']:
        fixPhysicals(args['trades'], args['Testmode'])


class PhysicalsFixingError(StandardError):
    """An error during futures fixing."""


def fixPhysicals(input_trades, testRun):
    Logme()("Fixing physically settled futures' and options' dates.")

    CLOSING_TYPES = ('Exercise', 'Abandon', 'Closing', 'Assign')
    COUNTERPARTIES = ['FMAINTENANCE', 'JSE CLEAR']

    wrongTrades = []
    # Go through all the positions (portfolio/instrument) and collect all
    # the wrong future trades.

    for trade_number in input_trades:
        trade = acm.FTrade[trade_number]
        instrument = trade.Instrument()

        # Only work on Futures on Stocks.
        if instrument.InsType() not in ('Future/Forward', 'Option'):
            continue

        if instrument.Underlying().InsType() != 'Stock':
            continue

        # Get rid of cash-settled futures.
        if instrument.SettlementType() != PHYSICAL_SETTLEMENT:
            continue

        # Select trades which could be wrongly booked.
        query = acm.CreateFASQLQuery('FTrade', 'AND')
        query.AddAttrNode('Portfolio.Name', 'EQUAL', trade.Portfolio().Name())
        query.AddAttrNode('Instrument.Name', 'EQUAL', trade.Instrument().Name())
        query.AddAttrNode('ValueDay', 'GREATER', acm.Time().AsDate(trade.Instrument().ExpiryDate()))  # when using datetime, an internal error is raised
        # query.AddAttrNode('Acquirer.Name', 'EQUAL', FMAINTENANCE)
        orNode = query.AddOpNode('OR')
        for cpty in COUNTERPARTIES:
            orNode.AddAttrNode('Counterparty.Name', 'EQUAL', cpty)
        # query.AddAttrNode('Trader.Name', 'EQUAL', FMAINTENANCE)
        query.AddAttrNode('Status', 'NOT_EQUAL', 'Void')
        orNode = query.AddOpNode('OR')
        for closing_type in CLOSING_TYPES:
            orNode.AddAttrNode('Type', 'EQUAL', closing_type)

        candidateTrades = query.Select()
        # Further filter out only trades executed on the expiry date.
        for candidateTrade in candidateTrades:
            tradeDate = acm.Time.DateFromTime(candidateTrade.TradeTime())
            executionDate = acm.Time.DateFromTime(candidateTrade.ExecutionTime())
            expiryDate = candidateTrade.Instrument().ExpiryDateOnly()
            
            if tradeDate == executionDate and tradeDate == expiryDate:
                wrongTrades.append(candidateTrade)
            
    Logme()('{0} wrong trades found.'.format(len(wrongTrades)))

    if testRun:
        Logme()('Test run - no changes made.')
        return

    successful = []
    failed = []
    for trade in wrongTrades:
        try:
            expiry = trade.Instrument().ExpiryDate()
            trade.ValueDay(expiry)
            trade.AcquireDay(expiry)
            trade.Commit()
            successful.append(trade)
        except Exception as ex:
            failed.append((trade, ex))

    Logme()('Successfully amended {0} trades.'.format(len(successful)))

    if failed:
        Logme()('Problem with amending of {0} trades:'.format(
            len(failed)), ERROR)
        for (trade, ex) in failed:
            Logme()('Trade {0}: {1}'.format(trade.Oid(), ex))

    Logme()('Fixing done.')


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


class Exercise(FBDPRollback.RollbackWrapper, object):

    def readArguments(self):
        if 'actions_for_trades' in self.ael_variables_dict:
            Logme()('Found \'actions_for_trades\' in ael_variables.', 'DEBUG')
            # Turn the parameter (a string) back into a real dictionary.
            self.actionsForTrades = eval(
                    self.ael_variables_dict['actions_for_trades'])
        else:
            msg = ('Failed to find \'actions_for_trades\' in ael_variables -- '
                    'this is a problem if you are running FManualExercise.')
            Logme()(msg, 'DEBUG')
            self.actionsForTrades = None
        self.doExeAssign = self.ael_variables_dict['DoExeAss']
        self.doAbandon = self.ael_variables_dict['DoAbandon']
        self.mode = self.ael_variables_dict['mode']
        settlePrice = self.ael_variables_dict['settle_price']
        if settlePrice:
            self.settlePrice = float(str(settlePrice).replace(',', '.'))
        else:
            self.settlePrice = 0.
        self.settleMarket = self.ael_variables_dict['settlemarket']
        self.givenTradeIds = self.ael_variables_dict['trades']

    def getPositions(self):
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

    def _createOption(self, ins):
        """
        Initializing method for creating exercise/ assign Option
        classes. Add to this method if creating new Option types for use in the
        new run() loop.
        """
        if isAsianOption(ins):
            return AsianOption(ins, self.settleMarket)

    def _abandon(self, option, positions, exDate):
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
                abandoned = _createClosingTrade(trade, link, exDate,
                        settleDate)
                self.add_trade(abandoned)

    def _exerciseAssign(self, option, positions, exDate):
        settleDate = _getSettleDate(option.instrument, exDate)
        cashSettle = option.instrument.SettlementType() == CASH_SETTLEMENT
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
                    continue

                link = _getLinkedTrade(trade, orgTrades, multiCurr)
                derivTrade = _createDerivativeTrade(trade, link, exDate,
                    settleDate, closingPrice.derivative)
                self.add_trade(derivTrade)

                if not cashSettle:
                    underlying = _createUnderlyingTrade(trade, link, exDate,
                        settleDate, closingPrice.underlying)
                    self.add_trade(underlying)

    # New loop for exercising or abandoning instruments.
    def run(self, ins, positions):
        manualAction = self.getManualOverride(ins)
        option = self._createOption(ins)
        exDate = self.getExerciseDate(ins).to_string(ael.DATE_ISO)

        if not option.canExercise(exDate):
            Logme()("{0}-style option {1} cannot be exercised on {2}.".format(
                option.instrument.ExerciseType(), option.instrument.Name(),
                exDate), WARNING)
            return

        if self.doExeAssign or manualAction == EXERCISE:
            if option.shouldExercise(exDate, self.settlePrice):
                self._exerciseAssign(option, positions, exDate)
                return

        if self.doAbandon or manualAction == ABANDON:
            self._abandon(option, positions, exDate)

        # TODO: Hooks

    def perform(self):
        self.insDates = {}

        # read given arguments
        self.readArguments()

        # Populate instrument dictionary with traded portfolios
        positions = self.getPositions()
        # positioning after hook recalculate_position
        hookArguments = {}
        try:
            from FBDPHook import recalculate_position
            hookArguments = self.ael_variables_dict
        except:
            pass

        for (ins, portfolios) in positions.items():
            manualAction = self.getManualOverride(ins)
            insIsBarrier = isBarrier(ins)
            date = self.getExerciseDate(ins)
            if hookArguments:
                portfolios = []

            # it is necessary to recalculate the position for each portfolio
            # otherwise, the calculated position may be outdated after adding
            # the close out and underlying trades.
            # see ABITFA-2410
            for p in portfolios:
                calcPositions = FBDPCalculatePosition.calculatePosition(ins,
                        end_date=date, portfolio=[p],
                        hookArguments=hookArguments)

                if isAsianOption(ins):
                    try:
                        # Convert calcPositions to ACM trades.
                        calcPositions = FBDPCalculatePosition.convertPositions(
                                calcPositions, toAel=False)
                        self.run(ins, calcPositions)
                    except ValidationError as e:
                        Logme()('Validation error processing {0}: {1}'.format(
                            ins.insid, e), ERROR)
                    except acm.FException as e:
                        Logme()('ACM error processing {0}: {1}'.format(ins.insid,
                            e), ERROR)
                    continue

                for pos in calcPositions:
                    calcTrades = pos[0]
                    dependTrades = pos[1]
                    port = calcTrades[0].prfnbr
                    posName = '[{0}:{1}]'.format((port and port.prfid or 'None'),
                                ins.insid)

                    if len(calcTrades) > 1:
                        useCurrencyDependency = True
                    else:
                        useCurrencyDependency = False
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
                        self.adjustPosition(ins, trd, depTrade, date, posName,
                                manualAction, insIsBarrier,
                                len(dependTrades) <= 1)

                        Exercise._fix_contract_trd_links(trd.contract_trdnbr)

    @staticmethod
    def _fix_contract_trd_links(trdnbr):
        """ Sets the ContractTrd value to the correct mirror trade number

        trdnbr - Trade number
        """
        # When exercising an FX Option, with a mirror trade, the script creates
        # four new trades. Two trades reference the FX Option, while other two
        # reference themselves. It is necessary to reference the mirror trade.
        # The first two trades reference (mirror) the trades that have to be
        # updated.

        o_trd = acm.FTrade[trdnbr]  # original trade
        if not o_trd:
            return
        m_trd = o_trd.MirrorTrade()  # mirror trade
        if not m_trd:
            return

        cmd = ("contractTrdnbr = {0} and oid<>{0} "
               "and mirrorTrade<>{1}").format(trdnbr, m_trd.Oid())
        o_exercise_trds = acm.FTrade.Select(cmd)

        if not o_exercise_trds:
            return

        for trd in o_exercise_trds:
            mirror_trd = trd.MirrorTrade()
            trd_clone = mirror_trd.Clone()
            trd_clone.ContractTrdnbr(m_trd.Oid())
            mirror_trd.Apply(trd_clone)
            mirror_trd.Commit()

    def adjustPosition(self, ins, trd, dependent_, date, posName, manualAction,
            insIsBarrier, isSingleTradePosition):
        Logme()('- ' * 23, 'DEBUG')
        Logme()('Processing {0}'.format(ins.insid), 'DEBUG')
        ignoreMsg = self.checkTradePosition(ins, trd, posName, manualAction,
                insIsBarrier)
        if ignoreMsg:
            Summary().ignore(Summary().POSITION, Summary().action, ignoreMsg,
                    posName)
            return

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

        if ins.instype == 'Future/Forward':
            return self.abandon(ins,
                    trd,
                    date,
                    settle,
                    mode=self.mode,
                    name=posName,
                    dependent=dependent_,
                    isSingleTradePosition=isSingleTradePosition)

        # Barrier Options
        if insIsBarrier:
            (errMsg, type) = self.checkBarrierOption(ins, posName,
                    manualAction)
            if errMsg:
                args = [Summary().POSITION, Summary().action, errMsg, posName]
                if type == 'fail':
                    Summary().fail(*args)
                else:
                    Summary().ignore(*args)
                return

        # Check if derivative is in-the-money.
        InTheMoney = 0
        strike_price = convert_price_to_und_or_strike_quotation(ins,
                ins.strike_price, 1)
        if insIsEuropeanSwaption:
            if settle:
                InTheMoney = 1
        elif ((ins.call_option == 1 and strike_price < settle) or
                (ins.call_option == 0 and strike_price > settle)):
            # ExeAss = 1 => in-the-money
            InTheMoney = 1
        ExeAss = 0
        Abandon = 0

        actionFromInTheMoney = True
        # If the user has changed the default value 'Normal' value of the
        # 'Action' column in the Trade Sheet, always do what the user says,
        # period.
        if manualAction in ['Exercise', 'Abandon', 'Skip']:
            actionFromInTheMoney = False
            msg = ('Manual override for {0}: {1}.'.format(trd.trdnbr,
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
                    if InTheMoney:
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
                    if InTheMoney:
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
            if InTheMoney:
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

        self.abandon(ins,
                    trd,
                    date,
                    settle,
                    exeass=ExeAss,
                    mode=self.mode,
                    aba=Abandon,
                    dependent=dependent_,
                    name=posName,
                    insIsBarrier=insIsBarrier,
                    isSingleTradePosition=isSingleTradePosition)

    def checkTradePosition(self, ins, trd, posName, manualAction,
            insIsBarrier):
        if trd.quantity == 0:
            if manualAction:
                Summary().warning(Summary().POSITION, Summary().action,
                        'MANUALLY OVERRIDING: Zero position',
                        '{0}'.format(posName))
            else:
                return 'Zero position'

        if not ins.instype in ['Option', 'Warrant', 'Future/Forward']:
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
        if (ins.exercise_type == 'European'
                and ins.exp_day > ael.date_today()
                and not insIsBarrier):
            if manualAction:
                msg = 'MANUALLY OVERRIDING: European option with Expiry > Today'
                Summary().warning(Summary().POSITION, Summary().action, msg, posName)
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

        isConfirmedKnockInEuropean   =  (exotic.barrier_option_type in ('Down & In', 'Up & In')
            and exotic.barrier_crossed_status == 'Confirmed' and ins.exercise_type == 'European')


        # include all knocked barriers, but not the european
        if (exotic.barrier_crossed_status == 'Confirmed' and
                not ins.exercise_type == 'European'):
            include = 1
        # include all expired options
        if ins.exp_day <= ael.date_today() and not isConfirmedKnockInEuropean:
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

    def abandon(self, ins, cp, exerciseDate, price, exeass=0, mode='Strike',
            aba=1, dependent=None, name=None, insIsBarrier=False,
            isSingleTradePosition=False):
        """
        Close/Abandon/Exercise/Assign a position. For future/forward a price
        can be given
        """
        if ins.instype not in abandon_types:
            msg = ('To Exercise/Assign/Abandon/Close positions in instruments '
                    'with instype {0} is not supported'.format(ins.instype))
            Logme()(msg, 'WARNING')
            return

        exp_day = exp_day_to_date(ins)
        n = 0
        originalTradePrice = cp.price
        t = cp.new()

        for p in t.payments():
            p.delete()
        t.quantity = -t.quantity
        t.curr = t.insaddr.curr
        if t.quantity == 0.0:
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

        ins_is_fx_ndf = (t.insaddr.instype == 'Future/Forward' and
                t.insaddr.und_instype == 'Curr' and
                t.insaddr.paytype == 'Forward' and
                t.insaddr.settlement == 'Cash')

        if price == None:
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
                t.disc_type_chlnbr = dependent.disc_type_chlnbr
            t.price = price

        t.time = exerciseDate.to_time() + TRADE_TIME - 2
        # For Pay at Hit, use the hit date plus currency pair spot
        if (ins.exotics() and not ins.exotics()[0].barrier_rebate_on_expiry and
            ins.exotics()[0].barrier_cross_date and
            ins.exotics()[0].barrier_crossed_status == 'Confirmed'):
            spotOffset = _getSpotOffset(ins)
            settleDate = _getSettleDateAEL(ins, exerciseDate, spotOffset)
        else:
            # Should use the delivery date
            settleDate = _getSettleDateAEL(ins, ins.exp_day)

        if insIsBarrier:
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

                # Upgrade 2010->2013: custom code adding two addinfos
                def check_or_set_addinfo(name, value):
                    if (not t_und.add_info(name) or
                            t_und.add_info(name) != value):
                        ais = ael.AdditionalInfoSpec[name]
                        ai = ael.AdditionalInfo.new(t_und)
                        ai.addinf_specnbr = ais
                        ai.value = value
                check_or_set_addinfo('BOTicketPrinted', 'Unprinted')
                check_or_set_addinfo('MIDAS_MSG', 'Not Sent')

                cs = t.insaddr.phys_contr_size
                cs_und = t_und.insaddr.contr_size
                if cs == 0:
                    cs = t.insaddr.contr_size
                if ins.digital or t.insaddr.call_option == 1:
                    t_und.quantity = -t.quantity * cs
                else:
                    t_und.quantity = t.quantity * cs
                t_und.time = t.time
                t_und.value_day = t.value_day
                t_und.acquire_day = t.acquire_day
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
            if not (ins.instype in ['Option', 'Warrant'] and
                    ins.und_instype == 'Curr'):
                if ins.digital or t.insaddr.call_option == 1:
                    t_und.quantity = -t.quantity * cs / cs_und
                else:
                    t_und.quantity = t.quantity * cs / cs_und

            if ins.instype == 'Future/Forward':
                t_und.quantity = -t.quantity * cs / cs_und
                t_und.price = t.price

                # Forwards in Strike mode + Physical delivery should buy the
                # underlying with original trade price of the Forward.
                if t.insaddr.paytype == 'Forward' and mode == 'Strike':
                    t_und.price = originalTradePrice
                    t.price = originalTradePrice

                if t_und.insaddr.instype == 'Bond':
                    t_und.quantity = -t.quantity * cs / cs_und
                    conv_factor = 1.0
                    del_link = ael.DeliverableLink.read(
                            'owner_insaddr.insaddr = {0} and '
                            'member_insaddr.insaddr = {1}'.format(
                            ins.und_insaddr.insaddr, t_und.insaddr.insaddr))
                    if del_link:
                        conv_factor = del_link.conversion_factor
                    t_und.price = t_und.price * conv_factor
                    # p_und never committed ???
                    p_und = create_accrued_payment(t_und)
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
            if exercise_trade_hook:
                t_und = exercise_trade_hook(ins, t_und)
            t_und.premium = FBDPCommon.calculate_premium(t_und)
            self.add_exercise_trade(dependent, t_und, isSingleTradePosition)
            n += 1

        if exercise_trade_hook:
            t = exercise_trade_hook(ins, t.new())

        if ins.paytype in ['Future', 'Forward']:
            t.premium = 0.0
        else:
            t.premium = FBDPCommon.calculate_premium(t)

        self.add_exercise_trade(dependent, t, isSingleTradePosition)
        if create_payment == 1 and pay:
            Logme()('trade payment. {0}'.format(pay.pp()), 'DEBUG')
        Summary().ok(Summary().POSITION, summaryType)

        if n == 0:
            Logme()("No underlying trade done.", 'DEBUG')
        ael.poll()
        hook = additional_excercise_trades_hook
        if hook:
            add_trades = hook(t.new(), t_und and t_und.new(), price,
                    self.ael_variables_dict)
            if add_trades:
                msg = ('Adding {0} extra trades from '
                        '\'additional_excercise_trades\' hook.'.format(
                        len(add_trades)))
                Logme()(msg, 'DEBUG')
                self.beginTransaction()
                for trade in add_trades:
                    self.add_exercise_trade(dependent, trade,
                            isSingleTradePosition)
                try:
                    self.commitTransaction()
                except Exception, e:
                    self.abortTransaction()
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
        # get the exercise date
        if (exotic and isBarrier(ins) and (isKnockIn or isOneTouch or
                isKnockOut or isNoTouch) and
                exotic.barrier_cross_date and
                exotic.barrier_crossed_status == 'Confirmed'):
            date = exotic.barrier_cross_date
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
            isSingleTradePosition):
        if isSingleTradePosition:
            tradeNbr = 0
            try:
                tradeNbr = aelDependent.trdnbr
            except:
                self.add_trade(aelTradeToAdd)
                return
            acmTradeToExercise = acm.FTrade[tradeNbr]
            mirrorPortfolio = acmTradeToExercise.CounterPortfolio()
            if mirrorPortfolio:
                acmTradeToAdd = acm.FTrade[aelTradeToAdd.trdnbr]
                acmTradeToAdd.MirrorPortfolio(mirrorPortfolio)
                self.add_trade(acmTradeToAdd)
            else:
                self.add_trade(aelTradeToAdd)
        else:
            self.add_trade(aelTradeToAdd)


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
    return instr.InsType() == OPTION and instr.IsAsian()


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
    """
    trade.premium_from_quote(date, quote)
    """
    trade = acm.FTrade[trdnbr]
    ins = trade.Instrument()
    quote = ins.DenominatedValue(quote, date)
    return (-ins.QuoteToUnitValue(quote, acm.Time().DateNow(), True, None,
            None, ins.Quotation(), 0, 0).Number() * trade.Nominal())


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
            denom_val = denom_func(price, ins.und_insaddr.insid, None,
                    ael.date_today())
            if (convert_to_und_quotation == 1):
                to_quotation = und_instr.Quotation()
                from_quotation = instr.StrikeQuotation()
            else:
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


# ------------------------------------------------------------------
# Functions below called by FSetFinalExercisePrices
# ------------------------------------------------------------------


def get_trades(exer_date):
    """
    Select all trades with trade type set to
    Exercise, Assign or Closing where trade time equals the input date
    """
    exer_date = ael.date(str(exer_date))
    exer_trades = []
    all_trades = ael.Trade.select()
    for t in all_trades:
        if t.time > 0 and ael.date_from_time(t.time) == exer_date:
            if (t.type in ('Exercise', 'Assign') and
                    t.insaddr.instype in ('Option', 'Warrant')):
                pass
            elif (t.type == 'Closing' and
                    t.insaddr.instype == 'Future/Forward' and
                    t.insaddr.settlement == 'Cash'):
                pass
            else:
                continue
            exer_trades.append(t)
            msg = ('Will update trade {0} in {1}.'.format(t.trdnbr,
                    t.insaddr.insid))
            Logme()(msg)
    return exer_trades


def get_physical_trade(t_exer):
    """
    Find the physical delivery trade corresponding to the exercise trade
    """
    if not t_exer.insaddr.und_insaddr:
        return None
    ins = ael.Instrument.read('insaddr={0}'.format(t_exer.insaddr.insaddr))
    is_strike_quotation_different = 0
    if (ins.und_insaddr.quotation_seqnbr and ins.strike_quotation_seqnbr and
            ins.strike_quotation_seqnbr != ins.und_insaddr.quotation_seqnbr):
        is_strike_quotation_different = 1

    und = ael.Instrument.read('insaddr={0}'.format(
            t_exer.insaddr.und_insaddr.insaddr))
    pr_trades = ael.Trade.select('contract_trdnbr={0}'.format(
            t_exer.contract_trdnbr))
    for t in pr_trades:
        if t.insaddr.insaddr == und.insaddr:
            return t
        elif (is_strike_quotation_different and t.curr.insaddr == und.insaddr):
            return t


def update_exercise_payment(t_exer, settle, mode, TestMode):
    """
    Update the payment of type Exercise Cash or create it if it doesn't exist
    """
    found = 0
    excess_lots = t_exer.insaddr.contr_size - t_exer.insaddr.phys_contr_size

    if t_exer.insaddr.instype == 'Option':
        strike_price = convert_price_to_und_or_strike_quotation(t_exer.insaddr,
                t_exer.insaddr.strike_price, 1)
        if t_exer.insaddr.call_option == 1:
            trade_price = FBDPCommon.create_quotetype_price(t_exer.insaddr,
                          settle - strike_price)
        else:
            trade_price = FBDPCommon.create_quotetype_price(t_exer.insaddr,
                          strike_price - settle)
    else:
        trade_price = settle

    premium = trade_premium_from_quote(t_exer.trdnbr, trade_price,
            t_exer.acquire_day)
    new_amount = premium * excess_lots / t_exer.insaddr.contr_size
    payments = ael.Payment.select('trdnbr={0}'.format(t_exer.trdnbr))

    for p in payments:

        if (p.type == 'Exercise Cash' and mode == 'Strike'):
            found = 1
            payment_clone = p.clone()
            payment_clone.amount = new_amount
            if not TestMode:
                payment_clone.commit()

    t_exer_clone = t_exer.clone()
    payments_clone = t_exer_clone.payments()

    for p in payments_clone:
        if (p.type == 'Exercise Cash' and mode == 'Market'):
            found = 1
            p.delete()

    if not TestMode:
        t_exer_clone.commit()

    if not found and mode == 'Strike':
        t_exer_clone = t_exer.clone()
        new_payment = ael.Payment.new(t_exer_clone)
        new_payment.ptynbr = t_exer.counterparty_ptynbr
        new_payment.type = 'Exercise Cash'
        new_payment.amount = new_amount
        new_payment.curr = t_exer.insaddr.curr
        new_payment.payday = trade_spot_date(t_exer.trdnbr, ael.date_from_time(
                t_exer.time))
    if not TestMode:
        t_exer_clone.commit()


def set_final_settle_prices(pr_trades, exer_date, mode, TestMode):
    """------------------------------------------------------------------------
    FUNCTION
        set_final_settle_prices(pr_trades, exer_date, mode)

    DESCRIPTION
        Sets the final settlement price in all exercising derivatives trades,
        and potential corresponding physical delivery trades, done on the
        specified date.

        Cash settled instruments: Read the price on the SETTLEMENT market
        first. If there is no such price, read the settle price from the
        market on which the trade was done. Set the price of the closing
        derivative trade to the difference between the settle price and the
        strike and change the premium accordingly.

        Physical settled instruments: Either the physical trade is done to
        market, in which case the exercise trade should carry the difference
        between strike and the settlement price, or the physical trade is done
        to the strike in which case the exercise trade should get the price
        and premium zero.

    ARGUMENTS
        The function takes the following arguments:
        1) trades - The Exercise trades found in get_trades().
        2) exer_date - Only Exercised trades done on this date are handled,
           i.e. the trade time of the trade with type Exercise, Assign or
           Abandon should equal this date. The settlement prices should also
           have been entered on this date.
        3) mode - This could either be set to Strike or to Market. This
           depends on whether the physical delivery trade is done to the
           strike price or to market price.
    ------------------------------------------------------------------------"""

    if not pr_trades:
        msg = ('No Exercise/Assign trades made on date {0}'.format(exer_date))
        Logme()(msg, 'WARNING')
        return

    for t in pr_trades:
        ins = t.insaddr
        settle_price = getSettlePriceFromMarket(ins, exer_date, "SETTLEMENT")
        if not settle_price:
            msg = ('Will skip trade {0} since there is no price for this '
                     'instrument {1}.'.format(t.trdnbr, ins.insid))
            Logme()(msg)
            continue

        strike_price = convert_price_to_und_or_strike_quotation(ins,
                ins.strike_price, 1)

        if ins.settlement == 'Cash':
            if ins.call_option:
                p_der = FBDPCommon.create_quotetype_price(ins,
                        settle_price - strike_price)
            elif ins.instype == 'Future/Forward':
                p_der = settle_price
            else:
                p_der = FBDPCommon.create_quotetype_price(ins,
                        strike_price - settle_price)

        else:  # Physical settlement
            p_phys = 0.0  # price to be set in the physical trade
            t_phys = get_physical_trade(t)
            if not t_phys:
                Logme()('Physical settlement trade does not exist for trade '
                        '{0}.'.format(t.trdnbr))
                continue
            if mode == 'Market':
                p_phys = settle_price
                if ins.instype == 'Option':
                    p_phys = settle_price
                    if ins.call_option:
                        p_der = FBDPCommon.create_quotetype_price(ins,
                                settle_price - strike_price)
                    else:
                        p_der = FBDPCommon.create_quotetype_price(ins,
                                strike_price - settle_price)
                else:  # Future
                    p_der = settle_price

            else:  # Physical is done to the strike price (Strike mode)
                p_der = 0.0
                if ins.instype == 'Option':
                    p_phys = ins.strike_price
                else:  # Future
                    p_phys = settle_price

                if (abs(ins.phys_contr_size) > 0.000001 and
                        abs(ins.phys_contr_size - ins.contr_size) > 0.000001):
                    update_exercise_payment(t, settle_price, mode, TestMode)

                phys_clone = t_phys.clone()
                phys_clone.price = p_phys
                if (ins.instype in ['Option', 'Warrant'] and
                        ins.und_instype == 'Curr'):
                    phys_clone.fx_update_non_dealt_amount(p_phys)
                else:
                    phys_clone.premium = trade_premium_from_quote(
                            phys_clone.trdnbr, p_phys, phys_clone.acquire_day)
                if not TestMode:
                    phys_clone.commit()

        der_clone = t.clone()
        der_clone.price = p_der
        der_clone.premium = trade_premium_from_quote(der_clone.trdnbr, p_der,
                t.acquire_day)

        if not TestMode:
            der_clone.commit()
        ael.poll
