
"""----------------------------------------------------------------------------- 
PURPOSE                 : Update - fixed strike calculation for asian ins.
REQUESTER               : Andrey Chechin 
DEVELOPER               : Eben Mare
CR NUMBER               : 498027 
-----------------------------------------------------------------------------""" 

import ael
import acm

CALC_SHEET = "FPortfolioSheet"

def getGreeks(instr, prfnbr, greeks, *rest):
    greeksToCalc = greeks.split('::')

    results = []
    for grk in greeksToCalc:
        tmpGrk = grk.split("|")
        instrument, portfolio, metric, context = acm.FInstrument[instr.insid], acm.FPhysicalPortfolio[prfnbr], tmpGrk[0], tmpGrk[1]
        eval = calcRiskMetric(instrument, portfolio, metric)        
        results.append(eval and str(eval) or "0")

    return "::".join(results)

def getStrike(instr, *rest):
    yesterday = ael.date_today().add_banking_day(ael.Instrument["ZAR"], -1)
    evalDate = yesterday
    if isAsian(instr):
        isPerformance = getAdditionalInfo(instr, "Forward Start Type")
        if instr.exotic().average_strike_type != "Average":
            #If there is no averaging of strike then check if it is performance and calc strike immediately
            percentStrike = isPerformance and float(getAdditionalInfo(instr, "AsianInWeight")) or 1
            return percentStrike*instr.strike_price

        averageInFixings = getAverageInFixings(instr)
        if not averageInFixings:
            #if there are no in fixings then even though it has been specified as averaging 
            #strike, there is nothing to average...  get the strike off the trade
            return instr.strike_price

        #Check whether averaging is done
        lastFixingDate = averageInFixings[-1][0]
        if (lastFixingDate <= evalDate):
            #Strike has already been fixed - get it off of the trade if present else calculate average
            return instr.strike_price != 0 and instr.strike_price \
                                           or getAverageStrike(averageInFixings)
        else:
            #Either none or some of of the fixings have fixed - 
            #calculate forwards for unfixed future fixings and average
            calcForwardFixings(instr, evalDate, averageInFixings)
            averageStrike = getAverageStrike(averageInFixings)

        percentStrike = isPerformance and float(getAdditionalInfo(instr, "AsianInWeight")) or 1
        return percentStrike*averageStrike
    else:
        return instr.strike_price

def isAsian(instr):
    exotic = instr.exotic()
    return exotic and exotic.average_method_type == "Arithmetic" or False

def getAverageInFixings(instr):
    '''Returns a sorted list of dates:fixings'''
    fixingsMap = []
    for event in instr.exotic_events():
        if event.type == "Average strike":
            fixingsMap.append([event.date, event.value])
    fixingsMap.sort(lambda x, y: cmp(x[0], y[0]))
    return fixingsMap

def calcForwardFixings(instr, evalDate, fixings):
    underlyingInstr = instr.und_insaddr
    for index, event in enumerate(fixings):
        fixingDate = event[0]
        if fixingDate > evalDate:
            #Hasn't fixed yet so calculate the forward
            if fixingDate < evalDate:
                raise Exception("There is a fixing missing on the instrument %1" % instr.insid)
            fwd = forwardPrice(underlyingInstr, fixingDate)
            fixings[index][1] = fwd

def forwardPrice(instr, date):
    return instr.forward_price(date)

def getAverageStrike(fixings):
    fixedValues = [fixing[1] for fixing in fixings]
    averageStrike = float(sum(fixedValues))/len(fixedValues)
    return averageStrike

def calcRiskMetric(instr, portfolio, metric):
    cs = acm.FCalculationSpace(CALC_SHEET)
    siat = acm.Risk.CreateSingleInstrumentAndTradesBuilder(portfolio, instr).GetTargetInstrumentAndTrades()
    calc = cs.CreateCalculation(siat, metric)
    return calc.Value().Number()

#Get an additional info field from an Arena Entity.
def getAdditionalInfo(entity, addInfo_fieldName):
    #get the specnbr for the additional info specification
    #as given by addInfo_fieldName
    spec_search = [ai for ai in ael.AdditionalInfoSpec \
                    if ai.field_name == addInfo_fieldName]
    if spec_search != []:
        #Get the value property from the add info table belonging
        #to entity
        lstReturn = [ai.value for ai in entity.additional_infos() \
                    if ai.addinf_specnbr == spec_search[0]]
        return lstReturn != [] and lstReturn[0] or None
