"""----------------------------------------------------------------------------
MODULE:
    FMT199Out

DESCRIPTION:
    This module provides the customizable class for the FMT199 outgoing implementation

CLASS:
    FMT199

VERSION: 3.0.0-0.5.3383
----------------------------------------------------------------------------"""
import MT199
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT199OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')

@accepts([acm.FSettlement, MT199.CTD_ANON, xml.dom.minidom.Document])
class FMT199(FMT199OutBase.FMT199Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT199, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic
    """
    narrative_79
    related_reference_21
    transaction_reference_20
    get_user_data
    """


class FMT199MessageHeader(FMT199OutBase.FMT199OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT199MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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



class FMT199NetworkRules(FMT199OutBase.FMT199OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT199NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)
