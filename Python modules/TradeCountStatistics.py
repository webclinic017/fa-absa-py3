import ael, acm


all_query = """select count(t.trdnbr),p.prfid, e.tag 
from trade t,portfolio p, instrument i,ds_enums e 
where e.name = 'InsType' and e.value = i.instype 
and t.prfnbr = p.prfnbr 
and t.archive_status = 0 
and t.insaddr = i.insaddr 
group by p.prfid,  e.tag 
having  count(t.trdnbr) > 1000 """

all_abcap       = acm.FCompoundPortfolio['ABSA CAPITAL'].AllPhysicalPortfolios()
all_abcap_names = [p.Name() for p in all_abcap]
date            = ael.date_today().to_string('%Y%m%d')  

def generate_all_file(filename):
    
    all_out=open(filename, "w")
    res = ael.dbsql(all_query)

    for cnt, port, instype in res[0]:
        
        abcap_ind = 'AbCapPortfolio' if port in all_abcap_names else 'Non-AbCapPortfolio'
        line = "%s|%s|%s|%s|%s\n"  % (port, instype, cnt, abcap_ind, date)
        print '...', line
        all_out.write(line)
    all_out.close()
    print 'Wrote file:', filename
    
    

ael_variables = [['pathwithname', 'Output filename(date.txt will be added)', 'string', None, '/services/frontnt/Task/TradeStats', 1, 0]]

def ael_main(dict):
    pathwithname = dict['pathwithname']
    
    all_out_file = r"%s_%s.csv" % (pathwithname, date)
     
    generate_all_file(all_out_file)
    print 'done'
