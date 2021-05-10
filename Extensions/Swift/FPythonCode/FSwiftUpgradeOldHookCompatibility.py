""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/upgrade/FSwiftUpgradeOldHookCompatibility.py"
"""
Kept for backward compatibility, under a different name, 
to be very clear that this is old and should not be used.
"""
import FOperationsUtils as Utils

class Hook(object):

    def __init__(self, moduleName, xmlTag, mtType):
        self.__xmlTag = xmlTag
        self.__mtType = mtType
        self.__module = self.__GetModule(moduleName)

    def __GetModule(self, moduleName):
        try:
            module = __import__(moduleName)
        except ImportError:
            Utils.LogAlways('Could not import hook module %s' % moduleName)
            module = None
        return module

    def HasXmlTag(self):
        return self.__xmlTag != None

    def HasModule(self):
        return self.__module != None

    def GetXmlTagName(self):
        if self.HasXmlTag():
            return self.__xmlTag
        return ''

    def GetModuleName(self):
        if self.HasModule():
            return self.__module.__name__
        return ''

    def GetMtType(self):
        return self.__mtType
