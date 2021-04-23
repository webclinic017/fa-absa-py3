import ael, acm, time

#This script is used to archive instruments (and add_infos) that are not needed anymore in the live environment.
#The instruments are created in order to create Vol surfaces using themas benchmark instruments
#The problem is that as the underlying market prices are moving many of these instruments are no longer
#needed, and are not re-used in current vol surfaces.
#Since we store all vol surfaces with VPS everyday, we can not delete most of these, therefore we are
#archiving them.
#In the longer term it would be better to re-design the vol solution to use vol points and not benchmarks,
#but it became urgent to archive these instruments since they reached 560k in number.
#The archiving is limited to only catch instruments created by a specific user and with specific underlyings.
#There are further exclusions in the sql to exclude where there are trades on it, used in a live vol surface,
#used as underlying for derivative etc.

#No other scripts/feeds/db updates should run while this is running, since we will
#clear db_updates at the end of the script.



create_date     = acm.Time().DateAddDelta(acm.Time().DateToday(), -20, 0, 0)
user_id         = acm.FUser['SDF_WRITE_PRD'].Oid()
instype_enum    = acm.EnumFromString('InsType', 'Option')
underlying_ids  = ['USD/S&P 500', 'GBP/FTSE', 'EUR/EUROSTOXX']



def check_ds_updates_empty():
    #want to only start script if ds_updates is empty, at the end of the script we will delete * from it.
    res = ael.dbsql("""select count(*) from ds_updates """)
    if len(res[0]) == 0:
        return True
    else:
        return False


def clear_ds_updates():
    #clear this table so that ambas etc do not process these updates.
    res = ael.dbsql("""delete ds_updates 
        SELECT @@rowcount""")
    print '\n\nCleared table ds_updates: ', len(res[0])
    
        
def get_queries(underlying_id, user_id, instype_enum, create_date):
    benchmark_instrs_info = """
      SELECT distinct i.insaddr
      FROM instrument as i, instrument as u
      WHERE
            i.und_insaddr = u.insaddr
        AND u.insaddr = %s
        AND i.creat_usrnbr = %i
        AND i.instype = %i
        AND i.creat_time >= '%s'
        AND i.archive_status = 0
        AND i.insaddr not in 
        (
            SELECT distinct insaddr
            FROM vol_point
            WHERE archive_status = 0
        )
        AND i.insaddr not in 
        (
            SELECT insaddr
            FROM trade
            WHERE archive_status = 0
        )
        AND i.insaddr not in 
        (
            SELECT distinct instrument
            FROM benchmark
            WHERE archive_status = 0
        )
        AND i.insaddr not in 
        (
            SELECT distinct member_insaddr
            FROM combination_link
            WHERE archive_status = 0
        )
        AND i.insaddr not in 
        (
            SELECT distinct und_insaddr
            FROM instrument
            WHERE archive_status = 0
        )        
        """ % (underlying_id, user_id, instype_enum, create_date)
    
        


    benchmark_instrs_archive = """
      UPDATE instrument 
      SET instrument.archive_status = 1 
      WHERE 
        instrument.insaddr in
        ( %s )
        
      SELECT @@rowcount
      """ % (benchmark_instrs_info)
      
      
    benchmark_instrs_add_info_archive = """
    UPDATE additional_info set additional_info.archive_status = 1 
      
    WHERE additional_info.valnbr in 
        (select ai.valnbr
    FROM 
        instrument i, 
        additional_info ai, 
        additional_info_spec ais  
    WHERE
        ais.specnbr = ai.addinf_specnbr and 
        ai.recaddr = i.insaddr and 
        ais.rec_type = 4 and 
        ai.archive_status = 0 and
        i.insaddr in ( %s )
)
    select @@rowcount
      
      """ % (benchmark_instrs_info)
      
    return benchmark_instrs_info, benchmark_instrs_archive, benchmark_instrs_add_info_archive


def exec_sql(sql, filename):
    res = ael.dbsql(sql)
    f = open(filename, 'w')
    for item in res[0]:
        f.write('%s \n' %str(item))
    f.close()
    print 'Wrote results (%i) of sql to file :%s' % (len(res[0]), filename)


ael_variables = [('outPath', 'OutPath', 'string', None, 'c:\\temp\\', 1),
                 ('archive', 'Archive', 'bool', [True, False], True, 1, None, 'Perform archiving when selected, else just print instrument detail')]

def ael_main(dict):
    outpath    = dict['outPath']
    archive    = dict['archive']
    
    print 'Start time: %s' %  (time.asctime(time.localtime()))
    
    if archive and not check_ds_updates_empty:
        print '*'*50
        print 'WARNING, will not run script. Table "ds_updates" is not empty. It needs to be empty since it will be cleared after this script completes.'
        print 'It contains records of changes done on the db that did not pass through the ADS. Since we use dbsql here it is logged there, but we do not'
        print 'want all these changes to be processed by the ambas etc, therefore we clear it afterwards.'
        print '*'*50
        return
    
    for underlying_id in underlying_ids:
        ins = acm.FInstrument[underlying_id]
        benchmark_instrs_info, benchmark_instrs_archive, benchmark_instrs_add_info_archive = get_queries(ins.Oid(), user_id, instype_enum, create_date)
    
    
        und_id =  r'benchmark_instrs_info_%s.csv' %(underlying_id)
        und_id = und_id.replace('/', '_').replace('&', '_').replace(' ', '_')   
        filename = outpath + '/' + und_id
        print '\nStarting: %s @ %s' % (filename, time.asctime(time.localtime()))
        exec_sql(benchmark_instrs_info, filename)
        
        if archive:
        
            und_id =  r'benchmark_instrs_addinfo_archive_%s.csv' %(underlying_id)
            und_id = und_id.replace('/', '_').replace('&', '_').replace(' ', '_')
            filename = outpath + '/' + und_id
            print '\nStarting: %s @ %s' % (filename, time.asctime(time.localtime()))
            exec_sql(benchmark_instrs_add_info_archive, filename)
            
            und_id =  r'benchmark_instrs_archive_%s.csv' %(underlying_id)
            und_id = und_id.replace('/', '_').replace('&', '_').replace(' ', '_')
            filename = outpath + '/' + und_id
            print '\nStarting: %s @ %s' % (filename, time.asctime(time.localtime()))
            exec_sql(benchmark_instrs_archive, filename)
        
            clear_ds_updates()
    
    print '\nEnd time: %s' % (time.asctime(time.localtime()))
    print 'Done'
