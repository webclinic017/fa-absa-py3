"""----------------------------------------------------------------------------
MODULE:
    FMT518Out

DESCRIPTION:
    This module provides the customizable class for the FMT518 outgoing implementation

CLASS:
    FMT518

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
import MT518
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT518OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with

notifier = FSwiftWriterLogger.FSwiftWriterLogger('SecSetOut', 'FSecuritySettlementOutNotify_Config')

@accepts([acm.FConfirmation, MT518.CTD_ANON, xml.dom.minidom.Document])
class FMT518(FMT518OutBase.FMT518Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT518, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic
    """
    settlement_indicator_22F
    transaction_type_22F
    quantity_of_instrument_36B
    date_time_98A
    settlement_party_95P
    settlement_party_95R
    settlement_party_9C
    settlement_party_95Q
    settlement_party_95L
    party_safekeeping_account_97A
    indicator_22H
    identification_of_financial_ins_35B
    linkages_20C_16R
    senders_message_reference_20C
    amount_19A
    flag_17B
    deal_price_90A
    deal_price_90B
	function_of_message_23G
    """

    """
    To override the options provided, use below methods to write your own logic:-
    methods:-
    get_acquirer_party_option  (options:P/Q/L)  default:P
    get_counter_party_option   (options:P/Q/L)  default:P
    get_party_95_option (options:C/L/P/Q/R) default:P
    get_party_safekeeping_97_option (options:A/B) default:A
    get_settlement_datetime_98_option (option:A/B/C) default:A
    get_deal_price_90_option (option:A/B) default:A

    For example:
    def get_party_95_option(self):
        condition = True
        if condition:
            return 'P'
        else:
            return 'Q'
    """


class FMT518MessageHeader(FMT518OutBase.FMT518OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom = None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT518MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic

    """
    message_type
    sender_logical_terminal_address
    receiver_logical_terminal_address
    logical_terminal_address
    input_or_output
    message_user_reference
    """

class FMT518NetworkRules(FMT518OutBase.FMT518OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom = None):
        super(FMT518NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom)


