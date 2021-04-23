"""-----------------------------------------------------------------------
MODULE
    FParametricValueAtRiskProcessing - Main entry point for parametric
    value at risk processing.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    TODO: Fill in a nice description

EXTERNAL DEPENDENCIES
    PRIME 2010.1 or later.
-----------------------------------------------------------------------"""

import acm
import exceptions
import FCorrVolProcessing
import FVaRFileParsing
import FADMRiskFactorDescription
import FScenarioGeneration
from FVaRPerformanceLogging import acm_perf_log
from FVaRPerformanceLogging import log_trace, log_debug, log_error

import RiskFactorExtensions


def parametric_value_at_risk_data(spec_header, corr_file_path,
    vol_file_path, fx_base_currency, valuation_parameters,
    valuation_date):
    
    #
    # return ADFL friendly data
    #
    out = acm.FDictionary()
    
    #
    # Generate base data
    #
    vol_data = FCorrVolProcessing.parse_volatility_file(vol_file_path,
        spec_header, fx_base_currency)
    external_ids = list(vol_data.unadjusted_volatilities.keys())
    
    risk_factor_scenario_builder = acm.FRiskFactorScenarioBuilder(
        spec_header, valuation_parameters)
    
    adm_rfds_data = FADMRiskFactorDescription.\
        packed_risk_factor_descriptions_from_external_ids(external_ids,
            risk_factor_scenario_builder)
                                                          
    out.AtPut("externalIds", adm_rfds_data.ordered_external_ids)
    out.AtPut("riskFactorTypes", adm_rfds_data.risk_factor_types)

    #
    # Generate Correlation matrix and adjusted vol vector
    #
    corr_vol_data = FCorrVolProcessing.parse_parametric_data(corr_file_path,
        vol_data.unadjusted_volatilities, spec_header,
        adm_rfds_data.ordered_external_ids, adm_rfds_data.risk_factor_types,
        fx_base_currency, vol_data.fx_base_currency_volatility,
        vol_data.volatility_base_currency_external_id)
        
    out.AtPut("correlationMatrix", corr_vol_data.correlation_matrix)
    out.AtPut("volatilityVector", corr_vol_data.volatilities)
    del corr_vol_data

    #
    # Handle scenario generation
    #
   
    scenarios = FScenarioGeneration.\
        generate_delta_scenarios(adm_rfds_data.adm_risk_factor_descriptions,
            risk_factor_scenario_builder, valuation_date)
    out.AtPut("deltaScenarios", scenarios)
    
    return out
    
def parametric_value_at_risk_delta_vector(spec_header,
    vol_file_path, fx_base_currency, valuation_parameters,
    valuation_date):

    
    #
    # Generate base data
    #
    vol_data = FCorrVolProcessing.parse_volatility_file(vol_file_path,
        spec_header, fx_base_currency)
    external_ids = list(vol_data.unadjusted_volatilities.keys())
    
    risk_factor_scenario_builder = acm.FRiskFactorScenarioBuilder(
        spec_header, valuation_parameters)
    
    adm_rfds_data = FADMRiskFactorDescription.\
        packed_risk_factor_descriptions_from_external_ids(external_ids,
            risk_factor_scenario_builder)

    #
    # Handle scenario generation
    #
   
    scenarios = FScenarioGeneration.\
        generate_delta_scenarios(adm_rfds_data.adm_risk_factor_descriptions,
            risk_factor_scenario_builder, valuation_date)
    
    return scenarios
  
def FilterOutRiskFactorsPerType(riskFactorSpecs, filterType):
    
    if filterType == "Total":
        return riskFactorSpecs
    else:
        filteredRiskFactors = acm.FArray()
        rfCreator = acm.FRiskFactorCreator( riskFactorSpecs[0].Rfspec() )
        rfTypeMatches = acm.GetFunction("riskFactorTypeMatches", 2)
        for rfSpec in riskFactorSpecs:
            rf = rfCreator.RiskFactor( rfSpec )
            if rfTypeMatches(filterType, rf.RiskFactorDescription().RiskFactorType().MappingType()):
                filteredRiskFactors.Add( rfSpec )
        return filteredRiskFactors


def RiskFactorComparatorForParametricValueAtRisk(leftRiskFactorSpec, rightRiskFactorSpec):

    rfCreator = acm.FRiskFactorCreator( leftRiskFactorSpec.Rfspec() )

    leftRiskFactor = rfCreator.RiskFactor(leftRiskFactorSpec)
    rightRiskFactor = rfCreator.RiskFactor(rightRiskFactorSpec) 
    
    leftRiskFactorType = leftRiskFactor.RiskFactorDescription().RiskFactorType()
    rightRiskFactorType = rightRiskFactor.RiskFactorDescription().RiskFactorType()

    # Sort by riskfactor type
    if leftRiskFactorType < rightRiskFactorType:
        return -1
    elif leftRiskFactorType > rightRiskFactorType:
        return 1
    
    leftRiskFactorGroup = leftRiskFactorSpec.Rfg().Name()
    rightRiskFactorGroup = rightRiskFactorSpec.Rfg().Name()
    
    # Sort by riskfactor group
    if leftRiskFactorGroup < rightRiskFactorGroup:
        return -1
    elif leftRiskFactorGroup > rightRiskFactorGroup:
        return 1

    # Sort by coordinate attributes
    for key in RiskFactorExtensions.keyOrderForExternalId:
        leftCoord = leftRiskFactor.RiskFactorDescription().Coordinate(key)
        rightCoord = rightRiskFactor.RiskFactorDescription().Coordinate(key)
        if leftCoord < rightCoord:
            return -1
        elif leftCoord > rightCoord:
            return 1
            
    return 0

