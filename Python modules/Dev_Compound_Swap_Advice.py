
'''
Developer   : Tshepo Mabena, [Tshepo Mabena],[Andrei Conicov], [Willie van der Bank]
Module      : Dev_Swap_Reset_Advice_PDF
Date        : 02/10/2009,[10/11/2010], [2014/06/05]
Description : This module builds Compound Swap Advice Note in pdf,[Modifying the disclaimer and fixing a bug.],[Email addresses need to be updated/corrected on the FA generated Reset Advice - Client facing]
CR Number   : 491343 ,[ABITFA-2001], [CHNG0002015587]

changes:

Purpose             : 2018 rebranding requires new colour pallete
Department and Desk : Post Trade Services
Requester           : Kgomotso Gumbo
Developer           : Deluan Cottle
CR Number           : CHG1000757460

'''

import ael

from reportlab.lib.styles    import ParagraphStyle
from reportlab.lib.units     import inch, cm
from reportlab.platypus      import Paragraph, Frame

from STATIC_TEMPLATE         import BuildLogos, BuildAdviceFooter
from zak_funcs               import formnum

def CompoundSwapAdviceStatic(temp, canvas, t, *rest):

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
    canvas.drawString(1.0 * cm, 25.0 * cm, str(Our_Ref))
    canvas.drawString(1.0 * cm, 24.5 * cm, CP)
    canvas.drawString(1.0 * cm, 24.0 * cm, Address)
    canvas.drawString(1.0 * cm, 23.5 * cm, Address2)
    canvas.drawString(1.0 * cm, 23.0 * cm, str(Zipcode))
    canvas.drawString(1.0 * cm, 22.5 * cm, City)
    canvas.drawString(1.0 * cm, 22.0 * cm, Attention)
    canvas.drawString(1.0 * cm, 21.5 * cm, 'FAX NO.' + Fax)
    canvas.drawString(1.0 * cm, 20.5 * cm, 'Dear Sirs')

    canvas.setFillColorRGB(0.862, 0, 0.196)
    canvas.drawString(8.0 * cm, 20.0 * cm, 'ADVICE OF INTEREST RATE SWAP RESET ("ADVICE")')
    canvas.setFillColorRGB(0, 0, 0)

    canvas.drawString(1.0 * cm, 19.5 * cm, 'The terms of the particular Transaction to which this Advice relates are as follows:')

    canvas.drawString(1.0 * cm, 19.0 * cm, 'Our Reference')
    canvas.drawString(1.0 * cm, 18.5 * cm, 'Notional Amount')
    canvas.drawString(1.0 * cm, 18.0 * cm, 'Trade Date')

    canvas.drawString(1.0 * cm, 17.0 * cm, 'Effective Date')
    canvas.drawString(1.0 * cm, 16.5 * cm, 'Fixed Rate Payer')
    canvas.drawString(1.0 * cm, 16.0 * cm, 'Fixed Rate')
    canvas.drawString(1.0 * cm, 15.5 * cm, 'Fixed Payment Date')
    canvas.drawString(1.0 * cm, 15.0 * cm, 'Period. (days)')
    canvas.drawString(1.0 * cm, 14.5 * cm, 'Fixed Payment')

    canvas.drawString(1.0 * cm, 13.5 * cm, 'Effective Date')
    canvas.drawString(1.0 * cm, 13.0 * cm, 'Floating Rate Payer')
    canvas.drawString(1.0 * cm, 12.5 * cm, 'Floating Rate')
    canvas.drawString(1.0 * cm, 12.0 * cm, 'Floating Payment Date')
    canvas.drawString(1.0 * cm, 11.5 * cm, 'Period. (days)')
    canvas.drawString(1.0 * cm, 11.0 * cm, 'Floating Payment')

    canvas.drawString(1.0 * cm, 10.0 * cm, 'Net Payment')

    canvas.drawString(1.0 * cm, 6.7 * cm, 'For and on behalf of')
    canvas.drawString(1.0 * cm, 6.2 * cm, CP)
    canvas.drawString(1.0 * cm, 5.0 * cm, '_' * 40)
    canvas.drawString(1.0 * cm, 4.7 * cm, 'Name of Signatory')
    canvas.drawString(10.0 * cm, 5.0 * cm, '_' * 40)
    canvas.drawString(10.0 * cm, 4.7 * cm, 'Date of Signature')
    canvas.drawString(1.0 * cm, 4.0 * cm, 'THIS ADVICE IS ELECTRONICALLY GENERATED AND REQUIRES NO SIGNATURE BY ABSA BANK LIMITED.')

    frame = Frame(0.122 * inch, 2.65 * inch, 7.8 * inch, 1.05 * inch, showBoundary=0)

    Text1 = (' ')
    Text2 = ('Please confirm that the foregoing correctly sets out all the terms and conditions of our agreement with respect to the Transaction by responding\
            within three (3) Business Days of receipt of this Advice by promptly signing in the space provided below and returning a copy of this Advice to\
            ourselves at email address irdsettlements@barclayscapital.com . Should there be any discrepancies to the foregoing, please advise us by email at\
            irdsettlements@barclayscapital.com within the period stipulated above. Your failure to respond within such period shall not affect the validity or enforceability\
            of the Transaction as against you. This Advice supplements, forms a part of, and is subject to, the Confirmation signed between us in respect of the\
            Transaction ("Confirmation"). Any terms defined in the Confirmation and not defined in this Advice shall have the meanings set forth in the Confirmation\
            In the event of any inconsistency between the provisions of this Advice and the Confirmation, the Confirmation will prevail for the purpose of the Transaction.')

    bodyStyle1 = ParagraphStyle('Text', spaceBefore=0, fontName='Helvetica', fontSize=7, leading=8, \
                spaceAfter=0, alignment=4, leftIndent=15)

    para1 = Paragraph(Text1, bodyStyle1)
    para2 = Paragraph(Text2, bodyStyle1)

    mydata = [para1, para2]

    frame.addFromList(mydata, canvas)

    return canvas

def BuildAdvice(temp, t, date, canvas, adviceType, *rest):
    if adviceType not in ('compound', 'weighted'):
        raise ValueError("adviceType must be one of: compound, weighted")

    Our_Ref = t.trdnbr
    Curr = t.display_id('curr')
    TradeDate = ael.date_from_time(t.time)

    # ########################## Fixed Leg ################################
    FixedEffectiveDate = ''
    FixedPaymentDate = ''
    FixedRate = 0.0
    Notional = 0.0
    Days_Fixed = 0
    FixedPayment = 0.0

    for cf in t.insaddr.cash_flows():
        if date == cf.start_day:
            if cf.type == 'Fixed Rate':
                FixedEffectiveDate = cf.start_day.to_string('%Y-%m-%d')
                Notional = round(t.nominal_amount(cf.start_day), 0)
                FixedRate = cf.period_rate(cf.start_day, cf.end_day)
                FixedPaymentDate = cf.pay_day.to_string('%Y-%m-%d')
                Days_Fixed = int(cf.start_day.days_between(cf.end_day))
                FixedPayment = cf.projected_cf() * t.quantity

    if  Notional == 0.0:
        Notional = t.nominal_amount()

    # ########################## Floating Leg ################################
    FloatEffectiveDate = ''
    FloatPaymentDate = ''
    Days_Float = 0
    FloatPayment = 0.0
    FloatingRate = 0.0

    for c in t.insaddr.cash_flows():
        if c.type == 'Float Rate':
            if date == c.start_day:
                FloatEffectiveDate = c.start_day.to_string('%Y-%m-%d')
                if adviceType == 'compound':
                    if t.insaddr.instype == 'IndexLinkedSwap':
                        if len(c.resets()) >= 1:
                            FloatingRate = c.resets()[0].value
                    else:
                        FloatingRate = c.period_rate(c.start_day, c.end_day)

                FloatPaymentDate = c.pay_day.to_string('%Y-%m-%d')
                Days_Float = int(c.start_day.days_between(c.end_day))
                FloatPayment = c.projected_cf() * t.quantity

                if adviceType == 'weighted':
                    for r in c.resets():
                        FloatingRate += r.value
                    FloatingRate = FloatingRate / len(c.resets())


    NettPayment = FixedPayment + FloatPayment

    usyou = ''
    if NettPayment > 0:
        usyou = 'Us'
    else:
        usyou = 'You'

    FixedPayer = ''
    FloatPayer = ''

    if t.nominal_amount() < 0:
        FixedPayer = t.counterparty_ptynbr.fullname
        FloatPayer = 'ABSA BANK LIMITED'
    else:
        FixedPayer = 'ABSA BANK LIMITED'
        FloatPayer = t.counterparty_ptynbr.fullname

    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(6.0 * cm, 19.0 * cm, ': ' + str(Our_Ref))
    canvas.drawString(6.0 * cm, 18.5 * cm, ': ' + Curr + ' ' + str(formnum(Notional)))
    canvas.drawString(6.0 * cm, 18.0 * cm, ': ' + str(TradeDate))

    canvas.drawString(6.0 * cm, 17.0 * cm, ': ' + FixedEffectiveDate)
    canvas.drawString(6.0 * cm, 16.5 * cm, ': ' + FixedPayer)
    canvas.drawString(6.0 * cm, 16.0 * cm, ': ' + str(FixedRate) + ' ' + '%' + ' ' + '(yield)')
    canvas.drawString(6.0 * cm, 15.5 * cm, ': ' + FixedPaymentDate)
    canvas.drawString(6.0 * cm, 15.0 * cm, ': ' + str(Days_Fixed))
    canvas.drawString(6.0 * cm, 14.5 * cm, ': ' + Curr + ' ' + formnum(abs(FixedPayment)))

    canvas.drawString(6.0 * cm, 13.5 * cm, ': ' + FloatEffectiveDate)
    canvas.drawString(6.0 * cm, 13.0 * cm, ': ' + FloatPayer)
    canvas.drawString(6.0 * cm, 12.5 * cm, ': ' + str(FloatingRate) + ' ' + '%' + ' ' + '(yield)')
    canvas.drawString(6.0 * cm, 12.0 * cm, ': ' + FloatPaymentDate)
    canvas.drawString(6.0 * cm, 11.5 * cm, ': ' + str(Days_Float))
    canvas.drawString(6.0 * cm, 11.0 * cm, ': ' + Curr + ' ' + formnum(abs(FloatPayment)))
    canvas.drawString(6.0 * cm, 10.0 * cm, ': ' + Curr + ' ' + formnum(NettPayment))
    canvas.drawString(6.0 * cm, 9.5 * cm, ' ' + ' Due to ' + usyou)

    # Calling Static Data
    CompoundSwapAdviceStatic(1, canvas, t, *rest)
    canvas.showPage()

def BuildWeightedAdvice(temp, t, date, canvas, *rest):
    return BuildAdvice(temp, t, date, canvas, 'weighted', *rest)

def BuildCompoundAdvice(temp, t, date, canvas, *rest):
    return BuildAdvice(temp, t, date, canvas, 'compound', *rest)
