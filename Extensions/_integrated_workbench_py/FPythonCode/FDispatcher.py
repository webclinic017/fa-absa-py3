""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FDispatcher.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FDispatcher

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import inspect

from FEvent import EventCallbackBase
from FIntegratedWorkbenchLogging import logger


class Dispatcher(object):

    def __init__(self):
        self._observers = set()
        self._history = set()

    def Observers(self):
        return self._observers

    def AddDependent(self, observer):
        logger.debug("Dispatcher.AddDependent() Add '%s'", self.ObserverClassName(observer))
        self._observers.add(observer)

    def RemoveDependent(self, observer):
        try:
            logger.debug("Dispatcher.RemoveDependent() Removing '%s'", self.ObserverClassName(observer))
            self._observers.remove(observer)
        except KeyError as exc:
            logger.error(
                        "Dispatcher.RemoveDependent() Exception while removing dependent: %s",
                        self.ObserverClassName(observer))
            logger.error(exc, exc_info=True)

    def Update(self, event):
        if event:
            logger.debug("Dispatcher.Update() event: %s" % event)
            for observer in list(self._observers):
                try:
                    self.HandleEvent(observer, event)
                except StandardError as exc:
                    logger.error(
                        "Exception while dispatching event to '%s':",
                        self.ObserverClassName(observer))
                    logger.error(exc, exc_info=True)
        else:
            logger.debug("Dispatcher.Update() attempting to send empty event")

    def RemoveDependents(self):
        for observer in self._observers:
            observer.RemoveDependent()

    @classmethod
    def GetMethod(cls, observer, methodName):
        return getattr(observer, methodName, None)

    @classmethod
    def IsValid(cls, method):
        return bool(method and isinstance(method, EventCallbackBase))

    @classmethod
    def HandleEvent(cls, observer, event):
        logger.debug('Handle Event %s %s', str(observer), str(event))
        for subclass in inspect.getmro(type(event)):
            methodName = subclass.__name__
            method = cls.GetMethod(observer, methodName)
            logger.debug('Handle Event %s %s', str(methodName), str(method))
            if cls.IsValid(method):
                logger.debug(
                    "Dispatcher.HandleEvent() Notifying %s about %s from %s",
                    cls.ObserverClassName(observer),
                    methodName,
                    cls.SenderClassName(event))
                return method(event)

    @staticmethod
    def SenderClassName(event):
        try:
            return event.Sender().ClassName()
        except AttributeError:
            return type(event.Sender()).__name__

    @staticmethod
    def ObserverClassName(observer):
        try:
            return observer.ClassName()
        except AttributeError:
            return type(observer).__name__

class Sender(object):
    def __init__(self, dispatcher):
        self._dispatcher = dispatcher

    def Dispatcher(self):
        return self._dispatcher

    def DispatchEvent(self, event):
        if event is not None:
            return self.Dispatcher().Update(event)
        raise ValueError("Invalid event")


class Observer(Sender):

    def __init__(self, observer, dispatcher):
        Sender.__init__(self, dispatcher)
        self.observer = observer
        self.AddDependent()

    def AddDependent(self, dispatcher=None):
        dispatcher = dispatcher or self.Dispatcher()
        dispatcher.AddDependent(self.observer)

    def RemoveDependent(self, dispatcher=None):
        dispatcher = dispatcher or self.Dispatcher()
        dispatcher.RemoveDependent(self.observer)
