"""-----------------------------------------------------------------------
MODULE
    FScenarioGeneration - Process shift data and risk factor descriptions and 
    generate scenarios.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    TODO: Fill in a nice description

EXTERNAL DEPENDENCIES
    PRIME 2010.1 or later.
-----------------------------------------------------------------------"""

import acm
import os.path
from FVaRPerformanceLogging import acm_perf_log
from FVaRPerformanceLogging import log_trace, log_debug, log_error, log_trace_object

@acm_perf_log
def generate_delta_scenarios(risk_factor_descriptions,
    risk_factor_scenario_builder, valuation_date):
    """
    TODO: correct description
    """
    delta_scenarios = acm.FArray()
    delta_shift = [1.000001, 0.000001]
    for stacked_containers in risk_factor_descriptions:
        explicit_scenario = acm.FExplicitScenario()
        log_debug("Created FExplicitScenario")
        dimension = explicit_scenario.CreateAndAddDimension()
        log_debug("Created and added dimension to explicit scenario")
        names = []
        for rf_container in stacked_containers:
            is_arithmetic = rf_container.IsArithmetic()
            dimension.AddShiftVector(risk_factor_scenario_builder.CreateShiftVector(
                rf_container,
                is_arithmetic and 1.0 or delta_shift[0],
                is_arithmetic and delta_shift[1] or 0.0))
        explicit_scenario.Name(",".join(names))
        delta_scenarios.Add(explicit_scenario)
    return delta_scenarios
