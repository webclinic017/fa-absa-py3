""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FDelPricePerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE

    FDelPricePerform.py - Delete Prices implementation.

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""


# #############################################################################
# Programming Guide (for performance)
#
# 1. Avoid using AEL or ACM to load any not-yet-cached objects, unless it is
#     necessary.  This reduces the need of caching and reduces the chance of
#     cache pollution.  In another word, manipulate objects by their oid
#     whenever possible.
# 2. Avoid correlated SQl statements.  The SQL engine may not optimise the
#    statement in the way developer would imagine.
# 3. Reduce I/O requirement.  Try batching up write() operations to files.
# 4. Reduce number of SQL query.  Avoid getting big result set from SQL.
# #############################################################################


import collections
import os
import time


import acm
import ael


import FBDPPerform
import FBDPCommon
import FDelPriceUtil
import importlib
importlib.reload(FDelPriceUtil)


DEFAULT_DELETE_PRICES_TRANSACTION_SIZE = 250  # may be override via hook
DEFAULT_DELETE_PRICES_INSTRUMENT_BATCH_SIZE = 100  # may be override via hook


_PARTY_SELECTION = collections.namedtuple('_PARTY_TYPE_INFO',
        ['typesDesc', 'ptyOidList', 'strIsoLastDelDate'])


def perform(world, execParam):

    r = _DeletePrices(world)
    r.perform(execParam)
    r.end()
    del r


class _MaxRunTimeReachedError(Exception):

    pass


class _DeletePrices(FBDPPerform.FBDPPerform):

    def __init__(self, world):

        FBDPPerform.FBDPPerform.__init__(self, world)
        self.__delPrcTrxSize = DEFAULT_DELETE_PRICES_TRANSACTION_SIZE
        self.__delPrcInsBatchSize = DEFAULT_DELETE_PRICES_INSTRUMENT_BATCH_SIZE
        self.__strIsoDateToday = ael.date_today().to_string(ael.DATE_ISO)
        self.__endTime = None
        self.__InsInfoCache = FDelPriceUtil.InsInfoCache()

    # #########################################################################
    # Timer methods
    #
    # The end time is setup at the beginning of the perform().  During the
    # perform(), call the __checkTimer() to check if end time is reached.  If
    # so, an _MaxRunTimeReachedError exception will be raised.  Inside the
    # perform() the try...except...finally blcoks are used to manage this
    # raised exception.
    # #########################################################################

    def __setupTimer(self, maxRunTime):

        self.__endTime = time.time() + maxRunTime

    def __checkTimer(self):
        """
        Raise _MaxRunTimeReachedError if time is up.
        """
        if self.__endTime is None:
            raise AssertionError('The end time had not been set.')
        if time.time() > self.__endTime:
            self._logError('Maximum Run Time Reached !!')
            raise _MaxRunTimeReachedError('')

    # #########################################################################
    # Price dump management methods
    # #########################################################################

    def __prepareDumpDirectory(self, dirPath):

        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
            self._logInfo('Created directory: {0}'.format(dirPath))

    def __setupPriceDumperAndPriceNumberLogger(self, isToDumpPrice,
            alsoLogPriceNumber, dumpDirPlusPrefix,
            dumpFileSuffix):

        # Parsing
        if isToDumpPrice and dumpDirPlusPrefix:
            dirPath, dumpFilePrefix = os.path.split(dumpDirPlusPrefix)
        else:
            dirPath, dumpFilePrefix = (os.getcwd(), '')
        # Price dumper
        priceDumper = None
        if isToDumpPrice:
            self.__prepareDumpDirectory(dirPath)
            priceDumper = FDelPriceUtil.PriceDumpWriter(self._getWorldRef(),
                    dirPath, dumpFilePrefix, dumpFileSuffix)
        # Price number logger
        priceNumberLogger = None
        if alsoLogPriceNumber:
            priceNumberLogger = FDelPriceUtil.PriceNumberLogWriter(
                    self._getWorldRef(), dirPath, dumpFilePrefix,
                    dumpFileSuffix)
        return priceDumper, priceNumberLogger

    # #########################################################################
    # Common helper methods
    # #########################################################################

    def __prcTyp_queryDateSortedPriceOidList(self, prcTypInfo, insOidList,
            ptyOidList=(), strLastDelDate=''):
        """
        Find sorted oids for prices in the price/price_hst table (determined by
        the given prcTypInfo) with the given instrument, list of parties, and
        before_date.
        """
        assert isinstance(prcTypInfo, FDelPriceUtil.PRICE_TYPE_INFO)
        qry = ('SELECT prinbr FROM {0} WHERE insaddr IN ({1})'.format(
                prcTypInfo.tblName,
                ','.join([str(insOid) for insOid in insOidList])))
        if ptyOidList:
            qry += (' AND ptynbr in ({0})'.format(
                    ','.join([str(oid) for oid in ptyOidList])))
        if strLastDelDate:
            qry += (' AND day <= \'{0}\''.format(strLastDelDate))
        qry += (' ORDER BY day, insaddr')
        result, msSelPrcDuration = FDelPriceUtil.timedAelDbSql(qry)
        self._logDebug('                    [QueryTime = {0} ms]'.format(
                msSelPrcDuration))
        allSortedPrcOidList = [row[0] for row in result]
        return allSortedPrcOidList

    def __prcTyp_delPrcsForDeletedInsAtOnceViaDbSql(self, prcTypInfo,
                delInsOid):

        assert isinstance(prcTypInfo, FDelPriceUtil.PRICE_TYPE_INFO)
        self._logDebug('        Deleting ALL {0}s of a deleted instrument '
                    'at once.'.format(prcTypInfo.desc))
        selQry = ('SELECT count(*) FROM {0} WHERE insaddr = {1}'.format(
                prcTypInfo.tblName, delInsOid))
        result, msSelCountDuration = FDelPriceUtil.timedAelDbSql(selQry)
        numPrc = result[0][0]
        self._logDebug('                    [QueryTime = {0} ms]'.format(
                msSelCountDuration))
        if not self._isInTestMode():
            delQry = 'DELETE FROM {0} WHERE insaddr = {1}'.format(
                    prcTypInfo.tblName, delInsOid)
            result, msDelDuration = FDelPriceUtil.timedAelDbSql(selQry)
            ael.dbsql(delQry)
            self._logDebug('                    [DeleteTime = {0} ms]'.format(
                    msDelDuration))
        self._logDebug('        ALL {0} {1}s of the deleted instrument are '
                    'deleted at once.'.format(numPrc, prcTypInfo.desc))
        # Fake price for summary
        for fakePrcOid in range(numPrc):
            self._summaryAddOk(prcTypInfo.recTyp, (delInsOid, fakePrcOid),
                    'DELETE')

    def __prcTyp_delPrcListViaAelOptDumpPrice(self, prcTypInfo, prcOidList,
            priceDumper):
        """
        Optionally dump price
        """
        assert isinstance(prcTypInfo, FDelPriceUtil.PRICE_TYPE_INFO)
        if not prcOidList:
            return []
        # Find the ael price.
        aelPrcList = []
        for oid in prcOidList:
            aelPrcOid = prcTypInfo.toAelPrcOidConvFunc(oid)
            aelPrice = ael.Price[aelPrcOid]
            if not aelPrice:
                failMsg = ('Unable to find AEL price representation for '
                       'price {0}'.format(aelPrcOid))
                self._logError(failMsg)
                self._summaryAddFail(prcTypInfo.recTyp, aelPrcOid,
                        'DELETE', reasons=[failMsg])
                continue
            aelPrcList.append(aelPrice)
        # Prices are always dumped regardless whether they are successfully
        # deleted.
        if priceDumper:
            mbfPrcSer = FDelPriceUtil.MBFPriceSerialiser()
            with FDelPriceUtil.AutoCloser(priceDumper):
                for aelPrc in aelPrcList:
                    strTimeStamp = FDelPriceUtil.getTimeStamp()
                    serPrcInfo = mbfPrcSer.serialiseAelPrice(aelPrc,
                            strTimeStamp)
                    priceDumper.dumpMbfSerialisedPrice(serPrcInfo)
        delAelPrcOidList = [aelPrc.prinbr for aelPrc in aelPrcList]
        if not self._isInTestMode():
            try:
                timeBefore = time.time()
                ael.begin_transaction()
                for aelPrc in aelPrcList:
                    aelPrc.delete()
                ael.commit_transaction()
                timeAfter = time.time()
                self._logDebug('                [DeleteTime = {0} ms]'.format(
                        (timeAfter - timeBefore) * 1000.0))
            except Exception as e:
                failMsg = ('Unable to delete ael prices. {0}'.format(e))
                self._logError(failMsg)
                for aelPrcOid in delAelPrcOidList:
                    self._summaryAddFail(prcTypInfo.recTyp,
                            aelPrcOid, 'DELETE', reasons=[failMsg])
                ael.abort_transaction()
                raise e
        return delAelPrcOidList

    def __prcTyp_delPrcListViaDbSqlOptDumpPrice(self, prcTypInfo, prcOidList,
            priceDumper):
        """
        Optionally dump price
        """
        assert isinstance(prcTypInfo, FDelPriceUtil.PRICE_TYPE_INFO)
        if not prcOidList:
            return []
        # Prices are always dumped regardless whether they are successfully
        # deleted.
        if priceDumper:
            mbfPrcSer = FDelPriceUtil.MBFPriceSerialiser()
            with FDelPriceUtil.AutoCloser(priceDumper):
                serPrcQry = mbfPrcSer.prcTyp_getPriceDumpDbSqlQuery(prcTypInfo,
                        prcOidList)
                result, _msDuration = FDelPriceUtil.timedAelDbSql(serPrcQry)
                for row in result:
                    strTimeStamp = FDelPriceUtil.getTimeStamp()
                    serPrcInfo = mbfPrcSer.prcTyp_serialiseDbSqlPriceRow(
                            prcTypInfo, row, strTimeStamp)
                    priceDumper.dumpMbfSerialisedPrice(serPrcInfo)
        delAelPrcOidList = [prcTypInfo.toAelPrcOidConvFunc(prcOid)
                for prcOid in prcOidList]
        if not self._isInTestMode():
            try:
                delQry = ('DELETE FROM {0} WHERE prinbr in ({1})'.format(
                        prcTypInfo.tblName,
                        ','.join([str(oid) for oid in prcOidList])))
                _result, msDuration = FDelPriceUtil.timedAelDbSql(delQry)
                self._logDebug('                [DeleteTime = {0} ms]'.format(
                        msDuration))
            except Exception as e:
                failMsg = 'Unable to delete prices via dbsql.  {0}'.format(e)
                self._logError(failMsg)
                for aelPrcOid in delAelPrcOidList:
                    self._summaryAddFail(prcTypInfo.recTyp, aelPrcOid,
                            'DELETE', reasons=[failMsg])
                raise e
        return delAelPrcOidList

    def __prcTyp_deletePricesOneBatchGivenPrcOidList(self, prcTypInfo,
            prcOidList, priceDumper, priceNumberLogger, isInsDeleted):

        assert isinstance(prcTypInfo, FDelPriceUtil.PRICE_TYPE_INFO)
        self.__checkTimer()
        self._logDebug('        Deleting {0} {1}s'.format(len(prcOidList),
                prcTypInfo.desc))
        # If the instruments are deleted.  It had to go through DbSQL.  If
        # dumping is required, going through AEL will be faster, as prices are
        # already cached.
        if isInsDeleted or not priceDumper:
            delAelPrcOidList = self.__prcTyp_delPrcListViaDbSqlOptDumpPrice(
                    prcTypInfo, prcOidList, priceDumper)
        else:
            delAelPrcOidList = self.__prcTyp_delPrcListViaAelOptDumpPrice(
                    prcTypInfo, prcOidList, priceDumper)
        # Now log prices
        if priceNumberLogger:
            priceNumberLogger.logPriceNumbers(delAelPrcOidList)
        for delAelPrcOid in delAelPrcOidList:
            self._summaryAddOk(prcTypInfo.recTyp, delAelPrcOid,
                    'DELETE')
        self._logDebug('        Deleted {0} {1}s'.format(len(delAelPrcOidList),
                prcTypInfo.desc))

    def __findProtectedInsOidList(self, protectedAcmInsList):

        insOidList = [ins.Oid() for ins in protectedAcmInsList]
        return insOidList

    def __findSelectedMtMMarketOidList(self, specifiedMtMMktNameList):
        """
        Return selected mtm markets' oid list.
        """
        acmMtMMktList = []
        if specifiedMtMMktNameList:
            for mtmMktName in specifiedMtMMktNameList:
                acmMtMMkt = acm.FMTMMarket[mtmMktName]
                if not acmMtMMkt:
                    self._logError('Unable to find MtM Market by the name '
                            '\'{0}\'.'.format(mtmMktName))
                acmMtMMktList.append(acmMtMMkt)
        return [mtmMkt.Oid() for mtmMkt in acmMtMMktList]

    def __findSelectedMarketAndBrokerOidList(self, specifiedMktBkrNameList):
        """
        Return selected markets' and brokers' oid list.
        """
        acmMktBkrList = []
        if specifiedMktBkrNameList:
            for ptyName in specifiedMktBkrNameList:
                acmPty = acm.FParty[ptyName]
                if acmPty and acmPty.Type() not in ('Market', 'Broker'):
                    self._logError('Unable to find market place or broker by '
                            'the name \'{0}\'.'.format(ptyName))
                acmMktBkrList.append(acmPty)
        return [pty.Oid() for pty in acmMktBkrList]

    # #########################################################################
    # Methods for processing orphaned prices
    #
    # For the orphaned prices, both historical prices and latest prices are
    # deleted.  The orphaned prices are deleted in individual instruments.  The
    # orphaned prices cannot be dump out (Instruments referred by the orphaned
    # prices prices are deleted and thus instrument name is not available;
    # Prices without instrument name are quite meaningless.)
    # #########################################################################

    def __prcTyp_queryOidSortedDeletedInsOidListOnPrices(self, prcTypInfo):
        """
        Find instrument oids that are in the price/price_hst table (determined
        by the given prcTypInfo), but not in the instrument table.  Return
        sorted oids in a list.
        """
        assert isinstance(prcTypInfo, FDelPriceUtil.PRICE_TYPE_INFO)
        delInsOidQry = (
                'SELECT p.insaddr '
                'FROM (SELECT insaddr '
                        'FROM {0} '
                        'GROUP BY insaddr) as p '
                'LEFT JOIN instrument i '
                'ON p.insaddr = i.insaddr '
                'WHERE i.insaddr IS NULL '
                'ORDER BY p.insaddr'.format(prcTypInfo.tblName))
        result, msDuration = FDelPriceUtil.timedAelDbSql(delInsOidQry)
        delInsOidList = [row[0] for row in result]
        self._logDebug('        Found {0} deleted instruments referred by '
                'the {1}s.  [QueryTime = {2} ms]'.format(
                len(delInsOidList), prcTypInfo.desc, msDuration))
        return delInsOidList

    def __prcTyp_processOrphanedPricesGivenInsOid(self, prcTypInfo,
                insOid, priceNumberLogger):

        assert isinstance(prcTypInfo, FDelPriceUtil.PRICE_TYPE_INFO)
        if priceNumberLogger:
            toBeDeletedPrcOidList = self.__prcTyp_queryDateSortedPriceOidList(
                    prcTypInfo, [insOid])
            while toBeDeletedPrcOidList:
                self.__checkTimer()  # Raise exception when time is up
                trxSize = min(len(toBeDeletedPrcOidList), self.__delPrcTrxSize)
                deletingPrcOidList = toBeDeletedPrcOidList[0:trxSize]
                toBeDeletedPrcOidList = toBeDeletedPrcOidList[trxSize:]
                self.__prcTyp_deletePricesOneBatchGivenPrcOidList(prcTypInfo,
                        deletingPrcOidList, priceDumper=None,
                        priceNumberLogger=priceNumberLogger, isInsDeleted=True)
        else:
            self.__prcTyp_delPrcsForDeletedInsAtOnceViaDbSql(prcTypInfo,
                    insOid)
        self._summaryAddOk('Instrument[Deleted]', insOid,
                'DEL_{0}'.format(prcTypInfo.banner))

    def __prcTyp_processOrphanedPrices(self, prcTypInfo, priceNumberLogger):

        assert isinstance(prcTypInfo, FDelPriceUtil.PRICE_TYPE_INFO)
        self.__checkTimer()  # Raise exception when time is up
        self._logInfo('Finding deleted instruments still referred by '
                '{0}s.'.format(prcTypInfo.desc))
        delInsOidList = self.__prcTyp_queryOidSortedDeletedInsOidListOnPrices(
                prcTypInfo)
        self._logDebug('    {0} deleted instruments found'.format(
                len(delInsOidList)))
        # Deleting prices for deleted instruments
        self._logInfo('Deleting {0} for deleted instruments.'.format(
                prcTypInfo.desc))
        if priceNumberLogger:
            priceNumberLogger.logMessage('\n#Orphaned {0}s '
                    'deleted {1}: \n'.format(prcTypInfo.desc,
                    self.__strIsoDateToday))
        numDeletedInsProcessed = 0
        try:
            for insOid in delInsOidList:
                self.__checkTimer()  # Raise exception when time is up
                self._logInfo('    Deleting {0}s for deleted '
                        'instrument (insaddr={1})'.format(
                        prcTypInfo.desc, insOid))
                self.__prcTyp_processOrphanedPricesGivenInsOid(prcTypInfo,
                        insOid, priceNumberLogger)
                numDeletedInsProcessed += 1
        finally:
            self._logInfo('Deleted {0}s for {1} deleted instruments'.format(
                    prcTypInfo.desc, numDeletedInsProcessed))

    def __processOrphanedPrices(self, priceNumberLogger):

        self.__prcTyp_processOrphanedPrices(
                FDelPriceUtil.PRICE_TYPE_INFO_HISTORICAL,
                priceNumberLogger)
        self.__prcTyp_processOrphanedPrices(
                FDelPriceUtil.PRICE_TYPE_INFO_LATEST,
                priceNumberLogger)

    # #########################################################################
    # Methods for processing expired prices
    #
    # For the expired prices, both historical prices and latest prices are
    # deleted.  The expired prices are deleted in batches of instruments and
    # order by date.  The expired prices are deleted in batches of instruments
    # and ordered by price date.  This allows dumps of the prices of the same
    # day to be accumulated and written into file together, so the overall
    # file access delay can be significantly reduced.
    # #########################################################################

    def __prcTyp_findOidSortedCandidateExpPrcInsOidList(self, prcTypInfo,
        lastTradeIsoDate):
        """
        Find instruments that
                (a) it has no trade
                        or last trade occurred after lastTradeIsoDate,
                (b) it is not a generic instrument,
                (c) it is not a currency instrument,
                (d) either it is a combination instruments (which is difficult
                        to determine whether it is expired in a SQL statement)
                        or it is properly expired, and
                (e) that it has price in the price/price_hst table (determined
                        by the prcTypInfo)
        By 'properly expired' it means an instrument has clear expiry date
        which is before today, and the instrument is not open-ended.
        """
        assert isinstance(prcTypInfo, FDelPriceUtil.PRICE_TYPE_INFO)
        #  All instrument oid in the trade table.
        tradeFilter = ''
        if lastTradeIsoDate:
            tradeFilter += (
                ' OR (i.insaddr IN ( '                        # (a.2)
                    'SELECT t.insaddr '
                    'FROM trade t '
                    'WHERE t.time < \'{0}\' '
                    'GROUP BY t.insaddr) '
                ')'.format(lastTradeIsoDate)
            )

        candExpUnTrdInsOidQry = (
                'SELECT i.insaddr '
                'FROM instrument i '
                'WHERE ( '
                    '(i.insaddr NOT IN ( '                    # (a.1)
                        'SELECT t.insaddr '
                        'FROM trade t '
                        'GROUP BY t.insaddr) '
                '){5} ) '
                'AND i.generic = 0 '                          # (b)
                'AND i.instype <> {0} '                       # (c)
                'AND (i.instype = {1} '                       # (d)
                        'OR (i.exp_day > \'1900-01-01\' '
                                'AND i.exp_day < \'{2}\' '
                                'AND i.open_end <> {3})) '
                'AND i.insaddr IN (SELECT p.insaddr '         # (e)
                        'FROM {4} p '
                        'GROUP BY p.insaddr) '
                'ORDER BY i.insaddr'.format(
                FDelPriceUtil.INS_TYPE_ENUM_CURR,
                FDelPriceUtil.INS_TYPE_ENUM_COMBINATION,
                self.__strIsoDateToday,
                FDelPriceUtil.OPEN_END_STATUS_ENUM_OPEN_END,
                prcTypInfo.tblName,
                tradeFilter))
        result, msDuration = FDelPriceUtil.timedAelDbSql(
                candExpUnTrdInsOidQry)
        candExpUnTrdInsOidList = [row[0] for row in result]

        self._logDebug('        Found {0}  instruments referred by '
                'the {1}s.  [QueryTime = {2} ms]'.format(
                len(candExpUnTrdInsOidQry), prcTypInfo.desc, msDuration))
        return candExpUnTrdInsOidList

    def __prcTyp_processExpiredPricesGivenInsOidList(self, prcTypInfo,
            insOidList, priceDumper, priceNumberLogger):

        assert isinstance(prcTypInfo, FDelPriceUtil.PRICE_TYPE_INFO)
        toBeDeletedPrcOidList = self.__prcTyp_queryDateSortedPriceOidList(
                prcTypInfo, insOidList)
        while toBeDeletedPrcOidList:
            self.__checkTimer()  # Raise exception when time is up
            trxSize = min(len(toBeDeletedPrcOidList), self.__delPrcTrxSize)
            deletingPrcOidList = toBeDeletedPrcOidList[0:trxSize]
            toBeDeletedPrcOidList = toBeDeletedPrcOidList[trxSize:]
            self.__prcTyp_deletePricesOneBatchGivenPrcOidList(prcTypInfo,
                    deletingPrcOidList, priceDumper, priceNumberLogger,
                    isInsDeleted=False)
        for insOid in insOidList:
            self._summaryAddOk('Instrument[ExpUntrd]', insOid,
                    'DEL_{0}'.format(prcTypInfo.banner))

    def __prcTyp_processExpiredPrices(self, prcTypInfo, priceDumper,
            priceNumberLogger, protectedInsOidList, lastTradeIsoDate):

        assert isinstance(prcTypInfo, FDelPriceUtil.PRICE_TYPE_INFO)
        self.__checkTimer()  # Raise exception when time is up
        if lastTradeIsoDate:
            self._logInfo('Finding candidate expired, untraded instruments '
                    'referred by {0}s'.format(prcTypInfo.desc))
        else:
            self._logInfo('Finding candidate expired instruments, not traded'
                    'after {0} referred by {1}s'.format(lastTradeIsoDate,
                    prcTypInfo.desc))

        candInsOidList = self.__prcTyp_findOidSortedCandidateExpPrcInsOidList(
                prcTypInfo, lastTradeIsoDate)
        self._logDebug('    Found {0} candidate expired, untraded '
                'instruments.'.format(len(candInsOidList)))
        # Excluding unexpired instruments
        self._logInfo('    Detail excluding unexpired instruments.')
        expUntrdInsOidList = [insOid for insOid in candInsOidList
                if self.__InsInfoCache.isInsExpired(
                insOid, self.__strIsoDateToday)]
        self._logDebug('    {0} instruments remains.'.format(
                len(expUntrdInsOidList)))
        # Excluding protected instruments
        self._logInfo('    Excluding protected instruments.')
        targetInsOidList = [insOid for insOid in expUntrdInsOidList
                if insOid not in protectedInsOidList]
        self._logInfo('    {0} instruments remains.'.format(
                len(targetInsOidList)))
        # Deleting prices for deleted instruments
        self._logInfo('Deleting {0}s for expired, untraded instruments'.format(
                prcTypInfo.desc))
        if priceNumberLogger:
            priceNumberLogger.logMessage('\n#Expired {0}s deleted {1}: '
                    '\n'.format(prcTypInfo.desc, self.__strIsoDateToday))
        # Batching up instruments.
        toBeProcessedInsOidList = targetInsOidList[:]
        while toBeProcessedInsOidList:
            self.__checkTimer()  # Raise exception when time is up
            batchSize = min(len(toBeProcessedInsOidList),
                    self.__delPrcInsBatchSize)
            processingInsOidList = toBeProcessedInsOidList[0:batchSize]
            toBeProcessedInsOidList = toBeProcessedInsOidList[batchSize:]
            self._logInfo('    Batching {0} instruments to be processed '
                    'at once.'.format(len(processingInsOidList)))
            self.__prcTyp_processExpiredPricesGivenInsOidList(prcTypInfo,
                    processingInsOidList, priceDumper, priceNumberLogger)
        return targetInsOidList

    def __processExpiredPrices(self, priceDumper, priceNumberLogger,
            protectedInsOidList, tradeOpenPeriod):

        today = acm.Time.DateToday()
        acm_lastTradeDate = FBDPCommon.dateAddDatePeriod(date=today,
            period=tradeOpenPeriod) if tradeOpenPeriod else None
        lastTradeIsoDate = ael.date(acm_lastTradeDate).to_string(
            ael.DATE_ISO) if acm_lastTradeDate else None
        self.__prcTyp_processExpiredPrices(
                FDelPriceUtil.PRICE_TYPE_INFO_HISTORICAL,
                priceDumper, priceNumberLogger, protectedInsOidList,
                lastTradeIsoDate)
        self.__prcTyp_processExpiredPrices(
                FDelPriceUtil.PRICE_TYPE_INFO_LATEST,
                priceDumper, priceNumberLogger, protectedInsOidList,
                lastTradeIsoDate)

    # #########################################################################
    # Methods for processing selected prices
    #
    # For the selected prices, only the historical prices are deleted, not the
    # latest prices.  However, the deletion of the selected historical prices
    # is further split into sub-processes based on the ptySln.  The selected
    # prices are deleted in batches of instruments and ordered by price date.
    # This allows dumps of the prices of the same day to be accumulated and
    # written into file together, so the overall file access delay can be
    # significantly reduced.
    # #########################################################################

    def __ptySln_processSelectedHistoricalPricesGivenInsOidList(self, ptySln,
            insOidList, priceDumper, priceNumberLogger, keepEndOfMonth):

        self.__checkTimer()  # Raise exception when time is up
        prcTypInfo = FDelPriceUtil.PRICE_TYPE_INFO_HISTORICAL
        toBeDeletedPrcOidList = self.__prcTyp_queryDateSortedPriceOidList(
                prcTypInfo, insOidList, ptySln.ptyOidList,
                ptySln.strIsoLastDelDate)
        self._logDebug('        Found {0} historical prices in {1} on and '
                'before {2}.'.format(len(toBeDeletedPrcOidList),
                ptySln.typesDesc, ptySln.strIsoLastDelDate))
        if not toBeDeletedPrcOidList:
            return
        if keepEndOfMonth:
            self.__checkTimer()  # Raise exception when time is up
            self._logDebug('        Filtering away end-of-month prices')
            aelPrices = [ael.Price[prcTypInfo.toAelPrcOidConvFunc(prcOid)]
                    for prcOid in toBeDeletedPrcOidList]
            nonEOMAelPrices = [aelPrice for aelPrice in aelPrices
                    if not FDelPriceUtil.isLastBankingDayOfMonth(
                            aelPrice.day, aelPrice.curr)]
            toBeDeletedPrcOidList = [
                    prcTypInfo.fromAelPrcOidConvFunc(aelPrice.prinbr) for
                    aelPrice in nonEOMAelPrices]
            self._logDebug('        {0} prices remains to be deleted.'.format(
                    len(toBeDeletedPrcOidList)))
        while toBeDeletedPrcOidList:
            self.__checkTimer()  # Raise exception when time is up
            trxSize = min(len(toBeDeletedPrcOidList), self.__delPrcTrxSize)
            deletingHstPrcOidList = toBeDeletedPrcOidList[0:trxSize]
            toBeDeletedPrcOidList = toBeDeletedPrcOidList[trxSize:]
            self.__prcTyp_deletePricesOneBatchGivenPrcOidList(prcTypInfo,
                    deletingHstPrcOidList, priceDumper, priceNumberLogger,
                    isInsDeleted=False)
        for insOid in insOidList:
            self._summaryAddOk('Instrument[Selected]', insOid,
                    'DEL_{0}'.format(prcTypInfo.banner))

    def __ptySln_processSelectedHistoricalPrices(self, ptySln,
            selectedInsOidList, priceDumper, priceNumberLogger,
            keepEndOfMonth):

        self.__checkTimer()  # Raise exception when time is up
        self._logInfo('Deleting historical prices of the selected {0} on the '
                '{1} selected instruments.'.format(ptySln.typesDesc,
                len(selectedInsOidList)))
        # Batching up instruments.
        toBeProcessedInsOidList = selectedInsOidList[:]
        while toBeProcessedInsOidList:
            self.__checkTimer()  # Raise exception when time is up
            batchSize = min(len(toBeProcessedInsOidList),
                    self.__delPrcInsBatchSize)
            processingInsOidList = toBeProcessedInsOidList[0:batchSize]
            toBeProcessedInsOidList = toBeProcessedInsOidList[batchSize:]
            self._logInfo('    Batching {0} instruments to be processed '
                    'at once.'.format(len(processingInsOidList)))
            self.__ptySln_processSelectedHistoricalPricesGivenInsOidList(
                    ptySln, processingInsOidList, priceDumper,
                    priceNumberLogger, keepEndOfMonth)
        return selectedInsOidList

    def __processSelectedPrices(self, priceDumper,
            priceNumberLogger, protectedInsOidList, specifiedAcmInsList,
            mtmMktPtySln, mktBrkPtySln, keepEndOfMonth, closedInsOnly):

        self.__checkTimer()  # Raise exception when time is up
        self._logInfo('Finding selected instruments.')
        if closedInsOnly:
            # Excluding non-closed instruments
            self._logInfo(
                '    Excluding instruments with non-zero positions.')
            specifiedAcmInsList = [acmIns for acmIns in
                specifiedAcmInsList if FDelPriceUtil.hasZeroPosition(acmIns)]
            self._logInfo('    {0} selected instruments remains'.format(
                    len(specifiedAcmInsList)))

        # Excluding protected instruments
        self._logInfo('    Excluding protected instruments.')
        selectedInsOidList = [acmIns.Oid() for acmIns in specifiedAcmInsList
                if acmIns.Oid() not in protectedInsOidList]
        self._logInfo('    {0} selected instruments remains'.format(
                len(selectedInsOidList)))
        if priceNumberLogger:
            priceNumberLogger.logMessage('\n#Selected historical prices '
                    'deleted {0}: \n'.format(self.__strIsoDateToday))
        # Identifying instruments that have prices on the MtM Markets
        if mtmMktPtySln.ptyOidList:
            self.__ptySln_processSelectedHistoricalPrices(mtmMktPtySln,
                    selectedInsOidList, priceDumper, priceNumberLogger,
                    keepEndOfMonth)
        # Identifying instruments that have prices on the MtM Markets
        if mktBrkPtySln.ptyOidList:
            self.__ptySln_processSelectedHistoricalPrices(mktBrkPtySln,
                    selectedInsOidList, priceDumper, priceNumberLogger,
                    keepEndOfMonth)

    # #########################################################################
    # Hook processing
    # #########################################################################

    def __loadHookGetDeletePricesTransactionSize(self):

        try:
            from FBDPHook import get_delete_prices_transaction_size
            self._logInfo('Load FBDPHook get_delete_prices_transaction_size()')
            val = get_delete_prices_transaction_size()
            if isinstance(val, int) and val > 0:
                self.__delPrcTrxSize = val
            else:
                self._logInfo('Obtained insane value \'{0}\', revert to the '
                        'default value {1}.'.format(val,
                        self.__delPrcTrxSize))
        except:
            pass  # Swallow
        self._logInfo('Set \'delete prices transaction size\' to '
                '{0}'.format(self.__delPrcTrxSize))

    def __loadHookGetDeletePricesInstrumentSizeBatchSize(self):

        try:
            from FBDPHook import get_delete_prices_instrument_batch_size
            self._logInfo('Load FBDPHook '
                    'get_delete_prices_instrument_batch_size()')
            val = get_delete_prices_instrument_batch_size()
            if isinstance(val, int) and val > 0:
                self.__delPrcInsBatchSize = val

            else:
                self._logInfo('Obtained insane value \'{0}\', revert to the '
                        'default value {1}.'.format(val,
                        self.__delPrcInsBatchSize))
        except:
            pass  # Swallow
        self._logInfo('Set \'delete prices instrument batch size\' to '
                '{0}'.format(self.__delPrcInsBatchSize))

    # #########################################################################
    # Entry methods: perform() and end()
    # #########################################################################

    def perform(self, execParam):

        isToDelOrphanedPrices = bool(execParam['CheckForPricesWithoutIns'])
        isToDelExpiredPrices = bool(execParam['DropExpIns'])
        isToDelSelectedPrices = bool(execParam.get('DelSelPrc', True))
        specifiedAcmInsList = execParam.get('Instruments', [])
        protectedAcmInsList = execParam['Protected']
        specifiedMtMMktNameList = execParam.get('MtMMarkets', [])
        mtmMktLastDate = execParam.get('DateMtM',
                FDelPriceUtil.INCEPTION_DATE)
        specifiedMktBkrNameList = execParam.get('Markets', [])
        mktBkrLastDate = execParam.get('DateLast',
                FDelPriceUtil.INCEPTION_DATE)
        closedInsOnly = bool(execParam.get('ClosedInstrumentsOnly', False))
        keepEndOfMonth = bool(execParam['KeepEndOfMonth'])
        isToDumpPrice = bool(execParam.get('SavePrices', False))
        dumpDirPlusPrefix = str(execParam['DumpDirPath'])
        dumpFileSuffix = str(execParam['DumpSuffix'])
        maxRunTime = float(execParam['MaxRuntime'])
        tradeOpenPeriod = execParam.get('TradeOpenPeriod') or None
        if tradeOpenPeriod:
            tradeOpenPeriod = '-%s' % tradeOpenPeriod

        alsoLogPriceNumber = False
        # Time
        self.__setupTimer(maxRunTime)
        # Configurations
        self.__loadHookGetDeletePricesTransactionSize()
        self.__loadHookGetDeletePricesInstrumentSizeBatchSize()
        # Price dumper and number logger
        priceDumper, priceNumberLogger = (
                self.__setupPriceDumperAndPriceNumberLogger(isToDumpPrice,
                        alsoLogPriceNumber, dumpDirPlusPrefix, dumpFileSuffix))
        # Find things
        protectedInsOidList = self.__findProtectedInsOidList(
                protectedAcmInsList)
        # Setup party selection for MtM Markets
        if mtmMktLastDate <= FDelPriceUtil.INCEPTION_DATE:
            mtmMktLastDate = FDelPriceUtil.INCEPTION_DATE
        selectedMtMMktOidList = self.__findSelectedMtMMarketOidList(
                specifiedMtMMktNameList)
        mtmMktPtySln = _PARTY_SELECTION(typesDesc='MtM Markets',
                ptyOidList=selectedMtMMktOidList,
                strIsoLastDelDate=mtmMktLastDate)
        self._logInfo('Date for {0} are set to \'{1}\''.format(
                mtmMktPtySln.typesDesc, mtmMktLastDate))
        # Setup party selection for Markets and Brokers
        if mktBkrLastDate <= FDelPriceUtil.INCEPTION_DATE:
            mktBkrLastDate = FDelPriceUtil.INCEPTION_DATE
        selectedMktBkrOidList = self.__findSelectedMarketAndBrokerOidList(
                specifiedMktBkrNameList)
        mktBrkPtySln = _PARTY_SELECTION(typesDesc='Market Places and Brokers',
                ptyOidList=selectedMktBkrOidList,
                strIsoLastDelDate=mktBkrLastDate)
        self._logInfo('Date for {0} are set to \'{1}\''.format(
                mktBrkPtySln.typesDesc, mktBkrLastDate))
        # Process
        try:
            self.__checkTimer()
            # Orphaned Prices
            if isToDelOrphanedPrices:
                if priceDumper:
                    self._logWarning('Prices refer to instruments that '
                            'no longer exists are not dumped out.')
                self.__processOrphanedPrices(priceNumberLogger)
            # Expired Prices
            if isToDelExpiredPrices:
                self.__processExpiredPrices(priceDumper, priceNumberLogger,
                        protectedInsOidList, tradeOpenPeriod)
            # Selected Prices
            if isToDelSelectedPrices:
                self.__processSelectedPrices(priceDumper, priceNumberLogger,
                        protectedInsOidList, specifiedAcmInsList, mtmMktPtySln,
                        mktBrkPtySln, keepEndOfMonth, closedInsOnly)
        except _MaxRunTimeReachedError:
            pass  # swallow exception
        finally:
            # Ensure priceDumper is properly closed once more time!
            if priceDumper:
                priceDumper.close()

    def end(self):

        pass
