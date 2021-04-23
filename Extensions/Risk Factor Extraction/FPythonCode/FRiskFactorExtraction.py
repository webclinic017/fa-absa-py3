"""
"""

import acm
import FRiskFactorExtractionUtils
import importlib
importlib.reload (FRiskFactorExtractionUtils)
import FRiskFactorFileProcessing
importlib.reload (FRiskFactorFileProcessing)
import FRiskFactorValueExtractor
importlib.reload (FRiskFactorValueExtractor)

import FLogger
logger = FLogger.FLogger.GetLogger('FARiskFactorExtraction')

def get_risk_factor_data(variableDictionary):
    today = acm.Time().DateToday()
    spec_header = variableDictionary["header"]

    filename = variableDictionary["File Name"]
    filepath = variableDictionary["File Path"]
    add_values = variableDictionary["add_values"]
    
    delimiter = spec_header.DelimiterChar()
    comment_char = spec_header.CommentChar()
    fx_base_curr = acm.UsedValuationParameters().FxBaseCurrency()
    if not fx_base_curr:
        fx_base_curr = acm.UsedValuationParameters().AccountingCurrency()
        err_msg = "No Fx Base currency set, defaulting to accounting" \
                  " currency '%s'" % fx_base_curr.StringKey()
        logger.LOG(err_msg)
    calendar = variableDictionary["calendar"]
    if not calendar:
        calendar = fx_base_curr.Calendar()
    
    old_values = None
    result = None
    
    """
    parse specified file
    """
    file = FRiskFactorExtractionUtils.get_output_filename_simple(filepath, filename, True, "")
    if file:
        old_values = FRiskFactorFileProcessing.parse_initial_file(file, delimiter)

    if add_values == "True":
        end_date = acm.Time().DateToday()
        if calendar.IsNonBankingDay(None, None, end_date):
            logger.ELOG("'%s' is not a banking day, aborting" % end_date)
            return old_values
                    
        start_date = end_date

        """
        new risk factor values
        """
        dates = [end_date]
        new_values = FRiskFactorValueExtractor.risk_factor_value_per_spec(
                    spec_header, today, fx_base_curr, dates, old_values)
        """
        write the file
        """

        result = FRiskFactorFileProcessing.merge_and_write_results(
                        old_values, new_values, file, comment_char, delimiter)
        return result
    return old_values
