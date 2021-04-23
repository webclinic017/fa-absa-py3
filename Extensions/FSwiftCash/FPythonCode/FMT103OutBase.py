"""----------------------------------------------------------------------------
MODULE:
    FMT103OutBase

DESCRIPTION:
    This module provides the base class for the FMT103 outgoing implementation

CLASS:
    FMT103Base

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftMLUtils
import FSwiftWriterLogger
import FSwiftWriterMessageHeader
import FSwiftWriterUtils
import MT103
import acm
import uuid
from FCashOutUtils import *
from FSwiftWriterEngine import validate_with, should_use_operations_xml

from FCustomerPaymentsOutBase import FCustomerPaymentsOutBase

from ChineseCommercialCode import CCC_simplified_writer, CCC_traditional_writer

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')

CONFIG_PARAM = FSwiftMLUtils.Parameters('FSwiftWriterConfig')

chinese_language_version = getattr(CONFIG_PARAM, 'ChineseLanguageVersion', None)
if chinese_language_version:
    if chinese_language_version == 'Simplified':
        lookup = CCC_simplified_writer
    if chinese_language_version == 'Traditional':
        lookup = CCC_traditional_writer
else:
    lookup = CCC_simplified_writer

class FMT103Base(FCustomerPaymentsOutBase):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = 'MT103'
        super(FMT103Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # Implementing it to pass the NotImplementedError
    def _message_sequences(self):
        pass

    # --------------------------------- senders_reference -------------------------------------------
    # getter
    def senders_reference_20(self):
        """ Returns a senders_reference_20 as string """
        if self.use_operations_xml:
            senders_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SETTLEMENT', 'SEQNBR'])
        else:
            senders_reference = self.acm_obj.Oid()
        return senders_reference

    # formatter
    def _format_senders_reference_20(self, val):
        """Formats the value provided by getter method"""
        if val:
            sett_obj = acm.FSettlement[str(val)]
            val = "%s-%s-%s-%s" % (get_settlement_reference_prefix(), str(val), str(get_message_version_number(sett_obj)), str(self.swift_message_type[2:5]))
        return val

    # validator
    @validate_with(MT103.MT103_20_Type)
    def _validate_senders_reference_20(self, val):
        """validates the value provided by formatter method"""
        validate_slash_and_double_slash(val, "Senders Reference")  # .value()
        return val

    # setter
    def _set_senders_reference_20(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.SendersReference = val
        self.swift_obj.SendersReference.swiftTag = "20"

    # --------------------------------- bank_operation_code -------------------------------------------
    # getter
    def bank_operation_code_23B(self):
        """ Returns a bank_operation_code as string """
        if self.use_operations_xml:
            bank_operation_code = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'BANK_OPERATION_CODE'])
        else:
            bank_operation_code = get_bank_operation_code()
        return bank_operation_code

    # formatter
    def _format_bank_operation_code_23B(self, val):
        """Formats the value provided by getter method"""
        return val

    # validator
    @validate_with(MT103.MT103_23B_Type)
    def _validate_bank_operation_code_23B(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _set_bank_operation_code_23B(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.BankOperationCode = val
        self.swift_obj.BankOperationCode.swiftTag = "23B"

    # --------------------------------- instruction_code -------------------------------------------
    # getter
    def instruction_code_23E(self):
        """ Returns a instruction_code as string """
        if self.use_operations_xml:
            instruction_code = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                        ['SWIFT', 'INSTRUCTION_CODE'],
                                                                        ignore_absence=True)
        else:
            instruction_code = get_instruction_code()  # code
        return instruction_code

    # formatter
    def _format_instruction_code_23E(self, val):
        """Formats the value provided by getter method"""
        return val

    # validator
    @validate_with(MT103.MT103_23E_Type)
    def _validate_instruction_code_23E(self, val):
        """validates the value provided by formatter method"""
        validate_instruction_code(val)
        return val

    # setter
    def _set_instruction_code_23E(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.InstructionCode.append(val)
        for each_instruction_code in self.swift_obj.InstructionCode:
            each_instruction_code.swiftTag = "23E"

    # --------------------------------- instruction_code -------------------------------------------
    # getter
    def value_date_32A(self):
        """ Returns a dictionary as {'value_date': value, 'currency':value, 'interbank_settled_amount':value} """
        values_dict = {}
        if self.use_operations_xml:
            value_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'VALUE_DATE'])
            currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'CURR'])
            interbank_settled_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                ['SWIFT', 'INTERBANK_SETTLED_AMOUNT'])
        else:
            value_date = get_value_date(self.acm_obj)
            currency = self.acm_obj.Currency().Name()
            interbank_settled_amount = self.acm_obj.Amount()

        values_dict['value_date'] = value_date
        values_dict['currency'] = currency
        values_dict['interbank_settled_amount'] = interbank_settled_amount

        return values_dict

    # formatter
    def _format_value_date_32A(self, val):
        """Formats the value provided by getter method"""
        value_date = val.get('value_date')
        currency = val.get('currency')
        interbank_settled_amount = val.get('interbank_settled_amount')
        date_format = '%y%m%d'
        if value_date and currency and interbank_settled_amount:
            value_date = FSwiftWriterUtils.format_date(value_date, date_format)
            interbank_settled_amount = apply_currency_precision(currency, abs(float(interbank_settled_amount)))
            val = str(value_date) + str(currency) + str(FSwiftMLUtils.float_to_swiftmt(str(interbank_settled_amount)))
            return val

    # validator
    @validate_with(MT103.MT103_32A_Type)
    def _validate_value_date_32A(self, val):
        """validates the value provided by formatter method"""
        validate_currency_amount(val[6:], '32A')  # .value
        return val

    # setter
    def _set_value_date_32A(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.ValueDateCurrencyInterbankSettledAmount = val
        self.swift_obj.ValueDateCurrencyInterbankSettledAmount.swiftTag = "32A"

    # --------------------------------- instruction_code -------------------------------------------
    # getter
    def instructed_amount_33B(self):
        """ Returns a dictionary as {'instructed_amount': value, 'currency':value} """
        values_dict = {}
        if self.use_operations_xml:
            instructed_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'INSTRUCTED_AMOUNT'],
                                                                         ignore_absence=True)
            currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'CURR'],
                                                                ignore_absence=True)


        else:
            instructed_amount = self.acm_obj.Amount()
            currency = self.acm_obj.Currency().Name()

        values_dict['instructed_amount'] = instructed_amount
        values_dict['currency'] = currency
        return values_dict

    # formatter
    def _format_instructed_amount_33B(self, val):
        """Formats the value provided by getter method"""
        instructed_amount = val.get('instructed_amount')
        currency = val.get('currency')
        if instructed_amount and currency:
            instructed_amount = apply_currency_precision(currency, abs(float(instructed_amount)))
            val = str(currency) + str(FSwiftMLUtils.float_to_swiftmt(str(instructed_amount)))
            return val

    # validator
    @validate_with(MT103.MT103_33B_Type)
    def _validate_instructed_amount_33B(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _set_instructed_amount_33B(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.CurrencyInstructedAmount = val
        self.swift_obj.CurrencyInstructedAmount.swiftTag = "33B"

    # --------------------------------- ordering_customer -------------------------------------------

    #option_getter
    def get_ordering_customer_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_ordering_customer(self):
        """Returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            ordering_customer_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                ['SWIFT', 'ORDERING_CUSTOMER_OPTION'])
        else:
            ordering_customer_option = self.get_ordering_customer_option()
        if ordering_customer_option == "A":
            getter_name = 'ordering_customer_50A'
        elif ordering_customer_option == "F":
            getter_name = 'ordering_customer_50F'
        elif ordering_customer_option == "K":
            getter_name = 'ordering_customer_50K'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(ordering_customer_option), 'OrderingCustomer_50a'))
            getter_name = 'ordering_customer_50A'  # default
        return getter_name

    # getter
    def ordering_customer_50A(self):
        """ Returns a dictionary as {'ordering_customer_account': value, 'ordering_customer_bic':value} """
        values_dict = {}
        if self.use_operations_xml:
            ordering_customer_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'ORDERING_CUSTOMER_ACCOUNT'],
                                                                                 ignore_absence=True)
            ordering_customer_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                             ['SWIFT', 'ORDERING_CUSTOMER_BIC'])
            values_dict['ACCOUNT'] = ordering_customer_account
            values_dict['BIC'] = ordering_customer_bic
            return values_dict
        else:
            return get_acquirer_details(self.acm_obj)

    # formatter
    def _format_ordering_customer_50A(self, val):
        """Formats the value provided by getter method"""
        ordering_customer_account = val.get('ACCOUNT')
        ordering_customer_bic = val.get('BIC')
        if ordering_customer_bic:
            if ordering_customer_account:
                val = "/" + str(ordering_customer_account) + "\n" + str(ordering_customer_bic)
            else:
                val = str(ordering_customer_bic)
            return val

    # validator

    @validate_with(MT103.MT103_50A_Type)
    def _validate_ordering_customer_50A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_customer_50A(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.OrderingCustomer_A = val
        self.swift_obj.OrderingCustomer_A.swiftTag = '50A'

    # getter
    def ordering_customer_50F(self):
        """ Returns a dictionary as {'ordering_customer_account': value, 'ordering_customer_name':value, 'ordering_customer_address':value,
        'ordering_customer_country_code':value, 'ordering_customer_town':value, 'ordering_customer_zipcode':value} """
        values_dict = {}
        if self.use_operations_xml:
            ordering_customer_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'ORDERING_CUSTOMER_ACCOUNT'],
                                                                                 ignore_absence=True)
            ordering_customer_name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                              ['SWIFT', 'ORDERING_CUSTOMER_NAME'], )
            ordering_customer_address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'ORDERING_CUSTOMER_ADDRESS'],
                                                                                 ignore_absence=True)
            ordering_customer_country_code = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                      ['SWIFT',
                                                                                       'ORDERING_CUSTOMER_COUNTRY_CODE'],
                                                                                      ignore_absence=True)
            ordering_customer_town = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                              ['SWIFT', 'ORDERING_CUSTOMER_TOWN'],
                                                                              ignore_absence=True)
            ordering_customer_zipcode = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'ORDERING_CUSTOMER_ZIPCODE'],
                                                                                 ignore_absence=True)
            values_dict['ACCOUNT'] = ordering_customer_account
            values_dict['NAME'] = ordering_customer_name
            values_dict['ADDRESS'] = ordering_customer_address
            values_dict['COUNTRY_CODE'] = ordering_customer_country_code
            values_dict['TOWN'] = ordering_customer_town
            values_dict['ZIP_CODE'] = ordering_customer_zipcode
            return values_dict
        else:
            return get_acquirer_details(self.acm_obj)

    # formatter
    def _format_ordering_customer_50F(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ACCOUNT')
        name = val.get('NAME')
        address = val.get('ADDRESS')
        country_code = val.get('COUNTRY_CODE')
        town = val.get('TOWN')
        town = '/' + str(town)
        zipcode = val.get('ZIP_CODE')
        zipcode = '/' + str(zipcode)
        name_list, address_list, country_and_town_list = [], [], []

        char_set = ''
        lookup_temp = lookup
        try:
            char_set = str(self.acm_obj.Acquirer().AdditionalInfo().TraditionalChinese())
        except Exception as e:
            notifier.WARN("Could not find Additional Info 'TraditionalChinese'.")

        if char_set == 'True':
            lookup_temp = CCC_traditional_writer
        elif char_set == 'False':
            lookup_temp = CCC_simplified_writer

        temp_name = name
        temp_address = address
        temp_town = town
        for key in list(lookup_temp.keys()):
            temp_name = temp_name.replace(str(key), lookup_temp[key] + " ")
            temp_address = temp_address.replace(str(key), lookup_temp[key] + " ")
            temp_town = temp_town.replace(str(key), lookup_temp[key] + " ")

        if name == temp_name:
            if name:
                name_list = FSwiftWriterUtils.split_text_and_prefix(str(name), 33, '1/')
            if address:
                address_list = FSwiftWriterUtils.split_text_and_prefix(str(address), 33, '2/')
            if country_code:
                additional_details = str(country_code)
                if town:
                    additional_details = additional_details + str(town)
                    if zipcode:
                        zipcode = additional_details + str(zipcode)
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
                    additional_details = additional_details + str(town)
                    if zipcode:
                        zipcode = additional_details + str(zipcode)
                country_and_town_list = FSwiftWriterUtils.split_text_logically_and_prefix(
                    str(additional_details), 33, '3/')
            value = FSwiftWriterUtils.allocate_space_for_name_and_address_with_constraint(name_list, address_list,
                                                                                          country_and_town_list)
            if account:
                account = '/' + account
                value = account + '\n' + value
            return value


    # validator
    @validate_with(MT103.MT103_50F_Type)
    def _validate_ordering_customer_50F(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_customer_50F(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.OrderingCustomer_F = val
        self.swift_obj.OrderingCustomer_F.swiftTag = '50F'

    # getter
    def ordering_customer_50K(self):
        """ Returns a dictionary as {'ordering_customer_account': value, 'ordering_customer_name':value, 'ordering_customer_address':value} """
        values_dict = {}
        if self.use_operations_xml:
            ordering_customer_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'ORDERING_CUSTOMER_ACCOUNT'],
                                                                                 ignore_absence=True)
            ordering_customer_name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                              ['SWIFT', 'ORDERING_CUSTOMER_NAME'])
            ordering_customer_address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'ORDERING_CUSTOMER_ADDRESS'])
            values_dict['ACCOUNT'] = ordering_customer_account
            values_dict['NAME'] = ordering_customer_name
            values_dict['ADDRESS'] = ordering_customer_address
            return values_dict
        else:
            return get_acquirer_details(self.acm_obj)

    # formatter
    def _format_ordering_customer_50K(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ACCOUNT')
        name = val.get('NAME')
        address = val.get('ADDRESS')

        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT103.MT103_50K_Type)
    def _validate_ordering_customer_50K(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_customer_50K(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.OrderingCustomer_K = val
        self.swift_obj.OrderingCustomer_K.swiftTag = '50K'

    # --------------------------------- ordering_institution -------------------------------------------

    #option_getter
    def get_ordering_institution_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_ordering_institution(self):
        """Returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            ordering_institution_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                   ['SWIFT',
                                                                                    'ORDERING_INSTITUTION_OPTION'],
                                                                                   ignore_absence=True)
        else:
            ordering_institution_option = self.get_ordering_institution_option()
        if ordering_institution_option == "A":
            getter_name = 'ordering_institution_52A'
        elif ordering_institution_option == "D":
            getter_name = 'ordering_institution_52D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(ordering_institution_option), 'OrderingInstitution_52a'))
            getter_name = 'ordering_institution_52A'  # default
        return getter_name

    # getter
    def ordering_institution_52A(self):
        """ Returns a dictionary as {'ordering_institution_account': value, 'ordering_institution_bic':value} """
        values_dict = {}
        if self.use_operations_xml:
            ordering_institution_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                    ['SWIFT',
                                                                                     'ORDERING_INSTITUTION_ACCOUNT'],
                                                                                    ignore_absence=True)
            ordering_institution_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                ['SWIFT', 'ORDERING_INSTITUTION_BIC'])
            values_dict['ACCOUNT'] = ordering_institution_account
            values_dict['BIC'] = ordering_institution_bic
            return values_dict
        else:
            values_dict = {}
            values_dict = get_acquirer_details(self.acm_obj)
            return values_dict

    # formatter
    def _format_ordering_institution_52A(self, val):
        """Formats the value provided by getter method"""
        ordering_institution_account = val.get('ACCOUNT')
        ordering_institution_bic = val.get('BIC')
        if ordering_institution_bic:
            if ordering_institution_account:
                val = "/" + str(ordering_institution_account) + "\n" + str(ordering_institution_bic)
            else:
                val = str(ordering_institution_bic)
            return val

    # validator
    @validate_with(MT103.MT103_52A_Type)
    def _validate_ordering_institution_52A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_institution_52A(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.OrderingInstitution_A = val
        self.swift_obj.OrderingInstitution_A.swiftTag = '52A'

    # getter
    def ordering_institution_52D(self):
        """ Returns a dictionary as {'ordering_institution_account': value, 'ordering_institution_bic':value, 'ordering_institution_address':value} """
        values_dict = {}
        if self.use_operations_xml:
            ordering_institution_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                    ['SWIFT',
                                                                                     'ORDERING_INSTITUTION_ACCOUNT'],
                                                                                    ignore_absence=True)
            ordering_institution_name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'ORDERING_INSTITUTION_NAME'])
            ordering_institution_address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                    ['SWIFT',
                                                                                     'ORDERING_INSTITUTION_ADDRESS'])
            values_dict['ACCOUNT'] = ordering_institution_account
            values_dict['NAME'] = ordering_institution_name
            values_dict['ADDRESS'] = ordering_institution_address
            return values_dict
        else:
            return get_acquirer_details(self.acm_obj)

    # formatter
    def _format_ordering_institution_52D(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ACCOUNT')
        name = val.get('NAME')
        address = val.get('ADDRESS')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT103.MT103_52D_Type)
    def _validate_ordering_institution_52D(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_institution_52D(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.OrderingInstitution_D = val
        self.swift_obj.OrderingInstitution_D.swiftTag = '52D'

    # --------------------------------- senders_correspondent -------------------------------------------

    #option_getter
    def get_senders_correspondent_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_senders_correspondent(self):
        """Returns name of the getter"""
        getter_name = ''
        if self.use_operations_xml:
            senders_correspondent_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                    ['SWIFT',
                                                                                     'SENDERS_CORRESPONDENT_OPTION'],
                                                                                    ignore_absence=True)
        else:
            senders_correspondent_option = self.get_senders_correspondent_option()
        if senders_correspondent_option == 'A':
            getter_name = 'senders_correspondent_53A'
        elif senders_correspondent_option == 'D':
            getter_name = 'senders_correspondent_53D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(senders_correspondent_option), 'SendersCorrespondent_53a'))
            getter_name = 'senders_correspondent_53A'  # default
        return getter_name

    # getter
    def senders_correspondent_53A(self):
        """ Returns a dictionary as {'senders_correspondent_account': value, 'senders_correspondent_bic':value} """
        values_dict = {}
        if self.use_operations_xml:
            senders_correspondent_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                     ['SWIFT',
                                                                                      'SENDERS_CORRESPONDENT_ACCOUNT'],
                                                                                     ignore_absence=True)
            senders_correspondent_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'SENDERS_CORRESPONDENT_BIC'],
                                                                                 ignore_absence=True)
            values_dict['ACCOUNT'] = senders_correspondent_account
            values_dict['BIC'] = senders_correspondent_bic
        else:
            values_dict = get_acquirer_correpondent_details(self.acm_obj)
            values_dict['ACCOUNT'] = self.acm_obj.AcquirerAccountRef().Account()
        return values_dict

    # formatter
    def _format_senders_correspondent_53A(self, val):
        """Formats the value provided by getter method"""
        senders_correspondent_account = val.get('ACCOUNT')
        senders_correspondent_bic = val.get('BIC')
        if senders_correspondent_bic:
            if senders_correspondent_account:
                val = "/" + str(senders_correspondent_account) + "\n" + str(senders_correspondent_bic)
            else:
                val = str(senders_correspondent_bic)
            return val

    # validator
    @validate_with(MT103.MT103_53A_Type)
    def _validate_senders_correspondent_53A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setsenders_correspondent_53A(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.SendersCorrespondent_A = val
        self.swift_obj.SendersCorrespondent_A.swiftTag = "53A"

    # getter
    def senders_correspondent_53D(self):
        """ Returns a dictionary as {'senders_correspondent_account': value, 'senders_correspondent_name':value, 'senders_correspondent_address':value} """
        values_dict = {}
        if self.use_operations_xml:
            senders_correspondent_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                     ['SWIFT',
                                                                                      'SENDERS_CORRESPONDENT_ACCOUNT'],
                                                                                     ignore_absence=True)
            senders_correspondent_name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT',
                                                                                                                'SENDERS_CORRESPONDENT_NAME'])
            senders_correspondent_address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                     ['SWIFT',
                                                                                      'SENDERS_CORRESPONDENT_ADDRESS'])
            values_dict['ACCOUNT'] = senders_correspondent_account
            values_dict['NAME'] = senders_correspondent_name
            values_dict['ADDRESS'] = senders_correspondent_address
            return values_dict
        else:
            return get_acquirer_correpondent_details(self.acm_obj)

    # formatter
    def _format_senders_correspondent_53D(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ACCOUNT')
        name = val.get('NAME')
        address = val.get('ADDRESS')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT103.MT103_53D_Type)
    def _validate_senders_correspondent_53D(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setsenders_correspondent_53D(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.SendersCorrespondent_D = val
        self.swift_obj.SendersCorrespondent_D.swiftTag = "53D"

    # --------------------------------- intermediary_institution -------------------------------------------

    #option_getter
    def get_intermediary_institution_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_intermediary_institution(self):
        """Returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            intermediary_institution_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                       ['SWIFT',
                                                                                        'INTERMEDIARY_INSTITUTION_OPTION'],
                                                                                       ignore_absence=True)
        else:
            intermediary_institution_option = self.get_intermediary_institution_option()
        if intermediary_institution_option == "A":
            getter_name = 'intermediary_institution_56A'
        elif intermediary_institution_option == "C":
            getter_name = 'intermediary_institution_56C'
        elif intermediary_institution_option == "D":
            getter_name = 'intermediary_institution_56D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(intermediary_institution_option), 'IntermediaryInstitution_56a'))
            getter_name = 'intermediary_institution_56A'  # default
        return getter_name

    # getter
    def intermediary_institution_56A(self):
        """ Returns a dictionary as {'intermediary_institution_account': value, 'intermediary_institution_bic':value} """
        values_dict = {}
        if self.use_operations_xml:
            intermediary_institution_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                        ['SWIFT',
                                                                                         'INTERMEDIARY_INSTITUTION_ACCOUNT'],
                                                                                        ignore_absence=True)
            intermediary_institution_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                    ['SWIFT',
                                                                                     'INTERMEDIARY_INSTITUTION_BIC'])

            values_dict['ACCOUNT'] = intermediary_institution_account
            values_dict['BIC'] = intermediary_institution_bic
            return values_dict
        else:
            return get_counterpartys_intermediary_details(self.acm_obj)

    # formatter
    def _format_intermediary_institution_56A(self, val):
        """Formats the value provided by getter method"""
        intermediary_institution_account = val.get('ACCOUNT')
        intermediary_institution_bic = val.get('BIC')
        if intermediary_institution_bic:
            if intermediary_institution_account:
                val = "/" + str(intermediary_institution_account) + "\n" + str(intermediary_institution_bic)
            else:
                val = str(intermediary_institution_bic)
            return val

    # validator
    @validate_with(MT103.MT103_56A_Type)
    def _validate_intermediary_institution_56A(self, val, swift_tag_obj=MT103.MT103_56A_Type):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setintermediary_institution_56A(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.IntermediaryInstitution_A = val
        self.swift_obj.IntermediaryInstitution_A.swiftTag = '56A'

    # getter
    def intermediary_institution_56C(self):
        """ Returns a intermediary_institution_account as string """
        if self.use_operations_xml:
            intermediary_institution_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                        ['SWIFT',
                                                                                         'INTERMEDIARY_INSTITUTION_ACCOUNT'],
                                                                                        ignore_absence=True)
        else:
            intermediary_institution_account = self.acm_obj.CounterpartyAccountRef().Account3()
        return intermediary_institution_account

    # formatter
    def _format_intermediary_institution_56C(self, val):
        """Formats the value provided by getter method"""
        if val:
            val = "/" + str(val)
            return val

    # validator
    @validate_with(MT103.MT103_56C_Type)
    def _validate_intermediary_institution_56C(self, val, swift_tag_obj=MT103.MT103_56C_Type):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setintermediary_institution_56C(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.IntermediaryInstitution_C = val
        self.swift_obj.IntermediaryInstitution_C.swiftTag = '56C'

    # getter
    def intermediary_institution_56D(self):
        """ Returns a dictionary as {'intermediary_institution_account': value, 'intermediary_institution_name':value, 'intermediary_institution_address':value} """
        values_dict = {}
        if self.use_operations_xml:
            intermediary_institution_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                        ['SWIFT',
                                                                                         'INTERMEDIARY_INSTITUTION_ACCOUNT'],
                                                                                        ignore_absence=True)
            intermediary_institution_name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                     ['SWIFT',
                                                                                      'INTERMEDIARY_INSTITUTION_NAME'])
            intermediary_institution_address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                        ['SWIFT',
                                                                                         'INTERMEDIARY_INSTITUTION_ADDRESS'])
            values_dict['ACCOUNT'] = intermediary_institution_account
            values_dict['NAME'] = intermediary_institution_name
            values_dict['ADDRESS'] = intermediary_institution_address
            return values_dict
        else:
            return get_counterpartys_intermediary_details(self.acm_obj)

    # formatter
    def _format_intermediary_institution_56D(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ACCOUNT')
        name = val.get('NAME')
        address = val.get('ADDRESS')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT103.MT103_56D_Type)
    def _validate_intermediary_institution_56D(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setintermediary_institution_56D(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.IntermediaryInstitution_D = val
        self.swift_obj.IntermediaryInstitution_D.swiftTag = '56D'

    # --------------------------------- account_with_institution -------------------------------------------

    #option_getter
    def get_account_with_institution_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_account_with_institution(self):
        """Returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            account_with_institution_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                       ['SWIFT',
                                                                                        'ACCOUNT_WITH_INSTITUTION_OPTION'],
                                                                                       ignore_absence=True)
        else:
            account_with_institution_option = self.get_account_with_institution_option()
        if account_with_institution_option == "A":
            getter_name = 'account_with_institution_57A'
        elif account_with_institution_option == "C":
            getter_name = 'account_with_institution_57C'
        elif account_with_institution_option == "D":
            getter_name = 'account_with_institution_57D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(account_with_institution_option), 'AccountWithInstitution_57a'))
            getter_name = 'account_with_institution_57A'  # default
        return getter_name

    # getter account_with_institution_57A
    # Moved to FCashSetttlementOutBase

    # formatter _format_account_with_institution_57A
    # Moved to FCashSetttlementOutBase

    # validator
    @validate_with(MT103.MT103_57A_Type)
    def _validate_account_with_institution_57A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setaccount_with_institution_57A(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.AccountWithInstitution_A = val
        self.swift_obj.AccountWithInstitution_A.swiftTag = '57A'

    # getter
    def account_with_institution_57C(self):
        """ Returns a account_with_institution as string """
        if self.use_operations_xml:
            account_with_institution_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                        ['SWIFT',
                                                                                         'ACCOUNT_WITH_INSTITUTION_ACCOUNT'],
                                                                                        ignore_absence=True)
        else:
            account_with_institution_account = self.acm_obj.CounterpartyAccountRef().Account2()  # get_account_with_institution_account(self.acm_obj)
        return account_with_institution_account

    # formatter
    def _format_account_with_institution_57C(self, val):
        """Formats the value provided by getter method"""
        if val:
            val = "/" + str(val)
            return val

    # validator
    @validate_with(MT103.MT103_57C_Type)
    def _validate_account_with_institution_57C(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setaccount_with_institution_57C(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.AccountWithInstitution_C = val
        self.swift_obj.AccountWithInstitution_C.swiftTag = '57C'

    # getter
    def account_with_institution_57D(self):
        """ Returns a dictionary as {'account_with_institution_account': value, 'account_with_institution_name':value, 'account_with_institution_address':value} """
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT',
                                                                'ACCOUNT_WITH_INSTITUTION_ACCOUNT'],
                                                               ignore_absence=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                            ['SWIFT',
                                                             'ACCOUNT_WITH_INSTITUTION_NAME'])
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT',
                                                                'ACCOUNT_WITH_INSTITUTION_ADDRESS'])
            values_dict['ACCOUNT'] = account
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            return values_dict
        else:
            return get_counterpartys_correspondent_details(self.acm_obj)

    # formatter
    def _format_account_with_institution_57D(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ACCOUNT')
        name = val.get('NAME')
        address = val.get('ADDRESS')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT103.MT103_57D_Type)
    def _validate_account_with_institution_57D(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setaccount_with_institution_57D(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.AccountWithInstitution_D = val
        self.swift_obj.AccountWithInstitution_D.swiftTag = '57D'

    # --------------------------------- beneficiary_customer -------------------------------------------

    #option_getter
    def get_beneficiary_customer_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        bic = ''
        counterparty_reference = self.acm_obj.CounterpartyAccountRef()
        if counterparty_reference and counterparty_reference.NetworkAlias():
            bic = counterparty_reference.NetworkAlias().Alias()
        if not bic and self.acm_obj.Counterparty():
            bic = self.acm_obj.Counterparty().Swift()
        if not bic:
            option = 'NO OPTION'
        return option

    # setter
    def _set_OPTION_beneficiary_customer(self):
        """Returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            beneficiary_customer_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                   ['SWIFT',
                                                                                    'BENEFICIARY_CUSTOMER_OPTION'])
        else:
            beneficiary_customer_option = self.get_beneficiary_customer_option()
        if beneficiary_customer_option == "A":
            getter_name = 'beneficiary_customer_59A'
        elif beneficiary_customer_option == "NO OPTION":
            getter_name = 'beneficiary_customer_no_option_59'
        elif beneficiary_customer_option == "F":
            getter_name = 'beneficiary_customer_59F'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(beneficiary_customer_option), 'BeneficiaryCustomer_59a'))
            getter_name = 'beneficiary_customer_59A'  # default
        return getter_name

    # getter
    def beneficiary_customer_59A(self):
        """ Returns a dictionary as {'beneficiary_customer_account': value, 'beneficiary_customer_bic':value} """
        values_dict = {}
        if self.use_operations_xml:
            beneficiary_customer_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                    ['SWIFT',
                                                                                     'BENEFICIARY_CUSTOMER_ACCOUNT'],
                                                                                    ignore_absence=True)
            beneficiary_customer_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                ['SWIFT', 'BENEFICIARY_CUSTOMER_BIC'])
            values_dict['ACCOUNT'] = beneficiary_customer_account
            values_dict['BIC'] = beneficiary_customer_bic
            return values_dict
        else:
            return get_counterparty_details(self.acm_obj)

    # formatter
    def _format_beneficiary_customer_59A(self, val):
        """Formats the value provided by getter method"""
        beneficiary_customer_account = val.get('ACCOUNT')
        beneficiary_customer_bic = val.get('BIC')
        if beneficiary_customer_bic:
            if beneficiary_customer_account:
                val = "/" + str(beneficiary_customer_account) + "\n" + str(beneficiary_customer_bic)
            else:
                val = str(beneficiary_customer_bic)
            return val
        else:
            notifier.ERROR("Inappropriate option selected. Option A is invalid.")

    # validator
    @validate_with(MT103.MT103_59A_Type)
    def _validate_beneficiary_customer_59A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setbeneficiary_customer_59A(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.BeneficiaryCustomer_A = val
        self.swift_obj.BeneficiaryCustomer_A.swiftTag = '59A'

    # getter
    def beneficiary_customer_no_option_59(self):
        """ Returns a dictionary as {'beneficiary_customer_account': value, 'beneficiary_customer_name':value, 'beneficiary_customer_address':value} """
        values_dict = {}
        if self.use_operations_xml:
            beneficiary_customer_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                    ['SWIFT',
                                                                                     'BENEFICIARY_CUSTOMER_ACCOUNT'],
                                                                                    ignore_absence=True)
            beneficiary_customer_name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'BENEFICIARY_CUSTOMER_NAME'])
            beneficiary_customer_address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                    ['SWIFT',
                                                                                     'BENEFICIARY_CUSTOMER_ADDRESS'])
            values_dict['ACCOUNT'] = beneficiary_customer_account
            values_dict['NAME'] = beneficiary_customer_name
            values_dict['ADDRESS'] = beneficiary_customer_address
            return values_dict
        else:
            return get_counterparty_details(self.acm_obj)

    # formatter
    def _format_beneficiary_customer_no_option_59(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ACCOUNT')
        name = val.get('NAME')
        address = val.get('ADDRESS')

        temp_name = name
        temp_address = address
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

        for key in list(lookup_temp.keys()):
            temp_name = temp_name.replace(str(key), lookup_temp[key] + " ")
            temp_address = temp_address.replace(str(key), lookup_temp[key] + " ")
        if name == temp_name:
            if name and address:
                name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
                address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
                val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
                if account:
                    val = "/" + str(account) + "\n" + str(val)
                return val
        else:
            name = temp_name
            address = 'ADD. ' + temp_address
            name_and_address = name + address
            split_name_and_address = FSwiftWriterUtils.split_text_logically_on_character_limit(name_and_address, 35)
            val = ('\n').join(split_name_and_address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val


    # validator
    @validate_with(MT103.MT103_59_Type)
    def _validate_beneficiary_customer_no_option_59(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setbeneficiary_customer_no_option_59(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.BeneficiaryCustomer = val
        self.swift_obj.BeneficiaryCustomer.swiftTag = '59'

    # getter
    def beneficiary_customer_59F(self):
        """ Returns a dictionary as {'beneficiary_customer_account': value, 'beneficiary_customer_name':value, 'beneficiary_customer_address':value,
        'beneficiary_customer_country_code':value, 'beneficiary_customer_town':value} """
        values_dict = {}
        if self.use_operations_xml:
            beneficiary_customer_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                    ['SWIFT',
                                                                                     'BENEFICIARY_CUSTOMER_ACCOUNT'],
                                                                                    ignore_absence=True)
            beneficiary_customer_name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'BENEFICIARY_CUSTOMER_NAME'])
            beneficiary_customer_address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                    ['SWIFT',
                                                                                     'BENEFICIARY_CUSTOMER_ADDRESS'],
                                                                                    ignore_absence=True)
            beneficiary_customer_country_code = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                         ['SWIFT',
                                                                                          'BENEFICIARY_CUSTOMER_COUNTRY_CODE'],
                                                                                         ignore_absence=True)
            beneficiary_customer_town = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'BENEFICIARY_CUSTOMER_TOWN'],
                                                                                 ignore_absence=True)

            values_dict['ACCOUNT'] = beneficiary_customer_account
            values_dict['NAME'] = beneficiary_customer_name
            values_dict['ADDRESS'] = beneficiary_customer_address
            values_dict['COUNTRY_CODE'] = beneficiary_customer_country_code
            values_dict['TOWN'] = beneficiary_customer_town
            return values_dict
        else:
            return get_counterparty_details(self.acm_obj)

    # formatter
    def _format_beneficiary_customer_59F(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ACCOUNT')
        name = val.get('NAME')
        address = val.get('ADDRESS')
        country_code = val.get('COUNTRY_CODE')
        town = val.get('TOWN')
        name_list, address_list, country_and_town_list = [], [], []

        if name:
            name_list = FSwiftWriterUtils.split_text_and_prefix(str(name), 33, '1/')
        if address:
            address_list = FSwiftWriterUtils.split_text_and_prefix(str(address), 33, '2/')
        if country_code:
            additional_details = str(country_code)
            if town:
                additional_details = str(additional_details) + '/' + str(town)
            country_and_town_list = FSwiftWriterUtils.split_text_and_prefix(
                str(additional_details), 33, '3/')
        value = FSwiftWriterUtils.allocate_space_for_name_and_address_with_constraint(name_list, address_list,
                                                                                      country_and_town_list)
        if account:
            account = '/' + str(account)
            value = account + '\n' + value
        return value

    # validator
    @validate_with(MT103.MT103_59F_Type)
    def _validate_beneficiary_customer_59F(self, val, swift_tag_obj=MT103.MT103_59F_Type):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setbeneficiary_customer_59F(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.BeneficiaryCustomer_F = val
        self.swift_obj.BeneficiaryCustomer_F.swiftTag = '59F'

    # --------------------------------- remittance_information -------------------------------------------
    # getter
    def remittance_information_70(self):
        """ Returns a remittance_information as string """
        if self.use_operations_xml:
            remittance_info = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                       ['SWIFT', 'REMITTANCE_INFO'],
                                                                       ignore_absence=True)
        else:
            remittance_info = self.get_remittance_info(self.acm_obj)
        return remittance_info

    # formatter
    def _format_remittance_information_70(self, val):
        """Formats the value provided by getter method"""
        if not self.use_operations_xml:
            val = self.format_MT103_field70(val, 35, 4)
        else:
            val = val.replace('newline', '\n')
        return str(val)

    # validator
    @validate_with(MT103.MT103_70_Type)
    def _validate_remittance_information_70(self, val):
        """validates the value provided by formatter method"""
        validate_remittance_info(val)
        return val

    # setter
    def _set_remittance_information_70(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.RemittanceInformation = val
        self.swift_obj.RemittanceInformation.swiftTag = '70'

    # --------------------------------- details_of_charges_71A -------------------------------------------
    # getter
    def details_of_charges_71A(self):
        """ Returns a details_of_charges as string """
        if self.use_operations_xml:
            details_of_charges = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'DETAILS_OF_CHARGES'])
        else:
            details_of_charges = self.get_details_of_charges(self.acm_obj)
        return details_of_charges

    # formatter
    def _format_details_of_charges_71A(self, val):
        """Formats the value provided by getter method"""
        return val

    # validator
    @validate_with(MT103.MT103_71A_Type)
    def _validate_details_of_charges_71A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _set_details_of_charges_71A(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.DetailsOfCharges = val
        self.swift_obj.DetailsOfCharges.swiftTag = '71A'

    def get_remittance_info(self, settlement):
        ''' Optional field 70 '''

        trade = settlement.Trade()
        instrument = settlement.Instrument()
        YOUR_REF = 'Your reference:'
        OUR_REF = 'Our reference:'
        code = '/INV/'
        newline = 'newline'
        info = []
        info.append(code)
        info.append(newline)
        if instrument:
            info.append('Instrument:')
            info.append(instrument.Name())
        info.append(newline)
        info.append(OUR_REF)
        if trade:
            info.append(str(trade.Oid()))
        info.append(newline)
        info.append(YOUR_REF)
        info.append(get_your_ref(settlement))
        info = ''.join(info)
        return info

    def get_details_of_charges(self, settlement):
        ''' Mandatory field 71A '''
        account = settlement.CounterpartyAccountRef()
        details = account.DetailsOfCharges()
        if details and details != 'None':
            return details
        return 'SHA'

    def format_MT103_field70(self, val, character_limit, n_lines):
        """returns formatted form of value provided"""
        text = []
        val = val.split('newline')
        for values in val:
            line = FSwiftWriterUtils.split_text_on_character_limit(values, character_limit)
            text.append(line)
        text = '\n'.join(str(i) for sub_list in text for i in sub_list)
        text = '\n'.join(text.split('\n')[:n_lines])
        return text


class FMT103OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_typ = "103"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT' + self.mt_typ)
        super(FMT103OutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

    def message_type(self):
        """returns message type"""
        return "103"

    def sender_logical_terminal_address(self):
        '''LT code is hardcoded as A for sender'''
        terminal_address = ''
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
        terminal_address = ''
        receivers_bic= ''
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'RECEIVER_BIC'])
        else:
            receivers_bic = get_receivers_bic(self.acm_obj)
        terminal_address = self.logical_terminal_address(receivers_bic, "X")
        return terminal_address

    def logical_terminal_address(self, bic_code, lt_code):
        """returns terminal address"""
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
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seqref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            seqnbr = self.acm_obj.Oid()
            seqref = get_settlement_reference_prefix()
        return "{108:%s-%s-%s-%s}" % (seqref, seqnbr, get_message_version_number(self.acm_obj), self.mt_typ[0:3])

    def service_identifier(self):
        """returns service identifier"""
        if self.use_operations_xml:
            sub_network = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                   ['SWIFT', 'SUB_NETWORK'],
                                                                   ignore_absence=True)
        else:
            sub_network = get_sub_network(self.acm_obj)
        if sub_network == "TARGET2":
            return "{103:TGT}"
        if sub_network == "EBA":
            return "{103:EBA}"
        return ''

    def banking_priority_code(self):
        """returns banking priority code"""
        banking_priority = ""
        if self.use_operations_xml:
            sub_network = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                   ['SWIFT', 'SUB_NETWORK'],
                                                                   ignore_absence=True)
            if sub_network == "TARGET2":
                banking_priority = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                   ['SWIFT', 'BANKING_PRIORITY'],
                                                                   ignore_absence=True)
        else:
            sub_network = get_sub_network(self.acm_obj)
            if sub_network == "TARGET2":
                banking_priority = get_banking_priority(self.acm_obj) #getter for BankingPriority
        if banking_priority:
            return "{113:%s}" % str(banking_priority)
        if sub_network == "EBA":
            return ""
        return ''

    def UETR(self):
        """returnd UETR"""
        ref_no = uuid.uuid4()
        return "{121:%s}" % (ref_no)

    def gpi_id(self):
        """returnd gpi id"""
        gpi_identifier = get_gpi_identifier(self.acm_obj)
        if gpi_identifier:
            return "{111:%s}" % str(gpi_identifier)


class FMT103OutBaseNetworkRules(object):
    """validation of swift message by network rules"""

    def __init__(self, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom=None):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.acm_obj = acm_obj
        self.mt_typ = "103"
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT' + self.mt_typ)

    def network_rule_C1(self):
        '''If field 33B is present and the currency code is different from the currency code in field 32A, field 36 must be present, otherwise field 36 is not allowed'''
        if self.swift_message_obj.CurrencyInstructedAmount and self.swift_message_obj.ValueDateCurrencyInterbankSettledAmount:
            currency_33B = str(self.swift_message_obj.CurrencyInstructedAmount.value())[:3]
            currency_32A = str(self.swift_message_obj.ValueDateCurrencyInterbankSettledAmount.value())[6:9]
            if currency_32A != currency_33B and not self.swift_message_obj.ExchangeRate:
                return "If field 33B is present and the currency code is different from the currency code in field 32A, field 36 must be present, otherwise field 36 is not allowed"
        return ''

    def network_rule_C2(self):
        '''If the country codes of the Sender's and the Receiver's BICs are within the following list: AD, AT, BE, BG, BV, CH, CY, CZ, \\
           DE, DK, ES, EE, FI, FR, GB, GF, GI, GP, GR, HU, IE, IS, IT, LI, LT, LU, LV, MC, MQ, MT, NL, NO, PL, PM, PT, RE, RO, SE, SI, SJ, \\
           SK, SM, TF and VA, then field 33B is mandatory, otherwise field 33B is optional '''
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'RECEIVER_BIC'])
            senders_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SENDER_BIC'])
        else:
            receivers_bic = get_receivers_bic(self.acm_obj)
            senders_bic = get_senders_bic(self.acm_obj)
        country_code = ['AD', 'AT', 'BE', 'BG', 'BV', 'CH', 'CY', 'CZ', 'DE', 'DK', 'ES', 'EE', 'FI', 'FR', 'GB', 'GF',
                        'GI', 'GP', 'GR', 'HU', 'IE', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'MC', 'MQ', 'MT', 'NL', 'NO',
                        'PL', 'PM', 'PT', 'RE', 'RO', 'SE', 'SI', 'SJ', 'SK', 'SM', 'TF', 'VA']
        if receivers_bic[4:6] in country_code and senders_bic[4:6] in country_code:
            if not self.swift_message_obj.CurrencyInstructedAmount:
                return "If the country codes of the Sender's and the Receiver's BICs are within the following list: AD, AT, BE, BG, BV, CH, CY, CZ, DE, DK, ES, EE, FI, FR, GB, GF, GI, GP, GR, HU, IE, IS, IT, LI, LT, LU, LV, MC, MQ, MT, NL, NO, PL, PM, PT, RE, RO, SE, SI, SJ, SK, SM, TF and VA, then field 33B is mandatory, otherwise field 33B is optional"
        return ""

    def network_rule_C3(self):
        '''If field 23B contains the code SPRI, field 23E may contain only the codes SDVA, TELB, PHOB, INTC.
           If field 23B contains one of the codes SSTD or SPAY, field 23E must not be used'''
        if self.swift_message_obj.BankOperationCode:
            if self.swift_message_obj.BankOperationCode.value() == 'SPRI':
                values_of_23E = [each.value() for each in self.swift_message_obj.InstructionCode]
                for each in values_of_23E:
                    if each not in ['SDVA', 'TELB', 'PHOB', 'INTC']:
                        return "If field 23B contains the code SPRI, field 23E may contain only the codes SDVA, TELB, PHOB, INTC"
            if self.swift_message_obj.BankOperationCode.value() in ['SSTD', 'SPAY']:
                if self.swift_message_obj.InstructionCode:
                    return "If field 23B contains one of the codes SSTD or SPAY, field 23E must not be used"
        return ""

    def network_rule_C4(self):
        '''If field 23B contains one of the codes SPRI, SSTD or SPAY, field 53a must not be used with option D'''
        if self.swift_message_obj.BankOperationCode:
            if self.swift_message_obj.BankOperationCode.value() in ['SPRI', 'SSTD', 'SPAY']:
                if self.swift_message_obj.SendersCorrespondent_D:
                    return "If field 23B contains one of the codes SPRI, SSTD or SPAY, field 53a must not be used with option D"
        return ""

    def network_rule_C5(self):
        '''If field 23B contains one of the codes SPRI, SSTD or SPAY and field 53a is present with option B, Party Identifier must be present in field 53B'''
        if self.swift_message_obj.BankOperationCode:
            if self.swift_message_obj.BankOperationCode.value() in ['SPRI', 'SSTD',
                                                                    'SPAY'] and self.swift_message_obj.SendersCorrespondent_B:
                party_identifier, location = str(self.swift_message_obj.SendersCorrespondent_B.value()).split('\n')
                if not party_identifier:
                    return "If field 23B contains one of the codes SPRI, SSTD or SPAY and field 53a is present with option B, Party Identifier must be present in field 53B"
        return ""

    def network_rule_C6(self):
        if self.swift_message_obj.BankOperationCode:
            if self.swift_message_obj.BankOperationCode.value() in ['SPRI', 'SSTD',
                                                                    'SPAY'] and not self.swift_message_obj.ReceiversCorrespondent_A:
                return "If field 23B contains one of the codes SPRI, SSTD or SPAY, field 54a may be used with option A only"
        return ""

    def network_rule_C7(self):
        if self.swift_message_obj.ThirdReimbursementInstitution_A or self.swift_message_obj.ThirdReimbursementInstitution_B or self.swift_message_obj.ThirdReimbursementInstitution_D:
            is_field_53a_present = (
                self.swift_message_obj.SendersCorrespondent_A or self.swift_message_obj.SendersCorrespondent_B or self.swift_message_obj.SendersCorrespondent_D)
            is_field_54a_present = (
                self.swift_message_obj.ReceiversCorrespondent_A or self.swift_message_obj.ReceiversCorrespondent_B or self.swift_message_obj.ReceiversCorrespondent_D)
            if not is_field_53a_present or not is_field_54a_present:
                return "If field 55a is present, then both fields 53a and 54a must also be present"
        return ""

    def network_rule_C8(self):
        '''If field 23B contains one of the codes SPRI, SSTD or SPAY, field 55a may be used with option A only'''
        if self.swift_message_obj.BankOperationCode:
            if self.swift_message_obj.BankOperationCode.value() in ['SPRI', 'SSTD',
                                                                    'SPAY'] and not self.swift_message_obj.ThirdReimbursementInstitution_A:
                return "If field 23B contains one of the codes SPRI, SSTD or SPAY, field 55a may be used with option A only"
        return ""

    def network_rule_C9(self):
        '''If field 56a is present, field 57a must also be present'''
        is_field_56a_present = (
            self.swift_message_obj.IntermediaryInstitution_A or self.swift_message_obj.IntermediaryInstitution_C or self.swift_message_obj.IntermediaryInstitution_D)
        is_field_57a_present = (
            self.swift_message_obj.AccountWithInstitution_A or self.swift_message_obj.AccountWithInstitution_B or self.swift_message_obj.AccountWithInstitution_C or self.swift_message_obj.AccountWithInstitution_D)
        if is_field_56a_present and not is_field_57a_present:
            return "If field 56a is present, field 57a must also be present"
        return ""

    def network_rule_C10(self):
        '''If field 23B contains the code SPRI, field 56a must not be present.
           If field 23B contains one of the codes SSTD or SPAY, field 56a may be used with either option A or option C.

           If option C is used, it must contain a clearing code- This part is not implemented/supported'''
        if self.swift_message_obj.BankOperationCode and self.swift_message_obj.BankOperationCode.value() == "SPRI":
            is_field_56a_present = (
                self.swift_message_obj.IntermediaryInstitution_A or self.swift_message_obj.IntermediaryInstitution_C or self.swift_message_obj.IntermediaryInstitution_D)
            if is_field_56a_present:
                return "If field 23B contains the code SPRI, field 56a must not be present."
        if self.swift_message_obj.BankOperationCode and self.swift_message_obj.BankOperationCode.value() in ['SSTD',
                                                                                                             'SPAY']:
            is_field_56A_and56C_present = (
                self.swift_message_obj.IntermediaryInstitution_A or self.swift_message_obj.IntermediaryInstitution_C)
            if not is_field_56A_and56C_present:
                return "If field 23B contains one of the codes SSTD or SPAY, field 56a may be used with either option A or option C"
        # If option C is used, it must contain a clearing code- This part is not implemented/supported because of unclear understanding
        return ""

    def network_rule_C11(self):
        '''If field 23B contains one of the codes SPRI, SSTD or SPAY,
           field 57a may be used with option A, option C or option D. Subfield 1 (Party Identifier) in option D must be present'''
        if self.swift_message_obj.BankOperationCode:
            if self.swift_message_obj.BankOperationCode.value() in ['SPRI', 'SSTD', 'SPAY']:
                is_field_57A_57C_57D_present = (
                    self.swift_message_obj.AccountWithInstitution_A or self.swift_message_obj.AccountWithInstitution_C or self.swift_message_obj.AccountWithInstitution_D)
                if not is_field_57A_57C_57D_present:
                    return "If field 23B contains one of the codes SPRI, SSTD or SPAY, field 57a may be used with option A, option C or option D."
                if self.swift_message_obj.AccountWithInstitution_D:
                    party_identifier, name_and_address = str(
                        self.swift_message_obj.AccountWithInstitution_D.value()).split('\n')
                    if not party_identifier:
                        return "If field 23B contains one of the codes SPRI, SSTD or SPAY, field 57a may be used with option A, option C or option D. Subfield 1 (Party Identifier) in option D must be present"
        return ""

    def network_rule_C12(self):
        '''If field 23B contains one of the codes SPRI, SSTD or SPAY, subfield 1 (Account) in field 59a Beneficiary Customer is mandatory'''
        if self.swift_message_obj.BankOperationCode:
            if self.swift_message_obj.BankOperationCode.value() in ['SPRI', 'SSTD', 'SPAY']:
                field_59a = [each for each in
                             [self.swift_message_obj.BeneficiaryCustomer, self.swift_message_obj.BeneficiaryCustomer_A,
                              self.swift_message_obj.BeneficiaryCustomer_F] if each != None]
                field_59a_value = field_59a[0].value()
                try:
                    if len(field_59a_value.split('\n')[0]) <= 0:
                        return "If field 23B contains one of the codes SPRI, SSTD or SPAY, subfield 1 (Account) in field 59a Beneficiary Customer is mandatory"
                except Exception as e:
                    return "If field 23B contains one of the codes SPRI, SSTD or SPAY, subfield 1 (Account) in field 59a Beneficiary Customer is mandatory"
        return ""

    def network_rule_C13(self):
        '''If any field 23E contains the code CHQB, subfield 1 (Account) in field 59a Beneficiary Customer is not allowed'''
        instruction_code_contains_CHQB = 'CHQB' in [each.value() for each in self.swift_message_obj.InstructionCode]
        if instruction_code_contains_CHQB:
            field_59a = [each for each in
                         [self.swift_message_obj.BeneficiaryCustomer, self.swift_message_obj.BeneficiaryCustomer_A,
                          self.swift_message_obj.BeneficiaryCustomer_F] if each != None]
            field_59a_value = field_59a[0].value()
            try:
                if len(field_59a_value.split('\n')[0]) > 0:
                    return "If any field 23E contains the code CHQB, subfield 1 (Account) in field 59a Beneficiary Customer is not allowed"
            except Exception as e:
                return "If any field 23E contains the code CHQB, subfield 1 (Account) in field 59a Beneficiary Customer is not allowed"
        return ""

    def network_rule_C14(self):
        '''If field 71A contains OUR, then field 71F is not allowed and field 71G is optional
           If field 71A contains SHA, then field(s) 71F is(are) optional and field 71G is not allowed
           If field 71A contains BEN, then at least one occurrence of field 71F is mandatory and field 71G is not allowed'''

        if self.swift_message_obj.DetailsOfCharges:
            is_field_71F_present = self.swift_message_obj.SendersCharges and len(
                self.swift_message_obj.SendersCharges) > 0
            is_field_71G_present = self.swift_message_obj.ReceiversCharges
            if self.swift_message_obj.DetailsOfCharges.value() == 'OUR':
                if is_field_71F_present:
                    return "If field 71A contains OUR, then field 71F is not allowed and field 71G is optional"
            if self.swift_message_obj.DetailsOfCharges.value() == 'SHA':
                if is_field_71G_present:
                    return "If field 71A contains SHA, then field(s) 71F is(are) optional and field 71G is not allowed"
            if self.swift_message_obj.DetailsOfCharges.value() == 'BEN':
                if is_field_71G_present or not is_field_71F_present:
                    return "If field 71A contains BEN, then at least one occurrence of field 71F is mandatory and field 71G is not allowed"
        return ""

    def network_rule_C15(self):
        '''If either field 71F (at least one occurrence) or field 71G is present, then field 33B is mandatory, otherwise field 33B is optional'''
        is_field_71F_present = self.swift_message_obj.SendersCharges and len(self.swift_message_obj.SendersCharges) > 0
        is_field_71G_present = self.swift_message_obj.ReceiversCharges
        is_field_33B_present = self.swift_message_obj.CurrencyInstructedAmount
        if (is_field_71F_present or is_field_71G_present) and not is_field_33B_present:
            return "If either field 71F (at least one occurrence) or field 71G is present, then field 33B is mandatory, otherwise field 33B is optional"
        return ""

    def network_rule_C16(self):
        '''If field 56a is not present, no field 23E may contain TELI or PHOI'''
        is_field_56a_present = (
            self.swift_message_obj.IntermediaryInstitution_A or self.swift_message_obj.IntermediaryInstitution_C or self.swift_message_obj.IntermediaryInstitution_D)
        if not is_field_56a_present:
            field_23E_values = [each.value() for each in self.swift_message_obj.InstructionCode]
            if 'TELI' in field_23E_values or 'PHOI' in field_23E_values:
                return "If field 56a is not present, no field 23E may contain TELI or PHOI"
        return ""

    def network_rule_C17(self):
        '''If field 57a is not present, no field 23E may contain TELE or PHON'''
        is_field_57a_present = (
            self.swift_message_obj.AccountWithInstitution_A or self.swift_message_obj.AccountWithInstitution_B or self.swift_message_obj.AccountWithInstitution_C or self.swift_message_obj.AccountWithInstitution_D)
        if not is_field_57a_present:
            field_23E_values = [each.value() for each in self.swift_message_obj.InstructionCode]
            if 'TELE' in field_23E_values or 'PHON' in field_23E_values:
                return "If field 57a is not present, no field 23E may contain TELE or PHON"
        return ""

    def network_rule_C18(self):
        '''The currency code in the fields 71G and 32A must be the same'''
        if self.swift_message_obj.ReceiversCharges and self.swift_message_obj.ValueDateCurrencyInterbankSettledAmount:
            currency_code_in_field_71G = str(self.swift_message_obj.ReceiversCharges.value())[0:3]
            currency_code_in_field_32A = str(self.swift_message_obj.ValueDateCurrencyInterbankSettledAmount.value())[
                                         6:9]
            if currency_code_in_field_32A != currency_code_in_field_71G:
                return "The currency code in the fields 71G and 32A must be the same"
        return ""

