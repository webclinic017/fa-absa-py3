import ael, acm, os
import reportlab.lib.pagesizes

from reportlab.pdfgen.canvas import Canvas
from Header                  import FirstPageLF, FirstPageHeader
from ShortFormLegal          import ShortMod1, ShortMod2, ShortMod3, ShortMod4, ShortMod5, AccountDetails, ShortMod6, ShortMod7\
                                    , ShortMod8, ShortMod9, Disclaimer    
from ShortTransTerms         import TransactionTerms
from Signatures              import Signatures  


def ASQL(*rest):
    acm.RunModuleWithParameters( 'SANLD_FX_Option_Short_Form_PDF', 'Standard' )
    return 'SUCCESS'
    
    
ael_variables = [('trdnbr', 'Trade Number', 'string', None, '0', 1),
                ('date', 'Date (dd/mm/ccyy)', 'string', ael.date_today(), ael.date_today(), 1),
                ('ACBB', 'ACBB Client', 'string', ['Yes', 'No'], '0')]

def ael_main(dict):
    
    print 'Loading...'
    if dict['trdnbr'] != '0':
        pdf = Canvas('F:/FX Option Confirmation.pdf') 
        for trd in dict['trdnbr'].replace(' ', '').split(','):
            try:
                trade = ael.Trade[int(trd)]
                Date = dict['date']
                if cmp(str(trade.acquire_day), Date) == 0:
                    if trade.insaddr.und_insaddr.instype == 'Curr':
                        if trade.insaddr.instype == 'Option':
                            if trade.status not in ['Simulated', 'Terminated', 'Void']:
                                try:
                                    ConfoDoc = FirstPageLF(pdf)            
                                    ConfoDoc = FirstPageHeader(pdf, trade) 
                                    ConfoDoc = ShortMod1(pdf, trade)
                                    ConfoDoc = ShortMod2(pdf, trade)
                                    ConfoDoc = ShortMod3(pdf)         
                                    ConfoDoc = TransactionTerms(pdf, trade)        
                                    ConfoDoc = ShortMod4(pdf)
                                    ConfoDoc = ShortMod5(pdf)
                                    ConfoDoc = AccountDetails(pdf, trade)
                                    ConfoDoc = ShortMod6(pdf, trade)   
                                    ConfoDoc = ShortMod7(pdf)
                                    ConfoDoc = ShortMod8(pdf)        
                                    ConfoDoc = ShortMod9(pdf)         
                                    ConfoDoc = Signatures(pdf, trade)      
                                                                        
                                    if dict['ACBB'] == 'Yes':
                                            ConfoDoc = Disclaimer(pdf)    
                                    
                                except:
                                    func=acm.GetFunction('msgBox', 3)
                                    func("Warning", "Fatal Error! No confirmation can be generated ", 0)
                                    break
                else:
                    func=acm.GetFunction('msgBox', 3)
                    func("Warning", "Invalid Date! Error generating confirmation...", 0)
                    break
            except:
                func=acm.GetFunction('msgBox', 3)
                func("Warning", "Invalid Trade Number! Error generating confirmation...", 0)
                break
            pdf.save()
        print 'Done.....'            
        os.startfile("F:/FX Option Confirmation.pdf")   
