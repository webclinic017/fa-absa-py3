"""----------------------------------------------------------------------------
MODULE:
    FMT210OutBase

DESCRIPTION:
    This module provides the base class for the FMT210 outgoing implementation

CLASS:
    FMT210Base

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftMLUtils
import FSwiftWriterMessageHeader
import MT210
from FCashOutUtils import *
from FInstitutionTransfersOutBase import FInstitutionTransfersOutBase
from FSwiftWriterEngine import validate_with, should_use_operations_xml

import FSwiftWriterLogger
import FSwiftWriterUtils

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')

from ChineseCommercialCode import CCC_simplified_writer, CCC_traditional_writer
CONFIG_PARAM = FSwiftMLUtils.Parameters('FSwiftWriterConfig')

chinese_language_version = getattr(CONFIG_PARAM, 'ChineseLanguageVersion', None)
if chinese_language_version:
    if chinese_language_version == 'Simplified':
        lookup = CCC_simplified_writer
    if chinese_language_version == 'Traditional':
        lookup = CCC_traditional_writer
else:
    lookup = CCC_simplified_writer

class FMT210Base(FInstitutionTransfersOutBase):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = 'MT210'
        super(FMT210Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    def _message_sequences(self):
        """Sets the sequences on the pyxb object for MT210"""
        self.swift_obj.SEQUENCE1 = MT210.MT210_SEQUENCE1()

    # getter
    def transaction_reference_number_20(self):
        '''
        Returns a dictionary with settlement id and settleent reference code as values
        example - {'SEQNBR':settlement id (OID), 'SEQREF':reference code (FAS)}
        '''
        values_dict = {}
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seq_ref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
            values_dict['SEQNBR'] = seqnbr
            values_dict['SEQREF'] = seq_ref
            return values_dict
        else:
            values_dict['SEQNBR'] = self.acm_obj.Oid()
            values_dict['SEQREF'] = get_settlement_reference_prefix()
            return values_dict

    # formatter
    def _format_transaction_reference_number_20(self, trans_ref_dict):
        """Formats the value provided by getter method"""
        seqnbr = trans_ref_dict.get('SEQNBR')
        seq_ref = trans_ref_dict.get('SEQREF')
        if seqnbr and seq_ref:
            trans_ref = '%s-%s-%s-%s' % (
            str(seq_ref), str(seqnbr), str(get_message_version_number(self.acm_obj)), self.swift_message_type[2:5])
            return trans_ref

    # validator
    @validate_with(MT210.MT210_SEQUENCE1_20_Type)
    def _validate_transaction_reference_number_20(self, trans_ref):
        """validates the value provided by formatter method"""
        return trans_ref

    # setter
    def _set_transaction_reference_number_20(self, trans_ref):
        """sets the value on python object"""
        self.swift_obj.SEQUENCE1.TransactionReferenceNumber = trans_ref
        self.swift_obj.SEQUENCE1.TransactionReferenceNumber.swiftTag = "20"

    # getter
    def account_identification_25(self):
        '''This returns a string for acquirer account id'''
        if self.use_operations_xml:
            account_identification = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'ACCOUNT_IDENTIFICATION'],
                                                                          ignore_absence=True)
            return account_identification
        else:
            return self.acm_obj.AcquirerAccount()

    # formatter
    def _format_account_identification_25(self, accnt_id):
        """Formats the value provided by getter method"""
        return accnt_id

    # validator
    @validate_with(MT210.MT210_SEQUENCE1_25_Type)
    def _validate_account_identification_25(self, accnt_id):
        """validates the value provided by formatter method"""
        return accnt_id

    # setter
    def _set_account_identification_25(self, accnt_id):
        """sets the value on python object"""
        self.swift_obj.SEQUENCE1.AccountIdentification = accnt_id
        self.swift_obj.SEQUENCE1.AccountIdentification.swiftTag = "25"

    # getter
    def value_date_30(self):
        '''This returns the value date for settlement'''
        if self.use_operations_xml:
            value_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'VALUE_DATE'])
            return value_date
        else:
            return get_value_date(self.acm_obj)

    # formatter
    def _format_value_date_30(self, value_date):
        """Formats the value provided by getter method"""
        if value_date:
            date_format = '%y%m%d'
            value_date = FSwiftWriterUtils.format_date(value_date, date_format)
            return str(value_date)

    # validator
    @validate_with(MT210.MT210_SEQUENCE1_30_Type)
    def _validate_value_date_30(self, value_date):
        """validates the value provided by formatter method"""
        return value_date

    # setter
    def _set_value_date_30(self, value_date):
        """sets the value on python object"""
        self.swift_obj.SEQUENCE1.ValueDate = value_date
        self.swift_obj.SEQUENCE1.ValueDate.swiftTag = "30"

    #option_getter
    def get_ordering_customer_option(self):
        """Returns default option if override is not provided"""
        return 'C'

    #option_getter
    def get_ordering_institution_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    #option_getter
    def get_intermediary_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # block getter
    def sequence_2(self):
        sequence_2_list = []
        seq_2 = MT210.MT210_SEQUENCE2()
        if self.use_operations_xml:
            seq2_blocks = FSwiftWriterUtils.get_repetative_xml_tag_value(
                self.swift_metadata_xml_dom,
                tag_names=['RELATED_REFERENCE', 'INTERBANK_SETTLED_AMOUNT', 'ORDERING_CUSTOMER_OPTION', \
                           'ORDERING_CUSTOMER_ACCOUNT', 'ORDERING_CUSTOMER_BIC', 'ORDERING_CUSTOMER_NAME', \
                           'ORDERING_CUSTOMER_ADDRESS', 'ORDERING_INSTITUTION_OPTION', 'ORDERING_INSTITUTION_ACCOUNT', \
                           'ORDERING_INSTITUTION_BIC', 'ORDERING_INSTITUTION_NAME', 'ORDERING_INSTITUTION_ADDRESS', \
                           'INTERMEDIARY_OPTION', 'INTERMEDIARY_ACCOUNT', 'INTERMEDIARY_BIC', 'INTERMEDIARY_NAME', \
                           'INTERMEDIARY_ADDRESS'],
                block_name='SWIFT', ignore_absence=True)
        else:
            seq2_blocks = []

            each_block = {}
            each_block['RELATED_REFERENCE'] = 'NONREF'
            each_block['INTERBANK_SETTLED_AMOUNT'] = self.acm_obj.Amount()

            each_block['ORDERING_CUSTOMER_OPTION'] = self.get_ordering_customer_option()
            each_block['ORDERING_CUSTOMER_ACCOUNT'] = get_ordering_customer_account(self.acm_obj)
            each_block['ORDERING_CUSTOMER_BIC'] = get_ordering_customer_bic(self.acm_obj)
            each_block['ORDERING_CUSTOMER_NAME'] = get_ordering_customer_name(self.acm_obj)
            each_block['ORDERING_CUSTOMER_ADDRESS'] = get_ordering_customer_address(self.acm_obj)

            each_block['ORDERING_INSTITUTION_OPTION'] = self.get_ordering_institution_option()
            each_block['ORDERING_INSTITUTION_ACCOUNT'] = get_ordering_institution_account(self.acm_obj)
            each_block['ORDERING_INSTITUTION_BIC'] = get_ordering_institution_bic(self.acm_obj)
            each_block['ORDERING_INSTITUTION_NAME'] = get_ordering_institution_name(self.acm_obj)
            each_block['ORDERING_INSTITUTION_ADDRESS'] = get_ordering_institution_address(self.acm_obj)

            each_block['INTERMEDIARY_OPTION'] =  self.get_intermediary_option()
            intermediary_details = get_counterpartys_intermediary_details(self.acm_obj)
            each_block['INTERMEDIARY_ACCOUNT'] = get_counterpartys_intermediary_account(self.acm_obj)
            each_block['INTERMEDIARY_BIC'] = intermediary_details.get('BIC', None)
            each_block['INTERMEDIARY_NAME'] = intermediary_details.get('NAME', None)
            each_block['INTERMEDIARY_ADDRESS'] = intermediary_details.get('ADDRESS', None)
            seq2_blocks.append(each_block)



        for block in seq2_blocks:
            block_val_dict = {}
            block_val_dict['RelatedReference'] = self.related_reference_21(block)
            block_val_dict['CurrencyCodeAmount'] = self.currency_code_amount_32B(block)

            ordering_customer_option = block['ORDERING_CUSTOMER_OPTION']
            if ordering_customer_option == "NO OPTION":
                block_val_dict['OrderingCustomer'] = self.ordering_customer_No_Option_50(block)
            elif ordering_customer_option == "C":
                block_val_dict['OrderingCustomer_C'] = self.ordering_customer_50C(block)
            elif ordering_customer_option == "F":
                block_val_dict['OrderingCustomer_F'] = self.ordering_customer_50F(block)
            else:
                notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                    self.swift_message_type, str(ordering_customer_option), 'OrderingCustomer_50'))
                block_val_dict['OrderingCustomer'] = self.ordering_customer_No_Option_50(block)

            ordering_institution_option = block['ORDERING_INSTITUTION_OPTION']
            if ordering_institution_option == "A":
                block_val_dict['OrderingInstitution_A'] = self.ordering_institution_52A(block)
            elif ordering_institution_option == "D":
                block_val_dict['OrderingInstitution_D'] = self.ordering_institution_52D(block)
            else:
                notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                    self.swift_message_type, str(ordering_institution_option), 'OrderingInstitution_52a'))
                block_val_dict['OrderingInstitution_A'] = self.ordering_institution_52A(block)

            intermediary_option = block['INTERMEDIARY_OPTION']
            if intermediary_option == "A":
                block_val_dict['Intermedairy_A'] = self.intermediary_56A(block)
            elif intermediary_option == "D":
                block_val_dict['Intermedairy_D'] = self.intermediary_56D(block)
            else:
                notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                    self.swift_message_type, str(intermediary_option), 'Intermediary_56a'))
                block_val_dict['Intermedairy_A'] = self.intermediary_56A(block)
            sequence_2_list.append(block_val_dict)
        return sequence_2_list

    # block formatter
    def _format_sequence_2(self, block_val_dicts):
        format_list = []
        for each_block in block_val_dicts:
            format_dict_val = {}
            format_dict_val['RelatedReference'] = self._format_related_reference_21(each_block['RelatedReference'])
            format_dict_val['CurrencyCodeAmount'] = self._format_currency_code_amount_32B(
                each_block['CurrencyCodeAmount'])
            if 'OrderingCustomer' in list(each_block.keys()):
                format_dict_val['OrderingCustomer'] = self._format_ordering_customer_No_Option_50(
                    each_block['OrderingCustomer'])
            if 'OrderingCustomer_C' in list(each_block.keys()):
                format_dict_val['OrderingCustomer_C'] = self._format_ordering_customer_50C(
                    each_block['OrderingCustomer_C'])
            if 'OrderingCustomer_F' in list(each_block.keys()):
                format_dict_val['OrderingCustomer_F'] = self._format_ordering_customer_50F(
                    each_block['OrderingCustomer_F'])
            if 'OrderingInstitution_A' in list(each_block.keys()):
                format_dict_val['OrderingInstitution_A'] = self._format_ordering_institution_52A(
                    each_block['OrderingInstitution_A'])
            if 'OrderingInstitution_D' in list(each_block.keys()):
                format_dict_val['OrderingInstitution_D'] = self._format_ordering_institution_52D(
                    each_block['OrderingInstitution_D'])
            if 'Intermedairy_A' in list(each_block.keys()):
                format_dict_val['Intermedairy_A'] = self._format_intermediary_56A(each_block['Intermedairy_A'])
            if 'Intermedairy_D' in list(each_block.keys()):
                format_dict_val['Intermedairy_D'] = self._format_intermediary_56D(each_block['Intermedairy_D'])
            format_list.append(format_dict_val)
        return format_list

    # block validator
    def _validate_sequence_2(self, format_val):
        err_msg = ''
        validated_val = []
        for each_block in format_val:
            validate_dict = {}
            val = self._validate_related_reference_21(each_block['RelatedReference'])
            validate_dict['RelatedReference'] = val
            val = self._validate_currency_code_amount_32B(each_block['CurrencyCodeAmount'])
            validate_dict['CurrencyCodeAmount'] = val
            if 'OrderingCustomer' in list(each_block.keys()):
                val = self._validate_ordering_customer_No_Option_50(each_block['OrderingCustomer'])
                validate_dict['OrderingCustomer'] = val
            if 'OrderingCustomer_C' in list(each_block.keys()):
                val = self._validate_ordering_customer_50C(each_block['OrderingCustomer_C'])
                validate_dict['OrderingCustomer_C'] = val
            if 'OrderingCustomer_F' in list(each_block.keys()):
                val = self._validate_ordering_customer_50F(each_block['OrderingCustomer_F'])
                validate_dict['OrderingCustomer_F'] = val
            if 'OrderingInstitution_A' in list(each_block.keys()):
                val = self._validate_ordering_institution_52A(each_block['OrderingInstitution_A'])
                validate_dict['OrderingInstitution_A'] = val
            if 'OrderingInstitution_D' in list(each_block.keys()):
                val = self._validate_ordering_institution_52D(each_block['OrderingInstitution_D'])
                validate_dict['OrderingInstitution_D'] = val
            if 'Intermedairy_A' in list(each_block.keys()):
                val = self._validate_intermediary_56A(each_block['Intermedairy_A'])
                validate_dict['Intermedairy_A'] = val
            if 'Intermedairy_D' in list(each_block.keys()):
                val = self._validate_intermediary_56D(each_block['Intermedairy_D'])
                validate_dict['Intermedairy_D'] = val
            validated_val.append(validate_dict)
        return validated_val

    # block
    def _set_sequence_2(self, block_val_dict):
        for each_val in block_val_dict:
            seq_2 = MT210.MT210_SEQUENCE2()
            self._setrelated_reference_21(each_val['RelatedReference'], seq_2)
            self._setcurrency_code_amount_32B(each_val['CurrencyCodeAmount'], seq_2)
            if 'OrderingCustomer' in list(each_val.keys()):
                self._setordering_customer_No_Option_50(each_val['OrderingCustomer'], seq_2)
            if 'OrderingCustomer_C' in list(each_val.keys()):
                self._setordering_customer_50C(each_val['OrderingCustomer_C'], seq_2)
            if 'OrderingCustomer_F' in list(each_val.keys()):
                self._setordering_customer_50F(each_val['OrderingCustomer_F'], seq_2)
            if not (seq_2.OrderingCustomer_F or seq_2.OrderingCustomer_C or seq_2.OrderingCustomer):  # network rule C2
                if 'OrderingInstitution_A' in list(each_val.keys()):
                    self._setordering_institution_52A(each_val['OrderingInstitution_A'], seq_2)
                if 'OrderingInstitution_D' in list(each_val.keys()):
                    self._setordering_institution_52D(each_val['OrderingInstitution_D'], seq_2)
            if 'Intermedairy_A' in list(each_val.keys()):
                self._setintermediary_56A(each_val['Intermedairy_A'], seq_2)
            if 'Intermedairy_D' in list(each_val.keys()):
                self._setintermediary_56D(each_val['Intermedairy_D'], seq_2)
            self.swift_obj.SEQUENCE2.append(seq_2)


    # getter
    def related_reference_21(self, block):
        '''returns the related reference settlement number'''
        related_reference = block['RELATED_REFERENCE']
        return related_reference

    # formatter
    def _format_related_reference_21(self, val):
        """Formats the value provided by getter method"""
        return val

    # validator
    @validate_with(MT210.MT210_SEQUENCE2_21_Type)
    def _validate_related_reference_21(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setrelated_reference_21(self, val, seq_2):
        """sets the value on python object"""
        if val:
            seq_2.RelatedReference = val
            seq_2.RelatedReference.swiftTag = "21"

    # getter
    def currency_code_amount_32B(self, block):
        '''returns a dictionary for settlement currrency and amount as values
        example - {curr : settlement.Currency(), 'amount' : INTERBANK_SETTLED_AMOUNT}'''
        values_dict = {}
        curr = None
        if self.use_operations_xml:
            curr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'CURR'])
        else:
            curr = self.acm_obj.Currency().Name()
        amount = block['INTERBANK_SETTLED_AMOUNT']
        values_dict['curr'] = curr
        values_dict['amount'] = amount
        return values_dict

    # formatter
    def _format_currency_code_amount_32B(self, val):
        """Formats the value provided by getter method"""
        curr = val.get('curr')
        amount = val.get('amount')
        amount = apply_currency_precision(curr, float(amount))
        curr_amount = str(curr) + FSwiftMLUtils.float_to_swiftmt(str(amount))
        return curr_amount

    # validator
    @validate_with(MT210.MT210_SEQUENCE2_32B_Type)
    def _validate_currency_code_amount_32B(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setcurrency_code_amount_32B(self, val, seq_2):
        """sets the value on python object"""
        if val:
            seq_2.CurrencyCodeAmount = val
            seq_2.CurrencyCodeAmount.swiftTag = "32B"

    # getter
    def ordering_customer_No_Option_50(self, block):
        '''returns ordering customer name and address in the form of dictionary'''
        values_dict = {}
        ordering_customer_name = block['ORDERING_CUSTOMER_NAME']
        ordering_customer_address = block['ORDERING_CUSTOMER_ADDRESS']
        values_dict['ordering_customer_name'] = ordering_customer_name
        values_dict['ordering_customer_address'] = ordering_customer_address
        return values_dict

    # formatter
    def _format_ordering_customer_No_Option_50(self, val):
        """Formats the value provided by getter method"""
        name = val.get('ordering_customer_name')
        address = val.get('ordering_customer_address')

        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            value = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            return value

    # validator
    @validate_with(MT210.MT210_SEQUENCE2_50_Type)
    def _validate_ordering_customer_No_Option_50(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_customer_No_Option_50(self, val, seq_2):
        """sets the value on python object"""
        if val:
            seq_2.OrderingCustomer = val
            seq_2.OrderingCustomer.swiftTag = "50"

    # getter
    def ordering_customer_50C(self, block):
        '''returns BIC of ordering customer'''
        ordering_customer_bic = block['ORDERING_CUSTOMER_BIC']
        return ordering_customer_bic

    # formatter
    def _format_ordering_customer_50C(self, val):
        """Formats the value provided by getter method"""
        return val

    # validator
    @validate_with(MT210.MT210_SEQUENCE2_50C_Type)
    def _validate_ordering_customer_50C(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_customer_50C(self, val, seq_2):
        """sets the value on python object"""
        if val:
            seq_2.OrderingCustomer_C = val
            seq_2.OrderingCustomer_C.swiftTag = "50C"

    # getter
    def ordering_customer_50F(self, block):
        '''returns ordering customer details in the form of dictionary'''
        values_dict = {}
        ordering_customer_account = block['ORDERING_CUSTOMER_ACCOUNT']
        ordering_customer_name = block['ORDERING_CUSTOMER_NAME']
        ordering_customer_address = block['ORDERING_CUSTOMER_ADDRESS']
        values_dict['ordering_customer_account'] = ordering_customer_account
        values_dict['ordering_customer_name'] = ordering_customer_name
        values_dict['ordering_customer_address'] = ordering_customer_address
        return values_dict

    # formatter
    def _format_ordering_customer_50F(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ordering_customer_account')
        name = val.get('ordering_customer_name')
        address = val.get('ordering_customer_address')
        country_code = GetOrderingCustomerCountryCode(self.acm_obj)
        town = GetOrderingCustomerTown(self.acm_obj)
        name_list, address_list, country_and_town_list = [], [], []

        temp_name = name
        temp_address = address
        temp_town = town
        char_set = ''
        lookup_temp = lookup
        try:
            char_set = str(self.acm_obj.Counterparty().AdditionalInfo().TraditionalChinese())
        except Exception as e:
            notifier.WARN("Could not find Additional Info 'TraditionalChinese'.")

        if char_set == 'True':
            lookup_temp = CCC_traditional_writer
        elif char_set == 'False':
            lookup_temp = CCC_simplified_writer

        if temp_name:
            try:
                for key in list(lookup_temp.keys()):
                    temp_name = temp_name.replace(str(key), lookup_temp[key] + " ")
                    temp_address = temp_address.replace(str(key), lookup_temp[key] + " ")
                    temp_town = temp_town.replace(str(key), lookup_temp[key] + " ")
            except Exception as e:
                pass
        if name == temp_name:
            if name:
                name_list = FSwiftWriterUtils.split_text_and_prefix(str(name), 33, '1/')
            if address:
                address_list = FSwiftWriterUtils.split_text_and_prefix(str(address), 33, '2/')
            if country_code:
                additional_details = str(country_code)
                if town:
                    additional_details = additional_details + '/' + str(town)
                country_and_town_list = FSwiftWriterUtils.split_text_and_prefix(
                    str(additional_details), 33, '3/')
            value = FSwiftWriterUtils.allocate_space_for_name_and_address_with_constraint(name_list, address_list,
                                                                                          country_and_town_list)
            if account:
                account = '/' + account
                value = account + '\n' + value
            return value
        else:
            name = temp_name
            address = temp_address
            town = temp_town
            if name:
                name_list = FSwiftWriterUtils.split_text_logically_and_prefix(str(name), 33, '1/')
            if address:
                address_list = FSwiftWriterUtils.split_text_logically_and_prefix(str(address), 33, '2/')
            if country_code:
                additional_details = str(country_code)
                if town:
                    additional_details = additional_details + '/' + str(town)
                country_and_town_list = FSwiftWriterUtils.split_text_logically_and_prefix(
                    str(additional_details), 33, '3/')
            value = FSwiftWriterUtils.allocate_space_for_name_and_address_with_constraint(name_list, address_list,
                                                                                          country_and_town_list)
            if account:
                account = '/' + account
                value = account + '\n' + value
            return value

    # validator
    @validate_with(MT210.MT210_SEQUENCE2_50F_Type)
    def _validate_ordering_customer_50F(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_customer_50F(self, val, seq_2):
        """sets the value on python object"""
        if val:
            seq_2.OrderingCustomer_F = val
            seq_2.OrderingCustomer_F.swiftTag = '50F'

    # getter
    def ordering_institution_52A(self, block):
        '''returns ordering institution details in the form of dictionary'''
        values_dict = {}
        ordering_institution_account = block['ORDERING_INSTITUTION_ACCOUNT']
        ordering_institution_bic = block['ORDERING_INSTITUTION_BIC']
        values_dict['ordering_institution_account'] = ordering_institution_account
        values_dict['ordering_institution_bic'] = ordering_institution_bic
        return values_dict

    # formatter
    def _format_ordering_institution_52A(self, val):
        """Formats the value provided by getter method"""
        ordering_institution_account = val.get('ordering_institution_account')
        ordering_institution_bic = val.get('ordering_institution_bic')
        field_value = ordering_institution_bic
        if ordering_institution_account:
            field_value = "/" + str(ordering_institution_account) + "\n" + str(field_value)
        return field_value

    # validator
    @validate_with(MT210.MT210_SEQUENCE2_52A_Type)
    def _validate_ordering_institution_52A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_institution_52A(self, val, seq_2):
        """sets the value on python object"""
        if val:
            seq_2.OrderingInstitution_A = val
            seq_2.OrderingInstitution_A.swiftTag = "52A"

    # getter
    def ordering_institution_52D(self, block):
        '''returns ordering institution details in the form of dictionary'''
        values_dict = {}
        ordering_institution_account = block['ORDERING_INSTITUTION_ACCOUNT']
        ordering_institution_name = block['ORDERING_INSTITUTION_NAME']
        ordering_institution_address = block['ORDERING_INSTITUTION_ADDRESS']
        values_dict['ordering_institution_account'] = ordering_institution_account
        values_dict['ordering_institution_name'] = ordering_institution_name
        values_dict['ordering_institution_address'] = ordering_institution_address
        return values_dict

    # formatter
    def _format_ordering_institution_52D(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ordering_institution_account')
        name = val.get('ordering_institution_name')
        address = val.get('ordering_institution_address')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
        if account:
            val = "/" + str(account) + "\n" + str(val)

        return val

    # validator
    @validate_with(MT210.MT210_SEQUENCE2_52D_Type)
    def _validate_ordering_institution_52D(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_institution_52D(self, val, seq_2):
        """sets the value on python object"""
        if val:
            seq_2.OrderingInstitution_D = val
            seq_2.OrderingInstitution_D.swiftTag = "52D"

    # getter
    def intermediary_56A(self, block):
        '''returns intermediary details in the form of dictionary'''
        values_dict = {}
        intermediary_account = block['INTERMEDIARY_ACCOUNT']
        intermediary_bic = block['INTERMEDIARY_BIC']
        values_dict['intermediary_account'] = intermediary_account
        values_dict['intermediary_bic'] = intermediary_bic
        return values_dict

    # formatter
    def _format_intermediary_56A(self, val):
        """Formats the value provided by getter method"""
        intermediary_account = val.get('intermediary_account')
        intermediary_bic = val.get('intermediary_bic')
        field_value = intermediary_bic
        if intermediary_account:
            field_value = "/" + str(intermediary_account) + "\n" + str(field_value)
        return field_value

    # validator
    @validate_with(MT210.MT210_SEQUENCE2_56A_Type)
    def _validate_intermediary_56A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setintermediary_56A(self, val, seq_2):
        """sets the value on python object"""
        if val:
            seq_2.Intermedairy_A = val
            seq_2.Intermedairy_A.swiftTag = "56A"

    # getter
    def intermediary_56D(self, block):
        '''returns intermediary details in the form of dictionary'''
        values_dict = {}
        intermediary_account = block['INTERMEDIARY_ACCOUNT']
        intermediary_name = block['INTERMEDIARY_NAME']
        intermediary_address = block['INTERMEDIARY_ADDRESS']
        values_dict['intermediary_account'] = intermediary_account
        values_dict['intermediary_name'] = intermediary_name
        values_dict['intermediary_address'] = intermediary_address
        return values_dict

    # formatter
    def _format_intermediary_56D(self, val):
        """Formats the value provided by getter method"""
        account = val.get('intermediary_account')
        name = val.get('intermediary_name')
        address = val.get('intermediary_address')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT210.MT210_SEQUENCE2_56D_Type)
    def _validate_intermediary_56D(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setintermediary_56D(self, val, seq_2):
        """sets the value on python object"""
        if val:
            seq_2.Intermedairy_D = val
            seq_2.Intermedairy_D.swiftTag = "56D"


class FMT210OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_typ = "210"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT'+ self.mt_typ)
        super(FMT210OutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

    def message_type(self):
        """returns type of message"""
        return "210"

    def sender_logical_terminal_address(self):
        '''LT code is hardcoded as A for sender'''
        terminal_address = ''
        senders_bic = None
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
        terminal_address = ''
        receivers_bic = None
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'RECEIVER_BIC'])
        else:
            receivers_bic = get_receivers_bic(self.acm_obj)
        if receivers_bic:
            terminal_address = self.logical_terminal_address(receivers_bic, "X")
        return terminal_address

    def logical_terminal_address(self, bic_code, lt_code):
        """returns logical terminal address"""
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
        """returns input or output"""
        return "I"

    def message_user_reference(self):
        '''MUR is sent in the format FAC-SEQNBR of confirmation-VersionID'''
        seqnbr = ''
        seqref = ''
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seqref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            seqnbr = self.acm_obj.Oid()
            seqref = get_settlement_reference_prefix()
            return "{108:%s-%s-%s-%s}" % (seqref, seqnbr, get_message_version_number(self.acm_obj), self.mt_typ[0:3])


class FMT210OutBaseNetworkRules(object):
    """validation of swift message by network rules"""
    def __init__(self, swift_message_obj, swift_message, acm_obj ,swift_metadata_xml_dom=None):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.acm_obj = acm_obj
        self.mt_typ = "210"
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT' + self.mt_typ)

    def network_rule_C1(self):
        ''' The repetitive sequence must not appear more than ten times(Error code(s): T10). '''
        if len(self.swift_message_obj.SEQUENCE2) > 10:
            return "Repeatitive Sequence must not appear more than ten times"

    def network_rule_C2(self):
        '''
            Either field 50a or field 52a, but not both, must be present in a repetitive sequence(Error code(s): C06).
            If field 50a is Present; Then field 52a is Not allowed
            If field 50a is Not Present; Then field 52a is Mandatory
        '''
        for field in self.swift_message_obj.SEQUENCE2:
            ord_customer = field.OrderingCustomer_F or field.OrderingCustomer_C or field.OrderingCustomer
            ord_institution = field.OrderingInstitution_A or field.OrderingInstitution_D
            if ord_customer and ord_institution:
                return "Field 50 is present so field 52 is Not allowed"
            elif not ord_customer and not ord_institution:
                return "Field 50a is not present, Hence field 52a is mandatory"

    def network_rule_C3(self):
        '''
            The currency code must be the same for all occurrences of field 32B in the message (Error code(s): C02).
        '''
        curr_list = []
        for curr_value in self.swift_message_obj.SEQUENCE2:
            if curr_value.CurrencyCodeAmount and curr_value.CurrencyCodeAmount.value():
                value = curr_value.CurrencyCodeAmount.value()
                curr_list.append(value)
        curr_list_from_set = list(set(curr_list))
        if len(curr_list_from_set) > 1:
            return "The currency code must be the same for all occurrences of field 32B in the message"


# Move this code to MT210 acm object mapping file


def GetOrderingCustomerCountryCode(settlement):
    """returns ordering customer country code"""
    return settlement.Counterparty().JurisdictionCountryCode()


def GetOrderingCustomerTown(settlement):
    """returns town of ordering customer"""
    return settlement.Counterparty().City()

