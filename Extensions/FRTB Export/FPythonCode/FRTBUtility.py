""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBUtility.py"
"""----------------------------------------------------------------------------
MODULE
    FRTBUtility - Misc. helper functions

    (c) Copyright 2016 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import collections
import inspect
import logging
import os

import acm

import FFileUtils
import FLogger
import FScenarioExportUtils
import FRTBSAStaticData

class __Defaults:
    logger = None

__ScenarioDetails = collections.namedtuple(
    'ScenarioDetails', 'start_date end_date column_idx relative_idx'
)

def __getLoggerKwArgsFromAelParams(ael_params):
    # workaround for bug in FLogger which duplicates logging
    log_file = ael_params['Logfile']
    logger_kwargs = {
        'level': int(ael_params['Logmode']),
        'logToConsole': int(ael_params['LogToConsole']) == 1,
        'logToPrime': False,
        'keep': False,
        'logOnce': False,
        'logToFileAtSpecifiedPath': log_file
    }
    return logger_kwargs

def getCaller():
    # Returns the caller of the caller of this method
    # (hence 3rd element in stack)
    frame = inspect.stack()[2]
    return inspect.getmodule(frame[0])

def getAcmDateFromString(string_date, calendar):
    string_date = string_date.strip().upper()
    if string_date == 'TODAY':
        return acm.Time.DateToday()

    if string_date == 'PREVIOUS BANKING DAY':
        return calendar.AdjustBankingDays(acm.Time.DateToday(), -1)

    if string_date == 'FIRST OF MONTH':
        return acm.Time.FirstDayOfMonth(acm.Time.DateToday())

    if string_date == 'FIRST OF QUARTER':
        return acm.Time.FirstDayOfQuarter(acm.Time.DateToday())

    if string_date == 'FIRST OF YEAR':
        return acm.Time.FirstDayOfYear(acm.Time.DateToday())

    acm_date = acm.Get('formats/DateTimeDefault').Parse(string_date)
    if not acm_date:
        try:
            d = int(string_date)
            if d > 0:
                raise ValueError()
        except ValueError:
            msg = (
                'Invalid date (%s). Format is: '
                '  %%Y-%%m-%%d, a period, a negative integer, '
                '  \'Today\', \n e.g. 2001-01-01, -1y, -3m, -20, \'Today\''
            ) % string_date
            raise Exception(msg)
        else:
            acm_date = calendar.AdjustBankingDays(acm.Time.DateToday(), d)

    return acm.Time.AsDate(acm_date)

def getScenarioEndDates(scenario_file, calendar):
    assert os.path.isfile(scenario_file), 'Unable to find file %s' % scenario_file
    first_line = None
    with open(scenario_file, 'r') as fin:
        for line in fin:
            line = line.strip()
            if line:
                first_line = line
                break

    assert first_line, 'Failed to retrieve first line of scenario file'
    assert len(first_line) > 1, 'Failed to retrieve dates from scenario file'
    end_dates = [s.strip() for s in first_line.split(',')[1:]]
    end_dates = [getAcmDateFromString(ed, calendar) for ed in end_dates if ed]
    assert end_dates, 'Unable to convert dates from scenario file'
    return tuple(end_dates)

def getScenarioDetails(scenario_file, first_end_date, last_end_date, horizon, calendar):
    def checkEndDate(end_date, end_dates):
        if end_date not in end_dates:
            msg = 'Expected end date (%s) not present in scenario file: %s' % (
                end_date, scenario_file
            )
            raise AssertionError(msg)

        return

    end_dates = getScenarioEndDates(scenario_file, calendar)
    if first_end_date:
        first_end_date = getAcmDateFromString(first_end_date, calendar)
        checkEndDate(first_end_date, end_dates)

    if last_end_date:
        last_end_date = getAcmDateFromString(last_end_date, calendar)
        checkEndDate(last_end_date, end_dates)

    first_idx = end_dates.index(first_end_date) if first_end_date else 0
    last_idx = end_dates.index(last_end_date) if last_end_date else (len(end_dates) - 1)
    if first_idx > last_idx:
        first_idx, last_idx = last_idx, first_idx

    if (first_end_date and last_end_date) and (first_end_date > last_end_date):
        msg = 'First end date (%s) is not before last end date (%s)' % (
            first_end_date, last_end_date
        )
        raise Exception(msg)

    end_dates = end_dates[first_idx:last_idx + 1]
    all_details = []
    for idx, end_date in enumerate(end_dates):
        start_date = calendar.AdjustBankingDays(end_date, -1 * horizon)
        details = __ScenarioDetails(
            start_date=start_date, end_date=end_date,
            column_idx=first_idx + idx, relative_idx=idx
        )
        all_details.append(details)

    return all_details

def getOutputFilename(
    prefix, filename, dir_path, sub_dir_name,
    create_date_dir, overwrite, max_files=256, ext='csv'
):
    if not filename:
        raise ValueError(' output file not specified')

    output_dir = str(dir_path)
    output_dir = FFileUtils.expandEnvironmentVar(output_dir)
    output_dir = os.path.join(output_dir, sub_dir_name)
    if create_date_dir:
        output_dir = os.path.join(output_dir, acm.Time().DateToday())

    if prefix:
        filename = '{0}_{1}'.format(prefix, filename)

    ext = ext.lstrip('.')
    if not os.path.isdir(output_dir):
        try:
            os.makedirs(output_dir)
        except Exception as e:
            print((str(e)))

    filepath = os.path.join(output_dir, filename) + '.' + ext
    if overwrite or not os.path.exists(filepath):
        return filepath

    for i in range(1, max_files + 1):
        filepath = os.path.join(
            output_dir, '{0}{1}.{2}'.format(filename, i, ext)
        )
        if not os.path.exists(filepath):
            return filepath

    msg = (
        'Maximum no. of %s files found in %s. Please clear '
        'out directory or allow overwrites.'
    ) % (filename, output_dir)
    raise Exception(msg)

def getInputDirectory(dir_path, ref_date, ext):
    dir_path = FFileUtils.expandEnvironmentVar(str(dir_path))
    if not dir_path:
        raise ValueError('Input \'Directory Path\' not specified')

    dir_path = FScenarioExportUtils.get_directory(dir_path, ref_date, bool(ref_date))
    paths = []
    if not os.path.isdir(dir_path):
        raise ValueError('{0} is not a valid directory path'.format(dir_path))

    for fname in os.listdir(dir_path):
        fpath = os.path.join(dir_path, fname)
        if os.path.isfile(fpath):
            if (not ext) or fname.endswith(ext):
                paths.append(fpath)

        return dir_path, tuple(paths)

    msg = 'No files found. Path=%s, Extension=%s' % (dir_path, ext)
    raise Exception(msg)

def getDefaultLogger():
    assert __Defaults.logger, 'Default logger not initialised'
    return __Defaults.logger

def createDefaultLogger(name, ael_params):
    log_dir = os.path.dirname(ael_params['Logfile'])
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    kwargs = __getLoggerKwArgsFromAelParams(ael_params)
    logger = FLogger.FLogger.LOGGERS.get(name)
    if logger:
        logger.Reinitialize(**kwargs)
    else:
        logger = FLogger.FLogger(name=name, **kwargs)

    log_formatter = logging.Formatter('%(asctime)s %(message)s', '%Y-%m-%d %H:%M:%S')
    for handler in logger.Handlers():
        handler.setFormatter(log_formatter)

    __Defaults.logger = logger
    return getDefaultLogger()

def translateHeaderColumnName(headerColumnName, translator):
    retVal = headerColumnName
    translations = FRTBSAStaticData.HeaderTranslators.get(translator)
    if (translations == None):
        return retVal

    translation = translations.get(headerColumnName)
    if (translation == None):
        return retVal

    return translation
