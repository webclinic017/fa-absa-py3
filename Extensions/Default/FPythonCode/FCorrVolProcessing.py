"""-----------------------------------------------------------------------
MODULE
    FCorrVolProcessing - Process correlation and volatility data.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    TODO: Fill in a nice description

EXTERNAL DEPENDENCIES
    PRIME 2010.1 or later.
-----------------------------------------------------------------------"""
import acm
import FVaRFileParsing
import exceptions
from collections import namedtuple
from FVaRPerformanceLogging import acm_perf_log
from FVaRPerformanceLogging import log_trace, log_debug, log_error
import math

class DimensionException(exceptions.Exception):
    pass

class MatrixException(exceptions.Exception):
    pass

def log_error(log_string):
    acm.Log(log_string)

def get_fx_external_id(currency, spec_header):
    """
    Find a mapped external id for currency.
    """
    try:
        rfm = acm.FRiskFactorMember.Select01("instrument = %s and riskFactorGrpType = FX"%currency.Oid(), "")
        rfs = acm.FRiskFactorSpec.Select01("rfg = %s and rfspec = %s"%(rfm.RiskFactorGroup().Oid(), spec_header.Oid()), "")
        log_debug("Found spec '%s' for currency '%s'" % \
            (rfs.Name(), currency.Name()))
        return rfs.Name()
    except:
        return None
    
def parse_volatility_line(line, delimiter, price_vol_col, yield_vol_col, max_col, mapped_external_ids):
    """
    TODO: Nice comment + exception handling + comment char
    """
    components = line.split(delimiter)
    if len(components) >= max_col:
        external_id = components[0].strip()
        if external_id in mapped_external_ids:
            price_vol = components[price_vol_col - 1].strip()
            yield_vol = components[yield_vol_col - 1].strip()
            return external_id, [price_vol, yield_vol]
    else:
        log_error("Too few columns in volfile %d (max=%d).Line is'%s'." % \
            (len(components), max_col, line))
    return None, [0.0, 0.0]

VolatilityData = namedtuple("VolatilityData", ["unadjusted_volatilities",
    "fx_base_currency_volatility", "volatility_base_currency_external_id"])
def parse_volatility_file(file_name, spec_header, fx_base_currency):
    """
    returns array(string), array(float)
    """
    log_debug("parse_volatility_file")
    comment_char = spec_header.CommentChar()
    delimiter = spec_header.DelimiterChar()
    price_vol_col = spec_header.PriceVolColNbr()
    yield_vol_col = spec_header.VolatilityColNbr()
    max_col = max(price_vol_col, yield_vol_col)
    lines = FVaRFileParsing.read_volatility_file(file_name)
    risk_factor_specs = acm.FRiskFactorSpec.Select("rfspec = '%s'" % spec_header.Name()).AsArray()
    mapped_external_ids = set([rfs.Name() for rfs in risk_factor_specs])
    fx_base_external_id = get_fx_external_id(fx_base_currency, spec_header)
    file_curr_external_id = get_fx_external_id(spec_header.VolatilityBaseCurrency(), spec_header)
    fx_base_vol = (fx_base_external_id, 0.0)
    vol_items = {}
    for line in lines:
        if not line.startswith(comment_char):
            external_id, volatility = \
                parse_volatility_line(line, delimiter, price_vol_col, yield_vol_col, max_col, mapped_external_ids)
            if external_id:
                if external_id == fx_base_external_id :
                    fx_base_vol = (fx_base_external_id, volatility[0])
                elif external_id == file_curr_external_id:
                    continue
                else:
                    vol_items[external_id] = volatility
    if file_curr_external_id and fx_base_external_id != file_curr_external_id:
        vol_items[file_curr_external_id] = [0.0, 0.0]
    return VolatilityData(vol_items, fx_base_vol, file_curr_external_id)

def parse_correlation_line(line, cross_delimiter, delimiter, external_ids, column):
    """
    Parses a correlation file line into
    EXTERNID1, EXTERNID2, Correlation
    """
    components = line.split(delimiter)
    if len(components) >= column:
        pair = components[0].strip()
        cs = pair.split(cross_delimiter)
        ext_id = cs[0]
        for c in cs[1:]:
            if ext_id in external_ids:
                other_ext_id = pair[len(ext_id) + 1:]
                if other_ext_id in external_ids:
                    return ext_id, other_ext_id, components[column - 1]
            ext_id = ext_id + cross_delimiter + c
        return None, None, 0.0
    else:
        log_error("Too few columns in corrfile %d (max=%d).Line is'%s'." % (len(components), column, line))
    return None, None, 0.0

def parse_correlation_lines(lines, external_ids, spec_header):
    """
    returns ordered_correlations, coordinates, dimension
    """
    cross_delimiter = spec_header.CorrelationIdDelimChar()
    delimiter = spec_header.DelimiterChar()
    comment_char = spec_header.CommentChar()
    column = spec_header.CorrelationColNbr()
    correlation_lookup_table = {}
    found_external_ids = set()
    for line in lines:
        if not line.startswith(comment_char):
            external_id, other_external_id, correlation = \
                parse_correlation_line(line, cross_delimiter, delimiter, external_ids, column)
            if external_id and other_external_id and not correlation_lookup_table.has_key((external_id, other_external_id)):
                correlation_lookup_table[(external_id, other_external_id)] = correlation
                correlation_lookup_table[(other_external_id, external_id)] = correlation
                if not external_id in found_external_ids:
                    found_external_ids.add(external_id)                
    return correlation_lookup_table, len(found_external_ids)
            
def parse_correlation_file(file_name, external_ids, spec_header, file_curr_external_id):
    """
    return matrix(float)
    Raises exception if the dimension of the correlation matrix does not
    correspond to that of the volatility vector (expected_dimension)
    """
    log_debug("parse_correlation_file")
    lines = FVaRFileParsing.read_correlation_file(file_name)
    expected_dimension = len(external_ids)
    correlation_lookup_table, dimension = parse_correlation_lines(lines, set(external_ids), spec_header)
    if expected_dimension != dimension:
        err_msg = "Correlation dimension %d "\
                  "!= volatility dimension %d." %\
                  (dimension, expected_dimension)
        log_error(err_msg)
        raise DimensionException(err_msg)
    return correlation_lookup_table

def get_volatility(volatility_pair, risk_type, ir_rf_type):
    """
    TODO:: Add support for FX factor scaling thingy
    """
    try:
        if risk_type == 'Interest Rate' and ir_rf_type == 'Yield':
            return float(volatility_pair[1])
        else:
            return float(volatility_pair[0])
    except Exception as msg:
        log_error(msg)

def get_correlation(correlation_lookup_table, external_id_x, external_id_y, file_curr_external_id):
    if external_id_x == file_curr_external_id or external_id_y == file_curr_external_id:
        return 0.0
    else:
        try:
            return float(correlation_lookup_table[(external_id_x, external_id_y)])
        except Exception as msg:
            log_error(msg)
            
def scale_fx_fx_correlation(vol_x, vol_y, corr_x_y, corr_x_fx_base, corr_y_fx_base, fx_base_vol):
    divisor = math.sqrt(vol_x**2 + fx_base_vol**2 - \
                        2 * corr_x_fx_base * vol_x * fx_base_vol) * \
              math.sqrt(vol_y**2 + fx_base_vol**2 - \
                        2 * corr_y_fx_base * vol_y * fx_base_vol)
    return (fx_base_vol**2 - vol_x *corr_x_fx_base * fx_base_vol - vol_y * corr_y_fx_base * fx_base_vol + vol_x * corr_x_y * vol_y) / divisor

def scale_fx_non_fx_correlation(vol_fx, vol_other, corr_fx_other, corr_fx_fx_base, corr_other_fx_base, fx_base_vol):
    divisor = math.sqrt(vol_fx**2 + fx_base_vol**2 - 2 * corr_fx_fx_base * fx_base_vol * vol_fx)
    return (corr_fx_other * vol_fx - corr_other_fx_base * fx_base_vol) / divisor
    
def rebase_volatilities_and_correlations(ir_rf_type, external_ids, types, unadjusted_volatilities, 
        correlation_lookup_table, fx_base_external_id, fx_base_vol, file_curr_external_id):
    correlation_matrix = acm.FRealMatrix()
    correlation_matrix.Size(len(external_ids), len(external_ids))
    log_debug("Created FRealMatrix of size %s*%s" % \
        (len(external_ids), len(external_ids)))
    volatilities = [] 
    for idx, (external_id_x, risk_type_x) in enumerate(zip(external_ids, types)):
        correlation_matrix.AtPut(idx, idx, 1.0)
        vol_x = get_volatility(unadjusted_volatilities[external_id_x], risk_type_x, ir_rf_type)
        corr_x_fx_base = get_correlation(correlation_lookup_table, external_id_x, fx_base_external_id, file_curr_external_id)
        if risk_type_x == "FX":
            volatilities.append(math.sqrt(vol_x**2 + fx_base_vol**2 - 2 * corr_x_fx_base * fx_base_vol * vol_x))
        else:
            volatilities.append(vol_x)
        for idx2, (external_id_y, risk_type_y) in enumerate(zip(external_ids[idx + 1:], types[idx + 1:])):

            idy = idx + idx2 + 1
            vol_y = get_volatility(unadjusted_volatilities[external_id_y], risk_type_y, ir_rf_type)
            corr_x_y = get_correlation(correlation_lookup_table, external_id_x, external_id_y, file_curr_external_id)
            corr_y_fx_base = get_correlation(correlation_lookup_table, external_id_y, fx_base_external_id, file_curr_external_id)
            if risk_type_x == "FX":
                if risk_type_y == "FX":
                    adjusted_correlation = scale_fx_fx_correlation(vol_x, vol_y, corr_x_y, corr_x_fx_base, corr_y_fx_base, fx_base_vol)
                else:
                    adjusted_correlation = scale_fx_non_fx_correlation(vol_x, vol_y, corr_x_y, corr_x_fx_base, corr_y_fx_base, fx_base_vol)
            elif risk_type_y == "FX":
                if risk_type_x == "FX":
                    adjusted_correlation = scale_fx_fx_correlation(vol_x, vol_y, corr_x_y, corr_x_fx_base, corr_y_fx_base, fx_base_vol)
                else:
                    adjusted_correlation = scale_fx_non_fx_correlation(vol_y, vol_x, corr_x_y, corr_y_fx_base, corr_x_fx_base, fx_base_vol)
            else:
                adjusted_correlation = corr_x_y
            correlation_matrix.AtPut(idx, idy, adjusted_correlation)
            correlation_matrix.AtPut(idy, idx, adjusted_correlation)
    return volatilities, correlation_matrix


def process_volatilities_and_correlations(ir_rf_type, external_ids, types, unadjusted_volatilities, correlation_lookup_table):
    correlation_matrix = acm.FRealMatrix()
    correlation_matrix.Size(len(external_ids), len(external_ids))
    volatilities = acm.FArray()
    for idx, (external_id, risk_type) in enumerate(zip(external_ids, types)):
        volatilities.Add(get_volatility(unadjusted_volatilities[external_id], risk_type, ir_rf_type))
        correlation_matrix.AtPut(idx, idx, 1.0)
        for idx2, external_id_other in enumerate(external_ids[idx + 1:]):
            idy = idx + idx2 + 1
            corr = correlation_lookup_table[(external_id, external_id_other)]
            correlation_matrix.AtPut(idx, idy, corr)
            correlation_matrix.AtPut(idy, idx, corr)
    return volatilities, correlation_matrix
        
CorrVolData = namedtuple("CorrVolData", ["volatilities", "correlation_matrix"])
@acm_perf_log
def parse_parametric_data(correlation_file, unadjusted_volatilities, spec_header, external_ids, risk_types, 
        fx_base_currency, fx_base_currency_volatility, file_curr_external_id):
    """
    main function in this module,
    returns a dictionary with one array containing external ids,
    one array containing corresponding volatilities and
    a correlation matrix.
    TODOT:: Add support for FX Transformations.
    """
    log_debug("parse_parametric_data")
    cross_delimiter = spec_header.CorrelationIdDelimChar()
    log_debug("Using cross delimiter char '%s'" % cross_delimiter)
    delimiter = spec_header.DelimiterChar()
    log_debug("Using delimiter char '%s'" % cross_delimiter)
    ir_rf_type = spec_header.RiskFactorType()
    log_debug("Using ir risk factor type '%s'" % ir_rf_type)
    comment_char = spec_header.CommentChar()
    log_debug("Using comment char '%s'" % comment_char)
    fx_base_external_id = fx_base_currency_volatility[0]
    fx_base_vol = float(fx_base_currency_volatility[1])
    log_debug("Extracted fx base extid '%s' with fx base vol=%s" % \
        (fx_base_external_id, fx_base_vol))
    rebase_values = fx_base_currency != spec_header.VolatilityBaseCurrency()
    if rebase_values:
        log_debug("Rebasing corr/vol")
        ext_ids = list(external_ids)
        if fx_base_external_id:
            ext_ids.append(fx_base_external_id)
        else:
            log_error("FX Base Currency different from volatility base currency")
            log_error("No RiskFactorSpec found for FX Base Currency")
        if file_curr_external_id and fx_base_external_id != file_curr_external_id:
            del ext_ids[ext_ids.index(file_curr_external_id)]
    else:
        ext_ids = external_ids
    correlation_lookup_table = \
        parse_correlation_file(correlation_file, ext_ids, spec_header, file_curr_external_id)
    if rebase_values and fx_base_external_id:
        volatilities, correlations = \
            rebase_volatilities_and_correlations(ir_rf_type, external_ids, risk_types, unadjusted_volatilities,
                correlation_lookup_table, fx_base_external_id, fx_base_vol, file_curr_external_id)
    else:
        volatilities, correlations = \
            process_volatilities_and_correlations(ir_rf_type, external_ids, risk_types, 
                unadjusted_volatilities, correlation_lookup_table)
    
    return CorrVolData(volatilities, correlations)

def parse_scenario_line(raw_text, delimiter):
    """
    Parses a scenario file line into
    TODO: document out format
    """
    pass

