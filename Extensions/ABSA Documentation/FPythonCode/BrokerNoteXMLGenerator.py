"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    BrokerNoteXMLGenerator

DESCRIPTION
    This module contains an object used for generating the XML content for a
    broker note.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-08-13      FAOPS-61        Stuart Wilson           Capital Markets         Initial Implementation.
2019-05-15      FAOPS-492       Hugo Decloedt           Seven Khoza             Adding companion fields for all instruments.
2020-02-10      FAOPS-725       Cuen Edwards            Kgomotso Gumbo          Minor refactoring.
2020-06-03      FAOPSS-739      Ntokozo Skosana         Nqubeko Zondi           Added logic for generating XML content
                                                                                for combination instruments.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

from datetime import datetime

import acm

import at
from at_time import acm_date
from DocumentGeneral import get_fparameter, get_party_full_name, format_amount
from DocumentXMLGenerator import GenerateDocumentXMLRequest, DocumentXMLGenerator
from zak_funcs import formnum


class GenerateCustodianAccountDetails(object):
    """
    Constructor class for generating required custodian details for broker notes

    Using constructor due to disconnection between settlement system and front sending out the broker notes
    keeping the custodian details separate because the way in which they settle may change in the future with MT500
    series and the inclusion of further custodians (Euroclear and JP Morgan)
    """

    def __init__(self, confirmation):

        settle_category = confirmation.Trade().SettleCategoryChlItem()
        currency = confirmation.Trade().Currency()
        acquirer = confirmation.Acquirer()
        """temporary bypass until front cache updates sett category for allocation trades"""
        if not settle_category:
            custodian = 'SA Custodian'

        elif settle_category:
            if settle_category.Name() == 'SA_CUSTODIAN':
                custodian = 'SA Custodian'
            elif settle_category.Name()[:9] == 'Euroclear':
                custodian = 'Euroclear Custodian'
            elif settle_category.Name()[:9] == 'JP Morgan':
                custodian = 'JP Morgan Custodian'
            elif settle_category.Name()[:3] == 'SSA':
                custodian = 'SSA Custodian'
            else:
                raise AttributeError("Invalid trade settlement category")
        #else:
         #   raise AttributeError("No settle category selected")

        valid_accounts = self._get_valid_acquirer_accounts(acquirer)

        cash_acc, scrip_acc = self._get_cash_and_securities_account_using_custodian_and_currency(valid_accounts,
                                                                                                 custodian, currency)

        try:
            self.custodian_cash = cash_acc.Account()
            self.custodian_scrip = scrip_acc.Account()
            self.custodian_bic = scrip_acc.Bic().Name()
            self.custodian = custodian
            if scrip_acc.Bic3() is not None:
                self.PSET = scrip_acc.Bic3().Name()
            else:
                self.PSET = scrip_acc.Bic().Name()

        except AttributeError:
            raise AttributeError("Custodian account details are not setup correctly on acquirer")

    def free_text_fields_used(self):
        return ['SA Custodian', 'Euroclear Custodian', 'SSA Custodian', 'JP Morgan Custodian']

    def _get_valid_acquirer_accounts(self, acquirer):
        valid_accounts = list()
        for account in acquirer.Accounts():
            if account.Accounting() is None:
                continue
            elif account.Accounting() not in self.free_text_fields_used():
                continue
            else:
                valid_accounts.append(account)
        return valid_accounts

    def _get_cash_and_securities_account_using_custodian_and_currency(self, valid_accounts, custodian, currency):
        cash_acc = None
        sec_acc = None
        for account in valid_accounts:
            if account.Accounting() != custodian:
                continue
            elif account.Currency() is None or account.Currency() == currency:
                if account.AccountType() == 'Cash':
                    cash_acc = account
                elif account.AccountType() == 'Cash and Security':
                    sec_acc = account

        if sec_acc is None:
            raise RuntimeError("Acquirer account details not setup for selected settlement category - Broker Note")

        elif cash_acc is None:
            cash_acc = sec_acc

        return cash_acc, sec_acc


class GenerateBrokerNoteXMLRequest(GenerateDocumentXMLRequest):
    """
    An object embodying the request to generate the XML content for a
    broker note.
    """

    def __init__(self, confirmation, custodian_parameters):
        """
        Constructor.
        """
        # super(GenerateBrokerNoteXMLRequest, self).__init__(confirmation, custodian_parameters, None, None)

        self.from_party = confirmation.Acquirer()
        self.from_party_contact = confirmation.AcquirerContactRef()
        self.to_party = confirmation.Counterparty()
        self.to_party_contact = confirmation.CounterpartyContactRef()
        self.instype = confirmation.Trade().Instrument().InsType()
        self.acm_trade = confirmation.Trade()
        self.acm_instrument = confirmation.Trade().Instrument()
        self.currency = self.acm_instrument.Currency().Name()
        self.counterparty = confirmation.Trade().Counterparty()
        self.acm_underlying = confirmation.Trade().Instrument().Underlying()
        self.calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
        self.unexcor_code = self.counterparty.AddInfoValue('UnexCor Code')
        self.acquirer_unexcore_code = confirmation.Acquirer().AddInfoValue('UnexCor Code')
        self.settlement_date = acm_date(self.acm_trade.ValueDay())
        self.custodian_cash = custodian_parameters.custodian_cash
        self.custodian_scrip = custodian_parameters.custodian_scrip
        self.custodian_bic = custodian_parameters.custodian_bic
        self.PSET = custodian_parameters.PSET
        self.custodian = custodian_parameters.custodian
        self.companion = self.acm_instrument.AddInfoValue('Companion')
        self.companion_spread = self.acm_trade.AddInfoValue('Companion_Spread')


class BrokerNoteXMLGenerator(DocumentXMLGenerator):
    """
    An object responsible for generating the XML content for a broker
    note.
    """

    def _get_documentation_parameter(self, parameter_name):
        """
        Get a documentation FParameter value.
        """
        return get_fparameter('ABSABrokerNoteParameters', parameter_name)

    def format_date(self, date):
        """
        Formats the date returned to meet required date specifications
        """
        if len(date) < 11:
            return datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
        return datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')

    def length_of_number(self, number):
        """
        Returns to the number of digits in a number excluding decimal digits
        """
        _string = str(number).split('.')
        return len(_string[0])

    def format_decimal_rounding(self, variable):
        """
        Formats the decimal rounding for numbers displayed on the broker notes
        """
        if isinstance(variable, float):
            if self.length_of_number(variable) > 3:
                variable = str(self._get_documentation_parameter('broker_note_number_format')).format(
                                                                                                format_amount(variable))
            else:
                variable = str(self._get_documentation_parameter('broker_note_percentage_format')).format(
                                                                                                format_amount(variable))
        return str(variable)

    def _generate_element_using_dictionary(self, element_name, element_dict=None, ignore_update=False):
        """
        Generates element using dictionary type and applies required formatting to currencies and decimals
        """
        element_text = None

        if not element_dict:
            element_text = ''

        elif isinstance(element_dict, (str, float, int)):
            element_text = element_dict

        elif isinstance(element_dict, dict):
            element_text = element_dict[element_name]
        return self._generate_element(element_name, self.format_decimal_rounding(element_text), ignore_update)

    def security_description(self, request):

        if request.acm_underlying:
            instrument_name = request.acm_underlying.Name()
        else:
            instrument_name = request.acm_instrument.Name()

        if request.instype in [at.INST_BUYSELLBACK, at.INST_REPO_REVERSE, at.INST_FRN, at.INST_COMBINATION]:
            return instrument_name
        else:
            leg = request.acm_instrument.Legs()[0]
        fixed_rate = leg.FixedRate()
        maturity_year = request.acm_instrument.ExpiryDate().split()[0][:4]
        security_description = str(instrument_name) + ' ' + str(fixed_rate) + '% ' + str(maturity_year)
        if fixed_rate == 0:
            return instrument_name
        else:
            return security_description

    def return_calc_value(self, calculation):
        return round(calculation.Value(), 5)

    def clean_price_repo(self, request):
        clean_price = self.trade_sheet_calculations(request)['clean_price_trade']
        dirty_price = self.trade_sheet_calculations(request)['dirty_price_trade']
        accrued_interest = dirty_price - clean_price
        actual_clean_price = request.acm_trade.AllInPrice() - accrued_interest
        return actual_clean_price

    def accrued_interest_combination(self, request):
        top_trade = request.acm_trade
        calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
        accrued_interest = calc_space.CreateCalculation(top_trade, 'Portfolio Traded Interest')
        return accrued_interest.Value()

    def check_population_of_companion_and_spread(self, request):
        """
        Check that if the companion is set on the instrument the companion spread is also set on the trade.
        :param request:
        """
        if request.companion and not request.companion_spread:
            raise ValueError('Instrument specifies a companion, but no companion spread is specified on trade.')
        elif not request.companion and request.companion_spread:
            raise ValueError('Trade specifies a companion spread, but no companion is specified on instrument.')

    def trade_sheet_calculations(self, request):
        top_node = request.calc_space.InsertItem(request.acm_trade)
        accr_int_leg_1_calc = request.calc_space.CreateCalculation(top_node, 'accruedInterestLeg1')
        accr_int_leg_2_calc = request.calc_space.CreateCalculation(top_node, 'accruedInterestLeg2')
        clean_consid_leg_1_calc = request.calc_space.CreateCalculation(top_node, 'cleanConsiderationLeg1')
        clean_consid_leg_2_calc = request.calc_space.CreateCalculation(top_node, 'cleanConsiderationLeg2')
        clean_price_trade_calc = request.calc_space.CreateCalculation(top_node, 'cleanPrice')
        dirty_price_trade_calc = request.calc_space.CreateCalculation(top_node, 'dirtyPrice')
        interest_bonds_frns_calc = request.calc_space.CreateCalculation(top_node, 'Portfolio Traded Interest')

        accr_int_leg_1 = self.return_calc_value(accr_int_leg_1_calc)
        accr_int_leg_2 = self.return_calc_value(accr_int_leg_2_calc)
        clean_consid_leg_1 = self.return_calc_value(clean_consid_leg_1_calc)
        clean_consid_leg_2 = self.return_calc_value(clean_consid_leg_2_calc)
        clean_price_trade = self.return_calc_value(clean_price_trade_calc)
        dirty_price_trade = self.return_calc_value(dirty_price_trade_calc)
        interest_bonds_frns = self.return_calc_value(interest_bonds_frns_calc)
        values = dict()
        values['bond_clean_consid'] = request.acm_trade.Premium()-interest_bonds_frns
        values['accr_int_leg_1'] = accr_int_leg_1
        values['accr_int_leg_2'] = accr_int_leg_2
        values['clean_consid_leg_1'] = clean_consid_leg_1
        values['clean_consid_leg_2'] = clean_consid_leg_2
        values['clean_price_trade'] = clean_price_trade
        values['dirty_price_trade'] = dirty_price_trade
        if request.acm_trade.Quantity() > 0:
            values['interest_bonds_frns'] = interest_bonds_frns * -1
        else:
            values['interest_bonds_frns'] = interest_bonds_frns

        return values

    def build_bsb_data_template(self, request):
        """
        Creates a dictionary of data for buysellback broker notes
        """
        template_dict = dict()
        accr_int_leg_1 = self.trade_sheet_calculations(request)['accr_int_leg_1']
        accr_int_leg_2 = self.trade_sheet_calculations(request)['accr_int_leg_2']
        clean_consid_leg_1 = self.trade_sheet_calculations(request)['clean_consid_leg_1']
        clean_consid_leg_2 = self.trade_sheet_calculations(request)['clean_consid_leg_2']

        premium1 = accr_int_leg_1 + clean_consid_leg_1
        premium2 = accr_int_leg_2 + clean_consid_leg_2

        if request.acm_trade.Quantity() > 0:
            repo_type = 'Buy Sellback'
            template_dict['PURCHASESALE'] = 'Purchase'
            template_dict['BUYER'] = get_party_full_name(request.counterparty)
            template_dict['SELLER'] = self._get_documentation_parameter('broker_note_absa_name')

        else:
            repo_type = 'Sell Buyback'
            template_dict['PURCHASESALE'] = 'Sale'
            template_dict['SELLER'] = get_party_full_name(request.counterparty)
            template_dict['BUYER'] = self._get_documentation_parameter('broker_note_absa_name')

        template_dict['HEAD'] = repo_type + ' Transaction Notification'
        template_dict['ISIN'] = request.acm_underlying.Isin()
        template_dict['MATURITYDATE'] = request.acm_instrument.ExpiryDateOnly()
        template_dict['CURRENCY'] = request.currency
        template_dict['SECURITYDESCR'] = self.security_description(request)
        template_dict['UNEXCORCODE'] = request.unexcor_code
        template_dict['HOSTID'] = request.counterparty.HostId()
        template_dict['TRADEDATE'] = self.format_date(request.acm_trade.ExecutionTime())
        template_dict['TRADENO'] = request.acm_trade.Oid()
        template_dict['NOMAMOUNT'] = formnum(abs(request.acm_trade.Nominal()))
        template_dict['REPORATE'] = request.acm_instrument.Rate()
        template_dict['DEALDATE'] = request.acm_trade.TradeTime()
        template_dict['SETTDATELEG1'] = self.format_date(request.acm_trade.ValueDay())
        template_dict['SETTDATELEG2'] = self.format_date(request.acm_instrument.ExpiryDateOnly())
        template_dict['YTMLEG1'] = request.acm_trade.Price()
        template_dict['YTMLEG2'] = request.acm_instrument.RefPrice()
        template_dict['CLEANPRICELEG1'] = formnum(abs((clean_consid_leg_1 / request.acm_trade.Nominal()) * 100))
        template_dict['CLEANPRICELEG2'] = formnum(abs((clean_consid_leg_2 / request.acm_trade.Nominal()) * 100))
        template_dict['PREMIUMLEG1'] = formnum(abs(premium1))
        template_dict['PREMIUMLEG2'] = formnum(abs(premium2))
        template_dict['INTEREST'] = formnum(abs(premium1 + premium2))
        template_dict['CUSTODIANBIC'] = request.custodian_bic
        template_dict['CUSTODIANSCRIP'] = request.custodian_scrip
        template_dict['CUSTODIANCASH'] = request.custodian_cash
        template_dict['MEMBERCODE'] = request.acquirer_unexcore_code
        template_dict['PSET'] = request.PSET
        return template_dict

    def build_repo_data_template(self, request):
        """
        Creates a dictionary of data for repo broker notes
        """
        template_dict = dict()
        premium1 = self.trade_sheet_calculations(request)['accr_int_leg_1']
        premium2 = self.trade_sheet_calculations(request)['accr_int_leg_2']

        if request.acm_trade.Quantity() > 0:
            repo_type = 'Reverse Repo'
            template_dict['PURCHASESALE'] = 'Purchase'
            template_dict['BUYER'] = self._get_documentation_parameter('broker_note_absa_name')
            template_dict['SELLER'] = get_party_full_name(request.counterparty)

        else:
            repo_type = 'Repo'
            template_dict['PURCHASESALE'] = 'Sale'
            template_dict['SELLER'] = self._get_documentation_parameter('broker_note_absa_name')
            template_dict['BUYER'] = get_party_full_name(request.counterparty)

        template_dict['HEAD'] = repo_type + ' Transaction Notification'
        template_dict['ISIN'] = request.acm_underlying.Isin()
        template_dict['MATURITYDATE'] = self.format_date(request.acm_instrument.ExpiryDateOnly())
        template_dict['CURRENCY'] = request.currency
        template_dict['SECURITYDESCR'] = self.security_description(request)
        template_dict['UNEXCORCODE'] = request.unexcor_code
        template_dict['HOSTID'] = request.counterparty.HostId()
        template_dict['TRADEDATE'] = self.format_date(request.acm_trade.ExecutionTime())
        template_dict['TRADENO'] = request.acm_trade.Oid()
        template_dict['NOMAMOUNT'] = formnum(abs(request.acm_instrument.RefValue() * request.acm_trade.Quantity()))
        template_dict['REPORATE'] = request.acm_instrument.Legs()[0].FixedRate()
        template_dict['DEALDATE'] = self.format_date(request.acm_trade.TradeTime())
        template_dict['SETTDATELEG1'] = self.format_date(request.acm_trade.ValueDay())
        template_dict['SETTDATELEG2'] = self.format_date(request.acm_instrument.ExpiryDateOnly())
        template_dict['YTMLEG1'] = abs(request.acm_instrument.RefPrice())
        template_dict['YTMLEG2'] = 0.0
        template_dict['CLEANPRICELEG1'] = formnum(abs(self.clean_price_repo(request)))
        template_dict['CLEANPRICELEG2'] = 0.0
        template_dict['PREMIUMLEG1'] = formnum(abs(premium1))
        template_dict['PREMIUMLEG2'] = formnum(abs(premium2))
        template_dict['INTEREST'] = formnum(abs(premium1 + premium2))
        template_dict['CUSTODIANBIC'] = request.custodian_bic
        template_dict['CUSTODIANSCRIP'] = request.custodian_scrip
        template_dict['CUSTODIANCASH'] = request.custodian_cash
        template_dict['COMPANION'] = request.companion if request.companion else ""

        companion_spread = ""
        if request.companion_spread and len(str(request.companion_spread)) <= 3:
            companion_spread = "{0:.2f}".format(float(request.companion_spread))
        elif request.companion_spread:
            companion_spread = "{0:.8g}".format(float(request.companion_spread))

        template_dict['COMPANIONSPREAD'] = companion_spread
        template_dict['MEMBERCODE'] = request.acquirer_unexcore_code
        template_dict['PSET'] = request.PSET
        return template_dict

    def build_bond_data_template(self, request):
        """
        Creates a dictionary of data for bond broker notes
        """
        template_dict = dict()

        self.check_population_of_companion_and_spread(request)

        if request.acm_trade.Bought():
            template_dict['PURCHASESALE'] = 'Purchase'
            template_dict['BUYER'] = self._get_documentation_parameter('broker_note_absa_name')
            template_dict['SELLER'] = get_party_full_name(request.counterparty)

        else:
            template_dict['PURCHASESALE'] = 'Sale'
            template_dict['SELLER'] = self._get_documentation_parameter('broker_note_absa_name')
            template_dict['BUYER'] = get_party_full_name(request.counterparty)

        template_dict['HEAD'] = 'Bond' + ' Transaction Notification'
        template_dict['ISIN'] = request.acm_instrument.Isin()
        template_dict['ISSUER'] = request.acm_instrument.Issuer().Name()
        template_dict['MATURITYDATE'] = self.format_date(request.acm_instrument.ExpiryDateOnly())
        template_dict['CURRENCY'] = request.currency
        template_dict['SECURITYDESCR'] = self.security_description(request)
        template_dict['UNEXCORCODE'] = request.unexcor_code
        template_dict['HOSTID'] = request.counterparty.HostId()
        template_dict['TRADEDATE'] = self.format_date(request.acm_trade.ExecutionTime())
        template_dict['TRADENO'] = request.acm_trade.Oid()
        template_dict['SETTLEDATE'] = self.format_date(request.settlement_date)
        template_dict['NOMAMOUNT'] = formnum(abs(request.acm_trade.Nominal()))
        template_dict['PRICE'] = abs(request.acm_trade.Price())
        template_dict['CLEANPRICE'] = abs(self.trade_sheet_calculations(request)['clean_price_trade'])
        template_dict['INTEREST'] = formnum(self.trade_sheet_calculations(request)['interest_bonds_frns'])
        template_dict['CUSTODIANBIC'] = request.custodian_bic
        template_dict['CUSTODIANSCRIP'] = request.custodian_scrip
        template_dict['CUSTODIANCASH'] = request.custodian_cash

        # We only populate the companion and companion spread fields for Corporate issued bonds
        companion_spread = ""
        if request.companion_spread and len(str(request.companion_spread)) <= 3:
            companion_spread = "{0:.2f}".format(float(request.companion_spread))
        elif request.companion_spread:
            companion_spread = "{0:.8g}".format(float(request.companion_spread))
        template_dict['COMPANION'] = request.companion if request.companion else ""
        template_dict['COMPANIONSPREAD'] = companion_spread

        template_dict['MEMBERCODE'] = request.acquirer_unexcore_code
        template_dict['CLEANCONSIDERATION'] = formnum(abs(self.trade_sheet_calculations(request)['bond_clean_consid']))
        template_dict['CONSIDERATION'] = formnum(abs(request.acm_trade.Premium()))
        template_dict['PSET'] = request.PSET
        return template_dict

    def build_frn_data_template(self, request):
        """
        Creates a dictionary of data for FRN broker notes
        """
        template_dict = dict()
        self.check_population_of_companion_and_spread(request)

        if request.acm_trade.Bought():
            template_dict['PURCHASESALE'] = 'Purchase'
            template_dict['BUYER'] = self._get_documentation_parameter('broker_note_absa_name')
            template_dict['SELLER'] = get_party_full_name(request.counterparty)

        else:
            template_dict['PURCHASESALE'] = 'Sale'
            template_dict['SELLER'] = self._get_documentation_parameter('broker_note_absa_name')
            template_dict['BUYER'] = get_party_full_name(request.counterparty)

        template_dict['HEAD'] = 'FRN' + ' Transaction Notification'
        template_dict['ISIN'] = request.acm_instrument.Isin()
        template_dict['ISSUER'] = request.acm_instrument.Issuer().Name()
        template_dict['MATURITYDATE'] = self.format_date(request.acm_instrument.ExpiryDateOnly())
        template_dict['CURRENCY'] = request.currency
        template_dict['SECURITYDESCR'] = self.security_description(request)
        template_dict['UNEXCORCODE'] = request.unexcor_code
        template_dict['HOSTID'] = request.counterparty.HostId()
        template_dict['TRADEDATE'] = self.format_date(request.acm_trade.ExecutionTime())
        template_dict['TRADENO'] = request.acm_trade.Oid()
        template_dict['SETTLEDATE'] = self.format_date(request.settlement_date)
        template_dict['NOMAMOUNT'] = formnum(abs(request.acm_trade.Nominal()))
        template_dict['PRICE'] = abs(request.acm_trade.Price())
        template_dict['CLEANPRICE'] = abs(self.trade_sheet_calculations(request)['clean_price_trade'])
        template_dict['INTEREST'] = formnum(self.trade_sheet_calculations(request)['interest_bonds_frns'])
        template_dict['CUSTODIANBIC'] = request.custodian_bic
        template_dict['CUSTODIANSCRIP'] = request.custodian_scrip
        template_dict['CUSTODIANCASH'] = request.custodian_cash
        template_dict['COMPANION'] = request.companion if request.companion else ""

        companion_spread = ""
        if request.companion_spread and len(str(request.companion_spread)) <= 3:
            companion_spread = "{0:.2f}".format(float(request.companion_spread))
        elif request.companion_spread:
            companion_spread = "{0:.8g}".format(float(request.companion_spread))

        template_dict['COMPANIONSPREAD'] = companion_spread
        template_dict['MEMBERCODE'] = request.acquirer_unexcore_code
        template_dict['CONSIDERATION'] = formnum(abs(request.acm_trade.Premium()))
        template_dict['PSET'] = request.PSET
        return template_dict

    def build_combination_data_template(self, request):
        """
        Creates a dictionary of data for Combination broker notes
        """
        template_dict = dict()
        self.check_population_of_companion_and_spread(request)

        if request.acm_trade.Bought():
            template_dict['PURCHASESALE'] = 'Purchase'
            template_dict['BUYER'] = self._get_documentation_parameter('broker_note_absa_name')
            template_dict['SELLER'] = get_party_full_name(request.counterparty)

        else:
            template_dict['PURCHASESALE'] = 'Sale'
            template_dict['SELLER'] = self._get_documentation_parameter('broker_note_absa_name')
            template_dict['BUYER'] = get_party_full_name(request.counterparty)

        template_dict['HEAD'] = 'Combination' + ' Transaction Notification'
        template_dict['ISIN'] = request.acm_instrument.Isin()[0:12]
        template_dict['ISSUER'] = request.acm_instrument.Issuer().Name()
        template_dict['CURRENCY'] = request.currency
        template_dict['SECURITYDESCR'] = request.acm_instrument.ExternalId1()[0:6]
        template_dict['UNEXCORCODE'] = request.unexcor_code
        template_dict['HOSTID'] = request.counterparty.HostId()
        template_dict['TRADEDATE'] = self.format_date(request.acm_trade.ExecutionTime())
        template_dict['TRADENO'] = request.acm_trade.Oid()
        template_dict['SETTLEDATE'] = self.format_date(request.settlement_date)
        template_dict['NOMAMOUNT'] = formnum(abs(request.acm_trade.Nominal()))
        template_dict['PRICE'] = abs(request.acm_trade.Price())
        template_dict['INTEREST'] = abs(round(self.accrued_interest_combination(request), 5))
        template_dict['CUSTODIANBIC'] = request.custodian_bic
        template_dict['CUSTODIANSCRIP'] = request.custodian_scrip
        template_dict['CUSTODIANCASH'] = request.custodian_cash
        template_dict['COMPANION'] = request.companion if request.companion else ""

        companion_spread = ""
        if request.companion_spread:
            companion_spread = "{0:.8g}".format(float(request.companion_spread))

        template_dict['COMPANIONSPREAD'] = companion_spread
        template_dict['MEMBERCODE'] = request.acquirer_unexcore_code
        template_dict['CONSIDERATION'] = formnum(abs(request.acm_trade.Premium()))
        template_dict['PSET'] = request.PSET
        return template_dict

    def clear_memory(self, request):
        """
        Clear memory after using a calculation space
        """
        request.calc_space.Clear()
        acm.Calculations().ResetEvaluatorBuilders()
        acm.Memory().GcWorldStoppedCollect()

    def _generate_document_specific_element(self, request):
        """
        Generates XML element specific to broker notes
        """
        if request.instype in [at.INST_BOND, at.INST_INDEXLINKED_BOND]:
            template_dict = self.build_bond_data_template(request)
            return self.convert_broker_data_to_xml(template_dict, request)

        elif request.instype == at.INST_FRN:
            template_dict = self.build_frn_data_template(request)
            return self.convert_broker_data_to_xml(template_dict, request)

        elif request.instype == at.INST_BUYSELLBACK:
            template_dict = self.build_bsb_data_template(request)
            return self.convert_broker_data_to_xml(template_dict, request)

        elif request.instype == at.INST_REPO_REVERSE:
            template_dict = self.build_repo_data_template(request)
            return self.convert_broker_data_to_xml(template_dict, request)

        elif request.instype == at.INST_COMBINATION:
            template_dict = self.build_combination_data_template(request)
            return self.convert_broker_data_to_xml(template_dict, request)

        raise ValueError("Unsupported instrument type '{instype}' encounter.".format(
            instype=request.instype
        ))

    def _generate_subject_element(self, request):
        """
        Generates the subject XML element
        """
        if request.instype in [at.INST_BOND, at.INST_INDEXLINKED_BOND]:
            return self._generate_element("SUBJECT", at.INST_BOND)

        elif request.instype == at.INST_FRN:
            return self._generate_element("SUBJECT", at.INST_FRN)

        elif request.instype == at.INST_BUYSELLBACK:
            return self._generate_element("SUBJECT", at.INST_BUYSELLBACK)

        elif request.instype == at.INST_REPO_REVERSE:
            return self._generate_element("SUBJECT", at.INST_REPO_REVERSE)

        elif request.instype == at.INST_COMBINATION:
            return self._generate_element("SUBJECT", at.INST_COMBINATION)

        raise ValueError("Unsupported instrument type '{instype}' encounter.".format(
            instype=request.instype
        ))

    def convert_broker_data_to_xml(self, template_dict, request):
        """
        Converts dictionary data to XML
        """
        element = self._generate_element("BROKER_NOTE")

        for xml_header in list(template_dict.keys()):
            element.append(self._generate_element_using_dictionary(xml_header, template_dict))

        element.append(self._generate_element('CUSTODIAN', request.custodian))
        self.clear_memory(request)

        return element
