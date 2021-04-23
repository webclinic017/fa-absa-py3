'''
Purpose               :  Calculate the value of the cashflows per trade for a trade filter and the effect of simulating a shift on the price would have
Department and Desk   :  MO
Requester             :  Martin vd Walt
Developer             :  Anwar Banoo
CR Number             :  195695
'''

import acm, ael, time

def trdflt():
    list = []
    for tf in ael.TradeFilter.select():
        list.append(tf.fltid)
    return list
    
ael_variables = [('outputpath', 'Output Path:', 'string', None, 'F:\\'),
                 ('tradefilter', 'Trade Filter', 'string', trdflt(), None, 1, 0)]
    
def ael_main(dict):

    dt = ael.date_today()
    ds = ael.date('1990-01-01')
    dt_str = dt.to_string('%Y-%m-%d')

    dt_ytd = dt.add_banking_day(ael.Instrument['ZAR'], -1)

    ins_cpi = ael.Instrument['SACPI']
    yc = ael.YieldCurve['ZAR-CPI']

    if time.localtime().tm_hour > 12:
        runtime = 'COB'
    else:
        runtime = 'SOB'
            
    filter = dict['tradefilter']
	
    Output = open(dict['outputpath'] +  filter + '_' + dt_str + '_' +  runtime + '.xls', 'w')

    PV_Dict = {}
    CASH_Dict = {}
 
    trds = ael.TradeFilter[filter].trades()    
    
    for trd in trds:    
        
        PV_Dict[(trd.trdnbr, 'Nominal')] = 0
        PV_Dict[(trd.trdnbr, 'Fixed Amount')] = 0
        PV_Dict[(trd.trdnbr, 'Real')] = 0
        PV_Dict[(trd.trdnbr, 'Real_Index')] = 0
        
        CASH_Dict[(trd.trdnbr, 'Nominal')] = 0
        CASH_Dict[(trd.trdnbr, 'Fixed Amount')] = 0
        CASH_Dict[(trd.trdnbr, 'Real')] = 0 
        CASH_Dict[(trd.trdnbr, 'Real_Index')] = 0
          
        ins = trd.insaddr
        
        if ins.instype == 'Curr':        
            if ael.date(trd.value_day) > dt:
                CASH_Dict[trd.trdnbr, 'Nominal'] = CASH_Dict[trd.trdnbr, 'Nominal'] + trd.premium * get_fx_rate(trd.curr.insid) +  trd.quantity * get_fx_rate(ins.insid)
            else:
                PV_Dict[trd.trdnbr, 'Nominal'] = PV_Dict[trd.trdnbr, 'Nominal'] +  trd.present_value()
	
        if ins.instype == 'Option':
        
            PV_Dict[trd.trdnbr, 'Nominal'] = PV_Dict[trd.trdnbr, 'Nominal'] +  trd.present_value()
                               
            if trd.payments() <> None:    
                for p in trd.payments():                
                    if ael.date(p.payday) <= dt:
                        CASH_Dict[trd.trdnbr, 'Nominal'] = CASH_Dict[trd.trdnbr, 'Nominal'] + p.amount * get_fx_rate(p.curr.insid)                  
                    else:
                        PV_Dict[trd.trdnbr, 'Nominal'] = PV_Dict[trd.trdnbr, 'Nominal'] +  (trd.present_value() - PV_Dict[trd.trdnbr, 'Nominal'] - PV_Dict[trd.trdnbr, 'Real'])
                
                if trd.premium <> 0 and ael.date(trd.value_day) <= dt:
                    CASH_Dict[trd.trdnbr, 'Nominal'] = CASH_Dict[trd.trdnbr, 'Nominal'] + trd.premium  
		
        if ins.instype == 'FRA':   
     
            for l in ins.legs():
                if l.index_ref <> None:
                    PV_Dict[trd.trdnbr, 'Real'] = PV_Dict[trd.trdnbr, 'Real'] +  l.present_value() * trd.quantity
                    for cf in l.cash_flows():                        
                        if ael.date(cf.pay_day) >= ael.date(trd.value_day) and ael.date(cf.pay_day) <= dt:
                            CASH_Dict[trd.trdnbr, 'Real'] = CASH_Dict[trd.trdnbr, 'Real'] + cf.projected_cf() * trd.quantity * get_fx_rate(l.curr.insid)  
							
                        for r in cf.resets():
                                if r.value == 0:
                                    if r.type == 'Nominal Scaling':                                    
                                        rc = r.clone()
                                        rc.value = ins_cpi.cpi_reference(dt_ytd) / yc.Rate(ael.date_today(), ael.date(r.day), 'Discount', 'Act/365', 'Discount') 
                                        tm = ael.date_today().to_time()
                                        rc.read_time = tm
                                        rc.apply()
                        
                    PV_Dict[trd.trdnbr, 'Real_Index'] = PV_Dict[trd.trdnbr, 'Real_Index'] +  l.present_value() * trd.quantity
                    
                    for cf in l.cash_flows():
                        for r in cf.resets():
                            r.revert_apply()
							
                else:
                    
                    PV_Dict[trd.trdnbr, 'Nominal'] = PV_Dict[trd.trdnbr, 'Nominal'] +  l.present_value() * trd.quantity
                    for cf in l.cash_flows():                        
                        if ael.date(cf.pay_day) >= ael.date(trd.value_day) and ael.date(cf.pay_day) <= dt:                            
                            CASH_Dict[trd.trdnbr, 'Nominal'] = CASH_Dict[trd.trdnbr, 'Nominal'] + cf.projected_cf() * trd.quantity * get_fx_rate(l.curr.insid)                            
							
            if trd.premium <> 0 and ael.date(trd.value_day) <= dt:
                CASH_Dict[trd.trdnbr, 'Nominal'] = CASH_Dict[trd.trdnbr, 'Nominal'] + trd.premium        
    
            if trd.payments() <> None:    
                for p in trd.payments():                
                    if ael.date(p.payday) <= dt:
                        CASH_Dict[trd.trdnbr, 'Nominal'] = CASH_Dict[trd.trdnbr, 'Nominal'] + p.amount * get_fx_rate(p.curr.insid)                  
                    else:      
                        PV_Dict[trd.trdnbr, 'Nominal'] = PV_Dict[trd.trdnbr, 'Nominal'] +  (trd.present_value() - PV_Dict[trd.trdnbr, 'Nominal'] - PV_Dict[trd.trdnbr, 'Real'])
        
        if ins.instype <> 'Combination' and ins.instype <> 'Option' and ins.instype <> 'FRA' and ins.instype <> 'Curr':
     
            for l in ins.legs():
                if l.index_ref <> None:
                    PV_Dict[trd.trdnbr, 'Real'] = PV_Dict[trd.trdnbr, 'Real'] +  l.present_value() * trd.quantity
                    for cf in l.cash_flows():                        
                        if ael.date(cf.pay_day) > ael.date(trd.value_day) and ael.date(cf.pay_day) <= dt:
                            CASH_Dict[trd.trdnbr, 'Real'] = CASH_Dict[trd.trdnbr, 'Real'] + cf.projected_cf() * trd.quantity * get_fx_rate(l.curr.insid)  

                        for r in cf.resets():
                            if r.value == 0:
                                if r.type == 'Nominal Scaling':
                                        
                                    rc = r.clone()
                                    rc.value = ins_cpi.cpi_reference(dt_ytd) / yc.yc_rate(ael.date_today(), ael.date(r.day), 'Discount', 'Act/365', 'Discount') 
                          
                                    tm = ael.date_today().to_time()
                                    rc.read_time = tm
                                    rc.apply()
                      
                    PV_Dict[trd.trdnbr, 'Real_Index'] = PV_Dict[trd.trdnbr, 'Real_Index'] +  l.present_value() * trd.quantity
 
                    for cf in l.cash_flows():
                        for r in cf.resets():
                            r.revert_apply()
      
                else:
                    
                    PV_Dict[trd.trdnbr, 'Nominal'] = PV_Dict[trd.trdnbr, 'Nominal'] +  l.present_value() * trd.quantity
                    for cf in l.cash_flows():                        
                        if ael.date(cf.pay_day) > ael.date(trd.value_day) and ael.date(cf.pay_day) <= dt:                            
                            CASH_Dict[trd.trdnbr, 'Nominal'] = CASH_Dict[trd.trdnbr, 'Nominal'] + cf.projected_cf() * trd.quantity * get_fx_rate(l.curr.insid)                            
                            
            if trd.premium <> 0 and ael.date(trd.value_day) <= dt:
                CASH_Dict[trd.trdnbr, 'Nominal'] = CASH_Dict[trd.trdnbr, 'Nominal'] + trd.premium        
    
            if trd.payments() <> None:    
                for p in trd.payments():                
                    if ael.date(p.payday) <= dt:    
                        CASH_Dict[trd.trdnbr, 'Nominal'] = CASH_Dict[trd.trdnbr, 'Nominal'] + p.amount * get_fx_rate(p.curr.insid)                  
                    else:
                        PV_Dict[trd.trdnbr, 'Nominal'] = PV_Dict[trd.trdnbr, 'Nominal'] +  (trd.present_value() - PV_Dict[trd.trdnbr, 'Nominal'] - PV_Dict[trd.trdnbr, 'Real'])
                            
        elif ins.instype == 'Combination':
            ins_acm = acm.FInstrument[ins.insid]
            for com_ins_acm in ins_acm.Instruments():
                com_ins_ael = ael.Instrument[com_ins_acm.Oid()]
                
                for l in com_ins_ael.legs():             

                    if l.index_ref <> None:
                        PV_Dict[trd.trdnbr, 'Real'] = PV_Dict[trd.trdnbr, 'Real'] + l.present_value() * trd.quantity 
                        for cf in l.cash_flows():                        
                            if ael.date(cf.pay_day) > ael.date(trd.value_day) and ael.date(cf.pay_day) <= dt:
                                CASH_Dict[trd.trdnbr, 'Real'] = CASH_Dict[trd.trdnbr, 'Real'] + cf.projected_cf() * trd.quantity * get_fx_rate(l.curr.insid)  
								
                            for r in cf.resets():
                                if r.value == 0:
                                    if r.type == 'Nominal Scaling':                                    
                                        rc = r.clone()
                                        rc.value = ins_cpi.cpi_reference(dt_ytd) / yc.yc_rate(ael.date_today(), ael.date(r.day), 'Discount', 'Act/365', 'Discount')
                                        tm = ael.date_today().to_time()
                                        rc.read_time = tm
                                        rc.apply()
                        
                        PV_Dict[trd.trdnbr, 'Real_Index'] = PV_Dict[trd.trdnbr, 'Real_Index'] +  l.present_value() * trd.quantity
                        
                        for cf in l.cash_flows():
                            for r in cf.resets():
                                r.revert_apply()	
								
                    else:
                        PV_Dict[trd.trdnbr, 'Nominal'] = PV_Dict[trd.trdnbr, 'Nominal'] + l.present_value() * trd.quantity
                        for cf in l.cash_flows():                        
                            if ael.date(cf.pay_day) > ael.date(trd.value_day) and ael.date(cf.pay_day) <= dt:
                                CASH_Dict[trd.trdnbr, 'Nominal'] = CASH_Dict[trd.trdnbr, 'Nominal'] + cf.projected_cf() * trd.quantity * get_fx_rate(l.curr.insid)                   
                        
            if trd.premium <> 0 and ael.date(trd.value_day) <= dt:
                CASH_Dict[trd.trdnbr, 'Nominal'] = CASH_Dict[trd.trdnbr, 'Nominal'] + trd.premium        
    
            if trd.payments() <> None:    
                for p in trd.payments():                
                    if ael.date(p.payday) <= dt:
                        CASH_Dict[trd.trdnbr, 'Nominal'] = CASH_Dict[trd.trdnbr, 'Nominal'] + p.amount * get_fx_rate(p.curr.insid)                  
                    else:
                        PV_Dict[trd.trdnbr, 'Nominal'] = PV_Dict[trd.trdnbr, 'Nominal'] +  (trd.present_value() - PV_Dict[trd.trdnbr, 'Nominal'] - PV_Dict[trd.trdnbr, 'Real'])

    s = GenStrFromList('\t', 'Date', dt)
    Output.write(s)
    
    s = GenStrFromList('\t', 'Filter', filter)
    Output.write(s)
    
    s = GenStrFromList('\t', 'Trade', 'PV Nominal', 'PV Real', 'Cash Nominal', 'Cash Real', 'PV Ytd Index Levels', 'Nominal Amount', 'Expiry Day')    
    Output.write(s)
    
    for t in trds:    
        ins = t.insaddr
        s = GenStrFromList('\t', t.trdnbr, PV_Dict[t.trdnbr, 'Nominal'],  PV_Dict[t.trdnbr, 'Real'],  CASH_Dict[t.trdnbr, 'Nominal'], CASH_Dict[t.trdnbr, 'Real'], PV_Dict[t.trdnbr, 'Real_Index'], t.nominal_amount(), t.maturity_date().to_string('%d %b %Y'))
        Output.write(s)
    
    print '===================DONE==========================='
    
    
def get_fx_rate(fccy):
    hccy = 'ZAR'
    curr_base = ael.Instrument[hccy] 
    curr = ael.Instrument[fccy]
    dt = ael.date_today()
    d = 1.0/curr_base.used_price(dt, curr.insid)
    return d
    
   
def GenStrFromList(delim, *list):
    s = ''
    k = 0
    cnt = len(list)    
    for o in list:
        k += 1
        if k < cnt:
            s = s + str(o) + delim
        else:
            s = s + str(o) + '\n'
    return s 

#Main('IRD_CPI')
