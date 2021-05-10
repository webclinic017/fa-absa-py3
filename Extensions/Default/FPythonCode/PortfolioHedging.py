
import acm
import PortfolioHedger
import GenericPortfolioHedger

def onAgentActivateClick(row, col, cell, activate, operation):  
    context = col.Context()
    tag = cell.GetEvaluator().Tag()
    
    agentType = acm.GetCalculatedValueFromString(row, context, 'agentPortfolioHedgerType', tag).Value()
            
    if agentType == 'Algorithm':
        GenericPortfolioHedger.onAgentActivateClick(row, col, cell, activate, operation)
    else:
        PortfolioHedger.onAgentActivateClick(row, col, cell, activate, operation)
