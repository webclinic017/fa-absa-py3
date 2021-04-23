'''
This Python script is used with ASQL Deriv_Cashflw_Rec.
    
Purpose                 :[Initial deployment],[Updated with Netted Amendments fix],[Added section to deal with dividends],[Added get_Port_Struct_from_Port],[Added TotalValEnd]
Department and Desk     :[PCG],[PCG],[PCG],[PCG],[Finance]
Requester:              :[Nick Bance],[Martin Kariuki],[Martin Kariuki],[Martin Kariuki],[Tshegofatso Phale]
Developer               :[Willie van der Bank],[Willie van der Bank],[Willie van der Bank],[Willie van der Bank],[Willie van der Bank],[Conicov Andrei]
CR Number               :[131939 12/04/2012],[CHNG0000210797 24/04/2012],[303927 2012-07-05],[354288 2012-07-27],[2013-02-07 782578],[2013-06-28]

Change 25/04/2016:
Faize adams             :Updated error handling in try block. Moved 'port = ael.Portfolio[portnbr]' inside try to prevent crashes when
                        it cant find the portfolio referenced by the portnbr variable.
'''

import acm, ael
from SAGEN_IT_Functions import get_Port_Struct

global count

def TopParentSeq(temp, seq, *rest):
    ID = 0
    seq = acm.FSettlement[seq]
    while seq.Parent():
        seq = seq.Parent()
        ID = seq.Oid()
    if ID != 0:
        if acm.FSettlement[ID].CashFlow():
            ID = 0
    return ID
    
def SettlemStatus(temp, seq, *rest):
    ParSeq = acm.FSettlement[TopParentSeq(1, seq)]
    seq = acm.FSettlement[seq]
    try:
        if ParSeq.Trade():  # This will be the case for a simple net involving only one trade
            # This will be true for amended settlements.
            Status = ParSeq.Status()
        else:  # This will be the case for a complicated net involving multiple trades
            Status = seq.Status()
    except:
        Status = seq.Status()
    return Status

def ExDivDate(temp, trd, *rest):
    acmtrd = acm.FTrade[trd]
    Date = ael.date(acmtrd.ValueDay())
    ExDivDate = Date
    DateAdjust = acmtrd.Instrument().Ex_coup_period_count()
    
    try:
        if acmtrd.Instrument().Ex_coup_period_unit() == 'Days':
            ExDivDate = acm.Time.DateAddDelta(Date, 0, 0, DateAdjust)
        elif acmtrd.Instrument().Ex_coup_period_unit() == 'Months':
            ExDivDate = acm.Time.DateAddDelta(Date, 0, DateAdjust, 0)
        elif acmtrd.Instrument().Ex_coup_period_unit() == 'Years':
            ExDivDate = acm.Time.DateAddDelta(Date, DateAdjust, 0, 0)
        else:
            print 'Error calculating ExDivDate'
    except:
        print 'Error calculating ExDivDate'
        
    return ExDivDate

def get_underlyingInsType(temp, trdnbr, *rest):
    uins = None
    t = ael.Trade[trdnbr]
    if t.insaddr.instype == 'TotalReturnSwap':
        iLegs = t.insaddr.legs()
        for iLeg in iLegs:
            if iLeg.type == 'Total Return':
                uins = iLeg.index_ref.instype
    return uins

def DailyEndCash(temp, trd, Date, *rest):
    try:
        t = acm.FTrade[trd]
        calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', Date)
        Calc = calc_space.CalculateValue(t, 'Portfolio Accumulated Cash Daily')
        Cash = Calc.Value().Number()
        return Cash
    except:
        return 0.0
        
def TotalEndCash(temp, trd, Date, *rest):
    try:
        t = acm.FTrade[trd]
        calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
        Calc = calc_space.CalculateValue(t, 'ZAR Cash')
        Cash = Calc.Value().Number()
        return Cash
    except:
        return 0.0
        
def TotalValEnd(temp, trd, Date, *rest):
    try:
        t = acm.FTrade[trd]
        calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', Date)
        Calc = calc_space.CalculateValue(t, 'Total Val End')
        Cash = Calc.Value().Number()
        return Cash
    except:
        return 0.0
  
# For historic dividends
def get_underlyingDividend(temp, trdnbr, start_day, end_day, *rest):
    val = 0.0
    t = ael.Trade[trdnbr]
    ins = t.insaddr
    if ins.instype == 'Stock':
        val = get_dividend('', ins, start_day, end_day) * t.quantity
            
    elif ins.instype == 'EquityIndex':
        for cl in ins.combination_links():
            # val = val + get_dividend('', cl.member_insaddr, start_day, end_day) * cl.weight / uins.index_factor
            val = val + get_dividend('', cl.member_insaddr, start_day, end_day) * cl.weight
    if t.quantity < 0:
        val = val * -1
    return val
    
def get_dividend(temp, i, start_day, end_day, *rest):
    val = 0.0    
    divs = i.historical_dividends()
    # print i.insid
    for div in divs:
        # print div.pay_day
        # if div.ex_div_day > start_day and div.ex_div_day < end_day:
        if div.pay_day >= start_day and div.pay_day <= end_day:
            val = val + div.dividend
    return val         

# For future dividends
def get_underlyingDividendEstimate(temp, t, start_day, end_day, *rest):
    val = 0.0
    t = ael.Trade[trdnbr]
    uins = t.insaddr
    if uins.instype == 'Stock':
        val = get_dividendEstimate('', uins, start_day, end_day)
            
    elif uins.instype == 'EquityIndex':
        for cl in uins.combination_links():
            # val = val + get_dividendEstimate('', cl.member_insaddr, start_day, end_day) * cl.weight / uins.index_factor
            val = val + get_dividendEstimate('', cl.member_insaddr, start_day, end_day) * cl.weight
    return val
    
def get_dividendEstimate(temp, i, start_day, end_day, *rest):   
    val = 0.0    
    divStreams = ael.DividendStream.select("insaddr = %s" % i.insaddr)
    for divStream in divStreams.members():
        # print divStream.name
        for divEst in divStream.estimates():
            # print divEst.pay_day
            # if divEst.ex_div_day > start_day and divEst.ex_div_day < end_day:
            if divEst.pay_day >= start_day and divEst.ex_div_day <= end_day:
                val = val + divEst.dividend
    return val   

# Function that calls the recursive portfolio tree climber function
# returns 1 if at least one of the specified portfolio match
def get_Port_Struct_from_Port(temp, portnbr, checkPorts, *rest):
    checkPort_list = checkPorts.split(',')
    match = 0
    for checkPort in checkPort_list:
        try:        
            port = ael.Portfolio[portnbr]
            portLink = ael.PortfolioLink.select('member_prfnbr=%i' % port.prfnbr)
            match = get_Port_Struct(portLink, checkPort)
        except:
            match = 0
        # if at least one match found, we can stop the search
        if match:
            return match
    return match
