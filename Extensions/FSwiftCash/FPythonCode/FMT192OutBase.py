"""----------------------------------------------------------------------------
MODULE:
    FMT192OutBase

DESCRIPTION:
    This module provides the base class for the FMT192 outgoing implementation

CLASS:
    FMT192Base

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftWriterLogger
import FSwiftWriterMessageHeader
import FSwiftWriterUtils
import MT192
from FCashOutUtils import *
from FSwiftWriterEngine import validate_with, should_use_operations_xml

from FRequestCancellationOutBase import FRequestCancellationOutBase

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')


class FMT192Base(FRequestCancellationOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = 'MT192'
        super(FMT192Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # Implementing it to pass the NotImplementedError
    def _message_sequences(self):
        pass

        # ------------------ transaction_reference -----------------------
        # getter transaction_reference_20

    # Moved to FRequestCancellationOutBase

    # formatter _format_transaction_reference_20
    # Moved to FRequestCancellationOutBase

    # validator
    @validate_with(MT192.MT192_20_Type)
    def _validate_transaction_reference_20(self, val):
        return val

    # setter
    def _set_transaction_reference_20(self, val):
        self.swift_obj.TransactionReferenceNumber = val
        self.swift_obj.TransactionReferenceNumber.swiftTag = "20"

        # ------------------ related_reference -----------------------

    # condition _check_condition_set_related_reference_21
    # Moved to FRequestCancellationOutBase

    # getter related_reference_21
    # Moved to FRequestCancellationOutBase

    # formatter _format_related_reference_21
    # Moved to FRequestCancellationOutBase

    # validator
    @validate_with(MT192.MT192_21_Type)
    def _validate_related_reference_21(self, val):
        return val

    # setter
    def _set_related_reference_21(self, val):
        self.swift_obj.RelatedReference = val
        self.swift_obj.RelatedReference.swiftTag = "21"

    # ------------------ date of original message -----------------------
    # getter mt_and_date_of_original_message_11S
    # Moved to FRequestCancellationOutBase

    # formatter _format_mt_and_date_of_original_message_11S
    # Moved to FRequestCancellationOutBase

    # validator
    @validate_with(MT192.MT192_11S_Type)
    def _validate_mt_and_date_of_original_message_11S(self, val):
        return val

    # setter
    def _set_mt_and_date_of_original_message_11S(self, val):
        self.swift_obj.MTAndDateOfTheOriginalMessage = val
        self.swift_obj.MTAndDateOfTheOriginalMessage.swiftTag = "11S"

    # getter narrative_description_of_original_message_79
    # Moved to FRequestCancellationOutBase

    # formatter _format_narrative_description_of_original_message_79
    # Moved to FRequestCancellationOutBase

    # validator
    @validate_with(MT192.MT192_79_Type)
    def _validate_narrative_description_of_original_message_79(self, val):
        return val

    # setter
    def _set_narrative_description_of_original_message_79(self, val):
        self.swift_obj.NarrativeDescriptionOfTheOriginalMessage = val
        self.swift_obj.NarrativeDescriptionOfTheOriginalMessage.swiftTag = "79"


class FMT192OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_type = "192"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT' + self.mt_type)

        super(FMT192OutBaseMessageHeader, self).__init__(self.mt_type, self.acm_obj, swift_msg_tags)

    def message_type(self):
        return "192"

    def sender_logical_terminal_address(self):
        '''LT code is hardcoded as A for sender'''
        terminal_address = ''
        senders_bic = ''
        if self.use_operations_xml:
            senders_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SENDER_BIC'])
        else:
            senders_bic = get_senders_bic(self.acm_obj)
        if not senders_bic:
            raise Exception("SENDER_BIC is a mandatory field for Swift message header")
        terminal_address = self.logical_terminal_address(senders_bic, "A")
        return terminal_address

    def receiver_logical_terminal_address(self):
        '''LT code is hardcoded as X for sender'''
        terminal_address = ''
        receivers_bic = ''
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'RECEIVER_BIC'])
        else:
            receivers_bic = get_receivers_bic(self.acm_obj)
        terminal_address = self.logical_terminal_address(receivers_bic, "X")
        return terminal_address

    def logical_terminal_address(self, bic_code, lt_code):
        terminal_address = ""
        branch_code = "XXX"
        if bic_code:
            if len(str(bic_code)) == 8:
                terminal_address = str(bic_code) + lt_code + branch_code
            elif len(str(bic_code)) == 11:
                branch_code = bic_code[8:]
                terminal_address = str(bic_code[:8]) + lt_code + branch_code
            else:
                raise Exception("Invalid BIC <%s>)" % bic_code)
        return terminal_address

    def input_or_output(self):
        return "I"

    def message_user_reference(self):
        '''MUR is sent in the format FAC-SEQNBR of confirmation-VersionID'''
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seqref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            seqnbr = get_sequence_number(self.acm_obj)
            seqref = get_settlement_reference_prefix()
        return "{108:%s-%s-%s-%s}" % (seqref, seqnbr, get_message_version_number(self.acm_obj, is_free_text_msg=True, child_mt_type=self.child_mt_type), self.mt_type[0:3])


class FMT192OutBaseNetworkRules(object):
    ''' '''

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.acm_obj = acm_obj

    def network_rule_C1(self):
        ''' Either field 79 or a copy of at least the mandatory fields of the original message must be present (Error code(s): C25).'''
        is_field_79_present = self.swift_message_obj.NarrativeDescriptionOfTheOriginalMessage
        if not is_field_79_present and not self.swift_message_obj.SEQUENCE103:
            return 'Field 79 or Mandatory fields of original message must be present'
        if not is_field_79_present and self.swift_message_obj.SEQUENCE103:
            original_message = self.swift_message_obj.SEQUENCE103
            if not original_message.SendersReference or not original_message.BankOperationCode or not original_message.ValueDateCurrencyInterbankSettledAmount or not original_message.DetailsOfCharges:
                return 'Field 79 or Mandatory fields of original message must be present'
        return ''

