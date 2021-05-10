"""-----------------------------------------------------------------------
MODULE
    FVaRFileParsing - Parse Scenario Files based on the
    Risk Metrics file format.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    TODO: Fill in a nice description

EXTERNAL DEPENDENCIES
    PRIME 2010.1 or later.
-----------------------------------------------------------------------"""
import sys
import os
import array

import acm

from FVaRPerformanceLogging import log_trace, log_debug, log_error

LABELS_TOKEN = "LABELS"

def is_file_path(fpath):
    log_trace("Checking '%s'" % fpath)
    return os.path.dirname(fpath) != ""

def read_correlation_file(correlation_path):
    """
    Reads a correlation file and returns a
    list of strings
    """
    try:
        log_debug("Trying to open file '%s'" % correlation_path)
        file_handle = open(correlation_path, "r")
    except Exception as msg:
        raise IOError("Could not open correlation file at %s: %s" % (correlation_path, msg))
    return [line.strip() for line in file_handle.readlines() if line.strip()]

def read_volatility_file(volatility_file):
    """
    Reads a volatility file and returns a
    list of strings
    """
    try:
        log_debug("Trying to open file '%s'" % volatility_file)
        file_handle = open(volatility_file, "r")
    except Exception as msg:
        err_msg = "Could not open volatility file at %s: %s" % (volatility_file, msg)
        log_error(err_msg)
        raise IOError(err_msg)
    return [line.strip() for line in file_handle.readlines() if line.strip()]


def merge_path_and_filename(path, filename):
    log_debug("Trying to merge '%s' and '%s'" % (path, filename))
    res = ""
    if path == "":
        path = os.getcwd()
        log_debug("Fallback to cwd '%s'" % path)
    try:
        res = os.path.join(path, filename)
        log_debug("Merged '%s' + '%s' to '%s'" % (path, filename, res))
    except Exception as msg:
        err_msg = "Could not merge path %s and filenam %s: %s" %\
            (path, filename, msg)
        log_error(err_msg)
        raise IOError(err_msg)
    return acm.FSymbol(res)

def file_with_path(file):
    fileWithPath = file
    if not is_file_path(fileWithPath):
        riskDir = acm.GetConfigVar('FCS_DIR_RISK')
        if not riskDir:
            riskDir = ''
        else:
            riskDir = str(riskDir)
        fileWithPath = str(merge_path_and_filename(riskDir, fileWithPath))
    return fileWithPath

def create_scenario_file_data(file, delimiterChar, commentChar):
    fileWithPath = file_with_path(file)
    return acm.Risk().CreateScenarioFileData(fileWithPath, delimiterChar, commentChar)

def scenario_file_data(file):
    specHeader = acm.Risk().MappedRiskFactorSpecHeader().Parameter()
    return create_scenario_file_data(file, specHeader.DelimiterChar(), specHeader.CommentChar())
