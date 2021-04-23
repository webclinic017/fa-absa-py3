 #----------------------------------------------------------------------------------------------
 #  Name      : Commodities_Confirmation
 #  Purpose   : Builds Agris confirmations
 #  Developer : Tshepo Mabena
 #  Date      : 26-05-2009
 #
 #  Changes
 #
 #  Developer           : Tshepo Mabena
 #  Purpose             : Fixing a bug in the modules(LetterOfPurchase and LetterOfSale modules).
 #  Department and Desk : Ops - Confirmations Team
 #  Requester           : Mampho Dhlamini
 #  CR Number           : 206161 
 #-----------------------------------------------------------------------------------------------

import ael, acm, os

from reportlab.pdfgen.canvas import Canvas
from LetterOfPurchase        import PurchaseLetter, PaymentAndDeliveryPurchase
from LetterOfSale            import LetterOfSale, PaymentAndDeliverySale
from reportlab.lib.pagesizes import *

def ASQL(*rest):
    acm.RunModuleWithParameters( 'Commodities_Confirmation', 'Standard' )
    return 'SUCCESS'

ael_variables = [('trdnbr', 'Trade Number', 'string', None, '0', 1),
                 ('PaymentAndDelivery', 'Payment And Delivery', 'string', ['1', '2', '3', '4', '5'], '1', 1),  
                 ('date', 'Cancelation Date', 'string', ael.date_today(), ael.date_today(), 1),
                 ('time', 'Cancelation Time', 'string', ['12H00', '24H00'], '12H00', 1),
                 ('InterestCost', 'Interest Cost', 'string', ['1', '2'], '1', 1),
                 ('TransDate', 'Transaction Date', 'string', ' ', ' ', 1)]
                
def ael_main(dict):
    
    try:
        date = ael.date(dict['date'])
    except:
        func=acm.GetFunction('msgBox', 3)
        func("Warning", "Invalid Date!", 0)
        raise Exception("Warning", "Invalid Date!")

    if dict['trdnbr'] != '0':
        for trd in dict['trdnbr'].replace(' ', '').split(','):
            trade = ael.Trade[int(trd)]
            
            if trade.counterparty_ptynbr:
                ClientName = trade.counterparty_ptynbr.ptyid
            else:    
                ClientName = ''
                print 'Trade ', t.trdnbr, ' does not have a counterparty'
            break
    
    SavePath   = 'Y:/Jhb/Operations Secondary Markets/Agris Confirmations/'
    #SavePath = 'F:/'
    directory = SavePath + ael.date_today().to_string('%Y%m%d') 
    
    if os.path.exists(directory):
        path = directory
    else:
        os.mkdir(directory)
        path = directory   
        
    tmp = path + '/Agris Confirmation ' + '-' + ClientName + ' ('+ str(trade.trdnbr)+ ') ' + '-'+ date.to_string('%d %b %Y') + '.pdf'    
    pdf = Canvas(tmp, pagesize = A4)
    
    
    if dict['trdnbr'] != '0':
        for trd in dict['trdnbr'].replace(' ', '').split(','):
            try:
                trade = ael.Trade[int(trd)]
                try:
                    PayAndDeliver = dict['PaymentAndDelivery']              
                    date          = dict['date']
                    Time          = dict['time']
                    InterestCost  = dict['InterestCost']
                    TransDate     = dict['TransDate'] 
                    
                    if trade.insaddr.instype in ('Commodity', 'Future/Forward', 'Option'):
                        
                        #Calls Letter Of Purchase
                        if trade.quantity > 0:
                            #try:
                            PurchaseLetter(1, trade, pdf)
                            #except Exception, e:
                            #    print 'method call', e
                            PaymentAndDeliveryPurchase(1, pdf, trade, date, Time, InterestCost, TransDate)
                            
                        #Calls Letter of Sale    
                        else:
                            LetterOfSale(1, trade, pdf)
                            PaymentAndDeliverySale(1, pdf, trade, PayAndDeliver, date, Time, InterestCost, TransDate)
                        
                    else:
                        func=acm.GetFunction('msgBox', 3)
                        func("Warning", "Invalid Trade Number", 0)
                        return "Invalid Trade Number"
                                         
                except:
                    func=acm.GetFunction('msgBox', 3)
                    func("Warning", "Fatal Error!", 0)
                    return "Fatal Error!"
            except:
                func=acm.GetFunction('msgBox', 3)
                func("Warning", 'Trade Number '+ trd +' is not a valid trade number', 0)
                return 'Trade Number '+ trd +' is not a valid trade number'

    else:
        func=acm.GetFunction('msgBox', 3)
        func("Warning", "Please Enter A Trade Number.", 0)
        return "Please Enter A Valid Trade Number"
    
    pdf.save()
    os.startfile(tmp)
