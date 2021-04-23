"""----------------------------------------------------------------------------
MODULE:
    FMT200OutBase

DESCRIPTION:
    This module provides the base class for the FMT200 outgoing implementation

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
import MT200
from FCashOutUtils import *
from FInstitutionTransfersOutBase import FInstitutionTransfersOutBase
from FSwiftWriterEngine import validate_with, should_use_operations_xml

import FSwiftWriterLogger
import FSwiftWriterUtils

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')

class FMT200Base(FInstitutionTransfersOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = 'MT200'
        super(FMT200Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # Implementing it to pass the NotImplementedError
    def _message_sequences(self):
        pass

    # getter
    # Moved to FInstitutionTransfersOutBase

    # formatter
    # Moved to FInstitutionTransfersOutBase

    # validator
    @validate_with(MT200.MT200_20_Type)
    def _validate_transaction_reference_20(self, val):
        """validates the value provided by formatter method"""
        validate_slash_and_double_slash(val, "Transaction Reference")
        return val

    # setter
    def _set_transaction_reference_20(self, val):
        """sets the value on python object"""
        self.swift_obj.TransactionReferenceNumber = val
        self.swift_obj.TransactionReferenceNumber.swiftTag = "20"

    # getter
    # Moved to FInstitutionTransfersOutBase

    # formatter


    # validator
    @validate_with(MT200.MT200_32A_Type)
    def _validate_date_currency_amount_32A(self, val):
        """validates the value provided by formatter method"""
        validate_currency_amount(val, "Date Currency Amount")
        amount = get_amount_from_currency_amount(val)
        validateAmount(amount.replace('.', ','), 15, "Date Currency Amount")
        return val

    # setter
    def _set_date_currency_amount_32A(self, val):
        """sets the value on python object"""
        self.swift_obj.DateCurrencyAmount = val
        self.swift_obj.DateCurrencyAmount.swiftTag = "32A"

    # getter
    def senders_correspondent_53B(self):
        """ Returns a senders_correspondent as string """
        if self.use_operations_xml:
            senders_correspondent_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                     ['SWIFT',
                                                                                      'SENDERS_CORRESPONDENT_ACCOUNT'],
                                                                                     ignore_absence=True)
            return senders_correspondent_account
        else:
            senders_correspondent_account = self.acm_obj.AcquirerAccountRef().Account()
        return senders_correspondent_account

    # formatter
    def _format_senders_correspondent_53B(self, val):
        """Formats the value provided by getter method"""
        if val:
            val = "/" + val
            return str(val)

    # validator
    @validate_with(MT200.MT200_53B_Type)
    def _validate_senders_correspondent_53B(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _set_senders_correspondent_53B(self, val):
        """sets the value on python object"""
        self.swift_obj.SendersCorrespondent_B = val
        self.swift_obj.SendersCorrespondent_B.swiftTag = "53B"

    #option_getter
    def get_intermediary_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_intermediary(self):
        """Returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            intermediary_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'INTERMEDIARY_OPTION'],
                                                                           ignore_absence=True)
        else:
            intermediary_option = self.get_intermediary_option()
        if intermediary_option == 'A':
            getter_name = 'intermediary_56A'
        elif intermediary_option == 'D':
            getter_name = 'intermediary_56D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(intermediary_option), 'Intermediary_56a'))
            getter_name = 'intermediary_56A'
        return getter_name

    # getter
    # Moved to FInstitutionTransfersOutBase

    # formatter
    # Moved to FInstitutionTransfersOutBase

    # validator
    @validate_with(MT200.MT200_56A_Type)
    def _validate_intermediary_56A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setintermediary_56A(self, val):
        """sets the value on python object"""
        self.swift_obj.Intermedairy_A = val
        self.swift_obj.Intermedairy_A.swiftTag = "56A"

    # getter
    def intermediary_56D(self):
        """ Returns a dictionary as {'account':<value>, 'name':<value>, 'address':<value>} """
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'INTERMEDIARY_ACCOUNT'],
                                                               ignore_absence=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'INTERMEDIARY_NAME'],
                                                            ignore_absence=True)
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'INTERMEDIARY_ADDRESS'],
                                                               ignore_absence=True)
            values_dict['ACCOUNT'] = account
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
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
    @validate_with(MT200.MT200_56D_Type)
    def _validate_intermediary_56D(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setintermediary_56D(self, val):
        """sets the value on python object"""
        self.swift_obj.Intermedairy_D = val
        self.swift_obj.Intermedairy_D.swiftTag = "56D"

    #option_getter
    def get_account_with_institution_option(self):
        """Returns default option if override is not provided"""
        return 'A'

    # setter
    def _set_OPTION_account_with_institution(self):
        """Returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            account_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_OPTION'])
        else:
            account_option = self.get_account_with_institution_option()
        if account_option == 'A':
            getter_name = 'account_with_institution_57A'
        elif account_option == 'D':
            getter_name = 'account_with_institution_57D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(account_option), 'AccountWithInstitution_57a'))
            getter_name = 'account_with_institution_57A'
        return getter_name

    # getter
    # Moved to FInstitutionTransfersOutBase

    # formatter
    # Moved to FInstitutionTransfersOutBase

    # validator
    @validate_with(MT200.MT200_57A_Type)
    def _validate_account_with_institution_57A(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setaccount_with_institution_57A(self, val):
        """sets the value on python object"""
        self.swift_obj.AccountWithInstitution_A = val
        self.swift_obj.AccountWithInstitution_A.swiftTag = "57A"

    # getter
    def account_with_institution_57D(self):
        """ Returns a dictionary as {'account':<value>, 'name':<value>, 'address':<value>} """
        values_dict = {}
        if self.use_operations_xml:
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
    @validate_with(MT200.MT200_57D_Type)
    def _validate_account_with_institution_57D(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setaccount_with_institution_57D(self, val):
        """sets the value on python object"""
        self.swift_obj.AccountWithInstitution_D = val
        self.swift_obj.AccountWithInstitution_D.swiftTag = "57D"


class FMT200OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_typ = "200"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT' + self.mt_typ)
        super(FMT200OutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

    def message_type(self):
        """returns type of message"""
        return "200"

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


class FMT200OutBaseNetworkRules(object):
    """validation of swift message by network rules"""

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        self.swift_message_obj = swift_message_obj
        self.acm_obj = acm_obj
        self.swift_message = swift_message

