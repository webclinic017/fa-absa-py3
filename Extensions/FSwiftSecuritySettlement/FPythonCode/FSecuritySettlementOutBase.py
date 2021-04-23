"""----------------------------------------------------------------------------
MODULE:
    FSecuritySettlementOutBase

DESCRIPTION:
    This module provides the base class for the security settlement outgoing implementation.
    It contains the common mwthods across security settlement outgoing solution.

CLASS:
    FSecuritySettlementOutBase

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
from FMTOutBase import FMTOutBase
import FSwiftWriterUtils
import FSecuritySettlementOutUtils
import FSwiftWriterLogger
import FSwiftMLUtils
import acm

notifier = FSwiftWriterLogger.FSwiftWriterLogger('SecSetOut', 'FSecuritySettlementOutNotify_Config')

class FSecuritySettlementOutBase(FMTOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FSecuritySettlementOutBase, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # ------------------ quantity of instrument-36B-----------------------

    def quantity_of_instrument_36B(self):
        '''
        Returns a list of dictionaries as [{k1:v1,k2:v2},{k1:v3,k2:v4}]
        '''
        if self.use_operations_xml:
            quantity_blocks = FSwiftWriterUtils.get_block_xml_tags(self.swift_metadata_xml_dom, 'QUANTITY',
                                                                   ['QUANTITY_TYPE_CODE', 'QUANTITY_QUANTITY'])
        else:
            quantity = {}
            quantity_blocks = []
            quantity['QUANTITY_TYPE_CODE'] = FSecuritySettlementOutUtils.get_quantity_type_code()
            quantity['QUANTITY_QUANTITY'] = FSecuritySettlementOutUtils.get_quantity(self.acm_obj)
            quantity_blocks.append(quantity)
        return quantity_blocks

    def _format_quantity_of_instrument_36B(self, val):
        quantity_of_instrument = []
        for each_block in val:
            quantity_of_instrument.append(":SETT//" + str(each_block['QUANTITY_TYPE_CODE']) + "/" + str(
                each_block['QUANTITY_QUANTITY']).replace('.', ','))
        return quantity_of_instrument

    def _validate_quantity_of_instrument_36B(self, val_list):
        err_msgs = []
        values = []
        for each_val in val_list:
            val = self._validate_quantity_of_instrument_36B_items(each_val)
            values.append(val)
        return values

    # ------------------ date time -98A-----------------------

    def get_settlement_datetime_98_option(self):
        """Returns default option if override is not provided
        :return: str; option choice as string
        """
        return 'A'

    def date_time(self):
        '''
        Returns a list of dictionaries as [{'DateTime_A':{k1:v1,k2:v2}},{'DateTime_A':{k1:v3,k2:v4}}]
        '''
        val_list = []
        if self.use_operations_xml:
            settlement_datetime_blocks = FSwiftWriterUtils.get_block_xml_tags(self.swift_metadata_xml_dom,
                                                                              'SETTLEMENT_DATETIME',
                                                                              ['SETTLEMENT_DATETIME_OPTION',
                                                                               'SETTLEMENT_DATETIME_QUALIFIER',
                                                                               'SETTLEMENT_DATETIME_DATE'])
            for each_block in settlement_datetime_blocks:
                val_dict = {}
                if each_block['SETTLEMENT_DATETIME_OPTION'] == 'A':
                    val_dict['DateTime_A'] = self.date_time_98A(each_block)
                val_list.append(val_dict)
        else:
            val_dict = {}
            each_block = {}
            each_block['SETTLEMENT_DATETIME_OPTION'] = self.get_settlement_datetime_98_option()
            each_block['SETTLEMENT_DATETIME_QUALIFIER'] = FSecuritySettlementOutUtils.get_settlement_datetime_qualifier()
            each_block['SETTLEMENT_DATETIME_DATE'] = FSecuritySettlementOutUtils.get_settlement_datetime_date(self.acm_obj)
            if each_block['SETTLEMENT_DATETIME_OPTION'] == 'A':
                val_dict['DateTime_A'] = self.date_time_98A(each_block)
            else:
                notifier.ERROR("%s Option %s is not supported for tag %s. Mapping default option: A" %
                               (self.swift_message_type, each_block['SETTLEMENT_DATETIME_OPTION'], 'SettlementDateTime_98a'))
                each_block['SETTLEMENT_DATETIME_OPTION'] = 'A'
                val_dict['DateTime_A'] = self.date_time_98A(each_block)
            val_list.append(val_dict)

            val_dict = {}
            each_block = {}
            each_block['SETTLEMENT_DATETIME_OPTION'] = self.get_settlement_datetime_98_option()
            each_block['SETTLEMENT_DATETIME_QUALIFIER'] = FSecuritySettlementOutUtils.get_trade_datetime_qualifier()
            each_block['SETTLEMENT_DATETIME_DATE'] = FSecuritySettlementOutUtils.get_trade_datetime_date(self.acm_obj)
            if each_block['SETTLEMENT_DATETIME_OPTION'] == 'A':
                val_dict['DateTime_A'] = self.date_time_98A(each_block)
            val_list.append(val_dict)
        return val_list

    def _format_date_time(self, val):
        format_list = []
        for each_val in val:
            format_dict = {}
            if 'DateTime_A' in each_val:
                format_dict['DateTime_A'] = self._format_date_time_98A(each_val['DateTime_A'])
                format_list.append(format_dict)
        return format_list

    def _validate_date_time(self, val_list):
        err_msg = ''
        valid_list = []
        for each_val in val_list:
            valid_dict = {}
            if 'DateTime_A' in each_val:
                val = self._validate_date_time_98A(each_val['DateTime_A'])
                if val:
                    valid_dict['DateTime_A'] = val
            valid_list.append(valid_dict)
        return valid_list

    # ------------------ date time 98A -----------------------
    def date_time_98A(self, sett_datetime_dict):
        '''
        Returns a dictionary as {key1:value1, key2:value2}
        '''
        values_dict = {}
        date = sett_datetime_dict['SETTLEMENT_DATETIME_DATE']
        qualifier = sett_datetime_dict['SETTLEMENT_DATETIME_QUALIFIER']
        values_dict['date'] = date
        values_dict['qualifier'] = qualifier
        return values_dict

    def _format_date_time_98A(self, val):
        date = val.get('date')
        qualifier = val.get('qualifier')
        date_format = '%Y%m%d'
        yyyymmdd_date = FSwiftWriterUtils.format_date(date, date_format)
        val = ":" + str(qualifier) + '//' + str(yyyymmdd_date)
        return val

    # ------------------ account -----------------------

    def get_account_97_option(self):
        """Returns default option if override is not provided
        :return: str; option choice as string
        """
        return 'A'

    def account(self):
        '''
        Returns a list of dictionaries as [{'Account_A':{k1:v1}},{'Account_A':{k1:v2}}]
        '''
        val_list = []
        if self.use_operations_xml:
            account_blocks = FSwiftWriterUtils.get_block_xml_tags(self.swift_metadata_xml_dom, 'ACCOUNT',
                                                                  ['ACCOUNT_OPTION', 'ACCOUNT_QUALIFIER', 'ACCOUNT_NUMBER'])
            for each_block in account_blocks:
                val_dict = {}
                if each_block and each_block['ACCOUNT_OPTION'] == 'A':
                    val_dict['Account_A'] = self.account_97A(each_block)
                val_list.append(val_dict)
        else:
            val_dict = {}
            each_block = {}
            each_block['ACCOUNT_OPTION'] = self.get_account_97_option()
            each_block['ACCOUNT_QUALIFIER'] = FSecuritySettlementOutUtils.get_account_qualifier()
            each_block['ACCOUNT_NUMBER'] = FSecuritySettlementOutUtils.get_account_number(self.acm_obj)
            if each_block and each_block['ACCOUNT_OPTION'] not in ['A']:
                    notifier.ERROR("%s Option %s is not supported for tag %s. Mapping default option: A" %
                                   (self.swift_message_type, each_block['ACCOUNT_OPTION'], 'Account_97a'))
                    each_block['ACCOUNT_OPTION'] = 'A'
            if each_block and each_block['ACCOUNT_OPTION'] == 'A':
                    val_dict['Account_A'] = self.account_97A(each_block)
            val_list.append(val_dict)
        return val_list

    def _format_account(self, val):
        format_list = []
        for each_val in val:
            format_dict = {}
            if 'Account_A' in each_val:
                format_dict['Account_A'] = self._format_account_97A(each_val['Account_A'])
            format_list.append(format_dict)
        return format_list

    def _validate_account(self, val_list):
        err_msg = ''
        valid_list = []
        for each_val in val_list:
            valid_dict = {}
            if 'Account_A' in each_val:
                val = self._validate_account_97A(each_val['Account_A'])
                if val:
                    valid_dict['Account_A'] = val
            valid_list.append(valid_dict)
        return valid_list

    # ------------------ account - 97A -----------------------
    def account_97A(self, account_dict):
        '''
        Returns a dictionary as {k1:v1, k2:v2}
        '''
        values_dict = {}
        qualifier = account_dict['ACCOUNT_QUALIFIER']
        number = account_dict['ACCOUNT_NUMBER']
        values_dict['qualifier'] = qualifier
        values_dict['number'] = number
        return values_dict

    def _format_account_97A(self, val):
        qualifier = val.get('qualifier')
        number = val.get('number')
        account_A = ":" + str(qualifier) + "//" + str(number)
        return account_A

    # ------------------ function of message - 23G -----------------------

    def function_of_message_23G(self):
        '''
        Returns a string containing value of fuction_of_message
        '''
        if self.use_operations_xml:
            function_of_message = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'FUNCTION_OF_MESSAGE'])
        else:
            function_of_message = FSecuritySettlementOutUtils.get_function_of_message(self.acm_obj)
        return function_of_message

    def _format_function_of_message_23G(self, val):
        return val

    # ------------------ place of safekeeping - 94F-----------------------

    def place_of_safekeeping(self):
        '''
        Returns a list of dictionaries as [{PlaceOfSafekeeping_F:{k1:v1,k2:v2}},{PlaceOfSafekeeping_F:{k1:v3,k2:v4}}]
        '''
        val_list = []
        if self.use_operations_xml:
            place_of_safekeeping_blocks = FSwiftWriterUtils.get_block_xml_tags(self.swift_metadata_xml_dom,
                                                                               'PLACE_OF_SAFEKEEPING',
                                                                               ['PLACE_OF_SAFEKEEPING_OPTION',
                                                                                'PLACE_OF_SAFEKEEPING_QUALIFIER',
                                                                                'PLACE_OF_SAFEKEEPING_PLACE_CODE',
                                                                                'PLACE_OF_SAFEKEEPING_IDENTIFIER_CODE'],
                                                                               ignore_absense=True)
            for each_block in place_of_safekeeping_blocks:
                val_dict = {}
                if each_block and each_block['PLACE_OF_SAFEKEEPING_OPTION'] == 'F':
                    val_dict['PlaceOfSafekeeping_F'] = self.place_of_safekeeping_94F(each_block)
                val_list.append(val_dict)
        return val_list

    def _format_place_of_safekeeping(self, val):
        format_list = []
        for each_val in val:
            format_dict = {}
            if 'PlaceOfSafekeeping_F' in each_val:
                format_dict['PlaceOfSafekeeping_F'] = self._format_place_of_safekeeping_94F(
                    each_val['PlaceOfSafekeeping_F'])
            format_list.append(format_dict)
        return format_list

    def _validate_place_of_safekeeping(self, val_list):
        err_msg = ''
        valid_list = []
        for each_val in val_list:
            valid_dict = {}
            if 'PlaceOfSafekeeping_F' in each_val:
                val = self._validate_place_of_safekeeping_94F(each_val['PlaceOfSafekeeping_F'])
                if val:
                    valid_dict['PlaceOfSafekeeping_F'] = val
            valid_list.append(valid_dict)
        return valid_list

    # ------------------ place of safekeeping 94F -----------------------
    def place_of_safekeeping_94F(self, place_of_safekeeping_dict):
        '''
        Returns a dictionary as {k1:v1,k2:v2}
        '''
        values_dict = {}
        qualifier = place_of_safekeeping_dict['PLACE_OF_SAFEKEEPING_QUALIFIER']
        place_code = place_of_safekeeping_dict['PLACE_OF_SAFEKEEPING_PLACE_CODE']
        identifier = place_of_safekeeping_dict['PLACE_OF_SAFEKEEPING_IDENTIFIER_CODE']
        values_dict['qualifier'] = qualifier
        values_dict['place_code'] = place_code
        values_dict['identifier'] = identifier
        return values_dict

    def _format_place_of_safekeeping_94F(self, val):
        qualifier = val.get('qualifier')
        place_code = val.get('place_code')
        identifier = val.get('identifier')
        place_of_safekeeping_F = str(qualifier) + "//" + \
                                 str(place_code) + "/" + \
                                 str(identifier)
        return place_of_safekeeping_F

    # ------------------ settlement parties -----------------------

    def get_party_95_option(self):
        """Returns option override if implemented
        :return: str; option choice as string
        """
        return 'P'

    def get_party_safekeeping_97_option(self):
        """Returns default option if override is not provided
        :return: str; option choice as string
        """
        return 'A'

    def _format_settlement_parties(self, val):
        format_list = []
        for each_val in val:
            format_dict = {}
            if 'PARTY_P' in each_val:
                format_dict['PARTY_P'] = self._format_settlement_party_95P(each_val['PARTY_P'])
            if 'PARTY_C' in each_val:
                format_dict['PARTY_C'] = self._format_settlement_party_95C(each_val['PARTY_C'])
            if 'PARTY_Q' in each_val:
                format_dict['PARTY_Q'] = self._format_settlement_party_95Q(each_val['PARTY_Q'])
            if 'PARTY_R' in each_val:
                format_dict['PARTY_R'] = self._format_settlement_party_95R(each_val['PARTY_R'])
            if 'SafekeepingAccount_A' in each_val:
                format_dict['SafekeepingAccount_A'] = self._format_party_safekeeping_account_97A(
                    each_val['SafekeepingAccount_A'])
            format_list.append(format_dict)
        return format_list

    def _validate_settlement_parties(self, val_list):
        err_msg = ''
        valid_list = []
        for each_val in val_list:
            valid_dict = {}
            if 'PARTY_P' in each_val:
                val = self._validate_settlement_party_95P(each_val['PARTY_P'])
                if val:
                    valid_dict['PARTY_P'] = val
            if 'PARTY_C' in each_val:
                val = self._validate_settlement_party_95C(each_val['PARTY_C'])
                if val:
                    valid_dict['PARTY_C'] = val
            if 'PARTY_Q' in each_val:
                val = self._validate_settlement_party_95Q(each_val['PARTY_Q'])
                if val:
                    valid_dict['PARTY_Q'] = val
            if 'PARTY_R' in each_val:
                val = self._validate_settlement_party_95R(each_val['PARTY_R'])
                if val:
                    valid_dict['PARTY_R'] = val
            if 'SafekeepingAccount_A' in each_val:
                val = self._validate_party_safekeeping_account_97A(each_val['SafekeepingAccount_A'])
                if val:
                    valid_dict['SafekeepingAccount_A'] = val
            valid_list.append(valid_dict)
        return valid_list

    # ------------------ settlement parties 95P -----------------------
    def settlement_party_95P(self, party_dict):
        '''
        Returns a dictionary as {k1:v1,k2:v2}
        '''
        values_dict = {}
        qualifier = party_dict['PARTY_QUALIFIER']
        code = party_dict['PARTY_IDENTIFIER_CODE']
        values_dict['qualifier'] = qualifier
        values_dict['code'] = code
        return values_dict

    def _format_settlement_party_95P(self, val):
        qualifier = val.get('qualifier')
        code = val.get('code')
        if not code:    # SPR 405530 in Prime, Prime > 2017.3 returns PARTY_IDENTIFIER_CODE in XML but < 2017.3 returns empty
            counter_party_account = self.acm_obj.CounterpartyAccountRef()
            if counter_party_account:
                code = FSwiftMLUtils.get_party_bic(counter_party_account)
        settlement_party_P = ":" + str(qualifier) + "//" + str(code)
        return settlement_party_P

    # ------------------ settlement parties 95R -----------------------
    def settlement_party_95R(self, party_dict):
        '''
        Returns a dictionary as {k1:v1,k2:v2}
        '''
        values_dict = {}
        qualifier = party_dict['PARTY_QUALIFIER']
        source_scheme = party_dict['PARTY_DATA_SOURCE_SCHEME']
        code = party_dict['PARTY_PROPRIETARY_CODE']
        values_dict['qualifier'] = qualifier
        values_dict['source_scheme'] = source_scheme
        values_dict['code'] = code
        return values_dict

    def _format_settlement_party_95R(self, val):
        qualifier = val.get('qualifier')
        source_scheme = val.get('source_scheme')
        code = val.get('code')
        settlement_party_R = ":" + str(qualifier) + "/" + str(source_scheme) + "/" + str(code)
        return settlement_party_R

    # ------------------ settlement parties 95C -----------------------
    def settlement_party_95C(self, party_dict):
        '''
        Returns a dictionary as {k1:v1,k2:v2}
        '''
        values_dict = {}
        qualifier = party_dict['PARTY_QUALIFIER']
        code = party_dict['PARTY_COUNTRY_CODE']
        values_dict['qualifier'] = qualifier
        values_dict['code'] = code
        return values_dict

    def _format_settlement_party_95C(self, val):
        qualifier = val.get('qualifier')
        code = val.get('code')
        settlement_party_C = ":" + str(qualifier) + "//" + str(code)
        return settlement_party_C

    # ------------------ settlement parties 95Q -----------------------
    def settlement_party_95Q(self, party_dict):
        '''
        Returns a dictionary as {k1:v1,k2:v2}
        '''
        values_dict = {}
        qualifier = party_dict['PARTY_QUALIFIER']
        name = party_dict['PARTY_NAME']
        address = party_dict['PARTY_ADDRESS']
        values_dict['qualifier'] = qualifier
        values_dict['name'] = name
        values_dict['address'] = address
        return values_dict

    def _format_settlement_party_95Q(self, val):
        qualifier = val.get('qualifier')
        name = val.get('name')
        address = val.get('address')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
        settlement_party_Q = ":" + str(qualifier) + "//" + val
        return settlement_party_Q

    # ------------------ party safekeeping account 97A -----------------------
    def party_safekeeping_account_97A(self, party_dict):
        '''
        Returns a dictionary as {k1:v1,k2:v2}
        '''
        values_dict = {}
        qualifier = party_dict['PARTY_SAFEKEEPING_QUALIFIER']
        account = party_dict['PARTY_SAFEKEEPING_ACCOUNT']
        values_dict['qualifier'] = qualifier
        values_dict['account'] = account
        return values_dict

    def _format_party_safekeeping_account_97A(self, val):
        qualifier = val.get('qualifier')
        account = val.get('account')
        party_safekeeping_account_A = ":" + str(qualifier) + "//" + str(account)
        return party_safekeeping_account_A

    # ------------------ indicator-22F -----------------------

    def indicator_22F(self):
        '''
        Returns a list of dictionaries as [{k1:v1,k2:v2},{k1:v3,k2:v4}]
        '''
        if self.use_operations_xml:
            indicator_blocks = FSwiftWriterUtils.get_block_xml_tags(self.swift_metadata_xml_dom, 'INDICATOR',
                                                                ['INDICATOR_QUALIFIER', 'INDICATOR_INDICATOR'])
        else:
            indicator_blocks = []
            indicators = FSecuritySettlementOutUtils.get_indicators(self.acm_obj)
            for indicator_pair in indicators:
                indicator_block = {}
                indicator_block['INDICATOR_QUALIFIER'] =  FSecuritySettlementOutUtils.get_qualifier(indicator_pair)
                indicator_block['INDICATOR_INDICATOR'] =  FSecuritySettlementOutUtils.get_indicator(indicator_pair)
                indicator_blocks.append(indicator_block)
        return indicator_blocks

    def _format_indicator_22F(self, val):
        indicator_values = []
        for each_block in val:
            indicator_values.append(
                ":" + str(each_block['INDICATOR_QUALIFIER']) + "//" + str(each_block["INDICATOR_INDICATOR"]))
        return indicator_values

    def _validate_indicator_22F(self, val_list):
        err_msgs = []
        values = []
        for each_val in val_list:
            val = self._validate_indicator_22F_items(each_val)
            values.append(val)
        return values

    # ------------------ identification of financial instruments-35B-----------------------

    def identification_of_financial_ins_35B(self):
        '''
        Returns a dictionary as {key1:value1, key2:value2}
        '''
        values_dict = {}
        if self.use_operations_xml:
            isin = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'INSTRUMENT_ISIN'])
            description_of_security = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                               ['SWIFT', 'DESCRIPTION_OF_SECURITY'],
                                                                               ignore_absense=True)
            values_dict['isin'] = isin
            values_dict['description_of_security'] = description_of_security
        else:
            values_dict['isin'] = FSecuritySettlementOutUtils.get_instrument_ISIN(self.acm_obj)
            values_dict['description_of_security'] = FSecuritySettlementOutUtils.get_description_of_security(self.acm_obj)
        return values_dict

    def _format_identification_of_financial_ins_35B(self, val):
        isin = val.get('isin')
        description_of_security = val.get('description_of_security')
        if description_of_security:
            lines = FSwiftWriterUtils.split_text_on_character_limit(description_of_security, 35)
            description_of_security = FSwiftWriterUtils.allocate_space_for_n_lines(4, lines)
            identification_of_financial_ins = str(isin) + "\n" + str(description_of_security)
        else:
            identification_of_financial_ins = str(isin) + "\n"
        return str(identification_of_financial_ins)

    # ------------------ linkage details   -----------------------

    def linkages_20C_16R(self):
        '''
        Returns a dictionary as {key:value, key1:value1}
        '''
        values_dict = {}
        if self.use_operations_xml:
            function_of_message = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'FUNCTION_OF_MESSAGE'])
            linkage_qualifier = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'LINKAGE', 'LINKAGE_QUALIFIER'],
                                                                         ignore_absense=True)
            linkage_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'LINKAGE', 'LINKAGE_REFERENCE'],
                                                                         ignore_absense=True)
            senders_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SETTLEMENT', 'SEQNBR'])
            seq_ref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])

            values_dict['function_of_message'] = function_of_message
            values_dict['linkage_qualifier'] = linkage_qualifier
            values_dict['linkage_reference'] = linkage_reference
            values_dict['senders_reference'] = senders_reference
            values_dict['seq_ref'] = seq_ref
        else:
            function_of_message = FSecuritySettlementOutUtils.get_function_of_message(self.acm_obj)
            linkage_qualifier = FSecuritySettlementOutUtils.get_linkage_qualifier(self.acm_obj)
            linkage_reference = FSecuritySettlementOutUtils.get_linkage_reference(self.acm_obj)
            values_dict['function_of_message'] = function_of_message
            values_dict['linkage_qualifier'] = linkage_qualifier
            values_dict['linkage_reference'] = linkage_reference
            values_dict['senders_reference'] = self.acm_obj.Oid()
            values_dict['seq_ref'] = FSecuritySettlementOutUtils.get_settlement_reference_prefix()
        return values_dict

    def _check_condition_set_linkages_20C_16R(self):
        if self.use_operations_xml:
            function_of_message = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'FUNCTION_OF_MESSAGE'])
        else:
            function_of_message = FSecuritySettlementOutUtils.get_function_of_message(self.acm_obj)
        if function_of_message == "CANC":
            return True
        return False

    # ------------------- senders reference - 20C-------------------

    def senders_message_reference_20C(self):
        '''
        Returns a dictionary as {'senders_reference':value1, 'seq_ref':value2}
        '''
        values_dict = {}
        if self.use_operations_xml:
            senders_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SETTLEMENT', 'SEQNBR'])
            seq_ref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
            values_dict['senders_reference'] = senders_reference
            values_dict['seq_ref'] = seq_ref
        else:
            values_dict = {}
            values_dict['senders_reference'] = self.acm_obj.Oid()
            values_dict['seq_ref'] = FSecuritySettlementOutUtils.get_settlement_reference_prefix()
        return values_dict

    def _format_senders_message_reference_20C(self, val):
        senders_reference = val.get('senders_reference')
        seq_ref = val.get('seq_ref')
        sett_obj = acm.FSettlement[str(senders_reference)]
        if senders_reference:
            val = ":SEME//%s-%s-%s" % (
            str(seq_ref), str(senders_reference), str(FSecuritySettlementOutUtils.get_message_version_number(sett_obj)))
            return str(val)

    # ------------------ amounts  block -----------------------

    # block getter
    def amounts(self):
        """ Returns a dictionary as [{'AMOUNT_BLOCKS': [list_of _dict_of amounts], 'FLAG_BLOCKS': [list_of_dict_of_flags]}]
        """
        amounts_block_details = dict()
        amounts_block_details['AMOUNT_BLOCKS'] = self.amount_19A()
        amounts_block_details['FLAG_BLOCKS'] = self.flag_17B()

        return amounts_block_details

    def _format_amounts(self, val_dict):
        """Format amounts block"""
        amounts_block = dict()

        amounts_block['AMOUNT_BLOCKS'] = self._format_amounts_19A(val_dict.get('AMOUNT_BLOCKS'))
        amounts_block['FLAG_BLOCKS'] = self._format_flag_17B(val_dict.get('FLAG_BLOCKS'))
        return amounts_block

    def _validate_amounts(self, val_dict):
        """ Validate amount block fields"""
        val_dict['AMOUNT_BLOCKS'] = self._validate_amount_list_19A(val_dict.get('AMOUNT_BLOCKS'))
        val_dict['FLAG_BLOCKS'] = self._validate_flag_list_17B(val_dict.get('FLAG_BLOCKS'))
        return val_dict


    def amount_19A(self):
        """Returns a list of dictionaries as [{k1:v1,k2:v2},{k1:v1,k2:v2}]"""
        if self.use_operations_xml:
            amount_blocks = FSwiftWriterUtils.get_block_xml_tags(self.swift_metadata_xml_dom, 'AMOUNT',
                                                                 ['AMOUNT_QUALIFIER', 'AMOUNT_SIGN',
                                                                  'AMOUNT_CURRENCY_CODE',
                                                                  'AMOUNT_AMOUNT'])
        else:
            amount_blocks = FSecuritySettlementOutUtils.get_amount_details(self.acm_obj, self.swift_message_type)

        return amount_blocks

    def flag_17B(self):
        """get the settlement amount flag"""
        flag_blocks = FSecuritySettlementOutUtils.get_amount_flags(self.acm_obj, self.swift_message_type)
        return flag_blocks

    def _format_amounts_19A(self, val):
        amount_fields = list()
        for each_block in val:
            amount_field = ":" + str(each_block['AMOUNT_QUALIFIER']) + "//" + str(each_block["AMOUNT_CURRENCY_CODE"])\
                           + str(each_block["AMOUNT_AMOUNT"]).replace('.', ',')

            amount_fields.append(amount_field)
        return amount_fields

    def _format_flag_17B(self, val):
        flag_fields = list()
        for each_block in val:
            flag_field = ":" + str(each_block["QUALIFIER"]) + "//" + str(each_block["FLAG"])
            flag_fields.append(flag_field)
        return flag_fields


    def _validate_amount_list_19A(self, val_list):
        err_msgs = []
        values = []
        for each_val in val_list:
            self._validate_amounts_19A(each_val)
            values.append(each_val)
        return values

    def _validate_flag_list_17B(self, val_list):
        err_msgs = []
        values = []
        for each_val in val_list:
            self._validate_flag_17B(each_val)
            values.append(each_val)
        return values


    # ------------------ SubSequence B1 date time - 98A -----------------------

    def subsequenceb1_date_time(self):
        """returns a list containing the dictionary of values of Qualifier and Date"""
        date_time_list = []
        date_time_dict = {}
        date_time_block = {}
        date_time_block['SETTLEMENT_DATETIME_QUALIFIER'] = FSecuritySettlementOutUtils.get_maturity_datetime_qualifier()
        date_time_block['SETTLEMENT_DATETIME_DATE'] = FSecuritySettlementOutUtils.get_maturity_datetime_date(self.acm_obj)
        date_time_dict['DateTime'] = self.subsequenceb1_date_time_98A(date_time_block)
        date_time_list.append(date_time_dict)

        date_time_dict = {}
        date_time_block = {}
        date_time_block['SETTLEMENT_DATETIME_QUALIFIER'] = FSecuritySettlementOutUtils.get_issue_datetime_qualifier()
        date_time_block['SETTLEMENT_DATETIME_DATE'] = FSecuritySettlementOutUtils.get_issue_datetime_date(self.acm_obj)
        date_time_dict['DateTime'] = self.subsequenceb1_date_time_98A(date_time_block)
        date_time_list.append(date_time_dict)
        return date_time_list

    def _format_subsequenceb1_date_time(self, date_time_values):
        """returns list of formatted values of provided input"""
        date_time_list = []
        for each_val in date_time_values:
            date_time_dict = {}
            if 'DateTime' in each_val:
                date_time_dict['DateTime'] = self._format_subsequenceb1_date_time_98A(each_val['DateTime'])
                date_time_list.append(date_time_dict)
        return date_time_list

    def _validate_subsequenceb1_date_time(self, date_time_values):
        """returns list of validated values"""
        err_msg = ''
        date_time_list = []
        for each_val in date_time_values:
            date_time_dict = {}
            if 'DateTime' in each_val:
                val = self._validate_subsequenceb1_date_time_98A(each_val['DateTime'])
                if val:
                    date_time_dict['DateTime'] = val
            date_time_list.append(date_time_dict)
        return date_time_list

    def _check_condition_set_subsequenceb1_date_time(self):
        """return True or False depending on the condition provided"""
        return False

    def _set_subsequenceb1_date_time(self, date_time_values):
        """calls actual setter APIs depending on the provided input"""
        for each_val in date_time_values:
            if 'DateTime' in each_val:
                self._setsubsequenceb1date_time_98A(each_val['DateTime'])

    def subsequenceb1_date_time_98A(self, sett_datetime_dict):
        """Returns a dictionary with values of Qualifier and Date"""
        date_time_dict = {}
        date = sett_datetime_dict['SETTLEMENT_DATETIME_DATE']
        qualifier = sett_datetime_dict['SETTLEMENT_DATETIME_QUALIFIER']
        date_time_dict['date'] = date
        date_time_dict['qualifier'] = qualifier
        return date_time_dict

    def _format_subsequenceb1_date_time_98A(self, date_time_values):
        """returns formatted values of provided input"""
        date = date_time_values.get('date')
        qualifier = date_time_values.get('qualifier')
        date_format = '%Y%m%d'
        yyyymmdd_date = FSwiftWriterUtils.format_date(date, date_format)
        date_time = ":" + str(qualifier) + '//' + str(yyyymmdd_date)
        return date_time

    def _setsubsequenceb1date_time_98A(self, date_time_values):
        """sets the provided tag and value in python object"""
        self.swift_obj.SequenceB_TradeDetails.SubSequenceB1_FinancialInstrumentAttributes.Date.append(date_time_values)
        self.swift_obj.SequenceB_TradeDetails.SubSequenceB1_FinancialInstrumentAttributes.Date[-1].swiftTag = "98A"

    # ------------------ SubSequence B1 rate - 92A -----------------------

    def subsequenceb1_rate(self):
        """returns a list containing the dictionary of values of Qualifier and rate"""
        rate_list = []
        rate_dict = {}
        rate_block = {}
        rate_block['SETTLEMENT_RATE_QUALIFIER'] = FSecuritySettlementOutUtils.get_rate_qualifier()
        rate_block['SETTLEMENT_RATE'] = FSecuritySettlementOutUtils.get_rate(self.acm_obj)
        rate_dict['Rate'] = self.subsequenceb1_rate_92A(rate_block)
        rate_list.append(rate_dict)
        return rate_list

    def _format_subsequenceb1_rate(self, rate_values):
        """returns list of formatted values of provided input"""
        rate_list = []
        for each_val in rate_values:
            rate_dict = {}
            if 'Rate' in each_val:
                rate_dict['Rate'] = self._format_subsequenceb1_rate_92A(each_val['Rate'])
                rate_list.append(rate_dict)
        return rate_list

    def _validate_subsequenceb1_rate(self, rate_values):
        """returns list of validated values"""
        err_msg = ''
        rate_list = []
        for each_val in rate_values:
            rate_dict = {}
            if 'Rate' in each_val:
                val = self._validate_subsequenceb1_rate_92A(each_val['Rate'])
                if val:
                    rate_dict['Rate'] = val
            rate_list.append(rate_dict)
        return rate_list

    def _check_condition_set_subsequenceb1_rate(self):
        """return True or False depending on the condition provided"""
        return False

    def _set_subsequenceb1_rate(self, rate_values):
        """calls actual setter APIs depending on the provided input"""
        for each_val in rate_values:
            if 'Rate' in each_val:
                self._setsubsequenceb1rate_92A(each_val['Rate'])

    def subsequenceb1_rate_92A(self, sett_rate_dict):
        """Returns a dictionary with values of Qualifier and rate"""
        rate_dict = {}
        rate = sett_rate_dict['SETTLEMENT_RATE']
        qualifier = sett_rate_dict['SETTLEMENT_RATE_QUALIFIER']
        rate_dict['rate'] = rate
        rate_dict['qualifier'] = qualifier
        return rate_dict

    def _format_subsequenceb1_rate_92A(self, rate_values):
        """returns formatted values of provided input"""
        rate = rate_values.get('rate')
        rate = FSecuritySettlementOutUtils.represent_negative_amount(rate)
        qualifier = rate_values.get('qualifier')
        rate_value = ":" + str(qualifier) + '//' + str(rate)
        return rate_value

    def _setsubsequenceb1rate_92A(self, rate_values):
        """sets the provided tag and value in python object"""
        self.swift_obj.SequenceB_TradeDetails.SubSequenceB1_FinancialInstrumentAttributes.Rate.append(rate_values)
        self.swift_obj.SequenceB_TradeDetails.SubSequenceB1_FinancialInstrumentAttributes.Rate[-1].swiftTag = "92A"

    # ------------------ type of financial instrument - 12C -----------------------

    def type_of_financial_instrument(self):
        """returns a list containing the dictionary of values of Qualifier and CFI Code or ISITC Code"""
        type_of_financial_instrument_list = []
        type_of_financial_instrument_dict = {}
        type_of_financial_instrument_block = {}
        type_of_financial_instrument_block['INSTRUMENT_TYPE_CFI_CODE'] = None
        type_of_financial_instrument_block['INSTRUMENT_TYPE_ISITC_CODE'] = None
        type_of_financial_instrument_block['INSTRUMENT_TYPE_OPTION'] = None

        type_of_financial_instrument_block['INSTRUMENT_TYPE_QUALIFIER'] = FSecuritySettlementOutUtils.get_instrument_type_qualifier()

        if self.cfi_code:
            type_of_financial_instrument_block['INSTRUMENT_TYPE_CFI_CODE'] = self.cfi_code
            type_of_financial_instrument_block['INSTRUMENT_TYPE_OPTION'] = 'C'
        if self.isitc_code:
            type_of_financial_instrument_block['INSTRUMENT_TYPE_ISITC_CODE'] = self.isitc_code
            type_of_financial_instrument_block['INSTRUMENT_TYPE_OPTION'] = 'A'

        if type_of_financial_instrument_block['INSTRUMENT_TYPE_OPTION'] == 'A':
            type_of_financial_instrument_dict['TypeOfInstrument'] = self.type_of_instrument_12A(type_of_financial_instrument_block)
        elif type_of_financial_instrument_block['INSTRUMENT_TYPE_OPTION'] == 'C':
            type_of_financial_instrument_dict['TypeOfInstrument'] = self.type_of_instrument_12C(type_of_financial_instrument_block)

        type_of_financial_instrument_list.append(type_of_financial_instrument_dict)
        return type_of_financial_instrument_list

    def _format_type_of_financial_instrument(self, fin_ins_values):
        """returns list of formatted values of provided input"""
        type_of_financial_instrument_list = []
        for each_val in fin_ins_values:
            type_of_financial_instrument_dict = {}
            type_of_instrument = each_val.get('TypeOfInstrument')
            if type_of_instrument:
                option = type_of_instrument.get('option')
                if option in ['A', 'C']:
                    if option == 'A':
                        type_of_financial_instrument_dict['TypeOfInstrument'] = self._format_type_of_instrument_12A(type_of_instrument)
                    else:
                        type_of_financial_instrument_dict['TypeOfInstrument'] = self._format_type_of_instrument_12C(type_of_instrument)
                    type_of_financial_instrument_dict['option'] = option
                    type_of_financial_instrument_list.append(type_of_financial_instrument_dict)
        return type_of_financial_instrument_list

    def _validate_type_of_financial_instrument(self, fin_ins_values):
        """returns list of validated values"""
        err_msg = ''
        type_of_financial_instrument_list = []
        for each_val in fin_ins_values:
            type_of_financial_instrument_dict = {}
            type_of_instrument = each_val.get('TypeOfInstrument')
            if type_of_instrument:
                option = each_val.get('option')
                if option in ['A', 'C']:
                    if option == 'A':
                        val = self._validate_type_of_instrument_12A(type_of_instrument)
                    else:
                        val = self._validate_type_of_instrument_12C(type_of_instrument)
                    type_of_financial_instrument_dict['TypeOfInstrument'] = val
                    type_of_financial_instrument_dict['option'] = option
                    type_of_financial_instrument_list.append(type_of_financial_instrument_dict)
        return type_of_financial_instrument_list

    def _check_condition_set_type_of_financial_instrument(self):
        """return True or False depending on the condition provided"""
        return False

    def _set_type_of_financial_instrument(self, fin_ins_values):
        """calls actual setter APIs depending on the provided input"""
        for each_val in fin_ins_values:
            type_of_instrument = each_val.get('TypeOfInstrument')
            if type_of_instrument:
                option = each_val.get('option')
                if option in ['A', 'C']:
                    if option == 'A':
                        self._settype_of_instrument_12A(type_of_instrument)
                    else:
                        self._settype_of_instrument_12C(type_of_instrument)

    def type_of_instrument_12A(self, instrument_type_dict):
        """Returns a dictionary with values of Qualifier and ISITC Code"""
        type_of_financial_instrument_dict = {}
        instrument_type_code = instrument_type_dict['INSTRUMENT_TYPE_ISITC_CODE']
        qualifier = instrument_type_dict['INSTRUMENT_TYPE_QUALIFIER']
        type_of_financial_instrument_dict['instrument_type_code'] = instrument_type_code
        type_of_financial_instrument_dict['qualifier'] = qualifier
        type_of_financial_instrument_dict['option'] = 'A'
        return type_of_financial_instrument_dict

    def _format_type_of_instrument_12A(self, fin_ins_values):
        """returns formatted values of provided input"""
        instrument_type_code = fin_ins_values.get('instrument_type_code')
        qualifier = fin_ins_values.get('qualifier')
        type_of_instrument = ":" + str(qualifier) + '/ISIT/' + str(instrument_type_code)
        return type_of_instrument

    def _settype_of_instrument_12A(self, fin_ins_values):
        """sets the provided tag and value in python object"""
        self.swift_obj.SequenceB_TradeDetails.SubSequenceB1_FinancialInstrumentAttributes.TypeOfFinancialInstrument_A.append(fin_ins_values)
        self.swift_obj.SequenceB_TradeDetails.SubSequenceB1_FinancialInstrumentAttributes.TypeOfFinancialInstrument_A[-1].swiftTag = "12A"

    def type_of_instrument_12C(self, instrument_type_dict):
        """Returns a dictionary with values of Qualifier and CFI Code"""
        type_of_instrument_dict = {}
        instrument_type_code = instrument_type_dict['INSTRUMENT_TYPE_CFI_CODE']
        qualifier = instrument_type_dict['INSTRUMENT_TYPE_QUALIFIER']
        type_of_instrument_dict['instrument_type_code'] = instrument_type_code
        type_of_instrument_dict['qualifier'] = qualifier
        type_of_instrument_dict['option'] = 'C'
        return type_of_instrument_dict

    def _format_type_of_instrument_12C(self, fin_ins_values):
        """returns formatted values of provided input"""
        instrument_type_code = fin_ins_values.get('instrument_type_code')
        qualifier = fin_ins_values.get('qualifier')
        type_of_instrument = ":" + str(qualifier) + '//' + str(instrument_type_code)
        return type_of_instrument

    def _settype_of_instrument_12C(self, fin_ins_values):
        """sets the provided tag and value in python object"""
        self.swift_obj.SequenceB_TradeDetails.SubSequenceB1_FinancialInstrumentAttributes.TypeOfFinancialInstrument_C.append(fin_ins_values)
        self.swift_obj.SequenceB_TradeDetails.SubSequenceB1_FinancialInstrumentAttributes.TypeOfFinancialInstrument_C[-1].swiftTag = "12C"

