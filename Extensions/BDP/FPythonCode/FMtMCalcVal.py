""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FMtMCalcVal.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

"""----------------------------------------------------------------------------
MODULE
    FMtMCalcVal - Module which provides calculation space related utilities to
    the Mark-to-Market script.

DESCRIPTION
    This module contains the calculated values functions used by the script
    FMarkToMarket.
----------------------------------------------------------------------------"""


import acm


import FBDPWorld
import FBDPCommon

from FMtMUtil import PRICE_BITMASK


class _ProcessTag(object):

    def __init__(self):

        self.__isSaved = False
        self.__isValid = True
        self.__isExisted = False
        self.__isFailure = False
        self.__errMsg = ''

    def isValid(self):

        return self.__isValid

    def isSaved(self):

        return self.__isSaved

    def isExisted(self):

        return self.__isExisted

    def isFailure(self):

        return self.__isFailure

    def markAsSaved(self):

        self.__isSaved = True

    def markAsInvalid(self):

        self.__isValid = False

    def markAsExisted(self):

        self.__isExisted = True

    def markAsFailure(self):

        self.__isSaved = False
        self.__isFailure = True

    def setErrMsg(self, errMsg):

        self.__errMsg = errMsg

    def getErrMsg(self):

        return self.__errMsg

    def __str__(self):

        s = ('ProcessTag[isSaved={0:<5},isValid={1:<5},isExisted={2:<5},'
                'isFailure={3:<5},errMsg="{4}"]'.format(self.__isSaved,
                self.__isValid, self.__isExisted, self.__isFailure,
                self.__errMsg))
        return s


class _PriceValue(object):

    def __init__(self, ins, curr, date, market,
                 bid, ask, settle, high, low, last):

        assert isinstance(date, str), 'bad date value'
        assert isinstance(bid, (int, float)) or bid is None, 'bad bid value'
        assert isinstance(ask, (int, float)) or ask is None, 'bad ask value'
        assert isinstance(settle, (int, float)), 'bad settle value'
        assert isinstance(high, (int, float)) or high is None, 'bad high value'
        assert isinstance(low, (int, float)) or low is None, 'bad low value'
        assert isinstance(last, (int, float)) or last is None, 'bad last value'
        self.__ins = ins
        self.__curr = curr
        self.__date = date
        self.__market = market
        self.__bid = bid
        self.__ask = ask
        self.__settle = settle
        self.__high = high
        self.__low = low
        self.__last = last

    def getIns(self):

        return self.__ins

    def getCurr(self):

        return self.__curr

    def getDate(self):

        return self.__date

    def getMarket(self):

        return self.__market

    def getBid(self):

        return self.__bid

    def getAsk(self):

        return self.__ask

    def getSettle(self):

        return self.__settle

    def getHigh(self):

        return self.__high

    def getLow(self):

        return self.__low

    def getLast(self):

        return self.__last

    def getBits(self):

        bits = PRICE_BITMASK['settle']
        bidVal = self.__bid
        if bidVal is not None:
            bits += PRICE_BITMASK['bid']
        askVal = self.__ask
        if askVal is not None:
            bits += PRICE_BITMASK['ask']
        if self.__high is not None:
            bits += PRICE_BITMASK['high']
        if self.__low is not None:
            bits += PRICE_BITMASK['low']
        if self.__last is not None:
            bits += PRICE_BITMASK['last']
        return bits

    def setIns(self, ins):

        self.__ins = ins

    def setBid(self, bid):

        self.__bid = bid

    def setAsk(self, ask):

        self.__ask = ask

    def setSettle(self, settle):

        self.__settle = settle

    def setHigh(self, high):

        self.__high = high

    def setLow(self, low):

        self.__low = low

    def setLast(self, last):

        self.__last = last

    def __str__(self):

        ss = ['PriceValue[']
        if self.__bid is not None:
            ss.append('{0:<8}: {1:f}'.format('Bid', self.__bid))
        if self._value.ask is not None:
            ss.append('{0:<8}: {1:f}'.format('Ask', self.__ask))
        if self.__last is not None:
            ss.append('{0:<8}: {1:f}'.format('Last', self.__last))
        if self.__high is not None:
            ss.append('{0:<8}: {1:f}'.format('High', self.__high))
        if self.__low is not None:
            ss.append('{0:<8}: {1:f}'.format('Low', self.__low))
        ss.append('{0:<8}: {1:f}'.format('Settle', self.__settle))
        ss.append('{0:<8}: {1}'.format('Curr', self.__curr.Name()))
        ss.append(']')
        return ' '.join(ss)


class _VolPriceValue(object):

    def __init__(self, ins, curr, date, market, vol,
                 bid, ask, high, low, last):

        assert isinstance(date, str), 'bad date value'
        assert isinstance(vol, (int, float)), 'bad vol value'
        self.__ins = ins
        self.__curr = curr
        self.__date = date
        self.__market = market
        self.__bid = bid
        self.__ask = ask
        self.__high = high
        self.__low = low
        self.__last = last
        self.__settle = vol

    def getIns(self):

        return self.__ins

    def getCurr(self):

        return self.__curr

    def getDate(self):

        return self.__date

    def getMarket(self):

        return self.__market

    def getVol(self):

        return self.__settle

    def getBid(self):

        return self.__bid

    def getAsk(self):

        return self.__ask

    def getSettle(self):

        return self.getVol()

    def getBits(self):

        return PRICE_BITMASK['settle']

    def getHigh(self):
        return self.__high

    def getLow(self):
        return self.__low

    def getLast(self):
        return self.__last

    def __str__(self):

        ss = ['VolPriceValue[']
        ss.append('{0:<8}: {1:f} '.format('Vol', self.getVol()))
        ss.append(']')
        return ' '.join(ss)


class CalculatedPrice(_PriceValue, _ProcessTag):

    def __init__(self, *args, **kwargs):

        _PriceValue.__init__(self, *args, **kwargs)
        _ProcessTag.__init__(self)

    def __str__(self):

        s0 = '<<< CalculatedPrice >>>'
        s1 = _PriceValue.__str__(self)
        s2 = _ProcessTag.__str__(self)
        return ' '.join([s0, s1, s2])


class CalculatedVolPrice(_VolPriceValue, _ProcessTag):

    def __init__(self, *args, **kwargs):

        _VolPriceValue.__init__(self, *args, **kwargs)
        _ProcessTag.__init__(self)

    def __str__(self):

        s0 = '<<< CalculatedVolPrice >>>'
        s1 = _VolPriceValue.__str__(self)
        s2 = _ProcessTag.__str__(self)
        return ' '.join([s0, s1, s2])


class CalculatedPriceCache(object):

    def __init__(self):

        self.__cache = {}

    def getCalcPrice(self, insOid, currOid):

        calcPrice = None
        if insOid in self.__cache and currOid in self.__cache[insOid]:
            calcPrice = self.__cache[insOid][currOid]
        return calcPrice

    def setCalcPrice(self, insOid, currOid, calcPrice):

        if not isinstance(calcPrice, CalculatedPrice):
            raise ValueError('The given calcPrice is not an instance of '
                    'CalculatedPrice.  The given calcPrice is of type '
                    '"{0}".'.format(type(calcPrice)))
        if insOid not in self.__cache:
            self.__cache[insOid] = {}
        self.__cache[insOid][currOid] = calcPrice


# #############################################################################
# Deal Sheet Calculation Space Management
# #############################################################################


class DealSheetCalcSpaceManager(FBDPWorld.WorldInterface):
    """
    Helper class for MtMTaskPrice and its derived classes.  This class is a
    proxy for isolating callls to the calc space.  This class manages automatic
    refresh after REFRESH_THRESHOLD_COUNT calls to the calc space.
    """
    SHEET_TYPE = 'FDealSheet'

    RefreshThresholdCount = FBDPCommon.valueFromFParameter('FMtMVariables', 'RefreshThresholdCount')
    if RefreshThresholdCount.isdigit():
        RefreshThresholdCount = int(RefreshThresholdCount)
    else:
        RefreshThresholdCount = 1000
        print('Default value (1000) is used. FParameter "RefreshThresholdCount" in module "FMtMVariables" should be an integer.')

    def __init__(self, world):

        FBDPWorld.WorldInterface.__init__(self, world)
        self.__count = 0
        self.__calcSpaceColl = self.__initCalcSpaceColl()
        self.__calcSpace = self.__initCalcSpace()

    def getCalcSpaceCalculateValue(self, acmIns, colName):

        self.__checkCalcSpaceUsage()
        val = self.__calcSpace.CalculateValue(acmIns, colName)
        self.__checkCalculatedValue(val)
        return val

    def getInsCalcMarketPriceParams(self, acmIns, fdict):

        self.__checkCalcSpaceUsage()
        val = acmIns.Calculation().MarketPriceParams(
                    self.__calcSpaceColl, fdict).Value()
        self.__checkCalculatedValue(val)
        return val

    def getInsCalcMarketPrice(self, acmIns, mtmIsoDate, useSpecificDate,
            acmCurr, useSpecificCurr):

        self.__checkCalcSpaceUsage()
        if acmIns.IsKindOf(acm.FCurrency):
            currPair = acmIns.CurrencyPair(acmCurr)

            if currPair is not None:
                date = currPair.SpotDate(mtmIsoDate)
            else:
                msg = 'Currency Pair {0}/{1} does not exist'.format(
                    acmIns.Name(), acmCurr.Name())
                self._logWarning(msg)
                msg = 'Using {0} calendar and spot days'.format(
                        acmIns.Name())
                self._logWarning(msg)
                spotCalendar = acmIns.Calendar()
                spotDays = acmIns.SpotBankingDaysOffset()
                date = spotCalendar.AdjustBankingDays(mtmIsoDate, spotDays)

            params = acm.FDictionary()
            params['fxDate'] = date
            params['toCurrency'] = acmCurr.Name()
            calc = acmIns.Calculation().FXRateParamsSource(
                self.__calcSpaceColl, params)
            val = calc.Value()
        else:
            val = acmIns.Calculation().MarketPrice(self.__calcSpaceColl,
                mtmIsoDate, useSpecificDate, acmCurr, useSpecificCurr)
        self.__checkCalculatedValue(val)
        return val

    def __initCalcSpaceColl(self):

        return acm.Calculations().CreateStandardCalculationsSpaceCollection()

    def __initCalcSpace(self):

        return acm.FCalculationSpace(self.SHEET_TYPE)

    def __checkCalcSpaceUsage(self):

        self.__count += 1
        if self.RefreshThresholdCount == 0:
            return
        elif self.__count % self.RefreshThresholdCount:
            return
        self.__calcSpaceColl.Clear()
        self.__calcSpace.Clear()
        acm.Calculations().ResetEvaluatorBuilders()
        self.__calcSpaceColl = self.__initCalcSpaceColl()
        self.__calcSpace = self.__initCalcSpace()
        acm.Memory().GcWorldStoppedCollect()

    def __checkCalculatedValue(self, value):

        if value.IsKindOf(acm.FException):
            self._logWarning(str(value))


# #############################################################################
# Portfolio Sheet Calculation Space Management
# #############################################################################


class PortfolioSheetCalcSpaceManagerNoWorld(object):
    RefreshThresholdCount = FBDPCommon.valueFromFParameter('FMtMVariables', 'RefreshThresholdCount')
    if RefreshThresholdCount.isdigit():
        RefreshThresholdCount = int(RefreshThresholdCount)
    else:
        RefreshThresholdCount = 1000
        print('Default value (1000) is used. FParameter "RefreshThresholdCount" in module "FMtMVariables" should be an integer.')

    def __init__(self, use_distributed_calculation):
        self.__count = 0
        self.__calcSpace = self.__initCalcSpace(
            use_distributed_calculation=use_distributed_calculation
        )

    def getCVAXML(self, creditBalanceIns):
        results = None
        try:
            results = self.getXMLs(
                creditBalanceInstrs=[creditBalanceIns],
                calcColumnNames=['CVA XML']
            )
        except Exception as e:
            errMsg = ('Error while obtaining "CVA XML" column for instrument '
                    '"{0}".  The instrument may not been setup properly.  '
                    '{1}'.format(creditBalanceIns.Name(),
                    ''.join(str(e).splitlines())))
            raise Exception(errMsg)

        results = results['CVA XML']
        assert len(results) == 1, 'Expected only a single CVA XML result'
        val = results[0][1]
        return val

    def getXMLs(self, creditBalanceInstrs, calcColumnNames):
        self.__checkCalcSpaceUsage()
        query = self.__createCreditBalanceQuery(creditBalanceInstrs)
        node = self.__calcSpace.InsertItem(query)
        self.__calcSpace.Refresh()  # Need to refresh before using node
        nodeIterator = node.Iterator()
        if not nodeIterator.HasChildren():
            names = ','.join((ins.Name() for ins in creditBalanceInstrs))
            raise Exception('Unable to obtain CVA XML of ' + names)

        it = nodeIterator.FirstChild()
        calculations = {}
        while it:
            tree = it.Tree()
            insName = tree.Item().StringKey()
            for name in calcColumnNames:
                calc = self.__calcSpace.CreateCalculation(tree, name)
                calculations.setdefault(name, []).append((insName, calc))

            it = it.NextSibling()

        self.__calcSpace.Refresh()
        for calcColumnName, results in calculations.items():
            for idx, res in enumerate(results):
                insName, calc = res
                results[idx] = (insName, calc.FormattedValue())

        return calculations

    def __initCalcSpace(self, use_distributed_calculation):
        spaceCollection = acm.Calculations().CreateCalculationSpaceCollection()
        calcSpace = spaceCollection.GetSpace(
            acm.FPortfolioSheet, acm.GetDefaultContext().Name(),
            None, use_distributed_calculation
        )
        return calcSpace

    def __createCreditBalanceQuery(self, creditBalanceInstrs):
        q = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        op = q.AddOpNode('OR')
        for ins in creditBalanceInstrs:
            assert ins.IsKindOf(acm.FCreditBalance), \
                'Expected credit balance instrument but got ' + ins.InsType()
            op.AddAttrNode('Instrument.Name', 'EQUAL', ins.Name())

        return q

    def __checkCalcSpaceUsage(self):
        self.__count += 1
        if self.RefreshThresholdCount == 0:
            return
        elif self.__count % self.RefreshThresholdCount:
            return

        self.__calcSpace.Clear()
        acm.Calculations().ResetEvaluatorBuilders()
        self.__calcSpace = self.__initCalcSpace()
        acm.Memory().GcWorldStoppedCollect()


class PortfolioSheetCalcSpaceManager(
    PortfolioSheetCalcSpaceManagerNoWorld, FBDPWorld.WorldInterface
):
    def __init__(self, world):
        PortfolioSheetCalcSpaceManagerNoWorld.__init__(self, False)
        FBDPWorld.WorldInterface.__init__(self, world)

    def __checkCalculatedValue(self, value):
        if value.IsKindOf(acm.FException):
            self._logWarning(str(value))
