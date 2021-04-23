import ael, string

def IndexDiv(s,Outfile,*rest):
    Global=[]
    
    ins = ael.Instrument.select('instype = "EquityIndex"')
    
    for i in ins.members():
    
        link = i.combination_links()
        
        for lnk in link.members():
            list=[]
            
            index = i.insid
            const = lnk.member_insaddr.insid
            weight = lnk.weight
            factor = i.index_factor
           
            mtm = lnk.member_insaddr.mtm_price(ael.date_today(), i.curr.insid, 0, 0)
            mtmindex = i.mtm_price(ael.date_today(), i.curr.insid, 0, 0)
            
            list.append(index)
            list.append(const)
            list.append(weight)
            list.append(factor)
            list.append(mtm)
            list.append(mtmindex)
            list.append(ael.date_today())
            Global.append(list)
    
    Global.sort()
    #print Global
                   
    
    #outfile = '//services/frontnt/dart/ERM/SAMR_Eq_IndexDividends.csv'
    outfile = Outfile
    
    report = open(outfile, 'w')
    Headers=[]
    
    Headers = ['IndexName', 'Constituent', 'Weight', 'Factor', 'ConstPrice', 'IndexPrice', 'DATA_Date']
    
    for i in Headers:
        report.write((str)(i))
        report.write(',')
    report.write('\n')
        
    
    for lsts in Global:
        
        for ls in lsts:
            report.write((str)(ls))
            report.write(',')
       
        report.write('\n')
        
    report.close()
    
    return 'Success'
    #print 'The file has been saved at: C:\\DeClercqIndex.csv'
    


