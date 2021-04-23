"""-----------------------------------------------------------------------------------------
MODULE
    SBL_Dividend_Summary_Report

DESCRIPTION
    Date                : 2019-10-30
    Purpose             : This will create the dividend summary report which SBL Ops will
                          use for making payments to clients.
    Department and Desk : SBL Ops
    Requester           : James Stevens
    Developer           : Qaqamba Ntshobane

HISTORY
=============================================================================================
Date            Change no       Developer               Description
---------------------------------------------------------------------------------------------
2019-10-30      PCGDEV-16       Qaqamba Ntshobane       Initial Implementation

ENDDESCRIPTION
------------------------------------------------------------------------------------------"""

import acm
import FRunScriptGUI

import re
import os
import xlsxwriter

import sl_functions
from at_logging import getLogger
from collections import OrderedDict, defaultdict
from at_ael_variables import AelVariableHandler

outputSelection = FRunScriptGUI.DirectorySelection()
directorySelection = acm.FFileSelection()
directorySelection.PickDirectory(True)
directorySelection.SelectedDirectory("Y:\Jhb\Secondary Markets IT\Fix_the_Front\Q\Corporate Actions\Dividend Summary Report\Reports\FA Reports")

GLOBAL = {'acquirer': 'SECURITY LENDINGS DESK',
          'portfolio': ['ACS A2X - Scrip Lending',
                        'ACS SBL Coll',
                        'ACS - Script Lending',
                        'Bond - Script Lending',
                        'Collateral optimize',
                        'MM Liquidity',
                        'new_SL Structured Deals',
                        'Prime optimize',
                        'SBL - Prime Clients',
                        'SBL Delta One Loans ACS',
                        'SBL ETF - Trading ACS',
                        'SBL SNP 44032 ACS',
                        'SBL_Accrued_1',
                        'SBL_Agency_Bond',
                        'SBL_Agency_OmsfinCFD',
                        'SBL_Agency_Prime_Broker',
                        'SBL_CFD_Old Mutual',
                        'SBL_Fixed Income DBR',
                        'SBL_Fixed Income Denel RF',
                        'SBL_Fixed Income Denel',
                        'SBL_Fixed Income National Tertiary RF',
                        'SBL_Fixed Income_ University Free State',
                        'SBL_Fixed Income_ Unisa',
                        'SBL_Fixed Income UPT',
                        'SBL Agency',
                        'SBL - Prime Clients',
                        'SL_LEIPS'
                        ],
          'excluded_parties': ['EQ Derivatives Desk'],
          'valid_collateral_instypes': ['Stock', 'ETF', 'SecurityLoan'],
          'excluded_clients': ['SLBPA1', 'SLBPA2', 'ABS401', 'ABS402'],
          'coll_parent_portfolio': 'SBL_NONCASH_COLLATERAL'
        }

LOGGER = getLogger(__name__)
OUTPUT_FILENAME = 'Dividend_Summary_Report'
CALC_SPACE = acm.FCalculationMethods().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')

ael_variables = AelVariableHandler()
ael_variables.add(
    'record_date',
    label = 'Record Date',
    default = acm.Time.DateToday(),
    alt = 'Date for report extraction.'
    )
ael_variables.add(
    'output_filename',
    label = 'Output File',
    cls = 'string',
    default = OUTPUT_FILENAME
    )
ael_variables.add(
    'file_drop_location',
    label = 'File Drop Location',
    cls = directorySelection,
    default = directorySelection,
    multiple = True
    )


class ReportDataProcessor(object):

    column_headers = [{'header': 'Trade No.'}, {'header': 'Combined'}, {'header': 'Security'}, 
                      {'header': 'Loan Quantity'}, {'header': 'Div Rate'}, {'header': 'B/L'}, 
                      {'header': 'T/C'}, {'header': 'Cpty Major'}, {'header': 'Cpty Short Name'}, 
                      {'header': 'Amount 100%'}, {'header': 'Net Div% Amount'},
                      {'header': 'Record Date'}, {'header': 'Payment Date'}
                     ]

    def __init__(self):
        self.detailed_data = []
        self.summarized_data = []
        self.report_row_data = OrderedDict(defaultdict(list))

    def add_report_row_data(self, key1, key2, value):
        self.report_row_data.setdefault(key1, [])
        self.report_row_data[key1].append({key2:value})

    def generate_detailed_data(self):
        for ls in list(self.report_row_data.values()):
            for l in ls:
                for v in list(l.values()):
                    if not list(v.values()) in self.detailed_data:
                        self.detailed_data.append(list(v.values()))

    def summarize_data(self):

        clone_dictionary = self.report_row_data

        for key, val in list(self.report_row_data.items()):

            if key[:6] in GLOBAL["excluded_clients"]:
                continue

            keys = [list(v.keys()) for v in val]
            keys = [k[0] for k in keys]
            key_duplicates = list([i for i in keys if keys.count(i) > 1])


            if not key_duplicates and len(keys) > 1:
                self.summarized_data.append(list(clone_dictionary[key][0].values())[0].values()[1:])
                self.summarized_data.append(list(clone_dictionary[key][1].values())[0].values()[1:])
                continue
            elif len(keys) == 1:
                self.summarized_data.append(list(clone_dictionary[key][0].values())[0].values()[1:])
                continue

            for trade_type in set(sorted(keys)):

                net_quantity = 0
                net_div_amount = 0
                full_amount = 0

                index = [list(dict.keys()) for dict in clone_dictionary[key]].index([trade_type])

                for v in sorted(val):

                    try:
                        net_quantity += v[trade_type]['loan_quantity']
                        net_div_amount += v[trade_type]['net_dividend_amount']
                        full_amount += v[trade_type]['full_amount']
                    except:
                        if net_quantity or net_div_amount or full_amount:
                            clone_dictionary[key][index][trade_type]['loan_quantity'] = net_quantity
                            clone_dictionary[key][index][trade_type]['net_dividend_amount'] = net_div_amount
                            clone_dictionary[key][index][trade_type]['full_amount'] = full_amount
                        continue

                if net_quantity == 0:
                    continue

                clone_dictionary[key][index][trade_type]['loan_quantity'] = net_quantity
                clone_dictionary[key][index][trade_type]['net_dividend_amount'] = net_div_amount
                clone_dictionary[key][index][trade_type]['full_amount'] = full_amount

                if (list(clone_dictionary[key][index].values())[0].values())[1:] not in self.summarized_data:
                    self.summarized_data.append((list(clone_dictionary[key][index].values())[0].values())[1:])

    def generate_report(self, record_date, output_file):

        if not self.report_row_data:
            LOGGER.info("No open positions to report for %s. No report produced." %record_date)
            return

        workbook = xlsxwriter.Workbook(output_file)
        div_summary_sheet = workbook.add_worksheet('Dividend Summary')
        div_detailed_sheet = workbook.add_worksheet('Dividend Detail')

        div_summary_sheet.add_table('A1:L%s' %str(len(self.summarized_data) + 1), {'data': self.summarized_data, 'columns': self.column_headers[1:]})
        div_detailed_sheet.add_table('A1:M%s' %str(len(self.detailed_data) + 1), {'data': self.detailed_data, 'columns': self.column_headers})

        workbook.close()
        LOGGER.info('Report saved to . %s' % str(output_file))


class ProcessTrade(object):

    def __init__(self):
        self.trade = ''
        self.combined_name = ''
        self.trade_type = ''
        self.party_type = ''
        self.party_short_code = ''
        self.party_major_code = ''
        self.dividend_data = {}
        self.dividend_factor = 1

    def process_trade(self, trade, dividend_data, process_second_trade=False):

        self.trade = trade
        self.dividend_data = dividend_data

        if not process_second_trade:
            self.set_party_details()
        else:
            self.set_party_details('process_second_trade')

        self.set_trade_type()
        self._add_row_data()

        return {'key1':self.combined_name, 'key2':self.trade_type, 'data_dict':self.trade_data_dict}

    def _add_row_data(self):

        security_code = self.trade.Instrument().Security().Name().split("/")[1]
        self.combined_name = self.party_short_code + security_code + '100'

        self.trade_data_dict = OrderedDict([('trade_id', self.trade.Oid()),
                                            ('combined_name', self.combined_name),
                                            ('security_code', security_code),
                                            ('loan_quantity', self.calculated_values()['quantity']),
                                            ('dividend_rate', self.dividend_data['amount']),
                                            ('counterparty_type', self.party_type),
                                            ('trade_type', self.trade_type),
                                            ('counterparty_major_code', self.party_major_code),
                                            ('counterparty_short_code', self.party_short_code),
                                            ('full_amount', self.calculated_values()['full_amount']),
                                            ('net_dividend_amount', self.calculated_values()['full_div_amount']),
                                            ('record_date', self.dividend_data['record_date']),
                                            ('payment_date', self.dividend_data['pay_date'])
                                           ])

    def calculated_values(self):

        if self.trade_type == 'Trade':
            if self.party_type == 'Borrower':
                loan_quantity  = abs(CALC_SPACE.CalculateValue(self.trade, 'Quantity'))
                full_amount = abs(loan_quantity * self.dividend_data['amount']) * self.dividend_factor

            if self.party_type == 'Lender':
                loan_quantity  = abs(CALC_SPACE.CalculateValue(self.trade, 'Quantity')) * -1
                full_amount = abs(loan_quantity * self.dividend_data['amount']) * self.dividend_factor * -1

        elif self.trade_type == 'Collateral':
            if self.party_type == 'Borrower':
                loan_quantity  = abs(CALC_SPACE.CalculateValue(self.trade, 'Quantity')) * -1
                full_amount = abs(loan_quantity * self.dividend_data['amount']) * -1

            if self.party_type == 'Lender':
                loan_quantity  = abs(CALC_SPACE.CalculateValue(self.trade, 'Quantity'))
                full_amount = abs(loan_quantity * self.dividend_data['amount'])
        net_dividend_amount = full_amount

        return {'quantity':loan_quantity, 'full_amount':full_amount, 'full_div_amount':net_dividend_amount}

    def set_party_details(self, counterparty2=None):

        counterparty = self.true_counterparty(self.trade, counterparty2)
        self.party_type = counterparty.AdditionalInfo().SL_CptyType() 

        if counterparty.AdditionalInfo().SL_G1PartyCode() and counterparty.AdditionalInfo().SL_G1PartyCode().startswith('COLLAC'):
            self.party_short_code = counterparty.AdditionalInfo().SL_G1PartyCode()[:-1]
        else:
            self.party_short_code = counterparty.AdditionalInfo().SL_G1PartyCode()
        self.party_major_code = counterparty.AdditionalInfo().SL_MajorPtyCode()

    @staticmethod
    def true_counterparty(trade, counterparty2=None):

        borrower = trade.AdditionalInfo().SL_G1Counterparty1()
        lender = trade.AdditionalInfo().SL_G1Counterparty2()
        true_party = sl_functions.sl_true_counterparty(trade) if (borrower and lender) else trade.Counterparty()

        if counterparty2 and true_party.Name() == borrower:
            return acm.FParty[lender]
        elif counterparty2 and true_party.Name() == lender:
            return acm.FParty[borrower]
        return true_party

    def set_trade_type(self):
        if self.trade.Instrument().InsType() == 'SecurityLoan':
            self.trade_type = "Trade"

            if self.trade.Instrument().AdditionalInfo().SL_Dividend_Factor():
                self.dividend_factor = self.trade.Instrument().AdditionalInfo().SL_Dividend_Factor()
        else:
            self.trade_type = "Collateral"


class CorporateActionsExtract(object):

    def __init__(self):

        self.output_file = None
        self.record_date = acm.Time.DateToday()

    @staticmethod
    def _is_sec_loan(trade):

        return trade.Instrument().InsType() == 'SecurityLoan'

    @staticmethod
    def _is_collateral_portfolio(prf):

        if prf.MemberLinks()[0]:
            return prf.MemberLinks()[0].OwnerPortfolio().Name() == GLOBAL["coll_parent_portfolio"]
        return False

    @staticmethod
    def _has_sbl_counterparty(trade):

        if trade.Counterparty().Name() in GLOBAL["excluded_parties"]:
            return False

        if CorporateActionsExtract._is_sec_loan(trade):
            borrower = trade.AdditionalInfo().SL_G1Counterparty1()
            lender = trade.AdditionalInfo().SL_G1Counterparty2()
            return (borrower and lender) or ProcessTrade.true_counterparty(trade).Name().startswith("SL")
        return trade.Counterparty().Name().startswith("SL") or trade.Counterparty().Name().startswith("COLL")

    @staticmethod
    def _dividend_details(corp_act, record_date):

        payment_date = ''
        dividend = 0

        if corp_act.Dividend():
            dividend = corp_act.Dividend().Amount()
            payment_date = corp_act.Dividend().PayDay()

        elif corp_act.AdditionalInfo().Gross_Taxable_Rate():
            dividend = corp_act.AdditionalInfo().Gross_Taxable_Rate()
            dividend = re.split('[A-Z]+', dividend)[1]

        elif corp_act.AdditionalInfo().Tax_Rate():
            dividend = corp_act.AdditionalInfo().Tax_Rate()
            dividend = re.split('[A-Z]+', dividend)

            if len(dividend) == 2:
                dividend = dividend[1]
        
        if dividend:
            dividend = float(dividend)
        else:
            dividend = 0.0

        if not payment_date:
            payment_date = corp_act.SettleDate()
        return {'amount':dividend, 'record_date':record_date, 'pay_date':payment_date}

    def _is_valid_selo_trade(self, trade):

        return (self._is_sec_loan(trade) and
                self._has_sbl_counterparty(trade) and
                (trade.ValueDay() <= self.record_date) and
                (trade.Portfolio().Name() in GLOBAL["portfolio"]) and
                (trade.Instrument().OpenEnd() == 'Open End' or
                 (trade.Instrument().OpenEnd() == 'Terminated' and trade.Instrument().ExpiryDate().split(' ')[0] > self.record_date)
                ))

    def _is_valid_coll_trade(self, trade):

        return (self._has_sbl_counterparty(trade) and
                (trade.ValueDay() <= self.record_date) and
                self._is_collateral_portfolio(trade.Portfolio()) and
                (trade.Instrument().InsType() in GLOBAL["valid_collateral_instypes"]))

    def get_additional_trade(self, securities_list):

        query_trades = acm.FStoredASQLQuery['div_summ_trades'].Query().Select()
        additional_trades = []

        for trade in query_trades:
            security_name = trade.Instrument().Security().Name()

            if ((security_name in securities_list) and
                (self._is_valid_selo_trade(trade) or
                self._is_valid_coll_trade(trade))):
                additional_trades.append(trade)
        return additional_trades

    def get_trades(self, corp_actions, extract_date):

        trades = []
        self.record_date = extract_date
        settlements = acm.FSettlement.Select("acquirer='%s' and valueDay<='%s' and status='Settled'" %("SECURITY LENDINGS DESK", self.record_date))
        settlements = list(set(settlements))

        for sett in settlements:
            trade = sett.Trade()

            if ((trade.Instrument().Security().Name() in list(corp_actions.keys())) and trade.Status() in ["BO Confirmed", "BO-BO Confirmed"] and
                trade.Text1()  != "FULL_RETURN" and trade.Type() != "Closing" and
                (self._is_valid_selo_trade(trade) or self._is_valid_coll_trade(trade))):
                trades.append(trade)

        trades.extend(self.get_additional_trade(list(corp_actions.keys())))

        return list(set(trades))

    @staticmethod
    def _is_bonus_issue(corpact):

        return corpact.Template() == 'BonusIssue'

    @staticmethod
    def get_corporate_actions(record_date):

        return {ca.Instrument().Name(): ca for ca in acm.FCorporateAction.Select("recordDate = '%s' and instrument<>''" % record_date) 
                                                    if (ca.Dividend() or ca.AdditionalInfo().Gross_Taxable_Rate() or 
                                                        CorporateActionsExtract._is_bonus_issue(ca))}

    def run_extraction(self, output_file, record_date):

        data_processor = ReportDataProcessor()

        corp_actions = self.get_corporate_actions(record_date)

        if corp_actions:
            LOGGER.info('>>> %s STARTING EXTRACTION' % str(acm.Time.TimeNow())[:-4])
        else:
            LOGGER.info("No open positions to report for %s. No report produced." % record_date)
            return

        trades = self.get_trades(corp_actions, record_date)

        for trade in trades:
            process_trade = ProcessTrade()

            security_code = trade.Instrument().Security().Name()
            dividend_data_dict = self._dividend_details(corp_actions[security_code], record_date)
            trade_data_dict = process_trade.process_trade(trade, dividend_data_dict)

            data_processor.add_report_row_data(trade_data_dict['key1'],
                                               trade_data_dict['key2'], 
                                               trade_data_dict['data_dict'])
            if self._is_sec_loan(trade):
                trade_data_dict = process_trade.process_trade(trade, dividend_data_dict, True)

                data_processor.add_report_row_data(trade_data_dict['key1'],
                                                   trade_data_dict['key2'], 
                                                   trade_data_dict['data_dict'])
        data_processor.generate_detailed_data()
        data_processor.summarize_data()
        data_processor.generate_report(record_date, output_file)


def ael_main(dictionary):

    record_date = acm.Time.DateAddDelta(dictionary['record_date'], 0, 0, 0)
    directory = str(dictionary['file_drop_location'])
    filename = str(dictionary['output_filename']) + "_%s.xlsx" % int(''.join(filter(str.isdigit, acm.Time.TimeNow())))
    output_file = os.path.join(directory, filename)

    CorporateActionsExtract().run_extraction(output_file, record_date)
    LOGGER.info('>>> %s COMPLETED SUCCESSFULLY' % str(acm.Time.TimeNow())[:-4])

