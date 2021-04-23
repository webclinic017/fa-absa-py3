""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/etc/RegInfoCustomMethods.py"

import acm
import traceback
from contextlib import contextmanager


@contextmanager
def TryExcept():
    try:
        yield None
    except Exception as e:
        print(Exception, e)
        print(traceback.format_exc())
        raise e

    
# ########## #
# INSTRUMENT #
# ########## #

def GetStandardMarketSize(insRegInfo):
    with TryExcept():
        standardMarketSize =  insRegInfo.AdditionalInfo().RegSMS()
        if standardMarketSize:
            return standardMarketSize
        else:
            return 0.0

def SetStandardMarketSize(insRegInfo, standardMarketSize):
    with TryExcept():
        insRegInfo.AdditionalInfo().RegSMS(standardMarketSize)
        

def GetTransactionType(insRegInfo):
    with TryExcept():
        return insRegInfo.AdditionalInfo().RegTransactionType()

def SetTransactionType(insRegInfo, transactionType):
    with TryExcept():
        insRegInfo.AdditionalInfo().RegTransactionType(transactionType)


def GetFinalPriceType(insRegInfo):
    with TryExcept():
        return insRegInfo.AdditionalInfo().RegFinalPriceType()

def SetFinalPriceType(insRegInfo, finalPriceType):
    with TryExcept():
        insRegInfo.AdditionalInfo().RegFinalPriceType(finalPriceType)


def GetSimilarIsin(insRegInfo):
    with TryExcept():
        return insRegInfo.AdditionalInfo().RegSimilarIsin()

def SetSimilarIsin(insRegInfo, similarIsin):
    with TryExcept():
        insRegInfo.AdditionalInfo().RegSimilarIsin(similarIsin)


def GetAdmissionRequestTime(insRegInfo):
    with TryExcept():
        requestTime = insRegInfo.AdditionalInfo().RegTrdAdmisReqTime()
        if not requestTime:
            return ""
        else:
            return acm.Time().DateTimeFromTime(requestTime)

def SetAdmissionRequestTime(insRegInfo, requestTime):
    with TryExcept():
        insRegInfo.AdditionalInfo().RegTrdAdmisReqTime(requestTime)


def GetAdmissionApprovalTime(insRegInfo):
    with TryExcept():
        approvalTime = insRegInfo.AdditionalInfo().RegTrdAdmisAppTime()
        if not approvalTime:
            return ""
        else:
            return acm.Time().DateTimeFromTime(approvalTime)

def SetAdmissionApprovalTime(insRegInfo, approvalTime):
    with TryExcept():
        insRegInfo.AdditionalInfo().RegTrdAdmisAppTime(approvalTime)


def GetFirstTradingTime(insRegInfo):
    with TryExcept():
        tradingTime = insRegInfo.AdditionalInfo().RegFirstTradeTime()
        if not tradingTime:
            return ""
        else:
            return acm.Time().DateTimeFromTime(tradingTime)

def SetFirstTradingTime(insRegInfo, tradingTime):
    with TryExcept():
        insRegInfo.AdditionalInfo().RegFirstTradeTime(tradingTime)


def GetTradingTerminationTime(insRegInfo):
    with TryExcept():
        terminationTime = insRegInfo.AdditionalInfo().RegTrdTerminateTime()
        if not terminationTime:
            return ""
        else:
            return acm.Time().DateTimeFromTime(terminationTime)

def SetTradingTerminationTime(insRegInfo, terminationTime):
    with TryExcept():
        insRegInfo.AdditionalInfo().RegTrdTerminateTime(terminationTime)


def GetHasTradingObligation(insRegInfo):
    with TryExcept():
        return insRegInfo.AdditionalInfo().RegHasTrdObligation()

def SetHasTradingObligation(insRegInfo, tradingObligation):
    with TryExcept():
        insRegInfo.AdditionalInfo().RegHasTrdObligation(tradingObligation)
            
            
def GetIsTradedOnTradingVenue(insRegInfo):
    with TryExcept():
        return insRegInfo.AdditionalInfo().RegToTV()

def SetIsTradedOnTradingVenue(insRegInfo, isTraded):
    with TryExcept():
        insRegInfo.AdditionalInfo().RegToTV(isTraded)


def GetLiquidityBand(insRegInfo):
    with TryExcept():
        return insRegInfo.AdditionalInfo().RegLiquidityBand()

def SetLiquidityBand(insRegInfo, liquidityBand):
    with TryExcept():
        insRegInfo.AdditionalInfo().RegLiquidityBand(liquidityBand)

def GetIsMiFIDTransparent(insRegInfo):
    with TryExcept():
        return insRegInfo.AdditionalInfo().RegMiFIDTransparent()

def SetIsMiFIDTransparent(insRegInfo, isMiFIDTransparent):
    with TryExcept():
        insRegInfo.AdditionalInfo().RegMiFIDTransparent(isMiFIDTransparent)
        
def GetFinancialInstrumentShortName(insRegInfo):
    with TryExcept():
        return insRegInfo.AdditionalInfo().RegFISN()

def SetFinancialInstrumentShortName(insRegInfo, financialInstrumentShortName):
    with TryExcept():
        insRegInfo.AdditionalInfo().RegFISN(financialInstrumentShortName)
        

# ##### #            
# TRADE #
# ##### #            

def GetExecutingEntity(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegExecutingEntity()
        
def SetExecutingEntity(tradeRegInfo, executingEntity):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegExecutingEntity(executingEntity)
            
def GetReportingEntity(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegReportingEntity()

def SetReportingEntity(tradeRegInfo, reportingEntity):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegReportingEntity(reportingEntity)
            
def GetVenue(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegVenue()

def SetVenue(tradeRegInfo, venue):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegVenue(venue)
            
def GetRepositoryId(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegRepositoryId()

def SetRepositoryId(tradeRegInfo, repositoryId):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegRepositoryId(repositoryId)
        
def GetAlgoId(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegAlgoId()

def SetAlgoId(tradeRegInfo, algoId):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegAlgoId(algoId)
        
def GetExchangeId(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegExchangeId()

def SetExchangeId(tradeRegInfo, exchangeId):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegExchangeId(exchangeId)
        
def GetComplexTradeComponentId(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegComplexTrdCmptId()

def SetComplexTradeComponentId(tradeRegInfo, id):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegComplexTrdCmptId(id)
        
def GetIsCommodityDerivative(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegComdtyDerivInd()

def SetIsCommodityDerivative(tradeRegInfo, isCommodityDerivative):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegComdtyDerivInd(isCommodityDerivative)
        
def GetIsSecurityFinancingTransaction(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegSecFinTransInd()

def SetIsSecurityFinancingTransaction(tradeRegInfo, isSecFin):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegSecFinTransInd(isSecFin)
        
def GetInvestmentDeciderCrmId(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegInvesDecidrCrmId()

def SetInvestmentDeciderCrmId(tradeRegInfo, crmId):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegInvesDecidrCrmId(crmId)
        
def GetCfiCode(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegInsCfiCode()

def SetCfiCode(tradeRegInfo, cfiCode):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegInsCfiCode(cfiCode)
        
def GetIsinTrade(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegInsIsin()

def SetIsinTrade(tradeRegInfo, isin):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegInsIsin(isin)

def GetNearLegIsin(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegNearLegIsin()

def SetNearLegIsin(tradeRegInfo, isin):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegNearLegIsin(isin)

def GetFarLegIsin(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegFarLegIsin()

def SetFarLegIsin(tradeRegInfo, isin):
    with TryExcept():
        tradeRegInfo.AdditionalInfo().RegFarLegIsin(isin)

def GetIsProvidingLiquidity(tradeRegInfo):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegProvideLiquidity()

def SetIsProvidingLiquidity(tradeRegInfo, isProvidingLiquidity):
    with TryExcept():
        return tradeRegInfo.AdditionalInfo().RegProvideLiquidity(isProvidingLiquidity)



