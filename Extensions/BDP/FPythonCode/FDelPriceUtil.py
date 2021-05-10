""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FDelPriceUtil.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE

    FDelPriceUtil.py - Delete Prices utility library.

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import collections
import os
import time


import acm
import ael


import FBDPWorld
import FBDPCalculatePosition

INCEPTION_DATE = '1970-01-01'


INS_TYPE_TEXT_CURR = 'Curr'
INS_TYPE_ENUM_CURR = 21
INS_TYPE_TEXT_COMBINATION = 'Combination'
INS_TYPE_ENUM_COMBINATION = 28


OPEN_END_STATUS_TEXT_OPEN_END = 'Open End'
OPEN_END_STATUS_ENUM_OPEN_END = 1


# #############################################################################
# Price type information
# #############################################################################


_PRICE_HST_OID_GAP = (1 << 30)


def hstPrcOidToAelPrcOid(hstPrcOid):

    return hstPrcOid + _PRICE_HST_OID_GAP


def aelPrcOidToHstPrcOid(aelPrcOid):

    return aelPrcOid - _PRICE_HST_OID_GAP


def ltsPrcOidToAelPrcOid(ltsPrcOid):

    return ltsPrcOid


def aelPrcOidToLtsPrcOid(aelPrcOid):

    return aelPrcOid


PRICE_TYPE_INFO = collections.namedtuple('PRICE_TYPE_INFO',
        ['recTyp', 'desc', 'tblName', 'banner', 'toAelPrcOidConvFunc',
        'fromAelPrcOidConvFunc'])


PRICE_TYPE_INFO_HISTORICAL = PRICE_TYPE_INFO(
        recTyp='Price[Historical]',
        desc='historical price',
        tblName='price_hst',
        banner='HIST_PRICE',
        toAelPrcOidConvFunc=hstPrcOidToAelPrcOid,
        fromAelPrcOidConvFunc=aelPrcOidToHstPrcOid)


PRICE_TYPE_INFO_LATEST = PRICE_TYPE_INFO(
        recTyp='Price[Latest]',
        desc='latest price',
        tblName='price',
        banner='LTST_PRICE',
        toAelPrcOidConvFunc=ltsPrcOidToAelPrcOid,
        fromAelPrcOidConvFunc=aelPrcOidToLtsPrcOid)


# #############################################################################
# Last Banking Day of the Month Test
# #############################################################################


def _isBankingDay(aelDate, aelCurr):

    return aelDate.adjust_to_banking_day(aelCurr) == aelDate


def isLastBankingDayOfMonth(aelDate, aelCurr):
    """
    The given date is last banking date of the month if the next banking day is
    the first banking day of next month.
    """
    # Find next banking day
    if _isBankingDay(aelDate, aelCurr):
        nextBankingDay = aelDate.add_banking_day(aelCurr, 1)
    else:
        nextBankingDay = aelDate
    # Find first banking day of next month
    firstDayOfNextMonth = aelDate.add_months(1).first_day_of_month()
    if _isBankingDay(firstDayOfNextMonth, aelCurr):
        firstBankingDayOfNextMonth = firstDayOfNextMonth
    else:
        firstBankingDayOfNextMonth = firstDayOfNextMonth.add_banking_day(
                aelCurr, 1)
    # If the next banking day is the first banking day of next month, then the
    # given date is last banking day of the month
    return nextBankingDay == firstBankingDayOfNextMonth


# #############################################################################
# Position calculations
# #############################################################################


def hasZeroPosition(ins):
    calcPositions = FBDPCalculatePosition.CalculatePosition(
        i=ins,
        end_date=ins.ExpiryDate() or acm.Time.DateToday(),
        showSummary=False,
        usePlClearDate=False
    )
    quantity = 0
    for calcPosition in calcPositions:
        # calcPosition[0] = FTrade representing position (already summed),
        #       always a list of one for this use-case.
        quantity += calcPosition[0][0].Quantity()

    return quantity == 0


# #############################################################################
# Timing functions
# #############################################################################


def timedAelDbSql(qry):

    timeBefore = time.time()
    resultSets = ael.dbsql(qry)
    if resultSets:
        resultSet = resultSets[0]
    else:
        resultSet = None
    timeAfter = time.time()
    msDuration = int((timeAfter - timeBefore) * 1000.0)
    return resultSet, msDuration


def _toStrWritingTime(timeBefore, timeAfter):

    msTimeDiff = int((timeAfter - timeBefore) * 1000.0)
    return '[WritingTime = {0} ms]'.format(msTimeDiff)


# #############################################################################
# Message Broker Format Price Serialiser
# #############################################################################


_PRICE_DB_COL_LIST = ('prinbr', 'insaddr', 'curr', 'ptynbr', 'creat_usrnbr',
        'updat_usrnbr', 'day', 'bid', 'ask', 'n_bid', 'n_ask', 'last_',
        'high', 'low', 'open_', 'settle', 'diff', 'volume_last',
        'volume_nbr', 'available', 'bits')


SerialisedPriceInfo = collections.namedtuple('SerialisedPriceInfo',
        ['aelprinbr', 'strIsoPrcDate', 'mbfSerPrcStr'])


_FA_VERSION = acm.InternalVersion()


def getTimeStamp():

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def _toStrValEmptyForNone(val):

    if val is None:
        return ''
    return str(val)


class MBFPriceSerialiser(object):

    _PriceRepr = collections.namedtuple('_PriceRepr', _PRICE_DB_COL_LIST)

    def __init__(self):

        self.__insNameOrStrOidCache = {}
        self.__ptyNameOrStrOidCache = {}
        self.__usrNameOrStrOidCache = {}

    def __getInsNameOrStrOid(self, insOid):

        if insOid in self.__insNameOrStrOidCache:
            return self.__insNameOrStrOidCache[insOid]
        aelIns = ael.Instrument[insOid]
        if aelIns:
            insNameOrStrOid = aelIns.insid
        elif insOid:
            insNameOrStrOid = str(insOid)
        else:
            insNameOrStrOid = ''
        self.__insNameOrStrOidCache[insOid] = insNameOrStrOid
        return insNameOrStrOid

    def __getPtyNameOrStrOid(self, ptyOid):

        if ptyOid in self.__ptyNameOrStrOidCache:
            return self.__ptyNameOrStrOidCache[ptyOid]
        aelPty = ael.Party[ptyOid]
        if aelPty:
            ptyNameOrStrOid = aelPty.ptyid
        elif ptyOid:
            ptyNameOrStrOid = str(ptyOid)
        else:
            ptyNameOrStrOid = ''
        self.__ptyNameOrStrOidCache[ptyOid] = ptyNameOrStrOid
        return ptyNameOrStrOid

    def __getUsrNameOrStrOid(self, usrOid):

        if usrOid in self.__usrNameOrStrOidCache:
            return self.__usrNameOrStrOidCache[usrOid]
        aelUsr = ael.User[usrOid]
        if aelUsr:
            usrNameOrStrOid = aelUsr.userid
        elif usrOid:
            usrNameOrStrOid = str(usrOid)
        else:
            usrNameOrStrOid = ''
        self.__usrNameOrStrOidCache[usrOid] = usrNameOrStrOid
        return usrNameOrStrOid

    def __prcTyp_getPriceReprGivenDbSqlPriceRow(self, prcTypInfo, row):

        # Bind the tuple/list to named tuple to get easy access by name
        limboPR = self._PriceRepr(*row)
        # Now convert each field to the real PriceRepr.
        priceRepr = self._PriceRepr(
                prinbr=prcTypInfo.toAelPrcOidConvFunc(int(limboPR.prinbr)),
                insaddr=self.__getInsNameOrStrOid(limboPR.insaddr),
                curr=self.__getInsNameOrStrOid(limboPR.curr),
                ptynbr=self.__getPtyNameOrStrOid(limboPR.ptynbr),
                creat_usrnbr=self.__getUsrNameOrStrOid(limboPR.creat_usrnbr),
                updat_usrnbr=self.__getUsrNameOrStrOid(limboPR.updat_usrnbr),
                day=ael.date(limboPR.day[:10]).to_string(ael.DATE_ISO),
                bid=_toStrValEmptyForNone(limboPR.bid),
                ask=_toStrValEmptyForNone(limboPR.ask),
                n_bid=_toStrValEmptyForNone(limboPR.n_bid),
                n_ask=_toStrValEmptyForNone(limboPR.n_ask),
                last_=_toStrValEmptyForNone(limboPR.last_),
                high=_toStrValEmptyForNone(limboPR.high),
                low=_toStrValEmptyForNone(limboPR.low),
                open_=_toStrValEmptyForNone(limboPR.open_),
                settle=_toStrValEmptyForNone(limboPR.settle),
                diff=_toStrValEmptyForNone(limboPR.diff),
                volume_last=_toStrValEmptyForNone(limboPR.volume_last),
                volume_nbr=_toStrValEmptyForNone(limboPR.volume_nbr),
                available=_toStrValEmptyForNone(limboPR.available),
                bits=_toStrValEmptyForNone(limboPR.bits))
        return priceRepr

    def __getPriceReprGivenAelPrice(self, aelPrice):

        warnMsgList = []
        # instrument name
        if aelPrice.insaddr:
            insName = aelPrice.insaddr.insid
        else:
            warnMsgList.append('Unable to find instrument name, left blank.')
            insName = ''
        # currency name
        if aelPrice.curr:
            currName = aelPrice.curr.insid
        else:
            warnMsgList.append('Unable to find currency name.')
            currName = ''
        # party name
        if aelPrice.ptynbr:
            ptyName = aelPrice.ptynbr.ptyid
        else:
            warnMsgList.append('Unable to find party name.')
            ptyName = ''
        # create user name
        if aelPrice.creat_usrnbr:
            creatUsrName = aelPrice.creat_usrnbr.userid
        else:
            warnMsgList.append('Unable to find create user name.')
            creatUsrName = ''
        # Update user name
        if aelPrice.updat_usrnbr:
            updatUsrName = aelPrice.updat_usrnbr.userid
        else:
            warnMsgList.append('Unable to find update user name.')
            updatUsrName = ''
        # date
        if aelPrice.day:
            strIsoPrcDate = aelPrice.day.to_string(ael.DATE_ISO)
        else:
            warnMsgList.append('Unable to find price date.')
            strIsoPrcDate = ''
        # Construct PriceRepr
        priceRepr = self._PriceRepr(
                prinbr=aelPrice.prinbr,
                insaddr=insName,
                curr=currName,
                ptynbr=ptyName,
                creat_usrnbr=creatUsrName,
                updat_usrnbr=updatUsrName,
                day=strIsoPrcDate,
                bid=str(aelPrice.bid),
                ask=str(aelPrice.ask),
                n_bid=str(aelPrice.n_bid),
                n_ask=str(aelPrice.n_ask),
                last_=str(aelPrice.last),
                high=str(aelPrice.high),
                low=str(aelPrice.low),
                open_=str(aelPrice.open),
                settle=str(aelPrice.settle),
                diff=str(aelPrice.diff),
                volume_last=str(aelPrice.volume_last),
                volume_nbr=str(aelPrice.volume_nbr),
                available=str(aelPrice.available),
                bits=str(aelPrice.bits))
        return priceRepr

    def __serialise(self, priceRepr, strTimeStamp):

        mbfSerPrcStr = (
                '[MESSAGE]\n'
                '    TYPE=INSERT_PRICE\n'
                '    VERSION={faVer}\n'
                '    TIME={timeStamp}\n'
                '    SOURCE=DumpPriceHst/Price\n'
                '    [PRICE]\n'
                '        INSADDR.INSID={pr.insaddr}\n'
                '        CURR.INSID={pr.curr}\n'
                '        PTYNBR.PTYID={pr.ptynbr}\n'
                '        CREAT_USRNBR.USERID={pr.creat_usrnbr}\n'
                '        UPDAT_USRNBR.USERID={pr.updat_usrnbr}\n'
                '        DAY={pr.day}\n'
                '        BID={pr.bid}\n'
                '        ASK={pr.ask}\n'
                '        N_BID={pr.n_bid}\n'
                '        N_ASK={pr.n_ask}\n'
                '        LAST={pr.last_}\n'
                '        HIGH={pr.high}\n'
                '        LOW={pr.low}\n'
                '        OPEN={pr.open_}\n'
                '        SETTLE={pr.settle}\n'
                '        DIFF={pr.diff}\n'
                '        VOLUME_LAST={pr.volume_last}\n'
                '        VOLUME_NBR={pr.volume_nbr}\n'
                '        AVAILABLE={pr.available}\n'
                '        BITS={pr.bits}\n'
                '    [/PRICE]\n'
                '[/MESSAGE]\n').format(
                faVer=_FA_VERSION, timeStamp=strTimeStamp, pr=priceRepr)
        serPrcInfo = SerialisedPriceInfo(
                aelprinbr=priceRepr.prinbr,
                strIsoPrcDate=priceRepr.day,
                mbfSerPrcStr=mbfSerPrcStr)
        return serPrcInfo

    def serialiseAelPrice(self, aelPrice, strTimeStamp):

        priceRepr = self.__getPriceReprGivenAelPrice(aelPrice)
        serPrcInfo = self.__serialise(priceRepr, strTimeStamp)
        return serPrcInfo

    def prcTyp_getPriceDumpDbSqlQuery(self, prcTypInfo, prcOidList):

        qry = ('SELECT {0} FROM {1} WHERE prinbr IN ({2})'.format(
                ','.join(self._PriceRepr._fields), prcTypInfo.tblName,
                ','.join([str(prcOid) for prcOid in prcOidList])))
        return qry

    def prcTyp_serialiseDbSqlPriceRow(self, prcTypInfo, prcRow, strTimeStamp):

        priceRepr = self.__prcTyp_getPriceReprGivenDbSqlPriceRow(prcTypInfo,
                prcRow)
        serPrcInfo = self.__serialise(priceRepr, strTimeStamp)
        return serPrcInfo


# #############################################################################
# Price Dump Writer
# #############################################################################


class PriceDumpWriter(FBDPWorld.WorldInterface):

    def __init__(self, worldRef, dirPath, filePrefix, fileSuffix):

        FBDPWorld.WorldInterface.__init__(self, worldRef)
        self.__dirPath = dirPath
        self.__filePrefix = filePrefix
        self.__fileSuffix = fileSuffix
        # Write Buffer
        self.__lastStrIsoPrcDate = None
        self.__serPrcInfoBuffer = []

    def __getFileFullPath(self, strPriceDate):

        filename = '{0}_{1}.{2}'.format(self.__filePrefix,
                ael.date(strPriceDate).to_string(ael.DATE_Quick),
                self.__fileSuffix)
        fileFullPath = os.path.join(self.__dirPath, filename)
        return fileFullPath

    def __flushBufferToFile(self):

        if self.__lastStrIsoPrcDate and self.__serPrcInfoBuffer:
            fileFullPath = self.__getFileFullPath(self.__lastStrIsoPrcDate)
            timeBefore = time.time()
            with open(fileFullPath, 'a') as dumpFile:
                dumpFile.write(''.join(self.__serPrcInfoBuffer))
            timeAfter = time.time()
            self._logDebug('                dumpPrc {0}'.format(
                    _toStrWritingTime(timeBefore, timeAfter)))
        # Reset buffer
        self.__lastStrIsoPrcDate = None
        self.__serPrcInfoBuffer = []

    def dumpMbfSerialisedPrice(self, serPrcInfo):

        if self._isInTestMode():
            return serPrcInfo.aelprinbr
        if serPrcInfo.strIsoPrcDate != self.__lastStrIsoPrcDate:
            self.__flushBufferToFile()
            self.__lastStrIsoPrcDate = serPrcInfo.strIsoPrcDate
        self.__serPrcInfoBuffer.append(serPrcInfo.mbfSerPrcStr)
        return serPrcInfo.aelprinbr

    def close(self):

        self.__flushBufferToFile()


# #############################################################################
# For automatic closing the price dumper.
# #############################################################################


class AutoCloser(object):

    def __init__(self, priceDumper):

        assert (isinstance(priceDumper, PriceDumpWriter) or
                priceDumper is None), ('Wrong type of priceDumper given.')
        self.__priceDumper = priceDumper

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        if self.__priceDumper:
            self.__priceDumper.close()
        return False  # Return False so exception won't be suppressed.


# #############################################################################
# Price Number Log Writer
# #############################################################################


class PriceNumberLogWriter(FBDPWorld.WorldInterface):

    def __init__(self, worldRef, dirPath, filePrefix, fileSuffix):

        FBDPWorld.WorldInterface.__init__(self, worldRef)
        self.__fileFullPath = self.__getFileFullPath(dirPath, filePrefix,
                fileSuffix)

    def __getFileFullPath(self, dirPath, filePrefix, fileSuffix):

        filename = '{0}_prinbr.{1}'.format(filePrefix, fileSuffix)
        fileFullPath = os.path.join(dirPath, filename)
        return fileFullPath

    def logMessage(self, msg):

        if self._isInTestMode():
            return
        timeBefore = time.time()
        with open(self.__fileFullPath, 'a') as priceNumberLogFile:
            priceNumberLogFile.write(msg)
        timeAfter = time.time()
        self._logDebug('                PrcNbrLogMsg {0}'.format(
                _toStrWritingTime(timeBefore, timeAfter)))

    def logPriceNumbers(self, aelPrcOidList):

        msgList = []
        for aelPrcOid in aelPrcOidList:
            msgList.append('{0}\n'.format(aelPrcOid))
        if self._isInTestMode():
            return
        timeBefore = time.time()
        with open(self.__fileFullPath, 'a') as priceNumberLogFile:
            for msg in msgList:
                priceNumberLogFile.write(msg)
        timeAfter = time.time()
        self._logDebug('                PrcNbrLogMsgList {0}'.format(
                _toStrWritingTime(timeBefore, timeAfter)))


# #############################################################################
# Instrument Information Cache
# #############################################################################


class InsInfoCache(object):

    def __init__(self):

        self.__isExpiredCache = {}

    def __checkIfCombInsExpired(self, insOid, strIsoDate):
        """
        The combination instrument is expired when all member expires.
        """
        memberInsOidList = [aelCombLink.member_insaddr.insaddr
                for aelCombLink in ael.CombinationLink.select(
                'owner_insaddr = {0}'.format(insOid))]
        for memberInsOid in sorted(memberInsOidList):
            if not self.isInsExpired(memberInsOid, strIsoDate):
                return False
        return True

    def __checkIfInsExpired(self, insOid, strIsoDate):

        aelIns = ael.Instrument[insOid]
        if not aelIns:
            return False
        # Check by generic
        if aelIns.generic:
            return False
        # Check by ins type
        if aelIns.instype == INS_TYPE_TEXT_CURR:
            return False
        elif aelIns.instype == INS_TYPE_TEXT_COMBINATION:
            return self.__checkIfCombInsExpired(insOid, strIsoDate)
        # Check by exp date
        expDate = aelIns.exp_day
        if not expDate:
            return False
        if aelIns.open_end == OPEN_END_STATUS_TEXT_OPEN_END:
            return False
        return expDate.to_string(ael.DATE_ISO)[:10] < strIsoDate[:10]

    def isInsExpired(self, insOid, strIsoDate):

        if insOid in self.__isExpiredCache:
            return self.__isExpiredCache[insOid]
        isInsExp = self.__checkIfInsExpired(insOid, strIsoDate)
        self.__isExpiredCache[insOid] = isInsExp
        return isInsExp
