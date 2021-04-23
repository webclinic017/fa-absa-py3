"""----------------------------------------------------------------------------
MODULE:
    FMT202OutBase

DESCRIPTION:
    This module provides the base class for the FMT202 outgoing implementation

CLASS:
    FMT200Base

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftMLUtils
import FSwiftWriterMessageHeader
import MT202
from FCashOutUtils import *
from FInstitutionTransfersOutBase import FInstitutionTransfersOutBase
from FSwiftWriterEngine import validate_with, should_use_operations_xml
import uuid
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

class FMT202Base(FInstitutionTransfersOutBase):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = 'MT202'
        super(FMT202Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # Implementing it to pass the NotImplementedError
    def _message_sequences(self):
        pass

    # getter
    # Moved to FInstitutionTransfersOutBase

    # formatter
    # Moved to FInstitutionTransfersOutBase


    # validator
    @validate_with(MT202.MT202_20_Type)
    def _validate_transaction_reference_20(self, transaction_reference):
        """validates the value provided by formatter method"""
        validate_slash_and_double_slash(transaction_reference, "Transaction Reference")
        return transaction_reference

    # setter
    def _set_transaction_reference_20(self, transaction_reference):
        """sets the value on python object"""
        self.swift_obj.TransactionReferenceNumber = transaction_reference
        self.swift_obj.TransactionReferenceNumber.swiftTag = "20"

    # getter
    def related_reference_21(self):
        """ Returns related_reference as String"""
        if self.use_operations_xml:
            return FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'YOUR_REFERENCE'])
        else:
            trade = self.acm_obj.Trade()
            if is_netted_settlement(self.acm_obj):
                trade = get_least_net_trade(self.acm_obj)
            if trade != None:
                if trade.YourRef():
                    return trade.YourRef()[:16]
            return 'NONREF'

    # formatter
    def _format_related_reference_21(self, related_reference):
        """Formats the value provided by getter method"""
        return related_reference

    # validator
    @validate_with(MT202.MT202_21_Type)
    def _validate_related_reference_21(self, related_reference):
        """validates the value provided by formatter method"""
        validate_slash_and_double_slash(related_reference, "Related Reference")
        return related_reference

    # setter
    def _set_related_reference_21(self, related_reference):
        """sets the value on python object"""
        self.swift_obj.RelatedReference = related_reference
        self.swift_obj.RelatedReference.swiftTag = "21"

    # getter
    # Moved to FInstitutionTransfersOutBase

    # formatter
    # Moved to FInstitutionTransfersOutBase

    # validator
    @validate_with(MT202.MT202_32A_Type)
    def _validate_date_currency_amount_32A(self, date_currency_amount):
        """validates the value provided by formatter method"""
        validate_currency_amount(date_currency_amount, "Date Currency Amount")
        amount = get_amount_from_currency_amount(date_currency_amount)
        validateAmount(amount.replace('.', ','), 15, "Date Currency Amount")
        return date_currency_amount

    # setter
    def _set_date_currency_amount_32A(self, date_currency_amount):
        """sets the value on python object"""
        self.swift_obj.ValueDateCurrencyCodeAmount = date_currency_amount
        self.swift_obj.ValueDateCurrencyCodeAmount.swiftTag = "32A"

    #option_getter
    def get_ordering_institution_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_ordering_institution(self):
        """returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            ordering_institution_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                   ['SWIFT',
                                                                                    'ORDERING_INSTITUTION_OPTION'],
                                                                                   ignore_absence=True)
        else:
            ordering_institution_option = self.get_ordering_institution_option()
        if ordering_institution_option == 'A':
            getter_name = 'ordering_institution_52A'
        if ordering_institution_option == 'D':
            getter_name = 'ordering_institution_52D'
        return getter_name

    # getter
    def ordering_institution_52A(self):
        """ Returns dictionary as {'ACCOUNT':<value>, 'BIC':<value>}"""
        if self.use_operations_xml:
            values_dict = {}
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
            return get_acquirer_details(self.acm_obj)

    # formatter
    def _format_ordering_institution_52A(self, ord_inst_details):
        """Formats the value provided by getter method"""
        ordering_institution_account = ord_inst_details.get('ACCOUNT')
        ordering_institution_bic = ord_inst_details.get('BIC')
        if ordering_institution_bic:
            if ordering_institution_account:
                ordering_inst_value = "/" + str(ordering_institution_account) + "\n" + str(ordering_institution_bic)
            else:
                ordering_inst_value = str(ordering_institution_bic)
            return ordering_inst_value

    # validator
    @validate_with(MT202.MT202_52A_Type)
    def _validate_ordering_institution_52A(self, ordering_inst_value):
        """validates the value provided by formatter method"""
        return ordering_inst_value

    # setter
    def _setordering_institution_52A(self, ordering_inst_value):
        """sets the value on python object"""
        self.swift_obj.OrderingInstitution_A = ordering_inst_value
        self.swift_obj.OrderingInstitution_A.swiftTag = "52A"

    # getter
    def ordering_institution_52D(self):
        """ Returns dictionary as {'ACCOUNT':<value>, 'NAME':<value>, 'ADDRESS':<value>}"""
        if self.use_operations_xml:
            values_dict = {}
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
    def _format_ordering_institution_52D(self, ord_inst_details):
        """Formats the value provided by getter method"""
        account = ord_inst_details.get('ACCOUNT')
        name = ord_inst_details.get('NAME')
        address = ord_inst_details.get('ADDRESS')

        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            ordering_inst_value = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                ordering_inst_value = "/" + str(account) + "\n" + str(ordering_inst_value)
            return ordering_inst_value

    # validator
    @validate_with(MT202.MT202_52D_Type)
    def _validate_ordering_institution_52D(self, ordering_inst_value):
        """validates the value provided by formatter method"""
        return ordering_inst_value

    # setter
    def _setordering_institution_52D(self, ordering_inst_value):
        """sets the value on python object"""
        self.swift_obj.OrderingInstitution_D = ordering_inst_value
        self.swift_obj.OrderingInstitution_D.swiftTag = "52D"

    #option_getter
    def get_senders_correspondent_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_senders_correspondent(self):
        """returns name of the getter method"""
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
        if senders_correspondent_option == 'D':
            getter_name = 'senders_correspondent_53D'
        return getter_name

    # getter
    def senders_correspondent_53A(self):
        """ Returns dictionary as {'ACCOUNT':<value>, 'BIC':<value>}"""
        if self.use_operations_xml:
            values_dict = {}
            senders_correspondent_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                     ['SWIFT',
                                                                                      'SENDERS_CORRESPONDENT_ACCOUNT'],
                                                                                     ignore_absence=True)
            senders_correspondent_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'SENDERS_CORRESPONDENT_BIC'])
            values_dict['ACCOUNT'] = senders_correspondent_account
            values_dict['BIC'] = senders_correspondent_bic
            return values_dict
        else:
            return get_acquirer_correpondent_details(self.acm_obj)

    # formatter
    def _format_senders_correspondent_53A(self, sender_corr_details):
        """Formats the value provided by getter method"""
        senders_correspondent_account = sender_corr_details.get('ACCOUNT')
        senders_correspondent_bic = sender_corr_details.get('BIC')
        if senders_correspondent_bic:
            if senders_correspondent_account:
                sender_corr = "/" + str(senders_correspondent_account) + "\n" + str(senders_correspondent_bic)
            else:
                sender_corr = str(senders_correspondent_bic)
            return sender_corr

    # validator
    @validate_with(MT202.MT202_53A_Type)
    def _validate_senders_correspondent_53A(self, sender_corr):
        """validates the value provided by formatter method"""
        return sender_corr

    # setter
    def _setsenders_correspondent_53A(self, sender_corr):
        """sets the value on python object"""
        self.swift_obj.SendersCorrespondent_A = sender_corr
        self.swift_obj.SendersCorrespondent_A.swiftTag = "53A"

    # getter
    def senders_correspondent_53D(self):
        """ Returns dictionary as {'ACCOUNT':<value>, 'NAME':<value>, 'ADDRESS':<value>}"""
        if self.use_operations_xml:
            values_dict = {}
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
    def _format_senders_correspondent_53D(self, sender_corr_details):
        """Formats the value provided by getter method"""
        account = sender_corr_details.get('ACCOUNT')
        name = sender_corr_details.get('NAME')
        address = sender_corr_details.get('ADDRESS')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            sender_corr = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                sender_corr = "/" + str(account) + "\n" + str(sender_corr)
            return sender_corr

    # validator
    @validate_with(MT202.MT202_53D_Type)
    def _validate_senders_correspondent_53D(self, sender_corr):
        """validates the value provided by formatter method"""
        return sender_corr

    # setter
    def _setsenders_correspondent_53D(self, sender_corr):
        """sets the value on python object"""
        self.swift_obj.SendersCorrespondent_D = sender_corr
        self.swift_obj.SendersCorrespondent_D.swiftTag = "53D"

    #option_getter
    def get_intermediary_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_intermediary(self):
        """returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            intermediary_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'INTERMEDIARY_OPTION'],
                                                                           ignore_absence=True)
        else:
            intermediary_option = self.get_intermediary_option()
        if intermediary_option == 'A':
            getter_name = 'intermediary_56A'
        if intermediary_option == 'D':
            getter_name = 'intermediary_56D'
        return getter_name

    # getter
    # Moved to FInstitutionTransfersOutBase

    # formatter
    # Moved to FInstitutionTransfersOutBase

    # validator
    @validate_with(MT202.MT202_56A_Type)
    def _validate_intermediary_56A(self, intermediary):
        """validates the value provided by formatter method"""
        return intermediary

    # setter
    def _setintermediary_56A(self, intermediary):
        """sets the value on python object"""
        self.swift_obj.Intermedairy_A = intermediary
        self.swift_obj.Intermedairy_A.swiftTag = "56A"

    # getter
    def intermediary_56D(self):
        """ Returns dictionary as {'ACCOUNT':<value>, 'NAME':<value>, 'ADDRESS':<value>}"""
        if self.use_operations_xml:
            values_dict = {}
            intermediary_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                            ['SWIFT', 'INTERMEDIARY_ACCOUNT'],
                                                                            ignore_absence=True)
            intermediary_name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'INTERMEDIARY_NAME'])
            intermediary_address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                            ['SWIFT', 'INTERMEDIARY_ADDRESS'])
            values_dict['ACCOUNT'] = intermediary_account
            values_dict['NAME'] = intermediary_name
            values_dict['ADDRESS'] = intermediary_address
            return values_dict
        else:
            return get_counterpartys_intermediary_details(self.acm_obj)

    # formatter
    def _format_intermediary_56D(self, intermediary_details):
        """Formats the value provided by getter method"""
        account = intermediary_details.get('ACCOUNT')
        name = intermediary_details.get('NAME')
        address = intermediary_details.get('ADDRESS')

        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            intermediary = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                intermediary = "/" + str(account) + "\n" + str(intermediary)
            return intermediary

    # validator
    @validate_with(MT202.MT202_56D_Type)
    def _validate_intermediary_56D(self, intermediary):
        """validates the value provided by formatter method"""
        return intermediary

    # setter
    def _setintermediary_56D(self, intermediary):
        """sets the value on python object"""
        self.swift_obj.Intermedairy_D = intermediary
        self.swift_obj.Intermedairy_D.swiftTag = "56D"

    #option_getter
    def get_account_with_institution_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_account_with_institution(self):
        """returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            account_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_OPTION'],
                                                                      ignore_absence=True)
        else:
            account_option = self.get_account_with_institution_option()
        if account_option == 'A':
            getter_name = 'account_with_institution_57A'
        if account_option == 'D':
            getter_name = 'account_with_institution_57D'
        return getter_name

    # getter
    # Moved to FInstitutionTransfersOutBase

    # formatter
    def _format_account_with_institution_57A(self, acct_with_inst_details):
        """Formats the value provided by getter method"""
        bic = acct_with_inst_details.get('BIC')
        if bic:
            return str(bic)

    # validator
    @validate_with(MT202.MT202_57A_Type)
    def _validate_account_with_institution_57A(self, acct_with_inst):
        """validates the value provided by formatter method"""
        return acct_with_inst

    # setter
    def _setaccount_with_institution_57A(self, acct_with_inst):
        """sets the value on python object"""
        self.swift_obj.AccountWithInstitution_A = acct_with_inst
        self.swift_obj.AccountWithInstitution_A.swiftTag = "57A"

    # getter
    def account_with_institution_57D(self):
        """ Returns dictionary as {'ACCOUNT':<value>, 'NAME':<value>, 'ADDRESS':<value>}"""
        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_ACCOUNT'],
                                                               ignore_absence=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                            ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_NAME'])
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_ADDRESS'])
            values_dict['ACCOUNT'] = account
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            return values_dict
        else:
            return get_counterpartys_correspondent_details(self.acm_obj)

    # formatter
    def _format_account_with_institution_57D(self, acct_with_inst_details):
        """Formats the value provided by getter method"""
        account = acct_with_inst_details.get('ACCOUNT')
        name = acct_with_inst_details.get('NAME')
        address = acct_with_inst_details.get('ADDRESS')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            acct_with_inst = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                acct_with_inst = "/" + str(account) + "\n" + str(acct_with_inst)
            return acct_with_inst

    # validator
    @validate_with(MT202.MT202_57D_Type)
    def _validate_account_with_institution_57D(self, acct_with_inst):
        """validates the value provided by formatter method"""
        return acct_with_inst

    # setter
    def _setaccount_with_institution_57D(self, acct_with_inst):
        """sets the value on python object"""
        self.swift_obj.AccountWithInstitution_D = acct_with_inst
        self.swift_obj.AccountWithInstitution_D.swiftTag = "57D"

    #option_getter
    def get_beneficiary_institution_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_beneficiary_institution(self):
        """returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            beneficiary_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'BENEFICIARY_INSTITUTION_OPTION'])
        else:
            beneficiary_option = self.get_beneficiary_institution_option()
        if beneficiary_option == 'A':
            getter_name = 'beneficiary_institution_58A'
        if beneficiary_option == 'D':
            getter_name = 'beneficiary_institution_58D'
        return getter_name

    # getter
    def beneficiary_institution_58A(self):
        """ Returns dictionary as {'ACCOUNT':<value>, 'BIC':<value>}"""
        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'BENEFICIARY_INSTITUTION_ACCOUNT'],
                                                               ignore_absence=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'BENEFICIARY_INSTITUTION_BIC'])
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            val = get_counterparty_details(self.acm_obj)
            return val

    # formatter
    def _format_beneficiary_institution_58A(self, beneficiary_inst_details):
        """Formats the value provided by getter method"""
        account = beneficiary_inst_details.get('ACCOUNT')
        bic = beneficiary_inst_details.get('BIC')
        if bic:
            if account:
                beneficiary_inst = "/" + str(account) + "\n" + str(bic)
            else:
                beneficiary_inst = str(bic)
            return beneficiary_inst

    # validator
    @validate_with(MT202.MT202_58A_Type)
    def _validate_beneficiary_institution_58A(self, beneficiary_inst):
        """validates the value provided by formatter method"""
        return beneficiary_inst

    # setter
    def _setbeneficiary_institution_58A(self, beneficiary_inst):
        """sets the value on python object"""
        self.swift_obj.BeneficiaryInstitution_A = beneficiary_inst
        self.swift_obj.BeneficiaryInstitution_A.swiftTag = "58A"

    # getter
    def beneficiary_institution_58D(self):
        """ Returns dictionary as {'ACCOUNT':<value>, 'NAME':<value>, 'ADDRESS':<value>}"""
        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'BENEFICIARY_INSTITUTION_ACCOUNT'],
                                                               ignore_absence=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                            ['SWIFT', 'BENEFICIARY_INSTITUTION_NAME'])
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'BENEFICIARY_INSTITUTION_ADDRESS'])
            values_dict['ACCOUNT'] = account
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            return values_dict
        else:
            beneficiary_inst_details = get_counterparty_details(self.acm_obj)
            counterparty_corr_details = get_counterpartys_correspondent_details(self.acm_obj)
            beneficiary_inst_details['BENEFICIARY_INST_NAME'] = counterparty_corr_details['NAME']
            beneficiary_inst_details['BENEFICIARY_INST_ADDRESS'] = counterparty_corr_details['ADDRESS']
            return beneficiary_inst_details

    # formatter
    def _format_beneficiary_institution_58D(self, beneficiary_inst_details):
        """Formats the value provided by getter method"""
        account = beneficiary_inst_details.get('ACCOUNT')
        name = beneficiary_inst_details.get('BENEFICIARY_INST_NAME')
        address = beneficiary_inst_details.get('BENEFICIARY_INST_ADDRESS')

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
                name_and_add = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
                if account:
                    name_and_add = "/" + str(account) + "\n" + str(name_and_add)
                return name_and_add
        else:
            name = temp_name
            address = 'ADD. ' + temp_address
            name_and_address = name + address
            split_name_and_address = FSwiftWriterUtils.split_text_logically_on_character_limit(name_and_address, 35)
            name_address = ('\n').join(split_name_and_address)
            if account:
                name_address = "/" + str(account) + "\n" + str(name_address)
            return name_address

    # validator
    @validate_with(MT202.MT202_58D_Type)
    def _validate_beneficiary_institution_58D(self, beneficiary_inst):
        """validates the value provided by formatter method"""
        return beneficiary_inst

    # setter
    def _setbeneficiary_institution_58D(self, beneficiary_inst):
        """sets the value on python object"""
        self.swift_obj.BeneficiaryInstitution_D = beneficiary_inst
        self.swift_obj.BeneficiaryInstitution_D.swiftTag = "58D"


class FMT202OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_typ = "202"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT' + self.mt_typ)
        super(FMT202OutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

    def message_type(self):
        """returns type of message"""
        return "202"

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
        receivers_bic = ''
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'RECEIVER_BIC'])
        else:
            receivers_bic = get_receivers_bic(self.acm_obj)
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
        """retuens input or output"""
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
                                                                   ['SWIFT', 'SUB_NETWORK'], ignore_absence=True)
            if sub_network == "TARGET2":
                return "{103:TGT}"
            if sub_network == "EBA":
                return "{103:EBA}"
        else:
            service_code = get_swift_service_code(self.acm_obj)
            if service_code:
                return "{103:%s}" % service_code
        return ''

    def banking_priority_code(self):
        """returns banking priority code"""
        if self.use_operations_xml:
            sub_network = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                   ['SWIFT', 'SUB_NETWORK'], ignore_absence=True)
            if sub_network == "TARGET2":
                banking_priority = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                            ['SWIFT', 'BANKING_PRIORITY'])
                return "{113:%s}" % str(banking_priority)
            if sub_network == "EBA":
                return ""
        else:
            banking_priority = get_banking_priority(self.acm_obj)
            if banking_priority:
                return "{113:%s}" % str(banking_priority)
        return ''

    def UETR(self):
        """returns UETR"""
        ref_no = uuid.uuid4()
        return "{121:%s}" % (ref_no)

    def gpi_id(self):
        """returns gpi id"""
        gpi_identifier = get_gpi_identifier(self.acm_obj)
        if gpi_identifier:
            return "{111:%s}" % str(gpi_identifier)

class FMT202OutBaseNetworkRules(object):
    """validation of swift message by network rules"""

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.acm_obj = acm_obj

    def network_rule_C1(self):
        ''' If field 56a is present, then field 57a must also be present'''
        is_field_56a_present = self.swift_message_obj.Intermedairy_A or self.swift_message_obj.Intermedairy_D
        is_field_57a_present = self.swift_message_obj.AccountWithInstitution_A or self.swift_message_obj.AccountWithInstitution_D or self.swift_message_obj.AccountWithInstitution_B
        if is_field_56a_present:
            if not is_field_57a_present:
                return 'If field 56a is present, then field 57a must also be present'
        return ''

