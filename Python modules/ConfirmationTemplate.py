import ael
import time
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units     import inch, cm
from reportlab.platypus      import Paragraph, Frame, Spacer
from STATIC_TEMPLATE         import BuildLogos, BuildFooter
from zak_funcs               import formnum
from PIL                     import Image

#--------------------------------------------------#
# FOOTER AND  ABCAP AND BARCAP LOGOS ON FIRST PAGE
#--------------------------------------------------#

def FirstPageLF(c):

    BuildLogos(c)
    BuildFooter(c)
    
def FirstPageHeader(canvas, t):
    
    #Confirmation Title
    canvas.setFont('Helvetica-Bold', 12)
    canvas.drawString(8.5 * cm, 24.5*cm, 'CONFIRMATION')
    
    #Counterparty Header Details
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(1.5 * cm, 23.5*cm, 'DATE:')
    canvas.drawString(1.5 * cm, 23.0*cm, 'TO:')
    canvas.drawString(1.5 * cm, 22.5*cm, 'ATT:')
    canvas.drawString(1.5 * cm, 22.0*cm, 'TEL:')
    canvas.drawString(1.5 * cm, 21.5*cm, 'FAX:')
    canvas.drawString(1.5 * cm, 21.0*cm, 'E-MAIL:')
    canvas.drawString(1.5 * cm, 20.5*cm, 'FROM:')
    canvas.drawString(1.5 * cm, 20.0*cm, 'SUBJECT:')
    canvas.drawString(1.5 * cm, 19.5*cm, 'REFERENCE NO:')
    
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(4.5 * cm, 20.5*cm, 'Absa Bank Limited, Johannesburg')
    canvas.drawString(4.5 * cm, 20.0*cm, 'OTC Currency Option Transaction')
    
    #Draws line under Header Details
    canvas.line(1.5*cm, 19.0*cm, 18.8*cm, 19.0*cm)
    
#-----------------------------------------------------------------------------#
#   Counterparty Header Details on first page
#-----------------------------------------------------------------------------# 
    
    DATE        = str(ael.date_today().to_string('%d %B %Y'))
    TO          = t.counterparty_ptynbr.fullname
    ATT         = t.counterparty_ptynbr.attention
    TEL         = t.counterparty_ptynbr.telephone
    TELEPHONE   = TEL[0:3].replace('+27', '0')+TEL[3:5] + ' '+TEL[5:8]+ '-'+TEL[8:]
    FAX         = t.counterparty_ptynbr.fax
    FAXNUMBER   = FAX[0:3].replace('+27', '0')+FAX[3:5] + ' '+FAX[5:8]+ '-'+FAX[8:]
    FROM        = 'Absa Bank Limited, Johannesburg'
    EMAIL       = t.counterparty_ptynbr.email
    REFERENCENO = str(t.trdnbr) 
    
    canvas.drawString(4.5 * cm, 23.5*cm, DATE)
    canvas.drawString(4.5 * cm, 23.0*cm, TO)
    canvas.drawString(4.5 * cm, 22.5*cm, ATT)
    canvas.drawString(4.5 * cm, 22.0*cm, TELEPHONE)
    canvas.drawString(4.5 * cm, 21.5*cm, FAXNUMBER)
    canvas.drawString(4.5 * cm, 21.0*cm, EMAIL)
    canvas.drawString(4.5 * cm, 19.5*cm, REFERENCENO)

# ---------------------------------------------------------------------------------#
#       First Paragraph on first Page,for both short-form and long form confo's
#----------------------------------------------------------------------------------#    
def LongShortPara1(canvas, t):
    
    frame = Frame(  0.5*inch,        # x
                    1*inch,          # y at bottom
                    7*inch,          # width
                    10*inch,         # height
                    showBoundary =0  #Helps to see the frame where text will be written
                    )
                    
    styleSheet = getSampleStyleSheet()                
    h1 = styleSheet['Heading3']
    Text2 = (' ')
    
    Text1 = ('The purpose of this communication ("this Confirmation") is to confirm the terms and conditions of the \
            transaction referred to above and entered into on the Trade Date specified below (this "Transaction"), between us, \
            <b>Absa Bank Limited ("ABSA")</b>, and you,<b> '+t.counterparty_ptynbr.fullname+' </b> .This Confirmation supersedes any previous\
            Confirmation or other communication with respect to this Transaction and evidences a complete and binding \
            agreement between us as to the terms of this Transaction.  This communication constitutes a Confirmation as referred \
            to in the Agreement specified below.')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=8, leading=12,\
                spaceAfter =255, alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
       
    mydata = [para2, para1]
           
    frame.addFromList(mydata, canvas)
    
def ShortFormPara1(canvas, t):
    
    #ISDA Master Agreement Date
    nbr =  t.counterparty_ptynbr.ptynbr
    a = ael.Agreement.select("counterparty_ptynbr = %i" %nbr)
    ISDA = '0001-01-01'
    for i in a:
        if i.dated == ' ':
            ISDA = '0001-01-01'
        else:    
            ISDA = i.dated.to_string('%d %B %Y')
          
    frame = Frame(  0.5*inch,        # x
                    1*inch,          # y at bottom
                    7*inch,          # width
                    10*inch,         # height
                    showBoundary =0  #Helps to see the frame where text will be written
                    )
    canvas.setFont("Helvetica", 8.0)                
    canvas.drawString(1.5 * cm, 16.15*cm, '1.')
    Text1 =   ('This Confirmation supplements, forms part of and is subject to, the ISDA Master Agreement\
                entered into between Absa and the Counterparty dated as of <b>'+ISDA+'</b>, as amended and supplemented\
                from time to time (the "Agreement"). All provisions contained in the Agreement govern this\
                Confirmation except as expressly modified below.')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =320,\
                alignment = 4, leftIndent = 15)
    
    para2  = Paragraph(Text2, bodyStyle1)
    para1  = Paragraph(Text1, bodyStyle1)
    
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
    
def ShortFormPara2(canvas):

    frame = Frame(  0.5*inch,        # x
                    1*inch,          # y at bottom
                    7*inch,          # width
                    10*inch,         # height
                    showBoundary =0  #Helps to see the frame where text will be written
                    )
    canvas.setFont("Helvetica", 8.0)                
    canvas.drawString(1.5 * cm, 14.73*cm, '2.')
    Text1 =   ('<b>Definitions.</b>  This Confirmation is subject to and incorporates the 2006 ISDA Definitions\
                (the "Definitions") as published by the International Swap Derivatives Association, Inc. ("ISDA"). \
                In the event of any inconsistency between the provisions of the Agreement and the Definitions, the \
                Agreement will prevail. In the event of any inconsistency between the Agreement and the Confirmation,\
                the Confirmation will prevail.')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =360,\
                alignment = 4, leftIndent = 15)
    
    para2  = Paragraph(Text2, bodyStyle1)
    para1  = Paragraph(Text1, bodyStyle1)
    
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
       
    
def ShortFormPara3(canvas):

    frame = Frame(  0.5*inch,        # x
                    1*inch,          # y at bottom
                    7*inch,          # width
                    10*inch,         # height
                    showBoundary =0  #Helps to see the frame where text will be written
                    )
    canvas.drawString(1.5 * cm, 12.79*cm, '3.')                
    Text1 =   ('Each of ABSA and the Counterparty represent to the other that it has entered into this Transaction\
                in reliance upon such tax, regulatory, legal, financial and investment advice as it deemed necessary \
                to obtain and not upon any view, option or proposal expressed by the other party.')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =415,\
                alignment = 4, leftIndent = 15)
    
    para2  = Paragraph(Text2, bodyStyle1)
    para1  = Paragraph(Text1, bodyStyle1)
    
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)    
   
    
def ShortFormPara4(canvas):

    frame = Frame(  0.5*inch,        # x
                    1*inch,          # y at bottom
                    7*inch,          # width
                    10*inch,         # height
                    showBoundary =0  #Helps to see the frame where text will be written
                    )
    canvas.drawString(1.5 * cm, 11.4*cm, '4.')                
    Text1 =   ('The Counterparty represents to ABSA that it is entering into this Transaction for the purpose\
                of managing its borrowings or investments, hedging its assets or liabilities or in connection \
                with a line of its business.')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =455,\
                alignment = 4, leftIndent = 15)
    
    para2  = Paragraph(Text2, bodyStyle1)
    para1  = Paragraph(Text1, bodyStyle1)
    
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
    canvas.showPage()
#---------------------------------------------------------------------------------------------------------#
#                                     END OF FIRST PAGE
#---------------------------------------------------------------------------------------------------------#   

#---------------------------------------------------------------------------------------------------------#
#                                TRANSACTION TERMS ON SECOND PAGE OF SHORT FORM CONFO  
#---------------------------------------------------------------------------------------------------------#
def TransactionTerms(canvas, t):

    #Transaction Terms static data
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(1.5 * cm, 27.43*cm, '5.')               
    canvas.drawString(2.0 * cm, 27.43*cm, 'The terms of the Transaction to which this Confirmation relates are as folllows:')  
    canvas.drawString(2.0 * cm, 26.5*cm, 'Trade Date:')
    canvas.drawString(2.0 * cm, 25.5*cm, 'Buyer:')
    canvas.drawString(2.0 * cm, 24.5*cm, 'Seller:')
    canvas.drawString(2.0 * cm, 23.5*cm, 'Currency Option Style:')
    canvas.drawString(2.0 * cm, 22.5*cm, 'Currency Option type:')
    canvas.drawString(2.0 * cm, 21.5*cm, 'Call Currency and Call Currency Amount:')
    canvas.drawString(2.0 * cm, 20.5*cm, 'Put Currency and Put Currency Amount:')
    canvas.drawString(2.0 * cm, 19.5*cm, 'Strike Price:')
    canvas.drawString(2.0 * cm, 18.5*cm, 'Expiration Date:')
    canvas.drawString(2.0 * cm, 17.5*cm, 'Expiration Time:')
    canvas.drawString(2.0 * cm, 16.5*cm, 'Settlement Date:')
    canvas.drawString(2.0 * cm, 15.5*cm, 'Premium Amount:')
    canvas.drawString(2.0 * cm, 14.5*cm, 'Premium Payment Date:')
    canvas.drawString(2.0 * cm, 13.5*cm, 'Calculation Agent:')
    
    #Page Number
    canvas.setFont("Helvetica", 8.0)
    pageNumber = canvas.getPageNumber()
    canvas.drawString(10*cm, cm, str(pageNumber))

    #--------------------------------------------------------------------------------#
    #                                   TRANSACTION TERMS
    #--------------------------------------------------------------------------------#
    TradeDate  = str(time.strftime('%d.%m.%Y', time.localtime(t.time)))
    
    Buyer  = ' '
    Seller = ' '    
    if t.quantity > 0:
        (Buyer, Seller)  = ('ABSA BANK LIMITED ', t.counterparty_ptynbr.fullname)
    else:
        (Buyer, Seller)  = (t.counterparty_ptynbr.fullname, 'ABSA BANK LIMITED ')
        
    CurrencyOptionStyle = t.insaddr.exercise_type
    
    PutCurrency  = ' '
    CallCurrency = ' '
    if t.insaddr.call_option == 1:
        PutCurrency, CallCurrency  = (t.insaddr.curr.insid, t.insaddr.und_insaddr.insid)
    else:
        PutCurrency, CallCurrency  = (t.insaddr.und_insaddr.insid, t.insaddr.curr.insid)
          
    CurrencyOptionType = PutCurrency + ' Put ' + CallCurrency + ' Call '
    
    PutAmount  = 0.0
    CallAmount = 0.0
    if t.insaddr.call_option == 1:
        PutAmount, CallAmount = (t.quantity*t.insaddr.strike_price, t.quantity)
    else:
        PutAmount, CallAmount = (t.quantity, t.quantity*t.insaddr.strike_price)
        
    CallCurrencyAmount = str(CallCurrency) +' '+str(formnum(abs(CallAmount)))
    PutCurrencyAmount  = str(PutCurrency)  +' '+ str(formnum(abs(PutAmount)))
    StrikePrice        = str(t.insaddr.strike_price)
    ExpirationDate     = str(t.insaddr.exp_day.to_string('%d.%m.%Y'))
    ExpirationTime     = '10:00 AM New York Time'
    
    # Settlement Date
    date   = t.insaddr.exp_day
    dts1   = date.add_banking_day(t.insaddr.curr, t.insaddr.pay_day_offset)
    dts2   = date.add_banking_day(t.insaddr.und_insaddr.curr, t.insaddr.pay_day_offset)
    
    SettlementDate = ' '
    if dts1 > dts2:
        SettlementDate = date.add_banking_day(t.insaddr.curr, t.insaddr.pay_day_offset).to_string('%d.%m.%Y')
    else:
        SettlementDate = date.add_banking_day(t.insaddr.und_insaddr.curr, t.insaddr.pay_day_offset).to_string('%d.%m.%Y')
    
    PremiumCurr    =  str(t.insaddr.und_insaddr.curr.insid)
    Premium        =  str(formnum(abs(t.premium)))
    PremiumAmount  =  PremiumCurr +' '+ Premium
    
    PremPayDay        = t.value_day.to_string('%d.%m.%Y')
        
    #TRANSACTION TERMS
    canvas.drawString(8.0 * cm, 26.5*cm, TradeDate)
    canvas.drawString(8.0 * cm, 25.5*cm, Buyer)
    canvas.drawString(8.0 * cm, 24.5*cm, Seller)
    canvas.drawString(8.0 * cm, 23.5*cm, CurrencyOptionStyle)
    canvas.drawString(8.0 * cm, 22.5*cm, CurrencyOptionType)
    canvas.drawString(8.0 * cm, 21.5*cm, CallCurrencyAmount)
    canvas.drawString(8.0 * cm, 20.5*cm, PutCurrencyAmount)
    canvas.drawString(8.0 * cm, 19.5*cm, StrikePrice)
    canvas.drawString(8.0 * cm, 18.5*cm, ExpirationDate+' '+'(subject to adjustment in accordance with the')
    canvas.drawString(8.0 * cm, 18.1*cm, 'Modified Following Business Day Convention)')
    canvas.drawString(8.0 * cm, 16.5*cm, SettlementDate+' '+'(subject to adjustment in accordance with the')
    canvas.drawString(8.0 * cm, 16.1*cm, 'Modified Following Business Day Convention)')
    canvas.drawString(8.0 * cm, 15.5*cm, PremiumAmount)
    
    canvas.drawString(8.0 * cm, 17.5*cm, '10:00 AM NEW YORK TIME')
    canvas.drawString(8.0 * cm, 14.5*cm, PremPayDay)
    canvas.drawString(8.0 * cm, 13.5*cm, 'ABSA')
    canvas.showPage() 
    #-----------------------------------------------------------------------------------------------------------------#
    #                           END OF SECOND PAGE OF SHORT FORM
    #-----------------------------------------------------------------------------------------------------------------#
    

    #-----------------------------------------------------------------------------------------------------------------#
    #                           BEGINNING OF THIRD PAGE
    #-----------------------------------------------------------------------------------------------------------------#
def LongShortPara2(canvas):

    #Page Number
    pageNumber = canvas.getPageNumber()
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(10*cm, cm, str(pageNumber))

    frame = Frame(  0.5*inch,        # x
                    1*inch,          # y at bottom
                    7*inch,          # width
                    10*inch,         # height
                    showBoundary =0  #Helps to see the frame where text will be written
                    )
    canvas.setFont("Helvetica", 8.0)                
    canvas.drawString(1.5 * cm, 27.43*cm, '6.')                    
    Text1 =('<b>Additional Representations:</b>')
    Text3 =('Additional Representations, as contemplated in the 2002 ISDA Form, will apply.  For the purpose of Section\
            3 of the 2002 ISDA Form, each of the following will constitute an Additional Representation:')
    canvas.drawString(2.0*cm, 26.02*cm, '6.1')        
    Text4 =('<b>Relationship between Parties.</b>  Each of us represents and will be deemed to represent to the other\
            on the date on which this Transaction is entered into that (absent a written agreement between us \
            that expressly imposes affirmative obligations to the contrary for this Transaction):') 
    canvas.drawString(2.5*cm, 24.7*cm, '(i)')   
    Text5 =('<b>Non-Reliance.</b>  Each of us is acting for its own account, and has made its own independent decisions to\
            enter into this Transaction and as to whether this Transaction is suitable, appropriate or proper for\
            each of us and as to whether it has the capacity to enter into this Transaction based upon our own judgment\
            and upon advice from such advisors as each of us has deemed necessary to obtain. No one of us is relying on \
            any communication (written or oral) of the other as tax, regulatory, investment or financial advice or as \
            a proposal or recommendation to enter into this Transaction; it being understood that any information and\
            explanations related to the terms and conditions of this Transaction shall not be considered or construed \
            as tax, regulatory, investment or financial advice or a proposal or recommendation to enter into this \
            Transaction. No one of us has received from the other any assurance or guarantee as to the expected \
            results or financial or investment returns of this Transaction. ')  
    canvas.drawString(2.5*cm, 20.8*cm, '(ii)')           
    Text6 =('<b>Assessment and Understanding.</b>  Each of us is capable of assessing the merits of and understanding\
            (on our own behalf or through independent professional advice that we have obtained prior to entering\
            into this Transaction), and understands and accepts, the terms, conditions and risks of and associated \
            with this Transaction.  Each of us is also capable of assuming, and assumes the risks of and associated \
            with this Transaction.')
    canvas.drawString(2.5*cm, 19.08*cm, '(iii)')           
    Text7 =('<b>Status of Parties.</b>  Each of us represents that the other party is not acting as a fiduciary for or as\
                an advisor of whatsoever nature or kind to it in respect of this Transaction.')
    canvas.drawString(2.5*cm, 18.15*cm, '(iv)')               
    Text8 =('<b>Contracting as Principal.</b>  Each of us will be liable as principal for our own obligations under this\
            Transaction read with the 2002 ISDA Form and Schedule incorporated by reference.')
    canvas.drawString(2.0*cm, 17.2*cm, '6.2')        
    Text9 =('<b>Not a Sanctioned Entity and/or Sanctioned Jurisdiction.</b>  For purposes of Section 5(b)(i) of the 2002\
            ISDA Form and any related sections of the 2002 ISDA Form, the Schedule and this Confirmation, each of \
            us represents to the other that at the time of entering into this Transaction it is not a sanctioned entity,\
            and in respect of and for purposes of performing in terms of this Transaction it does not operate from any \
            sanctioned jurisdiction, in each case as contemplated in the "applicable law" referred to and contemplated\
            in Section 5(b)(i) of the 2002 ISDA Form.')
    Text10  =('For purposes of these representations,')
    Text11  =('<b><i>"sanctioned entity"</i></b> means an entity that is subject to some form of financial or economic limitations,\
            or in respect of which there is some form of financial or economic limitation on other parties dealing \
            with it, in terms of applicable law.') 
    Text12  =('<b><i>"sanctioned jurisdiction</i></b>" means a country that is subject to certain financial or economic\
            limitations, or in respect of which there is some form of financial or economic limitation on other\
            countries dealing with a sanctioned country, in terms of applicable law.')
    canvas.drawString(1.5*cm, 12.2*cm, '7.')                
    Text13  =('<b>Illegality.</b>  For purposes of Section 5(b)(i) of the 2002 ISDA Form and any related sections of the 2002\
            ISDA Form, the Schedule and this Confirmation, "applicable law" shall include, without limitation, all \
            laws, regulations, rules, directives and policies regarding the combating of criminal activities, money \
            laundering and terrorist financing issued by any statutory, regulatory, supervisory and/or other\
            governmental agency of any country in which payment, delivery or compliance is required by either\
            party or any Credit Support Provider, as the case may be.')        
            
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)
    bodyStyle2 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)
    bodyStyle3 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 40)
    bodyStyle4 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 55)
    bodyStyle5 = ParagraphStyle('Text', spaceBefore=4, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 40)
    bodyStyle6 = ParagraphStyle('Text', spaceBefore=2, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =0,\
                 alignment = 4, leftIndent = 15)         
  
    para1  = Paragraph(Text1, bodyStyle1)
    para3  = Paragraph(Text3, bodyStyle2)
    para4  = Paragraph(Text4, bodyStyle3)
    para5  = Paragraph(Text5, bodyStyle4)
    para6  = Paragraph(Text6, bodyStyle4)
    para7  = Paragraph(Text7, bodyStyle4)
    para8  = Paragraph(Text8, bodyStyle4)
    para9  = Paragraph(Text9, bodyStyle3)
    para10 = Paragraph(Text10, bodyStyle5)
    para11 = Paragraph(Text11, bodyStyle3)
    para12 = Paragraph(Text12, bodyStyle3)
    para13 = Paragraph(Text13, bodyStyle6)
    
    mydata = [para1, para3, para4, para5, para6, para7, para8, para9, para10, para11, para12, para13]
    frame.addFromList(mydata, canvas) 
    canvas.showPage()

    #--------------------------------------------------------------------------------------------------------------------#
    #                                           END OF THIRD PAGE
    #--------------------------------------------------------------------------------------------------------------------#

    #--------------------------------------------------------------------------------------------------------------------#
    #                                           ACCOUNT DETAILS ON FOURTH PAGE
    #--------------------------------------------------------------------------------------------------------------------#    
def AccountDetails(canvas, t):

    canvas.setFont("Helvetica", 8.0)    
    canvas.drawString(1.5 * cm, 27.43*cm, '8.')
    canvas.setFont("Helvetica-Bold", 8.0)
    canvas.drawString(2.0 * cm, 27.43*cm, 'Account Details')
    canvas.drawString(2.0 * cm, 26.5*cm, 'Payment to ABSA:')
    
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(2.5 * cm, 26.0*cm, 'Name of Account:')
    canvas.drawString(2.5 * cm, 25.5*cm, 'Branch:')
    canvas.drawString(2.5 * cm, 25.0*cm, 'Account Number:')
    canvas.drawString(2.5 * cm, 24.5*cm, 'Branch Code:')
    
    #ABSA Account Details
    canvas.drawString(6.5 * cm, 26.0*cm, 'Absadirect - ABSAZAJJ')
    canvas.drawString(6.5 * cm, 25.5*cm, 'ABSA Bank Eloff Street')
    canvas.drawString(6.5 * cm, 25.0*cm, '660 158 642')
    canvas.drawString(6.5 * cm, 24.5*cm, '632505')
    
    canvas.setFont("Helvetica-Bold", 8.0)
    canvas.drawString(2.0 * cm, 23.5*cm, 'Payment to Counterparty:')
    
    #Counterparty Account Number
    act   = t.counterparty_ptynbr.accounts()
    CPAccountNumber = ' '
    for acc in act:
        CPAccountNumber = str(acc.account)
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(2.5 * cm, 23.0*cm, 'Account Number:')
    canvas.drawString(6.5 * cm, 23.0*cm, CPAccountNumber)
    
        
    canvas.drawString(1.5 * cm, 21.0*cm, '9.')
    canvas.setFont("Helvetica-Bold", 8.0)
    canvas.drawString(2.0 * cm, 21.0*cm, 'Offices')
    canvas.drawString(2.0 * cm, 20.5*cm, 'ABSA:')
    
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(2.0 * cm, 20.0*cm, 'Third Floor(3S) Absa Towers North')
    canvas.drawString(2.0 * cm, 19.5*cm, '180 Commissioner Street')
    canvas.drawString(2.0 * cm, 19.0*cm, 'Johannesburg 2001')
    canvas.drawString(2.0 * cm, 18.5*cm, 'South Africa')
    
    canvas.setFont("Helvetica-Bold", 8.0)
    canvas.drawString(2.0 * cm, 17.5*cm, 'Counterparty:')
    canvas.drawString(2.0 * cm, 17.0*cm, t.counterparty_ptynbr.fullname)
    
    #Page Number
    pageNumber = canvas.getPageNumber()
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(10*cm, cm, str(pageNumber))

    
def LongShortPara3(canvas, t):
    
    frame = Frame(  0.5*inch,        # x
                    1*inch,          # y at bottom
                    7*inch,          # width
                    10*inch,         # height
                    showBoundary =0  #Helps to see the frame where text will be written
                    )
                    
    styleSheet = getSampleStyleSheet()                
    h1 = styleSheet['Heading3']
    Text2 = (' ')
        
    Text1 =('Upon receipt hereof, you, the Counterparty hereby agrees to review this Confirmation (Ref No. <b>'+ str(t.trdnbr)+'</b>)\
            and either ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =350,\
                 alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
         
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)

def LongShortPara4(canvas):

    frame = Frame(  0.5*inch,        # x
                    1*inch,          # y at bottom
                    7*inch,          # width
                    10*inch,         # height
                    showBoundary =0  #Helps to see the frame where text will be written
                    )
                    
    styleSheet = getSampleStyleSheet()                
    
    Text2 = (' ')
    
    Text1 =('i)	notify us, ABSA of any errors or discrepancies; or ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =365, alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
       
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)
 
def LongShortPara5(canvas):

    frame = Frame(  0.5*inch,        # x
                    1*inch,          # y at bottom
                    7*inch,          # width
                    10*inch,         # height
                    showBoundary =0  #Helps to see the frame where text will be written
                    )
                    
    styleSheet = getSampleStyleSheet()                
    
    Text2 = (' ')
    
    Text1 =('ii)confirm that the foregoing correctly sets forth the terms of the agreement between us with\
            respect to this particular Transaction to which this Confirmation relates by signing this Confirmation\
            and returning to facsimile +27 11 350-7941, attention Derivative Confirmations Division; or  ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =380, alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
       
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)   
    
def LongShortPara6(canvas):

    frame = Frame(  0.5*inch,        # x
                    1*inch,          # y at bottom
                    7*inch,          # width
                    10*inch,         # height
                    showBoundary =0  #Helps to see the frame where text will be written
                    )
                    
    styleSheet = getSampleStyleSheet()                
    
    Text2 = (' ')
    
    Text1 =('iii)achieve an exchange of Confirmations as intended by Section 9(e)(ii) of the 2002 ISDA Form by\
            sending an authorised Confirmation in ISDA format to facsimile number +27 11 350-7941, attention Derivative\
            Confirmations Division.  ')
    Text2 = ('')
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=100, fontName='Helvetica', fontSize=8, leading=12, spaceAfter =420, alignment = 4)
    
    para2 = Paragraph(Text2, bodyStyle1)
    para1 = Paragraph(Text1, bodyStyle1)
       
    mydata = [para2, para1]
    
    frame.addFromList(mydata, canvas)   
    
    canvas.showPage()
    
    #--------------------------------------------------------------------------------------------------------------------#
    #                                   END OF FOURTH PAGE
    #--------------------------------------------------------------------------------------------------------------------#
    
    #---------------------------------------------------------------------------------------------------------------------#
    #                                   SIGNAURES ON FIFTH PAGE 
    #---------------------------------------------------------------------------------------------------------------------#
def Signatures(canvas, t):

    canvas.setFont("Helvetica", 8.0)    
    canvas.drawString(1.5 * cm, 27.43*cm, 'Yours faithfully,')
    canvas.setFont("Helvetica-Bold", 8.0)
    canvas.drawString(1.5 * cm, 26.5*cm, 'Absa Bank Limited')
        
    canvas.setFont("Helvetica", 8.0)
    canvas.drawInlineImage('Y:/Jhb/Arena/Data/Confirmations/Signatures/LRoux.jpg', 1.5*cm, 24.5 *cm, 2.5*cm, 1.2*cm)
    #canvas.drawString(1.5 * cm, 25.0*cm, 'Signed:' )
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
    canvas.setFont("Helvetica-Bold", 8.0)
    canvas.drawString(1.5 * cm, 17.0*cm, t.counterparty_ptynbr.fullname)
    
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(1.5 * cm, 15.5*cm, 'Name: '+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 14.5*cm, 'signed:'+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 13.5*cm, 'Title:    '+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 12.5*cm, 'Date:   '+'           '+ '_'*25)
    
    canvas.drawString(1.5 * cm, 11.0*cm, 'Name: '+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 10.0*cm, 'signed:'+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 9.0*cm, 'Title:    '+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 8.0*cm, 'Date:   '+'           '+ '_'*25)
    
    #Page Number
    pageNumber = canvas.getPageNumber()
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(10*cm, cm, str(pageNumber))

    canvas.showPage()  
    
    #-------------------------------------------------------------------------------------------------------#
    #                                   END OF FIFTH PAGE
    #-------------------------------------------------------------------------------------------------------#
    
    #-------------------------------------------------------------------------------------------------------#
    #                                   DISCLAIMER ON LAST PAGE FOR ACBB CLIENTS 
    #-------------------------------------------------------------------------------------------------------#
def Disclaimer(canvas):

    #Page Number
    pageNumber = canvas.getPageNumber()
    canvas.setFont("Helvetica", 8.0)
    canvas.drawString(10*cm, cm, str(pageNumber))

    frame = Frame(  0.5*inch,        # x
                    1*inch,          # y at bottom
                    7*inch,          # width
                    10*inch,         # height
                    showBoundary =0  #Helps to see the frame where text will be written
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
    
    #---------------------------------------------------------------------------------------------#
    #                           END OF DISCLAIMER ON LAST PAGE
    #---------------------------------------------------------------------------------------------#
