""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendWorkflowATS.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    FSecLendWorkflowATS

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    ATS for creating Business Processes, executing Action States and
    moving the Business Process for Workflow implementations. The ATS will
    handle Action States for all State Charts with a workflow implementation
    that is included in the FParameter WorkflowATSSettings.Implementations.
    The parameter should be defined as a list of <moduleName>.<className>
    where the workflow is implemented.

-----------------------------------------------------------------------------
"""
import acm
import ael
import traceback

import FSecLendHoldTrade
import FWorkflowATS
from FSecLendUtils import fn_timer, ActiveLoansBaseQuery
from FSecLendWorkflow import SETTINGS, TradeHandler
from FWorkflow import Logger
from ACMPyUtils import Transaction

logger = Logger()


def start():
    FWorkflowATS.start()
    RecoverTrades()
    logger.info('Starting trade subscriptions.')
    ael.Trade.subscribe(TradesCB)
    FSecLendHoldTrade.start()


def work():
    FWorkflowATS.work()
    FSecLendHoldTrade.work()


def stop():
    FWorkflowATS.stop()
    ael.Trade.unsubscribe(TradesCB)
    FSecLendHoldTrade.stop()


def AutomaticRecheck(bp, bp_executed):
    # This function rechecks the validation of the trade when it gets modified
    # Do not include a state having an EntryState/ActionState modifying the trade
    if bp :
        logger.debug('Creating business process "{0}"...'''.format(bp.Oid()))
        if bp.CurrentStateName() == "Validation failed" and bp.CanHandleEvent('Re-check'):
            bp.HandleEventEx("Re-check")
            bp.Undo()
            bp_executed[0] += 1
        elif bp.CurrentStep().IsInErrorState():
            bp.HandleEventEx("Revert")
            bp.Undo()
            bp_executed[0] += 1

def ModifyTrade(bp):
    # This function rechecks the validation of the trade when it gets modified
    # Do not include a state having an EntryState/ActionState modifying the trade
    if bp and bp.CurrentStateName() == "Booked" and bp.CanHandleEvent('Modify Trade'):
        bp.HandleEventEx("Modify Trade")
        bp.Undo()

def TradesCB(ael_table, ael_entity, arg, event):
    if event in ['insert', 'update']:
        try:
            trade = acm.Ael.AelToFObject(ael_entity)
            bp = TradeHandler(trade).StartWorkflow([0,0])
            if event == 'update' and trade.UpdateUser() != acm.User(): #ATS workflow User should not be used anywhere
                AutomaticRecheck(bp, [0,0])
                #ModifyTrade(bp)
        except:
            logger.error(traceback.format_exc())


@fn_timer
def RecoverTrades():
    query = ActiveLoansBaseQuery()
    dt = acm.Time.PeriodSymbolToDate(SETTINGS.RecoverFrom())
    query.AddAttrNode('UpdateTime', 'GREATER_EQUAL', dt)
    trades = query.Select()
    logger.info('Recovering the valid trades out of {} Trades for date > {}...'.format(len(trades), SETTINGS.RecoverFrom()))
    bp_executed = [0, 0]
    for chuned_trades in [trades[x:x+SETTINGS.ChunkSize()] for x in range(0, len(trades), SETTINGS.ChunkSize())]:
        with Transaction():
            for trade in chuned_trades:
                bp = TradeHandler(trade).StartWorkflow(bp_executed)
                AutomaticRecheck(bp, bp_executed)
    logger.info('RecoverTrades: Automatic Re-check executed on {} Business Processes.'.format(bp_executed[0]))
    logger.info('RecoverTrades: {} Business Processes initialized.'.format(bp_executed[1]))
