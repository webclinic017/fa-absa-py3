"""----------------------------------------------------------------------------
MODULE:
    FSecurityConfirmationInProcessingBase

DESCRIPTION:
    Base class for logic to be executed in each state. User can override/extend
    the default behavior in the FSecurityConfirmationInProcessing class
    derived from this class.

FUNCTIONS:
    process_state_ready():
        Pairing is performed in this state and either the 'Identified'/
        'NotIdentified'/'SecurityTransfer' event is triggered.

    process_state_paired():
        Matching/Partial matching is performed in this state and either the
        'Match'/'NoMatch'/'PartialMatch' event is triggered.

    process_state_partialmatch():
        Partial settlement is handled in this state and the 'Identified' event
        is triggered.

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""

import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('SecSetlConf', 'FSecuritySettlementInNotify_Config')
import FSwiftMLUtils
import FMTPairMatch
import FMTFactory
import ConfirmationProcessFunctions


class FSecurityConfirmationInProcessingBase(object):
    def __init__(self, bpr):
        self.business_process = bpr
        self.theirs = FSwiftMLUtils.create_their_object_from_bpr(self.business_process)

    def get_narrative_business_process(self, acm_object, in_or_out = 'Incoming'):
        """ Get the business process for narrative message"""
        ext_objects = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_object, integration_type=in_or_out, msg_typ = 'MT399',
            all_records=True)
        return ext_objects if ext_objects else None


    def process_state_ready(self):
        """ process bpr state ready"""
        try:
            notifier.INFO("Processing BPR step Ready")

            conf_obj = None
            if ConfirmationProcessFunctions.IsCancellation(self.theirs):
                ConfirmationProcessFunctions.process_cancellation(self.theirs, self.business_process)
                return

            if ConfirmationProcessFunctions.IsAmendment(self.theirs):
                conf_obj = ConfirmationProcessFunctions.process_amendment(self.theirs, self.business_process)

            if conf_obj is None:
                try:
                    notifier.DEBUG("Trying to pair incoming message with an object in the database")
                    conf_obj = FMTPairMatch.get_pairing_object(self.theirs)
                except Exception as e:
                    notifier.ERROR("Exception occurred in get_pairing_object : %s"%str(e))
                    notifier.DEBUG(str(e), exc_info=1)

            # Check if there is already an BPR attached to the acm object.
            # This happens if back to back swift message are fed to AMB.
            if conf_obj and FSwiftMLUtils.get_business_process(conf_obj) is None:
                FMTPairMatch.do_linking(self.business_process, conf_obj, self.theirs.swift_data)

            elif conf_obj and self.get_narrative_business_process(conf_obj) is not None:
                FMTPairMatch.do_linking(self.business_process, conf_obj, self.theirs.swift_data)
            else:
                notifier.INFO('BPR %d External object %d : Triggering event NotIdentified on State %s. %s --(NotIdentified)--> %s'%(self.business_process.Oid(), self.business_process.Subject().Oid(), self.business_process.CurrentStep().State().Name(), \
                                    self.business_process.CurrentStep().State().Name(), self.business_process.CurrentStep().TargetState('NotIdentified').Name()))
                FSwiftMLUtils.trigger_event(self.business_process, 'NotIdentified', self.theirs.swift_data)

            notifier.INFO("Completed processing BPR step Ready")
        except Exception as e:
            notifier.ERROR("Error occurred while processing BPR step Ready: %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

    def process_state_paired(self):
        """ process bpr state paired"""
        try:
            '''
            Below code deprecated after using AMBA
            # TODO In case of manual pairing, Pair event is triggered with notes = Manual match.
            # To fix the refreshment issue pairing and matching is performed in PRIME and in ATS we need to bypass this update.
            notes = self.business_process.Diary().GetEntry(self.business_process, self.business_process.CurrentStep()).Notes()
            if notes and notes.First() == 'Manual match':
                return
            '''
            notifier.INFO("Processing BPR step Paired")
            self.perform_matching()
            notifier.INFO("Completed processing BPR step Paired")
        except Exception as e:
            notifier.ERROR("Error occurred while processing BPR step Paired: %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

    def process_state_unpaired(self):
        """ process bpr state unpaired"""
        try:
            notifier.INFO("Processing BPR step Unpaired")

            if ConfirmationProcessFunctions.IsCancellation(self.theirs):
                notifier.INFO('BPR %d External object %d : Triggering event Cancel on State %s. %s --(Cancel)--> %s'%(self.business_process.Oid(), self.business_process.Subject().Oid(), self.business_process.CurrentStep().State().Name(), \
                                    self.business_process.CurrentStep().State().Name(), self.business_process.CurrentStep().TargetState('Cancel').Name()))
                FSwiftMLUtils.trigger_event(self.business_process, 'Cancel', self.theirs.swift_data)

                return

            notifier.INFO("Completed processing BPR step Unpaired")
        except Exception as e:
            notifier.ERROR("Error occurred while processing BPR step Unpaired: %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

    def perform_matching(self):
        """ Perform pairing and trigger match or no match"""
        if ConfirmationProcessFunctions.IsCancellation(self.theirs):
           notifier.INFO('BPR %d External object %d : Triggering event Cancel on State %s. %s --(Cancel)--> %s'%(self.business_process.Oid(), self.business_process.Subject().Oid(), self.business_process.CurrentStep().State().Name(), \
                                    self.business_process.CurrentStep().State().Name(), self.business_process.CurrentStep().TargetState('Cancel').Name()))
           FSwiftMLUtils.trigger_event(self.business_process, 'Cancel', self.theirs.swift_data)

           return

        conf_obj = FSwiftMLUtils.get_acm_object_from_bpr(self.business_process)
        if conf_obj is not None:
            our_swift_message = FSwiftMLUtils.get_outgoing_mt_message(conf_obj)
            ours = FMTFactory.FMTFactory.CreateMTObject(our_swift_message, None, 'OUT')
            ours.AdjustFieldsToCompare(self.theirs, conf_obj)
            self.theirs.SwapFieldsToCompare(True)
            try:
                cmp_success, cmp_result = FMTPairMatch.do_matching(self.theirs, ours)
            except Exception as e:
                notifier.ERROR("Exception occurred in do_matching : %s"%str(e))
                notifier.DEBUG(str(e), exc_info=1)
            ConfirmationProcessFunctions.trigger_match_nomatch(self.theirs, self.business_process, cmp_success, cmp_result)
        else:
            notifier.ERROR("Business process is not attached to any acm object. BPR Oid = %s"%str(self.business_process.Oid()))

