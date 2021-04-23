import ael
import time
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units     import inch, cm
from reportlab.platypus      import Paragraph, Frame, Spacer
from PIL                     import Image

def SwapMod1(canvas, t):
    
    canvas.drawString(5.0 * cm, 20.0*cm, 'Interest Rate Swap Transaction Confirmation')
    
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet()                
    Text2 = (' ')
    
    Text1 =('The purpose of this communication is to confirm the terms and conditions of the transaction referred\
             to above and entered into on the Trade Date specified below (the "Transaction") between <b>ABSA Bank\
             Limited("ABSA")</b> and <b> '+t.counterparty_ptynbr.fullname+' </b> . This communication constitutes\
             a Confirmation as referred to in the Agreement specified below.')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12,\
                spaceAfter =255, alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
       
    mydata = [para2, para1]
           
    frame.addFromList(mydata, canvas)
    
def SwapMod2(canvas, t):
    
    #ISDA Master Agreement Date
    nbr =  t.counterparty_ptynbr.ptynbr
    a = ael.Agreement.select("counterparty_ptynbr = %i" %nbr)
    ISDA = '0001-01-01'
    for i in a:
        if i.dated == ' ':
            ISDA = '0001-01-01'
        else:    
            ISDA = i.dated.to_string('%d %B %Y')
          
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
    
    canvas.setFont("Helvetica", 10.0)                
    canvas.drawString(1.5 * cm, 16.44*cm, '1.')
    
    Text1 =('This Confirmation supplements, forms part of and is subject to, the ISDA Master Agreement\
             entered into between Absa and the Counterparty dated as of <b>'+ISDA+'</b>, as amended and supplemented\
             from time to time (the Agreement). All provisions contained in the Agreement govern this\
             Confirmation except as expressly modified below.')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =310,\
                alignment = 4, leftIndent = 15)
    
    para2  = Paragraph(Text2, bodyStyle1)
    para1  = Paragraph(Text1, bodyStyle1)
    
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
    
def SwapMod3(canvas):

    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
    
    canvas.setFont("Helvetica", 10.0)                
    canvas.drawString(1.5 * cm, 14.5*cm, '2.')
    
    
    Text1 = ('<b>Definitions.</b> This Confirmation is subject to and incorporates the 2006 ISDA Definitions\
              and the Annex to the 2006 ISDA Definitions (the Definitions) as published by the International\
              Swap Derivatives Association, Inc. (ISDA). In the event of any inconsistency between the provisions\
              of this Agreement and the Definitions, this Agreement will prevail. In the event of any inconsistency\
              between this Agreement and the Confirmation, the Confirmation will prevail.')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =365,\
                alignment = 4, leftIndent = 15)
    
    para2  = Paragraph(Text2, bodyStyle1)
    para1  = Paragraph(Text1, bodyStyle1)
        
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
    canvas.showPage()
       
    
def SwapMod4(canvas):

    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
    
    canvas.setFont("Helvetica", 10.0)                
    canvas.drawString(1.5 * cm, 27.39*cm, '3.')
    canvas.drawString(1.5 * cm, 18.17*cm, '4.')
    canvas.drawString(1.5 * cm, 16.8*cm, '5.')
    
    canvas.drawString(2.5 * cm, 26.07*cm, '(i)')
    canvas.drawString(2.4 * cm, 22.4*cm, '(ii)')
    canvas.drawString(2.4 * cm, 20.4*cm, '(iii)')
    canvas.drawString(2.4 * cm, 19.3*cm, '(iv)')
    
    Text1 =('Relationship Between Parties. Each party will be deemed to represent to the other party on the date on\
            which it enters into a Transaction that (absent a written agreement between the parties that expressly imposes\
            affirmative obligations to the contrary for the Transaction):-')
    
    Text2 =('Non-Reliance. It is acting for its own account, and it has made its own independent decisions to enter\
            into that Transaction and as to whether that Transaction is appropriate or proper for it based upon its\
            own judgment and upon advice from such advisors as it has deemed necessary. It is not relying on any \
            communication (written or oral) of the other party as investment advice or as a recommendation to enter\
            into that Transaction; it being understood that information and explanations related to the terms and\
            conditions of a Transaction shall not be considered investment advice or a recommendation to enter into\
            that Transaction. It has not received from the other party any assurance or guarantee as to the expected\
            results of that Transaction.  ') 
    
    Text3 = ('Assessment and Understanding. It is capable of assessing the merits of and understanding\
            (on its own behalf or through independent professional advice), and understands and accepts, the terms,\
             conditions and risks of that Transaction. It is also capable of assuming, and assumes, the risks of that\
             Transaction.')  
   
    Text4 =('Status of Parties. The other party is not acting as a fiduciary for or as an advisor to it in respect\
            of that Transaction.')
    Text5 =('Contracting as Principal. Each party represents to the other party that it will be liable as principal\
             for its obligation under this Agreement and under each Transaction.') 
    Text6 =('ABSA and the Counterparty represent to each other that it has entered into this Transaction in reliance\
             upon such tax, regulatory, legal and financial advice as it deemed necessary and not upon any view expressed\
             by the other party.')
    Text7 =('The terms of the Transaction to which this Confirmation relates are as follows:')  
            
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)
    bodyStyle3 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =8,\
                 alignment = 4, leftIndent = 40)
    bodyStyle8 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)
         
    para1 = Paragraph(Text1, bodyStyle1)
    para2 = Paragraph(Text2, bodyStyle3)
    para3 = Paragraph(Text3, bodyStyle3)
    para4 = Paragraph(Text4, bodyStyle3)
    para5 = Paragraph(Text5, bodyStyle3)
    para6 = Paragraph(Text6, bodyStyle8)
    para7 = Paragraph(Text7, bodyStyle8)
    
    mydata = [para1, para2, para3,\
              para4, para5, para6, para7]
              
              
    frame.addFromList(mydata, canvas) 
    
def AccountDetails(canvas, t):

    canvas.setFont("Helvetica", 10.0)    
    canvas.drawString(1.5 * cm, 27.43*cm, '6.')
    canvas.setFont("Helvetica-Bold", 10.0)
    canvas.drawString(2.0 * cm, 27.43*cm, 'Account Details')
    canvas.drawString(2.0 * cm, 26.5*cm, 'Payment to ABSA:')
    
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(2.5 * cm, 26.0*cm, 'Name of Account:')
    canvas.drawString(2.5 * cm, 25.5*cm, 'Branch:')
    canvas.drawString(2.5 * cm, 25.0*cm, 'Account Number:')
    canvas.drawString(2.5 * cm, 24.5*cm, 'Branch Code:')
    
    #ABSA Account Details
    canvas.drawString(6.5 * cm, 26.0*cm, 'Absadirect - ABSAZAJJ')
    canvas.drawString(6.5 * cm, 25.5*cm, 'ABSA Bank Eloff Street')
    canvas.drawString(6.5 * cm, 25.0*cm, '660 158 642')
    canvas.drawString(6.5 * cm, 24.5*cm, '632505')
    
    canvas.setFont("Helvetica-Bold", 10.0)
    canvas.drawString(2.0 * cm, 23.5*cm, 'Payment to Counterparty:')
    
    #Counterparty Account Number
    act   = t.counterparty_ptynbr.accounts()
    CPAccountNumber = ' '
    for acc in act:
        CPAccountNumber = str(acc.account)
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(2.5 * cm, 23.0*cm, 'Account Number:')
    canvas.drawString(6.5 * cm, 23.0*cm, CPAccountNumber)
    
        
    canvas.drawString(1.5 * cm, 21.0*cm, '7.')
    canvas.setFont("Helvetica-Bold", 10.0)
    canvas.drawString(2.0 * cm, 21.0*cm, 'Offices')
    canvas.drawString(2.0 * cm, 20.5*cm, 'ABSA:')
    
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(2.0 * cm, 20.0*cm, 'Third Floor(3S) Absa Towers North')
    canvas.drawString(2.0 * cm, 19.5*cm, '180 Commissioner Street')
    canvas.drawString(2.0 * cm, 19.0*cm, 'Johannesburg 2001')
    canvas.drawString(2.0 * cm, 18.5*cm, 'South Africa')
    
    canvas.setFont("Helvetica-Bold", 10.0)
    canvas.drawString(2.0 * cm, 17.5*cm, 'Counterparty:')
    canvas.drawString(2.0 * cm, 17.0*cm, t.counterparty_ptynbr.fullname)
            
def SwapMod5(canvas, t):
    
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet()                
    h1 = styleSheet['Heading3']
    Text2 = (' ')
        
    Text1 =('Upon receipt hereof, you, the Counterparty hereby agrees to review this Confirmation (Ref No. <b>'+ str(t.trdnbr)+'</b>)\
            and either ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =350,\
                 alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
         
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)

def SwapMod6(canvas):

    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet()                
    
    Text2 = (' ')
    Text1 =('i)	notify us, ABSA of any errors or discrepancies; or ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12,\
                 spaceAfter =375, alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
       
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
 
def SwapMod7(canvas):

    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet()                
    
    Text2 = (' ')
    
    Text1 =('ii) confirm that the foregoing correctly sets forth the terms of the agreement between us with\
            respect to this particular Transaction to which this Confirmation relates by signing this Confirmation\
            and returning to facsimile +27 11 350-7941, attention Derivative Confirmations Division; or  ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =390, alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
       
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)   
    
def SwapMod8(canvas):

    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
            
    styleSheet = getSampleStyleSheet()                
    
    Text2 = (' ')
    
    Text1 =('iii) achieve an exchange of Confirmations as intended by Section 9(e)(ii) of the 2002 ISDA Form by\
            sending an authorised Confirmation in ISDA format to facsimile number +27 11 350-7941, attention Derivative\
            Confirmations Division.  ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =430, alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
       
    mydata = [para2, para1]
    frame.addFromList(mydata, canvas)   
    
    canvas.showPage()
    
def Signatures(canvas, t):

    canvas.setFont("Helvetica", 10.0)    
    canvas.drawString(1.5 * cm, 27.43*cm, 'Yours faithfully,')
    canvas.setFont("Helvetica-Bold", 8.0)
    canvas.drawString(1.5 * cm, 26.5*cm, 'Absa Bank Limited')
        
    canvas.setFont("Helvetica", 10.0)
    canvas.drawInlineImage('Y:/Jhb/Arena/Data/Confirmations/Signatures/LRoux.jpg', 1.5*cm, 24.5 *cm, 2.5*cm, 1.2*cm)
    canvas.drawString(1.5 * cm, 24.5*cm, 'L Roux')
    canvas.drawString(1.5 * cm, 24.0*cm, 'B77785')
    canvas.drawString(1.5 * cm, 23.5*cm, 'Administrator')
    canvas.drawString(1.5 * cm, 23.0*cm, 'Confirmations')
    canvas.drawString(1.5 * cm, 22.5*cm, 'VAT No. 4940112230')
    
    canvas.drawInlineImage('Y:/Jhb/Arena/Data/Confirmations/Signatures/MJacobs.jpg', 1.5*cm, 20.5 *cm, 2.5*cm, 1.2*cm)
    canvas.drawString(1.5 * cm, 20.5*cm, 'M R Jacobs')
    canvas.drawString(1.5 * cm, 20.0*cm, 'A74349')
    canvas.drawString(1.5 * cm, 19.5*cm, 'Team Leader')
    canvas.drawString(1.5 * cm, 19.0*cm, 'Confirmations')
    canvas.drawString(1.5 * cm, 18.5*cm, 'VAT No. 4940112230')
    
    canvas.drawString(1.5 * cm, 17.5*cm, 'Agreed and Accepted By:')
    canvas.setFont("Helvetica-Bold", 10.0)
    canvas.drawString(1.5 * cm, 17.0*cm, t.counterparty_ptynbr.fullname)
    
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(1.5 * cm, 15.5*cm, 'Name: '+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 14.5*cm, 'signed:'+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 13.5*cm, 'Title:    '+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 12.5*cm, 'Date:   '+'           '+ '_'*25)
    
    canvas.drawString(1.5 * cm, 11.0*cm, 'Name: '+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 10.0*cm, 'signed:'+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 9.0*cm, 'Title:    '+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 8.0*cm, 'Date:   '+'           '+ '_'*25)
    
    canvas.showPage()  
    
