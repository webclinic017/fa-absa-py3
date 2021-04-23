"""
Business require an automated script to BO confirm specific SBL trades in
certain portfolios with a few validations.

Date            JIRA              Developer               Requester                     Description        
==========      ===========       ==================      ======================        ======================

2013-07-02      ABITFA-1991       Pavel Saparov           Candice Johnson
2014-03-05      ABITFA-1991       Pavel Saparov           Candice Johnson
2014-05-20      ABITFA-2476       Jan Sinkora             Candice Johnson
2015-01-22      ABITFA-2903       Nada Jasikova           Candice Johnson
2015-04-15      ABITFA-3487       Andrei Conicov          Mbongwe Philela
2018-04-10      ABITFA-5315       Ondrej Bahounek         Bishop, Graham: Finance (NYK)
2020-02-26      PCGDEV-10         Sihle Gaxa              James Stevens                 Removed time delay strict rule
                                                                                        since this is an STP process now
2020-04-29      PCGDEV-371        Qaqamba Ntshobane       James Stevens                 Added close out trades auto-bo list
2020-06-10      PCGDEV-454        Qaqamba Ntshobane       James Stevens                 Added buys with SLB ACS Main borrower
2020-07-08      PCGDEV-505        Sihle Gaxa              James Stevens                 Added SBL principal legs and Deutsche
                                                                                        London bank to VAT restricted clients
2020-08-20      PCGDEV-567        Sihle Gaxa              James Stevens                 Excluded closing trades from mirror checks
"""
# core libs
import csv
from collections import namedtuple
from datetime import datetime
from time import mktime

# arena libs
import acm
import at
from auto_confirm import AutoConfirmation
from at_ael_variables import AelVariableHandler


class PCGAutoConfirmation(AutoConfirmation):

    # move trades to BO-Confirmed state
    state = at.TS_BO_CONFIRMED
    vat_restricted_borrowers = ['SLB BARCAP SEC',
                                'SLB GOLDMAN SACHS INTERNATIONAL',
                                'SLB MERRIL LYNCH INTERNATIONAL',
                                'SLB DEUTSCHE BANK LONDON']

    vat_restricted_funders = ['SLL BARCAP SEC',
                              'SLL GOLDMAN SACHS INTERNATIONAL',
                              'SLB MERRIL LYNCH INTERNATIONAL',
                              'SLL DEUTSCHE BANK LONDON']

    absa_lenders = ['SLL ABSA SECURITIES LENDING', 'SLL PRINCIPAL ACCOUNT']
    absa_borrowers = ['SLB ABSA SECURITIES LENDING', 'SLB PRINCIPAL ACCOUNT']


    def verify(self, trade):
        """Method verifies if Trade is suitable to be automatically BO-Confirmed
        depending on defined internal rules by PCG SBL department.
        """

        self.trade = trade
        self.portfolio = trade.Portfolio().Name()
        self.counterparty = trade.Counterparty().Name()
        self.acquirer = trade.Acquirer().Name()
        self.security_name = trade.Instrument().Security().Name()
        self.security_type = trade.Instrument().Security().InsType()
        self.borrower = trade.AdditionalInfo().SL_G1Counterparty1()
        self.funder = trade.AdditionalInfo().SL_G1Counterparty2()
        self.sl_vat = trade.Instrument().AdditionalInfo().SL_VAT()
        self.fixed_rate = trade.Instrument().Legs()[0].FixedRate()
        self.sl_g1fee = trade.AdditionalInfo().SL_G1Fee2()
        self.mirror = trade.GetMirrorTrade()
        self.trade_qty = trade.Quantity()
        self.trade_type = trade.Type()
        self.trade_purpose = trade.Text1()

        super(PCGAutoConfirmation, self).verify(trade)

    def generate_audit(self, output_path):
        """Generates CSV audit error file for business users."""

        audit_columns = (
            'TradeNumber', 'ConnectedRef', 'StartDate', 'EndDate',
            'AgeingFromStart', 'Error', 'Portfolio', 'SecurityType',
            'SecurityName', 'G1Borrower', 'G1Lender', 'Acquirer',
            'Counterparty', 'Quantity', 'VAT', 'G1Fee', 'FAFee'
        )
        audit_row = namedtuple('AuditRow', ','.join(audit_columns))
        acm_time = acm.Time()

        writer = csv.writer(open(output_path, "wb"), dialect='excel', delimiter=',')
        writer.writerow(audit_columns)

        for trade, bo_error in self.errors.items():
            data = {}
            data['TradeNumber'] = trade.Oid()
            data['ConnectedRef'] = trade.ConnectedTrade().Oid()
            data['StartDate'] = trade.Instrument().StartDate()
            data['EndDate'] = trade.Instrument().EndDate()
            data['AgeingFromStart'] = acm_time.DateDifference(acm_time.DateToday(), data['StartDate'])
            data['Error'] = bo_error
            data['Portfolio'] = trade.Portfolio().Name()
            data['SecurityType'] = trade.Instrument().Security().InsType()
            data['SecurityName'] = trade.Instrument().Security().Name()
            data['G1Borrower'] = trade.AdditionalInfo().SL_G1Counterparty1()
            data['G1Lender'] = trade.AdditionalInfo().SL_G1Counterparty2()
            data['Acquirer'] = trade.Acquirer().Name()
            data['Counterparty'] = trade.Counterparty().Name()
            data['Quantity'] = round(trade.FaceValue())
            data['VAT'] = trade.Instrument().AdditionalInfo().SL_VAT()
            data['G1Fee'] = trade.AdditionalInfo().SL_G1Fee2()
            data['FAFee'] = trade.Instrument().Legs()[0].FixedRate()

            writer.writerow(audit_row(**data))

        print "Output written to {0}".format(output_path)


    def __strict_rule_1(self, trade):
        """Don't confirm if fees are different."""

        if (self.borrower and self.funder and self.sl_g1fee
            and len(self.borrower) > 0 and len(self.funder) > 0
            and abs(self.fixed_rate - self.sl_g1fee) > 0.01):
                raise UserWarning('G1 lender does not equal FA fee')

    def __strict_rule_2(self, trade):
        """Don't confirm if borrower do not start with SLB."""

        if (self.borrower
            and len(self.borrower) > 0
            and not self.borrower.startswith('SLB')):
                raise UserWarning('Borrower is not starting with SLB')

    def __strict_rule_3(self, trade):
        """Don't confirm if lender do not start with SLL."""

        if (self.funder
            and len(self.funder) > 0
            and not self.funder.startswith('SLL')):
                raise UserWarning('Funder is not starting with SLL')

    def __strict_rule_4(self, trade):
        """Don't BO Confirm trade in MM funding portfolios and dormant portfolios"""

        exclude_portfolios = ('SBL_Fee', 'Call_SBL_Collateral', 'Call_SBL_Fixed Income',
                              'new_SL Term Trades', 'new_Reserved_Stock',
                              'new_Equity Script Lending', 'New_CFD', 'SL_Satu',
                              'SBL Prime Client 1 Loans', 'Delta One_MTN')

        if self.portfolio in exclude_portfolios:
            raise UserWarning('Trade located in MM funding/dormant portfolio')

    def __soft_rule_1(self, trade):
        """Confirm Bond Portfolios on Pension Fund Structure."""

        if self.portfolio in ('SBL_Fixed Income DBR',
                              'SBL_Fixed Income Denel',
                              'SBL_Fixed Income Denel RF',
                              'SBL_Fixed Income National Tertiary RF',
                              'SBL_Fixed Income UPT',
                              'SBL_Fixed Income_ Unisa',
                              'SBL_Fixed Income_ University Free State',
                              'SBL_Fixed Income_De Beers',
                              'SBL_MAPPS_Bonds'):

            self.check(self.counterparty == 'SBL AGENCY I/DESK',
                  'Incorrect Ctpy for Bond Portfolios on Pension Fund Structure')

            self.check((self.mirror and self.trade.CounterPortfolio().Name() == 'SBL_Agency_Bond') or
                        self.trade_type == "Closing",
                        'Incorrect CP portfolio')

            self.check(self.counterparty != self.acquirer,
                  'Counterparty equal to acquirer')

            self.check(self.security_type in (at.INST_BOND, at.INST_INDEXLINKED_BOND),
                  'Invalid security type for Pension Fund Structure')

            allowed_borrowers = ('SLB ABCAP DERIVATIVES STRUCT BOND EXTE',
                                 'SLB ABCAP DERIVATIVES STRUCT BOND INTE',
                                 'SLB ABCAP FI DE BEERS B INTERNAL',
                                 'SLB ABCAP FI DENEL PF INTERNAL',
                                 'SLB ABCAP FI DENEL RF INTERNAL',
                                 'SLB ABCAP FI NATIONAL TERTIARY RF INTER',
                                 'SLB ABCAP FI UNISA RF INTERNAL',
                                 'SLB ABCAP FI UNIV OF FREE STATE PF INTE',
                                 'SLB ABCAP FI UPT INTERNAL',
                                 'SLB REPO DESK STRUCTURED EXTERNAL',
                                 'SLB ABCAP FI DENEL PF EXTERNAL',
                                 'SLB ABCAP FI DENEL PF EXTERNAL',
                                 'SLB ABCAP FI DENEL RF EXTERNAL',
                                 'SLB ABCAP FI NATIONAL TERTIARY RF EXTER',
                                 'SLB ABCAP FI UNIV OF FREE STATE PF EXTE',
                                 'SLB ABCAP FI UNISA RF EXTERNAL',
                                 'SLB ABCAP FI UPT EXTERNAL',
                                 'SLB ABCAP FI DE BEERS B EXTERNAL')

            allowed_funders = ('SLL ABCAP DERIVATIVES STRUCT BOND EXTE',
                               'SLL ABCAP DERIVATIVES STRUCT BOND INTE',
                               'SLL REPO DESK STRUCTURED EXTERNAL')

            self.check(
                self.borrower in self.absa_borrowers
                or self.funder in self.absa_lenders
                or self.borrower in allowed_borrowers or self.funder in allowed_funders,
                'Wrong G1 ctpy'
            )

            self.check(self.borrower in self.absa_borrowers and self.trade_qty < 0
                  or self.funder in self.absa_lenders and self.trade_qty > 0,
                  'Position incorrect direction')

            self.check(self.sl_vat is False,
                  'VAT charged on internal')

            return True

    def __soft_rule_2(self, trade):
        """Confirm specific Stock Portfolios."""

        if self.portfolio == 'ACS - Script Lending':

            self.check(self.counterparty == 'SBL AGENCY I/DESK',
                  'Incorrect ctpy for Stock Portfolios')

            if self.mirror:
                self.check(self.trade.CounterPortfolio().Name() == 'SBL_Accrued_1',
                  'Incorrect CP portfolio')

            self.check(self.counterparty != self.acquirer,
                  'Counterparty equal to Acquirer')

            self.check(self.security_type in (at.INST_STOCK, at.INST_ETF),
                  'Invalid security type for Stock Portfolios - only Stocks and ETFs')

            allowed_borrowers = ('SLB ACS CFD',
                                 'SLB ACS Delta Structure',
                                 'SLB ACS LOCAL CFD',
                                 'SLB ACS MAIN',
                                 'SLB ACS MAIN PTH',
                                 'SLB ACS OVLAND WEALTH 1',
                                 'SLB ACS OVLAND WEALTH 2',
                                 'SLB ACS PTH',
                                 'SLB ACS STRUCTURED 2',
                                 'SLB ACS STRUCTURED 3',
                                 'SLB ACS STRUCTURED 4',
                                 )

            allowed_funders = ('SLL ACS LENDER', 
                               'SLL ACS LENDER PTH',
                               'SLL TITAN SHARE DEALERS ACCOUNT 2',
                               )

            self.check(
                self.borrower in self.absa_borrowers
                or self.funder in self.absa_lenders
                or self.borrower in allowed_borrowers or self.funder in allowed_funders,
                'Wrong G1 ctpy'
            )

            self.check(self.borrower in self.absa_borrowers and self.trade_qty < 0
                  or self.funder in self.absa_lenders and self.trade_qty > 0
                  or self.borrower == 'SLB ACS MAIN' and self.trade_qty > 0,
                  'Position incorrect direction')

            self.check(self.sl_vat is True,
                  'VAT not charged on ACS')

            if self.trade_purpose in ['PARTIAL_RETURN', 'FULL_RETURN']:
                self.check(self.trade_type in ['Normal', 'Closing'],
                    'Invalid trade type')
            return True

    def __soft_rule_3(self, trade):
        """Confirm Prime Broker Trades."""

        if self.portfolio == 'SBL - Prime Clients':

            self.check(self.counterparty == 'SBL AGENCY I/DESK',
                  'Incorrect ctpy SBL Prime Clients')

            self.check((self.mirror and self.trade.CounterPortfolio().Name() == 'SBL_Agency_Prime_Broker') or
                        self.trade_type == "Closing",
                        'Incorrect CP portfolio')

            self.check(self.counterparty != self.acquirer,
                  'Counterparty equal to Acquirer')

            allowed_borrowers = ('SLB ABCAP PB COGITSO',
                                  'SLB NITROGEN FT',
                                  'SLB MAP 290',
                                  'SLB MAP 501',
                                  'SLB SA ALPHA SPC CLASS V',
                                  'SLB NITROGEN FIRE',
                                  'SLB NITROGEN SKY')

            self.check(self.funder in self.absa_lenders
                  and self.borrower in allowed_borrowers,
                  'Wrong G1 ctpy')

            self.check(self.trade_qty > 0,
                  'Position incorrect direction')

            self.check(self.sl_vat is False,
                  'VAT charged on internal')

            return True

    def __soft_rule_4(self, trade):
        """Confirm LEIPS Structure"""

        if self.portfolio == 'SL_LEIPS':

            self.check(self.counterparty == 'SBL AGENCY I/DESK',
                 'Incorrect ctpy LEIPS Structure')

            self.check((self.mirror and self.trade.CounterPortfolio().Name() == 'SBL_Accrued_1') or
                        self.trade_type == "Closing",
                        'Incorrect CP portfolio')

            self.check(self.counterparty != self.acquirer,
                  'Counterparty equal to Acquirer')

            self.check(self.security_name in ('ZAR/AGL', 'ZAR/SAB'),
                  'AGLs and SABs only')

            self.check(self.funder in self.absa_lenders
                  and self.borrower == 'SLB ACS STRUCTURED 2',
                  'Wrong G1 ctpy')

            self.check(self.trade_qty > 0,
                  'Position incorrect direction')

            self.check(self.sl_vat is True,
                  'VAT not charged')

            return True

    def __soft_rule_5(self, trade):
        """Confirm Structured Repo Trades."""

        if self.portfolio == 'SBL_Structured Repo':

            self.check(self.counterparty == 'SBL AGENCY I/DESK',
                  'Incorrect ctpy Structured Repo Trades')

            self.check((self.mirror and self.trade.CounterPortfolio().Name() == 'SBL_Agency_Bond') or
                        self.trade_type == "Closing",
                        'Incorrect CP portfolio')

            self.check(self.counterparty != self.acquirer,
                  'Counterparty equal to Acquirer')

            self.check(self.security_type in (at.INST_BOND, at.INST_INDEXLINKED_BOND),
                  'Invalid security type for Structured Repo Trades')

            allowed_borrowers = ('SLB REPO DESK STRUCTURED EXTERNAL',
                                 'SLB REPO DESK STRUCTURED INTERNAL')

            allowed_funders = ('SLL ABCAP DERIVATIVES STRUCT BOND EXTE',
                               'SLL ABCAP DERIVATIVES STRUCT BOND INTE',
                               'SLL TRESC LENDER')

            self.check((self.borrower in self.absa_borrowers
                    or self.funder in self.absa_lenders)
                  and (self.borrower in allowed_borrowers or self.funder in allowed_funders),
                  'Wrong G1 ctpy')

            self.check(self.borrower in self.absa_borrowers and self.trade_qty < 0
                  or self.funder in self.absa_lenders and self.trade_qty > 0,
                  'Position incorrect direction')

            self.check(self.sl_vat is False,
                  'VAT charged on internal')

            return True

    def __soft_rule_6(self, trade):
        """Confirm MAPPs Growth Trades."""

        if self.portfolio == 'Bond - Script Lending':

            self.check(self.counterparty == 'SBL AGENCY I/DESK',
                 'Incorrect ctpy for MAPPs Growth Trades')

            self.check((self.mirror and self.trade.CounterPortfolio().Name() == 'SBL_Agency Bonds ETF') or
                        self.trade_type == "Closing",
                        'Incorrect CP portfolio')

            self.check(self.counterparty != self.acquirer,
                  'Counterparty equal to Acquirer')

            self.check(self.security_type in (at.INST_BOND, at.INST_INDEXLINKED_BOND),
                 'Invalid security type for MAPPs Growth Trades')

            self.check(self.borrower in self.absa_borrowers
                    and self.funder == 'SLL TRESC LENDER'
                  or self.borrower == 'SLB ABCAP MAPPS ETF GROWTH PRTF'
                    and self.funder in self.absa_lenders,
                  'Wrong G1 ctpy')

            self.check(self.borrower in self.absa_borrowers and self.trade_qty < 0
                  or self.funder in self.absa_lenders and self.trade_qty > 0,
                  'Position incorrect direction')

            self.check(self.sl_vat is False,
                  'VAT charged on internal')

            return True

    def __soft_rule_7(self, trade):
        """Confirm SBL Agency Trades."""

        if self.portfolio == 'SBL Agency':
        
            if (self.borrower in self.absa_borrowers
                    or self.funder in self.absa_lenders):
                self.check(self.borrower in self.absa_borrowers and self.trade_qty > 0
                    or self.funder in self.absa_lenders and self.trade_qty < 0,
                    'Position incorrect direction')

            if ((self.borrower == 'SLB TRESC BORROWER'
                    or self.funder in self.absa_lenders)
                and self.security_type in (at.INST_BOND, at.INST_INDEXLINKED_BOND)
                and self.sl_vat is False):
                    return True
            else:
                error_message = 'TRESC is bonds only, VAT charged on non-vendor'

            if ((self.borrower in self.absa_borrowers
                    or self.funder == 'SLL ABCAP MARKETS AND TRADING ETF')
                and self.security_type == at.INST_ETF
                and self.sl_vat is False):
                    return True
            else:
                error_message = 'NEWETF is ETFs only, VAT not charged on vendor'

            if ((self.borrower in self.vat_restricted_borrowers
                 or self.funder in self.vat_restricted_funders)
                    and self.sl_vat is False):
                    return True
            else:
                error_message = 'VAT charged on non-vendor'

            if ((self.borrower not in self.vat_restricted_borrowers
                 or self.funder not in self.vat_restricted_funders)
                    and self.sl_vat is True):
                    return True
            else:
                error_message = 'VAT not charged on vendor'

            raise UserWarning(error_message)

    def __soft_rule_8(self, trade):
        """Confirm OMSFIN Trades."""

        if self.portfolio == 'SBL_CFD_Old Mutual':

            self.check(self.counterparty == 'SBL AGENCY I/DESK',
                  'Incorrect ctpy for OMSFIN Trades')

            self.check((self.mirror
                  and self.trade.CounterPortfolio().Name() == 'SBL_Agency_OmsfinCFD') or self.trade_type == "Closing",
                  'Incorrect CP portfolio')

            self.check(self.counterparty != self.acquirer,
                  'Counterparty equal to Acquirer')

            self.check(self.security_type == at.INST_STOCK,
                  'Invalid security type for OMSFIN trades')

            self.check(self.borrower == 'SLB ACS LOCAL CFD'
                  and self.funder in self.absa_lenders,
                  'Wrong G1 ctpy')

            self.check(self.trade_qty > 0,
                  'Position incorrect direction')

            self.check((self.sl_g1fee, self.fixed_rate) == (0.0, 0.0),
                  'Fee not zero')

            self.check(self.sl_vat is True,
                  'VAT not charged on vendor')

            return True

    def __soft_rule_9(self, trade):
        """Confirm SL Structured Deals."""

        if self.portfolio == 'new_SL Structured Deals':

            self.check(self.security_type == at.INST_STOCK,
                  'Stock portfolio only')

            self.check(self.borrower == 'SLB ACS OVLAND WEALTH 1'
                  and self.funder in self.absa_lenders,
                  'Wrong G1 ctype')

            self.check(self.trade_qty > 0,
                  'Position incorrect direction')

            self.check(self.sl_vat is True,
                  'VAT charged not charged on ACS')

            return True

    def __soft_rule_10(self, trade):
        """Confirm Interdesk Trades."""

        allowed_parties = ['BOND DESK', 'EQ Derivatives Desk', 'IRD DESK',
                           'Money Market Desk', 'STRUCT NOTES DESK',
                           'PRIME SERVICES DESK', 'SECURITY LENDINGS DESK',
                           'SYNDICATE TRADING']

        bond_portfolios = ['Bond - Script Lending', 'SBL_Fixed Income DBR',
                           'SBL_Fixed Income Denel', 'SBL_Fixed Income Denel RF',
                           'SBL_Fixed Income National Tertiary RF',
                           'SBL_Fixed Income UPT', 'SBL_Fixed Income_ Unisa',
                           'SBL_Fixed Income_ University Free State',
                           'SBL - Prime Clients', 'SBL_Structured Repo',
                           'SBL_Fixed Income_De Beers', 'SBL_MAPPS_Bonds']

        stock_portfolios = ['SBL - Prime Clients', 'ACS - Script Lending',
                            'SBL_CFD_Old Mutual', 'SL_LEIPS', 'SBL_Accrued_1',
                            'Collateral optimize']

        # SBL specification of internal trade
        is_internal = self.borrower is None or self.funder is None

        # Process only internal trades
        if is_internal:

            #self.check(self.portfolio in (bond_portfolios + stock_portfolios),
            #      'Internal trade not in correct portfolio')

            self.check(self.counterparty in allowed_parties,
                  'Counterparty for Interdesk Trades is not allowed')

            self.check(self.mirror or
                       self.trade_type == "Closing",
                       'No mirror trade')

            self.check(self.counterparty != self.acquirer,
                  'Counterparty is same as Acquirer')

            if (self.security_type in (at.INST_BOND, at.INST_INDEXLINKED_BOND)
                and self.portfolio in bond_portfolios):

                    self.check(self.sl_vat is False, 'VAT charged on internal')
                    return True

            elif (self.security_type in (at.INST_STOCK, at.INST_ETF)
                  and self.portfolio in stock_portfolios):

                if self.portfolio == 'SBL - Prime Clients':

                    self.check(self.sl_vat is False,
                          'VAT charged on internal')
                    return True

                elif (self.portfolio == 'SBL_CFD_Old Mutual'
                      and self.security_type == at.INST_STOCK):

                    self.check(self.sl_vat is False,
                          'VAT charged on internal')
                    return True

                elif (self.portfolio == 'SL_LEIPS'
                      and self.security_name == 'ZAR/AGL'):

                    self.check(self.sl_vat is False,
                          'VAT charged on internal')
                    return True

                elif self.portfolio in ('ACS - Script Lending', 'SBL_Accrued_1'):
                    return True

                else:
                    self.check(self.sl_vat is False, 'VAT charged on internal')
                    return True
            else:
                raise UserWarning('Invalid security type for Interdesk Trades')


def enable_audit(selected_var):
    """hook"""
    output_path = ael_variables.get('output_path')
    output_path.enabled = True if int(selected_var.value) else False

ael_gui_parameters = {'windowCaption': 'PCG SBL Autoconfirm FO Trades'}

ael_variables = AelVariableHandler()

ael_variables.add('trade_filter',
                  label='Trade Filter',
                  alt='Trade filter that will be used to filter trades for automatic BO-Confirmation',
                  cls='FTradeSelection',
                  collection=sorted([f.Name() for f in acm.FTradeSelection.Select("")]),
                  default='Default TF')
ael_variables.add('is_audit',
                  label='Perform audit',
                  alt='Perform audit action to obtain remaining trades pending for BO-Confirmation',
                  cls='int',
                  collection=[0, 1],
                  default=0,
                  mandatory=False,
                  hook=enable_audit)

ael_variables.add('output_path',
                  label='Output path',
                  mandatory=False,
                  enabled=True)

def ael_main(params):

    print "Executing {0}".format(__name__)

    tf = params['trade_filter']

    # convert and copy from FPersistentSet to python list
    candidates = list(tf.Trades().SortByProperty('Oid', False))

    # verify valid trades for confirmation
    sbl_engine = PCGAutoConfirmation(candidates)
    sbl_engine.confirm()

    # generate audit details
    if params['is_audit']:
        sbl_engine.generate_audit(params['output_path'])

    # print the errors
    sbl_engine.print_errors()

    print "Completed successfully"
