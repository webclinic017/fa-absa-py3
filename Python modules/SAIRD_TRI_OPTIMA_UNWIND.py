"""-----------------------------------------------------------------------
MODULE
    SAIRD_TRI_OPTIMA_UNWIND

DESCRIPTION
    Date                : 2012-01-26
    Purpose             : To fully/partially unwind a group of trades instructed by the Tri-Optima proposal
    Department and Desk : Middle Office
    Requester           : Willem Kellerman
    Developer           : Hendrik Jansen van Rensburg
    CR Number           : 882986
    
HISTORY
================================================================================
Date       Change no    Developer                       Description
--------------------------------------------------------------------------------
2012-01-26 882986       Hendrik Jansen Van Rensburg     Initial Implementation
ENDDESCRIPTION
-----------------------------------------------------------------------"""
import ael, time

def remove_payment(trd):
    for z in trd.payments():
        if z.type == 'Broker Fee':
            try:
                z.delete()
            except Exception, e:
                print 'Could not delete Broker Fee for trade ', trd.trdnbr, '\t', e
        else:
            if z.payday <= ael.date_today():
                try:
                    z.delete()                        
                except Exception, e:
                    print 'Could not delete payment for trade ', trd.trdnbr, '\t', e

def unwind_Trades(file):
    #Check if file exist
    try:
    	f = open(file)
    	chk = 1
    except:
    	print 'File could not be found or opened'
	chk = 0
    
    if chk == 1:
        line = f.readline()
        line = f.readline()        
        count = 0
        print 'Original Trade', '\t', 'EAO Trade', '\t', 'New Trade', '\t', 'Original PV', '\t', 'EAO PV', '\t', 'New PV'
        while line:            
            l = []
            line = line.rstrip()
            l = line.split(',')
            
            #Check if trade is valid
            try:
                trd = ael.Trade[(int)(l[5])]
                chk = 1
            except Exception, e:
                print l[5], '\t', 'Not a valid trade', '\t', e
                chk = 0
                
            if chk == 1: 
                #Create eao (equal and opposite)                
                trdc_eao = trd.new()
                trdc_eao.quantity = trdc_eao.nominal_amount() / -1000000
                trdc_eao.status = 'BO Confirmed'
                trdc_eao.optional_key = ''
                trdc_eao.value_day = ael.date_today()
                trdc_eao.acquire_day = ael.date_today() 
                remove_payment(trdc_eao)
                try:
                    trdc_eao.commit()
                except Exception, e:
                    print 'Unable to commit eao trade for', l[5], '\t', e   
                ael.poll()    
                trdc_eao = trdc_eao.clone()
                trdc_eao.status = 'Terminated'
                try:
                    trdc_eao.commit() 
                except Exception, e:
                    print 'Unable to change status to Terminated on eao for trade', l[5], '\t', e
                
                #Create partial trade (if any)
                new_nom = int(l[13])
                if new_nom <> 0:                    
                    trdc_new = trd.new()
                    ins = trd.insaddr
                    l = ins.legs()[0]
                    cash_qaunt_now = trd.quantity
                    for c in l.cash_flows():
                        if ael.date_today() >= c.start_day and ael.date_today() < c.end_day:                        
                            cash_qaunt_now = c.nominal_factor * trd.quantity * ins.contr_size * l.nominal_factor / 1000000
                    if cash_qaunt_now < 0:           
                        cash_qaunt_now = -1 * cash_qaunt_now             
                    trdc_new.quantity = new_nom / 1000000 * (trd.quantity / cash_qaunt_now)                                    
                    trdc_new.status = 'BO Confirmed'
                    trdc_new.optional_key = ''
                    trdc_new.value_day = ael.date_today()
                    trdc_new.acquire_day = ael.date_today() 
                    remove_payment(trdc_new)
                    try:
                        trdc_new.commit()
                    except Exception, e:
                        print 'Unable to create new trade during partial unwind for', l[5], '\t', e                    
                
                #Terminate original deal
                trdc = trd.clone()
                trdc.status = 'Terminated'
                try:
                    trdc.commit()
                except Exception, e:
                    print 'Unable to change status to Terminated for original trade', l[5], '\t', e    
                
                if new_nom <> 0:
                    print trd.trdnbr, '\t', trdc_eao.trdnbr, '\t', trdc_new.trdnbr, '\t', trd.present_value(), '\t', trdc_eao.present_value(), '\t', trdc_new.present_value()
                else:
                    print trd.trdnbr, '\t', trdc_eao.trdnbr, '\t', 'None', '\t', trd.present_value(), '\t', trdc_eao.present_value(), '\t', 0

            line = f.readline()
        f.close()

FILE_NAME = 'F:/ABSA_Unwind.csv'
ael_variables = [['filename', 'File name', 'string', None, FILE_NAME, 1, 0, 'File directory and name', None, 1]]
                
def ael_main(dictionary):
    print '....Starting Unwinds....', time.ctime() 
    unwind_Trades(dictionary['filename'])
    print '....Unwinds Complete....', time.ctime()

