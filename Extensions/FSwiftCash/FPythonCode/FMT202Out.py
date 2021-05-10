"""----------------------------------------------------------------------------
MODULE:
    FMT202Out

DESCRIPTION:
    This module provides the customizable class for the FMT202 outgoing implementation

CLASS:
    FMT202

VERSION: 3.0.0-0.5.3383
----------------------------------------------------------------------------"""
import MT202
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT202OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')

@accepts([acm.FSettlement, MT202.CTD_ANON, xml.dom.minidom.Document])
class FMT202(FMT202OutBase.FMT202Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT202, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic
    """
    account_with_institution_57A
    account_with_institution_57D
    beneficiary_institution_58A
    beneficiary_institution_58D
    date_currency_amount_32A
    intermedairy_56A
    intermedairy_56D
    ordering_institution_52A
    ordering_institution_52D
    related_reference_21
    senders_correspondent_53A
    senders_correspondent_53D
    transaction_reference_20
    get_user_data
    """
    """
    To override the options provided, use below methods to write your own logic:-
    methods:- 
    get_ordering_institution_option (Tag-52 options:A/D)
    get_senders_correspondent_option (Tag-53 options:A/D)
    get_intermediary_option (Tag-56 options:A/D)
    get_account_with_institution_option (Tag-57 options:A/D)
    get_beneficiary_institution_option (Tag-58 options:A/D)
    
    For example:
    def get_ordering_institution_option(self):
        condition = True
        if condition:
            return 'A'
        else:
            return 'D'

    """

class FMT202MessageHeader(FMT202OutBase.FMT202OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT202MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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


class FMT202NetworkRules(FMT202OutBase.FMT202OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT202NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)


