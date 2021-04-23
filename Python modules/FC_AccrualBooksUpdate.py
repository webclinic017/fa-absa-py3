import ChorusHierarchy, pprint, acm, ael, time, os.path

file_path = 'C:/backup/'
if not os.path.exists(file_path):
    os.makedirs(file_path)
file_name = os.path.join(file_path, 'Accrual_books_backup(' + time.strftime("%Y%m%d_%H%M%S") + ').txt')
context = ael.Context['FC Accrual Books']
context_clone = context.clone()

def getLinkFromContext(prfnbr):
    if prfnbr:
        for link in context.links():
            if link.prfnbr.prfnbr == prfnbr:
                return link

def getMasterList():
    print '\n--- getting master list ---'
    chorus = ChorusHierarchy.ChorusDelegate()
    print '--- end of getting master list ---'
    return [str(prfnbr) for prfnbr in chorus.applyFilter("accountingTreatment", "Accrual")]

def getAccrualList():
    context_clone = context.clone()
    return [str(link.prfnbr.prfnbr) for link in context_clone.links()]

def backupCurrentContext():
    print '\n--- backup process ---'
    file = open(file_name, "w")
    for prfnbr in accrual_list:
        prfid = acm.FPhysicalPortfolio[prfnbr].Name()
        file.write("(%s)%s\n" % (prfnbr, prfid))
    file.close()
    print 'Backup file has been saved to', file_name
    print '--- end of backup ---'
    return True

def addContext(prfid):
    context_link = ael.ContextLink.new(context_clone)
    context_link.type = 'Accounting Parameter'
    context_link.mapping_type = 'Portfolio'
    context_link.name = 'AP_MM'
    context_link.prfnbr = ael.Portfolio[prfid].prfnbr
    try:
        context_link.commit()
        print 'Created new context link %s(%s)' % (prfid, context_link.prfnbr.prfnbr)
    except Exception, e:
        print 'Failed to create new context link %s(%s) with error : %s' % (prfid, context_link.prfnbr.prfnbr, str(e))

def removeContext(prfnbr=None):
    print '\n--- remove context process ---'
    if not prfnbr:
        print 'Remove all links:'
        for link in context_clone.links():
            if link.prfnbr:
                print 'Removed context link %s(%s)' % (link.prfnbr.prfid, link.prfnbr.prfnbr)
                link.delete()
        context_clone.commit()
    else:
        print 'remove individual link'
        for item in accrual_list:
            if str(prfnbr) == str(item):
                #original----------------------------
                link = getLinkFromContext(prfnbr)
                #link.delete()
                #link.commit
                #alternative-------------------------
                #for link in context.links():
                #    if link.prfnbr.prfnbr == prfnbr:
                #        link.delete()
                #        link.commit()
                print 'Removed context link %s(%s)' % (link.prfnbr.prfid, link.prfnbr.prfnbr)
                #context.links()[prfnbr].delete()
                #context.links()[prfnbr].commit()
    print '--- end of remove process ---'

def syncFromMasterList():
    print '\n--- add context process ---'
    for masterNbr in master_list:
        prfid = acm.FPhysicalPortfolio[masterNbr].Name()
        addContext(ael.Portfolio[prfid].prfid)
    print '--- end of add context ---'

def getPrfnbr(input):
    if input:
        start = str.index(input, '(') + 1
        end = str.index(input, ')')
    return input[start:end]

def getPrfid(input):
    if input:
        start = str.index(input, ')') + 1
        end = len(input)
    return str(input[start:end])

def rollBack():
    print '\n--- rollback process ---'
    print 'looking for file:', file_name
    if os.path.isfile(file_name):
        print 'file found:', file_name
        removeContext() #remove the current accrual list
        with open(file_name) as file:
            content = file.readlines()
        print '\n--- add context process ---'
        for line in content:
            prfnbr = getPrfnbr(line)
            prfid = acm.FPhysicalPortfolio[prfnbr].Name()
            addContext(ael.Portfolio[prfid].prfid)
        print '--- end of add context ---'
    else:
        print 'file not found:', 'C:/backup/Accrual_books_backup(20161107_130903).txt'
    print '--- end of rollback ---'

master_list = getMasterList()
accrual_list = getAccrualList()

#backup the current context portfolios
if backupCurrentContext():
    try:
        removeContext() #remove all current context portfolios
        syncFromMasterList() #add the entire master list into current context
    except Exception, e:
        rollBack()
        print 'Error: ', str(e)
