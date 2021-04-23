"""----------------------------------------------------------------------------
MODULE:
    FSecuritySettlementInProcessing

DESCRIPTION:
    OPEN EXTENSION MODULE
    User can write custom logic to be executed in each state of the
    FSwiftSecuritySettlementIn business process. It is derived from
    FSecuritySettlementInProcessingBase

    The function prototype should be : process_state_xxx(business_process)
    where xxx is state name e.g. process_state_ready

    The base class implements following state processing:
     - process_state_ready
     - process_state_paired
     - process_state_partialmatch

    If user wishes to add some extra processing for conditional entry state
     e.g. 'ready' he can implement method as
    def process_state_ready(self):
        # Custom logic before core logic
        super(FSecuritySettlementInProcessing, self).process_state_ready()
        # Custom logic after core logic

VERSION: 2.2.0-0.5.3102
----------------------------------------------------------------------------"""
import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('SecSetlConf', 'FSecuritySettlementInNotify_Config')
import FSecuritySettlementInProcessingBase
import FSwiftMLUtils
import acm
import sl_settlement_return_cancel

class FSecuritySettlementInProcessing(FSecuritySettlementInProcessingBase.FSecuritySettlementInProcessingBase):
    def __init__(self, bpr):
        super(FSecuritySettlementInProcessing, self).__init__(bpr)

    def process_state_xxx(self):
        """ process bpr state xxx"""
        try:
            notifier.INFO("Processing BPR step xxx")
            notifier.INFO("Completed processing BPR step xxx")
        except Exception as e:
            notifier.ERROR("Error occurred while processing BPR step xxx: %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

class FSecuritySettlementStatusProcessingAdviceInProcessing(FSecuritySettlementInProcessingBase.FSecuritySettlementStatusProcessingAdviceInProcessingBase):
    def __init__(self, bpr):
        '''
        **********************IMPORTANT NOTE**************************
        the reason why init mehtod is also overrideen is because how the Base class handles the defining of process_state_xxx methods with common_implementation. This makes our overrides inefffective . 
        So setattr on methods is called again
        
        Remove below when SPR 431945 is fixed
        '''
        super(FSecuritySettlementStatusProcessingAdviceInProcessing, self).__init__(bpr)
        setattr(self, 'process_state_paired', self.process_state_paired_derived)
        setattr(self, 'process_state_acknowledged', self.common_implementation_derived)
        setattr(self, 'process_state_matched', self.common_implementation_derived)
        setattr(self, 'process_state_pendingsettlement', self.common_implementation_derived)
        setattr(self, 'process_state_rejected', self.common_implementation_derived)
        setattr(self, 'process_state_failingsettlement', self.common_implementation_derived)
        setattr(self, 'store_new_message', self.store_new_message_derived)
            

        '''
        For 598_130 Positive flow is 0101NAFI(Acknowledged)->0101AFFI(Matched)->0258(PendingSettlement)->0601(Processed)
        For 598_131 Positive flow is 0201(Matched)->0258(PendingSettlement)->0601(Processed)
        '''
        self.status_to_event_dict_for_STRATE_548 = {
                                     '0101NAFI':'Acknowledge',
                                     '0101AFFI':'Match',
                                     '0258':'Pending',
                                     '0201':'Match',
                                     '0601':'Done',
                                     '0901':'Reject',
                                     '0835':'Failing'
                                     }

    def store_new_message_derived(self, log_text):
        bpr_diary = self.business_process.Diary()
        current_step = self.business_process.CurrentStep()
        entry = bpr_diary.GetEntry(self.business_process, current_step)

        notes_entry = log_text + '\n' +self.theirs.swift_data
        entry.Notes().AtInsert(0, notes_entry)
        entry.Parameters()['Error'] = log_text
        bpr_diary.PutEntry(self.business_process, current_step, entry)
        self.business_process.Commit()

    def trigger_event(self, event_to_trigger):
        
        bpr_state = self.business_process.CurrentStep()
        current_state = bpr_state.State().Name()
        if bpr_state:
            if event_to_trigger in bpr_state.ValidEvents():
                event_triggered =  FSwiftMLUtils.trigger_event(self.business_process, event_to_trigger, self.theirs.swift_data)
                if not event_triggered:
                    log_text = "Cannot process event '%s' from current state '%s' " % (event_to_trigger, current_state)
                    self.store_new_message(log_text)
                    notifier.WARN(log_text)
            else:
                if event_to_trigger is None:
                    log_text = "Transition for the status '%s' from current state '%s' is not supported" % (
                        self.current_status, current_state)

                else:
                    log_text = "Event '%s' from current state '%s' is not valid"%(event_to_trigger, current_state)

                notifier.WARN(log_text)
                self.store_new_message_derived(log_text)

    def process_state_paired_derived(self):
        """ process bpr state Paired"""
        """****************IMPORTANT NOTE******************
        the check for self.call_process_state_flag is not here for paired state because it's not a landing state.
        When you come here bpr is not supposed to stay here, it should just move ahead. 
        """
        try:
            acm_obj = FSwiftMLUtils.get_acm_object_from_bpr(self.business_process)
            if not self.is_Front_Arena_SBL_settlement(acm_obj):
                notifier.ERROR("Not a valid Front Arena SBL settlement %s. Bypass BPR step Paired." % acm_obj.Oid())
                return   
            notifier.INFO("Processing BPR step Paired")
            status_code = self.theirs.StatusCode()
            self.current_status = status_code[-4:]
            if self.current_status == '0101': 
                if 'NAFI' in self.theirs.python_object.SequenceB_SettlementTransactionDetails.SettlementInstructionProcessingNarrative.value():
                    self.current_status = '0101NAFI'
            event_to_trigger = self.status_to_event_dict_for_STRATE_548.get(self.current_status)
            self.trigger_event(event_to_trigger)
            self.update_statuses_settlement(self.business_process, status_code[-4:])
            notifier.INFO("Completed processing BPR step Paired")
        except Exception as e:
            notifier.ERROR("Error occurred while processing BPR step Paired: %s" % str(e))
            notifier.DEBUG(str(e), exc_info=1)

    def common_implementation_derived(self):
        """ process bpr state xxx"""
        if self.call_process_state_flag:
            try:
                acm_obj = FSwiftMLUtils.get_acm_object_from_bpr(self.business_process)
                if not self.is_Front_Arena_SBL_settlement(acm_obj):
                    notifier.ERROR("Not a valid Front Arena SBL settlement %s. Bypass business process update." % acm_obj.Oid())
                    return 
                current_state = self.business_process.CurrentStep().State().Name()
                if self.theirs.is_STRATE_reply():
                    notifier.INFO("Processing BPR step %s" % current_state)
                    status_code = self.theirs.StatusCode()
                    
                    self.current_status = status_code[-4:]
                    if self.current_status == '0101': 
                        if 'AFFI' in self.theirs.python_object.SequenceB_SettlementTransactionDetails.SettlementInstructionProcessingNarrative.value():
                            self.current_status = '0101AFFI'
                    event_to_trigger = self.status_to_event_dict_for_STRATE_548.get(self.current_status)
                    self.trigger_event(event_to_trigger)
                    self.update_statuses_settlement(self.business_process, status_code[-4:])
                    notifier.INFO("Completed processing BPR step %s" % str(current_state))
                
            except Exception as e:
                current_state = self.business_process.CurrentStep().State().Name()
                notifier.ERROR("Error occurred while processing BPR step %s: %s"%(current_state, str(e)))
                notifier.DEBUG(str(e), exc_info=1)
    
    def is_Front_Arena_SBL_settlement(self, acm_obj):
        if not acm_obj.Trade():
            return False
                
        if acm_obj.Trade().TradeInstrumentType() != 'SecurityLoan' and acm_obj.Trade().TradeCategory() != 'Collateral':
            return False
        
        if not acm_obj.Acquirer():
            return False
        
        if acm_obj.Acquirer().Name() != 'SECURITY LENDINGS DESK':
            return False
            
        return True
        
    def update_statuses_settlement(self, bpr, status_code):
        try:
            acm_obj = FSwiftMLUtils.get_acm_object_from_bpr(bpr)
            acm_obj_si = acm_obj.StorageImage()
            settlement_number = acm_obj.Oid()
            notifier.INFO("Processing SWIFT for settlement %s" % settlement_number)
            if acm_obj_si.Status() == 'Released':
                notifier.INFO("Setting settlement %s to Acknowledged" % settlement_number)
                acm_obj_si.Status('Acknowledged')
                acm_obj_si.Commit()
                        
            if status_code == '0601':
                notifier.INFO("Setting settlement %s to Settled" % settlement_number)
                acm_obj_si.Status('Settled')
                acm_obj_si.Commit()
                self.terminate_open_end_for_full_return(acm_obj_si)
            elif status_code in ['0401', '0808', '0835', '0800']:                    
                sl_settlement_return_cancel.cancel_return_settlement(acm_obj_si)
                trade = acm_obj_si.Trade()
                cancellation_settlement = acm_obj_si.GetTopSettlementInHierarchy()
                
                if status_code == '0401':
                    if acm_obj_si.Status() in ['Released', 'Acknowledged'] and cancellation_settlement.Status() == 'Void':
                        notifier.INFO("Setting settlement %s to Pending Closure" % settlement_number)
                        acm_obj_si.Status('Pending Closure')
                        acm_obj_si.Commit()
                        
                        notifier.INFO("Setting settlement %s to Pending Closure" % cancellation_settlement.Oid())
                        cancellation_settlement.Status('Pending Closure')
                        cancellation_settlement.Commit()
                elif acm_obj_si.Status() in ['Acknowledged', 'Released', 'Authorised']:
                    notifier.INFO("Setting settlement %s to Pending Closure" % acm_obj_si.Oid())
                    acm_obj_si.Status('Pending Closure')
                    acm_obj_si.Commit()
        except Exception as e:
            notifier.ERROR("Error updating settlement status from incomming swift message")
            notifier.DEBUG(str(e), exc_info=1)
    
    def terminate_open_end_for_full_return(self, settlement):
        """
        Terminates 
        """
        trade = settlement.Trade()
        instrument = trade.Instrument()
        if trade.Text1() != 'FULL_RETURN':
            return
        if trade.Type() != 'Closing':
            return
        if instrument.OpenEnd() == "Open End":
            instrument.OpenEnd('Terminated')
            instrument.Commit()



class FClientStatementOfHoldingInProcessing(FSecuritySettlementInProcessingBase.FClientStatementOfHoldingInProcessingBase):
    def __init__(self, bpr):
        super(FClientStatementOfHoldingInProcessing, self).__init__(bpr)

    def process_state_xxx(self):
        """ process bpr state xxx"""
        try:
            notifier.INFO("Processing BPR step xxx")
            notifier.INFO("Completed processing BPR step xxx")
        except Exception as e:
            notifier.ERROR("Error occurred while processing BPR step xxx: %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)
