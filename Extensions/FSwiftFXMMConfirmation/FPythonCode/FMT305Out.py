"""----------------------------------------------------------------------------
MODULE:
    FMT305Out

DESCRIPTION:
    This module provides the customizable class for the FMT305 outgoing implementation

CLASS:
    FMT305

VERSION: 3.0.1-0.5.3470
----------------------------------------------------------------------------"""

import MT305
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT305OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with

notifier = FSwiftWriterLogger.FSwiftWriterLogger('FXMMConfOut', 'FFXMMConfirmationOutNotify_Config')

@accepts([acm.FConfirmation, MT305.CTD_ANON, xml.dom.minidom.Document])
class FMT305(FMT305OutBase.FMT305Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT305, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below 'tag_name' methods to write your own logic

    """
    code_common_reference_22
    counter_currency_amount_33B
    date_contract_agreed_amended_30
    earliest_exercise_date_31C
    expiry_details_31G
    final_settlement_date_31E
    further_identification_23
    intermediary_56A
    intermediary_56D
    partyA_82A
    partyA_82D
    partyB_87A
    partyB_87D
    premium_payment_34P
    premium_payment_34R
    premium_price_37K
    related_reference_21
    sell_account_with_institution_57A
    sell_account_with_institution_57D
    sender_to_receiver_info_72
    senders_correspondent_53A
    senders_correspondent_53D
    settlement_type_26F
    strike_price_36
    transaction_reference_number_20
    underlying_currency_amount_32B
    get_user_data
    """

    """
    To override the options provided, use below methods to write your own logic:-
    methods:-
    get_partyA_option (Tag-82 options:A/D)
    get_partyB_option (Tag-87 options:A/D)
    get_premium_payment_option (Tag-34 options:R/P)
    get_senders_correspondent_option (Tag-53 options:A/D)
    get_intermediary_option (Tag-56 options:A/D)
    get_account_with_institution_option (Tag-57 options:A/D)

    For example:
    def get_partyA_option(self):
        condition = True
        if condition:
            return 'A'
        else:
            return 'D'

        """

class FMT305MessageHeader(FMT305OutBase.FMT305OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT305MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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


class FMT305NetworkRules(FMT305OutBase.FMT305OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT305NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)



