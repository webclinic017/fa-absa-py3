""" Settlement:1.2.2.hotfix23 """

import ael
import FSettlementGeneral, FSettlementGeneral3, FSettlementGeneralRT, FSettlementParams

A_status = ['Updated', 'Recalled']
B_status = ['New', 'Exception', 'Manual Match']
C_status = ['Authorised', 'Not Acknowledged']
D_status = ['Released', 'Acknowledged', 'Pending Closure', 'Non Receipt',\
            'Incorrect Receipt', 'Non Payment', 'Incorrect Payment']

# Settlement which is modified and returned if handle_recalled is
# called from FSettlementGeneral
ret_settle = None
param = FSettlementParams.get_default_params()
H_status = []
if param.update_void:
    H_status = ['Hold', 'Void']
else:
    H_status = ['Hold']

def isNonZeroAmount(trade, typ, corrected_setl=0):
    '''Calculates amount for certain settlement types.
    trade can be tr_c.
    '''
    amount = 0
    if typ == 'End Cash':
        amount = get_end_cash(trade, corrected_setl)
    elif typ == 'Premium 2':
        amount = get_premium2(trade, corrected_setl)
    if amount == 0 and trade and typ:
        pr = 'Zero %s for trade %d, no settlement added' % (typ, trade.trdnbr)
        log(2, pr)
    return amount

def clear_fields(settle):
    return FSettlementGeneral3.clear_fields(settle)

def validate_values(trade, setl, typ, corrected_setl = 0, tr_c=None):
    log(2, 'validate_values:')
    tr_c = FSettlementGeneralRT.set_c(tr_c, trade, 'Trade')
    instr = tr_c.insaddr
    if not instr:
        return
    if typ == 'End Cash':
        setl.amount = get_end_cash(tr_c, corrected_setl)
        setl.curr = tr_c.curr.insaddr
    setl.trdnbr = tr_c.trdnbr
    setl.value_day = instr.exp_day
    if tr_c.prfnbr:
        if setl.amount > 0:
            setl.to_prfnbr = tr_c.prfnbr.prfnbr
        else:
            setl.from_prfnbr = tr_c.prfnbr.prfnbr
    else:
        pr = 'No portfolio on trade %d' % (tr_c.trdnbr)
        log(2, pr)

    if tr_c.acquirer_ptynbr:
        setl.acquirer_ptyid = tr_c.acquirer_ptynbr.ptyid
    else:
        pr = 'No acquirer on trade %d' % (tr_c.trdnbr)
        log(2, pr)

    if tr_c.counterparty_ptynbr:
        setl.party_ptyid = tr_c.counterparty_ptynbr.ptyid
    else:
        pr = 'No counterparty on trade %d' % (tr_c.trdnbr)
        log(2, pr)

    FSettlementGeneral.account_info(trade, setl, 0)       

def already_created(trade, typ):
    '''trade can be tr_c '''
    already_created = 0
    for s in FSettlementGeneralRT.get_settlements(trade):### II
        if s.type == typ:
            if FSettlementGeneral.source_data(s):
                already_created = 1
                break
    return already_created
    
def validate(trade, op, tr_c=None, ins_c=None):
    tr_c = FSettlementGeneralRT.set_c(tr_c, trade, 'Trade')
    if FSettlementGeneralRT.is_trade(tr_c):
        pr = 'validate: trade %d' % (tr_c.trdnbr)
        log(3, pr)
        instr = tr_c.insaddr
        if ins_c:
            instr = ins_c
        create_end_sec = 0
        if not instr:
            return
        instype = instr.instype        
        corrected_setl = 0
        correct_trade = is_correction_trade(trade)  
                
        if op=='INSERT':
            if not tr_c.status in FSettlementGeneralRT.tr_status:
                return
                
            if instype in FSettlementGeneral.und_ins_security:
                if (FSettlementGeneral.paydayOK(instr.exp_day, trade, 1, 'End Security') \
                   or correct_trade) and not already_created(tr_c, 'End Security'):
                    create_end_sec = 1
            if FSettlementGeneral.is_collateral_trade(tr_c) and \
               FSettlementGeneral.paydayOK(tr_c.re_acquire_day, trade, 1,\
               'End Security') and not already_created(tr_c, 'End Security'):
                create_end_sec = 1
            if create_end_sec:            
                FSettlementGeneralRT.create_premium_t(trade, 'End Security', 'New', 0, None, tr_c, instr)
            if correct_trade:
                corrected_setl = get_corrected_setl(None, tr_c, 'End Cash')
                                        
            if instype == 'BuySellback' and (FSettlementGeneral.paydayOK(\
                instr.exp_day, trade, 1, 'End Cash') or correct_trade) and isNonZeroAmount(tr_c,\
                'End Cash', corrected_setl) and not already_created(tr_c, 'End Cash'):
                setl = ael.Settlement.new()
                setl.status = 'New'
                setl.type = 'End Cash'
                copy_protection_from_trade(setl, tr_c)
                validate_values(trade, setl, setl.type, corrected_setl, tr_c)
                FSettlementGeneral.append_transaction(setl)
        elif op=='UPDATE':
            if instype == 'BuySellback':
                try:
                    setl = ael.Settlement.select('trdnbr=%d' % trade.trdnbr)
                except:
                    setl = []
                found = 0
                if correct_trade:
                    corrected_setl = get_corrected_setl(None, trade, 'End Cash')

                for s in setl:
                    if s.type == 'End Cash':
                        if FSettlementGeneral.source_data(s):
                            new = s.new()
                            validate_values(trade, new, new.type, corrected_setl, tr_c)
                            paydayOK = FSettlementGeneral.paydayOK(\
                                new.value_day, new, 1, 'End Cash')
                            if paydayOK or corrected_setl:
                                FSettlementGeneralRT.update_setl_row(s, new, \
                                                                 'Updated')
                            else:
                                FSettlementGeneralRT.update_setl_row(s, new, \
                                                                 'Recalled')
                        found = 1
                        break
                
                if not found and isNonZeroAmount(trade, 'End Cash', corrected_setl) and \
                   trade.status in FSettlementGeneralRT.tr_status:
                    new_setl = ael.Settlement.new()
                    new_setl.status = 'New'
                    new_setl.type = 'End Cash'
                    copy_protection_from_trade(new_setl, trade)
                    validate_values(trade, new_setl, new_setl.type, corrected_setl, tr_c)
                    if FSettlementGeneral.paydayOK(\
                        new_setl.value_day, new_setl, 1, 'End Cash') or corrected_setl:
                        FSettlementGeneral.append_transaction(new_setl)
        elif op=='DELETE':
            if instype == 'BuySellback':
                try:
                    setl = ael.Settlement.select('trdnbr=%d' % trade.trdnbr)
                except:
                    setl = []    
                found = 0
                for s in setl:
                    if s.type == 'End Cash':
                        if FSettlementGeneral.source_data(s):
                            new = s.new()
                            FSettlementGeneralRT.update_setl_row(s, new,\
                                                                 'Recalled')
                        found = 1
                        break

def find_adjusted(seqnbr):    
    return FSettlementGeneral3.find_adjusted(seqnbr)

def find_parent(seqnbr):
    log(2, 'find_parent')
    try:
        sel = ael.Settlement.select('settle_seqnbr=%d' % seqnbr)    
        if sel:
            return sel[0]
    except:
        return None

def find_parent_2(seqnbr):
    log(2, 'find_parent_2')
    try:
        parent = None
        sel = ael.Settlement.select('ref_seqnbr=%d' % seqnbr)    
        if sel:
            for s in sel:
                if s.ref_type=='None':
                    parent = s
                break
        return parent
    except:
        return None

def update_net_hierarchy(settle, s_status, s_exp, parent, p_status, p_exp, cover, party_update = None):
    '''stt_c needed? '''
    log(2, 'update_net_hierarchy')
    global ret_settle
    settle.status = s_status
    se = ael.enum_from_string('StatusExplanation', s_exp)
    settle.status_explanation |= pow(2, se)
    pe = ael.enum_from_string('StatusExplanation', p_exp)
    parent.status_explanation |= pow(2, pe)
    parent.status = p_status
    intermediary_update = False
    parent_is_released_hold = False
    trade_update = False
    
    if party_update:
        intermediary_update = party_update.intermediary_update
        parent_is_released_hold = party_update.parent_is_released_hold
        trade_update = party_update.trade_update
        
    if intermediary_update:
        se2 = ael.enum_from_string('StatusExplanation', 'Change to account and/or intermediary data')
        settle.status_explanation |= pow(2, se2)
        parent.status_explanation |= pow(2, se2)
        
    if parent_is_released_hold and not trade_update:
        se3 = ael.enum_from_string('StatusExplanation', 'Party update: Void to Updated')
        settle.status_explanation |= pow(2, se3)
        parent.status_explanation |= pow(2, se3)

    if parent_is_released_hold and trade_update:
        se3 = ael.enum_from_string('StatusExplanation', 'Trd/Ins update: Void to Updated')
        settle.status_explanation |= pow(2, se3)
        parent.status_explanation |= pow(2, se3)

    if cover:        
        ret_settle = settle
        pr = 'Updating net hierarchy (setl:%d, parent:%d)' % (settle.seqnbr, parent.seqnbr)
        log(3, pr)
        parent.commit()
    else:
        FSettlementGeneral.append_transaction(settle)
        FSettlementGeneral.append_transaction(parent)

def delete_net_part(settle, delete, new, cover):

    log(2, 'delete_net_part')
    deleted = 0
    seqnbr = settle.seqnbr
    amount = settle.amount
    global ret_settle
    if settle:
        if settle.ref_seqnbr:
            parent = settle.ref_seqnbr
            if parent:
                if delete:
                    if FSettlementGeneral.get_mod_trans(settle.seqnbr):
                        FSettlementGeneral.remove_trans(settle.seqnbr)
                    FSettlementGeneral.append_delete(settle.seqnbr)    
                    settle.delete()
                    deleted = 1
                else:
                    clone2 = FSettlementGeneral.get_mod_trans(settle.seqnbr)
                    if not clone2:
                        clone2 = settle.clone()
                    if new:
                        FSettlementGeneralRT.update_values(clone2, new)
                    clone2.status = 'New'
                    clone2.ref_seqnbr = None
                    clone2.ref_type = 'None' #delete netting_rule_seqnbr
                    FSettlementGeneral.append_transaction(clone2)
                sel = ael.Settlement.select('ref_seqnbr=%d' % parent.seqnbr)
                delete_parent = 1
                for s in sel:
                    if not s.seqnbr==seqnbr and not \
                       FSettlementGeneral.is_deleted(s.seqnbr):
                        delete_parent = 0
                        clone = FSettlementGeneral.get_mod_trans(s.seqnbr)
                        if not clone:
                            clone = s.clone()
                        clone.status='New'
                        clone.ref_seqnbr=None
                        clone.ref_type='None' #delete netting_rule_seqnbr
                        if cover:
                            clone.commit()
                        else:
                            FSettlementGeneral.append_transaction(clone)
                if delete_parent and not \
                   FSettlementGeneral.is_deleted(parent.seqnbr):
                    FSettlementGeneral.append_delete(parent.seqnbr)
                    parent.delete()

    return deleted

def set_status_and_exp(clone, status, flag, cover, do_commit = False, party_update = False):
    '''Clone settlement gets new status as well as 
    status explanation. If cover=1 ret_setl will become clone
    otherwise clone is appended to the trans_dict.'''
    log(2, 'set_status_and_exp')
    clone.status=status
    global ret_settle
    parent_is_released_hold = False
    intermediary_update = False
    trade_update = False
    
    if party_update:
        parent_is_released_hold = party_update.parent_is_released_hold
        intermediary_update = party_update.intermediary_update
        trade_update = party_update.trade_update
    
    if flag:
        rd = ael.enum_from_string('StatusExplanation', 'Recalled data')
    else:
        rd = ael.enum_from_string('StatusExplanation', 'Change to source data')
        if intermediary_update:    
            rd2 = ael.enum_from_string('StatusExplanation', 'Change to account and/or intermediary data')
            if clone.ref_seqnbr:
                clone.text = clone.text.rstrip() + ' '
            clone.status_explanation |= pow(2, rd2)
        if parent_is_released_hold and not trade_update:
            rd3 = ael.enum_from_string('StatusExplanation', 'Party update: Void to Updated')
            clone.status_explanation |= pow(2, rd3)
        elif parent_is_released_hold and trade_update:
            rd4 = ael.enum_from_string('StatusExplanation', 'Trd/Ins update: Void to Updated')
            clone.status_explanation |= pow(2, rd4)

    clone.status_explanation |= pow(2, rd)
    
    if cover:
        ret_settle=clone
    elif do_commit:
        try:
            #Committing here because this code-snippet will be called from Prime.
            #The settlement will not be committed if append_transaction is
            #called.
            clone.commit()
        except Exception, error:
            log(0, 'ERROR in set_status_and_exp!')
            log(0, 'Could not commit settlement due to %s' % error)
    else:
        FSettlementGeneral.append_transaction(clone)

def set_protection_fields(settlement, protection, owner_user):
    if settlement:
        log(3, 'set_protection_fields')
        settlement.protection = protection
        settlement.owner_usrnbr = owner_user

def copy_protection_from_settlement(new_settle, old_seqnbr):
    old_settle = ael.Settlement[old_seqnbr]
    if old_settle:
        log(3, 'copy_protection_from_settlement')
        set_protection_fields(new_settle, old_settle.protection,
                              old_settle.owner_usrnbr.usrnbr)

def copy_protection_from_trade(settlement, trade):
    '''trade can be tr_c '''
    if trade:
        log(3, 'copy_protection_from_trade')
        set_protection_fields(settlement, trade.protection, trade.owner_usrnbr.usrnbr)

def new_settle(seqnbr, new, new_s, delete, cover, party_update = None):
    ''' '''
    log(2, 'new_settle')
    if new_s:
        if new:
            FSettlementGeneralRT.update_values(new_s, new)
            clear_fields(new_s)        
        new_s.ref_seqnbr = seqnbr
        parent_settlement = ael.Settlement[seqnbr]
        if parent_settlement and FSettlementGeneral3.has_the_keyword(parent_settlement):
            if not FSettlementGeneral3.has_the_keyword(new_s):
                paynbr = FSettlementGeneral3.get_paymentnbr_from_keyword(parent_settlement)
                if paynbr > 0:
                    str = 'PAYMENT=%d This payment references a closed payment with paynbr %d' % (paynbr, paynbr)
                    new_s.add_diary_note(str)
        if new_s.trdnbr:
            copy_protection_from_trade(new_s, new_s.trdnbr)
        else:
            copy_protection_from_settlement(new_s, seqnbr)
        
        if delete:
            if cover:
                set_status_and_exp(new, new.status, 1, cover)
                new_s.cfwnbr = None
                new_s.dividend_seqnbr = None
                new_s.paynbr = None
                set_status_and_exp(new_s, 'Recalled', 1, 0, 1)
            else:
                set_status_and_exp(new_s, 'Recalled', 1, cover)
        else:
            set_status_and_exp(new_s, 'Updated', 0, cover, 0, party_update)

def set_new_values(clone, new, status):

    log(2, 'set_new_values:')
    if new and clone and status:
        FSettlementGeneralRT.update_values(clone, new)
        clone.status = status
        FSettlementGeneral.append_transaction(clone)
    
def update_from_status(seqnbr, new, party_update = None):
    ''' '''
    log(2, 'update_from_status')
    settle = ael.Settlement[seqnbr]
    if settle:
        if do_not_update_recalled_settlement(settle):
            return
        clone = FSettlementGeneral.get_mod_trans(settle.seqnbr)
        if not clone:
            clone = settle.clone()
        if clone.status in A_status or clone.status in B_status:
            if clone.status == 'Updated':
                set_new_values(clone, new, 'Updated')
            else:
                set_new_values(clone, new, 'Exception')
        elif clone.status in C_status:
            if clone.manual_match:
                set_status_and_exp(clone, 'Exception', 0, 0)
                new_s = ael.Settlement.new()
                new_settle(clone.seqnbr, new, new_s, 0, 0)
            else:
                set_new_values(clone, new, 'Exception')
        elif clone.status in H_status:
            set_status_and_exp(clone, clone.status, 0, 0, 0, party_update)
            new_s = ael.Settlement.new()
            new_settle(clone.seqnbr, new, new_s, 0, 0, party_update)
        elif clone.status in D_status:
            clone.post_settle_action = 1
            set_status_and_exp(clone, clone.status, 0, 0, 0, party_update)
            new_s = ael.Settlement.new()
            new_settle(clone.seqnbr, new, new_s, 0, 0, party_update)
        elif clone.status=='Void':
            if not cancelled_explanation(clone.status_explanation) and \
               clone.manual_match:
                clone.post_settle_action = 1
                set_status_and_exp(clone, 'Void', 0, 0, 0, party_update)
                new_s = ael.Settlement.new()
                new_settle(clone.seqnbr, new, new_s, 0, 0, party_update)
            else:
                set_new_values(clone, new, 'Exception')
            

def cancelled_explanation(explanation):

    log(2, 'cancelled_explenation:')
    ok = 1
    if explanation:
        cu = ael.enum_from_string('StatusExplanation', 'Cancelled by us')
        cc = ael.enum_from_string('StatusExplanation', 'Cancelled by the counterparty')
        if (explanation & pow(2, cu)):
            ok = 0
        if (explanation & pow(2, cc)):
            ok = 0
    return ok
    
def delete_from_status(seqnbr, cover):

    log(2, 'delete_from_status:')
    settle = ael.Settlement[seqnbr]
    removed=0
    if settle:
        if settle.status in A_status or settle.status in B_status:
            if FSettlementGeneral.get_mod_trans(settle.seqnbr):
                FSettlementGeneral.remove_trans(settle.seqnbr)
            if not FSettlementGeneral.is_deleted(seqnbr):
                FSettlementGeneral.append_delete(settle.seqnbr)
                settle.delete()
            removed = 1
        elif settle.status in C_status:
            if settle.manual_match:
                clone = FSettlementGeneral.get_mod_trans(settle.seqnbr)
                if not clone:
                    clone = settle.clone()
                set_status_and_exp(clone, 'Exception', 1, cover)
                new_s = ael.Settlement.new()
                new_settle(clone.seqnbr, clone, new_s, 1, cover)
            else:
                if FSettlementGeneral.get_mod_trans(settle.seqnbr):
                    FSettlementGeneral.remove_trans(settle.seqnbr)
                FSettlementGeneral.append_delete(settle.seqnbr)    
                settle.delete()
                removed = 1
        elif settle.status in H_status:
            clone = FSettlementGeneral.get_mod_trans(settle.seqnbr)
            if not clone:
                clone = settle.clone()
            set_status_and_exp(clone, clone.status, 1, cover)
            new_s = ael.Settlement.new()
            new_settle(clone.seqnbr, clone, new_s, 1, cover)
        elif settle.status in D_status:
            clone = FSettlementGeneral.get_mod_trans(settle.seqnbr)
            if not clone:
                clone = settle.clone()
            clone.post_settle_action = 1
            set_status_and_exp(clone, clone.status, 1, cover)
            new_s = ael.Settlement.new()
            new_settle(clone.seqnbr, clone, new_s, 1, cover)
        elif settle.status == 'Void':
            if cancelled_explanation(settle.status_explanation) and not \
               settle.manual_match:
                if FSettlementGeneral.get_mod_trans(settle.seqnbr):
                    FSettlementGeneral.remove_trans(settle.seqnbr)
                FSettlementGeneral.append_delete(settle.seqnbr)    
                settle.delete()
                removed = 1
            else:
                clone = FSettlementGeneral.get_mod_trans(settle.seqnbr)
                if not clone:
                    clone = settle.clone()
                clone.post_settle_action = 1
                set_status_and_exp(clone, 'Void', 1, cover)
                new_s = ael.Settlement.new()
                new_settle(clone.seqnbr, clone, new_s, 1, cover)
    return removed
    
def delete_update_adjusted(seqnbr, delete, new, cover, party_update = None):

    log(2, 'delete_update_adjusted')
    settle = ael.Settlement[seqnbr]
    clone = FSettlementGeneral.get_mod_trans(settle.seqnbr)
    if not clone:
        clone = settle.clone()
    removed = 0

    parent = find_parent(seqnbr)
    parent2 = find_parent_2(seqnbr)
    if parent:
        clone_p = FSettlementGeneral.get_mod_trans(parent.seqnbr)
        if not clone_p:
            clone_p = parent.clone()
        # Update of normally adjusted settlement
        if parent.settle_category=='Adjusted' or parent.settle_category=='Good Value' \
           or parent.settle_category=='Fair Value' or parent.settle_category=='Compensation Payment' \
           or parent.settle_category=='Compensation Claim':
            if delete:
                set_status_and_exp(clone, 'Recalled', 1, cover)
            else:
                if do_not_update_recalled_settlement(settle):
                    return removed
                if new:
                    FSettlementGeneralRT.update_values(clone, new)
                if parent.status in H_status or parent.status in D_status:
                    if party_update:
                        party_update.parent_is_released_hold = True
                    else:
                        party_update = FSettlementGeneral3.PartyUpdate(False, True, True)
                set_status_and_exp(clone, 'Updated', 0, cover, 0, party_update)
        # Update of settlement that are post settlement and has new
        # referenced settlement with update values
        else:
            return removed
        
        if parent.status in A_status or parent.status in B_status or \
           parent.status in C_status:
            set_status_and_exp(clone_p, 'Exception', delete, cover)
        elif parent.status in H_status:
            if party_update:
                party_update.parent_is_released_hold = True
            else:
                party_update = FSettlementGeneral3.PartyUpdate(False, True, True)
            set_status_and_exp(clone_p, clone_p.status, delete, cover, 0, party_update)
        elif parent.status in D_status:
            clone_p.post_settle_action = 1
            if party_update:
                party_update.parent_is_released_hold = True
            else:
                party_update = FSettlementGeneral3.PartyUpdate(False, True, True)
            set_status_and_exp(clone_p, clone_p.status, delete, cover, 0, party_update)
        elif parent.status=='Void':
            if cancelled_explanation(parent.status_explanation):
                set_status_and_exp(clone_p, 'Exception', delete, cover)
            else:
                clone_p.post_settle_action=1
                set_status_and_exp(clone_p, 'Void', delete, cover)
        return removed
    elif parent2:
        clone_p = FSettlementGeneral.get_mod_trans(parent2.seqnbr)
        if not clone_p:
            clone_p = parent2.clone()
        if delete:
            rd = ael.enum_from_string('StatusExplanation', 'Recalled data')           
            rc = ael.enum_from_string('StatusExplanation', 'Change to source data')
            clone.status_explanation |= pow(2, rd)
            clone.status_explanation &=~pow(2, rc)
            FSettlementGeneral.append_transaction(clone)
            clone_p.status_explanation |= pow(2, rd)
            clone_p.status_explanation &=~pow(2, rc)
            set_status_and_exp(clone_p, 'Recalled', delete, cover)
        else:
            if do_not_update_recalled_settlement(clone_p):
                pass
            else:
                new_settle(seqnbr, new, clone_p, delete, cover, party_update)
        return removed

def update_split_parts(seqnbr,delete, cover, party_update = None):

    log(2, 'update_split_parts:')
    ret = False
    try:    
        sel = ael.Settlement.select('ref_seqnbr=%d' % seqnbr)
    except:
        sel = []        
    for s in sel:
        adj = find_adjusted(s.seqnbr)
        if adj:
            clone = FSettlementGeneral.get_mod_trans(adj.seqnbr)
            if not clone:
                clone = adj.clone()
            clone2 = FSettlementGeneral.get_mod_trans(s.seqnbr)
            if not clone2:
                clone2 = s.clone()
            if delete:
                set_status_and_exp(clone2, 'Recalled', delete, cover)
            else:
                set_status_and_exp(clone2, 'Updated', delete, cover)
        else:
            clone = FSettlementGeneral.get_mod_trans(s.seqnbr)
            if not clone:
                clone = s.clone()
        if clone.status in A_status or clone.status in B_status or \
           clone.status in C_status:
            set_status_and_exp(clone, 'Exception', delete, cover)
        elif clone.status in H_status:
            ret = True
            if party_update:
                party_update.parent_is_released_hold = True
            else:
                party_update = FSettlementGeneral3.PartyUpdate(False, True, True)
            set_status_and_exp(clone, clone.status, delete, cover, 0, party_update)
        elif clone.status in D_status:
            ret = True
            if party_update:
                party_update.parent_is_released_hold = True
            else:
                party_update = FSettlementGeneral3.PartyUpdate(False, True, True)
            clone.post_settle_action = 1
            set_status_and_exp(clone, clone.status, delete, cover, 0, party_update)
        elif clone.status=='Void':
            if cancelled_explanation(clone.status_explanation):
                set_status_and_exp(clone, 'Exception', delete, cover)
            else:
                clone.post_settle_action=1
                set_status_and_exp(clone, 'Void', delete, cover)
    return ret
    

def delete_referenced(seqnbr, cover):

    log(2, 'delete_referenced:')
    settle = ael.Settlement[seqnbr]
    exp = 'Recalled data'
    removed = 0
    parent = None
    if settle:
        if settle.ref_seqnbr:
            parent = ael.Settlement[settle.ref_seqnbr.seqnbr]
        if parent:
            adjusted=find_adjusted(parent.seqnbr)
            if adjusted:
                updated_referenced_adjusted(settle, parent, adjusted, 1, None, \
                                            cover)
            else:
                if settle.ref_seqnbr and settle.ref_type=='Net Part':
                    if parent.status in A_status or parent.status=='New' or \
                       parent.status=='Manual Match':
                        removed = delete_net_part(settle, 1, None, cover)
                    elif parent.status in C_status or parent.status=='Exception':
                        if parent.manual_match:
                            p_c = FSettlementGeneral.get_mod_trans(parent.seqnbr)
                            if not p_c:
                                p_c = parent.clone()
                            s_c = FSettlementGeneral.get_mod_trans(settle.seqnbr)
                            if not s_c:
                                s_c = settle.clone()
                            update_net_hierarchy(s_c, 'Recalled', exp, p_c,\
                                                 'Exception', exp, cover)
                        else:
                            removed=delete_net_part(settle, 1, None, cover)
                    elif parent.status in D_status or parent.status in H_status \
                        or (parent.status=='Void' \
                        and not cancelled_explanation(parent.status_explanation)) \
                        or (parent.status=='Void' and parent.manual_match):
                        p_c = parent.clone()
                        s_c = settle.clone()
                        p_c.post_settle_action=1
                        update_net_hierarchy(s_c, 'Recalled', exp, p_c, \
                                             p_c.status, exp, cover)
                    elif parent.status=='Void' and \
                         cancelled_explanation(parent.status_explanation):
                         removed = delete_net_part(settle, 1, None, cover)
                elif settle.ref_seqnbr and settle.ref_type=='Ad_hoc Net':
                    p_c = FSettlementGeneral.get_mod_trans(parent.seqnbr)
                    if not p_c:
                        p_c = parent.clone()
                    s_c = FSettlementGeneral.get_mod_trans(settle.seqnbr)
                    if not s_c:
                        s_c = settle.clone()
                    if parent.status in A_status or parent.status in B_status \
                       or parent.status in C_status:    
                        update_net_hierarchy(s_c, 'Recalled', exp, p_c, \
                                             'Exception', exp, cover)
                    elif parent.status in H_status:                                    
                        update_net_hierarchy(s_c, 'Recalled', exp, p_c,\
                                             p_c.status, exp, cover)
                    elif parent.status in D_status:
                        p_c.post_settle_action = 1
                        update_net_hierarchy(s_c, 'Recalled', exp, p_c,\
                                             p_c.status, exp, cover)
                    elif parent.status == 'Void':
                        if cancelled_explanation(parent.status_explanation):
                            update_net_hierarchy(s_c, 'Recalled', exp, p_c,\
                                                 'Exception', exp, cover)
                        else:
                            p_c.post_settle_action=1
                            update_net_hierarchy(s_c, 'Recalled', exp, p_c,\
                                                 'Void', exp, cover)
        elif settle.ref_type=='Split':
            update_split_parts(seqnbr, 1, cover)
            clone = FSettlementGeneral.get_mod_trans(settle.seqnbr)
            if not clone:
                clone = settle.clone()
            set_status_and_exp(clone, 'Recalled', 1, cover)
    return removed

def updated_referenced_adjusted(settle, parent, adj, delete, new, cover):

    log(2, 'updated_referenced_adjusted:')
    if settle and parent and adj:
        if delete:
            exp = 'Recalled data'
        else:
            exp = 'Change to source data'
        s_clone = FSettlementGeneral.get_mod_trans(settle.seqnbr)
        if not s_clone:
            s_clone = settle.clone()
        p_clone = FSettlementGeneral.get_mod_trans(parent.seqnbr)
        if not p_clone:
            p_clone = parent.clone()
        a_clone = FSettlementGeneral.get_mod_trans(adj.seqnbr)
        if not a_clone:
            a_clone = adj.clone()
        if not delete and new:
            FSettlementGeneralRT.update_values(s_clone, new)
        if delete:
            update_net_hierarchy(s_clone, 'Recalled', exp, p_clone,\
                                 'Updated', exp, cover)
        else:
            update_net_hierarchy(s_clone, 'Updated', exp, p_clone,\
                                 'Updated', exp, cover)
        if adj.status in A_status or adj.status in B_status or \
           adj.status in C_status:
            set_status_and_exp(a_clone, 'Exception', delete, cover)
        elif adj.status in H_status:
            set_status_and_exp(a_clone, adj.status, delete, cover)
        elif adj.status in D_status:
            a_clone.post_settle_action=1
            set_status_and_exp(a_clone, adj.status, delete, cover)
        elif adj.status=='Void' and not cancelled_explanation(adj.status_explanation):
            a_clone.post_settle_action=1
            set_status_and_exp(a_clone, 'Void', delete, cover)
        elif adj.status=='Void' and cancelled_explanation(adj.status_explanation):
            set_status_and_exp(a_clone, 'Exception', delete, cover)
            
        
def update_referenced(seqnbr, new, party_update = None):

    log(2, 'update_referenced:')
    settle = ael.Settlement[seqnbr]
    exp = 'Change to source data'
    if settle:
        if do_not_update_recalled_settlement(settle):
            return
        parent = None
        if settle.ref_seqnbr:
            parent = ael.Settlement[settle.ref_seqnbr.seqnbr]
        if parent:
            adjusted=find_adjusted(parent.seqnbr)
            if adjusted:
                updated_referenced_adjusted(settle, parent, adjusted, 0, new, 0)
            else:
                if settle.ref_type=='Net Part' and parent.ref_type=='Net':
                    if parent.status in A_status or parent.status=='New' or \
                       parent.status=='Manual Match':
                        delete_net_part(settle, 0, new, 0)
                    elif parent.status in C_status or parent.status=='Exception':
                        if parent.manual_match:
                            p_c = FSettlementGeneral.get_mod_trans(parent.seqnbr)
                            if not p_c:
                                p_c = parent.clone()
                            s_c = FSettlementGeneral.get_mod_trans(settle.seqnbr)
                            if not s_c:
                                s_c = settle.clone()
                            if new:
                                FSettlementGeneralRT.update_values(s_c, new)
                            update_net_hierarchy(s_c, 'Updated', exp, p_c,\
                                                 'Exception', exp, 0)
                        else:
                            delete_net_part(settle, 0, new, 0)
                    elif parent.status in H_status:
                        p_c = FSettlementGeneral.get_mod_trans(parent.seqnbr)
                        if not p_c:
                            p_c = parent.clone()
                        s_c = FSettlementGeneral.get_mod_trans(settle.seqnbr)
                        if not s_c:
                            s_c = settle.clone()                        
                        if new:
                            FSettlementGeneralRT.update_values(s_c, new)
                        if party_update:
                            party_update.parent_is_released_hold = True
                        else:
                            party_update = FSettlementGeneral3.PartyUpdate(False, True, True)
                        update_net_hierarchy(s_c, 'Updated', exp, p_c,\
                                             p_c.status, exp, 0, party_update)
                    elif parent.status in D_status:
                        p_c = FSettlementGeneral.get_mod_trans(parent.seqnbr)
                        if not p_c:
                            p_c = parent.clone()
                        s_c = FSettlementGeneral.get_mod_trans(settle.seqnbr)
                        if not s_c:
                            s_c = settle.clone()
                        p_c.post_settle_action = 1
                        if new:
                            FSettlementGeneralRT.update_values(s_c, new)
                        if party_update:
                            party_update.parent_is_released_hold = True
                        else:
                            party_update = FSettlementGeneral3.PartyUpdate(False, True, True)
                        update_net_hierarchy(s_c, 'Updated', exp, p_c,\
                                             p_c.status, exp, 0, party_update)
                    elif parent.status=='Void':
                        p_c = FSettlementGeneral.get_mod_trans(parent.seqnbr)
                        if not p_c:
                            p_c = parent.clone()
                        s_c = FSettlementGeneral.get_mod_trans(settle.seqnbr)
                        if not s_c:
                            s_c = settle.clone()
                        p_c.post_settle_action = 1
                        if new:
                            FSettlementGeneralRT.update_values(s_c, new)
                        update_net_hierarchy(s_c, 'Updated', exp, p_c,\
                                             p_c.status, exp, 0, party_update)
                elif settle.ref_type=='Net Part' and \
                     parent.ref_type=='Ad_hoc Net':
                    'This function can also be called from delete_update_adjusted'
                    'and then it has not got a new parameter'
                    p_c = FSettlementGeneral.get_mod_trans(parent.seqnbr)
                    if not p_c:
                        p_c = parent.clone()
                    s_c = FSettlementGeneral.get_mod_trans(settle.seqnbr)
                    if not s_c:
                        s_c = settle.clone()
                    if new:
                        FSettlementGeneralRT.update_values(s_c, new)
                    if parent.status in A_status or parent.status in B_status \
                       or parent.status in C_status:
                        update_net_hierarchy(s_c, 'Updated', exp, p_c,\
                                             'Exception', exp, 0)
                    elif parent.status in H_status:
                        if party_update:
                            party_update.parent_is_released_hold = True
                        else:
                            party_update = FSettlementGeneral3.PartyUpdate(False, True, True)
                        update_net_hierarchy(s_c, 'Updated', exp, p_c,\
                                             p_c.status, exp, 0, party_update)
                    elif parent.status in D_status:
                        p_c.post_settle_action = 1
                        if party_update:
                            party_update.parent_is_released_hold = True
                        else:
                            party_update = FSettlementGeneral3.PartyUpdate(False, True, True)
                        update_net_hierarchy(s_c, 'Updated', exp, p_c,\
                                             p_c.status, exp, 0, party_update)
                    elif parent.status=='Void':
                        if cancelled_explanation(p_c.status_explanation):
                            update_net_hierarchy(s_c, 'Updated', exp, p_c,\
                                                 'Exception', exp, 0, party_update)
                        else:
                            p_c.post_settle_action = 1
                            update_net_hierarchy(s_c, 'Updated', exp, p_c,\
                                                 'Void', exp, 0, party_update)
        elif settle.ref_type=='Split':
            s_c = FSettlementGeneral.get_mod_trans(settle.seqnbr)
            if not s_c:
                s_c = settle.clone()
            FSettlementGeneralRT.update_values(s_c, new)
            is_released_hold = update_split_parts(seqnbr, 0, 0, party_update)
            if is_released_hold and not party_update:
                party_update = FSettlementGeneral3.PartyUpdate(False, True, True)
            set_status_and_exp(s_c, 'Updated', 0, 0, 0, party_update)
                
def handle_recalled(seqnbr, cover):
    #If cover=1, the function has been called from
    #FSettlementGeneral.update_settle_and_references_cover
    #FUNCTION_CALLED_FROM_PRIME do not touch!
    global ret_settle
    removed=1
    clone = None
    pr = "FSettlementGeneral.handle_recalled(settl=%d,cover=%d) about to delete settlement" % (seqnbr, cover)    
    log(2, pr)
    settle = ael.Settlement[seqnbr]
    
    if FSettlementGeneral3.is_do_not_delete_diary_ref(settle):
        return ret_settle
        
    if not FSettlementGeneral.check_references(seqnbr):
        if not FSettlementGeneral.check_referenced_to(seqnbr, 0):
            removed = delete_from_status(seqnbr, cover)
        else:
            removed = delete_update_adjusted(seqnbr, 1, None, cover)
    else:
        removed = delete_referenced(seqnbr, cover)
    if ret_settle:
        clone = ret_settle.clone()
        ret_settle = None
    return clone
            
def handle_updates(seqnbr, new, party_update = None):

    #Check if the settlement is part of netting or splitted
    log(2, 'Handling updated settlement')
    if not FSettlementGeneral.check_references(seqnbr):
        #Check if settlement has been adjusted
        if not FSettlementGeneral.check_referenced_to(seqnbr, 0):
            #Update single settlement
            update_from_status(seqnbr, new, party_update)
        else:
            delete_update_adjusted(seqnbr, 0, new, 0, party_update)
    else:
        #Update settlement part of net of result of split
        update_referenced(seqnbr, new, party_update)
    return 1
            
def handle_changed_source_data(seqnbr, new, status, party_update = None):
    
    settle = None
    if seqnbr and status:
        if status == 'Recalled':
            settle = handle_recalled(seqnbr, 0)
        elif status == 'Updated':
            settle = handle_updates(seqnbr, new, party_update)
    return settle

# Below follows a number of functions for dealing with position, coupon
# and repo instruments
def coupon_transfer_amount(trade, cf, cf_c=None):
    ''' inc_c ?'''
    if not trade or not cf or not trade.insaddr:
        return 0
    cf_c = FSettlementGeneralRT.set_c(cf_c, cf, 'CashFlow')
    instr = trade.insaddr
    
    if not FSettlementGeneral.enter_cashflow(trade, cf, cf_c):
        return 0
    if instr.instype=='Repo/Reverse' or instr.instype=='SecurityLoan':
        und_instr = instr.und_insaddr
        if not und_instr:
            return 0
        amount=trade.quantity * instr.ref_value/\
                und_instr.nominal_amount(trade.value_day)
    else:
        amount = trade.quantity
    amount = amount * cf.projected_cf()
    amount = 0 - amount
    return amount
        
def coupon_transfer(trade, cf, cf_c=None, leg_c=None):
    '''Incomming trade is not tr_c '''
    instr = trade.insaddr
    instypes = ['Repo/Reverse', 'SecurityLoan']
    cf_c = FSettlementGeneralRT.set_c(cf_c, cf, 'CashFlow')
    if ((instr and instr.instype in instypes) or \
       FSettlementGeneral.is_collateral_trade(trade)) and \
       trade.status in param.status and \
       FSettlementGeneral.is_prevent_cash_flow(cf) == False:
        amount = coupon_transfer_amount(trade, cf, cf_c)
        new = ael.Settlement.new()
        new.type = 'Coupon transfer'        
        FSettlementGeneral.cf_creation(new, cf, 'New', 0, trade, 1, amount, 0, 0, leg_c, cf_c)

def update_coupon_transfer(trade, cf, cf_c=None, leg_c=None):
    ''' '''
    
    if not trade or not cf or \
       trade.status not in param.status:
        return
    cf_c = FSettlementGeneralRT.set_c(cf_c, cf, 'CashFlow')
    settles = get_coupon_transfer_settlement_records(cf, trade) # no need for stt_c below
    for settle in settles:
        obj_list = FSettlementGeneral.create_from_settle([settle])
        if len(obj_list):
            obj = obj_list[0]
            obj.amount = coupon_transfer_amount(trade, cf, cf_c)
            obj.curr = FSettlementGeneral.get_cf_curr(cf_c, leg_c)
            if obj.amount == 0 or FSettlementGeneral.is_prevent_cash_flow(cf) == True:
                obj.status = 'Recalled'
            else:
                obj.status = 'Updated'
            pr = "%s Coupon transfer (File)" % (obj.status)
            log(2, pr)
            FSettlementGeneralRT.update_row(settle, obj)

def find_coupons(cf, settle_type, do_add_closed_settl=0):
    '''cf_c ok '''
    settles = []
    settle_sel = []
    
    if type(cf) == int:
        cf = ael.CashFlow[cf]
        
    settle_sel = ael.Settlement.select('cfwnbr=%d' % cf.cfwnbr)
    for s in settle_sel:
        if s.type == settle_type and FSettlementGeneral.source_data(s):
            if not s.status=='Closed' or \
            (s.status=='Closed' and do_add_closed_settl):
                settles.append(s)
    return settles
    
def get_coupon_transfer_settlement_records(cashflow, trade):
    """
    Used instead of find_coupons when retrieving settlement records of type
    Coupon transfer.
    """
    settlements = []
    selection = ael.Settlement.select('cfwnbr=%d' % cashflow.cfwnbr)
    for settlement in selection:
        if settlement.type == 'Coupon transfer' and \
           settlement.trdnbr and \
           settlement.trdnbr.trdnbr == trade.trdnbr and \
           FSettlementGeneral.source_data(settlement) and not \
           settlement.status =='Closed':
            settlements.append(settlement)
    return settlements

def port_comparison(settle, prfnbr):
    return FSettlementGeneral3.port_comparison(settle, prfnbr)

def update_coupon_value(coupon, pos, typ, ipa):
    '''No need for ent_c'''
    obj_list = FSettlementGeneral.create_from_settle([coupon])
    if len(obj_list):
        obj = obj_list[0]
        old_amount = obj.amount
        old_status = obj.status
        if typ=='CashFlow':
            if obj.cfwnbr:
                cf = ael.CashFlow[obj.cfwnbr]
                obj.amount =  pos * cf.projected_cf()
                coupon_already_exists, new_amount = FSettlementGeneral3.intact_coupon_amount(obj)
                if coupon_already_exists and round(new_amount, 6) != 0:
                    obj.amount = new_amount
                obj.curr = FSettlementGeneral.get_cf_curr(coupon.cfwnbr)
        elif typ=='Dividend':
            # EquitySwap dividend handling before Prime 3.2.2.x
            if obj.dividend_seqnbr:
                div = ael.Dividend[obj.dividend_seqnbr]
                obj.amount = get_dividend(div, None, div.insaddr, pos)
                obj.curr = div.curr.insaddr
                
        if obj.amount < 0 and not ipa: #Can't pay to the issuer
            obj.amount = 0
            
        if round(old_amount, 6) == round(obj.amount, 6) and old_status == obj.status: #No update needed
            return
            
        if obj.amount == 0:
            obj.status = 'Recalled'
        else:
            obj.status = 'Updated'
        
        cv = ''
        if coupon.cfwnbr:
            cv = "%d" % (coupon.cfwnbr.cfwnbr)
        pr = "%s Coupon %s value (File)" % (obj.status, cv)
        log(2, pr)
        FSettlementGeneralRT.update_row(coupon, obj)

def create_coupon(settle, cf, pos, insaddr, cf_c=None, leg_c=None, cf_list=[]):
    '''update position mostly deals with entities but cf_c migh occur.
    settle can be stt_c'''
    if settle and cf and pos and settle.trdnbr:
        cf_c = FSettlementGeneralRT.set_c(cf_c, cf, 'CashFlow')
        amount = pos * cf.projected_cf()
        new = ael.Settlement.new()
        if cf_c.type=='Fixed Rate' or is_float_coupon(cf, cf, leg_c):
            new.type = 'Coupon'
        elif cf.type=='Fixed Amount':
            new.type = 'Redemption'
        corrected_setl = 0
        correct_trade = is_correction_trade(settle.trdnbr)
        if correct_trade:
            corrected_setl = get_corrected_setl(cf, settle.trdnbr, None)

        if len(cf_list) == 0:
            new_cf = FSettlementGeneral.cf_creation(new, cf, 'New', 0, settle.trdnbr, 1, amount,\
                    insaddr, corrected_setl, leg_c, cf_c, settle.trdnbr, 1)
        else:
            new_cf = FSettlementGeneral.cf_creation(new, cf, 'New', 0, settle.trdnbr, 1, amount,\
                    insaddr, corrected_setl, leg_c, cf_c, settle.trdnbr, 0)

            cf_list.append(new_cf)
            
            # if exactly the same settlement is there do not create a new coupon (status differs)
            # if status and amount differ then diff should be new amount
            coupon_already_exists, new_amount = FSettlementGeneral3.intact_coupon_amount(new_cf)
            pr = "%d %s already exists: %d, new_amount will be %f" % (new_cf.cfwnbr.cfwnbr, \
                new_cf.type, coupon_already_exists, new_amount)
            log(4, pr)
            new_cf_updated = 0
            if coupon_already_exists and round(new_amount, 6) != 0:
                new_cf.amount = new_amount
                new_cf_updated = 1

            if not coupon_already_exists or new_cf_updated:
                FSettlementGeneral.append_transaction(new_cf)
                FSettlementGeneral.print_commit(new_cf)
            else:
                pr = "%s for CF %d already exist no creation will be done!" % (new.type, cf.cfwnbr)
                log(4, pr)

def create_dividend(secnom, div, pos, insaddr, append_trans = 1):
    '''secnom can be stt_c '''
   
    if secnom and div and pos:
        new = ael.Settlement.new()
        return FSettlementGeneral.dividend_creation(new, div, 'New', 0, secnom.trdnbr, 1, pos, None, None, append_trans)
        
def acq_comparison(trade, settle, typ, obj, leg_c=None, tr_c=None):
    '''obj can be div_c or cf_c. '''
    ok = 0
    tr_acq = ''
    tr_acc_name = ''
    acq_links = []
    tr_c = FSettlementGeneralRT.set_c(tr_c, trade, 'Trade')
    if typ in ['Coupon', 'Dividend', 'Redemption']:
        tr_acq = FSettlementGeneral.get_acquirer(trade)
        links = FSettlementGeneral.get_tals(settle, trade)    
        for l in links:
            if l.party_type=='Intern Dept':
                acq_links.append(l)
        del_obj = FSettlementGeneral.DeliveryType()
        setl = FSettlementGeneral3.Settlement()
        setl.acquirer_ptyid = tr_acq
        setl.type = typ
        setl.value_day = obj.pay_day
        if typ in ['Coupon', 'Redemption']:
            setl.curr = FSettlementGeneral.get_cf_curr(obj, leg_c)
        elif obj.curr:
            setl.curr = obj.curr.insaddr
        FSettlementGeneral.set_account(setl, acq_links, 1, 1, del_obj)
        if settle.acquirer_accname == setl.acquirer_accname and \
           settle.acquirer_ptyid == setl.acquirer_ptyid:
            ok = 1
        else:
            if settle.acquirer_accname != setl.acquirer_accname:
                pr = "acq_comparison; different acq accounts (%s vs %s) File" % (settle.acquirer_accname, setl.acquirer_accname)
                log(3, pr)
            elif settle.acquirer_ptyid != setl.acquirer_ptyid:                                
                pr = "acq_comparison; different aquirers (%s vs %s) File" % (settle.acquirer_ptyid, setl.acquirer_ptyid)
                log(3, pr)
    
    log(3, "acq_comparison; %d" % (ok))
    return ok
    
def get_position(settle, date):
    '''Settle is security nominal!
    settle can be stt_c'''
    
    pos = 0
    if not settle.sec_insaddr:
        return pos
    instr = settle.sec_insaddr
    if not param.alternative_coupon_handling:
        port = None
        account = None        
        accname = settle.acquirer_accname
        accid = settle.acquirer_ptyid
    
        if settle.to_prfnbr:
            port = settle.to_prfnbr
        elif settle.from_prfnbr:
            port = settle.from_prfnbr
        if accid:
            party = ael.Party[accid]
            if party:
                ptynbr = party.ptynbr
                account = ael.Account.read('ptynbr=%d and name="%s"' % \
                                           (ptynbr, accname))
        if instr and account:
            pos = instr.position(None, None, None, date, None, port, 1, account, 1)
    else:                
        secnom_accounts = []
        trades = instr.trades().members()
        if settle.trdnbr and settle.trdnbr.insaddr:
            ins = settle.trdnbr.insaddr
            trs = ins.trades().members()
            for tr in trs:
                if tr not in trades:
                    trades.append(tr)
        for tr in trades:         
            acc = FSettlementGeneral3.get_secnom_acc_if_closed(tr)   #how about terminated
            if acc and acc not in secnom_accounts:
                secnom_accounts.append(acc)        

        for acc in secnom_accounts:        
            pos += instr.position(None, None, None, date, None, None, 1, acc, 1)

    return pos

def update_position(secnom, typ, tr_c = None, leg_c=None, cf_c=None):
    '''No ins_c here because it is secnom.sec_insaddr! 
    secnom can be stt_c'''
    update = 0
    trade = secnom.trdnbr
    instr = secnom.sec_insaddr
    if not trade:
        return    
    tr_c = FSettlementGeneralRT.set_c(tr_c, trade, 'Trade')
    if tr_c and tr_c.trdnbr != trade.trdnbr:
        pr = "update_position: different trades %d != %d" % (tr_c.trdnbr, trade.trdnbr)
        log(2, pr)
        tr_c = None

    if tr_c and not FSettlementGeneral.is_valid_instrument(instr):
        pr = "%s is not valid Instrument type, no position update" % (instr.instype)
        log(2, pr)
        return

    ipa = 0
    if FSettlementGeneral.issuing_paying_agent_position(tr_c):
        ipa = 1
    if typ == 'Bond':
        if tr_c.insaddr and tr_c.insaddr.instype in \
           FSettlementGeneral.und_ins_security:
            und_ins = tr_c.insaddr.und_insaddr
            cfs = FSettlementGeneralRT.coupons_from_tr(None, und_ins)
        else:
            cfs = FSettlementGeneralRT.coupons_from_tr(tr_c, None) 
        
        for cf in cfs:
            update = 0
            ent_c = cf # careful with cf_c from here
            # use amb where possible
            if cf_c:
                if cf.cfwnbr == cf_c.cfwnbr:
                    ent_c = cf_c
                else:
                    leg_c = None
            else:
                leg_c = None    
            if FSettlementGeneral.paydayOK(ent_c.pay_day, cf, 1, '') and \
                FSettlementGeneral.enter_cashflow(tr_c, cf, ent_c):
                pos = get_position(secnom, ent_c.pay_day)
                coupon_type = 'Coupon'
                if ent_c.type == 'Fixed Amount':
                    coupon_type = 'Redemption'
                coupons = find_coupons(ent_c, coupon_type, 1) #1 for even closed cf settls
                for coupon in coupons:
                    if coupon.status not in ['Closed']:
                        if not param.alternative_coupon_handling:
                            prfnbr = 0
                            if coupon.to_prfnbr:
                                prfnbr = coupon.to_prfnbr.prfnbr
                            if acq_comparison(trade, coupon, coupon_type, ent_c, leg_c, tr_c) and \
                               port_comparison(secnom, prfnbr):
                                update_coupon_value(coupon, pos, 'CashFlow', ipa)
                                update = 1
                        else:
                            update_coupon_value(coupon, pos, 'CashFlow', ipa)
                            update = 1

                if not update and (pos > 0 or ipa):
                    create_coupon(secnom, cf, pos, instr.insaddr, ent_c, leg_c, coupons)

                # For repo instruments there are coupon transfers as well
                settles = find_coupons(ent_c, 'Coupon transfer', True)
                transfer_found=0
                for item in settles:
                    if item.trdnbr and \
                       item.trdnbr.trdnbr == secnom.trdnbr.trdnbr and \
                       item.type=='Coupon transfer':
                        transfer_found=1
                        break
                if transfer_found:
                    update_coupon_transfer(trade, cf, ent_c, leg_c)
                else:
                    coupon_transfer(secnom.trdnbr, cf, ent_c, leg_c)
                
    elif typ == 'Stock':
        # note this is only type not the real instype Stock
        # EquitySwap dividend does not need to be implemented here
        divs = FSettlementGeneralRT.divs_from_instrument(instr, None, 1)
        for div in divs:    
            update = 0
            if div.seqnbr and FSettlementGeneral.paydayOK(div.pay_day,\
                div, 1, '') and FSettlementGeneral.enter_dividend(trade, div): #2nd check of enter_dividend
                sel = ael.Settlement.select('dividend_seqnbr=%d' % div.seqnbr)
                pos = get_position(secnom, div.pay_day)
                for dividend_setl in sel:
                    if acq_comparison(trade, dividend_setl, 'Dividend', div, None, tr_c):
                        update_coupon_value(dividend_setl, pos, 'Dividend', ipa)
                        update = 1
                if not update and (pos > 0 or ipa):
                    create_dividend(secnom, div, pos, instr.insaddr)
                                      
def coupon_ok(instr):
    return (instr.instype in FSettlementGeneral.coupon_types or\
        instr.instype in FSettlementGeneral.fixed_amount_pos)
    
def update_position_cover(settle, tr_c=None, leg_c=None, cf_c=None):
    '''settle is Security Nominal and can be stt_c '''
    if settle.sec_insaddr:
        if coupon_ok(settle.sec_insaddr):
            update_position(settle, 'Bond', tr_c, leg_c, cf_c)
        elif settle.sec_insaddr.instype == 'Stock':
            update_position(settle, 'Stock', tr_c, leg_c, cf_c)

def check_security(sel):
    ''' secnom may be netted'''
    ok = 0
    for s in sel:
        if s.type=='Security Nominal' and s.status=='Closed':
            ok = 1
            break
    return ok
    
def enter_coupon(cf, tr, cf_c=None):
    '''tr can be ent_c.'''
    enterCoupon = 0
    pr = "enter_coupon: 0"
    cf_c = FSettlementGeneralRT.set_c(cf_c, cf, 'CashFlow')
    if tr:
        sel = ael.Settlement.select('trdnbr=%d' % tr.trdnbr)
        if check_security(sel):
            enterCoupon = 1
        else:
            pr = "enter_coupon: 0, No Closed Security Nominal for tr (File)"
    else:
        if cf_c and cf_c.legnbr and cf_c.legnbr.insaddr:
            insaddr = cf_c.legnbr.insaddr.insaddr
            sel = ael.Settlement.select('sec_insaddr=%d' % insaddr)
            if check_security(sel):
                enterCoupon=1
            else:
                pr = "enter_coupon: 0, No Closed Security Nominal for sec instr (File)"
    if enterCoupon and tr and not FSettlementGeneral.enter_cashflow(tr, cf, cf_c):
        enterCoupon = 0
    if not enterCoupon:
        log(2, pr)
    return enterCoupon

def get_sec_trade(trdnbr, ins_c=None):
    '''No need for tr_c. '''
    sec = None
    if trdnbr:
        trade = ael.Trade[trdnbr]
        ins_c = FSettlementGeneralRT.set_c(ins_c, trade.insaddr, 'Instrument')
        sel = ael.Settlement.select('trdnbr=%d' % trdnbr)
        for s in sel:
            if s.type=='Security Nominal':
                if ins_c.instype in FSettlementGeneral.und_ins_security:
                        if s.value_day < ins_c.exp_day:
                            sec = s
                            break
                else:
                    sec = s
                    break
    return sec

def get_security(cf, div, prfnbr, settle = None, tr_for_sec_nom = None):
    '''cf_c and div_c ok '''    
    ret = None
    ins_c = None
    if cf and cf.legnbr and cf.legnbr.insaddr:
        ins_c = cf.legnbr.insaddr
        insaddr = ins_c.insaddr
    elif div and div.insaddr:
        ins_c = div.insaddr
        insaddr = ins_c.insaddr
    else:
        pr = "get_security: security instrument for cf nor div could be found (Error)"
        log(1, pr)
        return ret
        
    sel = ael.Settlement.select('sec_insaddr=%d' % insaddr)
    for s in sel:
        if check_security([s]) and port_comparison(s, prfnbr):
            if tr_for_sec_nom:
                if tr_for_sec_nom.trdnbr == s.trdnbr.trdnbr:
                    ret = s
                    break
            elif settle:
                    if settle.acquirer_accname == s.acquirer_accname and \
                    settle.acquirer_ptyid == s.acquirer_ptyid:
                        ret = s
                        break
            else:
                ret = s
                break

    if not ret:            
        pr = "get_security: no matching security nominal will be returned for instrument %s" % (ins_c.insid)
        log(1, pr)

    return ret


def noZoneinfoMsg():
    'Message that is presented if zoneinfo.py can not be loaded'
    
    str = '!!! Error: Python Module zoneinfo.py is not available,\
    \n cut off time calculations will not work corectly!!! \
    \n !!! On Solaris place zoneinfo.py in the Python path. \
    \n !!! On Windows place zoneinfo.py in the same\
    \n directory as the executable.\
    \n !!! After placing the file restart and check if\
    \n this message is gone.'
    return str
    

def is_status_to_be_voided(status):
    '''Returns 1 if trade status is to be voided.'''
    if status in FSettlementGeneral.from_status_to_void:
        return 1
    elif status in param.status:
        return 1
    return 0
    

def is_correction_trade(tr):
    return FSettlementGeneral3.is_correction_trade(tr)

def get_corresponding_setls(entity=None,tr=None,typ=None):
    return FSettlementGeneral3.get_corresponding_setls(entity, tr, typ)
    
def get_closed_settlement(setls):
    return FSettlementGeneral3.get_closed_settlement(setls)

def get_unclosed_settlement(setls):
    return FSettlementGeneral3.get_unclosed_settlement(setls)

def accrued_interest_setl_needed(tr):
    '''Returns true if settlement for the accrued interest should be created.'''
    ret = 0
    if is_closing(tr):
        if tr.insaddr.instype in param.valid_instrument_types_accrued_interest:
            ret = 1
    return ret            
    
def get_interest_accrued(tr, ins_c=None):
    '''tr can be tr_c '''
    trade_curr = None
    
    inst = tr.insaddr
    if not ins_c:
        ins_c = inst
    if tr.curr:
        trade_curr = tr.curr.insid
        
    ia = 0            
    q = tr.quantity
    if ins_c.instype == "EquitySwap":
        for leg in inst.legs(): # no ins_c here, todo #95
            if leg.float_rate and leg.index_ref and (leg.float_rate == leg.index_ref):
                continue
            else:                
                ia = leg.interest_accrued(None, tr.value_day, trade_curr) * q *-1
    else:
        ia = inst.interest_accrued(None, tr.value_day, trade_curr) * q * -1            

    return ia
    
def create_accrued_interest(tr, tr_c=None, ins_c=None, append_trans = 1):
    return FSettlementGeneral3.create_accrued_interest(tr, tr_c, ins_c, append_trans)

def update_accrued_interest(tr, diff_dict, ins_c=None, tr_c=None):
    return FSettlementGeneral3.update_accrued_interest(tr, diff_dict, ins_c, tr_c)

def is_interest_accrued(setl):
    ''' '''
    ret = 0
    if setl.type=='Fixed Rate' and not setl.cfwnbr:
        ret = 1
    return ret

def interest_accrued_creation(setl, status, trade, amount=None, ins_c=None, tr_c=None, append_trans = 1):
    return FSettlementGeneral3.interest_accrued_creation(setl, status, trade, amount, ins_c, tr_c, append_trans)

def get_closing_trades(tr):
    return FSettlementGeneral3.get_closing_trades(tr)
    
def recall_accrued_interest(tr, original_trade_status):
    return FSettlementGeneral3.recall_accrued_interest(tr, original_trade_status)

def get_comblinks(combs):
    return FSettlementGeneral3.get_comblinks(combs)

def sub_combinationlink(comb_dict, comb_instr, trades, diff_dict, ins_c=None):
    return FSettlementGeneral3.sub_combinationlink(comb_dict, comb_instr, trades, diff_dict, ins_c)

def get_corrected_setl(entity, tr, typ=None, setl=None):
    return FSettlementGeneral3.get_corrected_setl(entity, tr, typ, setl)

def get_dividend(div, tr, ins_c=None, pos=0, comb_info = None):
    '''For equityswaps dividend is already calculated (no matter position).
       div can be div_c '''
    ret = 0
    if not ins_c:
        ins_c = div.insaddr
    if not ins_c and tr:
        ins_c = tr.insaddr
    if ins_c.instype == 'EquitySwap':
        if tr:
            
            i = div.insaddr
            legs = i.legs()
            eq_leg = None
            factor = 1
            for leg in legs:
                if leg.float_rate and leg.index_ref and (leg.float_rate == leg.index_ref):
                    eq_leg = leg
                    break
            if eq_leg and eq_leg.payleg:
                factor = -1
            if eq_leg:
                ret = abs(div.dividend) * factor
            else:
                ret = div.dividend
            if comb_info:
                weight = get_combination_weight(comb_info.comb_ins, comb_info.comb_link, 1)
                dividend_factor = comb_info.comb_ins.dividend_factor
                nominal_amount = tr.nominal_amount(tr.value_day)
                ret = ret * nominal_amount * weight * dividend_factor     
            else:
                ret = ret * tr.quantity
    elif ins_c.und_insaddr:
        if ins_c.und_insaddr.instype == 'Stock':
            if not pos:
                pr = "Dividend position is 0 (ins=%s) Error?" % (div.insaddr.insid)
                log(5, pr)
            ret = div.dividend * pos * ins_c.und_insaddr.contr_size
    else:
        if not pos:
            pr = "Dividend position is 0 (ins=%s) Error?" % (div.insaddr.insid)
            log(5, pr)
        ret = div.dividend * pos * ins_c.contr_size
    return ret

def get_fee(tr, correction_amount=0):
    amount = tr.fee
    return (amount - correction_amount)

def get_premium(tr, correction_amount=0):
    amount = tr.premium    
    return (amount - correction_amount)

def get_premium2(tr, correction_amount=0, comblink=None):
    amount = tr.quantity * tr.insaddr.contr_size
    combination_member = FSettlementGeneral.get_combination_member(comblink)
    if combination_member:        
        weight = get_instrument_combination_weight(combination_member, tr)
        amount = tr.quantity * combination_member.contr_size * weight
    return (amount - correction_amount)        

def get_end_cash(tr, correction_amount=0):
    amount = tr.quantity * tr.insaddr.ref_value  #weight
    return (amount - correction_amount)        
 
def get_cashflow(tr, cf, correction_amount=0):    
    '''cf must not be cf_c, members must be deployed via amb '''
    amount = tr.quantity * cf.projected_cf()
    if tr.insaddr.instype in FSettlementGeneral.ins_combination:
        amount = amount * get_instrument_combination_weight(cf.legnbr.insaddr, tr)
    return (amount - correction_amount)

def get_payment(tr, payment, correction_amount=0):    
    amount = payment.amount
    return (amount - correction_amount)

def is_float_coupon(cf, cf_c=None, leg_c=None):
    cf_c = FSettlementGeneralRT.set_c(cf_c, cf, 'CashFlow')
    leg = cf.legnbr
    if leg_c:
        leg = leg_c
    if leg:
        return (leg.insaddr.instype=='FRN' and cf_c.type=='Float Rate')
    else:
        return 0

def get_combination_weight(comb_instr, comblink, use_index_factor=0):
    '''Returns weight of the combination member. If index_factor is sent 
    in weight is also divided with the index_factor of the combination member.
    '''
    if comblink:        
        if use_index_factor:
            if comb_instr.index_factor:
                return comblink.weight / comb_instr.index_factor
            else:
                pr = "Combination %s, index factor is 0, weight 0 will be returned. (File)" % (comb_instr.insid)
                log(1, pr)
                return 0                
        else:
            return comblink.weight
    pr = "Combination %s does not have deployed member. Combination weight 0 will be returned. (Error)" % (comb_instr.insid)
    log(4, pr)
    return 0
    

def set_combination_links_list_recursive(combination, comb_links_list):
    """
    see get_all_combination_links_recursive
    """
    for comb_link in combination.combination_links():
        if comb_link.member_insaddr.instype not in FSettlementGeneral.ins_combination:
            comb_links_list.append(comb_link)
        else:
            set_combination_links_list_recursive(comb_link.member_insaddr, comb_links_list)

def get_all_combination_links_recursive(combination):
    """
    Finds all combination links in combination tree.
    """
    comb_links_list = []
    set_combination_links_list_recursive(combination, comb_links_list)
    return comb_links_list

def set_security_instruments_dictionary(comb_link, sec_dictionary):
    """
    see get_security_instruments_from_combination
    """    
    if comb_link.member_insaddr.instype not in FSettlementGeneral.ins_combination:
        if (comb_link.member_insaddr.instype in FSettlementGeneral.ins_security or \
           comb_link.member_insaddr.instype in FSettlementGeneral.und_ins_security or \
           comb_link.member_insaddr.instype == 'Curr') and \
           not sec_dictionary.has_key(comb_link.member_insaddr.insid):
            sec_dictionary[comb_link.member_insaddr.insid] = comb_link
    else:
        for cbl in comb_link.member_insaddr.combination_links():
            set_security_instruments_dictionary(cbl, sec_dictionary)

def get_security_instruments_from_combination(combination, comb_link = None):
    """
    Finds all instruments generating security nominal, end security and premium 2 
    in combination tree
    """
    sec_dictionary = {}
    if comb_link == None:
        for cbl in combination.combination_links():
            set_security_instruments_dictionary(cbl, sec_dictionary)
    else:
        set_security_instruments_dictionary(comb_link, sec_dictionary)
    return sec_dictionary

def set_accumulated_cf_combination_weight(cf_ins, comb_ins, weight, acc_weight):
    """
    Weight is multiplied depth-wise and added breadth-wise.
    """
    for comb_link in comb_ins.combination_links():
        if comb_link.member_insaddr.instype not in FSettlementGeneral.ins_combination:
            if cf_ins.insaddr == comb_link.member_insaddr.insaddr:
                acc_weight[0] = acc_weight[0] + (weight * get_combination_weight(comb_ins, comb_link, 1))
        else:
            set_accumulated_cf_combination_weight(cf_ins, comb_link.member_insaddr, weight * get_combination_weight(comb_ins, comb_link, 1), acc_weight)

def get_instrument_combination_weight(ins, tr):
    """
    Gets the weight of an instrument ins for combination trade tr
    Weight is recursively calculated in function set_accumulated_cf_combination_weight
    """
    comb_ins = tr.insaddr
    weight = 1.0
    acc_weight = [0.0]
    set_accumulated_cf_combination_weight(ins, comb_ins, weight, acc_weight)
    return acc_weight[0]
    
def create_combination_securities(tr, tr_c = None, ins_c = None):
    tr_c = FSettlementGeneralRT.set_c(tr_c, tr, 'Trade')
    for cbl in get_security_instruments_from_combination(tr.insaddr).values():
        if cbl.member_insaddr.instype in FSettlementGeneral.ins_security:
            FSettlementGeneralRT.create_premium_t(tr, 'Security Nominal', 'New', 1, cbl, tr_c, ins_c)
        elif cbl.member_insaddr.instype in FSettlementGeneral.und_ins_security:
            FSettlementGeneralRT.create_premium_t(tr, 'End Security', 'New', 1, cbl, tr_c)
        elif cbl.member_insaddr.instype == 'Curr':
            FSettlementGeneralRT.create_premium_t(tr, 'Premium 2', 'New', 1, cbl, tr_c)

def update_combination_securities(tr, diff_dict, tr_c = None, comb_link = None, comb_link_removed = False):
    """
    tr is a combination trade. Update settlements of type security nominal,
    end security and premium 2.
    """
    tr_c = FSettlementGeneralRT.set_c(tr_c, tr, 'Trade')
    for cbl in get_security_instruments_from_combination(tr.insaddr, comb_link).values():
        if cbl.member_insaddr.instype in FSettlementGeneral.ins_security:
            FSettlementGeneralRT.update_premium(tr, diff_dict, 'Security Nominal', cbl, tr_c, None, comb_link_removed)
        elif cbl.member_insaddr.instype in FSettlementGeneral.und_ins_security:
            FSettlementGeneralRT.update_premium(tr, diff_dict, 'End Security', cbl, tr_c, None, comb_link_removed)
        elif cbl.member_insaddr.instype == 'Curr':
            FSettlementGeneralRT.update_premium(tr, diff_dict, 'Premium 2', cbl, tr_c, None, comb_link_removed)


def create_combination_member(tr, comblink, tr_c=None, ins_c=None, modified_comblink = False):
    '''Called when combination trade is inserted or combination link added.
    If modified_comblink is True create_combination_member was called from
    sub_combinationlink
    '''
    tr_c = FSettlementGeneralRT.set_c(tr_c, tr, 'Trade')
    combination_member = FSettlementGeneral.get_combination_member(comblink)
    if combination_member:
            
        if combination_member.instype == 'EquitySwap' and modified_comblink:
            FSettlementGeneralRT.create_eq_swap_dividend(tr_c)

def is_cashflow_part_of_combination(cashflow, comb_link):
    if comb_link.member_insaddr.instype not in FSettlementGeneral.ins_combination:
        return cashflow.legnbr.insaddr.insaddr == comb_link.member_insaddr.insaddr
    else:
        for cbl in comb_link.member_insaddr.combination_links():
            if is_cashflow_part_of_combination(cashflow, cbl):
                return True
        return False
                

def update_combination_cf(tr, comblink, diff_dict={}, tr_c=None):
    ''' '''
    tr_c = FSettlementGeneralRT.set_c(tr_c, tr, 'Trade') #no ins_c here, trade is trigger
    combination_member = FSettlementGeneral.get_combination_member(comblink)
    for cf in FSettlementGeneralRT.cfs_from_tr(tr, comb_member = combination_member):
        if is_cashflow_part_of_combination(cf, comblink):
            FSettlementGeneralRT.update_cf(cf, diff_dict, tr, None, tr_c, None, None, cf)
    FSettlementGeneralRT.update_combination_eq_swap_dividends(tr_c, diff_dict)

def update_combination_trade(tr, diff_dict={}, include_cf=0, tr_c=None):
    '''include_cf = 1 is used from EOD
       include_cf = 0 is used from AMB (cfs are handled anyway)
       See also sub_combinationlink with event +
    '''
    tr_c = FSettlementGeneralRT.set_c(tr_c, tr, 'Trade')
    if tr.insaddr.instype in FSettlementGeneral.ins_combination:
        for comblink in tr.insaddr.combination_links():
            if include_cf:
                update_combination_cf(tr, comblink, diff_dict, tr_c)
        update_combination_securities(tr, diff_dict, tr_c)

def cf_not_comb_member(tr, cf):
    '''Returns 1 if cf belongs to combinations cash flows. '''
    ret = 0
    if tr.insaddr.instype in FSettlementGeneral.ins_combination:
        if cf not in FSettlementGeneralRT.cfs_from_tr(tr):
            pr = "CF %d does not belong to combination %s." % (cf.cfwnbr, tr.insaddr.insid)
            log(1, pr)
            ret = 1
    return ret

def get_settlements2(tr, combination_member=None, typ='',include=1, comb_link_removed = False):
    '''This function can return following settlement selections (I to VI).
    I   based on tradenumber including alla combination members
    II  based on tradenumber but excluding all combination members (Default)
    III based on combination member (all types)
    IV  based on tradenumber type
    V   based on combination member and its type
    VI   based on combination member type but not combination member itself
    combination_member is instrument that is part of combination. #   
    If combination_member is None then type of the settlement is checked.
    typ = '' means All otherwise the type that is stated. 
    include matters only if (combination_member and (typ = '' or typ=something))        
    See also FSettlementGeneral.create_selection that is to be used after this function.
    See also FSettlementGeneralRT.get_settlements that is overriden by this function.'''
    ret = []
    is_combination_trade=0        
    
    tr = FSettlementGeneral3.get_trade_entity(tr)
    if tr:        
        instype = tr.insaddr.instype
        if instype and instype in FSettlementGeneral.ins_combination:
            is_combination_trade = 1
    else:
        pr = "get_settlements: wrong input, it should trade or trdnbr (File)"
        log(2, pr)
    sel = ael.Settlement.select('trdnbr=%d' % tr.trdnbr)    
    comb_members = []
    if combination_member or is_combination_trade:
        for c in get_all_combination_links_recursive(tr.insaddr): #ent_c ok
            if c.member_insaddr not in comb_members:
                comb_members.append(c.member_insaddr)
            
    all_trade_setls = [] 
    all_comb_setls = []
    all_tr_type_setls = []
    comb_type_setl = []
    all_comb_type_setls = []
    
    if combination_member and typ == '' and include:# I
        return sel
    if not combination_member and typ == '':# II
        return sel
        
    for s in sel:
        if s.sec_insaddr not in comb_members:
            all_trade_setls.append(s) 
    
    if combination_member and typ == '' and not include: # III    
        for s in sel:
            if s not in all_trade_setls and s.sec_insaddr in comb_members:
                all_comb_setls.append(s)
        return all_comb_setls
    if not combination_member and typ != '': # IV
        for s in all_trade_setls:
            if s.type == typ:
                all_tr_type_setls.append(s)
        return all_tr_type_setls
    if combination_member and typ != '': 
        if not include:# V
            for s in sel:
                if s not in all_trade_setls and s.sec_insaddr in comb_members and s.type == typ:
                    comb_type_setl.append(s)
            return comb_type_setl                    
        else:
            for s in sel: # VI
                if (s not in all_trade_setls or comb_link_removed) and s.sec_insaddr == combination_member and s.type == typ:
                    all_comb_setls.append(s)
            return all_comb_setls

    pr = 'function get_settlements is called wrongly, all settlements will be returned'
    log(2, pr)
    return sel

def get_trades(instrument):
    return FSettlementGeneral3.get_trades(instrument)

def void_trade_recall_setls2(tr, oldTrStatus, combination_member=None):
    '''If the trade status has changed from FSettlementGeneral.from_status_to_void
    to FSettlementGeneral.new_status_to_void then all settlement rows will be 
    recalled. Termination fee is kept when the trade is Terminated.
    Stand Alone Payments can be connected to a trade. Once the trade is voided 
    corresponding Stand Alone Payments are deleted.
    Deleting combination member corresponds to voiding a trade'''    
    
    setls = []
    setlObj = None # settlement object deployed to update row
    setlObjNew = None    
    leave_in_place = []

    if tr.status == 'Terminated':
        leave_in_place.append('Termination Fee')

    if tr:
        try:
            setls = FSettlementGeneralRT.get_settlements(tr, combination_member, '', 1) ### I or II                
        except:
            setls = []            
    else:
        log(0, 'void_trade_recall_setls: the input trade is None')
    
    for setl in setls:
        # no need for stt_c bellow
        if FSettlementGeneral.source_data(setl):
            if param.keep_old_settlements_when_void and \
               setl.status in param.keep_status and setl.status in \
               FSettlementGeneral.delete_status and setl.value_day <= ael.date_today():
                continue
            if FSettlementGeneral3.is_do_not_delete_diary_ref(setl):
                continue
            # Termination fee and stand alone payment must not be voided!
            if setl.type not in leave_in_place:
                if oldTrStatus:
                    pr = 'Trade %d changed status from %s to %s, \
                    Recalling Settlements' % (tr.trdnbr, oldTrStatus, tr.status)
                    log(1, pr)
                elif combination_member:
                    
                    skip_sec_insaddr = 0
                    if setl.dividend_seqnbr and \
                    setl.dividend_seqnbr.insaddr == combination_member:
                        skip_sec_insaddr = 1
                    
                    if not skip_sec_insaddr and combination_member != setl.sec_insaddr:
                        continue
                    pr = 'Combination member (%s) deleted, \
                    Recalling Settlement %d' % (combination_member.insid, setl.seqnbr)
                    log(1, pr)    
                      
                setlObjList = FSettlementGeneral.create_from_settle([setl])
                if len(setlObjList):
                    setlObj = setlObjList[0]
                    setlObjNew = setlObj
                if setlObj and setlObjNew:
                    setlObjNew['status'] = 'Recalled'
                    setlObjNew['text'] = oldTrStatus
                    

                    FSettlementGeneralRT.update_row(setlObj, setlObjNew)
            # We have to update the coupons and redemption amount if a trade
            # gets voided that have a Closed Security Nominal
            if check_security([setl]):            
                update_position_cover(setl)   
            else:
                str = "Settlement %d is Not Voided, it is " % setl.seqnbr
                str = str + setl.type
                log(1, str)

    if tr:                
        recall_accrued_interest(tr, oldTrStatus)
                
    return


def get_curr_premium2(tr, combination_member=None):
    ''' '''
    if not combination_member:
        return tr.insaddr.curr.insaddr
    else:
        return combination_member.curr.insaddr    


def is_closing(tr):
    '''Returns true if the trade is the closing (not correction) some other trade trade.
       See also get_closing_trades(tr)'''
    if tr.contract_trdnbr != tr.trdnbr and tr.type == 'Closing':
        return 1
    else:
        return 0


def is_closed(tr):
    '''Returns 1 if the trade is closed by some other trade. 
    See also FSettlementGenera2.get_closing_trades(tr).'''
    ret = 0
    selection = ael.Trade.select('contract_trdnbr="%d"' % (tr.trdnbr))
    if len(selection) > 1:
        ret = 1
    return ret


def get_closed_trades(closing):
    '''Get recursivly trades closed by closing trade. '''
    ret = []
    closed = get_closed_trade(closing)
    while closed:
        if closed not in ret:
            ret.append(closed)
        closed = get_closed_trade(closed)

    return ret

    
def get_closed_trade(closing):
    '''Returns the trade that is closed by the closing trade. '''
    if is_closing(closing):
        return ael.Trade[closing.contract_trdnbr]
    else:
        return None

    
def touch_closed_trade(closing):
    return FSettlementGeneral3.touch_closed_trade(closing)


def log(level, s):
    return FSettlementGeneral.log(level, s)

    
def is_partially_closing_some_trade(tr1, tr2):
    '''Returns true if different trades happen to partially close the same trade.'''    
    for ct1 in get_closed_trades(tr1):  
        for ct2 in get_closed_trades(tr2):
            if ct1 == ct2:
                return 1
    return 0            

def my_getattr(ent, attr='', ent_c = None):    
    return FSettlementGeneral3.my_getattr(ent, attr, ent_c)
    

def get_resets_from_leg(i):
    """i is an instrument. Returns a list with all resets associated with a leg
    with float_rate.instype = Stock """
    
    resets = []
    legs = i.legs()
    for leg in legs:
        if leg.float_rate and leg.float_rate.instype == 'Stock': 
            reset_list = leg.resets()
            for reset in reset_list:
                resets.append(reset)
    return resets

def get_earliest_reset_day(reset_list):
    """reset_list is a list containing resets. The function returns the 
    earliest reset day among all the resets."""
    
    earliest = None
    for reset in reset_list:
        if not earliest:
            earliest = reset
            continue
        if reset.day < earliest.day:
            earliest = reset

    if not earliest:
        return None
    else:
        return earliest.day
        
def get_latest_reset_day(reset_list):
    """reset_list is a list containing resets. The function returns the 
    latest reset day among all the resets."""
    
    latest = None
    for reset in reset_list:
        if not latest:
            latest = reset
            continue
        if reset.day > latest.day:
            latest = reset

    if not latest:
        return None
    else:
        return latest.day

def is_eligible_for_dividend_creation(t, d):
    """
    t is a trade entity, d is a dividend entity. This function is called for dividend related trades,
    to decide whether to create a dividend settlement record or not.
    """
    ok = 0
    
    if d.insaddr.instype == 'EquitySwap':
        
        if param.consider_resets_for_eq_swap_dividends:
            reset_list = get_resets_from_leg(d.insaddr)
            earliest_reset_day = get_earliest_reset_day(reset_list)
            latest_reset_day = get_latest_reset_day(reset_list)

            if earliest_reset_day and latest_reset_day:
                ok = earliest_reset_day < d.ex_div_day <= latest_reset_day
            else:
                log(3, 'is_eligible_for_dividend_creation: Could not retrieve reset days for instrument %s.' % t.insaddr.insid)
        else:
            ok = t.value_day <= d.ex_div_day
    else:
        ok = t.value_day <= d.ex_div_day
    return ok
    
def do_not_update_recalled_settlement(settlement):
    ret = 0
    if (settlement.status == 'Recalled' and not param.update_recalled):
        ret = 1
        log(2, 'Recalled settlement %d will not be updated!' % settlement.seqnbr)
        log(2, 'Cause: variable update_recalled = 0 in FSettlementVariables. ')
    return ret
    


