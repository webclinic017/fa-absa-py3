""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsHookAdministrator.py"
import acm

from FOperationsHook import CustomHook
from FOperationsExceptions import InvalidHookException
from FOperationsEngines import HookCaller

#-------------------------------------------------------------------------
class HookAdministrator(HookCaller):

    #-------------------------------------------------------------------------
    def __init__(self, customHooks, defaultHooks):
        self.hooks = dict(defaultHooks)
        self.customHooks = customHooks

        self.RegisterCustomHooks()

    #-------------------------------------------------------------------------
    def HA_IsCustomHook(self, hookName):
        hookObject = self.GetHookObject(hookName)
        return isinstance(hookObject, CustomHook)

    #-------------------------------------------------------------------------
    def HA_CallHook(self, hookName, *args):
        return self.hooks[hookName].CallHook(*args)

    #-------------------------------------------------------------------------
    def RegisterCustomHooks(self):
        self.ValidateCustomHooks()

        for hook in self.customHooks:
            hook.SetComparator(self.hooks[hook.GetHookName()].GetComparator())
            self.RegisterHook(hook.GetHookName(), hook)

    #-------------------------------------------------------------------------
    def RegisterHook(self, hookName, hook):
        self.hooks[hookName] = hook

    #-------------------------------------------------------------------------
    def ValidateCustomHooks(self):
        if self.__CustomHookDuplicates():
            raise InvalidHookException('Could not register custom hooks. Custom hook duplicates.')

        for hook in self.customHooks:
            if hook.GetHookName() not in self.hooks:
                raise InvalidHookException('Could not register custom hook {}. Incorrect hook name.'.format(hook.GetHookName()))
            if not hook.HasHook():
                raise InvalidHookException('Could not register custom hook {}. Hook is missing.'.format(hook.GetHookName()))

    #-------------------------------------------------------------------------
    def PrintRegisteredCustomHooks(self):
        for hook in self.hooks:
            if isinstance(hook, CustomHook):
                acm.Log('Custom hook %s is registered' % hook.GetHookName())

    #-------------------------------------------------------------------------
    def __CustomHookDuplicates(self):
        customHookNames = {hook.GetHookName() for hook in self.customHooks}
        return len(customHookNames) != len(self.customHooks)

    #-------------------------------------------------------------------------
    def GetHookObject(self, hookName):
        return self.hooks[hookName]

    #-------------------------------------------------------------------------
    def GetHook(self, hookName):
        return self.hooks[hookName].GetHook()
