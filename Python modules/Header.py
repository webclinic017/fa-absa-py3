import ael

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units     import cm
from STATIC_TEMPLATE         import BuildLogos, BuildFooter

#---------------------------------------------------#
# FOOTER AND  ABCAP AND BARCAP LOGOS ON FIRST PAGE
#---------------------------------------------------#

def FirstPageLF(c):

    BuildLogos(c)
    BuildFooter(c)
    
def FirstPageHeader(canvas, t):
    
    #Confirmation Title
    canvas.setFont('Helvetica-Bold', 12)
    canvas.drawString(8.5 * cm, 24.5*cm, 'CONFIRMATION')
    
    #Counterparty Header Details
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(1.5 * cm, 23.5*cm, 'DATE:')
    canvas.drawString(1.5 * cm, 23.0*cm, 'TO:')
    canvas.drawString(1.5 * cm, 22.5*cm, 'ATT:')
    canvas.drawString(1.5 * cm, 22.0*cm, 'TEL:')
    canvas.drawString(1.5 * cm, 21.5*cm, 'FAX:')
    canvas.drawString(1.5 * cm, 21.0*cm, 'E-MAIL:')
    canvas.drawString(1.5 * cm, 20.5*cm, 'FROM:')
    canvas.drawString(1.5 * cm, 20.0*cm, 'SUBJECT:')
    canvas.drawString(1.5 * cm, 19.5*cm, 'REFERENCE NO:')
    
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(4.5 * cm, 20.5*cm, 'Absa Bank Limited, Johannesburg')
        
    #Draws line under Header Details
    canvas.line(1.5*cm, 19.0*cm, 18.8*cm, 19.0*cm)
    
#-----------------------------------------------------------------------------#
#   Counterparty Header Details on first page
#-----------------------------------------------------------------------------# 
    DATE        = t.acquire_day.to_string('%d %B %Y')
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
