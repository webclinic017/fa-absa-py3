import ael, string 

try: infile = open('c:\\STTDump.csv', 'r')
except:
    print 'Outfile c:\STTDump.txt not found'
    ael.log('The file does not exist in the specified directory')

Default = ael.Instrument['BillDefault']
Trader = ael.User['ABCJ000'].usrnbr
Acquirer = ael.Party['Money Market Desk']
print Acquirer
line = infile.readline()
while line:
    insid, prfid, add_info, nom, contr_size, quantity, exp_day, price, val_date, opt_key, cp, prem = string.split(line, ',')
    print prfid, add_info, nom, contr_size, quantity, exp_day, price, val_date, opt_key, prem, cp, insid
    # Select portfolio number
    prfnbr = ael.Portfolio[prfid].prfnbr
    # Select Counterparty number
    cp_ptynbr = ael.Party[cp].ptynbr
    # Select Trader number
    trd_ptynbr = ael.User[Trader]
    # Select Acquirer number
    acq_ptynbr = ael.Party[Acquirer.ptyid].ptynbr
    
    print acq_ptynbr
    
    # Create new instrument if necessary
    if ael.Instrument[insid]:
    	new = ael.Instrument[insid]
	print 'Instrument in existance', insid
	#print new.pp()
    else:
    	print 'Instrument needed to be created', insid
	new = ael.Instrument.new('Bill') #Default.clone()
	print insid, contr_size, 'panos'
    	new.insid = insid
	new.contr_size = float(contr_size)
	print new.exp_day, 'Before', exp_day
	new.exp_day = ael.date_from_string(exp_day)
	new.legs()[0].end_day=ael.date_from_string(exp_day)
	new.legs()[0].start_day=ael.date_from_string(val_date)
	print new.pp()
      	new.commit()
	print new.exp_day, 'After'
	print new.exp_day
    
    if ael.Trade.read('optional_key=%s' % opt_key):
    	print 'Trade SKIPPED'
    else:
    	newtrd = ael.Trade.new(new)
    	newtrd.prfnbr = prfnbr
    	newtrd.quantity = float(quantity)
    	newtrd.price = float(price)
    
    
    	#newtrd.premium = ael.Instrument.read('insid = %s' %insid).premium_from_quote()*int(nom)
    	newtrd.value_day = ael.date_from_string(val_date)
    	newtrd.time = ael.date_from_string(val_date).to_time()
    	newtrd.acquire_day = ael.date_from_string(val_date)
    	newtrd.optional_key = str(opt_key)
    	newtrd.counterparty_ptynbr = int(cp_ptynbr)
    	newtrd.acquirer_ptynbr = acq_ptynbr
    	newtrd.curr = ael.Instrument['ZAR']
    	newtrd.status = 'FO Confirmed'
    	newtrd.type = 'Normal'
	print newtrd.prfnbr.prfid
    	newtrd.commit()
    	print 'INSTRUMENT'
    	#print new.pp()
    	print 'TRADE'
    	#print newtrd.pp()
    
    	#Find Additional Information Field, Link to trade and Populate Value
    
    	#AddInfoSpec = ael.AdditionalInfoSpec['MM_Instype'].specnbr
    	#AddInfo = ael.AdditionalInfo.new(newtrd)
    	#AddInfo.value = add_info
    	#AddInfo.commit()
    	#print AddInfo.pp()
    
    	#print AddInfoSpec.pp()
    
    line = infile.readline()


infile.close()

