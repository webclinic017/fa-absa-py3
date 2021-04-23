""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLMapping.py"
import acm

BASIS_SWAP              = 'Basis Swap'
BOND_OPTION             = 'Bond Option'
BOND_FORWARD            = 'Bond Forward'
BOND_SPOT               = 'Bond Spot'
BOND_REPO               = 'Bond Repo'
CAP                     = 'Cap'
CREDIT_DEFAULT_SWAP     = 'Credit Default Swap'
CURRENCY_SWAP           = 'Currency Swap'
EQUITY_OPTION           = 'Equity Option'
EQUITY_FORWARD          = 'Equity Forward'
EQUITY_SPOT             = 'Equity Spot'
EQUITY_SWAP             = 'Equity Swap'
EQUITY_REPO             = 'Equity Repo'
FRA                     = 'FRA'
FLOOR                   = 'Floor'
FX_BARRIER_OPTION       = 'FX Barrier Option'
FX_BINARY_OPTION        = 'FX Binary Option'
FX_FORWARD              = 'FX Forward'
FX_OPTION               = 'FX Option'
FX_CASH                 = 'FX Spot'
FX_SWAP                 = 'FX Swap'
INTEREST_DERIVATIVE     = 'Interest Derivative'
SWAP                    = 'Interest Rate Swap'
MM_LOAN_DEPOSIT         = 'MM Loan-Deposit'
DEMAND_LOAN_DEPOSIT     = 'Demand Loan-Deposit'
BOND_DERIVATIVE         = 'Other Bond Derivative'
EQUITY_DERIVATIVE       = 'Other Equity Derivative'
FX_DERIVATIVE           = 'Other FX Derivative'
OVERNIGHT_INDEX_SWAP    = 'Overnight Index Swap'
ODF                     = FX_FORWARD
SECURITIES_BORROW_LEND  = 'Securities Borrow-Lend'
SWAPTION                = 'Swaption'
TOTAL_RETURN_SWAP       = 'Total Return Swap'
UNKNOWN                 = 'Unknown'

# Swap types for Equity Swaps
EQEQ                    = 'Equity-Equity'
IREQ                    = 'Equity-IR'

excludeList = [ \
    #CREDIT_DEFAULT_SWAP, \
    #CURRENCY_SWAP, \
    #FRA, \
    #FX_FORWARD, \
    #FX_OPTION, \
    #FX_CASH, \
    #SWAP, \
    #DEMAND_LOAN, \
    #DEMAND_DEPOSIT, \
    #MM_DEPOSIT, \
    #MM_LOAN \
    ]

fixedIncomeInstrumentTypes = [ \
    'Bond', \
    'Bill', \
    'CD', \
    'CLN', \
    'DualCurrBond', \
    'FRN', \
    'IndexLinkedBond', \
    'MBS/ABS', \
    'PromisLoan', \
    'Zero', \
    'FreeDefCF' \
    ]
    
equityInstrumentTypes = [ \
    'Stock', \
    'Depositary Receipt', \
    'EquityIndex', \
    'Commodity', \
    'Commodity Index' \
    ]

def isVanilla(instrument):
    return instrument.ExerciseType() in ('European', 'American') and instrument.ExoticType() in ('None') and instrument.QuantoOptionType() in ('None')

def isVanillaOption(instrument):
    return isVanilla(instrument) and instrument.Digital() == 0

def isBinaryOption(instrument):
    return instrument.Digital() == 1 and instrument.ExerciseType() in ('European', 'American') and instrument.QuantoOptionType() in ('None')

def isBarrierOption(instrument):
    for e in instrument.Exotics():
        if e.BarrierOptionType != 'None':
            return True
    return False

def isForward(instrument):
    return instrument.PayType() == 'Forward'

def swapIsBasedOnEquity(swapInstrument):
    leg = getEquityLeg1(swapInstrument)
    if leg and leg.FloatRateReference() and leg.FloatRateReference().IsBasedOnEquity():
        return True
    return False
    
def isFixedIncomeInstrumentType(instrument):
    if instrument.InsType() in fixedIncomeInstrumentTypes:
        return True
    elif instrument.InsType() == 'TotalReturnSwap' and not swapIsBasedOnEquity(instrument):
        return True 
    return instrument.Underlying() and instrument.UnderlyingType() in fixedIncomeInstrumentTypes


def isFixedIncomeInstrumentTypeInsType(insType, undInsType):
    """
    this function does the same as isFixedIncomeInstrumentType(instrument),
    but it is used for deleted instruments, a TRS should not be sent to this function
    """
    if insType in fixedIncomeInstrumentTypes:
        return True
    return undInsType and undInsType in fixedIncomeInstrumentTypes

def isEquityInstrumentType(instrument):
    return isEquityInstrumentTypeInsType(instrument.InsType(), instrument.UnderlyingType())

def isEquityInstrumentTypeInsType(insType, undInsType):
    if insType in equityInstrumentTypes:
        return True
    return undInsType and undInsType in equityInstrumentTypes


def getEquitySwapType(equitySwapInstrument):
    legs = equitySwapInstrument.Legs()
    if getEquityLeg2(equitySwapInstrument):
        return EQEQ
    return IREQ

def getTotalReturnLegsSorted(equitySwapInstrument):
    totalReturnLegs = [l for l in equitySwapInstrument.Legs() if l.LegType() == "Total Return"]
    totalReturnLegs.sort(lambda x, y : x.PayLeg() and -1 or (y.PayLeg() and 1 or 0))
    return totalReturnLegs

def getEquityLeg1(equitySwapInstrument):
    totalReturnLegs = getTotalReturnLegsSorted(equitySwapInstrument)
    return len(totalReturnLegs) and totalReturnLegs[0] or None

def getEquityLeg2(equitySwapInstrument):
    totalReturnLegs = getTotalReturnLegsSorted(equitySwapInstrument)
    return 2 == len(totalReturnLegs) and totalReturnLegs[1] or None

def getPayOrReceiveEquity1(equitySwapTrade):
    equityLeg1 = getEquityLeg1(equitySwapTrade.Instrument())
    if isPayLeg(equityLeg1, equitySwapTrade):
        return "Pay"
    return "Receive"

def isPayLeg(leg, trade):
    if leg.PayLeg():
        if trade.Quantity() > 0:
            return True
        return False
    else: 
        if trade.Quantity() < 0:
            return True
        return False

def getIREquity2Currency(equitySwapInstrument):
    if getEquityLeg2(equitySwapInstrument):
        return getEquityLeg2(equitySwapInstrument).Currency()
    equityLeg1 = getEquityLeg1(equitySwapInstrument)
    if equityLeg1.PayLeg():
        return [l for l in equitySwapInstrument.Legs() if not l.PayLeg()][0].Currency() 
    else:
        return [l for l in equitySwapInstrument.Legs() if l.PayLeg()][0].Currency()
        
def getTRSUnderlyingName(trsInstrument):
    totalReturnLegs = getTotalReturnLegsSorted(trsInstrument)
    return len(totalReturnLegs) and totalReturnLegs[0].FloatRateReference().Oid() or None
    
def getNoticePeriodDays(instrument):
    startDate = instrument.StartDate()
    noticePeriod = instrument.NoticePeriod()
    dateAdjustPeriod = acm.Time.DateAdjustPeriod(startDate, noticePeriod)
    return acm.Time.DateDifference(dateAdjustPeriod, startDate)

def getInitialPrice(totalReturnSwapInstrument):
    totalReturnLegs = getTotalReturnLegsSorted(totalReturnSwapInstrument)
    return len(totalReturnLegs) and totalReturnLegs[0].InitialIndexValue()
    
def getIREquity2Principal(equitySwapTrade):
    leg = None
    equitySwapInstrument = equitySwapTrade.Instrument()
    equityLeg2 = getEquityLeg2(equitySwapInstrument)
    if equityLeg2:
        leg = equityLeg2
    else:
        equityLeg1 = getEquityLeg1(equitySwapInstrument)
        leg = [l for l in equitySwapInstrument.Legs() if l.PayLeg() != equityLeg1.PayLeg()][0]
    payOrReceive = isPayLeg(leg, equitySwapTrade) and -1 or 1
    return leg.InitialIndexValue() * equitySwapTrade.Quantity() * leg.IndexRef().ContractSizeInQuotation() * payOrReceive

    
def getEquity1Principal(equitySwapTrade):
    equitySwapInstrument = equitySwapTrade.Instrument()
    totalReturnLeg = getTotalReturnLegsSorted(equitySwapInstrument)[0]
    indexRef = totalReturnLeg.IndexRef()
    payOrReceive = isPayLeg(totalReturnLeg, equitySwapTrade) and -1 or 1
    return totalReturnLeg.InitialIndexValue() * equitySwapTrade.Quantity() * indexRef.ContractSizeInQuotation() * payOrReceive
    
def _getExercisingTrade(trade):
    toReturn = None
    bEvent = trade.OriginalOrSelf().BusinessEvents('Exercise/Assign')
    if bEvent:
        for link in bEvent[0].TradeLinks():
            linkTrade = link.Trade()
            if linkTrade.Type() in ['Exercise', 'Assign', 'Abandon'] and \
               linkTrade.Status() not in ['Void', 'Simulated'] and\
               linkTrade.Instrument().IsKindOf(acm.FOption):
                toReturn = linkTrade
                break
    return toReturn

def getFACLExpiryDate(trade):
    toReturn = trade.Instrument().ExpiryDateOnly()
    if trade.Instrument().IsKindOf(acm.FOption):
        exercisingTrade = _getExercisingTrade(trade)
        if exercisingTrade:
            toReturn = exercisingTrade.TradeTime()
        
    return acm.Time().AsDate(toReturn)
    
def getFACLSettlementDate(trade):
    toReturn = max(trade.AcquireDay(), trade.ValueDay())
    if trade.Instrument().IsKindOf(acm.FOption):
        exercisingTrade = _getExercisingTrade(trade)
        if exercisingTrade:
            toReturn = max(exercisingTrade.AcquireDay(), exercisingTrade.ValueDay())
        else:
            toReturn = trade.Instrument().SettlementDate()
    return acm.Time().AsDate(toReturn)
    
def getFACLProduct( trade ):
    product = getFACLProduct_internal( trade )
    if product in excludeList:
        product = UNKNOWN
    return product
    
def getFACLProduct_internal( trade ):
    instrument = trade.Instrument()
        
    if instrument.InsType() == 'Curr':
        if trade.IsFxSpot(): 
            return FX_CASH
        elif trade.IsFxForward():
            return FX_FORWARD
        elif trade.IsFxSwapNearLeg():
            return FX_SWAP
        elif trade.IsFxSwapFarLeg():
            return FX_SWAP            
            
    elif instrument.InsType() == 'Option':
        if isFixedIncomeInstrumentType(instrument.Underlying()): 
            if isVanillaOption(instrument):
                return BOND_OPTION
            else:
                return UNKNOWN
        elif isEquityInstrumentType(instrument.Underlying()): 
            if isVanillaOption(instrument):
                return EQUITY_OPTION
            else:
                return UNKNOWN
        elif instrument.UnderlyingType() == 'Curr':
            if isVanillaOption(instrument):
                return FX_OPTION
            elif isBinaryOption(instrument):
                return FX_BINARY_OPTION
            elif isBarrierOption(instrument):
                return FX_BARRIER_OPTION
            else:
                return UNKNOWN
        elif instrument.UnderlyingType() == 'Swap':
            if isVanillaOption(instrument):
                return SWAPTION
            else:
                return UNKNOWN
                
    elif instrument.InsType() == 'Future/Forward':
        if isFixedIncomeInstrumentType(instrument.Underlying()): 
            if isForward(instrument):
                return BOND_FORWARD
            else:
                return UNKNOWN
        elif isEquityInstrumentType(instrument.Underlying()): 
            if isForward(instrument):
                return EQUITY_FORWARD
            else:
                return UNKNOWN
        elif instrument.UnderlyingType() == 'Curr':
            if (isForward(instrument) and instrument.SettlementType() == 'Cash'):
                return FX_FORWARD
            else:
                return UNKNOWN
               
    elif instrument.InsType() == 'Repo/Reverse':
        if isFixedIncomeInstrumentType(instrument.Underlying()):
            return BOND_REPO
        elif instrument.Underlying() and instrument.Underlying().IsBasedOnEquity():
            return EQUITY_REPO
        else:
            return UNKNOWN
    
    elif instrument.InsType() == 'TotalReturnSwap':  
        if swapIsBasedOnEquity(instrument):
            return EQUITY_SWAP
        else:
            return TOTAL_RETURN_SWAP
            
    elif instrument.InsType() == 'SecurityLoan':
        return SECURITIES_BORROW_LEND
    elif instrument.InsType() == 'CreditDefaultSwap':
        return CREDIT_DEFAULT_SWAP
    elif instrument.InsType() == 'CurrSwap':
        return CURRENCY_SWAP
    elif instrument.InsType() == 'Cap':
        return CAP
    elif instrument.InsType() == 'Floor':
        return FLOOR
    elif instrument.InsType() == 'FRA':
        return FRA
    elif instrument.InsType() == 'Swap':
        floatLegCounter = 0
        for leg in instrument.Legs():
            if leg.LegType() == 'Float':
                floatLegCounter += 1
                if leg.ResetType() == 'Compound':
                    return OVERNIGHT_INDEX_SWAP
                if floatLegCounter == 2:
                    return BASIS_SWAP
        return SWAP
    elif instrument.InsType() == 'Deposit':
        for leg in instrument.Legs():
            if leg.LegType() in ('Call Fixed', 'Call Float', 'Call Fixed Adjustable'):
                return DEMAND_LOAN_DEPOSIT
        return MM_LOAN_DEPOSIT        
    elif instrument.InsType() == 'BuySellback':
        return UNKNOWN
    
    elif isFixedIncomeInstrumentType(instrument):
        if not instrument.IsDerivative():
            return BOND_SPOT   
     
    elif isEquityInstrumentType(instrument):
        if not instrument.IsDerivative():
            return EQUITY_SPOT
    elif instrument.InsType() == 'FXOptionDatedFwd':
        return ODF
        
    return UNKNOWN
