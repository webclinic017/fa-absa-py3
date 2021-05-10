"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TermStatementXMLGenerator
    
DESCRIPTION
    This module contains an object used for generating the XML content for a
    term deposit statement.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-05-15      FAOPS-127       Cuen Edwards            Elaine Visagie          Initial Implementation.
2019-04-29      FAOPS-402       Cuen Edwards            Chris van der Walt      Changed to support generation up to current date.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

import DocumentGeneral
from DocumentXMLGenerator import DocumentXMLGenerator, GenerateDocumentXMLRequest
import TermStatementGeneral


class GenerateTermStatementXMLRequest(GenerateDocumentXMLRequest):
    """
    An object embodying the request to generate the XML content for a 
    term deposit statement.
    """

    def __init__(self, from_party, from_party_contact, to_party, to_party_contact,
            from_date, to_date, schedule=None):
        """
        Constructor.
        """
        super(GenerateTermStatementXMLRequest, self).__init__(from_party, from_party_contact,
            to_party, to_party_contact)
        self.from_date = from_date
        self.to_date = to_date
        self.schedule = schedule


class TermStatementXMLGenerator(DocumentXMLGenerator):
    """
    An object responsible for generating the XML content for a term 
    deposit statement.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._money_flow_sheet_calculation_space = acm.Calculations().CreateCalculationSpace(
            acm.GetDefaultContext(), acm.FMoneyFlowSheet)
        self._calculation_space_collection = acm.Calculations(
            ).CreateStandardCalculationsSpaceCollection()

    def generate_xml(self, generate_term_statement_xml_request):
        """
        Generate the XML for a term deposit statement.
        """
        self._ensure_using_supported_accrued_inclusion_method()
        return super(TermStatementXMLGenerator, self).generate_xml(
            generate_term_statement_xml_request)

    @staticmethod
    def _ensure_using_supported_accrued_inclusion_method():
        """
        Ensure that the XML for a term deposit statement is 
        only generated for a supported accrued inclusion method.
        """
        accounting_parameters = acm.GetFunction("mappedGlobalAccountingParameters", 0)().Parameter()
        accrued_inclusion_method = accounting_parameters.AccruedInclusionMethod()
        if accrued_inclusion_method != 'None':
            error_message = "Unsupported accrued inclusion method "
            error_message += "'{accrued_inclusion_method}' specified."
            raise ValueError(error_message.format(
                accrued_inclusion_method=accrued_inclusion_method
            ))

    def _generate_subject_element(self, generate_term_statement_xml_request):
        """
        Generate the document SUBJECT XML element and sub-
        elements.
        """
        statement_from_date = generate_term_statement_xml_request.from_date
        statement_to_date = generate_term_statement_xml_request.to_date
        subject = 'Interest Statement for {period_description}'
        period_description = DocumentGeneral.get_date_range_description(
            statement_from_date, statement_to_date)
        subject = subject.format(
            period_description=period_description
        )
        return self._generate_element('SUBJECT', subject)

    def _generate_document_specific_element(self, generate_term_statement_xml_request):
        """
        Generate the TERM_STATEMENT XML element and sub-elements.
        """
        acquirer = generate_term_statement_xml_request.from_party
        counterparty = generate_term_statement_xml_request.to_party
        statement_from_date = generate_term_statement_xml_request.from_date
        statement_to_date = generate_term_statement_xml_request.to_date
        statement_schedule = generate_term_statement_xml_request.schedule
        element = self._generate_element('TERM_STATEMENT')
        element.append(self._generate_period_element(statement_from_date, statement_to_date))
        if statement_schedule:
            element.append(self._generate_element('SCHEDULE', statement_schedule))
        element.extend(self._generate_currency_values_elements(acquirer, counterparty,
            statement_from_date, statement_to_date))
        return element

    def _generate_period_element(self, statement_from_date, statement_to_date):
        """
        Generate the PERIOD XML element and sub-elements for a term 
        deposit statement.
        """
        element = self._generate_element('PERIOD')
        element.append(self._generate_element('FROM_DATE', statement_from_date))
        element.append(self._generate_element('TO_DATE', statement_to_date))
        return element

    def _generate_currency_values_elements(self, acquirer, counterparty,
            statement_from_date, statement_to_date):
        """
        Generate the CURRENCY_VALUES XML elements and sub-elements 
        for all term deposit currencies included in the term deposit 
        statement.
        """
        elements = list()
        trades = TermStatementGeneral.get_statement_trades(acquirer, counterparty,
            statement_from_date, statement_to_date)
        currencies = self._get_term_deposit_currencies(trades)
        currencies.sort(key=lambda currency: currency.Name())
        for currency in currencies:
            trades_in_currency = self._get_trades_in_currency(currency, trades)
            trades_in_currency.sort(key=lambda trade: trade.Oid())
            element = self._generate_currency_values_element(trades_in_currency,
                currency, statement_from_date, statement_to_date)
            elements.append(element)
        return elements

    def _generate_currency_values_element(self, trades, currency, statement_from_date,
            statement_to_date):
        """
        Generate the CURRENCY_VALUES XML element and sub-elements for 
        a single term deposit currency included in the term deposit 
        statement.
        """
        element = self._generate_element('CURRENCY_VALUES')
        element.append(self._generate_element('CURRENCY', currency.Name()))
        element.extend(self._generate_term_deposit_values_elements(trades, statement_from_date,
            statement_to_date))
        element.append(self._generate_currency_values_totals_element(element))
        return element

    def _generate_term_deposit_values_elements(self, trades, statement_from_date, statement_to_date):
        """
        Generate the TERM_DEPOSIT_VALUES XML elements and sub-elements 
        for all term deposit trades in a given currency.
        """
        elements = list()
        for trade in trades:
            element = self._generate_term_deposit_values_element(trade, statement_from_date,
                statement_to_date)
            elements.append(element)
        return elements

    def _generate_term_deposit_values_element(self, trade, statement_from_date,
            statement_to_date):
        """
        Generate the TERM_DEPOSIT_VALUES XML element and sub-elements 
        for a single term deposit trade.
        """
        element = self._generate_element('TERM_DEPOSIT_VALUES')
        # Reference.
        element.append(self._generate_element('REFERENCE', str(trade.Oid())))
        # Type.
        element.append(self._generate_element('TYPE', self.get_term_deposit_trade_type(trade)))
        # Nominal Amount.
        element.append(self._generate_element('NOMINAL_AMOUNT', str(self._negate_amount(trade.Nominal()))))
        # Start Date.
        element.append(self._generate_element('START_DATE', trade.ValueDay()))
        # Maturity Date.
        element.append(self._generate_element('MATURITY_DATE', trade.Instrument()
            .ExpiryDateOnly()))
        interest_money_flows = TermStatementGeneral.get_interest_money_flows_between_dates(
            trade, statement_from_date, statement_to_date)
        # Interest Rate.
        interest_rate = self._get_latest_interest_rate(interest_money_flows)
        element.append(self._generate_element('INTEREST_RATE', str(interest_rate)))
        # Interest Accrued Previous.
        interest_accrued_previous = self._get_term_deposit_interest_accrued_previous(trade,
            interest_money_flows, statement_from_date, statement_to_date)
        element.append(self._generate_element('INTEREST_ACCRUED_PREVIOUS',
            str(self._negate_amount(interest_accrued_previous))))
        # Interest Accrued Current.    
        interest_accrued_current = self._get_term_deposit_interest_accrued_current(trade,
            interest_money_flows, statement_from_date, statement_to_date)
        element.append(self._generate_element('INTEREST_ACCRUED_CURRENT',
            str(self._negate_amount(interest_accrued_current))))
        # Interest Settled Current.
        interest_settled_current = self._get_term_deposit_interest_settled_current(trade,
            statement_from_date, statement_to_date)
        element.append(self._generate_element('INTEREST_SETTLED_CURRENT',
            str(self._negate_amount(interest_settled_current))))
        # Balance.
        balance = self.get_term_deposit_balance(trade, interest_accrued_previous,
            interest_accrued_current, statement_to_date)
        element.append(self._generate_element('BALANCE', str(self._negate_amount(balance))))
        # Status.
        element.append(self._generate_element('STATUS', self._get_term_deposit_status(trade,
            statement_to_date)))
        return element

    @staticmethod
    def _get_term_deposit_currencies(trades):
        """
        Get a distinct list of term deposit currencies included in 
        the statement.
        """
        currencies = list()
        for trade in trades:
            currency = trade.Instrument().Currency()
            if currency not in currencies:
                currencies.append(currency)
        return currencies

    @staticmethod
    def _get_trades_in_currency(currency, trades):
        """
        Get a list of term deposit trades for a given currency.
        """
        trades_in_currency = list()
        for trade in trades:
            if trade.Instrument().Currency() == currency:
                trades_in_currency.append(trade)
        return trades_in_currency

    @staticmethod
    def get_term_deposit_trade_type(trade):
        """
        Get the deposit type of a term deposit trade.
        """
        if trade.AdditionalInfo().Funding_Instype():
            return trade.AdditionalInfo().Funding_Instype()
        elif trade.AdditionalInfo().MM_Instype():
            return trade.AdditionalInfo().MM_Instype()
        return None

    def _get_latest_interest_rate(self, interest_money_flows):
        """
        Get the interest rate of the latest interest moneyflow.
        """
        latest_interest_money_flow = self._get_latest_interest_money_flow(interest_money_flows)
        return round(self._money_flow_sheet_calculation_space.CalculateValue(latest_interest_money_flow,
            'Cash Analysis Forward Rate') * 100.0, 3)

    def _get_term_deposit_interest_accrued_previous(self, trade, interest_money_flows,
            statement_from_date, statement_to_date):
        """
        Get the interest accrued prior to the current statement period 
        for any moneyflow that settles after the statement period for 
        a given term deposit trade.
        """
        money_flow = self._get_money_flow_starting_before_and_settling_after_statement_period(
            interest_money_flows, statement_from_date, statement_to_date)
        if money_flow is None:
            return 0.0
        # Please note that accrued interest is shown on the statement 
        # offset by +1 day.
        # Exclusive start date.
        start_date = money_flow.StartDate()
        # Inclusive end date (offset by +1 day).
        end_date = statement_from_date
        interest_accrued_previous = self._get_interest_between_dates(trade, start_date,
            end_date)
        return interest_accrued_previous

    def _get_term_deposit_interest_accrued_current(self, trade, interest_money_flows,
            statement_from_date, statement_to_date):
        """
        Get the interest accrued during the current statement period for 
        any moneyflow that settles after the statement period.
        """
        money_flow = self._get_money_flow_accruing_interest_during_and_settling_after_statement_period(
            interest_money_flows, statement_to_date)
        if money_flow is None:
            return 0.0
        # Please note that accrued interest is shown on the statement 
        # offset by +1 day.      
        # Exclusive start date (offset by +1 day).
        start_date = statement_from_date
        if money_flow.StartDate() > start_date:
            start_date = money_flow.StartDate()
        # Inclusive end date (offset by +1 day).
        # If the statement is requested up until the current date, do
        # not show interest accrued until the balance has been held
        # overnight (i.e. max to date = yesterday).
        yesterday = self._get_previous_day(acm.Time.DateToday())
        interest_to_date = min(statement_to_date, yesterday)
        end_date = self._get_next_day(interest_to_date)
        interest_accrued_current = self._get_interest_between_dates(trade, start_date,
            end_date)
        return interest_accrued_current

    def _get_term_deposit_interest_settled_current(self, trade, statement_from_date,
            statement_to_date):
        """
        Get the interest settling during the current statement period.
        """
        # Convert inclusive statement from date to exclusive calculation 
        # start date.
        start_date = self._get_previous_day(statement_from_date)
        # Inclusive end date.
        end_date = statement_to_date
        interest_settled_current = self._get_interest_settled_between_dates(trade, start_date,
            end_date)
        return interest_settled_current

    def get_term_deposit_balance(self, trade, interest_accrued_previous, interest_accrued_current,
            statement_to_date):
        """
        Get the balance at the end of the statement period for a term 
        deposit trade.
        """
        growth = None
        if self._term_deposit_expires_before_end_of_statement_period(trade, statement_to_date):
            growth = self._get_interest_settled_between_dates(trade, trade.ValueDay(),
                trade.Instrument().ExpiryDateOnly())
        else:
            growth = interest_accrued_previous + interest_accrued_current
        return trade.Nominal() + growth

    def _get_term_deposit_status(self, trade, to_date):
        """
        Get the status at the end of the statement period for a term 
        deposit trade.
        """
        if self._term_deposit_expires_before_end_of_statement_period(trade, to_date):
            return 'Matured'
        return 'Live'

    def _generate_currency_values_totals_element(self, currency_values_element):
        """
        Generate the TOTALS XML element and sub-elements for a currency 
        values element.
        """
        element = self._generate_element('TOTALS')
        value_element_names = [
            'NOMINAL_AMOUNT',
            'INTEREST_ACCRUED_PREVIOUS',
            'INTEREST_ACCRUED_CURRENT',
            'INTEREST_SETTLED_CURRENT',
            'BALANCE'
        ]
        for value_element_name in value_element_names:
            element.append(self._generate_currency_values_total_element(currency_values_element,
                value_element_name))
        return element

    def _generate_currency_values_total_element(self, currency_values_element, value_element_name):
        """
        Generate an element containing the sum of and the same name 
        as a specified term deposit value name.
        """
        total = 0.0
        for element in currency_values_element.iterfind('./TERM_DEPOSIT_VALUES/{value_element_name}'
                .format(value_element_name=value_element_name)):
            total += float(element.text)
        return self._generate_element(value_element_name, str(total))

    @staticmethod
    def _get_latest_interest_money_flow(interest_money_flows):
        """
        Get the latest interest money flow from a list of interest 
        money flows.
        """
        interest_money_flows = sorted(interest_money_flows, key=lambda money_flow:
            money_flow.PayDay(), reverse=True)
        return interest_money_flows[0]

    @staticmethod
    def _get_money_flow_starting_before_and_settling_after_statement_period(
            interest_money_flows, statement_from_date, statement_to_date):
        """
        Find any interest money flow starting before the statement 
        period and settling after the statement period.

        Please note that for correctly booked term deposit instruments 
        there should be a maximum of one such interest moneyflow but 
        due to the ability to manually and programmatically edit 
        cashflows in Front Arena it is at least theoretically possible 
        that multiple may be encountered.  If such a scenario is 
        encountered then this function will fail-fast, as the statement 
        requirements do not support such.
        """
        money_flow = None
        for interest_money_flow in interest_money_flows:
            # Statement from date is exclusive.
            if interest_money_flow.StartDate() > statement_from_date:
                continue
            if interest_money_flow.EndDate() <= statement_to_date:
                continue
            if money_flow is not None:
                exception_message = 'Encountered more than one interest moneyflow '
                exception_message += 'starting before and settling after the statement '
                exception_message += 'period.'
                raise ValueError(exception_message)
            money_flow = interest_money_flow
        return money_flow

    @staticmethod
    def _get_money_flow_accruing_interest_during_and_settling_after_statement_period(
            interest_money_flows, statement_to_date):
        """
        Find any interest money flow accruing interest during the 
        statement period and settling after the statement period.
        
        Please note that for correctly booked term deposit instruments 
        there should be a maximum of one such interest moneyflow but 
        due to the ability to manually and programmatically, etc. edit 
        cashflows in Front Arena it is at least theoretically possible 
        that multiple may be encountered.  If such a scenario is 
        encountered then this function will fail-fast, as the statement 
        requirements do not support such.
        """
        money_flow = None
        for interest_money_flow in interest_money_flows:
            if interest_money_flow.StartDate() > statement_to_date:
                continue
            if interest_money_flow.EndDate() <= statement_to_date:
                continue
            if money_flow is not None:
                exception_message = 'Encountered more than one interest moneyflow '
                exception_message += 'accruing interest during and settling after '
                exception_message += 'the statement period.'
                raise ValueError(exception_message)
            money_flow = interest_money_flow
        return money_flow

    def _get_interest_between_dates(self, trade, start_date, end_date):
        """
        Get the interest earned for a term deposit trade between an 
        exclusive profit and loss start date and an inclusive profit 
        and loss end date.
        """
        currency = trade.Instrument().Currency()
        interest_accrued = trade.Calculation().AccruedInterest(self._calculation_space_collection,
            start_date, end_date, currency, None, 0).Number()
        interest_settled = self._get_interest_settled_between_dates(trade, start_date, end_date)
        return interest_accrued + interest_settled

    def _get_interest_settled_between_dates(self, trade, start_date, end_date):
        """
        Get the interest settled for a term deposit trade between an 
        exclusive profit and loss start date and an inclusive profit 
        and loss end date.
        """
        currency = trade.Instrument().Currency()
        interest_settled = trade.Calculation().SettledInterest(self
            ._calculation_space_collection, start_date, end_date,
            currency, None, 0).Number()
        return interest_settled

    @staticmethod
    def _term_deposit_expires_before_end_of_statement_period(trade,
            statement_to_date):
        """
        Determine if a term deposit trade expires by the end of the 
        statement period.
        """
        if trade.Instrument().ExpiryDateOnly() <= statement_to_date:
            return True
        return False

    @staticmethod
    def _negate_amount(amount):
        """
        Invert the sign of an amount.
        """
        return amount * -1

    @staticmethod
    def _get_previous_day(date):
        """
        Get the day before a given date.
        """
        return acm.Time.DateAddDelta(date, 0, 0, -1)

    @staticmethod
    def _get_next_day(date):
        """
        Get the day after a given date.
        """
        return acm.Time.DateAddDelta(date, 0, 0, 1)
