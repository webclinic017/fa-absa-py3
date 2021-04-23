"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PreSettlementAdviceXMLGenerator
    
DESCRIPTION
    This module contains an object used for generating the XML content for a
    pre-settlement advice.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial Implementation.
                                Tawanda Mukhalela
                                Stuart Wilson
2019-10-14      FAOPS-531       Cuen Edwards            Letitia Carboni         Added support for amendments.
2020-02-21      FAOPS-544/547   Cuen Edwards            Letitia Carboni         Added support for FRAs.
2020-04-20      FAOPS-706       Cuen Edwards            Letitia Carboni         Changed grouping of party settlements on advices from
                                                                                implicit linking via SDSID to explicit linking via advice
                                                                                party additional info.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import math
import xml.etree.ElementTree as ElementTree

import acm

import DocumentGeneral
import PreSettlementAdviceGeneral
from PreSettlementAdviceGeneral import AmendmentActions, AmendmentReasons, Settlement, SettlementInstruction


class GeneratePreSettlementAdviceXMLRequest(object):
    """
    An object embodying the request to generate the XML content for a
    pre-settlement advice.
    """

    def __init__(self, advice_party, instrument_type, from_date, to_date, previous_xml_content):
        """
        Constructor.
        """
        self.advice_party = advice_party
        self.instrument_type = instrument_type
        self.from_date = from_date
        self.to_date = to_date
        self.previous_xml_content = previous_xml_content


class PreSettlementAdviceXMLGenerator(object):
    """
    An object responsible for generating the XML content for a pre-
    settlement advice.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._money_flow_sheet_calculation_space = acm.Calculations().CreateCalculationSpace(
            acm.GetDefaultContext(), acm.FMoneyFlowSheet)
        self._calculation_space_collection = acm.Calculations(
            ).CreateStandardCalculationsSpaceCollection()

    def generate_xml(self, generate_advice_xml_request):
        """
        Generate the XML for a pre-settlement advice
        """
        pre_settlement_advice_element = self._generate_pre_settlement_advice_element(generate_advice_xml_request)
        return ElementTree.tostring(pre_settlement_advice_element)

    def _generate_pre_settlement_advice_element(self, generate_advice_xml_request):
        """
        Generate the PRE_SETTLEMENT_ADVICE XML element and sub-elements.
        """
        advice_party = generate_advice_xml_request.advice_party
        instrument_type = generate_advice_xml_request.instrument_type
        from_date = generate_advice_xml_request.from_date
        to_date = generate_advice_xml_request.to_date
        previous_xml_content = generate_advice_xml_request.previous_xml_content
        element = self._generate_element('PRE_SETTLEMENT_ADVICE')
        element.append(self._generate_element('BANK_ABBREVIATED_NAME', str(DocumentGeneral
            .get_default_bank_abbreviated_name())))
        element.append(self._generate_element('INSTRUMENT_TYPE', instrument_type))
        element.append(self._generate_element('FROM_DATE', from_date))
        element.append(self._generate_element('TO_DATE', to_date))
        pre_settlement_advice_money_flows = PreSettlementAdviceGeneral.get_advice_money_flows(
            advice_party, instrument_type, from_date, to_date)
        element.append(self._generate_settlements_element(pre_settlement_advice_money_flows, previous_xml_content))
        element.append(self._generate_settlement_instructions_element(pre_settlement_advice_money_flows))
        return element

    def _generate_settlements_element(self, pre_settlement_advice_money_flows, previous_xml_content):
        """
        Generate the SETTLEMENTS XML element and sub-elements.
        """
        element = self._generate_element('SETTLEMENTS')
        settlements = self._get_settlements(pre_settlement_advice_money_flows, previous_xml_content)
        settlements.sort(key=lambda settlement: (settlement.bank_trade_reference, settlement.settlement_reference))
        for settlement in settlements:
            element.append(settlement.to_xml_element())
        return element

    def _get_settlements(self, pre_settlement_advice_money_flows, previous_xml_content):
        """
        Create Settlement objects from the specified pre-settlement
        advice money flows and any previous xml content.
        """
        settlements_from_money_flows = self._get_settlements_from_advice_money_flows(
            pre_settlement_advice_money_flows)
        if previous_xml_content is None:
            return settlements_from_money_flows
        remaining_settlements_from_previous_xml = self._get_settlements_from_previous_xml_content(
            previous_xml_content)
        settlements = list()
        # Add current settlements.
        for settlement in settlements_from_money_flows:
            trade_status = acm.FTrade[settlement.bank_trade_reference].Status()
            amendment_reason = None
            if trade_status == 'Void':
                amendment_reason = AmendmentReasons.CANCELLED
            elif trade_status == 'Terminated':
                amendment_reason = AmendmentReasons.TERMINATED
            matching_settlement_from_previous_xml = self._find_matching_settlement_from_previous_xml(
                settlement, remaining_settlements_from_previous_xml)
            if matching_settlement_from_previous_xml is None:
                settlement.amendment_action = AmendmentActions.ADDED
                if amendment_reason is None:
                    amendment_reason = AmendmentReasons.NEW
            else:
                remaining_settlements_from_previous_xml.remove(matching_settlement_from_previous_xml)
                if matching_settlement_from_previous_xml.amendment_action == AmendmentActions.REMOVED:
                    settlement.amendment_action = AmendmentActions.ADDED
                    if amendment_reason is None:
                        amendment_reason = AmendmentReasons.NEW
                elif settlement != matching_settlement_from_previous_xml:
                    settlement.amendment_action = AmendmentActions.UPDATED
                    if amendment_reason is None:
                        amendment_reason = AmendmentReasons.AMENDED
            if amendment_reason is not None:
                settlement.amendment_reason = amendment_reason
            settlements.append(settlement)
        # Add any removed settlements.
        for remaining_settlement_from_previous_xml in remaining_settlements_from_previous_xml:
            trade_status = acm.FTrade[remaining_settlement_from_previous_xml.bank_trade_reference].Status()
            amendment_reason = AmendmentReasons.CANCELLED
            if trade_status == 'Terminated':
                amendment_reason = AmendmentReasons.TERMINATED
            remaining_settlement_from_previous_xml.amendment_action = AmendmentActions.REMOVED
            remaining_settlement_from_previous_xml.amendment_reason = amendment_reason
            settlements.append(remaining_settlement_from_previous_xml)
        return settlements

    def _get_settlements_from_advice_money_flows(self, pre_settlement_advice_money_flows):
        """
        Create Settlement objects from the specified pre-settlement
        advice money flows.
        """
        settlements = list()
        for money_flow in pre_settlement_advice_money_flows:
            settlement = self._get_settlement_from_advice_money_flow(money_flow)
            settlements.append(settlement)
        return settlements

    def _get_settlement_from_advice_money_flow(self, money_flow):
        """
        Create a Settlement object from the specified pre-settlement
        advice money flow.
        """
        trade = money_flow.Trade()
        instrument = trade.Instrument()
        money_flow_amount = round(money_flow.Calculation().Projected(self._calculation_space_collection).Number(), 2)
        counterparty_name = DocumentGeneral.get_party_full_name_and_short_code(trade.Counterparty())
        settlement = Settlement()
        settlement.bank_trade_reference = trade.Oid()
        if DocumentGeneral.is_string_value_present(trade.AdditionalInfo().CCPmiddleware_id()):
            settlement.markitwire_trade_reference = trade.AdditionalInfo().CCPmiddleware_id()
        if DocumentGeneral.is_string_value_present(trade.YourRef()):
            settlement.counterparty_trade_reference = trade.YourRef()
        settlement.settlement_reference = DocumentGeneral.get_money_flow_reference(money_flow)
        settlement.counterparty_name = counterparty_name
        settlement.currency = money_flow.Currency().Name()
        settlement.is_estimate = DocumentGeneral.is_estimated_money_flow(money_flow)
        settlement.amount = money_flow_amount
        settlement.pay_type = money_flow.Type()
        settlement.trade_date = acm.Time.AsDate(trade.TradeTime())
        settlement.effective_date = instrument.StartDate()
        settlement.termination_date = instrument.ExpiryDateOnly()
        settlement.payment_date = money_flow.PayDate()
        if money_flow.Type() in ['Fixed Rate', 'Float Rate', 'Return']:
            cash_flow = money_flow.SourceObject()
            leg = cash_flow.Leg()
            settlement.nominal = round(money_flow.SourceObject().Calculation().Nominal(self
                ._calculation_space_collection, trade, money_flow.Currency()).Number(), 2)
            settlement.payment_business_day_convention = leg.PayDayMethod()
            settlement.payment_calendars = DocumentGeneral.get_leg_payment_calendars(leg)
            settlement.day_count_method = leg.DayCountMethod()
            settlement.rolling_period = DocumentGeneral.get_leg_rolling_period(leg)
            settlement.days = acm.Time.DateDifference(money_flow.EndDate(), money_flow.StartDate())
            if money_flow.Type() in ['Float Rate', 'Return']:
                settlement.float_rate_reference = DocumentGeneral.get_float_rate_reference_name(
                    leg.FloatRateReference())
                settlement.fixing_offset = leg.ResetDayOffset()
                settlement.reset_calendars = DocumentGeneral.get_leg_reset_calendars(leg)
                settlement.reset_business_day_convention = leg.ResetDayMethod()
                if money_flow.Trade().Instrument().InsType() == 'FRA':
                    rate = self._money_flow_sheet_calculation_space.CalculateValue(money_flow,
                        'Cash Analysis Fixing Estimate').Number()
                    settlement.float_rate = rate
                    settlement.fixed_rate = cash_flow.FloatRateOffset()
                else:
                    rate = self._money_flow_sheet_calculation_space.CalculateValue(money_flow,
                        'Cash Analysis Forward Rate') * 100
                    if math.isnan(rate):
                        # Temporary (hopefully) avoidance of AR 753832.
                        rate = None
                    settlement.float_rate = rate
                    settlement.spread = cash_flow.Spread()
            else:
                rate = self._money_flow_sheet_calculation_space.CalculateValue(money_flow,
                    'Cash Analysis Forward Rate') * 100.0
                settlement.fixed_rate = rate
        return settlement

    @staticmethod
    def _get_settlements_from_previous_xml_content(previous_xml_content):
        """
        Create Settlement objects from the specified previous xml
        content.
        """
        settlements = list()
        previous_root_element = ElementTree.fromstring(previous_xml_content)
        for settlement_element in previous_root_element.iterfind('SETTLEMENTS/SETTLEMENT'):
            settlement = Settlement.from_xml_element(settlement_element)
            settlements.append(settlement)
        return settlements

    @staticmethod
    def _find_matching_settlement_from_previous_xml(settlement, settlements_from_previous_xml):
        """
        Find any Settlement object, created from previous xml content,
        that is for the same settlement as the specified Settlement
        object.
        """
        for settlement_from_previous_xml in settlements_from_previous_xml:
            if settlement_from_previous_xml.bank_trade_reference != settlement.bank_trade_reference:
                continue
            if settlement_from_previous_xml.settlement_reference != settlement.settlement_reference:
                continue
            return settlement_from_previous_xml
        return None

    def _generate_settlement_instructions_element(self, pre_settlement_advice_money_flows):
        """
        Generate the SETTLEMENT_INSTRUCTIONS XML element and sub-elements.
        """
        element = self._generate_element('SETTLEMENT_INSTRUCTIONS')
        instructions_by_currency = self._get_instructions_by_currency(pre_settlement_advice_money_flows)
        currencies = list(instructions_by_currency.keys())
        currencies.sort()
        for currency in currencies:
            instructions = instructions_by_currency[currency]
            # Ensure that there aren't conflicting details.
            if len(instructions) > 1:
                self._raise_conflicting_instructions_exception(currency, instructions,
                    pre_settlement_advice_money_flows)
            element.append(instructions[0].to_xml_element())
        return element

    def _get_instructions_by_currency(self, pre_settlement_advice_money_flows):
        """
        Get a dictionary of all distinct settlement instructions by
        currency.
        """
        # Get a distinct set of accounts.
        distinct_acquirer_accounts = set()
        for money_flow in pre_settlement_advice_money_flows:
            if money_flow.AcquirerAccount() is None:
                error_message = "No settlement instruction found for currency '{currency_name}' "
                error_message += "and acquirer: '{acquirer_name}'."
                raise ValueError(error_message.format(
                    currency_name=money_flow.Currency().Name(),
                    acquirer_name=money_flow.Trade().Acquirer().Name()
                ))
            distinct_acquirer_accounts.add(money_flow.AcquirerAccount())
        # Get the instructions by currency.
        instructions_by_currency = dict()
        for acquirer_account in distinct_acquirer_accounts:
            instruction = self._get_settlement_instruction_from_acquirer_account(acquirer_account)
            currency = instruction.currency
            if currency not in list(instructions_by_currency.keys()):
                instructions_by_currency[currency] = list()
                instructions_by_currency[currency].append(instruction)
            else:
                instructions = instructions_by_currency[currency]
                matching_instructions = self._find_matching_settlement_instruction(instruction, instructions)
                if matching_instructions is None:
                    instructions_by_currency[currency].append(instruction)
        return instructions_by_currency

    def _get_settlement_instruction_from_acquirer_account(self, acquirer_account):
        """
        Create a Settlement Instruction object from the specified
        acquirer account.
        """
        currency = acquirer_account.Currency().Name()
        account_number = self._get_account_number(acquirer_account)
        bank_party = DocumentGeneral.get_bank_party()
        beneficiary_bank_name = DocumentGeneral.get_party_full_name(bank_party)
        beneficiary_bank_bic = bank_party.Swift()
        correspondent_bank_name = DocumentGeneral.get_party_full_name(acquirer_account.CorrespondentBank())
        correspondent_bank_bic = acquirer_account.Bic().Name()
        instruction = SettlementInstruction()
        instruction.currency = currency
        instruction.account_number = account_number
        instruction.beneficiary_bank_name = beneficiary_bank_name
        instruction.beneficiary_bank_bic = beneficiary_bank_bic
        instruction.correspondent_bank_name = correspondent_bank_name
        instruction.correspondent_bank_bic = correspondent_bank_bic
        return instruction

    @staticmethod
    def _get_account_number(account):
        """
        Get the account number of an account.
        """
        currency = account.Currency()
        # Remove branch code from ZAR account numbers.
        if currency.Name() != 'ZAR':
            return account.Account()
        if ' ' in account.Account():
            return account.Account().split(' ')[1]
        return account.Account()

    @staticmethod
    def _find_matching_settlement_instruction(instruction, instructions):
        """
        Find any existing instruction that matches (refers to
        the same account as) the specified instruction.
        """
        for existing_instruction in instructions:
            if existing_instruction == instruction:
                return existing_instruction
        return None

    def _raise_conflicting_instructions_exception(self, currency, currency_instructions,
            pre_settlement_advice_money_flows):
        """
        Raise a exception indicating that conflicting settlement
        instructions were encountered for the specified currency.
        """
        error_message = "Conflicting settlement instructions found for "
        error_message += "currency '{currency_name}':\n"
        for instruction in currency_instructions:
            acquirers = self._find_acquirers_using_instruction(instruction, pre_settlement_advice_money_flows)
            error_message += "\n- {instruction_description}".format(
                instruction_description=self._get_settlement_instruction_description(instruction, acquirers)
            )
        raise ValueError(error_message.format(
            currency_name=currency
        ))

    def _find_acquirers_using_instruction(self, instruction, pre_settlement_advice_money_flows):
        """
        Get a distinct set of acquirers using using the specified
        settlement instruction.
        """
        acquirers = set()
        for money_flow in pre_settlement_advice_money_flows:
            acquirer_account = money_flow.AcquirerAccount()
            if acquirer_account.Currency().Name() != instruction.currency:
                continue
            settlement_instruction = self._get_settlement_instruction_from_acquirer_account(acquirer_account)
            if settlement_instruction != instruction:
                continue
            acquirers.add(money_flow.AcquirerAccount().Party())
        acquirers = list(acquirers)
        acquirers.sort(key=lambda acquirer: acquirer.Name())
        return acquirers

    @staticmethod
    def _get_settlement_instruction_description(instruction, acquirers):
        """
        Get a textural description of a settlement instruction.
        """
        acquirers_description = ''
        for acquirer in acquirers:
            if len(acquirers_description) > 0:
                acquirers_description += ', '
            acquirers_description += "'{acquirer_name}'".format(acquirer_name=acquirer.Name())
        acquirer_label = 'Acquirer'
        if len(acquirers) > 1:
            acquirer_label += 's'
        description = "Account Number: '{account_number}', Correspondent Bank: '{correspondent_bank_name}', "
        description += "Correspondent Bank BIC: '{correspondent_bank_bic}' ({acquirer_label}: {acquirers_description})"
        return description.format(
            account_number=instruction.account_number,
            correspondent_bank_name=instruction.correspondent_bank_name,
            correspondent_bank_bic=instruction.correspondent_bank_bic,
            acquirer_label=acquirer_label,
            acquirers_description=acquirers_description
        )

    @staticmethod
    def _generate_element(element_name, element_text=''):
        """
        Generate an XML element with the specified name and text.
        """
        element = ElementTree.Element(element_name)
        element.text = element_text
        return element
