import ael

def Test(temp,*rest):

    cpiOff = ael.YieldCurve['ZAR-REAL/PriceTesting']
    cpiSwap = ael.YieldCurve['ZAR-SWAP/PriceTesting']
    cpiTest= ael.YieldCurve['ZAR-CPI/PriceTesting']
    mkt = ael.Party['SPOT']
    
    bMarkPoints = []
    
    
    cpiTestPts= cpiTest.points()
    cpiTestBmks = cpiTest.benchmarks()
    
    
    for y in cpiTestBmks: 
        inst = y.instrument
        datePeriod = y.instrument.maturity_date()
        tpl = (inst, datePeriod)
        bMarkPoints.append(tpl)
    
    
    for bMP in bMarkPoints:
        period = bMP[1]
        today = ael.date_today()
        endDay = period
        
        df1 = cpiOff.yc_rate(today, endDay, None, 'Act/365', 'Discount')
        df2 = cpiSwap.yc_rate(today, endDay, None, 'Act/365', 'Discount')
    
        if today.days_between(endDay) <365:
            cpiPts=[]
        
            today = ael.date_today()
            Monthday=today.day_of_month()
            Monthdays=today.days_in_month()
        
            for x in ael.Instrument['SACPI'].historical_prices():
                day=x.day
                value=x.last
                tpl=(day, value)
                if value>0:
                    cpiPts.append(tpl)
            
            cpiPts.sort()
        
            listlen=len(cpiPts)
            
            cpilatest=cpiPts[listlen-1]
            cpi12=cpiPts[listlen-13]
            D=float(endDay.days_in_month())
            d=float(endDay.day_of_month())
            def lin_interp(x, y, val):    
        
                if val <= x[0]:
                    return y[0]
                
                for k in range(1, len(x)):
                    if x[k] > val:
                        n = x[k-1].days_between(x[k]) * 1.0
                        n1 = x[k-1].days_between(val) * 1.0
                        n2 = n - n1            
                        interp = n1/n * y[k] + n2/n * y[k-1]
                        return interp
                
                return y[ len(y)-1 ]
            
            #cpiPrice=cpilatest[1]
            pricenow=((cpilatest[1]-cpi12[1])/cpi12[1])*100
            cpiPrice=200*(((1+(pricenow/100))**(0.5))-1)
            
        #elif today.days_between(endDay) >= 31 and today.days_between(endDay) < 365:
            # cpiPrice =  (df1/df2-1)*36500/(today.days_between(endDay))   
        else:
            cpiPrice =  ((df1/df2)**(182.5/(today.days_between(endDay)))-1)*200.0
        print 'today', today, 'endDay', endDay, 'd1', df1, 'd2', df2, 'cpiPrice', cpiPrice, 'diff', today.days_between(endDay)
        updInst1 = bMP[0]
        if len(updInst1.prices()) > 0:
            for p in updInst1.prices():
                if p.ptynbr == mkt:
                    priEntity = ael.Price[p.prinbr]
                    
    
            if priEntity.bid <> cpiPrice or priEntity.ask <> cpiPrice:
                priEntityC = priEntity.clone()
                priEntityC.last = cpiPrice
                priEntityC.settle = cpiPrice
                priEntityC.day = ael.date_today()
                priEntityC.commit()
                
        else:
            pn = ael.Price.new()
            assert(pn.bits == 2)
            pn.last = cpiPrice
            assert(pn.bits == 18)
            pn.settle = cpiPrice
            pn.insaddr = updInst1
            pn.day = ael.date_today()
            pn.ptynbr = mkt
            pn.curr = updInst1.curr
            pn.commit()
    return 'Success'
