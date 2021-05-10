"""
Python module that contains a wrapper for FLogger. The logger level is set in the FParameter called
LogLevel.

    info     - information
    warn     - warnings
    error    - errors
    debug    - debug information
    critical - critical information
"""

import acm
import FLogger  # pylint: disable=import-error

_logger = None


def GetMandateSettingsParam(parameterName):
    """
    Get a specific parameter config value from LimitsExtensionSettings parameterList.
    :param parameterName: string
    :return: string
    """
    parameterName = parameterName.strip()
    # pylint: disable=no-member
    params = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', 'GenericMandatesSettings')
    if params:
        paramValue = params.Value()[parameterName]
        return paramValue.Text()


def getLoggerLevel():
    """
    Get the log level from FParameter. Set to 1 if it is not set.
    :return: int
    """
    if GetMandateSettingsParam("LogLevel"):
        logLevel = int(GetMandateSettingsParam("LogLevel"))
    else:
        logLevel = 1
    return logLevel


def getLogger():
    """
    Get logger object.
    :return: FLogger
    """
    global _logger  # pylint: disable=global-statement
    if not _logger:
        logLevel = getLoggerLevel()
        _logger = FLogger.FLogger("*Mandate*")
        _logger.Reinitialize(level=logLevel)

    return _logger


def printTraceBack():
    """
    Print the traceback for a specific exception that occurred.
    """
    if getLoggerLevel() >= 1:
        getLogger().error('-'*60)
        import sys
        import traceback
        traceback.print_exc(file=sys.stdout)
        getLogger().error('-'*60)
