import acm


def ABSA_get_ircurveinfo(yc, ins):
    '''space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    return ins.Calculation().MappedDiscountCurve(space)
    '''
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
        return ycatt.IrCurveInformation(ABSA_get_ircurveinfo(und, ins), valday)
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
        return insspread.IrCurveInformationOverCurve(ins, ABSA_get_ircurveinfo(und, ins), valday)
    elif yc.Category() in ('SpreadCurve'):
        undCurve = yc.UnderlyingCurve() 
        if not undCurve:
            return
        return yc.IrCurveInformation(undCurve.IrCurveInformation(valday), valday)
    else:
        return None
    
def ABSA_yc_rate(temp, ycid, date1, date2, rateType, dayCount, dispRate, insid, *rest):
    date1 = date1.to_ymd()
    date1 = acm.Time.DateFromYMD(date1[0], date1[1], date1[2])
    date2 = date2.to_ymd()
    date2 = acm.Time.DateFromYMD(date2[0], date2[1], date2[2])
    yc = acm.FYieldCurve[ycid]
    if not yc:
        return
    if yc.RealTimeUpdated():
        try:
            yc.Calculate()
            yc.Simulate()
        except:
            print 'Calculate failed for curve: ', yc.Name()
    ins = acm.FInstrument[insid]
    ircurveinfo = ABSA_get_ircurveinfo(yc, ins)
    if ircurveinfo:
        return ircurveinfo.Rate(date1, date2, rateType, dayCount, dispRate, None, 0)
