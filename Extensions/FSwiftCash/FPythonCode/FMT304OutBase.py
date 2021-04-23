"""----------------------------------------------------------------------------
MODULE:
    FMT304OutBase

DESCRIPTION:
    This module provides the base class for the FMT304 outgoing implementation

CLASS:
    FMT304Base

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
    1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
    2. This module is not customizable.
    3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""

import FSwiftMLUtils
import FSwiftWriterMessageHeader
import MT304
import acm
import FSwiftWriterLogger
import FCashOutUtils
import FSwiftConfirmationUtils
import FSwiftWriterMTFactory
import FSwiftWriterUtils
from FCashOutBase import FCashOutBase
from FSwiftWriterEngine import validate_with


notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')


class FMT304Base(FCashOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = "MT304"
        super(FMT304Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    def _message_sequences(self):
        self.swift_obj.SequenceA_GeneralInformation = MT304.MT304_SequenceA_GeneralInformation()
        self.swift_obj.SequenceA_GeneralInformation.swiftTag = "15A"
        self.swift_obj.SequenceA_GeneralInformation.formatTag = "False"
        self.swift_obj.SequenceB_ForexTransactionDetails = MT304.MT304_SequenceB_ForexTransactionDetails()
        self.swift_obj.SequenceB_ForexTransactionDetails.swiftTag = "15B"
        self.swift_obj.SequenceB_ForexTransactionDetails.formatTag = "False"
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought = MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought()
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold = MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold()

        # Setting Sequence D Accounting Information Block
        self.is_seq_d = self.__set_optional_seq_d()


    def handle_cancellation_message(self, swift_message_obj, msg_typ, acm_object):
        """ Creates a python object from parent settlement swift message.
            Assign that python object to fmt object.
            Set changed values only on fmt object.
        """
        try:
            canc_message = ''
            self.swift_obj = None
            pyobj = FSwiftWriterUtils.create_pyobj_from_swift_msg(swift_message_obj)
            if pyobj:
                self.swift_obj = pyobj

                # Setting related reference value (Tag 21) on the fmt object
                ref_val = pyobj.SequenceA_GeneralInformation.SendersReference.value()

                self.swift_obj.SequenceA_GeneralInformation.RelatedReference = ref_val
                self.swift_obj.SequenceA_GeneralInformation.RelatedReference.swiftTag = "21"

                # Setting the transaction reference number value (Tag 20) on the fmt object
                getter_value = self.senders_reference_20()
                formatter_value = self._format_senders_reference_20(getter_value)
                validated_value = self._validate_senders_reference_20(formatter_value)
                self._set_senders_reference_20(validated_value)

                # Setting type of operation value (Tag 22)
                old_val = pyobj.SequenceA_GeneralInformation.TypeOfOperation.value()
                if 'NEWT' in old_val:
                    val = old_val.replace('NEWT', 'CANC')
                self.swift_obj.SequenceA_GeneralInformation.TypeOfOperation = val
                self.swift_obj.SequenceA_GeneralInformation.TypeOfOperation.swiftTag = "22A"

                mt_message = FSwiftWriterUtils.create_swift_msg_from_pyobj(self.swift_obj)

                fmt_swift_header_class_obj = FSwiftWriterMTFactory.FSwiftWriterMTFactory.create_fmt_header_object(self.swift_message_type, self.acm_obj, mt_message, None)
                canc_message = fmt_swift_header_class_obj.swift_message_with_header()


        except Exception as e:
            raise e
        return canc_message, self.swift_obj


    # Methods to fetch data from the swift message

    # ------------------ senders_reference -----------------------
    # getter
    def senders_reference_20(self):
        """ Expected return type : a string containing senders's reference"""
        senders_reference = str(self.acm_obj.Oid())
        return senders_reference

    # formatter
    def _format_senders_reference_20(self, val):
        """ Formats the value provided by getter method """
        if val:
            sett_obj = acm.FSettlement[str(val)]
            val = "%s-%s-%s" % (FCashOutUtils.get_settlement_reference_prefix(), str(val), str(FCashOutUtils.get_message_version_number(sett_obj)))
        return val

    # validator
    @validate_with(MT304.MT304_SequenceA_GeneralInformation_20_Type)
    def _validate_senders_reference_20(self, val):
        """ Validates the value provided by formatter method """
        FCashOutUtils.validate_slash_and_double_slash(val, "Sender's Reference")
        return val

    # setter
    def _set_senders_reference_20(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceA_GeneralInformation.SendersReference = val
        self.swift_obj.SequenceA_GeneralInformation.SendersReference.swiftTag = "20"

    # ------------------ related_reference -----------------------

    # getter
    def related_reference_21(self):
        """ Returns 'NEW' or related confirmation object"""
        if FSwiftWriterUtils.get_type_of_operation(self.acm_obj) == 'CANC':
            return FCashOutUtils.get_related_settlement(self.acm_obj)


    # formatter
    def _format_related_reference_21(self, val):
        """ Formats the value provided by getter method """
        if val:
            related_conf = val
            related_reference = '%s-%s-%s' % (FCashOutUtils.get_settlement_reference_prefix(), str(val.Oid()), str(FCashOutUtils.get_version_for_sent_message_on(related_conf, 'MT304')))
            return related_reference


    # validator
    @validate_with(MT304.MT304_SequenceA_GeneralInformation_21_Type)
    def _validate_related_reference_21(self, val):
        """ Validates the value provided by formatter method """
        FCashOutUtils.validate_slash_and_double_slash(val, "Related Reference")
        return val

    # setter
    def _set_related_reference_21(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceA_GeneralInformation.RelatedReference = val
        self.swift_obj.SequenceA_GeneralInformation.RelatedReference.swiftTag = "21"


    # ------------------ type_of_operation -----------------------
    # getter
    def type_of_operation_22A(self):
        """ Returns type of operation code as string  """
        return 'NEWT'

    # formatter
    def _format_type_of_operation_22A(self, val):
        """ Formats the value provided by getter method """
        return val

    @validate_with(MT304.MT304_SequenceA_GeneralInformation_22A_Type)
    def _validate_type_of_operation_22A(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _set_type_of_operation_22A(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceA_GeneralInformation.TypeOfOperation = val
        self.swift_obj.SequenceA_GeneralInformation.TypeOfOperation.swiftTag = "22A"


    # -------------------- ScopeOfOperation --------------------------

    # getter
    def scope_of_operation_94A(self):
        """ Returns string based upon type of trade """
        val = ''
        if self.acm_obj.Trade().IsFxSpot():
            val = "ASET"
        elif self.acm_obj.Trade().IsFxForward():
            val = "AFWD"
        return val

    # formatter
    def _format_scope_of_operation_94A(self, val):
        """ Formats the value provided by getter method """
        return val

    # validator
    @validate_with(MT304.MT304_SequenceA_GeneralInformation_94A_Type)
    def _validate_scope_of_operation_94A(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _set_scope_of_operation_94A(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceA_GeneralInformation.ScopeOfOperation = val
        self.swift_obj.SequenceA_GeneralInformation.ScopeOfOperation.swiftTag = "94A"

    # --------------- OpenIndicator -----------------

    # getter
    def open_indicator_17O(self):
        """ Returns string Y/N denoting whether the trade is open/closing"""
        indicator = None
        if self.acm_obj.Trade().Type() == 'Normal':
            indicator = 'Y'
        elif self.acm_obj.Trade().Type() == 'Closing':
            indicator = 'N'

        return indicator

    # formatter
    def _format_open_indicator_17O(self, val):
        """ Formats the value provided by getter method """
        return val

    # validator
    @validate_with(MT304.MT304_SequenceA_GeneralInformation_17O_Type)
    def _validate_open_indicator_17O(self, val):
        """ Validates the value provided by formatter method """
        return val

    # check condition
    def _check_condition_set_open_indicator_17O(self):
        """ Checks conditional presence set_open_indicator_17O"""
        indicator = False
        if self.acm_obj.Trade().IsFxForward():
            indicator = True
        return indicator

    # setter
    def _set_open_indicator_17O(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceA_GeneralInformation.OpenIndicator = val
        self.swift_obj.SequenceA_GeneralInformation.OpenIndicator.swiftTag = "17O"

    # --------------- FinalCloseIndicator -----------------

    # getter
    def final_close_indicator_17F(self):
        """ Returns string Y/N denoting whether the trade is final closing trade """
        indicator = None
        if self.acm_obj.Trade().Type() == 'Closing':
            if self.acm_obj.Trade().RemainingNominal():
                indicator = 'N'
            else:
                indicator = 'Y'
        return indicator

    # formatter
    def _format_final_close_indicator_17F(self, val):
        """ Formats the value provided by getter method """
        return val

    # validator
    @validate_with(MT304.MT304_SequenceA_GeneralInformation_17F_Type)
    def _validate_final_close_indicator_17F(self, val):
        """ Validates the value provided by formatter method """
        return val

    # check condition
    def _check_condition_set_final_close_indicator_17F(self):
        """ Checks conditional presence for _set_final_close_indicator_17F"""
        indicator = False
        if self.acm_obj.Trade().IsFxForward():
            indicator = True
        return indicator

    # setter
    def _set_final_close_indicator_17F(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceA_GeneralInformation.FinalCloseIndicator = val
        self.swift_obj.SequenceA_GeneralInformation.FinalCloseIndicator.swiftTag = "17F"


     # --------------- NetSettlementIndicator -----------------

    # getter
    def net_settlement_indicator_17N(self):
        """ Returns string 'N' as netting is not supported """
        indicator = 'N'
        return indicator

    # formatter
    def _format_net_settlement_indicator_17N(self, val):
        """ Formats the value provided by getter method """
        return val

    # validator
    @validate_with(MT304.MT304_SequenceA_GeneralInformation_17N_Type)
    def _validate_net_settlement_indicator_17N(self, val):
        """ Validates the value provided by formatter method """
        return val

    # check condition
    def _check_condition_set_net_settlement_indicator_17N(self):
        """ Checks conditional presence for _set_net_settlement_indicator_17N"""
        indicator = False
        if self.acm_obj.Trade().IsFxForward():
            indicator = True
        return indicator

    # setter
    def _set_net_settlement_indicator_17N(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceA_GeneralInformation.NetSettlementIndicator = val
        self.swift_obj.SequenceA_GeneralInformation.NetSettlementIndicator.swiftTag = "17N"

    # -------------------- Option -------------------
    #option_getter
    def get_fund_option(self):
        """ Returns default option if override is not provided """
        option = "J"
        party_details = FCashOutUtils.get_party_a_details(self.acm_obj)
        if FCashOutUtils.get_bic(party_details):
            option = 'A'
        else:
            option = 'J'
        return option

    # option setter
    def _set_OPTION_fund(self):
        """ Returns getter name as string like 'fund_83A',  'fund_83J' """
        fund_option = self.get_fund_option()
        if fund_option == "A":
            getter_name = 'fund_83A'
        elif fund_option == "J":
            getter_name = 'fund_83J'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type, str(fund_option), 'Fund_83a'))
            getter_name = 'fund_83A'
        return getter_name

    # getter
    def fund_83A(self):
        """ Returns dictionary consisting fund party details """
        val = FCashOutUtils.get_party_a_details(self.acm_obj)
        return val

    # formatter
    def _format_fund_83A(self, val):
        """ Formats the value provided by getter method """
        bic = val.get('BIC')
        if bic:
            val = str(bic)
            return val


    # validator
    @validate_with(MT304.MT304_SequenceA_GeneralInformation_83A_Type)
    def _validate_fund_83A(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _setfund_83A(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceA_GeneralInformation.Fund_A = val
        self.swift_obj.SequenceA_GeneralInformation.Fund_A.swiftTag = "83A"


    # getter
    def fund_83J(self):
        """ Returns dictionary consisting fund party details """
        val = FCashOutUtils.get_party_a_details(self.acm_obj)
        return val

    # formatter
    def _format_fund_83J(self, val):
        """ Formats the value provided by getter method """
        return self._format_Option_J(val)


    # validator
    @validate_with(MT304.MT304_SequenceA_GeneralInformation_83J_Type)
    def _validate_fund_83J(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _setfund_83J(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceA_GeneralInformation.Fund_J = val
        self.swift_obj.SequenceA_GeneralInformation.Fund_J.swiftTag = "83J"


    # --------------------fund_manager Option -------------------
    # option_getter
    def get_fund_manager_option(self):
        """ Returns default option if override is not provided """
        option = "J"
        party_details = self.fund_manager_82A()
        if party_details:
            if FCashOutUtils.get_bic(party_details):
                option = 'A'
            else:
                option = 'J'
        return option


    # option setter
    def _set_OPTION_fund_manager(self):
        """ Returns getter name as string like 'fund_manager_82A',  'fund_manager_82J' """
        fund_option = self.get_fund_manager_option()
        if fund_option == "A":
            getter_name = 'fund_manager_82A'
        elif fund_option == "J":
            getter_name = 'fund_manager_82J'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % ( self.swift_message_type, str(fund_option), 'FundManager_a'))
            getter_name = 'fund_manager_82A'
        return getter_name

    # getter
    def fund_manager_82A(self):
        """ Returns dictionary with fund manager party details """
        val = ''
        try:
            custom_value = self.fund_manager()
            if custom_value:
                val = FCashOutUtils.get_fund_manager_details(custom_value)
            return val
        except NotImplementedError:
            notifier.WARN("Implement custom function fund_manager() in FMT304Out returning value for FundManager as it is mandatory in fund_manager_82A")


    # formatter
    def _format_fund_manager_82A(self, val):
        """ Formats the value provided by getter method """
        bic = val.get('BIC')
        if bic:
            val = str(bic)
            return val

    # validator
    @validate_with(MT304.MT304_SequenceA_GeneralInformation_82A_Type)
    def _validate_fund_manager_82A(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _setfund_manager_82A(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceA_GeneralInformation.FundManager_A = val
        self.swift_obj.SequenceA_GeneralInformation.FundManager_A.swiftTag = "82A"



    # getter
    def fund_manager_82J(self):
        """ Returns dictionary with fund manager party details """
        val = ''
        try:
            custom_value = self.fund_manager()
            if custom_value:
                val = FCashOutUtils.get_fund_manager_details(custom_value)
            return val
        except NotImplementedError:
            notifier.WARN("Implement custom function fund_manager() in FMT304Out returning value for FundManager as it is mandatory in fund_manager_82J")

    # formatter
    def _format_fund_manager_82J(self, val):
        """ Formats the value provided by getter method """
        return self._format_Option_J(val)

    # validator
    @validate_with(MT304.MT304_SequenceA_GeneralInformation_82J_Type)
    def _validate_fund_manager_82J(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _setfund_manager_82J(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceA_GeneralInformation.FundManager_J = val
        self.swift_obj.SequenceA_GeneralInformation.FundManager_J.swiftTag = "82J"

    # -------------------- ExecutingBroker -------------------
    # option getter
    def get_executing_broker_option(self):
        """ Returns default option if override is not provided """
        option = "J"
        party_details = self.executing_broker_87A()
        if party_details:
            if FCashOutUtils.get_bic(party_details):
                option = 'A'
            else:
                option = "J"
        return option

    # option setter
    def _set_OPTION_executing_broker(self):
        """ Returns getter name as string like 'ExecutingBroker_87A', 'ExecutingBroker_87J' """
        executing_broker_option = self.get_executing_broker_option()
        getter_name = 'executing_broker_87A'
        if executing_broker_option == "A":
            getter_name = 'executing_broker_87A'
        elif executing_broker_option == "J":
            getter_name = 'executing_broker_87J'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,  str(executing_broker),  'ExecutingBroker_87a'))
        return getter_name

    # getter
    def executing_broker_87A(self):
        """ Returns dictionary with executing broker party details """
        try:
            val = ''
            if not FCashOutUtils.get_executing_broker(self.acm_obj):
                custom_value = self.executing_broker()
            else:
                custom_value = FCashOutUtils.get_executing_broker(self.acm_obj)
            if custom_value:
                val = FCashOutUtils.get_executing_broker_details(custom_value)
                return val

        except NotImplementedError:
            notifier.WARN("Implement custom function executing_broker() in FMT304Out returning value for ExecutingBroker as it is mandatory in executing_broker_87A")

    # formatter
    def _format_executing_broker_87A(self, val):
        """ Formats the value provided by getter method """
        if val:
            bic = val.get('BIC')
            if bic:
                val = str(bic)
                return val

    # validator
    @validate_with(MT304.MT304_SequenceA_GeneralInformation_87A_Type)
    def _validate_executing_broker_87A(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _setexecuting_broker_87A(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceA_GeneralInformation.ExecutingBroker_A = val
        self.swift_obj.SequenceA_GeneralInformation.ExecutingBroker_A.swiftTag = "87A"



    # getter
    def executing_broker_87J(self):
        """ Returns dictionary with executing broker party details """
        try:
            val = ''
            if not FCashOutUtils.get_executing_broker(self.acm_obj):
                custom_value = self.executing_broker()
            else:
                custom_value = FCashOutUtils.get_executing_broker(self.acm_obj)
            if custom_value:
                val = FCashOutUtils.get_executing_broker_details(custom_value)
            return val

        except NotImplementedError:
            notifier.WARN("Implement custom function executing_broker() in FMT304Out returning value for ExecutingBroker as it is mandatory in executing_broker_87J")

    # formatter
    def _format_executing_broker_87J(self, val):
        """ Formats the value provided by getter method """
        return self._format_Option_J(val)

    # validator
    @validate_with(MT304.MT304_SequenceA_GeneralInformation_87J_Type)
    def _validate_executing_broker_87J(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _setexecuting_broker_87J(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceA_GeneralInformation.ExecutingBroker_J = val
        self.swift_obj.SequenceA_GeneralInformation.ExecutingBroker_J.swiftTag = "87J"

    # -------------------------- TradeDate --------------------------------------------

    # getter
    def trade_date_30T(self):
        """ Returns trade date as a string """
        trade_date = FCashOutUtils.get_trade_date(self.acm_obj)
        return trade_date

    # formatter
    def _format_trade_date_30T(self, val):
        """ Formats the value provided by getter method """
        if val:
            date_format = '%Y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)

            return str(val)

    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_30T_Type)
    def _validate_trade_date_30T(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _set_trade_date_30T(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.TradeDate = val
        self.swift_obj.SequenceB_ForexTransactionDetails.TradeDate.swiftTag = "30T"


    # ----------------------------- ValueDate -----------------------------------------
    # getter
    def value_date_30V(self):
        """ Returns value date as a string """
        value_day = self.acm_obj.Trade().ValueDay()
        return value_day

    # formatter
    def _format_value_date_30V(self, val):
        """ Formats the value provided by getter method """
        if val:
            date_format = '%Y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)
            return val

    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_30V_Type)
    def _validate_value_date_30V(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _set_value_date_30V(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.ValueDate = val
        self.swift_obj.SequenceB_ForexTransactionDetails.ValueDate.swiftTag = "30V"


    # ------------------------------ ExchangeRate ----------------------------------------
    # getter
    def exchange_rate_36(self):
        """ Returns exchange rate as a string """
        val = FCashOutUtils.get_exchange_rate(self.acm_obj)
        return val

    # formatter
    def _format_exchange_rate_36(self, val):
        """ Formats the value provided by getter method """
        if val:
            strike_currency = FCashOutUtils.base_currency(self.acm_obj)
            val = FCashOutUtils.apply_currency_precision(strike_currency, float(val))
            exchange_rate = FSwiftMLUtils.float_to_swiftmt(str(val))
            return exchange_rate


    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_36_Type)
    def _validate_exchange_rate_36(self, val):
        """ Validates the value provided by formatter method """
        FCashOutUtils.validateAmount(val, 12, "Exchange Rate")
        return val

    # setter
    def _set_exchange_rate_36(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.ExchangeRate = val
        self.swift_obj.SequenceB_ForexTransactionDetails.ExchangeRate.swiftTag = "36"


    # -------------------------------- currency_amount_bought  --------------------------------------

    def currency_amount_bought_32B(self):
        """ Returns dictionary consisting of buy_amount and currency as keys with their respective values """
        val_dict = {}
        amount_bought = ''
        currency = ''

        val_dict['BUY_AMOUNT'] = FCashOutUtils.get_buy_amount(self.acm_obj)
        val_dict['BUY_CURRENCY'] = FCashOutUtils.get_buy_currency(self.acm_obj)


        return val_dict

    # formatter
    def _format_currency_amount_bought_32B(self, val_dict):
        """ Formats the value provided by getter method """
        buy_amount = val_dict.get('BUY_AMOUNT')
        buy_currency = val_dict.get('BUY_CURRENCY')
        if buy_amount and buy_currency:
            buy_amount = FCashOutUtils.apply_currency_precision(buy_currency, float(buy_amount))
            val = str(buy_currency) + str(FSwiftMLUtils.float_to_swiftmt(str(buy_amount)))
            return val

    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type)
    def _validate_currency_amount_bought_32B(self, val):
        """ Validates the value provided by formatter method """
        FCashOutUtils.validate_currency_amount(val, "Currency Amount Bought")
        amount = FCashOutUtils.get_amount_from_currency_amount(val)
        FCashOutUtils.validateAmount(amount.replace('.', ','), 15, "Currency Amount Bought")
        return val

    # setter
    def _set_currency_amount_bought_32B(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.CurrencyAmountBought = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.CurrencyAmountBought.swiftTag = "32B"


    # ---------------------------------- buy_delivery_agent ------------------------------------
    def get_buy_delivery_agent_option(self):
        """ Returns default option if override is not provided """
        party_details = FCashOutUtils.get_counterparty_delivery_agent_details(self.acm_obj)
        bic = FCashOutUtils.get_bic(party_details)
        option = "J"
        if bic:
            option = "A"
        else:
            option = "J"
        return option

    # option setter
    def _set_OPTION_buy_delivery_agent(self):
        """ Returns getter name as string like 'delivery_agent_53A', 'delivery_agent_53D', 'delivery_agent_53J' """

        buy_delivery_agent_option = self.get_buy_delivery_agent_option()
        getter_name = 'buy_delivery_agent_53A'
        if buy_delivery_agent_option == "A":
            getter_name = 'buy_delivery_agent_53A'
        elif buy_delivery_agent_option == "J":
            getter_name = 'buy_delivery_agent_53J'
        else:
            notifier.WARN(
                "%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,  str(fund_option), 'delivery_agent_53a'))



        return getter_name

    # getter
    def buy_delivery_agent_53A(self):
        """ Returns dictionary consisting of delivery agent party details """
        return FCashOutUtils.get_counterparty_delivery_agent_details(self.acm_obj)

    # formatter
    def _format_buy_delivery_agent_53A(self, val):
        """ Formats the value provided by getter method """
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val


    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type)
    def _validate_buy_delivery_agent_53A(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _setbuy_delivery_agent_53A(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.DeliveryAgent_A = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.DeliveryAgent_A.swiftTag = "53A"



    # getter
    def buy_delivery_agent_53J(self):
        """ Returns dictionary consisting of delivery agent party details """
        return FCashOutUtils.get_counterparty_delivery_agent_details(self.acm_obj)

    # formatter
    def _format_buy_delivery_agent_53J(self, val):
        """ Formats the value provided by getter method """
        return self._format_Option_J(val)

    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type)
    def _validate_buy_delivery_agent_53J(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _setbuy_delivery_agent_53J(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.DeliveryAgent_J = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.DeliveryAgent_J.swiftTag = "53J"


    # ----------------------------------------------------------------------

    def get_buy_intermediary_option(self):
        """ Returns default option if override is not provided """
        party_details = FCashOutUtils.get_acquirer_intermediary_details(self.acm_obj)
        option = "J"
        if FCashOutUtils.get_bic(party_details):
            option = "A"
        else:
            option = "J"
        return option

    # option setter
    def _set_OPTION_buy_intermediary(self):
        #Returns getter name as string like 'buy_intermediary_56A', 'buy_intermediary_56D', 'buy_intermediary_56J'

        buy_intermediary_option = self.get_buy_intermediary_option()

        getter_name = 'buy_intermediary_56A'
        if buy_intermediary_option == "A":
            getter_name = 'buy_intermediary_56A'
        elif buy_intermediary_option == "J":
            getter_name = 'buy_intermediary_56J'
        else:
            notifier.WARN(
                "%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type, str(fund_option), 'intermediary_56a'))
        return getter_name

    # getter
    def buy_intermediary_56A(self):
        """Returns dictionary consisting of intermediary party details """
        values_dict = FCashOutUtils.get_acquirer_intermediary_details(self.acm_obj)
        return values_dict

    # formatter
    def _format_buy_intermediary_56A(self, val):
        """ Formats the value provided by getter method """
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type)
    def _validate_buy_intermediary_56A(self, val):
        """ Validates the value provided by formatter method """
        return val


    # setter
    def _setbuy_intermediary_56A(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.Intermediary_A = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.Intermediary_A.swiftTag = "56A"


    # getter
    def buy_intermediary_56J(self):
        """ Returns dictionary consisting of intermediary party details """
        values_dict = FCashOutUtils.get_acquirer_intermediary_details(self.acm_obj)

        return values_dict

    # formatter
    def _format_buy_intermediary_56J(self, val):
        """Formats the value provided by getter method """
        return self._format_Option_J(val)

    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type)
    def _validate_buy_intermediary_56J(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _setbuy_intermediary_56J(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.Intermediary_J = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.Intermediary_J.swiftTag = "56J"

    # ----------------------------------------------------------------------
    def get_buy_receiving_agent_option(self):
        """ Returns default option if override is not provided """
        party_details = FCashOutUtils.get_acquirer_receiving_agent_details(self.acm_obj)
        option = "J"
        if FCashOutUtils.get_bic(party_details):
            option = "A"
        else:
            option = "J"
        return option

    # setter
    def _set_OPTION_buy_receiving_agent(self):
        buy_receiving_agent_option = self.get_buy_receiving_agent_option()
        getter_name = 'buy_receiving_agent_57A'

        if buy_receiving_agent_option == "A":
            getter_name = 'buy_receiving_agent_57A'
        elif buy_receiving_agent_option == "J":
            getter_name = 'buy_receiving_agent_57J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % ( str(buy_receiving_agent_option), 'BuyReceivingAgent_57a'))

        return getter_name

    # getter
    def buy_receiving_agent_57A(self):
        """ Returns dictionary with keys 'ACCOUNT', 'BIC' and their corresponding values"""
        return FCashOutUtils.get_acquirer_receiving_agent_details(self.acm_obj)

    # formatter
    def _format_buy_receiving_agent_57A(self, val):
        """ Formats the value provided by getter method """
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val

    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type)
    def _validate_buy_receiving_agent_57A(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _setbuy_receiving_agent_57A(self, val):
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.ReceivingAgent_A = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.ReceivingAgent_A.swiftTag = "57A"


    # getter
    def buy_receiving_agent_57J(self):
        """ Returns dictionary with keys 'NAME', 'ADDRESS', 'ACCOUNT' and their corresponding values """
        return FCashOutUtils.get_acquirer_receiving_agent_details(self.acm_obj)

    # formatter
    def _format_buy_receiving_agent_57J(self, val):
        """ Formats the value provided by getter method """
        return self._format_Option_J(val)


    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type)
    def _validate_buy_receiving_agent_57J(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _setbuy_receiving_agent_57J(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.ReceivingAgent_J = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB1_AmountBought.ReceivingAgent_J.swiftTag = "57J"


    # ------------------ currency_amount_sold_details -----------------------

    # getter
    def currency_amount_sold_33B(self):
        """ Returns dictionary with keys 'SELL_AMOUNT', 'SELL_CURRENCY' and their corresponding values """
        currency = None
        amount_sold = None
        val_dict = {}
        val_dict['SELL_AMOUNT'] = FCashOutUtils.get_sell_amount(self.acm_obj)
        val_dict['SELL_CURRENCY'] = FCashOutUtils.get_sell_currency(self.acm_obj)

        return val_dict


    # formatter
    def _format_currency_amount_sold_33B(self, val_dict):
        """ Formats the value provided by getter method """
        sell_amount = val_dict.get('SELL_AMOUNT')
        sell_currency = val_dict.get('SELL_CURRENCY')
        if sell_amount and sell_currency:
            sell_amount = FCashOutUtils.apply_currency_precision(sell_currency, float(sell_amount))
            if sell_amount < 0:
                sell_amount = abs(sell_amount)
            val = str(sell_currency) + str(FSwiftMLUtils.float_to_swiftmt(str(sell_amount)))
            return val


    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type)
    def _validate_currency_amount_sold_33B(self, val):
        """ Validates the value provided by formatter method """
        FCashOutUtils.validate_currency_amount(val, "Currency Amount Sold")
        amount = FCashOutUtils.get_amount_from_currency_amount(val)
        FCashOutUtils.validateAmount(amount.replace('.', ','), 15, "Currency Amount Sold")
        return val


    # setter
    def _set_currency_amount_sold_33B(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.CurrencyAmountSold = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.CurrencyAmountSold.swiftTag = "33B"


    # ------------------ sell_delivery_agent -----------------------
    # option getter
    def get_sell_delivery_agent_option(self):
        """ Returns default option if override is not provided """
        option = "J"
        party_details = FCashOutUtils.get_acquirer_delivery_agent_details(self.acm_obj)
        if FCashOutUtils.get_bic(party_details):
            option = "A"
        else:
            option = "J"
        return option

    # option setter
    def _set_OPTION_sell_delivery_agent(self):

        sell_delivery_agent_option = self.get_sell_delivery_agent_option()
        getter_name = 'sell_delivery_agent_53A'

        if sell_delivery_agent_option == "A":
            getter_name = 'sell_delivery_agent_53A'
        elif sell_delivery_agent_option == "J":
            getter_name = 'sell_delivery_agent_53J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % (str(sell_delivery_agent_option), 'SellDeliveryAgent_53a'))
        return getter_name


    # getter
    def sell_delivery_agent_53A(self):
        """ Returns dictionary with keys 'ACCOUNT', 'BIC' and their corresponding values """
        values_dict = FCashOutUtils.get_acquirer_delivery_agent_details(self.acm_obj)

        return values_dict


    # formatter
    def _format_sell_delivery_agent_53A(self, val):
        """ Formats the value provided by getter method """
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val


    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type)
    def _validate_sell_delivery_agent_53A(self, val):
        """ Validates the value provided by formatter method """
        return val


    # setter
    def _setsell_delivery_agent_53A(self, val):
        """Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.DeliveryAgent_A = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.DeliveryAgent_A.swiftTag = "53A"



    # getter
    def sell_delivery_agent_53J(self):
        """ Returns dictionary with keys 'NAME', 'ACCOUNT', 'ADDRESS', 'BIC' and their corresponding values """
        return FCashOutUtils.get_acquirer_delivery_agent_details(self.acm_obj)


    # formatter
    def _format_sell_delivery_agent_53J(self, val):
        """ Formats the value provided by getter method """
        return self._format_Option_J(val)


    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type)
    def _validate_sell_delivery_agent_53J(self, val):
        """ Validates the value provided by formatter method """
        return val


    # setter
    def _setsell_delivery_agent_53J(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.DeliveryAgent_J = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.DeliveryAgent_J.swiftTag = "53J"


    # ------------------ sell_intermediary -----------------------
    #option_getter
    def get_sell_intermediary_option(self):
        """ Returns default option if override is not provided """
        party_details = FCashOutUtils.get_counterparty_intermediary_details(self.acm_obj)
        option = "J"
        if FCashOutUtils.get_bic(party_details):
            option = "A"
        else:
            option = "J"
        return option


    # setter
    def _set_OPTION_sell_intermediary(self):
        sell_intermediary_option = self.get_sell_intermediary_option()

        if sell_intermediary_option == "A":
            getter_name = 'sell_intermediary_56A'
        elif sell_intermediary_option == "J":
            getter_name = 'sell_intermediary_56J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % (str(sell_intermediary_option), 'SellIntermediary_56a'))
            getter_name =  'sell_intermediary_56A'
        return getter_name


    # getter
    def sell_intermediary_56A(self):
        """ Returns dictionary with keys 'ACCOUNT', 'BIC' and their corresponding values """
        return FCashOutUtils.get_counterparty_intermediary_details(self.acm_obj)


    # formatter
    def _format_sell_intermediary_56A(self, val):
        """ Formats the value provided by getter method """
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type)
    def _validate_sell_intermediary_56A(self, val):
        """ Validates the value provided by formatter method """
        return val


    # setter
    def _setsell_intermediary_56A(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.Intermediary_A = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.Intermediary_A.swiftTag = "56A"



    # getter
    def sell_intermediary_56J(self):
        """ Returns dictionary with keys 'NAME', 'ACCOUNT', 'ADDRESS' and their corresponding values """
        return FCashOutUtils.get_counterparty_intermediary_details(self.acm_obj)

    # formatter
    def _format_sell_intermediary_56J(self, val):
        """ Formats the value provided by getter method """
        return self._format_Option_J(val)

    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type)
    def _validate_sell_intermediary_56J(self, val):
        """ Validates the value provided by formatter method """
        return val

    # setter
    def _setsell_intermediary_56J(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.Intermediary_J = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.Intermediary_J.swiftTag = "56J"


    # ------------------ sell_receiving_agent -----------------------
    # option_getter
    def get_sell_receiving_agent_option(self):
        """ Returns default option if override is not provided """
        party_details = FCashOutUtils.get_counterparty_receiving_agent_details(self.acm_obj)
        option = "J"
        if FCashOutUtils.get_bic(party_details):
            option = "A"
        else:
            option = "J"
        return option


    # option setter
    def _set_OPTION_sell_receiving_agent(self):
        sell_receiving_agent_option = self.get_sell_receiving_agent_option()


        if sell_receiving_agent_option == "A":
            getter_name = 'sell_receiving_agent_57A'
        elif sell_receiving_agent_option == "J":
            getter_name = 'sell_receiving_agent_57J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % (str(sell_receiving_agent_option), 'SellReceivingAgent_57a'))
            getter_name = 'sell_receiving_agent_57A'

        return getter_name


    # getter
    def sell_receiving_agent_57A(self):
        """ Returns dictionary with keys  'ACCOUNT', 'BIC' and their corresponding values """
        return FCashOutUtils.get_counterparty_receiving_agent_details(self.acm_obj)


    # formatter
    def _format_sell_receiving_agent_57A(self, val):
        """ Formats the value provided by getter method """
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val


    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type)
    def _validate_sell_receiving_agent_57A(self, val):
        """ Validates the value provided by formatter method """
        return val


    # setter
    def _setsell_receiving_agent_57A(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.ReceivingAgent_A = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.ReceivingAgent_A.swiftTag = "57A"



    # getter
    def sell_receiving_agent_57J(self):
        """ Returns dictionary with keys 'NAME', 'ACCOUNT', 'ADDRESS' and their corresponding values """

        return FCashOutUtils.get_counterparty_receiving_agent_details(self.acm_obj)


    # formatter
    def _format_sell_receiving_agent_57J(self, val):
        """ Formats the value provided by getter method """
        return self._format_Option_J(val)

    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type)
    def _validate_sell_receiving_agent_57J(self, val):
        """ Validates the value provided by formatter method """
        return val


    # setter
    def _setsell_receiving_agent_57J(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.ReceivingAgent_J = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.ReceivingAgent_J.swiftTag = "57J"


    # ------------------ sell_beneficiary_institution -----------------------

    # option_getter
    def get_sell_beneficiary_institution_option(self):
        """ Returns default option if override is not provided """
        option = "J"
        party_details = FCashOutUtils.get_beneficiary_institution_details(self.acm_obj)
        if FCashOutUtils.get_bic(party_details):
            option = "A"
        else:
            option = "J"
        return option


    # option setter
    def _set_OPTION_sell_beneficiary_institution(self):
        sell_beneficiary_institution_option = self.get_sell_beneficiary_institution_option()
        if sell_beneficiary_institution_option == "A":
            getter_name = 'sell_beneficiary_institution_58A'
        elif sell_beneficiary_institution_option == "J":
            getter_name = 'sell_beneficiary_institution_58J'
        else:
            notifier.WARN("Option %s is not supported for tag %s. Mapping default option." % (str(sell_beneficiary_institution_option), 'SellBeneficiaryInstitution_58a'))
            getter_name = 'sell_beneficiary_institution_58A'
        return getter_name


    # getter
    def sell_beneficiary_institution_58A(self):
        """ Returns dictionary with keys  'ACCOUNT',  'BIC' and their corresponding values """
        return FCashOutUtils.get_beneficiary_institution_details(self.acm_obj)


    # formatter
    def _format_sell_beneficiary_institution_58A(self, val):
        """ Formats the value provided by getter method """
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val


    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type)
    def _validate_sell_beneficiary_institution_58A(self, val):
        """ Validates the value provided by formatter method """
        return val


    # setter
    def _setsell_beneficiary_institution_58A(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.BeneficiaryInstitution_A = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.BeneficiaryInstitution_A.swiftTag = "58A"




    # getter
    def sell_beneficiary_institution_58J(self):
        """ Returns dictionary with keys 'NAME', 'ACCOUNT', 'ADDRESS', 'BIC' and their corresponding values """
        return FCashOutUtils.get_beneficiary_institution_details(self.acm_obj)


    # formatter
    def _format_sell_beneficiary_institution_58J(self, val):
        """ Formats the value provided by getter method """
        return self._format_Option_J(val)


    # validator
    @validate_with(MT304.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type)
    def _validate_sell_beneficiary_institution_58J(self, val):
        """ Validates the value provided by formatter method """
        return val


    # setter
    def _setsell_beneficiary_institution_58J(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.BeneficiaryInstitution_J = val
        self.swift_obj.SequenceB_ForexTransactionDetails.SubsequenceB2_AmountSold.BeneficiaryInstitution_J.swiftTag = "58J"


    # block getter
    def reference_to_previous_deals_21P(self):
        """ Returns list of references to all previous deals"""
        val = []
        val = FCashOutUtils.reference_of_previous_deals(self.acm_obj)
        return val

    # block formatter
    def _format_reference_to_previous_deals_21P(self, val):
        """ Returns formatted value """
        return val

    # block validator
    def _validate_reference_to_previous_deals_21P(self, reference_list):
        """ Validates block consisting reference to previous deals """
        validated_value_list = []
        for each_reference in reference_list:
            validated_val = self._validate_reference_to_previous_deals(each_reference)
            if validated_val:
                validated_value_list.append(validated_val)

        return validated_value_list



    @validate_with(MT304.MT304_SequenceD_AccountingInformation_21P_Type)
    def _validate_reference_to_previous_deals(self, val):
        """ Validates the value provided by formatter method """
        return val

    # check condition
    def _check_condition_set_reference_to_previous_deals_21P(self):
        """ Checks conditional presence for sequence D"""
        condition = False
        if self.is_seq_d:
            condition = True
        return condition

    # block setter
    def _set_reference_to_previous_deals_21P(self, val):
        """ Set the value provided by validator"""
        for each in val:
            self.swift_obj.SequenceD_AccountingInformation.ReferenceToPreviousDeals.append(each)
            self.swift_obj.SequenceD_AccountingInformation.ReferenceToPreviousDeals[-1].swiftTag = "21P"

    # ------------------ GainIndicator  -----------------------
    # getter
    def gain_indicator_17G(self):
        """ Returns string indicating gain """
        gain_indicator = FCashOutUtils.gain_indicator(self.acm_obj)
        return gain_indicator

    # formatter
    def _format_gain_indicator_17G(self, val):
        """ Formats the value provided by getter method """
        if val:
            return val

    # validator
    @validate_with(MT304.MT304_SequenceD_AccountingInformation_17G_Type)
    def _validate_gain_indicator_17G(self, val):
        """ Validates the value provided by formatter method """
        return val

    # check condition
    def _check_condition_set_gain_indicator_17G(self):
        """ Checks conditional presence for sequence D"""
        condition = False
        if self.is_seq_d:
            condition = True
        return condition


    # setter
    def _set_gain_indicator_17G(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceD_AccountingInformation.GainIndicator = val
        self.swift_obj.SequenceD_AccountingInformation.GainIndicator.swiftTag = "17G"


    # ------------------ CurrencyAmount  -----------------------
    # getter
    def currency_amount_32G(self):
        """ Returns dict consisting of keys: CURRENCY, AMOUNT and their corresponding values """
        currency_amount_dict = FCashOutUtils.calculate_currency_amount(self.acm_obj)
        return currency_amount_dict


    # formatter
    def _format_currency_amount_32G(self, val_dict):
        """ Formats the value provided by getter method """
        currency = val_dict['CURRENCY']
        amount = val_dict['AMOUNT']
        if currency and str(amount):
            amount = FCashOutUtils.apply_currency_precision(currency, float(amount))
            val = str(currency) + str(FSwiftMLUtils.float_to_swiftmt(str(abs(amount))))
            return val

    # validator
    @validate_with(MT304.MT304_SequenceD_AccountingInformation_32G_Type)
    def _validate_currency_amount_32G(self, val):
        """ Validates the value provided by formatter method """
        FCashOutUtils.validate_currency_amount(val, "Currency Amount")
        amount = FCashOutUtils.get_amount_from_currency_amount(val)
        FCashOutUtils.validateAmount(amount.replace('.', ','), 15, "Currency Amount")
        return val

    # check condition
    def _check_condition_set_currency_amount_32G(self):
        """ Checks conditional presence for sequence D"""
        condition = False
        if self.is_seq_d:
            condition = True
        return condition

    # setter
    def _set_currency_amount_32G(self, val):
        """ Sets the value on python object of MT304 """
        self.swift_obj.SequenceD_AccountingInformation.CurrencyAmount = val
        self.swift_obj.SequenceD_AccountingInformation.CurrencyAmount.swiftTag = "32G"

    # optional sequence setter
    def __set_optional_seq_d(self):
        """ Setter for optiuonal sequence D"""
        condition = False
        if self.acm_obj.Trade().IsFxForward() and self.acm_obj.Trade().Type() == 'Closing':

            self.swift_obj.SequenceD_AccountingInformation = MT304.MT304_SequenceD_AccountingInformation()
            self.swift_obj.SequenceD_AccountingInformation.swiftTag = "15D"
            self.swift_obj.SequenceD_AccountingInformation.formatTag = "False"
            condition = True
        return condition

    #------------------------- Custom functions -------------------------

    def fund_manager(self):
        """ Raises Not Implemented error as default if implementation not provided, expects party name for fund manager """
        raise NotImplementedError

    def executing_broker(self):
        """ Raises Not Implemented error as default if implementation not provided, expects party name for executing broker """
        raise NotImplementedError


class FMT304OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_typ = "304"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom


        super(FMT304OutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

    def message_type(self):
        return "304"

    def sender_logical_terminal_address(self):
        """LT code is hardcoded as A for sender"""
        terminal_address = ""
        senders_bic = ''
        senders_bic = FCashOutUtils.get_senders_bic(self.acm_obj)
        if not senders_bic:
            raise Exception("SENDER_BIC is a mandatory field for Swift message header")
        terminal_address = self.logical_terminal_address(senders_bic, "A")
        return terminal_address

    def receiver_logical_terminal_address(self):
        """LT code is hardcoded as X for sender"""
        terminal_address = ""
        receivers_bic = ''
        receivers_bic = FCashOutUtils.get_receivers_bic(self.acm_obj)
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
        """MUR is sent in the format FAC-SEQNBR of confirmation-VersionID"""
        seqnbr = self.acm_obj.Oid()
        return "{108:%s-%s-%s}" % (FCashOutUtils.get_settlement_reference_prefix(), seqnbr, FCashOutUtils.get_message_version_number(self.acm_obj))


class FMT304OutBaseNetworkRules(object):
    """ class for network rules """

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.acm_obj = acm_obj

    def network_rule_C1(self):
        """ In sequence A, the presence of field 21 depends on fields 22A as follows:
        ----------------------------------------------------------------------------
        If fields 22A is:                                        Then field 21 is:
        ----------------------------------------------------------------------------
         AMND                                                   Mandatory
         CANC                                                   Mandatory
         DUPL                                                   Optional
         NEWT                                                   Ptional
        """
        if self.swift_message_obj.SequenceA_GeneralInformation.TypeOfOperation.value() in ['AMND', 'CANC']:
            if not self.swift_message_obj.SequenceA_GeneralInformation.RelatedReference or not self.swift_message_obj.SequenceA_GeneralInformation.RelatedReference.value():
                return "Field 21 in Sequence A is mandatory if field 22A in Sequence A is equal to either AMND or CANC"
        return ''

    def network_rule_C2(self):
        """ In sequence A, the presence of fields 17O and 17N depends on field 94A as follows (Error code(s): D03):
        ----------------------------------------------------------------------------
        if field 94A is ...  then field 17O is ... and field 17N is ...
        ----------------------------------------------------------------------------
        AFWD                 Mandatory               Mandatory
        ANDF                 Mandatory               Not allowed
        ASET                 Not allowed             Not allowed

        """
        if self.swift_message_obj.SequenceA_GeneralInformation.ScopeOfOperation.value() == 'AFWD':
            if (not self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator or not self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator.value())\
            or (not self.swift_message_obj.SequenceA_GeneralInformation.NetSettlementIndicator or not self.swift_message_obj.SequenceA_GeneralInformation.NetSettlementIndicator.value()):
                return "Field 17O , Field 17N in Sequence A is mandatory as Field 94A has value 'AFWD' "

        elif self.swift_message_obj.SequenceA_GeneralInformation.ScopeOfOperation.value() == 'ANDF':
            if (not self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator or not self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator.value()) \
            and (not self.swift_message_obj.SequenceA_GeneralInformation.NetSettlementIndicator or self.swift_message_obj.SequenceA_GeneralInformation.NetSettlementIndicator.value()):
                return "Field 17O is Mandatory and Field 17N is not allowed as Field 94A has value 'ANDF' "

        elif self.swift_message_obj.SequenceA_GeneralInformation.ScopeOfOperation.value() == 'ASET':
            if (self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator and self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator.value()) \
            and (self.swift_message_obj.SequenceA_GeneralInformation.NetSettlementIndicator and \
            self.swift_message_obj.SequenceA_GeneralInformation.NetSettlementIndicator.value()):
                return "Field 17O and Field 17N is not allowed as Field 94A has value 'ASET' "
        return ''


    def network_rule_C3(self):
        """ In sequence A, the presence of field 17F depends on field 17O as follows (Error code(s): D04):
        ----------------------------------------------------------------------------
        if field 17O is...        then field 17F is ...
        ----------------------------------------------------------------------------
        Y                         Not allowed
        N                         Mandatory
        Not present               Not allowed
        """
        if self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator and self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator.value() == 'Y':
            if self.swift_message_obj.SequenceA_GeneralInformation.FinalCloseIndicator and self.swift_message_obj.SequenceA_GeneralInformation.FinalCloseIndicator.value():
                return "Field 17N is not allowed as Field 17O has value 'Y' "

        elif self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator and self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator.value() == 'N':
            if self.swift_message_obj.SequenceA_GeneralInformation.FinalCloseIndicator and not self.swift_message_obj.SequenceA_GeneralInformation.FinalCloseIndicator.value():
                return "Field 17N is mandatory as Field 17O has value 'N' "
        elif self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator and not self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator.value():
                return 'Field 17N is not allowed as Field 17O is not present'
        return ''


    def network_rule_C4(self):
        #
        """ The presence of sequence D and fields 21P, 17G, and 32G in sequence D depends on fields 94A and 17O as follows
         (Error code(s): D23):
        -----------------------------------------------------------------------------------------------------------------------------------------------
        if field 94A is...         and if field 17O is...         Then sequence D is ...               Sequence D and fields 21P,
                                                                                                        17G, and 32G are...
        -----------------------------------------------------------------------------------------------------------------------------------------------
        AFWD                       N                              Mandatory                            Mandatory
        AFWD                       Y                              Optional                             Not allowed
        ANDF                       N                              Optional                             Optional
        ANDF                       Y                              Optional                             Optional
        ASET                       Not applicable                 Optional                             Not allowed
        """

        if self.swift_message_obj.SequenceA_GeneralInformation.ScopeOfOperation:


            if self.swift_message_obj.SequenceA_GeneralInformation.ScopeOfOperation.value() == 'AFWD':

                if self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator and self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator.value() == 'N':

                    if not self.swift_message_obj.SequenceD_AccountingInformation:
                        return "Field 94A has value 'AFWD' and 17O has value 'N' hence Sequence D is mandatory along with fields 21P, 17G and 32G"

                    elif self.swift_message_obj.SequenceD_AccountingInformation:
                        field_21_in_seq_D = False
                        if self.swift_message_obj.SequenceD_AccountingInformation.ReferenceToPreviousDeals:
                            for reference_field in self.swift_message_obj.SequenceD_AccountingInformation.ReferenceToPreviousDeals:
                                if reference_field.value():
                                    field_21_in_seq_D = True
                        if not field_21_in_seq_D and (self.swift_message_obj.SequenceD_AccountingInformation.GainIndicator and not self.swift_message_obj.SequenceD_AccountingInformation.GainIndicator.value()) \
                            or (self.swift_message_obj.SequenceD_AccountingInformation.CurrencyAmount and not self.swift_message_obj.SequenceD_AccountingInformation.CurrencyAmount.value()):

                            return "Field 94A has value 'AFWD' and 17O has value 'N' hence Sequence D is mandatory along with fields 21P, 17G and 32G"
                elif self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator and self.swift_message_obj.SequenceA_GeneralInformation.OpenIndicator.value() == 'Y':

                    if self.swift_message_obj.SequenceD_AccountingInformation:
                        if (self.swift_message_obj.SequenceD_AccountingInformation.ReferenceToPreviousDeals and self.swift_message_obj.SequenceD_AccountingInformation.ReferenceToPreviousDeals.value())\
                        or (self.swift_message_obj.SequenceD_AccountingInformation.GainIndicator and self.swift_message_obj.SequenceD_AccountingInformation.GainIndicator.value())\
                        or (self.swift_message_obj.SequenceD_AccountingInformation.CurrencyAmount and self.swift_message_obj.SequenceD_AccountingInformation.CurrencyAmount.value()):
                            return "Field 94A has value 'AFWD' and 17O has value 'Y' hence Sequence D is optional and fields 21P, 17G and 32G are NOT allowed"

            elif self.swift_message_obj.SequenceA_GeneralInformation.ScopeOfOperation.value() == 'ASET':

                if self.swift_message_obj.SequenceD_AccountingInformation:

                    if (self.swift_message_obj.SequenceD_AccountingInformation.ReferenceToPreviousDeals and self.swift_message_obj.SequenceD_AccountingInformation.ReferenceToPreviousDeals.value())\
                            or (self.swift_message_obj.SequenceD_AccountingInformation.GainIndicator and self.swift_message_obj.SequenceD_AccountingInformation.GainIndicator.value())\
                            or (self.swift_message_obj.SequenceD_AccountingInformation.CurrencyAmount and self.swift_message_obj.SequenceD_AccountingInformation.CurrencyAmount.value()):
                        return "Field 94A has value 'ASET' hence Sequence D is optional and fields 21P, 17G and 32G are NOT allowed"
        return ''


    def network_rule_C5(self):
        """
        The presence of sequence E depends on fields 17F and 17N as follows (Error code(s): D29):
        -----------------------------------------------------------------------------------------------------------------------------------------------
        if field 17F is ...  and field 17N is ...       Then sequence E is ...
        -----------------------------------------------------------------------------------------------------------------------------------------------
        Y                    Y                          Mandatory
        Y                    N                          Not allowed
        Y                    Not present                Optional
        N                    Y or N or not present      Not allowed
        Not present          Y or N or not present      Not allowed """

        if self.swift_message_obj.SequenceA_GeneralInformation.FinalCloseIndicator:
            if self.swift_message_obj.SequenceA_GeneralInformation.FinalCloseIndicator.value() == 'Y':
                if self.swift_message_obj.SequenceA_GeneralInformation.NetSettlementIndicator and self.swift_message_obj.SequenceA_GeneralInformation.NetSettlementIndicator.value() == 'Y':
                    if not self.swift_message_obj.SequenceE_NetAmountToBeSettled:
                        return "Field 17F has value 'Y' and Field 17N has value 'Y', hence Sequence E is mandatory"
                elif self.swift_message_obj.SequenceA_GeneralInformation.NetSettlementIndicator and self.swift_message_obj.SequenceA_GeneralInformation.NetSettlementIndicator.value() == 'N':
                    if self.swift_message_obj.SequenceE_NetAmountToBeSettled:
                        return "Field 17F has value 'Y' and Field 17N has value 'N', hence Sequence E is NOT allowed"

            elif self.swift_message_obj.SequenceA_GeneralInformation.FinalCloseIndicator.value() == 'N':
                if self.swift_message_obj.SequenceE_NetAmountToBeSettled:
                    return "Field 17F has value 'N', hence Sequence E is NOT allowed"

                return ''
        elif not self.swift_message_obj.SequenceA_GeneralInformation.FinalCloseIndicator:
            if self.swift_message_obj.SequenceE_NetAmountToBeSettled:
                return "Field 17F is not present, hence Sequence E is not allowed"

        return ''


    def network_rule_C6(self):
        """ In all optional sequences, the fields with status M must be present if the sequence is present, and are otherwise not allowed (Error code(s): C32)."""

        return ''


    def network_rule_C7(self):
        """ In sequence D, field 30F may only be present if field 34B is present (Error code(s): C20). """
        if self.swift_message_obj.SequenceD_AccountingInformation:
            if not self.swift_message_obj.SequenceD_AccountingInformation.CommissionAndFeesCurrencyAndAmount or not self.swift_message_obj.CommissionAndFeesCurrencyAndAmount.value():
                if self.swift_message_obj.SequenceD_AccountingInformation.CommissionAndFeesSettlementDate and self.swift_message_obj.SequenceD_AccountingInformation.CommissionAndFeesSettlementDate.value():
                    return "In sequence D, field 30F may only be present if field 34B is present "
        return ''


    def network_rule_C8(self):
        """ In sequence A, if field 94A contains "ANDF", then fields 32E, 14S and 21A are optional and field 30U is mandatory, otherwise fields 32E, 14S, 21A and 30U are not allowed (Error    code(s): C87):
        -----------------------------------------------------------------------------------------------------------------------------------------------
        if field 94A is ...       then fields 32E, 14S and 21A are ...                 and field 30U is ...
        -----------------------------------------------------------------------------------------------------------------------------------------------
        ANDF                      Optional                                              Mandatory
        AFWD, ASET                Not allowed                                           Not allowed
        """
        if self.swift_message_obj.SequenceA_GeneralInformation.ScopeOfOperation:

            if self.swift_message_obj.SequenceA_GeneralInformation.ScopeOfOperation.value() == 'ANDF':
                if not self.swift_message_obj.SequenceA_GeneralInformation.ValuationDate or not self.swift_message_obj.SequenceA_GeneralInformation.ValuationDate.value():
                    return "Field 94A has value 'ANDF' hence field 30U is mandatory"


            elif self.swift_message_obj.SequenceA_GeneralInformation.ScopeOfOperation.value() in ['AFWD', 'ASET']:

                if (self.swift_message_obj.SequenceA_GeneralInformation.SettlementCurrency and self.swift_message_obj.SequenceA_GeneralInformation.SettlementCurrency.value()) \
                    or (self.swift_message_obj.SequenceA_GeneralInformation.SettlementRateSource and self.swift_message_obj.SequenceA_GeneralInformation.SettlementRateSource.value())\
                    or (self.swift_message_obj.SequenceA_GeneralInformation.ReferenceToOpeningInstruction and self.swift_message_obj.SequenceA_GeneralInformation.ReferenceToOpeningInstruction.value())\
                    or (self.swift_message_obj.SequenceA_GeneralInformation.ValuationDate and not self.swift_message_obj.SequenceA_GeneralInformation.ValuationDate.value()):


                    return "Field 32E, 14S, 21A and 30U are NOT allowed"


        return ''


    def network_rule_C9(self):
        """
        In sequence D, if field 15D is present then at least one of the other fields of sequence D must be present (Error code(s): C98).
        """
        field_21_in_seq_D = False
        if self.swift_message_obj.SequenceD_AccountingInformation:
            if self.swift_message_obj.SequenceD_AccountingInformation.ReferenceToPreviousDeals:
                for reference_field in self.swift_message_obj.SequenceD_AccountingInformation.ReferenceToPreviousDeals:
                    if reference_field.value():
                        field_21_in_seq_D = True
            if not field_21_in_seq_D or (self.swift_message_obj.SequenceD_AccountingInformation.GainIndicator and not self.swift_message_obj.SequenceD_AccountingInformation.GainIndicator.value()) \
            or (self.swift_message_obj.SequenceD_AccountingInformation.CurrencyAmount and not self.swift_message_obj.SequenceD_AccountingInformation.CurrencyAmount.value()) \
            or (self.swift_message_obj.SequenceD_AccountingInformation.CommissionAndFeesCurrencyAndAmount and not self.swift_message_obj.SequenceD_AccountingInformation.CommissionAndFeesCurrencyAndAmount.value()) \
            or (self.swift_message_obj.SequenceD_AccountingInformation.CommissionAndFeesSettlementDate and not self.swift_message_obj.SequenceD_AccountingInformation.CommissionAndFeesSettlementDate.value()):


                return "Atleast one of the fields should be present in Sequence D"
        return ''




