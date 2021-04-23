import ael, string, math, acm, re
import InstrType
from zak_funcs import formnum
from SWAP_CONF_ENGINE_BREAK import real_round

"""-----------------------------------------------------------------------------------------

Name        : Call_Deposit_Loan_Confo
Developer   : Tshepo Mabena
Date        : 29-05-2008
Description : This AEL works with an ASQL query( SAMM_Primary_CONFO). The query opens 
              an AEL(SAMM_Primary_CONFO), then an AEL writes to the text document of which
              the contents are merged to the word document for the confirmatin of the Fixed 
              deposit loan.
----------------------------------------------------------------------------------------------"""


def OpenFile(temp,*rest):
    
    try: 
    	outfile=open('F:\Confirmations\SAMM_Primary_Confo\SAMM_Primary_Confo_Export.txt', 'w')
	
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%('TradeNo', 'Business_Day', 'Counterparty', 'Address',
                       'Address2', 'City', 'ZipCode', 'Attention', 'MM_Instype', 'Type', 'Nominal', 'Start_Day', 'End_Day', 'Rate',
                       'Intr', 'Acc_Num', 'Rollcount', 'Rollunit', 'Currency'))
        outfile.close()

	return 'Success'

    except: 
    	raise  'cant open'
    	print  'cant open'
	return 'Error opening file'


def conTest(temp,t,D,*rest):
        
    ael.poll()
    try: 
    	outfile=open('F:\Confirmations\SAMM_Primary_Confo\SAMM_Primary_Confo_Export.txt', 'a')
    except: 
    	raise 'cant open'
    	print 'cant open'
    
    Date = ael.date(D).to_string("%Y/%m/%d")
    m = re.match(r"(\d+)\/(\d+)\/(\d*)", Date)
    d1 = "%04d/%02d/%02d" % (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    
    # ############ Nominal Amount ######################
    ais = t.additional_infos()
    Nominal = 0.0
    for ai in ais:
        if ai.addinf_specnbr.field_name == 'BoConfirm timestamp':
            date = ai.value
            s = re.match(r"(\d+)\-(\d+)\-(\d*)", date)
            d2 = "%04d/%02d/%02d" % (int(s.group(1)), int(s.group(2)), int(s.group(3)))
    
        
    if Date == (ael.date_from_time(t.creat_time)).to_string("%Y/%m/%d") or d1 == d2:
        if  t.insaddr.instype in ['FRN', 'Deposit', 'CD']:
            Nominal = str(formnum(abs(t.nominal_amount(t.value_day))).replace(',', ' '))   
            
    Start_Day = t.value_day.to_string("%d %B %Y")
    End_Day = t.insaddr.exp_day.to_string("%d %B %Y")
    Rate = str(real_round(t.price, 4))
    
    Intr = (formnum(abs(t.interest_settled(t.value_day, t.insaddr.exp_day)))).replace(',', ' ')    
    
    TradeNo      = t.trdnbr 
    
    
    ################ Counterparty Address Details ###
    
    Business_Day = ael.date_today().to_string("%d  %B  %Y")
    Counterparty = t.counterparty_ptynbr.fullname + ' '+ t.counterparty_ptynbr.fullname2 
    Address      = t.counterparty_ptynbr.address
    Address2     = t.counterparty_ptynbr.address2
    City         = t.counterparty_ptynbr.city
    ZipCode      = t.counterparty_ptynbr.zipcode
    Attention    = t.counterparty_ptynbr.attention 
    
    
    ############### MM_Instype ###################
    MM_Instype = ' '       
    if t.add_info('Funding Instype') != ' ':
        MM_Instype = t.add_info('Funding Instype')
    elif t.add_info('MM_Instype') != ' ':
        MM_Instype = t.add_info('MM_Instype')
    else:
        MM_Instype = t.add_info('Instype')
        
               
    ############### Type ###################
    
    if t.nominal_amount(t.value_day) < 0:
        Type = 'your Deposit' 
    else:
        Type = 'our Loan to you'
        
    Acc_Num = ' '    
    p = t.counterparty_ptynbr
    act = p.accounts()
    for a in act:
        Acc_Num = a.account 
        
    Currency = t.display_id('curr')
    
    ############### Rolling_Period #############
    #Count:
    for l in t.insaddr.legs():
        if getattr(l, 'rolling_period.count') == 0:
            Rollcount = 'None'
        else:
            Rollcount = getattr(l, 'rolling_period.count')
    #Unit:        
        if getattr(l, 'rolling_period.count') == 0:
            Rollunit = ' '
        elif getattr(l, 'rolling_period.count') == 1 and getattr(l, 'rolling_period.unit') == 'Month':
            Rollunit = 'Month'
        else:
          Rollunit = getattr(l, 'rolling_period.unit')
    
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(TradeNo, Business_Day, Counterparty,
                                                                       Address, Address2, City, ZipCode, Attention, MM_Instype,
                                                                       Type, Nominal, Start_Day, End_Day, Rate, Intr, Acc_Num,
                                                                       Rollcount, Rollunit, Currency))
                
    outfile.close()
            
    return 'Success'			    
 
        
def ASQL(*rest):
    acm.RunModuleWithParameters( 'SAMM_Primary_CONFO', 'Standard' )
    return 'SUCCESS'

    
ael_variables = [('trdnbr', 'Trade Number:', 'string', None, 'All'),
                ('date', 'Date:', 'string', ael.date_today(), ael.date_today(), 1 )]
                

def ael_main(dict):
    
    if dict['trdnbr'] != 'All':
        OpenFile(1)
        try:
            for trd in dict['trdnbr'].replace(' ', '').split(','):
                trade = ael.Trade[int(trd)]
                try:
                   date = ael.date(dict['date'])
                   conTest(1, trade, date)
                except:
                   print 'Invalid DATE'
        except:
           print 'Invalid Trade'
            
    if dict['trdnbr'] == 'All':
        OpenFile(1)
        try:
            tf = ael.TradeFilter['Fixed_All_Trades']
            date = ael.date(dict['date'])
            for trd in tf.trades():
                if date == ael.date_from_time(trd.creat_time):
                    trade = ael.Trade[trd.trdnbr]
                    conTest(1, trade, date)
        except:
            print 'Invalid Date'
