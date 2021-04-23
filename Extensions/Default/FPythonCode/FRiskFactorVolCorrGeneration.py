
import math
import operator
import itertools
import exceptions

from FRiskFactorExtractionUtils import NEWLINE_TOKEN
from FRiskFactorExtractionUtils import RiskFactorDynamicsEnum
import FRiskFactorExtractionUtils
import FRiskFactorScenarioFileGeneration

import FLogger
logger = FLogger.FLogger.GetLogger('FARiskFactorExtraction')

NBR_OF_OBSERVATIONS_KEY = "nbr of observations"
MEAN_KEY = "mean"
ADJUSTED_RETURNS_KEY = "log returns"
VOL_KEY = "volatility"

estimation_methods = ["EWMA", "SMA"]

class DimensionalityError(exceptions.Exception):
    pass

def calc_mean(observations, nbr_of_observations):
    """Calculate the mean of the observations."""
    return sum(observations)/nbr_of_observations
        
def calc_log_returns(rel_returns):
    """Calculate the log returns from the relative returns."""
    return list(map(math.log, rel_returns))
        
def calc_corr(rf1_returns, rf2_returns, rf1_mean_return, rf2_mean_return,
    rf1_stddev, rf2_stddev, rf1_nbr_of_observations, rf2_nbr_of_observations,
    decay_factor=None):
    """
    Calculate the correlations between the rf1 returns and the rf2 returns.
    See table 5.4 in the RiskMetrics Technical Document:
    Exponentially weighted correlation estimator.
    """
    assert rf1_stddev and rf2_stddev
    if decay_factor and not decay_factor <= 1:
        err_msg = "Decay factor must be strictly less than 1: lambda = %s" % \
            decay_factor
        raise ValueError(err_msg)
    if not rf1_nbr_of_observations == rf2_nbr_of_observations:
        err_msg = "Must have same number of observations for both risk factors"\
                  " when calculating correlations: %s != %s" % \
                  (rf1_nbr_of_observations, rf2_nbr_of_observations)
        raise DimensionalityError(err_msg)
    nbr_of_observations = rf1_nbr_of_observations
    assert nbr_of_observations
    
    def kernel(idx, x, y):
        """Closure over rf1_mean_return, rf2_mean_return and decay factor."""
        if decay_factor:
            wdecay = decay_factor**idx
        else:
            wdecay = 1.0
        return wdecay*(x - rf1_mean_return)*(y - rf2_mean_return)
        
    if decay_factor:
        coeff = (1.0 - decay_factor)/(rf1_stddev*rf2_stddev)
    else:
        coeff = 1.0/(nbr_of_observations*rf1_stddev*rf2_stddev)
    return coeff*sum(
        itertools.starmap(
            kernel,
            itertools.izip(
                itertools.count(),
                rf1_returns,
                rf2_returns)))
        
def calc_std_dev(variance):
    return math.sqrt(variance)
        
def calc_vol(returns, mean_return, nbr_of_returns, decay_factor=None):
    """
    Calculate the volatility of the returns. See Table 5.1 in the
    RiskMetrics Technical Document: Exponentially weighted volatility
    estimator or Simple moving average.
    """    
    assert nbr_of_returns
    if decay_factor and not decay_factor <= 1:
        err_msg = "Decay factor must be strictly less than 1: lambda = %s" % \
            decay_factor
        raise ValueError(err_msg)
    def kernel(idx, x):
        """Closure over mean_return and decay."""
        if decay_factor:
            return (decay_factor**(idx))*((x - mean_return)**2)
        else:
            return (x - mean_return)**2
    if decay_factor:
        coeff = (1.0 - decay_factor)
    else:
        coeff = 1.0/nbr_of_returns
    return calc_std_dev(
        coeff*sum(
            itertools.starmap(
                kernel,
                itertools.izip(
                    itertools.count(),
                    returns))))

def write_corr_file(historical_scenarios, ext_id_infos, base_data,
    decay_factor, corr_ostream, cross_delimiter, corr_delimiter):
    """Calculate and write the correlations to file."""
    rf_combs = itertools.combinations(ext_id_infos, 2)
    for (ext_id1, rf_dyn1), (ext_id2, rf_dyn2) in rf_combs:
        rf1_mean = base_data[ext_id1][MEAN_KEY]
        rf2_mean = base_data[ext_id2][MEAN_KEY]
        rf1_nbr_of_observations = base_data[ext_id1][NBR_OF_OBSERVATIONS_KEY]
        rf2_nbr_of_observations = base_data[ext_id2][NBR_OF_OBSERVATIONS_KEY]
        rf1_returns = base_data[ext_id1][ADJUSTED_RETURNS_KEY]
        rf2_returns = base_data[ext_id2][ADJUSTED_RETURNS_KEY]
        rf1_vol = base_data[ext_id1][VOL_KEY]
        rf2_vol = base_data[ext_id2][VOL_KEY]
        
        if rf1_vol and rf2_vol:
            corr = calc_corr(rf1_returns, rf2_returns,
                rf1_mean, rf2_mean, rf1_vol, rf2_vol,
                rf1_nbr_of_observations, rf2_nbr_of_observations, decay_factor)
        else:
            err_msg = "Could not calculate correlation for %s*%s when vols " \
                      "are 0.0. Defaulting to zero correlation" % \
                      (ext_id1, ext_id2)
            logger.ELOG(err_msg)
            corr = 0.0
            
        FRiskFactorExtractionUtils.do_write(
            corr_delimiter.join(
                [cross_delimiter.join(
                    [ext_id1, ext_id2]),
                str(corr)]), corr_ostream)
        FRiskFactorExtractionUtils.do_write(NEWLINE_TOKEN, corr_ostream)
    for ext_id, rf_dynamics in ext_id_infos:
        FRiskFactorExtractionUtils.do_write(
            corr_delimiter.join(
                [cross_delimiter.join(
                    [ext_id, ext_id]),
                str(1.0)]), corr_ostream)
        FRiskFactorExtractionUtils.do_write(NEWLINE_TOKEN, corr_ostream)

def calc_base_data(observations, ext_id, rf_dynamics):
    """Pre-compute some values to avoid unnecessary looping."""
    base_data_per_ext_id = {}
    base_data_per_ext_id[NBR_OF_OBSERVATIONS_KEY] = \
        len(observations)
    if rf_dynamics == RiskFactorDynamicsEnum.GEOMETRIC:
        base_data_per_ext_id[ADJUSTED_RETURNS_KEY] = \
            calc_log_returns(observations)
    else:
        base_data_per_ext_id[ADJUSTED_RETURNS_KEY] = observations
    base_data_per_ext_id[MEAN_KEY] = \
        calc_mean(base_data_per_ext_id[ADJUSTED_RETURNS_KEY],
            base_data_per_ext_id[NBR_OF_OBSERVATIONS_KEY])
    return base_data_per_ext_id

def write_vol_file(historical_scenarios, ext_id_infos, decay_factor,
    vol_ostream, vol_delimiter):
    """Calculate and write vol to file. Returns residual calculations."""
    base_data = {}
    for ext_id, rf_dynamics in ext_id_infos:
        base_data[ext_id] = calc_base_data(historical_scenarios[ext_id],
            ext_id, rf_dynamics)
        vol = calc_vol(base_data[ext_id][ADJUSTED_RETURNS_KEY],
            base_data[ext_id][MEAN_KEY],
            base_data[ext_id][NBR_OF_OBSERVATIONS_KEY], decay_factor)
        base_data[ext_id][VOL_KEY] = vol
        adj_vol = 100*vol
        FRiskFactorExtractionUtils.do_write(
            vol_delimiter.join(
                [ext_id, str(adj_vol)]), vol_ostream)
        FRiskFactorExtractionUtils.do_write(NEWLINE_TOKEN, vol_ostream)
    return base_data

def write_vol_corr_file(historical_scenarios, ext_id_infos, decay_factor,
    vol_ostream, corr_ostream, vol_delimiter, cross_delimiter, corr_delimiter):
    """
    Main function for creating volatility and correlation files from
    historical returns for a risk factor.
    in:
        * historical_scenarios: {"ext_id1" : 
            [return1, return2, ...], ...}
            
        * ext_id_infos: [("ext_id1", RiskFactorDynamicsEnum.GEOMETRIC), 
                         ("ext_id2", RiskFactorDynamicsEnum.ARITHMETIC), ...]
        * Decay weight factor factor for EWMA model
            See section 5.2, RiskMetrics Technical Document
        * vol_ostream: stream to write volatility data to
        * corr_ostream: stream to write correlation data to
        * vol_delimiter: "," -> "ext_id1,0.2642"
        * cross_delimiter: "." ->
        * corr_delimiter: ","  -> "ext_id1.ext_id2,0.73452"
    """
    base_data = write_vol_file(historical_scenarios, ext_id_infos, decay_factor,
        vol_ostream, vol_delimiter)
    write_corr_file(historical_scenarios, ext_id_infos, base_data, decay_factor,
        corr_ostream, cross_delimiter, corr_delimiter)
