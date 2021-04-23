import ael, acm, sets, csv

def undEquityIndex(ins):
    ''' Return a list of stocks making up an equity index.  
    If the index contains another index recursively extract elements from this index.
    If index contains another instrument type (eg. commodity) return an empty list. 
    '''
    
    undElements = []
    for c in ael.Instrument[ins].combination_links():
        if c.member_insaddr.instype == 'Stock':
            undElements.append(c.member_insaddr.insid)
        elif c.member_insaddr.instype == 'EquityIndex':
            temp = undEquityIndex(c.member_insaddr.insid)
            if len(temp):
                for t in temp:
                    undElements.append(t)
    return undElements

def maxDividendDate(i):
    ''' Return the maximum dividend date for the given instrument
    '''
    
    ins = ael.Instrument[i]
    max_day = ael.SMALL_DATE
    for d in ins.dividends():
        max_day = max(max_day, d.ex_div_day)
    return max_day

def numDivsPerYear(i):
    ''' If the given instrument has no dividend estimates then the the number of dividends per year are estimated 
    from the historical dividends.  This is done by counting the number of dividends in the maximum year before the 
    current year and assuming it will be the same for following years. 
    '''
    
    yearly_divs = {}
    divs_per_year = 1
    max_year = 0
    
    ins = ael.Instrument[i]
    divs = ins.dividends()
    
    if len(divs):
        for d in divs:
            year = int(d.day.to_string('%Y'))
            if year < int(ael.date_today().to_string('%Y')):
                max_year = max(max_year, year)
            
            if year in yearly_divs:
                yearly_divs[year] += 1
            else:
                yearly_divs[year] = 1
        
        if max_year == 0:
            divs_per_year = yearly_divs[year]
        else:
            divs_per_year = yearly_divs[max_year]
    
    return divs_per_year


def Exception_Report(save_file, filter_name):
    myDerivatives = ('Option', 'Future/Forward', 'EquitySwap', 'TotalReturnSwap')
    final_report = [['InsType', 'InsName', 'Ins ExpDate', 'Underlying Type', 'Underlying Name', 'Missing Index Underlying', 'Dividend Estimate Status', 'Portfolios']]
    exception_report = []
    
    # Set to store unique names of instruments in the given tradefilter (filter_name)
    myInstruments = sets.Set([])
    
    # Set to store unique names of underlying instruments
    undInstruments = sets.Set([])
    
    # Dictionary of dividend streams and maximum dividend estimate date
    div_est = {}
    
    # Populate the div_est dictionaries
    for cl in ael.Context['ACMB Global'].links():
        if cl.type == 'Dividend Stream':
            if cl.name not in div_est:
                max_date = ael.SMALL_DATE
                for est in ael.DividendStream[cl.name].estimates():
                    max_date = max(max_date, est.day)
                div_est[cl.name] = max_date
    
    # Create a set of instruments in the given trade filter that are derivatives, haven't expired and have stock or equity index as underlying
    try:
        for t in ael.TradeFilter[filter_name].trades():
            if t.insaddr.insid not in myInstruments:
                if t.status not in ('Void', 'Simulated'):
                    if t.insaddr.instype in myDerivatives:
                        if t.insaddr.und_instype in ('Stock', 'EquityIndex') and t.insaddr.exp_day > ael.date_today():
                            myInstruments.add(t.insaddr.insid)  
                            undInstruments.add(t.insaddr.und_insaddr.insid)
    except:
        func = acm.GetFunction('msgBox', 3)
        func("Error", "Error in accessing the trade filter " + filter_name, 0)
        raise
        
    # Dictionary of underlying instruments and maximum estimate date
    undIns_Estimates = {}
    
    # Dictionary of underlying instruments and number of dividends per year
    undIns_DivPerYear = {}
    
    # Populate the undIns_Estimates and undIns_DivPerYear dictionaries.  If there are no dividend estimates then use data from historical dividends.
    for i in undInstruments:
        ins = ael.Instrument[i]
        if ins.instype == 'Stock':
            if ins.insid not in undIns_Estimates:
                undIns_Estimates[ins.insid] = ael.SMALL_DATE
                undIns_DivPerYear[ins.insid] = 0
                for cl in ael.ContextLink.select('insaddr = ' + str(ins.insaddr)):
                    if cl.name in div_est:
                        if div_est[cl.name] > undIns_Estimates[ins.insid]:
                            undIns_Estimates[ins.insid] = div_est[cl.name]
                            undIns_DivPerYear[ins.insid] = ael.DividendStream[cl.name].div_per_year
                
            # If there are no dividend estimates get the maximum dividend date
            if undIns_Estimates[ins.insid] == ael.SMALL_DATE:
                undIns_Estimates[ins.insid] = maxDividendDate(ins.insid)
            
            # If the number of dividends per year was missing then estimate from historical dividends
            if undIns_DivPerYear[ins.insid] == 0:
                undIns_DivPerYear[ins.insid] = numDivsPerYear(ins.insid)
                        
        # instype == EquityIndex
        else:
            for s in undEquityIndex(i):
                stck = ael.Instrument[s]
                if stck.insid not in undIns_Estimates:
                    undIns_Estimates[stck.insid] = ael.SMALL_DATE
                    undIns_DivPerYear[stck.insid] = 0
                    for cl in ael.ContextLink.select('insaddr = ' + str(stck.insaddr)):
                        if cl.name in div_est:
                            undIns_Estimates[stck.insid] = max(undIns_Estimates[stck.insid], div_est[cl.name])
                            undIns_DivPerYear[stck.insid] = ael.DividendStream[cl.name].div_per_year
                            
                    # If there are no dividend estimates get the maximum dividend date
                    if undIns_Estimates[stck.insid] == ael.SMALL_DATE:
                        undIns_Estimates[stck.insid] = maxDividendDate(stck.insid)
            
                    # If the number of dividends per year was missing then estimate from historical dividends
                    if undIns_DivPerYear[stck.insid] == 0:
                        undIns_DivPerYear[stck.insid] = numDivsPerYear(stck.insid)
            
    # Generate data for the exception report
    for i in myInstruments:
        ins = ael.Instrument[i]
        
        if ins.und_insaddr.instype == 'Stock':
            num_divs = undIns_DivPerYear[ins.und_insaddr.insid]
            if ins.exp_day > undIns_Estimates[ins.und_insaddr.insid].add_months(12//num_divs).adjust_to_banking_day(ael.Instrument['ZAR']):
                row = [str(ins.instype), str(ins.insid), str(ins.exp_day), str(ins.und_insaddr.instype), str(ins.und_insaddr.insid), 'NA', 'Missing']
                exception_report.append(row)
                
        # instype == EquityIndex
        else:
            und_Stocks = undEquityIndex(ins.und_insaddr.insid)
            if len(und_Stocks):
                for s in und_Stocks:
                    stck = ael.Instrument[s]
                    num_divs = undIns_DivPerYear[stck.insid]
                    if ins.exp_day > undIns_Estimates[stck.insid].add_months(12//num_divs).adjust_to_banking_day(ael.Instrument['ZAR']):
                        row = [str(ins.instype), str(ins.insid), str(ins.exp_day), str(ins.und_insaddr.instype), str(ins.und_insaddr.insid), str(stck.insid), 'Missing']
                        exception_report.append(row)
    
    # Generate the final report
    for row in exception_report:
        ins = ael.Instrument[row[1]]
        ports = []
        for t in ins.trades():
            if t.status not in ('Void', 'Simulated'):
                if t.prfnbr.prfid not in ports:
                    ports.append(t.prfnbr.prfid)
        new_row = row
        new_row.extend(ports)
        final_report.append(new_row)
    
    # Print missing dividend exception report
    try:
        f = file(save_file, 'wb')
        c = csv.writer(f, dialect = 'excel')
        c.writerows(final_report)
        f.close()
    except IOError:
        func = acm.GetFunction('msgBox', 3)
        func("Warning", "Error in creating: " + save_file, 0)
        raise
    
ael_variables = [('save_file', 'Missing dividend report pathname', 'string', None, 'F:\\MissingDividends.csv'),
                ('filter_name', 'Trade Filter', 'string', None, 'Francois Henrion')]

def ael_main(ael_dict):
    Exception_Report(ael_dict["save_file"], ael_dict["filter_name"])

