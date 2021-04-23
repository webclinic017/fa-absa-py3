"""----------------------------------------------------------------------------
MODULE:
    FMT299OutBase

DESCRIPTION:
    This module provides the base class for the FMT299 outgoing implementation

CLASS:
    FMT299Base

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftWriterLogger
import FSwiftWriterMessageHeader
import FSwiftWriterUtils
import MT299
from FCashOutUtils import *
from FSwiftWriterEngine import validate_with, should_use_operations_xml

from FFreeFormatOutBase import FFreeFormatOutBase

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')


class FMT299Base(FFreeFormatOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = 'MT299'
        super(FMT299Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # Implementing it to pass the NotImplementedError
    def _message_sequences(self):
        pass

    # getter transaction_reference_20
    # Moved to FFreeFormatOutBase

    # formatter _format_transaction_reference_20
    # Moved to FFreeFormatOutBase

    # validator
    @validate_with(MT299.MT299_20_Type)
    def _validate_transaction_reference_20(self, val):
        return val

    # setter
    def _set_transaction_reference_20(self, val):
        self.swift_obj.TransactionReferenceNumber = val
        self.swift_obj.TransactionReferenceNumber.swiftTag = "20"

    # getter related_reference_21
    # Moved to FFreeFormatOutBase

    # formatter _format_related_reference_21
    # Moved to FFreeFormatOutBase

    # validator
    @validate_with(MT299.MT299_21_Type)
    def _validate_related_reference_21(self, val):
        return val

    # setter
    def _set_related_reference_21(self, val):
        self.swift_obj.RelatedReference = val
        self.swift_obj.RelatedReference.swiftTag = "21"

    # getter narrative_79
    # Moved to FFreeFormatOutBase

    # formatter _format_narrative_79
    # Moved to FFreeFormatOutBase

    # validator
    @validate_with(MT299.MT299_79_Type)
    def _validate_narrative_79(self, val):
        return val

    # setter
    def _set_narrative_79(self, val):
        self.swift_obj.Narrative = val
        self.swift_obj.Narrative.swiftTag = "79"


class FMT299OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_type = "299"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT' + self.mt_type)

        super(FMT299OutBaseMessageHeader, self).__init__(self.mt_type, self.acm_obj, swift_msg_tags)

    def message_type(self):
        return "299"

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
        '''MUR is sent in the format FAS-SEQNBR of settlement-VersionID'''
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seqref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            seqnbr = get_sequence_number(self.acm_obj)
            seqref = get_settlement_reference_prefix()
        return "{108:%s-%s-%s-%s}" % (seqref, seqnbr, get_message_version_number(self.acm_obj, is_free_text_msg=False), self.mt_type[0:3])


class FMT299OutBaseNetworkRules(object):
    ''' '''

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.acm_obj = acm_obj

