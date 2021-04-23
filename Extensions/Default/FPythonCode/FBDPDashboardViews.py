""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/bdp_dashboard/FBDPDashboardViews.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
import collections
import json


import acm


import FBDPDashboardData
import FBDPDashboardDefaultConfig
import FBDPDashboardQuery
import FBDPDashboardUtil


_JSON_DEFAULT_ENCODING = 'latin_1'


class UIModelInterface(object):
    """
    This interface descript what the model need to implement.
    """
    def loadConfig(self, path):

        raise NotImplementedError('To be implemented in the derived class.')

    def saveConfig(self, path):

        raise NotImplementedError('To be implemented in the derived class.')

    def switchViewOnConfig(self, viewType, displayFunc):

        raise NotImplementedError('To be implemented in the derived class.')

    def switchViewOnPortSheet(self, viewType, selectedItem, displayFunc):

        raise NotImplementedError('To be implemented in the derived class.')

    def goBack(self, displayFunc):

        raise NotImplementedError('To be implemented in the derived class.')

    def drillDown(self, drillDownCategoryName, displayFunc):

        raise NotImplementedError('To be implemented in the derived class.')

    def updateCurrentView(self, displayFunc):

        raise NotImplementedError('To be implemented in the derived class.')

    def refreshCurrentView(self, displayFunc):

        raise NotImplementedError('To be implemented in the derived class.')

    def updateWithSheetSelection(self, selectedItem, displayFunc):

        raise NotImplementedError('To be implemented in the derived class.')

    def getViewType(self):

        raise NotImplementedError('To be implemented in the derived class.')

    def getViewLevel(self):

        raise NotImplementedError('To be implemented in the derived class.')


class _ViewLevel(object):

    def __init__(self, querySpec, qryCond, subTitle, qryResultCache):

        self.__qryProc = FBDPDashboardQuery.QueryProcessor(querySpec)
        self.__qryCond = qryCond
        self.__subTitle = subTitle
        self.__qryResultCache = qryResultCache
        self.__resultDataList = None

    def getLevelName(self):

        return self.__qryProc.getName()

    def getResultDataList(self):

        return self.__resultDataList

    def getSubTitle(self):

        return self.__subTitle

    def getChartType(self):

        return self.__qryProc.recommendChartType()

    def getDrillDownSubTitle(self, drillDownCategoryName):

        newSubTitlePart = '{0} = {1}  '.format(self.getLevelName(),
                drillDownCategoryName)
        return self.__subTitle + newSubTitlePart

    def getDrillDownQueryCondition(self, drillDownCategoryName):

        return self.__qryProc.getDrillDownQueryCondition(drillDownCategoryName,
                self.__qryCond)

    def getUnitDescription(self):

        return self.__qryProc.getUnitDescription()

    def updateViewLevelResult(self, forceRefresh):

        qryStmts = self.__qryProc.buildQueryStatements(self.__qryCond)
        strQryStmts = str(qryStmts)
        if not forceRefresh and strQryStmts in self.__qryResultCache:
            self.__resultDataList = self.__qryResultCache[strQryStmts]
            return
        qryResultRowsList = self.__qryProc.runQueryStatements(qryStmts)
        resultDataList = self.__qryProc.processQueryResults(qryResultRowsList,
                    self.__subTitle)

        self.__resultDataList = resultDataList
        self.__qryResultCache[strQryStmts] = resultDataList

    def getQueryStatements(self):
        qryStmts = self.__qryProc.buildQueryStatements(self.__qryCond)
        return str(qryStmts)

class _ConfigDataListBuilder(object):

    def __init__(self, viewDetail):

        self.__querySpecList = viewDetail

    @staticmethod
    def _buildActionDescription(actionSpecList):

        if not actionSpecList:
            return ''
        actionStrList = []
        for actionSpec in actionSpecList:
            descFmt = actionSpec['Description']
            maxCount = actionSpec['MaxCount']
            actionStrList.append(descFmt.format(maxCount))
        return ''.join(actionStrList)

    def build(self):

        configDataList = []
        for querySpec in self.__querySpecList:
            name = querySpec['Name']
            desc = querySpec['Description']
            actionSpecList = querySpec['Action']
            actionDesc = self._buildActionDescription(actionSpecList)
            configDataList.append(FBDPDashboardData.ConfigData(name=name,
                    description=desc, actionDescription=actionDesc))
        return configDataList


class _ViewHandler(object):

    def __init__(self, viewType, viewName, viewDetail, qryResultCache):

        self.__viewType = viewType
        self.__viewName = viewName
        self.__querySpecList = viewDetail  # details are the query specs
        self.__configDataList = _ConfigDataListBuilder(viewDetail).build()
        self.__qryResultCache = qryResultCache
        self.__viewLevelStack = self._initViewLevelStack()

    def _initViewLevelStack(self):

        viewLevel0 = _ViewLevel(self.__querySpecList[0], qryCond='',
                subTitle='', qryResultCache=self.__qryResultCache)
        return [viewLevel0]

    def getViewLevelNum(self):

        return len(self.__viewLevelStack) - 1  # 0-based

    def _getCurrentViewLevel(self):

        return self.__viewLevelStack[-1]

    def getUnitDescription(self):

        return self._getCurrentViewLevel().getUnitDescription()

    def getConfigDataList(self):

        return self.__configDataList

    def getCurrentViewLevelName(self):

        return self._getCurrentViewLevel().getLevelName()

    def go_BackResult(self):

        if len(self.__viewLevelStack) > 1:
            self.__viewLevelStack.pop()

    def get_DisplayResult(self):

        currentViewLevel = self._getCurrentViewLevel()
        resultDataList = currentViewLevel.getResultDataList()
        subTitle = currentViewLevel.getSubTitle()
        chartType = currentViewLevel.getChartType()
        return resultDataList, subTitle, chartType

    def get_viewLabel(self):

        return ''.join([self.__viewType.upper(), ': ', self.__viewName, ' : ',
                self.getCurrentViewLevelName()])

    def reset_currentPosition(self):

        self.__viewLevelStack = self._initViewLevelStack()

    def updateCurrentView(self, refresh=False):

        self._getCurrentViewLevel().updateViewLevelResult(forceRefresh=refresh)

    def drillDown(self, drillDownCategoryName):

        if len(self.__viewLevelStack) >= len(self.__querySpecList):
            print('No further drill down configured')
            return
        if drillDownCategoryName == FBDPDashboardQuery.CATEGORY_NAME_OTHERS:
            print('No drill down implemented for Others category yet.')
            return
        elif drillDownCategoryName == FBDPDashboardQuery.CATEGORY_NAME_NIL:
            print('No drill down implemented for \'Nil\' category.')
            return
        currentViewLevel = self._getCurrentViewLevel()
        drillDownSubTitle = currentViewLevel.getDrillDownSubTitle(
                drillDownCategoryName)
        drillDownQueryCondition = currentViewLevel.getDrillDownQueryCondition(
                drillDownCategoryName)
        drillDownLevelNum = len(self.__viewLevelStack)
        drillDownViewLevel = _ViewLevel(self.__querySpecList[
                drillDownLevelNum], drillDownQueryCondition, drillDownSubTitle,
                self.__qryResultCache)
        self.__viewLevelStack.append(drillDownViewLevel)
        self.updateCurrentView()


class _ViewCollectionHandler(object):

    def __init__(self, viewType, viewCollection, qryResultCache):

        self.__viewType = viewType
        self.__viewNameToDetailMap = viewCollection
        self.__qryResultCache = qryResultCache
        self.__currentViewName = None
        if not self.__currentViewName:
            self.setDefaultViewCurrent()

    def setDefaultViewCurrent(self):

        for viewName in self.__viewNameToDetailMap:
            if 'DEFAULT' in viewName.upper():
                self.__currentViewName = viewName
                return
        raise ValueError('None of the view name in the view collection '
                'contains the word "default".')

    def getCurrentViewHandler(self):

        viewDetail = self.__viewNameToDetailMap[self.__currentViewName]
        return _ViewHandler(viewType=self.__viewType,
                viewName=self.__currentViewName, viewDetail=viewDetail,
                qryResultCache=self.__qryResultCache)


def _unicodeToStr(obj):
    """
    Recursively iterate through dict and list.  For each unicode found, convert
    it into string.
    """
    if isinstance(obj, dict):
        return dict((_unicodeToStr(k), _unicodeToStr(v)) for (k, v)
                in obj.iteritems())
    if isinstance(obj, list):
        return [_unicodeToStr(e) for e in obj]
    if isinstance(obj, unicode):
        return obj.encode('ascii', 'ignore')
    return obj


def convertDbTableNameToViewType(dbTableName):

    mapping = FBDPDashboardDefaultConfig.DB_TABLE_NAME_TO_VIEW_TYPE_MAP
    if dbTableName in mapping:
        return mapping[dbTableName]
    print(('No view had been configured for database table "{0}".'.format(
            dbTableName)))
    return None


class _Configurator(object):

    def __init__(self, path='',
            configuration=FBDPDashboardDefaultConfig.DEFAULT_CONFIG):

        self._configuration = {}
        if path:
            self.load(path)
        else:
            self._configuration = configuration

    def load(self, path):
        """
        Path should be a case-normalized path for Windows.
        """
        with open(path) as fp:
            dct = json.load(fp, encoding=_JSON_DEFAULT_ENCODING)
        dct = _unicodeToStr(dct)
        self._configuration = dct

    def save(self, path):
        """
        Path should be a case-normalized path for Windows.
        """
        with open(path, 'w') as fp:
            json.dump(self._configuration, fp, ensure_ascii=True,
                    sort_keys=True, indent=4, separators=(',', ': '),
                    encoding=_JSON_DEFAULT_ENCODING)

    def getViewTypes(self):

        return self._configuration.keys()

    def getViewCollection(self, viewType):

        if viewType not in self._configuration:
            raise AttributeError('Invalid configuration: View type "{0}" '
                    'not found.'.format(viewType))
        return self._configuration[viewType]


class _LimitProcessor(object):

    def __init__(self, acmProxy=FBDPDashboardUtil.AcmProxy()):

        self.__acmProxy = acmProxy

    def getLimitsInRow(self, row):

        spec = acm.Limits.CreateTreeSpecification(row)
        return acm.Limits.FindByTreeSpecification(spec)

    @staticmethod
    def _isLimitForColumn(acmLimit, columnName):

        return FBDPDashboardUtil.getLimitColumnName(acmLimit) == columnName

    def getLimitsMinThresholdValue(self, columnName, row):

        if columnName is None:
            return None
        acmLimits = [acmLm for acmLm in self.getLimitsInRow(row) if
                self._isLimitForColumn(acmLm, columnName)]
        if not acmLimits:
            return None
        thresholds = [acmLimit.Threshold() for acmLimit in acmLimits]
        return min(thresholds)


def _sumValList(valList):

    if not valList:
        return 0
    return sum(valList)


def _minThresList(thresList):

    if not thresList:
        return None
    if all(t is None for t in thresList):
        return None
    return min(t for t in thresList if t is not None)


class DefaultUIModel(UIModelInterface):

    def __init__(self, configurator=_Configurator()):

        self.__configurator = configurator
        self.__currentViewHandler = None
        self.__currentViewType = None
        self.__qryResultCache = {}
        self.__limitProc = _LimitProcessor()
        self.__resultsFromFile = None

    def loadConfig(self, path):

        prevViewType = self.__currentViewType
        try:
            configurator = _Configurator(path)
        except (IOError, AttributeError) as e:
            print(("Could not load config from {0}: {1}".format(path, e)))
            return
        # Use the previous view if it is still available, or find something
        availableViewTypes = configurator.getViewTypes()
        if prevViewType and prevViewType in availableViewTypes:
            newViewType = prevViewType
        elif availableViewTypes:
            newViewType = availableViewTypes[0]
        else:
            print("No view is found in the new configuration.")
            return
        # Jump into the view
        self.__init__(configurator)
        self._initIntoViewType(newViewType)

    def saveConfig(self, path):

        try:
            self.__configurator.save(path)
        except IOError as e:
            print("Could not write config to {0}: {1}".format(path, e))

    def exportToFile(self, path):
        try:
            with open(path, 'w') as fp:
                json.dump(self.__qryResultCache, fp, ensure_ascii=True,
                    sort_keys=True, indent=4, separators=(',', ': '),
                    encoding=_JSON_DEFAULT_ENCODING)
        except IOError as e:
            print("Could not write config to {0}: {1}".format(path, e))

    def loadFromFile(self, path):
        """
        Path should be a case-normalized path for Windows.
        """
        with open(path) as fp:
            dct = json.load(fp, encoding=_JSON_DEFAULT_ENCODING)
        dct = _unicodeToStr(dct)
        self.__resultsFromFile = dct
        print(self.__resultsFromFile)

    def _initIntoViewType(self, viewType):

        viewCollection = self.__configurator.getViewCollection(viewType)
        viewCollHndlr = _ViewCollectionHandler(viewType,
                viewCollection, self.__qryResultCache)
        self.__currentViewHandler = viewCollHndlr.getCurrentViewHandler()
        self.__currentViewType = viewType
        self.__currentViewHandler.reset_currentPosition()
        self.__currentViewHandler.updateCurrentView(refresh=False)

    def switchViewOnConfig(self, viewType, displayFunc):

        self._initIntoViewType(viewType)
        uiData = self._prepareQueryTriggeredUiData()
        displayFunc(uiData)

    def switchViewOnPortSheet(self, viewType, selectedItem, displayFunc):

        self.__currentViewType = viewType
        self.updateWithSheetSelection(selectedItem, displayFunc)

    def goBack(self, displayFunc):

        self.__currentViewHandler.go_BackResult()
        uiData = self._prepareQueryTriggeredUiData()
        displayFunc(uiData)

    def drillDown(self, drillDownCategoryName, displayFunc):

        self.__currentViewHandler.drillDown(drillDownCategoryName)
        uiData = self._prepareQueryTriggeredUiData()
        displayFunc(uiData)

    def updateCurrentView(self, displayFunc):

        self.__currentViewHandler.updateCurrentView(refresh=False)
        uiData = self._prepareQueryTriggeredUiData()
        displayFunc(uiData)

    def refreshCurrentView(self, displayFunc):

        self.__currentViewHandler.updateCurrentView(refresh=True)
        uiData = self._prepareQueryTriggeredUiData()
        displayFunc(uiData)

    def _getSheetUpdateColumnName(self):

        if self.__currentViewType in ('database', 'trades'):
            columnName = 'Trade Count'
        elif self.__currentViewType == 'instruments':
            columnName = 'Position Total Count'
        elif self.__currentViewType == 'prices':
            columnName = 'Position Historical Price Count'
        else:
            columnName = None
        return columnName

    def _getGrouperNameForChainedGrouper(self, chainedGrouper,
            grouperOnLevelStringKey):

        # Find the target grouper level, where
        #    target level num = 0       if the chained grouper itself matched.
        #    target level num = N + 1   if the level N grouper matched.
        targetGpLvllNum = None
        groupers = chainedGrouper.Groupers()
        numGroupers = groupers.Size()
        if chainedGrouper.StringKey() == grouperOnLevelStringKey:
            targetGpLvllNum = 0
        else:
            for index in range(numGroupers):
                if groupers[index].StringKey() == grouperOnLevelStringKey:
                    targetGpLvllNum = index + 1
                    break
        # Now find the corresponding grouper name
        if targetGpLvllNum is None:
            gpName = 'No Grouper matched'
        elif (targetGpLvllNum >= numGroupers or
                groupers[targetGpLvllNum].IsKindOf(acm.FDefaultGrouper)):
            gpName = 'Instrument Name'
        else:
            gpName = groupers[targetGpLvllNum].StringKey()
        return gpName

    def _getGrouperName(self, selectedItem, gp):

        try:
            if gp.IsKindOf(acm.FDefaultGrouper):
                return 'Instrument Name'

            grouperOnLevel = selectedItem.GrouperOnLevel()
            grouperOnLevelStringKey = grouperOnLevel.StringKey()

            if gp.IsKindOf(acm.FChainedGrouper):
                return self._getGrouperNameForChainedGrouper(gp,
                        grouperOnLevelStringKey)

            if selectedItem.IsKindOf(acm.FPortfolioInstrumentAndTrades):
                return grouperOnLevel.StringKey()

        except Exception as e:
            print('Got Exception !')
            print(e)
            return ''
        return 'Instrument Name'

    def updateWithSheetSelection(self, selectedItem, displayFunc):

        columnName = self._getSheetUpdateColumnName()
        try:
            builder = selectedItem.Builder()
            grouper = builder.Grouper()
            calcSpace = acm.FCalculationSpace('FPortfolioSheet')
            if selectedItem.IsKindOf(acm.FPortfolioInstrumentAndTrades):
                port = builder.Portfolio()
                selectedNode = calcSpace.InsertItem(port)
                selectedNode.ApplyGrouper(grouper)
            else:
                selectedNode = calcSpace.InsertItem(selectedItem)

            calcSpace.Refresh()
            rowNameToValAndThresMap = {}
            if selectedNode.Iterator().HasChildren():
                child = selectedNode.Iterator().FirstChild()
                while child:
                    node = child.Tree()
                    rowName = node.StringKey()
                    val = calcSpace.CreateCalculation(node, columnName).Value()
                    val = FBDPDashboardUtil.tryCast(int, val, default=0)
                    thres = self.__limitProc.getLimitsMinThresholdValue(
                            columnName, node.Item())
                    rowNameToValAndThresMap[rowName] = (val, thres)
                    child = child.NextSibling()
            else:
                rowName = selectedNode.StringKey()
                val = calcSpace.CreateCalculation(selectedNode,
                        columnName).Value()
                val = FBDPDashboardUtil.tryCast(int, val, default=0)
                rowNameToValAndThresMap[rowName] = (val, None)

        except Exception as e:
            print('Got Exception !')
            print(e)
            return

        chartType, resultDataList = self._processSheetUpdateRowNameValAndThres(
                rowNameToValAndThresMap)
        viewLabel = ''.join([self.__currentViewType.upper(),
                ':Selected Item =', selectedNode.StringKey()])
        grouperName = self._getGrouperName(selectedItem, grouper)

        uiData = FBDPDashboardData.UIData(resultDataList=resultDataList,
                configDataList=self._getConfigDataList(),
                XAxisLabel=grouperName,
                YAxisLabel=columnName,
                subTitle=columnName,
                chartType=chartType,
                viewType=self.__currentViewType,
                viewLevelNum=0,
                viewLabel=viewLabel
                )
        displayFunc(uiData)

    def _processSheetUpdateRowNameValAndThres(self, rowNameToValAndThresMap):

        strDateToValAndThresListMap = collections.defaultdict(list)
        for rowName in rowNameToValAndThresMap:
            if not FBDPDashboardUtil.isDate(rowName):
                break
            strDate = FBDPDashboardUtil.strDateTimeToStrDate(rowName)
            valAndThres = rowNameToValAndThresMap[rowName]
            strDateToValAndThresListMap[strDate].append(valAndThres)

        if strDateToValAndThresListMap:
            chartType = FBDPDashboardData.CHART_TYPE_PLOT
            resultDataList = []
            for strDate in sorted(strDateToValAndThresListMap.iterkeys()):
                valAndThresList = strDateToValAndThresListMap[strDate]
                valList = [vt[0] for vt in valAndThresList]
                thresList = [vt[1] for vt in valAndThresList]
                count = _sumValList(valList)
                thres = _minThresList(thresList)
                resultData = FBDPDashboardData.ResultData(
                        categoryName=strDate, count=count, threshold=thres,
                        recommendedActions=('Threshold = {0}'.format(thres)))
                resultDataList.append(resultData)
        else:
            chartType = FBDPDashboardData.CHART_TYPE_BAR
            resultDataList = []
            for rowName in sorted(rowNameToValAndThresMap.iterkeys()):
                val, thres = rowNameToValAndThresMap[rowName]
                resultData = FBDPDashboardData.ResultData(
                        categoryName=rowName, count=val, threshold=thres,
                        recommendedActions=('Threshold = {0}'.format(thres)))
                resultDataList.append(resultData)
        return chartType, resultDataList

    def _prepareQueryTriggeredUiData(self):

        resultDataList, subTitle, chartType = (
                self.__currentViewHandler.get_DisplayResult())
        configDataList = self._getConfigDataList()
        XAxisLabel = self.__currentViewHandler.getCurrentViewLevelName()
        YAxisLabel = self.__currentViewHandler.getUnitDescription()
        viewType = self.__currentViewType
        viewLevelNum = self.__currentViewHandler.getViewLevelNum()
        viewLabel = self.__currentViewHandler.get_viewLabel()
        uiData = FBDPDashboardData.UIData(resultDataList=resultDataList,
                configDataList=configDataList, XAxisLabel=XAxisLabel,
                YAxisLabel=YAxisLabel,
                subTitle=subTitle, chartType=chartType, viewType=viewType,
                viewLevelNum=viewLevelNum, viewLabel=viewLabel)
        return uiData

    def _getConfigDataList(self):

        return self.__currentViewHandler.getConfigDataList()

    def getViewType(self):

        return self.__currentViewType

    def getViewLevel(self):

        return self.__currentViewHandler.getViewLevelNum()
