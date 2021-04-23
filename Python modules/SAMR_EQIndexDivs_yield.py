import ael, string

def IndexDiv(s,bdate,Outfile,*rest):
    Global=[]
    divisor = 1
    ins = ael.Instrument.select('instype = "EquityIndex"')
    TotalWeight = []
    TW = 0
    Counti = -1
    BDate = ael.date_from_string(bdate)
    
    for i in ins.members():
        link = i.combination_links()
        TW = 0
        for lnk in link.members():
            if lnk.member_insaddr.quote_type == 'Per 100 Units':
                divisor = 100
            else:
                divisor = 1
            mtm = lnk.member_insaddr.mtm_price(BDate, i.curr.insid, 0, 0)/divisor
            TW = TW + lnk.weight * mtm
        TotalWeight.append(TW)
        
    for i in ins.members():
        Counti = Counti + 1
        link = i.combination_links()
        for lnk in link.members():
            list=[]
            
            index = i.insid
            const = lnk.member_insaddr.insid
            weight = lnk.weight
            factor = i.index_factor
            
            if lnk.member_insaddr.quote_type == 'Per 100 Units':
                divisor = 100
            else:
                divisor = 1
            
            if i.quote_type == 'Per 100 Units':
                Index_divisor = 100
            else:
                Index_divisor = 1
                
            mtm = lnk.member_insaddr.mtm_price(BDate, i.curr.insid, 0, 0)/divisor
            #mtmindex = i.mtm_price(ael.date_today(),'ZAR',0,0)
            mtmindex = i.mtm_price(BDate, i.curr.insid, 0, 0)/Index_divisor
            if TotalWeight[Counti] == 0:
                NumInIndex = -200000
            else:
                if mtm == 0:
                    NumInIndex = -200000
                else:
                    NumInIndex = (weight * mtm) / TotalWeight[Counti] * mtmindex / mtm
            list.append(index)
            list.append(const)
            list.append(weight)
            list.append(factor)
            list.append(mtm)
            list.append(mtmindex)
            list.append(BDate)
            list.append(TotalWeight[Counti])
            list.append(NumInIndex)
            Global.append(list)
    
    Global.sort()
    #print Global
                   
    
    #outfile = '//services/frontnt/dart/ERM/SAMR_Eq_IndexDividends.csv'
    #outfile = '//v036syb004001/DART/ERM/SAMR_Eq_IndexDividends_yield.csv'
    outfile = Outfile
    
    report = open(outfile, 'w')
    Headers=[]
    
    Headers = ['IndexName', 'Constituent', 'Weight', 'Factor', 'ConstPrice', 'IndexPrice', 'Business_Date', 'CumIndexWeight', 'NumInIndex']
    
    for i in Headers:
        report.write((str)(i))
        report.write(';')
    report.write('\n')
    report.write('\n')
        
    
    for lsts in Global:
        
        for ls in lsts:
            report.write((str)(ls))
            report.write(';')
       
        report.write('\n')
        
    report.close()
    
    return 'Success'
    #print 'The file has been saved at: C:\\DeClercqIndex.csv'
    


