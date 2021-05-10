"""----------------------------------------------------------------------------
MODULE:
    FMT306Out

DESCRIPTION:
    This module provides the customizable class for the FMT306 outgoing implementation

CLASS:
    FMT306

VERSION: 3.0.1-0.5.3470
----------------------------------------------------------------------------"""

import MT306
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT306OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with

notifier = FSwiftWriterLogger.FSwiftWriterLogger('FXMMConfOut', 'FFXMMConfirmationOutNotify_Config')

@accepts([acm.FConfirmation, MT306.CTD_ANON, xml.dom.minidom.Document])
class FMT306(FMT306OutBase.FMT306Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT306, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below tag_name methods to write your own logic
    """
    agreement_77H
    barrier_indicator_17A
    barrier_level_37J
    barrier_window_location_and_time_for_end_date_29K
    barrier_window_location_and_time_for_start_date_29J
    barrier_window_start_date_end_date_details_30G
    buy_sell_indicator_17V
    calculation_agent_84A
    calculation_agent_84B
    calculation_agent_84D
    calculation_agent_84J
    call_currency_and_amount_33B
    common_reference_22C
    contract_number_party_A_21N
    earliest_exercise_date_30P
    expiration_date_30X
    expiration_location_time_29E
    expiration_style_12E
    final_settlement_date_30F
    lower_barrier_level_37L
    non_deliverable_indicator_17F
    option_style_12F
    partyA_82A
    partyA_82D
    partyB_87A
    partyB_87D
    payout_currency_amount_33E
    premium_currency_and_amount_34B
    premium_payment_date_30V
    put_currency_and_amount_32B
    receiving_agent_57A
    receiving_agent_57D
    receiving_agent_seq_e_57J
    related_reference_21
    scope_of_operation_94A
    senders_reference_20
    sequence_g_currency_pair_32Q
    sequence_g_lower_trigger_level_37P
    sequence_g_trigger_level_37U
    sequence_g_type_of_trigger_22J
    sequence_h_settlement_rate_source_14S
    settlement_currency_32E
    settlement_type_26F
    strike_price_36
    trade_date_30T
    type_event_22K
    type_of_barrier_22G
    type_of_operation_22A
    get_user_data
    """

    """
    To override the options provided, use below methods to write your own logic:-
    methods:-
    get_partyA_option (Tag-82 options:A/D)
    get_partyB_option (Tag-87 options:A/D)
    get_calculation_agent_option (Tag-84 options:A/B/D/J)
    get_receiving_agent_option (Tag-57 options:A/D)
    get_receiving_agent_seq_e_option (Tag-57 options:J)

    For example:
    def get_partyA_option(self):
        condition = True
        if condition:
            return 'A'
        else:
            return 'D'

            """



class FMT306MessageHeader(FMT306OutBase.FMT306OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT306MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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


class FMT306NetworkRules(FMT306OutBase.FMT306OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT306NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)




