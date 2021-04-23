"""
HISTORY
==================================================================================================================
Requester            Developer             CR number               Description
------------------------------------------------------------------------------------------------------------------
Sean Lang           Kevin Kistan           CHNG0002186520 (2014-08-07)    Information for all Equity Options
Angelique Macnabe	Lester Williams        CHNG0002986731 (2015-07-22)    Remove division rule from Strike and Spot price
																		  Both were divided by 100

------------------------------------------------------------------------------------------------------------------
"""
from __future__ import print_function

# Import stdlibs
import os
import sys

# Import Front Arena libs
import acm
import at
import ael
import math
from datetime import *

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
        
        self.columns = [{ 'name': 'Trade Number' },
                        { 'name': 'Instrument Type' },
                        { 'name': 'Expiry Date' },
                        { 'name': 'Currency'},
                        { 'name': 'Nominal' },
                        { 'name': 'Strike Price' },
                        { 'name': 'Interest Rate' },
                        { 'name': 'Spot Price' },
                        { 'name': 'Buy/Sell' },
                        { 'name': 'Volatility' },
                        { 'name': 'MTM' }]
        
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
        yield ["Equity Option Revaluation Report for {0}".format(self.date.strftime("%d %B %Y"))]
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
            ins = t.Instrument()
            ins_name = t.Instrument().Name()
            legs = ins.Legs()
                        
            #Expiry Date
            exp_date = ins.ExpiryDateOnly()
            
            if ins.InsType() == 'Option':
                und_ccy = ins.Underlying().Name()
                ins_type = "{0} Call".format(und_ccy) if ins.IsCallOption() \
                            else "{0} Put".format(und_ccy)
                nominal = "{0}".format(formnum(t.Nominal()))
                strike_price = formnum(ins.StrikePrice())
            else:
                ins_type = ins.InsType()
                nominal = "{0}".format(formnum(t.Nominal()))
                strike_price = '0.00'
                
            #Trade Currency
            trade_curr = t.Currency().Name()
                
            #Calculate the Spot price
            spot_rate = ins.Calculation().UnderlyingPrice(self.std_calc_space).Number()
            spot_rate = '' if math.isnan(spot_rate) else formnum(spot_rate)
            
            #ABSA Buy Sell
            buy_sell = buy_sell = 'buy' if t.Quantity() > 0 else 'sell'

            #Volatility
            volatility = ins.Calculation().Volatility(self.std_calc_space)
            volatility = '' if math.isnan(volatility) else "{0:.2f}%".format(volatility * 100)
                            
            #MTM
            self.prf_calc_space.SimulateValue(t, 'Portfolio Currency', self.mtm_ccy)
            mark_to_market = self.prf_calc_space.CalculateValue(t, 'Portfolio Value').Number()
            
            #Interest Rate
            calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
            int_rate = calc_space.CalculateValue(t, 'Portfolio Discount Rate')
            if int_rate:
                int_rate = "{0:.4f}".format(int_rate * 100)
            else:
                in_rate = '0.00'
            

            # calculate total_mtm
            total_mtm += mark_to_market
            
            data.append([
                t.Oid(),
                ins_type,
                exp_date,
                trade_curr,
                nominal,
                strike_price,
                int_rate,
                spot_rate,
                "Buy" if t.Quantity() > 0 else "Sell",
                volatility,
                formnum(mark_to_market)
                
            ])
        
        # Summary for MTM
        l = SummaryRow(['' for i in range(11)])
        l[0] = "TOTAL MTM IN {0}".format(self.mtm_ccy)
        l[10] = formnum(total_mtm) if (total_mtm > 0) else "({0})".format(formnum(abs(total_mtm)))
        data.append(l)
        
        return data


def BuildValuation(mtm_ccy, ctpy, date, trade_list, output_dir, file_format):
    """Function generate PDF confirmation"""    
    if (str(acm.Class()) != "FTmServer" and 
            acm.User().UserGroup().Name() in ('Integration Process', 'System Processes')):
                output_dir = "//nfs/fa/reports/EMEA/prod/FAReports/PCGClientValuations/Valuations/"
    
    filename = "Equity_Option_Client_Valuation-{0}-{1}".format(
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


TODAY = acm.Time().DateToday()

# Generate date lists to be used as drop downs in the GUI.
dateList   = {'Custom Date':TODAY,
              'Now':TODAY}
dateKeys = dateList.keys()
dateKeys.sort()


ael_variables = [
    ['tf', 'TradeFilter:', 'string',
        sorted([f.Name() for f in acm.FTradeSelection.Select("")]), ''],
    ['trdnbr', 'Trade Number:', 'string', None, '0'],
    ['skip_instypes', 'Skip InsTypes:', 'string', None, ''],
    ['date', 'Valuation Date:', 'string',  dateKeys, 'Now', 1, 0, 1],
    ['mtm_ccy', 'MTM Currency:', 'string',
        sorted([c.Name() for c in acm.FCurrency.Select("")]), 'ZAR'],
    ['format', 'Output Format:', 'string', ['PDF', 'Excel'], 'PDF'],
    ['path', 'Output Folder:', 'string', None,
        r'Y:\Jhb\Arena\Data\PCG-Client-Valuations\Equity Derivatives', 1],
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
        date = datetime.strptime(dateList[kwargs['date']], "%Y-%m-%d")
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
        if 'EQOP' in trade_filter:
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
            and (trade.Instrument().ExpiryDateOnly() > date.strftime("%Y-%m-%d") or 
                 trade.ValueDay() > date.strftime("%Y-%m-%d"))):
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
