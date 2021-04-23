import acm

def GetPayments(tradesInPosition, dateMin, dateMax, paymentDayComparisonRule, paymentType):
    ''' Returns all the payments of the specified type in the specified time interval'''
    
    result = []
    for t in tradesInPosition:
        result.extend([payment for payment in t.Payments() if payment.Type() == paymentType])
      
    if paymentDayComparisonRule == 'validFromDay':
        result = [payment for payment in result if dateMin <= payment.ValidFromDay() <= dateMax]
    elif paymentDayComparisonRule == 'payDay':
        result = [payment for payment in result if dateMin <= payment.PayDay() <= dateMax]
    else:
        raise Exception('Unexpected paymentDayComparisonRule {0}'.format(paymentDayComparisonRule))
    
    return result
