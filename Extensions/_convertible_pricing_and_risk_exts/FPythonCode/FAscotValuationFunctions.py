""" Compiled: 2017-11-06 12:31:15 """

#__src_file__ = "extensions/ConvertiblePricingAndRisk/etc/FAscotValuationFunctions.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FAscotValuationFunctions -

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()

def GetDecoratedIfExists(obj):
    if hasattr(obj, 'DecoratedObject'):
        return obj.DecoratedObject()
    return obj

def _CreateAndInsertExoticWithSwap(option, swap, exotics):
    exotic = acm.FExotic()
    exotic.BarrierOptionType('Custom')
    exotic.Instrument(option)
    exotic.OutsideBarrierInstrument(swap)
    exotics.Add(exotic)

def SetRecallSwap(option, swap):
    if not hasattr(option, 'Exotics'):
        logger.DLOG("First argument must have an Exotics reference")
        return
    swap = GetDecoratedIfExists(swap)
    option.ExoticType('Other')
    originalOption = GetDecoratedIfExists(option)
    exotics = option.Exotics()
    if len(exotics) == 0:
        _CreateAndInsertExoticWithSwap(originalOption, swap, exotics)
    elif len(exotics) == 1:
        exotic = exotics[0]
        exotic.BarrierOptionType('Custom')
        exotic.Instrument(originalOption)
        exotic.OutsideBarrierInstrument(swap)
    else:
        logger.DLOG("Exotics table for %s has more than one entry, aborting")
        return

def GetRecallSwap(option):
    if not hasattr(option, 'Exotics'):
        logger.DLOG("First argument must have an Exotics reference")
        return
    exotics = option.Exotics()
    if len(exotics) == 1:
        return exotics[0].OutsideBarrierInstrument()
    else:
        logger.DLOG("The ascot %s does not reference any recall swap through the Exotics table" % option.Name())
        return None

def GetQuotationAsClean(quotation):
    if not hasattr(quotation, 'Clean'):
        logger.DLOG("Argument must be of type FQuotation")
        return
    if not quotation.Clean():
        cleanQuotation = quotation.Clone()
        cleanQuotation.Clean(True)
        return cleanQuotation
    else:
        return quotation
