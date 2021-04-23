"""-----------------------------------------------------------------------------
Date:                   2010-02-04, 2010-02-18
Purpose:                Agris Dollar Exposure- For CBot and Cash Fx
Department and Desk:    FO Commodities
Requester:              Denzil Pieterse
Developer:              Zaakirah kajee
CR Number:              218003, 230247

History:

Date        CR Num   Who                      What
    
2010-04-22  288911  Paul Jacot-Guillarmod     Added the stringToDateTime function to convert a string
                                               to a datetime which is needed for the DenominatedValue
                                               function.
2010-06-01  333378  Rohan van der Walt        Added Additional Payments to Dollar Exposure calculation
                                               in getUSDExpforTrades()
2010-06-18  349842  Rohan van der Walt        Added agrisConvFactor()
2011-11-09  824593  Paul Jacot-Guillarmod / Rohan vd Walt Dollar Exp Factor Fix and Option Calculation
2012-01-12  863854  Rohan van der Walt        Excluding Simulated trades from calculation
-----------------------------------------------------------------------------"""

import ael, string, time, acm

usd = ael.Instrument['USD']

def stringToDateTime(date, format='%d/%m/%Y'):
    # Converts a string with a given format to a datetime
    dt = time.strptime(date, format)
    return acm.Time().LocalTimeAsUTCDays(dt.tm_year, dt.tm_mon, dt.tm_mday, 10, 0, 0, 0)
    
def getTrades(trades, startDate, endDate):
    newTrades = []
    invalidStatusses = ['Simulated']
    for trade in trades:
        if ael.date_from_time(trade.time) >= startDate  and  ael.date_from_time(trade.time) <= endDate and trade.status not in invalidStatusses:
            newTrades.append(trade)
    return newTrades
   

def getUSDExpforTrades(trades, startDate, endDate):
    
    filteredTrades = getTrades(trades, startDate, endDate)
    tradeSettled = 0
    tradeUnsettled = 0
    today = ael.date_today().to_string('%d/%m/%Y')
    data = {}
    results = acm.FArray()
    for trade in [t for t in filteredTrades if t.value_day >= ael.date_today()]:
        if trade.value_day > ael.date_today():
            if trade.value_day.to_string('%d/%m/%Y') in data.keys():
                data[trade.value_day.to_string('%d/%m/%Y')] += trade.quantity
            else:
                data[trade.value_day.to_string('%d/%m/%Y')] = trade.quantity
        else:
            tradeSettled += trade.quantity
        
        if trade.payments():
            for p in trade.payments():
                if p.curr == usd:
                    if p.payday > ael.date_today():
                        if p.payday.to_string('%d/%m/%Y') in data.keys():
                            data[p.payday.to_string('%d/%m/%Y')] += p.amount
                        else:
                            data[p.payday.to_string('%d/%m/%Y')] = p.amount
                    else:
                        tradeSettled += p.amount                    

    results.Add(acm.DenominatedValue(tradeSettled, 'USD', None, stringToDateTime(today)))
    for date, val in data.iteritems():
        results.Add(acm.DenominatedValue(val, 'USD', None, stringToDateTime(date)))
    
    return results
    
def getUSDExpforCBOT(trades, startDate, endDate, mprice):

    filteredTrades = getTrades(trades, startDate, endDate)
    UsdVal = 0
    data = {}
    today = ael.date_today().to_string('%d/%m/%Y')
    results = acm.FArray()
    for trade in filteredTrades :
        ins = acm.FInstrument[trade.insaddr.insid]
        UsdVal += trade.quantity* (mprice-trade.price)* trade.insaddr.contr_size * ins.Quotation().QuotationFactor()
        if trade.payments():
            for p in trade.payments():
                if p.curr == usd:
                    if p.payday > ael.date_today():
                        if p.payday.to_string('%d/%m/%Y') in data.keys():
                            data[p.payday.to_string('%d/%m/%Y')] += p.amount
                        else:
                            data[p.payday.to_string('%d/%m/%Y')] = p.amount
                    else:
                        UsdVal += p.amount
                        
    results.Add(acm.DenominatedValue(UsdVal, 'ZAR', None, stringToDateTime(today)))
    for date, val in data.iteritems():
        results.Add(acm.DenominatedValue(val, 'ZAR', None, stringToDateTime(date)))
    return results

def agrisConvFactor(origUnit, newUnit, commodity, *rest):
    if newUnit == "Tonnes":
        if origUnit == "Tonnes":
            return 1
        if origUnit == "Short Tonnes":
            return 1 / 1.1023
        if origUnit == "Pounds":
            return 1 / 2204.622
        if origUnit == "Ounces":        #Troy ounces
            return 1 / 311034.768
        if origUnit == "US Barrels":
            return 0                    #Just return 0 if trying to convert US Barrels to Tonnes
        if origUnit == "Bushels":
            if commodity == "Corn":
                return 1 / 39.3679
            if commodity == "White Maize":
                return 1 / 39.3679
            if commodity == "Wheat":
                return 0.027216
            if commodity == "Soya":
                return 0.027216

    return 1

def GetTheoreticalPrice(instrument):
    ''' Calculate the theoretical price for an instrument.
    '''
    calculationSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    calculation = instrument.Calculation()
    theoreticalPrice = calculation.TheoreticalPrice(calculationSpace)
    try:
        return theoreticalPrice.Number()
    except:
        return theoreticalPrice

def BumpUSDPrice(instrument, bumpValue):
    ''' Bump the USD price by bumpValue and return the theoretical price of the instrument
        after bumping.
    '''
    currUSD = ael.Instrument['USD']
    for price in currUSD.prices():
        if price.ptynbr.ptyid == 'SPOT' and price.curr.insid == 'ZAR':
            priceClone = price.clone()
            priceClone.settle = price.settle + bumpValue
            priceClone.last = price.last + bumpValue
            priceClone.bid = price.bid + bumpValue
            priceClone.ask = price.ask + bumpValue
            priceClone.apply()
            break
    
    theoreticalPrice = GetTheoreticalPrice(instrument)
    priceClone.revert_apply()
    
    return theoreticalPrice

def SimulateUnderlyingPrice(instrument, underlyingPrice):
    context = acm.GetDefaultContext()
    sheetType = 'FDealSheet'
    calculationSpace = acm.Calculations().CreateCalculationSpace(context, sheetType)
    calculationSpace.SimulateValue(instrument, 'Portfolio Underlying Price', underlyingPrice)
    theoreticalPrice = calculationSpace.CreateCalculation(instrument, 'Price Theor')
    try:
        return theoreticalPrice.Value().Number()
    except:
        return theoreticalPrice.Value()
    
def OptionDollarExposure(instrument, position):
    underlying = instrument.Underlying()
    bumpValue = 0.01
    
    underlyingTheorUp = BumpUSDPrice(underlying, bumpValue)
    theorUp = SimulateUnderlyingPrice(instrument, underlyingTheorUp)
    
    underlyingTheorDown = BumpUSDPrice(underlying, -bumpValue)
    theorDown = SimulateUnderlyingPrice(instrument, underlyingTheorDown)
    
    exposure = position * (theorUp - theorDown) / (2 * bumpValue)

    return acm.DenominatedValue(exposure, acm.FCurrency['ZAR'], acm.Time().DateToday())
    
