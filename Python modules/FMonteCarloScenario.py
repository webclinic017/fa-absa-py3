""" ConsolidatedRisk:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FMonteCarloScenario - Monte Carlo scenario generator

(c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
	This module generates Monte Carlo scenarios for value at risk
	calculations. A multi-normal variate distribution is used.

NOTE
	Limited error handling

DATA-PREP	
	Make sure the FCS_DIR_RISK environment variable is set to point to a
        directory on your local hard drive or somewhere where you have read and write
        permissions.
        A proper risk factor setup in FRONT ARENA is needed, including risk factor
	volatility and correlation files.
	Python extension packages Numeric and LinearAlgebra is required.

REFERENCES
        Python website http://www.python.org
        FRONT ARENA knowledge base.
        Risk Metrics Technical document.
----------------------------------------------------------------------------"""

import ael, FVaRTools
try:
    from os import environ
    from random import gauss
    import math
    import Numeric, LinearAlgebra, string
    import_modules_ok = 1
except:
    import_modules_ok = 0
    
"""----------------------------------------------------------------------------
FUNCTION	
	monte_carlo_scenario()

DESCRIPTION
	Generates a monte carlo scenario file.
	
ARGUMENTS
    	rfsh  	    Table	   A RiskFactorSpecHeader
	filename    String  	   The name of the target file
	nbr	    String  	   Number of scenarios
	time	    String  	   Holding period in days
	antithetic   String  	   Antithetic scenarios or not, yes or no
	volscale    String  	   A scale factor to get daily volatilities from
	    	    	    	   the volatility data file, unscaled for
				   percentiles or percent. E.g. a Risk Metrics file
				   would need to be scaled with 1/165.
	
RETURNS
	Int
	
----------------------------------------------------------------------------"""

def monte_carlo_scenario(rfsh,filename,nbr,time,antithetic=0,volscale=1.0/165.0,*rest):

    if not import_modules_ok:
    	print 'Module import error'
    	return 0

    # Help functions for map()
    def specific_model(x):
        return math.exp(x)

    def rf_extern_id(rf):
        return rf.extern_id

    # Error Handling
    if not check_input_data(rfsh, filename, nbr, time, antithetic, volscale):
        return 0

    volscale = float(volscale)
    rfspechdrnbr = rfsh.rfspechdrnbr
    dt = math.sqrt(float(time))
    nbr = int(nbr)
    antithetic = string.lower(antithetic) == 'yes'

    # Get risk factors
    rf_list = ael.RiskFactorSpec.select('rfspechdrnbr = %i' % rfspechdrnbr).members()

    # Generate covariance matrix
    cov_mtr = FVaRTools.covariance_matrix(rf_list, volscale)

    # Singular value decomposition
    Q_T = FVaRTools.singular_value_decomp(cov_mtr)

    # Initialise the scenario file
    rf_names = map(rf_extern_id, rf_list)
    FVaRTools.init_scenario_file(filename, rf_names, nbr)

    # Antithetic
    if antithetic:
    	nbr = int(float(nbr)/2.0)

    # Generate scenarios and write to file
    size = len(rf_list)
    for i in range(nbr):
        epsilon = map(gauss, Numeric.zeros(size, 'i'), Numeric.ones(size, 'i'))
        epsilon = Numeric.array(epsilon)
        x = Numeric.matrixmultiply(Q_T, epsilon)
        scenario = map(specific_model, dt*x)
        FVaRTools.write_scenario(scenario, None)
	if antithetic:
	    FVaRTools.write_scenario(revert_scenario(scenario), None)
    	    
    FVaRTools.close_scenario_file()
    return 1

#
#   Check for errors in input data
#

def check_input_data(rfsh, filename, nbr, time, antithetic, volscale):

    if rfsh.record_type != 'RiskFactorSpecHeader':
        print 'Type Error, first argument must be a RiskFactorSpecHeader entity'
        return 0
	
    if ael.os_getenv('FCS_DIR_RISK') in (None, ''):
        print 'Environment variable FCS_DIR_RISK not properly set'
        return 0
    try:
        if int(nbr) <= 0:
            raise
    except:
        print 'Type Error, NumberOfScenarios must be a positive integer'
        return 0

    try:
        if float(time) <= 0.0:
            raise
    except:
        print 'Type Error, HoldingPeriod must be a positive float'
        return 0

    try:
        float(volscale)
    except:
        print 'Type Error, volscale must be a float'
        return 0
    try:
    	str(antithetic)
    except:
    	print 'Type Error, antithetic must be a string'
	return 0

    return 1

#
#  Revert the scenario
#

def revert_scenario(scenario):
    
    def pw(x, y):
    	return x**y
    
    return map(pw, scenario, -1.0*Numeric.ones(len(scenario), 'f'))
