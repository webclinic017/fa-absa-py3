import ael, InstrType, d860_count_resets, string

dt = ael.date_today()

   
    
def Days(d):
    return ael.date('1900-01-01').days_between(ael.date(d), 'Act/365' ) + 2
    
def formatString(list):
    format =''
    for l in list:
        format = format + str(l) + ','
    return format
    
def createfile(file, heading):
    try:
        f = open(file, 'w')
    except:
        print 'File not opened for writing'
    
    f.write('%s\n' % formatString(heading))
    f.close()
    return        
    
def displayTF():
    filterlst = []
    for f in ael.TradeFilter.select():
        filterlst.append(f.fltid)
    filterlst.sort()
    return filterlst

def InputFile(file):
    try:
        f = open(file, 'r')
    except:
        print 'File not opened'
    line = f.readline()
# Ignore headings
    line = f.readline()  
    inputdata = []
    while line:
        l = []  
        l = string.split(line, ',')
        inputdata.append(l)
        line = f.readline()
    f.close()
    return inputdata
    
def OutputFile(file, data):
    try:
        f = open(file, 'a')
    except:
        print 'File not opened for writing'
 
    if data != None:
        for d in data:   
                f.write('%s\n'%formatString(d))
        f.close()


def BondCashflow(instrument):
    try:
        t = ael.Trade[(int)(instrument[0])]
        ExtNom = float(instrument[1])
        Liab_ID = instrument[3]
        ins = ael.Instrument[str(instrument[4])]
        Nominal = instrument[5]
        
        if abs(ExtNom) > abs(t.nominal_amount()):
            #raise "Trade :" + str(t.trdnbr) +" Nominal is greater than the nominal in front" 
            print "Trade :" + str(t.trdnbr) +" Nominal is greater than the nominal in front", ExtNom, t.nominal_amount(), t.maturity_date()
    
        ResRate = ""
        DealDate = instrument[2]
        Cash = []
        
        if  Nominal not in ('C', 'R'):    
            for l in ins.legs():
                for c in l.cash_flows():
                    #print  ins.insid,t.quantity,c.projected_cf(c.start_day,c.end_day), Nominal , t.nominal_amount()
                    #if t.nominal_amount() == 0 or Nominal in ('N','C'):
                    #print t.quantity,c.projected_cf(c.start_day,c.end_day),(int)(Nominal) , t.nominal_amount()   
                    #cashflow = t.quantity*c.projected_cf(c.start_day,c.end_day)*((int)(Nominal) / t.nominal_amount())                
                    #else:
                
                    cashflow = t.quantity*c.projected_cf()*((int)(Nominal) / t.nominal_amount())                
                    if Liab_ID == 'ABS51':
                        print t.trdnbr, t.quantity, c.projected_cf(), Nominal, t.nominal_amount(), c.start_day, c.end_day, cashflow

                    
#t.nominal_amount()
                    if c.type != 'Fixed Amount':
                        ResetDate = c.start_day.to_string('%d-%b-%y')
                        CFDate = c.pay_day.to_string('%d-%b-%y')	
                        #if t.nominal_amount() == 0:
                        #    cashflow = 0
                        #else:
                        #cashflow = t.quantity*c.projected_cf(c.start_day,c.end_day)*((int)(Nominal) / t.nominal_amount())
                        days = c.start_day.days_between(c.end_day, 'act/365')
                        Spread = l.spread
                    if c.type == 'Fixed Amount':
                        ResetDate = l.start_day.to_string('%d-%b-%y')
                        CFDate = c.pay_day.to_string('%d-%b-%y')	
                        #if t.nominal_amount() == 0:
                        #    cashflow = 0
                        #else:
                        #cashflow = t.quantity*c.projected_cf(c.start_day,c.end_day)*((int)(Nominal) / t.nominal_amount())
                        days = l.start_day.days_between(l.end_day, 'act/365')
                        Spread = l.spread
                    
                    #if l.type == 'Float':
                    #        for r in c.resets():
                    #            Cash.append([Liab_ID,DealDate,Days(DealDate),ResetDate,Days(ResetDate),CFDate,Days(CFDate),Nominal,cashflow,days,r.value,Spread])                    
                    #if l.type == 'Fixed':
                    ResRate = l.fixed_rate
                    if ExtNom != 0:
                        Cash.append([Liab_ID, DealDate, Days(DealDate), ResetDate, Days(ResetDate), CFDate, Days(CFDate), Nominal, cashflow, days, ResRate, Spread])                    
           
        return Cash
    except: instrument, " This instrument does not exist"
    
def SwapCashflow(trd):
   # try:
        t = ael.Trade[(int)(trd[0])]
        Deal_Date = trd[2]
        NCDnbr = trd[3]
        Nominal = float(trd[1])
        DesigDate = ael.date(Deal_Date)
    
        if DesigDate >= ael.date_today().first_day_of_month() and DesigDate <= ael.date_today():
            DealIndi = 'DD'
        else: DealIndi = 'ED'
        
        if abs(Nominal) > abs(t.nominal_amount()):
            #raise "Trade :" + str(t.trdnbr) + " Nominal is greater than the nominal in front" ,Nominal , t.nominal_amount()
            print "Trade :" + str(t.trdnbr) + " Nominal is greater than the nominal in front", Nominal, t.nominal_amount(), t.maturity_date()
        if NCDnbr == "CFH" :
            Nominal = -1 * Nominal

        Cash = []
        for  l in t.insaddr.legs():
            for c in l.cash_flows():                    
                Trdnbr = t.trdnbr
                if l.type == 'Float':
                    FixedFloatDescription = 'Float' 
                else: FixedFloatDescription = l.type                    
                ResetDate = c.start_day.to_string('%d-%b-%y')	
                CFDate = c.pay_day.to_string('%d-%b-%y')
   

                if t.quantity == 0:
                    cashflow = 0
                else:
                    cashflow = c.projected_cf()*t.quantity *(Nominal / (t.quantity*t.insaddr.contr_size))
                
                if NCDnbr == "CFH" :
                    cashflow = -1 * cashflow
                
                if t.trdnbr == 609984:
                    print t.trdnbr, c.projected_cf(), t.quantity, Nominal, t.nominal_amount(), cashflow, (t.quantity*t.insaddr.contr_size)
                    
                ResRate = l.fixed_rate
                Sprd = l.spread
                ResRateCln = " "
    
        
                    #Days = c.start_day.days_between(c.end_day) 
          
                if l.type == 'Float':
                    for r in c.resets():
                        ResRate = r.value
                        #ResRateCln = ResRate - Sprd
                        ResRateCln = ResRate 
                        days0 = abs(ael.date(CFDate).days_between(ael.date(ResetDate), 'act/365'))
                        if Nominal != 0:
                            Cash.append([Trdnbr, NCDnbr, Deal_Date, Days(Deal_Date), ResetDate, Days(ResetDate), CFDate, Days(CFDate), FixedFloatDescription, Nominal, cashflow, days0, ResRate, Sprd, ResRateCln, DealIndi])                    
                else: 
                    #ResRateCln = ResRate - Sprd
                    ResRateCln = ResRate 
                    days0 = abs(ael.date(CFDate).days_between(ael.date(ResetDate), 'act/365'))
                    if Nominal != 0:
                        Cash.append([Trdnbr, NCDnbr, Deal_Date, Days(Deal_Date), ResetDate, Days(ResetDate), CFDate, Days(CFDate), FixedFloatDescription, Nominal, cashflow, days0, ResRate, Sprd, ResRateCln, DealIndi])                    
            
        return Cash
   # except: 
   #     print trd, "This record has problem"    
        

ael_variables = [('swapsin', 'Input Swaps filename', 'string'),
                ('swapsout', 'Output Swaps filename', 'string'),
                #('bondsin', 'Input Bonds filename', 'string'),
                ('bondsout', 'Output Bonds filename', 'string')]


def ael_main(dict):
    
    LiabsCheck = []
    Liabs = []
    trds = InputFile(dict.get('swapsin'))
    

    fields = ['Trdnbr', 'NCDnbr', 'Deal_Date', 'Deal_Date', 'ResetDate', 'ResetDate', 'CFDate', 'CFDate', 'FixedFloatDescription', 'Nominal', 'cashflow', 'Days', 'ResRate', 'Sprd', 'ResRateCln', 'DealIndi']
    x =  createfile(dict.get('swapsout'), fields)
          
    for trade in trds:
        x = OutputFile(dict.get('swapsout'), SwapCashflow(trade))
        if  trade[3] not in LiabsCheck:
                LiabsCheck.append(trade[3])
                Liabs.append(trade)
    #for j in Liabs:
    #    print j
    fields = ['Liab_ID', 'DealDate', 'DealDate', 'ResetDate', 'ResetDate', 'CFDate', 'CFDate', 'Nominal', 'cashflow', 'days', 'ResRate', 'Spread']    
    x =  createfile(dict.get('bondsout'), fields)      
    for b in Liabs:
        x = OutputFile(dict.get('bondsout'), BondCashflow(b))
    
         
   
        
        

