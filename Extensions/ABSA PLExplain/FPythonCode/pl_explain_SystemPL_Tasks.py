"""---------------------------------------------------------------------------------------------
MODULE
    pl_explain_SystemPL_Tasks - 

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

context     = acm.GetDefaultContext()
contextDefinition = 'FC Accrual Books'
sens_master_Qf = acm.FStoredASQLQuery['PLE_Master_Sensitivities']
sens_master_Qf_not = acm.FStoredASQLQuery['PLE_Master_Sensitivities_NotInsType']
sysPL_master_Qf = acm.FStoredASQLQuery['PLE_Master_SystemPL']
sysPL_master_Qf_not = acm.FStoredASQLQuery['PLE_Master_SystemPL_NotInsType']

posSpecDefault = 'PLE Cpty/Curr/Port/InsType/TradeOid'
module = 'FArtiQMarketRiskExport'
today = acm.Time.DateToday()
yesterday = acm.Time.DateAdjustPeriod(today, '-1d', 'ZAR Johannesburg', 'Preceding')
dateDiff = str(acm.Time.DateDifference(yesterday, today)) + 'd'
firstOfMonth = acm.Time.FirstDayOfMonth(today)
amendmentPL_script = 'pl_explain_assign_edits_resets'
cancelledPL_script = 'pl_explain_dropped_deals'
priceAttributeParse_script = 'pl_explain_parse_PriceAttributePLFiles'


queryFolderMappings = {"Aggregate": "PLE_Master_Aggregate",
                       "Funding": "PLE_Master_FundingPL",
                       "NewTrades": "PLE_Master_NewTrades",
                       "Amendment": "PLE_Master_Amendments",
                       "SystemPL": "PLE_Master_NonVoidAndSimulated",
                       "HigherOrder_Voids": "PLE_Master_HigherOrder_Voids",
                       "HigherOrder": "PLE_Master_HigherOrder",
                      }

fileNameConventions = {"MajorDesk": "_MAD_",
                       "MinorDesk": "_MND_",
                       "Masterbook": "_MB_",
                       "Portfolio": "_P_",
                      }

systemPLColumnMappings = { "Accrual": "Portfolio Total Profit and Loss Accrual",
                           "MtM": "Portfolio Total Profit and Loss",
                           "SystemPL_MtM": "Portfolio Accumulated Cash,Portfolio Value",
                           "SystemPL_Accrual": "Portfolio Accumulated Cash,Portfolio Value Accrual",
                         }  

adaptivColumnMappings = { "Aggregate": "Aggregate Trades PL",
                          "Funding": "Funding PL",
                          "NewTrades": "New Trades PL",
                          "Amendment_SOB": "Total PL SOB",
                          "Amendment_COB": "Total PL COB",
                          "SystemPL": "Total Cash,Total PV",
                          "HigherOrder": "Total PL HO SOB",
                         }      
                         
taskNameSuffixConvention = { "Aggregate": "_T1_SERVER",
                             "Funding": "_T1_SERVER",
                             "NewTrades": "_T1_SERVER",
                             "CancelDeals": "_T1_SERVER",
                             "Amendment": "_T1_SERVER",
                             "Amendment_SOB": "_T0_SERVER",
                             "Amendment_COB": "_WS_T1_SERVER",
                             "SystemPL": "_T1_SERVER",
                             "SourcePL": "_T1_SERVER",
                             "HigherOrder": "_WS_T1_SERVER",
                             "PriceAttribute": "_WS_T1_SERVER",
                            }
                         
calcTypeOutputFolderMappings = {"Amendment_SOB": "Amendment_SOB",
                                "Amendment_COB": "Amendment_COB",
                                }
                                
dependencyOutputFolderMappings = {"CancelDeals": "SystemPL",
                                 }

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

def compare_lists(list1, list2):
    new_list = []
    for obj in list1:
        if not obj in list2:
            new_list.append(obj)
    return new_list
    

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

def createSystemPLETasks(calc_type, qf, posSpec, context, module, task_name, default_outputDirectory, outputFileName, portAccType, queryList):
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
    
    #Logging tab
    task_params.AtPutStrings("LogToConsole", "1")
    task_params.AtPutStrings("LogToFile", "0")
    task_params.AtPutStrings("Logmode", "2")
    #Ouput tab
    task_params.AtPutStrings("Output File Date", "False")
    task_params.AtPutStrings("Create directory with date", "True")
    task_params.AtPutStrings("output_dir", outputFilePath)
    task_params.AtPutStrings("Overwrite if file exists", "True")
    # Greeks tab
    if calc_type != 'HigherOrder':
        task_params.AtPutStrings("storedASQLQueries", qf)
    if calc_type == 'HigherOrder':
        task_params.AtPutStrings("storedASQLQueries", queryList)
    if calc_type == 'SourcePL':
        task_params.AtPutStrings("runPnLReports", "1")
        task_params.AtPutStrings("PL File Name", outputFileName)
        task_params.AtPutStrings("total_pl_source", "Total")
        task_params.AtPutStrings("clean_pl_source", "Hypothetical")
        task_params.AtPutStrings("daily_pl_source", "DailyTotal")
    if calc_type != 'SourcePL':
        task_params.AtPutStrings("runGreekReports", "1")
        task_params.AtPutStrings("greeks_file", qf)
        task_params.AtPutStrings("measures_Greeks", adaptivColumnMappings[calc_type]);
        task_params.AtPutStrings("column_name_Greeks", systemPLColumnMappings[portAccType]) # for Accrual or MtM portfolio accounting types
    task.Name(task_name)
    task.Parameters(task_params)
    task.Commit()
    print ("Committed task: %s" %(task.Name())) 
    
def checkForExistingTask(task_name):
    existingTask = acm.FAelTask[task_name]
    if existingTask: #check if task exists already, if so delete it
        existingTask.Delete()
        print ("Removed task: %s" %(task_name))


def createSystemPlParsingTasks(calc_type, qf_1, qf_2, qf_3, context, module, default_outputDirectory, groupingLevel, outputFileName, portAccType, dependencyTask_outputDirectory):
    # build new task from scratch
    task = acm.FAelTask()    
    task.ModuleName(module)
    task.ContextName(context)
    task_params = task.Parameters()    
    additionalFolder = check_riskFactor_outputFolder(calcTypeOutputFolderMappings, calc_type)
    outputFilePath = concatenate_file_path(default_outputDirectory, additionalFolder)
    file_Path = outputFilePath
    dependencyAddFolder = check_riskFactor_outputFolder(dependencyOutputFolderMappings, calc_type)
    dependencyPath = concatenate_file_path(dependencyTask_outputDirectory, dependencyAddFolder)
    dependency_file_Path = dependencyPath + "/"
    if calc_type == 'Amendment':
        """default settings"""
        input_SOBfile = qf_1 + ".csv"
        input_COBfile = qf_2 + ".csv"
        SOB_dependencyAddFolder = check_riskFactor_outputFolder(dependencyOutputFolderMappings, 'Amendment_SOB')
        SOB_dependencyPath = concatenate_file_path(dependencyTask_outputDirectory, SOB_dependencyAddFolder)
        SOB_dependency_file_Path = SOB_dependencyPath + "/"
        COB_dependencyAddFolder = check_riskFactor_outputFolder(dependencyOutputFolderMappings, 'Amendment_COB')
        COB_dependencyPath = concatenate_file_path(dependencyTask_outputDirectory, COB_dependencyAddFolder)
        COB_dependency_file_Path = COB_dependencyPath + "/"
        if portAccType == 'Accrual':
            output_file = "PLE_AmendmentPL_Accrual_" + fileNameConventions[groupingLevel] + outputFileName + ".csv"
            task_name = "PLE_AmendmentPL_Accrual" + fileNameConventions[groupingLevel] + outputFileName + taskNameSuffixConvention[calc_type]
        if portAccType == 'MtM':
            output_file = "PLE_AmendmentPL" + fileNameConventions[groupingLevel] + outputFileName + ".csv"
            task_name = "PLE_AmendmentPL" + fileNameConventions[groupingLevel] + outputFileName + taskNameSuffixConvention[calc_type]
        checkForExistingTask(task_name)
        task_params.AtPutStrings("inputPathSOB", SOB_dependency_file_Path)
        task_params.AtPutStrings("inputPathCOB", COB_dependency_file_Path)
        task_params.AtPutStrings("input_fileNameSOB", input_SOBfile)
        task_params.AtPutStrings("input_fileNameCOB", input_COBfile)
        task_params.AtPutStrings("outputPath", file_Path)
        task_params.AtPutStrings("output_fileName", output_file)
        task.Name(task_name)
        task.Parameters(task_params)
        task.Commit()
        print ("Committed task: %s" %(task.Name())) 
    elif calc_type == 'CancelDeals':
        """default settings"""
        input_yesterdayFile = qf_1 + ".csv"
        input_todayFile = qf_1 + ".csv"
        if portAccType == 'Accrual':
            output_file = "PLE_CancelPL_Accrual" + fileNameConventions[groupingLevel] + outputFileName + ".csv"
            task_name = "PLE_CancelPL_Accrual" + fileNameConventions[groupingLevel] + outputFileName + taskNameSuffixConvention[calc_type]
        if portAccType == 'MtM':
            output_file = "PLE_CancelPL" + fileNameConventions[groupingLevel] + outputFileName + ".csv"
            task_name = "PLE_CancelPL" + fileNameConventions[groupingLevel] + outputFileName + taskNameSuffixConvention[calc_type]
        checkForExistingTask(task_name)
        task_params.AtPutStrings("inputPath", dependency_file_Path)
        task_params.AtPutStrings("input_fileName", input_todayFile)
        task_params.AtPutStrings("yesterday_input_fileName", input_yesterdayFile)
        task_params.AtPutStrings("outputPath", file_Path)
        task_params.AtPutStrings("output_fileName", output_file)
        task.Name(task_name)
        task.Parameters(task_params)
        task.Commit()
        print ("Committed task: %s" %(task.Name()))
    elif calc_type == 'HigherOrder':
        """default settings"""
        input_SOBfile = qf_1 + ".csv"
        input_COBfile = qf_2 + ".csv"
        input_Cancelsfile = qf_3 + ".csv"
        inputPathCOB = dependency_file_Path.replace('HigherOrder', 'SystemPL')
        inputPathCancels = dependency_file_Path.replace('HigherOrder', 'CancelDeals')
        final_outputPath = file_Path.replace('HigherOrder', 'PriceAttribute')
        if portAccType == 'Accrual':
            output_file = "PLE_PriceAttributePL_Accrual" + fileNameConventions[groupingLevel] + outputFileName + ".csv"
            task_name = "PLE_PriceAttributePL_Accrual" + fileNameConventions[groupingLevel] + outputFileName + taskNameSuffixConvention[calc_type]
        if portAccType == 'MtM':
            output_file = "PLE_PriceAttributePL" + fileNameConventions[groupingLevel] + outputFileName + ".csv"
            task_name = "PLE_PriceAttributePL" + fileNameConventions[groupingLevel] + outputFileName + taskNameSuffixConvention[calc_type]
        checkForExistingTask(task_name)
        task_params.AtPutStrings("inputPathSOB", dependency_file_Path)
        task_params.AtPutStrings("input_SOB_fileName", input_SOBfile)
        task_params.AtPutStrings("inputPathCOB", inputPathCOB)
        task_params.AtPutStrings("input_COB_fileName", input_COBfile)
        task_params.AtPutStrings("inputPathCancels", inputPathCancels)
        task_params.AtPutStrings("input_CancelNewTradesfileName", input_Cancelsfile)
        task_params.AtPutStrings("outputPath", final_outputPath)
        task_params.AtPutStrings("outputfileName", output_file)
        task.Name(task_name)
        task.Parameters(task_params)
        task.Commit()
        print ("Committed task: %s" %(task.Name()))


"""---------------------------------------------------------------------------------------------"""
""" Create New Query Folders & Update their filtering criteria """

def createNewQueryFolder(master_Qf_name, qf_name):
    """create a child query folder based on a saved master query folder"""
    master_Qf = acm.FStoredASQLQuery[master_Qf_name]
    existingQuery = acm.FStoredASQLQuery[qf_name]
    
    if existingQuery:
        existingQuery.Delete()
    new_qf    = master_Qf.Clone()
    new_qf.Name(qf_name)
    new_qf.AutoUser(False)
    new_qf.Commit()
    print '==> Successfully Created Query Folder: %s.'%(qf_name) 

def queryFolderUpdate(filter_name, new_criteria, _field):
    """update a existing query folder's node with new criteria"""
    filter = acm.FStoredASQLQuery[filter_name]
    query = filter.Query()
    nodes = query.AsqlNodes()
    if _field == 'Portfolio': ins_node = nodes[1]
    if _field == 'InsType': ins_node = nodes[0]
    if _field == 'ExecutionTime': ins_node = nodes[2]
    
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
    if _field == 'ExecutionTime':
        print '==> Successfully Added Execution Time: %s to %s.'%(new_criteria, filter_name)


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
    

def CreateSystemPLQueryFoldersAndTasks(RunAtLevel, level, pl_type, masterQF, secondaryMasterQF, posSpec, default_outputDirectory, dependencyDirectory):
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
    if pl_type == 'Aggregate':
        if len(LevelPortfolios) != 0:
            newQF = "PLE_AggregateTrades" + fileNameConventions[RunAtLevel] + levelName
            taskName = newQF + taskNameSuffixConvention[pl_type]
            createNewQueryFolder(masterQF, newQF)
            for portfolio in LevelPortfolios:
                queryFolderUpdate(newQF, portfolio, 'Portfolio')
            queryFolderUpdate(newQF, dateDiff, 'ExecutionTime')
            commitChangesToQueryFolder(newQF)
            createSystemPLETasks('Aggregate', newQF, posSpec, context, module, taskName, default_outputDirectory, newQF, 'MtM', None)
        if len(accrualPortfolios) != 0: 
            newQF = "PLE_AggregateTradesAccrual" + fileNameConventions[RunAtLevel] + levelName
            taskName = newQF + taskNameSuffixConvention[pl_type]
            createNewQueryFolder(masterQF, newQF)
            for portfolio in accrualPortfolios:
                queryFolderUpdate(newQF, portfolio, 'Portfolio')
            queryFolderUpdate(newQF, dateDiff, 'ExecutionTime')
            commitChangesToQueryFolder(newQF)
            createSystemPLETasks('Aggregate', newQF, posSpec, context, module, taskName, default_outputDirectory, newQF, 'Accrual', None)
    elif pl_type =='Funding':
        if len(LevelPortfolios) != 0:
            newQF = "PLE_Funding" + fileNameConventions[RunAtLevel] + levelName
            taskName = newQF + taskNameSuffixConvention[pl_type]
            createNewQueryFolder(masterQF, newQF)
            for portfolio in LevelPortfolios:
                queryFolderUpdate(newQF, portfolio, 'Portfolio')
            queryFolderUpdate(newQF, firstOfMonth, 'ExecutionTime')
            commitChangesToQueryFolder(newQF)
            createSystemPLETasks('Funding', newQF, posSpec, context, module, taskName, default_outputDirectory, newQF, 'MtM', None)
    elif pl_type == 'NewTrades':
        if len(LevelPortfolios) != 0:
            newQF = "PLE_NewTrades" + fileNameConventions[RunAtLevel] + levelName
            taskName = newQF + taskNameSuffixConvention[pl_type]
            createNewQueryFolder(masterQF, newQF)
            for portfolio in LevelPortfolios:
                queryFolderUpdate(newQF, portfolio, 'Portfolio')
            commitChangesToQueryFolder(newQF)
            createSystemPLETasks('NewTrades', newQF, posSpec, context, module, taskName, default_outputDirectory, newQF, 'MtM', None)
        if len(accrualPortfolios) != 0:
            newQF = "PLE_NewTradesAccrual" + fileNameConventions[RunAtLevel] + levelName
            taskName = newQF + taskNameSuffixConvention[pl_type]
            createNewQueryFolder(masterQF, newQF)
            for portfolio in accrualPortfolios:
                queryFolderUpdate(newQF, portfolio, 'Portfolio')
            commitChangesToQueryFolder(newQF)
            createSystemPLETasks('NewTrades', newQF, posSpec, context, module, taskName, default_outputDirectory, newQF, 'Accrual', None)
    elif pl_type == 'Amendment':
        if len(LevelPortfolios) != 0:
            newQF_SOB = "PLE_AmendPL_SOB" + fileNameConventions[RunAtLevel] + levelName
            newQF_COB = "PLE_AmendPL_COB" + fileNameConventions[RunAtLevel] + levelName
            taskName_SOB = newQF_SOB + taskNameSuffixConvention['Amendment_SOB']
            taskName_COB = newQF_COB + taskNameSuffixConvention['Amendment_COB']
            createNewQueryFolder(masterQF, newQF_SOB)
            createNewQueryFolder(masterQF, newQF_COB)
            for portfolio in LevelPortfolios:
                queryFolderUpdate(newQF_SOB, portfolio, 'Portfolio')
                queryFolderUpdate(newQF_COB, portfolio, 'Portfolio')
            commitChangesToQueryFolder(newQF_SOB)
            commitChangesToQueryFolder(newQF_COB)
            createSystemPLETasks('Amendment_SOB', newQF_SOB, posSpec, context, module, taskName_SOB, default_outputDirectory, newQF_SOB, 'MtM', None)
            createSystemPLETasks('Amendment_COB', newQF_COB, posSpec, context, module, taskName_COB, default_outputDirectory, newQF_COB, 'MtM', None)
            createSystemPlParsingTasks('Amendment', newQF_SOB, newQF_COB, None, context, amendmentPL_script, default_outputDirectory, RunAtLevel, levelName, 'MtM', dependencyDirectory)
        if len(accrualPortfolios) != 0:
            newQF_SOB = "PLE_AmendPL_SOB_Accrual" + fileNameConventions[RunAtLevel] + levelName
            newQF_COB = "PLE_AmendPL_COB_Accrual" + fileNameConventions[RunAtLevel] + levelName
            taskName_SOB = newQF_SOB + taskNameSuffixConvention['Amendment_SOB']
            taskName_COB = newQF_COB + taskNameSuffixConvention['Amendment_COB']
            createNewQueryFolder(masterQF, newQF_SOB)
            createNewQueryFolder(masterQF, newQF_COB)
            for portfolio in accrualPortfolios:
                queryFolderUpdate(newQF_SOB, portfolio, 'Portfolio')
                queryFolderUpdate(newQF_COB, portfolio, 'Portfolio')
            commitChangesToQueryFolder(newQF_SOB)
            commitChangesToQueryFolder(newQF_COB)   
            createSystemPLETasks('Amendment_SOB', newQF_SOB, posSpec, context, module, taskName_SOB, default_outputDirectory, newQF_SOB, 'Accrual', None)
            createSystemPLETasks('Amendment_COB', newQF_SOB, posSpec, context, module, taskName_COB, default_outputDirectory, newQF_COB, 'Accrual', None)
            createSystemPlParsingTasks('Amendment', newQF_SOB, newQF_COB, None, context, amendmentPL_script, default_outputDirectory, RunAtLevel, levelName, 'Accrual', dependencyDirectory)
    elif pl_type == 'SystemPL':
        if len(LevelPortfolios) != 0:
            newQF = "PLE_SystemPL" + fileNameConventions[RunAtLevel] + levelName
            newSourcePLQF = "PLE_SourcePL" + fileNameConventions[RunAtLevel] + levelName
            taskName = newQF + taskNameSuffixConvention[pl_type]
            taskName_SourcePL = newSourcePLQF + taskNameSuffixConvention['SourcePL']
            createNewQueryFolder(masterQF, newQF)
            for portfolio in LevelPortfolios:
                queryFolderUpdate(newQF, portfolio, 'Portfolio')
            commitChangesToQueryFolder(newQF)
            createSystemPLETasks('SystemPL', newQF, posSpec, context, module, taskName, default_outputDirectory, newQF, 'SystemPL_MtM', None)
            createSystemPLETasks('SourcePL', newQF, posSpec, context, module, taskName_SourcePL, default_outputDirectory, newSourcePLQF, None, None)
            createSystemPlParsingTasks('CancelDeals', newQF, None, None, context, cancelledPL_script, default_outputDirectory, RunAtLevel, levelName, 'MtM', dependencyDirectory)
        if len(accrualPortfolios) != 0: 
            newQF = "PLE_SystemPLAccrual" + fileNameConventions[RunAtLevel] + levelName
            taskName = newQF + taskNameSuffixConvention[pl_type]
            createNewQueryFolder(masterQF, newQF)
            for portfolio in accrualPortfolios:
                queryFolderUpdate(newQF, portfolio, 'Portfolio')
            commitChangesToQueryFolder(newQF)
            createSystemPLETasks('SystemPL', newQF, posSpec, context, module, taskName, default_outputDirectory, newQF, 'SystemPL_Accrual', None)
            createSystemPlParsingTasks('CancelDeals', newQF, None, None, context, cancelledPL_script, default_outputDirectory, RunAtLevel, levelName, 'Accrual', dependencyDirectory)
    elif pl_type == 'HigherOrder':
        if len(LevelPortfolios) != 0:
            primaryNewQF = "PLE_HO_SOB" + fileNameConventions[RunAtLevel] + levelName
            secondaryNewQF = "PLE_HO_2_SOB" + fileNameConventions[RunAtLevel] + levelName
            systemPL_newQF = "PLE_SystemPL" + fileNameConventions[RunAtLevel] + levelName
            cancelPL_newQF = "PLE_CancelPL" + fileNameConventions[RunAtLevel] + levelName
            taskName = primaryNewQF + taskNameSuffixConvention[pl_type]
            createNewQueryFolder(masterQF, primaryNewQF)
            createNewQueryFolder(secondaryMasterQF, secondaryNewQF)
            for portfolio in LevelPortfolios:
                queryFolderUpdate(primaryNewQF, portfolio, 'Portfolio')
                queryFolderUpdate(secondaryNewQF, portfolio, 'Portfolio')
            commitChangesToQueryFolder(primaryNewQF)
            commitChangesToQueryFolder(secondaryNewQF)
            queryList = primaryNewQF+','+secondaryNewQF
            createSystemPLETasks('HigherOrder', primaryNewQF, posSpec, context, module, taskName, default_outputDirectory, primaryNewQF, 'MtM', str(queryList))
            createSystemPlParsingTasks('HigherOrder', primaryNewQF, systemPL_newQF, cancelPL_newQF, context, priceAttributeParse_script, default_outputDirectory, RunAtLevel, levelName, 'MtM', dependencyDirectory)
        if len(accrualPortfolios) != 0:
            primaryNewQF = "PLE_HO_SOB_Accrual" + fileNameConventions[RunAtLevel] + levelName
            secondaryNewQF = "PLE_HO_2_SOB_Accrual" + fileNameConventions[RunAtLevel] + levelName
            systemPLAccrual_newQF = "PLE_SystemPLAccrual" + fileNameConventions[RunAtLevel] + levelName
            cancelPLAccrual_newQF = "PLE_CancelPL_Accrual" + fileNameConventions[RunAtLevel] + levelName
            taskName = primaryNewQF + taskNameSuffixConvention[pl_type]
            createNewQueryFolder(masterQF, primaryNewQF)
            createNewQueryFolder(secondaryMasterQF, secondaryNewQF)
            for portfolio in accrualPortfolios:
                queryFolderUpdate(primaryNewQF, portfolio, 'Portfolio')
                queryFolderUpdate(secondaryNewQF, portfolio, 'Portfolio')
            commitChangesToQueryFolder(primaryNewQF)
            commitChangesToQueryFolder(secondaryNewQF)
            queryList = primaryNewQF+','+secondaryNewQF
            createSystemPLETasks('HigherOrder', primaryNewQF, posSpec, context, module, taskName, default_outputDirectory, primaryNewQF, 'Accrual', str(queryList))
            createSystemPlParsingTasks('HigherOrder', primaryNewQF, systemPLAccrual_newQF, cancelPLAccrual_newQF, context, priceAttributeParse_script, default_outputDirectory, RunAtLevel, levelName, 'Accrual', dependencyDirectory)
      

def _CreateSystemPLQueryFoldersAndTasks(RunAtLevel, level, posSpec, default_outputDirectory, dependencyDirectory):
    CreateSystemPLQueryFoldersAndTasks(RunAtLevel, level, 'Aggregate', queryFolderMappings["Aggregate"], None, posSpec, default_outputDirectory, dependencyDirectory)
    CreateSystemPLQueryFoldersAndTasks(RunAtLevel, level, 'Funding', queryFolderMappings["Funding"], None, posSpec, default_outputDirectory, dependencyDirectory)
    CreateSystemPLQueryFoldersAndTasks(RunAtLevel, level, 'NewTrades', queryFolderMappings["NewTrades"], None, posSpec, default_outputDirectory, dependencyDirectory)
    CreateSystemPLQueryFoldersAndTasks(RunAtLevel, level, 'Amendment', queryFolderMappings["Amendment"], None, posSpec, default_outputDirectory, dependencyDirectory)
    CreateSystemPLQueryFoldersAndTasks(RunAtLevel, level, 'SystemPL', queryFolderMappings["SystemPL"], None, posSpec, default_outputDirectory, dependencyDirectory)
    CreateSystemPLQueryFoldersAndTasks(RunAtLevel, level, 'SourcePL', queryFolderMappings["SystemPL"], None, posSpec, default_outputDirectory, dependencyDirectory)
    CreateSystemPLQueryFoldersAndTasks(RunAtLevel, level, 'HigherOrder', queryFolderMappings["HigherOrder"], queryFolderMappings["HigherOrder_Voids"], posSpec, default_outputDirectory, dependencyDirectory)
  
            
            
"""---------------------------------------------------------------------------------------------"""

absa_fa_physicalPortfolios = getPLeligiblePorfolioList()  
absa_fa_majorDesks = sorted(getMajorDesk())
absa_fa_minorDesks = sorted(getMinorDesk())
absa_fa_masterBooks = sorted(getMasterBooks())
positionSpecs = acm.FPositionSpecification.Select('')
trueAndFalseSelectionList = [True, False] 
outputDirectory = "/services/frontnt/Task/PNL"
dependencyDirectory = '/apps/frontnt/REPORTS/BackOffice/MarketRisk/FrontArena/PLExplain' 
        
ael_gui_parameters = {'hideExtracControls': True,
                      'windowCaption': 'PL Explain System PL Tasks Load Balancer'}

ael_variables = [ ['ABSA_MajorDesks', 'Major Desk', 'string', absa_fa_majorDesks, None, 0],
                  ['ABSA_MinorDesks', 'Minor Desk', 'string', absa_fa_minorDesks, None, 0],
                  ['ABSA_MasterBooks', 'Masterbook', 'string', absa_fa_masterBooks, None, 0],
                  ['ABSA_PhysicalPortfolios', 'Physical Portfolio', 'string', absa_fa_physicalPortfolios, None, 0],
                  ['ABSA_PositionSpecs', 'Position Specifications', 'string', positionSpecs, posSpecDefault, 0],
                  ['outputPath', 'Output Path', 'string', None, outputDirectory, 0],
                  ['dependencyTask_inputPath', 'Dependency Task Input Path', 'string', None, dependencyDirectory, 0],
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
    default_outputDirectory = ael_dict['outputPath']
    default_dependencyDirectory = ael_dict['dependencyTask_inputPath']  
    runAtMajorDeskLevel = ael_dict['runAtMajorDeskLevel']
    runAtMinorDeskLevel = ael_dict['runAtMinorDeskLevel']  
    runAtMasterBookLevel = ael_dict['runAtMasterBookLevel']
    runAtPortfolioLevel = ael_dict['runAtPortfolioLevel']
    print("********Running PL Explain System PL Task & Queries Setups***************", _nowTime())
    start_time= time.time()
    if runAtMajorDeskLevel == 'true':
        print("Run at Major Desk Level is ticked")
        if ABSA_MajorDesks:
            majorDesk = str(ABSA_MajorDesks)
            _CreateSystemPLQueryFoldersAndTasks('MajorDesk', majorDesk, posSpec, default_outputDirectory, default_dependencyDirectory)
    elif runAtMinorDeskLevel == 'true':
        print("Run at Minor Desk Level is ticked")
        if ABSA_MinorDesks:
            minorDesk = str(ABSA_MinorDesks)
            _CreateSystemPLQueryFoldersAndTasks('MinorDesk', minorDesk, posSpec, default_outputDirectory, default_dependencyDirectory)
    elif runAtMasterBookLevel == 'true':
        print("Run at Masterbook Level is ticked")
        if ABSA_MasterBooks:
            masterBook = str(ABSA_MasterBooks)
            _CreateSystemPLQueryFoldersAndTasks('Masterbook', masterBook, posSpec, default_outputDirectory, default_dependencyDirectory)
    elif runAtPortfolioLevel == 'true':
        print("Run at Portfolio Level is ticked")
        if ABSA_PhysicalPortfolios:
            portSelection = acm.FPhysicalPortfolio.Select('name = %s' %ABSA_PhysicalPortfolios)
            if len(portSelection) == 1:
                runPortfolio = portSelection[0].Name()
                _CreateSystemPLQueryFoldersAndTasks('Portfolio', runPortfolio, posSpec, default_outputDirectory, default_dependencyDirectory)
    elif runAtMajorDeskLevel == 'false':
        print("Run at Major Desk Level is unticked")
    elif runAtMinorDeskLevel == 'false':
        print("Run at Minor Desk Level is unticked")
    elif runAtMasterBookLevel == 'false':
        print("Run at Masterbook Level is unticked")
    elif runAtPortfolioLevel == 'false':
        print("Run at Portfolio Level is unticked")
    print("********Finished PL Explain System PL Task & Queries Setups***************", _nowTime())
    end_time = time.time()
    duration = end_time - start_time
    print("Total Batch Run Time Duration:", _convertTimeInSecondsToHoursMinutesSeconds(duration))
    






