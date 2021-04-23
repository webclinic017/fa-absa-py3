""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendLoanMenuItems.py"
"""--------------------------------------------------------------------------
MODULE
    FSecLendLoanMenuItems

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Menu items for Loan actions.

---------------------------------------------------------------------------"""
import acm
import FSecLendUtils
from ACMPyUtils import Transaction
from FSecLendMenuItem import SecLendMenuItemBase
from DealPackageAsDialog import OpenDealPackageDialogWithSaveNew  
from FSecLendOrdersWorkbookHandler import SecLendOrderManagerTradesHandler
from FSecLendInventoryPositionHandler import SecLendInventoryPositionHandler
from FSecLendInventoryAvailabilityPanels import SecLendInventoryAvailabilityPanelBase
from FSecLendEvents import (OnOrderCaptureInstrumentChanged,
                            OnOrderCaptureCounterpartyChanged)
from FIntegratedWorkbench import GetHandler
from FClipboardUtilities import SetClipboardText
from FWorkbenchObserver import WorkbenchObserver
import FSecLendHooks

class LoanMenuItem(SecLendMenuItemBase):

    def __init__(self, extObj):
        super(LoanMenuItem, self).__init__(extObj)

    def Shell(self):
        return self._frame.Shell()

    def ActiveSheetSelection(self):
        if hasattr(self._frame, 'ActiveSheet'):
            return self._frame.ActiveSheet().Selection().SelectedRowObjects()

class SendToViewsItem(LoanMenuItem):
    def __init__(self, eii):
        super(SendToViewsItem, self).__init__(eii)
        self._observer = None
    
    def EnabledFunction(self, *args):
        return self.SelectedTrade() is not None
    
    def SelectedCounterparty(self):
        return self.SelectedTrade() and self.SelectedTrade().Counterparty()

    def SelectedInstrument(self):
        return self.SelectedTrade() and self.SelectedTrade().Instrument().Underlying()
        
    def Observer(self):
        if self._observer is None:
            self._observer = WorkbenchObserver(self._Dispatcher(), self)
        return self._observer

    def SendEvent(self, event):
        self.Observer().SendEvent(event)

    def Invoke(self, eii):
        self.SendEvent(OnOrderCaptureCounterpartyChanged(self, self.SelectedCounterparty()))
        self.SendEvent(OnOrderCaptureInstrumentChanged(self, self.SelectedInstrument()))

class SendFromTradeSheetToViewsItem(SendToViewsItem):
    def SelectedTrade(self):
        trade = None
        handler = GetHandler(self.View(), SecLendOrderManagerTradesHandler)
        if handler and handler.Trades() and len(handler.Trades()) == 1:
            trade = handler.Trades().First()
        return trade

class SendFromPricingSheetToViewsItem(SendToViewsItem):
    def SelectedTrade(self):
        sheetSelection = self.ActiveSheetSelection()
        row = sheetSelection.First() if sheetSelection else None
        trade = None
        if row and row.IsKindOf('FTradeRow'):
            trade = row.Trade()
        return trade

class ApplySuggestedFeeItem(LoanMenuItem):    
    def EnabledFunction(self, *args):
        return self.ActiveSheetSelection() and self.ActiveSheetSelection().First().IsKindOf('FTradeRow')
    
    def Invoke(self, eii):
        editedTrades = []
        with Transaction():
            for row in self.ActiveSheetSelection():
                if row.IsKindOf('FTradeRow'):
                    trade = row.Trade()
                    if trade.StorageId() == trade.Originator().StorageId() and trade.StorageId() > 0:
                        FSecLendUtils.SetDefaultRate(trade) # Only changes the instrument
                        trade.Instrument().Commit()
                    else:
                        editedTrades.append(trade)
        for trade in editedTrades:
            FSecLendUtils.SetDefaultRate(trade)
    
class NewLoanMenuItem(LoanMenuItem):

    def InvokeAsynch(self, eii):
        """ Open the Security Loan Deal application for creating a new loan. """
        deal = acm.Deal.New('Security Loan Deal')
        self.SetDefaultAttributes(deal)
        acm.StartApplication('Deal', deal)

    def SetDefaultAttributes(self, deal):
        self.SetSelectedUnderlying(deal)
        self.SetSelectedCounterparty(deal)

    def SetSelectedUnderlying(self, deal):
        underlying = self._SelectedUnderlying()
        if underlying:
            deal.SetAttribute('ins_underlyingType', underlying.InsType())
            deal.SetAttribute('ins_underlying', underlying)
            
    def SetSelectedCounterparty(self, deal):
        counterparty = self._SelectedConterparty()
        if counterparty:
            deal.SetAttribute('trade_counterparty', counterparty)

    def _SelectedUnderlying(self):
        instrument = None
        orderCapturePanel = self._Panel('SecLendOrdersOrderCapturePanel')
        if orderCapturePanel:
            instrument = orderCapturePanel.GetSelectedInstrument()
        row = self.SelectedLoanRow()
        if instrument is None and hasattr(row, 'Instrument'):
            instrument = row.Instrument()
        if instrument is None and isinstance(row, acm._pyClass("FMultiInstrumentAndTrades")):
            instrument = self._InstrumentFromTree(row)
        return instrument.UnderlyingOrSelf() if instrument else None

    @classmethod
    def _InstrumentFromTree(cls, row):
        if row.Grouping():
            refVal = row.Grouping().GroupingValueReference()
            if isinstance(refVal, acm._pyClass("FInstrument")):
                return refVal
        return cls._InstrumentFromTree(row.Parent()) if row.Parent() else None
        

    def _SelectedConterparty(self):
        """ Get the selected counterparty in the current view. """
        cpty = None
        clientSelectionPanel = self._Panel('SecLendClientSelectionPanel')
        if clientSelectionPanel:
            cpty = clientSelectionPanel.GetSelectedClient()
        if cpty is None:
            orderCapturePanel = self._Panel('SecLendOrdersOrderCapturePanel')
            if orderCapturePanel:
                cpty = orderCapturePanel.GetSelectedCounterparty()
        if cpty is None:
            row = self.SelectedLoanRow()
            if isinstance(row, acm._pyClass('FInstrumentAndTrades')):
                cpty =  self._CounterpartyFromTree(row)
        return cpty

    @staticmethod
    def _IsCounterparty(party):
        if isinstance(party, acm._pyClass('FParty')) and \
            type(party) not in (acm._pyClass('FMTMMarket'), acm._pyClass('FIssuer')):
            return True
        return False

    @classmethod
    def _CounterpartyFromTree(cls, row):
        if row.Grouping():
            refVal = row.Grouping().GroupingValueReference()
            if cls._IsCounterparty(refVal):
                return refVal
        return cls._CounterpartyFromTree(row.Parent()) if row.Parent() else None

    def SelectedLoanRow(self):
        """ Get the selected loan row based on the current view and in
            which panel the loans are presented in each view.
        """
        sheetSelection = self.ActiveSheetSelection()
        return sheetSelection.First() if sheetSelection else None

class TradeActionNotEnabled(Exception):
    pass

class LoanActionMenuItem(LoanMenuItem):
    ACTION = ''
    
    def EnabledFunction(self):
        row = self.TargetRow01()
        if row:
            trade = self.GetTrade(row)
            return bool(trade) and acm.TradeActionUtil.ValidateTradeToClose(trade) == ""
        return False
        
    def TargetRow01(self):
        """ Check which the active view is and calculate """
        view = self._ViewName()
        if view == 'SecLendClientView':
            return self.PortfolioSheetTargetRow()
        elif view == 'SecLendInventoryView':
            return self.InventoryViewTargetRow()
        elif view == 'SecLendOrdersView':
            return self.OrderManagerViewTradesHandler()
        elif view == 'SecLendPortfolioView':
            return self.PortfolioSheetTargetRow()
        return None

    def OrderManagerViewTradesHandler(self):
        handler = GetHandler(self.View(), SecLendOrderManagerTradesHandler)
        if handler and handler.Trades() and len(handler.Trades()) == 1:
            return handler
            
    def InventoryViewTargetRow(self):
        handler = GetHandler(self.View(), SecLendInventoryPositionHandler)
        if handler and \
            handler.PositionRows() and \
            handler.PositionRows().Size() == 1 and \
            hasattr(handler.PositionRows().First(), 'Instrument') and \
            handler.PositionRows().First().Instrument() is not None:
            return handler.PositionRows().First()

    def PortfolioSheetTargetRow(self):
        selectedLoanRows = self.ActiveSheetSelection()
        if selectedLoanRows.Size() == 1 and \
            hasattr(selectedLoanRows.First(), 'Instrument') and \
            selectedLoanRows.First().Instrument() is not None:
            return selectedLoanRows.First()
        return None

    def InvokeAsynch(self, eii):
        try:
            row = self.TargetRow01()
            if row:
                trade = self.GetTrade(row)
                if trade:
                    self.ExecuteTradeActionForTrade(trade)
        except TradeActionNotEnabled as e:
            acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Information', str(e))
        except Exception as e:
            msg = 'Error when initiating trade action. Reason: {0}'.format(e)
            acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', msg)
       
     
    def GetTrade(self, row):
        if row and hasattr(row, 'Trades'):
            trades = {t.Contract() for t in row.Trades()}
            return trades.pop()
    
    def ExecuteTradeActionForTrade(self, trade):
        tradeAction = acm.Deal.Wrap(trade).TradeActionAt(self.ACTION)
        if tradeAction.Enabled():
            deals = tradeAction.Invoke()
            for deal in deals:
                caption = ' - '.join((tradeAction.DisplayName(), trade.StringKey(), trade.Instrument().StringKey()))
                OpenDealPackageDialogWithSaveNew(self.Shell(), deal, caption)
        else:
            raise TradeActionNotEnabled('Trade action is not enabled for this trade')

class IncreaseLoanMenuItem(LoanActionMenuItem):
    ACTION = 'increase'

class ReturnLoanMenuItem(LoanActionMenuItem):
    ACTION = 'close'

class RecallLoanMenuItem(LoanActionMenuItem):
    ACTION = 'recall'

class LoanActionRightClickMenuItem(LoanActionMenuItem):
    def Applicable(self):
        return  bool(self.TargetRow01()) and self._ViewName() in ('SecLendClientView', 'SecLendInventoryView')
    
    def Invoke(self, eii):
        self.ACTION = eii.MenuExtension().At('ACTION')
        super(LoanActionRightClickMenuItem, self).Invoke(eii)
        

class SortMenuItem(LoanMenuItem):
    def __init__(self, extObj):
        super(SortMenuItem, self).__init__(extObj)

    def Applicable(self):
        return  self._ViewName() == 'SecLendInventoryView'

    def GetObserver(self, sheet):
        for observer in self.View().Dispatcher().Observers():
            try:
                if sheet == observer.Sheet().Sheet():
                    return observer
            except AttributeError:
                continue

    def InvokeAsynch(self, eii):
        sheet = eii.Parameter( "sheet" )
        column = sheet.Selection().SelectedCell().Column()
        observer = self.GetObserver(sheet)
        if observer and column:
            if not isinstance(observer, SecLendInventoryAvailabilityPanelBase):
                #Menues shouldn't be available but it is not possible to get the sheet in the applicable method
                acm.Log('Persisted sorting only avialable in Internal and External Availability sheets')
                return
            ascending = str(eii.MenuExtension().Name()).lower().find("ascending") != -1
            observer.SortBy(column.ColumnId(), ascending, True)

def NewLoanItem(eii):
    return NewLoanMenuItem(eii)

def SendFromTradeSheetToViews(eii):
    return SendFromTradeSheetToViewsItem(eii)

def SendFromPricingSheetToViews(eii):
    return SendFromPricingSheetToViewsItem(eii)

def ApplySuggestedFee(eii):
    return ApplySuggestedFeeItem(eii)

def IncreaseLoanItem(eii):
    return IncreaseLoanMenuItem(eii)
    
def LoanActionRightClickItem(frame):
    return LoanActionRightClickMenuItem(frame)
    
def Sort(frame):
    return SortMenuItem(frame)

def ReturnLoanItem(eii):
    return ReturnLoanMenuItem(eii)
    
def RecallLoanItem(eii):
    return RecallLoanMenuItem(eii)

def GetBusinessProcessFromSheet(eii):
    sheet = eii.Parameter('sheet')
    trades = sheet.Selection().SelectedTrades()
    stateChartDefinition = FSecLendHooks.WorkflowStateChart
    bps = [ bp for trade in trades for bp in acm.BusinessProcess.FindBySubjectAndStateChart(trade, stateChartDefinition.NAME)]
    return bps

def OpenBusinessProcessesFromTrades(eii):
    businessProcesses = GetBusinessProcessFromSheet(eii)
    if businessProcesses:
        acm.StartApplication("Operations Manager", businessProcesses)

def OpenBusinessProcessDetailsFromTrades(eii):
    businessProcesses = GetBusinessProcessFromSheet(eii)
    if businessProcesses:
        acm.StartApplication("Business Process Details", businessProcesses[0])
        
def CopySecurityLoanTextToClipboard(eii):
    sheet = eii.Parameter('sheet')
    trades = sheet.Selection().SelectedTrades()
    
    clipboardText = FSecLendHooks.ClipBoardTextHookFromTrades(trades)
    
    if clipboardText:
    	SetClipboardText(clipboardText)
