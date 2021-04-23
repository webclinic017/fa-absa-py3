""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FCATypes.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FCATypes - Module which executes different corporate action types.

----------------------------------------------------------------------------"""

import ast
from math import floor
from string import digits

import ael
import acm

import FBDPCommon
import FBDPInstrument
import ArenaFunctionBridge
import FExeAssPerform
import FScripDivPerform
import FBDPGui

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme

MAX_INS_NAME_LENGTH = FBDPCommon.getMaxNameLength(acm.FInstrument)
MAX_NAME_LENGTHS = {
    'insid': MAX_INS_NAME_LENGTH,
    'extern_id1': FBDPCommon.getMaxExternalId1Length(acm.FInstrument),
    'extern_id2': FBDPCommon.getMaxExternalId1Length(acm.FInstrument),
    'isin': FBDPCommon.getMaxIsinLength(acm.FInstrument)
}

try:
    import FBDPHook
    reload(FBDPHook)
except:
    pass


class SkipPosition(Exception):
    """
    Raising this Exception means to skip the current position and continue
    with the next one.
    """
    pass


class SkipCorpact(Exception):
    """
    Raising this Exception means to skip the current corporate action and
    continue with the next one.
    """
    pass


def getHook(name):
    link = None
    try:
        exec 'from FBDPHook import ' + name + ' as link'
    except ImportError:
        return False
    else:
        return link

def callHook(name, params):
    try:
        return getHook(name)(*params)
    except Exception as e:
        Logme()('Error %s occured in %s: %s' % (type(e), name, e), 'ERROR')
        raise SkipPosition

def _tradeNumber(trade):
    try:
        trdnbr = trade.trdnbr
    except:
        trdnbr = trade.Oid()
    return trdnbr


class CorpactType:
    """ Common base class to all corporate actions. """

    def derString(self):
        return ''

    def __init__(self, d, businessEvt):
        self.hookArguments = d
        self.__dict__.update(d)
        self.Preview = d['Preview'] if d.get('Preview') else 0
        self.Derivatives = d.get('Derivatives', [])
        self.businessEvt = businessEvt
        self.f = self.setup()
        self.newprice = 0
        ChangeTradePrice = self.ChangeTradePrice
        self.AdjustedCombinations = []
        ca_hook = 'corporate_action_selection'
        self.SelectedInstruments = FBDPCommon.selectionHook(
                    self.selectInstrument(), ca_hook, d)
        self.AdjustOutsideBarriers()

        for instrumentID in self.SelectedInstruments:
            instrument = ael.Instrument[instrumentID]
            self.i = instrument
            self.ChangeTradePrice = ChangeTradePrice
            #self.f = f
            try:
                self.processCorporateAction(instrument)
            except SkipPosition:
                continue
        self.update_comb_name()
        acm.PollDbEvents()

    def AdjustOutsideBarriers(self):
        pass

    def create_trade_links(self, newTradeList):
        Logme()('create_trade_links', 'INFO')
        for trade in newTradeList:
            if not trade:
                continue
            trdnbr = _tradeNumber(trade)
            tradeLink = acm.FBusinessEventTradeLink()
            tradeLink.Trade(trdnbr)
            tradeLink.BusinessEvent(self.businessEvt)
            self.rollback.add(tradeLink)
            Summary().ok(tradeLink, Summary().CREATE, tradeLink.Oid())

    def setup(self):
        Logme()('')
        Logme()('%s to be performed on%s: %s' % (self.tempName,
                self.derString(), self.Instr.insid))
        Logme()('Ex Date: %s' % self.ExDate)
        self.Method = self.Method.replace(' ', '')
        self.curr = self.Instr.curr  # Overridden by position curr.
        self.n = self.NewQuantity
        self.o = self.OldQuantity
        self.mtmp = self.find_mtm_price()
        return self.calculateFactor(self.o, self.n)

    def processCorporateAction(self, instrument):
        Logme()('', 'NOTIME')
        if self.checkParameters():
            raise SkipCorpact
        self.checkMethod()
        Logme()('processCorporateAction',
                    'INFO')
        if self.Method == 'Adjust':
            self.aggregate_check(instrument)
            self.adjustInstrument(instrument)
            self.adjustPrice(instrument)
            self.adjustDividends(instrument)
            self.adjustTradeHistory(instrument)
            self.adjustInitialIndexAndHistoricalResets()
        elif self.Method == 'Increase/DecreasePosition':
            self.aggregate_check(instrument)
            self.adjustInstrument(instrument)
            positionList = self.getPositions(instrument)
            self.adjustPositionOnly(positionList)
            self.adjustPrice(instrument)
            self.adjustDividends(instrument)
        elif self.Method == 'CloseDown':
            self.adjustInstrument(instrument)
            positionList = self.getPositions(instrument, self.Portfolio)
            self.closeTrades(positionList)
            self.adjustPrice(instrument)
            self.adjustDividends(instrument)
        elif self.Method == 'CloseAndOpen':
            positionList = self.getPositions(instrument, self.Portfolio)
            self.adjustInstrument(instrument)
            closingTrades = self.closeTrades(positionList)
            self.openTrades(closingTrades)
            self.adjustPrice(instrument)
            self.adjustDividends(instrument)
            self.adjustInitialIndexAndHistoricalResets()
        else:
            raise SkipCorpact

    def checkParameters(self):
        if (self.ChangeQuantity and self.ChangeContractSize and
                self.ChangeTradePrice):
            Logme()('You are trying to update contract size, trade price and '
                    'quantity. One of them has to be left unchanged.  Please '
                    'update the corporate action definition and try again!',
                    'ERROR')
            return True

        elif (self.ChangeContractSize and self.NewContractSizeFormula == 0 and
                self.OldContractSizeFormula == 0):
            Logme()('Trying to update contract size, but no approach for the '
                    'update is selected. ', 'ERROR')
            Logme()('Please select an approach in the change tab (of the '
                    'corporate action run gui) and try again.', 'ERROR')
            return True

        elif (self.ChangeContractSize and self.NewContractSizeFormula == 1 and
                self.OldContractSizeFormula == 1):
            Logme()('Trying to update contract size with two approaches, '
                    'only one at a time can be used.', 'ERROR')
            Logme()('Please select one approach in the change tab (of the '
                    'corporate action run gui) and try again.', 'ERROR')
            return True

        elif (self.ChangeQuantity and self.ChangeWeights and
                self.ChangeWeightsWithRfactor == 0 and
                self.ChangeWeightsWithStrikeDiff == 0):
            Logme()('Trying to change the weights, but no approach for the '
                    'update is selected. ', 'ERROR')
            Logme()('Please select how to change the weights in the change '
                    'tab (of the corporate action run gui) and try again.',
                    'ERROR')
            return True

        elif (self.ChangeQuantity and self.ChangeWeights and
                self.ChangeWeightsWithRfactor and
                self.ChangeWeightsWithStrikeDiff):
            Logme()('Trying to change the weights with two approaches, only '
                    'one at a time can be used.', 'ERROR')
            Logme()('Please select how to change the weights in the change '
                    'tab (of the corporate action run gui) and try again.',
                    'ERROR')
            return True
        else:
            return False

    def adjustInstrument(self, instrument):
        Logme()('CorpActType:AdjustInstrument', 'INFO')
        self.updateLinksAndWeights(instrument)

    def adjustInitialIndexAndHistoricalResets(self):
        Logme()('CorpActType:adjustInitialIndexAndHistoricalResets', 'INFO')

    def closeTrades(self, positionList):
        Logme()('closeTrades', 'INFO')
        closingTrades = []
        self.newprice = 0
        self.tradeInNewIns = None
        for positionTrade in positionList:
            closingTrade = self.closeOut(positionTrade)
            closingTrades.append(closingTrade)

        self.create_trade_links(closingTrades)
        return closingTrades

    def openTrades(self, closingTrades):
        Logme()('openTrades', 'INFO')
        openingTrades = []
        self.newprice = 0

        # Find MtM Market Price:
        for closingTrade in closingTrades:
            openingTrade = self.openTrade(closingTrade)
            openingTrades.append(openingTrade)
            # If rounding errors are found, add cash payment for the
            # difference:
            self.premiumDifference(closingTrade, openingTrade)

        self.create_trade_links(openingTrades)
        return openingTrades

    def adjustPositionOnly(self, positionList):
        # using: scalingFactor = new quantity / old quantity,
        # op = trade.quantity, np = op * scalingFactor,
        # q = np - op = (op * scalingFactor) - op = op * (scalingFactor - 1)
        Logme()('adjustPositionOnly', 'INFO')
        multiplier = ((1.0 * self.NewQuantity) / self.OldQuantity) - 1.0
        try:
            self.rollback.beginTransaction()
            tradeTime = self.ExDate.to_time() + 1
            for trade in positionList:
                adjustmentTrade = self.copyTrade(old=trade)
                adjustmentTrade.quantity = trade.quantity * multiplier
                adjustmentTrade.price = 0
                adjustmentTrade.premium = 0
                adjustmentTrade.value_day = self.SettleDate
                adjustmentTrade.acquire_day = adjustmentTrade.value_day
                adjustmentTrade.time = tradeTime
                if self.Preview:
                    adjustmentTrade.status = 'Simulated'

                try:
                    adjustmentTrade.type = 'Corporate Action'
                except TypeError:
                    pass

                self.rollback.add_trade(adjustmentTrade)

            self.rollback.commitTransaction()
        except Exception as e:
            self.rollback.abortTransaction()
            raise Exception(e)

        return

    def adjustPrice(self, instrument):
        if self.ChangeHistoricalPrices:
            Logme()('', 'NOTIME')
            Logme()('### ADJUSTING TRADE HISTORY, Historical Prices ### ('
                    'should only be used if using method Adjust) ', 'INFO')
            l = ('bid', 'ask', 'last', 'high', 'low', 'open', 'settle', 'diff')
            pr = instrument.historical_prices()
            for i in pr.members():
                if (self.StartDate <= i.day.add_days(1) <= self.ExDate and
                        not (i.ptynbr and
                                i.ptynbr.ptyid in self.ProtectedMarkets)):
                    p = i.clone()
                    for j in l:
                        price = getattr(p, j) * self.f
                        price = self.roundValue(price,
                                self.HistoricalPriceDecimals)
                        setattr(p, j, price)
                    if self.SavePriceChanges:
                        if self.rollback.add(p, list(l)):
                            Summary().ok(p, Summary().UPDATE)

    def adjustDividends(self, instrument):
        Logme()('adjustDividends', 'INFO')
        if self.ChangeDividends:
            div = ael.Dividend.select('insaddr = "%i"' %
                    instrument.insaddr).members()
            stream = ael.DividendStream.select('insaddr = "%i"' %
                    instrument.insaddr)
            if stream:
                Logme()('Dividend Streams to adjust:')
            for s in stream:
                div = div + ael.DividendEstimate.select(
                        'stream_seqnbr = "%i"' % s.seqnbr).members()
            if div:
                Logme()('Dividends to adjust:')
            for d in div:
                # Method is always Adjust
                if ((d.ex_div_day >= self.ExDate or self.Method == 'Adjust')
                        and (d.day > self.StartDate)):
                    originalDividendValue = d.dividend
                    dc = d.clone()
                    dc.dividend = self.roundValue(dc.dividend *
                            self.f, self.DividendDecimals)
                    if self.rollback.add(dc, ['dividend']):
                        Summary().ok(dc, Summary().UPDATE)
                        s = ('Old Div %f -> New Div %f' %
                                (originalDividendValue, dc.dividend))
                        Logme()(s)

    def closeOut(self, positionTrade):
        Logme()('closeOut', 'INFO')
        closingTrade = None
        try:
            self.rollback.beginTransaction()
            self.calculateNewPrice(positionTrade)
            closingTrade = self.createClosingTrade(
                        self.ExDate.to_time() + 1, positionTrade)
            #if not closeDown
            if (self.doWithNewInstrument() == \
               DoWithNewInstrument.Distribute and
                    not self.Method == 'CloseDown' or
                    self.Method == 'CloseDown' and
                    self.doWithNewInstrument() == DoWithNewInstrument.Open):
                # Distribute NewInstrument:
                if self.Method == 'CloseDown':
                    self.calculateOpen(positionTrade)
                #Convert to quotetype of new instrument
                self.newprice = FBDPCommon.create_price(positionTrade.insaddr,
                                                        self.newprice)
                openingIns = self.getOpeningInstrument(positionTrade)
                self.newprice = FBDPCommon.create_quotetype_price(openingIns,
                                    self.newprice)
                self.tradeInNewIns = self.createOpeningTrade(self.calculateNew,
                                    self.ExDate.to_time() + 1, closingTrade)
            self.rollback.commitTransaction()
            if self.tradeInNewIns:
                self.rollback.beginTransaction()
                newTradeClone = self.tradeInNewIns.clone()
                newTradeClone.contract_trdnbr = closingTrade.trdnbr
                self.rollback.add(newTradeClone, ['contract_trdnbr'])
                self.rollback.commitTransaction()
                self.create_trade_links([self.tradeInNewIns])

        except Exception as e:
            self.rollback.abortTransaction()
            raise Exception(e)
        return closingTrade

    def openTrade(self, positionTrade):
        Logme()('openTrade', 'INFO')
        openingTrade = None
        try:
            self.rollback.beginTransaction()
            self.calculateNewPrice(positionTrade)
            self.newprice = FBDPCommon.create_price(
                positionTrade.insaddr, self.newprice)
            openingTrade = self.createOpeningTrade(self.calculateOpen,
                        self.ExDate.to_time() + 3, positionTrade)
            self.rollback.commitTransaction()

        except Exception as e:
            self.rollback.abortTransaction()
            raise Exception(e)
        return openingTrade

    def premiumDifference(self, closingTrade, openingTrade):
        Logme()('premiumDifference', 'INFO')
        if closingTrade and openingTrade:
            diff = (closingTrade.premium + openingTrade.premium -
                    self.CashAmount)
            if self.tradeInNewIns:
                diff = diff + self.tradeInNewIns.premium
            if round(diff, 8) != 0.0:
                Logme()('')
                Logme()("Premiums and payments for this position don't sum "
                        "up to 0 due to rounding. The difference is: %f" %
                        diff)
                if self.RoundingCompensationCash:
                    Logme()("Creating cash payment to compensate for "
                            "rounding difference of %f" % diff)
                    self.createPayment(-diff, openingTrade)

    def getTradePrice(self, trade):
        if self.ClosingPrice == ClosingPrice.Zero:
            return 0.0
        if self.ClosingPrice == ClosingPrice.MarkToMarket:
            return self.mtmp
        if self.ClosingPrice == ClosingPrice.Average:
            if trade.price == float('nan'):
                return 0.0
            return trade.price

    def getCashAmount(self, closingTrade):
        cash = -self.CashAmount * closingTrade.quantity
        return cash

    def createOpeningTrade(self, calculate, tradeTime, closingTrade):
        Logme()('createOpeningTrade', 'INFO')
        openingTrade = self.copyTrade(closingTrade)
        openingTrade.quantity = -closingTrade.quantity
        openingTrade.price = self.getTradePrice(openingTrade)
        calculate(openingTrade)
        try:
            openingTrade.type = 'Corporate Action'
        except TypeError:
            pass

        openingTrade.value_day = self.SettleDate
        openingTrade.acquire_day = openingTrade.value_day
        openingTrade.time = tradeTime
        openingTrade.contract_trdnbr = closingTrade.trdnbr
        cash = self.getCashAmount(closingTrade)
        if self.ChangeTradePrice:
            self.adjustTradeForPayment(openingTrade, 0)

        self.createPayment(cash, openingTrade)
        self.getTradePremium(openingTrade, openingTrade.price)
        if self.Preview:
            openingTrade.status = 'Simulated'
        self.rollback.add_trade(openingTrade)
        return openingTrade

    def createClosingTrade(self, tradeTime, positionTrade=None):
        Logme()('createClosingTrade', 'INFO')
        closingTrade = self.copyTrade(positionTrade)
        closingTrade.quantity = -closingTrade.quantity
        closingTrade.price = self.getTradePrice(closingTrade)
        try:
            closingTrade.type = 'Corporate Action'
        except TypeError:
            pass

        closingTrade.value_day = self.SettleDate
        closingTrade.acquire_day = closingTrade.value_day
        closingTrade.time = tradeTime
        #self.adjustTradeForPayment(closingTrade)
        self.getTradePremium(closingTrade, closingTrade.price)

        if (self.Method == "CloseDown" and
                not self.doWithNewInstrument() == DoWithNewInstrument.Open):
            cash = self.CashAmount * -closingTrade.quantity
            self.createPayment(cash, closingTrade)

        if self.Preview:
            closingTrade.status = 'Simulated'
        self.rollback.add_trade(closingTrade)

        return closingTrade

    def getTradePremium(self, trade, tradePrice):
        try:
            trade.premium = FBDPCommon.trade_premium_from_quote(trade,
                    tradePrice, self.ExDate)
        except:
            Logme()('Failed to get the trade premium from ArenaFunctionBridge',
                    'ERROR')

    def adjustTradeForPayment(self, trade, cash):
        fx = 1.0
        if self.CashCurrency:
            fx = ArenaFunctionBridge.fx_rate(trade.curr.insid,
                    self.CashCurrency, None)
            if not fx:
                Logme()('There is no price for %s in %s on %s. Trade '
                        'currency will be used.' % (trade.curr.insid,
                        self.CashCurrency, self.ExDate), 'WARNING')
                fx = 1.0
        if trade.quantity:  # Check that q is not rounded to 0.
            price = (hasattr(self, 'unRoundedOpenPrice') and
                    self.unRoundedOpenPrice or trade.price)
            trade.price = self.roundValue(price -
                    FBDPCommon.create_quotetype_price(
                    trade.insaddr, cash) /
                    fx / trade.quantity, self.TradePriceDecimals)

    def createPayment(self, cash, trade):
        if cash:
            p = ael.Payment.new(trade)
            p.payday = trade.acquire_day
            p.amount = cash
            p.curr = trade.curr
            if self.CashCurrency:
                p.curr = ael.Instrument[self.CashCurrency]
            if not self.Testmode:
                p.commit()
            Summary().ok(p, Summary().CREATE)
            Logme()('Additional Payment: %f (%s)' % (p.amount, p.curr.insid),
                    'INFO')

    def getOpeningInstrument(self, positionTrade):
        Logme()('getOpeningInstrument', 'INFO')
        if not self.ins:
            return positionTrade.insaddr
        else:
            return self.ins

    def calculateOpen(self, trade):
        Logme()('calculateOpen', 'INFO')
        openingIns = self.getOpeningInstrument(trade)
        if self.doWithNewInstrument() == DoWithNewInstrument.Distribute:
            if self.ChangeTradePrice:
                qf = trade.quantity * self.n / self.o
                if self.InstrumentType == "Stock":
                    qf = self.roundValue(qf, self.QuantityDecimals, 0)

                if (openingIns.quote_type == 'Per Contract' and
                        self.ChangeContractSize):
                    trade.price = (trade.price -
                            self.newprice * trade.insaddr.contr_size)
                else:
                    trade.price = (trade.price -
                            self.newprice * trade.insaddr.contr_size * qf /
                            trade.quantity)
                    trade.price = self.roundValue(trade.price,
                                      self.TradePriceDecimals)
        else:
            trade.insaddr = openingIns
            if self.ChangeQuantity:
                if (self.ChangeStrike and openingIns.strike_price and
                        self.x.strike_price != 0):
                    f = self.x.strike_price / self.oldInstrument.strike_price
                elif self.ChangeContractSize:
                    f = self.x.contr_size / self.oldInstrument.contr_size
                else:
                    f = self.f
                trade.quantity = self.roundValue(trade.quantity / f,
                                                  self.QuantityDecimals,
                                                  openingIns.otc) or 1
            if self.ChangeTradePrice:
                if self.ChangeQuantity and trade.premium:
                    p = self.quote(trade)
                elif self.ChangeContractSize:
                    try:
                        p = (trade.price * self.oldInstrument.contr_size /
                                self.x.contr_size)
                    except:
                        Logme()('Not possible to adjust ContractSize for '
                                'instrument %s.'
                                % (openingIns.insid), 'WARNING')
                        Logme()('Check if the adjustment is correct '
                                'for this instrument type.', 'WARNING')
                        raise SkipCorpact
                else:
                    p = trade.price * self.f
                trade.price = self.roundValue(p, self.TradePriceDecimals)
                self.unRoundedOpenPrice = p
                if self.doWithNewInstrument() == DoWithNewInstrument.Open:
                    trade.price = self.newprice
                    self.unRoundedOpenPrice = self.newprice

    def calculateNew(self, trade):
        Logme()('calculateNew', 'INFO')
        newins = self.getOpeningInstrument(trade).clone()
        if self.ChangeContractSize:
            cs = newins.contr_size * self.n / self.o
            newins.contr_size = (self.roundValue(cs,
                    self.ContractSizeDecimals, newins.otc) or 1)

            if self.rollback.add(newins, ['contr_size']):
                Summary().ok(self.ins, Summary().UPDATE)
                Logme()('', 'DEBUG')
                Logme()('ContractSize adjusted to %f for instrument %s' %
                        (newins.contr_size, newins.insid), 'DEBUG')
        else:
            q = trade.quantity * self.n / self.o
            trade.quantity = (self.roundValue(q, self.QuantityDecimals,
                        newins.otc) or 1)

        trade.insaddr = newins
        trade.price = self.newprice

    def quote(self, trade):
        if trade.quantity:
            return FBDPCommon.create_quotetype_price(trade.insaddr,
                    abs(trade.premium / trade.quantity))
        else:
            return 0.0

    def roundValue(self, value, decimals, alwaysRound=1):
        decimals = int(decimals)
        if decimals == 0 and not alwaysRound:
            return int(round(value, 4))
        elif decimals == -1:
            return value
        else:
            return round(value, decimals)

    def doWithNewInstrument(self):
        import FCorporateAction
        if not self.ins:
            return None
        else:
            return (FCorporateAction.toDoList.index(
                self.WhatToDoWithNewInstrument) + 1)

    def adjustTradeHistory(self, instrument):
        Logme()('## Adjusting trades with method Adjust ##', 'INFO')
        trades = filter(self.trdfilter, instrument.trades())
        for trd in trades:
            trade = trd.clone()
            self.calculateNewPrice(trade)
            self.calculateOpen(trade)
            trade.premium = FBDPCommon.trade_premium_from_quote(trade,
                        trade.price, self.ExDate)
            if self.Preview:
                trade.status = 'Simulated'
            self.rollback.add_trade(trade, ['price', 'quantity',
                        'insaddr', 'premium', 'type'])

    def getPositions(self, instrument, portfolio=None, grouper=None):
        positionList = []
        positions = []
        if portfolio:
            portlist = []
            if isinstance(portfolio, (list, tuple)):
                portlist = portfolio
            else:
                portlist.append(portfolio)

            from FBDPCalculatePosition import CalculatePositionUsingGrouper as cp
            for port in portlist:
                portfolio = acm.FPhysicalPortfolio[port.prfnbr]
                inst = acm.FInstrument[instrument.insaddr]
                positions += cp(inst, portfolio, grouper, self.StartDate,
                    self.ExDate.add_banking_day(self.curr, -1),
                    hookArguments=self.hookArguments, usePlClearDate=1)
        else:
            from FBDPCalculatePosition import calculatePosition as cp
            positions = cp(instrument, self.StartDate,
                self.ExDate.add_banking_day(self.curr, -1),
                hookArguments=self.hookArguments)
        for pos in positions:
            calcTrades = pos[0]
            for trade in calcTrades:
                if trade.quantity:  # Filter away 0 positions.
                    positionList.append(trade)
        if positionList:
            self.curr = positionList[0].curr
        else:
            Logme()('%s has zero quantity, skipping' %
                        (instrument.insid))
        return positionList

    def find_mtm_price(self, ins=None):
        # Find correct price type (Closing Price types are defined in calss
        # ClosingPrice and can be Zero (value = 1), Average (value = 1) or
        # MarkToMarket (value = 2)
        if (not self.ClosingPrice == ClosingPrice.MarkToMarket and
                self.NewPrice < NewPrice.MarkToMarket):
            # Closing price type is MarkToMarket and NewPrice Tpye is Zero
            # CostFraction
            return 0

        if not self.ExDate:
            Logme()('ExDate not found. Please correct and rerun.', 'ERROR')
            raise SkipCorpact

        date = self.ExDate.add_banking_day(self.curr, -1)
        if not ins:
            ins = self.Instr
        return FBDPInstrument.find_price(ins, date, ins.curr)

    def copyTrade(self, old):
        new = ael.Trade.new(old.insaddr)
        return self.fieldsFromTemplate(old, new, exclude=('trdnbr',))

    def copyInstrument(self, old):
        new = ael.Instrument.new(old.instype)
        return self.fieldsFromTemplate(old, new, exclude=('insaddr',))

    def fieldsFromTemplate(self, old, new, exclude=()):
        for c in old.columns():
            if c not in exclude:
                try:
                    setattr(new, c, getattr(old, c))
                except AttributeError:
                    Logme()(c, "ERROR")
        return new

    def trdfilter(self, t):
        isBefore = self.StartDate <= ael.date_from_time(t.time) < self.ExDate
        noConnectedTrd = (t.connected_trdnbr.trdnbr == t.trdnbr)
        return isBefore and noConnectedTrd

    def aggregate_check(self, instrument):
        """--------------------------------------------------------------------
        FUNCTION
            aggregate_check(ca)
        DESCRIPTION
            Function which checks if this is an aggregate trade.
            This function makes sure that there is no aggregate trade visible
            in the instrument for which the Corporate Action is to be
            performed. Aggregate trades are not visible from an ATLAS client
            logged on in archived mode.  This function is only called by the
            adjust out method.

        ARGUMENTS
            ca      Entity      Corporate Action record
        --------------------------------------------------------------------"""
        AggError = ('\nThere is an aggregate trade in the instrument on '
                'which the Corporate Action is to be performed.\nCalculations '
                'will be incorrect if trades are later dearchived or '
                'reaggregated.\nPlease open PRIME in archived mode or use '
                'the close out method.\n\nWill skip this Corporate Action.')
        for trade in instrument.trades():
            if trade.aggregate:
                Logme()(AggError, 'ERROR')
                raise SkipCorpact

    def checkMethod(self):
        if not self.Method:
            Logme()('The corporate action must '
                    'have a method (CloseAndOpen, CloseDown or Adjust).',
                    'WARNING')

    def selectInstrument(self):
        return FBDPCommon.convertEntityList(
                [acm.FInstrument[self.Instr.insaddr]], self.hookArguments)

    def calculateFactor(self, o, n):
        if (self.doWithNewInstrument() == DoWithNewInstrument.Distribute and
                self.ins):
            n = o + n * (self.ins.contr_size or 1.0)
        if n:
            f = round(o / n, 10)
            if f:
                return f
        if (self.Method == "CloseDown" and
                self.doWithNewInstrument() != DoWithNewInstrument.Open):
            return 0
        else:
            Logme()('A zero division occurred in factor calculation. Please '
                    'check OldQuantity and NewQuantity.', 'ERROR')
            raise SkipCorpact

    def calculateNewPrice(self, trade):
        if (self.doWithNewInstrument() == DoWithNewInstrument.Distribute or
                self.doWithNewInstrument() == DoWithNewInstrument.Open):
            if (self.ins and self.ins.instype == 'Option' and
                    self.NewPrice in (NewPrice.Diluted,
                            NewPrice.StockPriceMinusRightStrike)):
                n = self.n
                newprice = self.mtmp
                if self.NewPrice == NewPrice.Diluted and (self.o + n):
                    newprice = (self.o * self.mtmp +
                            n * self.ins.strike_price) / (self.o + n)
                self.newprice = max((newprice -
                        self.ins.strike_price) * n / self.o, 0.0)
            elif self.NewPrice == NewPrice.Zero:
                self.newprice = 0.0
            elif self.NewPrice == NewPrice.CostFraction:
                self.newprice = (trade.price * self.SpinoffCostFraction *
                        self.o / self.n)
            else:
                self.newprice = self.find_mtm_price(self.ins)
            self.newprice = self.roundValue(self.newprice,
                    self.TradePriceDecimals)

    def truncateName(self, s):
        s = s[:MAX_INS_NAME_LENGTH]
        Logme()('Insid: %s => %s' % (self.x.insid, s))
        self.x.insid = s

    def update_comb_name(self):

        if self.ChangeName and self.AdjustedCombinations:
            Logme()("", "NOTIME")
            Logme()("Updating Combination Names:", "INFO")
            for insaddr in self.AdjustedCombinations:
                if getHook('update_name_hook'):
                    self.x = ael.Instrument[insaddr]
                    s = callHook('update_name_hook', [self])
                    if s:
                        Logme()("Updating name of %s %s." % (self.x.instype,
                                self.x.insid))
                        self.x = self.x.clone()
                        self.x.insid = s[:MAX_INS_NAME_LENGTH]
                        if self.rollback.add(self.x, ['insid']):
                            Summary().ok(self.x, Summary(). RENAME)

    def updateLinksAndWeights(self, old, new=None):
        """
        Update the instrument and weight fields of the combination links
        associated with the old instrument.
            'old' - The old instrument in ael.
            'new' - The new instrument in ael.
        """

        # Adjust derivatives' underlying instrument.
        if new:
            drvs = [d.Oid() for d in acm.FInstrument[old.insaddr].Derivatives()
                            if d.Oid() not in self.SelectedInstruments]
            for insaddr in drvs:
                d = ael.Instrument[insaddr].clone()
                d.und_insaddr = new.insaddr
                if self.rollback.add(d, ['und_insaddr']):
                    Summary().ok(d, Summary().UPDATE)
                    Logme()("Updating underlying of %s %s from %s to %s." %
                          (d.instype, d.insid, old.insid, new.insid))

        # Adjust links and weights in Equity Indices and Combinations
        protected_combs = [c.Oid() for c in (self.ProtectedComb or [])]
        cm = [c for c in acm.FInstrument[old.insaddr].CombinationMaps()]
        for c in cm:
            # Find the combination link linking between the owner (combination)
            # instrument and the member (combined) instrument.
            w = ael.CombinationLink[c.Oid()]
            # Double check the combination link's member instrument is the old
            # instrument.
            if w.member_insaddr.insaddr != old.insaddr:
                continue
            needAdjustWeight = (self.ChangeWeights and
                    w.owner_insaddr.insaddr not in protected_combs)
            # Clone the combination link.
            ww = w.clone()
            updated_attribs = []
            # Explicitly remember the old weight, because w.weight may be
            # overwritten by the clone.
            oldWeight = w.weight

            # UPDATE INSTRUMENT: Update the cloned combination link's member
            # instrument if the new instrument is provided.
            if new:
                # Assign the new instrument.
                ww.member_insaddr = new.insaddr
                # Register the updated attribute.
                updated_attribs.append('member_insaddr')
            # UPDATE WEIGHT: Update the new combination link's weight if
            # weight adjustment is needed.
            if needAdjustWeight:
                if new:
                    # Calculate the strike factor.
                    if old.strike_price == 0:
                        strikeFactor = self.f
                    else:
                        strikeFactor = new.strike_price / old.strike_price
                    # Assign the new weight.
                    if strikeFactor == 0 or self.ChangeWeightsWithRfactor == 1:
                        Logme()('Weight adjusted with the adjustment factor',
                              'INFO')
                        ww.weight = self.roundValue(w.weight / self.f,
                                                    self.WeightDecimals)
                    else:
                        Logme()('Weight adjusted with strike factor %s ' %
                              (strikeFactor), 'INFO')
                        ww.weight = self.roundValue(w.weight / strikeFactor,
                                                    self.WeightDecimals)
                    # Register updated attribute.
                    updated_attribs.append('weight')
                else:
                    # Assign new weight
                    ww.weight = self.roundValue(w.weight / self.f,
                                            self.WeightDecimals)
                    # Register updated attribute
                    updated_attribs.append('weight')
            # If either instrument or weight attribute is updated on the
            # cloned combination link.  Send the cloned combination link along
            # with the updated attributes to the rollback code for recording.
            if updated_attribs and self.rollback.add(ww, updated_attribs):
                Summary().ok(ww, Summary().UPDATE)
                if new:
                    Logme()("Updating member of %s %s from %s to %s." %
                          (w.owner_insaddr.instype, w.owner_insaddr.insid,
                           old.insid, new.insid))
                if needAdjustWeight:
                    Logme()("Updating weight of %s in %s %s from %s to %s." %
                          (ww.member_insaddr.insid, w.owner_insaddr.instype,
                           w.owner_insaddr.insid, oldWeight, ww.weight))
                if not self.AdjustedCombinations.count(
                        w.owner_insaddr.insaddr):
                    self.AdjustedCombinations.append(w.owner_insaddr.insaddr)


class Derivative(CorpactType):
    """ InstrumentType == 'Option'. """

    def __init__(self, *args, **kwargs):

        CorpactType.__init__(self, *args, **kwargs)
        self._derivativeTypesUpper = []

    def doWithNewInstrument(self):
        return DoWithNewInstrument.NewUnderlying

    def adjustDividends(self, instrument):
        pass

    def quote(self, trade):
        value = CorpactType.quote(self, trade)
        return value / self.x.contr_size

    def getOpeningInstrument(self, positionTrade):
        return self.x

    def derString(self):
        return ' derivatives on '

    def AdjustOutsideBarriers(self):
        outsideBarriers = ael.Exotic.select('outside_barrier_insaddr="%i"' %
                self.Instr.insaddr)
        if outsideBarriers:
            Logme()('', 'NOTIME')
            Logme()('Outside Barriers on %s exists and the barrier properties '
                    'will be adjusted.' %
                    (outsideBarriers[0].outside_barrier_insaddr.insid))
            Logme()('-------- Begin adjusting Outside Barriers --------',
                    'DEBUG')
            rFactor = self.f
            Logme()('Adjustment factor: %s' % (rFactor), 'DEBUG')

            for outsideBarr in outsideBarriers:
                rollbackAttribs = []
                exoticRollbackAttribs = []
                derivWithOutsideBarr = outsideBarr.insaddr
                cloneDeriv = derivWithOutsideBarr.clone()
                Logme()('Outside Barrier: %s' % (derivWithOutsideBarr.insid),
                        'DEBUG')

                #Barrier. Should have a common method with adjustExotic()
                if cloneDeriv.exotic().barrier_option_type != 'None':
                    if self.ChangeBarriers:
                        Logme()('Barrier: %s ' % (cloneDeriv.barrier), 'DEBUG')
                        newBarrier = cloneDeriv.barrier * rFactor
                        cloneDeriv.barrier = newBarrier
                        Logme()('NewBarrier: %s' % (cloneDeriv.barrier),
                                'DEBUG')
                        rollbackAttribs.append('barrier')

                    if cloneDeriv.exotic().double_barrier and \
                            self.ChangeBarriers:
                        Logme()('--------------------', 'DEBUG')
                        Logme()('DoubleBarrier: %s' %
                                (cloneDeriv.exotic().double_barrier), 'DEBUG')
                        newSecondBarrier = (
                                cloneDeriv.exotic().double_barrier * rFactor)
                        cloneDeriv.exotic().double_barrier = newSecondBarrier
                        Logme()('NewDoubleBarrier: %s' %
                                (cloneDeriv.exotic().double_barrier), 'DEBUG')
                        exoticRollbackAttribs.append('double_barrier')

                    if cloneDeriv.exotic().barrier_risk_management:
                        Logme()('--------------------', 'DEBUG')
                        Logme()('RiskManagment: %s' %
                                (cloneDeriv.exotic().barrier_risk_management),
                                'DEBUG')
                        newRiskManagment = (
                                cloneDeriv.exotic().barrier_risk_management *
                                rFactor)
                        cloneDeriv.exotic().barrier_risk_management = (
                                newRiskManagment)
                        Logme()('NewRiskManagment: %s' %
                                (cloneDeriv.exotic().barrier_risk_management),
                                'DEBUG')
                        exoticRollbackAttribs.append('barrier_risk_management')

                    if cloneDeriv.exotic().second_barrier_risk_mgmt:
                        Logme()('--------------------', 'DEBUG')
                        Logme()('SecondRiskManagment: %s' %
                                (cloneDeriv.exotic().second_barrier_risk_mgmt),
                                'DEBUG')
                        newRiskManagment = (
                                cloneDeriv.exotic().second_barrier_risk_mgmt *
                                rFactor)
                        cloneDeriv.exotic().second_barrier_risk_mgmt = (
                                newRiskManagment)
                        Logme()('NewSecondRiskManagment: %s' %
                                (cloneDeriv.exotic().second_barrier_risk_mgmt),
                                'DEBUG')
                        exoticRollbackAttribs.append(
                                'second_barrier_risk_mgmt')

                    if self.rollback.add(cloneDeriv, rollbackAttribs, 'Update',
                            [(cloneDeriv.exotic(), exoticRollbackAttribs)]):
                        Summary().ok(cloneDeriv, Summary().UPDATE)
                    else:
                        Logme()('%s was not send to the rollback' %
                                (cloneDeriv.insid), 'ERROR')

                Logme()('--------------------', 'DEBUG')
            Logme()('-------- End adjusting Outside Barriers --------',
                    'DEBUG')

    def adjustInstrument(self, instrument):
        Logme()('Derivative:AdjustInstrument', 'INFO')
        if self.checkParameters():
            raise SkipCorpact
        else:
            self.adjusted_attributes = []
            self.adjusted_children = []
            self.oldInstrument = instrument.clone()
            self.x = instrument.clone()
            self.adjustExotic()
            self.adjustStrike()
            self.adjustRenamed()
            self.change_cs = self.ChangeContractSize
            self.updateContractSize()  # Modifies self.f!
            Logme()('', 'NOTIME')
            self.changeUnderlying()
            self.adjustName()
            self.commitInstrument()
            self.updateLinksAndWeights(self.oldInstrument, self.x)
            self.adjustOldInstrument()

    def adjustExotic(self):
        if self.x.exotic_type == 'Other':
            rFactor = self.f
            exDate = self.ExDate
            rollbackAttribs = []
            exoticAttribs = []
            modifiedChildren = []
            Logme()('', 'NOTIME')
            Logme()('--- Derivative: %s ---' % (self.x.insid), 'INFO')
            Logme()('Adjusting Exotic properties ', 'INFO')
            Logme()('Adjustment factor: %s' % (rFactor), 'DEBUG')
            Logme()('-------- Begin adjusting Exotic --------', 'DEBUG')

            # Forward Start
            if (self.x.exotic().forward_start_type == 'Forward Start Perf' or
                    (self.x.exotic().forward_start_type == 'Forward Start' and
                     self.x.strike_type != 'Absolute')):

                if self.x.exotic().forward_start_type == 'Forward Start Perf':
                    # Check for Exotic Events ...
                    for asianEvent in self.x.exotic_events():
                        if (asianEvent.type == 'Price Fixing' and
                                asianEvent.value != -1 and
                                asianEvent.date <= exDate):
                            Logme()('--------------------', 'DEBUG')
                            Logme()('Initial Fixings for Forward Start '
                                    'Performance option will be adjusted, '
                                    'date %s' % (asianEvent.date), 'DEBUG')
                            Logme()('Old value: %s' % (asianEvent.value),
                                    'DEBUG')
                            newAsianValue = asianEvent.value * rFactor
                            asianEvent.value = newAsianValue
                            Logme()('New value: %s' % (asianEvent.value),
                                    'DEBUG')
                            Logme()('--------------------', 'DEBUG')
                            modifiedChildren.append((asianEvent, ['value']))

                Logme()('---------********************----------', 'INFO')
                Logme()('NOTE! %s: Will NOT be adjusted completely. ' %
                        (self.x.insid), 'INFO')
                Logme()('A new instrument is created, but NO trades are made!')
                Logme()('---------********************----------', 'INFO')

            # BARRIER, not including Outside Barriers
            elif self.x.exotic().barrier_option_type != 'None':
                if self.x.exotic().outside_barrier_insaddr == None:
                    if self.ChangeBarriers:
                        Logme()('Barrier: %s ' % (self.x.barrier), 'DEBUG')
                        newBarrier = self.x.barrier * rFactor
                        self.x.barrier = newBarrier
                        Logme()('NewBarrier: %s' % (self.x.barrier), 'DEBUG')
                        rollbackAttribs.append('barrier')

                    if self.x.exotic().double_barrier and self.ChangeBarriers:
                        Logme()('--------------------', 'DEBUG')
                        Logme()('DoubleBarrier: %s' %
                                (self.x.exotic().double_barrier), 'DEBUG')
                        newSecondBarrier = (self.x.exotic().double_barrier *
                                rFactor)
                        self.x.exotic().double_barrier = newSecondBarrier
                        Logme()('NewDoubleBarrier: %s' %
                                (self.x.exotic().double_barrier), 'DEBUG')
                        exoticAttribs.append('double_barrier')

                    if self.x.exotic().barrier_risk_management:
                        Logme()('--------------------', 'DEBUG')
                        Logme()('RiskManagment: %s' %
                                (self.x.exotic().barrier_risk_management),
                                'DEBUG')
                        newRiskManagment = (
                                self.x.exotic().barrier_risk_management *
                                rFactor)
                        self.x.exotic().barrier_risk_management = (
                                newRiskManagment)
                        Logme()('NewRiskManagment: %s' %
                                (self.x.exotic().barrier_risk_management),
                                'DEBUG')
                        exoticAttribs.append('barrier_risk_management')

                    if self.x.exotic().second_barrier_risk_mgmt:
                        Logme()('--------------------', 'DEBUG')
                        Logme()('SecondRiskManagment: %s' %
                                (self.x.exotic().second_barrier_risk_mgmt),
                                'DEBUG')
                        newRiskManagment = (
                                self.x.exotic().second_barrier_risk_mgmt *
                                rFactor)
                        self.x.exotic().second_barrier_risk_mgmt = (
                                newRiskManagment)
                        Logme()('NewSecondRiskManagment: %s' %
                                (self.x.exotic().second_barrier_risk_mgmt),
                                'DEBUG')
                        exoticAttribs.append('second_barrier_risk_mgmt')

                if self.x.rebate and self.ChangeRebate:
                    Logme()('--------------------', 'DEBUG')
                    Logme()('Rebate: %s' % (self.x.rebate), 'DEBUG')
                    newRebate = self.x.rebate * rFactor
                    self.x.rebate = newRebate
                    Logme()('NewRebate: %s' % (self.x.rebate), 'DEBUG')
                    rollbackAttribs.append('rebate')

            # ASIAN
            elif self.x.exotic().average_method_type != 'None':
                # Check for Exotic Events ...
                for asianEvent in self.x.exotic_events():
                    if asianEvent.type == 'Average price':
                        if (asianEvent.value != -1 and
                                asianEvent.date <= exDate):
                            Logme()('--------------------', 'DEBUG')
                            Logme()('Asian Average Price will be adjusted, '
                                    'date %s' % (asianEvent.date), 'DEBUG')
                            Logme()('Old value: %s' % (asianEvent.value),
                                    'DEBUG')
                            newAsianValue = asianEvent.value * rFactor
                            asianEvent.value = newAsianValue
                            Logme()('New value: %s' % (asianEvent.value),
                                    'DEBUG')
                            Logme()('--------------------', 'DEBUG')
                            modifiedChildren.append((asianEvent, ['value']))

                    if asianEvent.type == 'Average strike':
                        if (asianEvent.value != -1 and
                                asianEvent.date <= exDate):
                            Logme()('--------------------', 'DEBUG')
                            Logme()('Asian Average Strike will be adjusted, '
                                    'date %s' % (asianEvent.date), 'DEBUG')
                            Logme()('Old value: %s' % (asianEvent.value),
                                    'DEBUG')
                            newAsianValue = asianEvent.value * rFactor
                            asianEvent.value = newAsianValue
                            Logme()('New value: %s' % (asianEvent.value),
                                    'DEBUG')
                            Logme()('--------------------', 'DEBUG')
                            modifiedChildren.append((asianEvent, ['value']))

            # CLIQUET
            elif self.x.exotic().cliquet_option_type != 'None':
                for asianEvent in self.x.exotic_events():
                    if asianEvent.type == 'Cliquet date':
                        if (asianEvent.value != -1 and
                                asianEvent.date <= exDate):
                            Logme()('--------------------', 'DEBUG')
                            Logme()('Cliquet date will be adjusted, date %s' %
                                    (asianEvent.date), 'DEBUG')
                            Logme()('Old value: %s' % (asianEvent.value),
                                    'DEBUG')
                            newAsianValue = asianEvent.value * rFactor
                            asianEvent.value = newAsianValue
                            Logme()('New value: %s' % (asianEvent.value),
                                    'DEBUG')
                            Logme()('--------------------', 'DEBUG')
                            modifiedChildren.append((asianEvent, ['value']))

                if 'Rel' in self.x.strike_type:
                    Logme()('---------********************----------', 'INFO')
                    Logme()('NOTE! %s: Will NOT be adjusted completely. ' %
                            (self.x.insid), 'INFO')
                    Logme()('A new instrument is created, but NO trades are '
                            'made!')
                    Logme()('---------********************----------', 'INFO')

            # RANGE ACCRUAL
            elif self.x.exotic().range_accrual_amount != 0:
                Logme()('RangeAccrual Amount: %s ' %
                        (self.x.exotic().range_accrual_amount), 'DEBUG')
                newRangeAccrualAmount = (self.x.exotic().range_accrual_amount *
                        rFactor)
                self.x.exotic().range_accrual_amount = newRangeAccrualAmount
                Logme()('NewRangeAccrual Amount: %s' %
                        (self.x.exotic().range_accrual_amount), 'DEBUG')
                exoticAttribs.append('range_accrual_amount')

                if self.x.exotic().range_accrual_cap != 0:
                    Logme()('--------------------', 'DEBUG')
                    Logme()('RangeAccrual Cap: %s ' %
                            (self.x.exotic().range_accrual_cap), 'DEBUG')
                    newRangeAccrualCap = (self.x.exotic().range_accrual_cap *
                            rFactor)
                    self.x.exotic().range_accrual_cap = newRangeAccrualCap
                    Logme()('NewRangeAccrual Cap: %s' %
                            (self.x.exotic().range_accrual_cap), 'DEBUG')
                    exoticAttribs.append('range_accrual_cap')

                if self.x.exotic().range_accrual_floor != 0:
                    Logme()('--------------------', 'DEBUG')
                    Logme()('RangeAccrual Floor: %s ' %
                            (self.x.exotic().range_accrual_floor), 'DEBUG')
                    newRangeAccrualFloor = (
                            self.x.exotic().range_accrual_floor * rFactor)
                    self.x.exotic().range_accrual_floor = newRangeAccrualFloor
                    Logme()('NewRangeAccrual Floor: %s' %
                            (self.x.exotic().range_accrual_floor), 'DEBUG')
                    exoticAttribs.append('range_accrual_floor')

                for asianEvent in self.x.exotic_events():
                    if asianEvent.type == 'Price Fixing':
                        if (asianEvent.value != -1 and
                                asianEvent.date <= exDate):
                            Logme()('--------------------', 'DEBUG')
                            Logme()('Range Accrual price fixing will be '
                                    'adjusted, date %s' % (asianEvent.date),
                                    'DEBUG')
                            Logme()('Old value: %s' % (asianEvent.value),
                                    'DEBUG')
                            newAsianValue = asianEvent.value * rFactor
                            asianEvent.value = newAsianValue
                            Logme()('New value: %s' % (asianEvent.value),
                                    'DEBUG')
                            Logme()('--------------------', 'DEBUG')
                            modifiedChildren.append((asianEvent, ['value']))

            # CHOOSER
            elif self.x.exotic().chooser_date != None:
                Logme()('Adjusting Chooser with date: %s ' %
                        (self.x.exotic().chooser_date), 'DEBUG')

                if self.x.exotic().chooser_call_strike > 0:
                    Logme()('--------------------', 'DEBUG')
                    Logme()('Call Strike: %s ' %
                            (self.x.exotic().chooser_call_strike), 'DEBUG')
                    newCallStrike = (self.x.exotic().chooser_call_strike *
                            rFactor)
                    self.x.exotic().chooser_call_strike = newCallStrike
                    Logme()('New Call Strike: %s' %
                            (self.x.exotic().chooser_call_strike), 'DEBUG')
                    exoticAttribs.append('chooser_call_strike')

                if self.x.exotic().chooser_put_strike > 0:
                    Logme()('--------------------', 'DEBUG')
                    Logme()('Put Strike: %s ' %
                            (self.x.exotic().chooser_put_strike), 'DEBUG')
                    newPutStrike = (self.x.exotic().chooser_put_strike *
                            rFactor)
                    self.x.exotic().chooser_put_strike = newPutStrike
                    Logme()('New Put Strike: %s' %
                            (self.x.exotic().chooser_put_strike), 'DEBUG')
                    exoticAttribs.append('chooser_put_strike')

            # LOOKBACK
            elif self.x.exotic().lookback_option_type != 'None':
                Logme()('Adjusting Lookback Option', 'DEBUG')

                if self.x.exotic().lookback_extreme_value > 0:
                    Logme()('Extreme Value: %s' %
                            (self.x.exotic().lookback_extreme_value), 'DEBUG')
                    newExtremValue = (self.x.exotic().lookback_extreme_value *
                            rFactor)
                    self.x.exotic().lookback_extreme_value = newExtremValue
                    Logme()('NewExtreme Value: %s' %
                            (self.x.exotic().lookback_extreme_value), 'DEBUG')
                    exoticAttribs.append('lookback_extreme_value')

            # LADDER
            elif self.x.exotic_events():
                for asianEvent in self.x.exotic_events():
                    if asianEvent.type == 'Ladder rung':
                        Logme()('--------------------', 'DEBUG')
                        Logme()('Ladder rung: %s' % (asianEvent.value),
                                'DEBUG')
                        newAsianValue = asianEvent.value * rFactor
                        asianEvent.value = newAsianValue
                        Logme()('New Ladder rung: %s' % (asianEvent.value),
                                'DEBUG')
                        modifiedChildren.append((asianEvent, ['value']))

            # RAINBOW & POWER
            else:
                if (self.x.digital or
                        self.x.exotic().rainbow_option_type != 'None' or
                        (self.x.exotic().power_exponent > 0 and
                        self.x.exotic().power_gearing > 0)):
                    Logme()('---------********************----------', 'INFO')
                    Logme()('NOTE! %s: May NOT be adjusted completely.' %
                            (self.x.insid), 'INFO')
                    Logme()('Rainbow and Power options are not fully '
                            'supported.')
                    Logme()('---------********************----------', 'INFO')
                else:
                    Logme()('Exotic type not supported!', 'INFO')

            Logme()('-------- End adjusting Exotic --------', 'DEBUG')
            Logme()('', 'NOTIME')

            if self.Method == 'Adjust':
                if exoticAttribs:
                    modifiedChildren.append((self.x.exotic(), exoticAttribs))

                self.adjusted_attributes = rollbackAttribs
                self.adjusted_children = modifiedChildren
        # DIGITAL
        elif self.x.digital:
            Logme()('---------********************----------', 'INFO')
            Logme()('NOTE! %s: May NOT be adjusted completely.' %
                    (self.x.insid), 'INFO')
            Logme()('Digital options are not fully supported.')
            Logme()('---------********************----------', 'INFO')

        else:
            Logme()('Not an Exotic Option', 'DEBUG')

    def selectInstrument(self):
        """ Adjust derivatives (same procedure for all corpact-types) """
        Logme()('', 'NOTIME')
        Logme()("Derivatives to adjust:", 'DEBUG')
        if self.Derivatives:
            ins = [deriv for deriv in self.Derivatives]
            self._derivativeTypesUpper = [d.InsType().upper()
                        for d in self.Derivatives]
        else:
            ins = acm.FInstrument[self.Instr.insaddr].Derivatives()
            self._initDerivativeTypesUpper()
        ins = [i for i in ins if self.isAdjusted(i)]
        if 'TOTAL RETURN SWAPS' in self._derivativeTypesUpper:
            Logme()("Closing and re-opening total return swaps.", 'INFO')
            TrsInsts = acm.FTotalReturnSwap.Select('')
            TRSLeg0Stock = [TRS for TRS in TrsInsts if (len(TRS.Legs()) == 2)
            and TRS.Legs()[0].LegType() == 'Total Return' \
            and TRS.Legs()[0].IndexRef() \
            and (TRS.Legs()[0].IndexRef().Class() == acm.FClass['FStock']) \
            and acm.FInstrument[self.Instr.insaddr]
                                              == TRS.Legs()[0].IndexRef() \
            and TRS.Legs()[0].NominalScaling() in ['Price', 'Initial Price']]
            ins = ins + TRSLeg0Stock

            TRSLeg1Stock = [TRS for TRS in TrsInsts if (len(TRS.Legs()) == 2)
            and TRS.Legs()[1].LegType() == 'Total Return' \
            and TRS.Legs()[1].IndexRef() \
            and (TRS.Legs()[1].IndexRef().Class() == acm.FClass['FStock']) \
            and acm.FInstrument[self.Instr.insaddr]
                                              == TRS.Legs()[1].IndexRef() \
            and TRS.Legs()[1].NominalScaling() in ['Price', 'Initial Price']]
            ins = ins + TRSLeg1Stock

        if not ins:
            Logme()("No Derivatives to adjust!", 'DEBUG')
            return ins

        return FBDPCommon.convertEntityList(ins, self.hookArguments)

    def _initDerivativeTypesUpper(self):
        # If self.DerivativeTypes is in string representation, unwrap it and
        # make sure it is in an list or tuple.
        try:
            derTypes = self.DerivativeTypes
            if not derTypes:
                derTypes = []
            elif isinstance(derTypes, str):
                derTypes = derTypes.strip()
                if derTypes[0] in ('[', '('):
                    derTypes = ast.literal_eval(derTypes)
                else:
                    derTypes = derTypes.split(',')
        except:
            derTypes = []
        # Make DerivateTypesUpper
        assert hasattr(derTypes, '__iter__'), ('The \'DerivativeTypes\' '
                'is not an iterable')
        self._derivativeTypesUpper = [typ.upper() for typ in derTypes]

    def isAdjusted(self, der):
        derivative = ael.Instrument[der.Oid()]
        if (str(der.Category()).upper() in self._derivativeTypesUpper):
            if (derivative.exp_day >= self.ExDate or
                    der.Category() == 'DepositaryReceipt'):
                if self.AdjustOTC == 'Only OTC' and derivative.otc == 0:
                    Logme()(('%s is not adjusted, non OTC derivative.' %
                             derivative.insid), 'INFO')
                    return False
                elif self.AdjustOTC == 'Only non OTC' and derivative.otc == 1:
                    Logme()(('%s is not adjusted, OTC derivative.' %
                             derivative.insid), 'INFO')
                    return False
                elif (self.newNamesForOldDerivative(derivative)['insid'] ==
                        derivative.insid):
                    Logme()(('%s is an old derivative and will not be '
                             'adjusted.' % derivative.insid), 'INFO')
                    return False
                elif self.isOldOption(derivative):
                    if self.AliasType:
                        for a in derivative.aliases():
                            if a.type.alias_type_name == self.AliasType:
                                Logme()(derivative.insid, 'DEBUG')
                                return True
                    else:
                        Logme()(derivative.insid, 'DEBUG')
                        return True
            else:
                Logme()(('%s expires before ExDate and will not be adjusted.' %
                        derivative.insid), 'INFO')
        return False

    def isOldOption(self, x):
        if x.instype == 'Option' and not x.otc:
            if self.Method == 'Adjust':
                ut = x.updat_time
                s = 'Update'
            else:
                ut = x.creat_time
                s = 'Create'
            if ut < self.ExDate.to_time() - 60 * 60 * 8:
                return True
            else:
                s = ('%s excluded! Reason: Instrument %s time is after 16h00 '
                        'day before Ex Date.' % (x.insid, s))
                Logme()(s, 'DEBUG')
                return False
        else:
            return True

    def adjustStrike(self):
        # Change Strike:
        if not 'Rel' in self.x.strike_type and self.ChangeStrike:
            self.x.strike_price = self.x.strike_price * self.f
            self.x.strike_price = self.roundValue(self.x.strike_price,
                    self.StrikeDecimals)
            Logme()('%s Strike: %s => %s' % (self.x.insid,
                    self.oldInstrument.strike_price, self.x.strike_price))
            self.adjusted_attributes.append('strike_price')

        elif 'Rel' in self.x.strike_type:
            Logme()('%s Strike: Is not adjusted, due to Relative Strike' %
                    (self.x.insid), 'INFO')

    def update_name(self):
        """
        -----------------------------------------------------------------------
        FUNCTION
            update_name(self)

        DESCRIPTION
            Changes the insid of a derivative.

            This function tries to figure out a new instrument id of a
            derivative.  If there is no strike figure in the name, the new
            name will be 'old name + a modifier', where a modifier will be X,
            Y, Z or A. If there is a strike number in the name, the new name
            will be 'old name + new strike + modifier'. The strike is assumed
            to be at the end of the name, unless the series has been modified
            before, and unless there is one of the emmitents at OM in the name.
            Modifies x.insid. Also changes underlying part of the name.

        ARGUMENTS
            self        Class       An instance of a subclass to CorpactType.
            self.x      Entity      A record in the Instrument table.
            s           String      Insid, extern_id1, extern_id2 or ''.

        RETURNS
            None
        --------------------------------------------------------------------"""
        def real_round(number, dec):
            r = round(number, dec)
            if dec == 0 or r == int(r):
                return str(int(r))
            str_dec = str(r - floor(r))
            zeros = dec + 2 - len(str_dec)
            return str(r) + zeros * '0'
        if getHook('update_name_hook'):
            s = callHook('update_name_hook', [self])
            if s:
                self.truncateName(s)
                return
        s = self.x.insid

        if self.OldShortCode:
            s = self.x.insid.replace(self.OldShortCode, self.NewShortCode)
        elif self.ins and self.ShortCodeFieldName:
            fieldName = self.ShortCodeFieldName.lower()
            old_underlying = getattr(self.Instr, fieldName)
            new_underlying = getattr(self.ins, fieldName)
            error = None
            if old_underlying:
                if new_underlying:
                    s = self.x.insid.replace(old_underlying, new_underlying)
                else:
                    error = self.ins
            else:
                error = self.Instr

            if error:
                Logme()('ShortCodeFieldName is set to %s, but the '
                    'instrument %s has no %s.' % fieldName, error.insid,
                    fieldName, 'WARNING')
        new_mod = 'X'
        if s[-1] in 'XYZ':
            new_mod = 'XYZA'['XYZ'.index(s[-1]) + 1]
            s = s[:-1]  # Peel off the modifier.
        if s[-3:] in ('ABE', 'CBK', 'DSE', 'FSP', 'SHB', 'NDS', 'SEB',
                            'SGA', 'UBS'):
            emmitent = s[-3:]
            s = s[:-3]  # Peel off the emmitent.
        else:
            emmitent = ''
        # Find out how many figures there are at the end.
        j = -1
        while j >= -len(s) and s[j] in digits + '.':
            j = j - 1
        if self.ChangeStrike and j != -1:
            name_strike = real_round(self.x.strike_price,
                    self.InstrumentNameDecimals)
            s = s[0:(j + 1)] + name_strike + emmitent
        else:
            s = s + emmitent
        if self.AddModifier:
            s = s + new_mod
        self.truncateName(s)

    def renameOldDerivative(self):
        self.oldInstrument = self.delete_aliases(self.oldInstrument)
        if FBDPCommon.delete_obsolete_data(self.i, self.Testmode,
                exceptionList=['Trade', 'CorpAction', 'Confirmation',
                        'Settlement', 'CombinationLink']):
            self.oldInstrument = self.oldInstrument.clone()
            newNamesDic = self.newNamesForOldDerivative(self.oldInstrument)
            dicAttr = newNamesDic.keys()
            self.oldInstrument = self.renameOldInstrument(self.oldInstrument,
                    newNamesDic)
            if self.rollback.add(self.oldInstrument, dicAttr):
                Summary().ok(self.oldInstrument, Summary().RENAME)
            else:
                Summary().fail(self.oldInstrument, Summary().RENAME,
                        "Failed to rename Old Instrument",
                        self.oldInstrument.insaddr)
        else:
            Logme()('Error in delete_obsote_data')
            raise SkipPosition

    def delete_aliases(self, ins):
        for a in ins.children():
            if a.record_type == 'InstrumentAlias':
                FBDPCommon.Summary().ok(a, FBDPCommon.Summary().DELETE)
                if self.Testmode:
                    Logme()('Deleting alias, but in Testmode...', 'DEBUG')
                else:
                    a.delete()
        return ins

    def renameOldInstrument(self, oldInstrument, new_name_dic):
        if ('insid' in new_name_dic.keys()):
            Logme()('Old Instrument will be renamed to: %s' %
                    new_name_dic['insid'], 'INFO')
            oldInstrument.insid = new_name_dic['insid'][:MAX_INS_NAME_LENGTH]
            del new_name_dic['insid']

        for attr in new_name_dic.keys():
            s = 'oldInstrument.' + attr
            if eval(s):
                Logme()("%s : %s -> %s" % (attr, eval('oldInstrument.' + attr),
                        new_name_dic[attr]), 'DEBUG')
                if not len(str(new_name_dic[attr])) <= MAX_NAME_LENGTHS[attr]:
                    new_name_dic[attr] = ""
                exec s + ' = new_name_dic[attr]'
        return oldInstrument

    def newNamesForOldDerivative(self, instr):
        nameDic = {}
        attr = ['insid', 'extern_id1', 'extern_id2', 'isin']

        for a in attr:
            nameDic[a] = instr.insid + "_ca" + str(self.ExDate)

        if getHook('rename_old_derivative_hook'):
            s = callHook('rename_old_derivative_hook', [instr])

            # If rename_old_derivative_hook returns a string, the string is
            # inserted in a tuple.
            if type(s) == str:
                s = (s,)

            if s:
                for i in range(len(attr)):
                    try:
                        if s[i]:
                            nameDic[attr[i]] = s[i]
                        elif i:
                            del nameDic[attr[i]]
                    except IndexError:
                        copy = list(range(len(attr)))[i:]
                        if i == 2 and s[1]:
                            del copy[0]
                            for i in [1, 2]:
                                nameDic[attr[i]] = (eval("instr." + attr[i]) +
                                        s[1])
                        for c in copy:
                            nameDic[attr[c]] = nameDic['insid']
                        break
        return nameDic

    def adjustRenamed(self):
        #hook for updating the renamed instrument
        if getHook('update_renamed_instrument_hook'):
            self.x = self.unpackHook(callHook('update_renamed_instrument_hook',
                    [self.x, self]))

    def adjustOldInstrument(self):
        if self.Method == 'Adjust':
            return
        self.adjusted_attributes = []
        self.adjusted_children = []
        if getHook('update_old_instrument_hook'):
            oldIns = self.unpackHook(callHook('update_old_instrument_hook',
                    [self.oldInstrument, self]))
            if self.adjusted_attributes or self.adjusted_children:
                if self.rollback.add(oldIns, self.adjusted_attributes,
                        "Update",
                        modified_child_entities=self.adjusted_children):
                    Summary().ok(oldIns, Summary().CREATE)
                else:
                    Summary().fail(oldIns, Summary().CREATE,
                            "Failed to commit changes to old instrument.",
                            oldIns.insaddr)

    def unpackHook(self, returnedValue):
        ins = None
        attrib = []
        if type(returnedValue) == type(self.x):
            ins = returnedValue
        elif len(returnedValue) == 1:
            (ins) = returnedValue
        elif len(returnedValue) < 3:
            (ins, attrib) = returnedValue
        else:
            (ins, attrib, self.adjusted_children) = returnedValue
        self.adjusted_attributes.extend(attrib)
        return ins

    def adjustName(self):
        if self.ChangeName:
            # Change Instrument Name of Derivative:
            self.update_name()
            self.adjusted_attributes.append('insid')

            # Check if self.x already exists.
            y = ael.Instrument[self.x.insid]
            if self.Method == 'Adjust':
                if y and self.AddModifier:
                    self.case = 3
                    s = ('ERROR! Adjusted instrument already exists, please '
                            'use the Close Out method, or delete the '
                            'instruments if you want to use the Adjust '
                            'method. %s, %s' % (self.i.insid, self.x.insid))
                    Logme()(s, 'ERROR')
                    raise SkipCorpact
                else:
                    self.case = 6
            else:
                if y and self.AddModifier:
                    self.case = 4
                    self.x = y
                    self.change_cs = self.ins = False
                    Logme()('Found new instrument %s' % self.x.insid, 'DEBUG')
                elif self.NewOptions == 'Please create':
                    self.case = 5
                    n = self.x.new()
                    n = self.delete_aliases(n)
                    if not self.CopyIsin:
                        n.isin = ''
                    self.x = n
                else:
                    Logme()("New instrument %s doesn't exist. Skipping "
                            "position %s..." % (self.x.insid, self.i.insid),
                            'WARNING')
                    raise SkipPosition
                self.renameOldDerivative()
        else:
            self.case = 1
            if self.Method == 'CloseAndOpen':
                self.case = 2
                Logme()('If the instrument name is not to be changed, the '
                        'instrument will be adjusted (i.e. not created new). '
                        'Therefore the adjust trade method is more natural '
                        'than the close out method.')

    def changeUnderlying(self):
        if self.ins and self.x.und_insaddr == self.Instr:
            Logme()('Change underlying of %s: %s => %s' % (self.x.insid,
                self.Instr.insid, self.ins.insid))
            self.x.und_insaddr = self.ins
            self.adjusted_attributes.append('und_insaddr')

    def commitInstrument(self):
        if self.case == 5:
            if self.rollback.add(self.x):
                Logme()('Creating new instrument %s' % self.x.insid, 'DEBUG')
                Summary().ok(self.x, Summary().CREATE)
            else:
                Summary().fail(self.x, Summary().CREATE,
                        "Failed to create new instrument.", self.x.insaddr)
        elif self.case != 4:
            self.adjusted_attributes.extend(['extern_id1', 'extern_id2',
                    'isin'])
            if self.rollback.add(self.x, self.adjusted_attributes, 'Update',
                    modified_child_entities=self.adjusted_children):
                Summary().ok(self.x, Summary().CREATE)
            else:
                Summary().fail(self.x, Summary().CREATE,
                        "Failed to create new instrument.", self.x.insaddr)

    def updateContractSize(self):
        """--------------------------------------------------------------------
        METHOD
             updateContractSize()

        DESCRIPTION
            Changes the nominal amount of Eurex and OM derivatives according
            to specified rules.

            The nominal_amount is the quantity times the contract_size. This
            function adjusts derivative contract size or quantity.

            In the Eurex case, the contract size is always changed, since the
            trade quantity is not changed. If the strike is adjusted, the
            contract size is adjusted to:
            'old contr_size * old strike_price / new strike_price'.

            If the strike has not been adjusted, the contract size is changed
            to:
            'old contr_size * new   stock quantity / old stock quantity'.

            In the OM case, it is possible to choose to adjust the contract
            size or the trade quantity. Therefore, in order to make it
            impossible to change both trade quantity and contract size, a rule
            has been specified (in FCAExecute) which forces the trade quantity
            to change and keeps the contract size as it was, if nothing else
            has been specified.

        Current approach:
        new contract size = (old strike * old contract size) /
                (new strike, after rounding)
        (Rounding of contract size after four decimal places)

        Eurex Release 11.0 approach:
        new contract size = (old contract size) / (r-factor)
        (Rounding of contract size after four decimal places)
        --------------------------------------------------------------------"""

        if self.change_cs:
            if (self.OldContractSizeFormula and self.ChangeStrike and
                    self.x.strike_price):
                cs = ((self.x.contr_size * self.oldInstrument.strike_price) /
                        self.x.strike_price)
                Logme()('Adjusting Contract size with the strike factor',
                        'INFO')
            else:
                cs = self.x.contr_size / self.f
                Logme()('Adjusting Contract size with the adjustment factor',
                        'INFO')
            if self.ChangeQuantity:  # Contract size change.
                self.f = 1.0 / self.f

            self.x.contr_size = self.roundValue(cs, self.ContractSizeDecimals)
            self.x.phys_contr_size = floor(self.x.contr_size)
            self.adjusted_attributes.extend(['contr_size', 'phys_contr_size'])
            Logme()('%s Contract size: %s => %s' % (self.x.insid,
                    self.oldInstrument.contr_size, self.x.contr_size))
            if self.i.quote_type == 'Per Contract':
                self.ChangeTradePrice = False  # SPR 241511

class Repo(Derivative):

    def getPositions(self, instrument, portfolio=None, grouper=None):
        Logme()('getPositions', 'INFO')
        positionList = []
        inst = FBDPCommon.ael_to_acm(instrument)
        positions = inst.Trades()
        for pos in positions:
            if pos.Type() != 'Corporate Action':
                positionList.append(pos)
        return positionList

    def closeTrades(self, positionList):
        Logme()('closeTrades', 'INFO')
        closingTrades = []
        self.newprice = 0
        self.tradeInNewIns = None
        for positionTrade in positionList:
            closingTrade = self.closeOut(positionTrade)
            closingTrades.append(closingTrade)

        self.create_trade_links(closingTrades)
        return closingTrades

    def openTrades(self, closingTrades):
        Logme()('openTrades', 'INFO')
        openingTrades = []

        for closingTrade in closingTrades:
            openingTrade = self.openTrade(closingTrade)
            openingTrades.append(openingTrade)
            # If rounding errors are found, add cash payment for the
            # difference:
            self.premiumDifference(closingTrade, openingTrade)

        self.create_trade_links(openingTrades)
        return openingTrades

    def openTrade(self, positionTrade):
        Logme()('openTrade', 'INFO')
        openingTrade = None
        try:
            self.rollback.beginTransaction()
            openingTrade = self.createTrade(self.ExDate,
                positionTrade, 'Open', self.calculateOpen)
            self.rollback.commitTransaction()

        except Exception as e:
            self.rollback.abortTransaction()
            raise Exception(e)
        return openingTrade

    def closeOut(self, trade):
        Logme()('closeOut on Acm trade', 'INFO')
        closingTrade = None
        try:
            self.rollback.beginTransaction()
            closingTrade = self.createTrade(self.ExDate,
                trade, 'Close')
            self.rollback.commitTransaction()

        except Exception as e:
            self.rollback.abortTransaction()
            raise Exception(e)
        return closingTrade

    def createTrade(self, tradeTime, origTrade, closeOrOpen, calculate=None):
        Logme()('createTrade on acm trade', 'INFO')
        newTrade = acm.FTrade()
        newTrade.Apply(origTrade)
        newTrade.Quantity(-1 * origTrade.Quantity())
        if calculate:
            calculate(newTrade)
        try:
            newTrade.Type('Corporate Action')
        except TypeError:
            pass

        valueDay = self.SettleDate
        newTrade.ValueDay(valueDay)
        newTrade.AcquireDay(valueDay)
        newTrade.TradeTime(tradeTime)
        if self.Preview:
            newTrade.Status('Simulated')

        if closeOrOpen == 'Open':
            newTrade.ContractTrdnbr(origTrade.Oid())

        self.rollback.add_trade(newTrade)
        return newTrade

    def calculateOpen(self, trade):
        Logme()('calculate open on acm trade', 'INFO')
        openingIns = self.getOpeningInstrument(trade)
        if openingIns:
            acmIns = FBDPCommon.ael_to_acm(openingIns)
            trade.Instrument(acmIns)

        if self.ChangeQuantity:
            faceValue = self.roundValue(trade.FaceValue() / self.f,
                self.QuantityDecimals, trade.Instrument().Otc())
            trade.FaceValue(faceValue)

        if self.ChangeTradePrice:
            p = trade.Price() * self.f
            trade.Price(self.roundValue(p, self.TradePriceDecimals))

    def premiumDifference(self, closingTrade, openingTrade):
        Logme()('premiumDifference on acm', 'INFO')
        if closingTrade and openingTrade:
            diff = (closingTrade.Premium() + openingTrade.Premium() -
                    self.CashAmount)
            if self.tradeInNewIns:
                diff = diff + self.tradeInNewIns.Premium()
            if round(diff, 8) != 0.0:
                Logme()('')
                Logme()("Premiums and payments for this position don't sum "
                        "up to 0 due to rounding. The difference is: %f" %
                        diff)
                if self.RoundingCompensationCash:
                    Logme()("Creating cash payment to compensate for "
                            "rounding difference of %f" % diff)
                    self.createPayment(-diff, openingTrade)

    def createPayment(self, cash, trade):
        if cash:
            payment = acm.FPayment()
            payment.Type('Cash')
            payment.Currency(trade.Currency())
            if self.CashCurrency:
                payment.Currency(acm.FInstrument[self.CashCurrency])

            payment.Amount(cash)
            payment.PayDay(trade.AcquireDay())
            payment.Party(trade.Acquirer())
            payment.Trade(trade)

            if not self.Testmode:
                payment.Commit()
            Summary().ok('Payment', Summary().CREATE)
            Logme()('Additional Payment: %f (%s)' % (payment.Amount(),
                    payment.Currency().Oid()), 'INFO')


class SecurityLoan(Repo):

    def SetTradeQuantity(self, trade, quantity):
        Logme()('SecurityLoan SetTradeQuantity', 'INFO')
        decoratedTrade = acm.FBusinessLogicDecorator.WrapObject(trade)
        decoratedTrade.QuantityOfUnderlying(quantity)
        decoratedTrade.CollateralAmount(decoratedTrade.CollateralAmount())

    def calculateOpen(self, trade):
        Logme()('SecurityLoan calculateOpen', 'INFO')
        trade = FBDPCommon.ael_to_acm(trade)
        if self.ChangeQuantity:
            quantity = self.roundValue(trade.FaceValue() / self.f,
                self.QuantityDecimals, trade.Instrument().Otc())
            self.SetTradeQuantity(trade, quantity)

        if self.ChangeTradePrice:
            p = trade.Instrument().RefPrice() * self.f
            trade.Instrument().RefPrice(
                self.roundValue(p, self.TradePriceDecimals))


class TotalReturnSwap(Derivative):

    def checkMethod(self):
        if not self.Method and \
            self.Method not in ['Adjust', 'CloseAndOpen']:
            Logme()('The corporate action for TotalReturnSwap only '
                    'supports method (CloseAndOpen and Adjust).',
                    'WARNING')

    def adjustInitialIndexAndHistoricalResets(self):
        try:
            self.rollback.beginTransaction()
            legs = self.x.legs()
            strExDate = FBDPCommon.toDate(
                FBDPCommon.businessDaySpot(self.x, self.ExDate))
            for l in legs:
                index_ref = getattr(l, 'index_ref')
                if index_ref and index_ref.insaddr == self.Instr.insaddr:
                    self.adjustLegResetAttrs(strExDate, l)

            self.rollback.commitTransaction()
        except Exception as e:
            Logme()('Exception in adjustInitialIndexAndHistoricalResets.'
                % (e.Message()), 'ERROR')
            self.rollback.abortTransaction()

    def adjustLegResetAttrs(self, strExDate, leg):

        legClone = leg.clone()
        initialV = getattr(leg, 'initial_index_value')
        indexV = initialV * self.f
        setattr(legClone, 'initial_index_value', indexV)
        if self.rollback.add(legClone, ['initial_index_value']):
            Summary().ok(legClone, Summary().UPDATE)

        self.adjustHistoricalCflResets(strExDate, legClone)

    def adjustHistoricalCflResets(self, strExDate, aelLeg):
        cashflows = aelLeg.cash_flows()
        sortedCfls = {}
        for cfl in cashflows:
            sortedCfls[cfl.start_day.to_string("%Y-%m-%d")] = cfl

        for k in sorted(sortedCfls.keys()):
            cfl = sortedCfls[k]
            cflStartDay = cfl.start_day.to_string("%Y-%m-%d")
            cflEndDay = cfl.end_day.to_string("%Y-%m-%d")
            if (cflEndDay < strExDate) or \
               (cflStartDay <= strExDate and cflEndDay > strExDate):
                self.adjustFixedResets(cfl, strExDate)

    def adjustFixedResets(self, cfl, strExDate):
        resets = cfl.resets()
        cflStartDay = cfl.start_day.to_string("%Y-%m-%d")
        Logme()('** Ajusted historical fixed resets on Cfl with \
                start date %s. ***' % (cflStartDay), 'INFO')
        for r in resets:
            resetDay = r.day.to_string("%Y-%m-%d")
            if resetDay < strExDate and r.value:
                newValue = r.value * self.f
                Logme()('** Ajust historical fixed reset type %s, \
                    day %s, value %s to new value %s '\
                    % (r.type, resetDay, r.value, newValue), 'INFO')
                rClone = r.clone()
                setattr(rClone, 'value', newValue)
                if self.rollback.add(rClone, ['value']):
                    Summary().ok(rClone, Summary().UPDATE)

class BasketRepo(CorpactType):
    def checkMethod(self):
        if not self.Method and \
            self.Method not in ['Adjust']:
            Logme()('The corporate action for BasketRepoLoan only '
                    'supports method ( Adjust).',
                    'WARNING')

    def trdfilter(self, t):
        if t.category != 'Collateral':
            return False

        connectedTrd = t.connected_trdnbr
        if connectedTrd.insaddr.instype not in ['BasketRepo/Reverse']:
            return False

        return self.StartDate <= ael.date_from_time(t.time) < self.ExDate

class BasketSecurityLoan(CorpactType):
    def checkMethod(self):
        if not self.Method and \
            self.Method not in ['Adjust']:
            Logme()('The corporate action for BasketSecurityLoan only '
                    'supports method ( Adjust).',
                    'WARNING')

    def trdfilter(self, t):
        if t.category != 'Collateral':
            return False

        connectedTrd = t.connected_trdnbr
        if connectedTrd.insaddr.instype not in ['BasketSecurityLoan']:
            return False

        return self.StartDate <= ael.date_from_time(t.time) < self.ExDate

class TradeType:
    #Do not use value 0, as that should represent an inactive field.
    Closing = 1
    Opening = 2
    New = 3

class ClosingPrice:
    #Do not use value 0, as that should represent an inactive field.
    Zero = 1
    Average = 2
    MarkToMarket = 3

class NewPrice:
    #Do not use value 0, as that should represent an inactive field.
    Zero = 1
    CostFraction = 2  # Only for SpinOffStock
    MarkToMarket = 3
    StockPriceMinusRightStrike = 4  # Only for options.
    Diluted = 5  # Only for options.

class DoWithNewInstrument:
    #Do not use value 0, as that should represent an inactive field.
    Distribute = 1     # Distribute it.
    Open = 2           # Move position to it.
    NewUnderlying = 3  # Use it as underlying to adjusted derivative.

class CorpactExerciseAssign:
    """ Exercise Assign corporate actions. """

    def derString(self):
        return ''

    def __init__(self, d, rollback, businessEvt):
        self.rollback = rollback
        self.businessEvt = businessEvt
        newParam = self._ConvertParam(d)
        e = FExeAssPerform.Exercise(
            'Corporate Action',
            d['Testmode'],
            newParam)
        e.perform_exercise_assign(newParam)
        e.end()
        return

    def _ConvertParam(self, d):
        corpExerciseAssignMap = {
            'DoExerciseAssign': 'DoExeAss',
            'DoAbandon': 'DoAbandon',
            'CloseAll': 'close_all',
            'ExercisePct': 'partial_exercise',
            'SettlePrice': 'settle_price',
            'SettleMarket': 'settlemarket',
            'ExerciseMode': 'mode',
            'Instrument': 'instruments',
            'NewInstrument': 'CAInstrument',
            'Exdate': 'ExDate',
            'TradeFilter': 'TradeFilter',
            'Portfolio': 'TradingPortfolios',
            'Grouper': 'PortfolioGrouper',
            'Logmode': 'Logmode',
            'LogToConsole': 'LogToConsole',
            'LogToFile': 'LogToFile',
            'Logfile': 'Logfile',
            'SendReportByMail': 'SendReportByMail',
            'MailList': 'MailList',
            'ReportMessageType': 'ReportMessageType',
            'Testmode': 'Testmode',
            'Preview': 'Preview'}
        newParam = {}
        for key in corpExerciseAssignMap:
            newKey = corpExerciseAssignMap[key]
            if key in d:
                if key == 'Instrument' and type(d[key]) is str:
                    inst = acm.FInstrument[d[key]]
                    if inst:
                        newParam[newKey] = [inst]
                else:
                    newParam[newKey] = d[key]
            else:
                Logme()('Missing key %s in the param.' % (key), 'ERROR')

        newParam['Rollback'] = self.rollback
        newParam['BusinessEvt'] = self.businessEvt
        FBDPGui.setPortfolioGrouper(newParam)
        return newParam

class CorpactScripDividend:
    """ Scrip Dividend corporate actions. """

    def derString(self):
        return ''

    def __init__(self, d, rollback, businessEvt):
        self.rollback = rollback
        self.businessEvt = businessEvt
        newParam = self._ConvertParam(d)
        FScripDivPerform.perform(newParam)
        return

    def _ConvertParam(self, d):
        corpExerciseAssignMap = {
            'IssuePerShare': 'ScripIssuePerShare',
            'RoundingType': 'TradeQuantityRounding',
            'Corpact': 'CorporateAction',
            'Instrument': 'Instrument',
            'TradeFilter': 'TradeFilters',
            'Portfolio': 'Portfolios',
            'Logmode': 'Logmode',
            'LogToConsole': 'LogToConsole',
            'LogToFile': 'LogToFile',
            'Logfile': 'Logfile',
            'SendReportByMail': 'SendReportByMail',
            'MailList': 'MailList',
            'ReportMessageType': 'ReportMessageType',
            'Testmode': 'Testmode',
            'Preview': 'Preview'}
        newParam = {}
        for key in corpExerciseAssignMap:
            newKey = corpExerciseAssignMap[key]
            if key in d:
                if key == 'Instrument' and type(d[key]) is str:
                    inst = acm.FInstrument[d[key]]
                    if inst:
                        newParam[newKey] = [inst]
                else:
                    newParam[newKey] = d[key]
            else:
                Logme()('Missing key %s in the param.' % (key), 'ERROR')
        newParam['Rollback'] = self.rollback
        newParam['BusinessEvt'] = self.businessEvt
        newParam['ScriptName'] = 'Scrip Dividend'
        return newParam

class CorpactDividendReinvestment:
    """ Dividend reinvestment corporate actions. """

    def derString(self):
        return ''

    def __init__(self, d, rollback, businessEvt):
        self.rollback = rollback
        self.businessEvt = businessEvt
        newParam = self._ConvertParam(d)
        FScripDivPerform.perform(newParam)
        return

    def _ConvertParam(self, d):
        corpExerciseAssignMap = {
            'IssuePerShare': 'DripIssuePerShare',
            'Corpact': 'CorporateAction',
            'RoundingType': 'TradeQuantityRounding',
            'Logmode': 'Logmode',
            'LogToConsole': 'LogToConsole',
            'LogToFile': 'LogToFile',
            'Logfile': 'Logfile',
            'SendReportByMail': 'SendReportByMail',
            'MailList': 'MailList',
            'ReportMessageType': 'ReportMessageType',
            'Testmode': 'Testmode',
            'Preview': 'Preview'}
        newParam = {}
        for key in corpExerciseAssignMap:
            newKey = corpExerciseAssignMap[key]
            if key in d:
                if key == 'Corpact' and type(d[key]) is str:
                    inst = acm.FCorporateAction[d[key]]
                    if inst:
                        newParam[newKey] = [inst]
                else:
                    newParam[newKey] = d[key]
            else:
                Logme()('Missing key %s in the param.' % (key), 'ERROR')
        newParam['Rollback'] = self.rollback
        newParam['BusinessEvt'] = self.businessEvt
        newParam['ScriptName'] = 'Dividend Reinvestment'
        return newParam
