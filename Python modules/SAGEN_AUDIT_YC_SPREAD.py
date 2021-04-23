import ael, acm
from zak_funcs import write_file


#       Written By Zaakirah kajee April 2009
#       Audit requirement: monitor changes to spreads on YC



today = ael.date_today()
yes = today.add_banking_day(ael.Instrument['ZAR'], -1)
#dateS =  today.to_string('%Y-%m-%d')
yesd=  yes.to_string('%m/%d/%y')

results = [['YIELD CURVE', 'CURVE TYPE', 'ATTRIBUTE NAME', 'ATTRIBUTE TYPE', 'OLD VAL', 'NEW VAL', 'LAST UPDATE USER', 'USER GROUP' ]]




def check_ins_spread():
    if today == ael.date_today():
        ycs = acm.FInstrumentSpreadCurve.Select("historicalDay = ''" )
    else:
        ycs = acm.FInstrumentSpreadCurve.Select("historicalDay = '%s'" %(tods))
        
    for c in ycs:
        ins = {}
        if ael.date_from_time(c.UpdateTime()) == today:
            for i in c.InstrumentSpreads():
                if ael.date_from_time(i.UpdateTime()) == today:
                    ins[i.Instrument().Name()] = i.Spread()
                    
                    
            if today == ael.date_today():
                ycname = c.Name()
                ycc = c
            else:
                ycname = c.OriginalCurve().Name()
                ycc = c.OriginalCurve()
            y1 = []
            y1 = acm.FInstrumentSpreadCurve.Select("originalCurve = '%s' and historicalDay = '%s'" %(ycc.Oid(), yesd))
            if len(y1) > 0:
                y = y1.At(0)
                for i in y.InstrumentSpreads():
                    if i.Instrument().Name() in ins.keys():
                        results.append([c.Name(), 'Instrument Spread', i.Instrument().Name(), i.SpreadType(), i.Spread(), ins[i.Instrument().Name()], c.UpdateUser().Name(), c.UpdateUser().UserGroup().Name() ])
            
               
def check_att_spread():
    if today == ael.date_today():
        ycs = acm.FAttributeSpreadCurve.Select("historicalDay = ''" )
    else:
        ycs = acm.FAttributeSpreadCurve.Select("historicalDay = '%s'" %(tods))

    for y1 in ycs:
        
        if y1 :
            points = []
            pdict = {}
            for p in y1.Points():
                count = 0
                spread = acm.FYCSpread.Select("point = '%s'" %p.Oid())
                for s in spread:
                    if ael.date_from_time(s.UpdateTime()) == today:
                        if p.DatePeriod() not in points:
                            points.append(p.DatePeriod())
                       
                        if y1.AttributeType() == 'Issuer':
                            if p.DatePeriod() in pdict.keys():
                                pdict[p.DatePeriod()].append([s.Attribute().Issuer().Name(), s.Spread()*100.0])
                            else:
                                pdict[p.DatePeriod()] = [[s.Attribute().Issuer().Name(), s.Spread()*100.0]]
                        if y1.AttributeType() == 'Currency':
                            if p.DatePeriod() in pdict.keys():
                                pdict[p.DatePeriod()].append([s.Attribute().Currency().Name(), s.Spread()*100.0])
                            else:
                                pdict[p.DatePeriod()] = [[s.Attribute().Currency().Name(), s.Spread()*100.0]]
            
            if len(pdict) != 0: 
                if today == ael.date_today():
                    ycname = y1.Name()
                    ycc = y1
                else:
                    ycname = y1.OriginalCurve().Name()
                    ycc = y1.OriginalCurve()
                y2 = []
                y2 = acm.FYieldCurve.Select("originalCurve = '%s' and historicalDay = '%s'" %(ycc.Oid(), yesd))
                
                if len(y2) > 0:
                    y = y2.At(0)
                    for p in y.Points():
                        if p.DatePeriod() in points:
                            spread = acm.FYCSpread.Select("point = '%s'" %p.Oid())
                            for s in spread:
                                for x in pdict[p.DatePeriod()]:
                                    
                                    if y1.AttributeType() == 'Issuer':
                                        if s.Attribute().Issuer().Name()== x[0] and round(s.Spread()*100.0, 5) != round(x[1], 5):
                                            results.append([y1.Name(), 'Issuer Spread', s.Attribute().Issuer().Name(), p.DatePeriod(), s.Spread()*100.0, x[1], y1.UpdateUser().Name(), y1.UpdateUser().UserGroup().Name()])
                                           
                                    if y1.AttributeType() == 'Currency':
                                        if s.Attribute().Currency().Name()== x[0] and round(s.Spread()*100.0, 5) != round(x[1], 5):
                                            
                                            results.append([y1.Name(), 'Currency Spread', s.Attribute().Currency().Name(), p.DatePeriod(), s.Spread()*100.0, x[1], y1.UpdateUser().Name(), y1.UpdateUser().UserGroup().Name()])
            
   

check_att_spread()
check_ins_spread()
prod = '//services/frontnt/BackOffice/Atlas-End-Of-Day/' +  ael.date_today().to_string('%Y-%m-%d') + '/'

if len(results) > 1:
    #write_file('F:/YC_CONST1.csv',results)
    write_file(prod + 'SAGEN_AUDIT_YC_SPREAD.csv', results)
else:
    print ael.log('SAGEN_AUDIT_YC_SPREAD, NO CHANGES TO SPREADS ON YC')
