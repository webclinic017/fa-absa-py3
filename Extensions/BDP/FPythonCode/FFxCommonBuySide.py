""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_position_rolls/etc/BuySide/FFxCommonBuySide.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
""" ---------------------------------------------------------------------------
MODULE
    FFxCommonBuySide

DESCRIPTION

----------------------------------------------------------------------------"""


import math


import acm


import FBDPString
import FBDPCommon


from FBDPValidation import FBDPValidate
import importlib


Summary = FBDPCommon.Summary
logme = FBDPString.logme

space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()


class ProfitAndLossDate():

    dateToday = 0
    currencyPairSpotdate = 1
    fxBaseDate = 2
    customPLValDate = 3


profitAndLossDate = ProfitAndLossDate()


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
    return max(map(lambda x: x.SpotDate(date), currObjects))


def getFxRate(date, curr1, curr2):

    #TODO: Should hot be needed. FXRate incorrect.
    if acm.Time().DateDifference(date, acm.Time().DateValueDay()) < 0:
        date = acm.Time().DateValueDay()
    return curr1.Calculation().FXRate(space, curr2, date).Value().Number()


def printEmp(msg, char):

    n = len(msg)
    logme(char * n)
    logme(msg)
    logme(char * n)


def addDicToDic(dic1, dic2):

    for k in dic1.keys():
        if k in dic2:
            dic2[k].extend(dic1[k])
        else:
            dic2[k] = dic1[k]


class DummyPort:

    def RecordType(self):

        return "Portfolio"


class TimeOrPorfolioSheet(FBDPValidate):

    def __init__(self):

        self.config = None
        self.portfolio = None
        self.calcSpace = None
        self.topNode = None
        self.grouping = []
        self.container = None
        FBDPValidate.__init__(self)

    def calcToNum(self, c):

        if not c:
            return 0
        try:
            val = c.Value()
            if val.IsKindOf(acm.FArray):
                val = map(lambda x: x.Number(), val)
                if len(val) == 1:
                    return val[0]
                return val
            if not val.IsKindOf(acm.FDenominatedValue):
                return 0
            return val.Number()
        except Exception, ex:
            logme(str(ex), 'ERROR')
            return None

    def getTrades(self, obj):

        if obj.IsKindOf(acm.FPortfolio):
            return obj.Trades()
        elif (obj.IsKindOf(acm.FStoredASQLQuery) and
                obj.SubType() == 'FTrade'):
            return obj.Query().Select()
        return []

    def createCalcSpace(self, tradingObjects, grouper=None,
            timeBucketGrouper=None):

        TimeOrPorfolioSheet.__init__(self)
        newGroupers = []
        if grouper and grouper.IsKindOf(acm.FChainedGrouper):
            for g in grouper.Groupers():
                self.grouping.append(str(g.Label()))
                newGroupers.append(g)
        if (timeBucketGrouper and
                timeBucketGrouper.IsKindOf(acm.FTimeBucketGrouper)):
            config = acm.Report().CreatePortfolioSheetGridConfiguration(
                    timeBucketGrouper.TimeBuckets())
            csc = acm.Calculations().CreateCalculationSpaceCollection()
            self.calcSpace = csc.GetSpace('FPortfolioSheet',
                    'Standard', config)
        else:
            self.calcSpace = acm.FCalculationSpace('FPortfolioSheet')
        self.container = self.createObjectUnion(tradingObjects)
        self.topNode = self.calcSpace.InsertItem(self.container)
        self.topNode.ApplyGrouper(acm.FChainedGrouper(newGroupers))
        self.calcSpace.Refresh()

    def createObjectUnion(self, objects):

        unionObject = acm.FCompoundPortfolio()
        unionObject.Name("Trade Union")
        accCurr = (acm.ObjectServer().UsedValuationParameters().
                AccountingCurrency())
        unionObject.Currency(accCurr)
        for obj in objects:
            fset = acm.FSet()
            fset.AddAll(unionObject.Trades().Union(self.getTrades(obj)))
            unionObject.Trades().Clear()
            unionObject.Trades().AddAll(fset)
        return unionObject

    def getPositionNodes(self, node=None, attrib_in={}):

        if not node:
            node = self.topNode
        positions = {}
        nodes = []
        it = node.Iterator().FirstChild()
        while it:
            tree = it.Tree()
            item = tree.Item()
            trades = item.Trades().AsList()
            portfolio = trades and trades[0].Portfolio() or item.Portfolio()
            grouper = item.Grouping().Grouper()
            try:
                method = str(grouper.Method())
            except AttributeError:
                method = str(grouper.Label())
            attrib_out = attrib_in.copy()
            if "Trade." in method:
                attrib_out[method.split("Trade.")[1]] = item.StringKey()
                if method.split("Trade.")[1] not in self.grouper_values:
                    self.grouper_values.append(method.split("Trade.")[1])
            if (tree.Depth() - 1 == len(self.grouping)):
                if not portfolio in positions:
                    positions[portfolio] = []
                positions[portfolio].append((tree, attrib_out))
            else:
                addDicToDic(self.getPositionNodes(tree, attrib_out), positions)
            it = it.NextSibling()
        return positions

    def printTree(self, node, colNames=["Portfolio Projected Payments"], max=0,
            start_depth=0, currencies=None):

        if logme.LogMode < 2:
            return
        if not start_depth:
            start_depth = node.Depth()
        if type(currencies) == type(acm.FCurrency()):
            currencies = [currencies]
        elif not currencies:
            currencies = [acm.ObjectServer().UsedValuationParameters().
                    AccountingCurrency()]
        values = []
        for name in colNames:
            self.setColumnConfig(currencies)
            val = self.getCalculation(node, name)
            values.append(val)
        for v in values:
            print v,
        print type(node), node.Depth(), node.Item().ClassName()
        if node.Iterator().HasChildren() and (not max or node.Depth() <= max):
            child = node.Iterator().FirstChild()
            while child:
                self.printTree(child.Tree(), colNames, max, start_depth,
                        currencies)
                child = child.NextSibling()

    def setColumnConfig(self, currencies):

        if type(currencies) == type(acm.FCurrency()):
            currencies = [currencies]
        Data = acm.FArray()
        if currencies:
            for curr in currencies:
                if curr and curr.Name():
                    DataBucket = acm.FNamedParameters()
                    DataBucket.AddParameter('currency', curr)
                    Data.Add(DataBucket)
        self.config = acm.Sheet().Column().ConfigurationFromVector(Data)

    def getColumnValue(self, node, colName, day=0):
        """
        Return the topnode value
        """
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

        cashes = map(lambda c: self.hasCashBalance(node, c), currencies)
        return reduce(lambda x, y: x or y, cashes)

    def getPL(self, node, day=0, pointsPL=True, curr=None, simulationDay=None):

        item = node.Item()
        self.setColumnConfig(None)
        column = "Portfolio Points Profit And Loss"
        if not pointsPL:
            if simulationDay:
                self.calcSpace.SimulateValue(item, "PL Valuation Date",
                        profitAndLossDate.customPLValDate)
                self.calcSpace.SimulateValue(item, "PL Valuation Date Custom",
                        simulationDay)
            column = "Portfolio Theoretical Total Profit and Loss"
        if curr:
            self.calcSpace.SimulateValue(item, "Portfolio Currency", curr)
        value = self.getColumnValue(node, column, day)
        #acm.StartApplication('ValuationViewer',value )
        self.calcSpace.RemoveSimulation(item, "Portfolio Currency")
        self.calcSpace.RemoveSimulation(item, "PL Valuation Date")
        self.calcSpace.RemoveSimulation(item, "PL Valuation Date Custom")
        self.calcSpace.Refresh()
        return value


class FxGroupingProcess(TimeOrPorfolioSheet):

    tradingObjects = None
    portfolioGrouper = None
    nextTradingDate = acm.Time.DateValueDay()

    def requirerdAttributesNotSet(self):
        msg = ""
        if not self.tradingObjects:
            msg = "tradingObjects must be set for a FxPortfolioProcess script."
        if not msg:
            msg = self.requirerdSubAttributesNotSet()
        if msg:
            logme("%s " % msg, 'ERROR')
        return msg

    def getTradingObjects(self, dic):
        objects = acm.FArray()
        for field in ['TradeQuery', 'TradeFilter', 'TradingPortfolios']:
            if field in dic and dic[field]:
                if field in ('TradeQuery'):
                    objects.AddAll([acm.FStoredASQLQuery[query] for query
                            in dic[field]])
                else:
                    objects.AddAll(dic[field])
        return objects

    def requirerdSubAttributesNotSet(self):

        return ''

    def performProcess(self, args):

        self.readArguments(args)
        if self.requirerdAttributesNotSet():
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
        if not self.tradingObjects:
            return
        logme('Process from day %s.' % (self.nextTradingDate))
        self.defineCalcSpace()
        self.grouper_values = []
        positions = self.getPositionNodes()
        # Perform process.
        aggregated_market_prf = {}
        size = len(positions.keys()) - 1
        counter = 0
        for portfolio, nodes in positions.iteritems():
            currencies = None
            pair = portfolio.CurrencyPair()
            if pair:
                currencies = [pair.Currency1(), pair.Currency2()]
            for n in nodes:
                self.printTree(n[0], currencies=currencies)
            self.processPortfolio(portfolio, nodes, aggregated_market_prf,
                    counter, size)
            counter += 1

    def defineCalcSpace(self):

        self.createCalcSpace(self.tradingObjects, self.portfolioGrouper)

    def createOrModifyGrouper(self, grouper):
        groupers = acm.FArray()
        portGrouperNeeded = True
        currencyPairGrouperNeeded = True
        if grouper and grouper.IsKindOf(acm.FChainedGrouper):
            for g in grouper.Groupers():
                groupers.Add(g)
                if str(g.Label()) == 'Trade Portfolio':
                    portGrouperNeeded = False
                if str(g.Label()) == 'Currency Pair':
                    currencyPairGrouperNeeded = False
        if portGrouperNeeded:
            portGrouper = acm.FAttributeGrouper("Trade.Portfolio")
            portGrouper.Label("Trade Portfolio")
            groupers.AtInsert(0, portGrouper)

        if currencyPairGrouperNeeded:
            currencyPairGrouper = acm.FAttributeGrouper("Trade.CurrencyPair")
            currencyPairGrouper.Label("Currency Pair")
            groupers.AtInsert(1, currencyPairGrouper)

        grouper = acm.FChainedGrouper(groupers)
        return grouper

    def getPortfoliosFromTradingObjects(self, objects):

        portfolios = acm.FSet()
        for obj in objects:
            for t in self.getTrades(obj):
                portfolios.Add(t.Portfolio())
        return portfolios.AsList()

    def readArguments(self, args):

        raise NotImplementedError("readArguments")

    def processPortfolio(self, portfolio, nodes, aggregated_market_prf,
            counter, size):

        raise NotImplementedError("processPortfolio")


class FxPortfolioProcess(FxGroupingProcess):

    defaultPortfolio = None
    mappedPortfolios = {}
    defaultAcquirer = None
    mappedAcquirers = {}
    isTimeSheet = True

    def requirerdAttributesNotSet(self):

        msg = FxGroupingProcess.requirerdAttributesNotSet(self)
        if msg:
            pass
        elif not self.defaultPortfolio:
            msg = "No default portfolio specified."
        elif not self.defaultAcquirer:
            msg = "No default acquirer specified."
        if not msg:
            msg = self.requirerdSubAttributesNotSet()
        if msg:
            logme("%s " % msg, 'ERROR')
        return msg

    def defineCalcSpace(self):

        portfolios = self.getPortfoliosFromTradingObjects(self.tradingObjects)
        currenyPairs = map(lambda x: x.CurrencyPair(), portfolios)
        currObjects = acm.FSet().AddAll(map(self.getCurrObjects, currenyPairs))
        currObjects = currObjects.AsList()
        if not currObjects.IsEmpty():
            currObjects = [c for c in currObjects[0]]
        today = acm.Time.DateValueDay()
        if self.nextTradingDate == today:
            endDate = maxOfSpotDates(currObjects, self.nextTradingDate)
            days = acm.Time.DateDifference(endDate, self.nextTradingDate)
            diff = acm.Time.DateDifference(self.nextTradingDate, today)
        else:
            endDate = self.nextTradingDate
            days = acm.Time.DateDifference(endDate, today)
            diff = 0
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

        #startDate = '0000-01-01', endDate = '9999-12-12'):
        today = acm.Time.DateValueDay()
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

    def getPortfolioAndAcquirer(self):

        return self.defaultPortfolio, self.defaultAcquirer

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

    def createMirrorTrade(self, trade, portfolio):
        """
        This method should no longer be used.  It was originally for creating
        mirror trades of FXSwaps, but the acm.MirrorPortfolio method now works
        for FXSwaps and should be used instead.
        """
        instrument = trade.Instrument()
        currency = trade.Currency()
        portfolio = portfolio
        acquirer = trade.Acquirer()
        counterparty = trade.Counterparty()
        broker = trade.Broker()
        strategy = trade.OptKey2()
        date = trade.ValueDay()
        price = trade.Price()
        quantity = -trade.Quantity()
        premium = -trade.Premium()
        typ = trade.Type()
        trade_process = trade.TradeProcess()
        mirrorTrade = self.createFxTrade(instrument, currency, portfolio,
                acquirer, counterparty, date, price, quantity, premium, typ,
                trade_process)
        mirrorTrade.GroupTrdnbr(trade)
        mirrorTrade.Broker(broker)
        mirrorTrade.OptKey2(strategy)
        return mirrorTrade

    def createFxTrade(self, instrument, currency, portfolio, acquirer,
            counterparty, date, price, quantity, premium, type, trade_process,
            status='BO Confirmed'):
        trade = acm.FTrade()
        trade.Instrument(instrument)
        trade.Currency(currency)
        # overridden from self.attributes if grouped on acq
        trade.Acquirer(acquirer)
        trade.Counterparty(counterparty)
        trade.Trader(acm.User())
        trade.Type(type)
        trade.Status(status)
        trade.Price(price)
        trade.ReferencePrice(price)
        rounding = self.getRounding(currency)
        trade.Quantity(self.roundPremiumForCurrency(quantity, rounding))
        trade.Premium(self.roundPremiumForCurrency(premium, rounding))
        tradeTime = acm.Time.DateNow()
        if acm.Time().DateDifference(tradeTime, date) > 0:
            tradeTime = date
        trade.TradeTime(tradeTime)
        trade.AcquireDay(date)
        trade.ValueDay(date)
        trade.TradeProcess(trade_process)
        trade.Portfolio(portfolio)
        return trade

    def getRounding(self, currency):
        if type(currency) != type(acm.FCurrency()):
            raise TypeError("Parameter 'currency' should be of type FCurrency")
        roundingSpec = currency.RoundingSpecification()
        if roundingSpec is None:
            return None
        roundings = acm.FRounding.Select("attribute='Premium'")
        rounding = next((r for r in roundings if
                r.RoundingSpec().Name() == roundingSpec.Name()), None)
        return rounding

    def roundPremiumForCurrency(self, premium, rounding):
        if not isinstance(premium, float) and not isinstance(premium, int):
            raise TypeError("Parameter 'premium' should be of type float or "
                    "int")
        premium = float(premium)
        if rounding is None:
            return premium
        if type(rounding) != type(acm.FRounding()):
            raise TypeError("Parameter 'rounding' should be of type FRounding "
                    "not of type " + str(type(rounding)))
        roundingFunction = acm.GetFunction('round', 3)
        return roundingFunction(premium, rounding.Decimals(), rounding.Type())

    def createGroupedFxTrade(self, instrument, currency, portfolio, acquirer,
            date, price, quantity, premium, type="Spot Roll",
            trade_process=4096):
        trade = self.createFxTrade(instrument, currency, portfolio, acquirer,
                self.defaultAcquirer, date, price, quantity, premium, type,
                trade_process)
        if self.attributes:
            for key, val in self.attributes.iteritems():
                trade.SetProperty(key, val)
        trade.Portfolio(portfolio)
        return trade

    def getCurrObjects(self, currencyPair):
        raise NotImplementedError("getCurrObjects")

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
