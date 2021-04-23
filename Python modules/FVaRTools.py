""" ConsolidatedRisk:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FVaRTools - Help functions for VaR scenario generation in FRONT ARENA

(c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
	Help functions for value at risk scenario generation and processing. 

NOTE
	Limited error handling

DATA-PREP	
	Make sure the FCS_DIR_RISK environmental variable is set to point to a
        directory on your local hard drive or somewhere where you have read and write
        permissions.
        A proper risk factor setup in FRONT ARENA is needed.

REFERENCES
        Python website http://www.python.org
        FRONT ARENA knowledge base.
        Risk Metrics Technical document.
----------------------------------------------------------------------------"""

# Column delimiter in the scenario file
# Rare cases of instability when using <tab> ('\t')
COLUMN_DELIMITER = ','

def column_delimiter():
    return COLUMN_DELIMITER


import ael

try:
    import Numeric
except:
    print 'Warning, Numeric module not found'
try:
    import LinearAlgebra
except:
    print 'Warning, LinearAlgebra module not found'
    
try:
    from os import environ, remove, rename
    from os.path import exists
except:
    print 'Warning, Python extension module os not found'

try:
    import tempfile
except:
    print 'Warning, extension module tempfile not found'

try:    
    from math import sqrt, exp
except:
    print 'Warning, Python extension module math not found'
    
from string import replace, split

try:
    from random import gauss
except:
    print 'Warning, Python extension module random not found'





"""----------------------------------------------------------------------------
CLASS	
	Mem - A global memory used by scenario file functions
	
----------------------------------------------------------------------------"""

class Mem:
    def __init__(self):
        self.extern_id_max_len = None
        self.row_len = None
        self.cell_len = None  
        self.max_nbr = None
        self.scen_nbr = None
        self.file = None
        self.filename = None

#
# correlation_matrix()
# Creates a correlation matrix with use of ARENA function rf_correlation. 
# Arguments:
#		rf_list - a list of references RiskFactorSpec entities
# Returns:
# 		A correlation matrix as a Numeric array
#
# Usage
# 		mtr = correlation_matrix(rf_list)
#

def correlation_matrix(rf_list):

    error = 0
    size = len(rf_list)
    mtr = Numeric.zeros([size, size], 'f')
    for row in range(size):
        rfs1 = rf_list[row]
        for col in range(row+1):
            rfs2 =  rf_list[col]
            try:
                corr = rfs2.rf_correlation(rfs1)
            except:
                corr = 0.0
                error = 1
            mtr[col][row] = mtr[row][col] = corr
    if error:
        print 'rf_correlation failed, check Risk Factor Specification in Parameter Override'
    return mtr

#
# covariance_matrix()
# Creates a covariance matrix with use of ARENA function rf_covariance. 
# Arguments:
#		rf_list - a list of references RiskFactorSpec entities
#		volscale - a volatility scale factor
# Returns:
# 		A covariance matrix as a Numeric array
#
# Usage
# 		mtr = covariance_matrix(rf_list)
#


def covariance_matrix(rf_list,volscale = 1.0):

    error = 0
    size = len(rf_list)
    mtr = Numeric.zeros([size, size], 'f')
    for row in range(size):
        rfs1 = rf_list[row]
        for col in range(row+1):
            rfs2 =  rf_list[col]
            try:
                cov = rfs1.rf_covariance(rfs2)*(volscale**2.0)
            except:
                cov = 0.0
                error = 1
            mtr[col][row] = mtr[row][col] = cov
    if error:
        print 'rf_correlation failed, check Risk Factor Specification in Parameter Override'
    return mtr

#
# gamma_matrix()
# Creates a cross gamma matrix
# Arguments:
#		tf      - a TradeFilter, Portfolio, Trade or Instrument
#		rf_list - a list of references RiskFactorSpec entities
# Returns:
# 		A gamma matrix as a Numeric array
#
# Usage
# 		mtr = gamma_matrix(tf,rf_list)
#


def gamma_matrix(tf, rf_list):
    
    size = len(rf_list)
    mtr = Numeric.zeros([size, size], 'f')
    for row in range(size):
        rfs1 = rf_list[row]
        for col in range(row+1):
            rfs2 =  rf_list[col]
            res = rf_gamma(tf, rfs1, rfs2)
            mtr[col][row] = mtr[row][col] = res
    return mtr

#
# gamma_diag_matrix()
# Creates a gamma matrix with only diagonal elements
# Arguments:
#		tf      - a TradeFilter, Portfolio, Trade or Instrument
#		rf_list - a list of references RiskFactorSpec entities
# Returns:
# 		A gamma matrix as a Numeric array
#
# Usage
# 		mtr = gamma_diag_matrix(tf,rf_list)
#

def gamma_diag_matrix(tf, rf_list):
    size = len(rf_list)
    mtr = Numeric.zeros([size, size], 'f')
    for row in range(size):
        rfs = rf_list[row]
        res = rf_gamma(tf, rfs, rfs)
        mtr[row][row] = res
    return mtr

#
# rf_gamma()
# Calculates the risk factor gamma similar to the ARENA function rf_gamma()
# A work around for a bug in the ARENA function 
# Arguments:
#		tf      - a TradeFilter, Portfolio, Trade or Instrument
#		rfs1    - a risk factor specification
#		rfs2    - a risk factor specification
# Returns:
# 		Gamma as a float
#
# Usage
# 		res = rf_gamma(tf,rfs1,rfs2)
#

def rf_gamma(tf, rfs1, rfs2):

    # ARENA function rf_gamma() does not work properly
    if rfs1 == rfs2:
        res = (tf.rf_scenario(None, None, None, None, rfs1, 1.000002)- \
              2.0*tf.rf_scenario(None, None, None, None, rfs1, 1.000001))*10000.0*10000.0
    else:
        res = (tf.rf_scenario(None, None, None, None, rfs1, 1.000001, None, None, rfs2, 1.000001) - \
              tf.rf_scenario(None, None, None, None, rfs2, 1.000001) - \
              tf.rf_scenario(None, None, None, None, rfs1, 1.000001))*10000.0*10000.0
        
    return res


#
# singular_value_decomp()
# Performs a singular value decomposition on a matrix with the use of
# the LinearAlgebra function singular_value_decomposition
#
# Arguments:
#		mtr - a matrix as a Numeric array
# Returns:
# 		The decomposed matrix as a Numeric array
# Usage
# 		svd_mtr = singular_value_decomp(mtr)
#

def singular_value_decomp(mtr):

    svd_output = LinearAlgebra.singular_value_decomposition(mtr)
    V = svd_output[0]
    sv = svd_output[1]
    
    # Error handling if sv[i] negative and complex (have never happend yet)
    # Will be set to zero if it happens.
    
    sqrt_sv = []
    for i in range(0, len(sv)):
        if sv[i] >= 0.0:
            sqrt_sv.append(sqrt(sv[i]))
        else:
            sqrt_sv.append(0.0)
            print "Numerical Error in SVD", sv[i], "Assuming 0.0"
            
    sqrt_sv = Numeric.array(sqrt_sv)

    sqrt_diagonal_matrix = sqrt_sv * (1.0*Numeric.identity(len(sv)))
    return Numeric.matrixmultiply(V, sqrt_diagonal_matrix)

#
# get_scenario_matrix()
# Reads the scenario file and returns a matrix consisting of all scenarios as
# a Numeric array.
# Each row in the matrix consists of all scenario outcomes from one risk
# factor. The scenario outcomes are in percent
# This function assumes the risk factors are sorted alphabetically
# in the scenario file.
# To loop through the scenarios the matrix needs to be transposed.
#
# Arguments:
#		filename - the full path to the file
#		nbr - the number of scenarios to be read
# Returns:
#		A matrix as a Numeric array
# 	        
# Usage
# 		mtr = get_scenario_matrix(filename,nbr)
#

def get_scenario_matrix(filename,nbr,rf_list = None):

    nbr = int(nbr)
    
    def helpfunc(x):
        return 100.0*(float(x) - 1.0)

    cd = COLUMN_DELIMITER
    file = open(filename, 'r')
    result = {}
    line = file.readline()
    while line != '' and line != None:
        temp_list = split(line, cd)
        id = temp_list[0]
        if rf_list == None or id in rf_list:
            length = min(len(temp_list), nbr)
            temp_list = map(helpfunc, temp_list[1:2*length+1])
            for i in range(length):
                del(temp_list[i+1])
            result[id] = Numeric.array(temp_list)
        line = file.readline()
            
    return result

#
# scenario_matrix()
# For a list of risk factor ids reads a scenario matrix from a file.
# Each row in the matrix consists of all scenario outcomes from one risk
# factor. The scenario outcomes are in percent
#
# Arguments:
#		filename - the full path to the file
#	        nbr - the number of scenarios to be read
#               rf_list - a list of risk factor ids
# Returns:
#		A matrix as a Numeric array
# 	        
# Usage
# 		mtr = scenario_matrix(filename,nbr,rf_list)
#

def scenario_matrix(filename, nbr, rf_list):

    def rf_extern_id(rf):
        return rf.extern_id
    
    rf_name_list = map(rf_extern_id, rf_list)
    try:
        path = ael.os_getenv('FCS_DIR_RISK') + '/'
    except:
        print 'FCS_DIR_RISK not properly set'
        return Numeric.array([[]])
    
    scen_mtr_dict = get_scenario_matrix(path+filename, nbr, rf_name_list)
    # Default vector
    try:
    	sz = len(scen_mtr_dict[scen_mtr_dict.keys()[0]])
    except:
    	raise
    default = Numeric.zeros(sz, 'f')
    # Build matrix
    scen_mtr = []
    for id in rf_name_list:
        try:
            scen_mtr.append(scen_mtr_dict[id])
        except:
            print id, 'not found in scenario file. Using zero shifts'
            scen_mtr.append(default)
    scen_mtr = Numeric.transpose(scen_mtr)
    scen_mtr_dict = None
    del(scen_mtr_dict)
    return scen_mtr

#
# create_filter()
# Creates a virtual trade filter sorting out trades made in a
# certain instrument type. 
#
# Arguments:
#		tf - a TradeFilter or a Portfolio
#	        instype_list - a list of instrument types
#               excl - 1 or 0. If 1, the tradefilter will exclude all
#               trades in instype_list. If 0, the trade filter will
#               include all trades in instype_list.
# Returns:
#		A reference to a TradeFilter
# 	        
# Usage
# 		tf_new = create_filter(tf,instype_list)
#

def create_filter(tf,instype_list,excl = 0):

    if tf.record_type == 'Portfolio':
        name = tf.prfid
        tfnew = ael.TradeFilter.new()
        tfnew.set_query([('Or', '', 'Portfolio', 'equal to', name, '')])
        
    elif tf.record_type == 'TradeFilter':
        tfnew = tf.new()

    else:
        return None

    q = tfnew.get_query()
    date = ael.date_today().add_years(-40)
    q[0] = ('Or', q[0][1], q[0][2], q[0][3], q[0][4], q[0][5])
    q.reverse()
    q.append(('', '(', 'Acquire day', 'equal to', str(date), ''))
    q.reverse()
    q.append(('Or', '', 'Acquire day', 'equal to', str(date), ')'))
    if excl:
        comp = 'not equal to'
    else:
        comp = 'equal to'
        
    nbr = len(instype_list)
    for i in range(nbr):
        if i == 0:
            start = '('
            logic = 'And'
        else:
            start = ''
            if excl:
                logic = 'And'
            else:
                logic = 'Or'
        if i == nbr-1:
            end = ')'
        else:
            end = ''
        q.append((logic, start, 'Instrument.Type', comp, instype_list[i], end))
    
    tfnew.set_query(q)

    return tfnew


#
# migrate_files()
# Reads the contents from multiple files and stores in one.
#

def migrate_files(db_filename, ext_list):

    path = ael.os_getenv('FCS_DIR_RISK') + '/'
    file = open(path + db_filename, 'w')

    for ext in ext_list:

        e_file = open(path + db_filename + ext, 'r')
        line = e_file.readline()
        empty = 1
        while line != None and line != '':
            empty = 0
            file.write(line)
            line = e_file.readline()
        if not empty:
            file.write('\n')
        e_file.close()

    file.close()
    return 1

#
# get_rf_list()
# For ATLAS versions < 3.3.x:
# Returns all risk factor specs in the specified risk factor specification
# header.
# For ATLAS versions >= 3.4:
# Returns all risk factor specs the ael entity tf is sensitive to.
#
# Arguments:
#		tf - a Trade, TradeFilter, Instrument or Portfolio
#		rfsh - The name of a RiskFactorSpecificationHeader
# Returns:
# 		A list of RiskFactorSpecs
#

def get_rf_list(tf = None,rfsh = None):

    try:
        rf_list = tf.rf_list()
    except:
        rfsh = ael.RiskFactorSpecHeader[rfsh]
        hdrnbr = rfsh.rfspechdrnbr
        rf_list = ael.RiskFactorSpec.select('rfspechdrnbr = %i' % hdrnbr).members()

    return rf_list

#
# init_scenario_file()
# Initiates the scenario file. The file will be stored in the FCS_DIR_RISK
# directory
#
# Arguments:
#		filename - the name of the file
#		rf_list - a list of RiskFactorSpec external IDs
#		nr_of_scenarios - the number of scenarios that are to
#		be stored in the file
# Returns:
# 		0 or 1,
# 	        0 for failed and 1 for success
# Usage
# 		init_scenario_file(filename,rf_list,nr_of_scenarios)
#

def init_scenario_file(filename, rf_list, nr_of_scenarios):

    global mem

    if ael.os_getenv('FCS_DIR_RISK') not in (None, ''):
        filename = ael.os_getenv('FCS_DIR_RISK')+'/'+filename
    else:
        print 'FCS_DIR_RISK not properly set'
        return 0

    try:
        tempfile.template = "scenario.tmp"
        temp_file_name = tempfile.mktemp()
        file = open(temp_file_name, 'w')
        temp_file_name2 = tempfile.mktemp()
        temp_file2 = open(temp_file_name2, 'w')

    except IOError:
        print "Could not open temporary file"
	return 0

    cd = COLUMN_DELIMITER
    
    # Build framework for scenario file

    MAX_NUMBER_OF_DIGITS = 20
    extern_id_max_len = max(map(len, rf_list))
    file_cell = cd + ' '*MAX_NUMBER_OF_DIGITS + cd + ' '*MAX_NUMBER_OF_DIGITS
    cell_len = len(file_cell)
    file_row = file_cell * nr_of_scenarios + '\n'
    file.write('\n')
    cr = file.tell() - 1
    file.seek(0)
    row_len = len(file_row) + extern_id_max_len + cr

    # Build blank file
    
    for id in rf_list:
        file.write(id + ' ' * (extern_id_max_len - len(id)) + file_row)
  
    # Memorise file format
  
    mem = Mem()
    mem.extern_id_max_len = extern_id_max_len
    mem.row_len = row_len
    mem.cell_len = cell_len    
    mem.max_nbr = MAX_NUMBER_OF_DIGITS
    mem.scen_nbr = -1
    mem.file = file
    mem.temp_file2 = temp_file2
    mem.filename = filename
    mem.temp_file_name = temp_file_name
    mem.temp_file_name2 = temp_file_name2
    return 1

#
# write_scenario()
# Writes one scenario to the scenario file
#
# Arguments:
#		rel_scenario - a list or a Numeric array containing 
#		               the relative shifts for each risk factor.
#		abs_scenario - a list or a Numeric array containing 
#		               the absolute shifts for each risk factor.
# Returns:
# 		0 or 1,
# 	        0 for failed and 1 for success
# Usage
# 		write_scenario(rel_scenario,abs_scenario)
#

def write_scenario(rel_scenario,abs_scenario = None):

    global mem

    try:
        mem.scen_nbr = mem.scen_nbr + 1
    except:
        print 'Run init_scenario_file() before write_scenario()'
        return 0

    if (abs_scenario == None or len(abs_scenario) == 0) and \
       (rel_scenario == None or len(rel_scenario) == 0):
        print 'No scenario specified'
        return 0
    
    if abs_scenario == None or len(abs_scenario) == 0:
        abs_scenario = Numeric.zeros(len(rel_scenario), 'f')
    if rel_scenario == None or len(rel_scenario) == 0:
        rel_scenario = Numeric.ones(len(abs_scenario), 'f')

    size = len(rel_scenario)
    start_pos = mem.extern_id_max_len + 1 + mem.scen_nbr * mem.cell_len

    # Write scenario with relative shifts
    for row in range(size):
            mem.file.seek(start_pos + row * mem.row_len)
            mem.file.write(str(rel_scenario[row])[:mem.max_nbr])
            
    # Write scenario with absolute shifts
    for row in range(size):
            mem.file.seek(start_pos + row * mem.row_len + 1 + mem.max_nbr)
            mem.file.write(str(abs_scenario[row])[:mem.max_nbr])
    return 1

#
# close_scenario_file()
# Closes the temporary file and builds the scenario file
#
# Returns:
# 		0 or 1,
# 	        0 for failed and 1 for success
# Usage
# 		close_scenario_file()
#

def close_scenario_file():

    global mem

    try:
        mem.file.close()
    except:
        print 'File not open or already closed'
        return 0

    # Remove whitespace
    temp_file = open(mem.temp_file_name, 'r')
    temp_file2 = mem.temp_file2
    row = temp_file.readline()
    while row != '' and row != None:
        temp_file2.write(replace(row, ' ', ''))
        row = temp_file.readline()

    temp_file.close()
    temp_file2.close()

    try:
        if exists(mem.filename):
            if exists(mem.filename+'.bak'):
                remove(mem.filename+'.bak')
            rename(mem.filename, mem.filename+'.bak')
        rename(mem.temp_file_name2, mem.filename)
        
    except OSError:
    	print "Could not move destination file"
        print "The file is located at", mem.temp_file_name2
	return 0

    mem = None
    del(mem)
        
    return 1
    
