"""----------------------------------------------------------------------------
MODULE:
    FMT299Out

DESCRIPTION:
    This module provides the customizable class for the FMT299 outgoing implementation

CLASS:
    FMT299

VERSION: 3.0.0-0.5.3383
----------------------------------------------------------------------------"""
import MT299
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT299OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with
import FSwiftWriterUtils
from FFreeFormatUtils import *

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')


@accepts([acm.FSettlement, MT299.CTD_ANON, xml.dom.minidom.Document])
class FMT299(FMT299OutBase.FMT299Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom = None):
        super(FMT299, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

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
            val = '%s2-%s-%s' % (str(seq_ref), str(seqnbr), str(message_version))
        return val

    # getter
    def related_reference_21(self):
        """ Returns related settlement number as string. """
        # msg_typ = get_corresponding_mt_type_of_canc_paygood(self.acm_obj, self.swift_message_type, 'paygood')
        msg_typ = self.child_mt_type[2:]
        if self.use_operations_xml:
            related_ref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                   ['SWIFT', 'YOUR_REFERENCE'], ignore_absense=True)
        else:
            related_ref = "%s%s-%s-%s" % (
                str(get_settlement_reference_prefix()),
                str(self.get_cov_indicator_for_reference()),
                str(self.acm_obj.Oid()),
                str(get_message_version_number(self.acm_obj)))
        return related_ref

    # getter
    def narrative_79(self):
        """ Returns the narrative description as string """
        values_dict = {}
        if self.use_operations_xml:
            sep = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'NARRATIVE_SEPARATOR'])
            values_dict['sep'] = sep
            ccy = self.acm_obj.Currency().Name()
            amount = str(abs(self.acm_obj.Amount()))
            value_date = self.acm_obj.ValueDay()
            original_value_day = self.acm_obj.Children()[-1].ValueDay()
            related_ref = "%s%s-%s-%s" % (
                str(get_settlement_reference_prefix()),
                str(self.get_cov_indicator_for_reference()),
                str(self.acm_obj.Oid()),
                str(get_message_version_number(self.acm_obj))
            )
            narrative = """ TODAY WE HAVE SENT YOU A PAYMENT INSTRUCTION UNDER REFERENCE {0} FOR {1} {2} WITH VALUE DATE {3}.
                     WITH REGARDS TO THIS PAYMENT WE HEREBY INSTRUCT YOU TO ARRANGE A BACKVALUATION FROM VALUE DATE {3} TO VALUE DATE {4}.""".format(
                related_ref, ccy, amount, value_date, original_value_day)
            values_dict['narrative'] = narrative
        else:
            values_dict['narrative'] = self.get_narrative_description(self.acm_obj, self.swift_message_type)
        return values_dict

    def get_narrative_description(self, settlement, mt_type=None):
        """ Optional field 79 for n92 Settlement.
        :param settlement: settlement object
        :param mt_type: message type
        :return: narrative description
        """
        narrative_description = ''
        if mt_type in ['MT199', 'MT299']:
            ccy = settlement.Currency().Name()
            amount = str(abs(settlement.Amount()))
            value_date = settlement.ValueDay()
            original_value_day = settlement.Children()[-1].ValueDay()
            related_ref = "%s%s-%s-%s" % (
                str(get_settlement_reference_prefix()),
                str(self.get_cov_indicator_for_reference()),
                str(settlement.Oid()),
                str(get_message_version_number(settlement))
            )
            narrative_description = """TODAY WE HAVE SENT YOU A PAYMENT INSTRUCTION UNDER REFERENCE {0} FOR {1} {2} WITH VALUE DATE {3}.WITH REGARDS TO THIS PAYMENT WE HEREBY INSTRUCT YOU TO ARRANGE A BACKVALUATION FROM VALUE DATE {3} TO VALUE DATE {4}.""".format(
                related_ref, ccy, amount, value_date, original_value_day)
        else:
            if is_cancellation(settlement):
                related_settlement = get_related_settlement(settlement)
                narrative_description = 'Settlement Id %s was due to %s' % (
                    related_settlement.Oid(), related_settlement.ValueDay()
                )
            elif is_nak_cancellation(settlement):
                narrative_description = 'Cancelling previous MT%s' % (get_original_message_type(settlement))

        return narrative_description

    def get_cov_indicator_for_reference(self):
        """
        Returns C if related settlement is a COV Method
        """
        indicator = 'C' if self.acm_obj.MTMessages() == '199' else ''
        return indicator


class FMT299MessageHeader(FMT299OutBase.FMT299OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT299MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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
        '''MUR is sent in the format FAS-SEQNBR of settlement-VersionID'''
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seqref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            seqnbr = get_sequence_number(self.acm_obj)
            seqref = get_settlement_reference_prefix()
        return "{108:%s2-%s-%s}" % (
            seqref, seqnbr, get_message_version_number(self.acm_obj, is_free_text_msg=False)
        )


class FMT299NetworkRules(FMT299OutBase.FMT299OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT299NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)
