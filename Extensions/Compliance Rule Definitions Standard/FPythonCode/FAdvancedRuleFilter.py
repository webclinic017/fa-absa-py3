""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRuleDefinitionsStandard/./etc/FAdvancedRuleFilter.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FAdvancedRuleFilter

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Functionality for creating advanced trade filters in exposure rules 
    using python. To create own defined trade filter that will be listed
    in the drop down list of python filters:
    
    1) import AdvancedFilter class and decorate the custom function with 
        AdvancedFilter, for example:
        
        @AdvancedFilter
        def IssuersOverFivePercent(valueProvider):
            ...
            return TradeASQLQuery
            
    2) Launch compliance Rule editor and use detailed mode for an Exposure
       Rule to view and set the advanced filter on the rule.
    

-------------------------------------------------------------------------------------------------------"""
from itertools import chain
import acm
import FGrouperUtils

class AdvancedFilter(object):
    
    _filterMethods = []

    def __init__(self, func):
        self._func = func
        if self._func not in self.__class__._filterMethods:
            self.__class__._filterMethods.append(self._func)
            
    @classmethod
    def GetFilterMethods(cls):
        return cls._filterMethods
        
    def __call__(self, *args):
        return self._func(*args)


