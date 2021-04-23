import ael
cpiOff = ael.YieldCurve['ZAR-REAL-OLD']
cpiSwap = ael.YieldCurve['ZAR-SWAP']
cpiTest= ael.YieldCurve['ZAR-CPI-OLD']
mkt = ael.Party['SPOT']

bMarkPoints = []


cpiTestPts= cpiTest.points()
cpiTestBmks = cpiTest.benchmarks()


for y in cpiTestBmks: 
    inst = y.instrument
    datePeriod = y.instrument.maturity_date()
    tpl = (datePeriod, inst)
    bMarkPoints.append(tpl)
    
bMarkPoints.sort()
step = ael.date_today()
EndPeriod = bMarkPoints[len(bMarkPoints)-1][0]
today = ael.date_today()


for bMP in bMarkPoints:
    sum = 0
    step = ael.date_today()
    step1 = step
    months = 0
    while  (step < EndPeriod and step <= bMP[0] ):
        
        df1 = cpiOff.yc_rate(today, step, None, 'Act/365', 'Discount')
        df2 = cpiSwap.yc_rate(today, step, None, 'Act/365', 'Discount')
        sum = sum + df2/df1*step1.days_between(step)/365
#       print step,EndPeriod,df2/df1,sum,step1.days_between(step)
        step1 = step 
        if months in [3, 4, 5]:
            months = months + 1
        else:
            months = months + 3
        step = ael.date_today().add_months(months)
        step = step.adjust_to_banking_day(ael.Instrument['ZAR'], 'Mod. Following')
        
        
    period = bMP[0]
    endDay = period
    
    if today.days_between(bMP[0]) > 365:
        cpiPrice = ((1-df2/df1)/sum)*100
    else:
        cpiPrice =  (df1/df2-1)*36500/(today.days_between(bMP[0]))   
        
    print period, "disc", cpiPrice, sum, bMP[1].insid, df1, df2
    

    updInst1 = bMP[1]
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
