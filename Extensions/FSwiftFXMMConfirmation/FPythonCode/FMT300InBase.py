"""----------------------------------------------------------------------------
MODULE:
    FMT300InBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module opened to display the logic to extract attributes
    from swift message and an acm object but the user should NOT edit it.
    User can extend/override default mapping in derived class i.e. FMT300
    Base class for mapping attributes.
    Default logic for extracting attributes from either swift data or
    confirmation object.

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""

import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('FXMMConfIn', 'FFXMMConfirmationInNotify_Config')
import FMT30X
import FSwiftMLUtils
import acm


class FMT300Base(FMT30X.FMT30X):
    """ Base class for MT300 mapping"""
    def __init__(self, source, direction):
        super(FMT300Base, self).__init__(source, direction)
        self._message_type = 'MT300'
        self.config_param = FSwiftMLUtils.Parameters('FMT300In_Config')

        self._scope_of_operation = None
        self._common_reference = None
        self._block_trade_indicator = None
        self._split_settlement_indicator = None
        self._fund_or_beneficiary_customer = None
        self._terms_and_conditions = None

        self._trade_date = None
        self._value_date = None
        self._exchange_rate = None

        self._buy_currency = None
        self._buy_amount = None
        self._buy_delivery_agent = None
        self._buy_intermediary = None
        self._buy_receiving_agent = None

        self._sell_currency = None
        self._sell_amount = None
        self._sell_delivery_agent = None
        self._sell_intermediary = None
        self._sell_receiving_agent = None
        self._sell_beneficiary_institution = None

        self._contact_information = None
        self._dealing_method = None
        self._dealing_branch_acquirer = None
        self._dealing_branch_cpty = None
        self._broker_identification = None
        self._broker_commission = None
        self._counterparty_reference = None
        self._broker_reference = None
        self._sender_receiver_information = None

        ''' NDF fields'''
        self._non_deliverable_indicator = None
        self._non_deliverable_open_indicator = None
        self._settlement_currency = None
        self._valuation_date = None
        self._settlement_rate_source = None
        self._money_flows = None


# ------------------------------------------------------------------------------
    def set_money_flows(self):
        self.simulated_closing_NDF_settlement = None
        self.is_confirmation_closing_NDF = False
        try:
            import FSwiftOperationsAPI
            EventType = FSwiftOperationsAPI.GetEventTypeEnum()
        except:
            import FConfirmationEnums
            EventType = FConfirmationEnums.EventType

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


        if self.simulated_closing_NDF_settlement:
            import FMTSettlementWrapper
            settlement_wrapper_obj = FMTSettlementWrapper.FMTSettlementWrapper(self.simulated_closing_NDF_settlement)
            self._money_flows = settlement_wrapper_obj.sell_money_flow()

            if not self._money_flows:
                self._money_flows = settlement_wrapper_obj.buy_money_flow()

            self._money_flows = [self._money_flows]

        else:
            self._money_flows = self.acm_obj.Trade().MoneyFlows()

    def SetAttributes(self):
        """ Set the attributes from incoming swift message/acm object to MT300"""
        try:
            if self.source == 'SWIFT':
                self.set_id_sender_reference()
                self.set_related_reference()
                self.set_message_function()
                self.set_scope_of_operation()
                self.set_common_reference()
                self.set_block_trade_indicator()
                self.set_split_settlement_indicator()
                self.set_acquirer()
                self.set_counterparty()
                self.set_fund_or_beneficiary_customer()
                self.set_terms_and_conditions()

                self.set_trade_date()
                self.set_value_date()
                self.set_exchange_rate()

                self.set_buy_cur_amount()
                self.set_buy_delivery_agent()
                self.set_buy_intermediary()
                self.set_buy_receiving_agent()

                self.set_sell_cur_amount()
                self.set_sell_delivery_agent()
                self.set_sell_intermediary()
                self.set_sell_receiving_agent()
                self.set_sell_beneficiary_institution()

                self.set_contact_information()
                self.set_dealing_method()
                self.set_dealing_branch_acquirer()
                self.set_dealing_branch_cpty()
                self.set_broker_identification()
                self.set_broker_commission()
                self.set_counterparty_reference()
                self.set_broker_reference()
                self.set_sender_receiver_information()

                self.set_non_deliverable_indicator()
                self.set_non_deliverable_open_indicator()
                self.set_settlement_currency()
                self.set_settlement_rate_source()
                self.set_valuation_date()

                self.ext_ref = self.InternalIdentifier()

            elif self.source == 'ACM':
                self.set_money_flows()
                self.set_curr_amt_from_trade()
                self.set_value_date_from_trade()
                self.set_trade_date_from_trade()
                self.set_exchange_rate_from_trade()
                self.set_acquirer_counterparty_from_trade()
                self.set_acq_acc_cpty_acc_from_trade()
                self.set_non_deliverable_indicator_from_trade()
                self.set_non_deliverable_open_indicator_from_trade()
                self.set_settlement_currency_from_trade()
                self.set_valuation_date_from_trade()
                self.set_settlement_rate_source_from_trade()
        except Exception as e:
            notifier.ERROR("Exception occurred in SetAttributes : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

# ------------------------------------------------------------------------------
    # Methods to fetch data from the swift message
    def set_id_sender_reference(self):
        try:
            if self.python_object.SequenceA_GeneralInformation and self.python_object.SequenceA_GeneralInformation.SendersReference:
                self._identifier = str(self.python_object.SequenceA_GeneralInformation.SendersReference.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_id_sender_reference : %s"%str(e))

    def set_message_function(self):
        try:
            self._message_function = str(self.python_object.SequenceA_GeneralInformation.TypeOfOperation.value()) if self.python_object.SequenceA_GeneralInformation.TypeOfOperation else None
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_message_function : %s"%str(e))

    def set_scope_of_operation(self):
        try:
            if self.python_object.SequenceA_GeneralInformation and self.python_object.SequenceA_GeneralInformation.ScopeOfOperation:
                self._scope_of_operation = str(self.python_object.SequenceA_GeneralInformation.ScopeOfOperation.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_scope_of_operation : %s"%str(e))

    def set_common_reference(self):
        try:
            if self.python_object.SequenceA_GeneralInformation and self.python_object.SequenceA_GeneralInformation.CommonReference:
                self._common_reference = str(self.python_object.SequenceA_GeneralInformation.CommonReference.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_common_reference : %s"%str(e))

    def set_block_trade_indicator(self):
        try:
            if self.python_object.SequenceA_GeneralInformation and self.python_object.SequenceA_GeneralInformation.BlockTradeIndicator:
                self._block_trade_indicator = str(self.python_object.SequenceA_GeneralInformation.BlockTradeIndicator.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_block_trade_indicator : %s"%str(e))

    def set_split_settlement_indicator(self):
        try:
            if self.python_object.SequenceA_GeneralInformation and self.python_object.SequenceA_GeneralInformation.SplitSettlementIndicator:
                self._split_settlement_indicator = str(self.python_object.SequenceA_GeneralInformation.SplitSettlementIndicator.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_split_settlement_indicator : %s"%str(e))

    def set_fund_or_beneficiary_customer(self):
        try:
            if self.python_object.SequenceA_GeneralInformation.FundOrBeneficiaryCustomer_A:
                self._fund_or_beneficiary_customer = str(self.python_object.SequenceA_GeneralInformation.FundOrBeneficiaryCustomer_A.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_fund_or_beneficiary_customer : %s"%str(e))

    def set_terms_and_conditions(self):
        try:
            if self.python_object.SequenceA_GeneralInformation.TermsAndConditions:
                self._terms_and_conditions = str(self.python_object.SequenceA_GeneralInformation.TermsAndConditions.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_terms_and_conditions : %s"%str(e))

    def set_trade_date(self):
        try:
            if self.python_object.SequenceB_TransactionDetails.TradeDate:
                self._trade_date = FSwiftMLUtils.swiftmt_to_date(str(self.python_object.SequenceB_TransactionDetails.TradeDate.value()))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_trade_date : %s"%str(e))

    def set_value_date(self):
        try:
            if self.python_object.SequenceB_TransactionDetails.ValueDate:
                self._value_date = FSwiftMLUtils.swiftmt_to_date(str(self.python_object.SequenceB_TransactionDetails.ValueDate.value()))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_value_date : %s"%str(e))

    def set_exchange_rate(self):
        try:
            if self.python_object.SequenceB_TransactionDetails.ExchangeRate:
                self._exchange_rate = FSwiftMLUtils.swiftmt_to_float(str(self.python_object.SequenceB_TransactionDetails.ExchangeRate.value()))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_exchange_rate : %s"%str(e))

    def set_buy_cur_amount(self):
        try:
            if self.direction == 'IN':
                self._buy_currency = str(self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.CurrencyAmount.value()[0:3])
                self._buy_amount = str(self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.CurrencyAmount.value()[3:])
            else:
                self._buy_currency = str(self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.CurrencyAmount.value()[0:3])
                self._buy_amount = str(self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.CurrencyAmount.value()[3:])
            self._buy_amount = FSwiftMLUtils.swiftmt_to_float(self._buy_amount)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_buy_cur_amount : %s"%str(e))

    def set_buy_delivery_agent(self):
        try:
            if self.direction == 'IN':
                self._buy_delivery_agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.DeliveryAgent_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.DeliveryAgent_A else None
            else:
                self._buy_delivery_agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.DeliveryAgent_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.DeliveryAgent_A else None
            if self._buy_delivery_agent:
                self._buy_delivery_agent = str(self.get_party_typeA(self._buy_delivery_agent))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_buy_delivery_agent : %s"%str(e))

    def set_buy_intermediary(self):
        try:
            if self.direction == 'IN':
                self._buy_intermediary = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.Intermediary_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.Intermediary_A else None
            else:
                self._buy_intermediary = self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.Intermediary_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.Intermediary_A else None
            if self._buy_intermediary:
                self._buy_intermediary = str(self.get_party_typeA(self._buy_intermediary))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_buy_intermediary : %s"%str(e))

    def set_buy_receiving_agent(self):
        try:
            if self.direction == 'IN':
                if self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_A:
                    self._buy_receiving_agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_A.value()
                elif self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_J:
                    self._buy_receiving_agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_J.value()
            else:
                if self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_A:
                    self._buy_receiving_agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_A.value()
                elif self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_J:
                    self._buy_receiving_agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_J.value()
            if self._buy_receiving_agent:
                self._buy_receiving_agent = str(self.get_party_typeA(self._buy_receiving_agent))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_buy_receiving_agent : %s"%str(e))

    def set_sell_cur_amount(self):
        try:
            if self.direction == 'IN':
                self._sell_currency = str(self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.CurrencyAmount.value()[0:3])
                self._sell_amount = self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.CurrencyAmount.value()[3:]
            else:
                self._sell_currency = str(self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.CurrencyAmount.value()[0:3])
                self._sell_amount = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.CurrencyAmount.value()[3:]
            self._sell_amount = FSwiftMLUtils.swiftmt_to_float(self._sell_amount) * -1
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_sell_cur_amount : %s"%str(e))

    def set_sell_delivery_agent(self):
        try:
            if self.direction == 'IN':
                self._sell_delivery_agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.DeliveryAgent_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.DeliveryAgent_A else None
            else:
                self._sell_delivery_agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.DeliveryAgent_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.DeliveryAgent_A else None
            if self._sell_delivery_agent:
                self._sell_delivery_agent = str(self.get_party_typeA(self._sell_delivery_agent))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_sell_delivery_agent : %s"%str(e))

    def set_sell_intermediary(self):
        try:
            if self.direction == 'IN':
                self._sell_intermediary = self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.Intermediary_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.Intermediary_A else None
            else:
                self._sell_intermediary = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.Intermediary_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.Intermediary_A else None
            if self._sell_intermediary:
                self._sell_intermediary = str(self.get_party_typeA(self._sell_intermediary))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_sell_intermediary : %s"%str(e))

    def set_sell_receiving_agent(self):
        try:
            if self.direction == 'IN':
                if self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_A:
                    self._sell_receiving_agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_A.value()
                elif self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_J:
                    self._sell_receiving_agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_J.value()
            else:
                if self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_A:
                    self._sell_receiving_agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_A.value()
                elif self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_J:
                    self._sell_receiving_agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_J.value()

            if self._sell_receiving_agent:
                self._sell_receiving_agent = str(self.get_party_typeA(self._sell_receiving_agent))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_sell_receiving_agent : %s"%str(e))

    def set_sell_beneficiary_institution(self):
        try:
            self._sell_beneficiary_institution = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.BeneficiaryInstitution_A.value() \
            if self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.BeneficiaryInstitution_A else None

            if self._sell_beneficiary_institution:
                self._sell_beneficiary_institution = str(self.get_party_typeA(self._sell_beneficiary_institution))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_sell_beneficiary_institution : %s"%str(e))

    def set_contact_information(self):
        try:
            if self.python_object.SequenceC_OptionalGeneralInformation and self.python_object.SequenceC_OptionalGeneralInformation.ContactInformation:
                self._contact_information = str(self.python_object.SequenceC_OptionalGeneralInformation.ContactInformation.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_contact_information : %s"%str(e))

    def set_dealing_method(self):
        try:
            if self.python_object.SequenceC_OptionalGeneralInformation and self.python_object.SequenceC_OptionalGeneralInformation.DealingMethod:
                self._dealing_method = str(self.python_object.SequenceC_OptionalGeneralInformation.DealingMethod.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_dealing_method : %s"%str(e))

    def set_dealing_branch_acquirer(self):
        try:
            if self.python_object.SequenceC_OptionalGeneralInformation and self.python_object.SequenceC_OptionalGeneralInformation.DealingBranchPartyA_A:
                self._dealing_branch_acquirer = str(self.python_object.SequenceC_OptionalGeneralInformation.DealingBranchPartyA_A.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_dealing_branch_acquirer : %s"%str(e))

    def set_dealing_branch_cpty(self):
        try:
            if self.python_object.SequenceC_OptionalGeneralInformation and self.python_object.SequenceC_OptionalGeneralInformation.DealingBranchPartyB_A:
                self._dealing_branch_cpty = str(self.python_object.SequenceC_OptionalGeneralInformation.DealingBranchPartyB_A.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_dealing_branch_cpty : %s"%str(e))

    def set_broker_identification(self):
        try:
            if self.python_object.SequenceC_OptionalGeneralInformation and self.python_object.SequenceC_OptionalGeneralInformation.BrokerIdentification_A:
                self._broker_identification = str(self.python_object.SequenceC_OptionalGeneralInformation.BrokerIdentification_A.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_broker_identification : %s"%str(e))

    def set_broker_commission(self):
        try:
            if self.python_object.SequenceC_OptionalGeneralInformation and self.python_object.SequenceC_OptionalGeneralInformation.BrokersCommission:
                self._broker_commission = str(self.python_object.SequenceC_OptionalGeneralInformation.BrokersCommission.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_broker_commission : %s"%str(e))

    def set_counterparty_reference(self):
        try:
            if self.python_object.SequenceC_OptionalGeneralInformation and self.python_object.SequenceC_OptionalGeneralInformation.CounterpartysReference:
                self._counterparty_reference = str(self.python_object.SequenceC_OptionalGeneralInformation.CounterpartysReference.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_counterparty_reference : %s"%str(e))

    def set_broker_reference(self):
        try:
            if self.python_object.SequenceC_OptionalGeneralInformation and self.python_object.SequenceC_OptionalGeneralInformation.BrokersReference:
                self._broker_reference = str(self.python_object.SequenceC_OptionalGeneralInformation.BrokersReference.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_broker_reference : %s"%str(e))

    def set_sender_receiver_information(self):
        try:
            if self.python_object.SequenceC_OptionalGeneralInformation and self.python_object.SequenceC_OptionalGeneralInformation.SenderToReceiverInformation:
                self._sender_receiver_information = str(self.python_object.SequenceC_OptionalGeneralInformation.SenderToReceiverInformation.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_sender_receiver_information : %s"%str(e))

    def set_non_deliverable_indicator(self):
        try:
            if self.python_object.SequenceA_GeneralInformation.Non_DeliverableIndicator:
                self._non_deliverable_indicator = str(self.python_object.SequenceA_GeneralInformation.Non_DeliverableIndicator.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_non_deliverable_indicator : %s" % str(e))

    def set_non_deliverable_open_indicator(self):
        try:
            if self.python_object.SequenceA_GeneralInformation.NDFOpenIndicator:
                self._non_deliverable_open_indicator = str(self.python_object.SequenceA_GeneralInformation.NDFOpenIndicator.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_non_deliverable_open_indicator : %s" % str(e))

    def set_settlement_currency(self):
        try:
            if self.python_object.SequenceA_GeneralInformation.SettlementCurrency:
                self._settlement_currency = str(self.python_object.SequenceA_GeneralInformation.SettlementCurrency.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_settlement_currency : %s" % str(e))

    def set_valuation_date(self):
        try:
            if self.python_object.SequenceA_GeneralInformation.ValuationDate:
                self._valuation_date = FSwiftMLUtils.swiftmt_to_date(self.python_object.SequenceA_GeneralInformation.ValuationDate.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_valuation_date : %s" % str(e))

    def set_settlement_rate_source(self):
        try:
            if self.python_object.SequenceA_GeneralInformation.SettlementRateSource:
                for src in self.python_object.SequenceA_GeneralInformation.SettlementRateSource:
                    self._settlement_rate_source = str(src.value())
                    break
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_settlement_rate_source : %s" % str(e))


# ------------------------------------------------------------------------------
    # Method to fetch data from the adm
    def set_curr_amt_from_trade(self):
        try:
            if self.simulated_closing_NDF_settlement or self.is_confirmation_closing_NDF:
                if self.acm_obj.Trade().Instrument().Currency().Name() == self.acm_obj.Trade().CurrencyPair().Currency1().Name():
                    if self.acm_obj.Trade().Sold():
                        self._buy_amount = abs(self.acm_obj.Trade().Quantity() / self.acm_obj.Trade().Price())
                        self._buy_currency = self.acm_obj.Trade().CurrencyPair().Currency1().Name()
                        self._sell_amount = self.acm_obj.Trade().Quantity()
                        self._sell_currency = self.acm_obj.Trade().CurrencyPair().Currency2().Name()
                    else:
                        self._buy_amount = self.acm_obj.Trade().Quantity()
                        self._buy_currency = self.acm_obj.Trade().CurrencyPair().Currency2().Name()
                        self._sell_amount = -1*(self.acm_obj.Trade().Quantity() / self.acm_obj.Trade().Price())
                        self._sell_currency = self.acm_obj.Trade().CurrencyPair().Currency1().Name()
                else:
                    if self.acm_obj.Trade().Sold():
                        self._buy_amount = abs(self.acm_obj.Trade().Quantity() * self.acm_obj.Trade().Price())
                        self._buy_currency = self.acm_obj.Trade().CurrencyPair().Currency2().Name()
                        self._sell_amount = self.acm_obj.Trade().Quantity()
                        self._sell_currency = self.acm_obj.Trade().CurrencyPair().Currency1().Name()
                    else:
                        self._buy_amount = self.acm_obj.Trade().Quantity()
                        self._buy_currency = self.acm_obj.Trade().CurrencyPair().Currency1().Name()
                        self._sell_amount = -1*(self.acm_obj.Trade().Quantity() * self.acm_obj.Trade().Price())
                        self._sell_currency = self.acm_obj.Trade().CurrencyPair().Currency2().Name()
            else:
                quantity = self.acm_obj.Trade().Quantity()
                premium = self.acm_obj.Trade().Premium()
                trdCurrency = self.acm_obj.Trade().Currency().Name()
                insCurrency = self.acm_obj.Trade().Instrument().Name()
                if quantity < 0:
                    self._buy_amount = premium
                    self._buy_currency = trdCurrency
                    self._sell_amount = quantity
                    self._sell_currency = insCurrency
                else:
                    self._buy_amount = quantity
                    self._buy_currency = insCurrency
                    self._sell_amount = premium
                    self._sell_currency = trdCurrency

                if self.acm_obj.Trade().QuantityIsDerived():
                    #TODO:
                    pass
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_curr_amt_from_trade : %s"%str(e))

    def set_acquirer_counterparty_from_trade(self):
        try:
            for flw in self._money_flows:
                if flw.Type() in ["Premium", "Payout"]:
                    self.counterparty = flw.CounterpartyAccount().NetworkAlias().Name() if (flw.CounterpartyAccount() and flw.CounterpartyAccount().NetworkAlias()) else self.acm_obj.Counterparty().Swift()
                    self.acquirer = flw.AcquirerAccount().NetworkAlias().Name() if (flw.AcquirerAccount() and flw.AcquirerAccount().NetworkAlias()) else self.acm_obj.Acquirer().Swift()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_counterparty_from_trade : %s"%str(e))

    def set_value_date_from_trade(self):
        try:
            self._value_date = self.acm_obj.Trade().ValueDay()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_value_date_from_trade : %s"%str(e))

    def set_trade_date_from_trade(self):
        try:
            self._trade_date = self.acm_obj.Trade().TradeTime().split()[0]
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_trade_date_from_trade : %s"%str(e))

    def set_exchange_rate_from_trade(self):
        try:
            self._exchange_rate = self.acm_obj.Trade().Price()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_price_from_trade : %s"%str(e))

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

    def set_acq_acc_cpty_acc_from_trade(self):
        try:
            for flw in self._money_flows:
                if flw.Type() in ["Premium", "Premium 2"]:
                    if flw.Currency().Name() == self._buy_currency:
                        self._buy_receiving_agent = flw.AcquirerAccount().Bic().Alias() if flw.AcquirerAccount() and flw.AcquirerAccount().Bic() else None
                        self._buy_delivery_agent = flw.CounterpartyAccount().Bic().Alias() if flw.CounterpartyAccount() and flw.CounterpartyAccount().Bic() else None
                    elif flw.Currency().Name() == self._sell_currency:
                        self._sell_delivery_agent = flw.AcquirerAccount().Bic().Alias() if flw.AcquirerAccount() and flw.AcquirerAccount().Bic() else None
                        self._sell_receiving_agent = flw.CounterpartyAccount().Bic().Alias() if flw.CounterpartyAccount() and flw.CounterpartyAccount().Bic() else None
                elif flw.Type() in ["Payout"]:
                    buy_curr = self.get_NDF_buy_sell_currency(True)
                    sell_curr = self.get_NDF_buy_sell_currency(False)
                    settle_curr = self.acm_obj.Trade().Instrument().Currency().Name()
                    if sell_curr == settle_curr:
                        self._sell_receiving_agent = flw.CounterpartyAccount().Bic().Alias() if flw.CounterpartyAccount() and flw.CounterpartyAccount().Bic() else None
                        self._buy_receiving_agent = '/NOSI/NDFS'
                    elif settle_curr == buy_curr:
                        self._buy_receiving_agent = flw.AcquirerAccount().Bic().Alias() if flw.AcquirerAccount() and flw.AcquirerAccount().Bic() else None
                        self._sell_receiving_agent = '/NOSI/NDFS'

        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acq_acc_cpty_acc_from_trade : %s"%str(e))

    def set_non_deliverable_indicator_from_trade(self):
        try:
            non_deliverable_indicator = 'N'
            trade = self.acm_obj.Trade()
            if trade:
                ins = trade.Instrument()
                if ins and ins.IsKindOf(acm.FFuture):
                    non_deliverable_indicator = 'Y'
            self._non_deliverable_indicator = non_deliverable_indicator
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_non_deliverable_indicator_from_trade: %s" % str(e))

    def set_non_deliverable_open_indicator_from_trade(self):
        try:
            ndf_open_indicator = 'N'
            trade = self.acm_obj.Trade()
            if trade:
                ins = trade.Instrument()
                if ins and ins.IsKindOf(acm.FFuture) and trade.Type() == "Normal":
                    ndf_open_indicator = 'Y'
            self._non_deliverable_open_indicator = ndf_open_indicator
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_non_deliverable_indicator_from_trade: %s" % str(e))

    def set_settlement_currency_from_trade(self):
        try:
            sett_curr = None
            trade = self.acm_obj.Trade()
            if trade:
                ins = trade.Instrument()
                if ins and ins.IsKindOf(acm.FFuture) and trade.Type() in ["Normal", 'Closing']:
                    sett_curr = ins.Currency().Name()
            self._settlement_currency = sett_curr
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_settlement_currency_from_trad: %s" % str(e))

    def set_valuation_date_from_trade(self):
        '''Returns terms and conditions as string'''
        trade = self.acm_obj.Trade()
        if trade:
            ins = trade.Instrument()
            if ins and ins.IsKindOf(acm.FFuture) and trade.Type() in ["Normal", "Closing"]:
                self._valuation_date = ins.ExpiryDate().split()[0]

    def set_settlement_rate_source_from_trade(self):
        ins = self.acm_obj.Trade().Instrument()
        cut_off = ''
        location = ''
        rate_source = ''
        if ins:
            fixing_source_party = ins.FixingSource()
            if fixing_source_party:
                cut_off = fixing_source_party.ExternalCutOff()
                location = fixing_source_party.City()
                for alias in fixing_source_party.Aliases():
                    if alias.Type().Name() == 'ISDASettlementSrc':
                        if alias.Alias():
                            rate_source = alias.Alias()

        if rate_source:
            self._settlement_rate_source = rate_source

            if rate_source != 'EMT00':
                if cut_off:
                    self._settlement_rate_source += '/' + str(cut_off)

                if location:
                    self._settlement_rate_source += '/' + location



# ------------------------------------------------------------------------------
    # Method to fetch data used in the Pairing and Matching attributes in the FParameter
    def SendersReference(self):
        return self._identifier

    def TypeOfOperation(self):
        return self._message_function

    def ScopeOfOperation(self):
        return self._scope_of_operation

    def CommonReference(self):
        return self._common_reference

    def BlockTradeIndicator(self):
        return self._block_trade_indicator

    def SplitSettlementIndicator(self):
        return self._split_settlement_indicator

    def FundOrBeneficiaryCustomer(self):
        return self._fund_or_beneficiary_customer

    def TermsAndConditions(self):
        return self._terms_and_conditions

    def TradeDate(self):
        return self._trade_date

    def ValueDate(self):
        return self._value_date

    def ExchangeRate(self):
        return self._exchange_rate

    def BuyCurrency(self):
        return self._buy_currency

    def BuyAmount(self):
        return self._buy_amount

    def BuyDeliveryAgent(self):
        return self._buy_delivery_agent

    def BuyIntermediary(self):
        return self._buy_intermediary

    def BuyReceivingAgent(self):
        return self._buy_receiving_agent

    def SellCurrency(self):
        return self._sell_currency

    def SellAmount(self):
        return self._sell_amount

    def SellDeliveryAgent(self):
        return self._sell_delivery_agent

    def SellIntermediary(self):
        return self._sell_intermediary

    def SellReceivingAgent(self):
        return self._sell_receiving_agent

    def SellBeneficiaryInstitution(self):
        return self._sell_beneficiary_institution

    def ContactInformation(self):
        return self._contact_information

    def DealingMethod(self):
        return self._dealing_method

    def DealingBranchAcquirer(self):
        return self._dealing_branch_acquirer

    def DealingBranchCounterParty(self):
        return self._dealing_branch_cpty

    def BrokerIdentification(self):
        return self._broker_identification

    def BrokerCommission(self):
        return self._broker_commission

    def CounterpartyReference(self):
        return self._counterparty_reference

    def BrokerReference(self):
        return self._broker_reference

    def SenderToReceiverInformation(self):
        return self._sender_receiver_information

    def NonDeliverableIndicator(self):
        return self._non_deliverable_indicator

    def NonDeliverableOpenIndicator(self):
        return self._non_deliverable_open_indicator

    def SettlementCurrency(self):
        return self._settlement_currency

    def SettlementRateSource(self):
        return self._settlement_rate_source

    def ValuationDate(self):
        return self._valuation_date


# +------------------------------------------------------------------------------------------+
# |             Getters to represent the real side of the incoming message                   |
# +------------------------------------------------------------------------------------------+

    def RealBuyCurrency(self):
        try:
            return str(self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.CurrencyAmount.value()[0:3])
        except Exception as e:
            notifier.INFO("Exception occurred in RealBuyCurrency : %s" % str(e))

    def RealBuyAmount(self):
        try:
            amt = str(self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.CurrencyAmount.value()[3:])
            return FSwiftMLUtils.swiftmt_to_float(amt)
        except Exception as e:
            notifier.INFO("Exception occurred in RealBuyAmount : %s" % str(e))

    def RealBuyDeliveryAgent(self):
        try:
            agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.DeliveryAgent_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.DeliveryAgent_A else None
            if agent:
                agent = str(self.get_party_typeA(agent))

            return  agent
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealBuyDeliveryAgent : %s"%str(e))


    def RealBuyIntermediary(self):
        try:
            intermediary = self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.Intermediary_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.Intermediary_A else None
            if intermediary:
                intermediary = str(self.get_party_typeA(intermediary))

            return intermediary
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealBuyIntermediary : %s"%str(e))

    def RealBuyReceivingAgent(self):
        try:
            agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB1_AmountBought.ReceivingAgent_A else None
            if agent:
                agent = str(self.get_party_typeA(agent))

            return agent
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealBuyReceivingAgent : %s"%str(e))


    def RealSellCurrency(self):
        try:
            currency = str(self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.CurrencyAmount.value()[0:3])
            return currency
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealSellCurrency : %s"%str(e))

    def RealSellAmount(self):
        try:
            amount = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.CurrencyAmount.value()[3:]
            amount = FSwiftMLUtils.swiftmt_to_float(amount)
            return amount
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealSellAmount : %s"%str(e))

    def RealSellDeliveryAgent(self):
        try:
            agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.DeliveryAgent_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.DeliveryAgent_A else None
            if agent:
                agent = str(self.get_party_typeA(agent))
            return agent
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealSellDeliveryAgent : %s"%str(e))


    def RealSellIntermediary(self):
        try:
            intermediary = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.Intermediary_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.Intermediary_A else None
            if intermediary:
                intermediary = str(self.get_party_typeA(intermediary))
            return intermediary
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealSellIntermediary : %s"%str(e))

    def RealSellReceivingAgent(self):
        try:
            agent = self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_A.value() if self.python_object.SequenceB_TransactionDetails.SubSequenceB2_AmountSold.ReceivingAgent_A else None
            if agent:
                agent = str(self.get_party_typeA(agent))
            return agent
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealSellReceivingAgent : %s"%str(e))


    @staticmethod
    def GetColumnMetaData():
        column_metadata = {
            'NonDeliverableIndicator': {'THEIRS_SWIFT_TAG': '17F', 'OURS_SWIFT_TAG': '17F',
                                        'SEQUENCE': 'General Information', 'COLOR': ''},
            'NonDeliverableOpenIndicator': {'THEIRS_SWIFT_TAG': '170', 'OURS_SWIFT_TAG': '170',
                                            'SEQUENCE': 'General Information', 'COLOR': ''},
            'SettlementCurrency': {'THEIRS_SWIFT_TAG': '32E', 'OURS_SWIFT_TAG': '32E',
                                   'SEQUENCE': 'General Information', 'COLOR': ''},
            'SettlementRateSource': {'THEIRS_SWIFT_TAG': '14S', 'OURS_SWIFT_TAG': '14S',
                                     'SEQUENCE': 'General Information', 'COLOR': ''},
            'ValuationDate': {'THEIRS_SWIFT_TAG': '30U', 'OURS_SWIFT_TAG': '30U', 'SEQUENCE': 'General Information',
                              'COLOR': ''},

            'SendersReference': {'THEIRS_SWIFT_TAG' : '20', 'OURS_SWIFT_TAG' : '20', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'RelatedReference': {'THEIRS_SWIFT_TAG' : '21', 'OURS_SWIFT_TAG' : '21', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'TypeOfOperation': {'THEIRS_SWIFT_TAG' : '22A', 'OURS_SWIFT_TAG' : '22A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'ScopeOfOperation': {'THEIRS_SWIFT_TAG' : '94A', 'OURS_SWIFT_TAG' : '94A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'CommonReference': {'THEIRS_SWIFT_TAG' : '22C', 'OURS_SWIFT_TAG' : '22C', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'BlockTradeIndicator': {'THEIRS_SWIFT_TAG' : '17T', 'OURS_SWIFT_TAG' : '17T', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'SplitSettlementIndicator': {'THEIRS_SWIFT_TAG' : '17U', 'OURS_SWIFT_TAG' : '17U', 'SEQUENCE': 'General Information', 'SHORT_NAME': 'Split', 'COLOR': ''},
            'Acquirer': {'REAL_GETTER' : 'RealAcquirer', 'REAL_SWIFT_TAG' : '82A', 'THEIRS_SWIFT_TAG' : '87A', 'OURS_SWIFT_TAG' : '82A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'Counterparty': {'REAL_GETTER' : 'RealCounterparty', 'REAL_SWIFT_TAG' : '87A', 'THEIRS_SWIFT_TAG' : '82A', 'OURS_SWIFT_TAG' : '87A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'FundOrBeneficiaryCustomer': {'THEIRS_SWIFT_TAG' : '83A', 'OURS_SWIFT_TAG' : '83A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'TermsAndConditions': {'THEIRS_SWIFT_TAG' : '77D', 'OURS_SWIFT_TAG' : '77D', 'SEQUENCE': 'General Information', 'COLOR': ''},

            'TradeDate': {'THEIRS_SWIFT_TAG' : '30T', 'OURS_SWIFT_TAG' : '30T', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'ValueDate': {'THEIRS_SWIFT_TAG' : '30V', 'OURS_SWIFT_TAG' : '30V', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'ExchangeRate': {'THEIRS_SWIFT_TAG' : '36', 'OURS_SWIFT_TAG' : '36', 'SEQUENCE': 'Transaction Details', 'COLOR': '','FORMAT':'SwiftFiveDecimalPrecision'},

            #Amount Bought
            'BuyCurrency': {'REAL_GETTER' : 'RealBuyCurrency', 'REAL_SWIFT_TAG' : '32B', 'THEIRS_SWIFT_TAG' : '33B', 'OURS_SWIFT_TAG' : '32B', 'SEQUENCE': 'Amount Bought', 'COLOR': ''},
            'BuyAmount': {'REAL_GETTER' : 'RealBuyAmount', 'REAL_SWIFT_TAG' : '32B','THEIRS_SWIFT_TAG' : '33B', 'OURS_SWIFT_TAG' : '32B', 'SEQUENCE': 'Amount Bought', 'COLOR': '','FORMAT':'NumDefault'},
            'BuyDeliveryAgent': {'REAL_GETTER' : 'RealBuyDeliveryAgent', 'REAL_SWIFT_TAG' : '53A', 'THEIRS_SWIFT_TAG' : '53A', 'OURS_SWIFT_TAG' : '53A', 'SEQUENCE': 'Amount Bought', 'COLOR': ''},
            'BuyIntermediary': {'REAL_GETTER' : 'RealBuyIntermediary', 'REAL_SWIFT_TAG' : '56A', 'THEIRS_SWIFT_TAG' : '56A', 'OURS_SWIFT_TAG' : '56A', 'SEQUENCE': 'Amount Bought', 'COLOR': ''},
            'BuyReceivingAgent': {'REAL_GETTER' : 'RealBuyReceivingAgent', 'REAL_SWIFT_TAG' : '57A', 'THEIRS_SWIFT_TAG' : '57A', 'OURS_SWIFT_TAG' : '57A', 'SEQUENCE': 'Amount Bought', 'COLOR': ''},

            #Amount Sold
            'SellCurrency': {'REAL_GETTER' : 'RealSellCurrency', 'REAL_SWIFT_TAG' : '33B','THEIRS_SWIFT_TAG' : '32B', 'OURS_SWIFT_TAG' : '33B', 'SEQUENCE': 'Amount Sold', 'COLOR': ''},
            'SellAmount': {'REAL_GETTER' : 'RealSellAmount', 'REAL_SWIFT_TAG' : '33B','THEIRS_SWIFT_TAG' : '32B', 'OURS_SWIFT_TAG' : '33B', 'SEQUENCE': 'Amount Sold', 'COLOR': '','FORMAT':'NumDefault'},
            'SellDeliveryAgent': {'REAL_GETTER' : 'RealSellDeliveryAgent', 'REAL_SWIFT_TAG' : '53A', 'THEIRS_SWIFT_TAG' : '53A', 'OURS_SWIFT_TAG' : '53A', 'SEQUENCE': 'Amount Sold', 'COLOR': ''},
            'SellIntermediary': {'REAL_GETTER' : 'RealSellIntermediary', 'REAL_SWIFT_TAG' : '56A', 'THEIRS_SWIFT_TAG' : '56A', 'OURS_SWIFT_TAG' : '56A', 'SEQUENCE': 'Amount Sold', 'COLOR': ''},
            'SellReceivingAgent': {'REAL_GETTER' : 'RealSellReceivingAgent', 'REAL_SWIFT_TAG' : '57A', 'THEIRS_SWIFT_TAG' : '57A', 'OURS_SWIFT_TAG' : '57A', 'SEQUENCE': 'Amount Sold', 'COLOR': ''},
            'SellBeneficiaryInstitution': {'THEIRS_SWIFT_TAG' : '58A', 'OURS_SWIFT_TAG' : '58A', 'SEQUENCE': 'Amount Sold', 'COLOR': ''},

            'ContactInformation': {'THEIRS_SWIFT_TAG' : '29A', 'OURS_SWIFT_TAG' : '29A', 'SEQUENCE': 'Optional General Information', 'COLOR': ''},
            'DealingMethod': {'THEIRS_SWIFT_TAG' : '24D', 'OURS_SWIFT_TAG' : '24D', 'SEQUENCE': 'Optional General Information', 'COLOR': ''},
            'DealingBranchAcquirer': {'THEIRS_SWIFT_TAG' : '84A', 'OURS_SWIFT_TAG' : '84A', 'SEQUENCE': 'Optional General Information', 'COLOR': ''},
            'DealingBranchCounterParty': {'THEIRS_SWIFT_TAG' : '85A', 'OURS_SWIFT_TAG' : '85A', 'SEQUENCE': 'Optional General Information', 'COLOR': ''},
            'BrokerIdentification': {'THEIRS_SWIFT_TAG' : '88A', 'OURS_SWIFT_TAG' : '88A', 'SEQUENCE': 'Optional General Information', 'COLOR': ''},
            'BrokerCommission': {'THEIRS_SWIFT_TAG' : '71F', 'OURS_SWIFT_TAG' : '71F', 'SEQUENCE': 'Optional General Information', 'COLOR': ''},
            'CounterpartyReference': {'THEIRS_SWIFT_TAG' : '26H', 'OURS_SWIFT_TAG' : '26H', 'SEQUENCE': 'Optional General Information', 'COLOR': ''},
            'BrokerReference': {'THEIRS_SWIFT_TAG' : '21G', 'OURS_SWIFT_TAG' : '21G', 'SEQUENCE': 'Optional General Information', 'COLOR': ''},
            'SenderToReceiverInformation': {'THEIRS_SWIFT_TAG' : '72', 'OURS_SWIFT_TAG' : '72', 'SEQUENCE': 'Optional General Information', 'COLOR': ''},

            }
        return column_metadata

    @staticmethod
    def GetColumnNamePrefix():
        return 'MT300'
