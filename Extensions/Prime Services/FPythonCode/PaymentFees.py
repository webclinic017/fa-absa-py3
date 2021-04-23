"""-----------------------------------------------------------------------
MODULE
    PaymentFees

DESCRIPTION

    Date                : 2012-09-19
    Purpose             : Returns the payment fees of a trade
    Department and Desk : Prime Services
    Requester           : Danilo Mantoan
    Developer           : Nidheesh Sharma
    CR Number           : 556348

ENDDESCRIPTION

HISTORY
    Date:       CR Number:      Developer:              Description:
    2013-03-19  C885651         Nidheesh Sharma         Excluded INS, SET, Brokerage fees from OtherFee
    2014-03-12  C1819376        Hynek Urban             Refactor & minor bug fix of other fees.
    2018-11-22  1001164411      Ondrej Bahounek         ABITFA-5622: Convert Other Fees to trade currency.
    2018-11-28                  Jaco Swanepoel          Payment migration: convert cash payments to appropriate new additional payment types.

-----------------------------------------------------------------------"""

import acm


FX_COLUMN_ID = 'FX Rate On Display Curr'
CS = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
ZAR_CUR = acm.FCurrency['ZAR']

PAYMENT_TYPES_TO_EXCLUDE = ('Premium', 
                            'Dividend Suppression', 
                            'INS', 
                            'SET', 
                            'Brokerage Vatable',
                            'Execution Fee',
                            'Aggregated Settled',
                            'Aggregated Accrued',
                            'Aggregated Funding',
                            'Aggregated Dividends',
                            'Aggregated Depreciation',
                            'Aggregated Future Settle',
                            'Aggregated Forward Funding PL',
                            'Aggregated Cash Open Value',
                            'Aggregated Cash Position',
                            'Aggregated Forward Premium',
                            'Aggregated Forward Settled',
                            'Aggregated Forward Dividends',
                            'Aggregated Forward Position')

PAYMENT_TEXTS_TO_EXCLUDE = ('Execution', 'ExecutionFee', 'INS', 'SET', 'Brokerage')

def ReturnOtherFee(trade, val_date):
    """
    Return the sum of all fees of a trade up to the specified date.
    
    Fees of type Execution Fee, INS, SET and Brokerage and any payments of type
    Aggregated Settled are excluded.

    """
                                
    CS.SimulateGlobalValue('Valuation Date', val_date)
    CS.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    CS.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', val_date)
    sumOfOtherFees = 0
    
    if trade.Status() not in ('Void'):
        payments = trade.Payments()
        for payment in payments:
            if payment.Type() in PAYMENT_TYPES_TO_EXCLUDE or\
                payment.Text() in PAYMENT_TEXTS_TO_EXCLUDE:
                continue
            if payment.ValidFrom() > val_date:
                continue
            
            amount = payment.Amount()
            
            if ZAR_CUR.Name() != payment.Currency().Name():
                
                # Ondrej's note:
                # Convert all non-ZAR payments to ZAR.
                # This should be ideally converted to trade currency,
                # but then many other attributes need to be changed and well tested.
                # This is just a fix to accommodate Futs on FXs by the end of the month.
                
                CS.SimulateValue(ZAR_CUR, "Portfolio Currency", payment.Currency())
                fx_rate = CS.CreateCalculation(ZAR_CUR, FX_COLUMN_ID).Value().Number()
                amount *= fx_rate
                
            sumOfOtherFees += amount
    
    return acm.DenominatedValue(sumOfOtherFees, ZAR_CUR.Name(), None, val_date)


#Function to return termination fee of a trade
def ReturnTerminationFee(trade):
    terminationFee = 0
    if trade.Status() in ('Terminated'):
        payments = trade.Payments()
        for payment in payments:
            if payment.Type() in ('Cash') and ('Termination' in payment.Text() or 'Terminated' in payment.Text()):
                terminationFee = terminationFee + payment.Amount()
            elif payment.Type() in ('Termination Fee'):
                terminationFee =  terminationFee + payment.Amount()
    return terminationFee


#Function to return termination fee date of a trade
def ReturnTerminationFeeDate(trade):
    terminationDate = ''
    if trade.Status() in ('Terminated'):
        payments = trade.Payments()
        for payment in payments:
            if payment.Type() in ('Cash') and ('Termination' in payment.Text() or 'Terminated' in payment.Text()):
                terminationDate = payment.PayDay()
            elif payment.Type() in ('Termination Fee'):
                terminationDate =  payment.PayDay()
    return terminationDate


#Function to return termination fee date of a trade in the correct format from an array of dates
def ReturnSingleTerminationFeeDate(arrayOfDates):
    terminationDate = ''
    for date in arrayOfDates:
        if date != '' and isinstance(date, str):
            dateFormatter = acm.FDateFormatter('dateFormatter')
            dateFormatter.FormatDefinition("%d/%m/%Y")
            terminationDate = dateFormatter.Format(date)#.replace('-','/')
            break
    return terminationDate
