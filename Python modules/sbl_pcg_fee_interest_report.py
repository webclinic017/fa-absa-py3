"""-----------------------------------------------------------------------------
PURPOSE              :  SBL onto FA
                        The script generates fee and interest report for a 
                        given date range.
DESK                 :  SBL PCG
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-06-03  CHG0102113     Libor Svoboda       Initial Implementation
"""
import csv
import datetime
import os
from collections import defaultdict

import acm
from at_ael_variables import AelVariableHandler
from at_time import acm_date
from at_logging import getLogger
from sbl_monthly_fee_payments import get_vat_rate, select_trades


LOGGER = getLogger(__name__)
CALENDAR = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time.DateToday()
PL_DATES = {
    'Inception': acm.Time.DateFromYMD(1970, 1, 1),
    'First Of Year': acm.Time.FirstDayOfYear(TODAY),
    'First Of Month': acm.Time.FirstDayOfMonth(TODAY),
    'Two Days Ago': acm.Time.DateAddDelta(TODAY, 0, 0, -2),
    'Yesterday': acm.Time.DateAddDelta(TODAY, 0, 0, -1),
    'PrevBusDay': CALENDAR.AdjustBankingDays(TODAY, -1),
    'Custom Date': TODAY,
    'First Of Week': acm.Time.FirstDayOfWeek(TODAY),
    'Now': TODAY,
}
CALC_CURRENCY = acm.FCurrency['ZAR']
CALC_SPACE_STD = acm.Calculations().CreateStandardCalculationsSpaceCollection()
CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
CALC_SPACE.SimulateGlobalValue('Fixed Currency', CALC_CURRENCY)
CALC_SPACE.SimulateGlobalValue('Position Currency Choice', 'Fixed Curr')
CALC_SPACE.SimulateGlobalValue('Aggregate Currency Choice', 'Fixed Curr')


def enable_custom_date(ael_input, custom_date_var):
    """Hook enabling custom date."""
    custom_date = ael_variables.get(custom_date_var)
    if ael_input.value == 'Custom Date':
        custom_date.enabled = True
    else:
        custom_date.enabled = False
        custom_date.value = TODAY


ael_variables = AelVariableHandler()
ael_variables.add(
    'start_date',
    label='Start Date',
    collection=acm.FEnumeration['EnumPLStartDate'].Enumerators(),
    default='Inception',
    cls='string',
    hook=lambda x: enable_custom_date(x, 'start_date_custom'),
    alt='PL Start Date.'
)
ael_variables.add(
    'start_date_custom',
    label='Custom Start Date',
    cls='date',
    alt='Custom PL Start Date.'
)
ael_variables.add(
    'end_date',
    label='End Date',
    collection=acm.FEnumeration['EnumPLEndDate'].Enumerators(),
    default='Now',
    cls='string',
    hook=lambda x: enable_custom_date(x, 'end_date_custom'),
    alt='PL End Date.'
)
ael_variables.add(
    'end_date_custom',
    label='Custom End Date',
    cls='date',
    alt='Custom PL End Date.'
)
ael_variables.add(
    'trade_query',
    label='Base Trade Query',
    cls='FStoredASQLQuery',
    default='',
    alt='Base trade query that is extended at runtime.'
)
ael_variables.add(
    'deposit_query',
    label='Base Deposit Query',
    cls='FStoredASQLQuery',
    default='',
    alt='Base deposit query that is extended at runtime.'
)
ael_variables.add(
    'parties',
    label='Parties',
    cls='FParty',
    default='',
    multiple=True,
)
ael_variables.add(
    'output_dir',
    label='Output Dir',
    cls='string',
)
ael_variables.add(
    'output_file',
    label='Output File',
    cls='string',
)


def get_output_path(output_dir, output_file, report_date):
    output_path = os.path.join(output_dir, output_file)
    dt = datetime.datetime(*acm.Time.DateToYMD(report_date))
    return output_path.format(dt)


def simulate_globals(params):
    start_date = params['start_date']
    end_date = params['end_date']
    CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date', start_date)
    if start_date == 'Custom Date':
        CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', 
                                       acm_date(params['start_date_custom']))
    CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', end_date)
    if end_date == 'Custom Date':
        CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', 
                                       acm_date(params['end_date_custom']))


def select_deposits(query, party):
    deposit_query = acm.FStoredASQLQuery[query.Name()].Query()
    deposit_query.AddAttrNode('Counterparty.Name', 'EQUAL', party.Name())
    return deposit_query.Select()


def select_loans(query, parties, start_date, end_date):
    borrowers = []
    lenders = []
    for party in parties:
        flag = party.AdditionalInfo().SL_CptyType()
        if flag == 'Borrower':
            borrowers.append(party)
        elif flag == 'Lender':
            lenders.append(party)
        else:
            LOGGER.warning('SL_CptyType not specified for party "%s".' % party.Name())
            continue
    loans_per_party = defaultdict(list)
    trade_query = acm.FStoredASQLQuery[query.Name()].Query()
    borrower_trades = select_trades(trade_query, start_date, end_date, borrowers=borrowers)
    for trade in borrower_trades:
        loans_per_party[trade.AdditionalInfo().SL_G1Counterparty1()].append(trade)
    trade_query = acm.FStoredASQLQuery[query.Name()].Query()
    lender_trades = select_trades(trade_query, start_date, end_date, lenders=lenders)
    for trade in lender_trades:
        loans_per_party[trade.AdditionalInfo().SL_G1Counterparty2()].append(trade)
    return loans_per_party


class FeeInterestCalc(object):
    
    internal = acm.FParty['internal']
    fieldnames = (
        'Cpty Name',
        'Cpty Code',
        'Cpty Major',
        'Fees Receivable',
        'Interest Receivable',
        'Fees Payable',
        'Interest Payable',
        'Net',
    )
    net_columns = (
        ('Fees Receivable', 1.0),
        ('Interest Receivable', 1.0),
        ('Fees Payable', -1.0),
        ('Interest Payable', -1.0),
    )
    total_columns = (
        'Fees Receivable',
        'Interest Receivable',
        'Fees Payable',
        'Interest Payable',
        'Net',
    )
    
    def __init__(self, party, loans, deposits, flag):
        self._party = party
        self._loans = loans
        self._deposits = deposits
        self._flag = flag
    
    @staticmethod
    def populate_values_row(cpty_name='', cpty_code='', cpty_major=''):
        row = defaultdict(float)
        row['Cpty Name'] = cpty_name
        row['Cpty Code'] = cpty_code
        row['Cpty Major'] = cpty_major
        return row
    
    @classmethod
    def get_totals(cls, rows):
        totals = cls.populate_values_row('OVERALL TOTALS')
        for col_name in cls.total_columns:
            totals[col_name] = sum([row[col_name] for row in rows if row[col_name]])
        return totals
    
    def _populate_header_row(self):
        row = defaultdict(str)
        row['Cpty Name'] = self._party.Name()
        row['Cpty Code'] = self._party.AdditionalInfo().SL_G1PartyCode()
        row['Cpty Major'] = self._party.AdditionalInfo().SL_MajorPtyCode()
        return row
    
    def _calculate_fees(self):
        fees = defaultdict(float)
        if not self._loans:
            LOGGER.info('%s: No loans found.' % self._party.Name())
            return fees
        adhoc_portfolio = acm.FAdhocPortfolio()
        for trade in self._loans:
            adhoc_portfolio.Add(trade)
        loans = CALC_SPACE.InsertItem(adhoc_portfolio)
        CALC_SPACE.Refresh()
        value = CALC_SPACE.CalculateValue(loans, 'SL PL Period Fee')
        direction =  1.0 if self._flag == 'Borrower' else -1.0
        total = float(value) * direction
        vat_rate = get_vat_rate(self._party, TODAY)
        vat = total * (vat_rate - 1) / vat_rate
        taxable = total - vat 
        fees['Total'] = total
        fees['Tax'] = vat
        fees['Taxable'] = taxable
        return fees
    
    def _calculate_interest(self):
        if not self._deposits:
            LOGGER.info('%s: No deposit trades found.' % self._party.Name())
            return 0.0
        adhoc_portfolio = acm.FAdhocPortfolio()
        for trade in self._deposits:
            adhoc_portfolio.Add(trade)
        deposits = CALC_SPACE.InsertItem(adhoc_portfolio)
        CALC_SPACE.Refresh()
        value = CALC_SPACE.CalculateValue(deposits, 'Portfolio Settled Interest')
        return float(value)
    
    def calculate(self):
        taxable_row = self.populate_values_row(cpty_code='Taxable')
        tax_row = self.populate_values_row(cpty_code='Netted Tax')
        try:
            fees = self._calculate_fees()
        except:
            LOGGER.exception('%s: Failed to calculate Fees.' % self._party.Name())
            fees = defaultdict(lambda: float('nan'))
            
        try:
            interest = self._calculate_interest()
        except:
            LOGGER.exception('%s: Failed to calculate Interest.' % self._party.Name())
            interest = float('nan')
        
        if fees['Total'] < 0:
            taxable_row['Fees Payable'] = abs(fees['Taxable'])
            tax_row['Fees Payable'] = abs(fees['Tax'])
        elif fees['Total'] > 0:
            taxable_row['Fees Receivable'] = fees['Taxable']
            tax_row['Fees Receivable'] = fees['Tax']
        else:
            taxable_row['Fees Payable'] = fees['Taxable']
            tax_row['Fees Payable'] = fees['Tax']
            taxable_row['Fees Receivable'] = fees['Taxable']
            tax_row['Fees Receivable'] = fees['Tax']
        
        if interest < 0:
            taxable_row['Interest Payable'] = abs(interest)
        elif interest > 0:
            taxable_row['Interest Receivable'] = interest
        else:
            taxable_row['Interest Receivable'] = interest
            taxable_row['Interest Payable'] = interest
            
        taxable_row['Net'] = sum([taxable_row[col_name] * direction 
                                  for (col_name, direction) in self.net_columns])
        tax_row['Net'] = sum([tax_row[col_name] * direction 
                              for (col_name, direction) in self.net_columns])
        return [
            self._populate_header_row(),
            taxable_row,
            tax_row
        ]


def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    simulate_globals(ael_params)
    start_date = (acm_date(ael_params['start_date_custom']) 
                      if ael_params['start_date'] == 'Custom Date' 
                      else PL_DATES[ael_params['start_date']])
    end_date = (acm_date(ael_params['end_date_custom']) 
                    if ael_params['end_date'] == 'Custom Date' 
                    else PL_DATES[ael_params['end_date']])
    loans_per_party = select_loans(ael_params['trade_query'], ael_params['parties'],
                                   start_date, end_date)
    rows = []
    for party_name in sorted(loans_per_party.keys()):
        party = acm.FParty[party_name]
        if not party:
            LOGGER.warning('Party object not found for "%s".' % party_name)
            continue
        loans = loans_per_party[party_name]
        deposits = select_deposits(ael_params['deposit_query'], party)
        calc = FeeInterestCalc(party, loans, deposits, party.AdditionalInfo().SL_CptyType())
        rows.extend(calc.calculate())
    totals = FeeInterestCalc.get_totals(rows)
    rows.append(totals)
    output_path = get_output_path(ael_params['output_dir'], 
                                  ael_params['output_file'], TODAY)
    with open(output_path, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FeeInterestCalc.fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    LOGGER.info('Output written to: %s' % output_path)
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')
