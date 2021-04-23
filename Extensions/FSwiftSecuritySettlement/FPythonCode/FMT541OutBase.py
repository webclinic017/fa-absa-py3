"""----------------------------------------------------------------------------
MODULE:
    FMT541OutBase

DESCRIPTION:
    This module provides the base class for the FMT541 outgoing implementation

CLASS:
    FMT541Base

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftMLUtils
import FSecuritySettlementOutUtils
import FSwiftWriterMessageHeader
import MT541
import acm
from FSecuritySettlementOutBase import FSecuritySettlementOutBase
from FSwiftWriterEngine import validate_with, should_use_operations_xml

import FSwiftWriterLogger
import FSwiftWriterUtils

notifier = FSwiftWriterLogger.FSwiftWriterLogger('SecSetOut', 'FSecuritySettlementOutNotify_Config')


class FMT541Base(FSecuritySettlementOutBase):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = "MT541"
        self.cfi_code = None
        self.isitc_code = None
        self.security_settlement_out_config = FSwiftMLUtils.Parameters('FSecuritySettlementOut_Config')
        super(FMT541Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    def _message_sequences(self):
        self.swift_obj.SequenceA_GeneralInformation = MT541.MT541_SequenceA_GeneralInformation()
        self.swift_obj.SequenceA_GeneralInformation.swiftTag = "16R"
        self.swift_obj.SequenceA_GeneralInformation.formatTag = "GENL"
        self.swift_obj.SequenceB_TradeDetails = MT541.MT541_SequenceB_TradeDetails()
        self.swift_obj.SequenceB_TradeDetails.swiftTag = "16R"
        self.swift_obj.SequenceB_TradeDetails.formatTag = "TRADDET"
        self.swift_obj.SequenceC_FinancialInstrumentAccount = MT541.MT541_SequenceC_FinancialInstrumentAccount()
        self.swift_obj.SequenceC_FinancialInstrumentAccount.swiftTag = "16R"
        self.swift_obj.SequenceC_FinancialInstrumentAccount.formatTag = "FIAC"
        self.swift_obj.SequenceE_SettlementDetails = MT541.MT541_SequenceE_SettlementDetails()
        self.swift_obj.SequenceE_SettlementDetails.swiftTag = "16R"
        self.swift_obj.SequenceE_SettlementDetails.formatTag = "SETDET"

        #condition to check if the subsequence b1 should be enabled
        should_use_isitc = getattr(self.security_settlement_out_config, 'MT54xSendISITCAlways', 'None')
        if str(should_use_isitc).upper() == 'TRUE':
            self.isitc_code = FSecuritySettlementOutUtils.get_isitc_code(self.acm_obj)
            if not self.isitc_code:
                notifier.WARN('ISITC code could not be inferred; hence field 12A will not be mapped')
        elif str(should_use_isitc).upper() == 'FALSE':
            self.cfi_code = FSecuritySettlementOutUtils.get_cfi_code(self.acm_obj)
            if not self.cfi_code:
                self.isitc_code = FSecuritySettlementOutUtils.get_isitc_code(self.acm_obj)
                if not self.isitc_code:
                    notifier.INFO('CFI code not present on instrument and ISITC code could not be inferred; hence field 12C/12A will not be mapped')
        else:
            self.cfi_code = FSecuritySettlementOutUtils.get_cfi_code(self.acm_obj)
            if not self.cfi_code:
                notifier.DEBUG('CFI code not present on instrument; hence field 12C will not be mapped')

        if self.acm_obj.Instrument().IsKindOf(acm.FBond) or self.cfi_code or self.isitc_code:
            self.swift_obj.SequenceB_TradeDetails.SubSequenceB1_FinancialInstrumentAttributes = MT541.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes()
            self.swift_obj.SequenceB_TradeDetails.SubSequenceB1_FinancialInstrumentAttributes.swiftTag = "16R"
            self.swift_obj.SequenceB_TradeDetails.SubSequenceB1_FinancialInstrumentAttributes.formatTag = "FIA"

    # ------------------ senders_reference -----------------------

    #getter
    def senders_message_reference_20C(self):
        '''
        Returns senders_message_reference
        '''
        if self.use_operations_xml:
            senders_message_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SETTLEMENT', 'SEQNBR'])
        else:
            senders_message_reference = self.acm_obj.Oid()
        return senders_message_reference

    #formatter
    def _format_senders_message_reference_20C(self, val):
        if val:
            sett_obj = acm.FSettlement[str(val)]
            sett_ref = FSecuritySettlementOutUtils.get_settlement_reference_prefix()
            val = ":SEME//%s-%s-%s" % (sett_ref, str(val), str(FSecuritySettlementOutUtils.get_message_version_number(sett_obj)))
            return val

    #validator
    @validate_with(MT541.MT541_SequenceA_GeneralInformation_20C_Type)
    def _validate_senders_message_reference_20C(self, val):
        FSecuritySettlementOutUtils.validate_slash_and_double_slash(val[7:], "Senders Message Reference")
        return val

    #setter
    def _set_senders_message_reference_20C(self, val):
        self.swift_obj.SequenceA_GeneralInformation.SendersMessageReference = val
        self.swift_obj.SequenceA_GeneralInformation.SendersMessageReference.swiftTag = "20C"

    # ------------------ function of message -----------------------

    #getter
    # moved to FSecuritySettlementOutBase

    #formatter
    # moved to FSecuritySettlementOutBase


    #validator
    @validate_with(MT541.MT541_SequenceA_GeneralInformation_23G_Type)
    def _validate_function_of_message_23G(self, val):
        return val

    #setter
    def _set_function_of_message_23G(self, val):
        self.swift_obj.SequenceA_GeneralInformation.FunctionOfMessage = val
        self.swift_obj.SequenceA_GeneralInformation.FunctionOfMessage.swiftTag = "23G"

    # ------------------ linkage details   -----------------------

    # check condition
    # moved to FSecuritySettlementOutBase

    #getter
    # moved to FSecuritySettlementOutBase

    #formatter
    def _format_linkages_20C_16R(self, val):
        function_of_message = val.get('function_of_message')
        linkage_qualifier = val.get('linkage_qualifier')
        linkage_reference = val.get('linkage_reference')
        senders_reference = val.get('senders_reference')
        seq_ref = val.get('seq_ref')

        sett_obj = acm.FSettlement[str(senders_reference)]
        linkage = ''
        if function_of_message == "CANC" and linkage_qualifier and sett_obj and seq_ref:
            # Getting the reference of cancelled message
            related_ref = sett_obj.Children()[0]
            version_number_of_related_reference = FSecuritySettlementOutUtils.get_version_for_sent_message_on(
                related_ref, 'MT541')
            linkage = ":" + str(linkage_qualifier) + "//" + "%s-%s-%s" % (
                str(seq_ref), str(related_ref.Oid()), str(version_number_of_related_reference))
        return linkage

    #validator
    @validate_with(MT541.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type)
    def _validate_linkages_20C_16R(self, val):
        return val

    #setter
    def _set_linkages_20C_16R(self, val):
        linkage = MT541.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages()
        linkage.Reference_C = val
        linkage.Reference_C.swiftTag = "20C"
        self.swift_obj.SequenceA_GeneralInformation.SubSequenceA1_Linkages.append(linkage)
        self.swift_obj.SequenceA_GeneralInformation.SubSequenceA1_Linkages[-1].swiftTag = "16R"
        self.swift_obj.SequenceA_GeneralInformation.SubSequenceA1_Linkages[-1].formatTag = "LINK"

    # ------------------ date time - 98A -----------------------

    #Block_getter
    # moved to FSecuritySettlementOutBase

    # block formatter
    # moved to FSecuritySettlementOutBase

    #Block_validator
    # moved to FSecuritySettlementOutBase

    #Bock_setter
    def _set_date_time(self, val):
        for each_val in val:
            if 'DateTime_A' in each_val:
                self._setdate_time_98A(each_val['DateTime_A'])

    #getter
    # moved to FSecuritySettlementOutBase

    #formatter
    # moved to FSecuritySettlementOutBase


    #validator
    @validate_with(MT541.MT541_SequenceB_TradeDetails_98A_Type)
    def _validate_date_time_98A(self, val):
        return val

    #setter
    def _setdate_time_98A(self, val):
        self.swift_obj.SequenceB_TradeDetails.DateTime_A.append(val)
        self.swift_obj.SequenceB_TradeDetails.DateTime_A[-1].swiftTag = "98A"


    # ------------------ identification of financial instruments -----------------------


    #getter
    # moved to FSecuritySettlementOutBase

    #formatter
    # moved to FSecuritySettlementOutBase

    #validator
    @validate_with(MT541.MT541_SequenceB_TradeDetails_35B_Type)
    def _validate_identification_of_financial_ins_35B(self, val):
        return val

    #setter
    def _set_identification_of_financial_ins_35B(self, val):
        self.swift_obj.SequenceB_TradeDetails.IdentificationOfFinancialInstrument = val
        self.swift_obj.SequenceB_TradeDetails.IdentificationOfFinancialInstrument.swiftTag = "35B"



    # ------------------ type of financial instrument - 12C -----------------------

    #Block_getter
    #moved to FSecuritySettlementOutBase

    #block formatter
    #moved to FSecuritySettlementOutBase

    #Block_validator
    #moved to FSecuritySettlementOutBase

    #Check condition
    def _check_condition_set_type_of_financial_instrument(self):
        """return True or False depending on the condition provided"""
        should_set_type_of_fin_ins = False
        if self.cfi_code or self.isitc_code:
            should_set_type_of_fin_ins = True
        return should_set_type_of_fin_ins

    #Block_setter
    #moved to FSecuritySettlementOutBase

    #getter
    #moved to FSecuritySettlementOutBase

    #formatter
    #moved to FSecuritySettlementOutBase

    #validator
    @validate_with(MT541.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type)
    def _validate_type_of_instrument_12A(self, fin_ins_values):
        """returns validated value"""
        return fin_ins_values

    #setter
    #moved to FSecuritySettlementOutBase

    #getter
    #moved to FSecuritySettlementOutBase

    #formatter
    #moved to FSecuritySettlementOutBase

    #validator
    @validate_with(MT541.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type)
    def _validate_type_of_instrument_12C(self, fin_ins_values):
        """returns validated value"""
        return fin_ins_values

    #setter
    #moved to FSecuritySettlementOutBase

    # ------------------ SubSequence B1 date time - 98A -----------------------

    #Block_getter
    #moved to FSecuritySettlementOutBase

    # block formatter
    #moved to FSecuritySettlementOutBase

    #Block_validator
    #moved to FSecuritySettlementOutBase

    #_check_condition
    def _check_condition_set_subsequenceb1_date_time(self):
        """return True or False depending on the condition provided"""
        return self.acm_obj.Instrument().IsKindOf(acm.FBond)

    #Block_setter
    #moved to FSecuritySettlementOutBase

    #getter
    #moved to FSecuritySettlementOutBase

    #formatter
    #moved to FSecuritySettlementOutBase

    #validator
    @validate_with(MT541.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type)
    def _validate_subsequenceb1_date_time_98A(self, date_time_values):
        """returns validated value"""
        return date_time_values

    #setter
    #moved to FSecuritySettlementOutBase

    # ------------------ SubSequence B1 rate - 92A -----------------------

    #Block_getter
    #moved to FSecuritySettlementOutBase

    # block formatter
    #moved to FSecuritySettlementOutBase

    #Block_validator
    #moved to FSecuritySettlementOutBase

    #_check_condition
    def _check_condition_set_subsequenceb1_rate(self):
        """return True or False depending on the condition provided"""
        return self.acm_obj.Instrument().IsKindOf(acm.FBond)

    #Block_setter
    #moved to FSecuritySettlementOutBase

    #getter
    #moved to FSecuritySettlementOutBase

    #formatter
    #moved to FSecuritySettlementOutBase

    #validator
    @validate_with(MT541.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type)
    def _validate_subsequenceb1_rate_92A(self, rate_values):
        """returns validated value"""
        rate = rate_values
        FSecuritySettlementOutUtils.validateAmount(rate.replace('N', ''), 15, 'Rate')
        return rate_values

    #setter
    #moved to FSecuritySettlementOutBase


    # ------------------ quantity of instrument-36B-----------------------


    # block getter
    # moved to FSecuritySettlementOutBase

    # block formatter
    # moved to FSecuritySettlementOutBase

    # block validator
    # moved to FSecuritySettlementOutBase

    # validator
    @validate_with(MT541.MT541_SequenceC_FinancialInstrumentAccount_36B_Type)
    def _validate_quantity_of_instrument_36B_items(self, val):
        return val

    #setter
    def _set_quantity_of_instrument_36B(self, val):
        for each_value in val:
            self.swift_obj.SequenceC_FinancialInstrumentAccount.QuantityOfFinancialInstrumentToBeSettled.append(each_value)
            self.swift_obj.SequenceC_FinancialInstrumentAccount.QuantityOfFinancialInstrumentToBeSettled[-1].swiftTag = "36B"

    # ------------------ account -----------------------

    # block getter
    # moved to FSecuritySettlementOutBase

    # block formatter
    # moved to FSecuritySettlementOutBase

    # block validator
    # moved to FSecuritySettlementOutBase

    # block setter
    def _set_account(self, val):
        for each_val in val:
            if 'Account_A' in each_val:
                self._setaccount_97A(each_val['Account_A'])

    # getter
    # moved to FSecuritySettlementOutBase

    # formatter
    # moved to FSecuritySettlementOutBase

    # validate
    @validate_with(MT541.MT541_SequenceC_FinancialInstrumentAccount_97A_Type)
    def _validate_account_97A(self, val):
        return val

    #setter
    def _setaccount_97A(self, val):
        self.swift_obj.SequenceC_FinancialInstrumentAccount.Account_A.append(val)
        self.swift_obj.SequenceC_FinancialInstrumentAccount.Account_A[-1].swiftTag = "97A"


    # ------------------ place of safekeeping -----------------------

    #Block getter
    # moved to FSecuritySettlementOutBase

    #Block Formatter
    # moved to FSecuritySettlementOutBase

    #Block_validator
    # moved to FSecuritySettlementOutBase

    #Bock_setter
    def _set_place_of_safekeeping(self, val):
        for each_val in val:
            if 'PlaceOfSafekeeping_F' in each_val:
                self._setplace_of_safekeeping_94F(each_val['PlaceOfSafekeeping_F'])

    #getter
    # moved to FSecuritySettlementOutBase

    #formatter
    # moved to FSecuritySettlementOutBase

    #validator
    @validate_with(MT541.MT541_SequenceC_FinancialInstrumentAccount_94F_Type)
    def _validate_place_of_safekeeping_94F(self, val):
        return val

    #setter
    def _setplace_of_safekeeping_94F(self, val):
        self.swift_obj.SequenceC_FinancialInstrumentAccount.PlaceOfSafekeeping_F.append(val)
        self.swift_obj.SequenceC_FinancialInstrumentAccount.PlaceOfSafekeeping_F[-1].swiftTag = "94F"


    # ------------------ indicator -----------------------


    # block getter
    # moved to FSecuritySettlementOutBase

    # block formatter
    # moved to FSecuritySettlementOutBase


    # block validator
    # moved to FSecuritySettlementOutBase

    #validator
    @validate_with(MT541.MT541_SequenceE_SettlementDetails_22F_Type)
    def _validate_indicator_22F_items(self, val):
        return val

    #setter
    def _set_indicator_22F(self, val):
        for each_value in val:
            self.swift_obj.SequenceE_SettlementDetails.Indicator.append(each_value)
            self.swift_obj.SequenceE_SettlementDetails.Indicator[-1].swiftTag = "22F"


    # ------------------ settlement parties -----------------------

    def settlement_parties(self):
        '''
        Returns a list of dictionaries as [{'Party_Option':{k1:v1,k2:v2}},{'Party_Option':{k1:v3,k2:v4}}]
        '''
        """To override tags in SETPRTY block user needs to override set_settlement_parties by changing the specific part"""
        val_list = []
        party_details_list = ['PARTY_OPTION', 'PARTY_QUALIFIER', 'PARTY_IDENTIFIER_CODE',
                                                                 'PARTY_COUNTRY_CODE', 'PARTY_NAME', 'PARTY_ADDRESS',
                                                                 'PARTY_DATA_SOURCE_SCHEME', 'PARTY_PROPRIETARY_CODE',
                                                                 'PARTY_SAFEKEEPING_OPTION', 'PARTY_SAFEKEEPING_ACCOUNT',
                                                                 'PARTY_SAFEKEEPING_QUALIFIER']
        if self.use_operations_xml:
            party_blocks = FSwiftWriterUtils.get_block_xml_tags(self.swift_metadata_xml_dom, 'PARTY', party_details_list)
            for each_block in party_blocks:
                val_dict = {}

                qualifier = each_block[
                    'PARTY_QUALIFIER']  # SPR 405530 in Prime, Qualifier BUYR and SELL should always return option P
                if qualifier in ['BUYR', 'SELL']:
                    each_block['PARTY_OPTION'] = 'P'

                if each_block['PARTY_OPTION'] == 'P':
                    val_dict['PARTY_P'] = self.settlement_party_95P(each_block)
                if each_block['PARTY_OPTION'] == 'C':
                    val_dict['PARTY_C'] = self.settlement_party_95C(each_block)
                if each_block['PARTY_OPTION'] == 'Q':
                    val_dict['PARTY_Q'] = self.settlement_party_95Q(each_block)
                if each_block['PARTY_OPTION'] == 'R':
                    val_dict['PARTY_R'] = self.settlement_party_95R(each_block)
                if each_block['PARTY_QUALIFIER'] != "PSET" and each_block['PARTY_OPTION'] == 'P':
                    if each_block['PARTY_SAFEKEEPING_OPTION'] == "A" and each_block['PARTY_SAFEKEEPING_ACCOUNT'] and \
                            each_block['PARTY_SAFEKEEPING_QUALIFIER']:
                        val_dict['SafekeepingAccount_A'] = self.party_safekeeping_account_97A(each_block)
                val_list.append(val_dict)
        else:
            party_option = self.get_party_95_option()
            party_safekeeping_option = self.get_party_safekeeping_97_option()
            multiplePartyDetails = FSecuritySettlementOutUtils.get_party_details(self.acm_obj, party_option)
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
                if each_block['PARTY_OPTION'] == 'P':
                    val_dict['PARTY_P'] = self.settlement_party_95P(each_block)
                if each_block['PARTY_OPTION'] == 'C':
                    val_dict['PARTY_C'] = self.settlement_party_95C(each_block)
                if each_block['PARTY_OPTION'] == 'Q':
                    val_dict['PARTY_Q'] = self.settlement_party_95Q(each_block)
                if each_block['PARTY_OPTION'] == 'R':
                    val_dict['PARTY_R'] = self.settlement_party_95R(each_block)
                if each_block['PARTY_QUALIFIER'] != "PSET" and each_block['PARTY_OPTION'] == 'P':
                    if each_block and each_block['PARTY_SAFEKEEPING_OPTION'] not in ["A"]:
                        notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option: A" %
                                      (self.swift_message_type, each_block['PARTY_SAFEKEEPING_OPTION'], 'SafekeepingAccount_97a'))
                        each_block['PARTY_SAFEKEEPING_OPTION'] = "A"
                    if each_block['PARTY_SAFEKEEPING_OPTION'] == "A" and each_block['PARTY_SAFEKEEPING_ACCOUNT'] and \
                            each_block['PARTY_SAFEKEEPING_QUALIFIER']:
                        val_dict['SafekeepingAccount_A'] = self.party_safekeeping_account_97A(each_block)
                val_list.append(val_dict)
        return val_list

    #Block Formatter
    # moved to FSecuritySettlementOutBase

    #Block validator
    # moved to FSecuritySettlementOutBase

    # Block Setter
    def _set_settlement_parties(self, val):

        for each_val in val:
            setprty = MT541.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties()

            if 'PARTY_P' in each_val:
                self._setsettlement_party_95P(each_val['PARTY_P'], setprty)
            if 'PARTY_C' in each_val:
                self._setsettlement_party_95C(each_val['PARTY_C'], setprty)
            if 'PARTY_Q' in each_val:
                self._setsettlement_party_95Q(each_val['PARTY_Q'], setprty)
            if 'PARTY_R' in each_val:
                self._setsettlement_party_95R(each_val['PARTY_R'], setprty)
            if 'SafekeepingAccount_A' in each_val:
                self._setparty_safekeeping_account_97A(each_val['SafekeepingAccount_A'], setprty)

            setprty.swiftTag = "16R"
            setprty.formatTag = "SETPRTY"
            self.swift_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties.append(setprty)

        # --- 95P ----

    # getter
    # moved to FSecuritySettlementOutBase

    # formatter
    # moved to FSecuritySettlementOutBase

    # validator
    @validate_with(MT541.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type)
    def _validate_settlement_party_95P(self, val):
        return val

    # setter
    def _setsettlement_party_95P(self, val, setprty):
        setprty.PARTY_P.append(val)
        setprty.PARTY_P[-1].swiftTag = "95P"

        # --- 95R ----

    # getter
    # moved to FSecuritySettlementOutBase

    # formatter
    # moved to FSecuritySettlementOutBase

    # validator
    @validate_with(MT541.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type)
    def _validate_settlement_party_95R(self, val):
        return val

    # setter
    def _setsettlement_party_95R(self, val, setprty):
        setprty.PARTY_R.append(val)
        setprty.PARTY_R[-1].swiftTag = "95R"

        # --- 95C ----

    #getter
    # moved to FSecuritySettlementOutBase

    #formatter
    # moved to FSecuritySettlementOutBase

    #validator
    @validate_with(MT541.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type)
    def _validate_settlement_party_95C(self, val):
        return val

    #setter
    def _setsettlement_party_95C(self, val, setprty):
        setprty.PARTY_C.append(val)
        setprty.PARTY_C[-1].swiftTag = "95C"

        # --- 95Q ----

    #getter
    # moved to FSecuritySettlementOutBase

    #formatter
    # moved to FSecuritySettlementOutBase

    #validator
    @validate_with(MT541.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type)
    def _validate_settlement_party_95Q(self, val):
        return val

    #setter
    def _setsettlement_party_95Q(self, val, setprty):
        setprty.PARTY_Q.append(val)
        setprty.PARTY_Q[-1].swiftTag = "95Q"


        # --- 97A(safekeeping account) ----

    #getter
    # moved to FSecuritySettlementOutBase

    #formatter
    # moved to FSecuritySettlementOutBase

    #validator
    @validate_with(MT541.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type)
    def _validate_party_safekeeping_account_97A(self, val):
        return val

    #setter
    def _setparty_safekeeping_account_97A(self, val, setprty):
        setprty.SafekeepingAccount_A = val
        setprty.SafekeepingAccount_A.swiftTag = "97A"


    # ------------------ amount -----------------------

    # block getter validator and formatter moved to FSecuritySettlementOutBase

    # individual formatter
    # moved to FSecuritySettlementOutBase

    # individual validator
    # moved to FSecuritySettlementOutBase

    #validator
    @validate_with(MT541.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type)
    def _validate_amounts_19A(self, val):
        return val

    #setter
    def _set_amounts(self, val_dict):
        """Set values for the amount block"""
        for amount in val_dict.get('AMOUNT_BLOCKS'):
            amt = MT541.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts()
            if 'SETT' in amount:
                for flag in val_dict.get('FLAG_BLOCKS'):
                    amt.Flag.append(flag)
                    amt.Flag[-1].swiftTag = "17B"
            amt.Amount.append(amount)
            amt.Amount[-1].swiftTag = "19A"
            amt.swiftTag = "16R"
            amt.formatTag = "AMT"
            self.swift_obj.SequenceE_SettlementDetails.SubSequenceE3_Amounts.append(amt)

    # ------------------ flag -----------------------

    @validate_with(MT541.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type)
    def _validate_flag_17B(self):
        return val



class FMT541OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_typ = "541"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT'+ self.mt_typ)
        super(FMT541OutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

    def message_type(self):
        return "541"

    def sender_logical_terminal_address(self):
        '''LT code is hardcoded as A for sender'''
        terminal_address = ''
        senders_bic = ''
        if self.use_operations_xml:
            senders_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SENDER_BIC'])
        else:
            senders_bic = FSecuritySettlementOutUtils.get_senders_bic(self.acm_obj)
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
            receivers_bic = FSecuritySettlementOutUtils.get_receivers_bic(self.acm_obj)
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
        '''MUR is sent in the format FAC-SEQNBR of confirmation-VersionID'''
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SETTLEMENT', 'SEQNBR'])
            seqref = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SEQREF'])
        else:
            seqnbr = self.acm_obj.Oid()
            seqref = FSecuritySettlementOutUtils.get_settlement_reference_prefix()
        return "{108:%s-%s-%s}" % (seqref, seqnbr, FSecuritySettlementOutUtils.get_message_version_number(self.acm_obj))


class FMT541OutBaseNetworkRules(object):
    ''' '''

    def __init__(self, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom=None):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.acm_obj = acm_obj

    def network_rule_C1(self):
        """The following amount fields cannot appear in more than one occurrence of subsequence E3 Amounts"""

        amount_qualifiers = ['ACRU', 'ANTO', 'CHAR', 'COUN', 'DEAL', 'EXEC', 'ISDI', 'LADT', 'LEVY', 'LOCL', 'LOCO',
                             'MARG', 'OTHR', \
                             'REGF', 'SETT', 'SHIP', 'SPCN', 'STAM', 'STEX', 'TRAN', 'TRAX', 'VATA', 'WITH', 'COAX',
                             'ACCA']
        qualifier_repeated = []

        if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE3_Amounts:
            for amounts in self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE3_Amounts:
                for amount in amounts.Amount:
                    if amount.swiftTag == '19A' and amount.value() and amount.value()[1:5] in amount_qualifiers:
                        qualifier_repeated.append(amount.value()[1:5])
            if len(qualifier_repeated) != len(list(set(qualifier_repeated))):
                return 'The following amount fields cannot appear in more than one occurrence of subsequence E3 Amounts %s' % str(
                    qualifier_repeated)

        return ''

    def network_rule_C2(self):
        '''It is mandatory to specify a settlement amount: one occurrence of the subsequence E3 Amounts, must contain Amount field :19A::SETT'''
        flag = False
        if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE3_Amounts:
            for amounts in self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE3_Amounts:
                for amount in amounts.Amount:
                    if amount.swiftTag == '19A' and amount.value().startswith(':SETT'):
                        flag = True
                        break
        if not flag:
            return "It is mandatory to specify a settlement amount: one occurrence of the subsequence E3 Amounts, must contain Amount field :19A::SETT"
        else:
            return ''

    def network_rule_C3(self):
        '''In sequence A, if the Total of Linked Settlement Instructions (field :99B::TOSE) is present, then the Current Settlement Instruction Number
        (field :99B::SETT) must be present'''

        flag_tose = False
        flag_sett = False
        if self.swift_message_obj.SequenceA_GeneralInformation.NumberCount:
            for instr in self.swift_message_obj.SequenceA_GeneralInformation.NumberCount:
                if instr.swiftTag == '99B' and instr.value().startswith(':TOSE'):
                    flag_tose = True
                if instr.swiftTag == '99B' and instr.value().startswith(':SETT'):
                    flag_sett = True

            if flag_tose and not flag_sett:
                return 'In sequence A, if the Total of Linked Settlement Instructions (field :99B::TOSE) is present, then the Current Settlement Instruction Number (field :99B::SETT) must be present'
            else:
                return ''
        return ''

    def network_rule_C4(self):
        '''In subsequence E3, if an Exchange Rate (field :92B::EXCH) is present, the corresponding Resulting  Amount (field :19A::RESU)
            must be present in the same subsequence. If the exchange rate is not present then the Resulting Amount is not allowed'''
        res_amt_flag = False
        if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE3_Amounts:
            for amounts in self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE3_Amounts:
                if amounts.ExchangeRate:
                    for amount in amounts.Amount:
                        if amount.swiftTag == '19A' and amount.value().startswith(':RESU'):
                            res_amt_flag = True
                            break
                    if not res_amt_flag:
                        error_msg = "'In subsequence E3, if an Exchange Rate (field :92B::EXCH) is present, the corresponding Resulting  Amount (field :19A::RESU) must be present in the same subsequence"
                        return error_msg

                else:
                    for amount in amounts.Amount:
                        if amount.swiftTag == '19A' and amount.value().startswith(':RESU'):
                            res_amt_flag = True
                            break
                    if res_amt_flag:
                        error_msg = "In subsequence E3, If the exchange rate is not present then the Resulting Amount (field :19A::RESU) is not allowed"
                        return error_msg

        return ''

    def network_rule_C5(self):
        '''The following party fields cannot appear more than once in a message'''
        repeat_flag = False
        if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties:
            qualifier_list = ['BUYR', 'DEAG', 'DECU', 'DEI1', 'DEI2', 'PSET', 'REAG', 'RECU', 'REI1', 'REI2', 'SELL']
            dup_qualifier = FSecuritySettlementOutUtils.check_duplicate_qualifier(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties,
                                                                                 'PARTY', qualifier_list,
                                                                                 ['P', 'Q', 'R', 'S', 'C', 'L'])
            if dup_qualifier:
                return 'The party fields %s cannot appear more than once in sequence SETPRTY' % str(dup_qualifier)

        if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE2_CashParties:
            qualifier_list = ['ACCW', 'BENM', 'PAYE', 'DEBT', 'INTM']
            dup_qualifier = FSecuritySettlementOutUtils.check_duplicate_qualifier(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE2_CashParties,
                                                                                 'PARTY', qualifier_list,
                                                                                 ['P', 'Q', 'R', 'S', 'L'])
            if dup_qualifier:
                return 'The party fields %s cannot appear more than once in sequence SubSequenceE2_CashParties' % str(dup_qualifier)

        if self.swift_message_obj.SequenceF_OtherParties:
            qualifier_list = ['EXCH', 'MEOR', 'MERE', 'TRRE', 'VEND', 'TRAG', 'QFIN', 'BRKR']
            dup_qualifier = FSecuritySettlementOutUtils.check_duplicate_qualifier(self.swift_message_obj.SequenceE_SettlementDetails.SequenceF_OtherParties,
                                                                                 'PARTY', qualifier_list,
                                                                                 ['P', 'Q', 'R', 'S', 'L'])
            if dup_qualifier:
                return 'The party fields %s cannot appear more than once in sequence SequenceF_OtherParties' % str(dup_qualifier)
        return ''

    def network_rule_C6(self):
        '''If field :22F::DBNM is NOT present in sequence E, then it is mandatory to specify a receiving agent
        and a place of settlement: one occurrence of the Settlement Parties'''
        if self.swift_message_obj.SequenceE_SettlementDetails:
            if self.swift_message_obj.SequenceE_SettlementDetails.Indicator:
                indicator_dbnm_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails,
                                                                                        'Indicator', 'DBNM', [])

                if not indicator_dbnm_flag:
                    if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties:
                        deag_flag = FSecuritySettlementOutUtils.check_qualifier_exists(
                            self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties, 'PARTY', 'DEAG', ['P', 'Q', 'R', 'S', 'C', 'L'])
                        pset_flag = FSecuritySettlementOutUtils.check_qualifier_exists(
                            self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties, 'PARTY', 'PSET', ['P', 'Q', 'R', 'S', 'C', 'L'])

                        if not deag_flag or not pset_flag:
                            return 'If field :22F::DBNM is NOT present in sequence E, then it is mandatory to specify a delivery agent and a place of settlement: one occurrence of the Settlement Parties'

        return ''

    def network_rule_C7(self):
        '''If a qualifier from the list Deliverers is present in a subsequence E1, in a field :95a::4!c, then all the
        remaining qualifiers following this qualifier in the list Deliverers must be present'''
        res = ''
        ret = self._validate_deliverer_qualifiers()
        if ret:
            res += ret
        ret = self._validate_receiverer_qualifiers()
        if ret:
            res += ret
        return res

    def _validate_deliverer_qualifiers(self):
        if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties:
            dei2_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties,
                                                                          'PARTY', 'DEI2',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            dei1_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties,
                                                                          'PARTY', 'DEI1',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            decu_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties,
                                                                          'PARTY', 'DECU',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            sell_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties,
                                                                          'PARTY', 'SELL',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            if dei2_flag:
                if not dei1_flag:
                    return 'If :95a::DEI2 is present in subsequence E1, then :95a::DEI1 must be present in another subsequence E1.'
            if dei1_flag:
                if not decu_flag:
                    return 'If :95a::DEI1 is present in subsequence E1, then :95a::DECU must be present in another subsequence E1.'
            if decu_flag:
                if not sell_flag:
                    return 'If :95a::DECU is present in subsequence E1, then :95a::SELL must be present in another subsequence E1.'
        return ''

    def _validate_receiverer_qualifiers(self):
        if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties:
            rei2_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties,
                                                                          'PARTY', 'REI2',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            rei1_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties,
                                                                          'PARTY', 'REI1',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            recu_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties,
                                                                          'PARTY', 'RECU',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            buyr_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties,
                                                                          'PARTY', 'BUYR',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            if rei2_flag:
                if not rei1_flag:
                    return 'If :95a::REI2 is present in subsequence E1, then :95a::REI1 must be present in another subsequence E1.'
            if rei1_flag:
                if not recu_flag:
                    return "If :95a::REI1 is present in subsequence E1, then :95a::RECU must be present in another subsequence E1."
            if recu_flag:
                if not buyr_flag:
                    return "If :95a::RECU is present in subsequence E1, then :95a::BUYR must be present in another subsequence E1."
        return ''

    def network_rule_C8(self):
        '''If the message is a cancellation, that is, Function of the Message (field 23G) is CANC, then
        subsequence A1 (Linkages) must be present at least once in the message, and in one and only one
        occurrence of A1, field :20C::PREV must be present; consequently, in all other occurrences of A1, field
        :20C::PREV is not allowed (Error code(s): E08).'''
        if self.swift_message_obj.SequenceA_GeneralInformation.FunctionOfMessage.value() == 'CANC':
            linkages = self.swift_message_obj.SequenceA_GeneralInformation.SubSequenceA1_Linkages
            if not linkages:
                return 'If the message is a cancellation, that is, Function of the Message (field 23G) is CANC, then subsequence A1 (Linkages) must be present at least once in the message'
            else:
                count = 0
                for link in linkages:
                    if link.Reference_C and link.Reference_C.value()[1:5] == 'PREV':
                        if count:
                            return 'If the message is a cancellation, that is, Function of the Message (field 23G) is CANC, then in one and only one occurrence of A1, field :20C::PREV must be present; consequently, in all other occurrences of A1, field :20C::PREV is not allowed'
                        count = count + 1
                if count == 0:
                    return 'If the message is a cancellation, that is, Function of the Message (field 23G) is CANC, then in one and only one occurrence of A1, field :20C::PREV must be present; consequently, in all other occurrences of A1, field :20C::PREV is not allowed'

        return ''

    def network_rule_C9(self):
        """In subsequence E1, if field :95a::PSET is present, then field :97a::SAFE is not allowed in the same
        subsequence"""
        pset_flag = False
        safe_flag = False
        if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties:
            pset_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties,
                                                                          'PARTY', 'PSET',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'])
            if pset_flag:
                setprty_to_be_checked = None
                for each_setprty in self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties:
                    if setprty_to_be_checked:
                        break
                    for each_option in ['P', 'Q', 'R', 'S', 'C', 'L']:
                        qualifier_exists = FSecuritySettlementOutUtils._check_for_val(each_setprty, 'PARTY', each_option,
                                                                                     "PSET")
                        if qualifier_exists:
                            setprty_to_be_checked = each_setprty
                            break
                if setprty_to_be_checked.SafekeepingAccount_A and setprty_to_be_checked.SafekeepingAccount_A.value()[
                                                                  1:5] == 'SAFE':
                    safe_flag = True
                elif setprty_to_be_checked.SafekeepingAccount_B and setprty_to_be_checked.SafekeepingAccount_B.value()[
                                                                    1:5] == 'SAFE':
                    safe_flag = True

                if safe_flag:
                    return 'In subsequence E1, if field :95a::PSET is present, then field :97a::SAFE is not allowed in the same subsequence'
        return ''

    def network_rule_C10(self):
        """If field :22F::FXCX//FXNO or FXYE is present in sequence E, then the message must be a
        cancellation, that is, Function of the Message in sequence A (field 23G) is CANC.
        If field :22F::FXCX//SINO is present in sequence E, then the message must be new, that is, Function of
        the Message in sequence A (field 23G) is NEWM (Error code(s): E14)."""
        if self.swift_message_obj.SequenceE_SettlementDetails:
            if self.swift_message_obj.SequenceE_SettlementDetails.Indicator:
                indicator_fxcx_flag = False
                indicator_fxye_flag = False
                indicator_sino_flag = False
                indicator_fxcx_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails,
                                                                                        'Indicator', 'FXCX//FXNO', [])
                indicator_fxye_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails,
                                                                                        'Indicator', 'FXCX//FXYE', [])
                indicator_sino_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails,
                                                                                        'Indicator', 'FXCX//SINO', [])
                if indicator_fxcx_flag or indicator_fxye_flag:
                    if self.swift_message_obj.SequenceA_GeneralInformation.FunctionOfMessage.value() != 'CANC':
                        return 'If field :22F::FXCX//FXNO or FXYE is present in sequence E, then the message must be a cancellation, that is, Function of the Message in sequence A (field 23G) is CANC.'
                if indicator_sino_flag:
                    if self.swift_message_obj.SequenceA_GeneralInformation.FunctionOfMessage.value() != 'NEWM':
                        return 'If field :22F::FXCX//SINO is present in sequence E, then the message must be new, that is, Function of the Message in sequence A (field 23G) is NEWM'
        return ''

    def network_rule_C11(self):
        """If field :22F::DBNM is present in sequence E, then a buyer must be specified, that is one occurrence of
        subsequence E1 must contain field :95a::BUYR"""
        if self.swift_message_obj.SequenceE_SettlementDetails:
            if self.swift_message_obj.SequenceE_SettlementDetails.Indicator:
                indicator_dbnm_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails,
                                                                                        'Indicator', 'DBNM', [])
                if indicator_dbnm_flag:
                    if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties:
                        party_buyr_flag = False
                        party_buyr_flag = FSecuritySettlementOutUtils.check_qualifier_exists(
                            self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties, 'PARTY', 'BUYR', ['P', 'Q', 'R', 'S', 'C', 'L'])
                        if not party_buyr_flag:
                            return 'If field :22F::DBNM is present in sequence E, then a buyer must be specified, that is one occurrence of subsequence E1 must contain field :95a::BUYR'

        return ''

    def network_rule_C12(self):
        """If field :22F::DBNM//VEND is present in sequence E, then a vendor must be specified; that is one
        occurrence of sequence F must contain field :95a::VEND (Error code(s): D71)."""
        if self.swift_message_obj.SequenceE_SettlementDetails:
            if self.swift_message_obj.SequenceE_SettlementDetails.Indicator:
                indicator_dbnm_flag = False
                indicator_dbnm_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails,
                                                                                        'Indicator', 'DBNM//VEND', [])
                if indicator_dbnm_flag:
                    if not self.swift_message_obj.SequenceF_OtherParties:
                        return 'If field :22F::DBNM//VEND is present in sequence E, then a vendor must be specified; that is one occurrence of sequence F must contain field :95a::VEND'
                    else:
                        party_vend_flag = False
                        party_vend_flag = FSecuritySettlementOutUtils.check_qualifier_exists(
                            self.swift_message_obj.SequenceF_OtherParties, 'PARTY', 'VEND', ['P', 'Q', 'R', 'S', 'C', 'L'])
                        if not party_vend_flag:
                            return 'If field :22F::DBNM//VEND is present in sequence E, then a vendor must be specified; that is one occurrence of sequence F must contain field :95a::VEND'

        return ''

    def network_rule_C13(self):
        """If field :36B: is present in minimum one occurrence of sequence A1, then the type of settlement
        transaction must be a pair-off or a turn-around; that is, sequence E field :22F::SETR//PAIR or
        :22F::SETR//TURN must be present """
        if self.swift_message_obj.SequenceA_GeneralInformation.SubSequenceA1_Linkages:
            flag_36b = False
            for link in self.swift_message_obj.SequenceA_GeneralInformation.SubSequenceA1_Linkages:
                if link.QuantityOfFinancialInstrument:
                    flag_36b = True
                    break
            if flag_36b:
                if self.swift_message_obj.SequenceE_SettlementDetails:
                    indicator_pair_off_flag = FSecuritySettlementOutUtils.check_qualifier_exists(
                        self.swift_message_obj.SequenceE_SettlementDetails, 'Indicator', 'SETR//PAIR', [])
                    indicator_turn_around_flag = FSecuritySettlementOutUtils.check_qualifier_exists(
                        self.swift_message_obj.SequenceE_SettlementDetails, 'Indicator', 'SETR//TURN', [])
                    if not indicator_pair_off_flag and not indicator_turn_around_flag:
                        return 'If field :36B: is present in minimum one occurrence of sequence A1, then the type of settlement transaction must be a pair-off or a turn-around; that is, sequence E field :22F::SETR//PAIR or :22F::SETR//TURN must be present '

        return ''

    def network_rule_C14(self):
        """In sequence C, field :36B::SETT cannot appear more than twice (maximum two occurrences). When
        repeated, one occurrence must have Quantity Type Code FAMT and the other occurrence must have
        Quantity Type Code AMOR"""
        if self.swift_message_obj.SequenceC_FinancialInstrumentAccount:
            if self.swift_message_obj.SequenceC_FinancialInstrumentAccount.QuantityOfFinancialInstrumentToBeSettled:
                count = 0
                quantity_code = []
                for ins_details in self.swift_message_obj.SequenceC_FinancialInstrumentAccount.QuantityOfFinancialInstrumentToBeSettled:
                    if ins_details.value()[1:].startswith('SETT'):
                        quantity_code.append(ins_details.value()[7:11])
                        if count > 2:
                            return 'In sequence C, field :36B::SETT cannot appear more than twice (maximum two occurrences)'
                        count = count + 1
                if count == 2:  # Repeated
                    if not 'FAMT' in quantity_code or not 'AMOR' in quantity_code:
                        return 'In sequence C, field :36B::SETT cannot appear more than twice (maximum two occurrences). When repeated, one occurrence must have Quantity Type Code FAMT and the other occurrence must have Quantity Type Code AMOR'

        return ''

    def network_rule_C15(self):
        """A value date must only be provided for cash/securities split settlement. That is, in any occurrence of
        subsequence E3, if value date field :98a::VALU is present, then in sequence E field :22F::STCO//SPST
        must be present, and settlement amount field :19A::SETT must be present in the same subsequence E3"""
        if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE3_Amounts:
            valu_date_flag = False
            indicator_flag = False
            flag_19A = False
            subsequence_E3_where_VALU_is_present = None
            for amounts in self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE3_Amounts:
                if amounts.ValueDateTime_A:
                    if amounts.ValueDateTime_A.value()[1:].startswith('VALU'):
                        valu_date_flag = True
                        subsequence_E3_where_VALU_is_present = amounts
                        break
                elif amounts.ValueDateTime_C:
                    if amounts.ValueDateTime_C.value()[1:].startswith('VALU'):
                        valu_date_flag = True
                        subsequence_E3_where_VALU_is_present = amounts
                        break

            if valu_date_flag:
                if self.swift_message_obj.SequenceE_SettlementDetails.Indicator:
                    indicator_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceE_SettlementDetails,
                                                                                       'Indicator', 'STCO//SPST', [])
                if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE3_Amounts:
                    flag_19A = subsequence_E3_where_VALU_is_present.value()[1:].startswith("SETT")
                    if not indicator_flag or not flag_19A:
                        return 'A value date must only be provided for cash/securities split settlement. That is, in any occurrence of subsequence E3, if value date field :98a::VALU is present, then in sequence E field :22F::STCO//SPST must be present, and settlement amount field :19A::SETT must be present in the same subsequence E3'
        return ''

    def network_rule_C16(self):
        """In sequence F, if field :95a::EXCH Stock Exchange or :95a::TRRE Trade Regulator is present, then
    field :97a:: is not allowed in the same sequence"""
        if self.swift_message_obj.SequenceF_OtherParties:
            flag_95a = False
            flag_95a_exch = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceF_OtherParties, 'PARTY',
                                                                              'EXCH', ['P', 'Q', 'R', 'S', 'C', 'L'])
            if not flag_95a_exch:
                flag_95a_trre = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceF_OtherParties,
                                                                                  'PARTY', 'TRRE',
                                                                                  ['P', 'Q', 'R', 'S', 'C', 'L'])
            flag_95a = flag_95a_exch or flag_95a_trre
            if flag_95a:
                sequence_f_to_be_checked = None
                if flag_95a_exch:
                    for each_othrprty in self.swift_message_obj.SequenceF_OtherParties:
                        if sequence_f_to_be_checked:
                            break
                        for each_option in ['P', 'Q', 'R', 'S', 'C', 'L']:
                            qualifier_exists = FSecuritySettlementOutUtils._check_for_val(each_othrprty, 'PARTY',
                                                                                         each_option, "EXCH")
                            if qualifier_exists:
                                sequence_f_to_be_checked = each_othrprty
                                break
                if flag_95a_trre:
                    for each_othrprty in self.swift_message_obj.SequenceF_OtherParties:
                        if sequence_f_to_be_checked:
                            break
                        for each_option in ['P', 'Q', 'R', 'S', 'C', 'L']:
                            qualifier_exists = FSecuritySettlementOutUtils._check_for_val(each_othrprty, 'PARTY',
                                                                                         each_option, "TRRE")
                            if qualifier_exists:
                                sequence_f_to_be_checked = each_othrprty
                                break
                if sequence_f_to_be_checked.SafekeepingAccount:
                    return 'In sequence F, if field :95a::EXCH Stock Exchange or :95a::TRRE Trade Regulator is present, then field :97a:: is not allowed in the same sequence'

        return ''

    def network_rule_C17(self):
        """In sequence C, if field :95L::ALTE is present, then field :95a::ACOW must be present"""
        flag_95L_alte = False
        flag_95_acow = False
        if self.swift_message_obj.SequenceC_FinancialInstrumentAccount:
            flag_95L_alte = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_FinancialInstrumentAccount, 'Party',
                                                                              'ALTE', ['L'])
            if flag_95L_alte:
                flag_95_acow = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceC_FinancialInstrumentAccount, 'Party',
                                                                                 'ACOW', ['L', 'P', 'R'])
                if not flag_95_acow:
                    return 'In sequence C, if field :95L::ALTE is present, then field :95a::ACOW must be present'
        return ''

    def network_rule_C18(self):
        ret_msg = ''
        res1 = self._validate_c18_1()
        res2 = self._validate_c18_2()
        res3 = self._validate_c18_3()
        res4 = self._validate_c18_4()
        res5 = self._validate_c18_5()
        res6 = self._validate_c18_6()

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

    def _validate_c18_1(self):
        """In sequence B, field :94a::CLEA must not be present more than twice. When repeated, one and only
        one occurrence must be with format option L (:94L::CLEA)"""
        if self.swift_message_obj.SequenceB_TradeDetails:
            count_clea = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceB_TradeDetails, 'Place', 'CLEA',
                                                                    ['L', 'B', 'H'])
            if count_clea > 2:
                return 'In sequence B, field :94a::CLEA must not be present more than twice.'
            if count_clea == 2:
                count_format_l = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceB_TradeDetails, 'Place',
                                                                            'CLEA', ['L'])
                if count_format_l > 1:
                    return 'In sequence B, only one occurrence must be with format option L (:94L::CLEA)'

        return ''

    def _validate_c18_2(self):
        """In sequence B, field :94a::TRAD must not be present more than twice. When repeated, one and only
        one occurrence must be with format option L (:94L::TRAD)"""
        if self.swift_message_obj.SequenceB_TradeDetails:
            count_trad = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceB_TradeDetails, 'Place', 'TRAD',
                                                                    ['L', 'B', 'H'])
            if count_trad > 2:
                return 'In sequence B, field :94a::TRAD must not be present more than twice.'
            if count_trad == 2:
                count_format_l = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceB_TradeDetails, 'Place',
                                                                            'TRAD', ['L'])
                if count_format_l > 1:
                    return 'In sequence B, only one occurrence must be with format option L (:94L::TRAD)'

        return ''

    def _validate_c18_3(self):
        """In sequence C, field :94a::SAFE must not be present more than twice. When repeated, one and only
        one occurrence must be with format option L (:94L::SAFE)"""
        if self.swift_message_obj.SequenceC_FinancialInstrumentAccount:
            count_safe = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceC_FinancialInstrumentAccount, 'PlaceOfSafekeeping',
                                                                    'SAFE', ['B', 'C', 'F', 'L'])
            if count_safe > 2:
                return 'In sequence C, field :94a::SAFE must not be present more than twice.'
            if count_safe == 2:
                count_format_l = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceC_FinancialInstrumentAccount,
                                                                            'PlaceOfSafekeeping', 'SAFE', ['L'])
                if count_format_l > 1:
                    return 'In sequence C, only one occurrence must be with format option L (:94L::SAFE)'

        return ''

    def _validate_c18_4(self):
        """In each occurrence of subsequence E1, field :95a::ALTE must not be present more than twice. When
        repeated, one and only one occurrence must be with format option L"""
        if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties:
            count_alte = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties, 'PARTY',
                                                                    'ALTE', ['L', 'Q', 'P', 'R', 'S', 'C'])
            if count_alte > 2:
                return 'In each occurrence of subsequence E1, field :95a::ALTE must not be present more than twice.'
            if count_alte == 2:
                count_format_l = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties,
                                                                            'PARTY', 'ALTE', ['L'])
                if count_format_l > 1:
                    return 'In each occurrence of subsequence E1, only one occurrence must be with format option L '
        return ''

    def _validate_c18_5(self):
        """In each occurrence of subsequence E2, field :95a::ALTE must not be present more than twice. When
        repeated, one and only one occurrence must be with format option L (:95L::ALTE)"""
        if self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE2_CashParties:
            count_alte = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE2_CashParties, 'PARTY',
                                                                    'ALTE', ['L', 'P', 'R', 'Q', 'S'])
            if count_alte > 2:
                return 'In each occurrence of subsequence E1, field :95a::ALTE must not be present more than twice.'
            if count_alte == 2:
                count_format_l = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceE_SettlementDetails.SubSequenceE2_CashParties,
                                                                            'PARTY', 'ALTE', ['L'])
                if count_format_l > 1:
                    return 'In each occurrence of subsequence E2, only one occurrence must be with format option L '
        return ''

    def _validate_c18_6(self):
        """In each occurrence of sequence F, field :95a::ALTE must not be present more than twice. When
        repeated, one and only one occurrence must be with format option L (:95L::ALTE)"""
        if self.swift_message_obj.SequenceF_OtherParties:
            count_alte = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceF_OtherParties, 'PARTY', 'ALTE',
                                                                    ['C', 'P', 'R', 'Q', 'S'])
            if count_alte > 2:
                return 'In each occurrence of sequence F, field :95a::ALTE must not be present more than twice.'
            if count_alte == 2:
                count_format_l = FSecuritySettlementOutUtils.qualifier_count(self.swift_message_obj.SequenceF_OtherParties, 'PARTY',
                                                                            'ALTE', ['L'])
                if count_format_l > 1:
                    return 'In each occurrence of sequence F, only one occurrence must be with format option L '
        return ''

    def network_rule_C19(self):
        """In each occurrence of sequence F, if field :95a::ALTE is present with format option L,               then          field
        :95a::MEOR and field :95a::MERE must not be present in the same occurrence of the sequence"""
        if self.swift_message_obj.SequenceF_OtherParties:
            alte_flag = FSecuritySettlementOutUtils.check_qualifier_exists(self.swift_message_obj.SequenceF_OtherParties, 'PARTY',
                                                                          'ALTE', ['L'])
            if alte_flag:
                sequence_f_to_be_checked = None
                for each_othrprty in self.swift_message_obj.SequenceF_OtherParties:
                    qualifier_exists = FSecuritySettlementOutUtils._check_for_val(each_othrprty, 'PARTY', "L", "ALTE")
                    if qualifier_exists:
                        sequence_f_to_be_checked = each_othrprty
                        break
                if sequence_f_to_be_checked:
                    meor_flag = FSecuritySettlementOutUtils._check_for_val(sequence_f_to_be_checked, 'PARTY',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'], "MEOR")
                    mere_flag = FSecuritySettlementOutUtils._check_for_val(sequence_f_to_be_checked, 'PARTY',
                                                                          ['P', 'Q', 'R', 'S', 'C', 'L'], "MERE")

                if meor_flag or mere_flag:
                    return 'In each occurrence of sequence F, if field :95a::ALTE is present with format option L, then field :95a::MEOR and field :95a::MERE must not be present in the same occurrence of the sequence'
        return ""

