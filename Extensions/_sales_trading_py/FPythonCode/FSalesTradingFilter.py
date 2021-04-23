""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FSalesTradingFilter.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSalesTradingFilter

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import FUxCore
import FFilter
from collections import namedtuple
import ast
import FSheetUtils

def ActiveSheet(eii):
    extObj = eii.ExtensionObject()
    if extObj.IsKindOf(acm.FUiTrdMgrFrame):
        return extObj.ActiveSheet()

def ColumnIds(eii):
    try:
        creators = ActiveSheet(eii).ColumnCreators()
        return [creators.At(i).ColumnId() for i in range(creators.Size())]
    except AttributeError:
        return []

def CreateApplicationInstance():
    return SalesTradingFilterApplication()

def StartFilterApplicationModal(content):
    acm.StartApplication('Sales Trading Filter', content)

class FilterApplicationMenuItem(FUxCore.MenuItem):
    def __init__(self, application):
        self._application = application

    def Application(self):
        return self._application

    def Invoke(self, cd):
        button = str(cd.Definition().GetName())
        if button == 'SaveAs':
            self.Application().OnSaveNew()
        elif button == 'Open':
            self.Application().OnFilterOpen()
        elif button == 'Remove':
            self.Application().OnRemoveRows()
        else:
            return True

    def Applicable(self):
        return True

    def Enabled(self):
        return True

    def Checked(self):
        return False

class ApplyMenuItem(FilterApplicationMenuItem):

    def Enabled(self):
        return self.Application().OnApplyEnabled()

    def Invoke(self, cd):
        return self.Application().OnApply()

class SaveMenuItem(FilterApplicationMenuItem):

    def Enabled(self):
        return self.Application().DeleteAndSaveEnabled()

    def Invoke(self, cd):
        return self.Application().OnSave()

class DeleteMenuItem(FilterApplicationMenuItem):

    def Enabled(self):
        return self.Application().DeleteAndSaveEnabled()

    def Invoke(self, cd):
        return self.Application().OnFilterDelete()

class SalesTradingFilterApplication(FUxCore.LayoutApplication):
    CONTROLS = ['select', 'attr', 'comparisonOp', 'minValue', 'maxValue', 'logicalOp']
    DEFAULT_COMPARATOR = FFilter.FBetweenOperator().OperatorSymbol()
    VISIBLE_ROWS = 1
    MAX_ROWS = 20

    def __init__(self):
        FUxCore.LayoutApplication.__init__(self)
        self._visibleRowsIdx = self.VISIBLE_ROWS-1
        self._columnIds = acm.FArray()
        self._columnsFromSheet = acm.FArray()
        self._inputValues = None
        self._filterName = None
        self._menuItem = None

    def SetCaption(self, filterName):
        self.SetContentCaption(filterName)

    def HandleRegisterCommands(self, builder):
        commands =[
        ['Open', 'View', '', '', '', '', self.CreateCommandCB, False],
        ['Save', 'View', '', '', '', '', self.CreateSaveCommandCB, False],
        ['SaveAs', 'View', '', '', '', '', self.CreateCommandCB, False],
        ['Apply', 'View', '', '', '', '', self.CreateApplyCommandCB, False],
        ['Delete', 'View', '', '', '', '', self.CreateDeleteCommandCB, False],
        ['Remove', 'View', '', '', '', '', self.CreateCommandCB, False]
        ]
        fileCommands = acm.FSet()
        fileCommands.Add('FileOpen')
        fileCommands.Add('FileSave')
        fileCommands.Add('FileSaveAs')
        builder.RegisterCommands(FUxCore.ConvertCommands(commands), fileCommands)

    def CreateCommandCB(self):
        return FilterApplicationMenuItem(self)

    def CreateApplyCommandCB(self):
        return ApplyMenuItem(self)

    def CreateSaveCommandCB(self):
        return SaveMenuItem(self)

    def CreateDeleteCommandCB(self):
        return DeleteMenuItem(self)

    def HandleSetContents(self, contents):
        if contents:
            self._inputValues = contents[0]
            self._columnIds = self.StoredColumns() or contents[1]
            self._columnsFromSheet = contents[1]
            self._menuItem = contents[2]
        else:
            self._columnIds = self.StoredColumns()

    def GetColumns(self, sheetColumns = None):
        pyColumns = self.StoredColumns() or self._columnsFromSheet
        acmColumns = acm.FArray()
        acmColumns.AddAll(pyColumns)
        return acmColumns

    def StoredColumns(self):
        columns = FSheetUtils.ColumnIds('SalesTradingFilterDefaultColumns2', 'FPortfolioSheet')
        if columns:
            return [acm.FSymbol(column) for column in columns]

    def OnApply(self, *args):
        try:
            output, columnsNotInSheet = self.FilterCtrlsData()
            if columnsNotInSheet:
                dialogOutput = acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Question', 'The following columns are not'
                + 'in the sheet and will not be used in the filtering: ' + str(columnsNotInSheet) + '. Continue?')
                if dialogOutput == 'Button1':
                    self.IsValidOutput(output)
                    self._menuItem.DoSendEvent(output)
            elif self._menuItem is not None:
                self.IsValidOutput(output)
                self._menuItem.DoSendEvent(output)
        except ValueError as e:
            self.ShowErrorMessageBox(e)

    def OnApplyEnabled(self):
        if self._menuItem is not None:
            return True
        else:
            return False

    def DeleteAndSaveEnabled(self):
        if self._filterName is not None:
            return True
        else:
            return False

    def HandleStandardFileCommandInvoke(self, commandName):
        if commandName == 'FileOpen':
            self.OnFilterOpen()
        elif commandName == 'FileSaveAs':
            self.OnSaveNew()
        elif commandName == 'FileSave':
            self.OnSave()
        elif commandName == 'FileDelete':
            self.OnFilterDelete()

    def HandleStandardFileCommandEnabled(self, commandName):
        if (commandName == 'FileSave' or commandName == 'FileDelete') and self._filterName is None:
            return False
        else:
            return True

    def OnFilterOpen(self):
        selectedObject = acm.UX().Dialogs().SelectObject(self.Shell(), 'Select Filter', 'FColumnFilter', self.GetFColumnFilter(), None)
        if selectedObject != None:
            self.PopulateDialogWithFilter(selectedObject)
            self._filterName = selectedObject.Name()
            self.SetCaption(self._filterName)

    def PopulateDialogWithFilter(self, columnFilter):
        self.OnClearRows()
        dlgOutput = ast.literal_eval(columnFilter.Text())
        self.AddExtraColumns(dlgOutput)
        for idx, row in enumerate(dlgOutput):
            self.ShowCtrlsRow(idx)
            for index, field in enumerate(row):
                ctrl = self.GetCtrl(self.CONTROLS[index], idx)
                ctrl.SetData(acm.FSymbol(str(field)))
            self.OnComparisonOpChanged(idx)
        self._visibleRowsIdx = len(dlgOutput) - 1

    def AddExtraColumns(self, dlgOutput):
        filterColumns = [acm.FSymbol(str(row[1])) for row in dlgOutput]
        self._columnIds = self.GetColumns().Union(filterColumns)

    def GetFColumnFilter(self, *args):
        FColumnFilters = acm.FColumnFilter.Select('').SortByProperty('Name')
        return FColumnFilters

    def OnSave(self):
        try:
            dlgOutput = self.GetCtrlsData()
            self.IsValidOutput(dlgOutput)
            FFilter.FFilter.SaveFilter(dlgOutput, self._filterName)
        except ValueError as e:
            self.ShowErrorMessageBox(e)

    def callbackSaveNew(self, *args):
        if self.doFilterExist(args[1]):
            output = acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Question', '\'' + args[1] + '\'' + ' already exist. Do you want to replace it?')
            if (output == 'Button1'):
                self.saveFilter(args[1])
                return True
            else:
                return False
        else:
            self.saveFilter(args[1])
            return True

    def doFilterExist(self, filterName):
        return acm.FColumnFilter[filterName]

    def OnSaveNew(self):
        acm.UX().Dialogs().SaveObjectAs(self.Shell(), 'Save Filter', 'FColumnFilter', self.GetFColumnFilter(), None, self.callbackSaveNew, None)

    def saveFilter(self, name):
        try:
            dlgOutput = self.GetCtrlsData()
            self.IsValidOutput(dlgOutput)
            FFilter.FFilter.SaveFilter(dlgOutput, name)
            self._filterName = name
            self.SetCaption(name)
        except ValueError as e:
            self.ShowErrorMessageBox(e)

    def OnFilterDelete(self):
        dialogOutput = acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Question', 'Do you want to delete \'' + self._filterName + '\' ?')
        if dialogOutput == 'Button1':
            FFilter.FFilter.DeleteFilter(self._filterName)
            self._filterName = None
            self.SetCaption('')
            self.OnClearRows()

    def HandleCreate( self, creationInfo ):
        pane = creationInfo.AddPane(self.CreateLayout(), "filterPane")
        self.InitInputCtrls(pane)
        self.InitInputCtrlValues()
        self.InitFocus()

    def NumberOfVisibleRows(self):
        return self._visibleRowsIdx + 1

    def OnAddRow(self, *_args):
        if self.RowsLeftToAdd():
            self._visibleRowsIdx += 1
            self.ShowCtrlsRow(self._visibleRowsIdx)
            return True
        return False

    def OnRemoveRow(self, *_args):
        if self.RowsLeftToRemove():
            self.HideCtrlsRow(self._visibleRowsIdx)
            self._visibleRowsIdx -= 1
            self.ClearLastLogicalOperatorCtrl()
            return True
        return False

    def RemoveRow(self, removeIdx):
        if self._visibleRowsIdx > 0:
            for idx in range(removeIdx, self._visibleRowsIdx):
                self.CopyRow(fromIdx = idx + 1, toIdx = idx)
            self.HideCtrlsRow(self._visibleRowsIdx)
            self._visibleRowsIdx -= 1
        else:
            self.OnClearRows()

    def CopyRow(self, fromIdx, toIdx):
        for name in self.CONTROLS:
            ctrlFrom = self.GetCtrl(name, fromIdx)
            ctrlTo = self.GetCtrl(name, toIdx)
            ctrlTo.SetData(ctrlFrom.GetData())
            ctrlTo.Visible(ctrlFrom.Visible())
            self.OnComparisonOpChanged(toIdx)

    def OnRemoveRows(self, *_args):
        idx = 0
        while idx < self._visibleRowsIdx:
            if self.GetCtrl('select', idx).Checked():
                self.RemoveRow(idx)
            else:
                idx += 1
        if self.GetCtrl('select', self._visibleRowsIdx).Checked():
            self.RemoveRow(self._visibleRowsIdx)
        self.ClearLastLogicalOperatorCtrl()

    def OnClearRows(self, *_args):
        try:
            while self.RowsLeftToRemove():
                self.OnRemoveRow()
            self.HideCtrlsRow(self._visibleRowsIdx)
            self._visibleRowsIdx -= 1
            self.OnAddRow()
            return True
        except StandardError:
            return False

    def OnLogicalOpChanged(self, *args):
        name, idx  = 'logicalOp', args[0]
        try:
            if (self.GetCtrl(name, idx).GetData() and
                not self.GetCtrl(name, idx+1).Visible()):
                self.OnAddRow()
        except AttributeError:
            pass

    def OnComparisonOpChanged(self, *args):
        name, idx  = 'comparisonOp', args[0]
        ctrlData = self.GetControlData(self.GetCtrl(name, idx))
        minValCtrl = self.GetCtrl('minValue', idx)
        maxValCtrl = self.GetCtrl('maxValue', idx)
        if ctrlData == 'BETWEEN':
            minValCtrl.Enabled(True)
            maxValCtrl.Enabled(True)
        elif ctrlData in ('>', '>=', '=', '!=', 'TOP', 'BOTTOM'):
            minValCtrl.Enabled(True)
            maxValCtrl.Enabled(False)
            maxValCtrl.Clear()
        elif str(ctrlData) in ('<', '<='):
            minValCtrl.Enabled(False)
            minValCtrl.Clear()
            maxValCtrl.Enabled(True)

    def GetCtrlsData(self):
        Comparator = namedtuple('Comparator', self.CONTROLS)
        return [Comparator(*(self.GetCtrl(name, i).GetData()
                for name in self.CONTROLS))
                for i in range(self.NumberOfVisibleRows())]

    def FilterCtrlsData(self):
        Comparator = namedtuple('Comparator', self.CONTROLS[1:])
        comparators = []
        columnsNotInSheet = []
        for index in range(self.NumberOfVisibleRows()):
            if (self.GetCtrl('select', index).GetData()):
                if not self.GetCtrl('attr', index).GetData() or self.GetCtrl('attr', index).GetData() in self._columnsFromSheet:
                    comparatorArguments = []
                    for name in self.CONTROLS[1:]:
                        comparatorArguments.append(self.GetCtrl(name, index).GetData())
                    comparators.append(Comparator(*comparatorArguments))
                else:
                    columnsNotInSheet.append(self.GetCtrl('attr', index).GetData())
        return comparators, columnsNotInSheet

    @staticmethod
    def GetControlData(ctrl):
        try:
            return str(ctrl.GetData())
        except StandardError:
            return ctrl.GetData()

    def HideCtrlsRow(self, idx):
        for name in self.CONTROLS:
            self.HideCtrl(name, idx)

    def HideCtrl(self, name, idx):
        ctrl = self.GetCtrl(name, idx)
        ctrl.Visible(False)
        ctrl.Clear()

    def ShowCtrlsRow(self, idx):
        for name in self.CONTROLS:
            self.ShowCtrl(name, idx)

    def ShowCtrl(self, name, idx):
        ctrl = self.GetCtrl(name, idx)
        ctrl.Visible(True)
        self.Populate(name, ctrl)
        self.SetDefaultValues(name, idx, ctrl)

    def SetDefaultValues(self, name, idx, ctrl):
        if name.startswith('comparisonOp'):
            ctrl.SetData(self.DEFAULT_COMPARATOR)
            self.OnComparisonOpChanged(idx)
        elif name.startswith('select'):
            ctrl.Checked(True)

    def RowsLeftToAdd(self):
        return self._visibleRowsIdx < self.MAX_ROWS - 1

    def RowsLeftToRemove(self):
        return self._visibleRowsIdx > 0

    def ClearLastLogicalOperatorCtrl(self):
        self.GetCtrl('logicalOp', self._visibleRowsIdx).SetData(acm.FSymbol(''))

    def UpdateCtlValues(self, idx, comparator):
        for name in self.CONTROLS:
            if name is not 'select':
                ctrl = self.GetCtrl(name, idx)
                if (name in ('minValue', 'maxValue') and
                    not ctrl.Enabled()):
                    continue
                ctrl.SetData(getattr(comparator, name) or '')
                if name == 'comparisonOp':
                    self.OnComparisonOpChanged(self._visibleRowsIdx)

    def InitColumnCtrlValues(self):
        if self._inputValues:
            try:
                enumerateInputValues = enumerate(self._inputValues)
                idx, comparator = next(enumerateInputValues)
                self.UpdateCtlValues(idx, comparator)
                for idx, comparator in enumerateInputValues:
                    if self.OnAddRow():
                        self.UpdateCtlValues(idx, comparator)
                self.ClearLastLogicalOperatorCtrl()
            except StopIteration:
                pass

    def InitInputCtrlValues(self):
        self.InitColumnCtrlValues()

    def InitFocus(self):
        if self.GetCtrl('attr', 0).GetData():
            self.GetCtrl('minValue', 0).SetFocus()

    def RegisterCtrl(self, name, idx, ctrl):
        setattr(self, self.CtrlName(name, idx), ctrl)

    def GetCtrl(self, name, idx):
        return getattr(self, self.CtrlName(name, idx))

    def IsRowHidden(self, idx):
        return idx > self._visibleRowsIdx

    def Populate(self, name, ctrl):
        if name.startswith('attr'):
            ctrl.Populate(self._columnIds)
        elif name.startswith('comparisonOp'):
            ctrl.Populate(self.ComparisonOperators())
        elif name.startswith('logicalOp'):
            ctrl.Populate(self.LogOperators())

    def RegisterCtrls(self, layout):
        for idx in range(self.MAX_ROWS):
            for name in self.CONTROLS:
                ctrl = layout.GetControl(self.CtrlName(name, idx))
                self.RegisterCtrl(name, idx, CtrlProxy(ctrl))

    @staticmethod
    def ComparisonOperators():
        return (FFilter.FComparisonOperator.OperatorSymbols() +
            FFilter.FTopOperator.OperatorSymbols() +
            FFilter.FBetweenOperator.OperatorSymbols())

    @staticmethod
    def LogOperators():
        return ([acm.FSymbol('')] +
            FFilter.FLogicalOperator.OperatorSymbols())

    def InitInputCtrls(self, layout):
        self.RegisterCtrls(layout)
        self.AddOperatorsCallback()
        self.InitCrlsVisibility()

    def AddOperatorsCallback(self):
        for idx in range(self.MAX_ROWS):
            self.AddOperatorCallback(idx)

    def AddOperatorCallback(self, idx):
        self.GetCtrl('logicalOp', idx).AddCallback('Changed', self.OnLogicalOpChanged, idx)
        self.GetCtrl('comparisonOp', idx).AddCallback('Changed', self.OnComparisonOpChanged, idx)

    def InitCrlsVisibility(self):
        for idx in range(self.MAX_ROWS):
            self.HideCtrlsRow(idx)
            if not self.IsRowHidden(idx):
                self.ShowCtrlsRow(idx)


    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('None')
        b. BeginVertBox('None')
        self.AddLabels(b)
        for i in range(self.MAX_ROWS):
            self.AddInputCtrls(b, i)
        b. EndBox()
        b. BeginVertBox('Invisible')
        b. EndBox()
        b.EndBox()
        return b

    def ShowErrorMessageBox(self, err):
        acm.UX.Dialogs().MessageBox(self.Shell(), 'Error', str(err), 'Ok', '', '', 'Button1', 'Button2')

    @classmethod
    def AddLabels(cls, builder):
        builder.BeginHorzBox('None')
        builder.AddLabel('select', '')
        builder.AddLabel('columnId', 'Field')
        builder.AddSpace(120)
        builder.AddLabel('cmpOp', 'Condition')
        builder.AddSpace(70)
        builder.AddLabel('minVal', 'Min')
        builder.AddSpace(78)
        builder.AddLabel('maxVal', 'Max')
        builder.AddSpace(45)
        builder.AddLabel('logOp', 'Operator')
        builder.EndBox()

    @classmethod
    def AddInputCtrls(cls, builder, idx):
        builder.BeginHorzBox('None')

        builder. AddCheckbox(cls.CtrlName(cls.CONTROLS[0], idx), '')
        builder. AddOption(cls.CtrlName(cls.CONTROLS[1], idx), '', 30, None)
        builder. AddOption(cls.CtrlName(cls.CONTROLS[2], idx), '', 18, None)
        builder. AddInput(cls.CtrlName(cls.CONTROLS[3], idx), '', None, None)
        builder. AddInput(cls.CtrlName(cls.CONTROLS[4], idx), '', None, None)
        builder. AddOption(cls.CtrlName(cls.CONTROLS[5], idx), '', 8, None)
        builder.EndBox()

    @classmethod
    def IsValidOutput(cls, output):
        cls.ValidateOutputFormat(output)
        cls.ValidateCtrlsData(output)
        cls.ValidateLogicalOperatorCtrls(output)
        cls.ValidateComparisonValues(output)

    @classmethod
    def ValidateCtrlsData(cls, output):
        for i, comparator in enumerate(output):
            what = None
            if comparator.attr is None:
                what = 'Field'
            elif comparator.comparisonOp is None:
                what = 'Condition'
            if what is not None:
                msg = '{0} missing on row {1}.'.format(what, i+1)
                raise ValueError(msg)

    @staticmethod
    def ValidateComparisonValues(output):
        for i, comparator in enumerate(output):
            if str(comparator.comparisonOp) in ('>', '>=', 'BETWEEN'):
                try:
                    float(comparator.minValue or 0)
                except (ValueError, TypeError):
                    msg = ('Invalid min value on row {0}. Expected a number '
                        'and got "{1}".'.format(i+1, comparator.minValue))
                    raise ValueError(msg)
            if str(comparator.comparisonOp) in ('<', '<=', 'BETWEEN'):
                try:
                    float(comparator.maxValue or 0)
                except (ValueError, TypeError):
                    msg = ('Invalid max value on row {0}. Expected a number '
                        'and got "{1}".'.format(i+1, comparator.maxValue))
                    raise ValueError(msg)
            if str(comparator.comparisonOp) in ('TOP', 'BOTTOM'):
                try:
                    int(comparator.minValue or 0)
                except (ValueError, TypeError):
                    msg = ('Invalid min value on row {0}. Expected an integer '
                        'and got "{1}".'.format(i+1, comparator.minValue))
                    raise ValueError(msg)

    @staticmethod
    def ValidateOutputFormat(output):
        if not output:
            msg = 'Failed to create filter. Reason: No input.'
            raise ValueError(msg)

    @staticmethod
    def ValidateLogicalOperatorCtrls(output):
        for i, row in enumerate(output):
            try:
                if output[i+1] and not row[-1]:
                    msg = 'Logical operator missing on row {0}.'.format(i+1)
                    raise ValueError(msg)
            except IndexError:
                pass

    @staticmethod
    def CtrlName(name, idx):
        return ''.join((name, str(idx)))

class CtrlProxy(object):
    def __init__(self, ctrl):
        self._ctrl = ctrl

    def GetData(self):
        if str(self._ctrl.ClassName()) == 'FUxCheckBox':
            return self._ctrl.Checked()
        else:
            return self._ctrl.GetData()

    def SetData(self, data):
        if str(self._ctrl.ClassName()) == 'FUxCheckBox':
            self._ctrl.Checked(str(data) == 'True')
        else:
            self._ctrl.SetData(data)

    def __getattr__(self, attr):
        return getattr(self._ctrl, attr)
