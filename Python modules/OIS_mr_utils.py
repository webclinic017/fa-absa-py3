import ael, time, acm

# ---------------------------------------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------------------------------------

 

debug = 1
g_regen_cpi = -1
cpi_curve = 'ZAR-CPI'
real_curve = 'ZAR-REAL'
nominal_curve = 'ZAR-SWAP'

# ---------------------------------------------------------------------------
# regenerate cpi curve in simulated status only - use for NACS curves
# ---------------------------------------------------------------------------

 

def update_cpi():
    cpiOff = ael.YieldCurve[real_curve].clone()
    cpiSwap = ael.YieldCurve[nominal_curve].clone()
    cpiTest= ael.YieldCurve[cpi_curve].clone()
    mkt = ael.Party['SPOT']
    
    bMarkPoints = []
    bm_pe = []
    
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
        mat = bMP[0]
        days = today.days_between(mat) 
        tf = 182.5 / days
        
        df1 = cpiOff.yc_rate(today, mat, None, 'Act/365', 'Discount')
        df2 = cpiSwap.yc_rate(today, mat, None, 'Act/365', 'Discount')
        
        cpiPrice = (((df1/df2) ** tf) - 1) * 2
        cpiPrice = cpiPrice * 100            
        
        #print today, mat, days, tf,  cpiPrice , bMP[1].insid       
    
        updInst1 = bMP[1]        

 

        if len(updInst1.prices()) > 0:
            for p in updInst1.prices():
                if p.ptynbr == mkt:
                    priEntity = ael.Price[p.prinbr]
                    
    
            if priEntity.bid <> cpiPrice or priEntity.ask <> cpiPrice:
                priEntityC = priEntity.clone()
                #log(1, mat, '%.2f' % ((cpiPrice - priEntityC.settle) * 100), '%.2f' % priEntityC.settle, '%.2f' % cpiPrice)
                priEntityC.last = cpiPrice
                priEntityC.settle = cpiPrice
                priEntityC.day = ael.date_today()
                priEntityC.apply()
                bm_pe.append(priEntityC)
    
    return bm_pe

#update_cpi() 

# ---------------------------------------------------------------------------
# updates the fwd starting cpi trades
# these trades are handled by front - the fwd starting index value is a function
# of cpi and as such needs to be updated when nominal, real or cpi curve is bumped - messy.
# ---------------------------------------------------------------------------
                
def calc_initial_indx(simulate_only):
    ins = ael.Instrument.select('instype = "IndexLinkedSwap"')
    indx_val = ael.Instrument['SACPI'].cpi_reference(ael.date_today())
    yc = ael.YieldCurve['ZAR-CPI']
    lgs = []
    
    for i in ins:
        for l in i.legs():
            if l.nominal_scaling == 'CPI':
                if i.add_info('Index_Date'):
                    if ael.date_today() <= ael.date(i.add_info('Index_Date')):                        
                        lc = l.clone()
                        oldidx = lc.initial_index_value
                        df = yc.yc_rate(ael.date_today(), ael.date(i.add_info('Index_Date')), None, 'Act/365', 'Discount')
                        if debug == 1:
                            print '====> generating new index', i.insid, df, oldidx, indx_val / df, (indx_val / df - oldidx)
                        lc.initial_index_value = indx_val / df                        
                        if simulate_only == 0:                            
                            lc.commit()
                        else:
                            lc.apply()
                            lgs.append(lc)
    
    return lgs 
                
# ---------------------------------------------------------------------------
# calcs benchmark deltas
# ---------------------------------------------------------------------------

 


def shiftCurve(temp,syc, lvl, *rest): 
    t0 = time.time()
    
    print ''
    
    if syc in (nominal_curve, real_curve):
        regen_cpi = g_regen_cpi
        yc_nom = ael.YieldCurve[nominal_curve].clone()
        print 'Calculating :', nominal_curve
        yc_nom.calculate()
        yc_nom.simulate()    
    else:
        regen_cpi = 0
    
    # we need this to update fwd starting cpi trades - see description for function calc_initial_indx()
    if syc in (nominal_curve, real_curve, cpi_curve):
        rebase_cpi_ins = -1
    else:
        rebase_cpi_ins = 0        
    
    #log(1, 'cpi regen set to : ', regen_cpi)        
    
    #if debug == 1:        
    #    print 'running bm delta', 'yc', syc, 'ins', ins.insid, 'tf', stf
    
    yc = ael.YieldCurve[syc].clone()
    yc_cpi = ael.YieldCurve[cpi_curve].clone()
    #tf = ael.TradeFilter[stf]    

 

    yc.calculate()
    yc.simulate()    

    

# Shift all benchmarks by same amount

    print 'Shifting all benchmarks parallel with predefined shift size'
    bm = yc.benchmarks()
    for b in bm:
        
        inss = b.instrument
        prc = inss.prices()
        for p in prc: 
            if p.ptynbr.ptyid == 'SPOT':
                pc = p.clone()
                pc.settle = p.settle + lvl
                pc.last = p.last + lvl
                pc.bid = p.bid + lvl
                pc.ask = p.ask + lvl
                pc.apply()                  

 
    print 'calculating yield curve'
    yc.calculate()
    print 'simulating yield curve'
    yc.simulate()  
    
    if regen_cpi == -1:
        if debug == 1:
            print 'calling cpi bm update function'            
        bm_pe = update_cpi()        
 
        if debug == 1:
            print 'simulating cpi curve'

        yc_cpi.calculate()
        yc_cpi.simulate()

    if rebase_cpi_ins == -1:
        print 'Rebasing cpi fwd ins. Calling function calc_initial_indx()'
        fwd_cpi_ins = calc_initial_indx(1)
    else:
        fwd_cpi_ins = []


 #End

    
    return 5

#shiftCurve(5,'ZAR-CPI', 0.5)


 
def revertshiftCurve(temp,syc, *rest): 
    t0 = time.time()
    
    print ''
    regen_cpi = -1
    rebase_cpi_ins = -1
    debug = 1

    yc = ael.YieldCurve[syc].clone()
    yc_cpi = ael.YieldCurve[cpi_curve].clone()


    yc.calculate()
    yc.simulate()    
    yc_cpi.calculate()
    yc_cpi.simulate()

 
#revert_apply all benchmark values

 

    bm = yc.benchmarks()
    for b in bm:
        inss = b.instrument
        prc = inss.prices()
        for p in prc: 
            if p.ptynbr.ptyid == 'SPOT':
                pc = p.clone()
                pc.revert_apply()  

#end

    print 'calculating yield curve'
    yc.calculate()
    print 'simulating yield curve'
    yc.simulate()

    print 'calling cpi bm update function'            
    bm_pe = update_cpi()        

    print 'simulating cpi curve'

    yc_cpi.calculate()
    yc_cpi.simulate()

    print 'Rebasing cpi fwd ins. Calling function calc_initial_indx()'
    fwd_cpi_ins = calc_initial_indx(1)
        
    for bmcpi in bm_pe:
        bmcpi.revert_apply()                
            
    yc_cpi.calculate()
    yc_cpi.simulate()
    
    print 'reverting fwd starting cpi index values'        

    for cpiins in fwd_cpi_ins:
        cpiins.revert_apply()            
 
    return 5

def shiftBasisCurve(temp, syc, lvl, *rest):
    t0 = time.time()
    if not lvl:
        lvl = 0
    
    #ael
    
    #ycb = ael.YieldCurve[syc]
    #yc = ycb.underlying_yield_curve_seqnbr.clone()
    #tf = ael.TradeFilter[stf]    

    #print ycb.points()
    
    #for member in ycb.attributes():
    #    for sprd in member.spreads():
    #        sc = sprd.clone()
    #        sc.spread = sprd.spread + float(lvl)/100
    #        sc.apply()            
 
    #yc.calculate()
    #yc.simulate()    
    
    # now let's try acm
    ycb = ael.YieldCurve[syc]
    yc = acm.FYieldCurve[ycb.underlying_yield_curve_seqnbr.seqnbr]
    ycc = yc.Clone()
    #tf = ael.TradeFilter[stf]    

    print ycb.points()
    
    for member in ycb.attributes():
        for sprd in member.spreads():
            sc = sprd.clone()
            sc.spread = sprd.spread + float(lvl)/100
            sc.apply()
 
    ycc.Calculate()
    yc.Apply(ycc)
        
    
    return 5

def revertshiftBasisCurve(temp, syc, lvl,*rest):
    t0 = time.time()
    if not lvl:
        sftsize = 0
    
    # ael
    # ycb = ael.YieldCurve[syc]
    # yc = ycb.underlying_yield_curve_seqnbr.clone()
#    tf = ael.TradeFilter[stf]    

    # print ycb.points()
    
    #for member in ycb.attributes():
    #    for sprd in member.spreads():
    #        sc = sprd.clone()
    #        #manually revert bumped value
    #        sc.spread = sprd.spread - float(lvl)/100 
    #        sc.apply() 
    #        #sc.revert_apply()  

    #yc.calculate()
    #yc.simulate()    
    
    # now let's try acm
    ycb = ael.YieldCurve[syc]
    yc = acm.FYieldCurve[ycb.underlying_yield_curve_seqnbr.seqnbr]
    ycc = yc.Clone()
    #tf = ael.TradeFilter[stf]    

    print ycb.points()
    
    for member in ycb.attributes():
        for sprd in member.spreads():
            sc = sprd.clone()
            #manually revert bumped value
            sc.spread = sprd.spread - float(lvl)/100 
            sc.apply() 
            #sc.revert_apply()

    ycc.Calculate()
    yc.Apply(ycc)

    
    return 5

#revertshiftBasisCurve(5, 'ZAR-BASIS')


#print shiftBasisCurve(None, 'ZAR-BASIS', 1.0)


