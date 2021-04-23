import ael, string, math, time
import InstrType
FileOutPut = 'Y:\\Jhb\\Arena\\Data\\PCG-Client-Valuations\\' + str(time.localtime()) + '.txt'
def real_round(number, dec):

    r = round(number, dec)

    if dec == 0:

        return str(int(r))

    else:

        str_dec = str(r - math.floor(r))

        zeros = dec + 2 - len(str_dec)

        return str(r) + zeros * '0' 
        
def OpenFile(temp, *rest):
    

    try:
        
        outfile = open(FileOutPut, 'w')
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%('Trade_Ref', 'Trade_Date', 'Maturity_Date', 'Instrument', 'Currency1', 'Nominal_1', 'Currency2', 'Nominal_2', 'Spot_1', 'PV_1', 'MTM_ZAR', 'Date_Today', 'Valuation_Date', 'CounterpartyName', 'Trade_Filter'))
        
        outfile.close()
        
        return 'Success'
    except:
    	raise 'cant open'
    	print 'cant open'
	return 'Error opening file'

def conTest(temp, t, date, Curr, MTM_ZAR, Trade_Filter, *rest):
    
    try:
        outfile=open(FileOutPut, 'a')
    except:
    	raise 'cant open'
    	print 'cant open'

    
    if t.insaddr.instype == 'Deposit' and t.insaddr.legs().members!= [] and t.insaddr.legs()[0].type in ('Call Fixed Adjustable', 'Fixed', 'Float', 'Call Fixed', 'Call Float', 'Fixed Adjustable'):
        Instrument = ''
        CounterpartyName = ''
        Trade_Ref = ''
        Trade_Date = ''
        PV_1 = ''
        Date_Today = ''
        Maturity_Date = ''
        Spot_1 = ''
        Valuation_Date = ''
        Currency1 = ''
        Currency2 = ''
        Nominal_1 = ''
        Nominal_2 = ''
        legs = ''
        MTM_ZAR = ''
        Trade_Filter = ''
        Total_PV_ZAR = ''
       
    else:
        Instrument = t.insaddr.instype
        CounterpartyName = t.counterparty_ptynbr.fullname
        Trade_Ref = t.trdnbr
        #print Trade_Ref
        #Trade_Date = ael.date_from_time(t.time)
        Trade_Date = ael.date_from_time(t.time)
        PV_1 = real_round(t.present_value(), 0)
        Date_Today = ael.date_today()
        Maturity_Date = t.insaddr.exp_day
        if t.insaddr.instype != 'FxSwap':
            if t.insaddr.spot_price() != 0:
                Spot_1 = real_round(t.insaddr.spot_price(), 0)
            elif t.insaddr.spot_price() == 0:
                Spot_1 = real_round(t.present_value(), 0)
        Valuation_Date = ael.date(date)
        leg = t.insaddr.legs()
        Currency1 = t.curr.insid
        #Currency2 = ''
        Nominal_1 = real_round(t.nominal_amount(), 0)
        #Nominal_2 = 0
        
        if t.insaddr.legs() and t.insaddr.instype not in ('Cap', 'Floor', 'Swap'):
            if t.insaddr.instype in ('FxSwap', 'Swap', 'CurrSwap', 'FRA', 'IndexLinkedBond', 'IndexLinkedSwap', 'Bond', 'CD', 'FRN', 'FreeDefCF'):
            
                for l in leg:
                    if l.payleg == 1:
                        Currency1 = l.curr.insid
                        cashflows = l.cash_flows()
                        for cf in cashflows:
                            Nominal_1 = real_round(cf.projected_cf(), 0) 
                            #print Nominal_1
                            
                    else:
                        Currency2 = l.curr.insid
                        cashflows = l.cash_flows()
                        for cf in cashflows:
                            Nominal_2 = real_round(cf.projected_cf(), 0)
                            #print  Nominal_2
                        if t.insaddr.instype == 'FxSwap':
                            Spot_1 = real_round(abs(float(Nominal_1)/float(Nominal_2)), 0)
            else:
                if l.payleg == 1:
                    Currency1 = l.curr.insid
                    cashflows = l.cash_flows()
                    for cf in cashflows:
                        Nominal_1 = real_round(l.nominal_amount(date, Currency1), 0) 
                    
                    
                elif l.payleg == 0:
                    Currency2 = l.curr.insid
                    cashflows = l.cash_flows()
                    for cf in cashflows:
                        Nominal_2 = real_round(l.nominal_amount(date, Currency1), 0) 
                    
        else:
            Currency1 = t.curr.insid
            Nominal_1 = real_round(t.nominal_amount(), 0)
            Currency2 = Currency1
            Nominal_2 = Nominal_1
        
        #print Nominal_1
        #print Nominal_2
        MTM_ZAR = real_round(MTM_ZAR, 0)
        Trade_Filter = Trade_Filter
        #Total_PV_ZAR = 'N/A'
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(Trade_Ref, Trade_Date, Maturity_Date, Instrument, Currency1, Nominal_1, Currency2, Nominal_2, Spot_1, PV_1, MTM_ZAR, Date_Today, Valuation_Date, CounterpartyName, Trade_Filter))
            
        outfile.close()
        
        return 'Success'

def OpenFile(temp, *rest):
    
    try:
        
        outfile = open(FileOutPut, 'w')
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%('Trade_Ref', 'Trade_Date', 'Maturity_Date', 'Instrument', 'Currency1', 'Nominal_1', 'Currency2', 'Nominal_2', 'Spot_1', 'PV_1', 'MTM_ZAR', 'Date_Today', 'Valuation_Date', 'CounterpartyName', 'Trade_Filter'))
        
        outfile.close()
        
        return 'Success'
    except:
    	raise 'cant open'
    	print 'cant open'
	return 'Error opening file'
def mtm_zar_sum(temp, Total, *rest):
    
    try:
        
        outfile=open(FileOutPut, 'a')
    except:
    	raise 'cant open'
    	print 'cant open'
    Instrument = 'N/A'
    CounterpartyName = 'N/A'
    Trade_Ref = 'Total'
    Trade_Date = 'N/A'
    PV_1 = 'N/A'
    Date_Today = 'N/A'
    Maturity_Date = 'N/A'
    Spot_1 = 'N/A'
    Valuation_Date = 'N/A'
    Currency1 = 'N/A'
    Currency2 = 'N/A'
    Nominal_1 = 'N/A'
    Nominal_2 = 'N/A'
    legs = 'N/A'
    MTM_ZAR = real_round(Total, 0) 
    #otal_PV_ZAR = real_round(Total,0)
    Trade_Filter = 'N/A'
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(Trade_Ref, Trade_Date, Maturity_Date, Instrument, Currency1, Nominal_1, Currency2, Nominal_2, Spot_1, PV_1, MTM_ZAR, Date_Today, Valuation_Date, CounterpartyName, Trade_Filter))
    
            
    outfile.close()
        
    return 'Success'        


### main
