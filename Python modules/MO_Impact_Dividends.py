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
    


def TrdFilter():

    TrdFilter=[]
    
    for t in ael.TradeFilter:
        TrdFilter.append(t.fltid)
    TrdFilter.sort()
    return TrdFilter

def divImpact(stf, outpath, percbump):
     

    tf = acm.FTradeSelection[stf]
    
    dt = ael.date_today()
    dt_str = dt.to_string('%y%m%d')
    
   
    tf = acm.FTradeSelection[stf]
    
    try:
        
        pvC_base = open(outpath + stf + '_' + 'BasePV' + '_'+ dt_str + '.xls', 'r')
        
    except Exception, e:
        print 'No base PV file found, please run divImpact_BasePV'
    
    pvC_b = {}
    pvC_u = {}
    inslist = []
 
    
    for line in pvC_base:
        tmp = line.split('\t')
        pvC_b[tmp[0]] = (float(tmp[1]), float(tmp[2]))
        ins = acm.FInstrument[tmp[0]]
        inslist.append(ins)
    
    t0 = time.time()
    t1 = time.time()
    
    
    #-----------------------------------------------------------------------
    #Make generic changes to risk group being stressed
    #-----------------------------------------------------------------------

    divList = []
    div_clones = []
    
   
    for divs_org in ael.DividendStream:

        #print divs_org
        divs_clone = divs_org.clone()
        div_clones.append(divs_clone)
    
        for p in divs_clone.estimates():
            p.dividend = p.dividend * (1 + percbump/100)
    
    for d in div_clones:
        d.apply()
            
    
    print '%.0f' % (time.time() - t0) + ' seconds bumping dividends'
    
    #-----------------------------------------------------------------------    
    
    for i in inslist:
        insid = i.Name()
        pv = pv_Ins_acm(stf, i)
        cash = cash_Ins_acm(stf, i) 
        pvC_u[insid] = (pv, cash)
           
    sum = 0
    
    for d in div_clones:
        d.revert_apply()

    impact = []
    
    for k in pvC_u.keys():
                
        imp = (pvC_u[k][0] + pvC_u[k][1]) - (pvC_b[k][0] + pvC_b[k][1])
        sum = sum + imp
        impact.append((k, pvC_u[k][0], pvC_b[k][0], imp))
    
    
    print 'Total dividend impact: ', sum
    
    pvC_impact = open(outpath + stf + '_' + 'divImpact' + '_'+ dt_str + '_' + str(percbump) + '.xls', 'w')
    
    s = GenStrFromList('\t', '', 'BasePV', 'BumpPV', 'Impact')
    pvC_impact.write(s)
    
        
    for i in impact:
        s = GenStrFromList('\t', i[0], i[1], i[2], i[3])
        pvC_impact.write(s)
    
    s = GenStrFromList('\t', 'Total', '', '', sum)
    pvC_impact.write(s)
    
    pvC_impact.close()
       
    print '%.0f' % (time.time() - t1) + ' seconds calculating dividend impact'
            

ael_variables = [('TrdFilter', 'TrdFilter', 'string', TrdFilter(), 'MO_EqRisk_Index', 1),
                 ('OutPath', 'OutPath', 'string', None, 'f:\\temp\\', 1),
                 ('PercBump', 'PercBump', 'double', None, 1, 1)] 

def ael_main(ael_dict):

    stf = ael_dict['TrdFilter']
    outpath = ael_dict['OutPath']
    percbump = ael_dict['PercBump']
    
    divImpact(stf, outpath, percbump)


