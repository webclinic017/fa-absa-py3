import acm

def getRelatedAgent(ownOrder):
    return acm.Trading().RelatedAgent(ownOrder)

def setPriceSpread(row, col, cell, val, operation):
    agent = getRelatedAgent(row)
    if agent:
        evaluator = agent.GetEvaluatorFromAgent('PriceSpread')
        if evaluator:
            evaluator.Simulate(val, 0)
    cell.GetEvaluator().RemoveSimulation()
