"""
Bond Archiving Code.

AEL code to archive bond positions up until a year end. Creates or amends one aggregate trade
for each combination of bond, portfolio, currency, trade area (Trade Key1) and acquirer.

All calculations implemented according to specifications given in Front
doc FCA 1816-1C, specifically section 5.

Has been written to be as robust as possible, with automatic error recovery.

2003-11-04  -	Russel Webber	-   Created
"""

import ael

#Calc Avg Price - set to 1 to calculate the aggregate trade's average price, else the
#MTM price at year end will be used.
calc_avg_price = 0

#Trade Status selection string
trade_status = '(%d)'% ael.enum_from_string('TradeStatus', 'BO Confirmed')

#Debug Flag, set to 1 to see detailed progress info
debug = 1

#Accounting method used in calculations
acc_method = 'FIFO'

#Funding - Account for funding costs
funding = 0

#Year-End date, trades archived up until this date.
year_end = ael.date('2003-03-31')

#Use Sybase and AEL transactions - This is the better option, but doesn't work for very large quantities
transactions = 0

#Aggregate trade trader
agg_trader = ael.User['AGGREGATE']

#Aggregate party
agg_party = ael.Party['AGGREGATE']

class AggregatePayment:
    """Class to encapsulate values and functions related to an aggregate payment."""

    def __init__(self, type, payday, curr, amount):

	self.type = type
	self.payday = payday
	self.curr = curr
	self.amount =  amount

class AggregateBondTrade:
    """Class to encapsulate values and functions related to an aggregate bond trade."""

    def __init__(self, ins, portfolio, curr, trade_area, acquirer, archive_date):
    	"""Initialisation method.

	Method creates an object with all calculated values required for an aggregate trade
	for position specified by parameters.

	Parameters:
	ins 	    	-   AEL Entity  -   Bond to be archived
	portfolio   	-   AEL Entity  -   Portfolio to be archived
	curr	    	-   AEL Entity  -   Currency to be archived
	trade_area  	-   AEL Entity  -   Trade Area to be archived
	acquirer    	-   AEL Entity	-   Acquirer to be archived
	archive_date	-   AEL Date	-   Only archive trades up to this date

	"""
    	try:

    	    if debug: print 'Creating aggregate trade object.'

    	    self.calcs_completed = 0

	    #Get all trades matching supplied criteria

    	    q = ''' SELECT
	    	    	    trdnbr
		    FROM
		    	    trade t noholdlock
		    WHERE
		    	    t.optkey1_chlnbr = %d
		    and     t.insaddr = %d
		    and     t.prfnbr = %d
		    and     t.curr = %d
		    and     t.acquirer_ptynbr = %d
		    and     t.value_day <= "%s"
		    and     t.aggregate = 0
		    and     t.status in %s''' % \
		    (trade_area.seqnbr, ins.insaddr, portfolio.prfnbr, curr.insaddr, \
			acquirer.ptynbr, archive_date.to_string('%Y-%m-%d'), trade_status)

    	    self.trades = []

    	    for res in ael.dbsql(q)[0]:

		self.trades.append(ael.Trade[res[0]])

    	    if debug: print 'Retrieved trades to be archived.'

	    #Set basic aggregate trade properties

    	    self.value_day = archive_date
	    self.acquire_day = archive_date
	    self.time = archive_date.to_time()
	    self.creat_time = ael.date_valueday().to_time()
	    self.updat_time = ael.date_valueday().to_time()
	    self.prfnbr = portfolio
	    self.optkey1_chlnbr = trade_area
	    self.insaddr = ins
	    self.curr = curr
	    self.trade_curr = curr
	    self.counterparty_ptynbr = agg_party
	    self.acquirer_ptynbr = acquirer
	    self.trader_usrnbr = agg_trader
	    self.creat_usrnbr = ael.user()
	    self.updat_usrnbr = ael.user()
	    self.owner_usrnbr = ael.user()
	    self.status = ael.enum_from_string('TradeStatus', 'BO Confirmed')
	    self.aggregate = 1
	    self.archive_status = 0
	    self.type = ael.enum_from_string('TradeType', 'Normal')

    	    if debug: print 'Basic aggregate trade properties set.'

    	    #Calculate calculated aggregate trade values.

	    self.quantity = 0
	    self.fee = 0
	    self.interest_accrued = 0
	    self.interest_settled = 0
	    self.funding = 0

	    for t in self.trades:
		self.quantity = self.quantity + t.quantity
		self.fee = self.fee + t.fees(ael.SMALL_DATE, self.value_day, curr.insid, 3)
		self.interest_accrued = self.interest_accrued \
	    	    + t.interest_accrued(ael.SMALL_DATE, self.value_day, curr.insid)
		self.interest_settled = self.interest_settled \
	    	    + t.interest_settled(ael.SMALL_DATE, self.value_day, curr.insid)
		if funding: self.funding = self.funding \
	    	    + t.accumulated_funding(self.value_day, curr.insid, 3, 0, '', 0, 'Continuous')

	    if calc_avg_price:
	    	self.price = ael.avg_price(self.trades, self.value_day, self.curr, acc_method, 3)
	    else:
	    	self.price = self.insaddr.mtm_price(self.value_day, self.curr.insid, 1)

	    self.premium = ins.premium_from_quote(self.value_day, self.price) * self.quantity
	    self.aggregate_pl =  ael.rpl(self.trades, ael.SMALL_DATE, self.value_day, curr, acc_method, 3) \
	    	    	    	    - self.fee - self.interest_accrued - self.interest_settled
    	    if debug: print 'Calculations completed.'


    	    #Create objects to represent any payments that need to be attached to
	    #the aggregate trade.

    	    self.payments = []

	    if self.funding != 0.0:
		self.payments.append(AggregatePayment(ael.enum_from_string('PaymentType', 'Aggregated Funding'), \
	    	    self.value_day, self.curr, self.funding))
    	    if self.fee != 0.0:
		self.payments.append(AggregatePayment(ael.enum_from_string('PaymentType', 'Aggregated Fees'), \
	    	    self.value_day, self.curr, self.fee))
	    if self.interest_settled != 0.0:
		self.payments.append(AggregatePayment(ael.enum_from_string('PaymentType', 'Aggregated Settled'), \
	    	    self.value_day, self.curr, self.interest_settled))
	    if self.interest_accrued != 0.0:
		self.payments.append(AggregatePayment(ael.enum_from_string('PaymentType', 'Aggregated Accrued'), \
	    	    self.value_day, self.curr, self.interest_accrued))

    	    if debug: print 'Created payment objects.'

    	    if debug: print 'Aggregate trade object creation completed.'

    	    self.calcs_completed = 1

	except Exception, err:

    	    print 'Error calculating aggregate trade values for position Bond %s, Portfolio %s, Currency %s, TradArea %s'%\
	    	    (ins.insid, portfolio.prfid, curr.insid, trade_area.entry)
	    print 'Error: ', err

    def save(self):
    	"""Save method.

	Method creates/amends a physical aggregate trade, with associated payments,
	according to the properties set by the initialisation method.
    	"""
    	try:

	    #Start database transaction

	    if transactions: ael.begin_transaction()
	    if transactions: ael.dbsql('BEGIN TRANSACTION')

    	    if not self.calcs_completed: raise ValueError, 'Calcs did not complete.'

	    #Create/Amend aggregate trade - Use SQL

	    q = '''SELECT 
	    	    	  sum(trdnbr), count(trdnbr)
		   FROM 
		          trade nooholdlock
		   WHERE 
		    	   aggregate = 1 
		   and     prfnbr = %d
		   and     curr = %d
		   and     insaddr = %d
		   and	   acquirer_ptynbr = %d
		   and     status in %s
		   and     optkey1_chlnbr = %d''' % \
		   (self.prfnbr.prfnbr, self.curr.insaddr, self.insaddr.insaddr, \
		    	self.acquirer_ptynbr.ptynbr, trade_status, self.optkey1_chlnbr.seqnbr)


	    aggtrd, count = ael.dbsql(q)[0][0]
	    aggtrd = int(aggtrd)

	    if count > 1:

	    	#Delete aggregate trades

		if debug: print 'Deleting multiple aggregate trades.'

		q = '''DELETE FROM trade
		       WHERE	
	    	    	    	aggregate = 1 
		    	and     prfnbr = %d
		    	and     curr = %d
		    	and     insaddr = %d
			and 	acquirer_ptynbr = %d
			and 	status in %s
		    	and     optkey1_chlnbr = %d''' % \
		   (self.prfnbr.prfnbr, self.curr.insaddr, trade_status, self.insaddr.insaddr, \
		    	self.acquirer_ptynbr.ptynbr, self.optkey1_chlnbr.seqnbr)

    	    	ael.dbsql(q)

	    	count = 0

	    if count == 0:

	    	#Create aggregate trade

		if debug: print 'Start trade creation'

		t = ael.Trade.new(self.insaddr)
 	    	t.value_day = self.value_day
	    	t.acquire_day = self.acquire_day
	    	t.time = self.time
	    	t.creat_time = self.creat_time
	    	t.updat_time = self.updat_time
	    	t.prfnbr = self.prfnbr
	    	t.optkey1_chlnbr = self.optkey1_chlnbr
    	    	t.curr = self.curr
	    	t.trade_curr = self.trade_curr
	    	t.counterparty_ptynbr = self.counterparty_ptynbr
	    	t.acquirer_ptynbr = self.acquirer_ptynbr
	    	t.trader_usrnbr = self.trader_usrnbr
	    	t.creat_usrnbr = self.creat_usrnbr
	    	t.updat_usrnbr = self.updat_usrnbr
	    	t.owner_usrnbr = self.owner_usrnbr
	    	t.status = ael.enum_to_string('TradeStatus', self.status)
	    	t.type = ael.enum_to_string('TradeType', self.type)
    	    	t.quantity = self.quantity
		t.price = self.price
		t.premium = self.premium
  	    	t.fee = self.fee
    		t.aggregate_pl = self.aggregate_pl
	    	t.archive_status = self.archive_status

    		t.commit()

		if debug: print 'Trade created OK'

		aggtrd = t

	    elif count == 1:

	    	#Amend aggregate trade

	    	#In archive mode the aggregate trade will be hidden,
		#so we need to make it available to AEL first.

		if debug: print 'Start trade updating'

    	    	q = '''UPDATE
		    	      trade
		       SET
		              aggregate = 0
		       WHERE
		              trdnbr = %d''' % (aggtrd)

		ael.dbsql(q)

    	    	if debug: print 'Set aggregate flag off.'

    	    	if debug: print 'AggTrd:', aggtrd

    	    	ael.poll()

		t = ael.Trade[aggtrd].clone()
 	    	t.value_day = self.value_day
	    	t.acquire_day = self.acquire_day
	    	t.time = self.time
	    	t.creat_time = self.creat_time
	    	t.updat_time = self.updat_time
	    	t.prfnbr = self.prfnbr
	    	t.optkey1_chlnbr = self.optkey1_chlnbr
    	    	t.curr = self.curr
	    	t.trade_curr = self.trade_curr
	    	t.counterparty_ptynbr = self.counterparty_ptynbr
	    	t.acquirer_ptynbr = self.acquirer_ptynbr
	    	t.trader_usrnbr = self.trader_usrnbr
	    	t.creat_usrnbr = self.creat_usrnbr
	    	t.updat_usrnbr = self.updat_usrnbr
	    	t.owner_usrnbr = self.owner_usrnbr
	    	t.status = ael.enum_to_string('TradeStatus', self.status)
	    	t.type = ael.enum_to_string('TradeType', self.type)
    	    	t.quantity = self.quantity
		t.price = self.price
		t.premium = self.premium
  	    	t.fee = self.fee
    		t.aggregate_pl = self.aggregate_pl
	    	t.archive_status = self.archive_status

		t.commit()

		aggtrd = t

		if debug: print 'Trade amended OK'

	    if debug: print aggtrd, count

	    if debug: print 'Linking archived trades to aggregate trade.'


	    for t in self.trades:

	    	#Mark payments as archived - Use AEL

		for p in t.payments():

		    pc = p.clone()
		    pc.archive_status = 1
		    pc.commit()

	    	#Mark trades as archived & link to agg trd - Use AEL

    		tc = t.clone()
		tc.archive_status = 1
		tc.aggregate_trdnbr = aggtrd
		tc.commit()

	    if debug: print 'Marked trades as archived and linked to agg trd.'

	    #Delete old aggregate payments - Use AEL

	    if debug: print 'Start deleting old payments'

	    for p in aggtrd.payments():

	    	p.delete()

	    if debug: print 'Old payments deleted OK'

	    #Create new aggregate payments - Use AEL

	    if debug: print 'Start creating new payments'

    	    for payment in self.payments:

	    	p = ael.Payment.new(aggtrd)
		p.type = ael.enum_to_string('PaymentType', payment.type)
	    	p.payday = payment.payday
    	    	p.curr = payment.curr
	    	p.amount =  payment.amount
		p.commit()

	    if debug: print 'New payments created OK'

	    if debug: print 'Commiting'

	    #Commit database transaction

	    if transactions: ael.commit_transaction()
	    if transactions: ael.dbsql('COMMIT TRANSACTION')

	    #Set aggregate trade's aggregate field to 1

	    if debug: print 'Setting aggregate field.'

	    t = aggtrd.clone()
	    t.aggregate = self.aggregate
	    t.commit()

	    if debug: print 'OK'

	    ael.log('Position Bond %s, Curr %s, Portfolio %s, TradArea %s archived successfully.' % \
	    	(self.insaddr.insid, self.curr.insid, self.prfnbr.prfid, self.optkey1_chlnbr.entry))
	    ael.log('%d trades archived.' % (len(self.trades)))

	    return 1

	except Exception, err:

	    #Rollback database transaction.

	    if transactions: ael.abort_transaction()
	    if transactions: ael.dbsql('ROLLBACK TRANSACTION')


	    ael.log('Problem archiving position Bond %s, Curr %s, Portfolio %s, TradArea %s.' % \
	    	(self.insaddr.insid, self.curr.insid, self.prfnbr.prfid, self.optkey1_chlnbr.entry))
    	    if transactions: ael.log('Transactions rolled back.')
	    ael.log('Error:' + str(err))

	    print 'Value of transactions', transactions

	    if not transactions:

		ael.log('Attempting to unarchive position.')
		self.unarchive()

	    return -1

    def unarchive(self):
    	"""Undo archiving for this aggregate trade.

	Should only be used if not using database transactions."""

	try:

    	    #Reset trades to unarchived.

	    q = '''
    		UPDATE 
	    	    trade 
    		SET 
	    	    archive_status = 0, 
	    	    aggregate_trdnbr = NULL 
    		WHERE 
	    	    archive_status = 1
		and optkey1_chlnbr = %d
		and status in %s
		and insaddr = %d
		and acquirer_ptynbr = %d
		and prfnbr = %d
		and curr = %d''' % \
		(self.optkey1_chlnbr.seqnbr, trade_status, self.insaddr.insaddr, \
	    	    self.acquirer_ptynbr.ptynbr, self.prfnbr.prfnbr, self.curr.insaddr)

    	    ael.dbsql(q)
    	    if debug: print 'Reset trades to unarchived.'

    	    #Reset payments to unarchived.

    	    q = '''
    		UPDATE
	    	    payment
    		SET
	    	    archive_status = 0
    		WHERE
	    	    archive_status = 1
		and trdnbr IN 
		(
		SELECT
	    	    trdnbr 
		FROM
	    	    trade
		WHERE
	     	    optkey1_chlnbr = %d
		and insaddr = %d
		and acquirer_ptynbr = %d
		and status in %s
		and prfnbr = %d
		and curr = %d
		)''' % \
		(self.optkey1_chlnbr.seqnbr, self.insaddr.insaddr, self.acquirer_ptynbr.ptynbr, \
		    trade_status, self.prfnbr.prfnbr, self.curr.insaddr)

    	    ael.dbsql(q)
    	    if debug: print 'Reset payments to unarchived.'

    	    #Delete aggregate trade's payments

    	    q = '''
    		DELETE 
    		FROM
	    	    payment 
    		WHERE
	    	    trdnbr IN
    		(SELECT 
	    	    trdnbr 
		FROM 
	    	    trade 
		WHERE
	    	    aggregate = 1
		and optkey1_chlnbr = %d
		and status in %s
		and insaddr = %d
		and acquirer_ptynbr = %d
		and prfnbr = %d
		and curr = %d
		)''' % \
		(self.optkey1_chlnbr.seqnbr, trade_status, self.insaddr.insaddr, \
	    	    self.acquirer_ptynbr.ptynbr, self.prfnbr.prfnbr, self.curr.insaddr)

    	    ael.dbsql(q)
	    if debug: print 'Deleted aggregate trade\'s payments'

    	    #Delete aggregate trade.

    	    q = '''
    		DELETE 
    		FROM 
	    	    trade 
    		WHERE 
	    	    aggregate = 1
		and optkey1_chlnbr = %d
		and insaddr = %d
		and status in %s
		and acquirer_ptynbr = %d
		and prfnbr = %d
		and curr = %d''' % \
		(self.optkey1_chlnbr.seqnbr, self.insaddr.insaddr, trade_status, \
	    	    self.acquirer_ptynbr.ptynbr, self.prfnbr.prfnbr, self.curr.insaddr)

    	    ael.dbsql(q)
    	    if debug: print 'Deleted aggregate trade.'

    	    ael.log('Position unarchived successfully.')

	except:

	    ael.log('SEVERE ERROR: Unable to automatically restore position. MANUAL INTERVENTION REQUIRED.')

def acquirers():
    acq_list = []

    for p in ael.Party:
		if p.type in ('Counterparty', 'Client'):
			acq_list.append(p.ptyid)

    return acq_list

def currencies():

    curr_list = []

    for i in ael.Instrument.select('instype = "Curr"'):
    	curr_list.append(i.insid)

    return curr_list

def bonds():

    bond_list = []

    for i in ael.Instrument.select('instype = "Bond"'):
    	bond_list.append(i.insid)

    return bond_list

def portfolios():

    portfolio_list = []

    for p in ael.Portfolio:
    	portfolio_list.append(p.prfid)

    return portfolio_list


def trade_areas():

    ta_list = []

    for cl in ael.ChoiceList:

    	if cl.list == 'TradArea':

	    ta_list.append(cl.entry)

    return ta_list

ael_variables = [('bond', 'Bond', 'string', bonds(), 'ZAR/R150', 0),
    	     	('portfolio', 'Portfolio', 'string', portfolios(), 'DERV', 0),
             	('trade_area', 'TradArea', 'string', trade_areas(), 'DER001', 0),
             	('currency', 'Currency', 'string', currencies(), 'ZAR', 0),
             	('acquirer', 'Acquirer', 'string', acquirers(), None, 0),
             	('all', 'Archive All', 'string', ['Yes', 'No'], 'No', 1)]

def ael_main(ael_dict):

    #Must be in archived mode
    if not ael.archived_mode():

	print 'Must run this AEL in archived mode.'

    else:

    	if ael_dict['all'] == 'Yes':

	    #Get all instrument, portfolio, currency, trade area, acquirer combinations

	    q = '''SELECT
    	    		    t.insaddr,
			    t.prfnbr,
			    t.curr,
			    t.optkey1_chlnbr,
			    t.acquirer_ptynbr
		   FROM
            		    trade t noholdlock,
			    instrument i,
			    portfolio p
		   WHERE
			    t.insaddr = i.insaddr
		   and      t.prfnbr <> NULL
		   and      t.aggregate = 0
		   and      t.optkey1_chlnbr <> NULL
		   and      (i.instype = %d or i.instype = %d)
		   and      t.status in %s
		   and	    t.value_day <= "%s"
		   and	    p.prfid not in ('ABS1','ABS2')
		   and	    p.prfnbr = t.prfnbr
		   GROUP BY 
    	    		    t.insaddr,
			    t.prfnbr,
			    t.curr,
			    t.optkey1_chlnbr,
			    t.acquirer_ptynbr			    
		   HAVING
            		    count(t.trdnbr) > 0''' % (ael.enum_from_string('InsType', 'Bond'), ael.enum_from_string('InsType', 'IndexLinkedBond'), \
		    trade_status, year_end.to_string('%Y-%m-%d'))

	    combinations = []
    	    print ael_dict['bond']
	    for combination in ael.dbsql(q)[0]:

    		combinations.append(combination)
    	    for combo in combinations:
    		AggregateBondTrade(ael.Instrument[combo[0]], ael.Portfolio[combo[1]], ael.Instrument[combo[2]], \
    		    ael.ChoiceList[combo[3]], ael.Party[combo[4]], year_end).save()

    	else:

	    #Painful way of getting the choice list

	    for cl in ael.ChoiceList:
	    	if cl.list == 'TradArea' and cl.entry == ael_dict['trade_area']:
		    break

	    AggregateBondTrade(ael.Instrument[ael_dict['bond']], ael.Portfolio[ael_dict['portfolio']], \
    	    	ael.Instrument[ael_dict['currency']], \
    	    	cl, \
		ael.Party[ael_dict['acquirer']],
   	    	year_end).save()
