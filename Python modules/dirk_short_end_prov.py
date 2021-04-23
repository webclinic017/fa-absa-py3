import ael

# =================================================================================================
# Function to return the interpolated market rate needed
# for the short end provision calc as performed by IRD desk
# rate is interpolated in the below series of market rates
# 3m Jibar, 1x4 through to 9x12 jibar fra rates
#
# parameters:
# 1. date : value date for interpolated reset rate
# 2. date : next MPC date
# 3. report date
#
# Dirk Strauss - 26-Jun-2007
# =================================================================================================

def mkt_rate(params):    

    #print params
    
    ccy = ael.Instrument['ZAR']        
    d1 = params[0][2]        
    
    mpc = params[0][1]
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
        
        if dte >= mpc and done_mpc == 0:
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
# FUNCTION TO CALC SHORT END PROV

def short_end_prov(trd, *rest):    

    ccy = ael.Instrument['ZAR']
    
    d1 = ael.date_today()
    d2 = d1.add_days(7).adjust_to_banking_day(ccy)
    
    mkt = []
    mkt_dte = []
    mkt_rt = []
    
    mkt.append('ZAR-JIBAR-3M')
    mkt_dte.append(d1)
    ins = ael.Instrument['ZAR-JIBAR-3M']
    mkt_rt.append(ins.used_price())
    
    for k in range(1, 10):    
        ins = ael.Instrument['ZAR/FRA/JI/' + str(k) + 'X' + str(k+3)]
        mkt.append(ins.insid)
        #lg = ins.legs() [0]
        mkt_dte.append(d1.add_months(k).adjust_to_banking_day(ccy))
        mkt_rt.append(ins.used_price())
    
    print len(mkt_rt), mkt_rt
    print len(mkt_dte), mkt_dte
    print ''
    
    #trds = ael.TradeFilter['IRP_Funding Hybrid IRS'].trades()
    
    adj = 0.0
    
    #for trd in trds:
    ins = trd.insaddr
    for lg in ins.legs():        
        if lg.type == 'Float':
            cfs = lg.cash_flows()
            for cf in cfs:                
                for rst in cf.resets():
                    if rst.day >= d1 and rst.day < d2:
                        nom = trd.quantity * ins.contr_size * lg.nominal_factor * cf.nominal_factor                        
                        #print trd.trdnbr, ins.insid, lg.type, cf.pay_day, rst.day, nom, tst()
                        
                        fwd = rst.forward_rate()
                        mkt_interp = lin_interp(mkt_dte, mkt_rt, rst.day)
                        tf = rst.start_day.years_between(rst.end_day)
                        diff = mkt_interp - fwd
                        adj = 96 * tf * nom * diff * 100 / 1000000
                        
                        print ''
                        print lg.float_rate.insid
                        print 'fwd : ' + str(fwd), 'interp : ' + str(mkt_interp), 'diff : ' + str(mkt_interp - fwd)
                        print 'adj : ' + str(96 * tf * nom * diff * 100 / 1000000)
    return adj
                        


# =================================================================================================
# FUNCTION USED LINEAR INTERPOLATE

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
    
    
    
    
    
    
    
    
