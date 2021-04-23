"""----------------------------------------------------------------------------
MODULE:
    FMT320InBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module opened to display the logic to extract attributes
    from swift message and an acm object but the user should NOT edit it.
    User can extend/override default mapping in derived class i.e. FMT320In
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
import acm
import FMT30X
import FSwiftMLUtils
import re
import FSwiftOperationsAPI
import FIntegrationUtils
acm_version = FIntegrationUtils.FIntegrationUtils.get_acm_version()
if acm_version < 2018.2:
    from FOperationsEnums import CashFlowType
else:
    CashFlowType = FSwiftOperationsAPI.GetCashFlowTypeEnum()
from FFXMMConfirmationInUtils import *

class FMT320Base(FMT30X.FMT30X):
    """ Base class for MT320 mapping"""
    def __init__(self, source, direction):
        super(FMT320Base, self).__init__(source, direction)
        self._message_type = 'MT320'
        self.config_param = FSwiftMLUtils.Parameters('FMT320In_Config')

        self._scope_of_operation           = None
        self._common_reference             = None
        self._fund_or_instructing_party    = None
        self._terms_and_conditions         = None

        self._trade_date       = None
        self._value_date       = None
        self._maturity_date    = None
        self._interest_rate    = None

        self._currency         = None
        self._principal_amount = None
        self._interest_amount  = None


        self._counterParty_delivery_agent          = None
        self._counterParty_intermediary            = None
        self._counterParty_receiving_agent         = None
        self._counterParty_beneficiary_institution = None


        self._acquirer_delivery_agent              = None
        self._acquirer_intermediary                = None
        self._acquirer_receiving_agent             = None
        self._acquirer_beneficiary_institution     = None

        self._contact_information          = None
        self._dealing_method               = None
        self._dealing_branch_acquirer      = None
        self._dealing_branch_cpty          = None
        self._broker_identification        = None
        self._broker_commission            = None
        self._counterparty_reference       = None
        self._broker_reference             = None
        self._sender_receiver_information  = None

        self._acquirer_role = None
        self._day_count_fraction = None
        self._amount_to_be_settled = None





# ------------------------------------------------------------------------------
    def SetAttributes(self):
        """ Set the attributes from incoming swift message/acm object to MT320"""
        try:
            if self.source == 'SWIFT':
                self.set_id_sender_reference()
                self.set_related_reference()
                self.set_message_function()
                self.set_scope_of_operation()
                self.set_common_reference()
                self.set_acquirer()
                self.set_counterparty()
                self.set_fund_or_instructing_party()
                self.set_terms_and_conditions()

                self.set_trade_date()
                self.set_value_date()
                self.set_maturity_date()
                self.set_interest_rate()

                self.set_cur_and_pricipal_amount()
                self.set_interest_amount()


                self.set_counter_party_intermediary()
                self.set_acquirer_intermediary()

                self.set_counter_party_delivery_agent()
                self.set_acquirer_delivery_agent()

                self.set_counter_party_receiving_agent()
                self.set_acquirer_receiving_agent()

                self.set_counter_party_beneficiary_institution()
                self.set_acquirer_beneficiary_institution()

                self.set_contact_information()
                self.set_dealing_method()
                self.set_dealing_branch_acquirer()
                self.set_dealing_branch_cpty()
                self.set_broker_identification()
                self.set_broker_commission()
                self.set_counterparty_reference()
                self.set_broker_reference()
                self.set_sender_receiver_information()

                self.set_acquirer_role()
                self.set_day_count_fraction()
                self.set_type_of_event()
                self.set_amount_to_be_settled()
                self.ext_ref = self.InternalIdentifier()

            elif self.source == 'ACM':
                self.set_original_trade_attributes()
                self.set_trade_date_from_trade()
                self.set_value_date_from_trade()
                self.set_maturity_date_from_trade()

                self.set_interest_rate_from_trade()
                self.set_currency_from_trade()
                self.set_pricipal_amount_from_trade()
                self.set_interest_amount_from_trade()

                self.set_acquirer_counterparty_from_trade()
                self.set_acquirer_counterparty_intermediary_from_trade()
                self.set_acquirer_counterparty_receiving_agent_from_trade()

                self.set_acquirer_role_from_trade()
                self.set_day_count_fraction_from_trade()
                self.set_type_of_event_from_trade()
                self.set_message_function_from_trade()
                self.set_amount_to_be_settled_from_trade()
        except Exception as e:
            notifier.ERROR("Exception occurred in SetAttributes : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

# ------------------------------------------------------------------------------
    def get_original_trade_tag_list(self, conf_obj):
        """
        This function extracts the swift message of the related confirmation
        :param conf_obj:
        :return:
        """
        ref_number = {}
        ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=conf_obj, integration_type="Outgoing")
        swift_message = FSwiftMLUtils.FSwiftExternalObject.get_stored_data(ext_obj, "swift_data")
        if swift_message:
            swift_msg_list = FSwiftMLUtils.swift_message_to_list(swift_message)
            for tag_list in swift_msg_list:
                if tag_list[0] == '20':
                    ref_number['senders_ref'] = tag_list[1]
                elif tag_list[0] == '17R':
                    ref_number['partyA_role'] = tag_list[1]
                elif tag_list[0] == '30T':
                    ref_number['trade_date'] = tag_list[1]
                elif tag_list[0] == '30V':
                    ref_number['value_date'] = tag_list[1]

        return ref_number

    def set_original_trade_attributes(self):
        """
        This function retrieves the attributes of related trade.
        :return:
        """
        import FSwiftConfirmationUtils
        type_of_event = FSwiftConfirmationUtils.get_event_type(self.acm_obj)

        self.original_trade_partyA_role = None
        self.original_value_date = None
        self.original_trade_date = None

        if type_of_event == "MATU" and self.acm_obj.EventType() != "Deposit Maturity":
            original_trade = self.acm_obj.Trade().ContractTrade()
            if original_trade.Type() == "Normal":
                for conf in original_trade.Confirmations():
                    if conf.IsNewestInConfirmationChain():
                        original_trade_msg_dict =  self.get_original_trade_tag_list(conf)
                        self.original_trade_partyA_role = original_trade_msg_dict.get('partyA_role')
                        self.original_trade_date = original_trade_msg_dict.get('trade_date')
                        self.original_value_date = original_trade_msg_dict.get('value_date')
                        break


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

    def set_type_of_event(self):
        try:
            self._type_of_event = str(self.python_object.SequenceA_GeneralInformation.TypeOfEvent.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_type_of_event : %s"%str(e))

    def set_amount_to_be_settled(self):
        try:
            if self.python_object.SequenceB_TransactionDetails.AmountToBeSettled:
                self._amount_to_be_settled = str(self.python_object.SequenceB_TransactionDetails.AmountToBeSettled.value())
                if self._amount_to_be_settled.startswith('N'):
                    self._amount_to_be_settled = FSwiftMLUtils.swiftmt_to_float(self._amount_to_be_settled[4:]) * -1
                else:
                    self._amount_to_be_settled = FSwiftMLUtils.swiftmt_to_float(self._amount_to_be_settled[3:])
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_amount_to_be_settled : %s" % str(e))


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

    def set_fund_or_instructing_party(self):
        try:
            if self.python_object.SequenceA_GeneralInformation.FundOrInstructingParty_A:
                self._fund_or_instructing_party = str(self.python_object.SequenceA_GeneralInformation.FundOrInstructingParty_A.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_fund_or_instructing_party : %s"%str(e))

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

    def set_maturity_date(self):
        try:
            if self.python_object.SequenceB_TransactionDetails.MaturityDate:
                self._maturity_date = FSwiftMLUtils.swiftmt_to_date(str(self.python_object.SequenceB_TransactionDetails.MaturityDate.value()))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_maturity_date : %s"%str(e))


    def set_interest_rate(self):
        try:
            if self.python_object.SequenceB_TransactionDetails.InterestRate:
                interest_rate = str(self.python_object.SequenceB_TransactionDetails.InterestRate.value())
                interest_index = re.search('\d', interest_rate).start()
                self._interest_rate = FSwiftMLUtils.swiftmt_to_float(interest_rate[interest_index:])

                if interest_index == 1:
                    self._interest_rate *= -1

        except Exception as e:
            notifier.DEBUG("Exception occurred in set_interest_rate : %s"%str(e))

    def set_cur_and_pricipal_amount(self):
        try:
            self._currency = str(self.python_object.SequenceB_TransactionDetails.CurrencyAndPrincipalAmount.value()[0:3])
            self._principal_amount = str(self.python_object.SequenceB_TransactionDetails.CurrencyAndPrincipalAmount.value()[3:])
            self._principal_amount = FSwiftMLUtils.swiftmt_to_float(self._principal_amount)
            self._principal_amount = apply_currency_precision(self._currency, self._principal_amount)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_cur_and_pricipal_amount : %s"%str(e))

    def __get_amount(self, reverse_sign=False):
        curr_interest_amt = str(self.python_object.SequenceB_TransactionDetails.CurrencyAndInterestAmount.value())
        interest_amt_index = re.search('\d', curr_interest_amt).start()

        interest_amt = curr_interest_amt[interest_amt_index:]

        _interest_amount = FSwiftMLUtils.swiftmt_to_float(interest_amt)
        if interest_amt_index == 4:
            interest_curr = curr_interest_amt[1:interest_amt_index]
        else:
            interest_curr = curr_interest_amt[0:interest_amt_index]
        _interest_amount = apply_currency_precision(interest_curr, _interest_amount)

        if reverse_sign:
            if interest_amt_index == 3:
                _interest_amount *= -1
        else:
            if interest_amt_index == 4:
                _interest_amount *= -1

        return _interest_amount

    def set_interest_amount(self):
        '''
        FORMAT

        Option E    [N]3!a15d    (Sign)(Currency)(Amount)
        '''
        try:
            self._interest_amount = self.__get_amount()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_interest_amount : %s"%str(e))

    def set_counter_party_delivery_agent(self):
        try:
            if self.direction == 'IN':
                self._counterParty_delivery_agent = self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.DeliveryAgent_A.value() if self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.DeliveryAgent_A else None
            else:
                self._counterParty_delivery_agent = self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.DeliveryAgent_A.value() if self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.DeliveryAgent_A else None

            if self._counterParty_delivery_agent:
                self._counterParty_delivery_agent = str(self.get_party_typeA(self._counterParty_delivery_agent))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_counter_party_delivery_agent : %s"%str(e))

    def set_acquirer_delivery_agent(self):
        try:
            if self.direction == 'IN':
                self._acquirer_delivery_agent = self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.DeliveryAgent_A.value() if self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.DeliveryAgent_A else None
            else:
                self._acquirer_delivery_agent = self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.DeliveryAgent_A.value() if self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.DeliveryAgent_A else None

            if self._acquirer_delivery_agent:
                self._acquirer_delivery_agent = str(self.get_party_typeA(self._acquirer_delivery_agent))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_delivery_agent : %s"%str(e))

    def set_counter_party_receiving_agent(self):
        try:
            if self.direction == 'IN':
                self._counterParty_receiving_agent = self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_A.value() if self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_A else None
            else:
                self._counterParty_receiving_agent = self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_A.value() if self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_A else None

            if self._counterParty_receiving_agent:
                self._counterParty_receiving_agent = str(self.get_party_typeA(self._counterParty_receiving_agent))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_counter_party_receiving_agent : %s"%str(e))

    def set_acquirer_receiving_agent(self):
        try:
            if self.direction == 'IN':
                self._acquirer_receiving_agent = self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_A.value() if self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_A else None
            else:
                self._acquirer_receiving_agent = self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_A.value() if self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_A else None

            if self._acquirer_receiving_agent:
                self._acquirer_receiving_agent = str(self.get_party_typeA(self._acquirer_receiving_agent))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_receiving_agent : %s"%str(e))

    def set_counter_party_intermediary(self):
        try:
            if self.direction == 'IN':
                self._counterParty_intermediary = self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary_A.value() if self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary_A else None
            else:
                self._counterParty_intermediary = self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary_A.value() if self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary_A else None

            if self._counterParty_intermediary:
                self._counterParty_intermediary = str(self.get_party_typeA(self._counterParty_intermediary))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_counter_party_intermediary : %s"%str(e))

    def set_acquirer_intermediary(self):
        try:
            if self.direction == 'IN':
                self._acquirer_intermediary = self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary_A.value() if self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary_A else None
            else:
                self._acquirer_intermediary = self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary_A.value() if self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary_A else None

            if self._acquirer_intermediary:
                self._acquirer_intermediary = str(self.get_party_typeA(self._acquirer_intermediary))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_intermediary : %s"%str(e))

    def set_counter_party_beneficiary_institution(self):
        try:
            if self.direction == 'IN':
                self._counterParty_beneficiary_institution = self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.BeneficiaryInstitution_A.value() \
                if self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.BeneficiaryInstitution_A else None
            else:
                self._counterParty_beneficiary_institution = self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.BeneficiaryInstitution_A.value() \
                if self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.BeneficiaryInstitution_A else None

                if self._counterParty_beneficiary_institution:
                    self._counterParty_beneficiary_institution = str(self.get_party_typeA(self._counterParty_beneficiary_institution))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_counter_party_beneficiary_institution : %s"%str(e))

    def set_acquirer_beneficiary_institution(self):
        try:
            if self.direction == 'IN':
                self._acquirer_beneficiary_institution = self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.BeneficiaryInstitution_A.value() \
                if self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.BeneficiaryInstitution_A else None
            else:
                self._acquirer_beneficiary_institution = self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.BeneficiaryInstitution_A.value() \
                if self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.BeneficiaryInstitution_A else None

                if self._acquirer_beneficiary_institution:
                    self._acquirer_beneficiary_institution = str(self.get_party_typeA(self._acquirer_beneficiary_institution))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_beneficiary_institution : %s"%str(e))

    def set_contact_information(self):
        try:
            if self.python_object.SequenceH_AdditionalInformation and self.python_object.SequenceH_AdditionalInformation.ContactInformation:
                self._contact_information = str(self.python_object.SequenceH_AdditionalInformation.ContactInformation.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_contact_information : %s"%str(e))

    def set_dealing_method(self):
        try:
            if self.python_object.SequenceH_AdditionalInformation and self.python_object.SequenceH_AdditionalInformation.DealingMethod:
                self._dealing_method = str(self.python_object.SequenceH_AdditionalInformation.DealingMethod.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_dealing_method : %s"%str(e))

    def set_dealing_branch_acquirer(self):
        try:
            if self.python_object.SequenceH_AdditionalInformation and self.python_object.SequenceH_AdditionalInformation.DealingBranchPartyA_A:
                self._dealing_branch_acquirer = str(self.python_object.SequenceH_AdditionalInformation.DealingBranchPartyA_A.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_dealing_branch_acquirer : %s"%str(e))

    def set_dealing_branch_cpty(self):
        try:
            if self.python_object.SequenceH_AdditionalInformation and self.python_object.SequenceH_AdditionalInformation.DealingBranchPartyB_A:
                self._dealing_branch_cpty = str(self.python_object.SequenceH_AdditionalInformation.DealingBranchPartyB_A.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_dealing_branch_cpty : %s"%str(e))

    def set_broker_identification(self):
        try:
            if self.python_object.SequenceH_AdditionalInformation and self.python_object.SequenceH_AdditionalInformation.BrokerIdentification_A:
                self._broker_identification = str(self.python_object.SequenceH_AdditionalInformation.BrokerIdentification_A.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_broker_identification : %s"%str(e))

    def set_broker_commission(self):
        try:
            if self.python_object.SequenceH_AdditionalInformation and self.python_object.SequenceH_AdditionalInformation.BrokersCommission:
                self._broker_commission = str(self.python_object.SequenceH_AdditionalInformation.BrokersCommission.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_broker_commission : %s"%str(e))

    def set_counterparty_reference(self):
        try:
            if self.python_object.SequenceH_AdditionalInformation and self.python_object.SequenceH_AdditionalInformation.CounterpartysReference:
                self._counterparty_reference = str(self.python_object.SequenceH_AdditionalInformation.CounterpartysReference.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_counterparty_reference : %s"%str(e))

    def set_broker_reference(self):
        try:
            if self.python_object.SequenceH_AdditionalInformation and self.python_object.SequenceH_AdditionalInformation.BrokersReference:
                self._broker_reference = str(self.python_object.SequenceH_AdditionalInformation.BrokersReference.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_broker_reference : %s"%str(e))

    def set_sender_receiver_information(self):
        try:
            if self.python_object.SequenceH_AdditionalInformation and self.python_object.SequenceH_AdditionalInformation.SenderToReceiverInformation:
                self._sender_receiver_information = str(self.python_object.SequenceH_AdditionalInformation.SenderToReceiverInformation.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_sender_receiver_information : %s"%str(e))

    def set_acquirer_role(self):
        try:
            self._acquirer_role = str(self.python_object.SequenceB_TransactionDetails.PartyAsRole.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_role : %s" % str(e))

    def set_day_count_fraction(self):
        try:
            self._day_count_fraction = str(self.python_object.SequenceB_TransactionDetails.DayCountFraction.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_day_count_fraction : %s" % str(e))



# ------------------------------------------------------------------------------
    # Method to fetch data from the adm
    def set_message_function_from_trade(self):
        try:
            import FFXMMConfirmationOutUtils
            if self.acm_obj.EventType() in ["Close", "Partial Close"]:
                self._message_function = 'NEWT'
            else:
                self._message_function = str(FFXMMConfirmationOutUtils.get_type_of_operation(self.acm_obj))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_message_function_trade : %s"%str(e))

    def set_type_of_event_from_trade(self):
        try:
            import FSwiftConfirmationUtils
            self._type_of_event = str(FSwiftConfirmationUtils.get_event_type(self.acm_obj))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_type_of_event_from_trade : %s"%str(e))

    def set_curr_amt_from_trade(self):
        try:
            pass
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_curr_amt_from_trade : %s"%str(e))

    def set_value_date_from_trade(self):
        try:
            if self.original_value_date:
                self._value_date = FSwiftMLUtils.swiftmt_to_date(self.original_value_date)
            else:
                self._value_date = self.acm_obj.Trade().ValueDay()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_value_date_from_trade : %s"%str(e))

    def set_maturity_date_from_trade(self):
        try:
            import FSwiftConfirmationUtils
            type_of_event = FSwiftConfirmationUtils.get_event_type(self.acm_obj)
            if type_of_event in ["MATU"] and self.acm_obj.EventType() != 'Deposit Maturity':
                self._maturity_date = self.acm_obj.Trade().ValueDay()
            else:
                self._maturity_date = self.acm_obj.Trade().Instrument().ExpiryDateOnly()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_maturity_date_from_trade : %s"%str(e))


    def set_trade_date_from_trade(self):
        try:
            if self.original_trade_date:
                self._trade_date = FSwiftMLUtils.swiftmt_to_date(self.original_trade_date)
            else:
                self._trade_date = self.acm_obj.Trade().TradeTime()[:10]
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_trade_date_from_trade : %s"%str(e))

    def set_interest_rate_from_trade(self):
        try:
            self._interest_rate = float(get_interest_rate(self.acm_obj))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_price_from_trade : %s"%str(e))

    def set_currency_from_trade(self):
        try:
            self._currency = self.acm_obj.Trade().Currency().Name()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_currency_from_trade : %s"%str(e))

    def set_pricipal_amount_from_trade(self):
        try:
            import FSwiftConfirmationUtils
            type_of_event = FSwiftConfirmationUtils.get_event_type(self.acm_obj)
            if type_of_event in ["MATU"] and self.acm_obj.EventType() != 'Deposit Maturity':
                self._principal_amount = abs(self.acm_obj.Trade().FaceValue())
            else:
                self._principal_amount = abs(self.acm_obj.Trade().Premium())

        except Exception as e:
            notifier.DEBUG("Exception occurred in set_pricipal_amount_from_trade : %s"%str(e))

    def set_interest_amount_from_trade(self):
        try:
            import FFXMMConfirmationOutUtils
            self._interest_amount = FFXMMConfirmationOutUtils.get_interest_amount(self.acm_obj)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_interest_amount_from_trade : %s"%str(e))

    def set_acquirer_counterparty_from_trade(self):
        try:
            for flw in self.acm_obj.Trade().MoneyFlows():
                if flw.Type() in ["Premium", "Payment Premium"]:
                    self.counterparty = flw.CounterpartyAccount().NetworkAlias().Name() if (flw.CounterpartyAccount() and flw.CounterpartyAccount().NetworkAlias()) else self.acm_obj.Counterparty().Swift()
                    self.acquirer = flw.AcquirerAccount().NetworkAlias().Name() if (flw.AcquirerAccount() and flw.AcquirerAccount().NetworkAlias()) else self.acm_obj.Acquirer().Swift()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_counterparty_from_trade in derived version : %s"%str(e))

    def set_acquirer_counterparty_intermediary_from_trade(self):
        try:
            for flw in self.acm_obj.Trade().MoneyFlows():
                if flw.Type() in ["Premium", "Premium 2", "Payment Premium"]:
                    self._counterParty_intermediary = flw.AcquirerAccount().Bic2().Alias() if flw.AcquirerAccount() and flw.AcquirerAccount().Bic2() else None
                    self._acquirer_intermediary = flw.CounterpartyAccount().Bic2().Alias() if flw.CounterpartyAccount() and flw.CounterpartyAccount().Bic2() else None
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_counterparty_intermediary_from_trade : %s"%str(e))

    def set_acquirer_counterparty_receiving_agent_from_trade(self):
        try:
            for flw in self.acm_obj.Trade().MoneyFlows():
                if flw.Type() in ["Premium", "Premium 2", "Payment Premium"]:
                    self._counterParty_receiving_agent = flw.AcquirerAccount().Bic().Alias() if flw.AcquirerAccount() and flw.AcquirerAccount().Bic() else None
                    self._acquirer_receiving_agent = flw.CounterpartyAccount().Bic().Alias() if flw.CounterpartyAccount() and flw.CounterpartyAccount().Bic() else None
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_counterparty_receiving_agent_from_trade : %s"%str(e))

    def set_acquirer_role_from_trade(self):
        try:
            import FSwiftConfirmationUtils
            type_of_event = FSwiftConfirmationUtils.get_event_type(self.acm_obj)
            if type_of_event in ["MATU"] and self.original_trade_partyA_role:
                self._acquirer_role = self.original_trade_partyA_role
            else:
                if self.acm_obj.Trade().Premium() < 0:
                    self._acquirer_role = 'L'
                else:
                    self._acquirer_role = 'B'


        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_counterparty_receiving_agent_from_trade : %s" % str(e))

    def set_day_count_fraction_from_trade(self):
        try:
            self._day_count_fraction = get_day_count_fraction(self.acm_obj)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_day_count_fraction_from_trade : %s" % str(e))

    def set_amount_to_be_settled_from_trade(self):
        try:
            import FFXMMConfirmationOutUtils
            settle_amt = FFXMMConfirmationOutUtils.get_settle_amount_MT320(self.acm_obj)
            if settle_amt:
                self._amount_to_be_settled = float(settle_amt)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_amount_to_be_settled_from_trade : %s" % str(e))


# ------------------------------------------------------------------------------
    # Method to fetch data used in the Pairing and Matching attributes in the FParameter
    def SendersReference(self):
        return self._identifier

    def TypeOfOperation(self):
        return self._message_function

    def TypeOfEvent(self):
        return self._type_of_event

    def ScopeOfOperation(self):
        return self._scope_of_operation

    def CommonReference(self):
        return self._common_reference

    def FundOrInstructingParty(self):
        return self._fund_or_instructing_party

    def TermsAndConditions(self):
        return self._terms_and_conditions

    def TradeDate(self):
        return self._trade_date

    def ValueDate(self):
        return self._value_date

    def MaturityDate(self):
        return self._maturity_date

    def InterestRate(self):
        return self._interest_rate

    def Currency(self):
        return self._currency

    def PrincipalAmount(self):
        return self._principal_amount

    # def InterestAmount(self):
    #     return self._interest_amount

    def InterestAmount(self):
        ret_val = ''
        if self._swap_field_flag == False:
            ret_val = self._interest_amount
        else:
            if self.direction == "IN":
                ret_val = self.__get_amount(reverse_sign=True)
        return ret_val

    def CounterpartyDeliveryAgent(self):
        return self._counterParty_delivery_agent

    def CounterpartyReceivingAgent(self):
        return self._counterParty_receiving_agent

    def CounterpartyIntermediary(self):
        return self._counterParty_intermediary

    def CounterpartyBeneficiaryInstitution(self):
        return self._counterParty_beneficiary_institution

    def AcquirerDeliveryAgent(self):
        return self._acquirer_delivery_agent

    def AcquirerReceivingAgent(self):
        return self._acquirer_receiving_agent

    def AcquirerIntermediary(self):
        return self._acquirer_intermediary

    def AcquirerBeneficiaryInstitution(self):
        return self._acquirer_beneficiary_institution

    def ContactInformation(self):
        return self._contact_information

    def DealingMethod(self):
        return self._dealing_method

    def DealingBranchAcquirer(self):
        return self._dealing_branch_acquirer

    def DealingBranchCounterparty(self):
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

    def AcquirerRole(self):
        ret_val = ''
        if self._swap_field_flag == False:
            ret_val = str(self._acquirer_role)
        else:
            if self.direction == "IN":
                if self.python_object.SequenceB_TransactionDetails.PartyAsRole.value() == 'B':
                    ret_val = 'L'
                else:
                    ret_val = 'B'
        return ret_val

    def DayCountFraction(self):
        return self._day_count_fraction

    # +------------------------------------------------------------------------------------------+
    # |             Getters to represent the real side of the incoming message                   |
    # +------------------------------------------------------------------------------------------+

    def RealCounterpartyDeliveryAgent(self):
        try:
            agent = self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.DeliveryAgent_A.value() if self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.DeliveryAgent_A else None
            if agent:
                agent = str(self.get_party_typeA(agent))
            return agent
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealCounterpartyDeliveryAgent : %s"%str(e))


    def RealCounterpartyReceivingAgent(self):
        try:
            agent = self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_A.value() if self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_A else None
            if agent:
                agent = str(self.get_party_typeA(agent))
            return agent
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealCounterpartyReceivingAgent : %s"%str(e))


    def RealCounterpartyIntermediary(self):
        try:
            intermediary = self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary_A.value() if self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary_A else None
            if intermediary:
                intermediary = str(self.get_party_typeA(intermediary))
            return intermediary
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealCounterpartyIntermediary : %s"%str(e))


    def RealCounterpartyBeneficiaryInstitution(self):
        try:
            institution = self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.BeneficiaryInstitution_A.value() if self.python_object.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.BeneficiaryInstitution_A else None
            if institution:
                institution = str(self.get_party_typeA(institution))
            return institution
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealCounterpartyBeneficiaryInstitution : %s"%str(e))


    def RealAcquirerDeliveryAgent(self):
        try:
            agent = self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.DeliveryAgent_A.value() if self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.DeliveryAgent_A else None
            if agent:
                agent = str(self.get_party_typeA(agent))
            return agent
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealAcquirerDeliveryAgent : %s" % str(e))


    def RealAcquirerReceivingAgent(self):
        try:
            agent = self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_A.value() if self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_A else None
            if agent:
                agent = str(self.get_party_typeA(agent))
            return agent
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealAcquirerReceivingAgent : %s" % str(e))


    def RealAcquirerIntermediary(self):
        try:
            intermediary = self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary_A.value() if self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary_A else None

            if intermediary:
                intermediary = str(self.get_party_typeA(intermediary))
            return intermediary
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealAcquirerIntermediary : %s"%str(e))


    def RealAcquirerBeneficiaryInstitution(self):
        try:
            institution = self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.BeneficiaryInstitution_A.value() if self.python_object.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.BeneficiaryInstitution_A else None
            if institution:
                institution = str(self.get_party_typeA(institution))
            return institution
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealAcquirerBeneficiaryInstitution : %s"%str(e))

    @staticmethod
    def GetColumnMetaData():
        column_metadata = {
            'TypeOfEvent': {'THEIRS_SWIFT_TAG': '22B', 'OURS_SWIFT_TAG': '22B', 'SEQUENCE': 'General Information','COLOR': ''},
            'SendersReference': {'THEIRS_SWIFT_TAG' : '20', 'OURS_SWIFT_TAG' : '20', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'RelatedReference': {'THEIRS_SWIFT_TAG' : '21', 'OURS_SWIFT_TAG' : '21', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'TypeOfOperation': {'THEIRS_SWIFT_TAG' : '22A', 'OURS_SWIFT_TAG' : '22A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'ScopeOfOperation': {'THEIRS_SWIFT_TAG' : '94A', 'OURS_SWIFT_TAG' : '94A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'CommonReference': {'THEIRS_SWIFT_TAG' : '22C', 'OURS_SWIFT_TAG' : '22C', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'Acquirer': {'REAL_GETTER' : 'RealAcquirer', 'REAL_SWIFT_TAG' : '82A', 'THEIRS_SWIFT_TAG' : '87A', 'OURS_SWIFT_TAG' : '82A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'Counterparty': {'REAL_GETTER' : 'RealCounterparty', 'REAL_SWIFT_TAG' : '87A', 'THEIRS_SWIFT_TAG' : '82A', 'OURS_SWIFT_TAG' : '87A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'FundOrInstructingParty': {'THEIRS_SWIFT_TAG' : '83A', 'OURS_SWIFT_TAG' : '83A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'TermsAndConditions': {'THEIRS_SWIFT_TAG' : '77D', 'OURS_SWIFT_TAG' : '77D', 'SEQUENCE': 'General Information', 'COLOR': ''},

            'AcquirerRole': {'REAL_SWIFT_TAG': '17R', 'THEIRS_SWIFT_TAG': '17R','OURS_SWIFT_TAG': '17R', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'TradeDate': {'THEIRS_SWIFT_TAG' : '30T', 'OURS_SWIFT_TAG' : '30T', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'ValueDate': {'THEIRS_SWIFT_TAG' : '30V', 'OURS_SWIFT_TAG' : '30V', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'MaturityDate': {'THEIRS_SWIFT_TAG' : '30P', 'OURS_SWIFT_TAG' : '30P', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'InterestRate': {'THEIRS_SWIFT_TAG' : '37G', 'OURS_SWIFT_TAG' : '37G', 'SEQUENCE': 'Transaction Details', 'COLOR': '','FORMAT':'NumDefault'},
            'InterestAmount': {'THEIRS_SWIFT_TAG': '34E', 'OURS_SWIFT_TAG': '34E', 'SEQUENCE': 'Transaction Details','COLOR': '', 'FORMAT': 'NumDefault'},
            'Currency': {'THEIRS_SWIFT_TAG' : '32B', 'OURS_SWIFT_TAG' : '32B', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'PrincipalAmount': {'THEIRS_SWIFT_TAG' : '32B', 'OURS_SWIFT_TAG' : '32B', 'SEQUENCE': 'Transaction Details', 'COLOR': '','FORMAT':'NumDefault'},
            'DayCountFraction': {'THEIRS_SWIFT_TAG': '14D', 'OURS_SWIFT_TAG': '14D', 'SEQUENCE': 'Transaction Details','COLOR': ''},


            #Acquirer party
            'AcquirerIntermediary': {'REAL_GETTER' : 'RealAcquirerIntermediary', 'REAL_SWIFT_TAG' : '56A','THEIRS_SWIFT_TAG' : '56A', 'OURS_SWIFT_TAG' : '56A', 'SEQUENCE': 'Sett Instr for Amt of Acquirer', 'COLOR': ''},
            'AcquirerReceivingAgent': {'REAL_GETTER' : 'RealAcquirerReceivingAgent', 'REAL_SWIFT_TAG' : '57A','THEIRS_SWIFT_TAG' : '57A', 'OURS_SWIFT_TAG' : '57A', 'SEQUENCE': 'Sett Instr for Amt of Acquirer', 'COLOR': ''},
            'AcquirerDeliveryAgent': {'REAL_GETTER': 'RealAcquirerDeliveryAgent', 'REAL_SWIFT_TAG': '53A','THEIRS_SWIFT_TAG': '57A', 'OURS_SWIFT_TAG': '57A', 'SEQUENCE': 'Sett Instr for Amt of Acquirer','COLOR': ''},


            #Counterparty
            'CounterpartyIntermediary': {'REAL_GETTER' : 'RealCounterpartyIntermediary', 'REAL_SWIFT_TAG' : '56A', 'THEIRS_SWIFT_TAG' : '56A', 'OURS_SWIFT_TAG' : '56A', 'SEQUENCE': 'Sett Instr for Amt of Counterparty', 'COLOR': ''},
            'CounterpartyReceivingAgent': {'REAL_GETTER' : 'RealCounterpartyReceivingAgent', 'REAL_SWIFT_TAG' : '57A', 'THEIRS_SWIFT_TAG' : '57A', 'OURS_SWIFT_TAG' : '57A', 'SEQUENCE': 'Sett Instr for Amt of Counterparty', 'COLOR': ''},
            'CounterpartyDeliveryAgent': {'REAL_GETTER': 'RealCounterpartyDeliveryAgent', 'REAL_SWIFT_TAG': '53A','THEIRS_SWIFT_TAG': '53A', 'OURS_SWIFT_TAG': '53A', 'SEQUENCE': 'Sett Instr for Amt of Counterparty',                                      'COLOR': ''},


            'ContactInformation': {'THEIRS_SWIFT_TAG' : '29A', 'OURS_SWIFT_TAG' : '29A', 'SEQUENCE': 'Optional Additional Information', 'COLOR': ''},
            'DealingMethod': {'THEIRS_SWIFT_TAG' : '24D', 'OURS_SWIFT_TAG' : '24D', 'SEQUENCE': 'Optional Additional Information', 'COLOR': ''},
            'DealingBranchAcquirer': {'THEIRS_SWIFT_TAG' : '84A', 'OURS_SWIFT_TAG' : '84A', 'SEQUENCE': 'Optional Additional Information', 'COLOR': ''},
            'DealingBranchCounterparty': {'THEIRS_SWIFT_TAG' : '85A', 'OURS_SWIFT_TAG' : '85A', 'SEQUENCE': 'Optional Additional Information', 'COLOR': ''},
            'BrokerIdentification': {'THEIRS_SWIFT_TAG' : '88A', 'OURS_SWIFT_TAG' : '88A', 'SEQUENCE': 'Optional Additional Information', 'COLOR': ''},
            'BrokerCommission': {'THEIRS_SWIFT_TAG' : '71F', 'OURS_SWIFT_TAG' : '71F', 'SEQUENCE': 'Optional Additional Information', 'COLOR': ''},
            'CounterpartyReference': {'THEIRS_SWIFT_TAG' : '26H', 'OURS_SWIFT_TAG' : '26H', 'SEQUENCE': 'Optional Additional Information', 'COLOR': ''},
            'BrokerReference': {'THEIRS_SWIFT_TAG' : '21G', 'OURS_SWIFT_TAG' : '21G', 'SEQUENCE': 'Optional Additional Information', 'COLOR': ''},
            'SenderToReceiverInformation': {'THEIRS_SWIFT_TAG' : '72', 'OURS_SWIFT_TAG' : '72', 'SEQUENCE': 'Optional Additional Information', 'COLOR': ''},

            }
        return column_metadata

    @staticmethod
    def GetColumnNamePrefix():
        return 'MT320'


# Helper methods for FMT320Base

def get_interest_rate(confirmation):
    ''' Mandatory field 37G in seq B '''
    cashFlow = get_fixed_rate_cash_flow(confirmation)
    if cashFlow:
        return swift_numeric_formatter(cashFlow.FixedRate())
    return 0

def get_day_count_fraction(confirmation):
    """returns day count fraction of the trade"""
    day_count_fraction = ''
    legs = confirmation.Trade().Instrument().Legs()
    if legs:
        leg = legs[0]
        day_count_fraction = leg.DayCountMethod().upper()

        day_count_mapping = {'30E/360': '30E/360',
                             '30/360': '360/360',
                             '30U/360': '360/360',
                             'NL/360': '360/360',
                             'NL/365': 'ACT/365',
                             'NL/ActISDA': 'ACT/365',
                             '360/360': '360/360',
                             'Actual/360': 'ACT/360',
                             'Act/360': 'ACT/360',
                             'Act/365': 'ACT/365',
                             'Act/365L': 'ACT/365',
                             'ACT/ACTISDA': 'ACT/365',
                             'ACT/ACTISMA': 'ACT/365',
                             'ACT/ACTICMA': 'ACT/365',
                             'ACT/ACTAFB': 'ACT/365',
                             }
        day_count_fraction = day_count_mapping.get(day_count_fraction, day_count_fraction)

    return day_count_fraction

def get_fixed_rate_cash_flow(confirmation):
    return get_rate_cash_flow(CashFlowType.FIXED_RATE, confirmation)

def get_rate_cash_flow(cashFlowType, confirmation):
    assert confirmation.Trade().Instrument().Legs(), "The instrument referenced by the trade referenced by the confirmation has no legs"
    leg = confirmation.Trade().Instrument().Legs().First()
    selection = acm.FCashFlow.Select('leg = %d and cashFlowType = "%s"' % (leg.Oid(), cashFlowType))
    if (selection.Size() > 0):
        return selection.SortByProperty('StartDate').First()
    return None

def swift_numeric_formatter(value):
    # slicing for SWIFT std 12d. #
    value = str(value)
    if len(value) > 12:
        value = value[:12]
    return value
