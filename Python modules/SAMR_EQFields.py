import ael

def EQFields(s,Outfile,*rest):    
    Global1=[]
    Global2=[]
    
    trds = ael.TradeFilter['MR_SingleStocks_TIERII']
    
    for t in trds.trades():
        
        ins = t.insaddr
        
        if ins.instype in ('Option', 'Future/Forward'):
            
            list=[]
            
            instype = ins.instype
            list.append(instype)
            
            insid = ins.insid
            list.append(insid)
            
            undtype = ins.und_insaddr.instype
            list.append(undtype)
            
            und = ins.und_insaddr.insid
            list.append(und)
            
            undval = ins.und_insaddr.used_price()
            list.append(undval)
            
            strike = ins.strike_price
            list.append(strike)
            
            exp = ins.exp_day
            list.append(exp)
            
            call = ins.call_option
            list.append(call)
            
            exertype = ins.exercise_type
            list.append(exertype)
            
            contrsize = ins.contr_size
            list.append(contrsize)
            
            quantity = t.quantity
            list.append(quantity)
            
            nominal = t.nominal_amount()
            list.append(nominal)
            
            vol = ins.used_vol()
            list.append(vol)
            
            mtm = ins.mtm_price(ael.date_today(), ins.curr.insid, 0, 0) 
            list.append(mtm)
            
            Global1.append(list)
        
        elif ins.instype in ('Stock'):
            
            list=[]        
            
            instype = ins.instype
            list.append(instype)
            
            insid = ins.insid
            list.append(insid)
            
            val = ins.used_price()
            list.append(val)
            
            quantity = t.quantity
            list.append(quantity)
            
            nominal = t.nominal_amount()
            list.append(nominal)
            
            Global2.append(list)
                
    Global1.sort()
    Global2.sort()        
            
    
    #outfile = '//services/frontnt/dart/ERM/SAMR_EQFields.csv'
    outfile = Outfile
    
    report = open(outfile, 'w')
    Headers1=[]
    Headers2=[]
    
    Headers1 = ['InsType', 'InsId', 'UndInsType', 'UndInsId', 'UndPrice', 'Strike', 'ExpDay', 'CallOption', 'ExerciseType', 'ContrSize', 'Quantity', 'Nominal', 'Volatility', 'MTMPrice']
    Headers2 = ['InsType', 'InsId', 'Price', 'Quantity', 'Nominal']
    
    for i in Headers1:
        
        report.write((str)(i))
        report.write(',')
    report.write('\n')
    
    for lsts in Global1:
        
        for ls in lsts:
            
            report.write((str)(ls))
            report.write(',')
        report.write('\n')
    
    for i in Headers2:
        
        report.write((str)(i))
        report.write(',')
    report.write('\n')
     
    for lsts in Global2:
        
        for ls in lsts:
            
            report.write((str)(ls))
            report.write(',')
        report.write('\n')
    
    report.close()
    return 'Success'
    #print 'The file has been saved at: C:\\CaraFields.csv'    
