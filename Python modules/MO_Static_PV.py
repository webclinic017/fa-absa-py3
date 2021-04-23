import ael, acm, time, sys

  
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

#======================================================================================== 
# Return PV of a tradefilter, on an instrument level 
#======================================================================================== 
    
def pv_Ins_acm(stf, ins):

    tf = acm.FTradeSelection[stf]
    insrw = acm.CreateSingleInstrumentAndTrades(tf, ins)

    tag = acm.CreateEBTag()
    context = 'Standard'        
    adfl = 'object:*"valPLEnd"' 
    
    eval = acm.GetCalculatedValueFromString(insrw, context, adfl, tag) 
    pvIns = eval.Value()    

    return pvIns
    

#======================================================================================== 
# Return cash balance of a tradefilter, on an instrument level 
#======================================================================================== 

def cash_Ins_acm(stf, ins):

    tf = acm.FTradeSelection[stf]
    insrw = acm.CreateSingleInstrumentAndTrades(tf, ins)

    tag = acm.CreateEBTag()
    context = 'Standard'        
    adfl = 'object:*"cashEnd"' 
    
    eval = acm.GetCalculatedValueFromString(insrw, context, adfl, tag) 
    cashIns = eval.Value()    

    return cashIns
    
  
def basePV_Ins(stf, outpath):
    
     
    tf = acm.FTradeSelection[stf]
    dt = ael.date_today()
    dt_str = dt.to_string('%y%m%d')
    
    trds = tf.Trades()
    inslist = []
    for t in trds:
        
        ins = t.Instrument()
        mat = ael.date(ins.maturity_date())
        
        if (mat >= dt) and ins not in inslist:
            inslist.append(ins)

      
    
    pvC_b = {}
    pvC_base = open(outpath + stf + '_' + 'BasePV' + '_'+ dt_str + '.xls', 'w')

    t0 = time.time()
    
    print 'Extracting base pv and cash'
    
    for i in inslist:
        insid = i.Name()
        pv = pv_Ins_acm(stf, i)
        cash = cash_Ins_acm(stf, i)
        pvC_b[insid] = (pv, cash)
        
    for k in pvC_b.keys():
        s = GenStrFromList('\t', k, pvC_b[k][0], pvC_b[k][1])
        pvC_base.write(s)
    
    pvC_base.close()
    
    
    print '%.0f' % (time.time() - t0) + ' seconds extracting base pv and cash'
        

def TrdFilter():

    TrdFilter=[]
    
    for t in ael.TradeFilter:
        TrdFilter.append(t.fltid)
    TrdFilter.sort()
    return TrdFilter


ael_variables = [('TrdFilter', 'TrdFilter', 'string', TrdFilter(), 'MO_EqRisk_Index', 1),
                 ('OutPath', 'OutPath', 'string', None, 'f:\\temp\\', 1)] 

def ael_main(ael_dict):

    stf = ael_dict['TrdFilter']
    outpath = ael_dict['OutPath']
    
    basePV_Ins(stf, outpath)

    
    












