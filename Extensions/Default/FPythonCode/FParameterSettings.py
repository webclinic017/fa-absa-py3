""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FParameterSettings.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FParameterSettings

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Class for automatically generating classes from FParameters.
-------------------------------------------------------------------------------------------------"""

__all__ = ['ParameterSettingsCreator']

import acm
import imp
import sys
import string

class Singleton(type):

    _instances = {}

    def __init__(self, *args, **kwargs):
        # pylint: disable-msg=W0231
        self._dict = args[2]

    def UpdateClass(self):
        for attr, value_ in self._dict.items():
            setattr(self.Class(), attr, value_)

    def Class(self):
        return self.Instance().__class__

    def Instance(self, instance=None):
        if instance is None:
            return self._instances.get(self.__name__)
        self._instances[self.__name__] = instance

    def __call__(self, *args, **kwargs):
        if self.__name__ not in self._instances:
            self.Instance(type.__call__(self, *args, **kwargs))
        self.UpdateClass()
        return self.Instance()


class ParameterSettings(object):
    """
    Base Class for ParameterSettings created using the ParameterSettingsCreator
    """
    pass


class ParameterSettingsCreator(object):

    _INVALID_CHARS = string.punctuation.replace('_', '')

    def __init__(self, rootName, extModName=None):
        self._extModName = str(extModName) if extModName is not None else None
        self._rootName = str(rootName)
        self._pythonModule = None


    @classmethod
    def FromRootParameter(cls, paramName, moduleName=None):
        return cls(paramName, moduleName).CreateSettings()

    def RootName(self):
        return self._rootName

    def ExtensionModuleName(self):
        return self._extModName

    def PythonModule(self):
        if self._pythonModule is None:
            moduleName = self._PythonModuleName(self.ExtensionModuleName())
            self._pythonModule = imp.new_module(moduleName)
            sys.modules[moduleName] = self._pythonModule
        return self._pythonModule

    def CreateSettings(self):
        for paramExt in self._Parameters(self.RootName()):
            if not self._SettingsClsCreated(paramExt):
                self._CreateCls(paramExt)
        return self._CreateInstance()

    @staticmethod
    def Context():
        return acm.GetDefaultContext()

    def _ExtensionModule(self):
        if self.ExtensionModuleName():
            for mod in self.Context().Modules():
                if mod.Name() == self.ExtensionModuleName():
                    return mod
            raise TypeError('Could not access Extension module {0} referenced by FParameter {1}.'.format(
                self.ExtensionModuleName(), self.RootName()))


    def _Parameters(self, paramName, parameters=None):
        if parameters is None:
            parameters = set()
        paramExt = self._ParameterFromName(paramName)
        if paramExt and paramExt not in parameters:
            parameters.add(paramExt)
            for setting in paramExt.Value().Values():
                if self._IsList(setting):
                    for s in self._AsList(setting):
                        self._Parameters(s, parameters)
                else:
                    self._Parameters(setting, parameters)
        return parameters

    def _SettingsClsCreated(self, paramExt):
        return bool(self._SettingsCls(self._ParameterName(paramExt)))

    def _SettingsCls(self, paramName):
        return getattr(self.PythonModule(), paramName, None)

    def _AttributesDict(self, parameters):
        return  dict((self._ValidNameOrException(param), self._Method(param, parameters))
                     for param in parameters)

    def _AddCommonAttributes(self, attrs, parameters):
        attrs['Name'] = lambda x: self._ParameterName(parameters)
        attrs['Commit'] = lambda x, module=None: self._Commit(parameters, module)
        attrs['__str__'] = lambda x: parameters.AsString()

    def _CreateCls(self, paramExt):
        parameters = paramExt.Value().Clone()
        attrs = self._AttributesDict(parameters)
        self._AddCommonAttributes(attrs, parameters)
        paramName = self._ParameterName(parameters)
        paramCls = Singleton(paramName, (ParameterSettings, ), attrs)
        setattr(self.PythonModule(), paramName, paramCls)

    def _CreateInstance(self):
        try:
            settingsCls = self._SettingsCls(self.RootName())
            return settingsCls()
        except TypeError:
            raise AttributeError("Unknown parameter '%s'" % self.RootName())

    def _ParameterFromName(self, name):
        paramSource = self._ExtensionModule() or self.Context()
        return paramSource.GetExtension(acm.FParameters, acm.FObject, name)

    def _Commit(self, parameters, module=None):
        moduleToSaveTo = module or self.Context().EditModule()
        assert isinstance(moduleToSaveTo, acm._pyClass(acm.FExtensionModule)), \
        'Commit: Module should be of type FExtensionModule'
        self.Context().EditImport('FParameters',
                                  ':'.join(('FObject', parameters.AsString())), editModule=moduleToSaveTo)
        try:
            moduleToSaveTo.Commit()
        except RuntimeError as err:
            raise RuntimeError('Failed to save parameters {0} in module {1}. '
                'Reason: {2}.'.format(parameters.Name(), moduleToSaveTo.Name(), err))

    def _Method(self, setting, settings):
        def InnerMethod(_self, value_=None):
            if value_ is None:
                setting_ = settings.GetString(setting, None)
                if self._IsList(setting_):
                    return (self._InstanceOrData(s)
                            for s in self._AsList(setting_))
                return self._InstanceOrData(setting_)
            settings.AtPut(setting, str(value_))
        return InnerMethod

    def _InstanceOrData(self, data):
        cls = getattr(self.PythonModule(), data, None)
        if cls is None:
            return self._AsVariant(data)
        return cls()

    @classmethod
    def _ParameterName(cls, paramExt):
        return cls._ValidNameOrException(paramExt.Name())

    @classmethod
    def _ValidNameOrException(cls, name):
        if cls._IsValidName(name):
            return str(name).replace(' ', '')
        raise NameError('"{0}" is not a valid name. Make sure it does not contain any of '
                        'the following characters "{1}"'.format(name, cls._INVALID_CHARS))

    @classmethod
    def _IsValidName(cls, name):
        return str(name) == cls._ValidName(name)

    @classmethod
    def _ValidName(cls, name):
        return str(name).translate(None, cls._INVALID_CHARS)

    @classmethod
    def _AsVariant(cls, variant):
        if isinstance(variant, str):
            if variant.lower() in ('true', 'yes'):
                return True
            elif variant.lower() in ('false', 'no'):
                return False
            try:
                return cls._AsNumber(variant)
            except ValueError:
                pass
        return variant

    @staticmethod
    def _AsNumber(text):
        try:
            return int(text)
        except ValueError:
            return float(text)

    @staticmethod
    def _IsList(data):
        stripdata = str(data).strip()
        if stripdata:
            return ('[', ']') == (stripdata[0], stripdata[-1])
        else:
            return False

    @staticmethod
    def _AsList(data):
        buff = str(data).strip()[1:-1]
        if buff:
            return [s.strip() for s in buff.split(';')]
        return []

    @classmethod
    def _PythonModuleName(cls, name):
        name = name or acm.UserName().upper()
        return 'F{0}Settings'.format(cls._ValidName(name))
