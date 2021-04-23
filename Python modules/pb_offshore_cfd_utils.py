"""-----------------------------------------------------------------------------
Utility functions for prime broking offshore trading.

HISTORY
================================================================================
Date           Developer          Description
--------------------------------------------------------------------------------
2020-11-20     Marcus Ambrose     Implemented
2021-02-24     Marcus Ambrose     Added get_fa_date() and str_to_float
-----------------------------------------------------------------------------"""
import csv
import datetime

import acm

WEEKEND_DAYS = ("Saturday", "Sunday")


def csv_dict_list(variables_file):
    reader = csv.DictReader(open(variables_file, "rb"))
    dict_list = []
    for line in reader:
        dict_list.append(line)

    return dict_list


def get_fx_rate(curr_from, curr_to, input_date):
    calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()

    if curr_from == curr_to:
        return 1.0

    from_curr = acm.FCurrency[curr_from]
    to_curr = acm.FCurrency[curr_to]
    input_date = input_date.replace("-", "/")

    try:
        return from_curr.Calculation().FXRate(calc_space, to_curr, input_date).Number()
    except Exception:
        raise Exception(
            "Could not find fx rate for {} and {} on {}".format(
                curr_from, curr_to, input_date
            )
        )


def get_time_series_spec(field_name, broker):
    spec = acm.FTimeSeriesSpec[field_name]
    if not spec:
        spec = acm.FTimeSeriesSpec()
        spec.Description("{} PnL History".format(broker))
        spec.FieldName(field_name)
        spec.RecType(acm.EnumFromString("B92RecordType", "Instrument"))
        spec.Commit()
    return spec


def get_previous_weekday(given_date):
    for day_delta in range(-1, -4, -1):
        prev_date = acm.Time.DateAddDelta(given_date, 0, 0, day_delta)
        prev_day = acm.Time.DayOfWeek(prev_date)

        if prev_day not in WEEKEND_DAYS:
            return prev_date


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_workdays_from_range(start_date, end_date):
    workdays = []

    num_days = acm.Time.DateDifference(end_date, start_date) + 1

    for days_to_add in range(num_days):
        sweep_date = acm.Time.DateAddDelta(start_date, 0, 0, days_to_add)
        if not acm.Time.DayOfWeek(sweep_date) in WEEKEND_DAYS:
            workdays.append(sweep_date)

    return workdays


def get_fa_date(date_to_format, source_format, fa_date_format=None):
    if not fa_date_format:
        fa_date_format = "%Y-%m-%d"

    if date_to_format:
        try:
            datetime.datetime.strptime(date_to_format, fa_date_format)
            return date_to_format
        except:
            try:
                d = datetime.datetime.strptime(date_to_format, source_format)
                return d.strftime(fa_date_format)
            except:
                raise ValueError("Unexpected date format: {}".format(date_to_format))


def str_to_float(val):
    try:
        return float(val)
    except ValueError:
        return float(val.replace(",", "")) if val != "" else 0
