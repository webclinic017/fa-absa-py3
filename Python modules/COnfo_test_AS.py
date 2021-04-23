import ael
import InstrType, RollingPeriod


def conTest(t,trd_ISDA,*rest):

    try: 
    	outfile=open('c:\\kexport.txt', 'w')
    except: 
    	raise 'cant open'
    	print('cant open')

    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' 
    %('TradeNo', 'FullName', 'Fax', 'CP', 'ISDA', 'Curr', 'Nominal', 'Date', 'TradeDate', 'EffectiveDate',
    'EndDate', 'FixedPayer', 'FixedRate', 'DayCount', 'dc', 'FloatPayer', 'Spread', 'Index',
    'DesMat', 'Calendar', 'Calendar2', 'Address1', 'Address2', 'ZipCode', 'City', 'Country'))
    
#    'strfix', 'RollPeriod', 'DayCount', 
#    'Calendar', 'Start', 'End', 'Nominal', 'FloatRef', 'Spread'))	  

    
    TradeNo = t.trdnbr
    Curr = t.insaddr.curr.insid
    Nominal = t.nominal_amount()
    Date = ael.date_today()
    TradeDate = ael.date_from_time(t.time)
    ISDA = trd_ISDA
    
    p = t.counterparty_ptynbr
    FullName = p.fullname
    
    if Nominal < 0:
    	FixedPayer = FullName
	FloatPayer = 'ABSA BANK LIMITED'
    else:
    	FixedPayer = 'ABSA BANK LIMITED'
	FloatPayer = FullName

    Fax = p.fax
    CP = p.ptyid
    if p.address == '':
    	Address1 = 'PLEASE ADVISE'
    else:
    	Address1 = p.address
	
    Address2 = p.address2
    ZipCode = p.zipcode
    City = p.city
    Country = p.country
    
    l = t.insaddr.legs()[0]
    EffectiveDate = l.start_day
    EndDate = l.end_day
    FixedRate = l.fixed_rate
    Spread = l.spread
    if l.float_rate.insid.find('JIBAR') != -1:
    	Index = 'ZAR-JIBAR-SAFEX'
    else:
    	Index = l.float_rate.insid
    DayCount = l.daycount_method
    if Curr == 'ZAR':
    	dc = '(Fixed)'
    else:
    	dc = ''
	
	
    dict = {'m':'Months','y':'Years','d':'Days'}
    field = RollingPeriod.RP(1, l)
    DesMaturity = field[0] + ' ' + dict[field[1]]

#    DesMaturity = l.start_day.days_between(l.end_day)/30
        
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
    	

    
    print(TradeNo, FullName, Fax, CP, ISDA)
    print(Curr, Nominal, Date, TradeDate, EffectiveDate, EndDate)
    print(FixedPayer, FixedRate, DayCount, dc, FloatPayer) 
    print(Spread, Index, DesMaturity, Calendar1, Calendar2)
    print(Address1, Address2, ZipCode, City, Country)


    outfile.write('%s,%s,%s,%s,%s,   %s,%f,%s,%s,%s,%s,   %s,%f,%s,%s,%s,   %f,%s,%s,%s,%s,   %s,%s,%s,%s,%s\n'  
    
    %(TradeNo, FullName, Fax, CP, ISDA,
    Curr, Nominal, Date, TradeDate, EffectiveDate, EndDate,
    FixedPayer, FixedRate, DayCount, dc, FloatPayer,
    Spread, Index,  DesMaturity, Calendar1, Calendar2,
    Address1, Address2, ZipCode, City, Country))
    
    
    outfile.close()
    
    return 'Success'
    #fixpyday



    '''
t.bo_trdnbr					'BOTrdnbr',
l.start_day 					'fixingday',
date_add_banking_day(l.start_day, display_id(i, 'curr'), reset_day_offset) 'resetday',
display_id(p, 'document_type_chlnbr')		'doc',
l.rolling_period.unit		'DesUnit',
ael_s(p,'AutoFax',t.trdnbr)  'AutoFaxNbr',

    '''



'''
    
    legs = t.insaddr.legs()
    
    for l in legs
        	
    	fixpyday = ''
	strfix = 9.9999999999
	    

    	cshflws = l.cash_flows()
	    	    
    	flag = 0
    	for c in cshflws:
    	    	if flag == 0:
    	    	    fixpyday = fixpyday + str(c.pay_day)
	 
    	    	    flag = 1
    	    	else:
	    	    fixpyday = fixpyday + '; ' + str(c.pay_day)
 
 
#    	print 'Fix', fixpyday
    	outfile.write('%s,%s,%s,%s,%s, %s, %s,%s, %s, %s, %s, %s, %s\n' 
    	%(t.trdnbr, fixpyday, l.curr.insid, ael.date_from_time(t.time),	strfix, 
	l.rolling_period, l.daycount_method, l.pay_calnbr.calid, l.start_day, l.end_day, 
	l.nominal_amount()*t.quantity, l.spread, t.premium))

#    	l.float_rate.insid, 	    	

'''
   
	    
def GenericFields(temp, t, *rest):
    nom = t.nominal_amount()
    trdtime = t.time.time_to_day()
#    start =
    PremDay = t.value_day
    Premium = t.premium
    
    	

### main 
#t= ael.Trade[677710]
#print conTest(t, '2000-11-28')
