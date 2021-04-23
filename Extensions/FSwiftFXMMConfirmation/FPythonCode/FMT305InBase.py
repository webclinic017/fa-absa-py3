"""----------------------------------------------------------------------------
MODULE:
    FMT305InBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module opened to display the logic to extract attributes
    from swift message and an acm object but the user should NOT edit it.
    User can extend/override default mapping in derived class i.e. FMTIn305
    Base class for mapping attributes.
    Default logic for extracting attributes from either the swift data or
    the confirmation object.

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
import FSwiftWriterUtils
import acm



def apply_currency_precision(currency, amount):
    """ Round decimal amount according to the precision for a currency stated in Fparameter: RoundPerCurrency in FSwiftWriterConfig """
    result = FSwiftWriterUtils.apply_rounding(currency, amount)
    return result

class FMT305Base(FMT30X.FMT30X):
    """ Base class for MT305 mapping"""
    def __init__(self, source, direction):
        super(FMT305Base, self).__init__(source, direction)
        self.config_param = FSwiftMLUtils.Parameters('FMT305In_Config')
        self._message_type = 'MT305'
        self._further_identification = None
        self._date_contract_agreed_amended = None
        self._earliest_exercise_date = None
        self._expiry_date = None
        self._final_settlement_date = None
        self._fund_or_beneficiary_customer = None
        self._is_call_option = None
        self._exercise_type = None
        self._buy_sell = None
        self._settlement_type = None
        self._underlying_currency = None
        self._underlying_amount = None
        self._strike_price = None
        self._counter_currency = None
        self._counter_amount = None
        self._premium_price = None
        self._premium_currency = None
        self._premium_date = None
        self._premium = None
        self._factor = 1
        self._senders_correspondent = None
        self._account_with_institution = None
        self._code_common_reference = None

        # ------------------------------------------------------------------------------
    def SetAttributes(self):
        """ Set the attributes from incoming swift message/acm object to MT305"""
        try:
            if self.source == 'SWIFT':
                self.set_id_transaction_ref_number()
                self.set_related_reference()
                self.set_message_function()
                self.set_code_common_reference()
                self.set_further_identification()
                self.set_acquirer()
                self.set_counterparty()
                self.set_date_contract_agreed_amended()
                self.set_earliest_exercise_date()
                self.set_expiry_date()
                self.set_final_settlement_date()
                self.set_settlement_type()
                self.set_underlying_currency_amount()
                self.set_strike_price()
                self.set_counter_currency_amount()
                self.set_premium_price()
                self.set_premium_payment()
                self.set_senders_correspondent()
                self.set_account_with_institution()
                self.ext_ref = self.InternalIdentifier()

            elif self.source == 'ACM':
                self.set_is_call_option_from_trade()
                self.set_exercise_type_from_trade()
                self.set_acquirer_counterparty_from_trade()
                self.set_date_contract_agreed_amended_from_trade()
                self.set_expiry_date_from_trade()
                self.set_final_settlement_date_from_trade()
                self.set_underlying_currency_from_trade()
                self.set_underlying_amount_from_trade()
                self.set_counter_currency_from_trade()
                self.set_premium_currency_from_trade()
                self.set_premium_date_from_trade()
                self.set_premium_from_trade()
                self.set_sender_receiver_account_from_trade()
        except Exception as e:
            notifier.ERROR("Exception occurred in SetAttributes : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

# ------------------------------------------------------------------------------
    # Methods to fetch data from the swift message
    def set_id_transaction_ref_number(self):
        try:
            #TODO: Change SendersReference to TransactionReferenceNumber
            self._identifier = str(self.python_object.SequenceA_GeneralInformation.TransactionReferenceNumber.value()) if self.python_object.SequenceA_GeneralInformation.TransactionReferenceNumber else None
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_id_transaction_ref_number : %s"%str(e))

    def set_message_function(self):
        try:
            self._message_function = str(self.python_object.SequenceA_GeneralInformation.CodeCommonReference.value().split('/')[0]) if self.python_object.SequenceA_GeneralInformation.CodeCommonReference else None
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_message_function : %s"%str(e))

    def set_code_common_reference(self):
        try:
            self._code_common_reference = str(self.python_object.SequenceA_GeneralInformation.CodeCommonReference.value()) if self.python_object.SequenceA_GeneralInformation.CodeCommonReference else None
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_code_common_reference : %s"%str(e))

    def set_further_identification(self):
        try:
            self._further_identification = str(self.python_object.SequenceA_GeneralInformation.FurtherIdentification.value()) if self.python_object.SequenceA_GeneralInformation.FurtherIdentification else None
            if self._further_identification:
                self.set_option_type_from_futher_id(self._further_identification)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_further_identification : %s"%str(e))

    def set_fund_or_beneficiary_customer(self):
        try:
            if self.python_object.SequenceA_GeneralInformation.FundOrBeneficiaryCustomer_A:
                self._fund_or_beneficiary_customer = str(self.python_object.SequenceA_GeneralInformation.FundOrBeneficiaryCustomer_A.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_fund_or_beneficiary_customer : %s"%str(e))

    def set_option_type_from_futher_id(self, further_id):
        try:
            further_id = str(self.python_object.SequenceA_GeneralInformation.FurtherIdentification.value())
            self._buy_sell = further_id.split('/')[0]
            call_put = further_id.split('/')[1]
            excercise_type = further_id.split('/')[2]
            self._is_call_option = 'True' if call_put == "CALL" else 'False'

            if excercise_type == "E":
                self._exercise_type = "European"
            elif excercise_type == "A":
                self._exercise_type = "American"
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_currency_amount : %s"%str(e))

    def set_date_contract_agreed_amended(self):
        try:
            date_contract_agreed_amended = str(self.python_object.SequenceA_GeneralInformation.DateContractAgreedAmended.value()) if self.python_object.SequenceA_GeneralInformation.DateContractAgreedAmended else None
            if date_contract_agreed_amended:
                self._date_contract_agreed_amended = FSwiftMLUtils.swiftmt_to_date(date_contract_agreed_amended)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_date_contract_agreed_amended : %s"%str(e))

    def set_earliest_exercise_date(self):
        try:
            earliest_exercise_date = str(self.python_object.SequenceA_GeneralInformation.EarliestExerciseDate.value()) if self.python_object.SequenceA_GeneralInformation.EarliestExerciseDate else None
            if earliest_exercise_date:
                self._earliest_exercise_date = FSwiftMLUtils.swiftmt_to_date(earliest_exercise_date)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_earliest_exercise_date : %s"%str(e))

    def set_expiry_date(self):
        try:
            expiry_date = str(self.python_object.SequenceA_GeneralInformation.ExpiryDetails.value()[:6]) if self.python_object.SequenceA_GeneralInformation.ExpiryDetails else None
            if expiry_date:
                self._expiry_date = FSwiftMLUtils.swiftmt_to_date(expiry_date)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_expiry_date : %s"%str(e))

    def set_final_settlement_date(self):
        try:
            settlement_date = str(self.python_object.SequenceA_GeneralInformation.FinalSettlementDate.value()) if self.python_object.SequenceA_GeneralInformation.FinalSettlementDate else None
            if settlement_date:
                self._final_settlement_date = FSwiftMLUtils.swiftmt_to_date(settlement_date)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_final_settlement_date : %s"%str(e))

    def set_settlement_type(self):
        try:
            self._settlement_type = str(self.python_object.SequenceA_GeneralInformation.SettlementType.value()) if self.python_object.SequenceA_GeneralInformation.SettlementType else None
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_settlement_type : %s"%str(e))

    def set_underlying_currency_amount(self):
        try:
            self._underlying_currency = str(self.python_object.SequenceA_GeneralInformation.UnderlyingCurrencyNAmount.value()[0:3])
            underlying_amount = self.python_object.SequenceA_GeneralInformation.UnderlyingCurrencyNAmount.value()[3:]
            self._underlying_amount = FSwiftMLUtils.swiftmt_to_float(underlying_amount)
            '''if (self.direction == "IN" and self._buy_sell == "BUY") or (self.direction == "OUT" and self._buy_sell == "SELL"):
                self._underlying_amount = self._underlying_amount * -1'''
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_underlying_currency_amount : %s"%str(e))

    def set_strike_price(self):
        try:
            self._strike_price = FSwiftMLUtils.swiftmt_to_float(str(self.python_object.SequenceA_GeneralInformation.StrikePrice.value()))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_strike_price : %s"%str(e))

    def set_counter_currency_amount(self):
        try:
            self._counter_currency = str(self.python_object.SequenceA_GeneralInformation.CounterCurrencyNAmount.value()[0:3])
            self._counter_amount = FSwiftMLUtils.swiftmt_to_float(self.python_object.SequenceA_GeneralInformation.CounterCurrencyNAmount.value()[3:])
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_counter_currency_amount : %s"%str(e))

    def set_premium_price(self):
        try:
            self._premium_price = FSwiftMLUtils.swiftmt_to_float(str(self.python_object.SequenceA_GeneralInformation.PremiumPrice.value()[3:]))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_premium_price : %s"%str(e))

    def AdjustFieldsToCompare(self, theirs_object, conf_obj):


        # Rate can be expressed in the form of a percentage or in the form of points per unit of either currency amount.
        # When the rate is expressed in the form of a percentage, Currency must contain PCT.
        # When the rate is expressed in the form of points per unit of either currency amount, the currency code must be specified in Currency.

        their_currency = str(theirs_object.python_object.SequenceA_GeneralInformation.PremiumPrice.value()[:3])


        conf_obj = self.acm_obj if self.acm_obj else conf_obj

        if conf_obj:
            if 'PCT' == their_currency:
                self._premium_price = conf_obj.Trade().Price()
            else:
                self._premium_price = abs(conf_obj.Trade().Premium())

            self.set_fields_from_further_identificatio(theirs_object.python_object, conf_obj)




    def get_mult_factor(self, f_instrument):
        if f_instrument:
            quotation_type = f_instrument.Quotation().QuotationType()

            if quotation_type:
                if 'Factor' == quotation_type:
                    return 1 / 100.0
                elif 'Points of UndCurr' == quotation_type:
                    curr = f_instrument.Currency().Name()
                    und_curr = f_instrument.Underlying().Name()
                    curr_pair = acm.FCurrencyPair.Select('currency1="%s" and currency2="%s"' % (und_curr, curr))
                    if curr_pair:
                        return curr_pair[0].PointValue()



    def set_premium_payment(self):
        try:
            if self.python_object.SequenceA_GeneralInformation.PremiumPayment_P:
                premium_details = str(self.python_object.SequenceA_GeneralInformation.PremiumPayment_P.value())
                if self.direction == "OUT":
                    self._factor = -1
            elif self.python_object.SequenceA_GeneralInformation.PremiumPayment_R:
                premium_details = str(self.python_object.SequenceA_GeneralInformation.PremiumPayment_R.value())
                if self.direction == "IN":
                    self._factor = -1
            self._premium_date = FSwiftMLUtils.swiftmt_to_date(premium_details[:6])
            self._premium_currency = premium_details[6:9]
            self._premium = self._factor * FSwiftMLUtils.swiftmt_to_float(premium_details[9:])
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_premium_payment : %s"%str(e))

    def set_senders_correspondent(self):
        try:
            self._senders_correspondent = str(self.get_party_typeA(self.python_object.SequenceA_GeneralInformation.SendersCorrespondent_A.value())) if self.python_object.SequenceA_GeneralInformation.SendersCorrespondent_A else None
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_senders_correspondent : %s"%str(e))

    def set_account_with_institution(self):
        try:
            self._account_with_institution = str(self.get_party_typeA(self.python_object.SequenceA_GeneralInformation.AccountWithInstitution_A.value())) if self.python_object.SequenceA_GeneralInformation.AccountWithInstitution_A else None
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_account_with_institution : %s"%str(e))

# ------------------------------------------------------------------------------
    # Method to fetch data from the adm

    def GetCode1(self, confirmation):
        if confirmation.Trade().Quantity() >= 0:
            return 'BUY'
        else:
            return 'SELL'

    def GetCode2(self, confirmation):
        if confirmation.Trade().Instrument().IsCallOption():
            return 'CALL'
        else:
            return 'PUT'

    def GetCode3(self, confirmation):
        return confirmation.Trade().Instrument().ExerciseType()

    def GetUnderlyingAmount(self, confirmation):
        amount = confirmation.Trade().Quantity()
        currency = confirmation.Trade().Currency().Name()
        return apply_currency_precision(currency, abs(amount))

    def GetCounterAmount(self, confirmation):
        contractSize = confirmation.Trade().Instrument().ContractSize()
        strikePrice = confirmation.Trade().Instrument().StrikePrice()
        quantity = confirmation.Trade().Quantity()
        quantity = abs(quantity)
        return contractSize * quantity * strikePrice

    def GetUnderlyingCurrency(self, confirmation):
        underlyingCurrency = ''
        underlyingIns = confirmation.Trade().Instrument().Underlying()
        if underlyingIns:
            underlyingCurrency = underlyingIns.Name()
        return underlyingCurrency

    def GetCounterCurrency(self, confirmation):
        strikeCurr = confirmation.Trade().Instrument().StrikeCurrency()
        if strikeCurr:
            return strikeCurr.Name()
        else:
            return ''

    def set_fields_from_further_identificatio(self, _python_object, conf_obj):
        try:
            def get_inverse(input):
                rev_dict = {'SELL':'BUY', 'BUY':'SELL','PUT':'CALL', 'CALL':'PUT'}
                return rev_dict.get(input)

            _theirs_further_identification = str(_python_object.SequenceA_GeneralInformation.FurtherIdentification.value()) if _python_object.SequenceA_GeneralInformation.FurtherIdentification else None

            if _theirs_further_identification:
                _theirs_further_identification_codes = _theirs_further_identification.split('/')
                _their_code_1 = _theirs_further_identification_codes[0]
                _their_code_2 = _theirs_further_identification_codes[1]
                _their_code_4 = _theirs_further_identification_codes[3]

                _inv_our_code_1 = get_inverse(self.GetCode1(conf_obj))
                _inv_our_code_2 = get_inverse(self.GetCode2(conf_obj))

                # If the counterparty have reversed their nomenclature then Sell Call becomes a Buy Put
                # and the fields 32B and 33B are reversed

                counter_curr = self.GetCounterCurrency(conf_obj)
                if (_their_code_1 == _inv_our_code_1) and (_their_code_2 == _inv_our_code_2) and (_their_code_4 == counter_curr):
                    self._counter_currency = self.GetUnderlyingCurrency(conf_obj)
                    self._underlying_currency = counter_curr

                    self._underlying_amount = self.GetCounterAmount(conf_obj)
                    self._counter_amount = self.GetUnderlyingAmount(conf_obj)

                    self._is_call_option = 'True' if "CALL" == _their_code_2 else 'False'

        except Exception as e:
            notifier.DEBUG("Exception occurred in set_is_call_option_from_trade : %s"%str(e))

    def set_is_call_option_from_trade(self):
        try:
            self._is_call_option = 'True' if self.acm_obj.Trade().Instrument().IsCallOption() else 'False'
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_is_call_option_from_trade : %s"%str(e))

    def set_exercise_type_from_trade(self):
        try:
            self._exercise_type = self.acm_obj.Trade().Instrument().ExerciseType()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_exercise_type_from_trade : %s"%str(e))

    def set_date_contract_agreed_amended_from_trade(self):
        try:
            self._date_contract_agreed_amended = self.acm_obj.Trade().TradeTime().split()[0]
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_date_contract_agreed_amended_from_trade : %s"%str(e))

    def set_expiry_date_from_trade(self):
        try:
            self._expiry_date = self.acm_obj.Trade().Instrument().ExpiryDateOnly()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_expiry_date_from_trade : %s"%str(e))

    def set_final_settlement_date_from_trade(self):
        try:
            self._final_settlement_date = self.acm_obj.Trade().Instrument().DeliveryDate()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_final_settlement_date_from_trade : %s"%str(e))

    def set_underlying_currency_from_trade(self):
        try:
            self._underlying_currency = self.acm_obj.Trade().Instrument().Underlying().Name()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_underlying_currency_from_trade : %s"%str(e))

    def set_underlying_amount_from_trade(self):
        try:
            self._underlying_amount = abs(self.acm_obj.Trade().Quantity())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_underlying_amount_from_trade : %s"%str(e))

    def set_counter_currency_from_trade(self):
        try:
            self._counter_currency = self.acm_obj.Trade().Instrument().StrikeCurrency().Name()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_counter_currency_from_trade : %s"%str(e))

    def set_premium_currency_from_trade(self):
        try:
            self._premium_currency = self.acm_obj.Trade().Currency().Name()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_premium_currency_from_trade : %s"%str(e))

    def set_premium_date_from_trade(self):
        try:
            self._premium_date = self.acm_obj.Trade().ValueDay()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_premium_date_from_trade : %s"%str(e))

    def set_premium_from_trade(self):
        try:
            self._premium = self.acm_obj.Trade().Premium()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_premium_from_trade : %s"%str(e))

    def set_sender_receiver_account_from_trade(self):
        try:
            acq_acct = ''
            cpty_acct = ''
            for flw in self.acm_obj.Trade().MoneyFlows():
                if flw.Type() in ["Premium", "Premium 2"]:
                    acq_acct = flw.AcquirerAccount().Bic().Alias() if flw.AcquirerAccount().Bic() else None
                    cpty_acct = flw.CounterpartyAccount().Bic().Alias() if flw.CounterpartyAccount().Bic() else None
                    if self._premium < 0:
                        self._senders_correspondent = acq_acct
                        self._account_with_institution = cpty_acct
                    else:
                        self._senders_correspondent = cpty_acct
                        self._account_with_institution = acq_acct
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_sender_receiver_account_from_trade : %s"%str(e))

# ------------------------------------------------------------------------------
    # Method to fetch data used in the Pairing and Matching attributes in the FParameter
    def TransactionReferenceNumber(self):
        return self._identifier

    def CodeCommonReference(self):
        return self._code_common_reference

    def FurtherIdentification(self):
        return self._further_identification

    def FundOrBeneficiaryCustomer(self):
        return self._fund_or_beneficiary_customer

    def IsCallOption(self):
        return self._is_call_option

    def ExerciseType(self):
        return self._exercise_type

    def DateContractAgreedAmended(self):
        return self._date_contract_agreed_amended

    def EarliestExerciseDate(self):
        return self._earliest_exercise_date

    def ExpiryDate(self):
        return self._expiry_date

    def FinalSettlementDate(self):
        return self._final_settlement_date

    def SettlementType(self):
        return self._settlement_type

    def UnderlyingCurrency(self):
        return self._underlying_currency

    def UnderlyingAmount(self):
        return self._underlying_amount

    def StrikePrice(self):
        return self._strike_price

    def CounterCurrency(self):
        return self._counter_currency

    def CounterAmount(self):
        return self._counter_amount

    def PremiumPrice(self):
        return self._premium_price

    def Premium(self):
        return self._premium

    def PremiumDate(self):
        return self._premium_date

    def PremiumCurrency(self):
        return self._premium_currency

    def SendersCorrespondent(self):
        return self._senders_correspondent

    def AccountWithInstitution(self):
        return self._account_with_institution

    @staticmethod
    def GetColumnMetaData():
        column_metadata = {
            'TransactionReferenceNumber': {'THEIRS_SWIFT_TAG' : '20', 'OURS_SWIFT_TAG' : '20', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'RelatedReference': {'THEIRS_SWIFT_TAG' : '21', 'OURS_SWIFT_TAG' : '21', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'CodeCommonReference': {'THEIRS_SWIFT_TAG' : '22', 'OURS_SWIFT_TAG' : '22', 'SEQUENCE': 'General Information', 'COLOR': ''},

            'FurtherIdentification': {'THEIRS_SWIFT_TAG' : '23', 'OURS_SWIFT_TAG' : '23', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'IsCallOption': {'THEIRS_SWIFT_TAG' : '23', 'OURS_SWIFT_TAG' : '23', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'ExerciseType': {'THEIRS_SWIFT_TAG' : '23', 'OURS_SWIFT_TAG' : '23', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'Acquirer': {'REAL_GETTER': 'RealAcquirer', 'REAL_SWIFT_TAG': '82A', 'THEIRS_SWIFT_TAG': '87A','OURS_SWIFT_TAG': '82A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'Counterparty': {'REAL_GETTER': 'RealCounterparty', 'REAL_SWIFT_TAG': '87A', 'THEIRS_SWIFT_TAG': '82A','OURS_SWIFT_TAG': '87A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'FundOrBeneficiaryCustomer': {'THEIRS_SWIFT_TAG' : '83A', 'OURS_SWIFT_TAG' : '83A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'DateContractAgreedAmended': {'THEIRS_SWIFT_TAG' : '30', 'OURS_SWIFT_TAG' : '30', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'EarliestExerciseDate': {'THEIRS_SWIFT_TAG' : '31C', 'OURS_SWIFT_TAG' : '31C', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'ExpiryDate': {'THEIRS_SWIFT_TAG' : '31G', 'OURS_SWIFT_TAG' : '31G', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'FinalSettlementDate': {'THEIRS_SWIFT_TAG' : '31E', 'OURS_SWIFT_TAG' : '31E', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'SettlementType': {'THEIRS_SWIFT_TAG' : '26F', 'OURS_SWIFT_TAG' : '26F', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'UnderlyingCurrency': {'THEIRS_SWIFT_TAG' : '32B', 'OURS_SWIFT_TAG' : '32B', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'UnderlyingAmount': {'THEIRS_SWIFT_TAG' : '32B', 'OURS_SWIFT_TAG' : '32B', 'SEQUENCE': 'General Information', 'COLOR': '', 'FORMAT':'NumDefault'},
            'StrikePrice': {'THEIRS_SWIFT_TAG' : '36', 'OURS_SWIFT_TAG' : '36', 'SEQUENCE': 'General Information', 'COLOR': '', 'FORMAT':'NumDefault'},
            'CounterCurrency': {'THEIRS_SWIFT_TAG' : '33B', 'OURS_SWIFT_TAG' : '33B', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'CounterAmount': {'THEIRS_SWIFT_TAG' : '33B', 'OURS_SWIFT_TAG' : '33B', 'SEQUENCE': 'General Information', 'COLOR': ''},

            'PremiumPrice': {'THEIRS_SWIFT_TAG' : '37K', 'OURS_SWIFT_TAG' : '37K', 'SEQUENCE': 'General Information', 'COLOR': '', 'FORMAT':'NumDefault'},
            'Premium': {'THEIRS_SWIFT_TAG' : '34A', 'OURS_SWIFT_TAG' : '34A', 'SEQUENCE': 'General Information', 'COLOR': '', 'FORMAT':'NumDefault'},
            'PremiumDate': {'THEIRS_SWIFT_TAG' : '34A', 'OURS_SWIFT_TAG' : '34A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'PremiumCurrency': {'THEIRS_SWIFT_TAG' : '34A', 'OURS_SWIFT_TAG' : '34A', 'SEQUENCE': 'General Information', 'COLOR': ''},

            'SendersCorrespondent': {'THEIRS_SWIFT_TAG' : '53A', 'OURS_SWIFT_TAG' : '53A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'AccountWithInstitution': {'THEIRS_SWIFT_TAG' : '57A', 'OURS_SWIFT_TAG' : '57A', 'SEQUENCE': 'General Information', 'COLOR': ''},

            }

        return column_metadata

    @staticmethod
    def GetColumnNamePrefix():
        return 'MT305'
