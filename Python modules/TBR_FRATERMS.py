import ael
import time
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units     import inch, cm
from reportlab.platypus      import Paragraph, Frame, Spacer
from zak_funcs               import formnum
from PIL                     import Image


def TransactionTerms(canvas, t):

    Curr      = t.insaddr.curr.insid
    Nominal   = formnum(abs(t.nominal_amount(t.value_day)))
    TradeDate = str(ael.date_from_time(t.time))
    
    l = t.insaddr.legs()[0]
    EffectiveDate   = str(l.start_day)
    TerminationDate = str(l.end_day)
    
    FixedRatePayer  = ''
    FloatPayer      = ''
    Calendar1       = ''
    Calendar2       = ''
     
    if t.nominal_amount() < 0:
        FixedRatePayer = t.counterparty_ptynbr.fullname
        FloatPayer     = 'ABSA BANK LIMITED'
    else:
        FixedRatePayer = 'ABSA BANK LIMITED'
        FloatPayer     = t.counterparty_ptynbr.fullname  
    
    FixedRate = ' '
    Spread    = ' '
    legs = t.insaddr.legs()
    for l in legs:
        FixedRate = l.fixed_rate
        if l.type == 'Float':
            if l.spread == 0:
                Spread = 'None'
            else:
                Spread = str(l.spread)
                
        Index = l.float_rate.insid
        if l.float_rate.insid.find('JIBAR') != -1:
	    Index = 'ZAR-JIBAR-SAFEX'
	elif l.float_rate.insid.find('USD-LIBOR') != -1:
	    Index = 'USD-LIBOR-BBA'
	else: 
            Index = l.float_rate.insid
            
        dict = {'m':'Months','y':'Years','d':'Days'}
    	field = l.rolling_period
    	amount = field.rstrip(field[len(field)-1])
    	c = field[len(field)-1]
    	DesMaturity =  (str)(amount) + ' ' + dict[c]
    	
    	try:
            Calendar1 = l.pay_calnbr.calid
        except:
    	    Calendar1 = ''
	try:
            Calendar2 = 'and' + ' ' + l.pay2_calnbr.calid
        except:
            Calendar2 = ''
            
    DayCount    = str(l.daycount_method)
    PaymentDate = str(l.start_day)
    
    dc = ''
    if Curr == 'ZAR':
    	dc = '(Fixed)'
    else:
    	dc = ''
    
    
    #Transaction Terms static data
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(1.5 * cm, 27.43*cm, '5.')               
    canvas.drawString(2.0 * cm, 27.43*cm, 'The terms of the Transaction to which this Confirmation relates are as folllows:')  
    canvas.drawString(2.0 * cm, 26.5*cm, 'Nominal Amount')
    canvas.drawString(2.0 * cm, 25.5*cm, 'Trade Date')
    canvas.drawString(2.0 * cm, 24.5*cm, 'Effective Date')
    canvas.drawString(2.0 * cm, 23.5*cm, 'Termination Date')
    canvas.drawString(2.0 * cm, 22.0*cm, 'Fixed Amounts:')
    canvas.drawString(2.0 * cm, 21.5*cm, 'Fixed Rate Payer')
    canvas.drawString(2.0 * cm, 20.5*cm, 'Fixed Rate')
    canvas.drawString(2.0 * cm, 19.0*cm, 'Floating Amounts:')
    canvas.drawString(2.0 * cm, 18.5*cm, 'Floating Rate Payer')
    canvas.drawString(2.0 * cm, 17.5*cm, 'Payment Date')
    canvas.drawString(2.0 * cm, 16.0*cm, 'Spread')
    canvas.drawString(2.0 * cm, 15.5*cm, 'Floating Rate Option')
    canvas.drawString(2.0 * cm, 14.5*cm, 'Floating Rate Daycount Fraction')
    canvas.drawString(2.0 * cm, 13.5*cm, 'Designated Maturity')
    canvas.drawString(2.0 * cm, 12.5*cm, 'Reset Dates')
    canvas.drawString(2.0 * cm, 11.5*cm, 'FRA discounting')
    canvas.drawString(2.0 * cm, 10.5*cm, 'Business Days')
    canvas.drawString(2.0 * cm,  9.5*cm, 'calculating Agent')
    
    canvas.drawString(9.0 * cm, 26.5*cm, Curr+ ' '+Nominal)
    canvas.drawString(9.0 * cm, 25.5*cm, TradeDate)
    canvas.drawString(9.0 * cm, 24.5*cm, EffectiveDate)
    canvas.drawString(9.0 * cm, 23.5*cm, TerminationDate)
    canvas.drawString(9.0 * cm, 23.1*cm, '(Subject to adjustment in accordance with the Modified')
    canvas.drawString(9.0 * cm, 22.7*cm, 'Following Business Day Convention.)')
    canvas.drawString(9.0 * cm, 21.5*cm, FixedRatePayer)
    canvas.drawString(9.0 * cm, 20.5*cm, str(FixedRate)+' % '+DayCount+dc)
    canvas.drawString(9.0 * cm, 18.5*cm, FloatPayer)
    canvas.drawString(9.0 * cm, 17.5*cm, PaymentDate)
    canvas.drawString(9.0 * cm, 17.1*cm, '(Subject to adjustment in accordance with the Modified')
    canvas.drawString(9.0 * cm, 16.7*cm, 'Following Business Day Convention.)')
    canvas.drawString(9.0 * cm, 16.0*cm, Spread)
    canvas.drawString(9.0 * cm, 15.5*cm, Index)
    canvas.drawString(9.0 * cm, 14.5*cm, DayCount+dc)
    canvas.drawString(9.0 * cm, 13.5*cm, DesMaturity)
    canvas.drawString(9.0 * cm, 12.5*cm, 'The first business day of each calculation period subject to ')
    canvas.drawString(9.0 * cm, 12.1*cm, 'adjustment in accordance woth the following business day convention.')
    canvas.drawString(9.0 * cm, 11.5*cm, 'Applicable')
    canvas.drawString(9.0 * cm, 10.5*cm, str(Calendar1)+' '+str(Calendar2))
    canvas.drawString(9.0 * cm,  9.5*cm, 'ABSA unless otherwise specified in the Master Agreement')
    canvas.showPage()
