"""----------------------------------------------------------------------------
MODULE:
    FMT304Out

DESCRIPTION:
    This module provides the customizable class for the FMT304 outgoing implementation

CLASS:
    FMT304

VERSION: 3.0.0-0.5.3383
----------------------------------------------------------------------------"""

import MT304
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT304OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')

@accepts([acm.FSettlement, MT304.CTD_ANON, xml.dom.minidom.Document])
class FMT304(FMT304OutBase.FMT304Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT304, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below 'tag_name' methods to write your own logic

    '''
    senders_reference_20
    related_reference_21
    type_of_operation_22A
    scope_of_operation_94A
    open_indicator_17O
    final_close_indicator_17F
    net_settlement_indicator_17N
    fund_83A
    fund_83D
    fund_83J
    fund_manager_82A
    fund_manager_82D
    fund_manager_82J
    executing_broker_87A
    executing_broker_87D
    executing_broker_87J
    trade_date_30T
    value_date_30V
    exchange_rate_36
    currency_amount_bought_32B
    buy_delivery_agent_53A
    buy_delivery_agent_53D
    buy_delivery_agent_53J
    buy_intermediary_56A
    buy_intermediary_56D
    buy_intermediary_56J
    buy_receiving_agent_57A
    buy_receiving_agent_57D
    buy_receiving_agent_57J
    currency_amount_sold_33B
    sell_delivery_agent_53A
    sell_delivery_agent_53D
    sell_delivery_agent_53J
    sell_intermediary_56A
    sell_intermediary_56D
    sell_intermediary_56J
    sell_receiving_agent_57A
    sell_receiving_agent_57D
    sell_receiving_agent_57J
    sell_beneficiary_institution_58A
    sell_beneficiary_institution_58D
    sell_beneficiary_institution_58J
    reference_to_previous_deals_21P
    gain_indicator_17G
    currency_amount_32G
    '''    

    # Custom Methods:
    '''
    def fund_manager(self):
        """ Method to return party name whose role is fund manager """
        return 'party_name'

    def executing_broker(self):
        """ Method to return party name whose role is executing broker """
        return 'party_name'

    '''


class FMT304MessageHeader(FMT304OutBase.FMT304OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT304MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic

    """
    message_type
    sender_logical_terminal_address
    receiver_logical_terminal_address
    logical_terminal_address
    input_or_output
    message_user_reference
    """


class FMT304NetworkRules(FMT304OutBase.FMT304OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT304NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)




