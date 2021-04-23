import acm
import ael
import pyodbc as odbc
JulianDate = '1971-12-31'
PROD = 'JHBPCM05015v05a\FXB_MAIN1_LIVE'
UAT = 'JHBPSM05017\FXB_MAIN1_UAT'
SQLConnection = None
SPACE = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection() 
"""================================================================================================
================================================================================================"""
def LastdayOfMonth(date,businessDays=False,calendar=None):
    date = acm.Time.DateAddDelta(date, 0, -1, 0)
    DaysInMonth = acm.Time.DaysInMonth(date)
    DateDict = acm.Time.DateToYMD(date)
    date = acm.Time.DateFromYMD(DateDict[0], DateDict[1], DaysInMonth)
    if businessDays == True and calendar.IsNonBankingDay(None, None, date) == True:
        date = calendar.AdjustBankingDays( date, -1 )  
    return date  
"""================================================================================================
================================================================================================"""
USD = acm.FCurrency['USD']  
ZAR = acm.FCurrency['ZAR']
CALENDAR = ZAR.Calendar()  
TODAY  = acm.Time.DateNow()
LASTDAYOFPREVMONTH = LastdayOfMonth(TODAY, True, CALENDAR)
FISRTDATOFTHEYEAR = acm.Time.FirstDayOfYear(TODAY)
LASTDAYOFPREVIOUSYEAR = acm.Time.DateAddDelta(FISRTDATOFTHEYEAR, 0, 0, -1)
PREVBUSINESSDAY = CALENDAR.AdjustBankingDays(TODAY, -1)
"""================================================================================================
================================================================================================"""
def midas_dealno(trade):
    if trade.IsFxSwapFarLeg(): trade = trade.FxSwapNearLeg()
    if trade.GroupTrdnbr()!= None: trade = trade.GroupTrdnbr()
    if trade.Trader().Name() == 'STRAUSD':
        if trade.OptionalKey() == '':
            MidasNo = trade.add_info('Source Trade Id')
        else:    
            MidasNo = trade.OptionalKey()
        if len(MidasNo.split('_')) > 1:
            return MidasNo.split('_')[1]    
    else:
        if trade.YourRef() == '':
            if len(trade.OptionalKey().split('|')) > 1:
                optkey = trade.OptionalKey().split('|')[0]
                return optkey[4:10]
        else:
            return trade.YourRef()
    return '' 
"""================================================================================================
================================================================================================"""
def MidasRecon(trade):

    Found = False
    global SQLConnection
    trade_date = acm.Time.DateFromTime(trade.TradeTime())  
    midas_date = acm.Time.DateDifference(trade_date, JulianDate)
    midas_number = midas_dealno(trade)
    
    if SQLConnection == None:
        connectionString = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s' % (PROD, 'MMG_FXF') 
        sqlConnection = odbc.connect(connectionString, autocommit=True) 
        SQLConnection = sqlConnection.cursor() 

    if midas_number != '':
        #check the deals tables
        sql = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM MIDDBLIB/DEALSDB WHERE DLNO = %s AND DDAT = %i UNION SELECT * FROM MIDDBLIB/DEALSDBH WHERE DLNO = %s AND DDAT = %i')"\
        % (midas_number, midas_date, midas_number, midas_date) 
        if len(SQLConnection.execute(sql).fetchall()  ) > 0: Found = True       
              
        #check the shadow tables      
        if Found == False:
            shadow_date = trade_date.replace('_', '')
            sql = "SELECT * FROM OPENQUERY (MIDAS, 'SELECT * FROM PFMIDSHA WHERE SHMDLN = %s AND SHDDAT = %s UNION SELECT * FROM MIDHSLIB/PFMIDSHAH WHERE SHMDLN = %s AND SHDDAT = %s')"\
            % (midas_number, shadow_date, midas_number, shadow_date)
            if len(SQLConnection.execute(sql).fetchall()) > 0: Found = True     

        #check the smalls tables.
        if Found == False:
            sql = "SELECT * FROM OPENQUERY (MIDAS, 'SELECT * FROM PFMIDLIVM WHERE DLNO = %s AND DEALDAT = ''%s''')"  % (midas_number, trade_date)
            if len(SQLConnection.execute(sql).fetchall()) > 0: Found = True     
    
    return Found
"""================================================================================================
================================================================================================"""
def BlotterPosition(portfolio, startDate, endDate, currency):
    global SQLConnection
    if SQLConnection == None:
        connectionString = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s' % (PROD, 'MMG_FXF') 
        sqlConnection = odbc.connect(connectionString, autocommit=True) 
        SQLConnection = sqlConnection.cursor() 
       
    sql = \
    """
    SELECT  
    sum(USD),
    sum(Currency)
    Code
    FROM 
      [MMG_FXF].[dbo].[BlotterHistory],
      [MMG_FXF].[dbo].[Portfolio]
    where
        BookId = 2
    and Active = 1
    and DateCaptured > '%s' 
    and DateCaptured < '%s'	
    and CurrencyCode = '%s'
    and BookId = PortfolioID
    and Code = '%s'
    group by Code
    """ % (startDate, endDate, currency.Name(), portfolio)
    result = SQLConnection.execute(sql).fetchall()
    if len(result) > 0:
        result = result[0]
        return float(result[0]), float(result[1])
    else:
        return 0.00, 0.00
#print BlotterPos('RND','2017-01-04','2017-01-05','EUR')
"""================================================================================================
================================================================================================"""
def GetCorrectSign(trade, currency, usdAmount):
    if trade.Instrument().Name() == currency:
        if trade.Quantity() > 0:return -1*usdAmount 
    else:
        if trade.Quantity() < 0:return -1*usdAmount
    return usdAmount    
"""================================================================================================
Scenarios:
================================================================================================"""
def GetUSDInSplitCurr(trade, posString):

        splitString = posString.split(':')
        currency = splitString[1]
        optionalKey = trade.OptionalKey()
        shadow = optionalKey[0:len(optionalKey)-1] + '%'
        USDTotal = 0.0

        if trade.Acquirer().Name() == 'MIDAS DUAL KEY':
            sqlStr = """
            select
                t.trdnbr
            from
                trade t,
                instrument i
            where 
                i.insaddr = t.insaddr
            and i.instype = 21
            and t.optional_key like '%s'            
            and t.optional_key ~= '%s'      
            and t.prfnbr = '%i'
            and t.value_day = '%s' 
            """ % (shadow, optionalKey, trade.Portfolio().Oid(), trade.ValueDay())
            tradeIds = ael.asql(sqlStr) #[['trdnbr'], [[(74582998,), (74583000,)]]]
            tradeCount = len(tradeIds[1][0])
            if tradeCount > 0: 
                for t in tradeIds[1][0]: 
                    acmTrade = acm.FTrade[t[0]]
                    if acmTrade.CurrencyPair().IncludesCurrency(currency) and acmTrade.CurrencyPair().IncludesCurrency(USD):
                        if acmTrade.Instrument() == USD:
                            USDTotal = USDTotal + acmTrade.Quantity()
                        else:
                            USDTotal = USDTotal + acmTrade.Premium()
        else:
            trades = acm.FTrade.Select('groupTrdnbr = %i' % trade.Oid())
            for t in trades:
                if t.CurrencyPair().IncludesCurrency(USD):
                    return GetCorrectSign(trade, currency, abs(t.Quantity())) if t.Instrument() == USD else GetCorrectSign(trade, currency, abs(t.Premium()))
   
        if USDTotal == 0: 
            if trade.Currency().Name() == currency:
                rate = trade.Currency().Calculation().FXRate(SPACE, USD, TODAY).Value().Number()
                USDTotal = rate * trade.Premium()    
            else:
                rate = trade.Instrument().Calculation().FXRate(SPACE, USD, TODAY).Value().Number()
                USDTotal = rate * trade.Quantity() 

        return USDTotal *-1  
"""================================================================================================
================================================================================================"""
def FXProfitAndLossValues(position, price):
    calcProxy = position.Calculation()
    plDaily = calcProxy.TotalProfitLoss(SPACE, PREVBUSINESSDAY, TODAY, ZAR).Number()
    plMonthly = calcProxy.TotalProfitLoss(SPACE, LASTDAYOFPREVMONTH, TODAY, ZAR).Number()
    plYearly = calcProxy.TotalProfitLoss(SPACE, LASTDAYOFPREVIOUSYEAR, TODAY, ZAR).Number()
    #plTotal = calcProxy.TotalProfitLoss(SPACE,JulianDate,TODAY, ZAR).Number()
    return acm.FArray().AddAll([plDaily, plMonthly, plYearly, 0.00])
"""================================================================================================
================================================================================================"""



