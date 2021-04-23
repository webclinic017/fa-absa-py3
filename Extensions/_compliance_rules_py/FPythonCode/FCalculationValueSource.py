""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FCalculationValueSource.py"
"""--------------------------------------------------------------------------
MODULE
    FCalculationValueSource

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

import acm

from FCalculationSpaceUtils import Space, Calculation, CalculationService
from FComplianceRulesUtils import logger
from FEventUtils import Observable

differential = acm.GetFunction('differential', 3)


class SpaceSource(object):

    def __init__(self, params):
        self.params = params
        self._space = None

    def SheetType(self):
        try:
            return self.params.SheetType()
        except AttributeError:
            return 'FPortfolioSheet'

    def Context(self):
        try:
            return self.params.Context()
        except AttributeError:
            return acm.GetDefaultContext()   

    def CalculationEnvironment(self):
        #TODO: Add CalculationEnvironment to rule definition info
        try:
            return self.params.CalculationEnvironment()
        except AttributeError:
            return None    

    def GridConfiguration(self):
        try:
            return self.params.GridConfiguration()
        except AttributeError:
            return None               

    def IsDistributed(self):
        #TODO: Add UseDistributedCalculations to rule defintion info
        try:
            return self.params.IsDistributed()
        except AttributeError:
            return False

    def InsertItem(self, anObject, grouper=None):
        return self.Space().InsertItem(anObject,
                                              grouper or acm.FDefaultGrouper())

    def Space(self):
        if self._space is None:
            self._space = Space(self.SheetType(),
                                self.Context(),
                                self.CalculationEnvironment(),
                                self.GridConfiguration(), 
                                self.IsDistributed())
        return self._space


class CalculationSource(Observable):

    def __init__(self, node, spaceSource, params):
        super(CalculationSource, self).__init__()
        self._node = node
        self._space = spaceSource.Space()
        self.params = params
        self._calculation = None
        self._baseCalculation = None

    def Value(self):
        value = self._Calculation().Value(self.ProjectionParts())
        displayType = self.ScenarioDisplayType()
        if displayType == 'Relative':
            value = self.Differential(value, self.BaseValue())
        elif displayType == 'Relative Percent':
            value = 100 * self.Differential(value, self.BaseValue(), isRelative=True)
        return value
        
    def BaseValue(self):
        return self._BaseCalculation().Value()

    def ColumnName(self):
        return self.params.ColumnName()

    def CalculationConfiguration(self):
        try:
            return self.params.CalculationConfiguration()
        except AttributeError:
            return None

    def ProjectionParts(self):
        try:
            return self.params.ProjectionParts()
        except AttributeError:
            return None    

    def ScenarioDisplayType(self):
        try:
            return self.params.ScenarioDisplayType()
        except AttributeError:
            return False

    def BaseCalculationConfiguration(self):
        return acm.Sheet.Column().ConfigurationWithoutScenario(self.CalculationConfiguration())            

    def _CreateCalculation(self, config=None):
        return Calculation(self._space, 
                           self._node,
                           self.ColumnName(),
                           config or self.CalculationConfiguration())

    def _Calculation(self):
        if self._calculation is None:
            self._calculation = self._CreateCalculation()
        return self._calculation

    def _BaseCalculation(self):
        if self._baseCalculation is None:
            self._baseCalculation = self._CreateCalculation(config=self.BaseCalculationConfiguration())
        return self._baseCalculation

    def OnObservableStart(self):
        self._Calculation().AddObserver(self)

    def OnObservableEnd(self):
        self._Calculation().RemoveObserver(self)

    @staticmethod
    def Differential(x, y, isRelative=False):
        try:
            if isRelative:
                return differential(x, y, y)
            return differential(x, y)
        except TypeError:
            return float('nan')
        except RuntimeError:
            return float('nan')
            
            
class CalculationSourceCollection(Observable):

    def __init__(self, params):
        super(CalculationSourceCollection, self).__init__()
        self._spaceSource = SpaceSource(params)
        self._params = params
        self._calculations = {}
        
    def GetValue(self, node):
        return self._GetCalcSource(node).Value()

    def InsertItem(self, anObject, grouper=None):
        return self._spaceSource.InsertItem(anObject, grouper)
        
    def OnObservableStart(self):
        for node in self._calculations:
            self._StartObserving(node)

    def OnObservableEnd(self):
        for node, calc in self._calculations.iteritems():
            self._StopObserving(node.Parent())
            calc.RemoveObserver(self)

    def ServerUpdate(self, sender, aspect, param):
        try:
            if str(aspect) == 'Remove' and param:
                self._StopObserving(param)
                self._RemoveNode(param)
            self.NotifyObservers(aspect, param)
        except Exception as err:
            logger.error(err)
            
    def _GetCalcSource(self, node):
        if node.IsKindOf('FCalculation'):
            return node    
        if node not in self._calculations:
            self._calculations[node] = CalculationSource(node, self._spaceSource, self._params)
            if self.IsObserved():
                self._StartObserving(node)
        return self._calculations[node]
        
    def _StartObserving(self, node):
        parent = node.Parent()
        if parent and self not in parent.Dependents():
            parent.AddDependent(self)
        calc = self._calculations.get(node)
        if calc is not None:
            calc.AddObserver(self)
            
    def _StopObserving(self, node):
        if self in node.Dependents():
            node.RemoveDependent(self)
        calc = self._calculations.get(node)
        if calc is not None:
            calc.RemoveObserver(self)
        
    def _RemoveNode(self, node):
        calc = self._calculations.get(node)
        if calc is not None:
            calc.RemoveObserver(self)
            del self._calculations[node] 