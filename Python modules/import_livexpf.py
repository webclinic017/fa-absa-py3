'''
-----------------------------------------------------------------------
MODULE
    SalesCredit
    
    Purpose                       :  Added portfolios 
    Requester                     :  Ramaremisa, Opy
    Developer                     :  Ickin Vural, Douglas Finkel
    CR Number                     :  418226 , C000000539118, 601016
   
DESCRIPTION
    11 March 2011 - Added additional portfolios
-----------------------------------------------------------------------
'''

import ael, datetime, time

load_all = -1
void_all_fx = 0

portfolio = 'FX_MIDAS_POS'    

# =================================================================================================
def void_all():
    for trd in ael.Portfolio[portfolio].trades():
        if trd.status <> 'Void':
            if (load_all == -1) or (load_all <> -1 and trd.value_day >= ael.date_today()):
                print 'void:', trd.insaddr.insid                
                trd = trd.clone()
                trd.status = 'Void'
                trd.commit() 
                
if void_all_fx == -1:
    void_all()
# =================================================================================================

def fix_delim_ln(sLine):
    lst = sLine.split(',')
    
    cnt = len(lst)
    k = 0
    
    while k < (cnt-1):    
        c = lst[k].count('"')
        if c == 1:
            lst[k] = lst[k] + lst[k+1]        
            lst.remove(lst[k+1])
            cnt = len(lst)
        k = k + 1
        
    return lst
    
# =================================================================================================

def import_fx(parms):          
    dte_today = ael.date_today()
    print 'Today :', dte_today

    run_for_book = ['FWD', 'JOL', 'CAT', 'AST', 'AND', 'ABT', 'EDI', 'CCS', 'GEM', 'FWT', 'ECF', 'UCF', 'GCF', 'FLO',\
                'ABC', 'BBL', 'BBM', 'BBP', 'BTB', 'CBB', 'CDS', 'COR', 'DAN', 'EUX', 'LED', 'NDF', 'OPT', 'RET',\
                'MHF', 'DAB', 'PRM', 'UDM', 'NIX', 'TRM', 'UMS', 'MHR', 'RFT', 'ETA', 'NZT', 'JDY', 'NWT', 'CDR', 'EDF',\
                'JCF', 'RVT', 'ACF', 'PJO', 'GKS', 'GKR', 'CCF', 'PRF', 'RN2', 'RND', 'SND', 'SPW', 'TKN',
                'DHJ', 'JCB', 'PBP', 'AWD', 'CJR', 'FIX', 'PGR', 'YST', 'TMT', 'DIS', 'BRC', 'COM', 'SML', 'WEL']

    sPath = parms[0][0]
    sLivfile = 'Pfmidliv.txt'
    sDkcFile = 'Pfmiddkc.txt'
    
    #run_for_book = parms[0][1].split(',')    
    
    time_format = "%d/%m/%Y %H:%M:%S"
    delim = ','
    c_ccy = 6
    c_bs = 7
    c_valdat = 9
    c_namt = 10
    c_bk = 22
    c_trd = 0
    c_sh = 21
    c_trddte = 8
    
    ins_template = 'FX_TEMPLATE'
    ins_template_type = 'FreeDefCF'    
    party = 'FMAINTENANCE'    
    
    today = ael.date_today()
    hc = ael.Instrument['ZAR']
    prev_biz = today.add_banking_day(hc, -1)
    
    dat = {}
    keys = []
    ccy_tot = {}
    inslst = []    

    f = open(sPath + sLivfile, 'r')        
    
    s = f.readline()
    ln = s.split(delim)
    print ln
    ColCnt = len(ln)
    print 'number of columns', ColCnt
    print 'ccy', ln[c_ccy], 'valdte', ln[c_valdat], 'namt', ln[c_namt]
    
    s = f.readline()
    
    print 'reading cash flows'
    k = 1
    
    while s <> '':    
        k = k + 1
        s = s.replace('\n', '')
        ln = s.split(delim)    
        
        if len(ln) <> ColCnt:
            print 'fixing delim in text qualifier'
            print ln
            ln = fix_delim_ln(s)
        
        for x in range(0, len(ln)):
            ln[x] = ln[x].replace('"', '')

        """
        print '-------------------------'
        print ln
        print '-------------------------'
        """
        
        if ln[c_bk] in run_for_book and ln[c_namt].strip() <> '':
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
            print k, ln            
            
        s = f.readline()
    
    f.close()
    
    # ---------------------------------------------
    # read in cash files from pfmiddkc

    c_dkc_dte = 0
    c_dkc_bk = 1
    c_dkc_ccy = 2
    c_dkc_namt = 3
    
    f = open(sPath + sDkcFile, 'r')
    
    s = f.readline()
    ln = s.split(delim)
    print ln
    ColCnt = len(ln)
    print 'number of columns', ColCnt
    print 'ccy', ln[c_dkc_ccy], 'valdte', ln[c_dkc_dte], 'namt', ln[c_dkc_namt]
    
    s = f.readline()
    
    print 'reading dkc cash balances'
    k = 1
    
    while s <> '':    
        k = k + 1
        s = s.replace('\n', '')
        ln = s.split(delim)    
        
        if len(ln) <> ColCnt:
            print 'fixing delim in text qualifier'
            print ln
            ln = fix_delim_ln(s)
        
        for x in range(0, len(ln)):
            ln[x] = ln[x].replace('"', '')
        
        if ln[c_dkc_bk] in run_for_book and ln[c_dkc_namt].strip() <> '':
            sdte = ln[c_dkc_dte]
            namt = float(ln[c_dkc_namt])            
            
            if abs(namt) > 0:                
                tpl = (ln[c_dkc_bk], ln[c_dkc_ccy], sdte)    
                if tpl in dat.keys():                
                    dat[tpl] = dat[tpl] + namt
                else:
                    dat[tpl] = namt
                print 'added cash', tpl, namt
                
                # total by book and ccy - control check
                tpl = (ln[c_dkc_bk], ln[c_dkc_ccy])        
                if tpl in ccy_tot.keys():                
                    ccy_tot[tpl] = ccy_tot[tpl] + namt
                else:
                    ccy_tot[tpl] = namt
                    
        s = f.readline()
    
    f.close()

    keys = dat.keys()
    keys.sort()    
    ins_keys = []
    trds = {}       
    
        
    for trd in ael.Portfolio[portfolio].trades():
        if trd.status <> 'Void':
            if (load_all == -1) or (load_all <> -1 and trd.value_day >= dte_today):
                trd = trd.clone()
                trd.status = 'Void'
                trd.commit() 
                
    
    
    for k in keys:        
        if dat[k] <> 0.0 and k[0] in run_for_book:
            print '\n-----------------------------------------'
            print 'found entry for ', k[1], k            
                
            dte = ael.date(k[2])
            insid = 'fd_' + k[0] + '_' + k[1] + '_' + dte_today.to_string('%Y%m%d')
            ins = ael.Instrument[insid]                        
            curr_ins = ael.Instrument[k[1]]
            
            print 'checking to see if ins exists : ', insid
            
            if ins == None or ins.instype <> ins_template_type:
                ins = ael.Instrument[ins_template].new()
                ins.insid = insid                    
                ins.curr = curr_ins
                ins.commit() 
                print 'created instr', insid            
            else:                
                print insid, ' found'

            ins = ael.Instrument[insid].clone()
            leg = ins.legs()[0]
            leg.curr = ael.Instrument[k[1]]                                
            leg.daycount_method = curr_ins.legs()[0].daycount_method
            
            
            if insid not in inslst:
                inslst.append(insid)
                print 'clearing cash flows'
                for cf in leg.cash_flows():
                    cf.delete()
                        
            cf = ael.CashFlow.new(leg)
            cf.type = 'Fixed Amount'
            cf.fixed_amount = dat[k]
            cf.start_day = ael.date_today().add_banking_day(ael.Instrument['ZAR'], -1)
            cf.end_day = dte
            cf.nominal_factor = 1000000
            cf.pay_day = cf.end_day
            ins.commit()
   
    for s_ins in inslst:
        print '\ncreating trade for :', s_ins
        ins = ael.Instrument[s_ins]
        trd = ael.Trade.new(ins)
        trd.acquirer_ptynbr = ael.Party[party]
        trd.counterparty_ptynbr = ael.Party[party]
        trd.prfnbr = ael.Portfolio[portfolio]                
        trd.quantity = 1.0
        trd.acquire_day = prev_biz
        trd.value_day = prev_biz
        trd.time = prev_biz.to_time()
        trd.commit() 
        print 'created :', trd.trdnbr, prev_biz
        
    print '\nUpload summary'
    #fo.close()
        
    keys = ccy_tot.keys()
    keys.sort()
    
    for k in keys:
        if ccy_tot[k] <> 0:                
            print k[0], '\t', k[1], '\t', '%.0f' % (ccy_tot[k] / 1.0)


#import_fx([['Y:\\Jhb\\FAReports\\AtlasEndOfDay\\LIVEXPF\\2010-01-20\\']])





