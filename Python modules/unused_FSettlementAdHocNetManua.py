""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementAdHocNetManual - Module for netting of netted 
    settlements (not supported by ordinary settlement script package)

    (c) Copyright 2006 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Result of the netting is Ad_hoc Net and because of that it will not 
    be possible to update it via usual trade or static data update.    
    
    Note that logging level of this module is based on verbosity stated in the
    FSettlementVariables (i.e. verbosity=5 should log everything).

----------------------------------------------------------------------------"""

import ael, FSettlementGeneral, FSettlementGeneral2, FSettlementNetting

def ad_hoc_net(seqnbrs=[],net_date=None,override_net_date=True,\
    net_different_account=False, net_account='',\
    net_different_party_account=False, net_party_account=''):
    '''This function does checks before doing actual netting '''        
    log(1, '----- FSettlementAdHocNetManual --------')
    to_net = []
    for seqnbr in seqnbrs:
        setl = ael.Settlement[int(seqnbr)]            
        if setl:
            to_net.append(setl)
        
    net_date_ok = override_net_date2(to_net, net_date, override_net_date)
    net_curr_ok = check_curr_and_status(to_net)
    net_account_ok = check_accounts(to_net, 1, net_different_account, net_account)
    if net_account_ok:
        net_account_ok = check_accounts(to_net, 0, net_different_party_account, net_party_account)
    
    #checks, if not ok empty net_list
    if not net_date_ok or not net_curr_ok or not net_account_ok:
        to_net = []
        log(0, 'Ad hoc netting will not be done')

    net(to_net, net_date, net_different_account, net_account, net_different_party_account, net_party_account)
    log(1, '----- FSettlementAdHocNetManual finished --------')


def check_curr_and_status(to_net):
    '''Returns 0 trying to net accross different currencies.
    0 is also returned if status is not Authorised'''
    curr = None
    ret = 1
    no=' not able to net'
    for setl in to_net:
        if not curr:
            curr = setl.curr
        elif curr != setl.curr: 
            ret = 0
            pr = "Currency differs (%s != %s), %s" % (curr.insid, setl.curr.insid, no)
            log(1, pr)
            break
        if setl.status != 'Authorised':
            ret = 0
            pr = "Settlement %s has status %s! It must be Authorised, %s" % (setl.seqnbr, setl.status, no)
            log(1, pr)            
 
    return ret


def check_accounts(to_net, acquirer=0, override_account=False, new_account=''):
    '''Returns 0 if accounts of the settlements to net are different.'''
    acc = None
    acc_temp = new_account
    mode = 'acquirer'
    if not acquirer:
        mode = 'counterparty'
    ret = 0    
    p = None            
    p2= None    
    for setl in to_net:
        if acquirer:
            p = setl.acquirer_ptyid
            acc_temp = setl.acquirer_accname
        else:
            p = setl.party_ptyid
            acc_temp = setl.party_accname

        #Party OK
        if not p2:
            p2 = p
        elif p2 != p and override_account:
            pr = "Override %s account is allowed but netting accros different parties is not" % (mode)
            log(1, pr)
            return 0
        elif p2 != p:
            pr = "Override %s account is not allowed nor netting accros different parties" % (mode)
            log(1, pr)
            return 0
 
        #Account OK
        if override_account and get_account(new_account, p, mode):
            ret = 1    
            pr = "Override %s account is allowed: %s" % (mode, new_account)
            log(1, pr)
            break
        elif not override_account and not acc:
            acc = acc_temp
            ret = 1
            #No break here
        elif not override_account and acc != acc_temp: 
            pr = "Different %s account are not allowed: %s != %s" % (mode, acc, acc_temp)
            log(1, pr)
            ret = 0
            break       
                
    return ret

    
def create_pairs_from_input(input):
    ''' '''
    output = []    
    not_valid = [None, '', ' ']    
    a = input.split('(')
    if a==[]:
        a=input
    
    for i in a:
        if i not in not_valid:
            x = i
            y = i.replace(')', '')                        
            output.append(y)
    return output
        
    
def get_account(accname,party,mode=''):
    '''Returns account entity'''
    acc = None
    if type(party)==type('abc'):
        party = ael.Party[party]
    
    if party and accname:
        acc = ael.Account.read("ptynbr=%d and name='%s'" % \
                                    (party.ptynbr, accname))                
    if not acc:
        if accname and party:
            pr = 'Unable to find %s account %s (party=%s)' % (mode, accname, party.ptyid) 
        else:
            pr = 'Unable to find %s account' % (mode)
        log(2, pr)
    return acc


def log(level, s):
    return FSettlementGeneral.log(level, s)

def net(net_list,net_date=None,net_different_account=False, net_account='',\
                                net_different_party_account=False, net_party_account=''):   
    log(1, '----- Net -----')
    if net_list and len(net_list) < 2:
        pr = "Could not create netting, only %d setls deployed\n" % (len(net_list))
        log(1, pr)
        return 1
    elif not net_list:  
        return 1
        
    ok = 0        
    if net_list:      
        first = None
        if len(net_list) > 1:
            first = net_list[0]
        if first:            
            net = ael.Settlement.new()
            prf = 0 
            amount = FSettlementNetting.round_net_amount(net_list, None, 1)           
            net.curr = first.curr.insaddr
            net.amount = amount
            net.ref_type = "Ad_hoc Net"
            net.acquirer_ptyid = first.acquirer_ptyid
            acc = get_account(net_account, first.acquirer_ptyid, 'acquirer')

            if net_different_account and net_account and acc:                                
                net.acquirer_account = acc.account
                net.acquirer_accname = acc.name                
            else:    
                net.acquirer_account = first.acquirer_account
                net.acquirer_accname = first.acquirer_accname
            net.party_ptyid = first.party_ptyid
            acc = get_account(net_party_account, first.party_ptyid, 'counterparty')
            
            if net_different_party_account and net_party_account and acc:                
                net.party_account = acc.account
                net.party_accname = acc.name
            else:
                net.party_account = first.party_account
                net.party_accname = first.party_accname
            if net_date:
                net.value_day = net_date
            else:
                net.value_day = first.value_day
            net.type = 'None'
            net.status = 'New'
            FSettlementGeneral2.copy_protection_from_settlement(net,\
                                                              first.seqnbr)
            try:
                ael.begin_transaction()
                net.commit()
                for n in net_list:
                    log_str = 'Netting setl %d (parent is %d)' % (n.seqnbr, net.seqnbr)
                    log(2, log_str)
                    clone = n.clone()
                    clone.ref_seqnbr = net.seqnbr
                    clone.status = 'Void'
                    clone.ref_type = 'Net Part'
                    clone.commit()                    
                ok = 1                
                ael.commit_transaction()
            except:
                log(1, 'Could not create netting for unknown reason.')
                
    if ok and net.seqnbr>0:            
        pr = "Net %d created (Net=parent)" % (net.seqnbr)
        log(2, pr)
    log(1, '----- Net end -----')                              
    return ok


def override_net_date2(to_net, net_date, override_net_date):
    '''Returns 0 if any of settlements to net has different value_day.'''
    date = None
    ret = 1
    #same
    #override_net_date
    for setl in to_net:
        if not date:
            date = setl.value_day
        elif date != setl.value_day and not override_net_date:
            ret = 0
            pr = "Different Value days are not allowed."
            log(1, pr)
            break
 
    return ret


ael_variables = [\
('to_net', 'Type in settlements seqnbrs to net, i.e. 1,2 or (1,2)(3,4,5)', 'string', None, '', 1, 0, 'Syntax: 1,2 or (1,2)(3,4,5)'),\
('override_net_date', 'Override value day?', 'bool', [True, False], False, 0, 0, 'Date validation to be done?'),\
('net_date', 'New value day of the net settlement', 'date', [ael.date_today()], ael.date_today(), 0, 0, 'Date'),\
('net_different_account', 'Toggle if you want to override acquirer account', 'bool', [False, True], False),\
('net_account', 'Account to override default acquirer account', 'string'),\
('net_different_party_account', 'Toggle if you want to override counterparty account', 'bool', [False, True], False),\
('net_party_account', 'Account to override default counterparty account', 'string')\
]
def ael_main(dict):
    ''' '''        
    net_date = dict['net_date']
    if dict['override_net_date']:
        override_net_date = True
    else:
        override_net_date = False
    
    if dict['net_different_account']:
        net_different_account = True
    else:
        net_different_account = False
    
    if dict['net_different_party_account']:
        net_different_party_account = True
    else:
        net_different_party_account = False        
    
    net_account = dict['net_account']
    net_party_account = dict['net_party_account']

    for net_pair in create_pairs_from_input(dict['to_net']):
        setls = net_pair.split(',')            
        pr = "\nCandidates for Ad Hoc Manual Netting %s" % (str(setls))
        log(1, pr)                     
        ad_hoc_net(setls, net_date, override_net_date,\
            net_different_account, net_account,\
            net_different_party_account, net_party_account)
        
#EOF


