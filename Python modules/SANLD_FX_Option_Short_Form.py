import ael, acm, os
import reportlab.lib.pagesizes
from reportlab.pdfgen.canvas import Canvas
import ConfirmationTemplate                                   

def ASQL(*rest):
    acm.RunModuleWithParameters( 'SANLD_FX_Option_Short_Form', 'Standard' )
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
                                    ConfoDoc = ConfirmationTemplate.FirstPageLF(pdf)            #Calls ABCap, BARCap Logos and Footer on the First Page 
                                    ConfoDoc = ConfirmationTemplate.FirstPageHeader(pdf, trade)  #Calls Counterparty header details on the first page 
                                    ConfoDoc = ConfirmationTemplate.LongShortPara1(pdf, trade)   #Calls First  paragraph on first page of the confo 
                                    ConfoDoc = ConfirmationTemplate.ShortFormPara1(pdf, trade)   #Calls Second paragaph  on first page of the confo
                                    ConfoDoc = ConfirmationTemplate.ShortFormPara2(pdf)         #Calls Third  paragaph  on first page of the confo     
                                    ConfoDoc = ConfirmationTemplate.ShortFormPara3(pdf)         #Calls Fourth paragaph  on first page of the confo
                                    ConfoDoc = ConfirmationTemplate.ShortFormPara4(pdf)         #Calls Fifth  paragaph  on first page of the confo
                                    ConfoDoc = ConfirmationTemplate.TransactionTerms(pdf, trade) #Calls Terms of the transaction on the second page of the confo
                                    ConfoDoc = ConfirmationTemplate.LongShortPara2(pdf)         #Calls details on the third page       
                                    ConfoDoc = ConfirmationTemplate.AccountDetails(pdf, trade)   #Calls Account details on fourth page
                                    ConfoDoc = ConfirmationTemplate.LongShortPara3(pdf, trade)   #Calls First paragraph on fourth page 
                                    ConfoDoc = ConfirmationTemplate.LongShortPara4(pdf)         #Calls Second paragraph on fourth page 
                                    ConfoDoc = ConfirmationTemplate.LongShortPara5(pdf)         #Calls Third paragraph on fourth page      
                                    ConfoDoc = ConfirmationTemplate.LongShortPara6(pdf)         #Calls Fourth paragraph on fourth page 
                                    ConfoDoc = ConfirmationTemplate.Signatures(pdf, trade)       #Calls signatures on fifth page
                                    
                                    if dict['ACBB'] == 'Yes':
                                             ConfoDoc = ConfirmationTemplate.Disclaimer(pdf)    #Disclaimer on the last page attached if counterparty is ACBB client 
                                    
                                except:
                                    func=acm.GetFunction('msgBox', 3)
                                    func("Warning", "Fatal Error! No confirmation can be generated ", 0)
                else:
                    func=acm.GetFunction('msgBox', 3)
                    func("Warning", "Invalid Date! Error generating confirmation...", 0)
            except:
                func=acm.GetFunction('msgBox', 3)
                func("Warning", "Invalid Trade Number! Error generating confirmation...", 0)
            
            pdf.save()
        print 'Done.....'            
        os.startfile("F:/FX Option Confirmation.pdf")   

