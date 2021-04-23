import acm 
import FRoutingCommon 
from FRoutingExtensions import IsSalesMargin, is_inverse, Debug, DB, SuppressPips
from FRoutingB2BMethods import GetDealtCurrency, IsSpot, PLCurrency
'''================================================================================================
================================================================================================'''
guiShell = acm.FBusinessLogicGUIDefault()
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def WrapInParameterClass(trade): return acm.FFxTradeConstellationParameters(trade) 
@Debug('', DB.DEBUG)
def GetDefaultPortfolioFromTrade(trade): return GetDefaultPortfolioFromCurrencyPair(trade.CurrencyPair(), trade)
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def GetDefaultPositionPairFromTrade(trade):
    portfolio = GetDefaultPortfolioFromCurrencyPair(trade.CurrencyPair(), trade)
    if portfolio: positionPair = portfolio.CurrencyPair()
    if not positionPair: positionPair = GetDefaultPositionPairFromCurrencyPair(trade.CurrencyPair(), trade)
    if not positionPair: positionPair = trade.PositionOrCurrencyPair()
    return positionPair
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def GetDefaultPortfolioFromCurrencyPair(currencyPair, trade):
    portfolio = None
    if trade.IsFxSpot():
        portfolio = currencyPair.SpotPortfolio()
    elif trade.IsFxForward() or trade.IsFxSwapFarLeg():
        portfolio = currencyPair.ForwardPortfolio()
    return portfolio
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def GetDefaultPositionPairFromCurrencyPair(currencyPair, trade):
    positionPair = None
    if trade.IsFxSpot():
        positionPair = currencyPair.SpotSplitPair()
    elif trade.IsFxForward() or trade.IsFxSwapFarLeg():
        positionPair = currencyPair.ForwardSplitPair()
    return positionPair
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def GetPositionPair(positionPair, portfolio):
    if not positionPair: positionPair = portfolio.CurrencyPair()
    return positionPair
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def IsFxUnevenSwap(trade): return True if trade.IsFxSwapFarLeg() and trade.IsFxUnevenSwap() else False
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def CandidateForSplit(trade, splitPortfolio, splitPositionPair = None):
    isCandidate = False
    if not splitPositionPair:
        if splitPortfolio:
            splitPositionPair = splitPortfolio.CurrencyPair()
    if splitPositionPair and trade: 
        isCandidate = splitPositionPair != trade.CurrencyPair()
    return isCandidate
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def CandidateForB2B(trade):
    #result = trade.SalesDeskPortfolio() != None and trade.SalesDeskAcquirer() != None
    result = trade.SalesDeskPortfolio() and trade.SalesDeskAcquirer() 
    return result
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def ValidateInstrumentAndTrade(trade ):        
    assert trade.Instrument().IsKindOf(acm.FCurrency), "Instrument name %s not of type FCurrency" % trade.Instrument().Name()
    assert not trade.IsFxSwapNearLeg()
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def TradeConstellationParamters(trade):
    tradeIntoParam = trade
    if tradeIntoParam.IsFxSwap():
        tradeIntoParam = tradeIntoParam.ConnectedTrade()
    constellationParameters = WrapInParameterClass(tradeIntoParam)
    defaultParamsDecorator = acm.FFxTradeConstellationParametersLogicDecorator( acm.FFxTradeConstellationParameters(tradeIntoParam), guiShell )
    return constellationParameters, defaultParamsDecorator
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def DecoupledTradeCopy(trade, tradeParameters):
    defaultValueTrade = acm.FTrade()
    if trade.IsFxSwap():
        farT = acm.FTrade()
        farT.Apply(trade)
        defaultValueTrade.Apply(trade.ConnectedTrade())
        defaultValueTrade.RegisterInStorage()
        farT.RegisterInStorage()
        defaultValueTrade.ConnectedTrade(defaultValueTrade)
        farT.ConnectedTrade(defaultValueTrade)
    else:
        defaultValueTrade.Apply(trade)
    defaultValueTrade.Portfolio(tradeParameters.Portfolio())
    defaultValueTrade.Acquirer(tradeParameters.Acquirer())
    defaultValueTrade.PositionPair(tradeParameters.PositionPair())
    return defaultValueTrade
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def SetSpotCoverParametersFromDefault(constellationParameters, defaultParameters):
    constellationParameters.SpotCoverEnabled = defaultParameters.SpotCoverEnabled()
    constellationParameters.SpotCoverPortfolio = defaultParameters.SpotCoverPortfolio()
    constellationParameters.SpotCoverPositionPair = defaultParameters.SpotCoverPositionPair()
    constellationParameters.SpotCoverAcquirer = defaultParameters.SpotCoverAcquirer()
    constellationParameters.SpotCoverCurrency = defaultParameters.SpotCoverCurrency()
    #constellationParameters.SpotCoverDate = defaultParameters.SpotCoverDate() #(mklimke)-spot cover date must be the spotdate of trade currencypair not the cover currencypair
    constellationParameters.SpotCoverDate = defaultParameters.Trade().CurrencyPair().SpotDate(acm.Time.DateToday())
    constellationParameters.SpotCoverDealerSpotPrice = defaultParameters.SpotCoverDealerSpotPrice()
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def SetSpotCoverWithSplitParametersFromDefault(constellationParameters, defaultParameters):
    spotCoverSplitSalesMargin = 0 
    constellationParameters.SpotCoverSplitPortfolio = defaultParameters.SpotCoverSplitPortfolio()
    constellationParameters.SpotCoverSplitAcquirer = defaultParameters.SpotCoverSplitAcquirer()
    constellationParameters.SpotCoverSplitDealerSpotPrice = defaultParameters.SpotCoverSplitDealerSpotPrice()
    constellationParameters.SpotCoverSplitSpotMargin = spotCoverSplitSalesMargin 
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def SetSplitParametersFromDefault(constellationParameters, defaultParameters):
    sales_margin, points_sales_margin, far_sales_margin, split_far_points_sales_margin = 0, 0, 0, 0
    constellationParameters.SplitPortfolio = defaultParameters.SplitPortfolio()
    constellationParameters.SplitAcquirer = defaultParameters.SplitAcquirer()
    constellationParameters.SplitCustomerSpotPrice = defaultParameters.SplitCustomerSpotPrice()
    constellationParameters.SplitCustomerPrice = defaultParameters.SplitCustomerPrice()
    constellationParameters.SplitPriceMargin = sales_margin
    constellationParameters.SplitPointsMargin = points_sales_margin
    constellationParameters.SplitFarCustomerPrice = defaultParameters.SplitFarCustomerPrice()
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def SetSwapToSpotParamsFromDefault(constellationParameters, defaultParameters):
    constellationParameters.SwapMainPortfolio = defaultParameters.SwapMainPortfolio()
    constellationParameters.SwapMainAcquirer = defaultParameters.SwapMainAcquirer()
    constellationParameters.SwapMainPoints = defaultParameters.SwapMainPoints()
    constellationParameters.SwapMainSpotDate = defaultParameters.SwapMainSpotDate()
    constellationParameters.SwapSplitPortfolio = defaultParameters.SwapSplitPortfolio()
    constellationParameters.SwapSplitAcquirer = defaultParameters.SwapSplitAcquirer()
    constellationParameters.SwapSplitPoints = defaultParameters.SwapSplitPoints()
    constellationParameters.SwapSplitSpotDate = defaultParameters.SwapSplitSpotDate()
'''================================================================================================
================================================================================================'''
def SetSplitOperationParameters(operationParams, tradeParameters, defaultParamsDecorator):
    if not operationParams.Acquirer1():
        operationParams.Acquirer1 = defaultParamsDecorator.SplitAcquirer()
    if not operationParams.Portfolio1():        #mklimke - dont overwrite the parameter if it has already been set
        operationParams.Portfolio1(defaultParamsDecorator.SplitPortfolio())
    operationParams.PositionPair1 = tradeParameters.PositionPair()
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def SetSpotCoverOperationParameters(operationParams, defaultParamsDecorator):
    operationParams.Currency = defaultParamsDecorator.SpotCoverCurrency()
    if not operationParams.Portfolio2(): operationParams.Portfolio2(defaultParamsDecorator.SpotCoverPortfolio()) #[mklimke - dont overwrite the parameter if it has already been set]
    operationParams.PositionPair2 = defaultParamsDecorator.SpotCoverPositionPair()
    if not operationParams.Acquirer2(): operationParams.Acquirer2(defaultParamsDecorator.SpotCoverAcquirer())
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def SetSpotCoverSplitOperationParameters(operationParams, defaultParamsDecorator):
    if not operationParams.Portfolio3(): operationParams.Portfolio3 = defaultParamsDecorator.SpotCoverSplitPortfolio() #[mklimke - dont overwrite the parameter if it has already been set]
    if not operationParams.Acquirer3(): operationParams.Acquirer3 = defaultParamsDecorator.SpotCoverSplitAcquirer()
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def SetSwapToSpotFromOperationParameters(defaultParamsDecorator, operationParams):
    defaultParamsDecorator.SwapMainPortfolio = operationParams.Portfolio5()
    defaultParamsDecorator.SwapMainAcquirer = operationParams.Acquirer5()
    defaultParamsDecorator.SwapSplitPortfolio = operationParams.Portfolio6()
    defaultParamsDecorator.SwapSplitAcquirer = operationParams.Acquirer6()
'''================================================================================================
Parameters:
    FFxTradeConstellationParameters constellationParameters
    FFxTradeConstellationParameters defaultParameters
================================================================================================'''
@Debug('', DB.DEBUG)
def SetB2BParametersFromDefault(constellationParameters, defaultParameters):
    constellationParameters.TradersPortfolio = defaultParameters.TradersPortfolio()
    constellationParameters.TradersPositionPair = defaultParameters.TradersPositionPair()
    constellationParameters.TradersAcquirer = defaultParameters.TradersAcquirer()
    fxSalesPortfolioName = "FX_SALES"
    portfolio = acm.FCompoundPortfolio[fxSalesPortfolioName]
    if constellationParameters.Trade().SalesDeskPortfolio() in portfolio.AllPhysicalPortfolios():
        constellationParameters.SalesCoverEnabled = True
    else:
        constellationParameters.SalesCoverEnabled = False
    #print "SalesCoverEnabled", constellationParameters.SalesCoverEnabled()
    #constellationParameters.SalesCoverEnabled = CandidateForB2B(constellationParameters.Trade())
    #constellationParameters.SalesCoverEnabled = defaultParameters.SalesCoverEnabled
    constellationParameters.SalesCoverReferencePrice = defaultParameters.SalesCoverReferencePrice()
    constellationParameters.SalesCoverPrice = defaultParameters.SalesCoverPrice()
    constellationParameters.SalesCoverFarPrice = defaultParameters.SalesCoverFarPrice()
    constellationParameters.SplitCustomerSpotPrice = defaultParameters.SplitCustomerSpotPrice()
    constellationParameters.SplitCustomerPrice = defaultParameters.SplitCustomerPrice()
    constellationParameters.SplitFarCustomerPrice = defaultParameters.SplitFarCustomerPrice()
    constellationParameters.SpotCoverDealerSpotPrice = defaultParameters.SpotCoverDealerSpotPrice()
    constellationParameters.SpotCoverSpotMargin = defaultParameters.SpotCoverSpotMargin()
    constellationParameters.SpotCoverSplitDealerSpotPrice = defaultParameters.SpotCoverSplitDealerSpotPrice()
    constellationParameters.SpotCoverSplitSpotMargin = defaultParameters.SpotCoverSplitSpotMargin()
    constellationParameters.PLCurrency(PLCurrency(defaultParameters.Trade()))

'''================================================================================================
================================================================================================'''
def PrintRates(constellationParam):

    print constellationParam.SalesCoverReferencePrice(), ' constellationParam.SalesCoverReferencePrice'
    print constellationParam.SalesCoverPrice(), ' constellationParam.SalesCoverPrice'
    print constellationParam.SalesCoverFarPrice(), ' constellationParam.SalesCoverFarPrice'  
    print constellationParam.SplitCustomerSpotPrice(), ' constellationParam.SplitCustomerSpotPrice'
    print constellationParam.SplitCustomerPrice(), ' constellationParam.SplitCustomerPrice'
    print constellationParam.SplitFarCustomerPrice(), ' constellationParam.SplitFarCustomerPrice' 
    print constellationParam.SpotCoverDealerSpotPrice(), 'constellationParam.SpotCoverDealerSpotPrice'
    print constellationParam.SpotCoverSplitDealerSpotPrice(), 'constellationParam.SpotCoverSplitDealerSpotPrice'
    print constellationParam.SpotCoverSpotMargin(), 'constellationParam.SpotCoverSpotMargin'

'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def SetB2BParamsFromOperationParams(trade, defaultParamsDecorator, operationParams, isSpotcover, isSplit, isSpotCoverSplit ):
    
    if operationParams.Portfolio4() and operationParams.Acquirer4():  
        spotCoverPrfCurrPair = defaultParamsDecorator.SpotCoverPositionPair()
        defaultParamsDecorator.TradersPortfolio( operationParams.Portfolio4() )
        defaultParamsDecorator.TradersAcquirer( operationParams.Acquirer4() )
        defaultParamsDecorator.TradersPositionPair( operationParams.PositionPair4() )
        defaultParamsDecorator.SalesCoverEnabled( True)
        if trade.IsFxSwap(): defaultParamsDecorator.FxSwapFarLegValueDate( trade.ValueDay() )
        constellationParam = defaultParamsDecorator.Parameters() 
        
        #----------------------------------------------------------------------------------------------------------------------------------
        assert FRoutingCommon.TradeAIproxyInstance != None, 'TradeAIProxy cannot be None'
        assert FRoutingCommon.TradeAIproxyInstance.Trade() == trade, 'TradeAiProxy trade must be equal to routed trade'

        swapfartrade = trade
        if trade.IsFxSwap(): trade = trade.ConnectedTrade() 
        calculateMargin = IsSalesMargin(trade)
        inverse = is_inverse(trade)
        
        tradeCurrencyPair = trade.CurrencyPair()      
        salesCurrencyPair = tradeCurrencyPair.SpotSplitPair()  #is that not equal to spotCoverPrfCurrPair
        if salesCurrencyPair != None:
            splitCurrencyPair = salesCurrencyPair.GetTriangulatingCurrencyPair(tradeCurrencyPair)
        else:
            splitCurrencyPair = salesCurrencyPair = tradeCurrencyPair
            
        SalesSpotPrice = trade.SalesSpotPrice(FRoutingCommon.TradeAIproxyInstance, salesCurrencyPair, isSplit, calculateMargin)
		
        #----------------------------------------------------------------------------------------------------------------------------------
        if not SalesSpotPrice: #mklimke : there is no SalesCover
            constellationParam.SalesCoverReferencePrice = defaultParamsDecorator.SalesCoverReferencePrice()                        
            constellationParam.SalesCoverPrice = defaultParamsDecorator.SalesCoverPrice()
            constellationParam.SalesCoverFarPrice = defaultParamsDecorator.SalesCoverFarPrice()
            constellationParam.SplitCustomerSpotPrice = defaultParamsDecorator.SplitCustomerSpotPrice()            
            constellationParam.SplitCustomerPrice = defaultParamsDecorator.SplitCustomerPrice()
            constellationParam.SplitFarCustomerPrice = defaultParamsDecorator.FarSplitCustomerPrice()            
            if constellationParam.SpotCoverPortfolio():
                if defaultParamsDecorator.SpotCoverSplitPortfolio() and constellationParam.SpotCoverPortfolio().CurrencyPair():
                    constellationParam.SpotCoverSplitDealerSpotPrice = defaultParamsDecorator.SplitCustomerSpotPrice()            
                    currPair = constellationParam.SpotCoverPortfolio().CurrencyPair()
                    constellationParam.SpotCoverDealerSpotPrice = GetTriangulatingSpotPrice(trade, currPair, constellationParam.SpotCoverSplitDealerSpotPrice())
                else:
                    constellationParam.SpotCoverDealerSpotPrice = trade.ReferencePrice()
            else:
                constellationParam.SpotCoverDealerSpotPrice = 0
                constellationParam.SpotCoverSplitDealerSpotPrice = 0
            constellationParam.SpotCoverSpotMargin = 0
        else:

            SalesNearPrice = trade.SalesNearPrice(FRoutingCommon.TradeAIproxyInstance, salesCurrencyPair, isSplit, calculateMargin)
            SalesFarPrice = trade.SalesFarPrice(FRoutingCommon.TradeAIproxyInstance, salesCurrencyPair, isSplit, calculateMargin) 
            TradeSpotPrice = trade.TradeSpotPrice(FRoutingCommon.TradeAIproxyInstance, inverse)
            TradePrice = trade.TradePrice(FRoutingCommon.TradeAIproxyInstance, inverse)
            TradeFarPrice = swapfartrade.TradeFarPrice(FRoutingCommon.TradeAIproxyInstance, inverse)
            SplitSpotPrice = trade.SplitSpotPrice(FRoutingCommon.TradeAIproxyInstance, splitCurrencyPair, isSplit)
            SplitNearPrice = trade.SplitNearPrice(FRoutingCommon.TradeAIproxyInstance, splitCurrencyPair, isSplit)
            SplitFarPrice = swapfartrade.SplitFarPrice(FRoutingCommon.TradeAIproxyInstance, splitCurrencyPair, isSplit)
            dealtCurrency = GetDealtCurrency(trade)
           
            if not calculateMargin and isSplit:
                if trade.SSA():
                    if salesCurrencyPair.AdditionalInfo().SSA(): 
                        SalesSpotPrice = salesCurrencyPair.TriangulateRate(tradeCurrencyPair, TradeSpotPrice, splitCurrencyPair, SplitSpotPrice)
                        SalesNearPrice = salesCurrencyPair.TriangulateRate(tradeCurrencyPair, TradePrice, splitCurrencyPair, SplitNearPrice)
                        if trade.IsFxSwap(): SalesFarPrice =  salesCurrencyPair.TriangulateRate(tradeCurrencyPair, TradeFarPrice, splitCurrencyPair, SplitFarPrice)
                    else:
                        SplitSpotPrice = splitCurrencyPair.TriangulateRate(tradeCurrencyPair, TradeSpotPrice, salesCurrencyPair, SalesSpotPrice)
                        SplitNearPrice = splitCurrencyPair.TriangulateRate(tradeCurrencyPair, TradePrice, salesCurrencyPair, SalesNearPrice)
                        if trade.IsFxSwap(): SplitFarPrice =  splitCurrencyPair.TriangulateRate(tradeCurrencyPair, TradeFarPrice, salesCurrencyPair, SalesFarPrice)
                elif tradeCurrencyPair.IncludesCurrency(acm.FCurrency['ZAR']):
                    if splitCurrencyPair == acm.FCurrencyPair['USD/ZAR']:  
                        SplitSpotPrice = splitCurrencyPair.TriangulateRate(tradeCurrencyPair, TradeSpotPrice, salesCurrencyPair, SalesSpotPrice)
                        SplitNearPrice = splitCurrencyPair.TriangulateRate(tradeCurrencyPair, TradePrice, salesCurrencyPair, SalesNearPrice)
                        if trade.IsFxSwap(): SplitFarPrice = splitCurrencyPair.TriangulateRate(tradeCurrencyPair, TradeFarPrice, salesCurrencyPair, SalesFarPrice)
                    else:
                        SalesSpotPrice = salesCurrencyPair.TriangulateRate(tradeCurrencyPair, TradeSpotPrice, splitCurrencyPair, SplitSpotPrice)
                        SalesNearPrice = salesCurrencyPair.TriangulateRate(tradeCurrencyPair, TradePrice, splitCurrencyPair, SplitNearPrice)
                        if trade.IsFxSwap(): SalesFarPrice =  salesCurrencyPair.TriangulateRate(tradeCurrencyPair, TradeFarPrice, splitCurrencyPair, SplitFarPrice)
                else:
                    if salesCurrencyPair.IncludesCurrency(dealtCurrency): 
                        SplitSpotPrice = splitCurrencyPair.TriangulateRate(tradeCurrencyPair, TradeSpotPrice, salesCurrencyPair, SalesSpotPrice)
                        SplitNearPrice = splitCurrencyPair.TriangulateRate(tradeCurrencyPair, TradePrice, salesCurrencyPair, SalesNearPrice)
                        if trade.IsFxSwap(): SplitFarPrice =  splitCurrencyPair.TriangulateRate(tradeCurrencyPair, TradeFarPrice, salesCurrencyPair, SalesFarPrice)
                    else:
                        SalesSpotPrice = salesCurrencyPair.TriangulateRate(tradeCurrencyPair, TradeSpotPrice, splitCurrencyPair, SplitSpotPrice)
                        SalesNearPrice = salesCurrencyPair.TriangulateRate(tradeCurrencyPair, TradePrice, splitCurrencyPair, SplitNearPrice)
                        if trade.IsFxSwap(): SalesFarPrice =  salesCurrencyPair.TriangulateRate(tradeCurrencyPair, TradeFarPrice, splitCurrencyPair, SplitFarPrice)
            
            if SuppressPips(trade):
                SalesSpotPrice = SalesNearPrice
                SplitSpotPrice = SplitNearPrice
            
            #Spot
            constellationParam.SalesCoverReferencePrice(SalesSpotPrice)
            constellationParam.SalesCoverPrice(SalesNearPrice)
            constellationParam.SalesCoverFarPrice(SalesFarPrice)
            #Split
            constellationParam.SplitCustomerSpotPrice(SplitSpotPrice)
            constellationParam.SplitCustomerPrice(SplitNearPrice)
            constellationParam.SplitFarCustomerPrice(SplitFarPrice)
            
            #Fwd
            constellationParam.SpotCoverDealerSpotPrice = GetSpotCoverDealerSpotPrice(trade, spotCoverPrfCurrPair, defaultParamsDecorator.TradersPositionPair(), isSplit, isSpotcover, isSpotCoverSplit, SalesSpotPrice)
            constellationParam.SpotCoverSplitDealerSpotPrice = GetSpotCoverSplitDealerSpotPrice(trade, isSpotcover, isSpotCoverSplit, SplitSpotPrice)
            #constellationParam.SpotCoverSpotMargin = GetSpotCoverSpotMargin(trade, spotCoverPrfCurrPair, constellationParam.SplitCustomerSpotPrice(), constellationParam.SpotCoverDealerSpotPrice(), trade.SplitSpotPrice(), isSplit, isSpotcover, isSpotCoverSplit)
            constellationParam.SpotCoverSpotMargin = GetSpotCoverSpotMargin(trade, spotCoverPrfCurrPair, constellationParam.SplitCustomerSpotPrice(), constellationParam.SpotCoverDealerSpotPrice(), SplitSpotPrice, isSplit, isSpotcover, isSpotCoverSplit)

        constellationParam.SpotCoverSplitSpotMargin(0)
        #PrintRates(constellationParam)
 
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def SetB2BTradeAndOperationParameters(trade, operationParameters, tradeParameters): 
    if CandidateForB2B(trade):
        operationParameters.Portfolio4(tradeParameters.Portfolio())   
        operationParameters.Acquirer4(tradeParameters.Acquirer())    
        operationParameters.PositionPair4(tradeParameters.PositionPair())
        tradeParameters.Portfolio(trade.SalesDeskPortfolio())
        tradeParameters.Acquirer(trade.SalesDeskAcquirer())
        tradeParameters.PositionPair(None)
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def SetUnevnSwapSpotCoverRates(trade, defaultParamsDecorator, operationParams, spotCoverEnabled, splitEnabled, spotCoverSplit):
    if IsFxUnevenSwap(trade):
        if not CandidateForB2B(trade) and spotCoverEnabled == True:
            if splitEnabled == False:  
                defaultParamsDecorator.SpotCoverDealerSpotPrice = trade.ReferencePrice()
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def ConstellationParametersForSplitAndSpotCoverWithFXSplit(trade, operationParams, spotCoverEnabled = False):
    constellationParameters, defaultParamsDecorator = TradeConstellationParamters(trade)

    splitPortfolio = trade.Portfolio()
    if operationParams.Portfolio1():
        splitPortfolio = operationParams.Portfolio1()
    splitPositionPair = trade.PositionPair()
    if operationParams.PositionPair1():
        splitPositionPair = operationParams.PositionPair1()

    splitEnabled = CandidateForSplit(trade, splitPortfolio, splitPositionPair)
    spotCoverSplit = CandidateForSplit(trade, operationParams.Portfolio2(), operationParams.PositionPair2())
     
    if operationParams.Portfolio2() and operationParams.Acquirer2():  #
        defaultParamsDecorator.SpotCoverEnabled(spotCoverEnabled)
        defaultParamsDecorator.SpotCoverCurrency = operationParams.Currency()
        defaultParamsDecorator.SpotCoverPortfolio = operationParams.Portfolio2()
        defaultParamsDecorator.SpotCoverPositionPair = GetPositionPair(operationParams.PositionPair2(), operationParams.Portfolio2())
        defaultParamsDecorator.SpotCoverAcquirer = operationParams.Acquirer2()
        defaultParamsDecorator.SpotCoverSplitPortfolio = operationParams.Portfolio3()
        defaultParamsDecorator.SpotCoverSplitAcquirer = operationParams.Acquirer3()    

    SetB2BParamsFromOperationParams(trade, defaultParamsDecorator, operationParams, spotCoverEnabled, splitEnabled, spotCoverSplit)  
    SetUnevnSwapSpotCoverRates(trade, defaultParamsDecorator, operationParams, spotCoverEnabled, splitEnabled, spotCoverSplit)
    if splitEnabled:
        defaultParamsDecorator.SplitPortfolio = operationParams.Portfolio1()
        defaultParamsDecorator.SplitAcquirer = operationParams.Acquirer1()
    
    defaultParamsDecorator.UpdateSwapToSpotEnabled()
    if defaultParamsDecorator.SwapToSpotEnabled():
        SetSwapToSpotFromOperationParameters(defaultParamsDecorator, operationParams)
   
    defaultParameters = defaultParamsDecorator.Parameters()  
    SetSplitParametersFromDefault(constellationParameters, defaultParameters)
    SetSpotCoverParametersFromDefault(constellationParameters, defaultParameters)
    SetSpotCoverWithSplitParametersFromDefault(constellationParameters, defaultParameters)
    SetSwapToSpotParamsFromDefault(constellationParameters, defaultParameters)
    
    #(mklimke)- note:finally routing paramters from the decorator 
    SetB2BParametersFromDefault(constellationParameters, defaultParameters)  
    #(mklimke)- change:had to clear the SpotCoverSplitPortfolio else it was trying to split
    if not splitEnabled:
        constellationParameters.SpotCoverSplitPortfolio(None) 
    else:
        if constellationParameters.SpotCoverSplitPortfolio() == None:
            constellationParameters.SpotCoverSplitPortfolio(constellationParameters.SplitPortfolio()) 
    return constellationParameters
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def SetSwapToSpotOperationParameters(operationParams, defaultParamsDecorator):
    if not operationParams.Acquirer5():
        operationParams.Acquirer5 = defaultParamsDecorator.SwapMainAcquirer()
    operationParams.Portfolio5 = defaultParamsDecorator.SwapMainPortfolio()
    if not operationParams.Acquirer6():
        operationParams.Acquirer6 = defaultParamsDecorator.SwapSplitAcquirer()
    operationParams.Portfolio6 = defaultParamsDecorator.SwapSplitPortfolio()
'''================================================================================================
def GetSpotCoverDealerSpotPrice(trade, spotCoverPrfCurrPair, tradersPrfCurrPair, isSplit, isSpotcover, isSpotCoverSplit):
================================================================================================'''
@Debug('', DB.DEBUG)
def GetSpotCoverDealerSpotPrice(trade, spotCoverPrfCurrPair, tradersPrfCurrPair, isSplit, isSpotcover, isSpotCoverSplit, SalesSpotPrice):
    if isSpotcover:
        if isSplit:   
            if isSpotCoverSplit:
                return SalesSpotPrice
            else:
                currPair = trade.CurrencyPair().GetTriangulatingCurrencyPair(tradersPrfCurrPair)
                fxRate = trade.CurrencyPair().TriangulateRate(currPair, trade.SplitSpotPrice(), tradersPrfCurrPair, SalesSpotPrice)
                fxRate = 1/fxRate if trade.CurrencyPair().Currency1() == trade.Currency() and fxRate else fxRate
                return fxRate
        else:
            if isSpotCoverSplit:
                currPair = spotCoverPrfCurrPair.GetTriangulatingCurrencyPair(trade.CurrencyPair())     
                salesSpotPrice = 1/SalesSpotPrice if trade.CurrencyPair().Currency1() == trade.Currency() and SalesSpotPrice else SalesSpotPrice
                fxRate = spotCoverPrfCurrPair.TriangulateRate(currPair, trade.SplitSpotPrice(), trade.CurrencyPair(), salesSpotPrice) 
                return fxRate
            else:
                return SalesSpotPrice
    return 0
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def GetSpotCoverSpotMargin(trade, spotCoverPrfCurrPair, splitCustomerSpotPrice, spotCoverDealerSpotPrice, splitSpotPrice, isSplit, isSpotcover, isSpotCoverSplit):
    if isSpotcover:
        if isSplit:
            if isSpotCoverSplit:
                currPair = spotCoverPrfCurrPair.GetTriangulatingCurrencyPair(trade.CurrencyPair())
                margin = GetTriangulatingSpotPrice(trade, currPair, splitCustomerSpotPrice) - spotCoverDealerSpotPrice
            else:
                return trade.ReferencePrice() - spotCoverDealerSpotPrice                
        if isSpotCoverSplit:            
            currPair = spotCoverPrfCurrPair.GetTriangulatingCurrencyPair(trade.CurrencyPair())            
            salesCustomerSpotPrice = GetTriangulatingSpotPrice(trade, currPair, splitSpotPrice)
            return salesCustomerSpotPrice - spotCoverDealerSpotPrice
        else:
            return trade.ReferencePrice() - spotCoverDealerSpotPrice
    return 0
'''================================================================================================
def GetSpotCoverSplitDealerSpotPrice(trade, isSpotcover, isSpotCoverSplit):
================================================================================================'''
@Debug('', DB.DEBUG)
def GetSpotCoverSplitDealerSpotPrice(trade, isSpotcover, isSpotCoverSplit, SplitSpotPrice):
    if isSpotcover and isSpotCoverSplit:
        return SplitSpotPrice
    return 0  
'''================================================================================================
================================================================================================'''
@Debug('', DB.DEBUG)
def GetTriangulatingSpotPrice(trade, otherCurrencyPair, otherRate):
    assert trade and otherCurrencyPair and otherRate and trade.CurrencyPair()
    tradeCurrencyPair = trade.CurrencyPair()
    tradeRate = 1/trade.ReferencePrice() if trade.CurrencyPair().Currency1() == trade.Currency() and trade.ReferencePrice() else trade.ReferencePrice()
    triangulatingCurrencyPair = tradeCurrencyPair.GetTriangulatingCurrencyPair(otherCurrencyPair)
    assert triangulatingCurrencyPair
    triangulatingRate = triangulatingCurrencyPair.TriangulateRate(otherCurrencyPair, otherRate, tradeCurrencyPair, tradeRate) if tradeRate else 0
    return triangulatingRate
'''================================================================================================
================================================================================================'''












