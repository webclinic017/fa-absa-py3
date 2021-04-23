import ael, acm, sets
from zak_funcs import write_file


#       Written By Zaakirah kajee April 2009
#       Audit requirement: monitor changes to makeup and settings on YC


today = ael.date_today()
yes = today.add_banking_day(ael.Instrument['ZAR'], -1)
#yesd=  yes.to_string('%m/%d/%y')
tods = today.to_string('%Y-%m-%d')
yesd = yes.to_string('%Y-%m-%d')



yc_attr = ['.PayDayMethod()', 'Att', '.EstimationType()', '.InterpolationType()', '.UseBenchmarkDates()', '.BenchmarkInstruments()', '.Points()', '.IrFormat()',
'.InstrumentSpreads()', '.Currency().Name()', '.AttributeType()', '.RiskType()', '.IsBidAsk()', '.IsYield()', '.Type()']


def get_att(yc):
    att = []
    for p in yc.Points():
        spread = acm.FYCSpread.Select("point = '%s'" %p.Oid())
        for s in spread:
            
            if yc.AttributeType() == 'Issuer':
                if s.Attribute().Issuer().Name() not in att:
                    att.append(s.Attribute().Issuer().Name())
            if yc.AttributeType() == 'Currency':
                if s.Attribute().Currency().Name() not in att:
                    att.append(s.Attribute().Currency().Name())
    return att

def check_curves():
    results = [['YIELD CURVE', 'PROPERTY', 'BEFORE', 'AFTER', 'LAST UPDATE USER', 'USER GROUP']]
    if today == ael.date_today():
        ycs = acm.FYieldCurve.Select("historicalDay = ''" )
    else:
        ycs = acm.FYieldCurve.Select("historicalDay = '%s'" %(tods))
    for yc in ycs:
        
        if ael.date_from_time(yc.UpdateTime()) == today:
            #name = yc.Name() + '_' + yesd
            if today == ael.date_today():
                ycname = yc.Name()
                ycc = yc
            else:
                ycname = yc.OriginalCurve().Name()
                ycc = yc.OriginalCurve()
            y1 = []
            y1 = acm.FYieldCurve.Select("originalCurve = '%s' and historicalDay = '%s'" %(ycc.Oid(), yesd))
            #print yc.Name(), yesd,tods,  y1, ycc.Name()          
            
            if len(y1) > 0:
                #print y1.At(0)
                y = y1.At(0)
                for a in yc_attr:
                    
                    if a == '.BenchmarkInstruments()':
                        
                        e1 = sets.Set([x.Name() for x in eval("yc" + a )])
                        e2 = sets.Set([x.Name() for x in eval("y" + a )])
                        #print 'ORIGINAL', e1
                        #print 'ARCHIVED', e2
                        for b in e1.difference(e2):
                            results.append([ycc.Name(), 'BENCHMARK INS', b, 'ADDED TO CURVE', yc.UpdateUser().Name(), yc.UpdateUser().UserGroup().Name()])
                        for b in e2.difference(e1):
                            results.append([ycc.Name(), 'BENCHMARK INS', b, 'REMOVED FROM CURVE', yc.UpdateUser().Name(), yc.UpdateUser().UserGroup().Name()])
                        
                    elif a == '.Points()':
                        e1 = sets.Set([x.DatePeriod() for x in eval("yc" + a )])
                        e2 = sets.Set([x.DatePeriod() for x in eval("y" + a )])
                        for b in e1.difference(e2):
                            results.append([ycc.Name(), 'YC POINTS', b, 'ADDED TO CURVE', yc.UpdateUser().Name(), yc.UpdateUser().UserGroup().Name()])
                        for b in e2.difference(e1):
                            #print b, 'REMOVED FROM CURVE'
                            results.append([ycc.Name(), 'YC POINTS', b, 'REMOVED FROM CURVE', yc.UpdateUser().Name(), yc.UpdateUser().UserGroup().Name()])
                    elif a == '.InstrumentSpreads()':
                        if yc.Type() == 'Instrument Spread':
                        
                            e1 = sets.Set([x.Instrument().Name() for x in eval("yc" + a )])
                            e2 = sets.Set([x.Instrument().Name() for x in eval("y" + a )])
                            for b in e1.difference(e2):
                                results.append([ycc.Name(), 'INSTRUMENT SPREAD', b, 'ADDED TO CURVE', yc.UpdateUser().Name(), yc.UpdateUser().UserGroup().Name()])
                            for b in e2.difference(e1):
                                results.append([ycc.Name(), 'INSTRUMENT SPREAD', b, 'REMOVED FROM CURVE', yc.UpdateUser().Name(), yc.UpdateUser().UserGroup().Name()])
                    elif a == 'Att':
                        if yc.Type() == 'Attribute Spread':
                                a1 = sets.Set(get_att(yc))
                                a2 = sets.Set(get_att(y))
                                
                                for b in a1.difference(a2):
                                    results.append([ycc.Name(), 'ATTRIBUTE', b, 'ADDED TO CURVE', yc.UpdateUser().Name(), yc.UpdateUser().UserGroup().Name()])
                                for b in a2.difference(a1):
                                    results.append([ycc.Name(), 'ATTRIBUTE', b, 'REMOVED FROM CURVE', yc.UpdateUser().Name(), yc.UpdateUser().UserGroup().Name()])
                    else:
                        try:
                            if eval("yc" + a) != eval("y" + a):
                                results.append([ycc.Name(), a[1:(len(a)-2)], eval("y" + a), eval("yc" + a), yc.UpdateUser().Name(), yc.UpdateUser().UserGroup().Name()])
                        except:
                            print 'error accessing attribute', a, yc.Name()
            else:
                #print 'VPS CURVE DOESNT EXIST FOR: ', ycc.Name(), 'Created : ', ael.date_from_time(yc.CreateTime())
                results.append([ycc.Name(), 'VPS CURVE DOESNT EXIST', 'Created : ', ael.date_from_time(yc.CreateTime()), yc.UpdateUser().Name(), yc.UpdateUser().UserGroup().Name() ])
    return results
  
r = []                
r = check_curves()
prod = '//services/frontnt/BackOffice/Atlas-End-Of-Day/' +  ael.date_today().to_string('%Y-%m-%d') + '/'

if len(r) > 1:
    #write_file('F:/YC_CONST.csv',r)
    write_file(prod + 'SAGEN_AUDIT_YC_CONST.csv', r)
else:
    print ael.log('SAGEN_AUDIT_YC_CONST, NO CHANGES TO SPREADS ON YC')
