import ael, time

# ---------------------------------------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------------------------------------

debug = 1
g_regen_cpi = -1
cpi_curve = 'ZAR-CPI'
real_curve = 'ZAR-REAL'
nominal_curve = 'ZAR-SWAP'
sim_swap_basis = -1

# ---------------------------------------------------------------------------
# function used for logging output to the immediate window
# ---------------------------------------------------------------------------

def log(lvl, *out):
    t0 = time.ctime()
    
    s = ''
    
    if lvl == debug:
        for o in out:
            s = s + '\t' + str(o)
        
    print t0, s

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
                log(1, mat, '%.2f' % ((cpiPrice - priEntityC.settle) * 100), '%.2f' % priEntityC.settle, '%.2f' % cpiPrice)
                priEntityC.last = cpiPrice
                priEntityC.settle = cpiPrice
                priEntityC.day = ael.date_today()
                priEntityC.apply()
                bm_pe.append(priEntityC)
    
    return bm_pe
                

# ---------------------------------------------------------------------------
# regenerate cpi curve in simulated status only
# ---------------------------------------------------------------------------

def update_cpi_old():
    bm_pe = []
    cpiOff = ael.YieldCurve['ZAR-REAL'].clone()
    cpiSwap = ael.YieldCurve['ZAR-SWAP'].clone()
    cpiTest= ael.YieldCurve['ZAR-CPI'].clone()
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
            
        if debug == 2:
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
                priEntityC.apply()
                bm_pe.append(priEntityC)
                
        else:
            print 'No price entry found for cpi curve'
            
            """
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
            """
            
    return bm_pe

# ---------------------------------------------------------------------------
# returns the exp_day for a curve point
# ---------------------------------------------------------------------------

def sprd_point_maturity(point, *rest):    
    dte = ael.date_today()
    return dte.add_period(point.date_period)


# ---------------------------------------------------------------------------
# returns the exp_day for generic instruments
# ---------------------------------------------------------------------------

def bm_maturity(ins, *rest):
    dte = ael.date_today()
    return dte.add_period(ins.exp_period)

# ---------------------------------------------------------------------------
# calcs basis delta (for basis curves)
# ---------------------------------------------------------------------------

def basis_delta(sprd, stf, syc, *rest):
    t0 = time.time()
    
    ycb = ael.YieldCurve[syc]
    yc = ycb.underlying_yield_curve_seqnbr.clone()
    tf = ael.TradeFilter[stf]    

    if tf == None:
        print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
        return -99999999999.0

    pv0 = tf.present_value()
    
    sc = sprd.clone()
    sc.spread = sprd.spread + 0.0001    
    sc.apply()            
    
    yc.calculate()
    yc.simulate()    

    pv1 = tf.present_value()
    pv01 = pv1 - pv0    
    
    sc.revert_apply()
    yc.calculate()
    yc.simulate()

    print '%.0f' % (time.time() - t0) + 'sec - calculated bm delta for ', sprd.point_seqnbr.date_period
    
    return pv01

                
# ---------------------------------------------------------------------------
# calcs benchmark deltas
# ---------------------------------------------------------------------------

def bm_delta(ins, stf, syc, *rest):    
    t0 = time.time()
    
    if syc in (nominal_curve, real_curve):
        regen_cpi = g_regen_cpi
    else:
        regen_cpi = 0
        
    log(1, 'cpi regen set to : ', regen_cpi)
        
    if sim_swap_basis == -1 and syc == 'ZAR-SWAP-BASIS':
        if debug == 1:
            print 'ignoring curve : ZAR-SWAP-BASIS'
            
        return 0.0
    
    if debug == 1:
        print ''
        print 'running bm delta', 'yc', syc, 'ins', ins.insid, 'tf', stf
    
    if syc == 'ZAR-SWAP' and sim_swap_basis == -1:
        yc_sb = ael.YieldCurve['ZAR-SWAP-BASIS'].clone()
        
    yc = ael.YieldCurve[syc].clone()
    yc_cpi = ael.YieldCurve[cpi_curve].clone()
    tf = ael.TradeFilter[stf]    

    if tf == None:
        print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
        return -99999999999.0
    
    if debug == 2:
        print 'original curve'
        print yc.pp()
        print ''
        
    if debug == 1:
        print 'calling present_value() function'    
    pv0 = tf.present_value()
    
    prc = ins.prices()            
    
    for p in prc:
        #print p.day, p.ptynbr.ptyid, p.settle
        if p.ptynbr.ptyid == 'SPOT':
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
        
    yc.calculate()
    yc.simulate()    

    if syc == 'ZAR-SWAP' and sim_swap_basis == -1:        
        print 'Simulating ZAR-SWAP-BASIS'
        yc_sb.calculate()
        yc_sb.simulate()    
    
    if regen_cpi == -1:
        if debug == 1:
            print 'calling cpi bm update function'            
        bm_pe = update_cpi()

        if debug == 1:
            print 'simulating cpi curve'
        
        yc_cpi.calculate()
        yc_cpi.simulate()
        
    if debug == 2:
        print 'modified curve'
        print yc.pp()
        print ''
        
    if debug == 1:
        print 'calculating bumped pv value'    
    
    pv1 = tf.present_value()
    pv01 = pv1 - pv0
    
    if debug == 1:
        print ins.insid, pv0, pv1, pv01        
        
    if debug == 1:
        print 'reverting bm entries and yc calc'

    pc.revert_apply()
    yc.calculate()
    yc.simulate()

    if syc == 'ZAR-SWAP' and sim_swap_basis == -1:
        yc_sb.calculate()
        yc_sb.simulate()    
    
    if regen_cpi == -1:
        if debug == 1:
            print 'reverting cpi bm entries and yc calc'        
        for bmcpi in bm_pe:
            bmcpi.revert_apply()        
        
        yc_cpi.calculate()
        yc_cpi.simulate()
        
    print '%.0f' % (time.time() - t0) + 'sec - calculated bm delta for ', ins.insid
    
    return pv01

# ---------------------------------------------------------------------------
# calcs fx exposure from PV
# ---------------------------------------------------------------------------

def fx_exposure_pv(ins, stf, *rest):    
    ccy = ins.insid

    dt = ael.date_today()
    bdt = ael.date('2099-01-01')
    
    tf = ael.TradeFilter[stf]    
    
    pv = tf.present_value(dt, bdt, bdt, ccy)    
    
    pv01 = pv * 0.01    

    if debug == -1:
        print ccy, pv, pv01  
    
    return pv01

# ---------------------------------------------------------------------------
# calcs fx exposure from CASH
# ---------------------------------------------------------------------------
    
def fx_exposure_cash(ins, stf, *rest):    
    ccy = ins.insid

    dt = ael.date_today()
    ye = dt.first_day_of_year().add_days(-1)
    
    tf = ael.TradeFilter[stf]    
    
    cash_ye = tf.accumulated_cash(ye, ccy)
    cash_t = tf.accumulated_cash(dt, ccy)
    cash = cash_t - cash_ye
    
    pv01 = cash * 0.01    

    if debug == -1:
        print ccy, 'cash_ye:', cash_ye, 'cash_today:', cash_t, cash, pv01    
    
    return pv01

"""
sf = 'Dirk_tmp'
bm = ael.Instrument['ZAR/FRA/JI/3X6']
sy = 'ZAR-SWAP'

print bm_delta(sf, sy, bm)
"""

# ---------------------------------------------------------------------------
# returns current nominal as per cash glow table
# ---------------------------------------------------------------------------

def current_nominal_leg(leg, rep_dte, *rest):    
    #print 'nominal for leg', leg.legnbr, 'date', rep_dte
    dt = ael.date(rep_dte)    
    
    curr_nom = 0.0
    
    cfs = leg.cash_flows()
    for cf in cfs:
        if cf.pay_day >= dt:
            curr_nom = cf.nominal_amount()
            break

    return curr_nom

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# used to copy all price entries from spot to the price test market
# ---------------------------------------------------------------------------

def Copy_PT_Prices():
    pt_mkt = 'PRICETEST'
    pt_pty = ael.Party[pt_mkt].ptynbr
    
    dt = ael.date_today()
    inslst = []
    inslst.append(ael.Instrument['ZAR/AGL'])
    k = 0
    
    for ins in inslst: #ael.Instrument:
        k=k+1
        print 'checking instr ' + str(k)
        
        prcs = ins.prices()    
        #delete
        for p in prcs:        
            try:            
                if p.ptynbr.ptyid == pt_mkt:
                    print 'deleting - ', p.insaddr.instype, p.insaddr.insid, p.curr.insid, p.day
                    p.delete()
            except:
                print 'invalid price entry - not linked to market', p.insaddr.instype, p.insaddr.insid
        
        prcs = ins.prices()
        #insert new
        for p in prcs:
            try:
                if p.ptynbr.ptyid == 'SPOT':
                    print 'cloning - ', p.insaddr.instype, p.insaddr.insid, p.curr.insid, p.day
                    np = p.new()
                    np.ptynbr = pt_pty
                    np.day = dt
                try:
                    np.commit()
                except:
                    print 'commit failed for Ins ', p.insaddr.insid, 'Curr', p.curr.insid, 'Type ', p.insaddr.instype
            except:
                print 'invalid price entry - not linked to market', p.insaddr.instype, p.insaddr.insid


