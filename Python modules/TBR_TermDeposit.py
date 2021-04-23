import ael, acm, os

import ael, time
import reportlab.lib.pagesizes

from PIL                     import Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import *
from reportlab.lib.units     import cm, inch
from STATIC_TEMPLATE         import BuildLogos, Term_Deposit_Footer
from reportlab.lib.colors    import black 
from zak_funcs               import formnum
from reportlab.lib           import colors
from reportlab.lib.colors    import black


def Term_Deposits_Maturity_Notice(temp,t,Term,*rest):
    
    #Counterparty Contact Details:
    Customer        = t.counterparty_ptynbr.fullname
    AddressLine1    = t.counterparty_ptynbr.address
    AddressLine2    = t.counterparty_ptynbr.address2
    PostalCode      = t.counterparty_ptynbr.zipcode
    Country         = t.counterparty_ptynbr.country
    CustomerContact = t.counterparty_ptynbr.attention
    
    #Date notice is printed
    DatePrinted = ael.date_today().to_string("%d %B %Y")
    
    #Account Number:
    Account_Number = ' '    
    p   = t.counterparty_ptynbr
    act = p.accounts()
    for a in act:
        Account_Number = a.account 
        
    #Term Deposit Maturity Notice Details    
    Reference       = str(t.trdnbr)
    Nominal         = str(formnum(abs(t.nominal_amount(t.value_day))).replace(',', ' '))
    Start_Day       = t.value_day.to_string("%d %B %Y")
    End_Day         = t.insaddr.exp_day.to_string("%d %B %Y")
    Rate            = str(t.price)
    InterestAmount  = (formnum(abs(t.interest_settled(t.value_day, t.insaddr.exp_day)))).replace(',', ' ')
    AccruedAmount   = formnum(abs(t.interest_settled(t.value_day, t.insaddr.exp_day))+ abs(t.nominal_amount(t.value_day))).replace(',', ' ')
    
    
    #ABSA and BarCap Logos and Footer    
    BuildLogos(Term)
    Term_Deposit_Footer(Term)
    
    Term.setFont("Helvetica", 10.0)
    Term.drawString(1.0 *cm, 25.0*cm,  'To:') 
    Term.drawString(3.0 *cm, 25.0*cm,  Customer) 
    Term.drawString(3.0 *cm, 24.5*cm,  AddressLine1)
    Term.drawString(3.0 *cm, 24.0*cm,  AddressLine2)
    Term.drawString(3.0 *cm, 23.5*cm,  PostalCode)
    Term.drawString(3.0 *cm, 23.0*cm,  Country)
    Term.drawString(3.0 *cm, 22.5*cm,  CustomerContact )
    Term.drawString(1.0 *cm, 22.5*cm,  'Attention:')
    
    Term.setFont("Helvetica", 10.0)
    Term.drawString(12.0 *cm, 23.0*cm, 'From:') 
    Term.drawString(14.0 *cm, 23.0*cm, 'CLIENT SERVICES')  
    Term.drawString(14.0 *cm, 22.5*cm, 'PRIVATE BAG X10056') 
    Term.drawString(14.0 *cm, 22.0*cm, 'SANDTON')  
    Term.drawString(14.0 *cm, 21.5*cm, 'SOUTH AFRICA')   
    Term.drawString(14.0 *cm, 21.0*cm, '2146')    

    Term.setFont("Helvetica", 10.0)
    Term.drawString(12.0 *cm, 19.5*cm, 'Enquiries:')
    
    Term.setFont("Helvetica", 10.0)
    Term.drawString(14.0 *cm, 19.5*cm, 'Tel: (011) 895 6754/34')
    Term.drawString(14.0 *cm, 19.0*cm, 'Fax: (011) 895 7858')
    Term.drawString(14.0 *cm, 18.5*cm, 'Contact: ')
    
    Term.drawString(15.5 *cm, 18.5*cm, 'SYLVIA ACKERMAN')
    Term.drawString(15.5 *cm, 17.5*cm, 'SHARON MAYNARD')
    
    Term.setFont("Helvetica", 6.0)
    Term.drawString(15.5 *cm, 18.2*cm, 'sylvia.ackerman@absacapital.com')
    Term.drawString(15.5 *cm, 17.2*cm, 'sharon.maynard@absacapital.com')
    
    Term.setFont("Helvetica", 10.0)
    Term.drawString(12.0 *cm, 16.5*cm,  'Date:')
    Term.drawString(14.0 *cm, 16.5*cm,  DatePrinted)
    
    Term.setFont("Helvetica-Bold", 10.0)
    Term.drawString(1.0 *cm, 15.0*cm,  'THE FOLLOWING FIXED TERM DEPOSIT MATURES:')
    Term.line(1.0*cm, 14.8*cm, 9.7*cm, 14.8*cm)
    
    Term.setFont("Helvetica", 10.0)
    Term.drawString(1.0 *cm, 14.0*cm,  'ACCOUNT NUMBER')
    Term.drawString(1.0 *cm, 13.0*cm,  'REFERENCE')
    Term.drawString(1.0 *cm, 12.0*cm,  'NOMINAL AMOUNT')
    Term.drawString(1.0 *cm, 11.0*cm,  'START DATE')
    Term.drawString(1.0 *cm, 10.0*cm,  'MATURITY DATE')
    Term.drawString(1.0 *cm,  9.0*cm,  'INTEREST RATE')
    Term.drawString(1.0 *cm,  8.0*cm,  'INTEREST AMOUNT')
    Term.drawString(1.0 *cm,  7.0*cm,  'ACCRUED AMOUNT')
    
    Term.drawString(5.0 *cm,  14.0*cm, ':')
    Term.drawString(5.0 *cm,  13.0*cm, ':')
    Term.drawString(5.0 *cm,  12.0*cm, ':')
    Term.drawString(5.0 *cm,  11.0*cm, ':')
    Term.drawString(5.0 *cm,  10.0*cm, ':')
    Term.drawString(5.0 *cm,   9.0*cm, ':')
    Term.drawString(5.0 *cm,   8.0*cm, ':')
    Term.drawString(5.0 *cm,   7.0*cm, ':')
    
    Term.drawString(6.0 *cm,  14.0*cm, str(Account_Number))
    Term.drawString(6.0 *cm,  13.0*cm, Reference)
    Term.drawString(6.0 *cm,  12.0*cm, 'R '+ Nominal)
    Term.drawString(6.0 *cm,  11.0*cm, Start_Day)
    Term.drawString(6.0 *cm,  10.0*cm, End_Day)
    Term.drawString(6.0 *cm,   9.0*cm, Rate + ' %')
    Term.drawString(6.0 *cm,   8.0*cm, 'R '+ InterestAmount)
    Term.drawString(6.0 *cm,   7.0*cm, 'R '+ AccruedAmount)
    
    Term.drawString(1.0 *cm,  5.0*cm,  'THIS IS A COMPUTER-GENERATED DOCUMENT AND DOES NOT REQUIRE ANY SIGNATURES.')
    
def ASQL(*rest):
    acm.RunModuleWithParameters( 'TermDeposit', 'Standard' )
    return 'SUCCESS'    
    
ael_variables = [('trdnbr', 'Trade Number:', 'string', None, '0')]
               

def ael_main(dict):

    print 'Loading...'
    
    trdnbr = ael.Trade[int(dict['trdnbr'])]
    Party  = trdnbr.counterparty_ptynbr.fullname
    
    tmp = "Y:/Jhb/Operations Secondary Markets/Sylvia Sharon/Fixed Term Deposit Maturity Notice " + Party +" ( "+str(trdnbr.trdnbr)+" ) " + ".pdf"
    pdf = Canvas(tmp, pagesize = A4 )
    
    if dict['trdnbr'] != '0':
        for trd in dict['trdnbr'].replace(' ', '').split(','):
            try:
                trade = ael.Trade[int(trd)]
                try:    
                    Term_Deposits_Maturity_Notice(1, trade, pdf)
                except:
                    print 'Fatal Error!'
            except:
                print 'Trade Number ', trd, ' is not a valid trade number'
                
        pdf.save() 
            
    print 'Done...'        
    os.startfile(tmp)
