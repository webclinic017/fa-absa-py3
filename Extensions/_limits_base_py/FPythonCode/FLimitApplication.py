""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitApplication.py"
"""--------------------------------------------------------------------------
MODULE
    FLimitApplication

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    A custom application used in the creation and management of limit
    objects.

-----------------------------------------------------------------------------"""
import acm
import FUxCore
import FLimitSettings
import FLimitTemplate
import FLimitUtils
import FLimitActions
import FLimitViewer
import FAssetManagementUtils
from FLimitTreeSpecification import LimitTreeSpecification

from contextlib import contextmanager

logger = FAssetManagementUtils.GetLogger()

def CreateApplicationInstance():
    return LimitApplication()


class LimitApplication(FUxCore.LayoutApplication):
    # pylint: disable-msg=E1101,W0108,R0201,R0902,R0904

    _LIMIT_UNIQUE_ATTRS = ('WarningValue', 'Threshold', 'ComparisonOperator',
            'Owner', 'Protection', 'TransformFunction', 'PercentageWarning',
            'Name')

    _LIMIT_TARGET_ATTRS = ('CalculationEnvironment', )

    def __init__(self):
        FUxCore.LayoutApplication.__init__(self)
        self._templatePane = None
        self._ownerPane = None
        self._editLimit = None
        self._originalLimit = None
        self._limitSpec = None
        self._limitTarget = None
        self._targetCell = None
        self._originObject = None
        self._initialised = False
        self._addInfoInitialised = False
        self._errorMessage = ''
        self._panes = []
        self._externalSheetType = None

    def GetCurrentObject(self):
        return self.OriginalLimit() or self.OriginObject()

    def EditLimit(self):
        return self._editLimit

    def OriginalLimit(self):
        return self._originalLimit

    def LimitSpecification(self, limitSpec=None):
        if not limitSpec:
            return self._limitSpec
        self._limitSpec = limitSpec
        self._SetEditLimit(useTemplate=bool(not self.EditLimit()))
        self._UpdateControls()

    def LimitTarget(self, limitTarget=None):
        if not limitTarget:
            return self._limitTarget
        self._limitTarget = limitTarget
        self._SetEditLimit(useTemplate=True)
        self._UpdateControls()

    def TargetCell(self):
        return self._targetCell

    def OriginObject(self):
        return self._originObject

    def IsAddInfoDlgInitialised(self, initialised=None):
        if initialised is None:
            return self._addInfoInitialised
        self._addInfoInitialised = initialised

    def CanHandleObject(self, obj):
        supportedClasses = (acm.FLimit, acm.FPair, acm.FPortfolio,
                acm.FStoredASQLQuery, acm.FASQLQuery, acm.FInstrumentFilter)
        return bool(not obj or [obj.IsKindOf(c) for c in supportedClasses])

    def HandleCreate(self, createContext):
        self._templatePane = LimitTemplatePane(self, self._originObject)
        self.Frame().CreateCustomDockWindow(self._templatePane,
                LimitTemplatePane.KEY, 'Limit Template', 'Top', None, True, False)

        def AddPane(paneClass):
            pane = paneClass(self)
            layout = createContext.AddPane(
                    pane.CreateLayout(), paneClass.__name__)
            pane.HandleCreate(layout)
            self._panes.append(pane)
        AddPane(LimitSpecificationPane)
        AddPane(LimitTargetDisplayPane)
        AddPane(LimitPane)

        self._SetCaption()
        self._UpdateControls()
        self.EnableOnIdleCallback(True)

    def HandleRegisterCommands(self, builder):
        la = FLimitActions
        commands = (
            # Item name, Name, Accelerator, Menu creation callback
            ('viewHistory', 'View History', 'Ctrl+H', la.CreateViewLimitHistoryMenuItem),
            ('viewTarget', 'View Target', 'Ctrl+T', la.CreateViewLimitTargetMenuItem),
            ('viewSpecification', 'View Specification',
                    'Ctrl+I', la.CreateViewLimitSpecificationMenuItem),
            ('viewParent', 'View Parent', 'Ctrl+P', la.CreateViewLimitParentMenuItem),
            ('viewTemplates', 'Apply Template', 'Ctrl+A', ViewLimitTemplatesMenuItem),
            ('createTemplate', 'Create Template', 'Ctrl+Shift+T', la.CreateLimitTemplateMenuItem),
            ('active', 'Active', '', la.CreateLimitActiveMenuItem),
            ('investigateBreach', 'Investigate Breach', '', la.CreateInvestigateEventMenuItem),
            ('acceptBreach', 'Accept Breach', '', la.CreateAcceptBreachEventMenuItem),
            ('fileSendAsMessage', 'Send As Message', 'Ctrl+M', la.CreateSendLimitMessageMenuItem),
            ('viewTransHist', 'Transaction History', '', la.CreateLimitTransactionHistoryMenuItem),
            ('viewProtection', 'Protection', '', la.CreateLimitProtectionMenuItem),
            ('additionalInfo', 'Add Info', '', la.CreateLimitAddInfoMenuItem),
            ('limitCheck', 'Manual Check', '', la.CreateLimitCheckMenuItem),
            )
        def CreateMenuItemCallback(callback):
            def CreateMenuItem():
                return callback(self.Frame())
            return CreateMenuItem

        limitCommands = []
        for cmd, name, accelerator, callback in commands:
            # Item name, Parent, Path, Tooltip Text, Accelerator, Mnemonic, Callback, Default
            limitCommands.append([cmd, 'Data', name, '', accelerator,
                    '', CreateMenuItemCallback(callback), False])
        fileCommands = acm.FSet()
        fileCommands.AddAll(['FileNewWindow', 'FileOpen', 'FileOpenAdvanced',
                'FileSave', 'FileSaveNew', 'FileRevert', 'FileDelete'])
        builder.RegisterCommands(FUxCore.ConvertCommands(limitCommands), fileCommands)

    def HandleGetContents(self):
        return self.GetCurrentObject()

    def HandleSetContents(self, contents):
        obj = contents
        if type(contents) == FLimitActions.SheetObject:
            obj = contents.Object()
        if self.CanHandleObject(obj):
            self.HandleObject(contents)

    def HandleCreateStatusBar(self, sb):
        self._ownerPane = sb.AddTextPane(200)
        self._ownerPane.SetDefaultActionCallback(self.OnOwnerPanelDoubleClick, self)

    def HandleObject(self, obj):
        if type(obj) == FLimitActions.SheetObject:
            self._externalSheetType = obj.SheetType()
            obj = obj.Object()
        if self.CanHandleObject(obj) and self._ConfirmDiscardUnsavedChanges():
            oldOriginObject = self.OriginObject()
            if not obj or obj.IsKindOf(acm.FLimit):
                self._HandleLimit(obj)
            elif obj and obj.IsKindOf(acm.FPair):
                self._HandleLimitTargetAndCell(obj.First(), obj.Second())
            else:
                self._HandleOriginObject(obj)
            if self._IsLimitTemplatePaneEnabled() and self.OriginObject() != oldOriginObject:
                self._templatePane.OnNewOriginObject()
            self._UpdateControls()
            self._SetCaption()

    def HandleOnIdle(self):
        if not self._initialised:
            # A nasty workaround to avoid a problem whereby the limit specification control
            # does not initially display correctly if initialised with a value
            self._initialised = True
            self._panes[1].SetFocus()
        if self._errorMessage:
            # Error messages from subscription callbacks are deferred to a popup here
            text = self._errorMessage
            self._errorMessage = ''
            acm.UX().Dialogs().MessageBoxInformation(self.Shell(), text)
        if self._ownerPane:
            try:
                self._ownerPane.SetText('Owner: ' +
                        str(self.EditLimit().Owner().Name()) if self.EditLimit() else '')
            except Exception:
                pass

    def HandleStandardFileCommandInvoke(self, commandName):
        callback = getattr(self, 'On' + commandName, None)
        if callable(callback):
            callback()

    def _IsLimitTargetChanged(self):
        editTarget = self.EditLimit().LimitTarget()
        originalTarget = self.OriginalLimit().LimitTarget()
        for a in self._LIMIT_TARGET_ATTRS:
            if getattr(editTarget, a)() != getattr(originalTarget, a)():
                return True
        return False

    def _IsLimitChanged(self):
        return bool(self.EditLimit()) and bool(self.EditLimit().Difference(self.OriginalLimit(), True))

    def HandleStandardFileCommandEnabled(self, commandName):
        if commandName in ('FileRevert', 'FileSave'):
            return bool(self.OriginalLimit() and
                (self._IsLimitChanged() or
                 self._IsLimitTargetChanged()))
        elif commandName == 'FileSaveNew':
            return bool(self.EditLimit() and
                (self._IsLimitChanged() or
                self._IsLimitTargetChanged()))
        elif commandName == 'FileDelete':
            return bool(self.OriginalLimit())
        return True

    def HandleClose(self):
        close = self._ConfirmDiscardUnsavedChanges()
        if close:
            self._SetDependentAttribute('_originalLimit', None)
            self._SetDependentAttribute('_originObject', None)
        return close

    def GetApplicationIcon(self):
        limit = self.OriginalLimit() or self.EditLimit()
        return limit.Icon() if limit else 'Protection'

    def DoChangeCreateParameters(self, params):
        params.UseSplitter(False)
        params.SplitHorizontal(False)
        params.LimitMinSize(True)
        params.AutoShrink(True)
        params.AdjustPanesWhenResizing(True)

    def ServerUpdate(self, sender, symbol, _params):
        if str(symbol) == 'delete':
            # Error popup is deferred to OnIdle handler, to prevent locking the main thread during
            # the callback. Doing so can cause issues for the limit sheet when removing row objects.
            self._errorMessage = '{0} ({1}) has been deleted.'.format(
                'Limit' if sender.IsKindOf(acm.FLimit) else 'Limit''s targeted object',
                str(sender.Oid()))
            self._editLimit = self._originalLimit
            self.HandleObject(None)
        elif (sender == self.OriginalLimit() and not sender.IsModified() and
              sender.VersionId() > self.EditLimit().VersionId()):
            with self._AddInfoDlgHandler(sender) as isAddInfoDlgInitialised:
                if not isAddInfoDlgInitialised:
                    text = 'Limit %s has been modified. Revert to modified limit?' % (sender.Oid())
                    result = acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Question', text)
                    if result == 'Button1':
                        self._editLimit = self._originalLimit
                        self.OnFileRevert()
                    else:
                        self.EditLimit().VersionId(sender.VersionId())

    def OnOwnerPanelDoubleClick(self, shell, _cd):
        if self.EditLimit():
            FLimitActions.ViewLimitProtection(self.EditLimit(), shell)

    def OnFileNewWindow(self):
        acm.UX().SessionManager().StartApplication('Limit', None)

    def OnFileOpen(self):
        selectedObject = acm.UX().Dialogs().SelectObject(
                self.Shell(), 'Select Limit', 'Limits',
                acm.FLimit.Select('').SortByProperty('Name'), self.OriginalLimit())
        if selectedObject:
            self.HandleObject(selectedObject)

    def OnFileOpenAdvanced(self):
        obj = acm.UX().Dialogs().SelectObjectsInsertItems(self.Shell(), acm.FLimit, False)
        if obj:
            self.HandleObject(obj)

    def Differences(self):
        return self.OriginalLimit().Difference(self.EditLimit()).Differences()

    def OnlyNameChanged(self):
        try:
            differences = self.Differences()
            return str(differences.Element().AssociationKey()) == 'name'
        except Exception:
            return False

    def UpdateChildren(self):
        originalLimit = self.OriginalLimit()
        return bool(originalLimit.IsParent() and
            self.HasChildren(originalLimit) and
            not self.OnlyNameChanged())

    def OnPreSave(self, limit):
        for pane in self._panes:
            try:
                pane.OnPreSave(limit)
            except AttributeError:
                pass

    def OnFileSave(self):
        originalLimit = self.OriginalLimit()
        editLimit = self.EditLimit()
        self.OnPreSave(editLimit)
        try:
            updateChildren = self.UpdateChildren()
            if updateChildren:
                text = 'Do you want to update existing child limits?'
                result = acm.UX().Dialogs().MessageBox(self.Shell(), 'Question', text, 'All', 'Unmodified', 'No', 'Button3', 'Button3')
                updateChildren = {'Button1': 1, 'Button2': 2, 'Button3': 3}.get(result)
            acm.BeginTransaction()
            originalLimit.RemoveDependent(self)
            if updateChildren != 3:
                uniqueChildAttrs = [a for a in  self._LIMIT_UNIQUE_ATTRS if a != 'Name']
                for child in originalLimit.Children():
                    child = child.StorageImage()
                    if updateChildren == 2:
                        equalAttrs = [a for a in uniqueChildAttrs \
                                if getattr(child, a)() == getattr(originalLimit, a)()]
                        if len(uniqueChildAttrs) != len(equalAttrs):
                            continue
                    for attr in uniqueChildAttrs:
                        setattr(child, attr, getattr(editLimit, attr)())
                    child.Commit()
            originalLimit.Apply(editLimit)
            originalLimit.Commit()
            acm.CommitTransaction()
        except Exception as e:
            originalLimit.Undo()
            originalLimit.AddDependent(self)
            acm.AbortTransaction()
            self._ShowErrorMessage('Error saving limit: ' + str(e))
        else:
            self._editLimit = None
            self.HandleObject(originalLimit)

    def OnFileSaveNew(self):
        if self.OriginalLimit():
            text = 'Do you really want to create a new limit?'
            result = acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Question', text)
            if result != 'Button1':
                return
            newLimit = self.EditLimit().StorageImage()
            newLimit.StorageSetNew()
        else:
            newLimit = self.EditLimit().StorageNew()
        self.OnPreSave(newLimit)
        try:
            newLimit.Parent(None)
            newLimit.Commit()
        except Exception as e:
            self._ShowErrorMessage('Error saving new limit: ' + str(e))
        else:
            self._editLimit = None
            self._SetDependentAttribute('_originalLimit', None)
            self._UpdateLimitViewers()
            self.HandleObject(newLimit)

    def OnFileDelete(self):
        limit = self.OriginalLimit()
        text = 'Are you sure you want to delete Limit %d?' % limit.Oid()
        result = acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Question', text)
        if result == 'Button1':
            try:
                limit.RemoveDependent(self)
                limit.Delete()
            except Exception as e:
                limit.AddDependent(self)
                self._ShowErrorMessage('Error deleting limit: ' + str(e))
            else:
                self._editLimit = self._originalLimit = None
                self.HandleObject(None)

    def OnFileRevert(self):
        self.HandleObject(self.OriginalLimit())

    @staticmethod
    def HasChildren(originalLimit):
        return bool(originalLimit.Children())

    @staticmethod
    def _GetDefaultLimitSpecification():
        limitSpec = acm.FLimitSpecification[FLimitSettings.DefaultLimitSpecificationName()]
        if not limitSpec:
            fromDate = acm.Time().DateAddDelta(acm.Time().DateNow(), 0, -1, 0)
            whereClause = "createUser='%s' and createTime > '%s'" % (acm.User().Name(), fromDate)
            recentLimits = acm.FLimit.Select(whereClause).SortByProperty('CreateTime', False)
            if recentLimits:
                limitSpec = recentLimits.First().LimitSpecification()
        return limitSpec

    @contextmanager
    def _AddInfoDlgHandler(self, sender):
        yield self._addInfoInitialised
        if self._addInfoInitialised:
            self.EditLimit().VersionId(sender.VersionId())
            self._addInfoInitialised = False

    def _ConfirmDiscardUnsavedChanges(self):
        if self._IsLimitChanged():
            text = 'The current limit has not been saved.\nDo you wish to disregard changes?'
            result = acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Question', text)
            if result != 'Button1':
                return False
        return True

    def _IsLimitTemplatePaneEnabled(self):
        return bool(self._templatePane and self.Frame().IsDockWindowVisible(LimitTemplatePane.KEY))

    def _UpdateControls(self):
        for pane in self._panes:
            pane.UpdateControls()

    def _SetCaption(self):
        limit = self.OriginalLimit()
        self.SetContentCaption(str(limit.Oid()) if limit else '')

    def _HandleLimit(self, limit):
        self._SetDependentAttribute('_originalLimit', limit)
        self._limitSpec = limit.LimitSpecification() if limit else None
        self._limitTarget = limit.LimitTarget() if limit else None
        self._targetCell = None
        self._SetDependentAttribute('_originObject',
                self._limitTarget.TreeSpecification().OriginObject() if self._limitTarget else None)
        self._SetEditLimit()

    def _HandleLimitTargetAndCell(self, limitTarget, cell):
        self._SetDependentAttribute('_originalLimit', None)
        self._limitSpec = self._GetDefaultLimitSpecification()
        self._limitTarget = limitTarget
        self._targetCell = cell
        self._SetDependentAttribute('_originObject',
                self._limitTarget.TreeSpecification().OriginObject() if self._limitTarget else None)
        self._SetEditLimit()

    def _HandleOriginObject(self, originObject):
        self._SetDependentAttribute('_originalLimit', None)
        self._limitSpec = self._GetDefaultLimitSpecification()
        self._limitTarget = None
        self._targetCell = None
        self._SetDependentAttribute('_originObject', originObject)
        self._SetEditLimit()
        frame = self.Frame()
        if frame:
            frame.ShowDockWindow(LimitTemplatePane.KEY)

    def _SetDependentAttribute(self, attributeName, value):
        attribute = getattr(self, attributeName)
        if attribute is not None:
            attribute.RemoveDependent(self)
        setattr(self, attributeName, value)
        if value is not None:
            value.AddDependent(self)

    def _SetEditLimit(self, useTemplate=False):
        if self.OriginalLimit():
            self._editLimit = self.OriginalLimit().StorageImage()
        elif self.LimitTarget() and self.LimitSpecification():
            oldEditLimit = self._editLimit
            template = self._templatePane.LimitTemplate() if self._templatePane else None
            self._editLimit = self.LimitSpecification().CreateLimit(self.LimitTarget())
            self._editLimit.RegisterInStorage()
            if useTemplate and self._IsLimitTemplatePaneEnabled() and template:
                template.ApplyToLimit(self._editLimit)
            elif oldEditLimit:
                for attr in self._LIMIT_UNIQUE_ATTRS:
                    setterFunc = getattr(self._editLimit, attr)
                    setterFunc(getattr(oldEditLimit, attr)())
            else:
                cell = self.TargetCell()
                defaultValue = self._GetDefaultValueFromCell(cell) if cell else 0
                try:
                    self._editLimit.TransformFunction(FLimitSettings.DefaultTransformFunction())
                except TypeError:
                    self._editLimit.TransformFunction(None)
                self._editLimit.PercentageWarning(FLimitSettings.DefaultPercentageWarning())
                self._editLimit.ComparisonOperator('Greater')
                self._editLimit.Threshold(defaultValue)
                self._editLimit.WarningValue(defaultValue \
                        if not self._editLimit.PercentageWarning() else \
                        FLimitSettings.DefaultWarningPercentageValue())
        else:
            self._editLimit = None

    def _ShowErrorMessage(self, message):
        acm.Log(message)
        acm.UX().Dialogs().MessageBox(self.Shell(), 'Error', message,
                'OK', None, None, 'Button1', 'Button1')

    @staticmethod
    def _GetDefaultValueFromCell(cell):
        try:
            value = cell.Value()
            value = FLimitUtils.SuggestedLimitValue(float(value))
        except AttributeError:
            pass
        except (TypeError, ValueError):
            value = float('nan')
        return value

    @staticmethod
    def _UpdateLimitViewers():
        try:
            for frame in acm.ApplicationList():
                if frame and frame.IsKindOf(acm.FUiTrdMgrFrame):
                    FLimitViewer.UpdateLimitUtilityView(frame)
        except Exception:
            pass


class LimitSpecificationPane(FUxCore.LayoutPanel):

    def __init__(self, parent):
        self._parent = parent
        self._limitSpecCtrl = None
        self._newButton = None
        self._typeCtrl = None
        self._descriptionCtrl = None
        self._realtimeCtrl = None
        self._bindings = None
        self._InitDataBindingControls()

    def HandleCreate(self, layout):
        self._limitSpecCtrl.InitLayout(layout)
        self._newButton = layout.GetControl('limitSpecNew')
        self._newButton.AddCallback('Activate', self.OnViewLimitSpecification, None)
        self._typeCtrl = layout.GetControl('limitSpecType')
        self._typeCtrl.Editable(False)
        self._descriptionCtrl = layout.GetControl('limitSpecDesc')
        self._descriptionCtrl.Editable(False)
        self._realtimeCtrl = layout.GetControl('realtime')
        self._realtimeCtrl.Enabled(False)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('EtchedIn', 'Limit specification')
        b.    BeginHorzBox()
        self._limitSpecCtrl.BuildLayoutPart(b, 'Name')
        b.      AddButton('limitSpecNew', 'New...')
        b.    EndBox()
        b.    BeginHorzBox()
        b.      AddInput('limitSpecType', 'Type')
        b.      AddCheckbox('realtime', 'Realtime monitored')
        b.    EndBox()
        b.    AddInput('limitSpecDesc', 'Description')
        b.  EndBox()
        b.EndBox()
        return b

    def ServerUpdate(self, _sender, symbol, binder):
        if str(symbol) != 'ControlValueChanged':
            return
        if binder == self._limitSpecCtrl:
            self._parent.LimitSpecification(binder.GetValue())

    def OnViewLimitSpecification(self, _params, _cd):
        # pylint: disable-msg=R0201
        acm.StartApplication('Limit Specification', None)

    def UpdateControls(self):
        ls = self._parent.LimitSpecification()
        self._limitSpecCtrl.SetValue(ls)
        limit = self._parent.OriginalLimit()
        limitSpecEnabled = bool(not limit)
        self._limitSpecCtrl.Enabled(limitSpecEnabled)
        self._newButton.Enabled(limitSpecEnabled)
        self._typeCtrl.SetData(ls.LimitType() if ls else '')
        self._descriptionCtrl.SetData(ls.Description() if ls else '')
        self._realtimeCtrl.Checked(ls.RealtimeMonitored() if ls else False)

    def _InitDataBindingControls(self):
        self._bindings = acm.FUxDataBindings()
        self._limitSpecCtrl = self._bindings.AddBinder('limitSpec', 'FLimitSpecification')
        self._bindings.AddDependent(self)


class LimitTargetDisplayPane(FUxCore.LayoutPanel):

    def __init__(self, parent):
        self._parent = parent
        self._path = None
        self._targetCtrl = None
        self._columnCtrl = None
        self._sheetTypeCtrl = None
        self._grouperCtrl = None
        self._scenarioCtrl = None
        self._bucketCtrl = None
        self._calcEnvCtrl = None
        self._parametersCtrl = None
        self._parametersLabelCtrl = None

    def HandleCreate(self, layout):
        self._targetCtrl = layout.GetControl('target')
        self._columnCtrl = layout.GetControl('column')
        self._sheetTypeCtrl = layout.GetControl('sheetType')
        self._grouperCtrl = layout.GetControl('grouper')
        self._scenarioCtrl = layout.GetControl('scenario')
        self._bucketCtrl = layout.GetControl('buckets')
        self._calcEnvCtrl = layout.GetControl('calcEnv')
        self._parametersCtrl = layout.GetControl('parameters')
        self._parametersLabelCtrl = layout.GetControl('parametersLabel') 
        self._calcEnvCtrl.AddCallback('Changed', self._OnCalcEnvChanged, None)
        self._UpdateCalcEnvCtrl()
        self._calcEnvCtrl.ToolTip('Select Calculation Environment')
        self._targetCtrl.ShowColumnHeaders()
        self._targetCtrl.ShowHierarchyLines(True)
        self._targetCtrl.WordWrap(True)
        self._targetCtrl.ColumnWidth(0, 310)
        self._columnCtrl.Editable(False)
        self._sheetTypeCtrl.Editable(False)
        self._grouperCtrl.Editable(False)
        self._scenarioCtrl.Editable(False)
        self._bucketCtrl.Editable(False)
        self._parametersCtrl.AddColumn('Name')
        self._parametersCtrl.AddColumn('Value')
        self._parametersCtrl.ShowColumnHeaders()
        self._parametersCtrl.ShowGridLines()
        self._parametersCtrl.EnableHeaderSorting()

    def CreateLayout(self):
        # pylint: disable-msg=R0201
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('EtchedIn', 'Limit target')
        b.  BeginVertBox('None')
        b.    AddTree('target', 500, 140)
        b.    AddInput('sheetType', 'Sheet type')
        b.    AddInput('grouper', 'Grouper')
        b.    AddInput('column', 'Column')
        b.    AddInput('scenario', 'Scenario')
        b.    AddInput('buckets', 'Time Buckets')
        b.    AddOption('calcEnv', 'Environment')
        b.    AddLabel('parametersLabel', 'Column Parameters:')
        b.    AddList('parameters', 4)
        b.  EndBox()
        b.EndBox()
        return b

    def UpdateControls(self):
        self._UpdateCalcEnvCtrl()
        limitTarget = self._parent.LimitTarget() if self._parent.EditLimit() else None
        if not (limitTarget and (limitTarget.Path() == self._path)):
            self._UpdateTreeControl(limitTarget)
        self._UpdatePropertiesControls(limitTarget)
        
    def SetFocus(self):
        self._targetCtrl.SetFocus()

    def _UpdateTreeControl(self, limitTarget):
        self._targetCtrl.RemoveAllItems()
        if limitTarget:
            lastItem = self._targetCtrl.GetRootItem()
            for constraint in limitTarget.PathAsArray(True):
                item = lastItem.AddChild()
                item.Label(constraint.First(), 0)
                item.Icon(constraint.Second(), constraint.Second())
                lastItem = item
            lastItem.Select()

    def _UpdatePropertiesControls(self, limitTarget):
        if limitTarget:
            calcSpec = limitTarget.CalculationSpecification()
            treeSpec = limitTarget.TreeSpecification()

            self._path = limitTarget.Path()
            self._columnCtrl.SetData(limitTarget.ColumnLabel())
            self._sheetTypeCtrl.SetData(FLimitUtils.SheetTypeDisplayName(limitTarget.SheetType()))
            self._grouperCtrl.SetData(treeSpec.Grouper().DisplayName() \
                    if (treeSpec and treeSpec.Grouper()) else '')
            self._calcEnvCtrl.SetData(limitTarget.CalculationEnvironment())
            if calcSpec and calcSpec.Configuration():
                configParams = calcSpec.Configuration().ParamDict()
                scenario = configParams.At('scenario')
                if scenario:
                    displayType = limitTarget.ScenarioDisplayType()
                    self._scenarioCtrl.SetData((scenario.Name() + ' (' + displayType + ')') \
                            if displayType != 'Absolute' else scenario.Name())
                else:
                    self._scenarioCtrl.SetData('')
                buckets = configParams.At('vectorValue')
                self._bucketCtrl.SetData(buckets if buckets else '')
                self._UpdateColumnParameters(configParams)
            else:
                for ctrl in (self._scenarioCtrl, self._bucketCtrl):
                    ctrl.SetData('')
                self._parametersCtrl.RemoveAllItems()
        else:
            for ctrl in (self._columnCtrl, self._grouperCtrl, self._scenarioCtrl, self._bucketCtrl, self._calcEnvCtrl):
                ctrl.SetData('')
            self._path = ''
        self._scenarioCtrl.Visible(bool(self._scenarioCtrl.GetData()))
        self._bucketCtrl.Visible(bool(self._bucketCtrl.GetData()))
        hasParams = bool(self._parametersCtrl.GetRootItem().Children().Size())
        self._parametersCtrl.Visible(hasParams)
        self._parametersLabelCtrl.Visible(hasParams)

    def _UpdateCalcEnvCtrl(self):
        calcEnvs = acm.FStoredCalculationEnvironment.Select('').AsArray()
        calcEnvs.Add('')
        self._calcEnvCtrl.Populate(calcEnvs.Sort())

        limit = self._parent.OriginalLimit()
        calcEnvCtrlEnabled = bool(not limit)
        self._calcEnvCtrl.Enabled(calcEnvCtrlEnabled)
        if limit:
            self._calcEnvCtrl.SetData(limit.LimitTarget().CalculationEnvironment())

    def _OnCalcEnvChanged(self, _params, _cd):
        limit = self._parent.EditLimit()
        if limit:
            limit.LimitTarget().CalculationEnvironment(self._calcEnvCtrl.GetData() or None)
            
    def _GetColumnParameterDefinition(self, parameterName):
        try:
            parameterDef = acm.GetDefaultContext().GetExtension('FColumnParameterDefinition', 'FObject', parameterName).Value()
            parameterDef.Validate()
            return parameterDef
        except Exception:
            return None

    def _UpdateColumnParameters(self, configParams):
        self._parametersCtrl.RemoveAllItems()
        columnParameters = configParams.At('columnParameters')
        if columnParameters:
            root = self._parametersCtrl.GetRootItem()
            for columnParam in columnParameters.Keys():
                parameterDef = self._GetColumnParameterDefinition(columnParam)
                if parameterDef is not None:
                    child = root.AddChild()
                    child.Label(parameterDef.DisplayName(), 0)
                    child.Label(columnParameters.At(columnParam), 1)

class LimitPane(FUxCore.LayoutPanel):
    # pylint: disable-msg=R0902

    def __init__(self, parent):
        self._parent = parent
        self._limit = None
        self._subLevels = acm.FArray()
        self._subLevelCtrl = None
        self._currentStateCtrl = None
        self._comparisonOperatorCtrl = None
        self._warningCtrl = None
        self._nameCtrl = None
        self._thresholdCtrl = None
        self._checkValueTypeCtrl = None
        self._warningTypeCtrl = None
        self._bindings = None
        self._lastModifiedCtrl = None
        self._InitDataBindingControls()

    def HandleCreate(self, layout):
        self._subLevelCtrl.InitLayout(layout)
        self._currentStateCtrl.InitLayout(layout)
        self._warningCtrl.InitLayout(layout)
        self._thresholdCtrl.InitLayout(layout)
        self._comparisonOperatorCtrl.InitLayout(layout)
        self._nameCtrl.InitLayout(layout)

        self._currentStateCtrl.Editable(False)
        self._checkValueTypeCtrl = layout.GetControl('checkValueType')
        transformFunctionRoot = acm.FChoiceList['Limit Transform Function']
        if transformFunctionRoot:
            for transformFunction in transformFunctionRoot.Choices().SortByProperty('Name'):
                self._checkValueTypeCtrl.AddItem(transformFunction)
            self._checkValueTypeCtrl.SetData('Value')
        self._checkValueTypeCtrl.AddCallback('Changed', self._OnCheckValueTypeChanged, None)

        self._warningTypeCtrl = layout.GetControl('warningType')
        self._warningTypeCtrl.AddItem('Absolute')
        self._warningTypeCtrl.AddItem('Percent')
        self._warningTypeCtrl.SetData('Absolute')
        self._warningTypeCtrl.AddCallback('Changed', self._OnWarningTypeChanged, None)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('EtchedIn', 'Limit')
        b.    BeginHorzBox()
        b.      BeginVertBox('None')
        self._nameCtrl.BuildLayoutPart(b, 'Name')
        self._subLevelCtrl.BuildLayoutPart(b, 'Create limit(s) on')
        self._currentStateCtrl.BuildLayoutPart(b, 'Current state')
        b.        BeginHorzBox()
        b.          AddOption('checkValueType', 'Breach when', 20)
        self._comparisonOperatorCtrl.BuildLayoutPart(b, '')
        b.        EndBox()
        self._thresholdCtrl.BuildLayoutPart(b, 'Threshold value')
        b.        BeginHorzBox()
        self._warningCtrl.BuildLayoutPart(b, 'Warning value')
        b.          AddOption('warningType', '', 16, 16)
        b.        EndBox()
        b.      EndBox()
        b.      AddFill()
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b

    def ServerUpdate(self, sender, symbol, binder):
        if self._limit and sender == self._limit.BusinessProcess():
            self._currentStateCtrl.SetValue(self._limit.BusinessProcess().CurrentStep().State())
            return
        limit = self._parent.EditLimit()
        if str(symbol) == 'ControlModifyStarted':
            self._lastModifiedCtrl = binder
        if not limit or str(symbol) not in ('ControlValueChanged', 'ControlModifyStarted'):
            return
        self.UpdateLimit(limit, binder)

    def UpdateLimit(self, limit, binder):
        if binder == self._subLevelCtrl:
            lt = self._parent.LimitTarget()
            subLevel = self._subLevels.IndexOfFirstEqual(self._subLevelCtrl.GetValue())
            lt.SubLevel(subLevel)
            self._parent.LimitTarget(lt)
        elif binder == self._comparisonOperatorCtrl:
            limit.ComparisonOperator(FLimitUtils.ComparisonOperatorAsEnum(binder.GetValue()))
            self._UpdateWarningControls(limit)
        elif binder == self._warningCtrl:
            limit.WarningValue(binder.GetValue())
        elif binder == self._thresholdCtrl:
            limit.Threshold(binder.GetValue())
            self._UpdateWarningControls(limit)
        elif binder == self._nameCtrl:
            limit.Name(binder.GetValue())

    def OnPreSave(self, limit):
        self.UpdateLimit(limit, self._lastModifiedCtrl)

    def UpdateControls(self):
        self._UpdateCurrentStateControl()
        limit = self._parent.EditLimit()
        self._UpdateSubLevelControl(limit)
        self._UpdateConditionControls(limit)
        self._UpdatePropertiesControls(limit)
        self._UpdateNameControl(limit)

    def _InitDataBindingControls(self):
        self._bindings = acm.FUxDataBindings()
        self._subLevelCtrl = self._bindings.AddBinder('subLevel', 'string', None, self._subLevels)
        self._currentStateCtrl = self._bindings.AddBinder('state', 'string')
        self._comparisonOperatorCtrl = self._bindings.AddBinder('comparisonOperator', 'string',
                None, FLimitUtils.ComparisonOperatorSymbols())
        formatter = acm.Get('formats/LimitValues')
        self._warningCtrl = self._bindings.AddBinder('warningValue', 'double', formatter, None, True)
        self._thresholdCtrl = self._bindings.AddBinder('threshold', 'double', formatter, None, True)
        self._nameCtrl = self._bindings.AddBinder('name', 'string', None, None, True)
        self._bindings.AddDependent(self)

    def _UpdateSubLevelControl(self, limit):
        subLevelsEnabled = not self._parent.OriginalLimit() and bool(self._parent.TargetCell())
        self._subLevelCtrl.Visible(subLevelsEnabled)
        if subLevelsEnabled and self._subLevels.IsEmpty():
            self._subLevels.Clear()
            self._subLevels.AddAll(self._GetSubLevelsForCell(self._parent.TargetCell()))
            self._subLevelCtrl.SetValue(self._subLevels.At(0))
        self._subLevelCtrl.Enabled(limit and subLevelsEnabled and self._subLevels.Size() > 1)

    def _UpdateCurrentStateControl(self):
        if self._parent.OriginalLimit() != self._limit:
            if self._limit and self._limit.BusinessProcess():
                self._limit.BusinessProcess().RemoveDependent(self)
            self._limit = self._parent.OriginalLimit()
            if self._limit and self._limit.BusinessProcess():
                self._limit.BusinessProcess().AddDependent(self)
        self._currentStateCtrl.Visible(bool(self._limit))
        self._currentStateCtrl.SetValue(self._limit.BusinessProcess().CurrentStep().State() \
            if self._limit and self._limit.BusinessProcess() else '')

    def _UpdateConditionControls(self, limit):
        self._warningCtrl.SetValue(limit.WarningValue() if limit else 0)
        self._warningCtrl.Enabled(limit and FLimitUtils.IsWarningEnabled(limit))
        self._thresholdCtrl.SetValue(limit.Threshold() if limit else 0)
        self._thresholdCtrl.Enabled(bool(limit))
        self._comparisonOperatorCtrl.SetValue(
                FLimitUtils.ComparisonOperatorAsSymbol(limit.ComparisonOperator()) \
                if limit else '>')
        self._comparisonOperatorCtrl.Enabled(bool(limit))

    def _UpdateNameControl(self, limit):
        self._nameCtrl.SetValue(limit.Name() if limit else '')
        self._nameCtrl.Enabled(bool(limit))

    def _UpdatePropertiesControls(self, limit):
        self._checkValueTypeCtrl.SetData(limit.TransformFunction() if limit else FLimitSettings.DefaultTransformFunction())
        self._checkValueTypeCtrl.Enabled(bool(limit))
        self._warningTypeCtrl.SetData('Percent'
                if limit and limit.PercentageWarning() else 'Absolute')
        self._warningTypeCtrl.Enabled(limit and FLimitUtils.IsWarningEnabled(limit))

    def _UpdateWarningControls(self, limit):
        warningEnabled = FLimitUtils.IsWarningEnabled(limit)
        self._warningCtrl.Enabled(warningEnabled)
        if not warningEnabled:
            self._warningCtrl.SetValue(0 if limit.PercentageWarning() else limit.Threshold())

    def _OnCheckValueTypeChanged(self, _params, _cd):
        limit = self._parent.EditLimit()
        if limit:
            limit.TransformFunction(self._checkValueTypeCtrl.GetData())

    def _OnWarningTypeChanged(self, _params, _cd):
        limit = self._parent.EditLimit()
        if limit:
            percentageWarning = bool(self._warningTypeCtrl.GetData() == 'Percent')
            if percentageWarning != limit.PercentageWarning():
                value = FLimitUtils.WarningPercentage(limit) if percentageWarning \
                        else FLimitUtils.WarningValue(limit)
                limit.PercentageWarning(percentageWarning)
                self._warningCtrl.SetValue(value)

    @staticmethod
    def _QueryClass(rowObject):
        if rowObject.IsKindOf(acm.FASQLQueryFolder):
            return rowObject.AsqlQuery().AsqlQueryClass() if rowObject.AsqlQuery() else None
        elif rowObject.IsKindOf(acm.FStoredASQLQuery):
            return rowObject.QueryClass()
        else:
            return None

    @staticmethod
    def _GetSubLevelsForCell(cell):
        subLevels = ['This cell value']
        rowObject = FLimitUtils.CellRowObject(cell)
        treeSpec = LimitTreeSpecification(cell).TreeSpecification()
        grouper = treeSpec.Grouper()
        isTopNode = (bool(cell.Tree().Depth() == 1) or
                rowObject.Class() in (acm.FPortfolioInstrumentAndTrades, acm.FASQLQueryFolder))
        # Do not allow parent limits on limits
        if (rowObject.IsKindOf(acm.FLimitMultiItem) or
            rowObject.IsKindOf(acm.FLimit) or
            (LimitPane._QueryClass(rowObject) == acm.FLimit)):
            return subLevels

        if grouper and FLimitUtils.IsMultiRow(rowObject):
            if grouper.IsKindOf(acm.FChainedGrouper):
                grprs = grouper.Groupers()
                if treeSpec.Constraints():
                    grprs = grprs[len(treeSpec.Constraints().FlatValues()):]
                for group in grprs:
                    subLevels.append('All child "%s" values' % group.DisplayName())
            elif isTopNode:
                # Single grouper means only the top level has grouper children
                if (not grouper.IsKindOf(acm.FDefaultGrouper) or
                        grouper.IsKindOf(acm.FSubportfolioGrouper)):
                    subLevels.append('All child "%s" values' % grouper.DisplayName())
            subLevels.append('All leaf values')
        return subLevels


class LimitTemplatePane(FUxCore.LayoutPanel):

    KEY = 'limitTemplate'

    def __init__(self, parent, originObject):
        self._parent = parent
        self._template = None
        self._templateCtrl = None
        self._templateDescCtrl = None
        self._bindings = None
        self._originObject = originObject

    def LimitTemplate(self):
        return self._template

    def SheetType(self):
        # pylint: disable-msg=W0212
        if not self._parent:
            return None
        # If the object has been opened from a sheet, the type is stored
        if self._parent._externalSheetType:
            return self._parent._externalSheetType
        target = self._parent.LimitTarget()
        if target:
            return target.SheetType()
        obj = self._parent.OriginObject()
        if not obj:
            return None
        if obj.IsKindOf(acm.FPortfolio):
            return 'FPortfolioSheet'
        elif obj.IsKindOf(acm.FLimit):
            return 'FLimitSheet'
        elif obj.IsKindOf(acm.FSettlement):
            return 'FSettlementSheet'
        else:
            return None

    def HandleCreate(self):
        self._template = None
        self._InitDataBindingControls()
        layout = self.SetLayout(self.CreateLayout()) # pylint: disable-msg=E1101
        self._templateCtrl.InitLayout(layout)
        self._templateDescCtrl = layout.GetControl('templateDesc')
        self._templateDescCtrl.Editable(False)
        self.UpdateControls()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('EtchedIn', 'Apply template')
        self._templateCtrl.BuildLayoutPart(b, 'Name')
        b.    AddInput('templateDesc', 'Description', 60)
        b.  EndBox()
        b.EndBox()
        return b

    def ServerUpdate(self, _sender, symbol, binder):
        if str(symbol) != 'ControlValueChanged':
            return
        if binder == self._templateCtrl:
            if not binder.GetValue() or self._ConfirmApplyTemplate():
                self._template = binder.GetValue()
                self.UpdateControls()

    def UpdateControls(self):
        t = self.LimitTemplate()
        self._templateDescCtrl.SetData(t.Description() if t else '')
        templatesEnabled = bool(self._parent.OriginObject())
        self._templateCtrl.Enabled(templatesEnabled)
        if templatesEnabled:
            self._UpdateLimitTargetControl()

    def OnNewOriginObject(self):
        if self._templateCtrl:
            self._templateCtrl.SetValue(None)

    def _InitDataBindingControls(self):
        self._bindings = acm.FUxDataBindings()
        self._templateCtrl = self._bindings.AddBinder('template', 'FObject',
                None, FLimitTemplate.GetLimitTemplates(self.SheetType()))
        self._bindings.AddDependent(self)

    def _UpdateLimitTargetControl(self):
        template = self.LimitTemplate()
        if not template:
            return
        try:
            self._SetLimitSpecification()
            limitTarget = template.SetupLimitTarget(self._originObject)
            self._SetLimitTarget(limitTarget)
        except Exception as e:
            self._DisplayErrorMessage('Could not apply selected template:\n\n' + str(e))

    def _SetLimitSpecification(self):
        template = self.LimitTemplate()
        if template:
            limitSpec = acm.FLimitSpecification[template.LimitSpecificationName()]
            if limitSpec and self._parent.LimitSpecification() != limitSpec:
                self._parent.LimitSpecification(limitSpec)

    def _SetLimitTarget(self, limitTarget):
        limit = self._parent.EditLimit()
        template = self.LimitTemplate()
        if limit and template:
            limit.ComparisonOperator(template.ComparisonOperator())
            limit.WarningValue(template.WarningValue())
            limit.Threshold(template.Threshold())
        self._parent.LimitTarget(limitTarget)

    def _ConfirmApplyTemplate(self):
        if self._parent.OriginalLimit() or self._parent.TargetCell():
            self._parent.HandleObject(self._parent.OriginObject())
            return bool(not self._parent.OriginalLimit() and not self._parent.TargetCell())
        return True

    def _DisplayErrorMessage(self, msg):
        acm.UX().Dialogs().MessageBox(self._parent.Shell(), 'Error', msg, 'OK',
            None, None, 'Button1', 'Button1')

class ViewLimitTemplatesMenuItem(FUxCore.MenuItem):

    def __init__(self, extObj):
        self._extObj = extObj

    def Checked(self):
        return self._extObj.IsDockWindowVisible(LimitTemplatePane.KEY)

    def Invoke(self, _eii):
        self._extObj.ShowDockWindow(LimitTemplatePane.KEY, not self.Checked())