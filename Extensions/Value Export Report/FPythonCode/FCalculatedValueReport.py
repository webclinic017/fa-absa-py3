
import acm
import FExportCalculatedValuesMain
import FCalculatedValueXMLWriter

import FReportAPI
import FReportUtils
import FRunScriptGUI
import FOutputSettingsTab
import FAdvancedSettingsTab

class CalculatedValueReport( FRunScriptGUI.AelVariablesHandler ):
    
    def __init__(self):

        ttPositionSpec = (
            'Used to define the positions and specifies which trade attributes '
            'to report.'
        )
        ttPortfolios = 'The physical portfolios to which the trades belong.'
        ttTradeFilters = 'The selection of trade filters.'
        ttTradeQueries = (
            'The stored ASQL queries, queries shown are shared and of type trade.'
        )

        tradeQueries = acm.FStoredASQLQuery.Select('user=0 and subType="FTrade"')
        columnCreators = acm.FStoredColumnCreator.Select('')

        vars = [
                #[VariableName,
                #    DisplayName,
                #    Type, CandidateValues, Default,
                #    Mandatory, Multiple, Description, InputHook, Enabled]

                ['Position Specification',
                    'Position specification',
                    acm.FPositionSpecification, None, None,
                    0, 0, ttPositionSpec],
                ['Portfolios',
                    'Portfolios',
                    acm.FPhysicalPortfolio, None, None,
                    0, 1, ttPortfolios],
                ['Trade Filters',
                    'Trade filters',
                    acm.FTradeSelection, None, None,
                    0, 1, ttTradeFilters],
                ['Trade Queries',
                    'Trade queries',
                    acm.FStoredASQLQuery, tradeQueries, None,
                    0, 1, ttTradeQueries],
                ['Stored Column Creators',
                    'Column Creators',
                    acm.FStoredColumnCreator, columnCreators, None,
                    0, 1, "Column Creators"],
                    
                ['Stored Calc Columns',
                    'Calculation Columns',
                    acm.FStoredCalcColumnSpecificationCollection, None, None,
                    0, 1, 'Calculation Columns']
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars)
        self.extend(FOutputSettingsTab.getAelVariables())
        advancedSettings = FAdvancedSettingsTab.getAelVariables()
        for var in advancedSettings:
            if var[0] in ['Include Raw Data', 'Include Full Data', 'Include Default Data', 'Include Formatted Data']:
                # Might need to add some entries to be able to set the 9:th.
                while len(var) < FRunScriptGUI.Controls.ENABLED + 1:
                    var.append(None)            
            
                # only data of one type is written
                if var[FRunScriptGUI.Controls.NAME] == 'Include Raw Data':
                    var[FRunScriptGUI.Controls.DEFAULT] = 'True'
                else:
                    var[FRunScriptGUI.Controls.DEFAULT] = 'False'
                
                # disable data type checkboxes
                var[FRunScriptGUI.Controls.ENABLED] = 0
        
        self.extend(advancedSettings)



ael_gui_parameters = {'windowCaption':'FCalculatedValueReport'}
ael_variables=CalculatedValueReport()

def create_column_configurations( storedColumnCreators, storedCalcColumnsCollection ):
    calcConfigs = []
    uniqueIds = acm.FIdentitySet()
    
    for storedColumnCreator in storedColumnCreators:
        calcConfigs.append( FExportCalculatedValuesMain.createColumnConfigurationFromStoredColumnCreator( storedColumnCreator ) )
    for storedCalcColumns in storedCalcColumnsCollection:
        calcColumns = storedCalcColumns.CalculationColumnSpecificationCollection()
        measureSpecs = calcColumns.CalculationColumnSpecifications(uniqueIds)
        for measureSpec in measureSpecs:
            calcConfigs.append( 
                FExportCalculatedValuesMain.createColumnConfigurationFromMeasureSpecification(
                    measureSpec,
                    acm.ExtensionTools().GetDefaultContext()
                )
            )
        
    return calcConfigs
    
def create_grouper(positionSpecification):
    groupingAttributes = []
    if positionSpecification:
        for attributeDefinition in positionSpecification.AttributeDefinitions():
            methodChain = attributeDefinition.Definition()
            displayName = acm.Sheet.Column().MethodDisplayName(
                acm.FTrade, methodChain, "Standard"
            )
            groupingAttributes.append([displayName, methodChain, True])
    grouper = acm.Risk().CreateChainedGrouperDefinition(acm.FTrade, 'Portfolio', True, 'Instrument', True, groupingAttributes)
    return grouper
    
def perform_report( params ):

    grouper = create_grouper( params['Position Specification'] )
    writer = FCalculatedValueXMLWriter.CalculatedValueXMLWriter("TEST_REPORT")
    columns = create_column_configurations( params['Stored Column Creators'], params['Stored Calc Columns'] )
    distributedMode = False
    calcEnvName = None
    
    
    portfolioNames = []
    if params['Portfolios']:
        portfolioNames.extend( [p.Name() for p in params['Portfolios'] ])
    
    tradeFilterNames = []
    if params['Trade Filters']:
        tradeFilterNames.extend( [tf.Name() for tf in params['Trade Filters'] ])

    tradeQueryNames = []
    if params['Trade Queries']:
        tradeQueryNames.extend( [tq.Name() for tq in params['Trade Queries'] ])
        
    FExportCalculatedValuesMain.main( portfolioNames, tradeFilterNames, tradeQueryNames, columns, grouper, [writer], distributedMode, calcEnvName)


    xmltext = writer.XmlText()

    report = FReportAPI.FWorksheetReportApiParameters()

    report.snapshot = True
    FReportAPI.init_from_output_settings_tab(report, params)
    FReportAPI.init_from_advanced_settings_tab(report, params)
    report.CreateReportByXml(xmltext)
    

def ael_main( params ):
    params=FReportUtils.adjust_parameters(params)
    
    perform_report( params )
    
