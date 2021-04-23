
import acm

import FSyntheticPrimeFunctions as Functions
import importlib
importlib.reload(Functions)
import FSyntheticPrimeCalculationAPIUtil as CalcUtil
importlib.reload(CalcUtil)
import FSyntheticPrimeCreateCF as CreateCF
importlib.reload(CreateCF)
from PortfolioSwapParameters import DealPackageParameters
from DealPackageDevKit import DealPackageUserException
import FSyntheticPrimeUtil as Util
   
def TradeAssign(parameters, resetStartDate, resetEndDate):
    if parameters.PortfolioSwap().OpenEnd() == 'Terminated':
        raise DealPackageUserException("Cannot perform Trade Assignment on a terminated Portfolio Swap.")

    Functions.TradeAssign(parameters, resetStartDate, resetEndDate)
             
def GeneratePortfolioSwap(parameters, fromDate, toDate):
    if parameters.PortfolioSwap().OpenEnd() == 'Terminated':
        raise DealPackageUserException("Cannot regenerate legs on a terminated Portfolio Swap.")

    Functions.GeneratePortfolioSwap(parameters, fromDate, toDate)
        
def Extend(parameters, date):
    if parameters.PortfolioSwap().OpenEnd() == 'Terminated':
        raise DealPackageUserException("Cannot perform Extend on a terminated Portfolio Swap.")
        
    Functions.ExtendPortfolioSwap(parameters, date)

def Fix(parameters, date):
    if parameters.PortfolioSwap().OpenEnd() == 'Terminated':
        raise DealPackageUserException("Cannot perform Fix Resets on a terminated Portfolio Swap.")

    Functions.FixPortfolioSwapResetsOnDate(parameters, date)

def Terminate(parameters, terminateDate = None):
 
    def PortfolioHasFutureTrades(terminateDate):
        trades = acm.FTrade.Select("portfolio = '%s' and valueDay > '%s' and status <> 'Void'" % (parameters.FundPortfolio().Name(), terminateDate))
        return trades.Size() > 0
    
    def PortfolioHasFutureFees(terminateDate):
        fees = CreateCF.ExecutionFeeCashFlowsPostdate(parameters, terminateDate, terminateDate)
        return len(fees) > 0
                   
    if not terminateDate:
        terminateDate = acm.Time.DateToday()
        
    if parameters.PortfolioSwap().OpenEnd() == 'Terminated':
        raise DealPackageUserException("Cannot perform Terminate on a terminated Portfolio Swap.")
    
    if Util.PortfolioHasOpenPosition(parameters.FilteredPortfolio(), Util.AdjustBankingDays(parameters.PortfolioSwap().Legs().First(), terminateDate, -1)):
        raise DealPackageUserException("Cannot terminate Portfolio Swap if Synthetic Portfolio has open positions.")
        
    if PortfolioHasFutureTrades(terminateDate):
        raise DealPackageUserException("Cannot terminate Portfolio Swap if Synthetic Portfolio contains trades with value date after the termination date.")
    
    if PortfolioHasFutureFees(terminateDate):
        raise DealPackageUserException("Cannot terminate Portfolio Swap if Synthetic Portfolio contains trades with payments where pay date is after the termination date.")
    
    if Util.PortfolioHasIncomingDividendPayment(parameters, terminateDate):
        raise DealPackageUserException("Cannot terminate Portfolio Swap if there are incoming dividends.") 
      
    if not parameters.PortfolioSwap().LongestLeg():
        raise DealPackageUserException("Cannot terminate Portfolio Swap on an incorrectly set up Portfolio Swap.")
    
    Functions.TerminatePortfolioSwap(parameters, terminateDate)
    return parameters.DealPackage().Save().First().Edit() 
    
def Roll(parameters, newExpiryDate = None, newPfName = None, terminateDate = None):
    if not terminateDate:
    	terminateDate = acm.Time.DateToday() 
        
    if Util.PortfolioHasIncomingDividendPayment(parameters, terminateDate):
        raise DealPackageUserException("Cannot roll Portfolio Swap if there are incoming dividends.") 
    
    expiryDate = parameters.DealPackage().GetAttribute('expiryDate')
    financingRollingBaseDate = parameters.DealPackage().GetAttribute('financingRollingBaseDate')
    cashRollingBaseDate = parameters.DealPackage().GetAttribute('cashRollingBaseDate')
    performanceRollingBaseDate = parameters.DealPackage().GetAttribute('performanceRollingBaseDate')
    rplPerformanceRollingBaseDate = parameters.DealPackage().GetAttribute('rplPerformanceRollingBaseDate')
    uplPerformanceRollingBaseDate = parameters.DealPackage().GetAttribute('uplPerformanceRollingBaseDate')
    stockBorrowRollingBaseDate = parameters.DealPackage().GetAttribute('stockBorrowRollingBaseDate')
    
    if not newExpiryDate:
        newExpiryDate = expiryDate
    
    newPf = parameters.DealPackage().Copy()
    newPf.SetAttribute('startDate', terminateDate)
    newPf.SetAttribute('expiryDate', newExpiryDate)
    newPf.SetAttribute('financingRollingBaseDate', financingRollingBaseDate)
    newPf.SetAttribute('cashRollingBaseDate', cashRollingBaseDate)
    newPf.SetAttribute('performanceRollingBaseDate', performanceRollingBaseDate)
    newPf.SetAttribute('rplPerformanceRollingBaseDate', rplPerformanceRollingBaseDate)
    newPf.SetAttribute('uplPerformanceRollingBaseDate', uplPerformanceRollingBaseDate)
    newPf.SetAttribute('stockBorrowRollingBaseDate', stockBorrowRollingBaseDate)
    newPf.SetAttribute('tradeTime', terminateDate)
    newPf.InstrumentAt('PrfSwap').Instrument().Legs().Clear()        
    Util.ClearPortfolioSwapPaymentsPreDate(newPf.TradeAt('PrfSwap'), terminateDate)
    
    if not newPfName:
        newPf.SuggestName()
        name = newPf.InstrumentPackage().Name()
        newPf.SetAttribute('name', name)
    else:
        newPf.SetAttribute('name', newPfName)
    

    rolledPf = None
    terminatedPf = None
    acm.BeginTransaction()
    try:
        rolledPf = newPf.SaveNew().First()
        Functions.TerminatePortfolioSwap(parameters, terminateDate)
        terminatedPf = parameters.DealPackage().Save().First()    
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        raise
    return (rolledPf.Edit(), terminatedPf)

def SweepCash(parameters, date):
    if parameters.PortfolioSwap().OpenEnd() == 'Terminated':
        raise DealPackageUserException("Cannot perform Sweep Cash on a terminated Portfolio Swap.")

    Functions.SweepCashPortfolioSwap(parameters, date, date)

def FixPortfolioSwapResetsOnDate(parameters, date):
    if parameters.PortfolioSwap().OpenEnd() == 'Terminated':
        raise DealPackageUserException("Can not perform Fixing on a terminated Portfolio Swap.")

    Functions.FixPortfolioSwapResetsOnDate(parameters, date)

def AdjustCash(parameters, amount = None, currency = None, date = None):

    if not amount:
        portfolioSwapTrade = parameters.DealPackage().TradeAt("PrfSwap")
        amount = Util.CalculateSyntheticCash(portfolioSwapTrade)
        
    if not currency:
        portfolioSwapTrade = parameters.DealPackage().TradeAt("PrfSwap")
        currency = portfolioSwapTrade.Currency()
    
    if not date:
        legs = [leg for leg in parameters.PortfolioSwap().Legs() if leg.IsSyntheticCashLeg()]
        syntheticCashLeg = 1 == len(legs) and legs[0] or None
        lastCallFloatRate = None
        for cf in syntheticCashLeg.CashFlows():
            if cf.CashFlowType() == "Call Float Rate":
                if not lastCallFloatRate:
                    lastCallFloatRate = cf
                elif acm.Time().DateDifference(cf.EndDate(), lastCallFloatRate.EndDate()):
                    lastCallFloatRate = cf
        if lastCallFloatRate:
            date = lastCallFloatRate.EndDate()
        else:
            date = acm.Time().DateToday()

    syntheticCashLeg = Util.GetCallDepositLeg(parameters.PortfolioSwap())
    portfolioSwapTrade = parameters.DealPackage().TradeAt("PrfSwap")
    Util.AdjustCash(syntheticCashLeg, portfolioSwapTrade, amount, currency, date)
