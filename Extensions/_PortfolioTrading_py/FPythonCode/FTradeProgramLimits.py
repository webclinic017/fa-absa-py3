""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramLimits.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FTradeProgramLimits

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import math
import acm
from contextlib import contextmanager

from FTradeProgramUtils import Logger
try:
    import FLimitMonitor
    import FLimitExceptions
    import FLimitUtils
    limitsBaseInstalled = True
except ImportError as err:
    limitsBaseInstalled = False
    Logger().info('Limits Base module not in context. No limit checks will be performed.')


def LimitsBaseInstalled():
    return limitsBaseInstalled


class CandidateTradesLimitsBase(object):

    def __init__(self, trades):
        self._trades = trades
        self._relevantLimits = None
        self._relevantTrades = None

    def RelevantTrades(self):
        if self._relevantTrades is None:
            self.RelevantLimits()
        return self._relevantTrades

    def RelevantLimits(self):
        if self._relevantLimits is None:
            self._relevantLimits = set()
            for trade in self._Trades():
                limitsByTrade = acm.Limits.FindByTrade(trade)
                if limitsByTrade:
                    if self._relevantTrades is None:
                        self._relevantTrades = []
                    self._relevantTrades.append(trade)
                    self._relevantLimits.update([limit for limit in limitsByTrade
                                                if self.IsActiveForMonitoring(limit)])
        return self._relevantLimits

    def _Trades(self):
        return self._trades

    @staticmethod
    def _CurrentState(obj):
        try:
            return obj.BusinessProcess().CurrentStep().State().Name()
        except AttributeError as e:
            Logger().warn(e, exc_info=True)
    
    @staticmethod
    def IsActiveForMonitoring(limit):
        return bool(FLimitUtils.IsActive(limit) or
                    FLimitUtils.CurrentState(limit) == 'Ready')
            

class TradeProgramLimits(CandidateTradesLimitsBase):

    class LIMIT_STATE(object):
        BREACHED = 'Breached'
        WORKING = 'Working...'
        PASSED = 'Passed'

    def __init__(self, tradeProgram):
        super(TradeProgramLimits, self).__init__(tradeProgram.AllTrades())
        self._tradeProgram = tradeProgram
        self._unCheckedLimits = {}
        self._checkedLimits = []
        self._StartMonitoring()

    def TradeProgram(self):
        return self._tradeProgram

    def ServerUpdate(self, limitValue, _symbol, _param):
        if self._IsChecked(limitValue) is True:
            limit = self._unCheckedLimits[limitValue]
            self._checkedLimits.append(limit)
            self._Detach(limitValue)

    def StopMonitoring(self):
        for limitValue in self._unCheckedLimits:
            limitValue.RemoveDependent(self)
        self._unCheckedLimits = {}

    def LimitsState(self):
        if self._unCheckedLimits:
            return self.LIMIT_STATE.WORKING
        for limit in self._checkedLimits:
            if self._CurrentState(limit) == 'Breached':
                return self.LIMIT_STATE.BREACHED
        return self.LIMIT_STATE.PASSED

    def LimitsUpdated(self):
        for limit in self.RelevantLimits():
            if self._IsChecked(limit.LimitValue()) is False:
                return False
        return True

    def _IsChecked(self, limitValue):
        return limitValue.UpdateTime() >= self.TradeProgram().UpdateTime()

    def _StartMonitoring(self):
        for limit in self.RelevantLimits():
            limitValue = limit.LimitValue()
            if self._IsChecked(limitValue) is False:
                self._unCheckedLimits[limitValue] = limit
                limitValue.AddDependent(self)
            else:
                self._checkedLimits.append(limit)

    def _Detach(self, limitValue):
        del self._unCheckedLimits[limitValue]
        limitValue.RemoveDependent(self)


class CandidateTradesLimits(CandidateTradesLimitsBase):

    def __init__(self, trades, tradeStatus=None):
        super(CandidateTradesLimits, self).__init__(trades)
        self._tradeStatus = tradeStatus

    def LimitResults(self):
        return self._SimulationResults()

    def _SimulationResults(self):
        results = dict()
        for limit in self.RelevantLimits():
            try:
                monitoredLimit = FLimitMonitor.FMonitoredLimit(limit)
            except FLimitExceptions.LimitError as e:
                Logger().info("Problem when checking if trade program breaks limit", limit.Oid(), e)
                Logger().info("Continuing with next limit...")
                continue
            with self.TradesInStatus(self.RelevantTrades(), self._tradeStatus) as trades:
                result = monitoredLimit.CheckLimit(trades)
            if self._LimitStateChanged(result):
                results[limit] = result
        return results
    
    @classmethod
    @contextmanager
    def TradesInStatus(cls, trades, status):
        originalStatuses = []
        if status:
            for trade in trades:
                originalStatuses.append(trade.Status())
                trade.Status(status)
                
        yield trades
        
        if status:
            for originalStatus in originalStatuses:
                trade.Status(originalStatus)
    
    @staticmethod
    def _LimitStateChanged(result):
        return result.StateBefore != result.StateAfter


class CandidateTradesCutToLimits(CandidateTradesLimits):

    def __init__(self, trades, statesToAvoid):
        super(CandidateTradesCutToLimits, self).__init__(trades)
        self._originalQuantities = None
        self._statesToAvoid = statesToAvoid
        self._results = None

    def LimitResults(self):
        results = self._SimulationResults()
        limitsAffected = results.keys()
        if self._LimitsInStatesToAvoid(results):
            try:
                Logger().info("Trade program will breach limits. Trying to adjust.")
                self._ScaleToLimits()
                if self._results:
                    for result in self._results.values():
                        result.StateBefore = self._CurrentState(result.Limit)
                    return dict((limit, self._results[limit]) for limit in limitsAffected if
                                self._results[limit].StateBefore != self._results[limit].StateAfter)
                return {}
            except Exception as e:
                Logger().error("Errors occurred while finding limit scale: %s" % e, exc_info=True)

    def _ScaleTrades(self, scaleValue):
        if scaleValue > 1.0 or scaleValue <= 0.0:
            raise ValueError('Cannot scale with value %f' % scaleValue)
        for t in self.RelevantTrades():
            t.Quantity(math.ceil(self._OriginalQuantities()[t] * scaleValue))

    def _ScaleToLimits(self):
        permitFunc = lambda scale: self._WillBreachAfterScale(scale) is False
        findPermittedLevel = FFindPermittedHighestInput(permitFunc)
        findPermittedLevel.Find()

    def _WillBreachAfterScale(self, scaleValue):
        self._ScaleTrades(scaleValue)
        self._results = self._SimulationResults()
        return bool(self._LimitsInStatesToAvoid(self._results))

    def _OriginalQuantities(self):
        if self._originalQuantities is None:
            self._originalQuantities = dict((t, t.Quantity()) for t in self.RelevantTrades())
        return self._originalQuantities

    def _StatesToAvoid(self):
        return self._statesToAvoid

    def _LimitsInStatesToAvoid(self, results):
        return [limit for limit in results
                if results[limit].StateAfter in self._StatesToAvoid()]


class FFindPermittedHighestInput(object):
    def __init__(self, testFunction, loops=10,
                 originalInput=1.0, closedLowest=0.0, openHighest=1.0):
        self.testFunction = testFunction
        self.originalInput = float(originalInput)
        self.maxLoops = loops
        self.loopNo = 0
        self.done = False
        self.closedLowest = closedLowest
        self.openHighest = openHighest

    def Find(self):
        foundValue = self._ValueClosestBelow(self.originalInput)
        self.loopNo = 0
        self.done = False
        if self.testFunction(foundValue):
            return foundValue
        else:
            raise RuntimeWarning("No acceptable level could be found. Last tried: %s%%"%foundValue)

    def _ValueClosestBelow(self, inputVal):
        self.loopNo += 1
        if self.loopNo > self.maxLoops:
            self.done = True #Lets get out

        valueDelta = self.originalInput / (2**self.loopNo)

        if inputVal > self.openHighest:
            return self.openHighest
        if inputVal <= self.closedLowest:
            return self.closedLowest

        if self.testFunction(inputVal):
            #The function returns true, we are on the right side
            if self.done:
                #Should not go further
                self.loopNo = 0 #Reset
                return inputVal
            else:
                #Try a little more
                return self._ValueClosestBelow(inputVal+valueDelta)
        else:
            #Function returns false, we need to go down
            if self.done:
                #We should stop but are still on the wrong side.
                #Lets go down a double step to be sure
                return self._ValueClosestBelow(inputVal-2*valueDelta)
            else:
                return self._ValueClosestBelow(inputVal-valueDelta)
