"""----------------------------------------------------------------------------
MODULE:
    FMT103Out

DESCRIPTION:
    This module provides the customizable class for the FMT103 outgoing implementation

CLASS:
    FMT103

VERSION: 3.0.0-0.5.3383
----------------------------------------------------------------------------"""
import FSwiftWriterLogger
notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')
import FMT103OutBase
import acm
import MT103
from FSwiftMLUtils import accepts
import xml.dom.minidom
from FSwiftWriterEngine import validate_with

@accepts([acm.FSettlement, MT103.CTD_ANON, xml.dom.minidom.Document])
class FMT103(FMT103OutBase.FMT103Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT103, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic

    """
    account_with_institution_57A
    account_with_institution_57C
    account_with_institution_57D
    bank_operation_code_23B
    beneficiary_customer_59A
    beneficiary_customer_59F
    beneficiary_customer_no_option_59
    details_of_charges_71A
    instructed_amount_33B
    instruction_code_23E
    intermediary_institution_56A
    intermediary_institution_56C
    intermediary_institution_56D
    ordering_customer_50A
    ordering_customer_50F
    ordering_customer_50K
    ordering_institution_52A
    ordering_institution_52D
    remittance_information_70
    senders_correspondent_53A
    senders_correspondent_53D
    senders_reference_20
    value_date_32A
    get_user_data

    """

    """
    To override the options provided, use below methods to write your own logic:-
    methods:- 
    get_ordering_customer_option (Tag-50 options:A/F/K)
    get_ordering_institution_option (Tag-52 options:A/D)
    get_senders_correspondent_option (Tag-53 options:A/D)
    get_intermediary_institution_option (Tag-56 options:A/C/D)
    get_account_with_institution_option (Tag-57 options:A/C/D)
    get_beneficiary_customer_option (Tag-59 options:A/NO OPTION/F)

    For example:
    def get_ordering_customer_option(self):
        condition = True
        if condition:
            return 'A'
        else:
            return 'F'

    """


class FMT103MessageHeader(FMT103OutBase.FMT103OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT103MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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


class FMT103NetworkRules(FMT103OutBase.FMT103OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom = None):
        super(FMT103NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom)

