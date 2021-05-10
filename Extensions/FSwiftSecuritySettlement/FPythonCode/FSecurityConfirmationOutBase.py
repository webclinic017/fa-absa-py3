"""----------------------------------------------------------------------------
MODULE:
    FSecurityConfirmationOutBase

DESCRIPTION:
    This module provides the base class for the security settlement outgoing implementation.
    It contains the common mwthods across security settlement outgoing solution.

CLASS:
    FSecurityConfirmationOutBase

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
from FMTOutBase import FMTOutBase
import FSwiftWriterUtils
import FSecuritySettlementOutUtils
import FSecurityConfirmationOutUtils
import FSwiftWriterLogger
import FSwiftMLUtils
import acm

notifier = FSwiftWriterLogger.FSwiftWriterLogger('SecSetOut', 'FSecuritySettlementOutNotify_Config')


class FSecurityConfirmationOutBase(FMTOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FSecurityConfirmationOutBase, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # ------------------ quantity of instrument-36B-----------------------
    def quantity_of_instrument_36B(self):
        '''
        Returns a list of dictionaries as [{k1:v1,k2:v2},{k1:v3,k2:v4}]
        '''
        quantity = {}
        quantity_blocks = []
        quantity['QUANTITY_TYPE_CODE'] = FSecurityConfirmationOutUtils.get_quantity_type_code()
        quantity['QUANTITY_QUANTITY'] = FSecurityConfirmationOutUtils.get_nominal(self.acm_obj)
        quantity_blocks.append(quantity)
        return quantity_blocks

    def _format_quantity_of_instrument_36B(self, val):
        quantity_of_instrument = []
        for each_block in val:
            quantity_of_instrument.append(":CONF//" + str(each_block['QUANTITY_TYPE_CODE']) + "/" + str(
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

        val_dict = {}
        each_block = {}
        each_block['SETTLEMENT_DATETIME_OPTION'] = self.get_settlement_datetime_98_option()
        each_block[
            'SETTLEMENT_DATETIME_QUALIFIER'] = FSecurityConfirmationOutUtils.get_confirmation_datetime_qualifier()
        each_block['SETTLEMENT_DATETIME_DATE'] = FSecurityConfirmationOutUtils.get_confirmation_datetime_date(
            self.acm_obj)
        if each_block['SETTLEMENT_DATETIME_OPTION'] in ['A', 'B', 'C', 'E']:
            val_dict['DateTime_A'] = self.date_time_98A(each_block)
        else:
            notifier.ERROR("%s Option %s is not supported for tag %s. Mapping default option: A" %
                           (
                           self.swift_message_type, each_block['SETTLEMENT_DATETIME_OPTION'], 'SettlementDateTime_98a'))
        val_list.append(val_dict)

        val_dict = {}
        each_block = {}
        each_block['SETTLEMENT_DATETIME_OPTION'] = self.get_settlement_datetime_98_option()
        each_block['SETTLEMENT_DATETIME_QUALIFIER'] = FSecurityConfirmationOutUtils.get_trade_datetime_qualifier()
        each_block['SETTLEMENT_DATETIME_DATE'] = FSecurityConfirmationOutUtils.get_trade_datetime_date(self.acm_obj)
        if each_block['SETTLEMENT_DATETIME_OPTION'] in ['A', 'B', 'C']:
            val_dict['DateTime_A'] = self.date_time_98A(each_block)
        else:
            notifier.ERROR("%s Option %s is not supported for tag %s. Mapping default option: A" %
                           (
                               self.swift_message_type, each_block['SETTLEMENT_DATETIME_OPTION'],
                               'SettlementDateTime_98a'))

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

    # ------------------ function of message - 23G -----------------------
    def function_of_message_23G(self):
        '''
        Returns a string containing value of fuction_of_message
        '''
        return FSecurityConfirmationOutUtils.get_function_of_message(self.acm_obj)

    def _format_function_of_message_23G(self, val):
        return val

    # ------------------ acquirer party-----------------------
    def get_acquirer_party_option(self):
        """Returns option override if implemented
        :return: str; option choice as string
        """
        return 'P'

    def _format_acquirer_party(self, party_dic):
        format_dict = {}
        if 'PARTY_P' in party_dic:
            format_dict['PARTY_P'] = self._format_settlement_party_95P(party_dic['PARTY_P'])
        if 'PARTY_L' in party_dic:
            format_dict['PARTY_L'] = self._format_settlement_party_95L(party_dic['PARTY_L'])
        if 'PARTY_Q' in party_dic:
            format_dict['PARTY_Q'] = self._format_settlement_party_95Q(party_dic['PARTY_Q'])
        return format_dict

    def _validate_acquirer_party(self, party_dict):
        valid_dict = {}
        if 'PARTY_P' in party_dict:
            val = self._validate_party_95P(party_dict['PARTY_P'])
            if val:
                valid_dict['PARTY_P'] = val
        if 'PARTY_L' in party_dict:
            val = self._validate_party_95L(party_dict['PARTY_L'])
            if val:
                valid_dict['PARTY_L'] = val
        if 'PARTY_Q' in party_dict:
            val = self._validate_party_95Q(party_dict['PARTY_Q'])
            if val:
                valid_dict['PARTY_Q'] = val
        return valid_dict

    # ------------------ counter party -----------------------
    def get_counter_party_option(self):
        """Returns option override if implemented
        :return: str; option choice as string
        """
        return 'P'

    def _format_counter_party(self, party_dic):
        format_dict = {}
        if 'PARTY_P' in party_dic:
            format_dict['PARTY_P'] = self._format_settlement_party_95P(party_dic['PARTY_P'])
        if 'PARTY_L' in party_dic:
            format_dict['PARTY_L'] = self._format_settlement_party_95L(party_dic['PARTY_L'])
        if 'PARTY_Q' in party_dic:
            format_dict['PARTY_Q'] = self._format_settlement_party_95Q(party_dic['PARTY_Q'])
        return format_dict

    def _validate_counter_party(self, party_dict):
        valid_dict = {}
        if 'PARTY_P' in party_dict:
            val = self._validate_party_95P(party_dict['PARTY_P'])
            if val:
                valid_dict['PARTY_P'] = val
        if 'PARTY_L' in party_dict:
            val = self._validate_party_95L(party_dict['PARTY_L'])
            if val:
                valid_dict['PARTY_L'] = val
        if 'PARTY_Q' in party_dict:
            val = self._validate_party_95Q(party_dict['PARTY_Q'])
            if val:
                valid_dict['PARTY_Q'] = val
        return valid_dict

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

    # ------------------ settlement parties 95L -----------------------
    def settlement_party_95L(self, party_dict):
        '''
        Returns a dictionary as {k1:v1,k2:v2}
        '''
        values_dict = {}
        qualifier = party_dict['PARTY_QUALIFIER']
        party_LEI = party_dict['PARTY_LEI']
        values_dict['qualifier'] = qualifier
        values_dict['LEI'] = party_LEI
        return values_dict

    def _format_settlement_party_95L(self, val):
        qualifier = val.get('qualifier')
        party_LEI = val.get('LEI')
        if party_LEI:
            settlement_party_Q = ":" + str(qualifier) + "//" + party_LEI
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

    # ------------------ indicator-22H -----------------------
    def get_indicator_22_option(self):
        """Returns default option if override is not provided
        :return: str; option choice as string
        """
        return 'H'

    def indicator_22H(self):
        '''
        Returns a list of dictionaries as [{k1:v1,k2:v2},{k1:v3,k2:v4}]
        '''

        indicator_blocks = []
        indicators = FSecurityConfirmationOutUtils.get_indicators(self.acm_obj)
        for indicator_pair in indicators:
            indicator_block = {}
            indicator_block['INDICATOR_QUALIFIER_OPTION'] = self.get_indicator_22_option()
            indicator_block['INDICATOR_QUALIFIER'] = FSecurityConfirmationOutUtils.get_qualifier(indicator_pair)
            indicator_block['INDICATOR_INDICATOR'] = FSecurityConfirmationOutUtils.get_indicator(indicator_pair)
            indicator_blocks.append(indicator_block)
        return indicator_blocks

    def _format_indicator_22H(self, val):
        indicator_values = []
        for each_block in val:
            if each_block["INDICATOR_INDICATOR"]:
                indicator_values.append(
                    ":" + str(each_block['INDICATOR_QUALIFIER']) + "//" + str(each_block["INDICATOR_INDICATOR"]))
            else:
                indicator_values = "Can not populate delivery type as settlement event is missing on the trade"

        return indicator_values

    def _validate_indicator_22H(self, val_list):
        err_msgs = []
        values = []
        for each_val in val_list:
            val = self._validate_indicator_22H_items(each_val)
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
            values_dict['isin'] = FSecurityConfirmationOutUtils.get_instrument_ISIN(self.acm_obj)
            values_dict['description_of_security'] = FSecurityConfirmationOutUtils.get_description_of_security(
                self.acm_obj)

        if not values_dict['isin'] and not values_dict['description_of_security']:
            raise Exception("Can not map 35B as ISIN and description not present on Instrument")
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
        function_of_message = FSecurityConfirmationOutUtils.get_function_of_message(self.acm_obj)
        linkage_qualifier = FSecurityConfirmationOutUtils.get_linkage_qualifier(self.acm_obj)
        linkage_reference = FSecurityConfirmationOutUtils.get_linkage_reference(self.acm_obj)
        values_dict['function_of_message'] = function_of_message
        values_dict['linkage_qualifier'] = linkage_qualifier
        values_dict['linkage_reference'] = linkage_reference
        values_dict['senders_reference'] = self.acm_obj.Oid()
        values_dict['seq_ref'] = FSecurityConfirmationOutUtils.get_confirmation_reference_prefix()
        return values_dict

    def _check_condition_set_linkages_20C_16R(self):
        if self.use_operations_xml:
            function_of_message = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'FUNCTION_OF_MESSAGE'])
        else:
            function_of_message = FSecurityConfirmationOutUtils.get_function_of_message(self.acm_obj)
        if function_of_message == "CANC":
            return True
        return False

    # ------------------- senders reference - 20C-------------------

    def senders_message_reference_20C(self):
        '''
        Returns a dictionary as {'senders_reference':value1, 'seq_ref':value2}
        '''
        values_dict = {}
        values_dict['senders_reference'] = self.acm_obj.Oid()
        values_dict['seq_ref'] = FSecurityConfirmationOutUtils.get_confirmation_reference_prefix()
        return values_dict

    def _format_senders_message_reference_20C(self, val):
        senders_reference = val.get('senders_reference')
        seq_ref = val.get('seq_ref')
        con_obj = acm.FConfirmation[str(senders_reference)]
        if senders_reference:
            val = ":SEME//%s-%s-%s" % (
                str(seq_ref), str(senders_reference),
                str(FSecurityConfirmationOutUtils.get_message_version_number(con_obj)))
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
        return FSecurityConfirmationOutUtils.get_amount_details(self.acm_obj, self.swift_message_type)

    def flag_17B(self):
        """get the settlement amount flag"""
        return FSecurityConfirmationOutUtils.get_amount_flags(self.acm_obj, self.swift_message_type)

    def _format_amounts_19A(self, val):
        amount_fields = list()
        for each_block in val:
            amount_field = ":" + str(each_block['AMOUNT_QUALIFIER']) + "//" + str(each_block["AMOUNT_CURRENCY_CODE"]) \
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

    # --------------------------------Deal Price-----------------------------------------------
    def get_deal_price_90_option(self):
        return 'A'

    def deal_price(self):
        """ Returns a dictionary as [{'DEAL_PRICE_A': [list_of _dict_of amounts], 'DEAL_PRICE_B': [list_of_dict_of_flags]}]
        """
        deal_price_block_details = dict()
        deal_price_option = self.get_deal_price_90_option()
        if deal_price_option not in ['A', 'B']:
            notifier.ERROR(
                "Deal Price Option {0} is not supported. Mapping default option: A".format(deal_price_option))
            deal_price_option = 'A'

        if deal_price_option == 'A':
            deal_price_block_details['DEAL_PRICE_A'] = self.deal_price_90A()

        elif deal_price_option == 'B':
            deal_price_block_details['DEAL_PRICE_B'] = self.deal_price_90B()
        return deal_price_block_details

    def _format_deal_price(self, val_dict):
        """Format amounts block"""
        amounts_block = dict()
        if 'DEAL_PRICE_A' in val_dict:
            amounts_block['DEAL_PRICE_A'] = self._format_deal_price_90A(val_dict.get('DEAL_PRICE_A'))
        elif 'DEAL_PRICE_B' in val_dict:
            amounts_block['DEAL_PRICE_B'] = self._format_deal_price_90B(val_dict.get('DEAL_PRICE_B'))
        return amounts_block

    def _validate_deal_price(self, val_dict):
        """ Validate amount block fields"""
        valid_dict = dict()
        if 'DEAL_PRICE_A' in val_dict:
            valid_dict['DEAL_PRICE_A'] = self._validate_deal_price_90A(val_dict.get('DEAL_PRICE_A'))
        elif 'DEAL_PRICE_B' in val_dict:
            valid_dict['DEAL_PRICE_B'] = self._validate_deal_price_90B(val_dict.get('DEAL_PRICE_B'))
        return valid_dict

    def deal_price_90A(self):
        """get the settlement amount flag"""
        price_details = FSecurityConfirmationOutUtils.get_deal_price_details(self.acm_obj, 'A')
        return price_details

    def _format_deal_price_90A(self, val):
        """Format amounts block"""
        deal_price = ''
        qualifer = val.get('qualifer')
        price = val.get('deal_price')
        if price == None:
            deal_price = "Can not populate price as quotation is not supported in swift"
        else:
            deal_price = ':DEAL//{0}/{1}'.format(qualifer, price)
        return deal_price

    def deal_price_90B(self):
        """get the settlement amount flag"""
        # flag_blocks = ":DEAL//ACTU/EUR101,20"     #FSecurityConfirmationOutUtils.get_deal_price(self.acm_obj)
        price_details = FSecurityConfirmationOutUtils.get_deal_price_details(self.acm_obj, 'B')
        return price_details

    def _format_deal_price_90B(self, val):
        """Format amounts block"""
        deal_price = ''
        qualifer = val.get('qualifer')
        price = val.get('deal_price')
        curr = val.get('currency')
        if qualifer and price:
            deal_price = ':DEAL//{0}/{1}{2}'.format(qualifer, curr, price)
        return deal_price


