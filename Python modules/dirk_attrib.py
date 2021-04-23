import ael

DEBUG = -1
HIST_MODE = 0

def GenBckts(series):
    
    b = []
    
    if series == 0:
        b.append('0d')
        b.append('1d')
        b.append('1m')
        b.append('3m')
        b.append('6m')
        b.append('9m')
        b.append('1y')
        b.append('15m')
        b.append('18m')
        b.append('21m')
        b.append('2y')
        b.append('3y')
        b.append('4y')
        b.append('5y')
        b.append('6y')            
    elif series == 1:
        b.append('5y')
        b.append('6y')
        b.append('7y')
        b.append('8y')
        b.append('9y')
        b.append('10y')
        b.append('12y')
        b.append('15y')
        b.append('20y')
        b.append('25y')
        b.append('30y')
        b.append('35y')
        b.append('100y')
        """b.append('6y')
        b.append('78m')
        b.append('7y')
        b.append('90m')
        b.append('8y')
        b.append('102m')
        """
    
    return b

# ==================================================================================

def GetVols(ins, *rest):

    vols = []
    t_vols = ins.used_volatilities()
    
    for t_vol in t_vols:        
        vol = t_vol[1]        
        if InList(vols, vol) == 0:
            vols.append(vol)
    
    return vols
    
# ==================================================================================

def GetCurves(ins, *rest):

    curves = []
    ycs = ins.used_yield_curves()
    
    for yc in ycs:        
        curve = yc[1]        
        if InList(curves, curve) == 0:
            curves.append(curve)
    
    return curves

# ==================================================================================

def GetCcys(trd, *rest):
    
    all_ccys = ael.Instrument.select('instype="curr"')
    ccys = []
    
    if DEBUG <> 0:
        print('-----------------------GetCcys----------------------------')
        
    for ccy in all_ccys:
        if DEBUG <> 0:
            print('checking ccy : ', ccy.insid)
        
        if trd.currency_included(ccy.insid) == 1:
            ccys.append(ccy.insid)
            if DEBUG <> 0:                
                print('Added ccy : ', ccy.insid)
                print('--------------')
    
    """ccys = []
    ycs = ins.used_yield_curves()
    
    for yc in ycs:        
        curve = yc[1]                
        ccy = ael.YieldCurve[curve].curr.insid
        if InList(ccys, ccy) == 0:
            ccys.append(ccy)
    """
    
    return ccys

# ==================================================================================
    
def InList(lst, val, *rest):
    
    for x in lst:
        if x == val:
            return -1
    
    return 0

# ==================================================================================

def cash_mv(trd, d0, d1, ccys, *rest):
    legs = trd.insaddr.legs()
    
    zar = ael.Instrument['ZAR']
    d0 = ael.date_today()
    d1 = d0.add_banking_day(zar, 1)

    cash = 0.0
    fx1 = 0.0
    
    if DEBUG <> 0:
        print('-----------------------cash drop----------------------------')
        print(ccys)
            
    for ccy in ccys:
        if ccy <> 'ZAR':
            fx1 = 1 / ael.Instrument['ZAR'].mtm_price(d1, ccy)
            
            cash0 = trd.accumulated_cash(d0, ccy, 2, 0, '', 1, 'None') * fx1
            cash1 = trd.accumulated_cash(d1, ccy, 2, 0, '', 1, 'None') * fx1
        else:
            cash0 = trd.accumulated_cash(d0, ccy, 2, 0, '', 1, 'None')
            cash1 = trd.accumulated_cash(d1, ccy, 2, 0, '', 1, 'None')
            
        if DEBUG <> 0:            
            print('ccy : ' + ccy)
            print(cash0, cash1, fx1)
            print('---------------------')
            
        cash = cash + cash1 - cash0
            
    return cash

# ==================================================================================

def fx_delta(trd, d0, d1, *rest):
    legs = trd.insaddr.legs()
    
    zar = ael.Instrument['ZAR']
    d0 = ael.date_today()
    d1 = d0.add_banking_day(zar, 1)
    
    fx_pnl = 0.0
    
    if DEBUG <> 0:
        print('-----------------------fx pnl----------------------------')        
        
    for leg in legs:
        ccy = leg.curr.insid
        
        if ccy <> 'ZAR':
            fx0 = 1 / ael.Instrument['ZAR'].mtm_price(d0, ccy)    
            fx1 = 1 / ael.Instrument['ZAR'].mtm_price(d1, ccy)    
            #pv = trd.mtm_value_fo(d0, ccy, 2, 0, 1)
            pv = leg.present_value()
            cash = trd.accumulated_cash(d0, ccy, 2, 0, '', 1, 'None')
            
            fx_pnl = fx_pnl + ((pv + cash) * (fx1 - fx0))            
            
            if DEBUG <> 0:            
                print('ccy : ' + ccy)
                print('fx_0: %.8f' % fx0, 'fx_1: %.8f' % fx1)
                print('pv: %.0f' % pv, 'cash: %.0f' % cash, 'net: %.0f' % (pv + cash))
                print('pnl: %.0f' % fx_pnl)
            
    return fx_pnl
            
# ==================================================================================

def bm_delta(trd, yc_0, yc_1, *rest):
    dt = ael.date_today()    
    zar = ael.Instrument['ZAR']    
    dt_tom = dt.add_banking_day(zar, 1)

    yc0 = ael.YieldCurve[yc_0]
    yc1 = ael.YieldCurve[yc_1]
    
    ccy = yc0.curr.insid
    fx = 1 / ael.Instrument['ZAR'].mtm_price(dt, ccy)    
    
    if DEBUG <> 0:
        print('---------------delta pnl------------------------')
        print('crv1', yc_0, 'crv2', yc_1)    
        print(trd.trdnbr)
    
    delta = []
    Rate_0 = []
    Rate_1 = []
    pnl = []
    tot_pnl = 0.0
    
    for series in range(0, 2):
        bckts = GenBckts(series)
        
        cnt = len(bckts)-1
        
        for k in range(1, cnt):
            d1 = dt.add_period(bckts[k])
            
            if trd.maturity_date() > dt:
                dDelta = trd.risk('Delta', '', 2, yc_0, '', '', k+1, *bckts)
                #dDelta = trd.delta_curve(ccy, 0, yc_0,'' ,'' ,-1, 0.01, 'Annual Comp', 'Act/365', 'Spot Rate','' , d0, d1, d2, '', '', '')
                dRate_0 = yc0.yc_rate(dt, d1, 'Annual Comp', 'Act/365', 'Spot Rate', 0, 'ZAR')*100
                dRate_1 = yc1.yc_rate(dt_tom, d1.add_banking_day(zar, 1), 'Annual Comp', 'Act/365', 'Spot Rate', 0, 'ZAR')*100
                dPnL = - dDelta * (dRate_1 - dRate_0) * 100
                
                delta.append(dDelta)
                Rate_0.append(dRate_0)
                Rate_1.append(dRate_1)
                pnl.append(dPnL)
                tot_pnl = tot_pnl + dPnL
                
                if DEBUG <> 0:
                    print(bckts[k], 'delta: %.0f' % dDelta, 'r0: %.2f' % dRate_0, 'r1: %.2f' % dRate_1, (dRate_1 - dRate_0) * 100, 'pnl: %.0f' % dPnL)            
    
    return tot_pnl

# ===========================================================================
# ===========================================================================
# ===========================================================================

def theta_trd(t, *rest):    
    zar = ael.Instrument['ZAR']
    d0 = ael.date_today()
    d1 = d0.add_banking_day(zar, 1)
    
    trddte = ael.date_from_time(t.execution_time)
    
    if trddte == d1:        
        theta = 0.0
    else:        
        theta = t.theta() * d0.days_between(d1)
    
    return theta

# ---------------------------------------------------------------------------

def is_new_deal_trd(t, *rest):
    zar = ael.Instrument['ZAR']
    d0 = ael.date_today()
    d1 = d0.add_banking_day(zar, 1)
    
    trddte = ael.date_from_time(t.execution_time)
    
    if trddte == d1:        
        new_dl = -1
    else:        
        new_dl = 0
    
    return new_dl

# ---------------------------------------------------------------------------

def cash_drop_trd(t, *rest):    
    zar = ael.Instrument['ZAR']
    d0 = ael.date_today()
    d1 = d0.add_banking_day(zar, 1)

    trddte = ael.date_from_time(t.execution_time)
    
    if trddte == d1:        
        return 0.0    

    ccys = GetCcys(t)
    cash = cash_mv(t, d0, d1, ccys)
    
    return cash
    
# ---------------------------------------------------------------------------

def fx_pnl_pvcash_trd(t, *rest):
    zar = ael.Instrument['ZAR']
    d0 = ael.date_today()
    d1 = d0.add_banking_day(zar, 1)

    trddte = ael.date_from_time(t.execution_time)
    
    if trddte == d1:        
        return 0.0    

                
    fx = fx_delta(t, d0, d1)
    
    return fx
    
# ---------------------------------------------------------------------------

def ir_delta_pnl_trd(t, crv_idx, *rest):        
    zar = ael.Instrument['ZAR']
    d0 = ael.date_today()
    d1 = d0.add_banking_day(zar, 1)

    trddte = ael.date_from_time(t.execution_time)
    
    if trddte == d1:        
        return 0.0    
    
    ins = t.insaddr
    ycs = GetCurves(ins)    
    cnt = len(ycs) -1
    
    ir = 0.0
    
    if crv_idx <= cnt:
        y = ycs[crv_idx]
        
        k = len(y)
    
        if HIST_MODE == 0:
            ymd = d0.to_ymd()
            dte = '%(m)02d/%(d)02d/%(y)02d' % \
                  {'y' : ymd[0]-2000, 'm' : ymd[1], 'd' : ymd[2]}
                  
            y1 = y # + '_' + dte
            
            ymd = d1.to_ymd()
            dte = '%(m)02d/%(d)02d/%(y)02d' % \
                  {'y' : ymd[0]-2000, 'm' : ymd[1], 'd' : ymd[2]}
                  
            y2 = y + '_' + dte
        else:
            crv = y1[0:k-8]
            ymd = d1.to_ymd()
        
            dte = '%(m)02d/%(d)02d/%(y)02d' % \
                  {'y' : ymd[0]-2000, 'm' : ymd[1], 'd' : ymd[2]}
            
            y1 = y
            y2 = crv + dte        
        
        #print 'calling irdelta with:', y1, y2
        ir = bm_delta(t, y1, y2)
        
    return ir

# ---------------------------------------------------------------------------

def ir_name_trd(t, crv_idx, stripdte, *rest):        
    ins = t.insaddr
    ycs = GetCurves(ins)    
    cnt = len(ycs) -1
    
    y = ''
    
    if crv_idx <= cnt:
        y1 = ycs[crv_idx]        
        
        if stripdte == -1:
            k = len(y1)
            y = y1[0:k-9]
        else:
            y = y1
        
    return y

# ---------------------------------------------------------------------------

def vol_name_trd(t, idx, *rest):        
    ins = t.insaddr
    vols = GetVols(ins)    
    cnt = len(vols) -1
    
    vol = ''
    
    if idx <= cnt:
        vol = vols[idx]        
        
    return vol

# ---------------------------------------------------------------------------

def trd_mod(t, *rest):        
    ins = t.insaddr
    zar = ael.Instrument['ZAR']
    d0 = ael.date_today()
    d1 = d0.add_banking_day(zar, 1)
    
    ret = ''
    ins_a = 0
    trd_a = 0
    
    ins_updte_tm = ael.date_from_time(ins.updat_time)
    trd_updte_tm = ael.date_from_time(t.updat_time)
    
    if ins_updte_tm > d0:      
        ins_a = 1
    
    if trd_updte_tm > d0:      
        trd_a = 2
    
    amend = ins_a + trd_a
    
    if amend == 0:
        ret = '-'
    elif amend ==1:
        ret = 'ins'
    elif amend == 2:
        ret = 'trd'
    elif amend == 3:
        ret = 'ins & trd'
        
    return ret

# ---------------------------------------------------------------------------




"""
unex_tot = 0.0
x = []
x.append(ael.Trade[1041045])
debug = 0

for t in ael.TradeFilter['LTFX_CCY_Only'].trades():
    zar = ael.Instrument['ZAR']
    ins = t.insaddr
    
    d0 = ael.date_today()
    d1 = d0.add_banking_day(zar, 1)
    
    ir_all = []
    ir_tot = 0.0
    
    # calc pnl
    pv0 = t.mtm_value_fo(d0, 'ZAR', 1, 0, 1)
    pv1 = t.mtm_value_fo(d1, 'ZAR', 1, 0, 1)
    cash0 = t.accumulated_cash(d0, 'ZAR', 1, 0, '', 1, 'None')
    cash1 = t.accumulated_cash(d1, 'ZAR', 1, 0, '', 1, 'None')
    pnl = pv1 - pv0 + cash1 - cash0
    
    trddte = ael.date_from_time(t.execution_time)
    
    if trddte == d1:
        new_dl = pnl
        theta = 0.0
    else:
        new_dl = 0.0
        
        #calc theta
        theta = t.theta()
        
        #calc cash move
        ccys = GetCcys(ins)
        cash = cash_mv(t, d0, d1, ccys)
        
        #calc fx pnl
        fx = fx_delta(t, d0, d1)
        
        #calc ir pnl    
        ycs = GetCurves(ins)    
        
        # print ycs
        
        for yc in ycs:
            y1 = yc
            
            k = len(y1)
        
            crv = y1[0:k-8]
            ymd = d1.to_ymd()
        
            dte = '%(m)02d/%(d)02d/%(y)02d' % \
                  {'y' : ymd[0]-2000, 'm' : ymd[1], 'd' : ymd[2]}
        
            y2 = crv + dte        
            
            #print 'calling irdelta with:', y1, y2
            ir = bm_delta(t, y1, y2)
            ir_tot = ir_tot + ir
            ir_all.append(ir)
    
    try:
        unex = pnl - theta - fx - ir_tot - cash - new_dl
        unex_tot = unex_tot + unex
    except:
        print t.trdnbr, pnl, theta, fx, ir_tot, cash, new_dl

    print t.trdnbr, '           ', '%.0f' % unex

    if debug == -1:
        print '-----------------------'
        print 'trade : ', t.trdnbr, 'Type : ', t.insaddr.instype
        print 'pnl: %.0f' % pnl
        print 'theta: %.0f' % theta
        print 'fx: %.0f' % fx
        cnt = len(ir_all)
        for k in range(0, cnt):
            print 'ir :', ycs[k], '%.0f' % ir_all[k]
        print 'cash: %.0f' % cash
        print 'new deal: %.0f' % new_dl
        print 'unex: %.0f' % unex

print '-----------------------'
print 'total : %.0f' % unex_tot


"""
