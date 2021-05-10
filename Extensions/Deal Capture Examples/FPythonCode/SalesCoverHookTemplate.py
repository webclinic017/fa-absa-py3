
import acm

PAYMENT_TYPE = 'Premium' 
standardCalcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
calcSpace = acm.Calculations().CreateCalculationSpaceCollection().GetSpace(acm.FDealSheet, acm.GetDefaultContext())

def SalesCoverDelete(artifacts):
    '''
    This function is called when the lead trade is deleted or the Sales Cover is removed from the lead trade. The input argument, artifacts, is an array containing the trades which are about to be deleted. Any additional objects which should be deleted should be added to the returnArray. The objects in the returnArray should be ordered in the order they should be deleted.
    '''
    
    returnArray = acm.FArray()

    return returnArray

def SalesCoverFxAndPmConstellation(artifacts, args):
    '''
    Write your sales cover code for FX and PM deals here
    '''
    pass

def SalesCoverOther(artifacts, args):
    '''
    Write your sales cover code for non-FX and PM deals here.
    Provided bellow is an example where margins are moved to payments.
    '''
    MoveMarginToPayments(artifacts)

def PreAllocateRisk(parameters):
    '''
    After parameters are set in the trade capture screen, before risk allocation is run.
    Return: args to pass into PostAllocateRisk
    '''
    pass
    
def PostAllocateRisk(artifacts, args):
    '''
    After risk allocation is run, before artifacts (trades, instruments, business events etc) are committed.
    '''
    if artifacts.ArtifactsToBeCommitted().IsEmpty():
        return
    if artifacts.Class().IsEqual(acm.FFxRiskAllocationResult):
        SalesCoverFxAndPmConstellation(artifacts, args)
    else:
        SalesCoverOther(artifacts, args)        
    
    
def InitializeParameters(parameters):
    '''
    After default initialization of sales cover paramters from persisted trade, before presentation in the 
    trade capture screen.
    '''
    if not parameters.IsKindOf(acm.FFxTradeConstellationParameters):
        InitializeParameters_MarginInPayments(parameters)

def MoveMarginToPayments(artifacts):
    customerTrade = None
    tradingDeskTrade = None
    for arti in artifacts.ArtifactsToBeCommitted():
        if arti.IsKindOf(acm.FTrade):
            if arti.IsSalesCoverParent():
                customerTrade = arti
                customerTrade.RegisterInStorage()
            if arti.IsSalesCoverChild():
                tradingDeskTrade = arti
                tradingDeskTrade.RegisterInStorage()
    if (not customerTrade) or (not tradingDeskTrade):
        return
    
    marginAmount = CalculateMargin(customerTrade, tradingDeskTrade)
    CopySalesCoverValues(tradingDeskTrade, customerTrade)
    
    CreatePayment(-marginAmount, tradingDeskTrade, customerTrade.Acquirer())

def CalculateMargin(custTrade, traderTrade):
    accountingCurrency = acm.UsedValuationParameters().AccountingCurrency()
    premiumMargin = custTrade.Premium() - traderTrade.Premium()
    
    if accountingCurrency != custTrade.Currency():
        fxRate = GetFxRate(custTrade, accountingCurrency)
        if fxRate:
            custTrade.BoFxRate(fxRate)
            traderTrade.BoFxRate(fxRate)
            premiumMargin = premiumMargin * fxRate
    
    presentValueMargin = 0
    if custTrade.Instrument().IsKindOf(acm.FCashFlowInstrument):
        custTradeValue = calcSpace.CalculateValue(custTrade, 'Present Value').Number()
        traderTradeValue = calcSpace.CalculateValue(traderTrade, 'Present Value').Number()
        presentValueMargin = custTradeValue - traderTradeValue
    
    margin = acm.DenominatedValue(premiumMargin + presentValueMargin, accountingCurrency, PAYMENT_TYPE, custTrade.TradeTime())
    return margin 
    
def GetFxRate(trade, currency):
    try:
        fxRate = trade.BoFxRate()
        if not fxRate:
            fxRate = trade.Currency().Calculation().FXRate(standardCalcSpace, currency, trade.TradeTime()).Number()
        return fxRate
    except Exception as e:
        raise Exception('Failed to get historical fx rate [%s]' % e)

def CopySalesCoverValues(toTrade, fromTrade):
    toTrade.Price(fromTrade.Price())
    toTrade.UpdatePremium(True)
    
    if toTrade.Instrument().IsKindOf(acm.FCashFlowInstrument):
        toLeg = GetSalesCoverLeg(toTrade.Instrument())
        fromLeg = GetSalesCoverLeg(fromTrade.Instrument())
        
        toLeg.FixedPrice(fromLeg.FixedPrice())
        toLeg.Spread(fromLeg.Spread())
        
        toLeg.GenerateCashFlows(0.0)

def GetSalesCoverLeg(ins):
    leg = ins.FirstFixedLeg()
    if not leg:
        leg = ins.FirstPayleg()
    if not leg:
        leg = ins.FirstLeg()
    return leg

def CreatePayment(amount, trade, party):
    payment = None
    for p in trade.Payments():
        if p.Type() == PAYMENT_TYPE:
            payment = p
    if not payment:
        payment = acm.FPayment()
        payment.Trade(trade)
        trade.Payments().Add(payment)
        
    payment.RegisterInStorage()
    payment.Amount(amount.Number())
    payment.Currency(amount.Unit())
    payment.Party(party)
    payment.PayDay(amount.DateTime())
    payment.Type( PAYMENT_TYPE )

def InitializeParameters_MarginInPayments(parameters):
    trade = parameters.Trade()
    if not trade.IsSalesCoverParent():
        return
    
    constellation = acm.FX().ConstellationFromTrade(trade)
    
    for t in constellation.AllTrades():
        if t.IsSalesCoverChild():
            tradingDeskTrade = t
    if tradingDeskTrade:
    
        gui = acm.FBusinessLogicGUIDefault()
        paramDec = acm.FB2BSalesCoverConstellationParametersLogicDecorator(parameters, gui)
        tradingDeskTradeDeco = acm.FTradeLogicDecorator(tradingDeskTrade, gui)
        
        paramDec.SalesMargin(tradingDeskTradeDeco.SalesMargin())
        CopySalesCoverValues(trade, tradingDeskTrade)
        paramDec.Refresh()
    
