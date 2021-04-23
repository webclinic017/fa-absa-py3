"""
Implementation of the Linker reset ladder report.
This script is a refactored version of the script created by TCU.

Project                : Linker reset ladder report
Department and Desk    : Middle Office
Requester              : Boshoff, Alex
Developer              : Nico Louw
CR Number              : CHNG0002298291

HISTORY
==============================================================================
Date        CR number    Developer       Description
------------------------------------------------------------------------------

------------------------------------------------------------------------------

"""
import ael
import acm
import csv

# ========================== Script functions ================================


def write_file(name, data, access='wb'):
    """ Method to write report output to csv file

    Arguments:
        name - the name of the file.
        data - the data to write to file.
    """
    file_obj = open(name, access)
    csv_writer = csv.writer(file_obj, dialect='excel-tab')
    csv_writer.writerows(data)
    file_obj.close()


def reset_fwd_rate(reset):
    """ Method to calculate the forward rate for a reset

    Arguments:
        reset - acm reset object
    """
    context = acm.GetDefaultContext()
    sheet_type = 'FMoneyFlowSheet'
    column_id = 'Cash Analysis Fixing Estimate'
    calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)
    value = calc_space.CalculateValue(reset, column_id).Value()
    try:
        fwd_rate = value.Number()*100.0
    except ArithmeticError:
        print('Error calculating fwd_rate, using 0.0')
        fwd_rate = 0.0
    return fwd_rate


def cf_proj(cash_flow, trade):
    """ Method to calculate the projected cash flow

    Arguments:
        cash_flow - acm cash flow object
        trade - acm trade object
    """
    context = acm.GetDefaultContext()
    sheet_type = 'FMoneyFlowSheet'
    column_id = 'Cash Analysis Projected'
    calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)
    value = calc_space.CalculateValue(cash_flow, column_id).Value()

    try:
        proj_cf = value.Number()*trade.Quantity()
    except ArithmeticError:
        print('Error calculating proj_cf, using 0.0')
        proj_cf = 0.0
    return proj_cf

# ========================== Report Class ====================================


class LinkerResetLadderReport(object):
    """ Report class
    """
    def __init__(self, data):
        self.cpi = data['cpi_Ins']
        self.portfolios = data['portfolios']
        self.outpath = data['Outpath']
        self.excl_status = list(data['excl_status'])
        self.excl_instypes = list(data['excl_instype'])

        self.start_date = self._get_start_date()
        self.mid_date = self.start_date.add_months(1)
        self.end_date = self.start_date.add_months(2)

        self.start_to_mid_count = self.start_date.days_between(
            self.mid_date)*1.0
        self.mid_to_end_count = self.mid_date.days_between(self.end_date)*1.0

        self.name = 'LinkerResetLadder_Report'
        self.file_name = '%s%s.xls' % (self.outpath, self.name)
        self.report_header = self._headers()
        self.output = []

    def _get_start_date(self):
        """ Private method to find the start date of the report based on the
            CPI Instrument (default CPI = SACPI)
        """
        cpi = self.cpi
        start_date = None
        for price in cpi.HistoricalPrices().Filter(
                lambda x: x.Day() >= start_date).SortByProperty('Day', False):
            start_date = ael.date(price.Day())
            break
        if start_date is None:
            print('Error finding start date')

        return start_date.add_months(4)

    def _headers(self):
        """ Private method to add the report headers
        """
        header = []
        header.append(['Report Name:', self.name])
        header.append(['Report Date:', ael.date_today()])
        header.append(['Price Index: ', self.cpi.Name()])
        header.append(['Start Date:', self.start_date])
        header.append(['End Date:', self.end_date])
        return header

    def print_header(self):
        """ Method to print the report header
        """
        print('\nStarting Linker Reset Ladder Report')
        print('REPORT PARAMETERS \n')
        for param in self.report_header:
            print(param[0].ljust(20), param[1])

# ===========================   Main  ========================================

# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory,
# Multiple, Description, Input Hook, Enabled

ael_variables = []
ael_variables.append([
    'cpi_Ins', 'CPI Index: ', 'FPriceIndex', acm.FPriceIndex.Instances(),
    'SACPI', 1, 0, 'Price Index parameter', None, 1
    ])
ael_variables.append([
    'portfolios', 'Portfolios: ', 'FPhysicalPortfolio',
    acm.FPhysicalPortfolio.Instances(), None, 1, 1, 'Portfolio parameter',
    None, 1
    ])
ael_variables.append([
    'Outpath', 'Output Path: ', 'string', None, 'F:\\\\', 1, 0, '', None, 1
    ])
ael_variables.append([
    'excl_status', 'Excluded Status: ', 'string',
    None, None, 1, 1, 'Enter status to be excluded (Comma separated)',
    None, 1
    ])
ael_variables.append([
    'excl_instype', 'Excluded InsTypes: ', 'string',
    None, None, 1, 1, 'Enter InsTypes to be excluded (Comma separated)',
    None, 1
    ])


def ael_main(data):
    """ Main method
    """
    report = LinkerResetLadderReport(data)
    report.print_header()
    calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()

    for port in report.portfolios:
        print('Extracting trades from portfolio: %s' % port.Name())
        # Get trades in portfolio where trade status is not Simulated or void,
        # and where the instrument has not expired.
        # Exclude all bonds and index linked bonds
        for trade in port.Trades().Filter(
                lambda x: x.Status() not in report.excl_status and
                x.Instrument().InsType() not in report.excl_instypes and
                not x.Instrument().IsExpired()):

            for leg in trade.Instrument().Legs():
                if (leg.IndexRef() and
                        leg.IndexRef().Name() == report.cpi.Name() and
                        abs(leg.InitialIndexValue()) > 0.0):

                    for cash_flow in leg.CashFlows():
                        for reset in cash_flow.Resets().Filter(
                            lambda x: ael.date(
                                x.Day()) >= report.start_date and
                                ael.date(x.Day()) <= report.end_date and
                                x.FixingValue() <= 0):

                            cf_dt = ael.date(reset.Day())
                            bump = 0.1
                            if cf_dt > report.mid_date:
                                multiplier = cf_dt.days_between(
                                    report.end_date)/report.mid_to_end_count
                                bump = bump*multiplier
                            elif cf_dt < report.mid_date:
                                multiplier = report.start_date.days_between(
                                    cf_dt)/report.start_to_mid_count
                                bump = bump*multiplier

                            fwd_rate = reset_fwd_rate(reset)
                            cf_calc_space = cash_flow.Calculation()
                            # cash_flow nominal
                            cf_nom = cf_calc_space.Nominal(
                                calc_space, trade,
                                cash_flow.Leg().Currency()).Number()
                            # cash_flow PV
                            pv0 = cf_calc_space.PresentValue(
                                calc_space, trade).Number()
                            try:
                                computed_trd_nom = cf_nom/fwd_rate
                                df = pv0/float(cf_nom)
                            except ZeroDivisionError as err:
                                print('Exception caught: ', err)
                                computed_trd_nom = 0
                                df = 0

                            new_nom = (fwd_rate + bump)*computed_trd_nom
                            pv1 = new_nom*df
                            pv01 = pv1 - pv0

                            # Add data to the report output
                            report.output.append([
                                trade.Oid(), trade.Instrument().Name(),
                                cash_flow.CashFlowType(),
                                cash_flow.StartDate(), cash_flow.PayDate(),
                                reset.Day(), trade.FaceValue(), cf_nom,
                                leg.InitialIndexValue(), fwd_rate,
                                cash_flow.FixedRate(),
                                cf_proj(cash_flow, trade), pv01,
                                trade.PortfolioId()
                                ])

    # Add column headers to the report
    report.report_header.append([])
    report.report_header.append([
        'Trdnbr', 'Instrument', 'Type', 'CF Start Date', 'CF Pay Date',
        'Reset Date', 'Trd Nom', 'CF Nom', 'Base CPI', 'Estimate', 'Rate',
        'Proj Val', 'Risk', 'Portfolio'
        ])

    # Add script output to the report and write to file
    report.output = report.report_header + report.output
    try:
        write_file(report.file_name, report.output)
        print('Wrote secondary output to:', report.file_name)
    except IOError:
        print('Error writing file: ', report.file_name)

    print('Report completed successfully.')
