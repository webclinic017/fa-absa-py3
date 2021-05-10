""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesSetup.py"
import FRunScriptGUI
import acm

from FOperationsLoggers import CreateLogger

from FOperationsViewerExamplesCustodyInventoryDataDisp import CreateCustodyInventoryDataDisposition
from FOperationsViewerExamplesCustodyInventoryViewDisp import CreateCustodyInventoryViewDisposition
from FOperationsViewerExamplesCustodyInventoryTemplate import CreateCustodyInventoryTemplate

from FOperationsViewerExamplesSettledInventoryDataDisp import CreateSettledInventoryDataDisposition
from FOperationsViewerExamplesSettledInventoryViewDisp import CreateSettledInventoryViewDisposition
from FOperationsViewerExamplesSettledInventoryTemplate import CreateSettledInventoryTemplate

from FOperationsViewerExamplesPlannedVsActualDataDisp import CreatePlannedVsActualDataDisposition
from FOperationsViewerExamplesPlannedVsActualViewDisp import CreatePlannedVsActualViewDisposition
from FOperationsViewerExamplesPlannedVsActualTemplate import CreatePlannedVsActualTemplate

from FOperationsViewerExamplesCashBalancesDataDisp import CreateCashBalancesDataDisposition
from FOperationsViewerExamplesCashBalancesViewDisp import CreateCashBalancesViewDisposition
from FOperationsViewerExamplesCashBalancesTemplate import CreateCashBalancesAllCCYTemplate, CreateCashBalancesMajorCCYTemplate, CreateCashBalancesMinorCCYTemplate

class FOperationsViewerExamplesSetupGUI(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):
        variables = self.__CreateAelVariables()
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)

    #-------------------------------------------------------------------------
    def __CreateAelVariables(self):
        ttGenerateCashBalancesSetup = "Generate Cash Balances setup"
        ttCashBalancesName = "Name for Cash Balances Data Disposition"
        ttGenerateCustodyInventorySetup = "Generate Custody Inventory setup"
        ttCustodyInventoryName = "Name for Custody Inventory Data Disposition"
        ttGenerateSettledInventorySetup = "Generate Settled Inventory setup"
        ttSettledInventoryName = "Name for Settled Inventory Data Disposition"
        ttGeneratePlannedVsActualSetup = "Generate Planned Vs Actual setup"
        ttPlannedVsActualName = "Name for Planned Vs Actual Data Disposition"
        
        return [('generateCashBalances', 'Cash Balances', 'bool', [False, True], True, True, False, ttGenerateCashBalancesSetup, self.__OnGenerateCashBalances),
                ('cashBalancesName', 'Cash Balances Name', 'string', None, "Cash Balances", True, False, ttCashBalancesName),
                ('generateCustodyInventoryTemplate', 'Custody Inventory', 'bool', [False, True], True, True, False, ttGenerateCustodyInventorySetup, self.__OnGenerateCustodyInventoryTemplate),
                ('custodyInventoryName', 'Custody Inventory Name', 'string', None, "Custody Inventory", True, False, ttCustodyInventoryName),
                ('generateSettledInventoryTemplate', 'Settled Inventory', 'bool', [False, True], True, True, False, ttGenerateSettledInventorySetup, self.__OnGenerateSettledInventoryTemplate),
                ('settledInventoryName', 'Settled Inventory Name', 'string', None, "Settled Inventory", True, False, ttSettledInventoryName),
                ('generatePlannedVsActualTemplate', 'Planned Vs Actual', 'bool', [False, True], True, True, False, ttGeneratePlannedVsActualSetup, self.__OnGeneratePlannedVsActualTemplate),
                ('plannedVsActualName', 'Planned Vs Actual Name', 'string', None, "Planned Vs Actual", True, False, ttPlannedVsActualName)]

    #-------------------------------------------------------------------------
    def __OnGenerateCustodyInventoryTemplate(self, index, fieldValues):
        generateCustodyInventoryTemplate = fieldValues[index]

        if generateCustodyInventoryTemplate == "true":
            self.custodyInventoryName.enable(True)
        else:
            self.custodyInventoryName.enable(False)
        return fieldValues

    #-------------------------------------------------------------------------
    def __OnGenerateSettledInventoryTemplate(self, index, fieldValues):
        generateSettledInventoryTemplate = fieldValues[index]

        if generateSettledInventoryTemplate == "true":
            self.settledInventoryName.enable(True)
        else:
            self.settledInventoryName.enable(False)
        return fieldValues

    #-------------------------------------------------------------------------
    def __OnGeneratePlannedVsActualTemplate(self, index, fieldValues):
        generatePlannedVsActualTemplate = fieldValues[index]

        if generatePlannedVsActualTemplate == "true":
            self.plannedVsActualName.enable(True)
        else:
            self.plannedVsActualName.enable(False)
        return fieldValues

    #-------------------------------------------------------------------------
    def __OnGenerateCashBalances(self, index, fieldValues):
        generateCashBalances = fieldValues[index]

        if generateCashBalances == "true":
            self.cashBalancesName.enable(True)
        else:
            self.cashBalancesName.enable(False)
        return fieldValues

#-------------------------------------------------------------------------
def GenerateCashBalancesSetupAndTemplates(cashBalancesDataDispName, logger):
    logger.LP_Log("Generating Cash Balances setup...")
    logger.LP_Flush()

    generationSuccessful = True
    acm.BeginTransaction()
    try:

        cashBalancesViewDispName = cashBalancesDataDispName + " View"
        CreateCashBalancesDataDisposition(cashBalancesDataDispName)
        logger.LP_Log("Created data dispostiton with name: " + cashBalancesDataDispName)
        logger.LP_Flush()

        CreateCashBalancesViewDisposition(cashBalancesViewDispName, cashBalancesDataDispName)
        logger.LP_Log("Created view dispostiton with name: " + cashBalancesViewDispName)
        logger.LP_Flush()

        cashBalancesAllCCYTemplateName = cashBalancesDataDispName + " Template - All CCY"
        CreateCashBalancesAllCCYTemplate(cashBalancesAllCCYTemplateName, cashBalancesViewDispName, cashBalancesDataDispName)

        logger.LP_Log("Created template with name: " + cashBalancesAllCCYTemplateName )
        logger.LP_Flush()

        cashBalancesMajorCCYTemplateName = cashBalancesDataDispName + " Template - Major CCY"
        CreateCashBalancesMajorCCYTemplate(cashBalancesMajorCCYTemplateName, cashBalancesViewDispName, cashBalancesDataDispName)

        logger.LP_Log("Created template with name: " + cashBalancesMajorCCYTemplateName)
        logger.LP_Flush()

        cashBalancesMinorCCYTemplateName = cashBalancesDataDispName + " Template - Minor CCY"
        CreateCashBalancesMinorCCYTemplate(cashBalancesMinorCCYTemplateName, cashBalancesViewDispName, cashBalancesDataDispName)

        logger.LP_Log("Created template with name: " + cashBalancesMinorCCYTemplateName)
        logger.LP_Flush()

        acm.CommitTransaction()
    except Exception as error:
        acm.AbortTransaction()
        generationSuccessful = False
        logger.LP_Log("Failed to generate setup for Cash Balances reverting changes")
        logger.LP_Log("Generating setup failed, following error was given: \n {} \n".format(error))
        logger.LP_Flush()

    if generationSuccessful:
        logger.LP_Log("Finished generating Cash Balances setup \n")
        logger.LP_Flush()

#-------------------------------------------------------------------------
def GenerateCustodyInventorySetupAndTemplate(custodyInventoryDataDispName, logger):
    logger.LP_Log("Generating Custody Inventory setup...")
    logger.LP_Flush()
    generationSuccessful = True
    acm.BeginTransaction()
    try:
        CreateCustodyInventoryDataDisposition(custodyInventoryDataDispName)
        logger.LP_Log("Created data dispostiton with name: " + custodyInventoryDataDispName)
        logger.LP_Flush()

        custodyInventoryViewDispName = custodyInventoryDataDispName + " View"
        CreateCustodyInventoryViewDisposition(custodyInventoryViewDispName, custodyInventoryDataDispName)
        logger.LP_Log("Created view dispostiton with name: " + custodyInventoryViewDispName)
        logger.LP_Flush()

        custodyInventoryTemplateName = custodyInventoryDataDispName + " Template"
        CreateCustodyInventoryTemplate(custodyInventoryTemplateName, custodyInventoryViewDispName, custodyInventoryDataDispName)
        logger.LP_Log("Created template with name: " + custodyInventoryTemplateName)
        logger.LP_Flush()

        acm.CommitTransaction()
    except Exception as error:
        acm.AbortTransaction()
        generationSuccessful = False
        logger.LP_Log("Failed to generate setup for Custody Inventory reverting changes")
        logger.LP_Log("Generating setup failed, following error was given: \n {} \n".format(error))
        logger.LP_Flush()

    if generationSuccessful:
        logger.LP_Log("Finished generating Custody Inventory setup \n")
        logger.LP_Flush()

#-------------------------------------------------------------------------
def GenerateSettledInventorySetupAndTemplate(settledInventoryDataDispName, logger):
    logger.LP_Log("Generating Settled Inventory setup... \n")
    logger.LP_Flush()

    generationSuccessful = True
    acm.BeginTransaction()
    try:
        CreateSettledInventoryDataDisposition(settledInventoryDataDispName)
        logger.LP_Log("Created data dispostiton with name: " + settledInventoryDataDispName)
        logger.LP_Flush()

        settledInventoryViewDispName = settledInventoryDataDispName + " View"
        CreateSettledInventoryViewDisposition(settledInventoryViewDispName, settledInventoryDataDispName)
        logger.LP_Log("Created view dispostiton with name: " + settledInventoryViewDispName)
        logger.LP_Flush()

        settledInventoryTemplateName = settledInventoryDataDispName + " Template"
        CreateSettledInventoryTemplate(settledInventoryTemplateName, settledInventoryViewDispName, settledInventoryDataDispName)
        logger.LP_Log("Created template with name: " + settledInventoryTemplateName)
        logger.LP_Flush()

        acm.CommitTransaction()
    except Exception as error:
        acm.AbortTransaction()
        generationSuccessful = False
        logger.LP_Log("Failed to generate setup for Settled Inventory reverting changes")
        logger.LP_Log("Generating setup failed, following error was given: \n {} \n".format(error))
        logger.LP_Flush()

    if generationSuccessful:
        logger.LP_Log("Finished generating Settled Inventory setup \n")
        logger.LP_Flush()

#-------------------------------------------------------------------------
def GeneratePlannedVsActualSetupAndTemplate(plannedVsActualDataDispName, logger):
    logger.LP_Log("Generating Planned Vs Actual setup... \n")
    logger.LP_Flush()

    generationSuccessful = True
    acm.BeginTransaction()
    try:
        CreatePlannedVsActualDataDisposition(plannedVsActualDataDispName)
        logger.LP_Log("Created data dispostiton with name: " + plannedVsActualDataDispName)
        logger.LP_Flush()

        plannedVsActualViewDispName = plannedVsActualDataDispName + " View"
        CreatePlannedVsActualViewDisposition(plannedVsActualViewDispName, plannedVsActualDataDispName)
        logger.LP_Log("Created view dispostiton with name: " + plannedVsActualViewDispName)
        logger.LP_Flush()

        plannedVsActualTemplateName = plannedVsActualDataDispName + " Template"
        CreatePlannedVsActualTemplate(plannedVsActualTemplateName, plannedVsActualViewDispName, plannedVsActualDataDispName)
        logger.LP_Log("Created template with name: " + plannedVsActualTemplateName)
        logger.LP_Flush()

        acm.CommitTransaction()
    except Exception as error:
        acm.AbortTransaction()
        generationSuccessful = False
        logger.LP_Log("Failed to generate setup for Planned Vs Actual reverting changes")
        logger.LP_Log("Generating setup failed, following error was given: \n {} \n".format(error))
        logger.LP_Flush()

    if generationSuccessful:
        logger.LP_Log("Finished generating Planned Vs Actual setup \n")
        logger.LP_Flush()

#-------------------------------------------------------------------------
def ael_main(params):
    logger = CreateLogger(True, False, True, "", "")

    generatedAtLeastOneSetup = False

    logger.LP_Log("Started generating setup... \n")
    logger.LP_Flush()

    if params["generateCashBalances"]:
        GenerateCashBalancesSetupAndTemplates(params["cashBalancesName"], logger)
        generatedAtLeastOneSetup = True
    
    if params["generateCustodyInventoryTemplate"]:
        GenerateCustodyInventorySetupAndTemplate(params["custodyInventoryName"], logger)
        generatedAtLeastOneSetup = True

    if params["generateSettledInventoryTemplate"]:
        GenerateSettledInventorySetupAndTemplate(params["settledInventoryName"], logger)
        generatedAtLeastOneSetup = True

    if params["generatePlannedVsActualTemplate"]:
        GeneratePlannedVsActualSetupAndTemplate(params["plannedVsActualName"], logger)
        generatedAtLeastOneSetup = True

    if generatedAtLeastOneSetup:
        logger.LP_Log("Finished generating setup \n")
    else:
        logger.LP_Log("No setup selected please choose an option \n")
    logger.LP_Flush()


ael_gui_parameters = {
    'runButtonLabel' : 'Run',
    'hideExtraControls' : False,
    'windowCaption' : 'FOperations Viewer Examples Setup',
    'version' : '%R%'
    }

ael_variables = FOperationsViewerExamplesSetupGUI()