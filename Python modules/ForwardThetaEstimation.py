'''
Purpose               :  Estimation of theta due to index level move on Inflation Trades
Department and Desk   :  MO
Requester             :  Martin vd Walt
Developer             :  Anwar Banoo
CR Number             :  195695
'''

import acm, ael

def trdflt():
    list = []
    for tf in ael.TradeFilter.select():
        list.append(tf.fltid)
    return list
    
ael_variables = [('outputpath', 'Output Path:', 'string', None, 'F:\\'),
                 ('tradefilter', 'Trade Filter', 'string', trdflt(), None, 1, 0)]

def ael_main(dict):
    print 'Starting estimation of theta due to index level move on Inflation Trades'
    
    filter = dict['tradefilter']
    dt = ael.date_today()
    dt_tom = dt.add_banking_day(ael.Instrument['ZAR'], 1)
    dt_str = dt.to_string('%Y-%m-%d')
    ins_cpi = ael.Instrument['SACPI']
    ref_tod = ins_cpi.cpi_reference(dt)
    ref_tom = ins_cpi.cpi_reference(dt_tom)
    
    Output = open(dict['outputpath'] +  'ThetaEstimate_' + filter + '_' + dt_str + '_' + '.xls', 'w')
        
    trds = ael.TradeFilter[filter].trades()    
    
    s = GenStrFromList('\t', 'Date', dt)
    Output.write(s)
    
    s = GenStrFromList('\t', 'Filter', filter)
    Output.write(s)
    
    s = GenStrFromList('\t', 'InsType', 'Trade', 'CfwNbr', 'PayDay', 'Orig Cf', 'New Cf', 'Diff')    
    Output.write(s)
    
    for trd in trds:
            ins = trd.insaddr
            if ins.instype <> 'Combination':
                for l in ins.legs():            
                    if l.index_ref <> None:
                        if l.index_ref.insid == 'SACPI':          
                            for cf in l.cash_flows():
                                if ael.date(cf.pay_day) > ael.date(trd.value_day) and ael.date(cf.pay_day) > dt:
                                    for r in cf.resets():
                                        if r.type == 'Nominal Scaling':
                                            orig_cf = cf.projected_cf() * trd.quantity 
                                            new_cf = cf.projected_cf()*trd.quantity * ref_tom / ref_tod
                                            s = GenStrFromList('\t', ins.instype, trd.trdnbr, cf.cfwnbr, cf.pay_day, orig_cf, new_cf, new_cf - orig_cf)
                                            Output.write(s)
            else:
                acm_ins = acm.FInstrument[ins.insid]
                for ins_und in acm_ins.Instruments():
                    ins_ael = ael.Instrument[ins_und.Oid()]                    
                    for l in ins_ael.legs():            
                        if l.index_ref <> None:
                            if l.index_ref.insid == 'SACPI':          
                                for cf in l.cash_flows():
                                    if ael.date(cf.pay_day) > ael.date(trd.value_day) and ael.date(cf.pay_day) > dt:
                                        for r in cf.resets():
                                            if r.type == 'Nominal Scaling':
                                                orig_cf = cf.projected_cf() * trd.quantity 
                                                new_cf = cf.projected_cf()*trd.quantity * ref_tom / ref_tod
                                                s = GenStrFromList('\t', ins.instype, trd.trdnbr, cf.cfwnbr, cf.pay_day, orig_cf, new_cf, new_cf - orig_cf)
                                                Output.write(s)
                                                
    print 'Finished'

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
