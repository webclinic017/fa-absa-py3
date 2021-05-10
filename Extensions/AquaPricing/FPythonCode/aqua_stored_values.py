"""-----------------------------------------------------------------------------
PURPOSE              :  Functionality to store and retrieve AQUA valuation 
                        parameters to custom text objects.
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer        Description
--------------------------------------------------------------------------------
2019-04-05  CHG1001587723  Libor Svoboda    Use instrument Oid instead of Name
                                            in custom text object name.
"""
import os
import acm


def read_values():
    return os.name != 'nt'


def get_value(name, instrument, date):
    cto_name = 'AQUA_%s_%s_%s' % (name, instrument.Oid(), date)
    cto = acm.FCustomTextObject[cto_name]
    if not cto:
        return 0.0
    try:
        return float(cto.Text())
    except:
        return 0.0


def add_value(name, instrument, value, date):
    cto_name = 'AQUA_%s_%s_%s' % (name, instrument.Oid(), date)
    cto = acm.FCustomTextObject[cto_name]
    if not cto:
        cto = acm.FCustomTextObject()
        cto.Name(cto_name)
        cto.SubType('AQUA')
    try:
        cto.Text(str(value))
        cto.Commit()
    except:
        pass
        

def save_result(result, instrument, date):
    pv = result.At("result").Number()
    delta = result.At("delta").Number()
    gamma = result.At("gamma").Number()
    vega = result.At("vega").Number()
    volga = result.At("volga").Number()
    vanna = result.At("vanna").Number()
    rho = result.At("rho").Number()
    
    add_value('PresentValue', instrument, pv, date)
    add_value('AssetDelta', instrument, delta, date)
    add_value('AssetGamma', instrument, gamma, date)
    add_value('AssetVega', instrument, vega, date)
    add_value('AssetVolga', instrument, volga, date)
    add_value('AssetVanna', instrument, vanna, date)
    add_value('RateDelta', instrument, rho, date)


def get_result_pv(instrument, currency, date):
    pv = get_value('PresentValue', instrument, date)
    
    result = acm.FVariantDictionary()
    result.AtPut("result", acm.DenominatedValue(pv, currency, date))
    return result


def get_result(instrument, currency, date):
    pv = get_value('PresentValue', instrument, date)
    delta = get_value('AssetDelta', instrument, date)
    gamma = get_value('AssetGamma', instrument, date)
    vega = get_value('AssetVega', instrument, date)
    volga = get_value('AssetVolga', instrument, date)
    vanna = get_value('AssetVanna', instrument, date)
    rho = get_value('RateDelta', instrument, date)
    
    result = acm.FVariantDictionary()
    result.AtPut("result", acm.DenominatedValue(pv, currency, date))
    result.AtPut("delta", acm.DenominatedValue(delta, currency, date))
    result.AtPut("gamma", acm.DenominatedValue(gamma, currency, date))
    result.AtPut("vega", acm.DenominatedValue(vega, currency, date))
    result.AtPut("volga", acm.DenominatedValue(volga, currency, date))
    result.AtPut("vanna", acm.DenominatedValue(vanna, currency, date))
    result.AtPut("rho", acm.DenominatedValue(rho, currency, date))
    return result

