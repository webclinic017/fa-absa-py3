'''
===================================================================================================
PURPOSE: Two tasks should be generated from this script.
            1. The first task should run on a daily basis and should delete all discarded HRs.
                It will by default also generate a report according to the following logic:
                - Find each parent (underlying) trade's number by parsing xml
                - Find each parent and child trade's update times
                - If parent's update time is after child's, add to report
                - Report includes:
                       parent trade's:
                               update user
                               update time
                               type (e.g. Internal, External...)
                               trade number
                       child trade's:
                               update user
                               update time
                               trade number
                               percentage of parent
                       HR's:
                               name
            2. The second task should be scheduled to run at the end of each month. It should run
                all active HRs. The report referred to above will be generated by default.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
===================================================================================================
'''

import sys
import os
import csv
import time
from xml.dom.minidom import parseString

import acm
import FRunScriptGUI
import FLogger
import FFileUtils

import HedgeRelation
import HedgeTestEngine
import HedgeConstants
import FLimitedOutputSettingsTab
import HedgeAccountingStorage

trueFalse = ['True', 'False']
logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE, HedgeConstants.LOG_VERBOSITY)


class HedgeScripts(FRunScriptGUI.AelVariablesHandler):
    def activeAllList(self, index, fieldValues):
        self.selectedActive.enable(trueFalse.index(fieldValues[index]))
        return fieldValues

    def __init__(self):
        vars = [['printTestResults',
                 'Print the test results to the log',
                 'string',
                 trueFalse,
                 'False',
                 1,
                 0,
                 'Print the test results to the log'],
                ['deleteDiscarded',
                 'Delete Discarded Hedge Relationships',
                 'string',
                 trueFalse,
                 'True',
                 1,
                 0,
                 'Delete Hedge Relationships that have been moved to Discarded status'],
                ['runAllActive',
                 'Test All Active Relationships',
                 'string',
                 trueFalse,
                 'True',
                 1,
                 0,
                 'Run tests for all Active Hedge Relationships', self.activeAllList, 1],
                ['selectedActive',
                 'Active Hedge Relationships',
                 'FCustomTextObject',
                 '',
                 '',
                 0,
                 1,
                 'Choice of ',
                 None,
                 0],
                ['numberOfWorkers',
                 'Total number of Hedge Test Workers',
                 'int',
                 0,
                 1,
                 1,
                 0,
                 'Number of Tasks used for the Hedge Effectiveness batch run.', 
                 None, 
                 1],
                ['workerNumber',
                 'Worker number',
                 'int',
                 0,
                 1,
                 1,
                 0,
                 'Worker x / y. For example worker 2 of 5.', 
                 None, 
                 1]]
                
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars)

        self.extend(FLimitedOutputSettingsTab.getAelVariables())


ael_variables = HedgeScripts()


def ael_main(params):
    logger.CLOG('FHedgeRelationTasks start.')
	
    if params['deleteDiscarded'] == 'True':
        deleteAllDiscarded()
    if params['runAllActive'] == 'True' or params['selectedActive']:
        runActive(params)
    name = HedgeConstants.STR_PARENT_CHANGE_REPORT
    filePath = getNewFilePath(name, params, '.csv')
    data, parent_count, hr_count = gather_data()
    export_data(filePath, data)
    logger.CLOG('FHedgeRelationTasks end.')
    logger.LOG('%s hedge relationships reviewed. %s unique parent(s) written to %s'
               % (hr_count, parent_count, filePath))


def _getAllTextObjects():
    query = "cid = 'Customizable' and name like 'HR/*'"
    return acm.FCustomTextObject.Select(query)


def _repair_settings(old_settings):
    if 'LoLimit' not in old_settings['ProDollarOffset'].keys():
        old_settings['ProDollarOffset']['LoLimit'] = HedgeConstants.DBL_PRO_DO_LO_LIMIT
    if 'HiLimit' not in old_settings['ProDollarOffset'].keys():
        old_settings['ProDollarOffset']['HiLimit'] = HedgeConstants.DBL_PRO_DO_HI_LIMIT
    if 'HiBetaLimit' not in old_settings['Regression'].keys():
        old_settings['Regression']['HiBetaLimit'] = HedgeConstants.DBL_PRO_REG_HI_B_LIMIT
    if 'LoBetaLimit' not in old_settings['Regression'].keys():
        old_settings['Regression']['LoBetaLimit'] = HedgeConstants.DBL_PRO_REG_LO_B_LIMIT
    if 'R2Limit' not in old_settings['Regression'].keys():
        old_settings['Regression']['R2Limit'] = HedgeConstants.DBL_PRO_REG_R2_LIMIT
    if 'PValueLimit' not in old_settings['Regression'].keys():
        old_settings['Regression']['PValueLimit'] = HedgeConstants.DBL_PRO_REG_P_LIMIT
    if 'Limit' not in old_settings['ProVRM'].keys():
        old_settings['ProVRM']['Limit'] = HedgeConstants.DBL_PRO_VRM_LIMIT
    if 'LoLimit' not in old_settings['RetroDollarOffset'].keys():
        old_settings['RetroDollarOffset']['LoLimit'] = HedgeConstants.DBL_RETRO_DO_LO_LIMIT
    if 'HiLimit' not in old_settings['RetroDollarOffset'].keys():
        old_settings['RetroDollarOffset']['HiLimit'] = HedgeConstants.DBL_RETRO_DO_HI_LIMIT
    if 'Limit' not in old_settings['RetroVRM'].keys():
        old_settings['RetroVRM']['Limit'] = HedgeConstants.DBL_RETRO_VRM_LIMIT

    return old_settings


def deleteAllDiscarded():
    textObjects = _getAllTextObjects()
    timeSeriesSpecId = acm.FTimeSeriesDvSpec[HedgeConstants.STR_TIMESERIESSPECNAME].Oid()
    timeSeriesTSSpecId = acm.FTimeSeriesDvSpec[HedgeConstants.STR_TSTIMESERIESSPECNAME].Oid()
    proDoSpecId = acm.FChoiceList[HedgeConstants.STR_PRODOVALUENAME].Oid()
    retDoSpecId = acm.FChoiceList[HedgeConstants.STR_RETDOVALUENAME].Oid()
    proVrmSpecId = acm.FChoiceList[HedgeConstants.STR_PROVRMVALUENAME].Oid()
    retVrmSpecId = acm.FChoiceList[HedgeConstants.STR_RETVRMVALUENAME].Oid()
    delCnt = 0
    for textObject in textObjects:
        name = textObject.Name()
        try:
            hedgeRelationship = HedgeRelation.HedgeRelation(name)
            hedgeRelationship.read()
        except Exception, e:
            logger.ELOG(e)
            continue
        if hedgeRelationship.get_status() != 'Discard':
            continue
        try:
            _, dealPackageName = hedgeRelationship.get_deal_package()
            query = 'optionalId = %s' % dealPackageName
            dealPackage = acm.FDealPackage.Select(query)
            if not dealPackage:
                continue
            else:
                dealPackage = dealPackage[0]
            query = 'timeSeriesDvSpecification = %s and recordAddress1 = %s' \
                    % (timeSeriesSpecId, dealPackage.Oid())
            timeSeriesDataPoints = acm.FTimeSeriesDv.Select(query)
            proDoTsDp = _getLastValueTs(timeSeriesSpecId,
                                        timeSeriesTSSpecId,
                                        dealPackage.Oid(),
                                        proDoSpecId)
            retDoTsDp = _getLastValueTs(timeSeriesSpecId,
                                        timeSeriesTSSpecId,
                                        dealPackage.Oid(),
                                        retDoSpecId)
            proVrmTsDp = _getLastValueTs(timeSeriesSpecId,
                                         timeSeriesTSSpecId,
                                         dealPackage.Oid(),
                                         proVrmSpecId)
            retVrmTsDp = _getLastValueTs(timeSeriesSpecId,
                                         timeSeriesTSSpecId,
                                         dealPackage.Oid(),
                                         retVrmSpecId)
        except Exception, e:
            print(e)
            logger.ELOG(e)
            continue

        # Base TS
        tsdpCnt = 0
        for timeSeriesDataPoint in timeSeriesDataPoints:
            tsdpCnt += 1
            timeSeriesDataPoint.Delete()
        logger.LOG('Deleted %i discarded time series points' % tsdpCnt)

        tsdpCnt = 0
        for tsList in [proDoTsDp, retDoTsDp, proVrmTsDp, retVrmTsDp]:
            if tsList is None:
                continue
            for timeSeriesDataPoint in tsList:
                ts = acm.FTimeSeriesDv[timeSeriesDataPoint]
                tsdpCnt += 1
                ts.Delete()
        logger.LOG('Deleted %i discarded time series points for hedge relationship %s '
                   % (tsdpCnt, name))

        hedgeRelationship.delete(True)
        delCnt += 1
        logger.LOG('Finished deleting hedge relationship: %s' % name)
    logger.LOG('Deleted %i discarded hedge relationships' % delCnt)


def _getLastValueTs(timeSeriesSpecId, timeSeriesTSSpecId, dealPackageOid, specId):
    query = 'timeSeriesDvSpecification = %s and recordAddress1 = %s and recordAddress2 = %s' \
            % (timeSeriesSpecId, dealPackageOid, specId)
    lastValues = acm.FTimeSeriesDv.Select(query)
    logger.LOG(query)
    if not lastValues:
        return None
    timeSeries = []
    for lastValue in lastValues:
        query = 'timeSeriesDvSpecification = %s and recordAddress1 = %s' \
                % (timeSeriesTSSpecId, lastValue.Oid())
        logger.LOG(query)
        for ts in acm.FTimeSeriesDv.Select(query):
            timeSeries.append(ts.Oid())
    return timeSeries


def runActive(params):

    numberOfWorkers = params['numberOfWorkers']
    workerModNumber = params['workerNumber'] - 1

    # add some validation
    if workerModNumber >= 0 and workerModNumber < numberOfWorkers:

        if params['runAllActive'] == 'True':
            textObjects = _getAllTextObjects()
        else:
            textObjects = params['selectedActive']
            
        runCnt = 0
        for textObject in textObjects:

            # Filter textObjects to split the tests into batches between task workers
            assignToWorkerNumber = textObject.Oid() % numberOfWorkers
            if assignToWorkerNumber == workerModNumber:
                name = textObject.Name()
                
                try:
                    hedgeRelationship = HedgeRelation.HedgeRelation(name)
                    hedgeRelationship.read()
                except:
                    continue
                    
                if hedgeRelationship.get_status() != 'Active':
                    continue
                    
                old_settings = hedgeRelationship.get_test_settings()
                new_settings = _repair_settings(old_settings)
                hedgeRelationship.set_test_settings(new_settings)
                
                print(('Start tests for active hedge relationships: %s' % name))
                results = HedgeTestEngine.run_tests(hedgeRelationship)
                
                if not results:
                    continue
                    
                runCnt += 1
                
                print(('Finished running tests for hedge relationship: %s' % name))
                
                if params['printTestResults'] == 'True':
                    print(results)
                else:
                    logger.LOG(results)
                    
                if params['XMLtoFile'] == 'True':
                    writeReport(name, params, results)
                    
        print(('Ran tests for %i active hedge relationships' % runCnt))
    else:
        logger.ELOG('Task configuration error.')



def writeReport(name, params, results):
    xml = createXML(name, results)
    writeXMLToFile(name, params, xml.toxml())
    logger.LOG('Finished exporting test data for hedge relationship: %s' % name)


def createXML(name, results):
    data = '<xml version="1.0"><TestResults></TestResults></xml>'
    xml = parseString(data)
    root = xml.getElementsByTagName('TestResults')[0]
    HedgeAccountingStorage.set_element_tag_value(xml, root, 'HR_Name', name)
    HedgeAccountingStorage.set_element_tag_value(xml, root, 'TestDate', acm.Time().TimeNow())
    HedgeAccountingStorage.set_element_tag_value(xml, root, 'OverAllResult',
                                                 results["Overall Result"])
    HedgeAccountingStorage.set_element_tag_value(xml, root, 'Tests', '')
    root = xml.getElementsByTagName('Tests')[0]
    testCount = 0
    for key in results.keys():
        HedgeAccountingStorage.set_element_tag_value(xml, root, 'Test', '')
        testRoot = xml.getElementsByTagName('Test')[testCount]
        HedgeAccountingStorage.set_element_tag_value(xml, testRoot, 'Name', key)
        if key == 'Overall Result':
            continue
        if 'result' in results[key].keys():
            HedgeAccountingStorage.set_element_tag_value(xml,
                                                         testRoot,
                                                         'Result',
                                                         results[key]['result'])
        if 'do' in results[key].keys():
            dataDict = results[key]['do']
            dates = sorted(dataDict.keys())
            HedgeAccountingStorage.set_element_tag_value(xml,
                                                         testRoot,
                                                         'DollarOffsetValue',
                                                         round(dataDict[dates[-1]], 5))
        if 'vr' in results[key].keys():
            dataDict = results[key]['vr']
            dates = sorted(dataDict.keys())
            HedgeAccountingStorage.set_element_tag_value(xml,
                                                         testRoot,
                                                         'VariableReductionValue',
                                                         round(dataDict[dates[-1]], 5))
        if 'alpha' in results[key].keys():
            HedgeAccountingStorage.set_element_tag_value(xml,
                                                         testRoot,
                                                         'RegressionAlpha',
                                                         results[key]['alpha'])
        if 'beta' in results[key].keys():
            HedgeAccountingStorage.set_element_tag_value(xml,
                                                         testRoot,
                                                         'RegressionBeta',
                                                         results[key]['beta'])
        if 'correlation' in results[key].keys():
            HedgeAccountingStorage.set_element_tag_value(xml,
                                                         testRoot,
                                                         'RegressionCorrelation',
                                                         results[key]['correlation'])
        if 'R2' in results[key].keys():
            HedgeAccountingStorage.set_element_tag_value(xml,
                                                         testRoot,
                                                         'RegressionRSquared',
                                                         results[key]['R2'])
        if 'PValue' in results[key].keys():
            HedgeAccountingStorage.set_element_tag_value(xml,
                                                         testRoot,
                                                         'RegressionPValue',
                                                         results[key]['PValue'])
        if 'Std_Err' in results[key].keys():
            HedgeAccountingStorage.set_element_tag_value(xml,
                                                         testRoot,
                                                         'RegressionStandardError',
                                                         results[key]['Std_Err'])
        testCount = testCount + 1
    return xml


def getNewFilePath(fileName, params, ext):
    # Add date to file name?
    fileName = fileName.replace('/', '_')
    if params['FileDateFormat']:
        if params['FileDateBeginning'] == 'True':
            fileName = time.strftime(params['FileDateFormat']) + '_' + fileName
        else:
            fileName = fileName + '_' + time.strftime(params['FileDateFormat'])
    outputDir = params['FilePath'].AsString()

    if params['CreateDirectoryWithDate'] == 'True':
        outputDir = createOutputDir(params)

    if params['OverwriteIfFileExists'] == 'True':
        return os.path.join(outputDir, fileName + ext)

    i = 1
    testFile = os.path.join(outputDir, fileName + ext)
    while os.path.exists(testFile):
        testFile = os.path.join(outputDir, fileName + '_' + str(i) + ext)
        i = i + 1
    return testFile


def createOutputDir(params):
    if isinstance(params['FilePath'], basestring):
        outputDir = params['FilePath']
    else:
        outputDir = params['FilePath'].AsString()

    if outputDir == "":
        # Use current directory by default
        outputDir = os.path.abspath(outputDir)

    if params['CreateDirectoryWithDate'] == 'True':
        outputDir = os.path.join(outputDir, time.strftime(params['DateFormat']) + os.sep)

    outputDir = FFileUtils.expandEnvironmentVar(outputDir)

    if not os.path.exists(outputDir):
        try:
            os.makedirs(outputDir)
            logger.LOG('Created report output directory:' + outputDir)
        except:
            msg = 'Failed to create report directory:' + outputDir
            logger.ELOG(msg)
            raise Exception(msg)

    return outputDir


def writeToFile(path, content):
    writeToFileMode(path, content, 'w')


def writeToFileMode(path, content, mode):
    m_file = open(path, mode)
    m_file.write(content)
    m_file.close()


def writeXMLToFile(name, params, reportXml):
    filePath = getNewFilePath(name, params, '.xml')
    writeToFile(filePath, reportXml)
    logger.LOG("Wrote XML to : " + filePath)


def export_data(outputfile, data):
    try:
        with open(outputfile, 'wb') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            header_row = ['Reason', 'Hedge Relationship',
                          'Parent Trade', 'Parent Trade Type', 'Parent Trade Update User',
                          'Parent Trade Update Time', 'Parent Instrument',
                          'Parent Instrument Type', 'Parent Instrument Update User',
                          'Parent Instrument Update Time', 'Child Trade',
                          'Child Trade Percentage', 'Child Trade Update Time',
                          'Child Trade Update User', 'Child Instrument', 'Child Instrument Type',
                          'Child Instrument Update Time', 'Child Instrument Update User',
                          'Expired Relationship?']
            writer.writerow(header_row)
            for row_data in data:
                writer.writerow(row_data)
    except Exception, e:
        logger.ELOG(e)
        sys.exit(e)


def gather_data():
    '''
    Determine whether parent trades (or their instruments) have been updated after their children.
    Also check for HRs which have expired. Add all of these to the report.
    '''
    data = []
    hr_count = 0
    unique_parents = set()
    all_HRs = HedgeRelation.get_hedge_accounting_filenames()
    hr_count = len(all_HRs)
    for hedge_relationship in all_HRs:
        hr = HedgeRelation.HedgeRelation(hedge_relationship)
        hr.read()

        if hr.get_status() == HedgeConstants.Hedge_Relation_Status.Active:
            trades = hr.get_trades()  # Format:{parent:[parent_type, child_percentage, child_trade]}
            for key in trades.keys():
                reason = ''
                flagged = False
                if trades[key][2]:
                    try:
                        parent_trd_obj = acm.FTrade[key]
                        child_trd_obj = acm.FTrade[trades[key][2]]
                        date_difference = acm.Time().DateDifference(hr.get_end_date(),
                                                                    HedgeConstants.DAT_TODAY)
                        parent_ins_obj = parent_trd_obj.Instrument()
                        child_ins_obj = child_trd_obj.Instrument()
                        if parent_trd_obj.UpdateTime() > child_trd_obj.UpdateTime():
                            reason += 'Parent Trade '
                            flagged = True
                        if (parent_ins_obj.UpdateTime() > child_ins_obj.UpdateTime()) or \
                           acm.Time.DateDifference(hr.get_start_date(),
                                                   acm.Time.DateFromTime(
                                                       parent_ins_obj.UpdateTime()
                                                   )) < 0:
                            reason += 'Parent Instrument '
                            flagged = True
                        if acm.Time.DateDifference(hr.get_start_date(),
                                                   acm.Time.DateFromTime(
                                                       child_ins_obj.UpdateTime()
                                                   )) < 0:
                            reason += 'Child Instrument '
                            flagged = True
                        if date_difference <= 0:
                            reason += 'HR Expired'
                            flagged = True

                        if flagged:

                            unique_parents.add(key)

                            parent_trade = key
                            parent_trade_type = trades[parent_trade][0]
                            parent_trd_update = acm.Time.DateTimeFromTime(
                                parent_trd_obj.UpdateTime()
                            )
                            parent_trade_update_user = parent_trd_obj.UpdateUser().Name()

                            parent_instrument = parent_ins_obj.Name()
                            parent_instrument_type = parent_ins_obj.InsType()
                            parent_instrument_update_user = parent_ins_obj.UpdateUser().Name()
                            parent_ins_update = acm.Time.DateTimeFromTime(
                                parent_ins_obj.UpdateTime()
                            )

                            child_percentage = trades[parent_trade][1]
                            child_trade = trades[parent_trade][2]
                            child_trd_update = acm.Time.DateTimeFromTime(child_trd_obj.UpdateTime())
                            child_trade_update_user = child_trd_obj.UpdateUser().Name()

                            child_instrument = child_ins_obj.Name()
                            child_instrument_type = child_ins_obj.InsType()
                            child_ins_update = acm.Time.DateTimeFromTime(child_ins_obj.UpdateTime())
                            child_instrument_update_user = child_ins_obj.UpdateUser().Name()

                            expired_relationship = False

                            if date_difference <= 0:
                                expired_relationship = True
                            row_data = [reason, hedge_relationship, parent_trade,
                                        parent_trade_type, parent_trade_update_user,
                                        parent_trd_update, parent_instrument,
                                        parent_instrument_type, parent_instrument_update_user,
                                        parent_ins_update, child_trade,
                                        child_percentage, child_trd_update,
                                        child_trade_update_user, child_instrument,
                                        child_instrument_type, child_ins_update,
                                        child_instrument_update_user, expired_relationship]
                            data.append(row_data)

                    except Exception, e:
                        logger.ELOG('For Parent: %s, Child: %s:' % (key, trades[key][2]))
                        logger.ELOG(e)
    parent_count = len(unique_parents)
    return data, parent_count, hr_count
