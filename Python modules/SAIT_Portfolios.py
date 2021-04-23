import ael, acm

def get_path_rec_ael(portfolio):
    if not portfolio:
        return []
    path_to_root = [portfolio]
    link = ael.PortfolioLink.select('member_prfnbr=%d' % portfolio.prfnbr)
    if len(link) == 0:
        return path_to_root
    elif link[0].owner_prfnbr:
        path_to_root = path_to_root + get_path_rec_ael(link[0].owner_prfnbr)
        
    return path_to_root

def get_super_portfolio(temp, p, level=0, *rest):
    '''level=0 is the root'''
    return get_path_rec_ael(ael.Portfolio[p])[-1-level]

def get_root(temp, p, level = 0, *rest): 
    list = [e.prfid for e in get_path_rec_ael(ael.Portfolio[p])]
    '''
    if level != 0:
        level = level - 1
    else:
        level = 1
    '''
    return list[len(list)-1]

def get_tree(temp, p, *rest): 
    list = [e.prfid for e in get_path_rec_ael(ael.Portfolio[p])]
    return str(list)
    
def get_root_chorus(temp, p, *rest):
    EXCLUDED_ROOTS = ['ABSA ALTERNATIVE ASSET MANAGEMENT']
    portfoliolist = [e.prfid for e in get_path_rec_ael(ael.Portfolio[p])]
    
    try:
        if portfoliolist[-1] == 'ABSA BANK LTD':
            return portfoliolist[-2]
        if portfoliolist[-1] not in EXCLUDED_ROOTS:
            return portfoliolist[-1]
    except:
        pass
    return None

 
        

def get_trade_count(prf, *rest):
    #set up temporary filter, not possible in acm
    filter = ael.TradeFilter.new()
    filter.fltid = 'TempFilter'
    
    #formulate conditions
    filter_conditions = []
    filter_condition = ("", "", "Portfolio", "equal to", "%s" % prf.prfid, "")
    filter_conditions.append(filter_condition)
    filter_condition = ("AND", "", "Instrument.Expiry day", "greater equal", "0d", "")
    filter_conditions.append(filter_condition)
    filter_condition = ("AND", "", "Status", "not equal to", "Simulated", "")
    filter_conditions.append(filter_condition)
    filter_condition = ("AND", "", "Status", "not equal to", "Void", "")
    filter_conditions.append(filter_condition)
    
    filter.set_query(filter_conditions)
    
    #convert to acm, since SnapshotTradeNbrs is not possible in ael
    ts = acm.Ael().AelToFObject(filter)
    size = int(ts.SnapshotTradeNbrs().Size())
    '''del filter_condition
    del ats
    del filter_conditions
    del ts
    
    mem=acm.Memory().VirtualMemorySize()/(1024*1024)
    print mem
    if mem > 3000:
        print 'collecting garbage'
        for eb in acm.FCache.Select01('.StringKey = "evaluator builders"', "").Contents():
            eb.Reset()  
        acm.Memory().GcWorldStoppedCollect()
        i = gc.collect()'''
    return size




def SetAddInfo(entity, addInfoName, addInfoValue):
    """ Sets an ael additional info field on a given entity """
    ec = entity.clone()
    for addInfo in entity.additional_infos():
        if addInfo.addinf_specnbr.field_name == addInfoName:
            newAddInfo = addInfo.clone()
            break
    else:
        ec = entity.clone()
        newAddInfo = ael.AdditionalInfo.new(ec)
        newAddInfo.addinf_specnbr = ael.AdditionalInfoSpec[addInfoName]

    newAddInfo.value = str(addInfoValue)
    try:
        ec.commit()
        newAddInfo.commit()
        #entityClone.commit()
    except:
        print 'Error: Could not update additional info value %s' %(addInfoName)



def set_add(temp, p, s, *rest):
    prf = ael.Portfolio[p]
    SetAddInfo(prf, 'Portfolio Status', s)
    return 'yes'


def isBankingDay(temp, Date, Curr,*rest):
    ReportingDate = ael.date(Date)
    CurrentDate = ReportingDate.adjust_to_banking_day(ael.Instrument[Curr], 'Following')

    if CurrentDate == ReportingDate:
        value = 1
    else:
        value = 0
    return value

