"""
HISTORY
=====================================================================================================
Requester            Developer             CR number               Description
-----------------------------------------------------------------------------------------------------
Kudakwashe Mawoneke  Pavel Saparov         C1080637                Complete refactoring of valuation  
                                                                   and including new letterheads
Angelique Macnabe    Nada Jasikova         CHNG0002370855          - Add TRANS REF column
                                                                   - Default value for missing SPOT_RATE 
                                                                   is None                                                    
-----------------------------------------------------------------------------------------------------
"""
from __future__ import print_function

# Import stdlibs
import math
import os
import sys

# Import Front Arena libs
import acm
import at

from FReportSettings import XSLT_PATH
from XMLReport import XMLReportGenerator, CSVReportGenerator, StatementReportBase, SummaryRow
from XMLReport import contact_from_pty, mkinfo, mktable, mkcaption, mkdisclaimer, mkvalues
from zak_funcs import formnum


class Report(StatementReportBase):
    
    def __init__(self, mtm_ccy, cpty, date, trade_list):
        self.mtm_ccy = mtm_ccy
        self.cpty = cpty
        self.date = date
        self.trade_list = trade_list
        
        self.columns = [{ 'name': 'TRADE NUMBER' },
                        { 'name': 'TRANS REF'},
                        { 'name': 'INSTRUMENT TYPE' },                        
                        { 'name': 'EXPIRY DAY' },
                        { 'name': 'NOMINAL', 'width': '3cm' },
                        { 'name': 'STRIKE PRICE' },
                        { 'name': 'SPOT RATE' },
                        { 'name': 'ABSA BUYS/SELLS' },
                        { 'name': 'VOLATILITY' },
                        { 'name': 'MARK TO MARKET VALUE IN {0}'.format(self.mtm_ccy)}]
        
        self.std_calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        
        self.prf_calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')
        self.prf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        self.prf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom',
                                                 self.date.strftime("%Y-%m-%d"))
        
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
        yield mkcaption("Fx Option Revaluation Report for {0}".format(
                        self.date.strftime("%d %B %Y")))
    
        yield mkvalues(
            ('USD/ZAR', "{0:.4f}".format(self.fx_rate('USD'))),
            ('EUR/ZAR', "{0:.4f}".format(self.fx_rate('EUR'))),
            ('GBP/ZAR', "{0:.4f}".format(self.fx_rate('GBP')))
        )
        
        yield mktable(self.columns, self.generate_data())
        
        yield mkinfo("Please note that this revaluation is done from the bank's point "
                     "of view so a negative is in the client's favour")
        
        yield mkdisclaimer(*self.disclaimer())

    def statement_detail_csv(self):
        yield ["Fx Option Revaluation Report for {0}".format(self.date.strftime("%d %B %Y"))]
        yield [] # represents new line
        
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
        
        for t in self.trade_list:
            ins = t.Instrument()
            exp_date = ins.ExpiryDateOnly()
            
            if ins.InsType() == 'Combination':
                for link in ins.InstrumentMaps():
                    if link.Instrument().ExpiryDateOnly() > exp_date:
                        exp_date = link.Instrument().ExpiryDateOnly()
            
            if ins.InsType() == 'Option':
                und_ccy = ins.Underlying().Name()
                ins_type = "{0} Call".format(und_ccy) if ins.IsCallOption() \
                            else "{0} Put".format(und_ccy)
                nominal = "{0} {1}".format(und_ccy, formnum(t.Nominal()))
                strike_price = ins.StrikePrice()
            else:
                ins_type = ins.InsType()
                nominal = "{0} {1}".format(t.Currency().Name(), formnum(t.Nominal()))
                strike_price = ''
            
            spot_rate = ins.Calculation().UnderlyingPrice(self.std_calc_space)
            spot_rate = self._get_number_or_text_none(spot_rate)
            
            volatility = ins.Calculation().Volatility(self.std_calc_space)
            volatility = "{0:.2f}%".format(volatility * 100) if volatility else ''
            
            self.prf_calc_space.SimulateValue(t, 'Portfolio Currency', self.mtm_ccy)
            mark_to_market = self.prf_calc_space.CalculateValue(t, 'Portfolio Value').Number()
            
            # Since Combinations don't have explicitly expiry date
            # we have to skip those with zero MTM value
            if ins_type == 'Combination' and mark_to_market == 0.0:
                continue
            
            total_mtm += mark_to_market
            
            mark_to_market = formnum(mark_to_market) if (mark_to_market > 0) else \
                "({0})".format(formnum(abs(mark_to_market)))
                
            trans_ref = t.TrxTrade().Oid() if t.TrxTrade() else None
            
            data.append([
                t.Oid(),
                trans_ref,
                ins_type,
                exp_date,
                nominal,
                strike_price,
                spot_rate,
                "Buy" if t.Quantity() > 0 else "Sell",
                volatility,
                mark_to_market
            ])
        
        # Summary for MTM
        column_length = len(self.columns)
        l = SummaryRow(['' for i in range(column_length)])
        l[0] = "TOTAL IN {0}".format(self.mtm_ccy)
        l[column_length - 1] = formnum(total_mtm) if (total_mtm > 0) else "({0})".format(formnum(abs(total_mtm)))
        data.append(l)
        
        return data
    
    def _get_number_or_text_none(self, calculated_value):
        result = "None"
        if calculated_value:
            try:
                if math.isnan(calculated_value):
                    result = "None";
                else:
                    result = "{0:.4f}".format(float(calculated_value.Number()))
            except ValueError:
                result = "None"
        return result


def Valuation(mtm_ccy, ctpy, date, trade_list, output_dir, file_format):
    """Function generate PDF confirmation"""    
    if (str(acm.Class()) != "FTmServer" and 
            acm.User().UserGroup().Name() in ('Integration Process', 'System Processes')):
                output_dir = "//nfs/fa/reports/EMEA/prod/FAReports/PCGClientValuations/FxOption/"
    
    filename = "FXO_Client_Valuation-{0}-{1}".format(
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
    
    pdffile = gen.create(xml, filename)
    return pdffile

    
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
    ['date', 'Valuation Date:', 'string', None, acm.Time.DateToday()],
    ['mtm_ccy', 'MTM Currency:', 'string',
        sorted([c.Name() for c in acm.FCurrency.Select("")]), 'ZAR'],
    ['format', 'Output Format:', 'string', ['PDF', 'Excel'], 'PDF'],
    ['path', 'Output Folder:', 'string', None,
        r'Y:\Jhb\Arena\Data\PCG-Client-Valuations\Fx Option', 1],
]


def ael_main(kwargs):
    """Main loop"""
    
    VALID_INSTYPES = ('Option', 'Combination')
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
        if 'OPT' in trade_filter:
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
        if (trade.Instrument().InsType() in VALID_INSTYPES
            and (trade.Instrument().ExpiryDateOnly() > kwargs['date'] or 
                 trade.Instrument().ExpiryDateOnly() == '')):
                    # Combinations don't have expiry date
                    trade_list.append(trade)
    
    if len(trade_list) > 0:
        # All Trades should belong to ONE Counterparty only, hence
        # we can use any trade to pick-up client name
        counterparty = trade_list[0].Counterparty()
        pdffile = Valuation(mtm_ccy, counterparty, date, trade_list, path, file_format)
        os.startfile(pdffile)
    else:
        warning_function("Warning", "No Trades found for client valuation!", 0)
        sys.exit()

    print('Done...')
