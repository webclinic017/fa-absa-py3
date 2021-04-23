'''
Created on 15 Jan 2014

    Purpose                 : Script to check all books in graveyard are flat
                                in terms of risk, PV and cash
    Department and Desk     : PCG
    Requester               : Boshoff Alex
    Developer               : Conicov Andrei
    CR Number               : ABITFA-2247
'''

from __future__ import print_function
from at_ael_variables import AelVariableHandler
import FBDPCommon
import acm
import csv
import os
import string


class ColumnDefinition(object):

    def __init__(self, col_id, title, group, is_vector=False, key=None):
        """
        Arguments:
        col_id - FA column col_id
        title - the column title
        group - the column group
        is_vector - the column is a part of a vector (the column title is
        a parameter in the calculation)
        """
        self.title = title
        self.group = group
        self.col_id = col_id
        self.is_vector = is_vector
        if key == None:
            self.key = col_id
        else:
            self.key = key


# PORTFOLIOS = ['GRAVEYARD']  # , 'PM Loans Waste'
PORTFOLIOS = ['PM Loans Waste']
ignore_portfolios = []
COLUMNS_TO_CHECK = [ColumnDefinition('Portfolio Delta Yield', 'YDelta',
                                     'Position Risk'),
                    ColumnDefinition('Portfolio Gamma Total', 'EQDeltaCash',
                                       'Position Risk'),
                    ColumnDefinition('Portfolio Accumulated Cash', 'Cash',
                                       'Position Risk'),
                    ColumnDefinition('Portfolio Value End', 'Val End',
                                       'Position Risk'),
                    ColumnDefinition('Portfolio Position', 'Pos',
                                       'Position Risk'),
                    ColumnDefinition('Portfolio Total Profit and Loss', 'TPL',
                                       'Profit/Loss')]
COLUMNS = []
CURRENCIES = [ColumnDefinition('Portfolio FX Delta Cash', 'USD',
                               'Position Risk', True,
                               'Portfolio FX Delta Cash-USD'),
              ColumnDefinition('Portfolio FX Delta Cash', 'GBP',
                                 'Position Risk', True,
                                 'Portfolio FX Delta Cash-GBP'),
              ColumnDefinition('Portfolio FX Delta Cash', 'EUR',
                                 'Position Risk', True,
                                 'Portfolio FX Delta Cash-EUR'),
              ColumnDefinition('Portfolio FX Delta Cash', 'JPY',
                                 'Position Risk', True,
                                 'Portfolio FX Delta Cash-JPY')]

GROUPER_NAMES = ['Subportfolio', 'Underlying']

SCRIPT_NAME = 'PCG_NoneZeroRisk'
EMAIL_LIST = ['andrei.conicov@barclays.com', 'andrei.conicov@barcap.com']


class ReportColumnDefinition(ColumnDefinition):

    def __init__(self, col_def, is_zero_check=True, is_zero_check_func=None):
        super(ReportColumnDefinition, self).__init__(col_def.col_id,
                                                     col_def.title,
                                                     col_def.group,
                                                     col_def.is_vector,
                                                     col_def.key)
        self.col_def = col_def
        self.is_zero_check = is_zero_check
        self.is_zero_check_func = is_zero_check_func


class NonZeroRiskReport:
    '''
    Computes the values of the specified columns and outputs the items
    that don't have zero values for the specified columns.
    '''

    def __init__(self, currencies, columns, grouper_names):
        '''
        Initialises a new instance.

        Arguments:
        currencies - a list of column definitions of type ReportColumnDefinition.
        It is used as a parameter for the column "Portfolio FX Delta Cash".
        columns - a list of column definitions of type ReportColumnDefinition.
        grouper_names - a list of strings that specifies the grouping
        '''
        self._currencies = currencies
        self._columns = filter(lambda col: not col.is_zero_check, columns)
        self._columns_to_check = filter(lambda col: col.is_zero_check, columns)
        self._grouper_names = grouper_names
        self._curr_vec_col = 'Portfolio FX Delta Cash'
        self._col_sub_und_desc = ColumnDefinition('Subportfolio/Underlying',
                                                  'Subportfolio/Underlying',
                                                  '')
        self._col_und_desc = ColumnDefinition('Underlying', 'Underlying', '')
        self._col_ins_desc = ColumnDefinition('Instrument', 'Instrument', '')
        self._calc_space = acm.Calculations().CreateCalculationSpace('Standard',
                                                                     'FPortfolioSheet')

        vector = acm.FArray()
        for currency in [col.title for col in currencies]:
            NonZeroRiskReport._create_named_param(vector
                                                  , acm.FCurrency[currency])

        self._cash_per_currency = acm.Sheet.Column().ConfigurationFromVector(vector)

    @staticmethod
    def _create_named_param(vector, currency):
        """Simple function that add FNamedParameters
        to passed vector.

        Arguments:
        vector - FArray
        currency - FCurrency
        """
        param = acm.FNamedParameters()
        param.AddParameter('currency', currency)
        vector.Add(param)

    def _calc(self, workbook_row):
        '''
        Calculates the values of the columns specified in the initialisation.

        Arguments:

        '''
        obj = workbook_row
        if obj == None:
            return None

        # will be set to true if the instrument values have to be output
        output = False

        data = {}

        cpc_vector = self._calc_space.CreateCalculation(obj, self._curr_vec_col,
                                                        self._cash_per_currency).Value()
        cpc_vector = [value.Number() for value in cpc_vector]
        abs_vector = [abs(number) for number in cpc_vector]

        if sum(abs_vector) > 0:
            output = output or True
        for i in range(0, len(self._currencies)):
            data[self._currencies[i].key] = str(cpc_vector[i])

        for col in self._columns_to_check:
            val = self._calc_space.CalculateValue(obj, col.col_id, None, False)
            if hasattr(val, 'Number'):
                val = val.Number()

            if (type(val) != float and type(val) != int
                and col.is_zero_check_func):
                output = output or col.is_zero_check_func(val)
            else:
                output = output or val != 0

            data[col.key] = str(val)

        if output:
            for col in self._columns:
                val = self._calc_space.CalculateValue(obj, col.col_id,
                                                      None, False)
                if hasattr(val, 'Number'):
                    val = val.Number()
                data[col.key] = str(val)

        if output:
            return data
        return None

    @staticmethod
    def _get_chained_grouper(grouper_names):
        groupers = map(acm.Risk().GetGrouperFromName, grouper_names)
        chained_grouper = acm.FChainedGrouper(groupers)
        return chained_grouper

    @staticmethod
    def _write_data(data_dict, writer_f):
        writer_f(data_dict)

    def _process_tree(self, node, writer_f, prev_port, prev_und):
        outputed_rows = 0
        prev_port_curr = ""
        prev_und_curr = ""
        while node:
            if  node.Tree().Item().StringKey() not in ignore_portfolios:
                result = self._calc(node.Tree())
                if result != None:
                    if node.Tree().Item().IsKindOf('FPortfolioInstrumentAndTrades'):
                        # portfolio
                        prev_port_curr = node.Tree().Item().StringKey()
                        if prev_port != "":
                            prev_port_curr = prev_port + "/" + prev_port_curr
                        result[self._col_sub_und_desc.key] = prev_port_curr
                        result[self._col_und_desc.key] = prev_und
                        result[self._col_ins_desc.key] = ""
                    elif node.Tree().Item().IsKindOf('FMultiInstrumentAndTrades'):
                        # underlying
                        prev_port_curr = prev_port
                        prev_und_curr = node.Tree().Item().StringKey()
                        if prev_und != "":
                            prev_und_curr = prev_und + "/" + prev_und_curr
                        result[self._col_sub_und_desc.key] = prev_port_curr
                        result[self._col_und_desc.key] = prev_und_curr
                        result[self._col_ins_desc.key] = ""
                    elif node.Tree().Item().IsKindOf('FInstrumentAndTrades'):
                        # instrument
                        result[self._col_sub_und_desc.key] = prev_port
                        result[self._col_und_desc.key] = prev_und
                        result[self._col_ins_desc.key] = node.Tree().Item().StringKey()

                    outputed_rows += 1
                    NonZeroRiskReport._write_data(result, writer_f)
                    outputed_rows += self._process_tree(node.Tree().Iterator().FirstChild(),
                                                        writer_f,
                                                        prev_port_curr,
                                                        prev_und_curr)
            node = node.NextSibling()
        return outputed_rows

    def get_col_header(self):
        full_col_def = [self._col_sub_und_desc]
        full_col_def.append(self._col_und_desc)
        full_col_def.append(self._col_ins_desc)
        full_col_def.extend(self._columns_to_check)
        full_col_def.extend(self._currencies)
        full_col_def.extend(self._columns)

        return full_col_def

    def create_output(self, portfolios, writer_f):
        """
        Creates the report containing all the instruments from the
        specified portfolios, which have values different from zero
        , for the specified columns.

        Arguments:
        portfolios - a list of portfolios names
        writer_f - a function that takes a list of strings
        """
        grouper = NonZeroRiskReport._get_chained_grouper(self._grouper_names)

        for p_name in portfolios:
            portfolio = acm.FPhysicalPortfolio[p_name]
            self._calc_space.Clear()
            print("Inserting the portfolio {0}".format(portfolio.Name()))
            top_node = self._calc_space.InsertItem(portfolio)
            print("Applying grouper")
            top_node.ApplyGrouper(grouper)
            self._calc_space.Refresh()
            node = top_node.Iterator()
            print("Processing tree")
            self.outputed_rows = self._process_tree(node, writer_f, "", "")


ael_variables = AelVariableHandler()

ael_variables.add(
    'portfolios',
    label='Portfolios',
    default=",".join(PORTFOLIOS),
    alt="The list of portfolios. Use ',' to delimit.",
    mandatory=1
    )
ael_variables.add(
    'path',
    label='Output Folder',
    default=r'c:\tmp\ABITFA-2247',
    alt='The directory where to which the file will be dropped.',
    mandatory=1
    )
ael_variables.add(
    'file_name',
    label='Output File Name',
    default='PCG_NonZeroRisk.xls',
    alt='The file name',
    mandatory=1
    )
ael_variables.add(
    'email_list',
    label='Mail warning to',
    default=",".join(EMAIL_LIST),
    alt=("The list of emails that will be notified if the report is not empty."
    "Use ',' to delimit emails"),
    mandatory=1
    )


def sendMail(TO, SUBJECT, MSG):
    """
    Copied from FBDPCommon, throws exceptions.
    """
    import smtplib

    HOST = acm.GetCalculatedValue(0, acm.GetDefaultContext().Name(),
            'mailServerAddress').Value()
    FROM = "PRIME client"
    BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "", MSG), "\r\n")
    if not HOST:
        raise Exception("Could not initialise the smtp Host")

    server = smtplib.SMTP(HOST)
    server.sendmail(FROM, TO.split(','), BODY)
    server.quit()


def send_warning(file_name, email_list):
    """
    Returns a return code and the list of errors.
    The return codes:
    0. No errors, the mail was sent to all recipients
    1. Some errors, could not send the mail to some of the recipients
    2. Could not send to any recipient
    """
    subject_field = ("WARNING: Not all books in Graveyard are flat in terms of risk")
    body = ("WARNING: Not all books in Graveyard are flat in terms of risk. "
            "Please check the file: {0} that contains additional information"
            .format(file_name))
    print ('Sending warnings for email recipients: {0}'.format(email_list))

    errors = []
    for address in email_list:
        try:
            sendMail(address, subject_field, body)
        except Exception as ex:
            errors.append(ex)
    if len(errors) == len(email_list):
        return_code = 2
    elif len(errors) > 0 and len(errors) <= len(email_list):
        return_code = 1
    else:
        return_code = 0

    return (return_code, errors)


def ael_main(dict_arg):
    """Main entry point for FA"""
    acm.Log("Starting {0}".format(__name__))

    if str(acm.Class()) == "FTmServer":
        warning_function = acm.GetFunction("msgBox", 3)
    else:
        warning_function = lambda t, m, *_r: print("{0}: {1}".format(t, m))

    path = dict_arg['path']
    file_name = dict_arg['file_name']
    portfolios = dict_arg['portfolios'].split(",")

    if not os.access(path, os.W_OK):
        warning_function("Warning",
            "Output path is not writable! Client valuation not generated!", 0)
        return

    file_path = os.path.join(path, file_name)

    cast = lambda col_defs: map(lambda col_def: ReportColumnDefinition(col_def),
                                col_defs)
    col_to_check = cast(COLUMNS_TO_CHECK)

    for col in col_to_check:
        if col.col_id == "Portfolio Position":
            col.is_zero_check_func = lambda val: val.IsKindOf("FVariantArray") and val.Size() > 0
    gReport = NonZeroRiskReport(cast(CURRENCIES), col_to_check, GROUPER_NAMES)

    col_header_keys = [col_def.key for col_def in gReport.get_col_header()]
    col_header_titles = dict((col_def.key, col_def.title) for col_def in gReport.get_col_header())

    with open(file_path, 'wb') as file_w:
        dict_writer = csv.DictWriter(file_w, col_header_keys
                                     , dialect='excel-tab')
        dict_writer.writerow(col_header_titles)
        writer_f = lambda row_dict: dict_writer.writerow(row_dict)
        gReport.create_output(portfolios, writer_f)

    acm.Log("Output rows:{0}".format(gReport.outputed_rows))

    return_code = 0
    errors = []
    if gReport.outputed_rows > 0:
        email_list = dict_arg['email_list'].split(",")
        (return_code, errors) = send_warning(file_name, email_list)

    acm.Log("Wrote secondary output to {0}".format(file_path))

    if return_code == 0:
        acm.Log("Completed successfully")
    else:
        for ex in errors:
            acm.Log("Error: {0}".format(ex))
        acm.Log("Completed with some errors")
