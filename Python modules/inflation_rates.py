"""-----------------------------------------------------------------------
MODULE
    inflation_rates.py

DESCRIPTION
    Date                : 2017-05-30
    Purpose             : Produce inflation rates
    Department and Desk : FICC
    Requester           : Anthonyrajah, Marlyn: Absa (JHB)
    Developer           : Ondrej Bahounek
    CR Number           : CHNG0004622336

HISTORY
==================================================================================
Date       Change no    Developer          Description
----------------------------------------------------------------------------------
2017-09-12              Ondrej Bahounek    post upgrade: recalculate inflation rate
                                           to match pre upgrade results.
ENDDESCRIPTION
--------------------------------------------------------------------------------"""

import acm
from at_report import CSVReportCreator
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
import os


LOGGER = getLogger(__name__)

    
def calculate_CPI(day_of_month, days_in_month, sacpi_4m, sacpi_3m):
    part_4m = (days_in_month - day_of_month + 1.) / days_in_month * sacpi_4m
    part_3m = (day_of_month - 1.) / days_in_month * sacpi_3m
    return part_4m + part_3m
    
    
def get_init_cpi(for_date):
    d_4m_back = acm.Time.DateAddDelta(for_date, 0, -4, 0)
    d_4m_back_1st = acm.Time.FirstDayOfMonth(d_4m_back)
    d_4m_back_1s_plus1m = acm.Time.DateAddDelta(d_4m_back_1st, 0, 1, 0)
    day_of_month = acm.Time.DayOfMonth(for_date)  # d
    days_in_month = acm.Time.DaysInMonth(for_date)  # D
    interp_interval = acm.Time.DateDifference(d_4m_back, d_4m_back_1st)
    
    sacpi_4m = acm.FInstrument['SACPI'].UsedPrice(d_4m_back_1st, 'ZAR', 'internal')
    if interp_interval == 0:
        return sacpi_4m
    
    sacpi_3m = acm.FInstrument['SACPI'].UsedPrice(d_4m_back_1s_plus1m, 'ZAR', 'internal')
    return calculate_CPI(day_of_month, days_in_month, sacpi_4m, sacpi_3m)


def get_last_cpi_price(for_date):
    prices = acm.FPrice.Select("instrument='%s' and market='%s'"
        %("SACPI", "internal"))

    for price in prices.SortByProperty('ReleaseDate', False):
        if price.ReleaseDate() <= for_date:
            return price


class InflationReport(CSVReportCreator):

    YEARS = 30

    def __init__(self, file_name, file_suffix, path, start_date, yc_name):
        super(InflationReport, self).__init__(file_name, file_suffix, path)
        self.start_date = start_date
        self.yc_name = yc_name
        
    def _header(self):
        return ["Benchmark Curve", "Start Date", "End Date", "Inflation", "Spot Rate", "Initial Price"]

    def _get_first_end_date(self):
        """Return the date of last SACPI entry day + 5 months"""
        ins = acm.FInstrument['SACPI']
        market = "internal"
        start_year = acm.Time.DateAddDelta(acm.Time.FirstDayOfYear(self.start_date), 0, 0, -1)
        this_year_prices = acm.FPrice.Select("instrument='%s' and market='%s' and day>'%s' and day<'%s'" 
                % (ins.Name(), market, start_year, self.start_date))

        prices = sorted(this_year_prices, key=lambda price: price.Day(), reverse=True)
        last_sacpi_day = prices[0].Day()
        sacpi_plus_five_m = acm.Time.FirstDayOfMonth(acm.Time.DateAddDelta(last_sacpi_day, 0, 5, 0))
        return sacpi_plus_five_m
        
    def _collect_data(self):
        yield_curve = acm.FYieldCurve[self.yc_name]
        months = self.YEARS * 12
        first_end_date = self._get_first_end_date()
        
        LOGGER.info("Generating rates...")
        LOGGER.info("YC name: '%s'", yield_curve.Name())
        LOGGER.info("Date Start: '%s'", self.start_date)
        LOGGER.info("First End Date: '%s'", first_end_date)
        
        cpi = get_init_cpi(self.start_date)
        sacpi_price = get_last_cpi_price(self.start_date)
        init_price = sacpi_price.Settle()
        init_date =sacpi_price.Day()
        
        self.content.append(("SACPI", self.start_date, "", "", "", cpi))
        curve_info = yield_curve.IrCurveInformation()
        
        for month_delta in range(months):
            month = acm.Time.DateAddDelta(first_end_date, 0, month_delta, 0)
            end_date = acm.Time.FirstDayOfMonth(month)
            
            '''
            Rate method parameters:
            IrRateType: 6 - refers to 'Simple'
            dayCountMethod: 2 - 'Act/365'
            calc type: 1 - 'Spot Rate'
            '''
            rate_spot = yield_curve.IrCurveInformation().Rate(self.start_date, end_date, 6, 2, 1)
            
            lagged_date1 = acm.Time.FirstDayOfMonth(end_date)
            lagged_date2 = acm.Time.DateAddDelta(lagged_date1, 0, 1, 0)
            unlagged_date1 = acm.Time.FirstDayOfMonth(acm.Time.DateAddDelta(end_date, 0, -4, 0))
            unlagged_date2 = acm.Time.DateAddDelta(unlagged_date1, 0, 1, 0)
            days_between1 = acm.Time.DateDifference(end_date, lagged_date1)
            days_between2 = acm.Time.DateDifference(lagged_date2, lagged_date1)
            
            
            disc_rate1 = curve_info.Rate(init_date, unlagged_date1, 'Annual Comp', 'Act/365', 'Discount')
            disc_rate2 = curve_info.Rate(init_date, unlagged_date2, 'Annual Comp', 'Act/365', 'Discount')
            estimate1 = init_price / disc_rate1
            estimate2 = init_price / disc_rate2
            
            inflation = ((estimate2 - estimate1) / days_between2 * days_between1) + estimate1
            rate_infl = inflation / cpi

            self.content.append((self.yc_name, self.start_date, end_date, rate_infl, rate_spot, ""))
    
    
ael_variables = AelVariableHandler()
ael_variables.add('filename', 
    label='Filename',
    default='ZAR-CPI_Rates', 
    alt='Filename')
ael_variables.add('output_path',
    label='Output Path',
    default='/services/frontnt/Task/',
    alt='Output Path')
ael_variables.add('start_date',
    label='Start Date',
    cls='date',
    default='Today')
ael_variables.add('yield_curve',
    label='Yield Curve',
    cls='FYieldCurve',
    default=acm.FYieldCurve['ZAR-CPI'],
    alt=("Inflation Curve"))
    

def ael_main(ael_dict):
    start_date = ael_dict['start_date'].to_string("%Y-%m-%d")
    filename = "{0}_{1}".format(ael_dict['filename'], start_date)
    
    yc = ael_dict['yield_curve'].Name()
    if start_date < acm.Time.DateToday():
        yc = "{0}_{1}".format(yc, start_date)  
    
    report = InflationReport(filename, 'csv', ael_dict['output_path'], 
        start_date, yc)
    
    report.create_report()
    
    outfile = os.path.join(ael_dict['output_path'], filename + ".csv")
    LOGGER.output(outfile)
    LOGGER.info("%s: Completed successfully.", acm.Time.TimeNow())
