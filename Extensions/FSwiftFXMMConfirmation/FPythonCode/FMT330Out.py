"""----------------------------------------------------------------------------
MODULE:
    FMT330Out

DESCRIPTION:
    This module provides the customizable class for the FMT330 outgoing implementation

CLASS:
    FMT330

VERSION: 3.0.1-0.5.3470
----------------------------------------------------------------------------"""
import MT330
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT330OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with

notifier = FSwiftWriterLogger.FSwiftWriterLogger('FXMMConfOut', 'FFXMMConfirmationOutNotify_Config')

@accepts([acm.FConfirmation, MT330.CTD_ANON, xml.dom.minidom.Document])
class FMT330(FMT330OutBase.FMT330Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        self.acm_obj = acm_obj
        self.swift_obj = swift_obj
        super(FMT330, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic
    """
    beneficiary_institution_PartyA_58A
    beneficiary_institution_PartyA_58D
    beneficiary_institution_PartyB_58A
    beneficiary_institution_PartyB_58D
    common_reference_22C
    currency_and_balance_32B
    day_count_fraction_14D
    interest_rate_37G
    partyA_82A
    partyA_82D
    partyB_87A
    partyB_87D
    party_A_role_17R
    period_of_notice_38A
    principle_amount_to_settle_32H
    receiving_agent_PartyA_57A
    receiving_agent_PartyA_57D
    receiving_agent_PartyB_57A
    receiving_agent_PartyB_57D
    related_reference_21
    senders_reference_20
    terms_and_condition_77D
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
    get_receiving_agent_PartyA_option (Tag-57 options:A/D)
    get_receiving_agent_PartyB_option (Tag-57 options:A/D)


    For example:
    def get_partyA_option(self):
       condition = True
       if condition:
           return 'A'
       else:
           return 'D'

       """

class FMT330MessageHeader(FMT330OutBase.FMT330OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom = None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT330MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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

class FMT330NetworkRules(FMT330OutBase.FMT330OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT330NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)



