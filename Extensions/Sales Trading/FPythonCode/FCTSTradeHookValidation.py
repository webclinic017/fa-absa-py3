""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSTradeHookValidation.py"
"""--------------------------------------------------------------------------
MODULE
    FCTSTradeHookValidation

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

from FSalesTradingLogging import logger

def Validate(salesActivity):
    validDealPackages = ['ASCOT', 'ASCOTOnSwap', 'ASCOTTrade', 'CBOriginalOption', 'CBTrade', 'EquityDerivativeOnSwap', 'InstrumentOnSwap']

    if not salesActivity.Trade():
        logger.warn("FCTSTradeHookValidation.Validate() No trade")
        return False

    if salesActivity.Trade().Status() == 'Simulated':
        logger.debug("FCTSTradeHookValidation.Validate() Status for trade %d is Simulated" % salesActivity.Trade().Oid())
        return False

    if not salesActivity.Trade().DealPackage():
        logger.warn("FCTSTradeHookValidation.Validate() No Deal Package for trade %d" % salesActivity.Trade().Oid())
        return False

    dealPackageName = salesActivity.Trade().DealPackage().DefinitionName()
    if dealPackageName in validDealPackages:
        return True
    else:
        logger.debug("FCTSTradeHookValidation.Validate() Trade %d in unsupported Deal Package '%s'" % (salesActivity.Trade().Oid(), dealPackageName))
        return False
