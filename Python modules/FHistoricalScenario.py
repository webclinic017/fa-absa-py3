""" ConsolidatedRisk:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FHistoricalScenario - Historical scenario generator

(c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
	This module generates historical scenarios from time series
        of risk factor values. This module also contains functions for
	manipulating risk factor time series.

NOTE
	Limited error handling

DATA-PREP	
	Make sure the FCS_DIR_RISK environment variable is set to point to a
        directory on your local hard drive or somewhere where you have read and write
        permissions.
        A proper risk factor setup in FRONT ARENA is needed.
        Daily saved risk factor values are required.

REFERENCES
        Python website http://www.python.org
        FRONT ARENA knowledge base.
        Risk Metrics Technical document.
----------------------------------------------------------------------------"""

import_modules_ok = 1

try:
    import ael, FVaRTools
except:
    print 'FVaRTools not found'
    import_modules_ok = 0
try:
    from os import environ, remove, rename
    from string import split, lower
    
except: 
    import_modules_ok = 0


COLUMN_DELIMITER = FVaRTools.column_delimiter()

#
#  Check input data for errors
#

def check_input_data(tss, filename, nbr, calendar, time, end_day, overlapping, \
                     antithetic, rfsh):

    try:
        if tss.record_type != 'TimeSeriesSpec':
            raise
    except:
        print 'Type Error, first argument must be a TimeSeriesSpec entity'
        return 0

    try:
        if int(nbr) < 1:
	    raise
        
    except:
        print 'Type Error, NumberOfScenarios must be a positive integer'
        return 0

    if ael.Calendar[calendar] == None:
        print 'Type Error, calendar', calendar, 'not found'
        return 0
    try:
        if float(time) < 0.0:
            raise
    except:
        print 'Type Error, TimeStep must be a float'
        return 0

    try:
        if end_day != 'TODAY':
            foo = ael.date(end_day)
            del foo
    except:
        print 'Type Error, input parameter LastDayofSeries not a date'
        return 0

    try:
        foo = lower(overlapping)
        del foo
    except:
        print 'Type Error, input variable overlapping must be \'yes\' or \'no\''
        return 0
        
    try:
        foo = lower(antithetic)
        del foo
    except:
        print 'Type Error, input variable antithetic must be \'yes\' or \'no\''
        return 0
    
    try:
    	path = ael.os_getenv('FCS_DIR_RISK') + '/'
	filep = open(filename, 'w')
	filep.close()
    except:
    	print 'Could not open destination file'
	print 'Check filename and FCS_DIR_RISK'
        
    
    return 1

"""----------------------------------------------------------------------------
FUNCTION	
	hist_scenario()

DESCRIPTION
	Generates historical scenarios from risk factor time series.
	
ARGUMENTS
    	tss  	    Table	   A TimeSeriesSpec
	filename    String  	   The name of the target file
    	nbr  	    Int 	   Number of scenarios
    	calendar    String	   The name of a Calendar
    	time  	    Float	   Holding period in days
    	end_day	    String	   Last day in time series
    	overlapping String	   yes or no
    	antithetic  String	   yes or no
    	scale  	    String	   yes or no. Scale for historical volatility
	volscale    Float	   Volatility scale factor
        
RETURNS
	1 for success, 0 for failure
	
----------------------------------------------------------------------------"""

def hist_scenario(tss,
    	    	filename,
		nbr,
		calendar,
		time = 1.0,
		end_day = 'TODAY',
		overlapping='no', 
                antithetic='no',
		rfsh = None,
		*rest):

    # Error Handling
    if not import_modules_ok:
    	print 'Module import error'
    	return 0
    if not check_input_data(tss, filename, nbr, calendar, time, end_day, \
                            overlapping, antithetic, rfsh):
        return 0
    volscale = 0.0
    # Beta functionality - not used
    scale_for_volatility = 'no'
    antithetic = lower(antithetic) == 'yes'
    overlapping = lower(overlapping) == 'yes'
    scale_for_volatility = lower(scale_for_volatility) == 'yes'
    
    try:
    	rfsh = ael.RiskFactorSpecHeader[rfsh]
    except:
    	rfsh = None
        
    time = float(time)
    calendar = ael.Calendar[calendar]
    nbr = int(nbr)
    nr_of_scenarios = nbr
    if end_day == 'TODAY':
        end_day = ael.date_today()
    else:
        end_day = ael.date(end_day)
    cd = COLUMN_DELIMITER
    
    # Max available data
    max_nbr = find_maximum_nbr(tss, end_day, calendar)

    if antithetic:
        nbr = nbr / 2 
    
    if overlapping:
        required_nbr = nbr + time - 1
    else:
        required_nbr = nbr * time 
    if max_nbr < required_nbr:
        print 'Not enough data in time series table'
        print 'Need', required_nbr, 'data samples, found', max_nbr
        return 0

    # Collect all dates to use in simulation in a list
    delta_t = -time
    if not overlapping:
        inc = -time
    else:
        inc = -1
	
    dates = create_date_list(nbr, end_day, inc, delta_t, calendar)

    # Make list of available external ids
    
    if rfsh != None:
    	def extern_id(rf):
	    return rf.extern_id
    	hdrnbr = rfsh.rfspechdrnbr
        rf_aval_list = ael.RiskFactorSpec.select('rfspechdrnbr = %i' % hdrnbr).members()
    	rf_aval_list = map(extern_id, rf_aval_list)
    else:
    	print 'RFSpecification not found'
	return 0

    # Historical rf values as a dictionary of dictionaries.
    # First key is extern_id, second key is date, value is rf value
    
    rfs_dict = {}
    rf_dict = rf_ts_values(tss, dates, rfsh, rf_aval_list, rfs_dict)

    ## Traverse the risk factors and calculate a shift for each date
    ## Write the result to a file
    rf_list = rf_dict.keys()

    # Open scenario file
    path = ael.os_getenv('FCS_DIR_RISK') + '/'
    target = path + filename
    file = open(target, 'w')
    missing = open(target+'_missing', 'w')
    missing.write('*External ID,Day 1,Day 2,\n')
    for rf in rf_dict.keys():
        prev = 1.0
        scen = rf
        for s in range(nbr):
            notfound = 0
            val_day1 = dates[s*2]
            val_day2 = dates[s*2+1]
            if rf_dict[rf].has_key(val_day1):
                val1 = rf_dict[rf][val_day1]
            else:
                notfound = 1
            if rf_dict[rf].has_key(val_day2):
                val2 = rf_dict[rf][val_day2]
            else:
                notfound = 1

            # Insert support for missing data here
            if notfound or val1 == 0.0:
                missing.write(rf+cd+str(val_day1)+cd+str(val_day2)+'\n')
                shift = prev # Last calculated shift
            else:
                shift = val2/val1
            scen = scen + cd + str(shift) + cd + '0'
            if antithetic:
                scen = scen + cd + str(1.0/shift) + cd + '0'
            prev = shift
        file.write(scen+'\n')
    missing.close()
    file.close()

    if scale_for_volatility:
        print 'Scaling for historical volatilities...'
        if not scale_scenario_file(target, rfs_dict, volscale):
            return 0
    
    return 1

#
#   rf_ts_values()
#
#   Returns a dictionary of dictionaries where 
#   first key is risk factor id, second key is date
#   and value is risk factor value.
#

def rf_ts_values(tss, dates, rfsh, rf_aval_list, rfs_dict):
    
    # Historical rf values as a dictionary of dictionaries.
    # First key is extern_id, second key is date, value is rf value
    rf_dict = {}
    tss_specnbr = tss.specnbr
    ts_list = ael.TimeSeries.select('ts_specnbr = %i' % tss_specnbr)
    for ts in ts_list:
        if ts.day.to_string() in dates:
            try:
                rfs = ael.RiskFactorSpec[ts.recaddr]
                id = rfs.extern_id 
		if rfsh == None or id in rf_aval_list:
                    rfs_dict[id] = rfs
                    if not rf_dict.has_key(id):
                    	rf_dict[id] = {}
                    rf_dict[id][`ts.day`] = ts.value
            except:
                pass
    ts_list = None
    del(ts_list)
    return rf_dict


def find_maximum_nbr(tss, date, calendar):

    # Find the number of banking days between the day when the first
    # data were saved and today. This assumes that data has been collected
    # on a daily basis.

    first_date = date
    for ts in ael.TimeSeries:
        if ts.ts_specnbr == tss:
            first_date = min(first_date, ts.day)
    i = 0
    while not date.add_banking_day(calendar, -i) <= first_date:
        i = i + 1
    return i

"""----------------------------------------------------------------------------
FUNCTION	
	save_time_series()

DESCRIPTION
	Saves risk factor values in the time series table
	
ARGUMENTS
    	rfsh  	    Table	   A RiskFactorSpecHeader
    	tss_name    String	   The name of a TimeSeriesSpec
    	convert	    String	   'yes' or 'no'. Convert to instrument ccy or not
	
RETURNS
	1 for success, 0 for failure
	
----------------------------------------------------------------------------"""

def save_time_series(rfsh, tss_field_name, convert = 'yes', *rest):

       
    if not import_modules_ok:
    	print 'Module import error'
    	return 0

    try:
    	convert = lower(convert) != 'no'
    except:
    	convert = 0
    
    try:
        if rfsh.record_type != 'RiskFactorSpecHeader':
            raise
    except:
        print 'Type Error, first argument must be a RiskFactorSpecHeader entity'
        return 0

    tss = ael.TimeSeriesSpec[tss_field_name]

    if tss == None:
        print 'No TimeSeriesSpec named "' + tss_field_name + \
              '" exists. Creating new.'
        tss = ael.TimeSeriesSpec.new()
        tss.field_name = tss_field_name
        tss.rec_type = 'RiskFactorSpec'
        tss.description = 'Daily saved rf_value for historical VaR'
        tss.commit()
    else:
    	try:
    	    specnbr = tss.specnbr
    	    ts_list = ael.TimeSeries.select('ts_specnbr = %i' % specnbr)
	    for ts in ts_list:
    	    	try:
	    	    rf_test = ael.RiskFactorSpec[ts.recaddr]
	    	    if rf_test.rfspechdrnbr != rfsh:
	    	    	print tss.field_name, 'uses RFSpecification', rf_test.rfspechdrnbr.rfspecid
	    	    	print 'Not', rfsh_name
	    	    	return 0
		    else:
		    	break
	    	except:
	    	    pass
	    ts_list = None
	    del(ts_list)
    	except:
    	    print 'Could not complete task, time series corrupt'
	    print 'Possibly due to deleted risk factors'
	    return 0

    ## Find max run_no from existing series
    today = ael.date_today()
    runnbr = 0
    for a in ael.TimeSeries:
        nr = int(a.run_no)
        if a.ts_specnbr == tss and a.day == today:
            runnbr = max(nr, runnbr)
    runnbr = runnbr + 1
    hdrnbr = rfsh.rfspechdrnbr
    rf_list = ael.RiskFactorSpec.select('rfspechdrnbr = %i' % hdrnbr) 
    print 'Saving data...'
    for rfs in rf_list:
        if convert:
            value = 0.0
            # Find value in instrument ccy
            for rfm in ael.RiskFactorMember:
                if rfm.rfgnbr == rfs.rfgnbr:
                    factor = 1.0
                    if rfm.rfgtype == 'Equity' or rfm.rfgtype == 'Commodity':
                        curr = rfm.insaddr.curr
                        acc_curr = ael.used_acc_curr()
                        fxrate = curr.used_price(None, acc_curr)
                        if fxrate != 0.0:
                            factor = fxrate
                    else:
                        value = rfs.rf_value()
                    value = rfs.rf_value()/factor
                    break
        else:
            value = rfs.rf_value()

        if value < 1.e-6:
            print "Zero value for " + rfs.extern_id + \
                  ". Please check Price Link Definition."
        ts_rf_list = rfs.time_series()
        found = 0
        for ts_temp in ts_rf_list:
            if ts_temp.day == today and ts_temp.ts_specnbr == tss:
                ts = ts_temp.clone()
                found = 1
                break
        if not found:
            ts = ael.TimeSeries.new()
            ts.run_no = runnbr
            
        ts.recaddr = rfs.rfspecnbr
        ts.ts_specnbr = tss.specnbr
        ts.day = today
        ts.value = value
        ts.commit()
    print 'Done!'
    return 1

"""----------------------------------------------------------------------------
FUNCTION	
	export_time_series()

DESCRIPTION
	Exports selected time series for risk factors to a text file
	
ARGUMENTS
    	tss 	    Table	   A TimeSeriesSpec entity
    	extern_id   String	   A risk factor external ID
    	filename    String	   The name of the output file
    	go	    None/String	   None or a string. If None, the function will add
	    	    	    	   a risk factor to the export list. If a string,
				   the function will try to export the time series.
	calendar    String  	   The name of a calendar
	start_day   String  	   A date as a string
	end_day     String  	   A date as a string
	
RETURNS
	1 for success, 0 for failure
	
----------------------------------------------------------------------------"""

def export_time_series(tss,extern_id,filename,go,calendar,start_day,end_day,*rest):
    
    if not import_modules_ok:
    	print 'Module import error'
    	return 0
    
    global id_list
    
    if go != None:

        
	# Column delimiter <tab> to match Excel
	cd = '\t'
        
	try:
            path = ael.os_getenv('FCS_DIR_RISK') + '/'
	except:
	    print 'Environment variable FCS_DIR_RISK not properly set'
	    return 0
	    
    	print 'Writing file'
	calendar = ael.Calendar[calendar]
	if end_day == 'TODAY':
	    end_day = ael.date_today()
	else:
	    try:
	    	end_day = ael.date(end_day)
		end_day = end_day.adjust_to_banking_day(calendar)
	    except:
	    	print end_day, 'not a valid date format'
		return 0
	try:
	    start_day = ael.date(start_day)
	except:
	    print start_day, 'not a valid date format'
	    return 0
	start_day = start_day.adjust_to_banking_day(calendar, 'Preceding')

	inc = -1
	delta_t = -1
	dates = create_date_list(None, end_day, inc, delta_t, calendar, start_day)
	
	for i in range(len(dates)/2-1):
	    del(dates[i+1])
	
	rfs_dict = {}
        rf_dict = rf_ts_values(tss, dates, None, id_list, rfs_dict)

	## Export to file

        # Build Header
        hdr = ' '
        for rf in id_list:
            hdr = hdr + cd + rf
        
        try:
	    file = open(path+filename, 'w')
	except:
	    print 'Could not open', path+filename
	    return 0
	    
        file.write(hdr + '\n')

        for d in dates:
            row = d
            for id in id_list:
                val = ''
                if rf_dict.has_key(id):
                    ts_dict = rf_dict[id]
                    if ts_dict.has_key(d):
                        val = ts_dict[d]
                    
                    
                row = row + cd + str(val)
            file.write(row+'\n')
        file.close()
	
	id_list = []
	print 'File created'
	return 1
    
    try:
    	foo = id_list
	del foo
    except:
    	id_list = []
    
    if extern_id not in id_list:
    	id_list.append(extern_id)
    
    id_list.sort()
    return 1
    
"""----------------------------------------------------------------------------
FUNCTION	
	import_time_series()

DESCRIPTION
	Imports risk factor time series data from a text file
	
ARGUMENTS
    	tss 	    Table	   A TimeSeriesSpec entity
    	filename    String	   The name of the data file
	rfsh_name   String  	   The name of a RiskFactorSpecHeader
	
RETURNS
	1 for success, 0 for failure
	
----------------------------------------------------------------------------"""
    
def import_time_series(tss,filename,rfsh_name,*rest):


    if not import_modules_ok:
    	print 'Module import error'
    	return 0
    
    # Column delimiter <tab> to match Excel
    cd = '\t'
    
    try:
    	path = ael.os_getenv('FCS_DIR_RISK') + '/'
    except:
    	print 'Environment variable FCS_DIR_RISK not properly set'
	return 0
	
    try:
    	rfsh = ael.RiskFactorSpecHeader[rfsh_name]
	if rfsh == None:
	    raise
    except:
    	print rfsh_name, 'not found in database'
	return 0
    
    try:
    	file = open(path+filename, 'r')
    except:
    	print 'Could not open file', path+filename
	return 0
    
    # Check if time series uses the same header
    
    try:
    	specnbr = tss.specnbr
    	ts_list = ael.TimeSeries.select('ts_specnbr = %i' % specnbr)
	for ts in ts_list:
    	    try:
	    	rf_test = ael.RiskFactorSpec[ts.recaddr]
	    	if rf_test.rfspechdrnbr != rfsh:
	    	    print tss.field_name, 'uses RFSpecification', rf_test.rfspechdrnbr.rfspecid
	    	    print 'Not', rfsh_name
	    	    return 0
		else:
		    break
	    except:
	    	pass
	ts_list = None
	del(ts_list)
    except:
    	print 'Could not complete task, time series corrupt'
	print 'Possibly due to deleted risk factors'
	return 0

    # Read file header
    
    hdr = file.readline()
    hdr = hdr[0:len(hdr)-1]
    hdr = split(hdr, cd)
    
    if hdr[0] == '' or hdr[0] == ' ':
    	hdr = hdr[1:len(hdr)]
    
    # Make list of available risk factors
    
    rf_db_list = FVaRTools.get_rf_list(None, rfsh_name)
    rf_dict = {}
    for rf in rf_db_list:
    	rf_dict[rf.extern_id] = rf
   
    id_list = []
    id_dict = {}
    for id in hdr:
    	if id != '':
    	    if id not in rf_dict.keys():
	    	print 'Risk factor', id, 'not found in RFSpecification', rfsh_name
	    else:
	    	id_dict[id] = rf_dict[id]
	    	id_list.append(id)
    
    
    # Read file and sort in dictionary
    
    file_data = {}
    line = file.readline()
    while line != None and line != '':
    	line = split(line, cd)
	date = line[0]
	for i in range(1, len(hdr)+1):
	    rf = hdr[i-1]
	    if rf in id_list:
	    	try:	    	
	    	    if line[i] not in (None, '', ' '):
		    
	    	    	if file_data.has_key(rf):
	    	    	    temp_dict = file_data[rf]
		    	else:
		    	    temp_dict = {}
		    	temp_dict[date] = float(line[i])
		    	file_data[rf] = temp_dict
		except:
		    pass
	line = file.readline()
    
    # Add/update time series
    
    for id in file_data.keys():
    	date_dict = file_data[id]
	rf = id_dict[id]
	ts_list = rf.time_series()
	for ts in ts_list:
	    if ts.ts_specnbr == tss:
	    	day = ts.day.to_string()
	    	if day in date_dict.keys():
	    	    ts_clone = ts.clone()
		    ts_clone.value = date_dict[day]
		    ts_clone.commit()
		    del(date_dict[day])
    	for day in date_dict.keys():
	    ts = ael.TimeSeries.new()
	    ts.run_no = 0
	    ts.ts_specnbr = tss
	    try:
	    	ts.day = ael.date(day)
	    except:
	    	print 'Invalid date format', day
		return 0
	    ts.recaddr = rf.rfspecnbr
	    ts.value = date_dict[day]
	    ts.commit()
    
    return 1

"""----------------------------------------------------------------------------
FUNCTION	
	delete_time_series()

DESCRIPTION
	Imports risk factor time series data from a text file
	
ARGUMENTS
    	tss 	    Table	   A TimeSeriesSpec entity
    	extern_id   String	   The name extern_id of a RiskFactorSpec
	start_day   String  	   The first day of the series to delete
	end_day     String  	   The last day of the series to delete
	rfsh	    String  	   The name of a RiskFactorSpecHeader
	
RETURNS
	1 for success, 0 for failure
	
----------------------------------------------------------------------------"""

def delete_time_series(tss,extern_id,start_day,end_day,rfsh = None,*rest):
    
    ael.poll()
     
    ts_sel = []
    try:
    	rfsh = ael.RiskFactorSpecHeader[rfsh]
    except:
    	rfsh = None
	
    if rfsh == None:
    	specnbr = tss.specnbr
    	ts_list = ael.TimeSeries.select('ts_specnbr = %i' % specnbr)
    	for ts in ts_list:
	    try:
	    	if ael.RiskFactorSpec[ts.recaddr].extern_id == extern_id:
	    	    ts_sel.append(ts)
	    except:
	    	pass
    else:
    	hdrnbr = rfsh.rfspechdrnbr
    	rfs_list = ael.RiskFactorSpec.select('rfspechdrnbr = %i' % hdrnbr)
	rfs = None
	for rf in rfs_list:
	    if rf.extern_id == extern_id:
	    	rfs = rf
		break
	    	
	if rfs == None:
	    return 0
	
	ts_list = rfs.time_series()
	for ts in ts_list:
	    if ts.ts_specnbr == tss:
	    	ts_sel.append(ts)
    
    try:
    	start_day = ael.date(start_day)
	if start_day == None:
	    raise
    except:
    	start_day = ael.date_today().add_years(-100)
    
    try:
    	end_day = ael.date(end_day)
	if end_day == None:
	    raise
    except:
    	end_day = ael.date_today()

    records = 0
    for ts in ts_sel:
    	if ts.day >= start_day and ts.day <= end_day:
	    try:
	    	ts.delete()
		print 'Deleted', extern_id, ts.day
		records = records + 1
    	    except:
	    	print 'Could not delete', extern_id, ts.day 
    if records > 0:
    	print 'Deleted', records, 'records for', extern_id, '\n\n'
        
	    
    return 1

    

#
#   create_date_list()
#
#   Creates a list of dates
#

def create_date_list(nbr,end_day,inc,delta_t,calendar,start_day = None):
    
    dates = []
    baseDate = end_day
    if start_day == None:
    	for i in range(nbr):
       	    prevDate2 = baseDate.add_banking_day(calendar, i*inc)
       	    prevDate1 = prevDate2.add_banking_day(calendar, delta_t)
       	    dates.insert(0, prevDate2.to_string())
       	    dates.insert(0, prevDate1.to_string())
    else:
    	i = 0
	prevDate1 = baseDate
    	while prevDate1.days_between(start_day) < 0:
	    prevDate2 = baseDate.add_banking_day(calendar, i*inc)
       	    prevDate1 = prevDate2.add_banking_day(calendar, delta_t)
       	    dates.insert(0, prevDate2.to_string())
       	    dates.insert(0, prevDate1.to_string())
	    i = i + 1
	    
    return dates
