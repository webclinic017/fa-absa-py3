import acm  
import FRoutingFunctionsUtil
import FRoutingCommon
from FRoutingB2BMethods import SetPortfolios, IsSpot #cant we use TradeProcess here
from FRoutingExtensions import trade_system, Debug, DB
'''================================================================================================
================================================================================================'''
def FXB2B( trade, operationParameters ):
    FRoutingFunctionsUtil.ValidateInstrumentAndTrade( trade )
    constellationParameters, defaultParamsDecorator = FRoutingFunctionsUtil.TradeConstellationParamters(trade)
    FRoutingFunctionsUtil.SetB2BParamsFromOperationParams(trade, defaultParamsDecorator, operationParameters, False, False, False)
    defaultParameters = defaultParamsDecorator.Parameters()
    FRoutingFunctionsUtil.SetB2BParametersFromDefault(constellationParameters, defaultParameters)
    return [constellationParameters.AllocateFXRisk()]
'''================================================================================================
================================================================================================'''
def FXSpotCover( trade, operationParameters ):
    FRoutingFunctionsUtil.ValidateInstrumentAndTrade( trade )
    constellationParameters, defaultParamsDecorator = FRoutingFunctionsUtil.TradeConstellationParamters(trade)
    defaultParamsDecorator.SpotCoverEnabled(True)
    defaultParamsDecorator.SpotCoverPortfolio = operationParameters.Portfolio1()
    defaultParamsDecorator.SpotCoverPositionPair= FRoutingFunctionsUtil.GetPositionPair(operationParameters.PositionPair1(), operationParameters.Portfolio1())
    defaultParamsDecorator.SpotCoverAcquirer = operationParameters.Acquirer1()
    defaultParamsDecorator.SpotCoverCurrency = operationParameters.Currency()
    FRoutingFunctionsUtil.SetB2BParamsFromOperationParams(trade, defaultParamsDecorator, operationParameters, True, False, False)
    defaultParameters = defaultParamsDecorator.Parameters()
    FRoutingFunctionsUtil.SetSpotCoverParametersFromDefault(constellationParameters, defaultParameters)
    FRoutingFunctionsUtil.SetB2BParametersFromDefault(constellationParameters, defaultParameters)
    return [constellationParameters.AllocateFXRisk()]
'''================================================================================================
================================================================================================'''
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
'''================================================================================================
================================================================================================'''
def FXSplitAndSpotCover( trade, operationParameters ):
    FRoutingFunctionsUtil.ValidateInstrumentAndTrade( trade )
    constellationParameters, defaultParamsDecorator = FRoutingFunctionsUtil.TradeConstellationParamters(trade)
    defaultParamsDecorator.SplitPortfolio = operationParameters.Portfolio1()
    defaultParamsDecorator.SplitAcquirer = operationParameters.Acquirer1()
    defaultParamsDecorator.SpotCoverEnabled(True)
    defaultParamsDecorator.SpotCoverPortfolio = operationParameters.Portfolio2() 
    defaultParamsDecorator.SpotCoverPositionPair = FRoutingFunctionsUtil.GetPositionPair(operationParameters.PositionPair2(), operationParameters.Portfolio2())
    defaultParamsDecorator.SpotCoverAcquirer = operationParameters.Acquirer2()
    defaultParamsDecorator.SpotCoverCurrency = operationParameters.Currency()
    FRoutingFunctionsUtil.SetB2BParamsFromOperationParams(trade, defaultParamsDecorator, operationParameters, True, True, False)
    defaultParameters = defaultParamsDecorator.Parameters()
    FRoutingFunctionsUtil.SetSplitParametersFromDefault(constellationParameters, defaultParameters)
    FRoutingFunctionsUtil.SetSpotCoverParametersFromDefault(constellationParameters, defaultParameters)
    FRoutingFunctionsUtil.SetB2BParametersFromDefault(constellationParameters, defaultParameters)
    return [constellationParameters.AllocateFXRisk()]
'''================================================================================================
================================================================================================'''
def FXSplitAndSpotCoverWithFXSplit ( trade, operationParameters ):
    FRoutingFunctionsUtil.ValidateInstrumentAndTrade( trade )
    constellationParameters = FRoutingFunctionsUtil.ConstellationParametersForSplitAndSpotCoverWithFXSplit(trade, operationParameters, True)
    return [constellationParameters.AllocateFXRisk()]    
'''================================================================================================
================================================================================================'''
def FXSpotCoverWithFXSplit( trade, operationParameters ):
    FRoutingFunctionsUtil.ValidateInstrumentAndTrade( trade )
    constellationParameters, defaultParamsDecorator = FRoutingFunctionsUtil.TradeConstellationParamters(trade)
    defaultParamsDecorator.SpotCoverEnabled(True)
    defaultParamsDecorator.SpotCoverPortfolio = operationParameters.Portfolio1()
    defaultParamsDecorator.SpotCoverPositionPair = FRoutingFunctionsUtil.GetPositionPair(operationParameters.PositionPair1(), operationParameters.Portfolio1())
    defaultParamsDecorator.SpotCoverAcquirer = operationParameters.Acquirer1()
    defaultParamsDecorator.SpotCoverSplitPortfolio = operationParameters.Portfolio2()
    defaultParamsDecorator.SpotCoverSplitAcquirer = operationParameters.Acquirer2()
    defaultParamsDecorator.SpotCoverCurrency = operationParameters.Currency()    
    defaultParamsDecorator.UpdateSwapToSpotEnabled()
    if defaultParamsDecorator.SwapToSpotEnabled():
        FRoutingFunctionsUtil.SetSwapToSpotFromOperationParameters(defaultParamsDecorator, operationParameters)
    defaultParameters = defaultParamsDecorator.Parameters()
    FRoutingFunctionsUtil.SetSpotCoverParametersFromDefault(constellationParameters, defaultParameters)
    FRoutingFunctionsUtil.SetSpotCoverWithSplitParametersFromDefault(constellationParameters, defaultParameters)
    FRoutingFunctionsUtil.SetSwapToSpotParamsFromDefault(constellationParameters, defaultParameters)
    return [constellationParameters.AllocateFXRisk()]    
'''================================================================================================
================================================================================================'''
def FXStandardNoCover( trade, operationParameters ): return doFXStandard( trade, operationParameters, False )
def FXStandard( trade, operationParameters ): return doFXStandard( trade, operationParameters, True )
def NoOperation( trade, operationParameters ): return doNoOperation( trade, operationParameters )
def doNoOperation( trade, operationParameters ): return [trade]   
'''================================================================================================
================================================================================================'''
def TradeAllocation( trade, operationParameters ):
    scheme = operationParameters.AllocationScheme()
    scheme_copy = acm.Allocation().DeepCopyScheme(scheme)
    if trade.IsFxSwapFarLeg(): # Allocation is done on the near leg
        trade = trade.ConnectedTrade()
    distribution = scheme_copy.AllocateTrade(trade)
    result = distribution.Apply()
    return result.Artifacts()
'''================================================================================================
================================================================================================'''
@Debug()
def doFXStandard( trade, operationParameters, spotCoverAllowed ):

    Temp = None 
    if trade.CorrectionTrade():
        Temp = trade.CorrectionTrade()
        trade.CorrectionTrade(None)

    FRoutingFunctionsUtil.ValidateInstrumentAndTrade( trade )
    #spotCoverEnabled = spotCoverAllowed and (trade.IsFxForward() or (FRoutingFunctionsUtil.IsFxUnevenSwap(trade)))
    spotCoverEnabled = spotCoverAllowed
    if spotCoverEnabled == True:
        spotCoverEnabled = False
        if trade.IsFxForward():
            spotCoverEnabled = True
            
            
        
        #MKlimke - Business requested that there be no spot cover on UnEvenSwaps 2015/06/12
        if FRoutingFunctionsUtil.IsFxUnevenSwap(trade):
            near_leg = acm.FTrade[trade.ConnectedTrdnbr()]       
            splitPortfolio = trade.Portfolio()
            if operationParameters.Portfolio1():
                splitPortfolio = operationParameters.Portfolio1()
            splitPositionPair = trade.PositionPair()
            if operationParameters.PositionPair1():
                splitPositionPair = operationParameters.PositionPair1()
            isSplit = FRoutingFunctionsUtil.CandidateForSplit(trade, splitPortfolio, splitPositionPair)
            isB2BSales = FRoutingFunctionsUtil.CandidateForB2B(trade)
            if (not IsSpot(near_leg) and IsSpot(trade)) or (IsSpot(near_leg) and not IsSpot(trade)):
                spotCoverEnabled = True
                           
            '''if isB2BSales == None:
                if (not IsSpot(near_leg) and not IsSpot(trade)):
                    if isSplit == False:
                        spotCoverEnabled = True'''
            
    constellationParameters = FRoutingFunctionsUtil.ConstellationParametersForSplitAndSpotCoverWithFXSplit(trade, operationParameters, spotCoverEnabled)
    trade.CorrectionTrade(Temp)
    return [constellationParameters.AllocateFXRisk()]
'''================================================================================================
================================================================================================'''
def FXStandardTradeAndOperationParametersOverrideHook( trade, tradeParameters, operationParameters ):
    doFXStandardTradeAndOperationParametersOverrideHook(trade, tradeParameters, operationParameters, True)
def FXStandardNoCoverTradeAndOperationParametersOverrideHook( trade, tradeParameters, operationParameters ):
    doFXStandardTradeAndOperationParametersOverrideHook(trade, tradeParameters, operationParameters, False)

def doFXStandardTradeAndOperationParametersOverrideHook( trade, tradeParameters, operationParameters, spotCoverAllowed ):

    Temp = None 
    if trade.CorrectionTrade():
        Temp = trade.CorrectionTrade()
        trade.CorrectionTrade(None)

    if tradeParameters.Portfolio() == None:
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
    trade.CorrectionTrade(Temp)
 
'''================================================================================================
================================================================================================'''
def FXStandardB2BTradeAndOperationParametersOverrideHook( trade, tradeParameters, operationParameters ):
    doFXStandardB2BTradeAndOperationParametersOverrideHook(trade, tradeParameters, operationParameters, True)

@Debug()
def doFXStandardB2BTradeAndOperationParametersOverrideHook( trade, tradeParameters, operationParameters, spotCoverAllowed ):

    Temp = None 
    if trade.CorrectionTrade():
        Temp = trade.CorrectionTrade()
        trade.CorrectionTrade(None)

    if tradeParameters.Portfolio() == None:
        tradeParameters.Portfolio(FRoutingFunctionsUtil.GetDefaultPortfolioFromTrade(trade))  
    tradeParameters.PositionPair(FRoutingFunctionsUtil.GetDefaultPositionPairFromTrade(trade))
    if not tradeParameters.Acquirer():
        tradeParameters.Acquirer( tradeParameters.Portfolio().PortfolioOwner() )
    
    tradeCopy = FRoutingFunctionsUtil.DecoupledTradeCopy(trade, tradeParameters) # create a tempory trade
    constellationParameters, defaultParamsDecorator = FRoutingFunctionsUtil.TradeConstellationParamters(tradeCopy) 
    FRoutingFunctionsUtil.SetSplitOperationParameters(operationParameters, tradeParameters, defaultParamsDecorator)
    
    spotcoverEnabled = spotCoverAllowed and (trade.IsFxForward() or FRoutingFunctionsUtil.IsFxUnevenSwap(trade)) 
    defaultParamsDecorator.SpotCoverEnabled = spotcoverEnabled
    
    #(mklimke) setting the oprtaion params
    if spotcoverEnabled:
        FRoutingFunctionsUtil.SetSpotCoverOperationParameters(operationParameters, defaultParamsDecorator)
        FRoutingFunctionsUtil.SetSpotCoverSplitOperationParameters(operationParameters, defaultParamsDecorator)

    FRoutingFunctionsUtil.SetB2BTradeAndOperationParameters(trade, operationParameters, tradeParameters) #???
    FRoutingFunctionsUtil.SetSwapToSpotOperationParameters(operationParameters, defaultParamsDecorator)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    splitPortfolio = trade.Portfolio()
    if operationParameters.Portfolio1():
        splitPortfolio = operationParameters.Portfolio1()
    splitPositionPair = trade.PositionPair()
    if operationParameters.PositionPair1():
        splitPositionPair = operationParameters.PositionPair1()

    splitEnabled = FRoutingFunctionsUtil.CandidateForSplit(trade, splitPortfolio, splitPositionPair)
    tradeCurrencyPair = trade.CurrencyPair()                                  
    salesCurrencyPair = tradeCurrencyPair.SpotSplitPair()
    
    if salesCurrencyPair != None:
        splitCurrencyPair = salesCurrencyPair.GetTriangulatingCurrencyPair(tradeCurrencyPair)
    else:
        splitCurrencyPair = tradeCurrencyPair
        salesCurrencyPair = tradeCurrencyPair
    
    if trade_system(trade) == 'PHO':
        SetPortfolios(trade, FRoutingCommon.TradeAIproxyInstance, operationParameters, splitEnabled, salesCurrencyPair, splitCurrencyPair)
    elif trade.OptKey2():
        if trade.OptKey2().Name() == 'PHO':
            SetPortfolios(trade, FRoutingCommon.TradeAIproxyInstance, operationParameters, splitEnabled, salesCurrencyPair, splitCurrencyPair)

    trade.CorrectionTrade(Temp)
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    
'''================================================================================================
================================================================================================'''












