import ael, InstrType, d860_count_resets, string

dt = ael.date_today()
fil = "c:\\ccc\\test.csv"

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
#       print l[3]
        inputdata.append(l)
        line = f.readline()
    f.close()
    return inputdata
    
def OutputFile(file, data):
    try:
        f = open(file, 'a')
    except:
        print 'File not opened for writing'
       
    f.writelines(data)
    f.close()


def HedgeStructure(struct):
    print 'Liab_ID', 'DealDate', 'DealDate', 'ResetDate', 'ResetDate', 'CFDate', 'CFDate', 'Nominal', 'cashflow', 'days', 'ResRate', 'Spread'    

def TradeCashflow(trd):
    #print 'INS','DevonNbr','Trdnbr','Resets','FixedFloat','FixedFloatDescription','ResetDay','ResetDate','CFDate','Duplicate','PayRec','Nominal','cashflow','days','Fixed','ResRate','Portfolio','TradeARea','CP','Contract','InsType'
    # print 'Trdnbr','NCDnbr','Deal_Date','Deal_Date','FixedFloatDescription','ResetDate','ResetDate','CFDate','CFDate','Nominal','cashflow','ResRate','Sprd','ResRateCln'
    #for t in trds:
    t = ael.Trade[(int)(trd[0])]
    Deal_Date = trd[2]
    NCDnbr = trd[3]
    #print t.pp()
    for  l in t.insaddr.legs():
        for c in l.cash_flows():                    
            Trdnbr = t.trdnbr
            if l.type == 'Float':
                FixedFloatDescription = 'Float' 
            else: FixedFloatDescription = l.type
                    
            ResetDate = c.start_day	
            ResetDate = c.start_day	
            CFDate = c.pay_day	
            CFDate = c.pay_day	
            Nominal = abs(t.quantity *t.insaddr.contr_size*c.nominal_factor)
            cashflow = c.projected_cf()*t.quantity
            ResRate = l.fixed_rate
            Sprd = l.spread
            ResRateCln = "ResRateCln"

    
                #Days = c.start_day.days_between(c.end_day) 
                                
            if l.type == 'Float':
                for r in c.resets():
                    
                    o =(Trdnbr+NCDnbr+Deal_Date+Deal_Date+FixedFloatDescription+ResetDate+ResetDate+CFDate+CFDate+Nominal+cashflow+ResRate+Sprd+ResRateCln)
                    OutputFile(o)
            else: 
                o =(Trdnbr+NCDnbr+Deal_Date+Deal_Date+FixedFloatDescription+ResetDate+ResetDate+CFDate+CFDate+Nominal+cashflow+ResRate+Sprd+ResRateCln)
                OutputFile(o)  
                        


ael_variables = \
[('Date', 'Run Date', 'date', dt, dt, 0, 0),
('flt', 'Filter', 'string', displayTF(), None, 0, 0),
('fil', 'Input filename', 'string', fil, None, 0, 0), ('ofil', 'Output filename', 'string', fil, None, 0, 0)]


def ael_main(dict):
    
    trds = ael.TradeFilter[dict.get('flt')].trades()
    trds = InputFile(dict.get('fil'))
    print 'Trdnbr', 'NCDnbr', 'Deal_Date', 'Deal_Date', 'FixedFloatDescription', 'ResetDate', 'ResetDate', 'CFDate', 'CFDate', 'Nominal', 'cashflow', 'ResRate', 'Sprd', 'ResRateCln'
    for trade in trds:
        print TradeCashflow(trade)
        x = 1
        
            

