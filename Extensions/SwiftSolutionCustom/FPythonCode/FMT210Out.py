"""----------------------------------------------------------------------------
MODULE:
    FMT210Out

DESCRIPTION:
    This module provides the customizable class for the FMT210 outgoing implementation

CLASS:
    FMT210

VERSION: 3.0.3-0.5.3744
----------------------------------------------------------------------------"""
import MT210
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT210OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with
from FCashOutUtils import *
import FSwiftWriterUtils

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')


@accepts([acm.FSettlement, MT210.CTD_ANON, xml.dom.minidom.Document])
class FMT210(FMT210OutBase.FMT210Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT210, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic
    """
    account_identification_25
    currency_code_amount_32B
    intermediary_56A
    intermediary_56D
    ordering_customer_50C
    ordering_customer_50F
    ordering_customer_No_Option_50
    ordering_institution_52A
    ordering_institution_52D
    related_reference_21
    transaction_reference_number_20
    value_date_30
    get_user_data

    """

    """
    To override the options provided, use below methods to write your own logic:-
    methods:- 
    get_ordering_customer_option (Tag-50 options:NO OPTION/C/F)
    get_ordering_institution_option (Tag-52 options:A/D)
    get_intermediary_option (Tag-56 options:A/D)

    For example:
    def get_ordering_customer_option(self):
        condition = True
        if condition:
            return 'NO OPTION'
        else:
            return 'C'

    """
    # formatter
    def _format_transaction_reference_number_20(self, trans_ref_dict):
        """Formats the value provided by getter method"""
        seqnbr = trans_ref_dict.get('SEQNBR')
        seq_ref = trans_ref_dict.get('SEQREF')
        if seqnbr and seq_ref:
            trans_ref = '%s-%s-%s' % (
            str(seq_ref), str(seqnbr), str(get_message_version_number(self.acm_obj)))
            return trans_ref


class FMT210MessageHeader(FMT210OutBase.FMT210OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT210MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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
        seqnbr = ''
        seqref = ''
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seqref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            seqnbr = self.acm_obj.Oid()
            seqref = get_settlement_reference_prefix()
        return "{108:%s-%s-%s}" % (seqref, seqnbr, get_message_version_number(self.acm_obj))


class FMT210NetworkRules(FMT210OutBase.FMT210OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom = None):
        super(FMT210NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom)




