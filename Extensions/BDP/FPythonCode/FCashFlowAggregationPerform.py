""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/cash_flow_agg/etc/FCashFlowAggregationPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE

    FCashFlowAggregationPerform.py - Cash flow aggregation implementation.

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""

# Import built-in modules
import collections
import string
import traceback

# Import Front modules
import acm
import ael

import FBDPCommon
import FBDPPerform


# The following table describes the classification of cash flow types.
#    +==============+=========================+============================+
#    |              | Fixed Amount Types      | Rates Types                |
#    +--------------+-------------------------+----------------------------+
#    | Aggregatable | Fixed Amount            | Fixed Rate                 |
#    | Types        | Interest Reinvestment   | Fixed Rate Adjustable      |
#    |              |                         | Float Rate                 |
#    |              |                         | Call Fixed Rate            |
#    |              |                         | Call Fixed Rate Adjustable |
#    |              |                         | Call Float Rate            |
#    +--------------+-------------------------+----------------------------+
#    | Aggregate    | Aggregated Fixed Amount | Aggregated Coupon          |
#    | Types        |                         |                            |
#    +==============+=========================+============================+
_CASH_FLOW_TYPE_AGGREGATED_FIXED_AMOUNT = 'Aggregated Fixed Amount'
_CASH_FLOW_TYPE_AGGREGATED_COUPON = 'Aggregated Coupon'
_CASH_FLOW_TYPE_REDEMPTION_AMOUNT = 'Redemption Amount'
_CASH_FLOW_TYPES_FIXED_AMOUNTS = ['Fixed Amount', 'Interest Reinvestment']
_CASH_FLOW_TYPES_FIXED_RATES = ['Fixed Rate', 'Fixed Rate Adjustable',
        'Call Fixed Rate', 'Call Fixed Rate Adjustable']
_CASH_FLOW_TYPES_FLOAT_RATES = ['Float Rate', 'Call Float Rate']
_CASH_FLOW_TYPES_RATES = (_CASH_FLOW_TYPES_FIXED_RATES +
        _CASH_FLOW_TYPES_FLOAT_RATES)
_CASH_FLOW_TYPES_AGGREGATABLES = (_CASH_FLOW_TYPES_FIXED_AMOUNTS +
        _CASH_FLOW_TYPES_RATES)
_CASH_FLOW_TYPES_AGGREGATES = [_CASH_FLOW_TYPE_AGGREGATED_FIXED_AMOUNT,
        _CASH_FLOW_TYPE_AGGREGATED_COUPON]
_CASH_FLOW_TYPES_PERIOD_DEFINED = (_CASH_FLOW_TYPES_AGGREGATES +
        _CASH_FLOW_TYPES_RATES)


_INCEPTION_DATE = '1970-01-01'


_LEG_TYPE_CALL_FIXED = 'Call Fixed'
_LEG_TYPE_CALL_FLOAT = 'Call Float'
_LEG_TYPE_CALL_FIXED_ADJUSTABLE = 'Call Fixed Adjustable'
_LEG_TYPES_CALLS = [_LEG_TYPE_CALL_FIXED, _LEG_TYPE_CALL_FLOAT,
        _LEG_TYPE_CALL_FIXED_ADJUSTABLE]


_RECORD_TYPE_ADDITIONAL_INFO = 'AdditionalInfo'
_RECORD_TYPE_CASH_FLOW = 'CashFlow'
_RECORD_TYPE_LEG = 'Leg'
_RECORD_TYPE_RESET = 'Reset'
_RECORD_TYPE_SETTLEMENT = 'Settlement'
_RECORD_TYPES_NO_ARCHIVE = ['Settlement']

_OUTCOME_OK = 'ok'
_OUTCOME_IGNORE = 'ignored'
_OUTCOME_FAIL = 'failed'

# If the instrument's trade which status contains the following keywords, the
# instrument will not be valid for cash flow aggregation.  The cash flow
# de-aggregation is always possible.
_TRADE_STATUS_KEYWORDS_INVALID_FOR_AGGREGATION = ['Void', 'Simulated',
        'Reserved']

_TRANSITIVE_ARCHIVE_FIND_DEPENDENTS_RECTYPE_OP_MAP = {
        # For additional info, find no dependent, so no operation.
        _RECORD_TYPE_ADDITIONAL_INFO: None,
        # For cash flow, find additional info and reset dependents.
        _RECORD_TYPE_CASH_FLOW: (lambda acmCF: [r for r in acmCF.Resets()] + [
                FBDPCommon.ael_to_acm(a) for a in
                FBDPCommon.acm_to_ael(acmCF).additional_infos()
                if a.archive_status == 0]),
        # For reset, find find no dependent, so no operation.
        _RECORD_TYPE_RESET: None
}

_TRANSITIVE_DEARCHIVE_FIND_DEPENDENTS_RECTYPE_OP_MAP = {
        # For additional info, find no dependent, so no operation.
        _RECORD_TYPE_ADDITIONAL_INFO: None,
        # For cash flow, find additional info and reset dependents.
        _RECORD_TYPE_CASH_FLOW: (lambda acmCF: [FBDPCommon.ael_to_acm(r) for
                r in FBDPCommon.acm_to_ael(acmCF).reference_in()
                if r.record_type == _RECORD_TYPE_RESET] + [
                FBDPCommon.ael_to_acm(a) for a in
                FBDPCommon.acm_to_ael(acmCF).additional_infos()]),
        # For reset, find no dependent, so no operation.
        _RECORD_TYPE_RESET: None
}


def perform(world, execParam):
    """
    """
    if not execParam['deaggregate']:
        r = _CashFlowAggregation(world)
    else:
        r = _CashFlowDeaggregation(world)
    r.perform(execParam)
    r.end()
    del r


class CashFlowAggregationCapturedError(Exception):
    """
    """
    def __init__(self, errMsg):
        """
        """
        self._errMsg = errMsg

    def __str__(self):
        """
        """
        return str(self._errMsg)


class CashFlowAggregationCalculateSettledInterestError(
        CashFlowAggregationCapturedError):
    """
    """
    def __init__(self, errMsg, cf, siParams):
        self._errMsg = errMsg
        cfOid = cf.Oid()
        tradeOid = siParams['trade'].Oid()
        currName = siParams['currency'].Name()
        self._errMsg += ('  Failed to calculate settled interest for a cash '
                'flow. (Cash flow id = {0}, trade id = {1} and currency name '
                '= {2})  Please consult the documentation FCA 4618 for help '
                'in diagnostics.'.format(cfOid, tradeOid, currName))


class _CashFlowAggregationBase(FBDPPerform.FBDPPerform):
    """
    This is the base class for _CashFlowAggregation and _CashFlowDeaggregation.
    Common code are placed in this class while individual subclass specialised
    for aggregation/deaggregation functionality.
    """

    def __init__(self, world):
        FBDPPerform.FBDPPerform.__init__(self, world)

    # For holding cash flow batch
    _CashFlowBatch = collections.namedtuple('_CashFlowBatch',
            'startDate endDate cfList')

    def _end(self):
        """
        """
        FBDPPerform.FBDPPerform._end(self)

    @staticmethod
    def _areTwoTradesMirrorTradesIfFalseGiveReason(trade1, trade2):
        """
        Test if the given two trades are a pair of mirror trades.  If true,
        return None; otherwise return the reason.
        """
        trade1Trdnbr = trade1.Oid()
        trade2Trdnbr = trade2.Oid()
        # Two references of the same trade by definition are not a pair of
        # mirror trades.
        if trade1Trdnbr == trade2Trdnbr:
            return ('The given two trades are references of the same trade '
                    '{0}, they are therefore not a pair of mirror '
                    'trades.'.format(trade1Trdnbr))
        # To be one of any mirror trade, a trade must have mirror trade number.
        trade1MirrorTrade = trade1.MirrorTrade()
        if not trade1MirrorTrade:
            return ('Trade {0} cannot be one of any mirror trade, as it lacks '
                    'of mirror trade number.'.format(trade1Trdnbr))
        trade2MirrorTrade = trade2.MirrorTrade()
        if not trade2MirrorTrade:
            return ('Trade {0} cannot be one of any mirror trade, as it lacks '
                    'of mirror trade number.'.format(trade2Trdnbr))
        trade1MirrorTrdnbr = trade1MirrorTrade.Oid()
        trade2MirrorTrdnbr = trade2MirrorTrade.Oid()
        # Find the main trade number.  If both trades' mirror trade number are
        # the same, this is the main trade's trade number.  If they are not
        # the same, the two trades are not mirrors.
        if trade1MirrorTrdnbr != trade2MirrorTrdnbr:
            return ('Trade {0} and trade {1} are not a pair of mirror trades, '
                    'as their mirror trade numbers ({2} and {3}, '
                    'respectively) are not the same.'.format(trade1Trdnbr,
                    trade2Trdnbr, trade1MirrorTrdnbr, trade2MirrorTrdnbr))
        mainTrdnbr = trade1MirrorTrdnbr
        # Either trade1 or trade2 is must be the main trade.  If not, they are
        # not mirror trades.
        if (trade1Trdnbr != mainTrdnbr and trade2Trdnbr != mainTrdnbr):
            return ('Trade {0} and trade {1} are not a pair of mirror trades, '
                    'as their common mirror trade number {2} does not refer '
                    'to either of them.'.format(trade1Trdnbr, trade2Trdnbr,
                    mainTrdnbr))
        # All passed, success and return None
        return None

    @staticmethod
    def _infraGetNonArchivedConfOidListByCashFlowOid(cfOid):
        q = 'SELECT seqnbr FROM confirmation WHERE cfwnbr = {0} and archive_status = 0'.format(cfOid)
        return [row[0] for row in ael.dbsql(q)[0]]

    @staticmethod
    def _infraGetNonArchivedSettlOidListByCashFlowOid(cfOid):
        q = 'SELECT seqnbr FROM settlement WHERE cfwnbr = {0} and archive_status = 0'.format(cfOid)
        return [row[0] for row in ael.dbsql(q)[0]]

    @staticmethod
    def _infraGetJournalInformationOidListByCashFlowOid(cfOid):
        q = 'SELECT seqnbr FROM journal_information WHERE cfwnbr = {0}'.format(
                cfOid)
        return [row[0] for row in ael.dbsql(q)[0]]

    @staticmethod
    def _infraGetConfirmationOidListByResetOid(rstOid):
        q = 'SELECT seqnbr FROM confirmation WHERE reset_resnbr = {0}'.format(
                rstOid)
        return [row[0] for row in ael.dbsql(q)[0]]

    @staticmethod
    def _calculateInstrumentFunding(ins, trade, valuationEndDate):
        calcMths = acm.FCalculationMethods()
        spaceCollection = calcMths.CreateStandardCalculationsSpaceCollection()
        insCalc = ins.Calculation()
        funding = insCalc.Funding(spaceCollection, trade.Portfolio(),
                _INCEPTION_DATE, valuationEndDate, trade.Currency(),
                trade.Currency(), 'None')
        return funding

    @staticmethod
    def _findUniqueTransitiveDependentList(objList, findRecTypeFunc,
            recTypeOpMap):
        """
        """
        processedList = []
        inProcessList = []
        uniqueObjSet = set()     # fast look-up
        # Initialise the in-process list.  Last element process first.
        for obj in objList:
            if obj and obj not in uniqueObjSet:
                inProcessList.append(obj)
                uniqueObjSet.add(obj)
        inProcessList.reverse()
        # Take the last element out of the in-process list, process it and put
        # it into the processed list.  Do this until there is no more element
        # in the in-process list.  For each element taken out, find the unique
        # dependents and push them unto the in-process list.
        while inProcessList:
            # pop the object
            obj = inProcessList.pop()
            recType = findRecTypeFunc(obj)
            if recType in list(recTypeOpMap.keys()):
                recTypeOp = recTypeOpMap[recType]
                # Find the corresponding operation for this record type.  Then
                # apply the operation to obtain the dependent list.  Finally
                # make the dependent list unique.
                if recTypeOp:
                    depObjList = recTypeOp(obj)
                    uniqueDepObjList = [depObj for depObj in depObjList
                                               if depObj not in uniqueObjSet]
                else:
                    # Don't have the recTypeOp to find dependents, so there
                    # won't be any.
                    uniqueDepObjList = None
            else:
                # Can't find the specific recType, so we are not looking for
                # its dependents.
                uniqueDepObjList = None
            # If there is the unique dependent list, insert it into the overall
            # unique list.
            while uniqueDepObjList:
                depObj = uniqueDepObjList.pop()
                inProcessList.append(depObj)
                uniqueObjSet.add(depObj)
            # Finished processing this object, add it to the processed list.
            processedList.append(obj)
        return processedList

    @staticmethod
    def _isAggregatesCashFlowDatesInPeriod(cfStartDate, cfEndDate,
            periodStartDate, periodEndDate):
        """
        """
        cfStartDate = str(cfStartDate)
        cfEndDate = str(cfEndDate)
        periodStartDate = str(periodStartDate)
        periodEndDate = str(periodEndDate)
        isStartDateInPeriod = ((periodStartDate <= cfStartDate) and
                (cfStartDate < periodEndDate))
        isEndDateInPeriod = ((periodStartDate < cfEndDate) and
                (cfEndDate <= periodEndDate))
        if isStartDateInPeriod != isEndDateInPeriod:
            raise ValueError('Not expecting the cash flow (from {0} to {1}) '
                    'to be partially overlap the period (from {2} to '
                    '{3}).'.format(cfStartDate, cfEndDate, periodStartDate,
                    periodEndDate))
        return isEndDateInPeriod

    @staticmethod
    def _isAggregatesCashFlowInPeriod(cf, periodStartDate, periodEndDate):
        """
        """
        cfType = cf.CashFlowType()
        if cfType not in _CASH_FLOW_TYPES_AGGREGATES:
            return False
        cfStartDate = cf.StartDate()
        cfEndDate = cf.EndDate()
        return _CashFlowAggregationBase._isAggregatesCashFlowDatesInPeriod(
                cfStartDate, cfEndDate, periodStartDate, periodEndDate)

    @staticmethod
    def _isAggregatablesCashFlowInPeriod(cf, periodStartDate, periodEndDate):
        """
        """
        cfType = cf.CashFlowType()
        if cfType in _CASH_FLOW_TYPES_FIXED_AMOUNTS:
            cfPayDate = cf.PayDate()
            if not cfPayDate:
                raise ValueError('Cash flow expected to have pay date. '
                        '{0}'.format(cf))
            return (_CashFlowAggregationBase.
                    _isFixedAmountsCashFlowDatesInPeriod(cfPayDate,
                    periodStartDate, periodEndDate))
        elif cfType in _CASH_FLOW_TYPES_RATES:
            cfStartDate = cf.StartDate()
            cfEndDate = cf.EndDate()
            if not cfStartDate:
                raise ValueError('Cash flow expected to have start date. '
                        '{0}'.format(cf))
            if not cfEndDate:
                raise ValueError('Cash flow expected to have end date. '
                        '{0}'.format(cf))
            return _CashFlowAggregationBase._isRatesCashFlowDatesInPeriod(
                    cfStartDate, cfEndDate, periodStartDate, periodEndDate)
        else:
            return False

    @staticmethod
    def _isFixedAmountsCashFlowDatesInPeriod(cfPayDate, periodStartDate,
            periodEndDate):
        """
        """
        cfPayDate = str(cfPayDate)
        periodStartDate = str(periodStartDate)
        periodEndDate = str(periodEndDate)
        return periodStartDate < cfPayDate and cfPayDate <= periodEndDate

    @staticmethod
    def _isRatesCashFlowDatesInPeriod(cfStartDate, cfEndDate, periodStartDate,
            periodEndDate):
        """
        """
        cfStartDate = str(cfStartDate)
        cfEndDate = str(cfEndDate)
        periodStartDate = str(periodStartDate)
        periodEndDate = str(periodEndDate)
        isStartDateInPeriod = ((periodStartDate <= cfStartDate) and
                (cfStartDate < periodEndDate))
        isEndDateInPeriod = ((periodStartDate < cfEndDate) and
                (cfEndDate <= periodEndDate))
        if isStartDateInPeriod != isEndDateInPeriod:
            raise ValueError('Not expecting the cash flow to be partially '
                    'overlap the period (from {0} to {1}).'.format(
                    periodStartDate, periodEndDate))
        return isEndDateInPeriod

    def _isTradeValidForAggregationByTradeStatus(self, trade):
        tradeStatus = trade.Status()
        for statusKeyword in _TRADE_STATUS_KEYWORDS_INVALID_FOR_AGGREGATION:
            if statusKeyword in tradeStatus:
                return False
        return True

    def _logObjInDebug(self, strPrepend, obj):
        """
        Simple pretty print each acm object into a one-liner.
        """
        objStr = str(obj)
        objStr = string.replace(objStr, '\n', '\t')
        self._logDebug('{0}{1}'.format(strPrepend, objStr))

    def _logObjListInDebug(self, strPrepend, objList):
        """
        Simple pretty print each acm object into a one-liner.
        """
        for obj in objList:
            self._logObjInDebug(strPrepend, obj)

    def _perform(self, execParam):
        """
        Shared main functionality body for the subclasses.
        """
        # VALIDATE phase
        self._logInfo('Validating environment and parameters...')
        self._validateMode()
        if self._hasAnyErrorMessage():
            self._listTopWarningMessages()
            self._listTopErrorMessages()
            return
        # ACQUIRING PARAMETER phase
        self._logInfo('Acquiring run parameters...')
        runParamList = self.__acquireRunParameter(execParam)
        if self._hasAnyErrorMessage():
            self._listTopWarningMessages()
            self._listTopErrorMessages()
            return
        # INSPECTION AND PROCESS phase
        toInspectQueue = collections.deque(runParamList)
        inspectedFailedList = []
        toProcessQueue = collections.deque()
        processedFailedList = []
        processedIgnoredList = []
        processedSuccessList = []
        numTotalToIter = len(runParamList)
        numInspected = 0
        numProcessed = 0
        while True:
            if not toInspectQueue and not toProcessQueue:
                break
            if toInspectQueue:
                runParam = toInspectQueue.popleft()
                self._logInfo('Inspecting ... {0}'.format(
                        self.__getRunParamLabel(runParam)))
                self.__inspect(inspectedFailedList, toProcessQueue, runParam)
                numInspected += 1
                self._logDebug('[Total={0}][Inspect:fail={1},success={2}]'
                        '[Process:fail={3},ignore={4},success={5}]'.format(
                        numTotalToIter, len(inspectedFailedList),
                        (numInspected - len(inspectedFailedList)),
                        len(processedFailedList), len(processedIgnoredList),
                        len(processedSuccessList)))
            if toProcessQueue:
                inspectionReport = toProcessQueue.popleft()
                self.__process(processedFailedList,
                        processedIgnoredList, processedSuccessList,
                        inspectionReport)
                numProcessed += 1
                self._logDebug('[Total={0}][Inspect:fail={1},success={2}]'
                        '[Process:fail={3},ignore={4},success={5}]'.format(
                        numTotalToIter, len(inspectedFailedList),
                        (numInspected - len(inspectedFailedList)),
                        len(processedFailedList), len(processedIgnoredList),
                        len(processedSuccessList)))
        # Finalise
        self._listTopWarningMessages()
        self._listTopErrorMessages()
        return

    def _processLegBatchUpCashFlowsToProcess(self, leg, lastCFAggDate,
            alignedAggDate, cfsToProcess):
        """
        """
        raise NotImplementedError('Must be overridden in the subclass.')

    def _processLegFindCashFlowToProcess(self, leg, lastCFAggDate,
            alignedAggDate):
        """
        """
        raise NotImplementedError('Must be overridden in the subclass.')

    def _processLegProcessBatches(self, leg, trade, cfsBatchList):
        """
        """
        raise NotImplementedError('Must be overridden in the subclass.')

    def _validateMode(self):
        """
        """
        if acm.ArchivedMode():
            errMsg = 'This script must not be run in the Archived mode.'
            self._logError(errMsg)
        if acm.IsHistoricalMode():
            errMsg = 'This script must not be run in the Historical mode.'
            self._logError(errMsg)
        return

    # For holding data structure among loops.
    __InspectionReport = collections.namedtuple('__InspectionReport',
            'ins legInspectionSubReports insProcParam')

    __InsProcParam = collections.namedtuple('__InsProcParam',
            'startDate firstValidTradeByTradeStatus')

    __LegInspectionSubReport = collections.namedtuple(
            '__LegInspectionSubReport', 'leg legProcParam')

    __LegProcessSubReport = collections.namedtuple('__LegProcessSubReport',
            'leg outcome')

    __LegProcParam = collections.namedtuple('__LegProcParam',
            'lastCFAggDate firstRACFPayDate alignedAggDate')

    __ProcessReport = collections.namedtuple('__ProcessReport',
            'ins legProcessSubReports')

    __RunParam = collections.namedtuple('__RunParam',
            'ins todayDate requestedAggDate isFundingEnabled')

    def __acquireRunParameter(self, execParam):
        """
        The ACQUIRING RUN PARAMETER phase of the perform()
        """
        insts = self.__acquireRunParameterInstruments(execParam)
        todayDate = acm.Time.DateToday()
        requestedAggDate = self.__acquireRunParameterAggregationDate(execParam)
        isFundingEnabled = self.__acquireRunParameterIsFundingEnabled(
                execParam)
        runParamList = []
        for ins in insts:
            runParamList.append(self.__RunParam(ins=ins,
                    todayDate=todayDate,
                    requestedAggDate=requestedAggDate,
                    isFundingEnabled=isFundingEnabled))
        return runParamList

    def __acquireRunParameterAggregationDate(self, execParam):
        """
        Obtain (and sanitise) the aggregation date from the param.
        """
        requestedAggDate = execParam['date']
        todayDate = acm.Time.DateToday()
        if requestedAggDate > todayDate:
            warnMsg = ('Aggregation date requested ({0}) in future is not '
                    'allowed.  Set it back to today.'.format(requestedAggDate,
                    todayDate))
            self._logWarning(warnMsg)
            requestedAggDate = todayDate
        self._logInfo('Aggregation date is {0}'.format(requestedAggDate))
        return requestedAggDate

    def __acquireRunParameterInstruments(self, execParam):
        """
        Obtain instrument's in the form of acm.FInstrument.
        """
        insts = []
        for insOid in execParam['instruments']:
            ins = acm.FInstrument[insOid]
            if ins:
                insts.append(ins)
            else:
                errMsg = ('Unable to convert oid {0} to acm '
                        'instrument.'.format(insOid))
                self._logError(errMsg)
        return insts

    def __acquireRunParameterIsFundingEnabled(self, execParam):
        """
        Obtain from the valuation parameter is the funding enabled.
        """
        valParam = acm.ObjectServer().UsedValuationParameters()
        return (not valParam.DisableFunding())

    def __findAlignedAggDate(self, leg, requestedAggDate, firstRACFPayDate):
        """
        Note, this method is correlated with
        __inspectInstrumentLegAlignedAggregationDateProperlySet().
        """
        # Find the practical aggregation date
        practicalAggDate = requestedAggDate
        if firstRACFPayDate and firstRACFPayDate < requestedAggDate:
            practicalAggDate = firstRACFPayDate
        # Find non-aggregated cash flow that have defined start and end dates.
        periodDefinedCFs = [cf for cf in leg.CashFlows()
                if cf.CashFlowType() in _CASH_FLOW_TYPES_PERIOD_DEFINED]
        # Find cash flow overlapped with requestedAggDate
        periodOverlappedCFs = [cf for cf in periodDefinedCFs
                if ((cf.StartDate() <= practicalAggDate) and
                (cf.EndDate() > practicalAggDate))]
        # No overlapped cash flow, the current practical aggregation date okay.
        if not periodOverlappedCFs:
            return practicalAggDate
        # Only one overlapped cash flows
        candidateAlignedAggDates = list({cf.StartDate() for cf in
                periodOverlappedCFs})
        if len(candidateAlignedAggDates) == 1:
            return candidateAlignedAggDates[0]
        else:
            return _INCEPTION_DATE

    def __findFirstRedemptionAmountCashFlowPayDate(self, leg):
        """
        Given all cash flows, find the first 'Redemption Amount' cash flow pay
        date.  Return None if there was no aggregates at all.
        """
        racfPayDates = [str(cf.PayDate()) for cf in leg.CashFlows()
                if cf.CashFlowType() == _CASH_FLOW_TYPE_REDEMPTION_AMOUNT]
        if racfPayDates:
            firstRACFPayDate = min(racfPayDates)
        else:
            firstRACFPayDate = None
        return firstRACFPayDate

    def __findInsProcParam(self, ins, runParam):
        """
        """
        theTrade = self.__findFirstValidTradeForAggregationByTradeStatus(ins)
        insProcParam = self.__InsProcParam(startDate=ins.StartDate(),
                firstValidTradeByTradeStatus=theTrade)
        return insProcParam

    def __findLastCashFlowAggregationDate(self, leg, insStartDate):
        """
        Given all cash flows, find the last cash flow aggregation date.  If
        there was no aggregates at all, return either inception date or
        instrument start date, whichever is later.
        """
        cfAggDates = [str(cf.PayDate()) for cf in leg.CashFlows() if
                cf.CashFlowType() == _CASH_FLOW_TYPE_AGGREGATED_FIXED_AMOUNT]
        if cfAggDates:
            lastCFAggDate = max(cfAggDates)
        else:
            lastCFAggDate = max(_INCEPTION_DATE, insStartDate)
        return lastCFAggDate

    def __findLegProcParam(self, leg, runParam, insProcParam):
        """
        """
        # Find the last cash flow aggregation date.  If nil, use the inception
        lastCFAggDate = self.__findLastCashFlowAggregationDate(leg,
                insProcParam.startDate)
        firstRACFPayDate = self.__findFirstRedemptionAmountCashFlowPayDate(leg)
        alignedAggDate = self.__findAlignedAggDate(leg,
                runParam.requestedAggDate, firstRACFPayDate)
        return self.__LegProcParam(lastCFAggDate=lastCFAggDate,
                firstRACFPayDate=firstRACFPayDate,
                alignedAggDate=alignedAggDate)

    def __findFirstValidTradeForAggregationByTradeStatus(self, ins):
        """
        Find the first valid trade for aggregation.  A valid trades have trade
        status which name contains keywords defined in
        _TRADE_STATUS_KEYWORDS_INVALID_FOR_AGGREGATION.
        """
        trades = sorted([trade for trade in ins.Trades() if trade.Oid() > 0],
                key=lambda trade: trade.Oid())
        for trade in trades:
            if self._isTradeValidForAggregationByTradeStatus(trade):
                return trade
        return None

    def __getRunParamLabel(self, runParam):
        """
        """
        return runParam.ins.Name()

    def __inspect(self, inspectFailedList, inspectSuccessQueue, runParam):
        """
        """
        numErrMsgsBefore = self._countErrorMessages()
        ins = runParam.ins
        # Inspect instrument except leg.
        insProcParam = self.__findInsProcParam(ins, runParam)
        self.__inspectInstrumentAllExceptLegs(ins, runParam, insProcParam)
        # Only proceed to inspect instrument legs if there is no error message
        legInspectionSubReportList = []
        if self._countErrorMessages() == numErrMsgsBefore:
            allLegs = sorted([leg for leg in ins.Legs()])
            for leg in allLegs:
                legProcParam = self.__findLegProcParam(leg, runParam,
                        insProcParam)
                self.__inspectInstrumentLeg(leg, runParam, insProcParam,
                        legProcParam)
                legInspectionSubReportList.append(
                        self.__LegInspectionSubReport(leg=leg,
                        legProcParam=legProcParam))
        # instrument report
        inspectionReport = self.__InspectionReport(ins=ins,
                legInspectionSubReports=legInspectionSubReportList,
                insProcParam=insProcParam)
        # If there is any error message, send the report to the failed queue;
        # otherwise (i.e. no error message at all) the success queue
        if self._countErrorMessages() > numErrMsgsBefore:
            inspectFailedList.append(inspectionReport)
            self._summaryAddFail(ins.RecordType(), ins.Oid(), 'INSPECT',
                    self._retrieveErrorMessagesAfter(numErrMsgsBefore))
        else:
            inspectSuccessQueue.append(inspectionReport)
            self._summaryAddOk(ins.RecordType(), ins.Oid(), 'INSPECT')

    def __inspectInstrumentAllExceptLegs(self, ins, runParam, insProcParam):
        """
        Inspect all about the instrument except its legs.
        """
        # Check instrument type.
        self.__inspectInstrumentType(ins, runParam, insProcParam)
        # Check instrument start date
        self.__inspectInstrumentStartDateExist(ins, runParam, insProcParam)
        # Checking instrument number of trades
        self.__inspectInstrumentAllTrades(ins, runParam, insProcParam)
        # Checking instrument number of legs
        self.__inspectInstrumentNumLegs(ins, runParam, insProcParam)
        # Checking instrument had funding or not
        self.__inspectInstrumentHasFunding(ins, runParam, insProcParam)

    def __inspectInstrumentAllTrades(self, ins, runParam, insProcParam):
        """
        Inspect all trades of the instrument.
        """
        return self._doInspectInstrumentAllTrades(ins,
                insProcParam.firstValidTradeByTradeStatus)

    def __inspectInstrumentLeg(self, leg, runParam, insProcParam,
            legProcParam):
        """
        Inspect the leg of the instrument.
        """
        # Check leg type
        self.__inspectInstrumentLegType(leg)
        # Inspect cash flows
        allCFs = [cf for cf in leg.CashFlows() if cf.PayDate() < runParam.requestedAggDate]
        for cf in allCFs:
            # Check the cash flow.
            self.__inspectInstrumentLegCashFlow(cf, runParam, insProcParam,
                    legProcParam)
        # Check leg's first redemption amount cash flow pay date against
        # aggregation date
        self.__inspectInstrumentLegFirstRACFPayDateAgainstAggDate(leg,
                runParam, insProcParam, legProcParam)
        # Check the leg's aligned aggregation date had been set properly.
        self.__inspectInstrumentLegAlignedAggregationDateProperlySet(leg,
                runParam, insProcParam, legProcParam)

    def __inspectInstrumentLegCashFlow(self, cf, runParam, insProcParam,
            legProcParam):
        """
        Check the cash flow on the instrument's leg.
        """
        # Check cash flow dates are on or after the instrument start date.
        self.__inspectInstrumentLegCashFlowDatesNotBeforeInsStartDate(cf,
                runParam, insProcParam, legProcParam)
        # Check float rates cash flows' resets have non-zero values
        self.__inspectInstrumentLegCashFlowFloatRateInPastResetsAllFixed(cf,
                runParam, insProcParam, legProcParam)
        # Check the cash flow has no confirmation attached.
        self.__inspectInstrumentLegCashFlowNoConfirmationAttached(cf,
                runParam, insProcParam, legProcParam)
        # Check the cash flow has no settlement attached
        self.__inspectInstrumentLegCashFlowNoClosedSettlementAttached(cf,
                runParam, insProcParam, legProcParam)
        # Check the cash flow has no journal information attached
        self.__inspectInstrumentLegCashFlowNoJournalInformationAttached(cf,
                runParam, insProcParam, legProcParam)
        # Inspect resets
        allRSTs = [rst for rst in cf.Resets()]
        for rst in allRSTs:
        # Check float rates cash flows' resets have non-zero values
            self.__inspectInstrumentLegCashFlowReset(rst, runParam,
                    insProcParam, legProcParam)

    def __inspectInstrumentLegCashFlowReset(self, rst, runParam, insProcParam,
            legProcParam):
        """
        Check the reset on the cash flow of the instrument's leg.
        """
        # Find confirmations on this reset.  If any, report!
        cfmOidList = self._infraGetConfirmationOidListByResetOid(rst.Oid())
        if cfmOidList:
            errMsg = ('Reset {0} of Cash flow {1} of Leg {2} of Instrument '
                    '{3} has confirmations {4} attached.'.format(rst.Oid(),
                    rst.CashFlow().Oid(), rst.CashFlow().Leg().Oid(),
                    rst.CashFlow().Leg().Instrument().Name(), cfmOidList))
            self._logError(errMsg)

    def __inspectInstrumentLegAlignedAggregationDateProperlySet(self, leg,
            runParam, insProcParam, legProcParam):
        """
        Check the aligned aggregation date for the instrument leg is properly
        check.  Situation is different for both case of aggregation and
        de-aggregation, hence dealt with separately in the subclass.
        Note, this method is correlated with __findAlignedAggDate()
        """
        self._doInspectLegAlignedAggregationDateProperlySet(
                runParam.requestedAggDate, legProcParam.firstRACFPayDate,
                legProcParam.alignedAggDate)

    def __inspectInstrumentLegCashFlowDatesNotBeforeInsStartDate(self, cf,
            runParam, insProcParam, legProcParam):
        """
        Inspect the cash flow's dates, and returns error messages.  If the cash
        flow has start date, end date or pay date before the instrument's start
        date, generate an error message.
        """
        # Finding useful bits
        insStartDate = insProcParam.startDate
        # Check cash flow start/end/pay dates all on or after instrument start
        # date.
        # Start date
        cfStartDate = cf.StartDate()
        if cfStartDate and cfStartDate < insStartDate:
            errMsg = ('Cash flow {0} (Type {1}) of Leg {2} of Instrument {3} '
                    'has start date {4} before the instrument start date '
                    '{5}'.format(cf.Oid(), cf.CashFlowType(), cf.Leg().Oid(),
                    cf.Leg().Instrument().Name(), cfStartDate, insStartDate))
            self._logError(errMsg)
        # End date
        cfEndDate = cf.EndDate()
        if cfEndDate and cfEndDate < insStartDate:
            errMsg = ('Cash flow {0} (Type {1}) of Leg {2} of Instrument {3} '
                    'has end date {4} before the instrument start date '
                    '{5}'.format(cf.Oid(), cf.CashFlowType(), cf.Leg().Oid(),
                    cf.Leg().Instrument().Name(), cfEndDate, insStartDate))
            self._logError(errMsg)
        # Pay date
        cfPayDate = cf.PayDate()
        if cfPayDate and cfPayDate < insStartDate:
            errMsg = ('Cash flow {0} (Type {1}) of Leg {2} of Instrument {3} '
                    'has pay date {4} before the instrument start date '
                    '{5}'.format(cf.Oid(), cf.CashFlowType(), cf.Leg().Oid(),
                    cf.Leg().Instrument().Name(), cfPayDate, insStartDate))
            self._logError(errMsg)

    def __inspectInstrumentLegCashFlowFloatRateInPastResetsAllFixed(self, cf,
            runParam, insProcParam, legProcParam):
        """
        Inspect the cash flow.  Situation are different between aggregtion and
        de-aggregation.  Call the handling function in the aggregation and
        de-aggregation subclass.
        """
        return self._doInspectPastFloatRateCashFlowResetsAllFixed(cf,
                runParam.requestedAggDate)

    def __inspectInstrumentLegCashFlowNoConfirmationAttached(self, cf,
            runParam, insProcParam, legProcParam):
        """
        Check the cash flow in the instrument's leg has no non archived
        confirmation objects attached.
        """
        # Find confirmations on this cash flow.  If any, report!
        cfmOidList = self._infraGetNonArchivedConfOidListByCashFlowOid(cf.Oid())
        if cfmOidList:
            errMsg = ('Cash flow {0} of Leg {1} of Instrument {2} has '
                    'non archived confirmations {3} attached.'.format(cf.Oid(),
                    cf.Leg().Oid(), cf.Leg().Instrument().Name(), cfmOidList))
            self._logError(errMsg)

    def __inspectInstrumentLegCashFlowNoClosedSettlementAttached(self, cf,
            runParam, insProcParam, legProcParam):
        """
        Check the cash flow in the instrument's leg has non archived
        settlement objects attached.
        """
        # Find settlements on this cash flow.  If any, report!
        stmOidList = self._infraGetNonArchivedSettlOidListByCashFlowOid(cf.Oid())
        if stmOidList:
            errMsg = ('Cash flow {0} of Leg {1} of Instrument {2} has '
                    ' non archived settlements {3} attached'.format(cf.Oid(),
                    cf.Leg().Oid(), cf.Leg().Instrument().Name(), stmOidList))
            self._logError(errMsg)

    def __inspectInstrumentLegCashFlowNoJournalInformationAttached(self, cf,
            runParam, insProcParam, legProcParam):
        """
        Check the cash flow in the instrument's leg has no journal information
        attached.
        """
        # Find journal informations on this cash flow.  If any, report!
        jiOidList = self._infraGetJournalInformationOidListByCashFlowOid(
                cf.Oid())
        if jiOidList:
            errMsg = ('Cash flow {0} of Leg {1} of Instrument {2} has journal '
                    'informations {3} attached.'.format(cf.Oid(),
                    cf.Leg().Oid(), cf.Leg().Instrument().Name(), jiOidList))
            self._logError(errMsg)

    def __inspectInstrumentLegFirstRACFPayDateAgainstAggDate(self, leg,
            runParam, insProcParam, legProcParam):
        """
        """
        # Find useful bits
        requestedAggDate = runParam.requestedAggDate
        firstRACFPayDate = legProcParam.firstRACFPayDate
        # Check requested aggregation date against firstRACFPayDate
        if firstRACFPayDate and firstRACFPayDate < requestedAggDate:
            warnMsg = ('The aggregate date for instrument {0} leg {1} is '
                    'moved early from {2} to {3}.  The leg has a \'Redemption '
                    'Amount\' cash flow pay date on {3}.'.format(
                    leg.Instrument().Name(), leg.Oid(), requestedAggDate,
                    firstRACFPayDate))
            self._logWarning(warnMsg)

    def __inspectInstrumentHasFunding(self, ins, runParam, insProcParam):
        return self._doInspectInstrumentHasFunding(runParam.isFundingEnabled,
                ins, insProcParam.firstValidTradeByTradeStatus,
                runParam.todayDate)

    def __inspectInstrumentLegType(self, leg):
        """
        Inspect the given instrument and returns error message.  The leg type
        is expected to be one of the 'Call Fixed', 'Call Float', 'Call Fixed
        Adjustable'.    """
        # Check instrument leg type
        legType = leg.LegType()
        if legType not in _LEG_TYPES_CALLS:
            errMsg = ('Leg \'{0}\' of instrument \'{1}\' is not of an '
                    'accepted leg type ({2}).  ''Accepted leg types are '
                    '{3}.'.format(leg.Oid(), leg.Instrument().Name(), legType,
                                  ', '.join(_LEG_TYPES_CALLS)))
            self._logError(errMsg)

    def __inspectInstrumentNumLegs(self, ins, runParam, insProcParam):
        """
        Inspect the instrument and check number of legs.
        """
        # Check there is only one leg.
        legs = ins.Legs()
        numLegs = len(legs)
        if numLegs != 1:
            errMsg = ('The cash flow instrument \'{0}\' should only have one '
                    'leg, but there are {1}: {2}.'.format(ins.Name(), numLegs,
                    legs))
            self._logError(errMsg)

    def __inspectInstrumentStartDateExist(self, ins, runParam, insProcParam):
        """
        Inspect instrument and check instrument's start date exists.
        """
        # Finding useful bits
        insStartDate = insProcParam.startDate
        # Check instrument has start date.
        if not insStartDate:
            errMsg = 'The instrument {0} start date cannot be found.'.format(
                    ins.Name())
            self._logError(errMsg)

    def __inspectInstrumentType(self, ins, runParam, insProcParam):
        """
        Inspect the given instrument and returns error message.  The instrument
        is expected to be an acm object, which should be of the type FDeposit
        (and must be a call deposit).
        """
        # Check instrument type
        if ins.IsKindOf('FDeposit'):
            if ins.OpenEnd() == 'None':
                errMsg = 'Instrument {0} is not a call deposit.'.format(
                        ins.Name())
                self._logError(errMsg)
        else:
            errMsg = ('The given instrument {0} is not of the right '
                    'instrument type.'.format(ins.Name()))
            self._logError(errMsg)

    def __process(self, processedFailedList, processedIgnoredList,
            processedSuccessList, inspectionReport):
        """
        """
        ins = inspectionReport.ins
        trade = inspectionReport.insProcParam.firstValidTradeByTradeStatus
        self._logInfo('Processing instrument \'{0}\' ...'.format(ins.Name()))
        legProcessSubReportList = []
        anyLegFailed = False
        for legInspectionSubReport in inspectionReport.legInspectionSubReports:
            leg = legInspectionSubReport.leg
            self._logInfo('    processing leg \'{0}\' ...'.format(leg.Oid()))
            if anyLegFailed:
                legOutcome = _OUTCOME_IGNORE
                legWarnMsg = ('Instrument {0} leg {1} ignored due to an '
                        'earlier leg processing failure in the same '
                        'instrument.'.format(leg.Instrument().Name(),
                        leg.Oid()))
                self._logWarning(legWarnMsg)
                self._summaryAddIgnore(leg.RecordType(), leg.Oid(), 'PROCESS',
                        [legWarnMsg])
                legProcessSubReport = self.__LegProcessSubReport(leg=leg,
                        outcome=legOutcome)
                legProcessSubReportList.append(legProcessSubReport)
            else:
                numErrMsgsBefore = self._countErrorMessages()
                numWarnMsgsBefore = self._countWarningMessages()
                legOutcome = self.__processLeg(leg, trade,
                        legInspectionSubReport.legProcParam.lastCFAggDate,
                        legInspectionSubReport.legProcParam.alignedAggDate)
                if self._countErrorMessages() > numErrMsgsBefore:
                    anyLegFailed = True
                    self._summaryAddFail(leg.RecordType(), leg.Oid(),
                            'PROCESS',
                            self._retrieveErrorMessagesAfter(numErrMsgsBefore))
                elif self._countWarningMessages() > numWarnMsgsBefore:
                    self._summaryAddIgnore(leg.RecordType(), leg.Oid(),
                            'PROCESS', self._retrieveWarningMessagesAfter(
                            numWarnMsgsBefore))
                else:
                    self._summaryAddOk(leg.RecordType(), leg.Oid(), 'PROCESS')
                legProcessSubReport = self.__LegProcessSubReport(leg=leg,
                        outcome=legOutcome)
                legProcessSubReportList.append(legProcessSubReport)
            self._logInfo('    processed  leg \'{0}\' ... {1}'.format(
                    leg.Oid(), legOutcome))
        # Determine the outcome for the instrument.  If any leg had failed,
        # then the out come is failed.  If none leg has failed, and there is
        # at least one success, then the out come is success.  Otherwise (i.e.
        # none failed but none success, must be all ignored) the outcome is
        # success.
        if anyLegFailed:
            insOutcome = _OUTCOME_FAIL
        else:
            anyLegSuccess = False
            for legProcessSubReport in legProcessSubReportList:
                if legProcessSubReport.outcome == _OUTCOME_OK:
                    anyLegSuccess = True
            if anyLegSuccess:
                insOutcome = _OUTCOME_OK
            else:
                insOutcome = _OUTCOME_IGNORE
        # Make the process report
        processReport = self.__ProcessReport(ins=ins,
                legProcessSubReports=legProcessSubReportList)
        # Depending on the instrument outcome, report into the summary.
        if insOutcome == _OUTCOME_FAIL:
            errMsg = ('Instrument {0} failed because one of the legs cannot '
                    'be processed.'.format(ins.Oid()))
            self._logError(errMsg)
            self._summaryAddFail(ins.RecordType(), ins.Oid(), 'PROCESS',
                    [errMsg])
            processedFailedList.append(processReport)
        elif insOutcome == _OUTCOME_IGNORE:
            warnMsg = ('Instrument {0} ignored because all legs have been '
                    'ignored.'.format(ins.Oid()))
            self._logWarning(warnMsg)
            self._summaryAddIgnore(ins.RecordType(), ins.Oid(), 'PROCESS',
                    [warnMsg])
            processedIgnoredList.append(processReport)
        else:  # i.e. insOutcome == _OUTCOME_OK
            self._summaryAddOk(leg.RecordType(), leg.Oid(), 'PROCESS')
            processedSuccessList.append(processReport)
        self._logInfo('Processed  instrument \'{0}\' ... {1}'.format(
                ins.Name(), insOutcome))

    def __processLeg(self, leg, trade, lastCFAggDate, alignedAggDate):
        """
        """
        numErrMsgsBefore = self._countErrorMessages()
        self._logDebug('        Processing instrument {0} leg {1} (last '
                  'aggregated on {2}) with aligned aggregation date '
                  '{3}'.format(leg.Instrument().Name(), leg.Oid(),
                  lastCFAggDate, alignedAggDate))
        # For the leg, find cash flow to process
        try:
            cfsToProcess = self._processLegFindCashFlowToProcess(leg,
                    lastCFAggDate, alignedAggDate)
            self._logObjListInDebug('            ', cfsToProcess)
        except CashFlowAggregationCapturedError as cface:
            errMsg = str(cface)
            self._logError(errMsg)
        except Exception as e:
            # Always do trace back as soon as the exception is handled.
            for tbLine in traceback.format_stack():
                self._logNoTime(tbLine)
            errMsg = str(e)
            # Log warning/error when exception is not going to be re-raised
            self._logError(errMsg)
        # If any error message, return.
        if self._countErrorMessages() > numErrMsgsBefore:
            outcome = _OUTCOME_FAIL
            return outcome
        # If there is no cash flow to process, put a warning message
        if not cfsToProcess:
            self._logDebug('        No cash flow to be processed.')
            warnMsg = ('Instrument {0} leg {1} has no cash flow to be '
                    'processed.'.format(leg.Instrument().Name(), leg.Oid()))
            self._logWarning(warnMsg)
            outcome = _OUTCOME_IGNORE
            return outcome
        # Batch up cash flow to process
        try:
            cfsBatchList = self._processLegBatchUpCashFlowsToProcess(leg,
                    lastCFAggDate, alignedAggDate, cfsToProcess)
            self._processLegProcessBatches(leg, trade, cfsBatchList)
        except CashFlowAggregationCapturedError as cface:
            errMsg = str(cface)
            self._logError(errMsg)
        except Exception as e:
            # Always do trace back as soon as the exception is handled.
            for tbLine in traceback.format_stack():
                self._logNoTime(tbLine)
            errMsg = str(e)
            # Log warning/error when exception is not going to be re-raised
            self._logError(errMsg)
        # If any error message, return.
        if self._countErrorMessages() > numErrMsgsBefore:
            outcome = _OUTCOME_FAIL
            return outcome
        # Return warning and error message lists
        outcome = _OUTCOME_OK
        return outcome


class _CashFlowAggregation(_CashFlowAggregationBase):
    """
    """

    def __init__(self, world):
        _CashFlowAggregationBase.__init__(self, world)

    def end(self):
        _CashFlowAggregationBase._end(self)

    def perform(self, execParam):
        _CashFlowAggregationBase._perform(self, execParam)

    def _doInspectInstrumentAllTrades(self, ins, firstValidTradeByTradeStatus):
        """
        Inspect all trades of the instrument.
        """
        trades = sorted([trade for trade in ins.Trades() if trade.Oid() > 0],
                key=lambda trade: trade.Oid())
        # First, check the instrument has no trades that are supposed not to
        # aggregate.  It there are trades that may not have PnL values, the
        # instrument should not be aggregated.
        for trade in trades:
            if not self._isTradeValidForAggregationByTradeStatus(trade):
                errMsg = ('The cash flow instrument \'{0}\' has a trade {1} '
                        'whose status is \'{2}\'.  As this trade may not '
                        'contribute to any profit-and-loss value, the '
                        'instrument will not be aggregated.'.format(ins.Name(),
                        trade.Oid(), trade.Status()))
                self._logError(errMsg)
        # Second, check instrument number of trades
        numTrades = len(trades)
        if numTrades == 0:
            errMsg = ('The cash flow instrument \'{0}\' should have only one '
                    'trade or a pair of mirror trades, but at the moment '
                    'there is none.'.format(ins.Name()))
            self._logError(errMsg)
        elif numTrades == 1:
            pass
        elif numTrades == 2:
            reason = self._areTwoTradesMirrorTradesIfFalseGiveReason(trades[0],
                    trades[1])
            if reason:
                errMsg = ('The cash flow instrument \'{0}\' should have only '
                        'one trade or a pair of mirror trades, but the two '
                        'trades here are not mirror trades.  NOTE: '
                        '{1}'.format(ins.Name(), reason))
                self._logError(errMsg)
        elif numTrades >= 3:
            errMsg = ('The cash flow instrument \'{0}\' should have only one '
                    'trade or a pair of mirror trades, but at the moment '
                    'there are {1}: {2}.'.format(ins.Name(), numTrades,
                    '[' + ','.join([str(t.Oid()) for t in trades]) + ']'))
            self._logError(errMsg)
        # Third, for the first valid trade by trade status, print the
        # instrument start date / spot day and the trade acquire date / value
        # date in debug.
        if firstValidTradeByTradeStatus:
            insStartDate = ins.StartDate()
            insSpotDayOffset = ins.SpotBankingDaysOffset()
            tradeAcquireDate = firstValidTradeByTradeStatus.AcquireDay()
            tradeValueDate = firstValidTradeByTradeStatus.ValueDay()
            self._logDebug('    [ins:startDate={0},spotDayOffset={1}][trade:'
                    'acqDate={2},valDate={3}]'.format(insStartDate,
                    insSpotDayOffset, tradeAcquireDate, tradeValueDate))

    def _doInspectInstrumentHasFunding(self, isFundingEnabled, ins,
            firstValidTradeByTradeStatus, todayDate):
        """
        """
        # Check if valuation parameter's funding is enabled
        if isFundingEnabled and firstValidTradeByTradeStatus:
            fundingValue = None
            try:
                fundingValue = self._calculateInstrumentFunding(ins,
                         firstValidTradeByTradeStatus, todayDate).Number()
            except Exception as e:
                # Always do trace back as soon as the exception is handled.
                for tbLine in traceback.format_stack():
                    self._logNoTime(tbLine)
                errMsg = ('Failed to calculate funding for instrument {0}.  '
                        '{1}'.format(ins.Name(), str(e)))
                # Log warning/error when exception is not going to be re-raised
                self._logError(errMsg)
            else:
                if fundingValue:
                    errMsg = ('Cash flow aggregation does not support '
                            'funding.  Funding on instrument {0} is not '
                            'zero, hence the instrument will not be '
                            'processed.'.format(ins.Name()))
                    self._logError(errMsg)

    def _doInspectLegAlignedAggregationDateProperlySet(self, requestedAggDate,
            firstRACFPayDate, alignedAggDate):
        """
        Inspect aligned aggregation date for the instrument leg.  If it is not
        properly set, it will be set to INCEPTION DATE.  For the aggregation,
        if it is not set, output an error message.  Note, this method is
        correlated with __findAlignedAggDate()
        """
        # Find the practical aggregation date
        practicalAggDate = requestedAggDate
        if firstRACFPayDate and firstRACFPayDate < requestedAggDate:
            practicalAggDate = firstRACFPayDate
        # If the aligned aggregation date is at the inception, that means the
        # aligned date had not been found by using this practical aggregation
        # date.  Report this error.
        if alignedAggDate == _INCEPTION_DATE:
            errMsg = ('The specified aggregation date {0} overlapped with '
                    'multiple cash flows\' period.  Unable to determine which '
                    'cash flow\'s start date should be used for aggregation '
                    'date alignment.'.format(practicalAggDate))
            self._logError(errMsg)

    def _doInspectPastFloatRateCashFlowResetsAllFixed(self, cf,
            requestedAggDate):
        """
        Inspect the cash flow.  If it is a float rates cash flow ended before
        and on the requested aggregation date, and the check all resets starts
        before the requested aggregation date must have fixing value; otherwise
        generate an error message.
        """
        # Check only for float rate types cash flows
        if (cf.CashFlowType() in _CASH_FLOW_TYPES_FLOAT_RATES and
                cf.EndDate() <= requestedAggDate):
            allRSTs = [rst for rst in cf.Resets()]
            for rst in allRSTs:
                if acm.Time.AsDate(rst.ReadTime()) != acm.Time.SmallDate():
                    continue
                errMsg = ('Reset {0} (Type:{1}, start date: {2}, end date:'
                        '{3}) not fixed.'.format(rst.Oid(), rst.ResetType(),
                        rst.StartDate(), rst.EndDate()))
                self._logError(errMsg)

    def _processLegBatchUpCashFlowsToProcess(self, leg, lastCFAggDate,
            alignedAggDate, cfsToProcess):
        """
        Use rates cash flows' end dates as batch boundary.
        """
        cfsBatchList = []
        endDates = [cf.EndDate() for cf in cfsToProcess
                if cf.CashFlowType() in _CASH_FLOW_TYPES_RATES]
        # If rates cash flows are found, so we go ahead to split them into
        # batches.
        if endDates:
            endDates = list(set(endDates))
            endDates.sort()
            startDate = lastCFAggDate
            for endDate in endDates:
                cfList = [cf for cf in cfsToProcess if
                        self._isAggregatablesCashFlowInPeriod(cf, startDate,
                        endDate)]
                cfsBatch = self._CashFlowBatch(startDate=startDate,
                        endDate=endDate, cfList=cfList)
                cfsBatchList.append(cfsBatch)
                startDate = endDate
        # If there is no rates cash flows, and hence no end dates, so can't
        # find a natural way to split the period. Then we have to batch up
        # according to the pay dates.
        else:
            payDates = [cf.PayDate() for cf in cfsToProcess
                    if cf.CashFlowType() not in _CASH_FLOW_TYPES_RATES]
            payDates = list(set(payDates))
            payDates.sort()
            startDate = lastCFAggDate
            for endDate in payDates:
                cfList = [cf for cf in cfsToProcess if
                        self._isAggregatablesCashFlowInPeriod(cf, startDate,
                        endDate)]
                cfsBatch = self._CashFlowBatch(startDate=startDate,
                        endDate=endDate, cfList=cfList)
                cfsBatchList.append(cfsBatch)
                startDate = endDate
        return cfsBatchList

    def _processLegFindCashFlowToProcess(self, leg, lastCFAggDate,
            alignedAggDate):

        cfsToProcess = [cf for cf in leg.CashFlows() if
                self._isAggregatablesCashFlowInPeriod(cf, lastCFAggDate,
                alignedAggDate)]
        self._logDebug('        There are {0} cash flows within the period '
                'from {1} to {2}'.format(len(cfsToProcess), lastCFAggDate,
                alignedAggDate))
        return cfsToProcess

    def _processLegProcessBatches(self, leg, trade, cfsBatchList):

        aggBatcher = self.__ObjBatchAggQueue(500)
        for cfsBatch in cfsBatchList:
            batchStartDate = cfsBatch.startDate
            batchEndDate = cfsBatch.endDate
            transDepObjs = self.__findUniqueTransitiveArchivingObjectList(
                    cfsBatch.cfList)
            self._logDebug('        Enqueuing batch (startDate={0},endDate='
                    '{1},numObj={2}) into the batch-aggregation-queue.'.format(
                    batchStartDate, batchEndDate, len(transDepObjs)))
            self._logObjListInDebug('            ', transDepObjs)
            objBatch = self._ObjBatch(startDate=batchStartDate,
                    endDate=batchEndDate, objList=transDepObjs)
            aggBatcher.enqueueBatch(objBatch)
        aggObjBatchList = []
        while not aggBatcher.isEmpty():
            aggObjBatch = aggBatcher.dequeueAggregatedBatch()
            self._logDebug('        Dequeued aggregation batch (startDate='
                    '{0},endDate={1},numObj={2}) from batch agregation '
                    'queue.'.format(aggObjBatch.startDate, aggObjBatch.endDate,
                    len(aggObjBatch.objList)))
            self._logObjListInDebug('            ', aggObjBatch.objList)
            aggObjBatchList.append(aggObjBatch)
        # Process batch
        self._logDebug('        There are total {0} aggregation batch to '
                'aggregate'.format(len(aggObjBatchList)))
        for aggObjBatch in aggObjBatchList:
            self.__aggregateBatch(leg, trade, aggObjBatch.startDate,
                    aggObjBatch.endDate, aggObjBatch.objList)

    # For holding acm object batch
    _ObjBatch = collections.namedtuple('_ObjBatch',
            'startDate endDate objList')

    class __ObjBatchAggQueue(object):
        """
        A queue that enqueues in batches and dequeues in aggregated batches.
        The dequeued aggregated batch consists of one or more original batches
        enqueued.  Original batch boundaries are preserved.  An aggregated
        batch contains as many original batch as possible, while not exceeding
        the specified limit aggBatchMaxLen.  The aggregated batch contains at
        least one original batch, whether or not exceeding the size limit
        aggBatchMaxLen.
        """
        def __init__(self, aggBatchMaxLen):
            """
            Initialiser.
            """
            self.__aggBatchMaxLen = aggBatchMaxLen
            self.__batchQueue = collections.deque()

        def enqueueBatch(self, objBatch):
            """
            Enqueue a batch.  A batch is a list of elements.
            """
            if not isinstance(objBatch, _CashFlowAggregation._ObjBatch):
                raise ValueError('The batch content must be an instance of '
                        '_ObjBatch, but it is of type {0}'.format(
                        type(objBatch)))
            self.__batchQueue.append(objBatch)

        def dequeueAggregatedBatch(self):
            """
            Dequeue an aggregated batch.  Returns either None or an aggregated
            batch.  The aggregated batch returned contains either (a) one
            original batch and the size exceeded the aggBatchMaxLen, or (b)
            one or more original batches and the size does not exceeds
            aggBatchMaxLen.
            """
            if self.isEmpty():
                return None
            headBatch = self.__batchQueue.popleft()
            startDateList = [headBatch.startDate]
            endDateList = [headBatch.endDate]
            aggObjList = headBatch.objList
            curLen = len(aggObjList)
            while (not self.isEmpty() and (
                     (curLen + len(self.__batchQueue[0].objList)) <=
                     self.__aggBatchMaxLen)):
                headBatch = self.__batchQueue.popleft()
                startDateList.append(headBatch.startDate)
                endDateList.append(headBatch.endDate)
                aggObjList.extend(headBatch.objList)
                curLen = curLen + len(headBatch.objList)
            return _CashFlowAggregation._ObjBatch(startDate=min(startDateList),
                    endDate=max(endDateList), objList=aggObjList)

        def isEmpty(self):
            """
            Return true if the internal queue is empty.
            """
            return len(self.__batchQueue) == 0

    def __aggregateBatch(self, leg, trade, batchStartDate, batchEndDate,
            aggObjList):
        """
        """
        self._logDebug('        Aggregating batch (startDate={0},endDate={1},'
                'numAcmObjs={2})'.format(batchStartDate, batchEndDate,
                len(aggObjList)))
        fixedAmountsCFs = [obj for obj in aggObjList
                if obj.RecordType() == _RECORD_TYPE_CASH_FLOW
                and obj.CashFlowType() in _CASH_FLOW_TYPES_FIXED_AMOUNTS]
        self._logDebug('        There are {0} cash flows to be aggregated '
                'into \'aggregated fixed amount\'.'.format(
                len(fixedAmountsCFs)))
        self._logObjListInDebug('            ', fixedAmountsCFs)
        ratesCFs = [obj for obj in aggObjList if
                obj.RecordType() == 'CashFlow' and
                obj.CashFlowType() in _CASH_FLOW_TYPES_RATES]
        self._logDebug('        There are {0} cash flows to be aggregated '
                  'into \'aggregated coupon\'.'.format(len(ratesCFs)))
        self._logObjListInDebug('            ', ratesCFs)
        # Begin transaction
        acm.BeginTransaction()
        try:
            # Calculate aggregated fixed amount if there is cash flows to be
            # aggregated
            cfAggFixedAmount = self.__calculateCashFlowAggregatedFixedAmount(
                    leg, batchStartDate, batchEndDate, fixedAmountsCFs)
            cfAggCouponList = self.__calculateCashFlowAggregatedCoupons(leg,
                    trade, batchStartDate, batchEndDate, ratesCFs)
            self._logDebug('        Aggregation commiting...')
            # Commit new aggregated fixed amount cash flow
            self._summaryAddOk(cfAggFixedAmount.RecordType(),
                    cfAggFixedAmount.Oid(), 'CREATE')
            self._logDebug('            creating {0} cash flow '
                    'acm.FCashFlow[{1}]'.format(
                    cfAggFixedAmount.CashFlowType(), cfAggFixedAmount.Oid()))
            if not self._isInTestMode():
                cfAggFixedAmount.Commit()
            # Commit new aggregated coupon cash flows.
            for cfAggCoupon in cfAggCouponList:
                self._summaryAddOk(cfAggCoupon.RecordType(), cfAggCoupon.Oid(),
                        'CREATE')
                self._logDebug('            creating {0} cash flow '
                        'acm.FCashFlow[{1}]'.format(cfAggCoupon.CashFlowType(),
                        cfAggCoupon.Oid()))
                if not self._isInTestMode():
                        cfAggCoupon.Commit()
            # Archive cash flow and dependent objects
            for obj in aggObjList:
                self._summaryAddOk(obj.RecordType(), obj.Oid(), 'ARCHIVE')
                self._logDebug('            archiving acm.F{0}[{1}]'.format(
                        obj.RecordType(), obj.Oid()))
                if not self._isInTestMode():
                    obj.ArchiveStatus(1)
                    obj.Commit()
        except CashFlowAggregationCalculateSettledInterestError:
            acm.AbortTransaction()
            raise
        except Exception as e:
            # Always do trace back as soon as the exception is handled.
            for tbLine in traceback.format_stack():
                self._logNoTime(tbLine)
            acm.AbortTransaction()
            # Raise captured error instead of the original if handled.
            raise CashFlowAggregationCapturedError(str(e))
        else:
            if self._isInTestMode():
                acm.AbortTransaction()
                self._logDebug('        Not committed due to test mode.')
            else:
                acm.CommitTransaction()
                self._logDebug('        Committed.')
        acm.PollDbEvents()
        self._logDebug('        Done aggregation batch.')

    def __calculateCashFlowAggregatedCoupons(self, leg, trade, periodStartDate,
            periodEndDate, ratesCFs):
        """
        Calculate the representing aggregates for the rates cash flows.
        """
        self._logDebug('        Calculating the aggregated coupon cash flow.')
        calcMths = acm.FCalculationMethods()
        spaceCollection = calcMths.CreateStandardCalculationsSpaceCollection()
        siParams = {}
        siParams['trade'] = trade
        siParams['currency'] = leg.Currency()
        siParams['valuationUntilSpot'] = 'P/L Until Spot OFF'
        # rates cash flows are grouped by pay date.
        payDateCashFlowsMap = {}
        for cf in ratesCFs:
            # For those cash flow with pay date before period end date,
            # consider them in the same way as they have pay date on the
            # period end date.
            payDate = cf.PayDate()
            if payDate <= periodEndDate:
                payDate = periodEndDate
            # Add the cash flow into the map.
            if payDate not in payDateCashFlowsMap:
                payDateCashFlowsMap[payDate] = [cf]
            else:
                payDateCashFlowsMap[payDate].append(cf)
        numPayDateGroups = len(payDateCashFlowsMap)
        self._logDebug('            Number of pay date groups = '
            '{0}.'.format(numPayDateGroups))
        # Go through each pay date and create aggregate
        cfAggList = []
        payDateGroupNum = 0
        for payDate in sorted(payDateCashFlowsMap.keys()):
            payDateGroupNum += 1
            cfList = payDateCashFlowsMap[payDate]
            self._logDebug('                Group ({0}/{1}) : PayDate={2} : '
                    '{3} cash flow(s) to aggregate.'.format(payDateGroupNum,
                    numPayDateGroups, payDate, len(cfList)))
            siParams['endDate'] = payDate
            # pro-rata settled interest list
            prsiList = self.__calculateRatesCashFlowSettledInterestList(
                    cfList, spaceCollection, siParams)
            if prsiList:
                self._logDebug('                settled interests = [')
                for settledInterest in prsiList:
                    self._logDebug('                    {0}'.format(
                            settledInterest))
                self._logDebug('                                    ]')
            else:
                self._logDebug('                settled interests = []')
            sumSettledInterest = sum(prsiList)
            self._logDebug('                sum of settled interests = '
                      '{0}'.format(sumSettledInterest))
            # Mark the aggregate
            cfAgg = acm.FCashFlow()
            cfAgg.Leg(leg)
            cfAgg.CashFlowType(_CASH_FLOW_TYPE_AGGREGATED_COUPON)
            cfAgg.FixedAmount(sumSettledInterest)
            cfAgg.NominalFactor(1.0)
            cfAgg.StartDate(periodStartDate)
            cfAgg.EndDate(periodEndDate)
            cfAgg.PayDate(payDate)
            cfAggList.append(cfAgg)
            self._logDebug('            Calculated {0} cash flow is S={1}/E='
                      '{2}/P={3}/FA={4}'.format(cfAgg.CashFlowType(),
                      cfAgg.StartDate(), cfAgg.EndDate(), cfAgg.PayDate(),
                      cfAgg.FixedAmount()))
        self._logDebug('            All pay date groups calculated.')
        return cfAggList

    def __calculateCashFlowAggregatedFixedAmount(self, leg, periodStartDate,
            periodEndDate, fixedAmountsCFs):
        """
        Calculate the representing aggregate for the fixed amounts cash flows.
        """
        self._logDebug('        Calculating the aggregated fixed amount '
                'cash flow.')
        # Calculate the sum
        fixedAmountList = [cf.FixedAmount() for cf in fixedAmountsCFs]
        if fixedAmountList:
            self._logDebug('            fixed amounts = [')
            for fixedAmount in fixedAmountList:
                self._logDebug('                {0}'.format(fixedAmount))
            self._logDebug('                            ]')
        else:
            self._logDebug('            fixed amounts = []')
        sumFixedAmount = sum(fixedAmountList)
        self._logDebug('            sum of fixed amounts = {0}'.format(
                sumFixedAmount))
        # Make the aggregate
        cfAgg = acm.FCashFlow()
        cfAgg.Leg(leg)
        cfAgg.CashFlowType(_CASH_FLOW_TYPE_AGGREGATED_FIXED_AMOUNT)
        cfAgg.FixedAmount(sumFixedAmount)
        cfAgg.NominalFactor(1.0)
        cfAgg.StartDate(periodStartDate)
        cfAgg.EndDate(periodEndDate)
        cfAgg.PayDate(periodEndDate)
        self._logDebug('        Calculated {0} cash flow is S={1}/E={2}/P='
                  '{3}/FA={4}'.format(cfAgg.CashFlowType(), cfAgg.StartDate(),
                  cfAgg.EndDate(), cfAgg.PayDate(), cfAgg.FixedAmount()))
        return cfAgg

    def __calculateRatesCashFlowSettledInterestList(self, acmCFList,
            spaceCollection, siParams):
        """
        """
        # Calculate settled interest
        settledInterestList = []
        for cf in acmCFList:
            try:
                si = cf.Calculation().SettledInterestParams(spaceCollection,
                        siParams).Value().Number()
            except Exception as e:
                # Always do trace back and log warning/error as soon as the
                # exception is handled.
                for tbLine in traceback.format_stack():
                    self._logNoTime(tbLine)
                # Raise captured error instead of the original if handled.
                raise CashFlowAggregationCalculateSettledInterestError(str(e),
                       cf, siParams)
            settledInterestList.append(si)
        tradeQuantity = siParams['trade'].Quantity()
        if tradeQuantity and isinstance(tradeQuantity, float):
            proRataSettledInterestList = [si / tradeQuantity for si in
                    settledInterestList]
        else:
            proRataSettledInterestList = settledInterestList
        # Return the settledInterest value number
        return proRataSettledInterestList

    def __findUniqueTransitiveArchivingObjectList(self, objList):
        """
        """
        transDepObjList = self._findUniqueTransitiveDependentList(objList,
                lambda obj: obj.RecordType(),
                _TRANSITIVE_ARCHIVE_FIND_DEPENDENTS_RECTYPE_OP_MAP)
        return transDepObjList


class _CashFlowDeaggregation(_CashFlowAggregationBase):
    """
    """

    def __init__(self, world):
        _CashFlowAggregationBase.__init__(self, world)

    def end(self):
        """
        """
        _CashFlowAggregationBase._end(self)

    def perform(self, execParam):
        """
        """
        _CashFlowAggregationBase._perform(self, execParam)

    def _doInspectInstrumentAllTrades(self, ins, firstValidTradeByTradeStatus):
        """
        Inspect all trades of the instrument.  If there was any reason why
        cash flow aggregation should not be run on the instrument, the cash
        flow de-aggregation should print it out as warning.
        """
        # Initialise warning and error message lists
        trades = sorted([trade for trade in ins.Trades() if trade.Oid() > 0],
                key=lambda trade: trade.Oid())
        # First, check the instrument has no trades that are supposed not to
        # aggregate.  It there are trades that may not have PnL values, the
        # instrument should not be aggregated.
        for trade in trades:
            if not self._isTradeValidForAggregationByTradeStatus(trade):
                warnMsg = ('The cash flow instrument \'{0}\' has a trade {1} '
                        'whose status is \'{2}\'.  As this trade may not '
                        'contribute to any profit-and-loss value, the '
                        'instrument can only be de-aggregated.'.format(
                        ins.Name(), trade.Oid(), trade.Status()))
                self._logWarning(warnMsg)
        # Second, check instrument number of trades
        numTrades = len(trades)
        if numTrades == 0:
            warnMsg = ('The cash flow instrument \'{0}\' should have only '
                    'one trade or a pair of mirror trades, but at the moment '
                    'there is none.'.format(ins.Name()))
            self._logWarning(warnMsg)
        elif numTrades == 1:
            pass
        elif numTrades == 2:
            reason = self._areTwoTradesMirrorTradesIfFalseGiveReason(trades[0],
                    trades[1])
            if reason:
                warnMsg = ('The cash flow instrument \'{0}\' should have only '
                        'one trade or a pair of mirror trades, but the two '
                        'trades here are not mirror trades.  NOTE: {1}'.format(
                        ins.Name(), reason))
                self._logWarning(warnMsg)
        elif numTrades >= 3:
            warnMsg = ('The cash flow instrument \'{0}\' should have only '
                    'one trade or a pair of mirror trades, but at the moment '
                    'there are {1}: {2}.'.format(ins.Name(), numTrades,
                    '[' + ','.join([str(t.Oid()) for t in trades]) + ']'))
            self._logWarning(warnMsg)

    def _doInspectInstrumentHasFunding(self, isFundingEnabled, ins,
            firstValidTradeByTradeStatus, todayDate):
        """
        """
        # Check if valuation parameter's funding is enabled
        if isFundingEnabled and firstValidTradeByTradeStatus:
            fundingValue = None
            try:
                fundingValue = self._calculateInstrumentFunding(ins,
                        firstValidTradeByTradeStatus, todayDate).Number()
            except Exception as e:
                # Always do trace back as soon as the exception is handled.
                for tbLine in traceback.format_stack():
                    self._logNoTime(tbLine)
                warnMsg = ('Failed to calculate funding for instrument {0}.  '
                        '{1}'.format(ins.Name(), str(e)))
                # Log warning/error when exception is not going to be re-raised
                self._logWarning(warnMsg)
            else:
                if fundingValue:
                    warnMsg = ('Cash flow aggregation does not support '
                            'funding.  Profit-and-loss values may change '
                            'after de-aggregation due to funding.'.format(
                            ins.Name()))
                    self._logWarning(warnMsg)

    def _doInspectLegAlignedAggregationDateProperlySet(self, requestedAggDate,
            firstRACFPayDate, alignedAggDate):
        """
        Inspect the aligned aggregation date for the instrument leg.  For the
        de-aggregation, it is okay if the aligned aggregation date is not set
        properly (i.e. set at INCEPTION DATE).  Therefore there is nothing is
        checked.  Note, this method is correlated with __findAlignedAggDate()
        """
        pass

    def _doInspectPastFloatRateCashFlowResetsAllFixed(self, cf,
            requestedAggDate):
        """
        Inspect the cash flow.  There is no point to test this during
        de-aggregation, so return straight away.
        """
        pass

    def _processLegBatchUpCashFlowsToProcess(self, leg, lastCFAggDate,
            alignedAggDate, cfsToProcess):
        """
        Use aggregated fixed amount's start date as batch boundary.
        """

        startDates = [cf.StartDate() for cf in cfsToProcess if
                cf.CashFlowType() == _CASH_FLOW_TYPE_AGGREGATED_FIXED_AMOUNT]
        startDates = list(set(startDates))
        startDates.sort()
        startDates.reverse()
        cfsBatchList = []
        endDate = lastCFAggDate
        for startDate in startDates:
            cfList = [cf for cf in cfsToProcess if
                    self._isAggregatesCashFlowInPeriod(cf, startDate, endDate)]
            cfsBatch = self._CashFlowBatch(startDate=startDate,
                    endDate=endDate, cfList=cfList)
            cfsBatchList.append(cfsBatch)
            endDate = startDate
        return cfsBatchList

    def _processLegFindCashFlowToProcess(self, leg, lastCFAggDate,
                alignedAggDate):
        """
        """
        cfsToProcess = [cf for cf in leg.CashFlows() if
                self._isAggregatesCashFlowInPeriod(cf, alignedAggDate,
                lastCFAggDate)]
        self._logDebug('        There are {0} cash flows within the period '
                'from {1} to {2}'.format(len(cfsToProcess), alignedAggDate,
                lastCFAggDate))
        return cfsToProcess

    def _processLegProcessBatches(self, leg, trade, cfsBatchList):
        """
        """
        # For the leg, find cash flows in the time period
        aelLeg = FBDPCommon.acm_to_ael(leg)
        remainingCFsToProcess = [FBDPCommon.ael_to_acm(aelObj) for aelObj
                in aelLeg.reference_in() if
                (aelObj.record_type == _RECORD_TYPE_CASH_FLOW and
                aelObj.type in _CASH_FLOW_TYPES_AGGREGATABLES)]
        self._logDebug('        There are {0} aggregatable cash flows in this '
                'leg.'.format(len(remainingCFsToProcess)))
        self._logObjListInDebug('            ', remainingCFsToProcess)
        for cfsBatch in cfsBatchList:
            batchStartDate = cfsBatch.startDate
            batchEndDate = cfsBatch.endDate
            aggCFList = cfsBatch.cfList
            # Separate the cash flows into two groups, between (1) those to be
            # processed in this # batch and (2) those remains to be processed.
            cfsToProcess = []
            cfsYetToProcess = []
            for cf in remainingCFsToProcess:
                if self._isAggregatablesCashFlowInPeriod(cf, batchStartDate,
                       batchEndDate):
                    cfsToProcess.append(cf)
                else:
                    cfsYetToProcess.append(cf)
            remainingCFsToProcess = cfsYetToProcess
            # Print out those to be process in this batch
            self._logDebug('        For period {0} to {1}, three are {2} '
                    'cash flows.'.format(batchStartDate, batchEndDate,
                    len(cfsToProcess)))
            self._logObjListInDebug('            ', cfsToProcess)
            deaggObjList = self.__findUniqueTransitiveDearchivingObjectList(
                    cfsToProcess)
            self._logDebug('        Also, three are {0} acmObjs to be '
                    'de-archived.'.format(len(deaggObjList)))
            deaggObjList = [acmObj for acmObj in deaggObjList]
            self._logObjListInDebug('            ', deaggObjList)
            # Process batch
            self.__deaggregateBatch(batchStartDate, batchEndDate, aggCFList,
                    deaggObjList)

    def __deaggregateBatch(self, batchStartDate, batchEndDate, aggCFList,
            deaggObjList):
        """
        """
        self._logDebug('    De-aggregating (period from {0} to {1}) '
                '...'.format(batchStartDate, batchEndDate))
        # Begin transaction
        acm.BeginTransaction()
        try:
            # Dearchive
            deaggObjList.reverse()
            for obj in deaggObjList:
                self._summaryAddOk(obj.RecordType(), obj.Oid(), 'DEARCHIVE')
                self._logDebug('            de-archiving acm.F{0}[{1}]'.format(
                        obj.RecordType(), obj.Oid()))
                if not self._isInTestMode():
                    obj.ArchiveStatus(0)
                    obj.Commit()
            # Delete aggregated cash flows
            for aggCF in aggCFList:
                self._summaryAddOk(aggCF.RecordType(), aggCF.Oid(), 'DELETE')
                self._logDebug('            deleting aggregate {0} '
                        'acm.FCashFlow[{1}]'.format(aggCF.CashFlowType(),
                        aggCF.Oid()))
                if not self._isInTestMode():
                    aggCF.Delete()
                aggCF = None
            # End transaction
        except Exception as e:
            # Always do trace back as soon as the exception is handled.
            for tbLine in traceback.format_stack():
                self._logNoTime(tbLine)
            acm.AbortTransaction()
            # Raise captured error instead of the original if handled.
            raise CashFlowAggregationCapturedError(str(e))
        else:
            if self._isInTestMode():
                acm.AbortTransaction()
            else:
                acm.CommitTransaction()
        acm.PollDbEvents()
        self._logDebug('    De-aggregating (period from {0} to {1}) ... '
                'done'.format(batchStartDate, batchEndDate))

    def __findUniqueTransitiveDearchivingObjectList(self, objList):
        """
        """
        transDepObjList = self._findUniqueTransitiveDependentList(objList,
                lambda obj: obj.RecordType(),
                _TRANSITIVE_DEARCHIVE_FIND_DEPENDENTS_RECTYPE_OP_MAP)
        archivedTransDepObjList = [obj for obj in transDepObjList if
                obj.ArchiveStatus()]
        return archivedTransDepObjList
