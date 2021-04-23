"""----------------------------------------------------------------------------
MODULE:
    FMT518OutBase

DESCRIPTION:
    This module provides the base class for the FMT518 outgoing implementation

CLASS:
    FMT518Base

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSecuritySettlementOutUtils
import FSecurityConfirmationOutUtils
import FSwiftWriterMessageHeader
import FSwiftWriterMTFactory
import MT518
import acm
from FSecurityConfirmationOutBase import FSecurityConfirmationOutBase
from FSwiftWriterEngine import validate_with, should_use_operations_xml

import FSwiftWriterLogger
import FSwiftWriterUtils

notifier = FSwiftWriterLogger.FSwiftWriterLogger('SecSetOut', 'FSecuritySettlementOutNotify_Config')


class FMT518Base(FSecurityConfirmationOutBase):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = "MT518"
        super(FMT518Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    def handle_cancellation_message(self, swift_message, msg_typ, acm_object):
        """creates a python object from parent confirmations swift message.
            Assign that python object to fmt object.
            Set changed values only on fmt object.
        """
        try:
            canc_message = ''
            self.swift_obj = None
            pyobj = FSwiftWriterUtils.create_pyobj_from_swift_msg(swift_message)
            if pyobj:
                self.swift_obj = pyobj

                #setting related reference value (Tag 20C) on the fmt object
                trans_val = pyobj.SequenceA_GeneralInformation.SendersMessageReference.value()
                trans_val = trans_val.replace(trans_val[:5], ':PREV')
                formatter_value = self._format_linkages_20C_16R(trans_val)
                validated_value = self._validate_linkages_20C_16R(formatter_value)
                self._set_linkages_20C_16R(validated_value)

                #Setting sender reference for cancellation message
                getter_value = self.senders_message_reference_20C()
                formatter_value = self._format_senders_message_reference_20C(getter_value)
                validated_value = self._validate_senders_message_reference_20C(formatter_value)
                self._set_senders_message_reference_20C(validated_value)

                #Setting function of the message 23G to CANC
                func_of_msg = pyobj.SequenceA_GeneralInformation.FunctionOfTheMessage.value()
                func_of_msg = func_of_msg.replace('NEWM', 'CANC')
                self.swift_obj.SequenceA_GeneralInformation.FunctionOfTheMessage = func_of_msg
                self.swift_obj.SequenceA_GeneralInformation.FunctionOfTheMessage.swiftTag = "23G"

                mt_message = FSwiftWriterUtils.create_swift_msg_from_pyobj(self.swift_obj)
                fmt_swift_header_class_obj = FSwiftWriterMTFactory.FSwiftWriterMTFactory.create_fmt_header_object(self.swift_message_type, self.acm_obj, mt_message, None)
                canc_message = fmt_swift_header_class_obj.swift_message_with_header()

        except Exception as e:
            raise e
        return canc_message, self.swift_obj



    def _message_sequences(self):

        self.swift_obj.SequenceA_GeneralInformation = MT518.MT518_SequenceA_GeneralInformation()

        self.swift_obj.SequenceA_GeneralInformation.swiftTag = "16R"
        self.swift_obj.SequenceA_GeneralInformation.formatTag = "GENL"


        self.swift_obj.SequenceB_ConfirmationDetails = MT518.MT518_SequenceB_ConfirmationDetails()
        self.swift_obj.SequenceB_ConfirmationDetails.swiftTag = "16R"
        self.swift_obj.SequenceB_ConfirmationDetails.formatTag = "CONFDET"

        self.swift_obj.SequenceC_SettlementDetails = MT518.MT518_SequenceC_SettlementDetails()
        #self.subSequenceC3_Amounts = MT518.SubSequenceC3_Amounts()
        #self.swift_obj.SequenceC_SettlementDetails.SubSequenceC3_Amounts = self.subSequenceC3_Amounts
        self.swift_obj.SequenceC_SettlementDetails.swiftTag = "16R"
        self.swift_obj.SequenceC_SettlementDetails.formatTag = "SETDET"


    # getter
    # moved to FSecurityConfirmationOutBase

    # formatter
    # moved to FSecurityConfirmationOutBase

    # validator
    #@validate_with(MT540.MT540_SequenceA_GeneralInformation_20C_Type)
    def _validate_senders_message_reference_20C(self, val):
        return val

    # setter
    def _set_senders_message_reference_20C(self, val):
        self.swift_obj.SequenceA_GeneralInformation.SendersMessageReference = val
        self.swift_obj.SequenceA_GeneralInformation.SendersMessageReference.swiftTag = "20C"

    # ------------------ function of message - 23G -----------------------

    # getter
    # moved to FSecurityConfirmationOutBase

    # formatter
    # moved to FSecurityConfirmationOutBase

    # validator
    @validate_with(MT518.MT518_SequenceA_GeneralInformation_23G_Type)
    def _validate_function_of_message_23G(self, val):
        return val

    # setter
    def _set_function_of_message_23G(self, val):
        self.swift_obj.SequenceA_GeneralInformation.FunctionOfTheMessage = val
        self.swift_obj.SequenceA_GeneralInformation.FunctionOfTheMessage.swiftTag = "23G"


    # ------------------ Trade Transaction Type- 22F -----------------------
    # getter
    def transaction_type_22F(self):
        return FSecurityConfirmationOutUtils.get_transaction_type()

    # formatter
    def _format_transaction_type_22F(self, transaction_type):
        return ":TRTR//%s" % (transaction_type)

    # Validtor
    @validate_with(MT518.MT518_SequenceA_GeneralInformation_22F_Type)
    def _validate_transaction_type_22F(self, transaction_type):
        return transaction_type

    # setter
    def _set_transaction_type_22F(self, val):
        self.swift_obj.SequenceA_GeneralInformation.TradeTransactionType = val
        self.swift_obj.SequenceA_GeneralInformation.TradeTransactionType.swiftTag = "22F"

    # ------------------ Settlement Trade - 22F -----------------------
    # getter
    def settlement_indicator_22F(self):
        return FSecurityConfirmationOutUtils.get_transaction_type()

    # formatter
    def _format_settlement_indicator_22F(self, transaction_type):
        return ":SETR//%s" % (transaction_type)

    # Validtor
    @validate_with(MT518.MT518_SequenceC_SettlementDetails_22F_Type)
    def _validate_settlement_indicator_22F(self, transaction_type):
        return transaction_type

    # setter
    def _set_settlement_indicator_22F(self, val):
        self.swift_obj.SequenceC_SettlementDetails.Indicator.append(val)
        self.swift_obj.SequenceC_SettlementDetails.Indicator[-1].swiftTag = "22F"



    # getter
    # moved to FSecurityConfirmationOutBase

    # check condition
    # moved to FSecurityConfirmationOutBase

    # formatter
    def _format_linkages_20C_16R(self, val):
        return val

    # validator
    @validate_with(MT518.MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type)
    def _validate_linkages_20C_16R(self, val):
        return val

    # setter
    def _set_linkages_20C_16R(self, val):
        function_of_message = FSecurityConfirmationOutUtils.get_function_of_message(self.acm_obj)
        if function_of_message == 'CANC':
            linkage = MT518.MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages()
            linkage.Reference_C = val
            linkage.Reference_C.swiftTag = "20C"
            self.swift_obj.SequenceA_GeneralInformation.SubSequenceA1_Linkages.append(linkage)
            self.swift_obj.SequenceA_GeneralInformation.SubSequenceA1_Linkages[-1].swiftTag = "16R"
            self.swift_obj.SequenceA_GeneralInformation.SubSequenceA1_Linkages[-1].formatTag = "LINK"

    # ------------------ date time - 98A -----------------------
    # Block_getter
    # moved to FSecurityConfirmationOutBase

    # Block_formatter
    # moved to FSecurityConfirmationOutBase

    # Block_validator
    # moved to FSecurityConfirmationOutBase

    # Bock_setter
    def _set_date_time(self, val):
        for each_val in val:
            if 'DateTime_A' in each_val:
                self._setdate_time_98A(each_val['DateTime_A'])

    # getter
    # moved to FSecurityConfirmationOutBase

    # formatter
    # moved to FSecurityConfirmationOutBase

    # validator
    @validate_with(MT518.MT518_SequenceB_ConfirmationDetails_98A_Type)
    def _validate_date_time_98A(self, val):
        return val

    # setter
    def _setdate_time_98A(self, val):
        self.swift_obj.SequenceB_ConfirmationDetails.DateTime_A.append(val)
        self.swift_obj.SequenceB_ConfirmationDetails.DateTime_A[-1].swiftTag = "98A"


   # -------------------------------- Indicator - 22A----------------------------------


   # ------------------ identification of financial instruments -----------------------

    # getter
    # moved to FSecurityConfirmationOutBase

    # formatter
    # moved to FSecurityConfirmationOutBase

    # validator
    @validate_with(MT518.MT518_SequenceB_ConfirmationDetails_35B_Type)
    def _validate_identification_of_financial_ins_35B(self, val):
        return val

    # setter
    def _set_identification_of_financial_ins_35B(self, val):
        self.swift_obj.SequenceB_ConfirmationDetails.IdentificationOfTheFinancialInstrument = val
        self.swift_obj.SequenceB_ConfirmationDetails.IdentificationOfTheFinancialInstrument.swiftTag = "35B"

    # ------------------ quantity of instrument-36B-----------------------
    # getter
    # moved to FSecurityConfirmationOutBase

    # formatter
    # moved to FSecurityConfirmationOutBase

    # validator
    # moved to FSecurityConfirmationOutBase

    @validate_with(MT518.MT518_SequenceB_ConfirmationDetails_36B_Type)
    def _validate_quantity_of_instrument_36B_items(self, val):
        return val

    # setter
    def _set_quantity_of_instrument_36B(self, val):
        #for each_value in val:
        val = val[0]
        self.swift_obj.SequenceB_ConfirmationDetails.QuantityOfFinancialInstrument = val
        self.swift_obj.SequenceB_ConfirmationDetails.QuantityOfFinancialInstrument.swiftTag = "36B"

    # ------------------ indicator-22H -----------------------
    # getter
    # moved to FSecurityConfirmationOutBase

    # formatter
    # moved to FSecurityConfirmationOutBase

    # validator
    # moved to FSecurityConfirmationOutBase

    @validate_with(MT518.MT518_SequenceB_ConfirmationDetails_22H_Type)
    def _validate_indicator_22H_items(self, val):
        return val

    # setter
    def _set_indicator_22H(self, val):
        for each_value in val:
            self.swift_obj.SequenceB_ConfirmationDetails.Indicator_H.append(each_value)
            self.swift_obj.SequenceB_ConfirmationDetails.Indicator_H[-1].swiftTag = "22H"

    # ------------------ Acquirer parties ----------------------------------------------------
    def acquirer_party(self):
        '''
        Returns a list of dictionaries as [{'Party_Option':{k1:v1,k2:v2}},{'Party_Option':{k1:v3,k2:v4}}]
        '''
        val_list = []
        party_details_list = ['PARTY_OPTION', 'PARTY_QUALIFIER', 'PARTY_IDENTIFIER_CODE',
                                'PARTY_COUNTRY_CODE', 'PARTY_NAME', 'PARTY_ADDRESS', 'PARTY_LEI']
        party_option = self.get_acquirer_party_option()
        partyDetails = FSecurityConfirmationOutUtils.get_acquirer_party_details(self.acm_obj)
        val_dict = {}
        each_block = {}

        for item in party_details_list:
            if item not in ['PARTY_OPTION']:
                item_getter_cmd = 'FSecuritySettlementOutUtils.get_' + item.lower() + '(partyDetails)'
                each_block[item] = eval(item_getter_cmd)
        else:
            each_block['PARTY_OPTION'] = party_option

        if each_block and each_block['PARTY_OPTION'] not in ['P', 'Q', 'L']:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option: P" %
                          (self.swift_message_type, each_block['PARTY_OPTION'], 'Party_95a'))
            each_block['PARTY_OPTION'] = 'P'
        if each_block['PARTY_OPTION'] == 'P':
            val_dict['PARTY_P'] = self.settlement_party_95P(each_block)
        if each_block['PARTY_OPTION'] == 'Q':
            val_dict['PARTY_Q'] = self.settlement_party_95Q(each_block)
        if each_block['PARTY_OPTION'] == 'L':
            val_dict['PARTY_L'] = self.settlement_party_95L(each_block)
        return val_dict

    # validator
    @validate_with(MT518.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type)
    def _validate_party_95P(self, val):
        return val

    # validator
    @validate_with(MT518.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type)
    def _validate_party_95Q(self, val):
        return val

    # validator
    @validate_with(MT518.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type)
    def _validate_party_95L(self, val):
        return val

    # Block Setter
    def _set_acquirer_party(self, val):
        for each_val in val:
            setprty = MT518.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties()
            if each_val == 'PARTY_P':
                self._setsettlement_party_95P(val['PARTY_P'], setprty)
            if each_val == 'PARTY_L':
                self._setsettlement_party_95L(val['PARTY_L'], setprty)
            if each_val == 'PARTY_Q':
                self._setsettlement_party_95Q(val['PARTY_Q'], setprty)
            setprty.swiftTag = "16R"
            setprty.formatTag = "CONFPRTY"
            self.swift_obj.SequenceB_ConfirmationDetails.SubSequenceB1_ConfirmationParties.append(setprty)

    # ------------------ Acquirer parties ----------------------------------------------------
    def counter_party(self):
        '''
        Returns a list of dictionaries as [{'Party_Option':{k1:v1,k2:v2}},{'Party_Option':{k1:v3,k2:v4}}]
        '''
        """To override tags in SETPRTY block user needs to override set_settlement_parties by changing the specific part"""
        val_list = []
        party_details_list = ['PARTY_OPTION', 'PARTY_QUALIFIER', 'PARTY_IDENTIFIER_CODE',
                                'PARTY_COUNTRY_CODE', 'PARTY_NAME', 'PARTY_ADDRESS', 'PARTY_LEI']
        party_option = self.get_counter_party_option()
        partyDetails = FSecurityConfirmationOutUtils.get_counter_party_details(self.acm_obj)
        val_dict = {}
        each_block = {}

        for item in party_details_list:
            if item not in ['PARTY_OPTION']:
                item_getter_cmd = 'FSecuritySettlementOutUtils.get_' + item.lower() + '(partyDetails)'
                each_block[item] = eval(item_getter_cmd)
        else:
            each_block['PARTY_OPTION'] = party_option

        if each_block and each_block['PARTY_OPTION'] not in ['P', 'Q', 'L']:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option: P" %
                          (self.swift_message_type, each_block['PARTY_OPTION'], 'Party_95a'))
            each_block['PARTY_OPTION'] = 'P'

        if each_block['PARTY_OPTION'] == 'P':
            val_dict['PARTY_P'] = self.settlement_party_95P(each_block)
        if each_block['PARTY_OPTION'] == 'Q':
            val_dict['PARTY_Q'] = self.settlement_party_95Q(each_block)
        if each_block['PARTY_OPTION'] == 'L':
            val_dict['PARTY_R'] = self.settlement_party_95L(each_block)
        return val_dict

    # Block Setter
    def _set_counter_party(self, val):
        for each_val in val:
            setprty = MT518.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties()
            if each_val == 'PARTY_P':
                self._setsettlement_party_95P(val['PARTY_P'], setprty)
            if each_val == 'PARTY_L':
                self._setsettlement_party_95L(val['PARTY_L'], setprty)
            if each_val == 'PARTY_Q':
                self._setsettlement_party_95Q(val['PARTY_Q'], setprty)
            setprty.swiftTag = "16R"
            setprty.formatTag = "CONFPRTY"
            self.swift_obj.SequenceB_ConfirmationDetails.SubSequenceB1_ConfirmationParties.append(setprty)

    # ------------------ settlement parties ----------------------------------------------------
    def settlement_parties(self):
        '''
        Returns a list of dictionaries as [{'Party_Option':{k1:v1,k2:v2}},{'Party_Option':{k1:v3,k2:v4}}]
        '''
        """To override tags in SETPRTY block user needs to override set_settlement_parties by changing the specific part"""
        val_list = []
        party_details_list = ['PARTY_OPTION', 'PARTY_QUALIFIER', 'PARTY_IDENTIFIER_CODE',
                                                                 'PARTY_COUNTRY_CODE', 'PARTY_NAME', 'PARTY_ADDRESS', 'PARTY_LEI',
                                                                 'PARTY_DATA_SOURCE_SCHEME', 'PARTY_PROPRIETARY_CODE',
                                                                 'PARTY_SAFEKEEPING_OPTION', 'PARTY_SAFEKEEPING_ACCOUNT',
                                                                 'PARTY_SAFEKEEPING_QUALIFIER']
        party_option = self.get_party_95_option()
        party_safekeeping_option = self.get_party_safekeeping_97_option()
        multiplePartyDetails = FSecurityConfirmationOutUtils.get_acquirer_party_custodian_details(self.acm_obj, party_option)
        for partyDetails in multiplePartyDetails:
            val_dict = {}
            each_block = {}

            for item in party_details_list:
                if item not in ['PARTY_SAFEKEEPING_OPTION', 'PARTY_OPTION']:
                    item_getter_cmd = 'FSecuritySettlementOutUtils.get_' + item.lower() + '(partyDetails)'
                    each_block[item] = eval(item_getter_cmd)
                else:
                    if item == 'PARTY_SAFEKEEPING_OPTION':
                        each_block['PARTY_SAFEKEEPING_OPTION'] = party_safekeeping_option
                    else:
                        item_getter_cmd = 'FSecuritySettlementOutUtils.get_' + item.lower() + '(partyDetails, party_option)'
                        each_block['PARTY_OPTION'] = eval(item_getter_cmd)

            if each_block and each_block['PARTY_OPTION'] not in ['P', 'C', 'Q', 'R']:
                notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option: P" %
                              (self.swift_message_type, each_block['PARTY_OPTION'], 'Party_95a'))
                each_block['PARTY_OPTION'] = 'P'

            if each_block['PARTY_QUALIFIER'] in ['BUYR', 'SELL']: # SPR 405530 in Prime, Qualifier BUYR and SELL should always return option P
                    each_block['PARTY_OPTION'] = 'P'

            if each_block['PARTY_OPTION'] == 'R':
                val_dict['PARTY_R'] = self.settlement_party_95R(each_block)
            elif each_block['PARTY_OPTION'] == 'P':
                val_dict['PARTY_P'] = self.settlement_party_95P(each_block)
            elif each_block['PARTY_OPTION'] == 'C':
                val_dict['PARTY_C'] = self.settlement_party_95C(each_block)
            elif each_block['PARTY_OPTION'] == 'Q':
                val_dict['PARTY_Q'] = self.settlement_party_95Q(each_block)
            elif each_block['PARTY_OPTION'] == 'L':
                val_dict['PARTY_L'] = self.settlement_party_95L(each_block)

            if each_block['PARTY_QUALIFIER'] != "PSET" and each_block['PARTY_OPTION'] == 'P':
                if each_block and each_block['PARTY_SAFEKEEPING_OPTION'] not in ["A"]:
                    notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option: A" %
                                  (self.swift_message_type,
                                   each_block['PARTY_SAFEKEEPING_OPTION'], 'SafekeepingAccount_97a'))
                    each_block['PARTY_SAFEKEEPING_OPTION'] = "A"
                if each_block['PARTY_SAFEKEEPING_OPTION'] == "A" and each_block['PARTY_SAFEKEEPING_ACCOUNT'] and \
                        each_block['PARTY_SAFEKEEPING_QUALIFIER']:
                    val_dict['SafekeepingAccount_A'] = self.party_safekeeping_account_97A(each_block)
            val_list.append(val_dict)
        return val_list
    # Block Formatter
    # moved to FSecurityConfirmationOutBase

    # Block validator
    # moved to FSecurityConfirmationOutBase

    # Block Setter

    def _set_settlement_parties(self, val):
        #{'PARTY_P': {'code': 'OURODEFF', 'qualifier': 'BUYR'}}
        #for each_val in val:
        for each_val in val:
            setprty = MT518.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties()
            if 'PARTY_P' in each_val:
                self._setsettlement_party_95P(each_val['PARTY_P'], setprty)
            if 'PARTY_C' in each_val:
                self._setsettlement_party_95C(each_val['PARTY_C'], setprty)
            if 'PARTY_Q' in each_val:
                self._setsettlement_party_95Q(each_val['PARTY_Q'], setprty)
            if 'PARTY_R' in each_val:
                self._setsettlement_party_95R(each_val['PARTY_R'], setprty)
            if 'PARTY_L' in each_val:
                self._setsettlement_party_95L(each_val['PARTY_L'], setprty)
            if 'SafekeepingAccount_A' in each_val:
                self._setparty_safekeeping_account_97A(each_val['SafekeepingAccount_A'], setprty)

            setprty.swiftTag = "16R"
            setprty.formatTag = "SETPRTY"
            self.swift_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties.append(setprty)



    # getter
    # moved to FSecurityConfirmationOutBase

    # formatter
    # moved to FSecurityConfirmationOutBase

    # validator
    @validate_with(MT518.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type)
    def _validate_settlement_party_95P(self, val):
        return val

    # setter
    def _setsettlement_party_95P(self, val, setprty):
        setprty.PARTY_P.append(val)
        setprty.PARTY_P[-1].swiftTag = "95P"

    # getter
    # moved to FSecurityConfirmationOutBase

    # formatter
    # moved to FSecurityConfirmationOutBase

    # validator
    @validate_with(MT518.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type)
    def _validate_settlement_party_95R(self, val):
        return val

    # setter
    def _setsettlement_party_95R(self, val, setprty):
        setprty.PARTY_R.append(val)
        setprty.PARTY_R[-1].swiftTag = "95R"

    # getter
    # moved to FSecurityConfirmationOutBase

    # formatter
    # moved to FSecurityConfirmationOutBase

    # validator
    @validate_with(MT518.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type)
    def _validate_settlement_party_95C(self, val):
        return val

    # setter
    def _setsettlement_party_95C(self, val, setprty):
        setprty.PARTY_C.append(val)
        setprty.PARTY_C[-1].swiftTag = "95C"

    # getter
    # moved to FSecurityConfirmationOutBase

    # formatter
    # moved to FSecurityConfirmationOutBase

    # validator
    @validate_with(MT518.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type)
    def _validate_settlement_party_95Q(self, val):
        return val

    # setter
    def _setsettlement_party_95Q(self, val, setprty):
        setprty.PARTY_Q.append(val)
        setprty.PARTY_Q[-1].swiftTag = "95Q"

    # validator
    @validate_with(MT518.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type)
    def _validate_settlement_party_95L(self, val):
        return val

    # setter
    def _setsettlement_party_95L(self, val, setprty):
        setprty.PARTY_L.append(val)
        setprty.PARTY_L[-1].swiftTag = "95L"

    # getter
    # moved to FSecurityConfirmationOutBase

    # formatter
    # moved to FSecurityConfirmationOutBase

    # validator
    @validate_with(MT518.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type)
    def _validate_party_safekeeping_account_97A(self, val):
        return val

    # setter
    def _setparty_safekeeping_account_97A(self, val, setprty):
        setprty.SafekeepingAccount_A = val
        setprty.SafekeepingAccount_A.swiftTag = "97A"

    #------------------ amounts 19A- ------------------------------------------------------
    @validate_with(MT518.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type)
    def _validate_amounts_19A(self, val):
        return val

    # ------------------ amounts Flag 17B- ------------------------------------------------------
    @validate_with(MT518.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type)
    def _validate_flag_17B(self, val):
        return val

    # setter
    def _set_amounts(self, val_dict):
        """ Set value for the amount block"""
        for amount in val_dict.get('AMOUNT_BLOCKS'):
            amt = MT518.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts()
            if 'ACRU' in amount:
                for flag in val_dict.get('FLAG_BLOCKS'):
                    if 'ACRU' in flag:
                        amt.Flag.append(flag)
                        amt.Flag[-1].swiftTag = "17B"
            amt.Amount.append(amount)
            amt.Amount[-1].swiftTag = "19A"
            amt.swiftTag = "16R"
            amt.formatTag = "AMT"
            self.swift_obj.SequenceC_SettlementDetails.SubSequenceC3_Amounts.append(amt)

    # --------------------------------Deal Price -90-----------------------------------------------
    # setter
    def _set_deal_price(self, val_dict):
        """ Set value for the amount block"""
        if 'DEAL_PRICE_A' in val_dict:
            self._setdeal_price_90A(val_dict['DEAL_PRICE_A'])
        elif 'DEAL_PRICE_B' in val_dict:
            self._setdeal_price_90B(val_dict['DEAL_PRICE_B'])

    # --------------------------------Deal Price -90A-----------------------------------------------
    # getter
    # moved to FSecurityConfirmationOutBase

    # formatter
    # moved to FSecurityConfirmationOutBase

    @validate_with(MT518.MT518_SequenceB_ConfirmationDetails_90A_Type)
    def _validate_deal_price_90A(self, val):
        return val

    def _setdeal_price_90A(self, val):

        self.swift_obj.SequenceB_ConfirmationDetails.DealPrice_A = val
        self.swift_obj.SequenceB_ConfirmationDetails.DealPrice_A.swiftTag = "90A"

    # --------------------------------Deal Price -90B-----------------------------------------------
    # getter
    # moved to FSecurityConfirmationOutBase

    # formatter
    # moved to FSecurityConfirmationOutBase

    @validate_with(MT518.MT518_SequenceB_ConfirmationDetails_90B_Type)
    def _validate_deal_price_90B(self, val):
        return val

    def _setdeal_price_90B(self, val):
        self.swift_obj.SequenceB_ConfirmationDetails.DealPrice_B = val
        self.swift_obj.SequenceB_ConfirmationDetails.DealPrice_B.swiftTag = "90B"

class FMT518OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_typ = "518"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT'+ self.mt_typ)
        super(FMT518OutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

    def message_type(self):
        return "518"

    def sender_logical_terminal_address(self):
        '''LT code is hardcoded as A for sender'''
        terminal_address = ''
        senders_bic = ''
        if self.use_operations_xml:
            senders_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SENDER_BIC'])
        else:
            senders_bic = FSecurityConfirmationOutUtils.get_senders_bic(self.acm_obj)
        if not senders_bic:
            raise Exception("SENDER_BIC is a mandatory field for Swift message header")
        terminal_address = self.logical_terminal_address(senders_bic, "A")
        return terminal_address

    def receiver_logical_terminal_address(self):
        '''LT code is hardcoded as X for sender'''
        terminal_address = ''
        receivers_bic = ''
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'RECEIVER_BIC'])
        else:
            receivers_bic = FSecurityConfirmationOutUtils.get_receivers_bic(self.acm_obj)
        terminal_address = self.logical_terminal_address(receivers_bic, "X")
        return terminal_address

    def logical_terminal_address(self, bic_code, lt_code):
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
        return "I"

    def message_user_reference(self):
        '''MUR is sent in the format FAC-SEQNBR of settlement-VersionID'''
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seqref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            seqnbr = self.acm_obj.Oid()
            seqref = FSecurityConfirmationOutUtils.get_confirmation_reference_prefix()
        return "{108:%s-%s-%s}" % (seqref, seqnbr, FSecurityConfirmationOutUtils.get_message_version_number(self.acm_obj))


class FMT518OutBaseNetworkRules(object):
    def __init__(self, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom=None):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.acm_obj = acm_obj

    def network_rule_C1(self):
        """If an Exchange Rate (field :92B::EXCH) is present, the corresponding Resulting Amount (field :19A::RESU)
        must be present in the same subsequence. If the Exchange Rate is not present,
        the Resulting Amount is not allowed (Error code(s): E62)."""
        flag = False
        message = ''
        for amounts in self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC3_Amounts:
            if amounts.ExchangeRate and amounts.ExchangeRate.value():
                if amounts.Amount:
                    for amount_value in amounts.Amount:
                        if 'RESU' in amount_value.value():
                            flag = True
                            break
                    if not flag:
                        message = 'If an Exchange Rate (field :92B::EXCH) is present, the corresponding Resulting Amount (field :19A::RESU) must be present in the same subsequence'
            else:
                if amounts.Amount:
                    for amount_value in amounts.Amount:
                        if 'RESU' in amount_value.value():
                            flag = True
                    if flag:
                        message = 'If the Exchange Rate is not present, the Resulting Amount is not allowed (Error code(s): E62).'
        return message

    def network_rule_C2(self):
        """If the Settlement Amount (:19A::SETT) is present in sequence B, it must not be present in any occurrence of subsequence C3 (Error code(s): E73)."""
        if self.swift_message_obj.SequenceB_ConfirmationDetails.SettlementAmount:
            if self.swift_message_obj.SequenceB_ConfirmationDetails.SettlementAmount.value():
                for amounts in self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC3_Amounts:
                    if amounts.Amount:
                        for amount_value in amounts.Amount:
                            if amount_value.value():
                                return 'If the Settlement Amount (:19A::SETT) is present in sequence B, it must not be present in any occurrence of subsequence C3 (Error code(s): E73).'


    def network_rule_C3(self):
        """If the message is a cancellation, that is, Function of the Message (field 23G) is CANC,
        then subsequence A1 (Linkages) must be present at least once in the message,
        and in one and only one occurrence of A1, field :20C::PREV must be present;
        consequently, in all other occurrences of A1, field :20C::PREV is not allowed (Error code(s): E08 )."""
        message = ''
        if self.swift_message_obj.SequenceA_GeneralInformation.FunctionOfTheMessage.value() == 'CANC':
            linkages = self.swift_message_obj.SequenceA_GeneralInformation.SubSequenceA1_Linkages
            if not linkages:
                message = 'If the message is a cancellation, that is, Function of the Message (field 23G) is CANC, then subsequence A1 (Linkages) must be present at least once in the message'
            else:
                count = 0
                for link in linkages:
                    if link.Reference_C and link.Reference_C.value()[1:5] == 'PREV':
                        if count:
                            message = 'If the message is a cancellation, that is, Function of the Message (field 23G) is CANC, then in one and only one occurrence of A1, field :20C::PREV must be present; consequently, in all other occurrences of A1, field :20C::PREV is not allowed'
                        count = count + 1
                if count == 0:
                    message = 'If the message is a cancellation, that is, Function of the Message (field 23G) is CANC, then in one and only one occurrence of A1, field :20C::PREV must be present; consequently, in all other occurrences of A1, field :20C::PREV is not allowed'
        return message

    def network_rule_C4(self):
        """The following party fields for subsequences C1 and C2 cannot appear more than once in sequence C.
         The party fields for sequence D cannot appear more than once in a message (Error code(s): E84)."""
        message = ''
        if self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties:
            qualifier_list = ['BUYR', 'DEAG', 'DECU', 'DEI1', 'DEI2', 'PSET', 'REAG', 'RECU', 'REI1', 'REI2', 'SELL']
            dup_qualifier_c1 = FSecuritySettlementOutUtils.check_duplicate_qualifier(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties,
                                                                                 'PARTY', qualifier_list,
                                                                                 ['P', 'Q', 'R', 'S', 'C', 'L'])
            if dup_qualifier_c1:
                message = 'The party fields %s cannot appear more than once in subsequence C1' % str(dup_qualifier_c1)

        if self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC2_CashParties:
            qualifier_list = ['ACCW', 'BENM', 'PAYE', 'DEBT', 'INTM']
            dup_qualifier_c2 = FSecuritySettlementOutUtils.check_duplicate_qualifier(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC2_CashParties,
                                                                                 'PARTY', qualifier_list,
                                                                                 ['P', 'Q', 'R', 'S', 'L'])
            if dup_qualifier_c2:
                message = 'The party fields %s cannot appear more than once in subsequence C2' % str(dup_qualifier_c2)

        if self.swift_message_obj.SequenceD_OtherParties:
            qualifier_list = ['EXCH', 'MEOR', 'MERE', 'TRRE', 'VEND', 'TRAG']
            dup_qualifier_d = FSecuritySettlementOutUtils.check_duplicate_qualifier(self.swift_message_obj.SequenceD_OtherParties,
                                                                                 'PARTY', qualifier_list,
                                                                                 ['P', 'Q', 'R', 'S', 'L'])
            if dup_qualifier_d:
                message = 'The party fields %s cannot appear more than once in sequence SequenceF_OtherParties' % str(dup_qualifier_d)
        return message

    def network_rule_C5(self):
        """If a qualifier from the list Deliverers is present in a subsequence C1, in a field :95a::4!c,
         then all the remaining qualifiers following this qualifier in the list Deliverers (see below) must be present (Error code(s): E86)."""
        res = ''
        ret = self._validate_deliverer_qualifiers()
        if ret:
            res += ret
        ret = self._validate_receiverer_qualifiers()
        if ret:
            res += ret
        return res

    def _validate_deliverer_qualifiers(self):
        message = ''
        if self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties:
            dei2_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties,
                                                                          'PARTY', 'DEI2',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            dei1_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties,
                                                                          'PARTY', 'DEI1',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            decu_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties,
                                                                          'PARTY', 'DECU',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            sell_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties,
                                                                          'PARTY', 'SELL',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            deag_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties,
                                                                          'PARTY', 'DEAG',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])

            if dei2_flag:
                if not dei1_flag:
                    message = 'If :95a::DEI2 is present in subsequence C1, then :95a::DEI1 must be present in another subsequence C1.'
            if dei1_flag:
                if not decu_flag:
                    message = 'If :95a::DEI1 is present in subsequence C1, then :95a::DECU must be present in another subsequence C1.'
            if decu_flag:
                if not sell_flag:
                    message = 'If :95a::DECU is present in subsequence C1, then :95a::SELL must be present in another subsequence C1.'
            if sell_flag:
                if not deag_flag:
                    message = 'If :95a::SELL is present in subsequence C1, then :95a::DEAG must be present in another subsequence C1.'

        return message

    def _validate_receiverer_qualifiers(self):
        message = ''
        if self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties:
            rei2_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties,
                                                                          'PARTY', 'REI2',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            rei1_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties,
                                                                          'PARTY', 'REI1',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            recu_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties,
                                                                          'PARTY', 'RECU',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            buyr_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties,
                                                                          'PARTY', 'BUYR',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            reag_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties,
                                                                          'PARTY', 'REAG',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])

            if rei2_flag:
                if not rei1_flag:
                    message = 'If :95a::REI2 is present in subsequence C1, then :95a::REI1 must be present in another subsequence C1.'
            if rei1_flag:
                if not recu_flag:
                    message = "If :95a::REI1 is present in subsequence C1, then :95a::RECU must be present in another subsequence C1."
            if recu_flag:
                if not buyr_flag:
                    message = "If :95a::RECU is present in subsequence C1, then :95a::BUYR must be present in another subsequence C1."
            if buyr_flag:
                if not reag_flag:
                    message = "If :95a::BUYR is present in subsequence C1, then :95a::REAG must be present in another subsequence C1."

        return message

    def network_rule_C6(self):
        """In subsequence C1, if field :95a::PSET is present, then field :97a::SAFE is not allowed in the same subsequence. (Error code(s): E52)."""
        message = ''
        pset_flag = False
        safe_flag = False
        if self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties:
            pset_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties,
                                                                          'PARTY', 'PSET',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            if pset_flag:
                setprty_to_be_checked = None
                for each_setprty in self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties:
                    if setprty_to_be_checked:
                        break
                    for each_option in ['P', 'Q', 'R', 'S', 'C', 'L']:
                        qualifier_exists = FSecuritySettlementOutUtils._check_for_val(each_setprty, 'PARTY', each_option,
                                                                                     "PSET")
                        if qualifier_exists:
                            setprty_to_be_checked = each_setprty
                            break
                # Checking in same setprty as where PSET is present
                if setprty_to_be_checked.SafekeepingAccount_A and setprty_to_be_checked.SafekeepingAccount_A.value()[
                                                                  1:5] == 'SAFE':
                    safe_flag = True
                elif setprty_to_be_checked.SafekeepingAccount_B and setprty_to_be_checked.SafekeepingAccount_B.value()[
                                                                    1:5] == 'SAFE':
                    safe_flag = True

                if safe_flag:
                    message = 'In subsequence C1, if field :95a::PSET is present, then field :97a::SAFE is not allowed in the same subsequence'
        return message

    def network_rule_C7(self):
        """If field :22F::DBNM//VEND is present in sequence C, then a vendor must be specified; that is one occurrence of sequence D must contain field :95a::VEND (Error code(s): D71)."""
        message = ''
        if self.swift_message_obj.SequenceC_SettlementDetails:
            if self.swift_message_obj.SequenceC_SettlementDetails.Indicator:
                indicator_dbnm_flag = False
                indicator_dbnm_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_SettlementDetails,
                                                                                        'Indicator', 'DBNM//VEND', [])
                if indicator_dbnm_flag:
                    if not self.swift_message_obj.SequenceD_OtherParties:
                        message = 'If field :22F::DBNM//VEND is present in sequence C, then a vendor must be specified; that is one occurrence of sequence D must contain field :95a::VEND'
                    else:
                        party_vend_flag = False
                        party_vend_flag = FSecuritySettlementOutUtils.check_qualifier_exists(
                            self.swift_message_obj.SequenceD_OtherParties, 'PARTY', 'VEND', ['P', 'Q', 'R', 'S', 'C', 'L'])
                        if not party_vend_flag:
                            message = 'If field :22F::DBNM//VEND is present in sequence C, then a vendor must be specified; that is one occurrence of sequence D must contain field :95a::VEND'
        return message

    def network_rule_C8(self):
        """In sequence D, if field :95a::EXCH Stock Exchange or :95a::TRRE Trade Regulator is present, then field :97a:: is not allowed in the same sequence (Error code(s): E63)."""
        message = ''
        if self.swift_message_obj.SequenceD_OtherParties:
            flag_95a = False
            flag_95a_exch = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceD_OtherParties, 'PARTY',
                                                                              'EXCH', ['P', 'Q', 'R', 'S', 'C', 'L'])
            if not flag_95a_exch:
                flag_95a_trre = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceD_OtherParties,
                                                                                  'PARTY', 'TRRE',
                                                                                  ['P', 'Q', 'R', 'S', 'C', 'L'])
            flag_95a = flag_95a_exch or flag_95a_trre
            if flag_95a:
                # check for same occurance
                sequence_d_to_be_checked = None
                if flag_95a_exch:
                    for each_othrprty in self.swift_message_obj.SequenceD_OtherParties:
                        if sequence_d_to_be_checked:
                            break
                        for each_option in ['P', 'Q', 'R', 'S', 'C', 'L']:
                            qualifier_exists = FSecuritySettlementOutUtils._check_for_val(each_othrprty, 'PARTY',
                                                                                         each_option, "EXCH")
                            if qualifier_exists:
                                sequence_d_to_be_checked = each_othrprty
                                break
                if flag_95a_trre:
                    for each_othrprty in self.swift_message_obj.SequenceD_OtherParties:
                        if sequence_d_to_be_checked:
                            break
                        for each_option in ['P', 'Q', 'R', 'S', 'C', 'L']:
                            qualifier_exists = FSecuritySettlementOutUtils._check_for_val(each_othrprty, 'PARTY',
                                                                                         each_option, "TRRE")
                            if qualifier_exists:
                                sequence_d_to_be_checked = each_othrprty
                                break
                if sequence_d_to_be_checked.Account_A:
                    message = 'In sequence D, if field :95a::EXCH Stock Exchange or :95a::TRRE Trade Regulator is present, then field :97a:: is not allowed in the same sequence'
        return message

    def network_rule_C9(self):
        ret_msg = ''
        res1 = self._validate_c9_1()
        res2 = self._validate_c9_2()
        res3 = self._validate_c9_3()
        res4 = self._validate_c9_4()
        res5 = self._validate_c9_5()
        res6 = self._validate_c9_6()

        if res1:
            ret_msg = res1 + '\n'
        if res2:
            ret_msg = res2 + '\n'
        if res3:
            ret_msg = res3 + '\n'
        if res4:
            ret_msg = res4 + '\n'
        if res5:
            ret_msg = res5 + '\n'
        if res6:
            ret_msg = res6 + '\n'

        return ret_msg

    def _validate_c9_1(self):
        """In sequence B, field :94a::TRAD must not be present more than twice.
        When repeated, one and only one occurrence must be with format option L (:94L::TRAD) (Error code(s): E99)."""
        message = ''
        if self.swift_message_obj.SequenceB_ConfirmationDetails:
            count_trad = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceB_ConfirmationDetails, 'Place', 'TRAD',
                                                                    ['L', 'B'])
            if count_trad > 2:
                message = 'In sequence B, field :94a::TRAD must not be present more than twice.'
            if count_trad == 2:
                count_format_l = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceB_ConfirmationDetails, 'Place',
                                                                            'TRAD', ['L'])
                if count_format_l > 1:
                    message = 'In sequence B, only one occurrence must be with format option L (:94L::TRAD)'
        return message

    def _validate_c9_2(self):
        """In sequence B, field :94a::SAFE must not be present more than twice.
        When repeated, one and only one occurrence must be with format option L (:94L::SAFE) (Error code(s): E99)."""
        message = ''
        if self.swift_message_obj.SequenceB_ConfirmationDetails:
            count_safe = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceB_ConfirmationDetails, 'Place',
                                                                    'SAFE', ['B', 'C', 'F', 'L'])
            if count_safe > 2:
                message = 'In sequence B, field :94a::SAFE must not be present more than twice.'
            if count_safe == 2:
                count_format_l = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceB_ConfirmationDetails,
                                                                            'Place', 'SAFE', ['L'])
                if count_format_l > 1:
                    message = 'In sequence B, only one occurrence must be with format option L (:94L::SAFE)'
        return message

    def _validate_c9_3(self):
        """In each occurrence of subsequence B1, field :95a::ALTE must not be present more than twice.
        When repeated, one and only one occurrence must be with format option L (:95L::ALTE) (Error code(s): E99)."""
        message = ''
        if self.swift_message_obj.SequenceB_ConfirmationDetails.SubSequenceB1_ConfirmationParties:
            count_alte = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceB_ConfirmationDetails.SubSequenceB1_ConfirmationParties, 'PARTY',
                                                                    'ALTE', ['L', 'Q', 'P', 'R', 'S'])
            if count_alte > 2:
                message = 'In each occurrence of subsequence B1, field :95a::ALTE must not be present more than twice.'
            if count_alte == 2:
                count_format_l = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceB_ConfirmationDetails.SubSequenceB1_ConfirmationParties,
                                                                            'PARTY', 'ALTE', ['L'])
                if count_format_l > 1:
                    message = 'In each occurrence of subsequence B1, only one occurrence must be with format option L '
        return message

    def _validate_c9_4(self):
        """In each occurrence of subsequence C1, field :95a::ALTE must not be present more than twice.
        When repeated, one and only one occurrence must be with format option L (:95L::ALTE) (Error code(s): E99)."""
        message = ''
        if self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties:
            count_alte = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties, 'PARTY',
                                                                    'ALTE', ['L', 'Q', 'P', 'R', 'S'])
            if count_alte > 2:
                message = 'In each occurrence of subsequence C1, field :95a::ALTE must not be present more than twice.'
            if count_alte == 2:
                count_format_l = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC1_SettlementParties,
                                                                            'PARTY', 'ALTE', ['L'])
                if count_format_l > 1:
                    message = 'In each occurrence of subsequence C1, only one occurrence must be with format option L '
        return message

    def _validate_c9_5(self):
        """In each occurrence of subsequence C2, field :95a::ALTE must not be present more than twice.
        When repeated, one and only one occurrence must be with format option L (:95L::ALTE) (Error code(s): E99)."""
        message = ''
        if self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC2_CashParties:
            count_alte = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC2_CashParties, 'PARTY',
                                                                    'ALTE', ['L', 'Q', 'P', 'R', 'S'])
            if count_alte > 2:
                message = 'In each occurrence of subsequence C2, field :95a::ALTE must not be present more than twice.'
            if count_alte == 2:
                count_format_l = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceC_SettlementDetails.SubSequenceC2_CashParties,
                                                                            'PARTY', 'ALTE', ['L'])
                if count_format_l > 1:
                    message = 'In each occurrence of subsequence C2, only one occurrence must be with format option L '
        return message

    def _validate_c9_6(self):
        """In each occurrence of sequence D, field :95a::ALTE must not be present more than twice.
        When repeated, one and only one occurrence must be with format option L (:95L::ALTE) (Error code(s): E99)"""
        message = ''
        if self.swift_message_obj.SequenceD_OtherParties:
            count_alte = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceD_OtherParties, 'PARTY',
                                                                    'ALTE', ['L', 'Q', 'P', 'R', 'S'])
            if count_alte > 2:
                message = 'In each occurrence of sequence D, field :95a::ALTE must not be present more than twice.'
            if count_alte == 2:
                count_format_l = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceD_OtherParties,
                                                                            'PARTY', 'ALTE', ['L'])
                if count_format_l > 1:
                    message = 'In each occurrence of sequence D, only one occurrence must be with format option L '
        return message

    def network_rule_C10(self):
        """In each occurrence of sequence D, if field :95a::ALTE is present with format option L,
        then field :95a::MEOR and field :95a::MERE must not be present in the same occurrence of the sequence (Error code(s): E88)."""
        message = ''
        if self.swift_message_obj.SequenceD_OtherParties:
            alte_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceD_OtherParties, 'PARTY',
                                                                          'ALTE', ['L'])
            if alte_flag:
                # check in same occurance of seqeunce
                sequence_d_to_be_checked = None
                for each_othrprty in self.swift_message_obj.SequenceD_OtherParties:
                    qualifier_exists = FSecuritySettlementOutUtils._check_for_val(each_othrprty, 'PARTY', "L", "ALTE")
                    if qualifier_exists:
                        sequence_d_to_be_checked = each_othrprty
                        break
                if sequence_d_to_be_checked:
                    meor_flag = FSecuritySettlementOutUtils._check_for_val(sequence_d_to_be_checked, 'PARTY',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'], "MEOR")
                    mere_flag = FSecuritySettlementOutUtils._check_for_val(sequence_d_to_be_checked, 'PARTY',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'], "MERE")

                if meor_flag or mere_flag:
                    message = 'In each occurrence of sequence D, if field :95a::ALTE is present with format option L, then field :95a::MEOR and field :95a::MERE must not be present in the same occurrence of the sequence'
        return message

