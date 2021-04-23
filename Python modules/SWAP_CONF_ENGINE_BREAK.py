'''
Purpose                       :  Confirmation templated updated and valtime added to script
Department and Desk           :  OPS
Requester                     :  Letitia Roux
Developer                     :  Anwar Banoo
CR Number                     :  227607
JIRA Issue		      :  ABOPSIT-104

Purpose                       :  Valution time change for johannesburg from 9am to 11am
Department and Desk           :  OPS
Requester                     :  Letitia Roux
Developer                     :  Anwar Banoo
CR Number                     :  238067
JIRA Issue		      :  ABOPSIT-115
'''

import ael, string, math, CalcSpreads
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

    #try:

    s = 'TradeNo,FullName,Fax,CP,ISDA,Law,LawCurr,Curr,Nominal,TradeDate,EffectiveDate,' \
    + 'EndDate,FixedPayer,FixedRate,DayCount,dc,FloatPayer,Spread,Index,' \
    + 'DesMaturity,Calendar,Calendar2,Address1,Address2,ZipCode,City,Country,' \
    + 'Date,FixPayDay,FloatPayDay,DayCountFloat,DayCountFixed,Template,' \
    + 'BreakForm,BreakType,BreakStart,BreakEnd,BreakDay,ExBusDays,BreakPlace,ValTime,' \
    + 'Attention,ComType,AName,AAccount,Branch,AccountNbr,BranchCode,Swift,ExerciseType,CPBranchCode,CPAcountNumber\n'

    outfile1=  open('F:\Confirmations\SWAP\Break_Clause\SwapExport.txt', 'w')
    outfile2= open('F:\Confirmations\SWAP\Break_None\SwapExport.txt', 'w')
    
    outfile1.write(s)    	
    outfile2.write(s)    	
    
#    	'strfix', 'RollPeriod', 'DayCount', 
#    	'Calendar', 'Start', 'End', 'Nominal', 'FloatRef', 'Spread'))	  
            
    outfile1.close()
    outfile2.close()

    return 'Success'
    '''
    except: 
    	raise 'cant open'
    	print 'cant open'
	return 'Error opening file'
    '''




def conTest(temp, t,*rest):

    ael.poll()

    ####### ISDA & template #######
    Law = ''
    LawCurr = ''
    ISDA = ''
    template = 'LONG FORM'
    nbr =  t.counterparty_ptynbr.ptynbr
    a = ael.Agreement.select("counterparty_ptynbr = %i" %nbr)
    for i in a:
    	if i.document_type_chlnbr == None or i.dated == None: 
	
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
    Nominal = real_round(abs(t.nominal_amount(t.value_day)), 0)
    
#    print 'XXXXXXXXXXXXXXXXXXXXXXXX', Nominal
#    print
    
    TradeDate = ael.date_from_time(t.time)
    
    p = t.counterparty_ptynbr
    
    FullName = p.fullname.replace(',', '')
    
    if t.nominal_amount() < 0:
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
	
    Address2  = p.address2
    ZipCode   = p.zipcode
    City      = p.city
    Fax       = p.fax
    Country   = p.country
    Attention = p.attention
    ComType   = ''
    
    flag  = 0
    act   = p.accounts()
    
    CPBranchCode = ' '
    CPAccountNumber = ' '
    for acc in act:
        CPBranchCode = str(acc.account[0:6])
        CPAccountNumber = str(acc.account[7:11]) + ' '+ str(acc.account[11:14]) + ' ' + str(acc.account[14:20])
        
        
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
    EndDate  = l.end_day
    DayCount = l.daycount_method
    #if Curr  == 'ZAR':
    #	dc   = '(Fixed)'
    #else:
    #	dc = ''
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
    term = ael.date_from_time(t.time).add_months(1).years_between(t.insaddr.exp_day)
    
    #European
    if term > 3.0 and term < 4.0:
	BreakType    = 'European'
	BreakForm    = 'Yes'
	ExerciseType = 'Partial Exercise'	
	
	if t.insaddr.curr.insid == 'ZAR':
    	    BreakPlace = 'Johannesburg'
	    ExBusDays  = 'London and Johannesburg'
	    ValTime    = '11:00 a.m. Johannesburg time'
	    
        elif t.insaddr.curr.insid == 'USD':
        
            if t.insaddr.legs()[0].float_rate.insid.find('LIBOR') != -1:            
                BreakPlace = 'London'
                ExBusDays  = 'New York and London'
                ValTime    = '9:00 a.m. New York time'
            else:
                BreakPlace = 'New York'
                ExBusDays  = 'New York'  
                ValTime    = '9:00 a.m. New York time'
    	else:
    	    BreakPlace = 'Johannesburg'
	    ExBusDays  = 'London and Johannesburg'
	    ValTime    = '11:00 a.m. Johannesburg time'	
	
    #Bermudan
    elif term >= 4.0:
	BreakType    = 'Bermuda'
	BreakForm    = 'Yes'
	ExerciseType = 'Multiple Exercise'
	
	if t.insaddr.curr.insid == 'ZAR':
    	    BreakPlace = 'Johannesburg'
	    ExBusDays  = 'London and Johannesburg'
	    ValTime    = '11:00 a.m. Johannesburg time'
	    
        elif t.insaddr.curr.insid == 'USD':
        
            if t.insaddr.legs()[0].float_rate.insid.find('LIBOR') != -1:            
                BreakPlace = 'London'
                ExBusDays  = 'New York and London'
                ValTime    = '9:00 a.m. New York time'
            else:
                BreakPlace = 'New York'
                ExBusDays  = 'New York'  
                ValTime    = '9:00 a.m. New York time'
    	else:
    	    BreakPlace = 'Johannesburg'
	    ExBusDays  = 'London and Johannesburg'
	    ValTime    = '11:00 a.m. Johannesburg time'
    #No Break
    else: 
    	BreakType    = 'None'
	BreakForm    = 'No'
	BreakPlace   = 'None'
	ExBusDays    = 'None'
        ExerciseType = 'None'
        ValTime      = ''
    BreakDay = str(ael.date_from_time(t.time).to_string("%d-%B"))                                  

    #start + 3yr
    BreakStart = str((ael.date_from_time(t.time).add_years(3)).to_string("%d-%B-%Y"))              
             
    year = str((t.insaddr.exp_day.add_years(-1)).to_string("-%Y"))                        
    BreakEnd = BreakDay + year



	
    ####### Leg Details #######	
    
    
    legs = t.insaddr.legs()
    
    for l in legs:

	if l.type == 'Float':

	    flpyday = ''
	
	    if l.float_rate.insid.find('JIBAR') != -1:
	    	Index = 'ZAR-JIBAR-SAFEX'
	    elif l.float_rate.insid.find('USD-LIBOR') != -1:
	    	Index = 'USD-LIBOR-BBA'
	    elif l.float_rate.insid.find('ILS-TELBOR') != -1:
	    	Index = 'ILS-TELBOR01-Reuters'
	    else: Index = l.float_rate.insid
	    

	    dict = {'m':'Months','y':'Years','d':'Days'}
    	    field = l.rolling_period
    	    amount = field.rstrip(field[len(field)-1])
    	    c = field[len(field)-1]
    	    DesMaturity =  (str)(amount) + ' ' + dict[c]
	    
	    DayCountFloat = l.daycount_method
            if DayCountFloat == 'Act/365':
                DayCountFloat = DayCountFloat + '(Fixed)'	    
	      
	    if l.spread == 0:
	    	Spread = 'None'
	    else:
	    	Spread = l.spread
	   
            
    	    cshflws = l.cash_flows()
    	    # this allows the dates to be printed from biggest to smallest
    	    list = []
    	    for c in cshflws:
                tup = (c.cfwnbr, c.pay_day)
                list.append(tup)
            flpyday = list.sort()#added now
            flpyday = list.reverse()#added now
            #print dir(list)
            
            
            count = 0
            flpyday = ''
            while count < len(list):
                if count == 0:
                    flpyday = str(list[count][1])
                else:
                    flpyday = flpyday + '; ' + str(list[count][1])
                count = count + 1
            
            #print flpyday
            
            
            # Remove Above
    	    #flag = 0
    	    #for c in cshflws:
	    	#if flag == 0:
		    #flpyday = flpyday + str(c.pay_day)
	     	    #flag = 1
		#else:
		    #flpyday = flpyday + '; ' + str(c.pay_day)

	    	    
	if l.type == 'Fixed':
	
    	    fixpyday = ''
	    FixedRate = l.fixed_rate
	    DayCountFixed = l.daycount_method
            if DayCountFixed == 'Act/365':
                DayCountFixed = DayCountFixed + '(Fixed)'	    
	      		    	
    	    cshflws = l.cash_flows()
        
    	    alist = []
    	    for c in cshflws:
                tup = (c.cfwnbr, c.pay_day)
                alist.append(tup)
            fixpyday = alist.sort()
            fixpyday = alist.reverse()
            #print alist
            
            count = 0
            fixpyday = ''
            while count < len(alist):
                if count == 0:
                    fixpyday = str(alist[count][1])
                else:
                    fixpyday = fixpyday + '; ' + str(alist[count][1])
                count = count + 1
            
            #print fixpyday
            # Remove Above
	    	    
    	    #flag = 0
    	    #for c in cshflws:
	    	#if flag == 0:
	    	    #fixpyday = fixpyday + str(c.pay_day)
	    	    #flag = 1
    	    	#else:
	    	    #fixpyday = fixpyday + '; ' + str(c.pay_day)



    if BreakForm == 'Yes':
        filename = 'F:\Confirmations\SWAP\Break_Clause\SwapExport.txt'
    else:
        filename = 'F:\Confirmations\SWAP\Break_None\SwapExport.txt'
        

    try: 
    	outfile=open(filename, 'a')
    except: 
    	print 'cant open'
        raise Exception('cant open')


    #print TradeNo, FullName, Fax, CP, ISDA, Law, LawCurr,
    #print Curr, Nominal, TradeDate, EffectiveDate, EndDate
    #print FixedPayer, FixedRate, DayCount, dc, FloatPayer 
    #print Spread, Index, DesMaturity, Calendar1, Calendar2
    #print Address1, Address2, ZipCode, City, Country, Date
    #print fixpyday, flpyday, DayCountFloat, DayCountFixed, template
    #print BreakForm, BreakType, BreakStart, BreakEnd, BreakDay, ExBusDays, BreakPlace
    #print Attention, ComType


    outfile.write('%s,%s,%s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'  
    
    %(TradeNo, FullName, Fax, CP, ISDA, Law, LawCurr,
    Curr, Nominal, TradeDate, EffectiveDate, EndDate,
    FixedPayer, FixedRate, DayCount, dc, FloatPayer,
    Spread, Index,  DesMaturity, Calendar1, Calendar2,
    Address1, Address2, ZipCode, City, Country, Date,
    fixpyday, flpyday, DayCountFloat, DayCountFixed, template,
    BreakForm, BreakType, BreakStart, BreakEnd, BreakDay, ExBusDays, BreakPlace, ValTime,
    Attention, ComType,  AName, AAccount, Branch, AccountNbr, BranchCode, Swift, ExerciseType, CPBranchCode, CPAccountNumber))
    
    outfile.close()
		    
    return 'Success'			    


#bermuda
#t= ael.Trade[1365717]
#OpenFile('1')
#print conTest(1, t)

#euro
#t= ael.Trade[6462577]
#OpenFile('1')
#print conTest(1, t)

