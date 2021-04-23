"""
HISTORY
====================================================================================================
Requester            Developer             CR number               Description
----------------------------------------------------------------------------------------------------
Angelique Macnabe    Pavel Saparov         CHNG0002585234          Commodity options client valuation report.
----------------------------------------------------------------------------------------------------
"""
from __future__ import print_function

# Import stdlibs
import math
import os
import sys

# Import Front Arena libs
import acm
import at

from at_ael_variables import AelVariableHandler
from FReportSettings import XSLT_PATH
from XMLReport import XMLReportGenerator, CSVReportGenerator, StatementReportBase, SummaryRow
from XMLReport import contact_from_pty, mkinfo, mktable, mkcaption, mkdisclaimer, mkvalues
from zak_funcs import formnum


class Report(StatementReportBase):

    rename_product = {
        'USD/ALUMINIUM_LME/FWD': 'Aluminium',
        'USD/BRENT_CRUDE_ICE/FWD': 'Crude Oil (Brent)',
        'USD/COAL_API4_NYMEX/FWD': 'Coal_API4',
        'USD/COPPER_LME/FWD': 'Copper',
        'USD/GASOIL_ICE/FWD': 'Gasoil',
        'USD/GO05CFS/FWD': 'HSFO 180 Cargoes FOB SGP',
        'USD/GO500PPMCFS/FWD': 'Gold',
        'USD/GOLD_COMEX/FWD': 'Gold',
        'USD/HSFO180Cargoes_PLATTS/FWD': 'HSFO 180 Cargoes FOB SGP',
        'USD/ICE_GASOIL/FWD': 'Gasoil',
        'USD/JET_CCN_Platts/FWD': 'JET_CCN_Platts',
        'USD/JET_KEROCFS_Platts/FWD': 'JET_KEROCFS',
        'USD/LEAD_LME/FWD': 'Lead',
        'USD/NICKEL_LME/FWD': 'Nickel',
        'USD/PALLADIUM_NYMEX/FWD': 'Palladium',
        'USD/PLATINUM_NYMEX/FWD': 'Platinum',
        'USD/SILVER_COMEX/FWD': 'Silver',
        'USD/TIN_LME/FWD': 'Aluminium',
        'USD/UD10CCN_PLATTS/FWD': 'UD10CCN',
        'USD/WTI_NYMEX/FWD': 'Crude Oil (WTI)',
        'USD/ZINC_LME/FWD': 'Zinc',
        'USD/COTTON/NYBOT': 'Cotton',
    }

    rename_quotation = {
        'Brent Crude oil Bbl': 'Barrels',
        'WTI Crude oil bbl': 'Barrels',
    }

    def __init__(self, mtm_ccy, cpty, date, trade_list):
        """Init Report"""
        self.mtm_ccy = mtm_ccy
        self.cpty = cpty
        self.date = date
        self.trade_list = trade_list

        self.columns = [{'name': 'TRADE NUMBER'},
                        {'name': 'PRODUCT'},
                        {'name': 'CALL/PUT'},
                        {'name': 'ACQUIRE DAY'},
                        {'name': 'EXPIRY DAY'},
                        {'name': 'NOMINAL'},
                        {'name': 'STRIKE PRICE'},
                        {'name': 'SPOT PRICE'},
                        {'name': 'ABSA BUYS/SELLS'},
                        {'name': 'QUOTATION'},
                        {'name': 'MTM IN {0}'.format(self.mtm_ccy)}]

        self.std_calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()

        self.prf_calc_space = acm.Calculations().CreateCalculationSpace(
            'Standard', 'FPortfolioSheet')
        self.prf_calc_space.SimulateGlobalValue(
            'Portfolio Profit Loss End Date', 'Custom Date')
        self.prf_calc_space.SimulateGlobalValue(
            'Portfolio Profit Loss End Date Custom', self.date.strftime("%Y-%m-%d"))

    def fx_rate(self, from_curr):
        """Obtain not discounted SPOT historical prices."""
        date = self.date.strftime("%Y-%m-%d")
        from_curr = acm.FCurrency[from_curr]
        return from_curr.UsedPrice(date, acm.FCurrency['ZAR'], 'SPOT')

    def client_address(self):
        return contact_from_pty(self.cpty)

    def disclaimer(self):
        disclaimer, dsc = os.path.join(XSLT_PATH, 'Client_Valuations_Disclaimer.txt'), []
        with open(disclaimer, 'rb') as fp:
            for line in fp:
                dsc.append(line)
        return dsc

    def create_report(self, output):
        """Create the report in XML or CSV.

        Args:
            output: report's output format (pdf or csv)
        """
        if output == 'xml':
            return super(Report, self).create_report()
        elif output == 'csv':
            return self.statement_detail_csv()

    def statement_detail(self):
        """Override statement_detail to call xml version"""
        return self.statement_detail_xml()

    def statement_detail_xml(self):
        yield mkcaption("Commodity Option Revaluation Report for {0}".format(
            self.date.strftime("%d %B %Y")))

        yield mkvalues(
            ('Starting spot rates', ''),
            ('USD/ZAR', "{0:.4f}".format(self.fx_rate('USD'))),
            ('EUR/ZAR', "{0:.4f}".format(self.fx_rate('EUR'))),
            ('GBP/ZAR', "{0:.4f}".format(self.fx_rate('GBP')))
        )

        yield mktable(self.columns, self.generate_data())

        yield mkinfo("Please note that this revaluation is done from the bank's point "
                     "of view so a negative is in the client's favour")

        yield mkdisclaimer(*self.disclaimer())

    def statement_detail_csv(self):
        yield ["Commodity Option Revaluation Report for {0}".format(
            self.date.strftime("%d %B %Y"))]

        yield [] # represents a new line

        yield ["Starting spot rates"]
        yield ["USD/ZAR: {0:.4f}".format(self.fx_rate('USD'))]
        yield ["EUR/ZAR: {0:.4f}".format(self.fx_rate('EUR'))]
        yield ["GBP/ZAR: {0:.4f}".format(self.fx_rate('GBP'))]
        yield []

        yield ["Client: {0}".format(self.client_address()['name'])]
        yield []

        yield [column['name'] for column in self.columns]
        for data in self.generate_data():
            yield data
        yield []

        yield [("Please note that this valuation is done from the bank's point "
               "of view so a negative value is in the client's favour")]
        yield []

        yield ["Disclaimer"]
        for line in self.disclaimer():
            yield [line.strip()]

    def generate_data(self):
        data = []
        total_mtm = 0.0

        for trade in self.trade_list:

            ins = trade.Instrument()
            exp_date = ins.ExpiryDateOnly()
            acquire_date = trade.AcquireDay()
            nominal = formnum(trade.Nominal())
            strike_price = "{0:.2f}".format(ins.StrikePrice())

            quotation = ins.Quotation().Name()
            quotation = self.rename_quotation.get(quotation, quotation)

            try:
                price_curve = self._get_price_curve_name(trade)
                product = self.rename_product[price_curve]
            except (AttributeError, KeyError):
                product = ins.Underlying().Name()

            spot_rate = ins.Calculation().UnderlyingPrice(self.std_calc_space)
            spot_rate = self._get_number_or_text_none(spot_rate)

            self.prf_calc_space.SimulateValue(
                trade, 'Portfolio Currency', self.mtm_ccy)

            mark_to_market = self.prf_calc_space.CalculateValue(
                trade, 'Portfolio Value').Number()

            self.prf_calc_space.RemoveSimulation(
                trade, 'Portfolio Currency')

            total_mtm += mark_to_market

            mark_to_market = formnum(mark_to_market) if (mark_to_market > 0) else \
                "({0})".format(formnum(abs(mark_to_market)))

            data.append([
                trade.Oid(),
                product,
                "Call" if ins.IsCallOption() else "Put",
                acquire_date,
                exp_date,
                nominal,
                strike_price,
                spot_rate,
                "Buy" if trade.Quantity() > 0 else "Sell",
                quotation,
                mark_to_market
            ])

        # Summary for MTM
        column_length = len(self.columns)
        summary = SummaryRow(['' for i in range(column_length)])
        summary[0] = "TOTAL IN {0}".format(self.mtm_ccy)
        summary[column_length-1] = formnum(total_mtm) if (total_mtm > 0) else \
            "({0})".format(formnum(abs(total_mtm)))
        data.append(summary)

        return data

    def _get_number_or_text_none(self, calculated_value):
        result = "None"
        if calculated_value:
            try:
                if math.isnan(calculated_value):
                    result = "None";
                else:
                    result = "{0:.2f}".format(
                        float(calculated_value.Number()))
            except ValueError:
                result = "None"
        return result

    def _get_price_curve_name(self, trade):
        curve_calc_space = self.prf_calc_space.CalculateValue(trade,
                    'BasePriceCurveInTheoreticalValue')
        
        if acm.IsHistoricalMode():
            curve_calc_space = curve_calc_space.OriginalCurve()
        
        return curve_calc_space.Name()

def BuildValuation(mtm_ccy, ctpy, date, trade_list, output_dir, file_format):
    """Function generate PDF confirmation"""

    filename = "Comm_Options_Client_Valuation-{0}-{1}".format(
        ctpy.Fullname().replace('/', '_'),
        date.strftime("%d %b %Y")
    )

    report = Report(mtm_ccy, ctpy, date, trade_list)
    xml = report.create_report(file_format)

    if file_format == 'xml':
        gen = XMLReportGenerator(output_dir)
        # we have to use 'true' as string because ElementTree
        # is not capable to convert it in Py2.6
        gen.set('Landscape', 'true')
    elif file_format == 'csv':
        gen = CSVReportGenerator(output_dir)

    new_report = gen.create(xml, filename)
    return new_report


def ASQL(*rest):
    """ASQL calling from Information Manager"""
    if str(acm.Class()) == "FTmServer":
        acm.RunModuleWithParameters(__name__, acm.GetDefaultContext().Name())
        return 'SUCCESS'
    else:
        return 'FAILED'

ael_variables = AelVariableHandler()

ael_variables.add(
    'tf',
    label='Trade Filter:',
    mandatory=False,
    collection=sorted([f.Name() for f in acm.FTradeSelection.Select('')])
)
ael_variables.add(
    'trdnbr',
    label='Trade Number:',
    mandatory=False,
    default='0'
)
ael_variables.add(
    'valid_instypes',
    label='Valid Instrument Types:',
    mandatory=True,
    default='Option',
    enabled=False
)
ael_variables.add(
    'date',
    label='Valuation Date:',
    mandatory=True,
    default=acm.Time.DateToday()
)
ael_variables.add(
    'mtm_ccy',
    label='MTM Currency:',
    mandatory=True,
    default='ZAR',
    collection=sorted([c.Name() for c in acm.FCurrency.Select('')])
)
ael_variables.add(
    'format',
    label='Output Format:',
    mandatory=True,
    default='PDF',
    collection=['PDF', 'Excel']
)
ael_variables.add(
    'path',
    label='Output Folder:',
    mandatory=True,
    default=r'Y:\Jhb\Arena\Data\PCG-Client-Valuations\Commodity Options'
)


def ael_main(kwargs):
    """Main loop"""

    VALID_INSTYPES = kwargs['valid_instypes']
    FILE_OUTPUT = {'Excel': 'csv', 'PDF': 'xml'}

    file_format = FILE_OUTPUT[kwargs['format']]
    trade_numbers = kwargs['trdnbr']
    trade_filter = kwargs['tf']
    mtm_ccy = kwargs['mtm_ccy']
    path = kwargs['path']
    date = at.date_to_datetime(kwargs['date'])

    if str(acm.Class()) == "FTmServer":
        warning_function = acm.GetFunction("msgBox", 3)
    else:
        warning_function = lambda t, m, *r: print("{0}: {1}")

    try:
        date = at.date_to_datetime(kwargs['date'])
    except ValueError:
        warning_function("Warning", "Invalid Date!", 0)
        return

    if not os.access(path, os.W_OK):
        warning_function("Warning",
            "Output path is not writable! Client valuation not generated!", 0)
        return

    if trade_numbers != '0' and trade_filter != '':
        warning_function("Warning",
            "Invalid Parameters! Client valuation not generated!", 0)
        return

    print('Loading...')

    # Validate user input
    if trade_numbers == '0' and trade_filter != '':
        if 'comm' in trade_filter.lower():
            trades = acm.FTradeSelection[trade_filter].Trades()
        else:
            warning_function("Warning",
                "Invalid TradeFilter! Client valuation not generated!", 0)
            return

    elif trade_numbers != '0' and trade_filter == '':
        try:
            trades = [acm.FTrade[int(t)] for t in trade_numbers.split(',')]
        except ValueError:
            warning_function("Warning",
                "Invalid Trade provided! Client valuation not generated!", 0)
            return

    elif trade_numbers == '0' and trade_filter == '':
            warning_function("Warning",
                "No Trades provided! Client valuation not generated!", 0)
            return

    # Filter trades for valuation
    trade_list = []
    for trade in trades:
        if (trade.Instrument().InsType() in VALID_INSTYPES
            and (trade.Instrument().ExpiryDateOnly() > kwargs['date'] or
                 trade.Instrument().ExpiryDateOnly() == '')):
                    trade_list.append(trade)

    if len(trade_list) > 0:
        # All Trades should belong to ONE Counterparty only, hence
        # we can use any trade to pick-up client name
        counterparty = trade_list[0].Counterparty()
        pdffile = BuildValuation(mtm_ccy, counterparty, date, trade_list, path, file_format)
        os.startfile(pdffile)
    else:
        warning_function("Warning", "No Trades found for client valuation!", 0)
        sys.exit()

    print('Done...')
