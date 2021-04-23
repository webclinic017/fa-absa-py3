"""-----------------------------------------------------------------------------
PURPOSE              :  Client Valuation Statements Automation
                        This module implements statements reporting logic used
                        to generate XML, PDF and XLSX.
DESK                 :  PCG Collateral
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2019-02-14  CHG1001362755  Libor Svoboda       Initial Implementation (FEC)
2019-03-14  CHG1001488095  Libor Svoboda       Enable Option statements
2020-06-03  CHG0103217     Libor Svoboda       Add SBL client statements
2020-06-23  CHG0108121     Libor Svoboda       Enable SBL Open Position XLSX
"""
import datetime
import os
import xml.etree.ElementTree as ET

import xlsxwriter

import acm
import XMLReport
from statements_params import (DATE_PATTERN_VALUES, DISCLAIMER_VALUATIONS, 
                               DATE_PATTERN_DOCS, FPARAMS, ABSA_ADDRESS_PARAM,
                               VALUATIONS_TEL_PARAM, ABSA_WEB_PARAM,
                               DATE_PATTERN_MONTH, SBL_ACC_NAME_PARAM,
                               SBL_BANK_PARAM, SBL_ACC_NUM_PARAM, 
                               SBL_BRANCH_PARAM, SBL_SWIFT_PARAM,
                               SBL_OPS_TEL_PARAM, SBL_OPS_EMAIL_PARAM,
                               SBL_COLL_TEL_PARAM, SBL_COLL_EMAIL_PARAM,
                               DISCLAIMER_SBL_MARGIN_CALL, SBL_DIV_ACC_NAME_PARAM,
                               SBL_DIV_ACC_NUM_PARAM, SBL_DIV_BRANCH_PARAM,
                               DISCLAIMER_SBL_DIVIDEND_NOTIFICATION,
                               ABSA_VAT_NBR_PARAM)
from statements_util import format_date, get_param_value


def contact_from_pty(pty, contact):
    if contact.Address2() == contact.City():
        city = [contact.Address2()]
    else:
        city = [contact.Address2(), contact.City()]
    return {
        'name': pty.Fullname(),
        'address': ([contact.Address()] + city 
                    + [contact.Country(), contact.Zipcode()]),
    }


def mktable(columns, rows, 
            size='normal', header=None, borderwidth='0.5mm',
            template_name='Table', **kwargs):
    table = ET.Element(template_name)
    if size:
        table.attrib['size'] = size
    if borderwidth:
        table.attrib['borderwidth'] = borderwidth
    if header:
        table.attrib['tableheader'] = header
    for key, value in kwargs.iteritems():
        table.attrib[key] = value

    columns_element = ET.SubElement(table, 'Columns')
    for label, spec in columns.iteritems():
        column_element = ET.SubElement(columns_element, 'Column')
        column_element.text = label
        for key, value in spec.iteritems():
            column_element.attrib[key] = value
    
    labels = columns.keys()
    rows_element = ET.SubElement(table, 'Rows')
    for row in rows:
        row_element = ET.SubElement(rows_element, 'Row')
        if hasattr(row, 'is_summary'):
            row_element.attrib['summary'] = 'true'
        if hasattr(row, 'is_subsummary'):
            row_element.attrib['subsummary'] = 'true'
        for index, cell in enumerate(row):
            cell_element = ET.SubElement(row_element, 'Cell')
            cell_element.text = cell
            if 'alignment' in columns[labels[index]]:
                cell_element.attrib['alignment'] = columns[labels[index]]['alignment']
    return table


def mktext(text, **kwargs):
    """Create caption block."""
    element = ET.Element('Caption')
    element.text = str(text)
    for key, value in kwargs.iteritems():
        element.attrib[key] = value
    return element


class XLSXReportGenerator(object):
    
    wb_settings = {
        'nan_inf_to_errors': True,
        'default_date_format': 'dd/mm/yyyy',
    }
    file_extension = '.xlsx'
    
    def __init__(self, output_dir):
        self._output_dir = output_dir
        self._worksheet = None
        self._root = ''
        self._percent_format = None
        self._max_col_count = 0
        self._current_row = 0
    
    def _col_count(self):
        if self._max_col_count:
            return self._max_col_count
        for table in self._root.findall('Content/Table[@dataset="main"]'):
            cols = len(table.findall('Columns/Column'))
            self._max_col_count = max(cols, self._max_col_count)
        return self._max_col_count
    
    def _add_merged_row(self, text, spacing=1, col_start=0, row_format=None):
        self._worksheet.merge_range(self._current_row, col_start, self._current_row, 
                                    self._col_count() - 1, text, row_format)
        self._current_row += spacing
    
    def _add_data(self, table):
        columns = table.findall('Columns/Column')
        rows = table.findall('Rows/Row')
        col_type = {}
        for col_index, column in enumerate(columns):
            self._worksheet.write(self._current_row, col_index, column.text)
            col_type[col_index] = column.get('datatype')
        self._current_row += 1
        for row in rows:
            if row.get('summary'):
                continue
            cells  = row.findall('Cell')
            for col_index, cell in enumerate(cells):
                if not cell.text:
                    self._worksheet.write_blank(self._current_row, col_index, None)
                    continue
                formatting = col_type[col_index]
                if formatting == 'float':
                    self._worksheet.write_number(self._current_row, col_index, 
                                                 float(cell.text.replace(',', '')))
                elif formatting == 'percent':
                    self._worksheet.write_number(self._current_row, col_index, 
                                                 float(cell.text.replace(',', '').replace('%', '')),
                                                 self._percent_format)
                elif formatting == 'int':
                    self._worksheet.write_number(self._current_row, col_index, int(cell.text))
                elif formatting == 'datetime':
                    dt = datetime.datetime.strptime(cell.text, DATE_PATTERN_VALUES)
                    self._worksheet.write_datetime(self._current_row, col_index, dt)
                else:
                    self._worksheet.write(self._current_row, col_index, cell.text)
            self._current_row += 1
    
    def _add_disclaimer(self):
        disclaimer = self._root.findall('Content/Disclaimer/Value')
        if not len(disclaimer):
            return
        self._add_merged_row('Disclaimer')
        for row in disclaimer:
            self._add_merged_row(row.text)
    
    def create(self, xml_string, filename):
        self._current_row = 0
        report_path = os.path.join(self._output_dir, 
                                   filename + self.file_extension)
        workbook = xlsxwriter.Workbook(report_path, self.wb_settings)
        self._percent_format = workbook.add_format({'num_format': '0.00"%"'})
        self._worksheet = workbook.add_worksheet()
        self._root = ET.fromstring(xml_string)
        self._add_merged_row(self._root.find('Client/Name').text, 2)
        captions = self._root.findall('Content/Caption')
        tables = self._root.findall('Content/Table[@dataset="main"]')
        for caption, table in zip(captions, tables):
            self._add_merged_row(caption.text, 2)
            self._add_merged_row(table.get('tableheader'))
            self._add_data(table)
            self._add_merged_row(table.get('tablefooter'), 2)
        self._add_disclaimer()
        workbook.close()
        return report_path


class SBLMovementXLSXGenerator(XLSXReportGenerator):
    
    def create(self, xml_string, filename):
        self._current_row = 0
        report_path = os.path.join(self._output_dir, 
                                   filename + self.file_extension)
        workbook = xlsxwriter.Workbook(report_path, self.wb_settings)
        self._worksheet = workbook.add_worksheet()
        self._root = ET.fromstring(xml_string)
        self._add_merged_row(self._root.find('Client/Name').text, 2)
        caption = self._root.find('Content/Caption')
        self._add_merged_row(caption.text, 2)
        tables = self._root.findall('Content/Table[@dataset="main"]')
        for table in tables:
            self._add_merged_row(table.get('tableheader'))
            self._add_data(table)
            self._add_merged_row(table.get('tablefooter'), 2)
        self._add_disclaimer()
        workbook.close()
        return report_path


class SBLSummaryPosXLSXGenerator(XLSXReportGenerator):
    
    format_default = {
        'font_name': 'Arial',
        'font_size': 8,
        'border': 0,
    }
    format_caption = {
        'font_name': 'Arial',
        'font_size': 10,
        'bold': True,
    }
    format_header = {
        'font_name': 'Arial',
        'font_size': 8,
        'bold': True,
        'bottom': 1,
    }
    format_title = {
        'font_name': 'Arial',
        'font_size': 8,
        'bold': True,
    }
    format_summary = {
        'font_name': 'Arial',
        'font_size': 8,
        'bold': True,
        'top': 1,
    }
    
    def _add_data(self, table, summary_format=None):
        columns = table.findall('Columns/Column')
        rows = table.findall('Rows/Row')
        col_type = {}
        for col_index, column in enumerate(columns):
            col_type[col_index] = column.get('datatype')
        cell_format = None
        for row in rows:
            cells  = row.findall('Cell')
            for col_index, cell in enumerate(cells):
                if row.get('summary') and summary_format:
                    if col_index in summary_format:
                        cell_format = summary_format[col_index]
                if not cell.text:
                    self._worksheet.write_blank(self._current_row, col_index, None, cell_format)
                    continue
                formatting = col_type[col_index]
                if formatting == 'float':
                    self._worksheet.write_number(self._current_row, col_index, 
                                                 float(cell.text.replace(',', '')), cell_format)
                elif formatting == 'percent':
                    self._worksheet.write_number(self._current_row, col_index, 
                                                 float(cell.text.replace(',', '').replace('%', '')),
                                                 self._percent_format)
                elif formatting == 'int':
                    self._worksheet.write_number(self._current_row, col_index, 
                                                 int(cell.text), cell_format)
                elif formatting == 'datetime':
                    dt = datetime.datetime.strptime(cell.text, DATE_PATTERN_VALUES)
                    self._worksheet.write_datetime(self._current_row, 
                                                   col_index, dt, cell_format)
                else:
                    self._worksheet.write(self._current_row, col_index, 
                                          cell.text, cell_format)
                cell_format = None
            self._current_row += 1
    
    def create(self, xml_string, filename):
        self._current_row = 0
        report_path = os.path.join(self._output_dir, 
                                   filename + self.file_extension)
        workbook = xlsxwriter.Workbook(report_path, self.wb_settings)
        self._percent_format = workbook.add_format({'num_format': '0.00"%"'})
        self._worksheet = workbook.add_worksheet('Counterparty')
        format_default = workbook.add_format(self.format_default)
        format_caption = workbook.add_format(self.format_caption)
        format_header = workbook.add_format(self.format_header)
        format_title = workbook.add_format(self.format_title)
        format_summary = workbook.add_format(self.format_summary)
        self._root = ET.fromstring(xml_string)
        self._worksheet.hide_gridlines(2)
        self._worksheet.set_column(0, self._col_count(), 13, format_default)
        captions = self._root.findall('Content/Caption')
        self._add_merged_row('', 1)
        self._add_merged_row(captions[0].text, 1, 1, row_format=format_caption)
        self._add_merged_row('', 1)
        tables = self._root.findall('Content/Table[@dataset="main"]')
        columns = tables[0].findall('Columns/Column')
        for col_index, column in enumerate(columns):
            self._worksheet.write(self._current_row, col_index, column.text, format_header)
        self._current_row += 1
        self._add_merged_row('', 1)
        lb_flag = self._root.findall('Content/Caption[@texttype="lb_flag"]')[0]
        party_code = self._root.findall('Content/Caption[@texttype="party_code"]')[0]
        self._add_merged_row(lb_flag.text, 1, row_format=format_title)
        self._add_merged_row('', 1)
        self._add_merged_row(party_code.text, 1, row_format=format_title)
        summary_row_format = {
            0: format_title,
            3: format_summary,
            4: format_summary,
        }
        for table in tables:
            self._add_data(table, summary_row_format)
            self._add_merged_row('', 1)
        workbook.close()
        return report_path


class XLSXGeneratorInclSubSummary(XLSXReportGenerator):
    
    format_default = {
        'font_name': 'Arial',
        'font_size': 8,
        'border': 0,
    }
    format_default_date = {
        'font_name': 'Arial',
        'font_size': 8,
        'border': 0,
        'num_format': 'mm/dd/yyyy',
    }
    format_caption = {
        'font_name': 'Arial',
        'font_size': 10,
        'bold': True,
    }
    format_header = {
        'font_name': 'Arial',
        'font_size': 8,
        'bold': True,
    }
    format_title = {
        'font_name': 'Arial',
        'font_size': 8,
        'bold': True,
        'align': 'right',
    }
    format_title_underline = {
        'font_name': 'Arial',
        'font_size': 8,
        'bold': True,
        'underline': True,
        'align': 'right',
    }
    format_subsummary_numeric = {
        'font_name': 'Arial',
        'font_size': 8,
        'bold': True,
        'top': 1,
    }
    format_summary_numeric = {
        'font_name': 'Arial',
        'font_size': 8,
        'bold': True,
        'top': 1,
        'bottom': 2,
    }
    
    def __init__(self, output_dir):
        super(XLSXGeneratorInclSubSummary, self).__init__(output_dir)
        self._formats = {}
    
    def _write_row(self, row, row_format, start_index=0):
        cells  = row.findall('Cell')
        for col_index, cell in enumerate(cells, start_index):
            if not col_index in row_format:
                continue
            datatype, cell_format = row_format[col_index]
            if not cell.text:
                self._worksheet.write_blank(self._current_row, col_index, None, cell_format)
                continue
            if datatype == 'float':
                self._worksheet.write_number(self._current_row, col_index, 
                                             float(cell.text.replace(',', '')), cell_format)
            elif datatype == 'int':
                self._worksheet.write_number(self._current_row, col_index, 
                                             int(cell.text.replace(',', '')), cell_format)
            elif datatype == 'datetime':
                dt = datetime.datetime.strptime(cell.text, DATE_PATTERN_VALUES)
                self._worksheet.write_datetime(self._current_row, 
                                               col_index, dt, cell_format)
            else:
                self._worksheet.write(self._current_row, col_index, 
                                      cell.text, cell_format)
    
    def _write_table_data(self, table, row_formats=None, start_index=0):
        columns = table.findall('Columns/Column')
        rows = table.findall('Rows/Row')
        default_format = {}
        for col_index, column in enumerate(columns, start_index):
            col_datatype = column.get('datatype')
            cell_format = (self._formats['default_date'] if col_datatype == 'datetime'
                               else self._formats['default'])
            default_format[col_index] = [col_datatype, cell_format]
        for row in rows:
            if row.get('summary') and row_formats and 'summary' in row_formats:
                self._write_row(row, row_formats['summary'], start_index)
            elif row.get('subsummary') and row_formats and 'subsummary' in row_formats:
                self._write_row(row, row_formats['subsummary'], start_index)
            else:
                self._write_row(row, default_format, start_index)
            self._current_row += 1
    
    def _setup_sheet(self, sheet):
        sheet.hide_gridlines(2)
        sheet.set_column(0, self._col_count(), 10, self._formats['default'])
        self._current_row = 0
        self._worksheet = sheet
    
    def _write_table_columns(self, table, format, start_index=0):
        columns = table.findall('Columns/Column')
        for col_index, column in enumerate(columns, start_index):
            self._worksheet.write(self._current_row, col_index, column.text, format)
        self._current_row += 1
    
    def _write_table_summary(self, table, row_formats=None, start_index=0):
        self._write_table_columns(table, self._formats['title'], start_index)
        self._write_table_data(table, row_formats, start_index)
        self._add_merged_row('')
    
    def _write_values(self, values, start_index=0):
        for value in values:    
            if not value.get('key'):
                self._add_merged_row(value.text, col_start=start_index,
                                     row_format=self._formats['header'])
                continue
            self._worksheet.merge_range(self._current_row, start_index, self._current_row, 
                                        start_index + 1, value.get('key'), self._formats['default'])
            self._add_merged_row(value.text, col_start=start_index + 2,
                                 row_format=self._formats['default'])


class SBLFeeXLSXGenerator(XLSXGeneratorInclSubSummary):
    
    def _populate_details_sheet(self, sheet, content):
        row_formats = {
            'subsummary': {
                8: ['int', self._formats['header']],
                9: ['float', self._formats['subsummary_numeric']],
                10: ['float', self._formats['subsummary_numeric']],
                11: ['float', self._formats['subsummary_numeric']],
            },
            'summary': {
                0: ['string', self._formats['header']],
                9: ['float', self._formats['summary_numeric']],
                10: ['float', self._formats['summary_numeric']],
                11: ['float', self._formats['summary_numeric']],
            },
        }
        self._setup_sheet(sheet)
        captions = content.findall('Caption')
        self._add_merged_row('')
        self._add_merged_row(captions[0].text, row_format=self._formats['header'])
        self._add_merged_row('')
        self._add_merged_row(captions[1].text, col_start=1, row_format=self._formats['caption'])
        self._add_merged_row('')
        self._add_merged_row(captions[2].text, row_format=self._formats['header'])
        self._add_merged_row('')
        tables = content.findall('Table[@dataset="main"]')
        for table in tables:
            header = table.attrib['tableheader']
            self._add_merged_row(header, row_format=self._formats['header'])
            self._write_table_columns(table, self._formats['title_underline'])
            self._write_table_data(table, row_formats)
            self._add_merged_row('')
        self._add_merged_row('')
        summary_table = content.find('TableHorizontalAlign[@dataset="summary"]')
        row_formats = {
            'summary': {
                8: ['string', self._formats['header']],
                9: ['float', self._formats['summary_numeric']],
                10: ['float', self._formats['summary_numeric']],
                11: ['float', self._formats['summary_numeric']],
            },
        }
        self._write_table_summary(summary_table, row_formats, 8)
    
    def _populate_summary_sheet(self, sheet, content):
        self._setup_sheet(sheet)
        captions = content.findall('Caption')
        self._add_merged_row('')
        self._add_merged_row(captions[0].text, col_start=1, row_format=self._formats['caption'])
        self._add_merged_row('')
        self._add_merged_row(captions[1].text, row_format=self._formats['header'])
        self._add_merged_row('')
        summary_table = content.find('TableHorizontalAlign[@dataset="summary"]')
        row_formats = {
            'summary': {
                1: ['string', self._formats['header']],
                2: ['float', self._formats['summary_numeric']],
                3: ['float', self._formats['summary_numeric']],
                4: ['float', self._formats['summary_numeric']],
            },
        }
        self._write_table_summary(summary_table, row_formats, 1)
    
    def _populate_invoice_sheet(self, sheet, content):
        self._setup_sheet(sheet)
        captions = content.findall('Caption')
        self._add_merged_row('')
        self._add_merged_row(captions[0].text, col_start=9, row_format=self._formats['header'])
        self._add_merged_row('')
        self._add_merged_row(captions[1].text, col_start=1, row_format=self._formats['caption'])
        self._add_merged_row('')
        self._add_merged_row(captions[2].text, row_format=self._formats['header'])
        self._add_merged_row('')
        summary_table = content.find('TableHorizontalAlign[@dataset="summary"]')
        row_formats = {
            'summary': {
                1: ['string', self._formats['header']],
                2: ['float', self._formats['summary_numeric']],
                3: ['float', self._formats['summary_numeric']],
                4: ['float', self._formats['summary_numeric']],
            },
        }
        self._write_table_summary(summary_table, row_formats, 1)
        self._add_merged_row('', 2)
        values = content.findall('Values/Value')
        self._write_values(values, 1)
    
    def create(self, xml_string, filename):
        report_path = os.path.join(self._output_dir, 
                                   filename + self.file_extension)
        workbook = xlsxwriter.Workbook(report_path, self.wb_settings)
        self._formats = {
            'default': workbook.add_format(self.format_default),
            'default_date': workbook.add_format(self.format_default_date),
            'caption': workbook.add_format(self.format_caption),
            'header': workbook.add_format(self.format_header),
            'title': workbook.add_format(self.format_title),
            'title_underline': workbook.add_format(self.format_title_underline),
            'subsummary_numeric': workbook.add_format(self.format_subsummary_numeric),
            'summary_numeric': workbook.add_format(self.format_summary_numeric),
        }
        self._root = ET.fromstring(xml_string)
        details_content = self._root.find('Content[@contenttype="Fee Details"]')
        details_sheet = workbook.add_worksheet('Fee Details')
        self._populate_details_sheet(details_sheet, details_content)
        
        summary_content = self._root.find('Content[@contenttype="Fee Summary"]')
        summary_sheet = workbook.add_worksheet('Fee Summary')
        self._populate_summary_sheet(summary_sheet, summary_content)
        
        invoice_content = self._root.find('Content[@contenttype="Tax Invoice"]')
        invoice_sheet = workbook.add_worksheet('Tax Invoice')
        self._populate_invoice_sheet(invoice_sheet, invoice_content)
        
        workbook.close()
        return report_path


class SBLOpenPosXLSXGenerator(XLSXGeneratorInclSubSummary):
    
    def _populate_sheet(self, sheet, content):
        row_formats = {
            'subsummary': {
                2: ['string', self._formats['header']],
                3: ['int', self._formats['subsummary_numeric']],
                6: ['float', self._formats['subsummary_numeric']],
                8: ['float', self._formats['subsummary_numeric']],
            },
            'summary': {
                0: ['string', self._formats['header']],
                6: ['float', self._formats['summary_numeric']],
                8: ['float', self._formats['summary_numeric']],
            },
        }
        self._setup_sheet(sheet)
        captions = content.findall('Caption')
        self._add_merged_row('')
        self._add_merged_row(captions[0].text, col_start=1, row_format=self._formats['caption'])
        self._add_merged_row('')
        self._add_merged_row(captions[1].text, row_format=self._formats['header'])
        self._add_merged_row('')
        tables = content.findall('Table[@dataset="main"]')
        for table in tables:
            header = table.attrib['tableheader']
            self._add_merged_row(header, row_format=self._formats['header'])
            self._write_table_columns(table, self._formats['title_underline'])
            self._write_table_data(table, row_formats)
            self._add_merged_row('')
        self._add_merged_row('')
    
    def create(self, xml_string, filename):
        report_path = os.path.join(self._output_dir, 
                                   filename + self.file_extension)
        workbook = xlsxwriter.Workbook(report_path, self.wb_settings)
        self._formats = {
            'default': workbook.add_format(self.format_default),
            'default_date': workbook.add_format(self.format_default_date),
            'caption': workbook.add_format(self.format_caption),
            'header': workbook.add_format(self.format_header),
            'title': workbook.add_format(self.format_title),
            'title_underline': workbook.add_format(self.format_title_underline),
            'subsummary_numeric': workbook.add_format(self.format_subsummary_numeric),
            'summary_numeric': workbook.add_format(self.format_summary_numeric),
        }
        self._root = ET.fromstring(xml_string)
        content = self._root.find('Content')
        worksheet = workbook.add_worksheet()
        self._populate_sheet(worksheet, content)
        workbook.close()
        return report_path


class ReportBase(XMLReport.StatementReportBase):
    
    doc_caption = ''
    bank_tel = ''
    
    def __init__(self, statement_type, party, contact, values,
                 generate_date, val_date):
        self._statement_type = statement_type
        self._party = party
        self._contact = contact
        self._values = values
        self._generate_date = generate_date
        self._val_date = val_date
    
    def client_address(self):
        return contact_from_pty(self._party, self._contact)
    
    def bank_address(self):
        return {
            'address': get_param_value(FPARAMS, ABSA_ADDRESS_PARAM).split(','),
            'tel': self.bank_tel,
            'web': get_param_value(FPARAMS, ABSA_WEB_PARAM),
            'date': format_date(self._generate_date, DATE_PATTERN_DOCS),
        }

    
class ValuationsReport(ReportBase):

    doc_caption = '%s Valuation Statement as at %s'
    table_header = 'Client Account Number: %s'
    table_footer = ("Please note that this valuation is done from the"
                    " bank's point of view so a negative value is in the"
                    " client's favour.")
    bank_tel = get_param_value(FPARAMS, VALUATIONS_TEL_PARAM)
    
    @staticmethod
    def get_table_rows(values, labels):
        for key in sorted(values.keys()):
            if key == 'SUMMARY':
                continue
            yield [values[key][label] for label in labels]
        if 'SUMMARY' in values:
            summary_row = [values['SUMMARY'][label] for label in labels]
            valid_indices =  [i for (i, element) in enumerate(summary_row) 
                              if element]
            if valid_indices and valid_indices[0] > 0:
                summary_row[valid_indices[0] - 1] = 'Total'
            yield XMLReport.SummaryRow(summary_row)
    
    def statement_detail(self):
        party_sd_id = self._party.AdditionalInfo().BarCap_Eagle_SDSID()
        header = self.table_header % party_sd_id
        caption_date = format_date(self._val_date, DATE_PATTERN_DOCS)
        for group_name, group_values in self._values.iteritems():
            statement_type = (' '.join([group_name, self._statement_type]) 
                                  if group_name else self._statement_type)
            yield XMLReport.mkcaption(self.doc_caption 
                                      % (statement_type, caption_date))
            labels = group_values['columns'].keys()
            table_rows = self.get_table_rows(group_values['values'], labels)
            yield mktable(group_values['columns'], table_rows, header=header, 
                          alignment='right', dataset='main', 
                          tablefooter=self.table_footer)
            add_vals = group_values['add_values']
            for table_name in add_vals:
                yield XMLReport.mkvalues(table_name, 
                                         *add_vals[table_name].items(), 
                                         width='20mm')
            yield XMLReport.mkpagebreak()
        yield XMLReport.mkdisclaimer(*DISCLAIMER_VALUATIONS.splitlines())


class SBLReport(ReportBase):
    
    bank_tel = get_param_value(FPARAMS, SBL_COLL_TEL_PARAM)
    bank_email = get_param_value(FPARAMS, SBL_COLL_EMAIL_PARAM)
    
    def bank_address(self):
        details = super(SBLReport, self).bank_address()
        details['email'] = self.bank_email
        return details
    
    @staticmethod
    def get_table_rows(values, labels, summary_label='Total', summary_position=0):
        for key in sorted(values.keys()):
            if key in ('SUMMARY', 'SUMMARY_RAW'):
                continue
            row = [values[key][label] for label in labels]
            if 'SUBSUMMARY' in key:
                yield XMLReport.SubSummaryRow(row)
            else:
                yield row
        if 'SUMMARY' in values:
            summary_row = [values['SUMMARY'][label] for label in labels]
            summary_row[summary_position] = summary_label
            yield XMLReport.SummaryRow(summary_row)


class SBLFeeReport(SBLReport):

    doc_caption = 'Securities Lending Fees For %s'
    banking_details_title = 'Our Banking Details are as follow:'
    bank_tel = get_param_value(FPARAMS, SBL_OPS_TEL_PARAM)
    bank_email = get_param_value(FPARAMS, SBL_OPS_EMAIL_PARAM)
    bank_vat_nbr = get_param_value(FPARAMS, ABSA_VAT_NBR_PARAM)
    
    @staticmethod
    def _banking_details():
        return (
            ('Account Name', get_param_value(FPARAMS, SBL_ACC_NAME_PARAM)),
            ('Bank Name', get_param_value(FPARAMS, SBL_BANK_PARAM)),
            ('Account Number', get_param_value(FPARAMS, SBL_ACC_NUM_PARAM)),
            ('Branch Code', get_param_value(FPARAMS, SBL_BRANCH_PARAM)),
            ('SWIFT', get_param_value(FPARAMS, SBL_SWIFT_PARAM)),
        )
    
    @staticmethod
    def _summary_label(lb_flag):
        return 'Due from You' if lb_flag == 'Borrower' else 'Due to You'
    
    @staticmethod
    def _get_lb_flag(cp_name):
        party = acm.FParty[cp_name]
        return party.AdditionalInfo().SL_CptyType()
    
    @staticmethod
    def _get_g1_code(cp_name):
        party = acm.FParty[cp_name]
        return party.AdditionalInfo().SL_G1PartyCode()
    
    def bank_address(self):
        details = super(SBLFeeReport, self).bank_address()
        details['vat_nbr'] = self.bank_vat_nbr
        return details
    
    def client_address(self):
        details = super(SBLFeeReport, self).client_address()
        client_vat_nbr = self._party.AdditionalInfo().Vat_Number()
        if client_vat_nbr: 
            details['vat_nbr'] = client_vat_nbr
        return details
    
    def statement_detail_main(self, cp_name, values):
        lb_flag = self._get_lb_flag(cp_name)
        g1_code = self._get_g1_code(cp_name)
        caption_date = format_date(self._val_date, DATE_PATTERN_MONTH)
        yield XMLReport.mkcaption(g1_code)
        yield XMLReport.mkcaption(self.doc_caption % caption_date)
        yield XMLReport.mkcaption(lb_flag)
        for group_name, group_values in values.iteritems():
            if group_name in ('STATEMENT_TOTALS', 'INVOICE_NBR'):
                continue
            labels = group_values['columns'].keys()
            security_name = group_name.split(' - ')[0]
            table_rows = self.get_table_rows(group_values['values'], labels,
                                             summary_label='%s Total' % security_name)
            yield mktable(group_values['columns'], table_rows, header=group_name, 
                          alignment='right', dataset='main')
        total_values = values['STATEMENT_TOTALS']
        columns = total_values['columns']
        labels = columns.keys()
        table_rows = self.get_table_rows(total_values['values'], labels,
                                         summary_label=self._summary_label(lb_flag))
        columns[labels[0]]['alignment'] = 'left'
        yield mktable(columns, table_rows,
                      template_name='TableHorizontalAlign', alignment='right', 
                      dataset='summary', firstcolwidth='110mm', lastcolwidth='0mm')
        yield XMLReport.mkpagebreak()
    
    def statement_detail_summary(self):
        caption_date = format_date(self._val_date, DATE_PATTERN_MONTH)
        yield XMLReport.mkcaption(self.doc_caption % caption_date)
        yield XMLReport.mkcaption('Summary')
        for cp_name, values in self._values.iteritems():
            lb_flag = self._get_lb_flag(cp_name)
            total_values = values['STATEMENT_TOTALS']
            columns = total_values['columns']
            labels = columns.keys()
            table_rows = self.get_table_rows(total_values['values'], labels,
                                             summary_label=self._summary_label(lb_flag))
            columns[labels[0]]['alignment'] = 'left'
            yield mktable(columns, table_rows,
                          template_name='TableHorizontalAlign', alignment='right', 
                          dataset='summary', firstcolwidth='55mm', lastcolwidth='55mm',
                          margintop='20mm')
        yield XMLReport.mkpagebreak()
    
    def statement_detail_invoice(self, cp_name, values):
        lb_flag = self._get_lb_flag(cp_name)
        invoice_nbr_text = 'Invoice Number: %s%s' % (lb_flag[0], values['INVOICE_NBR'])
        yield mktext(invoice_nbr_text, fontsize='8pt', alignment='right')
        caption_date = format_date(self._val_date, DATE_PATTERN_MONTH)
        yield XMLReport.mkcaption(self.doc_caption % caption_date)
        yield XMLReport.mkcaption('Tax Invoice')
        total_values = values['STATEMENT_TOTALS']
        columns = total_values['columns']
        labels = columns.keys()
        table_rows = self.get_table_rows(total_values['values'], labels,
                                         summary_label=self._summary_label(lb_flag))
        columns[labels[0]]['alignment'] = 'left'
        yield mktable(columns, table_rows,
                      template_name='TableHorizontalAlign', alignment='right', 
                      dataset='summary', firstcolwidth='55mm', lastcolwidth='55mm',
                      margintop='20mm')
        if lb_flag == 'Borrower':
            yield XMLReport.mkvalues(self.banking_details_title, 
                                     *self._banking_details(), width='47mm',
                                     firstcolwidth='48mm', lastcolwidth='48mm',
                                     margintop='20mm')
        yield XMLReport.mkpagebreak()
    
    def create_report(self):
        report = ET.Element('XMLReport')
        
        def create_and_append(parent, element_name, subelements, **kwargs):
            el = ET.SubElement(parent, element_name)
            for key, value in kwargs.iteritems():
                el.attrib[key] = value
            for subelement in subelements:
                el.append(subelement)
        
        report.append(XMLReport.mkcontact(self.bank_address(), "Bank"))
        report.append(XMLReport.mkcontact(self.client_address(), "Client"))
        
        for cp_name, values in self._values.iteritems():
            create_and_append(report, 'Content', self.statement_detail_main(cp_name, values),
                              contenttype='Fee Details')
        create_and_append(report, 'Content', self.statement_detail_summary(),
                          contenttype='Fee Summary')
        for cp_name, values in self._values.iteritems():
            create_and_append(report, 'Content', self.statement_detail_invoice(cp_name, values),
                              contenttype='Tax Invoice')
        
        return ET.tostring(report)


class SBLFinderFeeReport(SBLFeeReport):
    
    @staticmethod
    def _get_lb_flag(_cp_name):
        return 'Finder'


class SBLMovementReport(SBLReport):
    
    doc_caption = 'Movements - Date From: %s Date To: %s'
    
    @staticmethod
    def get_table_rows(values, labels):
        for key in sorted(values.keys()):
            yield [values[key][label] for label in labels]
    
    def statement_detail(self):
        params = self._values['PARAMS']
        start_date = format_date(params['start_date'], DATE_PATTERN_DOCS)
        end_date = format_date(params['end_date'], DATE_PATTERN_DOCS)
        yield XMLReport.mkcaption(self.doc_caption % (start_date, end_date))
        for group_name, group_values in self._values.iteritems():
            if group_name in ('PARAMS',):
                continue
            labels = group_values['columns'].keys()
            table_rows = self.get_table_rows(group_values['values'], labels)
            yield mktable(group_values['columns'], table_rows, 
                          header=group_name, alignment='right', dataset='main')
        yield XMLReport.mkpagebreak()


class SBLOpenPosCollReport(SBLReport):
    
    doc_caption = 'Open Position Report as at %s'
    
    def statement_detail(self):
        lb_flag = self._party.AdditionalInfo().SL_CptyType()
        caption_date = format_date(self._val_date, DATE_PATTERN_DOCS)
        yield XMLReport.mkcaption(self.doc_caption % caption_date)
        yield XMLReport.mkcaption(lb_flag)
        for group_name, group_values in self._values.iteritems():
            labels = group_values['columns'].keys()
            table_rows = self.get_table_rows(group_values['values'], labels)
            yield mktable(group_values['columns'], table_rows, 
                          alignment='right', dataset='main', header=group_name)
            yield XMLReport.mkpagebreak()


class SBLOpenPosOpsReport(SBLOpenPosCollReport):
    
    bank_tel = get_param_value(FPARAMS, SBL_OPS_TEL_PARAM)
    bank_email = get_param_value(FPARAMS, SBL_OPS_EMAIL_PARAM)


class SBLSummaryOpenPosReport(SBLReport):
    
    doc_caption = 'Summary Position as at %s'
    
    @staticmethod
    def get_table_rows(values, labels, summary_label='Total', summary_position=0):
        for key in sorted(values.keys()):
            if key == 'SUMMARY':
                continue
            if 'SUBSUMMARY' in key:
                yield [values[key][label] for label in labels]
        if 'SUMMARY' in values:
            summary_row = [values['SUMMARY'][label] for label in labels]
            summary_row[summary_position] = summary_label
            yield XMLReport.SummaryRow(summary_row)
    
    def statement_detail(self):
        caption_date = format_date(self._val_date, DATE_PATTERN_DOCS)
        yield XMLReport.mkcaption(self.doc_caption % caption_date)
        lb_flag = self._party.AdditionalInfo().SL_CptyType()
        yield mktext(lb_flag, fontsize='10pt', alignment='left', texttype='lb_flag')
        party_code = self._party.AdditionalInfo().SL_G1PartyCode()
        yield mktext(party_code, fontsize='10pt', alignment='left', texttype='party_code')
        for group_name, group_values in self._values.iteritems():
            labels = group_values['columns'].keys()
            table_rows = self.get_table_rows(group_values['values'], labels, group_name)
            yield mktable(group_values['columns'], table_rows, 
                          alignment='right', dataset='main')
        yield XMLReport.mkpagebreak()


class SBLMarginCallReport(SBLReport):
    
    doc_caption = 'Margin Call Report as at %s'
    
    def statement_detail(self):
        caption_date = format_date(self._val_date, DATE_PATTERN_DOCS)
        yield XMLReport.mkcaption(self.doc_caption % caption_date)
        collateral = self._values['Collateral']
        collateral_labels = collateral['columns'].keys()
        collateral_row = collateral['values'].values()[0]
        collateral_values = [collateral_row[label] for label in collateral_labels]
        yield XMLReport.mkvalues('Collateral Market Value', 
                                 *list(zip(collateral_labels, collateral_values)), 
                                 width='30mm', firstcolwidth='0mm', margintop='10mm')
        loans = self._values['Loans']
        loans_labels = loans['columns'].keys()
        loans_summary =  loans['values']['SUMMARY']
        loans_values = [loans_summary[label] for label in loans_labels]
        yield XMLReport.mkvalues('Loan Market Value', 
                                 *list(zip(loans_labels, loans_values)), 
                                 width='30mm', firstcolwidth='0mm', margintop='10mm')
        margin_call = self._values['Margin Call']
        margin_call_labels = margin_call['columns'].keys()
        table_rows = self.get_table_rows(margin_call['values'], margin_call_labels)
        margin_value = float(margin_call['values'].values()[0]['MarginValue'])
        lb_flag = self._party.AdditionalInfo().SL_CptyType()
        footer = ''
        if ((lb_flag == 'Borrower' and margin_value > 0) 
                or (lb_flag == 'Lender' and margin_value < 0)):
            footer = 'Margin due to you'
        elif ((lb_flag == 'Borrower' and margin_value < 0) 
                or (lb_flag == 'Lender' and margin_value > 0)):
            footer = 'Margin due to us'
        yield mktable(margin_call['columns'], table_rows, header='Margin Call',
                      template_name='TableHorizontalAlign', alignment='center', 
                      dataset='main', firstcolwidth='0mm', lastcolwidth='70mm',
                      margintop='10mm', tablefooter=footer)
        yield XMLReport.mkpagebreak()
        yield XMLReport.mkdisclaimer(DISCLAIMER_SBL_MARGIN_CALL)


class SBLDividendNotificationReport (SBLReport):

    doc_caption = 'Dividend Notification for Record Date %s'
    banking_details_title = 'Kindly make payment to the following account:'

    @staticmethod
    def _banking_details():
        return (
                    ('Account Name', get_param_value(FPARAMS, SBL_DIV_ACC_NAME_PARAM)),
                    ('Bank Name', get_param_value(FPARAMS, SBL_BANK_PARAM)),
                    ('Account Number', get_param_value(FPARAMS, SBL_DIV_ACC_NUM_PARAM)),
                    ('Branch Code', get_param_value(FPARAMS, SBL_DIV_BRANCH_PARAM)),
                    ('SWIFT', get_param_value(FPARAMS, SBL_SWIFT_PARAM)),
                )

    def statement_detail(self):
        caption_date = format_date(self._val_date, DATE_PATTERN_DOCS)
        yield XMLReport.mkcaption(self.doc_caption % caption_date)
        for group_name, group_values in self._values.iteritems():
            labels = group_values['columns'].keys()
            table_rows = self.get_table_rows(group_values['values'], labels)
            yield mktable(group_values['columns'], table_rows, 
                          alignment='right', dataset='main', header=group_name)

            if group_name == 'Receivable':
                yield XMLReport.mkvalues(self.banking_details_title, 
                                         *self._banking_details(), width='48mm',
                                         firstcolwidth='0mm', lastcolwidth='48mm',
                                         margintop='200px', marginbottom='0px')
            yield XMLReport.mkpagebreak()
        yield XMLReport.mkdisclaimer(DISCLAIMER_SBL_DIVIDEND_NOTIFICATION)

