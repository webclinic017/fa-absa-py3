""" SEQ_VERSION_NR = PRIME 2.8.1 """





"""----------------------------------------------------------------------------
MODULE
    FEqBasketUtils - Common Basket option code
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.
 ----------------------------------------------------------------------------""" 
import ael
import math
from FEqUtilsPRIME import *

F_BASKET_EXCEPT   = 'f_eq_basket_xcp'  
F_BASKET_WARNING  = 'f_eq_basket_warning,'  
TIMETOEXP_WARNING = 'The option has already expired.'

"""----------------------------------------------------------------------------
get_corr_matrix
    The function returns the correlation matrix mapped to the instrument itself 
    or to the valgroup. If this equals none, the matrix mapped to the underlying
    equity index is returned.
----------------------------------------------------------------------------"""    
def get_corr_matrix(i,trading = 0):
    corr_matrix = None
    corr_matrix = ael.CorrelationMatrix[i.used_context_parameter('Correlation Matrix')]
    if corr_matrix == None:
        corr_matrix = ael.CorrelationMatrix[i.und_insaddr.used_context_parameter('Correlation Matrix')]
    if corr_matrix == None:
        if not trading: 
            print "\n## !! EXCEPTION !! ##"
        raise F_BASKET_EXCEPT, 'No correlation is mapped to the instrument.'
    return corr_matrix
    
"""----------------------------------------------------------------------------
Corr
    Fetch the Correlation matrix of the stocks included in the basket.
----------------------------------------------------------------------------"""    
def Corr(stock_array, option, trading = 0,rainbow = 0):
    if len(stock_array) == 1:return [[[1.0]], {}]
    corr_mat = []
    correlation_dict = {}
    try: CORR = get_corr_matrix(option, trading)
    except F_BASKET_EXCEPT, msg: 
        if trading: 
            if rainbow: return [[msg, [msg]], msg]
            return [msg, msg]
        raise F_BASKET_EXCEPT, msg
    
    # Corr is a list of lists, where the i:th list corresponds the i:th colonn in 
    # the correlation matrix between the returns of the underlying assets. Since the 
    # correlation matrix is symmetrical we only define the upper triangular in the 
    # correlation matrix.
    if len(stock_array)<2: 
        if trading: return ['Too few components in basket!', 'Too few components in basket!']
        return 0
    for i in range(len(stock_array)):
        col=[]
        stock_i = stock_array[i]
        correlation_dict[stock_i.insid] = {}
        # Only the upper tringular of the correlation matrix needs to be defined
        for j in range(i):
            stock_j = stock_array[j]
            corr_ij = CORR.used_correlation(stock_i, stock_j)
            correlation_dict[stock_i.insid][stock_j.insid] = corr_ij
            correlation_dict[stock_j.insid][stock_i.insid] = corr_ij
            if abs(corr_ij) > 1:
                if trading: 
                    r = stock_i.insid + " vs. " + stock_j.insid + ": The corr. abs. value is > 1."
                    return [r, r]
                print "\n## !! "+ stock_i.insid + " vs. " + stock_j.insid +" !! ##"
                print "Value: ", corr_ij
                raise F_BASKET_EXCEPT, "The correlation's absolute value is greater than one."
            if corr_ij == 0.0:
                if trading:
                    r = stock_i.insid + " vs. " + stock_j.insid + ": The corr. equals zero!"
                    return [r, r]
                print "\n## !! "+ stock_i.insid + " vs. " + stock_j.insid +" !! ##"
                raise F_BASKET_EXCEPT, "The correlation between the stocks equals zero." 
            col.append(corr_ij)
        col.append(1.0)      
        corr_mat.append(col)
    return [corr_mat, correlation_dict]

"""----------------------------------------------------------------------------
CorrFx
    Fetch the Correlation matrix of the correlations between the FX rates.        
----------------------------------------------------------------------------"""    
def CorrFx(stock_array, option, val_date,strike_curr, trading = 0):
    corr_mat = []
    corr_dict = {}
    try: CORR = get_corr_matrix(option, trading)
    except F_BASKET_EXCEPT, msg: 
        if trading: return [msg, msg]
        raise F_BASKET_EXCEPT, msg
    if len(stock_array)<2: 
        if trading: return ['Too few components in basket!', 'Too few components in basket!']
        return 0
    for i in range(len(stock_array)):
        col = []
        stock_i = stock_array[i]
        for j in range(0, i+1):
            stock_j = stock_array[j]
            if stock_i.curr == strike_curr and stock_j.curr == strike_curr:
                corr_ij = 1
            else:
                if stock_i.curr != strike_curr:
                    try: curr_pair_i = strike_curr.currency_pair(stock_i.curr.insid)
                    except Exception, msg: 
                        if trading: return [str(msg), str(msg)]
                        print "\n## !! EXCEPTION !! ##"
                        raise F_BASKET_EXCEPT, msg
                else: curr_pair_i = None

                if stock_j.curr != strike_curr:
                    try: curr_pair_j = strike_curr.currency_pair(stock_j.curr.insid)
                    except Exception, msg: 
                        if trading: return [msg, msg]
                        print "\n## !! EXCEPTION !! ##"
                        raise F_BASKET_EXCEPT, msg
                else: curr_pair_j = None

                if curr_pair_i != None and curr_pair_j != None: 
                    if corr_dict.has_key((curr_pair_i.name, curr_pair_j.name)):
                        corr_ij = corr_dict[(curr_pair_i.name, curr_pair_j.name)]
                    else:
                        corr_ij = CORR.used_correlation(curr_pair_i, curr_pair_j)
                        if corr_ij == 0:
                            if trading:
                                r = curr_pair_i.name + " vs. " + curr_pair_j.name + ": The corr. equals zero."
                            print "\n## !! "+ curr_pair_i.name + " vs. " + curr_pair_j.name +" !! ##"
                            raise F_BASKET_EXCEPT, "The correlation between the currency pairs equals zero."
                        corr_dict[(curr_pair_i.name, curr_pair_j.name)] = corr_ij
                else: corr_ij = 0
            col.append(corr_ij)
        corr_mat.append(col)
    return [corr_mat, corr_dict]
    
"""----------------------------------------------------------------------------
CorrStockFx
    Fetch the Correlation matrix of the correlations between the stocks and the FX rates.
----------------------------------------------------------------------------"""    
def CorrStockFx(stock_array, option, val_date,strike_curr,trading = 0):
    corr_mat = []
    corr_dict = {}
    try: CORR = get_corr_matrix(option, trading)
    except F_BASKET_EXCEPT, msg: 
        if trading: return [msg, msg]
        raise F_BASKET_EXCEPT, msg
    if len(stock_array)<2: 
        if trading: return ['Too few components in basket!', 'Too few components in basket!']
        return 0
    for i in range(len(stock_array)):
        corr_mat.append([])   
        stock_i = stock_array[i]
        for j in range(len(stock_array)):
            stock_j = stock_array[j]
            if stock_i.curr == strike_curr: corr_ij = 0
            else:
                if stock_j.curr != strike_curr:
                    try: curr_pair_j = strike_curr.currency_pair(stock_j.curr.insid)
                    except Exception, msg: 
                        if trading: return [str(msg), str(msg)]
                        print "\n## !! EXCEPTION !! ##"
                        raise F_BASKET_EXCEPT, msg
                else: curr_pair_j = None

                if curr_pair_j != None:
                    if corr_dict.has_key((stock_i.insid, curr_pair_j.name)):
                        corr_ij = corr_dict[(stock_i.insid, curr_pair_j.name)]
                    else:
                        corr_ij = CORR.used_correlation(stock_i, curr_pair_j)
                        if corr_ij == 0:
                            if trading: 
                                r = stock_i.insid + " vs. " + curr_pair_j.name + ": The corr. equals zero."
                                return [r, r]
                            print "\n## !! "+ stock_i.insid + " vs. " + curr_pair_j.name +" !! ##"
                            raise F_BASKET_EXCEPT, "The correlation between the stock and the currency pair equals zero."
                        corr_dict[(stock_i.insid, curr_pair_j.name)] = corr_ij
                else: corr_ij = 0
            corr_mat[i].append(corr_ij)
    return [corr_mat, corr_dict]


"""----------------------------------------------------------------------------
get_fx_rates
    The fix fx rates are returned.
----------------------------------------------------------------------------"""    
def get_fx_rates(stock_links,trading=0):
    # Get the fix FX rates
    fx = []
    for stock_link in stock_links:
        fx_j = stock_link.fix_fx_rate
        if fx_j == 0.0:
            try:
                fx_j = float(ael.dbsql('select value from additional_info where recaddr = ' + str(stock_link.seqnbr))[0][0][0])
            except:
                # No FX rate is defined for the stock. The error will be 
                # handled later on.
                fx_j = 0.0
        if fx_j < 0.0:
            if trading: return "There are negative FX rates!"
            else: raise F_BASKET_EXCEPT, "There are negative FX rates!"
        fx.append(fx_j)
    return fx            

"""----------------------------------------------------------------------------
get_fx_error
    The function checks if the fix fx rates have been defined.
----------------------------------------------------------------------------"""    
def get_fx_error(fx, stocks):
    no_fx_ins = []
    fx_error = 0
    if fx != [] and fx != ():
        j = 0
        for fx_j in fx:
            if fx_j != 0.0: 
                fx_error = 0
            else: 
                fx_error = 1
                no_fx_ins.append(stocks[j].insid)
            j = j + 1
    return [fx_error, no_fx_ins]

"""----------------------------------------------------------------------------
get_dividends
    A vector with a dividend vector for each underlying instrument is returned.
----------------------------------------------------------------------------"""    
def get_dividends(stock_array, exp_day):
    dividends = []
    for stock in stock_array:
        # Discrete dividends, the value of the volatility part of the underlying assets
        jdiv = []
        for div in stock.dividends(exp_day):
            # The dividend is a pair (div,time)
            jdiv.append((div.dividend, ael.date_valueday().years_between(div.ex_div_day, 'Act/365')))
        dividends.append(jdiv)
    return dividends


"""----------------------------------------------------------------------------
basket_val_meth()
    The method derives the best valuation method. 
    There exists four different methods:

    "MonteCarlo"      - Crude Monte Carlo method.
    "quasiMC"         - quasi Monte Carlo method using sobol numbers.
    "KemnaVorstMC"    - Monte Carlo method using a control variates technique
                        proposed by Kemna et al in
                        Kemna, A.G.Z. & Vorst, A.C.F. (1990)
                        "A Pricing Method for Options Based on Average Asset Values"
                        Journal of Banking and Finance 14, 113-129
     "Gentle"         - An approximation method originally proposed by Gentle, see
                        Gentle, D. (1993) "Basket Weaving" RISK 6(6), 51-53
     "MomentMatching" - Moment matching method is now available in the valuation 
                        library f_eq_average.

     nbr_of_sim denotes the number of a simulations. One simulations means simulating the
     value of the (whole) basket (or portfolio) one time. 
----------------------------------------------------------------------------"""    
def basket_val_meth():
    val_meth = "MomentMatching"
    #val_meth = "Gentle"  
    if val_meth == "Gentle" or val_meth == "MomentMatching": 
        nbr_of_sim = 0
    else: 
        # 2 raised to the power of 14
        nbr_of_sim    = 16384 
    return [val_meth, nbr_of_sim]


"""----------------------------------------------------------------------------
ResultVal() 
    The function checks the result and displays error messages.
----------------------------------------------------------------------------"""    
def ResultVal(res):
    try:
        if res >= 0.0: return res
    except Exception, msg:
        print  "\n## !! EXCEPTION !! ##"
        raise F_BASKET_EXCEPT, msg
    if res == -1.0:
        print  "\n## !! EXCEPTION !! ##"
        raise F_BASKET_EXCEPT, 'The correlation matrix is not positive definite.'
    elif res == -3.0:
        print  "\n## !! EXCEPTION !! ##"
        raise F_BASKET_EXCEPT, 'There are too many assets in basket, max = 100.'
    elif res == -4.0:
        print  "\n## !! EXCEPTION !! ##"
        raise F_BASKET_EXCEPT, 'Negative input values.'
    elif res == -5.0:
        print  "\n## !! EXCEPTION !! ##"
        raise F_BASKET_EXCEPT, 'The number of simulations must be increased.'
    elif res == -6.0:
        print  "\n## !! EXCEPTION !! ##"
        raise F_BASKET_EXCEPT, 'The valuation method is not implemented.'
    else: 
        print  "\n## !! EXCEPTION !! ##"
        return 0.0     

"""----------------------------------------------------------------------------
get_pv() 
    The function returns the present value for a basket option/warrant.
----------------------------------------------------------------------------"""    
def get_pv(bp, val_meth_params):
    try:
        if (bp.eur_ame != 0): 
            print "\n## !! EXCEPTION !! ##"
            raise F_BASKET_EXCEPT, 'American basket options are not handled.'
        if (bp.texp == 0.0):
            raise F_BASKET_WARNING, TIMETOEXP_WARNING 
        if (bp.texp < 0.0):    
            return 0.0

        [val_meth, nbr_of_sim] = val_meth_params
        
        if bp.fx_error:
            print  "\n## !! NO VALUE !! ##"
            if len(bp.no_fx_ins) == bp.dim:
                raise F_BASKET_EXCEPT, "No FX rates are defined for the basket. Use the ASQL application .MaintCreateQuantoBasketFX."
            else: 
                for ins in bp.no_fx_ins:
                    print "## !!" + str(ins) + " !! ##"
                    raise F_BASKET_EXCEPT, "No FX rates are defined for these basket components. Use the ASQL application .MaintCreateQuantoBasketFX."
        
        for price in bp.price:
            try: float(price)
            except: 
                print  "\n## !! NO VALUE !! ##"
                raise F_BASKET_EXCEPT, "Some underlying prices does not exist."

        if bp.quanto_flag:
            res = ael.eq_quantobasket2(bp.price, bp.texp, bp.vol, bp.fx, 
                                    bp.fxvol, bp.corr_stocks, bp.corr_fx, bp.corr_stock_fx,
                                    bp.rate, bp.rate_stocks, bp.carry_cost, bp.strike,
                                    bp.put_call, bp.dividends, bp.fixfx_flag, bp.weights,
                                    val_meth, nbr_of_sim)
        else:
            res = ael.eq_basket2(bp.price, bp.texp, bp.vol, bp.corr_stocks, bp.rate,
                                     bp.carry_cost, bp.strike, bp.put_call, bp.dividends,
                                     bp.weights, val_meth, nbr_of_sim)
        res = ResultVal(res) * bp.df

    # Handling warnings: 
    except F_BASKET_WARNING, msg:
        if msg == TIMETOEXP_WARNING:
            wS0 = 0.0
            for j in range(bp.dim):
                wS0 = wS0 + bp.price[j]
            if (bp.put_call == 1) and (wS0>=bp.strike):
                res = wS0-bp.strike
            elif (bp.put_call == 0) and (wS0<=bp.strike):res = bp.strike-wS0
            else:res = 0.0 
        else:
            print  "\n## !! EXCEPTION !! ##"
            raise F_BASKET_EXCEPT, msg
    return res





