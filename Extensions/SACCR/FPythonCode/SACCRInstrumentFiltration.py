""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/saccr/./etc/SACCRInstrumentFiltration.py"
import acm

import AAParamsAndSettingsHelper
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()
    
def IsValidForSACCR(instrument, isOpenPosition):
    # This function is called by FilterSACCRInstruments and also from ADFL for Adaptiv Base Valuation
    if isOpenPosition:
        if instrument.IsKindOf("FSwap"):
            return True

    return False

def FilterSACCRInstruments(instruments, isOpenPositionArray):
    saccrInstruments = acm.FArray()
    for instrument, isOpenPosition in zip(instruments, isOpenPositionArray):
        if isOpenPosition:
            if IsValidForSACCR(instrument, isOpenPosition):
                saccrInstruments.Add(instrument)
            else:
                logger.ELOG("Can't calculate SACCR for instrument %s of type %s" %(instrument.Name(), instrument.Class().Name()))
 
    return saccrInstruments