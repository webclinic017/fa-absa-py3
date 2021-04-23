""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitActions.py"
"""--------------------------------------------------------------------------
MODULE
    FLimitActions

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    A collection of functions for user actions related to limit management.

-----------------------------------------------------------------------------"""

import acm
from contextlib import contextmanager
import FBusinessProcessUtils
import FLimitViewer
import FLimitSettings
import FLimitServer
import FLimitCheckReport
import FLimitCheckReportOutput
import FLimitCheck
from FLimitTemplate import FLimitTemplate
from FLimitTreeSpecification import LimitTreeSpecification
import FLimitUtils
from FLimitColumnCreatorHandler import ColumnCreatorHandler
import FAssetManagementUtils
import FOperationsManagerWorkbench
import FUxCore

logger = FAssetManagementUtils.GetLogger()


#------------------------------------------------------------------------------
# Actions
#------------------------------------------------------------------------------

def StartLimitWorkbench(limits=None):
    # pylint: disable-msg=E1101
    # Limits are inserted as a business process query folder
    queryFolder = acm.FASQLQueryFolder()
    queryFolder.Name('All Limits')
    query = acm.CreateFASQLQuery('FLimit', 'OR')
    if limits:
        for limit in limits:
            op = query.AddOpNode('AND')
            op.AddAttrNode('Oid', 'GREATER_EQUAL', limit.Oid())
            op.AddAttrNode('Oid', 'LESS_EQUAL', limit.Oid())
    queryFolder.AsqlQuery(query)

    FOperationsManagerWorkbench.StartOperationsManagerWorkbench(
            defaultObjects=[queryFolder, ],
            sheetTemplate=acm.FTradingSheetTemplate[FLimitSettings.WorkbenchSheetTemplate()],
            sheetType='LimitSheet',
            grouperSubjectClass=acm.FLimitGrouperSubject,
            grouperName=FLimitSettings.WorkbenchGrouper(),
            expandAllRows=FLimitSettings.WorkbenchAutoExpandRows(),
            expandedRowFilter=FLimitSettings.WorkbenchAutoExpandExclude())

def CheckLimits(limits):
    limits = set([l for l in limits if l.Parent() not in limits])
    engine = FLimitServer.FLimitEngine()
    for l in limits:
        engine.CheckLimit(l)

def ExecuteEvent(limits, event, shell=None):
    limits = [l for l in limits if l.BusinessProcess() and
       FBusinessProcessUtils.IsValidEvent(l.BusinessProcess(), event)]
    if limits:
        comment = ''
        if event in FLimitSettings.WorkbenchCommentOnActions(): # pylint: disable-msg=E1101
            dlg = ExecuteEventDialog(limits, event)
            comment = acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)
        if comment is not None:
            for l in limits:
                bp = l.BusinessProcess()
                bp.HandleEvent(event, None, [comment, ])
                bp.Commit()

def CreateLimitTemplate(limit, shell):
    dlg = LimitTemplateDialog(limit)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)

def ViewLimitHistory(limit):
    acm.StartApplication('Business Process Details', limit.BusinessProcess())

def ViewLimit(limit):
    acm.StartApplication('Limit', limit)

def ViewLimitProtection(limit, shell, commitOnApply=False):
    dlg = ProtectionDialog(limit, commitOnApply)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)

def ViewLimitSpecification(limitSpec):
    acm.StartApplication('Limit Specification', limitSpec)

def ViewLimitTransactionHistory(limit, shell):
    import TransactionHistory
    TransactionHistory.ShowTransactionHistoryPrivate(limit, shell)

def SendLimitUserMessage(limit):
    acm.StartApplication('Send Message', limit)

def ViewLimitTarget(limitTarget):
    tradingMgr = None
    if limitTarget.SheetType() in ('FLimitSheet', 'FSettlementSheet'):
        tradingMgr = acm.StartApplication('Operations Manager', None)
    else:
        tradingMgr = acm.StartApplication('Trading Manager', None)
    sheet = tradingMgr.ActiveWorkbook().ActiveSheet()
    if not sheet or str(sheet.SheetClass().Name()) != limitTarget.SheetType():
        sheet = tradingMgr.ActiveWorkbook().NewSheet(limitTarget.SheetType()[1:])
    try:
        sheet.ColumnCreators().Clear()
        _AddLimitTargetColumnsToSheet(sheet, limitTarget)
    except StandardError as e:
        logger.error('Failed to add limit target columns to sheet: {0}'.format(e))

    try:
        _AddTreeSpecificationToSheet(sheet, limitTarget.TreeSpecification())
    except StandardError as e:
        logger.error('Limit target could not be rebuilt: {0}'.format(e))

    def _PrivateCreateLimitUtilityView(_args):
        try:
            FLimitViewer.CreateLimitUtilityView(tradingMgr)
        except StandardError as e:
            logger.error('Failed to show limit viewer: {0}'.format(e))

    tradingMgr.Shell().CallAsynch(_PrivateCreateLimitUtilityView, None)

def LimitSheet_DoubleClick(eii):
    tm = eii.ExtensionObject()
    cell = eii.Parameter('sheet').Selection().SelectedCell()
    if cell and cell.RowObject() and cell.RowObject().Class() == acm.FLimit:
        acm.StartApplication('Limit', cell.RowObject())

def CreateCheckReportFile(limitCheckResults, name):
    ''' Creates a limit report on file/ads. Takes a list of limit check results and an identifier used 
    for naming the report. When storing on file, the file directory is specified in the FLimitReportSettings.
    The function returns the path from the limit directory, example "2016-01-01\\12345.xml". When storing on ads,
    the function returns the sequence number of the produced text object (FCustomArchive)'''
    if FLimitSettings.Storage() == 'ADS':
        output = FLimitCheckReportOutput.XmlReportOutput(name)
    elif FLimitSettings.Storage() == 'File':
        output = FLimitCheckReportOutput.XmlReportOutputFile(name)
    else:
        logger.error('Unknown storage place %s'%FLimitSettings.Storage())
        return
    FLimitCheckReport.LimitCheckReport(output.Writer()).Generate(limitCheckResults)
    return output.StoreAndGenerateKey()

#------------------------------------------------------------------------------
# Helper functions
#------------------------------------------------------------------------------

def _AddLimitTargetColumnsToSheet(sheet, limitTarget):
    columnCreators = sheet.ColumnCreators()
    columnIds = acm.FArray().AddAll(['Limit Count', ])
    requiredColumns = acm.GetColumnCreators(columnIds, acm.GetDefaultContext())
    if requiredColumns.Size() > 0 and not requiredColumns.At(0).IsFaulty():
        columnCreators.Add(requiredColumns.At(0))

    requiredColumns = _GetLimitTargetColumnCreators(sheet, limitTarget)
    if requiredColumns.Size() > 0 and not requiredColumns.At(0).IsFaulty():
        columnCreators.Add(requiredColumns.At(0))
    else:
        raise ValueError('Unable to add column "%s" to sheet' %
                limitTarget.CalculationSpecification().ColumnName())

def _GetLimitTargetColumnCreators(sheet, limitTarget):
    columnHandler = ColumnCreatorHandler(limitTarget)
    scenario = columnHandler.Scenario()
    if scenario:
        sheet.GridBuilder().ScenarioManager().RegisterScenario(scenario)
        return columnHandler.ColumnCreatorsFromScenario(scenario)
    return columnHandler.ColumnCreators()  

def _AddTreeSpecificationToSheet(sheet, treeSpec):
    try:
        sheet.InsertObject(treeSpec.OriginObject(), 'IOAP_LAST')
    except StandardError as e:
        raise ValueError('Failed to insert object "%s" into sheet: %s' % \
                (treeSpec.OriginObject().StringKey(), e))
    row = sheet.RowTreeIterator(True).FirstChild()
    if row and treeSpec.Grouper():
        row.Tree().ApplyGrouper(treeSpec.Grouper())
        sheet.GridBuilder().Refresh()

    # Expand the tree according to tree constraints
    treeIter = sheet.RowTreeIterator(True).FirstChild().Find(treeSpec)
    if treeIter:
        sheet.NavigateTo(treeIter.Tree().Item())

#----------------------------------------------------------------------------
# Menu item creation functions
#----------------------------------------------------------------------------

def CreateCreateLimitMenuItem(eii):
    return CreateLimitMenuItem(eii)

def CreateApplyLimitTemplateMenuItem(eii):
    return ApplyLimitTemplateMenuItem(eii)

def CreateViewAllLimitsMenuItem(eii):
    return LimitMenuItem(eii,
        invokeFunc=lambda l: StartLimitWorkbench(),
        enabledFunc=lambda l: True)

def CreateViewLimitHistoryMenuItem(eii):
    # pylint: disable-msg=W0108
    return LimitMenuItem(eii,
        invokeFunc=lambda l: ViewLimitHistory(l),
        validateFunc=lambda l: bool(l.BusinessProcess()))

def CreateViewLimitSpecificationMenuItem(eii):
    return LimitMenuItem(eii,
        invokeFunc=lambda l: ViewLimitSpecification(l.LimitSpecification()),
        validateFunc=lambda l: bool(l.LimitSpecification()))

def CreateViewLimitTargetMenuItem(eii):
    return LimitMenuItem(eii,
        invokeFunc=lambda l: ViewLimitTarget(l.LimitTarget()),
        validateFunc=lambda l: bool(l.LimitTarget()))

def CreateViewLimitMenuItem(eii):
    # pylint: disable-msg=W0108
    return LimitMenuItem(eii,
        invokeFunc=lambda l: ViewLimit(l),
        enabledFunc=lambda l: True)

def CreateViewLimitParentMenuItem(eii):
    return LimitMenuItem(eii,
        invokeFunc=lambda l: ViewLimit(l.Parent()),
        validateFunc=lambda l: bool(l.Parent()))

def CreateLimitProtectionMenuItem(eii):
    isInSheet = hasattr(eii, 'ActiveSheet')
    return LimitMenuItem(eii,
        invokeFunc=lambda l: ViewLimitProtection(l, eii.Shell(), commitOnApply=isInSheet))

def CreateLimitTemplateMenuItem(eii):
    return LimitMenuItem(eii,
        invokeFunc=lambda l: CreateLimitTemplate(l, eii.Shell()),
            enabledFunc=lambda limits: bool(limits and
                    FLimitTemplate.IsValidForTemplate(limits[0])))

def CreateLimitTransactionHistoryMenuItem(eii):
    return LimitMenuItem(eii, invokeFunc=lambda l: ViewLimitTransactionHistory(l, eii.Shell()))

def CreateLimitActiveMenuItem(eii):
    return LimitActivationMenuItem(eii)

def CreateSendLimitMessageMenuItem(eii):
    # pylint: disable-msg=W0108
    return LimitMenuItem(eii, invokeFunc=lambda l: SendLimitUserMessage(l))

def CreateLimitAddInfoMenuItem(eii):
    return LimitAddInfoMenuItem(eii)

def CreateAcceptBreachEventMenuItem(eii):
    return LimitEventMenuItem(eii, 'Breach Accepted')

def CreateInvestigateEventMenuItem(eii):
    return LimitEventMenuItem(eii, 'Investigate')

def CreateActivateEventMenuItem(eii):
    return LimitEventMenuItem(eii, 'Activate')

def CreateDeactivateEventMenuItem(eii):
    return LimitEventMenuItem(eii, 'Deactivate')

def CreateLimitCheckMenuItem(eii):
    return LimitCheckMenuItem(eii)

#------------------------------------------------------------------------------
# Menu item classes
#------------------------------------------------------------------------------

class CreateLimitMenuItem(FUxCore.MenuItem):

    def __init__(self, extObj):
        self._frame = extObj

    def Enabled(self):
        return True

    def Invoke(self, _eii):
        activeSheet = _eii.Parameter('sheet')
        if not activeSheet:
            activeSheet = FLimitUtils.ActiveSheet(self._frame)
        selection = activeSheet.Selection()
        if selection and self._IsValidConfiguration(selection):
            cell = selection.SelectedCell()
            sheetType = activeSheet.SheetClass()
            calcEnv = self._GetCalcEnvironment(activeSheet)
            limitTarget = self._GetLimitTarget(cell, sheetType, calcEnv )
            target = acm.FPair()
            target.First(limitTarget)
            target.Second(cell)
            acm.StartApplication('Limit', target)
        else:
            acm.UX().Dialogs().MessageBox(self._frame.Shell(), 'Error', "Unable to create limit for the selected cell", 'OK', None, None, 'Button1', 'Button1')

    def _GetCalcEnvironment(self, activeSheet):
        env = None
        if activeSheet.SheetContents().At('UseDefaultEnvironment'):
            # pylint: disable-msg=W0212
            env = FLimitSettings._GetUserConfigParameterValue('defaultCalculationEnvironment')
        else:
            env = activeSheet.SheetContents().At('calculationEnvironment')
        return env

    @staticmethod
    def _GetLimitTarget(cell, sheetType, calcEnv=None):
        t = acm.FLimitTarget()
        t.SheetType(FLimitUtils.TargetSheetType(sheetType))
        t.CalculationEnvironment(calcEnv)
        t.CalculationSpecification(cell.CalculationSpecification())
        t.TreeSpecification(LimitTreeSpecification(cell).TreeSpecification())
        t.ProjectionParts(cell.ProjectionParts())
        t.ColumnLabel(cell.Column().StringKey())
        t.ScenarioDisplayType(cell.ScenarioSettings().ShiftDisplayType()
            if cell.ScenarioSettings() else 0)
        return t

    @classmethod
    def _IsValidConfiguration(cls, selection):
        if selection:
            cell = selection.SelectedCell()
            if cell and cell.Evaluator() and cell.Evaluator().HasSimulatedInput():
                return False
            if FLimitUtils.IsSupportedCell(cell):
                rowObject = FLimitUtils.CellRowObject(cell)
                grouper = LimitTreeSpecification(cell).TreeSpecification().Grouper()
                index = cls._GetSubportfolioGroupingIndex(grouper)
                if cls._IsCompoundPortfolio(rowObject):
                    return index <= 0
                return index == -1
        return False

    @staticmethod
    def _GetSubportfolioGroupingIndex(grouper):
        if grouper:
            if grouper.IsKindOf(acm.FChainedGrouper):
                for i, subGrouper in enumerate(grouper.Groupers()):
                    if subGrouper.IsKindOf(acm.FSubportfolioGrouper):
                        return i
            elif grouper.IsKindOf(acm.FSubportfolioGrouper):
                return 0
        return -1

    @staticmethod
    def _IsCompoundPortfolio(rowObject):
        try:
            return rowObject.Portfolio().IsKindOf(acm.FCompoundPortfolio)
        except AttributeError:
            return False

class SheetObject(object):
    def __init__(self, sheetType, obj):
        self._sheetType = sheetType
        self._object = obj

    def SheetType(self):
        return self._sheetType

    def Object(self):
        return self._object

class ApplyLimitTemplateMenuItem(FUxCore.MenuItem):

    def __init__(self, extObj):
        self._extObj = extObj

    def Enabled(self):
        return bool(self._GetPortfolio())

    def Invoke(self, _eii):
        portfolio = self._GetPortfolio()
        if hasattr(self._extObj, 'ActiveSheet'):
            portfolio = SheetObject(str(self._extObj.ActiveSheet().SheetClass().Name()), portfolio)
        app = acm.StartApplication('Limit', portfolio)
        app.ShowDockWindow('limitTemplate')

    def _GetPortfolio(self):
        if self._extObj.IsKindOf(acm.FArray):
            return self._extObj.First()
        try:
            cell = self._extObj.ActiveSheet().Selection().SelectedCell()
            rowObject = FLimitUtils.CellRowObject(cell)
            portfolioFunc = getattr(rowObject, 'Portfolio', None)
            if portfolioFunc:
                return portfolioFunc()
            elif rowObject and (rowObject.IsKindOf(acm.FASQLQueryFolder) or rowObject.IsKindOf(acm.FStoredASQLQuery)):
                return rowObject
        except AttributeError:
            pass
        return None


class LimitMenuItem(FUxCore.MenuItem):

    def __init__(self, extObj, invokeFunc=None, enabledFunc=None, validateFunc=None):
        self._frame = extObj
        self._invokeFunc = invokeFunc
        self._enabledFunc = enabledFunc
        self._validateFunc = validateFunc

    def Enabled(self):
        if callable(self._enabledFunc):
            return self._enabledFunc(self._SelectedLimits())
        return bool(self._SelectedLimits())

    def Invoke(self, _eii):
        if callable(self._invokeFunc):
            self._invokeFunc(self._SelectedLimit())

    def _SelectedLimits(self):
        limits = []
        if hasattr(self._frame, 'ActiveSheet'):
            activeSheet = self._frame.ActiveSheet()
            if activeSheet:
                selection = activeSheet.Selection()
                if selection:
                    limits = [l for l in selection.SelectedRowObjects() \
                        if l.IsKindOf(acm.FLimit)]
        elif hasattr(self._frame, 'CustomLayoutApplication'):
            limit = self._frame.CustomLayoutApplication().EditLimit()
            if limit and limit.IsKindOf(acm.FLimit):
                limits = [limit, ]
        if callable(self._validateFunc):
            limits = [l for l in limits if self._validateFunc(l)]
        return limits

    def _SelectedLimit(self):
        limits = self._SelectedLimits()
        return limits[0] if limits else None


class LimitEventMenuItem(LimitMenuItem):

    def __init__(self, extObj, event):
        LimitMenuItem.__init__(self, extObj, validateFunc=lambda l: bool(l.BusinessProcess()))
        self._event = event

    def Enabled(self):
        limits = self._SelectedLimits()
        if not limits:
            return False
        for l in limits:
            if not FBusinessProcessUtils.IsValidEvent(l.BusinessProcess(), self._event):
                return False
        return True

    def Invoke(self, _eii):
        ExecuteEvent(self._SelectedLimits(), self._event, self._frame.Shell())


class LimitActivationMenuItem(LimitMenuItem):

    def __init__(self, extObj):
        LimitMenuItem.__init__(self, extObj,
            validateFunc=lambda l: bool(l.BusinessProcess()))

    def Checked(self):
        return self._IsSelectedLimitActive()

    def Enabled(self):
        limits = self._SelectedLimits()
        if limits:
            state = FLimitUtils.CurrentState(limits[0])
            limitsWithSameState = [l for l in limits if FLimitUtils.CurrentState(l) == state]
            return len(limitsWithSameState) == len(limits)
        return False

    def Invoke(self, _eii):
        limit = self._SelectedLimit()
        bp = limit.BusinessProcess()
        currentState = FLimitUtils.CurrentState(limit)
        deactivateEvent = 'Deactivate'
        activateEvent = 'Monitor Limit' if currentState == 'Ready' else 'Activate'
        event = deactivateEvent if self._IsSelectedLimitActive() else activateEvent
        if currentState == 'Ready' and limit.LimitSpecification().RealtimeMonitored():
            acm.UX().Dialogs().MessageBoxInformation(self._frame.Shell(),
                'New limits will automatically become active when monitored ' \
                'by the limit server.')
        elif bp and not FBusinessProcessUtils.IsValidEvent(bp, event):
            state = 'Active' if event == 'Activate' else 'Inactive'
            result = acm.UX().Dialogs().MessageBox(self._frame.Shell(), 'Question',
                '%s is not a valid event for current state "%s".\n\nWould you like ' \
                'to force to state "%s" instead?' % (event, currentState, state),
                'Yes', 'No', None, 'Button2', 'Button2')
            if result == 'Button1':
                for l in self._SelectedLimits():
                    bp = l.BusinessProcess()
                    bp.ForceToState(state)
                    bp.Commit()
        else:
            ExecuteEvent(self._SelectedLimits(), event, self._frame.Shell())

    def _IsSelectedLimitActive(self):
        limit = self._SelectedLimit()
        if limit:
            bp = limit.BusinessProcess()
            return bp and (FLimitUtils.IsActive(limit) or
                    FBusinessProcessUtils.IsValidEvent(bp, 'Deactivate'))
        return False


class LimitAddInfoMenuItem(LimitMenuItem):

    def __init__(self, extObj):
        # pylint: disable-msg=W0108
        LimitMenuItem.__init__(self, extObj,
            enabledFunc=lambda limits: bool(limits),
            validateFunc=lambda l: bool(l.IsRegisteredInStorage() or
                (l.IsClone() and l.Original().IsRegisteredInStorage())))

    def Invoke(self, _eii):
        if hasattr(self._frame, 'CustomLayoutApplication'):
            self._frame.CustomLayoutApplication().IsAddInfoDlgInitialised(True)
        acm.UX.Dialogs().EditAdditionalInfo(self._frame.Shell(),
            self._SelectedLimit())


class LimitCheckMenuItem(LimitMenuItem):

    def __init__(self, extObj):
        # pylint: disable-msg=W0108
        LimitMenuItem.__init__(self, extObj,
            enabledFunc=lambda limits: bool(limits),
            validateFunc=lambda l: bool(not l.Originator().IsInfant()))
           
    @staticmethod
    def _BuildAelParams(module, extraParam):
        params = {p[0]: p[3] for p in getattr(module, 'ael_variables')}
        params.update(extraParam)
        strParams = acm.FDictionary()
        for k, v in params.iteritems():
            strParams.AtPutStrings(k, v)
        return strParams
 
    @contextmanager
    def CreateTransientTask(self, context, module, extraParam):
        task = acm.FAelTask()
        task.ModuleName = module.__name__
        task.Parameters( self._BuildAelParams(module, extraParam) )
        task.RegisterInStorage()
        yield task
        task.Unsimulate()
        
    def Invoke(self, _eii):
        limits = (l.Originator() for l in self._SelectedLimits())
        extraParam = dict(Limits = ','.join((str(l.Oid()) for l in limits)))
        with self.CreateTransientTask(acm.GetDefaultContext(), FLimitCheck, extraParam) as task:
            acm.StartApplication("Run Script", task)

#------------------------------------------------------------------------------
# Dialog classes
#------------------------------------------------------------------------------

class ExecuteEventDialog(FUxCore.LayoutDialog):

    CAPTION = 'Execute Event'

    def __init__(self, limits, event):
        self._limits = limits
        self._event = event
        self._commentCtrl = None

    def CreateLayout(self):
        # pylint: disable-msg=R0201
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox()
        b.    AddInput('action', 'Limit action', 50)
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Comment')
        b.    AddText('comment', 200, 130)
        b.  EndBox()
        b.  BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b

    def HandleCreate(self, dialog, layout):
        dialog.Caption(self._GetCaption())
        self._commentCtrl = layout.GetControl('comment')
        actionCtrl = layout.GetControl('action')
        actionCtrl.SetData(self._event)
        actionCtrl.Editable(False)

    def HandleApply(self):
        return self._commentCtrl.GetData()

    def _GetCaption(self):
        maxLimits = 6
        if len(self._limits) == 1:
            caption =  self.CAPTION + ' - Limit ' + str(self._limits[0].Oid())
        else:
            caption = self.CAPTION + ' - Limits ' + \
                ', '.join([str(l.Oid()) for l in self._limits[:maxLimits]])
            caption += '...' if len(self._limits) > maxLimits else ''
        return caption


class ProtectionDialog(FUxCore.LayoutDialog):

    CAPTION = 'Protection'
    PROTECTION = {
        'World': {'Read': 9, 'Write': 10, 'Delete': 11},
        'Org.': {'Read': 6, 'Write': 7,  'Delete': 8},
        'Group': {'Read': 3, 'Write': 4,  'Delete': 5},
        'Owner': {'Read': 0, 'Write': 1,  'Delete': 2},
        }

    def __init__(self, businessObj, commitOnApply=False):
        self._businessObj = businessObj
        self._ownerCtrl = None
        self._rightCtrls = []
        self._commitOnApply = commitOnApply
        assert self._businessObj and self._businessObj.IsKindOf(acm.FBusinessObject)

    def PopulateOwnerCtrl(self):
        self._ownerCtrl.Populate([u for u in acm.FUser.Select(None).SortByProperty('Name')])
        self._ownerCtrl.SetData(acm.UserName())

    def PopulateProtectionCtrls(self):
        for ctrl in self._rightCtrls:
            for prot in ('Read/Write/Delete', 'Read/Write', 'Read', 'None'):
                ctrl.AddItem(prot)

    def InitOwnerControl(self):
        self.PopulateOwnerCtrl()
        self._ownerCtrl.SetData(self._businessObj.Owner())

    def RegisterRightCtrls(self, ctrl):
        if ctrl not in self._rightCtrls:
            self._rightCtrls.append(ctrl)
        return ctrl

    @staticmethod
    def GetBit(byteval, idx):
        return ((byteval & (1 << idx))!=0)

    @staticmethod
    def SetBit(idx):
        return 1 << idx

    def SetRights(self, ctrl, protection):
        level = ctrl.Label().split(' ')[0]
        data = ''.join(('%s/'%right for right in self.PROTECTION.get(level)
            if not self.GetBit(protection, self.PROTECTION[level][right])))
        ctrl.SetData(data[:-1] or 'None')

    def InitProtectionControls(self):
        self.PopulateProtectionCtrls()
        for ctrl in self._rightCtrls:
            self.SetRights(ctrl, self._businessObj.Protection())

    def RegisterControls(self, layout):
        self._ownerCtrl = layout.GetControl('owner')
        self.RegisterRightCtrls(layout.GetControl('ownerRights'))
        self.RegisterRightCtrls(layout.GetControl('groupRights'))
        self.RegisterRightCtrls(layout.GetControl('orgRights'))
        self.RegisterRightCtrls(layout.GetControl('worldRights'))

    def HandleCreate(self, dialog, layout):
        dialog.Caption(self.CAPTION)
        self.RegisterControls(layout)
        self.InitOwnerControl()
        self.InitProtectionControls()

    def Rights(self, ctrl):
        level = ctrl.Label().split(' ')[0]
        protection = 0
        for right in self.PROTECTION.get(level):
            if right not in ctrl.GetData():
                protection += self.SetBit(self.PROTECTION[level][right])
        return protection

    def HandleApply(self):
        protection = 0
        for ctrl in self._rightCtrls:
            protection += self.Rights(ctrl)
        owner = self._ownerCtrl.GetData()

        if protection != self._businessObj.Protection():
            self._businessObj.Protection(protection)
        if owner != self._businessObj.Owner():
            self._businessObj.Owner(owner)

        if self._commitOnApply and self._businessObj.IsModified():
            self._businessObj.Commit()
        return True

    def CreateLayout(self):
        # pylint: disable-msg=R0201
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('EtchedIn')
        b.   AddPopuplist('owner', 'Owner')
        b.   AddOption('ownerRights', 'Owner rights')
        b.   AddOption('groupRights', 'Group rights', 20)
        b.   AddOption('orgRights', 'Org. rights', 20)
        b.   AddOption('worldRights', 'World rights', 20)
        b.  EndBox()
        b.  BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b


class LimitTemplateDialog(FUxCore.LayoutDialog):
    # pylint: disable-msg=R0902

    CAPTION = 'Create Limit Template'

    def __init__(self, limit):
        self._limit = limit
        self._template = FLimitTemplate.CreateFromLimit(limit)
        self._module = self._GetDefaultModule()
        self._dialog = None
        self._nameCtrl = None
        self._descriptionCtrl = None
        self._moduleCtrl = None
        self._comparisonOperatorCtrl = None
        self._warningCtrl = None
        self._thresholdCtrl = None
        self._checkValueTypeCtrl = None
        self._warningTypeCtrl = None
        self._bindings = None
        self._InitDataBindingControls()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('EtchedIn', 'Limit template')
        b.    AddInput('name', 'Name', 60)
        b.    AddInput('description', 'Description')
        b.    BeginHorzBox('None')
        b.      AddInput('module', 'Module')
        b.      AddButton('moduleSelect', '...', False, True)
        b.    EndBox()
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Details')
        b.    AddInput('path', 'Limits created on')
        b.    AddInput('spec', 'Limit specification')
        b.    AddInput('grouper', 'Grouper')
        b.    AddInput('column', 'Column ID')
        b.    AddInput('columnParameters', 'Column Parameters')
        b.    AddInput('sheetType', 'Sheet type')
        b.    BeginHorzBox('EtchedIn', 'Default values')
        b.      BeginHorzBox()
        b.        BeginVertBox('None')
        b.          BeginHorzBox()
        b.            AddOption('checkValueType', 'Breach when', 20)
        self._comparisonOperatorCtrl.BuildLayoutPart(b, '')
        b.          EndBox()
        self._thresholdCtrl.BuildLayoutPart(b, 'Default threshold value')
        b.          BeginHorzBox()
        self._warningCtrl.BuildLayoutPart(b, 'Default warning value')
        b.            AddOption('warningType', '', 16, 16)
        b.          EndBox()
        b.        EndBox()
        b.        AddFill()
        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b

    def HandleCreate(self, dialog, layout):
        self._dialog = dialog
        self._dialog.Caption(self.CAPTION)
        ctrl = layout.GetControl

        self._nameCtrl = ctrl('name')
        self._nameCtrl.SetData(self._template.Name())
        self._descriptionCtrl = ctrl('description')
        self._descriptionCtrl.SetData(self._template.Description())
        self._moduleCtrl = ctrl('module')
        self._moduleCtrl.SetData(self._module.Name())
        self._moduleCtrl.Editable(False)
        ctrl('moduleSelect').AddCallback('Activate', self._OnSelectModule, None)

        ctrl('path').SetData(self._GetDisplayPath())
        ctrl('spec').SetData(self._template.LimitSpecificationName())
        ctrl('grouper').SetData(self._template.GrouperName())
        ctrl('column').SetData(self._template.ColumnName())
        ctrl('columnParameters').SetData(self._template.ColumnParameters())
        ctrl('sheetType').SetData(FLimitUtils.SheetTypeDisplayName(self._template.SheetClass()))
        for name in ('path', 'spec', 'grouper', 'column', 'columnParameters', 'sheetType'):
            ctrl(name).Enabled(False)

        self._comparisonOperatorCtrl.InitLayout(layout)
        self._comparisonOperatorCtrl.SetValue(
            FLimitUtils.ComparisonOperatorAsSymbol(self._template.ComparisonOperator()))
        self._warningCtrl.InitLayout(layout)
        self._warningCtrl.SetValue(self._template.WarningValue())
        self._thresholdCtrl.InitLayout(layout)
        self._thresholdCtrl.SetValue(self._template.Threshold())

        self._checkValueTypeCtrl = ctrl('checkValueType')
        for item in acm.FChoiceList['Limit Transform Function'].Choices():
            self._checkValueTypeCtrl.AddItem(item.Name())
        self._checkValueTypeCtrl.SetData(self._template.TransformFunction())

        self._warningTypeCtrl = ctrl('warningType')
        self._warningTypeCtrl.AddItem('Absolute')
        self._warningTypeCtrl.AddItem('Percent')
        self._warningTypeCtrl.SetData('Percent'
                if self._template.PercentageWarning() else 'Absolute')
        self._warningTypeCtrl.AddCallback('Changed', self._OnWarningTypeChanged, None)

        if self._template.ComparisonOperator() in ('Equal', 'Not Equal'):
            self._warningCtrl.Enabled(False)
            self._warningTypeCtrl.Enabled(False)

    def ServerUpdate(self, _sender, symbol, binder):
        if str(symbol) != 'ControlValueChanged':
            return
        if binder == self._comparisonOperatorCtrl:
            self._template.ComparisonOperator(
                FLimitUtils.ComparisonOperatorAsEnum(binder.GetValue()))
        warningEnabled = self._template.ComparisonOperator() not in ('Equal', 'Not Equal')
        self._warningCtrl.Enabled(warningEnabled)
        self._warningTypeCtrl.Enabled(warningEnabled)
        if not warningEnabled:
            self._warningCtrl.SetValue(self._thresholdCtrl.GetValue())

    def HandleApply(self):
        name = self._nameCtrl.GetData()
        self._template.Name(name)
        self._template.Description(self._descriptionCtrl.GetData())
        self._template.ComparisonOperator(
            FLimitUtils.ComparisonOperatorAsEnum(self._comparisonOperatorCtrl.GetValue()))
        self._template.WarningValue(self._warningCtrl.GetValue())
        self._template.Threshold(self._thresholdCtrl.GetValue())
        self._template.TransformFunction(self._checkValueTypeCtrl.GetData())
        self._template.PercentageWarning(self._warningTypeCtrl.GetData() == 'Percent')
        try:
            if (FLimitTemplate.CreateFromExtension(name, self._module) and
                not self._ConfirmOverwriteExtension()):
                return None
        except ValueError:
            pass
        try:
            self._template.SaveToModule(self._module)
            logger.info('Saved limit template "%s" in extension module "%s".',
                        name,
                        self._module.Name())
            return self._template
        except StandardError as e:
            msg = 'Failed to save template "%s":\n%s' % (name, e)
            acm.UX().Dialogs().MessageBox(self._dialog.Shell(), 'Error',
                msg, 'OK', None, None, 'Button1', 'Button1')
            return None

    def _OnSelectModule(self, _args, _cd):
        modules = [m for m in acm.GetDefaultContext().Modules() if not m.IsBuiltIn()]
        selected = acm.UX().Dialogs().SelectObject(self._dialog.Shell(), 'Select Module',
            'Extension Modules', modules, self._module)
        if selected:
            self._module = selected
            self._moduleCtrl.SetData(self._module.Name())

    def _OnWarningTypeChanged(self, _args, _cd):
        self._template.WarningValue(self._warningCtrl.GetValue() or 0)
        self._template.Threshold(self._thresholdCtrl.GetValue())
        self._template.ComparisonOperator(
            FLimitUtils.ComparisonOperatorAsEnum(self._comparisonOperatorCtrl.GetValue()))
        if self._template.WarningValue() is not None and self._template.Threshold() is not None:
            percentageWarning = bool(self._warningTypeCtrl.GetData() == 'Percent')
            if percentageWarning != self._template.PercentageWarning():
                value = FLimitUtils.WarningPercentage(self._template) if percentageWarning \
                        else FLimitUtils.WarningValue(self._template)
                self._template.PercentageWarning(percentageWarning)
                self._warningCtrl.SetValue(value)

    def _InitDataBindingControls(self):
        self._bindings = acm.FUxDataBindings()
        self._comparisonOperatorCtrl = self._bindings.AddBinder('comparison', 'string',
            None, FLimitUtils.ComparisonOperatorSymbols())
        formatter = acm.Get('formats/LimitValues')
        self._warningCtrl = self._bindings.AddBinder('warningValue', 'double', formatter)
        self._thresholdCtrl = self._bindings.AddBinder('threshold', 'double', formatter)
        self._bindings.AddDependent(self)

    def _GetDisplayPath(self):
        path = ['<Portfolio>']
        path.extend([str(p) for p in FLimitUtils.ConstraintsArray(self._limit)][1:])
        return ' / '.join(path)

    def _ConfirmOverwriteExtension(self):
        result = acm.UX().Dialogs().MessageBox(self._dialog.Shell(), 'Question',
                'Limit template "%s" already exists. Overwrite it?' % (self._template.Name()),
                'Yes', 'No', None, 'Button2', 'Button2')
        return bool(result == 'Button1')

    @staticmethod
    def _GetDefaultModule():
        # pylint: disable-msg=E1101
        module = acm.GetDefaultContext().EditModule()
        defModuleName = FLimitSettings.DefaultLimitTemplateModule()
        if defModuleName:
            customModule = acm.GetDefaultContext().GetModule(defModuleName)
            if not customModule:
                logger.info("Invalid default module '%s': module could not be found in context '%s'",
                            defModuleName,
                            acm.GetDefaultContext().Name())
            elif customModule.IsBuiltIn():
                logger.info("Invalid default module '%s': cannot be a built-in module", defModuleName)
            else:
                module = customModule
        return module