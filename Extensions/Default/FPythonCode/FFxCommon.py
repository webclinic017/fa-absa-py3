""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FFxCommon.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
""" ---------------------------------------------------------------------------
MODULE
    FFxCommon.

    Base class for FFxSpotRolloverMMFunding, FFxSpotRolloverSwapFunding
    and FPLSweep

DESCRIPTION


----------------------------------------------------------------------------"""


import math
from collections import namedtuple

import acm
import FBDPCommon
from FBDPValidation import FBDPValidate
from FBDPCurrentContext import Logme
import importlib

RESULT_FAIL = 0
RESULT_SUCCESS = 1
RESULT_IGNORED = 2
INVALID_NUMBERS = ['Infinity', '-Infinity', '1.#INF', '-1.#INF', '1.#IND',
                    '-1.#IND', 'NaN', '-NaN', '1.#QNAN', '-1.#QNAN']
CURRENCY = 'Curr'
CURRENCY_PAIR = 'CurrencyPair'
POSITION_PAIR = 'PositionPair'
POSITIONORCURRENCY_PAIR = 'PositionOrCurrencyPair'

SETTLE = 'Settle'

QuotedRate = namedtuple('QuotedRate', ['currencyPair', 'rate'])
PriceRate = namedtuple('PriceRate', 'currency1 currency2 price rate')

space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()


def currencyPair(curr1, curr2):
    currPair = acm.FCurrencyPair[curr1.Name() + "/" + curr2.Name()]
    if currPair:
        return currPair
    return acm.FCurrencyPair[curr2.Name() + "/" + curr1.Name()]


def currencyPairsAreConnected(pair1, pair2):
    return (pair1.Currency1() in (pair2.Currency1(), pair2.Currency2) or
        pair1.Currency2() in (pair2.Currency1(), pair2.Currency2))


def addBankingDays(curr, date, spot):
    cal = curr.Calendar()
    return cal.AdjustBankingDays(date, spot)


def maxOfSpotDates(currObjects, date):
    if not currObjects:
        return date
    return max([x.SpotDate(date) for x in currObjects])


def checkDenominatedValue(value):
    try:
        if not value:
            return False
        if value.Type() and value.Type().Text() == 'InvalidPrice':
            return False
        if str(value.Number()) in INVALID_NUMBERS:
            return False
        if not value.Number() >= 0.0 and not value.Number() < 0.0:
            return False
    except Exception:
        return False
    return True


def getBidAsk(cashflow):
    if cashflow < 0.0:
        bidAsk = 'Ask'
        counterBidAsk = 'Bid'
    else:
        bidAsk = 'Bid'
        counterBidAsk = 'Ask'
    return bidAsk, counterBidAsk


def getFxRate(date, curr1, curr2):
    if acm.Time().DateDifference(date, acm.Time().DateToday()) < 0:
        date = acm.Time().DateToday()
    val = curr1.Calculation().FXRate(space, curr2, date).Value()
    if checkDenominatedValue(val):
        rate = val.Number()
        msg = "FX rate for {0}:{1} on {2} is {3:.5f}".format(curr1.Name(),
                curr2.Name(), date, rate)
        Logme()(msg, 'DEBUG')
    else:
        rate = 0.
        msg = "Invalid FX rate found for {0}:{1} on {2}. Returning 0.".format(
                curr1.Name(), curr2.Name(), date)
        Logme()(msg, 'WARNING')
    return rate


def getTotalSwapPoints(currPair, fromDate, toDate, points):
    days = acm.Time().DateDifference(toDate, fromDate)
    pointValue = currPair.PointValue()
    totalPoints = points * pointValue * days
    Logme()('Total forward points for {0} day(s) from {1} to {2}: {3}'.format(
        days, fromDate, toDate, totalPoints), 'DEBUG')
    return totalPoints


def getLatestPointsPerDay(instr, curr, fromDate, bidAsk):
    calcValue = instr.Calculation().MarketPrice(space, fromDate,
            0, curr, 1, None, 0, 'Average' + bidAsk + 'Price', 1).Value()
    if not checkDenominatedValue(calcValue):
        message = ('Invalid swap points found for funding instrument {0} '
                    '({1}) on {2}'.format(instr.Name(), curr.Name(),
                        fromDate))
        Logme()(message, 'ERROR')
        return 0.0

    points = calcValue.Number()
    Logme()("Latest forward {0} points for {1} ({2}) on {3}: {4}.".format(
        bidAsk.lower(), instr.Name(), curr.Name(), fromDate, points,
        'DEBUG'))
    return points


def getLatestSwapPoints(currPair, fundInstr, fromDate, toDate, bidAsk):
    """
    Returns the latest forward FX points stored on the swap funding instrument
    passed in.
    """
    points = getLatestPointsPerDay(fundInstr, fundInstr.Currency(),
            fromDate, bidAsk)
    return getTotalSwapPoints(currPair, fromDate, toDate, points)


def getMtMSwapPoints(currPair, fundInstr, fromDate, toDate, mtmMarket,
        bidAsk=''):
    """
    Returns the marked-to-market forward FX points stored on the swap funding
    instrument passed in.
    """
    points = getMtMRate(fundInstr, fundInstr.Currency(), bidAsk,
            mtmMarket, fromDate)
    return getTotalSwapPoints(currPair, fromDate, toDate, points)


def getMtMFXRate(instr, curr, mtmMarket, date=acm.Time().DateToday()):
    """
    Returns the latest available mark-to-market settle FX rate, up to the
    specified date, for the instrument and currency requested.

    An inverse rate might be returned if that is how MtM rates are stored.

    A cross rate inferred from the instrument, currency and the FX base
    currency in the valuation parameters may also be returned in rates are not
    quoted directly for the instrument and currency.
    """
    rate = getMtMRate(instr, curr, SETTLE, mtmMarket, date)
    if rate != 0.0:
        return rate

    baseCurr = acm.ObjectServer().UsedValuationParameters().FxBaseCurrency()
    message = ("No MtM rates found for {0}:{1} or {1}:{0} on {2} in MtM "
            "market {3}. Getting cross rate from base currency {4}...".format(
                instr.Name(), curr.Name(), date, mtmMarket.Name(),
                baseCurr.Name()))
    Logme()(message, "INFO")
    crossRate = getCrossRate(instr, curr, baseCurr, mtmMarket, date)
    return crossRate


def getCrossRate(instr, curr, baseCurr, mtmMarket, date):
    rateQuotes = []
    for lookup in (instr, curr):
        p_rate = getLatestMtMPriceRate(lookup, baseCurr, SETTLE, mtmMarket,
                date)
        rate = p_rate.rate
        if rate != 0.:
            currPair = '{0}:{1}'.format(p_rate.currency1.Name(),
                    p_rate.currency2.Name())
            rateQuotes.append(QuotedRate(currPair, rate))
        else:
            message = ('Could not get cross rate for {0}:{1} on {2} from '
                'base currency {3} - no rate available for '
                '{0}:{3}'.format(instr.Name(), curr.Name(), date,
                    baseCurr.Name()))
            Logme()(message, "DEBUG")
            return 0.

    assert len(rateQuotes) == 2, "Need 2 rates to cross - found {0}".format(
            len(rateQuotes))

    crossRate = rateQuotes[0].rate / rateQuotes[1].rate
    message = ("{0}:{1} rate for {2} implied by MtM rates for {3} and {4}: "
            "{5:.6f}".format(instr.Name(), curr.Name(), date,
                rateQuotes[0].currencyPair, rateQuotes[1].currencyPair,
                crossRate))
    Logme()(message, "DEBUG")
    return crossRate

def getMtMRate(instr, curr, valueType, mtmMarket, date, checkInverse=True):
    p_rate = getLatestMtMPriceRate(instr, curr, valueType, mtmMarket, date,
            checkInverse)
    return p_rate.rate

def getLatestMtMPriceRate(instr, curr, valueType, mtmMarket, date,
        checkInverse=True):
    p_rate = getMtMPriceRate(instr, curr, valueType, mtmMarket, date)
    if checkInverse:
        inv_p_rate = getMtMPriceRate(curr, instr, valueType, mtmMarket, date)
        invert = False
        if p_rate:
            invert = inv_p_rate and \
                     (inv_p_rate.price.Day() > p_rate.price.Day())
        elif inv_p_rate:
            invert = True
        else:
            p_rate = None

        if invert:
            message = ('Using the more recent historical price for {0}:{1} '
                    ' instead of {1}:{0}.'.format(inv_p_rate.currency1.Name(),
                    inv_p_rate.currency2.Name()))
            Logme()(message, 'DEBUG')
            p_rate = PriceRate(inv_p_rate.currency1, inv_p_rate.currency2,
                    inv_p_rate.price, 1.0 / inv_p_rate.rate)

    if not p_rate:
        p_rate = PriceRate(instr, curr, None, 0.0)

    return p_rate

def getMtMPriceRate(instr, curr, valueType, mtmMarket, date):
    histPrices = instr.HistoricalPrices()
    if not histPrices:
        message = ("No mark-to-market rates available for {0} ({1}).".format(
                instr.Name(), curr.Name()))
        Logme()(message, "WARNING")
        return None

    last = None
    for hp in histPrices:
        if hp.Market() == mtmMarket and hp.Currency() == curr:
            if hp.Day() == date:
                last = hp
                break

            # Find latest available before MtM date
            if hp.Day() < date:
                if not last:
                    last = hp
                elif hp.Day() > last.Day():
                    last = hp

    if not last:
        message = ("No mark-to-market rates available for {2} ({1}) in "
                "MtM market '{0}' before {3}.".format(mtmMarket.Name(),
                curr.Name(), instr.Name(), date))
        Logme()(message, "WARNING")
        return None

    if last.Day() != date:
        assert last.Day() < date, ("Found historical price on "
                "{0} after MtM date {1}".format(last.Day(), date))
        message = ("No mark-to-market rate available for {0} ({1}) in "
                "MtM market '{2}' on {3}. Using latest available on "
                "{4}.".format(instr.Name(), curr.Name(), mtmMarket.Name(),
                date, last.Day()))
        Logme()(message, "WARNING")

    if valueType == 'Bid':
        rate = last.Bid()
    elif valueType == 'Ask':
        rate = last.Ask()
    elif valueType == 'High':
        rate = last.High()
    elif valueType == 'Low':
        rate = last.Low()
    elif valueType == 'Last':
        rate = last.Last()
    else:
        rate = last.Settle()

    if math.isnan(rate):
        message = ("Invalid mark-to-market {3} rate found for {0} ({1}) on "
                "{2}.".format(instr.Name(), curr.Name(), last.Day(),
                    valueType.lower()))
        Logme()(message, 'ERROR')
        return None

    Logme()("MtM {0} rate for {1} ({2}) {3}: {4}.".format(valueType.lower(),
        instr.Name(), curr.Name(), date, rate, 'DEBUG'))
    return PriceRate(instr, curr, last, rate)


def printEmp(msg, char, mode='INFO'):
    n = len(msg)
    Logme()(char * n, mode)
    Logme()(msg, mode)
    Logme()(char * n, mode)


def addDicToDic(dic1, dic2):
    for k in dic1.keys():
        if k in dic2:
            dic2[k].extend(dic1[k])
        else:
            dic2[k] = dic1[k]


def callGrouperHook(grouperName):
    try:
        import FBDPHook
        importlib.reload(FBDPHook)
    except ImportError:
        return None
    try:
        func = getattr(FBDPHook, "get_grouping_attribute_from_grouper")
    except:
        return None
    else:
        return func(grouperName)


def calcToNum(c):
    if not c:
        return 0
    try:
        val = c.Value()
        if val.IsKindOf(acm.FArray):
            val = [x.Number() for x in val]
            if len(val) == 1:
                return val[0]
            return val
        if not val.IsKindOf(acm.FDenominatedValue):
            return 0
        return val.Number()
    except Exception as ex:
        Logme()(str(ex), 'ERROR')
        return None


def setColumnConfig(currencies):
    if type(currencies) == type(acm.FCurrency()):
        currencies = [currencies]
    Data = acm.FArray()
    if currencies:
        for curr in currencies:
            if curr and curr.Name():
                DataBucket = acm.FNamedParameters()
                DataBucket.AddParameter('currency', curr)
                Data.Add(DataBucket)
    return acm.Sheet().Column().ConfigurationFromVector(Data)


class TimeOrPorfolioSheet(FBDPValidate):

    def __init__(self):

        FBDPValidate.__init__(self)

        self.config = None
        self.portfolio = None
        self.calcSpace = None
        self.topNode = None
        self.grouping = []
        self.container = None
        self.optKeys = {}

    def __initData(self):
        self.config = None
        self.calcSpace = None
        self.topNode = None
        self.grouping = []
        self.container = None
        self.optKeys = {}

    def calcToNum(self, c):
        return calcToNum(c)

    def getTrades(self, obj):
        if obj.IsKindOf(acm.FPortfolio):
            return obj.Trades()
        elif obj.IsKindOf(acm.FStoredASQLQuery) and \
            obj.SubType() == 'FTrade':
            return obj.Query().Select()
        return []

    def createCalcSpace(self, tradingObjects, grouper=None,
            timeBucketGrouper=None):

        TimeOrPorfolioSheet.__initData(self)

        newGroupers = []
        if grouper and grouper.IsKindOf(acm.FChainedGrouper):
            for g in grouper.Groupers():
                self.grouping.append(self.extractNodeGrouperMethod(g))
                newGroupers.append(g)

        if (timeBucketGrouper and
                timeBucketGrouper.IsKindOf(acm.FTimeBucketGrouper)):
            config = acm.Report().CreatePortfolioSheetGridConfiguration(
                    timeBucketGrouper.TimeBuckets())
            csc = acm.Calculations().CreateCalculationSpaceCollection()
            self.calcSpace = csc.GetSpace('FPortfolioSheet', 'Standard',
                    config)
        else:
            self.calcSpace = acm.FCalculationSpace('FPortfolioSheet')

        self.container = self.createObjectUnion(tradingObjects)
        accCurr = acm.ObjectServer().UsedValuationParameters(
            ).AccountingCurrency()
        self.calcSpace.SimulateValue(
            self.container, 'Portfolio Currency', accCurr)
        self.topNode = self.calcSpace.InsertItem(self.container)

        self.topNode.ApplyGrouper(acm.FChainedGrouper(newGroupers))
        self.calcSpace.Refresh()

    def createObjectUnion(self, objects):
        unionObject = acm.FAdhocPortfolio()
        unionObject.Name("Trade Union")
        settmp = acm.FIdentitySet()
        for obj in objects:
            settmp.AddAll(self.getTrades(obj))
        for t in settmp.AsIndexedCollection():
            unionObject.Add(t)
        return unionObject

    def extractNodeGrouperMethod(self, grouper):
        method = None
        if grouper.IsKindOf(acm.FAttributeGrouper):
            if str(grouper.Method()) == 'Instrument.Currency':
                method = 'Instrument.Currency'
            else:
                label = grouper.Label()
                method = str(label) if label else str(grouper.Method())
        else:
            method = str(grouper.Label())

        attr = callGrouperHook(method)
        if attr:
            method = attr

        if "Trade " in method:
            method = method.split("Trade ")[1]
        elif "Trade.OptKey" in method:
            return method
        elif method.startswith('Trade.'):
            method = method.split(".")[1]
        elif method == "Currency Pair":
            method = CURRENCY_PAIR

        return method

    def buildOptKeysBasedOldMapping(self):
        tradekeys = acm.FChoiceList.Select("list='Trade Keys'")
        i = 1
        for key in tradekeys:
            optKeyName = "OptKey%s" % i
            self.optKeys[optKeyName] = key.Name()
            i = i + 1

    def buildOptKeysDictionary(self):
        self.optKeys.clear()
        trdkeys = acm.FChoiceList.Select("list = 'ADM Choicelist Mappings'")
        if not trdkeys:
            self.buildOptKeysBasedOldMapping()
            return

        i = 1
        for k in trdkeys:
            kName = "Trade.optkey%s_chlnbr" % i
            if kName.upper() in k.Name().upper():
                optKeyName = "OptKey%s" % i
                self.optKeys[optKeyName] = k.Description()
                i = i + 1

    def getOptKeyObject(self, key, val):
        return acm.FChoiceList.Select("list='%s' AND name=%s" %
                (self.optKeys[key], val))[0]

    def extractNodeAttribute(self, grouper, item, attrib_out):
        method = self.extractNodeGrouperMethod(grouper)

        if "Trade.OptKey" in method:
            self.buildOptKeysDictionary()
            try:
                attribName = method.split(".")[1]
                attrib_out[attribName] = self.getOptKeyObject(
                        attribName, item.Value()).Name()
            except:
                pass
        else:
            attrib_out[method] = item.StringKey()

    def getPositionNodes(self, node=None, attrib_in={}):
        if not node:
            node = self.topNode
        positions = {}
        it = node.Iterator().FirstChild()
        while it:
            tree = it.Tree()
            item = tree.Item()
            trades = item.Trades().AsList()
            if trades.Size() > 0:
                portfolio = (trades and trades[0].Portfolio() or
                        item.Portfolio())
                grouper = item.Grouping().Grouper()
                attrib_out = attrib_in.copy()
                self.extractNodeAttribute(grouper, item, attrib_out)
                if (tree.Depth() - 1 == len(self.grouping)):
                    if portfolio not in positions:
                        positions[portfolio] = []
                    positions[portfolio].append((tree, attrib_out))
                else:
                    addDicToDic(self.getPositionNodes(tree, attrib_out),
                            positions)
            it = it.NextSibling()
        return positions

    def printTree(self, node, colNames=["Portfolio Projected Payments"],
            max_depth=0, start_depth=0, currencies=None):
        if Logme().LogMode < 2:
            return
        if not start_depth:
            start_depth = node.Depth()
        if type(currencies) == type(acm.FCurrency()):
            currencies = [currencies]
        elif not currencies:
            currencies = [acm.ObjectServer().UsedValuationParameters(
                    ).AccountingCurrency()]

        values = []
        for name in colNames:
            self.setColumnConfig(currencies)
            val = self.getCalculation(node, name)
            values.append(val)

        Logme()("%s (Node Level %s) %s => %s : %s " %
                (" " * (node.Depth() - start_depth) * 5, node.Depth(),
                node.Item().StringKey(), str(colNames), str(values)), "DEBUG")

        if (node.Iterator().HasChildren() and
                (not max_depth or node.Depth() <= max_depth)):
            child = node.Iterator().FirstChild()
            while child:
                self.printTree(child.Tree(), colNames, max_depth, start_depth,
                        currencies)
                child = child.NextSibling()

    def setColumnConfig(self, currencies):
        self.config = setColumnConfig(currencies)

    def getColumnValue(self, node, colName, day=0):

        # Return the topnode value
        if not day:
            return self.getCalculation(node, colName)

        # Return the correct bucket value
        treeIterator = node.Iterator()

        res = treeIterator.Find(day)
        if res:
            node = res.Tree()
            return self.getCalculation(node, colName)
        return None

    def getCalculation(self, node, colName):

        val = self.calcSpace.CreateCalculation(node, colName, self.config)
        val = self.calcToNum(val.Value())
        return val

    def getCashflow(self, node, day=0, configCurr=None):

        self.setColumnConfig(configCurr)
        val = self.getColumnValue(node, "Portfolio Projected Payments", day)
        return val

    def hasCashBalance(self, node, curr):

        self.setColumnConfig(curr)
        val = self.getColumnValue(node, "Portfolio Projected Payments", 0)
        cash = val
        if cash and math.fabs(cash) > 0.0001:
            return True
        return False

    def hasCashBalances(self, node, currencies):

        cashes = [self.hasCashBalance(node, c) for c in currencies]
        return reduce(lambda x, y: x or y, cashes)


class FxGroupingProcess(TimeOrPorfolioSheet):

    def __init__(self):

        TimeOrPorfolioSheet.__init__(self)

        self.tradingObjects = None
        self.portfolioGrouper = None
        self.nextTradingDate = None
        self.refreshCalcSpace = None
        self.attributes = None

    def requiredAttributesNotSet(self):

        msg = ""
        if not self.tradingObjects:
            msg = ("At least one of the fields in 'Stored Folder', "
                    "'Trade Filter' and 'Portfolio' needs to be set.")
        if not msg:
            msg = self.requiredSubAttributesNotSet()
        if msg:
            Logme()("%s " % msg, 'ERROR')
        return msg

    def getTradingObjects(self, dictionary):

        objects = acm.FArray()
        for field in ['TradeQuery', 'TradeFilter', 'TradingPortfolios']:
            if field in dictionary and dictionary[field]:
                objects.AddAll(dictionary[field])
        return objects

    def requiredSubAttributesNotSet(self):

        return ''

    def cleanAndRecreateCalcSpace(self):

        self.calcSpace.Clear()
        acm.PollDbEvents()
        acm.Calculations().ResetEvaluatorBuilders()
        acm.Memory().GcWorldStoppedCollect()
        self.defineCalcSpace()

    def performCalculation(self):

        self.refreshCalcSpace = False
        positions = self.getPositionNodes()
        for portfolio, nodes in positions.iteritems():
            self.processPortfolio(portfolio, nodes)

    def performProcess(self, args):

        self.readArguments(args)

        if self.requiredAttributesNotSet():
            return

        if type(self.portfolioGrouper) == type([]):
            self.portfolioGrouper = self.portfolioGrouper[0]

        if type(self.portfolioGrouper) == type(""):
            self.portfolioGrouper = acm.FChainedGrouper[self.portfolioGrouper]

        if self.portfolioGrouper:
            if self.portfolioGrouper.IsKindOf(acm.FStoredPortfolioGrouper):
                self.portfolioGrouper = self.portfolioGrouper.Grouper()
            elif not self.portfolioGrouper.IsKindOf(acm.FChainedGrouper):
                self.portfolioGrouper = None

        self.portfolioGrouper = self.createOrModifyGrouper(
                self.portfolioGrouper)

        if self.nextTradingDate:
            Logme()('Process from day %s.' % (self.nextTradingDate))
        self.defineCalcSpace()
        self.performCalculation()

    def defineCalcSpace(self):

        self.createCalcSpace(self.tradingObjects, self.portfolioGrouper)

    def createOrModifyGrouper(self, grouper):

        groupers = acm.FArray()
        portGrouperNeeded = True
        if grouper and grouper.IsKindOf(acm.FChainedGrouper):
            for g in grouper.Groupers():
                groupers.Add(g)
                if str(g.Label()) == 'Trade Portfolio':
                    portGrouperNeeded = False

        if portGrouperNeeded:
            portGrouper = acm.FAttributeGrouper("Trade.Portfolio")
            portGrouper.Label("Trade Portfolio")
            groupers.AtInsert(0, portGrouper)
        grouper = acm.FChainedGrouper(groupers)
        return grouper

    def getPortfoliosFromTradingObjects(self, objects):

        settmp = acm.FSet()
        for obj in objects:
            for t in self.getTrades(obj):
                settmp.Add(t.Portfolio())
        return settmp.AsList()

    def readArguments(self, args):
        self.tradingObjects = self.getTradingObjects(args)
        self.portfolioGrouper = ('PortfolioGrouper' in args and
                args['PortfolioGrouper'])

    def processPortfolio(self, portfolio, nodes):
        raise NotImplementedError("processPortfolio")

    def callAdjustTradeHook(self, trade, scriptName):
        try:
            import FBDPHook
            importlib.reload(FBDPHook)
        except ImportError:
            return
        try:
            FBDPHook.adjust_fx_ftrade(trade, scriptName)
        except:
            return

    def instrumentAtNode(self, node):
        t = self.tradeAtNode(node)
        if t:
            return t.Instrument()
        return None

    def tradeAtNode(self, node):
        nodeTrades = node.Item().Trades().AsIndexedCollection()
        if nodeTrades and nodeTrades.Size():
            return nodeTrades[0]
        return None

    def setTradePropertiesFromGrouper(self, trade, excludedAttributes=()):
        if self.attributes:
            for key, val in self.attributes.iteritems():
                if key == CURRENCY_PAIR:
                    continue
                if key not in excludedAttributes:
                    try:
                        if 'OptKey' in key:
                            val = self.getOptKeyObject(key, val)
                        if 'PositionOrCurrencyPair' in key:
                            key = 'PositionPair'
                        if 'AdditionalInfo' in key:
                            continue
                        trade.SetProperty(key, val)
                    except Exception as e:
                        msg = "Ignored setting {0} on trade as {1}".format(
                                key, str(e))
                        Logme()(msg, "DEBUG")


class FxPortfolioProcess(FxGroupingProcess):
    def __init__(self):
        FxGroupingProcess.__init__(self)

        self.defaultPortfolio = None
        self.defaultAcquirer = None
        self.mappedPortfolios = None
        self.mappedAcquirers = None
        self.mappedFundingInstruments = None
        self.mappedPositionPairs = None

    def readArguments(self, args):
        FxGroupingProcess.readArguments(self, args)
        self.defaultPortfolio = args['DefaultPortfolio'][0]
        if args['DefaultAcquirer']:
            self.defaultAcquirer = args['DefaultAcquirer'][0]
        else:
            self.defaultAcquirer = None
        if (self.defaultAcquirer and
             not self.defaultAcquirer.IsKindOf(acm.FInternalDepartment)):
            message = ('Default Acquirer \'%s\' is '
                    'not an Internal Department' %
                    self.defaultAcquirer.Name())
            Logme()(message, 'ERROR')
            raise Exception(message)

        self.mappedPortfolios = (args['MappedPortfolios'] if
                'MappedPortfolios' in args else {})
        self.mappedPositionPairs = (args['MappedPositionPairs'] if
                'MappedPositionPairs' in args else {})
        self.mappedAcquirers = (args['MappedAcquirers'] if
                'MappedAcquirers' in args else {})
        if self.mappedAcquirers:
            for k in self.mappedAcquirers:
                mappedAcquirer = acm.FParty[self.mappedAcquirers[k]]
                if not mappedAcquirer.IsKindOf(acm.FInternalDepartment):
                    message = ('Mapped Acquirer \'%s\' '
                    'is not an Internal Department' % mappedAcquirer.Name())
                    Logme()(message, 'ERROR')
                    raise Exception(message)

    def requiredAttributesNotSet(self):
        msg = FxGroupingProcess.requiredAttributesNotSet(self)
        if msg:
            pass
        elif not self.defaultPortfolio:
            msg = "No default portfolio specified."

        if not msg:
            msg = self.requiredSubAttributesNotSet()
        if msg:
            Logme()("%s " % msg, 'ERROR')
        return msg

    def defineCalcSpace(self):
        portfolios = self.getPortfoliosFromTradingObjects(self.tradingObjects)
        currenyPairs = [x.CurrencyPair() for x in portfolios]
        currObjects = acm.FSet().AddAll(
                [self.getCurrObjects(currPair) for currPair in currenyPairs])
        currObjects = currObjects.AsList()
        if not currObjects.IsEmpty():
            currObjects = [c for c in currObjects[0]]

        endDate = maxOfSpotDates(currObjects, self.nextTradingDate)
        today = acm.Time.DateToday()
        days = acm.Time.DateDifference(endDate, self.nextTradingDate)
        diff = acm.Time.DateDifference(self.nextTradingDate, today)

        bucketDefinitions = acm.FArray()
        bucketDefinitions.Add(self.createDefinition(diff))

        for n in range(1, days + 1):
            defi = self.createDefinition(n + diff)
            bucketDefinitions.Add(defi)
        bucketDefinitions.Add(acm.FRestTimeBucketDefinition())
        bucks = acm.Time().CreateTimeBucketsFromDefinitions(0,
                bucketDefinitions, None, 0, 0, 0, 0, 0, 0)

        self.createCalcSpace(self.tradingObjects, self.portfolioGrouper,
                acm.FTimeBucketGrouper(bucks))

    def createDefinition(self, n):
        # startDate = '0000-01-01', endDate = '9999-12-12'):
        today = acm.Time.DateToday()
        definition = acm.FDatePeriodTimeBucketDefinition()
        name = '%sd' % n
        definition.DatePeriod(name)
        definition.Name(acm.Time.DateAddDelta(today, 0, 0, n))
        definition.Adjust(False)
        definition.RelativeSpot(False)
        return definition

    def getDefaultPortfolio(self):
        return self.defaultPortfolio

    def getDefaultAcquirer(self):
        return self.defaultAcquirer

    def getDefaultPortfolioAndAcquirer(self):
        return self.defaultPortfolio, self.defaultAcquirer

    def getPortfolioAndAcquirer(self, currObject):
        mappedPortfolio, mappedAcquirer = self.getMappedPortfolioAndAcquirer(
                currObject)

        if not currObject:
            Logme()("Transactions within currency, using default portfolio "
                    "and acquirer.", "DEBUG")

        if not mappedPortfolio:
            mappedPortfolio = self.defaultPortfolio
            message = 'Using default portfolio.'
            Logme()(message, 'INFO')

        if not mappedAcquirer:
            mappedAcquirer = self.defaultAcquirer
            if 'Acquirer' not in self.attributes:
                message = 'Using default acquirer.'
                Logme()(message, 'INFO')

        return mappedPortfolio, mappedAcquirer

    def getMappedPortfolioAndAcquirer(self, currObject):
        mappedPortfolio = None
        mappedAcquirer = None

        if not currObject:
            return mappedPortfolio, mappedAcquirer

        if currObject.Name() in self.mappedPortfolios:
            mappedPortfolio = acm.FPhysicalPortfolio[self.mappedPortfolios[
                    currObject.Name()]]
        if not mappedPortfolio:
            message = ('No mapped portfolio specified for %s.' %
                    (currObject.Name()))
            Logme()(message, 'INFO')
        elif mappedPortfolio.Compound():
            message = ('Compound portfolio as mapped Portfolio %s .' %
                    (mappedPortfolio.Name()))
            Logme()(message, 'ERROR')
            raise Exception(message)
        else:
            Logme()("Using mapped portfolio: %s" % mappedPortfolio.Name(),
                    "DEBUG")

        if currObject.Name() in self.mappedAcquirers:
            mappedAcquirer = acm.FParty[self.mappedAcquirers[
                    currObject.Name()]]
        if not mappedAcquirer:
            message = ('No mapped acquirer specified for %s.' % (
                    currObject.Name()))
            Logme()(message, 'INFO')
        else:
            # Exception if not Int dEp or CounterParty
            Logme()("Using mapped acquirer: %s" % mappedAcquirer.Name(),
                    "DEBUG")
        return mappedPortfolio, mappedAcquirer

    def getSplittingCurr(self, rollCurr, counterCurr, fundCurr1, fundCurr2):
        if fundCurr1 == rollCurr:
            if fundCurr2 != counterCurr:
                return fundCurr2
        if fundCurr1 == counterCurr:
            if fundCurr2 != rollCurr:
                return fundCurr2
        if fundCurr2 == rollCurr:
            if fundCurr1 != counterCurr:
                return fundCurr1
        if fundCurr2 == counterCurr:
            if fundCurr1 != rollCurr:
                return fundCurr1
        return None

    def getSplittingCurrency(self, rollCurr, counterCurr, fundPort):
        fundPortCurrencyPair = fundPort.CurrencyPair()
        if fundPortCurrencyPair:
            fundCurr1 = fundPortCurrencyPair.Currency1()
            fundCurr2 = fundPortCurrencyPair.Currency2()
            return self.getSplittingCurr(rollCurr, counterCurr, fundCurr1,
                                         fundCurr2)
        mappedPositionPairList = None
        if fundPort.Name() in self.mappedPositionPairs:
            mappedPositionPairList = \
                self.mappedPositionPairs[fundPort.Name()]
        if not mappedPositionPairList:
            return None

        for p in mappedPositionPairList:
            currPair = acm.FCurrencyPair[p]
            fundCurr1 = currPair.Currency1()
            fundCurr2 = currPair.Currency2()
            splitCurr = self.getSplittingCurr(rollCurr, counterCurr,
                   fundCurr1, fundCurr2)
            if splitCurr:
                return splitCurr
        return None

    def getMappedFundingInstrument(self, currObject):
        mappedFundingInstrument = None
        if not currObject:
            return mappedFundingInstrument

        if currObject.Name() in self.mappedFundingInstruments:
            mappedFundingInstrument = acm.FInstrument[
                    self.mappedFundingInstruments[currObject.Name()]]

        return mappedFundingInstrument

    def getCounterCurrencyOfCurrPair(self, currPair):
        accountingCurr = acm.ObjectServer().UsedValuationParameters(
                ).AccountingCurrency()
        if (accountingCurr == currPair.Currency1() or
            accountingCurr == currPair.Currency2()):
            return accountingCurr
        else:
            cc = currPair.SweepCurrency()
            if (not cc or
                (cc != currPair.Currency1() and cc != currPair.Currency2())):
                if cc:
                    Logme()('CurrencyPairs SweepCurrency is not equal to '
                            'Currency1 or Currency2', 'WARNING')
                cc = currPair.Currency2()
            return cc

    def createFxTrade(self, instrument, currency, portfolio, acquirer,
            counterparty, date, price, quantity, premium, tradetype,
            trade_process):

        trade = acm.FTrade()
        trade.Instrument(instrument)
        trade.Currency(currency)
        # overridden from self.attributes if grouped on acq
        trade.Acquirer(acquirer)
        trade.Counterparty(counterparty)
        trade.Trader(acm.User())
        trade.Type(tradetype)
        trade.Status('Internal')
        trade.Price(price)
        trade.ReferencePrice(price)
        roundingForInstrument = FBDPCommon.getPremiumRounding(instrument)
        trade.Quantity(self.roundValueForInstrument(quantity,
                roundingForInstrument))
        roundingForCurrency = FBDPCommon.getPremiumRounding(currency)
        trade.Premium(self.roundValueForInstrument(premium,
                roundingForCurrency))
        tradeTime = acm.Time.DateNow()
        if acm.Time().DateDifference(tradeTime, date) > 0:
            tradeTime = date
        trade.TradeTime(tradeTime)
        trade.AcquireDay(date)
        trade.ValueDay(date)
        trade.TradeProcess(trade_process)
        trade.Portfolio(portfolio)
        return trade

    def getPremiumRounding(self, instrument):

        if instrument is None:
            raise TypeError("Parameter 'instrument' must not be null")
        roundingSpec = instrument.RoundingSpecification()
        if roundingSpec is None:
            return None
        roundings = acm.FRounding.Select("attribute='Premium'")
        rounding = next((r for r in roundings if
                r.RoundingSpec().Name() == roundingSpec.Name()), None)
        return rounding

    def getPnLRounding(self, instrument):

        if instrument is None:
            raise TypeError("Parameter 'instrument' must not be null")
        roundingSpec = instrument.RoundingSpecification()
        if roundingSpec is None:
            return None
        roundings = acm.FRounding.Select("attribute='Profit And Loss'")
        rounding = next((r for r in roundings if
                r.RoundingSpec().Name() == roundingSpec.Name()), None)
        return rounding

    def roundValueForInstrument(self, value, rounding):

        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("Parameter 'value' should be of type float or int")
        value = float(value)
        if rounding is None:
            return value
        if type(rounding) != type(acm.FRounding()):
            raise TypeError("Parameter 'rounding' should be of type FRounding "
                    "not of type " + str(type(rounding)))
        roundingFunction = acm.GetFunction('round', 3)
        return roundingFunction(value, rounding.Decimals(), rounding.Type())

    def createGroupedFxTrade(self, instrument, currency, portfolio, acquirer,
            date, price, quantity, premium, tradetype="Spot Roll",
            trade_process=4096):

        trade = self.createFxTrade(instrument, currency, portfolio, acquirer,
                self.defaultAcquirer, date, price, quantity, premium,
                tradetype, trade_process)
        self.setTradePropertiesFromGrouper(trade)
        trade.Portfolio(portfolio)
        return trade

    def getCurrObjects(self, currPair):
        raise NotImplementedError("getCurrObjects")
