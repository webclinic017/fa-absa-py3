"""-----------------------------------------------------------------------
MODULE
    SAEQ_Exception_Vols

DESCRIPTION
    Date                : 2011-05-19
    Purpose             : Compares the SAEQ_Exception_Report_Vols report in today's  AtlasEndOfDay folder with the previous business day's report. 
                          It then writes the differences to the  SAEQ_EXCEPTION_REPORT_VOL report in today's  AtlasEndOfDay folder.
    Department and Desk : Middle Office
    Requester           : Tendo Kiribakka
    Developer           : Herman Hoon
    CR Number           : 655300

HISTORY
================================================================================
Date       Change no Developer          Description
--------------------------------------------------------------------------------
2011-05-19 655300    Herman Hoon        Include all changes to Equity volatility surfaces that are identified with 'Skew','SSkew' postfixes

ENDDESCRIPTION
-----------------------------------------------------------------------"""

import ael, string, math, csv
from zak_funcs import write_file

# Rewritten - Zaakirah

PRODDIR = '//services/frontnt/BackOffice/Atlas-End-Of-Day/'

def read_file(name):
    f = open(name, 'rt')
    t = {}
    reader = csv.reader(f, delimiter=';')
    headers = reader.next()
    try:
        reader = csv.DictReader(f, fieldnames=headers, delimiter=';' )
    except:
        ael.log('Error reading file')
        
    for row in reader:
        if row['TrdNbr'] and row['Vol']:
            t[row['TrdNbr']] = [float(row['Vol']), row['Ins'], row['Port'], row['expiry'], row['acquirer'], row['vol surface']]
            
    f.close()
    return t

def main(diffList, *rest):
    results = [['TRADE', 'INSTRUMENT', 'PORTFOLIO', 'OLD VAL', 'NEW VAL', 'ABS DIFF', 'REL DIFF', 'EXPIRY', 'ACQUIRER', 'VOL SURFACE']]
    today = ael.date_today()
    yest = today.add_banking_day(ael.Instrument['ZAR'], -1)
 
    #filet = 'Y:/Jhb/FAReports/AtlasEndOfDay/2011-05-04/SAEQ_Exception_Report_Vols_110504.csv'
    #filey = 'Y:/Jhb/FAReports/AtlasEndOfDay/2011-05-03/SAEQ_Exception_Report_Vols_110503.csv'
    filet = PRODDIR + today.to_string('%Y-%m-%d') + '/SAEQ_Exception_Report_Vols_' + today.to_string('%y%m%d') + '.csv'
    filey = PRODDIR + yest.to_string('%Y-%m-%d') + '/SAEQ_Exception_Report_Vols_' + yest.to_string('%y%m%d') + '.csv'

    try:
        dicT = read_file(filet)
    except:
        ael.log('SAEQ_Exception_Vols  , ' + filet + '  missing file')
        return 'FAIL'
        
    try:
        dicY = read_file(filey)
    except:
        ael.log('SAEQ_Exception_Vols, ' + filey + '  missing file')
        return 'FAIL'
    
    for d in dicY.iteritems():
        try:
            new = dicT[d[0]]
            volSurface = new[5]
            
            for diff in diffList:
                checkValue = diff[0]
                if checkValue == 'Default':
                    absv = diff[1][0]
                    relv = diff[1][1]
                elif checkValue == 'Postfix':
                    values = diff[2]
                    postfix = volSurface.split('_')[-1]
                    if postfix in values:
                        absv = diff[1][0]
                        relv = diff[1][1]
                        
            if (abs(d[1][0] - new[0]) > absv ) and  abs(abs(d[1][0] - new[0])/d[1][0]) > relv:
                results.append([d[0], d[1][1], new[2], d[1][0], new[0], float(abs(d[1][0] - new[0])), abs(abs(d[1][0] - new[0])/d[1][0]), new[3], new[4], new[5], ])
        except:
            results.append([d[0], d[1][1], d[1][2], 'TRADE NO LONGER IN TRADE FILTER'])
    return results
    
     
r = main([['Default', [2.0, 0.1]], ['Postfix', [0, 0], ['Skew', 'SSkew']]])

prod = PRODDIR + ael.date_today().to_string('%Y-%m-%d') + '/'
if len(r) > 1:
    #write_file('f://SAEQ_EXCEPTION_REPORT_VOL.csv', r)
    write_file(prod + 'SAEQ_EXCEPTION_REPORT_VOL.csv', r)
else:
    ael.log('SAEQ_EXCEPTION_VOLS: NO AMENDMENTS TO VOLATILITY')

