"""------------------------------------------------------------------------------------------------------------------
MODULE
    ASUSNewTradeConfirmationXMLGenerator

DESCRIPTION
    This module contains an object used to generate the XML for ASUS New Trade Confirmation that
    will be sent to Adaptiv to form PDF's to be mailed to clients

---------------------------------------------------------------------------------------------------------------------
HISTORY
=====================================================================================================================
Date            Change no       Developer               Requester               Description
---------------------------------------------------------------------------------------------------------------------
2020-02-17      FAOPS-708       Tawanda Mukhalela       Ndivhuwo Mashishimise   ASUS New Trade Confirmations
2020-04-29      FAOPS-748       Tawanda Mukhalela       Ndivhuwo Mashishimise   ASUS DMA New Trade Confirmations
2020-03-22      FAOPS-991       Metse Moshobane         Ndivhuwo Mashishimise   Calculation of Local Accrued interest
---------------------------------------------------------------------------------------------------------------------
"""

import types

import acm

import ASUSNewTradeConfirmationGeneral
from at_logging import getLogger
import DocumentGeneral
from DocumentXMLGenerator import DocumentXMLGenerator, GenerateDocumentXMLRequest


LOGGER = getLogger(__name__)


class GenerateASUSNewTradeConfirmationXMLRequest(GenerateDocumentXMLRequest):
    """
    An object embodying the request to generate the XML content for
    ASUS New Trade Confirmation.
    """

    def __init__(self, from_party, from_party_contact, to_party, to_party_contact, confirmation):

        super(GenerateASUSNewTradeConfirmationXMLRequest, self).__init__(from_party, from_party_contact,
                                                                         to_party, to_party_contact)
        self.trade = confirmation.Trade()
        self.confirmation = confirmation


class ASUSNewTradeConfirmationXMLGenerator(DocumentXMLGenerator):

    def __init__(self):
        self.calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')

    def generate_xml(self, generate_document_xml_request):
        """
        Generates the XML Document
        """
        return super(ASUSNewTradeConfirmationXMLGenerator, self).generate_xml(generate_document_xml_request)

    def _generate_from_element(self, from_party, from_party_contact):
        """
        Overrides the From elements to cater for the US Documents
        """
        element = self._generate_element('FROM')
        element.append(self._generate_element('NAME', DocumentGeneral
                                              .get_default_us_document_from_name().lower().title()))
        element.append(self._generate_address_element(from_party_contact))
        element.append(self._generate_element('TEL', from_party_contact.Telephone()))
        element.append(self._generate_element('DATE', str(
            ASUSNewTradeConfirmationGeneral.format_string_to_asus_format(acm.Time.DateToday(), "%B %d, %Y"))))

        return element

    def _generate_to_element(self, to_party, to_party_contact):
        """
        Generate the document TO XML element and sub-elements.
        """
        element = self._generate_element('TO')
        element.append(self._generate_element('NAME', DocumentGeneral.get_party_full_name(to_party).lower().title()))
        # Add the value of the party ShortCode field if present.
        # This field is generally used to hold any related fund
        # code associated with a party.
        short_code = DocumentGeneral.get_party_short_code(to_party)
        if short_code is not None:
            element.append(self._generate_element('SHORTCODE', short_code))
        element.append(self._generate_address_element(to_party_contact))
        return element

    def _generate_address_element(self, party_contact):
        """
        Overrides the address element method to provide a
        title case representation
        """
        element = self._generate_element('ADDRESS')
        element.append(self._generate_element('LINE1', str(party_contact.Address())))
        element.append(self._generate_element('LINE2', str(party_contact.Address2())))
        element.append(self._generate_element('CITY', str(party_contact.City())))

        return element

    def _generate_subject_element(self, xml_request):
        """
        Generate the document SUBJECT XML element and sub-
        elements.
        """
        confirmation = xml_request.confirmation
        element = self._generate_element('SUBJECT', 'NEW TRADE CONFIRMATION')
        if confirmation.Type() == 'Amendment':
            element = self._generate_element('SUBJECT', 'TRADE AMENDMENT CONFIRMATION')
        elif confirmation.EventType() == 'Cancellation':
            element = self._generate_element('SUBJECT', 'TRADE CANCELLATION CONFIRMATION')

        return element

    def _generate_document_specific_element(self, xml_request):
        """
        Get Document Specific element TRADE_CONFIRMATION
        """
        if xml_request.trade.AdditionalInfo().XtpTradeType() in ['OBP_BROKER_NOTE', 'OBP_BLOCK_TRADE']:
            element = self._get_equity_trade_elements(xml_request)
        else:
            element = self._get_trade_elements(xml_request)

        return element

    def _get_trade_elements(self, xml_request):
        """
        Generates the elements for the Bond Block Trade
        """
        trade = xml_request.trade
        buy_or_sell = 'Sale' if trade.Bought() else 'Purchase'
        deal_reference = '{:0,.0f}'.format(trade.Oid())
        dealer_code = trade.Trader().Name()
        instrument = trade.Instrument()
        security_description = instrument.Name()
        isin = instrument.Isin()
        issue_date = ASUSNewTradeConfirmationGeneral.format_string_to_asus_format(instrument.StartDate())
        maturity_date = ASUSNewTradeConfirmationGeneral.format_string_to_asus_format(instrument.ExpiryDate())
        coupon = '{:0,.4f}'.format(instrument.Legs()[0].FixedRate())
        settlement_date = ASUSNewTradeConfirmationGeneral.format_string_to_asus_format(trade.ValueDay())
        trade_date = ASUSNewTradeConfirmationGeneral.format_string_to_asus_format(trade.TradeTime())
        yield_information = self.calc_space.CreateCalculation(trade, 'Trade Yield').Value().Number() * 100
        if not yield_information:
            raise ValueError('Could not get Yield Information')

        usd_currency_instrument = acm.FCurrency['USD']
        spot_price = ASUSNewTradeConfirmationGeneral.get_current_usd_pot_price(usd_currency_instrument,
                                                                               instrument.Currency()
                                                                               )
        principal_amount = trade.Nominal()
        local_currency = instrument.Currency().Name()
        usd_principal_amount = principal_amount / spot_price
        consideration = trade.Premium()
        usd_consideration = consideration / spot_price
        clean_price = float(acm.GetCalculatedValue(trade, acm.GetDefaultContext(), 'cleanPrice').Value()) / 100
        dirty_price = self._get_dirty_price(trade)
        us_clean_price = clean_price / spot_price
        if not clean_price:
            raise ValueError('Could not calculate the Clean price')

        local_interest = self._get_accrued_interest(trade, clean_price, dirty_price)
        if not local_interest:
            raise ValueError('Could not calculate Accrued Interest for Trade')

        us_interest = local_interest / spot_price
        commission = 'n/a'
        if instrument.InsType() == 'Bond':
            commission = 'n/a'
        delivery_type = 'DVP' if buy_or_sell == 'Sale' else 'RVP'
        disclosures = ''
        external_id1 = instrument.ExternalId1()
        external_id2 = instrument.ExternalId2()
        if not self.check_us_security_registration(external_id1, external_id2):
            disclosures += 'D1 '
        if instrument.Callable():
            disclosures += 'D2 '
        if 'absa' in instrument.Issuer().Name().lower():
            disclosures += 'D3'
        if disclosures == '':
            disclosures = 'n/a'

        accrued_days = '(' + str(acm.FBusinessLogicDecorator.WrapObject(trade).AccruedDays()) + ' days)'
        loacal_interest_with_days = ASUSNewTradeConfirmationGeneral.formated_display_value(local_currency,
                                                                                           '{:0,.2f}',
                                                                                           local_interest) + \
                                    str(' ' + accrued_days)

        us_interest_with_days = ASUSNewTradeConfirmationGeneral.formated_display_value('USD',
                                                                                       '{:0,.2f}',
                                                                                       us_interest) + \
                                    str(' ' + accrued_days)

        element = self._generate_element('TRADE_CONFIRMATION')

        element.append(self._generate_element('PURCHASE_OR_SALE', str(buy_or_sell)))
        element.append(self._generate_element('DEAL_REFERENCE', str(deal_reference)))
        element.append(self._generate_element('DEALER_CODE', str(dealer_code)))
        element.append(self._generate_element('SECURITY_DESCRIPTION', str(security_description)))
        element.append(self._generate_element('ISIN', str(isin)))
        element.append(self._generate_element('ISSUE_DATE', str(issue_date)))
        element.append(self._generate_element('MATURITY_DATE', str(maturity_date)))
        element.append(self._generate_element('COUPON', str(coupon)))
        element.append(self._generate_element('SETTLEMENT_DATE', str(settlement_date)))
        element.append(self._generate_element('TRADE_DATE', str(trade_date)))
        element.append(self._generate_element('YIELD_INFORMATION', str('{:0,.4f}'.format(yield_information))))
        element.append(
            self._generate_element('LOCAL_PRINCIPAL_AMOUNT',
                                   str(ASUSNewTradeConfirmationGeneral.formated_display_value(local_currency,
                                                                                              '{:0,.2f}',
                                                                                              principal_amount))))
        element.append(
            self._generate_element('USD_PRINCIPAL_AMOUNT',
                                   str(ASUSNewTradeConfirmationGeneral.formated_display_value('USD',
                                                                                              '{:0,.2f}',
                                                                                              usd_principal_amount))))
        element.append(
            self._generate_element('LOCAL_CLEAN_PRICE',
                                   str(ASUSNewTradeConfirmationGeneral.formated_display_value(local_currency,
                                                                                              '{:0,.4f}',
                                                                                              clean_price))))
        element.append(
            self._generate_element('US_CLEAN_PRICE',
                                   str(ASUSNewTradeConfirmationGeneral.formated_display_value('USD',
                                                                                              '{:0,.4f}',
                                                                                              us_clean_price))))
        element.append(
            self._generate_element('LOCAL_CONSIDERATION',
                                   str(ASUSNewTradeConfirmationGeneral.formated_display_value(local_currency,
                                                                                              '{:0,.2f}',
                                                                                              consideration))))
        element.append(
            self._generate_element('US_CONSIDERATION',
                                   str(ASUSNewTradeConfirmationGeneral.formated_display_value('USD',
                                                                                              '{:0,.2f}',
                                                                                              usd_consideration))))
        element.append(self._generate_element('LOCAL_ACCRUED_INTEREST', str(loacal_interest_with_days)))
        element.append(self._generate_element('US_ACCRUED_INTEREST', str(us_interest_with_days)))
        element.append(self._generate_element('COMMISSION', str(commission)))
        element.append(self._generate_element('US_COMMISSION', str(commission)))
        element.append(self._generate_element('SETTLEMENT_TERMS', str(delivery_type)))
        element.append(self._generate_element('ADDITIONAL_DISCLOSURES', str(disclosures)))
        element.append(self._generate_element('TRADE_TYPE', str('NORMAL_BONDS')))

        return element

    def _get_equity_trade_elements(self, xml_request):
        """
        Generate XML for XTP Trades
        """
        trade = xml_request.trade
        buy_or_sell = 'Purchase' if trade.Bought() else 'Sale'
        deal_reference = '{:0,.0f}'.format(trade.Oid())
        dealer_code = trade.Trader().Name()
        instrument = trade.Instrument()
        security_description = instrument.Name()
        isin = instrument.Isin()
        settlement_date = ASUSNewTradeConfirmationGeneral.format_string_to_asus_format(trade.ValueDay())
        trade_date = ASUSNewTradeConfirmationGeneral.format_string_to_asus_format(trade.TradeTime())
        usd_currency_instrument = acm.FCurrency['USD']
        spot_price = ASUSNewTradeConfirmationGeneral.get_current_usd_pot_price(usd_currency_instrument,
                                                                               instrument.Currency()
                                                                               )
        principal_amount = trade.Nominal()
        local_currency = instrument.Currency().Name()
        usd_principal_amount = principal_amount / spot_price
        commission = ASUSNewTradeConfirmationGeneral.get_commission_amount(trade)
        usd_commission = commission / spot_price
        consideration = abs(trade.Premium()) + commission if trade.Bought() else abs(trade.Premium()) - commission
        usd_consideration = consideration / spot_price
        clean_price = trade.Price() / 100
        us_clean_price = clean_price / spot_price
        if not clean_price:
            raise ValueError('Could not calculate the Clean price')

        delivery_type = 'DVP' if buy_or_sell == 'Sale' else 'RVP'
        disclosures = ''
        external_id1 = instrument.ExternalId1()
        external_id2 = instrument.ExternalId2()
        if not self.check_us_security_registration(external_id1, external_id2):
            disclosures += 'D1 '
        if instrument.Callable():
            disclosures += 'D2 '
        if instrument.Issuer() and 'absa' in instrument.Issuer().Name().lower():
            disclosures += 'D3'
        if disclosures == '':
            disclosures = 'n/a'

        element = self._generate_element('TRADE_CONFIRMATION')

        element.append(self._generate_element('PURCHASE_OR_SALE', str(buy_or_sell)))
        element.append(self._generate_element('DEAL_REFERENCE', str(deal_reference)))
        element.append(self._generate_element('DEALER_CODE', str(dealer_code)))
        element.append(self._generate_element('SECURITY_DESCRIPTION', str(security_description)))
        element.append(self._generate_element('ISIN', str(isin)))
        element.append(self._generate_element('SHARES', str('{:0,.0f}'.format(abs(trade.Quantity())))))
        element.append(self._generate_element('SETTLEMENT_DATE', str(settlement_date)))
        element.append(self._generate_element('TRADE_DATE', str(trade_date)))
        element.append(
            self._generate_element('LOCAL_PRINCIPAL_AMOUNT',
                                   str(ASUSNewTradeConfirmationGeneral.formated_display_value(local_currency,
                                                                                              '{:0,.2f}',
                                                                                              principal_amount)
                                       )))
        element.append(
            self._generate_element('USD_PRINCIPAL_AMOUNT',
                                   str(ASUSNewTradeConfirmationGeneral.formated_display_value('USD',
                                                                                              '{:0,.2f}',
                                                                                              usd_principal_amount)
                                       )))
        element.append(
            self._generate_element('LOCAL_CLEAN_PRICE',
                                   str(ASUSNewTradeConfirmationGeneral.formated_display_value(local_currency,
                                                                                              '{:0,.4f}',
                                                                                              clean_price)
                                       )))
        element.append(
            self._generate_element('US_CLEAN_PRICE',
                                   str(ASUSNewTradeConfirmationGeneral.formated_display_value('USD',
                                                                                              '{:0,.4f}',
                                                                                              us_clean_price)
                                       )))
        element.append(
            self._generate_element('LOCAL_CONSIDERATION',
                                   str(ASUSNewTradeConfirmationGeneral.formated_display_value(local_currency,
                                                                                              '{:0,.2f}',
                                                                                              consideration)
                                       )))
        element.append(
            self._generate_element('US_CONSIDERATION',
                                   str(ASUSNewTradeConfirmationGeneral.formated_display_value('USD',
                                                                                              '{:0,.2f}',
                                                                                              usd_consideration)
                                       )))
        element.append(self._generate_element('COMMISSION',
                                              str(ASUSNewTradeConfirmationGeneral.formated_display_value(local_currency,
                                                                                                         '{:0,.2f}',
                                                                                                         commission)
                                                  )))
        element.append(self._generate_element('US_COMMISSION',
                                              str(ASUSNewTradeConfirmationGeneral.formated_display_value('USD',
                                                                                                         '{:0,.2f}',
                                                                                                         usd_commission)
                                                  )))
        element.append(self._generate_element('SETTLEMENT_TERMS', str(delivery_type)))
        element.append(self._generate_element('ADDITIONAL_DISCLOSURES', str(disclosures)))
        element.append(self._generate_element('TRADE_TYPE', str('XTP_TRADES')))

        return element

    def check_us_security_registration(self, external_id1, external_id2):
        """
        Checks to see if the Security is registered in
        the U.S
        """
        if self.check_length_and_format(external_id1):
            return True
        if self.check_length_and_format(external_id2):
            return True

        return False

    @staticmethod
    def check_length_and_format(external_id):
        """
        Returns true if the ID meets the 7 digits
        and two Letters requirement
        """
        if external_id:
            if len(external_id) != 9:
                return False

            if not isinstance(external_id[:2], bytes):
                return False

            numbers = external_id[2:9]
            try:
                numbers = int(numbers)
            except Exception as error:
                LOGGER.warning('"{numbers}" : characters not in the correct format!: {error}'.format(numbers=numbers,
                                                                                                     error=error))
                return False
            return True

        return False


    def _get_dirty_price(self, trade):

        calculation_space_collection = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()

        from_quotation = trade.Instrument().Quotation()
        to_quotation = acm.FQuotation['Pct of Nominal']
        return trade.Calculation().PriceConvert(calculation_space_collection, trade.Price(), from_quotation,
                                                to_quotation, trade.ValueDay())


    def _get_accrued_interest(self, trade, clean_price, dirty_price):
        dirty_Price = dirty_price.Number()
        interest_in_price = dirty_Price - (clean_price * 100)
        return round(interest_in_price * trade.FaceValue() * 0.01, 2)
