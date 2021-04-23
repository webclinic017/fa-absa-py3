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
    	outfile=open('F:\Confirmations\FRA\FraExport.txt', 'w')
    	
	
    	outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' 
    	%('TradeNo', 'FullName', 'Fax', 'CP', 'ISDA', 'Law', 'LawCurr', 'Curr', 'Nominal', 'TradeDate', 'EffectiveDate',
    	'EndDate', 'FixedPayer', 'FixedRate', 'DayCount', 'dc', 'FloatPayer', 'Spread', 'Index',
    	'DesMaturity', 'Calendar', 'Calendar2', 'Address1', 'Address2', 'ZipCode', 'City', 'Country', 
    	'Date', 'FixPayDay', 'FloatPayDay', 'DayCountFloat', 'DayCountFixed', 'Template',
	'BreakForm', 'BreakType', 'BreakStart', 'BreakEnd', 'BreakDay', 'ExBusDays', 'BreakPlace',
    	'Attention', 'ComType', 'AName', 'AAccount', 'Branch', 'AccountNbr', 'BranchCode', 'Swift'))
	
#    	'strfix', 'RollPeriod', 'DayCount', 
#    	'Calendar', 'Start', 'End', 'Nominal', 'FloatRef', 'Spread'))	  
		
	outfile.close()
	

	return 'Success'

    except: 
        print 'cant open'
    	raise Exception('cant open')
	return 'Error opening file'





def conTest(temp, t,*rest):

    try: 
    	outfile=open('F:\Confirmations\FRA\FraExport.txt', 'a')
    except: 
    	print 'cant open'
    	raise Exception('cant open')
    

    ####### ISDA & template #######
    Law = ''
    LawCurr = ''
    ISDA = ''
    template = 'LONG FORM'
    nbr =  t.counterparty_ptynbr.ptynbr
    a = ael.Agreement.select("counterparty_ptynbr = %i" %nbr)
    for i in a:
        if i.document_type_chlnbr == None: 
	
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
    #Nominal = abs(t.nominal_amount())
    Nominal = real_round(abs(t.nominal_amount(t.value_day)), 0)
    
    
#    print 'XXXXXXXXXXXXXXXXXXXXXXXX', Nominal
#    print
    
    TradeDate = ael.date_from_time(t.time)
    
    p = t.counterparty_ptynbr
    FullName = p.fullname.replace(',', ' ')
    
    Fax = p.fax
    
    Attention = p.attention
    
    if  t.nominal_amount() < 0:
    	FixedPayer = FullName
	FloatPayer = 'ABSA BANK LIMITED'
    else:
    	FixedPayer = 'ABSA BANK LIMITED'
	FloatPayer = FullName


# Absa Bank Details
	
    if t.insaddr.curr.insid == 'ZAR':
        Branch = 'ABSA Eloff Street (AbsaDirect)'
        AccountNbr = '660 158 642'
        BranchCode = '632505'
        Swift = 'ABSAZAJJ'
        
    elif t.insaddr.curr.insid == 'EUR':
        Branch = 'BARCLAYS BANK LONDON'
        AccountNbr = '66986655'
        BranchCode = ''
        Swift = 'BARCGB22'
        
    elif t.insaddr.curr.insid == 'USD':
        Branch = 'BARCLAYS BANK NEW YORK'
        AccountNbr = '050038826'
        BranchCode = 'ABA026002574'
        Swift = 'BARCUS33'

    elif t.insaddr.curr.insid == 'GBP':
        Branch = 'BARCLAYS BANK LONDON'
        AccountNbr = '80642592'
        BranchCode = '//SC 20-32-53'
        Swift = 'BARCGB22'
    
    else:
        Branch = 'No Details for curr'
        AccountNbr = 'No Details for curr'
        BranchCode = 'No Details for curr'
        Swift = 'No Details for curr'


    

    ####### FAX & Email #######

 
    
    CP = p.ptyid.replace(',', '')
    
    
    if p.address == '':
    	Address1 = 'PLEASE ADVISE'
    else:
    	Address1 = p.address
	
    Address2 = p.address2
    ZipCode = p.zipcode
    City = p.city
    Country = p.country
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
    	Calendar1 = l.pay_calnbr.description
    except:
#    	print 'No pay calendar'
	Calendar1 = ''
	    
    try:
    	Calendar2 = 'and' + ' ' + l.pay2_calnbr.description
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
    
        FixedRate = real_round(l.fixed_rate, 4)
        fixpyday = ''
        DayCountFixed = ''
        

	if l.type == 'Float':

	    flpyday = ''
	
	    #flpyday = ''
            Index = l.float_rate.insid
            #print Index
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
		    flpyday = str(c.pay_day)
	     	    flag = 1
		else:
		    flpyday = flpyday + '; ' + str(c.pay_day)

	    	    



    #print TradeNo, FullName, Fax, CP, ISDA, Law, LawCurr,
    #print Curr, Nominal, TradeDate, EffectiveDate, EndDate
    #print FixedPayer, FixedRate, DayCount, dc, FloatPayer 
    #print Spread, Index, DesMaturity, Calendar1, Calendar2
    #print Address1, Address2, ZipCode, City, Country, Date
    #print fixpyday, flpyday, DayCountFloat, DayCountFixed, template
    #print BreakForm, BreakType, BreakStart, BreakEnd, BreakDay, ExBusDays, BreakPlace
    #print Attention, ComType


    outfile.write('%s,%s,%s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'  
    
    %(TradeNo, FullName, Fax, CP, ISDA, Law, LawCurr,
    Curr, Nominal, TradeDate, EffectiveDate, EndDate,
    FixedPayer, FixedRate, DayCount, dc, FloatPayer,
    Spread, Index,  DesMaturity, Calendar1, Calendar2,
    Address1, Address2, ZipCode, City, Country, Date,
    fixpyday, flpyday, DayCountFloat, DayCountFixed, template,
    BreakForm, BreakType, BreakStart, BreakEnd, BreakDay, ExBusDays, BreakPlace,
    Attention, ComType, AName, AAccount, Branch, AccountNbr, BranchCode, Swift))
    
    outfile.close()
		    
    return 'Success'			    


# ## main 
#689391
#t= ael.Trade[2816981]
#print OpenFile('1')
#print conTest(1,t)
