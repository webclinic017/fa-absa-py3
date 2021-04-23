
import acm
import itertools
import operator
import math

import FLogger
logger = FLogger.FLogger.GetLogger('FARiskFactorExtraction')
import FRiskFactorFileProcessing
import FRiskFactorExtractionUtils

import FScenarioExportMain
reload (FScenarioExportMain)

from FRiskFactorExtractionUtils import SourceDataInvalidValueError
from FRiskFactorExtractionUtils import NEWLINE_TOKEN
from FRiskFactorExtractionUtils import RiskFactorDynamicsEnum

DATE_ORDER_LAST_TO_FIRST = "LastToFirst"
DATE_ORDER_FIRST_TO_LAST = "FirstToLast"

def create_target_datepair_list(nbr_of_scenarios, end_day, step,
    holding_period, calendar):
    """
    Create a list of calendar adjusted date pairs, one for each shift.
    """
    date_pairs = []
    next_succ_date = calendar.ModifyDate(None, None, end_day, "Preceding")
    next_prec_date = calendar.AdjustBankingDays(next_succ_date, -holding_period)
    for i in range(nbr_of_scenarios):
        date_pairs.insert(0, (next_prec_date, next_succ_date))
        next_succ_date = calendar.AdjustBankingDays(next_succ_date,
            step)
        next_prec_date = calendar.AdjustBankingDays(next_succ_date, -holding_period)
    assert len(date_pairs) == nbr_of_scenarios
    return date_pairs
    
def hist_scenario_add_shifts(rel_shift, abs_shift, shifts, relevant_shifts,
    rf_dynamics, dateorder):
    if rf_dynamics == RiskFactorDynamicsEnum.GEOMETRIC:
        relevant_shift = rel_shift
    else:
        relevant_shift = abs_shift
        
    if dateorder == DATE_ORDER_FIRST_TO_LAST:
        relevant_shifts.insert(0, relevant_shift)
        shifts.append(rel_shift)
        shifts.append(abs_shift)
    else:
        relevant_shifts.insert(0, relevant_shift)
        shifts.insert(0, abs_shift)
        shifts.insert(0, rel_shift)
    return shifts, relevant_shifts
    
def shifts_per_riskfactor(ext_id, rf_dynamics, input_data, target_datepairs, 
    dateorder, labels_token, nbr_of_scenarios):    
    if rf_dynamics == RiskFactorDynamicsEnum.GEOMETRIC:
        last_shift = 1.0
    else:
        last_shift = 0.0
    shifts = []
    relevant_shifts = []
    for idx, (dp1, dp2) in enumerate(target_datepairs):
        try:
            value1 = FRiskFactorExtractionUtils.extract_value_on_date(
                ext_id, dp1, input_data, labels_token, rf_dynamics)
            value2 = FRiskFactorExtractionUtils.extract_value_on_date(
                ext_id, dp2, input_data, labels_token, rf_dynamics)
            if rf_dynamics == RiskFactorDynamicsEnum.GEOMETRIC:
                rel_shift = operator.truediv(value2, value1)
                abs_shift = 0.0
            else:
                rel_shift = 1.0
                abs_shift = value2 - value1
        except FRiskFactorExtractionUtils.SourceDataInvalidValueError as msg:
            err_msg = "Reusing shift for '%s' for dates '%s' and '%s': %s" \
                % (ext_id, dp1, dp2, msg)
            logger.ELOG(err_msg)
            if rf_dynamics == RiskFactorDynamicsEnum.GEOMETRIC:
                rel_shift = last_shift
                abs_shift = 0.0
            else:
                rel_shift = 1.0
                abs_shift = last_shift

        shifts, relevant_shifts = hist_scenario_add_shifts(rel_shift, 
            abs_shift, shifts, relevant_shifts, rf_dynamics, dateorder)
        if idx + 1 == nbr_of_scenarios:
            break
        if rf_dynamics == RiskFactorDynamicsEnum.GEOMETRIC:
            last_shift = rel_shift
        else:
            last_shift = abs_shift
    return shifts, relevant_shifts

def hist_scenario_core(input_data, ext_id_infos, target_datepairs, 
    labels_token, nbr_of_scenarios, delimiter, comment_char,
    dateorder=DATE_ORDER_LAST_TO_FIRST, ostream=None):
    """
    Prime data type independent core implementation of the historical scenario
    generation. Entry point for "offline" unit tests.
    
    In-parameters:
        * input_data: { "*LABELS": ["2006-11-29", ...],
                        ext_id1 : [3.4124, 2.5, ...],
                        ext_id2 : [6.345, 4.43, ...] 
                        ... }
        * ext_id_infos: [(ext_id1, RiskFactorDynamicsEnum.GEOMETRIC),
                         (ext_id2, RiskFactorDynamicsEnum.ARITHMETIC),
                         ... ]
        * target_datepairs: [("2006-11-05", "2006-11-06"),
                             ("2006-11-06", "2006-11-07"),
                             ... ]
        * labels_token: typically "*LABELS"
        * nbr_of_scenarios: the number of scenarios to extract from
            the source time series
        * delimiter: typically ","
        * comment_char: typically "*"
        * dateorder: DATE_ORDER_LAST_TO_FIRST or DATE_ORDER_FIRST_TO_LAST
        * ostream: None or an output stream to write shift results to
    
    Returns a dictionary of the form
        { ext_id1 : [shift, shift, ...],
          ext_id2 : [shift, shift, ...],
          ... }
    """
    #
    # PLEASE, keep the above doc-string up-to-date
    #
    hist_scenarios = {}
    FRiskFactorExtractionUtils.do_write(delimiter.join(
        itertools.chain(
            [labels_token], (d2 for d1, d2 in reversed(target_datepairs)))), ostream)
    FRiskFactorExtractionUtils.do_write(NEWLINE_TOKEN, ostream)
    for ext_id, rf_dynamics in ext_id_infos:
        FRiskFactorExtractionUtils.do_write(ext_id, ostream)
        FRiskFactorExtractionUtils.do_write(delimiter, ostream)
        shifts, relevant_shifts = shifts_per_riskfactor(ext_id, rf_dynamics,
            input_data, target_datepairs, dateorder, labels_token,
            nbr_of_scenarios)
        hist_scenarios[ext_id] = relevant_shifts
        FRiskFactorExtractionUtils.do_write(delimiter.join(
            itertools.imap(str, shifts)), ostream)
        FRiskFactorExtractionUtils.do_write(NEWLINE_TOKEN, ostream)
    return hist_scenarios
        
def hist_scenario(input_data, ext_id_infos, spec_header, calendar, horizon,
    end_day, nbr_of_scenarios, overlapping, delimiter, comment_char, 
    dateorder=DATE_ORDER_LAST_TO_FIRST, ostream=None):
    """
    Main function for historical scenario generation. Writes the output to
    the supplied (memory or file) stream (if present).
    
    Important in-parameters:
        * input_data: { "*LABELS": ["2006-11-29", ...],
                        ext_id1 : [3.4124, 2.5, ...],
                        ext_id2 : [6.345, 4.43, ...] 
                        ... }
        * ext_id_infos: [(ext_id1, RiskFactorDynamicsEnum.GEOMETRIC),
                         (ext_id2, RiskFactorDynamicsEnum.ARITHMETIC),
                         ... ]
        * spec_header: FRiskFactorSpecHeader instance
        * calendar: FCalendar instance
        * horizon: number of days between each scenario
        * end_day: the last observation point to use for returns
        * nbr_of_scenarios: the number of scenarios to extract from
            the source time series
        * overlapping: if horizon > 1, then overlapping == True means
            that the step size going backwards over the dates will be 1
            instead of horizon nbr of days
        * delimiter: typically ","
        * comment_char: typically "*"
        * dateorder: DATE_ORDER_LAST_TO_FIRST or DATE_ORDER_FIRST_TO_LAST
        * ostream: None or an output stream to write shift results to
    
    Returns a dictionary of the form
        { ext_id1 : [shift, shift, ...],
          ext_id2 : [shift, shift, ...],
          ... }
    """
    #
    # PLEASE, keep the above doc-string up-to-date
    #
    if overlapping:
        step = -1
    else:
        step = -horizon
    target_datepairs = create_target_datepair_list(nbr_of_scenarios,
        end_day, step, horizon, calendar)
    labels_token = FRiskFactorFileProcessing.labels_token(comment_char)
    return hist_scenario_core(input_data, ext_id_infos, target_datepairs, 
        labels_token, nbr_of_scenarios, delimiter, comment_char,
        dateorder, ostream)
    
