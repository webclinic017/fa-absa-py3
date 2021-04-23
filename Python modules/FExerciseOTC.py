""" Exercise_assign:1.1.2 """

"""----------------------------------------------------------------------------
2001-02-19 10:53:38  INDIRA (FCS Demo) - AEL  (set_final_exercise_prices.py)

MODULE
        FExerciseOTC - Trades in options and warrants that have not already 
	expired are abandoned, exercised or assigned. If no quantity is 
	specified, the whole position in chosen portfolios will be exercised.

DESCRIPTION
        The final settlement prices from the exchange should be stored on 
	the MtM Market called "SETTLEMENT", from which they are selected in 
	this script.

        If physical delivery is used, the settlement trade could either be
        done to the strike price or to the market price. The closing trade
        of the option (with trade type Exercise/Assign/Abandon) should then
        get a price according to the method.

NOTE            

DATA-PREP       
        A Party of type MtM Market and with the name "SETTLEMENT" is required
	if the Mode Market is used.

ENDDESCRIPTION
----------------------------------------------------------------------------"""
import ael
import sys, getopt, os, time

###############################################################################
# Select all trades in an instrument in specified portfolio(s)
# where expiry date date >= the input date.

def get_trades_to_exercise(exer_date, instr, pf):
	exer_trades = []
	#all_trades = ael.Trade.select('status = "Exchange"')
	all_trades = ael.Trade.select('insaddr = %i' % instr.insaddr)
	for t in all_trades:
		if t.insaddr.instype in ('Option', 'Warrant') and t.type == 'Normal':
			#if (t.insaddr.exp_day == ael.date(exer_date)):
			if t.prfnbr.prfid in pf:
			    	if t.insaddr.exp_day >= ael.date(exer_date):
				    	exer_trades.append(t)
	for t in exer_trades:
	    	print '\nrow50. Trades to Close/Exercise:', t.trdnbr, t.prfnbr.prfid, t.insaddr.insid
	return exer_trades


###############################################################################
### Find the settlement price for the underlying instrument. To be used if the
### Mode Market is used.

def get_settle_price(t, exer_date):

	settle_market = ael.Party.read('ptyid = "internal"')
	if not settle_market:
		print '\nrow 80. The MtM Market "internal" does not exist'
		return 'error'

	und = t.insaddr.und_insaddr
	mkt_nbr = settle_market.ptynbr

	settle_price = \
		ael.Price.read('insaddr=%d and day="%s" and curr=%d and ptynbr=%d'
		%(und.insaddr, exer_date, t.curr.insaddr, mkt_nbr))

	if not settle_price:    
		for p in und.prices():
			if (p.ptynbr.ptynbr == mkt_nbr and \
				p.curr.insaddr == t.curr.insaddr and \
				p.day == ael.date(exer_date)):
				settle_price = p


	if not settle_price: #Check the trade's market instead of SETTLEMENT, take used_price() otherwise.
		if t.market_ptynbr:
			mkt_nbr = t.market_ptynbr.ptynbr
		else:
			print '\nrow102. Used price:', und.used_price(), ', Trade %d: No price was found on "SETTLEMENT" market and the trade has no market set via market_ptynbr.\n' %(t.trdnbr)
			return und.used_price()

		settle_price = \
			ael.Price.read('insaddr=%d and day="%s" and curr=%d and ptynbr=%d'
			%(und.insaddr, exer_date, t.curr.insaddr, mkt_nbr))
		if not settle_price:
			for p in und.prices():
				if (p.ptynbr.ptynbr == mkt_nbr and \
					p.curr.insaddr == t.curr.insaddr and \
					p.day == ael.date(exer_date)):
					settle_price = p	
					
	if not settle_price:
		print '\nrow116. Used price:', und.used_price(), ', No %s settlement price for "%s" on %s (%s market)'\
			%(t.curr.insid, und.insid, exer_date, t.market_ptynbr.ptyid)
		return und.used_price()


	if not (settle_price.bits & 256):
		print '\nrow122. Settle bit for "%s" is zero on %s.'\
			%(t.insaddr.insid, exer_date),\
			'No valid settlement price for trade %d' %(t.trdnbr)
		return 'noprice'

	return settle_price.settle

###############################################################################
### Find the physical delivery trade corresponding to the exercise trade
### if it already exists. Otherwise it should be created elsewhere in the script.

def get_physical_trade(t_exer):
    	print '\nrow133. Now running get_physical_trade(t_exer).'
	if not t_exer.insaddr.und_insaddr:
		return None
	und = ael.Instrument.read('insaddr=%d'
		%(t_exer.insaddr.und_insaddr.insaddr))
	trades = ael.Trade.select('contract_trdnbr=%d' %(t_exer.contract_trdnbr))
	for t in trades:
		if t.insaddr.insaddr == und.insaddr:
			return t

###############################################################################
### Update the payment of type Exercise Cash or create it if it doesn't exist.
### Only done if Settlement type is Cash.

def update_exercise_payment(t_exer, settle):
    	print '\nrow147. Now running update_exercise_payment(t_exer,settle).'
	found = 0
	excess_lots = t_exer.insaddr.contr_size - t_exer.insaddr.phys_contr_size
	if t_exer.insaddr.instype in ('Option', 'Warrant'):
		if t_exer.insaddr.call_option == 1:
			trade_price = settle - t_exer.insaddr.strike_price
		else:
			trade_price = t_exer.insaddr.strike_price - settle
	else:
		trade_price = settle

	premium = t_exer.premium_from_quote(t_exer.acquire_day, trade_price)
	new_amount = premium * excess_lots / t_exer.insaddr.contr_size
	payments = ael.Payment.select('trdnbr=%d' %(t_exer.trdnbr))

	for p in payments:
		if p.type == 'Cash': #Exercise Cash in next release
			found=1
			payment_clone = p.clone()
			payment_clone.amount = new_amount
			payment_clone.commit()          

	if not found:
		t_exer_clone        = t_exer.clone()
		new_payment         = ael.Payment.new(t_exer_clone)
		new_payment.ptynbr  = t_exer.counterparty_ptynbr
		new_payment.type    = 'Cash' #Exercise Cash in next release
		new_payment.amount  = new_amount
		new_payment.curr    = t_exer.insaddr.curr
		new_payment.payday  = t_exer.spot_date(ael.date_from_time(t_exer.time))
		t_exer_clone.commit()



"""----------------------------------------------------------------------------
FUNCTION NOT USED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 set_final_settle_prices - Sets the final settlement price in one
	Exercising derivatives trade, and potential corresponding physical
	delivery trade, done on the specified date.

DESCRIPTION
        Cash settled instruments: Read the price on the SETTLEMENT market
        first. If there is no such price, read the settle price from the
        market on which the trade was done. Set the price of the closing
        derivative trade to the difference between the settle price and the
        strike and change the premium accordingly.
 
        Physical settled instruments: Either the physical trade is done to
        market, in which case the exercise trade should carry the difference
        between strike and the settlement price, or the physical trade is done
        to the strike in which case the exercise trade should get the price
        and premium zero.

ARGUMENTS
 The function takes the following arguments:
	1) t - The Exercise trade found in get_trades().
        2) exer_date - Only Exercised trades done on this date are handled,
           i.e. the trade time of the trade with type Exercise, Assign or
           Abandon should equal this date. The settlement prices should also
           have been entered on this date.
        3) mode - This could either be set to Strike or to Market. This
           depends on whether the physical delivery trade is done to the
           strike price or to market price.
 
RETURNS
 Nothing.

def set_final_settle_prices(t, exer_date, mode):	
		p_der = 0.0 #price to be set in the derivative trade
		settle_price = get_settle_price(t, exer_date)

		if settle_price == 'error':
			return
		if settle_price == 'noprice':
			return

		#A settlement price has been found
		if t.insaddr.settlement == 'Cash':
			if t.insaddr.call_option:
				p_der = settle_price - t.insaddr.strike_price
			else:
				p_der = t.insaddr.strike_price - settle_price

		else:  #Physical settlement
			p_phys = 0.0 #price to be set in the physical trade
			t_phys = get_physical_trade(t)
			if not t_phys:
				print '\nrow238. Physical settlement trade does not exist for trade %d.'\
					%(t.trdnbr)
				return

			if mode == 'Market':
				p_phys = settle_price
				if t.insaddr.instype in ('Option','Warrant'):
					if t.insaddr.call_option:
						p_der = settle_price - t.insaddr.strike_price
					else:
						p_der = t.insaddr.strike_price - settle_price
				else: #Future
					p_der = settle_price

			else: #Physical is done to the strike price
				p_der = 0.0
				if t.insaddr.instype in ('Option','Warrant'):
					p_phys = t.insaddr.strike_price
				else: #Future
					p_phys = settle_price

			if mode == 'Strike' and \
				(abs(t.insaddr.phys_contr_size) > 0.000001 and \
				abs(t.insaddr.phys_contr_size - t.insaddr.contr_size) > 0.000001):
				update_exercise_payment(t,settle_price)

			phys_clone = t_phys.clone()
			phys_clone.price = p_phys
			phys_clone.premium = \
				phys_clone.premium_from_quote(phys_clone.acquire_day,p_phys)
			phys_clone.commit()
	
		der_clone = t.clone()
		der_clone.price = p_der
		der_clone.premium = der_clone.premium_from_quote(t.acquire_day,p_der)
		der_clone.commit()
		ael.poll
----------------------------------------------------------------------------"""


"""----------------------------------------------------------------------------
FUNCTION 
	create_exercise_trade - Closes trades in options and warrants that
	are chosen from the Macro variables window. Trades in the underlying 
	security are entered for in-the-money derivatives with physical 
	delivery.

DESCRIPTION
	Cash settled instruments: Closing trades are created for out-of-the 
	money options and warrants at price 0. The trade status is set to Abandon. 
	In-the-money options are closed at the intrinsic values.
	Trade status is set to Exercise for long positions and Assign for short.
 
        Physical settled instruments: Either the physical trade is done to
        market, in which case the exercise trade should carry the difference
        between strike and the settlement price, or the physical trade is done
        to the strike in which case the exercise trade should get the price
        and premium zero.

ARGUMENTS
 The function takes the following arguments:
	1) t - An Exercise trade found in get_trades_to_exercise().
	2) exer_date - Trades with aquire_day on or before this date will be 
	   exercised or closed out.
        3) mode - This could either be set to Strike or to Market. This
           depends on whether the physical delivery trade is done to the
           strike price or to market price.
 
RETURNS
 Nothing.
----------------------------------------------------------------------------"""
		
def create_exercise_trade(t, exer_date, mode, amount_in_percent, amount_in_number, price, pos, p):

    	if t.insaddr.instype in ('Option', 'Warrant', 'Future/Forward'):
		settle = get_settle_price(t, exer_date)
		if settle == 'error':
			return
		if settle == 'noprice':
			return
	
		ExeAss = 0
		# Check if derivatives are in the money
		if (t.insaddr.call_option==1 and t.insaddr.strike_price<settle) or \
			(t.insaddr.call_option==0 and t.insaddr.strike_price>settle): 
			ExeAss = 1	


    	### Create Close/Exercise trade:
	t_new = t.new()
	
	#t_new = ael.Trade.new(t.insaddr)
	#t_old = t.clone()
	#new_trdnbr = t_new.trdnbr
	#t_new = t_old
	#t_new.trdnbr = new_trdnbr
	
    	### Set Dates and Time:
	dt = ael.date_today()
						# Derivative trade should maybe use spot_banking_days
	dt2 = dt.add_banking_day(t.insaddr.curr, t.insaddr.pay_day_offset)

	t_new.value_day = dt2
	t_new.acquire_day = dt2
	t_new.time = time.time()  # correct for UTC time
	
	### Set Quantity:
	if amount_in_number != None and amount_in_number != 0:
	    	quantity = float(amount_in_number)
	else:
	    	quantity = pos.values[p][0]
		#quantity = pos[p][0]
	#t_new.quantity = -t.quantity
	t_new.quantity = - quantity * amount_in_percent
	
	### Set Price:
	if price != None:
	    	t_new.price = float(price)
	
	### Set Premium:
	t_new.premium = t_new.premium_from_quote(ael.date(exer_date), t_new.price)
	print 'Closing Premium:', t_new.premium
	
	### Set Trade Type:
	if ExeAss == 0:
		t_new.type = 'Abandon'
	elif t.quantity > 0:
		t_new.type = 'Exercise'
	else:
		t_new.type = 'Assign'
		
    	### Set portfolio:
	t_new.prfnbr = p

	### Set BO-Contract Trade Number:
	t_new.contract_trdnbr = t.trdnbr
	
	try:
		t_new.commit()
	except RuntimeError:
		print '\nrow364. Error:', t_new.type, 'Trade', t_new.trdnbr, 'in', t.insaddr.insid, 'at settle price', settle
		return
	print '\nrow369.', t_new.type, 'Trade', t_new.trdnbr, 'in', t_new.insaddr.insid, 'at settle price', settle



	### Create physical trade if derivative is in the money:
	
	if t.insaddr.settlement == 'Physical Delivery' and ExeAss == 1:
	#if (t.insaddr.settlement == 'Physical Delivery' 
	    #or t.insaddr.instype == 'Convertible') and ExeAss == 1: #ExeAss == 1 means only derivatives in the money
		#tu_new = ael.Trade.new(t.insaddr.und_insaddr)
    	    	tu_new = t.new()
		
		#t_old = t.clone()
		#new_trdnbr = tu_new.trdnbr
		#tu_new = t_old
		#tu_new.trdnbr = new_trdnbr
		
		tu_new.insaddr = t.insaddr.und_insaddr
		tu_new.value_day = dt2
		tu_new.acquire_day = dt2
		tu_new.time = time.time()  # correct for UTC time

		cs = t.insaddr.phys_contr_size
		if cs == 0:
			cs = t.insaddr.contr_size


		if t.insaddr.call_option == 1 : 
			#tu_new.quantity = t.quantity * cs
			tu_new.quantity = quantity * cs * amount_in_percent
		else:
			#tu_new.quantity = - t.quantity * cs     
			tu_new.quantity = - quantity * cs * amount_in_percent


		if t.quantity > 0:
			tu_new.type = 'Exercise'
		else:
			tu_new.type = 'Assign'
		tu_new.prfnbr = p
		tu_new.contract_trdnbr = t.trdnbr
		###Added by BDR
		tu_new.price=t.insaddr.strike_price
		try:
			tu_new.commit()
		except RuntimeError:
			print '\nrow418. Error:', tu_new.type, 'Trade', tu_new.trdnbr, 'in', t.insaddr.insid, 'at settle price', settle
			return
		ael.poll()

		print '\nrow422.', tu_new.type, 'Trade', tu_new.trdnbr, 'in', tu_new.insaddr.insid, 'at settle price', settle
	


#######################################################################################
# main loop	
#######################################################################################

def exercise(exer_date, mode, autoexe, ins, pf, amount_in_percent, amount_in_number, price):
    	
	#print ins, type(ins)
	#print ins.instype, type(ins.instype)

	verb = 1
	debug = 1
	log = 0
	lf = None
	#instype = ins.instype

	if autoexe[0] == 'Y' or autoexe[0] == 'y':
		extrades = get_trades_to_exercise(exer_date, ins, pf)
		
		if not extrades:
		    	#print 'No trades to Exercise/Assign on date %s.' %(exer_date)
			print 'No trades to Exercise/Assign.'
		else:
    	    	    	### Calculate the positions in the instrument, per portfolio:
    	    	    	rec_date = ael.date(exer_date) #Only trades with acquire_date <= rec_date are included.
			prf = None #Assuming all trades should land in original portfolios.
			acc_method = 'Open Average' #For avg_price() calculation.
            	    	try:
			    	pos = FCAGeneral.position(log, lf, debug, extrades, rec_date, prf, acc_method)
            	    	except IndexError:
            	    	    	s = '\nNo trades in instrument %s.\n' % ca.insaddr.insid
                    	    	print s

    	    	    	### Create the trades in chosen portfolio with a position:
			#for t in extrades:
				#create_exercise_trade(t, exer_date, mode)
			for p in pos.keys():
			    	if pos[p][0] != 0.0:
			    	    	create_exercise_trade(extrades[0], exer_date, mode, 
					amount_in_percent, amount_in_number, price, pos, p)
    	    	    	    	else:
				    	print '\nZero position in portfolio', p.prfid
			
######################################################################
######################################################################
### Main
######################################################################

import FCAGeneral
instrs = FCAGeneral.instr()
pfs = FCAGeneral.pf()
cas = ['Buyback', 'Merger', 'New Issue', 'Stock Dividend', 'Conversion', 'Capital Adjustment']

ael_variables = \
	[('ins', 'Instrument', 'string', instrs, 'BMWtender'),
	('pf', 'Portfolio', 'string', pfs, 'AGGREGATE', 0, 1),
	#('amount_in_percent', 'Amount (fraction of pf)', 'string', '', '', 0, 0),
	('amount_in_number', 'Amount (quantity per pf)', 'string', '', '1', 0, 0),
	#('price', 'Price', 'string', '', '', 0, 0),
	('exer_date', 'Date', 'string', [], str(ael.date_today()), 1),
	('mode', 'Mode', 'string', ['Market', 'Strike'], 'Strike', 1)]
	#('autoexe', 'AutoExe', 'string', ['Yes','No'], 'Yes', 1)]

def ael_main(dict):
	#exercise(dict['exer_date'], dict['mode'], dict['autoexe'])

    	autoexe = 'Yes' #dict['autoexe']

	ins = ael.Instrument[dict['ins']]

    	price = None #dict.get('price')
	#if dict['price'] != None:
	    	#price = float(dict['price'])
	#else: 	price = dict['price']

    	amount_in_percent = 1 #dict.get('amount_in_percent')
	amount_in_number = dict.get('amount_in_number')
	print type(1)

    	exercise(dict['exer_date'], dict['mode'], autoexe, 
		 ins, dict['pf'], amount_in_percent, amount_in_number, price)






