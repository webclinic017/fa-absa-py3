""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsHook.py"
"""
FOperationsHook
"""

import acm, traceback
import types
import inspect
from FOperationsExceptions import InvalidHookException
from FOperationsTypeComparators import DummyTypeComparator

class Hook:

    def __init__(self, moduleName, hookName, comparator):
        assert type(moduleName) == str, 'Input parameter moduleName not of type string!'
        assert type(hookName) == str, 'Input parameter hookName not of type string!'
        self.__moduleName = moduleName
        self.__hookName = hookName
        self.__module = self.__GetModule()
        self.__hook = self.__GetHook()
        self.__comparator = comparator

    def __GetModule(self):
        try:
            module = __import__(self.__moduleName)
        except Exception as e:
            raise  InvalidHookException("Error when creating hook {}: {}. \n {}".format(self.__hookName, str(e), traceback.format_exc()))
        return module

    def __GetHook(self):
        hook = None
        if self.HasModule():
            try:
                assert True == self.__module.__dict__.has_key(self.__hookName), \
                    "{} not found in module {}.".format(self.__hookName, self.__moduleName)
                hook = self.__module.__dict__[self.__hookName]
                assert type(hook) == types.FunctionType, \
                    "{} is not a function.".format(self.__hookName)
            except Exception as e:
                hook = None
                raise InvalidHookException("Error when creating hook {}: {} \n {}".format(self.__hookName, str(e), traceback.format_exc()))

        return hook

    def HasHook(self):
        return self.__hook != None

    def HasModule(self):
        return self.__module != None

    def GetHook(self):
        return self.__hook

    def GetModule(self):
        return self.__module

    def GetHookName(self):
        hookName = ''
        if self.HasHook():
            hookName = self.__hook.__name__
        return hookName

    def GetModuleName(self):
        moduleName = ''
        if self.HasModule():
            moduleName = self.__module.__name__
        return moduleName

    def GetComparator(self):
        return self.__comparator

    def SetComparator(self, comparator):
        self.__comparator = comparator

    def __PrepareArguments(self, *args):
        argsToHook = args
        if inspect.getargspec(self.__hook)[0]:
            extraArgs = len(inspect.getargspec(self.__hook)[0]) - len(argsToHook)

            if extraArgs > 0:
                for i in range(0, extraArgs):
                    argsToHook = argsToHook +(None, )
            if extraArgs < 0:
                argsToHook = tuple()
                for i in range(0, len(inspect.getargspec(self.__hook)[0])):
                    argsToHook = argsToHook +(args[i], )
        return argsToHook

    def __CallHook(self, *args):
        return self.__hook(*args)

    def CallHook(self, *args):
        value = None
        try:
            value = self.__CallHook(*(self.__PrepareArguments(*args)))
            assert True == self.__comparator.IsCorrectType(value), \
                "Wrong type returned, got {} but expected {}".format(type(value), self.__comparator.GetExpectedType())
        except Exception as e:
            raise InvalidHookException("Exception caught when calling hook function {} with parameters ({}): {}. \n {}".format(self.GetHookName(), self.__FormatArgsForPrint(*args), str(e), traceback.format_exc()))
        return value

    def __FormatArgsForPrint(self, *args):
        stringArgs = list()
        for arg in args:
            stringArgs.append(self.__FormatArgument(arg))
        return ', '.join(stringArgs)

    def __FormatArgument(self, arg):
        if type(arg) in [list, set]:
            stringVals = list()
            for value in arg:
                stringVals.append(self.__FormatArgument(value))
            return "[{}]".format(', '.join(stringVals))
        try:
            return "{}: {}".format(arg.ClassName(), arg.Oid())
        except AttributeError:
            return str(arg)

class DefaultHook(Hook):

    def __init__(self, moduleName, hookName, comparator):
        Hook.__init__(self, moduleName, hookName, comparator)
        assert self.HasModule(), 'Default hook module %s not found!' % moduleName
        assert self.HasHook(), 'Default hook %s not found!' % hookName

class CustomHook(Hook):

    def __init__(self, moduleName, hookName, comparator=DummyTypeComparator()):
        Hook.__init__(self, moduleName, hookName, comparator)
