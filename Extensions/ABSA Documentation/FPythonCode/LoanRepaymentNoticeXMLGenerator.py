"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanRepaymentNoticeXMLGenerator

DESCRIPTION
    This module contains classes used to generate the XML that will
    be fed into the XML template through the XML hooks called. This specifically uses a constructor
    that is fed into the xml generator that returns an acmtemplate to make up the body of the xml.

    This is called in the XML hooks module for repayment notices called LoanRepaymentNoticeXMLHooks

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-11-20                      Stuart Wilson           Loan Ops                XML generator for repayment notices
-----------------------------------------------------------------------------------------------------------------------------------------
"""

from datetime import date as datef
from datetime import datetime

import acm

from DocumentXMLGenerator import GenerateDocumentXMLRequest, DocumentXMLGenerator
import LoanNoticeGeneral
import LoanRepaymentNoticeScript

calculation_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()


class GenerateRepaymentNoticeXMLRequest(GenerateDocumentXMLRequest):

    def __init__(self, from_party, from_party_contact, to_party, to_party_contact, confirmation):
        """
        Constructor class for rate notice xml generator
        """
        super(GenerateRepaymentNoticeXMLRequest, self).__init__(from_party, from_party_contact, to_party, to_party_contact)
        self.trade = confirmation.Trade()
        self.confirmation = confirmation
        self.date = str(datef.fromtimestamp(confirmation.CreateTime()))
        self.paydate = acm.Time().DateAddDelta(self.date, 0, 0, 7)
        self.valid_trades_list = LoanRepaymentNoticeScript.get_valid_trades_per_party_acquirer_pair((to_party, from_party), self.paydate)
        self.currencies = LoanRepaymentNoticeScript.get_currencies_from_trades(self.valid_trades_list)

class RepaymentNoticeXMLGenerator(DocumentXMLGenerator):

    def add_redemption_to_fixed_amount(self, trade, cashflow_fixed_and_redemption):
        fixed_amount = 0
        redemption_amount = 0
        if cashflow_fixed_and_redemption[0]:
            fixed_amount = cashflow_fixed_and_redemption[0].Calculation().Projected(calculation_space, trade).Number()

        if cashflow_fixed_and_redemption[1]:
            redemption_amount = cashflow_fixed_and_redemption[1].Calculation().Projected(calculation_space, trade).Number()

        return fixed_amount + redemption_amount

    def get_trade_pm_facility_id(self, trade, trade_currency):
        """
        Function to get trade additional info PM_Facility_ID and splits the value(e.g
        CORPL|AUG16|TL|A = AUG16|TL|A)
        """
        trade_facility_id = trade.AdditionalInfo().PM_FacilityID()
        facility_id = trade_facility_id[trade_facility_id.index('|') + 1:].replace('|', ' ').replace(trade_currency, '')

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
                "its Corporate and Investment "
                "Banking division) and {1}").format(confirmation.AcquirerContactRef().Fullname2(),
                                                    confirmation.Counterparty().Fullname())
        return fac_agreement

    def get_facility_instrument_cashflow(self, trade, date):
        """
        This function returns the trade facility  cashflow details
        """
        cashflow_fixed_and_redemption = LoanRepaymentNoticeScript.seven_days_before_pay_day_fixed_cashflow(trade, date)
        cashflow = LoanRepaymentNoticeScript.seven_days_before_pay_day_cashflow(trade, date)

        if cashflow_fixed_and_redemption[0] is None and cashflow_fixed_and_redemption[1] is None:
            capital_due = 0
        else:
            capital_due = self.add_redemption_to_fixed_amount(trade, cashflow_fixed_and_redemption)
            
        if cashflow is None:
            interest_due = 0
            forward_rate = 0

            if cashflow_fixed_and_redemption[0] is not None:
                cashflow_for_dates = cashflow_fixed_and_redemption[0]

            elif cashflow_fixed_and_redemption[0] is None and cashflow_fixed_and_redemption[1] is not None:
                cashflow_for_dates = cashflow_fixed_and_redemption[1]

            previous_cashflow = LoanNoticeGeneral.get_previous_cashflow(cashflow_for_dates)
            commencement_date = datetime.strptime(previous_cashflow.StartDate(), '%Y-%m-%d').strftime('%d/%m/%Y')
            end_date = datetime.strptime(previous_cashflow.EndDate(), '%Y-%m-%d').strftime('%d/%m/%Y')

        else:
            commencement_date = datetime.strptime(cashflow.StartDate(), '%Y-%m-%d').strftime('%d/%m/%Y')
            end_date = datetime.strptime(cashflow.EndDate(), '%Y-%m-%d').strftime('%d/%m/%Y')
            interest_due = cashflow.Calculation().Projected(calculation_space, trade).Number()
            forward_rate = (cashflow.Calculation().ForwardRate(calculation_space) * 100)
            for reset in cashflow.Resets():
                if reset.Day() == date:
                    if LoanNoticeGeneral.match_primelinked_trades(trade):
                        rate = reset.FixingValue()
                        forward_rate = rate + cashflow.Spread()
                        

        trade_currency = trade.Currency().Name()
        facility_dict = dict()

        facility_dict['FACILITY_ID'] = self.get_trade_pm_facility_id(trade, trade_currency)
        facility_dict['APPLICABLERATE'] = "{:0.9g}".format(float(forward_rate))
        facility_dict['COMMENCEMENTDATE'] = commencement_date
        facility_dict['MATURITYDATE'] = end_date
        facility_dict['NOMINAL_AMOUNT'] = LoanNoticeGeneral.sum_nominal_before_payday(trade, date)
        facility_dict['CURRENCY'] = trade_currency
        facility_dict['INTEREST_DUE'] = "{:0.2f}".format(float(interest_due))
        facility_dict['CAPITAL_DUE'] = "{:0.2f}".format(float(capital_due))
        facility_dict['RUNNING_TOTAL'] = "{:0.2f}".format(float(capital_due)+float(interest_due))
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

    def get_totals_in_facilities(self, element):
        capital_due = 0
        interest_due = 0
        for tag in element:
            for subtag in tag:
                if subtag.tag == 'CAPITAL_DUE':
                    capital_due += float(subtag.text)
                elif subtag.tag == 'INTEREST_DUE':
                    interest_due += float(subtag.text)

        return capital_due, interest_due

    def get_facilities_xml_element(self, xml_request, currency):
        element = self._generate_element('FACILITIES')
        date = xml_request.date

        if xml_request.valid_trades_list:

            for trade in xml_request.valid_trades_list:
                if trade.Currency() == currency:
                    if abs(LoanNoticeGeneral.sum_nominal_before_payday(trade, date)) > 0.00:
                        element.append(self.get_facility_cashflow_element(trade, date))
        totals = self.get_totals_in_facilities(element)
        element.append(self._generate_element('CAPITAL_DUE_TOTAL', "{:0.2f}".format(totals[0])))
        element.append(self._generate_element('INTEREST_DUE_TOTAL', "{:0.2f}".format(totals[1])))
        element.append(self._generate_element('GRAND_TOTAL', "{:0.2f}".format(totals[0] + totals[1])))

        return element

    def get_legalnotice_loan(self, xml_request):
        normal_disclaimer = LoanNoticeGeneral.loan_notice_get_documentation_parameter('normal_disclaimer')
        prime_disclaimer = LoanNoticeGeneral.loan_notice_get_documentation_parameter('prime_disclaimer')
        for trade in xml_request.valid_trades_list:
            if LoanNoticeGeneral.match_primelinked_trades(trade):
                disclaimer1 = '{prime}\n\n{normal}'.format(prime=prime_disclaimer,
                                                           normal=normal_disclaimer)
                return self._generate_element('REPAYMENT_NOTICE_DISClAIMER', disclaimer1)
        disclaimer2 = normal_disclaimer
        return self._generate_element('REPAYMENT_NOTICE_DISClAIMER', disclaimer2)

    def get_account_details(self, xml_request, currency):
        date = xml_request.paydate
        element = self._generate_element('ACCOUNT')
        for trade in xml_request.valid_trades_list:
            if trade.Currency().Name() == currency:
                accounts = trade.GenerateSettlements(date, date)
                break

        if accounts:
            account = accounts[0].AcquirerAccountRef()
            if currency == 'ZAR':

                element.append(self._generate_element('NAME', xml_request.confirmation.AcquirerContactRef().Fullname2()))
                element.append(self._generate_element('NUMBER', account.Account()[7:18]))
                element.append(self._generate_element('BANK', account.CorrespondentBank().Name()))
                element.append(self._generate_element('BRANCH', account.Account()[:6]))
                element.append(self._generate_element('REFERENCE', str(xml_request.trade.Counterparty().Fullname())))
                element.append(self._generate_element('CURRENCY', str(currency)))
            else:
                element.append(self._generate_element('NAME', xml_request.confirmation.AcquirerContactRef().Fullname2()))
                element.append(self._generate_element('NUMBER', account.Account()))
                element.append(self._generate_element('BANK', account.CorrespondentBank().Name()))
                element.append(self._generate_element('BRANCH', account.Bic().Name()))
                element.append(self._generate_element('REFERENCE', str(xml_request.trade.Counterparty().Fullname())))
                element.append(self._generate_element('CURRENCY', str(currency)))
        return element

    def get_date_payable(self, xml_request):

        date = datetime.strptime(acm.Time().DateAddDelta(xml_request.date, 0, 0, 7), '%Y-%m-%d').strftime('%d %B %Y')

        return self._generate_element('PAY_DATE', date)

    def _generate_subject_element(self, xml_request):
        """
        Generate the document SUBJECT XML element and sub-
        elements.
        """
        return self._generate_element('SUBJECT', 'Repayment Notice')

    def is_last_element_curr_loop(self, currency, xml_request):

        return self._generate_element('LAST_ELEMENT', str(currency == xml_request.currencies[-1]))

    def _generate_document_specific_element(self, xml_request):
        """
        Generate the document RATENOTICE XML element and sub-
        elements.
        """
        main_element = self._generate_element('REPAYMENTNOTICE')
        facility_agreement = xml_request.confirmation
        facility_aggr = self.rate_notice_facility_agreement(facility_agreement)

        for currency in xml_request.currencies:
            element = self._generate_element('MAIN_CURRENCY')
            element.append(self._generate_element('FACIL_AGREE', facility_aggr))
            element.append(self.get_facilities_xml_element(xml_request, currency))
            element.append(self.get_legalnotice_loan(xml_request))
            element.append(self.get_account_details(xml_request, currency.Name()))
            element.append(self.get_date_payable(xml_request))
            element.append(self.is_last_element_curr_loop(currency, xml_request))
            main_element.append(element)

        return main_element



