""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FIntegratedWorkbenchUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FIntegratedWorkbenchUtils

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    A collection of utility functions used by the Integrated Workbench classes.
-------------------------------------------------------------------------------------------------------"""

__all__ = [
    'Singleton',
    'AsIterable',
    'RemoveDuplicates',
    'ClassFactory',
    'UniqueSizedList',
    'IsKindOf',
    'IsFObject',
    'GetAttributeInModule',
    'GetAttributesInModule'
    ]

import time
import acm

from FIntegratedWorkbenchLogging import logger


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = type.__call__(cls, *args, **kwargs)
        return cls._instances[cls]

def AsIterable(selection):
    try:
        iter(selection)
        return selection
    except TypeError:
        return [selection]

def RemoveDuplicates(objects):
    return list(set(AsIterable(objects)))

def ClassFactory(name, BaseClass=object):
    def __init__(self, *args, **kwargs):
        BaseClass.__init__(self, *args)
    newclass = type(name, (BaseClass, ), {"__init__": __init__})
    return newclass

def Profiler(func):
    def Wrapper(*args, **kwargs):
        t0 = time.time()
        res = func(*args, **kwargs)
        logger.debug('{0} took {1} seconds'.format(func.__name__, time.time()-t0))
        return res
    return Wrapper

class UniqueSizedList(object):

    def __init__(self, maxSize):
        self._items = list()
        self._maxSize = maxSize

    def __iter__(self):
        return iter(self._items)

    def __nonzero__(self):
        return bool(self._items)

    def MaxSize(self):
        return self._maxSize

    def Items(self):
        return self._items

    def AddUnique(self, obj):
        if obj in self._items:
            return
        self._items.append(obj)
        if len(self._items) > self._maxSize:
            self._items.pop(0)

    def Clear(self):
        self._items[:] = []

    def IsDeleted(self):
        return False


def IsKindOf(instance, _acmType):
    return hasattr(instance, 'IsKindOf') and instance.IsKindOf(_acmType)

def IsFObject(instance):
    return IsKindOf(instance, acm.FObject)

def GetAttributeInModule(funcId):
    """ Get an attribute by name on the format <module>.<attribute>. """
    if not isinstance(funcId, str):
        logger.debug("GetAttributeInModule() Invalid function id: '%s'" % (funcId))
        return None
    if (not funcId) or (funcId.find('.') == -1):
        logger.debug("GetAttributeInModule() Invalid attribute id: '%s'" % (funcId))
        return None
    mod, func = None, None
    try:
        mod, func = funcId.split('.')
        return getattr(__import__(mod), func)
    except Exception as stderr:
        logger.error("GetAttributeInModule() Unable to get attribute '%s' in module '%s'" % (func, mod))
        logger.debug(stderr, exc_info=True)
        return None

def GetAttributesInModule(funcIds):
    if isinstance(funcIds, str):
        logger.warn('GetAttributesInModule() got str "%s", expected list' % funcIds)
    attrs = []
    for funcId in AsIterable(funcIds):
        attrs.append(GetAttributeInModule(funcId))
    return attrs

def MessageBoxError(shell, msg):
    acm.UX.Dialogs().MessageBox(shell, 'Error', msg,
        'OK', '', '', 'Button1', 'None')

class LayoutError(Exception):
    pass
