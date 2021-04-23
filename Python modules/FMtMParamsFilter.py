""" MarkToMarket:1.1.7 """

"""----------------------------------------------------------------------------
MODULE
    FMtMParams - Parameters for the Mark To Market procedure.

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Extracts and computes parameters for the Mark to Market procedure. Saves
    settlement prices and volatilities.

----------------------------------------------------------------------------"""
try:
    import string
except ImportError:
    print 'The module string was not found.'
    print
try:
    import ael
except ImportError:
    print 'The module ael was not found.'
    print
try:
    import time
except ImportError:
    print 'The module time was not found.'
    print
try:
    import FMtMGeneral
except ImportError:
    print 'The module FMtMGeneral was not found.'
    print
try:
    import FMtMVariables
    reload(FMtMVariables)
    print 'loaded'
except AttributeError, msg:
    print 'WARNING! All FMtMVariables have to be defined. Undefined:', msg
force_positive_mtm_price = FMtMVariables.ForcePositiveMtMPrice
update_vol = FMtMVariables.UpdateVol
update_otc_vol = FMtMVariables.UpdateOTCVol
recalc_vol = FMtMVariables.RecalcVol

"""----------------------------------------------------------------------------
CLASS			
    FMarkToMarket - Parameters for MarkToMarket.

INHERITS
    FMtMExecute
  	    	
DESCRIPTION		
    The class extracts all parameters needed to perform Mark-To-Market.

CONSTRUCTION	
    market  	Market	    An internal market where the MtM-prices are stored
    volmarket	Market	    An internal market where the volatilites are stored
    date    	Date	    The date on which the MtM-prices are stored
    base_curr	Currency    The currency against which the MtM prices are 
    	    	    	    stored for instruments of type Currency
    aliastypes	AliasTypes  alias
    spread  	float	    A spread which is substracted from the MtM-price
    	    	    	    for index warrants
    bid_and_ask int    	    If 0, no bid or ask prices will be stored, 
    	    	    	    otherwise bid and ask prices will be stored
    digits  	int 	    Rounding
    verbosity	int 	    Integer that indicate the level of information that
    	    	    	    will be generated in the AEL console

----------------------------------------------------------------------------"""

class FMarkToMarket:
    """MarkToMarket"""
    
    def __init__(self, market, volmarket, date, base_curr, aliastypes, 
    	    	 distributors, spread, bid_and_ask, digits, verbosity, tflist):
        """Constructor. Initialize and start MarkToMarket procedure."""
 
        self.market = market
	self.volmarket = volmarket
        self.date = date
        self.base_curr = ael.Instrument[base_curr]
	self.aliastypes = aliastypes
	self.distributors = distributors
	self.spread = spread
        self.bid_and_ask = bid_and_ask
	self.digits = digits	    	    	# Added rounding
        self.verbosity = verbosity
        self.batch_size = 10
        self.batch_count = 0
        self.trace(1, "MarkToMarket started %s" % str(time.ctime(time.time())))
    	self.B = tflist
	self.add_instruments()
    	self.handled_ins = {}
	self.ins1 = {} #ins1 = []
	self.ins4 = {} #[]
	self.ins2 = []
	self.ins3 = []


		    
	if aliastypes != None:
	    (self.ins1, alias_ins) = FMtMGeneral.find_alias_ins(aliastypes)
	    # self.ins1 is a dictionary with key = underlying, 
	    # and items for each key = options on the underlying
	    # alias_ins is the number of options in the dictionary (an integer)
	
	if distributors != None:
	    (self.ins4, dist_ins) = \
	    FMtMGeneral.find_distributors_ins(distributors)
	    # self.ins4 is a list of instruments (ael entities)
	    # dist_ins is the number of instruments in the list (an integer)
	self.ins2 = FMtMGeneral.find_opt_and_warrants_on_stock()
	self.ins3 = FMtMGeneral.find_opt_and_warrants_on_index()
    	ins_dict = {}
	for i in self.underlyings.values():
	    ins_dict[i.insid] = 1
	for (und, olist) in self.ins1.items(): #underlying, optionlist
	    for i in olist:
	        ins_dict[i.insid] = 1
	#for i in self.ins4:
	    #ins_dict[i.insid] = 1
	for (und, olist) in self.ins4.items(): #underlying, optionlist
	    for i in olist:
	        ins_dict[i.insid] = 1
	
	ins2tmp = []        
	for i in self.ins2:
	    if not ins_dict.has_key(i.insid):
	    	ins2tmp.append(i)
	    else:
	        ins_dict[i.insid] = 1
	self.ins2 = ins2tmp
	
	ins3tmp = []
	for i in self.ins3:
	    if not ins_dict.has_key(i.insid):
	        ins3tmp.append(i)
	    else:
	        ins_dict[i.insid] = 1
	self.ins3 = ins3tmp
	
	count_rest = len(self.instruments)
	count_rest = count_rest - 1
	for i in self.instruments.values():
	    if ins_dict.has_key(i.insid):
	    	count_rest = count_rest - 1
	
	if aliastypes == None: alias_ins = 0
	#if distributors == None: dist_ins = 0
	self.work_size = float(len(self.underlyings)+alias_ins+alias_ins+
	    	    	       len(self.ins4)+len(self.ins2)+len(self.ins3)+
			       count_rest)
        self.work_count = 0
        self.work_percent = 0.1
	
    def do_mtm_underlying(self):
    	try:
            ael.abort_transaction()
        except:
            pass
        ael.begin_transaction()
	for ins in self.underlyings.values():
	    #print '1',ins.insid, time.ctime(time.time())
	    self.work_in_progress()
            self.store_mtm_price(ins, ins.curr, 0, 0)
            self.commit_work(1)
        ael.abort_transaction()
    	
    def do_mtm_for_alias(self):	
	"""Save MtM-prices for all instruments that have type=aliastypes"""
	#(instruments,count) = FMtMGeneral.find_alias_ins(self.aliastypes)
	#for i in self.ins1.keys(): #type(self.ins1)=dictionary
	    #print 'Check if same instr.',i.insid
	    #for o in self.ins1[i]: print o.insid
	try:
            ael.abort_transaction()
        except:
            pass
        ael.begin_transaction()
	
	for (und, olist) in self.ins1.items(): #instruments.items():
	    for ins in olist:
	    	self.work_in_progress()
	    	self.store_mtm_price(ins, ins.curr, 1, 1)
                self.commit_work(1)
        ael.abort_transaction()
	
    def do_save_aliastype_vols(self):
    	#(instruments,count) = FMtMGeneral.find_alias_ins(self.aliastypes)
	
    	try:
            ael.abort_transaction()
        except:
            pass
        ael.begin_transaction()
	if self.B != []:
	    for (und, olist) in self.ins1.items(): #instruments.items():
	    	for ins in olist:
		    if ins.insid in self.B:
	    	    	self.work_in_progress()
	    	    	self.store_vol(ins, ins.curr, 1, 1)
                    	self.commit_work(1)
            ael.abort_transaction()
	else:
	    for (und, olist) in self.ins1.items(): #instruments.items():
	    	for ins in olist:
	    	    self.work_in_progress()
	    	    self.store_vol(ins, ins.curr, 1, 1)
                    self.commit_work(1)
            ael.abort_transaction()
	
    def do_mtm_for_distributors(self):	
	"""Save MtM-prices for all instruments that have distributor"""
	try:
            ael.abort_transaction()
        except:
            pass
        ael.begin_transaction()
    	if self.B != []:
	    for (und, olist) in self.ins4.items(): #ins in instruments:
	    #for ins in self.ins4:
	    	#if not self.handled_ins.has_key(ins.insid):
	    	for ins in olist:
		    if ins.insid in self.B:
		    	self.work_in_progress()
		    	self.store_mtm_price(ins, ins.curr, 1, 1)
        	    	self.commit_work(1)
	    ael.abort_transaction()
	else:
    	    for (und, olist) in self.ins4.items(): #ins in instruments:
	    #for ins in self.ins4:
	    	#if not self.handled_ins.has_key(ins.insid):
	    	for ins in olist:
		    self.work_in_progress()
		    self.store_mtm_price(ins, ins.curr, 1, 1)
        	    self.commit_work(1)
	    ael.abort_transaction()
	
    def do_save_distributors_vols(self):
    	try:
            ael.abort_transaction()
        except:
            pass
        ael.begin_transaction()
    	if self.B != []:
	    for (und, olist) in self.ins4.items(): 
	    #for ins in self.ins4: #instruments:
	    	for ins in olist:
		    if ins.insid in self.B:
	    	    	self.work_in_progress()
	    	    	self.store_vol(ins, ins.curr, 1, 1)
            	    	self.commit_work(1)
            ael.abort_transaction()
	else:
	    for (und, olist) in self.ins4.items(): 
	    #for ins in self.ins4: #instruments:
	    	for ins in olist:
	    	    self.work_in_progress()
	    	    self.store_vol(ins, ins.curr, 1, 1)
            	    self.commit_work(1)
            ael.abort_transaction()
	    
	
    def do_mtm_opt_and_warrants_on_stock(self):
    	#instruments = FMtMGeneral.find_opt_and_warrants_on_stock()
	try:
            ael.abort_transaction()
        except:
            pass
        ael.begin_transaction()
	self.trace(3, 'Already handled instruments, so far:')
    	for i, j in self.handled_ins.items():
	    self.trace(3, '%s' % i)
	
	for ins in self.ins2: #instruments:
	    if not self.handled_ins.has_key(ins.insid):
# ABSA Added Code
#-----------------
    	    	if self.B != []:
    	    	    if ins in self.B:
#-----------------		  
		    	self.work_in_progress()
	            	self.store_mtm_price(ins, ins.curr, 1, 1)
	            	if update_otc_vol and \
		    	    (ins.instype == 'Option' or ins.instype == 'Warrant'):
		    	    self.store_vol(ins, ins.curr, 1, 1)
               	    	self.commit_work(1)
	    	else:
		    self.work_in_progress()
	            self.store_mtm_price(ins, ins.curr, 1, 1)
	            if update_otc_vol and \
		        (ins.instype == 'Option' or ins.instype == 'Warrant'):
		    	self.store_vol(ins, ins.curr, 1, 1)
               	    	self.commit_work(1)    	    
        ael.abort_transaction()
	
    def do_mtm_opt_and_warrants_on_index(self):
    	#instruments = FMtMGeneral.find_opt_and_warrants_on_index()
	try:
            ael.abort_transaction()
        except:
            pass
        ael.begin_transaction()
	if self.B != []:
	    for ins in self.ins3: #instruments:
	    	if ins.insid in self.B:
# commented to test for EQ    	    if not self.handled_ins.has_key(ins.insid):
            	    self.work_in_progress()
	            self.store_mtm_price(ins, ins.curr, 1, 0)
	        
	            if update_otc_vol and \
		        (ins.instype == 'Option' or ins.instype == 'Warrant'):
		        self.store_vol(ins, ins.curr, 1, 1)

                    self.commit_work(1)
            ael.abort_transaction()
	else:
	    for ins in self.ins3: #instruments:
#	    	if not self.handled_ins.has_key(ins.insid):
	        self.work_in_progress()
	        self.store_mtm_price(ins, ins.curr, 1, 0)
	        
	        if update_otc_vol and \
		    (ins.instype == 'Option' or ins.instype == 'Warrant'):
		    self.store_vol(ins, ins.curr, 1, 1)

                self.commit_work(1)
            ael.abort_transaction()
	
    def do_mtm_on_rest(self):
    	try:
            ael.abort_transaction()
        except:
            pass
        ael.begin_transaction()
    	print 'last test'
    	self.trace(3, 'Already handled instruments:')
    	for i, j in self.handled_ins.items():
	    self.trace(3, '%s' % i)
	
	for ins in self.instruments.values():
	    if not self.handled_ins.has_key(ins.insid):
	    	self.work_in_progress()
		
		if ins.instype in ['Curr']:
                    self.store_mtm_price(self.base_curr, ins, 1, 1)
 
            	elif ins.instype in ['CurrSwap', 'FxSwap']:
                    # store one price per unique leg currency
    	    	    curr = {}
                    for l in ins.legs():
                    	curr[l.curr] = 1
		    for c in curr.keys():
                    	self.store_mtm_price(ins, c, 0, 1)

                elif ins.instype == 'Cap' or ins.instype == 'Floor':
                    self.store_mtm_price(ins, ins.curr, 1, 1)
                    if update_vol:
                        self.store_vol(ins, ins.curr, 1, 1)
                    
            	else:
                    self.store_mtm_price(ins, ins.curr, 1, 1)
	    	    if update_vol and \
	    	    	(ins.instype == 'Option' or ins.instype == 'Warrant'):
	    	    	self.store_vol(ins, ins.curr, 1, 1)
		
		#if ins.instype not in ('Option', 'Warrant'):
            	    #print ins.insid, time.ctime(time.time())
                
		self.commit_work(1)
        ael.abort_transaction()
  
    def add_instruments(self):
        """Add all instruments to mark to market. Use dictionaries to
        ensure that no duplicates are introduced."""
 
        self.underlyings = {}           # dict of underlyings to traded ins
        self.instruments = {}           # dict of all traded instruments
 
        self.add_underlyings_and_traded_instruments()
        self.add_currencies()
        self.add_benchmark_instruments()
 
        # Avoid underlyings in instruments
        for u in self.underlyings.values():
            if self.instruments.has_key(u.insaddr):
                del self.instruments[u.insaddr]

    def add_underlyings_and_traded_instruments(self):
        """Add traded instruments. Use database SQL directly to quickly
        retrieve a list of insaddrs."""
 
        q = '''select distinct insaddr from trade
        where status in (%d, %d, %d, %d, %d, %d)
        and archive_status = 0''' % \
                        (self.trade_status('Exchange'),
                         self.trade_status('FO Confirmed'),
                         self.trade_status('BO Confirmed'),
                         self.trade_status('BO-BO Confirmed'),
                         self.trade_status('Legally Confirmed'),
                         self.trade_status('Internal'))
            
        # test
        # q = 'select distinct insaddr from trade where trdnbr < 100'
 
        res = ael.dbsql(q)
        for i in res[0]:                # store result in dict
            insaddr = i[0]
            ins = ael.Instrument[insaddr]
            
            if ins:
#8888888 ABSA CODE
    	    	if self.B != []:
    	    	    if ins.insid in self.B:
#
                    	if ins.exp_day and ins.exp_day < self.date:
                    	    continue
                    	self.instruments[insaddr] = ins

                    	und = ins.und_insaddr
                    	if und == None or (und.exp_day and und.exp_day < self.date):
                    	    continue
                    	if und.insaddr > 0:
                    	    undaddr = und.insaddr
                    	    self.underlyings[undaddr] = ael.Instrument[undaddr]
	    	else:
		    if ins.exp_day and ins.exp_day < self.date:
                    	    continue
                    self.instruments[insaddr] = ins

                    und = ins.und_insaddr
                    if und == None or (und.exp_day and und.exp_day < self.date):
                        continue
                    if und.insaddr > 0:
                        undaddr = und.insaddr
                        self.underlyings[undaddr] = ael.Instrument[undaddr]
	    	  
                     
    def add_currencies(self):
        """Add currency instruments."""
        
        for i in ael.Instrument.select('instype="Curr"'):
            if self.B != []:
	    	if i.insid in self.B:
	    	    self.instruments[i.insaddr] = i
	    else:
	    	self.instruments[i.insaddr] = i		
 

    def add_benchmark_instruments(self):
        """Add benchmark instruments in MTM_YIELD_CURVES."""
        for i in ael.ListNode:
            if i.id == "MTM_YIELD_CURVES":
                for j in ael.ListNode.select('father_nodnbr=%d' % i.nodnbr):
                    for l in j.leafs():
                        ins = l.insaddr
                        if ins.instype == 'Zero':
                            if self.B != []:
	    	    	    	if ins.insid in self.B:
			    	    self.instruments[ins.insaddr] = ins
    	    	    	    else:
			    	self.instruments[ins.insaddr] = ins
    def commit_work(self, force=0):
        """Commit the current batch if size reached or forced commit."""
 
        self.batch_count = self.batch_count + 1
        if self.batch_count >= self.batch_size or force:
	    ael.commit_transaction()
            ael.begin_transaction()
            self.batch_count = 0
 

    def work_in_progress(self):
        """Print work in progress unless tracing is enabled."""
	
        if self.verbosity <= 1:
            self.work_count = self.work_count + 1
        
            if self.work_percent <= self.work_count/self.work_size:
                print '... %.0f%%' % (self.work_percent*100.0),
                self.work_percent = self.work_percent + 0.1
    
    def store_exception_price(self, ins, curr, res):
        self.trace(2, "Start Instr:%s Curr:%s" % (ins.insid, curr.insid))
            
    	sugg_price = res
    	    	    
        self.handled_ins[ins.insid] = sugg_price
        
        if self.bid_and_ask:
            sugg_price_bid = res
            sugg_price_ask = res
                
        		     
        q = 'insaddr=%d and day="%s" and curr=%d and ptynbr=%d' % \
            (ins.insaddr, self.date, curr.insaddr, self.market.ptynbr)
         
        price = ael.Price.read(q)
         
        if price:
            p = price.clone()           # need a copy to modify
        else:
            p = ael.Price.new()
            p.insaddr = ins.insaddr
            try:
        	p.day     = self.date
       	    except TypeError:
        	p.day     = ael.date(self.date)
            p.curr    = curr
            p.ptynbr  = self.market.ptynbr 
        	    
        #if '-1.#IND' != str(sugg_price):
        if str(sugg_price) not in ('-1.#IND', 'NaN'):
            p.settle  = sugg_price
                
        if self.bid_and_ask:
            if str(sugg_price_ask) not in ('-1.#IND', 'NaN') \
            and str(sugg_price_bid) not in ('-1.#IND', 'NaN'):
        	#not in (str(sugg_price_ask), str(sugg_price_bid)):
                p.ask = sugg_price_ask
                p.bid = sugg_price_bid
        
        self.trace(2, "Settle price: %s/%s = %.4f (%s)" % (ins.insid, curr.insid, 
            p.settle, sugg_price))
        
        self.trace(2, 'Insid %s, Expiry %s' % (ins.insid, ins.exp_day))
        if ins.exp_day == None or ins.exp_day >= ael.date_today():
            self.trace(2, 'Saved price')
            p.commit()
         
        self.commit_work()
    
    def store_mtm_price(self, ins, curr, incl, umtm):
        self.trace(2, "Start Instr:%s Curr:%s" % (ins.insid, curr.insid))
	if ins in self.ins3:
	    umtm = 0	
	#if (ins.insid != 'ZAR/C/BD//030430/10.25/R153' and ins.insid != 'ZAR/C/BD//030430/9.75/R153' and ins.insid != 'ZAR/C/BD//031106/10.00/R153' and ins.insid != 'ZAR/C/BD//031106/10.50/R153' and ins.insid != 'ZAR/C/BD//031106/9.25/R153' and ins.insid != 'ZAR/C/BD//031106/9.50/R153' and ins.insid != 'ZAR/C/BD//031106/9.75/R153' and ins.insid != 'ZAR/P/BD//031106/10.50/R153'):
	#if not ((ins.instype == 'Option' and ins.und_instype == 'Bond') or ins.instype == 'CurrSwap'):
	#if ins.instype != 'Curr' and ins.instype != 'CurrSwap' and ins.instype != 'FxSwap' and self.handled_ins.has_key(ins.insid):
	
	# for eq test 
	if ins.instype != 'Curr' and ins.instype != 'CurrSwap' and ins.instype != 'FxSwap' and self.handled_ins.has_key(ins.insid) and (not (ins.instype == 'Option' and ins.und_instype == 'EquityIndex')):
	#END eq test
	    sugg_price = self.handled_ins[ins.insid]
	else:
	    print '$$$$redoing: ', ins.insid 
            try:
	    	sugg_price = ins.mtm_price_suggest(ael.date(self.date),
	            curr.insid, incl, umtm)
	    except TypeError:
	    	sugg_price = ins.mtm_price_suggest(self.date, 
	    	    curr.insid, incl, umtm)
		 	
        self.handled_ins[ins.insid] = sugg_price
            
	if self.bid_and_ask:
            try:
	    	sugg_price_bid = ins.mtm_price_suggest(ael.date(self.date),
		    curr.insid, incl, umtm, 1)
	    except TypeError:
	    	sugg_price_bid = ins.mtm_price_suggest(self.date, 
		    curr.insid, incl, umtm, 1)
	    try:
                sugg_price_ask = ins.mtm_price_suggest(ael.date(self.date),
		    curr.insid, incl, umtm, -1)
	    except TypeError:
	    	sugg_price_ask = ins.mtm_price_suggest(self.date,
		    curr.insid, incl, umtm, -1)
 
      	q = 'insaddr=%d and day="%s" and curr=%d and ptynbr=%d' % \
            (ins.insaddr, self.date, curr.insaddr, self.market.ptynbr)
 
        price = ael.Price.read(q)
 
        if price:
            p = price.clone()           # need a copy to modify
    	else:
            p = ael.Price.new()
            p.insaddr = ins.insaddr
            try:
	    	p.day     = self.date
	    except TypeError:
	    	p.day     = ael.date(self.date)
            p.curr    = curr
            p.ptynbr  = self.market.ptynbr 
 
	    #Spread for index warrants.
    	if(ins.instype == 'Warrant' and 
	    ins.und_insaddr.instype == 'EquityIndex'):
	    sugg_price = sugg_price - self.spread
	
	    # Rounding
	if self.digits > 0:
	    try:
	    	from FMtMCustomization import custom_rounding	
	    	sugg_price = custom_rounding(ins, sugg_price, self.digits, 
	    	     force_positive_mtm_price)
	    except ImportError:
	        sugg_price = round(sugg_price, self.digits)
	
    	if force_positive_mtm_price == 1:
	    if sugg_price <= 0.0:
	    	sugg_price = 0.001
	
	    #if '-1.#IND' != str(sugg_price):
	if str(sugg_price) not in ('-1.#IND', 'NaN'):
            p.settle  = sugg_price
        
	if self.bid_and_ask:
	    if str(sugg_price_ask) not in ('-1.#IND', 'NaN') \
	    	and str(sugg_price_bid) not in ('-1.#IND', 'NaN'):
	    	#not in (str(sugg_price_ask), str(sugg_price_bid)):
            	p.ask = sugg_price_ask
                p.bid = sugg_price_bid

    	self.trace(2, "Settle price: %s/%s = %.4f (%s)" % (ins.insid, curr.insid, 
	    	p.settle, sugg_price))

    	self.trace(2, 'Insid %s, Expiry %s' % (ins.insid, ins.exp_day))
    	if ins.exp_day == None or ins.exp_day >= ael.date_today():
    	    self.trace(2, 'Saved price')
            p.commit()
 
        self.commit_work()

    def store_vol(self, ins, curr, incl, umtm):
        self.trace(2, "Start Instr:%s Curr:%s" % (ins.insid, curr.insid))
        
        if (ins.otc and ins.instype == 'Option') or ins.instype == 'Warrant':
            sugg_vol = ins.used_vol()
        else:
	    sugg_vol = ins.implied_volat(2, 'Close')
        
        if self.handled_ins.has_key(ins.insid):
            sugg_price = self.handled_ins[ins.insid]
	else:
	    try:
	        sugg_price = ins.mtm_price_suggest(ael.date(self.date),
		        curr.insid, incl, umtm)
	    except TypeError:
		sugg_price = ins.mtm_price_suggest(self.date, 
	    	        curr.insid, incl, umtm)
	
	self.handled_ins[ins.insid] = sugg_price

	if self.volmarket == None:
	    self.trace(4, 'Volatility surface does not exist, will not save'\
	    	' any value.')
	    return
	
 	qvp = 'insaddr=%d and day="%s" and curr=%d and ptynbr=%d' % \
            (ins.insaddr, self.date, curr.insaddr, self.volmarket.ptynbr)

      	volprice = ael.Price.read(qvp)

    	if volprice:
            vp = volprice.clone()           # need a copy to modify
        else:
            vp = ael.Price.new()
            vp.insaddr = ins.insaddr
	    try:
	    	vp.day     = self.date
	    except TypeError:
	    	vp.day     = ael.date(self.date)
            vp.curr    = curr
            vp.ptynbr  = self.volmarket.ptynbr

        self.trace(2, "Vol: %s/%s = %.4f" % (ins.insid, curr.insid, sugg_vol))

    	vp.settle = sugg_vol
	
	self.trace(2, 'Insid %s, Expiry %s' % (ins.insid, ins.exp_day))
    	if ins.exp_day >= ael.date_today():
    	    self.trace(2, 'Saved vol')
	    vp.commit()

    def trade_status(self, s):
        """Return integer value of trade status string."""
        return ael.enum_from_string('TradeStatus', s)
 

    def trace(self, level, s):
        """Trace."""
        if self.verbosity >= level: print s

