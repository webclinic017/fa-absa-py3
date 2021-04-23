import ael, string, math
import InstrType

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
    	outfile=open('c:\\ConfirmationE\Swap\SwapExport.txt', 'w')
	
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' 
    	%('TradeNo', 'FullName', 'Fax', 'CP', 'ISDA', 'Law', 'LawCurr', 'Curr', 'Nominal', 'TradeDate', 'EffectiveDate',
    	'EndDate', 'FixedPayer', 'FixedRate', 'DayCount', 'dc', 'FloatPayer', 'Spread', 'Index',
    	'DesMaturity', 'Calendar', 'Calendar2', 'Address1', 'Address2', 'ZipCode', 'City', 'Country', 
    	'Date', 'FixPayDay', 'FloatPayDay', 'DayCountFloat', 'DayCountFixed', 'Template',
	'BreakForm', 'BreakType', 'BreakStart', 'BreakEnd', 'BreakDay', 'ExBusDays', 'BreakPlace',
    	'Attention', 'ComType', 'AName', 'AAccount'))
	
#    	'strfix', 'RollPeriod', 'DayCount', 
#    	'Calendar', 'Start', 'End', 'Nominal', 'FloatRef', 'Spread'))	  
		
	outfile.close()

	return 'Success'

    except: 
    	raise 'cant open'
    	print 'cant open'
	return 'Error opening file'





def conTest(t,*rest):

    try: 
    	outfile=open('c:\\ConfirmationE\Swap\SwapExport.txt', 'a')
    except: 
    	raise 'cant open'
    	print 'cant open'
    

    ####### ISDA & template #######
    Law = ''
    LawCurr = ''
    ISDA = ''
    template = 'LONG FORM'
    nbr =  t.counterparty_ptynbr.ptynbr
    a = ael.Agreement.select("counterparty_ptynbr = %i" %nbr)
    for i in a:
    	if i.document_type_chlnbr.entry != 'ISDA' or i.dated == None: 
	
	    ISDA = '0001-01-01'
    	    template = 'LONG FORM'
	    
    	    ####### Law #######	    
    	    Law = t.counterparty_ptynbr.free1_chlnbr.entry
    	    if Law == 'SA':
    	        Law = 'South African'
    	        LawCurr = 'South African Rands'
    	    elif Law == 'ENG':
    	        Law = 'English'
    	        LawCurr = 'United States Dollars'
#	    else:
#	    	return 'Error - No Law type specified'
		
	else:
	    if i.document_type_chlnbr.entry == 'ISDA':
	    	ISDA = i.dated
	    	template = 'SHORT FORM'



    TradeNo = t.trdnbr
    Curr = t.insaddr.curr.insid
    Nominal = real_round(t.nominal_amount(), 0)
    
#    print 'XXXXXXXXXXXXXXXXXXXXXXXX', Nominal
#    print
    
    TradeDate = ael.date_from_time(t.time)
    
    p = t.counterparty_ptynbr
    FullName = p.fullname
    
    if t.nominal_amount() < 0:
    	FixedPayer = FullName
	FloatPayer = 'ABSA BANK LIMITED'
    else:
    	FixedPayer = 'ABSA BANK LIMITED'
	FloatPayer = FullName
	
  


    ####### FAX & Email #######
  
    CP = p.ptyid
    if p.address == '':
    	Address1 = 'PLEASE ADVISE'
    else:
    	Address1 = p.address
	
    Address2 = p.address2
    ZipCode = p.zipcode
    City = p.city
    Fax = p.fax
    Country = p.country
    Attention = p.attention
    ComType = ''
    
    flag = 0
    act = p.accounts()
    AName = ''
    AAccount = ''
    if len(act) > 0:
        for a in act:
            if a.accounting == 'IRD':
                AName = a.name
                AAccount = a.account
            else:
                AName = ''
                AAccount = ''
    	

    
    l = t.insaddr.legs()[0]
    EffectiveDate = l.start_day
    EndDate = l.end_day
    DayCount = l.daycount_method
    if Curr == 'ZAR':
    	dc = '(Fixed)'
    else:
    	dc = ''
	
    
    Date = ael.date_today()
    
    try:
    	Calendar1 = l.pay_calnbr.calid
    except:
#    	print 'No pay calendar'
	Calendar1 = ''
	    
    try:
    	Calendar2 = l.pay2_calnbr.calid
    except:
#    	print 'No pay calendar2'
	Calendar2 = ''
	
	

    ####### BREAK CLAUSE #######
    term = l.start_day.years_between(t.insaddr.exp_day)
    if term > 3:
	BreakType = 'European'
	BreakForm = 'Yes'
	BreakPlace = 'Johannesburg'
	ExBusDays = 'London and Johannesburg'
    elif term > 5:
	BreakType = 'Bermuda'
	BreakForm = 'Yes'
        if t.insaddr.curr.insid == 'EUR':
    	    BreakPlace = 'Brussels'
	    ExBusDays = 'London and Target Settlement Day'
    	else:
    	    BreakPlace = 'Johannesburg'
	    ExBusDays = 'London and Johannesburg'

    else: 
    	BreakType = 'None'
	BreakForm = 'No'
	BreakPlace = 'None'
	ExBusDays = 'None'
    
    
    BreakDay = l.start_day.to_string("%d %B")

    #start + 3yr
    BreakStart = (l.start_day.add_years(3)).adjust_to_banking_day(t.insaddr.curr)
    
    #exp - 1yr
    BreakEnd = (t.insaddr.exp_day.add_years(-1)).adjust_to_banking_day(t.insaddr.curr) 



	
    ####### Leg Details #######	
    legs = t.insaddr.legs()
    
    for l in legs:

	if l.type == 'Float':

	    flpyday = ''
	
	    if l.float_rate.insid.find('JIBAR') != -1:
	    	Index = 'ZAR-JIBAR-SAFEX'
	    elif l.float_rate.insid.find('USD-LIBOR') != -1:
	    	Index = 'USD-LIBOR-BBA'
	    else: Index = l.float_rate.insid
	    

	    dict = {'m':'Months','y':'Years','d':'Days'}
    	    field = l.rolling_period
    	    amount = field.rstrip(field[len(field)-1])
    	    c = field[len(field)-1]
    	    DesMaturity =  (str)(amount) + ' ' + dict[c]
	    
	    DayCountFloat = l.daycount_method
	      
	    if l.spread == 0:
	    	Spread = 'None'
	    else:
	    	Spread = l.spread
	   
    		    	
    	    cshflws = l.cash_flows()
	    	    
    	    flag = 0
    	    for c in cshflws:
	    	if flag == 0:
		    flpyday = flpyday + str(c.pay_day)
	     	    flag = 1
		else:
		    flpyday = flpyday + '; ' + str(c.pay_day)

	    	    
	if l.type == 'Fixed':
	
    	    fixpyday = ''
	    FixedRate = l.fixed_rate
	    DayCountFixed = l.daycount_method
	    
	      		    	
    	    cshflws = l.cash_flows()
	    	    
    	    flag = 0
    	    for c in cshflws:
	    	if flag == 0:
	    	    fixpyday = fixpyday + str(c.pay_day)
	    	    flag = 1
    	    	else:
	    	    fixpyday = fixpyday + '; ' + str(c.pay_day)




    print TradeNo, FullName, Fax, CP, ISDA, Law, LawCurr,
    print Curr, Nominal, TradeDate, EffectiveDate, EndDate
    print FixedPayer, FixedRate, DayCount, dc, FloatPayer 
    print Spread, Index, DesMaturity, Calendar1, Calendar2
    print Address1, Address2, ZipCode, City, Country, Date
    print fixpyday, flpyday, DayCountFloat, DayCountFixed, template
    print BreakForm, BreakType, BreakStart, BreakEnd, BreakDay, ExBusDays, BreakPlace
    print Attention, ComType


    outfile.write('%s,%s,%s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'  
    
    %(TradeNo, FullName, Fax, CP, ISDA, Law, LawCurr,
    Curr, Nominal, TradeDate, EffectiveDate, EndDate,
    FixedPayer, FixedRate, DayCount, dc, FloatPayer,
    Spread, Index,  DesMaturity, Calendar1, Calendar2,
    Address1, Address2, ZipCode, City, Country, Date,
    fixpyday, flpyday, DayCountFloat, DayCountFixed, template,
    BreakForm, BreakType, BreakStart, BreakEnd, BreakDay, ExBusDays, BreakPlace,
    Attention, ComType,  AName, AAccount))
    
    outfile.close()
		    
    return 'Success'			    


### main 
#689391
#t= ael.Trade[689391]
#print OpenFile('1')
#print conTest(t)
