""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramColumns.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FTradeProgramColumns

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm
import FSheetUtils
from FIntegratedWorkbench import GetView, GetHandlerByName
from FParameterSettings import ParameterSettingsCreator
from FTradeProgramAction import Action
from FTradeProgramUtils import Logger
from FIntegratedWorkbenchMenuItem import IntegratedWorkbenchMenuItem
from FTradeProgramUtils import ColumnWorkflowMenuItem
import FTradeProgram


SETTINGS = ParameterSettingsCreator.FromRootParameter('TradeProgramSettings')

class ExtensionInvokationInfo(object):

    __slots__ = ['frame']

    def __init__(self, frame):
        self.frame = frame

    def ExtensionObject(self):
        return self.frame

def GetTradeProgramActionMenuItem(app, column):
    for action in Action.GetActions():
        try:
            menuItem = action(app)
            if menuItem.ActionName() == str(column.ColumnId()) and menuItem.EnabledFunction():
                return menuItem
        except AttributeError:
            continue

def InvokeTradeProgramActionMenuItem(app, column):
    try:
        menuItem = GetTradeProgramActionMenuItem(app, column)
        if menuItem:
            eii = ExtensionInvokationInfo(app)
            menuItem.Invoke(eii)
    except Exception as e:
        Logger().debug(e)

def OnInputChanged(_row, column, _calcVal, _input, _event):
    if SETTINGS.QuickMode():
        for app in acm.ApplicationList():
            try:
                view = GetView(app)
                if view.ClassName() == 'TradeProgramView':
                    InvokeTradeProgramActionMenuItem(app, column)
                    return
            except AttributeError:
                continue

def TargetColumnIsDenominatedValue(value):
    return value.IsKindOf(acm.FDenominatedValue)

def GetExtensionAttribute(targetColumnId, settingsName):
    if not targetColumnId:
        settings = ParameterSettingsCreator.FromRootParameter(settingsName)
        targetColumnId = settings.TargetColumnId() if hasattr(settings, 'TargetColumnId') else None
    creators = acm.GetColumnCreators(targetColumnId, acm.GetDefaultContext())
    return creators.At(0).Columns().First().ExtensionAttribute()
        
def IsActionColumn(frame, column):
    for action in Action.GetActions():
        tradeProgramMenuAction = action(frame)
        try:
            hasActionName = str(column.ColumnName()) == tradeProgramMenuAction.ActionName()
            if hasActionName:
                return hasActionName
        except Exception:
            continue
        
def ClearInputColumns(sheet, frame):
    rowIter = sheet.RowTreeIterator(True)
    while rowIter.NextUsingDepthFirst():
        columnIter = sheet.GridColumnIterator().First()
        while columnIter:
            column = columnIter.GridColumn()
            if IsActionColumn(frame, column):
                try:
                    cell = sheet.GetCell(rowIter, columnIter)
                    evaluator = cell.Evaluator()
                    if evaluator and evaluator.HasSimulatedInput():
                        evaluator.RemoveSimulation()
                except AttributeError as e:
                    Logger().error(e, exc_info=True)
            columnIter = columnIter.Next()

def CreateInputColumnCP(eii):
    return CreateInputColumnMenuItem(eii, 'Change Percent')

def CreateInputColumnCV(eii):
    return CreateInputColumnMenuItem(eii, 'Change Value')

def CreateInputColumnTP(eii):
    return CreateTargetPercentColumnMenuItem(eii, 'Target Percent')

def CreateInputColumnTV(eii):
    return CreateInputColumnMenuItem(eii, 'Target Value')

class CreateInputColumnMenuItem(IntegratedWorkbenchMenuItem):

    def __init__(self, extObj, inputColumnId):
        super(CreateInputColumnMenuItem, self).__init__(extObj, view='TradeProgramView')
        self._sheet = extObj.ActiveSheet()
        self._inputColumnId = inputColumnId
        try:
            cell = self._sheet.Selection().SelectedCell()
            self._columnId = cell.Column().ColumnId().Text()
        except AttributeError:
            self._columnId = None

    def ApplicableOnNoWorkbench(self):
        return False

    def EnabledFunction(self):
        return bool(self._columnId)
    
    def ColumnParams(self):
        return {acm.FSymbol('TargetColumnParameters'): self._columnId}
    
    def NewColumn(self):
        columnParams = self.ColumnParams()
        columnConfig = acm.Sheet().Column().CreatorConfigurationFromColumnParameterDefinitionNamesAndValues(columnParams)
        
        columnCreator = FSheetUtils.ColumnCreator(self._inputColumnId)
        return columnCreator.Template().CreateCreator(columnConfig, None)
    
    def InvokeAsynch(self, _eii):
        columnCreator = self.NewColumn()
        targetColumnCretor = FSheetUtils.ColumnCreatorInSheet(self._sheet, self._columnId)
        self._sheet.ColumnCreators().InsertAfter(targetColumnCretor, columnCreator)

    def Invoke(self, eii):
        self._frame.Shell().CallAsynch(self.InvokeAsynch, eii)

class CreateTargetPercentColumnMenuItem(CreateInputColumnMenuItem):
    
    def ColumnParams(self):
        columnParams = super(CreateTargetPercentColumnMenuItem, self).ColumnParams()
        columnParams[acm.FSymbol('TargetPercentRelativeTo')] = 'Top'
        return columnParams

def TradeProgramStateChart():
    #Passing query to ensure reevaluation in ADFL
    cls = FTradeProgram.TradeProgramWorkflowClass()
    return acm.FStateChart[cls.StateChart()]

def showApproveBreachesButton(eii):
    return True

def onApproveBreachesStartButton(eii):
    button = eii.Parameter('ClickedButton')
    if button:
        order = button.RowObject()
        event = eii.MenuExtension().GetString('HandleEvent')
        if order and order.IsKindOf(acm.FOrderProgram):
            query = "optionalId={0}".format(order.OrderProgramId())
            dealPackage = acm.FDealPackage.Select01(query, None)
            tradeProgramClass = FTradeProgram.TradeProgramWorkflowClass()
            stateChart = acm.FStateChart[tradeProgramClass.StateChart()]
            if dealPackage and stateChart:
                try:
                    businessProcess = acm.BusinessProcess.FindBySubjectAndStateChart(dealPackage, stateChart)[0]
                    workflow = ColumnWorkflowMenuItem(eii.ExtensionObject(), tradeProgramClass, event, businessProcess)
                    workflow.Invoke(eii.ExtensionObject())
                except (TypeError, IndexError):
                    pass
