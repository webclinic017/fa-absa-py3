import acm

qf = 'wvdb confos temp'
confos = acm.FStoredASQLQuery[qf].Query().Select()
for conf in confos:
    conf.Status('Void')
    print(conf.Oid())
    conf.Commit()
