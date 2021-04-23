"""
HISTORY
================================================================================================================
Requester            Developer             CR number               Description
----------------------------------------------------------------------------------------------------------------
Macnabe, Angelique   Bhavik Mistry         CHNG0002917946    Initial implementation
Macnabe, Angelique   Fancy Dire            CHNG000    Replace ReferencePrice with Price and also change label 
                                                             from Spot Price to Forward Price on the report.

----------------------------------------------------------------------------------------------------------------
"""
from __future__ import print_function

# Import stdlibs
import os
import sys

# Import Front Arena libs
import acm
import at
import ael
from datetime import datetime
from math import isnan
from FReportSettings import XSLT_PATH
from XMLReport import XMLReportGenerator, CSVReportGenerator, StatementReportBase, SummaryRow
from XMLReport import contact_from_pty, mkinfo, mktable, mkcaption, mkdisclaimer
from zak_funcs import formnum
from xml.etree import ElementTree as ET
    
class Report(StatementReportBase):

    def __init__(self, cpty, date, trade_list, mtm_ccy):
        self.mtm_ccy = mtm_ccy
        self.cpty = cpty
        self.date = date
        self.trade_list = trade_list
        
        self.columns = [{ 'name': 'Trade Number' },
                        { 'name': 'Trade Date' },
                        { 'name': 'Value Date' },
                        { 'name': 'Instrument' },
                        { 'name': 'Quantity' },
                        { 'name': 'Buy/Sell' },
                        { 'name': 'Forward Price' },
                        {'name': 'MTM IN {0}'.format(self.mtm_ccy)}]
        
        self.spot_price_columns = [
            { 'name': 'Instrument' }, 
            { 'name': 'Quotation' }, 
            { 'name': 'Current Spot Price' },
            { 'name': 'Currency' }
        ]
        
        self.std_calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        
        self.prf_calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')
        self.prf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        self.prf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom',
                                                self.date.strftime("%Y-%m-%d"))


    def client_address(self):
        party_info = contact_from_pty(self.cpty)
        party_info['name'] = party_info['name']
        return party_info
    
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
            report = super(Report, self).create_report()
            return report
        elif output == 'csv':
            return self.statement_detail_csv()
    
    def statement_detail(self):
        """Override statement_detail to call xml version"""
        return self.statement_detail_xml()
        
    def statement_detail_xml(self):
        yield mkcaption("Spot prices for %s" % self.date.strftime("%d %B %Y"))
        
        yield mktable(self.spot_price_columns, self.generate_spot_price_data())
        
        yield mkcaption("Revaluation Report for {0}".format(self.date.strftime("%d %B %Y")))
        
        yield mktable(self.columns, self.generate_data())
        
        yield mkinfo("Please note that this valuation is done from the bank's point "
                     "of view so a negative value is in the client's favour")
        
        yield mkinfo("Please note Negative volume represents a Sell transaction "
                     "and Positive volume represents a Buy transaction")
        
        yield mkdisclaimer(*self.disclaimer())

    def statement_detail_csv(self):
        yield ["Revaluation Report for {0}".format(self.date.strftime("%d %B %Y"))]
        yield [] # represents new line
        
        yield ["Client: {0}".format(self.client_address()['name'])]
        yield []
        
        yield [column['name'] for column in self.spot_price_columns]
        for data in self.generate_spot_price_data():
            yield data
        yield []
        
        yield [column['name'] for column in self.columns]
        for data in self.generate_data():
            yield data
        yield []
        
        yield [("Please note that this valuation is done from the bank's point "
               "of view so a negative value is in the client's favour")]
        yield []
        
        yield [("Please note Negative volume represents a Sell transaction "
                "and Positive volume represents a Buy transaction")]
        yield []
        
        yield ["Disclaimer"]
        for line in self.disclaimer():
            yield [line.strip()]
    
    def generate_spot_price_data(self):
        data = []
        price_refs = set()

        for t in self.trade_list:
            rate = acm.FX().CreateFxRate(t.Instrument().Name(), t.Currency().Name())
            ins_name = t.Instrument().Name()
            
            if hasattr(t.Instrument().AdditionalInfo(), 'Commodity_Deli') and t.Instrument().AdditionalInfo().Commodity_Deli():
                ins_name = t.Instrument().AdditionalInfo().Commodity_Deli()

            price_refs.add((rate, ins_name))
        
        usd_zar = acm.FX().CreateFxRate('USD', 'ZAR')
        price_refs.add((usd_zar, 'USD/ZAR'))
        
        price_refs = sorted(list(price_refs), key=lambda e: e[0].Name())
        for price_ref in price_refs:
            commodity_name = price_ref[1]
            price_ref = price_ref[0]
            curr_spot_price = price_ref.Calculation().MarketPrice(self.std_calc_space)
            if isnan(curr_spot_price.Number()):
                curr_spot_price = price_ref.Calculation().MarkToMarketPrice(self.std_calc_space, acm.Time().DateToday(), price_ref.Currency())

            if price_ref.InsType() == 'Fx Rate':
                data.append([
                commodity_name,
                price_ref.Quotation().Name(),
                formnum(curr_spot_price.Number()),
                curr_spot_price.Unit()])

        return data
    
    def generate_data(self):
        data = []
        total_mtm = 0
       
                
        for t in self.trade_list:    
        
            try: 
                calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
                
                calc_space.SimulateValue(t, 'Portfolio Currency', self.mtm_ccy)
                calc = calc_space.CalculateValue(t, 'Total Val End')
                calc_space.RemoveSimulation(t, 'Portfolio Currency')
                
                mark_to_market = round(calc.Value().Number(), 2)
            except:
                mark_to_market = 0.0
            
            if hasattr(t.Instrument().AdditionalInfo(), 'Commodity_Deli') and t.Instrument().AdditionalInfo().Commodity_Deli():
                ins_name = t.Instrument().AdditionalInfo().Commodity_Deli()
            else:
                ins_name = t.Instrument().Name()
            
            # calculate total_mtm
            total_mtm += mark_to_market
            
            data.append([
                t.Oid(),
                at.date_to_ymd_string(t.TradeTime()),
                t.ValueDay(),
                ins_name,
                formnum(t.Quantity()) if (t.Quantity() > 0) else '(%s)' % formnum(abs(t.Quantity())),
                t.BoughtAsString(),
                formnum(t.Price()),           
                formnum(mark_to_market) if (mark_to_market > 0) else '(%s)' % formnum(abs(mark_to_market)),
            ])
        
        # Summary for MTM
        l = SummaryRow(['' for i in range(8)])
        l[0] = "TOTAL MTM"
        l[7] = formnum(total_mtm) if (total_mtm > 0) else "({0})".format(formnum(abs(total_mtm)))
        data.append(l)
        
        return data


def BuildValuation(ctpy, date, trade_list, output_dir, file_format, mtm_ccy):
    """Function generate PDF confirmation"""    
    if (str(acm.Class()) != "FTmServer" and 
            acm.User().UserGroup().Name() in ('Integration Process', 'System Processes')):
                output_dir = "//nfs/fa/reports/EMEA/prod/FAReports/PCGClientValuations/Valuations/"
    
    filename = "FX_Cash_Client_Valuation-{0}-{1}".format(
        ctpy.Fullname().replace('/', '_'),
        date.strftime("%d %b %Y")
    )

    report = Report(ctpy, date, trade_list, mtm_ccy)
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
    ['date', 'Valuation Date:', 'string',  dateKeys, 'Now', 1, 0, 1],
    ['mtm_ccy', 'MTM Currency:', 'string',        sorted([c.Name() for c in acm.FCurrency.Select("")]), 'ZAR'],
    ['format', 'Output Format:', 'string', ['PDF', 'Excel'], 'PDF'],
    ['path', 'Output Folder:', 'string', None,
        r'Y:\Jhb\Arena\Data\PCG-Client-Valuations\Commodity FX', 1],
]

def ael_main(kwargs):
    """Main loop"""
    
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
        if acm.FTradeSelection[trade_filter]:
            trades = acm.FTradeSelection[trade_filter].Trades()
        else:
            warning_function("Warning",
                "Invalid TradeFilter! Client valuation not generated!", 0)
            return 
            
    if trade_numbers != '0' and trade_filter == '':
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
        if (trade.Instrument().ExpiryDateOnly() > date.strftime("%Y-%m-%d") or 
             trade.ValueDay() > date.strftime("%Y-%m-%d")):
            trade_list.append(trade)

    if len(trade_list) > 0:
        # All Trades should belong to ONE Counterparty only, hence
        # we can use any trade to pick-up client name
        counterparty = trade_list[0].Counterparty()
        pdffile = BuildValuation(counterparty, date, trade_list, path, file_format, mtm_ccy)
        os.startfile(pdffile)
    else:
        warning_function("Warning", "No Trades found for client valuation!", 0)
        sys.exit()

    print('Done...')
