"""----------------------------------------------------------------------------
MODULE:
    FMT542Out

DESCRIPTION:
    This module provides the customizable class for the FMT542 outgoing implementation

CLASS:
    FMT542

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
import MT542
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT542OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with

notifier = FSwiftWriterLogger.FSwiftWriterLogger('SecSetOut', 'FSecuritySettlementOutNotify_Config')


@accepts([acm.FSettlement, MT542.CTD_ANON, xml.dom.minidom.Document])
class FMT542(FMT542OutBase.FMT542Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT542, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic
    """
    account_97A
    date_time_98A
    function_of_message_23G
    identification_of_financial_ins_35B
    indicator_22F
    linkages_20C_16R
    party_safekeeping_account_97A
    place_of_safekeeping_94F
    quantity_of_instrument_36B
    senders_message_reference_20C
    settlement_party_95C
    settlement_party_95P
    settlement_party_95Q
    settlement_party_95R
    get_user_data
    """

    """
    To override the options provided, use below methods to write your own logic:-
    methods:-
    get_settlement_datetime_98_option (options:A/C/E)
    get_account_97_option (options:A/B/E)
    get_party_95_option (options:C/L/P/Q/R/S)
    get_party_safekeeping_97_option (options:A/B)

    For example:
    def get_party_95_option(self):
        condition = True
        if condition:
            return 'P'
        else:
            return 'C'
    """


class FMT542MessageHeader(FMT542OutBase.FMT542OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT542MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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

class FMT542NetworkRules(FMT542OutBase.FMT542OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom = None):
        super(FMT542NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom)

