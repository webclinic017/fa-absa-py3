""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../reconciliation/etc/FReconciliationSettings.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationSettings

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

# pylint:disable-msg=W1401,W0102,W0221,


import sys
import collections
import re

import acm
import FUxCore
import FExternalDataImportEngine
import FBusinessDataStateChartUpgrader
import FReconciliationColumnCreator
import FReconciliationSpecification
import FReconciliationReaderFactory
import FBusinessDataImportHook
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()


GROUP_MAP = {
             'Position': ('portfoliosheet', 'FTrade', 'FPortfolioSheet'),
             'Trade': ('tradesheet', 'FTrade', 'FTradeSheet'),
             'Settlement': ('settlementsheet', 'FSettlement', 'FSettlementSheet'),
             'Instrument': ('dealsheet', 'FInstrument', 'FDealSheet'),
             'Journal': ('journalsheet', 'FJournal', 'FJournalSheet'),
             'Order': ('tradesheet', 'FTrade', 'FTradeSheet')
            }

class Control(object):

    _SYMBOL = 'FSymbol'
    _STRING = 'FString'
    _NAMESPACE = None
    _LABEL = None
    _PARAM_NAME = None
    _DEFAULT_OBJECT_TYPE = 'Trade'
    _CMP_TYPES = ('Absolute', 'Relative', 'Both', 'None')

    # Map from object type to a tuple of available file readers
    # The first item in the tuple is used as default
    _READER_TYPE_MAP = {
        'Position': ('CSV', 'Custom'),
        'Trade': ('CSV', 'Custom'),
        'Settlement': ('CSV', 'Custom'),
        'Instrument': ('CSV', 'Custom'),
        'Journal':('CSV', 'Custom'),
        'Order':('CSV', 'Custom')
    }

    def __init__(self):
        self.keys = None
        self.values = None
        self.pairs = None
        self.keysCtrl = None
        self.valuesCtrl = None
        self.pairsCtrl = None
        self.mainDlg = None
        self.ctrls = None
        self.btnAdd = None
        self.btnRemove = None
        self.btnRemoveAll = None
        self.edited = False
        self.applicationState = None # Used in sub classes

    @staticmethod
    def Context():
        return acm.GetDefaultContext()

    def GetModule(self, moduleName):
        for module in self.Context().Modules():
            if module.Name() == moduleName:
                return module

    def Edited(self, edited=None):
        if edited is None:
            return self.edited
        self.edited = edited

    def PreHandleCancel(self):
        if self.Edited():
            raise AssertionError()

    @staticmethod
    def ThrowException(dlg, errorStr):
        acm.UX().Dialogs().MessageBox(
                dlg.Shell(),
                'Error',
                errorStr,
                'OK',
                None,
                None,
                'Button1',
                'None')

    @staticmethod
    def OutputMsgBoxInformation(dlg, outputStr):
        acm.UX().Dialogs().MessageBoxInformation(dlg.Shell(), outputStr)

    def SaveSucceeded(self, name, moduleName):
        self.OutputMsgBoxInformation(self.mainDlg, '%s successfully saved in module %s.' % (name, moduleName))

    def SaveFailed(self, name, err):
        self.ThrowException(self.mainDlg, 'Could not save %s.\nReason: %s.' % (name, str(err)))

    def DeleteSucceeded(self, name):
        self.OutputMsgBoxInformation(self.mainDlg, '%s successfully deleted.' % name)

    def DeleteFailed(self, name, err):
        self.ThrowException(self.mainDlg, 'Could not delete %s.\nReason: %s' % (name, str(err)))

    def ConfirmDelete(self, name):
        TEXT = ('Are you sure you want to permanently delete %s?' % name)
        res = acm.UX().Dialogs().MessageBoxOKCancel(
                self.mainDlg.Shell(),
                'Question',
                TEXT)
        if res not in ('Button1', ):
            return False
        return True

    def AdjustPairsControl(self):
        self.pairsCtrl.AdjustColumnWidthToFitItems(0)
        self.pairsCtrl.AdjustColumnWidthToFitItems(1)

    def AdjustKeysControl(self):
        self.keysCtrl.AdjustColumnWidthToFitItems(0)

    def OnFileChanged(self, name, _cd):
        self.Edited(True)

    def AddEditCallback(self, name):
        # pylint: disable-msg=E1136
        ctrl = self.ctrls[name]
        if ctrl.IsKindOf(acm.FUxCheckBox):
            ctrl.AddCallback('Activate', self.OnFileChanged, None)
        elif str(name).startswith('dictPairs'):
            ctrl.AddCallback('Changed', self.OnFileChanged, None)
        elif name.startswith('threshold') or name in ('significant_decimals', ):
            ctrl.AddCallback('Changing', self.OnFileChanged, name)
        elif ctrl.IsKindOf(acm.FUxTreeControl):
            return
        elif ctrl.IsKindOf(acm.FUxListControl):
            return
        else:
            ctrl.AddCallback('Changed', self.OnFileChanged, name)

    def InitEditCallbacks(self):
        # pylint: disable-msg=E1133
        for name in self.ctrls:
            self.AddEditCallback(name)

    def Keys(self, keys=None):
        if keys is None:
            return self.keys
        self.keys = set(keys)

    def Values(self, values=None):
        if values is None:
            return self.values
        self.values = values

    def Pairs(self):
        return self.pairs

    def SelectNewItem(self, items, index, itemsList, listCtrl):
        if items:
            if len(items) <= index:
                index -= 1
            newItem = itemsList[index]
            if newItem:
                listCtrl.SetData(newItem)

    def OnPairsDefaultAction(self, _args, _cd):
        self.OnRemoveClicked()

    def OnKeyValuesDefaultAction(self, _args, _cd):
        self.OnAddClicked()

    def OnRemoveAllClicked(self, _args=None, _cd=None):
        for pair in self.pairs:
            item = str(pair.First())
            self.keys.add(item)
        self.pairs = set()
        self.pairsCtrl.Clear()
        self.AddKeyItems(self.keys)

    def OnRemoveClicked(self, _args=None, _cd=None):
        pairSelected = self.pairsCtrl.GetSelectedItem()
        if pairSelected:
            pair = pairSelected.GetData()
            self.AddKeyItems([str(pair.First())])
            self.RemoveItem(self.pairs, self.pairsCtrl, pair)

    def OnAddKeyValue(self, key, value, selection=False):
        pair = acm.FPair()
        pair.First(key)
        try:
            pair.Second(value.Name())
        except AttributeError:
            pair.Second(value)
        self.AddPairItem(pair)
        self.RemoveItem(self.keys, self.keysCtrl, key, selection)
        self.SelectFirstItem(self.pairs, self.pairsCtrl)

    def OnAddClicked(self, _args=None, _cd=None):
        selectedKey = self.keysCtrl.GetSelectedItem()
        if selectedKey:
            key = selectedKey.GetData()
            selectedValue = self.valuesCtrl.GetSelectedItem()
            value = selectedValue.GetData()
            if value:
                self.OnAddKeyValue(key, value)

    def AddPairItem(self, item):
        self.pairsCtrl.Clear()
        self.pairs.add(item)
        root = self.pairsCtrl.GetRootItem()
        pairItems = sorted(self.pairs, key=lambda p: p.First())
        for item in pairItems:
            child = root.AddChild()
            self.Label(child, item.First(), 0)
            self.Label(child, item.Second(), 1)
            child.SetData(item)
            child.Icon('BlueBall', 'BlueBall')
        self.AdjustPairsControl()

    def AddKeyItems(self, items=set()):
        self.keysCtrl.Clear()
        self.keys.update(items)
        root = self.keysCtrl.GetRootItem()
        for item in sorted(self.keys):
            child = root.AddChild()
            self.Label(child, item)
            child.SetData(item)
            self.Icon(child, item)
        self.SelectFirstItem(self.keys, self.keysCtrl)
        self.AdjustKeysControl()

    def RemoveItem(self, items, listCtrl, item, selection=False):
        itemsList = list(items)
        index = None
        try:
            index = itemsList.index(item)
            items.remove(item)
        except ValueError:
            pass
        finally:
            if selection:
                self.AddKeyItems(items)
            else:
                listCtrl.RemoveAllSelectedItems(True)
        if index is not None and len(items):
            self.SelectNewItem(items, index, itemsList, listCtrl)

    def SelectFirstItem(self, itemsList, listCtrl):
        if itemsList:
            firstItem = list(itemsList)[0]
            listCtrl.SetData(firstItem)

    def InitButtonCallbacks(self):
        self.btnAdd.AddCallback('Activate', self.OnAddClicked, None)
        self.btnRemove.AddCallback('Activate', self.OnRemoveClicked, None)
        self.btnRemoveAll.AddCallback('Activate', self.OnRemoveAllClicked, None)

    def InitPairsDefaultActionCallback(self):
        self.pairsCtrl.AddCallback('DefaultAction', self.OnPairsDefaultAction, None)

    def InitKeyValuesDefaultActionCallBack(self):
        self.valuesCtrl.AddCallback('DefaultAction', self.OnKeyValuesDefaultAction, None)
        self.keysCtrl.AddCallback('DefaultAction', self.OnKeyValuesDefaultAction, None)

    def Label(self, item, data, index=0):
        if type(data) is str:
            item.Label(data, index)
        elif data.IsKindOf(acm.FColumnDefinition):
            item.Label(data.At('Name') or data.StringKey())
        else:
            item.Label(data.StringKey(), index)

    def Icon(self, item, data):
        try:
            icon = data.Icon()
            if str(icon) in (self._SYMBOL, self._STRING):
                item.Icon('BlueBall', 'BlueBall')
            else:
                item.Icon(icon, icon)
        except AttributeError:
            item.Icon('BlueBall', 'BlueBall')

    def PopulateKeysCtrl(self, sortKey=None, customCmp=None):
        self.keysCtrl.Clear()
        root = self.keysCtrl.GetRootItem()
        for key in sorted(self.keys, key=sortKey, cmp=customCmp):
            child = root.AddChild()
            self.Label(child, key)
            child.SetData(key)
            self.Icon(child, key)
        self.AdjustKeysControl()

    def PopulateTreeValuesCtrl(self, includes=None, icon=None, setData=None, sortKey=None):
        self.valuesCtrl.Clear()
        root = self.valuesCtrl.GetRootItem()
        for key in sorted(self.values.keys()):
            child = root.AddChild()
            self.Label(child, key)
            if setData: child.SetData(key)
            if icon: child.Icon(icon, icon)
            for value in sorted(list(self.values[key]), key=sortKey):
                if (not includes or
                    includes.lower() in str(value.At('Name')).lower() or
                    includes.lower() in value.StringKey().lower()):
                    grandChild = child.AddChild()
                    self.Label(grandChild, value)
                    grandChild.SetData(value)
                    grandChild.Icon('BlueBall', 'BlueBall')
                    if includes: grandChild.EnsureVisible()

    def PopulateListValuesCtrl(self, customCmp=None):
        self.valuesCtrl.Clear()
        root = self.valuesCtrl.GetRootItem()
        for value in sorted(self.values, cmp=customCmp):
            child = root.AddChild()
            child.Label(value.Name())
            child.SetData(value)
            child.Icon(value.Icon(), value.Icon())

    def Controls(self):
        return self.ctrls

    @staticmethod
    def AsString(data):
        try:
            return data.StringKey()
        except AttributeError:
            return data

    def GetData(self, item):
        pair = item.GetData()
        first, second = pair.First(), pair.Second()
        return '='.join((self.AsString(first), self.AsString(second)))

    def SetData(self, ctrl, data):
        if ctrl.IsKindOf(acm.FUxCheckBox):
            data = True if str(data).lower() in ('true', ) else False
            ctrl.Checked(data)
        else:
            ctrl.Checked(data)

    def Parameters(self):
        root = self.pairsCtrl.GetRootItem()
        return '\n'.join(self.GetData(child) for child in root.Children())

    def HandleApply(self, name, module):
        paramStr = self.Parameters()
        if hasattr(self, 'applicationState') and not self.applicationState.IsUpload():
            if len(paramStr) == 0:
                raise ValueError(''.join([self.TabLabel(), ' does not contain any items to commit']))
        params = [
                    'FObject:%s =\n' % name,
                    paramStr
                 ]
        acm.GetDefaultContext().EditImport('FParameters', ''.join(params), True, module)

    @staticmethod
    def ColumnSort(column):
        try:
            return column.At('Name').AsString()
        except AttributeError:
            return column.StringKey()

    @classmethod
    def TabLabel(cls):
        return cls._LABEL

    @classmethod
    def NameSpace(cls):
        return cls._NAMESPACE

    @classmethod
    def ParamName(cls):
        return cls._PARAM_NAME

    def InitControl(self, layout, name, label=None):
        # pylint: disable-msg=E1135,E1136,
        _name = label or name
        if _name not in self.ctrls:
            ctrl = layout.GetControl(name)
            self.ctrls[_name] = ctrl
        return self.ctrls[_name]

    @classmethod
    def FormatControlNames(cls):
        for attrName in dir(cls):
            attr = getattr(cls, attrName)
            if (not attrName.startswith('_') and
                not hasattr(attr, '__call__')):
                setattr(cls, attrName, attr % cls.NameSpace())

    @staticmethod
    def CompareRuleIds(left, right):
        left, right = str(left.First()), str(right.First())
        leftValue, rightValue = left.split('Rule'), right.split('Rule')
        return int(leftValue[1]) - int(rightValue[1])


class SelectionPane(Control):
    KEYS = 'dictKeys%s'
    PAIRS = 'dictPairs%s'
    BTN_ADD = 'btnAdd%s'
    BTN_REMOVE = 'btnRemove%s'
    BTN_REMOVE_ALL = 'btnRemoveAll%s'
    BTN_UP = 'btnUp%s'
    BTN_DOWN = 'btnDown%s'

    def __init__(self, keys=set(), keysLabel=str(), pairsLabel=str()):
        super(SelectionPane, self).__init__()
        self.keys = keys
        self.pairs = list()
        self.btnAdd = None
        self.btnRemove = None
        self.btnRemoveAll = None
        self.btnUp = None
        self.btnDown = None
        self.keysLabel = keysLabel
        self.pairsLabel = pairsLabel
        self.FormatControlNames()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b.   AddList(self.KEYS, 15, 20, 40, 20)
        if self.NameSpace() in ('IdRules', 'UniverseQueries'):
            b.   BeginHorzBox()
            b.    AddButton('btnNew', 'New...')
            b.    AddButton('btnView', 'View...')
            b.   EndBox()
        b.  EndBox()
        b.   AddSpace(3)
        b.  BeginVertBox()
        b.   AddFill()
        b.   AddButton(self.BTN_ADD, "Add")
        b.   AddButton(self.BTN_REMOVE, "Remove")
        b.   AddSpace(3)
        b.   AddButton(self.BTN_REMOVE_ALL, "Remove All")
        b.   AddFill()
        b.  EndBox()
        b.  AddSpace(2)
        b.  BeginVertBox()
        b.   AddList(self.PAIRS, 15, 20, 40, 20)
        if self.NameSpace() in ('IdRules', 'UniverseQueries'):
            b.   BeginHorzBox()
            b.    AddButton('btnViewSelected', 'View...')
            b.   EndBox()
        b.  EndBox()
        b. AddSpace(3)
        if self.NameSpace() in ('IdRules', 'UniverseQueries'):
            b.  BeginVertBox()
            b.   AddFill()
            b.   AddButton(self.BTN_UP, 'Up')
            b.   AddButton(self.BTN_DOWN, 'Down')
            b.   AddFill()
            b.  EndBox()
        b. EndBox()
        b. AddSpace(5)
        b.EndBox()
        return b

    def SwapItems(self, up=True):
        try:
            item = self.pairsCtrl.GetSelectedItem()
            data = item.GetData()
            index = self.pairs.index(data)
            try:
                if up and (index-1) >= 0:
                    self.pairs[index-1], self.pairs[index] = self.pairs[index], self.pairs[index-1]
                elif not up:
                    self.pairs[index], self.pairs[index+1] = self.pairs[index+1], self.pairs[index]
            except IndexError:
                pass
            self.PopulatePairsControl(selected=data)
        except AttributeError:
            pass

    def OnUpClicked(self, _args, _cd):
        self.SwapItems()

    def OnDownClicked(self, _args, _cd):
        self.SwapItems(up=False)

    def PopulatePairsControl(self, selected=None):
        self.pairsCtrl.Clear()
        root = self.pairsCtrl.GetRootItem()
        for item in self.pairs:
            item.First('Rule%i' % (root.ChildrenCount() + 1))
            child = root.AddChild()
            second = item.Second()
            self.Label(child, second, 0)
            child.SetData(item)
            self.Icon(child, second)
            if item is selected:
                child.Select(True)

    def InitControls(self, layout):
        self.keysCtrl = self.InitControl(layout, self.KEYS)
        self.pairsCtrl = self.InitControl(layout, self.PAIRS)
        self.btnAdd = self.InitControl(layout, self.BTN_ADD)
        self.btnRemove = self.InitControl(layout, self.BTN_REMOVE)
        self.btnRemoveAll = self.InitControl(layout, self.BTN_REMOVE_ALL)
        if self.NameSpace() in ('IdRules', 'UniverseQueries'):
            self.btnUp = self.InitControl(layout, self.BTN_UP)
            self.btnDown = self.InitControl(layout, self.BTN_DOWN)

    def SetupControls(self):
        self.keysCtrl.AddColumn(self.keysLabel)
        self.keysCtrl.ShowColumnHeaders(True)
        self.pairsCtrl.AddColumn(self.pairsLabel)
        self.pairsCtrl.ShowColumnHeaders(True)
        self.pairsCtrl.ShowGridLines(True)

    def SetToolTips(self):
        if self.NameSpace() in ('IdRules'):
            self.keysCtrl.ToolTip('Selected queries will be filled with information from the imported file to find ' +
                'a matching item in the PRIME database. Only shared queries are available to be selected.')
            self.pairsCtrl.ToolTip('Selected rule queries ordered by descending priority')
        elif self.NameSpace() in ('UniverseQueries'):
            self.keysCtrl.ToolTip('Selected queries will be used to retrieve objects from the PRIME database for ' +
                'comparison with the imported file (optional). Only shared queries are available to be selected.')
            self.pairsCtrl.ToolTip('Selected universe queries ordered by descending priority')

    def HandleCreate(self, layout):
        self.InitControls(layout)
        self.SetupControls()
        self.InitButtonCallbacks()
        self.SetToolTips()

    def InitButtonCallbacks(self):
        self.btnAdd.AddCallback('Activate', self.OnAddClicked, None)
        self.btnRemove.AddCallback('Activate', self.OnRemoveClicked, None)
        self.btnRemoveAll.AddCallback('Activate', self.OnRemoveAllClicked, None)
        if self.NameSpace() in ('IdRules', 'UniverseQueries'):
            self.btnUp.AddCallback('Activate', self.OnUpClicked, None)
            self.btnDown.AddCallback('Activate', self.OnDownClicked, None)

    def PopulateControls(self):
        raise NotImplementedError


class MappingPane(Control):

    KEYS = 'dictKeys%s'
    VALUES = 'dictValues%s'
    PAIRS = 'dictPairs%s'
    INPUT = 'input%s'
    BTN_ADD = 'btnAdd%s'
    BTN_REMOVE = 'btnRemove%s'
    BTN_REMOVE_ALL = 'btnRemoveAll%s'
    BTN_NEW = 'btnNew%s'
    BTN_EDIT = 'btnEdit%s'
    BTN_DEL = 'btnDelete%s'
    _DECIMALS = 'significant_decimals'
    _THRESHOLD_PCT = 'threshold_percentage'
    _THRESHOLD_ABS = 'threshold_absolute'

    def __init__(self, keys=set(), values=None,
                 keysLabel='Theirs', valuesLabel='Ours'):
        super(MappingPane, self).__init__()
        self.keys = keys
        self.values = values
        self.pairs = set()
        self.keysLabel = keysLabel
        self.valuesLabel = valuesLabel
        self.btnAdd = None
        self.btnRemove = None
        self.btnRemoveAll = None
        self.btnNewCtrl = None
        self.btnEditCtrl = None
        self.btnDelCtrl = None
        self.inputCtrl = None
        self.decimalsCtrl = None
        self.thresholdAbsoluteCtrl = None
        self.thresholPercentageCtrl = None
        self.thresholds = None
        self.FormatControlNames()

    def SetupControls(self):
        self.keysCtrl.AddColumn(self.keysLabel)
        self.keysCtrl.ShowColumnHeaders(True)
        self.valuesCtrl.ColumnLabel(0, self.valuesLabel)
        self.valuesCtrl.ShowColumnHeaders(True)
        self.pairsCtrl.AddColumn(self.keysLabel)
        self.pairsCtrl.AddColumn(self.valuesLabel)
        self.pairsCtrl.ShowColumnHeaders(True)
        self.pairsCtrl.ShowGridLines(True)

    def InitControls(self, layout):
        self.keysCtrl = self.InitControl(layout, self.KEYS)
        self.valuesCtrl = self.InitControl(layout, self.VALUES)
        self.pairsCtrl = self.InitControl(layout, self.PAIRS)
        self.btnAdd = self.InitControl(layout, self.BTN_ADD)
        self.btnRemove = self.InitControl(layout, self.BTN_REMOVE)
        self.btnRemoveAll = self.InitControl(layout, self.BTN_REMOVE_ALL)
        if self.NameSpace() in ('Comparison', ):
            self.inputCtrl = self.InitControl(layout, self.INPUT)
            self.decimalsCtrl = self.InitControl(layout, self._DECIMALS)
            self.thresholdAbsoluteCtrl = self.InitControl(layout, self._THRESHOLD_ABS)
            self.thresholPercentageCtrl = self.InitControl(layout, self._THRESHOLD_PCT)
        elif self.NameSpace() in ('Attributes', ):
            self.inputCtrl = self.InitControl(layout, self.INPUT)
        else:
            self.btnNewCtrl = self.InitControl(layout, self.BTN_NEW)
            self.btnEditCtrl = self.InitControl(layout, self.BTN_EDIT)
            self.btnDelCtrl = self.InitControl(layout, self.BTN_DEL)

    def SetToolTips(self):
        if self.NameSpace() in ('DataTypes'):
            self.keysCtrl.ToolTip('Columns from imported file')
            self.valuesCtrl.ToolTip('Data types to be mapped to the imported columns')
            self.pairsCtrl.ToolTip('Mapped types')
        elif self.NameSpace() in ('Attributes'):
            self.keysCtrl.ToolTip('Attributes (columns) from the imported file used to identify the rows as items in the PRIME database')
            self.valuesCtrl.ToolTip('Attributes (columns) in the PRIME database which can be mapped to attributes from the imported file')
            self.pairsCtrl.ToolTip('Mapped attributes')
        elif self.NameSpace() in ('Comparison'):
            self.keysCtrl.ToolTip('Values from the imported file to be compared with values in the PRIME database after successful identification')
            self.valuesCtrl.ToolTip('Values (columns) in the PRIME database which can be mapped to the values from the imported file')
            self.pairsCtrl.ToolTip('Mapped values')

    def HandleCreate(self, layout):
        self.InitControls(layout)
        self.SetupControls()
        self.InitButtonCallbacks()
        self.SetToolTips()

    def AddThresholdPane(self, b):
        b.BeginVertBox('EtchedIn', '')
        b.  BeginHorzBox()
        b.    AddInput(self._THRESHOLD_PCT, 'Threshold %')
        b.    AddInput(self._THRESHOLD_ABS, 'Threshold Abs')
        b.  EndBox()
        b.  BeginHorzBox()
        b.    AddInput(self._DECIMALS, 'Decimals')
        b.    AddFill()
        b.  EndBox()
        b.EndBox()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b.   AddList(self.KEYS, 15, -1, 30, -1)
        b.  EndBox()
        b.  AddSpace(1)
        b.  BeginVertBox()
        b.    AddTree(self.VALUES, 250, -1)
        if self.NameSpace() in ('Comparison', 'Attributes'):
            label = 'Filter' if self.NameSpace() in ('Comparison', ) else 'Description'
            b.AddInput(self.INPUT, label)
        else:
            b.BeginHorzBox()
            b.  AddButton(self.BTN_NEW, 'New...')
            b.  AddButton(self.BTN_EDIT, 'Edit...')
            b.  AddButton(self.BTN_DEL, 'Delete')
            b.EndBox()
        b.  EndBox()
        b.  BeginVertBox()
        b.   AddFill()
        b.   AddButton(self.BTN_ADD, "Add")
        b.   AddButton(self.BTN_REMOVE, "Remove")
        b.   AddSpace(3)
        b.   AddButton(self.BTN_REMOVE_ALL, "Remove All")
        b.   AddFill()
        b.  EndBox()
        b.  AddSpace(2)
        b.  BeginVertBox()
        b.  AddList(self.PAIRS, 15, -1, 50)
        if self.NameSpace() in ('Comparison', ):
            self.AddThresholdPane(b)
        b.  EndBox()
        b. AddSpace(3)
        b. EndBox()
        b. AddSpace(5)
        b.EndBox()
        return b

    def PopulateControls(self):
        raise NotImplementedError


class ComparisonSettings(MappingPane):

    _PARAM_NAME = 'Compared Values Map'
    _NAMESPACE = 'Comparison'
    _LABEL = 'Comparison Values'
    _DATA_TYPE_TOKEN = 'DataType'

    def __init__(self, dlg, applicationState, thresholdParams):
        super(ComparisonSettings, self).__init__()
        self.pairsCtrl = None
        self.decimalsCtrl = None
        self.thresholdAbsoluteCtrl = None
        self.thresholPercentageCtrl = None
        self.dataTypeSettings = thresholdParams.dataTypeSettings
        self.moduleCtrl = thresholdParams.moduleCtrl
        self.reconNameCtrl = thresholdParams.reconNameCtrl
        self.mainDlg = dlg
        self.clearing = False
        self.thresholds = collections.defaultdict(dict)
        self.ctrls = dict()
        self.applicationState = applicationState

    def HandleCreate(self):
        builder = self.CreateLayout()
        comparisonLayout = self.mainDlg.AddPane(self.TabLabel(), builder)
        super(ComparisonSettings, self).HandleCreate(comparisonLayout)
        self.InitPairsDefaultActionCallback()
        self.InitKeyValuesDefaultActionCallBack()
        self.PopulateControls()
        self.InitEditCallbacks()
        self.InitCallbacks()
        self.EnableControls(False)

    def Module(self):
        data = self.moduleCtrl.GetData()
        return [
            m for m in acm.GetDefaultContext().Modules()
            if m.Name() in (data, )
            ][0]

    def EnableControls(self, enable=True, datatype=None):
        self.decimalsCtrl.Enabled(enable if datatype != 'integer' else False)
        self.thresholdAbsoluteCtrl.Enabled(enable)
        self.thresholPercentageCtrl.Enabled(enable)

    def PopulateThresholdControls(self, datatype):
        self.decimalsCtrl.SetData(datatype.GetString(self._DECIMALS))
        self.thresholdAbsoluteCtrl.SetData(datatype.GetString(self._THRESHOLD_ABS))
        self.thresholPercentageCtrl.SetData(datatype.GetString(self._THRESHOLD_PCT))
        self.Edited(False)

    @classmethod
    def Token(cls):
        return cls._DATA_TYPE_TOKEN

    @staticmethod
    def IsNumeric(dataType):
        return dataType in ('float', 'integer')

    def CollectThresholdsInMemory(self):
        thresholdName = self.ThresholdName()
        if self.thresholds.get(thresholdName):
            del self.thresholds[thresholdName]

    def DeleteDataType(self, name=None):
        try:
            if name is None:
                name = self.DataTypeParameterName()
            module = self.Module()
            module.RemoveExtension('FParameters', 'FObject', name)
            module.Commit()
        except ValueError as e:
            logger.error(e)
        except StandardError as e:
            logger.error(e)
            module.Undo()
        finally:
            self.CollectThresholdsInMemory()

    def OnRemoveClicked(self, _args=None, _cd=None):
        pairSelected = self.pairsCtrl.GetSelectedItem()
        if pairSelected:
            pair = pairSelected.GetData()
            self.AddKeyItems([pair.First()])
            self.DeleteDataType()
            self.RemoveItem(self.pairs, self.pairsCtrl, pair)

    def DataTypeName(self, columnName):
        root = self.dataTypeSettings.pairsCtrl.GetRootItem()
        for item in root.Children():
            pair = item.GetData()
            name = str(pair.First())
            if name in (columnName, ):
                return str(pair.Second())
        return None

    @staticmethod
    def DataTypeParam(name):
        dataTypeExtensions = acm.GetDefaultContext().GetAllExtensions(
                'FParameters',
                name)
        if dataTypeExtensions:
            return dataTypeExtensions[0].Value()
        raise ValueError('FParameter %s not found.' % name)

    def HandleThresholdsInMemory(self, params, datatype):
        self.EnableControls(datatype=datatype)
        self.decimalsCtrl.SetData(params.get(self._DECIMALS) or str())
        self.thresholdAbsoluteCtrl.SetData(params.get(self._THRESHOLD_ABS) or str())
        self.thresholPercentageCtrl.SetData(params.get(self._THRESHOLD_PCT) or str())
        self.Edited(False)

    def HandleCustomDataTypes(self, name):
        try:
            paramName = self.DataTypeParameterName(source='OnPairsChanged')
            dataTypeParam = self.DataTypeParam(paramName)
        except ValueError:
            dataTypeParam = self.DataTypeParam(name)
        dataType = (
            dataTypeParam.GetString('data_type')
            if dataTypeParam
            else None
            )
        thresholdName = self.ThresholdName()
        params = self.thresholds.get(thresholdName)
        if params:
            self.HandleThresholdsInMemory(params, dataType)
            return
        if dataType:
            if self.IsNumeric(dataType):
                self.EnableControls(datatype=dataType)
                baseDataType = dataTypeParam.GetString('base')
                if self.DataTypeName(self.SelectedColumnName()) == baseDataType:
                    self.PopulateThresholdControls(dataTypeParam)
            else:
                self.EnableControls(False)

    def ClearThresholdControls(self):
        self.decimalsCtrl.Clear()
        self.thresholdAbsoluteCtrl.Clear()
        self.thresholPercentageCtrl.Clear()

    def HandleDataTypes(self, name):
        self.clearing = True
        self.ClearThresholdControls()
        self.clearing = False
        self.EnableControls(self.IsNumeric(name), name)
        self.HandleCustomDataTypes(name)

    def SelectedColumnName(self):
        selectedItem = self.pairsCtrl.GetSelectedItem()
        if selectedItem:
            pair = selectedItem.GetData()
            return str(pair.First())
        return None

    def OnPairsChanged(self, _agrs, _cd):
        columnName = self.SelectedColumnName()
        if columnName:
            try:
                dataTypeName = self.DataTypeName(columnName)
                if dataTypeName:
                    self.HandleDataTypes(dataTypeName)
                else:
                    self.ClearThresholdControls()
                    self.EnableControls(False)
            except ValueError:
                pass
        else:
            self.ClearThresholdControls()
            self.EnableControls(False)

    def OnFileChanged(self, name, _cd):
        self.Edited(True)
        self.SaveThreshold(name)

    def ThresholdName(self):
        selectedColumnName = self.SelectedColumnName()
        if selectedColumnName:
            return ''.join((selectedColumnName, 'DataType'))

    def DataTypeParameterName(self, columnName=None, source=None):
        reconName = str(self.reconNameCtrl.GetData())
        selectedColumnName = self.SelectedColumnName()
        if not (reconName or source or selectedColumnName):
            raise ValueError('Name')
        elif not (self.Module() or source):
            raise ValueError('Module')
        return ''.join((
            reconName,
            columnName or selectedColumnName,
            'DataType'
            ))

    def SaveThresholdSucceeded(self, name, moduleName):
        self.OutputMsgBoxInformation(self.mainDlg, 'Thresholds successfully saved in module %s.' % moduleName)

    def SaveThresholdFailed(self, err):
        self.ThrowException(self.mainDlg, 'Could not save threshold. \nReason: %s' % str(err))

    def ParamMissingError(self, err):
        self.ThrowException(self.mainDlg, 'Could not save threshold - parameter value is not accepted. \nReason: %s' % str(err))

    def SelectionMissingError(self):
        self.ThrowException(self.mainDlg, 'Please select the column where the thresholds apply')

    def NotANumberError(self, value):
        self.ThrowException(self.mainDlg, '%s is not a valid number' % value)

    def BaseDataType(self, columnName=None):
        name  = self.DataTypeName(columnName or self.SelectedColumnName())
        res = str()
        if name and name not in DataTypesSettings.BuiltInTypes():
            param = self.DataTypeParam(name)
            res = '\n'.join(str(k)+'='+str(param.At(k)) for k in param.Keys())
        else:
            res = '\n'.join(('data_type=%s' % name, res))
        return '\n'.join(('base=%s' % name, res))

    def SaveThreshold(self, name):
        thresholds = (
                self._DECIMALS,
                self._THRESHOLD_PCT,
                self._THRESHOLD_ABS
                )
        if name in thresholds:
            thresholdName = self.ThresholdName()
            if thresholdName:
                try:
                    if not self.clearing:
                        data = self.ctrls[name].GetData()
                        self.clearing = False
                        if data:
                            float(data)
                        self.thresholds[thresholdName][name] = data
                except ValueError:
                    self.ctrls[name].Clear()
                    self.NotANumberError(data)

    def OnSaveThresholds(self, _args=None, _cd=None):
        try:
            context = acm.GetDefaultContext()
            module = self.Module()
            self.HandleApplyThresholds(context, module)
            module.Commit()
            self.Edited(False)
            self.thresholds.clear()
            #self.SaveThresholdSucceeded(name, module.Name())
        except ValueError as err:
            self.ParamMissingError(err)
        except TypeError:
            self.SelectionMissingError()
        except RuntimeError as err:
            module.Undo()
            self.SaveThresholdFailed(err)

    def ThresholdParams(self, name):
        try:
            res = []
            dataTypeParam = self.DataTypeParam(name)
            decimals = dataTypeParam.GetString(self._DECIMALS)
            res.append((self._DECIMALS, decimals))
            thresholdPct = dataTypeParam.GetString(self._THRESHOLD_PCT)
            res.append((self._THRESHOLD_PCT, thresholdPct))
            thresholdAbs = dataTypeParam.GetString(self._THRESHOLD_ABS)
            res.append((self._THRESHOLD_ABS, thresholdAbs))
            return '\n'.join(i+'='+j for i, j in res)
        except ValueError:
            return str()

    def ApplyThresholdInMemory(self, context, module, thresholdName):
        paramValues = self.thresholds.get(thresholdName)
        reconName = str(self.reconNameCtrl.GetData())
        name = ''.join((reconName, thresholdName))
        if list(set(paramValues.values())) != ['']:
            params = ['FObject:%s =\n' % name]
            params.append(
                '\n'.join(
                    key + '=' + str(value)
                    for key, value in paramValues.items()
                    )
                )
            params.append('\n'+ self.BaseDataType())
            context.EditImport('FParameters', ''.join(params), True, module)
        else:
            self.DeleteDataType(name)

    def ApplyThreshold(self, context, module, columnName, dataTypeName):
        try:
            dataTypeParam = self.DataTypeParam(dataTypeName)
            baseName = dataTypeParam.GetString('data_type')
            if self.IsNumeric(baseName):
                name = self.DataTypeParameterName(columnName)
                params = ['FObject:%s =\n' % name]
                params.append(
                    '\n'.join((
                        self.BaseDataType(columnName),
                        self.ThresholdParams(name)))
                    )
                context.EditImport('FParameters', ''.join(params), True, module)
        except ValueError:
            pass

    def HandleApplyThresholds(self, context, module):
        root = self.dataTypeSettings.pairsCtrl.GetRootItem()
        for child in root.Children():
            pair = child.GetData()
            columnName = str(pair.First())
            cmpRoot = self.pairsCtrl.GetRootItem()
            for cmpChild in cmpRoot.Children():
                cmpPair = cmpChild.GetData()
                if columnName in (str(cmpPair.First()), ):
                    thresholdName = ''.join((columnName, 'DataType'))
                    if thresholdName in self.thresholds:
                        self.ApplyThresholdInMemory(context, module, thresholdName)
                    else:
                        dataTypeName = str(pair.Second())
                        self.ApplyThreshold(context, module, columnName, dataTypeName)

    def InitCallbacks(self):
        self.pairsCtrl.AddCallback('SelectionChanged', self.OnPairsChanged, None)

    @staticmethod
    def Columns(group):
        context = acm.GetDefaultContext()
        sheetColumns = context.GetAllExtensions(
                'FColumnDefinition',
                None,
                True,
                True,
                'sheet columns',
                group)
        return sheetColumns

    @staticmethod
    def GroupLabel(column):
        try:
            groupLabel = column.At('GroupLabel')
            if groupLabel:
                return str(groupLabel)
            base = column.At('InheritsFrom')
            baseColumn = acm.GetDefaultContext().GetAllExtensions('FColumnDefinition', base)
            return ComparisonSettings.GroupLabel(baseColumn.First().Value())
        except StandardError:
            return 'None'

    @staticmethod
    def DisplayColumn(label):
        if str(label) not in ('None', ''):
            return True
        return False

    @staticmethod
    def ColumnsDict(group=str()):
        columnsDict = collections.defaultdict(set)
        for ext in ComparisonSettings.Columns(group):
            column = ext.Value()
            label = ComparisonSettings.GroupLabel(column)
            if ComparisonSettings.DisplayColumn(label):
                columnsDict[label].add(column)
        return columnsDict

    def PopulateFileData(self, data, _source=None):
        if _source:
            pairs = [str(p.First()) for p in self.Pairs()]
            data = [str(d) for d in data if str(d) not in pairs]
        self.Keys(data)
        self.PopulateKeysCtrl()

    def PopulateControls(self):
        group = self.applicationState.ColumnGroup()
        self.inputCtrl.AddCallback('Changed', self.OnChanged, None)
        self.Values(self.ColumnsDict(group or str()))
        self.PopulateTreeValuesCtrl(sortKey=self.ColumnSort)

    def OnChanged(self, _args, _cd):
        includes = self.inputCtrl.GetData()
        self.PopulateTreeValuesCtrl(includes)

    def SetControlValues(self, param, module):
        dataExtensions = self.GetModule(module).GetAllExtensions(
                'FParameters',
                param.GetSymbol(DataTypesSettings.ParamName()))
        extensions = self.GetModule(module).GetAllExtensions(
                'FParameters',
                param.GetSymbol(self.ParamName()))
        if extensions and dataExtensions:
            param = extensions.First().Value()
            dataParam = dataExtensions.First().Value()
            allparams = dataParam.Keys().AddAll(param.Keys()).AsSet()
            self.thresholds.clear()
            self.PopulateFileData(allparams)
            for key in allparams:
                value = param.At(key)
                if value:
                    self.OnAddKeyValue(key, value, True)

    def RemoveExtension(self, module, param):
        module.RemoveExtension('FParameters', 'FObject', param.GetSymbol(self.ParamName()))

    def ClearControlValues(self):
        self.pairs = set()
        for name, ctrl in self.ctrls.items():
            if name not in (self.VALUES, ):
                ctrl.Clear()

    def HandleApply(self, name, module):
        name = ''.join((name, self.NameSpace()))
        super(ComparisonSettings, self).HandleApply(name, module)


class AttributesSettings(MappingPane):

    _PARAM_NAME = 'External Attribute Map'
    _NAMESPACE = 'Attributes'
    _LABEL = 'Matching Attributes'

    def __init__(self, dlg, applicationState):
        super(AttributesSettings, self).__init__()
        self.mainDlg = dlg
        self.applicationState = applicationState
        self.ctrls = dict()

    @staticmethod
    def Attributes(selected):
        attributes = list()
        while selected.Parent():
            attributes.insert(0, str(selected.GetData().Name()))
            selected = selected.Parent()
        return attributes

    @staticmethod
    def DomainName(domain):
        elementDomain = domain.ElementDomain()
        if domain.IsArrayDomain() and elementDomain is not acm.FObject:
            return str(elementDomain.Name())
        return str(domain.DomainName())

    def PopulateFileData(self, data, _source=None):
        self.Keys(data)
        self.PopulateKeysCtrl()

    def OnSelectionChanged(self, _args=None, _cd=None):
        selected = self.valuesCtrl.GetSelectedItem()
        domain = selected.GetData().Domain()
        if domain.IsClass() and not selected.ChildrenCount():
            self.PopulateTree(
                    selected,
                    acm.FClass[self.DomainName(domain)]
                    )
        selectedValue = '.'.join(
                    (attr for attr in self.Attributes(selected))
                    )
        self.inputCtrl.SetData(selectedValue)

    def OnRemoveAllClicked(self, _args=None, _cd=None):
        self.pairsCtrl.Clear()
        self.pairs = set()

    def SetControlValues(self, param, module):
        dataExtensions = self.GetModule(module).GetAllExtensions(
                'FParameters',
                param.GetSymbol(DataTypesSettings.ParamName()))
        extensions = self.GetModule(module).GetAllExtensions(
                'FParameters',
                param.GetSymbol(self.ParamName()))
        if extensions and dataExtensions:
            param = extensions.First().Value()
            dataParam = dataExtensions.First().Value()
            allparams = dataParam.Keys().AddAll(param.Keys()).AsSet()
            self.PopulateFileData(allparams)
            for key in allparams:
                value = param.At(key)
                if value:
                    self.OnAddKeyValue(key, value)

    def RemoveExtension(self, module, param):
        module.RemoveExtension('FParameters', 'FObject', param.GetSymbol(self.ParamName()))

    def ClearControlValues(self):
        self.pairs = set()
        for name, ctrl in self.ctrls.items():
            if name not in (self.VALUES, ):
                ctrl.Clear()

    def OnRemoveClicked(self, _args=None, _cd=None):
        pairSelected = self.pairsCtrl.GetSelectedItem()
        if pairSelected:
            pair = pairSelected.GetData()
            self.RemoveItem(self.pairs, self.pairsCtrl, pair)
            self.AddKeyItems([pair.First()])

    def OnAddClicked(self, _args=None, _cd=None):
        selectedKey = self.keysCtrl.GetSelectedItem()
        if selectedKey:
            key = selectedKey.GetData()
            value = self.inputCtrl.GetData()
            if key and value:
                self.OnAddKeyValue(key, value)

    def OnAddKeyValue(self, key, value):
        pair = acm.FPair()
        pair.First(key)
        pair.Second(value)
        self.AddPairItem(pair)
        self.RemoveItem(self.keys, self.keysCtrl, key)
        self.SelectFirstItem(self.pairs, self.pairsCtrl)

    @staticmethod
    def AddChild(root, data, icon=None):
        child = root.AddChild()
        child.SetData(data)
        child.Label(data.Name())
        if icon:
            child.Icon(icon, icon)
        return child

    def PopulateTree(self, root, acmClass):
        for method in acmClass.PropertyGetMethods():
            domain = method.Domain()
            if domain.IsClass():
                self.AddChild(root, method)
            else:
                self.AddChild(root, method, 'BlueBall')

    def PopulateValuesCtrl(self, name):
        acmClass = acm.FClass[name]
        self.valuesCtrl.Clear()
        root = self.valuesCtrl.GetRootItem()
        child = self.AddChild(root, acmClass)
        self.PopulateTree(child, acmClass)

    def HandleCreate(self):
        builder = self.CreateLayout()
        attributesLayout = self.mainDlg.AddPane(self.TabLabel(), builder)
        super(AttributesSettings, self).HandleCreate(attributesLayout)
        self.inputCtrl.Editable(False)
        self.valuesCtrl.AddCallback('SelectionChanged', self.OnSelectionChanged, None)
        self.PopulateValuesCtrl(self.applicationState.SubClass())
        self.InitPairsDefaultActionCallback()
        self.InitKeyValuesDefaultActionCallBack()
        self.InitEditCallbacks()

    def GetData(self, key, values):
        return '='.join((self.AsString(key), ','.join(self.AsString(value) for value in values)))

    def Parameters(self):
        attrs = collections.defaultdict(set)
        root = self.pairsCtrl.GetRootItem()
        for child in root.Children():
            pair = child.GetData()
            attrs[pair.First()].add(pair.Second())
        return '\n'.join(self.GetData(key, values) for key, values in attrs.items())

    def HandleApply(self, name, module):
        name = ''.join((name, self.NameSpace()))
        super(AttributesSettings, self).HandleApply(name, module)

    def PopulateControls(self):
        raise NotImplementedError


class IdRulesSettings(SelectionPane):

    _PARAM_NAME = 'Identification Rules'
    _NAMESPACE = 'IdRules'
    _LABEL = 'Identification Rules'

    def __init__(self, dlg, applicationState, idKeysLabel='Shared Queries', idPairsLabel='Search Hierarchy'):
        super(IdRulesSettings, self).__init__(keysLabel=idKeysLabel, pairsLabel=idPairsLabel)
        self.mainDlg = dlg
        self.applicationState = applicationState
        self.btnNew = None
        self.btnView = None
        self.btnViewSelected = None
        self.queriesList = None
        self.ctrls = dict()

    def PopulateControls(self):
        queries = self.Queries()
        self.Keys(queries)
        self.PopulateKeysCtrl()

    def AddPairItem(self, item):
        self.pairs.append(item)
        self.PopulatePairsControl()

    def OnAddKey(self, key, selection=False):
        pair = acm.FPair()
        pair.Second(key)
        self.AddPairItem(pair)
        self.RemoveItem(self.keys, self.keysCtrl, key, selection)
        self.SelectFirstItem(self.pairs, self.pairsCtrl)

    def OnAddClicked(self, _args=None, _cd=None):
        selectedKey = self.keysCtrl.GetSelectedItem()
        if selectedKey:
            key = selectedKey.GetData()
            self.OnAddKey(key)

    def RemoveItem(self, items, listCtrl, item, selection=False):
        itemsList = list(items)
        try:
            index = itemsList.index(item)
            items.remove(item)
            if selection:
                self.AddKeyItems(items)
            else:
                if item.IsKindOf(acm.FPair):
                    self.PopulatePairsControl()
                    if not items:
                        self.Edited(True)
                else:
                    listCtrl.RemoveAllSelectedItems(True)
            self.SelectNewItem(items, index, itemsList, listCtrl)
        except StandardError:
            pass

    def OnRemoveAllClicked(self, _args=None, _cd=None):
        for pair in self.pairs:
            item = pair.Second()
            self.keys.add(item)
        self.pairs = list()
        self.pairsCtrl.Clear()
        self.AddKeyItems(self.keys)

    def OnRemoveClicked(self, _args=None, _cd=None):
        pairSelected = self.pairsCtrl.GetSelectedItem()
        if pairSelected:
            pair = pairSelected.GetData()
            self.AddKeyItems([pair.Second()])
            self.RemoveItem(self.pairs, self.pairsCtrl, pair)

    def OnKeysDefaultAction(self, _args, _cd):
        self.OnAddClicked()

    def Queries(self):
        # Works with instypes? FStock for example...
        return acm.FStoredASQLQuery.Select('subType="%s" and user=None' %
                self.applicationState.SubClass())

    def SetControlValues(self, param, module):
        extensions = self.GetModule(module).GetAllExtensions('FParameters', param.GetSymbol(self.ParamName()))
        if extensions:
            param = extensions.First().Value()
            ruleKeysSorted = sorted([key for key in param.Keys()])
            queries = self.Queries()
            for key in ruleKeysSorted:
                try:
                    query = [
                        q
                        for q in queries
                        if q.Name() in (str(param.At(key)), )
                        ][0]
                    if query in queries:
                        self.OnAddKey(query, True)
                except IndexError:
                    pass

    def RemoveExtension(self, module, param):
        module.RemoveExtension('FParameters', 'FObject', param.GetSymbol(self.ParamName()))

    def ClearControlValues(self):
        self.pairs = []
        for name, ctrl in self.ctrls.items():
            if name not in (self.KEYS, ):
                ctrl.Clear()

    def InitDefaultActionCallbacks(self):
        self.keysCtrl.AddCallback('DefaultAction', self.OnKeysDefaultAction, None)
        self.InitPairsDefaultActionCallback()

    def InitIdRulesControls(self, layout):
        self.btnNew = layout.GetControl('btnNew')
        self.btnView = layout.GetControl('btnView')
        self.btnViewSelected = layout.GetControl('btnViewSelected')

    @staticmethod
    def OnViewClicked(ctr, _cd):
        item = ctr.GetSelectedItem()
        if item:
            data = item.GetData()
            query = (data if not data.IsKindOf(acm.FPair)
                    else data.Second())
            acm.StartFASQLEditor(
                    None,
                    None,
                    query,
                    None,
                    None,
                    '',
                    False)

    def ServerUpdate(self, _sender, _aspect, _param):
        if str(_aspect) in ('OnDestroy', ):
            self.PopulateControls()
            try:
                newQueries = self.Queries().AsList()
                queries = newQueries.RemoveAll(self.queriesList)
                for query in queries:
                    if query.CreateUser().Name() == acm.UserName():
                        self.OnAddKey(query)
            except StandardError:
                pass
            finally:
                self.queriesList = None
                _sender.RemoveDependent(self)

    def OnNewClicked(self, _args, _cd):
        subtype = self.applicationState.SubClass()
        if type(subtype) == str and hasattr(acm, subtype):
            subtype = getattr(acm, subtype)
        else:
            logger.error('Subclass %s not available'%(subtype))
            raise AttributeError('No persistant class named %s'%(subtype))

        asqlEditor = acm.StartFASQLEditor(
                    None,
                    subtype,
                    None,
                    None,
                    None,
                    '',
                    False)
        self.queriesList = self.Queries().AsList()
        asqlEditor.AddDependent(self)

    def InitIdRulesCallbacks(self):
        self.btnNew.AddCallback('Activate', self.OnNewClicked, None)
        self.btnView.AddCallback('Activate', self.OnViewClicked, self.keysCtrl)
        self.btnViewSelected.AddCallback('Activate', self.OnViewClicked, self.pairsCtrl)

    def HandleCreate(self):
        builder = self.CreateLayout()
        idRulesLayout = self.mainDlg.AddPane(self.TabLabel(), builder)
        super(IdRulesSettings, self).HandleCreate(idRulesLayout)
        self.InitIdRulesControls(idRulesLayout)
        self.InitIdRulesCallbacks()
        self.PopulateControls()
        self.InitDefaultActionCallbacks()
        self.InitEditCallbacks()

    def HandleApply(self, name, module):
        name = ''.join((name, self.NameSpace()))
        super(IdRulesSettings, self).HandleApply(name, module)


class DataTypeEditor(FUxCore.LayoutDialog):

    NAME = 'dataTypeName'
    DATA_TYPE = 'data_type'
    DECIMAL_SIGN = 'decimal_sign'
    THOUSAND_SEPARATOR = 'thousand_separator'
    DATE_FORMAT = 'date_format'

    def __init__(self, datatype, settings):
        self.datatype = datatype
        self.settings = settings
        self.moduleCtrl = settings.moduleCtrl
        self.edited = False
        self.dlg = None
        self.dataNameCtrl = None
        self.dataTypeCtrl = None
        self.decimalSeparatorCtrl = None
        self.thousandSeparatorCtrl = None
        self.dateFormatCtrl = None
        self.ctrls = dict()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('EtchedIn', '')
        b.    AddInput(self.NAME, 'Name', 30)
        b.    AddComboBox(self.DATA_TYPE, 'Type')
        b.    AddComboBox(self.DECIMAL_SIGN, 'Decimal Sign')
        b.    AddComboBox(self.THOUSAND_SEPARATOR, 'Thousand Separator')
        b.    AddInput(self.DATE_FORMAT, 'Date Format')
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('ok', 'Save')
        b.    AddButton('cancel', 'Close')
        b.  EndBox()
        b.EndBox()
        return b

    def Edited(self, edited=None):
        if edited is None:
            return self.edited
        self.edited = edited

    def InitControl(self, layout, ctrlName):
        if ctrlName not in self.ctrls:
            ctrl = layout.GetControl(ctrlName)
            self.ctrls[ctrlName] = ctrl
        return self.ctrls[ctrlName]

    def PopulateControls(self):
        self.dataNameCtrl.SetData(self.datatype.StringKey())
        self.dataTypeCtrl.SetData(self.datatype.GetString(self.DATA_TYPE))
        self.decimalSeparatorCtrl.SetData(self.datatype.GetString(self.DECIMAL_SIGN))
        self.thousandSeparatorCtrl.SetData(self.datatype.GetString(self.THOUSAND_SEPARATOR))
        self.dateFormatCtrl.SetData(self.datatype.GetString(self.DATE_FORMAT))
        self.OnSelectionChanged()

    def InitControls(self, layout):
        self.dataNameCtrl = self.InitControl(layout, self.NAME)
        self.dataTypeCtrl = self.InitControl(layout, self.DATA_TYPE)
        self.decimalSeparatorCtrl = self.InitControl(layout, self.DECIMAL_SIGN)
        self.thousandSeparatorCtrl = self.InitControl(layout, self.THOUSAND_SEPARATOR)
        self.dateFormatCtrl = self.InitControl(layout, self.DATE_FORMAT)

    def VisibleControls(self, visible=True):
        self.decimalSeparatorCtrl.Visible(visible)
        self.thousandSeparatorCtrl.Visible(visible)
        self.dateFormatCtrl.Visible(not visible)

    def InitDataTypeCtrl(self):
        for i in ('date', 'float'):
            self.dataTypeCtrl.AddItem(i)
        self.dataTypeCtrl.SetData('float')

    def InitDecimalSeparatorCtrl(self):
        for i in ('.', ','):
            self.decimalSeparatorCtrl.AddItem(i)
        self.decimalSeparatorCtrl.SetData('.')

    def InitThousandSeparatorCtrl(self):
        for i in ('.', ',', ' '):
            self.thousandSeparatorCtrl.AddItem(i)
        self.thousandSeparatorCtrl.SetData('.')

    def InitDefaults(self):
        self.InitDataTypeCtrl()
        self.InitDecimalSeparatorCtrl()
        self.InitThousandSeparatorCtrl()
        self.VisibleControls()

    def OnSelectionChanged(self, _args=None, _cd=None):
        self.VisibleControls(
                True
                if self.dataTypeCtrl.GetData() in ('float', )
                else False
                )

    def OnCtrlChanged(self, _dlg, _cd):
        self.Edited(True)

    def InitEditCallbacks(self):
        for ctrl in self.ctrls.values():
            ctrl.AddCallback('Changed', self.OnCtrlChanged, None)

    def InitCallbacks(self):
        self.dataTypeCtrl.AddCallback('Changed', self.OnSelectionChanged, None)

    def HandleCancel(self):
        if self.Edited():
            TEXT = ('Current settings have not been saved.\n'
                   'Do you wish to disregard changes?')
            res = acm.UX().Dialogs().MessageBoxOKCancel(
                    self.dlg.Shell(),
                    'Question',
                    TEXT)
            if res not in ('Button1', ):
                return None
        return True

    def MissingModule(self):
        name = self.moduleCtrl.GetData()
        if not name:
            TEXT = ('A Module needs to be selected\n'
                   'before saving the new data type')
        try:
            acm.UX().Dialogs().MessageBox(
                    self.dlg.Shell(),
                    'Error',
                    TEXT,
                    'OK',
                    None,
                    None,
                    'Button1',
                    'None')
            return True
        except NameError:
            return False

    def GetData(self, key):
        return self.ctrls[key].GetData()

    def Module(self):
        if self.datatype:
            return [
                m
                for m in acm.GetDefaultContext().Modules()
                if m.ExtensionExists(acm.FParameters, self.datatype.Name())
                ][0]
        else:
            data = self.moduleCtrl.GetData()
            return [
                m
                for m in acm.GetDefaultContext().Modules()
                if m.Name() in (data, )
                ][0]

    def HandleApplyBase(self, name, parameters):
        params = ['FObject:%s =\n' % name]
        params.append(
            '\n'.join(
                (key+'='+self.GetData(key)
                for key in parameters))
            )
        try:
            context = acm.GetDefaultContext()
            module = self.Module()
            context.EditImport('FParameters', ''.join(params), True, module)
            module.Commit()
        except RuntimeError as err:
            module.Undo()
            raise RuntimeError(err)

    def SaveSucceeded(self, name, moduleName):
        acm.UX().Dialogs().MessageBoxInformation(
                self.dlg.Shell(),
                '%s data type successfully saved in module %s.' % (name, moduleName))

    def SaveFailed(self, err):
        acm.UX().Dialogs().MessageBox(
                self.dlg.Shell(),
                'Error',
                'Could not save data type.\nReason: %s' % str(err),
                'OK',
                None,
                None,
                'Button1',
                'None')

    def HandleApply(self):
        if self.datatype or not self.MissingModule():
            name = self.dataNameCtrl.GetData()
            parameters = [k for k in self.ctrls if k not in (self.NAME, )]
            try:
                self.HandleApplyBase(name, parameters)
                self.SaveSucceeded(name, self.Module().Name())
                self.settings.PopulateControls()
                self.Edited(False)
            except RuntimeError as err:
                self.SaveFailed(err)

    def HandleCreate(self, dlg, layout):
        dlg.Caption('Data Type Editor')
        self.dlg = dlg
        self.InitControls(layout)
        self.InitDefaults()
        self.InitCallbacks()
        if self.datatype:
            self.PopulateControls()


class DataTypesSettings(MappingPane):

    _PARAM_NAME = 'External Data Type Map'
    _NAMESPACE = 'DataTypes'
    _LABEL = 'Data Types'
    _DEFAULT_CATEGORY = 'Built-in'
    _DEFAULT_DATA_TYPES = ['float', 'integer', 'string']
    _DATA_TYPE_CATEGORIES = ['Date & Time', 'Date', 'Float', 'Integer']

    def __init__(self, dlg, applicationState, moduleCtrl, reconNameCtrl):
        self.pairsCtrl = None
        super(DataTypesSettings, self).__init__(valuesLabel='Type')
        self.mainDlg = dlg
        self.applicationState = applicationState
        self.moduleCtrl = moduleCtrl
        self.reconNameCtrl = reconNameCtrl
        self.ctrls = dict()

    @classmethod
    def BuiltInTypes(cls):
        return cls._DEFAULT_DATA_TYPES

    def OnNewClicked(self, _args, _cd):
        shell = self.mainDlg.Shell()
        dataTypeEditor = DataTypeEditor(_args, self)
        builder = dataTypeEditor.CreateLayout()
        acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dataTypeEditor)

    def OnEditClicked(self, _args, _cd):
        datatype = self.valuesCtrl.GetSelectedItem().GetData()
        self.OnNewClicked(datatype, None)

    def DeleteError(self, name):
        TEXT = ('Data Type %s is in a built in module and cant be deleted.' % name)
        self.ThrowException(self.mainDlg, TEXT)

    def DeleteFailed(self, name, err):
        TEXT = ('Failed to delete Data Type %s.\nReason: %s.' % (name, err))
        self.ThrowException(self.mainDlg, TEXT)

    def OnDeleteClicked(self, _args, _cd):
        datatype = self.valuesCtrl.GetSelectedItem().GetData()
        datatypeName = datatype.StringKey()
        if self.ConfirmDelete(datatypeName):
            modules = [m for m in acm.GetDefaultContext().Modules() if not m.IsBuiltIn()]
            for module in modules:
                if module.RemoveExtension(acm.FParameters, acm.FObject, datatypeName):
                    try:
                        module.Commit()
                        self.PopulateControls()
                        return None
                    except RuntimeError as err:
                        module.Undo()
                        self.DeleteFailed(datatypeName, err)
            self.DeleteError(datatypeName)

    @staticmethod
    def CustomDataTypes():
        parameters = acm.GetDefaultContext().GetAllExtensions('FParameters')
        return [
            param.Value()
            for param in parameters
            if param.Value().GetString('data_type')
            ]

    @classmethod
    def CategorisedDataTypes(cls):
        types = collections.defaultdict(list)
        types[cls._DEFAULT_CATEGORY] = cls._DEFAULT_DATA_TYPES
        for dataType in cls.CustomDataTypes():
            dataTypeName = str(dataType.Name())
            if not dataTypeName.endswith(ComparisonSettings.Token()):
                for category in cls._DATA_TYPE_CATEGORIES:
                    if dataTypeName.startswith(category):
                        types[category].append(dataType)
                        break
                else:
                    types['Custom'].append(dataType)
        return types

    def PopulateControls(self):
        values = self.CategorisedDataTypes()
        self.Values(values)
        self.PopulateTreeValuesCtrl(icon='OpenFolder')

    def EnabledEditControls(self, enabled=True):
        self.btnEditCtrl.Enabled(enabled)
        self.btnDelCtrl.Enabled(enabled)

    def InitDataTypesSettings(self):
        root = self.valuesCtrl.GetRootItem()
        defaultCategory = root.Children().First()
        defaultCategory.Expand()
        self.EnabledEditControls(False)

    def OnSelectionChanged(self, _args=None, _cd=None):
        selectedItem = self.valuesCtrl.GetSelectedItem()
        self.EnabledEditControls(selectedItem.ChildrenCount() == 0 and
                selectedItem.GetData() not in self._DEFAULT_DATA_TYPES)

    def SetControlValues(self, param, module):
        extensions = self.GetModule(module).GetAllExtensions('FParameters', param.GetSymbol(self.ParamName()))
        if extensions:
            param = extensions.First().Value()
            self.PopulateFileData(param.Keys())
            for key in param:
                dataTypeName = str(param.At(key))
                if self.IsCustomDataType(dataTypeName):
                    try:
                        dataTypeParam = ComparisonSettings.DataTypeParam(dataTypeName)
                        if ComparisonSettings.IsNumeric(dataTypeParam.GetString('data_type')):
                            dataTypeBaseName = dataTypeParam.GetString('base')
                            dataTypeName = (
                                    dataTypeBaseName
                                    if dataTypeBaseName
                                    else dataTypeName
                                    )
                    except ValueError as e:
                        logger.info(
                                'Ignoring %s mapping: %s - %s. %s',
                                self._LABEL,
                                key,
                                dataTypeName,
                                e
                                )
                        continue
                self.OnAddKeyValue(key, dataTypeName, True)

    def RemoveExtension(self, module, param):
        module.RemoveExtension('FParameters', 'FObject', param.GetSymbol(self.ParamName()))

    def ClearControlValues(self):
        self.pairs = set()
        for name, ctrl in self.ctrls.items():
            if name not in (self.VALUES, ):
                ctrl.Clear()

    def PopulateFileData(self, data, _source=None):
        if _source:
            pairs = [str(p.First()) for p in self.Pairs()]
            data = [str(d) for d in data if str(d) not in pairs]
        self.Keys(data)
        self.PopulateKeysCtrl()

    def DataTypeParameterName(self, columnName):
        reconName = str(self.reconNameCtrl.GetData())
        return ''.join((
            reconName,
            columnName,
            'DataType'
            ))

    def IsCustomDataType(self, name):
        return name not in self.BuiltInTypes()

    def GetDataType(self, item):
        pair = item.GetData()
        columnName = str(pair.First())
        baseDataType = dataTypeName = str(pair.Second())
        if self.IsCustomDataType(dataTypeName):
            dataType = ComparisonSettings.DataTypeParam(dataTypeName)
            baseDataType = dataType.GetString('data_type') if dataType else dataTypeName
        if ComparisonSettings.IsNumeric(baseDataType):
            try:
                extendedDataTypeName = self.DataTypeParameterName(columnName)
                dataTypeName = (
                        extendedDataTypeName
                        if ComparisonSettings.DataTypeParam(extendedDataTypeName)
                        else dataTypeName
                        )
            except ValueError:
                pass
        return '='.join((columnName, dataTypeName))

    def Parameters(self):
        root = self.pairsCtrl.GetRootItem()
        return '\n'.join(self.GetDataType(child) for child in root.Children())

    def HandleCreate(self):
        builder = self.CreateLayout()
        dataTypeLayout = self.mainDlg.AddPane(self.TabLabel(), builder)
        super(DataTypesSettings, self).HandleCreate(dataTypeLayout)
        self.PopulateControls()
        self.InitDataTypesSettings()
        self.btnNewCtrl.AddCallback('Activate', self.OnNewClicked, None)
        self.btnEditCtrl.AddCallback('Activate', self.OnEditClicked, None)
        self.btnDelCtrl.AddCallback('Activate', self.OnDeleteClicked, None)
        self.valuesCtrl.AddCallback('SelectionChanged', self.OnSelectionChanged, None)
        self.InitPairsDefaultActionCallback()
        self.InitKeyValuesDefaultActionCallBack()
        self.InitEditCallbacks()

    def HandleApply(self, name, module):
        name = ''.join((name, self.NameSpace()))
        super(DataTypesSettings, self).HandleApply(name, module)


class UniverseQueries(IdRulesSettings):

    _PARAM_NAME = 'Universe Queries'
    _NAMESPACE = 'UniverseQueries'
    _LABEL = 'Two Way Reconciliation'

    def __init__(self, dlg, applicationState):
        super(UniverseQueries, self).__init__(dlg, applicationState, idPairsLabel='Universe Queries')

    def HandleApply(self, name, module):
        pass

    def RemoveExtension(self, module, param):
        pass

    def GetData(self, item):
        pair = item.GetData()
        second = pair.Second()
        return self.AsString(second)

    def Universe(self):
        root = self.pairsCtrl.GetRootItem()
        return ','.join(self.GetData(child) for child in root.Children())

    def InitControls(self, layout):
        super(UniverseQueries, self).InitControls(layout)

    def SetToolTips(self):
        super(UniverseQueries, self).SetToolTips()

    def SetControlValues(self, param, module):
        extensions = self.GetModule(module).GetAllExtensions('FParameters', param.Name())
        if extensions:
            param = extensions.First().Value().GetString(self.ParamName()).split(',')
            queries = self.Queries()
            for key in param:
                try:
                    query = [
                        q
                        for q in queries
                        if q.Name() in (key, )
                        ][0]
                    if query in queries:
                        self.OnAddKey(query, True)
                except IndexError:
                    pass

class AdvancedPane(Control):

    _SHEET_TEMPLATE_CTRL = 'sheetTemplate'
    _BP_TEMPLATE_CTRL = 'bpTemplate'
    _CMP_TYPE_CTRL = 'cmpType'
    _SHEET_TEMPLATE = 'Sheet Template'
    _BP_TEMPLATE = 'Business Process Sheet Template'
    _CMP_TYPE = 'Comparison Type'
    _STORE_ITEMS_CTRL = 'storeItems'
    _STORE_ITEMS = 'Store Reconciled Items'
    MAX_UNIVERSE = 'maxUniverse'
    _MAX_UNIVERSE_PARAM_NAME = 'Max Nbr Of Items Missing in Document'
    MAX_NBR_OF_UNCLOSED_RECONITEMS = 'maxNbrOfUnclosedReconItems'
    _MAX_NBR_OF_UNCLOSED_RECONITEMS_PARAM_NAME = 'Max Nbr Of Unclosed Recon Items'

    _STORE_SUCCESSFUL_RECON_ITEMS_CAPTION = 'Store successfully reconciled items and business processes'

    # Recon limits
    _MAX_UNIVERSE_DEFAULT = '500'
    _MAX_NBR_OF_RECONITEMS_THRESHOLD = '500'

    _CREATE_COLUMN_DEFINITIONS_ON_SAVE = 'Create column definitions on save'
    _CREATE_COLUMN_DEFINITIONS_ON_SAVE_CTRL = 'createColumnDefinitionsOnSave'

    # Hooks
    PARSER_HOOK         = "parserHook"
    PARSER_HOOK_BUTTON ="parserHookButton"
    _PARSER_PARAM_NAME = "Parser Hook"

    EXTERNAL_VALUES_HOOK = "externalValuesHook"
    EXTERNAL_VALUES_HOOK_BUTTON ="externalValuesHookButton"
    _EXTERNAL_VALUES_PARAM_NAME = "External Values Hook"

    IDENTIFICATION_HOOK = "idHook"
    IDENTIFICATION_HOOK_BUTTON ="idHookButton"
    _ID_PARAM_NAME = "Identify Item Hook"

    IDENTIFICATION_VALUE_HOOK = "idValueHook"
    IDENTIFICATION_VALUE_HOOK_BUTTON ="idValueHookButton"
    _ID_VALUE_PARAM_NAME = "Identification Values Hook"

    PRE_COMMIT_HOOK = "preCommitHook"
    PRE_COMMIT_HOOK_BUTTON = "preCommitHookButton"
    _PRE_COMMIT_PARAM_NAME = "Pre Commit Hook"
    
    POST_PROCESSING_HOOK = "postProcessingHook"
    POST_PROCESSING_HOOK_BUTTON = "postProcessingHookButton"
    _POST_PROCESSING_PARAM_NAME = "Post Processing Hook"

    moduleRegex = re.compile('^(\w+)\.')
    onlyNumbers = re.compile('^\W*(\d*)\W*$')

    def __init__(self,layout, applicationState, generalSettings, label='Advanced'):
        super(AdvancedPane, self).__init__()
        self.applicationState = applicationState
        self.parserControl = None
        self.parserEdit = None
        self.externalValuesHookControl = None
        self.externalValuesHookEdit = None
        self.idControl = None
        self.idEdit = None
        self.idValueControl = None
        self.idValueEdit = None
        self.preCommitControl = None
        self.preCommitEdit = None
        
        self.postProcessingControl = None
        self.postProcessingEdit = None

        self.bpTemplateCtrl = None
        self.tradingTemplateCtrl = None
        self.cmpTypeCtrl = None

        self.storeItems = None
        self.maxUniverseControl = None
        self.maxNbrOfUnclosedReconItemsControl = None
        self.createColumnDefinitionsOnSaveControl = None

        self.generalSettings = generalSettings

        self.mainDlg = layout
        self.label = label
        self.ctrls = dict()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginVertBox('EtchedIn', 'General')
        b.  AddOption(self._CMP_TYPE_CTRL, 'Displayed Comparison')
        b.  AddCheckbox(self._STORE_ITEMS_CTRL, self._STORE_SUCCESSFUL_RECON_ITEMS_CAPTION)
        b.  AddCheckbox(self._CREATE_COLUMN_DEFINITIONS_ON_SAVE_CTRL, 'Create column definitions on save')
        b. EndBox()
        b. BeginVertBox('EtchedIn', 'Sheet Templates')
        b.  AddOption(self._BP_TEMPLATE_CTRL, 'Business Process Sheet')
        b.  AddOption(self._SHEET_TEMPLATE_CTRL,  'Object Sheet')
        b. EndBox()
        b. BeginVertBox('EtchedIn', 'Hooks')
        b.  BeginHorzBox()
        b.   AddInput(self.PARSER_HOOK, 'File Format Hook', 100, 100, 400, 'Horizontal')
        b.   AddButton(self.PARSER_HOOK_BUTTON, 'View...')
        b.  EndBox()
        b.  BeginHorzBox()
        b.   AddInput(self.EXTERNAL_VALUES_HOOK, 'External Values Hook', 100, 100, 400, 'Horizontal')
        b.   AddButton(self.EXTERNAL_VALUES_HOOK_BUTTON, 'View...')
        b.  EndBox()
        b.  BeginHorzBox()
        b.   AddInput(self.IDENTIFICATION_VALUE_HOOK, 'Identification Values Hook', 100, 100, 400, 'Horizontal')
        b.   AddButton(self.IDENTIFICATION_VALUE_HOOK_BUTTON, 'View...')
        b.  EndBox()
        b.  BeginHorzBox()
        b.   AddInput(self.IDENTIFICATION_HOOK, 'Identify Item Hook', 100, 100, 400, 'Horizontal')
        b.   AddButton(self.IDENTIFICATION_HOOK_BUTTON, 'View...')
        b.  EndBox()
        if self.applicationState.IsUpload():
            b.  BeginHorzBox()
            b.   AddInput(self.PRE_COMMIT_HOOK, 'Pre Commit Hook', 100, 100, 400, 'Horizontal')
            b.   AddButton(self.PRE_COMMIT_HOOK_BUTTON, 'View...')
            b.  EndBox()
        if self.applicationState.IsUpload():
            b.  BeginHorzBox()
            b.   AddInput(self.POST_PROCESSING_HOOK, 'Post Processing Hook', 100, 100, 400, 'Horizontal')
            b.   AddButton(self.POST_PROCESSING_HOOK_BUTTON, 'View...')
            b.  EndBox()
        b. EndBox()
        if not self.applicationState.IsUpload():
            b.BeginVertBox('EtchedIn', 'Reconciliation')
            b.  AddInput(self.MAX_NBR_OF_UNCLOSED_RECONITEMS, 'Max Nbr Of Unclosed Recon Items', 100, 100, 400, 'Horizontal')
            b.  BeginVertBox('None', 'Two Way Reconciliation')
            b.      AddInput(self.MAX_UNIVERSE, 'Max Nbr Of Items Missing in Document', 100, 100, 400, 'Horizontal')
            b.  EndBox()
            b.EndBox()
        b. AddFill()
        b.EndBox()
        return b

    def InitCallbacks(self):
        self.parserControl.AddCallback('Changed', self.OnModuleChanged, (self.parserControl, self.parserEdit))
        self.parserEdit.AddCallback('Activate', self.OnEditClicked, self.parserControl)
        self.externalValuesHookControl.AddCallback('Changed', self.OnModuleChanged, (self.externalValuesHookControl, self.externalValuesHookEdit))
        self.externalValuesHookEdit.AddCallback('Activate', self.OnEditClicked, self.externalValuesHookControl)
        self.idControl.AddCallback('Changed', self.OnModuleChanged, (self.idControl, self.idEdit))
        self.idEdit.AddCallback('Activate', self.OnEditClicked, self.idControl)
        self.idValueControl.AddCallback('Changed', self.OnModuleChanged, (self.idValueControl, self.idValueEdit))
        self.idValueEdit.AddCallback('Activate', self.OnEditClicked, self.idValueControl)

        if self.preCommitControl:
            self.preCommitControl.AddCallback('Changed', self.OnModuleChanged, (self.preCommitControl, self.preCommitEdit))
            self.preCommitEdit.AddCallback('Activate', self.OnEditClicked, self.preCommitControl)
        
        if self.postProcessingControl:
            self.postProcessingControl.AddCallback('Changed', self.OnModuleChanged, (self.postProcessingControl, self.postProcessingEdit))
            self.postProcessingEdit.AddCallback('Activate', self.OnEditClicked, self.postProcessingControl)

    def OnEditClicked(self, _args=None, _cd=None):
        moduleEntered = _args.GetData()
        module = self.moduleRegex.match(moduleEntered).group(1)
        textObject = acm.FPersistentText[module]
        if textObject:
            acm.StartApplication('Python Editor', textObject)
        else:
            logger.warn('Could not open module %s', module)

    def OnModuleChanged(self, _args=None, _cd=None):
        moduleEntered = _args[0].GetData()
        if moduleEntered:
            module = self.moduleRegex.match(moduleEntered)
            if module:
                _args[1].Enabled(True)
                return
        _args[1].Enabled(False)

    def PopulateTradingSheetTemplates(self, templates=None):
        if not templates:
            templates = acm.FTradingSheetTemplate.Select('').SortByProperty('Name')
        self.AddItems(self.tradingTemplateCtrl, self.applicationState.Filter(templates, self.applicationState.SheetClass()))
        if self.generalSettings.reconParam:
            try:
                paramName = [k for k, v in self.ctrls.items() if v is self.tradingTemplateCtrl][0]
                sheetTemplate = self.generalSettings.reconParam.GetString(paramName)
                self.tradingTemplateCtrl.SetData(sheetTemplate)
            except IndexError:
                pass

    def AddItems(self, ctrl, items):
        ctrl.Clear()
        for item in items:
            ctrl.AddItem(item)

    def PopulateControls(self):
        templates = acm.FTradingSheetTemplate.Select('').SortByProperty('Name')
        self.AddItems(self.bpTemplateCtrl, self.applicationState.Filter(templates, 'FBusinessProcessSheet'))
        self.PopulateTradingSheetTemplates(templates)
        self.AddItems(self.cmpTypeCtrl, self._CMP_TYPES)

    def RemoveExtension(self, module, param):
        pass

    def HandleApply(self, name, module):
        pass

    def InitControls(self, layout):
        self.bpTemplateCtrl = self.InitControl(layout, self._BP_TEMPLATE_CTRL, self._BP_TEMPLATE)
        self.tradingTemplateCtrl = self.InitControl(layout, self._SHEET_TEMPLATE_CTRL, self._SHEET_TEMPLATE)
        self.cmpTypeCtrl = self.InitControl(layout, self._CMP_TYPE_CTRL, self._CMP_TYPE)

        self.parserControl = self.InitControl(layout, self.PARSER_HOOK)
        self.parserEdit = self.InitControl(layout, self.PARSER_HOOK_BUTTON)
        self.parserEdit.Enabled(False)

        self.externalValuesHookControl = self.InitControl(layout, self.EXTERNAL_VALUES_HOOK)
        self.externalValuesHookEdit = self.InitControl(layout, self.EXTERNAL_VALUES_HOOK_BUTTON)
        self.externalValuesHookEdit.Enabled(False)

        self.idControl = self.InitControl(layout, self.IDENTIFICATION_HOOK)
        self.idEdit = self.InitControl(layout, self.IDENTIFICATION_HOOK_BUTTON)
        self.idEdit.Enabled(False)

        self.idValueControl = self.InitControl(layout, self.IDENTIFICATION_VALUE_HOOK)
        self.idValueEdit = self.InitControl(layout, self.IDENTIFICATION_VALUE_HOOK_BUTTON)
        self.idValueEdit.Enabled(False)

        self.storeItems = self.InitControl(layout, self._STORE_ITEMS_CTRL)
        self.createColumnDefinitionsOnSaveControl = self.InitControl(layout, self._CREATE_COLUMN_DEFINITIONS_ON_SAVE_CTRL)

        if self.applicationState.IsUpload():
            # Only for Upload
            self.preCommitControl = self.InitControl(layout, self.PRE_COMMIT_HOOK)
            self.preCommitEdit = self.InitControl(layout, self.PRE_COMMIT_HOOK_BUTTON)
            self.preCommitEdit.Enabled(False)
            
            self.postProcessingControl = self.InitControl(layout, self.POST_PROCESSING_HOOK)
            self.postProcessingEdit = self.InitControl(layout, self.POST_PROCESSING_HOOK_BUTTON)
            self.postProcessingEdit.Enabled(False)
        else:
            # Only for Reconciliation
            self.maxNbrOfUnclosedReconItemsControl = self.InitControl(layout, self.MAX_NBR_OF_UNCLOSED_RECONITEMS)
            self.maxUniverseControl = self.InitControl(layout, self.MAX_UNIVERSE)


    def TabLabel(self):
        return self.label

    def SetToolTips(self):
        self.parserControl.ToolTip('The hook function used to read item data from source with Custom File Format. Enter hook in format <module>.<function>')
        self.externalValuesHookControl.ToolTip('The hook function called after each item has been read from input, before identification. Use this hook to extend or manipulate the dictionary returned from the file parser. Enter hook in format <module>.<function>')
        self.idValueControl.ToolTip('Used to transform external reconciliation item values prior to identification. The input dictionary of this hook is a copy of the external values dictionary returned from the External Values Hook (if defined) or the file parser. Use this hook to manipulate the external values dictionary for the purpose of locating objects in the ADS (e.g., for completing a position query in a position reconciliation). Enter hook in format <module>.<function>')
        self.idControl.ToolTip('Can be used to manually identify the object to reconcile against. Use this hook when custom logic is needed in order to identify the reconciliation subject. Enter hook in format <module>.<function>')
        self.parserEdit.ToolTip('Launches python editor. Fill in the module name at least to "<module>." to enable.')
        self.externalValuesHookEdit.ToolTip('Launches python editor. Fill in the module name at least to "<module>." to enable.')
        self.idEdit.ToolTip('Launches python editor. Fill in the module name at least to "<module>." to enable.')
        self.idValueEdit.ToolTip('Launches python editor. Fill in the module name at least to "<module>." to enable.')
        if self.preCommitEdit:
            self.preCommitEdit.ToolTip('Launches python editor. Fill in the module name at least to "<module>." to enable.')
        self.cmpTypeCtrl.ToolTip("The type of comparison that will be shown for the objects")
        self.bpTemplateCtrl.ToolTip("Sheet template to show business processes")
        self.tradingTemplateCtrl.ToolTip("Sheet template to show the underlying objects of business processes")
        # SPR created to address this issue/choice of modelling
        self.storeItems.ToolTip("Reconciliation items and business processes will be created for successfully matched objects. Observe that such reconciliation items will not be displayed in the Operations Manager even if the display setting %s has been toggled." % self._STORE_SUCCESSFUL_RECON_ITEMS_CAPTION)
        self.createColumnDefinitionsOnSaveControl.ToolTip("FColumnDefinition extensions will be created on save")
        if not self.applicationState.IsUpload():
            self.maxNbrOfUnclosedReconItemsControl.ToolTip('Maximum number of unclosed reconciliation items (defined as any item that cannot be closed) and business processes allowed to be committed during a single reconciliation. If this number is exceeded, the remaining reconciliation items will be disregarded and hence no business processes will be created for those reconciliation items.')
            self.maxUniverseControl.ToolTip('Maximum number of missing document items allowed in a two way reconciliation. Set blank for no limit.')

    def OnRemoveAllClicked(self, _args=None, _cd=None):
        pass

    def GetData(self, key):
        ctrl = self.ctrls[key]
        if ctrl.IsKindOf(acm.FUxCheckBox):
            return ctrl.Checked()
        elif (key in (
                      self._CMP_TYPE_CTRL,
                      self._BP_TEMPLATE_CTRL,
                      self._SHEET_TEMPLATE_CTRL
                      ) and
              ctrl.GetData() in ('None', )):
            return ''
        return self.ctrls[key].GetData()

    def ClearControlValues(self):
        self.parserControl.SetData('')
        self.externalValuesHookControl.SetData('')
        self.idControl.SetData('')
        self.idValueControl.SetData('')
        self.cmpTypeCtrl.SetData('')
        self.bpTemplateCtrl.SetData('')
        self.tradingTemplateCtrl.SetData('')
        self.SetDefaultValues()
        self.storeItems.SetData(False)
        self.createColumnDefinitionsOnSaveControl.SetData(True)

    def SetDefaultValues(self):
        if self.generalSettings.readerTypeCtrl.GetData() == 'CSV':
            self.parserControl.SetData('')
            self.parserControl.Enabled(False)
        self.cmpTypeCtrl.SetData(self._CMP_TYPES[0])
        if not self.applicationState.IsUpload():
            self.maxNbrOfUnclosedReconItemsControl.SetData(self._MAX_NBR_OF_RECONITEMS_THRESHOLD)
            self.maxUniverseControl.SetData(self._MAX_UNIVERSE_DEFAULT)
        self.storeItems.Checked(False)
        self.createColumnDefinitionsOnSaveControl.Checked(True)

    def SetControlValues(self, param, module):
        extensions = acm.FExtensionModule[module].GetAllExtensions('FParameters', param.Name())
        if extensions:
            data = extensions.First().Value().GetString(self._CMP_TYPE)
            if data:
                self.cmpTypeCtrl.SetData(data)
            else:
                self.cmpTypeCtrl.SetData('None')

            data = extensions.First().Value().GetString(self._BP_TEMPLATE)
            if data:
                self.bpTemplateCtrl.SetData(data)
            data = extensions.First().Value().GetString(self._SHEET_TEMPLATE)
            if data:
                self.tradingTemplateCtrl.SetData(data)

            data = extensions.First().Value().GetString(self._PARSER_PARAM_NAME)
            if data:
                self.parserControl.SetData(data)
            data = extensions.First().Value().GetString(self._EXTERNAL_VALUES_PARAM_NAME)
            if data:
                self.externalValuesHookControl.SetData(data)
            data = extensions.First().Value().GetString(self._ID_PARAM_NAME)
            if data:
                self.idControl.SetData(data)
            data = extensions.First().Value().GetString(self._ID_VALUE_PARAM_NAME)
            if data:
                self.idValueControl.SetData(data)
            data = extensions.First().Value().GetString(self._PRE_COMMIT_PARAM_NAME)
            if self.preCommitControl:
                if data:
                    self.preCommitControl.SetData(data)
            
            data = extensions.First().Value().GetString(self._POST_PROCESSING_PARAM_NAME)
            if self.postProcessingControl:
                if data:
                    self.postProcessingControl.SetData(data)

            if not self.applicationState.IsUpload():
                # Max universe
                data = extensions.First().Value().GetString(self._MAX_UNIVERSE_PARAM_NAME)
                if data:
                    if data == 'N/A':
                        self.maxUniverseControl.SetData('')
                    else:
                        self.maxUniverseControl.SetData(data)
                # Max nbr of unclosed bps
                data = extensions.First().Value().GetString(self._MAX_NBR_OF_UNCLOSED_RECONITEMS_PARAM_NAME)
                if data:
                    if data == 'N/A':
                        self.maxNbrOfUnclosedReconItemsControl.SetData('')
                    else:
                        self.maxNbrOfUnclosedReconItemsControl.SetData(data)

            data = extensions.First().Value().GetString(self._STORE_ITEMS)
            if data and data == 'True':
                self.storeItems.Checked(True)
            else:
                self.storeItems.Checked(False)
            data = extensions.First().Value().GetString(self._CREATE_COLUMN_DEFINITIONS_ON_SAVE)
            if data and data == 'False':
                self.createColumnDefinitionsOnSaveControl.Checked(False)
            else:
                self.createColumnDefinitionsOnSaveControl.Checked(True)


    def Parameters(self):
        value = list()
        if self.parserControl.GetData():
            value.append(self._PARSER_PARAM_NAME + '=' + self.parserControl.GetData())
        if self.externalValuesHookControl.GetData():
            value.append(self._EXTERNAL_VALUES_PARAM_NAME + '=' + self.externalValuesHookControl.GetData())
        if self.idControl.GetData():
            value.append(self._ID_PARAM_NAME + '=' + self.idControl.GetData())
        if self.idValueControl.GetData():
            value.append(self._ID_VALUE_PARAM_NAME + '=' + self.idValueControl.GetData())
        if self.preCommitControl:
            if self.preCommitControl.GetData():
                value.append(self._PRE_COMMIT_PARAM_NAME + '=' + self.preCommitControl.GetData())
        
        if self.postProcessingControl:
            if self.postProcessingControl.GetData():
                value.append(self._POST_PROCESSING_PARAM_NAME + '=' + self.postProcessingControl.GetData())
        
        if not self.applicationState.IsUpload():
            mq = self.maxUniverseControl.GetData()
            mqTuple = ('Max Nbr Of Items Missing in Document', self._MAX_UNIVERSE_PARAM_NAME, mq)
            mnbps = self.maxNbrOfUnclosedReconItemsControl.GetData()
            mnbpsTuple = ('Max Nbr Of Unclosed Recon Items', self._MAX_NBR_OF_UNCLOSED_RECONITEMS_PARAM_NAME, mnbps)
            reconLimitInputList = [mqTuple, mnbpsTuple,]
            for reconLimitTuple in reconLimitInputList:
                attrName, paramName, paramValue = reconLimitTuple
                if paramValue:
                    try:
                        paramValue = int(paramValue)
                    except ValueError:
                        raise ValueError(attrName + ' is not a number')
                    if paramValue <= 0:
                        raise ValueError(attrName + ' must be larger than zero')
                    value.append(paramName + '=' + str(paramValue))
                else:
                    value.append(paramName + '=N/A')
        if self.cmpTypeCtrl.GetData():
            value.append(self._CMP_TYPE+'='+self.cmpTypeCtrl.GetData())
        if self.bpTemplateCtrl.GetData():
            value.append(self._BP_TEMPLATE+'='+self.bpTemplateCtrl.GetData())
        if self.tradingTemplateCtrl.GetData():
            value.append(self._SHEET_TEMPLATE+'='+self.tradingTemplateCtrl.GetData())
        if self.storeItems.Checked():
            value.append(self._STORE_ITEMS+'=True')
        else:
            value.append(self._STORE_ITEMS+'=False')
        if self.createColumnDefinitionsOnSaveControl.Checked():
            value.append(self._CREATE_COLUMN_DEFINITIONS_ON_SAVE+'=True')
        else:
            value.append(self._CREATE_COLUMN_DEFINITIONS_ON_SAVE+'=False')
        return value

    def HandleCreate(self):
        builder = self.CreateLayout()
        paneLayout = self.mainDlg.AddPane(self.TabLabel(), builder)
        self.InitControls(paneLayout)
        self.InitCallbacks()
        self.SetToolTips()
        self.PopulateControls()
        self.SetDefaultValues()


class GeneralSettings(Control):

    _NAME_CTRL = 'name'
    _NAME = 'Name'
    _READER_TYPE_CTRL = 'readerType'
    _READER_TYPE = 'File Format'
    _MODULE_CTRL = 'module'
    _MODULE = 'Module'
    _OBJECT_TYPE_CTRL = 'objectType'
    _OBJECT_TYPE = 'Object Type'
    _SUB_TYPE_CTRL = 'subType'
    _SUB_TYPE = 'Sub Type'
    _FX_RECON_CTRL = 'isFXRecon'
    _FX_RECON_CTRL_NAME = 'FX Recon'
    _STATE_CHART_CTRL = 'stateChart'
    _STATE_CHART = 'State Chart'
    #_INCLUDE_ZERO_CTRL = 'zeroPositions'
    #_INCLUDE_ZERO = 'Process Zero Positions'
    _OPEN_RECON_CTRL = 'openRecon'
    _OPEN_MODULE_CTRL = 'openModule'
    _FILE_PATH_CTRL = 'filePath'
    _FILE_PATH = 'File Path'
    _FILE_SELECTION_CTRL = 'fileSelection'
    _OPEN = '...'

    def __init__(self, dlg, applicationState):
        super(GeneralSettings, self).__init__()
        self.mainDlg = dlg
        self.applicationState = applicationState
        self.nameCtrl = None
        self.readerTypeCtrl = None
        self.objectTypeCtrl = None
        self.subObjectTypeCtrl = None
        self.stateChartCtrl = None
        self.bpTemplateCtrl = None
        self.tradingTemplateCtrl = None
        self.fileSelectionCtrl = None
        self.filePathCtrl = None
        self.moduleCtrl = None
        self.includeZeroCtrl = None
        self.universeCtrl = None
        self.openReconCtrl = None
        self.openModuleCtrl = None
        self.deleteCtrl = None
        self.clearCtrl = None
        self.saveCtrl = None
        self.saveNewCtrl = None
        self.module = None
        self.instances = None
        self.reconParam = None
        self.reconExtension = None
        self.lastObjectType = None
        self.objectTypes = None
        self.bypassOjectTypeChange = None
        self.openReconDlg = None
        self.identificationQueryCtrl = None
        self.edited = False
        self.tabs = list()
        self.ctrls = dict()

    def ObjectType(self):
        return self.objectTypeCtrl.GetData()

    def Tabs(self):
        return self.tabs

    def ReaderType(self):
        if self.readerTypeCtrl:
            return self.readerTypeCtrl.GetData()
        else:
            raise ValueError("Reader type control not initialized")

    def ClearEdited(self):
        for tab in self.Tabs():
            tab.Edited(False)
        self.Edited(False)

    def OnFileSelectionClicked(self, _args, _cd):
        fileFilter = (
            'All Files (*.*)|*.*',
            'CSV Files (*.csv)|*.csv',
            'Excel Files (*.xl*)|*.xl*',
            'XML Files (*.xml)|*.xml',
            'Text Files (*.txt)|*.txt',
            )
        path = 'c:\\'
        selection = acm.UX.Dialogs().BrowseForFiles(self.mainDlg.Shell(), '|'.join(fileFilter), path)
        selectedFile = selection[0] if selection else None
        if selectedFile:
            self.filePathCtrl.SetData(
                    ''.join((
                    str(selectedFile.SelectedDirectory()),
                    str(selectedFile.SelectedFile()))))

    def OnReaderTypeChanged(self, name, _cd):
        if self.ReaderType() == 'CSV':
            self.advancedCtrl.parserControl.SetData('')
            self.advancedCtrl.parserControl.Enabled(False)
        elif self.ReaderType() == 'Custom':
            self.advancedCtrl.parserControl.Enabled(True)

    def OnFilePathChanged(self, _arg, _cd):
        try:
            path = self.filePathCtrl.GetData()
            if path:
                with open(path, 'rb') as f:
                    columns = None
                    reader = FReconciliationReaderFactory.GetReconciliationDocumentReader(self.ReaderType(), self.advancedCtrl.parserControl.GetData())
                    columns = reader(f)
                    if not columns:
                        raise IOError("Reader yielded no result")

                    # check for external values hook
                    externalValuesHookName = self.advancedCtrl.externalValuesHookControl.GetData()
                    if externalValuesHookName:
                        externalValuesHook = FBusinessDataImportHook.FBusinessDataImportHook(externalValuesHookName)
                        columns = FBusinessDataImportHook.TransformDictionary(externalValuesHook, columns)

                    keys = [k for c in columns for k in c.keys()]
                    for tab in self.Tabs():
                        if tab.NameSpace() in ('Comparison', 'Attributes', 'DataTypes'):
                            tab.PopulateFileData(keys, _source='FilePathChange')
        except IOError as err:
            self.ThrowException(self.mainDlg, str(err))

        except Exception as ex:
            msg = "Unable to open file '%s' with reader for format '%s'. Exception: %s" % (path, self.ReaderType(), ex)
            logger.error(msg)
            acm.UX().Dialogs().MessageBox(
                    self.mainDlg.Shell(),
                    'Error',
                    msg,
                    'OK',
                    None,
                    None,
                    'Button1',
                    'None')

    def PopulateUniverseControl(self):
        if self.universeCtrl:
            self.universeCtrl.PopulateControls()

    def PopulateIdentificationQueryCtrl(self):
        if self.identificationQueryCtrl:
            self.identificationQueryCtrl.PopulateControls()

    def ConfirmObjectTypeChange(self):
        TEXT = ('Changing Object Type will clear existing mappings.\n'
                'Are you sure you want to proceed?')
        res = acm.UX().Dialogs().MessageBoxYesNo(
                self.mainDlg.Shell(),
                'Question',
                TEXT)
        if res not in ('Button1', ):
            self.objectTypeCtrl.SetData(
                    self.objectTypes.index(
                        self.lastObjectType or
                        self._DEFAULT_OBJECT_TYPE
                        )
                    )
            return False
        self.lastObjectType = self.objectTypeCtrl.GetData()
        return True

    def IsFXReconciliation(self):
        return not self.applicationState.IsUpload() and self.objectTypeCtrl.GetData() == 'Position'

    def ObjectTypeChanged(self, _args=None, _cd=None):
        if (self.bypassOjectTypeChange or
            self.ConfirmObjectTypeChange()):
            self.applicationState.ObjectType(self.objectTypeCtrl.GetData())
            subclass = self.applicationState.SubClass() # FTrade, FSettlement, FStock etc...
            group = self.applicationState.ColumnGroup() # dealsheet, tradesheet...

            # FX recon
            self.SetFXReconSettings()

            for tab in self.Tabs():
                namespace = tab.NameSpace()
                if namespace not in ('DataTypes', ):
                    tab.OnRemoveAllClicked()
                if namespace in ('Comparison', ):
                    tab.Values(ComparisonSettings.ColumnsDict(group or str()))
                    tab.PopulateTreeValuesCtrl(sortKey=self.ColumnSort)
                elif namespace in ('IdRules', 'Universe'):
                    tab.Keys(tab.Queries())
                    tab.PopulateKeysCtrl()
                elif namespace in ('Attributes', ):
                    tab.PopulateValuesCtrl(subclass)
            self.advancedCtrl.PopulateTradingSheetTemplates()
            self.PopulateUniverseControl()
            self.PopulateIdentificationQueryCtrl()
            self.bypassOjectTypeChange = False
            self._SetAvailableReaderTypes(self.objectTypeCtrl.GetData())
            self.ChangeSubTypeVisibility()

    def SubObjectTypeChanged(self, _args=None, _cd=None):
        self.applicationState.SubObjectType(self.subObjectTypeCtrl.GetData())
        subclass = str(self.applicationState.SubClass())
        group = self.applicationState.ColumnGroup() # dealsheet, tradesheet...

        comparisonTab = self.GetTab('Comparison')
        comparisonTab.OnRemoveAllClicked()
        comparisonTab.Values(ComparisonSettings.ColumnsDict(group or str()))
        comparisonTab.PopulateTreeValuesCtrl(sortKey=self.ColumnSort)

        IdRulesTab = self.GetTab('IdRules')
        IdRulesTab.OnRemoveAllClicked()
        IdRulesTab.Keys(IdRulesTab.Queries())
        IdRulesTab.PopulateKeysCtrl(sortKey=self.ColumnSort)

        attributesTab = self.GetTab('Attributes')
        attributesTab.OnRemoveAllClicked()
        attributesTab.PopulateValuesCtrl(subclass)

    def ChangeSubTypeVisibility(self):
        visible = True if 'Instrument' == self.applicationState.ObjectType() else False
        self.subObjectTypeCtrl.Visible(visible)

    def SetFXReconSettings(self):
        if self.fxReconCtrl:
            self.fxReconCtrl.Visible(bool(self.IsFXReconciliation()))

    def GetTab(self, tabName):
        resTab = None
        for tab in self.Tabs():
            if tab.NameSpace() == tabName:
                resTab = tab
        return resTab

    def ClearTabs(self, tabs):
        for tab in self.Tabs():
            if tab.NameSpace() in tabs:
                tab.OnRemoveAllClicked()

    def _SetAvailableReaderTypes(self, objectType):
        if self._READER_TYPE_MAP.has_key(objectType):
            readerTypes = self._READER_TYPE_MAP[objectType]
            self.AddItems(self.readerTypeCtrl, readerTypes)
            self.readerTypeCtrl.SetData(readerTypes[0])

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('None')
        b.  BeginVertBox('EtchedIn', '')
        b.    BeginHorzBox('None')
        b.      BeginVertBox('None')
        b.        BeginHorzBox('None')
        b.          AddInput(self._NAME_CTRL, self._NAME)
        b.          AddButton(self._OPEN_RECON_CTRL, self._OPEN, None, True)
        b.        EndBox()
        b.        BeginHorzBox('None')
        b.            AddOption(self._OBJECT_TYPE_CTRL, self._OBJECT_TYPE)
        b.            AddOption(self._SUB_TYPE_CTRL, self._SUB_TYPE)
        b.            AddCheckbox(self._FX_RECON_CTRL, self._FX_RECON_CTRL_NAME)
        b.            AddOption(self._READER_TYPE_CTRL, self._READER_TYPE)
        b.        EndBox()
        b.        BeginVertBox('None')
        b.          BeginHorzBox('None')
        b.            AddInput(self._MODULE_CTRL, self._MODULE)
        b.            AddButton(self._OPEN_MODULE_CTRL, self._OPEN, None, True)
        b.          EndBox()
        b.          AddComboBox(self._STATE_CHART_CTRL, self._STATE_CHART)
        b.          BeginHorzBox('None')
        b.            AddInput(self._FILE_PATH_CTRL, self._FILE_PATH)
        b.            AddButton(self._FILE_SELECTION_CTRL, self._OPEN, None, True)
        b.          EndBox()
        b.        EndBox()
        b.      EndBox()
        b.      BeginVertBox('None')
        b.        AddButton('saveNew', 'Save New')
        b.        AddButton('save', 'Save')
        b.        AddButton('clear', 'Clear')
        b.        AddButton('delete', 'Delete')
        b.        AddFill()
        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b

    def OnOpenReconClicked(self, _args, _cd):
        self.openReconDlg = OpenReconDlg(self, self.applicationState.IsUpload())
        builder = self.openReconDlg.CreateLayout()
        acm.UX().Dialogs().ShowCustomDialogModal(self.mainDlg.Shell(), builder, self.openReconDlg)

    def OnOpenModuleClicked(self, _args, _cd):
        openModuleDlg = OpenModuleDlg(self)
        builder = openModuleDlg.CreateLayout()
        acm.UX().Dialogs().ShowCustomDialogModal(self.mainDlg.Shell(), builder, openModuleDlg)

    def OnDeleteClicked(self, _args, _cd):
        self.HandleDelete()
        self.saveCtrl.Enabled(False)
        self.reconParam = None

    def OnClearClicked(self, _args, _cd):
        if self.DisregardChanges():
            self.ClearAllControlValues()
            self.SetDefaultValues()
            self.ClearEdited()

    def OnSaveClicked(self, _args, _cd):
        try:
            self.HandleApply()
            paramName = self.reconParam.Name()
            if str(paramName) not in (self.Name(), ):
                self.HandleDelete(bypass=True)
                self.reconExtension = self.Context().GetAllExtensions(
                        'FParameters',
                        self.Name())[0]
                self.reconParam = self.reconExtension.Value()
        except StandardError:
            pass

    def OnSaveNewClicked(self, _args, _cd):
        try:
            self.HandleApply()
            self.reconExtension = self.Context().GetAllExtensions(
                    'FParameters',
                    self.Name())[0]
            self.reconParam = self.reconExtension.Value()
        except StandardError:
            return None
        self.saveCtrl.Enabled(True)

    def InitControls(self, layout):
        self.deleteCtrl = layout.GetControl('delete')
        self.clearCtrl = layout.GetControl('clear')
        self.saveCtrl = layout.GetControl('save')
        self.saveCtrl.Enabled(False)
        self.saveNewCtrl = layout.GetControl('saveNew')
        self.nameCtrl = layout.GetControl(self._NAME_CTRL)
        self.readerTypeCtrl = self.InitControl(layout, self._READER_TYPE_CTRL, self._READER_TYPE)
        self.objectTypeCtrl = self.InitControl(layout, self._OBJECT_TYPE_CTRL, self._OBJECT_TYPE)
        self.subObjectTypeCtrl = self.InitControl(layout, self._SUB_TYPE_CTRL, self._SUB_TYPE)
        if not self.applicationState.IsUpload():
            self.fxReconCtrl = self.InitControl(layout, self._FX_RECON_CTRL, self._FX_RECON_CTRL_NAME)
            self.fxReconCtrl.Checked(False)
        else:
            self.fxReconCtrl = None
        self.moduleCtrl = layout.GetControl(self._MODULE_CTRL)
        self.moduleCtrl.Editable(False)
        self.stateChartCtrl = self.InitControl(layout, self._STATE_CHART_CTRL, self._STATE_CHART)
        #self.includeZeroCtrl = self.InitControl(layout, self._INCLUDE_ZERO_CTRL, self._INCLUDE_ZERO)
        self.universeCtrl = UniverseQueries(self.mainDlg, self.applicationState) if not self.applicationState.IsUpload() else None
        self.advancedCtrl = AdvancedPane(self.mainDlg, self.applicationState, self)
        self.fileSelectionCtrl = layout.GetControl(self._FILE_SELECTION_CTRL)
        self.filePathCtrl = layout.GetControl(self._FILE_PATH_CTRL)
        self.openReconCtrl = layout.GetControl(self._OPEN_RECON_CTRL)
        self.openModuleCtrl = layout.GetControl(self._OPEN_MODULE_CTRL)
        self.identificationQueryCtrl = IdRulesSettings(self.mainDlg, self.applicationState)
        # Some default settings
        self.filePathCtrl.Editable(False)
        self.ChangeSubTypeVisibility()

    def InitCallbacks(self):
        self.deleteCtrl.AddCallback('Activate', self.OnDeleteClicked, None)
        self.clearCtrl.AddCallback('Activate', self.OnClearClicked, None)
        self.saveCtrl.AddCallback('Activate', self.OnSaveClicked, None)
        self.saveNewCtrl.AddCallback('Activate', self.OnSaveNewClicked, None)
        self.fileSelectionCtrl.AddCallback('Activate', self.OnFileSelectionClicked, None)
        self.filePathCtrl.AddCallback('Changed', self.OnFilePathChanged, None)
        self.readerTypeCtrl.AddCallback('Changed', self.OnReaderTypeChanged, None)
        self.objectTypeCtrl.AddCallback('Changed', self.ObjectTypeChanged, None)
        self.subObjectTypeCtrl.AddCallback('Changed', self.SubObjectTypeChanged, None)
        self.openReconCtrl.AddCallback('Activate', self.OnOpenReconClicked, None)
        self.openModuleCtrl.AddCallback('Activate', self.OnOpenModuleClicked, None)
        self.nameCtrl.AddCallback('Changing', self.EnableSaveNewCtrl, None)

    def SetToolTips(self):
        self.nameCtrl.ToolTip("Name of the reconciliation solution")
        self.readerTypeCtrl.ToolTip("File format for input data")
        self.openReconCtrl.ToolTip("Open reconciliation solution")
        self.filePathCtrl.ToolTip("Imported File")
        self.fileSelectionCtrl.ToolTip("Select file to import")
        self.moduleCtrl.ToolTip("The module in which the solution will be saved")
        self.openModuleCtrl.ToolTip("Select module")
        self.stateChartCtrl.ToolTip("The state chart that will be used for the reconciliation")
        self.objectTypeCtrl.ToolTip("Type of object to reconcile")
        if not self.applicationState.IsUpload():
            self.fxReconCtrl.ToolTip('Toggle this checkbox to set up an FX reconciliation. This setting is only available in a ' \
                                     'position reconciliation setting; that is, when Object Type = Position. Observe that enabling ' \
                                     'FX position reconciliation implies that the Currency Pair grouper will be applied for calculating ' \
                                     'and comparing values.')

    def ClearAllControlValues(self):
        for tab in self.Tabs():
            tab.ClearControlValues()

    def SetAllControlValues(self, param):
        self.reconParam = param
        self.bypassOjectTypeChange = True
        module = self.ParamModule(param)
        self.SetControlValues(param, module)
        for tab in self.Tabs():
            tab.SetControlValues(param, module)

    def DefaultStateChartName(self):
        return 'Reconciliation' if not self.applicationState.IsUpload() else 'Data Upload'

    def DefaultStateChart(self):
        name = self.DefaultStateChartName()
        return self._GetOrCreateStateChart(name)

    def _EnsureStateChartIsUpToDate(self, name):
        if not self.applicationState.IsUpload():
            upgrader = FBusinessDataStateChartUpgrader.BusinessDataReconciliationStateChartUpgrader(name)
        else:
            upgrader = FBusinessDataStateChartUpgrader.BusinessDataUploadStateChartUpgrader(name)
        upgrader.EnsureUpgradedStateChart()

    def _GetOrCreateStateChart(self, name):
        try:
            if not acm.FStateChart[name]:
                newStateChart = None
                if not self.applicationState.IsUpload():
                    newStateChart = FExternalDataImportEngine.CreateStateChart(name)
                else:
                    import FBusinessDataUploadUtils
                    newStateChart = FBusinessDataUploadUtils.CreateStateChart(name)
                if newStateChart:
                    logger.info('State chart %s created', newStateChart.Name())
                    self.PopulateStateCharts()
                    self.stateChartCtrl.SetData(newStateChart)
                else:
                    logger.error('State chart %s not created', name)
            return acm.FStateChart[name]
        except StandardError as serr:
            errorStr = "Unable to create state chart '%s' : %s"%(name, serr)
            logger.warn(errorStr)
            raise ValueError(errorStr)

    def SetDefaultValues(self):
        for name, ctrl in self.ctrls.items():
            if name in (self._OBJECT_TYPE, ):
                ctrl.SetData(self._DEFAULT_OBJECT_TYPE)
                self.SetFXReconSettings()
            elif name in (self._READER_TYPE, ):
                self._SetAvailableReaderTypes(self._DEFAULT_OBJECT_TYPE)
            elif name in (self._STATE_CHART):
                ctrl.SetData(self.DefaultStateChart())
            elif ctrl.IsKindOf(acm.FUxCheckBox):
                ctrl.Checked(False)
            else:
                ctrl.SetData('')
        self.nameCtrl.SetData('')
        self.moduleCtrl.SetData(acm.GetDefaultContext().EditModule())
        self.filePathCtrl.SetData('')

    def RequiredEvents(self):
        try:
            if self.applicationState.IsUpload():
                import FUploadWorkflow
                cls = FUploadWorkflow.FUploadWorkflow
            else:
                import FReconciliationWorkflow
                cls = FReconciliationWorkflow.FReconciliationWorkflow
        except ImportError:
            return ['NOT_AN_EVENT']

        events = []
        for attr in dir(cls):
            event = getattr(cls, attr)
            if (not hasattr(event, '__call__') and
                not attr.startswith('__')):
                events.append(event)
        return events

    @staticmethod
    def IsValidChart(requiredEvents, events):
        for required in requiredEvents:
            if required not in events:
                return False
        return True

    def ValidStateCharts(self):
        charts = []
        requiredEvents = self.RequiredEvents()
        for chart in acm.FStateChart.Select('').SortByProperty('Name'):
            events = [
                event.Name()
                for state in chart.States()
                for event in state.TransitionsByEvent()
                ]
            if self.IsValidChart(requiredEvents, events):
                charts.append(chart)
        return charts

    def PopulateStateCharts(self):
        validCharts = self.ValidStateCharts()
        self.AddItems(self.stateChartCtrl, validCharts)

    def PopulateInsTypes(self):
        # todo - filter out unused instypes
        instypes = acm.FEnumeration['enum(InsType)'].Enumerators()
        instypes = instypes.Sort()
        self.AddItems(self.subObjectTypeCtrl, instypes)

    def ParamModule(self, param):
        try:
            return [
                mod
                for mod, params
                in self.instances.items()
                if str(param.Name()) in
                (str(p.Name()) for p in params)
                ][0]
        except IndexError:
            return None

    def SetData(self, ctrl, name, data):
        if ctrl.IsKindOf(acm.FUxCheckBox):
            data = True if str(data).lower() in ('true', ) else False
            ctrl.Checked(data)
        else:
            ctrl.SetData(data)

    def SetControlValues(self, param, module):
        for name, ctrl in self.ctrls.items():
            self.SetData(ctrl, name, param.GetString(name))
        self.nameCtrl.SetData(param.Name())
        self.moduleCtrl.SetData(module)
        self.ObjectTypeChanged()
        self.SubObjectTypeChanged()
        readerType = param.GetString(self._READER_TYPE)
        if not readerType:
            if param.GetString(AdvancedPane._PARSER_PARAM_NAME):
                readerType = 'Custom'
            else:
                readerType = 'CSV'
        self.readerTypeCtrl.SetData(readerType)

    def AddItems(self, ctrl, items):
        ctrl.Clear()
        for item in items:
            ctrl.AddItem(item)

    def PopulateControls(self):
        self.objectTypes = [e
                for e in sorted(list(acm.FEnumeration['enum(ReconciliationObjectType)'].Values()) + ['Order'])
                if (not str(e) in ('None')) and
                    ((self.applicationState.IsUpload() and str(e) in ['Trade', 'Instrument', 'Journal', 'Order']) or
                    (not self.applicationState.IsUpload() and str(e) in ['Trade', 'Position', 'Settlement', 'Order']))
                ]

        self.AddItems(self.objectTypeCtrl, self.objectTypes)
        self.PopulateStateCharts()
        self.PopulateInsTypes()

    def GetData(self, key):
        ctrl = self.ctrls[key]
        if ctrl.IsKindOf(acm.FUxCheckBox):
            return ctrl.Checked()
        return self.ctrls[key].GetData()

    def Name(self):
        return self.nameCtrl.GetData()

    @staticmethod
    def FormattedName(name, settings):
        return ''.join((name, settings.NameSpace())).strip()

    def HandleApplyGeneralParams(self, name, module):
        params = [
            'FObject:%s =' % self.Name(),
            '\n'.join(
                (key+'='+str(self.GetData(key))
                for key in self.ctrls)),
            'Compared Values Map=%s' % self.FormattedName(name, ComparisonSettings),
            'External Attribute Map=%s' % self.FormattedName(name, AttributesSettings),
            'External Data Type Map=%s' % self.FormattedName(name, DataTypesSettings),
            'Identification Rules=%s' % self.FormattedName(name, IdRulesSettings),
            'Upload=%s' % ('True' if self.applicationState.IsUpload() else 'False')
            ]
        for p in self.advancedCtrl.Parameters():
            params.append(p)

        if not self.applicationState.IsUpload():
            params.append('Universe Queries=%s' % ''.join(self.universeCtrl.Universe()))
        acm.GetDefaultContext().EditImport('FParameters', '\n'.join(params), True, module)

    def HandleApplyColumns(self, name, module):
        try:
            spec = FReconciliationSpecification.FReconciliationSpecification(name, self.applicationState.IsUpload(), onLoad = False)
            FReconciliationColumnCreator.CreateColumns(spec, module)
            logger.info('Successfully saved specification %s' % spec.Name())
        except StandardError as err:
            self.ThrowException(self.mainDlg, str(err))
            raise AssertionError()

    def Module(self):
        name = self.moduleCtrl.GetData()
        if name:
            return [
                m
                for m in acm.GetDefaultContext().Modules()
                if m.Name() in (name, )
                ][0]
        return acm.GetDefaultContext().EditModule()

    def CannotSave(self, name):
        TEXT = 'Can\'t save without a %s' % name.lower()
        self.ThrowException(self.mainDlg, TEXT)

    def HandleApplyStateChart(self):
        name = self.stateChartCtrl.GetData()
        self._GetOrCreateStateChart(name)
        self._EnsureStateChartIsUpToDate(name)

    def SaveThresholds(self):
        for tab in self.Tabs():
            if tab.NameSpace() in ('Comparison',):
                tab.OnSaveThresholds()

    def HandleApply(self):
        module = self.Module()
        name = self.Name()
        if not module:
            return self.CannotSave('Module')
        if not name:
            return self.CannotSave('Name')
        try:
            self.SaveThresholds()
            for tab in self.Tabs():
                tab.HandleApply(name, module)
            self.HandleApplyGeneralParams(name, module)
            self.HandleApplyStateChart()
            self.HandleApplyColumns(name, module)
            moduleName = module.Name()
            if module.IsBuiltIn():
                raise RuntimeError(
                        '%s module is built-in and can\'t be changed.' % moduleName
                        )
            module.Commit()
            self.SaveSucceeded(name, moduleName)
            self.ClearEdited()
        except RuntimeError as err:
            module.Undo()
            self.SaveFailed(name, err)
        except AssertionError as err:
            module.Undo()
            raise err
        except ValueError as err:
            module.Undo()
            self.SaveFailed(name, err)

    def ConfirmDelete(self, name):
        TEXT = 'Are you sure you want to delete %s?' % name
        res = acm.UX().Dialogs().MessageBoxYesNo(
                self.mainDlg.Shell(),
                'Question',
                TEXT)
        if res not in ('Button1', ):
            return False
        return True

    def DisregardChangesMsgBox(self):
        TEXT = ('Current settings have not been saved.\n'
               'Do you wish to disregard changes?')
        res = acm.UX().Dialogs().MessageBoxOKCancel(
                self.mainDlg.Shell(),
                'Question',
                TEXT)
        if res not in ('Button1', ):
            return None
        return True

    def DisregardChanges(self):
        try:
            for tab in self.Tabs():
                tab.PreHandleCancel()
            self.PreHandleCancel()
            return True
        except AssertionError:
            return self.DisregardChangesMsgBox()

    def HandleCancel(self):
        return self.DisregardChanges()

    def ReconParameters(self):
        return set(
            str(p.Name())
            for values in self.openReconDlg.ReconInstances().values()
            for p in values
            )

    def IsValidName(self):
        try:
            int(self.Name()[0])
            self.nameCtrl.Clear()
            TEXT = 'Reconciliation name can\'t start with a number.'
            self.OutputMsgBoxInformation(self.mainDlg, TEXT)
            self.saveNewCtrl.Enabled(False)
            return False
        except ValueError:
            return True

    def EnableSaveNewCtrl(self, _dlg, _cd):
        if self.Name() and self.IsValidName():
            if (not self.reconParam or
                self.reconParam and
                self.Name() not in self.ReconParameters()):
                self.saveNewCtrl.Enabled(True)
            else:
                self.saveNewCtrl.Enabled(False)
            self.Edited(True)
        else:
            self.saveNewCtrl.Enabled(False)

    def InitEditCallbacks(self):
        super(GeneralSettings, self).InitEditCallbacks()
        self.nameCtrl.AddCallback('Changed', self.EnableSaveNewCtrl, None)
        self.moduleCtrl.AddCallback('Changed', self.OnFileChanged, None)

    def ThresholdParams(self, dataTypeSettings):
        ThresholdParams = collections.namedtuple(
                        'ThresholdParams',
                        'dataTypeSettings, moduleCtrl, reconNameCtrl',
                        )
        ThresholdParams.dataTypeSettings = dataTypeSettings
        ThresholdParams.moduleCtrl = self.moduleCtrl
        ThresholdParams.reconNameCtrl = self.nameCtrl
        return ThresholdParams

    def AddAndCreateTabs(self):
        tabs = self.Tabs()

        # Add data types tab
        dataTypeSettings = DataTypesSettings(
                self.mainDlg,
                self.applicationState,
                self.moduleCtrl,
                self.nameCtrl
                )
        tabs.append(dataTypeSettings)

        # Add matching attributes tab
        tabs.append(AttributesSettings(self.mainDlg, self.applicationState))

        # Add identification query tab
        tabs.append(self.identificationQueryCtrl)

        # Add comparison values tab
        thresholdParams = self.ThresholdParams(dataTypeSettings)
        tabs.append(ComparisonSettings(self.mainDlg, self.applicationState, thresholdParams))

        # Add two-way recon tab
        if not self.applicationState.IsUpload():
            tabs.append(self.universeCtrl)

        # Add advanced tab
        tabs.append(self.advancedCtrl)
        for tab in tabs:
            tab.HandleCreate()

    def HandleCreate(self):
        builder = self.CreateLayout()
        generalLayout = self.mainDlg.AddTopLayout('Top', builder)
        self.InitControls(generalLayout)
        self.PopulateControls()
        self.SetDefaultValues()
        self.InitCallbacks()
        self.InitEditCallbacks()
        self.SetToolTips()
        self.AddAndCreateTabs()

    def RemoveExtension(self, module, param):
        module.RemoveExtension('FParameters', 'FObject', param.Name())

    def HandleDelete(self, bypass=False):
        if (bypass or
            self.reconParam and
            self.ConfirmDelete(self.reconParam.Name())):
            module = self.Module()
            for tab in self.Tabs():
                tab.RemoveExtension(module, self.reconParam)
            self.RemoveExtension(module, self.reconParam)
            try:
                module.Commit()
                if not bypass:
                    self.ClearAllControlValues()
                    self.SetDefaultValues()
                self.ClearEdited()
            except RuntimeError as err:
                self.DeleteFailed(module.Name(), err)


class OpenDlg(object, FUxCore.LayoutDialog):

    _INSTANCES_CTRL = 'Instances'

    def __init__(self, baseDlg, caption):
        self.baseDlg = baseDlg
        self.instancesCtrl = None
        self.caption = caption
        self.dlg = None

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.  BeginVertBox('None')
        b.    AddList(self._INSTANCES_CTRL, 15, 20, 40, 20)
        b.    BeginHorzBox('None')
        b.      AddFill()
        b.      AddButton('ok', 'Open')
        b.      AddButton('cancel', 'Close')
        b.    EndBox()
        b.  EndBox()
        return b

    def PopulateInstances(self):
        raise NotImplementedError

    def OnDoubleClicked(self, _args, _cd):
        self.dlg.CloseDialogOK()

    def InitControls(self, layout):
        self.instancesCtrl = layout.GetControl(self._INSTANCES_CTRL)

    def PopulateControls(self):
        self.PopulateInstances()

    def AddCallbacks(self):
        self.instancesCtrl.AddCallback('DefaultAction', self.OnDoubleClicked, None)

    def HandleCreate(self, dlg, layout):
        self.dlg = dlg
        dlg.Caption(self.caption)
        self.InitControls(layout)
        self.PopulateControls()
        self.AddCallbacks()

    def HandleApply(self):
        raise NotImplementedError


class OpenReconDlg(OpenDlg):

    def __init__(self, baseDlg, upload):
        self.baseDlg = None
        self.instancesCtrl = None
        self.dlg = None
        self.upload = upload
        super(OpenReconDlg, self).__init__(baseDlg, self.Caption())

    @staticmethod
    def Parameter(parameter):
        RECON_PARAMS = (
            'Compared Values Map',
            'External Attribute Map',
            'External Data Type Map',
            'Identification Rules',
            'Object Type'
            )
        for p in RECON_PARAMS:
            if not parameter.GetString(p):
                return False
        return (
            'Reconciliation'
            if (not parameter.GetString('Upload') or
                parameter.GetString('Upload') in ('False',))
            else 'Upload'
            )

    @classmethod
    def GetParameters(cls, mod, paramtype='Reconciliation'):
        return [
            p.Value()
            for p in mod.GetAllExtensions('FParameters')
            if cls.Parameter(p.Value()) == paramtype
            ]

    def ReconInstances(self):
        modules = acm.GetDefaultContext().Modules()
        instances = dict()
        paramtype = 'Upload' if self.upload else 'Reconciliation'
        for mod in modules:
            params = self.GetParameters(mod, paramtype)
            if params:
                instances[mod.Name()] = params
        return instances

    def Caption(self):
        caption = 'Data Upload' if self.upload else 'Reconciliation'
        return ' '.join(('Open', caption))

    def PopulateInstances(self):
        ICON = 'VtCenterPrice'
        self.instancesCtrl.Clear()
        self.baseDlg.instances = self.ReconInstances()
        root = self.instancesCtrl.GetRootItem()
        for recon in [p for params in self.baseDlg.instances.values() for p in params]:
            child = root.AddChild()
            child.Label(recon.Name())
            child.SetData(recon)
            child.Icon(ICON, ICON)

    def HandleApply(self):
        if self.baseDlg.DisregardChanges():
            self.baseDlg.ClearAllControlValues()
            paramName = self.instancesCtrl.GetSelectedItem().GetData().Name()
            if paramName:
                extension = self.baseDlg.Context().GetAllExtensions(
                            'FParameters',
                            paramName)[0]
                self.baseDlg.reconExtension = extension
                self.baseDlg.SetAllControlValues(extension.Value())
                self.baseDlg.saveCtrl.Enabled(True)
            else:
                self.baseDlg.SetDefaultValues()
                self.baseDlg.saveCtrl.Enabled(False)
                self.baseDlg.reconParam = None
                self.baseDlg.reconExtension = None
            self.baseDlg.lastObjectType = self.baseDlg.objectTypeCtrl.GetData()
            self.baseDlg.openReconCtrl.Enabled(True)
            self.baseDlg.ClearEdited()
            return True

    def HandleCreate(self, dlg, layout):
        self.baseDlg.openReconCtrl.Enabled(False)
        super(OpenReconDlg, self).HandleCreate(dlg, layout)

    def HandleCancel(self):
        self.baseDlg.openReconCtrl.Enabled(True)
        return True

class OpenModuleDlg(OpenDlg):

    CAPTION = 'Select Module'

    def __init__(self, baseDlg):
        self.baseDlg = None
        self.instancesCtrl = None
        self.dlg = None
        self.caption = None
        super(OpenModuleDlg, self).__init__(baseDlg, self.CAPTION)

    def Modules(self):
        return [module for module in acm.GetDefaultContext().Modules()]

    def PopulateInstances(self):
        self.instancesCtrl.Clear()
        root = self.instancesCtrl.GetRootItem()
        for mod in self.Modules():
            child = root.AddChild()
            child.Label(mod.Name())
            child.SetData(mod)
            child.Icon(mod.Icon(), mod.Icon())

    def HandleApply(self):
        try:
            module = self.instancesCtrl.GetSelectedItem().GetData()
            self.baseDlg.openModuleCtrl.Enabled(True)
            if module:
                self.baseDlg.moduleCtrl.SetData(module)
                self.baseDlg.module = module
                self.baseDlg.Edited(True)
            else:
                self.baseDlg.SetDefaultValues()
                self.baseDlg.ClearEdited()
            return True
        except AttributeError:
            return None

    def HandleCreate(self, dlg, layout):
        self.baseDlg.openModuleCtrl.Enabled(False)
        super(OpenModuleDlg, self).HandleCreate(dlg, layout)

    def HandleCancel(self):
        self.baseDlg.openModuleCtrl.Enabled(True)
        return True

class ApplicationState(object):

    _COLUMN_GRP_IDX  = 0
    _SUB_CLASS_IDX   = 1
    _SHEET_CLASS_IDX = 2

    # Todo - Base Caption here?

    def __init__(self, isUpload):
        self._objectType = 'Trade'
        self._subObjectType = None
        self._isUpload = isUpload

    def IsUpload(self, isUpload = None):
        if isUpload is None:
            return self._isUpload
        self._isUpload = isUpload

    def ObjectType(self, objectType = None):
        if objectType is None:
            return self._objectType
        self._objectType = objectType

    def SubObjectType(self, subObjectType = None):
        if subObjectType is None:
            return self._subObjectType
        self._subObjectType = subObjectType

    def ColumnGroup(self):
        return GROUP_MAP.get(self.ObjectType())[self._COLUMN_GRP_IDX]

    def InsTypeToFClass(self, insType):
        insTableType = acm.FEnumeration['enum(B92RecordType)'].Enumeration('Instrument')
        subType = acm.FEnumeration['enum(InsType)'].Enumeration(insType)
        return acm.Pom().MappedClass(insTableType, subType)

    def SubClass(self):
        #Todo - refactor!
        subclass = GROUP_MAP.get(self.ObjectType())[self._SUB_CLASS_IDX]
        if self.ObjectType() == 'Instrument':
            if self.SubObjectType():
                subclass = str(self.InsTypeToFClass(self.SubObjectType()).Name())
            else:
                subclass = 'FInstrument'
        return subclass

    def SheetClass(self):
        return GROUP_MAP.get(self.ObjectType())[self._SHEET_CLASS_IDX]

    @staticmethod
    def Filter(templates, sheetClass):
        templates = [
            t for t in templates
            if str(t.SheetClass()) == sheetClass
            ]
        templates.insert(0, '')
        return templates

    def Caption(self):
        caption = (
            'Data Upload'
            if self.IsUpload()
            else 'Reconciliation'
            )
        return ' '.join((caption, 'Manager'))

class ReconSettingsDialog(FUxCore.LayoutTabbedDialog):

    def __init__(self, upload=False):
        #Main dialog
        self.mainDlg = None
        self.mainPane = None
        self.applicationState = ApplicationState(upload)

    @staticmethod
    def InheritedColumn(inherits, extensions):
        extension = None
        while inherits:
            extension = [c for c in extensions if c.Name() in (inherits, )][0]
            inherits = extension.At('InheritsFrom')
        return extension

    def HandleCreate(self, dlg, _layout):
        self.mainDlg = dlg
        self.mainDlg.Caption(self.applicationState.Caption())
        #General Settings
        self.mainPane = GeneralSettings(dlg, self.applicationState)
        self.mainPane.HandleCreate()

    def HandleApply(self):
        self.mainPane.HandleApply()

    def HandleCancel(self):
        return self.mainPane.HandleCancel()


def CreateLayout():
    b = acm.FUxLayoutBuilder()
    #Bottom Layout
    b.BeginHorzBox('None')
    b.  AddFill()
    b.  AddButton('cancel', 'Close')
    b.EndBox()
    return b

def StartSettingsDlg(eii, upload=False):
    reload(sys.modules[__name__])
    shell = eii.Parameter('shell')
    builder = CreateLayout()
    dlg = ReconSettingsDialog(upload)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dlg)

def StartReconciliationDlg(eii):
    StartSettingsDlg(eii)

def StartDataUploadDlg(eii):
    StartSettingsDlg(eii, upload=True)