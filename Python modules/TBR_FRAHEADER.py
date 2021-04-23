import ael

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units     import cm
from STATIC_TEMPLATE         import BuildLogos, BuildFooter

#--------------------------------------------------#
# FOOTER AND  ABCAP AND BARCAP LOGOS ON FIRST PAGE
#--------------------------------------------------#

def FirstPageLF(c):

    BuildLogos(c)
    BuildFooter(c)
    
def FirstPageHeader(canvas, t):
    
    #Confirmation Title
    canvas.setFont('Helvetica', 10)
    canvas.drawString(1.5 * cm, 24.5*cm, 'Date:')
    canvas.drawString(1.5 * cm, 23.0*cm, 'TO:')
    canvas.drawString(2.5 * cm, 19.5*cm, 'Fax Number:')
    canvas.drawString(2.5 * cm, 19.0*cm, 'From:')
    canvas.drawString(2.5 * cm, 18.5*cm, 'Subject:')
    canvas.drawString(2.5 * cm, 18.0*cm, 'Ref no:')
    
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(5.0 * cm, 19.0*cm, 'Absa Bank Limited, Johannesburg')
    canvas.drawString(5.0 * cm, 18.5*cm, 'Forward Rate Agreement Transaction Confirmation')
    
    #Draws line under Header Details
    canvas.line(1.5*cm, 17.5*cm, 18.8*cm, 17.5*cm)
    
#-----------------------------------------------------------------------------#
#   Counterparty Header Details on first page
#-----------------------------------------------------------------------------# 
    
    DATE        = str(ael.date_today().to_string('%d %B %Y'))
    Address1    = t.counterparty_ptynbr.address
    Address2    = t.counterparty_ptynbr.address2
    City        = t.counterparty_ptynbr.city
    Zipcode     = t.counterparty_ptynbr.zipcode
    TO          = t.counterparty_ptynbr.fullname
    FAX         = t.counterparty_ptynbr.fax
    FAXNUMBER   = FAX[0:3].replace('+27', '0')+FAX[3:5] + ' '+FAX[5:8]+ '-'+FAX[8:]
    REFERENCENO = str(t.trdnbr) 
    
    
    canvas.drawString(5.0 * cm, 24.5*cm, DATE)
    canvas.drawString(5.0 * cm, 23.0*cm, TO)
    canvas.drawString(5.0 * cm, 22.5*cm, Address1)
    canvas.drawString(5.0 * cm, 22.0*cm, Address2)
    canvas.drawString(5.0 * cm, 21.5*cm, City)
    canvas.drawString(5.0 * cm, 21.0*cm, Zipcode)
    canvas.drawString(5.0 * cm, 19.5*cm, FAXNUMBER)
    canvas.drawString(5.0 * cm, 18.0*cm, REFERENCENO)
