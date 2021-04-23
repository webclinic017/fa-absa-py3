import ael
 
def change_div(temp,series_name,cashIns,divIns, *rest):
    sp =  ael.TimeSeriesSpec[series_name].specnbr
    times = ael.TimeSeries.select('ts_specnbr = %s' %sp)
    for ts in times:
        if ts.day == ael.date_today().add_days(-1):
            yesterday = ts.value
            run_no = ts.run_no
       
    cash = 0
    divIns = ael.Instrument[divIns]
    for l in divIns.legs():
        for c in l.cash_flows():
            if c.pay_day == ael.date_today():
                cash = round(cash + c.fixed_amount, 2)
        
    rate = ael.Instrument['ZAR-JIBAR-ON-DEP']
    price = rate.used_price(ael.date_today().add_days(-1), 'ZAR')
 
    value = round(yesterday * (1 + (price/100)*(1/365.00)) + cash, 2)
    cashIns = ael.Instrument[cashIns]
    
    ts_specnbr = ael.TimeSeriesSpec[series_name]
    ts = ael.TimeSeries.new() 
    ts.recaddr = cashIns.insaddr
    ts.ts_specnbr = ts_specnbr.specnbr
    ts.day = ael.date_today()
    ts.run_no = run_no + 1
    ts.value = value
    ts.commit()
    ael.poll()
    
    return 'Success'
