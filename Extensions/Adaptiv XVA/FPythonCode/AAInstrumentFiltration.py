""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAInstrumentFiltration.py"
import acm
import AACustomDealsCreator as cdc
import AACfInstrumentDealCCSwap
import AACfInstrumentDealSwaption
import AAParamsAndSettingsHelper
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

def isValidSwaption(swaption):
    if swaption.ExerciseType() not in ["European", "Bermudan"]:
        logger.LOG("Swaption %s is not of type European or Bermudan and will be excluded from CVA calculation" % str(swaption.Name()))
        return False
    if swaption.PayType() != "Spot":
        logger.LOG("Swaption %s has pay type different from Spot and will be excluded from CVA calculation" % str(swaption.Name()))
        return False
    if swaption.SettlementType() != "Physical Delivery":
        logger.LOG("Swaption %s has settlement type different from Physical Delivery and will be excluded from CVA calculation" % str(swaption.Name()))
        return False
    if swaption.QuantoOptionType() != "None":
        logger.LOG("Swaption %s has quanto feature and will be excluded from CVA calculation" % str(swaption.Name()))
        return False
    if swaption.Digital():
        logger.LOG("Swaption %s is digital and will be excluded from CVA calculation" % str(swaption.Name()))
        return False
    if not AACfInstrumentDealSwaption.AASwaptionDeal.sameDiscountCurves(swaption):
        logger.LOG("Discount curve of swaption %s is not the same as its underlying's discount curve and will be excluded from CVA calculation" % str(swaption.Name()))
        return False
    return True
    
def isValidIndexLinkedInstrument(instrument):
    # TODO: This logic needs to be more extensive.
    for l in instrument.Legs():
        if l.LegType() in ["Fixed", "Fixed Accretive"]:
            if l.NominalScaling() not in ("None", "CPI", "CPI Fixing In Arrears"):
                logger.LOG("Fixed leg of Swap %s has unsupported Nominal Scaling type %s and will be excluded from CVA calculation" %(str(instrument.Name()), str(l.NominalScaling())))
                return False
        elif l.LegType() == "Float":
            if l.NominalScaling() not in ("None"):
                logger.LOG("Float leg of Swap %s has unsupported Nominal Scaling type %s and will be excluded from CVA calculation" %(str(instrument.Name()), str(l.NominalScaling())))
                return False
        elif l.LegType() == "Zero Coupon Fixed":
            if l.NominalScaling() not in ("None"):
                logger.LOG("Zero coupon fixed leg of Swap %s has unsupported Nominal Scaling type %s and will be excluded from CVA calculation" %(str(instrument.Name()), str(l.NominalScaling())))
                return False
        else:
            logger.LOG("Leg type %s not implemented for index linked instrument %s and will be excluded from CVA calculation" %(l.LegType(), str(l.NominalScaling())))
            return False
    return True

def isValidCrossCurrencySwap(ccy_swap):
    if not isValidCflInst(ccy_swap):
        return False
    
    if AACfInstrumentDealCCSwap.AAMtMCrossCurrencySwapDeal.hasFXNominalScaling(ccy_swap):
        for l in ccy_swap.Legs():
            if l.PayOffsetCount() > 0:
                logger.LOG("Currency Swap %s with reset nominal property has pay offset and will be excluded from CVA calculation." %str(ccy_swap.Name()))
                return False
            for cf in l.CashFlows():
                if cf.IsManuallyEdited():
                    logger.LOG("Currency Swap %s with reset nominal property has manually edited cash flows and will be excluded from CVA calculation." %str(ccy_swap.Name()))
                    return False
    return True

def isValidCflInst(inst):
    if inst.NonDeliverable():
        logger.LOG("inst %s has Non-Deliverable feature and will be excluded from CVA calculation." %str(inst.Name()))
        return False
    
    for l in inst.Legs():
        if l.LegType() in ["Fixed", "Fixed Accretive"]:
            pass
        elif l.LegType() == "Zero Coupon Fixed":
            pass
        elif l.LegType() in ["Capped Float", "Floored Float", "Collared Float"]:
            pass
        elif l.LegType() == "Float":
            if str(l.ResetType()) not in ["Single", "Compound", "Weighted", "Unweighted"]:
                logger.LOG("Swap %s has unsupported reset type %s and will be excluded from CVA calculation" %(str(swap.Name()), str(l.ResetType())))
                return False
            for cashFlow in l.CashFlows():
                if cashFlow.CashFlowType() == "Float Rate" and cashFlow.FloatRateFactor() != 1.0:
                    logger.LOG("Swap %s has float rate factors different from 1.0 and will be excluded from CVA calculation" % str(swap.Name()))
                    return False
        else:
            logger.LOG("Swap %s has unsupported leg type %s and will be excluded from CVA calculation" %(str(swap.Name()), str(l.LegType())))
            return False
    return True

def isSupportedFxOption(option):

    if not option.IsExotic():
        return True
    
    if option.Digital():
        acm.Log("Digital option %s "
"currently is not supported yet." % (option.Name()))
        logger.LOG("Digital option %s "
"currently is not supported yet." % (option.Name()))
        return False
        
    exotics = option.Exotics()
    if len(exotics) > 1:
        acm.Log("Not support Option %s "
"that has more than one exotic feature." % (option.Name()))
        logger.LOG("Not support Option %s "
"that has more than one exotic feature." % (option.Name()))
        return False
    
    barrierType = str(exotics[0].BarrierOptionType())
    if barrierType in ["Custom", "None"]:
        acm.Log("Barrier type %s on Option %s "
"currently is not supported." % (barrierType, option.Name()))
        logger.LOG("Barrier type %s on Option %s "
"currently is not supported." % (barrierType, option.Name()))
        return False
        
    return True     

def isValidFxOption(fxoption):
    return isSupportedFxOption(fxoption)

def isSupportedCDS(instrument):
    if (instrument == None):
        logger.LOG("isSupportedCDS: instrument object passed is None")
        return False

    instrName = instrument.Name()
    payLeg = instrument.PayLeg()
    recLeg = instrument.RecLeg()

    if (payLeg == None or recLeg == None):
        logger.LOG("isSupportedCDS({0}): one of leg of the CDS is None".format(instrName))
        return False

    # exactly one must be of type 'Credit Default'
    exactlyOneLegTypeIsCDS = bool(payLeg.LegType() == 'Credit Default') ^ bool(recLeg.LegType() == 'Credit Default')
    if (not exactlyOneLegTypeIsCDS):
        logger.LOG("isSupportedCDS({0}): exactly one leg should be of 'Credit Default' type".format(instrName))
        return False

    noFloatLegs = payLeg.LegType() != 'Float' and recLeg.LegType() != 'Float'
    if (not noFloatLegs):
        logger.LOG("isSupportedCDS({0}): cds contains Float leg - not supported by Adaptiv Analytics".format(instrument.Name()))

    return noFloatLegs


def IsValidForCVA(instrument, isOpenPosition):
    # This function is called by FilterCVAInstruments and also from ADFL for Adaptiv Base Valuation
    if isOpenPosition:
        if cdc.CustomDealModelCall(instrument):
            return True
        if instrument.IsKindOf("FCommodity"):
            return True
        elif instrument.IsKindOf("FStock"):
            return True
        elif instrument.IsKindOf("FCurrency"):
            return True
        elif instrument.IsKindOf("FTotalReturnSwap"):
            return True
        elif instrument.IsKindOf("FCurrencySwap"):
            if isValidCrossCurrencySwap(instrument):
                return True
        elif instrument.IsKindOf("FIndexLinkedSwap") or instrument.IsKindOf("FIndexLinkedBond"):
            if isValidIndexLinkedInstrument(instrument):
                return True
        elif instrument.IsKindOf("FFxRate"):
            return True
        elif instrument.IsKindOf("FCreditDefaultSwap"):
            return isSupportedCDS(instrument)
        elif instrument.IsKindOf("FOption"):
            if instrument.Underlying().IsKindOf("FSwap"):
                if isValidSwaption(instrument):
                    return True
            if instrument.Underlying().IsKindOf("FCurrencySwap"):
                if isValidCrossCurrencySwap(instrument):
                    return True
            elif instrument.Underlying().IsKindOf("FCurrency"):
                if isValidFxOption(instrument):
                    return True
            elif instrument.Underlying().IsKindOf("FCommodity"):
                return True
            elif instrument.Underlying().IsKindOf("FStock"):
                return True
            elif instrument.Underlying().IsKindOf("FBond"):
                return True
        elif instrument.IsKindOf("FFuture"):
            if instrument.Underlying().IsKindOf("FCommodity"):
                return True
            elif instrument.Underlying().IsKindOf("FIndexLinkedBond"):
                return True
            elif instrument.Underlying().IsKindOf("FBond"):
                return True
        elif instrument.IsKindOf("FCap") or instrument.IsKindOf("FFloor"):
            return True
        elif instrument.IsKindOf("FFra"):
            return True
        elif instrument.IsKindOf("FCashFlowInstrument"):
            if isValidCflInst(instrument):
                return True
    return False

def FilterCVAInstruments(instruments, isOpenPositionArray):
    cvaInstruments = acm.FArray()
    for instrument, isOpenPosition in zip(instruments, isOpenPositionArray):
        if isOpenPosition:
            if IsValidForCVA(instrument, isOpenPosition):
                cvaInstruments.Add(instrument)
            else:
                logger.ELOG("Can't calculate CVA for instrument %s of type %s" %(instrument.Name(), instrument.Class().Name()))
 
    return cvaInstruments
