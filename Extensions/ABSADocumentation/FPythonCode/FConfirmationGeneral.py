""" Compiled: 2010-08-19 18:56:12 """

"""----------------------------------------------------------------------------
MODULE
    FConfirmationGeneral - Module including all functions for the
                         Confirmation population and update processes.

    (c) Copyright 2005 by Front Capital Systems AB. All rights reserved.

DESCRIPTION    

----------------------------------------------------------------------------"""
import ael
import time
import inspect
import types
import sys
import FConfirmationParams
import ArenaFunctionBridge as AFB
import FOperationsUtils
import FOperationsSwiftBic
import FConfirmationUtilities as utils

try:
    import FConfirmationClientSTP
    client_stp_imported = 1
except ImportError:
    client_stp_imported = 0

invalid_address = ['', ' ', '@', '.', 0, None]
param = FConfirmationParams.get_default_params()
OS = sys.platform
post_released_statuses = ['Released', 'Acknowledged', 'Not Acknowledged',
                          'Matched', 'Partial Match', 'Pending Matching',
                          'Void', 'Matching Failed']
primary_key_dict = {}

class CommitException(FOperationsUtils.WrapperException):
    def __init__(self, text, innerException = None):
        FOperationsUtils.WrapperException.__init__(self, text, innerException)
    
    def is_no_access_commit_failure(self):
        is_no_access = False
        if (str(self.GetInnerException()).find("No access") != -1):
            is_no_access = True
        return is_no_access
        

class UpdateCollisionException(CommitException):
    def __init__(self, text, innerException = None):
        CommitException.__init__(self, text, innerException)

def handle_amendment_confirmation(new_amendment_confirmation):
    ref_conf = new_amendment_confirmation.confirmation_seqnbr
    if ref_conf:
        transaction = 0
        copy_protection_from_confirmation(new_amendment_confirmation, new_amendment_confirmation.confirmation_seqnbr.seqnbr)
        if ref_conf.diary_seqnbr:
            note = ref_conf.diary_seqnbr.get_text()
            ael.begin_transaction()
            transaction = 1
            t = ael.TextObject.new()
            t.type = 'Confirmation diary'
            t.name = str(time.time())
            t.set_text(note)
            t.commit()
            new_amendment_confirmation.diary_seqnbr = t

        if ref_conf.status != 'Void':
            if not transaction:
                ael.begin_transaction()
                transaction = 1
            ref_conf_clone = ref_conf.clone()
            old_status = ref_conf.status
            ref_conf_clone.status = 'Void'
            commit_confirmation(ref_conf_clone, old_status)

        for a in ref_conf.additional_infos():
            if not transaction:
                ael.begin_transaction()
                transaction = 1
            addinfo_new =  ael.AdditionalInfo.new(new_amendment_confirmation)
            addinfo_new.value = a.value
            addinfo_new.addinf_specnbr = a.addinf_specnbr
        if transaction:
            commit_transaction()


def create_new_confirmation(trade,
                            reset,
                            event_chlnbr,
                            conf_seqnbr,
                            chaser_seqnbr,
                            void_original_conf,
                            text = "",
                            is_client_event = 0,
                            cf = None,
                            do_commit = True,
                            counterparty = None):
    ''' Creates and commits a new confirmation record with characteristics from
    the given input parameters. '''
    log_trace()
        
    c = ael.Confirmation.new()
    c.status = 'New'
    c.trdnbr = trade
    c.reset_resnbr = reset
    c.cfwnbr = cf
    c.event_chlnbr = event_chlnbr
    c.confirmation_seqnbr = conf_seqnbr
    c.chasing_seqnbr = chaser_seqnbr
    
    if c.text and text:
        c.text = "%s %s" % (c.text, text)
    elif text:
        c.text = text
    instruction = None
    if counterparty: #We are dealing with a counterparty cancellation
        instruction = c.instruction_from_party(counterparty)
        c.conf_instruction_seqnbr = instruction
    else:
        instruction = c.instruction()
      
            
    if instruction:
        if instruction.transport == "None":
            pr = "Transport for the matching confirmation instruction is not set, no confirmation will be generated."
            log(3, pr)
            return 
    if is_client_event and not instruction:
        pr = "Conf for client event will not be created no conf instruction."
        log(3, pr)
        return
    
    transaction = 0
    if conf_seqnbr and do_commit:
        copy_protection_from_confirmation(c, conf_seqnbr)

        ref_conf = ael.Confirmation[conf_seqnbr]
        if ref_conf:
            if ref_conf.diary_seqnbr:
                note = ref_conf.diary_seqnbr.get_text()
                ael.begin_transaction()
                transaction = 1
                t = ael.TextObject.new()
                t.type = 'Confirmation diary'
                t.name = str(time.time())
                t.set_text(note)
                t.commit()
                c.diary_seqnbr = t
                pr = 'copying diary notes from confirmation %d' % conf_seqnbr
                log(4, pr)

            if void_original_conf and ref_conf.status != 'Void':
                if not transaction:
                    ael.begin_transaction()
                    transaction = 1
                ref_conf_clone = ref_conf.clone()
                old_status = ref_conf.status
                ref_conf_clone.status = 'Void'
                commit_confirmation(ref_conf_clone, old_status)
            
            for a in ref_conf.additional_infos():
                if not transaction:
                    ael.begin_transaction()
                    transaction = 1
                addinfo_new =  ael.AdditionalInfo.new(c)
                addinfo_new.value = a.value
                addinfo_new.addinf_specnbr = a.addinf_specnbr

    elif chaser_seqnbr:
        copy_protection_from_confirmation(c, chaser_seqnbr)
    else:
        copy_protection_from_trade(c, trade)
    if do_commit:
        commit_confirmation(c)
        if transaction:
            commit_transaction()
    else:
        ael.abort_transaction()
        return c

def add_new_confirmation(tr, old_conf_exist, reset=None):
    ''' Adds a new confirmation record with event either New Trade, Amendment
    or Rate Fixing. '''
    log_trace()
        
    event_chlnbr = 0
    if tr:
        if reset:
            event_chlnbr = param.RATE_FIXING
        elif (old_conf_exist and trade_is_correction(tr) and
              not corr_trade_has_new_cp(tr)):
            event_chlnbr = param.AMENDMENT
        elif tr.contract_trdnbr and tr.contract_trdnbr != tr.trdnbr:
            org_trade = ael.Trade[tr.contract_trdnbr]
            if org_trade:
                is_full = abs(position(tr)) < 10e-6
                if tr.type == 'Closing':
                    if is_full:
                        event_chlnbr = param.CLOSE
                    else:
                        event_chlnbr = param.PARTIAL_CLOSE
                elif tr.type == 'Exercise':
                    if is_full:
                        event_chlnbr = param.EXERCISE
                    else:
                        event_chlnbr = param.PARTIAL_EXERCISE
        if not event_chlnbr:
            event_chlnbr = param.NEW_TRADE

        event_str = get_event_printable(event_chlnbr)
        pr = 'create %s confirmation' % event_str
        log(1, pr)
        
        create_new_confirmation(tr, reset, event_chlnbr, None, None, 0)

    return event_chlnbr


def add_new_ref_confirmation(conf, trade, new_event_chlnbr,
                             void_original_conf, do_commit = True,
                             counterparty = None):
    ''' Create a new confirmation record representing new_event event. '''
    log_trace()
    
    if conf:
        event_str = get_event_printable(new_event_chlnbr)
        pr = 'create %s of confirmation %d'  % (event_str, conf.seqnbr)
        log(1, pr)      

        if trade:
            use_trade = trade
        else:
            use_trade = conf.trdnbr
        reference_confirmation = create_new_confirmation(use_trade,
                                                         conf.reset_resnbr,
                                                         new_event_chlnbr,
                                                         conf.seqnbr,
                                                         None,
                                                         void_original_conf,
                                                         "",
                                                         False,
                                                         conf.cfwnbr,
                                                         do_commit,
                                                         counterparty)
        return reference_confirmation
    else:
        log(0, 'add_new_ref_confirmation: no confirmation')
    

def add_confirmation_copy(conf, trade):
    ''' Copy conf to a new confirmation record.  Set confirmation_seqnbr to
    point to conf.  Set trdnbr to point to trade.  In case the status is Void
    the status is not copied but set to Acknowledged. '''
    log_trace()

    transaction = 0
    conf_copy = conf.new()
    conf_copy.confirmation_seqnbr = conf
    conf_copy.trdnbr = trade
    if conf.status == 'Void':
        conf_copy.status = 'Acknowledged' #stp?
    else:
        transaction = 1
        ael.begin_transaction()
        old_status = conf.status
        c = conf.clone()
        c.status = 'Void'
        commit_confirmation(c, old_status)

    commit_confirmation(conf_copy)

    if transaction:
        commit_transaction()


def amendment_creation(conf, trade, do_commit = True):
    ''' Create amendment confirmation record. '''
    log_trace()

    return add_new_ref_confirmation(conf, trade, param.AMENDMENT, 1, do_commit)


def cancellation_creation(conf, counterparty = None):
    ''' Create cancellation confirmation record. '''
    log_trace()
    
    
    add_new_ref_confirmation(conf, None, param.CANCELLATION, 1, True, counterparty)


def correction_update_creation(conf, trade):
    ''' Create new trade confirmation record that references conf.  Also void
    conf. '''
    log_trace()
    
    add_new_ref_confirmation(conf, trade, param.NEW_TRADE, 1)

    
def check_bic(conf, contact, contact_is_cp):
    ''' Check that the contact has a valid bic code. If contact_is_cp equals 1
    check the counterparty contact, otherwise check the acquirer contact. '''
    log_trace()
    
    ret = 1
    if contact:
        bic = get_bic(contact)
        if not bic or not FOperationsSwiftBic.check_bic_code(contact.ptynbr, bic, 2):
            ret = 0
        else:
            if contact_is_cp:
                address = conf.counterparty_address
            else:
                address = conf.acquirer_address
            if not FOperationsSwiftBic.check_bic_code(contact.ptynbr, address, 2):
                ret = 0
    return ret


def validate_confirmation(conf):
    ''' Check that the confirmation record input is valid.  If ok return 0, if
    not, return status explanation. Not possible to check for Insufficient
    Message Data here since this is meant to be a status explanation set by
    Adaptiv. '''
    log_trace()
    
    missing_data = 0
    missing_address = 0
    missing_conf_instruction = 0
     
    if not conf:
        log(0, "validate_confirmation: no confirmation")
        return add_status_explanation(0, 'Missing data')

    id_str = "confirmation.seqnbr: %d" % (conf.seqnbr)
       
    if not conf.trdnbr:
        pr = "%s, no trade" % id_str
        log(0, pr)
        missing_data = 1
        
    if not conf.conf_instruction_seqnbr:
        pr = "%s, no confinstruction" % id_str
        log(0, pr)
        missing_conf_instruction = 1

    if not conf.conf_template_chlnbr:
        pr = "%s, no template" % id_str
        log(0, pr)
        missing_data = 1

    if not conf.transport or conf.transport in invalid_address:
        pr = ": %s, no transport" % id_str
        log(0, pr)        
        missing_data = 1
        
    if not conf.acquirer_contact:
        pr = "%s, no acquirer contact" % id_str
        log(4, pr)
    
    if not conf.counterparty_contact:
        pr = "%s, no counterparty contact" % id_str
        log(0, pr)
        missing_data = 1
    
    if (conf.transport != 'File' and conf.transport != 'Other' and
        (not conf.acquirer_address or
         conf.acquirer_address in invalid_address)):
        pr = "%s, no acquirer address" % id_str
        log(4, pr)
    
    if (conf.transport != 'File' and conf.transport != 'Other' and
        (not conf.counterparty_address or
         conf.counterparty_address in invalid_address)):
        pr = "%s, no counterparty address" % id_str
        log(0, pr)
        missing_address = 1
    
    if is_swift_mode(conf, conf.conf_instruction_seqnbr):
        aq_contact = conf.contact('Intern Dept')
        if aq_contact and not check_bic(conf, aq_contact, 0):
            pr = "%s, incorrect acquirer bic" % id_str
            log(0, pr)
            missing_address = 1
        cp_contact = conf.contact()
        if cp_contact and not check_bic(conf, cp_contact, 1):
            pr = "%s, incorrect counterparty bic" % id_str
            log(0, pr)
            missing_address = 1
                
    expl = 0
    if missing_data:
        expl = add_status_explanation(expl, 'Missing data')
    if missing_address:
        expl = add_status_explanation(expl, 'Missing Address')
    if missing_conf_instruction:
        expl = add_status_explanation(expl, 'Missing Confirmation Instruction')

    return expl
    

def get_counterparty_for_scoring(confirmation):
    ret_cp = confirmation.trdnbr.counterparty_ptynbr
    event_seqnbr = confirmation.event_chlnbr.seqnbr
    if event_seqnbr == param.CANCELLATION:
        ref_conf = confirmation.confirmation_seqnbr
        if ref_conf:
            confirmation_instr = ref_conf.conf_instruction_seqnbr
            if confirmation_instr:
                cp = confirmation_instr.counterparty_ptynbr
                if cp != ret_cp:
                    ret_cp = cp
    return ret_cp



def update_confirmation(conf, do_commit = True):
    ''' Main function for confirmation updates. Populate all fields all the
    time otherwise old info might remain'''
    log_trace()
    
    if not conf:
        log(0, 'update_confirmation: no confirmation')
        return

    trade = conf.trdnbr
    
    old_status = conf.status
    cp_for_scoring = get_counterparty_for_scoring(conf)
    confinst_cp = conf.instruction_from_party(cp_for_scoring)
    if not preserve_conf(conf):
        c = conf.clone()
    else:
        log(3, 'update_confirmation: confirmation could not be cloned')
        return            
    if confinst_cp:
        if confinst_cp.transport == "None":
            log(3, 'Transport for the matching confirmation instruction is not set, confirmation will be canceled')
            cancel_confirmation(conf)
            return

    # Setting Confirmation attributes
    if confinst_cp:
        c.conf_instruction_seqnbr = confinst_cp.seqnbr
        # if we have name tag we could compare confinst
        if confinst_cp.conf_template_chlnbr:
            c.conf_template_chlnbr = confinst_cp.conf_template_chlnbr.seqnbr
            
        c.stp = confinst_cp.stp
        # First time conf_instruction is used copy sign_off data
        # Next time compare, if conf_instruction changed override
        # possible signoffs
        if c.sign_off1_grpnbr != confinst_cp.sign_off1_grpnbr:
            if confinst_cp.sign_off1_grpnbr:
                c.sign_off1_grpnbr = confinst_cp.sign_off1_grpnbr.grpnbr
            else:
                c.sign_off1_grpnbr = 0
            c.sign_off1_status = 'None'
            c.sign_off1_usrnbr = 0
            
        if c.sign_off2_grpnbr != confinst_cp.sign_off2_grpnbr:
            if confinst_cp.sign_off2_grpnbr:
                c.sign_off2_grpnbr = confinst_cp.sign_off2_grpnbr.grpnbr
            else:                
                c.sign_off2_grpnbr = 0
            c.sign_off2_status = 'None'
            c.sign_off2_usrnbr = 0

        if confinst_cp.transport != c.transport:
            c.transport = confinst_cp.transport

    c.trdnbr = trade.trdnbr
    aq = trade.acquirer_ptynbr
    if aq:           
        c.acquirer_address = ''
        addr = c.address(aq.type)
        if addr and addr not in invalid_address:
            c.acquirer_address = c.address(aq.type)
        aq_contact = c.contact('Intern Dept')
        if aq_contact:            
            c.acquirer_contact = aq_contact.fullname
        else:
            c.acquirer_contact = aq.contact1

                
    cp = trade.counterparty_ptynbr
    if cp:
        pr = "cp transport = %s" % str(c.transport)
        log(0, pr)
        c.counterparty_address = ''
        addr = c.address_from_party(cp_for_scoring)
        if addr and addr not in invalid_address:
            c.counterparty_address = addr
        cp_contact = c.contact_from_party(cp_for_scoring)
        if cp_contact:
            c.counterparty_contact = cp_contact.fullname
        else:
            c.counterparty_contact = cp_for_scoring.contact1
            
    expl = validate_confirmation(c)
    if expl:
        new_status = 'Exception'
    elif c.status == 'Manual Match':
        new_status = 'New'
    else:
        if c.status == 'Pending Document Generation':
            new_status = 'New'
        else:
            if client_stp(c):
                new_status = 'Pending Document Generation'
            else:
                new_status = 'Manual Match'
    change_status(c, new_status, expl)
    if do_commit:
        commit_confirmation(c, old_status)
    else:
        return c



def client_stp(c):
    ''' Evaluate the client stp functions in FConfirmationClientSTP.  Return 0
    if any of these returns 0. '''
    log_trace()

    if client_stp_imported:
        for k, v in FConfirmationClientSTP.__dict__.items():
            if isinstance(v, types.FunctionType) and k[:6] == 'client':
                if not eval('FConfirmationClientSTP.' + k + '(c)'):
                    return 0
    return 1


def client_stp_stop_in_authorised(conf):
    ''' Evaluate the confirmation_stop_in_authorised function in
    FConfirmationClientSTP. '''
    log_trace()
    
    stop_in_authorised = -1
    if client_stp_imported:
        stop_in_authorised = \
                   FConfirmationClientSTP.confirmation_stop_in_authorised(conf)
        if stop_in_authorised >= 0:
            pr = 'FConfirmationClientSTP.confirmation_stop_in_authorised' \
                 ' returned %d' % stop_in_authorised
            log(3, pr)
    return stop_in_authorised


def preserve_conf(conf):
    ''' Check function for preserving Confirmation. '''
    log_trace()
    
    ok = 0        
    if conf.status in ['Hold', 'Void']:
        pr = 'confirmation %d in status %s should not be updated' % \
             (conf.seqnbr, conf.status)
        log(3, pr)
        ok = 1

    return ok


def conf_signed_off(conf):
    ''' Confirmation is signed off when all needed groups have approved or when
    no signoff is needed. '''
    log_trace()
    
    sign1 = 0
    sign2 = 0
    
    if not conf.sign_off1_grpnbr or conf.sign_off1_status == 'Approved':
        sign1 = 1

    if not conf.sign_off2_grpnbr or conf.sign_off2_status == 'Approved':
        sign2 = 1
    
    return sign1 and sign2    

    

def set_sign_off_status_pending_approval(conf):
    ''' Set sign off status 1 and/or 2 if needed. '''
    log_trace()
    
    set_status1 = 0
    set_status2 = 0

    if conf.sign_off1_grpnbr and conf.sign_off1_status == 'None':
        set_status1 = 1
    
    if conf.sign_off2_grpnbr and conf.sign_off2_status == 'None':
        set_status2 = 1

    if set_status1 or set_status2:
        c = conf.clone()

        if set_status1:
            c.sign_off1_status = 'Pending Approval'

        if set_status2:
            c.sign_off2_status = 'Pending Approval'
        
        commit_confirmation(c)


def get_all_customer_events():
    '''Returns a list including non core event ael entities.'''
    non_core_events = []
    all_events = ael.ChoiceList['Event'].members()
    for e in all_events:
        if e.entry not in FConfirmationParams.core_events:
            non_core_events.append(e)
    return non_core_events

    
def has_core_event(conf):
    '''Returns 1 if confirmation event is core event. 
    Note that source confirmation is checked not the parent.'''
    c = conf
    while c:                
        if not c.confirmation_seqnbr:
            conf = c
        c = c.confirmation_seqnbr
        
    if conf and conf.event_chlnbr:
        if conf.event_chlnbr.entry in FConfirmationParams.core_events:
            return 1
    return 0
def has_instrument_event(confirmation):
    return get_bottommost_confirmation(confirmation).event_chlnbr.entry in FConfirmationParams.instrument_events


def find_confirmations(tr, reset):

    ''' Return all confirmation records for the given trade. If the reset
    parameter is supplied the confirmation must match the reset via the
    reset_resnbr reference. '''
    log_trace()
    
    ret = []
    for conf in tr.confirmations():        
        if reset:
            if reset == conf.reset_resnbr:
                if not has_instrument_event(conf):
                    ret.append(conf)
        else:
            if not conf.reset_resnbr:
                if not has_instrument_event(conf):
                    ret.append(conf)

    return ret

class Filter:
    def __init__(self):
        if self.__class__ is Filter:
            raise NotImplementedError

    def isSatisfiedBy(self, obj):
        raise NotImplementedError

class PostReleaseFilter(Filter):
    def __init__(self):
        Filter.__init__(self)

    def isSatisfiedBy(self, obj):
        return not is_prereleased_confirmation(obj)        
        
class PreReleaseFilter(Filter):
    def __init__(self):
        Filter.__init__(self)

    def isSatisfiedBy(self, obj):
        return is_prereleased_confirmation(obj)

class IncludeAllFilter(Filter):
    def __init__(self):
        Filter.__init__(self)

    def isSatisfiedBy(self, obj):
        return True

def find_topmost_confirmations_including_instrument_events(trade, reset, include_voided_confirmations, includeFilter):
    log_trace()
    assert includeFilter != None
    foundConfirmations = list()
    for confirmation in trade.confirmations():
        validConfirmation = False
        if reset:
            if reset == confirmation.reset_resnbr:
                validConfirmation = True
        else:
            if not confirmation.reset_resnbr or utils.IsWeightedReset(confirmation.reset_resnbr):
                validConfirmation = True

        if validConfirmation and includeFilter.isSatisfiedBy(confirmation):
            if ((include_voided_confirmations or confirmation.status != 'Void') and confirmation.event_chlnbr.seqnbr != param.CHASER):
                if is_topmost_confirmation(confirmation):
                    foundConfirmations.append(confirmation)

    return foundConfirmations


def find_confirmation(trade, reset, void_is_ok=0):
    ''' Find a confirmation record for the given trade or reset. If void_is_ok
    is 1 also voided confirmations will be considered as result of this
    function. '''
    log_trace()

    conf = None
    confs = []
    for c in find_confirmations(trade, reset):
        if ((void_is_ok or c.status != 'Void') and
            c.event_chlnbr.seqnbr != param.CHASER):
            confs.append(c)
    
    if len(confs) == 1:
        conf = confs[0]#
    elif len(confs) > 1:
        max_seqnbr_conf = confs[0]
        for c in confs:
            if c.seqnbr > max_seqnbr_conf.seqnbr:
                max_seqnbr_conf = c

        c = max_seqnbr_conf
        linked_confs = 0
        while c:
            linked_confs += 1
            c = c.confirmation_seqnbr

        conf = max_seqnbr_conf
        
        if len(confs) > linked_confs:
            pr = 'warning, found more than one (%d) confirmations for trade ' \
                 '%d, selecting %d' % (len(confs), trade.trdnbr, conf.seqnbr)
            log(0, pr)

    return conf

def get_topmost_confirmation(confirmation):
    log_trace()
    result_set = ael.Confirmation.select('confirmation_seqnbr = %d' % confirmation.seqnbr)
    if len(result_set) == 0:
        return confirmation
    else:
        return get_topmost_confirmation(result_set[0])

def is_topmost_confirmation(confirmation):
    log_trace()
    return confirmation == get_topmost_confirmation(confirmation)

def get_bottommost_trade(trade):
    if trade.correction_trdnbr:
        while (trade.correction_trdnbr.trdnbr != trade.trdnbr):
            trade = trade.correction_trdnbr
    return trade.trdnbr

def get_bottommost_confirmation(confirmation):
    log_trace()
    
    referenced_confirmation = confirmation.confirmation_seqnbr
    if referenced_confirmation:
        return get_bottommost_confirmation(referenced_confirmation)
    else:
        return confirmation

def get_topmost_customer_event_confirmations_for_trade(trade):
    bottommost_confirmations = get_bottommost_customer_event_confirmations_for_trade(trade)
    topmost_confirmations = list()
    for bottommost_confirmation in bottommost_confirmations:
        topmost_confirmations.append(get_topmost_confirmation(bottommost_confirmation))
    return topmost_confirmations

def get_bottommost_customer_event_confirmations_for_trade(trade):
    log_trace()
    
    customer_event_confirmations = set()
    for confirmation in trade.confirmations():
        bottommost_confirmation = get_bottommost_confirmation(confirmation)
        if bottommost_confirmation.event_chlnbr.entry not in \
           FConfirmationParams.core_events:
            customer_event_confirmations.add(bottommost_confirmation)
    return customer_event_confirmations

def find_customer_event_confirmations(tr, reset, event_chlnbr, cf = None):
    ''' Return all confirmation records for the given trade and event_chlnbr.
    If the reset is supplied the confirmation must match the reset 
    via the reset_resnbr reference (same goes for cash flow via cfwnbr).
    Make sure event is non core one when calling this function.'''
    log_trace()      

    ret = []
    return ret
    '''
    for conf in get_bottommost_customer_event_confirmations_for_trade(tr):
        if conf.event_chlnbr == event_chlnbr:
            if reset and cf:
                if conf.reset_resnbr and conf.cfwnbr:
                    if reset.resnbr == conf.reset_resnbr.resnbr and \
                       cf.cfwnbr == conf.cfwnbr.cfwnbr:
                        ret.append(get_topmost_confirmation(conf))
            elif reset or cf:
                # choose only reset OR only cf confirmation
                if reset and conf.reset_resnbr:
                    if reset.resnbr == conf.reset_resnbr.resnbr:
                        ret.append(get_topmost_confirmation(conf))
                elif cf and conf.cfwnbr:
                    if cf.cfwnbr == conf.cfwnbr.cfwnbr:
                        ret.append(get_topmost_confirmation(conf))
            else:
                if not conf.reset_resnbr and not conf.cfwnbr:
                    ret.append(get_topmost_confirmation(conf))
                if not cf and conf.cfwnbr:
                    ret.append(get_topmost_confirmation(conf))
    return ret
    '''


def trade_is_correction(trade):
    ''' Return 1 if trade represents a correction trade. '''
    log_trace()
    
    res = 0
    if ((trade) and (trade.correction_trdnbr) and
        (trade.correction_trdnbr != trade)):
        res = 1
    return res


def corr_trade_has_new_cp(trade):
    ''' Return 1 if trade is a correction trade with a new counterparty. '''
    log_trace()
    
    res = 0
    corr_trade = trade.correction_trdnbr
    if (corr_trade and
        trade.counterparty_ptynbr != corr_trade.counterparty_ptynbr):
        res = 1
    return res
    

def corrected_has_confirmation(corr):
    ''' Return 1 if the trade that corr is correcting has a confirmation
    linked to it. '''
    log_trace()

    ret = 0
    trade = corr.correction_trdnbr
    if trade and find_confirmation(trade, None):
        ret = 1
    return ret
    
    
def correction_trade_exist(trade):
    ''' Return 1 if there is another trade that is a correction of the given
    trade, 0 otherwise. '''
    log_trace()
    
    ret = 0
    for t in ael.Trade.select('correction_trdnbr = %d' % trade.trdnbr):
        if t != trade:
            ret = 1
            break
    return ret


def is_postreleased_status(status):
    ''' Return 1 if status is a post released status, 0 otherwise. '''
    log_trace()
    
    ret = 0    
    if status in post_released_statuses:
        ret = 1

    pr = 'confirmation status %s is ' % status
    if ret:
        pr = pr + 'post released'
    else:
        pr = pr + 'pre released'
    log(4, pr)

    return ret


def is_prereleased_confirmation(conf):
    ''' Returns 1 if confirmation status is pre released otherwise 0. '''
    log_trace()
    
    return not is_postreleased_status(conf.status)

    
def is_swift_mode(conf=None, confinst_cp=None):
    ''' Returns true if confirmation instruction is SWIFT '''
    log_trace()
    
    ret = 0    
    if not confinst_cp and not conf:
        log(1, "is_swift_mode: function requires at least one input")
        return ret
    elif not confinst_cp and conf:
        confinst_cp = conf.conf_instruction_seqnbr

    if confinst_cp and confinst_cp.conf_template_chlnbr:
        if confinst_cp.conf_template_chlnbr.entry == 'SWIFT' and \
               confinst_cp.transport == 'Network':
            ret = 1
    
        
    return ret
        

def create_chaser(conf):
    ''' Look for pending matching. Just create chaser in status new. Let
    FConfirmationAMB take care of the rest incl what to do with source conf.'''
    log_trace()
    
    if not conf:
        log(0, 'create_chaser: no confirmation')
        return
    elif is_prereleased_confirmation(conf):
        return
        
    chasers = ael.Confirmation.select('chasing_seqnbr = %d' % conf.seqnbr)

    if not conf.chaser_cutoff:
        pr = 'Confirmation %d is missing chaser cutoff date. ' % conf.seqnbr +\
             'Chaser will not be created.' 
        log(2, pr)
    elif (len(chasers) == 0 and
          conf.chaser_cutoff.days_between(ael.date_today()) >= 0):
        create_new_confirmation(conf.trdnbr, None, param.CHASER, None, \
                                conf.seqnbr, 0)
        pr = "created chaser for confirmation %d" % (conf.seqnbr)
        log(2, pr)
    
def get_cutoff_from_default():
    cutoff = None
    calendar = ael.Instrument[AFB.used_acc_curr()]
    default_days = param.default_chaser_cutoff_days
    if param.default_chaser_cutoff_method_business_days:
        cutoff = ael.date_today().add_banking_day(calendar, \
                                                  default_days)
    else:
        cutoff = ael.date_today().add_days(default_days)
    return cutoff

def get_cutoff_from_business_days(period_count, period_unit):
    cutoff = None
    if period_unit == 'Days':
        calendar = ael.Instrument[AFB.used_acc_curr()]
        cutoff = ael.date_today().add_banking_day(calendar, period_count)
    else:
        pr = 'Business days not supported for' \
             ' unit = %s. Using default cutoff.' % period_unit
        log(0, pr)
        cutoff = get_cutoff_from_default()
    return cutoff

def get_cutoff_from_calendar_days(period_count, period_unit):
    days = 0
    months = 0
    years = 0
    if period_unit == 'Days':
        days = period_count
    elif period_unit == 'Weeks':
        days = period_count * 7
    elif period_unit == 'Months':
        months = period_count
    elif period_unit == 'Years':
        years = period_count
    return ael.date_today().add_delta(days, months, years)

def set_chaser_cutoff(conf):
    '''Sets cutoff time based on confinstruction. '''
    log_trace()
    
    cutoff = None
    confinst = conf.instruction()
    if confinst:
        period_unit = getattr(confinst, 'chaser_cutoff_period.unit')
        period_count = getattr(confinst, 'chaser_cutoff_period.count')
        chaser_cutoff_method = confinst.chaser_cutoff_method
        if chaser_cutoff_method == 'Default':
            cutoff = get_cutoff_from_default()
        elif chaser_cutoff_method == 'Business Days':
            cutoff = get_cutoff_from_business_days(period_count, period_unit)
        elif chaser_cutoff_method == 'Calendar Days':
            cutoff = get_cutoff_from_calendar_days(period_count, period_unit)
        else:
            log(2, 'No chaser cutoff method')
        conf.chaser_cutoff = cutoff
    else:
        log(2, 'No confirmation instruction found for confirmation %d' % \
            conf.seqnbr)
        cutoff = get_cutoff_from_default()
    if cutoff == None:
        log(2, 'Chaser cutoff not set for confirmation %d' % conf.seqnbr)
    else:
        log(2, 'Chaser cutoff set to %s for confirmation %d' % (str(cutoff), \
                                                                conf.seqnbr))
    
def add_status_explanation(se, expl):
    ''' Adds new Status Explanation value.
    se   - old status explantation value
    expl - string representation of the status explanation to be added to se
    '''
    log_trace()
    
    enm = ael.enum_from_string('StatusExplanation', expl)
    if enm:
        bitpattern = pow(2, enm)
        if not bitpattern & se:
            se |= bitpattern
            pr = 'adding %s to status explanation, ' \
                 'new value %d' % (expl, se)
            log(5, pr)
    else:
        pr = 'enum_to_string %s failed'  % expl
        log(1, pr)
        
    return se

    
def add_status_explanation_conf(conf, expl):
    ''' Wrapper for add_status_explanation. '''
    log_trace()

    return add_status_explanation(conf.status_explanation, expl)


def has_status_explanation(se, expl):
    ''' Return 1 if status explanation se contains expl as status explanation.
    '''
    log_trace()
    
    ret = 0
    enm = ael.enum_from_string('StatusExplanation', expl)
    if enm:
        bitpattern = pow(2, enm)
        if bitpattern & se:
            ret = 1
    else:
        pr = 'enum_to_string %s failed'  % expl
        log(1, pr)
        
    return ret


def has_status_explanation_conf(conf, expl):
    ''' Wrapper for has_status_explanation. '''
    log_trace()
    
    return has_status_explanation(conf.status_explanation, expl)


def get_status_explanation_as_string(conf, value=None,  *rest):
    ''' Returns a string representation of the status explanation.
    An input can be either entity e or a status explanation value.
    This function can be called via ASQL. '''
    log_trace()
    
    res = ''
    if conf:
        value = conf.status_explanation
    if value:    
        i = 0
        while i < 32:
            bitpattern = pow(2, i)            
            if (bitpattern & value) > 0:
                s = ael.enum_to_string('StatusExplanation', i)
                if s == '?':
                    break
                res = res + s + ', '
            i += 1
            
        if res[len(res)-2:] == ', ':
            res = res[:len(res)-2]
        
    return res


def get_resets(trade):
    ''' Get all fixed resets for trade. '''
    log_trace()
    resets = []
    for l in trade.insaddr.legs():
        for c in l.cash_flows():
            if c.is_fixed():
                for r in c.resets():
                    if not utils.IsWeightedReset(r):
                        resets.append(r)

    return resets


def get_reset_confirmations(trade):
    ''' Get all fixed reset confirmations for trade. 
    The selection will include client event confirmations.'''
    log_trace()

    conf_list = []
    for reset in get_resets(trade):
        confs = find_confirmations(trade, reset)
        for c in confs:
            if c not in conf_list:
                conf_list.append(c)

    return conf_list


def update_reset_trade_reference(correction_trade, reset_confirmation):
    ''' Change the trade reference on the reset confirmations related to
    corrected_trade to correction_trade.'''
    log_trace()

    reset_confirmation_clone = reset_confirmation.clone()
    reset_confirmation_clone.trdnbr = correction_trade
    commit_confirmation(reset_confirmation_clone)

def trade_status_ok(status):
    ''' Check that the status matches the user defined list of valid trade
    statuses. '''
    log_trace()
    
    ret = 0
    if status in param.valid_trade_statuses:
        ret = 1
    else:
        pr = 'confirmation not generated for trade status %s' % (status)
        log(2, pr)
            
    return ret

def position(trade):
    ''' Return confirmation position for instrument and counterparty connected
    to conf. '''
    log_trace()

    pos = 0
    if trade.insaddr:
        for t in trade.insaddr.trades():
            if (t.counterparty_ptynbr == trade.counterparty_ptynbr and
                t.status not in ['Void', 'Confirmed Void', 'Simulated']):
                pos += AFB.trade_nominal_amount(t.trdnbr)

    return pos
def is_cancellation_or_amendment(conf):
    event_chlnbr_as_string = conf.event_chlnbr.display_id()
    return event_chlnbr_as_string == 'Cancellation' or event_chlnbr_as_string == 'Amendment'

def cancel_confirmation(conf):
    ''' Trade is voided.  If conf is pre-released delete conf, otherwise void
    conf and create cancellation. '''
    log_trace()
        
    tr = conf.trdnbr            
    if tr:
        is_child = len(ael.Confirmation.select('confirmation_seqnbr = %d' % conf.seqnbr)) > 0            
        if not (tr.correction_trdnbr == tr or correction_trade_exist(tr)):
            if not is_child:
                cancellation_creation(conf)
        if not is_child:
            pr = 'trade %d, status=%s, voiding conf %d (status %s)' % \
                 (tr.trdnbr, tr.status, conf.seqnbr, conf.status)
            log(2, pr)
            change_status_and_commit(conf, 'Void')

def log(level, s):
    ''' Log string s if level is less than the log_level setting in
    FConfirmationVariables. '''
    
    if param.log_level >= level:
        stack_array = inspect.stack()
        fnk_name = stack_array[1][3]
        ael.log(fnk_name + ': ' + s)
    
def log_trace(silent = 0):
    ''' Print information about the function that log_trace is called from. '''

    if not silent:
        FOperationsUtils.LogTrace()


def change_status(conf, new_status, expl=0):
    ''' Set new_status and status explanation for confirmation conf. If new
    status is Released the chaser cutoff information will be set. '''
    log_trace()

    if new_status == 'Acknowledged':
        set_chaser_cutoff(conf)
    
    if new_status == 'Manual Match':
        conf.manual_match = 1

    pr = "changing status from %s to %s" % (conf.status, new_status)
    log(3, pr)
    conf.status = new_status

    if expl:
        pr = 'setting status explanation to %d' % expl
        log(5, pr)
    conf.status_explanation = expl

def change_status_and_commit(conf, new_status, expl = 0):
    ''' Confirmation conf gets status new_status and is then committed. '''
    log_trace()
    
    old_status = conf.status
    c = conf.clone()
    change_status(c, new_status, expl)
    commit_confirmation(c, old_status)

def raise_commit_exception(function_name, runtime_error):
    if (str(runtime_error).find("Update collision") != -1):
        raise UpdateCollisionException("Update Collision Exception in %s!" % function_name, runtime_error)
    else:
        raise CommitException("Commit Exception in %s!" % function_name, runtime_error)
    
def commit_confirmation(conf, old_status=None):
    ''' Commit the confirmation record and log status change. '''
    log_trace()
    if old_status and old_status != conf.status:
        pr = 'changing status %s to %s' % (old_status, conf.status)
        log(4, pr)
    try:
        conf.commit()
    except RuntimeError, error:
        raise_commit_exception(commit_confirmation.__name__, error)

def commit_transaction():
    ''' Wrapper for ael.commit_transaction(). '''
    log_trace()

    try:
        ael.commit_transaction()
    except RuntimeError, error:
        log(0, 'commit_transaction failed, aborting')
        ael.abort_transaction()
        raise_commit_exception(commit_transaction.__name__, error)

def confirmations_in_status(status):
    ''' Returns Confirmations in certain status. '''
    log_trace()
    
    confs = ael.Confirmation.select('status="%s"' % status)
    nr = len(confs)
    if nr:
        pr = "%d confirmations in status %s found" % (nr, status)
        log(0, pr)
    return confs


def get_bic(contact):
    ''' Returns BIC code of the contact. '''
    log_trace()
    
    ok = 0
    ret = ''
    network = contact.network_alias_seqnbr    
    if network:                
        if network.type and network.type.alias_type_name == 'SWIFT':
            ok = 1
            ret = network.alias            
    
    if not ok:
        network = contact.network2_alias_seqnbr
        if network:            
            if network.type and network.type.alias_type_name == 'SWIFT':
                ret = network.alias
    return ret


def get_confirmations_from_party(pty):
    ''' Returns prereleased confirmations not in status Hold. See also
    find_confirmations. Client events confirmations are included.'''
    log_trace()

    ret = []
    if pty:
        for conf in ael.pre_released_confirmations():
            if (conf.trdnbr and
                (conf.trdnbr.counterparty_ptynbr == pty or
                 conf.trdnbr.acquirer_ptynbr == pty) and
                not preserve_conf(conf)):
                ret.append(conf)
    return ret

def get_confirmations_from_instrument(ins):
    ''' Returns confirmations connected to the instrument through
        the trades. See also find_confirmations and preserve_conf. '''
    log_trace()

    ret = []
    if ins:
        for tr in ins.trades():
            conf = find_confirmation(tr, None)
            if conf and not preserve_conf(conf):
                ret.append(conf)

        for i in ael.Instrument.select('und_insaddr = %d' % ins.insaddr):
            ret = ret + get_confirmations_from_instrument(i)
    return ret

def get_event_printable(event_chlnbr):
    ''' Returns the choice list string from the given event_chlnbr. '''
    log_trace()
    
    chl = None
    event_str = ''

    if isinstance(event_chlnbr, ael.ael_entity):
        chl = event_chlnbr
    else:        
        chl = ael.ChoiceList[event_chlnbr]

    if chl:
        event_str = chl.entry
    return event_str
           

def set_protection_fields(confirmation, protection, owner_usrnbr):
    ''' Set the protection fields of the confirmation according to protection
    and owner_user. '''
    log_trace()

    if confirmation:
        confirmation.protection = protection
        confirmation.owner_usrnbr = owner_usrnbr


def copy_protection_from_confirmation(new_conf, old_seqnbr):
    ''' Copy protection settings from old_seqnbr to new_conf. '''
    log_trace()
    
    old_conf = ael.Confirmation[old_seqnbr]
    if old_conf:
        set_protection_fields(new_conf, old_conf.protection,
                              old_conf.owner_usrnbr.usrnbr)


def copy_protection_from_trade(confirmation, trade):
    ''' Copy the protection settings of trade to confirmation. '''
    log_trace()
    
    if trade:
        set_protection_fields(confirmation, trade.protection,
                              trade.owner_usrnbr.usrnbr)

def build_primary_key_dict():
    ''' Build the dictionary containing all tables and its 
        primary keys '''
    log_trace()

    for ael_obj in dir(ael):
        expr = 'ael.%s' % ael_obj
        if(isinstance(eval(expr), ael.ael_table)):
            table_name = ael_obj.upper()
            expr = 'ael.%s.keys()' % ael_obj
            for k in eval(expr):
                if k[1] == 'primary':
                    primary_key_dict[table_name] = k[0].upper()
                    continue
                    

def get_primary_key_field(record_type):
    ''' Returns the field name of the record primary key.
        Example: For INSTRUMENT this is INSADDR '''
    #log_trace()

    record_type = record_type.upper()
    if (len(primary_key_dict) == 0):
        build_primary_key_dict()
    if (primary_key_dict.has_key(record_type)):
        return primary_key_dict[record_type]
    else:
        return ''

def get_primary_key_value(entity):
    ''' Return the value of the primary key of entity. '''
    #log_trace()

    if not entity:
        return ''
    else:
        return getattr(entity, get_primary_key_field(entity.record_type).lower())

def is_a_correct_trade_structure(conf):
    is_amendment = False        
    event_chlnbr_as_string = conf.event_chlnbr.display_id()
    if event_chlnbr_as_string == 'Cancellation':
        if conf.confirmation_seqnbr != None:
            if conf.confirmation_seqnbr.event_chlnbr.display_id() == "Amendment":
                is_amendment = True
    return is_amendment
