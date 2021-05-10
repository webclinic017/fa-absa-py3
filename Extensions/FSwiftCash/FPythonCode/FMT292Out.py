"""----------------------------------------------------------------------------
MODULE:
    FMT292Out

DESCRIPTION:
    This module provides the customizable class for the FMT292 outgoing implementation

CLASS:
    FMT292

VERSION: 3.0.0-0.5.3383
----------------------------------------------------------------------------"""
import MT292
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT292OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')

@accepts([acm.FSettlement, MT292.CTD_ANON, xml.dom.minidom.Document])
class FMT292(FMT292OutBase.FMT292Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT292, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic
    """
    mt_and_date_of_original_message_11S
    narrative_description_of_original_message_79
    related_reference_21
    transaction_reference_20
    get_user_data
    """

class FMT292MessageHeader(FMT292OutBase.FMT292OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT292MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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

class FMT292NetworkRules(FMT292OutBase.FMT292OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT292NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)




