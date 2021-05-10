""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendHoldTrade.py"
"""--------------------------------------------------------------------------
MODULE
    FSecLendHoldTrade
    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.
    
DESCRIPTION
    Module with functions for setting a trade to status Reserved for a 
    specified amount of time. Requires Additional Info SBL_HoldTime on FTrade
-----------------------------------------------------------------------------"""
import acm
from datetime import datetime

import FSecLendHooks
from ACMPyUtils import Transaction
from FSecLendWorkflow import WorkflowBPHandleEvent
from FSecLendWorkflow import SETTINGS
from FWorkflow import Logger
import FSecLendUtils
from FSecLendUtils import ActiveLoansBaseQuery

logger = Logger()


def UnholdTrade(trade):
    trade.AddInfoValue("SBL_HoldTime", None)
    trade.Status(FSecLendHooks.DefaultTradeStatus())


def HoldTrade(trade, time=None):
    defaultTime = time if time else FSecLendHooks.DefaultHoldTime(trade)
    if not HasTimePast(defaultTime):
        trade.AddInfoValue("SBL_HoldTime", str(defaultTime))
        trade.Status(FSecLendHooks.OnHoldTradeStatus())
    else:
        UnholdTrade(trade)


def HasTimePast(time):
    timeNow = datetime.now()
    return time < timeNow


def IsTimePastHoldTime(trade):
    holdTime = trade.AddInfoValue("SBL_HoldTime")
    timeNow = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
    return holdTime < timeNow


def start():
    logger.info('Starting Reservation task.')


def getReservedTrades():
    query = ActiveLoansBaseQuery()
    query.AddAttrNode('status', 'EQUAL', FSecLendHooks.OnHoldTradeStatus())
    return query.Select()


def work():
    """
    This function will Unhold trades that are in reserved "trade status" and "order status"
    At recovery, trades in "awaiting reply" status and having a holdtime, will be hold by the workflow ATS
    and then their expiry will get rechecked here.
    """
    for trade in getReservedTrades():
        if IsTimePastHoldTime(trade):
            with Transaction():
                WorkflowBPHandleEvent(trade, 'Reject')


def stop():
    if SETTINGS.UnHoldAtShutDown():
        logger.info('Stopping Trade Reservation task. Unholding all reserved Orders...')
        for trade in getReservedTrades():
            with Transaction():
                WorkflowBPHandleEvent(trade, "Reply received",
                                      {"Reply Message": "Order unreserved due to workflow ATS Shutdown"})
