import acm

print 'Script started...'
try:
    date = acm.Time().DateFromYMD(2011, 04, 15)
    zar_calendar = acm.FCalendar['ZAR Johannesburg']
    instruments = acm.FSecurityLoan.Select('')
    counter = 0
    for instrument in instruments:
        for leg in instrument.Legs():
            if not leg.PayCalendar() and instrument.AdditionalInfo().SL_SweepingBatchNo() and instrument.ExpiryDate() >= date:
                leg.PayCalendar(zar_calendar)
                leg.Commit()
                print 'Processing', instrument.Name()
                counter += 1
except Exception, ex:
    print 'Error: The following exception occurred:', str(ex)
else:
    print 'Success:', counter, 'legs updated'
