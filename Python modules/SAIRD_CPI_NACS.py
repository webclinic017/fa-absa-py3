"""
This script is used to calculate the nacs cpi points and also populate the benchmarks
the function update_cpi_nacs takes one param which determines whether the update
is commited or only simulated - a value of -1 will simulate only 
and any other value will commit
Dirk Strauss    -       2007-10-04
"""

import ael

debug = 1

def update_cpi_nacs(simulate_only, price):    
    yc_real = ael.YieldCurve['ZAR-REAL'].clone()
    yc_swap = ael.YieldCurve['ZAR-SWAP'].clone()
    yc_cpi = ael.YieldCurve['ZAR-CPI']
    mkt = ael.Party['SPOT']
    #print price.pp()
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
    
         
    
    #===============================================================================================
    pi = ael.Instrument[price.insaddr.insid]
    for p in pi.prices():
        if p.ptynbr == mkt:
            new_p = p
            break
    pclone = new_p.clone()
    pclone.settle = price.settle
    pclone.last = price.last
    pclone.apply()
    yc_real.calculate()
    yc_real.simulate()
    yc_swap.calculate()
    yc_swap.simulate()
    
    
    #===============================================================================================
    
    
    for bm in bms:
        mat = bm[0]
        days = today.days_between(mat) 
        tf = 182.5 / days
        
        df1 = yc_real.yc_rate(today, mat, None, 'Act/365', 'Discount')
        df2 = yc_swap.yc_rate(today, mat, None, 'Act/365', 'Discount')
        
        cpi_yield = (((df1/df2) ** tf) - 1) * 2
        cpi_yield = cpi_yield * 100            
            
    
        bm_ins = bm[1]        
        
        if len(bm_ins.prices()) > 0:
            for p in bm_ins.prices():
                if p.ptynbr == mkt:
                    prc = ael.Price[p.prinbr]                    
            
            if round(prc.settle, 8) <> round(cpi_yield, 8) or round(prc.last, 8) <> round(cpi_yield, 8):
                prev = prc.settle
                prcs.append([prc, cpi_yield])
                
                #print '====>  ', bm_ins.insid, 'UPDATED.. Old Value ', prev, 'New Value', cpi_yield
                
            
    pclone.revert_apply()
    yc_real.calculate()
    yc_real.simulate()
    yc_swap.calculate()
    yc_swap.simulate()
    
    for p in prcs:
        pc = p[0].clone()
        pc.last = p[1]
        pc.settle = p[1]
        pc.day = ael.date_today()
        try:
            pc.commit()
        except:
            print 'price did not commit'
    ael.poll()
        

# ==========================================================

def calc_initial_indx():
    ins = ael.Instrument.select('instype = "IndexLinkedSwap"')
    indx_val = ael.Instrument['SACPI'].cpi_reference(ael.date_today())
    yc = ael.YieldCurve['ZAR-CPI']
    for i in ins:
        for l in i.legs():
            if l.nominal_scaling == 'CPI':
                if i.add_info('Index_Date'):
                    if ael.date_today() <= ael.date(i.add_info('Index_Date')):
                        lc = l.clone()
                        df = yc.yc_rate(ael.date_today(), ael.date(i.add_info('Index_Date')), None, 'Act/365', 'Discount')
                        lc.initial_index_value = indx_val / df
                        lc.commit()
                        print 'Updated: ', i.insid
    ael.poll()
def update(sim, price):

    update_cpi_nacs(0, price)
    try:
        calc_initial_indx()
        print 'Calculated Index Linked Swap(Index_Date)'
        return 'SUCCESS'
    except:
        print 'Could not recalculate Index Linked Swap(Index_Date)'
        return 'FAIL'
        
