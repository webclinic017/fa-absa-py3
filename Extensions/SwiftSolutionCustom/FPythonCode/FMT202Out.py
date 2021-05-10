"""----------------------------------------------------------------------------
MODULE:
    FMT202Out

DESCRIPTION:
    This module provides the customizable class for the FMT202 outgoing implementation

CLASS:
    FMT202

VERSION: 3.0.3-0.5.3744
------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2021-01-28      FAOPS-1038      Tawanda Mukhalela       Martin Wortmann         Remapped Account with institution 57A
                                                                                to Intermediary 1.
2021-03-09      FAOPS-1027      Willie vd Bank          Martin Wortmann         Amended 72 to retrieve the
                                                                                correct info for a netted settlement.
------------------------------------------------------------------------------------------------------------------------
"""
import MT202
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT202OutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with
from FCashOutUtils import *
import FSwiftWriterUtils
import FMTCustomFunctions
from ChineseCommercialCode import CCC_simplified_writer, CCC_traditional_writer

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')


@accepts([acm.FSettlement, MT202.CTD_ANON, xml.dom.minidom.Document])
class FMT202(FMT202OutBase.FMT202Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FMT202, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic
    """
    account_with_institution_57A
    account_with_institution_57D
    beneficiary_institution_58A
    beneficiary_institution_58D
    date_currency_amount_32A
    intermedairy_56A
    intermedairy_56D
    ordering_institution_52A
    ordering_institution_52D
    related_reference_21
    senders_correspondent_53A
    senders_correspondent_53D
    transaction_reference_20
    get_user_data
    """
    """
    To override the options provided, use below methods to write your own logic:-
    methods:- 
    get_ordering_institution_option (Tag-52 options:A/D)
    get_senders_correspondent_option (Tag-53 options:A/D)
    get_intermediary_option (Tag-56 options:A/D)
    get_account_with_institution_option (Tag-57 options:A/D)
    get_beneficiary_institution_option (Tag-58 options:A/D)
    
    For example:
    def get_ordering_institution_option(self):
        condition = True
        if condition:
            return 'A'
        else:
            return 'D'

    """
    # formatter
    def _format_transaction_reference_20(self, val):
        seqnbr = val.get('SEQNBR')
        seq_ref = val.get('SEQREF')
        if seqnbr and seq_ref:
            val = '%s-%s-%s' % (str(seq_ref), str(seqnbr), str(get_message_version_number(self.acm_obj)))
            return val

    def get_senders_correspondent_option(self):
        return 'B'

    # setter
    def _set_OPTION_senders_correspondent(self):
        """
        returns name of the getter method
        """
        senders_correspondent_option = self.get_senders_correspondent_option()
        if senders_correspondent_option == 'A':
            return 'senders_correspondent_53A'
        elif senders_correspondent_option == 'B':
            return 'senders_correspondent_53B'
        elif senders_correspondent_option == 'D':
            return 'senders_correspondent_53D'
        raise ValueError('Could not find any option applicable for Field 53')

    # getter
    def senders_correspondent_53B(self):
        """
        Returns dictionary as {'ACCOUNT':<value>, 'BIC':<value>}
        """
        return get_acquirer_correpondent_details(self.acm_obj)

    # formatter
    def _format_senders_correspondent_53B(self, sender_corr_details):
        """Formats the value provided by getter method"""
        senders_correspondent_account = sender_corr_details.get('ACCOUNT')
        senders_correspondent_bic = sender_corr_details.get('BIC')
        if not senders_correspondent_bic:
            raise ValueError('Missing Acquirer account Bic address for Field 53B')
        if not senders_correspondent_account:
            raise ValueError('Missing Acquirer account for Field 53B')

        return "/" + str(senders_correspondent_account)

    # validator
    @validate_with(MT202.MT202_53B_Type)
    def _validate_senders_correspondent_53B(self, sender_correspondent):
        """validates the value provided by formatter method"""
        return sender_correspondent

    # setter
    def _setsenders_correspondent_53B(self, sender_correspondent):
        """sets the value on python object"""
        self.swift_obj.SendersCorrespondent_B = sender_correspondent
        self.swift_obj.SendersCorrespondent_B.swiftTag = "53B"

    # formatter
    def _format_beneficiary_institution_58D(self, beneficiary_inst_details):
        """Formats the value provided by getter method"""
        account = beneficiary_inst_details.get('ACCOUNT')
        name = beneficiary_inst_details.get('BENEFICIARY_INST_NAME')
        address = beneficiary_inst_details.get('BENEFICIARY_INST_ADDRESS')

        temp_name = name
        temp_address = address
        char_set = ''
        lookup_temp = FMT202OutBase.lookup
        try:
            char_set = str(self.acm_obj.Counterparty().AdditionalInfo().TraditionalChinese())
        except:
            #   notifier.WARN("Could not find Additional Info 'TraditionalChinese'.")
            char_set = 'False'

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
            name_address = '\n'.join(split_name_and_address)
            if account:
                name_address = "/" + str(account) + "\n" + str(name_address)
            return name_address

    # getter
    def ordering_institution_52A(self):
        """
        Returns dictionary as {'ACCOUNT':<value>, 'BIC':<value>}
        """
        return {}

    def sender_to_receiver_information_72(self):
        """
        Returns a details_of_charges as string
        """
        field_72_rec_code = ''
        if self.acm_obj.Currency().Name() == 'ZAR':
            rec_code = self.get_rec_code_qf_name()
            field_72_rec_code = '/REC/' + str(rec_code)

        field_72_rec_code = self._get_extra_information_for_72(field_72_rec_code)
        return field_72_rec_code.upper()

    def get_rec_code_qf_name(self):
        """
        function used in SENDER_TO_RECEIVER_INFO
        """
        if self.acm_obj.Trade():
            settlement = self.acm_obj
        else:
            settlement = FMTCustomFunctions.get_lowest_settlement_from_hierarchy(self.acm_obj)

        rec_code_queries = [query.Name() for query in acm.FStoredASQLQuery.Select('')
                            if 'SwiftSenderToReceiver_' in query.Name()]
        for qf in rec_code_queries:
            if acm.FStoredASQLQuery[qf].Query() and acm.FStoredASQLQuery[qf].Query().IsSatisfiedBy(settlement):
                return qf.split('_')[1]
        return ''

    # formatter
    def _format_sender_to_receiver_information_72(self, sender_to_receiver_information):
        """Formats the value provided by getter method"""
        return sender_to_receiver_information

    # validator
    @validate_with(MT202.MT202_72_Type)
    def _validate_sender_to_receiver_information_72(self, sender_to_receiver_information):
        """validates the value provided by formatter method"""
        return sender_to_receiver_information

    # setter
    def _set_sender_to_receiver_information_72(self, sender_to_receiver_information):
        """sets the value on python object of MT103"""
        self.swift_obj.SenderToReceiverInformation = sender_to_receiver_information
        self.swift_obj.SenderToReceiverInformation.swiftTag = '72'

    def _get_extra_information_for_72(self, field_72_rec_code):
        """
        Generates the extra information for 72
        """
        diary = self.acm_obj.Diary()
        if not diary:
            return field_72_rec_code
        diary_entries = diary.Text().split('\n')
        valid_entries = list()
        for entry in diary_entries:
            if str(entry).startswith('/') and str(entry)[4] == '/':
                value = self._get_diary_entry_value(entry.strip())
                valid_entries.append(value.replace('\n', '\n//'))
        if len(valid_entries) == 0:
            return field_72_rec_code
        return field_72_rec_code + "\n" + "\n".join(valid_entries)

    @staticmethod
    def _get_diary_entry_value(diary_entry):
        """
        Formats the entry according to character limit
        """
        diary_entry_list = FSwiftWriterUtils.split_text_and_prefix(str(diary_entry), 35, '')
        formatted_value = FSwiftWriterUtils.allocate_space_for_name_and_address_with_constraint(diary_entry_list)
        return formatted_value

    # getter
    def account_with_institution_57A(self):
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
            party_details = get_counterpartys_correspondent_details(self.acm_obj)
            party_details['ACCOUNT'] = get_counterpartys_intermediary_details(self.acm_obj).get('ACCOUNT')
            return party_details

    # formatter
    def _format_account_with_institution_57A(self, account_with_institution_dict):
        account = account_with_institution_dict.get('ACCOUNT')
        bic = account_with_institution_dict.get('BIC')
        if bic:
            account_with_institution = str(bic)
            if account:
                account_with_institution = '/' + str(account) + '\n' + str(account_with_institution)
            return account_with_institution

    # formatter
    def _format_intermediary_56A(self, intermediary_information_dict):
        intermediary_bic = intermediary_information_dict.get('BIC')
        if intermediary_bic:
            return str(intermediary_bic)
        return None


class FMT202MessageHeader(FMT202OutBase.FMT202OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT202MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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
        '''MUR is sent in the format FAC-SEQNBR of confirmation-VersionID'''
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seqref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            seqnbr = self.acm_obj.Oid()
            seqref = get_settlement_reference_prefix()
        return "{108:%s-%s-%s}" % (seqref, seqnbr, get_message_version_number(self.acm_obj))

    def gpi_id(self):
        """
        returns gpi id
        """
        try:
            gpi_identifier = get_gpi_identifier(self.acm_obj)
            if gpi_identifier:
                return "{111:%s}" % str(gpi_identifier)
        except:
            return ''

    def receiver_logical_terminal_address(self):
        '''LT code is hardcoded as X for sender'''
        terminal_address = ''
        receivers_bic = ''
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'RECEIVER_BIC'])
        else:
            receivers_bic = get_receivers_bic(self.acm_obj)

        if self.acm_obj.Currency().Name() == 'ZAR':
            counterparty_account = self.acm_obj.CounterpartyAccountRef()
            if counterparty_account:
                if counterparty_account.Bic2():
                    receivers_bic = counterparty_account.Bic2().Alias()
                elif counterparty_account.Bic():
                    receivers_bic = counterparty_account.Bic().Alias()
                else:
                    raise ValueError('No BIC specified on account')

        terminal_address = self.logical_terminal_address(receivers_bic, "X")
        return terminal_address

    def service_identifier(self):
        """returns service identifier"""
        if self.use_operations_xml:
            sub_network = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                   ['SWIFT', 'SUB_NETWORK'],
                                                                   ignore_absence=True)
            if sub_network == "TARGET2":
                return "{103:TGT}"
            if sub_network == "EBA":
                return "{103:EBA}"
            if sub_network == "SRS":
                return "{103:SRS}"
        else:
            service_code = get_swift_service_code(self.acm_obj)
            if service_code:
                return "{103:%s}" % service_code
        return ''


class FMT202NetworkRules(FMT202OutBase.FMT202OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT202NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)
