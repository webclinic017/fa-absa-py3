"""----------------------------------------------------------------------------
MODULE:
    FMT210Out

DESCRIPTION:
    This module provides the customizable class for the FMT210 outgoing implementation

CLASS:
    FMT210

VERSION: 3.0.0-0.5.3383
----------------------------------------------------------------------------"""
import MT210
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT210OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with

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


class FMT210NetworkRules(FMT210OutBase.FMT210OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom = None):
        super(FMT210NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom)




