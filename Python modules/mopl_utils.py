import acm

"""================================================================================================
================================================================================================"""
dt = acm.Time().DateToday()
smalldt = acm.Time().SmallDate()    
cs_ts = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
"""================================================================================================
================================================================================================"""

def GetFxRate(bccy, fccy):

    if fccy == bccy:
        return 1.0

    date = acm.Time.DateToday()
    fcurr = acm.FCurrency[fccy]
    bcurr = acm.FCurrency[bccy]


    currBase = acm.FCurrency['USD']


    try:
        fx_ccyusd = fcurr.Calculation().FXRate(cs, currBase, date).Number()
    except BaseException as ex:
        log(LogLevel.ERROR, ex)
        fx_ccyusd = inf 

    if currBase == bcurr:
        fx_zarusd = 1
    else:
        fx_zarusd = currBase.Calculation().FXRate(cs, bcurr, date).Number()

    fx = fx_ccyusd * fx_zarusd

    return fx


def getCurrentNominal(trade, curr, calc_space):
    vector = acm.FArray()
    param = acm.FNamedParameters()
    param.AddParameter('currency', curr)    
    vector.Add(param)
    column_config = acm.Sheet.Column().ConfigurationFromVector(vector)
    # The column_config can be ignored, if nominal should be in the same currency as the trade. 
    nominal = calc_space.CreateCalculation(trade, 'Current Nominal', column_config).Value()
    
    return nominal



def moplPresentValue(trd):

    ins = trd.Instrument()
    insccy =  ins.Currency().Name()

    if ins.InsType() == "Portfolio Swap":
        cs_ts.SimulateValue(trd, 'Portfolio Currency', 'ZAR')
        pv =  cs_ts.CalculateValue(trd, 'Total Val End').Number()
        cs_ts.RemoveSimulation(trd, 'Portfolio Currency')

        return pv
    else:
 
        feeTrade = (trd.AdditionalInfo().Funding_Instype() == 'IRD Funding')
        isCall = (ins.InsType() == "Deposit" and ins.OpenEnd() == "Open End")
        forwardStart = (trd.AcquireDay() > acm.Time.DateToday())
        fwdMaturity = (ins.ExpiryDate() > acm.Time.DateToday())
        nominalInsType = ins.InsType() in ["SecurityLoan",  "Swap", "FRA" ]
        nominal = 0.0
        nominalRequired = (not nominalInsType and not isCall and fwdMaturity and not forwardStart and not feeTrade)
        fx_rate = GetFxRate('ZAR', insccy)

        cs_ts.SimulateValue(trd, 'Portfolio Currency', insccy)
        if nominalRequired : 
            nominal = getCurrentNominal(trd, insccy, cs_ts) #This return float and not denomiated value 

        if isCall: 
            balance_column_id = 'Deposit balance' if acm.ShortVersion() == '2014.4.8' else 'Balance'
            nominal = -1 * cs_ts.CalculateValue(trd, balance_column_id).Number()        

        accrued = cs_ts.CalculateValue(trd, 'Portfolio Accrued Interest').Number() 
        cs_ts.RemoveSimulation(trd, 'Portfolio Currency')

        return (accrued + nominal) * fx_rate
