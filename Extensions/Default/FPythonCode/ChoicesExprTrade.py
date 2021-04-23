

import acm
from ChoicesExprCommon import allEnumValuesExcludeNone


'''** Trade Status **'''
def getTradeStatusChoices( acmObj ):
    if acmObj.IsKindOf(acm.FTrade):
        # FTradeLogicDecorator objects as well
        trade = acmObj.Trade()
    elif acmObj.IsKindOf(acm.FSecurityTransfer):
        trade = acmObj.Source()
    elif acmObj.IsKindOf(acm.FCashTransfer) or acmObj.IsKindOf(acm.FCashFxRateFixing):
        trade = acmObj.Source().Trade()

    if trade.IsInfant():
        oldTrade = trade
        trade = acm.FTrade()
        trade.Apply(oldTrade)
        if not acmObj.IsKindOf(acm.FSecurityTransfer) and not acmObj.IsKindOf(acm.FCashTransfer):
            trade.Status('Simulated')
    else:
        trade = trade.OriginalOrSelf()

    return acm.FIndexedPopulator(trade.ValidTradeStatusChoices())

'''** Collateral Agreement Choices **'''
def getCollateralAgreementChoices(trade):
    populator = acm.FChoiceListPopulator()
    collateralAgreements = acm.Risk().CollateralAgreements(trade.Counterparty(), trade.Acquirer())
    populator.SetChoiceListSource(collateralAgreements)
    return populator

'''** Premium Calculation Methods **'''
def validPremiumCalculationMethods():
    return allEnumValuesExcludeNone( acm.FEnumeration['enum(PremiumCalculationMethod)'] )

def getAcquirers(trade=None):
    acquirers = acm.FParty.Select("notTrading = False and type = 'Intern Dept'")
    acquirers = acquirers.SortByProperty('StringKey', True)
    
    if trade and trade.IsKindOf(acm.FTrade) and trade.Acquirer():
        if not acquirers.Includes(trade.Acquirer()):
            acquirers.Add(trade.Acquirer())
    return acquirers

def getCurrencyPairPortfolioChoicesTriangulatedCurrencyPair(currencyPair, otherCurrencyPair, strict):
    portfolios = None
    if currencyPair:
        populator = currencyPair.TriangulatedCurrencyPairPortfolioPopulator(otherCurrencyPair, strict)
    else:
        portfolios = acm.Risk().UserPhysicalPortfolios()
        comparator = None
        populator = acm.FIndexedPopulator(portfolios)
        populator.SetComparator(comparator)
    return populator

def getCurrencyPairPortfolioChoices(currencyPair, strict = False):
    return getCurrencyPairPortfolioChoicesTriangulatedCurrencyPair(currencyPair, None, strict)


def getHedgePortfolioChoices(currencyPair):
    portfolios = None
    populator = acm.FChoiceListPopulator()
    if currencyPair:
        portfolios = currencyPair.ValidPortfolioChoices(True)
        comparator = currencyPair.PortfolioComparator()
    else:
        portfolios = acm.Risk().UserPhysicalPortfolios()
        comparator = None
        
    populator.SetChoiceListSource(portfolios)
    populator.SetComparator(comparator)
    return populator


def getParties():
    parties = acm.FParty.Select('')
    return parties
    
def getPhysicalPortfolioChoices():
    portfolios = acm.FPhysicalPortfolio.Select('compound=false')
    portfolios.SortByProperty('StringKey', True)
    return portfolios



def ins_is_fx_ndf(instrument):
    if instrument.Cid()== "Future/Forward":
        if instrument.UnderlyingType()== "Curr":
            if instrument.PayType() == "Forward":
                if instrument.SettlementType() == "Cash":
                    return True
    return False
    
filterCurr = None

def PositionPairFilter(currPair):
    global filterCurr
    if currPair.Currency1()==filterCurr or currPair.Currency2()==filterCurr:
        return True
    return False

def GetAllCurrencyPairsForCurrency( currency ):
    """
    returns all currencyPairs which contain currency
    """
    global filterCurr
    filterCurr = currency
    currencyPairs = acm.FCurrencyPair.Select("")
    currencyPairsFiltered = currencyPairs.Filter(PositionPairFilter)
    return currencyPairsFiltered
    
filterTradedInstrumentPair = None

def PreciousMetalPositionPairFilter(pmPair):
    global filterTradedInstrumentPair
    if pmPair.Instrument1()==filterTradedInstrumentPair.Instrument1():
        return pmPair.Instrument2() != filterTradedInstrumentPair.Instrument2()
    return False
    
def GetAllInstrumentPairsForPreciousMetal(tradedInstrumentPair):
    """
    returns all currencyPairs which contain commodityVariant
    """
    global filterTradedInstrumentPair
    filterTradedInstrumentPair = tradedInstrumentPair
    pmPairs = acm.FPreciousMetalPair.Select("")
    pmPairsFiltered = pmPairs.Filter(PreciousMetalPositionPairFilter)
    return pmPairsFiltered
    
    
def PositionPairChoicesImpl(object):
    try:
        trade = object.Trade()
        if trade:
            instrument = trade.Instrument()
            if ( (instrument.Cid() in ("Curr", "FXOptionDatedFwd")) or ins_is_fx_ndf(instrument) ):
                currencyPair = trade.CurrencyPair(True)
                if currencyPair:
                    return [cp for cp in currencyPair.AllTriangulatingInstrumentPairs() if (cp != object.Trade().CurrencyPair())]  
                else:
                    return None
            elif (instrument.Cid() == "Deposit"):
                return GetAllCurrencyPairsForCurrency( instrument.Currency() )
            elif (instrument.Cid() == "Commodity Variant"):
                return GetAllInstrumentPairsForPreciousMetal(trade.InstrumentPair(True))
                
        return acm.FCurrencyPair.Select("")
    except Exception as e:
        print ("Exception in the function PositionPairChoicesExpr connected to the ChoicesExpr list of the control PositionPair")
        print (e)

def PositionPairChoicesExpr(object):
    trade = object.Trade()
    if trade.IsSalesCoverParent():
        return trade.InstrumentPair()
    return PositionPairChoicesImpl(object)


def SplitCurrencyChoicesExpr(object):
    currs = acm.FArray()
    posPairs = PositionPairChoicesImpl(object)
    if posPairs:
        for posPair in posPairs:
            currs.Add(posPair.Instrument2())
    return currs

def TraderPositionPairChoicesExpr(object):
    return PositionPairChoicesImpl(object)
    
def TraderSplitCurrencyChoicesExpr(object):
    return SplitCurrencyChoicesExpr(object)

def SpotCoverPositionPairChoicesExpr(object):
    return PositionPairChoicesImpl(object)

def SpotCoverSplitCurrencyChoicesExpr(object):
    return SplitCurrencyChoicesExpr(object)

def getSwapMainPortfolioChoices(parameter):
    decorator = acm.FFxTradeConstellationParametersLogicDecorator(parameter.Clone(), acm.FBusinessLogicGUIDefault())
    currencyPair = decorator.SwapMainCurrencyPair()
    return getCurrencyPairPortfolioChoicesTriangulatedCurrencyPair(currencyPair, None, True)
    
def getSwapSplitPortfolioChoices(parameter):
    decorator = acm.FFxTradeConstellationParametersLogicDecorator(parameter.Clone(), acm.FBusinessLogicGUIDefault())
    currencyPair = decorator.SwapSplitCurrencyPair()
    return getCurrencyPairPortfolioChoicesTriangulatedCurrencyPair(currencyPair, None, True)

def getCashEntryAccounts(cashEntry):
    currency = cashEntry.Currency()
    acquirer = cashEntry.Trade().Acquirer()
    accountArray = acm.FArray()
    if acquirer:
        for account in acquirer.Accounts():
            if (account.Currency() == currency or account.Currency() == None):
                if ('Security' != account.AccountType()): 
                    accountArray.Add(account)
    return accountArray


def getPaymentTypes():
    return ['None',
            'Allocation Fee',
            'Assignment Fee',
            'Broker Fee',
            'Cash', 
            'Commission',
            'Exercise Cash',
            'Extension Fee',
            'Fill Fee',
            'Interest Accrued',
            'Internal Fee',
            'Premium',
            'Termination Fee',
            'Subscription/Redemption']

def getCashTransferPaymentTypes():
    return ['None', 'Account Transfer', 'Cash', 'Premium']

def getTradeKeyChoices(number):
    # find the name of the parent list
    st = 'list="MASTER" and name="Trade Keys"'
    tradeKeys = acm.FChoiceList.Select01(st, "")
    tk = tradeKeys.ChoicesSorted().At( number-1 )
    # return the children, sorted
    return tk.ChoicesSorted()

def getDiscountingTypeChoices():
    discountingTypes = None
    populator = acm.FChoiceListPopulator()
    
    discountingTypes = acm.FChoiceList.Select("list = 'DiscType'")
    populator.SetChoiceListSource(discountingTypes)

    return populator

def getCounterparties():
    q = "notTrading = False"
    q += " and type <> 'None'"
    q += " and type <> 'Issuer'"
    q += " and type <> 'MtM Market'"
    counterparties = acm.FParty.Select(q)
    counterparties = counterparties.SortByProperty('StringKey', True)
    return counterparties

def getAccountTransferPaymentTypes():
    paymentTypes = acm.FArray()
    paymentTypes.Add('Account Transfer')
    return paymentTypes
    
def getAccountAdjustmentPaymentTypes():
    paymentTypes = acm.FArray()
    paymentTypes.Add('Account Adjustment')
    return paymentTypes

def getCashAccounts(trade):
    currency = trade.Currency()
    acquirer = trade.Acquirer()
    accountArray = acm.FArray()
    if acquirer:
        for account in acquirer.Accounts():
            if (account.Currency() == currency or account.Currency() == None):
                if ('Cash and Security' == account.AccountType() or 'Cash' == account.AccountType()): 
                    accountArray.Add(account)
    return accountArray

def getSecurityAccounts(trade):
    currency = trade.Currency()
    acquirer = trade.Acquirer()
    accountArray = acm.FArray()
    if acquirer:
        for account in acquirer.Accounts():
            if (account.Currency() == currency or account.Currency() == None):
                if ('Cash and Security' == account.AccountType() or 'Security' == account.AccountType()): 
                    accountArray.Add(account)
    return accountArray

def tradeType(trade):
    return acm.FEnumeration['enum(TradeType)'].Enumerators()

def documentType(trade):
    populator = acm.FChoiceListPopulator()    
    documentTypes = acm.FChoiceList.Select("list = 'Standard Document'")
    populator.SetChoiceListSource(documentTypes)

    return populator
