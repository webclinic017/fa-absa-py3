"""----------------------------------------------------------------------------
MODULE:
    FFreeFormatOutBase

DESCRIPTION:
    A module for common functions used across free format messages out base files

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftWriterUtils
from FFreeFormatUtils import *
from FCommonGroupOutBase import FCommonGroupOutBase


class FFreeFormatOutBase(FCommonGroupOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FFreeFormatOutBase, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # getter
    def transaction_reference_20(self):
        """ Returns a dictionary as {'seqnbr': <value>, 'seq_ref': <value>} """
        values_dict = {}
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seq_ref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            seqnbr = get_sequence_number(self.acm_obj)
            seq_ref = get_settlement_reference_prefix()
        values_dict['seqnbr'] = seqnbr
        values_dict['seq_ref'] = seq_ref
        return values_dict

    # formatter
    def _format_transaction_reference_20(self, val):
        seqnbr = val.get('seqnbr')
        seq_ref = val.get('seq_ref')
        if seqnbr and seq_ref:
            message_version = str(get_message_version_number(self.acm_obj, is_free_text_msg=False))
            val = '%s-%s-%s-%s' % (
            str(seq_ref), str(seqnbr), str(message_version), str(self.swift_message_type[2:5]))
        return val

    # getter
    def related_reference_21(self):
        """ Returns related settlement number as string. """
        #msg_typ = get_corresponding_mt_type_of_canc_paygood(self.acm_obj, self.swift_message_type, 'paygood')
        msg_typ = self.child_mt_type[2:]
        if self.use_operations_xml:
            related_ref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                   ['SWIFT', 'YOUR_REFERENCE'], ignore_absense=True)
        else:
            related_ref = "%s-%s-%s-%s" % (str(get_settlement_reference_prefix()), str(self.acm_obj.Oid()),
                                        str(get_message_version_number(self.acm_obj)), str(msg_typ)[0:3])
        return related_ref

    # formatter
    def _format_related_reference_21(self, val):
        return val

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
            related_ref = "%s-%s-%s" % (str(get_settlement_reference_prefix()), str(self.acm_obj.Oid()),
                                        str(get_message_version_number(self.acm_obj)))
            narrative = """ TODAY WE HAVE SENT YOU A PAYMENT INSTRUCTION UNDER REFERENCE {0} FOR {1} {2} WITH VALUE DATE {3}.
             WITH REGARDS TO THIS PAYMENT WE HEREBY INSTRUCT YOU TO ARRANGE A BACKVALUATION FROM VALUE DATE {3} TO VALUE DATE {4}.""".format(
                related_ref, ccy, amount, value_date, original_value_day)
            values_dict['narrative'] = narrative
        else:
            values_dict['narrative'] = get_narrative_description(self.acm_obj, self.swift_message_type)
        return values_dict

    # formatter
    def _format_narrative_79(self, val):
        narrative = val.get('narrative')
        sep = val.get('sep')
        if self.use_operations_xml:
            val = narrative.split(sep)
            val = FSwiftWriterUtils.allocate_space_for_n_lines(35, val)
        else:
            lines = FSwiftWriterUtils.split_text_on_character_limit(narrative, 50)
            val = FSwiftWriterUtils.allocate_space_for_n_lines(35, lines)
        return str(val)

