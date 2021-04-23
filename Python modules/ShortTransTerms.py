import ael, time

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units     import cm
from zak_funcs               import formnum


def TransactionTerms(canvas, t):

    #--------------------------------------------------------------------------------#
    #                                   TRANSACTION TERMS
    #--------------------------------------------------------------------------------#
    TradeDate  = str(time.strftime('%d.%m.%Y', time.localtime(t.time)))
     
    Buyer  = ' '
    Seller = ' '    
    if t.quantity > 0:
        (Buyer, Seller)  = ('ABSA BANK LIMITED ', t.counterparty_ptynbr.fullname)
    else:
        (Buyer, Seller)  = (t.counterparty_ptynbr.fullname, 'ABSA BANK LIMITED ')
        
    CurrencyOptionStyle = t.insaddr.exercise_type
      
    PutCurrency            = ' '
    CallCurrency           = ' '
    CurrencyOptionType     = ' '
    PutCall                = ' '
    CallCurrencyAmount     = ' '
    CallPutAmount          = ' '
    CallPutTitle           = ' '
    PutAmount              = 0.0
    CallAmount             = 0.0
    
    if t.insaddr.call_option == 1:   #Call Option
        
        CallAmount = t.quantity
        PutCurrency, CallCurrency  = (t.insaddr.curr.insid, t.insaddr.und_insaddr.insid)
        CurrencyOptionType = PutCurrency+ ' ' + CallCurrency + ' ' + 'Call'
        PutCall = 'Call Currency'
        CallPutAmount = str(CallCurrency) +' '+str(formnum(abs(CallAmount)))
        CallPutTitle = 'Call Currency Amount'
        PutAmount, CallAmount = (t.quantity*t.insaddr.strike_price, t.quantity)
        
    elif t.insaddr.call_option == 0:  #Put Option
        
        PutAmount = t.quantity                  
        PutCurrency, CallCurrency  = (t.insaddr.und_insaddr.insid, t.insaddr.curr.insid)
        CurrencyOptionType =  PutCurrency+ ' ' + CallCurrency + ' ' + 'Put'
        PutCall = 'Put Currency'
        CallPutAmount  = str(PutCurrency)  +' '+ str(formnum(abs(PutAmount)))
        CallPutTitle = 'Put Currency Amount'
        PutAmount, CallAmount = (t.quantity, t.quantity*t.insaddr.strike_price)  
    
    CallCurrencyAmount = str(CallCurrency) +' '+str(formnum(abs(CallAmount)))
    PutCurrencyAmount  = str(PutCurrency)  +' '+ str(formnum(abs(PutAmount)))
    StrikePrice        = str(t.insaddr.strike_price)
    ExpirationDate     = str(t.insaddr.exp_day.to_string('%d.%m.%Y'))
    ExpirationTime     = '10:00 AM New York Time'
    
    # Settlement Date
    date   = t.insaddr.exp_day
    dts1   = date.add_banking_day(t.insaddr.curr, t.insaddr.pay_day_offset)
    dts2   = date.add_banking_day(t.insaddr.und_insaddr.curr, t.insaddr.pay_day_offset)
    
    SettlementDate = ' '
    if dts1 > dts2:
        SettlementDate = date.add_banking_day(t.insaddr.curr, t.insaddr.pay_day_offset).to_string('%d.%m.%Y')
    else:
        SettlementDate = date.add_banking_day(t.insaddr.und_insaddr.curr, t.insaddr.pay_day_offset).to_string('%d.%m.%Y')
    
    PremiumCurr    =  str(t.insaddr.und_insaddr.curr.insid)
    Premium        =  str(formnum(abs(t.premium)))
    PremiumAmount  =  PremiumCurr +' '+ Premium
    PremPayDay     =  t.value_day.to_string('%d.%m.%Y')
    
    #TRANSACTION TERMS STATIC DATA
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(1.5 * cm, 27.43*cm, '3.')               
    canvas.drawString(2.0 * cm, 27.43*cm, 'The terms of the Transaction to which this Confirmation relates are as folllows:')  
    canvas.drawString(2.0 * cm, 26.5*cm, 'Trade Date:')
    canvas.drawString(2.0 * cm, 25.5*cm, 'Buyer:')
    canvas.drawString(2.0 * cm, 24.5*cm, 'Seller:')
    canvas.drawString(2.0 * cm, 23.5*cm, 'Notional Amount:')
    canvas.drawString(2.0 * cm, 22.5*cm, 'Currency Option Style:')
    canvas.drawString(2.0 * cm, 21.5*cm, 'Currency Option Type:')
    canvas.drawString(2.0 * cm, 20.5*cm, PutCall+':')
    canvas.drawString(2.0 * cm, 19.5*cm, CallPutTitle +':')
    canvas.drawString(2.0 * cm, 18.5*cm, 'Strike Price:')
    canvas.drawString(2.0 * cm, 17.5*cm, 'Expiration Date:')
    canvas.drawString(2.0 * cm, 16.5*cm, 'Expiration Time:')
    canvas.drawString(2.0 * cm, 15.5*cm, 'Latest Exercise Time')
    canvas.drawString(2.0 * cm, 14.5*cm, 'Automatic Exercise:')
    canvas.drawString(2.0 * cm, 13.5*cm, 'Settlement Date:')
    canvas.drawString(2.0 * cm, 12.5*cm, 'Premium:')
    canvas.drawString(2.0 * cm, 12.0*cm, 'Premium Payment Date:')
    canvas.drawString(2.0 * cm, 11.0*cm, 'Event Currency:')
    canvas.drawString(3.5 * cm, 10.0*cm, 'Event Currency Buyer:')
    canvas.drawString(3.5 * cm,  9.5*cm, 'Event Currency Seller:')
    canvas.drawString(2.0 * cm,  8.5*cm, 'Disruption Events:')
    canvas.drawString(3.5 * cm,  8.0*cm, 'General Inconvertibility:')
    canvas.drawString(3.5 * cm,  7.5*cm, 'Specific Inconvertibility:')
    canvas.drawString(3.5 * cm,  7.0*cm, 'General Non-Transferability:')
    canvas.drawString(3.5 * cm,  6.5*cm, 'Specific Non-Transferability:')
    canvas.drawString(3.5 * cm,  6.0*cm, 'Inconvertibility/Non-Transferability:')
    canvas.drawString(3.5 * cm,  5.5*cm, 'Governmental Authority Default:')
    canvas.drawString(3.5 * cm,  5.0*cm, 'Nationalisation:')
    canvas.drawString(3.5 * cm,  4.5*cm, 'Material Change in Circumstance:')
    canvas.drawString(2.0 * cm,  4.0*cm, 'Calculation Agent Determination of')
    canvas.drawString(2.0 * cm,  3.5*cm, 'Disruption Event:')
    canvas.drawString(2.0 * cm,  3.1*cm, 'Maximum Days of Disruption:')
    
    #TRANSACTION TERMS
    canvas.drawString(9.0 * cm, 26.5*cm, TradeDate)
    canvas.drawString(9.0 * cm, 25.5*cm, Buyer)
    canvas.drawString(9.0 * cm, 24.5*cm, Seller)
    canvas.drawString(9.0 * cm, 23.5*cm, 'R '+formnum(abs(t.nominal_amount())))
    canvas.drawString(9.0 * cm, 22.5*cm, CurrencyOptionStyle)
    canvas.drawString(9.0 * cm, 21.5*cm, CurrencyOptionType)
    canvas.drawString(9.0 * cm, 20.5*cm, CallCurrency)
    canvas.drawString(9.0 * cm, 19.5*cm, CallPutAmount)
    canvas.drawString(9.0 * cm, 18.5*cm, StrikePrice)
    canvas.drawString(9.0 * cm, 17.5*cm, ExpirationDate+' '+'(subject to adjustment in accordance with the')
    canvas.drawString(9.0 * cm, 17.1*cm, 'Modified Following Business Day Convention)')
    canvas.drawString(9.0 * cm, 16.5*cm, '10:00 New York Time')
    canvas.drawString(9.0 * cm, 15.5*cm, '10:00 New York Time')
    canvas.drawString(9.0 * cm, 14.5*cm, 'Not Applicable')
    canvas.drawString(9.0 * cm, 13.5*cm, SettlementDate+' '+'(subject to adjustment in accordance with the')
    canvas.drawString(9.0 * cm, 13.1*cm, 'Modified Following Business Day Convention)')
    canvas.drawString(9.0 * cm, 12.5*cm, PremiumAmount)
    canvas.drawString(9.0 * cm, 12.0*cm, PremPayDay)
    canvas.drawString(9.0 * cm, 11.0*cm, 'ZAR')
    canvas.drawString(9.0 * cm, 10.0*cm, Buyer)
    canvas.drawString(9.0 * cm,  9.5*cm, Seller)
    canvas.drawString(9.0 * cm,  7.5*cm, 'Applicable')
    canvas.drawString(9.0 * cm,  7.0*cm, 'Applicable')
    canvas.drawString(9.0 * cm,  6.5*cm, 'Applicable')
    canvas.drawString(9.0 * cm,  6.0*cm, 'Applicable')
    canvas.drawString(9.0 * cm,  5.5*cm, 'Applicable')
    canvas.drawString(9.0 * cm,  5.0*cm, 'Applicable')
    canvas.drawString(9.0 * cm,  4.5*cm, 'Applicable')
    canvas.drawString(9.0 * cm,  8.0*cm, 'Applicable')
    canvas.drawString(9.0 * cm,  3.5*cm, 'Applicable')
    canvas.drawString(9.0 * cm,  3.1*cm, '2')
    canvas.showPage() 
