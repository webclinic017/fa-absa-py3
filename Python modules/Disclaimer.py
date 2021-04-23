"""------------------------------------------------------------------------------------------------------------------------------------

Name        	    : Disclaimer
Developer   	    : Tshepo Mabena, Bhavnisha Sarawan
Requester   	    : Haroon Mansoor (PCG)
Date        	    : 22/01/2009, 09/05/2011
Description 	    : This AEL module is developed to insert the disclaimer on the last page of the client valuation,
					  New Disclaimer for cashflows report (Called in CashFlowReportPdfBuilder.py)

Developer           : Ntuthuko Matthews
Requester           : Ryan Bates
Date                : 08/02/2013
Purpose             : Add an option to output the report into an excel format
Department and Desk : Primes Services Collateral Management and Client Valuations
CR Number           : 803296
			  
---------------------------------------------------------------------------------------------------------------------------------------"""

import ael
from Landscape                import BuildLogos, BuildFooter 
from reportlab.pdfgen.canvas  import Canvas
from reportlab.lib.units      import cm, inch
from reportlab.lib.styles     import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus       import Paragraph, Frame, Spacer

def BuildHeader(canvas, date):
   
    canvas.setFont("Helvetica-Bold", 12.0) 
    canvas.drawString(2.3 * inch, 15.0*cm, str(date)) 
    canvas.drawString(0.8 * inch, 17.0*cm, 'Revaluation Report')     
    canvas.drawString(0.8 * inch, 16.0*cm, 'Client Name:')
    canvas.drawString(0.8 * inch, 15.0*cm, 'Revaluation Date:') 
    canvas.drawString(0.8 * inch, 14.0*cm, 'Trade') 
    canvas.drawString(0.8 * inch, 13.6*cm, 'Number')
    canvas.drawString(2.0* inch, 14.0*cm,  'Trade') 
    canvas.drawString(2.0* inch, 13.6*cm,  'Date')
    canvas.drawString(3.1 * inch, 14.0*cm, 'Maturity') 
    canvas.drawString(3.1 * inch, 13.6*cm, 'Date')
    canvas.drawString(4.1 * inch, 13.6*cm, 'Instrument')
    canvas.drawString(5.3 * inch, 13.6*cm, 'Currency1')
    canvas.drawString(6.4 * inch, 13.6*cm, 'Nominal1')
    canvas.drawString(7.4 * inch, 13.6*cm, 'Currency2')
    canvas.drawString(8.4 * inch, 13.6*cm, 'Nominal2')
    canvas.drawString(9.5 * inch, 14.0*cm, 'Mark to')
    canvas.drawString(9.5 * inch, 13.6*cm, 'Market Value')
    canvas.drawString(2.0 * inch, 5.0*cm,  "Please note that this valuation is done from the bank's point of view so a negative value is in the client's favour")  
        
def Disclaimer(canvas):

    #Disclaimer on last page of the client valuation report
    
    Template = BuildLogos(canvas)
    Template = BuildFooter(canvas)
    
    canvas.setFont("Helvetica-Bold", 12.0) 
    canvas.drawString(0.9 * inch, 17.0*cm, 'Disclaimer') 
    canvas.drawString(0.9 * inch, 16.95*cm, '_'*9)
 
    frame = Frame(0.8*inch, 2.2*inch, 11.0*inch, 4.3*inch, showBoundary =0)
                
    Paragraph1  = ('This document has been prepared by Absa Capital, the investment banking division of Absa Bank Limited (registration number 1986/004794/06)\
                  ("Absa"), for information purposes only. This document is provided to you and at your specific request. ') 
    Paragraph2  = ('Any information herein is indicative, is subject to change, is not intended to be an offer or solicitation for the purchase, sale, assignment, settlement or termination of any\
                    financial instrument, and is provided for reference purposes only. This information is not intended as an indicative price or quotation, and does not imply that a market exists for\
                    any financial instrument discussed herein; it does not therefore reflect hedging and transaction costs, credit considerations, market liquidity or bid-offer spreads.\
                    Absa does not represent that any value(s) in this document directly correlate with values which could actually be achieved now or in the future Absa does not make any\
                    representation or warranty, neither does it guarantee the adequacy, accuracy, correctness or completeness of information which is contained in this document and which is\
                    stated to have been obtained from or is based upon trade and statistical services or other third party sources. Any data on past performance, modelling or back-testing\
                    contained herein is no indication as to future performance. No representation is made in respect of the assumptions or the accuracy or completeness of any modelling or\
                    back-testing. All opinions and estimates are given as of the date hereof and are subject to change. The value of any investment may fluctuate as a result of market changes.\
                    The information in this document is not intended to predict actual results and no assurances are given with respect thereto.\
                    This document represents our view as at the date hereof and subject to the limited scope of the assumptions and methodology set forth herein. This document has not been\
                    prepared in accordance with the standards and practice of any professional body in any jurisdiction and does not, and is not intended to, constitute an accounting, legal or tax opinion from Absa.')                
    
    Paragraph3 = ('This document is not intended to be legally binding. Neither you nor your affiliates or advisers or any other person may rely on the information contained herein. Absa does not,\
                   through this document or the views expressed herein, owe or accept any responsibility or liability to you or your affiliates or your advisers or any other person, whether in\
                   contract or in tort or howsoever otherwise arising, including the use of this document in the preparation of your own financial books and records, and shall have no responsibility\
                   or liability to you or your affiliates or advisers or any other person for any loss or damage suffered or costs or expenses incurred (whether direct or consequential) by any person\
                   arising out of or in connection with the provision of this document to you, howsoever loss or damage is caused or costs or expenses are incurred.\
                   Absa, its affiliates and the individuals associated therewith may (in various capacities) have positions or deal in transactions or securities (or related derivatives) identical or similar to those described herein.')               
    
    Paragraph4 = ('Absa Bank limited is registered in South Africa (all rights reserved). Copyright in this document is owned by Absa Bank Limited and is confidential, and no part of hereof may be\
                   reproduced, distributed or transmitted without the prior written permission of Absa Bank Limited.')
    Paragraph5 = ('Absa Bank Limited is an authorised Financial Services Provider.')    
               
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=0, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =4, alignment = 4)
        
    Paragraph1 = Paragraph(Paragraph1, bodyStyle1)
    Paragraph2 = Paragraph(Paragraph2, bodyStyle1)
    Paragraph3 = Paragraph(Paragraph3, bodyStyle1)
    Paragraph4 = Paragraph(Paragraph4, bodyStyle1)
    Paragraph5 = Paragraph(Paragraph5, bodyStyle1)
    
    mydata = [Paragraph1, Paragraph2, Paragraph3, Paragraph4, Paragraph5]
    
    frame.addFromList(mydata, canvas)

def CashflowsDisclaimer(canvas):
    #Disclaimer on the cashflow report
    canvas.setFont("Times-Roman", 6.0)
    canvas.drawString(2.0*cm, 6.36*cm, 'Disclaimer')
    frame = Frame(0.7*inch, 1.23*inch, 6.8*inch, 1.3*inch, showBoundary =0)
                
    Paragraph1  = ('This document (MS Excel Document) is provided to you together with the original version thereof (Pdf Format Document). At all time the Pdf Format Document shall be the primary reference and \
                    source of the information contained in these documents. If you open and/or use this MS Excel Document, you do so subject to all the risks associated with e-mail communications and the \
                    transmission of documentation through electronic communication systems, which risks include, but is not limited to, fraud, unauthorised transmission, errors in transmission, malfunction of \
                    equipment, distortion of communication links and the like. As a result of these risks or the subsequent opening and/or use of the MS Excel Document, the information contained in this MS \
                    Excel Document may be different from that of the Pdf Format Document. At all times you should only rely on the Pdf Format Document for purposes of accuracy of information and we will only be \
                    responsible for the information contained in the Pdf Format Document. ')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=0, fontName="Times-Roman", fontSize=6.0, leading=10, spaceAfter =4, alignment = 4)
    Paragraph1 = Paragraph(Paragraph1, bodyStyle1)
    data = [Paragraph1]
    frame.addFromList(data, canvas)

def ExcelDisclaimer(rows):
    rows.append(['Disclaimer'])
    rows.append('')
    #Paragraph1 
    rows.append(['This document has been prepared by Absa Capital, the investment banking division of Absa Bank Limited (registration number 1986/004794/06)'])
    rows.append(['("Absa"), for information purposes only. This document is provided to you and at your specific request.'])
    rows.append('')
    #Paragraph2 
    rows.append(['Any information herein is indicative, is subject to change, is not intended to be an offer or solicitation for the purchase, sale, assignment, settlement or termination of any'])
    rows.append(['financial instrument, and is provided for reference purposes only. This information is not intended as an indicative price or quotation, and does not imply that a market exists for'])
    rows.append(['any financial instrument discussed herein; it does not therefore reflect hedging and transaction costs, credit considerations, market liquidity or bid-offer spreads.'])
    rows.append(['Absa does not represent that any value(s) in this document directly correlate with values which could actually be achieved now or in the future Absa does not make any'])
    rows.append(['representation or warranty, neither does it guarantee the adequacy, accuracy, correctness or completeness of information which is contained in this document and which is'])
    rows.append(['stated to have been obtained from or is based upon trade and statistical services or other third party sources. Any data on past performance, modelling or back-testing'])
    rows.append(['contained herein is no indication as to future performance. No representation is made in respect of the assumptions or the accuracy or completeness of any modelling or'])
    rows.append(['back-testing. All opinions and estimates are given as of the date hereof and are subject to change. The value of any investment may fluctuate as a result of market changes.'])
    rows.append(['The information in this document is not intended to predict actual results and no assurances are given with respect thereto.'])
    rows.append(['This document represents our view as at the date hereof and subject to the limited scope of the assumptions and methodology set forth herein. This document has not been'])
    rows.append(['prepared in accordance with the standards and practice of any professional body in any jurisdiction and does not, and is not intended to, constitute an accounting, legal or tax opinion from Absa.'])               
    rows.append('')
    #Paragraph3 
    rows.append(['This document is not intended to be legally binding. Neither you nor your affiliates or advisers or any other person may rely on the information contained herein. Absa does not,'])
    rows.append(['through this document or the views expressed herein, owe or accept any responsibility or liability to you or your affiliates or your advisers or any other person, whether in'])
    rows.append(['contract or in tort or howsoever otherwise arising, including the use of this document in the preparation of your own financial books and records, and shall have no responsibility'])
    rows.append(['or liability to you or your affiliates or advisers or any other person for any loss or damage suffered or costs or expenses incurred (whether direct or consequential) by any person'])
    rows.append(['arising out of or in connection with the provision of this document to you, howsoever loss or damage is caused or costs or expenses are incurred.'])
    rows.append(['Absa, its affiliates and the individuals associated therewith may (in various capacities) have positions or deal in transactions or securities (or related derivatives) identical or similar to those described herein.'])             
    rows.append('')
    #Paragraph4 
    rows.append(['Absa Bank limited is registered in South Africa (all rights reserved). Copyright in this document is owned by Absa Bank Limited and is confidential, and no part of hereof may be'])
    rows.append(['reproduced, distributed or transmitted without the prior written permission of Absa Bank Limited.'])
    rows.append('')
    #Paragraph5              
    rows.append(['Absa Bank Limited is an authorised Financial Services Provider.'])    
    rows.append('')
    return rows
