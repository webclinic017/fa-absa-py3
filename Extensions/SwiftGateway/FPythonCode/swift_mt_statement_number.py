
import acm

MT940_STATEMENT_NUMBER_SPEC = 'MT940_StatementNum'
MT535_STATEMENT_NUMBER_SPEC = 'MT535_StatementNum'

def _getTimeSeriesSpec(name):

    spec = acm.FTimeSeriesSpec[name]
    if not spec:
        raise Exception('Could not load Time Series Spec: ' + name)
        
    return spec
    
def _getStatementNumberNewRunNo(specName, object, date):
    timeSeries = acm.FTimeSeries.Select("timeSeriesSpec = '%(spec)s' and recaddr = %(rec)i and day >= '%(day)s'" % 
        {'spec': specName, 'rec': object.Oid(), 'day': date})

    lastRunNo = -1
    for i in timeSeries:
        runNo = i.RunNo()
        if runNo > lastRunNo:
            lastRunNo = runNo
            
    return lastRunNo + 1

def _getStatementNumber(specName, object, date):

    numbers = acm.FTimeSeries.Select("timeSeriesSpec = '%(spec)s' and recaddr = %(rec)i and day >= '%(day)s'" % 
        {'spec': specName, 'rec': object.Oid(), 'day': acm.Time().FirstDayOfYear(date)})
        
    maxNumber = 0
    for number in numbers:
        value = int(number.Value())
        if value > maxNumber:
            maxNumber = value
            
    return maxNumber + 1
    
def _setStatementNumber(specName, object, date, value):

    spec = _getTimeSeriesSpec(specName)
    runNo = _getStatementNumberNewRunNo(specName, object, date)
    
    timeSeries = acm.FTimeSeries()
    timeSeries.TimeSeriesSpec(spec)
    timeSeries.Recaddr(object.Oid())
    timeSeries.Day(date)
    timeSeries.RunNo(runNo)
    timeSeries.Value(value)
    timeSeries.Commit()

def GetMt940StatementNumber(account, date):
    return _getStatementNumber(MT940_STATEMENT_NUMBER_SPEC, account, date)    
    
def SetMt940StatementNumber(account, date, value):
    _setStatementNumber(MT940_STATEMENT_NUMBER_SPEC, account, date, value)

def GetMt535StatementNumber(party, date):
    return _getStatementNumber(MT535_STATEMENT_NUMBER_SPEC, party, date)    
    
def SetMt535StatementNumber(party, date, value):
    _setStatementNumber(MT535_STATEMENT_NUMBER_SPEC, party, date, value)
