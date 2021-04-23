"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanBalanceStatementXMLGenerator

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

import acm

from DocumentXMLGenerator import GenerateDocumentXMLRequest, DocumentXMLGenerator


standard_calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')


class GenerateLoanBalanceStatementXMLRequest(GenerateDocumentXMLRequest):

    def __init__(self, trade, from_party, from_party_contact, to_party, to_party_contact,
            from_date, to_date):
        """
        Constructor.
        """
        super(GenerateLoanBalanceStatementXMLRequest, self).__init__(from_party, from_party_contact,
            to_party, to_party_contact)
        self.trade = trade
        self.from_date = from_date
        self.to_date = to_date
        self.date_day_before = acm.Time().DateAddDelta(from_date, 0, 0, -1)

class LoanBalanceStatementXMLGenerator(DocumentXMLGenerator):

    def _generate_element_using_dictionary(self, element_name, element_dict=None, ignore_update=False):
        """
        Generates element using dictionary type and applies required formatting to currencies and decimals
        """
        element_text = None

        if not element_dict:
            element_text = ''

        elif isinstance(element_dict, str) or isinstance(element_dict, float) or isinstance(element_dict, int):
            element_text = element_dict

        elif isinstance(element_dict, dict):
            element_text = element_dict[element_name]
        return self._generate_element(element_name, element_text, ignore_update)

    def is_trade_active_during_period(self, trade, request):
        start_date = trade.Instrument().StartDate()
        end_date = trade.Instrument().EndDate()
        if request.to_date < start_date or end_date < request.from_date:
            return False
        else:
            return True

    def get_all_counterparty_trades(self, request):
        query_name = 'ABSA_LOAN_BALANCE_STATEMENT'
        query_nodes = acm.FStoredASQLQuery[query_name].Query().AsqlNodes()
        asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        asql_query.AsqlNodes(query_nodes)
        asql_query.AddAttrNode('Counterparty.Oid', 'EQUAL', request.to_party.Oid())
        trades = asql_query.Select()
        valid_trades = list()
        for trade in trades:
            if self.is_trade_active_during_period(trade, request):
                valid_trades.append(trade)
        return valid_trades

    def filter_into_facilities(self, list_of_trades):
        facility_dict = dict()

        for trade in list_of_trades:

            pm_facility_id = self.get_trade_pm_facility_id(trade)
            if pm_facility_id not in list(facility_dict.keys()):
                facility_dict[pm_facility_id] = list()
                facility_dict[pm_facility_id].append(trade)
            else:
                facility_dict[pm_facility_id].append(trade)

        return facility_dict

    def filter_trades_into_currency(self, request):
        currency_dictionary = dict()

        for trade in self.get_all_counterparty_trades(request):
            currency = trade.Currency().Name()
            if currency not in list(currency_dictionary.keys()):
                currency_dictionary[currency] = list()
                currency_dictionary[currency].append(trade)
            else:
                currency_dictionary[currency].append(trade)
        return currency_dictionary

    def get_trade_pm_facility_id(self, trade):
        """
        Function to get trade additional info PM_Facility_ID and splits the value(e.g
        CORPL|AUG16|TL|A = AUG16|TL|A)
        """
        trade_currency = trade.Currency().Name()
        trade_facility_id = trade.AdditionalInfo().PM_FacilityID()
        facility_id = trade_facility_id[trade_facility_id.index('|') + 1:].replace('|', ' ').replace(trade_currency, '')

        return facility_id

    def _generate_subject_element(self, xml_request):
        """
        Generate the document SUBJECT XML element and sub-
        elements.
        """
        return self._generate_element('SUBJECT', 'Balance Statement')

    def _generate_document_specific_element(self, request):
        """
        Generate the document RATENOTICE XML element and sub-
        elements.
        """
        main_element = self._generate_element('BALANCE_STATEMENT')
        day_before_from_date_element = self._generate_element('DAY_BEFORE_FROM_DATE', request.date_day_before)
        main_element.append(day_before_from_date_element)
        from_date_element = self._generate_element('FROM_DATE', request.from_date)
        main_element.append(from_date_element)
        to_date_element = self._generate_element('TO_DATE', request.to_date)
        main_element.append(to_date_element)
        facility_element = self.create_facilities_xml(request)
        main_element.append(facility_element)

        return main_element

    def create_facilities_xml(self, request):
        currencies = self.filter_trades_into_currency(request)
        element = self._generate_element("FACILITIES")
        for currency in currencies:
            facilities_per_currency = self.filter_into_facilities(currencies[currency])
            for facility in facilities_per_currency:
                template_dict = self.create_facility_dictionary(currency, facilities_per_currency[facility], facility, request)
                sub_element = self.convert_dict_to_facility_xml(template_dict)
                element.append(sub_element)
        return element

    def set_calc_space_inception_to(self, _date, calc_space):
        calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Inception')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', _date)
        calc_space.Refresh()

    def get_specific_cashflows_total(self, trade, from_date, to_date, type):
        cashflows = trade.Instrument().MainLeg().CashFlows().AsArray()
        total = 0.0
        for cashflow in cashflows:
                if cashflow.CashFlowType() == type:
                    if from_date <= cashflow.PayDate() <= to_date:
                        total = total + cashflow.Calculation().Projected(standard_calc_space, trade).Value().Number()
        return total

    def facility_calculation(self, list_of_trades, currency, request):
        calc_dic = dict()
        interest_accrued = 0.0
        interest_paid = 0.0
        interest_reinvested = 0.0
        capital_out = 0.0
        interest = 0.0
        nominal = 0.0
        if currency == 'ZAR':
            nominal_col = 'Current Nominal'
            interest_col = 'Portfolio Accrued Interest'
        else:
            nominal_col = 'DDM Nominal TXN CCY'
            interest_col = 'DDM Accrued Interest TXN CCY'

        self.set_calc_space_inception_to(request.date_day_before, calc_space)
        for trade in list_of_trades:
            top_node = calc_space.InsertItem(trade)
            interest = interest + calc_space.CreateCalculation(top_node, interest_col).Value().Number()
            nominal = nominal + calc_space.CreateCalculation(top_node, nominal_col).Value()
            interest_paid = interest_paid + self.get_specific_cashflows_total(trade, request.from_date, request.to_date, 'Call Float Rate')
            interest_paid = interest_paid + self.get_specific_cashflows_total(trade, request.from_date, request.to_date, 'Call Fixed Rate')
            interest_reinvested = interest_reinvested + self.get_specific_cashflows_total(trade, request.from_date, request.to_date, 'Interest Reinvestment')

        self.set_calc_space_inception_to(request.to_date, calc_space)
        for trade in list_of_trades:
            top_node = calc_space.InsertItem(trade)
            capital_out = capital_out + calc_space.CreateCalculation(top_node, nominal_col).Value()
            interest_accrued = interest_accrued + calc_space.CreateCalculation(top_node, interest_col).Value().Number()

        opening_bal = nominal + interest
        closing_bal = capital_out + interest_accrued

        calc_dic['opening_bal'] = opening_bal
        calc_dic['interest_accrued'] = interest_accrued
        calc_dic['interest_paid'] = interest_paid
        calc_dic['interest_reinvested'] = interest_reinvested
        calc_dic['capital_out'] = capital_out
        calc_dic['closing_bal'] = closing_bal

        return calc_dic

    def create_facility_dictionary(self, currency, list_of_trades, pm_facility_id, request):
        template_dict = dict()
        calculated_results = self.facility_calculation(list_of_trades, currency, request)
        template_dict['CURRENCY'] = currency
        template_dict['FACILITY_ID'] = pm_facility_id
        template_dict['OPENING_BALANCE'] = str(calculated_results['opening_bal'])
        template_dict['INTEREST_ACCRUED'] = str(calculated_results['interest_accrued'])
        template_dict['INTEREST_PAID'] = str(calculated_results['interest_paid'])
        template_dict['INTEREST_REINVEST'] = str(calculated_results['interest_reinvested'])
        template_dict['CAPITAL_OUT_BALANCE'] = str(calculated_results['capital_out'])
        template_dict['CLOSING_BALANCE'] = str(calculated_results['closing_bal'])
        return template_dict

    def convert_dict_to_facility_xml(self, template_dict):
        """
        Converts dictionary data to XML
        """
        element = self._generate_element("FACILITY")

        for xml_header in list(template_dict.keys()):
            element.append(self._generate_element_using_dictionary(xml_header, template_dict))

        return element

