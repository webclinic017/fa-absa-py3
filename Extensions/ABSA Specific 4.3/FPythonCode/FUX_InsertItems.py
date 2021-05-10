'''
Created on 16 Jan 2017

Creates the Insert items frame, with additional types.

@author: conicova
'''
import acm
import FUxCore

def AddSubClasses(cls, arr):
    for subClass in cls.Subclasses():
        if cls.IsEqual(acm.FInstrument) or not cls.IncludesBehavior(acm.FInstrument):
            arr.Add(subClass)
            AddSubClasses(subClass, arr)

def StartIIExtendedCB(eii):
    arr = acm.FArray()
    AddSubClasses(acm.FCommonObject, arr)
    arr.SortByProperty('StringKey', True)
    acm.StartFASQLEditor('Insert Items Extended', arr, None, None, None, '', False, None)
