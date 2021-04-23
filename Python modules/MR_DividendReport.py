import ael, acm, time, csv

month = {1:'March',2:'March',3:'March',4:'June',5:'June',6:'June',7:'September',8:'September',9:'September',10:'December',11:'December',12:'December'}

def TrdFilter():
    
    TrdFilter=[]
    
    for t in ael.TradeFilter:
        TrdFilter.append(t.fltid)
    TrdFilter.sort()
    
    return TrdFilter

def write_file(name, data):

    f = file(name, 'wb')
    c = csv.writer(f, dialect = 'excel')
    c.writerows(data)
    f.close() 
    
def ImpactDiv(temp,tf,outpath,percbump,Years,*rest):
    
    trf      = ael.TradeFilter[tf]
      
    UndList  = []
    
    #Getting all the underlying stocks from a Trade Filter in a list            
    for t in trf.trades():
        if t.insaddr.exp_day > ael.date_today():
            if t.insaddr.und_instype != 'None':
                if t.insaddr.und_instype == 'Stock':
                    UndName = t.insaddr.und_insaddr.insid
                    if UndName not in UndList:
                        UndList.append(UndName)

                elif t.insaddr.und_instype in ('EquityIndex', 'ZAR/ALSI'):
                    UndName = t.insaddr.und_insaddr
                    link    = UndName.combination_links()
                    for mem in link.members():
                        share = mem.member_insaddr.insid
                        if share not in UndList:
                            UndList.append(share)
       
    #*********************** PV Calculation Of The Entire Tradefilter **************#
    portfolio = acm.FTradeSelection[tf]
    grouper   = acm.FDefaultGrouper("Default")
    fiat      = acm.CreateInstrumentAndTradesTree(portfolio, grouper, None, 0, 0)
    tag       = acm.CreateEBTag()
    context   = 'Standard'        
    adfl      = 'object:*"valPLEnd"[isCashGrouping=0]' 
    eval      = acm.GetCalculatedValueFromString(fiat, context, adfl, tag) 
    pv        = eval.Value()   
    #********************* End PV Calculation *************************************#
    
    #Base PV Before The Bumps    
    BasePv    = pv 
    
    #Determines The Number Of Years For The Bumps    
    cut_off_date  = ael.date_today().add_years(Years) 
            
    UndList.sort()
          
    buckets  = {}
    dlist    = []
    MainList = []
            
    t0 = time.time()  
    
    #******************** Computation Of The Bumps On Dividends and The Impact *****#
    if len(UndList) != 0:
    
        print 'Loading...Please be patient...' 
             
        for stock in UndList: 
            stockDivsStream = ael.DividendStream.select("insaddr='%s'" % ael.Instrument[stock].insaddr)
            if stockDivsStream:
                divs = list(stockDivsStream)[0].clone()
                for p in divs.estimates():
                    if p.pay_day > ael.date_today() and p.pay_day <= cut_off_date:
                        
                        sy, sm, sd = p.pay_day.to_ymd()
                        ds = month[sm] + '-' + str(sy)
                        
                        if p.pay_day not in dlist:
                            dlist.append(p.pay_day)
                           
                        p.dividend = round(p.dividend*(1.0+ percbump/100.0), 6)
                        p.apply()
                        StressedPV  = eval.Value()  
                        p.revert_apply()
                        
                        impact = StressedPV  - BasePv
                        MainList.append([stock, ds, BasePv, StressedPV, impact])
    
    FinalList = []
    UndStock  = ['UNDERLYING STOCK']
    
    dlist.sort(lambda x, y: cmp(x, y))
      
    count = 1
    for d in dlist:
        
        sy, sm, sd = d.to_ymd()
        ds = month[sm] + '-' + str(sy)
        
        if ds not in buckets.keys():
            UndStock.append(ds)
            buckets[ds] = count
            count +=1
           
    FinalList.append(UndStock)
        
    MainList.sort()
    stock = MainList[0][0]
    ImpactList = [' ']*(len(dlist)+1)
    
    for x in MainList:
        
        if x[0] == stock:
            ImpactList[0] = x[0]
            ImpactList[buckets[x[1]]] = x[4]
            
        else:
            stock = x[0]
            FinalList.append(ImpactList)
            ImpactList = [' ']*(len(dlist)+1)
            ImpactList[0] = x[0]
            ImpactList[buckets[x[1]]] = x[4]
    
    FinalList.append(ImpactList) 
    
    write_file(outpath + tf + '.csv', FinalList)
    
    print 'Done...Please locate your file in F:\\temp...'
    print '%.0f' % (time.time() - t0) + ' seconds extracting an impact on bumped dividends'
    
ael_variables = [('TrdFilter', 'TrdFilter', 'string', TrdFilter(), 'MR_IndexArb_TIERII', 1),
                 ('OutPath', 'OutPath', 'string', None, 'f:\\temp\\', 1),
                 ('PercBump', 'PercBump', 'double', None, 1, 1),
                 ('Years', 'Years', 'int', None, 5, 1)]

def ael_main(ael_dict):

    stf      = ael_dict['TrdFilter']
    outpath  = ael_dict['OutPath']
    percbump = ael_dict['PercBump']
    Years    = ael_dict['Years']
    
    ImpactDiv(1, stf, outpath, percbump, Years)
