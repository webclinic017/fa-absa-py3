"""-----------------------------------------------------------------------------
PURPOSE                 : This module is used to envoke confirmation EOD processing
--------------------------------------------------------------------------------
HISTORY
================================================================================
Date            Change no  Developer            Description
--------------------------------------------------------------------------------
2016            XXXXXXX    Willie vd Bank       Initial Implementation
2016-06-10                 Vojtech Sidorin      Replace hardcoded log path with ael variable.
"""

import os

import acm, sys, datetime, ael
from acm import Time
from PS_Functions import modify_asql_query
from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()
ael_variables.add_bool(
        name="write_log",
        label="Write log",
        default=True,
        mandatory=True,
        )
ael_variables.add(
        name="log_dir",
        label="Output log directory",
        cls="string",
        default="f:\Werk stuff\Front\Work\In progress\Demat\Eod\DematConfirmationIntraDay",
        mandatory=False,
        )

CFquery = 'Demat Valid CFs'
logging = ''

def log(text):
    global logging
    logging += str(datetime.datetime.utcnow())[0:19] + ' ' + text + '\n'


def writefile(text, location):
    try:
        file = open(location, 'w')
        file.write(text)
        file.close()
    except Exception, e:
        print 'Error creating output file.', e


def getCF(date):
    #Returns all the cash flows matching the given pay date
    
    global CFquery
    query = modify_asql_query(acm.FStoredASQLQuery[CFquery].Query(), "PayDate", False, date)
    return query.Select()


def ael_main(params):
    global logging
    log('Demat intra-day task started...')
    date = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(Time.DateNow(), 1)
    for cf in getCF(date):
        try:
            log('Cash flow ' + str(cf.Oid()) + ' on ISIN ' + cf.Leg().Instrument().Isin() + ' will be considered for Demat intra-day processing.')
            cf.Touch()
            cf.Commit()
        except Exception, e:
            log('Failed to commit cash flow!' + str(e))

    log('Demat intra-day task finished.')

    #print logging      #Maybe ael.log
    #Only for testing
    print logging
    if params["write_log"]:
        try:
            log_filename = os.path.join(params["log_dir"], str(datetime.datetime.utcnow())[0:10] + ".txt")
            writefile(logging, log_filename)
        except:
            ael.log('Test file failed to write')
