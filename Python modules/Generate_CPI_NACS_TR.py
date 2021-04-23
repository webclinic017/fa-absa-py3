
"""
This script is used to calculate the nacs cpi points and also populate the benchmarks
the function update_cpi_nacs takes one param which determines whether the update
is commited or only simulated - a value of -1 will simulate only 
and any other value will commit
Dirk Strauss    -       2007-10-04
"""

import ael

debug = 1

def update_cpi_nacs(simulate_only):    
    yc_real = ael.YieldCurve['ZAR-REAL-TR']
    yc_swap = ael.YieldCurve['ZAR-SWAP']
    yc_cpi = ael.YieldCurve['ZAR-CPI-TR']
    mkt = ael.Party['SPOT']
    
    bms = []    
    prcs = []
    
    yc_cpi_bms = yc_cpi.benchmarks()
    
    for bm in yc_cpi_bms: 
        inst = bm.instrument
        datePeriod = bm.instrument.maturity_date()
        tpl = (datePeriod, inst)
        bms.append(tpl)
        
    bms.sort()    

    today = ael.date_today()
    
    for bm in bms:
        mat = bm[0]
        days = today.days_between(mat) 
        tf = 182.5 / days
        
        df1 = yc_real.yc_rate(today, mat, None, 'Act/365', 'Discount')
        df2 = yc_swap.yc_rate(today, mat, None, 'Act/365', 'Discount')
        
        cpi_yield = (((df1/df2) ** tf) - 1) * 2
        cpi_yield = cpi_yield * 100            
        
        if debug == 1:
            print today, mat, days, tf, cpi_yield, bm[1].insid, df1, df2        
    
        bm_ins = bm[1]        

        if len(bm_ins.prices()) > 0:
            for p in bm_ins.prices():
                if p.ptynbr == mkt:
                    prc = ael.Price[p.prinbr]                    
    
            if prc.settle <> cpi_yield or prc.last <> cpi_yield:
                prcC = prc.clone()
                prcC.last = cpi_yield
                prcC.settle = cpi_yield
                prcC.day = ael.date_today()
                prcC.commit()                
                if simulate_only == -1:
                    prcC.apply()
                else:
                    prcC.commit()
                prcs.append(prcC)
            else:
                print '====>', bm_ins.insid, ' not updated - no change in cpi'
        else:
            prcN = ael.Price.new()            
            prcN.last = cpi_yield            
            prcN.settle = cpi_yield
            prcN.insaddr = bm_ins
            prcN.day = ael.date_today()
            prcN.ptynbr = mkt
            prcN.curr = bm_ins.curr
            if simulate_only == -1:
                prcN.apply()
            else:
                prcN.commit()
            prcs.append(prcN)


# ==========================================================

update_cpi_nacs(0)
