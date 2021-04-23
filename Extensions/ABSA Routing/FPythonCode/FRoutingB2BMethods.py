import acm
from FRoutingExtensions import get_fx_rate 
'''================================================================================================
================================================================================================'''
def GetDealtCurrency(trade):return trade.Currency() if trade.QuantityIsDerived() else trade.Instrument()
def IsSpot(trade): return trade.ValueDay() == trade.CurrencyPair().SpotDate(acm.Time.DateNow())
'''================================================================================================
================================================================================================'''
def TradeSpotPrice(trade, tradAiproxy, isInverse):
    if IsSpot(trade): # [mklimke - cant we use trade process here?] 
        TradeSpotPrice = trade.Price() if tradAiproxy.B2BCrossMktPr() == None else tradAiproxy.B2BCrossMktPr()  
    else:
        TradeSpotPrice = trade.ReferencePrice() if tradAiproxy.B2BCrossSptMktPr() == None else tradAiproxy.B2BCrossSptMktPr()  
    return 1/TradeSpotPrice if isInverse == True else TradeSpotPrice 
'''================================================================================================
================================================================================================'''
def TradePrice(trade, tradeAiProxy, isInverse):
    TradePrice = trade.Price() if tradeAiProxy.B2BCrossMktPr() == None else tradeAiProxy.B2BCrossMktPr()
    return 1/TradePrice if isInverse == True else TradePrice 
'''================================================================================================
================================================================================================'''
def TradeFarPrice(trade, tradeAiProxy, isInverse):
    if trade.IsFxSwap():
        TradeFarPrice = trade.Price() if tradeAiProxy.B2BCrossSwpFarMktPr() ==  None else tradeAiProxy.B2BCrossSwpFarMktPr()
        return 1/TradeFarPrice if isInverse == True else TradeFarPrice 
    return 0.0
'''================================================================================================
================================================================================================'''
def PLCurrency(trade):
    if trade.CurrencyPair().IncludesCurrency(acm.FCurrency['ZAR']):
        return acm.FCurrency['ZAR']
    else:
        return trade.Instrument() if trade.QuantityIsDerived() else trade.Currency()
'''================================================================================================
================================================================================================'''
def SalesDeskPortfolio(trade):
    tradePortfolio = acm.FPhysicalPortfolio[trade.Portfolio().AssignInfo()]
    if tradePortfolio != None:
        for portfolioLink in tradePortfolio.MemberLinks():
            if portfolioLink.OwnerPortfolio() == acm.FPhysicalPortfolio['FX_SALES']:
                return tradePortfolio
'''================================================================================================
================================================================================================'''
def SalesDeskAcquirer(trade):
    salesDeskPortfolio = SalesDeskPortfolio(trade)
    return salesDeskPortfolio.PortfolioOwner() if salesDeskPortfolio else None 
'''================================================================================================
================================================================================================'''
def SalesSpotPrice(trade,tradAiproxy,salesCurrencyPair,isSplit = True,calculateMargin = False):
    if SalesDeskPortfolio(trade) != None:
        if tradAiproxy.B2BSptMktPr() == None:  
            if isSplit == True:
                return get_fx_rate(trade, salesCurrencyPair) 
            else: 
                if calculateMargin == True: 
                    return get_fx_rate(trade, trade.CurrencyPair()) 
                else: 
                    return tradAiproxy.B2BCrossSptMktPr() if tradAiproxy.B2BCrossSptMktPr() != None else trade.ReferencePrice() 
        else:
            return tradAiproxy.B2BSptMktPr()
'''================================================================================================
================================================================================================'''
def SalesNearPrice(trade,tradeAiProxy,salesCurrencyPair,isSplit = True,calculateMargin = False): 
    if isSplit == False:
        if trade.CurrencyPair().IncludesCurrency(acm.FCurrency['USD']): # Non cross
            if tradeAiProxy.B2BMktPr() == None:
                return trade.Price() if calculateMargin == False else get_fx_rate(trade, trade.CurrencyPair(), trade.ValueDay())
            else:
                return tradeAiProxy.B2BMktPr()
        else: 
            return get_fx_rate(trade, trade.CurrencyPair(), trade.ValueDay()) if tradeAiProxy.B2BCrossMktPr() == None else tradeAiProxy.B2BCrossMktPr() 
    else: 
        return tradeAiProxy.B2BMktPr() if tradeAiProxy.B2BMktPr() != None else get_fx_rate(trade, salesCurrencyPair, trade.ValueDay())    
'''================================================================================================
================================================================================================'''
def SalesFarPrice(trade,tradeAiProxy,salesCurrencyPair,isSplit = True,calculateMargin = False):
    if trade.IsFxSwap():
        return get_fx_rate(trade, salesCurrencyPair, trade.ValueDay()) if tradeAiProxy.B2BSwpFarMktPr() == None else tradeAiProxy.B2BSwpFarMktPr()   
    return 0.0
'''================================================================================================
================================================================================================'''
def SplitSpotPrice(trade, tradeAiProxy, splitCurrencyPair, isSplit): 
    if isSplit != False:
        return get_fx_rate(trade, splitCurrencyPair) if tradeAiProxy.B2BSplitSptMktPr() == None else tradeAiProxy.B2BSplitSptMktPr()
    return 0.0
'''================================================================================================
================================================================================================'''
def SplitNearPrice(trade, tradeAiProxy, splitCurrencyPair, isSplit):
    if isSplit == True:
        return get_fx_rate(trade, splitCurrencyPair, trade.ValueDay()) if tradeAiProxy.B2BSplitMktPr() == None else tradeAiProxy.B2BSplitMktPr()
    return 0.0
'''================================================================================================
================================================================================================'''
def SplitFarPrice(trade, tradeAiProxy, splitCurrencyPair, isSplit): 
    if isSplit == True and trade.IsFxSwap():
        return get_fx_rate(trade, splitCurrencyPair, trade.ValueDay()) if tradeAiProxy.B2BSplitSwpFarMktPr() == None else tradeAiProxy.B2BSplitSwpFarMktPr()
    return 0.0
'''================================================================================================
    B2BPortfolioSpt
Example:
    USD/ZAR:AGG|EUR/USD:HDG
Todo:
    Should these methods return the default?    
================================================================================================'''
def PortfolioSpt(trade, tradeAiProxy, splitCurrencyPair): 
    if tradeAiProxy.B2BPortfolioSpt() != None:
        try:
            splitCurrencyPairName = splitCurrencyPair.Name()
            for CurrencyPair in tradeAiProxy.B2BPortfolioSpt().split('|'):
                if splitCurrencyPairName == CurrencyPair.split(':')[0]:
                    return acm.FPhysicalPortfolio[CurrencyPair.split(':')[1]]
        except Exception, err:
            print err
'''================================================================================================
    B2BPortfolioFwd
Example:
    USD/ZAR:AGG|EUR/USD:HDG
================================================================================================'''
def PortfolioFwd(trade, tradeAiProxy, splitCurrencyPair): 
    if tradeAiProxy.B2BPortfolioFwd() != None:
        try:
            splitCurrencyPairName = splitCurrencyPair.Name()
            for CurrencyPair in tradeAiProxy.B2BPortfolioFwd().split('|'):
                if splitCurrencyPairName == CurrencyPair.split(':')[0]:
                    return acm.FPhysicalPortfolio[CurrencyPair.split(':')[1]]
        except Exception, err:
            print err
'''================================================================================================
================================================================================================'''
def SetPortfolios(trade, tradeAiProxy, operationParameter, isSplit, salesCurrencyPair, splitCurrencyPair):
    if isSplit:
        if not IsSpot(trade):
            Portfolio1 = PortfolioFwd(trade, tradeAiProxy, splitCurrencyPair)
            Portfolio2 = PortfolioSpt(trade, tradeAiProxy, salesCurrencyPair)
            Portfolio3 = PortfolioSpt(trade, tradeAiProxy, splitCurrencyPair)
            Portfolio4 = PortfolioFwd(trade, tradeAiProxy, salesCurrencyPair)
            if Portfolio1 != None: operationParameter.Portfolio1(Portfolio1)
            if Portfolio2 != None: operationParameter.Portfolio2(Portfolio2)
            if Portfolio3 != None: operationParameter.Portfolio3(Portfolio3)
            if Portfolio4 != None: operationParameter.Portfolio4(Portfolio4)
        else: 
            Portfolio1 = PortfolioSpt(trade, tradeAiProxy, splitCurrencyPair)
            Portfolio4 = PortfolioSpt(trade, tradeAiProxy, salesCurrencyPair)
            if Portfolio1 != None: operationParameter.Portfolio1(Portfolio1) 
            if Portfolio4 != None: operationParameter.Portfolio4(Portfolio4) 
    else:
        if not IsSpot(trade):
            Portfolio2 = PortfolioSpt(trade, tradeAiProxy, salesCurrencyPair)
            Portfolio4 = PortfolioFwd(trade, tradeAiProxy, salesCurrencyPair)
            if Portfolio2 != None: operationParameter.Portfolio2(Portfolio2) 
            if Portfolio4 != None: operationParameter.Portfolio4(Portfolio4) 
        else:
            Portfolio4 = PortfolioSpt(trade, tradeAiProxy, salesCurrencyPair)
            if Portfolio4 != None: operationParameter.Portfolio4(Portfolio4)
'''================================================================================================
================================================================================================'''



