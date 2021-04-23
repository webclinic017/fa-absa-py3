'''
Purpose: Created for CFD_Project to pull up collateral specific data.
Department: Collateral
Requester: Lisa Nel
Developer: Willie van der Bank
CR Number: (23/10/2010)
'''

import ael, acm, ABSAPortfolioSwapCustom

def Required_Margin(temp,prfid,End_Day,*rest):

    calc_space  = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', End_Day)
  
    Port = acm.FCompoundPortfolio[prfid]
    
    Calc    = calc_space.CalculateValue(Port, 'Required Margin')
    calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    try:
        return str(round(Calc, 2))
    except:
        return ''

def Available_Margin(temp,prfid,End_Day,*rest):

    calc_space  = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', End_Day)
 
    Port = acm.FCompoundPortfolio[prfid]

    Calc    = calc_space.CalculateValue(Port, 'Available Margin')
    calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    try:
        return str(round(Calc.Value().Number(), 2))
    except:
        return ''
    
def Available_Trading_Capacity(temp,prfid,End_Day,*rest):

    calc_space  = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', End_Day)
  
    Port = acm.FCompoundPortfolio[prfid]    
    
    Calc    = calc_space.CalculateValue(Port, 'Available Trading Capacity')
    calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    try:
        return str(round(Calc, 2))
    except:
        return ''
    
def GetInstrumentPosition(PortfolioSwap, Instrument, Date):  
    for Leg in PortfolioSwap.Legs():
        if ABSAPortfolioSwapCustom.LegType(Leg) == 'MTM' and Leg.IndexRef() == Instrument:  
           Reset = GetReset(Leg.CashFlows()[0], 'Nominal Scaling', Date)
           if Reset != None:
                return Reset.FixingValue()
           else:
                return 0.0
    return 0.0  

def GetReset(CashFlow, Type, Date):
    for Reset in CashFlow.Resets():
        if Reset.ResetType() == Type and not acm.Time.DateDifference(Date, Reset.Day()):
            return Reset
    return None

def ClosingMarketExposure(PortfolioSwap, ClosingDate):
    TotalClosingMarketExposure  = 0.0
        
    for Leg in PortfolioSwap.Legs():
        if ABSAPortfolioSwapCustom.LegType(Leg) == 'MTM':  
            Instrument          = Leg.IndexRef()
            ClosingPrice        = ABSAPortfolioSwapCustom.Price(Instrument, ClosingDate)
            
            ClosingPosition             = GetInstrumentPosition(PortfolioSwap, Instrument, ClosingDate)
            ClosingExposure             = (ClosingPosition * ClosingPrice)/100
            TotalClosingMarketExposure  = TotalClosingMarketExposure + ClosingExposure
            
    return TotalClosingMarketExposure
    
def YMtM(temp,insid,Date,*rest):
    PortfolioSwap = acm.FPortfolioSwap[insid]
    ClosingDate = ael.date(Date)
    try:
        return str(round(ClosingMarketExposure(PortfolioSwap, ClosingDate), 2))
    except:
        return ''
