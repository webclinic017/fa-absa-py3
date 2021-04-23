import acm
import exceptions

import FLogger
logger = FLogger.FLogger.GetLogger('FARiskFactorExtraction')

"""
    FRiskFactorFileProcessing
"""

LABELS_TOKEN = "LABELS"

class RiskFactorExtractionError(exceptions.Exception):
    pass

def labels_token(comment_char):
    return comment_char + LABELS_TOKEN

def parse_initial_file(file_name, delimiter):
    try:
        istream = open(file_name, "r")
        lines = istream.readlines()
        out = {}
        for line in lines:
            line = line[:-1]
            components = line.split(delimiter)
            out[components[0]] = components[1:]
        istream.close()
        return out
    except:
        return None
        
def merge_dates(old_dates, new_dates):
    for new_date in new_dates:
        if not new_date in old_dates:
            old_dates.append(new_date)
    return old_dates

def date_compare(date1, date2):
    return acm.Time().DateDifference(date1, date2)

def join_dates_sorted(old_dates, new_dates):
    result_dates = [date for date in old_dates]
    result_dates.extend(new_dates)
    result_dates = sorted(set(result_dates), cmp=date_compare)
    return result_dates
    
def assemble_result_values(result_dates, old_dates, new_dates, 
    old_results, new_results):
    """
    New values overwrites old values.
    """
    assert len(old_dates) == len(old_results)
    assert len(new_dates) == len(new_results)
    result_values = []
    for date in result_dates:
        if date in new_dates:
            value = new_results[new_dates.index(date)]
        elif date in old_dates:
            value = old_results[old_dates.index(date)]
        else:
            err_msg = "Date '%s' not in old file dates "\
                      "or in the new date range" % date
            logger.ELOG(err_msg)
            raise RiskFactorExtractionError(err_msg)
        result_values.append(value)
    return result_values

def merge_results(old_result, new_result, labels_tag):
    if not old_result and not new_result:
        err_msg ="Must either specify an initial risk factor file "\
                 "or give start and end dates to generate new raw "\
                 "risk factor data"
        raise RiskFactorExtractionError(err_msg)
    if not old_result:
        return new_result
    if not new_result:
        return old_result
    if not len(list(old_result.keys())) == len(list(new_result.keys())):
        err_msg = "Nbr of risk factors in file = %s != nbr of risk factors in "\
                  "new result = %s" % (str(len(list(old_result.keys()))), 
                                       str(len(list(new_result.keys()))))
        logger.ELOG(err_msg)
        raise RiskFactorExtractionError(err_msg)
    old_dates = old_result[labels_tag]
    new_dates = new_result[labels_tag]
    dates = join_dates_sorted(old_dates, new_dates)
    result = {labels_tag : dates}
    for key in new_result:
        if key == labels_tag:
            continue
        if not key in old_result:
            err_msg = "'%s' is not present in the original file" % key
            logger.ELOG(err_msg)
            raise RiskFactorExtractionError(err_msg)
        result[key] = assemble_result_values(dates, old_dates, new_dates,
            old_result[key], new_result[key])
    return result

def write_line(label, values, delimiter, ostream):
    ostream.write(label)
    for value in values:
        ostream.write(delimiter + str(value))
    ostream.write("\n")
    
def write_file(results, ostream, delimiter, labels_tag):
    dates = []
    write_line(labels_tag, results[labels_tag], delimiter, ostream)
    for label in list(results.keys()):
        if not label == labels_tag:
            values = results[label]
            write_line(label, values, delimiter, ostream)

def merge_and_write_results(old_values, result, file_path, comment_char, delimiter):
    labels_tag = labels_token(comment_char)
    merged_results = merge_results(old_values, result, labels_tag)
    ostream = open(file_path, "w")
    write_file(merged_results, ostream, delimiter, labels_tag)
    ostream.close()
    return merged_results
