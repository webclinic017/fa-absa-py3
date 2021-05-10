'''
This module builds Swap advice Note in pdf

Changes
Date            Change Number   Developer         Description
02/10/2009                      Tshepo Mabena     Initial deployment
2010-09-17      C435671         Willie vd Bank    Changed 2 disclaimers, colour of heading to red, added signatory date and name
                ABITFA-2001     Andrei Conicov    Email addresses need to be updated/corrected on the FA generated Reset Advice - Client facing
2017                            Willie vd Bank    2017 FA upgrade - Reset start and end dates are not populated anymore
2018            FAOPS-146       Deluan Cottle     2018 Rebranding requires a different colour pallette, therefore some colours of fonts have been changed
'''

import ael, acm, os, time, re
import reportlab.lib.pagesizes

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import *
from reportlab.lib.units     import cm
from STATIC_TEMPLATE         import BuildLogos, BuildAdviceFooter
from reportlab.lib.colors    import *
from zak_funcs               import formnum

def SingleSwapAdviceStatic(temp, canvas, t, *rest): 
    
    # Builds Header and Footer
    BuildLogos(canvas)
    BuildAdviceFooter(canvas)

    # Counterparty Address Details    
    Attention = t.counterparty_ptynbr.attention
    Address = t.counterparty_ptynbr.address
    Address2 = t.counterparty_ptynbr.address2
    Zipcode = t.counterparty_ptynbr.zipcode
    City = t.counterparty_ptynbr.city
    Fax = t.counterparty_ptynbr.fax
        
    CP = t.counterparty_ptynbr.fullname    
    Our_Ref = t.trdnbr
        
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(1.0 * cm, 25.5 * cm, str(Our_Ref))  
    canvas.drawString(1.0 * cm, 24.5 * cm, CP)
    canvas.drawString(1.0 * cm, 24.0 * cm, Address)
    canvas.drawString(1.0 * cm, 23.5 * cm, Address2)
    canvas.drawString(1.0 * cm, 23.0 * cm, City)
    canvas.drawString(1.0 * cm, 22.5 * cm, Attention)
    canvas.drawString(1.0 * cm, 22.0 * cm, 'FAX NO.' + Fax)
    canvas.drawString(1.0 * cm, 20.5 * cm, 'Dear Sirs')
    
    canvas.setFillColorRGB(0.862, 0, 0.196)
    canvas.drawString(8.0 * cm, 20.0 * cm, 'ADVICE OF INTEREST RATE SWAP RESET ("ADVICE")')
    canvas.setFillColorRGB(0, 0, 0)
    
    canvas.drawString(1.0 * cm, 19.0 * cm, 'The terms of the particular Transaction to which this Advice relates are as follows:')
    
    canvas.drawString(1.0 * cm, 18.0 * cm, 'Our Reference')
    canvas.drawString(1.0 * cm, 17.5 * cm, 'Notional Amount')
    canvas.drawString(1.0 * cm, 17.0 * cm, 'Trade Date')
    canvas.drawString(1.0 * cm, 16.5 * cm, 'Effective Date')
    canvas.drawString(1.0 * cm, 16.0 * cm, 'Fixed Rate Payer')
    canvas.drawString(1.0 * cm, 15.5 * cm, 'Fixed Rate')
    canvas.drawString(1.0 * cm, 15.0 * cm, 'Fixed Payment Date')
    canvas.drawString(1.0 * cm, 14.5 * cm, 'Period. (days)')
    canvas.drawString(1.0 * cm, 14.0 * cm, 'Fixed Payment')
    canvas.drawString(1.0 * cm, 13.5 * cm, 'Floating Rate Payer')
    canvas.drawString(1.0 * cm, 13.0 * cm, 'Floating Rate Reset')
    canvas.drawString(1.0 * cm, 12.5 * cm, 'Spread')
    canvas.drawString(1.0 * cm, 12.0 * cm, 'Floating Payment Date')
    canvas.drawString(1.0 * cm, 11.5 * cm, 'Period. (days)')
    canvas.drawString(1.0 * cm, 11.0 * cm, 'Floating Payment')
    canvas.drawString(1.0 * cm, 10.5 * cm, 'Net Payment')
    
    # canvas.drawString(1.0*cm,9.5*cm,  'Please confirm that the aforegoing correctly sets out the terms of our agreement by signing and returning a copy of this advice to ourselves at fax number')
    # canvas.drawString(1.0*cm,9.1*cm,  '(011) 895 7822 or advise us of any discrepancies at telephone number (011) 895 6837.')
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(1 * cm, 9.5 * cm, 'Please confirm that the foregoing correctly sets out all the terms and conditions of our agreement with respect to the Transaction by responding')
    canvas.drawString(1 * cm, 9.2 * cm, 'within three (3) Business Days of receipt of this Advice by promptly signing in the space provided below and returning a copy of this Advice to ourselves')
    canvas.drawString(1 * cm, 8.9 * cm, 'at email address irdsettlements@barclayscapital.com . Should there be any discrepancies to the foregoing, please advise us by email at')
    canvas.drawString(1 * cm, 8.6 * cm, 'irdsettlements@barclayscapital.com within the period stipulated above. Your failure to respond within such period shall not affect the validity or enforceability')
    canvas.drawString(1 * cm, 8.3 * cm, 'of the Transaction as against you. This Advice supplements, forms a part of, and is subject to, the Confirmation signed between us in respect of the')
    canvas.drawString(1 * cm, 8.0 * cm, 'Transaction ("Confirmation"). Any terms defined in the Confirmation and not defined in this Advice shall have the meanings set forth in the Confirmation.')
    canvas.drawString(1 * cm, 7.7 * cm, 'In the event of any inconsistency between the provisions of this Advice and the Confirmation, the Confirmation will prevail for the purpose of the Transaction.')
    canvas.setFont("Helvetica", 8.0)
    
    canvas.drawString(1.0 * cm, 6.7 * cm, 'For and on behalf of')
    canvas.drawString(1.0 * cm, 6.2 * cm, CP)
    canvas.drawString(1.0 * cm, 5.0 * cm, '_' * 40)
    canvas.drawString(1.0 * cm, 4.7 * cm, 'Name of Signatory')
    canvas.drawString(10.0 * cm, 5.0 * cm, '_' * 40)
    canvas.drawString(10.0 * cm, 4.7 * cm, 'Date of Signature')
    canvas.drawString(1.0 * cm, 4.0 * cm, 'THIS ADVICE IS ELECTRONICALLY GENERATED AND REQUIRES NO SIGNATURE BY ABSA BANK LIMITED.')

    return canvas
    
def BuildSingleAdvice(temp, t, date, canvas, *rest):
   
    Our_Ref = t.trdnbr
    Your_Ref = t.your_ref
    TradeDate = ael.date_from_time(t.time)
    Curr = t.display_id('curr')
    
    # ################################### Fixed Leg #################################
    Notional = 0.0
    Days_Fixed = 0
    FixedPayment = 0.0
    EffectiveDate = ''
    FixedPaymentDate = ''
    for cf in t.insaddr.cash_flows():
        if date == cf.start_day:
            if cf.type == 'Fixed Rate':
                Notional = cf.nominal_factor * t.quantity * t.insaddr.contr_size
                EffectiveDate = cf.start_day
                FixedPaymentDate = cf.pay_day
                Days_Fixed = int(cf.start_day.days_between(cf.end_day))
                FixedPayment = cf.projected_cf() * t.quantity 
    
    # ################################# Floating Leg #################################
    FloatPayment = 0.0  
    FloatRateReset = 0.0 
    Days_Float = 0
    FloatPayment = 0.0
    FloatPaymentDate = ''
    for c in t.insaddr.cash_flows():
        if c.type == 'Float Rate':
            if date == c.start_day:
                FloatPayment = c.projected_cf() * t.quantity
                FloatPaymentDate = c.pay_day
                Days_Float = int(c.start_day.days_between(c.end_day))
                FloatPayment = c.projected_cf() * t.quantity 
                for r in c.resets():
                    if r.value != 0:
                        #if r.start_day == date:
                        FloatRateReset = r.value                
    FixedPayer = ''  
    FloatPayer = '' 
                                
    if t.nominal_amount() < 0:
        FixedPayer = t.counterparty_ptynbr.fullname 
        FloatPayer = 'ABSA BANK LIMITED'
    else:
        FixedPayer = 'ABSA BANK LIMITED'
        FloatPayer = t.counterparty_ptynbr.fullname     
    
    FixedRate = 0.0
    Spread = 0.0
    
    for l in t.insaddr.legs():
        if l.type == 'Fixed':
            if l.fixed_rate == 0.0:
                if cf.rate != 0.0:
                    FixedRate = cf.rate
            else:
                FixedRate = l.fixed_rate
        if l.type == 'Float':
            Spread = l.spread
      
    NetPayment = FloatPayment + FixedPayment 
       
    usyou = ''
    if NetPayment > 0:
        usyou = 'Us'
    else:
        usyou = 'You'
        
    canvas.setFont("Helvetica", 8.0)                
    canvas.drawString(6.0 * cm, 18.0 * cm, ': ' + str(Our_Ref))
    canvas.drawString(6.0 * cm, 17.5 * cm, ': ' + ' ' + Curr + ' ' + formnum(Notional))
    canvas.drawString(6.0 * cm, 17.0 * cm, ': ' + str(TradeDate))
    canvas.drawString(6.0 * cm, 16.5 * cm, ': ' + str(EffectiveDate))
    canvas.drawString(6.0 * cm, 16.0 * cm, ': ' + FixedPayer)
    canvas.drawString(6.0 * cm, 15.5 * cm, ': ' + str(FixedRate) + ' ' + '%' + ' ' + '(yield)')
    canvas.drawString(6.0 * cm, 15.0 * cm, ': ' + str(FixedPaymentDate))
    canvas.drawString(6.0 * cm, 14.5 * cm, ': ' + str(Days_Fixed))
    canvas.drawString(6.0 * cm, 14.0 * cm, ': ' + Curr + ' ' + formnum(abs(FixedPayment)))
    canvas.drawString(6.0 * cm, 13.5 * cm, ': ' + FloatPayer)
    canvas.drawString(6.0 * cm, 13.0 * cm, ': ' + str(FloatRateReset) + ' ' + '%' + ' ' + '(yield)')
    canvas.drawString(6.0 * cm, 12.5 * cm, ': ' + str(Spread))
    canvas.drawString(6.0 * cm, 12.0 * cm, ': ' + str(FloatPaymentDate))
    canvas.drawString(6.0 * cm, 11.5 * cm, ': ' + str(Days_Float))
    canvas.drawString(6.0 * cm, 11.0 * cm, ': ' + Curr + ' ' + formnum(abs(FloatPayment)))
    canvas.drawString(6.0 * cm, 10.5 * cm, ': ' + Curr + ' ' + formnum(NetPayment))
    canvas.drawString(6.0 * cm, 10.0 * cm, '  ' + 'Due to' + ' ' + usyou)
    
    # Calling Static Data
    SingleSwapAdviceStatic(1, canvas, t)
    canvas.showPage()
