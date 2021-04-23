""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FEvent.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FEvent

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Base class and class hierarchy for common events.
-------------------------------------------------------------------------------------------------------"""

__all__ = [
    'EventQueue',
    'InternalEventCallback',
    'EventCallback',
    'CreateEvent',
    'Event',
    'BaseEvent',
    'OnObjectsSelected',
    'OnInstrumentsSelected',
    'OnCounterpartiesSelected',
    'OnSaveSheetAsTemplate',
    'OnPanelVisibilityChanged',
    'OnError'
    ]


from FIntegratedWorkbenchLogging import logger
from FIntegratedWorkbenchUtils import AsIterable, ClassFactory


class EventQueue(object):

    def __init__(self):
        self._eventQueue = []

    def __iter__(self):
        return iter(self._eventQueue)

    def __bool__(self):
        return bool(self._eventQueue)

    def Add(self, event):
        self._eventQueue = [e for e in self._eventQueue if not isinstance(e, type(event))]
        self._eventQueue.append(event)

    def Clear(self):
        self._eventQueue[:] = []


class EventCallbackBase(object):

    def __init__(self, func):
        self._func = func
        self._instance = None

    def Callback(self, event):
        raise NotImplementedError

    def __call__(self, *args):
        event = self.GetEvent(args)
        if self.IsValid(event):
            return self.Callback(event)
        logger.debug('Non-valid call to {0}: expected '
            'Event as parameter'.format(self.__class__.__name__))

    def __get__(self, instance, _type):
        self._instance = instance
        return self

    @staticmethod
    def GetEvent(args):
        try:
            return args[0]
        except IndexError:
            pass

    @staticmethod
    def IsValid(event):
        return event and isinstance(event, Event)


class InternalEventCallback(EventCallbackBase):

    def __init__(self, func):
        super(InternalEventCallback, self).__init__(func)

    def Callback(self, event):
        return self._func(self._instance, event)


class EventCallback(EventCallbackBase):

    def __init__(self, func):
        super(EventCallback, self).__init__(func)

    def Callback(self, event):
        if self._instance.ReactOnEvent():
            return self._func(self._instance, event)
        self._instance.AddToEventQueue(event)


def CreateEvent(name, baseClass, *args, **kwargs):
    # pylint: disable-msg=W0640
    this = ClassFactory(name, baseClass)(*args, **kwargs)
    for name, value in kwargs.items():
        methodName = ''.join((name[0].upper(), name[1:]))
        setattr(this, methodName, lambda val=value: val)
    return this

class Event(object):

    def __init__(self, sender):
        self._sender = sender

    def Class(self):
        return self.__class__

    def Sender(self):
        return self._sender

class BaseEvent(Event):

    def __init__(self, sender, params=None):
        super(BaseEvent, self).__init__(sender)
        self._parameters = params

    def Parameters(self):
        return self._parameters

class OnObjectsSelected(BaseEvent):

    def __init__(self, sender, selection, params=None):
        super(OnObjectsSelected, self).__init__(sender, params)
        self._selection = AsIterable(selection)

    def Objects(self):
        return self._selection

    def First(self):
        try:
            return self._selection[0]
        except IndexError:
            return None

class OnInstrumentsSelected(OnObjectsSelected):
    pass

class OnCounterpartiesSelected(OnObjectsSelected):
    pass

class OnSaveSheetAsTemplate(BaseEvent):

    def Sheet(self):
        return self.Sender()

class OnPanelVisibilityChanged(BaseEvent):
    def __init__(self, sender, panelName=None, visible=None, params=None):
        super(OnPanelVisibilityChanged, self).__init__(sender, params)
        self._panelName = panelName
        self._visible = visible

    def PanelName(self):
        if self._panelName:
            return self._panelName
        return self.Sender().Name()

    def Visible(self):
        return self._visible


class OnError(BaseEvent):

    def __init__(self, sender, msgBoxType, msg):
        super(OnError, self).__init__(sender)
        self._msgBoxType = msgBoxType
        self._msg = msg

    def Msg(self):
        return self._msg

    def MsgBoxType(self):
        return self._msgBoxType
