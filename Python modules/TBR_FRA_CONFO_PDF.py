import ael, os, acm

from reportlab.pdfgen.canvas import Canvas
from FRAHEADER               import FirstPageLF, FirstPageHeader
from FRALegal                import FRAMod1, FRAMod2, FRAMod3, FRAMod4, FRAMod5, FRAMod6, AccountDetails,\
                                    FRAMod7, FRAMod8, FRAMod9, FRAMod10, Signatures
from FRATERMS                import TransactionTerms

def ASQL(*rest):
    acm.RunModuleWithParameters( 'FRA_CONFO_PDF', 'Standard' )
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
    
    pdf = Canvas('F:/FRA Confirmation.pdf')
    print 'Loading...'
    if dict['TrdFilter'] != '':
        tf = ael.TradeFilter[dict['TrdFilter']].trades()
        for trd in tf:
            if trd.insaddr.instype == 'FRA':
                if dict['TrdStatus'] != '':
                    if dict['TrdStatus'] == trd.status :
                        if dict['date']== str(ael.date_from_time(trd.time)):
                            
                            ConfoDoc = FirstPageLF(pdf)
                            ConfoDoc = FirstPageHeader(pdf, trd)
                            ConfoDoc = FRAMod1(pdf, trd)
                            ConfoDoc = FRAMod2(pdf, trd)
                            ConfoDoc = FRAMod3(pdf)
                            ConfoDoc = FRAMod4(pdf)
                            ConfoDoc = FRAMod5(pdf)
                            ConfoDoc = FRAMod6(pdf)
                            ConfoDoc = TransactionTerms(pdf, trd)
                            ConfoDoc = AccountDetails(pdf, trd)
                            ConfoDoc = FRAMod7(pdf, trd)
                            ConfoDoc = FRAMod8(pdf)
                            ConfoDoc = FRAMod9(pdf)
                            ConfoDoc = FRAMod10(pdf)
                            Confodoc = Signatures(pdf, trd)
                        
                else:
                    func=acm.GetFunction('msgBox', 3)
                    func("Warning", "Please Specify Status! Confirmation Will Not Be Generated!", 0)
                    break
            else:
                func=acm.GetFunction('msgBox', 3)
                func("Warning", "Trade Filter Error! Confirmation Will Not Be Generated!", 0)
                break
                
        pdf.save()
        
    elif dict['trdnbr'] != '0':
        for trd in dict['trdnbr'].replace(' ', '').split(','):
            try:    
                trade = ael.Trade[int(trd)]
                if trade.insaddr.instype == 'FRA' and trade.status == 'BO Confirmed':
                    if dict['date']== str(ael.date_from_time(trade.time)):
                                                
                        ConfoDoc = FirstPageLF(pdf)
                        ConfoDoc = FirstPageHeader(pdf, trade)
                        ConfoDoc = FRAMod1(pdf, trade)
                        ConfoDoc = FRAMod2(pdf, trade)
                        ConfoDoc = FRAMod3(pdf)
                        ConfoDoc = FRAMod4(pdf)
                        ConfoDoc = FRAMod5(pdf)
                        ConfoDoc = FRAMod6(pdf)
                        ConfoDoc = TransactionTerms(pdf, trade)
                        ConfoDoc = AccountDetails(pdf, trade)
                        ConfoDoc = FRAMod7(pdf, trade)
                        ConfoDoc = FRAMod8(pdf)
                        ConfoDoc = FRAMod9(pdf)
                        ConfoDoc = FRAMod10(pdf)
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
    os.startfile('F:/FRA Confirmation.pdf')
                            


