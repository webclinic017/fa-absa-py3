""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendReturns.py"

"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendReturns

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Business logic for finding proper instruments to return. 
    Creating return trades for the instruments with highest cost. 

------------------------------------------------------------------------------------------------"""
import acm
from collections import defaultdict, namedtuple
from FParameterSettings import ParameterSettingsCreator
from FSecLendHandler import SecurityLoanTradeAction
import FSecLendUtils

# -------------- Used for Finding Original/Mother Trades and Create Return Trades --------------
    
CostAndQuantity = namedtuple('CostAndQuantity', 'item, cost, quantity')
CalculationParameters = namedtuple('CalculationParameters', 'columnId, calculationConf, projectionParts')

_SETTINGS = ParameterSettingsCreator.FromRootParameter('SecLendAllocationSettings')

SECLEN_SETTINGS = ParameterSettingsCreator.FromRootParameter('SecLendSettings')
 # ----------------------------- Exceptions used for the Returns -------------------------------

class NoQuantityFoundError(Exception):
    pass

class NoReturnLoansFoundError(Exception):
    pass

 # ------------------ Find Orignial/Mother Trades and Create Return Trades ---------------------
    
def CreateReturnTrades(trades, quantity, clientReturns=False, returnPartial=False, **kwargs):
    if not trades:
        raise NoReturnLoansFoundError()
    returnCandidates = GetOriginalTrades(trades, quantity, clientReturns, returnPartial) #Suggests original/mother trades
    return ReturningTrades(returnCandidates, quantity, **kwargs) 

def GetOriginalTrades(trades, quantityToReturn, clientReturns=False, returnPartial=False):
    if not quantityToReturn:
        raise NoQuantityFoundError()
    activeTrades = ActiveTrades(trades, clientReturns)
    return ReturnLoansByCost(activeTrades, quantityToReturn, returnPartial, highCostFirst=True)

def ActiveTrades(trades, clientReturns=False): 
    def IsReturnable(ins):
        if ins.OpenEnd() == "Open End":
            return ins.NoticePeriod() == '2d' or not ins.NoticePeriodCount()
    def IsActiveInloan(trade):
        return (trade.Instrument().InsType() == 'SecurityLoan' and
                not FSecLendUtils.IsAvailabilityTrade(trade) and
                not trade.Instrument().IsTerminated() and
                trade.Instrument().ExpiryDate() >= acm.Time().DateAdjustPeriod(acm.Time.DateToday(),
                                                        SECLEN_SETTINGS.IncludeExpiredTill()) and
                IsReturnable(trade.Instrument()) and
                trade.Type() == 'Normal')
                
    activeTrades = []
    for trade in trades:
        tradeQty = SecurityLoanTradeAction._RemainingQuantity(trade)
        if (clientReturns and  tradeQty < 0) or \
           (not clientReturns and tradeQty > 0): #Check sign of quantity
            if IsActiveInloan(trade):
                remainingQuantity = abs(tradeQty)
                fee = CalculateLoanCost(trade)
                activeTrades.append(CostAndQuantity(trade, fee, remainingQuantity))
    return activeTrades

def CalculateLoanCost(trade):
    columnId = _SETTINGS.ReturnCostColumn()
    calc_space = acm.Calculations().CreateCalculationSpace(
                acm.GetDefaultContext(), 'FTradeSheet')
    return calc_space.CalculateValue(trade, columnId)

def ReturnLoansByCost(costAndQuantities, sourceAmount, returnPartial=False, highCostFirst=True):
    if not costAndQuantities and returnPartial:
        return {}
    itemPerCost = SortedByPrice(costAndQuantities) 
    amountLeft = abs(sourceAmount)
    loansToReturn = {}
    
    #Return loans with respect to the cost
    for cost in sorted(itemPerCost, reverse=highCostFirst):
        positionsAtCost = itemPerCost[cost]
        #Check if there exists a loan with quantity equal to the quantity to be returned
        position = next((pos for pos in positionsAtCost if pos.quantity == amountLeft), None) 
        if position: 
            loansToReturn[position.item] = amountLeft
            return loansToReturn
        #Return the loans with the highest quantities
        for pos in HighestQuantityFirst(positionsAtCost):
            if amountLeft > pos.quantity:   
                loansToReturn[pos.item] = pos.quantity
                amountLeft -= pos.quantity
            else:
                loansToReturn[pos.item] = amountLeft
                return loansToReturn
    if not returnPartial and amountLeft !=0:
        raise NoReturnLoansFoundError()
    return loansToReturn
    
def SortedByPrice(costAndQuantities):
    cptyPerPrice = defaultdict(list)
    for pos in costAndQuantities:
        cptyPerPrice[pos.cost].append(pos)
    return cptyPerPrice
    
def HighestQuantityFirst(costAndQuantities):
    return sorted(costAndQuantities, reverse=True, key=lambda x: x.quantity)
    
def ReturningTrades(returnCandidates,
                         qty, 
                         valueDay=None, 
                         status=None, 
                         acquirer=None, 
                         source=None,
                         returntype='return'):
    newTrades = []

    for orgTrade, quantity in returnCandidates.items():
        if returntype == 'return':
            trade = SecurityLoanTradeAction.CreateCloseTrade(orgTrade,
                                                         -quantity if qty < 0 else quantity,
                                                          valueDay,
                                                          orderType='Firm',
                                                          pendingOrder=False)
        else:
            trade = SecurityLoanTradeAction.CreateRecallTrade(orgTrade,
                                                             -quantity if qty < 0 else quantity,
                                                             valueDay,
                                                             orderType='Firm',
                                                             pendingOrder=False)
        portfolio = orgTrade.Portfolio()
        if portfolio is not None:
            trade.Portfolio = portfolio
        if status is not None:
            trade.Status = status
        if acquirer is not None:
            trade.Acquirer = acquirer
        if source is not None:
            trade.Market = source
        
        newTrades.append(trade)
    return newTrades
