"""-----------------------------------------------------------------------------------------
MODULE
    m2_surface_template

DESCRIPTION
    Date                : 2020-10-12
    Purpose             : This creates a volatility surface template with div points per 
                          expiry for given volatility structures
    Department and Desk : PCG Val & Risk Control
    Requester           : Ryan Fagri
    Developer           : Qaqamba Ntshobane

HISTORY
=============================================================================================
Date            Change no       Developer               Description
---------------------------------------------------------------------------------------------
2020-10-12      PCGDEV-570      Qaqamba Ntshobane       Initial Implementation
2021-01-29      PCGDEV-662      Qaqamba Ntshobane       Cosmetic improvements

ENDDESCRIPTION
------------------------------------------------------------------------------------------"""

import acm
import os
import xlsxwriter
import FRunScriptGUI
from at_logging import getLogger
from collections import OrderedDict
from at_ael_variables import AelVariableHandler

outputSelection = FRunScriptGUI.DirectorySelection()
directorySelection = acm.FFileSelection()
directorySelection.PickDirectory(True)
directorySelection.SelectedDirectory(r"F:")

LOGGER = getLogger(__name__)
OUTPUT_FILENAME = 'vol_surface_template.xlsx'

ael_variables = AelVariableHandler()
ael_variables.add(
    'volatility_structures',
    label = 'Volatility Structure(s)',
    cls = acm.FVolatilityStructure,
    collection=acm.FVolatilityStructure.Select(""),
    multiple = True,
    default = 'EQ_ALSI_SSkew, EQ_SWIX_SSkew, ZAR/NPN_Skew'
    )
ael_variables.add(
    'index',
    label = 'Index',
    cls = acm.FInstrument,
    collection=acm.FInstrument.Select("insType='EquityIndex'"),
    default = 'ZAR/ALSI'
    )
ael_variables.add(
    'file_directory',
    label = 'File Drop Location',
    cls = directorySelection,
    default = directorySelection,
    multiple = True
    )


class VolStructProcessor(object):

    def __init__(self, index, vol_structure):

        self.index = index
        self.table_headings = []
        
        if not vol_structure.Points()[0].Benchmark():
            vol_structure = vol_structure.Name().replace('_Skew', '')
            self.underlying = acm.FInstrument[vol_structure]
        else:
            self.underlying = vol_structure.Points()[0].Benchmark().Underlying()

    def get_report_data(self, vol_struct):

        report_dict = {}
        volatility_points_dict = self.get_vol_points(vol_struct)

        for expiry, points in volatility_points_dict.items():
            if len(points) != len(self.table_headings):
                self.add_headers(points)

            sorted_points = sorted(points, key=lambda x: x.Strike())

            report_dict.setdefault(expiry, [])
            report_dict[expiry].append(expiry)
            report_dict[expiry].append(self.underlying.Name())

            for point in sorted_points:
                report_dict[expiry].append(point.Volatility() * 100)
            report_dict[expiry].append(0.0)

        self.extend_headers()

        return self.table_headings, report_dict

    @staticmethod
    def get_vol_points(vol_structure):

        vol_points = vol_structure.Points()
        points = {}

        for vol_point in vol_points:
            expiry = vol_point.ExpiryDay()

            points.setdefault(expiry,[])
            points[expiry].append(vol_point)
        return points

    def add_headers(self, points):

        for point in points:
            if point.Strike() not in self.table_headings:
                self.table_headings.append(int(point.Strike()))
        self.table_headings.sort()

    def extend_headers(self):

        table_headings = ["Expiry", "Underlying"]
        table_headings.extend(self.table_headings)
        table_headings.append("Dividend Pts")
        self.table_headings = table_headings

    def get_dividends(self):

        latest_div = self.underlying.Dividends()
        div_stream = self.underlying.Name()

        if latest_div:
            latest_div = latest_div[-1]

        div_stream = div_stream.split("/")[1]
        div_estimates = acm.FDividendEstimate.Select("dividendStream="+div_stream)

        return [latest_div] + list(div_estimates)

    def get_weighting(self):

        combination_ins = acm.FCombInstrMap.Select("combination='%s' and instrument='%s'"
                                                    %(self.index.Name(), self.underlying.Name()))
        if combination_ins:
            return combination_ins[0].Weight()
        return 1

    def get_dividend_point(self, div_amount):

        weight = 1

        if not self.underlying.IsKindOf("FEquityIndex"):
            weight = self.get_weighting()
        index_factor = self.index.Factor()

        return weight / index_factor * div_amount

    @staticmethod
    def get_ymd(dates=[], date_type=0):

        return [acm.Time.DateToYMD(date)[date_type] for date in dates]

    def append_div_points(self, benchmark_dict):

        divs = self.get_dividends()

        if not divs[0]:
            return

        for index, div in enumerate(divs):

            for expiry in benchmark_dict.keys():
                ex_div = div.ExDivDay()
                next_ex_div = None

                if index+1 < len(divs):
                    next_ex_div = divs[index+1].ExDivDay()

                ex_div_year, expiry_year =  self.get_ymd([ex_div, expiry], 0)
                year_diff = ex_div_year - expiry_year

                if ex_div_year <= expiry_year and year_diff not in list(range(-1,1)):
                    break

                dividend_point = self.get_dividend_point(div.Amount())

                if next_ex_div and ex_div < expiry < next_ex_div:
                    benchmark_dict[expiry][-1] = dividend_point


class ReportProcessor(object):

    def __init__(self, output_file):

        self.output_file = output_file
        self.workbook = ''
        self.m2_surface_sheet = ''

    def create_report(self):

        self.workbook = xlsxwriter.Workbook(self.output_file)
        self.m2_surface_sheet = self.workbook.add_worksheet('M2_Surface_Template')
        return self.workbook, self.m2_surface_sheet

    @staticmethod
    def process_headers(headers):

        return [{'header':str(head)} for head in headers]

    def add_to_report(self, headers, first_row, data):

        last_column = xlsxwriter.utility.xl_col_to_name(len(headers)-1)
        last_row = (len(data) + 1 + first_row)

        self.m2_surface_sheet.add_table('A%s:%s%s' %(first_row, last_column, last_row), {'data': data, 'columns': headers})

    def close_report(self):

        self.workbook.close()
        LOGGER.info('Report saved to . %s' % str(self.output_file))


def ael_main(dictionary):

    index = dictionary['index']
    vol_structs = dictionary['volatility_structures']
    file_directory = dictionary['file_directory']
    filename = os.path.join(str(file_directory), OUTPUT_FILENAME)
    first_row = 1

    report_processor = ReportProcessor(filename)
    report_processor.create_report()

    for vol_struct in vol_structs:
        vol_struct_processor = VolStructProcessor(index, vol_struct)
        headers, data = vol_struct_processor.get_report_data(vol_struct)

        data = OrderedDict(sorted(data.items()))
        vol_struct_processor.append_div_points(data)

        headers = ReportProcessor.process_headers(headers)
        report_processor.add_to_report(headers, first_row, data.values())
        first_row += (len(data.values()) + 3)
    report_processor.close_report()

