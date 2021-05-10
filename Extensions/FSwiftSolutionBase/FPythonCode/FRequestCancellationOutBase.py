"""----------------------------------------------------------------------------
MODULE:
    FRequestCancellationOutBase

DESCRIPTION:
    A module for common getter formatter functions used across cancellation out base files

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""

import FSwiftWriterUtils
import FSwiftMLUtils
from FCashOutUtils import *
from FCommonGroupOutBase import FCommonGroupOutBase

class FRequestCancellationOutBase(FCommonGroupOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FRequestCancellationOutBase, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # ------------------ transaction_reference -----------------------
    # getter
    def transaction_reference_20(self):
        """
        Returns a dictionary as {'seqnbr': <value>, 'seq_ref': <value>}
        """
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
            message_version = get_message_version_number(self.acm_obj, is_free_text_msg=True, child_mt_type=self.child_mt_type)
            val = '%s-%s-%s-%s' % (str(seq_ref), str(seqnbr), str(message_version), str(self.swift_message_type[2:5]))
            return val

    # ------------------ related_reference -----------------------

    def _check_condition_set_related_reference_21(self):
        related_settlement = get_related_settlement(self.acm_obj)
        if related_settlement:
            return True
        else:
            return False

    # getter
    def related_reference_21(self):
        """ Returns related settlement number as string."""
        related_ref = ''
        newCancSettl = True
        #msg_typ = get_corresponding_mt_type_of_canc_paygood(self.acm_obj, self.swift_message_type, 'canc')
        related_settlement = get_related_settlement(self.acm_obj)
        # If true, means we are trying to generate cancellation on same settlement.
        # In such case, the purpose is to send cancellation for acked message
        # TODO: cases for sending cancellation for MT202COV case is not handled.
        if self.acm_obj == related_settlement:
            newCancSettl = False
        if related_settlement:
            external_objs = FSwiftWriterUtils.get_external_object_for_acm_object(related_settlement)
            for each_obj in external_objs:
                related_settlement_mt_type = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(each_obj)
                if related_settlement_mt_type == self.child_mt_type:
                    bpr = FSwiftMLUtils.FSwiftExternalObject.get_business_process_from_external_object(each_obj)
                    if related_settlement_mt_type and bpr.CurrentStateName() in ['Acknowledged', 'Sent'] and \
                            ((newCancSettl and str(self.child_mt_type) in related_settlement_mt_type) or (not newCancSettl)):
                        ext_data = FSwiftWriterUtils.get_stored_data_from_ext_obj(each_obj, 'swift_data')
                        if ext_data:
                            related_ref = FSwiftMLUtils.get_field_value(ext_data, '20')
                            return related_ref
        return related_ref

    # formatter
    def _format_related_reference_21(self, val):
        return val

    # ------------------ date of original message -----------------------
    # getter
    def mt_and_date_of_original_message_11S(self):
        """ Returns a dictionary as {'MT_type' = '103', 'value_day': <date of the settlement in '%y%m%d' format>} """
        val_dict = {}
        value_day = get_date_of_original_message(self.acm_obj, self.swift_message_type, child_mt_type=self.child_mt_type)
        original_msg_typ = self.child_mt_type
        original_msg_typ = original_msg_typ[2:5] if original_msg_typ else original_msg_typ
        val_dict['MT_type'] = original_msg_typ
        val_dict['value_day'] = value_day
        return val_dict

    # formatter
    def _format_mt_and_date_of_original_message_11S(self, val):
        mt_message_original = val.get('MT_type')
        value_day = val.get('value_day')
        value_day = FSwiftWriterUtils.format_date(value_day, '%y%m%d')
        val = str(mt_message_original) + '\n' + str(value_day)
        return val

    # getter
    def narrative_description_of_original_message_79(self):
        """
        Returns the narrative description as string
        """
        if self.use_operations_xml:
            description = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                   ['SWIFT', 'NARRATIVE_DESCRIPTION'],
                                                                   ignore_absense=True)
        else:
            description = get_narrative_description(self.acm_obj)
        return description

    # formatter
    def _format_narrative_description_of_original_message_79(self, val):
        lines = FSwiftWriterUtils.split_text_on_character_limit(val, 50)
        val = FSwiftWriterUtils.allocate_space_for_n_lines(35, lines)
        return val

