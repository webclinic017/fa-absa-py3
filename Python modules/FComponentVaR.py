""" ConsolidatedRisk:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FComponentVaR - Component Value at Risk

(c) Copyright 2002 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
	This module is intended as an example of how to calculate component VaR
        in FRONT ARENA.
        The component VaR for a trade is calculated as the delta for a trade
        towards a set of risk factors times the VaR delta vector for the filter.
        This method should be used instead of stand alone VaR calculations
        since this information is of much more value for hedging purposes
        and for explaining the total VaR number.

NOTE
	Limited error handling

DATA-PREP	
        A proper risk factor setup in FRONT ARENA is needed.

REFERENCES
        Python website http://www.python.org
        FRONT ARENA knowledge base.
        Improving on VaR, Mark Garman - Risk Magazine Vol 9 No 5 May 1996
----------------------------------------------------------------------------"""

import ael, math

try:
    import Numeric
    import_numeric_ok = 1
except:
    print 'Warning Python extension module Numeric not found'
    import_numeric_ok = 0


#
# covariance_matrix()
# Creates a covariance matrix with use of ARENA functions rf_correlation and
# rf_volatility. 
# Arguments:
#		rfsh - a reference to a RiskFactorSpecHeader entity
#		k - a volatility scale factor
# Returns:
# 		A tuple containing
#		- a dictionary with RiskFactorSpec external IDs as keys and
#		  containing RiskFactorSpec ael entities  
#		- a list of RiskFactorSpec external IDs sorted alphabetically
#		- a covariance matrix as a Numeric array
#
# Usage
# 		rf_dict,rf_list, mtr = covariance_matrix(rfsh)
#

def covariance_matrix(tf, rfsh, k):

    global recalc, rf_dict, rf_list, mtr

    try:
    	raise
    	rf_list = tf.rf_list()
	recalc = 1
    except:
    	hdrnbr = rfsh.rfspechdrnbr
    	rf_list = ael.RiskFactorSpec.select('rfspechdrnbr = %i' % hdrnbr)
	recalc = 0
    
    #try:
    #	if not recalc and mtr:
    #	    return (rf_dict,rf_list,mtr)
    #except:
    #	pass
    
    error = 0
    rf_dict = {}
    for rfs in rf_list:
        rf_dict[rfs.extern_id] = rfs
    rf_list = rf_dict.keys()
    rf_list.sort()
    size = len(rf_list)
    mtr = Numeric.zeros([size, size], 'f')
    
    for row in range(size):
    	rfs1 = rf_dict[rf_list[row]]
	try:
            vol1 = rfs1.rf_volatility()
	except:
	    vol1 = 0.0
	    error = 1
        for col in range(row+1):
            rfs2 =  rf_dict[rf_list[col]]
	    try:
            	vol2 = rfs2.rf_volatility()
            	corr = rfs2.rf_correlation(rfs1)
	    except:
	    	corr = vol2 = 0.0
		error = 1
            mtr[col][row] = mtr[row][col] = corr*vol1*vol2*k
    
    if error:
    	print 'rf_volatility or rf_correlation failed' 
	print 'Check Risk Factor Specification and FCS_DIR_RISK'
    
    return (rf_dict, rf_list, mtr)
#
# create_rftype_vector()
# Creates a vector with index corresponding to risk factors of a certain
# type in rf_list.
#
# Arguments:
#		rf_list - a list of risk factor external ids
#		rf_dict - a dictionary with [risk factor id] = rf ael entity
#		rftype - a risk factor type
# Returns:
# 		A python list
#
# Usage
# 		rf_type_vector = create_rftype_vector(rf_list,rf_dict,rftype)
#

def create_rftype_vector(rf_list, rf_dict, rftype):
    
    vec = []
    
    for i in range(len(rf_list)):
    	rf = rf_dict[rf_list[i]]
    	seqnbr = rf.rfgnbr.seqnbr
	rfgs = ael.RiskFactorMember.select('rfgnbr = %i' % seqnbr)
	if rfgs[0].rfgtype == rftype:
	    vec.append(i)
    return vec
    	

#
# deltaVector()
# Creates a delta vector with rf_delta
# Arguments:
#		tf - a Trade Filter
#		rf_list - a list of risk factor ids
#		rf_dict - a dictionary with RiskFactorSpec ael entities
#		rftype - a risk factor type
#		acc_cash - 1 or 0. IF 1, FX risk will be calculated for
#		accumulated cash  
#		recalc - 1 or 0. IF 1, all deltas will be recalculated.
#   	    	external_file - the name of a text file with risk factor
#   	    	deltas.
# Returns:
#		a delta vector as a Numeric array
#
# Usage
# 		rf_deltas = deltaVector(tf,rf_list,rf_dict,rftype,acc_cash,recalc)
#

def deltaVector(tf,rf_list,rf_dict,rftype,acc_cash,recalc,external_file = None):

    global delta_vectors, rf_type_vectors
    
    try:
    	rf_type_vectors
    except:
    	rf_type_vectors = {}
    
    
    try:
	delta_vectors
	if recalc:
	    raise
    except:
    	delta_vectors = {}
    
    if tf.record_type == 'TradeFilter':
    	name = tf.fltid
    else:
    	name = tf.trdnbr
    
    vec = 0.0*Numeric.ones(len(rf_list), 'f')
    
    try:
    	delta_vector = delta_vectors[name]
    except:     	
    	for i in range(len(rf_list)):
    	    vec[i] = tf.rf_delta(external_file, None, rf_dict[rf_list[i]], 1, acc_cash)
    	delta_vectors[name] = vec
	delta_vector = vec
    
    if not (rftype == None or rftype in ('None', '', 'full', 'all')):
    	
    	if rftype not in rf_type_vectors.keys():
	    rf_type_list = create_rftype_vector(rf_list, rf_dict, rftype)
	    rf_type_vectors[rftype] = rf_type_list
	else:
	    rf_type_list = rf_type_vectors[rftype]
	
	for inx in rf_type_list:
	    vec[inx] = delta_vector[inx]
    else:
    	vec = delta_vector
    
    return vec

#
# rfsDeltaVector()
# Creates a delta vector with rf_delta
# Arguments:
#		tf - a Trade Filter
#		rf_list - a list of risk factor ids
#		rf_dict - a dictionary with RiskFactorSpec ael entities
#		acc_cash - 1 or 0. IF 1, FX risk will be calculated for
#		accumulated cash  
#		recalc - 1 or 0. IF 1, all deltas will be recalculated.
#   	    	external_file - the name of a text file with risk factor
#   	    	deltas.
# Returns:
#		a delta vector as a Numeric array
#
# Usage
# 		rf_deltas = deltaVector(tf,rf_list,rf_dict,rftype,acc_cash,recalc)
#

def rfsDeltaVector(portf,rf_list,rf_dict,rfs,acc_cash,recalc,external_file = None):
    
    vec = 0.0*Numeric.ones(len(rf_list), 'f')
    
    try:
    	inx = rf_list.index(rfs.extern_id)
    except:
    	return vec
	
    vec[inx] = portf.rf_delta(external_file, None, rf_dict[rf_list[inx]], 1, acc_cash)
    
    return vec


#
# deltaVaR()
# Calculates a delta VaR vector for a tradefilter.
# Arguments:
#		tf - a Trade Filter
#		rfsh - a RiskFactorSpecHeader
#		acc_cash - 1 or 0. IF 1, FX risk will be calculated for
#		accumulated cash  
#   	    	external_file - The name of a text file containing risk 
#    	    	factor deltas.
# Returns:
# 		A tuple containing
#		- a delta VaR vector as a Numeric array
#		- a list of RiskFactorSpec external IDs sorted alphabetically
#		- a dictionary with RiskFactorSpec external IDs as keys and
#		  containing RiskFactorSpec ael entities  
#
# Usage
# 		delta_vec, rf_list, rf_dict = deltaVaR(tf,rfsh)
#

def deltaVaR(tf,rfsh,acc_cash,external_file = None):
    
    try:
	rfsh = ael.RiskFactorSpecHeader[rfsh]
	if rfsh == None:
	    print 'RiskFactorSpecHeader not found'
	    return None, None, None
    except:
    	pass
    
    k = rfsh.volscale
    
    rf_dict, rf_list, covmtr = covariance_matrix(tf, rfsh, k)

    delta = deltaVector(tf, rf_list, rf_dict, None, acc_cash, 1, external_file)

    Qp = Numeric.matrixmultiply(covmtr, delta)
    
    VaR = tf.value_at_risk(external_file, None, None, None, acc_cash)
    
    if VaR >= 0.0:
    	DeltaVaR = Qp/VaR
    else:
    	DeltaVaR = Qp*0.0  
    
    return DeltaVaR, rf_list, rf_dict

    

"""----------------------------------------------------------------------------
FUNCTION	
	component_var_trade()

DESCRIPTION
	Calculates component/incremental VaR for a tradefilter and the
        corresponding trades. 
	
ARGUMENTS
    	trade  	    Table	   A reference to a record in the Trade table
	portf  	    String	   The name of a TradeFilter
    	rfsh  	    String	   The name of a RiskFactorSpecHeader
	rftype	    String  	   A risk factor type
	acc_cash    String/Int	   1 or 0. IF 1, FX risk will be calculated for
    	    	    	    	   accumulated cash  

RETURNS
	The component VaR for a trade.
	
----------------------------------------------------------------------------"""


def component_var_trade(trade, portf, rfsh, rftype, acc_cash, *rest):
    
    global trade_dict, delta_var, rf_list, rf_dict
    
    if not import_numeric_ok:
    	return 0
    
    try:
    	acc_cash = int(acc_cash) == 1
    except:
    	acc_cash = 0
        
    init = 0
    recalc = 0
    
    try:
    	portf = ael.TradeFilter[portf]
    except:
    	print portf, 'not found in database'
    
    try:
    	trade_dict
    except:
    	trade_dict = {}
    	init = 1
    
    if init or trade_dict.has_key(trade.trdnbr):
    	if init or rftype in trade_dict[trade.trdnbr]:
	    trade_dict = {}
	    delta_var, rf_list, rf_dict = deltaVaR(portf, rfsh, acc_cash)
	    if delta_var == None:
	    	return 0
    	    recalc = 1
    
    delta_vector = deltaVector(trade, rf_list, rf_dict, rftype, acc_cash, recalc)    
    cVaR = Numeric.matrixmultiply(Numeric.transpose(delta_vector), delta_var)    
    if trade_dict.has_key(trade.trdnbr):
    	temp_list = trade_dict[trade.trdnbr]
	temp_list.append(rftype)
    	trade_dict[trade.trdnbr] = temp_list
    else:
	trade_dict[trade.trdnbr] = [rftype] 
    return cVaR

"""----------------------------------------------------------------------------
FUNCTION	
	component_var_rfs()

DESCRIPTION
	Calculates component/incremental VaR for a RiskFactorSpec. 
	
ARGUMENTS
    	rfs  	    Table	   A reference to a record in the RiskFactorSpec
	    	    	    	   table
	portf  	    String	   The name of a TradeFilter
    	rfsh  	    String	   The name of a RiskFactorSpecHeader
	acc_cash    String/Int	   1 or 0. IF 1, FX risk will be calculated for
    	    	    	    	   accumulated cash  
	ext_file    String  	   The name of a text file containing risk
	    	    	    	   factor deltas.

RETURNS
	The component VaR for a RiskFactorSpec.
	
----------------------------------------------------------------------------"""

def component_var_rfs(rfs,portf,rfsh,acc_cash,ext_file = None,*rest):
    
    global rflist, rfdict, deltavar, rfs_list
    
    if not import_numeric_ok:
    	return 0
    
    try:
    	acc_cash = int(acc_cash) == 1
    except:
    	acc_cash = 0
    
    init = 0
    recalc = 0
    
    try:
    	rfs_list
	rflist
    except:
    	init = 1
    	rfs_list = {}
   
    try:
    	portf = ael.TradeFilter[portf]
    except:
    	print portf, 'not found in database'
    
    if init or rfs_list.has_key(portf.fltid):
    	if init or rfs.rfspecnbr in rfs_list[portf.fltid]:
    	    rfs_list = {}
	    deltavar, rflist, rfdict = deltaVaR(portf, rfsh, acc_cash, ext_file)
	    if deltavar == None:
	    	return 0
	    recalc = 1
    
    deltavector = rfsDeltaVector(portf, rflist, rfdict, rfs, acc_cash, recalc, ext_file)
    cVaR = Numeric.matrixmultiply(Numeric.transpose(deltavector), deltavar)
    if rfs_list.has_key(portf.fltid):
    	temp_list = rfs_list[portf.fltid]
	temp_list.append(rfs.rfspecnbr)
    	rfs_list[portf.fltid] = temp_list
    else:
	rfs_list[portf.fltid] = [rfs.rfspecnbr]    
    
    return cVaR
    
