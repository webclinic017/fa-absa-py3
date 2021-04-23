'''
----------------------------------------------------------------------------------------------------------------------------------------
[Tshepo Mabena]       [26/06/2008]                      [This AEL is a module to be called by other programs to set the logos and footer for pdf documents]
[Willie van der Bank] [26/11/2009]                      [Updated directors]
[Ickin Vural]         [23/04/2009]                      [Updated directors]
[Tshepo Mabena]       [24/06/2010]                      [Updated directors]
[Tshepo Mabena]       [599893 15/03/2011]               [Updated directors]
[Willie van der Bank] [656249 19/05/2011]               [Added securities header and footer]
[Anwar Banoo]         [Upgrade 12/07/2011]              [Added support for unicode in the ' char of d'V name]
[Willie van der Bank] [831374 17/11/2011]               [Updated directors]
[Willie van der Bank] [838797 24/11/2011]               [Updated securities directors]
[Jaysen Naicker]      [891988 16/02/2012]               [Updated address and added in Confidential image]
[Willie van der Bank] [318890 2012-07-12]               [Updated Securities_Footer]
Willie vd Bank        CHG1000111833     2018-02-02      Removed Barclays footer and replaced Absa Capital with Absa
Deluan Cottle         CHG1000757460     2018-08-02      Incorporated new 2018 Absa logo
 ----------------------------------------------------------------------------------------------------------------------------------------
'''

import os
from reportlab.lib.colors import black          #@UnresolvedImport
from reportlab.lib.units import cm, inch        #@UnresolvedImport

import ael
import FReportSettings as frs

LOGO_ABCAP_SECURITIES = os.path.join(frs.LOGOS_PATH, 'ABCAPSECURITIESLOGO.jpg')
LOGO_AFFILIATED_WITH_BARCLAYS = os.path.join(frs.LOGOS_PATH, 'ABCAPSECURITIESFOOTER.jpg')

ABSA_REG = 'Absa Bank Limited, Reg. No. 1986/004794/06. Authorised Financial Services Provider. Registered Credit Provider Reg. No. NCRCP7.'

ADDRESS_ALICELANE = {
    'address': [' Absa, Sandton Campus South ,  15 Alice Lane  Sandton', 'Johannesburg 2196', 'Private Bag X10056 Sandton 2146 '],
    'tel': ' +27 (0)11 895 6000 ',
    'fax': ' +27 (0)11 895 7802 ',
    'web': ' www.absa.africa '
    }

ADDRESS_TOWERSNORTH = {
    'address': [' 1st Floor Absa Towers North (1E1)', '180 Commissioner Street', 'Johannesburg 2001', 'PO Box 7735 Johannesburg 2000'],
    'tel': ' +27 11 350 4000',
    'fax': ' +27 11 350 4000',
    'web': ' www.absa.africa'
}


def _rootpath():
    use_nfs_path = ael.user().grpnbr.grpid in ('Integration Process', 'System Processes')
    return frs.LOGOS_PMO_PATH if use_nfs_path else frs.LOGOS_PATH
    
def Directors(line):
    return ''

def Address(line):
    a = ADDRESS_TOWERSNORTH
    if line == 1:
        return ' '.join(a['address'])
    elif line == 2:
        return 'Tel {0} Fax {1} {2}'.format(a['tel'], a['fax'], a['web'])

def AddressAlice(line):
    a = ADDRESS_ALICELANE
    if line == 1:
        return ' '.join(a['address'])
    elif line == 2:
        return 'Tel {0} Fax {1} {2}'.format(a['tel'], a['fax'], a['web'])
   
def BuildLogos(ConfoTemp):
    
    # Absa Logo
 
    ConfoTemp.setFont("Helvetica", 6.5)
    ConfoTemp.setStrokeColorRGB(1, 0, 0)
    ConfoTemp.drawInlineImage(os.path.join(frs.LOGOS_PATH, 'absa_logo_2018.png'), 6.5*inch, 10.3 *inch, 1.01*inch, 1.01*inch)
    ConfoTemp.setFont("Helvetica", 24)
    ConfoTemp.setFillColorRGB(0.862, 0, 0.196)
    ConfoTemp.drawString(0.4*inch, 10.35 *inch, "CONFIDENTIAL")
    
    return ConfoTemp
    
def BuildFooter(ConfoTemp):
    
    # Footer
    
    ConfoTemp.setFillColor(black)
    
    ConfoTemp.setFont("Times-Roman", 6.0)
    ConfoTemp.drawString(3.0 * cm, 2.46*cm, Address(1))
    ConfoTemp.drawString(3.0 * cm, 2.16*cm, Address(2))
    
    return ConfoTemp
    
def BuildAdviceFooter(ConfoTemp):
    
    # Footer
    ConfoTemp.setFillColor(black)
    ConfoTemp.setFont("Times-Roman", 9.0)
    ConfoTemp.drawString(2.0*cm, 2.46*cm, 'Fixed Income')
        
    ConfoTemp.setFont("Times-Roman", 6.0)
    ConfoTemp.drawString(2.0 * cm, 1.88*cm, AddressAlice(1)+AddressAlice(2))
    
    ConfoTemp.setFont("Times-Roman", 5.5)

    return ConfoTemp
    
def Term_Deposit_Footer(ConfoTemp):
    
    # Footer
    ConfoTemp.setFont("Times-Roman", 6.0)
    ConfoTemp.drawString(3.5 * cm, 1.88*cm, Address(1)+Address(2))
    
    return ConfoTemp
    
def LetterOfPurchaseFooter(ConfoTemp):
        
    ConfoTemp.setFont("Times-Roman", 5.5)
    return ConfoTemp

def Securities_Header(ConfoTemp):
    
    # ABCap securities Logo
    ConfoTemp.setFont("Helvetica", 6.5)
    ConfoTemp.setStrokeColorRGB(1, 0, 0)
    ConfoTemp.drawInlineImage(os.path.join(frs.LOGOS_PATH, 'ABCAPSECURITIESLOGO.jpg'), 5.5*inch, 10.3 *inch, 2.5*inch, 1.2*inch)
    
    return ConfoTemp
    
def Securities_Footer(ConfoTemp):
    
    # Footer
    ConfoTemp.setFont("Helvetica", 6.5)
    ConfoTemp.setStrokeColorRGB(1, 0, 0)
    ConfoTemp.drawInlineImage(os.path.join(frs.LOGOS_PATH, 'ABCAPSECURITIESFOOTER.jpg'), 0.4*inch, 1.2*inch, 1.7*inch, 0.3*inch)
    
    ConfoTemp.setFillColor(black)
    ConfoTemp.setFont("Times-Roman", 6.0)
    ConfoTemp.drawString(2.0 * cm, 2.46*cm, 'Absa Capital Securities (Pty) Ltd')
    ConfoTemp.drawString(2.0 * cm, 2.16*cm, Address(1)+Address(2))
    
    ConfoTemp.setFont("Times-Roman", 5.5)
    ConfoTemp.drawString(2.0 * cm, 1.16*cm, "ABSA CAPITAL SECURITIES (PTY) LTD, MEMBER OF ABSA GROUP LTD REG NO 2008/021179/07 MEMBER OF THE JSE LTD SOUTH AFRICA")
