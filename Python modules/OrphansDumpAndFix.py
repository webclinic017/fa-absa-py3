import ael, time

#This script is intended to be run every weekend. 
#It cleans up orphan records.  Orphans are live linked records
#where the parent record has been deleted or archived.
#This happens if someone deletes or archives directly on the 
#database and forgets about linked records, like payments and add_infos.
#The core BDP FExpiration script also created orphans by not really archiving
#the linked records.
#Initial clean up was approsximately 4.3 mil records, but weekly volume should
#be zero or low.  The clean up runs fast (a few minutes for hundreds of thousands
#of records) when archiving them, while the delete is much slower, especially instrument
#deletes.



#---------------------------------
TradeAddInfoArchiveOrphans_base = """
where additional_info.valnbr in 
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
    ai.archive_status = 0)"""

TradeAddInfoArchiveOrphans_info = """
select * from additional_info""" + TradeAddInfoArchiveOrphans_base

TradeAddInfoArchiveOrphans_fix = """
update additional_info set additional_info.archive_status = 1""" + \
TradeAddInfoArchiveOrphans_base + """select @@rowcount"""



#---------------------------------
TradeAddInfoDeleteOrphans_base = """
where additional_info.valnbr in 
    (select ai.valnbr
  from 
    additional_info ai, 
    additional_info_spec ais
  where  
    ais.specnbr = ai.addinf_specnbr and 
    ais.rec_type = 19 
    and ai.recaddr not in (
        select t.trdnbr from trade t))"""

TradeAddInfoDeleteOrphans_info = """
select * from additional_info""" + TradeAddInfoDeleteOrphans_base

TradeAddInfoDeleteOrphans_fix = """
delete additional_info """ + \
TradeAddInfoDeleteOrphans_base + """select @@rowcount"""


#---------------------------------
InstrumentAddInfoArchiveOrphans_base = """
where additional_info.valnbr in 
    (select ai.valnbr
  from 
    instrument i, 
    additional_info ai, 
    additional_info_spec ais  
  where 
    ais.specnbr = ai.addinf_specnbr and 
    ai.recaddr = i.insaddr and 
    ais.rec_type = 4 and 
    i.archive_status = 1 and 
    ai.archive_status = 0)"""

InstrumentAddInfoArchiveOrphans_info = """
select * from additional_info""" + InstrumentAddInfoArchiveOrphans_base

InstrumentAddInfoArchiveOrphans_fix = """
update additional_info set additional_info.archive_status = 1 """ + \
InstrumentAddInfoArchiveOrphans_base  + """select @@rowcount"""



#---------------------------------
InstrumentAddInfoDeleteOrphans_base = """
where additional_info.valnbr in 
    (select ai.valnbr
  from 
    additional_info ai, 
    additional_info_spec ais
  where  
    ais.specnbr = ai.addinf_specnbr and 
    ais.rec_type = 4 
    and ai.recaddr not in (
        select  i.insaddr from instrument i))"""

InstrumentAddInfoDeleteOrphans_info = """
select * from additional_info """ + InstrumentAddInfoDeleteOrphans_base

InstrumentAddInfoDeleteOrphans_fix = """
delete additional_info """ + \
InstrumentAddInfoDeleteOrphans_base + """select @@rowcount"""



#---------------------------------
PaymentArchiveOrphans_base = """where payment.paynbr in 
    (select p.paynbr
  from 
    trade t, 
    payment p
  where 
    t.trdnbr = p.trdnbr and 
    t.archive_status = 1 and 
    p.archive_status = 0)"""

PaymentArchiveOrphans_info = """
select * from payment """ + PaymentArchiveOrphans_base

PaymentArchiveOrphans_fix = """
update payment set payment.archive_status = 1 """ + \
PaymentArchiveOrphans_base + """select @@rowcount"""
#---------------------------------



def exec_sql(sql, filename):
    res = ael.dbsql(sql)
    f = open(filename, 'w')
    for item in res[0]:
        f.write('%s \n' %str(item))
    f.close()
    print 'Wrote results (%i) of sql to file :%s' % (len(res[0]), filename)


queries = ['TradeAddInfoArchiveOrphans',      
           'TradeAddInfoDeleteOrphans',   
           'InstrumentAddInfoArchiveOrphans',
           'InstrumentAddInfoDeleteOrphans', 
           'PaymentArchiveOrphans']  

ael_variables = [('outPath', 'OutPath', 'string', None, 'c:\\temp\\', 1),
                 ('fixit', 'Fixit', 'bool', [True, False], True, 1, None, 'Perform clean up when selected, else just print orphan detail')]

def ael_main(dict):
    outpath  = dict['outPath']
    fixit    = dict['fixit']
    
    print 'Start time: %s' %  (time.asctime(time.localtime()))
    
    for what in ['info', 'fix']:
        if what == 'info' or (what == 'fix' and fixit):
            for query in queries:
                query_name = query + '_' + what
                filename = outpath + query_name + '.csv'
                print '\nStarting: %s @ %s' % (filename, time.asctime(time.localtime()))
                sql = eval(query_name)
                exec_sql(sql, filename)
        
    print 'End time: %s' % (time.asctime(time.localtime()))
    print 'Done'

