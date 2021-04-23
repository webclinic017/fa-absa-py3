'''
Purpose                 :Daily report to get daily rates for specified curve writen to a file
Department and Desk     :Group Treasury
Requester:              :Coen de Beer
Developer               :Jaysen Naicker
Date			:02/07/2010
CR Number               :362029
'''

import acm


'''
    Get curve info
'''
def get_ircurveinfo(yc, ins):
    valday = acm.Time.DateToday()
    if yc.Category() not in ('AttributeSpreadCurve', 'InstrumentSpreadCurve', 'InstrumentSpreadCurveBidAsk', 'SpreadCurve'):
        return yc.IrCurveInformation(valday)
    elif yc.Category() == 'AttributeSpreadCurve':
        if not ins:
            return
        if yc.AttributeType() == 'Currency':
            if ins.Category() == 'Currency':
                curr = ins
            else:
                curr = ins.Currency()
            ycatt = yc.YCAttribute(curr, curr)
        elif yc.AttributeType() == 'Issuer':
            if ins.Legs()[0].CreditRef():
                refins = ins.Legs()[0].CreditRef()
            else:
                refins = ins
            issuer = refins.Issuer()
            seniority = refins.Seniority()
            currency = refins.Currency()
            restructuring = ins.Restructuring()
            ycatt = yc.YCAttribute(issuer, currency, seniority, restructuring)
        else:
            return
        if not ycatt:
            return
        if ycatt.UnderlyingCurve():
            und = ycatt.UnderlyingCurve()
        else:
            und = yc.UnderlyingCurve()
        return ycatt.IrCurveInformation(get_ircurveinfo(und, ins), valday)
    elif yc.Category() in ('InstrumentSpreadCurve', 'InstrumentSpreadCurveBidAsk'):
        if not ins:
            return
        insspread = yc.InstrumentSpread(ins)
        if not insspread:
            return
        if insspread.UnderlyingYieldCurve():
            und = insspread.UnderlyingYieldCurve()
        else:
            return 
        return insspread.IrCurveInformationOverCurve(ins, get_ircurveinfo(und, ins), valday)
    elif yc.Category() in ('SpreadCurve'):
        undCurve = yc.UnderlyingCurve() 
        if not undCurve:
            return
        return yc.IrCurveInformation(undCurve.IrCurveInformation(valday),valday)
    else:
        return None
    
'''
    Write daily curve rate data output to file.
'''
def write_csv_file(date1, rates, fname, fpath, *rest):    
    tmpfile = file(fpath + fname + "_" + str(date1).replace("-","") + '.csv' , 'w')
    tmpfile.write(str(date1) + '\n')
    for r in rates:
        tmpfile.write(str(r) + '\n')
            
    tmpfile.close()
  
    return 

'''
    Extract daily curve rates for specified curves on a given day
'''    
def yc_rate_extract(temp, ycid, date1, n_entries, rateType, dayCount, dispRate, insid,  fpath, *rest):
    date1 = date1.to_ymd()
    date1 = acm.Time.DateFromYMD(date1[0],date1[1],date1[2])

    yc = acm.FYieldCurve[ycid]
    c_rates = []
    if not yc:
        return
    if yc.RealTimeUpdated():
        try:
            yc.Calculate()
            yc.Simulate()
        except:
            print 'Calculate failed for curve: ', yc.Name()
    ins = acm.FInstrument[insid]
    ircurveinfo = get_ircurveinfo(yc, ins)
    if ircurveinfo:
        dates = acm.Time.DateAddDelta(date1, 0, 0, list(range(1,n_entries + 1)))
        for d in dates:
            c_rates.append(ircurveinfo.Rate(date1, d, rateType, dayCount, dispRate, None, 0)*100.0)
            
    write_csv_file(date1, c_rates, ycid.replace("-","_"), fpath) 
    
    return 'done'



