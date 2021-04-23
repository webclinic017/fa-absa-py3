""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendWorkflow.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    FSecLendWorkflow

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

****************************************************************
**************** This is for our internal testing        *******
****************************************************************

-----------------------------------------------------------------------------"""
import acm
from contextlib import contextmanager

import FBusinessProcessUtils
import FLimitActions
import FLimitMonitor
import FLimitSettings
import FLimitUtils
import FSecLendHooks
import FSecLendUtils
from FParameterSettings import ParameterSettingsCreator
from FWorkflow import ActionState, Workflow

SETTINGS = ParameterSettingsCreator.FromRootParameter('WorkflowATSSettings')


class SecLendWorkflow(Workflow):
    INCLUDE_IN_CALCULATION_STATUS = FSecLendHooks.ApprovedTradeStatus()

    StateChartDefinition = FSecLendHooks.WorkflowStateChart

    @classmethod
    def StateChart(cls):
        return cls.StateChartDefinition.NAME

    @ActionState
    def Ready(self):
        event, parameters, notes = FSecLendHooks.Ready_WorkflowHook(self)
        if not event:
            event = "Start"
            parameters = FSecLendUtils.ColumnValuesFromExtensionattribute(self.Subject(),
                                                                       "_SecurityLoan_Reporting_Columns")
        return event, parameters, notes

    # ------------------------------- Limit checks -------------------------------------
    @ActionState
    def Validating(self):
        event, parameters, notes = FSecLendHooks.Validating_WorkflowHook(self)
        if not event:
            self.Subject().AddInfoValue("SBL_PendingOrder", False)
            self.Subject().Commit()
            isvalid_forProcessing, tooltip = FSecLendHooks.IsValidForProcessing(self.Subject())
            if tooltip:
                notes.append("Order Validation: {0}".format(tooltip))
            if SETTINGS.EnableLimitChecks():
                limits_results = self.LimitCheck(self.Subject())
                isvalid_limits = 'Breached' not in [res.StateAfter for res in limits_results]
                if SETTINGS.ServerLimitCheckCreateReport():
                    parameters.update(self.LimitCheckReportFile(limits_results, self.BusinessProcess().StringKey()))
                    if not isvalid_limits:
                        notes.append("Limit Validation failed")
                return ('OK' if all([isvalid_forProcessing, isvalid_limits]) else 'Failed'), parameters, notes
            return ('OK' if all([isvalid_forProcessing]) else 'Failed'), parameters, notes
        return event, parameters, notes

    @staticmethod
    def LimitCheckReportFile(results, fileName):
        parameters = {}
        reportId = FLimitActions.CreateCheckReportFile(results, fileName)
        parameters.update({'Report': reportId})
        parameters.update({'Storage': FLimitSettings.Storage()})
    
        return parameters

    @classmethod
    def LimitCheck(cls, trade):
        results = list()
        cls.ValidateTradeNotInCalculation(trade)
        limits = cls.RelevantLimits(trade)
        with cls.TransientCopy(trade) as checkTrade:
            for limit in limits:
                monitoredLimit = FLimitMonitor.FMonitoredLimit(limit)
                results.append(monitoredLimit.CheckLimit([checkTrade]))
        return results

    @staticmethod
    def ValidateTradeNotInCalculation(trade):
        param = acm.GetFunction('mappedValuationParameters', 0)().Parameter()
        if trade.IncludeInCalculations(
                param.IncludeSimulatedTrades(),
                param.IncludeReservedTrades()):
            raise Exception(
                'Can\'t perfrom pre-deal limit check since trade "{0}" is already '
                'in a Status that is included in calculations.'.format(trade.Oid()))

    @staticmethod
    @contextmanager
    def TransientCopy(trade):
        copy = acm.FTrade().Apply(trade)
        copy.Status(SETTINGS.ServerLimitCheckTradeStatus())
        copy.Simulate()
        try:
            yield copy
        finally:
            copy.Unsimulate()

    @staticmethod
    def RelevantLimits(trade):
        relevantLimits = set()
        limitsByTrade = acm.Limits.FindByTrade(trade)
        relevantLimits.update([limit for limit in limitsByTrade
                               if FLimitUtils.IsActive(limit)])
        return relevantLimits

def WorkflowBP(trade):
    try:
        bp = acm.BusinessProcess.FindBySubjectAndStateChart(trade, SecLendWorkflow.StateChart())[0]
    except IndexError:
        return None
    return bp


def WorkflowBPHandleEvent(trade, event, parameters={}):
    try:
        bp = WorkflowBP(trade)
        if bp and FBusinessProcessUtils.IsValidEvent(bp, event):
            bp.HandleEventEx(event, parameters)
            bp.Undo()
    except IndexError:
        return None
    return bp


class TradeHandler(object):

    def __init__(self, trade):
        self._trade = trade

    def StartWorkflow(self, bp_executed):
        #Commit here in batch
        if FSecLendHooks.IsValidForOrderWorkflow(self._trade):
            bp_executed[1] += 1
            return SecLendWorkflow.InitializeFromSubject(self._trade).BusinessProcess()

