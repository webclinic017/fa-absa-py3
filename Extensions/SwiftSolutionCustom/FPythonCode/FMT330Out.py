"""----------------------------------------------------------------------------
MODULE:
    FMT330Out

DESCRIPTION:
    This module provides the customizable class for the FMT330 outgoing implementation

CLASS:
    FMT330

VERSION: 3.0.1-0.5.3470

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2021-04-15      FAOPS-978       Tawanda Mukhalela       Nqubeko Zondi           Initial Customizations for outgoing
                                                                                MT330s.
------------------------------------------------------------------------------------------------------------------------
"""

import MT330
import acm
import xml.dom.minidom
import FMT330OutBase
import FSwiftWriterLogger
from FFXMMConfirmationOutUtils import *
from FSwiftWriterEngine import validate_with
from FSwiftMLUtils import (
    accepts, get_acm_version, float_to_swiftmt
)
from FSwiftConfirmationUtils import get_trade_date, get_value_date
from FSecuritySettlementOutUtils import represent_negative_amount
import FFXMMConfirmationOutUtils_Override

notifier = FSwiftWriterLogger.FSwiftWriterLogger('FXMMConfOut', 'FFXMMConfirmationOutNotify_Config')


@accepts([acm.FConfirmation, MT330.CTD_ANON, xml.dom.minidom.Document])
class FMT330(FMT330OutBase.FMT330Base):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_obj = swift_obj
        super(FMT330, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)
    # To override existing mappings use below methods to write your own logic
    """
    beneficiary_institution_PartyA_58A
    beneficiary_institution_PartyA_58D
    beneficiary_institution_PartyB_58A
    beneficiary_institution_PartyB_58D
    common_reference_22C
    currency_and_balance_32B
    day_count_fraction_14D
    interest_rate_37G
    partyA_82A
    partyA_82D
    partyB_87A
    partyB_87D
    party_A_role_17R
    period_of_notice_38A
    principle_amount_to_settle_32H
    receiving_agent_PartyA_57A
    receiving_agent_PartyA_57D
    receiving_agent_PartyB_57A
    receiving_agent_PartyB_57D
    related_reference_21
    senders_reference_20
    terms_and_condition_77D
    trade_date_30T
    type_of_event_22B
    type_of_operation_22A
    value_date_30V
    get_user_data
    """

    """
    To override the options provided, use below methods to write your own logic:-
    methods:-
    get_partyA_option (Tag-82 options:A/D)
    get_partyB_option (Tag-87 options:A/D)
    get_receiving_agent_PartyA_option (Tag-57 options:A/D)
    get_receiving_agent_PartyB_option (Tag-57 options:A/D)


    For example:
    def get_partyA_option(self):
       condition = True
       if condition:
           return 'A'
       else:
           return 'D'    
    """

    # getter
    def related_reference_21(self):
        values_dict = {}
        related_confirmation = None
        related_reference = None
        type_of_operation = str(get_type_of_operation(self.acm_obj))

        if self.acm_obj.EventChlItem().Name() == 'Adjust Deposit':
            reference = get_related_confirmation(self.acm_obj)
            related_confirmation = reference if reference else self.acm_obj
            values_dict['ref_conf'] = related_confirmation
            values_dict['related_reference'] = \
                get_confirmation_reference_prefix() + '-' + str(related_confirmation.Oid())

        if type_of_operation in ['AMND', 'CANC']:
            related_confirmation = get_related_confirmation(self.acm_obj)
            related_reference = get_confirmation_reference_prefix() + '-' + str(related_confirmation.Oid())

        if related_reference and related_confirmation:
            values_dict['related_reference'] = related_reference
            values_dict['ref_conf'] = related_confirmation
        return values_dict

    # formatter
    def _format_related_reference_21(self, val):
        related_reference = val.get('related_reference')
        related_confirmation = val.get('ref_conf')
        if self.acm_obj.EventChlItem().Name() != 'Adjust Deposit' or related_confirmation.Oid() != self.acm_obj.Oid():
            related_confirmation, related_reference = check_for_valid_related_reference(
                related_confirmation, related_reference
            )
            version_number_of_related_reference = get_version_for_sent_message_on(related_confirmation, 'MT330')
            val = str(related_reference) + "-" + str(version_number_of_related_reference)
        else:
            val = str(related_reference) + "-" + str(get_message_version_number(related_confirmation))
        return val

    # validator
    @validate_with(MT330.MT330_SequenceA_GeneralInformation_21_Type, is_mandatory=True)
    def _validate_related_reference_21(self, val):
        if self.acm_obj.EventChlItem().Name() != 'Adjust Deposit':
            validate_slash_and_double_slash(val, "Related Reference")
        return val

    def _check_condition_set_related_reference_21(self):
        """
        Checks Conditions to set field 21
        """
        type_of_event = FFXMMConfirmationOutUtils_Override.get_event_type_MT330(self.acm_obj)
        type_of_operation = str(get_type_of_operation(self.acm_obj))

        if type_of_event == 'CONF':
            if type_of_operation in ['AMND', 'CANC']:
                return True
            return False

        return True

    # getter
    def type_of_event_22B(self):
        """
        Get Type of Event
        """
        type_of_event = FFXMMConfirmationOutUtils_Override.get_event_type_MT330(self.acm_obj)
        return type_of_event

    def _check_condition_set_currency_and_balance_32B(self):
        """
        Checks Conditions to set field 32B
        """
        type_of_event = FFXMMConfirmationOutUtils_Override.get_event_type_MT330(self.acm_obj)

        return type_of_event in ['CHNG', 'CINT', 'CONF']

    def _check_condition_set_principle_amount_to_settle_32H(self):

        type_of_event = FFXMMConfirmationOutUtils_Override.get_event_type_MT330(self.acm_obj)
        if self.is_chng_event:
            type_of_event = 'CHNG'

        return type_of_event in ['CHNG', 'CINT', 'SETT']

    # getter
    def principle_amount_to_settle_32H(self):
        amount = 0
        if self.acm_obj.EventChlItem().Name() == 'Adjust Deposit':
            amount = self.acm_obj.CashFlow().FixedAmount()
        return abs(amount)

    # formatter
    def _format_principle_amount_to_settle_32H(self, val):

        if self.acm_obj.EventChlItem().Name() == 'Adjust Deposit':
            currency = self.acm_obj.Trade().Currency().Name()
            settle_amount = apply_currency_precision(currency, float(val))
            principal_amount = str(currency + float_to_swiftmt(settle_amount))
            return principal_amount

        if self.is_chng_event:
            last_amount = self.change_event_dict['last_amount'][3:].replace(',', '.')
            amount = float(last_amount) - float(get_total_fixed_amount_from_cashflow(self.acm_obj))
            amount = 0 if amount < 0 else amount
            currency = self.acm_obj.Trade().Currency().Name()
            sett_amount = apply_currency_precision(currency, float(amount))
            val = currency + float_to_swiftmt(sett_amount)

        return str(val)

    # formatter
    def _format_interest_rate_37G(self, val):
        if val:
            val = represent_negative_amount(val)
            return str(val)

    # getter
    def terms_and_condition_77D(self):
        return {}

    # formatter
    def _format_partyA_82A(self, val):
        bic = val.get('BIC')
        if bic:
            return str(bic)
        return None

    # formatter
    def _format_partyB_87A(self, val):
        bic = val.get('BIC')
        if bic:
            return str(bic)
        return None

    def contract_number_partyA_21N(self):
        """
        Returns a contract number as string
        """
        instrument = self.acm_obj.Trade().Instrument()
        instrument_id = instrument.Oid()
        currency = instrument.Currency().Name()
        contract_number = "{instrument_id}-{currency}".format(
            instrument_id=instrument_id,
            currency=currency
        )
        return contract_number

    # formatter
    def _format_contract_number_partyA_21N(self, val):
        """
        Formats the value provided by getter method
        """
        return val

    # validator
    @validate_with(MT330.MT330_SequenceA_GeneralInformation_21N_Type)
    def _validate_contract_number_partyA_21N(self, val):
        """
        validates the value provided by formatter method
        """
        return val

    # setter
    def _set_contract_number_partyA_21N(self, val):
        """
        sets the value on python object of MT330
        """
        self.swift_obj.SequenceA_GeneralInformation.ContractNumberPartyA = val
        self.swift_obj.SequenceA_GeneralInformation.ContractNumberPartyA.swiftTag = '21N'

    def trade_date_30T(self):
        """
        Default TradeDate to Cash Flow Pay Day
        """
        if self._get_cash_flow_pay_day():
            return self._get_cash_flow_pay_day()

        return get_trade_date(self.acm_obj)

    def value_date_30V(self):
        """
        Default ValueDate to Cash Flow pay day
        """
        if self._get_cash_flow_pay_day():
            return self._get_cash_flow_pay_day()

        return get_value_date(self.acm_obj)

    def _get_cash_flow_pay_day(self):
        cash_flow = self.acm_obj.CashFlow()
        if cash_flow:
            return cash_flow.PayDate()
        return None


class FMT330MessageHeader(FMT330OutBase.FMT330OutBaseMessageHeader):

    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom = None):
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        super(FMT330MessageHeader, self).__init__(acm_obj, swift_msg_tags, swift_metadata_xml_dom)

    # To override existing mappings use below methods to write your own logic

    """
    application_id
    service_id
    sender_logical_terminal_address
    session_number
    sequence_number
    input_or_output
    message_priority
    message_type
    receiver_logical_terminal_address
    delivery_monitoring
    non_delivery_notification_period
    service_identifier
    banking_priority_code
    message_user_reference
    validation_flag
    """


class FMT330NetworkRules(FMT330OutBase.FMT330OutBaseNetworkRules):

    def __init__(self, swift_message_obj, swift_message, acm_obj):
        super(FMT330NetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)

