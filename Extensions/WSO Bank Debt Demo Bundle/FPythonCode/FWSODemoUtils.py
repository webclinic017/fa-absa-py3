""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSODemoBundle/etc/FWSODemoUtils.py"
"""--------------------------------------------------------------------------
MODULE
    FWSODemoUtils

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Contains WSO demo bundle utility functions.

-----------------------------------------------------------------------------"""
import acm
from FSheetUtils import SheetContents, CreateSheetSetup, ColumnCreators
import FParameterSettings

from FWSOUploadDialog import WSOUploadDialog
from FWSOCustomMappingsTrade import FA_Acquirer, FA_Portfolio, FA_Counterparty, FA_Trader

import FAssetManagementUtils
logger = FAssetManagementUtils.GetLogger()

PRTFSHEET_DEFAULT_COLUMNS = ['Portfolio Position', 'Portfolio Present Value', 'Portfolio Delta Yield', 
                             'Price Theor', 'Instrument Currency', 'Portfolio Currency',]


def ParamsDict(uploadSpecName):
    try:
        from FWSODemoHooks import ParamsDictFromHook
        logger.info('WSO Demo Bundle log: WSO Demo Bundle log: Using hook generated input parameter dictionary for the WSO uploads.')
        paramsDict = ParamsDictFromHook(uploadSpecName)
    except ImportError:
        logger.info('WSO Demo Bundle log: Using default input parameter dictionary for the WSO uploads.')
        paramsDict = GetDefaultParamsDict(uploadSpecName)
    except AttributeError:
        logger.info('WSO Demo Bundle log: Using default input parameter dictionary for the WSO uploads.')
        paramsDict = GetDefaultParamsDict(uploadSpecName)
    except Exception:
        logger.info('WSO Demo Bundle log: Using default input parameter dictionary for the WSO uploads.')
        paramsDict = GetDefaultParamsDict(uploadSpecName)
    return paramsDict

def GetDefaultParamsDict(uploadSpecName):
    paramsDict = dict()    
    ael_variables = WSOUploadDialog(uploadSpecName)
    for i in range(len(ael_variables)):
        itemKey = ael_variables[i][0]
        if itemKey == 'ReconciliationSpecification':
            itemValue = uploadSpecName
        elif itemKey == 'DisplayOption':
            itemValue = "1"
        elif itemKey == 'CustomStartDate':
            itemValue = ''
        elif itemKey == 'CustomEndDate':
            itemValue = ''
        elif itemKey == 'StartDate':
            itemValue = 'Inception'
        elif itemKey == 'EndDate':
            itemValue = 'Now'
        elif itemKey == 'ForceReRun':
            itemValue = "1"
        elif itemKey == 'LogLevel':
            itemValue = '1. Normal'
        else:
            logger.error('WSO Demo Bundle log: Ael variable key %s could not be identified.' % itemKey)
            continue
        paramsDict[itemKey] = itemValue             
    return paramsDict
    
    
def ValidateAndCreateMappingObjects():

    def ValidateOutput(customMappingTypesAndOutputs, supportedMappingType, mappedFunction):
        errString = 'WSO Demo Bundle log: The custom mapping function %s has been overriden \
                is forbidden when running the demo bundle. Please check your module hierarchy \
                in the Extension Manager'    
                
        actualOutput = mappedFunction({})
        expectedOutput = customMappingTypesAndOutputs.get(supportedMappingType)
        if actualOutput != expectedOutput:
            raise ValueError(errString % str(mappedFunction))
        return expectedOutput
        
    def CommitObject(obj):
        try:
            obj.Commit()
        except RuntimeError:
            pass            
                
    customMappingTypesAndOutputs = {'Portfolio': 'Wall Street Structure Arbitrage SP USD', 
                                    'Acquirer': 'Demo_Acquirer', 
                                    'Trader': acm.UserName(), 
                                    'Counterparty': 'Demo_Counterparty',}
    
    for supportedMappingType in list(customMappingTypesAndOutputs.keys()):   
        if supportedMappingType == 'Portfolio':
            expectedOutput = ValidateOutput(customMappingTypesAndOutputs, supportedMappingType, FA_Portfolio)                        
            portfolio = acm.FPhysicalPortfolio[expectedOutput]
            if portfolio:
                continue
            portfolio = acm.FPhysicalPortfolio()
            portfolio.Name(expectedOutput)
            portfolio.AssignInfo('WSO Bank Debt Demo Bundle Portfolio' + '_' + str(acm.Time.TimeNow()))
            portfolio.Currency('USD')
            CommitObject(portfolio)      
        elif supportedMappingType == 'Acquirer':
            expectedOutput = ValidateOutput(customMappingTypesAndOutputs, supportedMappingType, FA_Acquirer)  
            acquirer = acm.FInternalDepartment[expectedOutput]            
            if acquirer:
                continue                                
            acquirer = acm.FInternalDepartment()
            acquirer.Name(expectedOutput)    
            CommitObject(acquirer)      
        elif supportedMappingType == 'Trader':
            expectedOutput = ValidateOutput(customMappingTypesAndOutputs, supportedMappingType, FA_Trader)  
            continue       
        elif supportedMappingType == 'Counterparty':
            expectedOutput = ValidateOutput(customMappingTypesAndOutputs, supportedMappingType, FA_Counterparty)  
            counterparty = acm.FCounterParty[expectedOutput]                        
            if counterparty:
                continue
            counterparty = acm.FCounterParty()
            counterparty.Name(expectedOutput)    
            CommitObject(counterparty)            
        else:
            raise ValueError('The mapping object of type %s is not supported.' % supportedMappingType)
    
def LaunchTradingManagerWithContents(portfolioSheetDefaultSettingsName = 'WSOBankDebtDemoPortfolioSheet',
                                     cashSheetDefCols = 'wsoDemoCashAnalysisSheetDefaultColumns',
                                     cashAnalysisSheetCaption = 'WSO Bank Debt Demo Cash Analysis'):
                                     
    settings = FParameterSettings.ParameterSettingsCreator.FromRootParameter(portfolioSheetDefaultSettingsName)
    contents = SheetContents(settings)
    app = acm.StartApplication('Trading Manager', contents.ForApplication())
    portfolioSheet = app.ActiveWorkbook().ActiveSheet()
    
    portfolio = acm.FPhysicalPortfolio[FA_Portfolio({})]    
    app.ActiveSheet().InsertObject(portfolio, 'IOAP_REPLACE')
    
    columnCreators = ColumnCreators(PRTFSHEET_DEFAULT_COLUMNS, acm.GetDefaultContext())        
    for index in range(columnCreators.Size()-1):
        app.ActiveSheet().ColumnCreators().Add(columnCreators.At(index))
        
    cashSheetSetup = CreateSheetSetup('FMoneyFlowSheet')
    cashSheetSetup.SheetTitle(cashAnalysisSheetCaption)
    workBook = app.ActiveWorkbook()
    cashSheet = workBook.NewSheet('MoneyFlowSheet', cashSheetDefCols, cashSheetSetup)

    instruments = portfolio.Instruments()
    for instrument in instruments:
        cashSheet.InsertObject(instrument, 'IOAP_LAST')    
        
    workBook.ActivateSheet(portfolioSheet)        