"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! PLEASE NOTE - This module has been deprecated. Any new functionality should be added to the Operations STP ATS. !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

PURPOSE           : This ATS should perform automated amendments on any object
                    based on system and user changes to confirmations and settlements.
                    Some of the latter "STP" fuctionality would currently sit
                    in FValidation and will be moved to this service piece by piece.

================================================================================
HISTORY
================================================================================
Date        Change no           Developer               Description
--------------------------------------------------------------------------------
                                Gabriel Marko           Initial development.
2017-02-10  CHNG0004099366      Willie van der Bank     Added enableAutoMatchConfo and
                                                        enableAutoReleaseSettlementForConfos.
2017-11-07  CHNG0005091348      Willie van der Bank     Added enableEncryption.
2017-12-11  CHNG0005220511      Willie van der Bank     Added DIS_Auto_Release.
2018-05-11  CHG1000406751       Willie van der Bank     Added enableAutoReleaseSettlement.
2018-05-15  CHG1000470615       Willie vd Bank          Corrected date format which is required on the back end.
2018-11-29                      Joash Moodley           Automated Demat Settlements.
2018-11-30  FAOPS-226           Cuen Edwards            Added enableTradeBOConfirmingPostAffirm.
2019-01-31  FAOPS-378           Cuen Edwards            Added enableMT320AutoProcessing.
2019-02-22  FAOPS-394           Tawanda Mukhalela       Added enableAdjustDepositSettlementAutoRelease.
2019-04-05  FAOPS-448           Cuen Edwards            Deprecation of this module and start of functional migration.
2019-04-05  FAOPS-481           Cuen Edwards            Migration of functionality for FAOPS-378.
2019-04-05  FAOPS-482           Cuen Edwards            Migration of functionality for FAOPS-226.
2019-04-12  FAOPS-483           Cuen Edwards            Migration of functionality for CHNG0004099366.
2020-11-22  SRG                 Tawanda Mukhalela       Added DIS confirmations with no cashflow to be auto released.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! PLEASE NOTE - This module has been deprecated. Any new functionality should be added to the Operations STP ATS. !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

import acm
import ael
from at_time import acm_date
from datetime import datetime
from Queue import Queue
from at_addInfo import save
from Confirmation_Encrypted_XML import create_xml_file_main
from Confirmation_Encrypted_FT import move_zip_file_main

#Functions:
enableEncryption = True
enableAutoReleaseSettlement = True
enableAutoReleaseSettlementPostConfirm = True
enableConfDISAutoRelease = True
enableAdjustDepositSettlementAutoRelease = True

# AR == Auto Release
AR_CONF_QF = 'Conf_For_Settmnt_Auto_Release'
ENCR_CONF_QF = 'Conf_Encrypt_XML'
DIS_CONF_QF = 'Conf_DIS_Auto_Release'
AR_STMNT_QF = 'Settmnt_Auto_Release'
ADJUST_DEPOSIT_CONF_QF = 'Conf_Adjust_Deposit_Auto_Release'
DEBUG = False
request_queue = Queue()


def start():
    print "Starting ATS..."

    # Recovering procedures...
    request_queue.put('Checking for backlog...')
    
    if enableEncryption:
        #print "Trying to create encryption XML"
        valid_confirmation = qf_select_conf_parent_only(ENCR_CONF_QF)

        for confirmation in valid_confirmation:
            if confirmation not in request_queue.queue:
                request_queue.put(confirmation)
                if DEBUG:
                    _print_debug_block(confirmation, 'Added to backlog queue')
                
    if enableAutoReleaseSettlement:
        #print "Trying to release auto-releasable settlements"
        valid_settlement = acm.FStoredASQLQuery[AR_STMNT_QF].Query().Select()

        for settlement in valid_settlement:
            if settlement not in request_queue.queue:
                request_queue.put(settlement)

    valid_confirmation = []
    
    if enableAutoReleaseSettlementPostConfirm:
        #print "Trying to release auto-releasable settlements post confirmation"
        valid_confirmation += list(acm.FStoredASQLQuery[AR_CONF_QF].Query().Select())

    if enableConfDISAutoRelease:
        #print "Trying to release auto-releasable settlements"
        valid_confirmation += list(acm.FStoredASQLQuery[DIS_CONF_QF].Query().Select())

    if enableAdjustDepositSettlementAutoRelease:
        valid_confirmation += list(acm.FStoredASQLQuery[ADJUST_DEPOSIT_CONF_QF].Query().Select())
    
    valid_confirmation = list(set(valid_confirmation) - set(request_queue.queue))
    for confirmation in valid_confirmation:
        request_queue.put(confirmation)

    request_queue.put('Backlog processed.')
    
    ael.Confirmation.subscribe(_listener)
    ael.Settlement.subscribe(_listener)
    print "Startup completed successfully."
    return True



def stop():
    print "Stopping ATS..."
    ael.Confirmation.unsubscribe(_listener)
    ael.Settlement.unsubscribe(_listener)


def work():
    while not request_queue.empty():
        #Not sure whether entity will always have record_type or RecordType
        #time.sleep(0.1) #without this sleep it sometimes misses update events
        entity = request_queue.get()
        if hasattr(entity, 'record_type'):
            if entity.record_type == 'Confirmation':
                print 'WORK: processing AEL confirmation %s' % entity.seqnbr
                confirmation_update(acm.FConfirmation[entity.seqnbr])
            elif entity.record_type == 'Settlement':
                print 'WORK: processing AEL settlement %s' % entity.seqnbr
                settlement_update(acm.FSettlement[entity.seqnbr])
        elif hasattr(entity, 'RecordType'):
            if entity.RecordType() == 'Confirmation':
                print 'WORK: processing ACM confirmation %s' % entity.Oid()
                confirmation_update(entity)
            elif entity.RecordType() == 'Settlement':
                print 'WORK: processing ACM settlement %s' % entity.Oid()
                settlement_update(entity)


def _listener(o, entity, arg, operation):
    """Adds the entity and the original entity to the request queue."""
    #time.sleep(0.1) #without this sleep it sometimes misses update events
    if entity not in request_queue.queue:
        print "LISTENER: adding to queue %s, %s" % (entity.seqnbr, entity.record_type)
        request_queue.put(entity)
    else:
        print "LISTENER: already in queue %s, %s" % (entity.seqnbr, entity.record_type)
        if DEBUG:
            print 'Object', entity.seqnbr, 'skipped.'


def settlement_update(settlement):
    """Main method for postprocessing settlements.

    It's subscribed to the Settlements table.
    """
    if enableAutoReleaseSettlement:
        if satisfies_qf(settlement, AR_STMNT_QF):
            auto_release_settlement(settlement)


def confirmation_update(confirmation):
    """Main method for postprocessing confirmations.

    It's subscribed to the Confirmation table.
    """
    #if not hasattr(confirmation, 'Oid'):
    #    confirmation = acm.FConfirmation[confirmation.seqnbr]

    # For testing purposes
    if DEBUG:
        _print_debug_block(confirmation)

    if enableEncryption:
        if satisfies_qf_empty_string(confirmation, ENCR_CONF_QF):
            print 'Encryption process started...'
            completed = 'Encryption process unsuccessful!'
            if create_xml_file_main(confirmation):
                if move_zip_file_main(confirmation):
                    save(confirmation, 'PendMatchStatus', 'XMLSent')
                    completed = 'Encryption process completed.'
            print completed

    if enableAutoReleaseSettlementPostConfirm:
        if satisfies_qf(confirmation, AR_CONF_QF):
            auto_release_related_settlements(confirmation)
            return
    
    if enableConfDISAutoRelease:
        if satisfies_qf(confirmation, DIS_CONF_QF):
            auto_release_dis_confirmation(confirmation)
            return
    
    if enableAdjustDepositSettlementAutoRelease:
        if satisfies_qf(confirmation, ADJUST_DEPOSIT_CONF_QF):
            auto_process_adjust_deposit_confirmation(confirmation)


def auto_release_dis_confirmation(confirmation):
    message = ''
    if confirmation.Status() == 'Hold':
        confirmation.Status('Pending Document Generation')
        message = "DIS confirmation %s moved out of Hold" % confirmation.Oid()

    elif confirmation.Status() == 'Authorised':
        if not confirmation.CashFlow():
            confirmation.Status('Released')
            message = "DIS confirmation %s Released" % confirmation.Oid()

        elif confirmation.CashFlow().AdditionalInfo().Demat_Calc_Approvl() is True:
            confirmation.Status('Released')
            message = "DIS confirmation %s Released" % confirmation.Oid()

        else:
            confirmation.Status('Hold')
            message = "DIS confirmation %s moved to Hold" % confirmation.Oid()
            
    if message != '':
        try:
            confirmation.Commit()
            print message
        except Exception as ex:
            print "DIS confirmation %s update failed" % confirmation.Oid()
            print ex
        

def auto_release_settlement(settlement):
    """Auto release settlement independent of confirmation."""
    print "Trying to auto-release settlements"
    release_settlement(settlement)
            
            
def auto_release_related_settlements(confirmation):
    """Auto release settlement having the same cashflow as the confirmation."""

    print "Trying to auto-release settlements"

    settlements = find_related_settlements(confirmation)

    if not settlements:
        print "No settlements to release."
        return

    print "%s settlement(s) to release" % len(settlements)

    for settlement in settlements:
        if validate_settlement(settlement):
            release_settlement(settlement)
        else:
            print "Settlement: %s (%s) skipped" % (
                settlement.Oid(),
                settlement.Status()
            )


def find_related_settlements(confirmation):
    """Find settlements with the same cashflow as the confirmation."""
    if confirmation.CashFlow() is None:
        print "Confirmation has no cashflow"
        return

    if confirmation.Trade() is None:
        print "Confirmation has no trade"
        return

    cf_number = confirmation.CashFlow().Oid()

    print "Cashflow: %s" % cf_number

    related_settlements = [
        settlement
        for settlement in confirmation.Trade().Settlements()
        if settlement.CashFlow() and settlement.CashFlow().Oid() == cf_number
        and settlement.Status() == 'Authorised'
        and settlement.Amount() < 0
    ]

    return related_settlements


def validate_settlement(settlement):
    return (
        settlement.Status() == 'Authorised'
        and settlement.ValueDay() == acm_date(ael.date_today()) #this exact date format is required for correct ATS processing
    )
    
    
def release_settlement(settlement):
    try:
        # Set Call_Confirmation AddInfo.
        save(
            settlement,
            'Call_Confirmation',
            _get_call_confirmation_value(settlement)
        )
        # Set Authorise Debit AddInfo.
        if _is_incoming_settlement(settlement):
            save(
                settlement,
                'Authorise Debit',
                'Yes'
            )
        settlement.Status = 'Released'
        settlement.Commit()
        print "Settlement: %s released" % settlement.Oid()
    except Exception as ex:
        print "Settlement: %s wasn't released" % settlement.Oid()
        print ex


def hold_settlement(settlement):
    """
    Change the status of a settlement to hold.
    """
    try:
        print('Auto-holding settlement {settlement_oid}.'.format(
            settlement_oid=settlement.Oid()
        ))
        settlement = settlement.StorageImage()
        settlement.Status = 'Hold'
        settlement.Commit()
        print('Auto-holding completed for settlement {settlement_oid}.'.format(
            settlement_oid=settlement.Oid()
        ))
    except Exception as ex:
        exception_message = 'Unable to auto-hold settlement {settlement_oid}.'
        print(exception_message.format(
            settlement_oid=settlement.Oid()
        ))
        print ex


def auto_process_adjust_deposit_confirmation(confirmation):
    """
    Auto release incoming payment for Matched Ajdust Deposit Confirmation
    :param confirmation    
    """
    settlement = _get_incoming_settlement(confirmation)
    if _is_correct_settle_type(confirmation) and settlement:
        if _is_incoming_settlement(settlement) and settlement.Status() == 'Authorised':
            accounts = acm.FAccount.Select("party = %i and account = '%s' and correspondentBank = '%s' " % (settlement.Counterparty().Oid(), settlement.TheirCorrAccount(), settlement.TheirCorrBank()))
            if len(accounts) == 1 and accounts[0].Bic().Name() == 'ABSAZAJJ' and confirmation.Status() == 'Matched':
                release_settlement(settlement)
            else:
                hold_settlement(settlement)


def _get_call_confirmation_value(settlement):
    """
    Get the Call_Confirmation additional info value to populate
    for a settlement.
    """
    call_confirmation_value = 'AutoRelease'
    demat_sett = settlement.Trade().Instrument().AdditionalInfo().Demat_Instrument()
    if demat_sett and settlement.CashFlow():
        demat_ce_ref = settlement.CashFlow().AdditionalInfo().Demat_CE_Reference()
        if demat_ce_ref:
            call_confirmation_value = "{0}CEM{1}".format(demat_ce_ref[:4], demat_ce_ref[4:])
    return call_confirmation_value


def _is_incoming_settlement(settlement):
    """
    Determines whether or not a specified settlement represents an
    incoming settlement.
    """
    return settlement.Amount() > 0


def _is_correct_settle_type(confirmation):
    """
    Get payment flow 
    """
    settle_type = 'Debit Cheque Account'
    cashflow = confirmation.CashFlow()
    if cashflow.AdditionalInfo().Settle_Type() == settle_type and cashflow.CashFlowType() == 'Fixed Amount':
        return True
        
    return False
    

def _get_incoming_settlement(confirmation):
    """
    get applicable settlment for matched confirmation
    """
    cashflow = confirmation.CashFlow()
    Settlements = [settlement 
                    for settlement in confirmation.Trade().Settlements()
                    if settlement.CashFlow() == cashflow and settlement.ValueDay() == confirmation.CreateDay() and settlement.SettlementType() == cashflow.CashFlowType()] 
    if len(Settlements):
        return Settlements[0]
                
    return None


def satisfies_qf(obj, qf_name):
    return acm.FStoredASQLQuery[qf_name].Query().IsSatisfiedBy(obj)


def satisfies_qf_empty_string(obj, qf_name):
    #IsSatisfiedBy doesn't work on a query folder which contains <Empty String> criteria
    valid_confirmations = qf_select_conf_parent_only(qf_name)
    return obj in valid_confirmations


def qf_select_conf_parent_only(qf_name):
    #Doing a Select on a qf returns the parent and children items, therefore additional filtering is required
    valid_confirmations_refs = []
    valid_confirmations = acm.FStoredASQLQuery[qf_name].Query().Select()
    for conf in valid_confirmations:
        for tradeconf in conf.Trade().Confirmations():
            valid_confirmations_refs.append(tradeconf.ConfirmationReference())
    #unique_valid_confirmations = [v_c for v_c in valid_confirmations if v_c not in valid_confirmations_refs]
    unique_valid_confirmations = list(set(valid_confirmations) - set(valid_confirmations_refs))
    return unique_valid_confirmations


def _print_debug_block(confirmation, text = None):
    print
    print 'Additional logging enabled...'
    print datetime.now()
    if text:
        print text
    print "Confirmation: %s" % confirmation.Oid()
    print "Confirmation Status: %s" % confirmation.Status()
    print "Event Type: %s" % confirmation.EventType()
