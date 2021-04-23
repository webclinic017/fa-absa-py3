"""-----------------------------------------------------------------------------------------

Name        : Call_Deposit_Loan_Confo
Developer   : Tshepo Mabena
Date        : 22-05-2008
Description : This AEL works with an ASQL query( SAMM_Call_Deposit_Loan_Confo). The query opens 
              an AEL(SAMM_Call_Deposit_Loan_Confo), then an AEL writes to the text document of which
              the contents are merged to the word document for the confirmatin of the call 
              deposit loan.
----------------------------------------------------------------------------------------------"""


import ael, string, math, acm
import InstrType
from SAMM_Statements import formnum

def OpenFile(temp, *rest):
    
    try: 
    	outfile=open('c:\\ConfirmationE\Call_Depo_Loan\Call_Depo_Loan_Confo_Export.txt', 'w')
	
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%('TradeNo', 'Counterparty', 'Address', 'City',
                      'Contact_Person', 'Telephone', 'Fax', 'Date', 'Account_Number', 'Account_Type', 'Transaction_Amount',
                      'Transaction_type', 'Transaction_Nbr', 'Transaction_Value_date', 'Interest_Rate'))
        outfile.close()

	return 'Success'

    except: 
    	raise  'cant open'
    	print  'cant open'
	return 'Error opening file'

def conTest(temp,t,cfnbr,D,*rest):

    ael.poll()
    Date = ael.date(D)
      
    try: 
    	outfile=open('c:\\ConfirmationE\Call_Depo_Loan\Call_Depo_Loan_Confo_Export.txt', 'a')
    except: 
    	raise 'cant open'
    	print 'cant open'
    
    Counterparty = t.counterparty_ptynbr.ptyid
    
    if t.counterparty_ptynbr.address == '':
        Address = 'PLEASE ADVISE'
    else:
        Address = t.counterparty_ptynbr.address 
    
    TradeNo        = t.trdnbr
           
    City           = t.counterparty_ptynbr.city    
    Contact_Person = t.counterparty_ptynbr.contact1
    Telephone      = t.counterparty_ptynbr.telephone
    Fax            = t.counterparty_ptynbr.fax
   
    Account_Number = t.insaddr.insid
    
    Account_Type   = t.add_info('Funding Instype')         
    
    ins = ael.Instrument[t.insaddr.insid]
    Interest_Rate = -1

    ############### Interest Rate ###############
    dict_reset = {}   
    for c in t.insaddr.legs()[0].cash_flows():
        if c.type == 'Call Fixed Rate Adjustable':
            for r in c.resets():
                d1 = r.start_day
                while d1 < r.end_day:
                    
                    if str(d1) in dict_reset.keys():
                        dict_reset[str(d1)] = dict_reset[str(d1)] + r.value
                    else:   
                        dict_reset[str(d1)] =  r.value
                    d1 = d1.add_days(1)
    if dict_reset.has_key(str(Date)):
        Interest_Rate = dict_reset[str(Date)]
    else:
        print 'no key'
     
                    
    
    ######## Transaction Amount #################
    
    cf_list=[]
    Transaction_Amount = 0
    Transaction_Nbr = 0
    Transaction_type = ' ' 
   
    for cf in t.insaddr.legs()[0].cash_flows():
        if cf.start_day and cf.start_day == Date:
            if (t.quantity*cf.fixed_amount) > 0 and cf.type == 'Fixed Amount':
                    
                temp =[]
                Transaction_type = 'TRG TRANSFER IN'
                Transaction_Amount =  str((formnum(t.quantity*cf.fixed_amount)).replace(',', ' '))
                Transaction_Nbr = cf.cfwnbr
                temp.append(Transaction_Amount)
                temp.append(Transaction_Nbr)
                temp.append(Transaction_type)
                cf_list.append(temp)
                
            
            elif (t.quantity*cf.fixed_amount) < 0 and cf.type == 'Fixed Amount':
                      
                temp =[]
                Transaction_type = 'TRG TRANSFER OUT'
                Transaction_Amount = str((formnum((t.quantity*cf.fixed_amount)*-1).replace(',', ' ')))
                Transaction_Nbr = cf.cfwnbr
                temp.append(Transaction_Amount)
                temp.append(Transaction_Nbr)
                temp.append(Transaction_type)
                cf_list.append(temp)
                
            else:
                Transaction_type = 'NO TRANSFER'
        else:
            if cf.pay_day == Date:
                if (t.quantity*cf.fixed_amount) > 0 and cf.type == 'Fixed Amount':
                
                    temp =[]
                    Transaction_type = 'TRG TRANSFER IN'
                    Transaction_Amount =  str((formnum(t.quantity*cf.fixed_amount)).replace(',', ' '))
                    Transaction_Nbr = cf.cfwnbr
                    temp.append(Transaction_Amount)
                    temp.append(Transaction_Nbr)
                    temp.append(Transaction_type)
                    cf_list.append(temp)
                    
                
                elif (t.quantity*cf.fixed_amount) < 0 and cf.type == 'Fixed Amount':
                          
                    temp =[]
                    Transaction_type = 'TRG TRANSFER OUT'
                    Transaction_Amount = str((formnum((t.quantity*cf.fixed_amount)*-1)).replace(',', ' '))
                    Transaction_Nbr = cf.cfwnbr
                    temp.append(Transaction_Amount)
                    temp.append(Transaction_Nbr)
                    temp.append(Transaction_type)
                    cf_list.append(temp)
                    
                else:
                    Transaction_type = 'NO TRANSFER'
            
    ######## Transaction Value Date #############
    
    Transaction_Value_date = ' '
    for cf in t.insaddr.legs()[0].cash_flows():
        if cf.type == 'Fixed Amount':   
            if cf.pay_day == Date:
                if cf.start_day == None:
                    Transaction_Value_date = cf.pay_day
                    
                else:
                    Transaction_Value_date = cf.start_day
    
   
    for x in cf_list:
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(TradeNo, Counterparty, Address, City, Contact_Person, Telephone, Fax,
                Date, Account_Number, Account_Type, x[0], x[2], x[1], Transaction_Value_date, Interest_Rate))
                
    outfile.close()
            
    return 'Success'			    


def concf(cf,*rest):

    ael.poll()
   
    t = cf.legnbr.insaddr.trades()[0]
    
    try: 
    	outfile=open('c:\\ConfirmationE\Call_Depo_Loan\Call_Depo_Loan_Confo_Export.txt', 'a')
    except: 
    	raise 'cant open'
    	print 'cant open'
    
    Counterparty = t.counterparty_ptynbr.ptyid
    
    if t.counterparty_ptynbr.address == '':
        Address = 'PLEASE ADVISE'
    else:
        Address = t.counterparty_ptynbr.address 
    
    TradeNo        = t.trdnbr
    
    Transaction_Value_date = ' '
    if cf.start_day == None:
        Transaction_Value_date = cf.pay_day
        
    else:
        Transaction_Value_date = cf.start_day
    
        
    City           = t.counterparty_ptynbr.city    
    Contact_Person = t.counterparty_ptynbr.contact1
    Telephone      = t.counterparty_ptynbr.telephone
    Fax            = t.counterparty_ptynbr.fax
   
    Account_Number = t.insaddr.insid
    
    Account_Type   = t.add_info('Funding Instype')         
    
    ins = ael.Instrument[t.insaddr.insid]
    Interest_Rate = -1

    ############### Interest Rate ###############
    dict_reset = {}   
    for c in t.insaddr.legs()[0].cash_flows():
        if c.type == 'Call Fixed Rate Adjustable':
            for r in c.resets():
                d1 = r.start_day
                while d1 < r.end_day:
                    
                    if str(d1) in dict_reset.keys():
                        dict_reset[str(d1)] = dict_reset[str(d1)] + r.value
                    else:   
                        dict_reset[str(d1)] =  r.value
                    d1 = d1.add_days(1)
    if dict_reset.has_key(str(Transaction_Value_date)):
        Interest_Rate = dict_reset[str(Transaction_Value_date)]
    else:
        print 'no key'
     
                    
    
    ######## Transaction Amount #################
    
    Transaction_Amount = 0
    Transaction_Nbr = 0
    Transaction_type = ' ' 
    
    if (t.quantity*cf.fixed_amount) > 0 and  cf.type == 'Fixed Amount':
        Transaction_type = 'TRG TRANSFER IN'
        Transaction_Amount =  str((formnum(t.quantity*cf.fixed_amount)).replace(',', ' '))
        Transaction_Nbr = cf.cfwnbr
    
    elif (t.quantity*cf.fixed_amount) < 0 and cf.type == 'Fixed Amount':
        Transaction_type = 'TRG TRANSFER OUT'
        Transaction_Amount = str(formnum((t.quantity*cf.fixed_amount)*-1 ).replace(',', ' '))
        Transaction_Nbr = cf.cfwnbr
    else :
            
        Transaction_type = 'NO TRANSFER'
            
    
    
   
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(TradeNo, Counterparty, Address, City, Contact_Person, Telephone, Fax,
                                                                   Transaction_Value_date, Account_Number, Account_Type, Transaction_Amount,
                                                                   Transaction_type, Transaction_Nbr, Transaction_Value_date, Interest_Rate))
                
    outfile.close()
            
    return 'Success'
    
def check_trade(t, date):
    
    cf =  t.insaddr.legs()[0].cash_flows()
    for c in cf:
        if c.type == 'Fixed Amount':
            if c.start_day and c.start_day == date:
                concf(c)
            else:
                if c.pay_day == date:
                    concf(c)
     
        
def ASQL(*rest):
    acm.RunModuleWithParameters( 'SAMM_Call_Deposit_Loan_Confo', 'Standard' )
    return 'SUCCESS'

filters = []
for f in ael.TradeFilter:
    filters.append(f.fltid)
filters.sort()

    
ael_variables = [('tf', 'TradeFilter:', 'string', filters, 'Call_All_Trades'),
                ('trdnbr', 'Trade Number:', 'string', None, 'All'),
                ('cfwnbr', 'CashFlow Number:', 'string', None, 'All'),
                ('date', 'Date:', 'string', ael.date_today(), ael.date_today() ),
                ('backdate', 'Include Backdate:', 'string', ['Include', 'Exclude'], 'Include')]

def ael_main(dict):
    if dict['trdnbr'] != 'All':
        OpenFile(1)
        for trd in dict['trdnbr'].replace(' ', '').split(','):
            try:
                trade = ael.Trade[int(trd)]
                try:
                    date = ael.date(dict['date'])
                    conTest(1, trade, 0, date)
                except:
                    print 'Invalid Date'
            except:
                print 'Invalid Trade' 
                    
    if dict['cfwnbr'] != 'All':
        OpenFile(1)
        for cfr in dict['cfwnbr'].replace(' ', '').split(','):
            try:
                cashf = ael.CashFlow[int(cfr)]
                concf(cashf)
            except:
                print 'not valid cf'
            
    if dict['cfwnbr'] == 'All' and dict['trdnbr'] == 'All':
        try:
            date = ael.date(dict['date'])
            tf = ael.TradeFilter[dict['tf']]
            OpenFile(1)
            for trd in tf.trades():
                check_trade(trd, date)    
        except:
            print 'Invalid DATE'
        

### main 
