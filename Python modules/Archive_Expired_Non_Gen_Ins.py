import ael, acm
from at_time import acm_date, ael_date, to_datetime, to_date
from datetime import datetime
from time import strftime
from at_ael_variables import AelVariableHandler
import os.path

ael_variables = AelVariableHandler()

ael_variables.add(
    'output_directory', 
    label = 'Output Directory', 
    cls = 'string', 
    default = r'F:\temp'
)

ael_variables.add(
    'output_file', 
    label = 'Output File', 
    cls = 'string', 
    default = 'expired_non_gen_instruments_to_be_archived.txt'
)

DATES = {
    'First Of Month': acm_date('FirstDayOfMonth'), 
} 

ael_variables.add(
    'date', 
    label = 'Date', 
    cls = 'string', 
    collection = DATES.keys(), 
    mandatory = True
)

ael_variables.add(
    'testmode', 
    label = 'Testmode', 
    cls = 'bool',
    collection = [True, False]
)

def write_report(filename, acm_date):
    instruments = set()
    legs = set()
    cash_flows = set()
    resets = set()
    
    ms_sql_date_string = to_datetime(DATES[acm_date]).timetuple() 
    ms_sql_date_string = strftime('%m/%d/%Y', ms_sql_date_string)
    query = r'''
    SELECT i.insaddr, l.legnbr, cf.cfwnbr, r.resnbr, i.insid, i.instype, i.exp_day, i.generic
    FROM instrument i LEFT OUTER JOIN trade t on i.insaddr = t.insaddr
    LEFT OUTER JOIN leg l ON i.insaddr = l.insaddr
    LEFT OUTER JOIN cash_flow cf ON l.legnbr = cf.legnbr
    LEFT OUTER JOIN reset r ON cf.cfwnbr = r.cfwnbr
    WHERE i.generic = 0
    AND t.insaddr IS NULL
    and i.archive_status = 0
    and NOT UPPER(i.insid) LIKE '%s'
    AND i.exp_day < '%s'
    and i.instype in (3, 4, 7, 8, 10, 11, 15, 16, 17, 18, 19, 33, 34, 36, 37, 38, 52, 59)
    ''' % ('%DEFAULT%', ms_sql_date_string)
    
    with open(filename, 'w') as f:
        res = ael.dbsql(query)[0]
        line = '%s;%s;%s;%s;%s;%s;%s;%s\n' % ('insaddr', 'legnbr', 'cfwnbr', 'resnbr', 'insid', 'instype', 'exp_day', 'generic')
        f.write(line)
        for insaddr, legnbr, cfwnbr, resnbr, insid, instype, exp_day, generic in res:
            line = '%s;%s;%s;%s;%s;%s;%s;%s\n' % (insaddr, legnbr, cfwnbr, resnbr, insid, acm.FEnumeration['enum(InsType)'].Enumerator(instype), exp_day, generic)
            f.write(line)
            instruments.add(insaddr)
            if legnbr:
                legs.add(legnbr)
            if cfwnbr:
                cash_flows.add(cfwnbr)
            if resnbr:
                resets.add(resnbr)
            
    return list(instruments), list(legs), list(cash_flows), list(resets)
    
def archive_instruments(instruments, output_dir):
    with open(os.path.join(output_dir, 'archived_instruments.log'), 'w') as f:
        idx = 0
        while idx < len(instruments):
            lower = idx
            if idx + 1000 > len(instruments):
                upper = len(instruments)
            else:
                upper = idx+1000
            
            query = r'''
            UPDATE instrument
            SET updat_usrnbr = 968, updat_time = GETDATE(), archive_status = 1
            WHERE insaddr in (%s)
            ''' % ','.join([str(e) for e in instruments[lower:upper]])
            ael.dbsql(query)
            for insaddr in instruments[lower:upper]:
                line = '%s\n' % insaddr
                f.write(line)
            idx = idx + 1000

def archive_legs(legs, output_dir):
    with open(os.path.join(output_dir, 'archived_legs.log'), 'w') as f: 
        idx = 0
        while idx < len(legs):
            lower = idx
            if idx + 1000 > len(legs):
                upper = len(legs)
            else:
                upper = idx+1000
            
            query = r'''
            UPDATE leg
            SET updat_usrnbr = 968, updat_time = GETDATE(), archive_status = 1
            WHERE legnbr in (%s)
            ''' % ','.join([str(e) for e in legs[lower:upper]])
            ael.dbsql(query)
            for legnbr in legs[lower:upper]:
                line = '%s\n' % legnbr
                f.write(line)
            idx = idx + 1000
        
def archive_cash_flows(cash_flows, output_dir):
    with open(os.path.join(output_dir, 'archived_cash_flows.log'), 'w') as f: 
        idx = 0
        while idx < len(cash_flows):
            lower = idx
            if idx + 1000 > len(cash_flows):
                upper = len(cash_flows)
            else:
                upper = idx+1000
            
            query = r'''
            UPDATE cash_flow
            SET updat_usrnbr = 968, updat_time = GETDATE(), archive_status = 1
            WHERE cfwnbr in (%s)
            ''' % ','.join([str(e) for e in cash_flows[lower:upper]])
            ael.dbsql(query)
            for cfwnbr in cash_flows[lower:upper]:
                line = '%s\n' % cfwnbr
                f.write(line)
            idx = idx + 1000

def archive_resets(resets, output_dir):
    with open(os.path.join(output_dir, 'archived_resets.log'), 'w') as f:
        idx = 0
        while idx < len(resets):
            lower = idx
            if idx + 1000 > len(resets):
                upper = len(resets)
            else:
                upper = idx+1000
            
            query = r'''
            UPDATE reset
            SET updat_usrnbr = 968, updat_time = GETDATE(), archive_status = 1
            WHERE resnbr in (%s)
            ''' % ','.join([str(e) for e in resets[lower:upper]])
            ael.dbsql(query)
            for resnbr in resets[lower:upper]:
                line = '%s\n' % resnbr
                f.write(line)
            idx = idx + 1000
        
def ael_main(ael_variables):
    print 'Writing Report...'
    instruments, legs, cash_flows, resets = write_report(os.path.join(ael_variables['output_directory'], ael_variables['output_file']), ael_variables['date'])
    print 'Written Report to %s' % os.path.join(ael_variables['output_directory'], ael_variables['output_file'])
    if not ael_variables['testmode']:
        print 'Archiving Instruments...'
        archive_instruments(instruments, ael_variables['output_directory'])
        print 'Archived Instruments. Written report to %s' % (os.path.join(ael_variables['output_directory'], 'archived_instruments.log'))
        print 'Archiving Legs...'
        archive_legs(legs, ael_variables['output_directory'])
        print 'Archived Legs. Written report to %s' % (os.path.join(ael_variables['output_directory'], 'archived_legs.log'))
        print 'Archiving Cash Flows...'
        archive_cash_flows(cash_flows, ael_variables['output_directory'])
        print 'Archived Cash Flows. Written report to %s' % (os.path.join(ael_variables['output_directory'], 'archived_cash_flows.log'))
        print 'Archiving Resets...'
        archive_resets(resets, ael_variables['output_directory'])
        print 'Archived Resets. Written report to %s' % (os.path.join(ael_variables['output_directory'], 'archived_resets.log'))
        print 'Completed Successfully.'
