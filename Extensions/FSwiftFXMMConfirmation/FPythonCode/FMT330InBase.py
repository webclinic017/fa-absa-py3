"""----------------------------------------------------------------------------
MODULE:
    FMT330InBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module opened to display the logic to extract attributes
    from swift message and an acm object but the user should NOT edit it.
    User can extend/override default mapping in derived class i.e. FMT330
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
import FSwiftWriterUtils
#import FSwiftMT330
import re
import FSwiftOperationsAPI
import FIntegrationUtils
acm_version = FIntegrationUtils.FIntegrationUtils.get_acm_version()
if acm_version < 2018.2:
    from FOperationsEnums import CashFlowType, LegType
else:
    CashFlowType = FSwiftOperationsAPI.GetCashFlowTypeEnum()
    LegType = FSwiftOperationsAPI.GetLegTypeEnum()


class FMT330Base(FMT30X.FMT30X):
    """ Base class for MT330 mapping"""
    def __init__(self, source, direction):
        super(FMT330Base, self).__init__(source, direction)
        self.config_param = FSwiftMLUtils.Parameters('FMT330In_Config')
        self._message_type = 'MT330'
        self._scope_of_operation           = None
        self._common_reference             = None
        self._fund_or_instructing_party    = None
        self._terms_and_conditions         = None

        self._trade_date       = None
        self._value_date       = None
        self._period_of_notice    = None
        self._interest_rate    = None

        self._currency         = None
        self._interest_amount  = None
        self._balance_amount   = None


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
        self._counterparty_reference       = None
        self._sender_receiver_information  = None

    # ------------------------------------------------------------------------------
    def SetAttributes(self):
        """ Set the attributes from incoming swift message/acm object to MT330"""
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
                self.set_period_of_notice()
                self.set_interest_rate()

                self.set_cur_and_balance_amount()
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
                self.set_counterparty_reference()
                self.set_sender_receiver_information()
                self.ext_ref = self.InternalIdentifier()

            elif self.source == 'ACM':
                self.set_trade_date_from_trade()
                self.set_value_date_from_trade()
                self.set_period_of_notice_from_trade()

                self.set_interest_rate_from_trade()
                self.set_currency_from_trade()
                self.set_balance_amount_from_trade()

                self.set_acquirer_counterparty_from_trade()

                self.set_acquirer_counterparty_receiving_agent_from_trade()
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

    def set_period_of_notice(self):
        try:
            if self.python_object.SequenceB_TransactionDetails.PeriodOfNotice:
                self._period_of_notice = FSwiftMLUtils.swiftmt_to_date(str(self.python_object.SequenceB_TransactionDetails.PeriodOfNotice.value()))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_period_of_notice : %s"%str(e))


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

    def set_interest_amount(self):
        '''
        FORMAT

        Option E    [N]3!a15d    (Sign)(Currency)(Amount)
        '''
        try:
            if self.python_object.SequenceB_TransactionDetails.CurrencyAndInterestAmount:
                curr_interest_amt = str(self.python_object.SequenceB_TransactionDetails.CurrencyAndInterestAmount.value())
                interest_amt_index = re.search('\d', curr_interest_amt).start()

                interest_amt = curr_interest_amt[interest_amt_index:]

                self._interest_amount = FSwiftMLUtils.swiftmt_to_float(interest_amt)

                if interest_amt_index == 4:
                    self._interest_amount *= -1
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_interest_amount : %s"%str(e))


    def set_cur_and_balance_amount(self):
        try:
            if self.python_object.SequenceB_TransactionDetails.CurrencyAndBalance:
                self._currency = str(self.python_object.SequenceB_TransactionDetails.CurrencyAndBalance.value())[0:3]
                self._balance_amount = FSwiftMLUtils.swiftmt_to_float(self.python_object.SequenceB_TransactionDetails.CurrencyAndBalance.value()[3:])
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_cur_and_balance_amount : %s"%str(e))


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

    def set_counterparty_reference(self):
        try:
            if self.python_object.SequenceH_AdditionalInformation and self.python_object.SequenceH_AdditionalInformation.CounterpartysReference:
                self._counterparty_reference = str(self.python_object.SequenceH_AdditionalInformation.CounterpartysReference.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_counterparty_reference : %s"%str(e))

    def set_sender_receiver_information(self):
        try:
            if self.python_object.SequenceH_AdditionalInformation and self.python_object.SequenceH_AdditionalInformation.SenderToReceiverInformation:
                self._sender_receiver_information = str(self.python_object.SequenceH_AdditionalInformation.SenderToReceiverInformation.value())
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_sender_receiver_information : %s"%str(e))

# ------------------------------------------------------------------------------
    # Method to fetch data from the adm

    def set_acquirer_counterparty_from_trade(self): #overridden
        try:
            for flw in self.acm_obj.Trade().MoneyFlows():
                if "Redemption Amount" == flw.Type():
                    self.counterparty = flw.CounterpartyAccount().NetworkAlias().Name() if (flw.CounterpartyAccount() and flw.CounterpartyAccount().NetworkAlias()) else self.acm_obj.Counterparty().Swift()
                    self.acquirer = flw.AcquirerAccount().NetworkAlias().Name() if (flw.AcquirerAccount() and flw.AcquirerAccount().NetworkAlias()) else self.acm_obj.Acquirer().Swift()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_counterparty_from_trade : %s"%str(e))

    def set_curr_amt_from_trade(self):
        try:
            pass
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_curr_amt_from_trade : %s"%str(e))

    def set_value_date_from_trade(self):
        try:
            self._value_date = self.acm_obj.Trade().ValueDay()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_value_date_from_trade : %s"%str(e))

    def set_period_of_notice_from_trade(self):
        try:
            self._period_of_notice = get_period_notice(self.acm_obj)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_period_of_notice_from_trade : %s"%str(e))


    def set_trade_date_from_trade(self):
        try:
            self._trade_date = self.acm_obj.Trade().TradeTime()[:10]
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_trade_date_from_trade : %s"%str(e))

    def set_interest_rate_from_trade(self):
        try:
            self._interest_rate = float(get_interest_rate(self.acm_obj))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_interest_rate_from_trade : %s"%str(e))

    def set_currency_from_trade(self):
        try:
            self._currency = self.acm_obj.Trade().Currency().Name()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_currency_from_trade : %s"%str(e))

    def set_balance_amount_from_trade(self):
        try:
            #import FSwiftMTConfirmation
            #import FSwiftMTLoanDeposit

            #FSwiftMTConfirmation.Init(self.acm_obj)
            #FSwiftMTLoanDeposit.Init(self.acm_obj)
            #import FSwiftMT330
            bal_amt = get_balance_amount(self.acm_obj)
            if bal_amt is not None:
                self._balance_amount = float(bal_amt)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_balance_amount_from_trade : %s"%str(e))



    def set_acquirer_counterparty_receiving_agent_from_trade(self):
        try:
            for flw in self.acm_obj.Trade().MoneyFlows():
                if "Redemption Amount" == flw.Type():
                    self._counterParty_receiving_agent = flw.AcquirerAccount().Bic().Alias() if flw.AcquirerAccount() and flw.AcquirerAccount().Bic() else None
                    self._acquirer_receiving_agent = flw.CounterpartyAccount().Bic().Alias() if flw.CounterpartyAccount() and flw.CounterpartyAccount().Bic() else None
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_counterparty_receiving_agent_from_trade : %s"%str(e))
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

    def FundOrInstructingParty(self):
        return self._fund_or_instructing_party

    def TermsAndConditions(self):
        return self._terms_and_conditions

    def TradeDate(self):
        return self._trade_date

    def ValueDate(self):
        return self._value_date

    def PeriodOfNotice(self):
        return self._period_of_notice

    def InterestRate(self):
        return self._interest_rate

    def Currency(self):
        return self._currency

    def BalanceAmount(self):
        return self._balance_amount

    def InterestAmount(self):
        return self._interest_amount

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

    def CounterpartyReference(self):
        return self._counterparty_reference

    def SenderToReceiverInformation(self):
        return self._sender_receiver_information

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
            'SendersReference': {'THEIRS_SWIFT_TAG' : '20', 'OURS_SWIFT_TAG' : '20', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'RelatedReference': {'THEIRS_SWIFT_TAG' : '21', 'OURS_SWIFT_TAG' : '21', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'TypeOfOperation': {'THEIRS_SWIFT_TAG' : '22A', 'OURS_SWIFT_TAG' : '22A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'ScopeOfOperation': {'THEIRS_SWIFT_TAG' : '94A', 'OURS_SWIFT_TAG' : '94A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'CommonReference': {'THEIRS_SWIFT_TAG' : '22C', 'OURS_SWIFT_TAG' : '22C', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'Acquirer': {'REAL_GETTER' : 'RealAcquirer', 'REAL_SWIFT_TAG' : '82A', 'THEIRS_SWIFT_TAG' : '87A', 'OURS_SWIFT_TAG' : '82A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'Counterparty': {'REAL_GETTER' : 'RealCounterparty', 'REAL_SWIFT_TAG' : '87A', 'THEIRS_SWIFT_TAG' : '82A', 'OURS_SWIFT_TAG' : '87A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'FundOrInstructingParty': {'THEIRS_SWIFT_TAG' : '83A', 'OURS_SWIFT_TAG' : '83A', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'TermsAndConditions': {'THEIRS_SWIFT_TAG' : '77D', 'OURS_SWIFT_TAG' : '77D', 'SEQUENCE': 'General Information', 'COLOR': ''},

            'TradeDate': {'THEIRS_SWIFT_TAG' : '30T', 'OURS_SWIFT_TAG' : '30T', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'ValueDate': {'THEIRS_SWIFT_TAG' : '30V', 'OURS_SWIFT_TAG' : '30V', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'PeriodOfNotice': {'THEIRS_SWIFT_TAG' : '30P', 'OURS_SWIFT_TAG' : '30P', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},
            'InterestRate': {'THEIRS_SWIFT_TAG' : '37G', 'OURS_SWIFT_TAG' : '37G', 'SEQUENCE': 'Transaction Details', 'COLOR': '','FORMAT':'NumDefault'},
            'InterestAmount': {'THEIRS_SWIFT_TAG' : '34E', 'OURS_SWIFT_TAG' : '34E', 'SEQUENCE': 'Transaction Details', 'COLOR': '','FORMAT':'NumDefault'},
            'BalanceAmount': {'THEIRS_SWIFT_TAG' : '32B', 'OURS_SWIFT_TAG' : '32B', 'SEQUENCE': 'Transaction Details', 'COLOR': '','FORMAT':'NumDefault'},
            'Currency': {'THEIRS_SWIFT_TAG' : '32B', 'OURS_SWIFT_TAG' : '32B', 'SEQUENCE': 'Transaction Details', 'COLOR': ''},

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
            'CounterpartyReference': {'THEIRS_SWIFT_TAG' : '26H', 'OURS_SWIFT_TAG' : '26H', 'SEQUENCE': 'Optional Additional Information', 'COLOR': ''},
            'SenderToReceiverInformation': {'THEIRS_SWIFT_TAG' : '72', 'OURS_SWIFT_TAG' : '72', 'SEQUENCE': 'Optional Additional Information', 'COLOR': ''},
            }
        return column_metadata

    @staticmethod
    def GetColumnNamePrefix():
        return 'MT330'

# Helper methods for FMT330Base

def get_period_notice(confirmation):
    assert confirmation.Trade(), "The confirmation has no trade reference"
    assert confirmation.Trade().Instrument(), "The trade referenced by the confirmation has no instrument"
    unit_map = dict(Days=1, Weeks=7, Months=30, Years=365)
    unit = confirmation.Trade().Instrument().NoticePeriodUnit()
    days = confirmation.Trade().Instrument().NoticePeriodCount() * unit_map[unit]
    if days > 999:
        days = 999
    return '%03d' % days

def get_interest_rate(confirmation):
    ''' Mandatory field 37G in seq B '''

    if confirmation.Reset():
        return confirmation.Reset().FixingValue()

    interestRate = ''
    cashFlow = get_cash_flow(confirmation)
    if cashFlow:
        interestRate = cashFlow.FixedRate()
        if not interestRate:
            for aReset in cashFlow.Resets():
                if aReset.FixingValue():
                    interestRate = aReset.FixingValue()
                    break
    return interestRate

def get_cash_flow(confirmation):
    legTocfTypeMappings = { LegType.CALL_FIXED : CashFlowType.CALL_FIXED_RATE,
                    LegType.CALL_FIXED_ADJUSTABLE : CashFlowType.CALL_FIXED_RATE_ADJUSTABLE,
                    LegType.CALL_FLOAT : CashFlowType.CALL_FLOAT_RATE
                     }

    cashflows = {}
    legs = confirmation.Trade().Instrument().Legs()
    for aLeg in legs:
        cfType = legTocfTypeMappings.get(aLeg.LegType(), '')
        if cfType:
            for aCashFlow in aLeg.CashFlows():
                if aCashFlow.CashFlowType() == cfType:
                    cashflows[aCashFlow.StartDate()] = aCashFlow

    cfStartdates = list(cashflows.keys())
    cfStartdates.sort()

    dateToday = acm.Time.DateToday()
    for startDate in cfStartdates:
        endDate = cashflows[startDate].EndDate()
        if startDate <= dateToday <= endDate or startDate > dateToday:
            return cashflows[startDate]

    return ''

def get_balance_amount(confirmation):
    ''' This together with balance_currency forms the mandatory field 32B in seq B '''

    assert confirmation.Trade(), "The confirmation has no trade reference"
    assert confirmation.Trade().Instrument(), "The trade referenced by the confirmation has no instrument"
    legs = confirmation.Trade().Instrument().Legs()
    for aLeg in legs:
        cashFlows = aLeg.CashFlows()
        for aCashFlow in cashFlows:
            if aCashFlow.CashFlowType() == CashFlowType.REDEMPTION_AMOUNT:
                value = get_projected_cash_flow(aCashFlow, confirmation.Trade())
                return apply_currency_precision(aLeg.Currency().Name(), abs(value))
    return ''


def get_projected_cash_flow(cashFlow, trade):
    value = ''
    #calcValue = cashFlow.Calculation().Projected(sharedVariables.get('calcSpace'), trade)
    calc_space = FSwiftMLUtils.get_calculation_space()
    calcValue = cashFlow.Calculation().Projected(calc_space, trade)
    if type(calcValue) == int:
        value = float(calcValue)
    else:
        value = calcValue.Value().Number()
        if acm.Operations.IsValueInfNanOrQNan(value):
            value = 0
    return value

def apply_currency_precision(currency, amount):
    """ Round decimal amount according to the precision for a currency stated in Fparameter: RoundPerCurrency in FSwiftWriterConfig """
    result = FSwiftWriterUtils.apply_rounding(currency, amount)
    return result

def apply_zero_precision(amount):
    ret = 0.0
    absoluteAmount = abs(amount)
    fraction, _ = modf(absoluteAmount)
    if 1.0 - fraction < 1e-6:
        if absoluteAmount - int(absoluteAmount) > 0:
            ret = ceil(absoluteAmount)
        elif absoluteAmount - int(absoluteAmount) < 0:
            ret = floor(absoluteAmount)
    else:
        ret = int(absoluteAmount)

    if amount < 0:
        ret *= -1

    return ret
