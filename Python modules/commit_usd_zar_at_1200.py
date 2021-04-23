'''
Purpose:                Commit the usd/zar spot rate at 1200 to a time series so that it can be compared
                        icap usd/zar fixing rate in the asql  'USD_ZAR_1200_Nominal_Scaling'
Department and Desk:    FX fwds desk
Requester:              Tafara Dakwa 
Developer:              Anil Parbhoo
CR Number:              CHNG0003503520
Date                    10 March 2016  



'''




import acm

ael_variables = []

def ael_main(dict):

    dt = acm.Time.DateToday()
    i = acm.FCurrency['USD']

    for p in i.Prices():
        if p.Currency().Name()=='ZAR':
            if p.Market().Name() == 'SPOT':
                b = p.Settle()

    tss = acm.FTimeSeriesSpec['USD_ZAR_1200_SAST']
    q = acm.FSQL['USD_ZAR_1200_Nominal_Scaling']
    
    ts = acm.FTimeSeries()
    ts.TimeSeriesSpec(tss)
    ts.Recaddr(q.Oid())
    ts.Day(dt)
    ts.RunNo(1)
    ts.TimeValue(b)
    
    try:
        ts.Commit()
    except:
        print('could not commit the USD-ZAR rate to the time series %s for date %s' % (tss.FieldName(), dt))
        

    
