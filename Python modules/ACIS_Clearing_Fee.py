"""---------------------------------------------------------------------------------------------------------------
Project                 : ACIS Clearing Fee
Purpose                 : The brokerage fee amount to be booked daily for every business day, and the payday must be
                          the 10th business day of the following month. The purpose of the additional payment is to 
                          accrue for ACIS fee during the month
Department and Desk     : PCG - Commodities
Requester               : Suveshan, Iyaloo
Developer               : Tshepo Mabena
CR Number               : CHNG0000118532 
------------------------------------------------------------------------------------------------------------------"""

import acm, ael
from FSQL_functions import FirstBusinessDay

def TradeFilter():

    TradeFilterList = []
    for tf in acm.FTradeSelection.Select(''):
        TradeFilterList.append(str(tf.Name()))
    TradeFilterList.sort()
    
    return TradeFilterList
    
def _TotalAmount(temp,Qty,AbsaEq,Strate,Message,VAT,*rest):

    TotalCostBeforeVat = Qty*(AbsaEq + Strate + Message)
    VatAmt             = TotalCostBeforeVat* (VAT/100)
    TotalAmount        = VatAmt + TotalCostBeforeVat 
         
    return    round(TotalAmount*-1, 0)
    
def _AddPayment(temp,trade, amount,PayDay,Date,Rdate,*rest):
        
    party = acm.FParty['ABSA BANK INVESTOR SERVICES']
        
    try:  
        payment = acm.FPayment()
        payment.Trade(trade)
        payment.Party(party)
        payment.Type('Broker Fee')
        payment.Amount(amount)
        payment.Currency(acm.FInstrument['ZAR'])
        payment.PayDay(PayDay)
        payment.ValidFrom(Rdate)
        payment.Text('ACIS fee' + ' ' + Rdate.to_string()[8:10] + '/' + Rdate.to_string()[5:7])
        payment.Commit()   
 
    except Exception, e:
        print "Commit Failed"
        
    
ael_variables = [['TradeFilter', 'Trade Filter', 'string', TradeFilter(), 'ACIS_Fee_Trade', 1, 0, 'To run for a Trade Filter', None, 1],
                 ['Quantity', 'Quantity', 'int', None, '2', 1, 0, None, 1],
                 ['AbsaEquity', 'Absa Equity Transactions - On Market ', 'float', None, '160.0', 1, 0, None, 1],
                 ['Strate', 'Strate On Market ', 'float', None, '13.1', 1, 0, None, 1],
                 ['Message', 'Messaging Fee - On Market ', 'float', None, '4.76', 1, 0, None, 1],
                 ['VAT', 'VAT % ', 'float', None, '14.0', 1, 0, None, 1],
                 ['Date', 'Date', 'date', '', acm.Time().DateNow(), 1]]

def ael_main(parameters):

    Qty     = parameters['Quantity']
    AbsaEq  = parameters['AbsaEquity']
    Strate  = parameters['Strate']
    Message = parameters['Message']
    VAT     = parameters['VAT']
     
    TotalAmnt = _TotalAmount(1, Qty, AbsaEq, Strate, Message, VAT)
    
    Rdate = parameters['Date']
    
    Date = parameters['Date'].add_months(1)
    FDOM = FirstBusinessDay(1, Date)
    
    PayDay = FDOM.add_banking_day(ael.Instrument['ZAR'], 10)
    
    Tf = acm.FTradeSelection[parameters['TradeFilter']].Trades()
    
    for t in Tf:        
        Payment =_AddPayment(1, t, TotalAmnt, PayDay, Date, Rdate)
        
    print 'Commit successful'
