"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Runs process to void a sweeping batch
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  494829
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-03-11 243997    Francois Truter    Initial Implementation
2010-11-16 494829    Francois Truter    Using sl_batch
"""

import acm
from sl_batch import SblSweepBatch
from sl_process_log import ProcessLog
from sl_process_log import ProcessLogException

sweepDateKey = 'SweepDate'
runNoKey = 'RunNo'
nextBusinessDay = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(acm.Time().DateNow(), 1)

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [sweepDateKey, 'Sweep Date', 'date', None, nextBusinessDay, 1, 0, 'The date which to void', None, 1],
    [runNoKey, 'Run No', 'int', None, 1, 1, 0, 'The run number for the sweep date', None, 1],
]

def ael_main(parameters):
    sweepDate = parameters[sweepDateKey]
    runNo = parameters[runNoKey]
    
    log = ProcessLog('SBL Void Sweeping')
    
    try:
        batch = SblSweepBatch.LoadBatch(sweepDate, runNo)
        batch.VoidBatch(log)
    except Exception, ex:
        if not isinstance(ex, ProcessLogException):
            log.Exception(str(ex))
        else:
            print(str(ex))
    finally:
        print(log)
