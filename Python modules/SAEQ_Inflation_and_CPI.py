import ael

ael_variables = [('Instrument', 'Instrument', 'string', None, 'SACPI', 1),
                 #'ZAR/Investec_Global_Strategic_Equity'
                 ('Server', 'Server', 'string', None, 'C:\\FrontArena.CPIPrices.Midbase.m.'+ael.date_today().to_string('%Y%m%d')+'.dat', 1)]               
                 #'C:\\FrontArena.InvestecFundPrices.Midbase.d.'+ael.date_today().to_string('%Y%m%d')+'.dat'


def ael_main(ael_dict):
    
    Instrument = ael_dict["Instrument"]
    Server = ael_dict["Server"]
    
    print EQ_get_prices(Instrument, Server)
    

def EQ_get_prices(Inst,Server,*rest):
   
    Global=[]
    
    ins = ael.Instrument[Inst]
    
    if ins.insid == 'ZAR/Investec_Global_Strategic_Equity':
        Inv=[]
        date = ael.date_today().to_string('%Y/%m/%d')
        Price = ins.used_price(ael.date_today(), ins.curr.insid)

        Inv.append(date)
        Inv.append(Price)
        
        Global.append(Inv)
    
    elif ins.insid == 'SACPI':
        CPI=[]
        for p in ins.historical_prices():
            if p.ptynbr.ptyid in ['internal']: 
                list=[]
                dat = p.day
                date = dat.to_string('%Y/%m/%d')
                list.append(date)
                list.append(p.settle)
                CPI.append(list)
                
        CPI.sort()
        length = len(CPI)
        number=50
        
        start = (length-number)
        end = length
        
        count = start
        while count < length:
            Global.append(CPI[count])
            count += 1
    
    elif ins.insid == 'ZAR-GEMS':
    
        Gem=[]
        date = ael.date_today().to_string('%Y/%m/%d')
        Price = ins.used_price(ael.date_today(), ins.curr.insid)

        Gem.append(date)
        Gem.append(Price)
        
        Global.append(Gem)
    
    else:
        print 'Instrument not in AEL'


    outfile = Server
    report = open(outfile, 'w')    

    for g in Global:
        for f in g:
            if f == g[0]:
                report.write((str)(f))
                report.write('|')
            else:
                report.write((str)(f))
    
        report.write('\n')
        
    report.close()
    
    return 'Success'

