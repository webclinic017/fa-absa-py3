'''
The initial requirement of this EOD is to move Pending Closure settlements to Closed in order for settlements to be archived.
FIS was requested to make this an optional extra as part of the core EOD so the need for this script might be temporary.

HISTORY
=================================================================================================================================
Date            Change no       Developer              Requester         Description
=================================================================================================================================
2017-03-07      CHNG0004374219  Willie vd Bank                           Initial implementation
'''

import acm
from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()

ael_variables.add_bool(
    "moveClosed",
    label="Set Pending Closure settlements to Closed",
    default=False,
    alt='Enable before running if settlements in Pending Closure status should be moved to Closed.'
)

def move_to_Closed():
    allPendingClosure = [settle.Oid() for settle in acm.FSettlement.Select('') if settle.Status() == 'Pending Closure']
    print('Number of settlements to be closed:', str(len(allPendingClosure)))

    for sOid in allPendingClosure:
        try:
            settle = acm.FSettlement[sOid]
            settle.Status('Closed')
            settle.Commit()
            print(sOid)
        except Exception, e:
            print('Error on settlement', str(sOid))
            print(e)
    print('Done.')

def ael_main(dict_arg):
    if dict_arg['moveClosed'] == True:
        print('Moving settlements to Closed...')
        move_to_Closed()
