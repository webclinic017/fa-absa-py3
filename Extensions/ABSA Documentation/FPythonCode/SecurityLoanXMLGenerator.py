"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SecurityLoanXMLGenerator

DESCRIPTION
    This module contains general functionality related to Security Loan XML generation

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-01-31      FAOPS-557       Tawanda Mukhalela       Khaya Mbebe             Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import datetime
import xml.etree.ElementTree as ElementTree

import acm

import DocumentGeneral
import DocumentBusinessProcessGeneral
import SecurityLoanGeneral


class GenerateSecurityLoanConfirmationXMLRequest(object):

    def __init__(self, business_process, previous_xml):
        """
        Generates XML request.
        """

        if business_process.Subject().IsKindOf(acm.FParty):
            self.counterparty = business_process.Subject()
        if business_process.Subject().IsKindOf(acm.FTrade):
            self.trade = business_process.Subject()
            self.counterparty = SecurityLoanGeneral.get_lender_or_borrower_party(business_process.Subject())
        self.is_amendment = business_process.Subject().IsKindOf(acm.FTrade)
        self.instrument_type = business_process.AddInfoValue(DocumentBusinessProcessGeneral
                                                             .get_business_process_instype_add_info_name())
        self.document_type = business_process.AddInfoValue(DocumentBusinessProcessGeneral
                                                           .get_business_process_trade_type_add_info_name())
        self.previous_xml = previous_xml


class SecurityLoanXMLGenerator(object):

    def __init__(self):
        pass

    def generate_xml(self, xml_request):
        security_loan_confirmation_element = self._generate_element('DOCUMENT')
        from_party = acm.FParty['SECURITY LENDINGS DESK']
        from_party_contact = SecurityLoanGeneral.get_party_contacts(from_party, xml_request.instrument_type)[0]
        to_party = xml_request.counterparty
        to_party_contact = SecurityLoanGeneral.get_party_contacts(to_party, xml_request.instrument_type)[0]
        security_loan_confirmation_element.append(self._generate_document_type_elelemnt(xml_request))
        security_loan_confirmation_element.append(self._generate_direction_message(xml_request))
        security_loan_confirmation_element.append(self._generate_from_element(from_party_contact))
        security_loan_confirmation_element.append(self._generate_to_element(to_party, to_party_contact))
        security_loan_confirmation_element.append(self._generate_subject_element(xml_request))
        security_loan_confirmation_element.append(self._generate_trades_element(xml_request))

        return ElementTree.tostring(security_loan_confirmation_element)

    def _generate_document_type_elelemnt(self, xml_request):
        """
        Generates the document type element
        """
        type = xml_request.document_type
        if type in (None, ''):
            return self._generate_element('DUCUMENT_TYPE', str('NEW_LOAN'))
        return self._generate_element('DUCUMENT_TYPE', str(type))

    def _generate_direction_message(self, xml_request):
        """
        Generates attention message for the document
        """
        direction = ''
        delivery_direction = ''
        if xml_request.document_type in ('PARTIAL_RETURN', 'FULL_RETURN'):
            direction = 'RETURN TO' if SecurityLoanGeneral.is_lender(xml_request.counterparty) else 'RETURN FROM'
            delivery_direction = 'DELIVER' if direction == 'RETURN TO' else 'RECEIVE'
        else:
            direction = 'BORROW FROM' if SecurityLoanGeneral.is_lender(xml_request.counterparty) else 'LOAN TO'
            delivery_direction = 'DELIVER' if direction == 'LOAN TO' else 'RECEIVE'

        summary1 = 'We are pleased to confirm the following {direction} YOU'.format(direction=direction)
        summary2 = 'We {delivery_direction} the following Securities Free Of Payment'.format(
            delivery_direction=delivery_direction
        )

        element = self._generate_element('ATTENTION_MESSAGE')
        element.append(self._generate_element('SUMMERY1', str(summary1)))
        element.append(self._generate_element('SUMMERY2', str(summary2)))

        return element

    def _generate_from_element(self, from_party_contact):
        """
        Generate the document FROM XML element and sub-elements.
        """
        element = self._generate_element('FROM')
        element.append(self._generate_element('NAME', DocumentGeneral.get_default_document_from_name()))
        element.append(self._generate_address_element(from_party_contact))
        element.append(self._generate_element('TEL', from_party_contact.Telephone()))
        element.append(self._generate_element('EMAIL', from_party_contact.Email()))
        element.append(self._generate_element('WEBSITE', DocumentGeneral.get_default_document_from_website()))
        element.append(self._generate_element('DATE', str(datetime.date.today().strftime("%d %B %Y"))))

        return element

    def _generate_to_element(self, to_party, to_party_contact):
        """
        Generate the document TO XML element and sub-elements.
        """
        element = self._generate_element('TO')
        element.append(self._generate_element('NAME', DocumentGeneral.get_party_full_name(to_party)))
        # Add the value of the party ShortCode field if present.
        # This field is generally used to hold any related fund
        # code associated with a party.
        short_code = DocumentGeneral.get_party_short_code(to_party)
        element.append(self._generate_element('SHORTCODE', short_code if short_code else ""))
        element.append(self._generate_address_element(to_party_contact))
        element.append(self._generate_element('TO_TELEPHONE', str(to_party_contact.Telephone())))
        element.append(self._generate_element('TO_ATTENTION', str(to_party_contact.Attention())))
        return element

    def _generate_address_element(self, party_contact):
        """
        Generate an ADDRESS XML element and sub-elements.
        """
        element = self._generate_element('ADDRESS')
        element.append(self._generate_element('LINE1', party_contact.Address()))
        element.append(self._generate_element('LINE2', party_contact.Address2()))
        element.append(self._generate_element('CITY', party_contact.City()))
        element.append(self._generate_element('COUNTRY', party_contact.Country()))
        element.append(self._generate_element('ZIPCODE', party_contact.Zipcode()))
        return element

    def _generate_subject_element(self, xml_request):
        """
        Generate the document SUBJECT XML element and sub-
        elements.
        """
        return_subject = 'Return Confirmation'
        newloan_subject = 'Loan Confirmation'
        if xml_request.is_amendment:
            if 'Void' == xml_request.trade.Status():
                return_subject = return_subject + ' ' + 'Cancellation'
                newloan_subject = newloan_subject + ' ' + 'Cancellation'
            else:
                return_subject = return_subject + ' ' + 'Amendment'
                newloan_subject = newloan_subject + ' ' + 'Amendment'

        if xml_request.document_type in ('PARTIAL_RETURN', 'FULL_RETURN'):
            return self._generate_element('SUBJECT', return_subject)
        return self._generate_element('SUBJECT', newloan_subject)

    def _generate_trades_element(self, xml_request):
        """"
        Get Document Specific element Security Loan
        """
        element = self._generate_element('TRADES')
        if xml_request.is_amendment:
            element.append(self.get_trade(xml_request.trade, xml_request))
        elif xml_request.previous_xml:
            previous_trades = SecurityLoanGeneral.get_trades_from_previons_xml(xml_request.previous_xml)
            for trade in previous_trades:
                acm_trade = acm.FTrade[trade.trade_number]
                trade_type = '' if xml_request.document_type is None else xml_request.document_type
                if acm_trade.Text1() != trade_type:
                    continue
                element.append(self.get_trade(acm_trade, xml_request))
        else:
            trades = SecurityLoanGeneral.get_valid_trades_for_counterparty(xml_request.counterparty,
                                                                           xml_request.document_type
                                                                           )
            if not trades:
                raise ValueError('All trades have already been sent. Suppressing Document in Generation Failed state')
            for trade in trades:
                element.append(self.get_trade(trade, xml_request))

        return element

    def get_trade(self, trade, xml_request):
        """
        Populates the Security Loan XML Details
        """
        instrument = trade.Instrument()
        security_instrument = instrument.Underlying().Name().split('/')[1]
        isin = instrument.Underlying().Isin()
        trade_date = datetime.datetime(*acm.Time.DateToYMD(trade.TradeTime())).strftime('%d/%m/%Y')
        value_date = datetime.datetime(*acm.Time.DateToYMD(trade.ValueDay())).strftime('%d/%m/%Y')
        link_ref = trade.ContractTrdnbr()
        rate = SecurityLoanGeneral.get_secloan_rate(trade)
        if rate is None:
            raise ValueError('No Fee defined on trade {trade}'.format(trade=trade))
        rate_including_vat = '{0:.3f}'.format(rate)
        rate_excluding_vat = SecurityLoanGeneral.get_secloan_rate_excl_vat(rate)
        loan_price = trade.AllInPrice()/100
        vatable = 'Vatable' if instrument.AdditionalInfo().SL_VAT() is True else 'Non-Vatable'
        recall_period = '3 Days'
        delivery_mode = ''
        if trade.AdditionalInfo().SL_SWIFT() == 'SWIFT':
            delivery_mode = 'On-Market'
        elif trade.AdditionalInfo().SL_SWIFT() == 'DOM':
            delivery_mode = 'Off-Market'
        min_fee = instrument.AdditionalInfo().SL_Minimum_Fee()
        text1 = trade.Text1()
        quantity = SecurityLoanGeneral.get_secloan_quantity(trade)
        if text1 in ('PARTIAL_RETURN', 'FULL_RETURN'):
            quantity = SecurityLoanGeneral.get_return_value(trade)

        # For partial Returns
        original_trade = acm.FTrade[link_ref]
        original_quantity = SecurityLoanGeneral.get_secloan_quantity(original_trade)
        original_date = datetime.datetime(*acm.Time.DateToYMD(original_trade.TradeTime())).strftime('%d/%m/%Y')
        original_price = '{:0,.2f}'.format(float(original_trade.AllInPrice())/100)
        original_rate = '{:0,.3f}'.format(SecurityLoanGeneral.get_secloan_rate(original_trade))
        original_loan_value = '{:0,.2f}'.format(loan_price * float(quantity))

        element = self._generate_element('TRADE')
        element.append(self._generate_element('TRADE_DNUMBER', str(trade.Oid())))
        element.append(self._generate_element('ISIN', str(isin)))
        element.append(self._generate_element('SECURITY', str(security_instrument)))
        element.append(self._generate_element('QUANTITY', str('{:0,.0f}'.format(quantity))))
        element.append(self._generate_element('TRADE_DATE', str(trade_date)))
        element.append(self._generate_element('SETTLEMENT_DATE', str(value_date)))
        element.append(self._generate_element('RATE_EXL_VAT', str(rate_excluding_vat)))
        element.append(self._generate_element('RATE_INC_VAT', str(rate_including_vat)))
        element.append(self._generate_element('LOAN_PRICE', str(loan_price)))
        element.append(self._generate_element('LOAN_VALUE', str(original_loan_value)))
        element.append(self._generate_element('VATABLE', str(vatable)))
        element.append(self._generate_element('RECALL_PERIOD', str(recall_period)))
        element.append(self._generate_element('DELIVERY_MODE', str(delivery_mode)))
        element.append(self._generate_element('MIN_FEE', str(min_fee)))
        element.append(self._generate_element('TEXT1', str(text1)))
        element.append(self._generate_element('ORIGINAL_DATE', str(original_date)))
        element.append(self._generate_element('ORIGINAL_PRICE', str(original_price)))
        element.append(self._generate_element('ORIGINAL_QUANTITY', str('{:0,.0f}'.format(original_quantity))))
        element.append(self._generate_element('ORIGINAL_RATE', str(original_rate)))

        return element

    @staticmethod
    def _generate_element(element_name, element_text=''):
        """
        Generate an XML element with the specified name and text.
        """
        element = ElementTree.Element(element_name)
        element.text = element_text
        return element

