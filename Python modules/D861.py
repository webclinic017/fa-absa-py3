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
                print d
        f.close()
        

def OutputData(data):    
    print data.keys().sort()
                
        



def BondCashflow(instrument):
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
                if c.type != 'Fixed Amount':
                    ResetDate = c.start_day.to_string('%d-%b-%y')
                    CFDate = c.pay_day.to_string('%d-%b-%y')	
                    cashflow = c.projected_cf()
                    days = c.start_day.days_between(c.end_day, 'act/365')
                    Spread = l.spread
                    if l.type == 'Float':
                        for r in c.resets():
                            Cash.append([Liab_ID, DealDate, Days(DealDate), ResetDate, Days(ResetDate), CFDate, Days(CFDate), Nominal, cashflow, days, r.value, Spread])                    
                    else: 
                        Cash.append([Liab_ID, DealDate, Days(DealDate), ResetDate, Days(ResetDate), CFDate, Days(CFDate), Nominal, cashflow, days, ResRate, Spread])                    
        
    return Cash
    
def SwapCashflow(trdes):
    try:
        Cash = []
        for trd in trdes:
            t = ael.Trade[(int)(trd[0])]
            Deal_Date = trd[2]
            NCDnbr = trd[3]
            Nominal = float(trd[1])
            if abs(Nominal) > abs(t.nominal_amount()):
                #raise "Trade :" + str(t.trdnbr) + " Nominal is greater than the nominal in front" ,Nominal , t.nominal_amount()
                print "Trade :" + str(t.trdnbr) + " Nominal is greater than the nominal in front", Nominal, t.nominal_amount(), t.maturity_date()
    
            
            for  l in t.insaddr.legs():
                for c in l.cash_flows():                    
                    Trdnbr = t.trdnbr
                    if l.type == 'Float':
                        FixedFloatDescription = 'Float' 
                    else: FixedFloatDescription = l.type                    
                    ResetDate = c.start_day.to_string('%d-%b-%y')	
                    CFDate = c.pay_day.to_string('%d-%b-%y')	
                    cashflow = c.projected_cf()*t.quantity
                    ResRate = l.fixed_rate
                    Sprd = l.spread
                    ResRateCln = " "
        
            
                        #Days = c.start_day.days_between(c.end_day) 
                                        
                    if l.type == 'Float':
                        for r in c.resets():
                            ResRate = r.value
                            ResRateCln = ResRate - Sprd
                            #Cash.append([Trdnbr,NCDnbr,Deal_Date,Days(Deal_Date),FixedFloatDescription,ResetDate,Days(ResetDate),CFDate,Days(CFDate),Nominal,cashflow,ResRate,Sprd,ResRateCln])                    
                            Cash.append([NCDnbr, Trdnbr, FixedFloatDescription, ResetDate, Deal_Date, Days(Deal_Date), Days(ResetDate), CFDate, Days(CFDate), Nominal, cashflow, ResRate, Sprd, ResRateCln])                    
                            #-Cash[NCDnbr,Trdnbr,FixedFloatDescription,ResetDate] = [Trdnbr,NCDnbr,Deal_Date,Days(Deal_Date),FixedFloatDescription,ResetDate,Days(ResetDate),CFDate,Days(CFDate),Nominal,cashflow,ResRate,Sprd,ResRateCln]                    
                    else: 
                        ResRateCln = ResRate - Sprd
                        #Cash.append([Trdnbr,NCDnbr,Deal_Date,Days(Deal_Date),FixedFloatDescription,ResetDate,Days(ResetDate),CFDate,Days(CFDate),Nominal,cashflow,ResRate,Sprd,ResRateCln])                  
                        Cash.append([NCDnbr, Trdnbr, FixedFloatDescription, ResetDate, Deal_Date, Days(Deal_Date), Days(ResetDate), CFDate, Days(CFDate), Nominal, cashflow, ResRate, Sprd, ResRateCln])                    
                        #-Cash[NCDnbr,Trdnbr,FixedFloatDescription,ResetDate] = [Trdnbr,NCDnbr,Deal_Date,Days(Deal_Date),FixedFloatDescription,ResetDate,Days(ResetDate),CFDate,Days(CFDate),Nominal,cashflow,ResRate,Sprd,ResRateCln]
                        #print Cash.keys(),Cash
        Cash.sort()
        return Cash
    except: 
        print trd    
        

ael_variables = [('swapsin', 'Input Swaps filename', 'string'),
                ('swapsout', 'Output Swaps filename', 'string'),
                #('bondsin', 'Input Bonds filename', 'string'),
                ('bondsout', 'Output Bonds filename', 'string')]


def ael_main(dict):
    
    LiabsCheck = []
    Liabs = []
    trds = InputFile(dict.get('swapsin'))


    fields = ['Trdnbr', 'NCDnbr', 'Deal_Date', 'Deal_Date', 'FixedFloatDescription', 'ResetDate', 'ResetDate', 'CFDate', 'CFDate', 'Nominal', 'cashflow', 'ResRate', 'Sprd', 'ResRateCln']
    x =  createfile(dict.get('swapsout'), fields)       
    #print trds.keys()        
    #for trade in trds:
        #x = OutputFile(dict.get('swapsout'),SwapCashflow(trade))
    x =SwapCashflow(InputFile(dict.get('swapsin')))
    for c in x:
        print c
        #if  trade[3] not in LiabsCheck:
        #        LiabsCheck.append(trade[3])
        #        Liabs.append(trade)
    
    #fields = ['Liab_ID','DealDate','DealDate','ResetDate','ResetDate','CFDate','CFDate','Nominal','cashflow','days','ResRate','Spread']    
    #x =  createfile(dict.get('bondsout'),fields)      
    #Liabs.sort()
    #print Liabs.keys()        
    #for b in Liabs:
       # x = OutputFile(dict.get('bondsout'),BondCashflow(b))

         
   
        
        

