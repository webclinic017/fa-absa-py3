import types
import inspect
import functools

class CommandActionBase(object):

    DISPLAY_NAME = 'Undefined'
    TOOL_TIP = ''
    ACCELERATOR = ''
    MNEMONIC = ''
    PARENT = ''

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        
    def Arguments(self):
        return self._args
        
    def KeyWordArguments(self):
        return self._kwargs
        
    def KeyWordArgumentAt(self, key):
        return self.KeyWordArguments().get(key)

    @classmethod
    def DisplayName(cls):
        return cls.DISPLAY_NAME
        
    @classmethod
    def ToolTip(cls):
        return cls.TOOL_TIP
    
    @classmethod
    def Accelerator(cls):
        return cls.ACCELERATOR
        
    @classmethod
    def Mnemonic(cls):
        return cls.MNEMONIC
        
    @classmethod
    def Parent(cls):
        return cls.PARENT
        
    def Invoke(self):
        raise NotImplementedError

    def Applicable(self):
        return True
        
    def Enabled(self):
        return True
        
    def Checked(self):
        return False
        
    def DealPackage(self):
        return self.KeyWordArgumentAt('dealPackage')
        
    def SetDealPackage(self, dp):
        self.KeyWordArguments().update(dealPackage=dp)
        
    def Buttons(self):
        return 'SaveNew'

class _ActionHandlers(object):
    '''Decorator to register Actions on definitions'''
    
    _HANDLER = NotImplementedError
    
    def __init__(self, **kwargs):
        self._kwargs = kwargs        

    def __call__(self, definition):
        thisClassTradeactions = {}
        superClassTradeactions = getattr(definition, self._HANDLER)
        thisClassTradeactions.update(superClassTradeactions())
        thisClassTradeactions.update(self._kwargs)
        thisClassTradeactions = {key : self._PartialClassFromInstance(actionHandler) for key, actionHandler in list(thisClassTradeactions.items()) 
                                        if self._IncludeActionHandler(actionHandler)}
        func = lambda _: thisClassTradeactions
        func = types.MethodType( func, definition )
        setattr(definition, self._HANDLER, func)
        return definition
    
    def _IncludeActionHandler(self, actionHandler):
        return actionHandler is not None
        
    def _PartialClassFromInstance(self, obj):
        if not inspect.isclass(obj):
            if hasattr(obj, '_args') and hasattr(obj, '_kwargs'):
                return functools.partial(obj.__class__, *obj._args, **obj._kwargs)
        return obj
    
class TradeActions(_ActionHandlers):
    _HANDLER = '_TradeActionHandlers'

def NoTradeActions(definition):
    class NoTradeActionsImpl(TradeActions):
        def _IncludeActionHandler(self, actionHandler):
            return False
    return NoTradeActionsImpl()(definition)

class CustomActions(_ActionHandlers):
    _HANDLER = '_CustomActionHandlers'
