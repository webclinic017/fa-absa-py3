""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FWorkbenchObserver.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWorkbenchObserver

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import FDispatcher
import FEvent


class WorkbenchObserver(object):

    def __init__(self, dispatcher, instance):
        self._dispatcher = dispatcher
        self._instance = instance
        self._eventQueue = None
        self._observer = None
        self._InitObserver()

    def EventQueue(self):
        if self._eventQueue is None:
            self._eventQueue = FEvent.EventQueue()
        return self._eventQueue

    def AddToEventQueue(self, event):
        self.EventQueue().Add(event)

    def SendEvent(self, event):
        self._Observer().DispatchEvent(event)

    def CreateEvent(self, name, *args, **kwargs):
        baseClass = kwargs.get('baseClass')
        if baseClass is not None:
            del kwargs['baseClass']
        else:
            baseClass = FEvent.Event
        return FEvent.CreateEvent(name, baseClass, self._Instance(), *args, **kwargs)

    def Dispatcher(self):
        return self._dispatcher

    def StartObserving(self, dispatcher=None):
        self._Observer().AddDependent(dispatcher)

    def StopObserving(self, dispatcher=None):
        self._Observer().RemoveDependent(dispatcher)

    def HandleQueuedEvents(self):
        for event in self.EventQueue():
            self.Dispatcher().HandleEvent(self._Instance(), event)
        self.EventQueue().Clear()

    def _Instance(self):
        return self._instance

    def _Observer(self):
        return self._observer

    def _InitObserver(self):
        self._observer = FDispatcher.Observer(
                                            self._Instance(),
                                            self.Dispatcher()
                                            )
