"""-----------------------------------------------------------------------
MODULE
    FVaRStaticData - Module with static mapping data.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    TODO: Fill in a nice description

EXTERNAL DEPENDENCIES
    PRIME 2010.1 or later.
-----------------------------------------------------------------------"""

from FVaRPerformanceLogging import log_error
"""
List of currently supported risk factor types.
"""

absolute_scale_factor_mapping = \
    { "Interest Rate" : 0.01,
      "Credit" : 0.01,
      "Volatility" : 0.01,
      "FX" : 1.0,
      "Equity" : 1.0,
      "Commodity" : 1.0 }

supported_risk_factor_types = \
    ( "Credit",
      "Equity",
      "FX",
      "Interest Rate",
      "Volatility",
      "Commodity")

def risk_type_supported(risk_type):
    if risk_type in supported_risk_factor_types:
        return True
    else:
        log_error("Unsupported risk type '%s'" %risk_type)
        return False
        
