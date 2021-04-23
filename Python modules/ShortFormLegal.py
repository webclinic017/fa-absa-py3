import ael
import time
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units     import inch, cm
from reportlab.platypus      import Paragraph, Frame, Spacer
from STATIC_TEMPLATE         import BuildLogos, BuildFooter
from zak_funcs               import formnum
from PIL                     import Image


def ShortMod1(canvas, t):
    
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet()                
    
    Text1 = (' ')
    Text2 =('The purpose of this letter agreement (this "Confirmation") is to confirm the terms and conditions of the\
             transaction referred to above and entered into on the Trade Date specified below ("this Transaction"), between\
             <b>Absa Bank Limited ("ABSA")</b> and <b>' + t.counterparty_ptynbr.fullname +' </b><b>("Counterparty")</b>.  This Confirmation supersedes any previous Confirmation\
             or other communication with respect to this Transaction and evidences a complete and binding agreement between \
             us as to the terms of this Transaction.  This communication constitutes a Confirmation as referred to in the\
             Agreement specified below.')
    
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12,\
                spaceAfter =255, alignment = 4)
    
    para1 = Paragraph(Text1, bodyStyle1)
    para2 = Paragraph(Text2, bodyStyle1)
       
    mydata = [para1, para2]
           
    frame.addFromList(mydata, canvas)
    
def ShortMod2(canvas, t):
    
    #ISDA Master Agreement Date
    nbr =  t.counterparty_ptynbr.ptynbr
    a = ael.Agreement.select("counterparty_ptynbr = %i" %nbr)
    ISDA = '0001-01-01'
    for i in a:
        if i.dated == ' ':
            ISDA = '0001-01-01'
        else:    
            ISDA = i.dated.to_string('%d %B %Y')
          
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0 )
    
    canvas.setFont("Helvetica", 10.0)                
    canvas.drawString(1.5 * cm, 15.73*cm, '1.')
    Text2 =   ('This Confirmation supplements, forms a part of and is subject to, the ISDA Master Agreement\
                entered into between Absa and the Counterparty dated as of <b>'+ISDA+'</b>, as amended and supplemented\
                from time to time (the "Agreement"). All provisions contained in the Agreement govern this\
                Confirmation except as expressly modified below.')
    Text1 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =330,\
                alignment = 4, leftIndent = 15)
    
    para1  = Paragraph(Text1, bodyStyle1)
    para2  = Paragraph(Text2, bodyStyle1)
    
    mydata = [para1, para2]
    
    frame.addFromList(mydata, canvas)
    
def ShortMod3(canvas):
    
    canvas.drawString(4.5 * cm, 20.0*cm, 'OTC Currency Option Transaction') # Subject
    
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
    canvas.setFont("Helvetica", 10.0)                
    canvas.drawString(1.5 * cm, 14.0*cm, '2.')
    Text1 =   ('<b>Definitions.</b> This Confirmation is subject to and incorporates the 2006 ISDA Definitions as\
               published by the International Swap Derivatives Association, Inc. ("ISDA") and the 1998 FX and Currency\
               Option Definitions as published by ISDA, the Emerging Markets Traders Association and The Foreign Exchange\
               Committee (the "FX Definitions", and together with the 2006 Definitions, the "Definitions"). In the event\
               of any inconsistency between this Confirmation and the Definitions or the Agreement, this Confirmation will\
               govern for the purposes of the Transaction. In the event of any inconsistency between the 2000 Definitions\
               and the FX Definitions, the FX Definitions will govern. References herein to a "Transaction" shall be\
               deemed to be references to a "Swap Transaction" for the purposes of the Definitions. Capitalised terms\
               used in this Confirmation and not defined in this Confirmation or the Definitions shall have the respective\
               meanings assigned in the Agreement."')
               
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =380,\
                alignment = 4, leftIndent = 15)
    
    para1  = Paragraph(Text1, bodyStyle1)
    para2  = Paragraph(Text2, bodyStyle1)
    
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
    canvas.showPage() 
    
def ShortMod4(canvas):

    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
    
    canvas.setFont("Helvetica", 10.0)                
    canvas.drawString(3.4 * cm, 23.3*cm, '(ii)')
    canvas.drawString(4.1 * cm, 20.39*cm, '(a)')
    canvas.drawString(4.1 * cm, 19.45*cm, '(b)')
    canvas.drawString(4.1 * cm, 18.53*cm, '(c)')
    canvas.drawString(3.4 * cm, 15.93*cm, '(iv) ')
    canvas.drawString(3.4 * cm, 14.5*cm, '(i) ')
    canvas.drawString(3.4 * cm, 13.65*cm, '(ii) ')
    canvas.drawString(3.4 * cm, 12.2*cm, '(i) ')
    canvas.drawString(3.4 * cm, 11.29*cm, '(ii) ')
    
    Text1 =('4. <b>Additional Representations:</b>')
    Text3 =('Additional Representations, as defined and contemplated in the Agreement, will apply and for the purpose\
            of Section 3 of the Agreement, each of the following will constitute an Additional Representation in respect\
            of this Transaction. In respect of each Additional Representation each of us as a party to the Transaction\
            represents to the other on the date on which this Transaction is entered into and will be deemed to\
            represent continuously for the duration of the term of this Transaction and at all times until the \
            termination of this Transaction that:')
    Text4 =('4.1 <b>Non Reliance.</b>  ') 
    Text5 =('(i) Each of us is acting for its own account, ')  
    Text6 =(' Each of us has made its own independent decisions based upon its own judgment and upon advice from such\
                  advisors as it has deemed necessary to obtain as to whether or not:')
    Text7 =('(a) to enter into this Transaction,')
    Text8 =('(b) it is suitable, appropriate or proper to enter in this Transaction,')
    Text9 =('(c) it has the capacity to enter into this Transaction;')
    Text10  =('(iii) Each of us has entered into this Transaction:')
    Text11  =(' in reliance upon such investment, financial, legal, regulatory, tax, accounting, actuarial and other advice as it deemed necessary;') 
    Text12  =(' not relying in any manner on any view, proposal, guidance, advice or opinion expressed by the other one of us;')
    Text13  =(' not relying in any manner on any communication (written or oral) of the other one of us as investment,\
                   financial, legal, regulatory, tax, accounting, actuarial and other advice, it being understood that any\
                   information and explanations relating to the terms and conditions of this Transaction shall not be \
                   considered or construed as investment, financial, legal, regulatory, tax, accounting, actuarial and \
                   other advice or as a proposal, guidance or recommendation to enter into this Transaction;') 
    Text14 =('  None of us has received from the other one any assurance, warranty or guarantee as to the expected\
                  results or financial or investment returns of or related to this Transaction.')
    Text15 =('4.2 <b>Assessment and Understanding.</b>')  
    Text16 =('Each of us is capable of assessing the merits of and understanding, and in fact understands and\
                   accepts the terms, conditions of, associated with and related to this Transaction; and') 
    Text17 =('Each of us is capable of assessing and assuming the risks of whatsoever nature, and in fact\
                    accepts and assumes all the risks of, associated with and related to this Transaction.')
    Text18 =('4.3 <b>Status of Parties.</b>')
    Text19 =(' None of us is acting as a fiduciary for or as an advisor of whatsoever nature or kind to the other\
                one of us in respect of this Transaction;') 
    Text20 =(' Each of us will be liable as principal for its own obligations under this Transaction read with\
                the Agreement and schedule elections incorporated by reference in this Confirmation.')
    Text21 =('4.4 <b> Purpose.</b>') 
    Text22 =('Each of us has entered into this Transaction:') 
    Text23 =('(i) for the purpose of managing its borrowings or investments, and/or')
    Text24 =('(ii) for the purpose of hedging its assets or liabilities; and/or')
    Text25 =('(iii) in connection with a line of its business.')
            
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)
    bodyStyle2 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)
    bodyStyle3 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 40)
    bodyStyle4 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 55, bulletIndent = 18)
    bodyStyle5 = ParagraphStyle('Text', spaceBefore=4, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 40)
    bodyStyle6 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)         
    bodyStyle7 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 75)  
    bodyStyle8 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 67)  
    bodyStyle9 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 87) 
    bodyStyle10 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 70)         
     
    para1  = Paragraph(Text1, bodyStyle1)
    para3  = Paragraph(Text3, bodyStyle2)
    para4  = Paragraph(Text4, bodyStyle3)
    para5  = Paragraph(Text5, bodyStyle4)
    para6  = Paragraph(Text6, bodyStyle8)
    para7  = Paragraph(Text7, bodyStyle7)
    para8  = Paragraph(Text8, bodyStyle7)
    para9  = Paragraph(Text9, bodyStyle7)
    para10 = Paragraph(Text10, bodyStyle4)
    para11 = Paragraph(Text11, bodyStyle9)
    para12 = Paragraph(Text12, bodyStyle9)
    para13 = Paragraph(Text13, bodyStyle9)
    para14 = Paragraph(Text14, bodyStyle10)
    para15 = Paragraph(Text15, bodyStyle3)
    para16 = Paragraph(Text16, bodyStyle10)
    para17 = Paragraph(Text17, bodyStyle10)
    para18 = Paragraph(Text18, bodyStyle3)
    para19 = Paragraph(Text19, bodyStyle10)
    para20 = Paragraph(Text20, bodyStyle10)
    para21 = Paragraph(Text21, bodyStyle3)
    para22 = Paragraph(Text22, bodyStyle4)
    para23 = Paragraph(Text23, bodyStyle4)
    para24 = Paragraph(Text24, bodyStyle4)
    para25 = Paragraph(Text25, bodyStyle4)
    
    mydata = [para1, para3, para4, para5, para6,\
              para7, para8, para9, para10, para11,\
              para12, para13, para14, para15, para16,\
              para17, para18, para19, para20, para21, para22,\
              para23, para24, para25]
              
    frame.addFromList(mydata, canvas) 
    canvas.showPage()
        
def ShortMod5(canvas):

    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
    
    canvas.setFont("Helvetica", 10.0)                
    canvas.drawString(3.4 * cm, 21.78*cm, '(b)')
    canvas.drawString(3.4 * cm, 19.9*cm, '(d)')
    canvas.drawString(3.4 * cm, 17.5*cm, '(b)')
    
    Text1 =('5. <b>Additional Termination Events:</b>')
    Text2 =('You represent to us on the date on which this Transaction is entered into and will be deemed to represent\
             continuously for the duration of the term of this Transaction and at all times until the termination of this\
             Transaction that:')
    Text3 =('5.1 you are not a sanctioned entity; and ')         
    Text4 =('5.2 this Transaction is not a sanctioned transaction.')
    Text5 =('Notwithstanding the provisions of the Agreement, including but not limited to Section 5(c)(ii) of the\
              Agreement, any misrepresentation in respect of paragraph 5.1 and 5.2 above shall constitute an Illegality\
              as contemplated in Section 5(b)(i) of the Agreement with this Transaction as the Affected Transaction.')
    Text6 =('For purposes of these representations:')
    Text7 =('<b><i>"sanctioned entity"</i></b> means an entity that:')
    Text8 =('(a) is listed in any sanction list and/or')
    Text9 =(' is subject to some form of financial or economic limitations, or in respect of which there is some form\
                 of financial or economic limitation on other parties dealing with it, in terms of the applicable law and/or ')        
    Text10 =('(c) is located or incorporated in a sanctioned jurisdiction and/or ')
    Text11 =(' is owned or controlled by an entity that is located or incorporated in a sanctioned jurisdiction and/or ')
    Text12 =('(e) undertakes significant business activity in a sanctioned jurisdiction;')
    Text13 =('<b><i>"sanctioned jurisdiction "</i></b> means a country or territory:')
    Text14 =('(a) that is listed in a sanction list and/or ')            
    Text15 =(' in respect of which there is some form of financial or economic limitation on other persons or \
                  countries dealing with or making payments or deliveries to or receiving payments or deliveries from\
                  such country or territory, in terms of the applicable law;')
    Text16 =('<b><i>"sanction list"</i></b> means any of the sanction lists of HM Treasury in the United Kingdom\
                  of Britain and Northern Ireland, the Bank of England, the Office of Foreign Asset Control and/or the\
                  United Nations Security Council (each as amended, supplemented or substituted from time to time); and')              
    Text17 =('<b><i>"sanctioned transaction"</i></b> means any payment, receipt or delivery of cash or assets to or\
                  from an entity that is a sanctioned entity or is located within a sanctioned jurisdiction;')
    Text18 =('<b><i>"applicable law"</i></b> as contemplated in Section 5(b)(i) of the Agreement and any related sections\
                  of the Agreement and this Confirmation includes, without limitation, all laws, regulations, rules,\
                  directives and policies regarding the combating of criminal activities, money laundering and terrorist\
                  financing issued by any statutory, regulatory, supervisory and/or other governmental agency of any\
                  country in which payment, delivery or compliance is required by either one of us or any Credit Support\
                  Provider of any one of us, as the case may be."')                
            
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)
    bodyStyle2 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)
    bodyStyle3 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 40)
    bodyStyle4 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 55)
    bodyStyle5 = ParagraphStyle('Text', spaceBefore=4, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 40)
    bodyStyle6 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)         
    bodyStyle7 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 75)  
    bodyStyle8 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 70)
     
    para1  = Paragraph(Text1, bodyStyle1)
    para2  = Paragraph(Text2, bodyStyle2)
    para3  = Paragraph(Text3, bodyStyle2)
    para4  = Paragraph(Text4, bodyStyle2)
    para5  = Paragraph(Text5, bodyStyle2)
    para6  = Paragraph(Text6, bodyStyle2)
    para7  = Paragraph(Text7, bodyStyle2)
    para8  = Paragraph(Text8, bodyStyle4)
    para9  = Paragraph(Text9, bodyStyle8)
    para10 = Paragraph(Text10, bodyStyle4)
    para11 = Paragraph(Text11, bodyStyle8)
    para12 = Paragraph(Text12, bodyStyle4)
    para13 = Paragraph(Text13, bodyStyle2)
    para14 = Paragraph(Text14, bodyStyle4)
    para15 = Paragraph(Text15, bodyStyle8)
    para16 = Paragraph(Text16, bodyStyle2)
    para17 = Paragraph(Text17, bodyStyle2)
    para18 = Paragraph(Text18, bodyStyle2)
    
    mydata = [para1, para2, para3, para4, para5,\
              para6, para7, para8, para9, para10,\
              para11, para12, para13, para14, para15,\
              para16, para17, para18]
              
    frame.addFromList(mydata, canvas) 
    canvas.showPage()
    
def AccountDetails(canvas, t):

    canvas.setFont("Helvetica", 10.0)    
    canvas.drawString(1.5 * cm, 27.43*cm, '8.')
    canvas.setFont("Helvetica-Bold", 8.0)
    canvas.drawString(2.0 * cm, 27.43*cm, 'Account Details')
    canvas.drawString(2.0 * cm, 26.5*cm, 'Payment to ABSA:')
    
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(2.5 * cm, 26.0*cm, 'Name of Account:')
    canvas.drawString(2.5 * cm, 25.5*cm, 'Account Number:')
    canvas.drawString(2.5 * cm, 25.0*cm, 'Branch Code:')
    
    #ABSA Account Details
    canvas.drawString(6.5 * cm, 26.0*cm, 'Absadirect - ABSAZAJJ')
    canvas.drawString(6.5 * cm, 25.5*cm, '660 158 642')
    canvas.drawString(6.5 * cm, 25.0*cm, '632505')
    
    canvas.setFont("Helvetica-Bold", 10.0)
    canvas.drawString(2.0 * cm, 23.5*cm, 'Payment to Counterparty:')
    
    #Counterparty Account Number
    act   = t.counterparty_ptynbr.accounts()
    CPAccountNumber = ' '
    for acc in act:
        CPAccountNumber = str(acc.account)
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(2.0 * cm, 23.0*cm, 'Please provide payment details to ABSA by sending it to facsimile number +27 11 350-7941, for attention ')
    canvas.drawString(2.0 * cm, 22.6*cm, 'Settlements Department')
    
        
    canvas.drawString(1.5 * cm, 21.0*cm, '9.')
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
    


def ShortMod6(canvas, t):
    
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet()                
    h1 = styleSheet['Heading3']
    Text2 = (' ')
        
    Text1 =('Upon receipt hereof, the Counterparty hereby agrees to review this Confirmation (Ref No. <b>'+ str(t.trdnbr)+'</b>)\
            and to either ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =350,\
                 alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
         
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)

def ShortMod7(canvas):

    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet()                
    
    Text2 = (' ')
    Text1 =('i)	notify ABSA of any errors or discrepancies; or ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12,\
                 spaceAfter =375, alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
       
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
 
def ShortMod8(canvas):
    
    canvas.setFont("Helvetica", 10.0)                
    canvas.drawString(1.5 * cm, 13.58*cm, 'ii)')
    
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet()                
    
    Text2 = (' ')
    
    Text1 =(' confirm that the foregoing correctly sets forth the terms of the agreement between us with\
            respect to this particular Transaction to which this Confirmation relates by signing this Confirmation\
            and returning to facsimile +27 11 350-7941, attention Derivative Confirmations Division; or  ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =390,\
                alignment = 4, leftIndent = 10)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
       
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)   
    
def ShortMod9(canvas):

    canvas.setFont("Helvetica", 10.0)                
    canvas.drawString(1.4*cm, 12.2*cm, 'iii)')
    
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
            
    styleSheet = getSampleStyleSheet()                
    
    Text2 = (' ')
    
    Text1 =('  achieve an exchange of Confirmations as intended by Section 9(e)(ii) of the 2002 ISDA Form by\
            sending an authorised Confirmation in ISDA format to facsimile number +27 11 350-7941, attention Derivative\
            Confirmations Division.  ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=10, leading=12, spaceAfter =430\
                , alignment = 4, leftIndent = 10)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
       
    mydata = [para2, para1]
    frame.addFromList(mydata, canvas)   
    
    canvas.showPage()
    
def Disclaimer(canvas):

    
    frame = Frame(  0.5*inch,        
                    1*inch,          
                    7*inch,          
                    10*inch,         
                    showBoundary =0  
                    )
    Text1  =('<b>THIS IS AN IMPORTANT NOTICE - PLEASE READ CAREFULLY</b>')
    Text3  =('<font fontSize =7>The information disclosures provided by you were used to conclude this transaction to ensure that your\
              financial needs and objectives were met.  You acknowledge that the product is appropriate and adequate\
              and no advice, as defined by Financial Advisory and Intermediary Services Act, 37 of 2002 (FAIS) was \
              required to be provided by Absa Bank Limited ("Absa Bank") to you.  The investment/transaction/products \
              may involve a high degree of risk including, but not limited to, the risk of (a) low or no investment\
              returns, (b) capital loss, (c) counterparty or issuer default, (d) adverse or unanticipated financial \
              market fluctuations, (e) inflation and (f) currency exchange. The value of any investment/transaction\
              (product) may fluctuate daily as a result of these risks. Absa Bank does not predict any (actual) results,\
              performances and/or financial returns and gives no assurances, warranties or guarantees in this regard.\
              Any information on past financial returns, modeling or back-testing is no indication of future returns\
              or performance.</font>')
    
    Text4  =('Please take note of the following:') 
    
    Text5  =('1.The Financial Services Provider, Absa Bank is a duly authorised Category 1 Financial Services Provider.')  
    
    Text6  =('2.Complaints:')
    
    Text7  =('2.1 Should you be dissatisfied with the service rendered by the Absa representative, you may lodge\
            a complaint with Action Line on the following number:  0800 414141 or fax 012 367 1212. The complaints\
            policy and procedure is available to you upon request.')
    
    Text8  =('2.2 Should you be dissatisfied with the outcome communicated to you in writing as the investigation may \
             be unfavourable to you, you may, within six months of receiving the written notice, pursue the complaint \
            with the relevant Ombuds office. The Ombuds contact details are:\
            Tel:	0860FAISOM / 0860324766	Fax:	012 348 3447\
            Email:	info@faisombud.co.za')
    
    Text9  =('3.	Absa Bank has professional indemnity insurance cover.')
    Text10 =('4.Absa Bank does not assume responsibility for the performance of investments nor for the timing of portfolio changes.')
    
    Text12 =('5.The details of the Absa Bank Compliance Department are as follows:\
                Tel:	 011 350 4355	Fax:	011 350 7419')
    
    Text13 =('6.The financial service rendered was in accordance with the FAIS Act General code of conduct.')  
    Text14 =('7.The Absa Bank Representative has been registered with the Financial Services Board.')   
    Text15 =('8.The Absa Bank representative has utilised his or her professional knowledge and ability to provide\
                the appropriate service to you and has taken all reasonable steps to ensure your fair treatment.')
    Text16 =('9.The Absa Bank representative declared that he/she is a permanent employee and declared that no\
                other personal interest in concluding this transaction exists. Further, there are no circumstances\
                that may give rise to an actual or potential conflict of interest.')  
    Text17 =('10.The Absa Bank representative declared that, should a personal interest exist (other than the receipt \
                of commission and/or fees), he/she undertook to inform the customer of the nature of the conflict and \
                take all reasonable steps to ensure fair treatment to the customer. ')    
    Text18 =('11.Should you encounter a possible misrepresentation, non-disclosure of a material fact or the \
                inclusion of incorrect information, please communicate this incident in writing to the Absa Action Line.')    
    Text19 =('12.In the event that the financial product recommended is a replacement product the Absa Representative\
                fully disclosed to you the actual and potential financial implications, costs and consequences of such\
                a replacement.') 
    Text20 =('13.In the event that a full analysis could not be undertaken there may be limitations on the\
                appropriateness of the financial product you selected.  You should take particular care to consider\
                on your own whether the financial product is appropriate considering your objectives, financial \
                situation and particular needs.')

   
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=7, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 120)
    bodyStyle2 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=7, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)
    bodyStyle3 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=7, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)
    bodyStyle4 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=7, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)
    bodyStyle5 = ParagraphStyle('Text', spaceBefore=4, fontName='Helvetica', fontSize=7, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 40)
    bodyStyle6 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=7, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)         
  
    para1  = Paragraph(Text1, bodyStyle1)
    para3  = Paragraph(Text3, bodyStyle2)
    para4  = Paragraph(Text4, bodyStyle3)
    para5  = Paragraph(Text5, bodyStyle4)
    para6  = Paragraph(Text6, bodyStyle4)
    para7  = Paragraph(Text7, bodyStyle5)
    para8  = Paragraph(Text8, bodyStyle5)
    para9  = Paragraph(Text9, bodyStyle3)
    para10 = Paragraph(Text10, bodyStyle3)
    para12 = Paragraph(Text12, bodyStyle3)
    para13 = Paragraph(Text13, bodyStyle6)
    para14 = Paragraph(Text14, bodyStyle6)
    para15 = Paragraph(Text15, bodyStyle6)
    para16 = Paragraph(Text16, bodyStyle6)
    para17 = Paragraph(Text17, bodyStyle6)
    para18 = Paragraph(Text18, bodyStyle6)
    para19 = Paragraph(Text19, bodyStyle6)
    para20 = Paragraph(Text20, bodyStyle6)
    
    mydata = [para1, para3, para4, para5, para6, para7, para8, para9, para10,\
            para12, para13, para14, para15, para16, para17, para18, para19, para20]
            
    frame.addFromList(mydata, canvas)     
