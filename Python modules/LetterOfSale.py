 #  Developer           : Tshepo Mabena, Jaysen Naicker, Jan Sinkora
 #  Purpose             : [Fixing a bug in the modules(LetterOfPurchase and LetterOfSale modules)],[Fixing to reflect correct price values], [Added in new signature], [long silo label wraps onto two lines]
 #  Department and Desk : Ops - Confirmations Team, Ops - Confirmations Team
 #  Requester           : Mampho Dhlamini, Mampho Dhlamini
 #  CR Number           : 206161,697918, 891988, 656220

import ael, time
import reportlab.lib.pagesizes

from PIL                     import Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import *
from reportlab.lib.units     import cm, inch
from STATIC_TEMPLATE         import BuildLogos, BuildFooter
from reportlab.lib.colors    import black 
from zak_funcs               import formnum
from reportlab.lib           import colors
from reportlab.lib.colors    import black

def LetterOfSale(temp,t,TempLetter,*rest):
    
    TransactionDate = str(ael.date_from_time(t.creat_time).to_string("%d %B %Y"))
    DealNumber      = str(t.trdnbr)
    Tonnage         = str(t.quantity*-1)
    InstrumentId    = t.insaddr.insid
    
    if t.counterparty_ptynbr:   
        Buyer      = t.counterparty_ptynbr.ptyid
    else:
        Buyer = ''
    
    Silo  = ''    
    for addinfo in t.additional_infos():
        if addinfo.addinf_specnbr.field_name == 'AgriSiloLocation':
            Silo = addinfo.value
            
    TransDiff = 0.0
    Price     = t.price

    sum=0.0

    for p in t.payments():
        if p.type=='Premium':
            sum+=p.amount
    
    if  Price == 0.0:
        for addinfo in t.additional_infos():
            if addinfo.addinf_specnbr.field_name == 'AgriTransportDiff':
                TransDiff = float(addinfo.value)
                if TransDiff == 0.0:
                    Price     = formnum(sum/abs(t.quantity))
                else:
                    Price = formnum(sum/abs(t.quantity) - TransDiff)
    else:
        for addinfo in t.additional_infos():
            if addinfo.addinf_specnbr.field_name == 'AgriTransportDiff':
                TransDiff = float(addinfo.value)
                if TransDiff == 0.0:
                    Price     = formnum(t.price)
                else:
                    Price = formnum(t.price - TransDiff)
                
    Grade      = ' '
    OptionType = ' '
    SiloID     = ' '
    product    = ' '
    
    if t.insaddr.instype == 'Option':
        Grade = t.insaddr.insid[8:12]
        
        if t.insaddr.insid[8:12]  == 'YMAZ':
            product = 'YELLOW MAIZE'
        
        elif t.insaddr.insid[8:12] == 'SOYA':
            product = 'SOYA'
        
        elif t.insaddr.insid[8:12] == 'WMAZ':
            product = 'WHITE MAIZE'
    
        elif t.insaddr.insid[8:12] == 'SUNS':
            product = 'SUNSEED'
            
        elif t.insaddr.insid[8:12] == 'SUNF':
            product = 'SUNFLOWER'
            
        elif t.insaddr.insid[8:12] == 'WEAT':
            product = 'WHEAT'
            
        elif t.insaddr.insid[8:12] == 'SORG':
            product = 'SORGHUM'
        else:
            product = t.insaddr.insid[8:12]
            
        if t.insaddr.insid[19]   == 'P':
            OptionType = 'Put'
            SiloID     = 'R'+ t.insaddr.insid[21:] + ' ' + t.insaddr.insid[13:18] + ' ' + OptionType         
        elif t.insaddr.insid[19] == 'C':
            OptionType = 'Call'
            SiloID     = 'R'+ t.insaddr.insid[21:] + ' ' + t.insaddr.insid[13:18] + ' ' + OptionType         
    else: 
        Grade = t.insaddr.insid[13:]
            
        if t.insaddr.insid[4:8]  == 'YMAZ':
            product = 'YELLOW MAIZE'
            
        elif t.insaddr.insid[4:8] == 'SOYA':
            product = 'SOYA'
        
        elif t.insaddr.insid[4:8] == 'WMAZ':
            product = 'WHITE MAIZE'
    
        elif t.insaddr.insid[4:8] == 'SUNS':
            product = 'SUNSEED'
            
        elif t.insaddr.insid[4:8] == 'SUNF':
            product = 'SUNFLOWER'
            
        elif t.insaddr.insid[4:8] == 'WEAT':
            product = 'WHEAT'
            
        elif t.insaddr.insid[4:8] == 'SORG':
            product = 'SORGHUM'
            
    if t.insaddr.instype == 'Future/Forward':
        SiloID = 'FWD ' + ' ' + t.insaddr.insid[16:]    
        Grade  = t.insaddr.und_insaddr.insid[13:]
    
    #Logos and Footer
    BuildLogos(TempLetter)
    BuildFooter(TempLetter)
    
    # Header
    TempLetter.setFillColor(black)
    TempLetter.setFont("Helvetica-Bold", 10.0)
    TempLetter.drawString(7.5 *cm, 24.5*cm, 'LETTER OF SALE') 

    #Contact Details   
    TempLetter.setFont("Helvetica-Bold", 8.0)
    TempLetter.drawString(13.5 *cm, 23.5*cm, 'ABSA AGRICULTURAL COMMODITIES') 
    TempLetter.drawString(13.5 *cm, 23.0*cm, 'TEL: (011) 895 - 7592')  
    TempLetter.drawString(13.5 *cm, 22.5*cm, 'FAX: (011) 895 - 7822') 

    #Trade Details  
    TempLetter.drawString(13.5 *cm, 22.0*cm, 'DATE: ........................................................................')   
    TempLetter.drawString(13.5 *cm, 21.0*cm, 'DEAL NUMBER: ........................................................')  
    TempLetter.drawString(13.5 *cm, 20.5*cm, 'INSTRUMENT ID: ......................................................')  
    TempLetter.drawString( 2.0 *cm, 20.5*cm, 'BUYER: ...............................................................................................')   
    TempLetter.drawString( 2.0 *cm, 20.0*cm, 'SELLER: ABSA AGRICULTURAL COMMODITIES')    

    TempLetter.setFont("Helvetica-Bold", 8.0)
    TempLetter.drawString(  2.0 *cm, 19.0*cm, 'PRODUCT')    
    TempLetter.drawString(  4.7 *cm, 19.0*cm, 'GRADE')    
    TempLetter.drawString(  6.0 *cm, 19.0*cm, 'TONNAGE')    
    TempLetter.drawString(  7.5 *cm, 19.0*cm, 'SILO/DETAIL')
    TempLetter.drawString( 14.5 *cm, 19.0*cm, 'AGRI DIFF')
    TempLetter.drawString( 16.7 *cm, 19.0*cm, 'PRICE, EX SILO, VAT EXCL.') 

    TempLetter.setFont("Helvetica", 8.0)
    TempLetter.drawString(15.0 *cm, 22.1*cm, TransactionDate) 
    TempLetter.drawString(16.0 *cm, 21.1*cm, DealNumber)
    TempLetter.drawString(16.0 *cm, 20.6*cm, InstrumentId)
    TempLetter.drawString( 3.5 *cm, 20.6*cm, Buyer)
    TempLetter.drawString( 2.0 *cm, 18.5*cm, product)    
    TempLetter.drawString( 4.7 *cm, 18.5*cm, Grade)    
    TempLetter.drawString( 6.0 *cm, 18.5*cm, Tonnage)
    
    silo = ''
    if t.insaddr.instype == 'Future/Forward':    
        #TempLetter.drawString( 7.5 *cm, 18.5*cm, SiloID + ' ' + Silo)
        silo = SiloID + ' ' + Silo
    else:
        #TempLetter.drawString( 7.5 *cm, 18.5*cm, Silo + ' ' + SiloID)
        silo = Silo + ' ' + SiloID
    
    # get the rendered width
    text = TempLetter.beginText(3.5*cm, 20.6*cm)
    width = TempLetter.stringWidth(silo, text._fontname, text._fontsize)
    field_width = 6 * cm
    
    # check if the label fits
    if width <= field_width:
        # a fit, render the label
        TempLetter.drawString( 7.5 *cm, 18.5*cm, silo)
    else:
        # a misfit, split the string
        split_index = int((field_width / width) * len(silo))
        
        # find the rightmost space to the split point
        index = silo.rfind(' ', 0, split_index)
        if index == -1:
            # there is no space, split inside a word
            TempLetter.drawString( 7.5 *cm, 18.5*cm, silo[:split_index])
            TempLetter.drawString( 7.5 *cm, 18.1*cm, silo[split_index:])
        else:
            # split on the space found
            TempLetter.drawString( 7.5 *cm, 18.5*cm, silo[:index])
            TempLetter.drawString( 7.5 *cm, 18.1*cm, silo[index+1:])
    
    TempLetter.drawString(14.5 *cm, 18.5*cm, str(TransDiff))
    TempLetter.drawString(16.7 *cm, 18.5*cm, 'R '+ str(Price)) 
            
def PaymentAndDeliverySale(temp,Letter,t,PayAndDeliver,date,Time,InterestCost,TransDate,*rest):
    
    #Transaction Date
    TransactionDate = str(ael.date_from_time(t.creat_time).to_string("%d %B %Y"))
    
    Letter.setFont("Helvetica-Bold", 8.0)   
    Letter.drawString(2.0 *cm, 17.5*cm, 'PAYMENT AND DELIVERY:')    
    Letter.drawString(2.0 *cm, 16.5*cm, 'CANCELLATION:')    
    Letter.drawString(2.0 *cm, 15.0*cm, 'INTEREST COST:')
    Letter.drawString(2.0 *cm, 14.0*cm, 'PACKING:')
    Letter.drawString(2.0 *cm, 13.5*cm, 'STORAGE COST:')
    Letter.drawString(2.0 *cm, 12.5*cm, 'TRANSPORT COST:')
    Letter.drawString(2.0 *cm, 12.0*cm, 'MOISTURE LEVEL:')
    Letter.drawString(2.0 *cm, 11.0*cm, 'TRANSACTION DATE:')
    
    Letter.setFont("Helvetica", 7.0)      
    Letter.drawString(6.0 *cm, 17.5*cm, 'Payment must take place within .................. working day/s from the date of transaction.The silo receipt will only be released once')    
    Letter.drawString(6.0 *cm, 17.0*cm, 'ABSA has payment for the full tonnage and agreed price. See banking details below.') 
    
    Letter.drawString(6.0 *cm, 16.5*cm, 'On default of payment by (date)..........................(time).............................ABSA reserves the right to cancel the transaction with the') 
    Letter.drawString(6.0 *cm, 16.0*cm, 'counterparty liable for any adverse price movements between transaction date and cancellation date. Should the SAFEX closing') 
    Letter.drawString(6.0 *cm, 15.5*cm, 'price of the near month be lower than the original transaction rate, ABSA will invoice the client with the full difference in consideration.') 
    
    Letter.drawString(6.0 *cm, 15.0*cm, "If payment has not been affected within ........... days after transaction date, interest will be charged at a rate of 2% above") 
    Letter.drawString(6.0 *cm, 14.5*cm, "ABSA's prime.") 
    
    Letter.drawString(6.0 *cm, 14.0*cm, "In bulk.") 
    
    Letter.drawString(6.0 *cm, 13.5*cm, "Storage cost is for the account of the seller up to the date of transaction. After the transaction date it will be for the account of the") 
    Letter.drawString(6.0 *cm, 13.0*cm, "buyer.")
 
    Letter.drawString(6.0 *cm, 12.5*cm, "Transport cost and VAT on transport cost is for the buyer's account.") 
    
    Letter.drawString(6.0 *cm, 12.0*cm, "Not more than 14% - payment on 12.5%") 
    
    Letter.drawString(6.0 *cm, 11.0*cm, "."*90) 
    
        
    Letter.drawString(2.0 *cm, 10.0*cm, "Should there be any irregularities on the buyer's side, ABSA reserves the right to hold the buyer fully responsible for any losses that might occur.") 
    
    Letter.drawString(2.0 *cm, 9.0*cm, "I (full name)  ........................................................................... hereby accept and commit myself to the terms and conditions applicable to this contract.")
    
    Letter.setFont("Helvetica-Bold", 8.0)      
    Letter.drawString(2.0 *cm, 8.0*cm, 'BANKING DETAILS: Bank ABSA Eloff Street. Account number: 660158642.') 

    Letter.setFont("Helvetica-Bold", 7.0)      
    Letter.drawString( 2.0 *cm, 5.0*cm, '_'*35) 
    Letter.drawString( 8.0 *cm, 5.0*cm, '_'*35)  
    Letter.drawString(14.0 *cm, 5.0*cm, '_'*35) 
    
    Letter.drawString( 3.0 *cm, 4.5*cm, 'ABSA Agricultural Commodities') 
    Letter.drawString( 9.0 *cm, 4.5*cm, 'Buyer (Signature)') 
    Letter.drawString(16.0 *cm, 4.5*cm, 'Date') 
    
    Letter.setFont("Helvetica", 6.5)
    Letter.setStrokeColorRGB(1, 0, 0)
    
    Letter.drawInlineImage('Y:\Jhb\Arena\Data\Confirmations\Signatures\Trader.jpg', 1.3*inch, 2.0*inch, 1.0*inch, 1.0*inch)
    
 
    Letter.drawString(6.5 *cm, 4.0*cm, 'PLEASE FAX COPY BACK TO THE FAX NUMBER MENTIONED ABOVE') 
    
    Letter.setFont("Helvetica", 7.0)      
    Letter.drawString( 6.0 *cm, 11.1*cm, TransDate) 
    Letter.drawString(10.0 *cm, 17.55*cm, str(PayAndDeliver))
    Letter.drawString( 9.7 *cm, 16.6*cm, date)
    Letter.drawString(12.5 *cm, 16.6*cm, Time)
    Letter.drawString(10.7 *cm, 15.05*cm, str(InterestCost))
    
    Letter.showPage()
