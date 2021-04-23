"""
HISTORY
================================================================================================================
Requester            Developer             CR number               Description
----------------------------------------------------------------------------------------------------------------
Sean Lang           Kevin Kistan           C###### (2014-06-30)    Commodity Swap Client Valuation
Angelique Macnabe   Andreas Bayer          20150804                ABITFA-3376 mtm currency conversion
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
from datetime import *
from at_time import is_banking_day
from math import isnan

factor = {
    'USD/UD10CCN_PLATTS/FWD': [1183.4319527, "Litres"],
    'USD/GASOIL_ICE/FWD': [1183.4319527, "Litres"],
}

#user request to explicitly rename products in the product field to remove the exchange from there:
rename_list = {
    'USD/UD10CCN_PLATTS/FWD': 'UD10CCN',
    'USD/PLATINUM_NYMEX/FWD': 'Platinum',
    'USD/BRENT_CRUDE_ICE/FWD': 'Crude',
    'USD/ICE_GASOIL/FWD': 'Gasoil',
    'USD/GOLD_COMEX/FWD': 'Gold',
    'USD/GO05CFS/FWD': 'HSFO 180 Cargoes FOB SGP',
    'USD/JET_KEROCFS_Platts/FWD':'JET_KEROCFS',
    'USD/COPPER_LME/FWD':'Copper',
    'USD/JET_CCN_Platts/FWD':'JET_Platts',
    'USD/ALUMINIUM_LME/FWD':'Aluminium',
    'USD/HSFO180Cargoes_PLATTS/FWD':'HSFO 180 Cargoes FOB SGP',
    'USD/COAL_API4_NYMEX/FWD': 'Coal_API4',
    'USD/PALLADIUM_NYMEX/FWD': 'Palladium',
    'USD/SILVER_COMEX/FWD': 'Silver',
    'USD/GO500PPMCFS/FWD': 'Gasoil',
    'USD/GASOIL_ICE/FWD': 'Gasoil',
    'USD/TIN_LME/FWD':'Aluminium',
    'USD/ZINC_LME/FWD': 'Zinc',
    'USD/LEAD_LME/FWD': 'Lead',
    'USD/WTI_NYMEX/FWD': 'Crude',
    'USD/NICKEL_LME/FWD': 'Nickel'
}

from FReportSettings import XSLT_PATH
from XMLReport import XMLReportGenerator, CSVReportGenerator, StatementReportBase, SummaryRow
from XMLReport import contact_from_pty, mkinfo, mktable, mkcaption, mkdisclaimer
from zak_funcs import formnum
from OPS_Pre_Confirmation import money_flow_value
from xml.etree import ElementTree as ET

def trunc(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    slen = len('%.*f' % (n, f))
    return str(f)[:slen]
    
class Report(StatementReportBase):

    def __init__(self, cpty, date, trade_list, mtm_ccy):
        self.mtm_ccy = mtm_ccy
        self.cpty = cpty
        self.date = date
        self.trade_list = trade_list
        
        self.columns = [{ 'name': 'Trade Number' },
                        { 'name': 'Trade Date' },
                        { 'name': 'Start Date' },
                        { 'name': 'Maturity' },
                        { 'name': 'Volume' },
                        { 'name': 'Product' },
                        #{ 'name': 'Buy/Sell' },
                        { 'name': 'Fixed Price' },
                        { 'name': 'Forward Price' },
                        { 'name': 'Discount Factor' },
                        #{ 'name': 'Spot Rate'},
                        { 'name': 'Quotation'},
                        { 'name': 'Currency'},
                        { 'name': 'MTM'}]
        
        self.spot_price_columns = [
            { 'name': 'Instrument' }, 
            { 'name': 'Quotation' }, 
            { 'name': 'Spot Price' },
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
    
    def get_base_curve(self, trade):
        CONTEXT = acm.GetDefaultContext()
        SHEET_TYPE = 'FPortfolioSheet'
        CALC_SPACE = acm.Calculations().CreateCalculationSpace(CONTEXT, SHEET_TYPE)
        PRICE_CURVE = 'BasePriceCurveInTheoreticalValue'
        top_node = CALC_SPACE.InsertItem(trade)
        CALC_SPACE.Refresh()
        base_curve = CALC_SPACE.CreateCalculation(top_node, PRICE_CURVE).Value()
        
        return base_curve
        
    def get_product(self, trade):
        float_leg = trade.Instrument().FirstFloatLeg()
        price_ref = float_leg.FloatPriceReference()
        product_name = ''
        #if price_ref:
        #    if hasattr(price_ref.AdditionalInfo(), 'Commodity_Deli'):
        #        product_name = price_ref.AdditionalInfo().Commodity_Deli()
        
        if not product_name:
            CONTEXT = acm.GetDefaultContext()
            SHEET_TYPE = 'FPortfolioSheet'
            CALC_SPACE = acm.Calculations().CreateCalculationSpace(CONTEXT, SHEET_TYPE)
            PRICE_CURVE = 'BasePriceCurveInTheoreticalValue'
            product_name = ''
            top_node = CALC_SPACE.InsertItem(trade)
            CALC_SPACE.Refresh()
            base_curve = CALC_SPACE.CreateCalculation(top_node, PRICE_CURVE).Value()
            
            if base_curve:
                try:
                    if base_curve.IsHistorical():
                        base_curve = base_curve.OriginalCurve()
                    product_name = rename_list[base_curve.Name()]
                #    first_benchmark = base_curve.Benchmarks().At(0).Instrument()
                #    if hasattr(first_benchmark.Underlying().AdditionalInfo(), 'Commodity_Deli'):
                #        product_name = first_benchmark.Underlying().AdditionalInfo().Commodity_Deli()
                #    if not product_name:
                #        product_name = first_benchmark.Underlying().Name()
                except Exception, e:
                    product_name = base_curve.Name()
        
        
        return product_name
    
    def get_spot_instrument(self, trade):
        CONTEXT = acm.GetDefaultContext()
        SHEET_TYPE = 'FPortfolioSheet'
        CALC_SPACE = acm.Calculations().CreateCalculationSpace(CONTEXT, SHEET_TYPE)
        PRICE_CURVE = 'BasePriceCurveInTheoreticalValue'
        product_name = None
        top_node = CALC_SPACE.InsertItem(trade)
        CALC_SPACE.Refresh()
        base_curve = CALC_SPACE.CreateCalculation(top_node, PRICE_CURVE).Value()
        print (trade.Oid())
        commodity_name = ''
        
        if base_curve:
            try:
                if base_curve.IsHistorical():
                    base_curve = base_curve.OriginalCurve()
                commodity_name = rename_list[base_curve.Name()]
            except Exception, e:
                commodity_name = base_curve.Name()
            first_benchmark = base_curve.Benchmarks().At(0).Instrument()
            product = first_benchmark.Underlying()

        return product, commodity_name
    
    def generate_spot_price_data(self):
        data = []
        price_refs = set()

        for t in self.trade_list:
            price_refs.add(self.get_spot_instrument(t))
        
        usd_zar = acm.FX().CreateFxRate('USD', 'ZAR')
        price_refs.add((usd_zar, 'USD/ZAR'))
        price_refs = sorted(list(price_refs), key=lambda e: e[0].Name())
        for price_ref in price_refs:
            commodity_name = price_ref[1]
            price_ref = price_ref[0]
            spot_price = price_ref.Calculation().MarketPrice(self.std_calc_space)
            if isnan(spot_price.Number()):
                spot_price = price_ref.Calculation().MarkToMarketPrice(self.std_calc_space, acm.Time().DateToday(), price_ref.Currency())
            
            spot_name = price_ref.Name()
            if hasattr(price_ref.AdditionalInfo(), 'Commodity_Deli') and price_ref.AdditionalInfo().Commodity_Deli():
                spot_name = price_ref.AdditionalInfo().Commodity_Deli()
            if price_ref.InsType() == 'Fx Rate':
                data.append([
                spot_name,
                price_ref.Quotation().Name(),
                formnum(spot_price.Number()),
                ''])
            else:
                data.append([
                    commodity_name,
                    price_ref.Quotation().Name(),
                    formnum(spot_price.Number()),
                    spot_price.Unit()])
        return data
    
    def generate_data(self):
        data = []
        date = self.date.strftime("%Y-%m-%d")
        total_mtm = 0.0
                
        for t in self.trade_list:
            ins = t.Instrument()
            ins_name = t.Instrument().Name()
            legs = ins.Legs()
                                   
            #Product Name
            product = self.get_product(t)
            
            #Quantity
            #Calculate total average and weighted average
            total_cf_nominal = []
            for cf in ins.FirstFixedLeg().CashFlows():
                nominal = (cf.NominalFactor() * t.Quantity() * ins.ContractSize()) 
                value = nominal
                if cf.EndDate() >= acm.Time().DateToday():
                    total_cf_nominal +=[value]
                
            total_quantity = sum(total_cf_nominal)
            
            #Weighted Average Quantity
            quantity = sum(total_cf_nominal) / len(total_cf_nominal)
            base_curve = self.get_base_curve(t)
            if base_curve.IsHistorical():
                base_curve = base_curve.OriginalCurve()
            if base_curve and base_curve.Name() in factor:
                quantity = quantity * factor[base_curve.Name()][0]
                quantity = formnum(quantity) if quantity > 0 else '(%s)' % formnum(abs(quantity))
            else:
                quantity = formnum(quantity) if quantity > 0 else '(%s)' % formnum(abs(quantity))
                        
            
            #ABSA Buy Sell
            buy_sell = buy_sell = 'buy' if t.Quantity() > 0 else 'sell'
            
            #Maturity Date. BU requested the end date and not the expiry date.
            exp_date = ins.LongestLeg().EndDate()                                        
                            
            #Calculate weighted average Fixed Price
            fixed_prices = []
            for cf in ins.FirstFixedLeg().CashFlows():
                value = acm.GetCalculatedValueFromString(cf, acm.GetDefaultContext(), 'hybridPrice', None).Value()
                if cf.EndDate() >= acm.Time().DateToday():
                    nominal = (cf.NominalFactor() * t.Quantity() * ins.ContractSize()) 
                    wavg_fixed_price = (value * nominal)
                    fixed_prices += [wavg_fixed_price]
      

            total_fixed_prices = sum(fixed_prices)
                    
            fixed_price = (total_fixed_prices / total_quantity)
            if base_curve.IsHistorical():
                base_curve = base_curve.OriginalCurve()
            if base_curve and base_curve.Name() in factor:
                fixed_price = fixed_price / factor[base_curve.Name()][0]
                fixed_price = formnum(fixed_price) if (fixed_price > 0) else '(%s)' % formnum(abs(fixed_price))
            else:
                fixed_price = formnum(fixed_price) if (fixed_price > 0) else '(%s)' % formnum(abs(fixed_price))
            
            #Calculate weighted average Forward Price
            forward_prices = [] 
            for cf in ins.FirstFloatLeg().CashFlows():
                value = acm.GetCalculatedValueFromString(cf, acm.GetDefaultContext(), 'hybridPrice', None).Value()
                if cf.EndDate() >= acm.Time().DateToday():
                    nominal = (cf.NominalFactor() * t.Quantity() * ins.ContractSize()) 
                    wavg_forward_price = (value * nominal)
                    forward_prices += [wavg_forward_price]

            total_forward_prices = sum(forward_prices)

            forward_price = (total_forward_prices / total_quantity)
            if base_curve.IsHistorical():
                base_curve = base_curve.OriginalCurve()
            if base_curve and base_curve.Name() in factor:
                forward_price = forward_price / factor[base_curve.Name()][0]
                forward_price = formnum(forward_price) if (forward_price > 0) else '(%s)' % formnum(abs(forward_price))
            else:
                forward_price = formnum(forward_price) if (forward_price > 0) else '(%s)' % formnum(abs(forward_price))

            
            #Calculate weighted average Discount Factor
            disc_factors = []
            for cf in t.Instrument().Legs()[0].CashFlows():
                value = cf.Calculation().DiscountFactor(self.std_calc_space, t)
                if cf.EndDate() >= acm.Time().DateToday():
                    nominal = (cf.NominalFactor() * t.Quantity() * ins.ContractSize()) 
                    wavg_disc_factor = (value * nominal)
                    disc_factors += [wavg_disc_factor]

            total_disc_factor = sum(disc_factors)
            
            discount_factor = trunc((total_disc_factor / total_quantity), 4)
            
                
                 
            #Start Date, BU requested that the 1st date of the next month be used as the start date
            start_date = ins.StartDate()
            if ael.date_from_string(start_date) != (ael.date_from_string(start_date).first_day_of_month()):
                start_date = acm.Time().AsDate(ael.date_from_string(start_date).first_day_of_month().add_months(1))
                
            #Calculate the Spot price for Metals only Platinum, Gold and Palladium
            floatLegs = [l for l in ins.Legs() if l.LegType() == 'Float']
            spot_rate = floatLegs[0].FloatRateReference().Calculation().TheoreticalPrice(self.std_calc_space)
            spot_rate = formnum(spot_rate.Number()) if spot_rate else ''
                                    
            #Trade Currency
            trade_curr = t.Currency().Name()
            
            #Quotation
            #quotation = t.Instrument().Quotation().Name()
            if base_curve.IsHistorical():
                base_curve = base_curve.OriginalCurve()
            if base_curve and base_curve.Name() in factor:
                quotation = factor[base_curve.Name()][1]
            else:
                quotation = t.Instrument().Quotation().Name()
                        
            
            #MTM, Total Val End
            try: 
                calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
                calc_space.SimulateValue(t, 'Portfolio Currency', self.mtm_ccy)
                calc = calc_space.CalculateValue(t, 'Total Val End')
                mark_to_market = round(calc.Value().Number(), 2)
                calc_space.RemoveSimulation(t, 'Portfolio Currency')
            except Exception, e:
                calc_space.RemoveSimulation(t, 'Portfolio Currency')
                mark_to_market = 0.0
                
            # calculate total_mtm
            total_mtm += mark_to_market
            data.append([
                t.Oid(),
                at.date_to_ymd_string(t.TradeTime()),
                start_date,
                exp_date,
                quantity,
                product,
                #buy_sell,
                fixed_price,
                forward_price,
                discount_factor,
                #spot_rate,
                quotation,
                trade_curr,                
                formnum(mark_to_market) if (mark_to_market > 0) else '(%s)' % formnum(abs(mark_to_market)),
            ])
        
        # Summary for MTM
        l = SummaryRow(['' for i in range(12)])
        l[0] = "TOTAL MTM in"#{0}".format(self.mtm_ccy)
        l[1] = self.mtm_ccy.Name()
        l[11] = formnum(total_mtm) if (total_mtm > 0) else "({0})".format(formnum(abs(total_mtm)))
        data.append(l)
        
        return data


def BuildValuation(ctpy, date, trade_list, output_dir, file_format, mtm_ccy):
    """Function generate PDF confirmation"""    
    if (str(acm.Class()) != "FTmServer" and 
            acm.User().UserGroup().Name() in ('Integration Process', 'System Processes')):
                output_dir = "//nfs/fa/reports/EMEA/prod/FAReports/PCGClientValuations/Valuations/"
    
    filename = "Commodity_Swap_Client_Valuation-{0}-{1}".format(
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
    ['mtm_ccy', 'MTM Currency:', 'string',        sorted([c.Name() for c in acm.FCurrency.Select("")]), 'ZAR'],
    ['format', 'Output Format:', 'string', ['PDF', 'Excel'], 'PDF'],
    ['path', 'Output Folder:', 'string', None,
        r'Y:\Jhb\Arena\Data\PCG-Client-Valuations\Commodity Valuations', 1],
]

def get_last_cash_flow_end_adjusted(i, calendars):
    cfs = []
    for leg in i.Legs():
        for cf in leg.CashFlows():
            cfs.append(cf)
    cfs = sorted(cfs, key=lambda e: e.EndDate())
    end_date = cfs[-1].EndDate()
    for calendar in calendars:
        if not is_banking_day(calendar, end_date):
            end_date = calendar.AdjustBankingDays(end_date, -1)
    return end_date

def ael_main(kwargs):
    """Main loop"""
    
    SKIP_INSTYPES = kwargs['skip_instypes']
    SKIP_INSTYPES = SKIP_INSTYPES.split(",")
    FILE_OUTPUT = {'Excel': 'csv', 'PDF': 'xml'}
    
    file_format = FILE_OUTPUT[kwargs['format']]
    trade_numbers = kwargs['trdnbr']
    trade_filter = kwargs['tf']
    mtm_ccy = acm.FCurrency[kwargs['mtm_ccy']]
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
        if 'COMM' in trade_filter:
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
                i = trade.Instrument()
                float_leg=i.FirstFloatLeg()
                calendars = []
                if float_leg.PayCalendar():
                    calendars.append(float_leg.PayCalendar())
                if float_leg.Pay2Calendar():
                    calendars.append(float_leg.Pay2Calendar())
                if float_leg.Pay3Calendar():
                    calendars.append(float_leg.Pay3Calendar())
                if float_leg.Pay4Calendar():
                    calendars.append(float_leg.Pay4Calendar())
                if float_leg.Pay5Calendar():
                    calendars.append(float_leg.Pay5Calendar())
                
                end_date = get_last_cash_flow_end_adjusted(i, calendars)
                if end_date > acm.Time().DateToday():
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
