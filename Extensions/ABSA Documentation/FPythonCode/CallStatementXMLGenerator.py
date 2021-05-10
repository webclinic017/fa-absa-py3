"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    CallStatementXMLGenerator
    
DESCRIPTION
    This module contains an object used for generating the XML content for a
    call deposit statement.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-08-14      FAOPS-167       Cuen Edwards            Elaine Visagie          Initial Implementation.
2018-11-08      FAOPS-319       Cuen Edwards            Nicolette Burger        Replaced usage of 'Deposit balance' column with custom
                                                                                calculation as 'Deposit balance' is inaccurate.
2018-12-05      FAOPS-328       Cuen Edwards            Nicolette Burger        Change to support multiple call interest cashflows on a
                                                                                single date.
2019-03-11      FAOPS-401       Cuen Edwards            Chris van der Walt      Changed to support generation up to current date.
2020-02-11      FAOPS-747       Cuen Edwards            Michelle Fowler         Changed to hide interest settling on the current date
                                                                                if the interest cash flow is still accruing.
2020-03-12      FAOPS-767       Cuen Edwards            Kgomotso Gumbo          Changed to prevent generation for incorrectly booked
                                                                                accounts.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

import CallStatementGeneral
import DocumentGeneral
from DocumentXMLGenerator import DocumentXMLGenerator, GenerateDocumentXMLRequest


class GenerateCallStatementXMLRequest(GenerateDocumentXMLRequest):
    """
    An object embodying the request to generate the XML content for a
    call deposit statement.
    """

    def __init__(self, trade, from_party, from_party_contact, to_party, to_party_contact,
            from_date, to_date, schedule=None):
        """
        Constructor.
        """
        super(GenerateCallStatementXMLRequest, self).__init__(from_party, from_party_contact,
            to_party, to_party_contact)
        self.trade = trade
        self.from_date = from_date
        self.to_date = to_date
        self.schedule = schedule


class CallStatementXMLGenerator(DocumentXMLGenerator):
    """
    An object responsible for generating the XML content for a call
    deposit statement.
    """

    def generate_xml(self, generate_call_statement_xml_request):
        """
        Generate the XML for a call deposit statement.
        """
        self._ensure_using_supported_accrued_inclusion_method()
        trade = generate_call_statement_xml_request.trade
        self._ensure_deposit_correctly_booked(trade)
        self._ensure_deposit_has_no_reinvestment_exercise_events(trade)
        return super(CallStatementXMLGenerator, self).generate_xml(
            generate_call_statement_xml_request)

    @staticmethod
    def _ensure_using_supported_accrued_inclusion_method():
        """
        Ensure that the XML for a call deposit statement is only
        generated for a supported accrued inclusion method.
        """
        accounting_parameters = acm.GetFunction("mappedGlobalAccountingParameters", 0)().Parameter()
        accrued_inclusion_method = accounting_parameters.AccruedInclusionMethod()
        if accrued_inclusion_method != 'None':
            error_message = "Unsupported accrued inclusion method "
            error_message += "'{accrued_inclusion_method}' specified."
            raise ValueError(error_message.format(
                accrued_inclusion_method=accrued_inclusion_method
            ))

    @classmethod
    def _ensure_deposit_correctly_booked(cls, trade):
        """
        Ensure that the XML for a call deposit statement is only
        generated for a deposit that is correctly booked.

        This allows statement generation to fail-fast rather than
        risking silent failure and the creation of a possibly
        incorrect statement.
        """
        cls._ensure_instrument_rounding_spec_correctly_booked(trade.Instrument())
        cls._ensure_trade_dates_correctly_booked(trade)
        for money_flow in trade.MoneyFlows().AsArray():
            cls._ensure_money_flow_dates_correctly_booked(trade, money_flow)

    @staticmethod
    def _ensure_instrument_rounding_spec_correctly_booked(instrument):
        """
        Ensure that the instrument rounding specification is set to
        call account rounding.
        """
        call_account_rounding_specification = acm.FRoundingSpec['Call_account_rounding']
        rounding_specification = instrument.RoundingSpecification()
        if rounding_specification != call_account_rounding_specification:
            error_message = "Incorrectly booked deposit detected - instrument round specification "
            error_message += "not equal to '{rounding_specification_name}'."
            raise ValueError(error_message.format(
                rounding_specification_name=call_account_rounding_specification.Name()
            ))

    @staticmethod
    def _ensure_trade_dates_correctly_booked(trade):
        """
        Ensure that trade acquire and value dates are aligned with
        instrument start date.
        """
        instrument = trade.Instrument()
        if trade.AcquireDay() != instrument.StartDate():
            error_message = "Incorrectly booked deposit detected - trade acquire day '{acquire_day}' "
            error_message += "not equal to instrument start date '{start_date}'."
            raise ValueError(error_message.format(
                acquire_day=trade.AcquireDay(),
                start_date=instrument.StartDate()
            ))
        if trade.ValueDay() != instrument.StartDate():
            error_message = "Incorrectly booked deposit detected - trade value day '{value_day}' "
            error_message += "not equal to instrument start date '{start_date}'."
            raise ValueError(error_message.format(
                value_day=trade.ValueDay(),
                start_date=instrument.StartDate()
            ))

    @staticmethod
    def _ensure_money_flow_dates_correctly_booked(trade, money_flow):
        """
        Ensure that money flow start and pay dates do not precede the
        instrument start date.
        """
        instrument = trade.Instrument()
        if money_flow.StartDate():
            if money_flow.StartDate() < instrument.StartDate():
                error_message = "Incorrectly booked deposit detected - {money_flow_type} "
                error_message += "{money_flow_reference} start date '{money_flow_start_date}' "
                error_message += "precedes instrument start date '{instrument_start_date}'."
                raise ValueError(error_message.format(
                    money_flow_type=money_flow.Type(),
                    money_flow_reference=DocumentGeneral.get_money_flow_reference(money_flow),
                    money_flow_start_date=money_flow.StartDate(),
                    instrument_start_date=instrument.StartDate()
                ))
        if money_flow.PayDate() < instrument.StartDate():
            error_message = "Incorrectly booked deposit detected - {money_flow_type} "
            error_message += "{money_flow_reference} pay date '{money_flow_pay_date}' "
            error_message += "precedes instrument start date '{instrument_start_date}'."
            raise ValueError(error_message.format(
                money_flow_type=money_flow.Type(),
                money_flow_reference=DocumentGeneral.get_money_flow_reference(money_flow),
                money_flow_pay_date=money_flow.PayDate(),
                instrument_start_date=instrument.StartDate()
            ))

    def _ensure_deposit_has_no_reinvestment_exercise_events(self, trade):
        """
        Ensure that the XML for a call deposit statement is only
        generated for a deposit that does not have reinvestment
        exercise events.

        Business indicated that call deposits should not be booked in
        this way and so this does not need to be supported.  As such,
        statement generation has been designed to fail-fast if this
        is encountered rather than risking silent failure and the
        creation of a possibly incorrect statement.
        """
        if self._has_reinvestment_exercise_events(trade):
            error_message = "Deposits with reinvestment exercise events "
            error_message += "are not currently supported."
            raise ValueError(error_message)

    @staticmethod
    def _has_reinvestment_exercise_events(trade):
        """
        Determines whether or not a trade has reinvestment events.
        """
        for exercise_event in trade.Instrument().ExerciseEvents():
            if exercise_event.Type() == 'Reinvestment':
                return True
        return False

    def _generate_subject_element(self, generate_call_statement_xml_request):
        """
        Generate the document SUBJECT XML element and sub-
        elements.
        """
        statement_from_date = generate_call_statement_xml_request.from_date
        statement_to_date = generate_call_statement_xml_request.to_date
        subject = 'Statement for {period_description}'
        period_description = DocumentGeneral.get_date_range_description(
            statement_from_date, statement_to_date)
        subject = subject.format(
            period_description=period_description
        )
        return self._generate_element('SUBJECT', subject)

    def _generate_document_specific_element(self, generate_call_statement_xml_request):
        """
        Generate the CALL_STATEMENT XML element and sub-elements.
        """
        statement_from_date = generate_call_statement_xml_request.from_date
        statement_to_date = generate_call_statement_xml_request.to_date
        statement_schedule = generate_call_statement_xml_request.schedule
        trade = generate_call_statement_xml_request.trade
        element = self._generate_element('CALL_STATEMENT')
        element.append(self._generate_period_element(statement_from_date, statement_to_date))
        if statement_schedule:
            element.append(self._generate_element('SCHEDULE', statement_schedule))
        element.append(self._generate_account_details_element(trade))
        statement_money_flows = CallStatementGeneral.get_statement_money_flows(trade,
            statement_from_date, statement_to_date)
        account_balance_from_date = self._get_earliest_required_account_balance_date(
            statement_from_date, statement_money_flows)
        account_balance_by_date = self._get_account_balance_by_date(trade, account_balance_from_date,
            statement_to_date)
        element.append(self._generate_summary_values_element(trade, statement_from_date,
            statement_to_date, statement_money_flows, account_balance_by_date))
        element.append(self._generate_transaction_values_element(statement_from_date,
            statement_to_date, statement_money_flows, account_balance_by_date))
        element.append(self._generate_daily_interest_values_element(statement_from_date,
            statement_to_date, statement_money_flows, account_balance_by_date))
        return element

    def _get_account_balance_by_date(self, trade, account_balance_from_date, account_balance_to_date):
        """
        Create dictionary of all account balances, stored by date,
        that are required for call statement generation.

        Note that this is done to avoid repeated calls to calculate
        the account balance.
        """
        account_balance_by_date = {}
        statement_money_flows = CallStatementGeneral.get_statement_money_flows(trade,
            account_balance_from_date, account_balance_to_date)
        unprocessed_transaction_money_flows = self._get_transaction_money_flows(account_balance_from_date,
            account_balance_to_date, statement_money_flows)
        unprocessed_transaction_money_flows = sorted(unprocessed_transaction_money_flows,
            key=lambda money_flow: (CallStatementGeneral.get_money_flow_value_date(money_flow),
            money_flow.SourceObject().CreateTime(), money_flow.SourceObject().Oid()))
        opening_balance_date = self._get_previous_day(account_balance_from_date)
        current_balance = self._get_account_balance(trade, opening_balance_date)
        account_balance_by_date[opening_balance_date] = current_balance
        current_date = account_balance_from_date
        next_date = self._get_next_day(current_date)
        while current_date <= account_balance_to_date:
            # Adjust balance.
            for transaction_money_flow in list(unprocessed_transaction_money_flows):
                value_date = CallStatementGeneral.get_money_flow_value_date(transaction_money_flow)
                if value_date > current_date:
                    break
                # Add any amounts affecting the account balance.
                if CallStatementGeneral.money_flow_affects_account_balance(transaction_money_flow):
                    money_flow_amount = DocumentGeneral.get_money_flow_amount(transaction_money_flow)
                    current_balance += money_flow_amount
                unprocessed_transaction_money_flows.remove(transaction_money_flow)
            account_balance_by_date[current_date] = current_balance
            current_date = next_date
            next_date = self._get_next_day(current_date)
        return account_balance_by_date

    @staticmethod
    def _get_earliest_required_account_balance_date(statement_from_date, statement_money_flows):
        """
        Determine the earliest date from which an account balance is
        required for call statement generation.
        """
        earliest_required_account_balance_date = statement_from_date
        for statement_money_flow in statement_money_flows:
            if not CallStatementGeneral.is_interest_money_flow(statement_money_flow):
                continue
            if statement_money_flow.StartDate() < earliest_required_account_balance_date:
                earliest_required_account_balance_date = statement_money_flow.StartDate()
        return earliest_required_account_balance_date

    def _generate_period_element(self, statement_from_date, statement_to_date):
        """
        Generate the PERIOD XML element and sub-elements for a call
        deposit statement.
        """
        element = self._generate_element('PERIOD')
        element.append(self._generate_element('FROM_DATE', statement_from_date))
        element.append(self._generate_element('TO_DATE', statement_to_date))
        return element

    def _generate_account_details_element(self, trade):
        """
        Generate the ACCOUNT_DETAILS XML element and sub-elements for a call
        deposit statement.
        """
        element = self._generate_element('ACCOUNT_DETAILS')
        instrument = trade.Instrument()
        element.append(self._generate_element('NUMBER', instrument.Name()))
        element.append(self._generate_element('CURRENCY', instrument.Currency().Name()))
        element.append(self._generate_element('TYPE', DocumentGeneral.strip_dti_notation_from_funding_instype(
            trade.AdditionalInfo().Funding_Instype())))
        return element

    def _generate_summary_values_element(self, trade, statement_from_date, statement_to_date,
            statement_money_flows, account_balance_by_date):
        """
        Generate the SUMMARY XML element and sub-elements for a call
        deposit statement.
        """
        element = self._generate_element('SUMMARY_VALUES')
        # Opening balance.  This is the balance at the end of the
        # date before the statement period starts.
        opening_balance_date = self._get_previous_day(statement_from_date)
        opening_balance = account_balance_by_date[opening_balance_date]
        element.append(self._generate_summary_value_element('Opening Balance', opening_balance))
        # Deposits.
        deposits = self._get_summary_deposit_amount(statement_money_flows)
        element.append(self._generate_summary_value_element('Deposits', deposits))
        # Withdrawals.
        withdrawals = self._get_summary_withdrawal_amount(statement_money_flows)
        element.append(self._generate_summary_value_element('Withdrawals', withdrawals))
        # Interest settled.
        interest_reinvested = self._get_summary_interest_reinvested_amount(statement_money_flows)
        interest_settled = self._get_summary_interest_settled_amount(statement_from_date,
            statement_to_date, statement_money_flows, interest_reinvested)
        element.append(self._generate_summary_value_element('Interest Settled', interest_settled))
        # Interest reinvested.
        # Only show on statement if non-zero.
        if not DocumentGeneral.is_almost_zero(interest_reinvested):
            interest_reinvested_description = self._get_summary_interest_reinvested_description(trade)
            element.append(self._generate_summary_value_element(interest_reinvested_description,
                interest_reinvested))
        # Interest accrued (this is confusing terminology - it is
        # actually the closing interest balance).
        interest_accrued = self._get_summary_interest_accrued_amount(statement_to_date, statement_money_flows,
            account_balance_by_date)
        element.append(self._generate_summary_value_element('Interest Accrued',
            interest_accrued))
        # Closing balance.  This is the balance at the end of the
        # statement period to date.
        closing_balance = account_balance_by_date[statement_to_date]
        element.append(self._generate_summary_value_element('Closing Balance', closing_balance))
        return element

    @staticmethod
    def _get_summary_deposit_amount(statement_money_flows):
        """
        Get the summary deposit amount to display on the statement.

        This is the total of all deposit money flows into the call
        account with a pay date during the statement period.
        """
        total_deposit_amount = 0.0
        for statement_money_flow in statement_money_flows:
            if not CallStatementGeneral.is_fixed_amount_money_flow(statement_money_flow):
                continue
            money_flow_amount = DocumentGeneral.get_money_flow_amount(statement_money_flow)
            if money_flow_amount < 0:
                continue
            total_deposit_amount += money_flow_amount
        return total_deposit_amount

    @staticmethod
    def _get_summary_withdrawal_amount(statement_money_flows):
        """
        Get the summary withdrawal amount to display on the statement.

        This is the total of all withdrawal money flows from the call
        account with a pay date during the statement period.
        """
        total_withdrawal_amount = 0.0
        for statement_money_flow in statement_money_flows:
            if not CallStatementGeneral.is_fixed_amount_money_flow(statement_money_flow):
                continue
            money_flow_amount = DocumentGeneral.get_money_flow_amount(statement_money_flow)
            if money_flow_amount > 0:
                continue
            total_withdrawal_amount += money_flow_amount
        return total_withdrawal_amount

    def _get_summary_interest_settled_amount(self, statement_from_date, statement_to_date,
            statement_money_flows, interest_reinvested):
        """
        Get the summary interest settled amount to display on the
        statement.

        This is the total of all interest money flows with a pay date
        during the statement period minus the total of any interest
        reinvestment money flows with a pay date during the statement
        period.

        Please note that 'settled' on the statement refers only to
        interest that has been settled externally (not reinvested
        in the case of a deposit / not compounded in the case of a
        loan).
        """
        # Convert inclusive statement from date to exclusive
        # calculation start date.
        start_date = self._get_previous_day(statement_from_date)
        # Inclusive end date.
        end_date = statement_to_date
        return self._get_interest_settled_between_dates(start_date, end_date,
            statement_money_flows) + interest_reinvested

    @staticmethod
    def _get_summary_interest_reinvested_amount(statement_money_flows):
        """
        Get the summary interest reinvested amount to display on the
        statement.

        This is the total of all interest reinvestment money flows with
        a pay date during the statement period.
        """
        total_interest_reinvested_amount = 0.0
        for statement_money_flow in statement_money_flows:
            if not CallStatementGeneral.is_interest_reinvestment_money_flow(statement_money_flow):
                continue
            money_flow_amount = DocumentGeneral.get_money_flow_amount(statement_money_flow)
            total_interest_reinvested_amount += money_flow_amount
        return total_interest_reinvested_amount

    def _get_summary_interest_reinvested_description(self, trade):
        """
        Get the description to display for the summary interest
        reinvested line on the statement.
        """
        if self._is_loan(trade):
            return 'Interest Compounded'
        return 'Interest Reinvested'

    def _get_summary_interest_accrued_amount(self, statement_to_date, statement_money_flows,
            account_balance_by_date):
        """
        Get the summary interest amount to display on the statement.

        This is any interest that has been accrued but not yet settled
        externally or reinvested at the end of the statement end date.

        As such, this is comprised of two amounts:
            - Interest that has accrued for any interest money flows
              that have not finished accruing (money flow end date is
              after the statement period)
            - Interest that has accrued for any interest money flows
              that have finished accruing but have not yet been
              paid (settled externally or reinvested).  This scenario
              can occur when the end date of an interest money flow is
              before the pay date of the money flow.
        """
        previous_date = self._get_previous_day(statement_to_date)
        interest_money_flows = self._get_interest_money_flows_between_dates(previous_date,
            statement_to_date, statement_money_flows)
        interest_balance = self._get_interest_balance(statement_to_date, interest_money_flows,
            account_balance_by_date)
        return self._negate_amount(interest_balance)

    def _generate_summary_value_element(self, description, amount):
        """
        Generate a SUMMARY_VALUE XML element and sub-elements.
        """
        element = self._generate_element('SUMMARY_VALUE')
        element.append(self._generate_element('DESCRIPTION', description))
        amount = DocumentGeneral.format_amount(amount)
        element.append(self._generate_element('AMOUNT', str(amount)))
        return element

    def _generate_transaction_values_element(self, statement_from_date, statement_to_date,
            statement_money_flows, account_balance_by_date):
        """
        Generate the TRANSACTION_VALUES XML element and sub-elements
        for a call deposit statement.
        """
        element = self._generate_element('TRANSACTION_VALUES')
        transaction_money_flows = self._get_transaction_money_flows(statement_from_date,
            statement_to_date, statement_money_flows)
        transaction_money_flows = sorted(transaction_money_flows, key=lambda money_flow:
            (CallStatementGeneral.get_money_flow_value_date(money_flow), money_flow
            .SourceObject().CreateTime(), money_flow.SourceObject().Oid()))
        current_date = None
        current_balance = None
        for transaction_money_flow in transaction_money_flows:
            value_date = CallStatementGeneral.get_money_flow_value_date(transaction_money_flow)
            # Get opening account balance for each new value date.
            if current_date is None or current_date != value_date:
                current_date = value_date
                opening_balance_date = self._get_previous_day(value_date)
                current_balance = account_balance_by_date[opening_balance_date]
            cash_flow = transaction_money_flow.SourceObject()
            posting_date = acm.Time.DateFromTime(cash_flow.CreateTime())
            money_flow_amount = DocumentGeneral.get_money_flow_amount(transaction_money_flow)
            # Add any amounts affecting the intra-day account balance.
            if CallStatementGeneral.money_flow_affects_account_balance(transaction_money_flow):
                current_balance += money_flow_amount
            reference = cash_flow.Oid()
            description = self._get_transaction_money_flow_description(transaction_money_flow,
                money_flow_amount)
            element.append(self._generate_transaction_value_element(value_date, posting_date,
                reference, description, money_flow_amount, current_balance))
        return element

    def _get_transaction_money_flows(self, statement_from_date, statement_to_date,
            statement_money_flows):
        """
        Get any money flows that should appear as transactions on the
        statement.

        This is any statement money flow with a 'value date' failing
        within the statement period.  For most money flows, the value
        date of the money flow is the pay date.  The exception to
        this is in the case of back-dated fixed amount money flows
        (deposits and withdrawals) created by the custom deposit
        adjustment tool where the start date is used to represent the
        date on which the fixed-amount should have reflected as paid.
        """
        transaction_money_flows = list()
        available_reinvestment_money_flows = self._get_interest_reinvestment_money_flows(statement_money_flows)
        for statement_money_flow in statement_money_flows:
            value_date = CallStatementGeneral.get_money_flow_value_date(statement_money_flow)
            # Only show money_flows with value dates within the
            # statement period.
            if value_date > statement_to_date:
                continue
            if value_date < statement_from_date:
                continue
            if CallStatementGeneral.is_interest_money_flow(statement_money_flow):
                # Only show interest money flows that are no longer accruing.
                if CallStatementGeneral.is_interest_money_flow_still_accruing(statement_money_flow):
                    continue
                # Only show interest money flows that have not been reinvested.
                reinvestment_money_flow = self._get_matching_reinvestment_money_flow(
                    available_reinvestment_money_flows, statement_money_flow)
                if reinvestment_money_flow is not None:
                    available_reinvestment_money_flows.remove(reinvestment_money_flow)
                    continue
            transaction_money_flows.append(statement_money_flow)
        return transaction_money_flows

    @staticmethod
    def _get_interest_reinvestment_money_flows(statement_money_flows):
        """
        Get any interest reinvestment money flows.
        """
        money_flows = list()
        for statement_money_flow in statement_money_flows:
            if CallStatementGeneral.is_interest_reinvestment_money_flow(statement_money_flow):
                money_flows.append(statement_money_flow)
        return money_flows

    def _get_matching_reinvestment_money_flow(self, reinvestment_money_flows, interest_money_flow):
        """
        Get any interest reinvestment money flow that matches the
        specified interest money flow.

        An interest reinvestment money flow is viewed as matching a
        interest money flow if:
            - It has same pay date.
            - It has the same amount but with the opposite sign.
        """
        interest_amount = DocumentGeneral.get_money_flow_amount(interest_money_flow)
        for reinvestment_money_flow in reinvestment_money_flows:
            if reinvestment_money_flow.PayDate() != interest_money_flow.PayDate():
                continue
            reinvestment_amount = DocumentGeneral.get_money_flow_amount(reinvestment_money_flow)
            if self._amounts_are_equal_and_opposite(interest_amount, reinvestment_amount):
                return reinvestment_money_flow
        return None

    @staticmethod
    def _amounts_are_equal_and_opposite(amount1, amount2):
        """
        Determine if two amounts are equal but with the opposite
        signs.
        """
        if amount1 > 0 and amount2 > 0:
            return False
        if amount1 < 0 and amount2 < 0:
            return False
        sum_of_amounts = amount1 + amount2
        return DocumentGeneral.is_almost_zero(sum_of_amounts)

    def _get_transaction_money_flow_description(self, money_flow, money_flow_amount):
        """
        Get the description to display for a transaction money flow
        on the statement.
        """
        if CallStatementGeneral.is_fixed_amount_money_flow(money_flow):
            description = ''
            if money_flow.StartDate():
                description = 'Back-dated '
            if money_flow_amount > 0:
                return description + 'Deposit'
            else:
                return description + 'Withdrawal'
        elif CallStatementGeneral.is_call_fixed_rate_adjustable_money_flow(money_flow):
            return 'Interest Settled'
        elif CallStatementGeneral.is_fixed_rate_adjustable_money_flow(money_flow):
            return 'Back-dated Interest Settled'
        elif CallStatementGeneral.is_interest_reinvestment_money_flow(money_flow):
            if self._is_loan(money_flow.Trade()):
                return 'Interest Compounded'
            else:
                return 'Interest Reinvested'
        raise RuntimeError('Unsupported money_flow type specified.')

    def _generate_transaction_value_element(self, value_date, posting_date, reference,
            description, transaction_amount, account_balance):
        """
        Generate a TRANSACTION_VALUE XML element and sub-elements.
        """
        element = self._generate_element('TRANSACTION_VALUE')
        element.append(self._generate_element('VALUE_DATE', value_date))
        element.append(self._generate_element('POSTING_DATE', posting_date))
        element.append(self._generate_element('REFERENCE', str(reference)))
        element.append(self._generate_element('DESCRIPTION', description))
        transaction_amount = DocumentGeneral.format_amount(transaction_amount)
        element.append(self._generate_element('AMOUNT', str(transaction_amount)))
        account_balance = DocumentGeneral.format_amount(account_balance)
        element.append(self._generate_element('ACCOUNT_BALANCE', str(account_balance)))
        return element

    def _generate_daily_interest_values_element(self, statement_from_date,
            statement_to_date, statement_money_flows, account_balance_by_date):
        """
        Generate the DAILY_INTEREST_VALUES XML element and sub-elements
        for a call deposit statement.
        """
        element = self._generate_element('DAILY_INTEREST_VALUES')
        # If the statement is requested up until the current date, do
        # not show daily interest values until the balance has been held
        # overnight (i.e. max to date = yesterday).
        yesterday = self._get_previous_day(acm.Time.DateToday())
        interest_values_to_date = min(statement_to_date, yesterday)
        interest_money_flows = self._get_interest_money_flows_between_dates(statement_from_date,
            interest_values_to_date, statement_money_flows)
        current_date = statement_from_date
        next_date = self._get_next_day(current_date)
        while current_date <= interest_values_to_date:
            # Interest amount.
            # Please note that accrued interest is shown on the
            # statement offset by +1 day.
            interest_amount = self._get_interest_accrued_between_dates(current_date, next_date,
                interest_money_flows, account_balance_by_date)
            if not DocumentGeneral.is_almost_zero(interest_amount):
                # Only display daily interest for days on which interest
                # was accrued.
                # Interest rate.
                interest_rate = self._get_interest_rate_on_date(current_date, interest_money_flows)
                # Interest balance (unsettled interest).
                interest_balance = self._negate_amount(self._get_interest_balance(current_date,
                    interest_money_flows, account_balance_by_date))
                # Account balance.
                account_balance = account_balance_by_date[current_date]
                element.append(self._generate_daily_interest_value_element(current_date,
                    interest_rate, interest_amount, interest_balance, account_balance))
            current_date = next_date
            next_date = self._get_next_day(current_date)
        return element

    @staticmethod
    def _get_interest_money_flows_between_dates(start_date, end_date, statement_money_flows):
        """
        Get any interest money flows that are active between two
        dates.
        """
        interest_money_flows = list()
        for statement_money_flow in statement_money_flows:
            if not CallStatementGeneral.is_interest_money_flow(statement_money_flow):
                continue
            if statement_money_flow.StartDate() > end_date:
                continue
            if statement_money_flow.PayDate() <= start_date:
                continue
            interest_money_flows.append(statement_money_flow)
        return interest_money_flows

    def _get_interest_accrued_between_dates(self, start_date, end_date, interest_money_flows,
            account_balance_by_date):
        """
        Get the interest accrued for a call deposit trade between an
        exclusive profit and loss start date and an inclusive profit
        and loss end date.
        """
        interest = 0.0
        for interest_money_flow in interest_money_flows:
            # Note: we only need to consider non-back-date interest
            # money flows here as any back-dates are reflected in
            # the account balance and we are recalculating the
            # daily interest accrued.
            if not CallStatementGeneral.is_call_fixed_rate_adjustable_money_flow(interest_money_flow):
                continue
            interest += self._get_interest_accrued_between_dates_for_call_interest_money_flow(
                interest_money_flow, start_date, end_date, account_balance_by_date)
        return interest

    def _get_interest_accrued_between_dates_for_call_interest_money_flow(self,
            interest_money_flow, start_date, end_date, account_balance_by_date):
        """
        Calculate the interest accrued for a call fixed rate interest
        money flow between two dates.

        A custom calculation is used here for the following reasons:
            - Business view interest accrued offset by +1 day when
              compared to how it is reflected in Front Arena*.  This
              does not effect the actual interest paid and is purely
              a reporting issue. Unfortunately the interest accrued
              for the last night of an interest money flow is not
              visible in the accrued column as the full money flow
              amount moves into the settled column on the pay date.
              Provided that there are no overlapping interest money
              flows, this accrued amount can sometimes be obtained by
              using the interest column instead (as it subtracts
              interest settled from interest accrued).  Unfortunately
              this is not always the case with the call accounts
              within the system.
            - Some call account interest money flows have a pay date
              greater than the money flow end date.  Front Arena is
              reflecting such interest as moving into settled on the
              end date of the money flow rather than the pay date***.
              This is not how business would like interest to be
              reflected on the statement.

        *Front Arena only reflects interest** as accrued once a
        balance has been held overnight. This can be thought of as
        two different ways of viewing interest accrual: business
        would like to reflect the date (night) FOR WHICH interest
        was accrued vs Front Arena reflecting the date ON WHICH
        interest was accrued.

        **This appears configurable via the accounting parameter
        'Accrued Inclusion Method' however it did not behave as
        expected when tested (at least in version 2017.1.4). It
        appeared to adjust the view for interest on the calculation
        end date but not the calculation start date (causing one
        extra day of accrual to be reflected).

        ***This appears configurable via the account parameter
        'Settle Interest on Pay Day' but, at the time of writing,
        the parameter is set to reflect interest on end date not
        pay date.  Additionally, the behaviour has not been tested.
        """
        start_date = max(start_date, interest_money_flow.StartDate())
        end_date = min(end_date, interest_money_flow.EndDate())
        interest = 0.0
        day_count_factor = None
        current_date = start_date
        while current_date < end_date:
            next_date = self._get_next_day(current_date)
            nominal = account_balance_by_date[current_date]
            if not DocumentGeneral.is_almost_zero(nominal):
                interest_rate = self._get_interest_rate_for_money_flow_on_date(interest_money_flow, current_date)
                if day_count_factor is None:
                    day_count_factor = self._get_day_count_factor(interest_money_flow, current_date, next_date)
                interest += nominal / 100.0 * interest_rate * day_count_factor
            current_date = next_date
        return interest

    def _get_interest_rate_on_date(self, date, interest_money_flows):
        """
        Get the interest rate for a call account on a date.
        """
        interest_rate = 0.0
        interest_money_flows_for_date = self._get_call_interest_money_flows_for_date(date, interest_money_flows)
        for interest_money_flow in interest_money_flows_for_date:
            interest_rate += self._get_interest_rate_for_money_flow_on_date(interest_money_flow, date)
        return interest_rate

    @staticmethod
    def _get_call_interest_money_flows_for_date(date, interest_money_flows):
        """
        Get all interest money flows relevant for a specified date.
        """
        interest_money_flow_for_dates = list()
        for interest_money_flow in interest_money_flows:
            # Note: we only need to consider non-back-date interest
            # money flows here as back-date interest money flows are
            # meant to copy any interest rates from the normal call
            # fixed rate adjustable money flows.
            if not CallStatementGeneral.is_call_fixed_rate_adjustable_money_flow(interest_money_flow):
                continue
            if interest_money_flow.StartDate() > date:
                continue
            if interest_money_flow.EndDate() <= date:
                continue
            interest_money_flow_for_dates.append(interest_money_flow)
        if len(interest_money_flow_for_dates) == 0:
            raise ValueError("Unable to find interest money flow for date '{date}'".format(
                date=date
            ))
        return interest_money_flow_for_dates

    @staticmethod
    def _get_interest_rate_for_money_flow_on_date(interest_money_flow, date):
        """
        Get the interest rate for an money flow for a given date.
        """
        for reset in interest_money_flow.SourceObject().Resets():
            if reset.StartDate() > date:
                continue
            if reset.EndDate() <= date:
                continue
            return round(reset.FixingValue(), 3)
        raise ValueError("Unable to find reset fixing value for date '{date}'".format(
            date=date
        ))

    @staticmethod
    def _get_day_count_factor(interest_money_flow, start_date, end_date):
        """
        Get the day count factor to use when calculating interest for
        a specified interest money flow and date range.
        """
        leg = interest_money_flow.SourceObject().Leg()
        day_count_method = leg.DayCountMethod()
        # Only supporting these day count methods for now as all
        # currencies setup in Front Arena use Act/360 or Act/365,
        # with the exception of two.
        if day_count_method not in ['Act/360', 'Act/365']:
            raise ValueError("Unsupported day count method '{day_count_method}' specified.".format(
                day_count_method=day_count_method
            ))
        start_date = max(start_date, interest_money_flow.StartDate())
        end_date = min(end_date, interest_money_flow.EndDate())
        days_accrued = acm.Time.DateDifference(end_date, start_date)
        days_in_year = float(day_count_method[4:])
        return days_accrued / days_in_year

    def _get_interest_settled_between_dates(self, start_date, end_date, statement_money_flows):
        """
        Get the interest settled for a call deposit trade between an
        exclusive profit and loss start date and an inclusive profit
        and loss end date.

        A custom calculation is used here for the following reason:
            - Some call account interest money flows have a pay date
              greater than the money flow end date.  Front Arena is
              reflecting such interest as moving into settled on the
              end date of the money flow rather than the pay date*.
              This is not how business would like interest to be
              reflected on the statement.

        *This appears configurable via the account parameter
        'Settle Interest on Pay Day' but, at the time of writing,
        the parameter is set to reflect interest on end date not
        pay date.  Additionally, the behaviour has not been tested.
        """
        interest_settled = 0.0
        interest_money_flows = self._get_interest_money_flows_settling_between_dates(start_date, end_date,
            statement_money_flows)
        for interest_money_flow in interest_money_flows:
            interest_settled += DocumentGeneral.get_money_flow_amount(interest_money_flow)
        return interest_settled

    @staticmethod
    def _get_interest_money_flows_settling_between_dates(start_date, end_date,
            statement_money_flows):
        """
        Get any interest money flows paying between two dates.
        """
        interest_money_flows = list()
        for money_flow in statement_money_flows:
            if not CallStatementGeneral.is_interest_money_flow(money_flow):
                continue
            if money_flow.PayDate() > end_date:
                continue
            if money_flow.PayDate() <= start_date:
                continue
            if CallStatementGeneral.is_interest_money_flow_still_accruing(money_flow):
                continue
            interest_money_flows.append(money_flow)
        return interest_money_flows

    def _get_interest_balance(self, date, interest_money_flows, account_balance_by_date):
        """
        Get the interest balance on a date.

        This is any interest that has been earned but not yet settled
        externally or reinvested at the end of the date.

        As such, this is comprised of two amounts:
            - Interest that has accrued for any interest money flows
              that have not finished accruing (money flow end date is
              after the statement period)
            - Interest that has accrued for any interest money flows
              that have finished accruing but have not yet been
              paid (settled externally or reinvested).  This scenario
              can occur when the end date of an interest money flow is
              before the pay date of the money flow.
        """
        interest_balance = 0.0
        for interest_money_flow in interest_money_flows:
            if CallStatementGeneral.is_call_fixed_rate_adjustable_money_flow(interest_money_flow):
                interest_balance += self._get_interest_balance_for_call_fixed_rate_adjustable_money_flow(
                    interest_money_flow, date, account_balance_by_date)
            elif CallStatementGeneral.is_fixed_rate_adjustable_money_flow(interest_money_flow):
                interest_balance += self._get_interest_balance_for_fixed_rate_adjustable_money_flow(
                    interest_money_flow, date)
        return interest_balance

    def _get_interest_balance_for_call_fixed_rate_adjustable_money_flow(self, money_flow, date,
            account_balance_by_date):
        """
        Get the interest balance for a call fixed rate adjustable
        money flow on a date.
        """
        if money_flow.StartDate() > date:
            return 0.0
        if money_flow.PayDate() <= date:
            return 0.0
        if money_flow.EndDate() <= date:
            return DocumentGeneral.get_money_flow_amount(money_flow)
        else:
            next_date = self._get_next_day(date)
            return self._negate_amount(self
                ._get_interest_accrued_between_dates_for_call_interest_money_flow(
                money_flow, money_flow.StartDate(), next_date, account_balance_by_date))

    @staticmethod
    def _get_interest_balance_for_fixed_rate_adjustable_money_flow(money_flow, date):
        """
        Get the interest balance for a fixed rate adjustable money
        flow on a date.
        """
        if money_flow.StartDate() > date:
            return 0.0
        if money_flow.PayDate() <= date:
            return 0.0
        if money_flow.EndDate() <= date:
            return DocumentGeneral.get_money_flow_amount(money_flow)
        else:
            return 0.0

    def _generate_daily_interest_value_element(self, value_date, interest_rate, interest_amount,
            interest_balance, account_balance):
        """
        Generate a DAILY_INTEREST_VALUE XML element and sub-elements..
        """
        element = self._generate_element('DAILY_INTEREST_VALUE')
        element.append(self._generate_element('VALUE_DATE', value_date))
        interest_rate = DocumentGeneral.format_amount(interest_rate)
        element.append(self._generate_element('INTEREST_RATE', str(interest_rate)))
        interest_amount = DocumentGeneral.format_amount(interest_amount)
        element.append(self._generate_element('INTEREST_AMOUNT', str(interest_amount)))
        interest_balance = DocumentGeneral.format_amount(interest_balance)
        element.append(self._generate_element('INTEREST_BALANCE', str(interest_balance)))
        account_balance = DocumentGeneral.format_amount(account_balance)
        element.append(self._generate_element('ACCOUNT_BALANCE', str(account_balance)))
        return element

    @staticmethod
    def _get_account_balance(trade, date):
        """
        Get the account balance of a call deposit trade on a date.
        """
        account_balance = 0.0
        for money_flow in trade.MoneyFlows().AsArray():
            if not CallStatementGeneral.money_flow_affects_account_balance(money_flow):
                continue
            value_date = CallStatementGeneral.get_money_flow_value_date(money_flow)
            if value_date > date:
                continue
            money_flow_amount = DocumentGeneral.get_money_flow_amount(money_flow)
            account_balance += money_flow_amount
        return account_balance

    @staticmethod
    def _is_loan(trade):
        """
        Determine if a call deposit trade is a loan or not.
        """
        return trade.Quantity() < 0

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
