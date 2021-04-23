""" ConsolidatedRisk:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FProcessScenarios - Scenario VaR processing module

(c) Copyright 2002 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
        This module handles results from simulation value at risk calculations.
        Step 1: Run process_scenarios(), process_per_instype() or
        process_per_instrument()
        Step 2: Run display_result() to get the value at risk figures

NOTE
	Limited error handling

DATA-PREP	
	Make sure the FCS_DIR_RISK environment variable is set to point to a
        directory on your local hard drive or somewhere where you have read and write
        permissions.
        A proper risk factor setup in FRONT ARENA is needed.
        AEL modules FVaR, FVaRTools and FCOMExport have to be installed in ATLAS.
        The Python modules Numeric and win32com must be installed in the Python path.

REFERENCES
        Python website http://www.python.org
        FRONT ARENA knowledge base.
        Risk Metrics Technical document.
----------------------------------------------------------------------------"""

EXP_WEIGHT_FACTOR = 0.98

import_modules_ok = 1

try:
    import ael,FVaR,FVaRTools
    import Numeric
except:
    import_modules_ok = 0

try:
    import copy
except:
    print 'Warning, Python module copy not found'
    import_modules_ok = 0
try:
    import FCOMexport
except:
    pass
try:
    import string
except:
    print 'Warning, Python module string not found'
    import_modules_ok = 0

try:
    import math
except:
    print 'Warning, Python module math not found'
    import_modules_ok = 0

try:
    from os import environ
except:
    pass

try:    
    COLUMN_DELIMITER = FVaRTools.column_delimiter()
except:
    pass



"""----------------------------------------------------------------------------
FUNCTION	
	process_scenarios - Process scenarios according to chosen method

DESCRIPTION
        Calculates a result for each scenario, stores them and exports
        distribution - and convergence graphs to Excel. 
	
ARGUMENTS
    	tf  	    Table	   A TradeFilter, Portfolio, Trade or Instrument
    	filename    String	   The name of the scenario file
    	nbr  	    String/Int	   Number of scenarios
    	hist_fx	    String/Int	   1 or 0. If 1, FX movements in acc cash will be
                                   taken into account
    	typ  	    String	   Processing method, either full, delta or gamma
    	rfsh  	    String	   A name of a Risk Factor Specification
	process     String  	   yes or no. If no, the stored result will be used
	export	    String  	   yes or no. If yes, results will be exported to Excel
	bins 	    String/Int     Number of histogram bins in the distribution
	
RETURNS
	Int, 1 for success, 0 for failure
	
----------------------------------------------------------------------------"""

def process_scenarios(tf,filename,nbr,hist_fx,typ = 'full',rfsh = None, \
                      process = 'yes',export = 'yes',bins = 30,*rest):

    global name,result
    
    if not import_modules_ok:
    	return 0

    # Error handling

    if not check_input_data(tf,filename,nbr,hist_fx,typ,rfsh,process,export,bins):
    	return 0

    export = string.lower(export) == 'yes'
    process = string.lower(process) == 'yes'
    hist_fx = string.lower(hist_fx) == 'yes'
    nbr = int(nbr)
    path = ael.os_getenv('FCS_DIR_RISK') + '/'
    bins = int(bins)

    name = get_name(tf)
    if name == None:
        return 0
    
    # Process scenarios if requested

    if process:
    	print 'Processing scenarios...'
        result = FVaR.multi_scenario(tf,filename,nbr,hist_fx,typ,rfsh)
        store_result(name,path,result)
    
    # else look up stored results
    else:
        result = get_result(name,path,nbr)
        if result == None:
            print 'No result stored for',name
            return 0
    
    # display results in excel if requested
    if export:
        export_to_excel(name,result,bins)
    
    print 'Done!'
    return 1


"""----------------------------------------------------------------------------
FUNCTION	
	display_result - Returns the result

DESCRIPTION
        Calculates a result for a certain confidence level according to a
        specified weighing method.
	
ARGUMENTS
    	tf  	    Table	   A TradeFilter, Portfolio, Trade or Instrument
    	conf_level  String/Int	   A confidence level
    	weight	    String	   'equal', 'exponential' or 'linear'
      	
RETURNS
	A float
	
----------------------------------------------------------------------------"""

def display_result(tf,conf_level,weight = None,*rest):

    global name, result
    
    if not import_modules_ok:
    	return 0

    try:
        cf = float(conf_level)
        if cf <0.0 or cf >100.0:
            raise
    except:
        print 'Type Error, confidence level must be a float [0,100]'
        return 0

    rname = get_name(tf)
    if rname == None:
        return 0
    try:
        if name != rname:
            raise
    except:
        print 'Run function process_scenarios() before display_results()'
        return 0
    
    return calculate_result(result,cf,weight)

"""----------------------------------------------------------------------------
FUNCTION	
	scenario_number

DESCRIPTION
        Returns the scenario number of a result
	
ARGUMENTS
    	tf  	    Table	   A TradeFilter, Portfolio, Trade or Instrument
    	scen_res    String/Float   The scenario result

RETURNS
	Int
	
----------------------------------------------------------------------------"""

def scenario_number(tf,scen_res,*rest):
    
    global name,result
    
    if not import_modules_ok:
    	return 0
    
    res = float(scen_res)
    
    rname = get_name(tf)
    if rname == None:
        return 0
    try:
        if name != rname:
            raise
    except:
    	return 0

    item = 0
    
    # Find res in the result vector
    # This part needs to be optimized
    
    try:
    	while abs(result[item] - res) > abs(res/1e10):
            item = item + 1
    except:
    	return 0
    
    return item + 1
    
    
"""----------------------------------------------------------------------------
FUNCTION	
	conditional_var

DESCRIPTION
        The conditional expected scenario given that a certain percentile
	has been broken.
	
ARGUMENTS
    	tf  	    Table	   A TradeFilter, Portfolio, Trade or Instrument
    	conf_level  String/Int	   A confidence level
    	weight	    String	   'equal', 'exponential' or 'linear'

RETURNS
	float
	
----------------------------------------------------------------------------"""

def conditional_var(tf,conf_level,weight = None,*rest):
    
    global name, result
    
    if not import_modules_ok:
    	return 0

    try:
        cf = float(conf_level)
        if cf <0.0 or cf >100.0:
            raise
    except:
        print 'Type Error, confidence level must be a float [0,100]'
        return 0

    rname = get_name(tf)
    if rname == None:
        return 0
    try:
        if name != rname:
            raise
    except:
        print 'Run function process_scenarios() before conditional_var()'
        return 0	
    
    return calculate_result(result,cf,weight,1)


"""----------------------------------------------------------------------------
FUNCTION	
	stats

DESCRIPTION
        Calculates simple statistical figures from the result vector.
	
ARGUMENTS
    	tf  	    Table	   A TradeFilter, Portfolio, Trade or Instrument
    	tp	    String	   'max', 'mean' or 'stddev'
	nbr 	    String/Int	   If tp = 'max', this argument specifies
	    	    	    	   the order.

RETURNS
	float
	
----------------------------------------------------------------------------"""
    
def stats(tf,tp,nbr,*rest):
    
    global name, result
    
    if not import_modules_ok:
    	return 0

    rname = get_name(tf)
    if rname == None:
        return 0
    try:
        if name != rname:
            raise
    except:
        print 'Run function process_scenarios() before stats()'
        return 0
    
    try:
    	tp = string.lower(tp)
    except:
    	print 'Type Error, tp must be a string'
	return 0.0
    
    if tp == 'max':
    	if nbr == None or int(nbr) == 1:
    	    return min(result)
	else:
	    res = copy.copy(result)
	    res.sort()
	    try:
	    	return res[int(nbr)-1]
	    except:
	    	return 0
    if tp == 'mean':
    	return Numeric.sum(result)/float(len(result))
    if tp == 'stddev':
    	sz = len(result)
	mean = Numeric.sum(result)/float(sz)
	res = 0.0
	for r in result:
	    res = res + (r-mean)**2.0
	return math.sqrt(res/(sz-1))
    
    return 0.0

#
#   From a vector of scenario results, this function returns a
#   value at risk number according to a certain confidence level
#   and weighting scheme
#
#   Arguments:
#      res        - result vector as a list
#      conf_level - confidence level as an integer
#      weight     - None, time or exponential
#      cond 	  - Conditional VaR number or not, 1 or 0
#
#   Returns a float
#

def calculate_result(res,conf_level,weight,cond = 0):

    sz = len(res)
    result = copy.copy(res)

    # Make weight vector
    weight_vector = Numeric.ones(sz,'f')
    if weight == None or string.lower(weight) == 'equal':
        result.sort()
	item = int(float(sz)*(1.0 - float(conf_level)/100.0))
	if cond:
	    item_cond = int(float(item)*0.5)
	    return abs(result[item_cond])
	else:
            return result[item]

    elif string.lower(weight) == 'exponential':

        def exponential(x):
            lambd = EXP_WEIGHT_FACTOR
            return (1-lambd)*lambd**(float(x)-1.0)
        weight_vector = Numeric.array(map(exponential,list(range(sz+1,1,-1))))

    elif string.lower(weight) == 'linear':

        def time_scaling(x,y):
	    fact = 2.0/(y+y**2.0)
            return (x+1)*fact
		
        weight_vector = Numeric.array(map(time_scaling,list(range(0,sz)),sz*Numeric.ones(sz,'f')))

    # Normalize weights
    weight_vector = weight_vector/Numeric.sum(weight_vector)
    # Sort results and weights
    nlist = (result,weight_vector)
    list = apply(map,(None,)+nlist)
    sortby = [0,1]
    nlist = map(lambda x,sortby=sortby: 
                map(lambda i,x=x: x[i],sortby) + [x],
                list)
    nlist.sort()
    listed = map(lambda l: l[-1], nlist)
    l = []
    for t in range(2):
        l.append(map(lambda x,t=t: x[t],listed))
    [result,weight_vector] = l

    # Find confidence level and result
    cv = 0.0
    item = 0
    while cv < 1.0 - float(conf_level)/100.0:
        cv = cv + weight_vector[item]
        item = item + 1
    
    if cond:
    	target_weight = 0.5*Numeric.sum(weight_vector[0:item])
    	cv = 0.0
	item = 0
    	while cv < target_weight:
	    cv = cv + weight_vector[item]
	    item = item + 1
	return abs(result[item-1])
    
    res = result[item-1]
    
    return res


#
#   Store the result in a file
#
#   Arguments:
#      name       - The name of the tradefilter or portfolio
#      path       - a path to where the file should be stored
#      result     - a vector with results as a list
#   

def store_result(name,path,result):

    filename = path+'__'+name+'.result'
    try:
        file = open(filename,'w')
        for r in result:
            file.write(str(r)+'\n')
        file.close()
    except:
        print 'Could not store result in file',filename

#
#   Extracts a result vector from a file
#
#   Arguments:
#      name       - The name of the tradefilter or portfolio
#      path       - a path to where the file should be stored
#      nbr        - nbr of scenarios
#
#   Returns a result vector as a list

def get_result(name,path,nbr):

    filename = path+'__'+name+'.result'
    try:
        result = []
        file = open(filename,'r')
        line = file.readline()
        i = 0
        while line != None and line != '' and i < nbr:
            i = i + 1
            line = string.split(line)
            result.append(float(line[0]))
            line = file.readline()
        file.close()
    except:
        result = None
    
    return result
                          
#
#   Calculates the convergence from vector of results.
#   No weighing is used
#
#   Arguments:
#      result     - a vector of results as a list
#      conf_int   - the confidence level
#
#   Returns a tuple with two lists:
#      - a range(0,size of series)
#      - the convergence vector
#

def convergence_series(result,conf_int):

    conv_series = []
    result = to_list(result)
    conf_int = float(conf_int)/100.0
    sz = len(result)
    for i in range(sz):
        res = result[0:i+1]
        res.sort()
        conv_series.append(abs(res[int(float(i)*(1.0-conf_int))]))

    return [list(range(sz)),conv_series]

#
#   Returns a unique id of an ael entity as a string
#
#   Arguments:
#      ael_entity - a reference to a TradeFilter, Portfolio, Trade or Ins
#

def get_name(ael_entity):

    name = None
    
    if ael_entity.record_type == 'TradeFilter':
        name = ael_entity.fltid

    if ael_entity.record_type == 'Portfolio':
        name = ael_entity.prfid

    if ael_entity.record_type == 'Trade':
        name = str(ael_entity.trdnbr)

    if ael_entity.record_type == 'Instrument':
        name = ael_entity.insid

    return name

#
#   Calculates a histogram from a result vector
#
#   Arguments:
#      result     - a vector of results as a list
#      bins       - the number of histogram bins
#
#   Returns a tuple with two lists:
#      - the histogram bins (x-axis)
#      - the bin value (y-axis)
#

def make_histogram(result,bins):

    res = copy.copy(result)

    res = to_list(res)
    res.sort()

    minv = res[0]
    maxv = res[-1]
    bins = int(float(len(result))*float(bins)/100.0)
    binrange = (maxv-minv)/bins
    idx = 0
    freq_list = []
    bin_list = []
    for b in range(bins):
    	count=0
    	while float(res[idx])<=minv+b*binrange:
	    count=count+1
	    idx=idx+1
	freq_list.append(count)
	bin_list.append(minv+b*binrange)
    data=[bin_list, freq_list]
    return data

#
#   Exports results to Excel
#
#   Arguments:
#      name   - the name of the session (normally the ael entity id)
#      result - the result vector as a list
#      bins   - the number of histogram bins
#
def export_to_excel(name,result,bins):
    
    print 'Exporting to Excel...'
    try:
    	data = make_histogram(result,bins)
	hist = 1
    except:
    	print 'Failed to create histogram'
	hist = 0
    title = 'Simulation histogram for '+name
    conv_title = '95th and 99th percentiles convergence graphs for '+name
    conv_title = conv_title + ' [equally weighted scenarios]'
    scen_title = 'Scenario results for '+name
    convdata = convergence_series(result,95)
    convdata.append(convergence_series(result,99)[1])
    legends = ['95th percentile','99th percentile']
    scenario_data = [list(range(len(result))),result]
 
    try:
    	FCOMexport.Export_To_Excel('', 3, scenario_data, scen_title, 'X', 'Y', None, None)
    	FCOMexport.Export_To_Excel('', 3, convdata, conv_title,'X','Y',legends,None)
    	if hist:
            FCOMexport.Export_To_Excel('', 2, data, title,'X','Y',None,None)
    except:
    	print 'Error accessing FCOMexport, possibly due to win32com module'



#
#   Converts a Numeric array to a Python list
#

def to_list(array):
    ret = []
    for i in array:
        ret.append(i)
    return ret
    
    
#
#   Error handling
#

def check_input_data(tf,filename,nbr,hist_fx,typ,rfsh,process,export,bins):

    if tf.record_type not in ('TradeFilter','Portfolio','Instrument','Trade'):
        print 'Type Error, first argument must be an ael entity of type'
	print 'TradeFilter, Portfolio, Instrument or Trade'
        return 0
    
    try:
        foo = string.lower(process)
	if foo not in ('yes','no'):
	    raise
        del foo
    except:
        print 'Type Error, process must be yes or no'
        return 0
    
    try:
        if int(nbr) < 1:
	    raise
    except:
        print 'Type Error, NumberOFScenarios must be a positive integer'
        return 0
    
    if string.lower(process) == 'yes':
   
    	path = ael.os_getenv('FCS_DIR_RISK') + '/'
	try:
	    file = open(path+filename,'r')
	except:
	    print 'File',path+filename,'not found'
	    return 0
	line = file.readline()
	line = string.split(line,COLUMN_DELIMITER)
	scenarios = int(float(len(line))/2.0)
	if scenarios < int(nbr):
	    print 'Not enough scenarios in scenario file'
	    print 'Found',scenarios,', requested',nbr
	    if scenarios == 0:
	    	print 'Column delimiter is set to \''+COLUMN_DELIMITER+'\''
	    return 0  

    try:
        foo = string.lower(hist_fx)
	if foo not in ('yes','no'):
	    raise
        del foo
    except:
        print 'Type Error, AccumulatedCash must be yes or no'
        return 0
    
    try:
        foo = string.lower(export)
	if foo not in ('yes','no'):
	    raise
        del foo
    except:
        print 'Type Error, export must be yes or no'
        return 0

    try:
        if int(bins) < 1:
            raise
    except:
        print 'Type Error, bins must be a positive integer'
        return 0
    try:
    	if string.lower(typ) not in ('full','delta','gamma','gammacross'):
	    raise
    except:
    	print 'Type Error, revaluation type must be either of full, delta, gamma or gammacross'
	return 0

    return 1
