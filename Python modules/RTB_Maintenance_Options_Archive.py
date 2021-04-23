import acm, ael
import time
from at_time import acm_datetime

BATCH_SIZE = 10000

query = r'''
SELECT i.insid
FROM instrument i left outer join trade t on i.insaddr = t.insaddr
WHERE
    i.instype = 4
    and i.generic = 0
    and i.exp_day < '06/01/2015'
    and t.insaddr is NULL
    and i.archive_status = 0
'''

res = ael.dbsql(query)[0]
count = 0

ael.log('%s Started.' % acm_datetime('NOW'))
print('%s Started.' % acm_datetime('NOW'))

for insid, in res:
    count += 1
    if count > BATCH_SIZE:
        count = 0
        ael.log('%s Sleep for the next 120 seconds.' % acm_datetime('NOW'))
        print('%s Sleep for the next 120 seconds.' % acm_datetime('NOW'))
        ael.log('-------------------------------------------------------------------------------------------------------')
        print('-------------------------------------------------------------------------------------------------------')
        time.sleep(120)
        ael.log('%s Resume Archiving.'  % acm_datetime('NOW'))
        print('%s Resume Archiving.'  % acm_datetime('NOW'))
    try:
        instr = ael.Instrument[insid]
        add_infos = instr.additional_infos()
        exotics = instr.exotics()
        
        if len(exotics) > 0:
            continue
        
        for add_info in add_infos:
            add_info_clone = add_info.clone()
            add_info_clone.archive_status = 1
            add_info_clone.apply()
            add_info_clone.commit()
        
        instr_clone = instr.clone()
        instr_clone.archive_status = 1
        instr_clone.apply()
        instr_clone.commit()
        
        ael.log('%s Archived Instrument %s' % (acm_datetime('NOW'), insid))
    except Exception, e:
        pass #ael.log('Exception in instrument %s. %s. Skipped.' % (insid, e))
