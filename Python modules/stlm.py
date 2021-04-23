
import acm
from AutoMatchConfirmationSTPHook import AutoMatchConfirmationSTPHook

stp_hook = AutoMatchConfirmationSTPHook()
#confirmations = acm.FConfirmation.Select("createTime > '2019-05-21' and status = 'Pending Matching'").AsArray()
confirmations = [848519]
#print(len(confirmations))
'''
for confirmation in confirmations:
    if not stp_hook.IsTriggeredBy(confirmation):
        continue
    confirmation.Touch()
    confirmation.Commit()
    print('Touched ' + str(confirmation.Oid()))
'''
for confo in confirmations:
    confirmation = acm.FConfirmation[confo]
    confirmation.Touch()
    confirmation.Commit()
    print(('Touched ' + str(confirmation.Oid())))
    
