""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/bdp_dashboard/FBDPDashboardQuery.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

import collections


import FBDPDashboardData
import FBDPDashboardUtil
import FBDPDashboardDefaultConfig

CATEGORY_NAME_OTHERS = 'Others'
CATEGORY_NAME_NIL = 'Nil'


NUM_MAX_TOP_N_EVAL_ACM_ROWS = 10

TAG_MULTIPLE_RESULTS = 'MULTIPLE RESULTS'
TAG_EVAL_ACM = 'EVAL_ACM'
TAG_EVAL_TIME = 'EVAL_TIME'
TAG_ACM_PORTFOLIO = 'acm.FPhysicalPortfolio'
TAG_ACM_INSTRUMENT = 'acm.FInstrument'
TAG_ACM_PARTY = 'acm.FParty'
TAG_ACM_INS_TYPE_ENUM = 'acm.FEnumeration[''enum(InsType)'']'


class QueryProcessor(object):

    def __init__(self, querySpec, acmProxy=FBDPDashboardUtil.AcmProxy(),
            dbSqlProxy=FBDPDashboardUtil.DbSqlProxy()):

        self.__querySpec = querySpec
        self.__acmProxy = acmProxy
        self.__dbSqlProxy = dbSqlProxy

    def getName(self):

        return self.__querySpec['Name']

    def getUnitDescription(self):

        return self.__querySpec['Unit Description']

    def hasEvalAcmTag(self):

        categoryNameList = self.__querySpec['Category Name']
        for categoryName in categoryNameList:
            if TAG_EVAL_ACM in categoryName:
                return True
        return False

    def hasEvalTimeTag(self):

        categoryNameList = self.__querySpec['Category Name']
        for categoryName in categoryNameList:
            if TAG_EVAL_TIME in categoryName:
                return True
        return False

    def hasMultipleResults(self):

        categoryNameList = self.__querySpec['Category Name']
        for categoryName in categoryNameList:
            if TAG_MULTIPLE_RESULTS in categoryName:
                return True
            elif categoryName in (
                    FBDPDashboardDefaultConfig.DB_TABLE_NAME_TRADE,
                    FBDPDashboardDefaultConfig.DB_TABLE_NAME_INSTRUMENT,
                    FBDPDashboardDefaultConfig.DB_TABLE_NAME_PRICE_HST,
                    FBDPDashboardDefaultConfig.DB_TABLE_NAME_ADDITIONAL_INFO):
                return True
        return False

    def hasTableTag(self):

        categoryNameList = self.__querySpec['Category Name']
        for categoryName in categoryNameList:
            if categoryName in (
                    FBDPDashboardDefaultConfig.DB_TABLE_NAME_TRADE,
                    FBDPDashboardDefaultConfig.DB_TABLE_NAME_INSTRUMENT,
                    FBDPDashboardDefaultConfig.DB_TABLE_NAME_PRICE_HST,
                    FBDPDashboardDefaultConfig.DB_TABLE_NAME_ADDITIONAL_INFO):
                return True
        return False

    def buildQueryStatements(self, previousQueryCondition):

        if not isinstance(previousQueryCondition, str):
            raise ValueError('The given previous query condition is expected '
                    'to be a string, but value {0} was given.'.format(
                    previousQueryCondition))

        categoryNameList = self.__querySpec['Category Name']
        selectFromClauses = self.__querySpec['Select Result']
        query_condition = self.__querySpec['Query Condition']

        # Build query statement for each category.
        perCategoryQueryStatementList = []
        for categorySequence in range(len(categoryNameList)):

            categoryQueryCondition = query_condition[categorySequence]
            if not previousQueryCondition:
                qryStmt = ''.join([selectFromClauses, ' ',
                        categoryQueryCondition])
            elif 'WHERE' in categoryQueryCondition.upper():
                qryStmt = ''.join([selectFromClauses, ' ',
                        previousQueryCondition, ' AND ',
                        categoryQueryCondition])
            else:
                qryStmt = ''.join([selectFromClauses, ' ',
                        previousQueryCondition, ' ', categoryQueryCondition])
            perCategoryQueryStatementList.append(qryStmt)
        return perCategoryQueryStatementList

    def runQueryStatements(self, qryStmts):

        qryResultRowsList = []
        for qryStmt in qryStmts:
            qryResultRows = self.__dbSqlProxy.execute(qryStmt)
            qryResultRowsList.append(qryResultRows)
        return qryResultRowsList

    def _reallyRecommendActions(self, currentSubTitle, categoryName,
            categoryCount):

        thresholdList = []
        recommendedActionNameList = []
        for actionSpec in self.__querySpec['Action']:
            actionKey = [k.strip() for k in actionSpec['Key'].split('&')]
            curKey = ''.join([self.__querySpec['Name'], ' = ', categoryName])
            found = False
            for aKey in actionKey:
                if aKey in curKey or aKey in currentSubTitle:
                    found = True
                else:
                    found = False
                    break
            if not found:
                continue
            categoryMaxCount = int(actionSpec['MaxCount'])
            thresholdList.append(categoryMaxCount)
            actionName = actionSpec['Action']
            if categoryCount > categoryMaxCount:
                recommendedActionNameList.append(actionName)
        # Find min threshold
        minThreshold = None
        if thresholdList:
            minThreshold = min(thresholdList)
        # Concatenation
        recommendedActionNames = ' '.join(recommendedActionNameList)
        return recommendedActionNames, minThreshold

    def recommendActions(self, currentSubTitle, categoryName, categoryCount):

        minThreshold = None
        recommendedActionNames = ''
        actionSpecList = self.__querySpec['Action']
        # If category name is 'Others'
        if (CATEGORY_NAME_OTHERS in categoryName or
                CATEGORY_NAME_NIL in categoryName):
            return recommendedActionNames, minThreshold
        # If action spec not exists.
        if not actionSpecList:
            return recommendedActionNames, minThreshold
        # Now start analyse each action spec
        recommendedActionNames, minThreshold = self._reallyRecommendActions(
                currentSubTitle, categoryName, categoryCount)
        return recommendedActionNames, minThreshold

    def _processQueryResultsWithEvalTimeTag(self, qryResultRowsList,
            currentSubTitle):

        assert len(self.__querySpec['Category Name']) == 1, ('There should be '
                'exactly one entry in the "Category Name" if that entry has '
                'EVAL_TIME tag.')
        qryResultRows = qryResultRowsList[0]
        strDateToCountMap = collections.defaultdict(int)
        for row in qryResultRows:
            count = row[0]
            strDate = row[1][:10]
            strDateToCountMap[strDate] += count
        if FBDPDashboardUtil.containsNonIsoDate(strDateToCountMap):
            print('Some dates are not in ISO date format -- date sorting '
                    'would be wrong.')
        resultDataList = []
        for strDate, dayTotalCount in sorted(strDateToCountMap.iteritems()):
            recmActNames, minThreshold = self.recommendActions(currentSubTitle,
                    categoryName=strDate, categoryCount=dayTotalCount)
            resultData = FBDPDashboardData.ResultData(categoryName=strDate,
                    count=dayTotalCount, threshold=minThreshold,
                    recommendedActions=recmActNames)
            resultDataList.append(resultData)
        return resultDataList

    def _evalAcmPhysicalPortfolioName(self, oidField):

        portOid = int(oidField)
        acmPort = self.__acmProxy.getFPhysicalPortfolioByOid(portOid)
        if acmPort:
            portName = acmPort.Name()
        elif portOid == 0:
            portName = CATEGORY_NAME_NIL
        else:
            print(('Failed to get the acm physical portfolio object '
                    '(oid={0})'.format(portOid)))
            portName = None
        return portName

    def _evalAcmInstrumentName(self, oidField):

        insOid = int(oidField)
        acmIns = self.__acmProxy.getFInstrumentByOid(insOid)
        if acmIns:
            insName = acmIns.Name()
        else:
            print(('Failed to get the acm instrument object (oid={0})'.format(
                    insOid)))
            insName = None
        return insName

    def _evalAcmPartyName(self, oidField):

        partyOid = int(oidField)
        acmParty = self.__acmProxy.getFPartyByOid(partyOid)
        if acmParty:
            partyName = acmParty.Name()
        else:
            print(('Failed to get the acm party object (oid={0})'.format(
                    partyOid)))
            partyName = None
        return partyName

    def _evalAcmEnumerationInsTypeName(self, oidField):

        insTypeNum = int(oidField)
        acmInsTypeEnum = self.__acmProxy.getFEnumerationInsType()
        insTypeName = acmInsTypeEnum.Enumerator(insTypeNum)
        return insTypeName

    def _selectEvalAcmNameFunction(self, categoryName):

        if TAG_ACM_PORTFOLIO in categoryName:
            evalAcmNameFunc = self._evalAcmPhysicalPortfolioName
        elif TAG_ACM_INSTRUMENT in categoryName:
            evalAcmNameFunc = self._evalAcmInstrumentName
        elif TAG_ACM_PARTY in categoryName:
            evalAcmNameFunc = self._evalAcmPartyName
        elif TAG_ACM_INS_TYPE_ENUM in categoryName:
            evalAcmNameFunc = self._evalAcmEnumerationInsTypeName
        else:
            raise AssertionError('Unable to decide which ACM evaluation '
                    'function to use.  The category name of this query spec '
                    'is: {0}'.format(self.__querySpec['Category Name']))
        return evalAcmNameFunc

    def _processQueryResultsWithEvalAcmTag(self, qryResultRowsList,
            currentSubTitle, numMaxTopNRows=NUM_MAX_TOP_N_EVAL_ACM_ROWS):

        categoryNameList = self.__querySpec['Category Name']
        assert len(categoryNameList) == 1, ('There should be '
                'exactly one entry in the "Category Name" if that entry has '
                'EVAL_ACM tag.')
        categoryName = categoryNameList[0]
        qryResultRows = qryResultRowsList[0]
        # Decide name evaluation function
        evalAcmNameFunc = self._selectEvalAcmNameFunction(categoryName)
        # Sort result
        revSortedResultRows = sorted(qryResultRows, reverse=True)
        numTopRows = min(numMaxTopNRows, len(revSortedResultRows))
        topResultRows = revSortedResultRows[:numTopRows]
        remainingResultRows = revSortedResultRows[numTopRows:]
        # Process top result rows
        resultDataList = []
        for row in topResultRows:
            count = row[0]
            name = evalAcmNameFunc(oidField=row[1])
            if name is not None:
                recmActNames, minThreshold = self.recommendActions(
                        currentSubTitle, categoryName=name,
                        categoryCount=count)
                resultData = FBDPDashboardData.ResultData(categoryName=name,
                        count=count, threshold=minThreshold,
                        recommendedActions=recmActNames)
                resultDataList.append(resultData)
        # Process 'other' rows
        if remainingResultRows:
            remainingCount = sum([row[0] for row in remainingResultRows])
            recmActNames, minThreshold = self.recommendActions(currentSubTitle,
                    CATEGORY_NAME_OTHERS, remainingCount)
            resultData = FBDPDashboardData.ResultData(
                    categoryName=CATEGORY_NAME_OTHERS, count=remainingCount,
                    threshold=minThreshold, recommendedActions=recmActNames)
            resultDataList.append(resultData)
        return resultDataList

    def _processQueryResultsWithNoEvalTag(self, qryResultRowsList,
            currentSubTitle):

        categoryNameList = self.__querySpec['Category Name']
        resultDataList = []
        for seqNum in range(len(qryResultRowsList)):
            categoryName = categoryNameList[seqNum]
            qryResultRows = qryResultRowsList[seqNum]

            assert len(qryResultRows) == 1, ('There should be only one row '
                    'per category; however, this category {0} has {1} '
                    'rows.'.format(categoryName, len(qryResultRows)))
            row = qryResultRows[0]
            categoryCount = row[0]
            recmActNames, minThreshold = self.recommendActions(currentSubTitle,
                    categoryName, categoryCount)

            resultData = FBDPDashboardData.ResultData(
                    categoryName=categoryName, count=categoryCount,
                    threshold=minThreshold, recommendedActions=recmActNames)
            resultDataList.append(resultData)
        return resultDataList

    def _processMultipleQueryResults(self, qryResultRowsList,
            currentSubTitle):

        dbName = None
        if self.__querySpec == FBDPDashboardDefaultConfig.DATABASE_QUERY_SPEC:
            dbName = self.__dbSqlProxy.execute('SELECT db_name()')[0][0]

        resultDataList = []
        for seqNum in range(len(qryResultRowsList)):
            qryResultRows = qryResultRowsList[seqNum]
            # if there are no rows, then go down to the next level
            if len(qryResultRows) == 0:
                #switch to lower level
                self.__querySpec = (
                        FBDPDashboardDefaultConfig.BDP_TABLES_QUERY_SPEC)
                queries = self.buildQueryStatements('')
                results = self.runQueryStatements(queries)
                return self._processMultipleQueryResults(results,
                        currentSubTitle)
            for row in qryResultRows:
                categoryName = row[0]
                categoryCount = row[1]
                if len(row) > 3:
                    categoryCount = row[2].replace('KB', '')
                if dbName is None or dbName == categoryName:
                    resultData = FBDPDashboardData.ResultData(
                            categoryName=categoryName, count=categoryCount,
                            threshold=None, recommendedActions='')
                    resultDataList.append(resultData)
        return resultDataList

    def processQueryResults(self, qryResultRowsList, currentSubTitle):

        if self.hasEvalTimeTag():
            resultDataList = self._processQueryResultsWithEvalTimeTag(
                    qryResultRowsList, currentSubTitle)
        elif self.hasEvalAcmTag():
            resultDataList = self._processQueryResultsWithEvalAcmTag(
                    qryResultRowsList, currentSubTitle)
        elif self.hasMultipleResults():
            resultDataList = self._processMultipleQueryResults(
                    qryResultRowsList, currentSubTitle)
        else:
            resultDataList = self._processQueryResultsWithNoEvalTag(
                    qryResultRowsList, currentSubTitle)
        return resultDataList

    def recommendChartType(self):

        if self.hasEvalTimeTag():
            chartType = FBDPDashboardData.CHART_TYPE_PLOT
        elif self.hasEvalAcmTag():
            chartType = FBDPDashboardData.CHART_TYPE_BAR
        elif self.hasTableTag():
            chartType = FBDPDashboardData.CHART_TYPE_BAR
        elif self.hasMultipleResults():
            chartType = FBDPDashboardData.CHART_TYPE_BAR
        else:
            chartType = FBDPDashboardData.CHART_TYPE_PIE
        return chartType

    def getDrillDownQueryCondition(self, drillDownCategoryName,
            existingQueryCondition):

        drillDownCategoryName = str(drillDownCategoryName)
        categoryNameList = self.__querySpec['Category Name']
        resultCondList = self.__querySpec['Result Condition']
        newQueryCondition = ''

        for idx in range(len(categoryNameList)):
            categoryName = categoryNameList[idx]
            result_condition = resultCondList[idx]
            if drillDownCategoryName == categoryName:
                if existingQueryCondition:
                    newQueryCondition = ''.join([existingQueryCondition,
                            ' and ', result_condition])
                else:
                    newQueryCondition = result_condition
                return newQueryCondition
            elif '{0}' in result_condition:
                existingQueryCondition = ''.join([existingQueryCondition,
                        ' and ', result_condition])
                if TAG_ACM_PORTFOLIO in categoryName:
                    obj = self.__acmProxy.getFPhysicalPortfolioByName(
                            drillDownCategoryName)
                    drillDownCategoryName = obj.Oid()

                if TAG_ACM_INSTRUMENT in categoryName:
                    obj = self.__acmProxy.getFInstrumentByName(
                            drillDownCategoryName)
                    drillDownCategoryName = obj.Oid()

                if TAG_ACM_PARTY in categoryName:
                    obj = self.__acmProxy.getFPartyByName(
                            drillDownCategoryName)
                    drillDownCategoryName = obj.Oid()

                if TAG_ACM_INS_TYPE_ENUM in categoryName:
                    enumObj = self.__acmProxy.getFEnumerationInsType()
                    drillDownCategoryName = str(enumObj.Enumeration(
                            drillDownCategoryName))

                condition = existingQueryCondition.format(
                        drillDownCategoryName)
                newQueryCondition = condition
                return newQueryCondition
        return newQueryCondition
