import acm

PointTotal=0.00000001
BaseCurr=acm.UsedValuationParameters().FxBaseCurrency()
CurrPairs=acm.FCurrencyPair.Select('')
for CP in CurrPairs:
    #print CP.Name()
    try:
        CP.PointValueInverse(PointTotal/CP.PointValue())
    except ZeroDivisionError, e:
        print 'Error', e, 'No Point Value set for', CP.Name()
    if CP.Currency1()==BaseCurr or CP.Currency2()==BaseCurr:
        CP.SpotHolidayObservance('Spot Days In Non-Base') # (1)
    else:    
        CP.SpotHolidayObservance('Spot Days In Both') #(3)
    #print CP.SpotHolidayObservance(),CP.PointValueInverse()
    CP.Commit()
