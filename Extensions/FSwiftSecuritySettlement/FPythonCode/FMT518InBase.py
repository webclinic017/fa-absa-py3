"""----------------------------------------------------------------------------
MODULE:
    FMT518InBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module opened to display the logic to extract attributes
    from swift message and an acm object but the user should NOT edit it. User
    can extend/override the default mapping in derived class i.e. FMT518
    Base class for mapping attributes.
    Default logic for extracting attributes from either swift data or the
    settlement object.

FUNCTIONS:
    ProcessMTMessage():
        Process the incoming MT518 message. It stores the incoming message in
        FExternalItem and creates the business process on it.

    UniquePair():
        Return paired object if incoming message has a unique identifier to get
        the object from acm. User can configure this.

    IsSecurityTransfer():
        Return true if the incoming message represents security transfer.
        User can configure this.

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import acm
import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('SecSetlConf', 'FSecuritySettlementInNotify_Config')
import FMTInBase
import FSwiftMLUtils
import FSecuritySettlementOutUtils
import FSecurityConfirmationOutUtils
import FSwiftWriterUtils

class FMT518Base(FMTInBase.FMTInBase):
    """ Base class for MT518 mapping"""
    def __init__(self, source, direction, msg_type):
        super(FMT518Base, self).__init__(source, direction)
        self.type = msg_type
        self.config_param = FSwiftMLUtils.Parameters('F%sIn_Config'%(self.type))

        self._senders_message_reference = None
        self._function_of_message = None
        self._trade_transaction_type = None
        self._buysell_indicator = None
        self._payment_indicator = None
        self._settlement_date = None
        self._trade_date = None
        self._identification_of_instrument = None
        self._quantity_of_instrument = None
        self._acquirer = None
        self._counterparty = None
        self._settlement_amount = None
        self._accrued_interest_amount = None
        self._deal_price = None

# ------------------------------------------------------------------------------


    def SetAttributes(self):
        """ Set the attributes from incoming swift message/acm object to MT518 type"""
        try:
            if self.source == 'SWIFT':
                self.set_senders_message_reference()
                self.set_function_of_message()
                self.set_trade_transaction_type()
                self.set_indicator()
                self.set_trade_date()
                self.set_identification_of_instrument()
                self.set_quantity_of_instrument()
                self.set_acquirer()
                self.set_counterparty()
                self.set_settlement_amount()
                self.set_deal_price()
            elif self.source == 'ACM':
                self.set_function_of_message_from_trade()
                self.set_trade_transaction_type_from_trade()
                self.set_indicator_from_trade()
                self.set_trade_date_from_trade()
                self.set_identification_of_instrument_from_trade()
                self.set_quantity_of_instrument_from_trade()
                self.set_acquirer_from_trade()
                self.set_counterparty_from_trade()
                self.set_settlement_amount_from_trade()
                self.set_deal_price_from_trade()

        except Exception as e:
            notifier.ERROR("Exception occurred in SetAttributes : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

# ------------------------------------------------------------------------------
    # Methods to fetch data from the swift message
    def set_senders_message_reference(self):
        try:
            self._senders_message_reference = str(self.python_object.SequenceA_GeneralInformation.SendersMessageReference.value())
            #val_list = senders_reference.split('/')
            #self._senders_message_reference = val_list[-1]
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_senders_message_reference : %s"%str(e))


    def set_function_of_message(self):
        try:
            self._function_of_message = str(self.python_object.SequenceA_GeneralInformation.FunctionOfTheMessage.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_function_of_message : %s"%str(e))


    def set_trade_transaction_type(self):
        try:
            trade_transaction_type = str(self.python_object.SequenceA_GeneralInformation.TradeTransactionType.value())
            val_list = trade_transaction_type.split('/')
            self._trade_transaction_type = val_list[-1]
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_trade_transaction_type : %s"%str(e))


    def set_indicator(self):
        try:
            for each in self.python_object.SequenceB_ConfirmationDetails.Indicator_H:
                indicator = each.value()
                if 'BUSE' in indicator:
                    indicator_value = indicator
                    val_list = indicator_value.split('/')
                    self._buysell_indicator = str(val_list[-1])
                elif 'PAYM' in indicator:
                    indicator_value = indicator
                    val_list = indicator_value.split('/')
                    self._payment_indicator = str(val_list[-1])
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_indicator : %s" % str(e))


    def set_trade_date(self):
        try:
            for each in self.python_object.SequenceB_ConfirmationDetails.DateTime_A:
                date = each.value()
                if 'SETT' in date:
                    date_value = date
                    val_list = date_value.split('/')
                    self._settlement_date = val_list[-1]
                    self._settlement_date = str(FSwiftMLUtils.swiftmt_to_date(self._settlement_date))
                elif 'TRAD' in date:
                    date_value = date
                    val_list = date_value.split('/')
                    self._trade_date = val_list[-1]
                    self._trade_date = str(FSwiftMLUtils.swiftmt_to_date(self._trade_date))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_trade_date : %s" % str(e))


    def set_identification_of_instrument(self):
        try:
            isin_value = str(self.python_object.SequenceB_ConfirmationDetails.IdentificationOfTheFinancialInstrument.value())
            val_list = isin_value.split(' ')
            self._identification_of_instrument = val_list[-1]
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_identification_of_instrument : %s" % str(e))


    def set_quantity_of_instrument(self):
        try:
            quantity = str(self.python_object.SequenceB_ConfirmationDetails.QuantityOfFinancialInstrument.value())
            val_list = quantity.split('/')
            self._quantity_of_instrument = val_list[-1]
            self._quantity_of_instrument = FSwiftMLUtils.swiftmt_to_float(self._quantity_of_instrument)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_quantity_of_instrument : %s" % str(e))


    def set_acquirer(self):
        try:
            for party in self.python_object.SequenceB_ConfirmationDetails.SubSequenceB1_ConfirmationParties:
                if party.PARTY_P:
                    for each in party.PARTY_P:
                        party_value = each.value()
                        if 'BUYR' in party_value:
                            value = party_value
                            val_list = value.split('/')
                            self._acquirer = str(val_list[-1])
                if party.PARTY_Q:
                    for each in party.PARTY_Q:
                        party_value = each.value()
                        if 'BUYR' in party_value:
                            value = party_value
                            val_list = value.split('/')
                            self._acquirer = str(val_list[-1])
                if party.PARTY_L:
                    for each in party.PARTY_L:
                        party_value = each.value()
                        if 'ALTE' in party_value:
                            value = party_value
                            val_list = value.split('/')
                            self._acquirer = str(val_list[-1])
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer : %s" % str(e))


    def set_counterparty(self):
        try:
            for party in self.python_object.SequenceB_ConfirmationDetails.SubSequenceB1_ConfirmationParties:
                if party.PARTY_P:
                    for each in party.PARTY_P:
                        party_value = each.value()
                        if 'SELL' in party_value:
                            value = party_value
                            val_list = value.split('/')
                            self._counterparty = str(val_list[-1])
                if party.PARTY_Q:
                    for each in party.PARTY_Q:
                        party_value = each.value()
                        if 'SELL' in party_value:
                            value = party_value
                            val_list = value.split('/')
                            self._counterparty = str(val_list[-1])
                if party.PARTY_L:
                    for each in party.PARTY_L:
                        party_value = each.value()
                        if 'ALTE' in party_value:
                            value = party_value
                            val_list = value.split('/')
                            self._counterparty = str(val_list[-1])
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_counterparty : %s" % str(e))


    def set_settlement_amount(self):
        try:
            for amount in self.python_object.SequenceC_SettlementDetails.SubSequenceC3_Amounts:
                for each in amount.Amount:
                    amount_value = each.value()
                    if 'SETT' in amount_value:
                        value = amount_value
                        val_list = value.split('/')
                        self._settlement_amount = val_list[-1][3:]
                        self._settlement_amount = FSwiftMLUtils.swiftmt_to_float(self._settlement_amount)
                    elif 'ACRU' in amount_value:
                        value = amount_value
                        val_list = value.split('/')
                        self._accrued_interest_amount = val_list[-1][3:]
                        self._accrued_interest_amount = FSwiftMLUtils.swiftmt_to_float(self._accrued_interest_amount)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_settlement_amount : %s" % str(e))


    def set_deal_price(self):
        try:
            deal_price = str(self.python_object.SequenceB_ConfirmationDetails.DealPrice_A.value())
            val_list = deal_price.split('/')
            self._deal_price = val_list[-1]
            self._deal_price = FSwiftMLUtils.swiftmt_to_float(self._deal_price)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_deal_price : %s" % str(e))


# ------------------------------------------------------------------------------
    # Method to fetch data from the adm

    def set_function_of_message_from_trade(self):
        try:
            self._function_of_message = FSwiftWriterUtils.get_type_of_operation(self.acm_obj)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_function_of_message_from_trade : %s" % str(e))


    def set_trade_transaction_type_from_trade(self):
        try:
            self._trade_transaction_type = FSecurityConfirmationOutUtils.get_transaction_type()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_trade_transaction_type_from_trade : %s" % str(e))


    def set_indicator_from_trade(self):
        try:
            self._buysell_indicator = None
            self._payment_indicator = None
            indicators = FSecurityConfirmationOutUtils.get_indicators(self.acm_obj)
            for indicator_pair in indicators:
                qualifier_value = FSecurityConfirmationOutUtils.get_qualifier(indicator_pair)
                indicator_value = FSecurityConfirmationOutUtils.get_indicator(indicator_pair)
                if 'BUSE' in qualifier_value:
                    self._buysell_indicator = indicator_value
                if 'PAYM' in qualifier_value:
                    self._payment_indicator = indicator_value
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_indicator_from_trade : %s" % str(e))


    def set_trade_date_from_trade(self):
        try:
            self._settlement_date = FSecurityConfirmationOutUtils.get_confirmation_datetime_date(self.acm_obj)
            self._trade_date = FSecuritySettlementOutUtils.get_trade_datetime_date(self.acm_obj)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_trade_date_from_trade : %s" % str(e))


    def set_identification_of_instrument_from_trade(self):
        try:
            isin = FSecurityConfirmationOutUtils.get_instrument_ISIN(self.acm_obj)
            val_list = isin.split(' ')
            self._identification_of_instrument = val_list[-1]
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_identification_of_instrument_from_trade : %s" % str(e))


    def set_quantity_of_instrument_from_trade(self):
        try:
            self._quantity_of_instrument = FSecurityConfirmationOutUtils.get_nominal(self.acm_obj)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_quantity_of_instrument_from_trade : %s" % str(e))


    def set_acquirer_from_trade(self):
        try:
            partyDetails = FSecurityConfirmationOutUtils.get_acquirer_party_details(self.acm_obj)
            self._acquirer = FSecuritySettlementOutUtils.get_party_identifier_code(partyDetails)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_from_trade : %s" % str(e))

    def set_counterparty_from_trade(self):
        try:
            partyDetails = FSecurityConfirmationOutUtils.get_counter_party_details(self.acm_obj)
            self._counterparty = FSecuritySettlementOutUtils.get_party_identifier_code(partyDetails)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_counterparty_from_trade : %s" % str(e))

    def set_settlement_amount_from_trade(self):
        try:
            amount_list = FSecurityConfirmationOutUtils.get_amount_details(self.acm_obj, 'MT518')
            for each in amount_list:
                if 'SETT' in each['AMOUNT_QUALIFIER']:
                    self._settlement_amount  = each['AMOUNT_AMOUNT']
                elif 'ACRU' in each['AMOUNT_QUALIFIER']:
                    self._accrued_interest_amount = each['AMOUNT_AMOUNT']
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_settlement_amount_from_trade : %s" % str(e))

    def set_deal_price_from_trade(self):
        try:
            deal_price = FSecurityConfirmationOutUtils.get_deal_price_details(self.acm_obj, 'A')
            self._deal_price = deal_price.get('deal_price')
            self._deal_price = FSwiftMLUtils.swiftmt_to_float(self._deal_price)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_deal_price_from_trade : %s" % str(e))



# ------------------------------------------------------------------------------
    # Method to fetch data used in the Pairing and Matching attributes in the FParameter
    def Type(self):
        """ Get the type of the MT message"""
        return self.type
    def SendersReference(self):
        return self._senders_message_reference

    def Identifier(self):
        return self._senders_message_reference

    def TypeOfOperation(self):
        return self._function_of_message

    def TradeTransactionType(self):
        return self._trade_transaction_type

    def BuySellIndicator(self):
        ret_val = ''
        if self._swap_field_flag == False:
            ret_val = str(self._buysell_indicator)
        else:
            if self.direction == "IN":
                for each in self.python_object.SequenceB_ConfirmationDetails.Indicator_H:
                    indicator = each.value()
                    if 'BUSE' in indicator:
                        indicator_value = indicator
                        val_list = indicator_value.split('/')
                        buysell_indicator = val_list[-1]
                if buysell_indicator == 'BUYI':
                    ret_val = 'SELL'
                else:
                    ret_val = 'BUYI'
        return ret_val

    def PaymentIndicator(self):
        return self._payment_indicator

    def SettlementDate(self):
        return self._settlement_date

    def TradeDate(self):
        return self._trade_date

    def IdentificationOfFinancialInstrument(self):
        return self._identification_of_instrument

    def QuantityOfInstrument(self):
        return self._quantity_of_instrument

    def Acquirer(self):
        return self._acquirer

    def CounterParty(self):
        return self._counterparty

    def SettlementAmount(self):
        return self._settlement_amount

    def AccruedInterestAmount(self):
        return self._accrued_interest_amount

    def DealPrice(self):
        return self._deal_price


# ------------------------------------------------------------------------------

    def get_bpr(self, external_obj, is_new):
        state_chart_name = FSwiftMLUtils.get_state_chart_name_for_mt_type(self.Type(), 'In')
        reconciliation_item = FSwiftMLUtils.FSwiftExternalObject.subject_for_business_process(external_obj)

        bpr = FSwiftMLUtils.get_or_create_business_process(external_obj, state_chart_name, self.Type())
        if bpr:
            notifier.INFO('%s : Business process id <%i> with state chart <%s> on %s <%i>' \
                          % ('Initialized' if is_new else 'Reusing', bpr.Oid(), state_chart_name, reconciliation_item.ClassName(), reconciliation_item.Oid()))

        return bpr

    def ProcessMTMessage(self, msg_id):
        """ process the incoming mt message"""
        notifier.INFO("Processing incoming %s message."%(self.type))
        try:
            value_dict = {'swift_data':self.swift_data}
            external_obj = FSwiftMLUtils.FSwiftExternalObject.create_external_object(value_dict, message_typ=self.Type(), channel_id=msg_id, subject_typ='Confirmation', ext_ref=self.Identifier(), in_or_out="Incoming")
            reconciliation_item = FSwiftMLUtils.FSwiftExternalObject.subject_for_business_process(external_obj)
            sc = FSwiftMLUtils.get_state_chart_name_for_mt_type(self.Type(), 'In')
            bpr = FSwiftMLUtils.get_or_create_business_process(external_obj, sc, self.Type())
            if bpr:
                notifier.INFO('Initialized : Business process id <%i> with state chart <%s> on %s <%i>' \
                                      %(bpr.Oid(), sc, reconciliation_item.ClassName(), reconciliation_item.Oid()))
        except Exception as e:
            notifier.ERROR("Exception occurred in ProcessMTMessage : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

    def IsSupportedMessageFunction(self):
        """check if the message type is supported"""
        is_supported = False
        if self._function_of_message in ["NEWM", "NEWT", "AMND", "CANC", "AMEND", "CANCEL", "NEWM/DUPL"]:
            is_supported = True
        return is_supported

    def IsSecurityTransfer(self):
        """Return True if incoming message represents Security transfer"""
        is_security_transfer = False
        return is_security_transfer

    def IsExchangeTradeRepoConfirmation(self):
        """There can not be a default implementation for this because to decide if its an exchange traded repo confirmation
           or not will be based on the BIC in field 95P for BUYR or SELLR"""
        return False

    def RepoCompareTolerance(self):
        """Tolerance used for comparing repo amounts.This can be configured by user. This method should return a integer/float as string"""
        return '0.01'

    @staticmethod
    def GetColumnMetaData():
        column_metadata = {
            'SendersReference': {'THEIRS_SWIFT_TAG' : '20', 'OURS_SWIFT_TAG' : '20', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'TypeOfOperation': {'THEIRS_SWIFT_TAG' : '22A', 'OURS_SWIFT_TAG' : '22A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'TradeTransactionType': {'THEIRS_SWIFT_TAG' : '22F', 'OURS_SWIFT_TAG' : '22F', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'BuySellIndicator': {'THEIRS_SWIFT_TAG' : '22H', 'OURS_SWIFT_TAG' : '22H', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'Acquirer': {'THEIRS_SWIFT_TAG' : '87A', 'OURS_SWIFT_TAG' : '82A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'CounterParty': {'THEIRS_SWIFT_TAG' : '82A', 'OURS_SWIFT_TAG' : '87A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'PaymentIndicator': {'THEIRS_SWIFT_TAG' : '22H', 'OURS_SWIFT_TAG' : '22H', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'SettlementDate': {'THEIRS_SWIFT_TAG' : '98A', 'OURS_SWIFT_TAG' : '98A', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'TradeDate': {'THEIRS_SWIFT_TAG' : '98A', 'OURS_SWIFT_TAG' : '98A', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'IdentificationOfFinancialInstrument': {'THEIRS_SWIFT_TAG' : '35B', 'OURS_SWIFT_TAG' : '35B', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'QuantityOfInstrument': {'THEIRS_SWIFT_TAG' : '36B', 'OURS_SWIFT_TAG' : '36B', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'SettlementAmount': {'THEIRS_SWIFT_TAG' : '19A', 'OURS_SWIFT_TAG' : '19A', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'AccruedInterestAmount': {'THEIRS_SWIFT_TAG' : '19A', 'OURS_SWIFT_TAG' : '19A', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'DealPrice': {'THEIRS_SWIFT_TAG' : '90A', 'OURS_SWIFT_TAG' : '90A', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            }
        return column_metadata

    @staticmethod
    def GetColumnNamePrefix():
        return 'MT518'

