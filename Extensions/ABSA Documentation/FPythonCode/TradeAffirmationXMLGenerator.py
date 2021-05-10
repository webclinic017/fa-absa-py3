"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TradeAffirmationXMLGenerator
    
DESCRIPTION
    This module contains an object used for generating the XML content for a
    trade affirmation.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-10-25      FAOPS-226       Cuen Edwards            Letitia Carboni         Initial Implementation.
2019-02-06      FAOPS-345       Cuen Edwards            Letitia Carboni         Addition of settlement type to affirmations.
2019-03-01      FAOPS-385       Cuen Edwards            Letitia Carboni         Addition of support for FX Barrier Options.
2019-04-30      FAOPS-461       Cuen Edwards            Letitia Carboni         Addition of support for Swaps.
2019-05-10      FAOPS-497       Cuen Edwards            Letitia Carboni         Addition of support for FRAs.
2019-08-28      FAOPS-606       Cuen Edwards            Letitia Carboni         Add stub-handling to Swaps.
2020-05-18      FAOPS-511       Cuen Edwards            Letitia Carboni         Addition of support for Currency Swaps.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import math

import acm

import DocumentConfirmationGeneral
import DocumentGeneral
from DocumentXMLGenerator import DocumentXMLGenerator, GenerateDocumentXMLRequest
import FXOptionDocumentGeneral
import TradeAffirmationGeneral


_calculation_space_collection = acm.Calculations().CreateStandardCalculationsSpaceCollection()


class GenerateTradeAffirmationXMLRequest(GenerateDocumentXMLRequest):
    """
    An object embodying the request to generate the XML content for a
    trade affirmation document.
    """

    def __init__(self, confirmation):
        """
        Constructor.
        """
        super(GenerateTradeAffirmationXMLRequest, self).__init__(
            confirmation.Acquirer(),
            DocumentConfirmationGeneral.get_confirmation_acquirer_contact(confirmation),
            confirmation.Counterparty(),
            DocumentConfirmationGeneral.get_confirmation_counterparty_contact(confirmation)
        )
        self.confirmation = confirmation


class TradeAffirmationXMLGenerator(DocumentXMLGenerator):
    """
    An object responsible for generating the XML content for a
    trade affirmation document.
    """

    def generate_xml(self, generate_trade_affirmation_xml_request):
        """
        Generate the XML for a trade affirmation.
        """
        return super(TradeAffirmationXMLGenerator, self).generate_xml(
            generate_trade_affirmation_xml_request)

    def _generate_subject_element(self, generate_trade_affirmation_xml_request):
        """
        Generate the document SUBJECT XML element and sub-
        elements.
        """
        return self._generate_element('SUBJECT', TradeAffirmationGeneral.get_event_description(
            generate_trade_affirmation_xml_request.confirmation))

    def _generate_document_specific_element(self, generate_trade_affirmation_xml_request):
        """
        Generate the TRADE_AFFIRMATION XML element and sub-elements.
        """
        confirmation = generate_trade_affirmation_xml_request.confirmation
        element = self._generate_element('TRADE_AFFIRMATION')
        element.append(self._generate_element('TEXT', self._get_trade_affirmation_text(confirmation)))
        element.append(self._generate_element('TRADE_TYPE', TradeAffirmationGeneral
            .get_trade_type_description(confirmation)))
        element.append(self._generate_trade_specific_element(generate_trade_affirmation_xml_request))
        return element

    def _generate_trade_specific_element(self, generate_trade_affirmation_xml_request):
        """
        Generate the trade-specific element and sub-elements.
        """
        confirmation = generate_trade_affirmation_xml_request.confirmation
        instrument = confirmation.Trade().Instrument()
        if FXOptionDocumentGeneral.is_fx_option(instrument):
            return self._generate_fx_option_element(generate_trade_affirmation_xml_request)
        elif instrument.InsType() == 'Swap':
            return self._generate_swap_element(generate_trade_affirmation_xml_request)
        elif instrument.InsType() == 'FRA':
            return self._generate_fra_element(generate_trade_affirmation_xml_request)
        elif instrument.InsType() == 'CurrSwap':
            return self._generate_currency_swap_element(generate_trade_affirmation_xml_request)
        raise ValueError("Unsupported confirmation trade specified.")

    def _generate_fx_option_element(self, generate_trade_affirmation_xml_request):
        """
        Generate the FX_OPTION element and sub-elements.
        """
        confirmation = generate_trade_affirmation_xml_request.confirmation
        trade = confirmation.Trade()
        instrument = trade.Instrument()
        element = self._generate_element('FX_OPTION')
        element.append(self._generate_element('REFERENCE', str(trade.Oid())))
        element.append(self._generate_element('TRADE_DATE', acm.Time.AsDate(trade.TradeTime())))
        element.append(self._generate_element('BUY_SELL_INDICATOR', trade.BoughtAsString()))
        element.append(self._generate_element('BUYER', FXOptionDocumentGeneral.get_buyer_name(trade)))
        element.append(self._generate_element('SELLER', FXOptionDocumentGeneral.get_seller_name(trade)))
        call_currency = FXOptionDocumentGeneral.get_call_currency(instrument)
        put_currency = FXOptionDocumentGeneral.get_put_currency(instrument)
        element.append(self._generate_element('CURRENCY_PAIR', FXOptionDocumentGeneral.get_currency_pair_name(
            call_currency, put_currency)))
        element.append(self._generate_element('OPTION_STYLE', instrument.ExerciseType()))
        element.append(self._generate_element('CALL_CURRENCY', call_currency.Name()))
        element.append(self._generate_element('CALL_AMOUNT', str(FXOptionDocumentGeneral.get_call_amount(
            trade, instrument))))
        element.append(self._generate_element('PUT_CURRENCY', put_currency.Name()))
        element.append(self._generate_element('PUT_AMOUNT', str(FXOptionDocumentGeneral.get_put_amount(
            trade, instrument))))
        element.append(self._generate_element('STRIKE_CURRENCY', instrument.StrikeCurrency().Name()))
        element.append(self._generate_element('STRIKE_PRICE', str(instrument.StrikePrice())))
        if instrument.IsBarrier():
            element.extend(self._generate_fx_barrier_option_elements(instrument))
        element.append(self._generate_element('EXPIRATION_DATE', instrument.ExpiryDateOnly()))
        element.append(self._generate_element('SETTLEMENT_TYPE', FXOptionDocumentGeneral.get_settlement_type(
            instrument)))
        element.append(self._generate_element('SETTLEMENT_DATE', instrument.DeliveryDate()))
        element.append(self._generate_element('EXPIRATION_TIME', DocumentGeneral.get_fixing_source_name(
            instrument.FixingSource())))
        if not DocumentGeneral.is_almost_zero(trade.Premium()):
            element.append(self._generate_element('PREMIUM_CURRENCY', trade.Currency().Name()))
            element.append(self._generate_element('PREMIUM_AMOUNT', str(abs(round(trade.Premium(), 2)))))
            element.append(self._generate_element('PREMIUM_DATE', trade.ValueDay()))
        return element

    def _generate_fx_barrier_option_elements(self, instrument):
        """
        Generate any elements for FX barrier options.
        """
        elements = list()
        elements.append(self._generate_element('BARRIER_TYPE', str(instrument.Exotic().BarrierOptionType())))
        elements.append(self._generate_element('BARRIER', str(instrument.Barrier())))
        if instrument.IsDoubleBarrier():
            elements.append(self._generate_element('DOUBLE_BARRIER', str(instrument.Exotic().DoubleBarrier())))
        barrier_monitoring = instrument.Exotic().BarrierMonitoring()
        if barrier_monitoring is None or barrier_monitoring == 'None':
            raise ValueError('The barrier monitoring type must be specified for a barrier option.')
        elements.append(self._generate_element('BARRIER_MONITORING', barrier_monitoring))
        if barrier_monitoring == 'Discrete':
            barrier_date_events = FXOptionDocumentGeneral.get_barrier_date_exotic_events(instrument)
            if len(barrier_date_events) == 0:
                error_message = 'One or more barrier date exotic events must be specified '
                error_message += 'for a discretely monitored option.'
                raise ValueError(error_message)
            elements.append(self._generate_monitoring_dates_element(barrier_date_events))
        elif barrier_monitoring == 'Window':
            barrier_date_events = FXOptionDocumentGeneral.get_barrier_date_exotic_events(instrument)
            if len(barrier_date_events) != 1:
                error_message = 'One barrier date exotic event must be specified for a '
                error_message += 'window monitored option.'
                raise ValueError(error_message)
            elements.append(self._generate_monitoring_window_element(barrier_date_events[0]))
        elif instrument.Exotic().BarrierMonitoring() != 'Continuous':
            error_message = "Unsupported barrier monitoring type '{barrier_monitoring}' "
            error_message += "specified."
            raise ValueError(error_message.format(
                barrier_monitoring=barrier_monitoring
            ))
        rebate_percentage = instrument.Rebate() / instrument.StrikePrice() * 100.0
        if not DocumentGeneral.is_almost_zero(rebate_percentage):
            elements.append(self._generate_fx_barrier_option_rebate_element(
                instrument, rebate_percentage))
        return elements

    def _generate_monitoring_dates_element(self, barrier_date_events):
        """
        Generate the MONITORING_DATES element and sub-elements for
        an FX barrier option with discrete barrier monitoring.
        """
        element = self._generate_element('MONITORING_DATES')
        for barrier_date_event in barrier_date_events:
            element.append(self._generate_element('DATE', barrier_date_event.Date()))
        return element

    def _generate_monitoring_window_element(self, barrier_date_event):
        """
        Generate the MONITORING_WINDOW element and sub-elements for
        an FX barrier option with window barrier monitoring.
        """
        element = self._generate_element('MONITORING_WINDOW')
        element.append(self._generate_element(
            'FROM_DATE', barrier_date_event.Date()))
        element.append(self._generate_element(
            'TO_DATE', barrier_date_event.EndDate()))
        return element

    def _generate_fx_barrier_option_rebate_element(self, instrument, rebate_percentage):
        """
        Generate the REBATE element and sub-elements for an FX barrier
        option with a rebate.
        """
        rebate_type = 'Pay At Hit'
        if instrument.Exotic().BarrierRebateOnExpiry():
            rebate_type = 'Pay At Expiry'
        element = self._generate_element('REBATE')
        element.append(self._generate_element(
            'PERCENTAGE', str(rebate_percentage)))
        element.append(self._generate_element(
            'TYPE', rebate_type))
        return element

    def _generate_swap_element(self, generate_trade_affirmation_xml_request):
        """
        Generate the SWAP element and sub-elements.
        """
        confirmation = generate_trade_affirmation_xml_request.confirmation
        trade = confirmation.Trade()
        instrument = trade.Instrument()
        element = self._generate_element('SWAP')
        element.append(self._generate_element('REFERENCE', str(trade.Oid())))
        element.append(self._generate_element('TRADE_DATE', acm.Time.AsDate(trade.TradeTime())))
        element.append(self._generate_element('CURRENCY', instrument.Currency().Name()))
        element.append(self._generate_element('NOMINAL_AMOUNT', str(abs(round(trade.Nominal(), 2)))))
        element.append(self._generate_element('START_DATE', instrument.StartDate()))
        element.append(self._generate_element('END_DATE', instrument.EndDate()))
        element.append(self._generate_swap_legs_element(trade))
        return element

    def _generate_swap_legs_element(self, trade):
        """
        Generate the LEGS element and sub-elements for a swap.
        """
        element = self._generate_element('LEGS')
        for leg in trade.Instrument().Legs():
            element.append(self._generate_swap_leg_element(trade, leg))
        return element

    def _generate_swap_leg_element(self, trade, leg):
        """
        Generate the LEG element and sub-elements for a swap.
        """
        leg_decorator = acm.FBusinessLogicDecorator.WrapObject(leg)
        element = self._generate_element('LEG')
        element.append(self._generate_element('PAYER', DocumentGeneral.get_leg_payer_name(trade, leg)))
        element.append(self._generate_element('RATE_TYPE', leg.LegType()))
        if leg.IsFixedLeg():
            element.append(self._generate_element('FIXED_RATE', str(leg.FixedRate())))
        else:
            element.append(self._generate_element('RATE_REFERENCE', DocumentGeneral.get_float_rate_reference_name(
                leg.FloatRateReference())))
            initial_rate = leg_decorator.InitialRate()
            if initial_rate is not None and not math.isnan(initial_rate):
                element.append(self._generate_element('REFERENCE_RATE', str(initial_rate)))
            element.append(self._generate_element('SPREAD', str(leg.Spread())))
            element.append(self._generate_element('FIXING_OFFSET', str(leg.ResetDayOffset())))
            element.append(self._generate_element('RESET_CALENDARS', DocumentGeneral.get_leg_reset_calendars(leg)))
            element.append(self._generate_element('STUB_HANDLING', leg.StubHandling()))
        element.append(self._generate_element('ROLLING_PERIOD', DocumentGeneral.get_leg_rolling_period(leg)))
        element.append(self._generate_element('PAYMENT_START_DATE', DocumentGeneral
            .get_leg_payment_start_date(leg)))
        element.append(self._generate_element('DAY_COUNT_METHOD', leg.DayCountMethod()))
        element.append(self._generate_element('PAY_DAY_METHOD', leg.PayDayMethod()))
        element.append(self._generate_element('PAYMENT_CALENDARS', DocumentGeneral.get_leg_payment_calendars(leg)))
        return element

    def _generate_fra_element(self, generate_trade_affirmation_xml_request):
        """
        Generate the FRA element and sub-elements.
        """
        confirmation = generate_trade_affirmation_xml_request.confirmation
        trade = confirmation.Trade()
        instrument = trade.Instrument()
        leg = instrument.MainLeg()
        element = self._generate_element('FRA')
        element.append(self._generate_element('REFERENCE', str(trade.Oid())))
        element.append(self._generate_element('TRADE_DATE', acm.Time.AsDate(trade.TradeTime())))
        element.append(self._generate_element('BUY_SELL_INDICATOR', trade.BoughtAsString()))
        element.append(self._generate_element('BUYER', DocumentGeneral.get_trade_buyer_name(trade)))
        element.append(self._generate_element('SELLER', DocumentGeneral.get_trade_seller_name(trade)))
        element.append(self._generate_element('CURRENCY', instrument.Currency().Name()))
        element.append(self._generate_element('NOMINAL_AMOUNT', str(abs(round(trade.Nominal(), 2)))))
        element.append(self._generate_element('START_DATE', instrument.StartDate()))
        element.append(self._generate_element('END_DATE', instrument.EndDate()))
        element.append(self._generate_element('SETTLEMENT_DATE', instrument.StartDate()))
        element.append(self._generate_element('DAY_COUNT_METHOD', leg.DayCountMethod()))
        element.append(self._generate_element('PAY_DAY_METHOD', leg.PayDayMethod()))
        element.append(self._generate_element('PAYMENT_CALENDARS', DocumentGeneral.get_leg_payment_calendars(leg)))
        element.append(self._generate_element('FIXED_RATE', str(leg.FixedRate())))
        element.append(self._generate_element('RATE_REFERENCE', DocumentGeneral.get_float_rate_reference_name(
            leg.FloatRateReference())))
        element.append(self._generate_element('FIXING_OFFSET', str(leg.ResetDayOffset())))
        element.append(self._generate_element('RESET_CALENDARS', DocumentGeneral.get_leg_reset_calendars(leg)))
        return element

    def _generate_currency_swap_element(self, generate_trade_affirmation_xml_request):
        """
        Generate the CURRENCY_SWAP element and sub-elements.
        """
        confirmation = generate_trade_affirmation_xml_request.confirmation
        trade = confirmation.Trade()
        instrument = trade.Instrument()
        element = self._generate_element('CURRENCY_SWAP')
        element.append(self._generate_element('REFERENCE', str(trade.Oid())))
        element.append(self._generate_element('TRADE_DATE', acm.Time.AsDate(trade.TradeTime())))
        element.append(self._generate_element('START_DATE', instrument.StartDate()))
        element.append(self._generate_element('END_DATE', instrument.EndDate()))
        element.append(self._generate_currency_swap_legs_element(trade))
        return element

    def _generate_currency_swap_legs_element(self, trade):
        """
        Generate the LEGS element and sub-elements for a currency swap.
        """
        element = self._generate_element('LEGS')
        for leg in trade.Instrument().Legs():
            element.append(self._generate_currency_swap_leg_element(trade, leg))
        return element

    def _generate_currency_swap_leg_element(self, trade, leg):
        """
        Generate the LEG element and sub-elements for a currency swap.
        """
        leg_decorator = acm.FBusinessLogicDecorator.WrapObject(leg)
        element = self._generate_element('LEG')
        element.append(self._generate_element('PAYER', DocumentGeneral.get_leg_payer_name(trade, leg)))
        element.append(self._generate_element('CURRENCY', leg.Currency().Name()))
        nominal = leg.Calculation().Nominal(_calculation_space_collection, trade)
        element.append(self._generate_element('NOMINAL_AMOUNT', str(abs(round(nominal.Number(), 2)))))
        element.append(self._generate_element('RATE_TYPE', leg.LegType()))
        if leg.IsFixedLeg():
            element.append(self._generate_element('FIXED_RATE', str(leg.FixedRate())))
        else:
            element.append(self._generate_element('RATE_REFERENCE', DocumentGeneral.get_float_rate_reference_name(
                leg.FloatRateReference())))
            initial_rate = leg_decorator.InitialRate()
            if initial_rate is not None and not math.isnan(initial_rate):
                element.append(self._generate_element('REFERENCE_RATE', str(initial_rate)))
            element.append(self._generate_element('SPREAD', str(leg.Spread())))
            element.append(self._generate_element('FIXING_OFFSET', str(leg.ResetDayOffset())))
            element.append(self._generate_element('RESET_CALENDARS', DocumentGeneral.get_leg_reset_calendars(leg)))
            element.append(self._generate_element('STUB_HANDLING', leg.StubHandling()))
        element.append(self._generate_element('ROLLING_PERIOD', DocumentGeneral.get_leg_rolling_period(leg)))
        element.append(self._generate_element('PAYMENT_START_DATE', DocumentGeneral.get_leg_payment_start_date(leg)))
        element.append(self._generate_element('DAY_COUNT_METHOD', leg.DayCountMethod()))
        element.append(self._generate_element('PAY_DAY_METHOD', leg.PayDayMethod()))
        element.append(self._generate_element('PAYMENT_CALENDARS', DocumentGeneral.get_leg_payment_calendars(leg)))
        initial_exchange_cash_flow = self._get_currency_swap_initial_exchange_cashflow(leg)
        if initial_exchange_cash_flow is not None:
            initial_exchange_amount = round(initial_exchange_cash_flow.Calculation().Projected(
                _calculation_space_collection, trade), 2)
            element.append(self._generate_element('INITIAL_EXCHANGE_AMOUNT', str(initial_exchange_amount)))
            element.append(self._generate_element('INITIAL_EXCHANGE_DATE', initial_exchange_cash_flow.PayDate()))
        final_exchange_cash_flow = self._get_currency_swap_final_exchange_cashflow(leg)
        if final_exchange_cash_flow is not None:
            final_exchange_amount = round(final_exchange_cash_flow.Calculation().Projected(
                _calculation_space_collection, trade), 2)
            element.append(self._generate_element('FINAL_EXCHANGE_AMOUNT', str(final_exchange_amount)))
            element.append(self._generate_element('FINAL_EXCHANGE_DATE', final_exchange_cash_flow.PayDate()))
        return element

    @staticmethod
    def _get_trade_affirmation_text(confirmation):
        """
        Get the text to display on the trade affirmation.
        """
        text = None
        if confirmation.Type() == 'Cancellation':
            text = 'We hereby confirm that the {trade_type} transaction below has been cancelled and no '
            text += 'longer requires your affirmation:'
        elif confirmation.Type() == 'Amendment':
            text = 'We hereby request that you affirm the terms of the amended {trade_type} transaction below:'
        else:
            text = 'We hereby request that you affirm the terms of the {trade_type} transaction below:'
        text = text.format(trade_type=TradeAffirmationGeneral.get_trade_type_description(confirmation))
        return text

    @staticmethod
    def _get_currency_swap_initial_exchange_cashflow(leg):
        """
        Get the initial exchange cash flow for a currency swap leg.
        """
        cash_flows = leg.CashFlows().AsArray().SortByProperty('PayDate')
        for cash_flow in cash_flows:
            if cash_flow.CashFlowType() == 'Fixed Amount':
                return cash_flow
        return None

    @staticmethod
    def _get_currency_swap_final_exchange_cashflow(leg):
        """
        Get the final exchange cash flow for a currency swap leg.
        """
        cash_flows = leg.CashFlows().AsArray().SortByProperty('PayDate', ascending=False)
        for cash_flow in cash_flows:
            if cash_flow.CashFlowType() == 'Fixed Amount':
                return cash_flow
        return None
