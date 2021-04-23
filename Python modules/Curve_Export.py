'''--------------------------------------------------------------------------------
Purpose         : This code addresses ABITFA-3515
                : For each Yield Curve and Price Index specified,
                    the relevant values are exported for the number
                    of years specified.
Notes           : Each run results in data being appended to a file.
                    Therefore, the output file will become very large
                    over time. The maximum file size is system-dependent
                    and has not been catered for in this code. The user
                    opted to manually manage the files, rather than have
                    the code produce a rolling period.
                : Reruns on the same day overwrite existing data.
Department      : Treasury
Requester       : Jeandre Immelman
Developer       : Mike Schaefer
CR Number       : CHNG0003051127
-----------------------------------------------------------------------------------
'''

import acm
import ael
import os
import csv
import time
import sys
import at
import ABSA_Rate

DEFAULT_PRICE_INDICES = 'SACPI'
DEFAULT_YIELD_CURVES = 'EUR-SWAP,EUR-BASIS,USD-SWAP,ZAR-SWAP,ZAR-BASIS,ZAR-CPI,ZAR-PRIME'
SOURCE_PATH = '/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/TradingManager/PCG_Group_Treasury_Hedging_Rates'
DESTINATION_PATH = '/services/frontnt/Task'
START_DATE_ACM = acm.Time.DateToday()
START_DATE_AEL = ael.date_today()

ael_variables = at.ael_variables.AelVariableHandler()
ael_variables.add('number_of_years', mandatory=1, label='Future Years',
                  default=30)
ael_variables.add_directory('source_path', mandatory=1, label='Source Path',
                  default=SOURCE_PATH)
ael_variables.add_directory('destination_path', mandatory=1, label='Destination Path',
                  default=DESTINATION_PATH)
ael_variables.add('yield_curves', mandatory=0, label='Yield Curves',
                  default=DEFAULT_YIELD_CURVES,
                  collection = acm.FYieldCurve.Select(''),
                  multiple = 1)
ael_variables.add('price_indices', mandatory=0, label='Price Indices',
                  default=DEFAULT_PRICE_INDICES,
                  collection = acm.FPriceIndex.Select(''),
                  multiple = 1)

def log(msg):
    print "%s - %s" %(time.strftime("%Y-%m-%d %H:%M:%S"), msg)

def create_input_file(source_path, export_object_name):
    try:
        open(source_path + export_object_name + '.csv', 'a').close()
    except Exception, e:
        log(e)
        sys.exit(e)

def write_yield_curves(reader, writer, number_of_years, yield_curve, empty_list, rerun):
    report_date = acm.Time.DateAddDelta(START_DATE_ACM, 0, 0, 1)
    end_date = acm.Time.DateAddDelta(START_DATE_ACM, number_of_years, 0, 0)
#-------------------------------------------------------------------------
# Note that the users explicitly asked for the following parameters to be
#   hard-coded. These values differ from the curve definitions in
#   front for Attribute Spread Curves, but the users always require
#   the parameters to be overriden.
    calc_type = 'Spot Rate'
    rate_type = 'Annual Comp'
    day_count = 'Act/365'
    if yield_curve.Name() == ('USD-SWAP'):
        day_count = 'Act/360'
#-------------------------------------------------------------------------    
    if yield_curve.Class().IncludesBehavior(acm.FAttributeSpreadCurve):
        curr = yield_curve.Attributes()[0].Currency()
    else:
        curr = None
    if yield_curve.RealTimeUpdated():
        try:
            yield_curve.Calculate()
            yield_curve.Simulate()
        except:
            print 'Calculate failed for curve: ', yield_curve.Name()        
    ircurveinfo = ABSA_Rate.ABSA_get_ircurveinfo(yield_curve, curr)
    for row in reader:
        row = row[:rerun]
        if report_date <= end_date:
            writer.writerow(row + [ircurveinfo.Rate(START_DATE_ACM, report_date, \
                        rate_type, day_count, calc_type, None, 0)*100])
        else:
            writer.writerow(row)
        report_date = acm.Time.DateAddDelta(report_date, 0, 0, 1)
    while report_date <= end_date:
        writer.writerow(empty_list + [ircurveinfo.Rate(START_DATE_ACM, report_date, \
                        rate_type, day_count, calc_type, None, 0)*100])
        report_date = acm.Time.DateAddDelta(report_date, 0, 0, 1)

def write_price_indices(reader, writer, number_of_years, price_index, empty_list, rerun):
# The user requested that the ael method forward_price be used    
    price_index = ael.Instrument[price_index.Name()]
    report_date = START_DATE_AEL.add_days(1)
    end_date = START_DATE_AEL.add_years(number_of_years)
    for row in reader:
        row = row[:rerun]
        if report_date <= end_date:
            writer.writerow(row + [price_index.forward_price(report_date)])
        else:
            writer.writerow(row)
        report_date = report_date.add_days(1)
    while report_date <= end_date:
        writer.writerow(empty_list + [price_index.forward_price(report_date)])
        report_date = report_date.add_days(1)

def calculate_and_write_output(inputfile, outputfile, export_object, number_of_years):
    rerun = None
    try:
        with open(inputfile, 'rb') as csvinput:
            with open(outputfile, 'wb') as csvoutput:
                writer = csv.writer(csvoutput, lineterminator = '\n')
                reader = csv.reader(csvinput)
                if os.stat(inputfile).st_size > 0:
                    header_row = next(reader)
                    if header_row[-1] == START_DATE_ACM:
                        header_row = header_row[:-1]
                        rerun = -1
                else:
                    header_row = []
                column_count = len(header_row)
                empty_list = [None] * column_count
                writer.writerow(header_row + [START_DATE_ACM])
                if export_object.Class().IncludesBehavior(acm.FYieldCurve):
                    write_yield_curves(reader, writer, number_of_years, export_object, empty_list, rerun)
                elif export_object.Class().IncludesBehavior(acm.FPriceIndex):
                    write_price_indices(reader, writer, number_of_years, export_object, empty_list, rerun)
    except Exception, e:
        log(e)
        sys.exit(e)

def export_data(source_path, destination_path, export_objects, number_of_years):
    for export_object in export_objects:
        export_object_name = export_object.Name()
        inputfile = source_path + export_object_name + '.csv'
        outputfile = destination_path + export_object_name + '.csv'
        if not os.path.exists(inputfile):
            create_input_file(source_path, export_object_name)
        calculate_and_write_output(inputfile, outputfile, export_object, number_of_years)
        log('%s written.'%outputfile)

def ael_main(input_dictionary):
    source_path = str(input_dictionary['source_path']) + '/'
    destination_path = str(input_dictionary['destination_path']) + '/'
    yield_curves = []
    price_indices = []
    number_of_years = int(input_dictionary['number_of_years'])
    yield_curve_names = list(input_dictionary['yield_curves'])
    price_indices_names = list(input_dictionary['price_indices'])
    for yield_curve_name in yield_curve_names:
        yield_curves.append(acm.FYieldCurve[yield_curve_name])
    for price_index_name in price_indices_names:
        price_indices.append(acm.FPriceIndex[price_index_name])
    export_data(source_path, destination_path, yield_curves, number_of_years)
    export_data(source_path, destination_path, price_indices, number_of_years)
    log('Task complete.\n' \
        '\t%s yield curve file(s) and\n' \
        '\t%s price index file(s) written to\n' \
        '\t%s'%(len(yield_curves), len(price_indices), destination_path))
