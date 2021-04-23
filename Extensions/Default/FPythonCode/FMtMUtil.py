""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FMtMUtil.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FMtMUtil - Module which provide utilities to the Mark-to-Market script.

DESCRIPTION
    This module contains the utility function and classes for the script
    FMarkToMarket.
----------------------------------------------------------------------------"""


import collections
import copy


import ael
import acm


import ArenaFunctionBridge
import FBDPCommon
import FBDPWorld
import FBDPYieldCurveLib


PRICE_BITMASK = {
    'bid': 1,  # 2^0
    'ask': 2,  # 2^1
    'last': 16,  # 2^4
    'settle': 256,  # 2^8
    'high': 32,  # 2^5
    'low': 64  # 2^6
    }


# #############################################################################
# Common tools.
# #############################################################################


def uniquifyListByOid(objList):
    """
    Given a list of object, return another non-repeating object list of the
    same sequence.  The later occurrences of objects previously appeared and
    of the same oid are excluded from the returned list.
    """
    uniqueObjList = []
    oidSet = set()
    for obj in objList:
        oid = obj.Oid()
        if oid not in oidSet:
            oidSet.add(oid)
            uniqueObjList.append(obj)
    return uniqueObjList


def hasBidValue(price):
    return (price.Bits() & PRICE_BITMASK['bid'])


def hasAskValue(price):
    return (price.Bits() & PRICE_BITMASK['ask'])


def hasHighValue(price):
    return (price.Bits() & PRICE_BITMASK['high'])


def hasLowValue(price):
    return (price.Bits() & PRICE_BITMASK['low'])


def hasLastValue(price):
    return (price.Bits() & PRICE_BITMASK['last'])


def hasSettleValue(price):
    return (price.Bits() & PRICE_BITMASK['settle'])


def getBidValue(price):
    if hasBidValue(price):
        return price.Bid()
    return 0.0


def getAskValue(price):
    if hasAskValue(price):
        return price.Ask()
    return 0.0


def getHighValue(price):
    if hasHighValue(price):
        return price.High()
    return 0.0


def getLowValue(price):
    if hasLowValue(price):
        return price.Low()
    return 0.0

def getLastValue(price):
    if hasLastValue(price):
        return price.Last()
    return 0.0

# #############################################################################
# Price batch transaction.
# #############################################################################


DEFAULT_BATCH_TRANSACTION_SIZE = 1000


class PriceBatchTransactionControl(FBDPWorld.WorldInterface):
    """------------------------------------------------------------------------
    FUNCTION
        PriceBatchTransactionControl()

    DESCRIPTION
        A class for implementing batch transaction with recovery for updating
        existing entities with new values.
    USAGE:
        Use with the ptyhon 'with' context manager statement.

        with PriceBatchTransactionControl(world, override) as batchHandler:
            ...
            batchHandler.Commit(price)
            ...
    ------------------------------------------------------------------------"""

    def __init__(self, world, override=False):
        FBDPWorld.WorldInterface.__init__(self, world)
        try:
            acm.AbortTransaction()
        except:
            pass
        self.__batchQueue = []
        self.__batchMaxSize = DEFAULT_BATCH_TRANSACTION_SIZE
        self.__override = bool(override)

    def __enter__(self):
        self._logDebug('        Entering batch transaction control '
                '(batchMaxSize={0}).'.format(self.__batchMaxSize))
        try:
            acm.AbortTransaction()
        except:
            pass
        acm.BeginTransaction()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__commitTransaction()
        try:
            acm.AbortTransaction()
        except:
            pass
        self._logDebug('        Exiting batch transaction control.')
        return False  # No exception suppression

    def __commitTransaction(self):
        """
        Internal operation implementing commit the transaction.
        """
        if self._isInTestMode():
            # If it is test mode, undo after the pretended logging is done.
            acm.AbortTransaction()
            self.__log()
            for price, _calcPrice in self.__batchQueue:
                price.Undo()
        else:
            # Commit the transaction then do the logging.  If the transaction
            # failed, call __recoverWithoutTransaction() which commit each
            # price in its own transaction.
            try:
                self._logDebug('            Committing transaction.')
                acm.CommitTransaction()
                self._logDebug('            Transaction committed.')
            except Exception as e:
                acm.AbortTransaction()
                self._logDebug('            Transaction Aborted.  '
                        '{0}'.format(e))
                self.__recoverWithoutTransaction()
            self.__log()
        # Clear batchQueue
        self.__batchQueue = []
        # Restart transaction.
        acm.BeginTransaction()

    def __readExistingPrice(self, insOid, currOid, marketOid, priceDay):
        """
        Read a price with given criteria
        """
        price = None
        query = ('instrument={0} and currency={1} and market={2} and '
                'day=\'{3}\''.format(insOid, currOid, marketOid, priceDay))
        prices = acm.FPrice.Select(query)
        if len(prices) == 1:
            price = prices[0]
        return price

    def __recoverWithoutTransaction(self):
        """
        Note this must be invoke while NOT in a transaction.
        Recover those still in the queue.  Commit them again.  Given now it is
        not in a transaction, each commit is a transaction on its own.
        """
        self._logDebug('            Recovering failed transaction by '
                'committing individually.')
        for (price, calcPrice) in self.__batchQueue:
            existingPrice = self.__readExistingPrice(calcPrice.getIns().Oid(),
                    calcPrice.getCurr().Oid(), calcPrice.getMarket().Oid(),
                    calcPrice.getDate())
            if existingPrice:
                self.__updatePrice(existingPrice, calcPrice.getBid(),
                        calcPrice.getAsk(), calcPrice.getSettle(),
                        calcPrice.getHigh(), calcPrice.getLow(),
                        calcPrice.getLast(), calcPrice.getBits())
                price = existingPrice
            # Commit price again.  Given it is not in a transaction, each
            # commit is a transaction on its own.  Need to wrap them in the
            # try...catch block.
            try:
                self._logDebug('                Individually committing price '
                        '\'{0}\' \'{1}\'.'.format(price.Instrument().Name(),
                        price.Currency().Name()))
                price.Commit()
            except Exception as e:
                self._logDebug('                Individual commit failed.  '
                        '{0}'.format(e))
                calcPrice.markAsFailure()
                calcPrice.setErrMsg(str(e))
        self._logDebug('            Finished individual commits.')

    def __updatePrice(self, price, bid, ask, settle, high, low, last, bits):
        """
        Internal operation for copying values from srcPrice to dstPrice.
        """
        # Bid
        if bid and price.Bid() != bid:
            price.Bid(bid)
        # Ask
        if ask and price.Ask() != ask:
            price.Ask(ask)
        # Settle
        if price.Settle() != settle:
            price.Settle(settle)
        # High
        if high and price.High() != high:
            price.High(high)
        # Low
        if low and price.Low() != low:
            price.Low(low)
        # Last
        if last and price.Last() != last:
            price.Last(last)
        # Bits
        if price.Bits() != bits:
            price.Bits(bits)

    def __makeNewAcmPrice(self, calcPrice):
        price = acm.FPrice()
        price.Instrument(calcPrice.getIns())
        price.Currency(calcPrice.getCurr())
        price.Market(calcPrice.getMarket())
        price.Day(calcPrice.getDate())
        calcPriceBid = calcPrice.getBid()
        if calcPriceBid:
            price.Bid(calcPriceBid)
        calcPriceAsk = calcPrice.getAsk()
        if calcPriceAsk:
            price.Ask(calcPriceAsk)
        price.Settle(calcPrice.getSettle())
        calcPriceHigh = calcPrice.getHigh()
        if calcPriceHigh:
            price.High(calcPriceHigh)
        calcPriceLow = calcPrice.getLow()
        if calcPriceLow:
            price.Low(calcPriceLow)
        calcPriceLast = calcPrice.getLast()
        if calcPriceLast:
            price.Last(calcPriceLast)
        price.Bits(calcPrice.getBits())
        return price

    def commit(self, calcPrice):
        """
        Commit a price.
        Return false if a price already exists, and not to be overridden.
        In test mode, the price will pretended to be committed and return True.
        """
        existingPrice = self.__readExistingPrice(calcPrice.getIns().Oid(),
                calcPrice.getCurr().Oid(), calcPrice.getMarket().Oid(),
                calcPrice.getDate())
        # If price already exists and not to be overridden.
        # Just do nothing and leave!
        self._logDebug('            Price exist.')
        if existingPrice and not self.__override:
            self._logDebug('            Existing price not to be overriden.')
            return False
        # Since price exists, update the existing price and use it instead.
        if existingPrice:
            self.__updatePrice(existingPrice, calcPrice.getBid(),
                    calcPrice.getAsk(), calcPrice.getSettle(),
                    calcPrice.getHigh(), calcPrice.getLow(),
                    calcPrice.getLast(), calcPrice.getBits())
            calcPrice.markAsExisted()
            price = existingPrice
        else:
            price = self.__makeNewAcmPrice(calcPrice)
        # Commit the price into transaction
        if not self._isInTestMode():
            price.Commit()
        self._logDebug('            Price committed into transaction.')
        self.__batchQueue.append((price, calcPrice))
        if len(self.__batchQueue) >= self.__batchMaxSize:
            self.__commitTransaction()
        return True

    def __log(self):
        for price, calcPrice in self.__batchQueue:
            # action
            if calcPrice.isExisted():
                action = 'UPDATE'
            else:
                action = 'CREATE'
            # price info
            priceInfoList = []
            priceInfoList.append('settle={0}'.format(calcPrice.getSettle()))
            if calcPrice.getBid():
                priceInfoList.append(' [bid={0}]'.format(calcPrice.getBid()))
            if calcPrice.getAsk():
                priceInfoList.append(' [ask={0}]'.format(calcPrice.getAsk()))
            if calcPrice.getLast():
                priceInfoList.append(' [last={0}]'.format(calcPrice.getLast()))
            if calcPrice.getHigh():
                priceInfoList.append(' [high={0}]'.format(calcPrice.getHigh()))
            if calcPrice.getLow():
                priceInfoList.append(' [low={0}]'.format(calcPrice.getLow()))
            priceInfoList.append(' for \'{0}\' in \'{1}\' in the market '
                    '\'{2}\' on {3}'.format(calcPrice.getIns().Name(),
                    calcPrice.getCurr().Name(), calcPrice.getMarket().Name(),
                    calcPrice.getDate()))
            priceInfo = ''.join(priceInfoList)
            # summary
            if calcPrice.isFailure():
                self._summaryAddFail(price.RecordType(), price.Oid(),
                        action, [calcPrice.getErrMsg()])
                self._logError('Failed to {0} price {1}'.format(
                        action.lower(), ''.join(priceInfo)))
            else:
                self._summaryAddOk(price.RecordType(), price.Oid(), action)
                self._logDebug('            {0}'.format(priceInfo))


class PriceBatchTransactionControlHandlerInterface(object):

    def __init__(self, world, override):
        self.__world = world
        self.__override = override

    def _getPriceBatchTransactionControlHandler(self):
        return PriceBatchTransactionControl(self.__world, self.__override)


# #############################################################################
# Volatility Structure Selection
# #############################################################################


UndAndDers = collections.namedtuple('UndAndDers', 'undIns derInsList')


VolInsArrayPair = collections.namedtuple('VolInsArrayPair', 'vol insArray')


class VolsInfo(object):

    def __init__(self):
        self.__map = {}

    def add(self, undInsNameCurrName, volInsArrayPair):
        assert isinstance(volInsArrayPair, VolInsArrayPair)
        self.__map[undInsNameCurrName] = volInsArrayPair

    def get(self, undInsNameCurrName):
        return self.__map.get(undInsNameCurrName)


def _getAllLiveVolOidList():

    liveVolOidList = [vol.seqnbr for vol in ael.Volatility]
    return liveVolOidList


def _getLiveVolOidToOnDateHistVolOidMap(strDateToday):

    liveVolOidToOnDateHistVolOidMap = {}
    for liveVol in ael.Volatility:
        query = ('select seqnbr from volatility where '
                'original_vol_seqnbr = {0} '
                'and historical_day = \'{1}\''.format(liveVol.seqnbr,
                strDateToday))
        onDateHistVolOidList = FBDPCommon.get_result_in_list(ael.dbsql(query))
        if len(onDateHistVolOidList) != 1:
            continue
        onDateHistVolOid = onDateHistVolOidList[0]
        histVol = ael.Volatility[onDateHistVolOid]
        if not histVol:
            continue
        liveVolOidToOnDateHistVolOidMap[liveVol.seqnbr] = onDateHistVolOid
    return liveVolOidToOnDateHistVolOidMap


def _getAllOnDateHistVolOidList(liveVolOidToOnDateHistVolOidMap):

    return [oid for oid in liveVolOidToOnDateHistVolOidMap.values()]


def _getNamedLiveVolOidList(world, volNames):

    liveVolOidList = []
    for volName in volNames:
        liveVol = ael.Volatility[volName]
        if not liveVol:
            world.logDebug('    Unable to find volatility structure '
                    '\'{0}\''.format(volName))
            continue
        liveVolOidList.append(liveVol.seqnbr)
    return liveVolOidList


def _getNamedOnDateHistVolOidList(world, volNames,
        liveVolOidToOnDateHistVolOidMap):

    onDateHistVolOidList = []
    for liveVolOid in _getNamedLiveVolOidList(world, volNames):
        if liveVolOid not in liveVolOidToOnDateHistVolOidMap:
            continue
        onDateHistVolOid = liveVolOidToOnDateHistVolOidMap[liveVolOid]
        onDateHistVolOidList.append(onDateHistVolOid)
    return onDateHistVolOidList


def findSelectedVolatilityStructures(world, volNames, all_except_vol):

    allOnDateVolOidList = []
    namedOnDateVolOidList = []
    # Process based the historical date mode setting
    if ael.historical_mode():
        strDateToday = ael.date_today().to_string(ael.DATE_ISO)
        liveVolOidToOnDateHistVolOidMap = _getLiveVolOidToOnDateHistVolOidMap(
                strDateToday)
        allOnDateVolOidList = _getAllOnDateHistVolOidList(
                liveVolOidToOnDateHistVolOidMap)
        namedOnDateVolOidList = _getNamedOnDateHistVolOidList(world,
                volNames, liveVolOidToOnDateHistVolOidMap)
    else:
        allOnDateVolOidList = _getAllLiveVolOidList()
        namedOnDateVolOidList = _getNamedLiveVolOidList(world, volNames)
    # Process based on the all_except_vol flag
    if all_except_vol:
        targetOnDateVolOidList = [oid for oid in allOnDateVolOidList
                if oid not in namedOnDateVolOidList]
    else:
        targetOnDateVolOidList = namedOnDateVolOidList
    # Convert into acm volatility structure
    selectedVolList = []
    for volOid in targetOnDateVolOidList:
        vol = acm.FVolatilityStructure[volOid]
        if not vol:
            continue
        selectedVolList.append(vol)
    return selectedVolList


# #############################################################################
# Yield Curve Selection
# #############################################################################


def _warnIfAcmYieldCurvesAreArchived(world, acmYcList):

    archivedAcmYcList = [acmYc for acmYc in acmYcList
            if FBDPYieldCurveLib.isAcmYieldCurveArchived(acmYc)]
    for acmYc in archivedAcmYcList:
        world.logWarning('The yield curve \'{0}\' specified in the list '
                'had already been archived.'.format(acmYc.Name()))


def findSelectedOriginalYieldCurveNames(world, v_recalc_yieldcurve,
        v_all_except_yieldcurve, v_recalc_also_dep_yc):

    assert (not v_all_except_yieldcurve or
            not v_recalc_also_dep_yc), (
            'v_recalc_in_dep_order should be false whenever '
            'v_all_except_yieldcurve is set to true.')
    specAcmYcList = [acm.FYieldCurve[ycOid] for ycOid in v_recalc_yieldcurve]

    # Warn if curve is archived
    _warnIfAcmYieldCurvesAreArchived(world, specAcmYcList)
    # Selection process
    specYcNameSet = set([acmYc.Name() for acmYc in specAcmYcList])
    allOrigYcNames = FBDPYieldCurveLib.findAllOriginalYieldCurveNameList()
    if v_all_except_yieldcurve:
        origYcNameList = [ycName for ycName in allOrigYcNames
                if ycName not in specYcNameSet]
    else:
        origYcNameList = [ycName for ycName in allOrigYcNames
                if ycName in specYcNameSet]
        if v_recalc_also_dep_yc:
            origYcNameList = (FBDPYieldCurveLib.
                    findBaseCurves(
                    initOrigYcNameList=origYcNameList,
                    toExclOrigYcNameList=[]))
    return origYcNameList


def hieSortYieldCurveNamesIfRequried(world, origYcNameList, isSortingRequired,
        isToWarnMissingDependency):

    if isSortingRequired or isToWarnMissingDependency:
        world.logDebug('    Hierarchical sorting is required.')
        ycHieSorter = FBDPYieldCurveLib.YieldCurveHierarchicalSorter(
                origYcNameList)
    else:
        world.logDebug('    Hierarchical sorting is not required.')
        ycHieSorter = None
    # Dependency warning
    if isToWarnMissingDependency:
        cachedOrigYcNameList = (ycHieSorter.
                getAllCachedOriginalYieldCurveNames())
        if len(cachedOrigYcNameList) > len(origYcNameList):
            diffOrigYcNames = set(cachedOrigYcNameList) - set(origYcNameList)
            warnMsgList = []
            warnMsgList.append('Yield curve dependency')
            warnMsgList.append('The selected yield curves for recalculation '
                    'depend on the following yield curves which had not been '
                    'specified.')
            for origYcName in diffOrigYcNames:
                warnMsgList.append('        {0}'.format(origYcName))
            warnMsgList.append('It is recommended that users should either '
                    'select \'Recalc also depended Yield Curves\' or include '
                    'all yield curves for this task, so that consistent '
                    'calibrations can be made.')
            world.logWarning('\n'.join(warnMsgList))

    #missingDerivedYieldCurvesWarning(world, origYcNameList)

    # Log debug
    if ycHieSorter:
        world.logDebug('            -------- sorter internal data --------')
        for msg in ycHieSorter.getStatisticsAsStringList():
            world.logDebug('            ' + msg)
        world.logDebug('            -------- sorter internal data --------')
    # Return sorting result
    if not isSortingRequired:
        return origYcNameList
    return ycHieSorter.getSortedOriginalYieldCurveNames()


def missingDerivedYieldCurvesWarning(world, origYcNameList):

    origYcOidList = [FBDPYieldCurveLib.
                     _findOriginalAcmYieldCurve(origYcName).Oid()
                     for origYcName in origYcNameList]
    derivedNameSet = set(FBDPYieldCurveLib.
                         findDerivedCurves(
                            origYcOidList))
    if not derivedNameSet.issubset(set(origYcNameList)):
        warnMsgList = []
        warnMsgList.append('Yield curve dependency')
        diffOrigYcNames = derivedNameSet - set(origYcNameList)
        warnMsgList.append('The following yield curves')
        for origYcName in diffOrigYcNames:
            warnMsgList.append('        {0}'.format(origYcName))

        warnMsgList.append('which had not been specified '
                           'depend on the selected yield curves for '
                           'recalculation. '
                           'It is recommended that tasks should include '
                           'these yield curves, '
                           'so that consistent calibrations can be made.')
        world.logWarning('\n'.join(warnMsgList))


def findOnDateAcmYieldCurveList(world, origYcNameList):

    if ael.historical_mode():
        world.logDebug('    In historical date mode.')
        strIsoDateToday = ael.date_today().to_string(ael.DATE_ISO)
        world.logDebug('    Date is \'{0}\'.'.format(strIsoDateToday))
        onDateAcmYcList = [acm.FYieldCurve[ycOid] for ycOid in
                FBDPYieldCurveLib.findOnDateHistoricalYieldCurveOidList(
                origYcNameList, strIsoDateToday)]
    else:
        onDateAcmYcList = [acm.FYieldCurve[origYcName] for origYcName
                in origYcNameList]
    return onDateAcmYcList


# #############################################################################
# Preferred Market
# #############################################################################


class PreferredMarketDescr(object):
    """------------------------------------------------------------------------
    CLASS
        PreferredMarketDescr() --> object
    DESCRIPTION
        A value-object class describing the ordering of a set of preferred
        markets for a price finding rule.
    USAGE:
        Given a price finding rule name (e.g. 'pfrulename'), and a list of
        preferred market names (e.g. ['mrkt1', 'mrkt2', 'mrkt3']), a object
        will be constructed with attributes
            name='pfrule'
            order={'mrkt1':0, 'mrkt2':1, 'mrkt3':2}
            length=3
    NOTE:
        The market assigned with a lower value will have higher preference.
    ------------------------------------------------------------------------"""

    def __init__(self, pfrulename, marketnames):
        """
        pfrulename: name of a price finding rule or None (default rule).
        marketnames: list of market names defining order from left to right.
        """
        # Record the price finding rule name as 'name'.
        if pfrulename == 'None':
            pfrulename = None
        self.name = pfrulename

        # Assign preference number starting from 0 to market names
        # Store the mapping of market name to preference number as 'order'
        mapping = {}
        if isinstance(marketnames, str):
            marketnames = [marketnames]
        for i in range(len(marketnames)):
            marketname = marketnames[i]
            mapping[marketname] = i
        self.order = mapping

        # Assign number of markets specified to 'length'.
        self.length = len(self.order)

    def ToString(self):
        s = '<<< PreferredMarketDescr >>> Name:   {0} '.format(self.name)
        s += 'Order:  {0} '.format(self.order)
        s += 'Length: {0}'.format(self.length)
        return s


class PreferredMarketHandler(dict):
    """------------------------------------------------------------------------
    CLASS
        PreferredMarketHandler() --> dict
    DESCRIPTION
        A value-object class to administer the preferred market descriptions.
    USAGE:
        The instantiated object provide the Prices() method.  It returns a
        tuple containing (1) the prices for the given instrument (sorted
        according to the preferred market descriptions stored during the
        instantiation) and (2) the name of the price finding rule used by the
        instrument.
    NOTE:
    ------------------------------------------------------------------------"""

    def __init__(self, descriptions):
        """
        Store the descriptions and setup the description for default.
        """
        dict.__init__(self)
        # First find the default preferred markets
        self.defaultDescr = None
        for d in descriptions:
            if not d.name:
                self.defaultDescr = d
                break
        # Second, add entry for each price finding rule in the system.  If
        # the default preferred markets has been defined, then use that
        # default preferred markets for the price finding rule.  Otherwise,
        # use the price finding rule's original market specified as the
        # preferred market.
        for pfrule in acm.FPriceFinding.Select(''):
            # Find out the rule name and rule's original market
            pfrulename = pfrule.Name()
            if not pfrulename:
                continue
            # If there is default preferred market.  Use the default
            # preferred market.  (Basically deepcopy the object and
            # make sure the rule name gets replaced)
            if self.defaultDescr:
                self[pfrulename] = copy.deepcopy(self.defaultDescr)
                self[pfrulename].name = pfrulename
                continue
            # Since there is no default preferred market. Find out the
            # price finding rule's original market specification, and
            # use it as the preferred market.
            pfrulemarket = pfrule.Market()
            descr = None
            if pfrulemarket:
                descr = PreferredMarketDescr(pfrulename,
                        [pfrulemarket.Name()])
            else:
                descr = PreferredMarketDescr(pfrulename, [])
            self[pfrulename] = descr
        # Third, if there are preferred markets specified for particular price
        # finding rules, overwrite their record now.
        for d in descriptions:
            self[d.name] = d
        # Last, if the default is still empty, create a blank descr.
        if not self.defaultDescr:
            self.defaultDescr = PreferredMarketDescr(None, [])

    @staticmethod
    def cmp_prices(descr, a, b):
        """
        Compare the two prices using the given preferred market description
        """
        o1 = descr.order.get(a.Market().Name(), descr.length)
        o2 = descr.order.get(b.Market().Name(), descr.length)
        if o2 == o1:
            if b.TradeTime() and a.TradeTime():
                return b.TradeTime() - a.TradeTime()
            else:
                return b.UpdateTime() - a.UpdateTime()
        return o1 - o2

    def Prices(self, ins, day, latest):
        """
        Returns a tuple containing (1) a list of sorted prices for the
        instrument ins and (2) the name of the price finding rule used.
        """
        # Find the price finding name used by the instrument
        priceFindName = None
        insid = ins.Oid()
        try:
            priceFindName = ArenaFunctionBridge.instrument_used_price_finding(
                    insid)
        except:
            pass
        # Find the preferred market description to be used.  If the user had
        # not specified the preferred markets for this price finding rule,
        # used the default one instead.
        descr = self.get(priceFindName, self.defaultDescr)
        # Find the sorted prices for this ins with the given descr.
        prices = self.findAndSortPrices(ins, day, latest, descr)
        # Return the sorted prices and the name of the price finding rule.
        return prices, priceFindName

    def findAndSortPrices(self, ins, day, latest, descr):
        """
        Find the prices for the instrument and return sorted prices in a list.
        """
        # Find the prices
        prices = []
        if latest:
            for p in ins.Prices():
                prices.append(p)
        else:
            # Use acm select when ael select doesn't work
            whereClause = "instrument={0} and day='{1}'".format(ins.Oid(),
                    day)
            fPrices = acm.FPrice.Select(whereClause)
            for price in fPrices:
                prices.append(price)
        # sort the prices into order according the the given descr.
        prices.sort(lambda a, b: PreferredMarketHandler.cmp_prices(descr, a,
                b))
        return prices

    def __str__(self):
        s = '<<< PreferredMarketHandler >>>'
        keys = self.keys()
        keys.sort()
        for k in keys:
            if self[k] == self.defaultDescr:
                tmp = "(default)"
            else:
                tmp = ''
            s += '\nKey: {0} {1} {2}'.format(k, tmp, self[k])
        return s


# #############################################################################
# Filename manipulation
# #############################################################################


VALID_FILE_NAME_CHAR_WHITESPACE = ' '
VALID_FILE_NAME_CHAR_UNDERSCORE = '_'
VALID_FILE_NAME_CHAR_DASH = '-'
VALID_FILE_NAME_CHAR_DOT = '.'


def _isValidFileNameChar(char):

    isValid = (str.isupper(char) or str.islower(char) or str.isdigit(char)
            or char in (VALID_FILE_NAME_CHAR_WHITESPACE,
                    VALID_FILE_NAME_CHAR_UNDERSCORE,
                    VALID_FILE_NAME_CHAR_DASH,
                    VALID_FILE_NAME_CHAR_DOT))
    return isValid


def makeValidFileName(origName):

    if not isinstance(origName, str):
        raise ValueError('The given original name must be a string, but "{0}" '
                'of type "{1}" is given.'.format(origName, type(origName)))
    validFileNameBytes = []
    for char in origName:
        if _isValidFileNameChar(char):
            validFileNameBytes.append(char)
        else:
            twoLetterHexNum = hex(ord(char)).upper().replace('X', '')[-2:]
            validFileNameBytes.append('%{0}'.format(twoLetterHexNum))
    return ''.join(validFileNameBytes)
