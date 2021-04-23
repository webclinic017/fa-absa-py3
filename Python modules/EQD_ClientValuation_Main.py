'''
Developer   : Tshepo Mabena
Name        : EQD_ClientValuation_Main
Date        : 25/09/2009
Description : This module generates client valuations in pdf.

Updates:

Developer           : Tshepo Mabena
Purpose             : Rounding-off calculated fields to two decimal places and changing the date format of the trade date field. 
Department and Desk : Primes Services Collateral Management and Client Valuations
Requester           : Mduduzi Nhlapo
CR Number           : 243325
Date                : 03/03/2010 

Developer           : Tshepo Mabena
Purpose             : Correction on the nominal for options based on the forward start type in the addinfo
Department and Desk : Primes Services Collateral Management and Client Valuations
Requester           : Mduduzi Nhlapo
CR Number           : 334191
Date                : 07/06/2010

Developer           : Ntuthuko Matthews
Purpose             : Add an option to output the report into an excel format
Department and Desk : Primes Services Collateral Management and Client Valuations
Requester           : Ryan Bates
CR Number           : 803296
Date                : 08/02/2013

Developer           : Conicov Andrei
Purpose             : Fix the nominal for stock options
Department and Desk : PCG
Requester           : Mawoneke Kudakwashe
CR Number           : 803296
Date                : 05/06/2013

Developer           : Kevin Kistan
Purpose             : Added Spot Price Column
Department and Desk : PCG
Requester           : sean Laing
CR Number           : CHNG0002186520
Date                : 07/08/2014

Developer           : Lester Williams
Purpose             : Remove division rule from Spot price
Department and Desk : PCG
Requester           : Angelique Macnabe
CR Number           : CHNG0002986731
Date                : 22/07/2015
'''

from __future__ import print_function

# Import stdlibs
import os
import sys
import math

# Import Front Arena libs
import acm, ael
import at
import FRunScriptGUI
from datetime import *

from FReportSettings import XSLT_PATH
from XMLReport import XMLReportGenerator, CSVReportGenerator, StatementReportBase, SummaryRow
from XMLReport import contact_from_pty, mkinfo, mktable, mkcaption, mkdisclaimer
from zak_funcs import formnum

class Report(StatementReportBase):

    def __init__(self, mtm_ccy, cpty, date, trade_list):
        self.date = date
        self.mtm_ccy = mtm_ccy
        self.cpty = cpty
        self.trade_list = trade_list
        
        self.columns = [{ 'name': 'Option Type' },
                        { 'name': 'Deal Number' },
                        { 'name': 'Trade Date' },
                        { 'name': 'Expiry Date' },
                        { 'name': 'Strike Price' },
                        { 'name': 'Spot Price' },
                        { 'name': 'Nominal in {0}'.format(self.mtm_ccy) },
                        { 'name': 'MTM in {0}'.format(self.mtm_ccy) }]
        
        self.std_calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        
        self.prf_calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')
        self.prf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        self.prf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom',
                                                self.date.strftime("%Y-%m-%d"))
        
    def client_address(self):
        return contact_from_pty(self.cpty) 
    
    def disclaimer(self):
        # To delete, have to use the configuration
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
        yield mkcaption("Equity Derivatives Revaluation Report for {0}".format(self.date.strftime("%d %B %Y")))
        
        yield mktable(self.columns, self.generate_data())
        
        yield mkinfo("Please note that this valuation is done from the bank's point "
                     "of view so a negative value is in the client's favour")
        
        yield mkdisclaimer(*self.disclaimer())
    
    def statement_detail_csv(self):
        yield ["Equity Derivatives Revaluation Report for {0}".format(self.date.strftime("%d %B %Y"))]
        yield []  # represents new line
        
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
            option_type = self._get_option_type(t)
                
            nominal = self._get_nominal(t, self.date)
            
            exp_date = t.ValueDay() if t.Instrument().InsType() == 'Curr' else \
                            t.Instrument().ExpiryDateOnly()
            if hasattr(t.Instrument(), 'StrikePrice'):
                strike_price = str(formnum(t.Instrument().StrikePrice()))
            else:
                strike_price = str(formnum(0))
            
            self.prf_calc_space.SimulateValue(t, 'Portfolio Currency', self.mtm_ccy)
            
            mark_to_market = self.prf_calc_space.CalculateValue(
                                 t, 'Portfolio Value').Number()
            
            #Calculate the Spot price
            spot_rate = ins.Calculation().UnderlyingPrice(self.std_calc_space).Number()
            spot_rate = '' if math.isnan(spot_rate) else formnum(spot_rate)
            
            # calculate total_mtm per currency_1
            total_mtm += mark_to_market
            
            mark_to_market = formnum(mark_to_market) if (mark_to_market > 0) else \
                "({0})".format(formnum(abs(mark_to_market)))
        
            data.append([
                option_type,
                t.Oid(),
                at.date_to_ymd_string(t.TradeTime()),
                exp_date,
                strike_price,
                spot_rate,
                nominal,
                mark_to_market
                         ])
        
        # Summary for MTM
        l = SummaryRow(['' for i in range(8)])
        l[0] = "TOTAL IN {0}".format(self.mtm_ccy)
        l[7] = formnum(total_mtm) if (total_mtm > 0) else "({0})".format(formnum(abs(total_mtm)))
        data.append(l)    
        
        return data    
       
    def _get_option_type(self, t):
        OptionType = ' '
        quantity = t.Quantity()
        # the option type is defined only for non zero quantity trades
        if quantity == 0:
            return OptionType
        
        inst_type = t.Instrument().InsType()
        
        if inst_type == 'Option':
            if not t.Instrument().IsCallOption():
                OptionType = 'LongPut' if quantity > 0 else 'ShortPut'
            else:
                OptionType = 'LongCall' if quantity > 0 else 'ShortCall'
        elif inst_type == 'Future/Forward':
            OptionType = 'LongExcluded' if quantity > 0 else 'ShortExcluded'
        
        return OptionType

    def _get_nominal(self, t, date):
        Nominal = 0    
    
        if t.Instrument().InsType() == 'Option':
            quotation_factor = t.Instrument().Underlying().Quotation().QuotationFactor()
            spot_price = t.Instrument().Underlying().UsedPrice(self.date.strftime("%d/%m/%Y"), self.mtm_ccy, 'SPOT')
            nominal_amount = t.Nominal()
            
            Nominal = formnum(spot_price * nominal_amount * quotation_factor)
            add_info_value = t.Instrument().add_info('Forward Start Type')
            if add_info_value and add_info_value == 'Performance':
                Nominal = formnum(t.Nominal())
        else:
            Nominal = formnum(t.Nominal())
            
        return Nominal
    

def _build_valuation(ctpy, date, trade_list, output_dir, file_format):
    """Generate a PDF or CSV client valuation"""    
    if (str(acm.Class()) != "FTmServer" and 
            acm.User().UserGroup().Name() in ('Integration Process', 'System Processes')):
                output_dir = "//nfs/fa/reports/EMEA/prod/FAReports/PCGClientValuations/Valuations/"
                
    '''print(type(date))
    print(date)
    dtdate = datetime.strptime(date,"%Y-%m-%d")
    print(type(dtdate))'''
    
    filename = "Client_Valuation-{0}-{1}".format(
        ctpy.Fullname().replace('/', '_'),
        date.strftime("%d %b %Y")
    )

    report = Report('ZAR', ctpy, date, trade_list)
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

def _similar_counter_parties(trade_list):
    ''' Checks if all counterparties are equal '''
    counterparty_id = trade_list[0].CounterpartyId()
    for t in trade_list:
        if counterparty_id != t.CounterpartyId():
            return False 
    return True
        

def ASQL(*rest):
    """ASQL calling from Information Manager"""
    if str(acm.Class()) == "FTmServer":
        acm.RunModuleWithParameters(__name__, acm.GetDefaultContext().Name())
        return 'SUCCESS'
    else:
        return 'FAILED'
       
def _get_trade_filters():
    ''' Returns a list of sorted trade filter
    '''
    filters = []
    for f in ael.TradeFilter:
        filters.append(f.fltid)
    filters.sort()
    
    return filters    

# directorySelection = FRunScriptGUI.DirectorySelection()

TODAY = acm.Time().DateToday()

# Generate date lists to be used as drop downs in the GUI.
dateList   = {'Custom Date':TODAY,
              'Now':TODAY}
dateKeys = dateList.keys()
dateKeys.sort()

NO_TRADE_FILTER = '0'
output_path = R'Y:\Jhb\Arena\Data\PCG-Client-Valuations\Equity Derivatives'
''' tf, trdnbr, date, format, path '''
# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [('tf', 'Trade Filter:', 'string', _get_trade_filters(), ''),
                ('trdnbr', 'Trade Number:', 'string', None, NO_TRADE_FILTER),
                ('date', 'Valuation Date:', 'string',  dateKeys, 'Now', 1, 0, 1),
                ('format', 'Output Format', 'string', ['PDF', 'Excel'], 'PDF'),
                ['path', 'Output Directory:', 'string', None, output_path, 1]
                ]
                
def ael_main(kwargs):
    
    FILE_OUTPUT = {'Excel': 'csv', 'PDF': 'xml'}
    
    file_format = FILE_OUTPUT[kwargs['format']]
    trade_numbers = kwargs['trdnbr']
    trade_filter = kwargs['tf']
    path = kwargs['path']
    
    if str(acm.Class()) == "FTmServer":
        warning_function = acm.GetFunction("msgBox", 3)
    else:
        warning_function = lambda t, m, *r: print("{0}: {1}".format(t, m))
        
    try:
        date = datetime.strptime(dateList[kwargs['date']], "%Y-%m-%d")
    except ValueError:
        warning_function("Warning", "Invalid Date!", 0)
        return 
    
    if not os.access(path, os.W_OK):
        warning_function("Warning",
            "Output path is not writable! Client valuation not generated!", 0)
        return 

    if trade_numbers != NO_TRADE_FILTER and trade_filter != '':
        warning_function("Warning",
            "Invalid Parameters (trade filter and trade number)! Client valuation not generated!", 0)
        return
    
    print ('Loading...')
    
    # Validate user input
    if trade_numbers == NO_TRADE_FILTER and trade_filter != '':
        tf = acm.FTradeSelection[trade_filter]
        if tf:
            trades = acm.FTradeSelection[trade_filter].Trades()
        else:
            warning_function("Warning",
                "Invalid TradeFilter! Client valuation not generated!", 0)
            return 
    
    elif trade_numbers != NO_TRADE_FILTER and trade_filter == '':
        try:
            trades = map(lambda t: acm.FTrade[int(t)], trade_numbers.split(','))
        except ValueError:
            warning_function("Warning",
                "Invalid Trade provided! Client valuation not generated!\
                 (Trade numbers have to be delimited by ',')", 0)
            return 
    
    elif trade_numbers == NO_TRADE_FILTER and trade_filter == '':
            warning_function("Warning",
                "No Trades provided! Client valuation not generated!", 0)
            return 
  
    trade_list = []
    for trade in trades:
        print(trade.Instrument().ExpiryDateOnly())
        if trade.Instrument().ExpiryDateOnly() > date.strftime("%Y-%m-%d"):
            trade_list.append(trade)
   
    if len(trade_list) > 0:
        # All Trades should belong to ONE Counterparty only, hence
        # we can use any trade to pick-up client name
        counterparty = trade_list[0].Counterparty()
        if not _similar_counter_parties(trade_list):
            warning_function("Warning", "The report contains more than one counterparty.\
             The report will use the first one!", 0)
        file_path = _build_valuation(counterparty, date, trade_list, path, file_format)
        os.startfile(file_path)
    else:
        warning_function("Warning", "No Trades found for client valuation!", 0)
        return
    
    
    print ("Wrote secondary output to {0}".format(file_path))
    print ("completed successfully")

    os.startfile(path)
