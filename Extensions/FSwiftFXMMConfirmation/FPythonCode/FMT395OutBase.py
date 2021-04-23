"""----------------------------------------------------------------------------
MODULE:
    FMT395OutBase

DESCRIPTION:
    This module provides the base class for the FMT395 outgoing implementation

CLASS:
    FMT395Base

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftWriterMessageHeader
import MT395
from FTreasuryOutBase import FTreasuryOutBase
from FSwiftWriterEngine import validate_with, should_use_operations_xml
import FSwiftWriterLogger

import FSwiftConfirmationUtils

from FFXMMConfirmationOutUtils import *

notifier = FSwiftWriterLogger.FSwiftWriterLogger('FXMMConfOut', 'FFXMMConfirmationOutNotify_Config')

class FMT395Base(FTreasuryOutBase):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = "MT395"
        super(FMT395Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # Implementing it to pass the NotImplementedError
    def _message_sequences(self):
        pass

    # ------------------ transaction_reference -----------------------
    # getter
    def transaction_reference_20(self):
        '''
        Returns a dictionary as {'seqnbr': value, 'seq_ref':value}
        '''
        if self.use_operations_xml:
            val_dict = {}
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['CONFIRMATION', 'SEQNBR'])
            seq_ref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            val_dict = {}
            seqnbr = self.acm_obj.Oid()
            seq_ref = get_confirmation_reference_prefix()
        val_dict['seqnbr'] = seqnbr
        val_dict['seq_ref'] = seq_ref
        if seqnbr and seq_ref:
            return val_dict

    # formatter
    def _format_transaction_reference_20(self, val):
        seqnbr = val.get('seqnbr')
        seq_ref = val.get('seq_ref')
        if seqnbr and seq_ref:
            val = '%s-%s-%s' % (seq_ref, seqnbr, get_message_version_number(self.acm_obj))
            return str(val)

    # validator

    @validate_with(MT395.MT395_20_Type)
    def _validate_transaction_reference_20(self, val):
        validate_slash_and_double_slash(val, "Transaction Reference")  # val.value()
        return val

    # setter
    def _set_transaction_reference_20(self, val):
        self.swift_obj.TransactionReferenceNumber = val
        self.swift_obj.TransactionReferenceNumber.swiftTag = "20"

    # ------------------ related_reference -----------------------
    # getter
    def related_reference_21(self):
        '''
        Returns 'related_reference' as string
        '''
        if self.use_operations_xml:
            related_ref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                   ['SWIFT', 'RELATED_REF'],
                                                                   ignore_absense=True)
        else:
            related_ref = GetRelatedRef(self.acm_obj)
        return related_ref

    # formatter
    def _format_related_reference_21(self, val):
        return val

    # validator
    @validate_with(MT395.MT395_21_Type)
    def _validate_related_reference_21(self, val):
        validate_slash_and_double_slash(val, "Related Reference")  # val.value()
        return val

    def _check_condition_set_related_reference_21(self):
        return True

    # setter
    def _set_related_reference_21(self, val):
        self.swift_obj.RelatedReference = val
        self.swift_obj.RelatedReference.swiftTag = "21"

    # ------------------ queries -----------------------
    # getter
    def queries_75(self):
        '''
        If self.use_operations_xml == True:   Returns dictionary as {'queries': value,'newline': value}
        If self.use_operations_xml == False:   Returns dictionary as {'queries': value}
        '''
        if self.use_operations_xml:
            val_dict = {}
            queries = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'QUERIES'])
            newline = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'NARRATIVE_SEPARATOR'], ignore_absense=True)
            val_dict['queries'] = queries
            val_dict['newline'] = newline
        else:
            val_dict = {}
            queries = get_queries(self.acm_obj)
            val_dict['queries'] = queries
            return val_dict

    # formatter
    def _format_queries_75(self, val):
        queries = val.get('queries')
        newline = val.get('newline')
        if queries:
            if newline:
                val = queries.replace(newline, '\n')
            else:
                queries_list = FSwiftWriterUtils.split_text_on_character_limit(queries, 35)
                val = FSwiftWriterUtils.allocate_space_for_n_lines(6, queries_list)
            return str(val)

    # validator
    @validate_with(MT395.MT395_75_Type)
    def _validate_queries_75(self, val):
        ''' TODO # Currently we are not handling the fields which have tag(s) in its value (ie, :TAG:VALUE as its content). We will be adding this support soon.'''
        from pyxb.exceptions_ import ValidationError
        if val:
            lines = val.split('\n')  # val.value()
            for line in lines:
                if line and line.startswith(':'):
                    raise ValidationError(message="Queries field cannot contain colon(:) at the beginning of any line")
        return val

    # setter
    def _set_queries_75(self, val):
        self.swift_obj.Queries = val
        self.swift_obj.Queries.swiftTag = "75"

    # ------------------ narrative -----------------------
    # getter
    def narrative_77A(self):
        '''
        If self.use_operations_xml == True:   Returns dictionary as {'narrative': value,'newline': value}
        If self.use_operations_xml == False:   Returns dictionary as {'narrative': value}
        '''
        val_dict = {}
        if self.use_operations_xml:
            narrative = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'NARRATIVE'],
                                                                 ignore_absense=True)
            newline = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'NARRATIVE_SEPARATOR'], ignore_absense=True)
            val_dict['narrative'] = narrative
            val_dict['newline'] = newline
        else:
            narrative = get_narrative()
            val_dict['narrative'] = narrative
            return val_dict

    # formatter
    def _format_narrative_77A(self, val):
        narrative = val.get('narrative')
        newline = val.get('newline')
        if narrative:
            if newline:
                val = narrative.replace(newline, '\n')
            else:
                narrative_list = FSwiftWriterUtils.split_text_on_character_limit(narrative, 35)
                val = FSwiftWriterUtils.allocate_space_for_n_lines(20, narrative_list)
            return str(val)

    # validator
    @validate_with(MT395.MT395_77A_Type)
    def _validate_narrative_77A(self, val):
        return val

    # setter
    def _set_narrative_77A(self, val):
        self.swift_obj.Narrative = val
        self.swift_obj.Narrative.swiftTag = "77A"

    # ------------------ mt_and_date_of_original_message -----------------------
    # setter
    def _set_OPTION_mt_and_date_of_original_message(self):
        sender_or_receiver = is_sender_or_receiver(self.acm_obj)
        if sender_or_receiver == "Sender":
            return 'mt_and_date_of_original_message_11S'
        elif sender_or_receiver == "Receiver":
            return 'mt_and_date_of_original_message_11R'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(sender_or_receiver), 'MTandDateOfOriginalMessage'))
            return 'mt_and_date_of_original_message_11S'  # default

    # getter
    def mt_and_date_of_original_message_11S(self):
        '''
        Returns a dictionary as {'mt_message_original': value, 'trade_date':value}
        '''
        val_dict = {}
        if self.use_operations_xml:
            mt_message_original = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'ORIGINAL_MESSAGE_MT'],
                                                                           ignore_absense=True)
            trade_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TRADE_DATE'],
                                                                  ignore_absense=True)
        else:
            mt_message_original = get_original_message_mt(self.acm_obj)
            trade_date = FSwiftConfirmationUtils.get_trade_date(self.acm_obj)

        val_dict['mt_message_original'] = mt_message_original
        val_dict['trade_date'] = trade_date
        return val_dict

    # formatter
    def _format_mt_and_date_of_original_message_11S(self, val):
        mt_message_original = val.get('mt_message_original')
        trade_date = val.get('trade_date')
        date_format = '%y%m%d'
        if mt_message_original and trade_date:
            val = mt_message_original + '\n' + FSwiftWriterUtils.format_date(trade_date, date_format)
            return str(val)

    # validator
    @validate_with(MT395.MT395_11S_Type)
    def _validate_mt_and_date_of_original_message_11S(self, val):
        validate_mt_and_date_of_original_message(val, "MT And Date Of The OriginalMessage")
        return val

    # setter
    def _setmt_and_date_of_original_message_11S(self, val):
        self.swift_obj.MTAndDateOfTheOriginalMessage_S = val
        self.swift_obj.MTAndDateOfTheOriginalMessage_S.swiftTag = "11S"

    # getter
    def mt_and_date_of_original_message_11R(self):
        '''
        Returns a dictionary as {'mt_message_original': value, 'trade_date':value}
        '''
        val_dict = {}
        if self.use_operations_xml:

            mt_message_original = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'ORIGINAL_MESSAGE_MT'],
                                                                           ignore_absense=True)
            trade_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TRADE_DATE'],
                                                                  ignore_absense=True)
        else:

            mt_message_original = get_original_message_mt(self.acm_obj)
            trade_date = get_trade_date_mt(self.acm_obj)

        val_dict['mt_message_original'] = mt_message_original
        val_dict['trade_date'] = trade_date
        return val_dict

    # formatter
    def _format_mt_and_date_of_original_message_11R(self, val):
        mt_message_original = val.get('mt_message_original')
        trade_date = val.get('trade_date')
        date_format = '%y%m%d'
        if mt_message_original and trade_date:
            val = mt_message_original + '\n' + FSwiftWriterUtils.format_date(trade_date, date_format)
            return str(val)

    # validator
    @validate_with(MT395.MT395_11R_Type)
    def _validate_mt_and_date_of_original_message_11R(self, val):
        return val

    # setter
    def _setmt_and_date_of_original_message_11R(self, val):
        self.swift_obj.MTAndDateOfTheOriginalMessage_R = val
        self.swift_obj.MTAndDateOfTheOriginalMessage_R.swiftTag = "11R"

    # ------------------ narrative_description_of_original_message -----------------------
    # getter

    def narrative_description_of_original_message_79(self):
        '''
              Returns dictionary as {'narrative_desc': value,'newline': value}
        '''
        val_dict = {}
        if self.use_operations_xml:
            narrative_desc = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'NARRATIVE_DESCRIPTION'],
                                                                      ignore_absense=True)
            newline = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'NARRATIVE_SEPARATOR'], ignore_absense=True)

        else:
            narrative_desc = get_narrative_description(self.acm_obj)
            newline = getattr(FSwiftMLUtils.Parameters("FFXMMConfirmationOut_Config"), "Separator", None)
            if not newline:
                newline = getattr(FSwiftMLUtils.Parameters("FSwiftWriterConfig"), "Separator", 'newline')
        val_dict['narrative_desc'] = narrative_desc
        val_dict['newline'] = newline
        return val_dict

    # formatter
    def _format_narrative_description_of_original_message_79(self, val):
        narrative_desc = val.get('narrative_desc')
        newline = val.get('newline')

        if narrative_desc and newline:
            val = narrative_desc.replace(newline, '\n')
        return str(val)

    # validator
    @validate_with(MT395.MT395_79_Type)
    def _validate_narrative_description_of_original_message_79(self, val):
        return val

    # setter
    def _set_narrative_description_of_original_message_79(self, val):
        self.swift_obj.NarrativeDescriptionOfTheOriginalMessage = val
        self.swift_obj.NarrativeDescriptionOfTheOriginalMessage.swiftTag = "79"


class FMT395OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_typ = "395"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT' + self.mt_typ)
        super(FMT395OutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

    def message_type(self):
        return "395"

    def sender_logical_terminal_address(self):
        '''LT code is hardcoded as A for sender'''
        senders_bic = ''
        if self.use_operations_xml:
            senders_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SENDER_BIC'])
        else:
            senders_bic = get_senders_bic(self.acm_obj)
        if not senders_bic:
            raise Exception("SENDER_BIC is a mandatory field for Swift message header")
        terminal_address = self.logical_terminal_address(senders_bic, "A")
        return terminal_address

    def receiver_logical_terminal_address(self):
        '''LT code is hardcoded as X for sender'''
        receivers_bic = ''
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'RECEIVER_BIC'])
        else:
            receivers_bic = get_receivers_bic(self.acm_obj)

        terminal_address = self.logical_terminal_address(receivers_bic, "X")
        return terminal_address

    def logical_terminal_address(self, bic_code, lt_code):
        terminal_address = ""
        branch_code = "XXX"
        if bic_code:
            if len(str(bic_code)) == 8:
                terminal_address = str(bic_code) + lt_code + branch_code
            elif len(str(bic_code)) == 11:
                branch_code = bic_code[8:]
                terminal_address = str(bic_code[:8]) + lt_code + branch_code
            else:
                raise Exception("Invalid BIC <%s>)" % bic_code)
        return terminal_address

    def input_or_output(self):
        return "I"

    def message_user_reference(self):
        '''MUR is sent in the format FAC-SEQNBR of confirmation-VersionID'''
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['CONFIRMATION', 'SEQNBR'])
            seq_ref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])

        else:
            seqnbr = self.acm_obj.Oid()
            seq_ref = get_confirmation_reference_prefix()
        return "{108:%s-%s-%s}" % (seq_ref, seqnbr, get_message_version_number(self.acm_obj))


class FMT395OutBaseNetworkRules(object):
    def __init__(self, swift_message_obj, swift_message, acm_obj):
        self.swift_message_obj = swift_message_obj
        self.acm_obj = acm_obj
        self.swift_message = swift_message

    def network_rule_C1(self):
        ''' Either field 79 or a copy of at least the mandatory fields of the original message must be present (Error code(s): C25).'''
        is_field_79_present = self.swift_message_obj.NarrativeDescriptionOfTheOriginalMessage
        if not is_field_79_present:
            return 'Field 79 or Mandatory fields of original message must be present'
        return ''



