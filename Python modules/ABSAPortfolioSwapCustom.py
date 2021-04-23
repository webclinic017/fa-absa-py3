"""-----------------------------------------------------------------------
MODULE
    ABSAPortfolioSwapCustom

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : Custom extensions for the ABSAPortfolioSwap module.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Micheal Klimke
    CR Number           : 455227

HISTORY
================================================================================
Date       Change no     Developer          Description
--------------------------------------------------------------------------------
2011-07-18               Herman Hoon        Added the logic for DMA and Non DMA EquityTradeType
                                            Execution premiums
2012-03-28               Peter Fabian       The cost plus methodology calculation used for
                                            calculating ExecutionFee
2012-05-16 C194115       Peter Fabian       Added support to pick up fees from Payment table if
                                            trades went through alloc process
2012-11-30 C620460       Peter Fabian       The fees for allocated trades are calculated on the
                                            fly instead of picked up from Payments
2014-06-05 C2018916      Jakub Tomaga       On-tree, off-tree execution fee calculations.
2018-12-21 CHG1001240466 Tibor Reiss        Sweeping of dividend suppression
-----------------------------------------------------------------------"""


import math

import ael
import acm

import PS_new_fees
import PS_TradeFees


DEBUG = False
INCLUDED_TRADE_STATUS = ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']
'''================================================================================================
================================================================================================'''
def Price(Instrument,Date,PriceFindType = 0,DaysOffSet = 0): 

    CalcSpace    = acm.FStandardCalculationsSpaceCollection()
    Price        = 0.0
    Calendar     = acm.FCalendar['ZAR Johannesburg']
    AdjustedDate = Calendar.AdjustBankingDays(Date, DaysOffSet)
    if not acm.Time.DateDifference(AdjustedDate, acm.Time.DateToday()):
        Price = Instrument.Calculation().MarketPrice(CalcSpace, AdjustedDate, False, None, False, acm.FParty['internal'], True, PriceFindType, 1).Number()
        if str(Price) == str(acm.Math.NotANumber()):
            Price = Instrument.Calculation().MarketPrice(CalcSpace, AdjustedDate, False, None, False, acm.FParty['SPOT'], True, PriceFindType, 1).Number()
    else:
        Price = Instrument.Calculation().MarketPrice(CalcSpace, AdjustedDate, False, None, False, acm.FParty['internal'], True, PriceFindType, 1).Number()
    if str(Price) == str(acm.Math.NotANumber()):
        #raise acm.Log("Failed to get price bid / ask price in market for "  + str(e))
        Price = 0.0  #MKLIMKE might be better to trow an exception here??
    return Price
'''================================================================================================
Can Improve this by using Calculation Space
PLPos
================================================================================================'''
def Position(Portfolio, Instrument, Date):
    Pos = 0.0
    dt  = ael.date(Date)
    dt  = dt.add_banking_day(ael.Instrument['ZAR'], -1)
    for Trade in Portfolio.Trades():
        if Trade.Instrument() == Instrument and Trade.Status()  in INCLUDED_TRADE_STATUS:
            if dt >=  ael.date(acm.Time.AsDate(Trade.TradeTime())):
                Pos += Trade.Quantity()
    return Pos
'''================================================================================================
Get Rid of ael...
================================================================================================'''
def FundingRate(aelPortfolioSwap, Portfolio, Security, Date):

    try:
        FRateIndex  = acm.FRateIndex[aelPortfolioSwap.add_info('PSONPremIndex')]
        UndPrice    = 0.0
        Spread      = 0.0
        Pos         = Position(Portfolio, Security, Date)
        if FRateIndex.Underlying() == None:
            return Price(FRateIndex, Date, 0, -1)
        else:
            if Pos > 0:
                Spread  = Price(FRateIndex, Date, 2, -1)   #ASK
            else:
                Spread  = Price(FRateIndex, Date, 1, -1)   #BID
            UndPrice    = Price(FRateIndex.Underlying(), Date, 0, -1)
            if DEBUG:
                print '-----------------------------------------------------'
                print 'Portfolio Swap       = ' + aelPortfolioSwap.insid
                print 'Security             = ' + Security.Name()
                print 'Base Rate            = ' + str(UndPrice) 
                print 'Spread               = ' + str(Spread)
                print 'Date                 = ' + str(Date)
                print '-----------------------------------------------------'
                
    except Exception, e:
    
        acm.Log("Failed to get Funding Rate please check RateIndex"  + str(e))
        raise e

    return Spread + UndPrice
'''================================================================================================
This should be done on Instrument level rather, using CalculationSpace
Performnace can be improved 
'TotalInvest' 
================================================================================================'''
def ExecutionFee(aelPortfolio, security, date):
    executionFee = 0.0
    
    try:
        for trade in aelPortfolio.Trades():
            if trade.Instrument() == security and trade.Status() in INCLUDED_TRADE_STATUS:
                if ael.date(date) ==  ael.date(acm.Time.AsDate(trade.TradeTime())):
                    executionFee += PS_new_fees.execution_fee_on_tree(trade)

    except Exception, e:
        acm.Log("Failed to get Execution Fee"  + str(e))
        raise e      
    return executionFee


def DividendSuppression(aelPortfolio, security, date):
    dividendSuppression = 0.0
    
    try:
        for trade in aelPortfolio.Trades():
            if trade.Instrument() == security and trade.Status() in INCLUDED_TRADE_STATUS:
                for p in trade.Payments():
                    if p.Type() == "Dividend Suppression" and ael.date(date) ==  ael.date(acm.Time.AsDate(p.PayDay())):
                        dividendSuppression += p.Amount()

    except Exception, e:
        acm.Log("Failed to get dividend suppression payment"  + str(e))
        raise e      
    return dividendSuppression
'''================================================================================================
================================================================================================'''
def CalculatePerPortfolioFixingData(calcSpace, treeNodeStockPortfolio, calculateFundingAmount, calculateExecutionFee, calculateRPL):
    result = {}
    if calculateFundingAmount:
        result["ID_PER_PORTFOLIO_FUNDING_AMOUNT"]       = 0.0
        result["ID_PER_PORTFOLIO_FUNDING_RATE"]         = 0.0
    if calculateExecutionFee:
        result["ID_PER_PORTFOLIO_EXECUTION_FEE"]        = 0.0
    if calculateRPL:
        result["ID_PER_PORTFOLIO_RPL"]                  = 0.0
    return result
'''================================================================================================
TOD0:
    Remove portfolio parameter from this
    Convert getTimeSeriesValue to acm so that it does not fail here
================================================================================================'''
def RepoRate(PortfolioSwap, Portfolio, Security, Date):
    try:
        Type                = PortfolioSwap.add_info('PSShortPremiumType')
        ShortPremRate       = float(get_timseries_value(PortfolioSwap, 'PSShortPremRate', ael.date(Date).add_days(-1)))
        if DEBUG:
            print 'Short Rate -------'
            print 'PortfolioSwap = ' + str(PortfolioSwap)
            print 'ShortPremRate = ' + str(ShortPremRate)            
            print 'ShortPremRate-------'
        if str(Type) == 'Fixed':
            return ShortPremRate
        else:
            RI          = acm.FRateIndex[Security.add_info('PSShortPremCost')]  #Note: get rateindex
            FloatRate   = Price(RI, Date, 0, -1)                                   #Note: Previous Business Days Rate
            return ShortPremRate + FloatRate
    except Exception, e:
        acm.Log("Failed to get Repo Rate for %s on %s : %s" %(Security.Name(), Date, str(e)))        
        raise e
'''================================================================================================
================================================================================================'''
def get_timseries_value(aelEntity, timeSeriesName, aelDate):
  
    TimeSeriesSpec      = ael.TimeSeriesSpec[timeSeriesName]
    TempTimeSeries      = None

    for TimeSeries in ael.TimeSeries.select('ts_specnbr = ' + str(TimeSeriesSpec.specnbr)):

        TSEntity = eval('ael.' + TimeSeriesSpec.rec_type + '[' + str(TimeSeries.recaddr) + ']')

        if TimeSeries.day <= aelDate and TSEntity == aelEntity:

            if TempTimeSeries == None:

                TempTimeSeries = TimeSeries

            else:

                if TimeSeries.day > TempTimeSeries.day:  #NOTE: We want the latest one

                    TempTimeSeries = TimeSeries




    if TempTimeSeries == None:  
        if aelEntity.add_info(timeSeriesName):
            return aelEntity.add_info(timeSeriesName)
        else: 
            return 0.0 #TODO: rather raise an exceptions here
    else:
        return TempTimeSeries.value
'''================================================================================================
================================================================================================'''
def CalculatePerSecurityFixingData(fixingDate, aelPortfolioSwap, aelPortfolio,
                                   calcSpace, treeNodeSecurity, calculateFundingAmount,
                                   calculateExecutionFee, calculateRepo):

    result      = {}
    security    = treeNodeSecurity.Item().Instrument()
    pos         = Position(aelPortfolio, security, fixingDate)
    marketValue = (pos * Price(security, fixingDate, 0, -1) / 100.0) * -1.0
    
    result["ID_PER_SECURITY_DIVIDEND_SUPPRESSION"] = DividendSuppression(aelPortfolio, security, fixingDate)
    
    if calculateFundingAmount:
        result["ID_PER_SECURITY_FUNDING_AMOUNT"]                = marketValue #This should really be VAL? NO?
        result["ID_PER_SECURITY_FUNDING_RATE"]                  = FundingRate(aelPortfolioSwap, aelPortfolio, security, fixingDate)

    if calculateExecutionFee:
        result["ID_PER_SECURITY_EXECUTION_FEE"]                 = ExecutionFee(aelPortfolio, security, fixingDate)

    if calculateRepo:
        if pos < 0:
            result["ID_PER_SECURITY_REPO_AMOUNT"]               = marketValue
            result["ID_PER_SECURITY_REPO_FINANCING_RATE"]       = RepoRate(aelPortfolioSwap, aelPortfolioSwap, security, fixingDate)
        else:
            result["ID_PER_SECURITY_REPO_AMOUNT"]               = 0.0
            result["ID_PER_SECURITY_REPO_FINANCING_RATE"]       = 0.0
       
    return result
'''================================================================================================
================================================================================================'''
def CalculatePortfolioSwapFixingData(calcSpace, treeNodePortfolioSwap, calculateDepositAmount):
    result = {}
    if calculateDepositAmount:
        result["ID_PORTFOLIO_SWAP_DEPOSIT_AMOUNT"] = 0.0
    return result
'''================================================================================================
Convert these into one functions.....
Vely important DateDifference()
================================================================================================'''
def get_timseries_value_test(acmObject, timeSeriesName, aelDate):

    TimeSeriesSpec      = acm.FTimeSeriesSpec[timeSeriesName]
    TempTimeSeries      = None

    if TimeSeriesSpec != None:
        for TimeSeries in TimeSeriesSpec.TimeSeries():
            if TimeSeries.Recaddr() == acmObject.Oid():
            
                if TimeSeries.Day() <= aelDate: #Why ? 

                    if TempTimeSeries == None:
                        TempTimeSeries = TimeSeries
                    else:
                        if TimeSeries.Day() > TempTimeSeries.Day():
                            TempTimeSeries = TimeSeries

    if TempTimeSeries == None:    
        try:
            return float(acmObject.add_info(timeSeriesName))
        except Exception, e:
            acm.Log("Failed to get Addinfo"  + str(timeSeriesName))         
            return 0.0
    else:
        if ael.date(aelDate) == ael.date_today(): #MKLIMKE change to acm...
        #SG Mivhael Nikiforov, if add info is missing return 0.0
            try:
                return float(acmObject.add_info(timeSeriesName))
            except Exception, e:
                acm.Log("Failed to get Addinfo"  + str(timeSeriesName))         
                return 0.0
        else:
            # Front Upgrade 2013.3 -- Value amended to TimeValue; method name changed
            return TempTimeSeries.TimeValue()
'''================================================================================================
================================================================================================'''
def LegType(Leg):
    LegType = Leg.LegType()
    if LegType == "Total Return":
        return 'MTM'
    elif  LegType == "Call Fixed":             
        return 'Account'
    elif  LegType == "Fixed":
        if Leg.NominalScaling() == 'Dividend':
            return 'Dividend'
        else:
            return 'Execution Fee'
    else:
        if Leg.PayLeg():
            return 'Short Premium'
        else:
            return 'Overnight Premium'
    return None  
'''================================================================================================
NOTES:
    Return the compound portfolio if there is one, we need this because this is where a lot 
    of the settings are stored. The Portfolio will be the underlying of the portfolio swap
    we must take for granted that it could be a compound or physical.
    It was decided however that there will always be a compound portfolio.
    Need to think about this??
    Do we need the client statement
    
    Remember a physical can havemore then one compund
    
    Will theclinet name be the same as thecounterparty?
================================================================================================'''
def GetBasePortfolio(Portfolio):

    if Portfolio.Compound() == False:
        for MembersLink in Portfolio.MemberLinks():
            if MembersLink.OwnerPortfolio().add_info('PSClientName'):
                return MembersLink.OwnerPortfolio()
    else:
        #if Portfolio.add_info('PSClientName'):
        return Portfolio
    return None
'''================================================================================================
================================================================================================'''
def getFutureAdjustableCashFlows(leg, repDay):
    res = []
    for c in leg.CashFlows():
        if c.CashFlowType() in ('Fixed Amount', 'Interest Reinvestment') and c.PayDate() > repDay and c.PayDate <= leg.EndDate():
            if not (c.StartDate() and c.StartDate() <= repDay):
                res.append(c)
    return res
