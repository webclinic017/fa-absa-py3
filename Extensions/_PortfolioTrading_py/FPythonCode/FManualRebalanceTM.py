""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FManualRebalanceTM.py"
"""--------------------------------------------------------------------------
MODULE
    FManualRebalancingTM.py

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    FManualRebalancingTM.py represents the interface between the TradingManager
    and the various Manual Rebalancing actions.
-----------------------------------------------------------------------------"""

import FSheetUtils
from FParameterSettings import ParameterSettingsCreator
from FTradeProgramAction import Action, RebalancingAction
from FTradeProgramTM import FTradeProgramTM
from FManualRebalance import FManualRebalance
from FTradeProgramMenuItem import TradeProgramActionMenuItem

@Action
def ChangePercent(eii):
    return ChangePercentMenuItem(eii)

@Action
def ChangeValue(eii):
    return ChangeValueMenuItem(eii)

@Action
def TargetPercent(eii):
    return TargetPercentMenuItem(eii)

@Action
def TargetValue(eii):
    return TargetValueMenuItem(eii)


class RebalancingStrategiesMenuItem(TradeProgramActionMenuItem):

    def __init__(self, extObj, actionName):
        self._actionName = actionName
        super(RebalancingStrategiesMenuItem, self).__init__(extObj)

    @staticmethod
    def HasSelection(sheet):
        return bool(sheet.Selection().SelectedRowObjects().Size())
    
    def TargetColumnId(self):
        colParams = FSheetUtils.ColumnParameters(self.InputColumn())
        return colParams.At('TargetColumnParameters') if colParams else None
    
    def InputColumn(self):
        return FSheetUtils.GetColumnIfOneSelected(self.Sheet())
    
    def ActionName(self):
        return self._actionName
    
    def IsActionColumn(self, sheet):
        columns = set(cell.Column() for cell in
                      sheet.Selection().SelectedCells())
        if len(columns) is 1:
            column = columns.pop()
            return str(column.ColumnName()) == self.ActionName()
        return False

    def EnabledFunction(self):
        sheet = self._frame.ActiveSheet()
        if sheet:
            return bool(self.HasSelection(sheet) and self.IsActionColumn(sheet))
        return True
    
    def Action(self):
        return RebalancingAction(self.ActionName(), self.TargetColumnId())

class ChangePercentMenuItem(RebalancingStrategiesMenuItem):

    def __init__(self, extObj):
        super(ChangePercentMenuItem, self).__init__(extObj, 'Change Percent')

    def InvokeAsynch(self, eii):
        rebalance = FManualRebalanceTM(
            eii,
            action=self.Action(),
            targetColumnId=self.TargetColumnId(),
            inputColumn=self.InputColumn(),
            relativeTo='Self',
            name=self._actionName)
        rebalance.Execute()

class ChangeValueMenuItem(RebalancingStrategiesMenuItem):

    def __init__(self, extObj):
        super(ChangeValueMenuItem, self).__init__(extObj, 'Change Value')

    def InvokeAsynch(self, eii):
        rebalance = FManualRebalanceTM(
            eii,
            action=self.Action(),
            targetColumnId=self.TargetColumnId(),
            inputColumn=self.InputColumn(),
            name=self._actionName)
        rebalance.Execute()


class TargetPercentMenuItem(RebalancingStrategiesMenuItem):

    def __init__(self, extObj):
        super(TargetPercentMenuItem, self).__init__(extObj, 'Target Percent')
    
    def RelativeTo(self):
        colParams = FSheetUtils.ColumnParameters(self.InputColumn())
        relativeTo = colParams.At('TargetPercentRelativeTo')
        assert relativeTo, '"Target Percent Relative To" must be set as a colum parameter.'
        return relativeTo
    
    def InvokeAsynch(self, eii):
        rebalance = FManualRebalanceTM(
            eii,
            action=self.Action(),
            targetColumnId=self.TargetColumnId(),
            inputColumn=self.InputColumn(),
            isTarget=True,
            relativeTo=self.RelativeTo(),
            name=self._actionName)
        rebalance.Execute()


class TargetValueMenuItem(RebalancingStrategiesMenuItem):

    def __init__(self, extObj):
        super(TargetValueMenuItem, self).__init__(extObj, 'Target Value')

    def InvokeAsynch(self, eii):
        rebalance = FManualRebalanceTM(
            eii,
            action=self.Action(),
            targetColumnId=self.TargetColumnId(),
            inputColumn=self.InputColumn(),
            isTarget=True,
            name=self._actionName)
        rebalance.Execute()

class FManualRebalanceTM(FTradeProgramTM):

    def __init__(self, eii, action, targetColumnId, inputColumn,
                 name=None, isTarget=False, relativeTo=None):
        
        FTradeProgramTM.__init__(self, eii, action, inputColumn,
                                 name=name, selectAll=True)
        
        self.targetColumnId = targetColumnId
        self.isTarget = isTarget
        self.relativeTo = relativeTo


    def Execute(self, trades=None):
        rowsAndInputs = self.RowsInputsAndCurrency()
        rebalance = FManualRebalance(rowsAndInputs, self.targetColumnId,
                                     self.isTarget, self.relativeTo)

        FTradeProgramTM.Execute(self, rebalance.trades)
