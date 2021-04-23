from types import *
import acm
import ael
import time



# =============================================================================================

def GetTrdPVs(trds, sumall=0, convToZar=1, IgnoreExpired=1, UseCore = 1):
    
    #If input is one trade, returns the pv as by adfl, if > 1 trade, returns list with trdnbr and pv
    trdlist = []
    cnt = 0
    #print trds
    if type(trds) <> ListType:
        trds = [trds] 
    else:
        if type(trds[0]) == ListType:
            trds = trds[0]           
    
    adfl = 'valPLEnd'
    tag = acm.CreateEBTag()
    context = acm.GetDefaultContext()      
    sum = 0.0   
    fxrts = GetFxRates()   

    if sumall:
        ret = 0.0
    else:
        ret = {}    

    tod = ael.date_today()  
    tm = {}       
        
    
    for itrd in trds:
        itrd = acm.FTrade[itrd]        
        t = time.clock()
        
        if type(itrd) in [IntType, StringType]:
            trd = acm.FTrade[itrd]    
        else:
            trd = itrd        

        mat_date = ael.date(trd.maturity_date())           

        if (mat_date >= tod and IgnoreExpired) or not IgnoreExpired:     
            trdnbr = trd.Name()
            ccy = trd.Trade().Currency().Name()           
            
            if convToZar:
                fx = fxrts[ccy]
            else:
                fx = 1.0            

            if UseCore:
                trdrw = acm.CreateTradeRow(trd, 0)            
                eval = acm.GetCalculatedValueFromString(trdrw, context, adfl, tag)                 
                pv = eval.Value() * fx
                            
            else:
                pv = trd.present_value() * fx                

            if sumall:
                ret += pv
            else:
                ret[trdnbr] = pv                     

            tm[trdnbr] = t - time.clock()         
        eval = None        
        p = (itrd.Name(), pv)
        trdlist.append(p)
    
    if len(trdlist) > 1:
        return trdlist        
    else:
        return trdlist[0][1]
    

#========================================================================================

def GetFxRates():

    fccys = acm.FCurrency.Select('')
    ccys = {}
    td = acm.DateToday()    

    for ccy in fccys:
        s = ccy.Name()
        if len(s) == 3:
            ccys[s] = ccy.used_price(td, 'ZAR')           

    return ccys

 

#========================================================================================

def PopulateBasis():

    dt = ael.date_today()    
    yc_s = ael.YieldCurve['ZAR-SWAP']    
    yc_fx = ael.YieldCurve['USD-ZAR/FX/FWDS']    
    yc_b = ael.YieldCurve['ZAR-BASIS']    
    sprd = {}   
    pnts = yc_b.points().members()    
    basis_pnt = []    
    dtmax = dt.add_period('3y')
     
    for pnt in pnts:                    
        ps = ael.YCSpread.select('point_seqnbr = ' + str(pnt.seqnbr))           
    
        if len(ps) > 0:    
            sprd = ps[0]    
        else:    
            sprd = None              
        dt2 = dt.add_period(pnt.date_period)        
        
        if dt2 <= dtmax and sprd <> None:    
            swp_rt = yc_s.yc_rate(dt, dt2, 'Quarterly', 'Act/365', 'Par Rate')             
            basis_rt = yc_fx.yc_rate(dt, dt2, 'Quarterly', 'Act/365', 'Par Rate')         
            basis = basis_rt - swp_rt            
            p = [dt2, pnt.date_period, basis*100, sprd.spread*100, swp_rt *100, basis_rt*100]             
            basis_pnt.append(p)             
            psc = ps[0].clone()    
            psc.spread = basis                      
            psc.commit()                     
                   
    basis_pnt.sort()
    
    return 'Success'

#=======================================================================



def Delete_ZeroCF():
    trds = []

    change = 0
    cnt = 0
    if type(trds) <> ListType:
        trds = [trds] 
    else:
        if type(trds[0]) == ListType:
            trds = trds[0] 
    

    for trd in trds:
        instrument = ael.Trade[trd].insaddr
        for leg in instrument.legs():
            lc=leg.clone()
            for cf in lc.cash_flows():
                if cf.projected_cf() == 0:
                    print 'Trade Number', ael.Trade[trd].trdnbr, 'CF Number', cf.cfwnbr, 'Projected Amount', cf.projected_cf() 
                    try:
                        cf.delete()
                    except:
                        print 'Cannot delete cf ', cf.cfwnbr
            
            if change == 1:
                try:
                    lc.commit()
                except:
                    print 'Cannot commit leg', lc.legnbr
