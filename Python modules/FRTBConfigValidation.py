"""--------------------------------------------------------------------
MODULE:         FRTBConfigValidation
    
DESCRIPTION:    This module contains a ael task that checks all FRTB configurations.:

                Checks Include:
                
                1. Risk Factor Additional Data Mapping Check (i.e. For SA - SA Bucket; For IMA - IMA Category, External ID, Moddelablity Flag, Include in Reduced Flag.),
                2. Risk Factor Completeness Check (i.e. was all risk factors in a ThVal calculation mapped to a spesified risk factor setup),
                3. Scenario file/IMA Risk Factor Mapping Comparison.
                
                #ADD LOGIC TO CHECK PORTFOLIOS IN SCOPE + Output a report 
                
History:        Created - Nicolaas Duvenage 2019-10-29
    
--------------------------------------------------------------------"""
import acm
import RiskFactorIdentification
import RiskFactorUtils
import FRunScriptGUI
import FLogger
import logging
import itertools
import inspect
import csv
import os
import platform
import time
import datetime
"""
Global Functions
"""
def __getLoggerKwArgsFromAelParams(ael_params):
    # workaround for bug in FLogger which duplicates logging
    log_file    = ael_params['Logfile']
    logger_kwargs = {
        'level': int(ael_params['Logmode']),
        'logToConsole': int(ael_params['LogToConsole']) == 1,
        'logToPrime': False,
        'keep': False,
        'logOnce': False,
        'logToFileAtSpecifiedPath' : str(log_file)
    }
    return logger_kwargs
    
def createDefaultLogger(name, ael_params):
    kwargs = __getLoggerKwArgsFromAelParams(ael_params)
    logger = FLogger.FLogger.LOGGERS.get(name)
    if logger:
        logger.Reinitialize(**kwargs)
    else:
        logger = FLogger.FLogger(name=name, **kwargs)

    log_formatter = logging.Formatter('%(asctime)s %(message)s', '%Y-%m-%d %H:%M:%S')
    for handler in logger.Handlers():
        handler.setFormatter(log_formatter)
    return logger

def getCaller():
    # Returns the caller of the caller of this method
    # (hence 3rd element in stack)
    frame = inspect.stack()[2]
    return inspect.getmodule(frame[0])

def getInputFileSelector():
    types = ('CSV Files (*.csv)|*.csv')
    return FRunScriptGUI.InputFileSelection(types)

def getOutputFileSelector():
    types = ('All Files (*.*)|*.*||')
    return FRunScriptGUI.OutputFileSelection(types)

def getBucketsAndRiskClasses(hierarchy):
    riskClassAndBuckets = {}
    nodes = hierarchy.HierarchyNodes()
    #Get all SA Buckets and Risk Classes
    if hierarchy.HierarchyType().Name() == 'FRTB SA Data Type':
        for node in nodes:
            nodeDataValues      = node.HierarchyDataValues().AsString()
            if ('Bucket' in nodeDataValues) == True and ('Time Bucket' in nodeDataValues) == False:
                bucket             = node.DisplayName()
                bucketParentNodeID = node.ParentId()
                parentNode         = acm.FHierarchyNode[bucketParentNodeID]
                parnentNodeDVs     = parentNode.HierarchyDataValues().AsString()

                if ('Risk Class' in parnentNodeDVs) == True:
                    riskClassName = parentNode.DisplayName()
                elif ('Subtype' in parnentNodeDVs) == True:
                    subtypeParentNodeID = parentNode.ParentId()
                    parentNode          = acm.FHierarchyNode[subtypeParentNodeID]
                    parnentNodeDVs      = parentNode.HierarchyDataValues().AsString()
            
                    if ('Risk Class' in parnentNodeDVs) == True:
                        riskClassName = parentNode.DisplayName()
                if not riskClassName in riskClassAndBuckets:
                    riskClassAndBuckets[riskClassName] = []
                    
                if not bucket in riskClassAndBuckets[riskClassName]:
                    riskClassAndBuckets[riskClassName].append(bucket)
                        
    #Get all IMA Categories and Risk Classes
    elif hierarchy.HierarchyType().Name() == 'FRTB IMA Data Type':
        for node in nodes:
            nodeDataValues = node.HierarchyDataValues().AsString()
            if ('Risk Factor Category' in nodeDataValues) == True:
                category             = node.DisplayName()
                categoryParentNodeID = node.ParentId()
                parentNode           = acm.FHierarchyNode[categoryParentNodeID]
                parnentNodeDVs       = parentNode.HierarchyDataValues().AsString()
                if ('Risk Class' in parnentNodeDVs) == True:
                    riskClassName = parentNode.DisplayName()
                    
                if not riskClassName in riskClassAndBuckets:
                    riskClassAndBuckets[riskClassName] = []
                    
                if not category in riskClassAndBuckets[riskClassName]:
                    riskClassAndBuckets[riskClassName].append(category)
    return riskClassAndBuckets
    
def addCSVExternalIdToList(csvScenarioFile):
    with open(str(csvScenarioFile)) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        lineCount = 0
        list      = []
        for row in csvReader:
            if lineCount == 0:
                lineCount += 1
            else:
                scenExternalId = row[0]
                lineCount += 1
                if not scenExternalId in list and scenExternalId != '':
                    list.append(scenExternalId)
    return list

"""
Config Validation Class
"""
def riskFactorDataMappingCheck(logger, riskfactorSetup, hierarchy, OutputDir, Extension, filePrefix, DateDir):
    isSARiskFactorSetup = True if ('FRTB SA Risk Class' in riskfactorSetup.RiskFactorPropertySpecifications().AsString()) else False
    isSAHierarchy       = True if (hierarchy.HierarchyType().Name() == 'FRTB SA Data Type') else False
    riskClassAndBuckets = getBucketsAndRiskClasses(hierarchy)
    collections         = riskfactorSetup.RiskFactorCollections()
    if isSARiskFactorSetup == True:
        calc_Type = 'SA'
    else:     
        calc_Type = 'IMA'

    if "Windows" in platform.platform():
        OutputFile    = str(OutputDir) + "\\" + filePrefix + "_" + "RiskFactorCompletnessCheck" + Extension
        print(OutputFile)
    elif "Linux" in platform.platform():
        OutputFile    = str(OutputDir) + "/" + filePrefix + "_" + "RiskFactorCompletnessCheck" + Extension
        print(OutputFile)
    
    saheaders     = '%s,%s,%s,%s,%s,%s,%s\n'%('Risk Factor Setup', 'Hierarchy', 'Risk Factor Collection', 'Risk Class', 'Risk Factor', 'Bucket', 'Comment')
    imaheaders    = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%('Risk Factor Setup', 'Hierarchy', 'Risk Factor Collection', 'Risk Class', 'Risk Factor', 'External Id', 'Include In Reduced', 'Modellable', 'FRTB IMA Category', 'Comment')
    if isSARiskFactorSetup != isSAHierarchy:
        #Check that Risk Factor Setup and Hierarchy Data types are consistant.
        logger.error('Data types differ for Risk Factor Setup and Hierarchy.')
        logger.error('Risk Factor Mapping Data Check will be ignored for: %s.\n'%(riskfactorSetup.Name()))
    else:
        #Check SA and IMA Risk Factor independently to catch SA FX Risk Class criteria exception (i.e. Other Currencies).
        if isSARiskFactorSetup == True:
            logger.info('Enter SA Data Check for: %s.\n'%(riskfactorSetup.Name()))
            file    = open(OutputFile, "w")
            file.write(saheaders)
            file.close()
            for collection in collections:
                logger.info('Starting Check For Collection: %s.'%(collection.DisplayName()))
                saRiskClass  = collection.AddInfoValue('FRTB SA Risk Class')
                rfInstances  = collection.RiskFactorInstances()
                for riskFactor in rfInstances:
                    saBucket      = riskFactor.AddInfoValue('FRTB SA Bucket')
                    riskFactorName= riskFactor.StringKey()
                    if saBucket == None:
                        logger.error('Risk Factor *%s* missing SA Bucket'%riskFactor.RiskFactorCoordinates())
                        file    = open(OutputFile, "a")
                        file.write('%s,%s,%s,%s,%s,%s,%s\n'%(riskfactorSetup.Name(), hierarchy.Name(), collection.DisplayName(), saRiskClass, riskFactorName, saBucket, 'Missing SA Bucket'))
                        file.close()
                    elif (saBucket not in riskClassAndBuckets[saRiskClass]) and saRiskClass == 'GIRR':
                        currency = acm.FCurrency[saBucket]
                        if not currency:
                            logger.error('Risk Factor *%s* has a invalid SA Bucket mapping: %s'%(riskFactor.RiskFactorCoordinates(), saBucket))
                            file    = open(OutputFile, "a")
                            file.write('%s,%s,%s,%s,%s,%s,%s\n'%(riskfactorSetup.Name(), hierarchy.Name(), collection.DisplayName(), saRiskClass, riskFactorName, saBucket, 'Invalid SA Bucket'))
                            file.close()
                    elif (saBucket not in riskClassAndBuckets[saRiskClass]) and saRiskClass != 'GIRR':
                        logger.error('Risk Factor *%s* has a invalid SA Bucket mapping: %s'%(riskFactor.RiskFactorCoordinates(), saBucket))
                        file    = open(OutputFile, "a")
                        file.write('%s,%s,%s,%s,%s,%s,%s\n'%(riskfactorSetup.Name(), hierarchy.Name(), collection.DisplayName(), saRiskClass, riskFactorName, saBucket, 'Invalid SA Bucket'))
                        file.close()
                logger.info('Finished Check For Collection: %s.\n'%(collection.DisplayName()))
            logger.info('Finished SA Data Check for: %s.\n'%(riskfactorSetup.Name()))
        elif isSARiskFactorSetup == False:
            logger.info('Enter IMA Data Check for: %s.'%(riskfactorSetup.Name()))
            file    = open(OutputFile, "w")
            file.write(imaheaders)
            file.close()
            for collection in collections:
                logger.info('Starting Check For Collection: %s.'%(collection.DisplayName()))
                imaRiskClass = collection.AddInfoValue('FRTB IMA Risk Class')
                rfInstances  = collection.RiskFactorInstances()
                for riskFactor in rfInstances:
                    imaCategory   = riskFactor.AddInfoValue('FRTB IMA Category')
                    imaExternalID = riskFactor.AddInfoValue('External Id')
                    imaReduced    = riskFactor.AddInfoValue('Include In Reduced')
                    imaModellable = riskFactor.AddInfoValue('Modellable')
                    riskFactorName= riskFactor.StringKey()
                    if imaCategory == None or imaExternalID == None or imaReduced == None or imaModellable == None:
                        logger.error('Risk Factor *%s* missing IMA mapping'%riskFactor.RiskFactorCoordinates())
                        file    = open(OutputFile, "a")
                        file.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(riskfactorSetup.Name(), hierarchy.Name(), collection.DisplayName(), imaRiskClass, riskFactorName, imaExternalID, imaReduced, imaModellable, imaCategory, 'Missing IMA Data'))
                        file.close()
                    elif (imaCategory not in riskClassAndBuckets[imaRiskClass]):
                        logger.error('Risk Factor *%s* has a invalid IMA Bucket mapping: %s'%(riskFactor.RiskFactorCoordinates(), imaCategory))
                        file    = open(OutputFile, "a")
                        file.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(riskfactorSetup.Name(), hierarchy.Name(), collection.DisplayName(), imaRiskClass, riskFactorName, imaExternalID, imaReduced, imaModellable, imaCategory, 'Invalid IMA Category'))
                        file.close()
                logger.info('Finished Check For Collection: %s.\n'%(collection.DisplayName()))       
            logger.info('Finished IMA Data Check for: %s.\n'%(riskfactorSetup.Name()))
    

def riskFactorCompletenessCheck(logger, riskFactorSetup, tradeQueries, OutputDir, Extension, filePrefix, DateDir):
    isSARiskFactorSetup = True if ('FRTB SA Risk Class' in riskFactorSetup.RiskFactorPropertySpecifications().AsString()) else False
    identifier          = RiskFactorIdentification.RiskFactorIdentifier()
    collections         = riskFactorSetup.RiskFactorCollections()
    headers             = '%s,%s,%s,%s\n'%('Risk Factor Setup', 'Collection', 'Risk Factor Instance', 'Comment')
    instruments         = []
    identifiedKeys      = {}
    existingKeys        = []
    if isSARiskFactorSetup == True:
        calc_Type = 'SA'
    else:     
        calc_Type = 'IMA'
    if "Windows" in platform.platform():
        OutputFile    = str(OutputDir) + "\\" + filePrefix + "_" + "RiskFactorCompletnessCheck" + Extension
        print(OutputFile)
    elif "Linux" in platform.platform():
        OutputFile    = str(OutputDir) + "/" + filePrefix + "_" + "RiskFactorCompletnessCheck" + Extension
        print(OutputFile)
    try:
        file    = open(OutputFile, "w")
        file.write(headers)
        file.close()
    except Exception as e:
        print(e)
        
    for tradeQuery in tradeQueries:
        trades = tradeQuery.Query().Select()
        for trade in trades:
            if not trade.Instrument() in instruments:
                instruments.append(trade.Instrument())

    #Get all Risk Factor Keys in Theoretical Value
    logger.info('Retrieving all risk factor in Theoretical Value for: %s.\n'%(tradeQueries))
    for collection in collections:
        logger.info('Starting retrieval for collection: %s.'%(collection.DisplayName()))
        #This is to computationally heavy step
        newRfsInCollection = identifier.DetectRiskFactors(collection, instruments)
        if not collection.DisplayName() in identifiedKeys:
            identifiedKeys[collection.DisplayName()] = []
            
        for riskFactor in newRfsInCollection:
            rfKey = RiskFactorUtils.GetRiskFactorInstanceKeyFromDict(collection, riskFactor)
            if rfKey not in identifiedKeys[collection.DisplayName()]:
                identifiedKeys[collection.DisplayName()].append(rfKey)
            
        logger.info('Finished retrieval for collection: %s.\n'%(collection.DisplayName()))
    
    #Get all mapped Risk Factor Keys
    logger.info('Retrieving all mapped risk factors for Risk Factor Setup: %s.\n'%(riskFactorSetup.Name()))
    for collection in collections:
        logger.info('Starting retrieval for collection: %s.'%(collection.DisplayName()))
        rfInstances = collection.RiskFactorInstances()
        for mappedRiskFactor in rfInstances:
            if mappedRiskFactor not in existingKeys:
                existingKeys.append(RiskFactorUtils.GetRiskFactorInstanceKey(mappedRiskFactor))
        
        logger.info('Finished retrieval for collection: %s.\n'%(collection.DisplayName()))

    #Get all mapped Risk Factor Keys
    logger.info('Identifying missing risk factors in risk factor setup: %s.\n'%(riskFactorSetup.Name()))
    for collectionName in identifiedKeys:
        for idenRf in identifiedKeys[collectionName]:
            if idenRf not in existingKeys:
                try:
                    file    = open(OutputFile, "a")
                    file.write('%s,%s,%s,%s\n'%(riskFactorSetup.Name(), collectionName, idenRf, 'Risk Factor Instance not mapped to collection'))
                    logger.error('Missing Risk Factor for %s Collection: %s'%(collectionName, idenRf))
                    file.close()
                except Exception as e:
                    print(e)
                
    logger.info('Finished Comparison for risk factor setup: %s.\n'%(riskFactorSetup.Name()))

   
def scenarioFileCheck(logger, riskfactorSetup, esfcScenarioFile, esrsScenarioFile, plScenarioFile, nmrfScenarioFile, OutputDir, Extension, filePrefix, DateDir):
    isSARiskFactorSetup = True if ('FRTB SA Risk Class' in riskfactorSetup.RiskFactorPropertySpecifications().AsString()) else False
    collections         = riskfactorSetup.RiskFactorCollections()
    externalIDsInRFSetup= []
    countRiskFactorIds  = 0
    countScenFileIds    = 0
    countMissing        = 0
    headers             = '%s,%s,%s,%s\n'%('Risk Factor Setup', 'Risk Factor ID (External ID)', 'Scenario File Name', 'Comment')
    if isSARiskFactorSetup == True:
        calc_Type = 'SA'
    else:     
        calc_Type = 'IMA'
    
    if isSARiskFactorSetup == True:
        logger.error('SA Risk Factor Setup Selected.')
        logger.error('Scenario File check will be ignored for: %s.\n'%(riskfactorSetup.Name()))
    elif isSARiskFactorSetup == False:
        logger.info('Enter Scenario File Comparison for: %s.\n'%(riskfactorSetup.Name()))
        scenfilecCheckOutputFile    = str(OutputDir) + "\\" + filePrefix + "_" + "RiskFactorMissingInScenFile" + Extension
        rfSetupCheckOutputFile      = str(OutputDir) + "\\" + filePrefix + "_" + "RiskFactorMissingInFAMapping" + Extension
        if "Windows" in platform.platform():
            scenfilecCheckOutputFile    = str(OutputDir) + "\\" + filePrefix + "_" + "RiskFactorMissingInScenFile" + Extension
            print(scenfilecCheckOutputFile)
            rfSetupCheckOutputFile      = str(OutputDir) + "\\" + filePrefix + "_" + "RiskFactorMissingInFAMapping" + Extension
            print(OutpurfSetupCheckOutputFiletFile)
        elif "Linux" in platform.platform():
            scenfilecCheckOutputFile    = str(OutputDir) + "/" + filePrefix + "_" + "RiskFactorMissingInScenFile" + Extension
            print(scenfilecCheckOutputFile)
            rfSetupCheckOutputFile      = str(OutputDir) + "/" + filePrefix + "_" + "RiskFactorMissingInFAMapping" + Extension
            print(OutpurfSetupCheckOutputFiletFile)
        
        file    = open(scenfilecCheckOutputFile, "w")
        file.write(headers)
        file.close()
        file    = open(rfSetupCheckOutputFile, "w")
        file.write(headers)
        file.close()
        #Add all Risk Factors External IDs in Setup to a List
        for collection in collections:
            imaRiskClass = collection.AddInfoValue('FRTB IMA Risk Class')
            rfInstances  = collection.RiskFactorInstances()
            for riskFactor in rfInstances:
                imaExternalID = riskFactor.AddInfoValue('External Id')
                if not imaExternalID in externalIDsInRFSetup:
                    countRiskFactorIds+=1
                    externalIDsInRFSetup.append(imaExternalID)    
        #Add all ES Scenario File ID's to a List
        externalIDsInESFCFile = addCSVExternalIdToList(esfcScenarioFile)
        esfcScenarioFileName  = str(esfcScenarioFile).split("\\")[-1]
        externalIDsInESRSFile = addCSVExternalIdToList(esrsScenarioFile)
        esrsScenarioFileName  = str(esrsScenarioFile).split("\\")[-1]
        externalIDsInPLFile   = addCSVExternalIdToList(plScenarioFile)
        plScenarioFileName    = str(plScenarioFile).split("\\")[-1]
        externalIDsInNMFile   = addCSVExternalIdToList(nmrfScenarioFile)
        nmrfScenarioFileName  = str(nmrfScenarioFile).split("\\")[-1]
        #Check ESFC Risk Factor ID's
        logger.info('Comparing ESFC Risk Factor IDs for: %s.'%(riskfactorSetup.Name()))
        for id in externalIDsInESFCFile:
            if not id in externalIDsInRFSetup:
                file    = open(rfSetupCheckOutputFile, "a")
                file.write('%s,%s,%s,%s\n'%(riskfactorSetup.Name(), id, esfcScenarioFileName, 'Missing in IMA Risk Factor Setup'))
                file.close()
                
        for id in externalIDsInRFSetup:
            if not id in externalIDsInESFCFile:
                file    = open(scenfilecCheckOutputFile, "a")
                file.write('%s,%s,%s,%s\n'%(riskfactorSetup.Name(), id, esfcScenarioFileName, 'Missing in IMA ESFC Scenario File'))
                file.close()
        logger.info('Finished Comparing ESFC Risk Factor IDs for: %s.\n'%(riskfactorSetup.Name()))
        #Check ESRS Risk Factor ID's
        logger.info('Comparing ESRS Risk Factor IDs for: %s.'%(riskfactorSetup.Name()))
        for id in externalIDsInESRSFile:
            if not id in externalIDsInRFSetup:
                file    = open(rfSetupCheckOutputFile, "a")
                file.write('%s,%s,%s,%s\n'%(riskfactorSetup.Name(), id, esrsScenarioFileName, 'Missing in IMA Risk Factor Setup'))
                file.close()
                
        for id in externalIDsInRFSetup:
            if not id in externalIDsInESRSFile:
                file    = open(scenfilecCheckOutputFile, "a")
                file.write('%s,%s,%s,%s\n'%(riskfactorSetup.Name(), id, esrsScenarioFileName, 'Missing in IMA ESRS Scenario File'))
                file.close()
        logger.info('Finished Comparing ESRS Risk Factor IDs for: %s.\n'%(riskfactorSetup.Name()))
        #Check PL Risk Factor ID's
        logger.info('Comparing PL Risk Factor IDs for: %s.'%(riskfactorSetup.Name()))
        for id in externalIDsInPLFile:
            if not id in externalIDsInRFSetup:
                file    = open(rfSetupCheckOutputFile, "a")
                file.write('%s,%s,%s,%s\n'%(riskfactorSetup.Name(), id, plScenarioFileName, 'Missing in IMA Risk Factor Setup'))
                file.close()
                
        for id in externalIDsInRFSetup:
            if not id in externalIDsInPLFile:
                file    = open(scenfilecCheckOutputFile, "a")
                file.write('%s,%s,%s,%s\n'%(riskfactorSetup.Name(), id, plScenarioFileName, 'Missing in IMA ES Scenario File'))
                file.close()
                
        logger.info('Finished Comparing PL Risk Factor IDs for: %s.\n'%(riskfactorSetup.Name()))
        #Check NMRF Risk Factor ID's
        logger.info('Comparing NMRF Risk Factor IDs for: %s.'%(riskfactorSetup.Name()))
        for id in externalIDsInNMFile:
            if not id in externalIDsInRFSetup:
                file    = open(rfSetupCheckOutputFile, "a")
                file.write('%s,%s,%s,%s\n'%(riskfactorSetup.Name(), id, nmrfScenarioFileName, 'Missing in IMA Risk Factor Setup'))
                file.close()
                
        for id in externalIDsInRFSetup:
            if not id in externalIDsInNMFile:
                file    = open(scenfilecCheckOutputFile, "a")
                file.write('%s,%s,%s,%s\n'%(riskfactorSetup.Name(), id, nmrfScenarioFileName, 'Missing in IMA ES Scenario File'))
                file.close()
                
        logger.info('Finished Comparing NMRF Risk Factor IDs for: %s.\n'%(riskfactorSetup.Name()))

"""
Define Ael Variables
"""
def getLoggingAelVariables(caller, log_filename):
    def logfile_cb(index, fieldValues):
        caller.ael_variables.Logfile.enable(
            fieldValues[index],
            'You have to check Log To File to be able to select a Logfile.'
        )
        return fieldValues

    logFileSelection = getOutputFileSelector()
    logFileSelection.SelectedFile = os.path.join('C:\\', 'temp', log_filename)
    ttLogMode = 'Defines the amount of logging produced.'
    ttLogToCon = (
        'Whether logging should be done in the Log Console or not.'
    )
    ttLogToFile = 'Defines whether logging should be done to file.'
    ttLogFile = (
        'Name of the logfile. Could include the whole path, c:\temp\...'
    )
    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        ['Logmode',
            'Logmode_Logging',
            'int', [1, 2, 3, 4], 1,
            1, 0, ttLogMode],
        ['LogToConsole',
            'Log to console_Logging',
            'int', [0, 1], 1,
            1, 0, ttLogToCon],
        ['LogToFile',
            'Log to file_Logging',
            'int', [0, 1], 0,
            1, 0, ttLogToFile, logfile_cb],
        ['Logfile',
            'Logfile_Logging',
            logFileSelection, None, logFileSelection,
            0, 1, ttLogFile, None, None],
    ]
    return ael_variables
    
def getOutputAelVariables():
    # tool tips
    ttOutputDir = (
        'Path to the directory where the reports should be '
        'created. Environment variables can be used for '
        'Windows (%VAR%) or Unix ($VAR).'
    )
    ttPrefix = 'Optional prefix for output file names.'
    ttExtension = 'Extension used for output file names.'
    ttDateDir = (
        'Create a directory with the todays date as the directory name'
    )
    ttOverwrite = (
        'If a file with the same name and path already exists, overwrite it.'
    )
    ttCalcType = (
        'Based on Calculation Type selection,'
        ' results will be stored in appropriate folder structure.'
    )
    directorySelection = FRunScriptGUI.DirectorySelection()
    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        ['OutputDir',
            'Directory path_Output settings',
            directorySelection, None, directorySelection,
            1, 1, ttOutputDir, None, 1],
        ['Extension',
            'Output file extension_Output settings',
            'string', None, '.csv',
            1, 0, ttExtension],
        ['outputPrefix',
            'Output file prefix_Output settings',
            'string', None, None,
            1, 0, ttPrefix],
        ['DateDir',
            'Create directory with todays date_Output settings',
            'int', [0, 1], 1,
            1, 0, ttDateDir]
    ]
    return ael_variables
    
def getTaskAelVariables(caller):
        
    def performMappingCheck(index, fieldValues):
        caller.ael_variables.rFSetup.enable(
        fieldValues[index],
        'You have to check "Perform  risk factor mapping check" to be able to select a Risk Factor Setup.'
        )
        caller.ael_variables.hierarchy.enable(
        fieldValues[index],
        'You have to check "Perform  risk factor mapping check" to be able to select a Hierarchy.'
        )
        return fieldValues
        
        
    def performCompletenessCheck(index, fieldValues):
        caller.ael_variables.rfSetupComp.enable(
        fieldValues[index],
        'You have to check "Perform Risk Factor Completeness Check" to be able to select a Risk Factor Setup.'
        )
        caller.ael_variables.tradeQueries.enable(
        fieldValues[index],
        'You have to check "Perform Risk Factor Completeness Check" to be able to select a Trade Queries.'
        )
        return fieldValues
        
    def performScenarioCheck(index, fieldValues):
        caller.ael_variables.imaRFSetup.enable(
        fieldValues[index],
        'You have to check "Perform Scenario File Check" to be able to select a IMA Risk Factor Setup.'
        )
        caller.ael_variables.esfcScenarioFile.enable(
        fieldValues[index],
        'You have to check "Perform Scenario File Check" to be able to select a Scenario File.'
        )
        caller.ael_variables.esrsScenarioFile.enable(
        fieldValues[index],
        'You have to check "Perform Scenario File Check" to be able to select a Scenario File.'
        )
        caller.ael_variables.plScenarioFile.enable(
        fieldValues[index],
        'You have to check "Perform Scenario File Check" to be able to select a Scenario File.'
        )
        caller.ael_variables.nmrfScenarioFile.enable(
        fieldValues[index],
        'You have to check "Perform Scenario File Check" to be able to select a Scenario File.'
        )
        return fieldValues
        
    scenFileSelection    = getInputFileSelector()
    default              = ['ABSA', 'FRTB SA Risk Factors', 'FRTB SA Static Data', 'VaR Risk Factors']
    directorySelection   = FRunScriptGUI.DirectorySelection()
    tradeQueries         = acm.FStoredASQLQuery.Select('user=0 and subType="FTrade"')
    ttHierarchy          = 'Select a hierarchy containing static risk factor data.'
    ttRFSetup            = 'Select a risk factor setup.'
    ttImaRFSetup         = 'Select a IMA risk factor setup.'
    ttCompoundPort       = 'Select a compound portfolio to check.'
    ttPerformDesk        = 'Perform Desk and Portfolio Owner Check'
    ttPerformMappingCheck= 'Perform Mapping validation.'
    ttRFCompare          = 'Perform Risk Factor Comparison.'
    ttPerformComp        = 'Perform Risk Factor Completeness Check.'
    ttPortfolios         = 'The physical portfolios to which the trades belong.'
    ttTradeFilters       = 'The selection of trade filters.'
    ttTradeQueries       = 'The stored ASQL queries, queries shown are shared and of type trade.'
    ttScenarioFile       = 'Select a Scenaio File.'
    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        ['performMappingCheck',
            'Perform risk factor mapping check_Risk Factor Static Data',
            'int', [0, 1], 0,
            1, 0, ttPerformMappingCheck, performMappingCheck],
        ['rFSetup',
            'Risk Factor Setup_Risk Factor Static Data',
            'FRiskFactorSetup', acm.FRiskFactorSetup.Select(''), default[1],
            0, 0, ttRFSetup, None, None],
        ['hierarchy', 
            'Hierarchy Setup_Risk Factor Static Data',
            'FHierarchy', acm.FHierarchy.Select(''), default[2],
            0, 0, ttHierarchy, None, None],
        ['performCompletenessCheck',
            'Perform Risk Factor Completeness Check_Risk Factor Setup Completeness',
            'int', [0, 1], 0,
            1, 0, ttPerformComp, performCompletenessCheck],
        ['rfSetupComp',
            'Risk Factor Setup_Risk Factor Setup Completeness',
            'FRiskFactorSetup', acm.FRiskFactorSetup.Select(''), default[1],
            0, 0, ttRFSetup, None, None],
        ['tradeQueries',
            'Trade queries_Risk Factor Setup Completeness',
            acm.FStoredASQLQuery, tradeQueries, None,
            0, 1, ttTradeQueries],
        ['performScenarioCheck',
            'Perform Scenario File Check_Scenario File Completeness',
            'int', [0, 1], 0,
            1, 0, ttRFCompare, performScenarioCheck],   
        ['imaRFSetup',
            'IMA Risk Factor Setup_Scenario File Completeness',
            'FRiskFactorSetup', acm.FRiskFactorSetup.Select(''), default[3],
            0, 0, ttImaRFSetup, None, None],
        ['esfcScenarioFile',
            'ESFC Scenario File_Scenario File Completeness',
            scenFileSelection, None, scenFileSelection,
            0, 1, ttScenarioFile, None, True],
        ['esrsScenarioFile',
            'ESRS Scenario File_Scenario File Completeness',
            scenFileSelection, None, scenFileSelection,
            0, 1, ttScenarioFile, None, True],
        ['plScenarioFile',
            'Risk P&L Scenario File_Scenario File Completeness',
            scenFileSelection, None, scenFileSelection,
            0, 1, ttScenarioFile, None, True],
        ['nmrfScenarioFile',
            'NMRF Scenario File_Scenario File Completeness',
            scenFileSelection, None, scenFileSelection,
            0, 1, ttScenarioFile, None, True]
    ]
    return ael_variables
    
    
def createAelVariables(ael_vars_list, log_filename):
    caller = getCaller()
    ael_vars_list.extend(getTaskAelVariables(
        caller=caller
    ))
    ael_vars_list.extend(getOutputAelVariables(
    ))
    ael_vars_list.extend(getLoggingAelVariables(
        caller=caller, log_filename=log_filename
    ))
    ael_vars = FRunScriptGUI.AelVariablesHandler(
        ael_vars_list, caller.__name__
    )
    return ael_vars
    
log_name           = 'FRTBConfigValidation'
ael_variables      = createAelVariables([], log_name)

def ael_main(ael_output):
    start_time = time.time()
    print ('STARTED ' + str(datetime.datetime.now()))
    logger                      = createDefaultLogger(log_name, ael_output)
    performMappingCheck         = ael_output['performMappingCheck']
    rFSetup                     = ael_output['rFSetup']
    hierarchy                   = ael_output['hierarchy']
    performCompletenessCheck    = ael_output['performCompletenessCheck']
    rfSetupComp                 = ael_output['rfSetupComp']
    tradeQueries                = ael_output['tradeQueries']
    performScenarioCheck        = ael_output['performScenarioCheck']
    imaRFSetup                  = ael_output['imaRFSetup']
    esfcScenarioFile            = ael_output['esfcScenarioFile']
    esrsScenarioFile            = ael_output['esrsScenarioFile']
    plScenarioFile              = ael_output['plScenarioFile']
    nmrfScenarioFile            = ael_output['nmrfScenarioFile']
    filePrefix                  = ael_output['outputPrefix']
    OutputDir                   = ael_output['OutputDir']
    Extension                   = ael_output['Extension']
    DateDir                     = ael_output['DateDir']
    logger.info('FRTB Config Checker Starting\n' + '-'*100)
    #Add Logic for Desk Check and Portfolios in scope
    #Check 1: Risk Factor Mapping Data Check
    if performMappingCheck == 1:
        logger.info('Starting Risk Factor Mapping Data Check\n')
        riskFactorDataMappingCheck(logger, rFSetup, hierarchy, OutputDir, Extension, filePrefix, DateDir)
        logger.info('Finished Risk Factor Mapping Data Check.\n' + '-'*100)
    #Check 2: Risk Factor Completeness Check
    if performCompletenessCheck == 1:
        logger.info('Starting Risk Factor Completeness Check\n')
        riskFactorCompletenessCheck(logger, rfSetupComp, tradeQueries, OutputDir, Extension, filePrefix, DateDir)
        logger.info('Finished Risk Factor Completeness Check.\n'+ '-'*100)
    #Check 3: Scenario file/IMA Risk Factor Mapping Comparison - Scenario File VS Risk Factor Setup
    if performScenarioCheck == 1:
        logger.info('Starting Scenario File Check\n')
        scenarioFileCheck(logger, imaRFSetup, esfcScenarioFile, esrsScenarioFile, plScenarioFile, nmrfScenarioFile, OutputDir, Extension, filePrefix, DateDir)
        logger.info('Finished Scenario File Check.\n' + '-'*100)
    end_time = time.time()
    print ('Execution time (hh:mm:ss): ' + str(datetime.timedelta(seconds=end_time - start_time)))
    print ('FINISHED ' + str(datetime.datetime.now()))
    print ('Total Clock-Time: ' + str(datetime.timedelta(seconds=time.clock())))
