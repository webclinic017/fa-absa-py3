"""----------------------------------------------------------------------------
MODULE:
    FMT306OutBase

DESCRIPTION:
    This module provides the base class for the FMT306 outgoing implementation

CLASS:
    FMT306Base

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftMLUtils
import FSwiftWriterMessageHeader
import MT306
import acm
from FSwiftWriterEngine import validate_with, should_use_operations_xml

import FSwiftWriterLogger
import FSwiftWriterUtils
from FFXMMConfirmationOutUtils import *
from FFXMMOutBase import FFXMMOutBase

notifier = FSwiftWriterLogger.FSwiftWriterLogger('FXMMConfOut', 'FFXMMConfirmationOutNotify_Config')


class FMT306Base(FFXMMOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = "MT306"
        super(FMT306Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    def _message_sequences(self):
        self.swift_obj.SequenceA_GeneralInformation = MT306.MT306_SequenceA_GeneralInformation()
        self.swift_obj.SequenceA_GeneralInformation.swiftTag = "15A"
        self.swift_obj.SequenceA_GeneralInformation.formatTag = "False"

        self.swift_obj.SequenceB_TransactionDetails = MT306.MT306_SequenceB_TransactionDetails()
        self.swift_obj.SequenceB_TransactionDetails.swiftTag = "15B"
        self.swift_obj.SequenceB_TransactionDetails.formatTag = "False"
        self.swift_obj.SequenceB_TransactionDetails.SubsequenceB2_CalculationAgent = MT306.MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent()

        self.is_seq_b1 = self.__set_optional_seq_b1()
        # Setting Sequence C Settlement Instructions
        self.is_seq_c = self.__set_optional_seq_c()

        # Setting Sequence D Vanilla Block
        self.is_seq_d = self.__set_optional_seq_d()

        # Setting Sequence E SequenceE_PayoutAmount Amount
        self.is_seq_e = self.__set_optional_seq_e()

        # Setting Sequence F Barrier Block
        self.is_seq_f = self.__set_optional_seq_f()

        # Setting Sequence H Non Deliverable Option
        self.is_seq_h = self.__set_optional_seq_h()

    # ------------------ senders_reference -----------------------
    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_20_Type)
    def _validate_senders_reference_20(self, val):
        validate_slash_and_double_slash(val, "Sender's Reference")
        return val

    # setter
    def _set_senders_reference_20(self, val):
        self.swift_obj.SequenceA_GeneralInformation.SendersReference = val
        self.swift_obj.SequenceA_GeneralInformation.SendersReference.swiftTag = "20"

    # ------------------ related_reference -----------------------
    # Getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_21_Type, is_mandatory=True)
    def _validate_related_reference_21(self, val):
        return val

    def _check_condition_set_related_reference_21(self):
        if get_type_of_operation(self.acm_obj) in ['AMND', 'CANC']:
            return True
        else:
            return False

    # setter
    def _set_related_reference_21(self, val):
        self.swift_obj.SequenceA_GeneralInformation.RelatedReference = val
        self.swift_obj.SequenceA_GeneralInformation.RelatedReference.swiftTag = "21"

    # ------------------ type_of_operation -----------------------
    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_22A_Type)
    def _validate_type_of_operation_22A(self, val):
        return val

    # setter
    def _set_type_of_operation_22A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.TypeOfOperation = val
        self.swift_obj.SequenceA_GeneralInformation.TypeOfOperation.swiftTag = "22A"

    # ------------------ scope_of_operation -----------------------
    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_94A_Type)
    def _validate_scope_of_operation_94A(self, val):
        return val

    # setter
    def _set_scope_of_operation_94A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.ScopeOfOperation = val
        self.swift_obj.SequenceA_GeneralInformation.ScopeOfOperation.swiftTag = "94A"

    # ------------------ common_reference -----------------------
    # getter
    def common_reference_22C(self):
        '''Returns dictionary val_dict with keys 'SENDERS_BIC', 'RECEIVERS_BIC', 'REFERENCE_CODE' and their correpsonding values'''
        if self.use_operations_xml:
            val_dict = {}
            senders_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SENDER_BIC'])
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'RECEIVER_BIC'])
            option_style = self.__get_option_style()
            is_seq_d = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                ['SWIFT', 'SETTLEMENT_TYPE'])
            is_seq_g = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'CURRENCY_PAIR'])
            reference_code = "0.0"
            if is_seq_d and option_style not in ['BINA', 'DIGI', 'NOTO']:
                reference_code = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'STRIKE_PRICE'],
                                                                          ignore_absense=True)
            elif is_seq_g and option_style in ['BINA', 'DIGI', 'NOTO']:
                reference_code = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'TRIGGER_LEVEL'],
                                                                          ignore_absense=True)

            val_dict['SENDERS_BIC'] = senders_bic
            val_dict['RECEIVER_BIC'] = receivers_bic
            val_dict['REFERENCE_CODE'] = reference_code


        else:
            val_dict = {}
            val_dict['SENDERS_BIC'] = get_senders_bic(self.acm_obj)
            val_dict['RECEIVER_BIC'] = get_receivers_bic(self.acm_obj)
            option_style = get_option_style_code(self.acm_obj)
            is_seq_d = get_settlement_type(self.acm_obj)
            is_seq_g = get_currency_pair(self.acm_obj)
            reference_code = "0.0"
            if is_seq_d and option_style not in ['BINA', 'DIGI', 'NOTO']:
                reference_code = get_strike_price(self.acm_obj)
            elif is_seq_g and option_style in ['BINA', 'DIGI', 'NOTO']:
                reference_code = get_barrier_level(self.acm_obj)
            val_dict['REFERENCE_CODE'] = str(reference_code)
        return val_dict

    # formatter
    def _format_common_reference_22C(self, val):
        senders_bic = val.get('SENDERS_BIC')
        receivers_bic = val.get('RECEIVER_BIC')
        reference_code = val.get('REFERENCE_CODE')
        if senders_bic and receivers_bic and reference_code:
            reference_code_part = represent_amount_in_four_digits(reference_code)
            if receivers_bic[0:4] + receivers_bic[-2:] > senders_bic[0:4] + senders_bic[-2:]:
                common_reference = senders_bic[0:4] + senders_bic[-2:] + reference_code_part + receivers_bic[
                                                                                               0:4] + receivers_bic[-2:]
            else:
                common_reference = receivers_bic[0:4] + receivers_bic[-2:] + reference_code_part + senders_bic[
                                                                                                   0:4] + senders_bic[
                                                                                                          -2:]
            return common_reference

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_22C_Type)
    def _validate_common_reference_22C(self, val):
        return val

    # setter
    def _set_common_reference_22C(self, val):
        self.swift_obj.SequenceA_GeneralInformation.CommonReference = val
        self.swift_obj.SequenceA_GeneralInformation.CommonReference.swiftTag = "22C"

    # ------------------ contract_number_party_A -----------------------
    # getter
    def contract_number_party_A_21N(self):
        ''' Returns oid of the corresponding trade'''
        if self.use_operations_xml:
            contract_no_party_a = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'CONTRACT_NO_PARTY_A'])
            return contract_no_party_a
        else:
            return get_contract_no_of_partyA(self.acm_obj)

    # formatter
    def _format_contract_number_party_A_21N(self, val):
        return val

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_21N_Type)
    def _validate_contract_number_party_A_21N(self, val):
        return val

    # setter
    def _set_contract_number_party_A_21N(self, val):
        self.swift_obj.SequenceA_GeneralInformation.ContractNumberPartyA = val
        self.swift_obj.SequenceA_GeneralInformation.ContractNumberPartyA.swiftTag = "21N"

    # ------------------ option_style -----------------------
    # getter
    def option_style_12F(self):
        '''Returns option style code as string'''
        if self.use_operations_xml:
            option_style = self.__get_option_style()
            return option_style
        else:
            return get_option_style_code(self.acm_obj)

    # formatter
    def _format_option_style_12F(self, val):
        return val

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_12F_Type)
    def _validate_option_style_12F(self, val):
        return val

    # setter
    def _set_option_style_12F(self, val):
        self.swift_obj.SequenceA_GeneralInformation.OptionStyle = val
        self.swift_obj.SequenceA_GeneralInformation.OptionStyle.swiftTag = "12F"

    # ------------------ expiration_style -----------------------
    # getter
    def expiration_style_12E(self):
        '''Returns expiration style code as either 'AMER' or 'EURO' '''
        if self.use_operations_xml:
            expiration_style = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                        ['SWIFT', 'EXPIRATION_STYLE'])
        else:
            expiration_style = get_option_expiration_style(self.acm_obj)
        return expiration_style

    # formatter
    def _format_expiration_style_12E(self, val):
        return val

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_12E_Type)
    def _validate_expiration_style_12E(self, val):
        return val

    # setter
    def _set_expiration_style_12E(self, val):
        self.swift_obj.SequenceA_GeneralInformation.ExpirationStyle = val
        self.swift_obj.SequenceA_GeneralInformation.ExpirationStyle.swiftTag = "12E"

    # ------------------ barrier_indicator -----------------------
    # getter
    def barrier_indicator_17A(self):
        '''Returns 'Y' or 'N' '''
        if self.use_operations_xml:
            barrier_indicator = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'BARRIER_INDICATOR'])
        else:
            barrier_indicator = get_barrier_indicator(self.acm_obj)
        return barrier_indicator

    # formatter
    def _format_barrier_indicator_17A(self, val):
        return val

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_17A_Type)
    def _validate_barrier_indicator_17A(self, val):
        return val

    # setter
    def _set_barrier_indicator_17A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.BarrierIndicator = val
        self.swift_obj.SequenceA_GeneralInformation.BarrierIndicator.swiftTag = "17A"

    # ------------------ non_deliverable_indicator -----------------------
    # getter
    def non_deliverable_indicator_17F(self):
        '''Returns 'Y' or 'N' '''
        if self.use_operations_xml:
            non_deliverable_indicator = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'NON_DELIVERABLE_INDICATOR'])
        else:
            non_deliverable_indicator = get_non_deliverable_indicator(self.acm_obj)
        return non_deliverable_indicator

    # formatter
    def _format_non_deliverable_indicator_17F(self, val):
        return val

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_17F_Type)
    def _validate_non_deliverable_indicator_17F(self, val):
        return val

    # setter
    def _set_non_deliverable_indicator_17F(self, val):
        self.swift_obj.SequenceA_GeneralInformation.NonDeliverableIndicator = val
        self.swift_obj.SequenceA_GeneralInformation.NonDeliverableIndicator.swiftTag = "17F"

    # ------------------ type_event -----------------------
    # getter
    def type_event_22K(self):
        '''Returns confirmaito nevent type code as string  '''
        if self.use_operations_xml:
            type_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TYPE_EVENT'])
        else:
            type_event = get_type_of_event(self.acm_obj)
        return type_event

    # formatter
    def _format_type_event_22K(self, val):
        if val:
            if val == "OTHR":
                narrative = "New Trade Amendment"
                val += "/" + narrative
            return val

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_22K_Type)
    def _validate_type_event_22K(self, val):
        return val

    # setter
    def _set_type_event_22K(self, val):
        self.swift_obj.SequenceA_GeneralInformation.TypeOfEvent = val
        self.swift_obj.SequenceA_GeneralInformation.TypeOfEvent.swiftTag = "22K"

    # ------------------ party_A -----------------------

    # option getter
    def get_partyA_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_partyA(self):
        if self.use_operations_xml:
            party_a_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT',
                                                                                                    'PARTY_A_OPTION'])
        else:
            party_a_option = self.get_partyA_option()
        if party_a_option == "A":
            return 'partyA_82A'
        elif party_a_option == "D":
            return 'partyA_82D'
        else:
            notifier.WARN(
                "%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,
                                                                                       str(party_a_option),
                                                                                       'PartyA_82a'))

        return 'partyA_82A'

    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_82A_Type)
    def _validate_partyA_82A(self, val):
        return val

    # setter
    def _setpartyA_82A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.PartyA_A = val
        self.swift_obj.SequenceA_GeneralInformation.PartyA_A.swiftTag = "82A"

    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_82D_Type)
    def _validate_partyA_82D(self, val):
        return val

    # setter
    def _setpartyA_82D(self, val):
        self.swift_obj.SequenceA_GeneralInformation.PartyA_D = val
        self.swift_obj.SequenceA_GeneralInformation.PartyA_D.swiftTag = "82D"

    # ------------------ party_B -----------------------
    # option getter
    def get_partyB_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_partyB(self):
        if self.use_operations_xml:
            party_b_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT',
                                                                                                    'PARTY_B_OPTION'])
        else:
            party_b_option = self.get_partyB_option()

        if party_b_option == "A":
            return 'partyB_87A'
        elif party_b_option == "D":
            return 'partyB_87D'
        else:
            notifier.WARN(
                "%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,
                                                                                       str(party_b_option),
                                                                                       'PartyB_87a'))
        return 'partyB_87A'

    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_87A_Type)
    def _validate_partyB_87A(self, val):
        return val

    # setter
    def _setpartyB_87A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.PartyB_A = val
        self.swift_obj.SequenceA_GeneralInformation.PartyB_A.swiftTag = "87A"

    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_87D_Type)
    def _validate_partyB_87D(self, val):
        return val

    # setter
    def _setpartyB_87D(self, val):
        self.swift_obj.SequenceA_GeneralInformation.PartyB_D = val
        self.swift_obj.SequenceA_GeneralInformation.PartyB_D.swiftTag = "87D"

    # ------------------ agreement -----------------------
    # getter
    def agreement_77H(self):
        '''Returns dictionary with keys 'AGREEMENT_DATE', 'AGREEMENT_TYPE', 'AGREEMENT_VERSION' and their corresponding values '''
        if self.use_operations_xml:
            val_dict = {}
            agreement_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'DATE_OF_AGREEMENT'],
                                                                      ignore_absense=True)
            agreement_type = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'TYPE_OF_AGREEMENT'])
            agreement_version = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'VERSION_OF_AGREEMENT'],
                                                                         ignore_absense=True)
            val_dict['AGREEMENT_DATE'] = agreement_date
            val_dict['AGREEMENT_TYPE'] = agreement_type
            val_dict['AGREEMENT_VERSION'] = agreement_version
        else:
            val_dict = {}
            val_dict['AGREEMENT_DATE'] = get_date_of_agreement(self.acm_obj)
            val_dict['AGREEMENT_TYPE'] = get_type_of_agreement(self.acm_obj)
            val_dict['AGREEMENT_VERSION'] = get_version_of_agreement(self.acm_obj)
        return val_dict

    # formatter
    def _format_agreement_77H(self, val):
        agreement_date = val.get('AGREEMENT_DATE')
        agreement_type = val.get('AGREEMENT_TYPE')
        agreement_version = val.get('AGREEMENT_VERSION')
        date_format = '%Y%m%d'

        if agreement_type:
            agreement = str(agreement_type)
            if agreement_date:
                agreement += "/" + FSwiftWriterUtils.format_date(agreement_date, date_format)
            if agreement_version:
                agreement += "//" + agreement_version
            return str(agreement)

    # validator
    @validate_with(MT306.MT306_SequenceA_GeneralInformation_77H_Type)
    def _validate_agreement_77H(self, val):
        return val

    # setter
    def _set_agreement_77H(self, val):
        self.swift_obj.SequenceA_GeneralInformation.TypeDateVersionOfTheAgreement = val
        self.swift_obj.SequenceA_GeneralInformation.TypeDateVersionOfTheAgreement.swiftTag = "77H"

    # ------------------ buy_sell_indicator -----------------------
    # getter
    def buy_sell_indicator_17V(self):
        '''Returns 'B' or 'S' '''
        if self.use_operations_xml:
            buy_sell_indicator = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'BUY_SELL_INDICATOR'])
        else:
            buy_sell_indicator = get_buy_sell_indicator(self.acm_obj)
        return buy_sell_indicator

    # formatter
    def _format_buy_sell_indicator_17V(self, val):
        return val

    # validator
    @validate_with(MT306.MT306_SequenceB_TransactionDetails_17V_Type)
    def _validate_buy_sell_indicator_17V(self, val):
        return val

    # setter
    def _set_buy_sell_indicator_17V(self, val):
        self.swift_obj.SequenceB_TransactionDetails.BuySellIndicator = val
        self.swift_obj.SequenceB_TransactionDetails.BuySellIndicator.swiftTag = "17V"

    # ------------------ trade_date -----------------------
    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT306.MT306_SequenceB_TransactionDetails_30T_Type)
    def _validate_trade_date_30T(self, val):
        return val

    # setter
    def _set_trade_date_30T(self, val):
        self.swift_obj.SequenceB_TransactionDetails.TradeDate = val
        self.swift_obj.SequenceB_TransactionDetails.TradeDate.swiftTag = "30T"

    # ------------------ expiration_date -----------------------
    # getter
    def expiration_date_30X(self):
        '''Returns expiration date as string'''
        if self.use_operations_xml:
            expiration_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT',
                                                                                                     'EXPIRATION_DATE'])
        else:
            expiration_date = get_option_expiry_date(self.acm_obj)
        return expiration_date

    # formatter
    def _format_expiration_date_30X(self, val):
        if val:
            date_format = '%Y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)
            return val

    # validator
    @validate_with(MT306.MT306_SequenceB_TransactionDetails_30X_Type)
    def _validate_expiration_date_30X(self, val):
        return val

    # setter
    def _set_expiration_date_30X(self, val):
        self.swift_obj.SequenceB_TransactionDetails.ExpirationDate = val
        self.swift_obj.SequenceB_TransactionDetails.ExpirationDate.swiftTag = "30X"

    # ------------------ expiration_location_time -----------------------
    # getter
    def expiration_location_time_29E(self):
        '''Returns dictionary with keys 'EXPIRATION_LOCATION', 'EXPIRATION_TIME' and their correpsonding values '''
        if self.use_operations_xml:
            val_dict = {}
            expiration_location = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'EXPIRATION_LOCATION'])
            expiration_time = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT',
                                                                                                     'EXPIRATION_TIME'])
            val_dict['EXPIRATION_LOCATION'] = expiration_location
            val_dict['EXPIRATION_TIME'] = expiration_time
        else:
            val_dict = {}
            val_dict['EXPIRATION_LOCATION'] = get_option_expiry_location(self.acm_obj)
            val_dict['EXPIRATION_TIME'] = get_option_expiry_time(self.acm_obj)

        return val_dict

    # formatter
    def _format_expiration_location_time_29E(self, val):
        if val:
            expiration_location = val.get('EXPIRATION_LOCATION')
            expiration_time = val.get('EXPIRATION_TIME')

            if expiration_location and expiration_time:
                val = str(expiration_location) + "/" + str(expiration_time)
                return val

    # validator
    @validate_with(MT306.MT306_SequenceB_TransactionDetails_29E_Type)
    def _validate_expiration_location_time_29E(self, val):
        return val

    # setter
    def _set_expiration_location_time_29E(self, val):
        self.swift_obj.SequenceB_TransactionDetails.ExpirationLocationAndTime = val
        self.swift_obj.SequenceB_TransactionDetails.ExpirationLocationAndTime.swiftTag = "29E"

    # ------------------ final_settlement_date -----------------------
    # getter
    def final_settlement_date_30F(self):
        '''Returns final settlement date as string'''
        if self.use_operations_xml:
            final_settlement_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                             ['SWIFT', 'FINAL_SETTLEMENT_DATE'])
        else:
            final_settlement_date = get_option_final_settlement_date(self.acm_obj)
        return final_settlement_date

    # formatter
    def _format_final_settlement_date_30F(self, val):
        if val:
            date_format = '%Y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)
            return val

    # validator
    @validate_with(MT306.MT306_SequenceB_TransactionDetails_30F_Type)
    def _validate_final_settlement_date_30F(self, val):
        return val

    def _check_condition_set_final_settlement_date_30F(self):
        # According to Network rule c7, 30F is mandatory if 12E has value EURO
        val = self.expiration_style_12E()
        if val == "EURO":
            return True
        else:
            return False

    # setter
    def _set_final_settlement_date_30F(self, val):
        self.swift_obj.SequenceB_TransactionDetails.FinalSettlementDate_F = val
        self.swift_obj.SequenceB_TransactionDetails.FinalSettlementDate_F.swiftTag = "30F"

    # ------------------ premium_payment_date -----------------------
    # getter
    def premium_payment_date_30V(self):
        '''Returns premium payment date as string'''
        if self.use_operations_xml:
            premium_payment_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                            ['SWIFT', 'PREMIUM_PAYMENT_DATE'])
        else:
            premium_payment_date = get_premium_payment_date(self.acm_obj)
        return premium_payment_date

    # formatter
    def _format_premium_payment_date_30V(self, val):
        if val:
            date_format = '%Y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)
            return val

    # validator
    @validate_with(MT306.MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails_30V_Type)
    def _validate_premium_payment_date_30V(self, val):
        return val

    def _check_condition_set_premium_payment_date_30V(self):
        if self.is_seq_b1:
            return True
        else:
            return False

    # setter
    def _set_premium_payment_date_30V(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubsequenceB1_PremiumDetails.PremiumPaymentDate = val
        self.swift_obj.SequenceB_TransactionDetails.SubsequenceB1_PremiumDetails.PremiumPaymentDate.swiftTag = "30V"

    # ------------------ premium_currency_and_amount -----------------------
    # getter
    def premium_currency_and_amount_34B(self):
        '''Returns dictionary with keys 'PREMIUM_CURRENCY', 'PREMIUM_AMOUNT' and their corresponding values'''
        if self.use_operations_xml:
            val_dict = {}
            premium_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                        ['SWIFT', 'PREMIUM_CURRENCY'])
            premium_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'PREMIUM_AMOUNT'])
            val_dict['PREMIUM_CURRENCY'] = premium_currency
            val_dict['PREMIUM_AMOUNT'] = premium_amount
        else:
            val_dict = {}
            val_dict['PREMIUM_CURRENCY'] = get_premium_payment_currency(self.acm_obj)
            val_dict['PREMIUM_AMOUNT'] = get_premium_payment_amount(self.acm_obj)
        return val_dict

    # formatter
    def _format_premium_currency_and_amount_34B(self, val):
        if val:
            premium_amount = val.get('PREMIUM_AMOUNT')
            premium_currency = val.get('PREMIUM_CURRENCY')

            if premium_amount and premium_currency and premium_currency not in ['XAU', 'XAG', 'XPD', 'XPT']:
                val = premium_currency + FSwiftMLUtils.float_to_swiftmt(
                    apply_currency_precision(premium_currency, float(premium_amount)))
                return str(val)

    # validator
    @validate_with(MT306.MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails_34B_Type)
    def _validate_premium_currency_and_amount_34B(self, val):
        validateAmount(val[3:], 15, "Premium currency and Amount")
        return val

    def _check_condition_set_premium_currency_and_amount_34B(self):
        if self.is_seq_b1:
            return True
        else:
            return False

    # setter
    def _set_premium_currency_and_amount_34B(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubsequenceB1_PremiumDetails.PremiumCurrencyAndAmount = val
        self.swift_obj.SequenceB_TransactionDetails.SubsequenceB1_PremiumDetails.PremiumCurrencyAndAmount.swiftTag = "34B"

    # ------------------ calculation_agent -----------------------
    # option getter
    def get_calculation_agent_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_calculation_agent(self):
        '''Returns name of the calculation agent getter like 'calculation_agent_84A', 'calculation_agent_84B', 'calculation_agent_84D', 'calculation_agent_84J' '''
        if self.use_operations_xml:
            calculation_agent_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                ['SWIFT', 'CALCULATION_AGENT_OPTION'])
        else:
            # This is a special handling for MT306 and it should remain their unless agreed on to change
            calculation_agent_option = self.get_calculation_agent_option()

            if calculation_agent_option != 'J':
                calc_agent = self.acm_obj.Trade().Calcagent()
                if calc_agent == 'Both':
                    calculation_agent_option = 'D'
                elif calc_agent != 'CP' and calc_agent != 'We':
                    calculation_agent_option = 'J'
        if calculation_agent_option == "A":
            # self._setoption_calculation_agent_84A()
            return 'calculation_agent_84A'
        elif calculation_agent_option == "B":
            # self._setoption_calculation_agent_84B()
            return 'calculation_agent_84B'
        elif calculation_agent_option == "D":
            # self._setoption_calculation_agent_84D()
            return 'calculation_agent_84D'
        elif calculation_agent_option == "J":
            # self._setoption_calculation_agent_84J()
            return 'calculation_agent_84J'
        else:
            notifier.WARN(
                "%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,
                                                                                       str(calculation_agent_option),
                                                                                       'CalculationAgent_84a'))
        return 'calculation_agent_84A'

    # getter
    def calculation_agent_84A(self):
        '''Returns dictionary with keys 'CALCULATION_AGENT_BIC', 'CALCULATION_AGENT_ACCOUNT' and their corresponding  values'''
        if self.use_operations_xml:
            val_dict = {}
            calculation_agent_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                             ['SWIFT', 'CALCULATION_AGENT_BIC'])
            calculation_agent_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'CALCULATION_AGENT_ACCOUNT'],
                                                                                 ignore_absense=True)
            val_dict['CALCULATION_AGENT_BIC'] = calculation_agent_bic
            val_dict['CALCULATION_AGENT_ACCOUNT'] = calculation_agent_account
        else:
            val_dict = {}
            val_dict['CALCULATION_AGENT_BIC'] = get_calculation_agent_bic(self.acm_obj)
            val_dict['CALCULATION_AGENT_ACCOUNT'] = get_calculation_agent_account(self.acm_obj)

        return val_dict

    # formatter
    def _format_calculation_agent_84A(self, val):
        if val:
            calculation_agent_bic = val.get('CALCULATION_AGENT_BIC')
            calculation_agent_account = val.get('CALCULATION_AGENT_ACCOUNT')
            if calculation_agent_bic:
                val = str(calculation_agent_bic)
                if calculation_agent_account:
                    val = '/' + str(calculation_agent_account) + "\n" + str(val)
                return val

    # validator
    @validate_with(MT306.MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84A_Type)
    def _validate_calculation_agent_84A(self, val):
        return val

    # setter
    def _setcalculation_agent_84A(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubsequenceB2_CalculationAgent.CalculationAgent_A = val
        self.swift_obj.SequenceB_TransactionDetails.SubsequenceB2_CalculationAgent.CalculationAgent_A.swiftTag = "84A"

    # getter
    def calculation_agent_84B(self):
        '''Returns dictionary with keys 'CALCULATION_AGENT_BIC', 'CALCULATION_AGENT_ACCOUNT', 'CALCUALTION_AGENT_NAME', 'CALCUALTION_AGENT_LOCATION' and their corresponding  values'''
        if self.use_operations_xml:
            val_dict = {}
            calculation_agent_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'CALCULATION_AGENT_ACCOUNT'],
                                                                                 ignore_absense=True)
            calculation_agent_name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                              ['SWIFT', 'CALCULATION_AGENT_NAME'])
            calculation_agent_location = self.__get_calc_agent_location(calculation_agent_name)

            val_dict['CALCULATION_AGENT_ACCOUNT'] = calculation_agent_account
            val_dict['CALCUALTION_AGENT_NAME'] = calculation_agent_name
            val_dict['CALCUALTION_AGENT_LOCATION'] = calculation_agent_location
        else:
            val_dict = {}
            val_dict['CALCULATION_AGENT_ACCOUNT'] = get_calculation_agent_account(self.acm_obj)
            val_dict['CALCUALTION_AGENT_NAME'] = get_calculation_agent_name(self.acm_obj)
            val_dict['CALCUALTION_AGENT_LOCATION'] = get_calculation_agent_location(self.acm_obj)

        return val_dict

    # formatter
    def _format_calculation_agent_84B(self, val):
        calculation_agent_location = val.get('CALCUALTION_AGENT_LOCATION')
        calculation_agent_account = val.get('CALCULATION_AGENT_ACCOUNT')
        val = ''
        if calculation_agent_location:
            if calculation_agent_account:
                val = '/' + str(calculation_agent_account) + "\n" + str(calculation_agent_location)
            else:
                val = str(calculation_agent_location)
        elif calculation_agent_account:
            val = '/' + str(calculation_agent_account)
        return val

    # validator
    @validate_with(MT306.MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84B_Type)
    def _validate_calculation_agent_84B(self, val):
        return val

    # setter
    def _setcalculation_agent_84B(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubsequenceB2_CalculationAgent.CalculationAgent_B = val
        self.swift_obj.SequenceB_TransactionDetails.SubsequenceB2_CalculationAgent.CalculationAgent_B.swiftTag = "84B"

    # getter
    def calculation_agent_84D(self):
        '''Returns dictionary with keys 'CALCULATION_AGENT_ACCOUNT', 'CALCUALTION_AGENT_NAME', 'CALCUALTION_AGENT_ADDRESS' and their corresponding  values'''
        if self.use_operations_xml:
            val_dict = {}
            calculation_agent_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'CALCULATION_AGENT_ACCOUNT'],
                                                                                 ignore_absense=True)
            calculation_agent_name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                              ['SWIFT', 'CALCULATION_AGENT_NAME'])
            calculation_agent_address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'CALCULATION_AGENT_ADDRESS'])
            val_dict['CALCULATION_AGENET_ACCOUNT'] = calculation_agent_account
            val_dict['CALCULATION_AGENT_NAME'] = calculation_agent_name
            val_dict['CALCULATION_AGENT_ADDRESS'] = calculation_agent_address
        else:
            val_dict = {}
            val_dict['CALCULATION_AGENET_ACCOUNT'] = get_calculation_agent_account(self.acm_obj)
            val_dict['CALCULATION_AGENT_NAME'] = get_calculation_agent_name(self.acm_obj)
            val_dict['CALCULATION_AGENT_ADDRESS'] = get_calculation_agent_address(self.acm_obj)
        return val_dict

    # formatter
    def _format_calculation_agent_84D(self, val):
        calculation_agent_account = val.get('CALCULATION_AGENET_ACCOUNT')
        calculation_agent_name = val.get('CALCULATION_AGENT_NAME')
        calculation_agent_address = val.get('CALCULATION_AGENT_ADDRESS')

        if calculation_agent_name and calculation_agent_address:
            name = FSwiftWriterUtils.split_text_and_prefix(calculation_agent_name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(calculation_agent_address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if calculation_agent_account:
                val = "/" + str(calculation_agent_account) + "\n" + str(val)
            return val
        elif calculation_agent_name:
            name = FSwiftWriterUtils.split_text_and_prefix(calculation_agent_name, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name)
            if calculation_agent_account:
                val = "/" + str(calculation_agent_account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT306.MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84D_Type)
    def _validate_calculation_agent_84D(self, val):
        return val

    # setter
    def _setcalculation_agent_84D(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubsequenceB2_CalculationAgent.CalculationAgent_D = val
        self.swift_obj.SequenceB_TransactionDetails.SubsequenceB2_CalculationAgent.CalculationAgent_D.swiftTag = "84D"

    # getter
    def calculation_agent_84J(self):
        '''Returns dictionary with keys 'CALCULATION_AGENT_ACCOUNT', 'CALCUALTION_AGENT_NAME', 'CALCUALTION_AGENT_ADDRESS', 'CALCUALTION_AGENT_BIC' and their corresponding  values'''
        if self.use_operations_xml:
            val_dict = {}
            calculation_agent_account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'CALCULATION_AGENT_ACCOUNT'],
                                                                                 ignore_absense=True)
            calculation_agent_name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                              ['SWIFT', 'CALCULATION_AGENT_NAME'])
            calculation_agent_address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'CALCULATION_AGENT_ADDRESS'])
            calculation_agent_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                             ['SWIFT', 'CALCULATION_AGENT_BIC'])

            val_dict['CALCULATION_AGENET_ACCOUNT'] = calculation_agent_account
            val_dict['CALCUALTION_AGENT_NAME'] = calculation_agent_name
            val_dict['CALCUALTION_AGENT_ADDRESS'] = calculation_agent_address
            val_dict['CALCULATION_AGENT_BIC'] = calculation_agent_bic
        else:
            val_dict = {}
            val_dict['CALCULATION_AGENT_BIC'] = get_calculation_agent_bic(self.acm_obj)
            val_dict['CALCULATION_AGENET_ACCOUNT'] = get_calculation_agent_account(self.acm_obj)
            val_dict['CALCUALTION_AGENT_NAME'] = get_calculation_agent_name(self.acm_obj)
            val_dict['CALCUALTION_AGENT_ADDRESS'] = get_calculation_agent_address(self.acm_obj)

        return val_dict

    # formatter
    def _format_calculation_agent_84J(self, val):
        calculation_agent_name = val.get('CALCUALTION_AGENT_NAME')
        calculation_agent_account = val.get('CALCULATION_AGENET_ACCOUNT')
        calculation_agent_address = val.get('CALCUALTION_AGENT_ADDRESS')
        calculation_agent_bic = val.get('CALCULATION_AGENT_BIC')
        if calculation_agent_name:
            val = '/ABIC/' + (calculation_agent_bic or 'UKWN')
            if calculation_agent_account:
                val = val + "/ACCT/" + calculation_agent_account
            if calculation_agent_address:
                val = val + '/ADD1/' + calculation_agent_address
            val = val + '/NAME/' + calculation_agent_name
            lines = FSwiftWriterUtils.split_text_on_character_limit(val, 40)
            val = FSwiftWriterUtils.allocate_space_for_n_lines(5, lines)
            return val

    # validator
    @validate_with(MT306.MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84J_Type)
    def _validate_calculation_agent_84J(self, val):
        return val

    # setter
    def _setcalculation_agent_84J(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubsequenceB2_CalculationAgent.CalculationAgent_J = val
        self.swift_obj.SequenceB_TransactionDetails.SubsequenceB2_CalculationAgent.CalculationAgent_J.swiftTag = "84J"

    # ------------------ receiving_agent -----------------------


    # option getter
    def get_receiving_agent_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_receiving_agent(self):
        '''Returns receiving agent getter name as string like 'receiving_agent_57A', 'receiving_agent_57D' '''
        if self.use_operations_xml:
            receiving_agent_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                              ['SWIFT',
                                                                               'SIP_PARTY_RECEIVING_AGENT_OPTION'])
        else:
            receiving_agent_option = self.get_receiving_agent_option()

        if receiving_agent_option == "A" and self.is_seq_c:
            # self._setoption_receiving_agent_57A()
            return 'receiving_agent_57A'
        elif receiving_agent_option == "D":
            # self._setoption_receiving_agent_57D()
            return 'receiving_agent_57D'
        else:
            notifier.WARN(
                "%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,
                                                                                       str(receiving_agent_option),
                                                                                       'SETTDETReceivingAgent_57a'))
        return 'receiving_agent_57A'

    # getter
    def receiving_agent_57A(self):
        '''Returns dictionary with keys 'BIC', 'ACCOUNT' and their corresponding  values'''
        if self.use_operations_xml:
            val_dict = {}
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SIP_PARTY_RECEIVING_AGENT_BIC'])
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIP_PARTY_RECEIVING_AGENT_ACCOUNT'],
                                                               ignore_absense=True)
            val_dict['BIC'] = bic
            val_dict['ACCOUNT'] = account
        else:
            val_dict = {}
            val_dict['BIC'] = get_receiving_agent_bic_for_sett_instr_for_premium_payment(self.acm_obj)
            val_dict['ACCOUNT'] = get_receiving_agent_account_for_sett_instr_for_premium_payment(self.acm_obj)
        return val_dict

    # formatter
    def _format_receiving_agent_57A(self, val):
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT306.MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57A_Type)
    def _validate_receiving_agent_57A(self, val):
        return val

    # setter
    def _setreceiving_agent_57A(self, val):
        self.swift_obj.SequenceC_SettlementInstructionsforPaymentofPremium.ReceivingAgent_A = val
        self.swift_obj.SequenceC_SettlementInstructionsforPaymentofPremium.ReceivingAgent_A.swiftTag = "57A"

    # getter
    def receiving_agent_57D(self):
        '''Returns dictionary with keys 'NAME', 'ADDRESS', 'ACCOUNT' and their corresponding  values'''
        if self.use_operations_xml:
            val_dict = {}
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                            ['SWIFT', 'SIP_PARTY_RECEIVING_AGENT_NAME'])
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIP_PARTY_RECEIVING_AGENT_ADDRESS'])
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIP_PARTY_RECEIVING_AGENT_ACCOUNT'],
                                                               ignore_absense=True)

            val_dict['NAME'] = name
            val_dict['ADDRESS'] = address
            val_dict['ACCOUNT'] = account
        else:
            val_dict = {}
            val_dict['NAME'] = get_receiving_agent_name_for_sett_instr_for_premium_payment(self.acm_obj)
            val_dict['ADDRESS'] = get_receiving_agent_address_for_sett_instr_for_premium_payment(self.acm_obj)
            val_dict['ACCOUNT'] = get_receiving_agent_account_for_sett_instr_for_premium_payment(self.acm_obj)

        return val_dict

    # formatter
    def _format_receiving_agent_57D(self, val):
        name = val.get('NAME')
        address = val.get('ADDRESS')
        account = val.get('ACCOUNT')

        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT306.MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57D_Type)
    def _validate_receiving_agent_57D(self, val):
        return val

    # setter
    def _setreceiving_agent_57D(self, val):
        self.swift_obj.SequenceC_SettlementInstructionsforPaymentofPremium.ReceivingAgent_D = val
        self.swift_obj.SequenceC_SettlementInstructionsforPaymentofPremium.ReceivingAgent_D.swiftTag = "57D"

    # ------------------ earliest_exercise_date -----------------------
    # getter
    def earliest_exercise_date_30P(self):
        '''Returns earliest exercise date as string'''
        if self.use_operations_xml:
            earliest_exercise_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                              ['SWIFT', 'EARLIEST_EXERCISE_DATE'],
                                                                              ignore_absense=True)
        else:
            earliest_exercise_date = get_earliest_exercise_date(self.acm_obj)
        return earliest_exercise_date

    # formatter
    def _format_earliest_exercise_date_30P(self, val):
        if FSwiftWriterUtils.is_valid(val):
            date_format = '%Y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)
            return val

    # validator
    @validate_with(MT306.MT306_SequenceD_VanillaBlock_30P_Type)
    def _validate_earliest_exercise_date_30P(self, val):
        return val

    def _check_condition_set_earliest_exercise_date_30P(self):
        if self.is_seq_d and get_option_expiration_style(self.acm_obj) == 'AMER':
            return True
        return False

    # setter
    def _set_earliest_exercise_date_30P(self, val):
        self.swift_obj.SequenceD_VanillaBlock.EarliestExerciseDate = val
        self.swift_obj.SequenceD_VanillaBlock.EarliestExerciseDate.swiftTag = "30P"

    # ------------------ settlement_type -----------------------
    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT306.MT306_SequenceD_VanillaBlock_26F_Type)
    def _validate_settlement_type_26F(self, val):
        return val

    def _check_condition_set_settlement_type_26F(self):
        if self.is_seq_d:
            return True
        return False

    # setter
    def _set_settlement_type_26F(self, val):
        self.swift_obj.SequenceD_VanillaBlock.SettlementType = val
        self.swift_obj.SequenceD_VanillaBlock.SettlementType.swiftTag = "26F"

    # ------------------ put_currency_and_amount -----------------------
    # getter
    def put_currency_and_amount_32B(self):
        '''Returns dictionary with keys 'PUT_CURRENCY', 'PUT_AMOUNT' and their corresponding  values'''
        if self.use_operations_xml:
            val_dict = {}
            put_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                    ['SWIFT', 'PUT_CURRENCY'])
            put_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'PUT_AMOUNT'])
            val_dict['PUT_CURRENCY'] = put_currency
            val_dict['PUT_AMOUNT'] = put_amount
        else:
            val_dict = {}
            val_dict['PUT_CURRENCY'] = get_underlying_currency(self.acm_obj)
            val_dict['PUT_AMOUNT'] = get_underlying_amount(self.acm_obj)

        return val_dict

    # formatter
    def _format_put_currency_and_amount_32B(self, val):
        put_currency = val.get('PUT_CURRENCY')
        put_amount = val.get('PUT_AMOUNT')

        if put_currency and put_amount:
            val = put_currency + FSwiftMLUtils.float_to_swiftmt(
                apply_currency_precision(put_currency, float(put_amount)))
            return str(val)

    # validator
    @validate_with(MT306.MT306_SequenceD_VanillaBlock_32B_Type)
    def _validate_put_currency_and_amount_32B(self, val):
        return val

    def _check_condition_set_put_currency_and_amount_32B(self):
        if self.is_seq_d:
            return True
        return False

    # setter
    def _set_put_currency_and_amount_32B(self, val):
        self.swift_obj.SequenceD_VanillaBlock.PutCurrencyAndAmount = val
        self.swift_obj.SequenceD_VanillaBlock.PutCurrencyAndAmount.swiftTag = "32B"

    # ------------------ strike_price -----------------------
    # getter
    # Moved to FXMMOutBase

    # formatter
    def _format_strike_price_36(self, val):
        if FSwiftWriterUtils.is_valid(val):
            val = str(val).replace(".", ',')
            return val

    # validator
    @validate_with(MT306.MT306_SequenceD_VanillaBlock_36_Type)
    def _validate_strike_price_36(self, val):
        return val

    def _check_condition_set_strike_price_36(self):
        if self.is_seq_d:
            return True
        return False

    # setter
    def _set_strike_price_36(self, val):
        self.swift_obj.SequenceD_VanillaBlock.StrikePrice = val
        self.swift_obj.SequenceD_VanillaBlock.StrikePrice.swiftTag = "36"

    # ------------------ call_currency_and_amount -----------------------
    # getter
    def call_currency_and_amount_33B(self):
        '''Returns dictionary with keys 'CALL_CURRENCY', 'CALL_AMOUNT' and their corresponding  values'''
        if self.use_operations_xml:
            val_dict = {}
            call_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'CALL_CURRENCY'])
            call_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                   ['SWIFT', 'CALL_AMOUNT'])
            val_dict['CALL_CURRENCY'] = call_currency
            val_dict['CALL_AMOUNT'] = call_amount
        else:
            val_dict = {}
            val_dict['CALL_CURRENCY'] = get_strike_currency(self.acm_obj)
            val_dict['CALL_AMOUNT'] = get_counter_amount(self.acm_obj)

        return val_dict

    # formatter
    def _format_call_currency_and_amount_33B(self, val):
        call_currency = val.get('CALL_CURRENCY')
        call_amount = val.get('CALL_AMOUNT')
        if call_currency and call_amount:
            val = call_currency + FSwiftMLUtils.float_to_swiftmt(apply_currency_precision(call_currency,
                                                                                          float(call_amount)))
            return str(val)

    # validator
    @validate_with(MT306.MT306_SequenceD_VanillaBlock_33B_Type)
    def _validate_call_currency_and_amount_33B(self, val):
        return val

    def _check_condition_set_call_currency_and_amount_33B(self):
        if self.is_seq_d:
            return True
        return False

    # setter
    def _set_call_currency_and_amount_33B(self, val):
        self.swift_obj.SequenceD_VanillaBlock.CallCurrencyAndAmount = val
        self.swift_obj.SequenceD_VanillaBlock.CallCurrencyAndAmount.swiftTag = "33B"

    # ------------------ payout_currency_amount -----------------------
    # getter
    def payout_currency_amount_33E(self):
        '''Returns dictionary with keys 'PAYOUT_CURRENCY', 'PAYOUT_AMOUNT' and their corresponding  values'''
        if self.use_operations_xml:
            val_dict = {}
            payout_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                       ['SWIFT', 'PAYOUT_CURRENCY'])
            payout_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'PAYOUT_AMOUNT'])
            val_dict['PAYOUT_CURRENCY'] = payout_currency
            val_dict['PAYOUT_AMOUNT'] = payout_amount
        else:
            val_dict = {}
            val_dict['PAYOUT_CURRENCY'] = get_underlying_currency(self.acm_obj)
            val_dict['PAYOUT_AMOUNT'] = get_underlying_amount(self.acm_obj)

        return val_dict

    # formatter
    def _format_payout_currency_amount_33E(self, val):
        payout_currency = val.get('PAYOUT_CURRENCY')
        payout_amount = val.get('PAYOUT_AMOUNT')
        if payout_currency and payout_amount:
            val = payout_currency + FSwiftMLUtils.float_to_swiftmt(
                apply_currency_precision(payout_currency, float(payout_amount)))
            return str(val)

    # validator
    @validate_with(MT306.MT306_SequenceE_PayoutAmount_33E_Type)
    def _validate_payout_currency_amount_33E(self, val):
        return val

    def _check_condition_set_payout_currency_amount_33E(self):
        if self.is_seq_e:
            return True
        return False

    # setter
    def _set_payout_currency_amount_33E(self, val):
        self.swift_obj.SequenceE_PayoutAmount.CurrencyAmount = val
        self.swift_obj.SequenceE_PayoutAmount.CurrencyAmount.swiftTag = "33E"

    # ------------------ receiving_agent_seq_e -----------------------

    # option getter
    def get_receiving_agent_seq_e_option(self):
        """Returns default option if override is not provided"""
        option = 'J'
        return option

    def _check_condition_set_OPTION_receiving_agent_seq_e(self):
        if self.is_seq_e:
            return True
        return False

    # setter
    def _set_OPTION_receiving_agent_seq_e(self):
        '''Returns name of the getter for receiving agent in sequence e like  'receiving_agent_seq_e_57J' '''
        if self.use_operations_xml:
            payout_receiving_agent_option = FSwiftWriterUtils.get_value_from_xml_tag(
                self.swift_metadata_xml_dom, ['SWIFT', 'PAYOUT_RECEIVING_AGENT_OPTION'], ignore_absense=True)
        else:
            payout_receiving_agent_option = self.get_receiving_agent_seq_e_option()
        if payout_receiving_agent_option:
            if payout_receiving_agent_option == "J":
                return "receiving_agent_seq_e_57J"
        else:
            notifier.WARN(
                "%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,
                                                                                       str(
                                                                                           payout_receiving_agent_option),
                                                                                       'PayoutReceivingAgent_57a'))
        return "receiving_agent_seq_e_57J"

    # getter
    def receiving_agent_seq_e_57J(self):
        ''' Returns dictionary with keys 'PAYOUT_RECEIVING_AGENT_BIC', 'PAYOUT_RECEIVING_AGENT_NAME' and their correpsonding values '''
        if self.use_operations_xml:
            val_dict = {}
            payout_receiving_agent_bic = FSwiftWriterUtils.get_value_from_xml_tag(
                self.swift_metadata_xml_dom,
                ['SWIFT', 'PAYOUT_RECEIVING_AGENT_BIC'])
            payout_receiving_agent_name = FSwiftWriterUtils.get_value_from_xml_tag(
                self.swift_metadata_xml_dom,
                ['SWIFT', 'PAYOUT_RECEIVING_AGENT_NAME'], ignore_absense=True)

            val_dict['PAYOUT_RECEIVING_AGENT_BIC'] = payout_receiving_agent_bic
            val_dict['PAYOUT_RECEIVING_AGENT_NAME'] = payout_receiving_agent_name
        else:
            val_dict = {}
            val_dict['PAYOUT_RECEIVING_AGENT_BIC'] = get_payout_receiving_agent_bic(self.acm_obj)
            val_dict['PAYOUT_RECEIVING_AGENT_NAME'] = get_payout_receiving_agent_name(self.acm_obj)
        return val_dict

    # formatter
    def _format_receiving_agent_seq_e_57J(self, val):
        payout_receiving_agent_bic = val.get('PAYOUT_RECEIVING_AGENT_BIC')
        payout_receiving_agent_name = val.get('PAYOUT_RECEIVING_AGENT_NAME')

        val = "/" + "ABIC" + "/" + (payout_receiving_agent_bic or 'UKWN') + \
              "/" + "NAME" + "/" + (payout_receiving_agent_name or 'UNKNOWN')
        lines = FSwiftWriterUtils.split_text_on_character_limit(val, 40)
        val = FSwiftWriterUtils.allocate_space_for_n_lines(5, lines)
        return val

    # validator
    @validate_with(MT306.MT306_SequenceE_PayoutAmount_57J_Type)
    def _validate_receiving_agent_seq_e_57J(self, val):
        return val

    def _check_condition_setreceiving_agent_seq_e_57J(self):
        if self.is_seq_e:
            return True
        return False

    # setter
    def _setreceiving_agent_seq_e_57J(self, val):
        self.swift_obj.SequenceE_PayoutAmount.ReceivingAgent_J = val
        self.swift_obj.SequenceE_PayoutAmount.ReceivingAgent_J.swiftTag = "57J"

    # ------------------ type_of_barrier -----------------------
    # getter
    def type_of_barrier_22G(self):
        '''Returns  barrier type code as string'''
        if self.use_operations_xml:
            type_of_barrier = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                       ['SWIFT', 'TYPE_OF_BARRIER'])
        else:
            type_of_barrier = get_type_of_barrier(self.acm_obj)
        return type_of_barrier

    # formatter
    def _format_type_of_barrier_22G(self, val):
        return val

    # validator
    @validate_with(MT306.MT306_SequenceF_BarrierBlock_22G_Type)
    def _validate_type_of_barrier_22G(self, val):
        return val

    def _check_condition_set_type_of_barrier_22G(self):
        if self.is_seq_f:
            return True
        return False

    # setter
    def _set_type_of_barrier_22G(self, val):
        self.swift_obj.SequenceF_BarrierBlock.TypeOfBarrier = val
        self.swift_obj.SequenceF_BarrierBlock.TypeOfBarrier.swiftTag = "22G"

    # ------------------ barrier_level -----------------------
    # getter
    def barrier_level_37J(self):
        '''Returns barrier level as string '''
        if self.use_operations_xml:
            barrier_level = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'BARRIER_LEVEL'])
        else:
            barrier_level = get_barrier_level(self.acm_obj)
        return barrier_level

    # formatter
    def _format_barrier_level_37J(self, val):
        if str(val):
            val = str(val).replace('.', ',')
            return val

    # validator
    @validate_with(MT306.MT306_SequenceF_BarrierBlock_37J_Type)
    def _validate_barrier_level_37J(self, val):
        return val

    def _check_condition_set_barrier_level_37J(self):
        if self.is_seq_f:
            return True
        return False

    # setter
    def _set_barrier_level_37J(self, val):
        self.swift_obj.SequenceF_BarrierBlock.BarrierLevel = val
        self.swift_obj.SequenceF_BarrierBlock.BarrierLevel.swiftTag = "37J"

    # ------------------ lower_barrier_level -----------------------
    # getter
    def lower_barrier_level_37L(self):
        '''Returns lower barrier level as string '''
        if self.use_operations_xml:
            lower_barrier_level = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'LOWER_BARRIER_LEVEL'],
                                                                           ignore_absense=True)
        else:
            lower_barrier_level = get_lower_barrier_level(self.acm_obj)
        return lower_barrier_level

    # formatter
    def _format_lower_barrier_level_37L(self, val):
        if self.use_operations_xml:
            if FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TYPE_OF_BARRIER'],
                                                        ignore_absense=True) not in ['SKIN', 'SKOT']:
                val = str(val).replace('.', ',')
                return str(val)
        else:
            type_of_barrier = get_type_of_barrier(self.acm_obj)
            if type_of_barrier not in ['SKIN', 'SKOT']:
                val = str(val).replace('.', ',')
                return str(val)

    # validator
    @validate_with(MT306.MT306_SequenceF_BarrierBlock_37L_Type, is_mandatory=True)
    def _validate_lower_barrier_level_37L(self, val):
        return val

    def _check_condition_set_lower_barrier_level_37L(self):
        # According to netwrok rule c15
        barrier_type = self.type_of_barrier_22G()
        if self.is_seq_f and barrier_type not in ['SKIN', 'SKOT']:
            return True
        return False

    # ------------------ barrier_window -----------------------
    # setter
    def _set_lower_barrier_level_37L(self, val):
        self.swift_obj.SequenceF_BarrierBlock.LowerBarrierLevel = val
        self.swift_obj.SequenceF_BarrierBlock.LowerBarrierLevel.swiftTag = "37L"

    # ------------------ barrier_window -----------------------
    def barrier_window(self):
        '''Returns list of dictionaries with  keys 'BARRIER_WINDOW_START_AND_END_DATE', 'LOCATION_TIME_FOR_START_DATE', 'LOCATION_TIME_FOR_END_DATE' and their corresponding values.
           Each dictionary in this list contains data for a barrier window. Each barrier window contains tags 30G, 29J, 29K '''
        barrier_details = []

        if self.use_operations_xml:
            all_windows = FSwiftWriterUtils.get_block_xml_tags(
                self.swift_metadata_xml_dom, 'SequenceF_BarrierBlock',
                ['BARRIER_WIN_START_DATE', 'BARRIER_WIN_END_DATE',
                 'START_DATE_LOCATION', 'START_DATE_TIME',
                 'END_DATE_LOCATION',
                 'END_DATE_TIME'], ignore_absense=True)
        else:
            all_windows = get_barrier_windows(self.acm_obj)

        for window in all_windows:
            val_dict = {}
            val_dict['BARRIER_WINDOW_START_AND_END_DATE'] = self.barrier_window_start_date_end_date_details_30G(window)
            val_dict['LOCATION_TIME_FOR_START_DATE'] = self.barrier_window_location_and_time_for_start_date_29J(window)
            val_dict['LOCATION_TIME_FOR_END_DATE'] = self.barrier_window_location_and_time_for_end_date_29K(window)
            barrier_details.append(val_dict)
        return barrier_details

    def _format_barrier_window(self, val_dict):
        format_val = []
        for each_barrier in val_dict:
            format_dict_val = {}
            format_dict_val[
                'BARRIER_WINDOW_START_AND_END_DATE'] = self._format_barrier_window_start_date_end_date_details_30G(
                each_barrier['BARRIER_WINDOW_START_AND_END_DATE'])
            format_dict_val[
                'LOCATION_TIME_FOR_START_DATE'] = self._format_barrier_window_location_and_time_for_start_date_29J(
                each_barrier['LOCATION_TIME_FOR_START_DATE'])
            format_dict_val[
                'LOCATION_TIME_FOR_END_DATE'] = self._format_barrier_window_location_and_time_for_end_date_29K(
                each_barrier['LOCATION_TIME_FOR_END_DATE'])
            format_val.append(format_dict_val)
        return format_val

    def _validate_barrier_window(self, format_val):
        validated_val = []
        for each_barrier in format_val:
            validate_dict = {}
            val = self._validate_barrier_window_start_date_end_date_details_30G(
                each_barrier['BARRIER_WINDOW_START_AND_END_DATE'])
            validate_dict['BARRIER_WINDOW_START_AND_END_DATE'] = val

            val = self._validate_barrier_window_location_and_time_for_start_date_29J(
                each_barrier['LOCATION_TIME_FOR_START_DATE'])
            validate_dict['LOCATION_TIME_FOR_START_DATE'] = val

            val = self._validate_barrier_window_location_and_time_for_end_date_29K(
                each_barrier['LOCATION_TIME_FOR_END_DATE'])
            validate_dict['LOCATION_TIME_FOR_END_DATE'] = val

            validated_val.append(validate_dict)
        return validated_val

    def _check_condition_set_barrier_window(self):
        if self.is_seq_f:
            if self.use_operations_xml:
                optional_seq_f1 = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'SequenceF_BarrierBlock',
                                                                            'BARRIER_WIN_START_DATE'],
                                                                           ignore_absense=True)
                if optional_seq_f1:
                    return True
            else:
                # According to specs
                # If there is no specific barrier window, Start Date should contain the trade date and End Date should
                # contain the expiration date.
                # Subsequence Barrier Window Block may be repeated in order to define multiple windows during
                # which the barrier or barriers are monitored.

                # This means that in any case there is going to be atleast one barrier window if sequence f is to be mapped
                return True

        return False

    def _set_barrier_window(self, val_dict):
        for each_barrier in val_dict:
            barrier_window = MT306.MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock()
            self._setbarrier_window_start_date_end_date_details_30G(each_barrier['BARRIER_WINDOW_START_AND_END_DATE'],
                                                                    barrier_window)
            self._setbarrier_window_location_and_time_for_start_date_29J(each_barrier['LOCATION_TIME_FOR_START_DATE'],
                                                                         barrier_window)
            self._setbarrier_window_location_and_time_for_end_date_29K(each_barrier['LOCATION_TIME_FOR_END_DATE'],
                                                                       barrier_window)
            self.swift_obj.SequenceF_BarrierBlock.SubsequenceF1_BarrierWindowBlock.append(barrier_window)

    # getter
    def barrier_window_start_date_end_date_details_30G(self, window):
        ''' Returns a dictionary with keys 'BARRIER_WIN_START_DATE', 'BARRIER_WIN_END_DATE' and their corresponding values  '''
        return dict((k, window[k]) for k in window if k in ('BARRIER_WIN_START_DATE', 'BARRIER_WIN_END_DATE'))

    # formatter
    def _format_barrier_window_start_date_end_date_details_30G(self, val):

        barrier_win_start_date = val.get('BARRIER_WIN_START_DATE')
        barrier_win_end_date = val.get('BARRIER_WIN_END_DATE')
        date_format = '%Y%m%d'
        val = FSwiftWriterUtils.format_date(barrier_win_start_date, date_format) + "/" + \
              FSwiftWriterUtils.format_date(barrier_win_end_date, date_format)
        return str(val)

    # validator
    @validate_with(MT306.MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_30G_Type)
    def _validate_barrier_window_start_date_end_date_details_30G(self, val):
        return val

    # setter
    def _setbarrier_window_start_date_end_date_details_30G(self, val, barrier_window):
        barrier_window.BarrierWindowStartDateAndEndDate = val
        barrier_window.BarrierWindowStartDateAndEndDate.swiftTag = "30G"

    # getter
    def barrier_window_location_and_time_for_start_date_29J(self, window):
        ''' Returns a dictionary with keys 'START_DATE_LOCATION', 'START_DATE_TIME' and their corresponding values  '''
        return dict((k, window[k]) for k in window if k in ('START_DATE_LOCATION', 'START_DATE_TIME'))

    # formatter
    def _format_barrier_window_location_and_time_for_start_date_29J(self, val):
        start_date_location = val.get('START_DATE_LOCATION')
        start_date_time = val.get('START_DATE_TIME')
        value = ''
        value = start_date_location
        if start_date_time:
            value += '/' + str(start_date_time)
        return value

    # validator
    @validate_with(MT306.MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_29J_Type)
    def _validate_barrier_window_location_and_time_for_start_date_29J(self, val):
        return val

    # setter
    def _setbarrier_window_location_and_time_for_start_date_29J(self, val, barrier_window):
        barrier_window.LocationAndTimeForStartDate = val
        barrier_window.LocationAndTimeForStartDate.swiftTag = "29J"

    # getter
    def barrier_window_location_and_time_for_end_date_29K(self, window):
        ''' Returns a dictionary with keys 'END_DATE_LOCATION', 'END_DATE_TIME' and their corresponding values  '''
        return dict((k, window[k]) for k in window if k in ('END_DATE_LOCATION', 'END_DATE_TIME'))

    # formatter
    def _format_barrier_window_location_and_time_for_end_date_29K(self, val):
        end_date_location = val.get('END_DATE_LOCATION')
        end_date_time = val.get('END_DATE_TIME')
        if end_date_location and end_date_time:
            val = str(end_date_location) + '/' + str(end_date_time)
            return val

    # validator
    @validate_with(MT306.MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_29K_Type)
    def _validate_barrier_window_location_and_time_for_end_date_29K(self, val):
        return val

    # setter
    def _setbarrier_window_location_and_time_for_end_date_29K(self, val, barrier_window):
        barrier_window.LocationAndTimeForEndDate = val
        barrier_window.LocationAndTimeForEndDate.swiftTag = "29K"

    # ------------------ sequence_g  -----------------------
    # block getter
    def sequence_g(self):
        ''' Returns a list of dictionaries with keys 'TYPE_OF_TRIGGER', 'TRIGGER_LEVEL', 'LOWER_TRIGGER_LEVEL', 'CURRENCY_PAIR' and their corresponding values.
         Each dictionary in this list contains key-values for a trigger block. Each trigger block contains tags  22J, 37U, 37P, 32Q.
         TYPE_OF_TRIGGER -> type of trigger code as string
         TRIGGER_LEVEL -> Barrier level as string
         LOWER_TRIGGER_LEVEL -> lower barrier level as string
         CURRENCY_PAIR -> Currency pair in the form CURR1/CURR2
         '''

        if self.use_operations_xml:
            trigger_blocks = FSwiftWriterUtils.get_repetative_xml_tag_value(self.swift_metadata_xml_dom,
                                                                            tag_names=['TYPE_OF_TRIGGER',
                                                                                       'TRIGGER_LEVEL',
                                                                                       'LOWER_TRIGGER_LEVEL',
                                                                                       'CURRENCY_PAIR'],
                                                                            block_name='SWIFT', ignore_absense=True)
        else:
            trigger_blocks = get_trigger_blocks(self.acm_obj)
        sequence_g_details = []
        for block in trigger_blocks:
            val_dict = {}
            val_dict['TYPE_OF_TRIGGER'] = self.sequence_g_type_of_trigger_22J(block)
            val_dict['TRIGGER_LEVEL'] = self.sequence_g_trigger_level_37U(block)
            if not str(val_dict['TYPE_OF_TRIGGER']) == 'SITR':  # Network Rule C16
                val_dict['LOWER_TRIGGER_LEVEL'] = self.sequence_g_lower_trigger_level_37P(block)
            val_dict['CURRENCY_PAIR'] = self.sequence_g_currency_pair_32Q(block)
            sequence_g_details.append(val_dict)
        return sequence_g_details

    def _format_sequence_g(self, val_list):
        format_val = []
        for each_sequence in val_list:
            format_val_dict = {}
            format_val_dict['TYPE_OF_TRIGGER'] = self._format_sequence_g_type_of_trigger_22J(
                each_sequence['TYPE_OF_TRIGGER'])
            format_val_dict['TRIGGER_LEVEL'] = self._format_sequence_g_trigger_level_37U(each_sequence['TRIGGER_LEVEL'])
            if 'LOWER_TRIGGER_LEVEL' in each_sequence:
                format_val_dict['LOWER_TRIGGER_LEVEL'] = self._format_sequence_g_lower_trigger_level_37P(
                    each_sequence['LOWER_TRIGGER_LEVEL'])
            format_val_dict['CURRENCY_PAIR'] = self._format_sequence_g_currency_pair_32Q(each_sequence['CURRENCY_PAIR'])
            format_val.append(format_val_dict)
        return format_val

    def _validate_sequence_g(self, format_val):
        validated_val = []
        for each_sequence in format_val:
            validate_dict = {}
            val = self._validate_sequence_g_type_of_trigger_22J(each_sequence['TYPE_OF_TRIGGER'])
            validate_dict['TYPE_OF_TRIGGER'] = val
            val = self._validate_sequence_g_trigger_level_37U(each_sequence['TRIGGER_LEVEL'])
            validate_dict['TRIGGER_LEVEL'] = val
            if 'LOWER_TRIGGER_LEVEL' in each_sequence:
                val = self._validate_sequence_g_lower_trigger_level_37P(each_sequence['LOWER_TRIGGER_LEVEL'])
                validate_dict['LOWER_TRIGGER_LEVEL'] = val
            val = self._validate_sequence_g_currency_pair_32Q(each_sequence['CURRENCY_PAIR'])
            validate_dict['CURRENCY_PAIR'] = val
            validated_val.append(validate_dict)
        return validated_val

    def _check_condition_set_sequence_g(self):
        if self.use_operations_xml:
            option_style = self.__get_option_style()
            if option_style in ['BINA', 'DIGI', 'NOTO']:  # Network Rule c9
                optional_seq_g = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'CURRENCY_PAIR'],
                                                                          ignore_absense=True)
                if optional_seq_g:
                    return True
            return False
        else:
            option_style_code = get_option_style_code(self.acm_obj)
            if option_style_code in ['BINA', 'DIGI', 'NOTO']:  # Network Rule c9
                currency_pair = get_currency_pair(self.acm_obj)
                if currency_pair:
                    return True
            return False

    def _set_sequence_g(self, val_dict):
        triggerB = MT306.MT306_SequenceG_TriggerBlock()
        for each_seq in val_dict:
            trigger = MT306.MT306_SequenceG_TriggerBlock_TRIGGER()
            trigger.swiftTag = "15G"
            trigger.formatTag = "False"

            self._setsequence_g_type_of_trigger_22J(each_seq['TYPE_OF_TRIGGER'], trigger)
            self._setsequence_g_trigger_level_37U(each_seq['TRIGGER_LEVEL'], trigger)
            if 'LOWER_TRIGGER_LEVEL' in each_seq:
                self._setsequence_g_lower_trigger_level_37P(each_seq['LOWER_TRIGGER_LEVEL'], trigger)
            self._setsequence_g_currency_pair_32Q(each_seq['CURRENCY_PAIR'], trigger)

            triggerB.TRIGGER = trigger
            self.swift_obj.SequenceG_TriggerBlock.append(triggerB)

    # getter
    def sequence_g_type_of_trigger_22J(self, block):
        type_of_trigger = block['TYPE_OF_TRIGGER']
        return type_of_trigger

    # formatter
    def _format_sequence_g_type_of_trigger_22J(self, val):
        return val

    # validator
    @validate_with(MT306.MT306_SequenceG_TriggerBlock_TRIGGER_22J_Type)
    def _validate_sequence_g_type_of_trigger_22J(self, val):
        return val

    # setter
    def _setsequence_g_type_of_trigger_22J(self, val, trigger):
        trigger.TypeOfTrigger = val
        trigger.TypeOfTrigger.swiftTag = "22J"

    # getter
    def sequence_g_trigger_level_37U(self, block):
        trigger_level = block['TRIGGER_LEVEL']
        return trigger_level

    # formatter
    def _format_sequence_g_trigger_level_37U(self, val):
        if str(val):
            val = str(val).replace('.', ',')
            return val

    # validate
    @validate_with(MT306.MT306_SequenceG_TriggerBlock_TRIGGER_37U_Type)
    def _validate_sequence_g_trigger_level_37U(self, val):
        return val

    # setter
    def _setsequence_g_trigger_level_37U(self, val, trigger):
        trigger.TriggerLevel = val
        trigger.TriggerLevel.swiftTag = "37U"

    # getter
    def sequence_g_lower_trigger_level_37P(self, block):
        return block['LOWER_TRIGGER_LEVEL']

    # formatter
    def _format_sequence_g_lower_trigger_level_37P(self, val):
        val = str(val).replace('.', ',')
        return val

    # validator
    # Network Rule C16
    @validate_with(MT306.MT306_SequenceG_TriggerBlock_TRIGGER_37P_Type, is_mandatory=True)
    def _validate_sequence_g_lower_trigger_level_37P(self, val):
        return val

    # setter
    def _setsequence_g_lower_trigger_level_37P(self, val, trigger):
        trigger.LowerTriggerLevel = val
        trigger.LowerTriggerLevel.swiftTag = "37P"

    # getter
    def sequence_g_currency_pair_32Q(self, block):
        currency_pair = block['CURRENCY_PAIR']
        return currency_pair

    # formatter
    def _format_sequence_g_currency_pair_32Q(self, val):
        return val

    # validator
    @validate_with(MT306.MT306_SequenceG_TriggerBlock_TRIGGER_32Q_Type)
    def _validate_sequence_g_currency_pair_32Q(self, val):
        return val

    # setter
    def _setsequence_g_currency_pair_32Q(self, val, trigger):
        trigger.CurrencyPair = val
        trigger.CurrencyPair.swiftTag = "32Q"

    # ------------------ settlement_rate_source -----------------------
    # block getter
    def sequence_h_settlement_rate_source_14S(self):
        '''Returns settlement rate source  as string'''
        if self.use_operations_xml:
            settlement_rate_source = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                              ['SWIFT', 'SETTLEMENT_RATE_SOURCE'])
        else:
            settlement_rate_source = get_sequence_h_settlement_rate_source(self.acm_obj)
        return settlement_rate_source

    # block formatter
    def _format_sequence_h_settlement_rate_source_14S(self, val):
        return val

    # block validator
    def _validate_sequence_h_settlement_rate_source_14S(self, val):
        validated_val_list = []
        for each in val:
            validated_val = self._validate_sequence_h_settlement_rate_source(each)
            if validated_val:
                validated_val_list.append(validated_val)
        return validated_val_list

    # validator
    @validate_with(MT306.MT306_SequenceH_NonDeliverableOptionBlockOPT_14S_Type)
    def _validate_sequence_h_settlement_rate_source(self, val):
        return val

    def _check_condition_set_sequence_h_settlement_rate_source_14S(self):
        if self.is_seq_h:
            return True
        return False

    # block setter
    def _set_sequence_h_settlement_rate_source_14S(self, val):
        for each in val:
            self.swift_obj.SequenceH_NonDeliverableOptionBlockOPT.SettlementRateSource.append(each)
            self.swift_obj.SequenceH_NonDeliverableOptionBlockOPT.SettlementRateSource[-1].swiftTag = "14S"

    # ------------------ settlement_currency -----------------------
    # getter
    def settlement_currency_32E(self):
        '''Returns premium currency as string'''
        if self.use_operations_xml:
            if self.swift_obj.SequenceH_NonDeliverableOptionBlockOPT:
                settlement_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                               ['SWIFT', 'SETTLEMENT_CURRENCY'])
                return settlement_currency
        else:
            return get_premium_currency(self.acm_obj)

    # formatter
    def _format_settlement_currency_32E(self, val):
        return val

    # validator
    @validate_with(MT306.MT306_SequenceH_NonDeliverableOptionBlockOPT_32E_Type)
    def _validate_settlement_currency_32E(self, val):
        return val

    def _check_condition_set_settlement_currency_32E(self):
        if self.is_seq_h:
            return True
        return False

    # setter
    def _set_settlement_currency_32E(self, val):
        self.swift_obj.SequenceH_NonDeliverableOptionBlockOPT.SettlementCurrency = val
        self.swift_obj.SequenceH_NonDeliverableOptionBlockOPT.SettlementCurrency.swiftTag = "32E"

    def __set_optional_seq_b1(self):
        if self.use_operations_xml:
            optional_seq_b1 = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                       ['SWIFT', 'PREMIUM_CURRENCY'],
                                                                       ignore_absense=True)
            type_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TYPE_EVENT'])
            #  Network Rule C20
            if optional_seq_b1 and type_event not in ['KNIN', 'KNOT', 'TRIG']:
                self.swift_obj.SequenceB_TransactionDetails.SubsequenceB1_PremiumDetails = MT306.MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails()
                return True
            return False
        else:
            premium_currency = get_premium_currency(self.acm_obj)
            type_of_event = get_type_of_event(self.acm_obj)
            #  Network Rule C20
            if premium_currency and type_of_event not in ['KNIN', 'KNOT', 'TRIG']:
                self.swift_obj.SequenceB_TransactionDetails.SubsequenceB1_PremiumDetails = MT306.MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails()
                return True
            return False

    def __set_optional_seq_c(self):
        if self.use_operations_xml:
            optional_seq_c = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'SIP_PARTY_RECEIVING_AGENT_OPTION'],
                                                                      ignore_absense=True)
            type_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TYPE_EVENT'])
            if optional_seq_c and type_event not in ['KNIN', 'KNOT', 'TRIG']:
                self.swift_obj.SequenceC_SettlementInstructionsforPaymentofPremium = MT306.MT306_SequenceC_SettlementInstructionsforPaymentofPremium()
                self.swift_obj.SequenceC_SettlementInstructionsforPaymentofPremium.swiftTag = "15C"
                self.swift_obj.SequenceC_SettlementInstructionsforPaymentofPremium.formatTag = "False"
                return True
            return False
        else:
            # making sure that receiving agent for premium has account since this field is mandatory in seq c
            receiving_agent_account = get_receiving_agent_account_for_sett_instr_for_premium_payment(self.acm_obj)
            type_of_event = get_type_of_event(self.acm_obj)
            #  Network Rule C20
            if receiving_agent_account and type_of_event not in ['KNIN', 'KNOT', 'TRIG']:
                self.swift_obj.SequenceC_SettlementInstructionsforPaymentofPremium = MT306.MT306_SequenceC_SettlementInstructionsforPaymentofPremium()
                self.swift_obj.SequenceC_SettlementInstructionsforPaymentofPremium.swiftTag = "15C"
                self.swift_obj.SequenceC_SettlementInstructionsforPaymentofPremium.formatTag = "False"
                return True
            return False

    def __set_optional_seq_d(self):
        if self.use_operations_xml:
            option_style = self.__get_option_style()
            if option_style in ['AVRF', 'AVRO', 'AVSF', 'AVSO', 'DAVF', 'DAVO', 'VANI']:  # Network Rule c9
                optional_seq_d = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'STRIKE_PRICE'],
                                                                          ignore_absense=True)
                if optional_seq_d:
                    self.swift_obj.SequenceD_VanillaBlock = MT306.MT306_SequenceD_VanillaBlock()
                    self.swift_obj.SequenceD_VanillaBlock.swiftTag = "15D"
                    self.swift_obj.SequenceD_VanillaBlock.formatTag = "False"
                    return True
            return False
        else:
            option_style_code = get_option_style_code(self.acm_obj)
            if option_style_code in ['AVRF', 'AVRO', 'AVSF', 'AVSO', 'DAVF', 'DAVO', 'VANI']:  # Network Rule c9
                # making sure we have strike price because its a mandatory field in sequence D
                strike_price = str(get_strike_price(self.acm_obj))
                if strike_price:
                    self.swift_obj.SequenceD_VanillaBlock = MT306.MT306_SequenceD_VanillaBlock()
                    self.swift_obj.SequenceD_VanillaBlock.swiftTag = "15D"
                    self.swift_obj.SequenceD_VanillaBlock.formatTag = "False"
                    return True
            return False

    def __set_optional_seq_e(self):
        if self.use_operations_xml:
            option_style = self.__get_option_style()
            type_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TYPE_EVENT'],
                                                                  ignore_absense=True)
            # Rule C12
            if not ((option_style == 'NOTO' and type_event == "TRIG") or option_style not in ['BINA', 'DIGI', 'NOTO']):
                optional_seq_e = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'PAYOUT_AMOUNT'],
                                                                          ignore_absense=True)
                if optional_seq_e:
                    self.swift_obj.SequenceE_PayoutAmount = MT306.MT306_SequenceE_PayoutAmount()
                    self.swift_obj.SequenceE_PayoutAmount.swiftTag = "15E"
                    self.swift_obj.SequenceE_PayoutAmount.formatTag = "False"
                return True
            return False
        else:
            option_style_code = get_option_style_code(self.acm_obj)
            type_of_event = get_type_of_event(self.acm_obj)
            # Rule C12
            if not (
                (option_style_code == 'NOTO' and type_of_event == "TRIG") or option_style_code not in ['BINA', 'DIGI',
                                                                                                       'NOTO']):
                # checking for SequenceE_PayoutAmount amount because its a mandatory field in sequence E
                payout_amount = get_underlying_amount(self.acm_obj)
                if payout_amount:
                    self.swift_obj.SequenceE_PayoutAmount = MT306.MT306_SequenceE_PayoutAmount()
                    self.swift_obj.SequenceE_PayoutAmount.swiftTag = "15E"
                    self.swift_obj.SequenceE_PayoutAmount.formatTag = "False"
                return True
            return False

    def __set_optional_seq_f(self):
        if self.use_operations_xml:
            is_seq_f_allowed = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                        ['SWIFT', 'BARRIER_INDICATOR'],
                                                                        ignore_absense=True)
            if is_seq_f_allowed == "Y":  # newtwork rule C14
                optional_seq_f = self.__get_type_of_barrier()
                if not optional_seq_f:
                    optional_seq_f = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                              ['SWIFT', 'TYPE_OF_BARRIER'],
                                                                              ignore_absense=True)
                if optional_seq_f:
                    self.swift_obj.SequenceF_BarrierBlock = MT306.MT306_SequenceF_BarrierBlock()
                    self.swift_obj.SequenceF_BarrierBlock.swiftTag = "15F"
                    self.swift_obj.SequenceF_BarrierBlock.formatTag = "False"
                return True
            return False
        else:
            barrier_indicator = get_barrier_indicator(self.acm_obj)
            if barrier_indicator == "Y":  # newtwork rule C14
                # checking type of barrier because its a mandatory field in sequence f
                type_of_barrier = get_type_of_barrier(self.acm_obj)
                if type_of_barrier:
                    self.swift_obj.SequenceF_BarrierBlock = MT306.MT306_SequenceF_BarrierBlock()
                    self.swift_obj.SequenceF_BarrierBlock.swiftTag = "15F"
                    self.swift_obj.SequenceF_BarrierBlock.formatTag = "False"
                return True
            return False

    def __set_optional_seq_h(self):
        if self.use_operations_xml:
            optional_seq_h = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'SETTLEMENT_CURRENCY'],
                                                                      ignore_absense=True)
            if optional_seq_h and FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT',
                                                                            'NON_DELIVERABLE_INDICATOR']) == 'Y':
                self.swift_obj.SequenceH_NonDeliverableOptionBlockOPT = MT306.MT306_SequenceH_NonDeliverableOptionBlockOPT()
                self.swift_obj.SequenceH_NonDeliverableOptionBlockOPT.swiftTag = "15H"
                self.swift_obj.SequenceH_NonDeliverableOptionBlockOPT.formatTag = "False"
                return True
            return False
        else:
            settlement_currency = get_premium_currency(self.acm_obj)
            ndf_indicator = get_non_deliverable_indicator(self.acm_obj)
            if settlement_currency and ndf_indicator == "Y":
                self.swift_obj.SequenceH_NonDeliverableOptionBlockOPT = MT306.MT306_SequenceH_NonDeliverableOptionBlockOPT()
                self.swift_obj.SequenceH_NonDeliverableOptionBlockOPT.swiftTag = "15H"
                self.swift_obj.SequenceH_NonDeliverableOptionBlockOPT.formatTag = "False"
                return True
            return False

    def __get_option_style(self):
        if not self.__option_style:
            option_style = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                    ['SWIFT', 'OPTION_STYLE'])
            instrument = self.acm_obj.Trade().Instrument()
            payType = instrument.PayType()
            exotic = instrument.Exotic()
            averagePriceType = exotic.AveragePriceType()
            averageStrikeType = exotic.AverageStrikeType()
            if payType == 'Spot' and averagePriceType == 'Average' and averageStrikeType == 'Fix':
                option_style = 'AVRO'
            elif payType == 'Spot' and averagePriceType == 'Float' and averageStrikeType == 'Average':
                option_style = 'AVSO'
            elif payType == 'Spot' and averagePriceType == 'Average' and averageStrikeType == 'Average':
                option_style = 'DAVO'
            elif 'KIKO' in exotic.BarrierOptionType():
                option_style = 'VANI'
            elif not instrument.Digital() and exotic.BarrierOptionType() in ('Double Out', 'Down & Out', 'Up & Out'):
                option_style = 'NOTO'
            elif not instrument.Digital() and exotic.BarrierOptionType() in ['Double In', 'Down & In', 'Up & In']:
                option_style = 'BINA'
            elif instrument.Digital():
                option_style = 'DIGI'
            else:
                option_style = 'VANI'
            self.__option_style = option_style
        return self.__option_style

    def __get_calc_agent_location(self, partyName):
        '''Fetch the location of the CalcAgent'''
        city = acm.FParty[partyName].City()
        return get_location_code(city)

    def __get_type_of_barrier(self):
        '''get the type of barrier for KIKO types'''
        barrier_type = ''
        try:
            exotic = self.acm_obj.Trade().Instrument().Exotic()
            tofbar = exotic.BarrierOptionType()
            if tofbar in ['KIKO Up In Down Out', 'KIKO Down In Up Out']:
                barrier_type = 'KIKO'
            elif tofbar in ['KIKO Up Out Down In', 'KIKO Down Out Up In']:
                barrier_type = 'KOKI'
            else:
                barrier_type = ''
        except Exception as e:
            barrier_type = ''
        return barrier_type


class FMT306OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    """  Set MT 306 message Headers """

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_typ = "306"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT' + self.mt_typ)
        super(FMT306OutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

    def message_type(self):
        return "306"

    def sender_logical_terminal_address(self):
        """ LT code is hardcoded as A for sender"""
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
        """ LT code is hardcoded as X for sender"""
        receivers_bic = ''
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'RECEIVER_BIC'])
        else:
            receivers_bic = get_receivers_bic(self.acm_obj)

        terminal_address = self.logical_terminal_address(receivers_bic, "X")
        return terminal_address

    def input_or_output(self):
        return "I"

    def message_user_reference(self):
        """ MUR is sent in the format FAC-SEQNBR of confirmation-VersionID"""
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['CONFIRMATION', 'SEQNBR'])
        else:
            seqnbr = self.acm_obj.Oid()
        conf_obj = acm.FConfirmation[str(seqnbr)]
        return "{108:%s-%s-%s}" % (get_confirmation_reference_prefix(), seqnbr, get_message_version_number(conf_obj))

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


class FMT306OutBaseNetworkRules(object):
    """ Set network rules for MT306 """

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.acm_obj = acm_obj

    def network_rule_c1(self):
        """ In sequence A, if field 12F consists of the code VANI, at least field 17A or field 17F must contain the
        code Y. Both fields may contain the code Y
        12F         17A         17F
        VANI        N           Y
        VANI        Y           N
        VANI        Y           Y
        """
        if self.swift_message_obj.SequenceA_GeneralInformation.OptionStyle.value() == "VANI" and not (
                    self.swift_message_obj.SequenceA_GeneralInformation.BarrierIndicator.value() or
                    self.swift_message_obj.SequenceA_GeneralInformation.NonDeliverableIndicator.value()):
            return "Field 12F consists of the code VANI, at least field 17A or field 17F must contain the code Y"

    def network_rule_c2(self):
        """
        In sequence A, the presence of field 21 depends on the value of field 22A
        22A         21
        AMND       Mandatory
        CANC       Mandatory
        NEWT       Optional
        """
        if self.swift_message_obj.SequenceA_GeneralInformation.TypeOfOperation.value() in ['AMND', 'CANC'] and \
                self.swift_message_obj.SequenceA_GeneralInformation.RelatedReference and not \
                bool(self.swift_message_obj.SequenceA_GeneralInformation.RelatedReference.value()):
            return 'Field 21 in Sequence A is mandatory if field 22A in Sequence A is equal to either AMND or CANC'

    def network_rule_c3(self):
        """
        In sequence A, the values allowed for field 12E depend on the value of field 12F,
         12F                12E
         BINA               AMER, EURO
         DIGI               EURO
         NOTO               EURO
         Any Other Value    AMER, ASIA, BERM, EURO
        """
        if self.swift_message_obj.SequenceA_GeneralInformation.OptionStyle.value() == 'BINA' and \
                        self.swift_message_obj.SequenceA_GeneralInformation.ExpirationStyle.value() not in ['AMER',
                                                                                                            'EURO']:
            return "Field 12F consists of code BINA then field 12E must be either AMER or EURO"
        elif self.swift_message_obj.SequenceA_GeneralInformation.OptionStyle.value() in ['DIGI', 'NOTO'] \
                and self.swift_message_obj.SequenceA_GeneralInformation.ExpirationStyle.value() != "EURO":
            return "Field 12F consists of code 'DIGI', 'NOTO' then field 12E must be EURO"
        elif self.swift_message_obj.SequenceA_GeneralInformation.ExpirationStyle.value() not in ['AMER', 'ASIA', 'BERM',
                                                                                                 'EURO']:
            return "Field 12F consists other value than BINA, DIGI, NOTO then field 12E must contain either of " \
                   "these 'AMER', 'ASIA', 'BERM', 'EURO'"

    def network_rule_c4(self):
        """
        In sequence A, the allowed values for subfield 1 of field 22K depend on the fields 12F and 17A
        12F                              17A            22K[:4]
        AVRF, AVRO, AVSF, AVSO,
        DAVF, DAVO, VANI                N               CONF, CLST, OTHR

        AVRF, AVRO, AVSF, AVSO,
        DAVF, DAVO, VANI                Y              CONF, CLST, KNIN, KNOT, OTHR

        BINA, DIGI, NOTO                N               CONF, CLST, TRIG, OTHR

        BINA, DIGI, NOTO                Y               CONF, CLST, KNIN, KNOT, TRIG, OTHR
        """
        if self.swift_message_obj.SequenceA_GeneralInformation.OptionStyle.value() in ['AVRF', 'AVRO', 'AVSF', 'AVSO',
                                                                                       'DAVF', 'DAVO', 'VANI']:
            if self.swift_message_obj.SequenceA_GeneralInformation.BarrierIndicator.value() == "N" and \
                            self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value()[:4] not in ['CONF',
                                                                                                                'CLST',
                                                                                                                'OTHR']:
                return "Field 12F is set to 'AVRF', 'AVRO', 'AVSF', 'AVSO', 'DAVF', 'DAVO', 'VANI' and 17A is N then " \
                       "22K must be either of 'CONF', 'CLST', 'OTHR'"
            elif self.swift_message_obj.SequenceA_GeneralInformation.BarrierIndicator.value() == "Y" and \
                            self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value()[:4] not in \
                            ['CONF', 'CLST', 'KNIN', 'KNOT', 'OTHR']:
                return "Field 12F is set to 'AVRF', 'AVRO', 'AVSF', 'AVSO', 'DAVF', 'DAVO', 'VANI' and 17A is Y then " \
                       "22K must be either of 'CONF', 'CLST', 'KNIN', 'KNOT', 'OTHR'"
        elif self.swift_message_obj.SequenceA_GeneralInformation.OptionStyle.value() in ['BINA', 'DIGI', 'NOTO']:
            if self.swift_message_obj.SequenceA_GeneralInformation.BarrierIndicator.value() == "N" and \
                            self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value()[:4] not in ['CONF',
                                                                                                                'CLST',
                                                                                                                'TRIG',
                                                                                                                'OTHR']:
                return "Field 12F is set to 'BINA', 'DIGI', 'NOTO' and 17A is N then 22K must be either of 'CONF'," \
                       "'CLST', 'TRIG', 'OTHR'"
            elif self.swift_message_obj.SequenceA_GeneralInformation.BarrierIndicator.value() == "Y" and \
                            self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value()[:4] not in \
                            ['CONF', 'CLST', 'KNIN', 'KNOT', 'TRIG', 'OTHR']:
                return "Field 12F is set to 'BINA', 'DIGI', 'NOTO' and 17A is Y then 22K must be either of 'CONF'," \
                       "'CLST', 'KNIN', 'KNOT', 'TRIG', 'OTHR'"

    # def network_rule_c5(self):
    #     """
    #     In sequence A, the presence of fields 30U and 29H depends on the value of subfield 1 of field 22K
    #     22K[:4]                  30U                 29H
    #     CONF                 Not allowed            Not allowed
    #     CLST                 Not allowed            Not allowed
    #     Any other value      Mandatory              Optional
    #     """
    #     if self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value()[:4] in ["CONF", "CLST"]:
    #         pass
    #     # TODO: field 30U and 29H are not supported now we cannot implement C5
    #
    # def network_rule_c6(self):
    #     pass
    #     # TODO: Not supported in FA

    def network_rule_c7(self):
        """
        In sequence B, the use of option F for field 30a depends on the value of field 12E in sequence
        12E         30F
        EURO        Mandatory
        Not EURO    Optional
        """
        if self.swift_message_obj.SequenceA_GeneralInformation.ExpirationStyle.value() == "EURO" and self.swift_message_obj.SequenceB_TransactionDetails.FinalSettlementDate_F and not \
                self.swift_message_obj.SequenceB_TransactionDetails.FinalSettlementDate_F.value():
            return "Field 12E is contains EURO then field 30F is mandatory"

    # def network_rule_c8(self):
    #     """
    #
    #     """
    #     if self.swift_message_obj and  self.swift_message_obj.SequenceE_PayoutAmount:
    #         # TODO: Not supported in FA
    #         pass

    def network_rule_c9(self):
        """
        The presence of sequence D and the presence of sequence G depends on the value of field 12F
        12F                             sequence D          sequence G

        AVRF, AVRO, AVSF, AVSO,         Mandatory           Not allowed
        DAVF, DAVO, VANI

        BINA, DIGI, NOTO                Not allowed         Mandatory
        """
        if self.swift_message_obj.SequenceA_GeneralInformation.OptionStyle.value() in ['AVRF', 'AVRO', 'AVSF', 'AVSO',
                                                                                       'DAVF', 'DAVO', 'VANI'] \
                and (
                    not self.swift_message_obj.SequenceD_VanillaBlock or self.swift_message_obj.SequenceG_TriggerBlock):
            return "Field 12F is set to either of 'AVRF', 'AVRO', 'AVSF', 'AVSO', 'DAVF', 'DAVO', 'VANI' then " \
                   "sequence D is mandatory and sequence G is not allowed "
        elif self.swift_message_obj.SequenceA_GeneralInformation.OptionStyle.value() in ['BINA', 'DIGI', 'NOTO'] and \
                (self.swift_message_obj.SequenceD_VanillaBlock or not self.swift_message_obj.SequenceG_TriggerBlock):
            return "Field 12F is set to either of 'BINA', 'DIGI', 'NOTO' then sequence D is  not allowed and sequence" \
                   " G is mandatory "

    def network_rule_c10(self):
        """
        In sequence D, if present, the presence of field 30P and the presence of field 30Q depends on the value of
        field 12E.
        12E                  30P                        30Q
        AMER                 Mandatory                  Not allowed
        BERM                 Not allowed                Mandatory (that is, at least one occurrence must be present)
        Any other value      Not allowed                Not allowed
        """
        # TODO: Field 30Q is not supported in FA so implemented partially.
        if self.swift_message_obj.SequenceA_GeneralInformation.OptionStyle.value() == 'AMER' and not self.swift_message_obj.SequenceD_VanillaBlock and \
                self.swift_message_obj.SequenceD_VanillaBlock.EarliestExerciseDate and \
                self.swift_message_obj.SequenceD_VanillaBlock.EarliestExerciseDate.value():
            return "Field 12E is contains AMER then Field 30P is Mandatory"
        elif self.swift_message_obj.SequenceA_GeneralInformation.OptionStyle.value() not in [
            'AMER'] and self.swift_message_obj.SequenceD_VanillaBlock and \
                self.swift_message_obj.SequenceD_VanillaBlock.EarliestExerciseDate and \
                self.swift_message_obj.SequenceD_VanillaBlock.EarliestExerciseDate.value():
            return "Field 12E is contains any value other than AMER then Field 30P is Not allowed"

    def network_rule_c11(self):
        """
        In sequence D, if present, the allowed values for field 26F depend on the value of field 17F in sequence A
        17F             26F
        Y               NETCASH
        N               NETCASH, PRINCIPAL
        """
        if self.swift_message_obj.SequenceD_VanillaBlock:
            if self.swift_message_obj.SequenceA_GeneralInformation.NonDeliverableIndicator.value() == "Y" and self.swift_message_obj.SequenceD_VanillaBlock. \
                    SettlementType.value() != "NETCASH":
                return "Field 17F contains value Y then 17F in sequence D must contain NETCASH"
            elif self.swift_message_obj.SequenceA_GeneralInformation.NonDeliverableIndicator.value() == "N" and \
                            self.swift_message_obj.SequenceD_VanillaBlock.SettlementType.value() not in ["NETCASH",
                                                                                                         'PRINCIPAL']:
                return "Field 17F contains value N then 17F in sequence D must contain NETCASH or PRINCIPAL"

    def network_rule_c12(self):
        """
        The presence of sequence E depends on the values of field 12F and subfield 1 of field 22K in sequence A
        12F                     22K[:4]             Sequence E
        BINA or DIGI            Any value           Mandatory
        NOTO                    Not TRIG            Mandatory
        NOTO                    TRIG                Not allowed
        Any Other Value         Any value           Not allowed
        """
        if self.swift_message_obj.SequenceA_GeneralInformation.OptionStyle.value() in ['BINA', 'DIGI'] and \
                not self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value()[:4] and \
                not self.swift_message_obj.SequenceE_PayoutAmount and \
                not self.swift_message_obj.SequenceE_PayoutAmount.CurrencyAmount:
            return "Field 12F is in BINA or DIGI and 22K part 1 is any value then sequence E is mandatory"
        elif self.swift_message_obj.SequenceA_GeneralInformation.OptionStyle.value() == "NOTO":
            if self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value()[:4] != "TRIG" and \
                    not self.swift_message_obj.SequenceE_PayoutAmount and \
                    not self.swift_message_obj.SequenceE_PayoutAmount.CurrencyAmount:
                return "Field 12F is NOTO and 22K part 1 is not TRIG then sequence E is mandatory"
            elif self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value()[:4] == "TRIG" and \
                    self.swift_message_obj.SequenceE_PayoutAmount and self.swift_message_obj.SequenceE_PayoutAmount.CurrencyAmount:
                return "Field 12F is NOTO and 22K part 1 is TRIG then sequence E is not allowed"
        elif self.swift_message_obj.SequenceA_GeneralInformation.OptionStyle.value() not in ['BINA', 'DIGI', 'NOTO'] and \
                self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value()[:4] and \
                self.swift_message_obj.SequenceE_PayoutAmount and self.swift_message_obj.SequenceE_PayoutAmount.CurrencyAmount:
            return "Field 12F is not in BINA, NOTO, DIGI and 22K part 1 is Any value then sequence E is not allowed"

    # def network_rule_c13(self):
    #     """
    #     In sequence E, if present, the presence of field 30H depends on the value of subfield 1 of field 22K and on
    #      field 12E in sequence A
    #
    #     """
    #     # TODO: Field 30H is not supported in FA can not implement this rule now
    #     pass

    def network_rule_c14(self):
        """
        The presence of sequence F depends on the value of field 17A in sequence A
        17A         Sequence F
        Y           Mandatory
        N           Not allowed
        """
        if self.swift_message_obj.SequenceA_GeneralInformation.BarrierIndicator == "Y" and not self.swift_obj.SequenceF_BarrierBlock:
            return "Field 17A consist value Y then sequence F is mandatory"
        elif self.swift_message_obj.SequenceA_GeneralInformation.BarrierIndicator == "N" and self.swift_obj.SequenceF_BarrierBlock:
            return "Field 17A consist value N then sequence F is not allowed"

    def network_rule_c15(self):
        """
        In sequence F (if present), the presence of field 37L depends on the value of field 22G
        22G             37L
        SKIN            Not allowed
        SKOT            Not allowed
        DKIN            Mandatory
        DKOT            Mandatory
        KIKO            Mandatory
        KOKI            Mandatory
        """
        if self.swift_message_obj.SequenceF_BarrierBlock and self.swift_message_obj.SequenceF_BarrierBlock.TypeOfBarrier:
            if self.swift_message_obj.SequenceF_BarrierBlock.TypeOfBarrier.value() == "SKIN" \
                    and self.swift_message_obj.SequenceF_BarrierBlock.LowerBarrierLevel \
                    and self.swift_message_obj.SequenceF_BarrierBlock.LowerBarrierLevel.value():
                return "Field 22G consists value SKIN then 37L is not allowed"

            elif self.swift_message_obj.SequenceF_BarrierBlock.TypeOfBarrier.value() == "SKOT" \
                    and self.swift_message_obj.SequenceF_BarrierBlock.LowerBarrierLevel \
                    and self.swift_message_obj.SequenceF_BarrierBlock.LowerBarrierLevel.value():
                return "Field 22G consists value SKOT then 37L is not allowed"

            elif self.swift_message_obj.SequenceF_BarrierBlock.TypeOfBarrier.value() == "DKIN" \
                    and not self.swift_message_obj.SequenceF_BarrierBlock.LowerBarrierLevel \
                    and not self.swift_message_obj.SequenceF_BarrierBlock.LowerBarrierLevel.value():
                return "Field 22G consists value DKIN then 37L is Mandatory"

            elif self.swift_message_obj.SequenceF_BarrierBlock.TypeOfBarrier.value() == "DKOT" \
                    and not self.swift_message_obj.SequenceF_BarrierBlock.LowerBarrierLevel \
                    and not self.swift_message_obj.SequenceF_BarrierBlock.LowerBarrierLevel.value():
                return "Field 22G consists value DKOT then 37L is Mandatory"

            elif self.swift_message_obj.SequenceF_BarrierBlock.TypeOfBarrier.value() == "KIKO" \
                    and not self.swift_message_obj.SequenceF_BarrierBlock.LowerBarrierLevel \
                    and not self.swift_message_obj.SequenceF_BarrierBlock.LowerBarrierLevel.value():
                return "Field 22G consists value KIKO then 37L is Mandatory"

            elif self.swift_message_obj.SequenceF_BarrierBlock.TypeOfBarrier.value() == "KOKI" \
                    and not self.swift_message_obj.SequenceF_BarrierBlock.LowerBarrierLevel \
                    and not self.swift_message_obj.SequenceF_BarrierBlock.LowerBarrierLevel.value():
                return "Field 22G consists value KOKI then 37L is Mandatory"

    def network_rule_c16(self):
        """
        In each occurrence of sequence G (if present), the presence of field 37P depends on the value of field 22J
        22J             37P
        SITR            Not allowed
        DBTR            Mandatory
        """
        for trig in self.swift_message_obj.SequenceG_TriggerBlock:
            if trig.TRIGGER.TypeOfTrigger:
                if trig.TRIGGER.TypeOfTrigger.value() == "SITR" and trig.TRIGGER.LowerTriggerLevel and \
                        trig.TRIGGER.LowerTriggerLevel.value():
                    return "Field 22J consists of value SITR then Field 37P is not allowed"
                elif trig.TRIGGER.TypeOfTrigger.value() == "DBTR" and not trig.TRIGGER.LowerTriggerLevel and not \
                        trig.TRIGGER.LowerTriggerLevel.value():
                    return "Field 22J consists of value DBTR then Field 37P is Mandatory"

    def network_rule_c17(self):
        """
        The presence of sequence H depends on the value of field 17F in sequence A
        17F             sequence H
        Y               Mandatory
        N               Not allowed
        """
        if self.swift_message_obj.SequenceA_GeneralInformation.NonDeliverableIndicator.value() == "Y" and not self.swift_message_obj.SequenceH_NonDeliverableOptionBlockOPT:
            return "Feild 17F is set to Y then Sequence H is mandatory"
        elif self.swift_message_obj.SequenceA_GeneralInformation.NonDeliverableIndicator.value() == "N" and self.swift_message_obj.SequenceH_NonDeliverableOptionBlockOPT:
            return "Feild 17F is set to N then Sequence H is Not allowed"

    # def network_rule_c18(self):
    #     """
    #     """
    #     # TODO: sequence 15K and field 88a, 71F are not supported in FA
    #     pass
    #
    # def network_rule_c19(self):
    #     """
    #     """
    #     # TODO: sequence 15K is supported in FA

    def network_rule_c20(self):
        """
        The presence of subsequence B1 and of sequence C depends on the values of subfield 1 of field 22K
        22K[:4]             subsequence B1          sequence C
        CLST                Optional                Optional
        CONF                Mandatory               Mandatory
        KNIN                Not allowed             Not allowed
        KNOT                Not allowed             Not allowed
        OTHR                Optional                Optional
        TRIG                Not allowed             Not allowed
        """
        if self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value()[:4] == "CONF" and not \
                self.swift_message_obj.SequenceB_TransactionDetails and not self.swift_message_obj.SequenceB_TransactionDetails.PremiumPaymentDate and not \
                self.swift_message_obj.SequenceE_PayoutAmount:
            return "Field 22K part 1 consists of CONF then subsequence B1 and Sequene C is mandatory"

        elif self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value()[:4] in ['KNIN', 'KNOT', 'TRIG'] and \
                self.swift_message_obj.SequenceB_TransactionDetails and self.swift_message_obj.SequenceB_TransactionDetails.PremiumPaymentDate and \
                self.swift_message_obj.SequenceE_PayoutAmount:
            return "Field 22K part 1 consists of KNIN, KNOT, TRIG then subsequence B1 and Sequene C is Not Allowed"

            # For Optional no handling is required. OTHR and CLST

            # def network_rule_c21(self):
            #     """
            #     In all optional sequences and sub-sequences, the fields with status M must be present if the sequence or
            #     sub-sequence is present,
            #     """
            #     # This rule is taken care at XSD level NO handling is required here.
            #     pass
            #
            # def network_rule_c22(self):
            #     """
            #     In sequence M, when field 17Z is "Y" then 22Q must be present
            #     """
            #     # TODO: Field 17Z and 22Q is not supported in FA
            #     pass
            #
            # def network_rule_c23(self):
            #     """
            #     In sequence I , if field 12G contains the code BERM then fields 30T and 22Y must be present
            #     """
            #     # TODO: Sequence I is not supported in FA
            #     pass
            #
            # def network_rule_c24(self):
            #     """
            #     In sequence I, if field 12G contains the code AMER then in field 30Y must be present
            #     """
            #     # TODO: Sequence I is not supported in FA
            #     pass
            #
            # def network_rule_c25(self):
            #     """
            #     The presence of sequence J, subsequence J1, subsequence J2 and field 14B in sequence J depends on the code in
            #     field 12F in sequence A
            #     """
            #     # TODO: Sequence J is not supported in FA
            #     pass




