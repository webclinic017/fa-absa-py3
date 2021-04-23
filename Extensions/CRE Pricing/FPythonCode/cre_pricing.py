"""----------------------------------------------------------------------------
PROJECT                 :  CRE into Front Arena
PURPOSE                 :  This module implements custom valuation and risk
                           functions based on values obtained from CRE.
DEPATMENT AND DESK      :  Middle Office, FX Trading
DEVELOPER               :  Libor Svoboda
CR NUMBER               :  CHNG0003040071
-------------------------------------------------------------------------------

HISTORY
===============================================================================
Date        Change no     Developer         Description
-------------------------------------------------------------------------------
18/02/2018  CHG1000032049 Libor Svoboda     Updated time series selection.

"""
import acm


REQUIRED_TIME_SERIES = ('CRE_TheorVal',)
CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()


def get_fx_rate(date, orig_curr, new_curr):
    """Return FX rate (denominated value) between two currencies.
    
    Arguments:
        date - FX rate date
        orig_curr - original currency
        new_curr - new currency
    """
    return orig_curr.Calculation().FXRate(CALC_SPACE, new_curr, date)


def get_time_series_values(ts_name, recaddr1, date):
    ts_spec = acm.FTimeSeriesDvSpec[ts_name]
    if ts_spec:
        query = "timeSeriesDvSpecification=%s and recordAddress1=%s and storageDate<='%s'" % (
                    ts_spec.Oid(), recaddr1, date)
        ts = acm.FTimeSeriesDv.Select(query)
        ts = ts.SortByProperty('StorageDate', True)
        return ts
    return None


def convert_value(dv, new_curr):
    """Convert denominated value to a different currency.
    
    Arguments:
        dv - denominated value
        new_curr - new currency
    
    Raises:
        CREPricingError if dv contains no currency or datetime
    """
    if not dv.Unit():
        error_msg = "Denominated value '%s' contains no currency." % dv
        raise CREPricingError(error_msg)
    
    if not dv.DateTime():
        error_msg = "Denominated value '%s' contains no datetime." % dv
        raise CREPricingError(error_msg)
    
    orig_curr = acm.FCurrency[dv.Unit().Text()]
    if orig_curr == new_curr:
        return dv
    
    fx_rate = get_fx_rate(dv.DateTime(), orig_curr, new_curr)
    return dv * fx_rate


def get_ts_value(ts_name, instrument, date):
    """Return time series denominated value.
    
    Arguments:
        ts_name - time series dv spec name
        instrument - instrument linked to time series (table 1)
        date - time series storage date
    
    Raises:
        CREPricingError if requested time series value does not exist
    """
    try:
        ts = get_time_series_values(ts_name, instrument.Oid(), date)[-1]
    except (IndexError, TypeError):
        if ts_name not in REQUIRED_TIME_SERIES:
            return acm.DenominatedValue(0, instrument.Currency().Name(), date)
        
        error_msg = ("No value for instrument '%s' and date '%s'. CRE might "
                     "not support pricing of this instrument or it has not "
                     "been calculated yet." 
                     % (instrument.Name(), date))
        raise CREPricingError(error_msg)
    
    dv = ts.DenominatedValue()
    dv_date = dv.DateTime()[:10]
    if not date == dv_date:
        print('WARNING: CRE value not calculated for %s, using latest value for %s.' % (date, dv_date))
        dv = acm.DenominatedValue(dv.Number(), dv.Unit(), date)
    return dv


def get_and_convert_value(ts_name, instrument, date, new_curr):
    """Get ts value and convert it to a different currency.
    
    Arguments:
        ts_name - time series dv spec name
        instrument - instrument linked to time series (table 1)
        date - time series storage date
    """
    dv = get_ts_value(ts_name, instrument, date)
    return convert_value(dv, new_curr)


def get_and_adjust_value(ts_name, instrument, date, fx_date, currency):
    """Get ts value and adjust it to CRE spot rate.
    
    Arguments:
        ts_name - time series dv spec name
        instrument - instrument linked to time series (table 1)
        date - time series storage date
        fx_date - underlying FX spot date
        currency - underlying currency
    
    Raises:
        CREPricingError if dv contains no currency
    """
    dv = get_ts_value(ts_name, instrument, date)
    if not dv.Unit():
        error_msg = "Denominated value '%s' contains no currency." % dv
        raise CREPricingError(error_msg)

    spot_rate = get_ts_value('CRE_Spot', instrument, date)
    if not spot_rate.Number():
        return dv
    
    fx_rate = get_fx_rate(fx_date, acm.FCurrency[dv.Unit().Text()], currency)
    adjustment_factor = spot_rate.Number() / fx_rate.Number()
    return dv * adjustment_factor
    

def theor_model_FI(ins, val_date, discount_curve, vol_info, version):
    """Return CRE figures for a fixed income instrument.
    
    Arguments:
        ins - fixed income instrument
        val_date - valuation date
        discount_curve - discount curve
        vol_info - volatility information
        version - time series version (re-calculation trigger)
    """
    arg_position = {
        'val_date': 1,
        'discount_curve': 2,
        'vol_info': 3,
    }
    
    # Get storage consistent parent object
    ins = acm.FInstrument[ins.Name()]
    currency = ins.Currency()
    
    theor_val_num = get_ts_value('CRE_TheorVal', ins, val_date).Number()
    # Add currency 
    theor_val = acm.DenominatedValue(theor_val_num, currency.Name(), val_date)
    delta = get_ts_value('CRE_IRDelta', ins, val_date)
    gamma = get_ts_value('CRE_IRGamma', ins, val_date)
    vega = get_ts_value('CRE_Vega', ins, val_date)

    result = acm.FVariantDictionary()
    result.AtPut('result', theor_val)
    result.AtPut('delta', delta)
    result.AtPut('gamma', gamma)
    result.AtPut('vega', vega)
    result.AtPut('arg_position', arg_position)
    return result


def risk_function_FI(model, model_output, original_input, shifted_input):
    """Calculate risk for a fixed income instrument.
    
    Arguments:
        model - custom function mapped to theor_model_FI
        model_output - output of theor_model_FI
        original_input - input of theor_model_FI
        shifted_input - shifted input of theor_model_FI
    """
    theor_val = model_output.At('result')
    delta = model_output.At('delta')
    gamma = model_output.At('gamma')
    vega = model_output.At('vega')
    pos = model_output.At('arg_position')
    
    output_date = shifted_input[pos['val_date']]
    output_unit = theor_val.Unit()
    vol_info_shift = shifted_input[pos['vol_info']].Shifts()

    try:
        disc_rate_shift = shifted_input[pos['discount_curve']].AbsoluteShift()
    except:
        disc_rate_shift = None
    
    # Order of conditions matters
    if disc_rate_shift:
        output_val = theor_val.Number() + delta.Number() / 1e3
        if shifted_input[pos['discount_curve']].UnderlyingShift():
            output_val += delta.Number() / 1e3 + gamma.Number() / 1e6
    elif vol_info_shift > 0:
        output_val = theor_val.Number() + vega.Number() * vol_info_shift * 1e2
    else:
        return model_output
    
    result = acm.FVariantDictionary()
    result.AtPut('result', acm.DenominatedValue(output_val, 
                                                output_unit,
                                                output_date))
    return result


def theor_model_FX(ins, strike_currency, val_date, under_fx_spot_date,
                   under_val, vol_val_model, discount_curve, vol_info, version):
    """Return CRE figures for a FX instrument.
    
    Arguments:
        ins - FX instrument
        strike_currency - strike currency
        val_date - valuation date
        under_fx_spot_date - underlying FX spot date
        under_val - underlying value
        vol_val_model - volatility value model
        discount_curve - discount curve
        vol_info - volatility information
        version - time series version (re-calculation trigger)
    """
    arg_position = {
        'val_date': 2,
        'under_val': 4,
        'vol_val_model': 5,
        'discount_curve': 6,
        'vol_info': 7,
    }
    
    # Get storage consistent parent object
    ins = acm.FInstrument[ins.Name()]

    theor_val = get_and_convert_value('CRE_TheorVal', ins,
                                      val_date, strike_currency)
    delta = get_and_adjust_value('CRE_Delta', ins, val_date,
                                 under_fx_spot_date, strike_currency)
    gamma = (get_and_convert_value('CRE_Gamma', ins, val_date, strike_currency)
             / (under_val.Number() * under_val.Number()))
    vega = get_and_convert_value('CRE_Vega', ins, val_date, strike_currency)
    rho = get_and_convert_value('CRE_IRDelta', ins, val_date, strike_currency)
    
    result = acm.FVariantDictionary()
    result.AtPut('result', theor_val)
    result.AtPut('delta', delta)
    result.AtPut('gamma', gamma)
    result.AtPut('vega', vega)
    result.AtPut('rho', rho)
    result.AtPut('arg_position', arg_position)
    return result


def risk_function_FX(model, model_output, original_input, shifted_input):
    """Calculate risk for a FX instrument.
    
    Arguments:
        model - custom function mapped to theor_model_FX
        model_output - output of theor_model_FX
        original_input - input of theor_model_FX
        shifted_input - shifted input of theor_model_FX
    """
    theor_val = model_output.At('result')
    delta = model_output.At('delta')
    gamma = model_output.At('gamma')
    vega = model_output.At('vega')
    rho = model_output.At('rho')
    pos = model_output.At('arg_position')

    output_date = shifted_input[pos['val_date']]
    output_unit = theor_val.Unit()
    
    price_shift = (shifted_input[pos['under_val']].Number()
                   - original_input[pos['under_val']].Number())
    vol_shift = (shifted_input[pos['vol_val_model']]
                 - original_input[pos['vol_val_model']])
    vol_info_shift = shifted_input[pos['vol_info']].Shifts()
    
    try:
        disc_rate_shift = shifted_input[pos['discount_curve']].AbsoluteShift()
    except:
        disc_rate_shift = None
    
    # Order of conditions matters
    if disc_rate_shift:
        output_val = theor_val.Number() + rho.Number() / 1e3
        if shifted_input[pos['discount_curve']].UnderlyingShift():
            output_val += rho.Number() / 1e3
    elif price_shift and vol_shift:
        output_val = (theor_val.Number() +
                      delta.Number() * price_shift +
                      gamma.Number() * price_shift * price_shift / 2.0 + 
                      vega.Number() * vol_info_shift * 1e2)
    elif price_shift:
        output_val = (theor_val.Number() +
                      delta.Number() * price_shift +
                      gamma.Number() * price_shift * price_shift / 2.0)
    elif vol_shift:
        output_val = theor_val.Number() + vega.Number() * vol_shift * 1e2
    else:
        return model_output
    
    result = acm.FVariantDictionary()
    result.AtPut('result', acm.DenominatedValue(output_val,
                                                output_unit,
                                                output_date))
    return result


class CREPricingError(Exception):
    """Custom CRE Pricing exception."""
    pass
