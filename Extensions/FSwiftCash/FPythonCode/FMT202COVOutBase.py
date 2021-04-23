"""----------------------------------------------------------------------------
MODULE:
    FMT202COVOutBase

DESCRIPTION:
    This module provides the base class for the FMT202COV outgoing implementation

CLASS:
    FMT200COVBase

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftMLUtils
import FSwiftWriterMessageHeader
import MT202COV
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

class FMT202COVBase(FInstitutionTransfersOutBase):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = 'MT202COV'
        super(FMT202COVBase, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # Implementing it to pass the NotImplementedError
    def _message_sequences(self):
        """Sets the sequences on the pyxb object for MT202COV"""
        self.swift_obj.SequenceA_GeneralInformation = MT202COV.MT202COV_SequenceA_GeneralInformation()
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails = MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails()

    # getter
    # Moved to FInstitutionTransfersOutBase

    # formatter
    # Moved to FInstitutionTransfersOutBase


    # validator
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_20_Type)
    def _validate_transaction_reference_20(self, val):
        """validates the value provided by formatter method"""
        validate_slash_and_double_slash(val, "Transaction Reference")
        return val

    # setter
    def _set_transaction_reference_20(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.TransactionReferenceNumber = val
        self.swift_obj.SequenceA_GeneralInformation.TransactionReferenceNumber.swiftTag = "20"

    # getter
    def related_reference_21(self):
        """ Returns related_reference as String"""
        if self.use_operations_xml:
            return FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'YOUR_REFERENCE'])
        else:
            settlement = self.acm_obj
            related_reference = ''
            try:
                if settlement.ExternalObjects():
                    for ext_obj in settlement.ExternalObjects():
                        mt_type = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(ext_obj)
                        mt_msg = FSwiftMLUtils.FSwiftExternalObject.get_stored_data(ext_obj, 'swift_data')
                        if str(mt_type) == 'MT103':
                            related_reference = FSwiftMLUtils.get_field_value(mt_msg, '20')
                else:
                    swift_message, mt_py_object, exceptions, getter_values = FSwiftWriterUtils.generate_swift_message(settlement, 'MT103')
                    related_reference = FSwiftMLUtils.get_field_value(swift_message, '20')
                return related_reference
            except Exception as e:
                notifier.WARN("Unable to get related reference")
            return 'NONREF'

    # formatter
    def _format_related_reference_21(self, val):
        """Formats the value provided by getter method"""
        return val

    # validator
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_21_Type)
    def _validate_related_reference_21(self, val):
        """validates the value provided by formatter method"""
        validate_slash_and_double_slash(val, "Related Reference")
        return val

    # setter
    def _set_related_reference_21(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.RelatedReference = val
        self.swift_obj.SequenceA_GeneralInformation.RelatedReference.swiftTag = "21"

    # getter
    # Moved to FInstitutionTransfersOutBase

    # formatter
    # Moved to FInstitutionTransfersOutBase

    # validator
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_32A_Type)
    def _validate_date_currency_amount_32A(self, val):
        """validates the value provided by formatter method"""
        validate_currency_amount(val, "Date Currency Amount")
        amount = get_amount_from_currency_amount(val)
        validateAmount(amount.replace('.', ','), 15, "Date Currency Amount")
        return val

    # setter
    def _set_date_currency_amount_32A(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.DateCurrencyAmount = val
        self.swift_obj.SequenceA_GeneralInformation.DateCurrencyAmount.swiftTag = "32A"

    #option_getter
    def get_ordering_institution_sequenceA_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_ordering_institution_sequenceA(self):
        """returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            ordering_institution_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                   ['SWIFT',
                                                                                    'ORDERING_INSTITUTION_OPTION'],
                                                                                   ignore_absence=True)
        else:
            ordering_institution_option = self.get_ordering_institution_sequenceA_option()
        if ordering_institution_option == 'A':
            getter_name = 'ordering_institution_52A_sequenceA'
        if ordering_institution_option == 'D':
            getter_name = 'ordering_institution_52D_sequenceA'
        return getter_name

    # getter
    def ordering_institution_52A_sequenceA(self):
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
    def _format_ordering_institution_52A_sequenceA(self, val):
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
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_52A_Type)
    def _validate_ordering_institution_52A_sequenceA(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_institution_52A_sequenceA(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.OrderingInstitution_A = val
        self.swift_obj.SequenceA_GeneralInformation.OrderingInstitution_A.swiftTag = "52A"

    # getter
    def ordering_institution_52D_sequenceA(self):
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
    def _format_ordering_institution_52D_sequenceA(self, val):
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
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_52D_Type)
    def _validate_ordering_institution_52D_sequenceA(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_institution_52D_sequenceA(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.OrderingInstitution_D = val
        self.swift_obj.SequenceA_GeneralInformation.OrderingInstitution_D.swiftTag = "52D"

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
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_53A_Type)
    def _validate_senders_correspondent_53A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setsenders_correspondent_53A(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.SendersCorrespondent_A = val
        self.swift_obj.SequenceA_GeneralInformation.SendersCorrespondent_A.swiftTag = "53A"

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
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_53D_Type)
    def _validate_senders_correspondent_53D(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setsenders_correspondent_53D(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.SendersCorrespondent_D = val
        self.swift_obj.SequenceA_GeneralInformation.SendersCorrespondent_D.swiftTag = "53D"

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
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_56A_Type)
    def _validate_intermediary_56A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setintermediary_56A(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.Intermedairy_A = val
        self.swift_obj.SequenceA_GeneralInformation.Intermedairy_A.swiftTag = "56A"

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
    def _format_intermediary_56D(self, val):
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
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_56D_Type)
    def _validate_intermediary_56D(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setintermediary_56D(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.Intermedairy_D = val
        self.swift_obj.SequenceA_GeneralInformation.Intermedairy_D.swiftTag = "56D"

    #option_getter
    def get_account_with_institution_sequenceA_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_account_with_institution_sequenceA(self):
        """returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            account_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_OPTION'],
                                                                      ignore_absence=True)
        else:
            account_option = self.get_account_with_institution_sequenceA_option()
        if account_option == 'A':
            getter_name = 'account_with_institution_57A_sequenceA'
        if account_option == 'D':
            getter_name = 'account_with_institution_57D_sequenceA'
        return getter_name

    # getter
    def account_with_institution_57A_sequenceA(self):
        """ Returns a dictionary as {'account':<value>, 'bic':<value>} """
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_ACCOUNT'],
                                                               ignore_absence=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_BIC'])
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            return get_counterpartys_correspondent_details(self.acm_obj)

    # formatter
    def _format_account_with_institution_57A_sequenceA(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ACCOUNT')
        bic = val.get('BIC')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val

    # validator
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_57A_Type)
    def _validate_account_with_institution_57A_sequenceA(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setaccount_with_institution_57A_sequenceA(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.AccountWithInstitution_A = val
        self.swift_obj.SequenceA_GeneralInformation.AccountWithInstitution_A.swiftTag = "57A"

    # getter
    def account_with_institution_57D_sequenceA(self):
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
    def _format_account_with_institution_57D_sequenceA(self, val):
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
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_57D_Type)
    def _validate_account_with_institution_57D_sequenceA(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setaccount_with_institution_57D_sequenceA(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.AccountWithInstitution_D = val
        self.swift_obj.SequenceA_GeneralInformation.AccountWithInstitution_D.swiftTag = "57D"

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
            val['BENEFICIARY_INST_BIC'] = self.__get_beneficiary_inst_bic(self.acm_obj)
            return val

    def __get_beneficiary_inst_bic(self, acm_obj):
        """helper method retuens bic of beneficiary institution"""
        if acm_obj.CounterpartyAccountRef().Bic() and acm_obj.CounterpartyAccountRef().Bic().Alias():
            return acm_obj.CounterpartyAccountRef().Bic().Alias()
        else:
            return ''

    # formatter
    def _format_beneficiary_institution_58A(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ACCOUNT')
        bic = val.get('BENEFICIARY_INST_BIC')
        if bic:
            if account:
                val = "/" + str(account) + "\n" + str(bic)
            else:
                val = str(bic)
            return val

    # validator
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_58A_Type)
    def _validate_beneficiary_institution_58A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setbeneficiary_institution_58A(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.BeneficiaryInstitution_A = val
        self.swift_obj.SequenceA_GeneralInformation.BeneficiaryInstitution_A.swiftTag = "58A"

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
            val = get_counterparty_details(self.acm_obj)
            temp = get_counterpartys_correspondent_details(self.acm_obj)
            val['BENEFICIARY_INST_NAME'] = temp['NAME']
            val['BENEFICIARY_INST_ADDRESS'] = temp['ADDRESS']
            return val


    # formatter
    def _format_beneficiary_institution_58D(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ACCOUNT')
        name = val.get('BENEFICIARY_INST_NAME')
        address = val.get('BENEFICIARY_INST_ADDRESS')

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
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_58D_Type)
    def _validate_beneficiary_institution_58D(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setbeneficiary_institution_58D(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.BeneficiaryInstitution_D = val
        self.swift_obj.SequenceA_GeneralInformation.BeneficiaryInstitution_D.swiftTag = "58D"

    #option_getter
    def get_ordering_customer_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_ordering_customer(self):
        """returns name of the getter method"""
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

    @validate_with(MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type)
    def _validate_ordering_customer_50A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_customer_50A(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.OrderingCustomer_A = val
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.OrderingCustomer_A.swiftTag = '50A'


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

    # validator
    @validate_with(MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type)
    def _validate_ordering_customer_50F(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_customer_50F(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.OrderingCustomer_F = val
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.OrderingCustomer_F.swiftTag = '50F'

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
    @validate_with(MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type)
    def _validate_ordering_customer_50K(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_customer_50K(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.OrderingCustomer_K = val
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.OrderingCustomer_K.swiftTag = '50K'

    #option_getter
    def get_ordering_institution_sequenceB_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_ordering_institution_sequenceB(self):
        """returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            ordering_institution_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                   ['SWIFT',
                                                                                    'ORDERING_INSTITUTION_OPTION'],
                                                                                   ignore_absence=True)
        else:
            ordering_institution_option = self.get_ordering_institution_sequenceB_option()
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
    @validate_with(MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern)
    def _validate_ordering_institution_52A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_institution_52A(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.OrderingInstitution_A = val
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.OrderingInstitution_A.swiftTag = '52A'

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
    @validate_with(MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type)
    def _validate_ordering_institution_52D(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setordering_institution_52D(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.OrderingInstitution_D = val
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.OrderingInstitution_D.swiftTag = '52D'

    #option_getter
    def get_account_with_institution_sequenceB_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # Setter
    def _set_OPTION_account_with_institution_sequenceB(self):
        """returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            account_with_institution_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                       ['SWIFT',
                                                                                        'ACCOUNT_WITH_INSTITUTION_OPTION'],
                                                                                       ignore_absence=True)
        else:
            account_with_institution_option = self.get_account_with_institution_sequenceB_option()
        if account_with_institution_option == "A":
            getter_name = 'account_with_institution_57A_sequenceB'
        elif account_with_institution_option == "C":
            getter_name = 'account_with_institution_57C_sequenceB'
        elif account_with_institution_option == "D":
            getter_name = 'account_with_institution_57D_sequenceB'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(account_with_institution_option), 'AccountWithInstitution_57a'))
            getter_name = 'account_with_institution_57A'  # default
        return getter_name

    # getter
    def account_with_institution_57A_sequenceB(self):
        """ Returns a dictionary as {'account':<value>, 'bic':<value>} """
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_ACCOUNT'],
                                                               ignore_absence=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_BIC'])
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            return get_counterpartys_correspondent_details(self.acm_obj)

    # formatter
    def _format_account_with_institution_57A_sequenceB(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ACCOUNT')
        bic = val.get('BIC')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val

    # validator
    @validate_with(MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern)
    def _validate_account_with_institution_57A_sequenceB(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setaccount_with_institution_57A_sequenceB(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.AccountWithInstitution_A = val
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.AccountWithInstitution_A.swiftTag = '57A'

    # getter
    def account_with_institution_57C_sequenceB(self):
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
    def _format_account_with_institution_57C_sequenceB(self, val):
        """Formats the value provided by getter method"""
        if val:
            val = "/" + str(val)
            return val

    # validator
    @validate_with(MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type)
    def _validate_account_with_institution_57C_sequenceB(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setaccount_with_institution_57C_sequenceB(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.AccountWithInstitution_C = val
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.AccountWithInstitution_C.swiftTag = '57C'

    # getter
    def account_with_institution_57D_sequenceB(self):
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
    def _format_account_with_institution_57D_sequenceB(self, val):
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
    @validate_with(MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type)
    def _validate_account_with_institution_57D_sequenceB(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setaccount_with_institution_57D_sequenceB(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.AccountWithInstitution_D = val
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.AccountWithInstitution_D.swiftTag = '57D'

    #option_getter
    def get_beneficiary_customer_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    #Setter
    def _set_OPTION_beneficiary_customer(self):
        """returns name of the getter method"""
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

    # validator
    @validate_with(MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern)
    def _validate_beneficiary_customer_59A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setbeneficiary_customer_59A(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.BeneficiaryCustomer_A = val
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.BeneficiaryCustomer_A.swiftTag = '59A'

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

        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type)
    def _validate_beneficiary_customer_no_option_59(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setbeneficiary_customer_no_option_59(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.BeneficiaryCustomer = val
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.BeneficiaryCustomer.swiftTag = '59'

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
    @validate_with(MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type)
    def _validate_beneficiary_customer_59F(self, val, swift_tag_obj=MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setbeneficiary_customer_59F(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.BeneficiaryCustomer_F = val
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.BeneficiaryCustomer_F.swiftTag = '59F'


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
            val = self.format_MT202COV_field70(val, 35, 4)
        else:
            val = val.replace('newline', '\n')
        return str(val)

    # validator
    @validate_with(MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern)
    def _validate_remittance_information_70(self, val):
        """validates the value provided by formatter method"""
        validate_remittance_info(val)
        return val

    # setter
    def _set_remittance_information_70(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.RemittanceInformation = val
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.RemittanceInformation.swiftTag = '70'

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
    @validate_with(MT202COV.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern)
    def _validate_instructed_amount_33B(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _set_instructed_amount_33B(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.CurrencyInstructedAmount = val
        self.swift_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.CurrencyInstructedAmount.swiftTag = "33B"

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

    def format_MT202COV_field70(self, val, character_limit, n_lines):
        """helper method returns formatted form of input provided"""
        text = []
        val = val.split('newline')
        for values in val:
            line = FSwiftWriterUtils.split_text_on_character_limit(values, character_limit)
            text.append(line)
        text = '\n'.join(str(i) for sub_list in text for i in sub_list)
        text = '\n'.join(text.split('\n')[:n_lines])
        return text

class FMT202COVOutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_typ = "202COV"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT' + self.mt_typ)
        super(FMT202COVOutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

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
        """returns service type identifier"""
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
        #ref_no = uuid.uuid4()
        #return "{121:%s}" % (ref_no)
        settlement = self.acm_obj
        try:
            ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj = settlement, msg_typ='MT103', integration_type='Outgoing')
            if ext_obj:
                mt_msg = FSwiftMLUtils.FSwiftExternalObject.get_stored_data(ext_obj, 'swift_data')
                temp_mt_msg = mt_msg
                index = temp_mt_msg.find('{121:')
                ref_no = temp_mt_msg[index+5:index+41]
                return "{121:%s}" % (ref_no)
        except Exception as e:
            notifier.WARN("Unable to get UETR")

    def gpi_id(self):
        """returns gpi id"""
        gpi_identifier = get_gpi_identifier(self.acm_obj)
        if gpi_identifier:
            return "{111:%s}" % str(gpi_identifier)

    def validation_flag(self):
        """returns validation flag"""
        return '{119:COV}'

class FMT202COVOutBaseNetworkRules(object):
    """validation of swift message by network rules"""

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.acm_obj = acm_obj

    def network_rule_C1(self):
        ''' In sequence A, If field 56a is present, then field 57a must also be present'''
        is_field_56a_present = self.swift_message_obj.SequenceA_GeneralInformation.Intermedairy_A or self.swift_message_obj.SequenceA_GeneralInformation.Intermedairy_D
        is_field_57a_present = self.swift_message_obj.SequenceA_GeneralInformation.AccountWithInstitution_A or self.swift_message_obj.SequenceA_GeneralInformation.AccountWithInstitution_D or self.swift_message_obj.SequenceA_GeneralInformation.AccountWithInstitution_B
        if is_field_56a_present:
            if not is_field_57a_present:
                return 'If field 56a is present in sequence A, then field 57a must also be present in sequence A'
        return ''
    """
    def network_rule_C2(self):
        ''' In sequence B, If field 56a is present, then field 57a must also be present'''
        is_field_56a_present = self.swift_message_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.Intermedairy_A or self.swift_message_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.Intermedairy_D
        is_field_57a_present = self.swift_message_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.AccountWithInstitution_A or self.swift_message_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.AccountWithInstitution_D or self.swift_message_obj.SequenceB_UnderlyingCustomerCreditTransferDetails.AccountWithInstitution_B
        if is_field_56a_present:
            if not is_field_57a_present:
                return 'If field 56a is present in sequence B, then field 57a must also be present in sequence B'
        return ''
    """

