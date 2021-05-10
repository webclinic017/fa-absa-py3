"""----------------------------------------------------------------------------
MODULE:
    FMT192Out

DESCRIPTION:
    This module provides the customizable class for the FMT192 outgoing implementation

CLASS:
    FMT192

VERSION: 3.0.0-0.5.3383
----------------------------------------------------------------------------"""
import FSwiftWriterLogger
import FMT192OutBase
import acm
import MT192
from FSwiftMLUtils import accepts
import xml.dom.minidom
from FSwiftWriterEngine import validate_with

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')

@accepts([acm.FSettlement, MT192.CTD_ANON, xml.dom.minidom.Document])
class FMT192(FMT192OutBase.FMT192Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FMT192, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic
    """
    mt_and_date_of_original_message_11S
    narrative_description_of_original_message_79
    related_reference_21
    transaction_reference_20
    get_user_data
    """


class FMT192MessageHeader(FMT192OutBase.FMT192OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT192MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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


class FMT192NetworkRules(FMT192OutBase.FMT192OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT192NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)

