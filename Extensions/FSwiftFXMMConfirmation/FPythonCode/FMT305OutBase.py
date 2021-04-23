"""----------------------------------------------------------------------------
MODULE:
    FMT305OutBase

DESCRIPTION:
    This module provides the base class for the FMT305 outgoing implementation

CLASS:
    FMT305Base

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""

import FSwiftMLUtils
import FSwiftWriterMessageHeader
import MT305
import acm
from FSwiftWriterEngine import validate_with, should_use_operations_xml

import FSwiftWriterLogger
from FFXMMConfirmationOutUtils import *
from FFXMMOutBase import FFXMMOutBase
import FSwiftConfirmationUtils
import FSwiftWriterMTFactory
import FSwiftWriterUtils

notifier = FSwiftWriterLogger.FSwiftWriterLogger('FXMMConfOut', 'FFXMMConfirmationOutNotify_Config')

class FMT305Base(FFXMMOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = "MT305"
        super(FMT305Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    def _message_sequences(self):
        self.swift_obj.SequenceA_GeneralInformation = MT305.MT305_SequenceA_GeneralInformation()
        self.swift_obj.SequenceA_GeneralInformation.swiftTag = "15A"
        self.swift_obj.SequenceA_GeneralInformation.formatTag = "False"

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

                #setting related reference value (Tag 21) on the fmt object
                trans_val = pyobj.SequenceA_GeneralInformation.TransactionReferenceNumber.value()
                self.swift_obj.SequenceA_GeneralInformation.RelatedReference = trans_val
                self.swift_obj.SequenceA_GeneralInformation.RelatedReference.swiftTag = "21"

                #setting the transaction reference number value (Tag 20) on the fmt object
                getter_value = self.transaction_reference_number_20()
                formatter_value = self._format_transaction_reference_number_20(getter_value)
                validated_value = self._validate_transaction_reference_number_20(formatter_value)
                self._set_transaction_reference_number_20(validated_value)

                #setting code common reference value (Tag 22)
                old_val = pyobj.SequenceA_GeneralInformation.CodeCommonReference.value()
                if 'NEW' in old_val:
                    val = old_val.replace('NEW', 'CANCEL')
                elif 'AMEND' in old_val:
                    val = old_val.replace('AMEND', 'CANCEL')
                self.swift_obj.SequenceA_GeneralInformation.CodeCommonReference = val
                self.swift_obj.SequenceA_GeneralInformation.CodeCommonReference.swiftTag = "22"

                mt_message = FSwiftWriterUtils.create_swift_msg_from_pyobj(self.swift_obj)

                fmt_swift_header_class_obj = FSwiftWriterMTFactory.FSwiftWriterMTFactory.create_fmt_header_object(self.swift_message_type, self.acm_obj, mt_message, None)
                canc_message = fmt_swift_header_class_obj.swift_message_with_header()

                #return canc_message, self.swift_obj
        except Exception as e:
            raise e
        return canc_message, self.swift_obj


    # Methods to fetch data from the swift message

    # ------------------ senders_reference -----------------------
    # getter
    def transaction_reference_number_20(self):
        '''Returns oid of the confirmation as string '''
        if self.use_operations_xml:
            transaction_reference_number = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                ['CONFIRMATION', 'SEQNBR'])
        else:
            transaction_reference_number = self.acm_obj.Oid()
        return transaction_reference_number

    # formatter
    def _format_transaction_reference_number_20(self, val):
        if val:
            return "%s-%s-%s" % (get_confirmation_reference_prefix(), str(val), str(get_message_version_number(self.acm_obj)))

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_20_Type)
    def _validate_transaction_reference_number_20(self, val):
        validate_slash_and_double_slash(val, "Transaction Reference Number")
        return val

    # setter
    def _set_transaction_reference_number_20(self, val):
        self.swift_obj.SequenceA_GeneralInformation.TransactionReferenceNumber = val
        self.swift_obj.SequenceA_GeneralInformation.TransactionReferenceNumber.swiftTag = "20"


    # ------------------ related_reference -----------------------
    # getter
    def related_reference_21(self):
        '''Returns  'NEW' or related confirmaiton object'''
        if self.use_operations_xml:
            related_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'YOUR_REFERENCE'])
            return related_reference
        else:
            if get_type_of_operation(self.acm_obj) in ['AMND', 'CANC']:
                return get_related_confirmation(self.acm_obj)
            else:
                return 'NEW'


    # formatter
    def _format_related_reference_21(self, val):
        if self.use_operations_xml:
            if val != 'NEW':
                conf_id = val.strip("FAC-")
                ref_conf = acm.FConfirmation[str(conf_id)]
                ref_conf, val = check_for_valid_related_reference(ref_conf, val)
                version_number_of_related_reference = get_version_for_sent_message_on(ref_conf, 'MT305')
                val = str(val) + "-" + str(version_number_of_related_reference)
                return val
            else:
                return val
        else:
            if val != 'NEW':
                related_conf = val
                related_reference = '%s-%s-%s' % (get_confirmation_reference_prefix(), str(val.Oid()), str(get_version_for_sent_message_on(related_conf, 'MT305')))
                related_conf, related_reference = check_for_valid_related_reference(related_conf, related_reference)
                return related_reference
            else:
                return val

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_21_Type, is_mandatory=True)
    def _validate_related_reference_21(self, val):
        validate_slash_and_double_slash(val, "Related Reference")
        return val

    # setter
    def _set_related_reference_21(self, val):
       self.swift_obj.SequenceA_GeneralInformation.RelatedReference = val
       self.swift_obj.SequenceA_GeneralInformation.RelatedReference.swiftTag = "21"


    # ------------------ code_common_reference -----------------------
    # getter
    def code_common_reference_22(self):
        '''Returns a dictionary with keys 'CODE', 'SENDERS_BIC', 'RECEIVERS_BIC', 'STRIKE_PRICE' and their corresponding values'''
        if self.use_operations_xml:
            val_dict = {}
            code = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'CODE'])
            type_of_operation = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'TYPE_OF_OPERATION'])
            if type_of_operation == "CANC":
                code = 'CANCEL'
            elif type_of_operation == "AMND":
                code = 'AMEND'
            elif type_of_operation == "NEWT":
                code = 'NEW'

            senders_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SENDER_BIC'])
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'RECEIVER_BIC'])
            strike_price = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'STRIKE_PRICE'])
            val_dict['CODE'] = code
            val_dict['SENDERS_BIC'] = senders_bic
            val_dict['RECEIVER_BIC'] = receivers_bic
            val_dict['STRIKE_PRICE'] = strike_price
        else:
            val_dict = {}
            type_of_operation = get_type_of_operation(self.acm_obj)
            if type_of_operation == "CANC":
                code = 'CANCEL'
            elif type_of_operation == "AMND":
                code = 'AMEND'
            elif type_of_operation == "NEWT":
                code = 'NEW'
            val_dict['CODE'] = code
            val_dict['SENDERS_BIC'] = get_senders_bic(self.acm_obj)
            val_dict['RECEIVER_BIC'] = get_receivers_bic(self.acm_obj)
            val_dict['STRIKE_PRICE'] = get_strike_price(self.acm_obj)

        return val_dict

    # formatter
    def _format_code_common_reference_22(self, val):
        code = val.get('CODE')
        senders_bic = val.get('SENDERS_BIC')
        receivers_bic = val.get('RECEIVER_BIC')
        strike_price = val.get('STRIKE_PRICE')

        if code and senders_bic and receivers_bic and strike_price:
            strike_currency = get_strike_currency(self.acm_obj)
            strike_price = apply_currency_precision(strike_currency, float(strike_price))
            strike_price_part = represent_amount_in_four_digits(str(strike_price))
            if receivers_bic[0:4] + receivers_bic[-2:] > senders_bic[0:4] + senders_bic[-2:]:
                val = code + "/" + senders_bic[0:4] + senders_bic[-2:] + strike_price_part + receivers_bic[
                                                                                             0:4] + receivers_bic[-2:]
            else:
                val = code + "/" + receivers_bic[0:4] + receivers_bic[-2:] + strike_price_part + senders_bic[
                                                                                                 0:4] + senders_bic[-2:]
            return str(val)

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_22_Type)
    def _validate_code_common_reference_22(self, val):
        return val

    # setter
    def _set_code_common_reference_22(self, val):
        self.swift_obj.SequenceA_GeneralInformation.CodeCommonReference = val
        self.swift_obj.SequenceA_GeneralInformation.CodeCommonReference.swiftTag = "22"

    # ------------------ further_identification -----------------------
    # getter
    def further_identification_23(self):
        '''Returns a dictionary with keys 'BUY_SELL', 'CALL_PUT', 'EXERCISE_TYPE', 'CURRENCY' and their correpsonding values '''
        if self.use_operations_xml:
            val_dict = {}
            buy_sell = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'CODE1'])
            call_put = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'CODE2'])
            exercise_type = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'CODE3'])
            currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                ['SWIFT', 'UNDERLYING_CURRENCY'])
            val_dict['BUY_SELL'] = buy_sell
            val_dict['CALL_PUT'] = call_put
            val_dict['EXERCISE_TYPE'] = exercise_type
            val_dict['CURRENCY'] = currency
        else:
            val_dict = {}
            val_dict['BUY_SELL'] = is_buy_or_sell(self.acm_obj)
            val_dict['CALL_PUT'] = is_call_or_put(self.acm_obj)
            val_dict['EXERCISE_TYPE'] = get_exercise_type(self.acm_obj)
            val_dict['CURRENCY'] = get_underlying_currency(self.acm_obj)

        return val_dict

    # formatter
    def _format_further_identification_23(self, val):
        buy_sell = val.get('BUY_SELL')
        call_put = val.get('CALL_PUT')
        exercise_type = val.get('EXERCISE_TYPE')
        currency = val.get('CURRENCY')

        if buy_sell and call_put and exercise_type and currency:
            further_identification = str(buy_sell) + "/" + str(call_put) + "/" + str(exercise_type[
                0]) + "/" + str(currency)
            return further_identification

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_23_Type)
    def _validate_further_identification_23(self, val):
        return val

    # setter
    def _set_further_identification_23(self, val):
        self.swift_obj.SequenceA_GeneralInformation.FurtherIdentification = val
        self.swift_obj.SequenceA_GeneralInformation.FurtherIdentification.swiftTag = "23"

    # ------------------ party_A -----------------------
    # option getter
    def get_partyA_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_party_A(self):
        '''Returns getter name as string like 'partyA_82A', 'partyA_82D' '''
        if self.use_operations_xml:
            party_A_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                  ['SWIFT', 'PARTY_A_OPTION'])
        else:
            party_A_option = self.get_partyA_option()

        if party_A_option == "A":
            return 'partyA_82A'
        elif party_A_option == "D":
            return 'partyA_82D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,
                                                                                                 str(party_A_option),
                                                                                                 'PartyA_82a'))
        return 'partyA_82A'

    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_82A_Type)
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

    @validate_with(MT305.MT305_SequenceA_GeneralInformation_82D_Type)
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
    def _set_OPTION_party_B(self):
        '''Returns getter name as string like 'partyB_87A', 'partyB_87D' '''
        if self.use_operations_xml:
            party_B_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                  ['SWIFT', 'PARTY_B_OPTION'])
        else:
            party_B_option = self.get_partyB_option()

        if party_B_option == "A":
            return 'partyB_87A'
        elif party_B_option == "D":
            return 'partyB_87D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,
                                                                                                 str(party_B_option),
                                                                                                 'PartyB_87a'))
        return 'partyB_87A'

    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_87A_Type)
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
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_87D_Type)
    def _validate_partyB_87D(self, val):
        return val

    # setter
    def _setpartyB_87D(self, val):
        self.swift_obj.SequenceA_GeneralInformation.PartyB_D = val
        self.swift_obj.SequenceA_GeneralInformation.PartyB_D.swiftTag = "87D"

    # ------------------ date_contract_agreed_amended -----------------------

    # getter
    def date_contract_agreed_amended_30(self):
        '''Returns date of contract agreed or amended as string '''
        if self.use_operations_xml:
            date_contract_agreed_amended = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                ['SWIFT', 'TRADE_DATE'])
        else:
            date_contract_agreed_amended = FSwiftConfirmationUtils.get_trade_date(self.acm_obj)

        return date_contract_agreed_amended

    # formatter
    def _format_date_contract_agreed_amended_30(self, val):
        if val:
            date_format = '%y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)

            return val

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_30_Type)
    def _validate_date_contract_agreed_amended_30(self, val):
        return val

    # setter
    def _set_date_contract_agreed_amended_30(self, val):
        self.swift_obj.SequenceA_GeneralInformation.DateContractAgreedAmended = val
        self.swift_obj.SequenceA_GeneralInformation.DateContractAgreedAmended.swiftTag = "30"

    # ------------------ earliest_exercise_date -----------------------
    # getter
    def earliest_exercise_date_31C(self):
        '''Returns earliest exercise date as string '''
        if self.use_operations_xml:
            earliest_exercise_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'EXERCISE_DATE'],
                                                                          ignore_absense=True)
        else:
            earliest_exercise_date = get_earliest_exercise_date(self.acm_obj)

        return earliest_exercise_date

    # formatter
    def _format_earliest_exercise_date_31C(self, val):
        if val:
            date_format = '%y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)
            return str(val)

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_31C_Type)
    def _validate_earliest_exercise_date_31C(self, val):
        return val

    def _check_condition_set_earliest_exercise_date_31C(self):
        if self.use_operations_xml:
            exercise_type = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'CODE3'])
        else:
            exercise_type = get_exercise_type(self.acm_obj)
        if "A" in exercise_type:
            return True
        return False

    # setter
    def _set_earliest_exercise_date_31C(self, val):
        self.swift_obj.SequenceA_GeneralInformation.EarliestExerciseDate = val
        self.swift_obj.SequenceA_GeneralInformation.EarliestExerciseDate.swiftTag = "31C"

    # ------------------ expiry_details -----------------------
    # getter
    def expiry_details_31G(self):
        '''Returns dictionary with keys 'EXPIRY_DETAILS_DATE', 'EXPIRY_DETAILS_TIME', 'EXPIRY_DETAILS_LOCATION' and their corresponding values '''
        if self.use_operations_xml:
            val_dict = {}
            expiry_details_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'EXPIRY_DETAILS_DATE'])
            expiry_details_time = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'EXPIRY_DETAILS_TIME'])
            expiry_details_location = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                               ['SWIFT', 'EXPIRY_DETAILS_LOCATION'])

            val_dict['EXPIRY_DETAILS_DATE'] = expiry_details_date
            val_dict['EXPIRY_DETAILS_TIME'] = expiry_details_time
            val_dict['EXPIRY_DETAILS_LOCATION'] = expiry_details_location
            return val_dict
        else:
            return get_option_expiry_details(self.acm_obj)

    # formatter
    def _format_expiry_details_31G(self, val):
        expiry_details_date = val.get('EXPIRY_DETAILS_DATE')
        expiry_details_time = val.get('EXPIRY_DETAILS_TIME')
        expiry_details_location = val.get('EXPIRY_DETAILS_LOCATION')
        date_format = '%y%m%d'

        if expiry_details_date and expiry_details_time and expiry_details_location:
            location_code = get_location_code(expiry_details_location)
            expiry_details_date = FSwiftWriterUtils.format_date(expiry_details_date, date_format)
            val = "/".join([str(expiry_details_date), str(expiry_details_time), str(location_code)])
            return val

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_31G_Type)
    def _validate_expiry_details_31G(self, val):
        return val

    # setter
    def _set_expiry_details_31G(self, val):
        self.swift_obj.SequenceA_GeneralInformation.ExpiryDetails = val
        self.swift_obj.SequenceA_GeneralInformation.ExpiryDetails.swiftTag = "31G"

    # ------------------ final_settlement_date -----------------------

    # getter
    def final_settlement_date_31E(self):
        '''Returns final settlement date as string '''
        if self.use_operations_xml:
            final_settlement_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'SETTLEMENT_DATE'])
        else:
            final_settlement_date = get_settlement_date(self.acm_obj)
        return final_settlement_date

    # formatter
    def _format_final_settlement_date_31E(self, val):
        if val:
            date_format = '%y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)

            return str(val)

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_31E_Type)
    def _validate_final_settlement_date_31E(self, val):
        return val

    # setter
    def _set_final_settlement_date_31E(self, val):
        self.swift_obj.SequenceA_GeneralInformation.FinalSettlementDate = val
        self.swift_obj.SequenceA_GeneralInformation.FinalSettlementDate.swiftTag = "31E"

    # ------------------ settlement_type -----------------------
    # getter
    # Moved to FXMMOutBase

    # formatter
    # Moved to FXMMOutBase

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_26F_Type)
    def _validate_settlement_type_26F(self, val):
        return val

    # setter
    def _set_settlement_type_26F(self, val):
        self.swift_obj.SequenceA_GeneralInformation.SettlementType = val
        self.swift_obj.SequenceA_GeneralInformation.SettlementType.swiftTag = "26F"

    # ------------------ underlying_currency_amount -----------------------
    # getter
    def underlying_currency_amount_32B(self):
        '''Returns dictioanry with keys 'UNDERLYING_CURRENCY', 'UNDERLYING_AMOUNT' and their correpsonding values '''
        if self.use_operations_xml:
            val_dict = {}
            underlying_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'UNDERLYING_CURRENCY'])
            underlying_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'UNDERLYING_AMOUNT'])
            val_dict['UNDERLYING_CURRENCY'] = underlying_currency
            val_dict['UNDERLYING_AMOUNT'] = underlying_amount
        else:
            val_dict = {}
            val_dict['UNDERLYING_CURRENCY'] = get_underlying_currency(self.acm_obj)
            val_dict['UNDERLYING_AMOUNT'] = get_underlying_amount(self.acm_obj)
        return val_dict

    # formatter
    def _format_underlying_currency_amount_32B(self, val):
        underlying_currency = val.get('UNDERLYING_CURRENCY')
        underlying_amount = val.get('UNDERLYING_AMOUNT')
        if underlying_amount and underlying_currency:
            underlying_amount = apply_currency_precision(underlying_currency, float(underlying_amount))
            val = str(underlying_currency) + FSwiftMLUtils.float_to_swiftmt(str(underlying_amount))

            return str(val)

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_32B_Type)
    def _validate_underlying_currency_amount_32B(self, val):
        validate_currency_amount(val, "Underlying Currency and Amount")
        amount = get_amount_from_currency_amount(val)
        validateAmount(amount.replace('.', ','), 15, "Underlying Currency and Amount")
        return val

    # setter
    def _set_underlying_currency_amount_32B(self, val):
        self.swift_obj.SequenceA_GeneralInformation.UnderlyingCurrencyNAmount = val
        self.swift_obj.SequenceA_GeneralInformation.UnderlyingCurrencyNAmount.swiftTag = "32B"

    # ------------------ strike_price -----------------------
    # getter
    def strike_price_36(self):
        '''Returns strike price as string '''
        if self.use_operations_xml:
            strike_price = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'STRIKE_PRICE'])
        else:
            strike_price = get_strike_price(self.acm_obj)
        return strike_price

    # formatter
    def _format_strike_price_36(self, val):
        if val:
            strike_currency = get_strike_currency(self.acm_obj)
            val = apply_currency_precision(strike_currency, float(val))
            val = FSwiftMLUtils.float_to_swiftmt(str(val))
            return str(val)

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_36_Type)
    def _validate_strike_price_36(self, val):
        strike_price = val
        validateAmount(strike_price.replace('.', ','), 15, "Strike Price")
        return val

    # setter
    def _set_strike_price_36(self, val):
        self.swift_obj.SequenceA_GeneralInformation.StrikePrice = val
        self.swift_obj.SequenceA_GeneralInformation.StrikePrice.swiftTag = "36"

    # ------------------ currency_amount_bought_details -----------------------
    # getter
    def counter_currency_amount_33B(self):
        '''Returns dictionary with keys 'COUNTER_CURRENCY', 'COUNTER_AMOUNT' and their corresponding values '''
        if self.use_operations_xml:
            val_dict = {}
            counter_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                        ['SWIFT', 'COUNTER_CURRENCY'])
            counter_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'COUNTER_AMOUNT'])
            val_dict['COUNTER_CURRENCY'] = counter_currency
            val_dict['COUNTER_AMOUNT'] = counter_amount
        else:
            val_dict = {}
            val_dict['COUNTER_CURRENCY'] = get_counter_currency(self.acm_obj)
            val_dict['COUNTER_AMOUNT'] = get_counter_amount(self.acm_obj)
        return val_dict

    # formatter
    def _format_counter_currency_amount_33B(self, val_dict):

        counter_currency = val_dict.get('COUNTER_CURRENCY')
        counter_amount = val_dict.get('COUNTER_AMOUNT')
        if counter_currency and counter_amount:
            counter_amount = apply_currency_precision(counter_currency, float(counter_amount))
            val = str(counter_currency) + FSwiftMLUtils.float_to_swiftmt(str(counter_amount))
            return str(val)

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_33B_Type)
    def _validate_counter_currency_amount_33B(self, val):
        validate_currency_amount(val, "Counter Currency and Amount")
        amount = get_amount_from_currency_amount(val)
        validateAmount(amount.replace('.', ','), 15, "Counter Currency and Amount")
        return val

    # setter
    def _set_counter_currency_amount_33B(self, val):
       self.swift_obj.SequenceA_GeneralInformation.CounterCurrencyNAmount = val
       self.swift_obj.SequenceA_GeneralInformation.CounterCurrencyNAmount.swiftTag = "33B"

    # ------------------ premium_price -----------------------
    # getter
    def premium_price_37K(self):
        ''' Returns premium price as string  '''
        if self.use_operations_xml:
            premium_price = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                 ['SWIFT', 'PREMIUM_PRICE'])
        else:
            premium_price = get_premium_price(self.acm_obj)
        return premium_price

    # formatter
    def _format_premium_price_37K(self, val):
        if val:
            premium_currency = get_premium_currency(self.acm_obj)
            val = apply_currency_precision(premium_currency, float(val))
            val = "PCT" + FSwiftMLUtils.float_to_swiftmt(str(val))
            return str(val)

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_37K_Type)
    def _validate_premium_price_37K(self, val):
        price = get_amount_from_currency_amount(val)
        validateAmount(price.replace('.', ','), 15, "Premium Price")
        return val

    # setter
    def _set_premium_price_37K(self, val):
        self.swift_obj.SequenceA_GeneralInformation.PremiumPrice = val
        self.swift_obj.SequenceA_GeneralInformation.PremiumPrice.swiftTag = "37K"

    # ------------------ premium_payment -----------------------
    # option getter
    def get_premium_payment_option(self):
        """Returns default option if override is not provided"""
        if is_buy_or_sell(self.acm_obj) == 'SELL':
            option = 'R'
        else:
            option = 'P'
        return option


    def _set_OPTION_premium_payment(self):
        '''Returns name of the getter like 'premium_payment_34R', 'premium_payment_34P' '''
        if self.use_operations_xml:
            premium_payment_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'PREMIUM_PAYMENT_OPTION'])
        else:
            premium_payment_option = self.get_premium_payment_option()

        if premium_payment_option == 'R':
            return 'premium_payment_34R'
        elif premium_payment_option == 'P':
            return 'premium_payment_34P'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,
                                                                                                 str(premium_payment_option),
                                                                                                 'premium_payment_34a'))

        return 'premium_payment_34R'

    # getter
    def premium_payment_34R(self):
        '''Returns dictionary with keys 'PREMIUM_PAYMENT_DATE', 'PREMIUM_PAYMENT_CURRENCY', 'PREMIUM_PAYMENT_AMOUNT' and their corresponding values '''
        if self.use_operations_xml:
            val_dict = {}
            premium_payment_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                            ['SWIFT', 'PREMIUM_PAYMENT_DATE'])
            premium_payment_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                ['SWIFT', 'PREMIUM_PAYMENT_CURRENCY'])
            premium_payment_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                              ['SWIFT', 'PREMIUM_PAYMENT_AMOUNT'])
            premium_payment_amount = apply_currency_precision(premium_payment_currency,
                                                                                   float(premium_payment_amount))
            val_dict['PREMIUM_PAYMENT_DATE'] = premium_payment_date
            val_dict['PREMIUM_PAYMENT_CURRENCY'] = premium_payment_currency
            val_dict['PREMIUM_PAYMENT_AMOUNT'] = premium_payment_amount
        else:
            val_dict = {}
            val_dict['PREMIUM_PAYMENT_DATE'] = get_premium_payment_date(self.acm_obj)
            val_dict['PREMIUM_PAYMENT_CURRENCY'] = get_premium_payment_currency(self.acm_obj)
            val_dict['PREMIUM_PAYMENT_AMOUNT'] = get_premium_payment_amount(self.acm_obj)
        return val_dict

    # formatter
    def _format_premium_payment_34R(self, val_dict):
        premium_payment_date = val_dict.get('PREMIUM_PAYMENT_DATE')
        premium_payment_currency = val_dict.get('PREMIUM_PAYMENT_CURRENCY')
        premium_payment_amount = val_dict.get('PREMIUM_PAYMENT_AMOUNT')
        date_format = '%y%m%d'

        if premium_payment_amount and premium_payment_currency and premium_payment_date:
            premium_payment_date = FSwiftWriterUtils.format_date(premium_payment_date, date_format)
            premium_payment_amount = apply_currency_precision(premium_payment_currency, float(premium_payment_amount))
            val = premium_payment_date + premium_payment_currency + FSwiftMLUtils.float_to_swiftmt(str(premium_payment_amount))
            return str(val)

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_34R_Type)
    def _validate_premium_payment_34R(self, val):
        premium_payment = val
        validate_currency_amount(premium_payment[6:], "Premium Payment")
        premium_amount = get_amount_from_currency_amount(premium_payment[6:])
        validateAmount(premium_amount.replace('.', ','), 15, "Premium Payment")
        return val

    # setter
    def _setpremium_payment_34R(self, val):
       self.swift_obj.SequenceA_GeneralInformation.PremiumPayment_R = val
       self.swift_obj.SequenceA_GeneralInformation.PremiumPayment_R.swiftTag = "34R"

    # getter
    def premium_payment_34P(self):
        ''' Returns dictionary with keys 'PREMIUM_PAYMENT_DATE', 'PREMIUM_PAYMENT_CURRENCY', 'PREMIUM_PAYMENT_AMOUNT' and their corresponding values '''
        if self.use_operations_xml:
            val_dict = {}
            premium_payment_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                            ['SWIFT', 'PREMIUM_PAYMENT_DATE'])
            premium_payment_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                ['SWIFT', 'PREMIUM_PAYMENT_CURRENCY'])
            premium_payment_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                              ['SWIFT', 'PREMIUM_PAYMENT_AMOUNT'])
            premium_payment_amount = apply_currency_precision(premium_payment_currency,
                                                                                   float(premium_payment_amount))
            val_dict['PREMIUM_PAYMENT_DATE'] = premium_payment_date
            val_dict['PREMIUM_PAYMENT_CURRENCY'] = premium_payment_currency
            val_dict['PREMIUM_PAYMENT_AMOUNT'] = premium_payment_amount
        else:
            val_dict = {}
            val_dict['PREMIUM_PAYMENT_DATE'] = get_premium_payment_date(self.acm_obj)
            val_dict['PREMIUM_PAYMENT_CURRENCY'] = get_premium_payment_currency(self.acm_obj)
            val_dict['PREMIUM_PAYMENT_AMOUNT'] = get_premium_payment_amount(self.acm_obj)
        return val_dict

    # formatter
    def _format_premium_payment_34P(self, val_dict):
        premium_payment_date = val_dict.get('PREMIUM_PAYMENT_DATE')
        premium_payment_currency = val_dict.get('PREMIUM_PAYMENT_CURRENCY')
        premium_payment_amount = val_dict.get('PREMIUM_PAYMENT_AMOUNT')
        date_format = '%y%m%d'

        if premium_payment_amount and premium_payment_currency and premium_payment_date:
            premium_payment_date = FSwiftWriterUtils.format_date(premium_payment_date, date_format)
            premium_payment_amount = apply_currency_precision(premium_payment_currency, float(premium_payment_amount))
            val = premium_payment_date + premium_payment_currency + FSwiftMLUtils.float_to_swiftmt(str(premium_payment_amount))
            return str(val)

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_34P_Type)
    def _validate_premium_payment_34P(self, val):
        premium_payment = val
        validate_currency_amount(premium_payment[6:], "Premium Payment")
        premium_amount = get_amount_from_currency_amount(premium_payment[6:])
        validateAmount(premium_amount.replace('.', ','), 15, "Premium Payment")
        return val

    # setter
    def _setpremium_payment_34P(self, val):
        self.swift_obj.SequenceA_GeneralInformation.PremiumPayment_P = val
        self.swift_obj.SequenceA_GeneralInformation.PremiumPayment_P.swiftTag = "34P"


    # ------------------ senders_correspondent -----------------------

    # option getter
    def get_senders_correspondent_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_senders_correspondent(self):
        '''Returns name of the getter like 'senders_correspondent_53A',  'senders_correspondent_53D' '''
        if self.use_operations_xml:
            senders_correspondent_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                ['SWIFT', 'SENDER_CORRESPONDENT_OPTION']
                                                                                , ignore_absense=True)
        else:
            senders_correspondent_option = self.get_senders_correspondent_option()
        if senders_correspondent_option == "A":
            return 'senders_correspondent_53A'
        elif senders_correspondent_option == "D":
            return 'senders_correspondent_53D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,
                                                                                                 str(senders_correspondent_option),
                                                                                                 'SendersCorrespondent_53a'))
        return 'senders_correspondent_53A'

    # getter
    def senders_correspondent_53A(self):
        '''Returns dictionary with keys 'ACCOUNT', 'BIC' and their correpsonding amount '''
        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SENDER_CORRESPONDENT_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SENDER_CORRESPONDENT_BIC'])
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            return get_acquirer_delivery_agent_details(self.acm_obj)



    # formatter
    def _format_senders_correspondent_53A(self, val):
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_53A_Type)
    def _validate_senders_correspondent_53A(self, val):
        return val

    # setter
    def _setsenders_correspondent_53A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.SendersCorrespondent_A = val
        self.swift_obj.SequenceA_GeneralInformation.SendersCorrespondent_A.swiftTag = "53A"


    # getter
    def senders_correspondent_53D(self):
        '''Returns dictionary with keys 'NAME','ADDRESS', 'ACCOUNT' and their corresponding values  '''
        if self.use_operations_xml:
            values_dict = {}

            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SENDER_CORRESPONDENT_ACCOUNT'],
                                                               ignore_absense=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                            ['SWIFT', 'SENDER_CORRESPONDENT_NAME'],
                                                            ignore_absense=True)
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SENDER_CORRESPONDENT_ADDRESS'],
                                                               ignore_absense=True)
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            return values_dict
        else:
            return get_acquirer_delivery_agent_details(self.acm_obj)


    # formatter
    def _format_senders_correspondent_53D(self, val):
        name = val.get('NAME')
        account = val.get('ACCOUNT')
        address = val.get('ADDRESS')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_53D_Type)
    def _validate_senders_correspondent_53D(self, val):
        return val

    # setter
    def _setsenders_correspondent_53D(self, val):
        self.swift_obj.SequenceA_GeneralInformation.SendersCorrespondent_D = val
        self.swift_obj.SequenceA_GeneralInformation.SendersCorrespondent_D.swiftTag = "53D"

    # ------------------ sell_intermediary -----------------------

    # option getter
    def get_intermediary_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_intermediary(self):
        '''Returns name of the getter like 'intermediary_56A',  'intermediary_56D' '''
        if self.use_operations_xml:
            intermediary_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                       ['SWIFT', 'INTERMEDIARY_OPTION'],
                                                                       ignore_absense=True)
        else:
            intermediary_option = self.get_intermediary_option()
        if intermediary_option == "A":
            return 'intermediary_56A'
        elif intermediary_option == "D":
            return 'intermediary_56D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,
                                                                                                 str(intermediary_option),
                                                                                                 'Intermediary_56a'))
        return 'intermediary_56A'

    # getter
    def intermediary_56A(self):
        '''Returns dictionary with keys 'ACCOUNT', 'BIC' and their corresponding values  '''
        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'INTERMEDIARY_ACCOUNT'], ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'INTERMEDIARY_BIC'])

            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            return get_counterparty_intermediary_details(self.acm_obj)

    # formatter
    def _format_intermediary_56A(self, val):
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_56A_Type)
    def _validate_intermediary_56A(self, val):
        return val

    # setter
    def _setintermediary_56A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.Intermediary_A = val
        self.swift_obj.SequenceA_GeneralInformation.Intermediary_A.swiftTag = "56A"


    # getter
    def intermediary_56D(self):
        '''Returns dictionary with keys 'NAME', 'ACCOUNT', 'ADDRESS' and their corresponding values  '''
        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_INTERMEDIARY_ACCOUNT'],
                                                               ignore_absense=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SELL_INTERMEDIARY_NAME']
                                                            , ignore_absense=True)
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SELL_INTERMEDIARY_ADDRESS'],
                                                               ignore_absense=True)
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            return values_dict
        else:
            return get_counterparty_intermediary_details(self.acm_obj)


    # formatter
    def _format_intermediary_56D(self, val):
        name = val.get('NAME')
        account = val.get('ACCOUNT')
        address = val.get('ADDRESS')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_56D_Type)
    def _validate_intermediary_56D(self, val):
        return val

    # setter
    def _setintermediary_56D(self, val):
        self.swift_obj.SequenceA_GeneralInformation.Intermediary_D = val
        self.swift_obj.SequenceA_GeneralInformation.Intermediary_D.swiftTag = "56D"

    # ------------------ sell_beneficiary_institution -----------------------

    # option getter
    def get_account_with_institution_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option


    # setter
    def _set_OPTION_account_with_institution(self):
        '''Returns name of the getter like 'sell_account_with_institution_57A', 'sell_account_with_institution_57D' '''
        if self.use_operations_xml:
            account_with_institution_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                   ['SWIFT',
                                                                                    'ACCOUNT_WITH_INSTITUTION_OPTION'])
        else:
            account_with_institution_option = self.get_account_with_institution_option()

        if account_with_institution_option == "A":
            return 'sell_account_with_institution_57A'
        elif account_with_institution_option == "D":
            return 'sell_account_with_institution_57D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,
                                                                                                 str(account_with_institution_option),
                                                                                                 'AccountWithInstitution_57a'))

        return 'sell_account_with_institution_57A'

    # getter
    def sell_account_with_institution_57A(self):
        '''Returns dictionary with keys 'ACCOUNT', 'BIC' and their corresponding values '''
        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_BIC'])
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            return get_counterparty_delivery_agent_details(self.acm_obj)

    # formatter
    def _format_sell_account_with_institution_57A(self, val):
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_57A_Type)
    def _validate_sell_account_with_institution_57A(self, val):
        return val

    # setter
    def _setsell_account_with_institution_57A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.AccountWithInstitution_A = val
        self.swift_obj.SequenceA_GeneralInformation.AccountWithInstitution_A.swiftTag = "57A"

    # getter
    def sell_account_with_institution_57D(self):
        '''Returns dictionary with keys 'ACCOUNT', 'NAME', 'ADDRESS' and their corresponding values '''
        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_ACCOUNT'],
                                                               ignore_absense=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                            ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_NAME'])
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_ADDRESS'])
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            return values_dict
        else:
            return get_counterparty_delivery_agent_details(self.acm_obj)

    # formatter
    def _format_sell_account_with_institution_57D(self, val):
        name = val.get('NAME')
        account = val.get('ACCOUNT')
        address = val.get('ADDRESS')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_57D_Type)
    def _validate_sell_account_with_institution_57D(self, val):
        return val

    # setter
    def _setsell_account_with_institution_57D(self, val):
       self.swift_obj.SequenceA_GeneralInformation.AccountWithInstitution_D = val
       self.swift_obj.SequenceA_GeneralInformation.AccountWithInstitution_D.swiftTag = "57D"

    # ------------------ sender_to_receiver_info_details -----------------------
    # getter
    def sender_to_receiver_info_72(self):
        ''' Returns sender to receiver information as string  '''
        if self.use_operations_xml:
            sender_to_receiver_info = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'SENDER_TO_RECEIVER_INFO'],
                                                                           ignore_absense=True)
        else:
            sender_to_receiver_info = get_sender_to_recieverinfo(self.acm_obj)

        return sender_to_receiver_info

    # formatter
    def _format_sender_to_receiver_info_72(self, val):
        lines = FSwiftWriterUtils.split_text_on_character_limit(val, 35)
        val = FSwiftWriterUtils.allocate_space_for_n_lines(6, lines)
        return val

    # validator
    @validate_with(MT305.MT305_SequenceA_GeneralInformation_72_Type)
    def _validate_sender_to_receiver_info_72(self, val):
        return val

    # setter
    def _set_sender_to_receiver_info_72(self, val):
        self.swift_obj.SequenceA_GeneralInformation.SenderToReceiverInformation = val
        self.swift_obj.SequenceA_GeneralInformation.SenderToReceiverInformation.swiftTag = "72"



class FMT305OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_typ = "305"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT'+ self.mt_typ)

        super(FMT305OutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

    def message_type(self):
        return "305"

    def sender_logical_terminal_address(self):
        '''LT code is hardcoded as A for sender'''
        terminal_address = ""
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
        terminal_address = ""
        receivers_bic = ''
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'RECEIVER_BIC'])
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


class FMT305OutBaseNetworkRules(object):
    ''' '''

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.acm_obj = acm_obj

    def network_rule_C1(self):
        '''C1 Field 31C may only be present when field 23 specifies an American style option (Error code(s): C79).'''
        if not "/A/" in self.swift_message_obj.SequenceA_GeneralInformation.FurtherIdentification.value():
            if self.swift_message_obj.SequenceA_GeneralInformation.EarliestExerciseDate:
                return "Field 31C may only be present when field 23 specifies an American style option"
        return ''

    def network_rule_C2(self):
        '''C2 The currency code in subfield 4 of field 23 must be the same as the currency code in field 32B (Error code(s): C88).'''
        field23_subfields = str(self.swift_message_obj.SequenceA_GeneralInformation.FurtherIdentification.value()).split('/')
        if not field23_subfields[3] == str(self.swift_message_obj.SequenceA_GeneralInformation.UnderlyingCurrencyNAmount.value())[:3]:
            return "The currency code in subfield 4 of field 23 must be the same as the currency code in field 32B"
        return ''


##    def network_rule_C3(self):
##        '''C3 In sequence B, if field 15B is present then at least one of the other fields of sequence B must be present (Error code(s): C98).'''
##        if self.swift_message_obj.REPINFO:
##            if not self.swift_message_obj.REPINFO.REPPARTY or not self.swift_message_obj.SequenceA_GeneralInformation.RelatedReference.value():
##                return 'Field 21 in Sequence A is mandatory if field 22A in Sequence A is equal to either AMND or CANC'
##        return ''



