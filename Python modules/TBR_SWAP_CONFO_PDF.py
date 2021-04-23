import ael, os, acm
from reportlab.pdfgen.canvas import Canvas

from ConfirmationHeader import FirstPageLF, FirstPageHeader
from SwapLegalTemp      import SwapMod1, SwapMod2, SwapMod3, SwapMod4, AccountDetails, SwapMod5, SwapMod6, SwapMod7, SwapMod8, Signatures               
from SwapTransTerm      import TransactionTerms, PaymentDates, BreakClause        

def ASQL(*rest):
    acm.RunModuleWithParameters( 'SWAP_CONFO_PDF', 'Standard' )
    return 'SUCCESS'
    
def TrdFilter():

    TrdFilter=[]
    
    for t in ael.TradeFilter:
        TrdFilter.append(t.fltid)
    TrdFilter.sort()
    return TrdFilter

     
def TrdStatus():
    
    TrdStatus=[]
    
    for i in range(11):
        TrdStatus.append(ael.enum_to_string("TradeStatus", i))
    TrdStatus.sort()
    return TrdStatus
    
ael_variables= [('TrdFilter', 'Trade Filter', 'string', TrdFilter(), '', 0),
                ('trdnbr', 'Trade Number:', 'string', None, '0'),
                ('date', 'Date(dd/mm/yyyy)', 'string', ael.date_today(), ael.date_today(), 1 ),
                ('TrdStatus', 'Status', 'string', TrdStatus(), '', 0)]

def ael_main(dict):
    
    pdf = Canvas('F:/Swap Confirmation.pdf')
    print 'Loading...'
    if dict['TrdFilter'] != '':
        tf = ael.TradeFilter[dict['TrdFilter']].trades()
        for trd in tf:	
            if trd.insaddr.instype == 'Swap':
                if dict['TrdStatus'] != '':
                    if dict['TrdStatus'] == trd.status :
                        if dict['date']== str(ael.date_from_time(trd.time)):
                            
                            term = ael.date_from_time(trd.time).add_months(1).years_between(trd.insaddr.exp_day)
                                                       
                            ConfoDoc = FirstPageLF(pdf)
                            ConfoDoc = FirstPageHeader(pdf, trd)
                            ConfoDoc = SwapMod1(pdf, trd)
                            ConfoDoc = SwapMod2(pdf, trd)
                            ConfoDoc = SwapMod3(pdf)
                            ConfoDoc = SwapMod4(pdf)
                            ConfoDoc = TransactionTerms(pdf, trd)
                            ConfoDoc = PaymentDates(pdf, trd)
                            ConfoDoc = AccountDetails(pdf, trd)
                            ConfoDoc = SwapMod5(pdf, trd)
                            ConfoDoc = SwapMod6(pdf)
                            ConfoDoc = SwapMod7(pdf)
                            ConfoDoc = SwapMod8(pdf)
                            
                            if term > 3.0 and term < 4.0 or term >= 4.0:
                                ConfoDoc = BreakClause(pdf, trd)
                                Confodoc = Signatures(pdf, trd)
                            else:
                                Confodoc = Signatures(pdf, trd)
                else:
                    func=acm.GetFunction('msgBox', 3)
                    func("Warning", "Please Specify Trade Status! Confirmation Will Not Be Generated!", 0)
                    break
                
        pdf.save()
        
    elif dict['trdnbr'] != '0':
        for trd in dict['trdnbr'].replace(' ', '').split(','):
            try:    
                trade = ael.Trade[int(trd)]
                if trade.insaddr.instype == 'Swap' and trade.status == 'BO Confirmed':
                    if dict['date']== str(ael.date_from_time(trade.time)):
                        term = ael.date_from_time(trade.time).add_months(1).years_between(trade.insaddr.exp_day)
                        
                        ConfoDoc = FirstPageLF(pdf)
                        ConfoDoc = FirstPageHeader(pdf, trade)
                        ConfoDoc = SwapMod1(pdf, trade)
                        ConfoDoc = SwapMod2(pdf, trade)
                        ConfoDoc = SwapMod3(pdf)
                        ConfoDoc = SwapMod4(pdf)
                        ConfoDoc = TransactionTerms(pdf, trade)
                        ConfoDoc = PaymentDates(pdf, trade)
                        ConfoDoc = AccountDetails(pdf, trade)
                        ConfoDoc = SwapMod5(pdf, trade)
                        ConfoDoc = SwapMod6(pdf)
                        ConfoDoc = SwapMod7(pdf)
                        ConfoDoc = SwapMod8(pdf)
                        
                        if term > 3.0 and term < 4.0 or term >= 4.0:
                            ConfoDoc = BreakClause(pdf, trade)
                            Confodoc = Signatures(pdf, trade)
                        else:
                            Confodoc = Signatures(pdf, trade)
                    else:
                        func=acm.GetFunction('msgBox', 3)
                        func("Warning", "Invalid Date! Confirmation Will Not Be Generated! ", 0)
                        break
                else:
                    func=acm.GetFunction('msgBox', 3)
                    func("Warning", "Invalid Trade Number! Confirmation Will Not Be Generated!", 0)
                    break
            except:
                func=acm.GetFunction('msgBox', 3)
                func("Warning", "Invalid Trade Number! Confirmation Will Not Be Generated!", 0)
                break
                
        pdf.save()
    print 'Done...'    
    os.startfile('F:/Swap Confirmation.pdf')
