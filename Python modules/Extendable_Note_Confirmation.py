import ael, acm, os

from reportlab.lib.pagesizes import *
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units     import inch, cm
from STATIC_TEMPLATE         import BuildLogos, BuildFooter
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus      import Paragraph, Frame, Spacer
from zak_funcs               import formnum

def BuildLogoFooter(c):
    
    BuildLogos(c)
    BuildFooter(c)
    
def FirstPage(canvas, t):
        
    Nominal_Amount = t.nominal_amount()
    
    if Nominal_Amount < 0:
        Nominal_Amount = formnum(-t.nominal_amount())
    else:
        Nominal_Amount = formnum(t.nominal_amount())
        
    Exp_Day = t.insaddr.exp_day.to_string('%d %B %Y')
        
    frame   = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
                    
    styleSheet = getSampleStyleSheet() 
               
    Flag        = (' ')
    Header      =('<b>Absa Bank Limited</b>')
    HeaderText1 = ('<i>(Incorporated with limited liability in the Republic of South Africa under Registration Number </i>')
    HeaderText2 = ('<i>1986/004794/06)</i>')
    HeaderText3 = ('<b>Issue of ' + 'R'+ Nominal_Amount + ' Extendable Notes due '+ Exp_Day + '</b>')
    HeaderText4 = ('<b>Under its ZAR15,000,000,000 Domestic Medium Term Note Programme<b>')
    Paragraph1  = ('This document constitutes the Applicable Pricing Supplement relating to the issue of the Extendable Notes (the <b>"Notes"</b>) described herein.\
                    Unless the context dictates otherwise, the terms used herein shall be deemed to be defined as such for the purposes of the terms and conditions\
                    set forth in the Programme Memorandum dated 25 March 2004 (the <b>"Programme Memorandum"</b>).  This Applicable Pricing Supplement must be read in conjunction\
                    with such Programme Memorandum.  To the extent that there is any conflict or inconsistency between the contents of this Applicable Pricing Supplement and the\
                    Programme Memorandum, the provisions of this Applicable Pricing Supplement shall prevail.')
    Paragraph2  =  ('<b>1. INTERPRETATION</b>')
    Paragraph3  =  ('1.1 In this Applicable Pricing Supplement, the following expressions shall have the following meanings:')
    Paragraph4  =  ('<b>"Final Maturity Date"</b> means the earlier to occur of:')                
    Paragraph5  =  ('(i)	'+Exp_Day + ' ; and')
    Paragraph6  =  ('(ii) any Maturity Reset Date upon which the Issuer chooses not to exercise its option to extend the Final Maturity Date as provided\
                     for in the "Issuer\'s Maturity Extension Option" provisions of this Applicable Pricing Supplement;') 
    Paragraph7  =  ('<b>"Extendable Notes"</b> means the Notes, the Final Maturity Date of which is extendable at the option of the')
    Paragraph8  =  ('Issuer upon each Maturity Reset Date occurring prior to '+ Exp_Day +' ;')
    Paragraph9  =  ('<b>"Maturity Reset Date"</b> means each date Specified as such in this Applicable Pricing Supplement, subject to:')
    Paragraph10 =  ('(i) the Issuer exercising its option to extend the Final Maturity Date until the next following Maturity Reset Date as provided for in the "Issuer\'s Maturity Extension Option" provisions of this Applicable Pricing Supplement; and')
    Paragraph11 =  ('(ii) adjustment in accordance with the Specified Business Day Convention.')
    Paragraph12 =  ('<b>"Specified"</b>  means specified in this Applicable Pricing Supplement;')
    Paragraph13  = ('1.2 To the extent that defined terms are used in this Applicable Pricing Supplement and are not defined in this Applicable Pricing\
                    Supplement, they will have the meanings set out in the Programme Memorandum.')
    Paragraph14  = ('1.3 In the event of any inconsistency between the terms defined in this Applicable Pricing Supplement and those defined in the\
                    Programme Memorandum, the Applicable Pricing Supplement will prevail.')
                    
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=70, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =60, alignment = 4, leftIndent = 185)
    bodyStyle2 = ParagraphStyle('Text', spaceBefore=0, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment  = 4, leftIndent = 195)
    bodyStyle3 = ParagraphStyle('Text', spaceBefore=0, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment  = 4, leftIndent = 40)
    bodyStyle4 = ParagraphStyle('Text', spaceBefore=0, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment  = 4, leftIndent = 185)
    bodyStyle5 = ParagraphStyle('Text', spaceBefore=10, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment  = 4, leftIndent = 65)
    bodyStyle6 = ParagraphStyle('Text', spaceBefore=10, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment  = 4, leftIndent = 65)
    bodyStyle7 = ParagraphStyle('Text', spaceBefore=10, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment  = 4)
    bodyStyle8 = ParagraphStyle('Text', spaceBefore=10, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment  = 4, leftIndent = 105)
    bodyStyle9 = ParagraphStyle('Text', spaceBefore=0, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment  = 4, leftIndent = 95)
    bodyStyle10 = ParagraphStyle('Text', spaceBefore=0, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment  = 4, leftIndent = 95)
    
    FlagText    = Paragraph(Flag,  bodyStyle1)
    PageHeader  = Paragraph(Header, bodyStyle2)
    HeaderText1 = Paragraph(HeaderText1, bodyStyle3)
    HeaderText2 = Paragraph(HeaderText2, bodyStyle4)
    HeaderText3 = Paragraph(HeaderText3, bodyStyle5)
    HeaderText4 = Paragraph(HeaderText4, bodyStyle6)
    Paragraph1  = Paragraph(Paragraph1, bodyStyle7)
    Paragraph2  = Paragraph(Paragraph2, bodyStyle7)
    Paragraph3  = Paragraph(Paragraph3, bodyStyle7)
    Paragraph4  = Paragraph(Paragraph4, bodyStyle7)
    Paragraph5  = Paragraph(Paragraph5, bodyStyle8)
    Paragraph6  = Paragraph(Paragraph6, bodyStyle8)
    Paragraph7  = Paragraph(Paragraph7, bodyStyle7)
    Paragraph8  = Paragraph(Paragraph8, bodyStyle9)
    Paragraph9  = Paragraph(Paragraph9, bodyStyle7)
    Paragraph10 = Paragraph(Paragraph10, bodyStyle10)
    Paragraph11 = Paragraph(Paragraph11, bodyStyle10)
    Paragraph12 = Paragraph(Paragraph12, bodyStyle7)
    Paragraph13 = Paragraph(Paragraph13, bodyStyle7)
    Paragraph14 = Paragraph(Paragraph14, bodyStyle7)
    
    mydata = [FlagText, PageHeader, HeaderText1, HeaderText2, HeaderText3, HeaderText4, Paragraph1, Paragraph2, Paragraph3,\
              Paragraph4, Paragraph5, Paragraph6, Paragraph7, Paragraph8, Paragraph9, Paragraph10, Paragraph11, Paragraph12, Paragraph13, Paragraph14]
           
    frame.addFromList(mydata, canvas)
    canvas.showPage()
    
def SecondPage(canvas):
    
    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
    
    styleSheet  =  getSampleStyleSheet()  
    
    Paragraph1  = ('<b> 2. RISK FACTORS IN RESPECT OF THE NOTES</b>')
    Paragraph2  = ('<i>The contents of this section shall not form part of the Terms and Conditions and may not be used in interpreting the Terms and Conditions.</i>')
    Paragraph3  = ('<i><b>Before making an investment decision, prospective purchasers of the Notes should consider carefully, in the light of their own\
                    financial circumstances and investment objectives, all the information set forth in the Programme Memorandum and this Applicable\
                    Pricing Supplement and, in particular, the considerations set forth below, relating to the "Issuer\'s Maturity Extension Option"\
                    in clause 22 of section 3.2 below.  This Applicable Pricing Supplement may contain specific representations to be given by the \
                    purchasers of the Notes as well as further disclaimers and risk warnings in addition to the general provisions set out below.</b></i>')
    Paragraph4  = ('<b>2.1 REDEMPTION PRIOR TO SCHEDULED REDEMPTION DATE</b>')
    Paragraph5  = ('The Issuer may extend the maturity date of the Notes at its sole discretion upon notice to the Noteholder in accordance with the provisions of this Applicable Pricing Supplement.')
    Paragraph6  = ('<b>2.2	NOTES NOT TRANSFERABLE</b>')
    Paragraph7  = ('No secondary market exists for the Notes and the Notes are issued on the basis that they are not transferable under any circumstances\
                    by the Noteholder, whether in terms of the "Applicable Procedures" as defined in the Programme Memorandum or otherwise.  Consequently,\
                    a prospective purchaser of the Notes must be prepared to hold its Notes until the redemption or maturity of the Notes.')
    Paragraph8  = ('<b>2.3 INDEPENDENT REVIEW AND ADVICE</b>')
    Paragraph9  = ('Each purchaser of and investor in the Notes is fully responsible for making its own investment decisions as to whether the Notes (i)\
                    are fully consistent with its (or if it is acquiring the Notes in a fiduciary capacity, the beneficiary\'s) financial needs, objectives\
                    and conditions, (ii) comply and are fully consistent with all investment policies, guidelines and restrictions applicable to it (or its beneficiary)\
                    and (iii) are a fit, proper and suitable investment for it (or its beneficiary).')
    Paragraph10 = ('Purchasers of and investors in Notes are deemed to have sufficient knowledge, experience and professional advice to make their own investment\
                    decisions, including, without limitation, their own legal, financial, tax, accounting, credit, regulatory and other business evaluation of the\
                    risks and merits of or associated with investments in the Notes.  Purchasers of and investors in Notes should ensure that they fully understand\
                    the risks of or associated with investments of this nature which are intended to be sold only to sophisticated investors having such knowledge, appreciation and understanding.')                
    Paragraph11  = ('<b> 3. SPECIFIC TERMS AND CONDITIONS APPLICABLE TO EXTENDABLE NOTES</b>')
    Paragraph12  = ('<b>3.1 REPRESENTATIONS</b>')
    Paragraph13  = ('By purchasing this Note, the Noteholder acknowledges and undertakes to the Issuer that the Noteholder:')
    Paragraph14  = ('(i) is either (a) acting for its own account, and has made its own independent decision to acquire the Note and as to whether\
                    the Note is appropriate or proper for it based upon its own judgement and upon advice from such advisers as it has deemed necessary,\
                    or (b) acting through a duly mandated asset manager and agent on behalf of the Noteholder, and that the asset manager and agent has\
                    made its own independent decision as asset manager and agent on behalf of the Noteholder to acquire this Note and as to whether this\
                    Note is appropriate or proper for the Noteholder based upon the asset manager\'s and agent\'s own judgement and upon advice from such\
                    advisers as the asset manager and agent has deemed necessary; and')
    Paragraph15  = ('(ii) is not relying on any communication (written or oral) from the Issuer or any agent or employee of the Issuer in regard to\
                    accounting, tax, legal or investment advice or as a recommendation to purchase the Note; it being understood that information and\
                    explanations relating to the terms and conditions of the Note will not be considered accounting, tax, legal or investment advice or\
                    a recommendation to purchase or invest in the Note;')               
    Paragraph16  = ('(iii) it has not received any guarantee or undertaking (written or oral) from the Issuer as to the expected investment and financial\
                    returns of the Note;')                
    Paragraph17  = ('(iv) is capable of assessing the merits of and understanding (on its own behalf or through independent professional advice), and\
                   does understand and accept the terms, conditions and all the risks of and associated with the purchasing of or investment in the Note.')
               
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=0, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment = 4)
    bodyStyle2 = ParagraphStyle('Text', spaceBefore=10, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment = 4)
    bodyStyle3 = ParagraphStyle('Text', spaceBefore=10, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment = 4, leftIndent = 3)
    
    Paragraph1  = Paragraph(Paragraph1, bodyStyle1)
    Paragraph2  = Paragraph(Paragraph2, bodyStyle2)
    Paragraph3  = Paragraph(Paragraph3, bodyStyle2)
    Paragraph4  = Paragraph(Paragraph4, bodyStyle2)
    Paragraph5  = Paragraph(Paragraph5, bodyStyle2)
    Paragraph6  = Paragraph(Paragraph6, bodyStyle2)
    Paragraph7  = Paragraph(Paragraph7, bodyStyle2)
    Paragraph8  = Paragraph(Paragraph8, bodyStyle2)
    Paragraph9  = Paragraph(Paragraph9, bodyStyle2)
    Paragraph10 = Paragraph(Paragraph10, bodyStyle2)
    Paragraph11 = Paragraph(Paragraph11, bodyStyle2)
    Paragraph12 = Paragraph(Paragraph12, bodyStyle3)
    Paragraph13 = Paragraph(Paragraph13, bodyStyle3)
    Paragraph14 = Paragraph(Paragraph14, bodyStyle3)
    Paragraph15 = Paragraph(Paragraph15, bodyStyle3)
    Paragraph16 = Paragraph(Paragraph16, bodyStyle3)
    Paragraph17 = Paragraph(Paragraph17, bodyStyle3)
    
    mydata = [Paragraph1, Paragraph2, Paragraph3, Paragraph4, Paragraph5, Paragraph6,\
             Paragraph7, Paragraph8, Paragraph9, Paragraph10, Paragraph11, Paragraph12, Paragraph13, Paragraph14, Paragraph15, Paragraph16, Paragraph17]
    
    frame.addFromList(mydata, canvas)
    canvas.showPage()

def ThirdPage(canvas):

    frame = Frame(0.5*inch, 1*inch, 7*inch, 10*inch, showBoundary =0)
    
    styleSheet  =  getSampleStyleSheet()  
    Paragraph1  = ('(iv) is capable of assessing the merits of and understanding (on its own behalf or through independent professional advice), and\
                   does understand and accept the terms, conditions and all the risks of and associated with the purchasing of or investment in the Note.')                
    bodyStyle1  = ParagraphStyle('Text', spaceBefore=10, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment = 4)
       
    Paragraph1  = Paragraph(Paragraph1, bodyStyle1)
    
    mydata = [Paragraph1]
  
    frame.addFromList(mydata, canvas)
       
def ThirdPageDescription(canvas, t):
    
    ListedUnListed = ' '
    ais = t.additional_infos()
    for ai in ais:
        if ai.addinf_specnbr.field_name == 'MM_Instype':
            ListedUnListed = ai.value
    
    PrincipalAmount = t.nominal_amount()        
    if PrincipalAmount < 0:
        PrincipalAmount = formnum(-t.nominal_amount())
    else:
        PrincipalAmount = formnum(t.nominal_amount()) 
        
    IssueDate = ' '    
    for l in t.insaddr.legs():
        IssueDate = str(l.start_day)
    
    FinalMaturityDate = t.insaddr.exp_day.to_string('%d %B %Y')
    
    EndDayList = []
    for cf in t.insaddr.legs()[0].cash_flows():
        if cf.type == 'Float Rate':
            EndDayList.append(cf.end_day)
    EndDayList.sort()  
        
    Paragraph1 =('(ii)	any Maturity Reset Date upon which the Issuer chooses not to exercise its option to extend the Final Maturity Date as provided for in the "Issuer\'s Maturity Extension Option" provision in clause 22 below.')
    Paragraph2 =('Such Final Maturity Date will be subject to adjustment in accordance with the Specified Business Day Convention.')
    Paragraph3 =(str(EndDayList[0]) + ','+ str(EndDayList[1])+','+ str(EndDayList[2])+ ', subject to:')
    Paragraph4 =('(i)	the Issuer exercising its option to extend the Final Maturity Date until the next following Maturity Reset Date as provided for in the "Issuer\'s Maturity Extension Option" provision in clause 22 below; and')
    Paragraph5 =('(ii)	adjustment in accordance with the Specified Business Day ')
    
    frame = Frame(5*inch, 1*inch, 2.5*inch, 4.5*inch, showBoundary =0)
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=10, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment = 4)
        
    Paragraph1  = Paragraph(Paragraph1, bodyStyle1)
    Paragraph2  = Paragraph(Paragraph2, bodyStyle1)
    Paragraph3  = Paragraph(Paragraph3, bodyStyle1)
    Paragraph4  = Paragraph(Paragraph4, bodyStyle1)
    Paragraph5  = Paragraph(Paragraph5, bodyStyle1)
    
    mydata = [Paragraph1, Paragraph2, Paragraph3, Paragraph4, Paragraph5]
  
    frame.addFromList(mydata, canvas)

    canvas.setFont("Times-Bold", 12.0)
    canvas.drawString(1.5 * cm, 25.5*cm, '3.2 DESCRIPTION OF THE NOTES')
    canvas.setFont("Times-Roman", 12.0)
    canvas.drawString(1.5 * cm, 24.5*cm, '1. Issuer')
    canvas.drawString(1.5 * cm, 23.5*cm, '2. Whether the Notes are Senior Notes or Subordinated')
    canvas.drawString(1.5 * cm, 22.5*cm, '3. Listed/Unlisted')
    canvas.drawString(1.5 * cm, 21.5*cm, '4. Principal Amount')
    canvas.drawString(1.5 * cm, 20.5*cm, '5. Interest/Payment Basis')
    canvas.drawString(1.5 * cm, 19.5*cm, '6. Issue Date')
    canvas.drawString(1.5 * cm, 18.5*cm, '7. Specified Denomination')
    canvas.drawString(1.5 * cm, 17.5*cm, '8. Issue Price')
    canvas.drawString(1.5 * cm, 16.5*cm, '9. Interest Commencement Date')
    canvas.drawString(1.5 * cm, 14.5*cm, '10. Final Maturity Date')
    
    canvas.drawString(13.0 * cm, 24.5*cm, 'Absa Bank Limited')
    canvas.drawString(13.0 * cm, 23.5*cm, 'Senior')
    canvas.drawString(13.0 * cm, 22.5*cm, ListedUnListed)
    canvas.drawString(13.0 * cm, 21.5*cm, PrincipalAmount)
    canvas.drawString(13.0 * cm, 20.5*cm, 'Floating Rate')
    canvas.drawString(13.0 * cm, 19.5*cm, IssueDate)
    canvas.drawString(13.0 * cm, 18.5*cm, 'Notes are subject to a minimum ')
    canvas.drawString(13.0 * cm, 18.1*cm, 'denomination of R1,000,000 ')
    canvas.drawString(13.0 * cm, 17.5*cm, '100%')
    canvas.drawString(13.0 * cm, 16.5*cm, 'Issue Date')
    canvas.drawString(13.0 * cm, 14.5*cm, 'means the earlier to occur of:')
    canvas.drawString(13.0 * cm, 14.1*cm, '(i) '+ FinalMaturityDate + ' ; and')
        
    canvas.drawString(1.5  * cm, 8.4*cm, '11. Maturity Reset Date(s)')
    
    canvas.showPage() 
    
def FourthPageDescription(canvas, t):
    
    EndDayList = []
    PayDayList = []
    
    NominalAmount = -t.nominal_amount()
    
    for cf in t.insaddr.legs()[0].cash_flows():
        if cf.type == 'Float Rate':
            EndDayList.append(cf.end_day)
            PayDayList.append(cf.pay_day)
            EndDayList.sort()  
            PayDayList.sort()
        
    FinalRedemptionAmount = ' '                    
    MaxDate = max(EndDayList)
    for cf in t.insaddr.legs()[0].cash_flows():
        if cf.end_day == MaxDate:
            FinalRedemptionAmount = formnum(cf.projected_cf()*1000 + NominalAmount)
            
    legs = t.insaddr.legs()    
    
    for l in legs:
        Spread    = str(l.spread)
        Float_Ref = l.float_rate.insid
    
    StartDayList = []
    
    for cf in t.insaddr.legs()[0].cash_flows():
        if cf.type == 'Float Rate':
            StartDayList.append(cf.start_day)
    StartDayList.sort()
    
    Paragraph1 =(str(PayDayList[0])+ ';' + str(PayDayList[1])+ ';' + str(PayDayList[2])+ ';'+ ' and '+ str(PayDayList[3])+ ' ,subject to adjustment in accordance with the applicable Business Day Convention.')
    Paragraph2 =('Each period from and including one Interest Payment Date to, but excluding the next Interest Payment Date, provided that the first Interest Period shall be from and including the Interest Commencement Date to but excluding the first Interest Payment Date thereafter. ')
    Paragraph3 = ('The Issuer has the right (but not the obligation) to extend the Final Maturity Date of the Notes at its sole ') 
    
    frame = Frame(5*inch, 1*inch, 2.5*inch, 8.9*inch, showBoundary =0)
    
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=10, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment = 4)
    bodyStyle2 = ParagraphStyle('Text', spaceBefore=10, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =2, alignment = 4)
    bodyStyle3 = ParagraphStyle('Text', spaceBefore=415, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =25, alignment = 4)
    
    Paragraph1 = Paragraph(Paragraph1, bodyStyle1)
    Paragraph2 = Paragraph(Paragraph2, bodyStyle2)
    Paragraph3 = Paragraph(Paragraph3, bodyStyle3)
    
    mydata = [Paragraph1, Paragraph2, Paragraph3]
  
    frame.addFromList(mydata, canvas)
    canvas.setFont("Times-Roman", 12.0)
    canvas.drawString(1.5 * cm, 27.5*cm, '12. Final Redemption Amount')
    canvas.setFont("Times-Bold", 12.0) 
    canvas.drawString(1.5 * cm, 25.5*cm, 'FLOATING RATE NOTES') 
    canvas.setFont("Times-Roman", 12.0)
    canvas.drawString(1.5 * cm, 24.5*cm, '13. Interest Payment Date(s)') 
    canvas.drawString(1.5 * cm, 22.5*cm, '14. Interest Period(s)')
    canvas.drawString(1.5 * cm, 19.0*cm, '15. Definitions of Business Day (if different from that')
    canvas.drawString(2.2 * cm, 18.5*cm, 'set out in the Terms and Conditions)')
    canvas.drawString(1.5 * cm, 17.1*cm, '16. Applicable Business Day Convention')
    canvas.drawString(1.5 * cm, 14.1*cm, '17. Other terms relating to the method of calculating')
    canvas.drawString(2.2 * cm, 13.6*cm, 'interest (eg: day count fraction, rounding up')
    canvas.drawString(2.2 * cm, 13.1*cm, 'provision, if different from Condition 7)')
    canvas.drawString(1.5 * cm, 12.1*cm, '18. Manner in which the Rate of Interest is to be determined')
    canvas.drawString(1.5 * cm, 11.1*cm, '19. Margin')
    canvas.drawString(1.5 * cm, 9.0*cm, '20. If Screen Determination')
    canvas.drawString(2.2 * cm, 8.5*cm, '(a) Reference Rate (including relevant period by')
    canvas.drawString(2.8 * cm, 8.0*cm, 'reference to which the Rate of Interest is to be')
    canvas.drawString(2.8 * cm, 7.5*cm, 'calculated)')
    canvas.drawString(2.2 * cm, 7.0*cm, '(b) Interest Rate Determination Date(s)')
        
    canvas.setFont("Times-Bold", 12.0) 
    canvas.drawString(1.5 * cm, 5.5*cm, 'PROVISIONS REGARDING REDEMPTION / MATURITY')
    canvas.setFont("Times-Roman", 12.0)
    canvas.drawString(1.5 * cm, 4.5*cm, '21. Issuers Maturity Extension Option')
    
    canvas.drawString(13.0 * cm, 27.5*cm, 'R'+FinalRedemptionAmount)
    canvas.drawString(13.0 * cm, 19.0*cm, 'Johannesburg')
    canvas.drawString(13.0 * cm, 17.1*cm, 'Following Business Day Convention ')
    canvas.drawString(13.0 * cm, 14.1*cm, 'Actual/365')
    canvas.drawString(13.0 * cm, 12.1*cm, 'Screen Rate Determination')
    
    canvas.drawString(13.0 * cm, 11.1*cm, Spread)
    canvas.drawString(13.0 * cm, 8.5*cm, Float_Ref)
    canvas.drawString(13.0 * cm, 7.0*cm, str(StartDayList[0]) + ',' +str(StartDayList[1])+','+ str(StartDayList[2]))
       
    canvas.showPage() 
    
def FifthPage(canvas, t):

    MaturityDate  =  str(t.insaddr.exp_day.to_string('%d %B %Y'))
    
    frame = Frame(5*inch, 1*inch, 2.7*inch, 10*inch, showBoundary =0)
    
    styleSheet  =  getSampleStyleSheet()  
         
    Paragraph1  = ('discretion on each Maturity Reset Date falling prior to the ' + MaturityDate + ' for a period up to, and including,\
                    the next Interest Payment Date which shall be regarded as the new Final Maturity Date, by providing notice thereof\
                    to the Noteholder on or prior to 3:00 p.m., Johannesburg time, on the day that falls five (5) Business Days prior to\
                    any Maturity Reset Date.  On such Maturity Reset Date, after an effective notice of extension to the Noteholder, the\
                    Final Maturity Date of this Note shall be extended on the terms and conditions specified in this Applicable Pricing Supplement.') 
               
    Paragraph2  = ('If no notice extension is provided by the Issuer to the Noteholder on or prior to 3:00 p.m., Johannesburg time, on the day that\
                    falls five (5) Business Days prior to any Maturity Reset Date, such Maturity Reset Date will be the Final Maturity Date and this \
                   Note shall be redeemed accordingly.') 
                   
    Paragraph3  =('Any notice given pursuant to this clause 22 may be given orally (including by telephone) or in written form (including by e-mail)\
                   and such notice will be deemed irrevocable.  If the notice is delivered by telephone, a written communication will be executed and\
                   delivered confirming the substance of that notice within one Business Day of that notice.  Failure to provide that written confirmation\
                   will not affect the effectiveness of that telephonic notice.')               
             
    bodyStyle1 = ParagraphStyle('Text', spaceBefore=10, fontName='Times-Roman', fontSize=11, leading=12, spaceAfter =0, alignment = 4)
        
    
    Paragraph1  = Paragraph(Paragraph1, bodyStyle1)
    Paragraph2  = Paragraph(Paragraph2, bodyStyle1)
    Paragraph3  = Paragraph(Paragraph3, bodyStyle1)
    
    mydata = [Paragraph1, Paragraph2, Paragraph3]
  
    frame.addFromList(mydata, canvas)
 
    canvas.setFont("Times-Bold", 12.0) 
    canvas.drawString(1.5 * cm, 11.0*cm, 'GENERAL')
    canvas.setFont("Times-Roman", 12.0) 
        
    canvas.drawString(1.5 * cm, 10.0*cm, '22. Method of distribution')
    canvas.drawString(1.5 * cm,  9.0*cm, '23. Any other terms and conditions')
        
    canvas.drawString(13.0 * cm,  10.0*cm, 'Private Placement')
    canvas.drawString(13.0 * cm,  9.0*cm, 'The Notes are not Transferable')
    
    canvas.setFont("Times-Bold", 12.0) 
    canvas.drawString(1.5 * cm, 6.0*cm, 'ABSA BANK LIMITED') 
    canvas.drawString(1.5 * cm, 5.0*cm, 'Issuer') 
    
    canvas.setFont("Times-Roman", 12.0) 
    canvas.drawString(1.5 * cm,  3.0*cm, 'By:') 
    canvas.drawString(13.0 * cm, 3.0*cm, 'By:') 
    canvas.showPage()
 
def SixthPage(canvas):
    
    canvas.setFont("Times-Bold", 12.0) 
    canvas.drawString(1.5 * cm, 26.0*cm, 'ABSA BANK LIMITED') 
    canvas.drawString(1.5 * cm, 25.5*cm, 'Issuer') 
    
    canvas.setFont("Times-Roman", 12.0) 
    canvas.drawString(1.5 * cm,  23.5*cm, 'By:') 
    canvas.drawString(13.0 * cm, 23.5*cm, 'By:') 
    
    
    
ael_variables= [('trdnbr', 'Trade Number:', 'string', None, '0', 1)]
                
def ael_main(dict):
    
    if dict['trdnbr'] != '0':
        trade = ael.Trade[int(dict['trdnbr'])]
        ClientName = trade.counterparty_ptynbr.ptyid
                    
    tmp = 'Y:/Jhb/Operations Secondary Markets/Money Market ops/MM Confirmations/Extendable Note Confirmation/Extendable Note Confirmation'+ '-'+ ClientName+ ' ('+ str(trade.trdnbr) +') '+ str(ael.date_today().to_string('%d %b %Y')) + ' .pdf'
    pdf = Canvas(tmp, pagesize = A4)
    if dict['trdnbr'] != '0':
        for trd in dict['trdnbr'].replace(' ', '').split(','):
            try:
                trade = ael.Trade[int(trd)]
                try: 
                    BuildLogoFooter(pdf)    
                    FirstPage(pdf, trade)
                    SecondPage(pdf)
                    ThirdPage(pdf)
                    ThirdPageDescription(pdf, trade)
                    FourthPageDescription(pdf, trade)
                    FifthPage(pdf, trade)
                    
                except:
                    func=acm.GetFunction('msgBox', 3)
                    func("Warning", "Ivalid Trade Number!", 0)
                    break
                    
            except:
                func=acm.GetFunction('msgBox', 3)
                func("Warning", "Ivalid Trade Number!", 0)
                break
                    
    pdf.save()
    os.startfile(tmp)
