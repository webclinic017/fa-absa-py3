"""
This module runs the calculation for commitment fees
for the Loans Portfolio business.

History
=======
12/10/2015 Bhavnisha Sarawan
ABITFA-3708 Amended status checks to include Simulated.

09/02/2016 Evgeniya Baskaeva
ABITFA-3928 - Commitment Fee updates

19/04/2016 Evgeniya Baskaeva
ABITFA-4045 - Add day count + Rolling Conv. option
ABITFA-4122 - Add Portfolio Field
ABITFA-4196 - Wrong calculation of paydates in CommFeeCalculation script

12/05/2016 Evgeniya Baskaeva
ABITFA-4295 - Comm Fee: payment dates, log, trade filter

30/06/2016 Evgeniya Baskaeva
ABITFA-4150 - Add PM_FacilityCPY & PM_FacilityID fields into Commitment Fee extract

01/07/2016 Evgeniya Baskaeva
ABITFA-4150 - Replace 'None' values with '' in the final output

19/10/2016 Evgeniya Baskaeva
ABITFA-4515 - Incorrect trade filtration

07/11/2017 Ntuthuko Matthews
ABITFA-5089 - Optimize the commitment fee calculation script 
            - Combine the Comm/Util Fee into a single excel workbook

08/11/2018 Ntuthuko Matthews
ABITFA-4345 - Utilisationfee
            - Enabling utilization fees
            - Enabling customised formatting for numeric columns
"""

import acm
import ael
import json
from time import localtime, strftime
from datetime import datetime, date
from at_ael_variables import AelVariableHandler
import os
import traceback
from abc import ABCMeta
from DataAccessUtil import DataAccess
import xlsxwriter as xlwt

# Set up global variables

AEL_TODAY = ael.date_today()
ZAR_CALENDAR = ael.Calendar[acm.FCurrency['ZAR'].Calendar().Oid()]

# List of portfolios to be used unless trade filter is specified
FEE_TYPE_LIST = ['Commitment', 'Utilization']
PF_LIST = ['PRIMARY MARKETS BANKING', 'PM Corp']
INS_TYPE_LIST = ['Curr']
TRADE_STATUS_LIST = ['Void', 'Simulated']
CP_TYPE_LIST = ['Intern Dept']
# Payment type commitment fee
PM_TYPE_COMM_FEE = {'CMF': 'Commitment Fee', 'UTF': 'Utilisation Fee'}
PERIOD_AT_END = 'At End'

EXCEPTION_LOG = []

# Create GUI

TRADE_FILTERS = [tf.Name() for tf in acm.FTradeSelection.Select("")]

ael_variables = AelVariableHandler()

ael_variables.add(
    'path',
    label='Path',
    cls='string',
    default=r'C:\Temp\CommFee'
)
ael_variables.add(
    'trade_filter',
    label='Trade Filter',
    cls='string',
    default='',
    collection=TRADE_FILTERS,
    mandatory=False
)
ael_variables.add_bool(
    'override',
    'Override the rows calculated today',
    default=False
)


# Classes and Functions

class ReportColumn(object):

    def __init__(self, col_name, col_title):
        self.name = col_name
        self.title = col_title


class NonCMFTrades(object):
    COLUMNS = [ReportColumn('trade_number', 'Trade Number'),
               ReportColumn('counterparty', 'Counterparty'),
               ]

    def __init__(self, trade):
        self.trade_number = trade.Oid()
        self.counterparty = trade.Counterparty().Name()
        # self.util_rate_used = None


class CMFTrades(object):
    """
    Class for Mentis trades with CMF flag

    Represents report row

    """

    COLUMNS = [ReportColumn('textobject_name', 'Text Object Name'),
               ReportColumn('trade_number', 'Cash Payment Trade Number'),
               ReportColumn('portfolio', 'Portfolio'),
               ReportColumn('currency', 'Currency'),
               ReportColumn('pm_facility_cpy', 'PM_FacilityCPY'),
               ReportColumn('pm_facility_id', 'PM_FacilityID'),
               ReportColumn('threshold', 'Threshold'),
               ReportColumn('comm_fee_rate', 'CommFee Rate'),
               ReportColumn('utilised', '% Utilised'),
               ReportColumn('calc_comm', 'Calculate Comm Fee? [Y:1,N:0]'),
               ReportColumn('rolling_convention', 'Rolling Conv'),
               ReportColumn('period', 'Period'),
               ReportColumn('base_date', 'Base Date'),
               ReportColumn('expiry_date', 'Expiry Date'),
               ReportColumn('facility_max', 'Facility Max'),
               ReportColumn('cash_payment_cp', 'Cash Payment CP'),
               ReportColumn('list_of_trades', 'List of Trades'),
               ReportColumn('current_notional', 'Current Notional'),
               ReportColumn('limit_breach',
                            'Threshold Breached[1:Not Breached, 0:Breached]'),
               ReportColumn('notional_charged', 'Notional Charged'),
               ReportColumn('payment_dates', 'Payment Dates'),
               ReportColumn('next_paydate_report', 'Next Paydate'),
               ReportColumn('days_charged_for', 'Days Charged For'),
               ReportColumn('amount_charged', 'Amount Charged'),
               ReportColumn('prev_cumulative_amount', 'Prev Cum. Amt'),
               ReportColumn('indicator', 'Indicator[0:Add On,1:New Payment]'),
               ReportColumn('new_cumulative_amount', 'New Cumulative Amount', ),
               ReportColumn('overdrawn', 'Overdrawn[Y:1,N:0]'),
               ReportColumn('sds_id', 'SDS ID'),
               ReportColumn('client_address', 'CP Address'),
               ReportColumn('fica_compliant', 'FICA Compliant')]

    def __init__(self, trade, key, override=False):
        self.trade = trade
        self.textobject_name = key
        self.pm_facility_cpy = self.get_pm_facility_cpy(trade)
        self.pm_facility_id = self.get_pm_facility_id(trade)
        self.trade_number = trade.Oid()
        self.portfolio = trade.PortfolioId()
        self.currency = trade.Currency().Name()
        calendar_id = acm.FCurrency[self.currency].Calendar().Oid()
        self.currency_calendar = ael.Calendar[calendar_id]
        self.threshold = ''
        self.comm_fee_rate = ''
        self.calc_comm = ''
        self.rolling_convention = ''
        self.period = ''
        self.base_date = ''
        self.expiry_date = ''
        self.facility_max = ''
        self.cash_payment_cp = ''
        self.list_of_trades = ''
        self.current_notional = ''
        self.limit_breach = ''
        self.notional_charged = ''
        self.payment_dates = ''
        self.next_paydate = ''
        self.next_paydate_report = ''
        self.days_charged_for = ''
        self.amount_charged = ''
        self.prev_cumulative_amount = ''
        self.indicator = ''
        self.new_cumulative_amount = ''
        self.overdrawn = ''
        cp = trade.Counterparty()
        self.sds_id = cp.AdditionalInfo().BarCap_SMS_CP_SDSID()
        if self.sds_id: self.sds_id = int(self.sds_id)
        self.client_address = cp.Address()
        self.fica_compliant = cp.AdditionalInfo().FICA_Compliant()
        self.dataAcess = DataAccess()
        self.day_count = ''
        self.prefix = key[0:3]
        self.utilised = ''
        """
        if self.prefix == 'UTF':
            self.util_rate_used = 0
        """

    def load_from_json(self, record):
        # record = self.dataAcess.Select(self.textobject_name)

        if self.prefix == 'CMF':
            self.threshold = float(record['PM_Limit'])
            self.comm_fee_rate = float(record['PM_CommitFeeRate']) / 100
            self.calc_comm = str(record['CalcCommFee'])
        else:
            self.threshold = 1
            self.comm_fee_rate = float(record['UtilFeeRate'])
            self.calc_comm = str(record['CalcUtilFee'])
            self.utilised = float(record['Utilised']) * 100
            self.amount_charged = float(record['PM_CommitFeeRate'])
        self.rolling_convention = str(record['Rolling Convention'])
        self.period = str(record['CommitPeriod'])
        self.base_date = ael.date(record['PM_CommitFeeBase'])
        self.expiry_date = ael.date(record['PM_FacilityExpiry'])
        self.facility_max = float(record['PM_FacilityMax'])

        counterparty = self.trade.Counterparty()
        self.cash_payment_cp = counterparty.Name()

        try:
            self.day_count = str(record['DayCount'])
        except KeyError:
            # this field did not exist in prev. version of CommFeeUploader.py
            pass

    @staticmethod
    def _convert_period_to_matrix(period):
        """
        get date period matrix
        """

        commit_fee_period_dict = {'Annually': [0, 0, 1],
                                  'Daily': [1, 0, 0],
                                  'Monthly': [0, 1, 0],
                                  'Quarterly': [0, 3, 0],
                                  'SemiAnnually': [0, 6, 0],
                                  'Weekly': [7, 0, 0]}
        return commit_fee_period_dict[period]

    def _get_sub_trades(self, loan_trade_list):
        """ Get list loan trades related to the particular cash trade
        pm_facility_id and pm_facility_cpy fields on both cash and loan trades
        have to be the same

        Args:
            loan_trade_list: list of all the trades which passed the initial conditions

        Returns:
            sub_trade_list: trades that belong to particular cash trade
        """

        sub_trade_list = []
        if (self.expiry_date > AEL_TODAY):
            for trade in loan_trade_list:
                pm_facility_cpy = self.get_pm_facility_cpy(trade)
                pm_facility_id = self.get_pm_facility_id(trade)
                if pm_facility_cpy == self.pm_facility_cpy and pm_facility_id == self.pm_facility_id:
                    sub_trade_list.append(trade.Name())
        return sub_trade_list
        
    def _check_for_utilisation(self):
        if round(self.current_notional, 2) == 0.00:
            return False
        return True

    
    def _calculate_comm_fee(self, trade_list, loan_trade_list, calc_space,save = True):
        """
        make all calculations related to comm fee

        Args:
            trade_list: list of all the trades which passed the initial conditions
            calc_space: calculation space
        """

        self.list_of_trades = self._get_sub_trades(loan_trade_list)
        self.current_notional = self._calculate_notional(calc_space)
        self.limit_breach = self._check_limit_breach()

        diff = self.facility_max - self.current_notional
        # Limit is +ve if lending out; -ve if borrowing
        self.notional_charged = (max(diff, 0)
                                 if self.facility_max >= 0
                                 else min(diff, 0))

        daycnt_div = self._get_day_count_divisor()
        self.payment_dates = self._generate_dates()

        self.next_paydate = self._get_next_paydate()

        if self.next_paydate == 0:
            self.next_paydate_report = 'No payments remaining'
        else:
            self.next_paydate_report = self.next_paydate

        self.days_charged_for = self._get_date_period()

        try:
            if self.prefix == 'CMF':
                self.amount_charged = (float(self.limit_breach) /
                                       daycnt_div * self.notional_charged *
                                       self.comm_fee_rate *
                                       self.days_charged_for)
        except ZeroDivisionError, e:
            log_exception(("{0}: zero devision in amount charged".format(self.trade_number),
                           traceback.format_exc()))

        if AEL_TODAY < self.expiry_date:
            if self.prefix == 'CMF' and self.limit_breach == 1:
                flag_overpay = 1 if self.notional_charged == 0 else 0
                if save:
                    log_message("{0}: Committing to db".format(self.trade_number))
                    self._add_payment(flag_overpay)
                else:
                    try:
                        return self.amount_charged / self.days_charged_for
                    except ZeroDivisionError:
                        log_exception(("{0}: division by zero caused by 0 days charged".format(self.trade_number),
                            traceback.format_exc()))
            elif self.prefix == 'UTF':
                flag_overpay = self.limit_breach
                if save:
                    log_message("{0}: Committing to db".format(self.trade_number))
                    self._add_payment(flag_overpay)
                else:
                    return self.amount_charged / self.days_charged_for

    def _calculate_notional(self, calc_space):
        return sum([float(calc_space.CalculateValue(acm.FTrade[trade],
                                                    'DDM Nominal TXN CCY'))
                    for trade
                    in self.list_of_trades])

    def _check_limit_breach(self):
        if self.prefix == 'CMF':
            return self._cmf_check_limit_breach()
        else:
            return self._utf_check_limit_breach()

    def _utf_check_limit_breach(self):
        if float(self.current_notional) > self.facility_max:
            return 1
        return 0

    def _cmf_check_limit_breach(self):
        if abs(float(self.current_notional) / self.facility_max) < self.threshold:
            return 1
        return 0

    def _new_payment(self):
        """
        create new payment and commit to db
        Args:
            next_paydate(ael.date): payday
        """

        paym = acm.FPayment()
        paym.Trade(self.trade)
        paym.Type(PM_TYPE_COMM_FEE[self.prefix])
        paym.Currency(self.trade.Currency())
        paym.Party(self.trade.Counterparty())
        paym.PayDay(ael.date(self.next_paydate))
        paym.ValidFrom(ael.date_today())
        paym.Amount(self.amount_charged)
        paym.Commit()

    def _add_payment(self, flag_overpay):
        """
        add payment to existing one and commit to db
        """

        create_payment = True
        next_paydate = self.next_paydate

        if not next_paydate:
            next_paydate = ael.date(self.expiry_date)

        for paym in self.trade.Payments():
            if (ael.date(paym.PayDay()) == ael.date(next_paydate) and
                    paym.Type() == PM_TYPE_COMM_FEE[self.prefix]):
                create_payment = False

                self.prev_cumulative_amount = paym.Amount()
                self.indicator = '0'
                paym.Amount(paym.Amount() + self.amount_charged)
                paym.Commit()

                self.new_cumulative_amount = paym.Amount()
                self.overdrawn = flag_overpay
                break

        if create_payment:
            self._new_payment()
            self.prev_cumulative_amount = 0
            self.indicator = '1'
            self.new_cumulative_amount = self.amount_charged
            self.overdrawn = flag_overpay

    def _get_calculate_flag(self, override):
        """
        check whether any payment was already made today,
        unless forced to add another one

        Args:
            override(boolean): from used input
        Returns:
            calculate_flag(boolean)
        """
        if self.calc_comm == '1':
            if not override:
                for pm in self.trade.Payments():
                    upd_time = ael.date_from_time(pm.UpdateTime())
                    ignore_payment = (pm.Type() == PM_TYPE_COMM_FEE[self.prefix] and
                                      upd_time == AEL_TODAY)
                    if ignore_payment:
                        log_message("{0}: payment already made today".format(self.trade_number))
                        return False
            return True
        return False

    def _get_day_count_divisor(self):
        """
        get day count divisor from the currency of the trade

        Returns:
            Divisor (int) or False if day count isn't in the list
        """
        day_count = self.day_count
        if not day_count:
            day_count = self.trade.Currency().DayCountMethod()
        if day_count == 'Act/365':
            return 365
        if day_count == 'Act/360':
            return 360
        raise Exception("Day Count has unexpected value: {0}".format(day_count))

    def _get_month(self, date):
        return date.to_string('%m')

    def _apply_roll_conv(self, date):
        roll_conv = self.rolling_convention
        temp_date = self._adjust_to_bank_day(date)

        if roll_conv == 'Mod. Following':
            if self._get_month(temp_date) != self._get_month(date):
                temp_date = min(date.add_banking_day(self.currency_calendar, -1),
                                date.add_banking_day(ZAR_CALENDAR, -1))
        elif roll_conv == 'Mod. Preceding':
            if self._get_month(temp_date) == self._get_month(date):
                temp_date = max(date.add_banking_day(self.currency_calendar, 1),
                                date.add_banking_day(ZAR_CALENDAR, 1))

        elif roll_conv == 'Preceding':
            if ael.date(temp_date) != ael.date(date):
                temp_date = min(date.add_banking_day(self.currency_calendar, -1),
                                date.add_banking_day(ZAR_CALENDAR, -1))

        elif roll_conv == 'Following':
            # use the temp_date as it is. option present for integrity
            pass

        return temp_date

    def _generate_dates(self):
        dates = []

        temp_runner = self.base_date
        value_day = ael.date(self.trade.ValueDay())

        if self.period == PERIOD_AT_END:
            dates.append(self.expiry_date)

        else:
            # Add dates before basedate
            k = -1
            while temp_runner > value_day:
                new_paydate = self._get_paydate(k)
                if new_paydate >= value_day:
                    f_d = self._apply_roll_conv(new_paydate)
                    if f_d not in dates:
                        dates.append(f_d)
                temp_runner = new_paydate
                k -= 1
            # Add basedate
            dates.append(self._apply_roll_conv(self.base_date))

            # Add dates after basedate
            k = 1
            while temp_runner < self.expiry_date:
                new_paydate = self._get_paydate(k)
                if new_paydate <= self.expiry_date:
                    f_d = self._apply_roll_conv(new_paydate)
                    if f_d not in dates:
                        dates.append(f_d)
                if new_paydate > self.expiry_date:
                    if self.expiry_date not in dates:
                        dates.append(self._apply_roll_conv(self.expiry_date))
                temp_runner = new_paydate
                k += 1
        return sorted(dates)

    def _adjust_to_bank_day(self, date):
        return max(date.adjust_to_banking_day(self.currency_calendar),
                   date.adjust_to_banking_day(ZAR_CALENDAR))

    def _get_paydate(self, k):
        y = self._convert_period_to_matrix(self.period)
        if y[0] > 0:
            new_paydate = self.base_date.add_delta(k * y[0], 0, 0)
        elif y[1] > 0:
            new_paydate = self.base_date.add_delta(0, k * y[1], 0)
        elif y[2] > 0:
            new_paydate = self.base_date.add_delta(0, 0, k * y[2])
        return new_paydate

    def _get_next_paydate(self):
        """
        get date of next pay

        Returns:
            next paydate (ael.date); if no payments remain - 0
        """

        for date in self.payment_dates:
            if date > AEL_TODAY:
                return date
        return 0

    def _get_date_period(self):
        """
        get number of days for which the comm fee should be calculated
        calendars of both trade currency and ZAR are checked
        """
        temp_date = max(AEL_TODAY.add_banking_day(self.currency_calendar, 1),
                            AEL_TODAY.add_banking_day(ZAR_CALENDAR, 1))
        if not self.next_paydate:
            next_paydate = self.expiry_date
        else:
            next_paydate = self.next_paydate
            
        return abs(AEL_TODAY.days_between(temp_date)) \
            if temp_date <= next_paydate \
            else 0

    @classmethod
    def get_pm_facility_id(cls, trade):
        if trade.AdditionalInfo().PM_FacilityID():
            return trade.AdditionalInfo().PM_FacilityID()
        return ''

    @classmethod
    def get_pm_facility_cpy(cls, trade):
        if trade.AdditionalInfo().PM_FacilityCPY():
            facility_cpy = trade.AdditionalInfo().PM_FacilityCPY()
            if facility_cpy.Id():
                return facility_cpy.Id()
        return ''


class OutputLogAndXLS(object):
    """
    base class for log and xls ouputs
    """

    __metaclass__ = ABCMeta

    COMM_EXCLUDE_COLUMNS = ['utilised']
    UTIL_EXCLUDE_COLUMNS = ['commfee', 'limit_breach', 'notional_charged', 'threshold']
    # specify the format for each column
    # see https://xlsxwriter.readthedocs.io/format.html#set_num_format
    COMM_NUM_FORMAT_CELL = {6: 0x00, 7: 0x00, 8: 0x00, 13: 0x04, 16: 0x04,
                            18: 0x04, 20: 0x04, 21: 0x04, 22: 0x00, 23: 0x04,
                            24: 0x00, 25: 0x04 
                            }
                       
    UTIL_NUM_FORMAT_CELL = {6: 0x00, 7: 0x00, 8: 0x00, 13: 0x04, 16: 0x04,
                           19: 0x00, 20: 0x04, 21: 0x04, 22: 0x00, 23: 0x04
                           }

    # static vars for delimiter and line break
    delim = '\t'
    br = '\n'
    xls_data = []

    def _get_xls_mentis(self):
        self._get_table(self.list_mentis)
        return self.xls_data

    def _get_xls_exempt(self):
        self.xls_data = []
        self._get_table(self.list_exempt)
        return self.xls_data

    def _get_xls_exception(self):
        self.xls_data = []
        self.xls_data = EXCEPTION_LOG
        return self.xls_data

    def _write_output(self, custom_writer):
        title = ('Comm Fee' if self.prefix == 'CMF' else 'Util Fee')
        custom_writer('{0} Applicable Trades'.format(title))
        custom_writer(self._get_table(self.list_mentis))
        custom_writer(self.br * 4)
        custom_writer('{0} Applicable Trades with No Input Text Object'.format(title))
        custom_writer(self.br)
        custom_writer(self._get_table(self.list_exempt))
        custom_writer(self.br * 4)
        custom_writer('Exceptions during the run:')
        for exc_tuple in EXCEPTION_LOG:
            custom_writer(self.br)
            custom_writer('%s\n%s' % exc_tuple)

    def _get_table(self, trade_list):
        if not len(trade_list):
            return 'No applicable trades'

        # get the column headers
        headers = ['{0}'.format(col.title) for col in self._get_columns(trade_list[0])]
        # table = self.delim.join(headers)
        table = []
        table.append(headers)
        self._set_xls_data(headers)

        for elem in trade_list:
            data = self._get_table_row(headers, elem)
            self._set_xls_data(data)
            # table += self.br + self.delim.join(self.log_data)
            # table += self.delim.join(data)
            table.append(data)
        return table

    def _get_table_row(self, headers, report_row):
        table_row = []
        self.log_data = []
        for col in self._get_columns(report_row):
            val = getattr(report_row, col.name)
            if val is None:
                val = ''
            result = self._handle_format(val)
            self.log_data.append('{0}'.format(result))
            table_row.append(result)
        return table_row

    def _set_xls_data(self, rows):
        if not self.xls_data:
            self.xls_data = []
        self.xls_data.append(rows)

    def _handle_format(self, val):
        if isinstance(val, ael.ael_date):
            return self.to_iso_format(val)
        elif isinstance(val, list):
            new_val = []
            for i in val:
                if isinstance(i, ael.ael_date):
                    _date = self.to_iso_format(i)
                    new_val.append(_date)
                else:
                    new_val.append(i)
            return str(new_val)
        elif isinstance(val, float):
            return format(val, ',')
        else:
            return val

    def to_iso_format(self, ael_date):
        #return str(ael_date)
        #iso format (reversed) will be implemented in future releases
        _date = ael_date.to_time()
        new_date_format = date.fromtimestamp(_date).isoformat().split('-')
        return '{}/{}/{}'.format(new_date_format[2], new_date_format[1], new_date_format[0])
        

    def _modify_title(self, c):
        if self.prefix == 'UTF':
            COLUMNS = {'comm_fee_rate': 'UtilFeeRate', 'calc_comm': 'Calculate Util Fee? [Y:1,N:0]'}
        else:
            COLUMNS = {'comm_fee_rate': 'CommFeeRate', 'calc_comm': 'Calculate Comm Fee? [Y:1,N:0]'}

        if c.name in COLUMNS:
            c.title = COLUMNS[c.name]

        if c.name == 'textobject_name':
            title = ('Comm Fee' if self.prefix == 'CMF' else 'Util Fee')
            c.title = '{} Applicable TradesText Object Name'.format(title)

        return c

    def _get_columns(self, row):
        if self.prefix == 'CMF':
            return [self._modify_title(c) for c in row.COLUMNS if c.name not in self.COMM_EXCLUDE_COLUMNS]
        else:
            columns = [self._modify_title(c) for c in row.COLUMNS if c.name not in self.UTIL_EXCLUDE_COLUMNS]
            return columns


class OutputLog(OutputLogAndXLS):
    """
    class to create log
    """

    def __init__(self, list_mentis, list_exempt, prefix):
        self.list_mentis = list_mentis
        self.list_exempt = list_exempt
        self.prefix = prefix

    @staticmethod
    def _print(line):
        print line

    # print out log
    def print_output(self):
        self._write_output(OutputLog._print)


class OutputXLS(OutputLogAndXLS):
    """
    class to create xls file
    """

    def __init__(self, list_mentis, list_exempt, prefix):
        self.xls = ''
        self.list_mentis = list_mentis
        self.list_exempt = list_exempt
        self.prefix = prefix
        self.workbook = None
        self.formatter = None
        self.data = []

    def _append_to_xls(self, text):
        self.xls += text

    # compose xls file
    def get_output(self):
        self._write_output(self._append_to_xls)
        return self.xls

    def get_xls_output(self, worksheet, prefix, workbook):
        rownum = 0
        colnum = 0
        title = PM_TYPE_COMM_FEE[prefix]
        self.workbook = workbook
        self.worksheet = worksheet
        self.worksheet.write(rownum, colnum, '{0} Applicable Trades'.format(title))
        self.data = self._get_xls_mentis()
        rownum = self._xls_process(rownum + 1)
        self.worksheet.write(rownum + 1, colnum, '{0} Applicable Trades with No Input Text Object'.format(title))
        self.data = self._get_xls_exempt()
        self._xls_process(rownum + 2)
        self.data = self._get_xls_exception()
        self._xls_process(rownum + 3)

    def get_clean_number(self, value):
        try:
            if isinstance(value, str) and len(value) > 0:
                return float(value.replace(',', ''))
            elif isinstance(value, int):
                return value
            return float(value)
        except:
            return value

    def get_number_format_cells_dict(self):
        if self.worksheet.name == 'Commitment Fee':
            return self.COMM_NUM_FORMAT_CELL
        else:
            return self.UTIL_NUM_FORMAT_CELL
        
    
    def set_num_formatter(self, num_format):
        # create and get a formatter based the expected output for each cell in the workbook
        self.formatter = self.workbook.add_format()
        self.formatter.set_num_format(num_format)

    def _xls_process(self, row=0):
        column = 0
        count = 1
        num_format_dict = self.get_number_format_cells_dict()
        if self.data:
            column_sizes = len(self.data[0])
            for items in self.data:
                for i in items:
                    if row > 1 and column in num_format_dict:
                        if i:
                            i = self.get_clean_number(i)
                            self.set_num_formatter(num_format_dict[column])
                            self.worksheet.write(row, column, i, self.formatter)
                        else:
                            self.worksheet.write(row, column, i)
                    else:
                        self.worksheet.write(row, column, i)
                    column += 1
                    if count == column_sizes:
                        row += 1
                        count = 0
                        column = 0
                    count += 1
        return row

def log_exception(msg):
    print msg
    EXCEPTION_LOG.append(msg)


def log_message(msg):
    # time = strftime("%d.%m.%Y %H:%M:%S", localtime())
    time = strftime("%Y.%m.%d %H:%M:%S", localtime())
    print "{0}\t{1}".format(time, msg)


def get_cash_trades(trade_list, loan_trade_list, override, fee_type):
    """
    get list of cash trades

    returns 2 lists with CMF and non-CMF trades
    """

    log_message("Selecting cash trades...")
    list_mentis = []
    list_exempt = []
    trade_row = None
    context = acm.GetDefaultContext()
    cs_ts = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')

    is_valid_bank_day_zar = AEL_TODAY.is_banking_day(ZAR_CALENDAR)

    for trade in trade_list:
        try:
            is_valid_value_day = ael.date(trade.ValueDay()) <= AEL_TODAY
            if is_valid_value_day:
                key = fee_type + str(trade.Name())
                # record = ael.TextObject.read('type = "Customizable" and name = "{0}"'.format(key))
                record = DataAccess().Select(key)
                if record:
                    trade_row = CMFTrades(trade, key, override)
                    trade_row.load_from_json(record)
                    log_message("{0}: Running...".format(trade_row.trade_number))
                    """
                    check whether it's banking day for calendars
                    of both trade currency and ZAR;
                    whether calculate flag is True;
                    whether party is FICA-compliant
                    """

                    is_valid_bank_day = AEL_TODAY.is_banking_day(trade_row.currency_calendar)
                    calc_flag = trade_row._get_calculate_flag(override)

                    if not trade_row.fica_compliant:
                        log_exception(
                            ("{0}: {1} is FICA non-compliant".format(trade_row.trade.Oid(),
                                                                     trade_row.trade.Counterparty().Id()), '')
                        )
                    elif (is_valid_bank_day and
                          is_valid_bank_day_zar and
                          calc_flag):
                        trade_row._calculate_comm_fee(trade_list, loan_trade_list, cs_ts)

                    list_mentis.append(trade_row)
                else:
                    trade_row = NonCMFTrades(trade)
                    list_exempt.append(trade_row)
        except Exception, e:
            log_exception(("{0}: {1}".format(trade.Oid(), e), traceback.format_exc()))
    return (list_mentis, list_exempt)


def filter_valid_trades(trade_list):
    # returns list of valid trades based on fields on trade
    return [
        trade
        for trade in trade_list
        if trade.Counterparty() and
           trade.Counterparty().Type() not in CP_TYPE_LIST and
           trade.Status() not in TRADE_STATUS_LIST and
           trade.AdditionalInfo().PM_FacilityID() and
           trade.AdditionalInfo().PM_FacilityCPY()
    ]


def ael_main(args):
    log_message("Script started")
    log_message("Input params: {0}".format(args))
    filename = 'LPFeesCalculation' + AEL_TODAY.to_string('%d-%m-%Y') + '.xlsx'
    output_filename = os.path.join(args['path'], filename)

    # check if possible to write into log
    try:
        open(output_filename, 'w')
    except Exception, e:
        print "The file is not writable {0}: {1}".format(output_filename, e)
        return

    # fetch all the trades from mentis portfolios
    mentis_trade_list_raw = [
        trade
        for p in PF_LIST
        for trade in acm.FPhysicalPortfolio[p].Trades()
    ]
    mentis_trade_list = filter_valid_trades(mentis_trade_list_raw)

    # get list of trades to be checked
    trade_filter = args['trade_filter']
    if trade_filter:
        log_message("Selecting trades from trade filter...")
        try:
            cash_trade_list_raw = acm.FTradeSelection[trade_filter].Trades()
            cash_trade_list = filter_valid_trades(cash_trade_list_raw)
        except Exception, e:
            print "The trade filter doesn't exist {0}: {1}".format(trade_filter, e)
            return

    else:
        log_message("Selecting trades...")
        cash_trade_list = [
            trade
            for trade in mentis_trade_list
            if trade.Instrument().InsType() in INS_TYPE_LIST
        ]

    loan_trade_list = [
        trade
        for trade in mentis_trade_list
        if trade.Instrument().InsType() not in INS_TYPE_LIST
    ]

    workbook = xlwt.Workbook(output_filename)

    for prefix in PM_TYPE_COMM_FEE:
        list_mentis, list_exempt = get_cash_trades(cash_trade_list,
                                                   loan_trade_list,
                                                   args['override'],
                                                   prefix)

        output_log = OutputLog(list_mentis, list_exempt, prefix)
        output_log.print_output()

        output_xls = OutputXLS(list_mentis, list_exempt, prefix)

        try:
            worksheet = workbook.add_worksheet(PM_TYPE_COMM_FEE[prefix])
            output_xls.get_xls_output(worksheet, prefix, workbook)
        except IOError, e:
            print "Couldn't write into file {0} {1}".format(output_filename, e)

    print "Wrote secondary output to " + output_filename
    log_message("completed successfully")
    workbook.close()


