""" ConsolidatedRisk:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FVaR - Functions for processing scenarios

(c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
	This module calculates Value at Risk from a scenario file

NOTE
	Limited error handling

DATA-PREP	
	Make sure the FCS_DIR_RISK environmental variable is set to point to a
        directory on your local hard drive or somewhere where you have read and write
        permissions.
        A proper risk factor setup in FRONT ARENA is needed.
        This module reads from a scenario file located in the FCS_DIR_RISK directory,
        generated by eg AEL module MonteCarloScen

REFERENCES
        Python website http://www.python.org
        FRONT ARENA knowledge base.
        Risk Metrics Technical document.
----------------------------------------------------------------------------"""

import ael, FVaRTools

try:
    import Numeric
except:
    pass

try:
    from os import environ
    from string import lower, split
except: 
    pass

COLUMN_DELIMITER = FVaRTools.column_delimiter()


#
#   Performs full revaluation on a scenario file
#
#   Arguments:
#      tf         - A TradeFilter, Portfolio, Instrument or Trade
#      filename   - The name of the scenario file
#      nbr        - Number of scenarios
#      hist_fx    - FX on accumulated cash or not (1 or 0)
#      offset     - Which scenario number to start at
#
#   Returns a vector of scenario results
#

def full_reval_scenario(tf,filename,nbr,hist_fx,offset = 0):

    res_list = []
    hist_fx = int(hist_fx)
    nbr = int(nbr)
    offset = int(offset)

    # Process scenarios
    
    for i in range(nbr):
        res_list.append(tf.rf_scenario(filename, offset+i+1, hist_fx))

    return res_list


#
#   Performs delta revaluation
#
#   Arguments:
#      tf         - A TradeFilter, Portfolio, Instrument or Trade
#      filename   - The name of the scenario file
#      nbr        - Number of scenarios
#      hist_fx    - FX on accumulated cash or not (1 or 0)
#      rfsh       - The name of a risk factor specification header
#      rf_list    - A list of risk factor specs
#      scen_mtr   - A scenario matrix
#
#   Returns a vector of scenario results
#

def delta_scenario(tf,filename,nbr,hist_fx,rfsh = None,rf_list = None,scen_mtr = None):

    hist_fx = int(hist_fx)
    nbr = int(nbr)

    # map help function
    def rf_extern_id(rf):
        return rf.extern_id

    # Check if ATLAS 3.4 or higher
    if rf_list == None or rf_list == []:
        rf_list = FVaRTools.get_rf_list(tf, rfsh)

    # Make delta vector
    rf_deltas = []
    for rf in rf_list:
        rf_deltas.append(tf.rf_delta(None, None, rf, 1, hist_fx))
    rf_deltas = Numeric.array(rf_deltas)

    # Make scenario matrix
    if scen_mtr == None:
        rf_name_list = map(rf_extern_id, rf_list)
        scen_mtr = FVaRTools.scenario_matrix(filename, nbr, rf_list)    
    
    # Process scenarios
    true_nbr = len(scen_mtr)
    results = []
    for s in range(true_nbr):
        res = Numeric.dot(rf_deltas, scen_mtr[s])
        results.append(res)

    scen_mtr = None
    del(scen_mtr)

    return results

#
#   Performs delta/gamma revaluation
#
#   Arguments:
#      tf         - A TradeFilter, Portfolio, Instrument or Trade
#      filename   - The name of the scenario file
#      nbr        - Number of scenarios
#      hist_fx    - FX on accumulated cash or not (1 or 0)
#      typ        - auto or cross
#      rfsh       - The name of a risk factor specification header
#      rf_list    - A list of risk factor specs
#      scen_mtr   - A scenario matrix
#
#   Returns a vector of scenario results
#

def delta_gamma_scenario(tf,filename,nbr,hist_fx,typ = 'auto',rfsh = None,rf_list = None, scen_mtr = None):

    hist_fx = int(hist_fx)
    nbr = int(nbr)

    if lower(typ) not in ('auto', 'cross'):
        print 'Type Error, argument type must be either of auto or cross'
        return [0]
        
    # map help function
    def rf_extern_id(rf):
        return rf.extern_id

    # Check if ATLAS 3.4 or higher
    if rf_list == None or rf_list == []:
        rf_list = FVaRTools.get_rf_list(tf, rfsh)

    # Make delta vector
    rf_deltas = []
    for rf in rf_list:
        rf_deltas.append(tf.rf_delta(None, None, rf, 1, hist_fx))
    rf_deltas = Numeric.array(rf_deltas)

    # Make gamma matrix
    if lower(typ) == 'cross':
        gamma_mtr = FVaRTools.gamma_matrix(tf, rf_list)
    else:
        gamma_mtr = FVaRTools.gamma_diag_matrix(tf, rf_list)

    # Make scenario matrix
    if scen_mtr == None:
        rf_name_list = map(rf_extern_id, rf_list)
        scen_mtr = FVaRTools.scenario_matrix(filename, nbr, rf_list)
    
    # Process scenarios
    true_nbr = len(scen_mtr)
    results = []
    for s in range(true_nbr):
        res = Numeric.dot(rf_deltas, scen_mtr[s]) + \
              0.5*Numeric.matrixmultiply(scen_mtr[s], Numeric.matrixmultiply(gamma_mtr, scen_mtr[s]))
        results.append(res)
    del(gamma_mtr)
    return results


#
#   Performs scenario revaluation according to chosen type   
#
#   Arguments:
#      tf         - A TradeFilter, Portfolio, Instrument or Trade
#      filename   - The name of the scenario file
#      nbr        - Number of scenarios
#      hist_fx    - FX on accumulated cash or not (1 or 0)
#      typ        - full, delta, gamma or gammacross
#      rfsh       - The name of a risk factor specification header
#      rf_list    - A list of risk factor specs
#      scen_mtr   - A scenario matrix
#
#   Returns a list of scenario results
#

def multi_scenario(tf,filename,nbr,hist_fx,typ,rfsh = None,rf_list = None,scen_mtr = None):

    if typ == 'full':
        res = full_reval_scenario(tf, filename, nbr, hist_fx)
    if typ == 'delta':
        res = delta_scenario(tf, filename, nbr, hist_fx, rfsh, rf_list, scen_mtr)
    if typ == 'gamma':
        res = delta_gamma_scenario(tf, filename, nbr, hist_fx, 'auto', rfsh, rf_list, scen_mtr)
    if typ == 'gammacross':
        res = delta_gamma_scenario(tf, filename, nbr, hist_fx, 'cross', rfsh, rf_list, scen_mtr)
    return res    

