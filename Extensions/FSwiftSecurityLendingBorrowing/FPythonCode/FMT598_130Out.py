"""----------------------------------------------------------------------------
MODULE:
    FMT598_130Out

DESCRIPTION:
    This module provides the customizable class for the FMT598_130 outgoing implementation

CLASS:
    FMT598_130

VERSION: 2.1.0-0.5.2940
----------------------------------------------------------------------------"""
import MT598_130
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT598_130OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with
pkg_name = 'FSwiftSecurityLendingBorrowingOut'
notifier = FSwiftWriterLogger.FSwiftWriterLogger('SBL', pkg_name+ 'Notify_Config')

@accepts([acm.FSettlement, MT598_130.CTD_ANON, xml.dom.minidom.Document])
class FMT598_130(FMT598_130OutBase.FMT598_130Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT598_130, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)
    # To override existing mappings use below methods to write your own logic
    """
    """

class FMT598_130MessageHeader(FMT598_130OutBase.FMT598_130OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom = None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT598_130MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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


class FMT598_130NetworkRules(FMT598_130OutBase.FMT598_130OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom = None):
        super(FMT598_130NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom)

