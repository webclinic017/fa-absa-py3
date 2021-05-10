"""----------------------------------------------------------------------------
MODULE:
    FInstitutionTransfersOutBase

DESCRIPTION:
    This module provides the base class for the FInstitutionTransfers outgoing implementation

CLASS:
    FInstitutionTransfersOutBase

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftMLUtils
import FSwiftWriterUtils

from FCashOutUtils import *
from FCashOutBase import FCashOutBase

class FInstitutionTransfersOutBase(FCashOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FInstitutionTransfersOutBase, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    #getter
    def intermediary_56A(self):
        """ Returns dictionary as {'ACCOUNT':<value>, 'BIC':<value>}"""
        if self.use_operations_xml:
            values_dict = {}
            intermediary_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                            ['SWIFT', 'INTERMEDIARY_ACCOUNT'],
                                                                            ignore_absence=True)
            intermediary_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                        ['SWIFT', 'INTERMEDIARY_BIC'])
            values_dict['ACCOUNT'] = intermediary_account
            values_dict['BIC'] = intermediary_bic
            return values_dict
        else:
            return get_counterpartys_intermediary_details(self.acm_obj)

    #formatter
    def _format_intermediary_56A(self, val):
        intermediary_account = val.get('ACCOUNT')
        intermediary_bic = val.get('BIC')
        if intermediary_bic:
            if intermediary_account:
                val = "/" + str(intermediary_account) + "\n" + str(intermediary_bic)
            else:
                val = str(intermediary_bic)
            return val

    # getter
    def transaction_reference_20(self):
        """ Returns a dictionary as {'seqnbr':<value>, 'seq_ref':<value>} """
        values_dict = {}
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seq_ref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            seqnbr = self.acm_obj.Oid()
            seq_ref = get_settlement_reference_prefix()

        values_dict['SEQNBR'] = seqnbr
        values_dict['SEQREF'] = seq_ref
        return values_dict

    # formatter
    def _format_transaction_reference_20(self, val):
        seqnbr = val.get('SEQNBR')
        seq_ref = val.get('SEQREF')
        if seqnbr and seq_ref:
            val = '%s-%s-%s-%s' % (
                str(seq_ref), str(seqnbr), str(get_message_version_number(self.acm_obj)), str(self.swift_message_type[2:5]))
            return val

    # getter
    def date_currency_amount_32A(self):
        """ Returns a dictionary as {'value_date':<value>, 'curr':<value>, 'amount':<value>} """
        values_dict = {}
        if self.use_operations_xml:
            value_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'VALUE_DATE'])
            curr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'CURR'])
            amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                              ['SWIFT', 'INTERBANK_SETTLED_AMOUNT'])
        else:
            value_date = get_value_date(self.acm_obj)
            curr = self.acm_obj.Currency().Name()
            amount = self.acm_obj.Amount()
        values_dict['VALUE_DATE'] = value_date
        values_dict['CURR'] = curr
        values_dict['INTERBANK_SETTLED_AMOUNT'] = amount
        return values_dict

    # formatter
    def _format_date_currency_amount_32A(self, val):
        value_date = val.get('VALUE_DATE')
        curr = val.get('CURR')
        amount = val.get('INTERBANK_SETTLED_AMOUNT')
        date_format = '%y%m%d'
        if value_date and curr and amount:
            amount = apply_currency_precision(curr, abs(float(amount)))
            date = FSwiftWriterUtils.format_date(value_date, date_format)
            date_curr_amount = str(date) + str(curr) + str(FSwiftMLUtils.float_to_swiftmt(str(amount)))
            return date_curr_amount

    # getter account_with_institution_57A
    # Moved to FCashSetttlementOutBase

    # formatter _format_account_with_institution_57A
    # Moved to FCashSetttlementOutBase

