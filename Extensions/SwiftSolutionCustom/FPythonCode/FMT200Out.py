"""----------------------------------------------------------------------------
MODULE:
    FMT200Out

DESCRIPTION:
    This module provides the customizable class for the FMT200 outgoing implementation

CLASS:
    FMT200

VERSION: 3.0.3-0.5.3744
----------------------------------------------------------------------------"""
import MT200
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT200OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with
from FCashOutUtils import *
import FSwiftWriterUtils

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')


@accepts([acm.FSettlement, MT200.CTD_ANON, xml.dom.minidom.Document])
class FMT200(FMT200OutBase.FMT200Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FMT200, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic
    """
    account_with_institution_57A
    account_with_institution_57D
    date_currency_amount_32A
    intermediary_56A
    intermediary_56D
    senders_correspondent_53B
    transaction_reference_20
    get_user_data
    """

    """
    To override the options provided, use below methods to write your own logic:-
    methods:- 
    get_intermediary_option (Tag-56 options:A/D)
    get_account_with_institution_option (Tag-57 options:A/D)

    For example:
    def get_intermediary_option(self):
        condition = True
        if condition:
            return 'A'
        else:
            return 'D'

    """
    # formatter
    def _format_transaction_reference_20(self, val):
        seqnbr = val.get('SEQNBR')
        seq_ref = val.get('SEQREF')
        if seqnbr and seq_ref:
            val = '%s-%s-%s' % (str(seq_ref), str(seqnbr), str(get_message_version_number(self.acm_obj)))
            return val


class FMT200MessageHeader(FMT200OutBase.FMT200OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT200MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic

    """
    application_id
    service_id
    sender_logical_terminal_address
    session_number
    sequence_number
    input_or_output
    message_priority
    message_type
    receiver_logical_terminal_address
    delivery_monitoring
    non_delivery_notification_period
    service_identifier
    banking_priority_code
    message_user_reference
    validation_flag
    """
    def message_user_reference(self):
        '''MUR is sent in the format FAC-SEQNBR of confirmation-VersionID'''
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seqref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            seqnbr = self.acm_obj.Oid()
            seqref = get_settlement_reference_prefix()
        return "{108:%s-%s-%s}" % (seqref, seqnbr, get_message_version_number(self.acm_obj))


class FMT200NetworkRules(FMT200OutBase.FMT200OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT200NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)

