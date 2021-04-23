'''
Date                    : 03/05/2010  
Purpose                 : Contains functions used for various other scripts, Made changes to lines 275 and 358 by keeping only the else statement logic
Department and Desk     : Middle Office, Middle Office
Requester               : Dirk Strauss, Hendrik Jansen Van Rensburg
Developer               : Dirk Strauss, Bhavnisha Sarawan
CR Number               : 306264, C614889

Date            Developer               Change
2010-12-09      Paul Jacot-Guillarmod   521283: bm_delta updated to simulate fixing on TRS's on bonds
'''

import ael, time, acm
import SAFI_BOND_TRS

# ---------------------------------------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------------------------------------

debug = 1
g_regen_cpi = -1
cpi_curve = 'ZAR-CPI'
real_curve = 'ZAR-REAL'
nominal_curve = 'ZAR-SWAP'

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
# function used for testing whether a variable is numeric
# ---------------------------------------------------------------------------

def is_num(n):
    return type(n) in (int, long, float, complex) 


# ---------------------------------------------------------------------------
# pv01 for bonds / futures
# ---------------------------------------------------------------------------

def nonotc_delta(pins):
    ins = pins[0][0]
    if ins.instype in ('Bond', 'IndexLinkedBond'):
        yld = ins.used_price()
        bump = 0.005
        pv_u = ins.dirty_from_yield(None, None, None, yld + bump) * 10000
        pv_d = ins.dirty_from_yield(None, None, None, yld - bump) * 10000
        pv01 = (pv_u - pv_d) / (2 * bump) / 100
    elif ins.instype == 'Future/Forward' and ins.und_insaddr.insid == 'USD-LIBOR-3M':
        pv01 = 25.0
    else:
        pv01 = -9.999
        
    return pv01
   
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
            if l.nominal_scaling == 'CPI' or l.nominal_scaling == 'CPI Fixing In Arrears':
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
# returns the exp_day for a curve / vol point
# ---------------------------------------------------------------------------

def sprd_point_maturity(point, *rest):    
    dte = ael.date_today()
    return dte.add_period(point.date_period)

def vol_point_expiry(point, *rest):    
    dte = ael.date_today()
    return dte.add_period(point.exp_period)

def vol_point_maturity(point, *rest):    
    dte = ael.date_today()
    return dte.add_period(point.undmat_period)
    
def vol_point_maturity_str(point, *rest):        
    dte = ael.date_today()
    mat = dte.add_period(point.undmat_period).to_string('%y%m%d')
    return mat + '_' + point.undmat_period

def vol_point_expiry_str(point, *rest):        
    dte = ael.date_today()
    exp = dte.add_period(point.exp_period).to_string('%y%m%d')

    return exp + '_' + point.exp_period

# ---------------------------------------------------------------------------
# returns the exp_day for generic instruments
# ---------------------------------------------------------------------------

def bm_maturity(ins, *rest):
    dte = ael.date_today()    
    return dte.add_period(ins.exp_period)

# ---------------------------------------------------------------------------
# calcs bm vega
# ---------------------------------------------------------------------------

def bm_vega(pnt, stf, svol, *rest):
    vol = ael.Volatility[svol].clone()
    tf = ael.TradeFilter[stf]
    pnt_c = pnt.clone()
    
    print '\nrunning for ', pnt.exp_period, pnt.undmat_period, pnt.strike
    
    pv0 = tf.present_value()
    pnt_c.volatility = pnt_c.volatility + 0.01
    pnt_c.apply()
    pv1 = tf.present_value()
    pnt_c.revert_apply()    
    
    return pv1 - pv0

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
    
#manually revert bumped value
    sc.spread = sprd.spread - 0.0001
    sc.apply()             

#    sc.revert_apply()
    yc.calculate()
    yc.simulate()

    print '%.0f' % (time.time() - t0) + 'sec - calculated bm delta for ', sprd.point_seqnbr.date_period
    
    return pv01

                
# ---------------------------------------------------------------------------
# calcs benchmark deltas
# ---------------------------------------------------------------------------

def bm_delta(ins, stf, syc, bond_trs=0, *rest):
    ''' If bond_trs=1 then a function will be called to simulate a
        fixing on TRS's on bonds.
    '''
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
    
    yc = ael.YieldCurve[syc].clone()
    yc_cpi = ael.YieldCurve[cpi_curve].clone()
    tf = ael.TradeFilter[stf]    

    yc.calculate()
    yc.simulate()    

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
    
    print pv0
    
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
    
    if regen_cpi == -1:
        if debug == 1:
            print 'calling cpi bm update function'            
        bm_pe = update_cpi()        

        if debug == 1:
            print 'simulating cpi curve'
        
        yc_cpi.calculate()
        yc_cpi.simulate()
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
    
    print pv1
    pv01 = pv1 - pv0
    
    if debug == 1:
        print ins.insid, pv0, pv1, pv01        
        
    if debug == 1:
        print 'reverting bm entries and yc calc'

#manually reverting bump to previously stressed level
    for p in prc:

        if p.ptynbr.ptyid == 'SPOT':
                
            pc = p.clone()
            
            pc.settle = p.settle - 0.01
            pc.last = p.last - 0.01
            pc.bid = p.bid - 0.01
            pc.ask = p.ask - 0.01
            pc.apply()   
            
#end

#    pc.revert_apply()
    yc.calculate()
    yc.simulate()


    if regen_cpi == -1:
        if debug == 1:
            print 'reverting cpi bm entries and yc calc'        
        #for bmcpi in bm_pe:
        #    bmcpi.revert_apply()                
        bm_pe = update_cpi()  
        yc_cpi.calculate()
        yc_cpi.simulate()        
        
#manually reverting bump to previously stressed level
    


#    if debug == 1:
#        print 'reverting fwd starting cpi index values'        
#    for cpiins in fwd_cpi_ins:
#        cpiins.revert_apply()        
        
#    print '%.0f' % (time.time() - t0) + 'sec - calculated bm delta for ', ins.insid

    return pv01

# ---------------------------------------------------------------------------
# calcs fx exposure from PV
# ---------------------------------------------------------------------------

def fx_exposure_pv(ins, stf, *rest):    
    ccy = ins.insid
    bRun = 0
    
    dt = ael.date_today()
    bdt = ael.date('2099-01-01')
    
    tf = ael.TradeFilter[stf]    
    
    for trd in tf.trades():
        if trd.currency_included(ccy) == 1:
            bRun = 1
            break
    
    if bRun == 1:
        pv = tf.present_value(dt, bdt, bdt, ccy)    
    
        pv01 = pv * 0.01    

        if debug == -1:
            print ccy, pv, pv01  
    else:
        pv01 = 0.0
        
    return pv01

# ---------------------------------------------------------------------------
# calcs fx exposure from CASH
# ---------------------------------------------------------------------------
    
def fx_exposure_cash(ins, stf, *rest): 
    ccy = ins.insid
    bRun = 0
    
    dt = ael.date_today()
    ye = dt.first_day_of_year().add_days(-1)
    
    tf = ael.TradeFilter[stf]    
    
    for trd in tf.trades():
        if trd.currency_included(ccy) == 1:
            bRun = 1
            break

    if bRun == 1:
        cash_ye = 0.0 #tf.accumulated_cash(ye, ccy)
        cash_t = tf.accumulated_cash(dt, ccy)
        cash = cash_t - cash_ye
        
        pv01 = cash * 0.01    
    
        if debug == -1:
            print ccy, 'cash_ye:', cash_ye, 'cash_today:', cash_t, cash, pv01    
        
        return pv01
    else:
        return 0.0
        
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
# Used to run trade level bm deltas
# ---------------------------------------------------------------------------

def trade_lvl_bm():
    # parameters
    stf = 'STIRT_FRA_TRADING'    
    sycs = ['USD-SWAP']    
    sfile = 'c:\\temp\\test.xls'
    
    f=open(sfile, 'w')
    
    t0 = time.time()
    
    tf = ael.TradeFilter[stf]    
    
    if debug == 2:
        print 'original curve'
        print yc.pp()
        print ''
    
    # create dictionary
    d = {}
    
    # add headers
    d['trade'] = []
    d['trade'].append('InsType')
    d['trade'].append('Curr')
    d['trade'].append('PV')
    
    # add header row for curve name
    d['curve'] = []
    d['curve'].append('')
    d['curve'].append('')
    d['curve'].append('')    
    
    bms = []
    
    for syc in sycs:    
        yc = ael.YieldCurve[syc].clone()        
        
        for bm in yc.benchmarks():
            ins = bm.instrument
            mat = bm_maturity(ins)
            tpl = (syc, mat, ins)
            bms.append(tpl)
    
    bms.sort()
    
    for bm in bms:
        ins = bm[2]
        d['trade'].append(ins.insid)
        d['curve'].append(bm[0])
    
    fxrt = {}
    
    for trd in tf.trades():    
        if trd.insaddr.exp_day > ael.date_today():
            ccy = trd.curr.insid
            if ccy not in fxrt.keys():
                fxrt[ccy] = get_fx_rate([[ccy]])
            
            pv0 = trd.present_value() * fxrt[ccy]
            
            d[trd.trdnbr] = []
            d[trd.trdnbr].append(trd.insaddr.instype)
            d[trd.trdnbr].append(trd.curr.insid)
            d[trd.trdnbr].append(pv0)    
    
    for k in fxrt.keys():
        print k, fxrt[k]
        
    for bm in bms:
        ins = bm[2]
        prc = ins.prices()            
        yc = ael.YieldCurve[bm[0]].clone()
        
        print 'bumping bm - ', ins.insid

        for p in prc:
            #print p.day, p.ptynbr.ptyid, p.settle
            if p.ptynbr.ptyid == 'SPOT':
                if debug == 2:
                    print 'found price'
                    print p.pp()
                    print ''
                    
                pc = p.clone()
                pc.settle = p.settle + 0.01
                pc.last = p.last + 0.01
                pc.bid = p.bid + 0.01
                pc.ask = p.ask + 0.01
                pc.apply()   
                
                if debug == 2:
                    print 'cloned point'
                    print pc.pp()
                    print ''
                    
        yc.calculate()
        yc.simulate()            

        if debug == 2:
            print 'modified curve'
            print yc.pp()
            print ''
            
        for trdnbr in d.keys():    
            if is_num(trdnbr):
                trd = ael.Trade[trdnbr]
                ccy = d[trd.trdnbr][1]
                fx = fxrt[ccy]
                pv0 = d[trd.trdnbr][2]
                pv1 = trd.present_value() * fx
                pv01 = pv1 - pv0
                d[trd.trdnbr].append(pv01)
        
                if debug == 1:
                    print trd.trdnbr, ccy, fxrt[ccy], pv0, pv1, pv01            
        
        if debug == 1:
            print ''
        
        pc.revert_apply()
        yc.calculate()
        yc.simulate()
    
    # write curve headers
    ls = d['curve']
    s = ''    
    for l in ls:        
        s = s + '\t' + str(l)
    
    s = s + '\n'
    f.write(s)

    # write trade headers    
    ls = d['trade']
    s = 'trade'    
    for l in ls:        
        s = s + '\t' + str(l)
    
    s = s + '\n'
    f.write(s)
    
    keys = d.keys()
    
    for key in keys:
        if key <> 'trade' and key <> 'curve':
            ls = d[key]
            s = str(key)
            k = 0
            for l in ls:        
                s = s + '\t' + str(l)
            
            s = s + '\n'
            f.write(s)
    
    f.close()
            
    print 'Done', '%.0f' % (time.time() - t0) + 'sec'


# ---------------------------------------------------------------------------
# returns the fx rate
# ccy is a list that can contain 1 or 2 parameters
# if ccy only contains one parameter then the base ccy is assumed to be ZAR
# if ccy contains 2 paramaters then the first entry will be taken as the base ccy
# ---------------------------------------------------------------------------

def get_fx_rate(ccy):
    if len(ccy[0]) == 1:
        hccy = 'ZAR'
        fccy = ccy[0][0]
    elif len(ccy[0]) == 2:
        hccy = ccy[0][0]
        fccy = ccy[0][1]
    else:
        return 0.0

    if fccy == hccy:
        return 1.0

    curr_base = ael.Instrument[hccy] 
    curr = ael.Instrument[fccy]    

    dt = ael.date_today()

    d = 1.0/curr_base.used_price(dt, curr.insid)

    return d

# ---------------------------------------------------------------------------
# Used to get bond bm deltas for a given tradefilter
# ---------------------------------------------------------------------------

def Bond_BM_delta(ins, stf, *rest):    
    tf = ael.TradeFilter[stf]
    
    res = {}
    
    pv_base = 0.0
    for t in tf.trades():
        pv_trd = t.mtm_value_fo()
        res[t.trdnbr] = [pv_trd]
        pv_base = pv_base + pv_trd

    prc = ins.prices()            
    
    for p in prc:
        #print p.day, p.ptynbr.ptyid, p.settle
        if p.ptynbr.ptyid == 'SPOT':
            if debug == 2:
                print 'found price'
                print p.pp()
                print ''
                
            pc = p.clone()                
            
            pc.settle = p.settle + 0.01
            pc.last = p.last + 0.01
            pc.bid = p.bid + 0.01
            pc.ask = p.ask + 0.01
            pc.apply()   

            break
            

    pv_up = 0.0
    for t in tf.trades():
        pv_trd = t.mtm_value_fo()
        res[t.trdnbr].append(pv_trd)
        pv_up = pv_up + pv_trd

    pc.revert_apply()
    
    """
    for k in res.keys():
        if res[k][1] - res[k][0] <> 0.0:
            print k, res[k][0], res[k][1], res[k][1] - res[k][0]
    """
    
    return pv_up - pv_base

# ---------------------------------------------------------------------------
# Used to get bond bm deltas for a given bond
# ---------------------------------------------------------------------------
    
def Bond_BM_delta_ins(ins, *rest):    
    pv_base = ins.mtm_value_fo()
        
    prc = ins.prices()            
    
    for p in prc:
        #print p.day, p.ptynbr.ptyid, p.settle
        if p.ptynbr.ptyid == 'SPOT':
            if debug == 2:
                print 'found price'
                print p.pp()
                print ''
                
            pc = p.clone()                
            
            pc.settle = p.settle + 0.01
            pc.last = p.last + 0.01
            pc.bid = p.bid + 0.01
            pc.ask = p.ask + 0.01
            pc.apply()   

            break
            
    pv_up = ins.mtm_value_fo()

    pc.revert_apply()    
    
    return pv_up - pv_base


# ---------------------------------------------------------------------------
# Used to get bond bm deltas for a given tradefilter - trading manager / prime vals
# ---------------------------------------------------------------------------
def Bond_BM_delta_acm(ins, stf, *rest):    

    context     = 'Standard'    
    portfolio   = acm.FTradeSelection[stf]
     
    calc_space  = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')
    value   	= calc_space.CalculateValue(portfolio, 'Portfolio Value End')
    pv_base	= value.Value().Number()

    prc         = ins.prices()            
    
    for p in prc:
        #print p.day, p.ptynbr.ptyid, p.settle
        if p.ptynbr.ptyid == 'SPOT':
            if debug == 2:
                print 'found price'
                print p.pp()
                print ''
                
            pc = p.clone()                
            
            pc.settle = p.settle + 0.01
            pc.last = p.last + 0.01
            pc.bid = p.bid + 0.01
            pc.ask = p.ask + 0.01
            pc.apply()   

            break
    
    value = calc_space.CalculateValue(portfolio, 'Portfolio Value End')
    pv_up = value.Value().Number()

    pc.revert_apply()    
    
    return pv_up - pv_base


# ---------------------------------------------------------------------------
# Used to get bond bm deltas for a given bond using core acm
# ---------------------------------------------------------------------------
    
def Bond_BM_delta_ins_acm(ins, *rest):
    context     = 'Standard'   
    fins = acm.FInstrument[ins.insid] 
    
    calc_space  = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')
    value   	= calc_space.CalculateValue(fins, 'Portfolio Value End')
    pv_base	= value.Value().Number()
    
    prc = ins.prices()            
    
    for p in prc:
        #print p.day, p.ptynbr.ptyid, p.settle
        if p.ptynbr.ptyid == 'SPOT':
            if debug == 2:
                print 'found price'
                print p.pp()
                print ''
                
            pc = p.clone()                
            
            pc.settle = p.settle + 0.01
            pc.last = p.last + 0.01
            pc.bid = p.bid + 0.01
            pc.ask = p.ask + 0.01
            pc.apply()   

            break

    value   	= calc_space.CalculateValue(fins, 'Portfolio Value End')
    pv_up	= value.Value().Number()

    pc.revert_apply()    
    
    return pv_up - pv_base


# ---------------------------------------------------------------------------
# Recalc and simulate yc
# ---------------------------------------------------------------------------

def recalc_yc_sim(yc, *rest):    
    try:
        ycc = yc.clone()
        ycc.calculate()
        ycc.simulate()
        ret = 'ok'
    except:
        ret = 'failed'
    
    return ret

# ---------------------------------------------------------------------------
# get acm pv for a trade filter
# ---------------------------------------------------------------------------

def pv_tf_acm(stf):

    context     = 'Standard'    
    portfolio   = acm.FTradeSelection[stf]
    calc_space  = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')
    value   	= calc_space.CalculateValue(portfolio, 'Portfolio Value End')
    pv	        = value.Value().Number()
    return pv

# ---------------------------------------------------------------------------
# get acm pv for a trade
# ---------------------------------------------------------------------------
def pv_trd_acm(trd):

    context             = 'Standard'    
    calc_space          = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')
    value   		= calc_space.CalculateValue(trd, 'Portfolio Value End')
    pv			= value.Value().Number()
    return pv

# ---------------------------------------------------------------------------
# calcs benchmark deltas using core valuation framwork
# ---------------------------------------------------------------------------

def bm_delta_acm(ins, stf, syc, *rest):    
    t0 = time.time()
    
    if syc in (nominal_curve, real_curve):
        regen_cpi = g_regen_cpi
    else:
        regen_cpi = 0
        
    log(1, 'cpi regen set to : ', regen_cpi)        
    
    if debug == 1:
        print ''
        print 'running bm delta', 'yc', syc, 'ins', ins.insid, 'tf', stf    
        
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
    pv0 = pv_tf_acm(stf)
    
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
    
    pv1 = pv_tf_acm(stf)
    pv01 = pv1 - pv0
    
    if debug == 1:
        print ins.insid, pv0, pv1, pv01        
        
    if debug == 1:
        print 'reverting bm entries and yc calc'

    pc.revert_apply()
    yc.calculate()
    yc.simulate()
    
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
# get strike for vol bm
# ---------------------------------------------------------------------------

def vol_bm_strike(ins, *rest):   

    if ins.instype == 'Cap':
        strike = ins.legs()[0].strike
    elif ins.instype == 'Option':
        strike = ins.strike_price
    else:
        strike = 0.0
        
    return strike
    
# ---------------------------------------------------------------------------
# get maturity for vol bm
# retflag ==>  0 : yymmdd_mat, 1 : date, 2 : mat
# ---------------------------------------------------------------------------

def vol_bm_mat(ins, retflag, *rest):
    dt = ael.date_today()
    
    if ins.instype == 'Cap':
        per = ins.legs()[0].rolling_period
    elif ins.instype == 'Option':
        per = ins.und_insaddr.legs()[0].end_period
    else:
        per = ''
        
    if per == '':
        return ael.date('1899-12-31').to_string('%y%m%d') + '_0d'
    else:
        if retflag == 0:
            return dt.add_period(per).to_string('%y%m%d') + '_' + per
        elif retflag == 1:
            return dt.add_period(per)
        elif retflag == 2:
            return per

# ---------------------------------------------------------------------------
# get expiry for vol bm
# retflag ==>  0 : yymmdd_mat, 1 : date, 2 : mat
# ---------------------------------------------------------------------------

def vol_bm_exp(ins, retflag, *rest):
    dt = ael.date_today()
    
    if ins.instype == 'Cap':
        per = ins.legs()[0].end_period        
    elif ins.instype == 'Option':
        per = ins.exp_period
    else:
        per = ''
        
    if per == '':
        return ael.date('1899-12-31').to_string('%y%m%d') + '_0d'
    else:
        if retflag == 0:
            return dt.add_period(per).to_string('%y%m%d') + '_' + per
        elif retflag == 1:
            return dt.add_period(per)
        elif retflag == 2:
            return per

# ---------------------------------------------------------------------------
# used to move trades to expired deals port
# gets trade list from c:\temp\exp.txt
# ---------------------------------------------------------------------------

def trade_aggr():
    new_port_id = 'IRD_EXPIRED_TRADES'
    new_port = ael.Portfolio[new_port_id]
    
    sfile = 'c:\\temp\\exp.txt'
    
    f = open(sfile, 'r')
    
    s = f.readline()
    
    while s <> '':    
        trdnbr = int(s)
        trd = ael.Trade[trdnbr]
        port = trd.prfnbr.prfid
        print 'changing trade', trd.trdnbr, port
        if trd.prfnbr <> new_port:
            ctrd = trd.clone()
            ctrd.prfnbr = new_port
            ctrd.commit()
            trd = ael.Trade[trdnbr]
            print 'changed', trdnbr, trd.prfnbr.prfid
        else:
            print 'trade already changed'
        
        print ''
        s = f.readline()
    
    f.close()

# ---------------------------------------------------------------------------
# calcs benchmark gammas
# ---------------------------------------------------------------------------

def bm_gamma(ins, stf, syc, *rest):    
    t0 = time.time()
    
    print ''
    pv = {}
    
    if syc in (nominal_curve, real_curve):
        regen_cpi = g_regen_cpi
        yc_nom = ael.YieldCurve[nominal_curve].clone()
        print 'Calculating :', nominal_curve
        yc_nom.calculate()
        yc_nom.simulate()    
    else:
        regen_cpi = 0
    
    log(1, 'cpi regen set to : ', regen_cpi)        
    
    if debug == 1:        
        print 'running bm gamma', 'yc', syc, 'ins', ins.insid, 'tf', stf    
       
    yc = ael.YieldCurve[syc].clone()
    yc_cpi = ael.YieldCurve[cpi_curve].clone()
    tf = ael.TradeFilter[stf]    

    yc.calculate()
    yc.simulate()    

    if tf == None:
        print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
        return -99999999999.0
    
    if debug == 2:
        print 'original curve'
        print yc.pp()
        print ''
        
    if debug == 1:
        print 'calling present_value() function'    
    pv[0] = tf.present_value()
    
    prc = ins.prices()            
        
    for k in range(1, 3):
        bump = 0.01 * k
        print '\nbumping by', bump
        for p in prc:
            #print p.day, p.ptynbr.ptyid, p.settle
            if p.ptynbr.ptyid == 'SPOT':
                if debug == 2:
                    print 'found price'
                    print p.pp()
                    print ''
                    
                pc = p.clone()                
                log(1, 'changing point from', pc.settle, 'to', pc.settle + bump)
                
                pc.settle = p.settle + bump
                pc.last = p.last + bump
                pc.bid = p.bid + bump
                pc.ask = p.ask + bump
                pc.apply()   
                
                if debug == 2:
                    print 'cloned point'
                    print pc.pp()
                    print ''
        
        if debug == 1:
            print 'simulating', syc
            
        yc.calculate()
        yc.simulate()        
        
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
        
        pv[k] = tf.present_value()                
            
        if debug == 1:
            print 'reverting bm entries and yc calc'
    
        pc.revert_apply()
        yc.calculate()
        yc.simulate()    
        
        if regen_cpi == -1:
            if debug == 1:
                print 'reverting cpi bm entries and yc calc'        
            for bmcpi in bm_pe:
                bmcpi.revert_apply()        
            
            yc_cpi.calculate()
            yc_cpi.simulate()
            
        print '%.0f' % (time.time() - t0) + 'sec - calculated bm delta for ', ins.insid
    
    pv01 = (pv[2] - pv[1]) - (pv[1] - pv[0])
    
    if debug == 1:
        print ins.insid, pv[0], pv[1], pv[2], pv01

    return pv01

# ---------------------------------------------------------------------------
# function to return business days between 2 dates
# ---------------------------------------------------------------------------

def get_biz_days(parm):
    p = parm[0]
    
    d1 = parm[0][0]    
    
    if len(p) > 1:
        d2 = p[1]
    else:
        d2 = ael.date_today()

    days = d2.bankingdays_between(d1, ael.Instrument['ZAR'])

    return days
