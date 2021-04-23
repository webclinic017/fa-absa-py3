'''================================================================================================
================================================================================================'''
import acm
TODAY = acm.Time.DateToday()  
FXBASECALENDAR = acm.UsedValuationParameters().FxBaseCurrency().Calendar()
t = acm.Time
CurrencyPairBucketDict = acm.FDictionary()
CurrencyBucketDict = acm.FDictionary()
'''================================================================================================
Buckets = ['CASH','TODAY','TOM''SPOT''SPOT NEXT''1W''2W''1M''3M''6M''9M''12M''18M''24M''REST']
================================================================================================'''
def GetLastDate(spotDate, spot_holiday_observance, period, calendar1, calendar2):
    date1 = t.AsDate(t.DateTimeAdjustPeriod(spotDate, period, calendar1, 'Mod. Following')) 
    date2 = t.AsDate(t.DateTimeAdjustPeriod(spotDate, period, calendar2, 'Mod. Following'))
    if spot_holiday_observance ==  'Split Via Base':
        date3 = t.AsDate(t.DateTimeAdjustPeriod(spotDate, period, FXBASECALENDAR, 'Mod. Following'))  
        return max(date1, date2, date3)  
    if spot_holiday_observance ==  'Spot Days In Non-Base':
        if calendar1 == FXBASECALENDAR: return date2
        elif calendar2 == FXBASECALENDAR: return date1 
    return max(date1, date2)  
'''================================================================================================
================================================================================================'''
def TimeBucket(trade):
    valueDate = trade.ValueDay()
    if valueDate == TODAY: return 'TODAY'
    if valueDate <= TODAY: return 'CASH'
    currencyPair = trade.CurrencyPair()
    bucketDict = BucketsDict[currencyPair.Name()]
    if valueDate == bucketDict['TOM']: return 'TOM'
    if valueDate == bucketDict['SPOT']: return 'SPOT'
    return 'REST'
'''================================================================================================
================================================================================================'''
def TimeBucket(trade):

    valueDate = trade.ValueDay()
    if valueDate == TODAY: return 'TODAY'
    if valueDate <= TODAY: return 'CASH'
    currencyPair = trade.CurrencyPair()
    
    if currencyPair != None:
        bucketDict = CurrencyPairBucketDict[currencyPair.Name()]
    else:
        bucketDict = CurrencyPairBucketDict[trade.Currency().Name()]

    if valueDate == bucketDict['TOM']: return 'TOM'
    if valueDate == bucketDict['SPOT']: return 'SPOT'
    if valueDate <= bucketDict['SPOT NEXT']: return 'SPOT NEXT'
    if valueDate <= bucketDict['1W']: return '1W'
    if valueDate <= bucketDict['2W']: return '2W'
    if valueDate <= bucketDict['1M']: return '1M'
    if valueDate <= bucketDict['3M']: return '3M'
    if valueDate <= bucketDict['6M']: return '6M'
    if valueDate <= bucketDict['9M']: return '9M'
    if valueDate <= bucketDict['12M']: return '12M'
    if valueDate <= bucketDict['18M']: return '18M'
    if valueDate <= bucketDict['24M']: return '24M'
    return 'REST'
'''================================================================================================
================================================================================================'''
def CacheBuckets():

    for currencyPair in  acm.FCurrencyPair.Select('').SortByProperty('Name'):
        bucketDict = acm.FDictionary()
        spot_holiday_observance = currencyPair.SpotHolidayObservance()
        spotDate = currencyPair.SpotDate(TODAY) 
        calendar1 = currencyPair.Currency1().Calendar()
        calendar2 = currencyPair.Currency2().Calendar()
        bucketDict.AtPut('TOM', GetLastDate(TODAY, spot_holiday_observance, '1D', calendar1, calendar2))
        bucketDict.AtPut('SPOT', spotDate)
        bucketDict.AtPut('SPOT NEXT', GetLastDate(spotDate, spot_holiday_observance, '1D', calendar1, calendar2)) 
        bucketDict.AtPut('1W', GetLastDate(spotDate, spot_holiday_observance, '1W', calendar1, calendar2)) 
        bucketDict.AtPut('2W', GetLastDate(spotDate, spot_holiday_observance, '2W', calendar1, calendar2)) 
        bucketDict.AtPut('1M', GetLastDate(spotDate, spot_holiday_observance, '1M', calendar1, calendar2)) 
        bucketDict.AtPut('3M', GetLastDate(spotDate, spot_holiday_observance, '3M', calendar1, calendar2)) 
        bucketDict.AtPut('6M', GetLastDate(spotDate, spot_holiday_observance, '6M', calendar1, calendar2)) 
        bucketDict.AtPut('9M', GetLastDate(spotDate, spot_holiday_observance, '9M', calendar1, calendar2))
        bucketDict.AtPut('12M', GetLastDate(spotDate, spot_holiday_observance, '12M', calendar1, calendar2)) 
        bucketDict.AtPut('18M', GetLastDate(spotDate, spot_holiday_observance, '18M', calendar1, calendar2))
        bucketDict.AtPut('24M', GetLastDate(spotDate, spot_holiday_observance, '24M', calendar1, calendar2))
        CurrencyPairBucketDict.AtPut(currencyPair.Name(), bucketDict) 

    for currency in acm.FCurrency.Select('').SortByProperty('Name'):
        bucketDict = acm.FDictionary()
        calendar = currency.Calendar()
        spotDays  = calendar.SpotBankingDays()  
        spotDate = calendar.AdjustBankingDays(TODAY, spotDays)
        bucketDict.AtPut('TOM', t.AsDate(t.DateTimeAdjustPeriod(TODAY, '1D', calendar, 'Mod. Following')))
        bucketDict.AtPut('SPOT', spotDate)
        bucketDict.AtPut('SPOT NEXT', t.DateTimeAdjustPeriod(spotDate, '1D', calendar, 'Mod. Following'))
        bucketDict.AtPut('1W', t.DateTimeAdjustPeriod(spotDate, '1W', calendar, 'Mod. Following'))
        bucketDict.AtPut('2W', t.DateTimeAdjustPeriod(spotDate, '2W', calendar, 'Mod. Following'))
        bucketDict.AtPut('1M', t.DateTimeAdjustPeriod(spotDate, '1M', calendar, 'Mod. Following'))
        bucketDict.AtPut('3M', t.DateTimeAdjustPeriod(spotDate, '3M', calendar, 'Mod. Following'))
        bucketDict.AtPut('6M', t.DateTimeAdjustPeriod(spotDate, '6M', calendar, 'Mod. Following'))
        bucketDict.AtPut('9M', t.DateTimeAdjustPeriod(spotDate, '9M', calendar, 'Mod. Following'))
        bucketDict.AtPut('12M', t.DateTimeAdjustPeriod(spotDate, '12M', calendar, 'Mod. Following'))
        bucketDict.AtPut('18M', t.DateTimeAdjustPeriod(spotDate, '18M', calendar, 'Mod. Following'))
        bucketDict.AtPut('24M', t.DateTimeAdjustPeriod(spotDate, '24M', calendar, 'Mod. Following'))
        CurrencyBucketDict.AtPut(currency.Name(), bucketDict) 
        
CacheBuckets()    
'''================================================================================================
================================================================================================'''
