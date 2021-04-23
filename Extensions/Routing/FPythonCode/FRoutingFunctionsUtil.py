import acm

guiShell = acm.FBusinessLogicGUIDefault()
#mock this function in unit-tests to get a parameter returned rather than doing allocation and getting artifacts object
def WrapInParameterClass(trade):
        return acm.FFxTradeConstellationParameters(trade) 
        
def GetDefaultPortfolioFromTrade(trade):
    return GetDefaultPortfolioFromInstrumentPair(trade.InstrumentPair(), trade)

def GetDefaultPositionPairFromTrade(trade):
    portfolio = GetDefaultPortfolioFromInstrumentPair(trade.InstrumentPair(), trade)
    if portfolio:
        positionPair = portfolio.InstrumentPair()
    if not positionPair:
        positionPair = GetDefaultPositionPairFromInstrumentPair(trade.InstrumentPair(), trade)
    if not positionPair:
        positionPair = trade.InstrumentPair()
    return positionPair    
    
def GetDefaultPortfolioFromInstrumentPair(instrumentPair, trade):
    portfolio = None
    if trade.IsFxSpot():
        portfolio = instrumentPair.SpotPortfolio()
    elif trade.IsFxForward() or trade.IsFxSwapFarLeg():
        portfolio = instrumentPair.ForwardPortfolio()
    return portfolio
    
def GetDefaultPositionPairFromInstrumentPair(instrumentPair, trade):
    positionPair = None
    if trade.IsFxSpot():
        positionPair = instrumentPair.SpotSplitPair()
    elif trade.IsFxForward() or trade.IsFxSwapFarLeg():
        positionPair = instrumentPair.ForwardSplitPair()
    return positionPair

def GetPositionPair(positionPair, portfolio):
    if not positionPair:
        positionPair = portfolio.InstrumentPair()
    return positionPair
    
def IsFxUnevenSwap(trade):
    if trade.IsFxSwapFarLeg() and trade.IsFxUnevenSwap():
        return True
    return False

def CandidateForSplit(trade, splitPortfolio, splitPositionPair = None):
    isCandidate = False
    if not splitPositionPair:
        if splitPortfolio:
            splitPositionPair = splitPortfolio.InstrumentPair()
        
    if splitPositionPair and trade:
        isCandidate = splitPositionPair != trade.InstrumentPair()
    return isCandidate

def CandidateForB2B(trade):
    return trade.SalesDeskPortfolio() and trade.SalesDeskAcquirer()
    
def ValidateInstrumentAndTrade(trade ):        
    assert trade.TradeInstrumentType() in ['Commodity Variant', 'Curr'], "Instrument name %s not of type FCurrency or FCommodityVariant" % trade.Instrument().Name()
    assert not trade.IsFxSwapNearLeg()
    
def TradeConstellationParamters(trade):
    tradeIntoParam = trade
    if tradeIntoParam.IsFxSwap():
        tradeIntoParam = tradeIntoParam.ConnectedTrade()
    constellationParameters = WrapInParameterClass(tradeIntoParam)
    defaultParamsDecorator = acm.FFxTradeConstellationParametersLogicDecorator( acm.FFxTradeConstellationParameters(tradeIntoParam), guiShell )
    return constellationParameters, defaultParamsDecorator
    
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


def SetSpotCoverParametersFromDefault(constellationParameters, defaultParameters):
    constellationParameters.SpotCoverEnabled = defaultParameters.SpotCoverEnabled()
    constellationParameters.SpotCoverPortfolio = defaultParameters.SpotCoverPortfolio()
    constellationParameters.SpotCoverPositionPair = defaultParameters.SpotCoverPositionPair()
    constellationParameters.SpotCoverAcquirer = defaultParameters.SpotCoverAcquirer()
    constellationParameters.SpotCoverCurrency = defaultParameters.SpotCoverCurrency()
    constellationParameters.SpotCoverDate = defaultParameters.SpotCoverDate()
    constellationParameters.SpotCoverDealerSpotPrice = defaultParameters.SpotCoverDealerSpotPrice()

def SetSpotCoverWithSplitParametersFromDefault(constellationParameters, defaultParameters):
    spotCoverSplitSalesMargin = 0 

    constellationParameters.SpotCoverSplitPortfolio = defaultParameters.SpotCoverSplitPortfolio()
    constellationParameters.SpotCoverSplitAcquirer = defaultParameters.SpotCoverSplitAcquirer()
    constellationParameters.SpotCoverSplitDealerSpotPrice = defaultParameters.SpotCoverSplitDealerSpotPrice()
    constellationParameters.SpotCoverSplitSpotMargin = spotCoverSplitSalesMargin 

def SetSplitParametersFromDefault(constellationParameters, defaultParameters):
    sales_margin, points_sales_margin, far_sales_margin, split_far_points_sales_margin = 0, 0, 0, 0
    
    constellationParameters.SplitPortfolio = defaultParameters.SplitPortfolio()
    constellationParameters.SplitAcquirer = defaultParameters.SplitAcquirer()
    constellationParameters.SplitCustomerSpotPrice = defaultParameters.SplitCustomerSpotPrice()
    constellationParameters.SplitCustomerPrice = defaultParameters.SplitCustomerPrice()
    constellationParameters.SplitPriceMargin = sales_margin
    constellationParameters.SplitPointsMargin = points_sales_margin
    constellationParameters.SplitFarCustomerPrice = defaultParameters.SplitFarCustomerPrice()

def SetSwapToSpotParamsFromDefault(constellationParameters, defaultParameters):
    constellationParameters.SwapMainPortfolio = defaultParameters.SwapMainPortfolio()
    constellationParameters.SwapMainAcquirer = defaultParameters.SwapMainAcquirer()
    constellationParameters.SwapMainPoints = defaultParameters.SwapMainPoints()
    constellationParameters.SwapMainSpotDate = defaultParameters.SwapMainSpotDate()
    constellationParameters.SwapSplitPortfolio = defaultParameters.SwapSplitPortfolio()
    constellationParameters.SwapSplitAcquirer = defaultParameters.SwapSplitAcquirer()
    constellationParameters.SwapSplitPoints = defaultParameters.SwapSplitPoints()
    constellationParameters.SwapSplitSpotDate = defaultParameters.SwapSplitSpotDate()

def SetSplitOperationParameters(operationParams, tradeParameters, defaultParamsDecorator):
    if not operationParams.Acquirer1():
        operationParams.Acquirer1 = defaultParamsDecorator.SplitAcquirer()
    operationParams.Portfolio1 = defaultParamsDecorator.SplitPortfolio()
    if tradeParameters.PositionPair() and tradeParameters.PositionPair() != defaultParamsDecorator.Trade().InstrumentPair():
        operationParams.PositionPair1 = defaultParamsDecorator.Trade().InstrumentPair().GetTriangulatingInstrumentPair(tradeParameters.PositionPair())

def SetSpotCoverOperationParameters(operationParams, defaultParamsDecorator):
    operationParams.CoverInstrument = defaultParamsDecorator.SpotCoverCurrency()
    operationParams.Portfolio2 = defaultParamsDecorator.SpotCoverPortfolio()
    operationParams.PositionPair2 = defaultParamsDecorator.SpotCoverPositionPair()    
    if not operationParams.PositionPair2() and operationParams.Portfolio2():
        operationParams.PositionPair2 = defaultParamsDecorator.Trade().InstrumentPair()
    
    if not operationParams.Acquirer2():
        operationParams.Acquirer2(defaultParamsDecorator.SpotCoverAcquirer())

def SetSpotCoverSplitOperationParameters(operationParams, defaultParamsDecorator):
    operationParams.Portfolio3 = defaultParamsDecorator.SpotCoverSplitPortfolio()
    if not operationParams.Acquirer3():
        operationParams.Acquirer3 = defaultParamsDecorator.SpotCoverSplitAcquirer()
    if operationParams.PositionPair2() and operationParams.PositionPair2() != defaultParamsDecorator.Trade().InstrumentPair():
        operationParams.PositionPair3 = defaultParamsDecorator.Trade().InstrumentPair().GetTriangulatingInstrumentPair(operationParams.PositionPair2())
        
def SetSwapToSpotFromOperationParameters(defaultParamsDecorator, operationParams):
    defaultParamsDecorator.SwapMainPortfolio = operationParams.Portfolio5()
    defaultParamsDecorator.SwapMainAcquirer = operationParams.Acquirer5()
    defaultParamsDecorator.SwapSplitPortfolio = operationParams.Portfolio6()
    defaultParamsDecorator.SwapSplitAcquirer = operationParams.Acquirer6()

def SetB2BParametersFromDefault(constellationParameters, defaultParameters):
        constellationParameters.TradersPortfolio = defaultParameters.TradersPortfolio()
        constellationParameters.TradersPositionPair = defaultParameters.TradersPositionPair()
        constellationParameters.TradersAcquirer = defaultParameters.TradersAcquirer()
        constellationParameters.SalesCoverEnabled = defaultParameters.SalesCoverEnabled()
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

def SetB2BParamsFromOperationParams(trade, defaultParamsDecorator, operationParams, isSpotcover, isSplit, isSpotCoverSplit ):
    if operationParams.Portfolio4() and operationParams.Acquirer4():        
        spotCoverPrfCurrPair = defaultParamsDecorator.SpotCoverPositionPair()

        defaultParamsDecorator.TradersPortfolio = operationParams.Portfolio4()
        defaultParamsDecorator.TradersAcquirer = operationParams.Acquirer4()
        defaultParamsDecorator.TradersPositionPair = operationParams.PositionPair4()
        if trade.IsFxSwap():
            defaultParamsDecorator.FxSwapFarLegValueDate(trade.ValueDay())
        defaultParamsDecorator.SalesCoverEnabled = True
        constellationParam = defaultParamsDecorator.Parameters()
        
        if not trade.SalesSpotPrice():
            constellationParam.SalesCoverReferencePrice = defaultParamsDecorator.SalesCoverReferencePrice()                        
            constellationParam.SalesCoverPrice = defaultParamsDecorator.SalesCoverPrice()
            constellationParam.SalesCoverFarPrice = defaultParamsDecorator.SalesCoverFarPrice()
            constellationParam.SplitCustomerSpotPrice = defaultParamsDecorator.SplitCustomerSpotPrice()            
            constellationParam.SplitCustomerPrice = defaultParamsDecorator.SplitCustomerPrice()
            constellationParam.SplitFarCustomerPrice = defaultParamsDecorator.FarSplitCustomerPrice()            
            if constellationParam.SpotCoverPortfolio():
                if defaultParamsDecorator.SpotCoverSplitPortfolio() and constellationParam.SpotCoverPortfolio().InstrumentPair():
                    constellationParam.SpotCoverSplitDealerSpotPrice = defaultParamsDecorator.SplitCustomerSpotPrice()            
                    instrPair = constellationParam.SpotCoverPortfolio().InstrumentPair()
                    constellationParam.SpotCoverDealerSpotPrice = GetTriangulatingSpotPrice(trade, instrPair, constellationParam.SpotCoverSplitDealerSpotPrice())
                else:
                    constellationParam.SpotCoverDealerSpotPrice = trade.ReferencePrice()
            else:
                constellationParam.SpotCoverDealerSpotPrice = 0
                constellationParam.SpotCoverSplitDealerSpotPrice = 0
                
            constellationParam.SpotCoverSpotMargin = 0
        else:
            constellationParam.SalesCoverReferencePrice = trade.SalesSpotPrice()
            constellationParam.SalesCoverPrice = trade.SalesNearPrice()
            constellationParam.SalesCoverFarPrice = GetSalesCoverFarPrice(trade)
            constellationParam.SplitCustomerSpotPrice = GetSplitCustomerSpotPrice(trade, isSplit)
            constellationParam.SplitCustomerPrice = GetSplitCustomerPrice(trade, isSplit)
            constellationParam.SplitFarCustomerPrice = GetSplitFarCustomerPrice(trade, isSplit)
            constellationParam.SpotCoverDealerSpotPrice = GetSpotCoverDealerSpotPrice(trade, spotCoverPrfCurrPair, defaultParamsDecorator.TradersPositionPair(), isSplit, isSpotcover, isSpotCoverSplit)
            constellationParam.SpotCoverSplitDealerSpotPrice = GetSpotCoverSplitDealerSpotPrice(trade, isSpotcover, isSpotCoverSplit)
            constellationParam.SpotCoverSpotMargin = GetSpotCoverSpotMargin(trade, spotCoverPrfCurrPair, constellationParam.SplitCustomerSpotPrice(), constellationParam.SpotCoverDealerSpotPrice(), trade.SplitSpotPrice(), isSplit, isSpotcover, isSpotCoverSplit)
        constellationParam.SpotCoverSplitSpotMargin = 0        

def SetB2BTradeAndOperationParameters(trade, operationParameters, tradeParameters): 
    if CandidateForB2B(trade):
        operationParameters.Portfolio4(tradeParameters.Portfolio())
        operationParameters.Acquirer4(tradeParameters.Acquirer())
        operationParameters.PositionPair4(tradeParameters.PositionPair())
        tradeParameters.Portfolio(trade.SalesDeskPortfolio())
        tradeParameters.Acquirer(trade.SalesDeskAcquirer())
        tradeParameters.PositionPair(trade.InstrumentPair())

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
    
    if operationParams.Portfolio2() and operationParams.Acquirer2():
        defaultParamsDecorator.SpotCoverEnabled(spotCoverEnabled)
        defaultParamsDecorator.SpotCoverCurrency = operationParams.CoverInstrument()
        defaultParamsDecorator.SpotCoverPortfolio = operationParams.Portfolio2()
        defaultParamsDecorator.SpotCoverPositionPair = GetPositionPair(operationParams.PositionPair2(), operationParams.Portfolio2())
        
        defaultParamsDecorator.SpotCoverAcquirer = operationParams.Acquirer2()
        defaultParamsDecorator.SpotCoverSplitPortfolio = operationParams.Portfolio3()
        defaultParamsDecorator.SpotCoverSplitAcquirer = operationParams.Acquirer3()    

    SetB2BParamsFromOperationParams(trade, defaultParamsDecorator, operationParams, spotCoverEnabled, splitEnabled, spotCoverSplit)      
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
    SetB2BParametersFromDefault(constellationParameters, defaultParameters)
    
    return constellationParameters

def SetSwapToSpotOperationParameters(operationParams, defaultParamsDecorator):
    if not operationParams.Acquirer5():
        operationParams.Acquirer5 = defaultParamsDecorator.SwapMainAcquirer()
    operationParams.Portfolio5 = defaultParamsDecorator.SwapMainPortfolio()
    if not operationParams.Acquirer6():
        operationParams.Acquirer6 = defaultParamsDecorator.SwapSplitAcquirer()
    operationParams.Portfolio6 = defaultParamsDecorator.SwapSplitPortfolio()
    if operationParams.Portfolio5():
        operationParams.PositionPair5 = defaultParamsDecorator.Trade().PositionPair()
    if operationParams.Portfolio5() and defaultParamsDecorator.SpotCoverPositionPair():
        operationParams.PositionPair5 = defaultParamsDecorator.SpotCoverPositionPair()    
    if operationParams.PositionPair1() and defaultParamsDecorator.SwapSplitPortfolio():
        operationParams.PositionPair6 = operationParams.PositionPair1()        
    if operationParams.PositionPair3() and defaultParamsDecorator.SwapSplitPortfolio():
        operationParams.PositionPair6 = operationParams.PositionPair3()
    
def GetSalesCoverFarPrice(trade):
    if trade.IsFxSwap():
        return trade.SalesFarPrice()
    return 0
    
def GetSplitCustomerSpotPrice(trade, isSplit):
    if isSplit:
        return trade.SplitSpotPrice()
    return 0

def GetSplitCustomerPrice(trade, isSplit):
    if isSplit:
        return trade.SplitNearPrice()
    return 0

def GetSplitFarCustomerPrice(trade, isSplit):
    if isSplit and trade.IsFxSwap():
        return trade.SplitFarPrice()
    return 0

def GetSpotCoverDealerSpotPrice(trade, spotCoverPrfCurrPair, tradersPrfCurrPair, isSplit, isSpotcover, isSpotCoverSplit):
    if isSpotcover:
        if isSplit:   
            if isSpotCoverSplit:
                return trade.SalesSpotPrice()
            else:
                instrPair = trade.InstrumentPair().GetTriangulatingInstrumentPair(tradersPrfCurrPair)
                fxRate = trade.InstrumentPair().TriangulateRate(instrPair, trade.SplitSpotPrice(), tradersPrfCurrPair, trade.SalesSpotPrice())
                fxRate = 1/fxRate if trade.InstrumentPair().Instrument1() == trade.Currency() and fxRate else fxRate
                return fxRate
        else:
            if isSpotCoverSplit:
                instrPair = spotCoverPrfCurrPair.GetTriangulatingInstrumentPair(trade.InstrumentPair())     
                salesSpotPrice = 1/trade.SalesSpotPrice() if trade.InstrumentPair().Instrument1() == trade.Currency() and trade.SalesSpotPrice() else trade.SalesSpotPrice()

                fxRate = spotCoverPrfCurrPair.TriangulateRate(instrPair, trade.SplitSpotPrice(), trade.InstrumentPair(), salesSpotPrice) 
                return fxRate
            else:
                return trade.SalesSpotPrice()
    return 0
        
def GetSpotCoverSpotMargin(trade, spotCoverPrfCurrPair, splitCustomerSpotPrice, spotCoverDealerSpotPrice, splitSpotPrice, isSplit, isSpotcover, isSpotCoverSplit):
    if isSpotcover:
        if isSplit:
            if isSpotCoverSplit:
                instrPair = spotCoverPrfCurrPair.GetTriangulatingInstrumentPair(trade.InstrumentPair())
                margin = GetTriangulatingSpotPrice(trade, instrPair, splitCustomerSpotPrice) - spotCoverDealerSpotPrice
            else:
                return trade.ReferencePrice() - spotCoverDealerSpotPrice                
        if isSpotCoverSplit:            
            instrPair = spotCoverPrfCurrPair.GetTriangulatingInstrumentPair(trade.InstrumentPair())            
            salesCustomerSpotPrice = GetTriangulatingSpotPrice(trade, instrPair, splitSpotPrice)
            return salesCustomerSpotPrice - spotCoverDealerSpotPrice
        else:
            return trade.ReferencePrice() - spotCoverDealerSpotPrice
    return 0

def GetSpotCoverSplitDealerSpotPrice(trade, isSpotcover, isSpotCoverSplit):
    if isSpotcover and isSpotCoverSplit:
        return trade.SplitSpotPrice()
    return 0  

def GetTriangulatingSpotPrice(trade, otherInstrumentPair, otherRate):
    assert trade and otherInstrumentPair and otherRate and trade.InstrumentPair()
    tradeInstrumentPair = trade.InstrumentPair()
    tradeRate = 1/trade.ReferencePrice() if trade.InstrumentPair().Instrument1() == trade.Currency() and trade.ReferencePrice() else trade.ReferencePrice()
    triangulatingInstrumentPair = tradeInstrumentPair.GetTriangulatingInstrumentPair(otherInstrumentPair)
    assert triangulatingInstrumentPair
    triangulatingRate = triangulatingInstrumentPair.TriangulateRate(otherInstrumentPair, otherRate, tradeInstrumentPair, tradeRate) if tradeRate else 0
    return triangulatingRate
