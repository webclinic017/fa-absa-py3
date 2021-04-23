import pyodbc as odbc
import ael
import pprint
import datetime, time
from FC_PARAMETERS_GENERIC import FC_PARAMETERS_GENERIC as parameters

ael_variables = [['reportDate', 'Report Date', 'string', '', '', 0, 0, 'Report date for trades.', None, 1]]

def ael_main(dict):
    if not dict['reportDate']:
        dict['reportDate'] = getTradeCreateTime()
    print dict['reportDate']
    getTradeCount(dict['reportDate'])

def getTradeCreateTime():
    from FC_PARAMETERS_ENVIRONMENT import FC_PARAMETERS_ENVIRONMENT as PARAMETERS_ENVIRONMENT
    eod_cutoffTime = str(PARAMETERS_ENVIRONMENT.environment.getElementsByTagName('GENERIC_PARAMETERS')[0].getElementsByTagName('TradeEODCreateCutOffTime')[0].firstChild.data)
    reportDate = time.strftime("%Y-%m-%d")
    trade_create_time = '%s %s' %(reportDate, eod_cutoffTime)
    return trade_create_time

def getTradeCount(cutOffTime):
    initialCatalog='FCACHE'
    dataSource = 'JHBDSM050000016\FCACHE_MAIN1_DEV'
    connectionString = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s' % (dataSource, initialCatalog)
    sqlConnection = odbc.connect(connectionString, autocommit=True)
    cursor = sqlConnection.cursor()

    selection = ael.asql(r'''
        select prfnbr,count(trdnbr)
        from trade t
        where t.status not in (1,7) and t.creat_time < '%s'
        group by 1
        ''' %cutOffTime)

    selection.sort()

    i = len(selection[0][0])

    l = selection[0][0]

    for j in range(i):
        BookID = l[j][0]
        TradeCount = l[j][1]
        ReportDate = cutOffTime[:10]
        
        sql = '''
        INSERT INTO FrontCache.PortfolioTradeCount
        (BookID, TradeCount, dbTimeStamp)
        VALUES('%s', '%s', GETDATE())
        ''' %(BookID, TradeCount)
        
        #print sql
        
        cursor.execute(sql)
    print 'Inserted %s rows successfully' %i
