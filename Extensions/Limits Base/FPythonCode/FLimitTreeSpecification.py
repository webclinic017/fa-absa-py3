""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitTreeSpecification.py"
"""--------------------------------------------------------------------------
MODULE
    FLimitTreeSpecification

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    

-----------------------------------------------------------------------------"""
import acm


class LimitTreeSpecification(object):

    _processedCells = {}

    def __init__(self, cell):
        self._cell = cell
        
    def TreeSpecification(self):
        if self._cell not in self._processedCells:
            spec = (self._cell.TreeSpecification() or 
                    self.CreateTreeSpecification(self._cell.RowObject()))
            self._processedCells[self._cell] = spec
        return self._processedCells[self._cell]

    @staticmethod
    def CreateTreeSpecification(rowObject):
        return acm.Limits.TreeSpecificationForObject(rowObject)
        
    @staticmethod
    def IsNative(spec):
        try:
            return (spec.OriginObject() and 
                    spec.GroupingSubjectClass() and 
                    spec.Grouper())
        except AttributeError:
            return False
