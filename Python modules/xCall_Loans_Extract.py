'''----------------------------------------------------------------------------------------------------------------------------------
Description                    :  Extract of all call loans, with the following rules:
                                - Balance to be positive 
                                - Exclude Credit limits that are less than R5
                                - Exclude CP's starting with ZZZ (in trade filter)
                                - Only include lines with non 0 Balances for a CP
                                - If a CP only has lines with 0 balance, include 1 line
                                - Divide the credit limit by the number of remaining accounts

Purpose                       :  [Initial deployment]
Department and Desk           :  [PCG - SND]
Requester                     :  [Andrew Nicholson]
Developer                     :  [Bhavnisha Sarawan]
CR Number                     :  [C416230]
----------------------------------------------------------------------------------------------------------------------------------'''



import acm, time, FCreditLimit, ael, string, os, csv

ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'xCall Loans Extract'}
                      
ael_variables = [ ['Path', 'Path', 'string', None, '', 1],
                  ['Filename', 'Filename', 'string', None, 'xCall_Loans_Extract.csv', 1],
                  ['Filter', 'Filter', 'FTradeSelection', None, 'Call_Loans_Extract', 1, 1, 'select trade filter', None, 1]]

context = acm.FExtensionContext['Repo']
calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
calcSpaceRepo = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')

def ael_main(parameter, *rest):
    
    fileName = os.path.join(parameter['Path'], parameter['Filename'])
    tradeFilter = parameter['Filter'][0]
    
    try:
        tradeFilter1 = removeSmallLimits(tradeFilter) 
    except Exception, e:
        print "Error occured in removing small limits: ", e  

    try:
        BalanceDict = getBalanceDict(tradeFilter1)
    except Exception, e:
        print "Error occured in creating a trade-balance dictionary: ", e  
        
        
    try:
        workingTrades = getWorkingTrades(tradeFilter1)
    except Exception, e:
        print "Error occured creating the SDS-trades dictionary: ", e  
        
  
    try:
        finalData = removeExtraLines(workingTrades, BalanceDict)
    except Exception, e:
        print "Error occured in removing the extra lines according to 0 balance: ", e  
        

    try:
        writeData(fileName, finalData, BalanceDict)
        print 'success|completed successfully'
        print 'Wrote secondary output to', fileName
    except Exception, e:
        print "Error occured writing out the data to the file: ", e  
  

def getBalance(trade):
    # Retrieves the balance of the trade
    balance = 0
    try:
        balance = abs(round(calcSpace.CalculateValue(trade, 'Deposit balance').Number(), 2))
    except:
        balance = 0.0
    return balance


def removeSmallLimits(tradeFilter):
    # Removes all trades with Counterparties that have a limit less than R5
    validLimit = [vl for vl in tradeFilter.Trades() if FCreditLimit.limit_cp(ael.Party[vl.Counterparty().Name()]) > 5.00]
    return validLimit


def getBalanceDict(tradeFilter):
    # Creates a dictionary of trades to balance for reuse
    BalanceDict = acm.FDictionary()
    for trade in tradeFilter:
        BalanceDict[trade.Name()] = getBalance(trade)
    return BalanceDict


def getWorkingTrades(tradeFilter):
    # Returns a dictionary of counterparty name and a list of trades linked to that counterparty
    TradeDict = acm.FDictionary()
    for trade in tradeFilter:
        key = trade.Counterparty().Name()
        if TradeDict.HasKey(key):
            TradeDict[key].Add(trade.Oid())
        elif not TradeDict.HasKey(key):
            TradeDict[key] = acm.FArray()
            TradeDict[key].Add(trade.Oid())
    return TradeDict


def removeExtraLines(TradeDict, BalanceDict):
    # Removes extra lines by returning trades with a non zero balance or only 1 zero balance for a counterparty
    tradeFilter = []
    for key in TradeDict.Keys():
        #print key, TradeDict[key]
        
        validNonZero = [nz for nz in TradeDict[key] if round(float(BalanceDict[str(nz)]), 0) != 0]
        if len(validNonZero) == 0:
            tradeFilter.append(TradeDict[key][0])
        else:
            for v in validNonZero:
                tradeFilter.append(v)
    return tradeFilter

def getRate(trade):
    node = calcSpaceRepo.InsertItem(trade)
    calcSpaceRepo.Refresh()
    Iter = node.Iterator().Clone().FirstChild()
    rate = calcSpaceRepo.CalculateValue(Iter.Tree(), 'New Rate')
    return rate

def getLimitDict(finalData):
#Creates a new dict of counterparty to trades with the final data.
#The final number of counterparty to trade ratio is needed for calculating the CPLimit in writeData()
    LimitDict = acm.FDictionary()
    for t in finalData:
        trade = acm.FTrade[t]
        key = trade.Counterparty().Name()
        if LimitDict.HasKey(key):
            LimitDict[key].Add(trade.Oid())
        elif not LimitDict.HasKey(key):
            LimitDict[key] = acm.FArray()
            LimitDict[key].Add(trade.Oid())
    return LimitDict
                    
def writeData(fileName, finalData, BalanceDict):
    outfile=open(fileName, 'wb')
    output = csv.writer(outfile, dialect = 'excel')
    header = ['Date', 'Instrument ID', 'Last Trade Number', 'Portfolio', 'Counterparty Name', 'Balance', 'Counterparty Credit Limit', 'Counterparty SDS ID', 'New Rate']
    output.writerow(header)
    # Writes the data to file
    LimitDict = getLimitDict(finalData)
    for t in finalData:
        trade = acm.FTrade[t]
        ins = trade.Instrument().Name()
        lastTrade = trade.Oid()
        portfolio = trade.Portfolio().Name()
        counterparty = trade.Counterparty().Name()
        balance = BalanceDict[trade.Name()]
        CP = ael.Party[trade.Counterparty().Name()]
        CPLimit = FCreditLimit.limit_cp(CP)/LimitDict[CP.ptyid].Size()
        CPSDS = trade.Counterparty().AdditionalInfo().BarCap_SMS_CP_SDSID()
        date = calcSpace.CalculateValue(trade, 'PLPeriodEnd')
        rate = getRate(trade)
        output.writerow([date, ins, lastTrade, portfolio, counterparty, balance, CPLimit, CPSDS, rate])
    outfile.close()
