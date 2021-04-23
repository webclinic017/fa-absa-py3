'''
Developer   : Tshepo Mabena
Module      : Dev_Swap_Reset_Advice_PDF
Date        : 02/10/2009
Description : This module builds an interface to build Swap advice Note in pdf
'''

import ael, acm, os
import reportlab.lib.pagesizes

from reportlab.pdfgen.canvas  import Canvas
from reportlab.lib.pagesizes  import *
from SingleWeightedAdvice     import BuildSingleWeightedAdvice

def ASQL(*rest):
    acm.RunModuleWithParameters('Dev_Swap_Reset_Advice_PDF', 'Standard' )
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
                if t.insaddr.instype in ('Swap'):
                
                    ClientName = t.counterparty_ptynbr.fullname.replace('/', '')
                    tmp = 'Y:/Jhb/Operations Secondary Markets/DERIVATIVES/Swap Cap Floor Advice/Swap Reset Advice/SWAP RESET ADVICE'+ \
                        ' '+ ' - ' + ClientName + ' '+ ' - ' + '(' +str(t.trdnbr)+ ')' + ' - '+ date.to_string('%d %b %Y') + '.pdf'
                    pdf = Canvas(tmp, pagesize = A4)
                    
                    if t.status in ('BO Confirmed'):
                        for cf in t.insaddr.cash_flows():
                            for r in cf.resets():
                                if date == r.end_day or date == cf.end_day:
                                    if r.type in ('Weighted', 'Single'):
                                        BuildSingleWeightedAdvice(1, t, date, pdf)
                    pdf.save()                    
                    os.startfile(tmp)                    
        except:
            func=acm.GetFunction('msgBox', 3)
            func("Warning", "Invalid Trade Number!", 0) 
            return 'Invalid Trade Number!'
