"""----------------------------------------------------------------------------
PURPOSE                 :  Weighted Average Life report for PLUM
REQUESTER               :  Ryan Bates
DEPARTMENT AND DESK     :  Loan Trading
DEVELOPER               :  Libor Svoboda
CR NUMBER               :  CHNG0004572889
-------------------------------------------------------------------------------

HISTORY
===============================================================================
Date        Change no     Developer              Description
-------------------------------------------------------------------------------

"""
import os
import csv
import acm
from collections import defaultdict
from datetime import datetime
from at_ael_variables import AelVariableHandler


DATE_TODAY = acm.Time.DateToday()
CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()


class WalCalculator(object):
    
    day_count = 365.0
    min_total = 1e-2
    to_curr = acm.FInstrument['ZAR']
    columns = (
        'KEY',
        'CP',
        'Mentis Proj Number',
        'PM_ACMFacilityID',
        'PM_Facility_Cpy',
        'PM_FacilityID',
        'Trades',
        'Date',
        'Numerator',
        'Total CFS',
        'Curr Vect',
        'Is RCF',
        'Is TL',
        'Max Expiry Date',
        'Weighted Avg Life(Date)',
    )
    
    def __init__(self):
        self._trades = []
        self._results = {}
        self._max_expiry = ''
        self._PM_FacilityID = ''
        self._PM_FacilityCPY = ''
        self._PM_ACMFacilityID = ''
        self._mentis_proj = ''
        self._currency = ''
        self._convert = True
    
    def _get_max_expiry(self):
        return max(DATE_TODAY, 
                   max([t.Instrument().ExpiryDateOnly() for t in self._trades]))
    
    def _check_facilityID(self, code):
        id_split = self._PM_FacilityID.split('|')
        return len(id_split) > 2 and id_split[2] == code
    
    def _is_RCF(self):
        return self._check_facilityID('RCF')

    def _is_TL(self):
        return self._check_facilityID('TL')
        
    def _prepare_data(self):
        trade_add_info = self._trades[0].AdditionalInfo()
        self._max_expiry = self._get_max_expiry()
        self._PM_FacilityID = (str(trade_add_info.PM_FacilityID())
                               if trade_add_info.PM_FacilityID() else 'Not Found')
        self._PM_FacilityCPY = (str(trade_add_info.PM_FacilityCPY().Name())
                                if trade_add_info.PM_FacilityCPY() else 'Not Found')
        self._PM_ACMFacilityID = (str(trade_add_info.PM_ACMFacilityID())
                                  if trade_add_info.PM_ACMFacilityID() else 'Not Found')
        self._mentis_proj = (str(trade_add_info.Mentis_Project_Num())
                             if trade_add_info.Mentis_Project_Num() else 'Not Found')
        self._currency = str(self._trades[0].Currency().Name())
    
    def _get_fx_rate(self, orig_curr, date):
        if not self._convert:
            return 1.0
        date = max(date, DATE_TODAY)
        return orig_curr.Calculation().FXRate(CALC_SPACE, self.to_curr, date).Number()
    
    def _get_premium(self, trade, date, delta_calc=False):
        premium = 0.0
        for flow in trade.MoneyFlows():
            if flow.Type() != 'Premium' or flow.PayDay() < date:
                continue
            fx_rate = self._get_fx_rate(flow.Currency(), date)
            db = 1
            if delta_calc:
                # Include 'Days Between' factor
                db = acm.Time.DateDifference(flow.PayDay(), date) / self.day_count
            premium += flow.Calculation().Projected(CALC_SPACE).Number() * db * fx_rate
        return premium
    
    def _get_cashflow_amount(self, trade, date, delta_calc=False):
        total = 0.0
        for leg in trade.Instrument().Legs():
            fx_rate = self._get_fx_rate(leg.Currency(), date)
            for cf in leg.CashFlows():
                if cf.PayDate() < date:
                    continue
                db = 1
                if delta_calc:
                    # Include 'Days Between' factor
                    if self._is_RCF():
                        db = acm.Time.DateDifference(self._max_expiry, date) / self.day_count
                    else: 
                        db = acm.Time.DateDifference(cf.PayDate(), date) / self.day_count
                total += cf.Calculation().Projected(CALC_SPACE, trade).Number()* db * fx_rate
        return total
    
    def _money_flows_total(self, date, delta_calc=False):
        total = 0.0
        for trade in self._trades:
            total += self._get_premium(trade, date, delta_calc)
            total += self._get_cashflow_amount(trade, date, delta_calc)
        return total
    
    def _to_plum_date(self, date):
        return datetime(*acm.Time.DateToYMD(date)).strftime('%d/%m/%Y')
    
    def append(self, item):
        self._trades.append(item)
    
    def calculate(self, dates, convert=True):
        self._prepare_data()
        self._convert = convert
        for date in dates:
            if date > self._max_expiry:
                continue
            total_mf = self._money_flows_total(date, False)
            delta_mf = self._money_flows_total(date, True)
            
            wal = 0.0
            if ((self._is_TL() and abs(total_mf) <= self.min_total) or 
                    (self._is_RCF() and abs(delta_mf) <= self.min_total)):
                wal = acm.Time.DateDifference(self._max_expiry, date) / self.day_count
            elif abs(total_mf) > self.min_total:
                wal = delta_mf / total_mf
            self._results[date] = {
                'WAL': wal,
                'Numerator': delta_mf,
                'Denominator': total_mf,
            }
    
    def get_report_rows(self, per_trade=False):
        if not self._results:
            return []
        row_variables = self._trades if per_trade else sorted(self._results.keys())
        first_date = min(self._results.keys())
        is_RCF = '1' if self._is_RCF() else '0'
        is_TL = '1' if self._is_TL() else '0'
        rows = []
        for var in row_variables:
            rows.append([
                '%s_%s' % (self._PM_FacilityCPY, self._PM_FacilityID),
                self._PM_FacilityCPY,
                self._mentis_proj,
                self._PM_ACMFacilityID,
                self._PM_FacilityCPY,
                self._PM_FacilityID,
                var.Name() if per_trade else str([t.Name() for t in self._trades]),
                self._to_plum_date(first_date if per_trade else var),
                (str(self._results[first_date]['Numerator']) 
                    if per_trade else str(self._results[var]['Numerator'])),
                (str(self._results[first_date]['Denominator']) 
                    if per_trade else str(self._results[var]['Denominator'])),
                self._currency,
                is_RCF,
                is_TL,
                self._to_plum_date(self._max_expiry),
                (str(self._results[first_date]['WAL']) 
                    if per_trade else str(self._results[var]['WAL'])),
            ])
        return rows


def enable_report(ael_input):
    var_name = ael_input.name[9:]
    enabled = ael_input.value == '1'
    report_var = ael_variables.get(var_name)
    report_var.enabled = enabled


ael_variables = AelVariableHandler()
ael_variables.add(
    'trade_filter',
    label='Trade Filter',
    cls='FTradeSelection',
    default=acm.FTradeSelection['PM_ClientPositions_Asset'],
)
ael_variables.add(
    'convert',
    label='FX conversion',
    alt='Convert non-ZAR denominated values.',
    collection=[0, 1],
    cls='int',
    default=1,
)
ael_variables.add(
    'outpath',
    label='Output directory',
    default='/services/frontnt/Task',
)
ael_variables.add(
    'generate_report',
    label='Generate report',
    collection=[0, 1],
    cls='int',
    default=0,
    hook=enable_report,
)
ael_variables.add(
    'report',
    label='Report name',
    mandatory=False,
)
ael_variables.add(
    'generate_trade_report',
    label='Generate per-trade report',
    collection=[0, 1],
    cls='int',
    default=0,
    hook=enable_report,
)
ael_variables.add(
    'trade_report',
    label='Trade report name',
    mandatory=False,
)


def _skip(trade):
    ins_override = trade.AdditionalInfo().InsOverride()
    return (trade.Instrument().IsExpired() or 
            trade.Status() in ('Void', 'Simulated') or
            (ins_override and ins_override == 'Commitment Fee'))


def _get_month_end_dates(start_date, count):
    first_of_next_month = acm.Time.FirstDayOfMonth(acm.Time.DateAddDelta(start_date, 0, 1, 0))
    return [acm.Time.DateAddDelta(first_of_next_month, 0, x, -1) for x in range(count)]


def _group_trades(trades):
    wal_splitter = defaultdict(lambda: defaultdict(lambda: defaultdict(WalCalculator)))
    for trade in trades:
        if _skip(trade):
            continue
        trade_add_info = trade.AdditionalInfo()
        PM_FacilityCPY = (str(trade_add_info.PM_FacilityCPY().Name())
                          if trade_add_info.PM_FacilityCPY() else 'Not Found')
        PM_FacilityID = (str(trade_add_info.PM_FacilityID())
                         if trade_add_info.PM_FacilityID() else 'Not Found')
        currency = str(trade.Currency().Name())
        wal_splitter[PM_FacilityCPY][PM_FacilityID][currency].append(trade)
    
    wal_groups = []
    for id_level in wal_splitter.itervalues():
        for curr_level in id_level.itervalues():
            wal_groups.extend(curr_level.values())
    return wal_groups


def _generate_report(wal_groups, path, per_trade=False):
    with open(path, 'wb') as report:
        report_writer = csv.writer(report, delimiter='\t')
        report_writer.writerow(WalCalculator.columns)
        for wal_group in wal_groups:
            for row in wal_group.get_report_rows(per_trade):
                report_writer.writerow(row)


def ael_main(ael_params):
    trades = ael_params['trade_filter'].Trades()
    convert = ael_params['convert']
    outpath = ael_params['outpath']
    
    wal_groups = _group_trades(trades)
    dates = _get_month_end_dates(DATE_TODAY, 360)
    for wal_group in wal_groups:
        wal_group.calculate(dates, convert)
    
    report_date = DATE_TODAY.replace('-', '')[:6]
    if ael_params['generate_report']:
        report_name = ael_params['report']
        report_path = os.path.join(outpath, report_name)
        report_path = report_path.format(date=report_date)
        _generate_report(wal_groups, report_path)
        print('Wrote secondary output to %s' % report_path)
    
    if ael_params['generate_trade_report']:
        trade_report_name = ael_params['trade_report']
        trade_report_path = os.path.join(outpath, trade_report_name)
        trade_report_path = trade_report_path.format(date=report_date)
        _generate_report(wal_groups, trade_report_path, True)
        print('Wrote secondary output to %s' % trade_report_path)
    
    print('completed successfully')

