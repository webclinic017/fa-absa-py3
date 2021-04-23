"""-------------------------------------------------------------------------------------------------------
MODULE
    FPortfolioProfiler

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Profile a portfolio given a configured grouper, set of columns and scenario. Outputs
    statistics and performance figures in log or CSV format.

-------------------------------------------------------------------------------------------------------"""
# pylint: disable-msg=R0902,R0903,R0913

from collections import defaultdict, deque, namedtuple
from contextlib import contextmanager
import datetime
import itertools
import os

import acm
import FLogger
import FRunScriptGUI
import FUxCore
try:
    # Compatibility with pre-2012.2 releases
    MenuItemBase = FUxCore.MenuItem
except AttributeError:
    MenuItemBase = object

logger = FLogger.FLogger.GetLogger(__name__)

SUPPORTED_PORTFOLIO_CLASSES = [acm.FPhysicalPortfolio, acm.FCompoundPortfolio, 
         acm.FTradeSelection, acm.FStoredASQLQuery]


def CreatePortfolioProfilerMenuItem(eii):
    return PortfolioProfilerMenuItem(eii)

def RunPortfolioProfiler(eii):
    # Compatibility with pre-2012.2 releases
    menuItem = PortfolioProfilerMenuItem(eii.ExtensionObject())
    if menuItem and menuItem.Applicable() and menuItem.Enabled():
        menuItem.Invoke(eii)


class ReportableItemBase(object):

    def DisplayValues(self):
        # pylint: disable-msg=R0201
        return []

    def __str__(self):
        return '\n'.join(['%s:\t%s' % (attr, value) for 
            attr, value in self.DisplayValues()])

    @classmethod
    def _MegabytesString(cls, byteValue):
        return cls._FloatString(float(byteValue) / (1000 * 1024), 2)

    @staticmethod
    def _FloatString(floatValue, decimals=6):
        formatString = '%%0.0%df' % decimals
        return formatString % floatValue


class PerformanceSnapshot(ReportableItemBase):

    def __init__(self, name='', resetCounters=False):
        super(PerformanceSnapshot, self).__init__()
        if resetCounters:
            self._ResetCounters()
        self.name = name
        self.time = datetime.datetime.now()
        self.virtualMemory = acm.Memory.VirtualMemorySize()
        self.evaluators = acm.FCache.Select01('.StringKey = evaluators', '').Size()
        self.collections = acm.Memory.GcNumberOfCollections()
        self.cpuUser = os.times()[0]
        self.cpuSystem = os.times()[1]
        self.gcHeapSize = acm.Memory.GcHeapSize()
        self.gcFree = acm.Memory.GcNumberOfFreeBytes()

    def Name(self, name=None):
        if name is not None:
            self.name = name
        return self.name

    def DisplayValues(self):
        return [
            ('Name', self.Name()),
            ('Time', str(self.time)),
            ('Evaluator Count', str(self.evaluators)),
            ('Garbage Collection Count', str(self.collections)),
            ('CPU Time (user)', str(self.cpuUser)),
            ('CPU Time (system)', str(self.cpuSystem)),
            ('Virtual Memory (Mb)', self._MegabytesString(self.virtualMemory)),
            ('GC Total Memory (Mb)', self._MegabytesString(self.gcHeapSize)),
            ('GC Used Memory (Mb)', self._MegabytesString(self.gcHeapSize - self.gcFree)),
            ]

    @staticmethod
    def _ResetCounters():
        evalcache = acm.FCache.Select01('.StringKey = "evaluators"', '')
        ebcache = acm.FCache.Select01('.StringKey = "evaluator builders"', '')
        for eb in ebcache.Contents():
            eb.Reset()
        acm.Memory.GcWorldStoppedCollect()
        evalcache.Statistics()
        ebcache.Statistics()

    def __sub__(self, other):
        return PerformanceDelta(other, self)


class PerformanceDelta(ReportableItemBase):
    # pylint: disable-msg=E1101

    def __init__(self, snapshotBefore, snapshotAfter):
        super(PerformanceDelta, self).__init__()
        self._before = snapshotBefore
        self._after = snapshotAfter
        beforeValues = vars(self.Before())
        afterValues = vars(self.After())
        for attribute, afterValue in afterValues.items():
            try:
                setattr(self, attribute, afterValue - beforeValues[attribute])
            except TypeError:
                pass

    def Before(self):
        return self._before

    def After(self):
        return self._after
    
    def DisplayValues(self, displayUnchanged=False):
        # pylint: disable-msg=W0221
        attrValuePairs = [
            ('Event', self.After().Name()),
            ('Time', str(self.time)),
            ('Time (secs)', str(self._TotalSeconds(self.time))),
            ('Evaluator Count', str(self.evaluators)),
            ('Garbage Collection Count', str(self.collections)),
            ('CPU Time Total', str(datetime.timedelta(
                    seconds=(self.cpuUser + self.cpuSystem)))),
            ('CPU Time Total (secs)', self._FloatString(self.cpuUser + self.cpuSystem)),
            ('CPU Time (user)', self._FloatString(self.cpuUser)),
            ('CPU Time (system)', self._FloatString(self.cpuSystem)),
            ('Virtual Memory (Mb)', self._MegabytesString(self.virtualMemory)),
            ('GC Total Memory (Mb)', self._MegabytesString(self.gcHeapSize)),
            ('GC Used Memory (Mb)', self._MegabytesString(self.gcHeapSize - self.gcFree)),
            ]
        return [(attr, value) for attr, value in attrValuePairs if 
                displayUnchanged or value not in ('0', '0.00', '0.000000', '0:00:00')]

    @staticmethod
    def _TotalSeconds(td):
        return float((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)) / 10**6


class MeasuredEvent(object):

    def __init__(self, event, resetCounters=False):
        logger.info('%s', event)
        self._event = event
        self._startSnapshot = PerformanceSnapshot(self._event, resetCounters)

    def Stop(self):
        return PerformanceSnapshot(self._event) - self._startSnapshot


class ReportDefinition(ReportableItemBase):

    def __init__(self, portfolio, grouperName=None, groupingLevels=None, 
            columnIds=None, scenarioName=None, evaluationLevel=1):
        super(ReportDefinition, self).__init__()
        self.portfolio = portfolio
        self.grouper = grouperName or 'Default'
        self.groupingLevels = groupingLevels or list()
        self.columns = columnIds or list()
        self.scenario = scenarioName
        self.evaluationLevel = evaluationLevel
        self.time = datetime.datetime.now()

    def DisplayValues(self):
        values = [
            ('Portfolio', self.portfolio.Name()), 
            ('Portfolio Type', self.portfolio.Class().Name()),
            ('Report Time', str(self.time)),
            ('Grouper', self.grouper), 
            ]
        for i, grouper in enumerate(self.groupingLevels):
            values.append(('Grouping Level ' + str(i+1), grouper))
        for i, column in enumerate(self.columns):
            values.append(('Column ' + str(i+1), column))
        if self.scenario:
            values.append(('Scenario', self.scenario))
        values.append(('Cell Evaluation', ('All levels' if self.evaluationLevel >= 999
                else 'To level ' + str(self.evaluationLevel))))
        return values


class PortfolioStatistics(ReportableItemBase):

    class InstrumentType(object):
        def __init__(self):
            self.instruments = set()
            self.positions = defaultdict(int)
            self.trades = defaultdict(int)

    def __init__(self):
        super(PortfolioStatistics, self).__init__()
        self.nodes = defaultdict(int)
        self.instruments = defaultdict(self.InstrumentType)

    def DisplayValues(self):
        values = [
            ('Total Instrument Count', str(sum(
                    [len(i.instruments) for i in self.instruments.values()]))),
            ('Total Trade Count', str(sum(itertools.chain.from_iterable(
                    [i.trades.values() for i in self.instruments.values()])))), 
            ('Total Position Count', str(sum(itertools.chain.from_iterable(
                    [i.positions.values() for i in self.instruments.values()])))),
            ('Live Position Count', str(sum(
                    [i.positions['Live'] for i in self.instruments.values()]))),
            ('Total Node Count', str(sum([c for c in self.nodes.values()]))),
            ]
        for level, count in sorted(self.nodes.items()):
            values.append((level + ' Node Count', str(count)))
        parentNodeCount = None
        for level, count in sorted(self.nodes.items()):
            if parentNodeCount:
                values.append(('Average ' + level + ' Node Count',
                    self._FloatString(float(count) / parentNodeCount, 2)))
            parentNodeCount = count
        return values

    def InstrumentTypeStatistics(self, delimiter='\t'):
        values = []
        positionTypes = ['Live', 'Closed', 'Expired']
        if self.instruments:
            values.append(delimiter.join(['Instrument Type', ] + 
                [posType + ' Positions' for posType in positionTypes] + ['Total Positions', ] +
                [posType + ' Trades' for posType in positionTypes] + ['Total Trades', ]))
            totals = defaultdict(int)
            for insType, stats in self.instruments.items():
                counts = ([insType, ] + 
                        [stats.positions[posType] for posType in positionTypes] +
                        [sum([c for c in stats.positions.values()]), ] + 
                        [stats.trades[posType] for posType in positionTypes] + 
                        [sum([c for c in stats.trades.values()]), ])
                values.append(delimiter.join([str(c) for c in counts]))
                for idx, count in enumerate(counts[1:]):
                    totals[idx] += count
            values.append(delimiter.join(['TOTAL', ] + [str(c) for c in totals.values()]))
        return values

    def __str__(self):
        return super(PortfolioStatistics, self).__str__() + '\n\n' + \
                '\n'.join(self.InstrumentTypeStatistics())


class PortfolioPerformanceReport(object):

    def __init__(self, report, statistics=None, events=None):
        self._report = report
        self._statistics = statistics
        self._events = events

    def ReportDefinition(self):
        return self._report

    def PortfolioStatistics(self):
        return self._statistics

    def PerformanceEvents(self):
        return self._events

    def GetLoggedEvents(self, reportTotalDelta=False):
        lines = []
        lines.append('PORTFOLIO REPORT\n' + '-' * 80)
        lines.append(str(self.ReportDefinition()))
        if self.PortfolioStatistics():
            lines.append('PORTFOLIO STATISTICS\n' + '-' * 80)
            lines.append(str(self.PortfolioStatistics()))
        if self.PerformanceEvents():
            lines.append('PERFORMANCE MEASUREMENTS\n' + '-' * 80)
            for delta in self.PerformanceEvents():
                lines.append(str(delta))
            if reportTotalDelta:
                firstSnapshot = self.PerformanceEvents()[0].Before()
                lastSnapshot = self.PerformanceEvents()[-1].After()
                totalDelta = lastSnapshot - firstSnapshot
                totalDelta.After().Name('Start to finish')
                lines.append(str(totalDelta))
        return '\n\n'.join(lines)

    def GetCommaSeparatedValues(self, delimiter=','):
        lines = []
        lines.append('PORTFOLIO REPORT\n' + '-' * 80)
        lines.append(self._GetCommaSeparatedValues(
                self.ReportDefinition().DisplayValues(), delimiter))
        if self.PortfolioStatistics():
            lines.append('PORTFOLIO STATISTICS\n' + '-' * 80)
            lines.append(self._GetCommaSeparatedValues(
                    self.PortfolioStatistics().DisplayValues(), delimiter))
            lines.append('\n'.join(
                    self.PortfolioStatistics().InstrumentTypeStatistics(delimiter)))
        if self.PerformanceEvents():
            rows = []
            for delta in self.PerformanceEvents():
                if not rows:
                    rows.append([values[0] for values in delta.DisplayValues(True)])
                rows.append([values[1] for values in delta.DisplayValues(True)])                    
            lines.append('PERFORMANCE MEASUREMENTS\n' + '-' * 80)
            lines.append(self._GetCommaSeparatedValues(rows, delimiter))
        return '\n\n'.join(lines)

    @staticmethod
    def _GetCommaSeparatedValues(rows, delimiter=','):
        try:
            import cStringIO as Python3CompatibleIO
        except ImportError:
            import io as Python3CompatibleIO
        import csv
        output = Python3CompatibleIO.StringIO()
        writer = csv.writer(output, delimiter=delimiter, 
                quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerows(rows)
        return output.getvalue()


class FPortfolioProfiler(object):

    def __init__(self, portfolio, grouper=None, columnIds=None, scenario=None):
        self._portfolio = portfolio
        self._grouperName = grouper or 'Default'
        self._columnIds = columnIds or list()
        self._scenarioName = scenario
        if not self._portfolio:
            raise ValueError('Portfolio must be defined')

    def Run(self, collectStatistics=True, cellEvaluationLevel=1):
        with self._CalculationSpace() as calcSpace:
            portfolio = self._GetReportDefinition(cellEvaluationLevel)
            logger.info('Measuring portfolio performance')
            events = self._GetPerformanceDeltas(calcSpace, cellEvaluationLevel)
            if collectStatistics:
                logger.info('Gathering portfolio statistics')
                statistics = self._GetPortfolioStatistics(calcSpace)
            else:
                statistics = None
            return PortfolioPerformanceReport(portfolio, statistics, events)

    @staticmethod
    @contextmanager
    def _CalculationSpace():
        collection = acm.FCalculationSpaceCollection()
        try:
            calcSpace = collection.GetSpace('FPortfolioSheet', acm.GetDefaultContext())
            yield calcSpace
        finally:
            collection.Clear()

    def _GetReportDefinition(self, evaluationLevel):
        groupers = self._GetGrouper(self._grouperName)
        if groupers:
            if groupers.IsKindOf(acm.FChainedGrouper):
                groupers = [g.Label() or g.DisplayName() for g in groupers.Groupers()]
            else:
                groupers = [groupers.Label() or g.DisplayName()]
        return ReportDefinition(
                portfolio=self._portfolio, 
                grouperName=self._grouperName, 
                groupingLevels=groupers, 
                columnIds=self._columnIds, 
                scenarioName=self._scenarioName,
                evaluationLevel=evaluationLevel)

    def _GetPerformanceDeltas(self, calcSpace, maxTreeDepth):
        events = []
        event = MeasuredEvent('Inserting portfolio "%s"' % self._portfolio.Name(), True)
        node = calcSpace.InsertItem(self._portfolio)
        calcSpace.Refresh()
        events.append(event.Stop())

        grouper = self._GetGrouper(self._grouperName)
        if not grouper:
            raise ValueError('Could not apply grouper ' + self._grouperName)
        if node and grouper:
            event = MeasuredEvent('Applying grouper "%s"' % self._grouperName)
            node.ApplyGrouper(grouper)
            calcSpace.Refresh()
            events.append(event.Stop())

        config = self._GetColumnConfiguration()
        treeNodes = self._TreeNodeItems(calcSpace, maxTreeDepth)
        for columnId in self._columnIds:
            event = MeasuredEvent('Adding column "%s"' % columnId)
            for _level, treeNode in treeNodes:
                try:
                    calcSpace.CalculateValue(treeNode, columnId, config)
                except StandardError as e:
                    logger.error('Error evaluating value for column "%s": %s', columnId, e)
            events.append(event.Stop())
        return events
    
    @staticmethod
    def _GetGrouper(name):
        grouper = acm.Risk().GetGrouperFromName(name)
        if not grouper:
            storedGroupers = acm.FStoredPortfolioGrouper.Select('')
            for storedGrouper in storedGroupers:
                if storedGrouper.Name() == name[:31]:
                    return storedGrouper.Grouper()
        return grouper

    def _GetColumnConfiguration(self):
        config = None
        if self._scenarioName:
            storedScenarios = acm.FStoredScenario.Select('name = ' + self._scenarioName)
            if storedScenarios and storedScenarios.Size() == 1:
                aspect = acm.FCalculationConfiguration()
                scenario = storedScenarios.First().Scenario()
                config = acm.Sheet.Column().ConfigurationFromScenario(scenario, aspect)
            else:
                logger.warn('Failed to load scenario "%s"', self._scenarioName)
        return config

    @classmethod
    def _GetPortfolioStatistics(cls, calcSpace):
        portfolioStats = PortfolioStatistics()
        for level, treeNode in cls._TreeNodeItems(calcSpace):
            rowItem = treeNode.Item()
            portfolioStats.nodes['Level ' + str(level)] += 1
            if cls._IsPositionNode(rowItem):
                positionType = 'Live'
                if cls._IsExpiredPosition(rowItem):
                    logger.debug('Position "%s" is expired', cls._PositionString(treeNode))
                    positionType = 'Expired'
                elif cls._IsClosedPosition(treeNode, calcSpace):
                    logger.debug('Position "%s" is closed', cls._PositionString(treeNode))
                    positionType = 'Closed'

                instrument = rowItem.Instrument()
                instrumentStats = portfolioStats.instruments[instrument.InsType()]
                instrumentStats.positions[positionType] += 1
                instrumentStats.trades[positionType] += rowItem.Trades().Size()
                instrumentStats.instruments.add(instrument)                    
                portfolioStats.instruments[instrument.InsType()] = instrumentStats
        return portfolioStats

    @staticmethod
    def _TreeNodeItems(calcSpace, maxDepth=999):
        def ParentNextSibling(nodeIter):
            parent = nodeIter.Parent()
            if parent:
                return parent.NextSibling() or ParentNextSibling(parent)
            return None
        nodes = []
        portfolioDepth = 0
        compoundPortfolioDepths = deque([portfolioDepth, ])
        iterator = calcSpace.RowTreeIterator().FirstChild()
        while iterator:
            # Count node depths from the portfolio level
            depth = iterator.Tree().Depth()
            rowTreeItem = iterator.Tree().Item()
            if (rowTreeItem.IsKindOf(acm.FPortfolioInstrumentAndTrades) and
                    rowTreeItem.Portfolio().IsKindOf(acm.FCompoundPortfolio)):
                compoundPortfolioDepths.append(depth)
            elif depth <= portfolioDepth and compoundPortfolioDepths:
                portfolioDepth = compoundPortfolioDepths.pop()

            depth -= portfolioDepth
            if depth > maxDepth:
                iterator = ParentNextSibling(iterator)
            else:
                nodes.append((depth, iterator.Tree()))
                iterator = iterator.FirstChild() or iterator.NextSibling() \
                            or ParentNextSibling(iterator)
        return nodes

    @staticmethod
    def _IsPositionNode(rowItem):
        return rowItem and rowItem.IsKindOf(acm.FSingleInstrumentAndTrades)

    @staticmethod
    def _IsExpiredPosition(rowItem):
        return rowItem and rowItem.IsExpired()

    @staticmethod
    def _IsClosedPosition(treeNodeItem, calcSpace):
        value = None
        try:
            value = calcSpace.CalculateValue(treeNodeItem, 'Portfolio Position')
            value = value.Number()
        except AttributeError:
            pass
        except RuntimeError as e:
            logger.error('Failed to evaluate position calculation: %s', e)
        return value is not None and value == 0

    @staticmethod
    def _PositionString(treeNodeItem):
        path = [str(i.Name() if hasattr(i, 'Name') else i) 
                for i in treeNodeItem.Item().Grouping().GroupingValues()]
        path.append(str(treeNodeItem.Item().Instrument().Name()))
        return ' / '.join(path)


class PortfolioProfilerMenuItem(MenuItemBase):

    AEL_TASK_NAME = 'Portfolio Profiler'
    
    def __init__(self, eii):
        self._eii = eii

    def Invoke(self, _eii):
        task = self._GetAelTask()
        task.Parameters(self._GetPortfolioParameters())
        acm.StartApplication('Run Script', task)

    def Applicable(self):
        if self._eii and hasattr(self._eii, 'ActiveSheet'):
            selection = self._eii.ActiveSheet().Selection()
            if selection:
                for rowObject in selection.SelectedRowObjects():
                    if rowObject.IsKindOf(acm.FPortfolioInstrumentAndTrades):
                        return True
        return False

    def Enabled(self):
        selection = self._eii.ActiveSheet().Selection()
        portfolio = self._GetPortfolioFromSelection(selection)
        return bool(portfolio and portfolio.Class() in SUPPORTED_PORTFOLIO_CLASSES)

    def _GetAelTask(self):
        task = acm.FAelTask[self.AEL_TASK_NAME]
        if not task:
            task = acm.FAelTask()
            task.Name(self.AEL_TASK_NAME)
            task.ModuleName(__name__)
            task.Commit()
        return task

    @staticmethod
    def _GetPortfolioFromSelection(selection):
        for rowObject in selection.SelectedRowObjects():
            if rowObject.IsKindOf(acm.FPortfolioInstrumentAndTrades):
                try:
                    portfolio = rowObject.Portfolio()
                    if portfolio.IsKindOf(acm.FASQLPortfolio):
                        portfolio = acm.FStoredASQLQuery.Select('name = "%s"' %
                                portfolio.Name()).First()
                    return portfolio
                except StandardError:
                    pass
    
    @staticmethod
    def _GetGrouperNameFromSelection(selection):
        for rowObject in selection.SelectedRowObjects():
            if rowObject.IsKindOf(acm.FPortfolioInstrumentAndTrades):
                return rowObject.Grouping().Grouper().StringKey()
        return 'Default'
        
    def _GetPortfolioParameters(self):
        sheet = self._eii.ActiveSheet()
        columnIds = []
        columnCreators = sheet.ColumnCreators()
        for i in range(columnCreators.Size()):
            creator = columnCreators.At(i)
            if not creator.Configuration():
                columnIds.append(str(creator.ColumnId()))
            else:
                logger.warn('Cannot profile parameterised column "%s"',
                        creator.Columns().First().ColumnName())
        portfolio = self._GetPortfolioFromSelection(sheet.Selection())
        if portfolio:
            return {
                'PortfolioClass': str(portfolio.Class().Name()),
                'Portfolio': str(portfolio.Name()),
                'Grouper': str(self._GetGrouperNameFromSelection(sheet.Selection())),
                'ColumnIDs': ','.join(columnIds),
                }
        logger.warn('Could not get portfolio parameters for profiling')
        return {}


class PortfolioProfilerRunscript(FRunScriptGUI.AelVariablesHandler):

    GUI_PARAMETERS = {
        'runButtonLabel':   '&&Run',
        'hideExtraControls': False,
        'windowCaption': __name__,
        }
    LOG_LEVELS = {
        '1. Normal': 1,
        '2. Warnings/Errors': 3,
        '3. Debug': 2
        }
    Options = namedtuple('PortfolioProfilerOptions', 
            ['Portfolio', 'Grouper', 'ColumnIDs', 'Scenario', 'EvaluationLevel',
             'CollectStatistics', 'OutputCSV', 'Delimiter', 'LogLevel', 'LogFile'])

    def __init__(self):
        self.ael_variables = []
        FRunScriptGUI.AelVariablesHandler.__init__(self, self.GetVariableDefinitions())

    @classmethod
    def GetPortfolioProfilerOptions(cls, params):
        portfolio = None
        portfolioClass = params['PortfolioClass']
        try:
            if portfolioClass in SUPPORTED_PORTFOLIO_CLASSES:
                portfolio = portfolioClass[params['Portfolio']]
                if not portfolio:
                    portfolio = portfolioClass.Select('name = "%s"' % 
                            params['Portfolio']).First()
        except StandardError:
            pass
        if not portfolio:
            raise ValueError('Could not load portfolio "%s" of type "%s"' %
                    (params['Portfolio'], params['PortfolioClass']))
        return cls.Options(
                Portfolio=portfolio,
                Grouper=params['Grouper'],
                ColumnIDs=params['ColumnIDs'],
                Scenario=params['Scenario'],
                EvaluationLevel=(999 if 'all' in params['EvaluationLevel'] else
                        int(params['EvaluationLevel'][-1])),
                CollectStatistics=(params['Statistics'] == 'true'),
                OutputCSV=(params['ReportFormat'] == 'Comma Separated Values'),
                Delimiter=params['Delimiter'],
                LogLevel=cls.LOG_LEVELS.get(params['LogLevel'], 1),
                LogFile=(os.path.expandvars(params['LogFile']) if 
                        params['EnableLogToFile'] == 'true' else False))

    def GetVariableDefinitions(self):
        logLevels = sorted(self.LOG_LEVELS)
        portfolioClasses = SUPPORTED_PORTFOLIO_CLASSES
        groupers = acm.Risk().GetAllPortfolioGroupers().Keys().Sort()
        columnIds = acm.GetDefaultContext().GetAllExtensions('FColumnDefinition',
                None, True, True, 'sheet columns', 'portfoliosheet').Sort()
        scenarios = sorted([s.Scenario().Name() for s in acm.FStoredScenario.Select('') 
                if s and s.Scenario()])
        evaluationLevels = ['Evaluate cells to tree level ' + str(i+1) for i in range(7)] + \
                ['Evaluate all cell values']
        reportFormats = ['Logged events', 'Comma Separated Values']
        delimiters = [',', ';', '|', ':', '\t', '=']
        return (
            # Portfolio type selection
            ('PortfolioClass', 'Portfolio Type_General', 'FClass', portfolioClasses, 
             portfolioClasses[0], True, False, 'Select the type of portfolio to profile.',
             self._OnPortfolioClassChange, True), 
            # Portfolio selection
            ('Portfolio', 'Portfolio_General', 'string', [], None, True, False, 
             'Select the portfolio to profile.'), 
            # Grouper selection
            ('Grouper', 'Grouper_General', 'string', groupers, '', True, False, 
             'Select the grouper that defines the positions in the portfolio.'),
            # Columns selection
            ('ColumnIDs', 'Column ID(s)_General', 'string', columnIds, None, 
              True, True, 'Select the column IDs to test performance for.'),
            # Scenario selection
            ('Scenario', 'Scenario_General', 'string', scenarios, '', True, False,
             'If desired, select the scenario to apply to all selected columns.'),
            # Cell evaluation level selection
            ('EvaluationLevel', 'Cell Evaluation_General', 'string', evaluationLevels, 
              evaluationLevels[0], 2, False, 'Select the calculations to evaluate.'),
            # Collect statistics mode
            ('Statistics', 'Collect portfolio statistics_General', 'string', [True, False], 
             True, True, False, 'If checked, collect statistics on the '),

            # Report format selection
            ('ReportFormat', 'Report Format_Output', 'string', reportFormats, 
              reportFormats[0], 2, False, 'Select the output report format.',
              self._ReportFormatChange),
            # CSV delimiter character
            ('Delimiter', 'CSV Delimiter_Output', 'string',  delimiters, delimiters[0], 
              True, False, 'Select the delimiter character for CSV reports.', None, False),
            # Logging level selection
            ('LogLevel', 'Logging Level_Output', 'string', logLevels, logLevels[0], 2, False,
             'Select the verbosity of logging output by the task.'),
            # Enabled logging to file
            ('EnableLogToFile', 'Enable Logging To File_Output', 'string', [True, False], 
             False, True, False, 'If checked, log output to the specified file.',
             self._EnableLogToFileToggle),
            # Log file selection
            ('LogFile', 'Log File_Output', 'string', None, '%TEMP%\\' + __name__ + '.txt',
              False, False, 'Select the file to log output to, if desired.', None, False),
            )

    def _OnPortfolioClassChange(self, index, fieldValues):
        portfolioClass = getattr(acm, fieldValues[index])
        portfolios = portfolioClass.Select(None).SortByProperty('Name')
        for i, var in enumerate(self.ael_variables):
            if var[FRunScriptGUI.Controls.NAME] == 'Portfolio':
                self.ael_variables[i][FRunScriptGUI.Controls.VALUES] = portfolios
                if fieldValues[i] not in [p.Name() for p in portfolios]:
                    fieldValues[i] = ''
                break
        return fieldValues

    def _ReportFormatChange(self, index, fieldValues):
        for i, var in enumerate(self.ael_variables):
            if var[FRunScriptGUI.Controls.NAME] == 'Delimiter':
                self.ael_variables[i][FRunScriptGUI.Controls.ENABLED] = \
                        (fieldValues[index] == 'Comma Separated Values')
                break
        return fieldValues

    def _EnableLogToFileToggle(self, index, fieldValues):
        for i, var in enumerate(self.ael_variables):
            if var[FRunScriptGUI.Controls.NAME] == 'LogFile':
                self.ael_variables[i][FRunScriptGUI.Controls.ENABLED] = \
                        (fieldValues[index] == 'true')
                break
        return fieldValues


ael_variables = PortfolioProfilerRunscript()
ael_gui_parameters = ael_variables.GUI_PARAMETERS

def ael_main(params):
    options = PortfolioProfilerRunscript.GetPortfolioProfilerOptions(params)

    logger.Reinitialize(level=options.LogLevel, logToFileAtSpecifiedPath=options.LogFile)
    logger.info('Running portfolio profiler script ...')

    profiler = FPortfolioProfiler(options.Portfolio, options.Grouper, 
            options.ColumnIDs, options.Scenario)
    report = profiler.Run(options.CollectStatistics, options.EvaluationLevel)
    logger.info('Portfolio profiling complete.')
    
    if report:
        logger.debug('Formatting portfolio profile report')
        if options.OutputCSV:
            reportOutput = report.GetCommaSeparatedValues(delimiter=options.Delimiter)
        else:
            reportOutput = report.GetLoggedEvents(reportTotalDelta=True)
        if reportOutput:
            logger.info('Profiling report follows:\n\n\n%s\n', reportOutput)
