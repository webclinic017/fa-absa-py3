import acm

list = ['AGG_SL_ALL_REPORT',
'AGG_SL_ARCHIVE',
'AGG_SL_CASH_POSTING',
'AGG_SL_DEAGG',
'AGG_SL_EXP',
'AGG_SL_EXP_REPORT',
'AGG_SL_GRAVEYARD',
'AGG_SL_INTERN_EXP',
'AGG_SL_INTERN_EXP_REP',
'AGG_SL_INTERN_TERM',
'AGG_SL_SIM',
'AGG_SL_TERM',
'AGG_SL_VOID']

for queryFolder in list:
    issue = False
    qf = acm.FStoredASQLQuery.Select01('name = %s' %queryFolder, '')

    qf_new = qf.Clone()
    name = qf.Name()
    qf_new.Name('%s_%s' %(name, 'N'))
    try:
        qf_new.Commit()
    except Exception, e:
        print 'Count not create a new Qury Folder for original query folder %s: %s' %(queryFolder, str(s))
        issue = True
        next

    if issue == False:
        try:
            qf.Delete()
        except Exception, e:
            print 'Count not delete the original Qury Folder %s: %s' %(queryFolder, str(s))
            issue = True
            next
    
    if issue == False:
        qf_new.Name(name)
        try:
            qf_new.Commit()
        except Exception, e:
            print 'Count not change the name of the new Qury Folder %s: %s' %(qf_new.Name, str(s))
            issue = True
            next
