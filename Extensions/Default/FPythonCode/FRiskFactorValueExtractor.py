from __future__ import print_function
"""-------------------------------------------------------------------------------------------------------
MODULE
    FRiskFactorValueExtractor - 
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import math
from operator import itemgetter

import FADMRiskFactorDescription
import FVaRStaticData
import FRiskFactorFileProcessing

import FLogger
logger = FLogger.FLogger.GetLogger('FARiskFactorExtraction')

cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
context = acm.GetDefaultContext()
sheet_type = 'FDealSheet'
calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)
mapped_valpar = acm.GetFunction("mappedValuationParameters", 0)().Parameter()
grid_mat_eps = acm.GetFunction("gridMaturityEpsilon", 1)(mapped_valpar.GridMinimumDays())


def get_possible_historical_entity(id, entity, reference_date, today):
    try:
        if entity.HistoricalDay():
            if entity.Class().IncludesBehavior(acm.FVolatilityStructure):
                entity = entity.OriginalStructure()
            elif entity.Class().IncludesBehavior(acm.FYieldCurve):
                entity = entity.OriginalCurve()
        if acm.IsHistoricalMode() or reference_date < today:
            entity = acm.GetHistoricalEntity(entity, reference_date)
            historical_day = entity.HistoricalDay()
            if not historical_day:
               logger.WLOG('%s: No historical record found for %s on %s, using live record' %(id, entity.Name(), reference_date)) 
        return entity
    except:
        return None

def log_extraction_error(id, target, reference_date):
    if target:
        msg = '%s: Failed to extract value from %s on %s' %(id, 
            target.Name(), reference_date)
    else:
        msg = '%s: Failed to extract value on %s' %(id, reference_date)
    logger.ELOG(msg)

def value_or_zero(value):
    try:
        val = float(value)
        if math.isnan(val):
            return 0.0, 0
    except: 
        return 0.0, 0
    return val, 1

def get_benchmark_underlying_instrument(vol_structure, date):
    points = vol_structure.Points().SortByProperty("ActualExpiryCoordinate")
    ins = None
    for point in points:
        if point.Benchmark() and point.Benchmark().ValuationUnderlying():
            ins = point.Benchmark().ValuationUnderlying()
            if date <= point.ActualExpiryDay():
                return ins
    return ins

def get_float_rate_instrument(vol_structure, date):
    points = vol_structure.Points().SortByProperty("ActualExpiryCoordinate")
    ins = None
    for point in points:
        benchmark = point.Benchmark()
        if benchmark and benchmark.IsKindOf('FCashFlowInstrument') and benchmark.FirstFloatLeg():
            ins = benchmark.FirstFloatLeg().FloatRateReference()
            if date <= point.ActualExpiryDay():
                return ins
    return ins

def get_reference_instrument(vol_structure, date):
    ins = None
    structure = vol_structure
    while structure and not ins:
        ins = structure.ReferenceInstrument()
        structure = structure.UnderlyingStructure()
    if not ins:
        structure = vol_structure
        while structure and not ins:
            ins = get_benchmark_underlying_instrument(structure, date)
            structure = structure.UnderlyingStructure()
    if not ins:
        structure = vol_structure
        while structure and not ins:
            ins = get_float_rate_instrument(structure, date)
            structure = structure.UnderlyingStructure()
    return ins

def get_vol_info_from_structure(structure, reference_date, grid_eps):
    underlying_structure = structure.UnderlyingStructure()
    if underlying_structure:
        underlying_info = get_vol_info_from_structure(
                    underlying_structure, reference_date, grid_eps)
        info = structure.VolatilityInformation(underlying_info, reference_date, grid_eps)
    else:
        info = structure.VolatilityInformation(reference_date, grid_eps)
    return info

def forward_price(ins, reference_date, date):
    today = acm.Time().DateToday()
    date = ins.SpotDate(date)
    if today == reference_date:
        strike = ins.Calculation().ForwardPrice(cs, date)
    else:
        calc_space.SimulateValue(ins, 'Valuation Date', reference_date)
        calc_space.SimulateValue(ins, 'Standard Calculations Forward Date', date)
        calc = calc_space.CreateCalculation(ins, 'Standard Calculations Forward Price')
        strike = calc.Value()
        calc_space.RemoveSimulation(ins, 'Valuation Date')
        calc_space.RemoveSimulation(ins, 'Standard Calculations Forward Date')
    return strike
    
def get_vol_from_vol_info(vol_info, reference_date, date, strike_type, reference_instrument):
    und_mat_date = reference_date
    strike = 0.0
    if 'Absolute' == strike_type or 'Spread' == strike_type:
        if reference_instrument:
            try:
                strike = forward_price(reference_instrument, reference_date, date)
            except:
                strike = 0.0
    elif 'Delta' == strike_type:
        strike = 0.5
    return value_or_zero(vol_info.Value(und_mat_date, date, strike, True, True))

            
def ipol_vol(x, days_vols):
    if x < days_vols[0][0]:
        return days_vols[0][1]
    elif x > days_vols[-1][0]:
        return days_vols[-1][1]
    else:
        for idx, day_vol in enumerate(days_vols):
            if x <= day_vol[0]:
                j = idx
                i = j - 1
                break
        try:
            return ((days_vols[j][0] - x) * days_vols[i][1] + \
                    (x - days_vols[i][0]) * days_vols[j][1]) / (days_vols[j][0] - days_vols[i][0])
        except ZeroDivisionError as msg:
            logger.ELOG(msg)
            return 0.0

def get_vol_from_vol_structure(vol_structure, reference_date, date):
    if vol_structure.IsParametricStructure():
        skews = vol_structure.Skews()
        days_vols = [(acm.Time().DateDifference(
                      skew.ActualExpiryDay(reference_date), reference_date),
                      skew.A1()) for skew in skews]
        days_vols.sort(key=itemgetter(0))
        if len(days_vols):
            x = acm.Time().DateDifference(date, reference_date)
            return ipol_vol(x, days_vols), 1
        else:
            return 0.0, 0
    elif 'Instrument Specific' == vol_structure.StructureType():
        logger.ELOG("Volatility structure %s is of unsupported type 'Instrument Specific'" % vol_structure.Name())
        return 0.0, 0
    elif 'Issuer' == vol_structure.StructureType():
        logger.ELOG("Volatility structure %s is of unsupported type 'Issuer'" % vol_structure.Name())
        return 0.0, 0
    else:
        vol_info = get_vol_info_from_structure(vol_structure, reference_date, grid_mat_eps)
        if vol_info:
            ins = get_reference_instrument(vol_structure, date)
            if not ins:
                logger.ELOG("No reference instrument for volatility %s" %vol_structure.Name())
            new_value, valid = get_vol_from_vol_info(vol_info, 
                    reference_date, date, vol_structure.StrikeType(), ins)
    return new_value, valid

def get_yc_attribute(curve, targetcoordinates):
    if targetcoordinates:
        currency = targetcoordinates[acm.FSymbol("Currency")]
        if not currency:
            currency = curve.Currency()
        targetAttributeValue = targetcoordinates[acm.FSymbol(curve.AttributeType().replace(" ", ""))]
        return curve.YCAttributeForRiskFactor(targetAttributeValue, currency)   
    else:
        print ("no attribute found for curve " + curve.Name())
    return None

def get_curve_info_from_curve(curve, reference_date, targetcoordinates=None):
    try:
        if curve.Class() == acm.FBenchmarkCurve:
            return curve.IrCurveInformation(reference_date)
        elif curve.Class() == acm.FPriceCurve:
            return curve.IrCurveInformation(reference_date)
        elif curve.Class() == acm.FInflationCurve:
            return curve.IrCurveInformation(reference_date)
        else:
            und_curve = None
            component = curve
            if curve.Class() == acm.FSpreadCurve:
                und_curve = curve.UnderlyingCurve()
            elif curve.Class() == acm.FAttributeSpreadCurve:
                component = get_yc_attribute(curve, targetcoordinates)
                if component:
                    und_curve = component.UnderlyingCurve()
                    if not und_curve:
                        und_curve = curve.UnderlyingCurve()
            else:
                return None
            und_curve_info = get_curve_info_from_curve(
                und_curve, reference_date)
            return component.IrCurveInformation(und_curve_info, reference_date)        
        return None
    except:
        return None

def vol_value_extractor(id, target, reference_date, today, base_curr,
                    timebucket, price_or_yield, targetcoordinates):
    date = timebucket.BucketDate()
    vol_structure = target
    value = 0
    valid = 0
    if vol_structure:
        vol_structure = get_possible_historical_entity(id, vol_structure, reference_date, today)
        if vol_structure:
            value, valid = get_vol_from_vol_structure(vol_structure, reference_date, date)
    if not valid:
        log_extraction_error(id, target, reference_date)
    return value, valid

def curve_value( id, target, reference_date, today, date, 
    targetcoordinates, rate_type, calc_type, rate_or_price ):
    
    value = 0
    valid = 0
    curve = target
    curve = get_possible_historical_entity(id, curve, reference_date, today)
    if curve:
        curve_info = get_curve_info_from_curve(curve, reference_date,
                        targetcoordinates)
        if curve_info:
            if 'Rate' == rate_or_price:
                value, valid = value_or_zero(curve_info.Rate(reference_date, date, rate_type, 
                    'Act/365', calc_type, None, 1))
            else:
                value, valid = value_or_zero(curve_info.Price( date ))
    if not valid:
        log_extraction_error(id, target, reference_date)
    return value, valid


def ir_value_extractor(id, target, reference_date, today, base_curr,
                    timebucket, price_or_yield, targetcoordinates):
    rate_type = 'Discount'
    calc_type = 'Discount'
    if 'Yield' == price_or_yield:
        rate_type = 'Annual Comp'
        calc_type = 'Spot Rate'
    date = timebucket.BucketDate()
    return curve_value( id, target, reference_date, today, date,
                targetcoordinates, rate_type, calc_type, 'Rate' )
    
def credit_value_extractor(id, target, reference_date, today, base_curr,
                    timebucket, price_or_yield, targetcoordinates):
    date = timebucket.BucketDate()
    
    return curve_value( id, target, reference_date, today, date,
                targetcoordinates, 'Annual Comp', 'Spot Rate', 'Rate' )

def spot_price( id, target, reference_date ):
    value, valid = value_or_zero(
        target.Calculation().MarketPrice(cs, reference_date).Number())
    if not valid:
        log_extraction_error(id, target, reference_date)
    return value, valid

def eq_value_extractor(id, target, reference_date, today, base_curr,
                    timebucket, price_or_yield, targetcoordinates):
    return spot_price( id, target, reference_date )

def commodity_value_extractor(id, target, reference_date, today, base_curr,
                    timebucket, price_or_yield, targetcoordinates):
    if timebucket:
        date = timebucket.BucketDate()
        return curve_value( id, target, reference_date, today, date,
                targetcoordinates, None, None, 'Price' )
    else:
        return spot_price( id, target, reference_date )
        
def fx_value_extractor(id, target, reference_date, today, base_curr, 
                    timebucket, price_or_yield, targetcoordinates):
    if target == base_curr:
        value = 1.0
        valid = 0
    else:
        value, valid = value_or_zero(
            target.Calculation().HistoricalFXRate(cs, base_curr, reference_date).Number())
        if not valid:
            log_extraction_error(id, target, reference_date)
    return value, valid
    
type_function_mapping = {
    'Interest Rate' : ir_value_extractor,
    'Equity': eq_value_extractor,
    'FX': fx_value_extractor,
    'Credit': credit_value_extractor,
    'Volatility': vol_value_extractor,
    'Commodity': commodity_value_extractor}

def get_risk_factor_value_from_risk_factors(riskfactors, today, 
        reference_date, base_curr, price_or_yield):
    value = 0.0
    count = 0.0
    for riskfactor in riskfactors:
        id = riskfactor.ExternalId()
        rf_type = riskfactor.Target().RiskFactorType()
        func = type_function_mapping[rf_type]
        factor = 1.0 / FVaRStaticData.absolute_scale_factor_mapping[rf_type]
        new_count = 0.0
        new_value = 0.0
        targets = riskfactor.Target().Targets()
        if not targets:
            continue
        if func and len(targets):
            target_value = 0.0
            target_weight = 0.0
            for idx, target in enumerate(targets):
                weights = riskfactor.Target().Weights()
                if weights and len(weights) > idx:
                    target_weight = weights[idx]
                else:
                    target_weight = 0.0
                target_value, valid = func(id, target, reference_date, today, base_curr,
                    riskfactor.RiskFactorDescription().Coordinate( "Time" ),
                    price_or_yield, riskfactor.RiskFactorDescription().TargetCoordinates() )
                target_weight = target_weight * valid
                target_value = target_value * target_weight
                new_value = new_value + target_value
                new_count = new_count + target_weight
        value = value + factor * new_value
        count = count + new_count
    return value, count

def risk_factor_value_per_spec(spec_header, today, base_curr,
    reference_dates, file_results = None, specs = None):
    
    out = {}
    price_or_yield = spec_header.RiskFactorType()
    
    risk_factor_creator = acm.FRiskFactorCreator(spec_header)
    
    risk_factor_specs = specs
    processed = []
    ids = []
    if file_results:
        """
        get ids from file_results
        """
        ids = file_results.keys()
    if len(ids) == 0:
        """
        Get risk factor spec ids from header
        """
        risk_factor_specs = acm.FRiskFactorSpec.Select("rfspec=%s" % spec_header.Oid())
        for spec in risk_factor_specs:
            ids.append(spec.Name())

    labels_token = FRiskFactorFileProcessing.labels_token(spec_header.CommentChar())

    out[labels_token] = reference_dates
    processed.append(labels_token)
    for id in ids:
        values = []
        if id in processed:
            #done, do next
            continue
        processed.append(id)
        riskfactors = risk_factor_creator.RiskFactors(id)
        for date in reference_dates:
            value, count = get_risk_factor_value_from_risk_factors(riskfactors, 
                    today, date, base_curr, price_or_yield)
            if count:
                values.append(value / count)
            else:
                values.append(float('nan'))
        if len(values):
            out[id] = values
    return out
