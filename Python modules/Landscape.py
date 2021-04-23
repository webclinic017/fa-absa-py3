"""------------------------------------------------------------------------------------------------------------------------------------
Name        : Landsacpe
Developer   : [Tshepo Mabena],[Willie van der Bank]
Date        : [22/01/2009],[24/06/2010],[831374 17/11/2011]
Description : [This AEL module is developed to embed logos(Absa and Barclays logos) and footers on pdf documents in landscape format.
	      This module is used to generate client valuations],[Updated directors],[Updated directors]
---------------------------------------------------------------------------------------------------------------------------------------"""

import ael

from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import *
from reportlab.lib.units import cm, inch

def BuildLogos(ConfoTemp):
    
    # ABCap and BARCap Logos
    if ael.user().grpnbr.grpid in ('Integration Process', 'System Processes'):
        folder = '//nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/LOGOS/'
    else:
        folder = 'Y:/Jhb/FAReports/AtlasEndOfDay/LOGOS/'
    
    ConfoTemp.setFont("Helvetica", 6.5)
    ConfoTemp.setStrokeColorRGB(1, 0, 0)
    ConfoTemp.drawInlineImage(folder + 'capitalA.jpg', 9.2*inch, 6.8 *inch, 2.5*inch, 1.2*inch)
    ConfoTemp.drawInlineImage(folder + 'ABCAPLOGO.jpg', 0.8*inch, 1.2*inch, 2.0*inch, 0.5*inch)
    return ConfoTemp
    
def BuildFooter(ConfoTemp):
    
    # Footer
    
    ConfoTemp.setFont("Times-Roman", 8.0)
    ConfoTemp.drawString(0.8 * inch, 2.5*cm, '15 Alice Lane Sandton 2196 Private Bag X10056 Sandton 2146')
    ConfoTemp.drawString(0.8 * inch, 2.2*cm, 'Tel +27 11 895 6000  Fax +27 11 895 7802 www.absacapital.com')
    
    ConfoTemp.setFont("Times-Roman", 8.0)
    ConfoTemp.drawString(0.8 * inch, 1.79*cm, "Directors: G  Griffin (Chairman) *M Ramos (Chief Executive)  C Beggs  BP Connellan  YZ Cuba  IR Ritossa (Australian)")
    ConfoTemp.drawString(0.8 * inch, 1.48*cm, 'SA  Fakie  *DWP Hodnett  MJ  Husain  AP  Jenkins (British)  R Le Blanc (British) PB Matlare')
    ConfoTemp.drawString(0.8 * inch, 1.17*cm, 'TM  Mokgosi-Mwantembe EC  Mondlane  Jr (Mozambican) TS  Munday  SG Pretorius  *LL  Von Zeuner  BJ  Willemse')
    ConfoTemp.drawString(0.8 * inch, 0.86*cm, '*Executive  Directors      Secretary:  S Martin         (12/2011)')
    ConfoTemp.setFont("Times-Roman", 5.0)
    ConfoTemp.drawString(1.5 * inch, 0.6*cm, 'Authorised Financial Services Provider - Registered Credit Provider, Reg-no NCRCP7')
    return ConfoTemp
