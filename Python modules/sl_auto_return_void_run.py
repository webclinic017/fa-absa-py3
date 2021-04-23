"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Runs process to void a auto return batch
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  494829
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-11-16 494829    Francois Truter    Initial Implementation
"""

import acm
from sl_batch import SblAutoReturnBatch

returnDateKey = 'AutoReturnDate'
runNoKey = 'RunNo'

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [returnDateKey, 'Sweep Date', 'date', None, acm.Time().DateNow(), 1, 0, 'The date the Auto Return process was run', None, 1],
    [runNoKey, 'Run No', 'int', None, 1, 1, 0, 'The run number for the Auto Return date', None, 1],
]

def ael_main(parameters):
    returnDate = parameters[returnDateKey]
    runNo = parameters[runNoKey]
    
    try:
        batch = SblAutoReturnBatch.LoadBatch(returnDate, runNo)
        batch.VoidBatch()
    except Exception, ex:
        print(str(ex))
