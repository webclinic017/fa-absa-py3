"""
DAILY : Detailed Ccy (Non Zar) cashflow report for all Front portfolios (Higher level would be fine)

Value date = Today for the T0 report and for the T+1 report = Yesterday
I need the trade level detail of all Non Zar cash legs in Front
Trade number, product, Value date, ccy cash amount, ZAR cash amount, portfolio
All portfolio's : PCG, Group, Spec fin
Only the 1 days'cashflows
Existing report that needs to be amended to include all portfolios

Include backdated, amended and voided non Zar cashflows.
list of all amendeded cashflows < Today for T0 and < Yesterday for T+1 rec
Have a look at the existing ZAR report?

Date              JIRA               Developer               Reporter
==========        ====               ====================    ====================== 
2012-12-07        ABITFA-1517        Pavel Saparov            Marisa Serfontein
2013-02-23        ABITFA-2027        Pavel Saparov            Thabo Moodie
2013-07-23        ABITFA-2144        Andrei Conicov           Thabo Moodie
2013-11-29        ABUGFIX-N/A        Peter Fabian & Jan Sinkora Thabo Moodie
"""
# import stdlibs 
import csv
from collections import namedtuple

# import arena libs
import acm
import FRunScriptGUI

# CSV columns in report file
DAILY_REPORT_COLUMNS = (
    'ReportDate', 'TrdStatus', 'TrdNumber', 'TrdCurrency', 'Portfolio',
    'Counterparty', 'Acquirer', 'Instrument', 'InsExpiry', 'InsType',
    'PayDate', 'PayReceive', 'CFType', 'CFCurrency', 'Nominal',
    'Projected', 'ZARNominal', 'ZARProjected' 
)
acm_time = acm.Time()
TODAY = acm_time.DateToday()
DailyReport = namedtuple('DailyReport', DAILY_REPORT_COLUMNS)


class PCGNonZARRunScript(FRunScriptGUI.AelVariablesHandler):
    """FRunScriptGUI class defining GUI parameters."""
    
    output_dir = FRunScriptGUI.DirectorySelection()
    
    start_dates = {
       'Today': TODAY,
       'Previous Business Day': acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(TODAY, -1),
       'Yesterday': acm_time.DateAddDelta(TODAY, 0, 0, -1),
       'Two Days Ago':  acm_time.DateAddDelta(TODAY, 0, 0, -2),
       'First Day of the Week': acm_time.FirstDayOfWeek(TODAY),
       'First Day of the Month': acm_time.FirstDayOfMonth(TODAY),
       'Custom Date': TODAY
    }
    
    def custom_start_date(self, index, fieldValues):
        """Input hook for ael_variables"""
        self.dateCustom.enable((fieldValues[0] == 'Custom Date'))
        return fieldValues
     
    def __init__(self):
        ael_vars = [
            ['date', 'Date', 'string', self.start_dates.keys(), 'Previous Business Day', 1, 0, 'Date for witch the file should be selected.', self.custom_start_date, 1],
            ['dateCustom', 'Date Custom', 'string', None, TODAY, 0, 0, 'Custom date', None, 0],
            ['compoundPortfolios', 'Compound Portfolios', 'FCompoundPortfolio', None, 'ABSA CAPITAL', 1, 1, 'Compound Portfolios', None, 1],
            ['exclude_mftypes', 'Exclude Cashflow Types', 'string', None, None, 0, 0, 'Will exclude ZAR instruments from the report', None, 1],
            ['currency', 'Report Cashflow Currencies', 'FCurrency', None, '', 1, 1, 'Cashflow currency that will be included in the report', None, 1],
            ['not_curr', 'Exclude Report Currencies', 'int', [0, 1], None, 0, 0, 'Negate previous currency statement selection', None, 1],
            ['exclude_zar', 'Exclude ZAR instruments', 'int', [0, 1], None, 0, 0, 'Will exclude ZAR instruments from the report', None, 1],
            ['daily_report', 'Daily Report Filename', 'string', None, '/services/frontnt/Task/PCG_NonZAR_CashRecon.csv', 1, 0, 'Output filename for daily report', None, 1],
            ['summary_report', 'Summary Report Filename', 'string', None, '/services/frontnt/Task/PCG_NonZAR_CashSummary.csv', 1, 0, 'Output filename for daily total cashflow report', None, 1],
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, ael_vars)


def fx_rate(from_currency, to_currency, date):
    """Obtains FX rate for a certain date.
    
    Arguments:
    from_currency -- str, eg. USD
    to_currency -- str, egk. ZAR
    date -- str, eg. 2012-10-10
    
    """

    if (from_currency, to_currency, date) not in fx_rate._ccy_cache.keys():
        calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        from_curr = acm.FCurrency[from_currency]
        to_curr = acm.FCurrency[to_currency]
        fx_rate._ccy_cache[(from_currency, to_currency, date)] = from_curr.Calculation().FXRate(
            calc_space, to_curr, date).Number()
    
    return fx_rate._ccy_cache[(from_currency, to_currency, date)]

fx_rate._ccy_cache = {}

def create_named_param(vector, currency):
    """Simple function that add FNamedParameters
    to passed vector.
    
    Arguments:
    vector - list
    currency - FCurrency
    """
    param = acm.FNamedParameters()
    param.Name(currency.Name())
    param.UniqueTag(currency.Oid())
    param.AddParameter('currency', currency)
    vector.append(param)

def _get_trades(portfolio, exclude_zar, report_date):
    """
    Return the list of trades for the specified portfolio and the report date.
    Creates the corresponding ASQL query and executes it.
    """
    # Select all Trades except Simulated and Terminated within physical portfolio
    # TODO: Move query below into QueryFolder
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')

    op = query.AddOpNode('AND')
    op.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
    
    op = query.AddOpNode('AND')
    op.AddAttrNode('Counterparty.Name', 'NOT_EQUAL', 'MIDAS DUAL KEY')
    
    op = query.AddOpNode('AND')
    op.AddAttrNode('Instrument.Currency.Name', 'EQUAL', 'ZAR')
    
    # Pavel confirmed that have to use op
    orNode = op.AddOpNode('OR')
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'Stock'))
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'Future/Forward'))
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'Bond'))
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'FRN'))
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'Repo/Reverse'))
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'SecurityLoan'))
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'CFD'))
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'Swap'))

    # Excluding ZAR instruments
    if exclude_zar:
        op.Not(True)

    op = query.AddOpNode('AND')
    op.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Simulated'))
    op.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Void'))
    
    op = query.AddOpNode('AND')
    query.AddAttrNode('ValueDay', 'LESS_EQUAL', report_date)
    
    return query.Select()

# Define variables for `ael_variables` used in GUI

def _init_trade_data(trade, report_date):
    """
    Initialises trade information, that has to be output.
    Returns a dictionary with the initialised values.
    """
    data = {}
    data['ReportDate'] = report_date
    data['TrdNumber'] = trade.Oid()
    data['TrdStatus'] = trade.Status()
    data['TrdCurrency'] = trade.Currency().Name()
    data['Portfolio'] = trade.PortfolioId()
    data['Counterparty'] = trade.CounterpartyId()
    data['Acquirer'] = trade.AcquirerId()
    data['Instrument'] = trade.Instrument().Name()
    data['InsExpiry'] = trade.Instrument().ExpiryDate()
    data['InsType'] = trade.Instrument().InsType()
    
    return data

def _init_money_flow_data(data, money_flow, mf_calc_space):
    """
    Initialises money flow and fx rate information, 
    that has to be output.
    Returns a dictionary with the initialised values.
    """
    data['PayDate'] = money_flow.PayDate()
    data['CFType'] = money_flow.Type()
    data['CFCurrency'] = money_flow.Currency().Name()
    data['Nominal'] = mf_calc_space.CalculateValue(money_flow, 'Cash Analysis Event Face Value', None, False)
    data['Projected'] = mf_calc_space.CalculateValue(money_flow, 'Cash Analysis Projected Custom', None, False)
    if hasattr(data['Projected'], "Number"):
        data['Projected'] = data['Projected'].Number()
    data['PayReceive'] = 'Receive' if data['Projected'] > 0 else 'Pay'
    data['ZARNominal'] = fx_rate(data['CFCurrency'], 'ZAR', data['ReportDate']) * data['Nominal']
    data['ZARProjected'] = fx_rate(data['CFCurrency'], 'ZAR', data['ReportDate']) * data['Projected']

    return data

ael_gui_parameters = {
  'windowCaption' : 'PCG Non-ZAR Cashflows Recon'
}

ael_variables = PCGNonZARRunScript()


def ael_main(kwargs):
    """Main function"""
    
    acm.Log("Starting {0}".format(__name__))
    
    # Get report date
    report_date = PCGNonZARRunScript.start_dates[kwargs['date']]
    if kwargs['date'] == 'Custom Date':
        report_date = kwargs['dateCustom']
    
    # Prepare CSV writers
    with open(kwargs['daily_report'], 'wb') as csv_writer_f:
        csv_writer = csv.writer(csv_writer_f)
        csv_writer.writerow(DAILY_REPORT_COLUMNS)
        
        # Obtain all physical portfolios within compound portfolios
        portfolios = sum([list(cp.AllPhysicalPortfolios()) for cp in kwargs['compoundPortfolios']], [])

        # For each physical portfolios, obtain it's trade, for those trades
        if  kwargs['not_curr']:
            f_use_mf_by_curr = lambda currency: currency not in kwargs['currency']
        else:
            f_use_mf_by_curr = lambda currency: currency in kwargs['currency']
        
        # Obtain currencies to prepare vector for vector calculations
        currencies = []
        for ccy in acm.FCurrency.Select(""):
            if (f_use_mf_by_curr(ccy) and len(ccy.Name()) == 3):
                currencies.append(ccy)
        
        currencies = sorted(currencies, key=lambda ccy: ccy.Name())
        currencies_code_list = [ccy.Name() for ccy in currencies]
        
        # ``rowdicts_header`` is united set of all defaultdict keys
        # ``rowdicts`` is list of defaultdicts containing data for output
        rowdicts_header, rowdicts = ['TrdNumber', 'Portfolio'] + currencies_code_list, []
        
        portfolio_counter = len(portfolios)

            
        for portfolio in portfolios:
            trades = _get_trades(portfolio, kwargs['exclude_zar'], report_date)
            
            # Prepare calculation spaces
            context = acm.GetDefaultContext()
            mf_calc_space = acm.Calculations().CreateCalculationSpace(context, 'FMoneyFlowSheet')
            pf_calc_space = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')
            
            # Set the P&L date
            mf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
            mf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', report_date)
            pf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
            pf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', report_date)
            
            vector = [] #acm.FArray()
            for currency in currencies:
                create_named_param(vector, currency)
            
            cash_per_currency = acm.Sheet.Column().ConfigurationFromVector(vector)
            
            
            acm.Log("Processing {0} trades in {1} portfolio. {2} portfolio remaining".format(len(trades), portfolio.Name(), portfolio_counter))
            portfolio_counter -= 1
            for trade in trades:
                # Obtain related Money Flow objects; very complex -- no other way
                for money_flow in trade.MoneyFlows(report_date, report_date):
                    if (money_flow.Type() not in kwargs['exclude_mftypes'] 
                        and f_use_mf_by_curr(money_flow.Currency())):
                        # The if is evaluated to true very rarely
                        # otherwise it would be more effective to call 
                        # _init_trade_data before iterating the money flows
                        data = _init_trade_data(trade, report_date)
                        data = _init_money_flow_data(data, money_flow, mf_calc_space)
                        csv_writer.writerow(DailyReport(**data))
     
                # Calculate Cash Per Currency and store calculation in ``data`` dictionary
                cpc_vector = pf_calc_space.CreateCalculation(trade, 'Portfolio Cash Vector', cash_per_currency).Value()
                cpc_vector = [value.Number() for value in cpc_vector]
                abs_vector = [abs(number) for number in cpc_vector]
                 
                if sum(abs_vector) > 0:
                    data = dict(list(zip(currencies_code_list, cpc_vector)))
                    data['TrdNumber'] = trade.Oid()
                    data['Portfolio'] = portfolio.Name()
                    rowdicts.append(data)
                
            # Clear calculations
            mf_calc_space.Clear()
            pf_calc_space.Clear()
        
    with open(kwargs['summary_report'], 'wb') as dict_writer_f:
        dict_writer = csv.DictWriter(dict_writer_f, rowdicts_header)
        dict_writer.writerow(dict(list(zip(rowdicts_header, rowdicts_header))))
        dict_writer.writerows(rowdicts)

    
    acm.Log("Wrote secondary output to {0}".format(kwargs['daily_report']))
    acm.Log("Wrote secondary output to {0}".format(kwargs['summary_report']))
    acm.Log("Completed successfully")
