import acm


import SettlementProcessUtils
state_chart_name = SettlementProcessUtils.mediumRiskStateChart

def CreateStateChart():
    stateChart = acm.FStateChart(name = state_chart_name)
    stateChart.Commit()
    
    
def CreateStateChartStates():
    stateChart = acm.FStateChart[state_chart_name]
    
    stateChart.CreateState(SettlementProcessUtils.approvedLevel1)
    stateChart.CreateState(SettlementProcessUtils.approvalComplete)
    
    
    stateChart.CreateState(SettlementProcessUtils.rejectedLevel1)
    stateChart.CreateState(SettlementProcessUtils.rejectedLevel2)
        
    stateChart.Commit()
    
def CreateStateChartEvents():
    
    stateChart = acm.FStateChart[state_chart_name]
    states = stateChart.StatesByName()
    
    readyState = stateChart.ReadyState()
    
    rejectedState1 = states[SettlementProcessUtils.rejectedLevel1]
    rejectedState2 = states[SettlementProcessUtils.rejectedLevel2]
    
    initiallyApproved =states[SettlementProcessUtils.approvedLevel1]
    approvedState = states[SettlementProcessUtils.approvalComplete]    
    
    approvePaymentsLevel1 = acm.FStateChartEvent(SettlementProcessUtils.approvePaymentsLevel1)
    rejectEventLevel1 = acm.FStateChartEvent(SettlementProcessUtils.rejectPaymentsLevel1)
    approveRejectEventLevel1 = acm.FStateChartEvent(SettlementProcessUtils.approveRejectedLevel1)
    
    approvePaymentsLevel2 = acm.FStateChartEvent(SettlementProcessUtils.approvePaymentsLevel2)
    rejectEventLevel2 = acm.FStateChartEvent(SettlementProcessUtils.rejectPaymentsLevel2)
    approveRejectEventLevel2 = acm.FStateChartEvent(SettlementProcessUtils.approveRejectedLevel2)
    
    settlementUpdate = acm.FStateChartEvent(SettlementProcessUtils.settlementUpdate)
    
    
    approvePaymentsLevel1.Commit()
    rejectEventLevel1.Commit()
    approveRejectEventLevel1.Commit()
    
    approvePaymentsLevel2.Commit()
    rejectEventLevel2.Commit()
    approveRejectEventLevel2.Commit()
    
    settlementUpdate.Commit()
    
    readyState.CreateTransition(approvePaymentsLevel1, initiallyApproved)
    readyState.CreateTransition(rejectEventLevel1, rejectedState1)
    
    rejectedState1.CreateTransition(approveRejectEventLevel1, initiallyApproved)
    rejectedState1.CreateTransition(settlementUpdate, readyState)
    
    initiallyApproved.CreateTransition(approvePaymentsLevel2, approvedState)
    initiallyApproved.CreateTransition(rejectEventLevel2, rejectedState2)
    initiallyApproved.CreateTransition(settlementUpdate, readyState)
    
    rejectedState2.CreateTransition(approveRejectEventLevel2, approvedState)
    rejectedState2.CreateTransition(settlementUpdate, readyState)
    
    
    stateChart.Commit()

def CreateStateChartLayout():
    stateChart = acm.FStateChart[state_chart_name]
    layout = "Ready,50,0;Approved Level 1,450,-200;Approval Complete,900,0;" + \
            "Rejected Level 1,300,300; Rejected Level 2, 700, 300"
    stateChart.Layout().Text(layout)
    stateChart.Commit()
    
def Create():
    CreateStateChart()
    CreateStateChartStates()
    CreateStateChartEvents()
    CreateStateChartLayout()
    
