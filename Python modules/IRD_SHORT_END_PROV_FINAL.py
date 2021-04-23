'''
Purpose               :  Calculate the intermediate points on the ZAR-SWAP curve for non standard resets
Department and Desk   :  MO
Requester             :  Martin vd Walt
Developer             :  Anwar Banoo
CR Number             :  208636
'''

import ael, acm

#=====================================================================================

'''
dt = ael.date_today()
dt_str = dt.to_string()
'''

lmpczar = acm.FList()
lmpcusd = acm.FList()
fxlist = acm.FDictionary()

# ---------------------------------------------------------------------------
# returns the fx rate
# ccy is a list that can contain 1 or 2 parameters
# if ccy only contains one parameter then the base ccy is assumed to be ZAR
# if ccy contains 2 paramaters then the first entry will be taken as the base ccy
# ---------------------------------------------------------------------------

def get_fx_rate(curr):
    currency = curr[0][0]
    
    if currency in fxlist.Keys():        
        return fxlist[currency]
        
    hccy = 'ZAR'
    d = 0.0

    if currency == hccy:
        fxlist[currency] = 1.0
        return 1.0

    curr_base = ael.Instrument[hccy] 
    curr = ael.Instrument[currency]

    dt = ael.date_today()

    d = 1.0/curr_base.used_price(dt, curr.insid)
    fxlist[currency] = d

    return d

def setup_mpcZAR():
    tsspec = acm.FTimeSeriesSpec['MO_MPC_ZAR']
    ts = tsspec.TimeSeries()
    for t in ts:
        lmpczar.Add(t.Day())
    lmpczar.Sort()

def setup_mpcUSD():
    tsspec = acm.FTimeSeriesSpec['MO_MPC_USD']
    ts = tsspec.TimeSeries()
    for t in ts:
        lmpcusd.Add(t.Day())
    lmpcusd.Sort()
    
def get_next_mpczar(repdte):
    if lmpczar.Size() == 0:
        setup_mpcZAR()
        
    for d in lmpczar:
        if d > repdte:
            return d    
    return -1

def get_next_mpcusd(repdte):
    if lmpcusd.Size() == 0:
        setup_mpcUSD()
        
    for d in lmpcusd:
        if d > repdte:
            return d    
    return -1
	
def mkt_rate_ZAR(params):
    ccy = ael.Instrument['ZAR']        
    
    resetd = params[0][0]
    resetd = ael.date_from_string(resetd)    

    d1 = params[0][1] 
    d1 = ael.date_from_string(d1)

    #mpc = params[0][2]
    mpc = get_next_mpczar(d1) #ael.date_from_string(mpc)

    done_mpc = 0
    
    mkt = []
    mkt_dte = []
    mkt_rt = []
    
    mkt.append('ZAR-JIBAR-3M')
    mkt_dte.append(d1)
    ins = ael.Instrument['ZAR-JIBAR-3M']
    mkt_rt.append(ins.used_price()) 

    for k in range(1, 10):    
        ins = ael.Instrument['ZAR/FRA/JI/' + str(k) + 'X' + str(k+3)]
        dte = d1.add_months(k).adjust_to_banking_day(ccy)
        rt = ins.used_price()
        
        if dte > mpc and done_mpc == 0:
            mkt.append('pre-mpc')        
            mkt_dte.append(mpc)
            mkt_rt.append( ael.Instrument['ZAR/FRA/JI/PRE_MPC'].used_price())
            
            mkt.append('post-mpc')        
            mkt_dte.append(mpc.add_days(1).adjust_to_banking_day(ccy))
            mkt_rt.append( ael.Instrument['ZAR/FRA/JI/POST_MPC'].used_price())
            
            done_mpc = -1
        
        mkt.append(ins.insid)        
        mkt_dte.append(dte)
        mkt_rt.append(rt)

    return lin_interp(mkt_dte, mkt_rt, resetd)

#=====================================================================================

def mkt_rate_USD(params):    

    ccy = ael.Instrument['USD']        
    d1 = params[0][1]        
    
    mpc = get_next_mpcusd(d1) #params[0][2]
    done_mpc = 0
    
    mkt = []
    mkt_dte = []
    mkt_rt = []
    
    mkt.append('USD-LIBOR-3M')
    mkt_dte.append(d1)
    ins = ael.Instrument['USD-LIBOR-3M']
    mkt_rt.append(ins.used_price())
    
    for k in range(1, 10):    
        ins = ael.Instrument['USD/FRA/LI/' + str(k) + 'X' + str(k+3) ]
        dte = d1.add_months(k).adjust_to_banking_day(ccy)
        rt = ins.used_price()
        
        if dte > mpc and done_mpc == 0:
            mkt.append('pre-mpc')        
            mkt_dte.append(mpc)
            mkt_rt.append( mkt_rt[len(mkt_rt)-1] )
            
            mkt.append('post-mpc')        
            mkt_dte.append(mpc.add_days(1))
            mkt_rt.append(rt)
            
            done_mpc = -1
        
        mkt.append(ins.insid)        
        mkt_dte.append(dte)
        mkt_rt.append(rt)

    return lin_interp(mkt_dte, mkt_rt, params[0][0])	
	
#=====================================================================================

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
	
#=====================================================================================
   
def ExcludeBasisTrades(trade):    
    Check = 0
    trd = acm.FTrade[trade[0][0]]    
    legs = trd.Instrument().Legs()
    #legs = ins.Legs()
    for l in legs:
        if l.LegType() == 'Float':
            Check = Check + 1
    if Check < 2:
        return trd.Name()        
    else:
        return '2'


