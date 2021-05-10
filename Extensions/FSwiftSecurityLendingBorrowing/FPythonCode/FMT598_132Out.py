"""----------------------------------------------------------------------------
MODULE:
    FMT598_130Out

DESCRIPTION:
    This module provides the customizable class for the FMT598_130 outgoing implementation

CLASS:
    FMT598_130

VERSION: 2.1.0-0.5.2940
----------------------------------------------------------------------------"""
import MT598_132
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT598_132OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with
pkg_name = 'FSwiftSecurityLendingBorrowingOut'
notifier = FSwiftWriterLogger.FSwiftWriterLogger('SBL', pkg_name+ 'Notify_Config')

@accepts([acm.FSettlement, MT598_132.CTD_ANON, xml.dom.minidom.Document])
class FMT598_132(FMT598_132OutBase.FMT598_132Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT598_132, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)
    # To override existing mappings use below methods to write your own logic
    """
    """

class FMT598_132MessageHeader(FMT598_132OutBase.FMT598_132OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom = None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT598_132MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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


class FMT598_132NetworkRules(FMT598_132OutBase.FMT598_132OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom = None):
        super(FMT598_132NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom)
