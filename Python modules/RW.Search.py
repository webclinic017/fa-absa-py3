#AEL module to search through AELs and ASQLs, generating a report of the results found.
#
#Input Variables:
#   Search For - String to search for, case sensitive.
#   Search In - Search AELs, ASQLs, or both.
#   No of Context Lines - Number of lines to return above and below matching line.
#   Save location - Location for html report.
#
#Requires Python installation on client PC.
#
#Russel Webber
#2003-11-21


# Updated - Zaakirah - for ASQL search textobject and not parameter

import ael, string, os

def check_AELs(search_string, context_lines):

    return_lines = []

    for t in ael.TextObject:

    	if t.type == 'AEL Module':
    
    	    text = t.get_text()
    	    
	    name = t.name

	    lineno = 0
	
    	    lines = text.splitlines()
	    
	    for line in lines:
	    
	    	lineno = lineno + 1
		
		if line.find(search_string) > 0:
	    	    
		    if context_lines > 0:

		    	for i in range(context_lines, 0, -1):
			
			    if lineno - i > 0:
			
			    	try:
			    	    return_lines.append([name, lineno - i, lines[lineno - i - 1], 0])
			    	except:
			    	    pass
		    
		    return_lines.append([name, lineno, line, 1])
		    
		    if context_lines > 0:

		    	for i in range(1, context_lines + 1):
			
			    if lineno + i < len(lines):
			
    			    	try:
			    	    return_lines.append([name, lineno + i, lines[lineno + i - 1], 0])
			    	except:
			    	    pass
			    
    return return_lines


def check_SQLs(search_string, context_lines):

    '''return_lines = []

    for p in ael.Parameter:

    	if p.type == 'SQL_QUESTION':
    
    	    name = p.name

    	    sql = 'SELECT data FROM parameter WHERE name = "%s"' % (p.name)
	
	    text = ael.dbsql(sql)[0][0][0]
    	
	    lineno = 0
	
    	    lines = text.splitlines()
	    
	    for line in lines:
	    
	    	lineno = lineno + 1
		
		if line.find(search_string) > 0:
	    	    
		    if context_lines > 0:

		    	for i in range(context_lines, 0, -1):
			
			    if lineno - i > 0:
			
			    	try:
			    	    return_lines.append([name, lineno - i, lines[lineno - i - 1], 0])
			    	except:
			    	    pass
		    
		    return_lines.append([name, lineno, line, 1])
		    
		    if context_lines > 0:

		    	for i in range(1, context_lines + 1):
			
			    if lineno + i < len(lines):
			
    			    	try:
			    	    return_lines.append([name, lineno + i, lines[lineno + i - 1], 0])
			    	except:
			    	    pass
			    
    return return_lines'''
    
    return_lines = []

    for t in ael.TextObject:

    	if t.type == 'SQL Query':
    
    	    text = t.get_text()
    	    
	    name = t.name

	    lineno = 0
	
    	    lines = text.splitlines()
	    
	    for line in lines:
	    
	    	lineno = lineno + 1
		
		if line.find(search_string) > 0:
	    	    
		    if context_lines > 0:

		    	for i in range(context_lines, 0, -1):
			
			    if lineno - i > 0:
			
			    	try:
			    	    return_lines.append([name, lineno - i, lines[lineno - i - 1], 0])
			    	except:
			    	    pass
		    
		    return_lines.append([name, lineno, line, 1])
		    
		    if context_lines > 0:

		    	for i in range(1, context_lines + 1):
			
			    if lineno + i < len(lines):
			
    			    	try:
			    	    return_lines.append([name, lineno + i, lines[lineno + i - 1], 0])
			    	except:
			    	    pass
			    
    return return_lines

		    
def table_element(s):

    return '<td>' + str(s) + '</td>\n'

def table_row(s):

    return '<tr>' + str(s) + '</tr>\n'
    
def table(s, align='"LEFT"', border='"1"', width='"50%"'):    

    return '<table align=' + align + ' border=' + border + ' width=' + width \
    	    + ' >' + str(s) + '</table>\n'

def emphasis(s):
    
    return '<STRONG>' + str(s) + '</STRONG>\n'
    
def small(s):

    return '<SMALL>' + str(s) + '</SMALL>\n'
    
def keyboard(s):

    return '<KBD>' + str(s) + '</KBD>\n'
    
def html(s, title=''):

    return '<HTML><HEAD><TITLE>' + str(title) + '</TITLE></HEAD><BODY>' \
    	    + str(s) + '</BODY></HTML>\n'

def heading(s):

    return  '<H1>' + str(s) + '</H1>\n'
    
def bold(s):

    return '<B>' + str(s) + '</B>'

ael_variables = [('search_string', 'Search For (case sensitive)', 'string', None, None),
    	     	('target', 'Search in', 'string', ['AEL', 'ASQL', 'Both'], None),
    	     	('context_lines', 'No of Context Lines', 'int', None, '0'),		
             	('save_file', 'Save Location', 'string', None, 'F:\\Report.html')]

def ael_main(ael_dict):

    tmpfile = file(ael_dict["save_file"], 'w')

    report = ''
    ael_report = ''
    asql_report = ''

    if ael_dict["target"] in ['ASQL', 'Both']:

  	asql_report = asql_report + \
    		    	    table_row(table_element(bold('ASQL Query Name')) \
	    		    + table_element(bold('Line')) \
		    	    + table_element(bold('Code')))
				    
	for line in check_SQLs(ael_dict["search_string"], ael_dict["context_lines"]):

  

	    if line[3]:

        	asql_report = asql_report + \
    		    		table_row(table_element(emphasis(line[0])) \
	    			+ table_element(emphasis(line[1])) \
		    		+ table_element(emphasis(keyboard(line[2]))))

	    else:

        	asql_report = asql_report + \
    		    		table_row(table_element(small(line[0])) \
	    			+ table_element(small(line[1])) \
		    		+ table_element(small(keyboard(line[2]))))


	asql_report = heading('ASQL Results') + \
	    table(asql_report, '"LEFT"', '"1"', '"100%"')
	
    if ael_dict["target"] in ['AEL', 'Both']:
        	   
    	ael_report = ael_report + \
    		    	    table_row(table_element(bold('AEL Module Name')) \
	    		    + table_element(bold('Line')) \
		    	    + table_element(bold('Code')))

	for line in check_AELs(ael_dict["search_string"], ael_dict["context_lines"]):

	    if line[3]:

        	ael_report = ael_report + \
    		    		table_row(table_element(emphasis(line[0])) \
	    			+ table_element(emphasis(line[1])) \
		    		+ table_element(emphasis(keyboard(line[2]))))

	    else:

        	ael_report = ael_report + \
    		    		table_row(table_element(small(line[0])) \
	    			+ table_element(small(line[1])) \
		    		+ table_element(small(keyboard(line[2]))))


	ael_report = heading('AEL Results')  + \
	    table(ael_report, '"LEFT"', '"1"', '"100%"')

    report = asql_report + '<BR clear="left"><P>' + ael_report

    report = html(report, 'Search Results - "' + ael_dict["search_string"] + '"')

    tmpfile.write(report)
    tmpfile.close()

    os.startfile(ael_dict["save_file"])
