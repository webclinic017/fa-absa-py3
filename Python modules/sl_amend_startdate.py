"""----------------------------------------------------------------------------
Enable to set start date on Security Loan instrument.

Start Date has to be set on Leg, not on its instrument.
This is not possible from classical GUI,
where only instrument's start date is available.

History:
Date        CR Number  Who                    What
===============================================================================
2016-03-08  3314909    Ondrej Bahounek        Initial implementation.
----------------------------------------------------------------------------"""

import acm
from FBDPCommon import toDate
from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()
ael_variables.add(
    'instruments',
    label = 'SL Instrument',
    cls = 'FSecurityLoan',
    default = None,
    mandatory = True,
    multiple = True,
    alt = 'Security loan on which start date will be changed.'
    )
ael_variables.add(
    'start_date',
    label = 'Start Date',
    cls = 'string',
    default = acm.Time.DateToday(),
    mandatory = True,
    multiple = False,
    alt = 'Date to be used for an instrument start date.'
    )


def amend_sl_startdate(instr, start_date):
    leg = instr.Legs()[0]
    print("Setting start date on '{0}'...".format(instr.Name()))
    print("\t", "Start date: '{0}'".format(start_date))
    print("\t", "End date: '{0}'".format(leg.EndDate()))
    if start_date > leg.EndDate():
        msg = "ERROR: Start date mustn't be later than the End date"
        print(msg)
        raise RuntimeError(msg)
    leg.StartDate(start_date)
    leg.Commit()
    
    if len(leg.CashFlows()) == 1:
        print("Setting start date on SL's cashflow...")
        cf = leg.CashFlows()[0]
        cf.StartDate(start_date)
        cf.Commit()
    elif len(leg.CashFlows()) > 1:
        msg = "ERROR: More than one cashflow found. Can't decide which one should be amended." + \
            "Please, amend them manually."
        print(msg)
        raise RuntimeError(msg)
    print("DONE.")
    
def ael_main(ael_dict):
    start_date = toDate(ael_dict['start_date'])
    instruments = ael_dict['instruments']
    for sl in instruments:
        amend_sl_startdate(sl, start_date)
