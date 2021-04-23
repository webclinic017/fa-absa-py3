
# Desk   Requester        Developer              CR Number
# What
# =============================================================================
# OPS    Sharon Maynard   Willie van der Bank    C194697 (12/01/2010)
# Generates PDF Audit Certificates

# OPS    Sharon Maynard    Willie / Ickin         C286240 (20/04/2010)
# Update contact info, create dynamic trade filter for shorter
# run time and export folder gets specified as parameter

# OPS    Sharon Maynard   Willie / Ickin         C311669 (18/05/2010)
# Removed dynamic trade filter],[Amended to correctly read trade filter

# OPS    Sharon Maynard   Willie / Ickin         C368883 (13/07/2010)
# Updated contact info

# OPS    Sharon Maynard   Willie / Ickin         C375386 (20/07/2010)
# Updated Nominal to display Original Nominal

# OPS    Sharon Maynard   Willie / Ickin         C416822 (07/09/2010)
# Added Start/End Date

# OPS    Sharon Maynard   Willie / Ickin         C485068 (09/11/2010)
# Corrected indentation error that occured during import of py file

# OPS    Sharon Maynard   Willie / Ickin         C498346 (18/11/2010)
# Corrected the way that Back-dated cashflows are picked up

# OPS    Sharon Maynard   Willie / Ickin         C54688 (14/01/2011)
# Previous fix were causing some cash flows to be excluded

# OPS    Sharon Maynard   Willie / Ickin         C550641 (20/01/11)
# Adapt Audit report to cater for Shariah Clients

# OPS    Sharon Maynard   Willie / Ickin         C666056 (26/05/2011)
# Added Report Date

# OPS    Letitia Carboni  Lukas Paluzga          ABITFA-1795
# New letterhead

# OPS Sipho Ndlalane	Sanele Macanda		CHNG0001662676 - ABITFA -No Jira (23/01/2014)
# Replaced os.startfile() with startFile() see SAGEN_IT_Functions

# OPS Nastasha Adams	Manan Ghosh		CHNG0001741693	- ABITFA-2379 Audit Report generating incorrectly (25/02/2014)
# Included flag to Exclude deposits and also dynamically generate trade filter with the selected counterparty added on to trade filter

# OPS Letitia Roux  Sanele Macanda CHNG0002294380 - ABITFA-2702 Statement information vs audit information not pulling through the same
#information for the client services team. Client Security SPV 2 (18/09/2014)

# OPS Lucille Josephs Sanele Macanda 	 - Audit Certificate Production issue - Not providing complete details (18-11-2014)

# OPS Letitia Roux Bushy Ngwako - CHNG0003225022 - Include all Cashflows from Start Date and Include Non Zar Trades (ABITFA-3416(including ABITFA-3520))

# OPS    Kathleen Rutherfurd    Gabriel Marko          ABITFA-3945
# Update email address on call statements and audit certificates

# OPS    Nicolette Burger    Bhavnisha Sarawan         INC0049749063 - No Jira
# Add the currency for formcurr so that Non ZAR certificates doesn't display as ZAR

# OPS    Nicolette Burger    Cuen Edwards              FAOPS-523
# Quick fix: replaced calculations for deposit trades with call statement functions.
# To be refactored/replaced as tech-debt.

import copy
# import os
# import sys
# import subprocess

import ael
import acm

import at
import STATIC_TEMPLATE
import XMLReport
reload(XMLReport)

from zak_funcs import formcurr
# from FixedRate import getFixedRate  # @UnresolvedImport
from XMLReport import mkcaption, mkinfo, mktable, mkvalues
from SAGEN_IT_Functions import startFile
from SAGEN_IT_TM_Column_Calculation import money_flow_value
from at_time import to_date
import CallStatementGeneral
import CallStatementXMLGenerator
import DocumentGeneral


class PartyMock(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, attr):
        return ''


class Report(XMLReport.StatementReportBase):
    def __init__(self, start, end, shariah, party, tf_name, mm_instype, no_accounts, auditor_address, use_custom_dates=False, excludeDeposit=False):
        self.start = start
        self.end = end
        self.shariah = shariah
        self.mm_instype = mm_instype
        self.no_accounts = no_accounts
        self.party = party  # ael or mock
        self.auditor_address = auditor_address
        self.use_custom_dates = use_custom_dates
        self.excludeDeposit = excludeDeposit

        print "Loading trades, this will take a while..."

        tf = ael.TradeFilter[tf_name]
        query = tf.get_query()
        query.append(('And', '', 'Counterparty', 'equal to', party.ptyid, ''))

        tradefilternew = ael.TradeFilter.new()
        tradefilternew.fltid = 'Audit_Certificate_' + str(party.ptynbr)
        tradefilternew.set_query(query)

        if tradefilternew:
            self.trades = [t for t in tradefilternew.trades()
                           if t.counterparty_ptynbr == party]
                           # ABITFA-3520 - Include Non Zar Trades
        else:
            self.trades = []

        tradefilternew.delete()
        print "...trades loaded."

    def bank_address(self):
        addr = copy.copy(STATIC_TEMPLATE.ADDRESS_TOWERSNORTH)
        addr['name'] = 'Secondary Market Operations'
        addr['tel'] = '+27 (0)11 895 6734 / 3741'
        addr['fax'] = '+27 (0)11 895 7858'
        addr['email'] = 'tmscs@barclayscapital.com'
        return addr

    def client_address(self):
        return self.auditor_address

    def statement_detail(self):
        yield mkcaption('AUDIT CERTIFICATE')

        if self.no_accounts:
            if self.shariah:
                yield mkinfo('We hereby confirm that the below mentioned Transactions were held by ourselves for the abovementioned client for the period as at ' +  self.end.to_string("%d %B %Y")+ '.')
            else:
                yield mkinfo('We hereby confirm that there were no instrument(s) held by ourselves for the abovementioned client for the period as at ' +  self.end.to_string("%d %B %Y")+ '.')

        else:
            yield mkvalues(
                ('Report Date', ael.date_today().to_string("%d %B %Y")),
                ('Start Date', self.start.to_string("%d %B %Y")),
                ('End Date', self.end.to_string("%d %B %Y"))
            )

            if self.shariah:
                yield mkinfo('We hereby confirm that the below mentioned transactions were held by ourselves as at ' + self.end.to_string("%d %B %Y")+ '.')
            else:
                yield mkinfo('We hereby confirm that the below mentioned instrument(s) were held by ourselves as at ' + self.end.to_string("%d %B %Y")+ '.')

            if not self.excludeDeposit:
                columns = [{'name': 'Facility'},
                           {'name': 'Account No'},
                           {'name': 'Total Interest'},
                           {'name': 'Balance'},
                           {'name': 'Accrued Interest'}]

                yield mktable(columns, self._get_transaction_rows())


            for trd in sorted(self.trades, key=lambda t: t.insaddr.exp_day):

                instrument = acm.FInstrument[trd.insaddr.insid]

                ai_funding_instype = trd.add_info('Funding Instype')
                ai_mm_instype = trd.add_info(at.addInfoSpecEnum.MM_INSTYPE)

                trade_mm_instype = ai_funding_instype or ai_mm_instype or ''

                if trade_mm_instype in self.mm_instype or 'All' in self.mm_instype:

                    ins = trd.insaddr

                    if self.excludeDeposit and ins.instype == 'Deposit' and ins.open_end == 'Open End':
                            continue


                    if ael.date_from_time(trd.time) <= self.end and (
                        (self.use_custom_dates and ael.date_from_time(trd.time) >= self.start)
                        or (not self.use_custom_dates and ael.date(ins.exp_day) >= self.start)
                    ):

                        columns = [
                            {'name': 'Facility'},
                            {'name': 'Ref Number'},
                            {'name': 'StartDate'},
                            {'name': 'Expiry Date'},
                            {'name': 'Ref Rate'},
                            {'name': 'Rate/Spread (%)', 'width': '2.8cm'}
                        ]

                        yield mktable(columns, self._get_trade_row(trd))

                        columns = [
                            {'name': 'Start Date'},
                            {'name': 'End Date'},
                            {'name': 'Nominal', 'width': '2.8cm'},
                            {'name': 'Cash(paid/receipt)', 'width': '2.8cm'},
                            {'name': 'Interest', 'width': '2.8cm'},
                            {'name': 'All-In-Rate', 'width': '2cm'},
                            {'name': 'Pay day'}
                        ]

                        yield mktable(columns, self._get_final_rows(trd), size='small')


        yield mkinfo('We trust that you will find the above mentioned information in order.')

        yield mkinfo('THIS IS A COMPUTER-GENERATED DOCUMENT AND DOES NOT REQUIRE ANY SIGNATURES.')


    def _get_all_money_flows(self, trade, start_date, end_date):

        temp_list = []
        calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FMoneyFlowSheet')

        ''' This method will get all money flows for a trade and put it in a list '''
        for money_flow in trade.MoneyFlows(start_date, '').SortByProperty('PayDay'): #ABITFA-3416 - Including All cashflow within Start Date

            start_date = to_date(money_flow.StartDate())
            end_date = to_date(money_flow.EndDate())

            money_flow_type = calc_space.CreateCalculation(money_flow, 'Money Flow Type')

            if money_flow_type.Value() not in ('Float Rate', 'Fixed Rate', 'Fixed Amount'):
                continue

            if money_flow_type.Value() in ('Float Rate', 'Fixed Rate'):
                nominal_2 = ''
                nominal_1 = formcurr(abs(money_flow_value(money_flow, self.end, 'Cash Analysis Nominal')), None, money_flow.Currency().Name())
                forward_rate = money_flow_value(money_flow, self.end, 'Cash Analysis Forward Rate')
                projected = formcurr(abs(money_flow_value(money_flow, self.end, 'Cash Analysis Projected')), None, money_flow.Currency().Name())

                if forward_rate != None:
                    forward_rate = abs(round(forward_rate * 100, 5))

            elif money_flow_type.Value() in ('Fixed Amount', 'Redemption'):
                nominal_1 = ''
                nominal_2 = formcurr(abs(money_flow_value(money_flow, self.end, 'Cash Analysis Nominal')), None, money_flow.Currency().Name())
                projected = formcurr(0, None, money_flow.Currency().Name())
                forward_rate = 0

            payday = to_date(money_flow.PayDate())
            temp_list.append([nominal_1, nominal_2, projected, start_date, end_date, forward_rate, payday])

        return temp_list

    def _get_mf_of_same_period(self, temp_list):

        result_list = []
        ''' This method will group money flows of the same period and return the list of money flows '''

        for current in temp_list:
            try:
                last_insert = result_list[-1]

                if last_insert[5] == current[5] and last_insert[6] == current[6]:
                    if last_insert[0] == '':
                        last_insert[0] = current[0]
                    elif last_insert[1] == '':
                        last_insert[1] = current[1]
                    continue
            except IndexError:
                pass

            result_list.append(current)

        return result_list

    def _get_trade_row(self, trd):

        trade = acm.FTrade[trd.trdnbr]
        ''' this method will extract trade and instrument static data '''
        row = []

        ins_type = trade.Instrument().InsType()

        if trade.Instrument().InsType() == 'Deposit':
            if trade.Premium() < 0:
                ins_type = 'Loan'
            else:
                ins_type = 'Deposit'
        if trade.Instrument().Legs()[0].LegType() == 'Float':
            ref_rate = trade.Instrument().Legs()[0].FloatRateReference().Name()
            rate = trade.Instrument().Legs()[0].Spread()
        else:
            ref_rate = ''
            rate = trade.Instrument().Legs()[0].FixedRate()

        row.append(
            [ins_type,
             trade.Oid(),
             trade.Instrument().StartDate(),
             trade.Instrument().EndDate(),
             str(ref_rate),
             rate]
        )

        return row

    def _get_transaction_rows(self):
        calc_space  = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', self.end)

        rows = []

        # trades will be removed in the cycle from self.trades
        for t in list(self.trades):
            total_interest = 0.0
            total_accr = 0.0
            cashflowamount = 0.0
            sd = ael.date(self.start)
            ed = ael.date(self.end)

            if t.add_info('Account_Name'):
                self.trades.remove(t)
                legs = t.insaddr.legs()

                while sd <= ed:
                    day1 = sd
                    day2 = sd.add_days(1)
                    sd = day2

                    int_set = legs[0].interest_settled(day1, day2, 'ZAR')
                    int_acc = legs[0].interest_accrued(day1, day2, 'ZAR')
                    int_due = legs[0].interest_due(day1, day2, 'ZAR')

                    total_interest -= int_set + int_acc + int_due

                tt = acm.FTrade[t.trdnbr]
                facility = None
                if CallStatementGeneral.is_eligible_for_statement(tt):
                    facility = DocumentGeneral.strip_dti_notation_from_funding_instype(t.add_info('Funding Instype'))
                    statement_start_date = self.start.to_string(ael.DATE_ISO)
                    statement_end_date = self.end.to_string(ael.DATE_ISO)
                    statement_xml_generator = CallStatementXMLGenerator.CallStatementXMLGenerator()
                    statement_xml_generator._ensure_deposit_correctly_booked(tt)
                    statement_money_flows = CallStatementGeneral.get_statement_money_flows(tt,
                        statement_start_date, statement_end_date)
                    account_balance_from_date = statement_xml_generator._get_earliest_required_account_balance_date(
                        statement_start_date, statement_money_flows)
                    account_balance_by_date = statement_xml_generator._get_account_balance_by_date(
                        tt, account_balance_from_date, statement_end_date)
                    # Unsettled Interest.
                    interest_balance = statement_xml_generator._get_summary_interest_accrued_amount(
                        statement_end_date, statement_money_flows, account_balance_by_date)
                    # Settled Interest.
                    interest_reinvested = statement_xml_generator._get_summary_interest_reinvested_amount(
                        statement_money_flows)
                    interest_settled = statement_xml_generator._get_summary_interest_settled_amount(
                        statement_start_date, statement_end_date, statement_money_flows, interest_reinvested)
                    # Closing Balance.
                    closing_balance = account_balance_by_date[statement_end_date]
                    total_interest = DocumentGeneral.format_amount(interest_reinvested + (interest_settled * -1))
                    cashflowamount = DocumentGeneral.format_amount(closing_balance)
                    total_accr = DocumentGeneral.format_amount(interest_balance)
                else:
                    facility = t.add_info('Funding Instype')
                    calc_interest = calc_space.CalculateValue(tt, 'Portfolio Accrued Interest')
                    total_accr += abs(calc_interest.Value().Number())

                    cashflows = ael.CashFlow.select('legnbr = %d' % legs[0].legnbr)
                    for cashflow in cashflows:
                        if cashflow.start_day and cashflow.start_day <= ed: # For back-dated trades
                            cashflowamount = cashflowamount + cashflow.fixed_amount
                        elif cashflow.pay_day <= ed:
                            cashflowamount = cashflowamount + cashflow.fixed_amount

                rows.append([facility,
                             str(t.insaddr.insid).replace('ZAR-', ''),
                             formcurr(total_interest, None, tt.Currency().Name()),
                             formcurr(cashflowamount, None, tt.Currency().Name()),
                             formcurr(total_accr, None, tt.Currency().Name())])

        calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')

        return rows

    def _get_final_rows(self, trd):

            trade = acm.FTrade[trd.trdnbr]

            all_money_flows = self._get_all_money_flows(trade, self.start.to_string("%Y-%m-%d"), self.end.to_string("%Y-%m-%d"))

            final_output = self._get_mf_of_same_period(all_money_flows)

            for member in final_output:

                ''' this method will write the each money flow into the pdf report '''
                start_date = ''
                end_date = ''
                rate = ''

                nominal = str(member[0])
                cash_paid_receipt = str(member[1])
                interest = str(member[2])

                if member[3] is not None:
                    start_date = member[3].strftime("%d %b %Y")

                if member[4] is not None:
                    end_date = member[4].strftime("%d %b %Y")

                if member[5] is not None:
                    rate = str(member[5]) + '%'

                payday = member[6].strftime("%d %b %Y")

                yield [start_date,
                       end_date,
                       nominal,
                       cash_paid_receipt,
                       interest,
                       rate,
                       payday]

def filters():
    return sorted(tf.fltid for tf in ael.TradeFilter)

def MM_Instype():
    mms = set(['All'])
    for instype in ['Funding Instype', 'Instype', 'MoneyMarket Instype']:
        mms = mms.union(cl.entry for cl in ael.ChoiceList[instype].members())

    return sorted(mms)

ael_variables = [('AuditorID', 'Name_Auditor', 'string', '', '', 1),
                 ('AuditorOrg1', 'AddressLine1_Organization', 'string', '', ''),
                 ('AuditorOrg2', 'AddressLine2_Organization', 'string', '', ''),
                 ('AuditorOrg3', 'AddressLine3_Organization', 'string', '', ''),
                 ('AuditorOrg4', 'AddressLine4_Organization', 'string', '', ''),
                 ('AuditorOrg5', 'AddressLine5_Organization', 'string', '', ''),
                 ('AuditorOrg6', 'AddressLine6_Organization', 'string', '', ''),
                 ('AuditorTel', 'Tel_Auditor', 'string', '', '', 1),
                 ('AuditorFax', 'Fax_Auditor', 'string', '', '', 1),
                 ('PartyID', 'Counter Party', 'string', sorted(p.ptyid for p in ael.Party), ''),
                 ('InsID', 'Account', acm.FInstrument, [], '', 0, 1),
                 ('MM_Instype', 'MM Instype', 'string', MM_Instype(), 'All', 1, 1),
                 ('tf', 'TradeFilter_Trade Filter', 'string', filters(), 'Audit_Certificate'),
                 ('Start', 'Start Date', 'string', '', '', 1),
                 ('End', 'End Date', 'string', '', ael.date_today(), 1),
                 ('TradeDates', 'Trade Dates', 'string', ['All live trades', 'Custom dates'], 'All live trades', 1),
                 ('NoAccounts', 'No Accounts Template', 'string', ('Yes', 'No'), 'No'),
                 ('Shariah', 'Shariah Client', 'string', ('Yes', 'No'), 'No'),
                 ('Folder', 'Folder_Path', 'string', ['Y:\Jhb\Operations Secondary Markets\Sylvia Sharon\AUDIT CERTIFICATES'], '', 1),
                 ('ExcludeDeposit', 'Exclude Deposit', 'string', ['Yes', 'No'], 'No', 1)]

def ael_main(params):
    print 'Loading...'
    End = ael.date(params['End'])
    ExcludeDeposit = (params['ExcludeDeposit']=='Yes' and True or False)

    # If no_accounts is true, then the counterparty does not have to exist
    # and we infer there are no trades held by the counterparty.
    no_accounts = params['NoAccounts'] == 'Yes'
    party = ael.Party[params['PartyID']]
    if not party:
        if no_accounts:
            party = PartyMock(fullname = params['PartyID'])
        else:
            ins = ael.Instrument[params['InsID'][0].Name()]
            trades = ael.Trade.select('insaddr = %d' %ins.insaddr)
            party = trades[0].counterparty_ptynbr

    party_name = party.fullname + " " + party.fullname2

    acmParty = acm.Ael.AelToFObject(party)
    if 'ShortCode' not in dir(acmParty):
        raise Exception('Custom method "ShortCode" not available for party object')

    auditor_address = {
        'name': party_name,
        'aliasname': acmParty.ShortCode(),
        'att': [{'att': params['AuditorID']}],
        'tel': params['AuditorTel'],
        'fax': params['AuditorFax'],
        'address': [params['AuditorOrg1'],
                    params['AuditorOrg2'],
                    params['AuditorOrg3'],
                    params['AuditorOrg4'],
                    params['AuditorOrg5'],
                    params['AuditorOrg6']]
    }

    report = Report(start=ael.date(params['Start']),
                    end=End,
                    shariah=params['Shariah'] == 'Yes',
                    party=party,
                    tf_name=params['tf'],
                    mm_instype=params['MM_Instype'],
                    no_accounts=no_accounts,
                    auditor_address=auditor_address,
                    use_custom_dates=params['TradeDates'] == 'Custom dates',
                    excludeDeposit=ExcludeDeposit)

    xml = report.create_report()
    filename = "Audit Report {0} {1}".format(party_name.replace('/', ''), End.to_string("%d %B %Y"))
    gen = XMLReport.XMLReportGenerator(str(params['Folder']), 'XMLReport')
    pdffile = gen.create(xml, filename)
    startFile(pdffile)


def ASQL(*rest):
    acm.RunModuleWithParameters('Audit_Certificate', 'Standard') #@UndefinedVariable
    return 'Done'
