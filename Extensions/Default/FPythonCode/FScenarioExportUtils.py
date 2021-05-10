""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportUtils.py"
import os.path


import acm
import FFileUtils

PROFIT_AND_LOSS_MEASURE_LABEL = "TOTAL"
STD_CALC_PARAM_DISPLAY_CURR = "currency"
STD_CALC_PARAM_START_DATE = "startDate"
STD_CALC_PARAM_END_DATE = "endDate"

SCENARIO_COUNT = "scenariocount"
SCENARIO_EXPORT_EXT = ".dat"
MAX_FILES_IN_DIR = 256

risk_factor_type_labels_map = {"None": "Total"}
risk_factor_type_map = {"Total": "None"}


def convert_risk_type(risk_type):
    if risk_type in risk_factor_type_map:
        return risk_factor_type_map[risk_type]
    else:
        return risk_type


def convert_risk_types(risk_types):
    out = []
    for risk_type in risk_types:
        out.append(convert_risk_type(risk_type))
    return out


def incl_in_residual_dict(risk_types_incl):
    out = {}
    all_risk_types = acm.FEnumeration["EnumRiskFactorTypes"].Values()
    all_risk_types = convert_risk_types(all_risk_types)
    for risk_type in all_risk_types:
        if risk_type in risk_types_incl:
            value = 1
        else:
            value = 0
        out[risk_type] = value
    return out


def is_date(strdate):
    try:
        return acm.Time().IsValidDateTime(strdate)
    except RuntimeError:
        return False


def adjust_date(date, base_date, calendar, bdmethod):
    strdate = str(date).strip()
    if strdate.upper() == "TODAY":
        day = acm.Time.DateToday()
    elif is_date(strdate):
        day = strdate
    else:
        try:
            day = acm.Time().PeriodSymbolToRebasedDate(strdate, base_date)
            if not day:
                raise ValueError("")
        except:
            raise ValueError("Date must be either a date,"
                             " 'TODAY' or a dateperiod, not %s" % strdate)
    return calendar.ModifyDate(None, None, day, bdmethod)


def adjust_ref_date(ref_date, calendar):
    return adjust_date(ref_date, acm.Time().DateToday(),
        calendar, "Preceding")


def get_end_date(start_date, calendar, horizon):
    return adjust_date(horizon, start_date, calendar, "Following")


def get_unique_file_name(out_dir, name, ext):
    for i in range(1, MAX_FILES_IN_DIR + 1):
        if i == 1:
            numbering = ""
        else:
            numbering = "_" + str(i)
        test_file = os.path.join(out_dir, name + numbering + ext)
        if not os.path.exists(test_file):
            return test_file
    msg = "Could not create file"
    raise IOError(msg)


def get_output_file_name(out_dir, file_name, overwrite, is_count_file):
    f = file_name
    if is_count_file:
        f = f + "_" + SCENARIO_COUNT
    if overwrite:
        return os.path.join(out_dir, f + SCENARIO_EXPORT_EXT)
    else:
        return get_unique_file_name(out_dir, f, SCENARIO_EXPORT_EXT)


def create_directory(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        return True
    return False


def get_directory(dir_path, reference_date, date_directory):
    if date_directory:
        dir_path = os.path.join(dir_path, reference_date)
    dir_path = FFileUtils.expandEnvironmentVar(dir_path)
    return dir_path
