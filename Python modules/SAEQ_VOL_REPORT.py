import FPortfolioComparison, acm, csv, ael

def compare_reports(file1, file2, resultfile):
    diff_result = FPortfolioComparison.diff(file1, file2, "Output", 2, 0.1)
    print diff_result
    list1 = [['PORTFOLIO', 'INSTRUMENT', 'COLUMN', 'BEFORE', 'AFTER', 'ABS DIFFERENCE']]
    for (column, diff_lists) in diff_result.iteritems():
        if column == 'Vola':
            for diff_list in diff_lists:
                
                l0 = []
                s0 = diff_list[0].split('^')
                l0.append(s0[1])
                #if len(s0) > 1:
                #    l0.append(s0[1])
                #else:
                #    l0.append('Portfolio Summary')
                l0.append(column)
                l0.append(diff_list[4])
                l0.append(diff_list[3])
                l0.append(diff_list[1])
                list1.append(l0)
        
    print list1
    write_file(resultfile, list1)
    
def write_file(name, data):
    f = file(name, 'wb')
    c = csv.writer(f, dialect = 'excel')
    c.writerows(data)
    f.close()
    
#f1 = r'F:\report080409\portfolio_report_zak 9806 Options.xml'
#f2 = r'F:\report080409\portfolio_report_zak 9806 Options_2.xml'
#r = r'F:\report080409\VOL_COMPARISON1.csv'
prod = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradingManager/' +  ael.date_today().to_string('%Y-%m-%d') + '/'
ds = ael.date_today().to_string('%y%m%d')
f = 'portfolio_report_EQ_OpenVol'
f1 = prod + f + '.xml'
f2 = prod + f + '_2.xml'
out = prod + 'SAEQ_VOL_REPORT_RESULTS.csv'
#sprint f1, f2
#print out
try:
    compare_reports(f1, f2, out)
except:
    ael.log('SAEQ_VOL_REPORT,  VOL COMPARISON REPORT FAILED')









