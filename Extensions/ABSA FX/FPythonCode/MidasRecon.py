import acm
import pyodbc as odbc

today = acm.Time.DateToday()
PROD = 'AGLFXFRTPRD01.corp.dsarena.com\FXFRT_MAIN1_LIVE'
UAT = 'ZAPRNBMSQL1030.corp.dsarena.com\FXFRT_MAIN1_UAT'
SQLConnection = None
tradeCache = {}
midasCache = {}

sqlSelectFromLive = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLD WHERE CCY = ''%s'' AND DESK = ''%s'' AND PCCY = ''%s'' AND SCCY = ''%s'' AND VALDTEL >= ''%s'' AND VALDTEL <= ''%s''')"

sqlSelectFromHistory = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLDH WHERE CCY = ''%s'' AND DESK = ''%s'' AND PCCY = ''%s'' AND SCCY = ''%s'' AND VALDTEL >= ''%s'' AND VALDTEL <= ''%s''')"

sqlSelectFromHistoryArchive = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLDHA WHERE CCY = ''%s'' AND DESK = ''%s'' AND PCCY = ''%s'' AND SCCY = ''%s'' AND VALDTEL >= ''%s'' AND VALDTEL <= ''%s''')"

sqlSelectFromSuperHistoryArchive = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLDHA WHERE CCY = ''%s'' AND DESK = ''%s'' AND PCCY = ''%s'' AND SCCY = ''%s'' AND VALDTEL >= ''%s'' AND VALDTEL <= ''%s''')"

sqlSelectFromLiveData = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLD WHERE CCY = ''%s'' AND AMT = ''%s'' AND DESK = ''%s'' AND PCCY = ''%s'' AND SCCY = ''%s'' AND VALDTEL >= ''%s'' AND VALDTEL <= ''%s'' AND EXRT = ''%s''')"

sqlSelectFromHistoryData = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLDH WHERE CCY = ''%s'' AND AMT = ''%s'' AND DESK = ''%s'' AND PCCY = ''%s'' AND SCCY = ''%s'' AND VALDTEL >= ''%s'' AND VALDTEL <= ''%s'' AND EXRT = ''%s''')"

sqlSelectFromHistoryArchiveData = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLDHA WHERE CCY = ''%s''  AND AMT = ''%s'' AND DESK = ''%s'' AND PCCY = ''%s'' AND SCCY = ''%s'' AND VALDTEL >= ''%s'' AND VALDTEL <= ''%s'' AND EXRT = ''%s''')"

sqlSelectFromSuperHistoryArchiveData = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLDHA WHERE CCY = ''%s'' AND AMT = ''%s'' AND DESK = ''%s'' AND PCCY = ''%s'' AND SCCY = ''%s'' AND VALDTEL >= ''%s'' AND VALDTEL <= ''%s'' AND EXRT = ''%s''')"


def executeMidasSQL(sql):
    global SQLConnection
    print sql
    return SQLConnection.execute(sql).fetchall()

def getBuySellCurrencies(trade):
    if trade.Quantity() >= 0:
        buyCurr = trade.Instrument().Currency().Name()
        sellCurr = trade.Currency().Name()
        buyAmount = trade.Quantity()
    else:
        buyCurr = trade.Currency().Name()
        sellCurr = trade.Instrument().Currency().Name()
        buyAmount = trade.Premium()
    return buyCurr, sellCurr, buyAmount

def getPortfolio(trade):
    if trade.Portfolio() and trade.Portfolio().Name().__contains__('MIDAS'):
        desk = trade.Portfolio().Name()[6:]
    else:
        desk = trade.Portfolio().Name()
    
    return desk

def updateCache(dataSet, midasId, FATrdnbr):
    global tradeCache
    global midasCache
    
    if len(dataSet) > 0:
        print 'Updatig Cache'
        #Add result to Midas Cache and the specific trade to Front Arena Cache
        for item in dataSet:
            rowMidasId = int(item[7])
            if rowMidasId not in midasCache.keys():
                midasCache[rowMidasId] = item
                if midasId == rowMidasId:
                    #Add specific item to FA Cache
                    print 'Adding Front Arena trade %s linked to Midas trade %s to cache' %(FATrdnbr, midasId)
                    tradeCache[FATrdnbr] = item
            else:
                #Add specific item to FA Cache
                if FATrdnbr not in tradeCache.keys():
                    #Add specific item to FA Cache
                    print 'Adding Front Arena trade %s linked to Midas trade %s to cache' %(FATrdnbr, midasId)
                    tradeCache[FATrdnbr] = item

def getMidasTradeFromData(currency, desk, valueDay, buyCurr, sellCurr, FATrdnbr, amount, rate, potentialMidasId):
    global SQLConnection
    global tradeCache
    global midasCache
    amount = round(amount, 2)
    calendar = acm.FCalendar['ZAR Johannesburg']
    toDate = calendar.AdjustBankingDays(valueDay, 1)
    #toDate = acm.Time.AsDate(acm.Time.DateTimeAdjustPeriod(valueDay, '1d', acm.FCalendar['ZAR Johannesburg'], 0))

    #Check FA Cache
    if FATrdnbr in tradeCache.keys():
        print 'From FA Cache'
        return tradeCache[FATrdnbr]
    
    #Check Midas Cache
    '''if midasId in midasCache.keys():
        print 'From Midas Cache'
        tradeCache[FATrdnbr] = midasCache[midasId]
        return tradeCache[FATrdnbr]
    '''
    
    if valueDay >= today:
        #Select first from Live table
        result = executeMidasSQL(sqlSelectFromLiveData % (currency, amount, desk, buyCurr, sellCurr, valueDay, toDate, rate))
        
        if len(result) == 1:
            midasId = result[0][7]
            updateCache([result[0]], midasId, FATrdnbr)
        elif len(result) > 1:
            found = 0
            for item in result:
                mId = int(item[7])
                if mId == int(potentialMidasId):
                    found = 1
                    updateCache([item], mId, FATrdnbr)
            if found == 0:
                return 'Multiple Midas Results'
        
        if FATrdnbr not in tradeCache.keys():
            #Select from the history table
            
            result = executeMidasSQL(sqlSelectFromHistoryData % (currency, amount, desk, buyCurr, sellCurr, valueDay, toDate, rate))

            if len(result) == 1:
                midasId = result[0][7]
                updateCache([result[0]], midasId, FATrdnbr)
            elif len(result) > 1:
                found = 0
                for item in result:
                    mId = int(item[7])
                    if mId == int(potentialMidasId):
                        found = 1
                        updateCache([item], mId, FATrdnbr)
                if found == 0:
                    return 'Multiple Midas Results'

            if FATrdnbr not in tradeCache.keys():
                #Select from the history archive table
                
                result = executeMidasSQL(sqlSelectFromHistoryArchiveData % (currency, amount, desk, buyCurr, sellCurr, valueDay, toDate, rate))

                if len(result) == 1:
                    midasId = result[0][7]
                    updateCache([result[0]], midasId, FATrdnbr)
                elif len(result) > 1:
                    found = 0
                    for item in result:
                        mId = int(item[7])
                        if mId == int(potentialMidasId):
                            found = 1
                            updateCache([item], mId, FATrdnbr)
                    if found == 0:
                        return 'Multiple Midas Results'
                    
                if FATrdnbr not in tradeCache.keys():
                    #Select from the super history archive table
                    
                    result = executeMidasSQL(sqlSelectFromSuperHistoryArchiveData % (currency, amount, desk, buyCurr, sellCurr, valueDay, toDate, rate))
                    
                    if len(result) == 1:
                        midasId = result[0][7]
                        updateCache([result[0]], midasId, FATrdnbr)
                    elif len(result) > 1:
                        found = 0
                        for item in result:
                            mId = int(item[7])
                            if mId == int(potentialMidasId):
                                found = 1
                                updateCache([item], mId, FATrdnbr)
                        if found == 0:
                            return 'Multiple Midas Results'
    else:
        #Select from the history table
        result = executeMidasSQL(sqlSelectFromHistoryData % (currency, amount, desk, buyCurr, sellCurr, valueDay, toDate, rate))
        
        if len(result) == 1:
            midasId = result[0][7]
            updateCache([result[0]], midasId, FATrdnbr)
        elif len(result) > 1:
            found = 0
            for item in result:
                mId = int(item[7])
                if mId == int(potentialMidasId):
                    found = 1
                    updateCache([item], mId, FATrdnbr)
            if found == 0:
                return 'Multiple Midas Results'
            
        if FATrdnbr not in tradeCache.keys():
            #Select from the history archive table
            result = executeMidasSQL(sqlSelectFromHistoryArchiveData % (currency, amount, desk, buyCurr, sellCurr, valueDay, toDate, rate))
            
            if len(result) == 1:
                midasId = result[0][7]
                updateCache([result[0]], midasId, FATrdnbr)
            elif len(result) > 1:
                found = 0
                for item in result:
                    mId = int(item[7])
                    if mId == int(potentialMidasId):
                        found = 1
                        updateCache([item], mId, FATrdnbr)
                if found == 0:
                    return 'Multiple Midas Results'
                
            if FATrdnbr not in tradeCache.keys():
                #Select from the super history archive table
                
                #result = executeMidasSQL(sqlSelectFromSuperHistoryArchive % (currency, desk, buyCurr, sellCurr, valueDay, toDate))
                result = executeMidasSQL(sqlSelectFromLiveData % (currency, amount, desk, buyCurr, sellCurr, valueDay, toDate, rate))

                if len(result) == 1:
                    midasId = result[0][7]
                    updateCache([result[0]], midasId, FATrdnbr)
                elif len(result) > 1:
                    found = 0
                    for item in result:
                        mId = int(item[7])
                        if mId == int(potentialMidasId):
                            found = 1
                            updateCache([item], mId, FATrdnbr)
                    if found == 0:
                        return 'Multiple Midas Results'
                    
                if FATrdnbr not in tradeCache.keys():
                    #Select first from Live table
                    
                    result = executeMidasSQL(sqlSelectFromSuperHistoryArchiveData % (currency, amount, desk, buyCurr, sellCurr, valueDay, toDate, rate))
                    #result = executeMidasSQL(sqlSelectFromLive % (currency, desk, buyCurr, sellCurr, valueDay, toDate))
                    
                    if len(result) == 1:
                        midasId = result[0][7]
                        updateCache([result[0]], midasId, FATrdnbr)
                    elif len(result) > 1:
                        found = 0
                        for item in result:
                            mId = int(item[7])
                            if mId == int(potentialMidasId):
                                found = 1
                                updateCache([item], mId, FATrdnbr)
                        if found == 0:
                            return 'Multiple Midas Results'
    
    if FATrdnbr in tradeCache.keys():
        return tradeCache[FATrdnbr]
    else:
        return 'No Trade'


def getMidasTrade(midasId, currency, desk, valueDay, buyCurr, sellCurr, FATrdnbr):
    global SQLConnection
    global tradeCache
    global midasCache
    
    calendar = acm.FCalendar['ZAR Johannesburg']
    toDate = calendar.AdjustBankingDays(valueDay, 1)
    #toDate = acm.Time.AsDate(acm.Time.DateTimeAdjustPeriod(valueDay, '1d', acm.FCalendar['ZAR Johannesburg'], 0))
    
    #Check FA Cache
    if FATrdnbr in tradeCache.keys():
        print 'From FA Cache'
        return tradeCache[FATrdnbr]
    
    #Check Midas Cache
    if midasId in midasCache.keys():
        print 'From Midas Cache'
        tradeCache[FATrdnbr] = midasCache[midasId]
        return tradeCache[FATrdnbr]
    
    if valueDay >= today:
        #Select first from Live table
        result = executeMidasSQL(sqlSelectFromLive % (currency, desk, buyCurr, sellCurr, valueDay, toDate))
        
        if len(result) > 0:
            updateCache(result, midasId, FATrdnbr)
        
        if FATrdnbr not in tradeCache.keys():
            #Select from the history table
            
            result = executeMidasSQL(sqlSelectFromHistory % (currency, desk, buyCurr, sellCurr, valueDay, toDate))

            if len(result) > 0:
                updateCache(result, midasId, FATrdnbr)
                
            if FATrdnbr not in tradeCache.keys():
                #Select from the history archive table
                
                result = executeMidasSQL(sqlSelectFromHistoryArchive % (currency, desk, buyCurr, sellCurr, valueDay, toDate))

                if len(result) > 0:
                    updateCache(result, midasId, FATrdnbr)
                    
                if FATrdnbr not in tradeCache.keys():
                    #Select from the super history archive table
                    
                    result = executeMidasSQL(sqlSelectFromSuperHistoryArchive % (currency, desk, buyCurr, sellCurr, valueDay, toDate))
                    
                    if len(result) > 0:
                        updateCache(result, midasId, FATrdnbr)
    else:
        #Select from the history table
        result = executeMidasSQL(sqlSelectFromHistory % (currency, desk, buyCurr, sellCurr, valueDay, toDate))
        if len(result) > 0:
            updateCache(result, midasId, FATrdnbr)
            
        if FATrdnbr not in tradeCache.keys():
            #Select from the history archive table
            
            result = executeMidasSQL(sqlSelectFromHistoryArchive % (currency, desk, buyCurr, sellCurr, valueDay, toDate))

            if len(result) > 0:
                updateCache(result, midasId, FATrdnbr)
                
            if FATrdnbr not in tradeCache.keys():
                #Select from the super history archive table
                
                #result = executeMidasSQL(sqlSelectFromSuperHistoryArchive % (currency, desk, buyCurr, sellCurr, valueDay, toDate))
                result = executeMidasSQL(sqlSelectFromLive % (currency, desk, buyCurr, sellCurr, valueDay, toDate))

                if len(result) > 0:
                    updateCache(result, midasId, FATrdnbr)
                    
                if FATrdnbr not in tradeCache.keys():
                    #Select first from Live table
                    
                    result = executeMidasSQL(sqlSelectFromSuperHistoryArchive % (currency, desk, buyCurr, sellCurr, valueDay, toDate))
                    #result = executeMidasSQL(sqlSelectFromLive % (currency, desk, buyCurr, sellCurr, valueDay, toDate))
                    
                    if len(result) > 0:
                        updateCache(result, midasId, FATrdnbr)
    
    if FATrdnbr in tradeCache.keys():
        return tradeCache[FATrdnbr]
    else:
        return 'No Trade'
    
def MidasRecon(trade):
    print 'Retreiving Midas ID for trade %i' %trade.Oid()
    global SQLConnection
    midas_parent_trdnbr = None
    midas_shadow_trdnbr = None
    search_shadow = False
    tradeSystem = trade.TradeSystem()
    
    if SQLConnection == None:
        connectionString = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s' % (PROD, 'MMG_FXF') 
        sqlConnection = odbc.connect(connectionString, autocommit=True) 
        SQLConnection = sqlConnection.cursor()

    if trade.Type() == 'FX Aggregate':
        return '0_0'

    desk = getPortfolio(trade)
    
    if tradeSystem not in ('FRONT', 'MIDAS CFR'):
        buyCurr, sellCurr, buyAmount = getBuySellCurrencies(trade)

        #Check if Front Arena trade is in FORTRESSPF (Midas Parent Trade)
        sql = "SELECT * FROM OPENQUERY (MIDAS, 'SELECT * FROM FORTRESSPF WHERE FRONTDEALNO = %i ORDER BY DATETIMEADDED DESC')" %trade.Oid()
        result = SQLConnection.execute(sql).fetchall()
        if len(result) > 0:
            midas_parent_trdnbr = int(result[0][1])
            
            result = getMidasTrade(midas_parent_trdnbr, buyCurr, desk, trade.ValueDay(), buyCurr, sellCurr, trade.Oid())

            if len(result) > 0: return '%i_0' %midas_parent_trdnbr
        else:
            search_shadow = True
        
        if search_shadow == True:
            #Fetch Midas ID for 4Front internal trade
            sql = "SELECT * FROM OPENQUERY (MIDAS, 'SELECT sh.MIDASDEALNO, sh.SHADOWDEALNO, sh.FRONTINTERNALNO, MAX(p.DATETIMEADDED) AS DEALDATETIME FROM PFSHADOW4F sh LEFT JOIN FORTRESSPF p ON sh.MIDASDEALNO = p.MIDASDEALNO WHERE sh.FRONTINTERNALNO = %i\
                GROUP BY sh.MIDASDEALNO, sh.SHADOWDEALNO, sh.FRONTINTERNALNO')" %trade.Oid()
            result = SQLConnection.execute(sql).fetchall()
            
            if len(result) > 0:
                midas_parent_trdnbr = (result[0][0])
                midas_shadow_trdnbr = (result[0][1])
                
                result = getMidasTrade(midas_shadow_trdnbr, buyCurr, desk, trade.ValueDay(), buyCurr, sellCurr, trade.Oid())
            
                if len(result) > 0: return '%i_%i' %(midas_parent_trdnbr, midas_shadow_trdnbr)
            
            else:
                if trade.YourRef():
                    #result = getMidasTrade(int(trade.YourRef()), buyCurr, desk, trade.ValueDay(), buyCurr, sellCurr, trade.Oid())
                    
                    #if len(result) > 0: 
                    #    return '%i_0' %int(trade.YourRef())
                    #else:
                    midasData = getMidasTradeFromData(buyCurr, desk, trade.ValueDay(), buyCurr, sellCurr, trade.Oid(), buyAmount, round(trade.Price(), 8), trade.YourRef())
                    
                    if len(midasData) > 0:
                        if midasData == 'Multiple Midas Results':
                            return midasData
                        else:
                            return '%s_0' %midasData[7]
                else:
                    return '0_0'
            
    elif tradeSystem == 'MIDAS CFR':
        if trade.Status() == 'Void':
            return trade.OptionalKey()[14:]
        else:
            return trade.OptionalKey()[9:]
    else:
        return '0_0'

def MidasStatus(trade):
    midasStatus = ''
    midasTradeNbr = MidasRecon(trade)
    midasIds = midasTradeNbr.split('_')
    buyCurr, sellCurr, buyAmount = getBuySellCurrencies(trade)
    portfolio = getPortfolio(trade)
    
    if midasIds[0] == 'Multiple Midas Results':
        return midasIds[0]
    
    if midasIds[0] != '0' and midasIds[1] == '0':
        midasTrade = getMidasTrade(int(midasIds[0]), buyCurr, portfolio, trade.ValueDay(), buyCurr, sellCurr, trade.Oid())
    elif midasIds[0] != '0' and midasIds[1] != '0':
        midasTrade = getMidasTrade(int(midasIds[1]), buyCurr, portfolio, trade.ValueDay(), buyCurr, sellCurr, trade.Oid())
    else:
        midasTrade = []
        
    if len(midasTrade) > 0:
        midasStatus = midasTrade[3]
    
    return midasStatus.encode("ascii")
        
#print MidasRecon(acm.FTrade[64732591])
#print MidasStatus(acm.FTrade[79303163])
