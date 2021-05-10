import re
import acm
import FRoutingExtensions

DEFAULT_TRADE_SYSTEM = 'FRONT'

def isAGGREGATIONTradeSystem(trade):
    if trade.Type() in ('Aggregate', 'FX Aggregate', 'Cash Posting'):
        return 'AGGREGATION'

def isAMBATradeSystem(trade):
    if trade.CreateUser() and trade.CreateUser().Name() == 'AMBA':
        return 'AMBA'

def isAPEXTradeSystem(trade):
    tradeSystem = 'APEX'
    if trade.CreateUser() and trade.CreateUser().Name() == 'ATS_APEX':
        isNutronTrade = isNutronTradeSystem(trade)
        if isNutronTrade != None:
            return '%s_%s' %(tradeSystem, isNutronTrade)
        return tradeSystem

def isATSTradeSystem(trade):
    if trade.CreateUser() and trade.CreateUser().Name() == 'ATS':
        return 'ATS'

def isAxeTradeSystem(trade):
    if trade.OptionalKey():
        optionalKeySplit = trade.OptionalKey().split('|')
        if len(optionalKeySplit) >= 2:
            mainSystem = optionalKeySplit[1]
            if mainSystem == 'AXE':
                return '%s_%s' %(mainSystem, trade.AdditionalInfo().Source_System())

def isXTPTradeSystem(trade):
    optionalKey = trade.OptionalKey()
    if optionalKey:
        if optionalKey.__contains__('XTP_A2X'):
            return 'XTP_A2X'
        if optionalKey.__contains__('XTPEDR_COLO'):
            return 'XTP_COLO'
        elif optionalKey.__contains__('XTP'):
            return 'XTP_JSE'
        elif re.match('[0-9]+_[0-9]+', optionalKey):
            return 'XTP'

def isBARXFxOptionTradeSystem(trade):
    if trade.OptionalKey().__contains__('PFXO_'):
        return 'BARX_FX_Option'

def isBARXMMTradeSystem(trade):
    if trade.OptionalKey().__contains__('BARXMM'):
        return 'BARX_MM'

def isBARXTSTradeSystem(trade):
    if trade.OptionalKey().__contains__('BARXTS_T'):
        return 'BARX_TS'

def isFXAutorollTradeSystem(trade):
    if trade.Type() == 'Spot Roll':
        if trade.OptionalKey():
            return 'FAR_AUTOROLL'
        else:
            return 'FRONT_AUTOROLL'

def isOBPTradeSystem(trade):
    optionalKey = trade.OptionalKey()
    
    if (not optionalKey) and trade.MirrorTrade():
        mirrorTrade = trade.GetMirrorTrade()
        if isOBPTradeSystem(mirrorTrade) == 'OBP':
            return 'OBP'
            
    if re.match('B[A-Z]_[0-9]+_[0-9]+', optionalKey):
        return 'OBP'

def isMarkitWireTrade(trade):
    if trade.CreateUser().Name() in ('ATS_AMWI_PRD', 'ATS_AMWI_TST'):
        return 'MarkitWire'

def isNutronTradeSystem(trade):
    if trade.OptionalKey().__contains__('STATUS-'):
        return 'Nutron'

def isPLSweepTrade(trade):
    if isATSTradeSystem(trade) == 'ATS' and trade.Type() == 'PL Sweep':
        return 'FRONT_PL_SWEEP'

def isSafexTradeSystem(trade):
    if trade.OptionalKey().__contains__('SFX'):
        return 'SAFEX'

def isYieldXTradeSystem(trade):
    if trade.OptionalKey().__contains__('YIELDX'):
        return 'YIELD-X'

def billTradeSystem(trade):
    billTS = isAGGREGATIONTradeSystem(trade)
    
    return billTS
    
def bondTradeSystem(trade):
    bondTS = isAGGREGATIONTradeSystem(trade)
    if bondTS:
        return bondTS
        
    bondTS = isAPEXTradeSystem(trade)
    if bondTS:
        return bondTS
    
    bondTS = isAxeTradeSystem(trade)
    if bondTS:
        return bondTS
        
    bondTS = isNutronTradeSystem(trade)
    return bondTS

def buySellbackTradeSystem(trade):
    buySellbackTS = isAGGREGATIONTradeSystem(trade)
    if buySellbackTS:
        return buySellbackTS
        
    buySellbackTS = isNutronTradeSystem(trade)
    return buySellbackTS
    
def cfdTradeSystem(trade):
    cfdTS = isAGGREGATIONTradeSystem(trade)
    if cfdTS:
        return cfdTS
        
    cfdTS = isATSTradeSystem(trade)
    return cfdTS

def currTradeSystem(trade):
    currTS = isAGGREGATIONTradeSystem(trade)
    if currTS:
        return currTS
        
    currTS = isBARXTSTradeSystem(trade)
    if currTS:
        return currTS
        
    currTS = isBARXFxOptionTradeSystem(trade)
    if currTS:
        return currTS
    
    currTS = isFXAutorollTradeSystem(trade)
    if currTS:
        return currTS
        
    currTS = FRoutingExtensions.trade_system(trade)
    if currTS:
        return currTS

    currTS = isATSTradeSystem(trade)
    return currTS

def currSwapTradeSystem(trade):
    currSwapTS = isAGGREGATIONTradeSystem(trade)
    
    return currSwapTS

def depositTradeSystem(trade):
    depositTS = isAGGREGATIONTradeSystem(trade)
    if depositTS:
        return depositTS

    depositTS = isBARXMMTradeSystem(trade)
    return depositTS

def etfTradeSystem(trade):
    etfTS = isAGGREGATIONTradeSystem(trade)
    if etfTS:
        return etfTS

    etfTS = isOBPTradeSystem(trade)
    if etfTS:
        return etfTS
        
    etfTS = isXTPTradeSystem(trade)
    if etfTS:
        return etfTS
        
    etfTS = isAMBATradeSystem(trade)
    return etfTS

def fraTradeSystem(trade):
    fraTS = isAGGREGATIONTradeSystem(trade)
    if fraTS:
        return fraTS

    fraTS = isMarkitWireTrade(trade)
    if fraTS:
        return fraTS
        
    fraTS = isATSTradeSystem(trade)
    return fraTS

def frnTradeSystem(trade):
    frnTS = isAGGREGATIONTradeSystem(trade)
    if frnTS:
        return frnTS

    frnTS = isNutronTradeSystem(trade)
    return frnTS

def futureForwardTradeSystem(trade):
    futureForwardTS = isAGGREGATIONTradeSystem(trade)
    if futureForwardTS:
        return futureForwardTS

    futureForwardTS = isSafexTradeSystem(trade)
    if futureForwardTS:
        return futureForwardTS
        
    futureForwardTS = isXTPTradeSystem(trade)
    if futureForwardTS:
        return futureForwardTS
    
    futureForwardTS = isYieldXTradeSystem(trade)
    if futureForwardTS:
        return futureForwardTS
    
    futureForwardTS = isATSTradeSystem(trade)
    return futureForwardTS

def indexLinkedBondTradeSystem(trade):
    indexLinkedBondTS = isAGGREGATIONTradeSystem(trade)
    if indexLinkedBondTS:
        return indexLinkedBondTS

    indexLinkedBondTS = isNutronTradeSystem(trade)
    return indexLinkedBondTS

def optionTradeSystem(trade):
    optionTS = isAGGREGATIONTradeSystem(trade)
    if optionTS:
        return optionTS

    optionTS = isYieldXTradeSystem(trade)
    if optionTS:
        return optionTS
        
    optionTS = isSafexTradeSystem(trade)
    if optionTS:
        return optionTS
        
    optionTS = isBARXTSTradeSystem(trade)
    if optionTS:
        return optionTS
        
    optionTS = isBARXFxOptionTradeSystem(trade)
    if optionTS:
        return optionTS
        
    optionTS = isATSTradeSystem(trade)
    return optionTS

def repoReverseTradeSystem(trade):
    repoReverseTS = isAGGREGATIONTradeSystem(trade)
    if repoReverseTS:
        return repoReverseTS

    repoReverseTS = isNutronTradeSystem(trade)
    return repoReverseTS

def securityLoanTradeSystem(trade):
    securityLoanTS = isAGGREGATIONTradeSystem(trade)
    if securityLoanTS:
        return securityLoanTS
    
    securityLoanTS = isPLSweepTrade(trade)
    if securityLoanTS:
        return securityLoanTS
    
    securityLoanTS = isATSTradeSystem(trade)
    return securityLoanTS

def stockTradeSystem(trade):
    stockTS = isAGGREGATIONTradeSystem(trade)
    if stockTS:
        return stockTS
        
    stockTS = isXTPTradeSystem(trade)
    if stockTS:
        return stockTS
        
    stockTS = isOBPTradeSystem(trade)
    if stockTS:
        return stockTS
        
    stockTS = isAMBATradeSystem(trade)
    if stockTS:
        return stockTS
        
    stockTS = isATSTradeSystem(trade)
    return stockTS

def swapTradeSystem(trade):
    swapTS = isAGGREGATIONTradeSystem(trade)
    if swapTS:
        return swapTS
        
    swapTS = isMarkitWireTrade(trade)
    if swapTS:
        return swapTS
        
    swapTS = isATSTradeSystem(trade)
    return swapTS

def getTradeSystem(trade):
    trade_system = DEFAULT_TRADE_SYSTEM
    InsTypeClasification = {'Bill': billTradeSystem,
                            'Bond': bondTradeSystem,
                            'BuySellback': buySellbackTradeSystem,
                            'CFD': cfdTradeSystem,
                            'Curr': currTradeSystem,
                            'CurrSwap': currSwapTradeSystem,
                            'Deposit' : depositTradeSystem,
                            'ETF' : etfTradeSystem,
                            'FRA' : fraTradeSystem,
                            'FRN' : frnTradeSystem,
                            'Future/Forward' : futureForwardTradeSystem,
                            'IndexLinkedBond' : indexLinkedBondTradeSystem,
                            'Option' : optionTradeSystem,
                            'Repo/Reverse' : repoReverseTradeSystem,
                            'SecurityLoan' : securityLoanTradeSystem,
                            'Stock': stockTradeSystem,
                            'Swap' : swapTradeSystem}
    
    insType = trade.Instrument().InsType()
    
    try:
        trade_system_value = InsTypeClasification[insType](trade)
        if trade_system_value:
            trade_system = trade_system_value
        return trade_system
    except:
        return trade_system

#print getTradeSystem(acm.FTrade[75769389])
#print acm.FTrade[75769389].Instrument().InsType()
