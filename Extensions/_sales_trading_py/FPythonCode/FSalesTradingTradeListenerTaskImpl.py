""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FSalesTradingTradeListenerTaskImpl.py"
"""--------------------------------------------------------------------------
MODULE
    FSalesTradingTradeListenerTaskImpl

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
# pylint: disable-msg=W0603,W0602
from FSalesTradingLogging import logger
from FParameterSettings import ParameterSettingsCreator
from FTrade2SalesActivityTradeListener import Trade2SalesActivityTradeListener

#
# - Expected parameters:
# OnTradeHook=<module>.<function>
# ServerLoggingLevel=<integer 1-3>
# InitializationHook=<module>.<function>

tradeListener = None

def DoStart():
    global tradeListener
    try:
        parameters = ParameterSettingsCreator.FromRootParameter('SalesTradingTradeListener')

        logger.Reinitialize(int(parameters.ServerLoggingLevel()))

        tradeListener = Trade2SalesActivityTradeListener()
        logger.info('Starting SalesTradingTradeListenerTaskImpl')
        tradeListener.StartSubscription()
        logger.info('SalesTradingTradeListenerTaskImpl started')
    except Exception as stderr:
        logger.error('SalesTradingTradeListenerTaskImpl.start() Exception: %s' % stderr)
        logger.error(stderr, exc_info=True)

def DoWork():
    global tradeListener
    if tradeListener:
        tradeListener.Work()

def DoStop():
    global tradeListener
    try:
        if tradeListener:
            tradeListener.EndSubscription()
            logger.info('SalesTradingTradeListenerTaskImpl stop')
            tradeListener = None
        else:
            logger.error('SalesTradingTradeListenerTaskImpl No trade listener, can not stop')
    except Exception as stderr:
        logger.error('SalesTradingTradeListenerTaskImpl.stop() Exception: %s' % stderr)
        logger.error(stderr, exc_info=True)
