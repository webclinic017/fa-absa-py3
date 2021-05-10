'''
Purpose             : [Changed 2 disclaimers, colour of heading to red, added signatory date and name],[Email addresses need to be updated/corrected on the FA generated Reset Advice - Client facing]
Department and Desk : [OPS],[OPS]
Requester           : [Nomsa Vilakazi],[Bruce Dell]
Developer           : [Willie van der Bank],[Andrei Conicov]
CR Number           : [C435671 2010-09-17],[ABITFA-2001]

Changes:

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
from reportlab.lib.units import cm
from reportlab.lib.colors    import black, red
from zak_funcs import formnum
from STATIC_TEMPLATE import BuildLogos, BuildAdviceFooter 


def BuildAdviceNote(t, c, payDay):
    ael.poll()
    c.setFont("Helvetica", 8.0)
    
    # set coordinates
    x1 = 1
    x2 = 3
    x3 = 6
    x10 = 10
    y = 26
    
    # Static Data
    c.drawString(x1 * cm, y * cm, str(t.trdnbr))
    y = y - 0.75
    
    cpty = t.counterparty_ptynbr
    # Counterparty Address
    
    c.drawString(x1 * cm, y * cm, cpty.fullname)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, cpty.address)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, cpty.address2)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, cpty.city)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, cpty.zipcode)
    y = y - 0.75
    
    # Attention:
    c.drawString(x1 * cm, y * cm, 'Attention:')
    c.drawString(x2 * cm, y * cm, cpty.attention)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, 'Fax Number:')
    c.drawString(x2 * cm, y * cm, cpty.fax)
    y = y - 0.75
    c.drawString(x1 * cm, y * cm, 'Dear Sirs')
    y = y - 0.5
    
    c.setFillColorRGB(0.862, 0, 0.196)
    c.drawString(x3 * cm, y * cm, 'ADVICE OF INTEREST RATE SWAP RESET ("ADVICE")')
    c.setFillColorRGB(0, 0, 0)
    
    y = y - 0.75
    c.drawString(x1 * cm, y * cm, 'The terms of the particular Transaction to which this Advice relates are as follows:')
    y = y - 0.75
    

    # Beginning of the dynamic data table
    c.drawString(x1 * cm, y * cm, 'Our Reference')
    c.drawString(x3 * cm, y * cm, ': ' + str(t.trdnbr))
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, 'Trade Date')
    c.drawString(x3 * cm, y * cm, ': ' + str(ael.date_from_time(t.time)))
    y = y - 0.75
    
    # Retrieve the dynamic data
    ins = t.insaddr
    for l in ins.legs():
        leg = l
        for cf in l.cash_flows():
            if cf.pay_day == payDay and cf.type in ('Fixed Rate', 'Float Rate'):
                cashflow = cf

                amount = cashflow.projected_cf() * t.quantity
                if amount > 0:
                    payer = t.counterparty_ptynbr.fullname
                else:
                    payer = 'ABSA Bank Limited'
                
                curr = leg.curr.insid
                nominal = formnum(abs(cashflow.nominal_amount()))
                days = str(cashflow.start_day.days_between(cashflow.end_day))
                rate = cashflow.period_rate(cashflow.start_day, cashflow.end_day)
                spread = leg.spread
                daycount = str(leg.daycount_method)
                
                # print the data for each leg
                c.drawString(x1 * cm, y * cm, curr + ' Rate Payer')
                c.drawString(x3 * cm, y * cm, ': ' + payer)
                y = y - 0.5
                c.drawString(x1 * cm, y * cm, 'Notional Amount')
                c.drawString(x3 * cm, y * cm, ': ' + curr + ' ' + nominal)
                y = y - 0.5
                c.drawString(x1 * cm, y * cm, 'Rate')
                c.drawString(x3 * cm, y * cm, ': ' + str(rate) + '%')
                y = y - 0.5
                c.drawString(x1 * cm, y * cm, 'Spread')
                c.drawString(x3 * cm, y * cm, ': ' + str(spread) + '%')
                y = y - 0.5
                c.drawString(x1 * cm, y * cm, 'Calculation Period')
                c.drawString(x3 * cm, y * cm, ': ' + str(cashflow.start_day) + ' to ' + str(cashflow.end_day))
                y = y - 0.5
                c.drawString(x1 * cm, y * cm, 'Day Count')
                c.drawString(x3 * cm, y * cm, ': ' + str(daycount))
                y = y - 0.5
                c.drawString(x1 * cm, y * cm, 'Days in Calculation Period')
                c.drawString(x3 * cm, y * cm, ': ' + days)
                y = y - 0.5
                c.drawString(x1 * cm, y * cm, 'Interest calculation')
                c.drawString(x3 * cm, y * cm, ': ' + curr + ' ' + nominal + ' * ' + str(rate + spread) + '% * ' + days + '/' + daycount.split('/')[1] + ' = ' + curr + ' ' + ' ' + formnum(abs(amount)))
                y = y - 0.75
        
                if l.nominal_scaling == 'FX':
                    for cf in l.cash_flows():
                        if cf.pay_day == payDay and cf.type == 'Return':
                            cashflow = cf
                            amount2 = cashflow.projected_cf() * t.quantity
                            netPayment = amount + amount2 
       
                            usyou = ''
                            if netPayment > 0:
                                usyou = 'Us'
                            else:
                                usyou = 'You'
                            
                            y = y + 0.25
                            c.drawString(x1 * cm, y * cm, 'Reset of Notional Amount')
                            
                            c.drawString(x3 * cm, y * cm, ': ' + curr + ' ' + formnum(amount2))
                            y = y - 0.5
                            c.drawString(x1 * cm, y * cm, curr + ' Net Amount')
                            c.drawString(x3 * cm, y * cm, ': ' + curr + ' ' + formnum(abs(netPayment)) + '   ' + 'Due to ' + usyou)
                            y = y - 0.75

    # c.drawString(x1*cm,8.0*cm,  'Please confirm that the aforegoing correctly sets out the terms of our agreement by signing and returning a copy of this advice to ourselves at fax number')
    # c.drawString(x1*cm,7.5*cm,  '(011) 895 7822 or advise us of any discrepancies at telephone number (011) 895 6837.')
    c.setFont("Helvetica", 8.0)
    c.drawString(x1 * cm, 8.5 * cm, 'Please confirm that the foregoing correctly sets out all the terms and conditions of our agreement with respect to the Transaction by responding')
    c.drawString(x1 * cm, 8.2 * cm, 'within three (3) Business Days of receipt of this Advice by promptly signing in the space provided below and returning a copy of this Advice to ourselves')
    c.drawString(x1 * cm, 7.9 * cm, 'at email address irdsettlements@barclayscapital.com . Should there be any discrepancies to the foregoing, please advise us by email at')
    c.drawString(x1 * cm, 7.6 * cm, 'irdsettlements@barclayscapital.com within the period stipulated above. Your failure to respond within such period shall not affect the validity or enforceability')
    c.drawString(x1 * cm, 7.3 * cm, 'of the Transaction as against you. This Advice supplements, forms a part of, and is subject to, the Confirmation signed between us in respect of the')
    c.drawString(x1 * cm, 7.0 * cm, 'Transaction ("Confirmation"). Any terms defined in the Confirmation and not defined in this Advice shall have the meanings set forth in the Confirmation.')
    c.drawString(x1 * cm, 6.7 * cm, 'In the event of any inconsistency between the provisions of this Advice and the Confirmation, the Confirmation will prevail for the purpose of the Transaction.')
    c.setFont("Helvetica", 8.0)
    
    c.drawString(x1 * cm, 6.0 * cm, 'For and on behalf of')
    c.drawString(x1 * cm, 5.5 * cm, cpty.fullname)
    c.drawString(x1 * cm, 5.0 * cm, '_' * 40)
    c.drawString(x1 * cm, 4.7 * cm, 'Name of Signatory')
    c.drawString(x10 * cm, 5.0 * cm, '_' * 40)
    c.drawString(x10 * cm, 4.7 * cm, 'Date of Signature')
    c.drawString(x1 * cm, 4.0 * cm, 'THIS ADVICE IS ELECTRONICALLY GENERATED AND REQUIRES NO SIGNATURE BY ABSA BANK LIMITED.')
    
    BuildLogos(c)
    BuildAdviceFooter(c)
    
    c.showPage()
    return c
