""" MarkToMarket:1.1.10.hotfix1 """

"""----------------------------------------------------------------------------
MODULE
    FMtMParams - Parameters for the Mark To Market procedure.

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Extracts and computes parameters for the Mark to Market procedure. Saves
    settlement prices and volatilities.

----------------------------------------------------------------------------"""
print 'Inside FMtMParams.'
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
    import re
except ImportError:
    print 'The module re was not found.'
    print
try:
    import FMtMGeneral
except ImportError:
    print 'The module FMtMGeneral was not found.'
    print
import FMtMTTGeneral
try:
    import FMtMVariables
    reload(FMtMVariables)
except AttributeError, msg:
    print 'WARNING! All FMtMVariables have to be defined. Undefined:', msg
force_positive_mtm_price = FMtMVariables.ForcePositiveMtMPrice
update_vol = FMtMVariables.UpdateVol
update_otc_vol = FMtMVariables.UpdateOTCVol
recalc_vol = FMtMVariables.RecalcVol
save_historical = FMtMVariables.SaveHistoricalValuationPrices

"""----------------------------------------------------------------------------
CLASS
    FMarkToMarket - Parameters for MarkToMarket.

INHERITS
    FMtMExecute

DESCRIPTION
    The class extracts all parameters needed to perform Mark-To-Market.

CONSTRUCTION
    market      Market      An internal market where the MtM-prices are stored
    volmarket   Market      An internal market where the volatilites are stored
    date        Date        The date on which the MtM-prices are stored
    base_curr   Currency    The currency against which the MtM prices are
                            stored for instruments of type Currency
    aliastypes  AliasTypes  alias
    spread      float       A spread which is substracted from the MtM-price
                            for index warrants
    bid_and_ask int         If 0, no bid or ask prices will be stored,
                            otherwise bid and ask prices will be stored
    digits      int         Rounding
    verbosity   int         Integer that indicate the level of information that
                            will be generated in the AEL console

----------------------------------------------------------------------------"""

class FMarkToMarket:
    """MarkToMarket"""

    def __init__(self, market, volmarket, date, base_curr, aliastypes,
                 distributors, spread, bid_and_ask, digits, verbosity, use_tt_mtm,
                 tt_fx_swap_has_2_legs, tt_reporting_currency,split_price_per_currency,
                 save_vol_prices=1,ignore_zero_prices=0):
        """Constructor. Initialize and start MarkToMarket procedure."""

        self.market = market
        self.volmarket = volmarket
        self.date = date
        self.ael_date = ael.date(str(date))
        self.base_curr = ael.Instrument[base_curr]
        self.aliastypes = aliastypes
        self.distributors = distributors
        self.spread = spread
        self.bid_and_ask = bid_and_ask
        self.split_price_per_currency = split_price_per_currency
        self.use_tt_mtm = use_tt_mtm
        self.tt_fx_swap_has_2_legs = tt_fx_swap_has_2_legs
        self.tt_reporting_currency = tt_reporting_currency
        self.digits = digits            # Added rounding
        self.batch_size = 10            # size(trade) ~= 3.3*size(price) and aggregation commits 400 trades.
        self.batch_count = 0
        self.assume_new_price = 1       # Try insert
        self.verbosity = verbosity
        self.save_vol_prices = save_vol_prices
        if FMtMVariables.Test_Underlyings:
            self.add_instruments_test()
        else:
            self.add_instruments()
        self.handled_ins   = {} # insaddr : None
        self.calc_mtm_price= {}     # insaddr : price, vola benchmark instruments.
        self.ins1 = {}
        self.ins4 = {}
        self.ins2 = []
        self.ins3 = []
        self.price_batch = []
        self.n_found_price=0
        self.no_valid_prices={} # insaddr : 1|0, Used to exclude derivatives with no price!
                                # Marks only invalid ins, opposite not always true
        
	self.ignore_zero_prices=ignore_zero_prices

        if not FMtMVariables.Test_Underlyings and aliastypes != None:
            (self.ins1, alias_ins) = FMtMGeneral.find_alias_ins(aliastypes, self.ael_date, FMtMVariables.UpdateVolInsTypes)
            # self.ins1 is a dictionary with key = underlying,
            # and items for each key = options on the underlying
            # alias_ins is the number of options in the dictionary (an integer)

        if not FMtMVariables.Test_Underlyings and distributors != None:
            (self.ins4, dist_ins) = \
                FMtMGeneral.find_distributors_ins(distributors, self.ael_date, FMtMVariables.UpdateVolInsTypes)
            # self.ins4 is a list of instruments (ael entities)
            # dist_ins is the number of instruments in the list (an integer)



        if FMtMVariables.Test_Underlyings:
            self.ins2=[]
            self.ins3=[]
            #Note: It is assumed that the underlying has trades or something
            for (und_insaddr, und) in self.underlyings.items():
                for der in ael.Instrument.select('und_insaddr=%d' % und_insaddr):
                    if self.is_expired(der): continue

                    if der.paytype == 'Future' or not FMtMVariables.CheckIfTrades or der.trades():
                        self.instruments[der.insaddr] = der

                    if der.instype in ['Option', 'Warrant']:
                        if und.instype=='Stock':
                            self.ins2.append(der)
                        elif und.instype=='EquityIndex':
                            self.ins3.append(der)
                        if der.instype == 'Option':
                            options=self.ins1.get(und, [])
                            options.append(der)
                            self.ins1[und]=options
                    elif der.instype == 'Future/Forward':
                        self.instruments[der.insaddr]=der
            alias_ins=0
            if aliastypes:
                for (und, options) in self.ins1.items():
                    alias_ins = alias_ins + len(options) + 1
        else:
            self.ins2 = FMtMGeneral.find_opt_and_warrants_on_stock(self.ael_date, FMtMVariables.ExcludeMtMInstypes)
            self.ins3 = FMtMGeneral.find_opt_and_warrants_on_index(self.ael_date, FMtMVariables.ExcludeMtMInstypes)

        ins_dict = {}
        for i in self.underlyings.values():
            ins_dict[i.insid] = 1
        for (und, olist) in self.ins1.items(): #underlying, optionlist
            for i in olist:
                ins_dict[i.insid] = 1
                if not self.has_valid_prices(i): # check if valid prices exists
                    self.no_valid_prices[i]=1
        for (und, olist) in self.ins4.items(): #underlying, optionlist
            for i in olist:
                ins_dict[i.insid] = 1
                if not self.has_valid_prices(i): # check if valid prices exists
                    self.no_valid_prices[i]=1

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
            if not self.handled_ins.has_key(ins):
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
                if not self.handled_ins.has_key(ins):
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

        for (und, olist) in self.ins1.items(): #instruments.items():
            for ins in olist:
                self.work_in_progress()
                self.store_vol(ins, ins.curr, 1, 1)
                self.commit_work()
        self.commit_work(1)
        ael.abort_transaction()

    def do_mtm_for_distributors(self):
        """Save MtM-prices for all instruments that have distributor"""
        try:
            ael.abort_transaction()
        except:
            pass
        ael.begin_transaction()

        for (und, olist) in self.ins4.items(): #ins in instruments:
            for ins in olist:
                if not self.handled_ins.has_key(ins):
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

        for (und, olist) in self.ins4.items():
            for ins in olist:
                self.work_in_progress()
                self.store_vol(ins, ins.curr, 1, 1)
                self.commit_work()
        self.commit_work(1)
        ael.abort_transaction()

    def do_mtm_opt_and_warrants_on_stock(self):
        try:
            ael.abort_transaction()
        except:
            pass
        ael.begin_transaction()

        for ins in self.ins2: #instruments:
            if not self.handled_ins.has_key(ins):
                self.work_in_progress()
                self.store_mtm_price(ins, ins.curr, 1, 1)
                if update_otc_vol and \
                    (ins.instype == 'Option' or ins.instype == 'Warrant'):
                    self.store_vol(ins, ins.curr, 1, 1)
                    self.commit_work()
        self.commit_work(1)
        ael.abort_transaction()

    def do_mtm_opt_and_warrants_on_index(self):
        #instruments = FMtMGeneral.find_opt_and_warrants_on_index()
        try:
            ael.abort_transaction()
        except:
            pass
        ael.begin_transaction()

        for ins in self.ins3: #instruments:
            if not self.handled_ins.has_key(ins):
                self.work_in_progress()
                self.store_mtm_price(ins, ins.curr, 1, 1)

                if update_otc_vol and \
                    (ins.instype == 'Option' or ins.instype == 'Warrant'):
                    self.store_vol(ins, ins.curr, 1, 1)
                    self.commit_work()  
        self.commit_work(1)
        ael.abort_transaction()

    def do_mtm_on_rest(self):
        try:
            ael.abort_transaction()
        except:
            pass
        ael.begin_transaction()

        for ins in self.instruments.values():
            if not self.handled_ins.has_key(ins):
                self.work_in_progress()

                if ins.instype in ['Curr']:
                    self.store_mtm_price(self.base_curr, ins, 1, 1)

		elif self.use_tt_mtm and ins.instype in ['FxSwap'] and ins.extern_id2[:2] == 'TT':
                    self.store_mtm_price(ins, ins.curr, 1, 1)

                elif self.split_price_per_currency and ins.instype in ['CurrSwap', 'FxSwap']:
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
                        self.commit_work()
                else:
                    self.store_mtm_price(ins, ins.curr, 1, 1)
                    if update_vol and \
                        (ins.instype == 'Option' or ins.instype == 'Warrant'):
                        self.store_vol(ins, ins.curr, 1, 1)
                        self.commit_work()
                #if ins.instype not in ('Option', 'Warrant'):
                    #print ins.insid, time.ctime(time.time())

        self.commit_work(1)
        ael.abort_transaction()

    def add_instruments_test(self):
        self.underlyings = {}           # dict of underlyings to traded ins
        self.instruments = {}           # dict of all traded instruments

        self.add_currencies()
        self.add_benchmark_instruments()
        for undid in FMtMVariables.Test_Underlyings:
            und=ael.Instrument[undid]
            if not und: raise ('NO such instrument: %s' % undid)
            self.underlyings[und.insaddr]=und

    def add_instruments(self):
        """Add all instruments to mark to market. Use dictionaries to
        ensure that no duplicates are introduced."""

        self.underlyings = {}           # dict of underlyings to traded ins
        self.instruments = {}           # dict of all traded instruments

        self.add_underlyings_and_traded_instruments()
        self.add_currencies()
        self.add_benchmark_instruments()
        if save_historical:
            self.add_param_benchmark_instruments()

        # Avoid underlyings in instruments
        for u in self.underlyings.values():
            if self.instruments.has_key(u.insaddr):
                del self.instruments[u.insaddr]

        
        # Run all instruments through the FMtMCustomization.check_instrument() hook
        
        try:
            from FMtMCustomization import check_instrument
        except:
            check_instrument = 0

        if check_instrument:
            
            tmp_instruments = []
            tmp_underlyings = []

            for ent in self.instruments.values():
                if not check_instrument(ent):
                    tmp_instruments.append(ent.insaddr)

            for ent in self.underlyings.values():
                if not check_instrument(ent):
                    tmp_underlyings.append(ent.insaddr)

            for ia in tmp_instruments:
                del self.instruments[ia]

            for ia in tmp_underlyings:
                del self.underlyings[ia]
        

    def add_underlyings_and_traded_instruments(self):
        """Add traded instruments or instruments with paytype Future. 
        In larger database quering  the underlying database (trade)
        is to slow so AEL is used"""

        tmp={} # ael_entity instrument : None
        if FMtMVariables.CheckIfTrades:
            for t in ael.Trade.select():
                if t.insaddr and not t.insaddr.instype in FMtMVariables.ExcludeMtMInstypes:
                    tmp[t.insaddr] = None
                    
            # Make sure all instruments with paytype Future is included
            for i in ael.Instrument.select():
                if i.paytype == 'Future':
                    tmp[i] = None
        else:
            for i in ael.Instrument.select():
                if not i.generic or not re.search("default", i.insid, re.I) \
                    or not i.instype in FMtMVariables.ExcludeMtMInstypes:
                    tmp[i] = None
            ael.Price.select() # Load all prices 
                
        for i in tmp.keys():                # store result in dict
            insaddr = i.insaddr
            ins = i

            if ins:
                ###if ins.exp_day and ins.exp_day < self.date:
                if ins.exp_day and self.is_expired(ins):
                    continue
                self.instruments[insaddr] = ins

                und = ins.und_insaddr
                ###if und == None or (und.exp_day and und.exp_day < self.date):
                if und == None or (und.exp_day and self.is_expired(und)):
                    continue
                if und.insaddr > 0 and und.instype != 'Curr':
                    undaddr = und.insaddr
                    self.underlyings[undaddr] = ael.Instrument[undaddr]
                    if save_historical:
                        self.add_underlying_hierarchy(und)

    def add_currencies(self):
        """Add currency instruments."""

        for i in ael.Instrument.select('instype="Curr"'):
            self.instruments[i.insaddr] = i


    def add_benchmark_instruments(self):
        """Add benchmark instruments in MTM_YIELD_CURVES."""
        for i in ael.ListNode:
            if i.id == "MTM_YIELD_CURVES":
                for j in ael.ListNode.select('father_nodnbr=%d' % i.nodnbr):
                    for l in j.leafs():
                        ins = l.insaddr
                        if ins.instype == 'Zero':
                            self.instruments[ins.insaddr] = ins

    def add_param_benchmark_instruments(self):
        """Add all yc and vol benchmark instruments."""
        try:
            import FVPSVariables, FVPSYieldCurve, FVPSVolatility
        except:
            self.trace(1, "One or more of FVPSVariables and FVPSYieldCurve")
            self.trace(1, "were not found. These AEL modules are needed to perform")
            self.trace(1, "MtM for all benchmark instruments")
            return

        ycs = FVPSYieldCurve.GetDefinedSet()
        vols = FVPSVolatility.GetDefinedSet()

        ins_list = []

        for yc in ycs:
            if yc.yield_curve_type == 'Instrument Spread':
                iss = yc.instrument_spreads()
                for is_ in iss:
                    if is_.instrument1 != None:
                        ins_list.append(is_.instrument1)
                    if is_.instrument2 != None:
                        ins_list.append(is_.instrument2)

            if yc.yield_curve_type in ('Benchmark', 'Spread'):
                bms = yc.benchmarks()
                for bm in bms:
                    if bm.instrument != None:
                        ins_list.append(bm.instrument)

        for vol in vols:
            if vol.ref_insaddr != None:
                ins_list.append(vol.ref_insaddr)

            vps = vol.points()
            for vp in vps:
                if vp.insaddr != None:
                    ins_list.append(vp.insaddr)

            vbbs = vol.beta_benchmarks()
            for vbb in vbbs:
                if vbb.insaddr != None:
                    ins_list.append(vbb.insaddr)

        for i in ins_list:
            if i.insaddr > 0:
                self.instruments[i.insaddr] = i
                if save_historical:
                    self.add_underlying_hierarchy(i)


    def add_underlying_hierarchy(self, ins):
        """Add all underlyings in a traded instrument."""

        und = ins.und_insaddr
        del_links = ins.deliverable_links()
        comb_links = ins.combination_links()
        legs = ins.legs()

        if und != None and (not und.exp_day or not self.is_expired(und)):
            if und.insaddr > 0:
                self.underlyings[und.insaddr] = und
                self.add_underlying_hierarchy(und)

        if del_links != None and len(del_links) > 0:
            for dl in del_links:
                mbr = dl.member_insaddr
                if mbr != None and (not mbr.exp_day or not self.is_expired(mbr)):
                    if mbr.insaddr > 0:
                        self.underlyings[mbr.insaddr] = mbr
                        self.add_underlying_hierarchy(mbr)

        if comb_links != None and len(del_links) > 0:
            for cl in comb_links:
                mbr = cl.member_insaddr
                if mbr != None and (not mbr.exp_day or not self.is_expired(mbr)):
                    if mbr.insaddr > 0:
                        self.underlyings[mbr.insaddr] = mbr
                        self.add_underlying_hierarchy(mbr)

        if legs != None and len(legs) > 0:
            for l in legs:
                candidates = [l.float_rate,
                    l.float_rate2,
                    l.index_ref,
                    l.credit_ref]
                for i in candidates:
                    if i != None and (not i.exp_day or not self.is_expired(i)):
                        if i.insaddr > 0:
                            self.underlyings[i.insaddr] = i
                            self.add_underlying_hierarchy(i)



    def commit_work(self, force=0):
        """Commit the current batch if size reached or forced commit."""

        self.batch_count = self.batch_count + 1
        if self.batch_count >= self.batch_size or force:
            tf_start_secs = time.time()
        
            if len(self.price_batch)>0:
                FMtMGeneral.log(2, 'Commit, mode=%d, n=%d' % (self.assume_new_price, len(self.price_batch)))
                old_mode=self.assume_new_price               
                found=0 
                try:
         	    for p in self.price_batch:
                        p.commit()
                    ael.commit_transaction()
                except:
                    ael.log('INFO: any duplicate logging is normal!') 
                    ael.abort_transaction()
                    ael.begin_transaction()
                    self.n_found_price=0
                    for p in self.price_batch:
                       q = 'insaddr=%d and day="%s" and curr=%d and ptynbr=%d' % \
                               (p.insaddr.insaddr, p.day, p.curr.insaddr, p.ptynbr.ptynbr)
                       price = ael.Price.read(q)
                       if price:
                          found=1
                          new_p = price.clone()           # need a copy to modify
                          new_p.ask = p.ask
                          new_p.bid = p.bid
                          new_p.last = p.last
                          new_p.settle = p.settle
                          new_p.commit()
                       else:
                          new_p = ael.Price.new()
                          new_p.insaddr = p.insaddr
                          new_p.day = p.day
                          new_p.ptynbr = p.ptynbr
                          new_p.curr = p.curr
                          new_p.bits = p.bits
                          new_p.ask = p.ask
                          new_p.bid = p.bid
                          new_p.last = p.last
                          new_p.settle = p.settle
                          new_p.commit()
		    try:
                    	ael.commit_transaction()
                    except:
		    	print "Error in commiting price batch-possible duplacate entry."
		if self.n_found_price == 0 and not found:
                    self.assume_new_price=1
                else:
                    self.assume_new_price=0
                if old_mode != self.assume_new_price:
		    FMtMGeneral.log(2, "==> Switching price batch mode from %d to %d" % (old_mode, self.assume_new_price))
                self.n_found_price=0
                self.price_batch = []     
            else:
                ael.commit_transaction()
            ael.begin_transaction()
            tf_end_secs = time.time()
            self.batch_count = 0
            self.trace(3, "Commit work in %s" % (str(tf_end_secs - tf_start_secs)))

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

        self.handled_ins[ins] = sugg_price

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
        if save_historical and ins.generic:
            self.trace(2, 'Insid %s, Generic' % ins.insid)
        else:
            self.trace(2, 'Insid %s, Expiry %s' % (ins.insid, ins.exp_day))
        if ins.exp_day == None or not self.is_expired(ins):
            self.trace(2, 'Saved price')
            p.commit()

        self.commit_work()

    def store_mtm_price(self, ins, curr, incl, umtm):
        tf_start_secs = time.time()
        self.trace(2, "Start Instr:%s Curr:%s" % (ins.insid, curr.insid))
        if ins.exp_day and self.is_expired(ins):
            return

        if 0 and self.no_valid_prices.has_key(ins):
              self.handled_ins[ins] = sugg_price= 0.0
        elif self.handled_ins.has_key(ins) and not ins.instype in ['Curr', 'CurrSwap', 'FxSwap']:
            sugg_price = self.handled_ins[ins]
        elif self.calc_mtm_price.has_key(ins):
            sugg_price = self.calc_mtm_price[ins]
        else:
            if self.use_tt_mtm == 1 and ins.instype == 'Curr':
                sugg_price = FMtMTTGeneral.get_spot_rate(ins.insid, curr.insid, 0)
            elif self.use_tt_mtm == 1 and ins.instype == 'FxSwap' and ins.extern_id2[:2] == 'TT':
                sugg_price = FMtMTTGeneral.get_fxswap_price(ins, self.tt_fx_swap_has_2_legs, self.tt_reporting_currency)
            else:
                #sugg_price = ins.mtm_price_suggest(self.ael_date,curr.insid, incl, umtm)
                sugg_price = FMtMGeneral.suggest_price(ins, self.ael_date, curr.insid, incl, umtm)

        self.handled_ins[ins] = sugg_price

        if sugg_price == 0.0 and self.ignore_zero_prices:
            self.trace(2, 'Ignore price eq 0.0')
	    return 
        if self.bid_and_ask:
            if self.use_tt_mtm == 1 and ins.instype == 'Curr':
                sugg_price_bid = FMtMTTGeneral.get_spot_rate(ins.insid, curr.insid, 1)
                sugg_price_ask = FMtMTTGeneral.get_spot_rate(ins.insid, curr.insid, -1)
            elif self.use_tt_mtm == 1 and ins.instype == 'FxSwap':
                # Since the bid and ask flag doesn't affect instrument with MtM From Feed 
                # untoggled, we will get the same result as theor price for midprice.
                # The sugg_price is here calculated from MtM values in Treasury Trader.
                sugg_price_bid = sugg_price
                sugg_price_ask = sugg_price
            else:
                #sugg_price_bid = ins.mtm_price_suggest(self.ael_date,curr.insid, incl, umtm, 1)
                #sugg_price_ask = ins.mtm_price_suggest(self.ael_date,curr.insid, incl, umtm, -1)
                if 0 and self.no_valid_prices.has_key(ins):
                    sugg_price_bid = sugg_price_ask = 0.0
                else:   
                    sugg_price_bid = FMtMGeneral.suggest_price(ins, self.ael_date, curr.insid, incl, umtm, 1)
                    sugg_price_ask = FMtMGeneral.suggest_price(ins, self.ael_date, curr.insid, incl, umtm, -1)

        p=None
	if not self.assume_new_price:
            q = 'insaddr=%d and day="%s" and curr=%d and ptynbr=%d' % \
                (ins.insaddr, self.date, curr.insaddr, self.market.ptynbr)
            p= ael.Price.read(q)
        if not p:
            p = ael.Price.new()
            p.insaddr = ins.insaddr
            p.day     = self.ael_date
            p.curr    = curr
            p.ptynbr  = self.market.ptynbr
        else:
            self.n_found_price=self.n_found_price+1
            p=p.clone()       
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
        tf_end_secs = time.time()
        if ins.exp_day == None or not self.is_expired(ins):
            self.trace(2, 'Saved price')
            self.trace(3, "Saved price, %s" % (str(tf_end_secs - tf_start_secs)))
            self.price_batch.append(p)
#            p.commit()
        else:
            self.trace(3, "Price not saved, %s" % (str(tf_end_secs - tf_start_secs)))

        self.commit_work()

    
            
    def store_vol(self, ins, curr, incl, umtm):
        if not self.save_vol_prices or self.is_expired(ins): 
            return
        
        tf_start_secs = time.time()
        self.trace(2, "Start Instr:%s Curr:%s" % (ins.insid, curr.insid))

        if ins.otc and ins.instype in ['Option', 'Warrant']:
            sugg_vol = FMtMGeneral.calculate_vol(ins)/100.0
        else:
            if self.calc_mtm_price.has_key(ins):
                quote = self.calc_mtm_price[ins]
            else:
                quote = FMtMGeneral.suggest_price(ins, self.ael_date, curr.insid, incl, umtm)
                self.calc_mtm_price[ins] = quote
            sugg_vol = FMtMGeneral.calculate_vol(ins, quote)/100.0
        
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

        vp.settle = sugg_vol

        if self.verbosity >= 2:
            self.trace(2, "Vol: %s/%s = %.4f" % (ins.insid, curr.insid, sugg_vol))
            self.trace(2, 'Insid %s, Expiry %s' % (ins.insid, ins.exp_day))
            tf_end_secs = time.time()
            self.trace(3, "Saved vol, %s" % (str(tf_end_secs - tf_start_secs)))
        self.price_batch.append(vp)
        #vp.commit()


    def trade_status(self, s):
        """Return integer value of trade status string."""
        return ael.enum_from_string('TradeStatus', s)


    def trace(self, level, s):
        """Trace."""
        if self.verbosity >= level: print s

    def is_expired(self, ins):
        """is_expired(ins)
        Returns true (1) if the instrument has expired, false (0) otherwise"""
        if save_historical and ins.generic:
            return 0
        return FMtMGeneral.is_ins_expired(ins, self.ael_date)

    def has_valid_prices(self, ins):
        """ Perhaps improve check below """
	if not ins.mtm_from_feed:
	    return 1
        for p in ins.prices():
            if p.settle > 0.0 or p.last > 0.0 or p.ask > 0.0 or p.bid > 0.0:
                return 1
        return 0


