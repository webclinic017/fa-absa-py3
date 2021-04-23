"""----------------------------------------------------------------------------
MODULE:
    FSwiftSecurityLendingBorrowingOutProcessingBase

DESCRIPTION:
    Base class for logic to be executed in each state. User can override/extend
    the default behavior in FSecuritySettlementOutProcessingBase class derived from this
    class.

FUNCTIONS:
    process_state_ready():

VERSION: 2.1.1-0.5.2995

RESTRICTIONS/LIMITATIONS:
    1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
    2. This module is not customizable.
    3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import os
import acm
import datetime
import xml.dom.minidom as dom
import FSwiftWriterLogger
import FSwiftML
from FSwiftWriterEngine import should_use_operations_xml
import FSwiftMLUtils
import FSwiftWriterUtils
import FSwiftWriterHooks
import FSwiftOperationsAPI
from FValidation_core import show_validation_warning
try:
    OperationsDocumentStatus = FSwiftOperationsAPI.GetOperationsDocumentStatusEnum()
    OperationsDocumentType = FSwiftOperationsAPI.GetOperationsDocumentTypeEnum()
except:
    pass

notifier = FSwiftWriterLogger.FSwiftWriterLogger('SBL', 'FSwiftSecurityLendingBorrowingOutNotify_Config')


class FSwiftSecurityLendingBorrowingOutProcessingBase(object):

    def __init__(self, bpr):
        self.business_process = bpr
        self.acm_obj = FSwiftMLUtils.get_acm_object_from_bpr(bpr)
        self._ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object_from_bpr(bpr)
        self.msg_type = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(self._ext_obj)
        self.mt_py_object = None
        self.swift_message = FSwiftMLUtils.get_swift_data_from_bpr(self.business_process)
        self.getter_values = None
        self.fsec_lending_borrowing_out_msg_config = FSwiftMLUtils.Parameters(
            'FSwiftSecurityLendingBorrowingOut_Config')

    def process_state_ready(self):
        """ process bpr state ready"""
        try:
            notifier.DEBUG("{0} Processing State Ready".format(self.msg_type))
            if FSwiftMLUtils.get_acm_version() >= 2016.4:
                ops_doc = FSwiftWriterUtils.CreateOperationsDocument(OperationsDocumentStatus.PENDING_GENERATION,
                                                                     self.msg_type.strip('MT'), 0, "", "",
                                                                     OperationsDocumentType.SWIFT, self.acm_obj)
            else:
                ops_doc = FSwiftWriterUtils.CreateOperationsDocument('Pending generation', self.msg_type.strip('MT'), 0,
                                                                     "", "", 'SWIFT', self.acm_obj)
            ops_doc.Commit()
            client = FSwiftMLUtils.get_parameters_from_bpr_state(self.business_process, 'Ready', 'party')
            self.swift_message, self.mt_py_object, self.attribute_exceptions, self.getter_values = FSwiftWriterUtils.generate_swift_message(
                self.acm_obj, self.msg_type)
            entry = self.business_process.Diary().GetEntry(self.business_process, self.business_process.CurrentStep())
            for key in entry.Parameters():
                self.getter_values[key] = entry.Parameters().At(key)
            entry.Parameters(self.getter_values)
            self.business_process.Diary().PutEntry(self.business_process, self.business_process.CurrentStep(), entry)
            if self.attribute_exceptions:
                external_item = FSwiftMLUtils.FSwiftExternalObject.get_external_object_from_bpr(self.business_process)
                exception_str = FSwiftWriterUtils.exceptions_as_string(self.attribute_exceptions)
                if self.swift_message:
                    FSwiftMLUtils.FSwiftExternalObject.set_external_data(external_item, str(self.swift_message),
                                                                         'swift_data')
                notifier.INFO('%s BPR %d External object %d : Triggering event Fail on State %s. %s --(Fail)--> %s' % (
                self.msg_type, self.business_process.Oid(), self.business_process.Subject().Oid(),
                self.business_process.CurrentStep().State().Name(), \
                self.business_process.CurrentStep().State().Name(),
                self.business_process.CurrentStep().TargetState('Fail').Name()))
                try:
                    self.attribute_exceptions['Error'] = 'Incorrect attribute mapping. View the message for details.'
                    FSwiftMLUtils.trigger_event(self.business_process, 'Fail', self.swift_message,
                                                self.attribute_exceptions)
                except Exception, e:
                    notifier.ERROR("%s Exception in process_state_ready : %s" % (self.msg_type, str(e)))
                    notifier.DEBUG(str(e), exc_info=1)
                notifier.ERROR("{0} Failed to generate SWIFT message".format(self.msg_type))

            elif self.mt_py_object and self.swift_message:
                external_item = FSwiftMLUtils.FSwiftExternalObject.get_external_object_from_bpr(self.business_process)

                FSwiftMLUtils.FSwiftExternalObject.set_external_data(external_item, str(self.swift_message),
                                                                     'swift_data')

                try:
                    swiftml_obj = FSwiftML.FSwiftML()
                    self.mt_py_object = swiftml_obj.swift_to_pyobject(str(self.swift_message))
                    validation_result, validation_failed, brief_result_dict = FSwiftWriterUtils.validate_network_rules(
                        self.msg_type, self.mt_py_object, str(self.swift_message), self.acm_obj)
                    if validation_failed:
                        notifier.INFO(
                            '%s BPR %d External object %d : Triggering event Fail on State %s. %s --(Fail)--> %s' % (
                                self.msg_type,
                                self.business_process.Oid(), self.business_process.Subject().Oid(),
                                self.business_process.CurrentStep().State().Name(), \
                                self.business_process.CurrentStep().State().Name(),
                                self.business_process.CurrentStep().TargetState('Fail').Name()))
                        FSwiftMLUtils.trigger_event(self.business_process, 'Fail', str(self.swift_message),
                                                    param=brief_result_dict)
                        notifier.ERROR("%s Failed to perform network validation." % self.msg_type)
                    else:
                        notifier.INFO(
                            '%s BPR %d External object %d : Triggering event GenerateSWIFT on State %s. %s --(GenerateSWIFT)--> %s' %
                            (self.msg_type, self.business_process.Oid(), self.business_process.Subject().Oid(),
                             self.business_process.CurrentStep().State().Name(),
                             self.business_process.CurrentStep().State().Name(),
                             self.business_process.CurrentStep().TargetState('GenerateSWIFT').Name()))
                        FSwiftMLUtils.trigger_event(self.business_process, 'GenerateSWIFT', str(self.swift_message),
                                                    brief_result_dict)

                except Exception, e:
                    if "Update collision" in str(e):
                        self.business_process.ForceToState("Ready",
                                                           "Reverting due to Update Collision")
                        self.business_process.Commit()
                        raise Exception(str(e))
                    notifier.INFO(
                        '%s BPR %d External object %d : Triggering event Fail on State %s. %s --(Fail)--> %s' % (
                            self.msg_type,
                            self.business_process.Oid(), self.business_process.Subject().Oid(),
                            self.business_process.CurrentStep().State().Name(), \
                            self.business_process.CurrentStep().State().Name(),
                            self.business_process.CurrentStep().TargetState('Fail').Name()))
                    try:
                        error_dict = {'Error': str(e)}
                        FSwiftMLUtils.trigger_event(self.business_process, 'Fail', str(e), error_dict)
                    except Exception, e:
                        notifier.ERROR("%s Exception in process_state_ready : %s" % (self.msg_type, str(e)))
                        notifier.DEBUG(str(e), exc_info=1)
                    notifier.ERROR("%s Failed to perform network validation %s" % (self.msg_type, str(e)))
                    notifier.DEBUG(str(e), exc_info=1)
        except Exception, e:
            if "Update collision" in str(e):
                self.business_process.ForceToState("Ready", "Reverting due to Update Collision")
                self.business_process.Commit()
                raise Exception(str(e))
            try:
                error_dict = {'Error': str(e)}
                FSwiftMLUtils.trigger_event(self.business_process, 'Fail', str(e), error_dict)
            except Exception, e:
                notifier.ERROR("%s Exception in process_state_ready : %s" % (self.msg_type, str(e)))
                notifier.DEBUG(str(e), exc_info=1)

            notifier.ERROR("%s Exception in process_state_ready : %s" % (self.msg_type, str(e)))
            notifier.DEBUG(str(e), exc_info=1)
        notifier.DEBUG("{0} Done Processing State Ready".format(self.msg_type))

    def process_state_swiftmsggenerated(self):
        """ process bpr state swiftmsggenerated"""
        try:
            notifier.DEBUG("{0} Processing State SwiftMsgGenerated".format(self.msg_type))

            self.acm_obj = FSwiftMLUtils.get_acm_object_from_bpr(self.business_process)
            carbon_copy_swift_path = getattr(self.fsec_lending_borrowing_out_msg_config, 'CarbonCopySwiftPath',
                                             r'C:\Sent Swift Messages')
            try:
                if getattr(self.fsec_lending_borrowing_out_msg_config, 'SaveCarbonCopySwift', 'False') == 'True':
                    if os.path.exists(carbon_copy_swift_path):
                        file_name = "Settlement_%d_" % self.acm_obj.Oid() + str(self.msg_type) + ".txt"
                        full_path = os.path.join(carbon_copy_swift_path, file_name)
                        with open(full_path, 'w+') as f:
                            f.write(self.swift_message)
                        notifier.INFO("%s Saved SWIFT message at %s" % (self.msg_type, str(full_path)))
                    else:
                        message = "%s Could not find path %s to save outgoing SWIFT message" % (self.msg_type, str(carbon_copy_swift_path))
                        notifier.ERROR(message)
                        #FSwiftMLUtils.trigger_event(self.business_process, 'Fail', str(e), error_dict)
                        self.process_state_sync_bp()
                            
                external_item = FSwiftMLUtils.FSwiftExternalObject.get_external_object_from_bpr(self.business_process)
                senders_reference = FSwiftMLUtils.get_field_value(self.swift_message, '20')
                #senders_reference = self.swift_message[self.swift_message.find('108:') + 4: self.swift_message.find('}}{')]
                FSwiftMLUtils.FSwiftExternalObject.set_external_reference(external_item, senders_reference)
            except Exception, e:
                notifier.ERROR("%s Exception while saving outgoing SWIFT message : %s" % (self.msg_type, str(e)))
                notifier.DEBUG(str(e), exc_info=1)
                error_dict = {'Error': str(e)}
                FSwiftMLUtils.trigger_event(self.business_process, 'Fail', str(e), error_dict)

            # external_item = FSwiftMLUtils.get_exteral_item_from_bpr(self.business_process)
            # TODO This is temporary arrangement and needs to be taken up in FExternalObject change drive.
            # Choicelist SourceType needs to be populated with AMB_MSG_ID
            try:
                swift_msg_before = self.swift_message
                self.swift_message = FSwiftWriterHooks.message_exit_hook(swift_msg_before)
                if str(self.swift_message) != str(swift_msg_before):
                    notifier.INFO('%s Updated swift message = %s' % (self.msg_type, self.swift_message))
                    FSwiftWriterUtils.validate_outgoing_swift_msg(swift_msg_before, self.swift_message)

                self.swift_message = FSwiftWriterUtils.process_aditional_delimiter(self.swift_message)
                encrypted_swift_message, param_dict = FSwiftWriterUtils.encrypt_message(self.swift_message)
                param_dict["SentDate"] = str(datetime.datetime.now().date())
                pkg_name = FSwiftWriterUtils.get_module_name(self.msg_type)
                config_name = pkg_name + '_Config'
                last_mid = FSwiftWriterUtils.send_swift_message_to_amb(self.msg_type, str(encrypted_swift_message),
                                                                       external_item.Oid(), config_name)
                if last_mid:
                    FSwiftMLUtils.FSwiftExternalObject.set_channel_details(external_item, 'AMB', last_mid)
                    notifier.INFO(
                        '%s BPR %d External object %d : Triggering event Send on State %s. %s --(Send)--> %s' % (
                            self.msg_type,
                            self.business_process.Oid(), self.business_process.Subject().Oid(),
                            self.business_process.CurrentStep().State().Name(),
                            self.business_process.CurrentStep().State().Name(),
                            self.business_process.CurrentStep().TargetState('Send').Name()))

                    FSwiftMLUtils.trigger_event(self.business_process, 'Send',
                                                "Sent over AMB with message id %s" % str(last_mid),
                                                param=param_dict)
            except Exception, e:
                notifier.INFO(
                    '%s BPR %d External object %d : Triggering event SendFail on State %s. %s --(SendFail)--> %s' % (
                        self.msg_type,
                        self.business_process.Oid(), self.business_process.Subject().Oid(),
                        self.business_process.CurrentStep().State().Name(), \
                        self.business_process.CurrentStep().State().Name(),
                        self.business_process.CurrentStep().TargetState('SendFail').Name()))
                try:
                    error_dict = {'Error': str(e)}
                    FSwiftMLUtils.trigger_event(self.business_process, 'SendFail', str(e), error_dict)
                    notifier.ERROR("%s Exception in process_state_swiftmsggenerated : %s" % (self.msg_type, str(e)))
                except Exception, e:
                    notifier.ERROR("%s Exception in trigger_event call from process_state_swiftmsggenerated  : %s" % (
                    self.msg_type, str(e)))
                    notifier.DEBUG(str(e), exc_info=1)
        except Exception, e:
            if "Update collision" in str(e):
                self.business_process.ForceToState("SwiftMsgGenerated", "Reverting due to Update Collision")
                self.business_process.Commit()
                raise Exception(str(e))
            try:
                notifier.INFO('%s BPR %d External object %d : Triggering event Fail on State %s. %s --(Fail)--> %s' % (
                self.msg_type, self.business_process.Oid(), self.business_process.Subject().Oid(),
                self.business_process.CurrentStep().State().Name(), \
                self.business_process.CurrentStep().State().Name(),
                self.business_process.CurrentStep().TargetState('Fail').Name()))
                error_dict = {'Error': str(e)}
                FSwiftMLUtils.trigger_event(self.business_process, 'Fail', str(e), error_dict)
            except Exception, e:
                notifier.ERROR("%s Exception in process_state_swiftmsggenerated : %s" % (self.msg_type, str(e)))
                notifier.DEBUG(str(e), exc_info=1)
            notifier.ERROR("%s Failed to send swift message over AMB %s" % (self.msg_type, str(e)))
            notifier.DEBUG(str(e), exc_info=1)
        notifier.DEBUG("{0} Done Processing State SwiftMsgGenerated".format(self.msg_type))

    def process_state_sync_bp(self):
        print("process_state_sync_bp")
        self.business_process.ForceToState("GenerationFailed")
        self.business_process.Commit()

    def process_state_sent(self):
        """ process bpr state sent"""

        try:
            notifier.DEBUG("{0} Processing State Sent".format(self.msg_type))
            if getattr(self.fsec_lending_borrowing_out_msg_config, 'AutoAcknowledgeMessage', 'False') == 'True':
                FSwiftMLUtils.trigger_event(self.business_process, 'Ack', "Acknowledged")
                acm_obj_si = self.acm_obj.StorageImage()
                acm_obj_si.Status('Acknowledged')
                acm_obj_si.Commit()

                # Process settlemnet cancellation
                if self.msg_type == 'MT598_132':
                    self.handle_cancellation_business_process()

            elif getattr(self.fsec_lending_borrowing_out_msg_config, 'AutoAcknowledgeMessage', 'False') == 'False':
                FSwiftMLUtils.set_document_status_on_acm_object(self.acm_obj, 'SENDING')

        except Exception, e:
            if "Update collision" in str(e):
                self.business_process.ForceToState("Sent", "Reverting due to Update Collision")
                self.business_process.Commit()
                raise Exception(str(e))
        notifier.DEBUG("{0} Done Processing State Sent".format(self.msg_type))

    def handle_cancellation_business_process(self):
        """ process cancellation businessprocess"""
        try:
            cancellation_statechart = acm.FStateChart['FPTSSettlementCancellation']
            business_pro = acm.BusinessProcess.InitializeProcess(self.acm_obj, cancellation_statechart)
            params = {"Security Lending Borrowing BPR ID": self.business_process.Oid()}

            entry = business_pro.Diary().GetEntry(business_pro, business_pro.CurrentStep())
            entry.Parameters(params)
            business_pro.Diary().PutEntry(business_pro, business_pro.CurrentStep(), entry)
            business_pro.Commit()
            
        except Exception as e:
            notifier.ERROR("Exception in handle_cancellation_business_process : %s" % str(e))
    
    def process_state_acknowledged(self):
        try:
            acm_obj_si = self.acm_obj.StorageImage()
            acm_obj_si.Status('Acknowledged')
            acm_obj_si.Commit()
        except Exception as e:
            notifier.ERROR("Exception in process_state_acknowledged : %s" % str(e))
            
    def process_state_sendfailed(self):
        try:
            acm_obj_si = self.acm_obj.StorageImage()
            acm_obj_si.Status('Not Acknowledged')
            acm_obj_si.Commit()
        except Exception as e:
            notifier.ERROR("Exception in process_state_acknowledged : %s" % str(e))
