import acm
from AutoMatchConfirmationSTPHook import AutoMatchConfirmationSTPHook

stp_hook = AutoMatchConfirmationSTPHook()
confirmations = acm.FConfirmation.Select("createTime > '2019-05-21' and status = 'Pending Matching'").AsArray()
#print(len(confirmations))
for confirmation in confirmations:
    if not stp_hook.IsTriggeredBy(confirmation):
        continue
    confirmation.Touch()
    confirmation.Commit()
    print(('Touched ' + str(confirmation.Oid())))
