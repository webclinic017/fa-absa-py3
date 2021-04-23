""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitCheck.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    FLimitCheck

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Functionality for the checking of limits in pre-deal and non-realtime
    monitoring.

-----------------------------------------------------------------------------"""
import collections

import acm
import FAssetManagementUtils
import FLimitActions
import FLimitMonitor
import FLimitSettings
import FLimitUtils
import FLimitExceptions
import FRunScriptGUI
import FUxCore

logger = FAssetManagementUtils.GetLogger()


def InitialVisibility(insDefApp):
    visible = True
    hookFunc = FLimitSettings.PreDealCheckVisibilityHook()
    if hookFunc:
        try:
            visible = hookFunc(insDefApp)
        except Exception as e:
            print('Error invoking limit check visibility hook:', e)
    else:
        try:
            visible = acm.GetDefaultValueFromName(acm.GetDefaultContext(), 
                    insDefApp.Class(), 'ShowLimitPreDealCheck')
        except Exception:
            pass
    return visible

def OnCreate(eii):
    insDefApp = eii.ExtensionObject()
    if FLimitSettings.EnablePreDealCheck():     # pylint: disable-msg=E1101
        limitCheckPanel = FLimitCheckPanel(insDefApp)
        insDefApp.CreateCustomDockWindow(limitCheckPanel, 
                'FLimitCheckPanel', 'Limit Check Panel', 'Bottom',
                showInitially=InitialVisibility(insDefApp))


class FLimitDisplayDialog(FUxCore.LayoutDialog):
    # pylint: disable-msg=R0902
    
    class Colours(object):
        # pylint: disable-msg=E0213,W0613,R0201,R0903
        try:
            RGB = acm.UX().Colors().Create
        except AttributeError:
            # Default colours when UX is not available/used (e.g. ATS tasks)
            def RGB(r, g, b):
                return acm.FColor()

        RED = RGB(255, 0, 0)
        YELLOW = RGB(255, 255, 0)
        WHITE = RGB(255, 255, 255)
        BLACK = RGB(0, 0, 0)


    def __init__(self, trade, limitFilterQueryFolder):
        self._trade = trade
        self._limitQuery = limitFilterQueryFolder
        self._limits = None
        self._limitSheet = None
        self._totalCountCtrl = None
        self._applicableCountCtrl = None
        self._warningCountCtrl = None
        self._breachCountCtrl = None
        self._updatedStates = {}
        self._dependencies = []
        self._InitialiseLimits()

    def CreateLayout(self):
        # pylint: disable-msg=R0201
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginHorzBox()
        b.    BeginVertBox('EtchedIn')
        b.      AddInput('filter', 'Limit filter', 80)
        b.      BeginHorzBox()
        b.        AddInput('total', 'Total limits checked')
        b.        AddInput('applicable', 'Applicable for trade')
        b.        AddInput('warning', 'Warning count')
        b.        AddInput('breach', 'Breach count')
        b.      EndBox()           
        b.    EndBox()
        b.    AddFill()
        b.  EndBox()
        b.  BeginVertBox()
        b.    AddCustom('limits', 'sheet.FLimitSheet', 1100, 250)
        b.  EndBox()
        b.  AddSeparator()
        b.  BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'Close')
        b.  EndBox()
        b.EndBox()
        return b

    def HandleCreate(self, dialog, layout):
        dialog.Caption('Limits - ' + self._GetTradeDescription())

        ctrl = layout.GetControl
        ctrl('filter').SetData(self._limitQuery.Name())
        self._totalCountCtrl = ctrl('total')
        self._applicableCountCtrl = ctrl('applicable')
        self._warningCountCtrl = ctrl('warning')
        self._breachCountCtrl = ctrl('breach')
        for name in ('filter', 'total', 'applicable', 'warning', 'breach'):
            ctrl(name).Editable(False)

        self._limitSheet = ctrl('limits').GetCustomControl()
        self._InitialiseLimitSheet()
        self._CheckLimits()
        self._UpdateControls()
        
    def HandleApply(self):
        return self.HandleCancel()

    def HandleCancel(self):
        try:
            for dependent in self._dependencies:
                if not dependent.IsDeleted():
                    dependent.RemoveDependent(self)
            self._ClearLimitColumnSimulations()
        except Exception:
            pass
        return True
        
    def ServerUpdate(self, _sender, _symbol, _params):
        self._UpdateControls()
        
    def _UpdateControls(self):
        warningCount, breachCount, applicableCount, totalCount = self._GetStateCounts()
        self._totalCountCtrl.SetData(totalCount)
        self._applicableCountCtrl.SetData(applicableCount)
        
        bgColour = self.Colours.YELLOW if warningCount > 0 else self.Colours.WHITE
        font = 'Bold' if warningCount > 0 else 'Default'
        self._warningCountCtrl.SetData(warningCount)
        self._warningCountCtrl.SetColor('BackgroundReadonly', bgColour)
        self._warningCountCtrl.SetStandardFont(font)

        bgColour = self.Colours.RED if breachCount > 0 else self.Colours.WHITE
        textColour = self.Colours.WHITE if breachCount > 0 else self.Colours.BLACK
        font = 'Bold' if breachCount > 0 else 'Default'
        self._breachCountCtrl.SetData(breachCount)
        self._breachCountCtrl.SetColor('BackgroundReadonly', bgColour)
        self._breachCountCtrl.SetColor('Text', textColour)
        self._breachCountCtrl.SetStandardFont(font)
        
    def _InitialiseLimits(self):
        self._limits = acm.FASQLQueryFolder()
        self._limits.Name(self._GetTradeDescription())
        query = acm.CreateFASQLQuery('FLimit', 'OR')
        for limit in self._limitQuery.Query().Select():
            if self._IsLimitApplicableForTrade(limit):
                query.AddOpNode('OR')
                query.AddAttrNode('Oid', 'EQUAL', limit.Oid())
                bp = limit.BusinessProcess()
                if bp:
                    bp.AddDependent(self)
                    self._dependencies.append(bp)
        if not query.AsqlNodes():
            # No limits to display
            query.AddOpNode('AND')
            query.AddAttrNode('Oid', 'EQUAL', -1)
        self._limits.AsqlQuery(query)

    def _InitialiseLimitSheet(self):
        # pylint: disable-msg=E1101
        context = acm.GetDefaultContext()
        defaultColumns = acm.GetColumnCreators(
                FLimitSettings.DefaultDisplayColumns(), context)
        columns = self._limitSheet.ColumnCreators()
        columns.Clear()
        for i in range(defaultColumns.Size()):
            columns.Add(defaultColumns.At(i))
        self._limitSheet.InsertObject(self._limits, 'IOAP_LAST')
        self._limitSheet.PrivateTestSyncSheetContents()

    def _CheckLimits(self):
        # pylint: disable-msg=W0703
        if self._IsLimitCheckingEnabled():
            self._ClearLimitColumnSimulations()
            for limit in self._limits.Query().Select():
                try:
                    result = self._CheckLimit(limit)
                    if result and self._IsCheckedLimitUpdated(result):
                        self._UpdateLimitState(limit, result)
                except Exception as e:
                    print('Error checking limit', limit.Oid(), ':', e)
         
    def _CheckLimit(self, limit):
        try:
            FLimitUtils.InitialiseLimit(limit)
            monitoredLimit = FLimitMonitor.FMonitoredLimit(limit)
        except FLimitExceptions.EmptyCalculationError:
            pass
        else:
            result = monitoredLimit.CheckLimit([self._trade, ])
            if result and result.Children:
                self._UpdateParentLimitCheckResult(result)
            del monitoredLimit
            return result

    def _UpdateLimitState(self, limit, checkResult):
        currentValue = limit.LimitValue().CheckedValue()
        checkedValue = checkResult.CheckedValue
        if checkedValue and checkedValue != currentValue:
            self._SetLimitColumnSimulated(limit, 
                    'Limit Checked Value', checkedValue)
        if checkResult.StateBefore != checkResult.StateAfter:
            self._SetLimitColumnSimulated(limit, 
                    'Limit Current State', checkResult.StateAfter)
            self._updatedStates[limit] = checkResult.StateAfter

    def _ClearLimitColumnSimulations(self):
        for limit in self._limits.Query().Select():
            self._SetLimitColumnSimulated(limit,
                    'Limit Checked Value', None)
            self._SetLimitColumnSimulated(limit,
                    'Limit Current State', None)
        self._updatedStates.clear()

    def _SetLimitColumnSimulated(self, limit, columnId, value):
        try:
            cell = self._GetCell(limit, columnId)
            evaluator = cell.Evaluator() if cell else None
            if evaluator:
                if value is not None:
                    evaluator.Simulate(value, False)
                else:
                    evaluator.RemoveSimulation()
        except Exception:
            pass

    def _GetCell(self, limit, columnId):
        columnIter = self._limitSheet.GridColumnIterator()
        while columnIter:
            columnName = str(columnIter.GridColumn().ColumnId()) if \
                    columnIter.GridColumn() else None
            if columnName == columnId:
                break
            columnIter = columnIter.Next()
        if columnIter:
            rowIter = self._limitSheet.RowTreeIterator(False)
            rowIter = rowIter.Find(limit) if rowIter else None
            if rowIter:
                return self._limitSheet.GetCell(rowIter, columnIter)
        return None

    def _GetLimitState(self, limit):
        return self._updatedStates.get(limit, None) or FLimitUtils.CurrentState(limit)

    def _GetTradeDescription(self):
        return self._trade.Instrument().Name() + ' ' + self._trade.StringKey()

    def _GetStateCounts(self):
        states = collections.defaultdict(int)
        for limit in self._limits.Query().Select():
            state = self._GetLimitState(limit)
            states[state] = states[state] + 1
        return (states['Warning'], states['Breached'], 
            sum(states.values()), self._limitQuery.Query().Select().Size())

    def _IsLimitCheckingEnabled(self):
        return bool(FLimitCheckPanel.IsLocalLimitCheckEnabled() and 
                (self._trade.IsInfant() or self._trade.IsModified()))

    def _IsLimitApplicableForTrade(self, limit):
        if limit.IsParent() and not self._IsLimitCheckingEnabled():
            return False
        if not (FLimitUtils.IsActive(limit) or FLimitUtils.CurrentState(limit) == 'Ready'):
            return False
        return limit.LimitTarget().Includes(self._trade)

    @staticmethod
    def _IsCheckedLimitUpdated(checkResult):
        limit = checkResult.Limit
        return bool(checkResult.StateAfter != checkResult.StateBefore or 
                checkResult.CheckedValue != limit.LimitValue().CheckedValue())

    @staticmethod
    def _UpdateParentLimitCheckResult(checkResult):
        assert checkResult.Children
        worstChildResult = checkResult.Children[0]
        for childResult in checkResult.Children:
            if (childResult.StateAfter == 'Breached' or
                (childResult.StateAfter == 'Warning' and
                 worstChildResult.StateAfter != 'Breached')):
                worstChildResult = childResult
        checkResult.StateAfter = worstChildResult.StateAfter
        checkResult.CheckedValue = worstChildResult.CheckedValue


class FLimitCheckPanel(FUxCore.LayoutPanel):
    
    class Filters(object):
        # pylint: disable-msg=R0903
        ALL_LIMITS = 'All limits'
        MY_LIMITS = 'My limits'
        LIMITS_OF_SPEC = 'Limits of specification'
        LIMITS_OF_TYPE = 'Limits of type'
        LIMITS_IN_QUERY = 'Limits in query'


    def __init__(self, insDefApp):
        self._insDefApp = insDefApp
        self._filterCtrl = None
        self._limitSpecCtrl = None
        self._limitTypeCtrl = None
        self._limitQueryCtrl = None
        self._checkCtrl = None
        self._bindings = None
        
    def HandleCreate(self):
        self._InitDataBindingControls()
        layout = self.SetLayout(self.CreateLayout())    # pylint: disable-msg=E1101
        ctrls = (self._filterCtrl, self._limitSpecCtrl, self._limitTypeCtrl, self._limitQueryCtrl)
        for ctrl in ctrls:
            ctrl.InitLayout(layout)
        self._checkCtrl = layout.GetControl('check')
        self._checkCtrl.AddCallback('Activate', self.OnCheckLimits, None)
        self._insDefApp.EditTrade().AddDependent(self)
        
        self._SetDefaultLimitFilter()
        self._UpdateControls()
        
    def ServerUpdate(self, sender, symbol, _binder):
        if str(symbol) == 'delete':
            # InsDef has loaded a new trade
            sender.RemoveDependent(self)
            self._insDefApp.EditTrade().AddDependent(self)
        self._UpdateControls()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('EtchedIn', 'Limits')
        b.  BeginHorzBox()
        b.    BeginVertBox()
        self._filterCtrl.BuildLayoutPart(b, 'Filter')
        self._limitSpecCtrl.BuildLayoutPart(b, 'Specification')
        self._limitTypeCtrl.BuildLayoutPart(b, 'Type')
        self._limitQueryCtrl.BuildLayoutPart(b, 'Query')
        b.    EndBox()
        b.    AddButton('check', 'Check...')
        b.  EndBox()
        b.EndBox()
        return b

    @staticmethod
    def IsLocalLimitCheckEnabled():
        # pylint: disable-msg=E1101
        return FLimitSettings.PreDealCheckType().lower() == 'local'

    def OnCheckLimits(self, _params, _cd):
        trade = self._GetTrade()
        if trade.IsModified() or trade.IsInfant():
            trade = trade.Clone()
            if trade.Instrument().Original():
                trade.Instrument(trade.Instrument().Original())

        limits = self._GetSelectedLimitQuery()
        dlg = FLimitDisplayDialog(trade, limits)
        acm.UX().Dialogs().ShowCustomDialogModal(
                self._insDefApp.Shell(), dlg.CreateLayout(), dlg)

    def _InitDataBindingControls(self):
        self._bindings = acm.FUxDataBindings()
        self._filterCtrl = self._bindings.AddBinder(
                'filter', 'string', None, self._GetLimitFilters())
        self._limitSpecCtrl = self._bindings.AddBinder('specs', 'FLimitSpecification')
        self._limitTypeCtrl = self._bindings.AddBinder(
                'types', 'string', None, self._GetLimitTypes())
        self._limitQueryCtrl = self._bindings.AddBinder(
                'queries', 'FStoredASQLQuery', None, self._GetLimitQueries())
        self._bindings.AddDependent(self)

    def _SetDefaultLimitFilter(self):
        # pylint: disable-msg=E1101
        filterTypeMap = {
            'all': (self.Filters.ALL_LIMITS, None, None),
            'my': (self.Filters.MY_LIMITS, None, None),
            'spec': (self.Filters.LIMITS_OF_SPEC, self._limitSpecCtrl, acm.FLimitSpecification),
            'type': (self.Filters.LIMITS_OF_TYPE, self._limitTypeCtrl, None),
            'query': (self.Filters.LIMITS_IN_QUERY, self._limitQueryCtrl, acm.FStoredASQLQuery),
            }
        default = FLimitSettings.DefaultPreDealCheckFilter()
        defaultType = default.split(':')[0].lower()
        defaultItem = ':'.join(default.split(':')[1:])
        
        filterType, ctrl, domain = filterTypeMap.get(defaultType, (None, None, None))
        if filterType:
            self._filterCtrl.SetValue(filterType)
            if domain and defaultItem:
                defaultItem = domain[defaultItem]
            if defaultItem and ctrl:
                ctrl.SetValue(defaultItem)

    def _UpdateControls(self):
        trade = self._GetTrade()
        filterType = self._filterCtrl.GetValue()
        checkEnabled = bool(filterType and self._IsTradeApplicable(trade))
        filterItemCtrlMap = {
            self.Filters.LIMITS_OF_SPEC: self._limitSpecCtrl,
            self.Filters.LIMITS_OF_TYPE: self._limitTypeCtrl,
            self.Filters.LIMITS_IN_QUERY: self._limitQueryCtrl,
            }
        filterItemCtrl = filterItemCtrlMap.get(filterType, None)
        for ctrl in filterItemCtrlMap.values():
            if ctrl == filterItemCtrl:
                ctrl.Visible(True)
                checkEnabled &= bool(ctrl.GetValue())
            else:
                ctrl.Visible(False)
        self._checkCtrl.Enabled(checkEnabled)

    def _GetTrade(self):
        return self._insDefApp.EditTrade()

    def _GetSelectedLimitQuery(self):
        queryMap = {
            self.Filters.MY_LIMITS: (self._GetMyLimitsQuery, None),
            self.Filters.LIMITS_OF_TYPE: 
                    (self._GetLimitsOfTypeQuery, self._limitTypeCtrl.GetValue()),
            self.Filters.LIMITS_OF_SPEC: 
                    (self._GetLimitsOfSpecificationQuery, self._limitSpecCtrl.GetValue()),
            self.Filters.LIMITS_IN_QUERY: 
                    (self._GetLimitsInQueryQuery, self._limitQueryCtrl.GetValue()),
            }
        queryFunc, param = queryMap.get(
                self._filterCtrl.GetValue(), (self._GetAllLimitsQuery, None))
        return queryFunc(param) if param else queryFunc()

    @classmethod
    def _GetLimitFilters(cls):
        return [v for k, v in vars(cls.Filters).items() if not k.startswith('_')]
    
    @staticmethod
    def _GetLimitTypes():
        try:
            return acm.FChoiceList['Limit Type'].Choices()
        except Exception:
            return []
    
    @staticmethod
    def _GetLimitQueries():
        return acm.FStoredASQLQuery.Select('subType="FLimit"')

    @classmethod
    def _GetAllLimitsQuery(cls):
        folder = acm.FASQLQueryFolder()
        folder.Name(cls.Filters.ALL_LIMITS)
        folder.AsqlQuery(acm.CreateFASQLQuery('FLimit', 'AND'))
        return folder

    @classmethod
    def _GetMyLimitsQuery(cls):
        folder = acm.FASQLQueryFolder()
        folder.Name(cls.Filters.MY_LIMITS)
        query = acm.CreateFASQLQuery('FLimit', 'AND')
        query.AddAttrNode('Owner.Name', 'RE_LIKE_NOCASE', acm.User().Name())
        folder.AsqlQuery(query)
        return folder

    @classmethod
    def _GetLimitsOfTypeQuery(cls, limitType):
        folder = acm.FASQLQueryFolder()
        folder.Name(cls.Filters.LIMITS_OF_TYPE + ' "%s"' % limitType)
        query = acm.CreateFASQLQuery('FLimit', 'AND')
        query.AddAttrNode('LimitSpecification.LimitType.Name', 'RE_LIKE_NOCASE', limitType)
        folder.AsqlQuery(query)
        return folder

    @classmethod
    def _GetLimitsOfSpecificationQuery(cls, limitSpec):
        folder = acm.FASQLQueryFolder()
        folder.Name(cls.Filters.LIMITS_OF_SPEC + ' "%s"' % limitSpec.Name())
        query = acm.CreateFASQLQuery('FLimit', 'AND')
        query.AddAttrNodeNumerical('LimitSpecification.Oid', limitSpec.Oid(), limitSpec.Oid())
        folder.AsqlQuery(query)
        return folder

    @classmethod
    def _GetLimitsInQueryQuery(cls, storedQuery):
        folder = acm.FASQLQueryFolder()
        folder.Name(cls.Filters.LIMITS_IN_QUERY + ' "%s"' % storedQuery.Name())
        folder.AsqlQuery(storedQuery.Query())
        return folder

    @classmethod
    def _IsTradeApplicable(cls, trade):
        return bool(trade and (cls.IsLocalLimitCheckEnabled() or not trade.IsInfant()))

             
class LimitCheckRunscript(FRunScriptGUI.AelVariablesHandler):
    """Runscript for checking non-realtime monitored limits."""

    GUI_PARAMETERS = {
        'runButtonLabel':   '&&Run',
        'hideExtraControls': False,
        'windowCaption' : __name__
        }
    LOG_LEVELS = {
        '1. Normal': 1,
        '2. Warnings/Errors': 3,
        '3. Debug': 2
        }

    def __init__(self):
        FRunScriptGUI.AelVariablesHandler.__init__(self, self._GetVariableDefinitions())

    @staticmethod
    def GetParameters(params):
        paramClass = collections.namedtuple('LimitParameters', params.keys())
        return paramClass(**params)

    @classmethod
    def GetLoggingLevel(cls, logLevel):
        return cls.LOG_LEVELS.get(logLevel, 1)

    @staticmethod
    def GetDefaultLimitQuery():
        q = acm.CreateFASQLQuery(acm.FLimit, 'AND')
        q.AddAttrNode('LimitSpecification.RealtimeMonitored', 'EQUAL', False)
        return q

    def _GetVariableDefinitions(self):
        logLevels = sorted(self.LOG_LEVELS)
        return (
            # Limit oid selection
            ('Limits', 'Limits_General', 'FSymbol', None, self._GetLimitOidQuery(), True, True, 
             'Select the individual limit(s) to check.', None, True), 
            # Limit query selection
            ('LimitQueries', 'Limit query_General', 'FStoredASQLQuery', None, 
             self._GetLimitInsertItemQueries(), True, True, 
             'Select the insert item query or queries containing limits to check.', None, True),
            # Display limits in operations manager
            ('DisplayLimits', 'Display limits in Operations Manager_General', 
             'string', [True, False], False, False, False, 
             'If checked, processed limits will be displayed in the Operations Manager.'),
            # Force processing realtime monitored limits
            ('ForceProcessRealtime', 'Force processing of realtime monitored limits_General',
             'string', [True, False], False, False, False, 
             'If checked, force the processing of limits marked as realtime monitored.'),
            # Logging level selection
            ('LogLevel', 'Logging Level_Logging', 'string', logLevels, logLevels[0], 2, 0,
             'Select the verbosity of logging output by the limit engine task.'),
            )

    @staticmethod
    def _GetLimitOidQuery():
        q = acm.CreateFASQLQuery(acm.FLimit, 'AND')
        op = q.AddOpNode('AND')
        op.AddAttrNode('Oid', 'GREATER_EQUAL', None)
        op.AddAttrNode('Oid', 'LESS_EQUAL', None)
        q.AddOpNode('AND').AddAttrNode('LimitSpecification.Name', 'RE_LIKE_NOCASE', None)
        q.AddOpNode('AND').AddAttrNode('LimitSpecification.LimitType.Name', 'EQUAL', None)
        op = q.AddOpNode('AND')
        op.AddAttrNode('CreateTime', 'GREATER_EQUAL', None)
        op.AddAttrNode('CreateTime', 'LESS_EQUAL', None)
        q.AddOpNode('AND').AddAttrNode('LimitSpecification.RealtimeMonitored', 'EQUAL', False)
        return q

    @staticmethod
    def _GetLimitInsertItemQueries():
        q = acm.CreateFASQLQuery(acm.FStoredASQLQuery, 'AND')
        q.AddOpNode('AND').AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
        q.AddOpNode('AND').AddAttrNode('SubType', 'RE_LIKE_NOCASE', 'FLimit')
        return q


ael_variables = LimitCheckRunscript()
ael_gui_parameters = ael_variables.GUI_PARAMETERS

def ael_main(params):
    options = LimitCheckRunscript.GetParameters(params)
    displayLimits = bool(options.DisplayLimits == 'true')
    distributedMode = FLimitSettings.UseDistributedCalculations()

    FAssetManagementUtils.ReinitializeLogger(
            LimitCheckRunscript.GetLoggingLevel(options.LogLevel))
    logger.info('Running limits check ...')
    logger.info('Using distributed calculations: %s', distributedMode)
    if distributedMode:
        calcEnv = FLimitSettings.CalculationEnvironment()
        logger.info('Using calculation environment: %s', calcEnv.Name() if calcEnv else 'None')

    # Load and validate limits
    limits = acm.FArray()
    limits.AddAll([acm.FLimit[l.Text()] for l in options.Limits])

    for query in options.LimitQueries:
        limits.AddAll(query.Query().Select())
    if not limits and not options.LimitQueries:
        limits = ael_variables.GetDefaultLimitQuery().Select()
    limits = [l for l in limits.AsSet() if l and (options.ForceProcessRealtime or 
            not l.LimitSpecification().RealtimeMonitored())]

    # Perform limit check and display results
    FLimitActions.CheckLimits(limits)
    if displayLimits and limits and acm.IsSessionUserInteractive():
        FLimitActions.StartLimitWorkbench(limits)
    logger.info('Limits check complete.')
