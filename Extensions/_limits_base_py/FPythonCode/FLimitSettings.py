""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitSettings.py"
"""--------------------------------------------------------------------------
MODULE
    FLimitSettings

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    A centralised module for accessing all limits configuration settings.

    NOTE: Unless explicitly defined, functions for accessing settings are
          dynamically generated at module import time. 
          
          New settings may be introduced by adding them to the _SETTINGS 
          dictionary with a default value and will be overridden by the 
          corresponding FParameter setting (if set) at runtime.

-----------------------------------------------------------------------------"""
import string   # pylint: disable-msg=W0402
import sys

import acm
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()


_FPARAMETER_NAMES = ['FLimitSettings', 'FLimitReportSettings']
_SETTINGS = {
    # FParameter/Method name => default value
    #ReportSettings:
    'Date In File Name Beginning': True,
    'Dir Name Date Format': '',
    'File Name Date Format': '',
    'Maximum Reports In Path': 1000,
    'Overwrite': False,
    'Report Columns': '',
    'Report Dir': r'C:\temp\Limits',
    'Report Grouper': 'Checked State / Limit Split',
    'Report Name': 'Limit Report',
    'Sub Dir Name': 'Limit Checks',
    'Storage': 'File',
    #Other Settings:
    'Calculation Environment': '',
    'Create Standard Default State Chart': True,
    'Default Transform Function': 'Value',
    'Default Display Columns': ('Limit Status',
                                'Limit Current State',
                                'Limit Checked Value',
                                'Limit Comparison Operator',
                                'Limit Warning Value',
                                'Limit Threshold',
                                'Limit Availability',
                                'Limit Path Short',
                                'Limit Column ID'),
    'Default Limit Specification Name': '',
    'Default Limit Template Module': '',
    'Default Pre Deal Check Filter': 'my',
    'Default Realtime Monitored': True,
    'Default State Chart': 'Limits',
    'Default Percentage Warning': False,
    'Default Warning Percentage Value': 0,
    'Enable Pre Deal Check': True,
    'Notification Sender Address': 'noreply.limits@frontarena.com',
    'Notification SMTP Server': '',
    'Notification SMTP Timeout': 60,
    'Pre Deal Check Type': 'None',
    'Pre Deal Check Visibility Hook': '',
    'Server Invalid Limit Check Period': 60,
    'Server Logging Level': 'Info',
    'Server Write Limit Values': True,
    'Use Distributed Calculations': False,
    'Workbench Auto Expand Rows': True,
    'Workbench Auto Expand Exclude': ('Ready', 'Active', 'Inactive'),
    'Workbench Comment On Actions': ('Investigate', 'Breach Accepted', 'Deactivate'),
    'Workbench Grouper': 'Current State',
    'Workbench Sheet Template': '',
    }
    
_SETTING_CHOICES = {
    # FParameter name => list of valid choices (lower-case)
    'Default Pre Deal Check Filter': ['all', 'my', 'spec', 'type', 'query'],
    'Pre Deal Check Type': ['none', 'local'],
    'Storage': ['file', 'ads']
    }


def CachedParameter(function):
    # Decorator for caching a parameter value. The user must restart Prime / ATS
    # for a changed parameter value to be used after it is first read.
    cache = {}
    def wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            value = function(*args)
            cache[args] = value
            return value
    return wrapper

def LogLimitSettings():
    """Logs the current value of all limit configuration settings."""
    logger.info('Using limit configuration settings:')
    module = sys.modules[__name__]
    for param in sorted(_SETTINGS.keys()):
        paramValueFunc = getattr(module, _FunctionNameForParameter(param))
        value = paramValueFunc()
        logger.info('\t%s = %s', param, value.Name() if hasattr(value, 'Name') else value)

def ServerLoggingLevel():
    # Allow specification of the logging level as a string (e.g. info/warn/error)
    parameter = 'Server Logging Level'
    try:
        level = _GetParameterValue(parameter)
        if level:
            # FLogger logging levels:
            # Error => 4, Warning => 3, Debug/Verbose => 2, Info/Normal/Default => 1
            log_levels = {'e': 4, 'w': 3, 'd': 2, 'v': 2}
            return log_levels.get(level.lower()[0], 1)
    except KeyError:
        pass
    return _SETTINGS[parameter]

def PreDealCheckVisibilityHook():
    parameter = 'Pre Deal Check Visibility Hook'
    try:
        hookName = _GetParameterValue(parameter)
        if hookName:
            try:
                hook = FAssetManagementUtils.GetFunction(hookName)
                if not hook:
                    logger.warn('Failed to load limit hook function "%s"', hookName)
                return hook
            except ValueError:
                logger.error('Invalid limit hook definition "%s" ' \
                    '(must be in format "<module>.<function>")', hookName)
    except KeyError:
        pass
    return None

@CachedParameter
def UseDistributedCalculations():
    # Use a specialised search order for this setting:
    #   1. The FParameter setting, if set
    #   2. The users 'Use Distribution As Default' configuration, if set
    #   3. The default value
    parameter = 'Use Distributed Calculations'
    try:
        value = _ParameterValueFromExtension(parameter)
        if value is None:
            raise KeyError
        return value
    except KeyError:
        return (_GetUserConfigParameterValue('useDistributionAsDefault') == 'Yes')
    return _SETTINGS[parameter]

@CachedParameter
def CalculationEnvironment():
    parameter = 'Calculation Environment'
    calcEnvName = None
    try:
        calcEnvName = _ParameterValueFromExtension(parameter)
        if not calcEnvName:
            raise KeyError
    except KeyError:
        calcEnvName = _GetUserConfigParameterValue('defaultCalculationEnvironment')
    if calcEnvName:
        return acm.FStoredCalculationEnvironment[calcEnvName]


def _FunctionNameForParameter(parameterName):
    return parameterName.translate(None, string.punctuation + ' ')

def _ExtensionParameters():
    settings = acm.FDefinition()
    for paramName in _FPARAMETER_NAMES:
        param = acm.GetDefaultContext().GetExtension( \
            'FParameters', 'FObject', paramName)
        if param:
            settings.AddAll(param.Value())
    return settings
            
def _ParameterValueFromExtension(parameter):
    assert parameter in _SETTINGS
    value = None
    extensionParams = _ExtensionParameters()
    if extensionParams:
        if extensionParams.At(parameter):
            attributeType = type(_SETTINGS[parameter])
            try:
                if attributeType in (list, tuple):
                    value = [str(s).strip() for s in extensionParams.GetArray(parameter)]
                elif attributeType in (int, float):
                    value = extensionParams.GetNumber(parameter)
                elif attributeType == bool:
                    value = extensionParams.GetBool(parameter)
                else:
                    value = str(extensionParams.GetString(parameter)).strip()
            except RuntimeError as e:
                logger.error('Invalid FParameter value for "%s": %s', parameter, e)
    if value is None:
        raise KeyError('No FParameter for key "' + parameter + '"')
    return value

def _GetParameterValue(parameter):
    try:
        value = _ParameterValueFromExtension(parameter)
        return _ValidateParameterValue(parameter, value)
    except KeyError:
        pass
    return _SETTINGS[parameter]

def _GetUserConfigParameterValue(parameter):
    group = acm.UserGroup()
    userHierarchy = (
        ('user', acm.UserName()),
        ('group', group.Name()),
        ('organisation', group.Organisation().Name()),
        )
    for level, value in userHierarchy:
        configParams = acm.FConfigurationParameter.Select(level + ' = ' + value)
        if configParams:
            for param in configParams:
                if param.Specification() == parameter:
                    return param.ParameterValue()

def _ValidateParameterValue(parameter, value):
    if parameter in _SETTING_CHOICES:
        choice = value.split(':')[0].lower()
        if choice not in _SETTING_CHOICES[parameter]:
            value = _SETTINGS[parameter]
            logger.warn('Limit setting "%s" has invalid value "%s". Using default "%s".', 
                    parameter, choice, value)
            logger.warn('Valid values include: %s', ', '.join(_SETTING_CHOICES[parameter]))
    return value

def _CreateAccessorFunction(parameter):
    def f():
        return _GetParameterValue(parameter)
    return f

def _CreateFunctions():
    module = sys.modules[__name__]
    for parameter in list(_SETTINGS.keys()):
        name = _FunctionNameForParameter(parameter)
        if not getattr(module, name, None):
            func = _CreateAccessorFunction(parameter)
            setattr(module, name, func)


# Generate functions in this module for accessing settings. Existing functions
# providing specialised handling will not be overridden.
_CreateFunctions()
