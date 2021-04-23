"""----------------------------------------------------------------------------
MODULE:
    FMT300OutBase

DESCRIPTION:
    This module provides the base class for the FMT300 outgoing implementation

CLASS:
    FMT300Base

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""

import FSwiftMLUtils
import FSwiftWriterMessageHeader
import MT300
import acm
from FSwiftWriterEngine import validate_with, should_use_operations_xml

import FSwiftWriterLogger
import FSwiftWriterUtils
from FFXMMConfirmationOutUtils import *
from FFXMMOutBase import FFXMMOutBase
import FSwiftConfirmationUtils

notifier = FSwiftWriterLogger.FSwiftWriterLogger('FXMMConfOut', 'FFXMMConfirmationOutNotify_Config')

class FMT300Base(FFXMMOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = "MT300"
        super(FMT300Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)
        self.init_NDF()

    def _message_sequences(self):
        self.swift_obj.SequenceA_GeneralInformation = MT300.MT300_SequenceA_GeneralInformation()
        self.swift_obj.SequenceA_GeneralInformation.swiftTag = "15A"
        self.swift_obj.SequenceA_GeneralInformation.formatTag = "False"

        self.swift_obj.SequenceB_TransactionDetails = MT300.MT300_SequenceB_TransactionDetails()
        self.swift_obj.SequenceB_TransactionDetails.swiftTag = "15B"
        self.swift_obj.SequenceB_TransactionDetails.formatTag = "False"

        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought = MT300.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought()
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold = MT300.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold()

        if self.use_operations_xml:
            counterpartys_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                               ['SWIFT', 'COUNTERPARTYS_REFERENCE'],
                                                                               ignore_absense=True)
        else:
            counterpartys_reference = self.acm_obj.Trade().YourRef()

        if counterpartys_reference:
            self.swift_obj.SequenceC_OptionalGeneralInformation = MT300.MT300_SequenceC_OptionalGeneralInformation()
            self.swift_obj.SequenceC_OptionalGeneralInformation.swiftTag = "15C"
            self.swift_obj.SequenceC_OptionalGeneralInformation.formatTag = "False"

    def init_NDF(self):
        self.simulated_closing_NDF_settlement = None
        self.is_confirmation_closing_NDF = False


        if self.acm_obj.Trade().Instrument().IsKindOf(acm.FFuture):
            if self.acm_obj.EventType() in [EventType.NEW_TRADE_AMENDMENT, EventType.NEW_TRADE, EventType.NEW_TRADE_CANCELLATION]:
                openingTrade = self.acm_obj.Trade()
                closing_trade = acm.TradeActions.CloseTrade(openingTrade, openingTrade.AcquireDay(),
                                                          openingTrade.ValueDay(), openingTrade.Nominal(),
                                                          openingTrade.Premium(), openingTrade.Payments())
                closing_settlement = closing_trade.GenerateSettlements(None, None)
                if closing_settlement:
                    self.simulated_closing_NDF_settlement = closing_settlement[0]
            elif self.acm_obj.EventType() == "Close":
                self.is_confirmation_closing_NDF = True

    def get_NDF_buy_sell_currency(self, buy):
        curr = None
        curr_pair = self.acm_obj.Trade().CurrencyPair()
        is_sett_curr_same_as_first_curr = self.acm_obj.Trade().Instrument().Currency().Name() == curr_pair.Currency1().Name()
        if buy == True:
            if is_sett_curr_same_as_first_curr:
                if self.acm_obj.Trade().Sold():
                    curr = curr_pair.Currency1()
                else:
                    curr = curr_pair.Currency2()
            else:
                if self.acm_obj.Trade().Sold():
                    curr = curr_pair.Currency2()
                else:
                    curr = curr_pair.Currency1()
        else:
            if is_sett_curr_same_as_first_curr:
                if self.acm_obj.Trade().Sold():
                    curr = curr_pair.Currency2()
                else:
                    curr = curr_pair.Currency1()
            else:
                if self.acm_obj.Trade().Sold():
                    curr = curr_pair.Currency1()
                else:
                    curr = curr_pair.Currency2()
        if curr:
            return curr.Name()

    def get_acquirer_receiving_agent_details_NDF(self):
        values_dict = {}
        wrapper_obj = None
        if self.simulated_closing_NDF_settlement:
            import FMTSettlementWrapper
            wrapper_obj = FMTSettlementWrapper.FMTSettlementWrapper(self.simulated_closing_NDF_settlement)
        else:
            wrapper_obj = FMTConfirmationWrapper(self.acm_obj)

        money_flow = wrapper_obj.sell_money_flow()
        # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
        if not money_flow:
            money_flow = wrapper_obj.buy_money_flow()
        if money_flow:
            party = money_flow.AcquirerAccount().CorrespondentBank()
            party_account = money_flow.AcquirerAccount()
            values_dict = get_party_details(party, party_account, "CORRESPONDENT")

        return values_dict

    def get_counterparty_receiving_agent_details_NDF(self):
        values_dict = {}
        wrapper_obj = None
        if self.simulated_closing_NDF_settlement:
            import FMTSettlementWrapper
            wrapper_obj = FMTSettlementWrapper.FMTSettlementWrapper(self.simulated_closing_NDF_settlement)
        else:
            wrapper_obj = FMTConfirmationWrapper(self.acm_obj)

        money_flow = wrapper_obj.sell_money_flow()
        # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
        if not money_flow:
            money_flow = wrapper_obj.buy_money_flow()
        if money_flow:
            party = money_flow.CounterpartyAccount().CorrespondentBank()
            party_account = money_flow.CounterpartyAccount()
            values_dict = get_party_details(party, party_account, "CORRESPONDENT")

        return values_dict



    # ------------------ senders_reference -----------------------
    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    @validate_with(MT300.MT300_SequenceA_GeneralInformation_20_Type)
    def _validate_senders_reference_20(self, val):
        validate_slash_and_double_slash(val, "Sender's Reference")
        return val

    # setter
    def _set_senders_reference_20(self, val):
        self.swift_obj.SequenceA_GeneralInformation.SendersReference = val
        self.swift_obj.SequenceA_GeneralInformation.SendersReference.swiftTag = "20"


    # ------------------ related_reference -----------------------
    # Getter
    def related_reference_21(self):
        """Returns Confirmation Object. If the trade is a NDF closing, return the field 20 of parent confirmation"""
        related_ref = ''
        if get_type_of_operation(self.acm_obj) in ['AMND', 'CANC']:
            related_ref = super(FMT300Base, self).related_reference_21()
        return related_ref

    # formatter
    def _format_related_reference_21(self, val):
        formatted_value = ''
        if get_type_of_operation(self.acm_obj) in ['AMND', 'CANC']:
            formatted_value = super(FMT300Base, self)._format_related_reference_21(val)
        return formatted_value

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_21_Type, is_mandatory=True)
    def _validate_related_reference_21(self, val):
        validate_slash_and_double_slash(val, "Related Reference")
        return val

    def _check_condition_set_related_reference_21(self):
        rel_ref_cond = False
        if get_type_of_operation(self.acm_obj) in ['AMND', 'CANC']:
            rel_ref_cond  = True
        return rel_ref_cond

    # setter
    def _set_related_reference_21(self, val):
        self.swift_obj.SequenceA_GeneralInformation.RelatedReference = val
        self.swift_obj.SequenceA_GeneralInformation.RelatedReference.swiftTag = "21"

    # ------------------ related_reference -----------------------
    # Getter
    def reference_to_opening_confirmation_21A(self):
        """Returns Confirmation Object. If the trade is a NDF closing, return the field 20 of parent confirmation"""
        related_ref = ''
        original_trade = self.acm_obj.Trade().ContractTrade()
        for conf in original_trade.Confirmations():
            swift_message = FSwiftMLUtils.get_outgoing_mt_message(conf)
            if swift_message:
                swift_msg_list = FSwiftMLUtils.swift_message_to_list(swift_message)
                for tag_list in swift_msg_list:
                    if tag_list[0] == '20':
                        related_ref = tag_list[1]
                        break
        return related_ref

    # formatter
    def _format_reference_to_opening_confirmation_21A(self, val):
        return val

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_21A_Type_Pattern)
    def _validate_reference_to_opening_confirmation_21A(self, val):
        validate_slash_and_double_slash(val, "Related Reference")
        return val

    def _check_condition_set_reference_to_opening_confirmation_21A(self):
        rel_ref_cond = False
        if self.is_confirmation_closing_NDF:
            rel_ref_cond = True

        return rel_ref_cond

    # setter
    def _set_reference_to_opening_confirmation_21A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.ReferenceToOpeningConfirmation = val
        self.swift_obj.SequenceA_GeneralInformation.ReferenceToOpeningConfirmation.swiftTag = "21A"

    # ------------------ type_of_operation -----------------------
    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_22A_Type)
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
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_94A_Type)
    def _validate_scope_of_operation_94A(self, val):
        return val

    # setter
    def _set_scope_of_operation_94A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.ScopeOfOperation = val
        self.swift_obj.SequenceA_GeneralInformation.ScopeOfOperation.swiftTag = "94A"

    # ------------------ common_reference -----------------------
    # getter
    def common_reference_22C(self):
        '''Returns  dictionary with keys 'SENDERS_BIC', 'RECEIVERS_BIC', 'EXCHANGE_RATE' and their corresponding values  '''
        if self.use_operations_xml:
            val_dict = {}
            senders_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SENDER_BIC'])
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'RECEIVER_BIC'])
            exchange_rate = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'EXCHANGE_RATE'])
        else:
            val_dict = {}
            senders_bic = get_senders_bic(self.acm_obj)
            receivers_bic = get_receivers_bic(self.acm_obj)
            exchange_rate = get_exchange_rate(self.acm_obj)

        val_dict['SENDERS_BIC'] = str(senders_bic)
        val_dict['RECEIVERS_BIC'] = str(receivers_bic)
        val_dict['EXCHANGE_RATE'] = str(exchange_rate)

        return val_dict

    # formatter
    def _format_common_reference_22C(self, val):
        senders_bic = val.get('SENDERS_BIC')
        receivers_bic = val.get('RECEIVERS_BIC')
        exchange_rate = val.get('EXCHANGE_RATE')

        exchange_rate_part = represent_amount_in_four_digits(exchange_rate)
        if senders_bic and receivers_bic and exchange_rate_part:
            if receivers_bic[0:4] + receivers_bic[-2:] > senders_bic[0:4] + senders_bic[-2:]:
                val = senders_bic[0:4] + senders_bic[
                                         -2:] + exchange_rate_part + receivers_bic[
                                                                     0:4] + receivers_bic[
                                                                            -2:]
            else:
                val = receivers_bic[0:4] + receivers_bic[
                                           -2:] + exchange_rate_part + senders_bic[
                                                                       0:4] + senders_bic[
                                                                              -2:]
            return str(val)

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_22C_Type)
    def _validate_common_reference_22C(self, val):
        return val

    # setter
    def _set_common_reference_22C(self, val):
        self.swift_obj.SequenceA_GeneralInformation.CommonReference = val
        self.swift_obj.SequenceA_GeneralInformation.CommonReference.swiftTag = "22C"

        # ------------------ block_trade_indicator -----------------------

    # getter
    def block_trade_indicator_17T(self):
        '''Returns 'Y' or 'N' '''
        block_trade_indicator_val = None
        if self.use_operations_xml:
            block_trade_indicator = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                             ['SWIFT', 'BLOCK_TRADE'],
                                                                             ignore_absense=True)
        else:
            if self.is_confirmation_closing_NDF or self.simulated_closing_NDF_settlement:
                block_trade_indicator_val = None
            else:
                block_trade_indicator_val = get_block_trade_indicator_for(self.acm_obj)
        return block_trade_indicator_val

    # formatter
    def _format_block_trade_indicator_17T(self, val):
        return val

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_17T_Type)
    def _validate_block_trade_indicator_17T(self, val):
        return val

    # setter
    def _set_block_trade_indicator_17T(self, val):
        self.swift_obj.SequenceA_GeneralInformation.BlockTradeIndicator = val
        self.swift_obj.SequenceA_GeneralInformation.BlockTradeIndicator.swiftTag = "17T"

        # ------------------ split_settlement_indicator -----------------------

    # getter
    def split_settlement_indicator_17U(self):
        '''Returns 'Y' or 'N' '''
        split_settlement_indicator = None
        if self.use_operations_xml:
            split_settlement_indicator = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                  ['SWIFT',
                                                                                   'SPLIT_SETTLEMENT_INDICATOR'],
                                                                                  ignore_absense=True)
        else:
            if self.is_confirmation_closing_NDF or self.simulated_closing_NDF_settlement:
                split_settlement_indicator = None
            else:
                split_settlement_indicator = get_split_settlement_indicator_for(self.acm_obj)
        return split_settlement_indicator

    # formatter
    def _format_split_settlement_indicator_17U(self, val):
        return val

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_17U_Type)
    def _validate_split_settlement_indicator_17U(self, val):
        return val

    # setter
    def _set_split_settlement_indicator_17U(self, val):
        self.swift_obj.SequenceA_GeneralInformation.SplitSettlementIndicator = val
        self.swift_obj.SequenceA_GeneralInformation.SplitSettlementIndicator.swiftTag = "17U"

    # ------------------ party_A -----------------------
    #option getter
    def get_partyA_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option


    # setter
    def _set_OPTION_partyA(self):
        if self.use_operations_xml:
            party_A_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'PARTY_A_OPTION'])
        else:
            party_A_option = self.get_partyA_option()

        if party_A_option == "A":
            return 'partyA_82A'
        elif party_A_option == "J":
            return 'partyA_82J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % (str(party_A_option), 'PartyA_82a'))
        return 'partyA_82A'

    # getter
    def partyA_82A(self):
        party_details = {}
        if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
            values_dict = {}
            wrapper_obj = None
            if self.simulated_closing_NDF_settlement:
                import FMTSettlementWrapper
                wrapper_obj = FMTSettlementWrapper.FMTSettlementWrapper(self.simulated_closing_NDF_settlement)
            else:
                wrapper_obj = FMTConfirmationWrapper(self.acm_obj)

            money_flow = wrapper_obj.sell_money_flow()
            # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
            if not money_flow:
                money_flow = wrapper_obj.buy_money_flow()
            if money_flow:
                party = money_flow.Acquirer()
                party_account = money_flow.AcquirerAccount()
                party_details = get_party_details(party, party_account)
        else:
            party_details = super(FMT300Base, self).partyA_82A()

        return party_details

    # formatter
    def _format_partyA_82A(self, val):
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            return val

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_82A_Type)
    def _validate_partyA_82A(self, val):
        return val

    def _setpartyA_82A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.PartyA_A = val
        self.swift_obj.SequenceA_GeneralInformation.PartyA_A.swiftTag = "82A"

    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_82J_Type)
    def _validate_partyA_82J(self, val):
        return val

    # setter
    def _setpartyA_82J(self, val):
        self.swift_obj.SequenceA_GeneralInformation.PartyA_J = val
        self.swift_obj.SequenceA_GeneralInformation.PartyA_J.swiftTag = "82J"

    # ------------------ party_B -----------------------
    # option getter
    def get_partyB_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_partyB(self):
        if self.use_operations_xml:
            party_B_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'PARTY_B_OPTION'])
        else:
            party_B_option = self.get_partyB_option()
        if party_B_option == "A":
            return 'partyB_87A'
        elif party_B_option == "J":
            return 'partyB_87J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % (str(party_B_option), 'PartyB_87a'))
        return 'partyB_87A'

    # getter
    def partyB_87A(self):
        party_details = {}
        if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
            values_dict = {}
            wrapper_obj = None
            if self.simulated_closing_NDF_settlement:
                import FMTSettlementWrapper
                wrapper_obj = FMTSettlementWrapper.FMTSettlementWrapper(self.simulated_closing_NDF_settlement)
            else:
                wrapper_obj = FMTConfirmationWrapper(self.acm_obj)

            money_flow = wrapper_obj.sell_money_flow()
            # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
            if not money_flow:
                money_flow = wrapper_obj.buy_money_flow()
            if money_flow:
                party = money_flow.Counterparty()
                party_account = money_flow.CounterpartyAccount()
                party_details = get_party_details(party, party_account)
        else:
            party_details = super(FMT300Base, self).partyB_87A()

        return party_details

    # formatter
    def _format_partyB_87A(self, val):
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            return val

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_87A_Type)
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
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_87J_Type)
    def _validate_partyB_87J(self, val):
        return val

    # setter
    def _setpartyB_87J(self, val):
        self.swift_obj.SequenceA_GeneralInformation.PartyB_J = val
        self.swift_obj.SequenceA_GeneralInformation.PartyB_J.swiftTag = "87J"

    # ------------------ terms_and_conditions -----------------------
    # getter
    def terms_and_conditions_77D(self):
        '''Returns terms and conditions as string'''
        if self.use_operations_xml:
            terms_and_conditions = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                            ['SWIFT', 'TERMS_CONDITIONS'],
                                                                            ignore_absense=True)
        else:
            terms_and_conditions = ''
            trade = self.acm_obj.Trade()
            doc_type = trade.DocumentType()
            if doc_type:
                agreement = self.acm_obj.AgreementFromDocument(doc_type)
                if agreement and agreement.Dated():
                    terms_and_conditions = trade.DocumentType().Name() + ' AS PER ' + agreement.Dated()
        return terms_and_conditions

    # formatter
    def _format_terms_and_conditions_77D(self, val):
        lines = FSwiftWriterUtils.split_text_on_character_limit(val, 35)
        val = FSwiftWriterUtils.allocate_space_for_n_lines(6, lines)
        return val

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_77D_Type)
    def _validate_terms_and_conditions_77D(self, val):
        validate_terms_and_conditions(val, "Terms And Conditions", codes_not_allowed=['VALD', 'SETC', 'SRCE'])
        return val

    # setter
    def _set_terms_and_conditions_77D(self, val):
        self.swift_obj.SequenceA_GeneralInformation.TermsAndConditions = val
        self.swift_obj.SequenceA_GeneralInformation.TermsAndConditions.swiftTag = "77D"

    # ------------------ non_deliverable_indicator -----------------------
    # getter
    def non_deliverable_indicator_17F(self):
        '''Returns terms and conditions as string'''
        non_deliverable_indicator = None
        trade = self.acm_obj.Trade()
        if trade:
            ins = trade.Instrument()
            if ins and ins.IsKindOf(acm.FFuture):
                non_deliverable_indicator = 'Y'
        return non_deliverable_indicator

    # formatter
    def _format_non_deliverable_indicator_17F(self, val):
        return val

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_17F_Type)
    def _validate_non_deliverable_indicator_17F(self, val):
        return val

    # setter
    def _set_non_deliverable_indicator_17F(self, val):
        self.swift_obj.SequenceA_GeneralInformation.Non_DeliverableIndicator= val
        self.swift_obj.SequenceA_GeneralInformation.Non_DeliverableIndicator.swiftTag = "17F"

    # ------------------ NDF_Open_Indicator -----------------------
    # getter
    def ndf_open_indicator_17O(self):
        '''Returns terms and conditions as string'''
        ndf_open_indicator = None
        trade = self.acm_obj.Trade()
        if trade:
            ins = trade.Instrument()
            if ins and ins.IsKindOf(acm.FFuture):
                ndf_open_indicator = 'N'
                if trade.Type() == "Normal":
                    ndf_open_indicator = 'Y'
        return ndf_open_indicator

    # formatter
    def _format_ndf_open_indicator_17O(self, val):
        return val

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_17O_Type)
    def _validate_ndf_open_indicator_17O(self, val):
        return val

    # setter
    def _set_ndf_open_indicator_17O(self, val):
        self.swift_obj.SequenceA_GeneralInformation.NDFOpenIndicator = val
        self.swift_obj.SequenceA_GeneralInformation.NDFOpenIndicator.swiftTag = "17O"

    # ------------------ Settlement Currency -----------------------
    # getter
    def settlement_currency_32E(self):
        '''Returns terms and conditions as string'''
        sett_curr = ''
        trade = self.acm_obj.Trade()
        if trade:
            ins = trade.Instrument()
            if ins and ins.IsKindOf(acm.FFuture) and trade.Type() in ["Normal"]:
                sett_curr = ins.Currency().Name()
        return sett_curr

    # formatter
    def _format_settlement_currency_32E(self, val):
        return val

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_32E_Type)
    def _validate_settlement_currency_32E(self, val):
        return val

    # setter
    def _set_settlement_currency_32E(self, val):
        self.swift_obj.SequenceA_GeneralInformation.SettlementCurrency = val
        self.swift_obj.SequenceA_GeneralInformation.SettlementCurrency.swiftTag = "32E"

    # ------------------ Valuation Date -----------------------
    # getter
    def valuation_date_30U(self):
        '''Returns terms and conditions as string'''
        valuation_date = ''
        trade = self.acm_obj.Trade()
        if trade:
            ins = trade.Instrument()
            if ins and ins.IsKindOf(acm.FFuture) and trade.Type() in ["Normal"]:
                valuation_date = ins.ExpiryDate()
        return valuation_date

    # formatter
    def _format_valuation_date_30U(self, val):
        if val:
            date_format = '%Y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)
            return val

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_30U_Type)
    def _validate_valuation_date_30U(self, val):
        return val

    # setter
    def _set_valuation_date_30U(self, val):
        self.swift_obj.SequenceA_GeneralInformation.ValuationDate = val
        self.swift_obj.SequenceA_GeneralInformation.ValuationDate.swiftTag = "30U"

    # ------------------ related_reference -----------------------
    # Getter
    def settlement_rate_source_14S(self):
        """Returns Confirmation Object. If the trade is a NDF closing, return the field 20 of parent confirmation"""
        settlement_rate_source_dict = {}
        ret_val = None
        ins = self.acm_obj.Trade().Instrument()
        if ins:
            fixing_source_party = ins.FixingSource()
            if fixing_source_party:
                settlement_rate_source_dict['CUTT_OFF'] = fixing_source_party.ExternalCutOff()
                settlement_rate_source_dict['LOCATION'] = fixing_source_party.City()
                for alias in fixing_source_party.Aliases():
                    if alias.Type().Name() == 'ISDASettlementSrc':
                        if alias.Alias():
                            settlement_rate_source_dict['RATE_SOURCE'] = alias.Alias()
                            ret_val = settlement_rate_source_dict
                        break

                if ret_val is None:
                    notifier.ERROR("Set party alias 'ISDASettlementSrc' on MTMMarket parties and specify settlement source code as its value."
                                   "It is required to populate field 14S in MT300.")
        return ret_val

    # formatter
    def _format_settlement_rate_source_14S(self, val):
        settlement_rate_source_dict = val
        formatted_value = ''
        cutt_off = settlement_rate_source_dict.get('CUTT_OFF', None)
        location = settlement_rate_source_dict.get('LOCATION', None)
        rate_source = settlement_rate_source_dict.get('RATE_SOURCE', None)

        formatted_value = rate_source
        # If the user has specified EMT00 in party alias we skip cut off and location
        if rate_source != 'EMT00':
            if cutt_off:
                formatted_value += '/' + str(cutt_off)

            if location:
                formatted_value += '/' + location

        return formatted_value

    # validator
    @validate_with(MT300.MT300_SequenceA_GeneralInformation_14S_Type)
    def _validate_settlement_rate_source_14S(self, val):
        return val

    def _check_condition_set_settlement_rate_source_14S(self):
        rel_ref_cond = False
        if self.simulated_closing_NDF_settlement:
            rel_ref_cond = True
        return rel_ref_cond

    # setter
    def _set_settlement_rate_source_14S(self, val):
        settlement_rate_source_seq = MT300.MT300_SequenceA_GeneralInformation().SettlementRateSource

        settlement_rate_source_seq.SettlementRateSource = val
        settlement_rate_source_seq.SettlementRateSource.swiftTag = "14S"

        self.swift_obj.SequenceA_GeneralInformation.SettlementRateSource.append(settlement_rate_source_seq.SettlementRateSource)

    # ------------------ trade_date -----------------------

    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_30T_Type)
    def _validate_trade_date_30T(self, val):
        return val

    # setter
    def _set_trade_date_30T(self, val):
        self.swift_obj.SequenceB_TransactionDetails.TradeDate = val
        self.swift_obj.SequenceB_TransactionDetails.TradeDate.swiftTag = "30T"

    # ------------------ value_date -----------------------
    # getter
    def value_date_30V(self):
        '''Returns value date as string'''
        if self.use_operations_xml:
            value_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'VALUE_DATE'])
        else:
            value_date = FSwiftConfirmationUtils.get_value_date(self.acm_obj)
        return value_date

    # formatter
    def _format_value_date_30V(self, val):
        if val:
            date_format = '%Y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)
            return val

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_30V_Type)
    def _validate_value_date_30V(self, val):
        return val

    # setter
    def _set_value_date_30V(self, val):
        self.swift_obj.SequenceB_TransactionDetails.ValueDate = val
        self.swift_obj.SequenceB_TransactionDetails.ValueDate.swiftTag = "30V"

    # ------------------ exchange_rate -----------------------
    # getter
    def exchange_rate_36(self):
        '''Returns exchange rate as string'''
        if self.use_operations_xml:
            exchange_rate = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'EXCHANGE_RATE'])
        else:
            exchange_rate = get_exchange_rate(self.acm_obj)
        return exchange_rate

    # formatter
    def _format_exchange_rate_36(self, val):
        if val:
            val = FSwiftMLUtils.float_to_swiftmt(str(val))
            return val

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_36_Type)
    def _validate_exchange_rate_36(self, val):
        validateAmount(val, 12, "Exchange Rate")
        return val

    # setter
    def _set_exchange_rate_36(self, val):
        self.swift_obj.SequenceB_TransactionDetails.ExchangeRate = val
        self.swift_obj.SequenceB_TransactionDetails.ExchangeRate.swiftTag = "36"

    # ------------------ currency_amount_bought_details -----------------------
    # getter
    def currency_amount_bought_32B(self):
        '''Returns dictionary with keys 'BUY_AMOUNT', 'BUY_CURRENCY' and their corresponding values '''
        if self.use_operations_xml:
            val_dict = {}
            buy_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'BUY_AMOUNT'])
            buy_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                    ['SWIFT', 'BUY_CURRENCY'])
            val_dict['BUY_AMOUNT'] = buy_amount
            val_dict['BUY_CURRENCY'] = buy_currency
            return val_dict
        else:
            val_dict = {}
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                if self.acm_obj.Trade().Instrument().Currency().Name() == self.acm_obj.Trade().CurrencyPair().Currency1().Name():
                    if self.acm_obj.Trade().Sold():
                        val_dict['BUY_AMOUNT'] = abs(self.acm_obj.Trade().Quantity() / self.acm_obj.Trade().Price())
                        val_dict['BUY_CURRENCY'] = self.acm_obj.Trade().CurrencyPair().Currency1().Name()
                    else:
                        val_dict['BUY_AMOUNT'] = self.acm_obj.Trade().Quantity()
                        val_dict['BUY_CURRENCY'] = self.acm_obj.Trade().CurrencyPair().Currency2().Name()
                else:
                    if self.acm_obj.Trade().Sold():
                        val_dict['BUY_AMOUNT'] = abs(self.acm_obj.Trade().Quantity() * self.acm_obj.Trade().Price())
                        val_dict['BUY_CURRENCY'] = self.acm_obj.Trade().CurrencyPair().Currency2().Name()
                    else:
                        val_dict['BUY_AMOUNT'] = self.acm_obj.Trade().Quantity()
                        val_dict['BUY_CURRENCY'] = self.acm_obj.Trade().CurrencyPair().Currency1().Name()
            else:
                val_dict['BUY_AMOUNT'] = get_buy_amount(self.acm_obj)
                val_dict['BUY_CURRENCY'] = get_buy_currency(self.acm_obj)
            return val_dict

    # formatter
    def _format_currency_amount_bought_32B(self, val_dict):
        buy_amount = val_dict.get('BUY_AMOUNT')
        buy_currency = val_dict.get('BUY_CURRENCY')
        if buy_amount and buy_currency:
            buy_amount = apply_currency_precision(buy_currency, float(buy_amount))
            val = str(buy_currency) + str(FSwiftMLUtils.float_to_swiftmt(str(buy_amount)))
            return val

    # validator
    @validate_with(MT300.MT300_SubSequenceB1_AmountBought_32B_Type)
    def _validate_currency_amount_bought_32B(self, val):
        validate_currency_amount(val, "Currency Amount Bought")
        amount = get_amount_from_currency_amount(val)
        validateAmount(amount.replace('.', ','), 15, "Currency Amount Bought")
        return val

    # setter
    def _set_currency_amount_bought_32B(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.CurrencyAmount = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.CurrencyAmount.swiftTag = "32B"

    # ------------------ buy_delivery_agent -----------------------

    # option getter
    def get_buy_delivery_agent_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_buy_delivery_agent(self):
        if self.use_operations_xml:
            buy_delivery_agent_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'BUY_DELIVERY_AGENT_OPTION'])
        else:
            buy_delivery_agent_option = self.get_buy_delivery_agent_option()

        if buy_delivery_agent_option == "A":
            return 'buy_delivery_agent_53A'
        elif buy_delivery_agent_option == "J":
            return 'buy_delivery_agent_53J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % (str(buy_delivery_agent_option), 'BuyDeliveryAgent_53a'))
        return 'buy_delivery_agent_53A'

    # getter
    def buy_delivery_agent_53A(self):
        '''Returns dictionary with keys 'ACCOUNT', 'BIC' and their corresponding values
           Since Acquirer & Counterparty are both buyer and seller. While sending confirmation sender will represents both
           sides i.e. buy and sell. 53A of amount bought section 'This field identifies the financial institution from which the payer will transfer the amount bought.'
        '''
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'BUY_DELIVERY_AGENT_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'BUY_DELIVERY_AGENT_BIC'],
                                                           ignore_absense=True)
            values_dict['BIC'] = bic
        else:
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                values_dict = None
            else:
                values_dict = get_counterparty_delivery_agent_details(self.acm_obj)
                values_dict.pop('ACCOUNT')
            return values_dict

    # formatter
    def _format_buy_delivery_agent_53A(self, val):
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type)
    def _validate_buy_delivery_agent_53A(self, val):
        return val

    # setter
    def _setbuy_delivery_agent_53A(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.DeliveryAgent_A = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.DeliveryAgent_A.swiftTag = "53A"


    # getter
    def buy_delivery_agent_53J(self):
        '''Returns dictionary with keys 'NAME', 'ADDRESS', 'ACCOUNT', 'BIC' and their corresponding values '''
        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'BUY_DELIVERY_AGENT_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'BUY_DELIVERY_AGENT_BIC'],
                                                           ignore_absense=True) or "UKWN"
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                            ['SWIFT', 'BUY_DELIVERY_AGENT_NAME'],
                                                            ignore_absense=True)
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'BUY_DELIVERY_AGENT_ADDRESS'],
                                                               ignore_absense=True)
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            values_dict = {}
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                values_dict = None
            else:
                values_dict = get_counterparty_delivery_agent_details(self.acm_obj)
            return values_dict

    # formatter
    def _format_buy_delivery_agent_53J(self, val):
        return self._format_Option_J(val)


    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type)
    def _validate_buy_delivery_agent_53J(self, val):
        return val

    # setter
    def _setbuy_delivery_agent_53J(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.DeliveryAgent_J = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.DeliveryAgent_J.swiftTag = "53J"

    # ------------------ buy_intermediary -----------------------
    # option getter
    def get_buy_intermediary_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option


    # setter
    def _set_OPTION_buy_intermediary(self):
        if self.use_operations_xml:
            buy_intermediary_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                               ['SWIFT', 'BUY_INTERMEDIARY_OPTION'],
                                                                               ignore_absense=True)
        else:
            buy_intermediary_option = self.get_buy_intermediary_option()

        if buy_intermediary_option == "A":
            return 'buy_intermediary_56A'
        elif buy_intermediary_option == "J":
            return 'buy_intermediary_56J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % (str(buy_intermediary_option), 'BuyIntermediary_56a'))
        return 'buy_intermediary_56A'

    # getter
    def buy_intermediary_56A(self):
        '''Returns dictionary with keys 'ACCOUNT', 'BIC' and their corresponding values '''
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'BUY_INTERMEDIARY_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'BUY_INTERMEDIARY_BIC'],
                                                           ignore_absense=True)
            if bic:
                values_dict['BIC'] = bic
            return values_dict
        else:
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                values_dict = None
            else:
                values_dict = get_acquirer_intermediary_details(self.acm_obj)
                values_dict.pop('ACCOUNT')
            return values_dict

    # formatter
    def _format_buy_intermediary_56A(self, val):

        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type)
    def _validate_buy_intermediary_56A(self, val):
        return val

    # setter
    def _setbuy_intermediary_56A(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.Intermediary_A = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.Intermediary_A.swiftTag = "56A"

    # getter
    def buy_intermediary_56J(self):
        '''Returns dictionary with keys 'NAME', 'ADDRESS', 'ACCOUNT' and their corresponding values '''

        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'BUY_INTERMEDIARY_ACCOUNT'],
                                                               ignore_absense=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                            ['SWIFT', 'BUY_INTERMEDIARY_NAME'],
                                                            ignore_absense=True)
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'BUY_INTERMEDIARY_ADDRESS'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                ['SWIFT', 'BUY_INTERMEDIARY_BIC'],
                                                                ignore_absense=True)
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                values_dict = None
            else:
                values_dict = get_acquirer_intermediary_details(self.acm_obj)
            return values_dict

    # formatter
    def _format_buy_intermediary_56J(self, val):
        return self._format_Option_J(val)

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type)
    def _validate_buy_intermediary_56J(self, val):
        return val

    # setter
    def _setbuy_intermediary_56J(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.Intermediary_J = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.Intermediary_J.swiftTag = "56J"

    # ------------------ buy_receiving_agent -----------------------

    # option getter
    def get_buy_receiving_agent_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_buy_receiving_agent(self):
        if self.use_operations_xml:
            buy_receiving_agent_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                  ['SWIFT',
                                                                                   'BUY_RECEIVING_AGENT_OPTION'])
        else:
            buy_receiving_agent_option = self.get_buy_receiving_agent_option()

        if self.is_confirmation_closing_NDF or self.simulated_closing_NDF_settlement:
            if self.get_NDF_buy_sell_currency(True) != self.acm_obj.Trade().Instrument().Currency().Name():
                buy_receiving_agent_option = "J"

        if buy_receiving_agent_option == "A":
            return 'buy_receiving_agent_57A'
        elif buy_receiving_agent_option == "J":
            return 'buy_receiving_agent_57J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % (str(buy_receiving_agent_option), 'BuyReceivingAgent_57a'))

        return 'buy_receiving_agent_57A'

    # getter
    def buy_receiving_agent_57A(self):
        '''Returns dictionary with keys 'ACCOUNT', 'BIC' and their corresponding values '''
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'BUY_RECEIVING_AGENT_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'BUY_RECEIVING_AGENT_BIC'])
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                values_dict = self.get_acquirer_receiving_agent_details_NDF()
            else:
                values_dict = get_acquirer_receiving_agent_details(self.acm_obj)

            return values_dict

    # formatter
    def _format_buy_receiving_agent_57A(self, val):
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type)
    def _validate_buy_receiving_agent_57A(self, val):
        return val

    # setter
    def _setbuy_receiving_agent_57A(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_A = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_A.swiftTag = "57A"

    # getter
    def buy_receiving_agent_57J(self):
        '''Returns dictionary with keys 'NAME', 'ADDRESS', 'ACCOUNT' and their corresponding values '''

        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'BUY_RECEIVING_AGENT_ACCOUNT'],
                                                               ignore_absense=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                            ['SWIFT', 'BUY_RECEIVING_AGENT_NAME'])
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'BUY_RECEIVING_AGENT_ADDRESS'])

            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            return values_dict
        else:
            values_dict = {}
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                if self.get_NDF_buy_sell_currency(True) != self.acm_obj.Trade().Instrument().Currency().Name():
                    values_dict['NDF'] = 'NDFS'
                else:
                    values_dict = self.get_acquirer_receiving_agent_details_NDF()
            else:
                values_dict = get_acquirer_receiving_agent_details(self.acm_obj)
            return values_dict

    # formatter
    def _format_buy_receiving_agent_57J(self, val):
        name = val.get('NAME')
        account = val.get('ACCOUNT')
        address = val.get('ADDRESS')
        bic = val.get('BIC')
        nosi = val.get('NDF')
        if name:
            val = '/ABIC/' + (bic or 'UKWN')
            if account:
                val = val + "/ACCT/" + account
            if address:
                val = val + '/ADD1/' + address
            val = str(val) + '/NAME/' + str(name)
        if nosi:
            val = '/NOSI/' + str(nosi)
        lines = FSwiftWriterUtils.split_text_on_character_limit(val, 40)
        val = FSwiftWriterUtils.allocate_space_for_n_lines(5, lines)
        return val

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type)
    def _validate_buy_receiving_agent_57J(self, val):
        return val

    # setter
    def _setbuy_receiving_agent_57J(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_J = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_J.swiftTag = "57J"

    # ------------------ currency_amount_sold_details -----------------------

    # getter
    def currency_amount_sold_33B(self):
        '''Returns dictionary with keys 'SELL_AMOUNT', 'SELL_CURRENCY' and their corresponding values '''

        if self.use_operations_xml:
            val_dict = {}
            sell_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                   ['SWIFT', 'SELL_AMOUNT'])
            sell_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'SELL_CURRENCY'])

            val_dict['SELL_AMOUNT'] = sell_amount
            val_dict['SELL_CURRENCY'] = sell_currency
            return val_dict
        else:
            val_dict = {}
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                if self.acm_obj.Trade().Instrument().Currency().Name() == self.acm_obj.Trade().CurrencyPair().Currency1().Name():
                    if self.acm_obj.Trade().Sold():
                        val_dict['SELL_AMOUNT'] = abs(self.acm_obj.Trade().Quantity())
                        val_dict['SELL_CURRENCY'] = self.acm_obj.Trade().CurrencyPair().Currency2().Name()
                    else:
                        val_dict['SELL_AMOUNT'] = abs(self.acm_obj.Trade().Quantity()/self.acm_obj.Trade().Price())
                        val_dict['SELL_CURRENCY'] = self.acm_obj.Trade().CurrencyPair().Currency1().Name()
                else:
                    if self.acm_obj.Trade().Sold():
                        val_dict['SELL_AMOUNT'] = abs(self.acm_obj.Trade().Quantity())
                        val_dict['SELL_CURRENCY'] = self.acm_obj.Trade().CurrencyPair().Currency1().Name()
                    else:
                        val_dict['SELL_AMOUNT'] = abs(self.acm_obj.Trade().Quantity() * self.acm_obj.Trade().Price())
                        val_dict['SELL_CURRENCY'] = self.acm_obj.Trade().CurrencyPair().Currency2().Name()
            else:
                val_dict['SELL_AMOUNT'] = get_sell_amount(self.acm_obj)
                val_dict['SELL_CURRENCY'] = get_sell_currency(self.acm_obj)
            return val_dict

    # formatter
    def _format_currency_amount_sold_33B(self, val_dict):
        sell_amount = val_dict.get('SELL_AMOUNT')
        sell_currency = val_dict.get('SELL_CURRENCY')
        if sell_amount and sell_currency:
            sell_amount = apply_currency_precision(sell_currency, float(sell_amount))
            if sell_amount < 0:
                sell_amount = abs(sell_amount)
            val = str(sell_currency) + str(FSwiftMLUtils.float_to_swiftmt(str(sell_amount)))
            return val

    # validator
    @validate_with(MT300.MT300_SubSequenceB2_AmountSold_33B_Type)
    def _validate_currency_amount_sold_33B(self, val):
        validate_currency_amount(val, "Currency Amount Sold")
        amount = get_amount_from_currency_amount(val)
        validateAmount(amount.replace('.', ','), 15, "Currency Amount Sold")
        return val

    # setter
    def _set_currency_amount_sold_33B(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.CurrencyAmount = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.CurrencyAmount.swiftTag = "33B"

    # ------------------ sell_delivery_agent -----------------------

    # option getter
    def get_sell_delivery_agent_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_sell_delivery_agent(self):
        if self.use_operations_xml:
            sell_delivery_agent_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                  ['SWIFT',
                                                                                   'SELL_DELIVERY_AGENT_OPTION'],
                                                                                  ignore_absense=True)
        else:
            sell_delivery_agent_option = self.get_sell_delivery_agent_option()
        if sell_delivery_agent_option == "A":
            return 'sell_delivery_agent_53A'
        elif sell_delivery_agent_option == "J":
            return 'sell_delivery_agent_53J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % (str(sell_delivery_agent_option), 'SellDeliveryAgent_53a'))
        return 'sell_delivery_agent_53A'


    # getter
    def sell_delivery_agent_53A(self):
        '''Returns dictionary with keys 'ACCOUNT', 'BIC' and their corresponding values '''

        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_DELIVERY_AGENT_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SELL_DELIVERY_AGENT_BIC'],
                                                           ignore_absense=True)
            values_dict['BIC'] = bic
            return values_dict
        else:
            values_dict = {}
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                values_dict = None
                if values_dict:
                    values_dict.pop('ACCOUNT')
            else:
                values_dict= get_acquirer_delivery_agent_details(self.acm_obj)
                values_dict.pop('ACCOUNT')
            return values_dict

    # formatter
    def _format_sell_delivery_agent_53A(self, val):
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type)
    def _validate_sell_delivery_agent_53A(self, val):
        return val

    # setter
    def _setsell_delivery_agent_53A(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.DeliveryAgent_A = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.DeliveryAgent_A.swiftTag = "53A"


    # getter
    def sell_delivery_agent_53J(self):
        '''Returns dictionary with keys 'NAME', 'ACCOUNT', 'ADDRESS', 'BIC' and their corresponding values '''

        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_DELIVERY_AGENT_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SELL_DELIVERY_AGENT_BIC']
                                                           , ignore_absense=True) or "UKWN"
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                            ['SWIFT', 'SELL_DELIVERY_AGENT_NAME'],
                                                            ignore_absense=True)
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_DELIVERY_AGENT_ADDRESS'],
                                                               ignore_absense=True)
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            values_dict = {}
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                values_dict = None
            else:
                values_dict = get_acquirer_delivery_agent_details(self.acm_obj)
            return values_dict

    # formatter
    def _format_sell_delivery_agent_53J(self, val):
        return self._format_Option_J(val)

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type)
    def _validate_sell_delivery_agent_53J(self, val):
        return val

    # setter
    def _setsell_delivery_agent_53J(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.DeliveryAgent_J = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.DeliveryAgent_J.swiftTag = "53J"

    # ------------------ sell_intermediary -----------------------

    # option getter
    def get_sell_intermediary_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_sell_intermediary(self):
        if self.use_operations_xml:
            sell_intermediary_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                ['SWIFT', 'SELL_INTERMEDIARY_OPTION'],
                                                                                ignore_absense=True)
        else:
            sell_intermediary_option = self.get_sell_intermediary_option()
        if sell_intermediary_option == "A":
            return 'sell_intermediary_56A'
        elif sell_intermediary_option == "J":
            return 'sell_intermediary_56J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % (str(sell_intermediary_option), 'SellIntermediary_56a'))
        return 'sell_intermediary_56A'

    # getter
    def sell_intermediary_56A(self):
        '''Returns dictionary with keys 'ACCOUNT', 'BIC' and their corresponding values '''

        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_INTERMEDIARY_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SELL_INTERMEDIARY_BIC'],
                                                           ignore_absense=True)
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                values_dict = None
            else:
                values_dict= get_counterparty_intermediary_details(self.acm_obj)
            return values_dict



    # formatter
    def _format_sell_intermediary_56A(self, val):
        bic = val.get('BIC')
        if bic:
            val = str(bic)
            return val

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type)
    def _validate_sell_intermediary_56A(self, val):
        return val

    # setter
    def _setsell_intermediary_56A(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.Intermediary_A = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.Intermediary_A.swiftTag = "56A"

    # getter
    def sell_intermediary_56J(self):
        '''Returns dictionary with keys 'NAME', 'ACCOUNT', 'ADDRESS' and their corresponding values '''
        if self.use_operations_xml:
            values_dict = {}

            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_INTERMEDIARY_ACCOUNT'],
                                                               ignore_absense=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                            ['SWIFT', 'SELL_INTERMEDIARY_NAME']
                                                            , ignore_absense=True)
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_INTERMEDIARY_ADDRESS'],
                                                               ignore_absense=True)
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            return values_dict
        else:
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                values_dict = None
            else:
                values_dict= get_counterparty_intermediary_details(self.acm_obj)
            return values_dict

    # formatter
    def _format_sell_intermediary_56J(self, val):
        return self._format_Option_J(val)

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type)
    def _validate_sell_intermediary_56J(self, val):
        return val

    # setter
    def _setsell_intermediary_56J(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.Intermediary_J = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.Intermediary_J.swiftTag = "56J"

    # ------------------ sell_receiving_agent -----------------------

    # option getter
    def get_sell_receiving_agent_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_sell_receiving_agent(self):
        if self.use_operations_xml:
            sell_receiving_agent_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                   ['SWIFT',
                                                                                    'SELL_RECEIVING_AGENT_OPTION'])
        else:
            sell_receiving_agent_option = self.get_sell_receiving_agent_option()

        if self.is_confirmation_closing_NDF or self.simulated_closing_NDF_settlement:
            sell_curr = self.get_NDF_buy_sell_currency(False)
            if self.acm_obj.Trade().Instrument().Currency().Name() != sell_curr:
                sell_receiving_agent_option = "J"

        if sell_receiving_agent_option == "A":
            return 'sell_receiving_agent_57A'
        elif sell_receiving_agent_option == "J":
            return 'sell_receiving_agent_57J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % (str(sell_receiving_agent_option), 'SellReceivingAgent_57a'))
        return 'sell_receiving_agent_57A'

    # getter
    def sell_receiving_agent_57A(self):
        '''Returns dictionary with keys  'ACCOUNT', 'BIC' and their corresponding values '''

        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_RECEIVING_AGENT_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SELL_RECEIVING_AGENT_BIC'])
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                values_dict = self.get_counterparty_receiving_agent_details_NDF()
            else:
                values_dict = get_counterparty_receiving_agent_details(self.acm_obj)
            return values_dict



    # formatter
    def _format_sell_receiving_agent_57A(self, val):
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type)
    def _validate_sell_receiving_agent_57A(self, val):
        return val

    # setter
    def _setsell_receiving_agent_57A(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_A = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_A.swiftTag = "57A"

    # getter
    def sell_receiving_agent_57J(self):
        '''Returns dictionary with keys 'NAME', 'ACCOUNT', 'ADDRESS' and their corresponding values '''

        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_RECEIVING_AGENT_ACCOUNT'],
                                                               ignore_absense=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                            ['SWIFT', 'SELL_RECEIVING_AGENT_NAME'])
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_RECEIVING_AGENT_ADDRESS'])
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            return values_dict
        else:
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                values_dict = {}
                sell_curr = self.get_NDF_buy_sell_currency(False)
                if self.acm_obj.Trade().Instrument().Currency().Name() != sell_curr:
                    values_dict['NDF'] = 'NDFS'
                else:
                    values_dict = self.get_counterparty_receiving_agent_details_NDF()
            else:
                values_dict= get_counterparty_receiving_agent_details(self.acm_obj)
            return values_dict

    # formatter
    def _format_sell_receiving_agent_57J(self, val):
        name = val.get('NAME')
        account = val.get('ACCOUNT')
        address = val.get('ADDRESS')
        bic = val.get('BIC')
        nosi = val.get('NDF')
        if name:
            val = '/ABIC/' + (bic or 'UKWN')
            if account:
                val = val + "/ACCT/" + account
            if address:
                val = val + '/ADD1/' + address
            val = str(val) + '/NAME/' + str(name)
        if nosi:
            val = '/NOSI/' + str(nosi)
        lines = FSwiftWriterUtils.split_text_on_character_limit(val, 40)
        val = FSwiftWriterUtils.allocate_space_for_n_lines(5, lines)
        return val

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type)
    def _validate_sell_receiving_agent_57J(self, val):
        return val

    # setter
    def _setsell_receiving_agent_57J(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_J = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_J.swiftTag = "57J"

    # ------------------ sell_beneficiary_institution -----------------------

    # option getter
    def get_sell_beneficiary_institution_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_sell_beneficiary_institution(self):
        if self.use_operations_xml:
            sell_beneficiary_institution_option = FSwiftWriterUtils.get_value_from_xml_tag \
                (self.swift_metadata_xml_dom, ['SWIFT', 'SELL_BENEFICIARY_INSTITUTION_OPTION'], ignore_absense=True)
        else:
            sell_beneficiary_institution_option = self.get_sell_beneficiary_institution_option()

        if sell_beneficiary_institution_option == "A":
            return 'sell_beneficiary_institution_58A'
        elif sell_beneficiary_institution_option == "J":
            return 'sell_beneficiary_institution_58J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % (str(sell_beneficiary_institution_option), 'SellBeneficiaryInstitution_58a'))
        return 'sell_beneficiary_institution_58A'

    # getter
    def sell_beneficiary_institution_58A(self):
        '''Returns dictionary with keys  'ACCOUNT',  'BIC' and their corresponding values '''

        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_BENEFICIARY_INSTITUTION_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SELL_BENEFICIARY_INSTITUTION_BIC'],
                                                           ignore_absense=True)
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                values_dict = None
            else:
                values_dict = get_beneficiary_institution_details(self.acm_obj)
            return values_dict


    # formatter
    def _format_sell_beneficiary_institution_58A(self, val):
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type)
    def _validate_sell_beneficiary_institution_58A(self, val):
        return val

    # setter
    def _setsell_beneficiary_institution_58A(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.BeneficiaryInstitution_A = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.BeneficiaryInstitution_A.swiftTag = "58A"


    # getter
    def sell_beneficiary_institution_58J(self):
        '''Returns dictionary with keys 'NAME', 'ACCOUNT', 'ADDRESS', 'BIC' and their corresponding values '''
        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_BENEFICIARY_INSTITUTION_ACCOUNT'],
                                                               ignore_absense=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                            ['SWIFT', 'SELL_BENEFICIARY_INSTITUTION_NAME'],
                                                            ignore_absense=True)
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_BENEFICIARY_INSTITUTION_ADDRESS'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SELL_BENEFICIARY_INSTITUTION_BIC'],
                                                           ignore_absense=True)
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                values_dict = None
            else:
                values_dict = get_beneficiary_institution_details_MT300(self.acm_obj)
            return values_dict

    # formatter
    def _format_sell_beneficiary_institution_58J(self, val):
        return self._format_Option_J(val)

    # validator
    @validate_with(MT300.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type)
    def _validate_sell_beneficiary_institution_58J(self, val):
        return val

    # setter
    def _setsell_beneficiary_institution_58J(self, val):
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.BeneficiaryInstitution_J = val
        self.swift_obj.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.BeneficiaryInstitution_J.swiftTag = "58J"

    # ------------------ counterpartys_reference -----------------------
    def counterpartys_reference_26H(self):
        '''Returns counterparty reference as string '''

        if self.use_operations_xml:
            counterpartys_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                               ['SWIFT', 'COUNTERPARTYS_REFERENCE'],
                                                                               ignore_absense=True)
        else:
            counterpartys_reference = self.acm_obj.Trade().YourRef()
        return counterpartys_reference

    def _format_counterpartys_reference_26H(self, val):
        return val

    @validate_with(MT300.MT300_SequenceC_OptionalGeneralInformation_26H_Type)
    def _validate_counterpartys_reference_26H(self, val):
        return val

    def _set_counterpartys_reference_26H(self, val):
        self.swift_obj.SequenceC_OptionalGeneralInformation.CounterpartysReference = val
        self.swift_obj.SequenceC_OptionalGeneralInformation.CounterpartysReference.swiftTag = "26H"


# ================================================================================================================


class FMT300OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_type = "300"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT' + self.mt_type)
        super(FMT300OutBaseMessageHeader, self).__init__(self.mt_type, self.acm_obj, swift_msg_tags)

    def message_type(self):
        return "300"

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
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['CONFIRMATION', 'SEQNBR'])
        else:
            seqnbr = self.acm_obj.Oid()
        return "{108:%s-%s-%s}" % (get_confirmation_reference_prefix(), seqnbr, get_message_version_number(self.acm_obj))


class FMT300OutBaseNetworkRules(object):
    ''' '''

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.acm_obj = acm_obj

    def network_rule_C1(self):
        '''In sequence A, the presence of field 21 depends on field 22A
            Sequence A if field 22A is ...   Sequence A then field 21 is ...
            AMND                                Mandatory
            CANC                                Mandatory
            DUPL                                Optional
            EXOP                                Optional
            NEWT                                Optional'''
        if self.swift_message_obj.SequenceA_GeneralInformation.TypeOfOperation.value() in ['AMND', 'CANC']:
            if not self.swift_message_obj.SequenceA_GeneralInformation.RelatedReference or not self.swift_message_obj.SequenceA_GeneralInformation.RelatedReference.value():
                return "Field 21 in Sequence A is mandatory if field 22A in Sequence A is equal to either AMND or CANC"
        return ''

    def network_rule_C8(self):
        '''Network rule C8'''

        ndf_indicator = self.swift_message_obj.SequenceA_GeneralInformation.NDFOpenIndicator
        settle_curr = self.swift_message_obj.SequenceA_GeneralInformation.SettlementCurrency
        valuation_date = self.swift_message_obj.SequenceA_GeneralInformation.ValuationDate
        settle_source = self.swift_message_obj.SequenceA_GeneralInformation.SettlementRateSource
        ref_to_open_conf = self.swift_message_obj.SequenceA_GeneralInformation.ReferenceToOpeningConfirmation

        if ndf_indicator:
            ndf_indicator = ndf_indicator.value()
            if ndf_indicator == 'Y':
                if not settle_curr or not valuation_date or not settle_source:
                    return "Field 32E, 30U and 14S in Sequence A are mandatory if field 17O in Sequence A is equal to Y"

                if ref_to_open_conf:
                    return "Field 21A in Sequence A is not allowed if field 17O in Sequence A is equal to Y"
            else:
                if settle_curr or valuation_date or settle_source:
                    return "Field 32E, 30U and 14S in Sequence A are not allowed if field 17O in Sequence A is equal to N"

                if not ref_to_open_conf:
                    return "Field 21A in Sequence A is mandatory if field 17O in Sequence A is equal to N"
        else:
            if settle_curr or valuation_date or settle_source or ref_to_open_conf:
                return "Field 32E, 30U, 14S and 21A in Sequence A are not allowed if field 17O in Sequence A is not present"

        return ''

