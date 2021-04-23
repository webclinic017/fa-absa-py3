import inspect
import types
import acm
import sys
from functools import wraps
import traceback


from DealPackageUtil import FormatException, IsCallable, DealPackageUserException

class AttributeException(Exception):
    pass
    
class ExceptionAccumulator(object):
    def __init__(self, dealpackageDefinition):
        self.Clear()
        self._dealpackageDefinition = dealpackageDefinition
        
    def TraitInErrorState(self):
        return len(self.ErrorList()) > 0
    
    def ErrorList(self):
        return self._errorList
    
    def ErrorString(self):
        return " - ATTR ERROR"
        
    def Clear(self):
        self._errorList = []
        
    def Raise(self):
        compoundError = ""
        for err in self.ErrorList():
            compoundError = compoundError + format(err) + '\n'
        if compoundError:
            raise AttributeException(compoundError)
        
    def InvokeAndCatch(self, default_return_value, catch_exception_type, call_func, *args, **kwargs):
        result = default_return_value
        try:
            result = call_func(*args, **kwargs)
            self.Clear()
        except catch_exception_type as e:
            self._dealpackageDefinition.Log().Warning(e)
            self._errorList.append(FormatException(e))
        return result


class ThrowOrAccumulate(object):
    def __init__(self, defaultReturnValue, catchExceptionOfType):
        self._defaultReturnValue = defaultReturnValue
        self._catchExceptionOfType = catchExceptionOfType

    def __call__(dec_self, func):
    
        def wrapper_func(*args, **kwargs):
            klas = args[0]
            traitName = args[1]
            accumulator = klas._GetExceptionAccumulator(traitName)
            
            if accumulator:
                return accumulator.InvokeAndCatch(dec_self._defaultReturnValue, dec_self._catchExceptionOfType, func, *args, **kwargs)
            else:
                return func(*args, **kwargs)
                
        return wrapper_func


class CallableBase(object):
    class Dummy():
        pass
    
    NoValue = Dummy()
    
    def __init__(self, preArgs=[], postArgs=[]):
        self._preArgs = preArgs
        self._postArgs = postArgs
        
    def _MakeSingleCall(self, cb, *args):
        allArgs = []
        allArgs.extend( self._preArgs )
        allArgs.extend(  args )
        allArgs.extend( self._postArgs )
        return cb(*allArgs)
    
    def _AssertEqualReturn(self, prevReturn, newReturn):
        if prevReturn != CallableBase.NoValue and prevReturn != newReturn:
            raise Exception('Inconsistent return values, got: %s and %s' % (prevReturn, newReturn))

class CallableCollection(CallableBase):
    def __init__(self, collection, method, preArgs=[], postArgs=[]):
        CallableBase.__init__(self, preArgs, postArgs)
        self._collection = []
        self._InitCallableCollection( self._CreateCollectionOfCalables(collection, method) )
    
    def _InitCallableCollection(self, collection):
        self._collection = collection
        
    def _CreateCollectionOfCalables(self, collection, method):
        allCallables = []
        try:
            for c in collection:
                allCallables.append( getattr(c, method) )
        except TypeError:
            allCallables.append( getattr(collection, method) )
        return allCallables
    
    def __call__(self, *args):
        prevReturn = CallableBase.NoValue
        newReturn = None
        for cb in self._collection:
            newReturn = self._MakeSingleCall(cb, *args)
            self._AssertEqualReturn(prevReturn, newReturn)
            prevReturn = newReturn
        return newReturn

class CallableMethodChain(CallableBase):
    methodSplitter = '.'
    def __init__(self, methodBase, methodChain, preArgs=[], postArgs=[]):
        CallableBase.__init__(self, preArgs, postArgs)
        self._methodBase = methodBase
        self._methodLinks = methodChain.split( CallableMethodChain.methodSplitter )
        self.__AssertCallable()
    
    def __AssertCallable(self):
        if not IsCallable(self._methodBase, self._methodLinks[0]):
            raise AttributeException('Method %s is not callable' % self._methodLinks[0])
    
    def __call__(self, *args):
        baseObj = self._methodBase
        lastMethod = self._methodLinks[-1]
        for link in self._methodLinks[:-1]:
            baseObj = getattr(baseObj, link)()
        return CallableCollection(baseObj, lastMethod, self._preArgs, self._postArgs)(*args)
    
class CallableMultiMethodChain(CallableCollection):
    chainSplitter = '|'
    def __init__(self, methodBase, multiMethodChains, preArgs=[], postArgs=[]):
        CallableBase.__init__(self)
        self._InitCallableCollection( self._CreateCallableMethodChains(methodBase, multiMethodChains, preArgs, postArgs) )
    
    def _CreateCallableMethodChains(self, methodBase, multiMethodChains, preArgs, postArgs):
        callableChains=[]
        chains = multiMethodChains.split( CallableMultiMethodChain.chainSplitter )
        for c in chains:
            callableChains.append( CallableMethodChain(methodBase, c, preArgs, postArgs) )
        
        return callableChains
        
class CallableMultiCalcConfigurationMethodChain(CallableMultiMethodChain):
    def __call__(self, *args):
        config = None
        for cb in self._collection:
            newConfig = self._MakeSingleCall(cb, *args)
            config = config.Merge(newConfig) if config and newConfig else config or newConfig
        return config
        
class AttributeLog(object):
    validModes = ['Verbose', 'Warning', 'Error']
    def __init__(self, mode='Error'):
        self._mode = mode
        self.AssertValidMode(self._mode)
    
    @classmethod
    def AssertValidMode(cls, mode):
        assert mode in cls.validModes, 'LogMode "%s" is invalid. Must be one of %s' % (mode, cls.validModes)
    
    def Verbose(self, msg):
        if self._mode in ['Verbose']:
            acm.Log(msg)
    
    def Warning(self, msg):
        if self._mode in ['Verbose', 'Warning']:
            acm.Log(msg)
    
    def Error(self, msg):
        if self._mode in ['Verbose', 'Warning', 'Error']:
            acm.Log(msg)

class LogException(object):
    def __init__(self, logAs='Error'):
        self._logAs = logAs
        AttributeLog.AssertValidMode(self._logAs)
    
    def __Log(self, log, e):
        getattr(log, self._logAs)(str(e))
    
    def __RaiseOriginalException(self, e, originalStacktrace):
        raise type(e)(e).with_traceback(originalStacktrace)
        
    def __call__(self, f):
        @wraps(f)
        def exceptionLogger(*args, **kwds):
            definition = args[0]
            try:
                return f(*args, **kwds)
            except DealPackageUserException as e:
                raise
            except Exception as e:
                originalStacktrace = sys.exc_info()[2]
                msg = '%s:\n%s' % (str(e), traceback.format_exc())
                self.__Log(definition.Log(), msg)
                self.__RaiseOriginalException(e, originalStacktrace)
        return exceptionLogger
