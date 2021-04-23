"""
HISTORY
=====================================================================================================
Requester            Developer             CR number               Description
-----------------------------------------------------------------------------------------------------
Angelique Macnabe    Nada Jasikova         2295976                Create a valuation script to run 
                                                                  MtM reports for the combination 
                                                                  trades under SND Rates BTB 
                                                                  portfolio
-----------------------------------------------------------------------------------------------------
"""
from __future__ import print_function

# Import stdlibs
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
    
    def __init__(self, mtm_ccy, cpty, date, trade_list):
        self.mtm_ccy = mtm_ccy
        self.cpty = cpty
        self.date = date
        self.trade_list = trade_list
        
        self.columns = [{ 'name': 'DEAL NUMBER' },
                        { 'name': 'TRADE DATE' },
                        { 'name': 'MATURITY DATE' },
                        { 'name': 'CURRENCY OF NOMINAL' },
                        { 'name': 'NOMINAL AMOUNT' },
                        { 'name': 'MARK TO MARKET VALUE'}]
        
        self.std_calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        
        self.prf_calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')
        
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
        yield mkcaption("Combination Trade Valuation Report for {0}".format(
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
        yield ["Combination Trade Valuation Report for {0}".format(self.date.strftime("%d %B %Y"))]
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
            
            for link in ins.InstrumentMaps():
                if link.Instrument().ExpiryDateOnly() > exp_date:
                    exp_date = link.Instrument().ExpiryDateOnly()
        
            ins_type = ins.InsType()
            nominal = formnum(t.Premium())
            
            self.prf_calc_space.SimulateValue(t, 'Portfolio Currency', self.mtm_ccy)
            mark_to_market = self.prf_calc_space.CalculateValue(t, 'Portfolio Value').Number()
            
            # Since Combinations don't have explicitly expiry date
            # we have to skip those with zero MTM value
            if mark_to_market == 0.0:
                continue
            
            total_mtm += mark_to_market
            
            mark_to_market = (formnum(mark_to_market) if (mark_to_market > 0) else 
                "({0})".format(formnum(abs(mark_to_market))))
            
            data.append([
                t.Oid(),
                acm.Time.AsDate(t.TradeTime()),
                t.maturity_date(),
                self.mtm_ccy,
                nominal,
                mark_to_market
            ])
        
        # Summary for MTM
        column_length = len(self.columns)
        l = SummaryRow(['' for i in range(column_length)])
        l[0] = "TOTAL IN {0}".format(self.mtm_ccy)
        l[column_length - 1] = formnum(total_mtm) if (total_mtm > 0) else "({0})".format(formnum(abs(total_mtm)))
        data.append(l)
        
        return data


def Valuation(mtm_ccy, ctpy, date, trade_list, output_dir, file_format):
    """Function generate PDF confirmation"""    

    filename = "Combination_Trade_Valuation-{0}-{1}".format(
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

ael_variables = AelVariableHandler()
ael_variables.add('tf',
        label='Trade Filter',
        default='',
        mandatory=False,
        collection=sorted([f.Name() for f in acm.FTradeSelection.Select("")]))
ael_variables.add('trdnbr',
        label='Trade Number',
        default='0')
ael_variables.add('date',
        label='Valuation Date',
        default=acm.Time.DateToday())
ael_variables.add('mtm_ccy',
        label='MTM Currency',
        default='ZAR',
        collection=sorted([c.Name() for c in acm.FCurrency.Select("")]))
ael_variables.add('format',
        label='Output Format',
        default='PDF',
        collection=['PDF', 'Excel'])
ael_variables.add('path',
        label='Output Folder',
        default=r'Y:/Jhb/Arena/Data/PCG-Client-Valuations/Combinations')

def ael_main(kwargs):
    """Main loop"""
    
    VALID_INSTYPES = ('Combination')
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
        if 'COMBI' in trade_filter:
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
                    # Combinations don't have expiry da
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
