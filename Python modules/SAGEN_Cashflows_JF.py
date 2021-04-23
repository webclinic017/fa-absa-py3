import ael, acm

#------------------------------------------------#
def FormattedValue(format):
    
    if (format == 0):
        return '0001-01-01'
    
    return '0.00'

#------------------------------------------------#
def CurrentCashFlow(leg, currentDate):
    
    if leg == None:
        return None
    else:
        try:
            currentDateS = ael.date_from_string(currentDate)
        except:
            # print '\n argument1 not in string format\n'
            currentDateS = currentDate
            
        for cashFlow in leg.cash_flows():
            if (cashFlow.start_day <= currentDateS) and (currentDateS < cashFlow.end_day):
                return cashFlow

    return None

#------------------------------------------------#
def PeriodRate(leg, currentDate, format, *rest):
    
    value = FormattedValue(format)
    cashFlow = CurrentCashFlow(leg, currentDate)
    if(cashFlow):
        if cashFlow.type in ('Caplet', 'Floorlet'):
            value = (str)(cashFlow.forward_rate()*100)
        else:
            value = (str)(cashFlow.period_rate(cashFlow.start_day, cashFlow.end_day))
    
    return value

#------------------------------------------------#
def ForwardRate(leg, currentDate, format, *rest):
    
    value = FormattedValue(format)
    cashFlow = CurrentCashFlow(leg, currentDate)
    if(cashFlow):
        value = (str)(cashFlow.forward_rate()*100)
    
    return value


#------------------------------------------------#
def PeriodDays(leg, currentDate, format, *rest):
    
    value = FormattedValue(format)
    cashFlow = CurrentCashFlow(leg, currentDate)
    if(cashFlow):

        start_day = cashFlow.start_day
        end_day = cashFlow.end_day
        
        if start_day == None:
            start_day = leg.start_day
        if end_day == None:
            end_day = leg.insaddr.exp_day   
 
        value = (str)(start_day.days_between(end_day, 'Act/365'))
    
    return value

#------------------------------------------------#
def NominalAmount(leg, currentDate, format, *rest):
    
    value = FormattedValue(format)
    cashFlow = CurrentCashFlow(leg, currentDate)
    if(cashFlow):

        # Should be multiplied by (t.quantity/i.index_factor) in the calling function
        nominalAmount = cashFlow.nominal_amount()
        if leg.payleg:
            nominalAmount = -1.0 * nominalAmount

        value = (str)(nominalAmount)
    
    return value

#------------------------------------------------#
def PayDay(leg, currentDate, *rest):
    
    value = FormattedValue(0)
    cashFlow = CurrentCashFlow(leg, currentDate)
    if(cashFlow):       
        value = (str)(cashFlow.pay_day)
    
    return value
    
#------------------------------------------------#
def StartDay(leg, currentDate, *rest):

    value = FormattedValue(0)
    cashFlow = CurrentCashFlow(leg, currentDate)
    if(cashFlow):
        if(cashFlow.start_day == None):
            return value

        value = (str)(cashFlow.start_day)
    
    return value


#----------#

def PayDay_DayPart(leg, currentDate, *rest):

    

    value = FormattedValue(0)

    cashFlow = CurrentCashFlow(leg, currentDate)
    print cashFlow

    if(cashFlow):

        payDay = cashFlow.pay_day

        #ymd = payDay.to_ymd()

        #d = ymd[2]

        #value = (str)(d)
        
        value = payDay.to_string('%d')

    

    return value
