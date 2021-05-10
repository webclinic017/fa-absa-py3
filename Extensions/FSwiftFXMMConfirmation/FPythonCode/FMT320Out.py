"""----------------------------------------------------------------------------
MODULE:
    FMT320Out

DESCRIPTION:
    This module provides the customizable class for the FMT320 outgoing implementation

CLASS:
    FMT320

VERSION: 3.0.1-0.5.3470
----------------------------------------------------------------------------"""
import MT320
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT320OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with

notifier = FSwiftWriterLogger.FSwiftWriterLogger('FXMMConfOut', 'FFXMMConfirmationOutNotify_Config')

@accepts([acm.FConfirmation, MT320.CTD_ANON, xml.dom.minidom.Document])
class FMT320(FMT320OutBase.FMT320Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT320, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)
    # To override existing mappings use below methods to write your own logic
    """
    amount_to_be_settled_32H
    common_reference_22C
    currency_interest_amount_34E
    currency_principal_amount_32B
    day_count_fraction_14D
    interest_rate_37G
    intermediary_PartyA_56A
    intermediary_PartyA_56D
    intermediary_PartyB_56A
    intermediary_PartyB_56D
    maturity_date_30P
    next_interest_due_date_30X
    partyA_82A
    partyA_82D
    partyB_87A
    partyB_87D
    party_As_role_17R
    receiving_agent_PartyA_57A
    receiving_agent_PartyA_57D
    receiving_agent_PartyB_57A
    receiving_agent_PartyB_57D
    related_reference_21
    senders_reference_20
    terms_and_conditions_77D
    trade_date_30T
    type_of_event_22B
    type_of_operation_22A
    value_date_30V
    get_user_data
    """

    """
    To override the options provided, use below methods to write your own logic:-
    methods:-
    get_partyA_option (Tag-82 options:A/D)
    get_partyB_option (Tag-87 options:A/D)
    get_intermediary_PartyA_option (Tag-56 options:A/D)
    get_delivery_agent_PartyA_option (Tag-53 options:A/D)
    get_receiving_agent_PartyA_option (Tag-57 options:A/D)
    get_intermediary_PartyB_option (Tag-56 options:A/D)
    get_receiving_agent_PartyB_option (Tag-57 options:A/D)


    For example:
    def get_partyA_option(self):
        condition = True
        if condition:
            return 'A'
        else:
            return 'D'

    """


class FMT320MessageHeader(FMT320OutBase.FMT320OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom = None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT320MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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


class FMT320NetworkRules(FMT320OutBase.FMT320OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT320NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)


