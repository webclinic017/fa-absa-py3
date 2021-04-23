import ael, acm
from at_time import to_datetime
from at_ael_variables import AelVariableHandler
import os.path

ael_variables = AelVariableHandler()

ael_variables.add(
    'file_name', 
    label = 'File Name', 
    cls = 'string', 
    default = '/services/frontnt/Task/Output.txt'
)

ael_variables.add(
    'instrument_type', 
    label = 'Instrument Type', 
    cls = 'string', 
    collection = acm.FEnumeration['enum(InsType)'].Values(),
    default = acm.FEnumeration['enum(InsType)'].Enumerator(3)
)

def ael_main(ael_variables):
    void_futures_select = r'''
        SELECT 
            t.trdnbr,
            i.insid,
            p.prfid,
            t.archive_status,
            t.aggregate_trdnbr,
            t.status
        FROM
            trade t,
            instrument i,
            portfolio p
        WHERE
            t.insaddr = i.insaddr
            AND t.prfnbr = p.prfnbr
            AND t.aggregate_trdnbr = null
            AND i.instype = %s
            AND NOT t.status = 7
            AND t.archive_status = 1
    ''' % (acm.FEnumeration['enum(InsType)'].Enumeration(ael_variables['instrument_type']))

    void_futures_update = r'''
        UPDATE
            trade
        SET 
            status = 7,
            updat_time = '%s',
            updat_usrnbr = %s
        WHERE
            aggregate_trdnbr = null
            AND insaddr in (
                SELECT
                    i.insaddr
                FROM
                    instrument i
                WHERE
                    i.instype = %s
            )
            AND NOT status = 7
            AND archive_status = 1
    ''' % (to_datetime('NOW').strftime('%m/%d/%Y %H:%M:%S'), 
           acm.User().Oid(), acm.FEnumeration['enum(InsType)'].Enumeration(ael_variables['instrument_type']))
    
    records = ael.dbsql(void_futures_select)
    with open(ael_variables['file_name'], 'w') as f:
        for r in records[0]:
            f.write(';'.join([str(e) for e in r]))
            f.write('\n')
    print('Select query:', void_futures_select)
    print('Update statement:', void_futures_update)
    records = ael.dbsql(void_futures_update)
