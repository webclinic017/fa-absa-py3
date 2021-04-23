"""
-------------------------------------------------------------------------------
MODULE
    LoanNoticeConfirmationXMLGenerator


DESCRIPTION
    Date                : 2018-06-14
    Purpose             :
    Requester           : Kgomotso Gumbo
    Developer           : Adelaide Davhana


HISTORY
===============================================================================
2018-02-27    Adelaide Davhana   FAOPS-97: initial implementation
2018-09-20    Stuart Wilson      FAOPS-97  Refactor
-------------------------------------------------------------------------------"""

from datetime import date as datef

import acm
import ael

from DocumentXMLGenerator import GenerateDocumentXMLRequest, DocumentXMLGenerator
import LoanNoticeGeneral


calculation_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()


class GenerateRateNoticeXMLRequest(GenerateDocumentXMLRequest):

    def __init__(self, from_party, from_party_contact, to_party, to_party_contact, confirmation):
        """
        Constructor class for rate notice xml generator
        """
        super(GenerateRateNoticeXMLRequest, self).__init__(from_party, from_party_contact, to_party, to_party_contact)
        self.trade = confirmation.Trade()
        self.confirmation = confirmation
        self.date = str(datef.fromtimestamp(confirmation.CreateTime()))
        self.valid_trades_list = LoanNoticeGeneral.trade_filter(self.trade, self.date)


class RateNoticeXMLGenerator(DocumentXMLGenerator):

    def get_trade_pm_facility_id(self, trade):
        """
        Function to get trade additional info PM_Facility_ID and splits the value(e.g
        CORPL|AUG16|TL|A = AUG16|TL|A)
        """
        trade_facility_id = trade.AdditionalInfo().PM_FacilityID()
        facility_id = trade_facility_id[trade_facility_id.index('|') + 1:].replace('|', ' ')
        return facility_id

    def rate_notice_facility_agreement(self, confirmation):
        """
        This Function returns the Facility agreement between counterparty and acquirer
        """
        if confirmation.Acquirer().Name() == 'IMPUMELELO SERIES 1 ACQUIRER':
            fac_agreement = (
                "Facility Agreement/s entered into between {0} (administered by Absa "
                "through its Corporate and Investment Banking division) and {1}").format(
                                                    confirmation.AcquirerContactRef().Fullname2(),
                                                    confirmation.Counterparty().Fullname())

        else:
            fac_agreement = (
                "Facility Agreement/s entered into between {0} (acting through "
                "it's Corporate and Investment "
                "Banking division) and {1}").format(confirmation.AcquirerContactRef().Fullname2(),
                                                    confirmation.Counterparty().Fullname())
        return fac_agreement

    def get_facility_instrument_cashflow(self, trade, date):
        """
        This function returns the trade facility  cashflow details
        """

        rate = '0.00'
        forward_rate = '0.00'
        cashflow = LoanNoticeGeneral.get_current_cashflow(trade, date)
        trade_currency = trade.Currency().Name()
        facility_dict = dict()
        for reset in cashflow.Resets():
            if reset.FixingValue() != 0.0 and reset.Day() == date:
                if LoanNoticeGeneral.match_primelinked_trades(trade):
                    rate = reset.FixingValue()
                    forward_rate = rate + cashflow.Spread()
                else:
                    rate = reset.FixingValue()
                    forward_rate = (cashflow.Calculation().ForwardRate(calculation_space) * 100)
        facility_dict['FACILITY_ID'] = self.get_trade_pm_facility_id(trade)
        facility_dict['APPLICABLERATE'] = "{:0.9g}".format(float(forward_rate))
        facility_dict['COMMENCEMENTDATE'] = cashflow.StartDate()
        facility_dict['MARGIN'] = "{:0.9g}".format(float(cashflow.Spread()))
        facility_dict['MATURITYDATE'] = cashflow.EndDate()
        facility_dict['DURATION'] = ael.date(cashflow.StartDate()).days_between(ael.date(cashflow.EndDate()))
        facility_dict['RATE'] = "{:0.9g}".format(float(rate))
        facility_dict['RATE_TYPE'] = LoanNoticeGeneral.get_instrument_leg_float_ref(trade.Instrument()).Name()
        facility_dict['NOMINAL_AMOUNT'] = float("{:.2f}".format(float(LoanNoticeGeneral.sum_nominal_before_payday(trade, date))))
        facility_dict['CURRENCY'] = trade_currency
        return facility_dict

    def get_facility_cashflow_element(self, trade, date):
        """
        Function to create facility cashflow xml child element 'FACILITY'
        """
        facility_dict = self.get_facility_instrument_cashflow(trade, date)
        element = self._generate_element('FACILITY')
        for tag_name, value in list(facility_dict.items()):
            element.append(self._generate_element(tag_name, str(value)))
        return element

    def get_facilities_xml_element(self, xml_request):
        element = self._generate_element('FACILITIES')
        date = xml_request.date

        if xml_request.valid_trades_list:
            for trade in xml_request.valid_trades_list:

                if LoanNoticeGeneral.check_valid_reset(trade, date) and \
                        abs(LoanNoticeGeneral.sum_nominal_before_payday(trade, date)) > 0.00:
                    element.append(self.get_facility_cashflow_element(trade, date))

        return element

    def get_legalnotice_loan(self, xml_request):
        normal_disclaimer = LoanNoticeGeneral.loan_notice_get_documentation_parameter('normal_disclaimer')
        prime_disclaimer = LoanNoticeGeneral.loan_notice_get_documentation_parameter('prime_disclaimer')
        if LoanNoticeGeneral.is_prime_facility_present_in_element(self.get_facilities_xml_element(xml_request)):
            disclaimer1 = '{prime}\n\n{normal}'.format(prime=prime_disclaimer,
                                                       normal=normal_disclaimer)
            return self._generate_element('LOAN_NOTICE_DISClAIMER', disclaimer1)
        disclaimer2 = normal_disclaimer
        return self._generate_element('LOAN_NOTICE_DISClAIMER', disclaimer2)

    def _generate_subject_element(self, xml_request):
        """
        Generate the document SUBJECT XML element and sub-
        elements.
        """
        facility_agreement = xml_request.confirmation
        facility_aggr = self.rate_notice_facility_agreement(facility_agreement)
        return self._generate_element('SUBJECT', facility_aggr)

    def _generate_document_specific_element(self, xml_request):
        """
        Generate the document RATENOTICE XML element and sub-
        elements.
        """
        element = self._generate_element('RATENOTICE')
        element.append(self.get_facilities_xml_element(xml_request))
        element.append(self.get_legalnotice_loan(xml_request))
        return element
