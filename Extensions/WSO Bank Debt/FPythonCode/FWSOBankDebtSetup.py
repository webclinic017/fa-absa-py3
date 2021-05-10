""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOBankDebtSetup.py"
"""--------------------------------------------------------------------------
MODULE
    FWSOBankDebtSetup

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    WSO Bank Debt setup script. This script needs only be run once, unless a new 
    ADS is used or an old one has been reconfigured to such extent that required
    data structures do not exist anymore.
    This script must be run prior to any upload attempts; it ensures that a state 
    chart and mandatory identification queries exist in the database before any upload.

-----------------------------------------------------------------------------"""

import acm
import FAssetManagementUtils

STATECHART_NAME = 'Data Upload'
FACILITY_IDENTIFICATION_QUERY_NAME = 'WSO_Facility_ExternalId1'
CONTRACT_IDENTIFICATION_QUERY_NAME = 'WSO_Contract_ExternalId1'
TRADE_IDENTIFICATION_QUERY_NAME = 'WSO_Trade_OptionalKey'
ALL_DATA_STRUCTURES = [STATECHART_NAME, FACILITY_IDENTIFICATION_QUERY_NAME, CONTRACT_IDENTIFICATION_QUERY_NAME, TRADE_IDENTIFICATION_QUERY_NAME]

logger = FAssetManagementUtils.GetLogger()

def CreateStateChart():
    import FStateChartUtils

    name = STATECHART_NAME
    logger.info('Uploading state chart %s.' % name)
    
    # Create the default state chart for WSO Business Data Upload
    limit = 'Single'
    layout = 'Unidentified,445,328;Successful,835,-71;Invalid data,443,96;Pending upload,676,99;Comparison,578,-254;Ready,164,42;Discrepancy,579,-86;'
    definition = {
        'Ready':                {'Identified': 'Comparison',
                                 'Not identified': 'Unidentified'},
        'Unidentified':         {'Create business object': 'Pending upload',
                                 'Validation failed': 'Invalid data'},
        'Invalid data':         {'Corrected': 'Ready'},
        'Discrepancy':          {'Corrected': 'Ready',
                                 'Update business object': 'Pending upload'},

        'Comparison':           {'Mismatch found': 'Discrepancy',
                                 'Matched': 'Successful'},
        'Pending upload':       {'Validation failed': 'Invalid data',
                                 'Uploaded successfully': 'Successful'}
        }

    success = FStateChartUtils.CreateStateChart(name, definition, layout, limit)
    if not success:
        logger.info('Could not upload state chart %s to the ADS.' % name)
        return None
    logger.info('Successfully uploaded state chart %s to the ADS.' % name)
    
def CreateIdentificationQueriesInADS():
    queryNames = [FACILITY_IDENTIFICATION_QUERY_NAME, CONTRACT_IDENTIFICATION_QUERY_NAME, TRADE_IDENTIFICATION_QUERY_NAME]
    for queryName in queryNames:
        wsoStoredASQLQuery = acm.FStoredASQLQuery[queryName]
        if wsoStoredASQLQuery:
            logger.info('WSO query identifier %s already exists in the ADS. No upload is needed.' % queryName)
            continue
        logger.info('Creating identification query %s in the ADS.' % queryName)
        acmQueryClass = queryName.split('_')[1]
        if acmQueryClass == 'Facility':
            query = acm.CreateFASQLQuery(acm.FCombination, 'AND')
        elif acmQueryClass == 'Contract':
            query = acm.CreateFASQLQuery(acm.FFrn, 'AND')
        elif acmQueryClass == 'Trade':
            query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        else:
            logger.info('WSO query Identifier could not be retrieved. The types "Facility", "Contract", and "Trade" are only allowed.')
            return
        opNode = query.AddOpNode('OR')
        queryKey = queryName.split('_')[2]
        opNode.AddAttrNode(queryKey, 'EQUAL', None)
        storedQuery = acm.FStoredASQLQuery()
        storedQuery.Query(query)
        storedQuery.Name(queryName)
        storedQuery.Commit()
        logger.info('Successfully persisted data upload identification query %s in the ADS.' % queryName)

def IsSuccessfulUpload():
    stateChartInADS = acm.FStateChart[STATECHART_NAME]
    facilityQueryInADS = acm.FStoredASQLQuery[FACILITY_IDENTIFICATION_QUERY_NAME]
    contractQueryInADS = acm.FStoredASQLQuery[CONTRACT_IDENTIFICATION_QUERY_NAME]
    tradeQueryInADS = acm.FStoredASQLQuery[TRADE_IDENTIFICATION_QUERY_NAME]
    if stateChartInADS and facilityQueryInADS and contractQueryInADS and tradeQueryInADS:
        logger.info('Successfully initialized WSO Bank Debt data structures.')
    else:
        logger.info('One or more WSO Bank Debt data structures were not correctly initialized.')
        
def DisplaySummary(displaySummary):
    dataStructureNames = list()
    nonPersistedObjects = list()
    for DATA_STRUCTURE in ALL_DATA_STRUCTURES:
        if DATA_STRUCTURE == STATECHART_NAME:
            if acm.FStateChart[DATA_STRUCTURE]:
                dataStructureNames.append(DATA_STRUCTURE)
        elif DATA_STRUCTURE != STATECHART_NAME:
            if acm.FStoredASQLQuery[DATA_STRUCTURE]:
                dataStructureNames.append(DATA_STRUCTURE)
        else:
            nonPersistedObjects.append(DATA_STRUCTURE)
    if displaySummary:
        logger.info('---------- WSO Bank Debt Setup Summary ----------')
        logger.info('Persisted the following data structures: ')
        for dataStructureName in dataStructureNames:
            logger.info('%s' % dataStructureName)
        if len(nonPersistedObjects) > 0:
            logger.info('Failed to persist the following objects: ')
            for nonPersistedObject in nonPersistedObjects:
                logger.info('%s' % nonPersistedObject)
        logger.info('---------- End of Summary ----------')
        
def GetDisplaySummary():
    tab = ''
    label = 'Display summary'
    tooltip = ('Select this option to obtain a summary after the script has been executed. ', )
    return (('DisplayOption', '_'.join((label, tab)), 'string', ["1", "0"], "1", 0, 0, tooltip),)
    
def RunSetup(params = None):
    logger.info('Starting WSO Bank Debt setup procedures. Initializing data structures...')
    CreateStateChart()
    CreateIdentificationQueriesInADS()
    IsSuccessfulUpload()
    if params:
        DisplaySummary(params['DisplayOption'])
    logger.info('Finishing WSO Bank Debt setup procedures.')

ael_variables = []
ael_variables.extend(GetDisplaySummary())

def ael_main(params):
    RunSetup(params)