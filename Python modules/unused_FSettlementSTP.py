""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementSTP - Module including STP functions.

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    STP

----------------------------------------------------------------------------"""
def run_netting(settle):
    '''Returns 1 if netting is done. '''
    result=0
    if settle:
        result = FSettlementNetting.SingleNetting(settle)
    return result

def run_clientSTP(settlement):
    ''' settlement as stt_c??'''
    try:
        #convert settlement=stt_c to entity
        FSettlementClientSTP.clientSTP(settlement)
    except Exception, e:
        pr = 'ERROR: %s. Unable to run client STP for settlement %d' % \
             (str(e), settlement.seqnbr)
        log(0, pr)

def commit_and_set_status_explanation(settle, status, status_explanation, param):
    ''' '''
    clone = settle.clone() # If settle is stt_c clone can be done anyway
    clone.status = status
    if status == 'Authorised':
        if status_explanation != 64:
            FSettlementGeneral.clear_status_explanation(clone)
        elif param.authorise_historic_value_day:
            pr = 'Setl %d will be Authorised but with Historic value day status explanation' % (settle.seqnbr)
            log(0, pr)
        else:
            FSettlementGeneral.clear_status_explanation(clone)
    else:
        clone.status_explanation = status_explanation
    try:
        clone.commit()
    except Exception, e:
        pr = 'Error: %s. Unable to commit settlement (File)' % (str(e))
        log(0, pr)

def settle_apply_for_stp(seqnbr, stt_c=None):
    ''' '''
    ok = 0
    if seqnbr:
        settle = ael.Settlement[seqnbr]
        if settle:
            if settle.status in FSettlementGeneral.stp_status:        
                if settle.status=='Exception':
                    if FSettlementGeneral.check_status_exp(settle.status_explanation):
                        ok = 1
                else:
                    ok = 1
        else:
            pr = 'Can not find settlement %d (Error)' % (seqnbr)
            log(0, pr)
            
    return ok

def log(level, s):
    return FSettlementGeneral.log(level, s)
    
"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
import ael, time, FSettlementGeneral, FSettlementNetting
try:
    import FSettlementClientSTP
except ImportError:
    import FSettlementClientSTPTemplate as FSettlementClientSTP
import FSettlementGeneral2

def STP(settle, param):
    '''settle can be both stt_c and entity'''
    ZoneInfoImported = param.ZoneInfoImported
    if settle and settle_apply_for_stp(settle.seqnbr):
        if settle.record_type == 'Settlement':
            log_str = 'Running STP rules on Settlement %d, status %s' % (settle.seqnbr, settle.status)
            log(1, log_str)
            status_explanation = settle.run_stp()

            if status_explanation == 0:
                if settle.ref_type=='None':
                    if settle.manual_match:
                        pr = 'STP: Manually matched Setl about to be Authorised'
                        log(2, pr)    
                        commit_and_set_status_explanation(settle, 'Authorised',\
                                                          status_explanation, param)
                    elif not run_netting(settle):
                        log(1, 'Not netted, calling client STP')
                        run_clientSTP(settle)
                elif settle.ref_type=='Net' and not settle.manual_match:
                    pr = "STP: Calling client STP on netted Setl (not manually matched)"
                    log(2, pr)
                    run_clientSTP(settle)
                else:
                    log(2, 'STP: Authorise (not Net nor child)')
                    commit_and_set_status_explanation(settle, 'Authorised',\
                                                      status_explanation, param)
            elif settle.status == 'Exception' and status_explanation == 64 \
            and param.authorise_historic_value_day:                                
                pr = 'STP: Historic value day BUT about to be Authorised'
                FSettlementGeneral.log(1, pr)
                commit_and_set_status_explanation(settle, 'Authorised',\
                                                      status_explanation, param)            
            else:
                pr = 'STP: about to get status Exception (status_explanation %d)' % (status_explanation)
                log(2, pr)
                commit_and_set_status_explanation(settle, 'Exception',\
                                                  status_explanation, param)
    elif not settle:
        pr = 'STP: no settlement deployed as input (Error)'
        log(1, pr)
    return


