import ael
import time
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units     import inch, cm
from reportlab.platypus      import Paragraph, Frame, Spacer
from zak_funcs               import formnum
from PIL                     import Image


def TransactionTerms(canvas, t):

    Nominal = formnum(abs(t.nominal_amount(t.value_day)))
    TradeDate = str(ael.date_from_time(t.time))
    
    l = t.insaddr.legs()[0]
    EffectiveDate = str(l.start_day)
    EndDate  = str(l.end_day)        
    DayCount = l.daycount_method
    
    Curr = t.insaddr.curr.insid
    dc = ' '
    if Curr  == 'ZAR':
    	dc   = '(Fixed)'
    else:
    	dc = ''
	
    Date = ael.date_today()
    
    Calendar1 = ' '
    Calendar2 = ' '
    
    try:
    	Calendar1 = l.pay_calnbr.calid
    except:
	Calendar1 = ''
	    
    try:
    	Calendar2 = 'and' + ' ' + l.pay2_calnbr.calid
    except:
	Calendar2 = ''
    
    FixedPayer = ''
    FloatPayer = '' 
    
    p = t.counterparty_ptynbr
    FullName = p.fullname
    
    if t.nominal_amount() < 0:
    	FixedPayer = FullName
	FloatPayer = 'ABSA BANK LIMITED'
    else:
    	FixedPayer = 'ABSA BANK LIMITED'
	FloatPayer = FullName
	
    # ###### Leg Details #######	
    
    legs = t.insaddr.legs()
    
    FixedRate     = ' '
    DayCountFixed = ' '
    fixpyday      = ' '
    for l in legs:

	if l.type == 'Float':

	    flpyday = ''
	
	    if l.float_rate.insid.find('JIBAR') != -1:
	    	Index = 'ZAR-JIBAR-SAFEX'
	    elif l.float_rate.insid.find('USD-LIBOR') != -1:
	    	Index = 'USD-LIBOR-BBA'
	    else: Index = l.float_rate.insid
	    

	    dict = {'m':'Months','y':'Years','d':'Days'}
    	    field = l.rolling_period
    	    amount = field.rstrip(field[len(field)-1])
    	    c = field[len(field)-1]
    	    DesMaturity =  (str)(amount) + ' ' + dict[c]
	    
	    DayCountFloat = l.daycount_method
	    
	    Spread = ''  
	    if l.spread == 0:
	    	Spread = 'None'
	    else:
	    	Spread = l.spread
	   
            
    	    cshflws = l.cash_flows()

    	    list = []
    	    for c in cshflws:
                tup = (c.cfwnbr, c.pay_day)
                list.append(tup)
            flpyday = list.sort()
            flpyday = list.reverse()
            
                   
            count = 0
            flpyday = ''         
            while count < len(list):
                if count == 0:
                    flpyday = str(list[count][1])
                else:
                    flpyday = flpyday + '; ' + str(list[count][1])
                count = count + 1
        
        if l.type == 'Fixed':
	    fixpyday = ''        
	    FixedRate = str(l.fixed_rate)
	    DayCountFixed = l.daycount_method
	    	      		    	
    	    cshflws = l.cash_flows()
        
    	    alist = []
    	    for c in cshflws:
                tup = (c.cfwnbr, c.pay_day)
                alist.append(tup)
            fixpyday = alist.sort()
            fixpyday = alist.reverse()
                        
            count = 0
            fixpyday = ''             
            while count < len(alist):
                if count == 0:
                    fixpyday = str(alist[count][1])
                else:
                    fixpyday = fixpyday + '; ' + str(alist[count][1])
                count = count + 1
                
    
    #Transaction Terms static data
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(2.0 * cm, 16.0*cm, 'Notional Amount:')
    canvas.drawString(2.0 * cm, 15.0*cm, 'Trade Date:')
    canvas.drawString(2.0 * cm, 14.0*cm, 'Effective Date:')
    canvas.drawString(2.0 * cm, 13.0*cm, 'Termination Date:')
    canvas.drawString(2.0 * cm, 12.0*cm, 'Fixed Rate Payer :')
    canvas.drawString(2.0 * cm, 11.0*cm, 'Fixed Rate:')
    canvas.drawString(2.0 * cm, 10.0*cm, 'Fixed Rate Day Count:')
    canvas.drawString(2.0 * cm, 9.0*cm, 'Float Rate Payer:')
    canvas.drawString(2.0 * cm,  8.0*cm, 'Floating Rate Option:')
    canvas.drawString(2.0 * cm,  7.0*cm, 'Designated Maturity:')
    canvas.drawString(2.0 * cm,  6.0*cm, 'Floating Rate Day Count:')
    canvas.drawString(2.0 * cm,  5.0*cm, 'Floating Rate Spread:')
    canvas.drawString(2.0 * cm,  4.0*cm, 'Reset Dates:')
    canvas.drawString(2.0 * cm,  3.0*cm, 'Business Days:')
    canvas.drawString(2.0 * cm,  2.0*cm, 'Calculating Agent:')
    
    #Transaction terms
    canvas.drawString(8.0 * cm, 16.0*cm, Curr + Nominal)
    canvas.drawString(8.0 * cm, 15.0*cm, TradeDate)
    canvas.drawString(8.0 * cm, 14.0*cm, EffectiveDate)
    canvas.drawString(8.0 * cm, 13.0*cm, EndDate)
    canvas.drawString(10.0 * cm, 13.0*cm, '(Subject to adjustment in accordance with the Modified')
    canvas.drawString(10.0 * cm, 12.6*cm, 'Following Business Day convention)')
    canvas.drawString(8.0 * cm, 12.0*cm, FixedPayer)
    canvas.drawString(8.0 * cm, 11.0*cm, str(FixedRate) +'%')
    canvas.drawString(8.0 * cm, 10.0*cm, str(DayCountFixed)+dc)
    canvas.drawString(8.0 * cm,  9.0*cm, FloatPayer)
    canvas.drawString(8.0 * cm,  8.0*cm, Index)
    canvas.drawString(8.0 * cm,  7.0*cm, DesMaturity)
    canvas.drawString(8.0 * cm,  6.0*cm, DayCountFloat+dc)
    canvas.drawString(8.0 * cm,  5.0*cm, Spread)
    canvas.drawString(8.0 * cm,  4.0*cm, 'The first business day of each calculation period')
    canvas.drawString(8.0 * cm,  3.0*cm, Calendar1 + Calendar2)
    canvas.drawString(8.0 * cm,  2.0*cm, 'ABSA BANK LIMITED, Johannesburg, unless otherwise')
    canvas.drawString(8.0 * cm,  1.6*cm, 'specified in the Agreement')
    canvas.showPage()
    
def PaymentDates(canvas, t):
    
    # ###### Leg Details #######	
    
    legs = t.insaddr.legs()
    
    fixpyday = ' '
    for l in legs:

	if l.type == 'Float':

	    flpyday = ''
	
	    cshflws = l.cash_flows()

    	    list = []
    	    for c in cshflws:
                tup = (c.cfwnbr, c.pay_day)
                list.append(tup)
            flpyday = list.sort()
            flpyday = list.reverse()
                               
            count = 0
            flpyday = ''         
            while count < len(list):
                if count == 0:
                    flpyday = str(list[count][1])
                else:
                    flpyday = flpyday + '; ' + str(list[count][1])
                count = count + 1
            	    
	if l.type == 'Fixed':
	    fixpyday = ''        
	    	      		    	
    	    cshflws = l.cash_flows()
        
    	    alist = []
    	    for c in cshflws:
                tup = (c.cfwnbr, c.pay_day)
                alist.append(tup)
            fixpyday = alist.sort()
            fixpyday = alist.reverse()
                        
            count = 0
            fixpyday = ''             
            while count < len(alist):
                if count == 0:
                    fixpyday = str(alist[count][1])
                else:
                    fixpyday = fixpyday + '; ' + str(alist[count][1])
                count = count + 1
                
    
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
        
    Text1 = (fixpyday+' '+'(Subject to adjustment in accordance with the Modified Following Business Day convention).')
    Text2 = (flpyday +' '+'(Subject to adjustment in accordance with the Modified Following Business Day convention).')
    Text3 = ('Fixed Rate Payer Payment Dates:')
    Text4 = ('Float Rate Payer Payment Dates:') 
    bodyStyle1 =ParagraphStyle('Text', spaceBefore=0, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                alignment = 4, leftIndent = 0)
    bodyStyle2 =ParagraphStyle('Text', spaceBefore=0, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                alignment = 4, leftIndent = 180)
    bodyStyle3 =ParagraphStyle('Text', spaceBefore=0, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                alignment = 4, leftIndent = 180)
                   
    
    para1  = Paragraph(Text1, bodyStyle2)
    para2  = Paragraph(Text2, bodyStyle3)
    para3  = Paragraph(Text3, bodyStyle1)
    para4  = Paragraph(Text4, bodyStyle1)
    mydata = [para3, para1, para4, para2]
    
    frame.addFromList(mydata, canvas)
    canvas.showPage()
    
def BreakClause(canvas, t):
  
    ####### BREAK CLAUSE #######
    term = ael.date_from_time(t.time).add_months(1).years_between(t.insaddr.exp_day)
    
    BreakType    = ' '
    BreakForm    = ' '
    BreakPlace   = ' '
    ExBusDays    = ' '
    ExerciseType = ' '
    
    if term > 3.0 and term < 4.0:
	BreakType    = 'European'
	BreakForm    = 'Yes'
	BreakPlace   = 'Johannesburg'
	ExBusDays    = 'London and Johannesburg'
	ExerciseType = 'Partial Exercise'
    elif term >= 4.0:
	BreakType    = 'Bermuda'
	BreakForm    = 'Yes'
	ExerciseType = 'Multiple Exercise'
	
        if t.insaddr.curr.insid == 'EUR':
    	    BreakPlace = 'Brussels'
	    ExBusDays  = 'London and Target Settlement Day'
    	else:
    	    BreakPlace = 'Johannesburg'
	    ExBusDays  = 'London and Johannesburg'

    else: 
    	BreakType    = 'None'
	BreakForm    = 'No'
	BreakPlace   = 'None'
	ExBusDays    = 'None'
        ExerciseType = 'None'
    
    BreakDay = str(ael.date_from_time(t.time).to_string("%d-%B"))                                  

    #start + 3yr
    BreakStart = str((ael.date_from_time(t.time).add_years(3)).to_string("%d-%B-%Y"))              
             
    year = str((t.insaddr.exp_day.add_years(-1)).to_string("-%Y"))                        
    BreakEnd = BreakDay + year

    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(1.5 * cm, 27.43*cm, '8.')
    canvas.setFont("Helvetica-Bold", 10.0)            
    canvas.drawString(2.0 * cm, 27.43*cm, 'OTHER PROVISIONS')  
    canvas.drawString(2.0 * cm, 26.5*cm, '(a) Early Termination:')
    canvas.setFont("Helvetica", 10.0)            
    canvas.drawString(2.0 * cm, 25.5*cm, 'Optional Early Termination:')
    canvas.drawString(2.0 * cm, 24.5*cm, 'Option Style:')
    canvas.drawString(2.0 * cm, 23.5*cm, 'Business Days for Payment:')
    canvas.drawString(2.0 * cm, 22.5*cm, 'Calculation Agent:')
    
    canvas.setFont("Helvetica-Bold", 10.0)            
    canvas.drawString(2.0 * cm, 21.5*cm, '(b) Procedure for Exercise:')
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(2.0 * cm, 20.5*cm, 'Bermuda Option Exercise dates:')
    canvas.drawString(2.0 * cm, 19.5*cm, 'Expiration Date:')
    canvas.drawString(2.0 * cm, 18.5*cm, 'Earliest Exercise Time:')
    canvas.drawString(2.0 * cm, 17.5*cm, 'Latest Exercise Time:')
    canvas.drawString(2.0 * cm, 16.5*cm, 'Multiple Exercise:')
    
    canvas.setFont("Helvetica-Bold", 10.0)            
    canvas.drawString(2.0 * cm, 15.5*cm, '(c) Settlement Terms:')
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(2.0 * cm, 14.5*cm, 'Cash Settlement:')
    canvas.drawString(2.0 * cm, 13.5*cm, 'Cash Settlement Valuation Time:')
    canvas.drawString(2.0 * cm, 12.5*cm, 'Cash Settlement Valuation Date:')
    canvas.drawString(2.0 * cm, 11.5*cm, 'Valuation Business Days:')
    canvas.drawString(2.0 * cm, 10.5*cm, 'Cash Settlement Payment Dates:')
    canvas.drawString(2.0 * cm,  9.5*cm, 'Business Day Convention for Cash')
    canvas.drawString(2.0 * cm,  9.1*cm, 'Settlement Payment Date:')
    canvas.drawString(2.0 * cm,  8.5*cm, 'Cash Settlement Method:')
    canvas.drawString(2.0 * cm,  7.5*cm, 'Settlement Rate:')
    canvas.drawString(2.0 * cm,  6.5*cm, 'Cash Settlement Reference Banks:')
    canvas.drawString(2.0 * cm,  5.0*cm, 'Quotation Rate:')
    
    canvas.setFont("Helvetica", 10.0)            
    canvas.drawString(8.0 * cm, 25.5*cm, 'Applicable')
    canvas.drawString(8.0 * cm, 24.5*cm, BreakType)
    canvas.drawString(8.0 * cm, 23.5*cm, 'Johannesburg')
    canvas.drawString(8.0 * cm, 22.5*cm, 'Non-Exercising Party')
    
    canvas.setFont("Helvetica-Bold", 10.0)            
    canvas.drawString(2.0 * cm, 21.5*cm, '(b) Procedure for Exercise:')
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(8.0 * cm, 20.5*cm, 'Five Exercise Business Days prior to each Cash')
    canvas.drawString(8.0 * cm, 20.1*cm, 'Settlement Payment Date.')
    canvas.drawString(8.0 * cm, 19.5*cm, 'The date that is 5 Exercise Business Days')
    canvas.drawString(8.0 * cm, 19.1*cm, 'preceding the last Cash Settlement Payment Date.')
    canvas.drawString(8.0 * cm, 18.5*cm, '9:00 a.m Johannesburg time')
    canvas.drawString(8.0 * cm, 17.5*cm, '11:00 a.m Johannesburg time')
    canvas.drawString(8.0 * cm, 16.5*cm, 'Inapplicable')
    
    canvas.setFont("Helvetica-Bold", 10.0)            
    canvas.drawString(2.0 * cm, 15.5*cm, '(c) Settlement Terms:')
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(8.0 * cm, 14.5*cm, 'Applicable')
    canvas.drawString(8.0 * cm, 13.5*cm, '11:00 a.m Johannesburg time')
    canvas.drawString(8.0 * cm, 12.5*cm, 'Two Valuation Business Days prior to Cash')
    canvas.drawString(8.0 * cm, 12.1*cm, 'Settlement Payment Date')
    canvas.drawString(8.0 * cm, 11.5*cm, 'Johannesburg')
    canvas.drawString(8.0 * cm, 10.5*cm, 'Anually, each '+ BreakDay + ' ,commencing on')
    canvas.drawString(8.0 * cm, 10.1*cm, BreakStart + ' and ending on '+ BreakEnd)
    canvas.drawString(8.0 * cm,  9.1*cm, 'Modified Following Business Day Convention')
    canvas.drawString(8.0 * cm,  8.5*cm, 'Cash Price')
    canvas.drawString(8.0 * cm,  7.5*cm, 'Reference Banks')
    canvas.drawString(8.0 * cm,  6.5*cm, 'Five Market Dealers should be agreed upon')
    canvas.drawString(8.0 * cm,  6.1*cm, 'between the parties 5 Business Days preceding')
    canvas.drawString(8.0 * cm,  5.6*cm, 'the Cash Settlemt Date')
    canvas.drawString(8.0 * cm,  5.1*cm, 'Mid')
    canvas.showPage()
