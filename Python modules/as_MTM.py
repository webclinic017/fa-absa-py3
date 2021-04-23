""" MarkToMarket:1.1.7 """

"""----------------------------------------------------------------------------
MODULE
    FMtMExecute - Module which executes the Mark-to-Market.

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module executes the Mark-to-Market procedure.

DATA-PREP
    All variables have to be set in this module. Two internal markets have
    to be created. One on which the MtM-prices are stored and one on which
    the implied volatilites are stored.
    Also a context where the mapping between volatility surfaces and
    instruments are done need to be defined
    
    The variables that should be set are:
    market  	String	    An internal market where the MtM-prices are stored
    volmarket	String	    An internal market where the implied volatilites
                            are stored
    date    	Date	    The date on which the MtM-prices are stored
    basecurr	Currency    The currency against which the MtM prices are 
    	    	    	    stored for instruments of type Currency
    aliastypes	String	    A list of Alias Types. All instruments that have 
                            these alias types set will be selected and used in
                            the functions do_mtm_for_alias() and
                            do_save_aliastype_vols().
                            do_mtm_for_alias() will calculate and store
                            MtM-prices for the selected instruments.
                            do_save_aliastype_vols() will calculate the implied
                            volatilities for the selected instruments.
                            Thereafter these volatilites will be stored in the
                            historical price table with the volmarket set as
                            market.
    yieldcurves String	    A list of yieldcurves. These yieldcurves will
                            automatically be recalculated with the help of the
                            update_yc()-function found in the
                            FMtMGeneral-module.
    spread  	float	    A price spread which is substracted from the
                            MtM-price for index warrants
    bid_and_ask	int 	    If 0, no bid or ask prices will be stored, 
    	    	    	    otherwise bid and ask prices will be stored
    digits  	int 	    Rounding
    volsuffix	String	    volsuffix
    context 	String	    Context
    verbosity	int 	    Integer that indicate the level of information that
    	    	    	    will be generated in the AEL console

    There are a number of functions that are called from this module:
    do_mtm_underlying()     Calculates and stores MtM-prices for all underlying
                            instruments.
    do_mtm_for_alias()      Calculates and stores MtM-prices for the
                            instruments that have certain alias type set.
    update_yc(yieldcurves)  Recalculate all yieldcurves specified.
    do_save_aliastype_vols() Calculates the implied volatilities for the
                            instruments that have a certain alias type set.
                            The volatilites are stored in the historical
                            price table with the volmarket set as market.
    create_vols_and_ctx(volsuffix, mtm.aliastypes, context) Creates volatility-
    	    	    	    surfaces and contexts.
    update_vols(volsuffix, mtm.aliastypes, context) Updates volatilitysurfaces.
    do_mtm_opt_and_warrants_on_stock() Calculates and stores MtM-prices for
                            all options and warrants on stocks.  
    do_mtm_opt_and_warrants_on_index() Calculates and stores MtM-prices for
                            all options and warrants on indices.
    do_mtm_on_rest()        Calculates and stores MtM-prices for all other
                            instruments.
    It is possible to run only parts of the MtM-procedure. If so just comment
    the parts that are not to be used.
        
REFERENCES
    See modules FMtMParams and FMtMGeneral.

----------------------------------------------------------------------------"""
import sys
class ExitScriptError:
    def __init__(self, msg):
    	self.msg = msg
    def __str__(self):
        return str(self.msg)
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
if __name__ == "__main__":
    try:
    	from os import environ
    except ImportError:
    	print 'The module os was not found.'
    	print
try:
    import FMtMGeneral
    reload(FMtMGeneral)
except ImportError:
    print 'The module FMtMGeneral was not found.'
    print
try:
    import FMtMParamsFilter
    reload(FMtMParamsFilter)
except ImportError:
    print 'The module FMtMParams was not found.'
    print
#try:
#    import FDivYield
#    reload(FDivYield)
#except ImportError:
#    print 'The module FDivYield was not found.'
#    print
try:
    import FMtMVariables
    reload(FMtMVariables)
except AttributeError, msg:
    print 'WARNING! All FMtMVariables have to be defined. Undefined:', msg

calc_exceptions = FMtMVariables.CalcMtMPriceForExceptions
if calc_exceptions:
    exception_list = FMtMVariables.ExceptionList

try:
    # Compulsory variables:
    save_prices = FMtMVariables.Save_MtM_Prices
    save_theor_prices = FMtMVariables.Save_Theor_Prices
    save_seq_prices = FMtMVariables.SaveSEQPrices
    market	    = FMtMVariables.Market
    calc_imp_div_yield = FMtMVariables.CalcImpDivYield
    update_yc   = FMtMVariables.UpdateYC
    recalc_vol = FMtMVariables.RecalcVol
    update_vol = FMtMVariables.UpdateVol
    update_otc_vol = FMtMVariables.UpdateOTCVol
    spread	    = float(FMtMVariables.Spread)
    bid_and_ask  = FMtMVariables.SaveBidAndAsk

    sendmail    = FMtMVariables.Sendmail
    if sendmail:
	rec     = FMtMVariables.Receiver
    verbosity   = int(FMtMVariables.Verb)

    try:
	digits	= int(FMtMVariables.Rounding)
    except:
	digits  	= -1

    try:
	date    	= None
	date    	= FMtMVariables.Date # Date is set to today later if not here.
    except: pass

    try:
	basecurr    = FMtMVariables.BaseCurr
    except:
	basecurr	= None # to be set later to acc_curr.

    if calc_imp_div_yield:
	underlyings = FMtMVariables.Underlyings
    else:
    	underlyings = None
    if update_yc:
	yieldcurves = FMtMVariables.YieldCurves
    else:
	yieldcurves = None

    if update_vol or update_otc_vol:
        volmarket   = FMtMVariables.VolMarket
    else:
        volmarket     = None

    if update_vol:
	base    	= FMtMVariables.Base
	volsuffix   = FMtMVariables.VolSuffix
	context     = FMtMVariables.Context
    else:
	volsuffix	= None
	context 	= None

    if recalc_vol:
        volsurfaces     = FMtMVariables.VolSurfaces
    else:
        volsurfaces     = None
	
    if update_vol or update_otc_vol or calc_imp_div_yield:
	try:
    	    aliastypes  = FMtMVariables.AliasTypes
	except AttributeError:
    	    aliastypes = None
	try:
    	    distributors = FMtMVariables.Distributors
	except AttributeError:
    	    distributors = None
    else:
    	aliastypes	= None
	distributors	= None
    
except AttributeError, msg:
    print 'WARNING! All FMtMVariables have to be defined. Undefined:', msg

"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
try:
    if __name__ == "__main__":
    	import sys, getopt
    
    	try:
	    opts, args = getopt.getopt(sys.argv[1:], 'u:p:m:h:')
	
	    if len(opts) < 2:
            	raise getopt.error, ''
    	except getopt.error, msg:
            print msg
            m = '''Usage: ael <config name> FMtMExecute.py -u username
	        -p password [-m MtMmarket]'''
	    print m
            sys.exit(2)

        for o, a in opts:
            if o == '-a': ads_address = a
            if o == '-u': atlas_user = a
            if o == '-p': atlas_passw = a
            if o == '-m': market = a
            if o == '-h': help_text()

        if not date or date == 'Today':
            day = str(ael.date_today())
    	elif date == 'Yesterday':
    	    day = str(ael.date_today().add_days(-1))
        else:
            day = str(ael.date(date))

    	FMtMGeneral.log(1, 'MtM date:%s' % day)

     	ael.date_set_today(ael.date(day))

    	ael.connect(environ['ADS_ADDRESS'], str(atlas_user), str(atlas_passw))
    
    	market = ael.Party[market]
    	if market == None or market.type != 'MtM Market':
            print 'Market must be a party of type MtM Market.'
            sys.exit(2)

	if update_vol:
	    if aliastypes != None:
	        FMtMGeneral.log(2, '\n0 Create Vols and Context\n')
	    	FMtMGeneral.create_vols_and_ctx(mtm, volsuffix,
	    	    mtm.aliastypes, context)
	    		
	    if distributors != None:
	    	FMtMGeneral.log(2, '\n0 Create Vols and Context\n')
	    	FMtMGeneral.create_vols_and_ctx(mtm, volsuffix,
	    	    mtm.distributors, context)
        
        if save_seq_prices:
            try:
	        import FEqAverage
	        if hasattr(FEqAverage, 'UdateAveragePrice'):
	            FMtMGeneral.log(2, '\n UpdateAveragePrice \n')
		    FEqAverage.UpdateAveragePrice()
	    except ImportError:
    	    	pass
            try:
	        import FCliquetParams
	        if hasattr(FCliquetParams, 'UpdateCliquetPrice'):
		    FMtMGeneral.log(2, '\n UpdateCliquetPrice \n')
		    FCliquetParams.UpdateCliquetPrice()
	    except ImportError:
    	    	pass
            try:
	        import FEqLadder
	        if hasattr(FEqLadder, 'UpdateLadderRungs'):
	            FMtMGeneral.log(2, '\n UpdateLadderRungs \n')
		    FEqLadder.UpdateLadderRungs()
	    except ImportError:
    	    	pass
            try:
	        import FEqBarrier
	        if hasattr(FEqBarrier, 'UpdateBarrierStatus'):
	            FMtMGeneral.log(2, '\n UpdateBarrierStatus \n')
		    FEqBarrier.UpdateBarrierStatus()
	    except ImportError:
    	    	pass
            try:
	        import FEqDoubleBarrier
	        if hasattr(FEqDoubleBarrier, 'UpdateDoubleBarrierStatus'):
		    FMtMGeneral.log(2, '\n UpdateDoubleBarrierStatus \n')
		    FEqDoubleBarrier.UpdateDoubleBarrierStatus()
	    except ImportError:
    	    	pass
   
        if update_vol or update_otc_vol:
    	    volmarket = ael.Party[volmarket]
    	    if volmarket == None or volmarket.type != 'MtM Market':
	    	print 'VolMarket must be a party of type MtM Market, \
	    	    if volatilities should be saved.'
                sys.exit(2)
    
	if basecurr == None:
	    try:
	        basecurr = ael.used_acc_curr()
	    except Exception:
	    	print "No accounting currency selected, please select "
    	    	print "a currency in Accounting Parameters."
    	    	sys.exit(2)
    	else:
	    if ael.Instrument[basecurr] == None:
	        print "The variable BaseCurr, '%s', is not a currency. Please " % basecurr
	       	print "select a currency in FMtMVariables or use the currency "
		print "in the Accounting Parameters."
		sys.exit(2)
	
    	mtm = FMtMParams.FMarkToMarket(market, volmarket, 
    	    ael.date_from_string(day), basecurr, 
    	    aliastypes, distributors, spread, bid_and_ask, digits, verbosity)

        if save_prices and calc_exceptions:
    	    FMtMGeneral.log(2, '\n1 MtM for Exceptions\n')
    	    try:
    	    	from FMtMCustomization import custom_valuation
    	    	res = custom_valuation(exception_list)
    	    	for r in res:
	            ins = r[0]
	            value = r[1]
    	            mtm.store_exception_price(ins, ins.curr, value)
    	    except ImportError:
    	    	pass
    	        
    	if update_yc:
            FMtMGeneral.log(2, '\n2 Update Yield Curves\n')
       	    FMtMGeneral.update_yc(yieldcurves)
    
    	if calc_imp_div_yield:
       	    FMtMGeneral.log(2, '\n3 Calculate Div Yield\n')
    	    for i in underlyings:
    	        x = ael.Instrument[i]
    	        #FDivYield.update_yc(x, 'All')
    	        if aliastypes != None:
    	    	    FDivYield.update_yc(x, 'All', mtm.ins1.items())
    	        if distributors != None:
    		        FDivYield.update_yc(x, 'All', mtm.ins4.items())
    	        if None in (aliastypes, distributors):
    		        FDivYield.update_yc(x, 'All', None)
        
        if recalc_vol:
	    FMtMGeneral.log(2, '\n4 Recalculate Volatility Surfaces\n')
            FMtMGeneral.recalc_vol_surfaces(volsurfaces)
        
    	if update_vol:
            if aliastypes != None:
            	FMtMGeneral.log(2, '\n5 Update Vols\n')
    	    	FMtMGeneral.update_vols(mtm, volsuffix,
    	    	    mtm.aliastypes, context)
    		
            if distributors != None:
    	        FMtMGeneral.log(2, '\n5 Update Vols\n')
    	        FMtMGeneral.update_vols(mtm, volsuffix,
	    	    mtm.distributors, context)
    
        if update_vol:
            if aliastypes != None:
                FMtMGeneral.log(2, '\n8 Save AliasType Vols\n')
                mtm.do_save_aliastype_vols()
         
            if distributors != None:
    	        FMtMGeneral.log(2, '\n8 Save Distributor Vols\n')
    	        mtm.do_save_distributors_vols()
       
        if save_prices:
    	    FMtMGeneral.log(2, '\n9 MtM for Underlying\n') 
    	    mtm.do_mtm_underlying()
    
    	    if aliastypes != None:
	        FMtMGeneral.log(2, '\n10 MtM for Alias\n')
    	        mtm.do_mtm_for_alias()
    
    	    if distributors != None:
	        FMtMGeneral.log(2, '\n10 MtM for Distributors\n')
    	        mtm.do_mtm_for_distributors()

    	    FMtMGeneral.log(2, '\n11 MtM on Rest\n')    
    	    mtm.do_mtm_on_rest()
    	
	import SAGEN_CopyMTM_TO_SPOT
    	SAGEN_CopyMTM_TO_SPOT.copy_mtm_to_spot(['ZAR/PIC_BASKET', 'ZAR/OPTI', 'ZAR/OPTI_NEW', 'ZAR/PIC2', 'ZAR/PIC3', 'ZAR/CAD'])

    	if save_theor_prices:
    	    FMtMGeneral.log(2, '\n6 MtM/Vol for Options and Warrants on Stock\n')
    	    mtm.do_mtm_opt_and_warrants_on_stock()
    
    	    FMtMGeneral.log(2, '\n7 MtM/Vol for options and Warrants on Index\n')
    	    mtm.do_mtm_opt_and_warrants_on_index()


        FMtMGeneral.log(1, "\nMarkToMarket finished %s" % \
    	    str(time.ctime(time.time())))
    	FMtMGeneral.log(1, "MarkToMarket has been successful!")
    	subj = 'MarkToMarket'
    	msg = 'has been successful!'
    	if sendmail:
    	    ael.sendmail(rec, subj, msg)
    
    	ael.disconnect()
    else:
    	mkt_list = FMtMGeneral.mtm_markets()
    	    
    	market = ael.Party[market]
    	if market == None or market.type != 'MtM Market':
            raise 'Market must be a party of type MtM Market.'

    	if update_vol or update_otc_vol:
    	    volmarket = ael.Party[volmarket]
    	    if volmarket == None or volmarket.type != 'MtM Market':
                raise 'VolMarket must be a party of type MtM Market, \
	    	    if volatilities should be saved.'

	if basecurr == None:
	    try:
	        basecurr = ael.used_acc_curr()
	    except Exception:
	    	raise ExitScriptError("No accounting currency selected, please select "\
    	    		"a currency in Accounting Parameters.")
    	else:
	    if ael.Instrument[basecurr] == None:
	        raise ExitScriptError("The variable BaseCurr, '%s', is not a currency. Please select "\
	       	        "a currency in FMtMVariables or use the currency in the "\
			"Accounting Parameters." % basecurr)

        dates = ['Today', 'Yesterday']
        if date:
            display_day = date
        else:
            display_day = 'Today'

    	def displayMkt():
    	    ml = []
    	    for m in ael.Party.select('type="MtM Market"'):
    	    	ml.append(m.ptyid)
    	    return ml
	def displayTF():
	    filterlst = []
	    for f in ael.TradeFilter.select():
	    	filterlst.append(f.fltid)
	    return filterlst
	usefltval = ['YES', 'NO']
	ycval = {'YES':1,'NO':0}
        ael_variables = [('date', 'Date', 'string', dates, display_day, 0, 0), ('mkt', 'MARKET', 'string', displayMkt(), None, 1, 0), ('bcurr', 'BaseCurr', 'string', None, 'ZAR', 1, 0), ('updatYC', 'Update YC', 'string', ycval.keys(), 'YES', 1, 0), ('flt', 'FILTER', 'string', displayTF(), None, 0, 0), ('useflt', 'UseFilter', 'string', usefltval, 'NO', 1, 0)]
        def ael_main(parameter):
            day = parameter.get('date')
	    market = ael.Party[parameter.get('mkt')]
	    basecurr = parameter.get('bcurr')
	    update_yc = ycval[parameter.get('updatYC')]
	    use = parameter.get('useflt')
	    Filterid = ''
	    if not day:
                day = date
            if not day or day in ('Today', 'today', 't', 'T'):
                day = str(ael.date_today())
            elif day in ('Yesterday', 'yesterday', 'y', 'Y'):
                day = str(ael.date_today().add_days(-1))
            else:
                day = str(ael.date(day))
#############
#   ABSA CODE
#############
    	    
    	    B = []
    	    if (use == 'YES'):
	    	Filterid = parameter.get('flt')
		list = ael.TradeFilter[Filterid]
    	    	trds = list.trades()
    	    	for i in trds:
    	    	    if i.insaddr.insid not in B:
    	    	    	B.append(i.insaddr.insid)     	    
	   	
            FMtMGeneral.log(1, 'MtM date:%s' % str(day))
    	    ael.date_set_today(ael.date_today())
	    print 'ABSA CODE'	
    	    mtm = FMtMParamsFilter.FMarkToMarket(market, volmarket, 
	        ael.date_from_string(day), basecurr, aliastypes, distributors, 
	        spread, bid_and_ask, digits, verbosity, B)

	    if update_vol:
    	    	if aliastypes != None:
    		    FMtMGeneral.log(2, '\n0 Create Vols and Context\n')
    	    	    FMtMGeneral.create_vols_and_ctx(mtm, volsuffix,
    		        mtm.aliastypes, context)
    		    
    	    	if distributors != None:
    		    FMtMGeneral.log(2, '\n0 Create Vols and Context\n')
    		    FMtMGeneral.create_vols_and_ctx(mtm, volsuffix,
		        mtm.distributors, context)

            if save_seq_prices:
            	try:
	            import FEqAverage
	            if hasattr(FEqAverage, 'UdateAveragePrice'):
	                FMtMGeneral.log(2, '\n UpdateAveragePrice \n')
		        FEqAverage.UpdateAveragePrice()
	        except ImportError:
    	            pass
                try:
	            import FCliquetParams
	            if hasattr(FCliquetParams, 'UpdateCliquetPrice'):
		    	FMtMGeneral.log(2, '\n UpdateCliquetPrice \n')
		    	FCliquetParams.UpdateCliquetPrice()
	    	except ImportError:
    	    	    pass
            	try:
	            import FEqLadder
	            if hasattr(FEqLadder, 'UpdateLadderRungs'):
	                FMtMGeneral.log(2, '\n UpdateLadderRungs \n')
		    	FEqLadder.UpdateLadderRungs()
	        except ImportError:
    	    	    pass
                try:
	            import FEqBarrier
	            if hasattr(FEqBarrier, 'UpdateBarrierStatus'):
	            	FMtMGeneral.log(2, '\n UpdateBarrierStatus \n')
		    	FEqBarrier.UpdateBarrierStatus()
	        except ImportError:
    	    	    pass
                try:
	            import FEqDoubleBarrier
	            if hasattr(FEqDoubleBarrier, 'UpdateDoubleBarrierStatus'):
		    	FMtMGeneral.log(2, '\n UpdateDoubleBarrierStatus \n')
		    	FEqDoubleBarrier.UpdateDoubleBarrierStatus()
	    	except ImportError:
    	    	    pass

    	    if save_prices and calc_exceptions:
	    	FMtMGeneral.log(2, '\n1 MtM for Exceptions\n')
	    	try:
	            import FMtMCustomization
	            res = FMtMCustomization.custom_valuation(exception_list)
	            for r in res:
		    	ins = r[0]
		    	value = r[1]
    	            	mtm.store_exception_price(ins, ins.curr, value)
	        except ImportError:
    	            pass
    	    
	    if update_yc:
	        FMtMGeneral.log(2, '\n2 Update Yield Curves\n')
	        FMtMGeneral.update_yc(yieldcurves)

    	    if calc_imp_div_yield:
	    	FMtMGeneral.log(2, '\n3 Calculate Div Yield\n')
	    	for i in underlyings:
	    	    x = ael.Instrument[i]
		    if aliastypes != None:
	    	    	FDivYield.update_yc(x, 'All', mtm.ins1.items())
		    if distributors != None:
		    	FDivYield.update_yc(x, 'All', mtm.ins4.items())
		    if None in (aliastypes, distributors):
		    	FDivYield.update_yc(x, 'All', None)

            if recalc_vol:
                FMtMGeneral.log(2, '\n4 Recalculate Volatility Surfaces\n')
                FMtMGeneral.recalc_vol_surfaces(volsurfaces)

	    if update_vol:
	    	if aliastypes != None:
		    FMtMGeneral.log(2, '\n5 Update Vols\n')
	    	    FMtMGeneral.update_vols(mtm, volsuffix,
		        mtm.aliastypes, context)
		    
	    	if distributors != None:
		    FMtMGeneral.log(2, '\n5 Update Vols\n')
		    FMtMGeneral.update_vols(mtm, volsuffix,
		        mtm.distributors, context)
    	
    	    if update_vol:
	    	if aliastypes != None:
	    	    FMtMGeneral.log(2, '\n8 Save AliasType Vols\n')
	    	    mtm.do_save_aliastype_vols()
		    
	    	if distributors != None:
	    	    FMtMGeneral.log(2, '\n8 Save Distributor Vols\n')
	    	    mtm.do_save_distributors_vols()
    	
    	    if save_prices:
    	    	FMtMGeneral.log(2, '\n9 MtM for Underlying\n')
	    	mtm.do_mtm_underlying()

    	        if aliastypes != None:
    		    FMtMGeneral.log(2, '\n10 MtM for Alias\n')
		    mtm.do_mtm_for_alias()

	    	if distributors != None:
		    FMtMGeneral.log(2, '\n10 MtM for Distributors\n')
		    mtm.do_mtm_for_distributors()

    	    	FMtMGeneral.log(2, '\n11 MtM on Rest\n')
	    	mtm.do_mtm_on_rest()
    	    
    	    import SAGEN_CopyMTM_TO_SPOT
    	    SAGEN_CopyMTM_TO_SPOT.copy_mtm_to_spot(['ZAR/PIC_BASKET', 'ZAR/OPTI', 'ZAR/OPTI_NEW', 'ZAR/PIC2', 'ZAR/PIC3', 'ZAR/CAD'])

    	    if save_theor_prices:
    	    	FMtMGeneral.log(2, '\n6 MtM/Vol for Options and Warrants on Stock\n')
    	    	mtm.do_mtm_opt_and_warrants_on_stock()
    
    	    	FMtMGeneral.log(2, '\n7 MtM/Vol for options and Warrants on Index\n')
    	    	mtm.do_mtm_opt_and_warrants_on_index()
	    
	    FMtMGeneral.log(1, "\nMarkToMarket finished %s" % \
	        str(time.ctime(time.time())))
	    FMtMGeneral.log(1, "MarkToMarket has been successful!")
	    subj = 'MarkToMarket'
	    msg = 'has been successful!'
	    if sendmail:
	        ael.sendmail(rec, subj, msg)
#-----------------------------------------------------------------------------------------
#  ASQL Function
#-----------------------------------------------------------------------------------------
	def automain(i,basecurr,day,market,update_yc,flt,use,*rest):
    	    print basecurr, day, market, update_yc
#   	    reload(FMtMParams)
#	    print 'load'
#	    reload(FMtMGeneral)
	    market = ael.Party[market]
	    print market.ptyid
	    print 'Starting Ael Mark To Market'
	    Filterid = ''
	    if not day:
                day = date
            if not day or day in ('Today', 'today', 't', 'T'):
                day = str(ael.date_today())
            elif day in ('Yesterday', 'yesterday', 'y', 'Y'):
                day = str(ael.date_today().add_days(-1))
            else:
                day = str(ael.date(day))

            FMtMGeneral.log(1, 'MtM date:%s' % str(day))
    	    ael.date_set_today(ael.date_today())
    	    B = []
	    if (use == 'YES'):
	    	Filterid = flt
		list = ael.TradeFilter[Filterid]
    	    	trds = list.trades()
    	    	for i in trds:
    	    	    if i.insaddr.insid not in B:
    	    	    	B.append(i.insaddr.insid)
			
	    mtm = FMtMParamsFilter.FMarkToMarket(market, volmarket, 
	        ael.date_from_string(day), basecurr, aliastypes, distributors, 
	        spread, bid_and_ask, digits, verbosity, B)

	    if update_vol:
    	    	if aliastypes != None:
    		    FMtMGeneral.log(2, '\n0 Create Vols and Context\n')
    	    	    FMtMGeneral.create_vols_and_ctx(mtm, volsuffix,
    		        mtm.aliastypes, context)
    		    
    	    	if distributors != None:
    		    FMtMGeneral.log(2, '\n0 Create Vols and Context\n')
    		    FMtMGeneral.create_vols_and_ctx(mtm, volsuffix,
		        mtm.distributors, context)

            if save_seq_prices:
            	try:
	            import FEqAverage
	            if hasattr(FEqAverage, 'UdateAveragePrice'):
	                FMtMGeneral.log(2, '\n UpdateAveragePrice \n')
		        FEqAverage.UpdateAveragePrice()
	        except ImportError:
    	            pass
                try:
	            import FCliquetParams
	            if hasattr(FCliquetParams, 'UpdateCliquetPrice'):
		    	FMtMGeneral.log(2, '\n UpdateCliquetPrice \n')
		    	FCliquetParams.UpdateCliquetPrice()
	    	except ImportError:
    	    	    pass
            	try:
	            import FEqLadder
	            if hasattr(FEqLadder, 'UpdateLadderRungs'):
	                FMtMGeneral.log(2, '\n UpdateLadderRungs \n')
		    	FEqLadder.UpdateLadderRungs()
	        except ImportError:
    	    	    pass
                try:
	            import FEqBarrier
	            if hasattr(FEqBarrier, 'UpdateBarrierStatus'):
	            	FMtMGeneral.log(2, '\n UpdateBarrierStatus \n')
		    	FEqBarrier.UpdateBarrierStatus()
	        except ImportError:
    	    	    pass
                try:
	            import FEqDoubleBarrier
	            if hasattr(FEqDoubleBarrier, 'UpdateDoubleBarrierStatus'):
		    	FMtMGeneral.log(2, '\n UpdateDoubleBarrierStatus \n')
		    	FEqDoubleBarrier.UpdateDoubleBarrierStatus()
	    	except ImportError:
    	    	    pass

    	    if save_prices and calc_exceptions:
	    	FMtMGeneral.log(2, '\n1 MtM for Exceptions\n')
	    	try:
	            import FMtMCustomization
	            res = FMtMCustomization.custom_valuation(exception_list)
	            for r in res:
		    	ins = r[0]
		    	value = r[1]
    	            	mtm.store_exception_price(ins, ins.curr, value)
	        except ImportError:
    	            pass
 
	    if update_yc:
	        FMtMGeneral.log(2, '\n2 Update Yield Curves\n')
	        FMtMGeneral.update_yc(yieldcurves)

    	    if calc_imp_div_yield:
	    	FMtMGeneral.log(2, '\n3 Calculate Div Yield\n')
	    	for i in underlyings:
	    	    x = ael.Instrument[i]
		    if aliastypes != None:
	    	    	FDivYield.update_yc(x, 'All', mtm.ins1.items())
		    if distributors != None:
		    	FDivYield.update_yc(x, 'All', mtm.ins4.items())
		    if None in (aliastypes, distributors):
		    	FDivYield.update_yc(x, 'All', None)

            if recalc_vol:
                FMtMGeneral.log(2, '\n4 Recalculate Volatility Surfaces\n')
                FMtMGeneral.recalc_vol_surfaces(volsurfaces)

	    if update_vol:
	    	if aliastypes != None:
		    FMtMGeneral.log(2, '\n5 Update Vols\n')
	    	    FMtMGeneral.update_vols(mtm, volsuffix,
		        mtm.aliastypes, context)
		    
	    	if distributors != None:
		    FMtMGeneral.log(2, '\n5 Update Vols\n')
		    FMtMGeneral.update_vols(mtm, volsuffix,
		        mtm.distributors, context)
    	
    	    if update_vol:
	    	if aliastypes != None:
	    	    FMtMGeneral.log(2, '\n8 Save AliasType Vols\n')
	    	    mtm.do_save_aliastype_vols()
		    
	    	if distributors != None:
	    	    FMtMGeneral.log(2, '\n8 Save Distributor Vols\n')
	    	    mtm.do_save_distributors_vols()
 
    	    if save_prices:
    	    	FMtMGeneral.log(2, '\n9 MtM for Underlying\n')
	    	mtm.do_mtm_underlying()

    	        if aliastypes != None:
    		    FMtMGeneral.log(2, '\n10 MtM for Alias\n')
		    mtm.do_mtm_for_alias()

	    	if distributors != None:
		    FMtMGeneral.log(2, '\n10 MtM for Distributors\n')
		    mtm.do_mtm_for_distributors()

    	    	FMtMGeneral.log(2, '\n11 MtM on Rest\n')
	    	mtm.do_mtm_on_rest()
	    
	    import SAGEN_CopyMTM_TO_SPOT
    	    SAGEN_CopyMTM_TO_SPOT.copy_mtm_to_spot(['ZAR/PIC_BASKET', 'ZAR/OPTI', 'ZAR/OPTI_NEW', 'ZAR/PIC2', 'ZAR/PIC3', 'ZAR/CAD'])

    	    if save_theor_prices:
    	    	FMtMGeneral.log(2, '\n6 MtM/Vol for Options and Warrants on Stock\n')
    	    	mtm.do_mtm_opt_and_warrants_on_stock()
    
    	    	FMtMGeneral.log(2, '\n7 MtM/Vol for options and Warrants on Index\n')
    	    	mtm.do_mtm_opt_and_warrants_on_index()
		
 	    FMtMGeneral.log(1, "\nMarkToMarket finished %s" % \
	        str(time.ctime(time.time())))
	    	
	    FMtMGeneral.log(1, "MarkToMarket has been successful!")
	    subj = 'MarkToMarket'
	    msg = 'has been successful!'
	    if sendmail:
	        ael.sendmail(rec, subj, msg)
	    return 1	
except ExitScriptError, e:
    if globals().has_key('ael_variables'):
    	del globals()['ael_variables']
    if globals().has_key('ael_main'):
    	del globals()['ael_main']
    print e
