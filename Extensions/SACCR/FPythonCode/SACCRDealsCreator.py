""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/saccr/./etc/SACCRDealsCreator.py"
import acm
import AAParamsAndSettingsHelper

import SACCRInstrumentDealSwap

logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

def createSACCRTagString(inst):
    tags = ''
    if inst.IsKindOf('FSwap'):
        tags = '&lt;NONE&gt;,0,Interest Rate,' + inst.PayLeg().Currency().Name() + ':' + inst.RecLeg().Currency().Name() + ',Swap,False'
    return tags
        
def createSACCRSwapDealString(swap, portfolioTradeQuantities, staticLegInformations, valuationDate, mtm, creditBalance, collateralAgreement):
    AASwap = SACCRInstrumentDealSwap.SACCRSwapDeal(swap, portfolioTradeQuantities, staticLegInformations, valuationDate, mtm, creditBalance, collateralAgreement)
    return AASwap.get()

def getSACCRDealModelCall(instrument):
    if instrument.IsKindOf('FSwap'):
        return 'createSACCRSwapDealStringModelCall'
    
    logger.ELOG("Instrument %s of type %s is not supported for SACCR." %(instrument.Name(), instrument.Class().Name()))
    return ''
