"""----------------------------------------------------------------------------
MODULE:
    FMTx99Out

DESCRIPTION:
    OPEN EXTENSION MODULE
    FMT699 class for user customization.
    User can override the mapping defined in the base class FMT699OutBase.
    This class can be populated using either swift data or an acm object.
    See FMT699OutBase for extracting the values from acm

VERSION: 2.1.1-0.5.2990
----------------------------------------------------------------------------"""


import FMTx99OutBase
import FSwiftWriterLogger


notifier = FSwiftWriterLogger.FSwiftWriterLogger('NarrativeOut', 'FNarrativeOutNotify_Config')


class FMT999(FMTx99OutBase.FMTx99Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        swift_message_type = 'MT999'
        super(FMT999, self).__init__(acm_obj, swift_message_type, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic
    """
    narrative_79
    related_reference_21
    transaction_reference_20
    get_user_data
    """


class FMT999MessageHeader(FMTx99OutBase.FMTx99OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.mt_type = '999'
        super(FMT999MessageHeader, self).__init__(self.acm_obj, self.mt_type, swift_msg_tags)

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



class FMT999NetworkRules(FMTx99OutBase.FMTx99OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT999NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)

