import acm
import FUxCore

import FExportCalculatedValuesCalculator
reload( FExportCalculatedValuesCalculator )

class CalcInfo( object ):
    def __init__( self, calcSpec, isDynamic, dimensions, coordinateLabels ):
        self.m_calcSpec = calcSpec
        self.m_isDynamic = isDynamic
        self.m_dimensions = tuple(dimensions)
        self.m_coordinateLabels = coordinateLabels

class CalcInfoCollection( object ):
    def __init__( self ):
        self.m_calcInfos = []
        
    def AddCalcInfo( self, calcInfo ):
        self.m_calcInfos.append( calcInfo )

class DimensionalityData( object ):
    def __init__( self ):
        self.m_coordinates = []
        self.m_data = acm.FOrderedDictionary()
        
class SourceData( object ):
    def __init__( self, sourceObject, calcInfoCollection, cs ):
        self.m_sourceObject = sourceObject
        self.m_cs = cs
        self.m_calcInfoCollection = calcInfoCollection

        self.m_calcs = []
        self.m_dependents = []
        
        self.m_dataByDimensionality = {}
        
    def ReInitialize( self ):
        for calc in self.m_calcs:
            calc.RemoveDependent( self )
        del self.m_calcs[:]
        self.m_dataByDimensionality.clear()
        
        for calcInfo in self.m_calcInfoCollection.m_calcInfos:
            self.m_dataByDimensionality[ calcInfo.m_dimensions ] = DimensionalityData()
            cs = calcInfo.m_calcSpec
            calc = self.m_cs.CreateCalculation( self.m_sourceObject, cs.ColumnName(), cs.Configuration() )
            calc.AddDependent( self )
            self.m_calcs.append( calc )
            
    def Populate( self ):
        
        for calc, calcInfo in zip(self.m_calcs, self.m_calcInfoCollection.m_calcInfos):
            data = self.m_dataByDimensionality[ calcInfo.m_dimensions ]
            for cInfo in FExportCalculatedValuesCalculator._customProject(calc.Value(), calcInfo.m_calcSpec, not calcInfo.m_isDynamic, acm.FDictionary()):
                if type(cInfo.projectionCoordinates) == str:
                    coordinates = [acm.FSymbol( cInfo.projectionCoordinates ) ]
                else:
                    coordinates = []
                    for idx, coordinate in enumerate( cInfo.projectionCoordinates ):
                        customCoordinates = calcInfo.m_coordinateLabels[ calcInfo.m_dimensions[idx] ]
                        if customCoordinates:
                            coordinates.append( acm.FSymbol( customCoordinates[coordinate] ) )
                        else:
                            coordinates.append( acm.FSymbol( coordinate ) )
                value = cInfo.values
                data.m_data[ coordinates ] = value
                data.m_coordinates.append( coordinates )
        
    def Coordinates( self, dimensionId, path ):
        coordinatesSet = set()
        coordinates = []
        idx = None
        for dimensions in self.m_dataByDimensionality:
            data = self.m_dataByDimensionality[ dimensions ]
            if dimensionId:
                if str(dimensionId) in dimensions:
                    idx = dimensions.index( str(dimensionId) )
            for coords in data.m_coordinates:
                ok = True
                for pathDim in path.Keys():
                    pathDimIdx = None
                    if str(pathDim) in dimensions:
                        pathDimIdx = dimensions.index( str( pathDim ) )
                    if pathDimIdx is not None and str(coords[ pathDimIdx ]) != str(path[ pathDim ]):
                        ok = False
                if ok:
                    coord = coords[ idx ] if idx is not None and idx < len(coords) else None
                    if coord is not None and not coord in coordinatesSet:
                        coordinates.append( coord )
                        coordinatesSet.add( coord )
        return coordinates
    
    def GetValue( self, coordinateByDimension ):
        for dimensions in self.m_dataByDimensionality:
            if len(dimensions) == coordinateByDimension.Size():
                key = acm.FVariantArray()
                for dim in dimensions:
                    coord = coordinateByDimension[ str(dim) ]
                    if coord:
                        key.Add( acm.FSymbol( coord ) )
                data = self.m_dataByDimensionality[ dimensions ]
                if data.m_data[key]:
                    return data.m_data[key]
    
    def Recalculate( self ):
        self.ReInitialize()
        self.Populate()
        
    def AddDependent( self, dependent ):
        self.m_dependents.append( dependent )
        
    def ServerUpdate( self, sender, aspect, param ):
        for dep in self.m_dependents:
            dep.ServerUpdate( sender, aspect, param )
        
    def HandleDestroy( self ):
        for calc in self.m_calcs:
            calc.RemoveDependent( self )
        del self.m_calcs[:]
        
class XAxisColumnCreator( object ):
    def __init__( self, xAxisDimension, sourceData ):
        self.m_axisDimension = xAxisDimension 
        self.m_sourceData = sourceData
    
    def Coordinates( self ):
        if self.m_axisDimension:
            return self.m_sourceData.Coordinates( self.m_axisDimension, acm.FDictionary() )
        else:
            return [None]
        
    def CreateColumns( self, grid ):
        if self.m_axisDimension:
            if self.m_sourceData:
                grid.ShowColumnHeaders( True )
                for lbl in self.m_sourceData.Coordinates( self.m_axisDimension, acm.FDictionary() ):
                    grid.AddColumn( lbl, 50 )
        else:
            grid.AddColumn( "Value", 220 )

    def Dimension( self ):
        return self.m_axisDimension
        
class Projection( object ):

    def __init__( self, name, columnCreator, sourceData, yAxisDimensions ):

        self.m_name  = name
        self.m_sourceData = sourceData
        self.m_columnCreator = columnCreator
        self.m_sourceData.AddDependent( self )
        
        self.m_tree = acm.FOrderedDictionary()
        self.m_values = acm.FOrderedDictionary()

        self.m_rowDimensions = yAxisDimensions
        
        self.m_dependents = []
        self.Project()
        
    def HandleDestroy( self ):
        self.m_sourceData.HandleDestroy()

    def CreateTreeRecursive( self, dimIdx, tree, path ):
        if len( self.m_rowDimensions ) == 0:
            tree[" "] = acm.FOrderedDictionary()
        elif dimIdx < len( self.m_rowDimensions ):
            dimension = self.m_rowDimensions[dimIdx]
            coordinates = self.m_sourceData.Coordinates( dimension, path )
            for coord in coordinates:
                newItem =  acm.FOrderedDictionary()
                tree[ coord ] = newItem
                newPath = path.Clone()
                newPath[str(dimension)] = coord
                self.CreateTreeRecursive( dimIdx + 1, newItem, newPath )
                
    def FillValues( self, dimIdx, tree, values, coordinates ):
        dimensions = self.m_rowDimensions
        for node in tree.Keys():
            dimension = None
            if dimIdx < len(self.m_rowDimensions):
                dimension = dimensions[dimIdx]
                coordinates[dimension] = node
            values[node] = acm.FDictionary()
            values[node]["values"] = acm.FArray()
            values[node]["children"] = acm.FOrderedDictionary()
            for xCoordinate in self.m_columnCreator.Coordinates():
                if self.m_columnCreator.Dimension():
                    coordinates[self.m_columnCreator.Dimension()] = xCoordinate
                value = self.m_sourceData.GetValue( coordinates )
                values[node]["values"].Add( value )
                    
            self.FillValues( dimIdx + 1, tree[node], values[node]["children"], coordinates )
            if dimension:
                coordinates.RemoveKey( dimension )
            
            
    def Project( self ):
        self.m_tree.Clear()
        self.CreateTreeRecursive( 0, self.m_tree, acm.FDictionary() )
        self.m_values.Clear()
        self.FillValues( 0, self.m_tree, self.m_values, acm.FDictionary() )
        
    def RemoveDependent( self, dependent ):
        self.m_dependents.remove( dependent )

    def AddDependent( self, dependent ):
        self.m_dependents.append( dependent )

    def ServerUpdate( self, sender, aspect, param ):
        for dep in self.m_dependents:
            dep.ServerUpdate( sender, aspect, param )

class Grid( object ):
    def __init__( self ):
        self.m_isDirty = False
        self.m_gridCtrl = None
        self.m_projection = None
        
    def HandleCreate( self, layout ):
        self.m_gridCtrl = layout.GetControl( 'grid' )
        self.SetValues()
        
    def CreateLayout( self, builder ):
        builder.  AddGrid( 'grid', 600, 200 )
    
    def SetColumnsAutoWidth(self):
        columnIterator = self.m_gridCtrl.GridColumnIterator()
        while columnIterator.Next():
            columnIterator.GridColumn().Width( -1 )

    def SetValuesRecursive( self, data, root ):
        
        for dataKey in data.Keys():
            newTreeItem = None
            newTreeItemIt = root.Iterator().Find( dataKey )
            if newTreeItemIt:
                newTreeItem = newTreeItemIt.Tree()
            if not newTreeItem:
                newTreeItem = root.AddChild()
                if newTreeItem.Depth() < 2:
                    newTreeItem.Expand( True )
                newTreeItem.Label( dataKey )
            nodeData = data[ dataKey ]
            values = nodeData["values"]
            idx = 0
            columnIterator = self.m_gridCtrl.GridColumnIterator()
            while columnIterator.Next():
                if idx < values.Size():
                    cell = newTreeItem.GetCell( columnIterator.GridColumn() )
                    cell.SetData( values[idx] )
                    
                idx += 1
            
            self.SetValuesRecursive( nodeData["children"], newTreeItem )
            
    def SetValues( self ):
        if self.m_projection:
            root = self.m_gridCtrl.GetRootItem()
            root.Label("")
            self.SetValuesRecursive( self.m_projection.m_values, root )
        
    def ServerUpdate( self, sender, aspect, param ):
        self.m_isDirty = True
        
    def Refresh( self ):
        self.m_projection.m_sourceData.Recalculate()
        self.m_projection.Project()
        self.SetValues()
        self.m_isDirty = False
        
    def IsDirty( self ):
        return self.m_isDirty

    def SetProjection( self, projection ):
        if self.m_projection:
            self.m_projection.RemoveDependent( self )
        self.m_projection = projection
        self.m_projection.AddDependent( self )

        self.m_gridCtrl.RemoveAllItems()

        columnIterator = self.m_gridCtrl.GridColumnIterator()
        gridColumns = []
        while columnIterator.Next():
            gridColumns.append( columnIterator.GridColumn() )
        for gridColumn in gridColumns:
            self.m_gridCtrl.RemoveColumn( gridColumn )
        
        self.m_projection.m_sourceData.Recalculate()
        self.m_projection.m_columnCreator.CreateColumns( self.m_gridCtrl )
        self.m_projection.Project()
        self.m_gridCtrl.RowHeaderColumn().Width( 200 )
        
        self.SetValues()
    
    def ExpandedNodes( self ):
        treeIterator = self.m_gridCtrl.RowTreeIterator()
        expanded = set()
        while treeIterator.NextUsingDepthFirst():
            if treeIterator.Tree().IsExpanded():
                expanded.add( treeIterator.Tree() )
        return expanded
    
class CustomRiskDialog( FUxCore.LayoutDialog ):

    def __init__( self, projections ):
        self.m_projections = projections
        self.m_grid = Grid()
        self.m_expandedNodes = set()
        self.m_adjusted = False
        
    def HandleDestroy( self ):
        for grid in self.m_projections:
            grid.HandleDestroy()
        self.m_grid = None
        
    def OnTimer( self, ud ):
        self.m_refreshBtn.Enabled( self.m_grid.IsDirty() )

        if not self.m_adjusted:
            self.m_grid.SetColumnsAutoWidth()
            self.m_adjusted = True
            
        currentExpandedNodes = self.m_grid.ExpandedNodes()
        expNodesCopy = set( currentExpandedNodes )
        for node in self.m_expandedNodes:
            if node in expNodesCopy:
                expNodesCopy.remove( node )
        if len( expNodesCopy ) > 0:
            self.m_adjusted = False
        self.m_expandedNodes = currentExpandedNodes
        
    def OnChoiceChanged( self, ud, cd ):
        selected = self.m_gridChoicListCtrl.GetSelectedItem().GetData() if self.m_gridChoicListCtrl.GetSelectedItem() else None
        for projection in self.m_projections:
            if projection.m_name == selected:
                self.m_grid.SetProjection( projection )
                
    def OnRefresh( self, ud, cd ):
        self.m_grid.Refresh()
        
    def OnClose( self, ud, cd ):
        self.HandleCancel()
    
    def HandleCreate(self, dlg, layout):
        self.m_grid.HandleCreate( layout )
        self.m_gridChoicListCtrl = layout.GetControl( 'gridChoiceList' )
        self.m_gridChoicListCtrl.Populate( [p.m_name for p in self.m_projections] )
        self.m_gridChoicListCtrl.AddCallback( 'SelectionChanged', self.OnChoiceChanged, None )
        self.m_gridChoicListCtrl.SetSelectedItems( [self.m_gridChoicListCtrl.GetRootItem().FirstChild()] )
        
        self.m_closeBtn = layout.GetControl( 'close' )
        self.m_closeBtn.AddCallback( 'Activate', self.OnClose, None )
        
        self.m_refreshBtn = layout.GetControl( 'refresh' )
        self.m_refreshBtn.Enabled( False )
        self.m_refreshBtn.AddCallback( 'Activate', self.OnRefresh, None )
        
        dlg.RegisterTimer(self.OnTimer, 100)
        
    def CreateLayout( self ):
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        builder.  BeginHorzBox()
        builder.    AddList( 'gridChoiceList', 5, -1, 30, 30 )
        self.m_grid.CreateLayout( builder )
        builder.  EndBox()
        builder.  BeginHorzBox()
        builder.    AddButton( 'refresh', "Refresh" )
        builder.    AddFill()
        builder.    AddButton( 'close', "Close" )
        builder.  EndBox()
        builder.EndBox()
        return builder 

def StandardTimeBuckets():
    bucketDefinitions =[]
    for datePeriod in ['1D', '1M', '3M', '6M', '1Y', '2Y', '3Y', '4Y', '5Y', '7Y', '10Y', '15Y', '20Y']:
        bucketDefinition = acm.FDatePeriodTimeBucketDefinition()
        bucketDefinition.DatePeriod( datePeriod )
        bucketDefinitions.append(bucketDefinition)
    bucketDefinitions.append(acm.FRestTimeBucketDefinition())
    definition = acm.TimeBuckets().CreateTimeBucketsDefinition(0, bucketDefinitions, False, False, False, False, False)
    definitionAndConfiguration = acm.TimeBuckets().CreateTimeBucketsDefinitionAndConfiguration(definition)
    return acm.TimeBuckets().CreateTimeBuckets(definitionAndConfiguration)
    
class ProjectionDefinition( object ):
    def __init__( self, name ):
        self.m_name = name
        self.m_calcInfoCollection = CalcInfoCollection()
        self.m_xAxisDimension = None
        self.m_yAxisDimensions = []
        
    def AddCalcInfo( self, calcInfo ):
        self.m_calcInfoCollection.AddCalcInfo( calcInfo )

    def SetXAxis( self, xAxis ):
        self.m_xAxisDimension = xAxis
        
    def AddYAxis( self, yAxis ):
        self.m_yAxisDimensions.append( yAxis )

def FXDeltaDefinition( contextName, trade ):
    
    definition = ProjectionDefinition("FX Delta Cash")
    colId = 'Portfolio FX Delta Cash'
    config = DisplayCurrencyConfiguration( trade )
     
    units = acm.GetFunction("instrumentAndTradesDiscountingUnits", 4)( trade.Instrument(), [trade], acm.Time().DateToday(), acm.GetFunction('tradeStatusInclusionMaskStandard', 2)(True, True) )
    
    currencies = acm.GetFunction("currenciesFromInstrumentAndTradesDiscountingUnits", 1)( units )

    dimId = "Dim1"
    customCoordinates = acm.FDictionary()
    customCoordinates[dimId] = acm.FArray()
    npa = []
    for currency in currencies:
        np = acm.FNamedParameters()
        np.UniqueTag( currency.Name() )
        np.AddParameter( "currency", currency )
        npa.append( np )
        customCoordinates[dimId].Add( currency.Name() )
    
    config = acm.Sheet().Column().ConfigurationFromVector( npa, config )

    calcInfo = CalcInfo( acm.Sheet().Column().CreateCalculationSpecification( config, colId, contextName ), False, [dimId], customCoordinates )
    definition.AddCalcInfo( calcInfo )
    definition.AddYAxis( dimId )
    return definition
    
def BenchmarkDeltaDefinition( contextName, trade ):
    definition = ProjectionDefinition("Benchmark Delta")
    colId = 'Position Benchmark Delta'
    
    d = acm.FDictionary()
    d["PositionReportCurrency"] = trade.Instrument().Currency()

    baseConfig = acm.Sheet().Column().ConfigurationFromColumnParameterDefinitionNamesAndValues( d )
    colDef = acm.Risk().CreateLiveColumnDefinition( colId, contextName )
    dimDefByExtId = colDef.OptionalDimensionDefinitionsByLogicalName()
    
    for dp in [["Currency", "Yield Curve", "Benchmark Instrument"], ["Currency", "Yield Curve"], ["Currency"]]:
        params = {}
        params["dimensions"] = acm.FArray()
        for xx in dp:
            dimData = acm.FDictionary()
            dimData["externalId"] = xx
            dimData["dimDefName"] = dimDefByExtId[xx].Name()
            params["dimensions"].Add( dimData )
            
        vConfig = acm.Risk().CreateDynamicVectorConfiguration( contextName, 'VectorConfiguration', params )
        config = acm.Sheet().Column().ConfigurationFromVectorConfiguration( vConfig, baseConfig )
        calcInfo = CalcInfo( acm.Sheet().Column().CreateCalculationSpecification( config, colId, contextName ), True, dp, acm.FDictionary() )
        definition.AddCalcInfo( calcInfo ) 
    definition.AddYAxis( "Currency" )
    definition.AddYAxis( "Yield Curve" )
    definition.AddYAxis( "Benchmark Instrument" )
    return definition
    
def YieldDeltaDefinition( contextName, trade ):
    definition = ProjectionDefinition("Yield Delta")
    colId = "Position Interest Rate Yield Delta"

    d = acm.FDictionary()
    d["PositionReportCurrency"] = trade.Instrument().Currency()

    baseConfig = acm.Sheet().Column().ConfigurationFromColumnParameterDefinitionNamesAndValues( d )
    colDef = acm.Risk().CreateLiveColumnDefinition( colId, contextName )
    dimDefByExtId = colDef.OptionalDimensionDefinitionsByLogicalName()
    
    for dp in [["Currency", "Yield Curve", "Time Bucket"], ["Currency", "Time Bucket"]]:
        params = {}
        params["dimensions"] = acm.FArray()
        for xx in dp:
            dimData = acm.FDictionary()
            dimData["externalId"] = xx
            dimData["dimDefName"] = dimDefByExtId[xx].Name()
            if xx == "Time Bucket":
                dimData["coordinatesParams"] = StandardTimeBuckets()
            params["dimensions"].Add( dimData )
            
        vConfig = acm.Risk().CreateDynamicVectorConfiguration( contextName, 'VectorConfiguration', params )
        config = acm.Sheet().Column().ConfigurationFromVectorConfiguration( vConfig, baseConfig )
        calcInfo = CalcInfo( acm.Sheet().Column().CreateCalculationSpecification( config, colId, contextName ), True, dp, acm.FDictionary() )
        definition.AddCalcInfo( calcInfo ) 
    definition.SetXAxis( "Time Bucket" )
    definition.AddYAxis( "Currency" )
    definition.AddYAxis( "Yield Curve" )

    return definition

def VegaDefinition( contextName, trade ):
    definition = ProjectionDefinition( "Vega" )

    colId = 'Portfolio Vega Implicit Per Volatility Structure Vertical'
    
    config = DisplayCurrencyConfiguration( trade )
    calcInfo = CalcInfo( acm.Sheet().Column().CreateCalculationSpecification( config, colId, contextName ), True, ["dimId"], acm.FDictionary() )
    definition.AddCalcInfo( calcInfo )
    definition.AddYAxis( "dimId" )
    return definition
    
def ThValDefinition( contextName, trade ):
    definition = ProjectionDefinition( "Theoretical Value" )
    colId = 'Portfolio Theoretical Value'
    config = DisplayCurrencyConfiguration( trade )
    calcInfo = CalcInfo( acm.Sheet().Column().CreateCalculationSpecification( config, colId, contextName ), False, [], acm.FDictionary() )
    definition.AddCalcInfo( calcInfo )
    return definition

_s_cb = { "benchmark curve" : BenchmarkDeltaDefinition,
"fx matrix" : FXDeltaDefinition,
"volatility information" : VegaDefinition,
"yield curve" : YieldDeltaDefinition
}
def CreateProjectionDefinitionFromRiskFactorGroup( riskFactorGroup, contextName, trade ):
    return _s_cb[ riskFactorGroup ]( contextName, trade )


def DisplayCurrencyConfiguration( trade ):
    d = acm.FDictionary()
    d["AggCurrChoice"] = 'Fixed Curr'
    d["PosCurrChoice"] = 'Fixed Curr'
    d["FixedCurr"] = trade.Instrument().Currency()
    return acm.Sheet().Column().ConfigurationFromColumnParameterDefinitionNamesAndValues( d )

def CreateDialogX( sourceObject, shell ):
    contextName = acm.ExtensionTools().GetDefaultContext().Name()
    cs = acm.Calculations().CreateCalculationSpace( contextName, acm.FPortfolioSheet )

    riskFactors = ["benchmark curve", "yield curve", "fx matrix", "volatility information"]

    npa = []
    for rfgroup in riskFactors:
        np = acm.FNamedParameters()
        np.UniqueTag( rfgroup )
        np.AddParameter( "rfgroup", rfgroup )
        npa.append( np )
    config = DisplayCurrencyConfiguration( sourceObject )
    calc = cs.CreateCalculation( sourceObject, 'Is Sensitive To', acm.Sheet().Column().ConfigurationFromVector( npa, config ) )
    projections = []
    projDef = ThValDefinition( contextName, sourceObject )
    sourceData = SourceData( sourceObject, projDef.m_calcInfoCollection, cs )
    projection = Projection( projDef.m_name, XAxisColumnCreator( projDef.m_xAxisDimension, sourceData ), sourceData, projDef.m_yAxisDimensions )
    projections.append( projection )
    
    for rfg, enabled in zip( riskFactors, calc.Value() ):
        if enabled:
            projDef = CreateProjectionDefinitionFromRiskFactorGroup( rfg, contextName, sourceObject )
            if projDef:
                sourceData = SourceData( sourceObject, projDef.m_calcInfoCollection, cs )
                projection = Projection( projDef.m_name, XAxisColumnCreator( projDef.m_xAxisDimension, sourceData ), sourceData, projDef.m_yAxisDimensions )
                projections.append( projection )
    
    dlg = CustomRiskDialog( projections )

    acm.UX().Dialogs().ShowCustomDialog( 
        shell, 
        dlg.CreateLayout(),
        dlg
    )

class MenuItem(FUxCore.MenuItem):
    def __init__(self, extObj):
        self.m_extObj = extObj
    
    def IsMenuEnabled(self, extObj):
        return True
        
    def Invoke(self, eii):
        extObj = eii.ExtensionObject()
        if self.IsMenuEnabled(extObj):
            ins = extObj.OriginalInstrument()
            shell = eii.ExtensionObject().Shell()
            CreateDialogX( extObj.EditTrade(), shell )
        else:
            pass
        
    def Enabled(self):
        return True
        
    def Applicable(self):
        return True
        
def CreateDialog(extObj):
    return MenuItem(extObj)
    
