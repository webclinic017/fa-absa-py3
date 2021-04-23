'''
Created on 22 Feb 2016

This should be one time run script. It will fix the Deposits expiry time. For more details please see:
https://confluence.barcapint.com/display/ABCAPFA/Deposit+expiry+date

@author: conicova
'''

import acm, ael
from at_log import log
from at_ael_variables import AelVariableHandler


def _fix_expiry_date(ins, new_date):
    log("Amending '{0}' expiry date '{1}'->'{2}'".format(ins.Name(), ins.ExpiryDate(), ''), False)
    # ins.ExpiryDate(new_date)
    ins.ExpiryTime('')
    ins.Commit()

def _get_instruments_to_fix(start_date):
    sql = """SELECT 
                i.insaddr
            FROM
                instrument i,
                leg l
            WHERE
                i.instype = 'Deposit'
            AND i.insaddr=l.insaddr
            AND i.exp_time<l.end_day
            AND i.exp_time>'{0}'""".format(start_date)
    
    _, data = ael.asql(sql, 0)
    result = []
    for table in data:
        for row in table:
            result.append(str(row[0]))
            
    return result

ael_variables = AelVariableHandler()
ael_variables.add('start_date',
                  label='Start Date',
                  default=ael.date_today().add_days(-5),
                  alt='Start date')

def ael_main(args):
    
    start_date = args['start_date']
    
    insaddrs = _get_instruments_to_fix(start_date)
    log("{0} instruments to fix".format(len(insaddrs)), False)
    for insaddr in insaddrs:
        ins = acm.FInstrument[insaddr]
        leg = ins.Legs()[0]
        if ins.ExpiryDate() < leg.EndDate():
            prime_trades = len([t for t in ins.Trades() if t.Acquirer().Name() == 'PRIME SERVICES DESK'])
            if prime_trades == 0:
                log("No prime service desk trades: {0}".format(ins.Name()), False)
                continue
            if prime_trades != len(ins.Trades()):
                log("Warning: at least one trade is not a prime desk trade: {0}".format(ins.Name()), False)
                continue
            _fix_expiry_date(ins, leg.EndDate())
    
    log("Finished")
