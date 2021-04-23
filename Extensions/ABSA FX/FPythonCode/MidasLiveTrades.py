import acm
import pyodbc as odbc
today = acm.Time.DateToday()
PROD = 'AGLFXFRTPRD01.corp.dsarena.com\FXFRT_MAIN1_LIVE'
UAT = 'ZAPRNBMSQL1030.corp.dsarena.com\FXFRT_MAIN1_UAT'
SQLConnection = None
isProd = True

if acm.FDhDatabase['ADM'].InstanceName() != 'Production':
    isProd = False

def sumCurrencyAmounts(data, currency, currPosition, amountPosition):
    total = 0
    for item in data:
        if item[currPosition] == currency:
            total = total + float(item[amountPosition])
    return total

def sumCurrencyPairAmounts(data, currency, currency1, currency2, currencyColumnNumber, amountColumnNumber, purchaseCurrencyNumber, saleCurrencyNumber):
    total = 0
    
    if currency not in (currency1, currency2):
        return total
    
    for item in data:
        if item[currencyColumnNumber] == currency and  (currency1 in (item[purchaseCurrencyNumber], item[saleCurrencyNumber]) and (currency2 in (item[purchaseCurrencyNumber], item[saleCurrencyNumber]))):
            total = total + float(item[amountColumnNumber])
    return total

def sumCurrencySplitAmounts(data, currency, currSplit, purchaseCurrPosition, purchaseAmountPosition, saleCurrPosition, saleAmountPosition):
    total = 0
    
    if currency != currSplit:
        return total
    
    for item in data:
        if item[purchaseCurrPosition] == currSplit:
            total = total + item[purchaseAmountPosition]
        elif item[saleCurrPosition] == currSplit:
            total = total - item[saleAmountPosition]
    return total
    

def midasPositionPerPortfolioData(portfolio, profitAndLossDisplayDateEnd):
    global SQLConnection
    endDate = profitAndLossDisplayDateEnd.to_string('%Y-%m-%d')
    if SQLConnection == None:
        connectionString = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s' % (PROD, 'MMG_FXF') 
        sqlConnection = odbc.connect(connectionString, autocommit=True) 
        SQLConnection = sqlConnection.cursor()
    
    if isProd:
        #Select Midas trades for the portfolio and date
        sql = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLD WHERE DESK = '%s' AND VALDTEL >= ''%s'' AND MLID != ''REV'' AND MLID != ''R''')"\
        %(portfolio, endDate)
        print sql
        result = SQLConnection.execute(sql).fetchall()

        #Select Midas trades for the portfolio and date from the history DB
        sql = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLDH WHERE DESK = '%s' AND VALDTEL >= ''%s'' AND MLID != ''REV'' AND MLID != ''R''')"\
        %(portfolio, endDate)
        print sql
        result += SQLConnection.execute(sql).fetchall()
    else:
        #Select Midas trades for the portfolio and date
        sql = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLD WHERE DESK = '%s' AND VALDTEL >= ''%s'' AND MLID != ''REV'' AND MLID != ''R'' AND TDATEL != ''%s''')"\
        %(portfolio, endDate, today)
        print sql
        result = SQLConnection.execute(sql).fetchall()

        #Select Midas trades for the portfolio and date from the history DB
        sql = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM PFMIDMLDH WHERE DESK = '%s' AND VALDTEL >= ''%s'' AND MLID != ''REV'' AND MLID != ''R'' AND TDATEL != ''%s''')"\
        %(portfolio, endDate, today)
        print sql
        result += SQLConnection.execute(sql).fetchall()

    return result

def midasPositionPerCurrencyValues(dataSet, currencies):
    resultList = []
    currPosition = 2
    amountPosition = 4
    for curr in currencies:
        total = 0
        currency = curr.Name()
        total = sumCurrencyAmounts(dataSet, currency, currPosition, amountPosition)
        resultList.append(acm.DenominatedValue(total, curr, None))
    
    return resultList

def midasPositionPerCurrencyInstrumentValues(currPair, dataSet, currencies):
    currencyColumnNumber = 2
    amountColumnNumber = 4
    purchaseCurrencyNumber = 10
    saleCurrencyNumber = 11
    resultList = []
    
    try:
        curr1, curr2 = currPair.AsString().replace("'", '').split('/')
    except:
        curr1, curr2 = None, None
    
    for curr in currencies:
        if not curr1 or not curr2:
            resultList.append(acm.DenominatedValue(0, curr, None))
        else:
            currency = curr.Name()
            value = sumCurrencyPairAmounts(dataSet, currency, curr1, curr2, currencyColumnNumber, amountColumnNumber, purchaseCurrencyNumber, saleCurrencyNumber)
            resultList.append(acm.DenominatedValue(value, curr, None))
    
    return resultList

def midasPositionPerCurrencySplitValues(currSplit, dataSet, currencies):
    purchaseColumnNumber = 0
    purchaseAmountColumnNumber = 1
    saleColumnNumber = 2
    saleAmountColumnNumber = 3
    resultList = []
    
    currSplit = currSplit.AsString().replace("'", '')
    
    for curr in currencies:
        currency = curr.Name()
        value = sumCurrencySplitAmounts(dataSet, currency, currSplit, purchaseColumnNumber, purchaseAmountColumnNumber, saleColumnNumber, saleAmountColumnNumber)
        resultList.append(acm.DenominatedValue(float(value / 100), curr, None))
    
    return resultList

def sumFAPositions(tradesInPosition, date, currency):
    total = 0
    for trade in tradesInPosition:
        if trade.status not in ('Void', 'Simulated'):
            if trade.value_day >= date:
                if trade.curr.insid == currency.Name():
                    total += trade.premium
                elif trade.insaddr.curr.insid == currency.Name():
                    total += trade.quantity
    return total

def FA_LivePositionPerCurrency(tradesInPosition, date, currencies):
    resultList = []
    for curr in currencies:
        total = sumFAPositions(tradesInPosition, date, curr)
        resultList.append(acm.DenominatedValue(total, curr, None))
        
    return resultList

#dataSet = midasPositionPerCurrencyData("'BBM'", [acm.FCurrency['AUD'], acm.FCurrency['GBP']])
#print dataSet
#print midasPositionPerCurrencyInstrumentValues('AUD/JPY', dataSet, [acm.FCurrency['AUD']])
#print midasPositionPerCurrencyValues(dataSet, [acm.FCurrency['AUD'], acm.FCurrency['GBP']])
