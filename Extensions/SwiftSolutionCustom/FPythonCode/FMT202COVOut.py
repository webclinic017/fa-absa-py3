"""----------------------------------------------------------------------------
MODULE:
    FMT200COVOut

DESCRIPTION:
    This module provides the customizable class for the FMT202COV outgoing implementation

CLASS:
    FMT200COV

VERSION: 3.0.3-0.5.3744
------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2021-01-26      FAOPS-1026      Tawanda Mukhalela       Martin Wortmann         Added Cpty Ref Check for Remittance Info
                                                                                Remapped 58A account to Intermediary1
2021-02-23      FAOPS-1034      Willie vd Bank          Martin Wortmann         Added FSwiftWriterUtils_Override to
                                                                                50F and 59F to limit the field length
                                                                                Updated 50F to remove incorrect /
2021-03-09      FAOPS-1027      Willie vd Bank          Martin Wortmann         Amended 50F to retrieve the
                                                                                correct info for a netted settlement.
------------------------------------------------------------------------------------------------------------------------
"""
import MT202COV
import acm
import xml.dom.minidom
from FSwiftMLUtils import accepts

import FMT202COVOutBase
import FInstitutionTransfersOutBase
import FSwiftWriterLogger
from FSwiftWriterEngine import validate_with
from FCashOutUtils import *
import FSwiftWriterUtils
import FSwiftWriterUtils_Override
import FMTCustomFunctions
from ChineseCommercialCode import CCC_simplified_writer, CCC_traditional_writer
from DocumentGeneral import get_bank_party_name, get_default_bank_country_code

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')


@accepts([acm.FSettlement, MT202COV.CTD_ANON, xml.dom.minidom.Document])
class FMT202COV(FMT202COVOutBase.FMT202COVBase):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FMT202COV, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

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
    get_ordering_institution_sequenceA_option (Tag-52 options:A/D)
    get_senders_correspondent_option (Tag-53 options:A/D)
    get_intermediary_option (Tag-56 options:A/D)
    get_account_with_institution_sequenceA_option (Tag-57 options:A/D)
    get_beneficiary_institution_option (Tag-58 options:A/D)
    get_ordering_customer_option (Tag-50 options:A/F/K)
    get_ordering_institution_sequenceB_option (Tag-52 options:A/D)
    get_account_with_institution_sequenceB_option (Tag-57 options:A/C/D)
    get_beneficiary_customer_option (Tag-59 options:A/NO OPTION/F)
    
    For example:
    def get_ordering_institution_sequenceA_option(self):
        condition = True
        if condition:
            return 'A'
        else:
            return 'D'

    """

    def get_beneficiary_customer_option(self):
        return 'F'

    def get_ordering_customer_option(self):
        return 'F'

    # formatter
    def _format_transaction_reference_20(self, val):
        seq_ref = 'FASC'
        seqnbr = self.acm_obj.Oid()
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
        else:
            raise ValueError('Could not find any Option for field 53')

    # getter
    def senders_correspondent_53B(self):
        """
        Returns dictionary as {'ACCOUNT':<value>, 'BIC':<value>}
        """
        return get_acquirer_correpondent_details(self.acm_obj)

    # formatter
    def _format_senders_correspondent_53B(self, val):
        """Formats the value provided by getter method"""
        senders_correspondent_account = val.get('ACCOUNT')
        senders_correspondent_bic = val.get('BIC')
        if not senders_correspondent_bic:
            raise ValueError('Missing Acquirer account Bic address for Field 53B')
        if not senders_correspondent_account:
            raise ValueError('Missing Acquirer account for Field 53B')

        return "/" + str(senders_correspondent_account)

    # validator
    @validate_with(MT202COV.MT202COV_SequenceA_GeneralInformation_53B_Type)
    def _validate_senders_correspondent_53B(self, val):
        """validates the value provided by formatter method"""
        return val

    # setter
    def _setsenders_correspondent_53B(self, val):
        """sets the value on python object"""
        self.swift_obj.SequenceA_GeneralInformation.SendersCorrespondent_B = val
        self.swift_obj.SequenceA_GeneralInformation.SendersCorrespondent_B.swiftTag = "53B"

    # formatter
    def _format_beneficiary_institution_58D(self, val):
        """Formats the value provided by getter method"""
        account = val.get('ACCOUNT')
        name = val.get('BENEFICIARY_INST_NAME')
        address = val.get('BENEFICIARY_INST_ADDRESS')

        temp_name = name
        temp_address = address
        char_set = ''
        lookup_temp = FMT202COVOutBase.lookup
        try:
            char_set = str(self.acm_obj.Counterparty().AdditionalInfo().TraditionalChinese())
        except Exception as e:
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

    # formatter
    def _format_ordering_customer_50F(self, val):
        """Formats the value provided by getter method"""
        party_identifier = val.get('PARTY_IDENTIFIER')
        name = val.get('NAME')
        address = val.get('ADDRESS')
        country_code = val.get('COUNTRY_CODE')
        town = val.get('TOWN')
        town = str(town)
        name_list, address_list, country_and_town_list = [], [], []

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
            return party_identifier + '\n' + value

        return value

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
            country_and_town_list = FSwiftWriterUtils.split_text_and_prefix(
                str(additional_details), 33, '3/')
        value = FSwiftWriterUtils_Override.allocate_space_for_name_and_address_with_constraint(name_list, address_list,
                                                                                      country_and_town_list)
        if account:
            account = '/' + str(account)
            value = account + '\n' + value
        return value

    # getter
    def ordering_institution_52A_sequenceA(self):
        return {}

    def ordering_institution_52A(self):
        return {}

    # getter
    def intermedairy_56A(self):
        return {}

    # formatter
    def _format_intermediary_56A(self, val):
        """
        Returning an empty string for 56A
        """
        return ""

    # getter
    def account_with_institution_57A_sequenceA(self):
        """
        Returns a dictionary as {'account':<value>, 'bic':<value>}
        """
        return get_counterpartys_intermediary_details(self.acm_obj)

    def account_with_institution_57A_sequenceB(self):
        return {}

    def instructed_amount_33B(self):
        return {}

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
            val = self.format_MT202COV_field70(val, 35, 4)
        else:
            val = val.replace('newline', '\n')
        return str(val).upper()

    # getter
    def beneficiary_institution_58A(self):
        """
        Returns dictionary as {'ACCOUNT':<value>, 'BIC':<value>}
        """
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
            val = get_counterpartys_intermediary_details(self.acm_obj)
            val['BENEFICIARY_INST_BIC'] = self._get_beneficiary_institution_bic(self.acm_obj)
            return val

    def _get_beneficiary_institution_bic(self, acm_obj):
        """
        helper method returns bic of beneficiary institution
        """
        if acm_obj.CounterpartyAccountRef().Bic() and acm_obj.CounterpartyAccountRef().Bic().Alias():
            return acm_obj.CounterpartyAccountRef().Bic().Alias()
        return ''

    # formatter
    def _format_account_with_institution_57A_sequenceA(self, val):
        """
        Formats the value provided by getter method
        """
        bic = val.get('BIC')
        return bic if bic else None


class FMT202COVMessageHeader(FMT202COVOutBase.FMT202COVOutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT202COVMessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

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
            seqref = str(get_settlement_reference_prefix()) + 'C'
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


class FMT202COVNetworkRules(FMT202COVOutBase.FMT202COVOutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT202COVNetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)
