""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/HedgingCostWorkflowInsDefDock.py"

import acm
import FUxCore
from HedgingCostPaymentsDialog import HedgingCostPaymentsDialog, HedgingCostReRequestPaymentsDialog
from HedgingCostUtils import IsSwapDesk, IsHedgingCostDesk, HedgingCostStateChartConstants
from HedgingCostHooksHelper import IsHedgingCostCandidate

CHART_NAME = HedgingCostStateChartConstants.CHART_NAME
STATES     = HedgingCostStateChartConstants.STATES
EVENTS     = HedgingCostStateChartConstants.EVENTS

def OnRequestHedgingCostClicked( self, cd ):
    if not self.CheckErrors():
        bp = self.ActiveBusinessProcess()
        
        if acm.BusinessProcess.CanInitializeProcess(self.m_trade, self.m_stateChart):
            bp = acm.BusinessProcess.InitializeProcess(self.m_trade, self.m_stateChart)
            bp.Commit()
            bp.HandleEvent(EVENTS.HEDGINGCOST_REQUESTED)
            bp.Commit()
        elif bp and bp.CanHandleEvent(EVENTS.HEDGINGCOST_RE_REQUEST):
            dialog = HedgingCostReRequestPaymentsDialog( self.Owner().Shell() )
            reason = dialog.ShowHedgingCostReRequestPaymentsDialog()
            if reason:
                paramsDict = {'reRequestReason' : reason}
                bp.HandleEvent(EVENTS.HEDGINGCOST_RE_REQUEST, paramsDict)
                bp.Commit()

def OnAssignHedgingCostClicked( self, cd ):    
    if self.Owner().ContentIsChanged():
        acm.UX().Dialogs().MessageBoxInformation(self.Owner().Shell(), 'Content has changed, Save before Assign Hedging Cost')
    else:
        bp = self.ActiveBusinessProcess()
        if bp and bp.CanHandleEvent(EVENTS.HEDGINGCOST_ASSIGNED):
            notes = ''
            for n in bp.CurrentStep().DiaryEntry().Notes():
                notes += n + '\n'
            dialog = HedgingCostPaymentsDialog( self.Owner().Shell() )
            paymentsDict = dialog.ShowHedgingCostPaymentsDialog(self.Owner().OriginalTrade(), notes)
            if paymentsDict:
                bp.HandleEvent(EVENTS.HEDGINGCOST_ASSIGNED, paymentsDict)
                bp.Commit()


def OnConfirmTradeClicked( self, cd ):
    if self.Owner().ContentIsChanged():
        acm.UX().Dialogs().MessageBoxInformation(self.Owner().Shell(), 'Content has changed, Save before Confirm Trade')
    else:
        bp = self.ActiveBusinessProcess()
        if bp and bp.CanHandleEvent(EVENTS.TRADE_CONFIRMED):
            bp.HandleEvent(EVENTS.TRADE_CONFIRMED)
            bp.Commit()
            
def OnBusinessProcessDetailClicked( self, cd ):    
    bp = self.LastBusinessProcess()
    if bp:      
        acm.StartApplication('Business Process Details', bp )
    

class BusinessProcessInsDefDock ( FUxCore.LayoutPanel ):
    def __init__(self):
        self.m_stateChart = acm.FStateChart[CHART_NAME]
        self.m_trade = None

    def UpdateControls(self):
        bp = self.ActiveBusinessProcess()
        lastBp = self.LastBusinessProcess()

        trade = self.Owner().EditTrade()
        if trade and trade.Instrument().IsKindOf('FCurrency') and not trade.IsFxForward():
            requestHedgingCostEnabled = False
            assignHedgingCostEnabled = False
            reRequestHedgingCostEnabled = False
            confirmTradeEnabled = False
        else:
            requestHedgingCostEnabled = acm.BusinessProcess.CanInitializeProcess(self.m_trade, self.m_stateChart)
            assignHedgingCostEnabled = bp and bp.CanHandleEvent(EVENTS.HEDGINGCOST_ASSIGNED)
            reRequestHedgingCostEnabled = bp and bp.CanHandleEvent(EVENTS.HEDGINGCOST_RE_REQUEST)
            confirmTradeEnabled = bp and bp.CanHandleEvent(EVENTS.TRADE_CONFIRMED)

        businessProcessDetailEnabled = bool( lastBp )        
        boxLabel = ''
        
        if bp:
            boxLabel += 'State: ' + bp.CurrentStep().State().Name()
            
        self.m_HedgingCostBoxCtrl.Label(boxLabel)
        self.m_requestHedgingCostBtn.Enabled(requestHedgingCostEnabled or reRequestHedgingCostEnabled)
        self.m_assignHedgingCostBtn.Enabled(assignHedgingCostEnabled)
        self.m_confirmTradeBtn.Enabled(confirmTradeEnabled)
        self.m_businessProcessDetailBtn.Enabled(businessProcessDetailEnabled)

    def CreateQueryResultToFindBySubjectAndStateChart(self, object):
        if object:
            query = acm.BusinessProcess.FindBySubjectAndStateChartQuery(object, self.m_stateChart)
            queryResult = query.Select_Triggered()
            queryResult.AddDependent(self) 
            return queryResult
        return None
        
    def ActiveBusinessProcess(self):
        activeProcess = None
        nbrActive = 0
        allBusinessProcesses = self.AllBusinessProcessesForTrade()
        for bp in allBusinessProcesses:
            if not bp.IsInEndState():
                activeProcess = bp
                nbrActive +=1
                
        if nbrActive > 1:
            print(allBusinessProcesses, 'Cannot have more than ONE active Business Process')
            return
        else:
            return activeProcess
            
    def LastBusinessProcess(self):
        allBusinessProcesses = self.AllBusinessProcessesForTrade()
        if allBusinessProcesses:
            return allBusinessProcesses[-1]
        else:
            return None
        
    def CheckErrors(self):
        if self.Owner().ContentIsChanged():
            acm.UX().Dialogs().MessageBoxInformation(self.Owner().Shell(), 'Content has changed, Save before Request Hedging Cost')
            return True
        if not self.m_trade.Acquirer():
            acm.UX().Dialogs().MessageBoxInformation(self.Owner().Shell(), 'No Acquirer selected')
            return True
        
        return False

    def AllBusinessProcessesForTrade(self):
        bps = acm.FSortedCollection()
        if self.m_tradeQueryResult:
            bps = self.m_tradeQueryResult.Result()
        return bps
        
    def UpdateDependent(self):    
        if not self.m_trade == self.Owner().OriginalTrade():
            if self.m_tradeQueryResult: self.m_tradeQueryResult.RemoveDependent(self)
            self.m_trade = self.Owner().OriginalTrade()
            self.m_tradeQueryResult = self.CreateQueryResultToFindBySubjectAndStateChart(self.m_trade)

    def ServerUpdate(self, sender, aspect, parameter ):
        if sender.IsKindOf(acm.FASQLQueryResult):
            if str(aspect) == 'resultChanged':
                self.m_tradeQueryResult.ApplyChanges()
                self.UpdateControls()
         
        elif sender.IsKindOf(acm.CInsDefAppFrame):
            if str(aspect) == 'ContentsChanged':
                self.UpdateDependent()
                self.UpdateControls()
            elif str(aspect) == 'delete':
                sender.RemoveDependent(self)
                self.UpdateControls()
            elif str(aspect) == 'OnDestroy':
                if self.m_tradeQueryResult: self.m_tradeQueryResult.RemoveDependent(self)

        elif sender.IsKindOf(acm.FTrade):
            if str(aspect) == 'delete':
                sender.RemoveDependent(self)
                self.Owner().EditTrade().AddDependent(self)
            self.UpdateControls()

    def HandleCreate( self ):
        layout = self.SetLayout( self.CreateLayout() )
        
        self.m_HedgingCostBoxCtrl = layout.GetControl('HedgingCostBox')
        
        self.m_requestHedgingCostBtn = layout.GetControl('requestHedgingCostBtn')
        self.m_requestHedgingCostBtn.AddCallback( 'Activate', OnRequestHedgingCostClicked, self )
        self.m_requestHedgingCostBtn.Visible( IsSwapDesk() )

        self.m_assignHedgingCostBtn = layout.GetControl('assignHedgingCostBtn')
        self.m_assignHedgingCostBtn.AddCallback( 'Activate', OnAssignHedgingCostClicked, self )
        self.m_assignHedgingCostBtn.Visible( IsHedgingCostDesk() )

        self.m_confirmTradeBtn = layout.GetControl('confirmTradeBtn')
        self.m_confirmTradeBtn.AddCallback( 'Activate', OnConfirmTradeClicked, self )
        self.m_confirmTradeBtn.Visible( IsSwapDesk() )

        self.m_businessProcessDetailBtn = layout.GetControl('businessProcessDetailBtn')
        self.m_businessProcessDetailBtn.AddCallback( "Activate", OnBusinessProcessDetailClicked, self )

        self.m_trade = self.Owner().OriginalTrade()
        
        self.Owner().AddDependent(self)
        self.Owner().EditTrade().AddDependent(self)
        self.m_tradeQueryResult = self.CreateQueryResultToFindBySubjectAndStateChart(self.m_trade)
        self.UpdateControls()
        
    def CreateLayout( self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginHorzBox('Invisible', '', 'HedgingCostBox')
        b.    AddButton('requestHedgingCostBtn', 'Request')
        b.    AddButton('assignHedgingCostBtn', 'Assign...')
        b.    AddButton('confirmTradeBtn', 'Confirm')
        b.    AddFill()
        b.    AddButton('businessProcessDetailBtn', 'Show Details...')
        b.  EndBox()
        b.EndBox()
        return b

def OnCreate(eii):
    if IsSwapDesk() or IsHedgingCostDesk():
        basicApp = eii.ExtensionObject()
        myPanel = BusinessProcessInsDefDock()
        basicApp.CreateCustomDockWindow(myPanel, 'HedgingCostWorkflowInsDefDock', 'HedgingCost', 'Bottom')
