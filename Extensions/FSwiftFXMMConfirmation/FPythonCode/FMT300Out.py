"""----------------------------------------------------------------------------
MODULE:
    FMT300Out

DESCRIPTION:
    This module provides the customizable class for the FMT300 outgoing implementation

CLASS:
    FMT300

VERSION: 3.0.1-0.5.3470
----------------------------------------------------------------------------"""

import MT300
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT300OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with

notifier = FSwiftWriterLogger.FSwiftWriterLogger('FXMMConfOut', 'FFXMMConfirmationOutNotify_Config')

@accepts([acm.FConfirmation, MT300.CTD_ANON, xml.dom.minidom.Document])
class FMT300(FMT300OutBase.FMT300Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FMT300, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below 'tag_name' methods to write your own logic

    """
    block_trade_indicator_17T
    buy_delivery_agent_53A
    buy_delivery_agent_53D
    buy_delivery_agent_53J
    buy_intermediary_56A
    buy_intermediary_56D
    buy_receiving_agent_57A
    buy_receiving_agent_57D
    common_reference_22C
    counterpartys_reference_26H
    currency_amount_bought_32B
    currency_amount_sold_33B
    exchange_rate_36
    partyA_82A
    partyA_82D
    partyB_87A
    partyB_87D
    related_reference_21
    scope_of_operation_94A
    sell_beneficiary_institution_58A
    sell_beneficiary_institution_58D
    sell_beneficiary_institution_58J
    sell_delivery_agent_53A
    sell_delivery_agent_53D
    sell_delivery_agent_53J
    sell_intermediary_56A
    sell_intermediary_56D
    sell_receiving_agent_57A
    sell_receiving_agent_57D
    senders_reference_20
    split_settlement_indicator_17U
    terms_and_conditions_77D
    trade_date_30T
    type_of_operation_22A
    value_date_30V
    get_user_data
    """

    """
    To override the options provided, use below methods to write your own logic:-
    methods:-
     get_partyA_option (Tag-82 options:A/D)
     get_partyB_option (Tag-87 options:A/D)
     get_buy_delivery_agent_option (Tag-53 options:A/D/J)
     get_buy_intermediary_option (Tag-56 options:A/D)
     get_buy_receiving_agent_option (Tag-57 options:A/D)
     get_sell_delivery_agent_option (Tag-53 options:A/D/J)
     get_sell_intermediary_option (Tag-56 options:A/D)
     get_sell_receiving_agent_option (Tag-57 options:A/D)
     get_sell_beneficiary_institution_option(Tag-58 options:A/D/J)


    For example:
    def get_partyA_option(self):
        condition = True
        if condition:
            return 'A'
        else:
            return 'D'

    """




class FMT300MessageHeader(FMT300OutBase.FMT300OutBaseMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom = None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT300MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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

class FMT300NetworkRules(FMT300OutBase.FMT300OutBaseNetworkRules):
    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT300NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)




