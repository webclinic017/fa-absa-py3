'''
Developer   : Tshepo Mabena
Module      : Dev_Swap_Reset_Advice_PDF
Date        : 02/10/2009
Description : This module builds Advice Notes for Caps and Floors in pdf

Changes

Purpose             : [To calculate the net payment of the Floor],[Changed 2 disclaimers, colour of heading to red, added signatory date and name][Email addresses need to be updated/corrected on the FA generated Reset Advice - Client facing]
Department and Desk : [OPS : Derivative Settlements],[OPS],[OPS]
Requester           : [Nhlanhla Mhlophe],[Nomsa Vilakazi],[Bruce Dell]
Developer           : [Tshepo Mabena],[Willie van der Bank],[Andrei Conicov]
CR Number           : [216108],[C435671 2010-09-17],[ABITFA-2001]

Purpose             : 2018 rebranding requires new colour pallete
Department and Desk : Post Trade Services
Requester           : Kgomotso Gumbo
Developer           : Deluan Cottle
CR Number           : CHG1000757460
'''

import ael, acm, os, time
import reportlab.lib.pagesizes

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import *
from reportlab.lib.units     import cm
from STATIC_TEMPLATE         import BuildLogos, BuildAdviceFooter
from reportlab.lib.colors    import *
from zak_funcs               import formnum

def CapFloorAdviceStatic(temp, canvas, t, date, *rest): 
    
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
    canvas.drawString(1.0 * cm, 25.5 * cm, CP)  
    canvas.drawString(1.0 * cm, 25.0 * cm, Address)
    canvas.drawString(1.0 * cm, 24.5 * cm, Address2)
    canvas.drawString(1.0 * cm, 24.0 * cm, Zipcode)
    canvas.drawString(1.0 * cm, 23.5 * cm, City)
    canvas.drawString(1.0 * cm, 23.0 * cm, 'ATTENTION: ' + Attention)
    canvas.drawString(1.0 * cm, 22.5 * cm, 'FAX NO.' + Fax)
    canvas.drawString(1.0 * cm, 21.5 * cm, 'Dear Sirs')
    
    canvas.setFillColorRGB(0.862, 0, 0.196)
    canvas.drawString(7.0 * cm, 20.5 * cm, 'ADVICE OF INTEREST RATE ' + t.insaddr.instype.upper() + ' RESET ("ADVICE")')
    canvas.setFillColorRGB(0, 0, 0)
    
    canvas.drawString(1.0 * cm, 19.5 * cm, 'The terms of the particular Transaction to which this Advice relates are as follows:')
    
    canvas.drawString(1.0 * cm, 18.5 * cm, 'Our Reference')
    canvas.drawString(1.0 * cm, 18.0 * cm, 'Notional Amount')
    canvas.drawString(1.0 * cm, 17.5 * cm, 'Trade Date')
    canvas.drawString(1.0 * cm, 17.0 * cm, 'Effective Date')
    canvas.drawString(1.0 * cm, 16.5 * cm, 'Fixed Rate Payer')
    
    if t.insaddr.instype == 'Floor':
        canvas.drawString(1.0 * cm, 16.0 * cm, 'Floor Rate')
    else:
        canvas.drawString(1.0 * cm, 16.0 * cm, 'CAP Rate')
        
    canvas.drawString(1.0 * cm, 15.5 * cm, 'Period End Date')
    canvas.drawString(1.0 * cm, 15.0 * cm, 'Fixed Payment Date')
    canvas.drawString(1.0 * cm, 14.5 * cm, 'Period. (days)')
    canvas.drawString(1.0 * cm, 14.0 * cm, 'Floating Rate Payer')
    canvas.drawString(1.0 * cm, 13.5 * cm, 'Floating Rate Reset')
    canvas.drawString(1.0 * cm, 13.0 * cm, 'Floating Payment Date')
    canvas.drawString(1.0 * cm, 12.5 * cm, 'Period. (days)')
    canvas.drawString(1.0 * cm, 12.0 * cm, 'Net Payment')
       
    # canvas.drawString(1.0*cm,10.5*cm,  'Please confirm that the aforegoing correctly sets out the terms of our agreement by signing and returning a copy of this advice to ourselves at fax number')
    # canvas.drawString(1.0*cm,10.1*cm,  '(011) 895 7822 or advise us of any discrepancies at telephone number (011) 895 6837.')
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

def BuildAdvice(temp, t, canvas, date, *rest):
    
    Our_Ref = t.trdnbr
    Curr = t.display_id('curr')
    TradeDate = ael.date_from_time(t.time)
       
    Notional_Amount = 0.0
    Start = ''
    End = ''
    Pay_Dates = ''
    Days = 0
    FloatRateReset = 0.0
    NettPayment = 0.0
    FixedRate = 0.0
    Floorlet = 0.0
    
    for cf in t.insaddr.cash_flows():
        for r in cf.resets():
            if r.day == date:
                Notional_Amount = cf.nominal_factor * t.quantity * t.insaddr.contr_size
                Start = cf.start_day
                End = cf.end_day
                Pay_Dates = cf.pay_day
                Days = int(cf.start_day.days_between(cf.end_day))
                FloatRateReset = r.value
                              
    if t.insaddr.instype == 'Floor':
        for cf in t.insaddr.cash_flows():
            if cf.pay_day == Pay_Dates:
                if cf.type == 'Floorlet':
                    Floorlet = cf.projected_cf() * t.quantity 
                if cf.type == 'Fixed Rate':    
                    FixedRate = cf.projected_cf() * t.quantity 
                
        NettPayment = Floorlet + FixedRate 
       
    elif t.insaddr.instype == 'Cap':
        for l in t.insaddr.legs():
            Strike = l.strike 
            if FloatRateReset > Strike:
                NettPayment = cf.projected_cf() * t.quantity      
            else:
                NettPayment = 0 
        
    Strike = 0.0
    for l in t.insaddr.legs():
        Strike = l.strike
            
    FixedPayer = ''        
    FloatPayer = ''
    usthem = ''
    
    if Notional_Amount > 0:
        FixedPayer = 'ABSA BANK LIMITED'
        FloatPayer = t.counterparty_ptynbr.fullname
        usthem = 'us'
    else:
        FixedPayer = t.counterparty_ptynbr.fullname
        FloatPayer = 'ABSA BANK LIMITED'
        if t.insaddr.instype == 'Cap':
            usthem = 'yourselves'
        else:    
            usthem = 'them'
        
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(6.0 * cm, 18.5 * cm, ': ' + str(Our_Ref))
    canvas.drawString(6.0 * cm, 18.0 * cm, ': ' + ' ' + Curr + ' ' + formnum(abs(Notional_Amount)))
    canvas.drawString(6.0 * cm, 17.5 * cm, ': ' + str(TradeDate))
    canvas.drawString(6.0 * cm, 17.0 * cm, ': ' + str(Start))
    canvas.drawString(6.0 * cm, 16.5 * cm, ': ' + FixedPayer)
    canvas.drawString(6.0 * cm, 16.0 * cm, ': ' + str(Strike))
    canvas.drawString(6.0 * cm, 15.5 * cm, ': ' + str(End))
    canvas.drawString(6.0 * cm, 15.0 * cm, ': ' + str(Pay_Dates))
    canvas.drawString(6.0 * cm, 14.5 * cm, ': ' + str(Days))
    canvas.drawString(6.0 * cm, 14.0 * cm, ': ' + FloatPayer)
    canvas.drawString(6.0 * cm, 13.5 * cm, ': ' + str(FloatRateReset))
    canvas.drawString(6.0 * cm, 13.0 * cm, ': ' + str(Pay_Dates))
    canvas.drawString(6.0 * cm, 12.5 * cm, ': ' + str(Days))
    canvas.drawString(6.0 * cm, 12.0 * cm, ': ' + Curr + ' ' + formnum(NettPayment) + ' ' + ' Due to ' + ' ' + usthem)
    
    # Calling Static Data
    CapFloorAdviceStatic(1, canvas, t, date)
    canvas.showPage()
