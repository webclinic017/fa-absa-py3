""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLFunctions.py"
from __future__ import print_function
import acm
import math
import datetime
from FACLUtils import IsProlongChild, IsRepoProlongChild
import FACLParameters as params

def internalNumber():
    if hasattr(params.CommonSettings, "internal"):
        return params.CommonSettings.internal
    else:
        print("'internal' attribute missing from FACLParameters.CommonSettings")
    
    return None
    
def moodysNumber():
    if hasattr(params.CommonSettings, "moodys"):
        return params.CommonSettings.moodys
    else:
        print("'moodys' attribute missing from FACLParameters.CommonSettings")
    
    return None
    
def standardAndPoorsNumber():
    if hasattr(params.CommonSettings, "standardAndPoors"):
        return params.CommonSettings.standardAndPoors
    else:
        print("'standardAndPoors' attribute missing from FACLParameters.CommonSettings")
    
    return None

def partyRating(party, index):
    if index == 1:
        rating = party.Rating1()
        return rating.Name() if rating else ''
    elif index == 2:
        rating = party.Rating2()
        return rating.Name() if rating else ''
    elif index == 3:
        rating = party.Rating3()
        return rating.Name() if rating else ''
    
    return None
    
def internalRating(party):
    index = internalNumber()
    return partyRating(party, index) if index else None

def moodysRating(party):
    index = moodysNumber()
    return partyRating(party, index) if index else None

def standardAndPoorsRating(party):
    index = standardAndPoorsNumber()
    return partyRating(party, index) if index else None


def FACLDayCount(dayCountMethod):
    st = str( dayCountMethod )
    return st.replace("/", "_")

def FACLPayRateType(legType): 
    if legType in ('Fixed', 'Total Return'):
        return legType
    elif legType in ('Zero Coupon Fixed', 'Fixed Accretive'):
        return 'Fixed'
    elif legType in ('Float', 'Capped Float', 'Floored Float',
                    'Collared Float', 'Reverse Float'):
        return "Floating"
    else:
        return "Undefined"

def FACLAmortSchedule(quantity, cashFlows):
    amortSchedule = []
    
    if cashFlows.Size() < 2:
        return amortSchedule    

    cashFlows.SortByProperty('EndDate')
    i = 0
    while i < (cashFlows.Size() - 1):
        diff = cashFlows.At(i).NominalFactor() - cashFlows.At(i+1).NominalFactor()
        diff = diff * quantity
        diff = round(diff, 8)
        if abs(diff) > 0: 
            date = FACLDateStringToCQSString(str(cashFlows.At(i).EndDate()))
            amort = [date, diff]
            amortSchedule.append(amort)
        i = i + 1 
    return amortSchedule

def FACLOutstandingPrincipal(quantity, cashFlows, profitAndLossEndDate):
    factor = 0.0
    cashFlows.SortByProperty('StartDate')
    for cashflow in cashFlows:
        if cashflow.CashFlowType() == "Fixed Amount":
            continue
        if cashflow.StartDate() > profitAndLossEndDate:
            # the case where no amortisation has occurred yet
            factor = 1.0
            break
        if cashflow.EndDate() > profitAndLossEndDate:
            # We have got the first cashflow with end date after the plEndDate
            factor = cashflow.NominalFactor()
            break
            
    return factor * quantity

def FACLDateStringToCQSString( dateStr ):
    if not dateStr or not dateStr.strip():
        return ''
    
    try:
        date = datetime.datetime.strptime(dateStr, '%Y-%m-%d')
    except ValueError:
        date = datetime.datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')
        
    return FACLDateToCQSString(date)

def FACLDateToCQSString(d):
    months=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    return d.strftime('%d{0}%Y'.format(months[d.month-1]))
    
def getODFRate(faclTradeObject):
    """
       if Buy:
            return most expensive rate
       if Sell:
            return cheapest rate
    """
    toReturn = None
    odfInstrument = faclTradeObject.Instrument()
    allPeriods = odfInstrument.ExerciseEvents()
    decorator = acm.FOdfDecorator(odfInstrument, None)
    
    if allPeriods:
        allRates = []
        for p in allPeriods:
            allRates.append(p.Strike())
            allRates.append(p.Strike2())
        
        quantity = faclTradeObject.Quantity() if decorator.IsCallOption() else -1 * faclTradeObject.Quantity()
        isBuy = quantity >= 0
        isPerUnitQuotation = odfInstrument.Quotation().QuotationType() == 'Per Unit'
        
        returnMax = (    isBuy and     isPerUnitQuotation) or\
                    (not isBuy and not isPerUnitQuotation)
        
        if bool(faclTradeObject.TradeProcess() & 268435456): # if DrawdownOffset
            returnMax = not returnMax
        
        if returnMax:
            toReturn = max(allRates)
        else:
            toReturn = min(allRates)
            

    return toReturn

def IsTransientCorrectionMaster(trade):
    return trade.CorrectionTrade() and trade != trade.CorrectionTrade()

def FACLUnwrapTradeActionOriginal(trade):
    if trade:
        # Correct trade
        if IsTransientCorrectionMaster(trade):
            return FACLUnwrapTradeActionOriginal(trade.CorrectionTrade())
        # Reprice
        elif trade.Type() == 'Reprice':
            return FACLUnwrapTradeActionOriginal(trade.Contract())
        # Close trade
        elif trade.Type() == 'Closing' or trade.Type() == 'Novated':
            return trade.Contract()
        # ODF Drawdown
        elif trade.IsDrawdownOffset():
            return trade.Contract()
        # FX prolong
        elif IsProlongChild(trade):
            prev = trade.TrxTrade()
            while (prev and prev != trade):
                trade = prev
                prev = trade.TrxTrade()
        # repo prolong
        elif IsRepoProlongChild(trade):
            prev = trade.Contract()
            while (prev and prev != trade):
                trade = prev
                prev = trade.Contract()    
                
    return trade

def FACLScalingFactor():
    return params.CommonSettings.scalingFactor

def FACLCallDepositBalance(cashflows):
    """
    Returns the balance as of acm.Time.DateToday()
    """
    today = acm.Time.DateToday()
    #sum all cashflows up until and including today
    balance = 0.0
    curr = None
    for cashflow in cashflows:
        if curr == None:
            curr = cashflow.Leg().Currency()
        
        if cashflow.PayDate() <= today:
            balance += cashflow.FixedAmount()
        else:
            if cashflow.FixedAmount() < 0.0 and cashflow.CashFlowType() != 'Redemption Amount':
                balance += cashflow.FixedAmount()
    
    return math.fabs(balance)
