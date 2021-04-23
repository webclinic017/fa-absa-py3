import acm
import pyodbc as odbc
JulianDate = '1971-12-31'
PROD = 'AGLFXFRTPRD01.corp.dsarena.com\FXFRT_MAIN1_LIVE'
UAT = 'ZAPRNBMSQL1030.corp.dsarena.com\FXFRT_MAIN1_UAT'
SQLConnection = None

def sumCurrencyAmounts(data, currency, purchaseCurrPosition, purchaseAmountPosition, saleCurrPosition, saleAmountPosition):
    total = 0
    for item in data:
        if item[purchaseCurrPosition] == currency:
            total = total + item[purchaseAmountPosition]
        elif item[saleCurrPosition] == currency:
            total = total - item[saleAmountPosition]
    return total

def sumCurrencyPairAmounts(data, currency, currency1, currency2, purchaseCurrPosition, purchaseAmountPosition, saleCurrPosition, saleAmountPosition):
    total = 0
    
    if currency not in (currency1, currency2):
        return total
    
    for item in data:
        if item[purchaseCurrPosition] in (currency1, currency2) and item[saleCurrPosition] in (currency1, currency2):
            if item[purchaseCurrPosition] == currency:
                total = total + item[purchaseAmountPosition]
            elif item[saleCurrPosition] == currency:
                total = total - item[saleAmountPosition]
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
    

def midasPositionPerCurrencyData(portfolio, currencies, profitAndLossDisplayDateEnd):
    global SQLConnection
    result = []
    #endDate = acm.Time.DateToday()
    endDate = profitAndLossDisplayDateEnd
    midas_date = acm.Time.DateDifference(endDate, JulianDate)
    
    if SQLConnection == None:
        connectionString = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s' % (PROD, 'MMG_FXF') 
        sqlConnection = odbc.connect(connectionString, autocommit=True) 
        SQLConnection = sqlConnection.cursor()

    #Select Midas Cash for the selected currencies.
    for currency in currencies:
        curr = currency.Name()
        sql = "SELECT * FROM OPENQUERY (MIDAS,'SELECT * FROM MIDDBLIB/PFMIDDKC WHERE DCDESK = '%s' AND DCRUND = %i AND DCCCY = ''%s''')"\
        %(portfolio, midas_date, curr)
        print sql
        result += SQLConnection.execute(sql).fetchall()
        
    return result

def midasPositionPerCurrencyValues(dataSet, currencies):
    resultList = []
    
    for curr in currencies:
        currency = curr.Name()
        for data in dataSet:
            if data[1] == currency:
                resultList.append(acm.DenominatedValue(float(data[2]), curr, None))
    
    return resultList

def midasPositionPerCurrencyInstrumentValues(currPair, dataSet, currencies):
    purchaseColumnNumber = 0
    purchaseAmountColumnNumber = 1
    saleColumnNumber = 2
    saleAmountColumnNumber = 3
    resultList = []
    
    curr1, curr2 = currPair.AsString().replace("'", '').split('/')
    
    for curr in currencies:
        currency = curr.Name()
        value = sumCurrencyPairAmounts(dataSet, currency, curr1, curr2, purchaseColumnNumber, purchaseAmountColumnNumber, saleColumnNumber, saleAmountColumnNumber)
        resultList.append(acm.DenominatedValue(float(value / 100), curr, None))
    
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

#dataSet = midasPositionPerCurrencyData("'BBM'", [acm.FCurrency['AUD'], acm.FCurrency['GBP']])
#print dataSet
#print midasPositionPerCurrencyInstrumentValues('AUD/JPY', dataSet, [acm.FCurrency['AUD']])
#print midasPositionPerCurrencyValues(dataSet, [acm.FCurrency['AUD'], acm.FCurrency['GBP']])
