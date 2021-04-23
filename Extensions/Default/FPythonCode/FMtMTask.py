""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FMtMTask.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FMtMTask - Module containing the main functionality for MarktoMarket.

DESCRIPTION
    This module is a collection of utility functions and classes for the
    FMarkToMarket script.
----------------------------------------------------------------------------"""


import math
import re
import types


import ael
import acm


import FBDPWorld
import FBDPCommon
import FBDPYieldCurveLib
import FMtMCalcVal
import FMtMSelInsCurr
import FMtMUtil
import FFxCommon


PROTECTED_TYPES = ('Instrument Specific',)


def calibrateVolatility(vol,
        legacyOp=lambda volStruct: volStruct.Calibrate()):
    calcRtn = True
    errMsg = ''
    if FBDPCommon.useNewCalibrationFramework(
        'FMtMVariables') \
        and FBDPCommon.supportNewCalibrationFramework(vol):
        calcRtn, errMsg = \
            FBDPCommon.calibrateVolatility(vol)
    else:
        legacyOp(vol)
    return calcRtn, errMsg


class MtMTask(FBDPWorld.WorldInterface):
    """------------------------------------------------------------------------
    CLASS
        MtMTask()
    DESCRIPTION
        MtMTask is the abstract super class.
    HOOKS:
        InitHook: A method.
        CalcHook: A class method.
        PostAdjustHook: A class method.
        (USAGE needs to be decided)
    USAGE:
    NOTE:
        - The PostAdjustHook is called before CalculatedValue's are saved and
        not against Registered values!
    ------------------------------------------------------------------------"""

    calc_hook = None
    init_hook = None
    post_adjust_hook = None

    def __init__(self, world, mtmDate, mtmMarket):
        """
        CONSTRUCTOR ARGUMENT:
        mtmDate:  An ael date.
        market:    A party of type MtM Market.
        """
        assert (self.__class__ != MtMTask), 'MtMTask is an abstract class'
        assert isinstance(world, FBDPWorld.World), ('The given \'world\' must '
                'be an instance of FBDPWorld.')
        assert isinstance(mtmDate, (ael.ael_date, type(None))), ('The '
                'given \'mtmDate\' must be an instance of ael_date')
        assert ((hasattr(mtmMarket, 'IsKindOf') and
                mtmMarket.IsKindOf(acm.FMTMMarket)) or mtmMarket is None), (
                'The given \'market\' must be an instance of FMTMMarket or is '
                'None')
        FBDPWorld.WorldInterface.__init__(self, world)
        self.today = ael.date_today()
        self.mtmDate = mtmDate
        self.mtmMarket = mtmMarket

    def calculate(self):
        """
        Calculates all or one. Normally values are calculated once
        """
        raise NotImplementedError('MtMTask.calculate() should be implemented '
                'in the derived classes.')

    def save(self):
        """
        Saves all or one instrument
        """
        raise NotImplementedError('MtMTask.save() should be implemented '
                'in the derived classes.')

    @classmethod
    def setCalcHook(cls, h):
        """
        calc_hook(self,ins,day,....)
        Should have the same signature as the calculate function in the class.
        """
        cls.calc_hook = h

    @classmethod
    def setPostAdjustHook(cls, h):
        """
        post_adjust_hook(ins,value). Should also adjust spread
        """
        cls.post_adjust_hook = h


class MtMTaskPrice(MtMTask,
        FMtMUtil.PriceBatchTransactionControlHandlerInterface):
    """------------------------------------------------------------------------
    CLASS
        MtMTaskPrice --> MtMTask

    DESCRIPTION
        The MtM task that can calculate and save a mtm price.
    ------------------------------------------------------------------------"""

    def __init__(self, world, mtmDate, mtmMarket, insCurrPairList,
            calcPriceCache, exclude_zero=0, bid_and_ask=0,
            high_and_low=0, last=0,
            use_zero_prices=1, digits=4,
            override_price=0, useYesterday=0,
            sourceMtmMarket=None, backDated=0):
        """
        CONSTRUCTOR ARGUMENTS:
        exclude_zero: If prices for zero settlement price is excluded.
        bid_and_ask:  If bid and ask prices also should be created.
        high_and_low: If high and low prices should also be created.
        last_low:     If last prices should also be created.
        """
        assert mtmMarket is not None, ('This derived class required a mtm '
                'market.')
        MtMTask.__init__(self, world, mtmDate, mtmMarket)
        FMtMUtil.PriceBatchTransactionControlHandlerInterface.__init__(self,
                world, override_price)
        assert isinstance(insCurrPairList, list), ('The given '
                '\'insCurrPairList\' must be an instance of list.')
        for elem in insCurrPairList:
            assert isinstance(elem, FMtMSelInsCurr.InsCurrPair), ('The '
                    'elements in the \'insCurrPairList\' must be an instance '
                    'of FMtMSelInsCurr.InsCurrPair.')
        self.insCurrPairList = insCurrPairList
        self._calcPriceCache = calcPriceCache
        self.exclude_zero = exclude_zero
        self.bid_and_ask = bid_and_ask
        self.high_and_low = high_and_low
        self.last = last
        self.use_zero_prices = use_zero_prices
        self.useYesterday = useYesterday
        self.sourceMtmMarket = sourceMtmMarket
        self.backDated = backDated
        if digits != '':
            if (digits < 0) or (digits > 20):
                raise ValueError('The number of decimals places must be '
                        'between 0 and 20.')
        self.digits = digits
        self._dealSheetCalcSpaceMngr = FMtMCalcVal.DealSheetCalcSpaceManager(
                world)

    def _getCalcFromHook(self, ins, mtmDate, curr):
        if MtMTaskPrice.calc_hook:
            return MtMTaskPrice.calc_hook.im_func(ins, mtmDate, curr)
        return None

    def _calculate(self, ins, mtmDate, curr):
        """
        calculates a pure price without rounding
        """
        # mtmDate >= self.today
        result = self._getCalcFromHook(ael.Instrument[ins.Oid()],
            mtmDate, ael.Instrument[curr.Oid()])
        if result is not None:
            return result

        if (ins.InsType() == 'Curr' or ins.Currency().Name() != curr.Name() or
                ins.Name() == FMtMSelInsCurr.HIST_FUNDING_INS_NAME):
            try:
                useSpecificCurr = 0
                if ins.Name() == FMtMSelInsCurr.HIST_FUNDING_INS_NAME:
                    useSpecificCurr = 1
                priceValue = (self._dealSheetCalcSpaceMngr.
                        getInsCalcMarketPrice(ins,
                        self.mtmDate.to_string(ael.DATE_ISO), 0, curr,
                        useSpecificCurr))
                return priceValue.Number()
            except:
                if ins.InsType() == 'Curr':
                    msg = 'Could not get fx rate between {0} and {1}'.format(
                            ins.Name(), curr.Name())
                else:
                    msg = 'Could not get {0} rate for {1}'.format(
                            curr.Name(), ins.Name())
                self._logDebug(msg)
                return 0.0
        else:
            try:
                priceValue = (self._dealSheetCalcSpaceMngr.
                        getCalcSpaceCalculateValue(ins,
                        'Suggested Mark-to-Market Price'))
                return priceValue.Number()
            except:
                self._logDebug('Failed to get mtmPriceSuggest for instrument '
                        '{0}.'.format(ins.Name()))
                return 0.0

    def _getBidAskPrice(self, ins, currency):
        bid_price = 0.0
        ask_price = 0.0
        if self.bid_and_ask:
            bid_price = self._getMarketPrice(ins, self.mtmDate, currency,
                'AverageBidPrice')
            if not MtMTaskPrice._validPrice(bid_price):
                bid_price = 0.0
            ask_price = self._getMarketPrice(ins, self.mtmDate, currency,
                'AverageAskPrice')
            if not MtMTaskPrice._validPrice(ask_price):
                ask_price = 0.0
        return bid_price, ask_price

    def _calculateLegPrices(self, ins):
        """
        Function for instruments of type CurrSwap and FxSwap
        """
        strMtMIsoDate = self.mtmDate.to_string(ael.DATE_ISO)
        prices = []
        try:
            suggestValues = (self._dealSheetCalcSpaceMngr.
                    getCalcSpaceCalculateValue(ins,
                    'Suggested Mark-to-Market MultiCurrency Price'))
            try:
                twoCurrencies = len(suggestValues) == 2
            except:
                twoCurrencies = False
            if twoCurrencies:
                price1 = suggestValues[0].Number()
                price2 = suggestValues[1].Number()
                curr1 = suggestValues[0].Unit()
                curr2 = suggestValues[1].Unit()
                # If the currencies are not in the denominatedValue structs,
                # get them from the legs.
                if curr1:
                    curr1 = acm.FInstrument[str(curr1)]
                else:
                    curr1 = ins.Legs().At(0).Currency()
                if curr2:
                    curr2 = acm.FInstrument[str(curr2)]
                else:
                    curr2 = ins.Legs().At(1).Currency()

                bid_price, ask_price = self._getBidAskPrice(ins, curr1)
                calcPrice1 = FMtMCalcVal.CalculatedPrice(ins, curr1,
                        strMtMIsoDate, self.mtmMarket, bid_price,
                        ask_price, price1, 0.0, 0.0, 0.0)
                prices.append(calcPrice1)

                bid_price, ask_price = self._getBidAskPrice(ins, curr2)
                calcPrice2 = FMtMCalcVal.CalculatedPrice(ins, curr2,
                        strMtMIsoDate, self.mtmMarket, bid_price,
                        ask_price, price2, 0.0, 0.0, 0.0)
                prices.append(calcPrice2)

            else:
                curr = ins.Currency()
                bid_price, ask_price = self._getBidAskPrice(ins, curr)
                price = suggestValues.Number()
                prices.append(FMtMCalcVal.CalculatedPrice(ins, curr,
                        strMtMIsoDate, self.mtmMarket, bid_price,
                        ask_price, price, 0.0, 0.0, 0.0))
            return prices
        except Exception as e:
            self._logDebug('Failed to get ACM price for instrument '
                    '{0}. Exception={1}'.format(ins.Name(), e))
            return []

    def _calculateHistorical(self, ins, mtmDate, curr):

        result = self._getCalcFromHook(ael.Instrument[ins.Oid()],
            mtmDate, ael.Instrument[curr.Oid()])
        if result is not None:
            return result

        # mtmDate < self.today
        bid_price = 0.0
        ask_price = 0.0
        if self.bid_and_ask:
            bid_price = self._getMarketPrice(ins, mtmDate, curr,
                    'AverageBidPrice')
            ask_price = self._getMarketPrice(ins, mtmDate, curr,
                    'AverageAskPrice')
        settle_price = self._getMarketPrice(ins, mtmDate, curr)
        high_price = 0.0
        low_price = 0.0
        if self.high_and_low:
            high_price = self._getMarketPrice(ins, mtmDate, curr, 'HighPrice')
            low_price = self._getMarketPrice(ins, mtmDate, curr, 'LowPrice')
        last_price = 0.0
        if self.last:
            last_price = self._getMarketPrice(ins, mtmDate, curr, 'LastPrice')
        return [settle_price, bid_price, ask_price,
                high_price, low_price, last_price]

    def _getMarketPrice(self, ins, date, curr, priceFindType=None):
        calcInsMarketPriceArgs = acm.FDictionary()
        calcInsMarketPriceArgs['priceDate'] = date
        calcInsMarketPriceArgs['currency'] = curr
        if ins.Name() == FMtMSelInsCurr.HIST_FUNDING_INS_NAME:
            calcInsMarketPriceArgs['useSpecificCurrency'] = 1
        if priceFindType:
            calcInsMarketPriceArgs['typeOfPrice'] = priceFindType
            calcInsMarketPriceArgs['useSpecificTypeOfPrice'] = 1
        try:
            priceValue = (self._dealSheetCalcSpaceMngr.
                    getInsCalcMarketPriceParams(ins, calcInsMarketPriceArgs))
            return priceValue.Number()
        except Exception as ex:
            price = priceFindType or 'MarketPrice'
            self._logWarning('Could not get {0} for {1} on day {2} in '
                    '{3}'.format(price, ins.Name(), date, curr.Name()))
            self._logDebug(str(ex))
            return 0.0

    @staticmethod
    def _validPrice(price):
        if not price:
            return False
        if isinstance(price, float):
            return not (math.isinf(price) or math.isnan(price))
        return True

    def _getPrices(self, mtmDate, insCurrPair):

        bid_price = 0.0
        ask_price = 0.0
        high_price = 0.0
        low_price = 0.0
        last_price = 0.0

        if self.bid_and_ask:
            bid_price = self._getMarketPrice(insCurrPair.ins,
                mtmDate, insCurrPair.curr, 'AverageBidPrice')
            ask_price = self._getMarketPrice(insCurrPair.ins,
                mtmDate, insCurrPair.curr, 'AverageAskPrice')
        if self.high_and_low:
            high_price = self._getMarketPrice(insCurrPair.ins,
                mtmDate, insCurrPair.curr, 'HighPrice')
            low_price = self._getMarketPrice(insCurrPair.ins,
                mtmDate, insCurrPair.curr, 'LowPrice')
        if self.last:
            last_price = self._getMarketPrice(insCurrPair.ins,
                mtmDate, insCurrPair.curr, 'LastPrice')
        return [bid_price, ask_price, high_price, low_price, last_price]

    def calculate(self):

        for insCurrPair in self.insCurrPairList:
            insOid = insCurrPair.ins.Oid()
            currOid = insCurrPair.curr.Oid()
            #- Calculate only once
            if self._calcPriceCache.getCalcPrice(insOid, currOid):
                continue
            #- Calculate Mid and perhaps Bid and Ask prices
            if (insCurrPair.ins.InsType() in ['CurrSwap', 'FxSwap'] and
                    self.mtmDate >= self.today):
                calcPrices = self._calculateLegPrices(insCurrPair.ins)
            else:
                args = [insCurrPair.ins, self.mtmDate, insCurrPair.curr]
                #
                bid_price = 0.0
                ask_price = 0.0
                settle_price = 0.0
                high_price = 0.0
                low_price = 0.0
                last_price = 0.0
                if self.backDated:
                    bid_price, ask_price, high_price, low_price, last_price = \
                                       self._getPrices(self.today, insCurrPair)
                    settle_price = self._calculate(*args)
                else:
                    if self.mtmDate < self.today:
                        mtmDate = self.mtmDate
                        settle_price = self._calculateHistorical(*args)
                        if (isinstance(settle_price, list) and
                                math.isnan(settle_price[0])):
                            settle_price = self._calculate(*args)
                            mtmDate = self.today
                        bid_price, ask_price, high_price, low_price, last_price = \
                                       self._getPrices(mtmDate, insCurrPair)
                    elif self.useYesterday:
                        cal = insCurrPair.curr.Calendar()
                        yesterday = cal.AdjustBankingDays(self.mtmDate, -1)
                        settle_price = FFxCommon.getMtMRate(insCurrPair.ins,
                            insCurrPair.curr,
                            'Settle', self.sourceMtmMarket, yesterday)
                        if self.bid_and_ask:
                            bid_price = FFxCommon.getMtMRate(insCurrPair.ins,
                                insCurrPair.curr,
                                'Bid', self.sourceMtmMarket, yesterday)
                            ask_price = FFxCommon.getMtMRate(insCurrPair.ins,
                                insCurrPair.curr,
                                'Ask', self.sourceMtmMarket, yesterday)
                        if self.high_and_low:
                            high_price = FFxCommon.getMtMRate(insCurrPair.ins,
                                insCurrPair.curr,
                                'High', self.sourceMtmMarket, yesterday)
                            low_price = FFxCommon.getMtMRate(insCurrPair.ins,
                                insCurrPair.curr,
                                'Low', self.sourceMtmMarket, yesterday)
                        if self.last:
                            last_price = FFxCommon.getMtMRate(insCurrPair.ins,
                                insCurrPair.curr,
                                'Last', self.sourceMtmMarket, yesterday)
                    else:
                        bid_price, ask_price, high_price, low_price, last_price = \
                            self._getPrices(self.mtmDate, insCurrPair)
                        settle_price = self._calculate(*args)

                if isinstance(settle_price, list):
                    bid_price = settle_price[1] or 0.0
                    ask_price = settle_price[2] or 0.0
                    high_price = settle_price[3] or 0.0
                    low_price = settle_price[4] or 0.0
                    last_price = settle_price[5] or 0.0
                    settle_price = settle_price[0]
                strMtMIsoDate = self.mtmDate.to_string(ael.DATE_ISO)
                calcPrices = [FMtMCalcVal.CalculatedPrice(insCurrPair.ins,
                        insCurrPair.curr, strMtMIsoDate, self.mtmMarket,
                        bid_price, ask_price, settle_price,
                        high_price, low_price, last_price)]
            # Now deal with calcPrices
            validCalcPrices = self._excludeBadPrices(calcPrices)
            # Get the calcPrices and update local/global cache
            for calcPrice in validCalcPrices:
                calcPriceCurrOid = calcPrice.getCurr().Oid()
                self._calcPriceCache.setCalcPrice(insOid, calcPriceCurrOid,
                        calcPrice)
        return

    def _correctBadPrices(self, price, funcName):
        value = getattr(price, "get" + funcName)()
        if math.isinf(value) or math.isnan(value):
            if self.use_zero_prices:
                self._logDebug('            Bad {0} price \'{1}\' for '
                        '\'{2}\' in \'{3}\' corrected to 0.0'.format(
                        funcName, value, price.getIns().Name(),
                        price.getCurr().Name()))
                getattr(price, "set" + funcName)(0.0)
            else:
                self._logDebug('            Bad {0} price \'{1}\' for '
                        '\'{2}\' in \'{3}\' skipped'.format(
                        funcName, value, price.getIns().Name(),
                        price.getCurr().Name()))

    def _excludeBadPrices(self, calcPrices):
        """
        Exclude bad prices from the given list of calcPrices.  Inf and NaN
        value in the prices will be corrected to 0.0.  If zero prices is
        to be excluded, price with zero settle value will be ignored.  Returns
        a list of valid calculated prices.
        """
        validCalcPrices = []
        for cp in calcPrices:
            # Processing settle value
            settleVal = cp.getSettle()
            self._correctBadPrices(cp, 'Settle')

            # Processing bid/ask values
            if self.bid_and_ask:
                self._correctBadPrices(cp, 'Bid')
                self._correctBadPrices(cp, 'Ask')

            # zero price should be ignored
            ignorePrice, ignMsg = (False, '')
            curSettleVal = cp.getSettle()
            if curSettleVal == 0.0 and self.exclude_zero:
                ignorePrice = True
                if settleVal == 0.0:  # If it was zero
                    ignMsg = ('Zero settle price exclusion for {0} [{1}] '
                            'on {2}.'.format(cp.getIns().Name(),
                            cp.getCurr().Name(), cp.getDate()))
                else:  # If it wasn't zero, but was corrected to zero.
                    ignMsg = ('Bad settle price \'{0}\' for {1} [{2}] on '
                        '{3} was corrected to 0.0 and then removed by '
                        'zero price exclusion.'.format(settleVal,
                        cp.getIns().Name(), cp.getCurr().Name(),
                        cp.getDate()))

            # Ignore bad prices
            if curSettleVal is None or math.isinf(curSettleVal) or math.isnan(curSettleVal):
                ignorePrice = True

            # Need an unique id for instrument and currency.
            sid = (cp.getIns().Oid(), cp.getCurr().Oid())
            if ignorePrice:
                cp.markAsSaved()
                cp.markAsInvalid()
                validCalcPrices.append(cp)
                self._summaryAddIgnore('Price', sid, 'CALCULATE', [ignMsg])
                self._logWarning(ignMsg)
            else:
                validCalcPrices.append(cp)
                self._summaryAddOk('Price', sid, 'CALCULATE')
        return validCalcPrices

    def _postAdjust(self, ins, value):
        """
        PostAdjust: Note SetPostAdjustHook only sets per class
        """
        if value is None or math.isinf(value) or math.isnan(value):
            return None
        else:
            if MtMTaskPrice.post_adjust_hook:
                aelIns = ael.Instrument[ins.Oid()]
                return MtMTaskPrice.post_adjust_hook.im_func(aelIns, value)
            if self.digits != '':
                return round(value, self.digits)
            return value

    def save(self):

        with self._getPriceBatchTransactionControlHandler() as batchCtrlHndl:
            for insCurrPair in self.insCurrPairList:
                ins = insCurrPair.ins
                insOid = ins.Oid()
                curr = insCurrPair.curr
                currOid = curr.Oid()
                self._logInfo('        Saving prices for instrument '
                        '\'{0}\' in currency \'{1}\'.'.format(ins.Name(),
                        curr.Name()))
                calcPrice = self._calcPriceCache.getCalcPrice(insOid, currOid)
                if not calcPrice:
                    self._logDebug('        Unable to find calculated price '
                            'for instrument \'{0}\' in currency '
                            '\'{1}\'.'.format(ins.Name(), curr.Name()))
                    continue
                self._logDebug('        Calculated price for instrument '
                        '\'{0}\' in currency \'{1}\' found.'.format(
                        ins.Name(), curr.Name()))
                if calcPrice.isSaved():
                    self._logDebug('        Calculated price already '
                            'enqueued to be saved'.format(ins.Name(),
                            curr.Name()))
                    continue
                #- PostAdjust
                settle = calcPrice.getSettle()
                postAdjustSettleValue = self._postAdjust(ins, settle)
                if self.bid_and_ask:
                    bid = calcPrice.getBid()
                    postAdjustBidValue = self._postAdjust(ins, bid)
                    ask = calcPrice.getAsk()
                    postAdjustAskValue = self._postAdjust(ins, ask)
                else:
                    postAdjustBidValue = None
                    postAdjustAskValue = None

                if self.high_and_low:
                    high = calcPrice.getHigh()
                    postAdjustHighValue = self._postAdjust(ins, high)
                    low = calcPrice.getLow()
                    postAdjustLowValue = self._postAdjust(ins, low)
                else:
                    postAdjustHighValue = None
                    postAdjustLowValue = None

                if self.last:
                    last = calcPrice.getLast()
                    postAdjustLastValue = self._postAdjust(ins, last)
                else:
                    postAdjustLastValue = None

                preAdjustBidValue = calcPrice.getBid()
                preAdjustAskValue = calcPrice.getAsk()
                preAdjustSettleValue = calcPrice.getSettle()
                preAdjustHighValue = calcPrice.getHigh()
                preAdjustLowValue = calcPrice.getLow()
                preAdjustLastValue = calcPrice.getLast()
                calcPrice.setBid(postAdjustBidValue)
                calcPrice.setAsk(postAdjustAskValue)
                calcPrice.setSettle(postAdjustSettleValue)
                calcPrice.setHigh(postAdjustHighValue)
                calcPrice.setLow(postAdjustLowValue)
                calcPrice.setLast(postAdjustLastValue)
                self._logDebug('        Post Adjust: '
                        'Bid: {0} => {1}, Ask: {2} => {3}, '
                        'Settle: {4} => {5}, Last: {6} => {7}, '
                        'High: {8} => {9}, Low: {10} => {11}'.format(
                        preAdjustBidValue, postAdjustBidValue,
                        preAdjustAskValue, postAdjustAskValue,
                        preAdjustSettleValue, postAdjustSettleValue,
                        preAdjustLastValue, postAdjustLastValue,
                        preAdjustHighValue, postAdjustHighValue,
                        preAdjustLowValue, postAdjustLowValue,
                        ))
                if batchCtrlHndl.commit(calcPrice):
                    self._logDebug('        Calculated price enqueued.')
                else:
                    self._logDebug('        Calculated price ignored.')
                calcPrice.markAsSaved()


class MtMTaskPricePreferredMarket(MtMTaskPrice):
    """------------------------------------------------------------------------
    CLASS
        MtMTaskPricePreferredMarket --> MtMTaskPrice --> MtMTask

    DESCRIPTION
        The MtMTaskPricePreferredMarket calculates a mtm_from_feed marked
        instruments using prices order by a PreferredMarketHandler.
    USAGE:
    NOTE:
       - If a calculation hook is on MtMTaskPricePreferredMarket it will
       override the default behaviour.
       - If a calculation hook is not set on MtMTaskPricePreferredMarket but
       the MtMTaskPrice calculation hook should be used for instruments using
       the standard mtm defined in MtMTaskPrice make sure to set it on
       MtMTaskPrice before using this class.
    ------------------------------------------------------------------------"""

    def __init__(self, world, mtmDate, mtmMarket, insCurrPairList,
            calcPriceCache, pref_handler, exclude_instypes=[],
            exclude_zero=0, bid_and_ask=0, high_and_low=0, last=0,
            use_zero_prices=1, digits=4, override_price=0,
            useYesterday=0, sourceMtmMarket=None, backDated=0):
        """
        CONSTRUCTOR ARGUMENTS:
        pref_handler: A PreferredMarketHandler.
        exclude_instypes: A list of instypes to exclude using preferred marker
            order calculation.  Excluded instrument will be calculated using
            the super class calculate()
        """
        MtMTaskPrice.__init__(self, world, mtmDate, mtmMarket, insCurrPairList,
                calcPriceCache, exclude_zero, bid_and_ask, high_and_low, last,
                use_zero_prices, digits,
                override_price, useYesterday,
                sourceMtmMarket, backDated)
        self.pref_handler = pref_handler
        self.exclude_instypes = exclude_instypes

    def _calculateHistorical(self, ins, mtmDate, curr):

        result = self._getCalcFromHook(ins, mtmDate, curr)
        if result is not None:
            return result

        if not ins.MtmFromFeed() or ins.InsType() in self.exclude_instypes:
            return MtMTaskPrice._calculateHistorical(self, ins,
                    mtmDate, curr)
        else:
            return self.__getPreferredPrices(ins, mtmDate, curr, False)

    def _calculate(self, ins, mtmDate, curr):
        """
        calculates a pure price without rounding
        """

        result = self._getCalcFromHook(ins, mtmDate, curr)
        if result is not None:
            return result

        if not ins.MtmFromFeed() or ins.InsType() in self.exclude_instypes:
            return MtMTaskPrice._calculate(self, ins, mtmDate,
                    curr)
        else:
            return self.__getPreferredPrices(ins, mtmDate, curr,
                    True)

    def __getPreferredPrices(self, ins, mtmDate, curr, latest):
        value = 0.0
        prices, pfrulename = self.pref_handler.Prices(ins, mtmDate, latest)
        for p in prices:
            if p.Currency().Name() != curr.Name():
                continue
            value = self._choosePriceValue(p, pfrulename)
            if not FBDPCommon.eps_compare(value):
                return [value,
                        FMtMUtil.getBidValue(p), FMtMUtil.getAskValue(p),
                        FMtMUtil.getHighValue(p), FMtMUtil.getLowValue(p),
                        FMtMUtil.getLastValue(p)]
        return value

    def _getPriceFindType(self, pfrulename):

        # First stage, find the 'type' i.e. which value to be used in the
        # price information.
        typ = None
        # Use the pfrulename to find the price finding rule and the specified
        # price type.
        if not typ:
            pfrule = None
            if pfrulename:
                pfrule = acm.FPriceFinding[pfrulename]
            if pfrule:
                typ = pfrule.PriceType()
        # 'type' is still not found.  Use the valuation parameters then.
        if not typ:
            defaultValParam = ael.used_valuation_parameters()
            if defaultValParam:
                typ = defaultValParam.prif_type
        return typ

    def _calcAverage(self, *values):
        """
        Return None if no values, otherwise return average
        """
        return sum(values) / len(values) if values else None

    def _priceCalcSprAvgValue(self, acmPrice):

        # If there are bid and ask value, use bid and ask spread
        if FMtMUtil.hasBidValue(acmPrice) and FMtMUtil.hasAskValue(acmPrice):
            return self._calcAverage(acmPrice.Bid(), acmPrice.Ask())
        # Then either bid or ask value is present.
        values = []
        if FMtMUtil.hasBidValue(acmPrice):
            values.append(acmPrice.Bid())
            if (FMtMUtil.hasLastValue(acmPrice) and
                    acmPrice.Last() > acmPrice.Bid()):
                values.append(acmPrice.Last())
        elif FMtMUtil.hasAskValue(acmPrice):
            values.append(acmPrice.Ask())
            if (FMtMUtil.hasLastValue(acmPrice) and
                    acmPrice.Last() < acmPrice.Ask()):
                values.append(acmPrice.Last())
        return self._calcAverage(*values)

    def _priceCalcMedianValue(self, acmPrice):

        values = []
        if FMtMUtil.hasLastValue(acmPrice):
            values.append(acmPrice.Last())
        if FMtMUtil.hasBidValue(acmPrice):
            values.append(acmPrice.Bid())
        if FMtMUtil.hasAskValue(acmPrice):
            values.append(acmPrice.Ask())
        return self._calcAverage(*values)

    def _priceCalcFallbackValue(self, acmPrice):

        if FMtMUtil.hasLastValue(acmPrice):
            return acmPrice.Last()
        if FMtMUtil.hasSettleValue(acmPrice):
            return acmPrice.Settle()
        if FMtMUtil.hasBidValue(acmPrice) and FMtMUtil.hasAskValue(acmPrice):
            return self._calcAverage(acmPrice.Bid(), acmPrice.Ask())
        return 0.0

    def _choosePriceValue(self, acmPrice, pfrulename):
        """
        Return price according to price find type in valuation parameters.
        Otherwise return either settle, last or a mid price.
        Function unit-tested by test_MtMTask module.
        """
        typ = self._getPriceFindType(pfrulename)
        # Base on the price type, return the value.
        val = None
        if typ == 'Last':
            if FMtMUtil.hasLastValue(acmPrice):
                val = acmPrice.Last()
        elif typ == 'Bid':
            if FMtMUtil.hasBidValue(acmPrice):
                val = acmPrice.Bid()
        elif typ == 'Ask':
            if FMtMUtil.hasAskValue(acmPrice):
                val = acmPrice.Ask()
        elif typ == 'Close':
            if FMtMUtil.hasSettleValue(acmPrice):
                val = acmPrice.Settle()
        elif typ == 'SprAvg':
            sprAvgVal = self._priceCalcSprAvgValue(acmPrice)
            if sprAvgVal is not None:
                val = sprAvgVal
        elif typ == 'Median':
            medianVal = self._priceCalcMedianValue(acmPrice)
            if medianVal is not None:
                val = medianVal
        # Return the chosen value, otherwise use fallback value
        if val is not None:
            return val
        return self._priceCalcFallbackValue(acmPrice)


class MtMTaskVol(MtMTask):
    """------------------------------------------------------------------------
    CLASS
        MtMTaskVol --> MtMTask
    DESCRIPTION
        The MtMTaskVol class calculates and stores implied volatilities based
        on the option mtm and underlying price. One surface per underlying and
        options with the same strike_curr.
    USAGE:
    NOTE:
       - !!! To be able to create the context links they must be generated
        before the calculate() and save() of MtM prices, Yield, etc is done
        because a ael.poll() must be called after generation. This is done in
        the constructor.
       - The Derivative and the underlying price is taken from already
        calculated mtm prices i.e. such prices most accessible by
        CalculatedPrice. This means that a MtMTaskPrice must have calculated
        the underlying and the option price.
    ------------------------------------------------------------------------"""

    def __init__(self, world, mtmDate, mtmMarket, undAndDersList, base='Name',
            vol_prefix=None, vol_suffix=None, context='Global',
            call_put=0, ca_adjust_regexp=r'_ca\d\d\d\d-\d\d-\d\d$',
            remove_zero_volatilities=1):
        """
        CONSTRUCTOR ARGUMENTS:
        base: 'Name','ExternalIid2' or any good name field.
        vol_suffix: Suffix to use on the volatility surface and context link.
        context: Name in the context were to add context links. PERHAPS A LIST,
            REMOVE LATER
        cut_off: Max volatility, 1.0 means 100%.
        ca_adjust_regexp: Regular expression defining.
        """
        MtMTask.__init__(self, world, mtmDate, mtmMarket)
        assert isinstance(undAndDersList, list), ('The given '
                '\'undAndDersList\' must be an instance of list.')
        for elem in undAndDersList:
            assert isinstance(elem, FMtMUtil.UndAndDers), ('The elements in '
                    'the \'undAndDersList\' must be an instance of '
                    'FMtMUtil.UndAndDers.')
        mapping = {'insid': 'Name', 'extern_id1': 'ExternalId1'}
        base = (base in mapping) and mapping[base] or base
        self.base = base
        self.vol_suffix = vol_suffix
        self.vol_prefix = vol_prefix
        self.context = context
        self.call_put = call_put
        self.ca_adjust_regexp = ca_adjust_regexp
        self.buckets = {}  # und: ListDict{}, und: { strike_curr : [options] }
        context = acm.FContext[self.context]
        if not context:
            raise RuntimeError('Context not found. Check variable "Link '
                    'Volatility Structure in Context" in the GUI and rerun!')
        self.__undAndDersList = undAndDersList
        self.__volsInfo = FMtMUtil.VolsInfo()
        self.__remove_zero_volatilities = remove_zero_volatilities

    def calculate(self):

        raise NotImplementedError('This class is intended NOT to have '
                'calculate() method')

    def save(self):

        for undAndDers in self.__undAndDersList:
            undIns = undAndDers.undIns
            derStrikeCurrOidSet = set()
            for derIns in undAndDers.derInsList:
                derStrikeCurrOidSet.add(derIns.StrikeCurrency().Oid())
            derStrikeCurrList = [acm.FCurrency[currOid] for
                    currOid in derStrikeCurrOidSet]
            for derStrikeCurr in derStrikeCurrList:
                derStrikeCurrOid = derStrikeCurr.Oid()
                # Create surface
                vol = self.__getVolStruct(undIns, derStrikeCurr)
                vol.RemoveExpired()
                # build instrument array
                insArray = acm.FArray()
                for derIns in undAndDers.derInsList:
                    if derIns.StrikeCurrency().Oid() != derStrikeCurrOid:
                        continue
                    if not self.__isDerInsToBeIgnored(derIns):
                        insArray.Add(derIns)
                self._logDebug('        Creating points from {0} '
                        'instruments'.format(len(insArray)))
                res = vol.InsertPointArray(insArray)
                if not res:
                    self._logDebug('        Some instruments gave duplicate '
                            'points or were expired')
                try:
                    self.__addCxtLinks(undIns, derStrikeCurr, vol.Name())
                    self._logInfo('        Calibrating '
                            'for \'{0}\'.'.format(vol.Name()))
                    calcRtn = True
                    errMsg = ''
                    op = lambda vol: vol.CalcImpliedVolatilities()
                    calcRtn, errMsg = calibrateVolatility(
                                                    vol, legacyOp=op)
                    if errMsg != '':
                        self._logError('Calibrate volatility error '
                        'for \'{0}\', errMsg: {1}.'.format(
                        vol.Name(), errMsg))

                    if not calcRtn:
                        self._summaryAddFail(vol.RecordType(), vol.Oid(),
                            'CALIBRATE', reasons=[errMsg])
                    else:
                        if not self._isInTestMode():
                            if not vol.StructureType() in PROTECTED_TYPES \
                            and self.__remove_zero_volatilities:
                                vol.RemoveZeroVolatilities()
                            vol.Commit()
                        self._summaryAddOk(vol.RecordType(), vol.Oid(),
                                'CALCULATE')
                        self._logDebug(
                            '        Calculated implied volatility.')
                except Exception as e:
                    failMsg = (
                        'Failed to calculate implied volatility for '
                        '\'{0}\'.  {1}'.format(vol.Name(), e))
                    self._summaryAddFail(vol.RecordType(), vol.Oid(),
                            'CALCULATE', reasons=[failMsg])
                    self._logError(failMsg)
                undInsNameCurrName = undIns.Name() + derStrikeCurr.Name()
                volInsArrayPair = FMtMUtil.VolInsArrayPair(vol=vol,
                        insArray=insArray)
                self.__volsInfo.add(undInsNameCurrName, volInsArrayPair)

    def getVolsInfo(self):

        return self.__volsInfo

    def __getVolStruct(self, undIns, derStrikeCurr):

        volName = self.__getVolName(undIns, derStrikeCurr)
        vol = acm.FVolatilityStructure[volName]
        if vol:
            if self._isInTestMode():
                volClone = vol.Clone()
                self.__setInsRefOnVol(volClone, undIns)
                return volClone
            else:
                self.__setInsRefOnVol(vol, undIns)
        else:
            vol = self.__createNewVolStruct(undIns, derStrikeCurr, volName)
        # TODO: why?
        acm.PollDbEvents()
        ael.poll()
        return vol

    def __setInsRefOnVol(self, vol, undIns):

        if not vol.ReferenceInstrument():
            self._logWarning('Set missing underlying reference for surface '
                    '{0}'.format(vol.Name()))
            vol.ReferenceInstrument(undIns)
            if not self._isInTestMode():
                vol.Commit()

    def __createNewVolStruct(self, ins, curr, volName):

        if self.call_put:
            vol = acm.FBenchmarkCallPutVolatilityStructure()
        else:
            vol = acm.FBenchmarkVolatilityStructure()
        vol.Name(volName)
        vol.InterpolationMethod('Hermite')
        vol.RiskType('Equity Vol')
        vol.ReferenceInstrument(ins)
        vol.Currency(curr)
        vol.Framework('Black & Scholes')
        vol.StrikeType('Absolute')
        vol.VolatilityValueType('Absolute')
        vol.AbsUnderlyingMaturity(1)
        vol.BondVolatilityType('Price')
        try:
            self._logInfo('        Creating new volatility structure '
                    '\'{0}\'.'.format(vol.Name()))
            if not self._isInTestMode():
                vol.Commit()
            self._summaryAddOk(vol.RecordType(), vol.Oid(), 'CREATE')
            self._logDebug('        New volatility structure created.')
        except Exception as e:
            failMsg = ('Failed to create new volatility structure \'{0}\'.  '
                    '{1}'.format(vol.Name(), e))
            self._summaryAddFail(vol.RecordType(), vol.Oid(), 'CREATE',
                    reasons=[failMsg])
            self._logError(failMsg)
        return vol

    def __getVolName(self, und, curr):

        name = getattr(und, self.base)()
        s = ('{0}{1}{2}/{3}'.format(self.vol_prefix, name, self.vol_suffix,
                curr.Name()))
        return s[0:30]

    def __isDerInsToBeIgnored(self, derIns):
        """
        Predicate for check if the derivative should be ignored
        """
        isToBeIgnored = False
        if derIns.Generic():
            isToBeIgnored = True
            msg = ('Volatility benchmark {0} ignored. Instrument is '
                    'generic'.format(derIns.Name()))
        elif self.__isCorpActAdjusted(derIns):
            isToBeIgnored = True
            msg = ('Volatility benchmark {0} ignored. Exclusion rule in '
                    'GUI'.format(derIns.Name()))
        if isToBeIgnored:
            self._logDebug(msg)
        return isToBeIgnored

    def __isCorpActAdjusted(self, ins):

        if self.ca_adjust_regexp:
            if re.search(self.ca_adjust_regexp, ins.Name(), re.I):
                return True
        return False

    def __addCxtLinks(self, undIns, derStrikeCurr, volName):
        """
        Make sure that surfaces and context links exists for the underlying.
        One link per underlying
        """
        context = acm.FContext[self.context]
        ctxlnks = [ctxlnk for ctxlnk in acm.FContextLink.Select(
                'instrument=\'{0}\''.format(undIns.Name()))]
        contextRenamed = False
        for c in ctxlnks:
            if c.Context().Name() == self.context and c.Name() == volName:
                self._logDebug('Found link: {0}'.format(volName))
                return
        for c in ctxlnks:
            if (c.Context().Name() == self.context and
                    c.Instrument() == undIns and
                    c.Type() == 'Volatility' and
                    c.MappingType() == 'Instrument' and
                    (not c.Currency() or c.Currency() == derStrikeCurr)):
                self._logDebug('Renaming Context {0}=>{1}'.format(
                        c.Name(), volName))
                contextRenamed = True
                break
        found = False
        if contextRenamed:
            for newlink in context.ContextLinks():
                if newlink.Oid() == c.Oid():
                    self._logDebug('Found old link!')
                    found = True
                    break
        if not found:
            newlink = acm.FContextLink()
            newlink.Context(context)
        newlink.Currency(derStrikeCurr)
        newlink.Instrument(undIns)
        newlink.Type('Volatility')
        newlink.MappingType('Instrument')
        newlink.Name(volName[0:30])
        try:
            self._logInfo('        Creating new context link \'{0}\' to '
                    'context \'{1}\'.'.format(newlink.Name(), self.context))
            if not self._isInTestMode():
                newlink.Commit()
            self._logDebug('        New context link created.'.format(
                    newlink.Name(), self.context))
        except Exception as e:
            failMsg = ('Failed to create new context link \'{0}\' to context '
                    '\'{1}\'.  {2}'.format(newlink.Name(), self.context, e))
            self._summaryAddFail(newlink.RecordType(), newlink.Oid(),
                    'CREATE', reasons=[failMsg])
            self._logError(failMsg)


class MtMTaskVolPrice(MtMTask,
        FMtMUtil.PriceBatchTransactionControlHandlerInterface):
    """------------------------------------------------------------------------
    CLASS
        MtMTaskVolPrice --> MtMTask
    DESCRIPTION
        Saves volatilities as prices in the price table. This class is not
        able to calculate any volatilities itself but relies on that
        volatilities have been calculated and published beforehand (by
        MtMTaskVol).
    ------------------------------------------------------------------------"""

    def __init__(self, world, mtmDate, mtmMarket, undAndDersList, volsInfo):

        assert mtmMarket is not None, ('This derived class required a mtm '
                'market.')
        MtMTask.__init__(self, world, mtmDate, mtmMarket)
        FMtMUtil.PriceBatchTransactionControlHandlerInterface.__init__(self,
                world, override=False)
        assert isinstance(undAndDersList, list), ('The given '
                '\'undAndDersList\' must be an instance of list.')
        for elem in undAndDersList:
            assert isinstance(elem, FMtMUtil.UndAndDers), ('The elements in '
                    'the \'undAndDersList\' must be an instance of '
                    'FMtMUtil.UndAndDers.')
        self.__undAndDersList = undAndDersList
        self.__localCalcVolPriceCache = {}  # indexed by derIns only
        self.__volsInfo = volsInfo

    def calculate(self):

        strMtMIsoDate = self.mtmDate.to_string(ael.DATE_ISO)
        for undAndDers in self.__undAndDersList:
            undIns = undAndDers.undIns
            for derIns in undAndDers.derInsList:
                vol, insArray = self.__volsInfo.get(
                        undIns.Name() + derIns.StrikeCurrency().Name())
                if derIns not in insArray:
                    continue
                if derIns in self.__localCalcVolPriceCache:
                    # cache hit
                    continue
                volValue = vol.GetVolatility(derIns)
                calcVolPrice = FMtMCalcVal.CalculatedVolPrice(derIns,
                        derIns.Currency(), strMtMIsoDate, self.mtmMarket,
                        volValue, 0.00, 0.00, 0.00, 0.00, 0.00)
                self.__localCalcVolPriceCache[derIns] = calcVolPrice

    def save(self):
        """
        It is an error to call this operation on a non-underlying
        """
        with self._getPriceBatchTransactionControlHandler() as batchCtrlHndl:
            for undAndDers in self.__undAndDersList:
                for derIns in undAndDers.derInsList:
                    self._logInfo('        Saving prices for instrument '
                            '\'{0}\'.'.format(derIns.Name()))
                    if derIns not in self.__localCalcVolPriceCache:
                        self._logWarning('Calculated Vol Price not found for '
                        'instrument \'{0}\'.'.format(derIns.Name()))
                        continue
                    calcVolPrice = self.__localCalcVolPriceCache[derIns]
                    if calcVolPrice.isSaved():
                        continue
                    batchCtrlHndl.commit(calcVolPrice)


class MtMTaskRecalcVolStructs(MtMTask):
    """------------------------------------------------------------------------
    CLASS
        MtMTaskRecalcVolStructs --> MtMTask
    DESCRIPTION
        An MtMTaskRecalcVolStructs is a simplified task that just
        recalculates existing volatility surfaces, i.e. calculate() and save()
        in one operation which is done in save(). Expired benchmark instruments
        are removed from the surface.
    USAGE:
    NOTE:
        - It is intended not to have calculate() method.
    ------------------------------------------------------------------------"""

    def __init__(self, world, mtmDate, volList, remove_zero_volatilities,
                 apply_filter):

        MtMTask.__init__(self, world, mtmDate, None)
        self.__volList = volList
        self.__remove_zero_volatilities = remove_zero_volatilities
        self.__apply_filter = apply_filter

    def calculate(self):

        raise NotImplementedError('This class is intended NOT to have '
                'calculate() method')

    def applyFilter(self, vol):
        query = acm.FStoredASQLQuery.Select('name=%s' % (vol.Name()))
        if query:
            asqlQuery = query[0]
            collection = asqlQuery.Query().Select().AsArray()
            vol.ApplyInstruments(collection, False)
        return

    def save(self):
        for vol in self.__volList:
            self._logInfo('    Saving recalculation for volatility structure '
                    '\'{0}\'.'.format(vol.Name()))
            try:
                vol.RemoveExpired()
                clone = vol.Clone()
                if self.__apply_filter:
                    self.applyFilter(clone)

                # Calc Implied Volatilities ----->
                framework = vol.Framework()
                volatilityValueType = vol.VolatilityValueType()
                if framework in ('Ho & Lee', 'Hull & White'):
                    vol.Framework('Black & Scholes')
                    vol.VolatilityValueType('Relative')
                calcRtn = True
                errMsg = ''
                if 'SABR' == clone.StructureType():
                    clone.UpdateUnderlyingForwards()
                    clone.CalcSabrAtmVol()
                    clone.CalcImpliedVolatilities()
                    calcRtn, errMsg = calibrateVolatility(clone)
                elif 'SVI' == clone.StructureType():
                    clone.UpdateUnderlyingForwards()
                    clone.RefreshFilter()
                    clone.CalcImpliedVolatilities()
                    calcRtn, errMsg = calibrateVolatility(clone)
                else:
                    op = lambda vol: \
                        vol.CalcImpliedVolatilities()
                    calcRtn, errMsg = calibrateVolatility(
                                                    clone, legacyOp=op)
                if errMsg != '':
                    self._logError('Calibrate volatility error '
                        'for \'{0}\', errMsg: {1}.'.format(
                        vol.Name(), errMsg))
                if not calcRtn:
                    self._summaryAddFail(vol.RecordType(), vol.Oid(),
                            'RECALCULATE', reasons=[errMsg])
                    continue
                vol.Apply(clone)
                if framework in ('Ho & Lee', 'Hull & White'):
                    vol.Framework(framework)
                    vol.VolatilityValueType(volatilityValueType)
                # <-----
                if not self._isInTestMode():
                    if not vol.StructureType() in PROTECTED_TYPES and \
                            self.__remove_zero_volatilities:
                        vol.RemoveZeroVolatilities()
                    vol.Commit()
                self._summaryAddOk(vol.RecordType(), vol.Oid(), 'RECALCULATE')
                self._logDebug('    Recalculated volatility structure \'{0}\' '
                        'saved.'.format(vol.Name()))
            except Exception as e:
                failMsg = ('Failed to recalculate and save volatility '
                        'structure \'{0}\'. {1}'.format(vol.Name(), e))
                self._logError(failMsg)
                self._summaryAddFail(vol.RecordType(), vol.Oid(),
                        'RECALCULATE', reasons=[failMsg])


class MtMTaskRecalcYieldCurves(MtMTask):
    """------------------------------------------------------------------------
    CLASS
        MtMTaskRecalcYieldCurve --> MtMTask
    DESCRIPTION
        An MtMTaskRecalcYieldCurve is a simplified task that just recalculates
        existing yield curves, i.e. calculate() and save() in one operation
        which is done in save().
    USAGE:
    NOTE:
        - It is intended not to have calculate() method.
    ------------------------------------------------------------------------"""

    def __init__(self, world, mtmDate, ycList):

        MtMTask.__init__(self, world, mtmDate, None)
        self.__ycList = ycList

    def calculate(self):

        raise NotImplementedError('This class is intended NOT to have '
                'calculate() method')

    def __backupInstrumentSpreads(self, acmYc):
        insSpreadMap = {}
        spreads = acm.FInstrumentSpread.Select('curve="%s"' % (acmYc.Name()))
        for s in spreads:
            insSpreadMap[s.Instrument().Name()] = s.Spread()
        return insSpreadMap

    def __validateCalibration(self, acmYc, insSpreadMap):
        spreads = acm.FInstrumentSpread.Select('curve="%s"' % (acmYc.Name()))
        for s in spreads:
            if math.isnan(s.Spread()) or math.isinf(s.Spread()):
                s.Spread(insSpreadMap[s.Instrument().Name()])
                warningMsg = ('Calibration of \'{0}\' is reverted as '
                        '\'nan or inf\' found after calibration.'.format(
                        s.Instrument().Name()))
                self._logWarning(warningMsg)

    def __recalcAndSaveYc(self, acmYc, calibrationResults=None, \
          recalcOp=lambda yc, calcResults: yc.Calculate(calcResults)):

        self._logInfo('    Saving recalculation for yield curve '
            '\'{0}\'.'.format(acmYc.Name()))
        if FBDPYieldCurveLib.isAcmYieldCurveArchived(acmYc):
            self._logWarning('Yield curve \'{0}\' is found to be archived. '
                    'This is not a supported setup. The calibration '
                    'consistency for this curve and for curves depending on '
                    'this curve cannot be guaranteed.'.format(acmYc.Name()))
        try:
            if calibrationResults:
                recalcOp(acmYc, calibrationResults)
                errMsgs = []
                rtn = True
                for result in calibrationResults.Results().Values():
                    rtn = result.SolverResult().Success()
                    if not rtn:
                        errMsg = result.SolverResult().ErrorMessage()
                        if errMsg:
                            errMsgs.append(errMsg)
                if not rtn or errMsgs:
                    errMsgs = 'Reasons: ' + ' '.join(errMsgs) + '.'
                    errMsg = ('Skipping the yield curve '
                          '\'{0}\'. Calculation Failed. {1}'.format(
                          acmYc.Name(), errMsgs))
                    self._summaryAddFail(acmYc.RecordType(), acmYc.Oid(),
                        'RECALCULATE', reasons=[errMsg])
                    self._logError(errMsg)
                    return
            else:
                insSpreadMap = self.__backupInstrumentSpreads(acmYc)
                recalcOp(acmYc)
                self.__validateCalibration(acmYc, insSpreadMap)

            if not self._isInTestMode():
                acmYc.Commit()
            self._logDebug('    Recalculated {0} Yield Curves '
                '\'{1}\' saved.'.format(acmYc.Type(), acmYc.Name()))
            self._summaryAddOk(acmYc.RecordType(), acmYc.Oid(),
                'RECALCULATE')

        except Exception as e:
            failMsg = ('Failed to recalculate and save for {0} yield curve '
                    '\'{1}\'.  {2}'.format(acmYc.Type(), acmYc.Name(), e))
            self._logError(failMsg)
            self._summaryAddFail(acmYc.RecordType(), acmYc.Oid(),
                    'RECALCULATE', reasons=[failMsg])
        return

    def save(self):

        # Split yield curves into those calling CalibrateSpreads(), those
        # calling Calculate() and filter out those cannot be recalculated.
        ycToCalculate = []
        ycToCalibrateSpreads = []
        for yc in self.__ycList:
            ycType = yc.Type()
            # Instrument spreads curves do not have Calculate() method, but
            # still have CalibrateSpreads() method for recalculation.
            if ycType in FBDPYieldCurveLib.CURVE_TYPES_SUPPORT_CALCULATE:
                ycToCalculate.append(yc)
                continue
            if ycType in (FBDPYieldCurveLib.
                    CURVE_TYPES_SUPPORT_CALIBRATE_SPREADS):
                ycToCalibrateSpreads.append(yc)
                continue
            ignMsg = ('Yield curve \'{0}\' of type \'{1}\' cannot be '
                    'recalculated.'.format(yc.Name(), ycType))
            self._summaryAddIgnore(yc.RecordType(), yc.Oid(), 'RECALCULATE',
                    reasons=[ignMsg])
            self._logWarning(ignMsg)
        # For those calling Calculate()
        recalcOpCalculate = lambda yc, results: yc.Calculate(results)
        for yc in ycToCalculate:
            calcResults = acm.FCalibrationResults()
            self.__recalcAndSaveYc(yc, calibrationResults=calcResults,
                recalcOp=recalcOpCalculate)
        # For those calling CalibrateSpreads()
        recalcOpCalibrateSpreads = lambda yc: yc.CalibrateSpreads()
        for yc in ycToCalibrateSpreads:
            self.__recalcAndSaveYc(yc, calibrationResults=None,
                recalcOp=recalcOpCalibrateSpreads)
