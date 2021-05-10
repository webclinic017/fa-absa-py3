import acm


import SettlementProcessUtils
state_chart_name = SettlementProcessUtils.lowRiskStateChart
def CreateStateChart():
    stateChart = acm.FStateChart(name = state_chart_name)
    stateChart.Commit()
    
    
def CreateStateChartStates():
    stateChart = acm.FStateChart[state_chart_name]
    
    stateChart.CreateState(SettlementProcessUtils.approvalComplete)
    
    
    stateChart.CreateState(SettlementProcessUtils.rejectedLevel1)
    stateChart.Commit()
    
def CreateStateChartEvents():
    
    stateChart = acm.FStateChart[state_chart_name]
    states = stateChart.StatesByName()
    
    readyState = stateChart.ReadyState()
    
    rejectedState1 = states[SettlementProcessUtils.rejectedLevel1]
    approvedState = states[SettlementProcessUtils.approvalComplete]    
    
    approvePaymentsLevel1 = acm.FStateChartEvent(SettlementProcessUtils.approvePaymentsLevel1)
    rejectEventLevel1 = acm.FStateChartEvent(SettlementProcessUtils.rejectPaymentsLevel1)
    approveRejectEventLevel1 = acm.FStateChartEvent(SettlementProcessUtils.approveRejectedLevel1)
    sendForReProcessing = acm.FStateChartEvent(SettlementProcessUtils.sendForReProcessing)
    settlementUpdate = acm.FStateChartEvent(SettlementProcessUtils.settlementUpdate)
    
    
    approvePaymentsLevel1.Commit()
    rejectEventLevel1.Commit()
    approveRejectEventLevel1.Commit()
    settlementUpdate.Commit()
    
    readyState.CreateTransition(approvePaymentsLevel1, approvedState)
    readyState.CreateTransition(rejectEventLevel1, rejectedState1)
    
    rejectedState1.CreateTransition(approveRejectEventLevel1, approvedState)
    rejectedState1.CreateTransition(sendForReProcessing, readyState)
    rejectedState1.CreateTransition(settlementUpdate, readyState)
    
    stateChart.Commit()

def CreateStateChartLayout():
    stateChart = acm.FStateChart[state_chart_name]
    layout = "Ready,50,-100;Rejected Level 1,400,-100;Approval Complete,220,50"
    stateChart.Layout().Text(layout)
    stateChart.Commit()
    
def Create():
    CreateStateChart()
    CreateStateChartStates()
    CreateStateChartEvents()
    CreateStateChartLayout()
    
