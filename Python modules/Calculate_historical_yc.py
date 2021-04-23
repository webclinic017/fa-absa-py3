import ael

def calc_yc(temp, ins, yieldc, nbr, daycount, *rest):
#    ins = ael.Instrument['USD']
    yc = ael.YieldCurve[yieldc]
    hist_date = ael.date_today()
    yc_hist = yc.get_historical_entity(hist_date)
    #print dir(TODAY)
    #print ins.present_value()
    #print ins.present_value(None, None, None, None, None, yc_hist.yield_curve_name)
#    a = 1
#    while a < 10:
    d = hist_date.add_delta(nbr, 0, 0)
    rate = yc_hist.yc_rate(hist_date, d, 'Annual Comp', daycount, 'Spot Rate', None, ins.insid)*100
#    print d, yc.yc_rate(hist_date,d,'Annual Comp',daycount,'Spot Rate',None,ins.insid)*100, rate
#    a = a + 1
    return rate

