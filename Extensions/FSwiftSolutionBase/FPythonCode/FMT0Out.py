"""----------------------------------------------------------------------------
MODULE:
    FMT0Out

DESCRIPTION:
    A default template for confirmations that do not have any MT type.

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
import FMT0OutBase
import FSwiftWriterLogger
notifier = FSwiftWriterLogger.FSwiftWriterLogger('SwiftWriter', 'FSwiftWriterNotifyConfig')

class FMT0(FMT0OutBase.FMT0Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        self.acm_obj = acm_obj
        self.swift_obj = swift_obj
        super(FMT0, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic
    # As well as a new get_method could be added, value returned by such get_method would be considered in calculating checksum
    """
                'get_codeword_newline',
                'get_narrative_saperator',
                'get_swift_message_type',
                'get_partyA_option',
                'get_partyA_account',
                'get_partyA_bic',
                'get_partyA_name',
                'get_partyA_address',
                'get_partyB_option',
                'get_partyB_account',
                'get_partyB_bic',
                'get_partyB_name',
                'get_partyB_address',
                'get_receiver_bic',
                'get_sender_bic',
                'get_seq_ref',
                'get_network',
                'get_trade_date',
                'get_confirmation_template',
                'get_confirmation_event_name',
                'get_confirmation_reset_oid',
                'get_confirmation_transport',
                'get_confirmation_trade_oid',
                'get_confirmation_cashflow'
    """
