""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FPromise.py"
"""--------------------------------------------------------------------------
MODULE
    FPromise

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Decorator to help when an asynchronous event needs to be performed 
    before calling a function.
-----------------------------------------------------------------------------"""
from collections import namedtuple

import acm
from FParameterSettings import ParameterSettingsCreator

SETTINGS = ParameterSettingsCreator.FromRootParameter('BSOMSSettings')

class PromiseInterface(object):

    def Init(self, *args, **kwargs):
        """ Used to Initialize the interface with the arguments passed to the decorated function """
        pass
    
    def Subscriptions(self):
        """ Should return a list of objects for the Promise decorator to subscribe to """
        raise NotImplementedError
        
    def Fulfilled(self, *args, **kwargs):
        """ Should return True when the function is ready to be called """
        raise NotImplementedError
        
    def Timeout(self):
        """ Number of seconds before timeout. Raises StandardError on Timeout if Fulfilled still returns False """
        return SETTINGS.DefaultPromiseTimeOut()
    
    def ErrorMessage(self):
        """ The error message that will be used on timeout """ 
        return 'Timeout reached without fulfilling criteria on Promise {0}'.format(self.__class__.__name__)

class AsynchronousCall(object):
    """ Makes sure method is called in the main thread """
    
    def __init__(self, func):
        self._func = func
        
    def __call__(self, *args, **kwargs):
        acm.AsynchronousCall(self._func, args)
        
class Promise(object):
    """ Class used to decorate function. Takes an instance of PromiseInterface as argument """
    
    def __init__(self, interface, onRejected=None):
        self._interface = interface
        self._func = None
        self._timer = None
        self._onRejected = onRejected
        self._instances = list()
        self.InstanceInfo = namedtuple('InstanceInfo', ['instance', 'args', 'kwargs'])
                 
    def __call__(self, func):
        self._func = func
        def wrapper(*args, **kwargs):
            instanceInfo = self.InstanceInfo(self._interface(), args, kwargs)
            self._instances.append(instanceInfo)
            if len(self._instances) == 1:
                self._InitializeInstance(*instanceInfo)
        return wrapper
    
    def ServerUpdate(self, sender, aspect, param):
        try:
            instanceInfo = self._InstanceInfo()
            if instanceInfo.instance.Fulfilled(sender, aspect, param):
                self._RemoveSubscriptions()
                self._OnFulfilled(*instanceInfo)
        except Exception as e:
            self._HandleRejection(self, self._InstanceInfo(), str(e))

    def OnTimeout(self, arg):
        try:
            self._RemoveSubscriptions()
            instanceInfo = self._InstanceInfo()
            if instanceInfo.instance.Fulfilled():
                self._OnFulfilled(*instanceInfo)
            else:
                self._HandleRejection(self, instanceInfo, instanceInfo.instance.ErrorMessage())
        except Exception as e:
            self._HandleRejection(self, self._InstanceInfo(), str(e))
        
    @AsynchronousCall
    def _HandleRejection(self, instanceInfo, errorMessage):
        if self._onRejected:
            self._OnRejected(instanceInfo[0], instanceInfo[1], instanceInfo[2], errorMessage=errorMessage)
        else:
            raise Exception(errorMessage)
        
    def _OnFulfilled(self, instance, args, kwargs):
        self._func(*args, **kwargs)
        self._InitializeNextInstance()
        
    def _OnRejected(self, instance, args, kwargs, errorMessage=None):
        kwargs = {k:kwargs[k] for k in kwargs.Keys()}
        self._onRejected(*args, errorMessage=errorMessage, **kwargs)
        self._InitializeNextInstance()
    
    def _InitializeInstance(self, instance, args, kwargs):
        try:
            instance.Init(*args, **kwargs)
            if not instance.Fulfilled():
                self._InitializeSubscriptions(instance)
            else:
                self._OnFulfilled(instance, args, kwargs)
        except Exception as e:
            self._HandleRejection(self, self._InstanceInfo(), str(e))
            
    def _InitializeNextInstance(self):
        self._instances.pop(0)
        if self._instances:
            self._InitializeInstance(*self._InstanceInfo())
    
    def _InitializeSubscriptions(self, instance):
        for obj in instance.Subscriptions():
            obj.AddDependent(self)
        self._timer = acm.FTimer().CreateTimerEvent(instance.Timeout(), self.OnTimeout, None)
    
    def _RemoveSubscriptions(self):
        acm.FTimer().RemoveTimerEvent(self._timer)
        instance = self._InstanceInfo().instance
        for obj in instance.Subscriptions():
            obj.RemoveDependent(self)
            
    def _InstanceInfo(self):
        return self._instances[0]
