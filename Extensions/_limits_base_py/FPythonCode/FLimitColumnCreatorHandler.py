""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitColumnCreatorHandler.py"
"""--------------------------------------------------------------------------
MODULE
    FLimitColumnCreatorHandler

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
-----------------------------------------------------------------------------"""

import acm


class VectorColumn(object):

    def __init__(self, vectorElements):
        self._vectorElements = vectorElements

    def Configuration(self, elementId=None):
        if elementId is None:
            return self._vectorElements
        return self._ConfigurationAt(elementId)
            
    def _ConfigurationAt(self, elementId):
        try:
            for elem in self._vectorElements:
                #Name returns None for FNamedParameters
                #need to use UniqueTag instead
                elemId = elem.Name() or elem.UniqueTag()
                if elemId == elementId:
                    return [elem]
        except TypeError:
            pass
    
    @classmethod
    def FromCalculationSpec(cls, calcSpec):
        vectorElements = cls._VectorElements(calcSpec)
        return cls(vectorElements)

    @classmethod
    def _VectorElements(cls, calcSpec):
        try:
            vectorConfig = cls._VectorConfig(calcSpec)
            return (vectorConfig.At(cls._Dimensions(calcSpec)) or 
                    vectorConfig.At(calcSpec.ColumnName()) or
                    vectorConfig.At('Time Buckets'))
        except AttributeError:
            pass
            
    @classmethod
    def _Dimensions(cls, calcSpec):
        context = acm.FExtensionContext[str(calcSpec.ContextName())]
        columnDef = context.GetExtension('FColumnDefinition', 
                                         'FTradingSheet', 
                                         calcSpec.ColumnName()).Value()
        return columnDef.At('Dimensions')
        
    @staticmethod
    def _VectorConfig(calcSpec):
        try:
            configParams = calcSpec.Configuration().ParamDict()
            return configParams.At('vectorConfig').ParamDict()
        except AttributeError:
            pass


class ColumnCreatorHandler(object):
    
    def __init__(self, limitTarget):
        self._limitTarget = limitTarget
        
    def ColumnCreators(self):
        initialCreators = self._InitialCreators()
        columnConfigCreator = self._NewCreatorFromColumnConfig(initialCreators.At(0))
        if columnConfigCreator:
            return self._NewCreators([columnConfigCreator])
        return initialCreators
    
    def ColumnCreatorsFromScenario(self, scenario):
        columnCreator = self.ColumnCreators().At(0).ApplyScenario(scenario)
        return self._NewCreators([columnCreator])
        
    def Scenario(self):
        try:
            scenarioParams = self._GetScenarioParams()
            return scenarioParams.ExtractCoordinate(self._limitTarget.ProjectionParts())
        except AttributeError:
            pass
    
    def _InitialCreators(self):
        columnId = self._ColumnId()
        columnData = self._ColumnData()
        columnIds = acm.FArray().AddAll([columnId, ])
        return acm.GetColumnCreators(columnIds, 
                                     self._CalculationSpec().ContextName(), 
                                     columnData)
        
    def _CalculationSpec(self):
        return self._limitTarget.CalculationSpecification()
        
    def _ColumnData(self):
        try:
            vectorColumn = VectorColumn.FromCalculationSpec(self._CalculationSpec())
            elementId = self._ElementId(self._limitTarget.ColumnLabel())
            config = vectorColumn.Configuration(elementId)
            return self._CreateColumnData(self._ColumnId(), config)
        except AttributeError:
            pass
    
    def _ConfigParams(self):
        try:
            return self._CalculationSpec().Configuration().ParamDict()
        except AttributeError:
            pass
            
    def _GetScenarioParams(self):
        try:
            configParams = self._ConfigParams()
            return configParams.At('scenario')
        except AttributeError:
            pass
    
    def _GetColumnConfig(self):
        try:
            configParams = self._ConfigParams()
            columnParams = configParams.At('columnParameters')
            if columnParams is not None:
                return acm.Sheet().Column().\
                    CreatorConfigurationFromColumnParameterDefinitionNamesAndValues(columnParams)
        except AttributeError:
            pass

    def _ColumnId(self):
        return self._CalculationSpec().ColumnName()
        
    def _NewCreatorFromColumnConfig(self, initialCreator):
        try:
            columnConfig = self._GetColumnConfig()
            if columnConfig:
                return initialCreator.Template().CreateCreator(columnConfig, None)
            return initialCreator
        except AttributeError:
            pass
    
    @staticmethod
    def _CreateColumnData(columnId, vectorItems):
        columnData = acm.FDictionary()
        columnData.AtPut(columnId, vectorItems)
        return columnData

    @staticmethod
    def _ElementId(columnLabel):
        try:
            return columnLabel.split('-')[-1].strip()
        except (AttributeError, IndexError):
            pass
            
    @staticmethod
    def _NewCreators(creators):
        columnCreators = acm.FColumnCreators()
        for creator in creators:
            columnCreators.Add(creator)
        return columnCreators
