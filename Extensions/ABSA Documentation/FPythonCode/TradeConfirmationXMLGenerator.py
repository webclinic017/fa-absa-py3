"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TradeConfirmationXMLGenerator

DESCRIPTION
    This module contains an object used for generating the XML content for a
    trade confirmation.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-06-14      FAOPS-439       Cuen Edwards            Letitia Carboni         Initial Implementation.
                                Tawanda Mukhalela
2020-02-07      FAOPS-724       Cuen Edwards            Letitia Carboni         Addition of support for option type (put/call).
2020-02-14      FAOPS-732       Cuen Edwards            Letitia Carboni         Addition of support for related trade references.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

import DocumentGeneral
import DocumentConfirmationGeneral
from DocumentXMLGenerator import DocumentXMLGenerator, GenerateDocumentXMLRequest
import FXOptionDocumentGeneral
import TradeConfirmationGeneral


class GenerateTradeConfirmationXMLRequest(GenerateDocumentXMLRequest):
    """
    An object embodying the request to generate the XML content for a
    trade confirmation document.
    """

    def __init__(self, confirmation):
        """
        Constructor.
        """
        super(GenerateTradeConfirmationXMLRequest, self).__init__(
            confirmation.Acquirer(),
            DocumentConfirmationGeneral.get_confirmation_acquirer_contact(confirmation),
            confirmation.Counterparty(),
            DocumentConfirmationGeneral.get_confirmation_counterparty_contact(confirmation)
        )
        self.confirmation = confirmation


class TradeConfirmationXMLGenerator(DocumentXMLGenerator):
    """
    An object responsible for generating the XML content for a
    trade confirmation document.
    """

    def generate_xml(self, generate_trade_confirmation_xml_request):
        """
        Generate the XML for a trade affirmation.
        """
        return super(TradeConfirmationXMLGenerator, self).generate_xml(
            generate_trade_confirmation_xml_request)

    def _generate_subject_element(self, generate_trade_confirmation_xml_request):
        """
        Generate the document SUBJECT XML element and sub-
        elements.
        """
        return self._generate_element('SUBJECT', TradeConfirmationGeneral.get_event_description(
            generate_trade_confirmation_xml_request.confirmation))

    def _generate_document_specific_element(self, generate_trade_confirmation_xml_request):
        """
        Generate the TRADE_CONFIRMATION XML element and sub-elements.
        """
        confirmation = generate_trade_confirmation_xml_request.confirmation
        element = self._generate_element('TRADE_CONFIRMATION')
        element.append(self._generate_element('TRADE_TYPE', TradeConfirmationGeneral
            .get_trade_type_description(confirmation)))
        element.append(self._generate_element('REFERENCE', str(confirmation.Trade().Oid())))
        element.append(self._generate_element('BANK_NAME', str(DocumentGeneral.get_default_bank_name())))
        element.append(self._generate_element('BANK_ABBREVIATED_NAME', str(DocumentGeneral
            .get_default_bank_abbreviated_name())))
        element.append(self._generate_element('COUNTERPARTY_NAME', DocumentGeneral.get_party_full_name(
            confirmation.Counterparty())))
        isda_agreement = TradeConfirmationGeneral.get_party_isda_agreement(confirmation.Counterparty())
        if isda_agreement is None:
            raise ValueError("No ISDA agreement found for counterparty '{counterparty_name}'.".format(
                counterparty_name=confirmation.Counterparty().Name()
            ))
        element.append(self._generate_element('ISDA_AGREEMENT_DATE', isda_agreement.Dated()))
        first_bank_signatory = TradeConfirmationGeneral.get_first_bank_signatory()
        if not first_bank_signatory:
            raise ValueError("No first bank signatory found.")
        element.append(self._generate_element('BANK_SIGNATORY1_NAME', first_bank_signatory))
        second_bank_signatory = TradeConfirmationGeneral.get_second_bank_signatory()
        if not first_bank_signatory:
            raise ValueError("No second bank signatory found.")
        element.append(self._generate_element('BANK_SIGNATORY2_NAME', second_bank_signatory))
        element.append(self._generate_trade_specific_element(generate_trade_confirmation_xml_request))
        return element

    def _generate_trade_specific_element(self, generate_trade_affirmation_xml_request):
        """
        Generate the trade-specific element and sub-elements.
        """
        confirmation = generate_trade_affirmation_xml_request.confirmation
        if FXOptionDocumentGeneral.is_fx_option_structure_trade(confirmation.Trade()):
            return self._generate_fx_option_structure_element(generate_trade_affirmation_xml_request)
        elif FXOptionDocumentGeneral.is_fx_option_standalone_trade(confirmation.Trade()):
            return self._generate_fx_option_standalone_trade_element(generate_trade_affirmation_xml_request)
        else:
            raise ValueError("Unsupported confirmation trade specified.")

    def _generate_fx_option_structure_element(self, generate_trade_confirmation_xml_request):
        """
        Generate the trade-specific element and sub-elements for an
        FX Option structure.
        """
        element = self._generate_element('FX_OPTION_STRUCTURE')
        trade = generate_trade_confirmation_xml_request.confirmation.Trade()
        for fx_option_trade in FXOptionDocumentGeneral.get_supported_fx_option_trades(trade):
            element.append(self._generate_fx_option_element(fx_option_trade))
        return element

    def _generate_fx_option_standalone_trade_element(self, generate_trade_confirmation_xml_request):
        """
        Generate the trade-specific element and sub-elements for a
        stand-alone FX Option trade.
        """
        confirmation = generate_trade_confirmation_xml_request.confirmation
        return self._generate_fx_option_element(confirmation.Trade())

    def _generate_fx_option_element(self, trade):
        """
        FIXME
        Generate an FX_OPTION element and sub-elements.
        """
        instrument = trade.Instrument()
        element = self._generate_element('FX_OPTION')
        element.append(self._generate_element('REFERENCE', str(trade.Oid())))
        product_type = FXOptionDocumentGeneral.get_product_type(instrument)
        if product_type in TradeConfirmationGeneral.PRODUCT_TYPES_WITH_RELATED_REFERENCES:
            element.append(self._generate_element('RELATED_REFERENCE', trade.Text2().strip()))
        element.append(self._generate_element('TRADE_DATE', acm.Time.AsDate(trade.TradeTime())))
        element.append(self._generate_element('BUY_SELL_INDICATOR', trade.BoughtAsString()))
        element.append(self._generate_element('BUYER', FXOptionDocumentGeneral.get_buyer_name(trade)))
        element.append(self._generate_element('SELLER', FXOptionDocumentGeneral.get_seller_name(trade)))
        call_currency = FXOptionDocumentGeneral.get_call_currency(instrument)
        put_currency = FXOptionDocumentGeneral.get_put_currency(instrument)
        currency_pair = FXOptionDocumentGeneral.get_currency_pair_name(call_currency, put_currency)
        element.append(self._generate_element('CURRENCY_PAIR', currency_pair))
        element.append(self._generate_element('OPTION_TYPE', instrument.OptionType()))
        element.append(self._generate_element('OPTION_STYLE', instrument.ExerciseType()))
        element.append(self._generate_element('CALL_CURRENCY', call_currency.Name()))
        element.append(self._generate_element('CALL_AMOUNT', str(FXOptionDocumentGeneral.get_call_amount(
            trade, instrument))))
        element.append(self._generate_element('PUT_CURRENCY', put_currency.Name()))
        element.append(self._generate_element('PUT_AMOUNT', str(FXOptionDocumentGeneral.get_put_amount(
            trade, instrument))))
        element.append(self._generate_element('STRIKE_CURRENCY', instrument.StrikeCurrency().Name()))
        strike_price = instrument.StrikePrice()
        non_zar_strike_description = str(currency_pair.split('/')[0]) + ' ' + str(strike_price) + ' / 1.00 ' \
                                     + str(currency_pair.split('/')[1])
        zar_strike_description = str(currency_pair.split('/')[1]) + ' ' + str(strike_price) + ' / 1.00 ' + \
                                 str(currency_pair.split('/')[0])
        strike_price_description = zar_strike_description if 'ZAR' in currency_pair else non_zar_strike_description
        element.append(self._generate_element('STRIKE_PRICE', strike_price_description))
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
        element.append(self._generate_element('BUSINESS_DAYS', FXOptionDocumentGeneral.get_business_days(
            instrument)))
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
        monitoring_dates_element = self._generate_element('MONITORING_DATES')
        for barrier_date_event in barrier_date_events:
            monitoring_dates_element.append(self._generate_element('DATE', barrier_date_event.Date()))
        return monitoring_dates_element

    def _generate_monitoring_window_element(self, barrier_date_event):
        """
        Generate the MONITORING_WINDOW element and sub-elements for
        an FX barrier option with window barrier monitoring.
        """
        monitoring_window_element = self._generate_element('MONITORING_WINDOW')
        monitoring_window_element.append(self._generate_element(
            'FROM_DATE', barrier_date_event.Date()))
        monitoring_window_element.append(self._generate_element(
            'TO_DATE', barrier_date_event.EndDate()))
        return monitoring_window_element

    def _generate_fx_barrier_option_rebate_element(self, instrument, rebate_percentage):
        """
        Generate the REBATE element and sub-elements for an FX barrier
        option with a rebate.
        """
        rebate_type = 'Pay At Hit'
        if instrument.Exotic().BarrierRebateOnExpiry():
            rebate_type = 'Pay At Expiry'
        rebate_element = self._generate_element('REBATE')
        rebate_element.append(self._generate_element(
            'PERCENTAGE', str(rebate_percentage)))
        rebate_element.append(self._generate_element(
            'TYPE', rebate_type))
        return rebate_element
