import ael, string


def CheckCFD(temp, insid, prfid, ddate, *rest):
    
    trds = ael.Instrument[insid + '/CFD'].trades()
    ddt = ael.date(ddate)
    for t in trds:
    	#print t.time, ael.date_today(), t.trdnbr
    	if t.time == ddt.to_time():
            if t.prfnbr == ael.Portfolio[prfid + '_CFD']:
               msg = 'CFDs have already been committed on this instrument and account for ' + ddate.to_string()
               print(msg)
               return msg

    return 'ok'   







def CreateCFD(temp, insid, prfid, qty, vwap, fee, premium,  *rest):

    i = ael.Instrument[insid + '/CFD']
    if i == None:
        print('CFD instrument does not exist')
        return 0
    t_new = ael.Trade.new(i)
	    
    t_new.price = vwap
    t_new.text1 = 'Fee Received ' + str(fee)
    t_new.fee = fee
    
    if qty > 0:
        t_new.premium = (premium)
    elif qty < 0:
        t_new.premium = (premium) * -1
    else:
        print('Net quantity on stocks is zero')

    t_new.quantity = qty * -1        
    t_new.status = 'Simulated'
    port = ael.Portfolio[prfid + '_CFD']
    t_new.prfnbr = port
    t_new.acquirer_ptynbr = ael.Party['EQ Derivatives Desk']
    
    ais = ael.Portfolio[prfid].additional_infos()
    for ai in ais:
        if ai.addinf_specnbr.field_name == 'CFD Counterparty':
            t_new.counterparty_ptynbr = ael.Party[ai.value]  
        if ai.addinf_specnbr.field_name == 'CFD Broker':
            t_new.broker_ptynbr = ael.Party[ai.value]  
        
    #t_new.counterparty_ptynbr = ael.Party['BARCLAYS CAPITAL SECURITIES LTD']
    
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%% TESTING %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
    #t_new.time = ael.date_today().to_time()
    ccy = ael.Instrument['ZAR']
    t_new.time = ael.date_today().add_banking_day(ccy, 0).to_time()
        
    #t_new.value_day = ael.date_today()
    t_new.value_day = ael.date_today().add_banking_day(ccy, 5)
    #t_new.acquire_day = ael.date_today()
    t_new.acquire_day = ael.date_today().add_banking_day(ccy, 5)

    t_new.curr = i.curr
    user = ael.userid()
    t_new.trader_usrnbr = ael.User[user]
    
    #set add_info Stock Hedges
    Shedge = StockHedge(1, insid, prfid, ael.date_today())
    ai_new = ael.AdditionalInfo.new(t_new)
    ai_new.value = Shedge
    ai_new.addinf_specnbr = ael.AdditionalInfoSpec['Stock Hedges'].specnbr
    try:
        ai_new.commit()
        #print 'ai commited'
    except:
        print('Warning : Error writing add_info Stock Hedges')


           
    try:
    	t_new.commit()
    	#print 'CFD Trade commited'
	return t_new.trdnbr
    except:
    	print('Error committing trade')
	return 0









	
   


def CreateFunding(temp, newprfid, PLIncep, ddate, ABUser, *rest):
    if CheckUser(temp, ABUser) == 'Denied':
        return 'Access Denied'
    
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% testing %%%%%%%%%%%%%%%%%%%#
    today = ael.date_from_string(ddate)
    #ael.date_today()
    #i = ael.Instrument['ZAR']
    #today = ael.date_today()
    
    port = ael.Portfolio[newprfid].trades()
    
    LNom = 0
    DNom = 0
    
    for t in port:
        # %%%%%%%%%%% for testing take out FO Confirmed %%%%%%%%%% #
        if t.insaddr.exp_day >= today and t.status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
            if string.find(t.insaddr.insid, 'Loan') != -1:
                Loan = t
                LNom = t.nominal_amount(today)
                LQty = t.quantity
                for l in t.insaddr.legs():
                    sday = l.start_day
                
	    
            elif string.find(t.insaddr.insid, 'Depo') != -1:
                Depo = t
                DNom = t.nominal_amount(today)
                DQty = t.quantity
                for l in t.insaddr.legs():
                    sday = l.start_day



    # PLIncep2 (redemption amount) after day1
    for c in Depo.insaddr.cash_flows():
        if c.type == 'Redemption Amount':
            RedD = c.projected_cf() * DQty
            
            
    for c in Loan.insaddr.cash_flows():
        if c.type == 'Redemption Amount':
            RedL = c.projected_cf() * LQty
    
    #print 'REDsss ', RedD, RedL, today, sday
   
    if RedL == 0:
        Red = RedD
    else:
        Red = RedL

    day1 = 'no'
    if today > sday:    
        PLIncep2 = Red
        if Red == -1.0 or Red == 1.0:
            Red = 0.0                
    else:
        day1 = 'yes'
        PLIncep2 = 0.0
    #print 'RED', Red, PLIncep, PLIncep2
   

    # dc is a variable used to determine whether an acc is debited or credited	
    if PLIncep2 + PLIncep  > 0:
    	dc = 'credit'
    else:
    	dc = 'debit'
    #print 'DC', dc


    # dcb is a variable used to determine whether the acc balance is in debit or credit	
    if PLIncep2 > 0:
    	dcb = 'credit'
    elif PLIncep2 < 0:
    	dcb = 'debit'
    else:
    	 dcb = 'debit'
    #print 'DCB', dcb

    #debit and credit split
    if dcb == dc:
    	split = 0
    elif dcb == 'debit': 
    	split = 1
    elif dcb == 'credit': 
    	split = 1
    else:
    	split = 0
    	
    #print 'before SPLIT', split, dc, dcb, PLIncep
    
    cf_flag1 = ''
    cf_flag2 = ''
    res_flag1 = ''
    res_flag2 = ''    
    
    if split == 1 and dcb == 'debit':
	#shift from Deposit to Loan instrument
        #add redemption cashflow to Deposit such that zero nominal on Deposit
        #add total portfolio balance to Loan
	cf_flag1 = add_cashflow(Loan, 'Fixed Amount', -(PLIncep2 + PLIncep), -1, today, '')
	cf_flag2 = add_cashflow(Depo, 'Fixed Amount', -PLIncep2, -1, today, '')
	res_flag1 = FixCurrentResets(temp, Loan, today)
	res_flag2 = FixCurrentResets(temp, Depo, today)
		
    elif split == 1 and dcb == 'credit':
    	#shift from Loan to Deposit instrument
        #add redemption cashflow to Loan such that zero nominal on Loan
        #add total portfolio balance to Deposit
	cf_flag1 = add_cashflow(Depo, 'Fixed Amount', (PLIncep2 + PLIncep), -1, today, '')
	cf_flag2 = add_cashflow(Loan, 'Fixed Amount', PLIncep2, -1, today, '')
	res_flag1 = FixCurrentResets(temp, Depo, today)
	res_flag2 = FixCurrentResets(temp, Loan, today)
                
    elif split == 0 and dcb == 'debit':   
    	#add PLIncep cashflow to Depo
	cf_flag1 = add_cashflow(Depo, 'Fixed Amount', PLIncep, -1, today, '')	
	res_flag1 = FixCurrentResets(temp, Loan, today)
	res_flag2 = FixCurrentResets(temp, Depo, today)
	
    elif split == 0 and dcb == 'credit':   
    	#add PLIncep cashflow to Loan
	cf_flag1 = add_cashflow(Loan, 'Fixed Amount', -PLIncep, -1, today, '')	
	res_flag1 = FixCurrentResets(temp, Loan, today)
	res_flag2 = FixCurrentResets(temp, Depo, today)

    else:
    	pass

    if res_flag1 == 'Error':
        #print res_flag1
        return res_flag1
    
    if res_flag2 == 'Error':
        #print res_flag2
        return res_flag2
    
    if cf_flag1 == 'Error':
        #print cf_flag1
        return cf_flag1
    
    if cf_flag2 == 'Error':
        #print cf_flag2        
        return cf_flag2
    
    return 'Success'
    
    
    






def add_cashflow(trd, type, value, factor, dat, subtype):
    legs = trd.insaddr.legs()
    l = legs[0].clone()
    
    if abs(value) > 0.000000001:
    	cf = ael.CashFlow.new(l)
    	cf.type = type 
    else:
    	return 'No Cashflow Booked'
    
    if type in ('Fixed Amount'):
    	cf.fixed_amount = value
     	cf.nominal_factor = 1
    	cf.pay_day = dat

    try:
    	cf.commit()
	#print 'Cashflow committed'
	return 'Success'
    except:
    	print('Error commiting cashflow')
    	return 'Error'
 
    




   
def FixCurrentResets(temp, trd, dat, *rest):
    #get spread
    ais = trd.additional_infos()
    for ai in ais:
        if ai.addinf_specnbr.field_name == 'CFD Spread':
            cfdSpread = ai.value

    import SAGEN_Resets
    current = SAGEN_Resets.CurrentReset(1, trd.insaddr.legs()[0].legnbr, dat, 0)
    spr = (((float)(cfdSpread) * (float)(trd.insaddr.legs()[0].spread)) + (float)(current))
    #print 'Current', current, spr, cfdSpread, trd.insaddr.legs()[0].spread
    fixed = SAGEN_Resets.FixReset(1, trd.insaddr, dat, spr, 0)
    #fixed = 1
       
    return fixed






#Checks is User has correct profile to Create Funding
def CheckUser(temp, ABUser, *rest):   
    u = ael.User[ABUser]
    pl = u.profile_links()
    ret = 'Denied'
    for p in pl:
        if p.profnbr.profid in ('BYPASS_FOUREYES'):
            ret = 'Allow'
            
    return ret
    





def StockHedge(temp, insid, prfid, ddate, *rest):
    stocks = ''
    trds = ael.Portfolio[prfid].trades()
    for t in trds:
    	if ael.date_from_time(t.time) == ddate:
            if t.insaddr == ael.Instrument[insid]:
                if stocks == '':
                    stocks = (str)(t.trdnbr)
                else:
                    if len(stocks + '/' + (str)(t.trdnbr)) < 40:
                        stocks = stocks + '/' + (str)(t.trdnbr)
                    else:
                        return stocks
    return stocks


    
### main ###
#CreateCFD(1, 'ZAR/AGL', '99999', -1000, 14406.67, 64830, -14406667)
#print CheckCFD(1, 'ZAR/AGL', '99999')
#CreateFunding(1, 2)
#import SAGEN_Resets
#trd = ael.Trade[857680]
#print StockHedge(1, 'ZAR/AGL', '99999', ael.date_today())
#r = SAGEN_Resets.FixReset(1, trd, ael.date_today(), 11.5, 0)
#res = ael.Reset[(int)(r)]
#print res.pp()
#print r
#AddCashflow(1, 12345.67, trd)
#CheckCFD(1, 'ZAR/AGL', '99999')
