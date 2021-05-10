"""-----------------------------------------------------------------------
MODULE
    sales_credit_ytd_report.py

DESCRIPTION
    Date                : 2017-03-21
    Purpose             : Generate YTD Sales Credits report
    Department and Desk : Sales Credits CIB Africa
    Requester           : Joubert, Sonel: Operation Risk (JHB)
    Developer           : Ondrej Bahounek
    CR Number           : CHNG0004400748

HISTORY
===============================================================================
Date       Change no    Developer          Description
-------------------------------------------------------------------------------

ENDDESCRIPTION
-----------------------------------------------------------------------"""

import acm, ael
from at_report import CSVReportCreator
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
import os


LOGGER = getLogger(__name__)

START_OF_YEAR = 'StartOfTheYear'


class SalesCreditsReport(CSVReportCreator):
    
    HEADER_FUNC_MAPPING = (
        ('Trade', lambda t: t.Oid()),
        ('Status', lambda t: t.Status()),
        ('Time', lambda t: t.TradeTime()),
        ('Instrument', lambda t: t.Instrument().Name()),
        ('Portfolio', lambda t: t.PortfolioId()),
        ('RelationShipParty', lambda t: t.add_info('Relationship_Party')),
        ('SalesCredit', lambda t: t.SalesCredit()),
        ('Sales_Credit2', lambda t: t.add_info('Sales_Credit2')),
        ('Sales_Credit3', lambda t: t.add_info('Sales_Credit3')),
        ('Sales_Credit4', lambda t: t.add_info('Sales_Credit4')),
        ('Sales_Credit5', lambda t: t.add_info('Sales_Credit5')),
        ('Sales_Credit6', lambda t: t.add_info('Sales_Credit6')),
        ('ValueAddCredits', lambda t: t.add_info('ValueAddCredits')),
        ('ValueAddCredits2', lambda t: t.add_info('ValueAddCredits2')),
        ('ValueAddCredits3', lambda t: t.add_info('ValueAddCredits3')),
        ('ValueAddCredits4', lambda t: t.add_info('ValueAddCredits4')),
        ('ValueAddCredits5', lambda t: t.add_info('ValueAddCredits5')),
        ('SalesPerson', lambda t: t.SalesPerson().Name() if t.SalesPerson() else ""),
        ('SalesPerson2', lambda t: t.add_info('Sales_Person2')),
        ('SalesPerson3', lambda t: t.add_info('Sales_Person3')),
        ('SalesPerson4', lambda t: t.add_info('Sales_Person4')),
        ('SalesPerson5', lambda t: t.add_info('Sales_Person5')),
        ('SalesPerson6', lambda t: t.add_info('Sales_Person6')),
    )
    
    SC_NAMES = ['Sales_Credit2', 'Sales_Credit3', 'Sales_Credit4', 'Sales_Credit5', 'Sales_Credit6']
    VA_NAMES = ['ValueAddCredits', 'ValueAddCredits2', 'ValueAddCredits3', 'ValueAddCredits4', 'ValueAddCredits5']
    AI_FILTER_NAMES = SC_NAMES + VA_NAMES

    
    def __init__(self, file_name, file_suffix, path, start_date, end_date=None):
        super(SalesCreditsReport, self).__init__(file_name, file_suffix, path)
        self.start_date = start_date
        if end_date:
            self.end_date = end_date
        else:
            self.end_date = acm.Time.DateToday()
        
    def _header(self):
        return [header for header, _f in self.HEADER_FUNC_MAPPING]
        
    def _collect_data(self):
        QUERY="""
            SELECT DISTINCT t.trdnbr
            FROM trade t
            WHERE
            t.time > '{start_date}'
            AND t.time < '{end_date}'
            AND t.status NOT IN (1, 7, 8)
            AND t.archive_status = 0
        """.format(start_date=self.start_date, end_date=self.end_date)
        
        LOGGER.info("Selecting trades (start: '%s'; end: '%s')...",
            self.start_date, self.end_date)
            
        res = ael.dbsql(QUERY)
        
        LOGGER.info("Total trades found: %d", len(res[0]))
        LOGGER.info("Filtering trades...")
        trades = [trdnbr[0] for trdnbr in res[0] if self._passes_query(trdnbr[0])]
        LOGGER.info("Trades filtered: %d", len(trades))
        
        for trdnbr in trades:
            trd = acm.FTrade[trdnbr]
            row = [fnc(trd) for _hdr, fnc in self.HEADER_FUNC_MAPPING]
            self.content.append(row)

    def _passes_query(self, trdnbr):
        trd = ael.Trade[trdnbr]
        
        if trd.sales_credit != 0:
            return True
            
        for ai_name in self.AI_FILTER_NAMES:
            if trd.add_info(ai_name) not in ('', 0, '0', '0.0'):
                return True


ael_variables = AelVariableHandler()
ael_variables.add('filename', 
    label='Filename',
    default='SalesCreditsYTD', 
    alt='Filename')
ael_variables.add('output_path',
    label='Output Path',
    default='/services/frontnt/Task/',
    alt='Output Path')
ael_variables.add('start_date',
    label='Start Date',
    cls='string',
    default=START_OF_YEAR,
    mandatory=True,
    alt=("Start Date of time span from which trades will be taken "
         "(format: '2017-03-28' or 'StartOfTheYear')"))
ael_variables.add('end_date',
    label='End Date',
    cls='date',
    default='Today',
    mandatory=True,
    alt=("End Date of time span from which trades will be taken "
         "(format: '2017-03-28')"))


def ael_main(ael_dict):
    if ael_dict['start_date'] == START_OF_YEAR:
        start_date = acm.Time.FirstDayOfYear(acm.Time.DateToday())
    else:
        start_date = acm.Time.DateFromTime(ael_dict['start_date'])
        
    end_date = ael_dict['end_date'].to_string()
    filename = "{0}_{1}".format(ael_dict['filename'], end_date)
    
    LOGGER.info("%s: Generating Sales Credits report...", acm.Time.TimeNow())
    LOGGER.info("Start Date: '%s'", start_date)
    LOGGER.info("End Date: '%s'", end_date)
    
    report = SalesCreditsReport(filename, 'csv', ael_dict['output_path'], 
        start_date, end_date)
        
    report.create_report()
    
    outfile = os.path.join(ael_dict['output_path'], filename + ".csv")
    LOGGER.output(outfile)
    LOGGER.info("%s: Completed successfully.", acm.Time.TimeNow())
