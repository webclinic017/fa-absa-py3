import ael

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

    if today.days_between(endDay) < 365:
         cpiPrice =  (df1/df2-1)*36500/(today.days_between(endDay))   
    else:

        cpiPrice =  ((df1/df2)**(365.0/(today.days_between(endDay)))-1)*100.0
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
