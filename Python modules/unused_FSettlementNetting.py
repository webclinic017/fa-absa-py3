""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementNetting
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

----------------------------------------------------------------------------"""

import FSettlementGeneral
import FSettlementGeneral2
import FSettlementGeneral3
import FSettlementParams
param = FSettlementParams.get_default_params()
do_round_net_amount = param.round_net_amount
CLOSE_TRADE_RULE = 'net_based_on_close_trade'


def check_intra_trade(rule, settle1, settle2, s1_parent=0):
    '''
    Checks if settlements can be netted according to the 
    (non) bilatteral netting rule and returns 1 or 0.    
    rule      - Netting rule that applies settle2
    settle1   - settlement or parent settlement (stt_c ok)
    settle2   - settlement to be netted (stt_c ok)
    s1_parent - toggle, if settle1 is parent or just settlement
    
    Note that this functions speacially takes care of netting rules
    called net_based_on_close_trade.
    '''    
    ok = 0
    
    pr = "check_intra_trade: netting rule %s (bilateral=%d)" % (rule.ruleid, rule.bilateral_netting)
    log(3, pr)   
    if s1_parent:
        pr = "Parent %d, Settl %d" % (settle1.seqnbr, settle2.seqnbr)
    else:
        pr = "Settl1 %d, Settl2 %d" % (settle1.seqnbr, settle2.seqnbr)
    log(3, pr)           
    rule_ok = rule.seqnbr in get_close_trade_nr()    
    
    if not rule.bilateral_netting:
        # WITHIN TRADE
        if settle1.trdnbr and settle2.trdnbr:
            if settle1.trdnbr.trdnbr==settle2.trdnbr.trdnbr:                
                ok = 1
            elif rule_ok and setl_trades_are_closing(settle1, settle2):
                ok = 1
        elif rule_ok:
            ok = setl_trades_are_closing(settle1, settle2)
    else:
        # BILATERAL, ACROSS TRADES
        if rule_ok:            
            ok = setl_trades_are_closing(settle1, settle2)
        else:   
            ok = 1
    return ok

    
def get_trades_from_net_parts(parent,setl=None,is_close_trade_net=0):
    '''Returns list with the trades connected to the parent settlement.
    Second parameter setl is optional, if parent and setl are the same
    corresponding trades will not be a part of the result.
    is_close_trade_net is per default 0 meaning that this function works
    even for non_close_trade_net settlements.
    See also function get_trade_from_net.
    '''
    ret = []
    sel = ael.Settlement.select('ref_seqnbr=%d' % parent.seqnbr)    
    
    for net_part in sel:
        seqnbr = None
        if setl:
            seqnbr = setl.seqnbr
        if net_part.seqnbr != seqnbr:
            # and not FSettlementGeneral.is_deleted(net_part.seqnbr):
            trds = []
            if not net_part.trdnbr:
                trds = get_trades_from_net_parts(net_part, None, is_close_trade_net)
            else:
                trds = [net_part.trdnbr]
            for tr2 in trds:        
                ct_related = FSettlementGeneral2.is_closed(tr2) or FSettlementGeneral2.is_closing(tr2)
                ct_related = ct_related or not is_close_trade_net
                if tr2 and ct_related:
                    if tr2 not in ret:
                        ret.append(tr2)
    return ret            

    
def trades_are_closing(tr1,tr2,closing_same_trade=1):
    '''Returns 1 if tr1 or tr2 are closing each other.
    Flag closing_same_trade is per default on and it make it 
    possible to return match if both tr1 and tr2 close the same trade.'''
        
    if tr2 and tr2 in FSettlementGeneral2.get_closing_trades(tr1):
        return 1        
    elif tr1 and tr1 in FSettlementGeneral2.get_closing_trades(tr2):
        return 1
    elif closing_same_trade and \
        FSettlementGeneral2.is_partially_closing_some_trade(tr1, tr2):
        return 1
    return 0


def setl_trades_are_closing(settle1, settle2):
    '''Returns True if trades of the settlements (no matter
    if it is net or single settlement) are closing each other.
    settle can be stt_c.
    See also function trades_are_closing.'''
    ok = 0
    trds1 = []
    trds2 = []    
    if settle1.trdnbr:
        trds1 = [settle1.trdnbr]
    elif is_close_trade_net(settle1):
        trds1 = get_trades_from_net_parts(settle1, None, 1)

    if settle2.trdnbr:
        trds2 = [settle2.trdnbr]            
    elif is_close_trade_net(settle2):
        trds2 = get_trades_from_net_parts(settle2, None, 1)

    for tr1 in trds1:        
        for tr2 in trds2:
            if (tr1.trdnbr == tr2.trdnbr) or trades_are_closing(tr1, tr2):            
                ok = 1
                break
    return ok    
    
def get_stored_netted_amount(settlement):
    """
    settlement is the parent node in a netted hierarchy
    """
    returned_amount = 0.0
    settlement_list = ael.Settlement.select('ref_seqnbr = %d' % (settlement.seqnbr))
    for s in settlement_list:
        if s.ref_type == 'Net Part':
            returned_amount = returned_amount + s.amount
    return returned_amount
    

def find_parent(netting_rule, settle, is_close_trade_net=0):
    ''' '''
    ret = 0
    if netting_rule:
        sel = ael.Settlement.select('netting_rule_seqnbr=%d' % \
                                    netting_rule.seqnbr) # om i net_dict?       
        pr = "%d settlements are netted via %s" % (len(sel), netting_rule.ruleid)
        log(1, pr)
        for s in sel:
            if s.status in parent_status:
                if comparison(s, settle) and not ret and \
                   check_intra_trade(netting_rule, s, settle, 1):
                    pr = 'Settlement %d is parent! Netting rule: %s' % (s.seqnbr, netting_rule.ruleid)
                    log(2, pr)

                    old_net = FSettlementGeneral.get_net(s)
                    if old_net:
                        new_amount = old_net.amount + settle.amount
                    else:
                        sna = get_stored_netted_amount(s)
                        new_amount = sna + settle.amount
                    
                    clone = s.clone()
                    clone.status = 'Exception'
                    clone.amount = new_amount
                    net_children_list = FSettlementGeneral.get_net_children_wrapper(s)
                    net_children_list.append(settle)
                    if is_same_trade_among_net_children(net_children_list):
                        clone.trdnbr = net_children_list[0].trdnbr
                    else:
                        clone.trdnbr = None
                        
                    
                    if clone.to_prfnbr:
                        prf = clone.to_prfnbr.prfnbr
                        clone.to_prfnbr = set_portfolio(prf, settle)
                        clone.from_prfnbr = set_portfolio(prf, settle)
                    s_clone = settle.clone() # stt_c to entity and clone!?
                    FSettlementGeneral.clear_status_explanation(s_clone)
                    s_clone.status = 'Void'
                    s_clone.ref_seqnbr = clone.seqnbr
                    s_clone.ref_type = 'Net Part'
                    FSettlementGeneral.append_net(clone)
                    FSettlementGeneral.append_net(s_clone)
                    pr = 'Settlement %d will be part of netting' % (settle.seqnbr)
                    log(2, pr)

                    ret = 1
    return ret

# Fields that are recquired on a settlement for it to be subject to netting.
def comparison(settle1, settle2):
    ''' settle can be stt_c'''
    ok = 0
    if settle1.acquirer_ptyid == settle2.acquirer_ptyid and \
       settle1.acquirer_account == settle2.acquirer_account and \
       settle1.value_day.to_string() == settle2.value_day.to_string() and \
       settle1.curr.insaddr == settle2.curr.insaddr and \
       settle1.party_account == settle2.party_account:
        ok = 1
    return ok

def my_sort(arg1, arg2):
    if arg1.ordernbr < arg2.ordernbr:
        return -1
    elif arg1.ordernbr == arg2.ordernbr:
        return 0
    elif arg1.ordernbr > arg2.ordernbr:
        return 1

def party_netting_rules(ptynbr, acq):
    links = []
    members = []
    rules = []
    if ptynbr:
        links = ael.NettingRuleLink.select('ptynbr = %d' % ptynbr)
        for r in links:
            if r.enabled:
                members.append(r)
        if len(members):
            members.sort(my_sort)
            for m in members:
                rule = m.netting_rule
                if rule.acquirer_ptynbr:
                    if acq:
                        if rule.acquirer_ptynbr.ptynbr==acq.ptynbr:
                            rules.append(rule)
                else:
                    rules.append(rule)
    return rules

def ael_hook_apply_on_settlement(rule, settle):
    '''settle can be stt_c'''
    ok = 0
    func = rule.netting_hook
    try:
        ok = getattr(FSettlementClientNetting, func)(settle)
    except AttributeError:
        log_str = 'Could not call client netting hook %s' % func
        log(0, log_str)
    return ok

def rule_apply_on_settlement(rule, settle, is_close_trade_net=0):
    '''settle can be stt_c but see comment bellow '''
    ok = 0
    if settle and rule:
        trdnbr = settle.trdnbr
        #if not trdnbr and is_close_trade_net:            
        #    trdnbr = get_trade_from_net(settle,1)
                
        if trdnbr and trdnbr.insaddr:
            instype = trdnbr.insaddr.instype
            rtype = rule.instype
            if rtype!='FxSwap' and rtype!='Curr' and rtype!='None':
                if rule.curr:
                    if settle.curr.insaddr == rule.curr.insaddr:
                        if rtype == instype:
                            ok = 1
                else:
                    if rtype == instype:
                        ok = 1
            elif rtype == 'FxSwap' or rtype == 'Curr':
                ins = trdnbr.insaddr
                if ins and trdnbr.curr:
                    if instype == rule.instype:
                        legs = ins.legs()
                        leg_curr = []
                        for l in legs:
                            leg_curr.append(l.curr.insaddr)
                        if instype == 'Curr':
                            leg_curr.append(trdnbr.curr.insaddr)
                        if rule.curr_pair:
                            pair = rule.curr_pair
                            pair_curr = []
                            pair_curr.append(pair.curr1.insaddr)
                            pair_curr.append(pair.curr2.insaddr)
                            ok = 1
                            for leg in pair_curr:
                                if not leg in leg_curr:
                                    ok = 0
                        else:
                            ok = 1
            elif rtype == 'None':
                ins = trdnbr.insaddr
                if rule.curr:
                    if rule.curr.insaddr == settle.curr.insaddr and \
                       ins.instype != 'FxSwap' and ins.instype != 'Curr':
                        ok = 1
                elif rule.curr_pair:
                    if ins and trdnbr.curr:
                        legs = ins.legs()
                        if legs:
                            if instype == 'Curr' or instype == 'FxSwap':
                                leg_curr = []
                                for l in legs:
                                    leg_curr.append(l.curr.insaddr)
                                if instype == 'Curr':
                                    leg_curr.append(trdnbr.curr.insaddr)
                                pair_curr = []
                                pair_curr.append(rule.curr_pair.curr1.insaddr)
                                pair_curr.append(rule.curr_pair.curr2.insaddr)
                                ok = 1
                                for leg in pair_curr:
                                    if not leg in leg_curr:
                                        ok = 0
                else:
                    ok = 1 # different curr?
        if ok:
            if rule.netting_hook:
                ok = ael_hook_apply_on_settlement(rule, settle)
    return ok

def create_acquirer_lists(net_list, rule):
    ''' NOT USED in 3_2_fix'''
    acquirer_dic = {}
    for n in net_list:
        acq_str = n.acquirer_ptyid + n.acquirer_account + n.party_account
        acq_str = acq_str + n.value_day.to_string() + n.curr.insid
        if acq_str in acquirer_dic:
            temp_list = acquirer_dic[acq_str]
            temp_list.append(n)
        else:
            temp_list = [n]
            acquirer_dic[acq_str] = temp_list
    keys = acquirer_dic.keys()
    for k in keys:
        acq_list = acquirer_dic[k]
        if len(acq_list) > 1:
            create_netting(acq_list, rule, None) #None??

"""----------------------------------------------------------------------------
FUNCTION
    set_portfolio() - Function which compares a net settlement record's
                      portfolio with a specific settlement's portfolio. If
                      they are not the same or if either is not set, the 0
                      portfolio should be returned.

----------------------------------------------------------------------------"""
def set_portfolio(prf, settle):
    '''settle can be stt_c '''
    if prf:
        if settle.from_prfnbr:
            port = settle.from_prfnbr.prfnbr
            if not port==prf:
                prf = 0
        elif settle.to_prfnbr:
            port = settle.to_prfnbr.prfnbr
            if not port==prf:
                prf = 0
        else:
            prf = 0
    return prf

"""----------------------------------------------------------------------------
FUNCTION
    create_netting() - Function which nets together a list of settlements and
                       creates a new net settlement.

DESCRIPTION
    Function which nets together a list of settlements and creates a new net
    settlement.

ARGUMENTS
    net_list        A list of settlements to net together
    rule            A netting_rule
    settle          A settlement object, if not none, this function is being
                    called from SingleNetting.
----------------------------------------------------------------------------"""
def create_netting(net_list, rule, settle):
    '''Does the netting based on the netting rule. The settlement that is
    deployed is the one that should be additionally netted. 
    settle can be stt_c'''

    ok = 1
    if net_list and settle:
        set_ent = None
        if FSettlementGeneral3.is_entity_class(settle):
            set_ent = settle.get_ael_entity()
        elif type(settle) == int:
            pr = 'create_netting received seqnbr %d not Settlement(Error)' % (settle)
            log(2, pr)
            set_ent = ael.Settlement[settle]
            
        if set_ent in net_list:
            log(2, 'create_netting: settlement is already netted')
            ok = 0
        first = None
        if len(net_list):
            first = net_list[0]
        if first and ok:            
            if settle_apply_for_netting(settle):
                amount = 0
                net = ael.Settlement.new()
                prf = 0
                if first.to_prfnbr:
                    prf = first.to_prfnbr.prfnbr
                elif first.from_prfnbr:
                    prf = first.from_prfnbr.prfnbr
                for n in net_list:
                    prf = set_portfolio(prf, n)

                amount = round_net_amount(net_list, settle)
                # net should not have trdnbr inspite netted settlements beloning the same trade!
                #if not rule.bilateral_netting and first.trdnbr:
                #    net.trdnbr = first.trdnbr.trdnbr
                net.curr = first.curr.insaddr
                net.amount = amount
                net.ref_type = 'Net'
                net.acquirer_ptyid = first.acquirer_ptyid
                net.acquirer_account = first.acquirer_account
                net.acquirer_accname = first.acquirer_accname
                net.party_ptyid = first.party_ptyid
                net.party_account = first.party_account
                net.party_accname = first.party_accname
                net.netting_rule_seqnbr = rule.seqnbr
                net.value_day = first.value_day
                net.type = 'None'
                net.status = 'New'
                if is_same_trade_among_net_children(net_list):
                    net.trdnbr = first.trdnbr
                FSettlementGeneral2.copy_protection_from_settlement(net,\
                                                                  first.seqnbr)
                if prf:
                    net.to_prfnbr = prf
                    net.from_prfnbr = prf
                try:
                    net.commit()
                    for n in net_list:
                        if FSettlementGeneral.get_mod_settle(n.seqnbr):
                            FSettlementGeneral.remove_settle(n.seqnbr)
                        log_str = 'Netting setl %d, parent is %d' % (n.seqnbr, net.seqnbr)
                        log(2, log_str)
                        clone = n.clone()
                        clone.ref_seqnbr = net.seqnbr
                        clone.status = 'Void'
                        clone.ref_type = 'Net Part'
                        FSettlementGeneral.append_net(clone)
                    #also the deployed settlement must be netted
                    s_clone = settle.clone()
                    FSettlementGeneral.clear_status_explanation(s_clone)
                    s_clone.ref_seqnbr = net.seqnbr
                    s_clone.status = 'Void'
                    s_clone.ref_type = 'Net Part'
                    FSettlementGeneral.append_net(s_clone)
                    log_str = 'Netting setl %d, parent is %d' % (s_clone.seqnbr, net.seqnbr)
                    log(2, log_str)
                except:
                    log(1, 'Could not create netting')
    elif not settle:
        pr = 'create_netting: No settlement deployed (File)'
        log(0, pr)

    return ok

def is_same_trade_among_net_children(net_children_list):
    is_same_trade_among_net_children = True
    trdnbr = net_children_list[0].trdnbr.trdnbr
    for net_child in net_children_list:
        if trdnbr != net_child.trdnbr.trdnbr:
            is_same_trade_among_net_children = False
            break
    return is_same_trade_among_net_children

def create_net_selection(is_close_trade_net=0):
    'Returns a list with Settlements that apply for netting.'

    net_sel = []
    sel = ael.Settlement.select()
    for s in sel:
        if settle_apply_for_netting(s, is_close_trade_net):
            net_sel.append(s)
    return net_sel

def create_new_parent(rule, settle, is_close_trade_net=0):
    '''settle can be stt_c? see create_netting '''
    net_list = []
    pr ='create_new_parent for settl %d' % (settle.seqnbr)
    log(2, pr)    
    settles = create_net_selection(is_close_trade_net) 
    for s in settles:
        if s.seqnbr != settle.seqnbr and s.party_ptyid == settle.party_ptyid:
            if rule_apply_on_settlement(rule, s, is_close_trade_net):
                same = comparison(s, settle)
                not_bilateral = check_intra_trade(rule, settle, s)
                br = best_netting_rule(s, rule)
                pr = "comparison %d or check_intra_trade %d or best rule %d" % (same, not_bilateral, br)  
                log(5, pr)    
                if same and not_bilateral and br:
                    net_list.append(s)
    if net_list:
        log_str = 'Before create_netting %d settlements may be netted with %d' % (len(net_list), settle.seqnbr)
        log(2, log_str)
        if create_netting(net_list, rule, settle):
            return 1
    return 0


"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
import ael, time, FSettlementGeneral
try:
    import FSettlementClientNetting
except ImportError:
    import FSettlementClientNettingTemp as FSettlementClientNetting

parent_status = ['New', 'Exception', 'Authorised', 'Manual Match']

def SingleNetting(settle, is_close_trade_net=0):
    '''settle can be stt_c '''
    netted=0
    if settle_apply_for_netting(settle, is_close_trade_net):
        log_str = 'Trying to net Settlement %d' % settle.seqnbr
        log(2, log_str)
        party = ael.Party[settle.party_ptyid]
        acquirer = ael.Party[settle.acquirer_ptyid]
        if party:
            rules = party_netting_rules(party.ptynbr, acquirer)
            if len(rules):
                for r in rules:
                    if rule_apply_on_settlement(r, settle):
                        log_str2 = 'Rule %s apply on Settlement %d' % \
                                   (r.ruleid, settle.seqnbr)
                        log(2, log_str2)
                        if not find_parent(r, settle, is_close_trade_net):
                            if create_new_parent(r, settle, is_close_trade_net):
                                netted=1
                            else:
                                log(5, 'rule apply but not netted, see create_new_parent')
                        else:
                            log(5, 'already netted no find parent')
                            netted=1 # find parent does net update
                        break
            else:
                log_str = 'No netting rule set for party %s' % (party.ptyid)
                log(2, log_str)
        else:
            log_str = 'No counterparty set on Settlement %d, no netting' % settle.seqnbr
            log(1, log_str)
    return netted

def settle_apply_for_netting(s, is_close_trade_net=0):
    '''Flag is_close_trade_net makes it possible to net a settlement 
    that is netted via close trade netting rule.
    s can be stt_c'''
    ret = 0        
    if s:
        if s.status== 'Authorised' and not s.ref_seqnbr \
           and (s.ref_type == 'None' or is_close_trade_net) \
           and s.delivery_type != 'Delivery versus Payment' and \
           s.type not in FSettlementGeneral.sec_types and not \
           s.manual_match and s.settle_category== 'None' and s.type != 'Coupon':
            ret = 1
    if ret and not param.net_after_unnet:
        ret = net_ok_keyword(s)    
        if not ret:
            log_str = 'Settlement %d will not be netted, diary keyword (File)' % (s.seqnbr)
            log(2, log_str)
            
    return ret

def best_netting_rule(settle, rule):
    '''Some netting rule might apply but there could be some better matching rules.
    This function should be called only if rule_apply_on_settlement(r, settle)
    is called before. settle can be stt_c.
    '''
    party = ael.Party[settle.party_ptyid]
    acquirer = ael.Party[settle.acquirer_ptyid]
    if party:
        sorted_rules = party_netting_rules(party.ptynbr, acquirer)
        for r in sorted_rules:
            if r != rule:
                if rule_apply_on_settlement(r, settle):
                    pr = 'NettingRule %s matches better then rule %s (Settl %d)' % \
                                               (r.ruleid, rule.ruleid, settle.seqnbr)
                    log(2, pr)
                    return 0
            else:
                return 1
    return 0
    

def round_net_amount(net_list, setl=None, no_setl_ok=1):
    ''' '''
    type_dict = {}
    non_types = [None, 'None'] # net does not have type, ref_type will be used instead
    
    if setl and setl not in net_list:
        net_list.append(setl)
    elif setl:
        pr = 'Settlement %d is already in the net list' % (setl.seqnbr)
        log(3, pr)        
    elif no_setl_ok:
        pr = 'Settlement not deployed, net amount might be wrong (still %d settlements to net)' % (len(net_list))
        log(3, pr)
                        
    pr = '%d settlements to net' % (len(net_list))
    log(3, pr)
    
    for setl in net_list:
        st = setl.type
        if st in non_types:
            st = setl.ref_type
        if type_dict.has_key(st):
            type_dict[st].append(setl)
        else:            
            type_dict[st]=[setl]

    amount = 0        
    for settle_type in type_dict.keys():
        setls = type_dict[settle_type]
        setls_amount = 0
        for s in setls:
            st = s.type
            if st in non_types:
                st = s.ref_type
            setls_amount = setls_amount + s.amount
            pr = 'Adding amount %f (%s)' % (s.amount, st)
            log(3, pr)

        if do_round_net_amount:
            r = round(setls_amount)     
            pr = 'Total %s amount is %f (rounded from %f)' % (settle_type, r, setls_amount)
        else:
            r = setls_amount
            pr = 'Total %s amount is %f' % (settle_type, r)    

        log(3, pr)            
        amount = amount + r # per curr?            
        
    pr = 'Total Net amount is %f' % (amount)
    log(3, pr)
    
    return amount                
    
    
def net_ok_keyword(setl):
    '''Returns 0 if the settlement should NOT be netted otherwise 1.
    Note no strange characters such as underscore in the keywords!
    setl can be stt_c.
    '''
    KEYWORDS = {'net0':0, 'net1':1}
    d = setl.diary
    if d:
        diary = d.get_text()
        datetime = diary.split('<DateTime>')
        datetime.reverse()        
        for di in datetime:
            for k in KEYWORDS.keys():       
                if di.find(k)>-1:
                    return KEYWORDS[k]
    return 1


def log(level, s):
    return FSettlementGeneral.log(level, s)
    
    
def get_close_trade_nr():
    '''Returns a list containing close trade netting rules. '''
    
    ret = []    
    for nr in ael.NettingRule.select():
        if nr.netting_hook == CLOSE_TRADE_RULE:
            ret.append(nr.seqnbr)                        
    return ret


def is_close_trade_net(setl):
    '''Returns true if the settlement is netted via close trade netting.'''
    ret = 0
    if setl.netting_rule_seqnbr:
        ret = setl.netting_rule_seqnbr.seqnbr in get_close_trade_nr()
            
    return ret
    
    
def get_trade_from_net(settle,nbr=0):
    '''Returns one of the trades that are connected to the settlements 
    that are netted. If nbr is supplied trdnbr is returned'''
    tr = None
    trds = get_trades_from_net_parts(settle)
    
    if len(trds):
        tr = trds[0]
        pr = "Netted settl %d, corresponding trade is %d" % (settle.seqnbr, tr.trdnbr)
        FSettlementGeneral.log(3, pr)
        if tr and nbr:
            tr = tr.trdnbr
    return tr

def get_net_parents(net_dict):
    net_parent_list = []
    for (seqnbr, settlement) in net_dict.items():
        if settlement.type == 'None' and \
           settlement.ref_type == 'Net':
            net_parent_list.append(settlement)
    return net_parent_list
    
def get_net_children(net_dict, parent):
    net_children_list = []
    ref_seqnbr_list = ael.Settlement.select('ref_seqnbr = %d' % parent.seqnbr)
    
    for child in ref_seqnbr_list:
        if child.ref_type == 'Net Part':
            net_children_list.append(child)
    
    for (seqnbr, settlement) in net_dict.items():
        if settlement.ref_seqnbr:
            if seqnbr != parent.seqnbr and \
               settlement.ref_seqnbr.seqnbr == parent.seqnbr:
                net_children_list.append(settlement)
    
    return net_children_list
    


