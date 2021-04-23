'''
Developer   : Tshepo Mabena
Name        : EQD_ClientValuation_Main
Date        : 25/09/2009
Description : This module generates client valuations in pdf.

Updates:

Developer           : Tshepo Mabena
Purpose             : Rounding-off calculated fields to two decimal places and changing the date format of the trade date field. 
Department and Desk : Primes Services Collateral Management and Client Valuations
Requester           : Mduduzi Nhlapo
CR Number           : 243325
Date                : 03/03/2010 

'''

import acm, ael, os

from zak_funcs import formnum
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units     import cm, inch
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
from Landscape               import BuildLogos, BuildFooter 
from Disclaimer              import Disclaimer

def BuildHeader(temp,canvas,t,date,*rest):
    
    # Calls Logos and Footer 
    Logos  = BuildLogos(canvas)
    Footer = BuildFooter(canvas)
       
    canvas.setFont("Helvetica-Bold", 14.5) 
    canvas.drawString(0.8 * inch, 18.0*cm, 'Equity Derivatives Revaluation Report')
    
    canvas.setFont("Helvetica-Bold", 13.5) 
    canvas.drawString(0.8 * inch, 17.0*cm, t.counterparty_ptynbr.fullname)
    
    canvas.line(2.05*cm, 17.85*cm, 11.3*cm, 17.85*cm)
    
    canvas.setFont("Helvetica-Bold", 12.0)  
    canvas.drawString(0.8 * inch, 16.0*cm, 'Revaluation Date')
    canvas.drawString(2.5 * inch, 16.0*cm, date.to_string("%d %B %Y"))
    
    canvas.setFont("Helvetica-Bold", 10.0)  
    canvas.drawString(0.8 * inch, 14.5*cm, 'Option Type')
    canvas.drawString(2.2 * inch, 14.5*cm, 'Deal Number')
    canvas.drawString(3.6 * inch, 14.5*cm, 'Trade Date')
    canvas.drawString(5.2 * inch, 14.5*cm, 'Expiry Date')
    canvas.drawString(7.0 * inch, 14.5*cm, 'Strike Price')
    canvas.drawString(9.0 * inch, 14.5*cm, 'Nominal')
    canvas.drawString(11.0 * inch, 14.5*cm, 'MTM')
        
    canvas.line(2.05*cm, 14.2*cm, 30.0*cm, 14.2*cm)
    
    canvas.setFont("Times-Italic", 12.0)  
    canvas.drawString(3.5 *inch, 3.5*cm, "Please note that this revaluation is done from the bank's point of view so a negative is in the client's favour")
    

def BuildValuation(temp,t,date,valuation,Filter,*rest):
    
    ael.poll()
    
    y = 13.5
    sum = 0.0
    OptionType = ' '
    for t in Filter:
        if t.insaddr.instype == 'Option':
            
            if t.insaddr.call_option == 0:
                if t.quantity < 0:
                    OptionType = 'ShortPut'
                else:
                    if t.quantity > 0:
                        OptionType = 'LongPut'
            else:
                if t.insaddr.call_option == 1:
                    if t.quantity > 0:
                        OptionType = 'LongCall'
                if  t.insaddr.call_option == 1:
                    if t.quantity < 0:
                        OptionType = 'ShortCall'
        else:
            if t.insaddr.instype == 'Future/Forward': 
                if t.quantity > 0:
                    OptionType = 'LongExcluded'
                else:
                    OptionType = 'ShortExcluded'
                    
        Nominal = ''    
        if t.insaddr.instype == 'Option':
            Nominal = formnum(t.insaddr.und_insaddr.used_price(ael.date(date), 'ZAR', '', 0, 'SPOT')* t.nominal_amount())
        else:
            Nominal = formnum(t.nominal_amount())
            
        DealNumber  = t.trdnbr
        TradeDate   = str(ael.date_from_time(t.creat_time).to_string("%Y/%m/%d")) 
        ExpiryDay   = str(t.insaddr.exp_day.to_string("%Y/%m/%d"))
        StrikePrice = formnum(t.insaddr.strike_price)
        
        MTM_ZAR     = formnum(t.mtm_value_fo(ael.date(date), 'ZAR'))
        
        Total       = t.mtm_value_fo(ael.date(date), 'ZAR') 
        sum         = sum + Total
        
        valuation.setFont("Helvetica", 10.0)  
        valuation.drawString(0.8 * inch, y*cm, OptionType)
        valuation.drawString(2.2 * inch, y*cm, str(DealNumber))
        valuation.drawString(3.6 * inch, y*cm, TradeDate)
        valuation.drawString(5.2 * inch, y*cm, ExpiryDay)
        valuation.drawString(7.0 * inch, y*cm, str(StrikePrice))
        valuation.drawString(8.5 * inch, y*cm, 'ZAR '+Nominal)
        valuation.drawString(11.0 *inch, y*cm, MTM_ZAR)
        
        y = y - 0.5
        
        if y == 6.5:
            Temp = BuildHeader(1, valuation, t, date)
            valuation.showPage()
            y = 13.5
            
    TotalMTM = formnum(sum)        
        
    valuation.setFont("Helvetica-Bold", 10.0)
    valuation.drawString(10.65* inch, y*cm, 'ZAR '+' '+TotalMTM)
    
    Temp = BuildHeader(1, valuation, t, date) 
       
    valuation.showPage()
        
    Disclaimer(valuation)
    
    valuation.save()        
    
def Filter():

    filters = []
    for f in ael.TradeFilter:
        filters.append(f.fltid)
    filters.sort()
    
    return filters    
    
ael_variables = [('tf', 'TradeFilter:', 'string', Filter(), ''),
                ('trdnbr', 'Trade Number:', 'string', None, '0'),
                ('date', 'Date:', 'string', ael.date_today(), ael.date_today())]
                
def ael_main(dict):
    
    ClientName = ' '
    try:
        date = ael.date(dict['date'])
    except:
        func=acm.GetFunction('msgBox', 3)
        func("Warning", "Invalid Date!", 0)
        raise Exception("Warning", "Invalid Date!")
          
    if dict['trdnbr'] == '0' and dict['tf'] != '':
        tf = ael.TradeFilter[dict['tf']]
        for t in tf.trades():
            ClientName = t.counterparty_ptynbr.fullname
            break
            
    if dict['trdnbr'] != '0' and dict['tf'] == '':
            for trd in dict['trdnbr'].replace(' ', '').split(','):
                trade = ael.Trade[int(trd)]
                ClientName = trade.counterparty_ptynbr.fullname
                break
                
    print 'Loading...'
    PdfFile = 'Y:/Jhb/Arena/Data/PCG-Client-Valuations/Equity Derivatives/Client Valuation'+ '-'+ ClientName + '-'+ date.to_string('%d %b %Y') + '.pdf'
    pdf = Canvas(PdfFile, pagesize = (32*cm, 21*cm))
    
    TradeList = []
    
    if dict['trdnbr'] == '0' and dict['tf'] != '':
         
        tf = ael.TradeFilter[dict['tf']]
        for trd in tf.trades():
            if trd.insaddr.exp_day > date:
                TradeList.append(trd)
                if len(TradeList) == 0:
                    func=acm.GetFunction('msgBox', 3)
                    func("Warning", "No Valuation Report!", 0)
        BuildValuation(1, trd, date, pdf, TradeList)
       
    if dict['trdnbr'] != '0' and dict['tf'] == '':
        for trd in dict['trdnbr'].replace(' ', '').split(','):
            try:
                trade = ael.Trade[int(trd)]
                if trade.insaddr.exp_day > date:
                    TradeList.append(trade)
            except:
                func=acm.GetFunction('msgBox', 3)
                func("Warning", "Invalid Trade Number! No confirmation can be generated!", 0)
                break
        BuildValuation(1, trade, date, pdf, TradeList)
    
    if dict['trdnbr'] != '0' and dict['tf'] != '':
        func=acm.GetFunction('msgBox', 3)
        func("Warning", "Invalid Parameters! Client Valuation will not be generated!", 0)
        
    print 'Done...'
    pdf.save()  
    os.startfile(PdfFile)
