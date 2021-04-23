'''
Developer   : Ickin Vural
Module      : CashFlow_PDF_Report_Generator
Date        : 05/01/2010
Description : Generates PDF Report for trades CashFlows
CR		: C000000537548,C000000542772
'''

import ael, acm, os
import reportlab.lib.pagesizes

from reportlab.pdfgen.canvas  import Canvas
from reportlab.lib.pagesizes  import *
from CashFlowReportPdfBuilder import BuildCashFlow


def ASQL(*rest):
    acm.RunModuleWithParameters('CashFlow_PDF_Report_Generator', 'Standard' )
    return 'SUCCESS'   

ael_variables = [('trdnbr', 'Trade Number:', 'string', None, '0'),
                 ('date', 'Date:', 'string', ael.date_today(), ael.date_today(), 1)]
                 
def ael_main(dict): 
    
    try:
        date = ael.date(dict['date'])
    except:
        func=acm.GetFunction('msgBox', 3)
        func("Warning", "Invalid Date!", 0)
        return 'Invalid Date!'
    
    ClientName = ''
    if dict['trdnbr'] != 0:
        try:
            for trd in dict['trdnbr'].replace(' ', '').split(','):
                t = ael.Trade[int(trd)]
                tmp = 'F:/'+ str(t.trdnbr)+  ' - '+ date.to_string('%d %b %Y') + '.pdf'  
                                   
                try:
                    os.remove(tmp)
                except Exception, e:
                    print e
                try:
                    pdf = Canvas(tmp, pagesize = A4)
                except Exception, e:
                    print e
                

                BuildCashFlow(1, t, date, pdf)
                pdf.save()                    
                os.startfile(tmp)
        except:
            func=acm.GetFunction('msgBox', 3)
            func("Warning", "Invalid Trade Number!", 0) 
            return 'Invalid Trade Number!'
    print 'Complete'
