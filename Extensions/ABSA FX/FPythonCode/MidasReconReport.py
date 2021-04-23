import acm
import ael
import pyodbc as odbc
'''================================================================================================
Description :


Enhancements:
    * Do date callbacks use TRS code as example
    * Output to file and use directory picker
    * Maybe us insert item rather 
================================================================================================'''
JulianDate      = '1971-12-31'
SQLConnection   = None
PROD            = 'JHBPCM05015v05a\FXB_MAIN1_LIVE'
UAT             = 'JHBPSM05017\FXB_MAIN1_UAT'
'''================================================================================================
================================================================================================'''
def establishSQLConnection():
    global SQLConnection
    if SQLConnection == None:
        connectionString = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s' % (PROD, 'MMG_FXF') 
        sqlConnection = odbc.connect(connectionString, autocommit=True) 
        SQLConnection = sqlConnection.cursor() 
    return SQLConnection
'''================================================================================================
================================================================================================'''
def MidasTradeCheck(midsno, trade):
    
    Found = False
    Date  = acm.Time.DateFromTime(trade.TradeTime())

    resultSet = SQLConnection.execute("SELECT * FROM OPENQUERY (MIDAS, 'SELECT * FROM MIDDBLIB/DEALSDB WHERE DLNO IN (%s) ORDER BY DDAT DESC')"  % midsno).fetchall()   
    for x in resultSet:
        TradeDate = acm.Time.DateAdjustPeriod(JulianDate, str(x[8])+ 'd') 
        if Date == TradeDate:
            Found = True
            
    if Found == False:
        resultSet = SQLConnection.execute("SELECT * FROM OPENQUERY (MIDAS, 'SELECT * FROM MIDDBLIB/DEALSDBH WHERE DLNO IN (%s) ORDER BY DDAT DESC')"  % midsno).fetchall()   
        for x in resultSet:
            TradeDate = acm.Time.DateAdjustPeriod(JulianDate, str(x[8])+ 'd') 
            if Date == TradeDate:
                Found = True     
            
    if Found == False and trade.Status() != "Void":
        print   str(trade.Oid()) + ',' + midsno + ',' + Date + ',' + trade.ValueDay() + ',' +  trade.CurrencyPair().Name() + ',' + str(trade.Quantity()) + ',' + \
                str(trade.Premium()) + ',' +  trade.TimeBucket() + ',' +  trade.Status() + ',' + trade.CreateUser().Name() + ',' + trade.OptionalKey()
'''================================================================================================
================================================================================================'''
def midas_dealno(trade):
    trade = acm.FTrade[trade]
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
'''================================================================================================
================================================================================================'''
def GetAggregationTrades(trade): # passing aggregate trades 
    tradeIds = ael.dbsql("select trdnbr from trade where aggregate_trdnbr = %d" % trade.Oid() )
    for t in tradeIds[0]:
        midasno =  midas_dealno(t[0])
        MidasTradeCheck(midasno, acm.FTrade[t[0]])
        
'''================================================================================================
================================================================================================'''
ael_gui_parameters = {'runButtonLabel': '&&Run',
                      'hideExtraControls': False,
                      'windowCaption': 'Midas Recon Report'}
'''================================================================================================
================================================================================================'''
ael_variables = [
    # Variable          Display name                    Type                    Candidate values                Default                 Mandatory       Multiple        Description          Hook           Enabled
    ('server',          'Server',                       'string',               ['UAT', 'PROD'],                 'UAT',                  1,              0,              ),
    ('tradeType',       'Trade Type',                   'string',               ['Normal', 'FX Aggregate'],      None,                   1,              0,              ),
    ('portfolios',      'Portfolios',                   acm.FPhysicalPortfolio, None,                           None,                   1,              1,              ),
    ('currecnyPairs',   'Currency Pairs',               acm.FCurrencyPair,      None,                           None,                   1,              1,              ),
    ('fromDate',        'From Date',                    'date',                 None,                           '1970-01-01',           1,              0,              ),
    ('toDate',          'To Date',                      'date',                 None,                           acm.Time.DateToday(),   1,              0,              ),
    ('filePath',        'File Path',                    'string',               None,                           'C:/Temp',              1,              0,              ),
    ('openTrade',       'Open Trades in Workbook',      'string',               ['Yes', 'No'],                   'Yes',                  1,              0,              )
    ]
'''================================================================================================
================================================================================================'''
def ael_main(dict):

    server              = dict['server']          
    tradeType           = dict['tradeType']       
    portfolios          = dict['portfolios']      
    currecnyPairs       = dict['currecnyPairs']   
    fromDate            = dict['fromDate'] 
    toDate              = dict['toDate'] 
    filePath            = dict['filePath']       
    openWorkbook        = dict['openTrade']      
    
    Portfolio = 'MIDAS_AGG'
    Currency1 = 'USD'
    Currency2 = 'ZAR'
    
    #currency pair is going to be a problem
    #selStr = 'portfolio in("%s") and type = "%s" and instrument in "%s" and currency = "%s" and tradetime >' % (Portfolio,Type,Currency1,Currency2)
    selStr = "portfolio = '%s' and type = 'FX Aggregate' and tradeTime > '2016-06-01'" % (Portfolio)
    #print acm.FTrade.Select("portfolio = 'MIDAS_RND' and type = 'FX Aggregate'  and instrument = 'USD' and currency = 'ZAR'")

    establishSQLConnection()
    for trade in acm.FTrade.Select(selStr):
        GetAggregationTrades(trade)
    SQLConnection.close()

    if openWorkbook == 'Yes':
        TempPort = acm.FAdhocPortfolio()
        TempPort.Name(trade.Oid())
        [TempPort.Add(acm.FTrade[t[0]]) for t in tradeIds[0]]
        if TempPort.Trades().Size() > 0:     
            tradingMgr = acm.StartApplication('Trading Manager', acm.FTradingSheetTemplate['FX_AggregationView'])
            sheet = tradingMgr.ActiveSheet() #.NewSheet("TradeSheet") #Maybe use existing Trade Sheet or Template
            sheet.InsertObject(TempPort, 0)
         
    
'''================================================================================================
================================================================================================'''
    
    



