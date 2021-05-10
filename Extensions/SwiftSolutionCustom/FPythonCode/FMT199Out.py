"""----------------------------------------------------------------------------
MODULE:
    FMT199Out

DESCRIPTION:
    This module provides the customizable class for the FMT199 outgoing implementation

CLASS:
    FMT199

VERSION: 3.0.0-0.5.3383
----------------------------------------------------------------------------"""
import MT199
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT199OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with
from FFreeFormatUtils import *
import FSwiftWriterUtils
import FSwiftMLUtils
from FCashOutUtils import *

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')


@accepts([acm.FSettlement, MT199.CTD_ANON, xml.dom.minidom.Document])
class FMT199(FMT199OutBase.FMT199Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT199, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic
    """
    narrative_79
    related_reference_21
    transaction_reference_20
    get_user_data
    """

    # formatter
    def _format_transaction_reference_20(self, val):
        seqnbr = val.get('seqnbr')
        seq_ref = val.get('seq_ref')
        if seqnbr and seq_ref:
            message_version = str(get_message_version_number(self.acm_obj, is_free_text_msg=False))
            val = '%s1-%s-%s' % (str(seq_ref), str(seqnbr), str(message_version))
        return val

    # getter
    def related_reference_21(self):
        """ Returns related settlement number as string. """
        # msg_typ = get_corresponding_mt_type_of_canc_paygood(self.acm_obj, self.swift_message_type, 'paygood')
        msg_typ = self.child_mt_type[2:]
        if self.use_operations_xml:
            related_ref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                   ['SWIFT', 'YOUR_REFERENCE'],
                                                                   ignore_absense=True
                                                                   )
        else:
            related_ref = "%s-%s-%s" % (
                str(get_settlement_reference_prefix()),
                str(self.acm_obj.Oid()),
                str(get_message_version_number(self.acm_obj))
            )
        return related_ref


class FMT199MessageHeader(FMT199OutBase.FMT199OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT199MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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
    def message_user_reference(self):
        """
        MUR is sent in the format FAS-SEQNBR of settlement-VersionID
        """
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seqref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            seqnbr = get_sequence_number(self.acm_obj)
            seqref = get_settlement_reference_prefix()
        return "{108:%s1-%s-%s}" % (
            seqref, seqnbr, get_message_version_number(self.acm_obj, is_free_text_msg=False)
        )

    def receiver_logical_terminal_address(self):
        """
        LT code is hardcoded as X for sender
        """
        receivers_bic = ''
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'RECEIVER_BIC'])
        else:
            receivers_bic = get_receivers_bic(self.acm_obj)

        if self.acm_obj.Currency().Name() == 'ZAR':
            receivers_bic = self.get_counterparty_correspondent_address()

        if self.acm_obj.MTMessages() == '199':
            receivers_bic = self.acm_obj.CounterpartyAccountRef().Bic().Alias()

        terminal_address = self.logical_terminal_address(receivers_bic, "X")
        return terminal_address

    def get_counterparty_correspondent_address(self):
        """
        Gets Correspondent BIC address
        """
        counterparty_account = self.acm_obj.CounterpartyAccountRef()
        if counterparty_account:
            if counterparty_account.Bic2():
                return counterparty_account.Bic2().Alias()
            elif counterparty_account.Bic():
                return counterparty_account.Bic().Alias()
            else:
                raise ValueError('No BIC specified on account')

        raise ValueError('No account specified for Settlement')


class FMT199NetworkRules(FMT199OutBase.FMT199OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT199NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)
