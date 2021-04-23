'''
This module builds Swap advice Note in pdf

Changes
Date            Change Number   Developer         Description
02/10/2009                      Tshepo Mabena     Initial deployment
2017                            Willie vd Bank    2017 FA upgrade - Reset start and end dates are not populated anymore
'''

import ael, acm, os, time, re
import reportlab.lib.pagesizes

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import *
from reportlab.lib.units     import cm
from STATIC_TEMPLATE         import BuildLogos, BuildAdviceFooter
from reportlab.lib.colors    import black 
from zak_funcs               import formnum

def SingleWeightedAdviceStatic(temp,canvas,t,*rest): 
    
    #Builds Header and Footer
    BuildLogos(canvas)
    BuildAdviceFooter(canvas)

    # Counterparty Address Details    
    Attention = t.counterparty_ptynbr.attention
    Address   = t.counterparty_ptynbr.address
    Address2  = t.counterparty_ptynbr.address2
    Zipcode   = t.counterparty_ptynbr.zipcode
    City      = t.counterparty_ptynbr.city
    Fax       = t.counterparty_ptynbr.fax
        
    CP        = t.counterparty_ptynbr.fullname    
    Our_Ref   = t.trdnbr
        
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(1.0*cm, 25.0*cm, str(Our_Ref))  
    canvas.drawString(1.0*cm, 24.5*cm, CP)
    canvas.drawString(1.0*cm, 24.0*cm, Address)
    canvas.drawString(1.0*cm, 23.5*cm, Address2)
    canvas.drawString(1.0*cm, 23.0*cm, str(Zipcode))
    canvas.drawString(1.0*cm, 22.5*cm, City)
    canvas.drawString(1.0*cm, 22.0*cm, Attention)
    canvas.drawString(1.0*cm, 21.5*cm, 'FAX NO.'+ Fax)
    canvas.drawString(1.0*cm, 20.5*cm, 'Dear Sirs')
    
    canvas.drawString(8.0*cm, 20.0*cm, 'ADVICE OF INTEREST RATE SWAP RESET')
    
    canvas.drawString(1.0*cm, 19.0*cm, 'The terms of the particular Transaction to which this Advice relates are as follows:')
    
    canvas.drawString(1.0*cm, 18.0*cm, 'Our Reference')
    canvas.drawString(1.0*cm, 17.5*cm, 'Notional Amount')
    canvas.drawString(1.0*cm, 17.0*cm, 'Trade Date')
    
    canvas.drawString(1.0*cm, 16.0*cm, 'Effective Date')
    canvas.drawString(1.0*cm, 15.0*cm, 'Fixed Rate')
    canvas.drawString(1.0*cm, 15.5*cm, 'Fixed Rate Payer')
    canvas.drawString(1.0*cm, 14.5*cm, 'Fixed Payment Date')
    canvas.drawString(1.0*cm, 14.0*cm, 'Period. (days)')
    canvas.drawString(1.0*cm, 13.5*cm, 'Fixed Payment')
    
    canvas.drawString(1.0*cm, 12.5*cm, 'Effective Date')
    canvas.drawString(1.0*cm, 12.0*cm, 'Floating Rate Payer')
    canvas.drawString(1.0*cm, 11.5*cm, 'Floating Rate')
    canvas.drawString(1.0*cm, 11.0*cm, 'Floating Payment Date')
    canvas.drawString(1.0*cm, 10.5*cm, 'Period. (days)')
    canvas.drawString(1.0*cm, 10.0*cm, 'Floating Payment')
    
    canvas.drawString(1.0*cm, 9.0*cm,  'Net Payment')
    
    canvas.drawString(1.0*cm, 8.0*cm,  'Please confirm that the aforegoing correctly sets out the terms of our agreement by signing and returning a copy of this advice to ourselves at fax number')
    canvas.drawString(1.0*cm, 7.6*cm,  '(011) 895 7822 or advise us of any discrepancies at telephone number (011) 895 6837.')
    
    canvas.drawString(1.0*cm, 7.0*cm, 'For and on behalf of')
    canvas.drawString(1.0*cm, 6.5*cm, CP)
    canvas.drawString(1.0*cm, 5.5*cm, '_'*40)
    canvas.drawString(1.0*cm, 5.0*cm, 'THIS CONFIRMATION IS ELECTRONICALLY GENERATED AND REQUIRES NO SIGNATURE BY ABSA BANK LIMITED.')

    return canvas
    
def BuildSingleWeightedAdvice(temp,t,date,canvas,*rest):    
    
    Our_Ref   = t.trdnbr
    Your_Ref  = t.your_ref
    Curr      = t.display_id('curr')
    TradeDate = ael.date_from_time(t.time)
    
    Notional = t.nominal_amount()
   
    # ########################## Fixed Leg ##################################            
    FixedEffectiveDate = ''
    FixedPaymentDate   = ''
    FixedRate          = 0.0
    Days_Fixed         = 0
    FixedPayment       = 0.0
       
    for cf in t.insaddr.cash_flows():
        for r in cf.resets():
            if date == r.end_day or date == cf.end_day:
                if r.type in ('Weighted'):
                    FixedEffectiveDate = cf.start_day.to_string('%Y-%m-%d')
                    FixedRate          = cf.period_rate(cf.start_day, cf.end_day)
                    FixedPayment       = cf.projected_cf()*t.quantity
                    FixedPaymentDate   = cf.pay_day.to_string('%Y-%m-%d')
                    Days_Fixed         = int(cf.start_day.days_between(cf.end_day))
                    
    # ########################## Floating Leg ################################## 
    FloatEffectiveDate = ''
    FloatingRate       = 0.0
    FloatPayment       = 0.0
    FloatPaymentDate   = ''
    Days_Float         = 0
                
    for cf in t.insaddr.cash_flows():
        for r in cf.resets():
            if date == r.end_day or date == cf.end_day:
                if r.type in ('Single'):
                    FloatEffectiveDate = cf.start_day.to_string('%Y-%m-%d')
                    FloatingRate       = cf.period_rate(cf.start_day, cf.end_day)
                    FloatPayment       = cf.projected_cf()*t.quantity
                    FloatPaymentDate   = cf.pay_day.to_string('%Y-%m-%d')
                    Days_Float         = int(cf.start_day.days_between(cf.end_day))                
                 
    NettPayment  = FixedPayment + FloatPayment
    
    usyou         = ''
    if NettPayment > 0:
        usyou     = 'Us'
    else:
        usyou     = 'You'    
        
    FixedPayer = ''  
    FloatPayer = '' 
 
    if t.nominal_amount() < 0:
        FixedPayer = t.counterparty_ptynbr.fullname 
        FloatPayer = 'ABSA BANK LIMITED'
    else:
        FixedPayer = 'ABSA BANK LIMITED'
        FloatPayer = t.counterparty_ptynbr.fullname 
    
    
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(6.0*cm, 18.0*cm, ': '+ str(Our_Ref))
    canvas.drawString(6.0*cm, 17.5*cm, ': '+ Curr+' '+ str(formnum(Notional)))
    canvas.drawString(6.0*cm, 17.0*cm, ': '+ str(TradeDate))
        
    canvas.drawString(6.0*cm, 16.0*cm, ': '+ FixedEffectiveDate)
    canvas.drawString(6.0*cm, 15.5*cm, ': '+ FixedPayer)
    canvas.drawString(6.0*cm, 15.0*cm, ': '+ str(FixedRate)+ ' ' + '%' + ' ' + '(yield)')
    canvas.drawString(6.0*cm, 14.5*cm, ': '+ FixedPaymentDate)
    canvas.drawString(6.0*cm, 14.0*cm, ': '+ str(Days_Fixed))
    canvas.drawString(6.0*cm, 13.5*cm, ': '+ Curr + ' ' + formnum(abs(FixedPayment)))
    
    canvas.drawString(6.0*cm, 12.5*cm, ': '+ FloatEffectiveDate)
    canvas.drawString(6.0*cm, 12.0*cm, ': '+ FloatPayer)
    canvas.drawString(6.0*cm, 11.5*cm, ': '+ str(FloatingRate)+ ' ' + '%' + ' '+ '(yield)' )
    canvas.drawString(6.0*cm, 11.0*cm, ': '+ FloatPaymentDate)
    canvas.drawString(6.0*cm, 10.5*cm, ': '+ str(Days_Float))
    canvas.drawString(6.0*cm, 10.0*cm, ': '+ Curr + ' ' + formnum(abs(FloatPayment)))
    canvas.drawString(6.0*cm, 9.0*cm, ': '+ Curr + ' ' + formnum(NettPayment))
    canvas.drawString(6.0*cm, 8.5*cm, ' ' + ' Due to ' + usyou)
    
    #Calling Static Data
    SingleWeightedAdviceStatic(1, canvas, t, *rest)
    canvas.showPage()
    
    
