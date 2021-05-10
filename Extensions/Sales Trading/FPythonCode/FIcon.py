""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FIcon.py"
import os
import acm

def IconAliases():
    params = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', 'IconAliases')
    return params.Value()

def IconModuleNames():
    pythonModules = acm.GetDefaultContext().GetAllExtensions('FPythonCode')
    for module in pythonModules:
        if str(module.Name()).startswith('IconString'):
            yield str(module.Name())

class Icon(object):

    _registered = set()
    _alias = IconAliases()
    _modules = [__import__(m) for m in IconModuleNames()]

    def __init__(self, name):
        self._name = self._IconName(name)

    def IconStr(self):
        name = self._name.replace(' ', '')
        for module in self._Modules():
            if hasattr(module, name):
                return getattr(module, name)
        return None

    def GetIconFromStr(self, iconStr):
        if iconStr is None:
            return None
        try:
            icon = acm.UX().IconFromString(self._name, iconStr)
            self.RegisterIcon(icon)
            return icon
        except RuntimeError:
            return None

    def RegisterIcon(self, icon):
        if icon is not None and not acm.UX().IconExist(self._name):
            icon.RegisterIcon()
            self._Registered().add(self._name)

    def GetIcon(self):
        if (self._name in self._Registered() or
                self.GetIconFromStr(self.IconStr())):
            return self._name

    @classmethod
    def _IconName(cls, name):
        return str(cls._alias.At(name, name))

    @classmethod
    def _Registered(cls):
        return cls._registered

    @classmethod
    def _Modules(cls):
        return cls._modules


def CreatePythonFileWithIcons(fileName, path):
    buff = ''.join(('FObject:IconString', fileName, '\n'))
    for ico in os.listdir(path):
        name = os.path.splitext(ico)[0]
        ico_path = os.path.join(path, ico)
        icon = acm.UX().IconFromFile(name, ico_path)
        if icon != None:
            buff = ''.join((buff, name.replace('-', ''), ' = ',
                            '\"""', '\n', icon.ToString(), '\"""', '\n'))

    context = acm.GetDefaultContext()
    context.EditImport('FPythonCode', buff)
    context.EditModule().Commit()

    