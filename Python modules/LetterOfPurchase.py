 #  Developer           : Tshepo Mabena
 #  Purpose             : Fixing a bug in the modules(LetterOfPurchase and LetterOfSale modules).
 #  Department and Desk : Ops - Confirmations Team
 #  Requester           : Mampho Dhlamini
 #  CR Number           : 206161 
 
 # Changes:
 
 # Developer            : Tshepo Mabena
 # Purpose              : Fixing a bug to convert variable from float to string and fixing a Silo/Detail field on confirmation for Future/Forward.  
 # Department and Desk  : Ops - Confirmations Team
 # Requester            : Mampho Dhlamini
 # CR Number            : 249649 
 
 # Developer            : Willie van der Bank,Tshepo Mabena, Jaysen Naicker, Jan Sinkora
 # Purpose              : [Fixing a problem with Price populating as 0],[Fixing to reflect correct price values] , [Added in new signature], [long silo label wraps onto two lines]
 # Department and Desk  : Ops - Confirmations Team, Ops - Confirmations Team
 # Requester            : Mampho Dhlamini, Mampho Dhlamini
 # CR Number            : 645940, 697918, 891988, 656220


import ael, time
import reportlab.lib.pagesizes

from PIL                     import Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import *
from reportlab.lib.units     import cm, inch
from STATIC_TEMPLATE         import BuildLogos, BuildFooter, LetterOfPurchaseFooter
from reportlab.lib.colors    import black 
from zak_funcs               import formnum
from reportlab.lib           import colors

def PurchaseLetter(temp,t,TempLetter,*rest):
    
    TransactionDate = str(ael.date_from_time(t.creat_time).to_string("%d %B %Y"))
    DealNumber      = str(t.trdnbr)
    Tonnage         = str(t.quantity)
    InstrumentId    = t.insaddr.insid
    
    if t.counterparty_ptynbr:   
        Seller      = t.counterparty_ptynbr.ptyid
    else:
        Seller = ''     
        
    Silo = ''    
    for addinfo in t.additional_infos():
        if addinfo.addinf_specnbr.field_name == 'AgriSiloLocation':
            Silo = addinfo.value
            
    TransDiff = 0.0
    Price     = t.price
    
    sum=0.0

    for p in t.payments():
        if p.type=='Premium':
            sum+=p.amount

    if Price == 0.0:
        for addinfo in t.additional_infos():
            if addinfo.addinf_specnbr.field_name == 'AgriTransportDiff':
                TransDiff = float(addinfo.value)
                if TransDiff == 0.0:
                    Price     = formnum(sum/abs(t.quantity))
                else:
                    Price = formnum(sum/abs(t.quantity) - (TransDiff))
    else:
        Price     = formnum(t.price)
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
            SiloID     =  t.insaddr.insid[13:18] + ' ' + OptionType + ' ' + 'R'+ t.insaddr.insid[21:]        
        elif t.insaddr.insid[19] == 'C':
            OptionType = 'Call'
            SiloID     =  t.insaddr.insid[13:18] + ' ' + OptionType + ' ' + 'R'+ t.insaddr.insid[21:]        
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
        
        SiloID = 'FWD ' + ' ' + t.insaddr.insid[14:]
        Grade  = t.insaddr.und_insaddr.insid[13:]
    
    #Logos and Footer
    BuildLogos(TempLetter)
    BuildFooter(TempLetter)
    
    # Header
    TempLetter.setFillColor(black)
    TempLetter.setFont("Helvetica-Bold", 10.0)
    TempLetter.drawString(7.5 *cm, 24.5*cm, 'LETTER OF PURCHASE') 

    #Contact Details   
    TempLetter.setFont("Helvetica-Bold", 8.0)
    TempLetter.drawString(13.5 *cm, 23.5*cm, 'ABSA AGRICULTURAL COMMODITIES') 
    TempLetter.drawString(13.5 *cm, 23.0*cm, 'TEL: (011) 895 - 7592')  
    TempLetter.drawString(13.5 *cm, 22.5*cm, 'FAX: (011) 895 - 7822') 

    #Trade Details  
    TempLetter.drawString(13.5 *cm, 22.0*cm, 'DATE: ........................................................................')   
    TempLetter.drawString(13.5 *cm, 21.0*cm, 'DEAL NUMBER: ........................................................')  
    TempLetter.drawString(13.5 *cm, 20.5*cm, 'INSTRUMENT ID: ......................................................')  
    TempLetter.drawString( 2.0 *cm, 20.5*cm, 'BUYER: ABSA AGRICULTURAL COMMODITIES')   
    TempLetter.drawString( 2.0 *cm, 20.0*cm, 'SELLER:')    
    TempLetter.drawString( 2.0 *cm, 19.5*cm, 'ADDRESS OF SELLER:')    
    TempLetter.drawString( 2.0 *cm, 19.0*cm, 'TEL:')    
    TempLetter.drawString( 2.0 *cm, 18.5*cm, 'FAX:')
    
    TempLetter.drawString( 5.5 *cm, 20.0*cm, '.'*95)    
    TempLetter.drawString( 5.5 *cm, 19.5*cm, '.'*95)    
    TempLetter.drawString( 5.5 *cm, 19.0*cm, '.'*95)    
    TempLetter.drawString( 5.5 *cm, 18.5*cm, '.'*95)    
    
    TempLetter.setFont("Helvetica-Bold", 8.0)
    TempLetter.drawString(  2.0 *cm, 17.5*cm, 'PRODUCT')    
    TempLetter.drawString(  4.5 *cm, 17.5*cm, 'GRADE')    
    TempLetter.drawString(  6.5 *cm, 17.5*cm, 'TONNAGE')    
    TempLetter.drawString(  8.5 *cm, 17.5*cm, 'SILO/DETAIL')
    TempLetter.drawString( 14.5 *cm, 17.5*cm, 'AGRI DIFF')
    TempLetter.drawString( 16.5 *cm, 17.5*cm, 'PRICE, EX SILO, VAT EXCL.') 

   
    TempLetter.setFont("Helvetica", 8.0)
    TempLetter.drawString(15.0 *cm, 22.1*cm, TransactionDate) 
    TempLetter.drawString(16.0 *cm, 21.1*cm, DealNumber)  
    TempLetter.drawString(16.0 *cm, 20.6*cm, InstrumentId)  
    TempLetter.drawString( 5.5 *cm, 20.1*cm, Seller)
    TempLetter.drawString( 2.0 *cm, 17.1*cm, product)    
    TempLetter.drawString( 4.5 *cm, 17.1*cm, Grade)    
    TempLetter.drawString( 6.5 *cm, 17.1*cm, Tonnage)
    
    silo = ''
    if t.insaddr.instype == 'Future/Forward': 
        if Silo == 'SAFEX':
            Silo = ''
            #TempLetter.drawString( 8.5 *cm, 17.1*cm, SiloID + ' ' + Silo)
        else:    
            #TempLetter.drawString( 8.5 *cm, 17.1*cm, SiloID + ' ' + Silo)
            pass
        silo = SiloID + ' ' + Silo
    else:
        #TempLetter.drawString( 8.5 *cm, 17.1*cm, Silo + ' ' + SiloID)
        silo = Silo + ' ' + SiloID
    
    # get the rendered width
    text = TempLetter.beginText(3.5*cm, 20.6*cm)
    width = TempLetter.stringWidth(silo, text._fontname, text._fontsize)
    field_width = 6 * cm
    
    # check if the label fits
    if width <= field_width:
        # a fit, render the label
        TempLetter.drawString( 8.5 *cm, 17.1*cm, silo)
    else:
        # a misfit, split the string
        split_index = int((field_width / width) * len(silo))
        
        # find the rightmost space to the split point
        index = silo.rfind(' ', 0, split_index)
        if index == -1:
            # there is no space, split inside a word
            TempLetter.drawString( 8.5 *cm, 17.1*cm, silo[:split_index])
            TempLetter.drawString( 8.5 *cm, 16.7*cm, silo[split_index:])
        else:
            # split on the space found
            TempLetter.drawString( 8.5 *cm, 17.1*cm, silo[:index])
            TempLetter.drawString( 8.5 *cm, 16.7*cm, silo[index+1:])
        
    TempLetter.drawString(14.5 *cm, 17.1*cm, str(TransDiff))
    TempLetter.drawString(16.5 *cm, 17.1*cm, 'R'+ str(Price)) 

            
def PaymentAndDeliveryPurchase(temp,Letter,t,date,Time,InterestCost,TransDate,*rest):
    
    Letter.setFont("Helvetica-Bold", 8.0)   
    Letter.drawString(2.0 *cm, 15.0*cm, 'CANCELLATION:')    
    Letter.drawString(2.0 *cm, 13.0*cm, 'INTEREST COST:')
    Letter.drawString(2.0 *cm, 12.0*cm, 'PACKING:')
    Letter.drawString(2.0 *cm, 11.5*cm, 'STORAGE COST:')
    Letter.drawString(2.0 *cm, 11.0*cm, 'ADMIN-/ AND HANDLING FEES:')
    Letter.drawString(2.0 *cm, 10.5*cm, 'MOISTURE LEVEL:')
    Letter.drawString(2.0 *cm, 10.0*cm, 'TRANSACTION DATE:')
    Letter.drawString(2.0 *cm,  9.5*cm, 'FORCE MAJEUR:')
    Letter.drawString(2.0 *cm,  9.0*cm, 'PAYMENT:')
    
    Letter.setFont("Helvetica", 7.0)      
    Letter.drawString(6.5 *cm, 15.0*cm, 'On default of delivery of product by (date).................................. (time)........................... ABSA reserves the right to cancel the')    
    Letter.drawString(6.5 *cm, 14.5*cm, 'the transaction with the counterparty liable for any adverse price movements between transaction date and cancellation date.')    
    Letter.drawString(6.5 *cm, 14.0*cm, 'Should the SAFEX closing price of the near month be higher than the original transaction rate, ABSA will invoice the client') 
    Letter.drawString(6.5 *cm, 13.5*cm, 'with the full difference in consideration.') 
        
    Letter.drawString(6.5 *cm, 13.0*cm, "If payment has not been affected within ........... day/s after transaction date, interest will be charged at a rate of 2% above") 
    Letter.drawString(6.5 *cm, 12.5*cm, "ABSA's prime.") 
    
    Letter.drawString(6.5 *cm, 12.0*cm, "In bulk.") 
    
    Letter.drawString(6.5 *cm, 11.5*cm, "Storage cost is for the account of the seller up to the date of transaction/receipt of original silo certificate.") 
    
    Letter.drawString(6.5 *cm, 11.0*cm, "For the account of the seller.") 
        
    Letter.drawString(6.5 *cm, 10.5*cm, "Not more than 14% - payment on 12.5%") 
    
    Letter.drawString(6.5 *cm, 10.0*cm, "."*90) 
    Letter.drawString(6.5 *cm,  9.5*cm, "None.") 
        
    Letter.drawString(6.5 *cm,  9.0*cm, "Payment will only take place once the original silo certificate is received or confirmation is given by the silo owner.")  
    
    Letter.setFont("Helvetica", 7.0)      
    Letter.drawString(11.5 *cm, 15.1*cm, date) 
    Letter.drawString(14.5 *cm, 15.1*cm, Time) 
    Letter.drawString(11.2 *cm, 13.1*cm, InterestCost) 
    Letter.drawString(6.5 *cm,  10.1*cm, TransDate) 
    
    #End Of First Page
    Letter.showPage() 
 
    #BuildFooter(Letter)
    LetterOfPurchaseFooter(Letter)
       
    Letter.setFont("Helvetica-Bold", 8.0)
    Letter.drawString(2.0 *cm, 28.0*cm, "SILO CERTIFICATE:")
    
    Letter.setFont("Helvetica", 7.0)      
    Letter.drawString(2.0 *cm, 27.5*cm, "Does the client have the original silo certificate?") 
    
    Letter.setFont("Helvetica-Bold", 8.0)
    Letter.drawString(2.0 *cm, 27.0*cm, "YES") 
    Letter.drawString(2.0 *cm, 26.5*cm, "NO")
    
    Letter.drawString(3.5 *cm, 27.0*cm, "Silo certificate no.") 
    Letter.drawString(3.5 *cm, 26.5*cm, "Courier date")
    
    Letter.drawString(6.0 *cm, 27.0*cm, "."*40) 
    Letter.drawString(6.0 *cm, 26.5*cm, "."*40) 
 
    Letter.setFont("Helvetica", 7.0)      
    Letter.drawString(2.0 *cm, 25.5*cm, "If yes, the client needs to sign-off ownership on the silo certificate. The client needs to complete his name and sign 'transferor' and hand the silo certificate over to the")
    Letter.drawString(2.0 *cm, 25.0*cm, "branch. The branch must complete 'ABSA' and sign as 'transferee'. Thereafter the branch will courier the certificate to the address below. After ABSA Capital has received ")
    Letter.drawString(2.0 *cm, 24.5*cm, "the silo certificates/s, the client will be paid.")
    
    Letter.drawString(2.0 *cm, 23.5*cm, "If no, the client needs to sign-off ownership of the grain at the silo and ask them to confirm that the grain is registered in the name of ABSA Capital. After ABSA has")
    Letter.drawString(2.0 *cm, 23.0*cm, "received confirmation (silo certificate) the client will be paid.")
    
    Letter.setFont("Helvetica-Bold", 7.0)      
    Letter.drawString(2.0 *cm, 22.5*cm, "Banking details of seller:")
    
    Letter.setFont("Helvetica", 7.0)      
    Letter.drawString(2.0 *cm, 21.5*cm, "Bank:")
    Letter.drawString(2.0 *cm, 20.5*cm, "Branch:")
    
    Letter.drawString(10.0 *cm, 21.5*cm, "Account no:")
    Letter.drawString(10.0 *cm, 20.5*cm, "Branch code:")
    
    Letter.drawString(3.0 *cm, 21.5*cm, "."*70)
    Letter.drawString(3.0 *cm, 20.5*cm, "."*70)
    Letter.drawString(11.5 *cm, 21.5*cm, "."*70)
    Letter.drawString(11.5 *cm, 20.5*cm, "."*70)
    
    Letter.drawString(2.0 *cm, 20.0*cm, "Should there be any irregularities on the seller's side, ABSA reserves the right to hold the seller fully responsible for any losses that might occur.")
    Letter.drawString(2.0 *cm, 19.0*cm, "I (full name)  ........................................................................... hereby accept and commit myself to the terms and conditions applicable to this contract.")
    
    Letter.setFont("Helvetica-Bold", 8.0)      
    Letter.drawString(2.0 *cm, 18.0*cm, 'BANKING DETAILS: Bank ABSA Eloff Street. Account number: 660158642.') 

    Letter.setFont("Helvetica-Bold", 7.0)      
    Letter.drawString( 2.0 *cm, 13.0*cm, '_'*35) 
    Letter.drawString( 8.0 *cm, 13.0*cm, '_'*35)  
    Letter.drawString(14.0 *cm, 13.0*cm, '_'*35) 
    
    Letter.drawString( 3.0 *cm, 12.5*cm, 'ABSA Agricultural Commodities') 
    Letter.drawString( 9.0 *cm, 12.5*cm, 'Seller(Signature)') 
    Letter.drawString(16.0 *cm, 12.5*cm, 'Date') 
    
    Letter.setFont("Helvetica", 6.5)
    Letter.setStrokeColorRGB(1, 0, 0)
    Letter.drawInlineImage('Y:\Jhb\Arena\Data\Confirmations\Signatures\Trader.jpg', 1.1*inch, 5.2 *inch, 1.5*inch, 1.5*inch)
 
    Letter.drawString(6.0 *cm, 11.5*cm, 'PLEASE FAX COPY BACK TO THE FAX NUMBER MENTIONED ABOVE') 
    
    Letter.setFont("Helvetica-Bold", 7.0)      
    Letter.drawString(2.0 *cm, 10.5*cm, 'COURIER ADDRESS:') 
    Letter.drawString(2.0 *cm, 9.5*cm, 'ABSA Capital')
    Letter.drawString(2.0 *cm, 9.0*cm, '1W2')
    Letter.drawString(2.0 *cm, 8.5*cm, '180 Commissioner street')
    Letter.drawString(2.0 *cm, 8.0*cm, 'Johannesburg')
    Letter.drawString(2.0 *cm, 7.5*cm, 'SA')
    
    Letter.setFont("Helvetica-Bold", 5.0)      
    Letter.drawString(2.0 *cm, 5.5*cm, 'Authorised Financial Services Provider')
    Letter.drawString(2.0 *cm, 5.0*cm, 'ABSA Bank Limited Reg No 1986/004794/06')
    Letter.drawString(2.0 *cm, 4.5*cm, 'Trading as ABSA Capital')
    Letter.drawString(2.0 *cm, 4.0*cm, 'Vat 4940112230')
    
    #End Of Second Page
    Letter.showPage()
