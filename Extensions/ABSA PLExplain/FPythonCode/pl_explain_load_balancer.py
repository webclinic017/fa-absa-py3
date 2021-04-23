"""---------------------------------------------------------------------------------------------
MODULE
    pl_explain_load_balancer - 

    Gino Bellato, FIS

DESCRIPTION

    This script will look up applicable physical portfolios and analyse their trade contents
    based on instrument/product type to assign tasks & query folders

---------------------------------------------------------------------------------------------"""

import acm, ael
import time
import datetime
import os.path
import csv
import operator

context = acm.GetDefaultContext()
contextDefinition = 'FC Accrual Books'
sens_master_Qf = acm.FStoredASQLQuery['PLE_Master_Sensitivities']
sens_master_Qf_not = acm.FStoredASQLQuery['PLE_Master_Sensitivities_NotInsType']
sysPL_master_Qf = acm.FStoredASQLQuery['PLE_Master_SystemPL']
sysPL_master_Qf_not = acm.FStoredASQLQuery['PLE_Master_SystemPL_NotInsType']
sysPL_master_Qf_ShortMaturity = acm.FStoredASQLQuery['PLE_Master_SystemPL_ShortMaturity']
sysPL_master_Qf_MediumMaturity = acm.FStoredASQLQuery['PLE_Master_SystemPL_MediumMaturity']
sysPL_master_Qf_LongMaturity = acm.FStoredASQLQuery['PLE_Master_SystemPL_LongMaturity']
sysPL_master_Qf_Theta = acm.FStoredASQLQuery['PLE_Master_ThetaPL']
sysPL_master_Qf_Theta_SOB = acm.FStoredASQLQuery['PLE_Master_ThetaPL_SOB']
sysPL_master_Qf_Theta_not = acm.FStoredASQLQuery['PLE_Master_ThetaPL_NotInsType']
sysPL_master_Qf_Theta_ShortMaturity = acm.FStoredASQLQuery['PLE_Master_ThetaPL_ShortMaturity']
sysPL_master_Qf_Theta_MediumMaturity = acm.FStoredASQLQuery['PLE_Master_ThetaPL_MediumMaturity']
sysPL_master_Qf_Theta_LongMaturity = acm.FStoredASQLQuery['PLE_Master_ThetaPL_LongMaturity']


posSpecDefault = 'PLE Cpty/Curr/Port/InsType/TradeOid'
module = 'FArtiQMarketRiskExport'
default_outputDirectory = "/services/frontnt/Task/PNL"


riskfactorAbbreviations = { "InterestRate": "IntRate",
                            "Inflation": "Inflation",
                            "InstrumentSpread": "InsSpread",
                            "Benchmark": "Bench",
                            "CommodityPrice": "CmdtyPrice", 
                            "Credit": "Credit", 
                            "FXRate": "FXRate",
                            "Theta": "Theta",
                            "EquityPrice": "EQPrice",
                            "Dividend": "EQDivs",
                            "Volatility": "Vola",
                            "HistoricalVariance": "HistVar",
                            }
                            
taskNameSuffixConvention = { "InterestRate": "_T0_SERVER",
                             "Inflation": "_T0_SERVER",
                             "InstrumentSpread": "_T0_SERVER",
                             "Benchmark": "_T0_SERVER",
                             "CommodityPrice": "_T0_SERVER", 
                             "Credit": "_T0_SERVER", 
                             "FXRate": "_T0_SERVER",
                             "Theta": "_T1_SERVER",
                             "Theta_PSwap_SOB": "_T0_SERVER",
                             "Theta_PSwap_COB": "_T1_SERVER",
                             "EquityPrice": "_T0_SERVER",
                             "Dividend": "_T0_SERVER",
                             "Volatility": "_T0_SERVER",
                             "HistoricalVariance": "_T1_SERVER",
                            }
                            
calcTypeOutputFolderMappings = {"Theta": "Theta",
                                "HistoricalVariance": "HistoricalVariance",
                                "Theta_PSwap_SOB": "Theta",
                                "Theta_PSwap_COB": "Theta",
                                  }
                                        
riskfactorDataTypeMap = {"Benchmark RF Run Times": 4,
                         "Benchmark Delta Sensitivity": 5, 
                         "Interest Rate RF Run Times": 6, 
                         "Interest Rate Yield Delta Sensitivity": 7,
                         "Inflation RF Run Times": 8,
                         "Inflation Delta Sensitivity": 9,
                         "Instrument Spread RF Run Times": 10,
                         "Instrument Spread Delta Sensitivity": 11,
                         "Theta RF Run Times": 12,
                         "Theta Sensitivity": 13,
                         "FX RF Run Times": 14,
                         "FX Delta Sensitivity": 15,
                        }

fileNameConventions = {"MajorDesk": "_MAD_",
                       "MinorDesk": "_MND_",
                       "Masterbook": "_MB_",
                       "Portfolio": "_P_",
                      }
heavyCalcInsTypes = ['Swap', 'CurrSwap', 'IndexLinkedSwap', 'Bond', 'IndexLinkedBond', 'CreditDefaultSwap', 'VarianceSwap', 'Portfolio Swap', 'TotalReturnSwap', 'BuySellback']


def _nowTime():
    """
    Returns a sting with current time in the format HH:MM:SS, for example:
    10:12:43
    """
    return time.strftime('%H:%M:%S', time.localtime(time.time()))
    
def _convertTimeInSecondsToHoursMinutesSeconds(timeInSeconds):
    timeInSeconds = int(timeInSeconds)
    mins = timeInSeconds // 60
    hrs = mins // 60
    return '{0:02d}:{1:02d}:{2:02d}'.format(hrs, mins % 60, timeInSeconds % 60)

   
def getValidPorfoliosList(RunAtLevel, level):
    valid_ports = []
    portfolios  = acm.FPhysicalPortfolio.Select('')
    
    for portfolio in portfolios:
        if portfolio.AdditionalInfo().PL_Explain_Eligible() == True:
            if RunAtLevel == 'MajorDesk':
                if portfolio.AdditionalInfo().MajorDesk() == level:
                    valid_ports.append(portfolio.Name())
            elif RunAtLevel == 'MinorDesk':
                if portfolio.AdditionalInfo().MinorDesk() == level:
                    valid_ports.append(portfolio.Name())
            elif RunAtLevel == 'Masterbook':
                if portfolio.AdditionalInfo().Masterbook() == level:
                    valid_ports.append(portfolio.Name())
    return valid_ports
    
def getPLeligiblePorfolioList():
    valid_ports = []
    portfolios  = acm.FPhysicalPortfolio.Select('')
    
    for portfolio in portfolios:
        if portfolio.AdditionalInfo().PL_Explain_Eligible() == True:
            valid_ports.append(portfolio.Name())
            
    return valid_ports

    
def getMasterBooks():
    masterBooks = []
    portfolios  = acm.FPhysicalPortfolio.Select('')
    
    for portfolio in portfolios:
        if portfolio.AdditionalInfo().PL_Explain_Eligible() == True:
            if portfolio.AdditionalInfo().Masterbook():
                masterBooks.append(portfolio.AdditionalInfo().Masterbook())
            
    return list(set(masterBooks))
    
def getMinorDesk():
    minorDesks = []
    portfolios  = acm.FPhysicalPortfolio.Select('')
    
    for portfolio in portfolios:
        if portfolio.AdditionalInfo().PL_Explain_Eligible() == True:
            if portfolio.AdditionalInfo().MinorDesk():
                minorDesks.append(portfolio.AdditionalInfo().MinorDesk())
            
    return list(set(minorDesks))
    
def getMajorDesk():
    majorDesks = []
    portfolios  = acm.FPhysicalPortfolio.Select('')
    
    for portfolio in portfolios:
        if portfolio.AdditionalInfo().PL_Explain_Eligible() == True:
            if portfolio.AdditionalInfo().MajorDesk():
                majorDesks.append(portfolio.AdditionalInfo().MajorDesk())
            
    return list(set(majorDesks))
    
def getAccrualPortfoliosFromContextDefn(contextDefinition):
    portList = []
    context = acm.FContext.Select('name = %s' %contextDefinition)
    for setting in context.Element().Elements():
        if setting.MappingType() == 'Portfolio':
            portList.append(setting.Portfolio().Name())
    return portList
    
def getAccrualorMtMPortfolios(allAccrualPortfolios, RunAtLevel, level):
    accrual_portfolios = []
    portfolios  = acm.FPhysicalPortfolio.Select('')
    
    for portfolio in portfolios:
        if portfolio.AdditionalInfo().PL_Explain_Eligible() == True:
            if RunAtLevel == 'MajorDesk':
                if portfolio.AdditionalInfo().MajorDesk() == level:
                    if portfolio.Name() in allAccrualPortfolios:
                        accrual_portfolios.append(portfolio.Name())
            elif RunAtLevel == 'MinorDesk':
                if portfolio.AdditionalInfo().MinorDesk() == level:
                    if portfolio.Name() in allAccrualPortfolios:
                        accrual_portfolios.append(portfolio.Name())
            elif RunAtLevel == 'Masterbook':
                if portfolio.AdditionalInfo().Masterbook() == level:
                    if portfolio.Name() in allAccrualPortfolios:
                        accrual_portfolios.append(portfolio.Name())
    return accrual_portfolios

       
def retrieve_minAndmax_runtimes(dict):
    insTypes = []
    if len(dict) > 2:
        sortedRunTimes = sorted(dict.items(), key = operator.itemgetter(1))   
        minValue = min(dict, key=dict.get)
        maxValue = max(dict, key=dict.get)
        insTypes.append(maxValue)
        insTypes.append(minValue)
        return insTypes
    else:
        for k in dict.keys():
            insTypes.append(k)
        return insTypes

  
def remove_max_and_min(dict, minAndMaxList):
    empty = {}
    if len(dict) > 2:
        for instype in minAndMaxList:
            del dict[instype]
        return dict
    else:
        return empty
        
def compare_lists(list1, list2):
    new_list = []
    for obj in list1:
        if not obj in list2:
            new_list.append(obj)
    return new_list
    
def filterOutPSwaps(list):
    newList = []
    for type in list:
        if type !='Portfolio Swap':
            newList.append(type)
    return newList
    
def check_riskFactor_outputFolder(dict, calc_type):
    if dict.has_key(calc_type):
        return dict[calc_type]
    else:
        return calc_type

def concatenate_file_path(baseFilePath, additionalFolder):
    filePath = baseFilePath + '/' + additionalFolder
    return filePath

"""---------------------------------------------------------------------------------------------"""
""" Create PLE Task """

def createPLETasks(calc_type, qf, posSpec, riskFactor, context, module, task_name, default_outputDirectory, outputFileName, accMethod):
    task_name_local = task_name
    existingTask = acm.FAelTask[task_name]
    additionalFolder = check_riskFactor_outputFolder(calcTypeOutputFolderMappings, calc_type)
    outputFilePath = concatenate_file_path(default_outputDirectory, additionalFolder)
    if existingTask: #check if task exists already, if so delete it
        existingTask.Delete()
        print ("Removed task: %s" %(task_name))
        
    # build new task from scratch
    task = acm.FAelTask()    
    task.ModuleName(module)
    task.ContextName(context)
    task_params = task.Parameters()
    """default settings"""
    task_params.AtPutStrings("batchSize", '200')
    task_params.AtPutStrings("horizon", "1d")
    #Position tab
    task_params.AtPutStrings("positionSpec", posSpec)
    task_params.AtPutStrings("storedASQLQueries", qf)
    #Logging tab
    task_params.AtPutStrings("LogToConsole", "1")
    task_params.AtPutStrings("LogToFile", "0")
    task_params.AtPutStrings("Logmode", "2")
    #Ouput tab
    task_params.AtPutStrings("Output File Date", "False")
    task_params.AtPutStrings("Output File Prefix", "")
    task_params.AtPutStrings("Create directory with date", "True")
    task_params.AtPutStrings("output_dir", outputFilePath)
    task_params.AtPutStrings("Overwrite if file exists", "True")
    if calc_type == 'Sensitivities':
        #Profit & Loss Explain tab
        task_params.AtPutStrings("runPLExplainReport", "1")
        task_params.AtPutStrings("plExplainOutputFile", outputFileName)
        task_params.AtPutStrings("riskFactors", riskFactor)
        #task_params.AtPutStrings("timebucket_name_PLExplain", None)
        task.Name(task_name)
        task.Parameters(task_params)
        task.Commit()
        print ("Committed task: %s" %(task.Name()))  
    elif calc_type == 'Theta':
        task_params.AtPutStrings("runGreekReports", "1")
        task_params.AtPutStrings("greeks_file", qf)
        task_params.AtPutStrings("measures_Greeks", "Theta PL")
        if not accMethod:
            task_params.AtPutStrings("column_name_Greeks", "Portfolio Theta ThTPL PLE") # for MtM portfolio accounting types
        if accMethod:
            task_params.AtPutStrings("column_name_Greeks", "Portfolio Theta ThTPL PLE Accrual") # for Accrual portfolio accounting types
        task.Name(task_name)
        task.Parameters(task_params)
        task.Commit()
        print ("Committed task: %s" %(task.Name())) 
    elif calc_type == 'Theta_PSwap_SOB':
        task_params.AtPutStrings("runGreekReports", "1")
        task_params.AtPutStrings("greeks_file", qf)
        task_params.AtPutStrings("measures_Greeks", "Pswap PL SOB")
        task_params.AtPutStrings("column_name_Greeks", "Portfolio Total Profit and Loss") # special case for Portfolio Swap Instrument types
        task.Name(task_name)
        task.Parameters(task_params)
        task.Commit()
        print ("Committed task: %s" %(task.Name())) 
    elif calc_type == 'Theta_PSwap_COB':
        task_params.AtPutStrings("runGreekReports", "1")
        task_params.AtPutStrings("greeks_file", qf)
        task_params.AtPutStrings("measures_Greeks", "Pswap PL COB")
        task_params.AtPutStrings("column_name_Greeks", "Portfolio Total Profit and Loss") # special case for Portfolio Swap Instrument types
        task.Name(task_name)
        task.Parameters(task_params)
        task.Commit()
        print ("Committed task: %s" %(task.Name()))
    elif calc_type == 'HistoricalVariance':
        task_params.AtPutStrings("runGreekReports", "1")
        task_params.AtPutStrings("greeks_file", qf)
        task_params.AtPutStrings("measures_Greeks", "Historical Variance PL")
        task_params.AtPutStrings("column_name_Greeks", "Historical Variance") # special case for Variance Swap Instrument types
        task.Name(task_name)
        task.Parameters(task_params)
        task.Commit()
        print ("Committed task: %s" %(task.Name())) 

"""---------------------------------------------------------------------------------------------"""
""" Create New Query Folders & Update their filtering criteria """

def createNewQueryFolder(master_Qf, qf_name):
    """create a child query folder based on a saved master query folder"""
    existingQuery = acm.FStoredASQLQuery[qf_name]
    if existingQuery:
        existingQuery.Delete()
    new_qf    = master_Qf.Clone()
    new_qf.Name(qf_name)
    new_qf.AutoUser(False)
    new_qf.Commit()
    print '==> Successfully Created Query Folder: %s.'%(qf_name) 

def queryFolderUpdate(filter_name, new_criteria, _field):
    """update a exsting query folder's node with new criteria"""
    print "entering queryFolderUpdate", filter_name
    filter = acm.FStoredASQLQuery[filter_name]
    if filter:
        query = filter.Query()
        nodes = query.AsqlNodes()
    if not filter:
        print "cannot find query", filter_name
    if _field == 'Portfolio': ins_node = nodes[1]
    if _field == 'InsType': ins_node = nodes[0]
    
    ins_nodes_array = ins_node.AsqlNodes()    
    if ins_node.AsqlNodes()[0].AsqlValue() == None:
        ins_node.AsqlNodes()[0].AsqlValue(new_criteria)
    else:
        new_node = ins_nodes_array[0].Clone()
        new_node.AsqlValue(new_criteria)
        ins_nodes_array.Add(new_node)
    filter.Query(query)
    if _field == 'Portfolio':
        print '==> Successfully Added Portfolio: %s to %s.'%(new_criteria, filter_name)
    if _field == 'InsType':
        print '==> Successfully Added Instrument Type: %s to %s.'%(new_criteria, filter_name)
        
def commitChangesToQueryFolder(filter_name):
    """commit all updates to the query folder"""
    filter = acm.FStoredASQLQuery[filter_name]
    query = filter.Query()
    nodes = query.AsqlNodes()
    nodes.Commit()
    query.Commit()
    filter.Query(query)
    filter.AutoUser(False)
    filter.Commit()
    print '==> Successfully committed changes to query folder: %s.'%(filter_name)

def CreateQueryFoldersAndTasksAtRunLevel(RunAtLevel, level, riskFactor, type_id, data, posSpec, useMaturityBuckets):
    if RunAtLevel != 'Portfolio':
        levelName = level.replace(' ', '')
        levelPortfolioList = getValidPorfoliosList(RunAtLevel, level)
        allAccrualPortfolios = getAccrualPortfoliosFromContextDefn(contextDefinition) #retrieve accrual portfolios from Context Defn : 'FC Accrual Books'
        accrualPortfolios = getAccrualorMtMPortfolios(allAccrualPortfolios, RunAtLevel, level)
        LevelPortfolios = compare_lists(levelPortfolioList, accrualPortfolios) 
    if RunAtLevel == 'Portfolio':
        levelName = level.replace(' ', '')
        levelPortfolioList = [level]
        allAccrualPortfolios = getAccrualPortfoliosFromContextDefn(contextDefinition) #retrieve accrual portfolios from Context Defn : 'FC Accrual Books'
        accrualPortfolios = []
        if level in allAccrualPortfolios:
            accrualPortfolios.append(level)
        LevelPortfolios = compare_lists(levelPortfolioList, accrualPortfolios)  
    heavyCalcIns_QF = "PLE_Sens" + fileNameConventions[RunAtLevel] + levelName + "_" + riskfactorAbbreviations[riskFactor]
    acc_heavyCalcIns_QF = "PLE_Sens" + fileNameConventions[RunAtLevel] + "Acc_" + levelName + "_" + riskfactorAbbreviations[riskFactor]
    newQF_A = "PLE_Sens" + fileNameConventions[RunAtLevel] + levelName + "_" + riskfactorAbbreviations[riskFactor] + "_A"
    taskName_A = newQF_A + taskNameSuffixConvention[riskFactor]
    newQF_B = "PLE_Sens" + fileNameConventions[RunAtLevel] + levelName + "_" + riskfactorAbbreviations[riskFactor] + "_B"
    taskName_B = newQF_B + taskNameSuffixConvention[riskFactor]
    newQF_C = "PLE_Sens" + fileNameConventions[RunAtLevel] + levelName + "_" + riskfactorAbbreviations[riskFactor] + "_C"
    taskName_C = newQF_C + taskNameSuffixConvention[riskFactor]
    newQF_D = "PLE_Sens" + fileNameConventions[RunAtLevel] + levelName + "_" + riskfactorAbbreviations[riskFactor] + "_D"
    taskName_D = newQF_D + taskNameSuffixConvention[riskFactor]
    newQF_E = "PLE_Sens" + fileNameConventions[RunAtLevel] + levelName + "_" + riskfactorAbbreviations[riskFactor] + "_E"
    taskName_E = newQF_E + taskNameSuffixConvention[riskFactor]
    acc_newQF_D = "PLE_Sens" + fileNameConventions[RunAtLevel] + "Acc_" + levelName + "_" + riskfactorAbbreviations[riskFactor] + "_D"
    acc_taskName_D = acc_newQF_D + taskNameSuffixConvention[riskFactor]  
    acc_newQF_E = "PLE_Sens" + fileNameConventions[RunAtLevel] + "Acc_" + levelName + "_" + riskfactorAbbreviations[riskFactor] + "_E"
    acc_taskName_E = acc_newQF_E + taskNameSuffixConvention[riskFactor]
    acc_newQF_F = "PLE_Sens" + fileNameConventions[RunAtLevel] + "Acc_" + levelName + "_" + riskfactorAbbreviations[riskFactor] + "_F"
    acc_taskName_F = acc_newQF_F + taskNameSuffixConvention[riskFactor]
    acc_newQF_G = "PLE_Sens" + fileNameConventions[RunAtLevel] + "Acc_" + levelName + "_" + riskfactorAbbreviations[riskFactor] + "_G"
    acc_taskName_G = acc_newQF_G + taskNameSuffixConvention[riskFactor]
    acc_newQF_H = "PLE_Sens" + fileNameConventions[RunAtLevel] + "Acc_" + levelName + "_" + riskfactorAbbreviations[riskFactor] + "_H"
    acc_taskName_H = acc_newQF_H + taskNameSuffixConvention[riskFactor]
    if riskFactor == 'Theta': # Changed the naming convention for the Theta tasks and Query folders
        heavyCalcIns_QF = "PLE_Theta" + fileNameConventions[RunAtLevel] + levelName    
        acc_heavyCalcIns_QF = "PLE_Theta" + fileNameConventions[RunAtLevel] + "Acc_" + levelName
        newQF_A = "PLE_Theta" + fileNameConventions[RunAtLevel] + levelName + "_A"
        taskName_A = newQF_A + taskNameSuffixConvention[riskFactor]
        newQF_B = "PLE_Theta" + fileNameConventions[RunAtLevel] + levelName + "_B"
        taskName_B = newQF_B + taskNameSuffixConvention[riskFactor]
        newQF_C = "PLE_Theta" + fileNameConventions[RunAtLevel] + levelName + "_C"
        taskName_C = newQF_C + taskNameSuffixConvention[riskFactor]
        newQF_D = "PLE_Theta" + fileNameConventions[RunAtLevel] + levelName + "_D"
        taskName_D = newQF_D + taskNameSuffixConvention[riskFactor]
        newQF_E = "PLE_Theta" + fileNameConventions[RunAtLevel] + levelName + "_E"
        taskName_E = newQF_E + taskNameSuffixConvention[riskFactor]
        acc_newQF_D = "PLE_Theta" + fileNameConventions[RunAtLevel] + "Acc_" + levelName + "_D"
        acc_taskName_D = acc_newQF_D + taskNameSuffixConvention[riskFactor]
        acc_newQF_E = "PLE_Theta" + fileNameConventions[RunAtLevel] + "Acc_" + levelName + "_E"
        acc_taskName_E = acc_newQF_E + taskNameSuffixConvention[riskFactor]
        acc_newQF_F = "PLE_Theta" + fileNameConventions[RunAtLevel] + "Acc_" + levelName + "_F"
        acc_taskName_F = acc_newQF_F + taskNameSuffixConvention[riskFactor]
        acc_newQF_G = "PLE_Theta" + fileNameConventions[RunAtLevel] + "Acc_" + levelName + "_G"
        acc_taskName_G = acc_newQF_G + taskNameSuffixConvention[riskFactor]
        acc_newQF_H = "PLE_Theta" + fileNameConventions[RunAtLevel] + "Acc_" + levelName + "_H"
        acc_taskName_H = acc_newQF_H + taskNameSuffixConvention[riskFactor]
    old_runnings = {'Swap':70, 'Curr':25, 'Stock':1, 'CurrSwap':90, 'Bond':20, 'Bill':8, 'FRA':9, 'Option':10, 
                    'CreditDefaultSwap':60, 'Deposit':2, 'IndexLinkedSwap':80, 'IndexLinkedBond':40}
    runnings = {'Curr':25, 'Stock':1, 'Bill':7, 'FRA':8, 'Option':10, 'Deposit':2, 'Future/Forward':20, 'Warrant':9}
    print "get min and max run times"
    print "runnings before", runnings
    insTypeMinAndMax = retrieve_minAndmax_runtimes(runnings)
    print "insTypeMinAndMax", insTypeMinAndMax
    print "get rid of insTypeMinAndMax"
    if len(insTypeMinAndMax) > 1:
        print "insTypeMinAndMax greater then 1", insTypeMinAndMax
        print "runnings", runnings
        remainingInsTypesData = remove_max_and_min(runnings, insTypeMinAndMax)
        print "remainingInsTypesData", remainingInsTypesData
        insTypeMinAndMax_1 = retrieve_minAndmax_runtimes(remainingInsTypesData)
        print "insTypeMinAndMax_1", insTypeMinAndMax_1
        remainingInsTypesData_1 = remove_max_and_min(remainingInsTypesData, insTypeMinAndMax_1)
        print "remainingInsTypesData_1", remainingInsTypesData_1
        insTypeMinAndMax_2 = retrieve_minAndmax_runtimes(remainingInsTypesData_1)
        print "insTypeMinAndMax_2", insTypeMinAndMax_2
        remainingInsTypesData_2 = remove_max_and_min(remainingInsTypesData_1, insTypeMinAndMax_2)
        print "remainingInsTypesData_2", remainingInsTypesData_2
        insTypeMinAndMax_3 = retrieve_minAndmax_runtimes(remainingInsTypesData_2)
        print "insTypeMinAndMax_3", insTypeMinAndMax_3
        All_maxAndMin_InsTypes = heavyCalcInsTypes + insTypeMinAndMax + insTypeMinAndMax_1 + insTypeMinAndMax_2 + insTypeMinAndMax_3
        print "All_maxAndMin_InsTypes", All_maxAndMin_InsTypes
    if len(insTypeMinAndMax) == 1:
        print "insTypeMinAndMax = 1"
        remainingInsTypesData = {}
        print "remainingInsTypesData", remainingInsTypesData
        insTypeMinAndMax_1 = []
        print "insTypeMinAndMax_1", insTypeMinAndMax_1
        All_maxAndMin_InsTypes = []
        print "All_maxAndMin_InsTypes", All_maxAndMin_InsTypes
    if riskFactor == 'HistoricalVariance':
        varianceSwap_QF = heavyCalcIns_QF + "_VARSWAP"
        taskName_VarSwap = varianceSwap_QF + taskNameSuffixConvention[riskFactor]
        acc_varianceSwap_QF = acc_heavyCalcIns_QF + "_VARSWAP"
        acc_taskName_VarSwap = acc_varianceSwap_QF + taskNameSuffixConvention[riskFactor]
        if len(LevelPortfolios) != 0:
            createNewQueryFolder(sysPL_master_Qf_Theta, varianceSwap_QF)
            for portfolio in LevelPortfolios:
                queryFolderUpdate(varianceSwap_QF, portfolio, 'Portfolio')
            queryFolderUpdate(varianceSwap_QF, 'VarianceSwap', 'InsType')
            commitChangesToQueryFolder(varianceSwap_QF)
            createPLETasks('HistoricalVariance', varianceSwap_QF, posSpec, riskFactor, context, module, taskName_VarSwap, default_outputDirectory, taskName_VarSwap, None)
        if len(accrualPortfolios) != 0:
            createNewQueryFolder(sysPL_master_Qf_Theta, acc_varianceSwap_QF)
            for portfolio in accrualPortfolios:
                queryFolderUpdate(acc_varianceSwap_QF, portfolio, 'Portfolio')
            queryFolderUpdate(acc_varianceSwap_QF, 'VarianceSwap', 'InsType')
            commitChangesToQueryFolder(acc_varianceSwap_QF)
            createPLETasks('HistoricalVariance', acc_varianceSwap_QF, posSpec, riskFactor, context, module, acc_taskName_VarSwap, default_outputDirectory, acc_taskName_VarSwap, None)
    if riskFactor != 'HistoricalVariance':
        if useMaturityBuckets:# allocate tasks & queryfolders for instrument types listed in heavyCalcInsTypes list
            shortMaturity_QF = heavyCalcIns_QF + "_SM"
            mediumMaturity_QF = heavyCalcIns_QF + "_MM"        
            longMaturity_QF = heavyCalcIns_QF + "_LM"
            portfolioSwap_QF_SOB = heavyCalcIns_QF + "_PSWAP_SOB"
            portfolioSwap_QF_COB = heavyCalcIns_QF + "_PSWAP_COB"
            taskName_ShortMat = shortMaturity_QF + taskNameSuffixConvention[riskFactor]
            taskName_MediumMat = mediumMaturity_QF + taskNameSuffixConvention[riskFactor]
            taskName_LongMat = longMaturity_QF + taskNameSuffixConvention[riskFactor]
            taskName_PSwap_SOB = portfolioSwap_QF_SOB + taskNameSuffixConvention['Theta_PSwap_SOB']
            taskName_PSwap_COB = portfolioSwap_QF_COB + taskNameSuffixConvention['Theta_PSwap_COB']
            acc_shortMaturity_QF = acc_heavyCalcIns_QF + "_SM"
            acc_mediumMaturity_QF = acc_heavyCalcIns_QF + "_MM"        
            acc_longMaturity_QF = acc_heavyCalcIns_QF + "_LM"
            acc_portfolioSwap_QF_SOB = acc_heavyCalcIns_QF + "_PSWAP_SOB"
            acc_portfolioSwap_QF_COB = acc_heavyCalcIns_QF + "_PSWAP_COB"
            acc_taskName_ShortMat = acc_shortMaturity_QF + taskNameSuffixConvention[riskFactor]
            acc_taskName_MediumMat = acc_mediumMaturity_QF + taskNameSuffixConvention[riskFactor]
            acc_taskName_LongMat = acc_longMaturity_QF + taskNameSuffixConvention[riskFactor]
            acc_taskName_PSwap_SOB = acc_portfolioSwap_QF_SOB + taskNameSuffixConvention['Theta_PSwap_SOB']
            acc_taskName_PSwap_COB = acc_portfolioSwap_QF_COB + taskNameSuffixConvention['Theta_PSwap_COB']
            if riskFactor == 'Theta':
                newList = filterOutPSwaps(heavyCalcInsTypes)
                if len(LevelPortfolios) != 0:
                    createNewQueryFolder(sysPL_master_Qf_Theta_ShortMaturity, shortMaturity_QF)
                    createNewQueryFolder(sysPL_master_Qf_Theta_MediumMaturity, mediumMaturity_QF)
                    createNewQueryFolder(sysPL_master_Qf_Theta_LongMaturity, longMaturity_QF)
                    createNewQueryFolder(sysPL_master_Qf_Theta_SOB, portfolioSwap_QF_SOB)
                    createNewQueryFolder(sysPL_master_Qf_Theta, portfolioSwap_QF_COB)
                    for portfolio in LevelPortfolios:
                        queryFolderUpdate(shortMaturity_QF, portfolio, 'Portfolio')
                        queryFolderUpdate(mediumMaturity_QF, portfolio, 'Portfolio')
                        queryFolderUpdate(longMaturity_QF, portfolio, 'Portfolio')
                        queryFolderUpdate(portfolioSwap_QF_SOB, portfolio, 'Portfolio')
                        queryFolderUpdate(portfolioSwap_QF_COB, portfolio, 'Portfolio')
                    for instrumentType in newList:
                        queryFolderUpdate(shortMaturity_QF, instrumentType, 'InsType')  
                        queryFolderUpdate(mediumMaturity_QF, instrumentType, 'InsType')  
                        queryFolderUpdate(longMaturity_QF, instrumentType, 'InsType')   
                    queryFolderUpdate(portfolioSwap_QF_SOB, 'Portfolio Swap', 'InsType')   
                    queryFolderUpdate(portfolioSwap_QF_COB, 'Portfolio Swap', 'InsType')  
                    commitChangesToQueryFolder(shortMaturity_QF)
                    commitChangesToQueryFolder(mediumMaturity_QF)
                    commitChangesToQueryFolder(longMaturity_QF)
                    commitChangesToQueryFolder(portfolioSwap_QF_SOB)
                    commitChangesToQueryFolder(portfolioSwap_QF_COB)
                    createPLETasks('Theta', shortMaturity_QF, posSpec, riskFactor, context, module, taskName_ShortMat, default_outputDirectory, shortMaturity_QF, None)
                    createPLETasks('Theta', mediumMaturity_QF, posSpec, riskFactor, context, module, taskName_MediumMat, default_outputDirectory, mediumMaturity_QF, None)
                    createPLETasks('Theta', longMaturity_QF, posSpec, riskFactor, context, module, taskName_LongMat, default_outputDirectory, longMaturity_QF, None)
                    createPLETasks('Theta_PSwap_SOB', portfolioSwap_QF_SOB, posSpec, riskFactor, context, module, taskName_PSwap_SOB, default_outputDirectory, portfolioSwap_QF_SOB, None)
                    createPLETasks('Theta_PSwap_COB', portfolioSwap_QF_COB, posSpec, riskFactor, context, module, taskName_PSwap_COB, default_outputDirectory, portfolioSwap_QF_COB, None)
                if len(accrualPortfolios) != 0:
                    createNewQueryFolder(sysPL_master_Qf_Theta_ShortMaturity, acc_shortMaturity_QF)
                    createNewQueryFolder(sysPL_master_Qf_Theta_MediumMaturity, acc_mediumMaturity_QF)
                    createNewQueryFolder(sysPL_master_Qf_Theta_LongMaturity, acc_longMaturity_QF)
                    createNewQueryFolder(sysPL_master_Qf_Theta_SOB, acc_portfolioSwap_QF_SOB)
                    createNewQueryFolder(sysPL_master_Qf_Theta, acc_portfolioSwap_QF_COB)
                    for portfolio in accrualPortfolios:
                        queryFolderUpdate(acc_shortMaturity_QF, portfolio, 'Portfolio')
                        queryFolderUpdate(acc_mediumMaturity_QF, portfolio, 'Portfolio')
                        queryFolderUpdate(acc_longMaturity_QF, portfolio, 'Portfolio')
                        queryFolderUpdate(acc_portfolioSwap_QF_SOB, portfolio, 'Portfolio')
                        queryFolderUpdate(acc_portfolioSwap_QF_COB, portfolio, 'Portfolio')
                    for instrumentType in newList:    
                        queryFolderUpdate(acc_shortMaturity_QF, instrumentType, 'InsType')  
                        queryFolderUpdate(acc_mediumMaturity_QF, instrumentType, 'InsType')  
                        queryFolderUpdate(acc_longMaturity_QF, instrumentType, 'InsType')    
                    queryFolderUpdate(acc_portfolioSwap_QF_SOB, 'Portfolio Swap', 'InsType')    
                    queryFolderUpdate(acc_portfolioSwap_QF_COB, 'Portfolio Swap', 'InsType')  
                    commitChangesToQueryFolder(acc_shortMaturity_QF)
                    commitChangesToQueryFolder(acc_mediumMaturity_QF)
                    commitChangesToQueryFolder(acc_longMaturity_QF)
                    commitChangesToQueryFolder(acc_portfolioSwap_QF_SOB)
                    commitChangesToQueryFolder(acc_portfolioSwap_QF_COB)
                    createPLETasks('Theta', acc_shortMaturity_QF, posSpec, riskFactor, context, module, acc_taskName_ShortMat, default_outputDirectory, acc_shortMaturity_QF, True)
                    createPLETasks('Theta', acc_mediumMaturity_QF, posSpec, riskFactor, context, module, acc_taskName_MediumMat, default_outputDirectory, acc_mediumMaturity_QF, True)
                    createPLETasks('Theta', acc_longMaturity_QF, posSpec, riskFactor, context, module, acc_taskName_LongMat, default_outputDirectory, acc_longMaturity_QF, True)
                    createPLETasks('Theta_PSwap_SOB', acc_portfolioSwap_QF_SOB, posSpec, riskFactor, context, module, acc_taskName_PSwap_SOB, default_outputDirectory, acc_portfolioSwap_QF_SOB, True)
                    createPLETasks('Theta_PSwap_COB', acc_portfolioSwap_QF_COB, posSpec, riskFactor, context, module, acc_taskName_PSwap_COB, default_outputDirectory, acc_portfolioSwap_QF_COB, True)
            else:
                createNewQueryFolder(sysPL_master_Qf_ShortMaturity, shortMaturity_QF)
                createNewQueryFolder(sysPL_master_Qf_MediumMaturity, mediumMaturity_QF)
                createNewQueryFolder(sysPL_master_Qf_LongMaturity, longMaturity_QF)
                if len(LevelPortfolios) != 0:
                    for portfolio in LevelPortfolios:
                        queryFolderUpdate(shortMaturity_QF, portfolio, 'Portfolio')
                        queryFolderUpdate(mediumMaturity_QF, portfolio, 'Portfolio')
                        queryFolderUpdate(longMaturity_QF, portfolio, 'Portfolio')
                if len(accrualPortfolios) != 0:
                    for portfolio in accrualPortfolios:
                        queryFolderUpdate(shortMaturity_QF, portfolio, 'Portfolio')
                        queryFolderUpdate(mediumMaturity_QF, portfolio, 'Portfolio')
                        queryFolderUpdate(longMaturity_QF, portfolio, 'Portfolio')
                for instrumentType in heavyCalcInsTypes:
                    queryFolderUpdate(shortMaturity_QF, instrumentType, 'InsType')  
                    queryFolderUpdate(mediumMaturity_QF, instrumentType, 'InsType')  
                    queryFolderUpdate(longMaturity_QF, instrumentType, 'InsType')   
                commitChangesToQueryFolder(shortMaturity_QF)
                commitChangesToQueryFolder(mediumMaturity_QF)
                commitChangesToQueryFolder(longMaturity_QF)
                createPLETasks('Sensitivities', shortMaturity_QF, posSpec, riskFactor, context, module, taskName_ShortMat, default_outputDirectory, shortMaturity_QF, None)
                createPLETasks('Sensitivities', mediumMaturity_QF, posSpec, riskFactor, context, module, taskName_MediumMat, default_outputDirectory, mediumMaturity_QF, None)
                createPLETasks('Sensitivities', longMaturity_QF, posSpec, riskFactor, context, module, taskName_LongMat, default_outputDirectory, longMaturity_QF, None)
        #allocate tasks & queryfolders for instrument types NOT listed in heavyCalcInsTypes list         
        if len(insTypeMinAndMax) != 0: #first max & min run time iteration
            if riskFactor == 'Theta':
                if len(LevelPortfolios) != 0:
                    createNewQueryFolder(sysPL_master_Qf_Theta, newQF_A)
                    for portfolio in LevelPortfolios:
                        queryFolderUpdate(newQF_A, portfolio, 'Portfolio')
                    for ins in list(set(insTypeMinAndMax)): 
                        queryFolderUpdate(newQF_A, ins, 'InsType')  
                    commitChangesToQueryFolder(newQF_A)
                    createPLETasks('Theta', newQF_A, posSpec, riskFactor, context, module, taskName_A, default_outputDirectory, newQF_A, None)
                if len(accrualPortfolios) != 0:
                    createNewQueryFolder(sysPL_master_Qf_Theta, acc_newQF_D)
                    for portfolio in accrualPortfolios:
                        queryFolderUpdate(acc_newQF_D, portfolio, 'Portfolio')
                    for ins in list(set(insTypeMinAndMax)): 
                        queryFolderUpdate(acc_newQF_D, ins, 'InsType')  
                    commitChangesToQueryFolder(acc_newQF_D)
                    createPLETasks('Theta', acc_newQF_D, posSpec, riskFactor, context, module, acc_taskName_D, default_outputDirectory, acc_newQF_D, True)
            else:
                createNewQueryFolder(sens_master_Qf, newQF_A)
                if len(LevelPortfolios) != 0:
                    for portfolio in LevelPortfolios:
                        queryFolderUpdate(newQF_A, portfolio, 'Portfolio')
                if len(accrualPortfolios) != 0:
                    for portfolio in accrualPortfolios:
                        queryFolderUpdate(newQF_A, portfolio, 'Portfolio')
                for ins in list(set(insTypeMinAndMax)): 
                    queryFolderUpdate(newQF_A, ins, 'InsType')  
                commitChangesToQueryFolder(newQF_A)
                createPLETasks('Sensitivities', newQF_A, posSpec, riskFactor, context, module, taskName_A, default_outputDirectory, newQF_A, None)
        if len(insTypeMinAndMax_1) != 0: #second max & min run time iteration
            if riskFactor == 'Theta':
                if len(LevelPortfolios) != 0:
                    createNewQueryFolder(sysPL_master_Qf_Theta, newQF_B)
                    for portfolio in LevelPortfolios:
                        queryFolderUpdate(newQF_B, portfolio, 'Portfolio')
                    for ins in list(set(insTypeMinAndMax_1)): 
                        queryFolderUpdate(newQF_B, ins, 'InsType')
                    commitChangesToQueryFolder(newQF_B)
                    createPLETasks('Theta', newQF_B, posSpec, riskFactor, context, module, taskName_B, default_outputDirectory, newQF_B, None)
                if len(accrualPortfolios) != 0:
                    createNewQueryFolder(sysPL_master_Qf_Theta, acc_newQF_E)
                    for portfolio in accrualPortfolios:
                        queryFolderUpdate(acc_newQF_E, portfolio, 'Portfolio')
                    for ins in list(set(insTypeMinAndMax_1)): 
                        queryFolderUpdate(acc_newQF_E, ins, 'InsType')  
                    commitChangesToQueryFolder(acc_newQF_E)
                    createPLETasks('Theta', acc_newQF_E, posSpec, riskFactor, context, module, acc_taskName_E, default_outputDirectory, acc_newQF_E, True)
            else: 
                createNewQueryFolder(sens_master_Qf, newQF_B)
                if len(LevelPortfolios) != 0:
                    for portfolio in LevelPortfolios:
                        queryFolderUpdate(newQF_B, portfolio, 'Portfolio')
                if len(accrualPortfolios) != 0:
                    for portfolio in accrualPortfolios:
                        queryFolderUpdate(newQF_B, portfolio, 'Portfolio')
                for ins in list(set(insTypeMinAndMax_1)): 
                    queryFolderUpdate(newQF_B, ins, 'InsType')
                commitChangesToQueryFolder(newQF_B)
                createPLETasks('Sensitivities', newQF_B, posSpec, riskFactor, context, module, taskName_B, default_outputDirectory, newQF_B, None)
        if len(insTypeMinAndMax_2) != 0: #third max & min run time iteration
            if riskFactor == 'Theta':
                if len(LevelPortfolios) != 0:
                    createNewQueryFolder(sysPL_master_Qf_Theta, newQF_C)
                    for portfolio in LevelPortfolios:
                        queryFolderUpdate(newQF_C, portfolio, 'Portfolio')
                    for ins in list(set(insTypeMinAndMax_2)): 
                        queryFolderUpdate(newQF_C, ins, 'InsType')
                    commitChangesToQueryFolder(newQF_C)
                    createPLETasks('Theta', newQF_C, posSpec, riskFactor, context, module, taskName_C, default_outputDirectory, newQF_C, None)
                if len(accrualPortfolios) != 0:
                    createNewQueryFolder(sysPL_master_Qf_Theta, acc_newQF_F)
                    for portfolio in accrualPortfolios:
                        queryFolderUpdate(acc_newQF_F, portfolio, 'Portfolio')
                    for ins in list(set(insTypeMinAndMax_2)): 
                        queryFolderUpdate(acc_newQF_F, ins, 'InsType')  
                    commitChangesToQueryFolder(acc_newQF_F)
                    createPLETasks('Theta', acc_newQF_F, posSpec, riskFactor, context, module, acc_taskName_F, default_outputDirectory, acc_newQF_F, True)
            else: 
                createNewQueryFolder(sens_master_Qf, newQF_C)
                if len(LevelPortfolios) != 0:
                    for portfolio in LevelPortfolios:
                        queryFolderUpdate(newQF_C, portfolio, 'Portfolio')
                if len(accrualPortfolios) != 0:
                    for portfolio in accrualPortfolios:
                        queryFolderUpdate(newQF_C, portfolio, 'Portfolio')
                for ins in list(set(insTypeMinAndMax_2)): 
                    queryFolderUpdate(newQF_C, ins, 'InsType')
                commitChangesToQueryFolder(newQF_C)
                createPLETasks('Sensitivities', newQF_C, posSpec, riskFactor, context, module, taskName_C, default_outputDirectory, newQF_C, None)
        if len(insTypeMinAndMax_3) != 0: #fourth max & min run time iteration
            if riskFactor == 'Theta':
                if len(LevelPortfolios) != 0:
                    createNewQueryFolder(sysPL_master_Qf_Theta, newQF_D)
                    for portfolio in LevelPortfolios:
                        queryFolderUpdate(newQF_D, portfolio, 'Portfolio')
                    for ins in list(set(insTypeMinAndMax_3)): 
                        queryFolderUpdate(newQF_D, ins, 'InsType')
                    commitChangesToQueryFolder(newQF_D)
                    createPLETasks('Theta', newQF_D, posSpec, riskFactor, context, module, taskName_D, default_outputDirectory, newQF_D, None)
                if len(accrualPortfolios) != 0:
                    createNewQueryFolder(sysPL_master_Qf_Theta, acc_newQF_G)
                    for portfolio in accrualPortfolios:
                        queryFolderUpdate(acc_newQF_G, portfolio, 'Portfolio')
                    for ins in list(set(insTypeMinAndMax_3)): 
                        queryFolderUpdate(acc_newQF_G, ins, 'InsType')
                    commitChangesToQueryFolder(acc_newQF_G)
                    createPLETasks('Theta', acc_newQF_G, posSpec, riskFactor, context, module, acc_taskName_G, default_outputDirectory, acc_newQF_G, True)
            else: 
                createNewQueryFolder(sens_master_Qf, newQF_D)
                if len(LevelPortfolios) != 0:
                    for portfolio in LevelPortfolios:
                        queryFolderUpdate(newQF_D, portfolio, 'Portfolio')
                if len(accrualPortfolios) != 0:
                    for portfolio in accrualPortfolios:
                        queryFolderUpdate(newQF_D, portfolio, 'Portfolio')
                for ins in list(set(insTypeMinAndMax_3)): 
                    queryFolderUpdate(newQF_D, ins, 'InsType')
                commitChangesToQueryFolder(newQF_D)
                createPLETasks('Sensitivities', newQF_D, posSpec, riskFactor, context, module, taskName_D, default_outputDirectory, newQF_D, None)
        if len(All_maxAndMin_InsTypes) != 0: #not ins types from first,second, third and fourth max & min run time iteration
            if riskFactor == 'Theta':
                if len(LevelPortfolios) != 0:
                    createNewQueryFolder(sysPL_master_Qf_Theta_not, newQF_E)
                    for portfolio in LevelPortfolios:
                        queryFolderUpdate(newQF_E, portfolio, 'Portfolio')
                    for ins in list(set(All_maxAndMin_InsTypes)): 
                        queryFolderUpdate(newQF_E, ins, 'InsType')
                    commitChangesToQueryFolder(newQF_E)
                    createPLETasks('Theta', newQF_E, posSpec, riskFactor, context, module, taskName_E, default_outputDirectory, newQF_E, None)
                if len(accrualPortfolios) != 0:
                    createNewQueryFolder(sysPL_master_Qf_Theta_not, acc_newQF_H)
                    for portfolio in accrualPortfolios:
                        queryFolderUpdate(acc_newQF_H, portfolio, 'Portfolio')
                    for ins in list(set(All_maxAndMin_InsTypes)): 
                        queryFolderUpdate(acc_newQF_H, ins, 'InsType') 
                    commitChangesToQueryFolder(acc_newQF_H)
                    createPLETasks('Theta', acc_newQF_H, posSpec, riskFactor, context, module, acc_taskName_H, default_outputDirectory, acc_newQF_H, True)
            else: 
                createNewQueryFolder(sens_master_Qf_not, newQF_E)
                if len(LevelPortfolios) != 0:
                    for portfolio in LevelPortfolios:
                        queryFolderUpdate(newQF_E, portfolio, 'Portfolio')
                if len(accrualPortfolios) != 0:
                    for portfolio in accrualPortfolios:
                        queryFolderUpdate(newQF_E, portfolio, 'Portfolio')
                for ins in list(set(All_maxAndMin_InsTypes)): 
                    queryFolderUpdate(newQF_E, ins, 'InsType')
                commitChangesToQueryFolder(newQF_E)
                createPLETasks('Sensitivities', newQF_E, posSpec, riskFactor, context, module, taskName_E, default_outputDirectory, newQF_E, None)

            
"""---------------------------------------------------------------------------------------------"""
   
def _CreateSensitivityTasksAndQueryFolders(RunAtLevel, level, type_id, data, posSpec):
    CreateQueryFoldersAndTasksAtRunLevel(RunAtLevel, level, "Benchmark", None, None, posSpec, True)
    CreateQueryFoldersAndTasksAtRunLevel(RunAtLevel, level, "InterestRate", None, None, posSpec, True)
    CreateQueryFoldersAndTasksAtRunLevel(RunAtLevel, level, "Inflation", None, None, posSpec, True)
    CreateQueryFoldersAndTasksAtRunLevel(RunAtLevel, level, "InstrumentSpread", None, None, posSpec, True)
    CreateQueryFoldersAndTasksAtRunLevel(RunAtLevel, level, "Theta", None, None, posSpec, True)
    CreateQueryFoldersAndTasksAtRunLevel(RunAtLevel, level, "FXRate", None, None, posSpec, True)
    CreateQueryFoldersAndTasksAtRunLevel(RunAtLevel, level, "EquityPrice", None, None, posSpec, True)
    CreateQueryFoldersAndTasksAtRunLevel(RunAtLevel, level, "Volatility", None, None, posSpec, True)
    CreateQueryFoldersAndTasksAtRunLevel(RunAtLevel, level, "HistoricalVariance", None, None, posSpec, True)
    CreateQueryFoldersAndTasksAtRunLevel(RunAtLevel, level, "Dividend", None, None, posSpec, True)


localOutputPath = 'C:\Users\AB00697\Desktop\Pnl_Explain\Extracts\\'
outputPath = 'C:\Users\AB00697\Desktop\Extracts\\'
file = 'FixedIncomeTrading_testingLoad.csv'

absa_fa_physicalPortfolios = getPLeligiblePorfolioList()  
absa_fa_majorDesks = sorted(getMajorDesk())
absa_fa_minorDesks = sorted(getMinorDesk())
absa_fa_masterBooks = sorted(getMasterBooks())
positionSpecs = acm.FPositionSpecification.Select('')
trueAndFalseSelectionList = [True, False]

  
ael_gui_parameters = {'hideExtracControls': True,
                      'windowCaption': 'PL Explain Task Load Balancer'}

ael_variables = [ ['ABSA_MajorDesks', 'Major Desk', 'string', absa_fa_majorDesks, None, 0],
                  ['ABSA_MinorDesks', 'Minor Desk', 'string', absa_fa_minorDesks, None, 0],
                  ['ABSA_MasterBooks', 'Masterbook', 'string', absa_fa_masterBooks, None, 0],
                  ['ABSA_PhysicalPortfolios', 'Physical Portfolio', 'string', absa_fa_physicalPortfolios, None, 0],
                  ['ABSA_PositionSpecs', 'Position Specifications', 'string', positionSpecs, posSpecDefault, 0],
                  ['runAtMajorDeskLevel', 'Run at Major Desk Level', 'string', trueAndFalseSelectionList, False, 0],
                  ['runAtMinorDeskLevel', 'Run at MinorDesk Level', 'string', trueAndFalseSelectionList, False, 0],
                  ['runAtMasterBookLevel', 'Run at Masterbook Level', 'string', trueAndFalseSelectionList, False, 0],
                  ['runAtPortfolioLevel', 'Run at Portfolio Level', 'string', trueAndFalseSelectionList, False, 0]]


def ael_main(ael_dict):
    ABSA_MajorDesks = ael_dict['ABSA_MajorDesks']
    ABSA_MinorDesks = ael_dict['ABSA_MinorDesks']
    ABSA_MasterBooks = ael_dict['ABSA_MasterBooks']
    ABSA_PhysicalPortfolios = ael_dict['ABSA_PhysicalPortfolios']
    posSpec = str(ael_dict['ABSA_PositionSpecs'])
    runAtMajorDeskLevel = ael_dict['runAtMajorDeskLevel']
    runAtMinorDeskLevel = ael_dict['runAtMinorDeskLevel']
    runAtMasterBookLevel = ael_dict['runAtMasterBookLevel']
    runAtPortfolioLevel = ael_dict['runAtPortfolioLevel']
    print("********Running PL Explain Load Balancer Analysis***************", _nowTime())
    start_time= time.time()
    if runAtMajorDeskLevel == 'true':
        print("Run at Major Desk Level is ticked")
        if ABSA_MajorDesks:
            majorDesk = str(ABSA_MajorDesks)
            _CreateSensitivityTasksAndQueryFolders('MajorDesk', majorDesk, None, None, posSpec)
    if runAtMinorDeskLevel == 'true':
        print("Run at Minor Desk Level is ticked")
        if ABSA_MinorDesks:
            minorDesk = str(ABSA_MinorDesks)
            print 'minorDesk', minorDesk
            _CreateSensitivityTasksAndQueryFolders('MinorDesk', minorDesk, None, None, posSpec)
    if runAtMasterBookLevel == 'true':
        print("Run at Masterbook Level is ticked")
        if ABSA_MasterBooks:
            masterBook = str(ABSA_MasterBooks)
            _CreateSensitivityTasksAndQueryFolders('Masterbook', masterBook, None, None, posSpec)
    elif runAtPortfolioLevel == 'true':
        print("Run at Portfolio Level is ticked")      
        if ABSA_PhysicalPortfolios:
            portSelection = acm.FPhysicalPortfolio.Select('name = %s' %ABSA_PhysicalPortfolios)
            if len(portSelection) == 1:
                runPortfolio = portSelection[0].Name()
                _CreateSensitivityTasksAndQueryFolders('Portfolio', runPortfolio, None, None, posSpec)              
    elif runAtMajorDeskLevel == 'false':
        print("Run at Major Desk Level is unticked")
    elif runAtMinorDeskLevel == 'false':
        print("Run at Minor Desk Level is unticked")
    elif runAtMasterBookLevel == 'false':
        print("Run at Masterbook Level is unticked")
    elif runAtPortfolioLevel == 'false':
        print("Run at Portfolio Level is unticked")
    print("********Finished PL Explain Load Balancer Analysis***************", _nowTime())
    end_time = time.time()
    duration = end_time - start_time
    print("Total Batch Run Time Duration:", _convertTimeInSecondsToHoursMinutesSeconds(duration))
    







