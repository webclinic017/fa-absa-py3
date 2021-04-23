"""----------------------------------------------------------------------------
MODULE:
    FMT330OutBase

DESCRIPTION:
    This module provides the base class for the FMT330 outgoing implementation

CLASS:
    FMT330Base

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftMLUtils
import FSwiftWriterMessageHeader
import MT330
import acm
from FExternalObject import FExternalObject
from FLoanDepositOutBase import FLoanDepositOutBase
from FSwiftWriterEngine import validate_with, should_use_operations_xml

from FFXMMConfirmationOutUtils import *
import FSwiftWriterLogger
import FSwiftWriterUtils
import FSwiftOperationsAPI
try:
    #from FConfirmationEnums import ConfirmationType
    ConfirmationType = FSwiftOperationsAPI.GetConfirmationTypeEnum()
    #from FOperationsEnums import LegType
    #from FOperationsEnums import CashFlowType
except:
    pass

notifier = FSwiftWriterLogger.FSwiftWriterLogger('FXMMConfOut', 'FFXMMConfirmationOutNotify_Config')

class FMT330Base(FLoanDepositOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = "MT330"
        self.use_operations_xml = should_use_operations_xml(self.swift_message_type)
        super(FMT330Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)
        self.is_chng_event = None
        self.change_event_dict = {}

        if self.use_operations_xml:
            type_of_operation = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'TYPE_OF_OPERATION'])
        else:
            type_of_operation = str(get_type_of_operation(self.acm_obj))
        if type_of_operation == 'AMND':
            self.is_chng_event, self.change_event_dict = check_for_chng_event_type(self.acm_obj, self.swift_metadata_xml_dom)

    def _message_sequences(self):
        self.swift_obj.SequenceA_GeneralInformation = MT330.MT330_SequenceA_GeneralInformation()
        self.swift_obj.SequenceA_GeneralInformation.swiftTag = "15A"
        self.swift_obj.SequenceA_GeneralInformation.formatTag = "False"

        self.swift_obj.SequenceB_TransactionDetails = MT330.MT330_SequenceB_TransactionDetails()
        self.swift_obj.SequenceB_TransactionDetails.swiftTag = "15B"
        self.swift_obj.SequenceB_TransactionDetails.formatTag = "False"

        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA = MT330.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA()
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.swiftTag = "15C"
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.formatTag = "False"

        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB = MT330.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB()
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.swiftTag = "15D"
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.formatTag = "False"

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT330.MT330_SequenceA_GeneralInformation_20_Type)
    def _validate_senders_reference_20(self, val):
        validate_slash_and_double_slash(val, "Sender's Reference")
        return val

    #setter
    def _set_senders_reference_20(self, val):
        self.swift_obj.SequenceA_GeneralInformation.SendersReference = val
        self.swift_obj.SequenceA_GeneralInformation.SendersReference.swiftTag = "20"

    #getter
    def related_reference_21(self):
        values_dict = {}
        ref_conf = None
        related_reference = None

        if self.use_operations_xml:
            type_of_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'TYPE_EVENT'])
            type_of_operation = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'TYPE_OF_OPERATION'])
        else:
            type_of_event = get_event_type_MT330(self.acm_obj)
            type_of_operation = str(get_type_of_operation(self.acm_obj))


        if type_of_operation in ['AMND', 'CANC']:

            if self.use_operations_xml:
                related_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'YOUR_REFERENCE'],
                                                                                 ignore_absense=True)
                conf_id = related_reference.strip("FAC-")
            else:
                conf_id = get_related_confirmation(self.acm_obj).Oid()
                related_reference = get_confirmation_reference_prefix() + '-' + str(conf_id)

            if related_reference:
                ref_conf = acm.FConfirmation[str(conf_id)]
            else:
                #Getting related reference on our own as OperationsAPI does not provide related reference in case of AMND/CANC
                if self.use_operations_xml:
                    senders_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                     ['CONFIRMATION', 'SEQNBR'])
                else:
                    senders_reference = self.acm_obj.Oid()

                confirmation = acm.FConfirmation[str(senders_reference)]
                ref_conf = None
                if FSwiftMLUtils.get_acm_version() >= 2016.4:
                    try:
                        #from FConfirmationEnums import ConfirmationType
                        if confirmation.Type() in (ConfirmationType.AMENDMENT, ConfirmationType.CANCELLATION):
                            ref_conf = confirmation.ConfirmationReference()
                    except Exception as e:
                        pass
                else:
                    if confirmation.Type() in ("Amendment", "Cancellation"):
                        ref_conf = confirmation.ConfirmationReference()
                related_reference = get_confirmation_reference_prefix() + "-" + str(ref_conf.Oid())
        if related_reference and ref_conf:
            values_dict['related_reference'] = related_reference
            values_dict['ref_conf'] = ref_conf
        return values_dict

    #formatter
    def _format_related_reference_21(self, val):
        related_reference = val.get('related_reference')
        ref_conf = val.get('ref_conf')
        ref_conf, related_reference = check_for_valid_related_reference(ref_conf, related_reference)
        version_number_of_related_reference = get_version_for_sent_message_on(ref_conf, 'MT330')
        val = str(related_reference) + "-" + str(version_number_of_related_reference)
        return val

    #validator
    @validate_with(MT330.MT330_SequenceA_GeneralInformation_21_Type, is_mandatory = True)
    def _validate_related_reference_21(self, val):
        validate_slash_and_double_slash(val, "Related Reference")
        return val

    def _check_condition_set_related_reference_21(self):
        if self.use_operations_xml:
            type_of_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'TYPE_EVENT'])
            type_of_operation = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'TYPE_OF_OPERATION'])
        else:
            type_of_event = get_event_type_MT330(self.acm_obj)
            type_of_operation = str(get_type_of_operation(self.acm_obj))

        if type_of_event == 'CONF':
            if type_of_operation in ['AMND', 'CANC']:
                return True
        else:
            return True
        return False

    #setter
    def _set_related_reference_21(self, val):
        self.swift_obj.SequenceA_GeneralInformation.RelatedReference = val
        self.swift_obj.SequenceA_GeneralInformation.RelatedReference.swiftTag = "21"

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    def _format_type_of_operation_22A(self, val):
        if val:
            if self.is_chng_event:
                val = "NEWT"
                if self.change_event_dict['is_change_event_amnd']:
                    val = "AMND"
            return val

    #validator
    @validate_with(MT330.MT330_SequenceA_GeneralInformation_22A_Type)
    def _validate_type_of_operation_22A(self, val):
        return val

    #setter
    def _set_type_of_operation_22A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.TypeOfOperation = val
        self.swift_obj.SequenceA_GeneralInformation.TypeOfOperation.swiftTag = "22A"

    #getter
    def type_of_event_22B(self):
        if self.use_operations_xml:
            type_of_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TYPE_EVENT'])
        else:
            type_of_event = get_event_type_MT330(self.acm_obj)
        return type_of_event

    #formatter
    def _format_type_of_event_22B(self, val):
        if val:
            if self.is_chng_event:
                val = 'CHNG'
            return val

    #validator
    @validate_with(MT330.MT330_SequenceA_GeneralInformation_22B_Type)
    def _validate_type_of_event_22B(self, val):
        return val

    #setter
    def _set_type_of_event_22B(self, val):
        self.swift_obj.SequenceA_GeneralInformation.TypeOfEvent = val
        self.swift_obj.SequenceA_GeneralInformation.TypeOfEvent.swiftTag = "22B"

    #getter
    def common_reference_22C(self):
        values_dict = {}
        if self.use_operations_xml:
            senders_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SENDER_BIC'])
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'RECEIVER_BIC'])
            interest_rate = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'INTEREST_RATE'])
        else:
            senders_bic = get_senders_bic(self.acm_obj)
            receivers_bic = get_receivers_bic(self.acm_obj)
            interest_rate = get_interest_rate_MT330(self.acm_obj)

        values_dict['senders_bic'] = senders_bic
        values_dict['receivers_bic'] = receivers_bic
        values_dict['interest_rate'] = interest_rate

        return values_dict

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT330.MT330_SequenceA_GeneralInformation_22C_Type)
    def _validate_common_reference_22C(self, val):
        return val

    #setter
    def _set_common_reference_22C(self, val):
        self.swift_obj.SequenceA_GeneralInformation.CommonReference = val
        self.swift_obj.SequenceA_GeneralInformation.CommonReference.swiftTag = "22C"


    # option getter
    def get_partyA_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    #setter
    def _set_OPTION_party_A(self):
        if self.use_operations_xml:
            party_A_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'PARTY_A_OPTION'])
        else:
            party_A_option = self.get_partyA_option()

        if party_A_option == 'A':
            return 'partyA_82A'
        elif party_A_option == "D":
            return 'partyA_82D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." %
                          (self.swift_message_type, str(party_A_option), 'PartyA_82a'))
            return 'partyA_82A'

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT330.MT330_SequenceA_GeneralInformation_82A_Type)
    def _validate_partyA_82A(self, val):
        return val

    #setter
    def _setpartyA_82A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.PartyA_A = val
        self.swift_obj.SequenceA_GeneralInformation.PartyA_A.swiftTag = '82A'

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT330.MT330_SequenceA_GeneralInformation_82D_Type)
    def _validate_partyA_82D(self, val):
        return val

    #setter
    def _setpartyA_82D(self, val):
       self.swift_obj.SequenceA_GeneralInformation.PartyA_D = val
       self.swift_obj.SequenceA_GeneralInformation.PartyA_D.swiftTag = '82D'


    # option getter
    def get_partyB_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    #setter
    def _set_OPTION_party_B(self):
        if self.use_operations_xml:
            party_B_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'PARTY_B_OPTION'])
        else:
            party_B_option = self.get_partyB_option()

        if party_B_option == 'A':
            return 'partyB_87A'
        elif party_B_option == "D":
            return 'partyB_87D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." %
                          (self.swift_message_type, str(party_B_option), 'PartyA_82a'))
            return 'partyB_87A'

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase


    #validator
    @validate_with(MT330.MT330_SequenceA_GeneralInformation_87A_Type)
    def _validate_partyB_87A(self, val):
        return val

    #setter
    def _setpartyB_87A(self, val):
        self.swift_obj.SequenceA_GeneralInformation.PartyB_A = val
        self.swift_obj.SequenceA_GeneralInformation.PartyB_A.swiftTag = '87A'

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT330.MT330_SequenceA_GeneralInformation_87D_Type)
    def _validate_partyB_87D(self, val):
        return val

    #setter
    def _setpartyB_87D(self, val):
        self.swift_obj.SequenceA_GeneralInformation.PartyB_D = val
        self.swift_obj.SequenceA_GeneralInformation.PartyB_D.swiftTag = '87D'

    #getter
    def terms_and_condition_77D(self):
        if self.use_operations_xml:
            terms_and_conditions = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                            ['SWIFT', 'TERMS_CONDITIONS'],
                                                                            ignore_absense=True)
        else:
            terms_and_conditions = get_terms_and_conditions(self.acm_obj, self.swift_message_type)

        return terms_and_conditions

    #formatter
    def _format_terms_and_condition_77D(self, val):
        character_limit = 35
        lines = FSwiftWriterUtils.split_text_on_character_limit(val, character_limit)
        n = 6
        val = FSwiftWriterUtils.allocate_space_for_n_lines(n, lines)
        return val


    #validator
    @validate_with(MT330.MT330_SequenceA_GeneralInformation_77D_Type)
    def _validate_terms_and_condition_77D(self, val):
        return val

    #setter
    def _set_terms_and_condition_77D(self, val):
        self.swift_obj.SequenceA_GeneralInformation.TermsAndConditions = val
        self.swift_obj.SequenceA_GeneralInformation.TermsAndConditions.swiftTag = "77D"

    #getter
    def party_A_role_17R(self):
        if self.use_operations_xml:
            party_As_role = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'PARTY_A_ROLE'])
        else:
            party_As_role = get_party_A_role_MT330(self.acm_obj)

        return party_As_role

    #formatter
    def _format_party_A_role_17R(self, val):
        return val

    #validator
    @validate_with(MT330.MT330_SequenceB_TransactionDetails_17R_Type)
    def _validate_party_A_role_17R(self, val):
        return val

    #setter
    def _set_party_A_role_17R(self, val):
        self.swift_obj.SequenceB_TransactionDetails.PartyAsRole = val
        self.swift_obj.SequenceB_TransactionDetails.PartyAsRole.swiftTag = '17R'

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT330.MT330_SequenceB_TransactionDetails_30T_Type)
    def _validate_trade_date_30T(self, val):
        return val

    #setter
    def _set_trade_date_30T(self, val):
        self.swift_obj.SequenceB_TransactionDetails.TradeDate = val
        self.swift_obj.SequenceB_TransactionDetails.TradeDate.swiftTag = '30T'

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT330.MT330_SequenceB_TransactionDetails_30V_Type)
    def _validate_value_date_30V(self, val):
        return val

    #setter
    def _set_value_date_30V(self, val):
        self.swift_obj.SequenceB_TransactionDetails.ValueDate = val
        self.swift_obj.SequenceB_TransactionDetails.ValueDate.swiftTag = '30V'

    #getter
    def period_of_notice_38A(self):
        if self.use_operations_xml:
            period_of_notice = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                        ['SWIFT', 'PERIOD_NOTICE'])
        else:
            period_of_notice = get_period_notice(self.acm_obj)

        return period_of_notice

    #formatter
    def _format_period_of_notice_38A(self, val):
        return val

    #validator
    @validate_with( MT330.MT330_SequenceB_TransactionDetails_38A_Type)
    def _validate_period_of_notice_38A(self, val):
        return val

    #setter
    def _set_period_of_notice_38A(self, val):
        self.swift_obj.SequenceB_TransactionDetails.PeriodOfNotice = val
        self.swift_obj.SequenceB_TransactionDetails.PeriodOfNotice.swiftTag = '38A'

    #getter
    def currency_and_balance_32B(self):
        values_dict = {}
        if self.use_operations_xml:
            balance_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                        ['SWIFT', 'BALANCE_CURRENCY'], ignore_absense=True)
            balance_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'BALANCE_AMOUNT'], ignore_absense=True)
        else:
            balance_currency = str(get_balance_currency(self.acm_obj))
            balance_amount = str(get_balance_amount(self.acm_obj))

        values_dict['balance_amount'] = balance_amount
        values_dict['balance_currency'] = balance_currency
        return values_dict

    #formatter
    def _format_currency_and_balance_32B(self, val):
        balance_amount = val.get('balance_amount')
        balance_currency = val.get('balance_currency')
        if balance_currency and balance_amount:
            balance_amount = apply_currency_precision(balance_currency, float(balance_amount))
            val = str(balance_currency) + str(FSwiftMLUtils.float_to_swiftmt(balance_amount))
            return val

    #validator
    @validate_with(MT330.MT330_SequenceB_TransactionDetails_32B_Type, is_mandatory = True)
    def _validate_currency_and_balance_32B(self, val):
        curr_balance = get_amount_from_currency_amount(val)
        validateAmount(curr_balance.replace('.', ','), 15, "Currency And Balance")
        return val

    def _check_condition_set_currency_and_balance_32B(self):
        if self.use_operations_xml:
            type_of_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TYPE_EVENT'])
        else:
            type_of_event = get_event_type_MT330(self.acm_obj)

        return type_of_event in ['CHNG', 'CINT', 'CONF']

    #setter
    def _set_currency_and_balance_32B(self, val):
        self.swift_obj.SequenceB_TransactionDetails.CurrencyAndBalance = val
        self.swift_obj.SequenceB_TransactionDetails.CurrencyAndBalance.swiftTag = '32B'

    #getter
    def principle_amount_to_settle_32H(self):
        amount = 0
        return amount

    #formatter
    def _format_principle_amount_to_settle_32H(self, val):
        amount = 0
        if self.is_chng_event:
            last_amount= self.change_event_dict['last_amount'][3:].replace(',', '.')
            amount = float(last_amount) - float(get_total_fixed_amount_from_cashflow(self.acm_obj))
            if amount < 0:
                amount = 0
            curr = self.acm_obj.Trade().Currency().Name()
            sett_amount = apply_currency_precision(curr, float(amount))
            val = curr + FSwiftMLUtils.float_to_swiftmt(sett_amount)
        return str(val)

    #validator
    @validate_with(MT330.MT330_SequenceB_TransactionDetails_32H_Type, is_mandatory = True)
    def _validate_principle_amount_to_settle_32H(self, val):
        return val

    def _check_condition_set_principle_amount_to_settle_32H(self):
        if self.use_operations_xml:
            type_of_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TYPE_EVENT'])
        else:
            type_of_event = get_event_type_MT330(self.acm_obj)
            if self.is_chng_event:
                type_of_event = 'CHNG'

        return type_of_event in ['CHNG', 'CINT', 'SETT']

    #setter
    def _set_principle_amount_to_settle_32H(self, val):
        self.swift_obj.SequenceB_TransactionDetails.PrincipalAmountToBeSettled = val
        self.swift_obj.SequenceB_TransactionDetails.PrincipalAmountToBeSettled.swiftTag = "32H"

    #getter
    def interest_rate_37G(self):
        if self.use_operations_xml:
            interest_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                       ['SWIFT', 'INTEREST_RATE'])
        else:
            interest_amount = get_interest_rate_MT330(self.acm_obj)
        return interest_amount

    #formatter
    def _format_interest_rate_37G(self, val):
        if val:
            val = FSwiftWriterUtils.represent_negative_amount(val)
            return str(val)

    #validator
    @validate_with(MT330.MT330_SequenceB_TransactionDetails_37G_Type)
    def _validate_interest_rate_37G(self, val):
        interest_rate = val
        validateAmount(interest_rate.replace('N', ''), 12, "Interest Rate")
        return val

    #setter
    def _set_interest_rate_37G(self, val):
        self.swift_obj.SequenceB_TransactionDetails.InterestRate = val
        self.swift_obj.SequenceB_TransactionDetails.InterestRate.swiftTag = '37G'

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT330.MT330_SequenceB_TransactionDetails_14D_Type)
    def _validate_day_count_fraction_14D(self, val):
        return val

    #setter
    def _set_day_count_fraction_14D(self, val):
        self.swift_obj.SequenceB_TransactionDetails.DayCountFraction = val
        self.swift_obj.SequenceB_TransactionDetails.DayCountFraction.swiftTag = '14D'

    # option getter
    def get_receiving_agent_PartyA_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    #setter
    def _set_OPTION_receiving_agent_PartyA(self):
        if self.use_operations_xml:
            buy_receiving_agent_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SIA_PARTY_A_RECEIVING_AGENT_OPTION'])
        else:
            option = self.get_receiving_agent_PartyA_option()
            buy_receiving_agent_option = get_SIA_party_receiving_agent_option('A', self.acm_obj, self.swift_message_type, option)

        if buy_receiving_agent_option == "A":
            return 'receiving_agent_PartyA_57A'
        elif buy_receiving_agent_option == "D":
            return 'receiving_agent_PartyA_57D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." %
                          (self.swift_message_type, str(buy_receiving_agent_option), 'Receiving_agent_PartyA_57a'))
            return 'receiving_agent_PartyA_57A'

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase


    #validator
    @validate_with(MT330.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type)
    def _validate_receiving_agent_PartyA_57A(self, val):
        return val

    #setter
    def _setreceiving_agent_PartyA_57A(self, val):
       self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_A = val
       self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_A.swiftTag = "57A"

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase


    #validator
    @validate_with(MT330.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type)
    def _validate_receiving_agent_PartyA_57D(self, val):
        return val

    #setter
    def _setreceiving_agent_PartyA_57D(self, val):
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_D = val
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_D.swiftTag = "57D"

    # option getter

    def get_receiving_agent_PartyB_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    #setter
    def _set_OPTION_receiving_agent_PartyB(self):
        if self.use_operations_xml:
            buy_receiving_agent_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SIA_PARTY_B_RECEIVING_AGENT_OPTION'])
        else:
            option = self.get_receiving_agent_PartyB_option()
            buy_receiving_agent_option = get_SIA_party_receiving_agent_option('B', self.acm_obj, self.swift_message_type, option)

        if buy_receiving_agent_option == "A":
            return 'receiving_agent_PartyB_57A'
        elif buy_receiving_agent_option == "D":
            return 'receiving_agent_PartyB_57D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(buy_receiving_agent_option), 'Receiving_agent_PartyB_57a'))
            return 'receiving_agent_PartyB_57A'

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase


    #validator
    @validate_with(MT330.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type)
    def _validate_receiving_agent_PartyB_57A(self, val):
        return val

    #setter
    def _setreceiving_agent_PartyB_57A(self, val):
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_A = val
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_A.swiftTag = "57A"

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase


    #validator
    @validate_with(MT330.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type)
    def _validate_receiving_agent_PartyB_57D(self, val):
        return val

    #setter
    def _setreceiving_agent_PartyB_57D(self, val):
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_D = val
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_D.swiftTag = "57D"

    '''
    # ToDo analyze fields and map their corresponding value for without using operations xml
    #setter
    def _set_OPTION_beneficiary_institution_PartyA(self):
        if self.use_operations_xml:
            sell_beneficiary_institution_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SIA_PARTY_A_BEN_INSTI_OPTION'], ignore_absense=True)

        if sell_beneficiary_institution_option == "A":
            return 'beneficiary_institution_PartyA_58A'
        elif sell_beneficiary_institution_option == "D":
            return 'beneficiary_institution_PartyA_58D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                    self.swift_message_type, str(sell_beneficiary_institution_option), 'beneficiary_institution_PartyA_58a'))
            return 'beneficiary_institution_PartyA_58A'

    #getter
    def beneficiary_institution_PartyA_58A(self):
        values_dict = {}
        account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SIA_PARTY_A_BEN_INSTI_ACCOUNT'],
                                                           ignore_absense=True)
        bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                       ['SWIFT', 'SIA_PARTY_A_BEN_INSTI_BIC'],
                                                       ignore_absense=True)
        values_dict['account'] = account
        values_dict['bic'] = bic
        return values_dict

    #formatter
    def _format_beneficiary_institution_PartyA_58A(self, val):
        account = val.get('account')
        bic = val.get('bic')
        if bic:
            field_value = str(bic)
            if account:
                field_value = "/" + str(account) + "\n" + str(field_value)
            return field_value


    #validator
    @validate_with(MT330.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type)
    def _validate_beneficiary_institution_PartyA_58A(self, val):
        return val

    #setter
    def _setbeneficiary_institution_PartyA_58A(self, val):
       self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.BeneficiaryInstitution_A = val
       self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.BeneficiaryInstitution_A.swiftTag = "58A"

    #getter
    def beneficiary_institution_PartyA_58D(self):
        values_dict = {}
        account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SIA_PARTY_A_BEN_INSTI_ACCOUNT'],
                                                           ignore_absense=True)
        name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SIA_PARTY_A_BEN_INSTI_NAME'],
                                                           ignore_absense=True)
        address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SIA_PARTY_A_BEN_INSTI_ADDRESS'],
                                                           ignore_absense=True)
        values_dict['account'] = account
        values_dict['name'] = name
        values_dict['address'] = address
        return values_dict

    #formatter
    def _format_beneficiary_institution_PartyA_58D(self, val):
        account = val.get('account')
        name = val.get('name')
        address = val.get('address')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                field_value = "/" + str(account) + "\n" + str(val)
            return field_value


    #validator
    @validate_with(MT330.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type)
    def _validate_beneficiary_institution_PartyA_58D(self, val):
        return val

    #setter
    def _setbeneficiary_institution_PartyA_58D(self, val):
       self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.BeneficiaryInstitution_D = val
       self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.BeneficiaryInstitution_D.swiftTag = "58D"

    #setter
    def _set_OPTION_beneficiary_institution_PartyB(self):
        sell_beneficiary_institution_option = FSwiftWriterUtils.get_value_from_xml_tag(
            self.swift_metadata_xml_dom, ['SWIFT', 'SIA_PARTY_B_BEN_INSTI_OPTION'], ignore_absense=True)
        if sell_beneficiary_institution_option == "A":
            return 'beneficiary_institution_PartyB_58A'
        elif sell_beneficiary_institution_option == "D":
            return 'beneficiary_institution_PartyB_58D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                    self.swift_message_type, str(sell_beneficiary_institution_option), 'beneficiary_institution_PartyB_58a'))
            return 'beneficiary_institution_PartyB_58A'


    #getter
    def beneficiary_institution_PartyB_58A(self):
        values_dict = {}
        account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SIA_PARTY_B_BEN_INSTI_ACCOUNT'],
                                                           ignore_absense=True)
        bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                       ['SWIFT', 'SIA_PARTY_B_BEN_INSTI_BIC'],
                                                       ignore_absense=True)
        values_dict['account'] = account
        values_dict['bic'] = bic
        return values_dict

    #formatter
    def _format_beneficiary_institution_PartyB_58A(self, val):
        account = val.get('account')
        bic = val.get('bic')
        if bic:
            field_value = str(bic)
            if account:
                field_value = "/" + str(account) + "\n" + str(field_value)
            return field_value


    #validator
    @validate_with(MT330.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type)
    def _validate_beneficiary_institution_PartyB_58A(self, val):
        return val

    #setter
    def _setbeneficiary_institution_PartyB_58A(self, val):
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.BeneficiaryInstitution_A = val
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.BeneficiaryInstitution_A.swiftTag = "58A"

    #getter
    def beneficiary_institution_PartyB_58D(self):
        values_dict = {}
        account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SIA_PARTY_B_BEN_INSTI_ACCOUNT'],
                                                           ignore_absense=True)
        name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SIA_PARTY_B_BEN_INSTI_NAME'],
                                                           ignore_absense=True)
        address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                        ['SWIFT', 'SIA_PARTY_B_BEN_INSTI_ADDRESS'],
                                                        ignore_absense=True)
        values_dict['account'] = account
        values_dict['name'] = name
        values_dict['address'] = address
        return values_dict

    #formatter
    def _format_beneficiary_institution_PartyB_58D(self, val):
        account = val.get('account')
        name = val.get('name')
        address = val.get('address')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                field_value = "/" + str(account) + "\n" + str(val)
            return field_value


    #validator
    @validate_with(MT330.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type)
    def _validate_beneficiary_institution_PartyB_58D(self, val):
        return val

    #setter
    def _setbeneficiary_institution_PartyB_58D(self, val):
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.BeneficiaryInstitution_D = val
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.BeneficiaryInstitution_D.swiftTag = "58D" '''


class FMT330OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_typ = '330'
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT' + self.mt_typ)
        super(FMT330OutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

    def message_type(self):
        return self.mt_typ

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
        terminal_address = self.logical_terminal_address(senders_bic, 'A')
        return terminal_address

    def receiver_logical_terminal_address(self):
        '''LT code is hardcoded as X for sender'''
        terminal_address = ''
        receivers_bic = ''
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'RECEIVER_BIC'])
        else:
            receivers_bic = get_receivers_bic(self.acm_obj)

        terminal_address = self.logical_terminal_address(receivers_bic, 'X')
        return terminal_address

    def logical_terminal_address(self, bic_code, lt_code):
        terminal_address = ''
        branch_code = 'XXX'
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
        return 'I'

    def message_user_reference(self):
        '''MUR is sent in the format FAC-SEQNBR of confirmation-VersionID'''
        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['CONFIRMATION', 'SEQNBR'])
        else:
            seqnbr = self.acm_obj.Oid()
        return "{108:%s-%s-%s}" % (get_confirmation_reference_prefix(), seqnbr, get_message_version_number(self.acm_obj))


class FMT330OutBaseNetworkRules(object):
    ''' '''

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.acm_obj = acm_obj


        '''
            Mandatory fields used across rules
        '''
        self._22B_Value = self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value()
        self._22A_Value = self.swift_message_obj.SequenceA_GeneralInformation.TypeOfOperation.value()
        self._17R_Value = self.swift_message_obj.SequenceB_TransactionDetails.PartyAsRole.value()

    def network_rule_C1(self):
        '''
            In sequence A, the presence of field 21 depends on the value of fields 22B and 22A as follows (Error code(s): D70):

            +-------------------------------------------------------------------------------------------------------------------------------+
            |      Sequence A             |            Sequence A                                    |          Sequence A                  |
            |      if field 22B is ...    |            and field 22A is ...                          |          then field 21 is ...        |
            |-------------------------------------------------------------------------------------------------------------------------------|
            |        CONF                 |           NEWT                                           |        Optional                      |
            |        CONF                 |           Not equal to NEWT                              |        Mandatory                     |
            |        Not equal to CONF    |           Any value                                      |        Mandatory                     |
            +-------------------------------------------------------------------------------------------------------------------------------+

        '''

        _21A_isMandatory = True

        if self._22B_Value == 'CONF':
            _21A_isMandatory = (self._22A_Value != 'NEWT')

        if _21A_isMandatory and self.swift_message_obj.SequenceA_GeneralInformation.RelatedReference is None:
            return 'Field 21 in Sequence A is mandatory if field 22B in Sequence A is equal to CONF and 22A in Sequence A is not equal to NEWT'

        return ''

    def network_rule_C3(self):
        '''
            In sequence B, the presence of fields 32B, 32H and 30X depends on the value of field 22B in sequence A as follows (Error code(s): D56):

            +------------------------------------------------------------------------------------------------------------------------------+
            |      Sequence A             | Sequence B             |          Sequence B                 |    Sequence B                   |
            |      if field 22B is ...    | then field 32B is ...  |         and field 32H is ...        |    and field 30X is ...         |
            |------------------------------------------------------------------------------------------------------------------------------|
            |        CHNG                 | Mandatory              |        Mandatory                    |    Optional                     |
            |        CINT                 | Mandatory              |        Mandatory                    |    Optional                     |
            |        CONF                 | Mandatory              |        Not allowed                  |    Not allowed                  |
            |        SETT                 | Not allowed            |        Mandatory                    |    Mandatory                    |
            +------------------------------------------------------------------------------------------------------------------------------+

        '''
        _32H_Value = None
        _30X_Value = None
        _32B_Value = None

        if self.swift_message_obj.SequenceB_TransactionDetails.CurrencyAndBalance:
            _32B_Value = self.swift_message_obj.SequenceB_TransactionDetails.CurrencyAndBalance.value()

        if self.swift_message_obj.SequenceB_TransactionDetails.PrincipalAmountToBeSettled:
            _32H_Value = self.swift_message_obj.SequenceB_TransactionDetails.PrincipalAmountToBeSettled.value()

        if self.swift_message_obj.SequenceB_TransactionDetails.InterestDueDate:
            _30X_Value = self.swift_message_obj.SequenceB_TransactionDetails.InterestDueDate.value()

        if 'CHNG' == self._22B_Value or 'CINT' == self._22B_Value:
            if not (_32B_Value and _32H_Value):
                return 'Field 32B and 32H in Sequence B are if field 22B in Sequence A is equal to CHNG or CINT'
        elif 'CONF' == self._22B_Value:
            if not (_32B_Value and (_32H_Value is None) and (_30X_Value is None)):
                return 'Field 32B is mandatory and 32H and 30X are not allowed in Sequence B if field 22B in Sequence A is equal to CONF'
        elif 'SETT' == self._22B_Value:
            if not ((_32B_Value is None) and _32H_Value and _30X_Value):
                return 'Field 30X and 32H are mandatory and 32B is not allowed in Sequence B if field 22B in Sequence A is equal to SETT'

        return ''

    def network_rule_C4(self):
        '''
            In sequence B, the values allowed for subfield 3 of field 32H depend on the values of field 22B in sequence A and field 17R in sequence B as follows (Error code(s): D57):

            +-------------------------------------------------------------------------------------------------------------------------------+
            |      Sequence A             |            Sequence B                    |          Sequence B                                  |
            |      if field 22B is ...    |            and field 17R is ...          |          then subfield 3 of field 32H must be ...    |
            |-------------------------------------------------------------------------------------------------------------------------------|
            |        SETT                 |           L                              |        Negative or zero                              |
            |        SETT                 |           B                              |        Positive or zero                              |
            |        Not equal to SETT    |           Not applicable                 |        Not applicable                                |
            +-------------------------------------------------------------------------------------------------------------------------------+

            The presence of the letter N (sign) in subfield 1 of field 32H specifies a negative amount.

            The absence of the letter N (sign) in subfield 1 of field 32H specifies a positive amount.

            If the value in subfield 3 of field 32H is zero, then the letter N (sign) in subfield 1 of field 32H is not allowed (Error code(s): T14).

        '''

        _32H_Amount = None

        if 'SETT' == self._22B_Value:
            if self.swift_message_obj.SequenceB_TransactionDetails.PrincipalAmountToBeSettled:
                _32H_Value = self.swift_message_obj.SequenceB_TransactionDetails.PrincipalAmountToBeSettled.value()
                if _32H_Value[0] == 'N':
                    _32H_Amount = 'NEGATIVE'
                    if float(_32H_Value[3:]) == 0.0:
                        _32H_Amount = 'NOT ALLOWED'
                else:
                    _32H_Amount = 'POSITIVE'
                    if float(_32H_Value[3:]) == 0.0:
                        _32H_Amount = 'ZERO'

        if 'SETT' == self._22B_Value:
            if self._17R_Value in ['L']:
                if _32H_Amount not in ['ZERO', 'NEGATIVE']:
                    return 'Field 32H in Sequence B must contain negative or zero amount if field 22B in Sequence A is equal SETT and field 17R is equal to L'
            elif self._17R_Value in ['B']:
                if _32H_Amount not in ['ZERO', 'POSITIVE']:
                    return 'Field 32H in Sequence B must contain positive or zero amount if field 22B in Sequence A is equal SETT and field 17R is equal to L'
        else:
            pass
            # What is Not Applicable

        return ''

    def network_rule_C5(self):
        '''
            In sequence B, if field 30X is present, then field 34E is mandatory, otherwise field 34E is not allowed (Error code(s): D85):

            +------------------------------------------------------------------------+
            |      Sequence B             |            Sequence B                    |
            |      if field 30X is ...    |            then field 34E is ...         |
            |------------------------------------------------------------------------|
            |        Present              |           Mandatory                      |
            |        Not present          |           Not allowed                    |
            +------------------------------------------------------------------------+
        '''
        _34E_Value = None

        if self.swift_message_obj.SequenceB_TransactionDetails.CurrencyAndInterestAmount:
            _34E_Value = self.swift_message_obj.SequenceB_TransactionDetails.CurrencyAndInterestAmount.value()

        if (self.swift_message_obj.SequenceB_TransactionDetails.InterestDueDate and _34E_Value is None) or (
                self.swift_message_obj.SequenceB_TransactionDetails.InterestDueDate is None and _34E_Value is not None):
            return 'In sequence B, if field 30X is present, then field 34E is mandatory, otherwise field 34E is not allowed'

        return ''

    def network_rule_C6(self):
        '''
            In sequence A, if field 22B contains SETT, then field 30F in sequence B is not allowed, otherwise field 30F is optional (Error code(s): D69).:

            +------------------------------------------------------------------------+
            |      Sequence A             |            Sequence B                    |
            |      if field 22B is ...    |            then field 30F is ...         |
            |------------------------------------------------------------------------|
            |        SETT                 |           Not allowed                    |
            |        Not equal to SETT    |           Optional                       |
            +------------------------------------------------------------------------+
        '''
        if 'SETT' == self._22B_Value and self.swift_message_obj.SequenceB_TransactionDetails.LastDayOfTheNextInterestPeriod is not None:
            return 'In sequence A, if field 22B contains SETT, then field 30F in sequence B is not allowed, otherwise field 30F is optional'

        return ''

    def network_rule_C7(self):
        '''
            In sequence B, if field 30F is present, then field 38J is mandatory, otherwise field 38J is not allowed (Error code(s): D60).

            +------------------------------------------------------------------------+
            |      Sequence B             |            Sequence B                    |
            |      if field 30F is ...    |            then field 38J is ...         |
            |------------------------------------------------------------------------|
            |      Present                |           Mandatory                      |
            |      Not present            |           Not allowed                    |
            +------------------------------------------------------------------------+
        '''
        _30F_Value = None
        if self.swift_message_obj.SequenceB_TransactionDetails.LastDayOfTheNextInterestPeriod:
            _30F_Value = self.swift_message_obj.SequenceB_TransactionDetails.LastDayOfTheNextInterestPeriod.value()

        if (_30F_Value is not None and self.swift_message_obj.SequenceB_TransactionDetails.NumberOfDays is None) or (
                _30F_Value is None and self.swift_message_obj.SequenceB_TransactionDetails.NumberOfDays is not None):
            return 'In sequence B, if field 30F is present, then field 38J is mandatory, otherwise field 38J is not allowed.'

        return ''

    def check_rule_C8(self, seqObj):
        if seqObj is not None:
            if (seqObj.Intermediary_A is None and seqObj.Intermediary2_A is not None):
                return False

            if (seqObj.Intermediary_D is None and seqObj.Intermediary2_D is not None):
                return False

            if (seqObj.Intermediary_J is None and seqObj.Intermediary2_J is not None):
                return False

        return True

    def network_rule_C8(self):
        '''
            In sequences C, D, E (if present) and F (if present), if field 56a is not present, then field 86a in the same sequence C, D, E or F is not allowed, otherwise field 86a is optional (Error code(s): E35).

            +------------------------------------------------------------------------+
            |      Sequence C             |            Sequence C                    |
            |      if field 56a is ...    |            then field 86a is             |
            |------------------------------------------------------------------------|
            |      Not present            |           Not allowed                    |
            |      Present                |           Optional                       |
            +------------------------------------------------------------------------+

            +------------------------------------------------------------------------+
            |      Sequence D             |            Sequence D                    |
            |      if field 56a is ...    |            then field 86a is             |
            |------------------------------------------------------------------------|
            |      Not present            |           Not allowed                    |
            |      Present                |           Optional                       |
            +------------------------------------------------------------------------+

            +------------------------------------------------------------------------+
            |      Sequence E             |            Sequence E                    |
            |      if field 56a is ...    |            then field 86a is             |
            |------------------------------------------------------------------------|
            |      Not present            |           Not allowed                    |
            |      Present                |           Optional                       |
            +------------------------------------------------------------------------+

            +------------------------------------------------------------------------+
            |      Sequence F             |            Sequence F                    |
            |      if field 56a is ...    |            then field 86a is             |
            |------------------------------------------------------------------------|
            |      Not present            |           Not allowed                    |
            |      Present                |           Optional                       |
            +------------------------------------------------------------------------+
        '''

        errorCode = 'In sequences C, D, E (if present) and F (if present), if field 56a is not present, then field 86a in the same sequence C, D, E or F is not allowed, otherwise field 86a is optional'
        if not self.check_rule_C8(self.swift_message_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA):
            return errorCode

        if not self.check_rule_C8(self.swift_message_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB):
            return errorCode

        if not self.check_rule_C8(self.swift_message_obj.SequenceE_SettlementInstructionsforInterestsPayablebyPartyA):
            return errorCode

        if not self.check_rule_C8(self.swift_message_obj.SequenceF_SettlementInstructionsforInterestsPayablebyPartyB):
            return errorCode

        return ''

    def network_rule_C9(self):
        '''The currency code in the amount fields must be the same for all occurrences of these fields in the entire message, except for fields 33B and 33E in sequence G (Error code(s): C02).'''
        _34E_Value = None
        _32H_Value = None
        _32B_Value = None
        currSet = set()

        if self.swift_message_obj.SequenceB_TransactionDetails.CurrencyAndInterestAmount:
            _34E_Value = get_currency_from_currency_amount(
                self.swift_message_obj.SequenceB_TransactionDetails.CurrencyAndInterestAmount.value())
            if _34E_Value is not None:
                currSet.add(_34E_Value)

        if self.swift_message_obj.SequenceB_TransactionDetails.PrincipalAmountToBeSettled:
            _32H_Value = get_currency_from_currency_amount(
                self.swift_message_obj.SequenceB_TransactionDetails.PrincipalAmountToBeSettled.value())
            if _32H_Value is not None:
                currSet.add(_32H_Value)

        if self.swift_message_obj.SequenceB_TransactionDetails.CurrencyAndBalance:
            _32B_Value = get_currency_from_currency_amount(
                self.swift_message_obj.SequenceB_TransactionDetails.CurrencyAndBalance.value())
            if _32B_Value is not None:
                currSet.add(_32B_Value)
        '''
            If all the currecies are same the size of set should be 1
        '''
        if len(currSet) != 1:
            return 'The currency code in the amount fields must be the same for all occurrences of these fields in the entire message, except for fields 33B and 33E in sequence G'

        return ''


