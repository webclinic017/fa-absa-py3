import acm
import FLogger
import os.path
import csv
import math
import traceback, sys
from at_time import to_datetime, to_date, acm_date, add_months
from at_ael_variables import AelVariableHandler
from collections import defaultdict, namedtuple
from PLExplainExtensions import *
from RiskFactorExtensions import *
from interestRateSpreadDeltaCurveBucketsShift import *

REPORT_ENTRY = namedtuple('risk_service_report_entry', [
    'Trade_Number',
    'Instrument_Name',
    'Instrument_Type',
    'Trade_Process',
    'Instrument_Expiry',
    'Value_Day',
    'Portfolio_Name',
    'Chorus_Id',
    'Counterparty_Name',
    'BarCap_SMS_CP_SDSID',
    'BarCap_SMS_LE_SDSID',
    'Risk_Factor',
    'Risk_Factor_Type',
    'Risk_Factor_Currency',
    'Risk_Factor_Element',
    'Risk_Factor_Element_Type',
    'Risk_Type',
    'Currency',
    'Risk_Factor_Description',
    'Risk_Value',
    'Risk_Factor_Element_Maturity',
    'Global_Context',
    'Org_Context',
    'User_Context',
    'Group_Context',
    'Workspace_Context'
])

'''
select c.name, pm.override_level, pm.workspace_name, display_id(pm, 'usrnbr'), display_id(pm, 'grpnbr'), display_id(pm, 'orgnbr')
from
    ParMappingInstance pmi,
    ParameterMapping pm,
    Context c

Where pmi.context_seqnbr = c.seqnbr
and pmi.mapping_seqnbr = pm.seqnbr
and pmi.parameter_type = 'Context Par'
'''

global_mapping = ''
org_mapping = ''
user_mapping = ''
workspace_mapping = ''
group_mapping = ''

'''
whereClause = "overrideLevel='Global'"
global_mapping = acm.FParameterMapping.Select01(whereClause, '')

whereClause = "overrideLevel='Organisation' organisation='%s'" % (acm.Organisation().Name())
org_mapping = acm.FParameterMapping.Select01(whereClause, '')

whereClause = "overrideLevel='Group' userGroup='%s'" % (acm.User().UserGroup().Name())
group_mapping = acm.FParameterMapping.Select01(whereClause, '')
#group_mapping = group_mapping.Size() > 0 and group_mapping.At(0) and None

whereClause = "overrideLevel='User' user='%s'" % (acm.User().Name())
user_mapping = acm.FParameterMapping.Select01(whereClause, '')
#user_mapping = user_mapping.Size() > 0 and user_mapping.At(0) and None

#whereClause = "user='%s' overrideLevel='Workspace' workspaceName='%s'" % (acm.User().Name(), acm.FWorkspace['Simulated_Cosic'])
whereClause = "user='%s' overrideLevel='Workspace' workspaceName='%s'" % (acm.User().Name(), acm.ActiveWorkspace())
workspace_mapping = acm.FParameterMapping.Select01(whereClause, '')

if global_mapping:
    for i in global_mapping.ParMappingInstances():
        if i.ParameterType() == 'Context Par':
            global_mapping = i.Context().Name()
            break
else:
    global_mapping = ''

if org_mapping:
    for i in org_mapping.ParMappingInstances():
        if i.ParameterType() == 'Context Par':
            org_mapping = i.Context().Name()
            break
else:
    org_mapping = ''

if group_mapping:
    group_mapping = ''
    #for i in group_mapping.ParMappingInstances():
    #    if i.ParameterType() == 'Context Par':
    #        group_mapping = i.Context().Name()
    #        break
else:
    group_mapping = ''

if user_mapping:
    
    for i in user_mapping.ParMappingInstances():
        if i.ParameterType() == 'Context Par':
            user_mapping = i.Context().Name()
            
            break
        else:
            user_mapping = ''
else:
    user_mapping = ''

if workspace_mapping:
    workspace_mapping = ''
    #for i in workspace_mapping.ParMappingInstances():
    #    if i.ParameterType() == 'Context Par':
    #        workspace_mapping = i.Context().Name()
    #        break
else:
    workspace_mapping = ''
    
'''

ael_gui_parameters = {
    'windowCaption' : 'Risk Service'
}

ael_variables = AelVariableHandler()

ael_variables.add(
    'trade_selection', 
    label = 'Trade Query', 
    cls = acm.FTrade, 
    multiple = True,
    default = '?BAY_RiskService',
)

ael_variables.add(
    'out_file',
    label = 'Output File',
    cls = 'string',
    default = r'C:\temp\Commodity_Price_Delta.csv'
)

CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), acm.FTradeSheet)
CALC_SPACE_PORTFOLIO = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), acm.FPortfolioSheet)
DOMESTIC_CURRENCY = acm.FCurrency['ZAR']

def currency_exposure(trade):
    CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), acm.FTradeSheet)
    column = 'TheoreticalTotalProfitLossCurrencies'
    currencies = CALC_SPACE.CreateCalculation(trade, column).Value()
    idx = currencies.IndexOf(DOMESTIC_CURRENCY)
    if idx >= 0:
        del currencies[idx]
        
    return currencies
    
class Calculation_Environment(object):
    def __init__(self):
        self.CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), acm.FTradeSheet)
    
    def get_calculation_environment(self):
        return self.CALC_SPACE

#creates a time bucket structure
def create_timebuckets(bucket_lables, add_rest_bucket):
    today = acm.Time().DateToday()
    buckets_definition =[]
    for label in bucket_lables:
        bucket_definition = acm.FDatePeriodTimeBucketDefinition()
        bucket_definition.DatePeriod(label)
        buckets_definition.append(bucket_definition)
    if add_rest_bucket:
        buckets_definition.append(acm.FRestTimeBucketDefinition())
        
    definition = acm.TimeBuckets().CreateTimeBucketsDefinition(today,
    buckets_definition, False, False, False, False, False)
    def_and_conf = acm.TimeBuckets().CreateTimeBucketsDefinitionAndConfiguration(definition)
    return acm.TimeBuckets().CreateTimeBuckets(def_and_conf)
    
def mapped_price_curve(trade):
    '''get name of mapped price curve'''
    SHEET_TYPE = 'FTradeSheet'
    CALC_SPACE = acm.Calculations().CreateCalculationSpace('Commodities', SHEET_TYPE)
    PRICE_CURVE = 'BasePriceCurveInTheoreticalValue'
        
    top_node = CALC_SPACE.InsertItem(trade)
    CALC_SPACE.Refresh()
    base_curve = CALC_SPACE.CreateCalculation(top_node, PRICE_CURVE)
    return base_curve.Value().Name() if base_curve.Value() else None
    
def mapped_benchmark_curve(trade):
    '''get name of mapped price curve'''
    SHEET_TYPE = 'FTradeSheet'
    CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), SHEET_TYPE)
    BENCHMARK_CURVE = 'BenchmarkCurvesInTheoreticalValue'
        
    top_node = CALC_SPACE.InsertItem(trade)
    CALC_SPACE.Refresh()
    base_curve = CALC_SPACE.CreateCalculation(top_node, BENCHMARK_CURVE)
    return base_curve.Value()
    
def mapped_volatility_structure(trade):
    '''get name of mapped price curve'''
    SHEET_TYPE = 'FTradeSheet'
    CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), SHEET_TYPE)
    BENCHMARK_CURVE = 'TopVolatilityStructuresInTheoreticalValue'
        
    top_node = CALC_SPACE.InsertItem(trade)
    CALC_SPACE.Refresh()
    base_curve = CALC_SPACE.CreateCalculation(top_node, BENCHMARK_CURVE)
    return base_curve.Value() if base_curve.Value() else acm.FList()

def mapped_underlying(trade):
    '''get name of derivative underlying'''
    SHEET_TYPE = 'FTradeSheet'
    CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), SHEET_TYPE)
    BENCHMARK_CURVE = 'Used Underlying'
        
    top_node = CALC_SPACE.InsertItem(trade)
    CALC_SPACE.Refresh()
    base_curve = CALC_SPACE.CreateCalculation(top_node, BENCHMARK_CURVE)
    
    if base_curve.Value():
        if base_curve.Value().IsKindOf(acm.FStock) or base_curve.Value().IsKindOf(acm.FCfd):
            return base_curve.Value()
    return acm.FList()
    
def mapped_spread_curves(trade):
    '''get name of mapped price curve'''
    SHEET_TYPE = 'FTradeSheet'
    CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), SHEET_TYPE)
    BENCHMARK_CURVE = 'AllYieldCurvesIncludingInflationInTheoreticalValue'
        
    top_node = CALC_SPACE.InsertItem(trade)
    CALC_SPACE.Refresh()
    base_curve = CALC_SPACE.CreateCalculation(top_node, BENCHMARK_CURVE)
    l = acm.FList()
    
    for curve in base_curve.Value():
        #print curve.Name(), curve.Type()
        if curve.Type() in ('Spread', 'Instrument Spread', 'Attribute Spread'):
            l.Add(curve)
            
    
    return l

def mapped_credit_curve(trade):
    '''get name of mapped price curve'''
    SHEET_TYPE = 'FTradeSheet'
    CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), SHEET_TYPE)
    BENCHMARK_CURVE = 'Standard Calculations Mapped Credit Curve'
        
    top_node = CALC_SPACE.InsertItem(trade)
    CALC_SPACE.Refresh()
    base_curve = CALC_SPACE.CreateCalculation(top_node, BENCHMARK_CURVE)
    l = acm.FList()
    
    curve = base_curve.Value()
    #print curve.Name(), curve.Type()
    if curve.YieldCurve().Type() == 'Attribute Spread':
        l.Add(curve)
    
    return l
    
class Sensitivity(object):
    def __init__(self, trade, shift_size, risk_factor, calculation):
        self.trade = trade
        self.trdnbr = str(trade.Oid())
        self.instrument = trade.Instrument()
        self.instrument_name = self.instrument.Name()
        self.instrument_type = self.instrument.InsType()
        self.shift_size = shift_size
        self.risk_factor = risk_factor
        self.calculation = calculation
        self.portfolio = trade.Portfolio().Name() if trade.Portfolio() else ''
        self.chorus_id = str(trade.Portfolio().Oid()) if trade.Portfolio() else ''
        self.counterparty_name = trade.Counterparty().Name() if trade.Counterparty() else ''
        self.barCap_SMS_CP_SDSID = trade.Counterparty().AdditionalInfo().BarCap_SMS_CP_SDSID() if trade.Counterparty() else ''
        self.barCap_SMS_LE_SDSID = trade.Counterparty().AdditionalInfo().BarCap_SMS_LE_SDSID() if trade.Counterparty() else ''
        
    def calculate_sensitivity(*args, **kwargs):
        return
    
class Commodity_Benchmark_Delta(Sensitivity):

    def __init__(self, trade, shift_size, risk_factor, calculation):
        super(Commodity_Benchmark_Delta, self).__init__(trade, shift_size, risk_factor, calculation)
        
    def _calculate_benchmark_sensitivity(self, benchmark):
        prices = benchmark.Instrument().Prices()
        pv0 = self.calculation.Value().Number()
        
        for price in prices:
            price.Bid(price.Bid() * self.shift_size)
            price.Ask(price.Ask() * self.shift_size)
            price.Last(price.Last() * self.shift_size)
            price.Settle(price.Settle() * self.shift_size)
            
            price.SimulateRecursive()
        
        pv1 = self.calculation.Value().Number()
        
        for price in prices:
           
            price.Unsimulate()
            
        return pv1 - pv0
        
    def calculate_sensitivity(self):
        sensitivities = []
        
        for benchmark in self.risk_factor.Benchmarks():
            sensitivities.append(REPORT_ENTRY(
                Trade_Number = self.trdnbr,
                Instrument_Name = self.instrument_name,
                Instrument_Type = self.instrument_type,
                Trade_Process = self.trade.TradeProcessesToString(),
                Instrument_Expiry = self.instrument.maturity_date(),
                Value_Day=self.trade.ValueDay(),
                Portfolio_Name = self.portfolio,
                Chorus_Id = self.chorus_id,
                Counterparty_Name = self.counterparty_name,
                BarCap_SMS_CP_SDSID = self.barCap_SMS_CP_SDSID,
                BarCap_SMS_LE_SDSID = self.barCap_SMS_LE_SDSID,
                Risk_Factor = self.risk_factor.Name(),
                Risk_Factor_Type = self.risk_factor.Type(),
                Risk_Factor_Currency = self.risk_factor.Currency().Name(),
                Risk_Factor_Element = benchmark.Instrument().Name(),
                Risk_Factor_Element_Type = 'Benchmark',
                Risk_Type = self.risk_factor.RiskType(),
                Currency = 'ZAR',
                Risk_Factor_Description = '1% Relative Benchmark Price Shift',
                Risk_Value = str(self._calculate_benchmark_sensitivity(benchmark)),
                Risk_Factor_Element_Maturity = benchmark.Instrument().maturity_date(),
                Global_Context = global_mapping,
                Org_Context = org_mapping,
                User_Context = user_mapping,
                Group_Context = group_mapping,
                Workspace_Context = workspace_mapping
            )._asdict())
        return sensitivities

class IR_Benchmark_Delta_Sensitivity(Sensitivity):
    def __init__(self, trade, shift_size, risk_factor, calculation):
        super(IR_Benchmark_Delta_Sensitivity, self).__init__(trade, shift_size, risk_factor, calculation)
        
    def calculate_sensitivity(self):
        sensitivities = []
        COLUMN_ID = 'Benchmark Delta Instruments'
        benchmarks = self.risk_factor.Benchmarks()
        
        instruments = [b.Instrument() for b in benchmarks]
        column_config = acm.Sheet.Column().ConfigurationFromVector(instruments)
        top_node = CALC_SPACE.InsertItem(self.trade)
        calc = CALC_SPACE.CreateCalculation(top_node, COLUMN_ID, column_config)
        
        if self.risk_factor.Name() in ('ZAR-CPI', 'ZAR-CPI-Bond'):
            risk_factor_description = '1bp Absolute Real Rate Shift'
            risk_factor_type = 'Inflation'
        else:
            risk_factor_description = '1bp Absolute Benchmark Price Shift'
            risk_factor_type = self.risk_factor.RiskType()
        idx = 0
        while idx < len(instruments):
            if len(instruments) == 1:
                #print instruments, calc.Value()
                instr = instruments[idx].Name()
                value = calc.Value()
                value_number = value.Number()
            else:
                instr = instruments[idx].Name()
                value = calc.Value()[idx]
                value_number = value.Value().Number()
            
            sensitivities.append(REPORT_ENTRY(
                Trade_Number = self.trdnbr,
                Instrument_Name = self.instrument_name,
                Instrument_Type = self.instrument_type,
                Trade_Process = self.trade.TradeProcessesToString(),
                Instrument_Expiry = self.instrument.maturity_date(),
                Value_Day=self.trade.ValueDay(),
                Portfolio_Name = self.portfolio,
                Chorus_Id = self.chorus_id,
                Counterparty_Name = self.counterparty_name,
                BarCap_SMS_CP_SDSID = self.barCap_SMS_CP_SDSID,
                BarCap_SMS_LE_SDSID = self.barCap_SMS_LE_SDSID,
                Risk_Factor = self.risk_factor.Name(),
                Risk_Factor_Type = self.risk_factor.Type(),
                Risk_Factor_Currency = self.risk_factor.Currency().Name(),
                Risk_Factor_Element = instr,
                Risk_Factor_Element_Type = 'Benchmark',
                Risk_Type = risk_factor_type,
                Currency = 'ZAR',
                Risk_Factor_Description = risk_factor_description,
                Risk_Value = str(value_number),
                Risk_Factor_Element_Maturity = instruments[idx].maturity_date(),
                Global_Context = global_mapping,
                Org_Context = org_mapping,
                User_Context = user_mapping,
                Group_Context = group_mapping,
                Workspace_Context = workspace_mapping
            )._asdict())
            idx += 1
            
        return sensitivities

class Credit_Par_Delta_Sensitivity(Sensitivity):
    def __init__(self, trade, shift_size, risk_factor, calculation):
        super(Credit_Par_Delta_Sensitivity, self).__init__(trade, shift_size, risk_factor, calculation)
        
    def calculate_sensitivity(self):
        sensitivities = []
        COLUMN_ID = 'Credit Par Delta'
        points = self.risk_factor.YieldCurve().Points()
        
        time_buckets = create_timebuckets([p.DatePeriod() for p in points], True)
        actual_dates = [p.ActualDate() for p in points]
        column_config = acm.Sheet.Column().ConfigurationFromTimeBuckets( time_buckets )
        
        top_node = CALC_SPACE_PORTFOLIO.InsertItem(self.trade)
        portf = acm.FAdhocPortfolio()
        portf.Add(self.trade)
        
        calc = CALC_SPACE_PORTFOLIO.CreateCalculation(portf, COLUMN_ID, column_config)
        CALC_SPACE_PORTFOLIO.Refresh()
        
        for value, period, actual_date in zip(calc.Value(), time_buckets, actual_dates):
            value_number = value.Number()

            sensitivities.append(REPORT_ENTRY(
                Trade_Number = self.trdnbr,
                Instrument_Name = self.instrument_name,
                Instrument_Type = self.instrument_type,
                Trade_Process = self.trade.TradeProcessesToString(),
                Instrument_Expiry = self.instrument.maturity_date(),
                Value_Day=self.trade.ValueDay(),
                Portfolio_Name = self.portfolio,
                Chorus_Id = self.chorus_id,
                Counterparty_Name = self.counterparty_name,
                BarCap_SMS_CP_SDSID = self.barCap_SMS_CP_SDSID,
                BarCap_SMS_LE_SDSID = self.barCap_SMS_LE_SDSID,
                Risk_Factor = self.risk_factor.Name(),
                Risk_Factor_Type = self.risk_factor.Type(),
                Risk_Factor_Currency = self.risk_factor.CurrencySymbol(),
                Risk_Factor_Element = self.risk_factor.YieldCurveComponent().AttributeName(),
                Risk_Factor_Element_Type = 'Credit Spread',
                Risk_Type = 'Credit',
                Currency = 'ZAR',
                Risk_Factor_Description = '1bp Par CDS Spread Shift',
                Risk_Value = str(value_number),
                Risk_Factor_Element_Maturity = actual_date,
                Global_Context = global_mapping,
                Org_Context = org_mapping,
                User_Context = user_mapping,
                Group_Context = group_mapping,
                Workspace_Context = workspace_mapping
            )._asdict())
            
        return sensitivities

class Credit_Recovery_Sensitivity(Sensitivity):
    def __init__(self, trade, shift_size, risk_factor, calculation):
        super(Credit_Recovery_Sensitivity, self).__init__(trade, shift_size, risk_factor, calculation)
        
    def calculate_sensitivity(self):
        sensitivities = []
        COLUMN_ID = 'Credit Recovery Sensitivity'
        top_node = CALC_SPACE.InsertItem(self.trade)
        calc = CALC_SPACE.CreateCalculation(top_node, COLUMN_ID)
        idx = 0

            #print instruments, calc.Value()

        value = calc.Value()
        value_number = value.Number()
        
        sensitivities.append(REPORT_ENTRY(
            Trade_Number = self.trdnbr,
            Instrument_Name = self.instrument_name,
            Instrument_Type = self.instrument_type,
            Trade_Process = self.trade.TradeProcessesToString(),
            Instrument_Expiry = self.instrument.maturity_date(),
            Value_Day=self.trade.ValueDay(),
            Portfolio_Name = self.portfolio,
            Chorus_Id = self.chorus_id,
            Counterparty_Name = self.counterparty_name,
            BarCap_SMS_CP_SDSID = self.barCap_SMS_CP_SDSID,
            BarCap_SMS_LE_SDSID = self.barCap_SMS_LE_SDSID,
            Risk_Factor = self.risk_factor.Name(),
            Risk_Factor_Type = self.risk_factor.Type(),
            Risk_Factor_Currency = self.risk_factor.CurrencySymbol(),
            Risk_Factor_Element = self.instrument_name,
            Risk_Factor_Element_Type = 'Recovery Rate',
            Risk_Type = 'Credit',
            Currency = 'ZAR',
            Risk_Factor_Description = '1% Absolute Recovery Rate Shift',
            Risk_Value = str(value_number),
            Risk_Factor_Element_Maturity = '',
            Global_Context = global_mapping,
            Org_Context = org_mapping,
            User_Context = user_mapping,
            Group_Context = group_mapping,
            Workspace_Context = workspace_mapping
        )._asdict())
        idx += 1
            
        return sensitivities
        
class Instrument_Spread_Delta(Sensitivity):
    def __init__(self, trade, shift_size, risk_factor, calculation):
        super(Instrument_Spread_Delta, self).__init__(trade, shift_size, risk_factor, calculation)
        
    def calculate_sensitivity(self):
        sensitivities = []
        COLUMN_ID = 'Instrument Spread Delta'
        benchmarks = self.risk_factor.Benchmarks()
        
        
        
        top_node = CALC_SPACE.InsertItem(self.trade)
        calc = CALC_SPACE.CreateCalculation(top_node, COLUMN_ID)
        idx = 0

            #print instruments, calc.Value()

        value = calc.Value()
        value_number = value.Number()
        
        sensitivities.append(REPORT_ENTRY(
            Trade_Number = self.trdnbr,
            Instrument_Name = self.instrument_name,
            Instrument_Type = self.instrument_type,
            Trade_Process = self.trade.TradeProcessesToString(),
            Instrument_Expiry = self.instrument.maturity_date(),
            Value_Day=self.trade.ValueDay(),
            Portfolio_Name = self.portfolio,
            Chorus_Id = self.chorus_id,
            Counterparty_Name = self.counterparty_name,
            BarCap_SMS_CP_SDSID = self.barCap_SMS_CP_SDSID,
            BarCap_SMS_LE_SDSID = self.barCap_SMS_LE_SDSID,
            Risk_Factor = self.risk_factor.Name(),
            Risk_Factor_Type = self.risk_factor.Type(),
            Risk_Factor_Currency = self.risk_factor.Currency().Name(),
            Risk_Factor_Element = self.instrument_name,
            Risk_Factor_Element_Type = 'Instrument Spread',
            Risk_Type = self.risk_factor.RiskType(),
            Currency = 'ZAR',
            Risk_Factor_Description = '1bp Absolute Spread Shift',
            Risk_Value = str(value_number),
            Risk_Factor_Element_Maturity = '',
            Global_Context = global_mapping,
            Org_Context = org_mapping,
            User_Context = user_mapping,
            Group_Context = group_mapping,
            Workspace_Context = workspace_mapping
        )._asdict())
        idx += 1
            
        return sensitivities

class Vega(Sensitivity):
    def __init__(self, trade, shift_size, risk_factor, calculation):
        super(Vega, self).__init__(trade, shift_size, risk_factor, calculation)
        
    def calculate_sensitivity(self):
        sensitivities = []
        COLUMN_ID = 'Portfolio Vega Implicit Per Volatility Structure'
        
        volatility_structure = [self.risk_factor]
        column_config = acm.Sheet.Column().ConfigurationFromVector(volatility_structure)
        top_node = CALC_SPACE.InsertItem(self.trade)
        calc = CALC_SPACE.CreateCalculation(top_node, COLUMN_ID, column_config)
        
        top_node = CALC_SPACE.InsertItem(self.trade)
        calc = CALC_SPACE.CreateCalculation(top_node, COLUMN_ID)
        
        idx = 0

        value = calc.Value()
        value_number = value.Number()
        
        risk_factor_name = ''
        risk_factor_structure_type = ''
        
        try:
            risk_factor_structure_type = self.risk_factor.StructureType()
            risk_factor_name = self.risk_factor.Name()
        except Exception, e:
            pass
        
        sensitivities.append(REPORT_ENTRY(
            Trade_Number = self.trdnbr,
            Instrument_Name = self.instrument_name,
            Instrument_Type = self.instrument_type,
            Trade_Process = self.trade.TradeProcessesToString(),
            Instrument_Expiry = self.instrument.maturity_date(),
            Value_Day=self.trade.ValueDay(),
            Portfolio_Name = self.portfolio,
            Chorus_Id = self.chorus_id,
            Counterparty_Name = self.counterparty_name,
            BarCap_SMS_CP_SDSID = self.barCap_SMS_CP_SDSID,
            BarCap_SMS_LE_SDSID = self.barCap_SMS_LE_SDSID,
            Risk_Factor = risk_factor_name,
            Risk_Factor_Type = risk_factor_structure_type,
            Risk_Factor_Currency = self.risk_factor.Currency().Name() if self.risk_factor.Currency() else '',
            Risk_Factor_Element = risk_factor_name,
            Risk_Factor_Element_Type = 'Volatility Structure',
            Risk_Type = self.risk_factor.RiskType(),
            Currency = 'ZAR',
            Risk_Factor_Description = '1% Parallel Volatility Shift',
            Risk_Value = str(value_number),
            Risk_Factor_Element_Maturity = '',
            Global_Context = global_mapping,
            Org_Context = org_mapping,
            User_Context = user_mapping,
            Group_Context = group_mapping,
            Workspace_Context = workspace_mapping
        )._asdict())
        idx += 1
            
        return sensitivities

class EquityDelta(Sensitivity):
    def __init__(self, trade, shift_size, risk_factor, calculation):
        super(EquityDelta, self).__init__(trade, shift_size, risk_factor, calculation)
        
    def calculate_sensitivity(self):
        sensitivities = []
        COLUMN_ID = 'Portfolio Delta Implicit % Equity'
        
        top_node = CALC_SPACE.InsertItem(self.trade)
        calc = CALC_SPACE.CreateCalculation(self.trade, COLUMN_ID)
        
        idx = 0
        #print calc
        value = calc.Value()
        value_number = value.Number()
        
        sensitivities.append(REPORT_ENTRY(
            Trade_Number = self.trdnbr,
            Instrument_Name = self.instrument_name,
            Instrument_Type = self.instrument_type,
            Trade_Process = self.trade.TradeProcessesToString(),
            Instrument_Expiry = self.instrument.maturity_date(),
            Value_Day=self.trade.ValueDay(),
            Portfolio_Name = self.portfolio,
            Chorus_Id = self.chorus_id,
            Counterparty_Name = self.counterparty_name,
            BarCap_SMS_CP_SDSID = self.barCap_SMS_CP_SDSID,
            BarCap_SMS_LE_SDSID = self.barCap_SMS_LE_SDSID,
            Risk_Factor = self.risk_factor.Name(),
            Risk_Factor_Type = 'EquitySpot',
            Risk_Factor_Currency = self.risk_factor.Currency().Name(),
            Risk_Factor_Element = self.risk_factor.Name(),
            Risk_Factor_Element_Type = 'EquitySpotPrice',
            Risk_Type = 'Equity',
            Currency = 'ZAR',
            Risk_Factor_Description = '1% Equity Price Shift',
            Risk_Value = str(value_number),
            Risk_Factor_Element_Maturity = '',
            Global_Context = global_mapping,
            Org_Context = org_mapping,
            User_Context = user_mapping,
            Group_Context = group_mapping,
            Workspace_Context = workspace_mapping
        )._asdict())
        idx += 1
            
        return sensitivities

class PresentValue(Sensitivity):
    def __init__(self, trade, shift_size, risk_factor, calculation):
        super(PresentValue, self).__init__(trade, shift_size, risk_factor, calculation)
        
    def calculate_sensitivity(self):
        sensitivities = []
        
        try:
            value  = self.calculation.Value().Number() 
        except Exception, e:
            value = '#'
        sensitivities.append(REPORT_ENTRY(
            Trade_Number = self.trdnbr,
            Instrument_Name = self.instrument_name,
            Instrument_Type = self.instrument_type,
            Trade_Process = self.trade.TradeProcessesToString(),
            Instrument_Expiry = self.instrument.maturity_date(),
            Value_Day=self.trade.ValueDay(),
            Portfolio_Name = self.portfolio,
            Chorus_Id = self.chorus_id,
            Counterparty_Name = self.counterparty_name,
            BarCap_SMS_CP_SDSID = self.barCap_SMS_CP_SDSID,
            BarCap_SMS_LE_SDSID = self.barCap_SMS_LE_SDSID,
            Risk_Factor = 'Present Value',
            Risk_Factor_Type = 'Present Value',
            Risk_Factor_Element = self.instrument_name,
            Risk_Factor_Currency = self.instrument.Currency().Name(),
            Risk_Factor_Element_Type = 'Present Value',
            Risk_Type = '',
            Currency = 'ZAR',
            Risk_Factor_Description = 'Present Value',
            Risk_Value = str(value),
            Risk_Factor_Element_Maturity = '',
            Global_Context = global_mapping,
            Org_Context = org_mapping,
            User_Context = user_mapping,
            Group_Context = group_mapping,
            Workspace_Context = workspace_mapping
        )._asdict())
            
        return sensitivities
        
class FX_Delta(Sensitivity):
    def __init__(self, trade, shift_size, risk_factor, calculation):
        super(FX_Delta, self).__init__(trade, shift_size, risk_factor, calculation)
    
    def _create_named_param(self, vector, currency ):
        param = acm.FNamedParameters();
        param.AddParameter( 'currency', currency)
        vector.Add( param )

    def calculate_sensitivity(self):
        sensitivities = []
        COLUMN_ID = 'Portfolio FX Delta %'
        
        vector = acm.FArray()
        self._create_named_param( vector, self.risk_factor)

        column_config = acm.Sheet.Column().ConfigurationFromVector(vector)
        
        top_node = CALC_SPACE_PORTFOLIO.InsertItem(self.trade)
        portf = acm.FAdhocPortfolio()
        portf.Add(self.trade)
        
        calc = CALC_SPACE_PORTFOLIO.CreateCalculation(portf, COLUMN_ID, column_config)
        CALC_SPACE_PORTFOLIO.Refresh()
        
        idx = 0
    
        value = calc.Value()
        value_number = value.Number()
        
        sensitivities.append(REPORT_ENTRY(
            Trade_Number = self.trdnbr,
            Instrument_Name = self.instrument_name,
            Instrument_Type = self.instrument_type,
            Trade_Process = self.trade.TradeProcessesToString(),
            Instrument_Expiry = self.instrument.maturity_date(),
            Value_Day=self.trade.ValueDay(),
            Portfolio_Name = self.portfolio,
            Chorus_Id = self.chorus_id,
            Counterparty_Name = self.counterparty_name,
            BarCap_SMS_CP_SDSID = self.barCap_SMS_CP_SDSID,
            BarCap_SMS_LE_SDSID = self.barCap_SMS_LE_SDSID,
            Risk_Factor = self.risk_factor.Name(),
            Risk_Factor_Type = 'FX Rate',
            Risk_Factor_Element = self.risk_factor.Name(),
            Risk_Factor_Element_Type = 'FX Rate',
            Risk_Factor_Currency = self.risk_factor.Name(),
            Risk_Type = 'FX',
            Currency = 'ZAR',
            Risk_Factor_Description = '1% Increase vs all other currencies',
            Risk_Value = str(value_number),
            Risk_Factor_Element_Maturity = '',
            Global_Context = global_mapping,
            Org_Context = org_mapping,
            User_Context = user_mapping,
            Group_Context = group_mapping,
            Workspace_Context = workspace_mapping
        )._asdict())
        idx += 1
            
        return sensitivities

class IR_Spread_Delta(Sensitivity):
    def __init__(self, trade, shift_size, risk_factor, calculation):
        super(IR_Spread_Delta, self).__init__(trade, shift_size, risk_factor, calculation)
    
    def _create_named_param(self, vector, curve ):
        param = acm.FNamedParameters();
        param.AddParameter( 'Interest Rate Spread Delta Curve', curve)
        vector.Add( param )

    def calculate_sensitivity(self):
        sensitivities = []
        COLUMN_ID = 'Interest Rate Spread Delta Buckets Per Yield Curve'
        
        vector = ael_main_ex({'Yield Curve': self.risk_factor, 'Base Value':'Theoretical Total Profit/Loss'}, {})
        
        dates = [e.UniqueTag() for e in vector]
        column_config = acm.Sheet.Column().ConfigurationFromVector(vector)
        
        top_node = CALC_SPACE_PORTFOLIO.InsertItem(self.trade)
        portf = acm.FAdhocPortfolio()
        portf.Add(self.trade)
        
        calc = CALC_SPACE_PORTFOLIO.CreateCalculation(portf, COLUMN_ID, column_config)
        CALC_SPACE_PORTFOLIO.Refresh()
        
        
        for value, date in zip(calc.Value(), dates):
            value_number = value.Number()
            
            sensitivities.append(REPORT_ENTRY(
                Trade_Number = self.trdnbr,
                Instrument_Name = self.instrument_name,
                Instrument_Type = self.instrument_type,
                Trade_Process = self.trade.TradeProcessesToString(),
                Instrument_Expiry = self.instrument.maturity_date(),
                Value_Day=self.trade.ValueDay(),
                Portfolio_Name = self.portfolio,
                Chorus_Id = self.chorus_id,
                Counterparty_Name = self.counterparty_name,
                BarCap_SMS_CP_SDSID = self.barCap_SMS_CP_SDSID,
                BarCap_SMS_LE_SDSID = self.barCap_SMS_LE_SDSID,
                Risk_Factor = self.risk_factor.Name(),
                Risk_Factor_Type = self.risk_factor.Type(),
                Risk_Factor_Currency = self.risk_factor.Currency().Name(),
                Risk_Factor_Element = self.risk_factor.Name(),
                Risk_Factor_Element_Type = 'Spread',
                Risk_Type = self.risk_factor.RiskType(),
                Currency = 'ZAR',
                Risk_Factor_Description = '1bp Absolute Spread Shift',
                Risk_Value = str(value_number),
                Risk_Factor_Element_Maturity = date,
                Global_Context = global_mapping,
                Org_Context = org_mapping,
                User_Context = user_mapping,
                Group_Context = group_mapping,
                Workspace_Context = workspace_mapping
            )._asdict())
            
        return sensitivities
        
class One_Percent_Vega_Sensitivity(Sensitivity):

    def __init__(self, trade, shift_size, risk_factor, calculation):
        super(One_Percent_Vega_Sensitivity, self).__init__(trade, shift_size, risk_factor, calculation)
        
    def _calculate_vega(self, vol_surface):
        prices = benchmark.Instrument().Prices()
        pv0 = self.calculation.Value().Number()
        
        for price in prices:
            price.Bid(price.Bid() * self.shift_size)
            price.Ask(price.Ask() * self.shift_size)
            price.Last(price.Last() * self.shift_size)
            price.Settle(price.Settle() * self.shift_size)
            
            price.SimulateRecursive()
        
        pv1 = self.calculation.Value().Number()
        
        for price in prices:
           
            price.Unsimulate()
            
        return pv1 - pv0
        
    def calculate_sensitivity(self):
        sensitivities = []
        
        sensitivities.append(REPORT_ENTRY(
            Trade_Number = self.trdnbr,
            Instrument_Name = self.instrument_name,
            Instrument_Type = self.instrument_type,
            Trade_Process = self.trade.TradeProcessesToString(),
            Instrument_Expiry = self.instrument.maturity_date(),
            Value_Day=self.trade.ValueDay(),
            Portfolio_Name = self.portfolio,
            Chorus_Id = self.chorus_id,
            Counterparty_Name = self.counterparty_name,
            BarCap_SMS_CP_SDSID = self.barCap_SMS_CP_SDSID,
            BarCap_SMS_LE_SDSID = self.barCap_SMS_LE_SDSID,
            Risk_Factor = self.risk_factor.Name(),
            Risk_Factor_Type = self.risk_factor.Type(),
            Risk_Factor_Currency = self.risk_factor.Currency().Name(),
            Risk_Factor_Element = benchmark.Instrument().Name(),
            Risk_Factor_Element_Type = 'Volatility Structure',
            Risk_Type = self.risk_factor.RiskType(),
            Currency = 'ZAR',
            Risk_Factor_Description = '1% Parallel Volatility Shift',
            Risk_Value = str(self._calculate_benchmark_sensitivity(benchmark)),
            Risk_Factor_Element_Maturity = benchmark.Instrument().maturity_date(),
            Global_Context = global_mapping,
            Org_Context = org_mapping,
            User_Context = user_mapping,
            Group_Context = group_mapping,
            Workspace_Context = workspace_mapping
        )._asdict())
        
        return sensitivities
        
def ael_main(ael_params):
    risk_factors = {
        'benchmark_curve': defaultdict(set),
        'spread_curve': defaultdict(set),
        'instrument_spread_curve': defaultdict(set),
        'price_curve': defaultdict(set),
        'vega': defaultdict(set),
        'curr': defaultdict(set),
        'equity': defaultdict(set),
        'issuer_curve': defaultdict(set),
        'present_value': defaultdict(set)
    }
    

    trades = ael_params['trade_selection']
    
    for trade in trades:
        #if trade.Instrument().maturity_date() < acm_date('today'):
        #    continue
        price_curve = mapped_price_curve(trade)
        benchmark_yield_curves = mapped_benchmark_curve(trade)
        spread_curves = mapped_spread_curves(trade)
        credit_curves = mapped_credit_curve(trade)
        volatility_structures = mapped_volatility_structure(trade)
        currencies = currency_exposure(trade)
        equity = mapped_underlying(trade)
        
        if price_curve:
            risk_factors['price_curve'][price_curve].add(trade)
        
        for yc in benchmark_yield_curves:
            risk_factors['benchmark_curve'][yc].add(trade)
        
        for curr in currencies:
            risk_factors['curr'][curr].add(trade)
        if equity:
            risk_factors['equity'][equity].add(trade)
        
        risk_factors['present_value'][trade] = CALC_SPACE.CreateCalculation(trade, 'Portfolio Present Value')
        
        if volatility_structures:
            if volatility_structures.IsKindOf(acm.FCollection):
                for vs in volatility_structures:
                    risk_factors['vega'][vs].add(trade)
            else:
                risk_factors['vega'][volatility_structures].add(trade)
        
        for credit_curve in credit_curves:
            risk_factors['issuer_curve'][credit_curve].add(trade)
            
        for spread_curve in spread_curves:
            if spread_curve.Type() == 'Instrument Spread':
                risk_factors['instrument_spread_curve'][spread_curve].add(trade)
            elif spread_curve.Type()  == 'Attribute Spread' and spread_curve.AttributeType() == 'Issuer':
                risk_factors['issuer_curve'][spread_curve].add(trade)
            else:
                risk_factors['spread_curve'][spread_curve].add(trade)
        #print risk_factors['spread_curve']
        
        
    
    with open(ael_params['out_file'], 'w') as f:
        writer = csv.DictWriter(
            f,
            REPORT_ENTRY._fields,
            delimiter=';',
            lineterminator = '\n'
        )
        
        writer.writerow(dict(list(zip(REPORT_ENTRY._fields, REPORT_ENTRY._fields))))

        CALC_SPACE.SimulateGlobalValue('Position Currency Choice', 'Fixed Curr')
        CALC_SPACE.SimulateGlobalValue('Fixed Currency', acm.FCurrency['ZAR'])
        
        for curve in risk_factors['equity']:
            for t in risk_factors['equity'][curve]:
                sensitivities = EquityDelta(t, 1.01, curve, risk_factors['present_value'][t]).calculate_sensitivity()
                writer.writerows(sensitivities)
        
        for t in risk_factors['present_value']:
            sensitivities = PresentValue(t, 1.01, t, risk_factors['present_value'][t]).calculate_sensitivity()
            writer.writerows(sensitivities)
                
        for curve in risk_factors['benchmark_curve']:
            for t in risk_factors['benchmark_curve'][curve]:
                sensitivities = IR_Benchmark_Delta_Sensitivity(t, 1.01, curve, risk_factors['present_value'][t]).calculate_sensitivity()
                writer.writerows(sensitivities)

        for curve in risk_factors['price_curve']:
            for t in risk_factors['price_curve'][curve]:
                price_curve = acm.FPriceCurve[curve]
                sensitivities = Commodity_Benchmark_Delta(t, 1.01, price_curve, risk_factors['present_value'][t]).calculate_sensitivity()
                writer.writerows(sensitivities)
        
        for curve in risk_factors['instrument_spread_curve']:
            for t in risk_factors['instrument_spread_curve'][curve]:
                sensitivities = Instrument_Spread_Delta(t, 1.01, curve, risk_factors['present_value'][t]).calculate_sensitivity()
                writer.writerows(sensitivities)
        
        for curve in risk_factors['spread_curve']:
            for t in risk_factors['spread_curve'][curve]:
                sensitivities = IR_Spread_Delta(t, 1.01, curve, risk_factors['present_value'][t]).calculate_sensitivity()
                writer.writerows(sensitivities)
                
        print risk_factors['issuer_curve']
        for curve in risk_factors['issuer_curve']:
            for t in risk_factors['issuer_curve'][curve]:
                sensitivities = Credit_Par_Delta_Sensitivity(t, 1.01, curve, risk_factors['present_value'][t]).calculate_sensitivity()
                writer.writerows(sensitivities)
                sensitivities = Credit_Recovery_Sensitivity(t, 1.01, curve, risk_factors['present_value'][t]).calculate_sensitivity()
                writer.writerows(sensitivities)
        
        for vol_surface in risk_factors['vega']:
            for t in risk_factors['vega'][vol_surface]:
                sensitivities = Vega(t, 1.01, vol_surface, risk_factors['present_value'][t]).calculate_sensitivity()
                writer.writerows(sensitivities)
        
        for curr in risk_factors['curr']:
            for t in risk_factors['curr'][curr]:
                sensitivities = FX_Delta(t, 1.01, curr, risk_factors['present_value'][t]).calculate_sensitivity()
                writer.writerows(sensitivities)
                
        CALC_SPACE.RemoveGlobalSimulation('Position Currency Choice')
        CALC_SPACE.RemoveGlobalSimulation('Fixed Currency')

print '/services/frontnt/Task/ISDA_SIMM_Sensitivities.csv'
