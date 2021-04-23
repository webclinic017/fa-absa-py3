import FExportCalculatedValuesRunDefinition as run_def
import FExportCalculatedValuesPublisher as pub
import FExportCalculatedValuesCalculator as calc
import importlib

importlib.reload(run_def)
importlib.reload(pub)
importlib.reload(calc)

import acm

from collections import namedtuple

ColumnConfiguration = namedtuple('ColumnConfiguration',
                               ['customColumnName',
                                'columnID',
                                'calculationSpecification',
                                'scenarioDimensionNames',
                                'columnCreator'])


def _createColumnConfiguration(name, columnCreator, scenario, parameters, timebuckets, vector, scenarioDimensionNames, vectorConfiguration):
    calcSpec = acm.Sheet.Column().CalculationSpecificationForColumn(columnCreator)

    config = calcSpec.Configuration()
    
    if vectorConfiguration is not None:
        config = acm.Sheet.Column().ConfigurationFromVectorConfiguration(
            vectorConfiguration,
            config)
            
    if scenario is not None:
        config = acm.Sheet.Column().ConfigurationFromScenario(
                            scenario,
                            config)
        
        # As long as we store a reference to the column creator, 
        # it must be configured with scenario information
        columnCreator = columnCreator.ApplyScenario(scenario)
        
        sheet_def = acm.Sheet.GetSheetDefinition(acm.FPortfolioSheet)
        gridBuilder = sheet_def.CreateGridBuilder(False)
        gridBuilder.RegisterScenarios([scenario])
        columnCreators = gridBuilder.ColumnCreators()
        columnCreators.Add(columnCreator)
    
    if parameters is not None:
        config = acm.Sheet.Column().ConfigurationFromColumnParameterDefinitionNamesAndValues(
                            parameters,
                            config)
    
    assert( not (timebuckets and vector) )
    
    if timebuckets is not None:
        config = acm.Sheet.Column().ConfigurationFromTimeBuckets(
                            timebuckets,
                            config)
    
        # As long as we store a reference to the column creator, 
        # it must be configured with time bucket information
        columnCreatorConf = acm.Sheet.Column().CreatorConfigurationFromTimeBuckets(
            timebuckets,
            columnCreator.Configuration())            
        columnCreator = columnCreator.Template().CreateCreator(columnCreatorConf)
        
        sheet_def = acm.Sheet.GetSheetDefinition(acm.FPortfolioSheet)
        gridBuilder = sheet_def.CreateGridBuilder(False)
        columnCreators = gridBuilder.ColumnCreators()
        columnCreators.Add(columnCreator)
    
    if vector is not None:
        
        liveColumnDefinition = columnCreator.Template().LiveColumnDefinition()
        dimensionDefinitions = liveColumnDefinition.DimensionDefinitions()
        dimensionId = dimensionDefinitions[0].Name() if len(dimensionDefinitions) > 0 else None
        
        if dimensionId:
            config = acm.Sheet.Column().ConfigurationFromVector( dimensionId, vector, config )
        else:
            config = acm.Sheet.Column().ConfigurationFromVector( vector, config )
        
        # As long as we store a reference to the column creator, 
        # it must be configured with vector information
        columnCreatorConf = acm.Sheet.Column().CreatorConfigurationFromVector(
            vector,
            columnCreator.Configuration())            
        columnCreator = columnCreator.Template().CreateCreator(columnCreatorConf)
        
        sheet_def = acm.Sheet.GetSheetDefinition(acm.FPortfolioSheet)
        gridBuilder = sheet_def.CreateGridBuilder(False)
        columnCreators = gridBuilder.ColumnCreators()
        columnCreators.Add(columnCreator)
        
    newCalcSpec = acm.Sheet.Column().CreateCalculationSpecification(config,
                                                                    calcSpec.ColumnName(),
                                                                    calcSpec.ContextName())
    columnID = str(columnCreator.OriginalColumnId() if columnCreator.OriginalColumnId() is not None else name)
    return ColumnConfiguration(name,
                               columnID,
                               newCalcSpec,
                               scenarioDimensionNames,
                               columnCreator)
    
def createColumnConfiguration(columnID,
                              extensionContext,
                              customName=None,
                              scenario=None,
                              timebuckets=None,
                              vector=None,
                              parameters=None,
                              scenarioDimensionNames=None,
                              vectorConfiguration=None):
                                                                                           
    name = customName if customName is not None else columnID
    columnCreator = acm.Sheet.Column().GetCreatorTemplate(columnID, extensionContext).CreateCreator()
    
    return _createColumnConfiguration(name, columnCreator, scenario, parameters, timebuckets, vector, scenarioDimensionNames, vectorConfiguration)
    

def createColumnConfigurationFromMeasureSpecification(measureSpecification,
                                                      extensionContext):
    columnId = measureSpecification.ColumnId()
    columnCreator = acm.Sheet.Column().GetCreatorTemplate(columnId, extensionContext).CreateCreator()
    scenarioDimensionNames = None
    calcConfig = measureSpecification.ConfigurationExceptScenarios()
    if measureSpecification.Scenarios() and len( measureSpecification.Scenarios() ) > 0:
        sheet_def = acm.Sheet.GetSheetDefinition(acm.FPortfolioSheet)
        gridBuilder = sheet_def.CreateGridBuilder(False)
        gridBuilder.RegisterScenarios(measureSpecification.Scenarios())
        scenario = gridBuilder.ScenarioManager().FromListOfScenario( measureSpecification.Scenarios() )
        calcConfig = acm.Sheet().Column().ConfigurationFromScenario( scenario, calcConfig )
    calcSpec = acm.Sheet().Column().CreateCalculationSpecification( calcConfig, columnId, extensionContext.Name() )
    
    return ColumnConfiguration(measureSpecification.Name(),
                               columnId,
                               calcSpec,
                               scenarioDimensionNames,
                               columnCreator)
    
def createColumnConfigurationFromStoredColumnCreator(storedColumnCreator,
                                                     customName=None,
                                                     scenarioDimensionNames=None):
    
    name = customName if customName is not None else storedColumnCreator.Name()
    actualParameters = {}
    columnCreator = storedColumnCreator.ColumnCreator()
    
    #Steps required to get the scenario and time bucket parts set up correcly
    sheet_def = acm.Sheet.GetSheetDefinition(acm.FPortfolioSheet)
    gridBuilder = sheet_def.CreateGridBuilder(False)
    candidateScenarios = acm.FStoredScenario.Instances()
    gridBuilder.RegisterScenarios(candidateScenarios)
    columnCreators = gridBuilder.ColumnCreators()
    columnCreators.Add(columnCreator)

    scenario = None #Already correctly set up for the column creator
    timebuckets = None #Already correctly set up for the column creator
    vector = None #Already correctly set up for the column creator

    return _createColumnConfiguration(name, columnCreator, scenario, actualParameters, timebuckets, vector, scenarioDimensionNames, None)

    
def main(portfolioNames,
         tradeFilterNames,
         storedASQLQueryNames,
         columnConfigurations,
         chainedGrouperDefinition, 
         writers,
         distributedMode=False,
         calcEnvironment=None,
         testMode = False,
         logger = None):
    
    runDef = run_def.createRunDefinition(portfolioNames = portfolioNames,
                                         tradeFilterNames = tradeFilterNames,
                                         storedASQLQueryNames = storedASQLQueryNames,
                                         chainedGrouperDefinition = chainedGrouperDefinition,
                                         columnConfigurations = columnConfigurations,
                                         distributedMode = distributedMode,
                                         calculationEnvironment = calcEnvironment,
                                         logger = logger)
               
    publisher = pub.Publisher(contentProvider = calc.Calculator(runDef),
                              writers = writers,
                              logger = logger,
                              testMode = testMode)
    publisher.publish()
    
