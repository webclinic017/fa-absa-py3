
import acm
import math
import FRoutingFunctionsUtil
       

def PreciousMetalFilter(instrument):
    underlying = instrument.Underlying() if instrument else None
    return underlying.SettlementType() == 'Physical Delivery' if underlying else False

def CoverInstrumentChoices():
    return acm.FCommodityVariant.Instances().Filter(PreciousMetalFilter) 
    
def PreciousMetalPairChoices():
    return acm.FPreciousMetalPair.Instances()

'''****************************************************************************************
*
* FXB2B
*
****************************************************************************************'''
def FXB2B( trade, operationParameters ):
    FRoutingFunctionsUtil.ValidateInstrumentAndTrade( trade )
    constellationParameters, defaultParamsDecorator = FRoutingFunctionsUtil.TradeConstellationParamters(trade)
    FRoutingFunctionsUtil.SetB2BParamsFromOperationParams(trade, defaultParamsDecorator, operationParameters, False, False, False)
    
    defaultParameters = defaultParamsDecorator.Parameters()
    
    FRoutingFunctionsUtil.SetB2BParametersFromDefault(constellationParameters, defaultParameters)
    return [constellationParameters.AllocateFXRisk()]

'''****************************************************************************************
*
* FXSpotCover
*
****************************************************************************************'''
def FXSpotCover( trade, operationParameters ):
    FRoutingFunctionsUtil.ValidateInstrumentAndTrade( trade )

    constellationParameters, defaultParamsDecorator = FRoutingFunctionsUtil.TradeConstellationParamters(trade)
    defaultParamsDecorator.SpotCoverEnabled(True)
    defaultParamsDecorator.SpotCoverPortfolio = operationParameters.Portfolio1()
    defaultParamsDecorator.SpotCoverPositionPair= FRoutingFunctionsUtil.GetPositionPair(operationParameters.PositionPair1(), operationParameters.Portfolio1())
    defaultParamsDecorator.SpotCoverAcquirer = operationParameters.Acquirer1()
    defaultParamsDecorator.SpotCoverCurrency = operationParameters.CoverInstrument()
    FRoutingFunctionsUtil.SetB2BParamsFromOperationParams(trade, defaultParamsDecorator, operationParameters, True, False, False)
    
    defaultParameters = defaultParamsDecorator.Parameters()
    FRoutingFunctionsUtil.SetSpotCoverParametersFromDefault(constellationParameters, defaultParameters)
    FRoutingFunctionsUtil.SetB2BParametersFromDefault(constellationParameters, defaultParameters)

    return [constellationParameters.AllocateFXRisk()]

'''****************************************************************************************
*
* FXSplit
*
****************************************************************************************'''
def FXSplit( trade, operationParameters ):
    FRoutingFunctionsUtil.ValidateInstrumentAndTrade( trade )
    
    constellationParameters, defaultParamsDecorator = FRoutingFunctionsUtil.TradeConstellationParamters(trade)
    
    defaultParamsDecorator.SplitPortfolio = operationParameters.Portfolio1()
    defaultParamsDecorator.SplitAcquirer = operationParameters.Acquirer1()
    defaultParamsDecorator.UpdateSwapToSpotEnabled()
    if defaultParamsDecorator.SwapToSpotEnabled():
        FRoutingFunctionsUtil.SetSwapToSpotFromOperationParameters(defaultParamsDecorator, operationParameters)
    FRoutingFunctionsUtil.SetB2BParamsFromOperationParams(trade, defaultParamsDecorator, operationParameters, False, True, False)

    defaultParameters = defaultParamsDecorator.Parameters()
    FRoutingFunctionsUtil.SetSplitParametersFromDefault(constellationParameters, defaultParameters)
    
    FRoutingFunctionsUtil.SetSwapToSpotParamsFromDefault(constellationParameters, defaultParameters)
    FRoutingFunctionsUtil.SetB2BParametersFromDefault(constellationParameters, defaultParameters)

    return [constellationParameters.AllocateFXRisk()]     
        
'''****************************************************************************************
*
* FXSplitAndSpotCover
*
****************************************************************************************'''
def FXSplitAndSpotCover( trade, operationParameters ):
    FRoutingFunctionsUtil.ValidateInstrumentAndTrade( trade )

    constellationParameters, defaultParamsDecorator = FRoutingFunctionsUtil.TradeConstellationParamters(trade)
    
    defaultParamsDecorator.SplitPortfolio = operationParameters.Portfolio1()
    defaultParamsDecorator.SplitAcquirer = operationParameters.Acquirer1()
    
    defaultParamsDecorator.SpotCoverEnabled(True)
    defaultParamsDecorator.SpotCoverPortfolio = operationParameters.Portfolio2()
    defaultParamsDecorator.SpotCoverPositionPair = FRoutingFunctionsUtil.GetPositionPair(operationParameters.PositionPair2(), operationParameters.Portfolio2())
    defaultParamsDecorator.SpotCoverAcquirer = operationParameters.Acquirer2()
    defaultParamsDecorator.SpotCoverCurrency = operationParameters.CoverInstrument()
    FRoutingFunctionsUtil.SetB2BParamsFromOperationParams(trade, defaultParamsDecorator, operationParameters, True, True, False)
    defaultParameters = defaultParamsDecorator.Parameters()
    
    FRoutingFunctionsUtil.SetSplitParametersFromDefault(constellationParameters, defaultParameters)
    FRoutingFunctionsUtil.SetSpotCoverParametersFromDefault(constellationParameters, defaultParameters)
    FRoutingFunctionsUtil.SetB2BParametersFromDefault(constellationParameters, defaultParameters)

    return [constellationParameters.AllocateFXRisk()]


'''****************************************************************************************
*
* FXSplitAndSpotCoverWithFXSplit
*
****************************************************************************************'''
def FXSplitAndSpotCoverWithFXSplit ( trade, operationParameters ):
    FRoutingFunctionsUtil.ValidateInstrumentAndTrade( trade )
    constellationParameters = FRoutingFunctionsUtil.ConstellationParametersForSplitAndSpotCoverWithFXSplit(trade, operationParameters, True)
    return [constellationParameters.AllocateFXRisk()]    

'''****************************************************************************************
*
* FXSpotCoverWithFXSplit
*
****************************************************************************************'''
def FXSpotCoverWithFXSplit( trade, operationParameters ):
    FRoutingFunctionsUtil.ValidateInstrumentAndTrade( trade )
        
    constellationParameters, defaultParamsDecorator = FRoutingFunctionsUtil.TradeConstellationParamters(trade)
    defaultParamsDecorator.SpotCoverEnabled(True)
    defaultParamsDecorator.SpotCoverPortfolio = operationParameters.Portfolio1()
    defaultParamsDecorator.SpotCoverPositionPair = FRoutingFunctionsUtil.GetPositionPair(operationParameters.PositionPair1(), operationParameters.Portfolio1())
    defaultParamsDecorator.SpotCoverAcquirer = operationParameters.Acquirer1()
    defaultParamsDecorator.SpotCoverSplitPortfolio = operationParameters.Portfolio2()
    defaultParamsDecorator.SpotCoverSplitAcquirer = operationParameters.Acquirer2()
    defaultParamsDecorator.SpotCoverCurrency = operationParameters.CoverInstrument()    
    defaultParamsDecorator.UpdateSwapToSpotEnabled()
    if defaultParamsDecorator.SwapToSpotEnabled():
        FRoutingFunctionsUtil.SetSwapToSpotFromOperationParameters(defaultParamsDecorator, operationParameters)

    defaultParameters = defaultParamsDecorator.Parameters()
    
    FRoutingFunctionsUtil.SetSpotCoverParametersFromDefault(constellationParameters, defaultParameters)
    FRoutingFunctionsUtil.SetSpotCoverWithSplitParametersFromDefault(constellationParameters, defaultParameters)
    FRoutingFunctionsUtil.SetSwapToSpotParamsFromDefault(constellationParameters, defaultParameters)
    
    return [constellationParameters.AllocateFXRisk()]    

'''****************************************************************************************
*
* FXStandardNoCoverTradeAndOperationParametersOverrideHook
*
****************************************************************************************'''
def FXStandardNoCoverTradeAndOperationParametersOverrideHook( trade, tradeParameters, operationParameters ):
    doFXStandardTradeAndOperationParametersOverrideHook(trade, tradeParameters, operationParameters, False)

'''****************************************************************************************
*
* FXStandardNoCover
*
****************************************************************************************'''
def FXStandardNoCover( trade, operationParameters ):
    return doFXStandard( trade, operationParameters, False )

'''****************************************************************************************
*
* FXStandardTradeAndOperationParametersOverrideHook
*
****************************************************************************************'''
def FXStandardTradeAndOperationParametersOverrideHook( trade, tradeParameters, operationParameters ):
    doFXStandardTradeAndOperationParametersOverrideHook(trade, tradeParameters, operationParameters, True)

'''****************************************************************************************
*
* FXStandard
*
****************************************************************************************'''
def FXStandard( trade, operationParameters ):
    return doFXStandard( trade, operationParameters, True )

'''****************************************************************************************
*
* TradeAllocation
*
****************************************************************************************'''
def TradeAllocation( trade, operationParameters ):
    scheme = operationParameters.AllocationScheme()
    scheme_copy = acm.Allocation().DeepCopyScheme(scheme)

    if trade.IsFxSwapFarLeg():
        # Allocation is done on the near leg
        trade = trade.ConnectedTrade()
    
    distribution = scheme_copy.AllocateTrade(trade)
    result = distribution.Apply()

    return result.Artifacts()


'''****************************************************************************************
*
* NoOperation
*
****************************************************************************************'''
def NoOperation( trade, operationParameters ):
    return [trade]


def doFXStandard( trade, operationParameters, spotCoverAllowed ):
    FRoutingFunctionsUtil.ValidateInstrumentAndTrade( trade )
    spotCoverEnabled = spotCoverAllowed and (trade.IsFxForward() or FRoutingFunctionsUtil.IsFxUnevenSwap(trade))
    constellationParameters = FRoutingFunctionsUtil.ConstellationParametersForSplitAndSpotCoverWithFXSplit(trade, operationParameters, spotCoverEnabled)
    return [constellationParameters.AllocateFXRisk()]


def doFXStandardTradeAndOperationParametersOverrideHook( trade, tradeParameters, operationParameters, spotCoverAllowed ):
    tradeParameters.Portfolio(FRoutingFunctionsUtil.GetDefaultPortfolioFromTrade(trade))
    tradeParameters.PositionPair(FRoutingFunctionsUtil.GetDefaultPositionPairFromTrade(trade))
    if not tradeParameters.Acquirer():
        tradeParameters.Acquirer( tradeParameters.Portfolio().PortfolioOwner() )
    
    tradeCopy = FRoutingFunctionsUtil.DecoupledTradeCopy(trade, tradeParameters)
    constellationParameters, defaultParamsDecorator = FRoutingFunctionsUtil.TradeConstellationParamters(tradeCopy)
    FRoutingFunctionsUtil.SetSplitOperationParameters(operationParameters, tradeParameters, defaultParamsDecorator)
    
    spotcoverEnabled = spotCoverAllowed and (trade.IsFxForward() or FRoutingFunctionsUtil.IsFxUnevenSwap(trade)) 
    defaultParamsDecorator.SpotCoverEnabled = spotcoverEnabled
    if spotcoverEnabled:
        FRoutingFunctionsUtil.SetSpotCoverOperationParameters(operationParameters, defaultParamsDecorator)
        FRoutingFunctionsUtil.SetSpotCoverSplitOperationParameters(operationParameters, defaultParamsDecorator)
    
    FRoutingFunctionsUtil.SetB2BTradeAndOperationParameters(trade, operationParameters, tradeParameters)
    FRoutingFunctionsUtil.SetSwapToSpotOperationParameters(operationParameters, defaultParamsDecorator)
