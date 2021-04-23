import pyodbc as odbc
import acm, re
from MidasTrade import MidasTrade

global midasTradeLookup
midasTradeLookup = None

class MidasTradeLookup():
    def __init__(self):
        self.__internalMidasCache = {}
        self.__midasCache = {}
        self.__SQLConnection = None
        self.__setSQLConnection()
    
    def getBuySellDetails(self, trade):
        if trade.Quantity() >= 0:
            buyCurrency = trade.Instrument().Name()
            buyAmount = round(trade.Quantity(), 2)
            sellCurrency = trade.Currency().Name()
            sellAmount = round(trade.Premium(), 2)
        else:
            buyCurrency = trade.Currency().Name()
            buyAmount = round(trade.Premium(), 2)
            sellCurrency = trade.Instrument().Name()
            sellAmount = round(trade.Quantity(), 2)
        
        return buyCurrency, buyAmount, sellCurrency, sellAmount
    
    def __getMidasPortfolio(self, fPortfolio):
        if fPortfolio:
            if fPortfolio.Name().__contains__('MIDAS_'):
                return fPortfolio.Name()[6:]
            elif fPortfolio.Name() == 'Africa_Curr':
                return 'AFC'
            elif fPortfolio.Name() == 'JN_FXOptions':
                return 'JNS'
            elif fPortfolio.Name() in ('LTnonzar', 'LTNZ_4Front'):
                return 'LTN'
            elif fPortfolio.Name() in ('BTB Trades', 'BTB_Exotics', 'BVOE', 'G7OE', 'Mauritius_BTB', 'ABVOE4F'):
                return 'VOE'
            else:
                return fPortfolio.Name()
        else:
            return None
    
    def __setSQLConnection(self):
        if self.__SQLConnection == None:
            connectionString = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s' % ('AGLFXFRTPRD01.corp.dsarena.com\FXFRT_MAIN1_LIVE', 'MMG_FXF') 
            sqlConnection = odbc.connect(connectionString, autocommit=True) 
            self.__SQLConnection = sqlConnection.cursor()
    
    def __executeMidasSQL(self, sql):
        print sql
        return self.__SQLConnection.execute(sql).fetchall()

    def __addBusinessDay(self, date):
        calendar = acm.FCalendar['ZAR Johannesburg']
        return calendar.AdjustBankingDays(date, 5)

    def __addMidasResultToInternalMidasCache(self, midasResults, valueDay):
        if len(midasResults) >= 1:
            for result in midasResults:
                midasDealNo = result[7]
                midasValueDate = result[9]
                if valueDay < midasValueDate:
                    key = '%s_%s' %(midasDealNo, valueDay)
                else:
                    key = '%s_%s' %(midasDealNo, midasValueDate)
                if key not in self.__internalMidasCache.keys():
                    self.__internalMidasCache[key] = result

    def __addMidasTradeToMidasCache(self, FATrdnbr, lookupKey):
            if FATrdnbr not in self.__midasCache.keys():
                if lookupKey in self.__internalMidasCache.keys():
                    midasTrade = MidasTrade()
                    midasTradeFromCache = self.__internalMidasCache[lookupKey]
                    midasTrade.dealNo = midasTradeFromCache[7]
                    midasTrade.status = midasTradeFromCache[3]
                    midasTrade.rate = midasTradeFromCache[12]
                    midasTrade.buyAmount = midasTradeFromCache[15]
                    midasTrade.buyCurrency = midasTradeFromCache[10]
                    midasTrade.sellAmount = -1*midasTradeFromCache[16]
                    midasTrade.sellCurrency = midasTradeFromCache[11]
                    midasTrade.desk = midasTradeFromCache[22]
                    self.__midasCache[FATrdnbr] = midasTrade
        

    def __getMidasTradeFromValueDateAndNumber(self, trade, midasDealNo, desk):
        sqlSelectFromLiveData = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLD WHERE VALDTEL >= ''%s'' AND VALDTEL <= ''%s'' AND DESK = ''%s''')"

        sqlSelectFromHistoryData = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLDH WHERE VALDTEL >= ''%s'' AND VALDTEL <= ''%s'' AND DESK = ''%s''')"

        sqlSelectFromHistoryArchiveData = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLDHA WHERE VALDTEL >= ''%s'' AND VALDTEL <= ''%s'' AND DESK = ''%s''')"

        valueDate = trade.ValueDay()
        nextDayFromValueDay = self.__addBusinessDay(valueDate)

        lookupKey = '%s_%s' %(midasDealNo, valueDate)
        
        if lookupKey not in self.__internalMidasCache.keys():
            #Check Live Table
            results = self.__executeMidasSQL(sqlSelectFromLiveData % (valueDate, nextDayFromValueDay, desk))
            if len(results) >= 1:
                self.__addMidasResultToInternalMidasCache(results, valueDate)
        
        if lookupKey not in self.__internalMidasCache.keys():
            #Check History Table
            results = self.__executeMidasSQL(sqlSelectFromHistoryData % (valueDate, nextDayFromValueDay, desk))
            if len(results) >= 1:
                self.__addMidasResultToInternalMidasCache(results, valueDate)

        if lookupKey not in self.__internalMidasCache.keys():
            #Check History Archive Table
            results = self.__executeMidasSQL(sqlSelectFromHistoryArchiveData % (valueDate, nextDayFromValueDay, desk))
            if len(results) >= 1:
                self.__addMidasResultToInternalMidasCache(results, valueDate)

        self.__addMidasTradeToMidasCache(trade.Oid(), lookupKey)

    def __get4FrontTradeInMidasMappingTable(self, trade):
        if trade.Oid() not in self.__midasCache.keys():
            #Check if Front Arena trade is in FORTRESSPF (Midas Parent Trade)
            sql = "SELECT * FROM OPENQUERY (MIDAS, 'SELECT * FROM FORTRESSPF WHERE FRONTDEALNO = %i ORDER BY DATETIMEADDED DESC')" %trade.Oid()
            result = self.__executeMidasSQL(sql)
            if len(result) >= 1:
                midas_parent_trdnbr = int(result[0][1])
                if trade.Portfolio():
                    midasPortfolio = self.__getMidasPortfolio(trade.Portfolio())
                    self.__getMidasTradeFromValueDateAndNumber(trade, midas_parent_trdnbr, midasPortfolio)
        
        if trade.Oid() not in self.__midasCache.keys():
            #Fetch Midas ID for 4Front internal trade
            sql = "SELECT * FROM OPENQUERY (MIDAS, 'SELECT sh.MIDASDEALNO, sh.SHADOWDEALNO, sh.FRONTINTERNALNO, MAX(p.DATETIMEADDED) AS DEALDATETIME FROM PFSHADOW4F sh LEFT JOIN FORTRESSPF p ON sh.MIDASDEALNO = p.MIDASDEALNO WHERE sh.FRONTINTERNALNO = %i\
                GROUP BY sh.MIDASDEALNO, sh.SHADOWDEALNO, sh.FRONTINTERNALNO')" %trade.Oid()
            result = self.__executeMidasSQL(sql)
            
            if len(result) == 1:
                midas_parent_trdnbr = (result[0][0])
                midas_shadow_trdnbr = (result[0][1])
                if trade.Portfolio():
                    midasPortfolio = self.__getMidasPortfolio(trade.Portfolio())
                    self.__getMidasTradeFromValueDateAndNumber(trade, midas_shadow_trdnbr, midasPortfolio)
        
        if trade.Oid() in self.__midasCache.keys():
            return True
        return False

    def __getCFRTrade(self, trade):
        if trade.Portfolio() and trade.Portfolio().Name().__contains__('MIDAS_'):
            if trade.Instrument() == trade.Currency():
                return False
            else:
                if re.match('[0-9]+_[0-9]+_[0-9]+', trade.OptionalKey()) or re.match('[A-Z]+_[0-9]+_[0-9]+_[0-9]+', trade.OptionalKey()):
                    if trade.Oid() not in self.__midasCache.keys():
                        optionalKeySplit = trade.OptionalKey().split('_')
                        if optionalKeySplit[len(optionalKeySplit) - 1] == '0':
                            midasId = optionalKeySplit[len(optionalKeySplit) - 2]
                        else:
                            midasId = optionalKeySplit[len(optionalKeySplit) - 1]
                        midasPortfolio = self.__getMidasPortfolio(trade.Portfolio())
                        self.__getMidasTradeFromValueDateAndNumber(trade, midasId, midasPortfolio)
                        
                    if trade.Oid() in self.__midasCache.keys():
                        return True
        return False

    def __getFrontTradesBasedOnYourRef(self, trade):
        if not trade.YourRef():
            return False
        
        if trade.Status() == 'Internal' and trade.GroupTrdnbr() != None:
            return False
        
        if trade.Portfolio():
            midasPortfolio = self.__getMidasPortfolio(trade.Portfolio())
            self.__getMidasTradeFromValueDateAndNumber(trade, trade.YourRef(), midasPortfolio)
        
            if trade.Oid() in self.__midasCache.keys():
                return True

        return False

    def __getTradesBasedOnEconomics(self, trade):
        for entry in self.__internalMidasCache.items():
            value = entry[1]
            
            rate = round(trade.Price(), 8)
            if trade.Portfolio() and trade.Portfolio().Name().__contains__('MIDAS_'):
                portfolio = trade.Portfolio().Name()[6:]
            else:
                portfolio = trade.Portfolio().Name()
                
            buyCurrency, buyAmount, sellCurrency, sellAmount = self.getBuySellDetails(trade)
            
            midasRate = round(value[12], 2)
            midasBuyCurrency = str(value[10])
            midasBuyAmount = round(value[15], 2)
            midasSellCurrency = str(value[11])
            midasSellAmount = round(-1*value[16], 2)
            midasDesk = str(value[22])
            
            if midasDesk == portfolio and midasRate == rate and midasBuyCurrency == buyCurrency and midasBuyAmount == buyAmount and midasSellCurrency == sellCurrency and midasSellAmount == sellAmount:
                self.__addMidasTradeToMidasCache(trade.Oid(), entry[0])
                return True
        return False

    def getMidasTrade(self, trade):
        useDefault = False
        
        if trade.Portfolio():
            if (not trade.Portfolio().Name().__contains__('MIDAS_')) and (not trade.Portfolio().AdditionalInfo().MidasSettleEnabled()):
                useDefault = True
        else:
            useDefault = True
        
        if trade.Instrument().InsType() != 'Curr':
            useDefault = True
            
        if trade.Status() == 'Simulated':
            useDefault = True
        
        if trade.Type() in ('Aggregate', 'FX Aggregate'):
            useDefault = True
        
        if useDefault == False:
            if trade.Oid() not in self.__midasCache.keys():
                if not self.__getCFRTrade(trade):
                    if not self.__get4FrontTradeInMidasMappingTable(trade):
                        if trade.YourRef():
                            if not self.__getFrontTradesBasedOnYourRef(trade):
                                useDefault = True
                        else:
                            if not self.__getTradesBasedOnEconomics(trade):
                                useDefault = True
        
        if useDefault == True:
            defaultMidasTrade = MidasTrade()
            self.__midasCache[trade.Oid()] = defaultMidasTrade

        return self.__midasCache[trade.Oid()]

if midasTradeLookup == None:
    midasTradeLookup = MidasTradeLookup()

def getMidasDealNo(trade):
    global midasTradeLookup
    midasTrade = midasTradeLookup.getMidasTrade(trade)
    return str(midasTrade.dealNo)

def getMidasStatus(trade):
    global midasTradeLookup
    midasTrade = midasTradeLookup.getMidasTrade(trade)
    return str(midasTrade.status)

def getMidasRate(trade):
    global midasTradeLookup
    midasTrade = midasTradeLookup.getMidasTrade(trade)
    return str(midasTrade.rate)

def getMidasBuyAmount(trade):
    global midasTradeLookup
    midasTrade = midasTradeLookup.getMidasTrade(trade)
    return str(midasTrade.buyAmount)

def getMidasBuyCurrency(trade):
    global midasTradeLookup
    midasTrade = midasTradeLookup.getMidasTrade(trade)
    return str(midasTrade.buyCurrency)

def getMidasSellAmount(trade):
    global midasTradeLookup
    midasTrade = midasTradeLookup.getMidasTrade(trade)
    return str(midasTrade.sellAmount)

def getMidasSellCurrency(trade):
    global midasTradeLookup
    midasTrade = midasTradeLookup.getMidasTrade(trade)
    return str(midasTrade.sellCurrency)

def getMidasDesk(trade):
    global midasTradeLookup
    midasTrade = midasTradeLookup.getMidasTrade(trade)
    return str(midasTrade.desk)

def getMidasRateBreak(trade):
    midasRate = getMidasRate(trade)
    if midasRate == 'None':
        return midasRate
    else:
        return str(round(trade.Price(), 8) - round(float(midasRate), 8))

def getMidasStatusBreak(trade):
    midasStatus = getMidasStatus(trade)
    
    if midasStatus == 'None':
        return midasStatus
    elif midasStatus == 'REV' and trade.Status() != 'Void':
        return 'Break'
    elif midasStatus != 'REV' and trade.Status() == 'Void':
        return 'Break'
    return 'Match'

def getMidasBuyAmountBreak(trade):
    midasBuyAmount = getMidasBuyAmount(trade)
    
    if midasBuyAmount == 'None':
        return midasBuyAmount
    else:
        buyCurrency, buyAmount, sellCurrency, sellAmount = midasTradeLookup.getBuySellDetails(trade)
        
        return str(round(buyAmount - float(midasBuyAmount), 2))
    
def getMidasBuyCurrencyBreak(trade):
    midasBuyCurrency = getMidasBuyCurrency(trade)
    
    if midasBuyCurrency == 'None':
        return midasBuyCurrency
    else:
        buyCurrency, buyAmount, sellCurrency, sellAmount = midasTradeLookup.getBuySellDetails(trade)
        
        if buyCurrency == midasBuyCurrency:
            return 'Match'
        else:
            return 'Break'
    
def getMidasSellAmountBreak(trade):
    midasSellAmount = getMidasSellAmount(trade)
    if midasSellAmount == 'None':
        return midasSellAmount
    else:
        buyCurrency, buyAmount, sellCurrency, sellAmount = midasTradeLookup.getBuySellDetails(trade)
        
        return str(round(sellAmount - float(midasSellAmount), 2))

def getMidasSellCurrencyBreak(trade):
    midasSellCurrency = getMidasSellCurrency(trade)
    if midasSellCurrency == 'None':
        return midasSellCurrency
    else:
        buyCurrency, buyAmount, sellCurrency, sellAmount = midasTradeLookup.getBuySellDetails(trade)
        
        if sellCurrency == midasSellCurrency:
            return 'Match'
        else:
            return 'Break'
