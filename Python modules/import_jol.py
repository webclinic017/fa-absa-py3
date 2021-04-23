import ael, datetime, time

load_all = -1
void_all_fx = 0

portfolio = 'FX_JOL_POS'    

def void_all():
    for trd in ael.Portfolio[portfolio].trades():
        if trd.status <> 'Void':
            if (load_all == -1) or (load_all <> -1 and trd.value_day >= ael.date_today()):
                print('void:', trd.insaddr.insid)                
                trd = trd.clone()
                trd.status = 'Void'
                trd.commit() 
                
if void_all_fx == -1:
    void_all()


def import_fx(sInfile):      
    dte_today = ael.date_today().add_banking_day(ael.Instrument['ZAR'], -1)
    print('Today :', dte_today)
    run_for_book = 'JOL'
    
    time_format = "%d/%m/%Y %H:%M:%S"
    delim = '\t'
    c_ccy = 5
    c_bs = 6
    c_valdat = 8
    c_namt = 9
    c_bk = 21
    c_trd = 0
    c_sh = 20
    c_trddte = 7
    
    ins_template = 'ZERO-TEST'
    ins_template_type = 'Zero'    
    party = 'FMAINTENANCE'
    
    #sInfile = 'c:\\temp\\LIVEXPF.CSV'
    sOutFile = 'c:\\temp\\out.txt'
    
    today = ael.date_today()
    hc = ael.Instrument['ZAR']
    prev_biz = today.add_banking_day(hc, -1)
    
    dat = {}
    keys = []
    ccy_tot = {}
    inslst = []
    
    f = open(sInfile[0][0], 'r')
    #fo = open(sOutFile, 'w')
    
    s = f.readline()
    ln = s.split(delim)
    print('ccy', ln[c_ccy], 'valdte', ln[c_valdat], 'namt', ln[c_namt])
    
    s = f.readline().replace('"', '')
    
    print('reading cash flows')
    k = 1
    
    while s <> '':    
        k = k + 1
        s = s.replace('\n', '')
        ln = s.split(delim)    
        
        if ln[c_bk] == run_for_book and ln[c_namt].strip() <> '':
            sdte = ln[c_valdat]
            sdte = sdte.replace('/', '-')
            d = sdte
            
            sdte = ln[c_trddte]
            sdte = sdte.replace('/', '-')
            trddte = ael.date(sdte)
            
            if load_all == -1 or (load_all <> -1 and trddte >= prev_biz):
                if ln[c_bs] == 'P':
                    bs = 1.0
                else:
                    bs = 1.0
                    
                tpl = (ln[c_bk], ln[c_ccy], d)    
                if tpl in keys:                
                    dat[tpl] = dat[tpl] + (float(ln[c_namt]) * bs)                
                else:
                    dat[tpl] = float(ln[c_namt]) * bs
                    keys = dat.keys()
                    
                # total by book and ccy - control check
                tpl = (ln[c_bk], ln[c_ccy])        
                if tpl in ccy_tot.keys():                
                    ccy_tot[tpl] = ccy_tot[tpl] + (float(ln[c_namt]) * bs)
                else:
                    ccy_tot[tpl] = float(ln[c_namt]) * bs
        elif ln[c_namt].strip() == '':
            print(k, ln)            
            
        s = f.readline().replace('"', '')
    
    f.close()
    
    keys.sort()    
    ins_keys = []
    trds = {}
    """  
    for trd in ael.Portfolio[portfolio].trades():
        if trd.status <> 'Void':
            if (load_all == -1) or (load_all <> -1 and trd.value_day >= ael.date_today()):
                trd = trd.clone()
                trd.status = 'Void'
                trd.commit() 
    """
    for k in keys:        
        if dat[k] <> 0.0 and k[0] == 'JOL':
            print('\n-----------------------------------------')
            print('found entry for JOL', k)            
                
            dte = ael.date(k[2])
            insid = k[0] + '_' + k[1] + '_' + dte.to_string('%Y%m%d')
            ins = ael.Instrument[insid]
            inslst.append(insid)
            
            tot_ins_cf = 0.0
            print('checking to see if ins exists : ', insid)
            
            if ins == None or ins.instype <> ins_template_type:
                ins = ael.Instrument[ins_template].new()
                ins.insid = insid                    
                ins.curr = ael.Instrument[k[1]]                
                ins.exp_day = dte
                ins.commit() 
                print('created instr', insid)
            
                ins = ael.Instrument[insid]
                leg = ins.legs()[0].clone()
                leg.end_day = dte
                leg.pay_calnbr = ael.Instrument[k[1]].legs()[0].pay_calnbr
                leg.curr = ael.Instrument[k[1]]                
                leg.commit()
    
                cf = ins.legs()[0].cash_flows()[0].clone()
                cf.pay_day = dte
                cf.commit()                            
            else:
                for trd in ins.trades():
                    if trd.status <> 'Void':
                        tot_ins_cf = tot_ins_cf + trd.quantity
                
            qunt_to_book = (dat[k] / 1.0) - tot_ins_cf
            
            if abs(qunt_to_book) > 1.0:
                trd = ael.Trade.new(ins)
                trd.acquirer_ptynbr = ael.Party[party]
                trd.counterparty_ptynbr = ael.Party[party]
                trd.prfnbr = ael.Portfolio[portfolio]                
                trd.quantity = qunt_to_book
                trd.acquire_day = dte_today
                trd.value_day = dte_today
                trd.time = dte_today.to_time()
                trd.commit() 
                print('created trade', trd.trdnbr, dat[k] / 1.0, tot_ins_cf, trd.quantity) 
    
                trds[ins.insid] = trd.trdnbr  
            else:
                print('no change in notional for ins :', insid)
    
    ccy_tot_sys = {}
    
    print('\nvoid dropped deals')
    for trd in ael.Portfolio[portfolio].trades():
        ins = trd.insaddr
        leg = ins.legs()[0]
        if trd.status <> 'Void':
            if leg.end_day >= today and ins.insid not in inslst:
                print('void :', trd.trdnbr, ins.insid, leg.end_day, trd.quantity, trd.acquire_day)
                trd = trd.clone()
                trd.status = 'Void'
                trd.commit()
            elif leg.end_day >= dte_today:
                ccy = ins.curr.insid
                if ccy in ccy_tot_sys.keys():
                    ccy_tot_sys[ccy] = ccy_tot_sys[ccy] + trd.quantity
                else:
                    ccy_tot_sys[ccy] = trd.quantity
            else:
                print('???', trd.trdnbr, leg.end_day, dte_today, leg.end_day >= dte_today)
            
    print('\nUpload summary')
    #fo.close()
        
    keys = ccy_tot.keys()
    keys.sort()
    
    for k in keys:
        if ccy_tot[k] <> 0:
            if k[1] in ccy_tot_sys.keys():
                sysval = ccy_tot_sys[k[1]]
            else:
                sysval = 0.0
                
            print(k[0], '\t', k[1], '\t', '%.0f' % (ccy_tot[k] / 1.0), '\t\t%.0f' % sysval, '\t\t%.0f' % (ccy_tot[k] / 1.0 - sysval))
    
# =======================================================================

import_fx([['c:\\temp\\jollive.xls']])

