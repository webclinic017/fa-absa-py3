import ael, time, acm
import SAFI_BOND_TRS

from dirk_utils import mightBeUsedPrice as mightBeUsedPrice

debug = 1
g_regen_cpi = -1
regen_cpi = 0
cpi_curve = 'ZAR-CPI'
real_curve = 'ZAR-REAL'
nominal_curve = 'ZAR-SWAP'
fwd_cpi_ins = []

def log(lvl, *out):
    t0 = time.ctime()
    
    s = ''
    
    if lvl == debug:
        for o in out:
            s = s + '\t' + str(o)
        
    print t0, s

def shiftCurve(temp, syc, lvl, stf, *rest):
    t0 = time.time()
    
    print ''
    
    if syc in (nominal_curve, real_curve):
        regen_cpi = g_regen_cpi
        #yc_nom = ael.YieldCurve[nominal_curve].clone()
        #print 'Calculating :', nominal_curve
        #yc_nom.calculate()
        #yc_nom.simulate()
        yc_nom = acm.FYieldCurve[nominal_curve]
        ycc_nom = yc_nom.Clone()
        print 'Calculating :', nominal_curve
        ycc_nom.Calculate()
        yc_nom.Apply(ycc_nom)
    else:
        regen_cpi = 0
    
    # we need this to update fwd starting cpi trades - see description for function calc_initial_indx()
    if syc in (nominal_curve, real_curve, cpi_curve):
        rebase_cpi_ins = -1
    else:
        rebase_cpi_ins = 0        
    
    log(1, 'cpi regen set to : ', regen_cpi)        
    
    if debug == 1:        
        print 'running bm delta', 'yc', syc
    
    #yc = ael.YieldCurve[syc].clone()
    #yc_cpi = ael.YieldCurve[cpi_curve].clone()
    #tf = ael.TradeFilter[stf]     
    
    #yc.calculate()
    #yc.simulate()    
    
    yc = acm.FYieldCurve[syc]
    ycc = yc.Clone()
    yc_cpi = acm.FYieldCurve[cpi_curve]
    ycc_cpi = yc_cpi.Clone()
    tf = ael.TradeFilter[stf]    

    ycc.Calculate()
    yc.Apply(ycc)    

# Shift all benchmarks by same amount

    print 'Shifting all benchmarks parallel with predefined shift size'
    if lvl:
        lvl = float(lvl)    
        
    bm = ael.YieldCurve[yc.Oid()].benchmarks()
    for b in bm:
        inss = b.instrument
        prc = inss.prices()      
        for p in prc: 
            if mightBeUsedPrice(p) or p.ptynbr.ptyid == 'SPOT':
                pc = p.clone()
                pc.settle = p.settle + lvl
                pc.last = p.last + lvl
                pc.bid = p.bid + lvl
                pc.ask = p.ask + lvl
                pc.apply()                  
 
    print 'calculating yield curve'
    #yc.calculate()
    print 'simulating yield curve'
    #yc.simulate()  

    ycc.Calculate()
    yc.Apply(ycc)

    if regen_cpi == -1:
        if debug == 1:
            print 'calling cpi bm update function'            
        bm_pe = update_cpi()        
 
        if debug == 1:
            print 'simulating cpi curve'

        #yc_cpi.calculate()
        #yc_cpi.simulate()
        ycc_cpi.Calculate()
        yc_cpi.Apply(ycc_cpi)

    if rebase_cpi_ins == -1:
        print 'Rebasing cpi fwd ins. Calling function calc_initial_indx()'
        fwd_cpi_ins = calc_initial_indx(1)
    else:
        fwd_cpi_ins = []

    if debug == 2:
        print 'original curve'
        print yc
        print ''
        
    if debug == 1:
        print 'calling present_value() function'    
    pv0 = tf.present_value()
       
    if debug == 1:
        print 'simulating', syc
        
    ycc.Calculate()
    yc.Apply(ycc)   
    
    if regen_cpi == -1:
        if debug == 1:
            print 'calling cpi bm update function'            
        bm_pe = update_cpi()        

        if debug == 1:
            print 'simulating cpi curve'
        
        ycc_cpi.Calculate()
        yc_cpi.Apply(ycc_cpi)
    
    if rebase_cpi_ins == -1:
        print 'Rebasing cpi fwd ins. Calling function calc_initial_indx()'
        fwd_cpi_ins = calc_initial_indx(1)
    else:
        fwd_cpi_ins = []
        
    if debug == 2:
        print 'modified curve'
        print yc
        print ''
        
    if debug == 1:
        print 'calculating bumped pv value'    
    
    pv1 = tf.present_value()
    pv01 = pv1 - pv0
    
    if debug == 1:
        print pv0, pv1, pv01        
           

def revertshiftCurve(temp, syc, lvl, *rest):
    t0 = time.time()

    #ycb = ael.YieldCurve[syc]
    #yc = ycb.clone()
    yc = acm.FYieldCurve[syc]
    ycc = yc.Clone()
#    tf = ael.TradeFilter[stf]  

    if debug == 1:
        print 'reverting bm entries and yc calc'  
   
    if lvl:
        lvl = float(lvl) 
        
    bm = ael.YieldCurve[yc.Oid()].benchmarks()
    for b in bm:        
        inss = b.instrument
        prc = inss.prices()
        for p in prc: 
            if mightBeUsedPrice(p) or p.ptynbr.ptyid == 'SPOT':
                pc = p.clone()
                pc.settle = p.settle - lvl
                pc.last = p.last - lvl
                pc.bid = p.bid - lvl
                pc.ask = p.ask - lvl
                pc.apply() 

#end
    #yc.calculate()
    #yc.simulate()
    ycc.Calculate()
    yc.Apply(ycc)  
    
    if regen_cpi == -1:
        # this will never be reached, regen_cpi is 0
        if debug == 1:
            print 'reverting cpi bm entries and yc calc'        
        for bmcpi in bm_pe:
            bmcpi.revert_apply()                
            
        yc_cpi.calculate()
        yc_cpi.simulate()
    
    if debug == 1:
        print 'reverting fwd starting cpi index values' 

    if fwd_cpi_ins:
        for cpiins in fwd_cpi_ins:
            cpiins.revert_apply()        
            
    
def bm_delta(ins, stf, syc, bond_trs=0, *rest):
    """Yield curve price bumping {along with ZAR-CPI update).
        
    Manual version of price bumping which doesn't use 'revert apply' in order
    to prevent reverting applied changes from the previous (parallel) shift
    (e.g. when using OIS_BmpBM_CalcBM query where the first step is to bump
    the same curve by the given level).
    
    AEL version of applying changes to yield curves is depricated in FA 2013
    and doesn't work properly. Present value before and after price bumping 
    does not change. ACM version (combination of Calculate() and Apply() does
    produce the desired output.
        
    If bond_trs=1 then a function will be called to simulate a fixing on TRS's
    on bonds.
    
    """
    t0 = time.time()
    
    print ''
    
    if syc in (nominal_curve, real_curve):
        regen_cpi = g_regen_cpi
        yc_nom = acm.FYieldCurve[nominal_curve]
        yc_nom_clone = yc_nom.Clone()
        print 'Calculating :', nominal_curve
        yc_nom_clone.Calculate()
        yc_nom.Apply(yc_nom_clone)
    else:
        regen_cpi = 0
    '''
    # we need this to update fwd starting cpi trades - see description for function calc_initial_indx()
    if syc in (nominal_curve, real_curve, cpi_curve):
        rebase_cpi_ins = -1
    else:
        rebase_cpi_ins = 0        
    '''
    rebase_cpi_ins = 0        
    
    log(1, 'cpi regen set to : ', regen_cpi)        
    
    if debug == 1:        
        print 'running bm delta', 'yc', syc, 'ins', ins.insid, 'tf', stf
    
    yc = acm.FYieldCurve[syc]
    yc_clone = yc.Clone()
    
    yc_cpi = acm.FYieldCurve[cpi_curve]
    yc_cpi_clone = yc_cpi.Clone()
    
    tf = ael.TradeFilter[stf]    

    yc_clone.Calculate()
    yc.Apply(yc_clone)

    if tf == None:
        print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
        return -99999999999.0
    
    if debug == 2:
        print 'original curve'
        print yc.pp()
        print ''
        
    if debug == 1:
        print 'calling present_value() function'    
    
    if bond_trs:
        ''' Invalid pv01's are calculated when this query is run for the first time.  After the data has been 
            loaded into memory and run again the query runs correctly.  Calculating the PV loads all the 
            relevant yield curves into memory.
        '''
        temp = tf.present_value()
        pv0 = SAFI_BOND_TRS.PVSimulateFixedFilter(acm.FTradeSelection[stf])
    else:
        pv0 = tf.present_value()
    
    print 'pv0 =', pv0
    
    prc = ins.prices()            
    
    for p in prc:
        #print p.day, p.ptynbr.ptyid, p.settle
        if mightBeUsedPrice(p) or p.ptynbr.ptyid == 'SPOT':
            if debug == 2:
                print 'found price'
                print p.pp()
                print ''
                
            pc = p.clone()
            log(1, 'changing point from', pc.settle, 'to', pc.settle + 0.01)
            
            pc.settle = p.settle + 0.01
            pc.last = p.last + 0.01
            pc.bid = p.bid + 0.01
            pc.ask = p.ask + 0.01
            pc.apply()   
            
            if debug == 2:
                print 'cloned point'
                print pc.pp()
                print ''
    
    if debug == 1:
        print 'simulating', syc
        
    yc_clone.Calculate()
    yc.Apply(yc_clone)
    
    if regen_cpi == -1:
        if debug == 1:
            print 'calling cpi bm update function'            
        bm_pe = update_cpi()        

        if debug == 1:
            print 'simulating cpi curve'
        
        yc_cpi_clone.Calculate()
        yc_cpi.Apply(yc_cpi_clone)
    '''
    if rebase_cpi_ins == -1:
        print 'Rebasing cpi fwd ins. Calling function calc_initial_indx()'
        fwd_cpi_ins = calc_initial_indx(1)
    else:
        fwd_cpi_ins = []
    '''
    fwd_cpi_ins = []    
        
    if debug == 2:
        print 'modified curve'
        print yc.pp()
        print ''
        
    if debug == 1:
        print 'calculating bumped pv value'    
    
    if bond_trs:
        pv1 = SAFI_BOND_TRS.PVSimulateFixedFilter(acm.FTradeSelection[stf])
    else:
        pv1 = tf.present_value()
    
    print 'pv1 =', pv1
    pv01 = pv1 - pv0
    print 'pv01 =', pv01
    
    if debug == 1:
        print ins.insid, pv0, pv1, pv01        
        
    if debug == 1:
        print 'reverting bm entries and yc calc'

#manually reverting bump to previously stressed level
    for p in prc:
        if mightBeUsedPrice(p) or p.ptynbr.ptyid == 'SPOT':
            pc = p.clone()
            pc.settle = p.settle - 0.01
            pc.last = p.last - 0.01
            pc.bid = p.bid - 0.01
            pc.ask = p.ask - 0.01
            pc.apply()   
            
#end

#    pc.revert_apply()
    yc_clone.Calculate()
    yc.Apply(yc_clone)


    if regen_cpi == -1:
        if debug == 1:
            print 'reverting cpi bm entries and yc calc'        
        #for bmcpi in bm_pe:
        #    bmcpi.revert_apply()                
        bm_pe = update_cpi()  
        yc_cpi_clone.Calculate()
        yc_cpi.Apply(yc_cpi_clone)
        
#manually reverting bump to previously stressed level
    


#    if debug == 1:
#        print 'reverting fwd starting cpi index values'        
#    for cpiins in fwd_cpi_ins:
#        cpiins.revert_apply()        
        
#    print '%.0f' % (time.time() - t0) + 'sec - calculated bm delta for ', ins.insid

    return pv01

def basis_delta(sprd, stf, syc, *rest):
    t0 = time.time()
    
    sftsize = float(0.0001)
    
    ycb = ael.YieldCurve[syc]
    yc = ycb.underlying_yield_curve_seqnbr.clone()
    tf = ael.TradeFilter[stf]    

    if tf == None:
        print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
        return -99999999999.0

    pv0 = tf.present_value()
    
    sc = sprd.clone()
    sc.spread = sprd.spread + sftsize  
    sc.apply()   

    print sc.spread
    
    yc.calculate()
    yc.simulate()    


    pv1 = tf.present_value()
    pv01 = pv1 - pv0    
    
#manually revert bumped value
    sc.spread = sprd.spread - sftsize
    sc.apply()             

#    sc.revert_apply()
    yc.calculate()
    yc.simulate()

    print '%.0f' % (time.time() - t0) + 'sec - calculated bm delta for ', sprd.point_seqnbr.date_period
    
    return pv01
    
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
                log(1, mat, '%.2f' % ((cpiPrice - priEntityC.settle) * 100), '%.2f' % priEntityC.settle, '%.2f' % cpiPrice)
                priEntityC.last = cpiPrice
                priEntityC.settle = cpiPrice
                priEntityC.day = ael.date_today()
                priEntityC.apply()
                bm_pe.append(priEntityC)
    
    return bm_pe
    
def bm_maturity(ins, *rest):
    dte = ael.date_today()    
    return dte.add_period(ins.exp_period)
    
def sprd_point_maturity(point, *rest):    
    dte = ael.date_today()
    return dte.add_period(point.date_period)

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
