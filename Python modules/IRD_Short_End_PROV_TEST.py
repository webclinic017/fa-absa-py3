import ael

# =================================================================================================
# Function to return the interpolated market rate needed
# for the short end provision calc as performed by IRD desk
# rate is interpolated in the below series of market rates
# 3m Jibar, 1x4 through to 9x12 jibar fra rates
#
# parameters:
# 1. DATE : value date for interpolated reset rate
# 2. DATE : report date
# 
#
# Dirk Strauss - 26-Jun-2007
# =================================================================================================

lmpczar = []
lmpczar.append(ael.date('2007-12-12'))
lmpczar.append(ael.date('2008-01-31'))
lmpczar.append(ael.date('2008-04-10'))
lmpczar.append(ael.date('2008-06-12'))
lmpczar.append(ael.date('2008-08-14'))
lmpczar.append(ael.date('2008-10-09'))
lmpczar.append(ael.date('2008-12-11'))

lmpcusd = []
lmpcusd.append(ael.date('2007-12-11'))
lmpcusd.append(ael.date('2008-01-30'))
lmpcusd.append(ael.date('2008-03-18'))
lmpcusd.append(ael.date('2008-04-30'))
lmpcusd.append(ael.date('2008-06-25'))
lmpcusd.append(ael.date('2008-08-05'))
lmpcusd.append(ael.date('2008-09-16'))
lmpcusd.append(ael.date('2008-10-29'))
lmpcusd.append(ael.date('2008-12-16'))


# ===================================================================================
def get_next_mpczar(repdte):
    
    for d in lmpczar:
        if d > repdte[0][0]:
            return d
    
    return -1
        
#print get_next_mpczar(ael.date('2008-10-08'))

# ===================================================================================

# ===================================================================================
def get_next_mpcusd(repdte):
    
    for d in lmpcusd:
        if d > repdte[0][0]:
            return d
    
    return -1
        
#print get_next_mpcusd(ael.date('2008-10-08'))

# ===================================================================================

def mkt_rate_ZAR(params):    

    #print params
    
    ccy = ael.Instrument['ZAR']        
    d1 = params[0][1]        
    
    mpc = params[0][2]
    #mpc = get_next_mpczar([[d1]])
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
            mkt_rt.append( mkt_rt[len(mkt_rt)-1] )
            
            mkt.append('post-mpc')        
            mkt_dte.append(mpc.add_days(1))
            mkt_rt.append(rt)
            
            done_mpc = -1
        
        mkt.append(ins.insid)        
        mkt_dte.append(dte)
        mkt_rt.append(rt)
    
    #print mkt
    #print mkt_rt
    #print mkt_dte
    #print ''
    print mpc
    return lin_interp(mkt_dte, mkt_rt, params[0][0])

# =======================================================================================

def mkt_rate_USD(params):    

    #print params
    
    ccy = ael.Instrument['USD']        
    d1 = params[0][1]        
    
    mpc = params[0][2]
    #mpc = get_next_mpcusd([[d1]])
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
    
    #print mkt
    #print mkt_rt
    #print mkt_dte
    #print ''
    
    return lin_interp(mkt_dte, mkt_rt, params[0][0])




# =================================================================================================
# Function for returning a leanear interpolated value
#
# parameters
# 1. LIST : x-values (must contain DATEs)
# 2. LIST : y-values (must be numeric)
# 3. DATE : value to interpolate
#
# Dirk Strauss - 26-Jun-2007
# =================================================================================================

def lin_interp(x, y, val):    
    
    # print 'Interp for date : ' + str(val)
    
    if val <= x[0]:
        return y[0]
        
    for k in range(1, len(x)):
        if x[k] > val:
            n = x[k-1].days_between(x[k]) * 1.0
            n1 = x[k-1].days_between(val) * 1.0
            n2 = n - n1            
            interp = n1/n * y[k] + n2/n * y[k-1]
            # print n, n1, n2, k, val, x[k-1], x[k], y[k-1], y[k]
            return interp
    
    return y[ len(y)-1 ]
