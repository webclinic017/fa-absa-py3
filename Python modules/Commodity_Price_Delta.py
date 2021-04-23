'''
:Author: Andreas Bayer <Andreas.Bayer@absacapital.com>
:Summary: Hedge Feed
price curves.
:Version: 1.0, 2014-04-07
'''

import acm
import FLogger
import os.path
import csv
import math
import traceback, sys
from at_time import to_datetime, to_date, acm_date, add_months
from at_ael_variables import AelVariableHandler
from collections import namedtuple

ael_gui_parameters = {
    'windowCaption' : 'Price Curve Delta'
}

ael_variables = AelVariableHandler()

ael_variables.add(
    'extension_context',
    label = 'Commodity Extension Context',
    cls = 'FExtensionContext',
    multiple = True
)

ael_variables.add(
    'price_curves',
    label = 'Price Curves',
    cls = 'FPriceCurve',
    multiple = True
)

ael_variables.add(
    'filter_name',
    label = 'Filter Label',
    cls = 'string'
)

ael_variables.add(
    'trade_filter',
    label = 'Trades',
    cls = 'FTrade',
    multiple = True
)

ael_variables.add(
    'end_date',
    label = 'Benchmark Maturity',
    cls = 'date',
    default = acm.Time().DateToday(),
    alt = 'Exclude benchmarks by maturity'
)

ael_variables.add(
    'out_file',
    label = 'Output File',
    cls = 'string',
    default = 'C:\temp\Commodity_Price_Delta.csv'
)

ael_variables.add(
    'exception_report',
    label = 'NaN Exception Report',
    cls = 'string',
    default = 'C:\temp\Commodity_Price_Delta_NaNException.csv'
)

ael_variables.add(
    'out_mode',
    label = 'Output Mode',
    cls = 'string',
    collection = [
        'csv'
    ],
    default = 'csv'
)

ael_variables.add(
    'log_directory',
    label='Log Directory',
    cls = 'string'
)

ael_variables.add(
    'ignore_zero_nan',
    label = 'Ignore Nan to Zero',
    cls = 'bool',
    default = 'True'
)

ael_variables.add(
    'log_level',
    label='Log Level',
    cls = 'string',
    collection = [
        'DEBUG', 
        'INFO', 
        'WARNING', 
        'ERROR'
    ],
    default = 'INFO',
)

LOGGER = None
LOG_LEVEL = {'DEBUG': 2, 'INFO': 1, 'WARNING':3, 'ERROR':4}

class PriceCurveDeltaReport(object):
    REPORT_ENTRY = namedtuple('PriceCurveDeltaReportEntry', [
        'portfolio',
        'ins_type',
        'disc_idx',
        'proj_idx',
        'tenor',
        'label',
        'months',
        'market_price',
        'notnl_delta',
        'usd_exposure',
        'notnl_delta_up',
        'usd_exposure_up',
        'notnl_delta_down',
        'usd_exposure_down'
    ])
    
    REPORT_HEADER = {
        'portfolio': 'Portfolio',
        'ins_type': 'Ins-Type',
        'disc_idx': 'Disc-Idx',
        'proj_idx': 'Proj-Idx',
        'tenor': 'Tenor',
        'label': 'Label',
        'months': 'Months',
        'market_price': 'Market_Price',
        'notnl_delta': 'Notnl_Delta',
        'usd_exposure': 'USDExposure',
        'notnl_delta_up': 'Notnl_Delta+1%',
        'usd_exposure_up': 'USDExposureUp',
        'notnl_delta_down': 'Notnl_Delta-1%',
        'usd_exposure_down': 'USDExposureDown'
    }
    
    def __init__(self, price_curves, extension_context, filter_name, trade_groups, exp_date, out_file = '', exception_report = '', ignore_zero_nan = 'True'):
        self.report_data = []
        self.exception_data = []
        self.price_curves = price_curves
        self.filter_name = filter_name
        self.trade_groups = trade_groups
        self.exp_date = exp_date
        self.out_file = out_file
        self.exception_report = exception_report
        self.extension_context = extension_context
        self.generate_zeros = ignore_zero_nan
    
    @staticmethod
    def benchmark_expiry_comparator(instr1, instr2):
        '''Comparator for sorting benchmarks by their expiration dates.'''
        d1 = to_datetime(instr1.Instrument().ExpiryDate())
        d2 = to_datetime(instr2.Instrument().ExpiryDate())
        if d1 < d2:
            return -1
        elif d2 > d1:
            return 1
        else:
            return 0
    
    @staticmethod
    def report_entry_comparator(entry1, entry2):
        '''Comparator for sorting report entries by benchmark expiration date'''
        d1 = to_datetime(entry1.label)
        d2 = to_datetime(entry2.label)
        if d1 < d2:
            return -1
        elif d2 > d1:
            return 1
        else:
            return 0

    def sort_benchmarks_by_expiry(self, benchmarks):
        return sorted(benchmarks, cmp = PriceCurveDeltaReport.benchmark_expiry_comparator)
    
    def sorted_report_data(self):
        return sorted(self.report_data, cmp = PriceCurveDeltaReport.report_entry_comparator)
        
    def sorted_exception_data(self):
        return sorted(self.exception_data, cmp = PriceCurveDeltaReport.report_entry_comparator)
    
    def create_time_buckets(self, all_benchmarks):
        '''Create time buckets b(i-1) < t <= b(i) using the expiry dates 
        of the benchmarks in a collection of benchmarks.'''
        
        buckets = []
        sorted_benchmarks = self.sort_benchmarks_by_expiry(all_benchmarks)
        
        for b in sorted_benchmarks:
            b = b.Instrument()
            bd = acm.FFixedDateTimeBucketDefinition()
            bd.FixedDate(b.ExpiryDate())
            bd.DiscardIfExpired(True)
            bd.UninterruptedSequence(True)
            buckets.append(bd)
        
        definition = acm.TimeBuckets().CreateTimeBucketsDefinition(
            acm.Time().DateToday(), 
            buckets, 
            False, 
            False, 
            False, 
            False, 
            False
        )
        
        def_conf = acm.TimeBuckets().CreateTimeBucketsDefinitionAndConfiguration(definition)
        time_buckets = acm.TimeBuckets().CreateTimeBuckets(def_conf)
        
        return time_buckets

    def _price_curve_delta(self, trades, price_curve):
        '''Calculate the price curve delta for certain time buckets, which are defined 
        by the benchmarks of the price curve. The rest time bucket is currently not 
        considered.'''
        CONTEXT = self.extension_context
        SHEET_TYPE = 'FPortfolioSheet'
        CALC_SPACE = acm.Calculations().CreateCalculationSpace(CONTEXT, SHEET_TYPE)
        COLUMN_ID = 'Price Curve Delta Bucket'
        
        benchmarks = price_curve.Benchmarks()
        
        buckets = self.create_time_buckets(benchmarks)
        column_config = acm.Sheet.Column().ConfigurationFromTimeBuckets(buckets)
        
        query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        op_node = query.AddOpNode('OR')
        for trade in trades:
            op_node.AddAttrNode('Oid', 'EQUAL', trade.Oid())
        folder = acm.FASQLQueryFolder()
        folder.AsqlQuery(query)
        top_node = CALC_SPACE.InsertItem(folder)
        
        CALC_SPACE.Refresh()
        
        node = top_node
        calc = CALC_SPACE.CreateCalculation(node, COLUMN_ID, column_config)
        
        return calc.Value()
    
    def write_NaN_exception_report(self):
        '''write report_data to a csv file'''
        header_dict = {}
        
        for column in PriceCurveDeltaReport.REPORT_ENTRY._fields:
            header_dict[column] = PriceCurveDeltaReport.REPORT_HEADER[column]
    
        with open(self.exception_report, 'wb') as f:
            writer = csv.DictWriter(
                f,
                PriceCurveDeltaReport.REPORT_ENTRY._fields,
                delimiter=';',
                lineterminator = '\n'
            )
            writer.writerow(header_dict)
            print 'About to write the file entry'
            for exception_data in self.sorted_exception_data():
                writer.writerow(exception_data._asdict())
    
    def write_csv_report(self):
        '''write report_data to a csv file'''
        header_dict = {}
        
        for column in PriceCurveDeltaReport.REPORT_ENTRY._fields:
            header_dict[column] = PriceCurveDeltaReport.REPORT_HEADER[column]
        
        with open(self.out_file, 'wb') as f:
            writer = csv.DictWriter(
                f, 
                PriceCurveDeltaReport.REPORT_ENTRY._fields, 
                delimiter=';', 
                lineterminator = '\n'
            )
            writer.writerow(header_dict)
            for report_entry in self.sorted_report_data():
                writer.writerow(report_entry._asdict())
                
    def _mtm_price(self, instr, date):
        CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection(
            acm.GetDefaultContext()
        )
        mtm_price = instr.Underlying().Calculation().MarkToMarketPrice(
            CALC_SPACE, 
            date, 
            instr.Underlying().Currency()
        )
        return mtm_price.Number()
    
    def _determine_index(self, all_benchmarks, benchmark):
        '''Determine the position of a benchmark in an collection of benchmarks
        sorted by expiry'''
        
        sorted_benchmarks = self.sort_benchmarks_by_expiry(all_benchmarks)
        idx=0
        for b in sorted_benchmarks:
            b = b.Instrument()
            benchmark_expiry = to_date(to_datetime(b.ExpiryDate()))
            if benchmark_expiry < self.exp_date:
                continue 
            if b.Instrument().Name() == benchmark.Name():
                bucket_index = idx
                break
            idx+=1
        return bucket_index
    
    def calculate_report_data(self):
        for price_curve in self.price_curves:
            if not self.trade_groups.has_key(price_curve.Name()):
                continue
            LOGGER.LOG('Processing curve %s...' % price_curve.Name())
            delta = self._price_curve_delta(
                self.trade_groups[price_curve.Name()]['trades'], 
                price_curve
            )
            benchmarks = price_curve.Benchmarks()
            for benchmark in benchmarks: 
                benchmark_instr = benchmark.Instrument()
                LOGGER.DLOG('Processing Benchmark: %s' % (
                    benchmark_instr.Name()))
                benchmark_expiry = to_date(to_datetime(benchmark_instr.ExpiryDate()))
                if benchmark_expiry >= self.exp_date:
                    benchmark_expiry = to_date(to_datetime(benchmark_instr.ExpiryDate()))
                    today = to_date(to_datetime('TODAY'))
                    months = 0
                    nanDetermineIndex = 0
                    if not math.isnan(float(delta[self._determine_index(benchmarks, benchmark_instr)].Number())):
                        nanDetermineIndex = float(delta[self._determine_index(benchmarks, benchmark_instr)].Number())
                    else:
                        exception_data = PriceCurveDeltaReport.REPORT_ENTRY(
                            self.filter_name,
                            '', 
                            'LIBOR.USD', 
                            ','.join(list(self.trade_groups[price_curve.Name()]['commodity_labels'])), 
                            '',
                            benchmark_instr.ExpiryDate(),
                            '%sM'% months,
                            self._mtm_price(benchmark_instr, acm.Time().DateToday()),
                            float(delta[self._determine_index(benchmarks, benchmark_instr)].Number()),
                            '',
                            '',
                            '',
                            '',
                            ''
                            )
                        self.exception_data.append(exception_data)
                        
                    while True:
                        if add_months(today, months) >= benchmark_expiry:
                            break
                        months+=1
                    if self.generate_zeros == True and math.isnan(float(delta[self._determine_index(benchmarks, benchmark_instr)].Number())):
                        print 'Ignoring this line and writing the next'
                        continue
                    else:
                        report_entry = PriceCurveDeltaReport.REPORT_ENTRY(
                            self.filter_name, '', 'LIBOR.USD', ','.join(list(self.trade_groups[price_curve.Name()]['commodity_labels'])), '', benchmark_instr.ExpiryDate(), '%sM'% months,
                            self._mtm_price(benchmark_instr, acm.Time().DateToday()),
                            nanDetermineIndex, '', '', '', '', '')
                        self.report_data.append(report_entry)
                    
            LOGGER.LOG('Finished curve %s.' % price_curve.Name())

def get_commodity_label(trades):
    l = set()
    for trade in trades:
        if trade.Instrument().AdditionalInfo().Commodity_Label():
            l.add(trade.Instrument().AdditionalInfo().Commodity_Label())
    return ','.join(list(l))

def mapped_price_curve(trade, extension_context):
    '''get name of mapped price curve'''
    CONTEXT = extension_context
    SHEET_TYPE = 'FTradeSheet'
    CALC_SPACE = acm.Calculations().CreateCalculationSpace(CONTEXT, SHEET_TYPE)
    PRICE_CURVE = 'BasePriceCurveInTheoreticalValue'
    
    top_node = CALC_SPACE.InsertItem(trade)
    CALC_SPACE.Refresh()
    base_curve = CALC_SPACE.CreateCalculation(top_node, PRICE_CURVE)
    return base_curve.Value().Name()

def get_trade_groups(trade_filter, extension_context):
    '''group trades by mapped price curve'''
    trade_groups = {}
    mapping = {}
    for trade in trade_filter:
        try:
            if mapping.has_key(trade.Instrument().Name()):
                price_curve = mapping[trade.Instrument().Name()]
            else:
                price_curve = mapped_price_curve(trade, extension_context)
                mapping[trade.Instrument().Name()] = price_curve
                
            if not trade_groups.has_key(price_curve):
                trade_groups[price_curve] = {'trades': [trade]}
                trade_groups[price_curve]['commodity_labels'] = set()
            else:
                trade_groups[price_curve]['trades'].append(trade)
                
            commodity_label = trade.Instrument().AdditionalInfo().Commodity_Label()
            if commodity_label:
                trade_groups[price_curve]['commodity_labels'].add(commodity_label)
                
        except Exception, e:
            LOGGER.LOG('Could not process trade %s in instrument %s. Skipped.' % (
                trade.Oid(), trade.Instrument().Name()))
            LOGGER.DLOG('Traceback: %s' % (
                repr(traceback.extract_stack())))
            LOGGER.DLOG(e)
    return trade_groups

def _init_logging(log_directory, log_level):
    '''initialize logging'''
    global LOGGER
    LOGGER = FLogger.FLogger('CRT Feed')
    LOGGER.Reinitialize(
        level=LOG_LEVEL[log_level], 
        keep=False, 
        logOnce=False, 
        logToConsole=False, 
        logToPrime=True, 
        logToFileAtSpecifiedPath=os.path.join(log_directory, 
            'Repcube_Hedge_Report_%s.log' % acm_date('TODAY')
        ), 
        filters=None)

def ael_main(ael_params):
    _init_logging(ael_params['log_directory'], ael_params['log_level'])
    LOGGER.LOG('STARTING PRICE CURVE DELTA REPORT GENERATION...')
    
    exp_date = to_date(ael_params['end_date'])
    
    generate_NaN_zeros = ael_params['ignore_zero_nan']
    
    try:
        trade_groups = get_trade_groups(
            ael_params['trade_filter'],
            ael_params['extension_context']
        )
        report = PriceCurveDeltaReport(
            ael_params['price_curves'],
            ael_params['extension_context'],
            ael_params['filter_name'],
            trade_groups,
            exp_date,
            ael_params['out_file'],
            ael_params['exception_report'],
            ael_params['ignore_zero_nan']
        )
        report.calculate_report_data()
        if ael_params['out_mode'] == 'csv':
            report.write_csv_report()
            print 'Reached NAN write exception report'
            report.write_NaN_exception_report()
            
    except Exception, e:
        exc_traceback = sys.exc_info()
        LOGGER.LOG('Report Generation failed: %s. Traceback: %s' % (
            e, traceback.format_exception(*exc_traceback)))
        LOGGER.LOG('REPORT GENERATION FAILED')
        return
    LOGGER.LOG('COMPLETED SUCCESSFULLY')
    LOGGER.LOG('WROTE SECONDARY OUTPUT TO: %s' % ael_params['out_file'])
    LOGGER.LOG('WROTE EXCEPTION OUTPUT TO: %s' % ael_params['exception_report'])
