""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../reconciliation/etc/FBusinessDataImportHook.py"
"""--------------------------------------------------------------------------
MODULE
    FBusinessDataImportHook

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()


def _LoadPythonHook(moduleName, functionName):
    """Load a Python module as script or extension.
    If the module cannot be found, raise a ValueError."""
    try:
        pyModule = acm.LoadAel(moduleName, acm.GetDefaultContext())
        if not pyModule:
            errorStr = "Module '%s' not loaded" % (moduleName)
            raise ValueError(errorStr)
        return getattr(pyModule, functionName)
    except Exception as serr:
        errorStr = "Exception while loading function '{}' in module '{}' : {}".format(
                functionName, moduleName, serr)
        logger.warn(errorStr)
        raise ValueError(errorStr)


class FBusinessDataImportHook(object):
    """Proxy for a generic hook, defined in a Python extension or a Python module."""

    def __init__(self, mod, func=None):
        """ Create a Hook object, by either passing one or two arguments.
        The single argument option expects a function id as 'module.function'
        while the two argument option requires module and function name separately.
        In case the function can not be loaded, a ValueError exception will be raised."""
        if not func:
            try:
                mod, func = mod.split('.')
            except ValueError:
                raise ValueError("Invalid function identifier '%s' expected <module>.<function>" % mod)
        self._moduleName = mod
        self._functionName = func
        self._pyHook = _LoadPythonHook(self._moduleName, self._functionName)

    def ModuleName(self):
        """Return the name of the Python module."""
        return self._moduleName

    def FunctionName(self):
        """Return the name of the Python function."""
        return self._functionName

    def HookFunction(self):
        """Return the loaded hook function."""
        return self._pyHook

    def IsLoaded(self):
        """Return True if the function has been loaded successfully."""
        return (self._pyHook != None)

    def Run(self, *arguments):
        """Run the hook function, pass given arguments."""
        if not self._pyHook:
            errorStr = "Function '{}' in module '{}' not loaded".format(
                    self._functionName, self._moduleName)
            logger.warn(errorStr)
            raise ValueError(errorStr)
        try:
            return self._pyHook(*arguments)
        except Exception as serr:
            errorStr = "Exception while running function '{}' in module '{}' : {}".format(
                self.FunctionName(), self.ModuleName(), serr)
            logger.warn(errorStr)
            raise ValueError(errorStr)

    def __call__(self, *arguments):
        return self.Run(*arguments)

    def __nonzero__(self):
        return (self._pyHook != None)

def _ApplyHookToDictionaryAndLog(hook, dictItem):
    """ Assuming a hook that takes a dictionary as argument and transforms it, log
    the difference between source and transformed dicts."""
    originalDict = dict(dictItem)
    dictItem = hook(dictItem)
    if dictItem:
        for key, value in dictItem.items():
            if not key in originalDict:
                logger.debug("Added column '%s'='%s'", key, value)
            elif not value == originalDict[key]:
                logger.debug("Modified column '%s'='%s' from '%s'",
                        key, value, originalDict[key])
        for key in (set(originalDict.keys()) - set(dictItem.keys())):
            logger.debug("Removed column '%s'='%s'", key, originalDict[key])
    else:
        logger.debug('Row filtered out by external values hook')
    return dictItem

def TransformDictionary(hook, dictGen):
    """ Apply a hook to each element of a dictionary generator, return a new dictionary generator.
    Log the difference between the dictionaries."""
    return (_ApplyHookToDictionaryAndLog(hook, dictItem) for dictItem in dictGen)
