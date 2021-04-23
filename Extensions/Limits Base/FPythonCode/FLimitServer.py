""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitServer.py"
"""--------------------------------------------------------------------------
MODULE
    FLimitServer

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Provides functionality for server side monitoring of limit calculations
    and the management of limit states.

-----------------------------------------------------------------------------"""
import datetime as dt
from collections import defaultdict
import Queue

import acm
import FAssetManagementUtils
import FBusinessProcessUtils
import FLimitMonitor
import FLimitSettings
import FLimitUtils
from FLimitExceptions import MissingLimitTargetError

logger = FAssetManagementUtils.GetLogger()


class FLimitServer(object):
    """A server for the monitoring of limits.

    Provides a thread-safe means for the addition of new limits to monitor,
    while retrying limits that may be 'invalid' (e.g. due to empty calculations).

    """
    def __init__(self):
        # pylint: disable-msg=E1101
        self._engine = FLimitEngine()
        self._invalidCheckPeriod = dt.timedelta(
                seconds=FLimitSettings.ServerInvalidLimitCheckPeriod())
        self._lastInvalidCheckTime = dt.datetime.now()
        self._invalidLimits = set()
        self._pendingLimits = Queue.Queue()

    def AddLimit(self, limit):
        """Add a limit to be managed by the server. The limit will monitored on
        the next call to ProcessLimits().
        """
        self._pendingLimits.put(limit)

    def ProcessLimits(self):
        """Process new, updated and invalid limits. This method must be called
        repeatedly to maintain realtime limit monitoring.

        """
        self._engine.DoWork()
        self._ProcessInvalidLimits()
        self._ProcessPendingLimits()
        self._ProcessUpdatedLimits()

    def RemoveLimit(self, limit):
        """Remove a limit from being managed by the server."""
        self._UnmonitorLimit(limit)
        self._invalidLimits.discard(limit)
        self._StopSubscriptions(limit)

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        if parameter.IsKindOf(acm.FBusinessProcess):
            for limit in self._LimitsForSubscription(sender):
                if str(aspectSymbol) == 'delete':
                    self.RemoveLimit(limit)
                elif self._IsValidForActiveMonitoring(limit):
                    self._MonitorLimit(limit)
                else:
                    self._UnmonitorLimit(limit)

    def _ProcessUpdatedLimits(self):
        for monitoredLimit in self._engine.UpdatedLimits():
            limit = monitoredLimit.Limit()
            self._UnmonitorLimit(limit)
            self._MonitorLimit(limit)

    def _ProcessInvalidLimits(self):
        if self._invalidLimits:
            checkTime = dt.datetime.now()
            if self._InvalidCheckPeriodTick(checkTime):
                for limit in self._invalidLimits:
                    self.AddLimit(limit)
                self._invalidLimits.clear()
                self._lastInvalidCheckTime = checkTime

    def _ProcessPendingLimits(self):
        while not self._pendingLimits.empty():
            limit = self._pendingLimits.get()
            assert(limit)
            logger.debug('Adding limit %d to monitored limit list.', limit.Oid())
            if self._IsValidForActiveMonitoring(limit):
                self._MonitorLimit(limit)
            self._StartSubscriptions(limit)
            self._pendingLimits.task_done()

    def _MonitorLimit(self, limit):
        try:
            self._engine.MonitorLimit(limit)
        except MissingLimitTargetError:
            if self._invalidCheckPeriod:
                self._invalidLimits.add(limit)
        except Exception as err:
            logger.error(err, exc_info=True)

    def _UnmonitorLimit(self, limit):
        try:
            self._engine.UnmonitorLimit(limit)
        except Exception as e:
            logger.error('Error unmonitoring limit: %s', e)

    def _StartSubscriptions(self, limit):
        for item in self._LimitMonitorStateSubscriptions(limit):
            item.AddDependent(self)

    def _StopSubscriptions(self, limit):
        for item in self._LimitMonitorStateSubscriptions(limit):
            item.RemoveDependent(self)

    def _InvalidCheckPeriodTick(self, checkTime):
        return (checkTime - self._lastInvalidCheckTime) > self._invalidCheckPeriod

    @staticmethod
    def IsActiveForMonitoring(limit):
        return bool(FLimitUtils.IsActive(limit) or
                    FLimitUtils.CurrentState(limit) == 'Ready')

    @classmethod
    def _IsValidForActiveMonitoring(cls, limit):
        return bool(cls.IsActiveForMonitoring(limit) and
                    cls._IsRealTimeMonitored(limit))

    @staticmethod
    def _LimitMonitorStateSubscriptions(limit):
        items = (limit.LimitSpecification(), limit.BusinessProcess())
        return [i for i in items if i]

    @staticmethod
    def _LimitsForSubscription(sender):
        if sender.IsKindOf(acm.FBusinessProcess):
            return [sender.Subject(), ]
        elif sender.IsKindOf(acm.FLimitSpecification):
            return sender.Limits()
        return []

    @staticmethod
    def _IsRealTimeMonitored(limit):
        return bool(limit.LimitSpecification() and
                    limit.LimitSpecification().RealtimeMonitored())


class FLimitEngine(object):
    """An engine for transitioning limit business processes based on monitored
    limit updates.

    """
    def __init__(self):
        # pylint: disable-msg=E1101
        super(FLimitEngine, self).__init__()
        self._monitoredLimits = dict()              # FLimit -> FMonitoredLimit
        self._subscriptions = defaultdict(set)      # FObject -> set(FMonitoredLimit)
        self._calculationSpaces = set()
        self._updatedLimits = Queue.Queue()

    def MonitorLimit(self, limit):
        if self._AddLimit(limit):
            self._StartSubscriptions(limit)
            self._CheckMonitoredLimit(limit)
            logger.info('Monitoring limit %d on "%s" (%s).',
                         limit.Oid(),
                         FLimitUtils.Constraints(limit),
                         FLimitUtils.ColumnName(limit))

    def UnmonitorLimit(self, limit):
        if self.IsMonitoringLimit(limit) is True:
            self._StopSubscriptions(limit)
            self._RemoveLimit(limit)

    def CheckMonitoredLimit(self, limit):
        if self.IsMonitoringLimit(limit) is True:
            self._CheckMonitoredLimit(limit)

    def CheckLimit(self, limit):
        if FLimitServer.IsActiveForMonitoring(limit):
            if self._AddLimit(limit):
                logger.debug('Checking limit %d on "%s" (%s).',
                        limit.Oid(),
                        FLimitUtils.Constraints(limit),
                        FLimitUtils.ColumnName(limit))
                try:
                    self._CheckMonitoredLimit(limit)
                    self._RemoveLimit(limit)
                except Exception as err:
                    logger.debug(err, exc_info=True)
        else:
            logger.debug('Limit %d is not in an active monitorable state (%s).',
                         limit.Oid(),
                         FLimitUtils.CurrentState(limit))

        if limit.IsParent():
            for l in limit.Children():
                self.CheckLimit(l)

    def DoWork(self):
        for cs in self._calculationSpaces:
            try:
                cs.Refresh()
            except Exception:
                pass

    def IsMonitoringLimit(self, limit):
        return bool(limit in self._monitoredLimits)

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        monitoredLimits = self._subscriptions.get(sender, [])
        for monitoredLimit in monitoredLimits:
            # Ignore business process updates reflected back on the limit subject
            if not (str(aspectSymbol) == 'delete' or sender.IsKindOf(acm.FLimit)
                    and parameter and parameter.IsKindOf(acm.FBusinessProcess)):
                self._updatedLimits.put(monitoredLimit)

    def UpdatedLimits(self):
        updatedLimits = set()
        while not self._updatedLimits.empty():
            monitoredLimit = self._updatedLimits.get_nowait()
            if monitoredLimit:
                updatedLimits.add(monitoredLimit)
                self._updatedLimits.task_done()
        return updatedLimits

    def _GetMonitoredLimit(self, limit):
        return self._monitoredLimits[limit]

    def _AddLimit(self, limit):
        if self.IsMonitoringLimit(limit) is False:
            monitoredLimit = FLimitMonitor.FMonitoredLimit(limit, listener=FLimitListener())
            self._monitoredLimits[limit] = monitoredLimit
            return True
        return False

    def _RemoveLimit(self, limit):
        del self._monitoredLimits[limit]
        logger.debug('Removed monitoring of limit %d on "%s" (%s).',
                     limit.Oid(),
                     FLimitUtils.Constraints(limit),
                     FLimitUtils.ColumnName(limit))

    def _StartSubscriptions(self, limit):
        monitoredLimit = self._GetMonitoredLimit(limit)
        for item in monitoredLimit.GetDependencies():
            self._subscriptions[item].add(monitoredLimit)
            item.AddDependent(self)
        self._calculationSpaces.add(monitoredLimit.CalculationSpace())

    def _StopSubscriptions(self, limit):
        monitoredLimit = self._GetMonitoredLimit(limit)
        subscriptions = (item for item, mls in self._subscriptions.items() if monitoredLimit in mls)
        for item in subscriptions:
            self._subscriptions[item].discard(monitoredLimit)
            if not self._subscriptions[item]:
                item.RemoveDependent(self)
                del self._subscriptions[item]
        self._calculationSpaces = set([ml.CalculationSpace() for ml in self._monitoredLimits.values()])

    def _CheckMonitoredLimit(self, limit):
        try:
            self._CheckLimit(limit)
        except Exception as err:
            self._RemoveLimit(limit)
            raise err

    def _CheckLimit(self, limit):
        logger.debug('Checking value of limit %d...', limit.Oid())
        result = self._GetMonitoredLimit(limit).CheckLimit()
        if result.StateAfter == 'Ready' and result.ErrorMsg:
            logger.warn('Limit {0} references a missing limit target ({1}) and cannot be '
                        'checked'.format(limit.Oid(), limit.LimitTarget().Path()))
            logger.debug(result.ErrorMsg)
            raise MissingLimitTargetError(result.ErrorMsg)
        elif result.StateAfter == 'Error':
            logger.error(result.ErrorMsg)
            raise Exception(result.ErrorMsg)
        return result


class FLimitListener(FLimitMonitor.ILimitListener):

    def __init__(self):
        # pylint: disable-msg=E1101
        super(FLimitListener, self).__init__()
        self._writeLimitValues = FLimitSettings.ServerWriteLimitValues()

    def OnLimitValueChecked(self, checkResult):
        if self._writeLimitValues:
            try:
                lv = checkResult.Limit.LimitValue()
                if lv.CheckedValue() != checkResult.CheckedValue:
                    lv.CheckedValue(checkResult.CheckedValue)
                    lv.Commit()
            except Exception as e:
                logger.error('Error committing limit value for limit %d: %s',
                             checkResult.Limit.Oid(), e)

    def OnLimitWarningEvent(self, checkResult):
        currentState = FLimitUtils.CurrentState(checkResult.Limit)
        if currentState in ('Ready', 'Active', 'Breached'):
            self._LogLimitEvent('entered warning level',
                                checkResult.Limit,
                                checkResult.CheckedValue,
                                FLimitUtils.WarningValue(checkResult.Limit))
            if currentState == 'Ready':
                self._UpdateBusinessProcess('Monitor Limit',
                                            checkResult)
            self._UpdateBusinessProcess('Warn',
                                        checkResult)

    def OnLimitBreachedEvent(self, checkResult):
        currentState = FLimitUtils.CurrentState(checkResult.Limit)
        if currentState in ('Ready', 'Active', 'Warning'):
            self._LogLimitEvent('has been breached',
                                checkResult.Limit,
                                checkResult.CheckedValue,
                                FLimitUtils.Threshold(checkResult.Limit))
            if currentState == 'Ready':
                self._UpdateBusinessProcess('Monitor Limit',
                                            checkResult)
                self._UpdateBusinessProcess('Warn',
                                            checkResult)
            if currentState == 'Active':
                # Must go through warning state first
                self._UpdateBusinessProcess('Warn',
                                            checkResult)
            self._UpdateBusinessProcess('Breach',
                                        checkResult)

    def OnLimitActiveEvent(self, checkResult):
        currentState = FLimitUtils.CurrentState(checkResult.Limit)
        if currentState in ('Ready', 'Warning', 'Breached'):
            self._LogLimitEvent('has returned within limits',
                                checkResult.Limit,
                                checkResult.CheckedValue,
                                FLimitUtils.WarningValue(checkResult.Limit))
            if currentState == 'Ready':
                self._UpdateBusinessProcess('Monitor Limit',
                                            checkResult)
            else:
                self._UpdateBusinessProcess('Recede',
                                            checkResult)

    def OnLimitReadyEvent(self, checkResult):
        if FLimitUtils.CurrentState(checkResult.Limit) != 'Ready':
            self._LogLimitEvent('has been set to Ready',
                                checkResult.Limit,
                                checkResult.CheckedValue,
                                FLimitUtils.WarningValue(checkResult.Limit))
            self._SetLimitToReadyState(checkResult.Limit,
                        'Limit Checked Value is not a numeric value.')
        self.OnLimitValueChecked(checkResult)

    def OnLimitErrorEvent(self, checkResult):
        self._SetLimitToErrorState(checkResult.Limit, checkResult.ErrorMsg)

    def OnLimitUnmonitoredChildren(self, checkResult):
        try:
            acm.BeginTransaction()
            for childResult in checkResult.Children:
                childResult.Limit.Commit()
            acm.CommitTransaction()

            for childResult in checkResult.Children:
                logger.info('Limit %d on "%s" (%s) created for parent limit %d',
                            childResult.Limit.Oid(),
                            FLimitUtils.Constraints(childResult.Limit),
                            FLimitUtils.ColumnName(checkResult.Limit),
                            checkResult.Limit.Oid())
        except RuntimeError as e:
            acm.AbortTransaction()
            logger.error('Failed to commit new child limits: %s', e)

    @classmethod
    def _SetLimitToReadyState(cls, limit, reason=' '):
        bp = limit.BusinessProcess()
        currentState = FLimitUtils.CurrentState(limit)
        if bp and currentState != 'Ready':
            try:
                cls._SetBusinessProcessToReady(bp, reason)
            except Exception as e:
                logger.error('Failed to set business process %d to ready state: %s', bp.Oid(), e)

    @staticmethod
    def _UpdateBusinessProcess(event, checkResult):
        limit = checkResult.Limit
        params = {
            'Threshold value': str(FLimitUtils.Threshold(limit)),
            'Warning value': str(FLimitUtils.WarningValue(limit)),
            'Value at checking': str(checkResult.CheckedValue),
            'Raw checked value': str(checkResult.RawValue),
            'Comparison operator': limit.ComparisonOperator(),
            }
        try:
            bp = limit.BusinessProcess()
            bp.HandleEvent(event, params)
            bp.Commit()
        except AttributeError as e:
            logger.error(e)
        except Exception as e:
            logger.error('Business process %d failed to handle event "%s": %s', bp.Oid(), event, e)

    @staticmethod
    def _SetBusinessProcessToReady(businessProcess, reason = ' '):
        assert(businessProcess)
        assert(reason)
        businessProcess.ForceToState('Ready', reason)
        businessProcess.Commit()

    @staticmethod
    def _SetLimitToErrorState(limit, reason):
        bp = limit.BusinessProcess()
        currentState = FLimitUtils.CurrentState(limit)
        if bp and currentState != 'Error':
            try:
                FBusinessProcessUtils.SetBusinessProcessToError(bp, reason)
            except Exception as e:
                logger.error('Failed to set business process %d to error state: %s', bp.Oid(), e)

    @staticmethod
    def _LogLimitEvent(event, limit, currentValue, notificationValue):
        logger.info('Limit %d on "%s" (%s) %s [%s %s %s]',
                    limit.Oid(),
                    FLimitUtils.Constraints(limit),
                    FLimitUtils.ColumnName(limit),
                    event,
                    currentValue,
                    FLimitUtils.ComparisonOperatorAsSymbol(limit.ComparisonOperator()),
                    notificationValue)