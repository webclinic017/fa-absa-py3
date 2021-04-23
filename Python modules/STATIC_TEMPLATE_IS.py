"""------------------------------------------------------------------------------------------------------------------------------------

Name        : STATIC_TEMPLATE_IS
Developer   : Willie van der Bank
Date        : 02/10/2009
Description : This AEL is a module to be called by other programs to set the logos for pdf documents. Based on STATIC_TEMPLATE.

---------------------------------------------------------------------------------------------------------------------------------------"""

import ael

from reportlab.lib.units import inch

def BuildLogos(ConfoTemp):
    
    # ABCap and BARCap Logos
 
    ConfoTemp.setFont("Helvetica", 6.5)
    ConfoTemp.setStrokeColorRGB(1, 0, 0)
    if ael.user().grpnbr.grpid in ('Integration Process', 'System Processes'):  #If this module is used in a scheduled task
        ConfoTemp.drawInlineImage('/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/InterestStatements/Logos//capitalA.jpg', 5.5*inch, 10.3 *inch, 2.5*inch, 1.2*inch)
        ConfoTemp.drawInlineImage('/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/InterestStatements/Logos//ABCAPLOGO.jpg', 0.4*inch, 1.2*inch, 1.7*inch, 0.3*inch)
    else:
        ConfoTemp.drawInlineImage('Y:/Jhb//Arena//Data//Confirmations//Logos//capitalA.jpg', 5.5*inch, 10.3 *inch, 2.5*inch, 1.2*inch)
        ConfoTemp.drawInlineImage('Y:/Jhb//Arena//Data//Confirmations//Logos//ABCAPLOGO.jpg', 0.4*inch, 1.2*inch, 1.7*inch, 0.3*inch)
        
    return ConfoTemp
