""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendOrdersWorkbookPanel.py"

"""--------------------------------------------------------------------------
MODULE
    FSecLendOrdersWorkbookPanel

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Order Manager - Main workbook panel.

-----------------------------------------------------------------------------"""
import acm
from FEvent import EventCallback
from FParameterSettings import ParameterSettingsCreator
from FSecLendEvents import (OnOrderManagerOrdersSelected,
                            OnOrderCaptureInstrumentChanged,
                            OnOrderCaptureCounterpartyChanged)
from FSecLendCommon import ExtendedWorkbookPanel, WorkbenchSheet
import FSecLendUtils
import FSecLendHooks

_SETTINGS = ParameterSettingsCreator.FromRootParameter('SecLendSettings')

class SecLendOrdersWorkbookPanel(ExtendedWorkbookPanel):
    
    def RowSelectionChanged(self, selection):
        rowObjects = selection.SelectedRowObjects()
        trades = [row.Trade() for row in rowObjects 
                    if row.IsKindOf(acm.FTradeRow) and row.Trade().Instrument().IsKindOf(acm.FSecurityLoan)]
        if trades:
            self.SendEvent(OnOrderManagerOrdersSelected(self, trades))
            if _SETTINGS.ActiveInboxInstrEvent():
                security = trades[0].Instrument().Underlying()
                self.SendEvent(OnOrderCaptureInstrumentChanged(self, security))
            if _SETTINGS.ActiveInboxPartyEvent():
                counterparty = trades[0].Counterparty()
                self.SendEvent(OnOrderCaptureCounterpartyChanged(self, counterparty))


class SecLendOrdersOrdersSheet(WorkbenchSheet):

    def DefaultInsertItemQuery(self):
        query = FSecLendHooks.ActiveLoansQuery()
        FSecLendUtils.AddQueryAttrNodeList(query, 'Status', self.Settings().FilterTradeStatuses())
        FSecLendUtils.AddQueryAttrNodeList(query, 'Type', self.Settings().FilterTradeTypes())
        FSecLendUtils.AddQueryAttrNodeList(query, 'Market.Name', self.Settings().FilterOrderSources())
        FSecLendUtils.AddQueryAttrNodeList(query, 'AdditionalInfo.SBL_OrderType', self.Settings().FilterOrderTypes())
        FSecLendUtils.AddQueryAttrNodeList(query, 'AdditionalInfo.SBL_PendingOrder',
                                                            self.Settings().FilterPendingOrders())
        if self.Settings().FilterUserTrades():
            FSecLendUtils.AddQueryAttrNodeList(query, 'Trader.Name', [acm.User().Name()])
        return query

    @EventCallback
    def OnOrderManagerOrdersEntered(self, event):
        trades = event.Parameters()
        if trades:
            self.CreateTimedPeriodicEvent(0.5, 0.25, self.GoToRow, trades[0])

    def CreateTimedPeriodicEvent(self, timeout, interval, func, param=None):
        def RemoveEvent(arg):
            timer.RemoveTimerEvent(event)
        timer = acm.FTimer()
        event = timer.CreatePeriodicTimerEvent(interval, func, param)
        timer.CreateTimerEvent(timeout, RemoveEvent, None)

    def GoToRow(self, trade):
        for sheet in self.Workbook().Sheets():
            sheet.PrivateTestSyncSheetContents()
            iterator = sheet.RowTreeIterator(False)
            while(iterator.NextUsingDepthFirst()):
                row = iterator.Tree().Item()
                if row.IsKindOf(acm.FTradeRow) and trade == row.Trade():
                    sheet.NavigateTo(row)
                    return True


class SecLendOrdersMySheet(SecLendOrdersOrdersSheet):
    def DefaultInsertItemQuery(self):
        query = super(SecLendOrdersMySheet, self).DefaultInsertItemQuery()
        FSecLendUtils.AddQueryAttrNodeList(query, 'AdditionalInfo.SBL_ToDoList', [''])
        return query
        

class SecLendOrdersToDoSheet(SecLendOrdersOrdersSheet):
    def DefaultInsertItemQuery(self):
        query = super(SecLendOrdersToDoSheet, self).DefaultInsertItemQuery()
        FSecLendUtils.AddQueryAttrNodeList(query, 'AdditionalInfo.SBL_ToDoList', [''], True)
        return query
