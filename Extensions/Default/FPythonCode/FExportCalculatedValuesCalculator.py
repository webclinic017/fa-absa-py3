import acm
import collections

import FExportCalculatedValuesWriterCommon as writerCommon 

def _columnLabelsFromCreator(columnCreator):
    columns = columnCreator.Columns() if hasattr(columnCreator, "Columns") else [] 
    return [str(column.Label()) for column in columns]
    
def _calcSpecIsDynamic( columnCreator, calcSpec ):
    vConf = calcSpec.VectorConfiguration()
    if vConf:
        return vConf.FirstUnfixedDynamicDimensionId() is not None
    return acm.Sheet.Column().CalculationSpecificationForDynamicVector(columnCreator) is not None

def _columnCreatorHasStaticColumnName( columnCreator, calcSpec ):
    vConf = calcSpec.VectorConfiguration()
    if vConf:
        return False
    return acm.Sheet.Column().CalculationSpecificationForDynamicVector(columnCreator) is None

def _partNamesFromColumnCreator(columnCreator, calcSpec):
    partNames = None 

    if _columnCreatorHasStaticColumnName( columnCreator, calcSpec ):
        partNames = _columnLabelsFromCreator(columnCreator)
    return partNames

def _vectorInformation(calcSpec):
    if calcSpec.VectorConfiguration():
        return writerCommon.VectorInformation( dimensionNames = calcSpec.VectorConfiguration().DimensionIds() )
    return None
    
def _columnCreatorScenarioInformation(columnCreator, scenarioDimensionNames):
    scenarioInformation = None
    scenario = columnCreator.Scenario() if hasattr(columnCreator, "Scenario") else None
    if scenario is not None:
        cardinalities = [dim.Cardinality() for dim in scenario.ShiftDimensions()] 
        
        if (None not in [cardinalities, scenarioDimensionNames] and
                len(cardinalities) == len(scenarioDimensionNames)):
            
            scenarioName = scenario.Name() if scenario.Name() else None
                
            scenarioInformation = writerCommon.ScenarioInformation(storageName = scenarioName,
                                                                dimensionCardinalities = cardinalities,
                                                                dimensionNames = scenarioDimensionNames)
        else:
            raise Exception('Mismatch in number of dimensions, %s is incorrect for %s' % 
                            (cardinalities, scenarioDimensionNames))
            
    return scenarioInformation
    

def _finalMethodInMethodChain(class_, methodChain):
    nameOfFirstMethodInChain = methodChain.First()
    method = class_.GetMethod(nameOfFirstMethodInChain, 0)
    
    if methodChain.Size() == 1:
        return method
    else:
        return _finalMethodInMethodChain(method.Domain(),
                                         methodChain[1:])
        

_stringDomain= acm.GetDomain('string')

def _actualDomain( domain ):
    if domain.BaseDomain() == _stringDomain:
        return _stringDomain
    return domain

def _domainName(class_, methodChain):
    finalMethod = _finalMethodInMethodChain(class_, methodChain.Split('.'))
    return _actualDomain( finalMethod.Domain() ).DomainName()


def _acmDomainName(itemWithAttributeGrouper):
    try:
        itemClass = itemWithAttributeGrouper.Class()
        if str(itemClass) == "FDistributedRow":
            #Distributed Mode
            if itemWithAttributeGrouper.Instrument():
                return itemWithAttributeGrouper.Instrument().Class().DomainName()
            else:
                attributeGrouper = itemWithAttributeGrouper.GrouperOnLevel()
                if attributeGrouper.IsKindOf( acm.FAttributeGrouper ):
                    return _domainName(attributeGrouper.SubjectClass(),
                                   attributeGrouper.Method())
                else:
                    return itemWithAttributeGrouper.Portfolio().Class().DomainName()
        else:
            if itemClass == acm.FPortfolioInstrumentAndTrades:
                return itemWithAttributeGrouper.Portfolio().Class().DomainName()
            elif itemClass == acm.FMultiInstrumentAndTrades:
                attributeGrouper = itemWithAttributeGrouper.GrouperOnLevel()
                return _domainName(attributeGrouper.SubjectClass(),
                                   attributeGrouper.Method())
            elif itemClass == acm.FSingleInstrumentAndTrades:
                return itemWithAttributeGrouper.Instrument().Class().DomainName()
    except Exception as e:
        raise Exception("Unable to determine ACM type for %s (type %s)" % (
                            itemWithAttributeGrouper,
                            type(itemWithAttributeGrouper)))

def _column_part_name_in_dynamic_column(obj):
    usePreferredMethodForIdentification = obj.Class().GetMethod("Identifier", 0) is not None
    if usePreferredMethodForIdentification:
        name = obj.Identifier()
    else:
        name = obj.StringKey()
    return name

def _custom_coordinate_labels( calcSpec, coordinatePart ):
    dimensions = coordinatePart.Aspect().Key()
    config = calcSpec.Configuration()
    vectorConfig = calcSpec.VectorConfiguration()
    scenario = calcSpec.Scenario()
    labels = acm.FArray()
    for idx, dim in enumerate(dimensions):
        if acm.FSymbol("vectorValue") == dim:
            assert( config.ParamDict()[acm.FSymbol("vectorValue")] )
            labels.Add( coordinatePart.Coordinates()[idx] )
        elif acm.FSymbol("vectorItemValue") == dim:
            assert( config.ParamDict()[acm.FSymbol("vectorItemValue")] )
            labels.Add( coordinatePart.Coordinates()[idx] )
        elif vectorConfig and vectorConfig.VectorDimension( dim ):
            vDim = vectorConfig.VectorDimension( dim )
            labels.Add( vDim.Labels()[ coordinatePart.Coordinates()[idx] ] )
        elif scenario:
            labels.Add( coordinatePart.Coordinates()[idx] )
    return labels

def _calculationProjectionParts( calcSpec ):
    config = calcSpec.Configuration()
    if not config:
        return ([], [acm.FArray()])
    vectorItemValue = config.ParamDict()[acm.FSymbol("vectorItemValue")]
    if vectorItemValue:
        return ([], [_column_part_name_in_dynamic_column(vectorItemValue[0])])
    proj = calcSpec.Project1D()
    parts = calcSpec.CreateAspectCoordinateParts(proj)
    return ( parts, [_custom_coordinate_labels(calcSpec, p) for p in parts] )

def _getCoordinatesAndParts( coordinatesCache, calcSpec ):
    cacheKey = calcSpec.Configuration() or 0
    parts, coordinates = coordinatesCache[ cacheKey ] or (None, None)
    if not parts:
        parts, coordinates = _calculationProjectionParts( calcSpec )
        coordinatesCache[ cacheKey ] = (parts, coordinates)
    return parts, coordinates

def _customProject(value, calcSpec, isStatic, coordinatesCache):
    vectorConf = calcSpec.VectorConfiguration()
    calcInfos = []
    if vectorConf:
        unfixedDimensionsId = vectorConf.FirstUnfixedDynamicDimensionId()
        if unfixedDimensionsId:
            if not value:
                return calcInfos
            for key in value.Keys().Sort():
                refinedSpec = calcSpec.RefinedCalculationSpecification( unfixedDimensionsId, key )
                calcInfos.extend( _customProject( value[ key ], refinedSpec, isStatic, coordinatesCache ) )
            return calcInfos
            
    elif not isStatic:
        if not value:
            return calcInfos
        for key in value.Keys().Sort():
            refinedSpec = calcSpec.RefinedCalculationSpecification( "vectorItemValue", key )
            calcInfos.extend( _customProject( value[ key ], refinedSpec, True, coordinatesCache ) )
        return calcInfos

    parts, coordinates = _getCoordinatesAndParts( coordinatesCache, calcSpec )
    projectedValue = calcSpec.ProjectValue( value, parts )

    if isinstance( projectedValue, collections.Iterable ) and len(parts) > 0:
        for idx, value in enumerate( projectedValue ):
            calcInfos.append( writerCommon.CalculationInformation( coordinates[idx], value ) )
    else:
        calcInfos.append( writerCommon.CalculationInformation( coordinates[0], value ) )
    return calcInfos

def _createCalculationInformations( space, tree, calcSpec, coordinatesCache, isDynamic):
    value = space.CalculateValue( tree, calcSpec.ColumnName(), calcSpec.Configuration(), False )
    return _customProject(value, calcSpec.Clone(), not isDynamic, coordinatesCache)

def _createCalculationInformationsFromCalculation( calculation, calcSpec, coordinatesCache, isDynamic ):
    value = calculation.ValueOrException()
    return _customProject(value, calcSpec.Clone(), not isDynamic, coordinatesCache)

class Calculator(object):
    def __init__(self, runDefinition):
        self._runDefinition = runDefinition
        self._cachedCalculationSpace = None
        self._coordinatesCache = acm.FDictionary()
        
    def RootPositions(self):
        for portfolio in self._portfolios():
            rootPosInfo = writerCommon.RootPositionInformation(name = portfolio.Name(),
                                                               acmDomainName = portfolio.Class().DomainName())
            yield (rootPosInfo,  self._rootPosInfoID(rootPosInfo))

    def _portfolios(self):
        portfolios = []
        for name in self._runDefinition.portfolioNames:
            portfolios.append(acm.FPhysicalPortfolio[name])
        for name in self._runDefinition.tradeFilterNames:
            portfolios.append(acm.FTradeSelection[name])
        for name in self._runDefinition.storedASQLQueryNames:
            portfolios.append(acm.FStoredASQLQuery.Select01('user=0 and name=' + name, ''))

        assert len(portfolios) > 0
        return portfolios

    def _rootPosInfoID(self, info):
        return (info.name, info.acmDomainName)

    def Positions(self):
        space = self._calculationSpace()
        
        parentInfoIDs = [None] # Stack-like structure to leave a trace of the parent to child nodes
        
        iterator = space.RowTreeIterator()
        
        rootPositionInfoAndIdPairs = [rootPositionInfoAndId for rootPositionInfoAndId in self.RootPositions()]
        
        
        latestRootPositionID = None
        
        while iterator.NextUsingDepthFirst():
            currDepth = iterator.Tree().Depth()
            dimensionIndex = currDepth-1
            parentInfoIDIndex = currDepth-1
            item = iterator.Tree().Item()
            
            #Update the current root position ID
            if currDepth == 1:
                name = item.StringKey()
                acmDomainName = _acmDomainName(item)
                for (rootPosition, rootPosinfoID) in rootPositionInfoAndIdPairs:
                    if name == rootPosition.name and acmDomainName == rootPosition.acmDomainName:
                        latestRootPositionID = rootPosinfoID
                      
            positionInfo = writerCommon.PositionInformation(
                                    rootPositionInformationID = latestRootPositionID,
                                    parentInfoID = parentInfoIDs[parentInfoIDIndex],
                                    name = item.StringKey(),
                                    acmDomainName = _acmDomainName(item),
                                    dimensionName = self._chainedGrouperDefinition().DimensionLabel(dimensionIndex))
            ownID = self._posInfoID(positionInfo)
            
            while (len(parentInfoIDs) > currDepth):
                parentInfoIDs.pop()
            parentInfoIDs.append(ownID)
            
            yield (positionInfo, ownID)
   
    def _calculationSpace(self):
        if self._cachedCalculationSpace is None:
            spaceCollection = acm.Calculations().CreateCalculationSpaceCollection(self._runDefinition.calculationEnvironment)
            space = spaceCollection.GetSpace(acm.FPortfolioSheet,
                                            acm.GetDefaultContext().Name(),
                                            None,
                                            self._runDefinition.distributedMode)
                                            
            for (rootPosInfo, rootInfoID) in self.RootPositions():
                
                pf = acm.GetClass(rootPosInfo.acmDomainName)[rootPosInfo.name]
                
                top_node = space.InsertItem(pf)
                top_node.ApplyGrouper(self._grouper())
                
            space.Refresh()
            self._cachedCalculationSpace = space
        return self._cachedCalculationSpace
            
    def _grouper(self):
        return self._chainedGrouperDefinition().AsPortfolioSheetGrouper()

    def _chainedGrouperDefinition(self):
        return self._runDefinition.chainedGrouperDefinition
    
    def _posInfoID(self, info):
        return (info.rootPositionInformationID, info.parentInfoID, info.name)

    def Columns(self):
        for columnInfo in self._columnInformations(self._runDefinition.columnConfigurations):
            yield (columnInfo, self._columnInfoID(columnInfo))
    
    def _columnInformations(self, columnConfigurations):
        rv = []
        
        for columnConfiguration in columnConfigurations:
            columnCreator = columnConfiguration.columnCreator
            calcSpec = columnConfiguration.calculationSpecification
            
            name = columnConfiguration.customColumnName
            columnID = columnConfiguration.columnID
            scenarioDimensionNames = columnConfiguration.scenarioDimensionNames
            columnPartNames = _partNamesFromColumnCreator(columnCreator, calcSpec)
            rv.append(writerCommon.ColumnInformation(
                         name = name,
                         columnID = columnID,
                         columnPartNames = columnPartNames,
                         isDynamic = _calcSpecIsDynamic(columnCreator, calcSpec),
                         scenarioInformation = _columnCreatorScenarioInformation(
                                                    columnCreator,
                                                    scenarioDimensionNames),
                         vectorInformation = _vectorInformation(calcSpec)))
        return rv

    def _columnInfoID(self, columnInfo):
        return columnInfo.name

    def ValuesDistributed( self ):
        values = []
        space = self._calculationSpace()
        calculationSpecifications = []
        for (columnInfo, columnInfoID) in self.Columns():
            calcSpec = self._calcSpec(columnInfo.name)
            calculationSpecifications.append( (calcSpec, columnInfoID, columnInfo.isDynamic ) )
        iterator = space.RowTreeIterator()
        positionGenerator = self.Positions()
        while iterator.NextUsingDepthFirst():
            (posInfo, posInfoID) = positionGenerator.next()
            tree = iterator.Tree()
            if self._shouldPerformCalculation(tree.Depth()):
                assert posInfo.name == tree.Item().StringKey()
                for (calcSpec, columnInfoID, isDynamic) in calculationSpecifications:
                    calculation = space.CreateCalculation(tree, calcSpec.ColumnName(), calcSpec.Configuration())
                    values.append( (posInfoID, columnInfoID, calcSpec, calculation, isDynamic) )
                   
        space.Refresh()
        for (posInfoID, columnInfoID, calcSpec, calculation, isDynamic) in values:
            calcInfos = _createCalculationInformationsFromCalculation( calculation, calcSpec, self._coordinatesCache, isDynamic )
            yield ( posInfoID, columnInfoID, calcInfos )        
        
    def ValuesLocal( self ):
        space = self._calculationSpace()
        calculationSpecifications = []
        for (columnInfo, columnInfoID) in self.Columns():
            calcSpec = self._calcSpec(columnInfo.name)
            calculationSpecifications.append( (calcSpec, columnInfoID, columnInfo.isDynamic ) )
        iterator = space.RowTreeIterator()
        positionGenerator = self.Positions()
        while iterator.NextUsingDepthFirst():
            (posInfo, posInfoID) = positionGenerator.next()
            tree = iterator.Tree()
            if self._shouldPerformCalculation(tree.Depth()):
                assert posInfo.name == tree.Item().StringKey()
                for (calcSpec, columnInfoID, isDynamic) in calculationSpecifications:
                    try:
                        calcInfos = _createCalculationInformations( space, tree, calcSpec,
                                self._coordinatesCache, isDynamic )
                        yield ( posInfoID, columnInfoID, calcInfos )
                    except Exception as e:
                        if self._runDefinition.logger:
                            msg = "Failed to calculate column '%s' for position '%s'. '%s'" % (columnInfoID, posInfo.name, str(e))
                            self._runDefinition.logger.ELOG( msg )
        
    def Values(self):
        if self._runDefinition.distributedMode:
            return self.ValuesDistributed()
        else:
            return self.ValuesLocal()
                
    def _calcSpec(self, name):
        xs = [cc.calculationSpecification for cc in self._runDefinition.columnConfigurations if cc.customColumnName == name]
        assert len(xs) == 1
        return xs[0]
       
    def _shouldPerformCalculation(self, treeDepth):
        # -1 to offset for "sheet root level" which is at depth 0
        dimensionLevel = treeDepth - 1
        return self._chainedGrouperDefinition().DimensionIsRequired(dimensionLevel)
