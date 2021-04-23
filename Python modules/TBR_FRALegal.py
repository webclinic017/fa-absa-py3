import ael

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units     import inch, cm
from reportlab.platypus      import Paragraph, Frame, Spacer

def FRAMod1(canvas, t):
    
    canvas.setFont('Helvetica', 10)
    canvas.drawString(1.5 * cm, 16.8*cm, '1.')
    
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet()
                
    Text1 =(' ')     
    Text2 =('The purpose of this communication is to confirm the terms and conditions of the transaction referred\
             to above and entered into on the Trade Date specified below (the "Transaction") between <b>ABSA Bank\
             Limited("ABSA")</b> and <b> '+t.counterparty_ptynbr.fullname+' </b> . This communication constitutes\
             a Confirmation as referred to in the Master Agreement specified below.')
        
    bodyStyle1 =ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12,\
                spaceAfter =300, alignment = 4, leftIndent = 15)
                     
    para1 = Paragraph(Text1, bodyStyle1)
    para2 = Paragraph(Text2, bodyStyle1)
        
    mydata = [para1, para2]
           
    frame.addFromList(mydata, canvas)

def FRAMod2(canvas, t):
    
    canvas.setFont('Helvetica', 10)
    canvas.drawString(1.5 * cm, 14.83*cm, '2.')
              
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
    
    # ############# ISDA DATE ################### #
    ISDA = ''
    nbr  = t.counterparty_ptynbr.ptynbr
    a = ael.Agreement.select("counterparty_ptynbr = %i" %nbr)
    for i in a:
        if i.document_type_chlnbr == None: 
	    ISDA = '0001-01-01'
	else:
	    if i.document_type_chlnbr.entry == 'ISDA':
	    	ISDA = i.dated    
        
    Text1 =('This Confirmation supplements, forms part of, and is subject to, the ISDA Master Agreement dated as\
             of '+ str(ISDA)+', as amended and supplemented from time to time (the "Master Agreement").  All provisions \
             contained in the Master Agreement govern this Confirmation except as expressly modified below. ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =355,\
                alignment = 4, leftIndent = 15)
    
    para2  = Paragraph(Text2, bodyStyle1)
    para1  = Paragraph(Text1, bodyStyle1)
    
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
    
def FRAMod3(canvas):
    
    canvas.setFont('Helvetica', 10)
    canvas.drawString(1.5 * cm, 13.45*cm, '3.')
             
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
        
    Text1 =('Definitions')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =395,\
                 alignment = 4, leftIndent = 15)
                    
    para2  = Paragraph(Text2, bodyStyle1)
    para1  = Paragraph(Text1, bodyStyle1)
        
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
    
def FRAMod4(canvas):

    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
        
    Text1 =('This Confirmation is subject to and incorporates the 2006 ISDA Definitions and Annex to the 2006 ISDA\
            Definitions (the "Definitions") as published by the International Swap Derivatives Association, Inc. ("ISDA").\
            In the event of any inconsistency between the provisions of this Agreement and the Definitions, this\
            Agreement will prevail. In the event of any inconsistency between the Master Agreement and the Confirmation,\
            the Confirmation will prevail.')
            
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =420,\
                 alignment = 4, leftIndent = 15)
                    
    para2  = Paragraph(Text2, bodyStyle1)
    para1  = Paragraph(Text1, bodyStyle1)
        
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
    
def FRAMod5(canvas):
    
    canvas.setFont('Helvetica', 10)
    canvas.drawString(1.5 * cm, 10.25*cm, '4.')
    
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
        
    Text1 =('Relationship Between Parties.  Each party will be deemed to represent to the other party on the date on\
            which it enters into a Transaction that (absent a written agreement between the parties that expressly\
            imposes affirmative obligations to the contrary for the Transaction):- ')
            
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =485,\
                 alignment = 4, leftIndent = 15)
                    
    para2  = Paragraph(Text2, bodyStyle1)
    para1  = Paragraph(Text1, bodyStyle1)
        
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
    canvas.showPage()
    
def FRAMod6(canvas):
    
    canvas.setFont('Helvetica', 10)
    canvas.drawString(2.0 * cm, 27.4*cm, 'i)')
    canvas.drawString(2.0 * cm, 23.4*cm, 'ii)')
    canvas.drawString(2.0 * cm, 21.4*cm, 'iii)')
    canvas.drawString(2.0 * cm, 20.3*cm, 'iv)')
    
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
        
    Text2 =('Non-Reliance.  It is acting for its own account, and it has made its own independent decisions to enter\
            into that Transaction and as to whether that Transaction is appropriate or proper for it based upon its own\
            judgement and upon advice from such advisors, as it has deemed necessary. ') 
    
    Text3 =('It is not relying on any communication (written or oral) of the other party as investment advice or as a\
            recommendation to enter into that Transaction; it being understood that information and explanations related\
            to the terms and conditions of a Transaction shall not be considered investment advice or a recommendation\
            to enter into that Transaction.  It has not received from the other party any assurance or guarantee as to\
            the expected results of that Transaction. ')  
   
    Text4 =('Assessment and Understanding.  It is capable of assessing the merits of and understanding (on its own behalf\
            or through independent professional advice), and understands and accepts, the terms, conditions and risks of \
            that Transaction.  It is also capable of assuming, and assumes, the risks of that Transaction. ')
            
    Text5 =('Status of Parties.  The other party is not acting as a fiduciary for or as an advisor to it in respect of\
            that Transaction. ') 
            
    Text6 =('Contracting as Principal.  Each party represents to the other party that it will be liable as principal for\
            its obligations under this Agreement and under each Transaction. ')        
            
    bodyStyle3 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =8,\
                 alignment = 4, leftIndent = 40)
       
    para2 = Paragraph(Text2, bodyStyle3)
    para3 = Paragraph(Text3, bodyStyle3)
    para4 = Paragraph(Text4, bodyStyle3)
    para5 = Paragraph(Text5, bodyStyle3)
    para6 = Paragraph(Text6, bodyStyle3)
    
    mydata = [para2, para3, para4, para5, para6]
              
    frame.addFromList(mydata, canvas)
    canvas.showPage()

def AccountDetails(canvas, t):

    Branch     = ' '
    AccountNbr = ' '
    BranchCode = ' ' 
    Swift      = ' '
    if t.insaddr.curr.insid == 'ZAR':
        Branch = 'ABSA Eloff Street (AbsaDirect)'
        AccountNbr = '660 158 642'
        BranchCode = '632505'
        Swift = 'ABSAZAJJ'
        
    elif t.insaddr.curr.insid == 'EUR':
        Branch = 'BARCLAYS BANK LONDON'
        AccountNbr = '66986655'
        BranchCode = ''
        Swift = 'BARCGB22'
        
    elif t.insaddr.curr.insid == 'USD':
        Branch = 'BARCLAYS BANK NEW YORK'
        AccountNbr = '050038826'
        BranchCode = 'ABA026002574'
        Swift = 'BARCUS33'

    elif t.insaddr.curr.insid == 'GBP':
        Branch = 'BARCLAYS BANK LONDON'
        AccountNbr = '80642592'
        BranchCode = '//SC 20-32-53'
        Swift = 'BARCGB22'
    
    else:
        Branch = 'No Details for curr'
        AccountNbr = 'No Details for curr'
        BranchCode = 'No Details for curr'
        Swift = 'No Details for curr'
    
    p = t.counterparty_ptynbr    
    act = p.accounts()
    AName = ''
    AAccount = ''
    if len(act) > 0:
        for a in act:
            if a.accounting == 'IRD':
                AName = a.name
                AAccount = a.account
            else:
                AName = ''
                AAccount = ''    

    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(1.5 * cm, 27.43*cm, '6.') 
    canvas.drawString(2.5 * cm, 27.43*cm, 'Account Details:')
    canvas.drawString(2.5 * cm, 27.0*cm,  '(a) Payment details of ABSA Bank Limited, Johannesburg? Absadirec - '+ Swift) 
    canvas.drawString(3.0 * cm, 26.5*cm,  'Branch:') 
    canvas.drawString(3.0 * cm, 26.0*cm,  'Account no:')
    canvas.drawString(3.0 * cm, 25.5*cm,  'Branch Code:')  
    
    canvas.drawString(2.5 * cm, 24.5*cm,  '(b) Payment details to Counterparty')  
    canvas.drawString(3.0 * cm, 24.0*cm,  'Account name:')
    canvas.drawString(3.0 * cm, 23.5*cm,  'Account number:') 

    canvas.drawString(1.5 * cm, 22.5*cm, '7.') 
    canvas.drawString(2.5 * cm, 22.5*cm, 'Offices')
    canvas.drawString(2.5 * cm, 22.0*cm,  '(a) The Office of ABSA for the Transaction is:')
    canvas.drawString(3.0 * cm, 21.6*cm,  '1st Floor(3S), ABSA Towers North,180 Commissioner Stree, Johannesburg 2001.') 
    canvas.drawString(2.5 * cm, 21.0*cm,  '(b) The Office of Counterparty for the Transacion is:')
    
    canvas.drawString(6.0 * cm, 26.5*cm,  Branch) 
    canvas.drawString(6.0 * cm, 26.0*cm,  AccountNbr )
    canvas.drawString(6.0 * cm, 25.5*cm,  BranchCode)  
    
    canvas.drawString(6.0 * cm, 24.0*cm,  AName)
    canvas.drawString(6.0 * cm, 23.5*cm,  AAccount)  
    
    canvas.drawString(3.0 * cm, 20.5*cm, t.counterparty_ptynbr.fullname)
    canvas.drawString(3.0 * cm, 20.0*cm, t.counterparty_ptynbr.address)
    canvas.drawString(3.0 * cm, 19.5*cm, t.counterparty_ptynbr.address2)
    canvas.drawString(3.0 * cm, 19.0*cm, t.counterparty_ptynbr.city+' '+t.counterparty_ptynbr.zipcode)
    canvas.drawString(3.0 * cm, 18.5*cm, t.counterparty_ptynbr.country)
    
def FRAMod7(canvas, t):
    
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet()                
    
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

def FRAMod8(canvas):

    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet()                
    
    Text2 = (' ')
    
    Text1 =('i) notify Absa of any errors or discrepancies; or ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =375, alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
       
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
 
def FRAMod9(canvas):

    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet()                
    
    Text2 = (' ')
    
    Text1 =('ii) to confirm that the foregoing correctly sets forth the terms of the agreement with respect to the\
                 particular Transaction to which this Confirmation relates by signing this Confirmation and returning\
                 to facsimile (011) 350-8486/2899/2898, attention Derivative Confirmations Division; or  ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =390, alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
       
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)   
    
def FRAMod10(canvas):

    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet()                
    
    Text2 = (' ')
    
    Text1 =('iii) to achieve an exchange of Confirmations as intended by Section 9(e)(ii) of the ISDA Master Agreement\
                  by sending an authorised Confirmation in ISDA format to facsimile (011) 350-8486/2899/2898, attention\
                  Derivative Confirmations Division. ')
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
    canvas.setFont("Helvetica-Bold", 10.0)
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
    
    
