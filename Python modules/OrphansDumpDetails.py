import ael

sql_1 = """
select * from additional_info

where  additional_info.valnbr in 
(select ai.valnbr
from 
trade t,
additional_info ai, 
additional_info_spec ais 
where 
ais.specnbr = ai.addinf_specnbr and 
ai.recaddr = t.trdnbr and 
ais.rec_type = 19 and 
t.archive_status = 1 and 
ai.archive_status = 0)
"""

sql_2 = """
select * from additional_info
where
additional_info.valnbr in 
(select ai.valnbr
from 
additional_info ai, 
additional_info_spec ais

where  
ais.specnbr = ai.addinf_specnbr and 
ais.rec_type = 19 

and ai.recaddr not in (
select t.trdnbr from trade t))
"""

sql_3 = """
select * from additional_info

where
additional_info.valnbr in 
(select 
ai.valnbr
from 
instrument i, 
additional_info ai, 
additional_info_spec ais  
where 
ais.specnbr = ai.addinf_specnbr and 
ai.recaddr = i.insaddr and 
ais.rec_type = 4 and 
i.archive_status = 1 and 
ai.archive_status = 0)
"""

sql_4 = """
select * from additional_info 
where
additional_info.valnbr in 
(select ai.valnbr
from 
additional_info ai, 
additional_info_spec ais

where  
ais.specnbr = ai.addinf_specnbr and 
ais.rec_type = 4 

and ai.recaddr not in (
select  i.insaddr from instrument i))
"""

sql_5 = """
select * from payment
where
payment.paynbr in (

select 
p.paynbr
from 
trade t, 
payment p

where 
t.trdnbr = p.trdnbr and 
t.archive_status = 1 and 
p.archive_status = 0)
"""

queries = {'TradeAddInfoArchiveOrphans'         :sql_1,
           'TradeAddInfoDeleteOrphans.txt'      :sql_2,
           'InstrumentAddInfoArchiveOrphans'    :sql_3,
           'InstrumentAddInfoDeleteOrphans'     :sql_4,
           'PaymentArchiveOrphans'              :sql_5}


def exec_sql(sql, filename):
    res = ael.dbsql(sql)
    f = open(filename, 'w')
    for item in res[0]:
        f.write('%s \n' %str(item))
    f.close()
    print 'Wrote results (%i) of sql to file :%s' % (len(res[0]), filename)


ael_variables = [('OutPath', 'OutPath', 'string', None, 'c:\\tsemp\\', 1)]

def ael_main(dict):
    outpath  = dict['OutPath']
    
    for sql_name in queries:
        filename = outpath + sql_name + '.csv'
        print '\nStarting:', filename
        exec_sql(queries[sql_name], filename)
        
    print 'Done'

