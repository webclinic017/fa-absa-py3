import acm, ael

def selectTrades():
    #validTradeSystem = ['BARX_TS','FRONT','MUREX', 'BARX_FX_Option']
    validTradeSystem = ['FRONT']
    reportDate = ael.date_today().add_banking_day(ael.Instrument['ZAR'], 1).to_string('%Y-%m-%d')
    excludedTrdnbrs = [29383920, 29378613, 29381287]

    tradesTemp = acm.FTrade.Select('portfolio = VOE')
    trades = []

    for trade in tradesTemp:
        if trade.TradeInstrumentType() == 'Curr' and trade.Status() not in ('Simulated', 'Void') and trade.ValueDay() >= reportDate and trade.TradeSystem() in validTradeSystem and trade.Oid() not in excludedTrdnbrs:
            trades.append(trade)
            
    return trades

#trdNbrList = selectTrades()
#trdNbrList = [acm.FTrade[69831504]]
trdNbrList = [acm.FTrade[82706300],	acm.FTrade[82690393],	acm.FTrade[82690156],	acm.FTrade[82489849],	acm.FTrade[82457738],	acm.FTrade[82375673],	acm.FTrade[82271010],	acm.FTrade[82177250],	acm.FTrade[82175743],	acm.FTrade[82162984],	acm.FTrade[81923517],	acm.FTrade[81754852],	acm.FTrade[81255092],	acm.FTrade[81030644],	acm.FTrade[80977948],	acm.FTrade[80977856],	acm.FTrade[80977691],	acm.FTrade[80977616],	acm.FTrade[80977288],	acm.FTrade[80977060],	acm.FTrade[80976836],	acm.FTrade[80976596],	acm.FTrade[80919213],	acm.FTrade[80915986],	acm.FTrade[80595930],	acm.FTrade[80151445],	acm.FTrade[79461099],	acm.FTrade[79156192],	acm.FTrade[79094133],	acm.FTrade[78742024],	acm.FTrade[78647957],	acm.FTrade[77283181],	acm.FTrade[77179758],	acm.FTrade[77098541],	acm.FTrade[76778548],	acm.FTrade[75193044],	acm.FTrade[74851381],	acm.FTrade[73988971],	acm.FTrade[71951922],	acm.FTrade[71950245],	acm.FTrade[71843923],	acm.FTrade[71346921],	acm.FTrade[71165913]]
nbrOFTrades = len(trdNbrList)
print 'Touching %i trade(s).' %nbrOFTrades

count = 0
for trade in trdNbrList:
    count = count + 1
    trade.Touch()
    try:
        #trade.Portfolio('VOE')
        trade.Status('BO Confirmed')
        trade.Commit()
        pctComplete = count / float(nbrOFTrades) * 100
        print 'Number of trades complete: %i of %i. %i percent complete.' %(count, nbrOFTrades, pctComplete)
    except Exception, e:
        print 'Could not touch trade i%: %s' %(trade.Oid(), str(e))
