"""
HISTORY
====================================================================================================
Requester            Developer             CR number               Description
----------------------------------------------------------------------------------------------------
Mduduzi Nhlapo       Willie van der Bank   C889542 (2012-02-09)    Updated MTM_ZAR calculation
Ryan Bates           Pavel Saparov         C1080603 (2013-06-14)   Complete refactoring of valuation
                                                                   and including new letterheads
----------------------------------------------------------------------------------------------------
"""
from __future__ import print_function

# Import stdlibs
import os
import sys

# Import Front Arena libs
import acm
import at

from FReportSettings import XSLT_PATH
from XMLReport import XMLReportGenerator, CSVReportGenerator, StatementReportBase, SummaryRow
from XMLReport import contact_from_pty, mkinfo, mktable, mkcaption, mkdisclaimer
from zak_funcs import formnum


class Report(StatementReportBase):
    
    def __init__(self, mtm_ccy, cpty, date, trade_list):
        self.mtm_ccy = mtm_ccy
        self.cpty = cpty
        self.date = date
        self.trade_list = trade_list
        
        self.columns = [{ 'name': 'TRADE NUMBER' },
                        { 'name': 'TRADE DATE' },
                        { 'name': 'MATURITY DATE' },
                        { 'name': 'INSTRUMENT' },
                        { 'name': 'CURRENCY 1' },
                        { 'name': 'NOMINAL 1' },
                        { 'name': 'CURRENCY 2' },
                        { 'name': 'NOMINAL 2' },
                        { 'name': 'MARK TO MARKET VALUE IN {0}'.format(self.mtm_ccy) }]
        
        self.std_calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        
        self.prf_calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')
        self.prf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        self.prf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom',
                                                self.date.strftime("%Y-%m-%d"))

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
            
        :param output: string xml|csv
        """
        if output == 'xml':
            return super(Report, self).create_report()
        elif output == 'csv':
            return self.statement_detail_csv()
    
    def statement_detail(self):
        """Override statement_detail to call xml version"""
        return self.statement_detail_xml()
        
    def statement_detail_xml(self):
        yield mkcaption("Revaluation Report for {0}".format(self.date.strftime("%d %B %Y")))
        
        yield mktable(self.columns, self.generate_data())
        
        yield mkinfo("Please note that this valuation is done from the bank's point "
                     "of view so a negative value is in the client's favour")
        
        yield mkdisclaimer(*self.disclaimer())

    def statement_detail_csv(self):
        yield ["Revaluation Report for {0}".format(self.date.strftime("%d %B %Y"))]
        yield [] # represents new line
        
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
        date = self.date.strftime("%Y-%m-%d")
        total_mtm = 0.0
        
        for t in self.trade_list:
            legs = t.Instrument().Legs()
            
            if legs:
                if len(legs) == 2:
                    for leg in legs:
                        if leg.PayLeg():
                            currency_1 = leg.Currency().Name()
                            nominal_1 = -1 * leg.Calculation().Nominal(self.std_calc_space, t,
                                date, currency_1).Number()
                        else:
                            currency_2 = leg.Currency().Name()
                            nominal_2 = leg.Calculation().Nominal(self.std_calc_space, t,
                                date, currency_2).Number()

                elif len(legs) == 1:
                    currency_1 = currency_2 = legs[0].Currency().Name()
                    nominal_1 = nominal_2 = t.Nominal()
                    
                    for cashflow in legs[0].CashFlows():
                        if not(cashflow.StartDate() <= date <= cashflow.EndDate()):
                            continue
                        
                        nominal_1 = nominal_2 = cashflow.Calculation().Nominal(self.std_calc_space,
                            t, currency_1).Number()
            else:
                currency_1 = currency_2 = t.Currency().Name()
                nominal_1 = nominal_2 = t.Nominal()

            ins_type = 'FxSwap' if t.Instrument().InsType() == 'Curr' else \
                            t.Instrument().InsType()
            
            exp_date = t.ValueDay() if t.Instrument().InsType() == 'Curr' else \
                            t.Instrument().ExpiryDateOnly()
            
            self.prf_calc_space.SimulateValue(t, 'Portfolio Currency', self.mtm_ccy)
            
            mark_to_market = self.prf_calc_space.CalculateValue(
                                 t, 'Portfolio Value').Number()
            
            
            # calculate total_mtm per currency_1
            total_mtm += mark_to_market
            
            mark_to_market = formnum(mark_to_market) if (mark_to_market > 0) else \
                "({0})".format(formnum(abs(mark_to_market)))
            
            data.append([
                t.Oid(),
                at.date_to_ymd_string(t.TradeTime()),
                exp_date,
                ins_type,
                currency_1,
                formnum(nominal_1),
                currency_2,
                formnum(nominal_2),
                mark_to_market
            ])
        
        # Summary for MTM
        l = SummaryRow(['' for i in range(9)])
        l[0] = "TOTAL IN {0}".format(self.mtm_ccy)
        l[8] = formnum(total_mtm) if (total_mtm > 0) else "({0})".format(formnum(abs(total_mtm)))
        data.append(l)
        
        return data


def BuildValuation(mtm_ccy, ctpy, date, trade_list, output_dir, file_format):
    """Function generate PDF confirmation"""    
    if (str(acm.Class()) != "FTmServer" and 
            acm.User().UserGroup().Name() in ('Integration Process', 'System Processes')):
                output_dir = "//nfs/fa/reports/EMEA/prod/FAReports/PCGClientValuations/Valuations/"
    
    filename = "IRD_Client_Valuation-{0}-{1}".format(
        ctpy.Fullname().replace('/', '_'),
        date.strftime("%d %b %Y")
    )

    report = Report(mtm_ccy, ctpy, date, trade_list)
    gen_data = report.create_report(file_format)
    
    if file_format == 'xml':
        gen = XMLReportGenerator(output_dir)
        # we have to use 'true' as string because ElementTree
        # is not capable to convert it in Py2.6
        gen.set('Landscape', 'true')
    
    elif file_format == 'csv':
        gen = CSVReportGenerator(output_dir)
    
    out_file = gen.create(gen_data, filename)
    return out_file
    

def ASQL(*rest):
    """ASQL calling from Information Manager"""
    if str(acm.Class()) == "FTmServer":
        acm.RunModuleWithParameters(__name__, acm.GetDefaultContext().Name())
        return 'SUCCESS'
    else:
        return 'FAILED'


ael_variables = [
    ['tf', 'TradeFilter:', 'string',
        sorted([f.Name() for f in acm.FTradeSelection.Select("")]), ''],
    ['trdnbr', 'Trade Number:', 'string', None, '0'],
    ['skip_instypes', 'Skip InsTypes:', 'string', None, 'FxSwap'],
    ['date', 'Valuation Date:', 'string', None, acm.Time.DateToday()],
    ['mtm_ccy', 'MTM Currency:', 'string',
        sorted([c.Name() for c in acm.FCurrency.Select("")]), 'ZAR'],
    ['format', 'Output Format:', 'string', ['PDF', 'Excel'], 'PDF'],
    ['path', 'Output Folder:', 'string', None,
        r'Y:\Jhb\Arena\Data\PCG-Client-Valuations\Valuations', 1],
]


def ael_main(kwargs):
    """Main loop"""
    
    SKIP_INSTYPES = kwargs['skip_instypes']
    SKIP_INSTYPES = SKIP_INSTYPES.split(",")
    FILE_OUTPUT = {'Excel': 'csv', 'PDF': 'xml'}
    
    file_format = FILE_OUTPUT[kwargs['format']]
    trade_numbers = kwargs['trdnbr']
    trade_filter = kwargs['tf']
    mtm_ccy = kwargs['mtm_ccy']
    path = kwargs['path']

    
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
        if 'IRD' in trade_filter:
            trades = acm.FTradeSelection[trade_filter].Trades()
        else:
            warning_function("Warning",
                "Invalid TradeFilter! Client valuation not generated!", 0)
            return 
    
    elif trade_numbers != '0' and trade_filter == '':
        try:
            trades = map(lambda t: acm.FTrade[int(t)], trade_numbers.split(','))
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
        if (trade.Instrument().InsType() not in SKIP_INSTYPES
            and (trade.Instrument().ExpiryDateOnly() > kwargs['date'] or 
                 trade.ValueDay() > kwargs['date'])):
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
