""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FViewUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FViewUtils

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Internal classes for creating handlers and panels.
-------------------------------------------------------------------------------------------------------"""
import acm
from FIntegratedWorkbenchLogging import creationLogger
from FParameterSettings import ParameterSettingsCreator
from types import GeneratorType

def ViewSettings(viewName):
    for settings in ViewParameterSettings():
        if viewName == settings.Name():
            return settings
    errorMessage = ('Could not find valid parameter for view "{0}". ' +
               'If parameter exist, make sure it is added to the extension group "view". ' +
               'Turn up creation logging for more information.')
    raise ValueError(errorMessage.format(viewName))

def ViewParameterExists(viewName):
    try:
        ViewSettings(viewName)
        return True
    except ValueError:
        return False

def ViewParameterSettings():
    for parameter in _ViewFParameters():
        settings = ParameterSettingsCreator.FromRootParameter(parameter.Name())
        if _IsValidView(settings):
            yield settings

def _ViewFParameters():
    return acm.GetDefaultContext().GetAllExtensions('FParameters', '', False, False, 'view', '', False)

def _IsValidView(parameter):
    isValid = hasattr(parameter, 'DockWindows') and isinstance(parameter.DockWindows(), GeneratorType)
    if isValid is False:
        creationLogger.debug('View {0} missing valid DockWindows parameter'.format(parameter.Name()))
    return isValid
