"""----------------------------------------------------------------------------
MODULE:
    FMT103Out

DESCRIPTION:
    This module provides the customizable class for the FMT103 outgoing implementation

CLASS:
    FMT103

VERSION: 3.0.3-0.5.3744
------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2020-12-14      FAOPS-821       Tawanda Mukhalela       Martin Wortmann         Added Check for account on 57A.
2021-01-26      FAOPS-1026      Tawanda Mukhalela       Martin Wortmann         Added Cpty Ref Check for Remittance Info
2021-02-23      FAOPS-1034      Willie vd Bank          Martin Wortmann         Added FSwiftWriterUtils_Override to
                                                                                50F and 59F to limit the field length
                                                                                Updated 50F to remove incorrect /
2021-03-09      FAOPS-1027      Willie vd Bank          Martin Wortmann         Amended 50F and 72 to retrieve the
                                                                                correct info for a netted settlement.
------------------------------------------------------------------------------------------------------------------------
"""

import xml.dom.minidom

import acm

from DocumentGeneral import get_bank_party_name, get_default_bank_country_code
import FMT103OutBase
import MT103
import FSwiftWriterLogger
from FSwiftMLUtils import accepts
from FSwiftWriterEngine import validate_with
from FCashOutUtils import *
import FSwiftWriterUtils
import FSwiftWriterUtils_Override
import FMTCustomFunctions
from ChineseCommercialCode import CCC_simplified_writer, CCC_traditional_writer

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')


@accepts([acm.FSettlement, MT103.CTD_ANON, xml.dom.minidom.Document])
class FMT103(FMT103OutBase.FMT103Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FMT103, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic

    """
    account_with_institution_57A
    account_with_institution_57C
    account_with_institution_57D
    bank_operation_code_23B
    beneficiary_customer_59A
    beneficiary_customer_59F
    beneficiary_customer_no_option_59
    details_of_charges_71A
    instructed_amount_33B
    instruction_code_23E
    intermediary_institution_56A
    intermediary_institution_56C
    intermediary_institution_56D
    ordering_customer_50A
    ordering_customer_50F
    ordering_customer_50K
    ordering_institution_52A
    ordering_institution_52D
    remittance_information_70
    senders_correspondent_53A
    senders_correspondent_53D
    senders_reference_20
    value_date_32A
    get_user_data

    """

    """
    To override the options provided, use below methods to write your own logic:-
    methods:- 
    get_ordering_customer_option (Tag-50 options:A/F/K)
    get_ordering_institution_option (Tag-52 options:A/D)
    get_senders_correspondent_option (Tag-53 options:A/D)
    get_intermediary_institution_option (Tag-56 options:A/C/D)
    get_account_with_institution_option (Tag-57 options:A/C/D)
    get_beneficiary_customer_option (Tag-59 options:A/NO OPTION/F)

    For example:
    def get_ordering_customer_option(self):
        condition = True
        if condition:
            return 'A'
        else:
            return 'F'

    """

    # formatter
    def _format_senders_reference_20(self, val):
        """
        Formats the value provided by getter method
        Removed Message Type at the end
        """
        if val:
            sett_obj = acm.FSettlement[str(val)]
            val = "%s-%s-%s" % (get_settlement_reference_prefix(), str(val), str(get_message_version_number(sett_obj)))
        return val

    def get_ordering_customer_option(self):
        """
        Overrides the default option
        """
        return 'F'

    # option_getter
    def get_senders_correspondent_option(self):
        """Returns default option if override is not provided"""
        if self.acm_obj.MTMessages() == '202COV':
            return 'A'
        return 'B'

    # setter
    def _set_OPTION_senders_correspondent(self):
        """Returns name of the getter"""
        if self.use_operations_xml:
            senders_correspondent_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                    ['SWIFT',
                                                                                     'SENDERS_CORRESPONDENT_OPTION'],
                                                                                    ignore_absence=True)
        else:
            senders_correspondent_option = self.get_senders_correspondent_option()
        if senders_correspondent_option == 'A':
            return 'senders_correspondent_53A'
        elif senders_correspondent_option == 'B':
            return 'senders_correspondent_53B'
        elif senders_correspondent_option == 'D':
            return 'senders_correspondent_53D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(senders_correspondent_option), 'SendersCorrespondent_53a'))
            return 'senders_correspondent_53A'  # default

    # formatter
    def _format_senders_correspondent_53A(self, val):
        """
        Formats the value provided by getter method
        """
        senders_correspondent_bic = val.get('BIC')
        if senders_correspondent_bic:
            return str(senders_correspondent_bic)
        raise ValueError('Senders correspondent BIC not Found')

    # getter
    def senders_correspondent_53B(self):
        """
        Returns a dictionary as {'senders_correspondent_account': value, 'senders_correspondent_bic':value}
        """
        values_dict = get_acquirer_correpondent_details(self.acm_obj)
        values_dict['ACCOUNT'] = self.acm_obj.AcquirerAccountRef().Account()
        return values_dict

    # formatter
    def _format_senders_correspondent_53B(self, val):
        """
        Formats the value provided by getter method
        """
        senders_correspondent_account = val.get('ACCOUNT')
        senders_correspondent_bic = val.get('BIC')
        if not senders_correspondent_bic:
            raise ValueError('Missing Acquirer account Bic address for Field 53B')
        if not senders_correspondent_account:
            raise ValueError('Missing Acquirer account for Field 53B')

        return "/" + str(senders_correspondent_account)

    # validator
    @validate_with(MT103.MT103_53B_Type)
    def _validate_senders_correspondent_53B(self, val):
        """
        validates the value provided by formatter method
        """
        return val

    # setter
    def _setsenders_correspondent_53B(self, val):
        """
        sets the value on python object of MT103
        """
        self.swift_obj.SendersCorrespondent_B = val
        self.swift_obj.SendersCorrespondent_B.swiftTag = "53B"

    def get_beneficiary_customer_option(self):
        return 'F'

    # getter
    def ordering_customer_50F(self):
        """
        Returns a dictionary as {'ordering_customer_account': value, 'ordering_customer_name':value,
        'ordering_customer_address':value, 'ordering_customer_country_code':value, 'ordering_customer_town':value,
        'ordering_customer_zipcode':value}
        """
        party_details = dict()

        counterparty = self.acm_obj.Counterparty()
        if self.acm_obj.Trade():
            counterparty = self.acm_obj.Trade().Counterparty()
        else:
            settlement = FMTCustomFunctions.get_lowest_settlement_from_hierarchy(self.acm_obj)
            if settlement.Trade():
                counterparty = settlement.Trade().Counterparty()

        party_sds_id = str(counterparty.AdditionalInfo().BarCap_SMS_CP_SDSID())
        bank_name = str(get_bank_party_name())
        country_code = str(get_default_bank_country_code())
        cust_constant = 'CUST'
        party_identifier = [cust_constant, country_code, bank_name, party_sds_id]
        party_details['PARTY_IDENTIFIER'] = "/".join(party_identifier)
        party_details['NAME'] = get_party_full_name(counterparty)
        address = [counterparty.Address(), counterparty.Address2()]
        party_details['ADDRESS'] = " ".join(address)
        party_details['COUNTRY_CODE'] = get_party_country_code(counterparty)
        party_details['TOWN'] = get_party_town(counterparty)

        return party_details

    # formatter
    def _format_ordering_customer_50F(self, val):
        """
        Formats the value provided by getter method
        """
        party_identifier = val.get('PARTY_IDENTIFIER')
        name = val.get('NAME')
        address = val.get('ADDRESS')
        country_code = val.get('COUNTRY_CODE')
        town = val.get('TOWN')
        town = str(town)
        name_list, address_list, country_and_town_list = [], [], []

        char_set = ''
        lookup_temp = FMT103OutBase.lookup
        try:
            char_set = str(self.acm_obj.Acquirer().AdditionalInfo().TraditionalChinese())
        except Exception as e:
            char_set = 'False'

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

        name = temp_name
        if name:
            name_list = FSwiftWriterUtils.split_text_and_prefix(str(name), 33, '1/')
        if address:
            address_list = FSwiftWriterUtils.split_text_and_prefix(str(address), 33, '2/')
        if country_code:
            additional_details = str(country_code)
            if town:
                additional_details = additional_details + '/' + str(town)
            country_and_town_list = FSwiftWriterUtils.split_text_and_prefix(str(additional_details), 33, '3/')
        value = FSwiftWriterUtils_Override.allocate_space_for_name_and_address_with_constraint(name_list, address_list,
                                                                                      country_and_town_list)
        if party_identifier:
            value = party_identifier + '\n' + value
        return value

    # getter
    def beneficiary_customer_59F(self):
        """ Returns a dictionary as {'beneficiary_customer_account': value, 'beneficiary_customer_name':value, 'beneficiary_customer_address':value,
        'beneficiary_customer_country_code':value, 'beneficiary_customer_town':value} """

        party_details = dict()
        party_details['ACCOUNT'] = get_counterparty_details(self.acm_obj)['ACCOUNT']
        party_details['NAME'] = get_counterparty_details(self.acm_obj)['NAME']
        address = [self.acm_obj.Counterparty().Address(), self.acm_obj.Counterparty().Address2()]
        party_details['ADDRESS'] = " ".join(address)
        party_details['COUNTRY_CODE'] = get_counterparty_details(self.acm_obj)['COUNTRY_CODE']
        party_details['TOWN'] = get_counterparty_details(self.acm_obj)['TOWN']
        return party_details

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
            country_and_town_list = FSwiftWriterUtils.split_text_and_prefix(str(additional_details), 33, '3/')
        value = FSwiftWriterUtils_Override.allocate_space_for_name_and_address_with_constraint(name_list, address_list,
                                                                                      country_and_town_list)
        if account:
            account = '/' + str(account)
            value = account + '\n' + value
        return value

    # getter
    def ordering_institution_52A(self):
        """
        Returns dictionary as {'ACCOUNT':<value>, 'BIC':<value>}
        """
        return {}

    # getter
    def intermediary_institution_56A(self):
        """
        Returns a dictionary as {'intermediary_institution_account': value, 'intermediary_institution_bic':value}
        """
        party_details = self._get_party_details_dictionary('INTERMEDIARY')

        return party_details

    # formatter
    def _format_intermediary_institution_56A(self, account_details):
        """
        Formats the value provided by getter method
        """
        intermediary_institution_bic = account_details.get('BIC')
        if intermediary_institution_bic:
            if self._intermediary_account_exists():
                clearing_code = account_details.get('CLEARING_SYSTEM')
                if clearing_code is not None:
                    branch_code = account_details.get('BRANCH_CODE')
                    return '//' + str(clearing_code) + str(branch_code) + '\n' + str(intermediary_institution_bic)
            return intermediary_institution_bic

    # getter
    def account_with_institution_57A(self):
        """
        Returns a dictionary as {'account':<value>, 'bic':<value>}
        """
        party_details = self._get_party_details_dictionary('CORRESPONDENT')
        return party_details

    # formatter
    def _format_account_with_institution_57A(self, account_details):
        account = get_counterpartys_intermediary_details(self.acm_obj).get('ACCOUNT')
        bic = account_details.get('BIC')
        if bic:
            if self._intermediary_account_exists():
                if account:
                    return '/' + str(account) + '\n' + str(bic)
                return str(bic)
            else:
                clearing_code = account_details.get('CLEARING_SYSTEM')
                if clearing_code is not None:
                    branch_code = account_details.get('BRANCH_CODE')
                    return '//' + str(clearing_code) + str(branch_code) + '\n' + str(bic)
                return str(bic)

    def _get_party_details_dictionary(self, account_type):
        """
        Returns a dictionary with party details
        """
        if account_type == 'INTERMEDIARY':
            party_details = get_counterpartys_intermediary_details(self.acm_obj)
        else:
            party_details = get_counterpartys_correspondent_details(self.acm_obj)

        clearing_system = get_national_clearing_system(self.acm_obj)
        clearing_code = None
        branch_code = self.acm_obj.CounterpartyAccountRef().Accounting()
        if self.acm_obj.Currency().Name() == 'ZAR' and clearing_system == 'ZA':
            clearing_code = get_national_clearing_code(self.acm_obj)

        party_details_dict = dict()
        party_details_dict['CLEARING_SYSTEM'] = clearing_code
        party_details_dict['BRANCH_CODE'] = branch_code
        party_details_dict['ACCOUNT'] = party_details.get('ACCOUNT')
        party_details_dict['BIC'] = party_details.get('BIC')

        return party_details_dict

    def _intermediary_account_exists(self):
        """
        Checks is intermediary account is loaded
        """
        party_details = get_counterpartys_intermediary_details(self.acm_obj)
        if party_details.get('NAME'):
            return True
        return False

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
    def _format_sender_to_receiver_information_72(self, val):
        """Formats the value provided by getter method"""
        return val

    # validator
    @validate_with(MT103.MT103_72_Type)
    def _validate_sender_to_receiver_information_72(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _set_sender_to_receiver_information_72(self, val):
        """sets the value on python object of MT103"""
        self.swift_obj.SenderToReceiverInformation = val
        self.swift_obj.SenderToReceiverInformation.swiftTag = '72'

    # setter
    def _set_OPTION_intermediary_institution(self):
        """Returns name of the getter method"""
        getter_name = ''
        if self.use_operations_xml:
            intermediary_institution_option = FSwiftWriterUtils.get_value_from_xml_tag(
                self.swift_metadata_xml_dom,
                ['SWIFT', 'INTERMEDIARY_INSTITUTION_OPTION'],
                ignore_absence=True
            )
        else:
            intermediary_institution_option = self.get_intermediary_institution_option()
        if intermediary_institution_option == "A":
            if self.acm_obj.MTMessages() == '202COV':
                getter_name = 'receivers_correspondent_54A'
            else:
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
    def receivers_correspondent_54A(self):
        """
        Returns a dictionary as {'intermediary_institution_account': value, 'intermediary_institution_bic':value}
        """
        party_details = self._get_party_details_dictionary('INTERMEDIARY')

        return party_details

    # formatter
    def _format_receivers_correspondent_54A(self, val):
        """
        Formats the value provided by getter method
        """
        correspondent_bic = val.get('BIC')
        if correspondent_bic:
            return str(correspondent_bic)

    # validator
    @validate_with(MT103.MT103_54A_Type)
    def _validate_receivers_correspondent_54A(self, val):
        """
        validates the value provided by formatter method
        """
        return val

    # setter
    def _setreceivers_correspondent_54A(self, val):
        """
        sets the value on python object of MT103
        """
        self.swift_obj.ReceiversCorrespondent_A = val
        self.swift_obj.ReceiversCorrespondent_A.swiftTag = '54A'

    def instruction_code_23E(self):
        return {}

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

    def get_remittance_info(self, settlement):
        """
        Remittance information
        """

        trade = settlement.Trade()
        instrument = settlement.Instrument()
        their_reference = 'Your reference:'
        our_reference = 'Our reference:'
        code = settlement.AdditionalInfo().Ext_CP_Ref_Sett()
        if code and str(code)[0] == '/' and str(code)[4] == '/':
            return str(code).upper()
        newline = 'newline'
        remittance_info = list()
        remittance_info.append('/RFB/')
        remittance_info.append(newline)
        if instrument:
            remittance_info.append('Product:')
            remittance_info.append(instrument.InsType())
        remittance_info.append(newline)
        remittance_info.append(our_reference)
        if trade:
            remittance_info.append(str(trade.Oid()))
        remittance_info.append(newline)
        remittance_info.append(their_reference)
        remittance_info.append(self.get_counterparty_reference(settlement))
        return ''.join(remittance_info)

    @staticmethod
    def get_counterparty_reference(settlement):
        """
        Get the counterparty reference
        """
        counter_party = settlement.Counterparty()
        if settlement.AdditionalInfo().Ext_CP_Ref_Sett():
            return str(settlement.AdditionalInfo().Ext_CP_Ref_Sett())
        elif counter_party.AdditionalInfo().Ext_CP_Ref():
            return str(counter_party.AdditionalInfo().Ext_CP_Ref())
        elif settlement.Trade() and settlement.Trade().YourRef():
            return str(settlement.Trade().YourRef())
        else:
            return ''

    # formatter
    def _format_remittance_information_70(self, val):
        """Formats the value provided by getter method"""
        if not self.use_operations_xml:
            val = self.format_MT103_field70(val, 35, 4)
        else:
            val = val.replace('newline', '\n')
        return str(val).upper()


class FMT103MessageHeader(FMT103OutBase.FMT103OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT103MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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
            return ''
        except:
            return ''

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
        if sub_network == 'SRS':
            return "{103:SRS}"
        return ''

    def receiver_logical_terminal_address(self):
        """
        LT code is hardcoded as X for sender
        """
        receivers_bic = ''
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'RECEIVER_BIC'])
        else:
            receivers_bic = get_receivers_bic(self.acm_obj)

        if self.acm_obj.Currency().Name() == 'ZAR':
            receivers_bic = self.get_counterparty_correspondent_address()

        if self.acm_obj.MTMessages() == '202COV':
            receivers_bic = self.acm_obj.CounterpartyAccountRef().Bic().Alias()

        terminal_address = self.logical_terminal_address(receivers_bic, "X")
        return terminal_address

    def get_counterparty_correspondent_address(self):
        """
        Gets Correspondent BIC address
        """
        counterparty_account = self.acm_obj.CounterpartyAccountRef()
        if counterparty_account:
            if counterparty_account.Bic2():
                return counterparty_account.Bic2().Alias()
            elif counterparty_account.Bic():
                return counterparty_account.Bic().Alias()
            else:
                raise ValueError('No BIC specified on account')

        raise ValueError('No account specified for Settlement')


class FMT103NetworkRules(FMT103OutBase.FMT103OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom=None):
        super(FMT103NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom)
